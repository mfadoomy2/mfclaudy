# -*- coding: utf-8 -*-
"""GEOMETRIA MAESTRA v005 — FASE 03B.8 (PURGA + MICRODETAIL).
Rama sobre v004 (INTACTA). Cambios de DATOS:
  · §2 AIRE CONTRA FACHADA: margenes urbanos suben para garantizar ~2.0 m LIBRES continuos
    (no "justo no colisiona"): cinta 2.65→3.80 (borde de tablero ~1.45 → libre ~2.0+),
    loop 3.25→4.30, aereo 0.5→1.2, suelo 0.8→1.0.
  · TANQUES: paso de la fila = diametro real del toro + luz (los toros de v004 quedaban
    ENTRELAZADOS: paso 2.6 < 2·(r+0.85)).
  · TREN: el paso del tren usa la LONGITUD real del bloque POD_TRAIN (5.3) — en v004 las
    capsulas se interpenetraban (acordeon).
Diff en _v005_diff.json.
"""
import datetime
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.normpath(os.path.join(HERE, '..', 'FASE_03B7_DETAILING_V004'))
m = json.load(open(os.path.join(V4, 'geometria_maestra_v004.json'), encoding='utf-8'))

DIFF = {'base': 'geometria_maestra_v004.json', 'fecha': '2026-08-11', 'cambios': []}


def log(cr, que, detalle=None):
    print('[%s] %s' % (cr, que))
    DIFF['cambios'].append({'causa': cr, 'que': que, 'detalle': detalle})


# ---------- §2 · MARGENES DE FACHADA (aire real, no tangencia) ----------
U = m['urbano_v004']
U_old = dict(U['margen_edificio'])
U['margen_edificio'] = {'suelo': 1.0, 'aereo': 1.2, 'loop': 4.30, 'cinta': 3.80}
U['nota_v005'] = ('03B.8 §2: el criterio deja de ser "no colisiona" y pasa a ser AIRE: '
                  'borde de tablero/aro a >=2.0 m libres de fachada de forma continua. '
                  'La fachada se lee, se mantiene y se recorre.')
log('S08/D-16', 'margenes edificio: %s -> %s' % (U_old, U['margen_edificio']))

# ---------- TANQUES: fila sin eslabones ----------
for t in m.get('estructura_ligera', {}).get('tanks', []):
    if 'paso' not in t:
        t['paso'] = round(2 * (t['r'] + 0.85) + 0.60, 2)   # diametro del toro (r+seccion .85) + luz
        log('S04/D-43', 'tanque %s: paso de fila %.2f (antes 2.6 implicito)' % (t.get('id', '?'), t['paso']))

# ---------- TREN: paso >= longitud real ----------
tp = m['programa'].get('tren_portico')
if tp:
    tp['L_capsula'] = 5.3
    log('S07/D-12', 'tren_portico: L_capsula 5.3 en datos (el build usaba w=3.4 como paso)')

m['version'] = 'v005 (2026-08-11, FASE 03B.8 — purga total + microdetalle extremo)'
json.dump(m, open(os.path.join(HERE, 'geometria_maestra_v005.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
json.dump(DIFF, open(os.path.join(HERE, '_v005_diff.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('OK geometria_maestra_v005.json (%d cambios)' % len(DIFF['cambios']))
