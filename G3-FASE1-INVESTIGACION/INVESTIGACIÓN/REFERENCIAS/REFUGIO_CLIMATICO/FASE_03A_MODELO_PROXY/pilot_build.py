# -*- coding: utf-8 -*-
"""
PILOT_FRAGMENT — fragmento piloto 32x33 m del nudo C2 (salon urbano + dosel + capsulas + agua + cinta).
Nivel de detalle superior al proxy: discos con nervios y embudo, mastiles ramificados con cuba,
bancos con respaldo, capsulas con gajos y amarres, estanque con murete y oleaje, escalera real.
Salidas: PILOT_FRAGMENT.3dm + _viewer/scene_pilot.js + _viewer/viewer_pilot.html
"""
import json
import math
import os
import random

import rhino3dm as r3

import mesh_kit as mk

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, '..', 'FASE_01_BASE_GRAFICA', '01_BASE_GEOMETRICA', 'planta_maestra', 'geometria_maestra.json')
m = json.load(open(GEO, encoding='utf-8'))
OV = json.load(open(os.path.join(HERE, 'geometria_overrides_f03a.json'), encoding='utf-8'))
rng = random.Random(777)

BOX = (-4, -2, 28, 31)   # x0 y0 x1 y1


def inbox(x, y, mrg=0.0):
    return BOX[0] - mrg <= x <= BOX[2] + mrg and BOX[1] - mrg <= y <= BOX[3] + mrg


# overrides relevantes
for pid, (nx_, ny_) in OV.get('pond_moves', {}).items():
    for p in m['agua_clima']['ground_ponds']:
        if p['id'] == pid and p['kind'] == 'circle':
            p['cx'], p['cy'] = nx_, ny_

H = dict(SEAT=0.45, BACK=0.85, PLANTER=0.60, CURB=0.60, BRANCH=3.0, MIST=4.0, RIBBON=6.0)
LOOP_Z = {'C2-L1': 11.0, 'C2-L2': 9.0}

LAYERS = [
    ('01_GROUND', (240, 238, 233, 255), 1.0),
    ('02_PRIMARY_STRUCTURE', (62, 150, 155, 255), 1.0),
    ('03_SECONDARY_STRUCTURE', (120, 170, 172, 255), 1.0),
    ('04_MASTS', (150, 148, 142, 255), 1.0),
    ('05_CABLES', (120, 120, 118, 255), 1.0),
    ('07_CANOPIES', (195, 212, 138, 190), 0.68),
    ('08_PINK_MODULES', (231, 148, 172, 220), 0.8),
    ('09_PLANTERS', (111, 143, 83, 255), 1.0),
    ('10_FURNITURE', (176, 137, 104, 255), 1.0),
    ('11_WATER', (110, 170, 140, 210), 0.85),
    ('12_MIST', (170, 215, 205, 120), 0.4),
    ('13_PIPES', (214, 87, 127, 255), 1.0),
    ('14_VEGETATION_PROXY', (126, 158, 106, 255), 1.0),
    ('16_PEOPLE_PROXY', (90, 90, 90, 255), 1.0),
]
f3 = r3.File3dm()
f3.Settings.ModelUnitSystem = r3.UnitSystem.Meters
LIDX = {}
for name, col, _ in LAYERS:
    lay = r3.Layer(); lay.Name = name; lay.Color = col
    LIDX[name] = f3.Layers.Add(lay)
SCENE, LINES = [], []


def att(layer, name):
    a = r3.ObjectAttributes(); a.LayerIndex = LIDX[layer]; a.Name = name
    return a


def add(layer, name, VF):
    V, F = VF
    if not F:
        return
    mm = r3.Mesh()
    for v in V:
        mm.Vertices.Add(*v)
    for fc in F:
        mm.Faces.AddFace(*fc)
    f3.Objects.AddMesh(mm, att(layer, name))
    col = next(c for (n, c, o) in LAYERS if n == layer)
    op = next(o for (n, c, o) in LAYERS if n == layer)
    SCENE.append(dict(layer=layer, color=list(col[:3]), opacity=op,
                      V=[[round(a, 3) for a in v] for v in V], F=F))


