# -*- coding: utf-8 -*-
"""Probe 12: que triangulo CONTEXT (z<2.2) cubre en planta los puntos rojos de arenal."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '_reaudit9'))
import audit_core as AC
import numpy as np

objs, m, B = AC.load_scene()


def cubre(px, py, V, F):
    x, y = V[:, 0], V[:, 1]
    a, b, c = F[:, 0], F[:, 1], F[:, 2]
    x1, y1, x2, y2, x3, y3 = x[a], y[a], x[b], y[b], x[c], y[c]
    d1 = (px - x2) * (y1 - y2) - (x1 - x2) * (py - y2)
    d2 = (px - x3) * (y2 - y3) - (x2 - x3) * (py - y3)
    d3 = (px - x1) * (y3 - y1) - (x3 - x1) * (py - y1)
    neg = (d1 < 0) | (d2 < 0) | (d3 < 0)
    pos = (d1 > 0) | (d2 > 0) | (d3 > 0)
    return ~(neg & pos)


for tag, fx, fy in (('s16', -81.93, 17.55), ('s44', -59.56, 32.61)):
    print('=== FOCO', tag, (fx, fy))
    for o in objs:
        if o['kind'] != 'mesh' or o['layer'] != '00_CONTEXT':
            continue
        V, F = o['V'], o['F']
        if V[:, 2].min() > 2.2 or len(F) == 0:
            continue
        hit = cubre(fx, fy, V, F)
        if hit.any():
            zmins = V[F[hit]][:, :, 2].min()
            print('  %-24s tris_cubren=%d zmin_tri=%.2f' % (o['name'], int(hit.sum()), zmins))
