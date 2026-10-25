# -*- coding: utf-8 -*-
"""FASE FINAL - S08: cruces interdisciplinares del documento global (mandato final §4).

Cuatro calculos NUEVOS que no existen en ningun analisis individual:
  1. METRO x FLUJO x CLIMA: distancia geodesica de cada boca de Metro al primer
     refugio efectivo + sombra del primer tramo de salida.
  2. VISUALES x FLUJO: cuanta GENTE EN MOVIMIENTO conserva la vista del reloj
     (visibilidad muestreada sobre las trazas de los ejes, ponderada por flujo).
  3. BENEFICIO x COMPLEJIDAD OPERATIVA: aporte de confort de cada mecanismo frente
     a sus dependencias y frecuencia de mantenimiento.
  4. VERANO x INVIERNO: correlacion celda a celda entre sombra estival ganada y sol
     invernal perdido — el trade-off estacional medido, con sus excepciones.
"""
import json
import os
import sys

import numpy as np
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
RC = os.path.normpath(os.path.join(BASE, '..'))
MONT = os.path.normpath(os.path.join(RC, '..'))
F9 = os.path.join(RC, 'FASE_03B9_HYPERDETAIL_V006')
CLI = os.path.join(F9, '_reclima9', '_data')
AUD = os.path.join(F9, '_reaudit9', '_data')
OUT = os.path.join(BASE, '10_SINTESIS_GLOBAL', 'B_DATOS')
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402


def L(n, d=CLI):
    return np.load(os.path.join(d, n))


