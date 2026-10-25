"""Cinco maneras de juntar 40 unidades en la parcela real de Ribera de Curtidores 31.

Coordenadas locales: origen UTM 439984 / 4473229.4 (EPSG:25830). La calle está al oeste (x ≈ 12–13);
la parcela tiene 14,98 m de frente y 49,5 m de fondo, y se estrecha hacia el este.

Alturas según el estudio de sol del 21 de diciembre (SOL_POR_ALTURA_ESTUDIO_PREVIO.json): a +16,4 m el 16,5 %
de la parcela tiene ≥ 2 h de sol; a +19,5 el 33 %; a +22,6 el 65 %; a +25,7 el 100 %.
"""
import glob
import json
import math
import os
import sys

import numpy as np
from shapely.geometry import Polygon, Point, box, shape
from shapely import affinity

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom3d import Pieza, COL, caja, cilindro, extruir, elipse, rect, tela_vertical, elipsoide, resta, mover, girar_z, anillo
from render import axon, planta_bn, seccion_bn, cortar
from rhino_out import Escritor

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
REPO = os.path.normpath(os.path.join(RAIZ, '..', '..'))
D_MOD, D_VIS, D_PLA, D_VER = [os.path.join(RAIZ, d) for d in ('modelos', 'vistas/uniones', 'planos', 'verificacion')]
for d in (D_MOD, D_VIS, D_PLA, D_VER):
    os.makedirs(d, exist_ok=True)

ORIGEN = (439984.0, 4473229.4)
PARCELA = Polygon([(21.56, 12.67), (41.56, 4.95), (47.17, 2.78), (51.69, 2.76), (61.45, 2.72), (61.55, -5.66), (58.92, -5.87),
                   (47.2, -6.82), (39.35, -7.46), (35.61, -7.48), (32.95, -7.47), (27.35, -7.42), (20.72, -7.46), (18.5, -7.47),
                   (17.18, -7.48), (16.9, -7.48), (13.28, -7.5), (12.07, 7.43), (20.5, 7.54)])
ALTURA_PLANTA = 3.1
SOL = {16.4: 16.5, 19.5: 33.4, 22.6: 65.2, 25.7: 100.0}
SX, SY = 3.45, 4.35


def contexto(radio=70):
    """Vecinos del Catastro extruidos por plantas sobre rasante (3,1 m por planta)."""
    p = [Pieza('parcela 650,9 m²', extruir(PARCELA, -0.3, 0.3), COL['parcela'], 'contexto::parcela')]
    ruta = glob.glob(os.path.join(REPO, 'G3-CODEX', '06_*', 'G3_CONTINUIDAD_PARCELA_2026-10-19', 'fuentes', 'CONTEXTO_CATASTRAL.geojson'))
    if not ruta:
        return p
    d = json.load(open(ruta[0]))
    c = PARCELA.centroid
    for f in d['features']:
        g = shape(f['geometry'])
        g = affinity.translate(g, -ORIGEN[0], -ORIGEN[1])
        if g.distance(c) > radio or g.intersects(PARCELA.buffer(-0.5)):
            continue
        n = f['properties'].get('plantas_sr', 0) or 0
        h = max(0.3, n * ALTURA_PLANTA)
        try:
            if g.geom_type == 'Polygon':
                g = g.buffer(0)
                p.append(Pieza(f"vecino {f['properties'].get('rc', '')[:7]} · {n} pl", extruir(g, 0, h), COL['vecino'], 'contexto::vecinos', 0.55))
        except Exception:
            pass
    return p


