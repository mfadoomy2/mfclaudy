# -*- coding: utf-8 -*-
"""03D — QA TECNICO (heredado de E03; el juicio visual manda, esto solo detecta roturas).
Sobre hero_03D: tamano, rango tonal sano, ROI de sombra H1, contraste torre/cielo H4-tarde."""
import json
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'hero_03D')
R = {}
for f in sorted(os.listdir(OUT)):
    if not f.endswith('.png'):
        continue
    p = os.path.join(OUT, f)
    L = np.asarray(Image.open(p).convert('L'), float)
    row = {'kb': os.path.getsize(p) // 1024, 'lum': round(float(L.mean()), 1),
           'p05': round(float(np.percentile(L, 5)), 1), 'p95': round(float(np.percentile(L, 95)), 1)}
    row['ok_30kb'] = row['kb'] > 30
    row['ok_rango'] = bool(row['p95'] - row['p05'] > 40 and 25 < row['lum'] < 215)
    if f == 'H1_mediodia.png':
        p35 = np.percentile(L, 35)
        roi = L[int(L.shape[0]*0.55):int(L.shape[0]*0.92), int(L.shape[1]*0.22):int(L.shape[1]*0.78)]
        row['H1_roi_sombra_pct'] = round(100 * float((roi < p35).mean()), 1)
        row['ok_H1_sombra_30'] = row['H1_roi_sombra_pct'] >= 30
    if f == 'H4_tarde.png':
        h, w = L.shape
        torre = L[int(h*0.28):int(h*0.42), int(w*0.46):int(w*0.54)].mean()
        cielo = L[int(h*0.05):int(h*0.15), int(w*0.05):int(w*0.20)].mean()
        row['H4_contraste_pct'] = round(float(abs(torre - cielo) / max(cielo, 1) * 100), 1)
        row['ok_H4_contraste_15'] = bool(row['H4_contraste_pct'] >= 15)
    R[f[:-4]] = row
json.dump(R, open(os.path.join(HERE, '_checks_03d.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fails = [k for k, v in R.items() if any(kk.startswith('ok') and not vv for kk, vv in v.items())]
print(json.dumps(R, ensure_ascii=False, indent=1))
print('FALLOS:', fails or 'ninguno')