def addline(layer, pts):
    pl = r3.Polyline()
    for p in pts:
        pl.Add(*p)
    f3.Objects.AddCurve(pl.ToPolylineCurve(), att(layer, 'LN'))
    col = next(c for (n, c, o) in LAYERS if n == layer)
    LINES.append(dict(layer=layer, color=list(col[:3]), pts=[[round(a, 3) for a in p] for p in pts]))


def on_ell(cx, cy, rx, ry, rot, a_deg):
    r = math.radians(rot); a = math.radians(a_deg)
    x, y = rx * math.cos(a), ry * math.sin(a)
    return (cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r))


# ---------- suelo + despiece ----------
add('01_GROUND', 'GROUND', mk.box(((BOX[0] + BOX[2]) / 2, (BOX[1] + BOX[3]) / 2, -0.1), BOX[2] - BOX[0] + 8, BOX[3] - BOX[1] + 8, 0.1))
for k in range(int((BOX[3] - BOX[1]) / 1.8) + 1):
    yy = BOX[1] + k * 1.8
    addline('01_GROUND', [(BOX[0] - 2, yy, 0.005), (BOX[2] + 2, yy + (BOX[2] - BOX[0]) * math.tan(math.radians(7)) * 0, 0.005)])

# ---------- loops C2 (haz triple + traviesas) dentro de caja ----------
for lp in m['estructura_principal']['loops']:
    if lp['id'] not in LOOP_Z:
        continue
    z = LOOP_Z[lp['id']]
    arc = []
    for adeg in range(0, 361, 3):
        px, py = on_ell(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'], adeg)
        if inbox(px, py, 6):
            arc.append((px, py, z, adeg))
    if len(arc) < 4:
        continue
    pts = [(p[0], p[1], p[2]) for p in arc]
    add('02_PRIMARY_STRUCTURE', 'PRIMARY_%s' % lp['id'], mk.tube(pts, 0.28, 12))
    for off in (0.75, -0.75):
        pts2 = []
        for (px, py, zz, adeg) in arc:
            qx, qy = on_ell(lp['cx'], lp['cy'], lp['rx'] + off, lp['ry'] + off, lp['rot'], adeg)
            pts2.append((qx, qy, zz - 0.35))
        add('03_SECONDARY_STRUCTURE', 'SAT_%s' % lp['id'], mk.tube(pts2, 0.09, 8))
    for i in range(0, len(arc), 4):
        (px, py, zz, adeg) = arc[i]
        for off in (0.75, -0.75):
            qx, qy = on_ell(lp['cx'], lp['cy'], lp['rx'] + off, lp['ry'] + off, lp['rot'], adeg)
            add('03_SECONDARY_STRUCTURE', 'TRV', mk.cylinder((px, py, zz), (qx, qy, zz - 0.35), 0.05, 6))

# ---------- discos con nervios y embudo ----------
DISCS = [d for d in m['paisaje']['discs'] if inbox(d['cx'], d['cy'], 2)]
for i, d in enumerate(DISCS):
    cota = min(max(d.get('cota', 6.0), 4.2), 8.5)
    r = d['r']
    add('07_CANOPIES', 'CANOPY_LF_%02d' % i, mk.disc_sag((d['cx'], d['cy']), r, cota, n=24, rings=5))
    add('03_SECONDARY_STRUCTURE', 'RIM_%02d' % i, mk.torus((d['cx'], d['cy'], cota), r, 0.07, 24, 8))
    sag = max(0.25, r * 0.18)
    for k in range(10):
        a = 2 * math.pi * k / 10
        add('03_SECONDARY_STRUCTURE', 'RIB', mk.cylinder(
            (d['cx'], d['cy'], cota - sag), (d['cx'] + r * math.cos(a), d['cy'] + r * math.sin(a), cota), 0.035, 5))
    # embudo de drenaje + bajante de goteo
    add('03_SECONDARY_STRUCTURE', 'FUNNEL', mk.cylinder((d['cx'], d['cy'], cota - sag), (d['cx'], d['cy'], cota - sag - 0.5), 0.09, 6))
    addline('11_WATER', [(d['cx'], d['cy'], cota - sag - 0.5), (d['cx'], d['cy'], 0.4)])

# ---------- mastiles ramificados con cuba ----------
MASTS = [p for p in m['estructura_ligera']['masts'] if inbox(p[0], p[1], 0)]
for i, (mx, my) in enumerate(MASTS):
    nd = sorted(DISCS, key=lambda dd: (dd['cx'] - mx) ** 2 + (dd['cy'] - my) ** 2)[:2]
    nd = [dd for dd in nd if (dd['cx'] - mx) ** 2 + (dd['cy'] - my) ** 2 < 22]
    add('04_MASTS', 'MAST_%02d' % i, mk.cylinder((mx, my, 0), (mx, my, H['BRANCH']), 0.12, 8))
    add('09_PLANTERS', 'CUBA_%02d' % i, mk.cylinder((mx, my, 0), (mx, my, 0.55), 0.8, 12))
    add('14_VEGETATION_PROXY', 'CUBAVEG_%02d' % i, mk.sphere((mx, my, 0.9), 0.55, 7, 5))
    for dd in nd:
        cota = min(max(dd.get('cota', 6.0), 4.2), 8.5)
        mid = ((mx + dd['cx']) / 2, (my + dd['cy']) / 2, H['BRANCH'] + (cota - H['BRANCH']) * 0.5 + 0.4)
        add('03_SECONDARY_STRUCTURE', 'BR_A', mk.cylinder((mx, my, H['BRANCH']), mid, 0.08, 6))
        add('03_SECONDARY_STRUCTURE', 'BR_B', mk.cylinder(mid, (dd['cx'], dd['cy'], cota - 0.3), 0.07, 6))
        addline('05_CABLES', [(mx, my, H['BRANCH']), (dd['cx'], dd['cy'], cota)])

# ---------- bancos con respaldo + jardineras dobles ----------
for i, b in enumerate(m['programa']['benches']):
    pts = [q for q in b['pts'] if inbox(q[0], q[1], 1)]
    if len(pts) < 3:
        continue
    add('10_FURNITURE', 'BENCH_%d' % i, mk.strip(pts, 0.62, 0, H['SEAT']))
    back = [(q[0] * 0.99 + 0.01 * 8, q[1] * 0.99 + 0.01 * 13) for q in pts]
    add('10_FURNITURE', 'BENCHBACK_%d' % i, mk.strip(back, 0.16, H['SEAT'], H['BACK']))
for i, p in enumerate(m['paisaje']['planters']):
    pts = [q for q in p['pts'] if inbox(q[0], q[1], 1)]
    if len(pts) < 3:
        continue
    add('09_PLANTERS', 'PLANTER_%d' % i, mk.strip(pts, 1.4, 0, H['PLANTER']))
    for q in pts[::2]:
        for _ in range(4):
            add('14_VEGETATION_PROXY', 'LV', mk.sphere((q[0] + rng.uniform(-0.6, 0.6), q[1] + rng.uniform(-0.6, 0.6),
                                                        H['PLANTER'] + rng.uniform(0.2, 0.7)), rng.uniform(0.25, 0.5), 6, 4))

# ---------- estanque E-3 con murete + oleaje + parches de alga ----------
for p in m['agua_clima']['ground_ponds']:
    if p['kind'] == 'circle' and inbox(p['cx'], p['cy'], 1):
        pts = mk.ell_pts(p['cx'], p['cy'], p['r'], p['r'], 0, 32)
        add('09_PLANTERS', 'CURB_%s' % p['id'], mk.tube([(q[0], q[1], H['CURB']) for q in pts], 0.16, 8))
        add('09_PLANTERS', 'CURBWALL_%s' % p['id'], mk.strip([(q[0], q[1]) for q in pts], 0.28, 0, H['CURB']))
        add('11_WATER', 'WATER_%s' % p['id'], mk.surf(pts[:-1], H['CURB'] - 0.12))
        for f in (0.75, 0.5):
            add('11_WATER', 'WAVE', mk.torus((p['cx'], p['cy'], H['CURB'] - 0.11), p['r'] * f, 0.02, 24, 5))
        for _ in range(4):
            a = rng.uniform(0, 6.28); rr = p['r'] * rng.uniform(0.2, 0.7)
            add('14_VEGETATION_PROXY', 'ALGA', mk.sphere((p['cx'] + rr * math.cos(a), p['cy'] + rr * math.sin(a),
                                                          H['CURB'] - 0.1), rng.uniform(0.2, 0.45), 6, 3))

# ---------- capsulas con gajos, valvula y amarres ----------
for i, c in enumerate(m['programa']['capsules']):
    if c.get('id') not in ('R-N',) or not inbox(c['cx'], c['cy'], 1):
        continue
    dia = max(c['w'], 1.8)
    elevated = (i % 3 == 0)
    z = 4.5 if elevated else 0.3 + dia / 2
    add('08_PINK_MODULES', 'PINK_POD_%02d' % i, mk.sphere((c['cx'], c['cy'], z), dia / 2, 14, 10))
    for adeg in (0, 60, 120):
        arc = []
        for t in range(13):
            ph = math.pi * t / 12
            a = math.radians(adeg)
            arc.append((c['cx'] + dia / 2 * math.sin(ph) * math.cos(a),
                        c['cy'] + dia / 2 * math.sin(ph) * math.sin(a),
                        z + dia / 2 * math.cos(ph)))
        add('08_PINK_MODULES', 'SEAM', mk.tube(arc, 0.025, 5))
    add('08_PINK_MODULES', 'VALVE', mk.cylinder((c['cx'], c['cy'], z + dia / 2), (c['cx'], c['cy'], z + dia / 2 + 0.18), 0.09, 6))
    if elevated:
        addline('05_CABLES', [(c['cx'], c['cy'], z + dia / 2), (c['cx'] + 1.5, c['cy'] - 1.2, 9.0)])
    else:
        for adeg in (30, 150, 270):
            a = math.radians(adeg)
            gx, gy = c['cx'] + (dia / 2 + 0.7) * math.cos(a), c['cy'] + (dia / 2 + 0.7) * math.sin(a)
            addline('05_CABLES', [(c['cx'] + dia / 2 * 0.8 * math.cos(a), c['cy'] + dia / 2 * 0.8 * math.sin(a), z + 0.3), (gx, gy, 0)])

# ---------- red rosa + goteros + nebulizadores con abanico + vapor ----------
for w in m['agua_clima']['mains']:
    pts = [(p[0], p[1], 0.32) for p in w if inbox(p[0], p[1], 3)]
    if len(pts) >= 2:
        add('13_PIPES', 'MAIN', mk.tube(pts, 0.16, 8))
        for q in pts[::3]:
            addline('13_PIPES', [(q[0], q[1], 0.32), (q[0] + rng.uniform(-2, 2), q[1] + rng.uniform(-2, 2), 0.05)])
NEB = [p for p in m['agua_clima']['nebul'] if inbox(p[0], p[1], 0)]
for (nx, ny) in NEB:
    add('13_PIPES', 'NEBPOST', mk.cylinder((nx, ny, 0), (nx, ny, H['MIST']), 0.05, 6))
    add('13_PIPES', 'NEBHEAD', mk.sphere((nx, ny, H['MIST']), 0.12, 6, 4))
    for _ in range(9):
        add('12_MIST', 'VAPOR', mk.sphere((nx + rng.uniform(-1.4, 1.4), ny + rng.uniform(-1.4, 1.4),
                                           H['MIST'] - rng.uniform(0.2, 1.6)), rng.uniform(0.25, 0.6), 6, 4))

# ---------- cinta + escalera real ----------
rib = [p for p in m['circulacion']['ribbon'] if inbox(p[0], p[1], 6)]
if len(rib) > 3:
    deck = mk.strip([(p[0], p[1]) for p in rib], 2.5, H['RIBBON'] - 0.22, H['RIBBON'])
    add('02_PRIMARY_STRUCTURE', 'RIBBON_DECK', deck)
    for off in (1.2, -1.2):
        side = []
        n = len(rib)
        for i, p in enumerate(rib):
            a = rib[max(i - 1, 0)]; b = rib[min(i + 1, n - 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1e-9
            side.append((p[0] - dy / L * off, p[1] + dx / L * off))
        add('03_SECONDARY_STRUCTURE', 'RAILTUBE', mk.tube([(q[0], q[1], H['RIBBON'] + 1.05) for q in side], 0.04, 6))
        for q in side[::2]:
            add('03_SECONDARY_STRUCTURE', 'BALPOST', mk.cylinder((q[0], q[1], H['RIBBON']), (q[0], q[1], H['RIBBON'] + 1.05), 0.025, 5))
for (sx, sy) in m['circulacion']['stairs']:
    if not inbox(sx, sy, 2):
        continue
    top = H['RIBBON'] - 0.22
    run = top * 1.1
    for dy0 in (0, 1.2):
        add('03_SECONDARY_STRUCTURE', 'STRINGER', mk.cylinder((sx - run / 2, sy + dy0, 0), (sx + run / 2, sy + dy0, top), 0.09, 6))
    nstep = 16
    for k in range(nstep):
        t = k / (nstep - 1)
        add('03_SECONDARY_STRUCTURE', 'STEP', mk.box((sx - run / 2 + run * t, sy + 0.6, top * t), 0.32, 1.28, 0.05))

# ---------- arbol nuevo detallado ----------
for (tx, ty) in m['paisaje']['new_trees']:
    if not inbox(tx, ty, 0):
        continue
    add('14_VEGETATION_PROXY', 'TRUNK', mk.cylinder((tx, ty, 0), (tx, ty, 2.6), 0.14, 7))
    for adeg in (20, 140, 260):
        a = math.radians(adeg)
        add('14_VEGETATION_PROXY', 'BRANCH', mk.cylinder((tx, ty, 2.3), (tx + 1.1 * math.cos(a), ty + 1.1 * math.sin(a), 3.6), 0.06, 5))
    add('14_VEGETATION_PROXY', 'CROWN1', mk.sphere((tx, ty, 4.0), 1.9, 9, 7))
    add('14_VEGETATION_PROXY', 'CROWN2', mk.sphere((tx + 0.8, ty - 0.5, 3.4), 1.2, 8, 6))

# ---------- personas ----------
for (px, py) in [(2, 4), (10, 8), (16, 18), (6, 24), (20, 4)]:
    add('16_PEOPLE_PROXY', 'PERSON', mk.merge([mk.cylinder((px, py, 0), (px, py, 1.45), 0.22, 8),
                                               mk.sphere((px, py, 1.58), 0.12, 6, 4)]))

out = os.path.join(HERE, 'PILOT_FRAGMENT.3dm')
print('3dm:', f3.Write(out, 8))
with open(os.path.join(HERE, '_viewer', 'scene_pilot.js'), 'w', encoding='utf-8') as fp:
    fp.write('const SCENE_MESHES = ')
    json.dump(SCENE, fp, separators=(',', ':'))
    fp.write(';\nconst SCENE_LINES = ')
    json.dump(LINES, fp, separators=(',', ':'))
    fp.write(';\n')
vh = open(os.path.join(HERE, '_viewer', 'viewer.html'), encoding='utf-8').read().replace('scene.js', 'scene_pilot.js')
open(os.path.join(HERE, '_viewer', 'viewer_pilot.html'), 'w', encoding='utf-8').write(vh)
print('mallas:', len(SCENE), 'tris:', sum(len(o['F']) for o in SCENE))