def comisiones_pb(z=0.0):
    """Las comisiones de Sol como programa de planta baja: cocina, lavadero, baños, taller, asamblea, acogida."""
    prog = [('acogida e información', 13.5, -7.0, 5.0, 4.0, 3.0), ('cocina y comedor', 19.5, -7.0, 9.0, 7.0, 3.5),
            ('lavandería y secado', 29.5, -7.0, 5.0, 4.5, 3.0), ('baños y duchas', 35.5, -7.0, 6.0, 4.5, 3.0),
            ('taller y herramientas', 42.5, -6.5, 8.0, 5.0, 3.5), ('asamblea', 51.5, -5.5, 9.0, 7.5, 4.0),
            ('cuidados · punto violeta', 14.0, 2.5, 5.0, 4.0, 3.0), ('biblioteca y coworking', 20.0, 2.0, 10.0, 5.0, 3.5)]
    out = []
    for n, x, y, dx, dy, h in prog:
        out.append(Pieza(n, caja(x, y, z, dx, dy, h), COL['comision'], 'comisiones', 0.8))
    return out


def bloque_unidad(x, y, z, rot=0, tipo='H3', nombre='unidad', capa='unidades', membrana=True):
    """Bloque simplificado de una unidad: plinto + superficie blanda + canto + aro de membrana."""
    p = []
    if tipo in ('H3', 'H4'):
        base = caja(0, 0, 0, SX, SY, 0.33)
        blando = caja(0, 0, 0.33, SX, SY, 0.12)
        canto = anillo(rect(-0.3, -0.3, SX + 0.6, SY + 0.6, 0.1), 0.3, 0, 0.45)
        piezas = [('plinto', base, COL['plinto'], 1.0), ('superficie', blando, COL['blando'] if tipo == 'H3' else COL['blando_calido'], 1.0), ('canto', canto, COL['canto'], 1.0)]
        if membrana:
            m = tela_vertical(list(elipse(SX / 2, SY / 2, SX / 2 + 0.5, SY / 2 + 0.5, 40).exterior.coords)[:-1], 0.45, 1.95)
            piezas.append(('membrana', m, COL['membrana'], 0.30))
    elif tipo == 'H5':
        piezas = [('15 m²', caja(0, 0, 0, SX, SY, 0.05), COL['suelo'], 1.0), ('colchón', caja(0.6, 1.0, 0.05, 2.1, 2.1, 0.12), COL['blando'], 1.0)]
        if membrana:
            t = elipsoide(1.65, 2.05, 0.05, 1.25, 1.25, 1.3)
            t = resta(t, caja(-1, -1, -3, 6, 7, 3.05))
            piezas.append(('tienda', t, COL['membrana'], 0.45))
        for (px, py) in [(0, 0), (SX, 0), (SX, SY), (0, SY)]:
            piezas.append(('poste', cilindro(px, py, 0, 0.03, 2.4, 8), COL['plinto'], 1.0))
    else:
        piezas = [('bloque', caja(0, 0, 0, SX, SY, 0.45), COL['blando'], 1.0)]
    for n, m, c, a in piezas:
        if rot:
            m = girar_z(m, rot, (SX / 2, SY / 2, 0))
        p.append(Pieza(f'{nombre} · {n}', mover(m, x - SX / 2, y - SY / 2, z), c, capa, a))
    return p


