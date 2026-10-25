# -*- coding: utf-8 -*-
"""Textura procedural del granito de Sol + mapa de rugosidad con HUMEDAD REAL:
zonas mojadas pintadas en radio 3-5 m de cada boquilla (42), splash y estanques (v002)."""
import json
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.normpath(os.path.join(HERE, '..', 'FASE_03B_MODELO_MAESTRO', 'geometria_maestra_v002.json'))
m = json.load(open(V2, encoding='utf-8'))
rng = random.Random(9)

# extension del plano de suelo del modelo: centro (0,5), 320x220  ->  x -160..160, y -105..115
X0, X1, Y0, Y1 = -160.0, 160.0, -105.0, 115.0
W = 3200
Hpx = int(W * (Y1 - Y0) / (X1 - X0))


def px(x, y):
    return ((x - X0) / (X1 - X0) * W, (Y1 - y) / (Y1 - Y0) * Hpx)


# ---- color base: granito con despiece en bandas de 1.8 m a 7 grados ----
col = Image.new('RGB', (W, Hpx), (207, 201, 190))
d = ImageDraw.Draw(col)
for _ in range(90000):   # moteado granitico
    x = rng.uniform(0, W); y = rng.uniform(0, Hpx)
    g = rng.choice([(188, 182, 172), (218, 213, 204), (176, 170, 160), (226, 222, 214)])
    r = rng.uniform(0.5, 2.2)
    d.ellipse([x - r, y - r, x + r, y + r], fill=g)
# despiece E02: juntas mas legibles (sombra + brillo) + cortes transversales cada 5.4 m
ang = math.radians(7)
step = 1.8 / (X1 - X0) * W
k0 = int(-Hpx * math.tan(ang) / step) - 120
for k in range(k0, int(W / step) + 120):
    x_at0 = k * step
    d.line([(x_at0, 0), (x_at0 + Hpx * math.tan(ang), Hpx)], fill=(168, 162, 152), width=3)
    d.line([(x_at0 + 3, 0), (x_at0 + 3 + Hpx * math.tan(ang), Hpx)], fill=(224, 220, 212), width=1)
step2 = 5.4 / (X1 - X0) * W
for k in range(0, int(Hpx / step2) + 40):
    y0 = k * step2 + (k % 3) * step2 * 0.33
    d.line([(0, y0), (W, y0 - W * math.tan(ang))], fill=(174, 168, 158), width=2)
col = col.filter(ImageFilter.GaussianBlur(0.5))

# ---- humedad: mapa de mojado (blanco=mojado) ----
wet = Image.new('L', (W, Hpx), 0)
dw = ImageDraw.Draw(wet)


def wet_blob(x, y, r_m, core=255):
    cx, cy = px(x, y)
    rp = r_m / (X1 - X0) * W
    dw.ellipse([cx - rp, cy - rp, cx + rp, cy + rp], fill=core)


for (nx, ny) in m['agua_clima']['nebul']:
    wet_blob(nx, ny, rng.uniform(3.2, 5.0))
sp = m['agua_clima']['splash']
for f, v in [(1.9, 120), (1.45, 190), (1.0, 255)]:
    cx, cy = px(sp['cx'], sp['cy'])
    rx = sp['rx'] * f / (X1 - X0) * W
    ry = sp['ry'] * f / (X1 - X0) * W
    dw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=v)
for p in m['agua_clima']['ground_ponds']:
    if p['kind'] == 'circle':
        wet_blob(p['cx'], p['cy'], p['r'] + 1.8, 200)
for w0 in m['agua_clima']['mains']:
    for q in w0[::2]:
        wet_blob(q[0], q[1], 1.1, 120)
wet = wet.filter(ImageFilter.GaussianBlur(int(2.2 / (X1 - X0) * W)))

# oscurecer color donde moja (-28% valor) + roughness map (seco 0.82 -> mojado 0.20)
colp = col.load(); wetp = wet.load()
rough = Image.new('L', (W, Hpx), int(0.85 * 255))
rp_ = rough.load()
for yy in range(Hpx):
    for xx in range(W):
        wv = wetp[xx, yy] / 255.0
        if wv > 0.02:
            r, g, b = colp[xx, yy]
            f = 1.0 - 0.34 * wv
            colp[xx, yy] = (int(r * f), int(g * f * 1.02), int(b * f * 1.03))
            rp_[xx, yy] = int((0.85 - 0.69 * wv) * 255)

os.makedirs(os.path.join(HERE, '_viewer', 'tex'), exist_ok=True)
col.save(os.path.join(HERE, '_viewer', 'tex', 'granito.jpg'), quality=88)
rough.save(os.path.join(HERE, '_viewer', 'tex', 'granito_rough.jpg'), quality=88)
print('texturas ok', W, Hpx)
