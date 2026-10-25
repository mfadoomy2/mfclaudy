# -*- coding: utf-8 -*-
"""FASE FINAL - MOTOR PATRIMONIO (PAT-01) sobre v006.

Visibilidad de los tres hitos (reloj, torre, fachada de Correos) desde el suelo:
por superficie (la metrica clasica) y PONDERADA POR USO (vis x IPE) — la metrica
que importa: que ve la gente desde donde de verdad se queda.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
RC = os.path.normpath(os.path.join(BASE, '..'))
MONT = os.path.normpath(os.path.join(RC, '..'))
F9 = os.path.join(RC, 'FASE_03B9_HYPERDETAIL_V006')
OUT = os.path.join(BASE, '08_PATRIMONIO_VISUALES_Y_PAISAJE_URBANO', 'B_DATOS')
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402

with open(os.path.join(F9, '_reaudit9', '_data', 'a7_views.json'), encoding='utf-8') as f:
    a7 = json.load(f)
ipe = np.load(os.path.join(BASE, '06_USO_SOCIAL_Y_EXPERIENCIA', 'B_DATOS', 'ipe.npy'))
X0, Y0, CS = -112, -45, 0.5
ny, nx = ipe.shape

pts = np.array(a7['pts'])
R = dict(baseline='v006 build 12', n_puntos=a7['n'], pct_superficie=a7['pct'])

pond = {}
for hito, visl in a7['vis'].items():
    vis = np.array(visl, bool)
    w = []
    for (px, py) in pts:
        j = int((px - X0) / CS); i = int((py - Y0) / CS)
        v = ipe[i, j] if (0 <= i < ny and 0 <= j < nx) else np.nan
        w.append(v if np.isfinite(v) else 0.0)
    w = np.array(w)
    pond[hito] = dict(
        pct_superficie=round(a7['pct'][hito], 1),
        pct_ponderado_uso=round(100 * float((vis * w).sum() / max(w.sum(), 1e-9)), 1),
        pct_en_estancia_alta=round(100 * float(vis[w >= 0.6].mean()) if (w >= 0.6).any() else 0.0, 1))
R['ponderada'] = pond
R['nota'] = ('vis x IPE: la visibilidad que experimentan los USUARIOS (ponderada por '
             'potencial de estancia), frente a la clasica por superficie. El estado A '
             '(plaza actual) tiene visibilidad cuasi-total desde el vacio central: la '
             'reduccion es real y se publica; la pregunta correcta es cuanta visibilidad '
             'queda desde donde la gente se detiene.')

with open(os.path.join(OUT, 'pat_stats.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)

flog.event(fase='FINAL', tipo_evento='motor_patrimonio',
           objetivo='PAT: visibilidad de hitos por superficie y ponderada por uso (vis x IPE)',
           resultado='; '.join('%s: %s%% superficie -> %s%% ponderada uso'
                               % (h, d['pct_superficie'], d['pct_ponderado_uso'])
                               for h, d in pond.items()))
print(json.dumps(pond, ensure_ascii=False, indent=1))