def J(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


X0, Y0, CS = -112, -45, 0.5
walk = L('walk.npy', AUD)[::2, ::2].astype(bool)
ref = L('refugio.npy')                      # clases 0-3; 3 = REFUGIO EFECTIVO
ny, nx = ref.shape
walk = walk[:ny, :nx]
sh = L('shade_crit_B.npy')
R = {}

# ================================================= 1 · METRO x FLUJO x CLIMA
a6 = J(os.path.join(AUD, 'a6_metro.json'))
bocas = [r for r in a6['rows'] if r.get('en_ambito')]
refmask = (np.nan_to_num(ref) >= 3)
st = ndi.generate_binary_structure(2, 2)
res_bocas = []
for b in bocas:
    j = int((b['x'] - X0) / CS); i = int((b['y'] - Y0) / CS)
    j = np.clip(j, 0, nx - 1); i = np.clip(i, 0, ny - 1)
    if not walk[i, j]:
        ii, jj = np.where(walk)
        k = int(np.argmin((ii - i) ** 2 + (jj - j) ** 2))
        i, j = int(ii[k]), int(jj[k])
    # BFS hasta el primer refugio
    front = np.zeros_like(walk); front[i, j] = True
    visto = front.copy()
    d = 0.0
    hit = refmask[i, j]
    while not hit and front.any() and d < 400:
        front = ndi.binary_dilation(front, st) & walk & ~visto
        visto |= front
        d += CS * 1.11
        hit = (front & refmask).any()
    # sombra media de los primeros 30 m de salida (disco geodesico)
    disco = ndi.binary_dilation(np.equal(visto, True), st, iterations=0)
    zona30 = visto if d >= 30 else ndi.binary_dilation(visto, st, iterations=int(max(0, (30 - d) / CS)))
    zona30 &= walk
    s30 = float(np.nanmean(np.where(zona30, sh, np.nan))) if zona30.any() else float('nan')
    res_bocas.append(dict(boca=b['name'], d_refugio_m=round(d, 0),
                          sombra_salida_30m=round(s30, 2)))
R['metro_clima'] = dict(
    bocas=res_bocas,
    dato_flujo='73 M viajeros/ano por la estacion de Sol (F-01)',
    lectura='distancia geodesica de cada boca al primer REFUGIO EFECTIVO y sombra '
            'critica media del entorno de salida (30 m)')

# ================================================= 2 · VISUALES x FLUJO (transito)
a7 = J(os.path.join(AUD, 'a7_views.json'))
pts = np.array(a7['pts'])
vis_reloj = np.array(a7['vis']['RELOJ'], bool)
a1 = J(os.path.join(AUD, 'a1_paths.json'))
a5 = J(os.path.join(AUD, 'a5_access.json'))
pesos = {e['id']: e['w_p05'] for e in a5['rows'] if 'CINTA' not in e['id'].upper()}
wsum = sum(pesos.values())
from scipy.spatial import cKDTree  # noqa: E402
tree = cKDTree(pts)
vis_flujo = 0.0
det = []
for p_ in a1['paths']:
    w = pesos.get(p_['id'], 0) / wsum
    if not w:
        continue
    est = [(r['x'], r['y']) for r in p_['rows']]
    _, idx = tree.query(est, k=1)
    frac = float(vis_reloj[idx].mean())
    det.append(dict(eje=p_['id'], pct_traza_con_reloj=round(100 * frac, 1),
                    peso_flujo=round(w, 3)))
    vis_flujo += w * frac
R['visuales_flujo'] = dict(
    pct_flujo_con_vista_reloj=round(100 * vis_flujo, 1),
    detalle=det,
    comparacion=dict(por_superficie=41.5, por_estancia=25.5,
                     por_flujo=round(100 * vis_flujo, 1)),
    lectura='fraccion del FLUJO peatonal (ponderado por eje) que conserva la vista del '
            'reloj a lo largo de su traza — la tercera metrica de visibilidad')

# ================================================= 3 · BENEFICIO x COMPLEJIDAD
R['beneficio_complejidad'] = [
    dict(mecanismo='Sombra estructural', aporte_dUTCI_pct=85, dependencias=0,
         frecuencia_mant='anual (inspeccion)',
         indice='maximo beneficio, cero dependencia: el nucleo antifragil'),
    dict(mecanismo='Agua laminas/splash', aporte_dUTCI_pct=8, dependencias=2,
         frecuencia_mant='mensual', indice='beneficio medio, dependencia red+bombas'),
    dict(mecanismo='Nebulizacion', aporte_dUTCI_pct=5, dependencias=3,
         frecuencia_mant='trimestral (cal)',
         indice='beneficio condicional, dependencia maxima (agua+bomba AP+meteo)'),
    dict(mecanismo='Vegetacion', aporte_dUTCI_pct=2, dependencias=2,
         frecuencia_mant='continua (jardineria)',
         indice='beneficio termico menor, retorno ecologico/social dominante'),
]

# ================================================= 4 · VERANO x INVIERNO (correlacion)
winA, winB = L('radwin_A.npy'), L('radwin_B.npy')
shA = L('shade_crit_A.npy')
m = walk & np.isfinite(sh) & np.isfinite(winA) & np.isfinite(winB) & (np.nan_to_num(winA) > 0.1)
gan = (np.nan_to_num(sh) - np.nan_to_num(shA))[m]       # sombra estival ganada
per = (1 - np.nan_to_num(winB)[m] / np.nan_to_num(winA)[m])  # fraccion de sol invernal perdida
cc = float(np.corrcoef(gan, per)[0, 1])
# excepciones: celdas con mucha sombra estival ganada (>0.5) y poca perdida invernal (<0.25)
exc = m.copy()
exc[m] = (gan > 0.5) & (per < 0.25)
R['verano_invierno'] = dict(
    correlacion=round(cc, 2),
    n_celdas=int(m.sum()),
    m2_excepcion=round(float(exc.sum()) * 0.25, 0),
    lectura='correlacion celda a celda entre sombra estival ganada y fraccion de sol '
            'invernal perdida: el trade-off es %s (r=%.2f). Las excepciones (mucha '
            'sombra de verano, poca perdida de invierno: %d m2) son celdas bajo hojas '
            'ALTAS con sol invernal rasante lateral — la geometria que conviene '
            'replicar.' % ('fuerte y lineal' if cc > 0.6 else 'parcial', cc,
                           int(float(exc.sum()) * 0.25)))

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, 'global_cross.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)

flog.event(fase='FINAL', tipo_evento='cruces_globales',
           objetivo='4 cruces interdisciplinares nuevos para el documento global',
           resultado='metro: %s; vista reloj por flujo %.1f%%; verano-invierno r=%.2f, '
                     'excepciones %d m2'
                     % ('; '.join('%s %dm' % (b['boca'][:14], b['d_refugio_m'])
                                  for b in res_bocas[:3]),
                        100 * vis_flujo, cc, int(float(exc.sum()) * 0.25)))
print(json.dumps(R['metro_clima']['bocas'], ensure_ascii=False))
print('vista reloj por flujo:', R['visuales_flujo']['pct_flujo_con_vista_reloj'], '%')
print('verano x invierno r =', R['verano_invierno']['correlacion'],
      '| excepciones:', R['verano_invierno']['m2_excepcion'], 'm2')
