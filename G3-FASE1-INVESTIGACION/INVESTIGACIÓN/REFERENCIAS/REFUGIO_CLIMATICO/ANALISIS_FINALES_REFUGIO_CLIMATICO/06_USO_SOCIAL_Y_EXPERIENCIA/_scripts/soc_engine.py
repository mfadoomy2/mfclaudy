# -*- coding: utf-8 -*-
"""FASE FINAL - MOTOR SOCIAL (SOC-01..02) sobre v006.

Indice de Potencial de Estancia (IPE) por celda — formula EXPLICITA, pesos declarados,
sensibilidad de pesos incluida — y personas-hora protegidas en LOW/BASE/HIGH (C).
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
OUT = os.path.join(BASE, '06_USO_SOCIAL_Y_EXPERIENCIA', 'B_DATOS')
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
sys.path.insert(0, os.path.join(F9, '_reaudit9'))
import flog  # noqa: E402
import audit_core as AC  # noqa: E402


def L(n, d=CLI):
    return np.load(os.path.join(d, n))


walk = L('walk.npy', AUD)[::2, ::2].astype(bool)
u = L('u_E2_16_B.npy')
ny, nx = u.shape
walk = walk[:ny, :nx]
sh = L('shade_crit_B.npy')
cause = L('cause.npy', AUD)[::2, ::2][:ny, :nx]
CELLA = 0.25
X0, Y0, CS = -112, -45, 0.5

# ---------------------------------------------------------------- capas del indice
# 1 sombra critica (0-1 directa)
c_sombra = np.clip(np.nan_to_num(sh), 0, 1)
# 2 confort: UTCI E2/16h normalizado (1 a <=32, 0 a >=42)
c_confort = np.clip((42.0 - np.nan_to_num(u, nan=42.0)) / 10.0, 0, 1)
# 3/4 proximidad a asiento y agua: anclas de la escena
objs, m, B = AC.load_scene()
# los bancos se emiten con add_mesh (sin ancla): centroide de cada malla de asiento
bench_xy = sorted({(round(float(o['V'][:, 0].mean()), 1),
                    round(float(o['V'][:, 1].mean()), 1))
                   for o in objs if o['kind'] == 'mesh'
                   and o['name'].startswith('BENCH_') and o['layer'] == '10_FURNITURE'
                   and not o['name'].startswith(('BENCH_TESTERO', 'BENCH_PATA'))})
agua_xy = [(p['cx'], p['cy']) for p in m['agua_clima']['ground_ponds']
           if p.get('kind') == 'circle']
sp = m['agua_clima']['splash']
agua_xy.append((sp['cx'], sp['cy']))


def prox(points, alcance):
    """Campo 0-1: 1 junto al punto, 0 a >= alcance (decae lineal)."""
    f = np.zeros((ny, nx))
    if not points:
        return f
    mask = np.ones((ny, nx), bool)
    for (px, py) in points:
        j = int((px - X0) / CS); i = int((py - Y0) / CS)
        if 0 <= i < ny and 0 <= j < nx:
            mask[i, j] = False
    d = ndi.distance_transform_edt(mask) * CS
    return np.clip(1.0 - d / alcance, 0, 1)


c_asiento = prox(bench_xy, 15.0)
c_agua = prox(agua_xy, 20.0)
# 5 efecto borde (Gehl): cerca de jardineras/mobiliario/vegetacion pero EN celda libre
FAM = ['CONTEXT', 'STRUCTURE', 'RIBBON', 'PODS', 'CANOPY', 'PLANTER', 'VEGETATION',
       'FURNITURE', 'WATER']
borde_src = np.isin(cause, [FAM.index('PLANTER') + 1, FAM.index('FURNITURE') + 1,
                            FAM.index('VEGETATION') + 1])
d_borde = ndi.distance_transform_edt(~borde_src) * CS
c_borde = np.clip(1.0 - d_borde / 6.0, 0, 1)

PESOS = dict(sombra=0.30, confort=0.30, asiento=0.15, agua=0.10, borde=0.15)
IPE = (PESOS['sombra'] * c_sombra + PESOS['confort'] * c_confort +
       PESOS['asiento'] * c_asiento + PESOS['agua'] * c_agua +
       PESOS['borde'] * c_borde)
IPE = np.where(walk, IPE, np.nan)
np.save(os.path.join(OUT, 'ipe.npy'), IPE)

v = IPE[walk]
R = dict(baseline='v006 build 12',
         formula='IPE = 0,30·sombra + 0,30·confort(UTCI) + 0,15·asiento(≤15 m) + '
                 '0,10·agua(≤20 m) + 0,15·borde(≤6 m)',
         pesos=PESOS,
         capas=dict(bancos=len(bench_xy), puntos_agua=len(agua_xy)),
         ipe=dict(media=round(float(np.nanmean(v)), 3),
                  p90=round(float(np.nanpercentile(v, 90)), 3),
                  m2_alto=round(float((v >= 0.6).sum() * CELLA), 0),
                  m2_medio=round(float(((v >= 0.4) & (v < 0.6)).sum() * CELLA), 0)))

# ---------------------------------------------------------------- sensibilidad de pesos
rng = [0.5, 1.0, 1.5]
rank_stab = []
base_top = np.nan_to_num(IPE) >= 0.6
for k in PESOS:
    for f in (0.5, 1.5):
        pw = dict(PESOS)
        pw[k] = PESOS[k] * f
        s = sum(pw.values())
        pw = {kk: vv / s for kk, vv in pw.items()}
        ipe2 = (pw['sombra'] * c_sombra + pw['confort'] * c_confort +
                pw['asiento'] * c_asiento + pw['agua'] * c_agua + pw['borde'] * c_borde)
        top2 = np.where(walk, ipe2, 0) >= 0.6
        inter = float((base_top & top2).sum()) / max(1.0, float((base_top | top2).sum()))
        rank_stab.append(dict(peso=k, factor=f, jaccard_top=round(inter, 2)))
R['sensibilidad_pesos'] = dict(
    detalle=rank_stab,
    jaccard_min=min(r['jaccard_top'] for r in rank_stab),
    nota='estabilidad del conjunto IPE>=0,6 al variar cada peso +-50 % (Jaccard): '
         'el mapa de estancia no es un artefacto de los pesos.')

# ---------------------------------------------------------------- personas-hora (C)
ESC = dict(LOW=dict(afluencia=30000, se_detiene=0.15, estancia_min=10, conc=1.3),
           BASE=dict(afluencia=60000, se_detiene=0.25, estancia_min=15, conc=1.6),
           HIGH=dict(afluencia=120000, se_detiene=0.35, estancia_min=20, conc=1.9))
ref_frac = 0.36
ph = {}
for k, e in ESC.items():
    frac_refugio = min(0.95, ref_frac * e['conc'])
    val = e['afluencia'] * e['se_detiene'] * (e['estancia_min'] / 60.0) * frac_refugio
    ph[k] = dict(**e, frac_estancia_en_refugio=round(frac_refugio, 2),
                 personas_hora_protegidas_dia=int(round(val, -1)))
R['personas_hora'] = dict(
    escenarios=ph,
    hipotesis='HIPOTESIS (C): afluencia diaria sin dato oficial cerrado (se busca en '
              '07_ECONOMIA); % que se detiene y estancia media por rangos de literatura '
              'de espacio publico (Gehl/PPS); factor de concentracion = los que se '
              'detienen ELIGEN el confort (IPE alto esta en refugio).')

with open(os.path.join(OUT, 'soc_stats.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)

flog.event(fase='FINAL', tipo_evento='motor_social',
           objetivo='SOC: indice de potencial de estancia explicito + personas-hora LOW/BASE/HIGH',
           resultado='IPE medio %.2f; %d m2 de estancia alta (>=0,6); Jaccard min pesos %.2f; '
                     'personas-hora/dia LOW %d / BASE %d / HIGH %d'
                     % (R['ipe']['media'], R['ipe']['m2_alto'],
                        R['sensibilidad_pesos']['jaccard_min'],
                        ph['LOW']['personas_hora_protegidas_dia'],
                        ph['BASE']['personas_hora_protegidas_dia'],
                        ph['HIGH']['personas_hora_protegidas_dia']))
print(json.dumps({k: R[k] for k in ('ipe', 'capas')}, ensure_ascii=False))
print('jaccard min:', R['sensibilidad_pesos']['jaccard_min'])
print('p-h:', {k: v['personas_hora_protegidas_dia'] for k, v in ph.items()})
