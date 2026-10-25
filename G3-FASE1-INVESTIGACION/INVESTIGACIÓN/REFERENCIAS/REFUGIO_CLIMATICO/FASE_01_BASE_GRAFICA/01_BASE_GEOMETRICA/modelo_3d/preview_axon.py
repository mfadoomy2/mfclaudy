# -*- coding: utf-8 -*-
"""Render axonometrico de validacion del OBJ (painter, PIL)."""
import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OBJ = os.path.join(HERE, 'refugio_fase01.obj')
MTL = os.path.join(HERE, 'refugio_fase01.mtl')

colors = {}
cur = None
for line in open(MTL):
    if line.startswith('newmtl'):
        cur = line.split()[1]
    elif line.startswith('Kd') and cur:
        r, g, b = [float(v) for v in line.split()[1:4]]
        colors[cur] = (int(r * 255), int(g * 255), int(b * 255))

Vs, faces = [], []
grp = mtl = None
for line in open(OBJ):
    if line.startswith('v '):
        _, x, y, z = line.split()
        Vs.append((float(x), float(y), float(z)))
    elif line.startswith('g '):
        grp = line.split()[1]
    elif line.startswith('usemtl'):
        mtl = line.split()[1]
    elif line.startswith('f '):
        idx = [int(t) - 1 for t in line.split()[1:]]
        faces.append((idx, mtl, grp))

R = math.radians(-25)
CE, SE = math.cos(R), math.sin(R)
ELC, ELS = math.cos(math.radians(30)), math.sin(math.radians(30))


def proj(p):
    x, y, z = p
    xr = x * CE - y * SE
    yr = x * SE + y * CE
    u = xr
    v = yr * ELS + z * ELC
    depth = yr * ELC - z * ELS
    return u, v, depth


P = [proj(p) for p in Vs]
us = [p[0] for p in P]
vs = [p[1] for p in P]
u0, u1, v0, v1 = min(us), max(us), min(vs), max(vs)
W = 2000
sc = W / (u1 - u0)
H = int((v1 - v0) * sc) + 40

img = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(img, 'RGBA')

# ordenar: lejos primero
order = sorted(faces, key=lambda f: -sum(P[i][2] for i in f[0]) / len(f[0]))
skip_ctx = 0
for idx, mtlname, grp in order:
    col = colors.get(mtlname, (120, 120, 120))
    pts = [((P[i][0] - u0) * sc, H - 20 - (P[i][1] - v0) * sc) for i in idx]
    alpha = 235
    if grp in ('01_CONTEXTO_EDIFICIOS',):
        alpha = 255
    if grp in ('05_DISCOS', '06_BALSAS'):
        alpha = 170
    d.polygon(pts, fill=col + (alpha,), outline=(90, 90, 90, 120))

img.save(os.path.join(HERE, 'axon_preview.png'))
print('-> axon_preview.png', img.size, 'caras:', len(faces))
