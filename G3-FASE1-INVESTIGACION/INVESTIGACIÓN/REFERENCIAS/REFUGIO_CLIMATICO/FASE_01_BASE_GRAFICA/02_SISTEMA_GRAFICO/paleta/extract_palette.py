# -*- coding: utf-8 -*-
"""Extraccion de paleta real de las referencias del Refugio (k-means numpy, determinista)."""
import json
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = r'C:\Users\iraxx_c0wouln\OneDrive\Documentos\iraxxxdios_ARQUITECTURA\xxxmiguelxxx\Monteserin\MONTESERIN IA\MONTESERIN IA\MUTACIONES (DIBUJO + IA)\DIBUJO3 (REFUGIO CLIMATICO)'

SOURCES = [
    ('00_DIBUJO 03.jpg', 'dibujo matriz'),
    ('HR01.png', 'cenital arquitectonica'),
    ('HR02.png', 'maqueta acrilico'),
    ('HR11.png', 'maqueta rosa/verde'),
    (os.path.join('IN PROGRESS REFUGIO', '0F53E6F0-C499-4057-8C95-A0928F3680D9.png'), 'cenital Sol real'),
    (os.path.join('IN PROGRESS REFUGIO', '12CA810C-437B-41C2-B54C-62B449F8FD7B.png'), 'peatonal salon urbano'),
    (os.path.join('IN PROGRESS REFUGIO', 'A2BD2AAA-FA08-48B3-ACD8-BEFFD226B1B1.png'), 'peatonal dosel'),
]


def kmeans(px, k=10, iters=24, seed=7):
    rs = np.random.RandomState(seed)
    C = px[rs.choice(len(px), k, replace=False)].astype(np.float64)
    for _ in range(iters):
        d2 = ((px[:, None, :] - C[None, :, :]) ** 2).sum(-1)
        lab = d2.argmin(1)
        for j in range(k):
            sel = px[lab == j]
            if len(sel):
                C[j] = sel.mean(0)
    counts = np.bincount(lab, minlength=k)
    return C, counts


all_px = []
per_image = {}
for rel, tag in SOURCES:
    im = Image.open(os.path.join(BASE, rel)).convert('RGB').resize((240, 120))
    a = np.asarray(im).reshape(-1, 3).astype(np.float64)
    all_px.append(a)
    C, n = kmeans(a, k=8, iters=16)
    order = np.argsort(-n)
    per_image[tag] = [('#%02X%02X%02X' % tuple(int(v) for v in C[j]), int(n[j])) for j in order]

px = np.vstack(all_px)
# quitar blancos/grises de fondo para encontrar los acentos
mask = ~((px.std(1) < 12) & (px.mean(1) > 190))
C, n = kmeans(px[mask], k=12, iters=24)
order = np.argsort(-n)
global_pal = [('#%02X%02X%02X' % tuple(int(v) for v in C[j]), int(n[j])) for j in order]

out = {'global_sin_fondo': global_pal, 'por_imagen': per_image}
json.dump(out, open(os.path.join(HERE, 'paleta_extraida.json'), 'w'), indent=1)

# swatch sheet
sw = Image.new('RGB', (1200, 90 * (len(per_image) + 1) + 30), 'white')
from PIL import ImageDraw
d = ImageDraw.Draw(sw)
y = 10
d.text((10, y), 'GLOBAL (sin blancos de fondo)', fill='black')
for i, (hx, _) in enumerate(global_pal):
    d.rectangle([10 + i * 95, y + 16, 95 + i * 95, y + 66], fill=hx, outline='gray')
    d.text((12 + i * 95, y + 68), hx, fill='black')
y += 90
for tag, pal in per_image.items():
    d.text((10, y), tag, fill='black')
    for i, (hx, _) in enumerate(pal):
        d.rectangle([10 + i * 95, y + 16, 95 + i * 95, y + 66], fill=hx, outline='gray')
        d.text((12 + i * 95, y + 68), hx, fill='black')
    y += 90
sw.save(os.path.join(HERE, 'paleta_extraida.png'))
print('OK -> paleta_extraida.json / paleta_extraida.png')
for hx, n_ in global_pal:
    print(hx, n_)
