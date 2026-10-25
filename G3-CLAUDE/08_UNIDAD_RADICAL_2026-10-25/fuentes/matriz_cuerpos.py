"""Matriz cuerpos × unidades: qué exige cada cuerpo y qué da cada unidad. Reglas explícitas, no juicio."""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cuerpos import CATALOGO
from unidades import UNIDADES

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
D_VER = os.path.join(RAIZ, 'verificacion')

# Lo que da cada unidad (lectura del modelo)
DA = {
    'H1': dict(asiento=0.45, cierre='parcial', sonido='no', zonas_temp=False, cielo=True, suelo_llano=True, luz_propia=True),
    'H2': dict(asiento=0.45, cierre='total', sonido='si', zonas_temp=False, cielo=True, suelo_llano=False, luz_propia=True),
    'H3': dict(asiento=0.45, cierre='total', sonido='parcial', zonas_temp=True, cielo=True, suelo_llano=False, luz_propia=True),
    'H4': dict(asiento=0.45, cierre='total', sonido='parcial', zonas_temp=True, cielo=True, suelo_llano=False, luz_propia=True),
    'H5': dict(asiento=0.12, cierre='parcial', sonido='no', zonas_temp=False, cielo=False, suelo_llano=True, luz_propia=False),
    'H6': dict(asiento=0.42, cierre='parcial', sonido='parcial', zonas_temp=True, cielo=True, suelo_llano=False, luz_propia=True),
}
ORDEN_CIERRE = {'abierto': 0, 'parcial': 1, 'total': 2}


def cabe_tumbada(bw, bh, largo, ancho):
    if (bw >= largo and bh >= ancho) or (bh >= largo and bw >= ancho):
        return True
    d = math.hypot(bw, bh)
    if d >= largo:
        # anchura disponible perpendicular a la diagonal
        return (bw * bh / d) >= ancho
    return False


def evaluar(c, info):
    bx, by, bw, bh = info['blando']
    da = DA[info['id']]
    r = {}
    r['tumbada'] = cabe_tumbada(bw, bh, c.largo_tumbada, c.ancho_tumbada)
    r['dos'] = (min(bw, bh) >= c.ancho_dos and max(bw, bh) >= c.largo_tumbada)
    r['seis_sentadas'] = bw * bh >= 6.0 and min(bw, bh) >= 2.2
    lo, hi = c.canto_sentarse
    r['canto'] = lo <= da['asiento'] <= hi
    r['cierre'] = ORDEN_CIERRE[da['cierre']] >= ORDEN_CIERRE[c.cierre]
    r['sonido'] = True if c.libido != 'alta' and c.id not in ('C12',) else da['sonido'] in ('si',) or (da['sonido'] == 'parcial' and c.libido != 'alta')
    r['temperatura'] = True if c.temperatura == 'media' else (da['zonas_temp'] or (c.temperatura == 'frio' and da['cierre'] == 'total') or (c.temperatura == 'calor' and not da['cielo'] is False and da['cierre'] != 'total'))
    if c.movilidad == 'reducida':
        r['movilidad'] = da['suelo_llano'] and da['asiento'] <= 0.12 or info['id'] in ('H1', 'H3', 'H4')  # transferencia desde el paso
    elif c.movilidad == 'dolor':
        r['movilidad'] = da['asiento'] >= 0.42
    else:
        r['movilidad'] = True
    r['vestirse_dentro'] = da['cierre'] == 'total' and da['luz_propia']
    r['perro'] = (bw * bh >= 8) if c.id == 'C16' else True
    n_ok = sum(1 for v in r.values() if v)
    return r, n_ok, len(r)


def main():
    unidades = []
    for f in UNIDADES:
        _, _, info = f()
        unidades.append(info)
    filas = []
    for c in CATALOGO:
        fila = dict(cuerpo=c.id, nombre=c.nombre, estatura=c.estatura, exige=dict(largo=round(c.largo_tumbada, 2), ancho=round(c.ancho_tumbada, 2),
                    dos=round(c.ancho_dos, 2), canto=c.canto_sentarse, cierre=c.cierre, temperatura=c.temperatura, libido=c.libido, movilidad=c.movilidad), unidades={})
        for info in unidades:
            r, n, t = evaluar(c, info)
            fila['unidades'][info['id']] = dict(ok=n, de=t, detalle=r)
        filas.append(fila)
    json.dump(filas, open(f'{D_VER}/CUERPOS_X_UNIDADES.json', 'w'), ensure_ascii=False, indent=1)
    # markdown
    ids = [u['id'] for u in unidades]
    L = ['# Cuerpos × unidades\n', 'Cada celda: criterios cumplidos de 10 (tumbada · dos · seis sentadas · canto · cierre · sonido · temperatura · movilidad · vestirse dentro · perro). Reglas en `fuentes/matriz_cuerpos.py`; las medidas de los cuerpos son hipótesis.\n',
         '| cuerpo | exige | ' + ' | '.join(ids) + ' |', '|---|---|' + '---|' * len(ids)]
    tot = {i: 0 for i in ids}
    for fila in filas:
        e = fila['exige']
        ex = f"{e['largo']} × {e['ancho']} m · canto {e['canto'][0]}–{e['canto'][1]} · cierre {e['cierre']} · {e['temperatura']}"
        celdas = []
        for i in ids:
            u = fila['unidades'][i]
            falla = [k for k, v in u['detalle'].items() if not v]
            celdas.append(f"**{u['ok']}**" + (f" ({', '.join(falla)})" if falla else ''))
            tot[i] += u['ok']
        L.append(f"| {fila['cuerpo']} {fila['nombre']} | {ex} | " + ' | '.join(celdas) + ' |')
    L.append('| **total** | | ' + ' | '.join(f'**{tot[i]}** / {10 * len(filas)}' for i in ids) + ' |')
    open(f'{D_VER}/CUERPOS_X_UNIDADES.md', 'w').write('\n'.join(L) + '\n')
    print({i: tot[i] for i in ids})


if __name__ == '__main__':
    main()
