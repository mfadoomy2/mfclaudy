# -*- coding: utf-8 -*-
"""Probe 11: (a) dueno del vertice penetrante (51.81,-2.75); (b) que hay de 00_CONTEXT
en los 2 puntos rojos de arenal; (c) el eje vs poligonos 133/067/068."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '_reaudit9'))
import audit_core as AC
import numpy as np

objs, m, B = AC.load_scene()
M = json.load(open(os.path.join(HERE, 'geometria_maestra_v006.json'), encoding='utf-8'))


def pip(x, y, poly):
    n = len(poly); dentro = False; j = n - 1
    for i in range(n):
        xi, yi = poly[i][0], poly[i][1]
        xj, yj = poly[j][0], poly[j][1]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi):
            dentro = not dentro
        j = i
    return dentro


print('=== (a) vertices en (51.81,-2.75) z<1')
for o in objs:
    if o['kind'] != 'mesh':
        continue
    V = o['V']
    sel = (np.abs(V[:, 0] - 51.81) < 0.15) & (np.abs(V[:, 1] + 2.75) < 0.15) & (V[:, 2] < 1.0)
    if sel.any():
        print(' ', o['layer'], o['name'], 'nvert=', int(sel.sum()), 'ej=', V[sel][0].round(2).tolist())

print('=== (b) 00_CONTEXT z<2.2 tocando los puntos rojos de arenal')
for tag, fx, fy in (('s16', -81.93, 17.55), ('s44', -59.56, 32.61)):
    print(' FOCO', tag, (fx, fy))
    for o in objs:
        if o['kind'] != 'mesh' or o['layer'] != '00_CONTEXT':
            continue
        V = o['V']
        if V[:, 2].min() > 2.2:
            continue
        sel = (np.abs(V[:, 0] - fx) < 0.6) & (np.abs(V[:, 1] - fy) < 0.6)
        if sel.any():
            print('   ', o['name'], 'nvert=', int(sel.sum()), 'ej=', V[sel][0].round(2).tolist())

print('=== (c) pip del eje en poligonos')
bld = M['contexto']['buildings']
for tag, fx, fy in (('s16', -81.93, 17.55), ('s44', -59.56, 32.61)):
    hits = [bi for bi, b in enumerate(bld) if len(b['pts']) > 3 and pip(fx, fy, b['pts'])]
    print(' ', tag, 'dentro de edificios:', hits, [bld[i].get('name', '') for i in hits])

print('=== (d) ECI_ZOCALO bbox build10')
for o in objs:
    if o['name'] == 'ECI_ZOCALO':
        V = o['V']
        print('  x[%.2f,%.2f] y[%.2f,%.2f]' % (V[:, 0].min(), V[:, 0].max(), V[:, 1].min(), V[:, 1].max()))
        for tag, fx, fy in (('s16', -81.93, 17.55), ('s44', -59.56, 32.61)):
            d = np.hypot(V[:, 0] - fx, V[:, 1] - fy).min()
            print('  dist vert mas cercano a', tag, '= %.2f' % d)

print('=== (e) eje arenal-alcala: puntos declarados cerca de s16/s44')
for eje in M['recorridos']['ejes']:
    if 'arenal' in eje.get('id', '') or 'arenal' in eje.get('nombre', ''):
        pts = eje['pts']
        print('  eje', eje.get('id', eje.get('nombre')), 'npts', len(pts))
        for p in pts:
            if math.hypot(p[0] + 81.93, p[1] - 17.55) < 8 or math.hypot(p[0] + 59.56, p[1] - 32.61) < 8:
                print('   pt', [round(a, 2) for a in p])
