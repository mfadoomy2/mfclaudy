# -*- coding: utf-8 -*-
"""03B.7-A · Medicion de los dos conflictos urbanos sobre la escena v003 HORNEADA.
A) que geometria del proyecto PENETRA volumetrias de edificios (y cuanto)
B) que rodea al conjunto Metro/Cercanias/estancos (perimetros, distancias, piezas)
Salida: URBAN_CONFLICTS_v003.json + plano diagnostico _conflictos.png"""
import json
import math
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Circle

import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, '..', 'FASE_03B6_RESOLUCION'))
if len(sys.argv) > 1 and sys.argv[1] == 'v004':
    V3 = HERE
    GJ = 'geometria_maestra_v004.json'
    OUTJ, OUTP = 'URBAN_CONFLICTS_v004.json', '_conflictos_v004.png'
else:
    GJ = 'geometria_maestra_v003.json'
    OUTJ, OUTP = 'URBAN_CONFLICTS_v003.json', '_conflictos.png'
M = json.load(open(os.path.join(V3, GJ), encoding='utf-8'))
txt = open(os.path.join(V3, '_viewer', 'scene_full.js'), encoding='utf-8').read()
a = txt.index('const SCENE_MESHES = ') + len('const SCENE_MESHES = ')
MESHES = json.loads(txt[a:txt.index(';\nconst SCENE_LINES')])

PROJ_SKIP = {'00_CONTEXT', '01_GROUND', '17_METRO_CLEARANCES', '30_CURVES', '16_PEOPLE_PROXY', '12_MIST'}


def pip(x, y, poly):
    n = len(poly)
    dentro = False
    j = n - 1
    for i in range(n):
        xi, yi = poly[i][0], poly[i][1]
        xj, yj = poly[j][0], poly[j][1]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi):
            dentro = not dentro
        j = i
    return dentro


def d_borde(x, y, poly):
    best = 1e9
    for i in range(len(poly)):
        ax, ay = poly[i][0], poly[i][1]
        bx, by = poly[(i + 1) % len(poly)][0], poly[(i + 1) % len(poly)][1]
        vx, vy = bx - ax, by - ay
        L2 = vx * vx + vy * vy or 1e-9
        t = max(0, min(1, ((x - ax) * vx + (y - ay) * vy) / L2))
        best = min(best, math.hypot(x - (ax + vx * t), y - (ay + vy * t)))
    return best


BLD = []
for i, b in enumerate(M['contexto']['buildings']):
    pts = b['pts']
    if len(pts) < 4:
        continue
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    if max(xs) < -130 or min(xs) > 150 or max(ys) < -100 or min(ys) > 110:
        continue
    area = 0.5 * abs(sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1]
                         for k in range(len(pts))))
    BLD.append(dict(i=i, name=b.get('name', ''), pts=pts, area=round(area, 1),
                    bbox=(min(xs), min(ys), max(xs), max(ys))))
print('edificios en ambito:', len(BLD))

