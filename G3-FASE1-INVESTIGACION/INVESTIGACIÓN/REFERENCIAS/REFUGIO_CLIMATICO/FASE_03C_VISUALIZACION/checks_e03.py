# -*- coding: utf-8 -*-
"""E03 §8 — controles automaticos sobre hero_E03: tamano, luminancia vs E02, ROI de sombra H1,
ancho analitico de chorros H3, contraste torre/cielo H4-tarde. Emite _checks_e03.json."""
import json
import math
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'hero_E03')
E02 = os.path.join(HERE, 'direccion_arte')
CFG = json.load(open(os.path.join(HERE, 'atmos_config.json'), encoding='utf-8'))
PAR_E02 = {'H1': 'DA_V05_banda_correos', 'H2': 'DA_V06_bajo_C1', 'H3': 'DA_V13_splash',
           'H4': 'DA_V07_reloj', 'H5': 'DA_V19_sobre_cinta', 'H6': 'DA_V10_cupula'}
R = {}


def lum(p):
    a = np.asarray(Image.open(p).convert('L'), float)
    return a


for c in CFG['camaras_hero']:
    for luz in ('mediodia', 'tarde'):
        n = '%s_%s' % (c['id'], luz)
        p = os.path.join(OUT, n + '.png')
        row = {'existe': os.path.exists(p)}
        if row['existe']:
            row['kb'] = os.path.getsize(p) // 1024
            row['ok_30kb'] = row['kb'] > 30
            L = lum(p)
            row['lum_media'] = round(float(L.mean()), 1)
            # luminancia vs E02 (solo mediodia, pares H1..H6)
            par = PAR_E02.get(c['id'])
            if luz == 'mediodia' and par:
                pe = os.path.join(E02, par + '.png')
                if os.path.exists(pe):
                    L2 = lum(pe)
                    dl = 100 * (L.mean() - L2.mean()) / L2.mean()
                    row['dLum_vs_E02_pct'] = round(float(dl), 1)
                    row['ok_niebla_8pct'] = bool(dl <= 8.0)
            if c['id'] == 'H1' and luz == 'mediodia':
                p35 = np.percentile(L, 35)
                roi = L[int(L.shape[0]*0.55):int(L.shape[0]*0.92), int(L.shape[1]*0.22):int(L.shape[1]*0.78)]
                fr = float((roi < p35).mean())
                row['H1_roi_sombra_pct'] = round(100 * fr, 1)
                row['ok_H1_sombra_30'] = bool(fr >= 0.30)
            if c['id'] == 'H4' and luz == 'tarde':
                h, w = L.shape
                torre = L[int(h*0.28):int(h*0.42), int(w*0.46):int(w*0.54)].mean()
                cielo = L[int(h*0.05):int(h*0.15), int(w*0.05):int(w*0.20)].mean()
                ct = abs(torre - cielo) / max(cielo, 1) * 100
                row['H4_contraste_pct'] = round(float(ct), 1)
                row['ok_H4_contraste_15'] = bool(ct >= 15.0)
        R[n] = row

# H3: ancho de chorro ANALITICO (r=0.045 -> 0.09 m de diametro) a la distancia media camara-splash
c3 = next(c for c in CFG['camaras_hero'] if c['id'] == 'H3')
d = math.dist(c3['cam'][:2], [17, -8])
pxm = 2560 / (2 * d * math.tan(math.radians(c3['fov'] / 2)))
R['H3_chorro_px'] = round(0.09 * pxm, 1)
R['ok_H3_chorro_3px'] = bool(0.09 * pxm * 1920 / 2560 >= 3.0)

json.dump(R, open(os.path.join(HERE, '_checks_e03.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fails = [k for k, v in R.items() if isinstance(v, dict) and any(kk.startswith('ok') and not vv for kk, vv in v.items())]
print(json.dumps(R, ensure_ascii=False, indent=1))
print('FALLOS:', fails or 'ninguno')
