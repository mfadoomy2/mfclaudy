# -*- coding: utf-8 -*-
"""
SOL_REFUGIO_3D_PROXY_v001 — constructor del modelo proxy transitable.
Fuente XY: geometria_maestra.json (planta maestra Fase 01 = fuente de verdad).
Fuente Z:  HEIGHT_SYSTEM.md (cotas CONFIRMED/INFERRED del workflow de interiores).
Salidas:  SOL_REFUGIO_3D_PROXY_v001.3dm (capas + bloques + nombres) y _viewer/scene.js.
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
rng = random.Random(2026)

# ---- overrides F03A (propuesta v1.1, ver geometria_overrides_f03a.json) ----
OV = json.load(open(os.path.join(HERE, 'geometria_overrides_f03a.json'), encoding='utf-8'))
for c in m['circulacion']['corridors']:
    ov = OV['corridors'].get(c['id'])
    if ov:
        c['pts'] = [tuple(p) for p in ov]
METRO_XY = [(e['x'], e['y']) for e in m['contexto']['metro'] if -110 < e['x'] < 100 and -45 < e['y'] < 75]
R_EXCL = OV['metro_exclusion_radius']


def near_metro(x, y, extra=0.0):
    return any(math.hypot(x - mx, y - my) < R_EXCL + extra for (mx, my) in METRO_XY)


m['programa']['capsules'] = [c for c in m['programa']['capsules'] if not near_metro(c['cx'], c['cy'], max(c['w'], 1.8) / 2)]
for p in m['paisaje']['planters']:
    p['pts'] = [q for q in p['pts'] if not near_metro(q[0], q[1], 0.9)]
for b in m['programa']['benches']:
    b['pts'] = [q for q in b['pts'] if not near_metro(q[0], q[1], 0.5)]
m['estructura_ligera']['drops'] = [d for d in m['estructura_ligera']['drops'] if not near_metro(d[0], d[1], 1.0)]
m['estructura_ligera']['masts'] = [p for p in m['estructura_ligera']['masts'] if not near_metro(p[0], p[1], 0.3)]
m['paisaje']['new_trees'] = [t for t in m['paisaje']['new_trees'] if not near_metro(t[0], t[1], 0.4)]
for idx_s, (f0, f1) in OV.get('planter_trim', {}).items():
    pl = m['paisaje']['planters'][int(idx_s)]
    n = len(pl['pts'])
    pl['pts'] = pl['pts'][int(f0 * n):int(f1 * n)]
for pid, (nx_, ny_) in OV.get('pond_moves', {}).items():
    for p in m['agua_clima']['ground_ponds']:
        if p['id'] == pid and p['kind'] == 'circle':
            p['cx'], p['cy'] = nx_, ny_
cy_min = OV.get('capsule_rules', {}).get('T-O_cy_min')
if cy_min is not None:
    m['programa']['capsules'] = [c for c in m['programa']['capsules']
                                 if not (c.get('id') == 'T-O' and c['cy'] < cy_min)]
cx_max = OV.get('capsule_rules', {}).get('T-SE_cx_max')
if cx_max is not None:
    m['programa']['capsules'] = [c for c in m['programa']['capsules']
                                 if not (c.get('id') == 'T-SE' and c['cx'] > cx_max)]
lsh = OV.get('lab_shift')
if lsh:
    m['programa']['lab']['pts'] = [(p[0] + lsh[0], p[1] + lsh[1]) for p in m['programa']['lab']['pts']]
for (old, new) in OV.get('tree_moves', []):
    m['paisaje']['new_trees'] = [tuple(new) if (abs(t[0] - old[0]) < 0.6 and abs(t[1] - old[1]) < 0.6) else t
                                 for t in m['paisaje']['new_trees']]

# ---------------- HEIGHT SYSTEM (ver HEIGHT_SYSTEM.md) ----------------
H = dict(
    PERSON=1.70, SEATING=0.45, PLANTER=0.60, BENCH_BACK=0.85, POND_CURB=0.60,
    CLEAR_MIN=3.00, BRANCH=3.00, MIST=4.00, LOW=5.00, RIBBON=6.00, MID=6.75,
    HIGH=8.50, TANK_ELEV=10.50, DOME=8.00, TREE_NEW=5.00, TREE_EXIST=7.00,
    GTANK=1.35, NURSERY=3.00,
)
LOOP_Z = {'C1-L1': 10.0, 'C1-L2': 8.0, 'C1-L3': 8.0, 'C2-L1': 11.0, 'C2-L2': 9.0,
          'C2-L3': 7.5, 'C3-L1': 10.0, 'C3-L2': 8.5}
POD_TRAIN = dict(dia=2.4, length=5.5, z=0.3 + 1.2)   # apoyo 0.3, centro a 1.5

# ---------------- capas ----------------
LAYERS = [
    ('00_CONTEXT', (205, 200, 192, 255), 1.0),
    ('01_GROUND', (240, 238, 233, 255), 1.0),
    ('02_PRIMARY_STRUCTURE', (62, 150, 155, 255), 1.0),
    ('03_SECONDARY_STRUCTURE', (120, 170, 172, 255), 1.0),
    ('04_MASTS', (150, 148, 142, 255), 1.0),
    ('05_CABLES', (120, 120, 118, 255), 1.0),
    ('06_MEMBRANES', (225, 235, 225, 120), 0.45),
    ('07_CANOPIES', (195, 212, 138, 190), 0.72),
    ('08_PINK_MODULES', (231, 148, 172, 220), 0.85),
    ('09_PLANTERS', (111, 143, 83, 255), 1.0),
    ('10_FURNITURE', (176, 137, 104, 255), 1.0),
    ('11_WATER', (110, 170, 140, 200), 0.8),
    ('12_MIST', (143, 199, 174, 160), 0.6),
    ('13_PIPES', (214, 87, 127, 255), 1.0),
    ('14_VEGETATION_PROXY', (126, 158, 106, 255), 1.0),
    ('16_PEOPLE_PROXY', (90, 90, 90, 255), 1.0),
    ('17_METRO_CLEARANCES', (91, 91, 143, 90), 0.3),
    ('99_HELPERS', (40, 40, 40, 255), 1.0),
]

f3 = r3.File3dm()
f3.Settings.ModelUnitSystem = r3.UnitSystem.Meters
LIDX = {}
for name, col, _op in LAYERS:
    lay = r3.Layer()
    lay.Name = name
    lay.Color = col
    LIDX[name] = f3.Layers.Add(lay)

SCENE = []   # [{layer,color,opacity,V,F}] para three.js
LINES = []   # [{layer,color,pts}]
COUNTS = {}


def att(layer, name):
    a = r3.ObjectAttributes()
    a.LayerIndex = LIDX[layer]
    a.Name = name
    return a


def add_mesh(layer, name, VF, to_scene=True):
    V, F = VF
    if not F:
        return
    mm = r3.Mesh()
    for (x, y, z) in V:
        mm.Vertices.Add(x, y, z)
    for (a, b, c) in F:
        mm.Faces.AddFace(a, b, c)
    f3.Objects.AddMesh(mm, att(layer, name))
    COUNTS[layer] = COUNTS.get(layer, 0) + 1
    if to_scene:
        col = next(c for (n, c, o) in LAYERS if n == layer)
        op = next(o for (n, c, o) in LAYERS if n == layer)
        SCENE.append(dict(layer=layer, color=[col[0], col[1], col[2]], opacity=op,
                          V=[[round(v[0], 3), round(v[1], 3), round(v[2], 3)] for v in V], F=F))


def add_line(layer, name, pts):
    pl = r3.Polyline()
    for p in pts:
        pl.Add(p[0], p[1], p[2] if len(p) > 2 else 0)
    f3.Objects.AddCurve(pl.ToPolylineCurve(), att(layer, name))
    col = next(c for (n, c, o) in LAYERS if n == layer)
    LINES.append(dict(layer=layer, color=[col[0], col[1], col[2]],
                      pts=[[round(p[0], 3), round(p[1], 3), round(p[2], 3) if len(p) > 2 else 0] for p in pts]))


def ell_xy(cx, cy, rx, ry, rot, n=64):
    return mk.ell_pts(cx, cy, rx, ry, rot, n)


# ================= 00_CONTEXT =================
cc = m['contexto']['casa_correos']
poly = [(p[0], p[1]) for p in cc['pts']]
wallV, wallF = mk.strip([(p[0], p[1]) for p in poly], 0.4, 0, 17)
add_mesh('00_CONTEXT', 'CTX_CASA_CORREOS', (wallV, wallF))
add_mesh('00_CONTEXT', 'CTX_CC_TORRE', mk.box((-25.2, -37.5, 17), 7.5, 6.5, 12))
add_mesh('00_CONTEXT', 'CTX_CC_RELOJ', mk.cylinder((-25.2, -34.35, 26.5), (-25.2, -34.05, 26.5), 1.6, 16))
add_mesh('00_CONTEXT', 'CTX_CC_CUPULIN', mk.sphere((-25.2, -37.5, 29.0), 2.2, 10, 6))
n_ctx = 0
for b in m['contexto']['buildings']:
    if b['name'] == cc['name'] or len(b['pts']) < 4:
        continue
    xs = [p[0] for p in b['pts']]
    ys = [p[1] for p in b['pts']]
    if max(xs) < -130 or min(xs) > 150 or max(ys) < -100 or min(ys) > 110:
        continue
    wl = mk.strip([(p[0], p[1]) for p in b['pts']], 0.3, 0, 14)
    add_mesh('00_CONTEXT', 'CTX_BLD_%03d' % n_ctx, wl)
    n_ctx += 1

# ================= 01_GROUND =================
add_mesh('01_GROUND', 'GROUND_PLANE', mk.box((0, 5, -0.12), 320, 220, 0.12))

# ================= 02_PRIMARY_STRUCTURE =================
for lp in m['estructura_principal']['loops']:
    z = LOOP_Z[lp['id']]
    pts = [(p[0], p[1], z) for p in ell_xy(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'], 72)]
    add_mesh('02_PRIMARY_STRUCTURE', 'PRIMARY_%s' % lp['id'], mk.tube(pts, 0.30, 10))
    add_line('02_PRIMARY_STRUCTURE', 'AXIS_%s' % lp['id'], pts)
dm = m['estructura_principal']['dome']
dv, df = mk.sphere((dm['cx'], dm['cy'], 0.0), dm['r'], 14, 10)
dv2 = [(x, y, max(z * (H['DOME'] / dm['r']), 0)) for (x, y, z) in dv]
add_mesh('06_MEMBRANES', 'DOME_MEMBRANE', (dv2, df))

# ================= CANOPIES + MASTS + SECONDARY + CABLES =================
DISCS = m['paisaje']['discs']
for i, d in enumerate(DISCS):
    cota = min(max(d.get('cota', 6.0), H['LOW'] - 0.8), H['HIGH'])
    add_mesh('07_CANOPIES', 'CANOPY_LF_%03d' % (i + 1), mk.disc_sag((d['cx'], d['cy']), d['r'], cota))
    add_mesh('03_SECONDARY_STRUCTURE', 'CANOPY_RIM_%03d' % (i + 1),
             mk.torus((d['cx'], d['cy'], cota), d['r'], 0.06, 18, 6))

MASTS = m['estructura_ligera']['masts']


def nearest_discs(x, y, k=2, dmax2=20):
    ds = sorted(DISCS, key=lambda dd: (dd['cx'] - x) ** 2 + (dd['cy'] - y) ** 2)
    return [dd for dd in ds[:k] if (dd['cx'] - x) ** 2 + (dd['cy'] - y) ** 2 < dmax2]


for i, (mx, my) in enumerate(MASTS):
    nd = nearest_discs(mx, my)
    top = max([min(dd.get('cota', 6) + 0.3, H['HIGH']) for dd in nd], default=H['LOW']) if nd else H['LOW']
    add_mesh('04_MASTS', 'MAST_%03d' % (i + 1), mk.cylinder((mx, my, 0), (mx, my, H['BRANCH']), 0.13, 8))
    for dd in nd:
        cota = min(max(dd.get('cota', 6.0), H['LOW'] - 0.8), H['HIGH'])
        add_mesh('03_SECONDARY_STRUCTURE', 'BRANCH_%03d' % (i + 1),
                 mk.cylinder((mx, my, H['BRANCH']), (dd['cx'], dd['cy'], cota - 0.35), 0.09, 6))
        add_line('05_CABLES', 'CABLE_%03d' % (i + 1),
                 [(mx, my, H['BRANCH']), (dd['cx'], dd['cy'], cota)])

# cables de los loops a discos proximos
for lp in m['estructura_principal']['loops']:
    z = LOOP_Z[lp['id']]
    for adeg in range(0, 360, 30):
        px = lp['cx'] + lp['rx'] * math.cos(math.radians(adeg))
        py = lp['cy'] + lp['ry'] * math.sin(math.radians(adeg))
        nd = nearest_discs(px, py, 1, 42)
        if nd:
            dd = nd[0]
            cota = min(max(dd.get('cota', 6.0), H['LOW'] - 0.8), H['HIGH'])
            add_line('05_CABLES', 'LOOPCABLE_%s_%d' % (lp['id'], adeg),
                     [(px, py, z), (dd['cx'], dd['cy'], cota)])

# ================= CIRCULACION: cinta a +6 =================
rib = m['circulacion']['ribbon']
rib3 = [(p[0], p[1], H['RIBBON']) for p in rib]
deckV, deckF = mk.strip([(p[0], p[1]) for p in rib], 2.5, H['RIBBON'] - 0.25, H['RIBBON'])
add_mesh('02_PRIMARY_STRUCTURE', 'RIBBON_DECK', (deckV, deckF))
# barandillas
for off in (1.15, -1.15):
    side = []
    n = len(rib)
    for i, p in enumerate(rib):
        a = rib[max(i - 1, 0)]
        b = rib[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1e-9
        side.append((p[0] - dy / L * off, p[1] + dx / L * off, H['RIBBON'] + 1.05))
    add_line('03_SECONDARY_STRUCTURE', 'RIBBON_RAIL', side)
# soportes cada ~12 m evitando corredores
CORR = [c['pts'] for c in m['circulacion']['corridors']]


def near_corridor(x, y, dmin=2.2):
    for pts in CORR:
        for i in range(len(pts) - 1):
            ax, ay = pts[i]
            bx, by = pts[i + 1]
            vx, vy = bx - ax, by - ay
            L2 = vx * vx + vy * vy or 1e-9
            t = max(0, min(1, ((x - ax) * vx + (y - ay) * vy) / L2))
            if math.hypot(x - (ax + vx * t), y - (ay + vy * t)) < dmin:
                return True
    return False


acc = 0.0
sup_n = 0
for i in range(1, len(rib)):
    acc += math.hypot(rib[i][0] - rib[i - 1][0], rib[i][1] - rib[i - 1][1])
    if acc > 12:
        x, y = rib[i]
        if not near_corridor(x, y):
            sup_n += 1
            add_mesh('02_PRIMARY_STRUCTURE', 'RIBBON_SUP_%02d' % sup_n,
                     mk.cylinder((x, y, 0), (x, y, H['RIBBON'] - 0.25), 0.16, 8))
            acc = 0.0
# escaleras (zanca ligera inclinada, no torre maciza)
for i, (sx, sy) in enumerate(m['circulacion']['stairs']):
    top = H['RIBBON'] - 0.25
    run = top * 1.15
    p0 = (sx - run / 2, sy, 0.0)
    p1 = (sx + run / 2, sy, top)
    add_mesh('03_SECONDARY_STRUCTURE', 'RIBBON_STAIR_%d' % (i + 1),
             mk.merge([mk.cylinder(p0, p1, 0.16, 6),
                       mk.cylinder((p0[0], p0[1] + 1.2, 0), (p1[0], p1[1] + 1.2, top), 0.16, 6),
                       mk.cylinder((p0[0], p0[1] + 0.6, 0), (p0[0], p0[1] + 0.6, 0.9), 0.1, 6)]))

# ================= MEMBRANAS: redes tensadas =================
for lp, a0, a1 in [(m['estructura_principal']['loops'][0], 150, 260),
                   (m['estructura_principal']['loops'][3], -30, 80),
                   (m['estructura_principal']['loops'][6], 120, 230)]:
    z = LOOP_Z[lp['id']]
    outer = [(p[0], p[1], z - 0.4) for p in ell_xy(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'], 24)]
    inner = [(p[0], p[1], z - 2.2) for p in ell_xy(lp['cx'], lp['cy'], lp['rx'] * 0.45, lp['ry'] * 0.45, lp['rot'], 24)]
    i0, i1 = int(a0 / 360 * 24), int(a1 / 360 * 24)
    V, F = [], []
    seg = [(outer[i % 24], inner[i % 24]) for i in range(i0, i1 + 1)]
    for (o, ii) in seg:
        V.append(o); V.append(ii)
    for i in range(len(seg) - 1):
        a = 2 * i
        F.append((a, a + 2, a + 3)); F.append((a, a + 3, a + 1))
    add_mesh('06_MEMBRANES', 'NET_%s' % lp['id'], (V, F))

# ================= 08_PINK_MODULES =================
pods_ground = []
for i, c in enumerate(m['programa']['capsules']):
    cid = c.get('id', 'POD')
    if cid in ('T-O', 'T-SE'):
        vf = mk.pill((c['cx'], c['cy'], POD_TRAIN['z']), POD_TRAIN['length'] * c['w'] / 5.5 if c['w'] > 3 else 4.5,
                     POD_TRAIN['dia'], c.get('rot', 0))
        add_mesh('08_PINK_MODULES', 'PINK_POD_%03d' % (i + 1), vf)
        pods_ground.append((c['cx'], c['cy'], 2.6))
    else:
        dia = max(c['w'], 1.8)
        if cid == 'R-N' and i % 3 == 0:
            z = 4.5   # dos esferas colgadas (999C4F45)
        else:
            z = 0.3 + dia / 2
            pods_ground.append((c['cx'], c['cy'], dia / 2 + 0.4))
        add_mesh('08_PINK_MODULES', 'PINK_POD_%03d' % (i + 1), mk.sphere((c['cx'], c['cy'], z), dia / 2, 12, 8))
lab = m['programa']['lab']
labpts = [(p[0], p[1]) for p in lab['pts']]
add_mesh('08_PINK_MODULES', 'LAB02_WALLS', mk.strip(labpts, 0.12, 0, 3.5))

# ================= 09/10 PLANTERS + FURNITURE =================
for i, p in enumerate(m['paisaje']['planters']):
    add_mesh('09_PLANTERS', 'PLANTER_%03d' % (i + 1), mk.strip(p['pts'], 1.4, 0, H['PLANTER']))
for i, b in enumerate(m['programa']['benches']):
    add_mesh('10_FURNITURE', 'PLANTER_BENCH_%03d' % (i + 1), mk.strip(b['pts'], 0.6, 0, H['SEATING']))

# depositos-gota
for i, (dx, dy) in enumerate(m['estructura_ligera']['drops']):
    add_mesh('13_PIPES', 'DROP_TANK_%02d' % (i + 1), mk.cylinder((dx, dy, 0.1), (dx, dy, 2.2), 0.8, 10))

# depositos elevados sobre torre
for t in m['estructura_ligera']['tanks']:
    for k in range(t['n']):
        cx = t['cx'] + k * 2.6
        add_mesh('04_MASTS', '%s_POLE_%d' % (t['id'], k), mk.cylinder((cx, t['cy'], 0), (cx, t['cy'], H['TANK_ELEV'] - 1), 0.18, 8))
        add_mesh('08_PINK_MODULES', '%s_TANK_%d' % (t['id'], k), mk.torus((cx, t['cy'], H['TANK_ELEV']), t['r'], 0.85, 16, 8))
        add_line('13_PIPES', '%s_RISER_%d' % (t['id'], k), [(cx, t['cy'], H['TANK_ELEV']), (cx, t['cy'], 0.3)])

# ================= 11_WATER + 12_MIST + 13_PIPES =================
for p in m['agua_clima']['pools']:
    cota = p['cota']
    pts = ell_xy(p['cx'], p['cy'], p['rx'], p['ry'], p['rot'], 36)
    add_mesh('11_WATER', 'BASIN_ELEV_%s' % p['id'], mk.surf(pts[:-1], cota))
    add_mesh('03_SECONDARY_STRUCTURE', 'BASIN_RIM_%s' % p['id'],
             mk.tube([(q[0], q[1], cota) for q in pts], 0.12, 8))
for p in m['agua_clima']['ground_ponds']:
    if p['kind'] == 'circle':
        pts = ell_xy(p['cx'], p['cy'], p['r'], p['r'], 0, 28)
        add_mesh('09_PLANTERS', 'POND_CURB_%s' % p['id'], mk.tube([(q[0], q[1], H['POND_CURB']) for q in pts], 0.18, 8))
        add_mesh('11_WATER', 'POND_%s' % p['id'], mk.surf(pts[:-1], H['POND_CURB'] - 0.15))
    else:
        pts = [(q[0], q[1]) for q in p['pts']]
        add_mesh('11_WATER', 'POND_%s' % p['id'], mk.surf(pts, 0.45))
sp = m['agua_clima']['splash']
add_mesh('11_WATER', 'SPLASH_PAD', mk.surf(ell_xy(sp['cx'], sp['cy'], sp['rx'], sp['ry'], sp['rot'], 30)[:-1], 0.03))
for i, (nx, ny) in enumerate(m['agua_clima']['nebul']):
    add_mesh('12_MIST', 'MIST_NOZZLE_%03d' % (i + 1), mk.sphere((nx, ny, H['MIST']), 0.15, 6, 4))
for i, w in enumerate(m['agua_clima']['mains']):
    add_mesh('13_PIPES', 'WATER_PIPE_%02d' % (i + 1), mk.tube([(p[0], p[1], 0.35) for p in w], 0.17, 8))

# ================= 14_VEGETATION_PROXY =================
def tree(x, y, h, crown_r, name):
    add_mesh('14_VEGETATION_PROXY', name + '_TRUNK', mk.cylinder((x, y, 0), (x, y, h * 0.6), 0.14, 6))
    add_mesh('14_VEGETATION_PROXY', name + '_CROWN', mk.sphere((x, y, h * 0.6 + crown_r * 0.55), crown_r, 10, 7))


for i, (tx, ty) in enumerate(m['paisaje']['new_trees']):
    tree(tx, ty, H['TREE_NEW'], 1.9, 'TREE_NEW_%02d' % (i + 1))
for i, t in enumerate(m['contexto']['trees']):
    if -110 < t['x'] < 100 and -45 < t['y'] < 75:
        tree(t['x'], t['y'], H['TREE_EXIST'], 2.4, 'TREE_EX_%02d' % (i + 1))
# vegetacion baja junto a jardineras (muestras)
for i, p in enumerate(m['paisaje']['planters'][::2]):
    for q in p['pts'][::5]:
        add_mesh('14_VEGETATION_PROXY', 'LOWVEG_%d' % i,
                 mk.sphere((q[0] + rng.uniform(-0.5, 0.5), q[1] + rng.uniform(-0.5, 0.5),
                            H['PLANTER'] + 0.35), 0.45, 6, 4))

# ================= 16_PEOPLE_PROXY =================
PEOPLE = [(-70, -8), (-44, -14), (-20, -20), (2, -16), (26, -20), (48, -16), (-2, 30), (14, 40),
          (-36, 34), (60, 20), (-86, 2), (34, 4), (10, 4), (-14, 18), (72, -2), (-58, 22),
          (20, 24), (-30, 6)]
for i, (px, py) in enumerate(PEOPLE):
    add_mesh('16_PEOPLE_PROXY', 'PERSON_%02d' % (i + 1),
             mk.merge([mk.cylinder((px, py, 0), (px, py, 1.45), 0.22, 8),
                       mk.sphere((px, py, 1.58), 0.12, 6, 4)]))

# ================= 17_METRO_CLEARANCES =================
for i, e in enumerate(m['contexto']['metro']):
    if -110 < e['x'] < 100 and -45 < e['y'] < 75:
        add_mesh('17_METRO_CLEARANCES', 'METRO_CLEAR_%02d' % (i + 1),
                 mk.box((e['x'], e['y'], 0), 5, 5, 3.2))

# ================= 99_HELPERS =================
add_mesh('99_HELPERS', 'SCALE_CUBE_1M', mk.box((-100, -40, 0), 1, 1, 1))
add_line('99_HELPERS', 'NORTH', [(-100, -35, 0), (-100, -30, 0), (-100.8, -31, 0), (-100, -30, 0), (-99.2, -31, 0)])

# ================= salida =================
out3dm = os.path.join(HERE, 'SOL_REFUGIO_3D_PROXY_v001.3dm')
ok = f3.Write(out3dm, 8)

os.makedirs(os.path.join(HERE, '_viewer'), exist_ok=True)
scene_js = os.path.join(HERE, '_viewer', 'scene.js')
with open(scene_js, 'w', encoding='utf-8') as fp:
    fp.write('const SCENE_MESHES = ')
    json.dump(SCENE, fp, separators=(',', ':'))
    fp.write(';\nconst SCENE_LINES = ')
    json.dump(LINES, fp, separators=(',', ':'))
    fp.write(';\n')

tris = sum(len(o['F']) for o in SCENE)
print('3dm escrito:', ok, out3dm)
print('objetos por capa:', {k: v for k, v in sorted(COUNTS.items())})
print('escena: %d mallas, %d lineas, %d triangulos' % (len(SCENE), len(LINES), tris))
print('soportes de cinta:', sup_n)