def empaquetar(poly, cw, ch, gap=0.6, margen=0.4, paso=0.25, rot=0, maximo=None):
    """Filas a lo largo de x; en cada fila se colocan celdas cw × ch (más holgura) donde quepan dentro del
    polígono. Se prueban varios desfases y se devuelve la mejor. Centros ordenados por x."""
    zona = poly.buffer(-margen)
    minx, miny, maxx, maxy = zona.bounds
    w, h = (cw + gap, ch + gap) if rot == 0 else (ch + gap, cw + gap)
    mejores = []
    for oy in np.arange(0, h, paso):
        cs = []
        y = miny + oy + h / 2
        while y + h / 2 <= maxy + 1e-6:
            x = minx + w / 2
            while x + w / 2 <= maxx + 1e-6:
                cel = box(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
                if zona.contains(cel):
                    cs.append((x, y))
                    x += w
                else:
                    x += paso
            y += h
        if len(cs) > len(mejores):
            mejores = cs
    mejores.sort()
    return mejores[:maximo] if maximo else mejores


def troncos(poly, z_top, paso=8.0, r=0.3, capa='estructura'):
    out = []
    minx, miny, maxx, maxy = poly.bounds
    for x in np.arange(minx + 3, maxx, paso):
        for y in np.arange(miny + 3, maxy, paso):
            if poly.buffer(-1.5).contains(Point(x, y)):
                out.append(Pieza('tronco', cilindro(x, y, 0, r, z_top, 10), COL['tronco'], capa))
    return out


def bandeja(poly, z, capa='bandejas', nombre='bandeja', e=0.45):
    return Pieza(f'{nombre} +{z:.1f}', extruir(poly, z - e, e), COL['plinto'], capa, 0.9)


def con_cielo(unidades, bandejas):
    """Una unidad tiene cielo si ninguna bandeja más alta contiene su centro."""
    res = []
    for (x, y, z) in unidades:
        libre = all(not (bz > z + 0.5 and bp.contains(Point(x, y))) for bp, bz in bandejas)
        res.append(libre)
    return res


# ---------------------------------------------------------------------------

def U1_campo():
    """U1 · El campo. Una sola superficie continua (Supersuperficie) a +22,6 m sobre toda la parcela; las
    membranas son la única partición. Lo que no cabe en una bandeja sube a una segunda sobre el fondo."""
    capa = 'U1_campo'
    p = []
    poly = PARCELA
    z1 = 22.6
    centros = empaquetar(poly, SX + 0.6, SY + 0.6, gap=0.8, margen=0.2, rot=90)
    bandejas = [(poly, z1)]
    p.append(bandeja(poly, z1, capa + '::bandejas', 'campo'))
    unidades = [(x, y, z1) for (x, y) in centros[:40]]
    n1 = len(unidades)
    nivel = 1
    while len(unidades) < 40 and nivel < 6:
        zk = z1 + 6.2 * nivel
        p.append(bandeja(poly, zk, capa + '::bandejas', f'campo {nivel + 1}'))
        bandejas.append((poly, zk))
        for (x, y) in centros[:40 - len(unidades)]:
            unidades.append((x, y, zk))
        nivel += 1
    z2 = z1 + 6.2 * (nivel - 1)
    for i, (x, y, z) in enumerate(unidades):
        p += bloque_unidad(x, y, z, 90, 'H3', f'U{i + 1:02d}', capa + '::unidades')
    p += troncos(poly, z2 if n1 < 40 else z1, 8.0, capa=capa + '::troncos')
    p += comisiones_pb()
    cielo = con_cielo(unidades, bandejas)
    info = dict(id='U1', nombre='El campo', unidades=len(unidades), en_primera_bandeja=n1, con_cielo=sum(cielo), alturas=sorted(set(round(z, 1) for _, _, z in unidades)),
                bandeja_m2=round(poly.area, 1), nota='Una bandeja de 650,9 m² admite unas 18 superficies de 15 m² con canto y paso (la parcela tiene 15 m de ancho: solo tres filas). Para 40 hacen falta dos campos, y el de abajo pierde el cielo.')
    return p, info, unidades


def U2_terrazas():
    """U2 · Las terrazas. Diez bandejas de 4,65 m de fondo que suben de oeste a este, de +16,4 a +25,7, para
    que ninguna tape el cielo de la anterior. Como en la megaestructura: bandejas y troncos."""
    capa = 'U2_terrazas'
    p = []
    minx, miny, maxx, maxy = PARCELA.bounds
    x0 = minx + 1.0
    prof = SY + 0.55
    n_band = int((maxx - x0) // prof)
    unidades, bandejas = [], []
    for k in range(n_band):
        tira = PARCELA.intersection(box(x0 + k * prof, miny - 1, x0 + (k + 1) * prof, maxy + 1))
        if tira.is_empty or tira.area < 10:
            continue
        z = 16.4 + k * (9.3 / max(1, n_band - 1))
        p.append(bandeja(tira, z, capa + '::bandejas', f'terraza {k + 1}'))
        bandejas.append((tira, z))
        cs = empaquetar(tira, SX, SY, gap=0.25, margen=0.12, rot=90)
        for (x, y) in cs:
            if len(unidades) < 40:
                unidades.append((x, y, z))
    n_terr = len(unidades)
    if n_terr < 40:
        # las que faltan, en una bandeja alta sobre las dos primeras terrazas
        sub = PARCELA.intersection(box(x0, miny - 1, x0 + 3 * prof, maxy + 1))
        z = 25.7 + 3.6
        p.append(bandeja(sub, z, capa + '::bandejas', 'bandeja alta'))
        bandejas.append((sub, z))
        for (x, y) in empaquetar(sub, SX, SY, gap=0.25, margen=0.12, rot=90):
            if len(unidades) < 40:
                unidades.append((x, y, z))
    for i, (x, y, z) in enumerate(unidades):
        p += bloque_unidad(x, y, z, 90, 'H3', f'U{i + 1:02d}', capa + '::unidades')
    p += troncos(PARCELA, 25.7, 7.0, capa=capa + '::troncos')
    p += comisiones_pb()
    cielo = con_cielo(unidades, bandejas)
    info = dict(id='U2', nombre='Las terrazas', unidades=len(unidades), en_terrazas=n_terr, con_cielo=sum(cielo), alturas=sorted(set(round(z, 1) for _, _, z in unidades)),
                nota='Diez terrazas escalonadas: cada una ve el cielo porque la siguiente está detrás y más alta. La parcela se estrecha al fondo y allí caben menos.')
    return p, info, unidades


def U3_racimos():
    """U3 · Los racimos de comisión. Cinco grupos de ocho alrededor de una comisión (cocina, lavandería, baños,
    taller, asamblea), en cinco niveles que alternan oeste y este."""
    capa = 'U3_racimos'
    p = []
    minx, miny, maxx, maxy = PARCELA.bounds
    comis = ['cocina', 'lavandería', 'baños y duchas', 'taller', 'asamblea']
    unidades, bandejas = [], []
    k = -1
    while len(unidades) < 40 and k < 7:
        k += 1
        lado = k % 2
        xa = minx + 1 + lado * 19.0
        sub = PARCELA.intersection(box(xa, miny - 1, xa + 19.0, maxy + 1))
        z = 16.4 + k * 3.1
        p.append(bandeja(sub, z, capa + '::bandejas', f'racimo {k + 1}'))
        bandejas.append((sub, z))
        cx, cy = sub.centroid.x, sub.centroid.y
        # comisión en el centro del racimo
        p.append(Pieza(f'comisión · {comis[k % 5]}', cilindro(cx, cy, z, 2.6, 3.0, 24), COL['comision'], capa + '::comisiones', 0.85))
        # ocho unidades alrededor, de pie hacia la comisión
        n_ok = 0
        for j in range(8):
            a = 2 * math.pi * j / 8 + math.pi / 8
            r = 5.6
            x, y = cx + r * math.cos(a), cy + r * math.sin(a)
            cel = affinity.rotate(box(x - SX / 2, y - SY / 2, x + SX / 2, y + SY / 2), math.degrees(a) + 90, origin=(x, y))
            if sub.buffer(0.6).contains(cel) and len(unidades) < 40:
                unidades.append((x, y, z))
                p += bloque_unidad(x, y, z, math.degrees(a) + 90, 'H3', f'R{k + 1}-{j + 1}', capa + '::unidades')
                n_ok += 1
    p += troncos(PARCELA, 16.4 + k * 3.1, 7.0, capa=capa + '::troncos')
    p += comisiones_pb()
    cielo = con_cielo(unidades, bandejas)
    info = dict(id='U3', nombre='Los racimos de comisión', unidades=len(unidades), con_cielo=sum(cielo), alturas=sorted(set(round(zz, 1) for _, _, zz in unidades)), racimos=k + 1,
                nota='Un anillo de ocho alrededor de una comisión necesita unos 17 m de diámetro y la parcela tiene 15: los anillos pierden unidades en los bordes.')
    return p, info, unidades


def U4_torre_de_turnos():
    """U4 · La torre de turnos. Veinte superficies H4 para cuarenta personas, en una torre estrecha sobre el
    frente de 14,98 m; cuarenta armarios-maleta abajo; las comisiones ocupan el resto de la parcela a cota 0."""
    capa = 'U4_torre'
    p = []
    minx, miny, maxx, maxy = PARCELA.bounds
    unidades, bandejas = [], []
    huella = box(13.6, -7.0, 13.6 + 2 * (SY + 0.6) + 0.6, -7.0 + 2 * (SX + 0.6) + 0.6)
    for k in range(5):
        z = 16.4 + k * 3.3
        p.append(bandeja(huella, z, capa + '::bandejas', f'nivel {k + 1}'))
        bandejas.append((huella, z))
        for i in range(2):
            for j in range(2):
                x = 13.6 + 0.6 + (SY + 0.6) * i + SY / 2
                y = -7.0 + 0.6 + (SX + 0.6) * j + SX / 2
                unidades.append((x, y, z))
                p += bloque_unidad(x, y, z, 90, 'H4', f'T{k + 1}-{i * 2 + j + 1}', capa + '::unidades')
    # cuarenta armarios-maleta en planta baja
    for n in range(40):
        p.append(Pieza(f'armario {n + 1}', caja(14 + (n % 20) * 0.7, 3.5 + (n // 20) * 0.9, 0, 0.6, 0.6, 2.0), COL['dock'], capa + '::armarios'))
    for (x, y) in [(14.5, -6.5), (23.5, -6.5), (14.5, 1.5), (23.5, 1.5)]:
        p.append(Pieza('tronco', cilindro(x, y, 0, 0.4, 16.4 + 4 * 3.3, 12), COL['tronco'], capa + '::troncos'))
    p += comisiones_pb()
    cielo = con_cielo(unidades, bandejas)
    info = dict(id='U4', nombre='La torre de turnos', unidades=len(unidades), personas=2 * len(unidades), con_cielo=sum(cielo), alturas=[16.4 + k * 3.3 for k in range(5)],
                nota='Veinte superficies, cuarenta personas, media parcela libre. Solo el último nivel ve el cielo en vertical; los demás, por la fachada. Choca con el mínimo de 15 m² por unidad privativa si la unidad es de una persona.')
    return p, info, unidades


def U5_plaza():
    """U5 · La plaza-acampada. Una bandeja-plaza a +22,6 con docks H5 (bastidor, enchufe, armario y colchón);
    cada persona trae su tienda. Las comisiones son tiendas más grandes en la misma plaza."""
    capa = 'U5_plaza'
    p = []
    poly = PARCELA
    z = 22.6
    p.append(bandeja(poly, z, capa + '::bandejas', 'plaza'))
    centros = empaquetar(poly, SX, SY, gap=0.9, margen=0.3, rot=90)
    unidades = [(x, y, z) for (x, y) in centros[:40]]
    n1 = len(unidades)
    nivel = 1
    while len(unidades) < 40 and nivel < 6:
        p.append(bandeja(poly, z + 6.2 * nivel, capa + '::bandejas', f'plaza {nivel + 1}'))
        for (x, y) in centros[:40 - len(unidades)]:
            unidades.append((x, y, z + 6.2 * nivel))
        nivel += 1
    for i, (x, y, zz) in enumerate(unidades):
        p += bloque_unidad(x, y, zz, 90, 'H5', f'D{i + 1:02d}', capa + '::docks', membrana=(i % 3 != 2))
    # comisiones como tiendas grandes en la plaza (donde quede sitio) y en planta baja
    zt = max(zz for _, _, zz in unidades)
    libres = centros[40 - n1:] if n1 < 40 else centros[40:]
    for n, (x, y) in zip(['cocina', 'cuidados', 'asamblea'], libres):
        t = elipsoide(x, y, zt, 2.6, 2.6, 2.6)
        t = resta(t, caja(x - 5, y - 5, zt - 6, 10, 10, 6))
        p.append(Pieza(f'tienda común · {n}', t, COL['comision'], capa + '::comisiones', 0.6))
    p += troncos(poly, z, 8.0, capa=capa + '::troncos')
    p += comisiones_pb()
    info = dict(id='U5', nombre='La plaza-acampada', unidades=len(unidades), en_primera_plaza=n1, con_cielo=sum(1 for _, _, zz in unidades if zz == max(q[2] for q in unidades)), alturas=sorted(set(round(zz, 1) for _, _, zz in unidades)), docks_posibles=len(centros),
                nota='Sin canto ni membrana fija caben algo más docks que superficies H3, pero tampoco 40: hace falta una segunda plaza. Cada tienda es de quien la trae. Es Sol literal, a +22,6 m.')
    return p, info, unidades


UNIONES = [U1_campo, U2_terrazas, U3_racimos, U4_torre_de_turnos, U5_plaza]


def main():
    ctx = contexto()
    w = Escritor('G3 · uniones de 40 unidades en Ribera de Curtidores 31 · coordenadas locales (origen UTM 439984 / 4473229.4) · metros')
    for c in ctx:
        w.malla(c)
    resumen = []
    for k, f in enumerate(UNIONES):
        p, info, unidades = f()
        uid, nombre = info['id'], info['nombre']
        tit = f'{uid} · {nombre}'
        print(uid, nombre, info['unidades'], 'con cielo', info['con_cielo'])
        sub = f"{info['unidades']} unidades · {info['con_cielo']} con cielo en vertical · alturas {', '.join(f'+{z:.1f}' for z in info['alturas'])}"
        axon(ctx + p, f'{D_VIS}/{uid}_contexto.png', titulo=tit, subtitulo=sub + ' · con los vecinos del Catastro', az=235, el=26, ancho_cm=36, alto_cm=22)
        axon([c for c in ctx if 'parcela' in c.capa] + p, f'{D_VIS}/{uid}_solo.png', titulo=tit, subtitulo=sub, az=235, el=30, ancho_cm=36, alto_cm=22)
        axon([c for c in ctx if 'parcela' in c.capa] + p, f'{D_VIS}/{uid}_desde_la_calle.png', titulo=tit, subtitulo=sub + ' · desde Ribera de Curtidores', az=180, el=18, ancho_cm=30, alto_cm=22)
        zmax = max(z for _, _, z in unidades)
        planta_bn(p + [c for c in ctx if 'parcela' in c.capa], zmax + 1.2, f'{D_PLA}/{uid}_planta_1_250.png', escala=250, titulo=f'{tit} · planta a +{zmax + 1.2:.1f}',
                  nota='corte por el nivel más alto de unidades · lo de debajo en proyección', hoja_cm=(42.0, 29.7))
        seccion_bn(p + ctx, f'{D_PLA}/{uid}_seccion_1_250.png', origen=[30, 0, 0], normal=[0, 1, 0], escala=250, titulo=f'{tit} · sección longitudinal por y = 0',
                   nota='mirando a +y · vecinos del Catastro en proyección', hoja_cm=(42.0, 29.7))
        dx = k * 90.0
        for q in p:
            w.malla(q.copia(dx=dx), prefijo=f'{uid}::')
        for c in ctx:
            if 'vecinos' in c.capa and k > 0:
                pass
        w.vista(uid, (dx - 60, -70, 60), (dx + 37, 0, 15))
        resumen.append(info)
    w.guardar(f'{D_MOD}/UNIONES_U1_U5.3dm')
    json.dump(resumen, open(f'{D_VER}/UNIONES.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(resumen, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
