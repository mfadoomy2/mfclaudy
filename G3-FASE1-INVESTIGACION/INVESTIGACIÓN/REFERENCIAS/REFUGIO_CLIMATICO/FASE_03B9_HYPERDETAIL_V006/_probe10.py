# -*- coding: utf-8 -*-
"""Probe 10: identificar mallas concretas que ocupan los 3 focos RED de build 9."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '_reaudit9'))
import audit_core as AC

objs, m, B = AC.load_scene()

FOCOS = [('arenal_s16', -81.93, 17.55, 1.0), ('arenal_s44', -59.56, 32.61, 1.0),
         ('estacion', 51.81, -2.75, 1.0), ('pod_huerto', -57.46, 11.2, 1.0)]

for tag, fx, fy, r in FOCOS:
    print('=== FOCO', tag, (fx, fy))
    for o in objs:
        if o['kind'] != 'mesh':
            continue
        V = o['V']
        x0, x1 = V[:, 0].min(), V[:, 0].max()
        y0, y1 = V[:, 1].min(), V[:, 1].max()
        z0, z1 = V[:, 2].min(), V[:, 2].max()
        if x0 - r <= fx <= x1 + r and y0 - r <= fy <= y1 + r and z0 <= 3.0 and z1 >= 0.05:
            print(f'  {o["layer"]:26s} {o["name"]:28s} x[{x0:7.2f},{x1:7.2f}] y[{y0:7.2f},{y1:7.2f}] z[{z0:5.2f},{z1:5.2f}]')