# --------- A · penetraciones proyecto -> edificio ---------
PEN = {}
GRAZE = {}
for o in MESHES:
    if o['layer'] in PROJ_SKIP:
        continue
    if o.get('fam') == 'VEG2_ARBOL_EX':
        continue   # arbolado urbano EXISTENTE (OSM): que roce su propia fachada es la realidad, no el proyecto
    V = o['V']
    xs = [v[0] for v in V]; ys = [v[1] for v in V]
    ob = (min(xs), min(ys), max(xs), max(ys))
    for b in BLD:
        bb = b['bbox']
        if ob[2] < bb[0] - 1.5 or ob[0] > bb[2] + 1.5 or ob[3] < bb[1] - 1.5 or ob[1] > bb[3] + 1.5:
            continue
        # altura REAL del obstaculo: manzanas bloquean todo; Estacion ~6 m; kioscos ~3.6 m
        htope = 6.5 if b['i'] == 106 else (4.1 if b['area'] < 80 else 99.0)
        nin = 0
        maxdep = 0.0
        zmin, zmax = 1e9, -1e9
        ex = None
        for v in V[::max(1, len(V) // 160)]:
            if v[2] > htope:
                continue
            if pip(v[0], v[1], b['pts']):
                nin += 1
                d = d_borde(v[0], v[1], b['pts'])
                if d > maxdep:
                    maxdep = d
                    ex = (round(v[0], 1), round(v[1], 1), round(v[2], 1))
                zmin = min(zmin, v[2]); zmax = max(zmax, v[2])
        if nin:
            k = (b['i'], o['layer'], o.get('fam') or o.get('name', ''))
            r = PEN.setdefault(k, dict(edificio=b['i'], name_b=b['name'], layer=o['layer'],
                                       fam=o.get('fam') or o.get('name', ''), n_mallas=0, n_pts=0,
                                       max_dep=0.0, ejemplo=None, z=[1e9, -1e9]))
            r['n_mallas'] += 1
            r['n_pts'] += nin
            if maxdep > r['max_dep']:
                r['max_dep'] = round(maxdep, 2)
                r['ejemplo'] = ex
            r['z'][0] = round(min(r['z'][0], zmin), 1)
            r['z'][1] = round(max(r['z'][1], zmax), 1)

PENL = sorted(PEN.values(), key=lambda r: -r['max_dep'])
print('\n=== A · PENETRACIONES (proyecto dentro de edificio) ===')
for r in PENL[:24]:
    print('%-14s %-16s edif %3d %-18s mallas %3d pts %4d dep_max %.2f m z %s ej %s'
          % (r['layer'], str(r['fam'])[:16], r['edificio'], str(r['name_b'])[:18],
             r['n_mallas'], r['n_pts'], r['max_dep'], r['z'], r['ejemplo']))

# --------- B · conjunto Metro / Cercanias / kioscos ---------
MET = [e for e in M['contexto']['metro'] if -110 < e['x'] < 100 and -45 < e['y'] < 75]
KIO = [b for b in BLD if b['area'] < 80]
print('\n=== B · bocas en ambito ===')
for e in MET:
    print('  boca (%.1f, %.1f)' % (e['x'], e['y']), e.get('name', ''))
print('kioscos/estancos candidatos (area<80 m2):')
for b in KIO:
    cx = sum(p[0] for p in b['pts']) / len(b['pts'])
    cy = sum(p[1] for p in b['pts']) / len(b['pts'])
    print('  edif %d area %.0f m2 c(%.1f, %.1f) %s' % (b['i'], b['area'], cx, cy, b['name']))

RIB = M['circulacion']['ribbon']
LOOPS = M['estructura_principal']['loops']
print('\nentorno de cada boca (dist a cinta-json / loop mas cercano):')
ENT = []
for e in MET:
    dr = min(min(math.hypot(e['x'] - p[0], e['y'] - p[1]) for p in RIB), 999)
    dl = 999
    ll = ''
    for lp in LOOPS:
        d = abs(math.hypot(e['x'] - lp['cx'], e['y'] - lp['cy']) - (lp['rx'] + lp['ry']) / 2)
        if d < dl:
            dl = d; ll = lp['id']
    ENT.append(dict(x=e['x'], y=e['y'], name=e.get('name', ''), d_cinta=round(dr, 1),
                    d_loop=round(dl, 1), loop=ll))
    print('  %-14s d_cinta %5.1f · d_%s %5.1f' % (str(e.get('name', ''))[:14], dr, ll, dl))

json.dump(dict(penetraciones=PENL, bocas=ENT,
               kioscos=[dict(i=b['i'], area=b['area'], name=b['name']) for b in KIO]),
          open(os.path.join(HERE, OUTJ), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

# --------- plano diagnostico ---------
fig, ax = plt.subplots(figsize=(16, 11))
ax.set_facecolor('#F7F4EE')
for b in BLD:
    ax.add_patch(MPoly([(p[0], p[1]) for p in b['pts']], closed=True, fc='#DDD6C8', ec='#999', lw=0.5, zorder=1))
for lp in LOOPS:
    th = np.linspace(0, 2 * np.pi, 100)
    r = math.radians(lp['rot'])
    x = lp['cx'] + lp['rx'] * np.cos(th) * math.cos(r) - lp['ry'] * np.sin(th) * math.sin(r)
    y = lp['cy'] + lp['rx'] * np.cos(th) * math.sin(r) + lp['ry'] * np.sin(th) * math.cos(r)
    ax.plot(x, y, '-', color='#B08968', lw=2, zorder=3)
P = np.array(RIB)
ax.plot(P[:, 0], P[:, 1], '-', color='#D6577F', lw=2.5, zorder=4)
for r in PENL:
    if r['ejemplo']:
        ax.plot(r['ejemplo'][0], r['ejemplo'][1], 'x', ms=14, mew=3, color='red', zorder=6)
        ax.annotate('%s %.1fm' % (r['fam'], r['max_dep']), r['ejemplo'][:2], textcoords='offset points',
                    xytext=(6, 6), fontsize=8, color='red', zorder=6)
for e in MET:
    ax.add_patch(Circle((e['x'], e['y']), 5.5, fill=False, ec='#5B5B8F', lw=1.6, zorder=5))
    ax.plot(e['x'], e['y'], 's', ms=7, color='#5B5B8F', zorder=5)
for b in KIO:
    cx = sum(p[0] for p in b['pts']) / len(b['pts'])
    cy = sum(p[1] for p in b['pts']) / len(b['pts'])
    ax.plot(cx, cy, 'D', ms=8, mfc='#D98E32', mec='k', zorder=6)
ax.set_xlim(-115, 105); ax.set_ylim(-50, 80); ax.set_aspect('equal')
ax.set_title('v003 · conflictos urbanos: X rojas = penetracion en edificio · cuadrados = bocas (5.5) · rombos = kioscos')
plt.tight_layout()
plt.savefig(os.path.join(HERE, OUTP), dpi=110)
print('\nplano:', OUTP)
