# -*- coding: utf-8 -*-
"""FASE FINAL - MOTOR DE MOVILIDAD (MOB-01..04) sobre v006 build 12.

Nuevos calculos sobre los rasters de la auditoria:
  - distancia geodesica de cada celda pisable al acceso mas cercano (evacuacion basica);
  - escenario de fallo de ascensor (PMR): rodeo maximo entre ascensores del tablero;
  - LOS peatonal por eje en 3 escenarios de afluencia (C: hipotesis declaradas).
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
AUD = os.path.join(F9, '_reaudit9', '_data')
OUT = os.path.join(BASE, '02_MOVILIDAD_Y_ACCESIBILIDAD', 'B_DATOS')
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402

CELL = 0.25
X0, Y0 = -112, -45


def J(n):
    with open(os.path.join(AUD, n), encoding='utf-8') as f:
        return json.load(f)


walk = np.load(os.path.join(AUD, 'walk.npy')).astype(bool)
a1 = J('a1_paths.json')
a5 = J('a5_access.json')
a4 = J('a4_ribbon.json')

# --------------------------------------------------- 1 · distancia geodesica a accesos
acc = a1['access']                    # 10 extremos de los 5 ejes
pts = [(k, v[0], v[1]) for k, v in acc.items()]
seed = np.zeros_like(walk)
for _, ax_, ay_ in pts:
    j = int((ax_ - X0) / CELL)
    i = int((ay_ - Y0) / CELL)
    j = np.clip(j, 0, walk.shape[1] - 1)
    i = np.clip(i, 0, walk.shape[0] - 1)
    # ancla al pisable mas cercano (el extremo declarado puede caer fuera del raster util)
    if not walk[i, j]:
        ii, jj = np.where(walk)
        d2 = (ii - i) ** 2 + (jj - j) ** 2
        k = int(np.argmin(d2))
        i, j = int(ii[k]), int(jj[k])
    seed[i, j] = True

# BFS geodesico por dilatacion iterativa (paso = 1 celda = 0.25 m, conectividad 8)
dist = np.full(walk.shape, np.inf)
front = seed & walk
dist[front] = 0.0
st = ndi.generate_binary_structure(2, 2)
paso = 0
alcanzado = front.copy()
while front.any():
    paso += 1
    nxt = ndi.binary_dilation(front, st) & walk & ~alcanzado
    if not nxt.any():
        break
    dist[nxt] = paso * CELL * 1.11     # 1.11 ~ correccion media diagonal (chebyshev->euclid)
    alcanzado |= nxt
    front = nxt
    if paso > 4000:
        break

dw = dist[walk]
sin_conexion = float(np.isinf(dw).mean())
dw_fin = dw[np.isfinite(dw)]
np.save(os.path.join(OUT, 'dist_accesos.npy'), np.where(np.isfinite(dist), dist, np.nan))
R = dict(baseline='v006 build 12',
         accesos=len(pts),
         dist_acceso=dict(media=round(float(dw_fin.mean()), 1),
                          p50=round(float(np.median(dw_fin)), 1),
                          p95=round(float(np.percentile(dw_fin, 95)), 1),
                          max=round(float(dw_fin.max()), 1),
                          pct_a_menos_60m=round(100 * float((dw_fin <= 60).mean()), 1),
                          pct_sin_conexion=round(100 * sin_conexion, 2)))

# --------------------------------------------------- 2 · PMR: ascensores y fallo N-1
# anclas de ascensor medidas en la escena por la auditoria (log A4): reconstruye por bloque
sys.path.insert(0, os.path.join(F9, '_reaudit9'))
import audit_core as AC  # noqa: E402
objs, m, B = AC.load_scene()
lifts = sorted({tuple(np.round(o['anchor'][:2], 1)) for o in objs
                if o.get('block') == 'LIFT_TOWER' and o.get('anchor')})
stairs = a4.get('stairs')
# proyeccion de cada ascensor sobre la polilinea de la cinta (s a lo largo)
prof = a4['prof'] if isinstance(a4.get('prof'), list) else []
sx = np.array([q['x'] for q in prof]); sy = np.array([q['y'] for q in prof])
ss = np.array([q['s'] for q in prof])


def s_de(px, py):
    d2 = (sx - px) ** 2 + (sy - py) ** 2
    return float(ss[int(np.argmin(d2))])


s_lifts = sorted(s_de(px, py) for (px, py) in lifts)
Ltot = a4['long']
# rodeo peor caso con N y con N-1 (anillo cerrado): max distancia a lo largo hasta ascensor
def peor_rodeo(s_list):
    if not s_list:
        return None
    s_arr = np.array(sorted(s_list))
    smues = np.linspace(0, Ltot, 400)
    d = np.min(np.minimum(np.abs(smues[:, None] - s_arr[None, :]),
                          Ltot - np.abs(smues[:, None] - s_arr[None, :])), axis=1)
    return float(d.max())


rodeos = dict(todos=round(peor_rodeo(s_lifts), 0))
for k in range(len(s_lifts)):
    resto = [s for i, s in enumerate(s_lifts) if i != k]
    rodeos['sin_asc_%d' % (k + 1)] = round(peor_rodeo(resto), 0)
R['pmr'] = dict(n_ascensores=len(lifts), ascensores_xy=[list(p) for p in lifts],
                n_escaleras=a4['n_accesos'], cinta_long_m=Ltot,
                rodeo_max_con_todos_m=rodeos['todos'],
                rodeo_max_N1_m=max(v for k, v in rodeos.items() if k != 'todos'),
                rodeos=rodeos,
                nota='El nivel +6 es APTO PMR solo via ascensor: con los %d operativos el '
                     'rodeo maximo sobre la cinta es %.0f m; con el peor N-1 sube a %.0f m. '
                     'Las 6 escaleras no son itinerario accesible.'
                     % (len(lifts), rodeos['todos'],
                        max(v for k, v in rodeos.items() if k != 'todos')))

# --------------------------------------------------- 3 · LOS por eje (escenarios C)
# Capacidad de servicio peatonal: flujo (p/min/m) segun HCM/Fruin. LOS C ~ 33-49 p/min/m.
ejes = a5['rows']
# hipotesis de demanda (C): reparto del flujo diario declarado en escenarios
ESCEN = [('COTIDIANO', 40000, 0.10), ('HORA PUNTA', 40000, 0.18), ('GRAN AFLUENCIA', 120000, 0.15)]
FR = [(23, 'A-B (libre)'), (33, 'C (confortable)'), (49, 'D (denso)'), (66, 'E (critico)')]
los_rows = []
for nombre, diario, pct_hora in ESCEN:
    flujo_h = diario * pct_hora
    # reparto por eje ~ proporcional a su anchura p05 (los anchos atraen flujo)
    wsum = sum(e['w_p05'] for e in ejes)
    for e in ejes:
        f_eje = flujo_h * e['w_p05'] / wsum
        # el punto critico es el ancho transversal minimo del eje
        q = f_eje / 60.0 / max(e['w_transv_min'], 0.5)
        los = next(l for lim, l in FR if q <= lim) if q <= 66 else 'F (saturado)'
        los_rows.append(dict(escenario=nombre, eje=e['id'], flujo_p_h=round(f_eje, 0),
                             ancho_min_m=round(e['w_transv_min'], 2),
                             q_p_min_m=round(q, 1), LOS=los))
R['los'] = dict(escenarios=los_rows,
                hipotesis='HIPOTESIS (C): demanda diaria 40.000 peatones/dia ordinario y '
                          '120.000 en gran afluencia (orden de magnitud de un eje centrico '
                          'de Madrid; pendiente de dato oficial en 07_ECONOMIA); hora punta '
                          '18 %; reparto proporcional al ancho p05 de cada eje; el LOS se '
                          'evalua en el ancho transversal MINIMO (punto pesimo).')

# --------------------------------------------------- 4 · sintesis de red (pass-through)
R['red'] = dict(frag=a1['frag'], bottleneck_peor=min(a1['bottleneck'].values()),
                pockets=a1['pockets'], narrow_n=len(a1['narrow']),
                choke_n=len(a1['choke']))
R['ejes'] = ejes
R['cinta'] = {k: a4[k] for k in ('long', 'z', 'ancho_util', 'n_soportes', 'galibo_bajo',
                                 'n_accesos', 'radio_min')}

with open(os.path.join(OUT, 'mob_stats.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)

flog.event(fase='FINAL', tipo_evento='motor_movilidad',
           objetivo='MOB: distancias de evacuacion, PMR N-1, LOS por escenarios sobre v006',
           resultado='dist acceso p95 %.0f m (max %.0f); PMR: %d ascensores, rodeo N-1 %.0f m; '
                     'peor cuello entre accesos %.2f m; LOS peor escenario: %s'
                     % (R['dist_acceso']['p95'], R['dist_acceso']['max'],
                        R['pmr']['n_ascensores'], R['pmr']['rodeo_max_N1_m'],
                        R['red']['bottleneck_peor'],
                        max((r['q_p_min_m'], r['LOS']) for r in los_rows)[1]))
print(json.dumps({k: R[k] for k in ('dist_acceso', 'pmr')}, ensure_ascii=False, indent=1)[:900])
print('LOS peor:', max(los_rows, key=lambda r: r['q_p_min_m']))
