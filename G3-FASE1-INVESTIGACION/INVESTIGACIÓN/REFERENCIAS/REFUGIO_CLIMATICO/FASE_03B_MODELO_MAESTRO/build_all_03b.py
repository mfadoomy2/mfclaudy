# -*- coding: utf-8 -*-
"""
FASE 03B — constructor integral.
Genera: MASTER_ARCHITECTURE_v002.3dm · ASSET_LIBRARY_v001.3dm · SOL_FULL_SCENE_v001.3dm
        + _viewer/scene_full.js (visor clay/material)
Fuente XY: geometria_maestra_v002.json · Z: HEIGHT_SYSTEM (03A).
Todo elemento repetido = BLOQUE Rhino (instancias con rotacion via Transform.Multiply).
Curvas generatrices editables en capa 30_CURVES.
"""
import json
import math
import os
import random
import sys

import rhino3dm as r3

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', 'FASE_03A_MODELO_PROXY')))
import mesh_kit as mk  # noqa: E402

m = json.load(open(os.path.join(HERE, 'geometria_maestra_v002.json'), encoding='utf-8'))
rng = random.Random(31)

H = dict(SEAT=0.45, BACK=0.85, PLANTER=0.60, CURB=0.60, BRANCH=3.0, MIST=4.0, LOW=5.0,
         RIBBON=6.0, MID=6.75, HIGH=8.5, TANK=10.5, GTANK=1.35)
LOOP_Z = {'C1-L1': 10.0, 'C1-L2': 8.0, 'C1-L3': 8.0, 'C2-L1': 11.0, 'C2-L2': 9.0,
          'C2-L3': 7.5, 'C3-L1': 10.0, 'C3-L2': 8.5}

LAYERS = [
    ('00_CONTEXT', (205, 200, 192, 255), 1.0),
    ('01_GROUND', (240, 238, 233, 255), 1.0),
    ('02_PRIMARY_STRUCTURE', (176, 137, 104, 255), 1.0),     # madera laminada (D14)
    ('03_SECONDARY_STRUCTURE', (196, 168, 138, 255), 1.0),
    ('04_MASTS', (186, 152, 118, 255), 1.0),
    ('05_CABLES', (120, 120, 118, 255), 1.0),
    ('06_MEMBRANES', (228, 236, 228, 110), 0.4),
    ('07_CANOPIES', (195, 212, 138, 190), 0.68),
    ('08_PINK_MODULES', (231, 148, 172, 215), 0.8),
    ('09_PLANTERS', (111, 143, 83, 255), 1.0),
    ('10_FURNITURE', (176, 137, 104, 255), 1.0),
    ('11_WATER', (110, 170, 140, 210), 0.82),
    ('12_MIST', (170, 215, 205, 110), 0.35),
    ('13_PIPES', (214, 87, 127, 255), 1.0),
    ('14_VEGETATION_PROXY', (126, 158, 106, 255), 1.0),
    ('15_VEGETATION_FULL', (104, 142, 88, 255), 1.0),
    ('16_PEOPLE_PROXY', (90, 90, 90, 255), 1.0),
    ('17_METRO_CLEARANCES', (91, 91, 143, 80), 0.25),
    ('30_CURVES', (30, 30, 30, 255), 1.0),
]
LCOL = {n: c for (n, c, o) in LAYERS}
LOP = {n: o for (n, c, o) in LAYERS}


def ell_pts(cx, cy, rx, ry, rot, n=64):
    return mk.ell_pts(cx, cy, rx, ry, rot, n)


def on_ell(cx, cy, rx, ry, rot, a_deg):
    r = math.radians(rot); a = math.radians(a_deg)
    x, y = rx * math.cos(a), ry * math.sin(a)
    return (cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r))


# ============================================================ FAMILIAS (partes = [(layer,(V,F))])
def leaf_canopy(rx, ry, ribs=10, drop=None, sag=None, tilt=0.0):
    """LEAF_CANOPY_MASTER: aro + nervios + membrana + lamina + embudo + bajante + orejetas."""
    drop = drop if drop is not None else max(0.25, 0.18 * max(rx, ry))
    sag = sag if sag is not None else 0.08 * max(rx, ry)
    parts = []
    rim = [(p[0], p[1], math.sin(math.radians(tilt)) * p[0]) for p in ell_pts(0, 0, rx, ry, 0, 40)]
    parts.append(('03_SECONDARY_STRUCTURE', mk.tube(rim, 0.06, 8)))
    # membrana con flecha y embudo central
    V, F = [], []
    rings, n = 5, 28
    for j in range(rings + 1):
        f = j / rings
        for i in range(n):
            a = 2 * math.pi * i / n
            px, py = rx * f * math.cos(a), ry * f * math.sin(a)
            z = -drop * (1 - f) ** 1.6 - sag * math.sin(math.pi * f) * 0.5 + math.sin(math.radians(tilt)) * px
            V.append((px, py, z))
    for j in range(rings):
        for i in range(n):
            i2 = (i + 1) % n
            a = j * n + i; b = j * n + i2; c = (j + 1) * n + i2; d = (j + 1) * n + i
            F.append((a, c, b)); F.append((a, d, c))
    parts.append(('07_CANOPIES', (V, F)))
    # lamina de microalgas (D15): disco interior a +0.04
    wpts = ell_pts(0, 0, rx * 0.82, ry * 0.82, 0, 24)
    parts.append(('11_WATER', mk.surf(wpts[:-1], -drop * 0.35 + 0.04)))
    for k in range(ribs):
        a = 2 * math.pi * k / ribs
        p1 = (rx * math.cos(a), ry * math.sin(a), math.sin(math.radians(tilt)) * rx * math.cos(a))
        parts.append(('03_SECONDARY_STRUCTURE', mk.cylinder((0, 0, -drop), p1, 0.035, 5)))
    parts.append(('03_SECONDARY_STRUCTURE', mk.cylinder((0, 0, -drop), (0, 0, -drop - 0.55), 0.08, 6)))
    for adeg in (0, 120, 240):
        px, py = on_ell(0, 0, rx, ry, 0, adeg)
        parts.append(('03_SECONDARY_STRUCTURE', mk.sphere((px, py, 0), 0.09, 5, 4)))
    return parts


def mast(arms=2, top=5.6):
    parts = [('04_MASTS', mk.cylinder((0, 0, 0), (0, 0, H['BRANCH']), 0.12, 9))]
    parts.append(('09_PLANTERS', mk.cylinder((0, 0, 0), (0, 0, 0.55), 0.8, 12)))
    parts.append(('15_VEGETATION_FULL', mk.sphere((0, 0, 0.95), 0.55, 7, 5)))
    for k in range(arms):
        a = 2 * math.pi * k / max(arms, 1) + 0.5
        mid = (1.4 * math.cos(a), 1.4 * math.sin(a), H['BRANCH'] + (top - H['BRANCH']) * 0.55)
        tip = (2.9 * math.cos(a), 2.9 * math.sin(a), top)
        parts.append(('04_MASTS', mk.cylinder((0, 0, H['BRANCH']), mid, 0.08, 6)))
        parts.append(('04_MASTS', mk.cylinder(mid, tip, 0.06, 6)))
    parts.append(('13_PIPES', mk.cylinder((0.14, 0, 0.5), (0.14, 0, H['MIST']), 0.03, 5)))
    parts.append(('13_PIPES', mk.sphere((0.14, 0, H['MIST']), 0.1, 5, 4)))
    return parts


def pink_pod(dia, door=False):
    r = dia / 2
    parts = [('08_PINK_MODULES', mk.sphere((0, 0, r + 0.3), r, 16, 11))]
    for adeg in (0, 60, 120):
        arc = []
        for t in range(15):
            ph = math.pi * t / 14
            a = math.radians(adeg)
            arc.append((r * math.sin(ph) * math.cos(a), r * math.sin(ph) * math.sin(a), r + 0.3 + r * math.cos(ph)))
        parts.append(('08_PINK_MODULES', mk.tube(arc, 0.025, 5)))
    parts.append(('08_PINK_MODULES', mk.cylinder((0, 0, dia + 0.3), (0, 0, dia + 0.48), 0.09, 6)))
    for adeg in (30, 150, 270):
        a = math.radians(adeg)
        parts.append(('03_SECONDARY_STRUCTURE', mk.cylinder((r * 0.75 * math.cos(a), r * 0.75 * math.sin(a), 0.3),
                                                            (r * 0.9 * math.cos(a), r * 0.9 * math.sin(a), 0.02), 0.05, 5)))
        parts.append(('03_SECONDARY_STRUCTURE', mk.cylinder((r * 0.9 * math.cos(a), r * 0.9 * math.sin(a), 0.02),
                                                            (r * 0.9 * math.cos(a), r * 0.9 * math.sin(a), 0.0), 0.14, 6)))
    if door:
        ring = []
        for t in range(17):
            a = 2 * math.pi * t / 16
            ring.append((r * 0.995, 0.62 * math.cos(a), r + 0.3 + 0.7 * math.sin(a)))
        parts.append(('08_PINK_MODULES', mk.tube(ring, 0.04, 5)))
    return parts


def pod_train():
    parts = [('08_PINK_MODULES', mk.pill((0, 0, 0), 5.5, 2.4, 0, z=1.5))]
    for dx in (-1.8, -0.6, 0.6, 1.8):
        ring = []
        for t in range(21):
            a = 2 * math.pi * t / 20
            ring.append((dx, 1.21 * math.cos(a), 1.5 + 1.21 * math.sin(a)))
        parts.append(('08_PINK_MODULES', mk.tube(ring, 0.035, 5)))
    for dx in (-1.5, 1.5):
        parts.append(('03_SECONDARY_STRUCTURE', mk.box((dx, 0, 0.0), 0.6, 1.9, 0.32)))
    parts.append(('13_PIPES', mk.cylinder((2.75, 0, 1.5), (3.15, 0, 1.5), 0.08, 6)))
    return parts


def drop_tank():
    parts = [('13_PIPES', mk.sphere((0, 0, 0.95), 0.78, 12, 9))]
    cone = []
    for t in range(13):
        a = 2 * math.pi * t / 12
        cone.append((0.5 * math.cos(a), 0.5 * math.sin(a), 1.55))
    V = [(0, 0, 2.25)] + cone
    F = [(0, 1 + i, 1 + (i + 1) % 12) for i in range(12)]
    parts.append(('13_PIPES', (V, F)))
    for zz in (0.7, 1.2):
        rr = math.sqrt(max(0.78 ** 2 - (zz - 0.95) ** 2, 0.05)) + 0.02
        parts.append(('03_SECONDARY_STRUCTURE', mk.torus((0, 0, zz), rr, 0.025, 16, 5)))
    parts.append(('03_SECONDARY_STRUCTURE', mk.cylinder((0, 0, 0), (0, 0, 0.3), 0.1, 6)))
    return parts


def nursery():
    parts = []
    for (dx, dy) in ((-0.9, -0.35), (0.9, -0.35), (-0.9, 0.35), (0.9, 0.35)):
        parts.append(('10_FURNITURE', mk.cylinder((dx, dy, 0), (dx, dy, 3.0), 0.05, 5)))
    for z in (0.75, 1.5, 2.25, 3.0):
        parts.append(('10_FURNITURE', mk.box((0, 0, z - 0.03), 2.0, 0.8, 0.05)))
        for k in range(4):
            px = -0.75 + k * 0.5
            parts.append(('15_VEGETATION_FULL', mk.sphere((px, 0, z + 0.16), 0.16, 5, 4)))
    parts.append(('13_PIPES', mk.cylinder((1.05, 0, 0), (1.05, 0, 3.1), 0.03, 5)))
    return parts


def tree(kind='A'):
    if kind == 'EX':
        h, crowns = 7.0, [((0, 0, 5.0), 2.4), ((1.0, 0.6, 4.2), 1.5), ((-0.9, -0.4, 4.5), 1.3)]
    elif kind == 'B':
        h, crowns = 6.0, [((0, 0, 4.4), 1.8), ((0.7, -0.5, 3.6), 1.1)]
    else:
        h, crowns = 5.0, [((0, 0, 3.6), 1.7), ((0.8, 0.5, 3.0), 1.0), ((-0.7, 0.3, 3.1), 0.9)]
    parts = [('15_VEGETATION_FULL', mk.cylinder((0, 0, 0), (0, 0, h * 0.55), 0.14, 7))]
    for adeg in (30, 160, 270):
        a = math.radians(adeg)
        parts.append(('15_VEGETATION_FULL', mk.cylinder((0, 0, h * 0.5), (0.9 * math.cos(a), 0.9 * math.sin(a), h * 0.66), 0.05, 5)))
    for (c, r) in crowns:
        parts.append(('15_VEGETATION_FULL', mk.sphere(c, r, 9, 7)))
    return parts


def tropical():
    parts = []
    for k in range(6):
        a = 2 * math.pi * k / 6 + 0.3
        tip = (1.1 * math.cos(a), 1.1 * math.sin(a), 0.9 + 0.25 * (k % 2))
        parts.append(('15_VEGETATION_FULL', mk.cylinder((0, 0, 0.15), tip, 0.03, 4)))
        parts.append(('15_VEGETATION_FULL', mk.sphere(tip, 0.3, 5, 4)))
    return parts


def shrub():
    return [('15_VEGETATION_FULL', mk.sphere((0, 0, 0.4), 0.45, 7, 5)),
            ('15_VEGETATION_FULL', mk.sphere((0.4, 0.2, 0.3), 0.3, 6, 4))]


def aquatic():
    parts = []
    for k in range(5):
        a = 2 * math.pi * k / 5
        parts.append(('15_VEGETATION_FULL', mk.cylinder((0.15 * math.cos(a), 0.15 * math.sin(a), 0),
                                                        (0.3 * math.cos(a), 0.3 * math.sin(a), 0.75), 0.02, 4)))
    return parts


def climber():
    pts = []
    for t in range(26):
        f = t / 25
        a = f * 4.6
        pts.append((0.2 * math.cos(a), 0.2 * math.sin(a), f * 3.0))
    parts = [('15_VEGETATION_FULL', mk.tube(pts, 0.05, 5))]
    for t in range(4, 26, 6):
        parts.append(('15_VEGETATION_FULL', mk.sphere((pts[t][0] * 1.6, pts[t][1] * 1.6, pts[t][2]), 0.22, 5, 4)))
    return parts


# ============================ BIBLIOTECA VEGETAL E02 (roles) ============================
def _lobed_crown(cz, r, lobes, squash=0.85):
    parts = []
    parts.append(('15_VEGETATION_FULL', mk.sphere((0, 0, cz), r, 10, 8)))
    for k in range(lobes):
        a = 2 * math.pi * k / lobes + 0.4
        rr = r * rng.uniform(0.45, 0.62)
        parts.append(('15_VEGETATION_FULL', mk.sphere((r * 0.72 * math.cos(a), r * 0.72 * math.sin(a),
                                                       cz + rng.uniform(-0.3, 0.5) * r * squash), rr, 8, 6)))
    return parts


def veg2_arbol(kind='A'):
    """ARBOL DE SOMBRA: copa multilobulada, tronco con 3 ramas."""
    h = dict(A=5.2, B=6.2, EX=7.2)[kind]
    r = dict(A=2.1, B=1.9, EX=2.7)[kind]
    parts = [('15_VEGETATION_FULL', mk.cylinder((0, 0, 0), (0, 0, h * 0.52), 0.15, 8))]
    for adeg in (25, 145, 265):
        a = math.radians(adeg)
        parts.append(('15_VEGETATION_FULL', mk.cylinder((0, 0, h * 0.45),
                                                        (1.1 * math.cos(a), 1.1 * math.sin(a), h * 0.62), 0.06, 5)))
    parts += _lobed_crown(h * 0.62 + r * 0.5, r, 5)
    return parts


def veg2_trepadora():
    """TREPADORA en mastil: helice + matas + derrame en el brazo."""
    pts = []
    for t in range(30):
        f = t / 29
        a = f * 5.2
        pts.append((0.19 * math.cos(a), 0.19 * math.sin(a), f * 3.0))
    parts = [('15_VEGETATION_FULL', mk.tube(pts, 0.045, 5))]
    for t in range(3, 30, 5):
        parts.append(('15_VEGETATION_FULL', mk.sphere((pts[t][0] * 2.2, pts[t][1] * 2.2, pts[t][2]),
                                                      rng.uniform(0.18, 0.3), 6, 4)))
    for k in range(4):   # derrame superior
        a = 0.5 + k * 0.5
        parts.append(('15_VEGETATION_FULL', mk.sphere((1.0 + 0.45 * k * math.cos(a), 0.45 * k * math.sin(a),
                                                       3.1 + 0.35 * math.sin(k * 2.0)), 0.22, 5, 4)))
    return parts


def veg2_baja():
    """VEGETACION BAJA DE ESTANCIA: matas redondas + gramineas."""
    parts = []
    for (dx, dy, r) in ((0, 0, 0.42), (0.5, 0.25, 0.3), (-0.4, 0.3, 0.26)):
        parts.append(('15_VEGETATION_FULL', mk.sphere((dx, dy, r * 0.8), r, 7, 5)))
    for k in range(6):
        a = 2 * math.pi * k / 6 + 0.2
        x0, y0 = 0.55 * math.cos(a), 0.55 * math.sin(a)
        V = [(x0, y0, 0), (x0 + 0.05, y0, 0), (x0 + 0.02, y0 + 0.02, rng.uniform(0.55, 0.85))]
        parts.append(('15_VEGETATION_FULL', (V, [(0, 1, 2)])))
    return parts


def veg2_tropical():
    """TROPICAL HUMEDA (alocasia): palas grandes inclinadas."""
    parts = [('15_VEGETATION_FULL', mk.sphere((0, 0, 0.25), 0.28, 6, 5))]
    for k in range(7):
        a = 2 * math.pi * k / 7 + 0.3
        L = rng.uniform(0.9, 1.35)
        tip = (L * math.cos(a), L * math.sin(a), 0.7 + 0.45 * (k % 3))
        parts.append(('15_VEGETATION_FULL', mk.cylinder((0, 0, 0.15), tip, 0.035, 4)))
        # pala: elipsoide aplastado orientado
        V, F = mk.sphere((0, 0, 0), 1.0, 8, 6)
        ca, sa = math.cos(a), math.sin(a)
        V2 = []
        for (x, y, z) in V:
            xs, ys, zs = x * 0.52, y * 0.30, z * 0.10   # pala plana
            xr = xs * ca - ys * sa
            yr = xs * sa + ys * ca
            V2.append((tip[0] + xr + 0.3 * ca, tip[1] + yr + 0.3 * sa, tip[2] + zs + 0.12))
        parts.append(('15_VEGETATION_FULL', (V2, F)))
    return parts


def veg2_huerto():
    """FILA DE HUERTO 2.6 m: bancal + matas + tutores + linea de goteo."""
    parts = [('09_PLANTERS', mk.box((0, 0, 0), 2.6, 0.7, 0.26))]
    for k in range(5):
        x0 = -1.05 + k * 0.525
        parts.append(('15_VEGETATION_FULL', mk.sphere((x0, 0, 0.45), rng.uniform(0.2, 0.3), 6, 5)))
    for k in range(3):
        x0 = -0.8 + k * 0.8
        parts.append(('10_FURNITURE', mk.cylinder((x0, 0.12, 0.26), (x0, 0.05, 1.7), 0.02, 4)))
    parts.append(('13_PIPES', mk.tube([(-1.3, -0.2, 0.3), (0, -0.22, 0.3), (1.3, -0.2, 0.3)], 0.03, 5)))
    return parts


def veg2_acuatica():
    """ACUATICA: carrizos + nenufares flotantes."""
    parts = []
    for k in range(6):
        a = 2 * math.pi * k / 6
        x0, y0 = 0.22 * math.cos(a), 0.22 * math.sin(a)
        parts.append(('15_VEGETATION_FULL', mk.cylinder((x0, y0, 0), (x0 * 1.6, y0 * 1.6, rng.uniform(0.7, 1.05)), 0.022, 4)))
    for (dx, dy) in ((0.55, 0.1), (-0.4, 0.45), (0.15, -0.5)):
        parts.append(('15_VEGETATION_FULL', mk.cylinder((dx, dy, 0.0), (dx, dy, 0.015), 0.24, 8)))
    return parts


def veg2_colgante():
    """COLGANTE: 4 guias descolgandose (para aros de loop y borde de cinta)."""
    parts = []
    for k in range(4):
        a = 2 * math.pi * k / 4 + 0.4
        x0, y0 = 0.25 * math.cos(a), 0.25 * math.sin(a)
        Lc = rng.uniform(1.3, 2.3)
        nb = 6
        for j in range(nb):
            f = j / (nb - 1)
            parts.append(('15_VEGETATION_FULL', mk.sphere((x0 + 0.12 * math.sin(f * 5 + k), y0 + 0.1 * math.cos(f * 4),
                                                           -f * Lc), 0.14 * (1 - 0.3 * f) + 0.05, 5, 4)))
    return parts


def person():
    return [('16_PEOPLE_PROXY', mk.merge([mk.cylinder((0, 0, 0), (0, 0, 1.45), 0.22, 8),
                                          mk.sphere((0, 0, 1.58), 0.12, 6, 4)]))]


def neb_post():
    return [('13_PIPES', mk.cylinder((0, 0, 0), (0, 0, H['MIST']), 0.045, 6)),
            ('13_PIPES', mk.sphere((0, 0, H['MIST']), 0.12, 6, 4)),
            ('12_MIST', mk.sphere((0, 0, H['MIST'] - 0.5), 0.55, 6, 4))]


def totem():
    return [('10_FURNITURE', mk.box((0, 0, 0), 0.45, 0.14, 1.35)),
            ('13_PIPES', mk.sphere((0, 0.0, 1.42), 0.06, 5, 4))]


BLOCKS = {
    'LEAF_S1': leaf_canopy(1.5, 1.5, 8), 'LEAF_S2': leaf_canopy(1.8, 1.8, 9),
    'LEAF_M1': leaf_canopy(2.3, 2.3, 10), 'LEAF_M2': leaf_canopy(2.6, 2.6, 10),
    'LEAF_MT': leaf_canopy(2.4, 2.4, 10, tilt=4), 'LEAF_OV': leaf_canopy(2.9, 2.1, 10),
    'LEAF_L1': leaf_canopy(3.2, 3.2, 12), 'LEAF_LT': leaf_canopy(3.4, 3.4, 12, tilt=3),
    'LEAF_XL': leaf_canopy(4.2, 4.2, 12),
    'MAST_1': mast(1, 5.4), 'MAST_2': mast(2, 5.8), 'MAST_3': mast(3, 6.4),
    'POD_S': pink_pod(2.25), 'POD_M': pink_pod(3.25, door=True), 'POD_L': pink_pod(4.5, door=True),
    'POD_TRAIN': pod_train(), 'DROP_TANK': drop_tank(), 'NURSERY': nursery(),
    'TREE_A': tree('A'), 'TREE_B': tree('B'), 'TREE_EX': tree('EX'),
    'TROPICAL': tropical(), 'SHRUB': shrub(), 'AQUATIC': aquatic(), 'CLIMBER': climber(),
    'PERSON': person(), 'NEB_POST': neb_post(), 'TOTEM': totem(),
    # E02 — biblioteca vegetal por roles
    'VEG2_ARBOL_A': veg2_arbol('A'), 'VEG2_ARBOL_B': veg2_arbol('B'), 'VEG2_ARBOL_EX': veg2_arbol('EX'),
    'VEG2_TREPADORA': veg2_trepadora(), 'VEG2_BAJA': veg2_baja(), 'VEG2_TROPICAL': veg2_tropical(),
    'VEG2_HUERTO': veg2_huerto(), 'VEG2_ACUATICA': veg2_acuatica(), 'VEG2_COLGANTE': veg2_colgante(),
}


# ============================================================ ARCHIVOS
def new_file():
    f = r3.File3dm()
    f.Settings.ModelUnitSystem = r3.UnitSystem.Meters
    lidx = {}
    for name, col, _ in LAYERS:
        lay = r3.Layer(); lay.Name = name; lay.Color = col
        lidx[name] = f.Layers.Add(lay)
    return f, lidx


def register_blocks(f, lidx, names):
    ids = {}
    for name in names:
        geoms, atts = [], []
        for (layer, (V, F)) in BLOCKS[name]:
            if not F:
                continue
            mm = r3.Mesh()
            for v in V:
                mm.Vertices.Add(*v)
            for fc in F:
                mm.Faces.AddFace(*fc)
            a = r3.ObjectAttributes(); a.LayerIndex = lidx[layer]; a.Name = name
            geoms.append(mm); atts.append(a)
        gid = f.InstanceDefinitions.Add(name, 'familia 03B', '', '', r3.Point3d(0, 0, 0), tuple(geoms), tuple(atts))
        ids[name] = f.InstanceDefinitions.FindIndex(gid).Id
    return ids


class Scene:
    """acumula geometria para el visor (bloques horneados con transformacion)."""

    def __init__(self):
        self.meshes = []
        self.lines = []

    def inst(self, name, x, y, z, rot=0.0):
        ca, sa = math.cos(rot), math.sin(rot)
        for pi, (layer, (V, F)) in enumerate(BLOCKS[name]):
            if not F:
                continue
            Vt = [(round(vx * ca - vy * sa + x, 3), round(vx * sa + vy * ca + y, 3), round(vz + z, 3)) for (vx, vy, vz) in V]
            self.meshes.append(dict(layer=layer, color=list(LCOL[layer][:3]), opacity=LOP[layer],
                                    fam=name, part=pi, V=Vt, F=F))

    def mesh(self, layer, VF, fam=''):
        V, F = VF
        if F:
            self.meshes.append(dict(layer=layer, color=list(LCOL[layer][:3]), opacity=LOP[layer], fam=fam,
                                    V=[[round(a, 3) for a in v] for v in V], F=F))

    def line(self, layer, pts):
        self.lines.append(dict(layer=layer, color=list(LCOL[layer][:3]),
                               pts=[[round(a, 3) for a in p] for p in pts]))


def add_mesh(f, lidx, layer, name, VF):
    V, F = VF
    if not F:
        return
    mm = r3.Mesh()
    for v in V:
        mm.Vertices.Add(*v)
    for fc in F:
        mm.Faces.AddFace(*fc)
    a = r3.ObjectAttributes(); a.LayerIndex = lidx[layer]; a.Name = name
    f.Objects.AddMesh(mm, a)


def add_curve(f, lidx, layer, name, pts):
    pl = r3.Polyline()
    for p in pts:
        pl.Add(p[0], p[1], p[2] if len(p) > 2 else 0)
    a = r3.ObjectAttributes(); a.LayerIndex = lidx[layer]; a.Name = name
    f.Objects.AddCurve(pl.ToPolylineCurve(), a)


def place(f, ids, name, x, y, z, rot=0.0, lidx=None):
    tr = r3.Transform.Translation(x, y, z)
    if rot:
        tr = r3.Transform.Multiply(tr, r3.Transform.Rotation(rot, r3.Vector3d(0, 0, 1), r3.Point3d(0, 0, 0)))
    ir = r3.InstanceReference(ids[name], tr)
    a = r3.ObjectAttributes(); a.Name = name
    f.Objects.AddInstanceObject(ir, a)


# ============================================================ MONTAJE DE SITIO
def build_site(f, lidx, ids, sc, full=False):
    """Monta el sitio en el File3dm f y en la escena sc."""
    cc = m['contexto']['casa_correos']
    add_mesh(f, lidx, '00_CONTEXT', 'CTX_CORREOS', mk.strip([(p[0], p[1]) for p in cc['pts']], 0.4, 0, 17))
    sc.mesh('00_CONTEXT', mk.strip([(p[0], p[1]) for p in cc['pts']], 0.4, 0, 17))
    for nm, VF in [('CTX_TORRE', mk.box((-25.2, -37.5, 17), 7.5, 6.5, 12)),
                   ('CTX_RELOJ', mk.cylinder((-25.2, -34.35, 26.5), (-25.2, -34.05, 26.5), 1.6, 16)),
                   ('CTX_CUPULIN', mk.sphere((-25.2, -37.5, 29.0), 2.2, 10, 6))]:
        add_mesh(f, lidx, '00_CONTEXT', nm, VF)
        sc.mesh('00_CONTEXT', VF)
    nb = 0
    for b in m['contexto']['buildings']:
        if b['name'] == cc['name'] or len(b['pts']) < 4:
            continue
        xs = [p[0] for p in b['pts']]; ys = [p[1] for p in b['pts']]
        if max(xs) < -130 or min(xs) > 150 or max(ys) < -100 or min(ys) > 110:
            continue
        VF = mk.strip([(p[0], p[1]) for p in b['pts']], 0.3, 0, 14)
        add_mesh(f, lidx, '00_CONTEXT', 'CTX_%03d' % nb, VF)
        sc.mesh('00_CONTEXT', VF)
        nb += 1
    g = mk.box((0, 5, -0.12), 320, 220, 0.12)
    add_mesh(f, lidx, '01_GROUND', 'GROUND', g)
    sc.mesh('01_GROUND', g)

    # ---- estructura principal: loops (haz + traviesas + nudos) + curvas ----
    for lp in m['estructura_principal']['loops']:
        z = LOOP_Z[lp['id']]
        pts = [(p[0], p[1], z) for p in ell_pts(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'], 84)]
        add_curve(f, lidx, '30_CURVES', 'AXIS_%s' % lp['id'], pts)
        main = mk.tube(pts, 0.30, 12)
        add_mesh(f, lidx, '02_PRIMARY_STRUCTURE', 'PRIMARY_%s' % lp['id'], main)
        sc.mesh('02_PRIMARY_STRUCTURE', main)
        for off in (0.75, -0.75):
            pts2 = [(p[0], p[1], z - 0.35) for p in ell_pts(lp['cx'], lp['cy'], lp['rx'] + off, lp['ry'] + off, lp['rot'], 84)]
            sat = mk.tube(pts2, 0.10, 8)
            add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'SAT_%s' % lp['id'], sat)
            sc.mesh('03_SECONDARY_STRUCTURE', sat)
        per = 2 * math.pi * (lp['rx'] + lp['ry']) / 2
        ntr = max(10, int(per / 2.4))
        for k in range(ntr):
            adeg = 360 * k / ntr
            p0 = on_ell(lp['cx'], lp['cy'], lp['rx'] + 0.75, lp['ry'] + 0.75, lp['rot'], adeg)
            p1 = on_ell(lp['cx'], lp['cy'], lp['rx'] - 0.75, lp['ry'] - 0.75, lp['rot'], adeg)
            trv = mk.cylinder((p0[0], p0[1], z - 0.35), (p1[0], p1[1], z - 0.35), 0.05, 5)
            add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'TRV', trv)
            sc.mesh('03_SECONDARY_STRUCTURE', trv)
        for k in range(0, ntr, 3):
            adeg = 360 * k / ntr
            p0 = on_ell(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'], adeg)
            nd = mk.sphere((p0[0], p0[1], z), 0.22, 6, 5)
            add_mesh(f, lidx, '02_PRIMARY_STRUCTURE', 'NODE', nd)
            sc.mesh('02_PRIMARY_STRUCTURE', nd)

    # ---- cupula-pergola v002 (D03B-04) ----
    dm = m['estructura_principal']['dome']
    R = dm['r']; z0 = dm['base_z']; z1 = dm['apex_z']; ocu = dm['oculus_r']
    V, F = [], []
    nu, nv = 20, 8
    for j in range(nv + 1):
        fz = j / nv
        zz = z0 + (z1 - z0) * fz
        rr = R * math.cos(fz * 1.35) if fz < 1 else ocu
        rr = max(rr, ocu)
        for i in range(nu):
            a = 2 * math.pi * i / nu
            V.append((dm['cx'] + rr * math.cos(a), dm['cy'] + rr * math.sin(a), zz))
    for j in range(nv):
        for i in range(nu):
            i2 = (i + 1) % nu
            a = j * nu + i; b = j * nu + i2; c = (j + 1) * nu + i2; d = (j + 1) * nu + i
            F.append((a, b, c)); F.append((a, c, d))
    add_mesh(f, lidx, '06_MEMBRANES', 'DOME_SHELL', (V, F))
    sc.mesh('06_MEMBRANES', (V, F))
    ring = [(p[0], p[1], z0) for p in ell_pts(dm['cx'], dm['cy'], R, R, 0, 32)]
    rb = mk.tube(ring, 0.14, 8)
    add_mesh(f, lidx, '02_PRIMARY_STRUCTURE', 'DOME_RING', rb)
    sc.mesh('02_PRIMARY_STRUCTURE', rb)
    add_curve(f, lidx, '30_CURVES', 'DOME_RING_AXIS', ring)
    for k in range(dm['n_supports']):
        a = 2 * math.pi * k / dm['n_supports']
        px, py = dm['cx'] + R * 0.96 * math.cos(a), dm['cy'] + R * 0.96 * math.sin(a)
        sp = mk.cylinder((px, py, 0), (px, py, z0), 0.14, 7)
        add_mesh(f, lidx, '04_MASTS', 'DOME_SUP', sp)
        sc.mesh('04_MASTS', sp)

    # ---- cinta ----
    rib = m['circulacion']['ribbon']
    add_curve(f, lidx, '30_CURVES', 'RIBBON_AXIS', [(p[0], p[1], H['RIBBON']) for p in rib])
    deck = mk.strip([(p[0], p[1]) for p in rib], 2.5, H['RIBBON'] - 0.22, H['RIBBON'])
    add_mesh(f, lidx, '02_PRIMARY_STRUCTURE', 'RIBBON_DECK', deck)
    sc.mesh('02_PRIMARY_STRUCTURE', deck)
    n = len(rib)
    for off in (1.2, -1.2):
        side = []
        for i, p in enumerate(rib):
            a0 = rib[max(i - 1, 0)]; b0 = rib[min(i + 1, n - 1)]
            dx, dy = b0[0] - a0[0], b0[1] - a0[1]
            L = math.hypot(dx, dy) or 1e-9
            side.append((p[0] - dy / L * off, p[1] + dx / L * off))
        rail = mk.tube([(q[0], q[1], H['RIBBON'] + 1.05) for q in side], 0.045, 6)
        add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'RIBBON_RAIL', rail)
        sc.mesh('03_SECONDARY_STRUCTURE', rail)
        for q in side[::2]:
            bp = mk.cylinder((q[0], q[1], H['RIBBON']), (q[0], q[1], H['RIBBON'] + 1.05), 0.028, 5)
            add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'BALPOST', bp)
            sc.mesh('03_SECONDARY_STRUCTURE', bp)
    CORR = [c['pts'] for c in m['circulacion']['corridors']]

    def near_corr(x, y, dmin=2.2):
        for pts in CORR:
            for i in range(len(pts) - 1):
                ax, ay = pts[i]; bx, by = pts[i + 1]
                vx, vy = bx - ax, by - ay
                L2 = vx * vx + vy * vy or 1e-9
                t = max(0, min(1, ((x - ax) * vx + (y - ay) * vy) / L2))
                if math.hypot(x - (ax + vx * t), y - (ay + vy * t)) < dmin:
                    return True
        return False

    acc = 0.0
    for i in range(1, n):
        acc += math.hypot(rib[i][0] - rib[i - 1][0], rib[i][1] - rib[i - 1][1])
        if acc > 12 and not near_corr(*rib[i]):
            sup = mk.cylinder((rib[i][0], rib[i][1], 0), (rib[i][0], rib[i][1], H['RIBBON'] - 0.22), 0.17, 8)
            cap = mk.cylinder((rib[i][0], rib[i][1], H['RIBBON'] - 0.8), (rib[i][0], rib[i][1], H['RIBBON'] - 0.22), 0.3, 8)
            add_mesh(f, lidx, '02_PRIMARY_STRUCTURE', 'RIB_SUP', sup)
            add_mesh(f, lidx, '02_PRIMARY_STRUCTURE', 'RIB_CAP', cap)
            sc.mesh('02_PRIMARY_STRUCTURE', sup); sc.mesh('02_PRIMARY_STRUCTURE', cap)
            acc = 0.0
    for (sx, sy) in m['circulacion']['stairs']:
        top = H['RIBBON'] - 0.22
        run = top * 1.1
        for dy0 in (0, 1.2):
            st = mk.cylinder((sx - run / 2, sy + dy0, 0), (sx + run / 2, sy + dy0, top), 0.09, 6)
            add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'STRINGER', st)
            sc.mesh('03_SECONDARY_STRUCTURE', st)
        for k in range(16):
            t = k / 15
            stp = mk.box((sx - run / 2 + run * t, sy + 0.6, top * t), 0.32, 1.28, 0.05)
            add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'STEP', stp)
            sc.mesh('03_SECONDARY_STRUCTURE', stp)

    # ---- redes tensadas ----
    for lpi, a0, a1 in [(0, 150, 260), (3, -30, 80), (6, 120, 230)]:
        lp = m['estructura_principal']['loops'][lpi]
        z = LOOP_Z[lp['id']]
        nn = 12
        outer = [on_ell(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'], a0 + (a1 - a0) * i / nn) for i in range(nn + 1)]
        inner = [on_ell(lp['cx'], lp['cy'], lp['rx'] * 0.45, lp['ry'] * 0.45, lp['rot'], a0 + (a1 - a0) * i / nn) for i in range(nn + 1)]
        for i in range(nn + 1):
            sc.line('05_CABLES', [(outer[i][0], outer[i][1], z - 0.4), (inner[i][0], inner[i][1], z - 2.2)])
            add_curve(f, lidx, '05_CABLES', 'NET', [(outer[i][0], outer[i][1], z - 0.4), (inner[i][0], inner[i][1], z - 2.2)])
        V, Fq = [], []
        for i in range(nn + 1):
            V.append((outer[i][0], outer[i][1], z - 0.4)); V.append((inner[i][0], inner[i][1], z - 2.2))
        for i in range(nn):
            a = 2 * i
            Fq.append((a, a + 2, a + 3)); Fq.append((a, a + 3, a + 1))
        add_mesh(f, lidx, '06_MEMBRANES', 'NET_%s' % lp['id'], (V, Fq))
        sc.mesh('06_MEMBRANES', (V, Fq))

    # ---- canopies como bloques + mastiles + cables ----
    DISCS = m['paisaje']['discs']
    variants_c = ['LEAF_S1', 'LEAF_S2', 'LEAF_M1', 'LEAF_M2', 'LEAF_MT', 'LEAF_OV', 'LEAF_L1', 'LEAF_LT', 'LEAF_XL']
    for i, d in enumerate(DISCS):
        r = d['r']
        cota = min(max(d.get('cota', 6.0), 4.2), H['HIGH'])
        if r < 1.7:
            nm = ('LEAF_S1', 'LEAF_S2')[i % 2]
        elif r < 2.45:
            nm = ('LEAF_M1', 'LEAF_M2', 'LEAF_MT', 'LEAF_OV')[i % 4]
        elif r < 3.4:
            nm = ('LEAF_L1', 'LEAF_LT')[i % 2]
        else:
            nm = 'LEAF_XL'
        rot = (i * 0.7) % (2 * math.pi)
        place(f, ids, nm, d['cx'], d['cy'], cota, rot)
        sc.inst(nm, d['cx'], d['cy'], cota, rot)
    MASTS = m['estructura_ligera']['masts']
    for i, (mx, my) in enumerate(MASTS):
        nd = sorted(DISCS, key=lambda dd: (dd['cx'] - mx) ** 2 + (dd['cy'] - my) ** 2)[:2]
        nd = [dd for dd in nd if (dd['cx'] - mx) ** 2 + (dd['cy'] - my) ** 2 < 22]
        nm = ('MAST_1', 'MAST_2', 'MAST_3')[min(len(nd), 2)]
        rot = math.atan2(nd[0]['cy'] - my, nd[0]['cx'] - mx) - 0.5 if nd else (i * 0.9) % 6.28
        place(f, ids, nm, mx, my, 0, rot)
        sc.inst(nm, mx, my, 0, rot)
        for dd in nd:
            cota = min(max(dd.get('cota', 6.0), 4.2), H['HIGH'])
            sc.line('05_CABLES', [(mx, my, H['BRANCH']), (dd['cx'], dd['cy'], cota)])
            add_curve(f, lidx, '05_CABLES', 'CBL', [(mx, my, H['BRANCH']), (dd['cx'], dd['cy'], cota)])
    for lp in m['estructura_principal']['loops']:
        z = LOOP_Z[lp['id']]
        for adeg in range(0, 360, 30):
            px, py = on_ell(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'], adeg)
            nd = sorted(DISCS, key=lambda dd: (dd['cx'] - px) ** 2 + (dd['cy'] - py) ** 2)[:1]
            if nd and (nd[0]['cx'] - px) ** 2 + (nd[0]['cy'] - py) ** 2 < 42:
                dd = nd[0]
                cota = min(max(dd.get('cota', 6.0), 4.2), H['HIGH'])
                sc.line('05_CABLES', [(px, py, z), (dd['cx'], dd['cy'], cota)])
                add_curve(f, lidx, '05_CABLES', 'LCBL', [(px, py, z), (dd['cx'], dd['cy'], cota)])

    # ---- capsulas ----
    for i, c in enumerate(m['programa']['capsules']):
        cid = c.get('id', '')
        rot = math.radians(-c.get('rot', 0))
        if cid in ('T-O', 'T-SE'):
            place(f, ids, 'POD_TRAIN', c['cx'], c['cy'], 0, rot)
            sc.inst('POD_TRAIN', c['cx'], c['cy'], 0, rot)
        else:
            dia = max(c['w'], 1.8)
            nm = 'POD_S' if dia < 2.7 else ('POD_M' if dia < 3.9 else 'POD_L')
            if cid == 'R-N' and i % 3 == 0:
                zc = 4.5 - (dia / 2 + 0.3)
                place(f, ids, nm, c['cx'], c['cy'], zc, rot)
                sc.inst(nm, c['cx'], c['cy'], zc, rot)
                sc.line('05_CABLES', [(c['cx'], c['cy'], zc + dia + 0.5), (c['cx'] + 1.5, c['cy'] - 1.5, 9.0)])
            else:
                place(f, ids, nm, c['cx'], c['cy'], 0, rot)
                sc.inst(nm, c['cx'], c['cy'], 0, rot)
    lab = m['programa']['lab']
    labw = mk.strip([(p[0], p[1]) for p in lab['pts']], 0.12, 0, 3.5)
    add_mesh(f, lidx, '08_PINK_MODULES', 'LAB02', labw)
    sc.mesh('08_PINK_MODULES', labw)
    labr = mk.tube([(p[0], p[1], 3.55) for p in lab['pts']], 0.08, 6)
    add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'LAB_RING', labr)
    sc.mesh('03_SECONDARY_STRUCTURE', labr)

    # ---- agua ----
    for p in m['agua_clima']['pools']:
        pts = ell_pts(p['cx'], p['cy'], p['rx'], p['ry'], p['rot'], 40)
        w = mk.surf(pts[:-1], p['cota'])
        rimt = mk.tube([(q[0], q[1], p['cota']) for q in pts], 0.12, 8)
        add_mesh(f, lidx, '11_WATER', 'BASIN_%s' % p['id'], w)
        add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'BASINRIM_%s' % p['id'], rimt)
        sc.mesh('11_WATER', w); sc.mesh('03_SECONDARY_STRUCTURE', rimt)
        add_curve(f, lidx, '30_CURVES', 'BASIN_AXIS_%s' % p['id'], [(q[0], q[1], p['cota']) for q in pts])
    for p in m['agua_clima']['ground_ponds']:
        if p['kind'] == 'circle':
            pts = ell_pts(p['cx'], p['cy'], p['r'], p['r'], 0, 32)
            cw = mk.strip([(q[0], q[1]) for q in pts], 0.28, 0, H['CURB'])
            wt = mk.surf(pts[:-1], H['CURB'] - 0.12)
            add_mesh(f, lidx, '09_PLANTERS', 'CURB_%s' % p['id'], cw)
            add_mesh(f, lidx, '11_WATER', 'POND_%s' % p['id'], wt)
            sc.mesh('09_PLANTERS', cw); sc.mesh('11_WATER', wt)
            if full:
                for k in range(3):
                    a = 2 * math.pi * k / 3 + 0.5
                    px_, py_ = p['cx'] + p['r'] * 0.55 * math.cos(a), p['cy'] + p['r'] * 0.55 * math.sin(a)
                    sc.inst('VEG2_ACUATICA', px_, py_, H['CURB'] - 0.12, k * 1.1)
                    place(f, ids, 'VEG2_ACUATICA', px_, py_, H['CURB'] - 0.12, k * 1.1)
        else:
            wt = mk.surf([(q[0], q[1]) for q in p['pts']], 0.45)
            add_mesh(f, lidx, '11_WATER', 'POND_%s' % p['id'], wt)
            sc.mesh('11_WATER', wt)
    sp = m['agua_clima']['splash']
    spl = mk.surf(ell_pts(sp['cx'], sp['cy'], sp['rx'], sp['ry'], sp['rot'], 32)[:-1], 0.03)
    add_mesh(f, lidx, '11_WATER', 'SPLASH', spl)
    sc.mesh('11_WATER', spl)
    for w in m['agua_clima']['mains']:
        pts3 = [(p[0], p[1], 0.32) for p in w]
        t = mk.tube(pts3, 0.16, 8)
        add_mesh(f, lidx, '13_PIPES', 'MAIN', t)
        sc.mesh('13_PIPES', t)
        add_curve(f, lidx, '30_CURVES', 'PIPE_AXIS', pts3)
    for (nx, ny) in m['agua_clima']['nebul']:
        place(f, ids, 'NEB_POST', nx, ny, 0)
        sc.inst('NEB_POST', nx, ny, 0)
    for t in m['estructura_ligera']['tanks']:
        for k in range(t['n']):
            cx = t['cx'] + k * 2.6
            pole = mk.cylinder((cx, t['cy'], 0), (cx, t['cy'], H['TANK'] - 1), 0.18, 8)
            toro = mk.torus((cx, t['cy'], H['TANK']), t['r'], 0.85, 18, 9)
            add_mesh(f, lidx, '04_MASTS', 'TKPOLE', pole)
            add_mesh(f, lidx, '08_PINK_MODULES', 'TANK', toro)
            sc.mesh('04_MASTS', pole); sc.mesh('08_PINK_MODULES', toro)
            sc.line('13_PIPES', [(cx, t['cy'], H['TANK']), (cx, t['cy'], 0.32)])
            add_curve(f, lidx, '13_PIPES', 'RISER', [(cx, t['cy'], H['TANK']), (cx, t['cy'], 0.32)])
    for (dx, dy) in m['estructura_ligera']['drops']:
        place(f, ids, 'DROP_TANK', dx, dy, 0)
        sc.inst('DROP_TANK', dx, dy, 0)

    # ---- mobiliario ----
    for i, b in enumerate(m['programa']['benches']):
        if len(b['pts']) < 3:
            continue
        s1 = mk.strip(b['pts'], 0.62, 0, H['SEAT'])
        add_mesh(f, lidx, '10_FURNITURE', 'BENCH_%d' % i, s1)
        sc.mesh('10_FURNITURE', s1)
    for i, p in enumerate(m['paisaje']['planters']):
        if len(p['pts']) < 3:
            continue
        s1 = mk.strip(p['pts'], 1.4, 0, H['PLANTER'])
        add_mesh(f, lidx, '09_PLANTERS', 'PLANTER_%d' % i, s1)
        sc.mesh('09_PLANTERS', s1)
        if full:
            for qi, q in enumerate(p['pts'][::4]):
                nmv = ('VEG2_TROPICAL', 'VEG2_BAJA')[qi % 2]
                place(f, ids, nmv, q[0], q[1], H['PLANTER'], qi * 0.8)
                sc.inst(nmv, q[0], q[1], H['PLANTER'], qi * 0.8)
    for k, (vx, vy) in enumerate([(64, 18), (67, 14), (61, 12)]):
        place(f, ids, 'NURSERY', vx, vy, 0, k * 0.9)
        sc.inst('NURSERY', vx, vy, 0, k * 0.9)
    for (tx, ty) in [(-70, -2), (-20, 24), (30, 22), (74, 4)]:
        place(f, ids, 'TOTEM', tx, ty, 0)
        sc.inst('TOTEM', tx, ty, 0)

    # ---- vegetacion / personas (solo full) ----
    if full:
        # E02: arboles de sombra multilobulados
        for i, (tx, ty) in enumerate(m['paisaje']['new_trees']):
            nmv = ('VEG2_ARBOL_A', 'VEG2_ARBOL_B')[i % 2]
            place(f, ids, nmv, tx, ty, 0, i * 0.8)
            sc.inst(nmv, tx, ty, 0, i * 0.8)
        for i, t in enumerate(m['contexto']['trees']):
            if -110 < t['x'] < 100 and -45 < t['y'] < 75:
                place(f, ids, 'VEG2_ARBOL_EX', t['x'], t['y'], 0, i * 0.6)
                sc.inst('VEG2_ARBOL_EX', t['x'], t['y'], 0, i * 0.6)
        # trepadoras en la mitad de los mastiles
        for i, (mx, my) in enumerate(MASTS):
            if i % 2 == 0:
                place(f, ids, 'VEG2_TREPADORA', mx, my, 0, i * 0.5)
                sc.inst('VEG2_TREPADORA', mx, my, 0, i * 0.5)
        # HUERTO en el interior de C1 (bajo las balsas elevadas, cf. 24D82F58)
        MXY = [(e['x'], e['y']) for e in m['contexto']['metro'] if -110 < e['x'] < 100 and -45 < e['y'] < 75]

        def near_metro_pt(x, y):
            return any(math.hypot(x - a, y - b) < 6.0 for (a, b) in MXY)

        hu = 0
        for gx in range(-62, -40, 4):
            for gy in range(0, 17, 5):
                px_, py_ = gx + (gy % 10) * 0.3, gy + (gx % 8) * 0.2
                if near_corr(px_, py_, 2.6) or near_metro_pt(px_, py_):
                    continue
                place(f, ids, 'VEG2_HUERTO', px_, py_, 0, 0.31)
                sc.inst('VEG2_HUERTO', px_, py_, 0, 0.31)
                hu += 1
        # TROPICALES bajo el nucleo denso de C2 y dentro de la cupula-pergola
        DISCS2 = m['paisaje']['discs']
        tr = 0
        for d in DISCS2:
            if tr >= 10:
                break
            if abs(d['cx'] - 8) < 16 and abs(d['cy'] - 13) < 14 and d.get('cota', 6) >= 6.2:
                if not near_corr(d['cx'], d['cy'], 2.4):
                    place(f, ids, 'VEG2_TROPICAL', d['cx'] + 0.8, d['cy'] - 0.5, 0, tr * 0.7)
                    sc.inst('VEG2_TROPICAL', d['cx'] + 0.8, d['cy'] - 0.5, 0, tr * 0.7)
                    tr += 1
        dm2 = m['estructura_principal']['dome']
        for k in range(3):
            a = 2 * math.pi * k / 3 + 0.8
            px_, py_ = dm2['cx'] + 3.1 * math.cos(a), dm2['cy'] + 3.1 * math.sin(a)
            if not near_corr(px_, py_, 2.2):
                place(f, ids, 'VEG2_TROPICAL', px_, py_, 0, k * 1.3)
                sc.inst('VEG2_TROPICAL', px_, py_, 0, k * 1.3)
        # VEGETACION BAJA junto a bancos (estancias)
        for b in m['programa']['benches']:
            for q in b['pts'][1::3]:
                place(f, ids, 'VEG2_BAJA', q[0] + 0.9, q[1] + 0.4, 0, q[0] * 0.1)
                sc.inst('VEG2_BAJA', q[0] + 0.9, q[1] + 0.4, 0, q[0] * 0.1)
        # COLGANTES bajo los aros de los loops grandes y el borde de la cinta
        for lp in m['estructura_principal']['loops']:
            if lp['id'] not in ('C1-L1', 'C2-L1', 'C3-L1'):
                continue
            z = LOOP_Z[lp['id']]
            for adeg in range(0, 360, 40):
                px_, py_ = on_ell(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'], adeg)
                place(f, ids, 'VEG2_COLGANTE', px_, py_, z - 0.45, adeg * 0.02)
                sc.inst('VEG2_COLGANTE', px_, py_, z - 0.45, adeg * 0.02)
        rib2 = m['circulacion']['ribbon']
        for i in range(6, len(rib2) - 6, 14):
            px_, py_ = rib2[i]
            place(f, ids, 'VEG2_COLGANTE', px_ + 1.1, py_, H['RIBBON'] - 0.3, i * 0.1)
            sc.inst('VEG2_COLGANTE', px_ + 1.1, py_, H['RIBBON'] - 0.3, i * 0.1)
        for (px, py) in [(-70, -8), (-44, -14), (-20, -16), (2, -16), (26, -18), (48, -16), (-2, 30), (14, 40),
                         (-36, 34), (60, 20), (-86, 2), (34, 4), (10, 4), (-14, 18), (72, -2), (-58, 22),
                         (20, 24), (-30, 6), (40, 8), (52, 26)]:
            place(f, ids, 'PERSON', px, py, 0)
            sc.inst('PERSON', px, py, 0)


# ============================================================ EJECUCION
ALL_BLOCKS = list(BLOCKS.keys())

if __name__ == '__main__':
    # 1) MASTER_ARCHITECTURE_v002 (sin vegetacion full ni personas)
    fM, lM = new_file()
    idsM = register_blocks(fM, lM, ALL_BLOCKS)
    scM = Scene()
    build_site(fM, lM, idsM, scM, full=False)
    okM = fM.Write(os.path.join(HERE, 'MASTER_ARCHITECTURE_v002.3dm'), 8)

    # 2) ASSET_LIBRARY_v001 (bloques + un ejemplar en malla)
    fA, lA = new_file()
    idsA = register_blocks(fA, lA, ALL_BLOCKS)
    for i, nm in enumerate(ALL_BLOCKS):
        x, y = (i % 7) * 8.0, (i // 7) * 8.0
        place(fA, idsA, nm, x, y, 0)
        dot = r3.TextDot(nm, r3.Point3d(x, y - 2.5, 0))
        a = r3.ObjectAttributes(); a.LayerIndex = lA['30_CURVES']
        fA.Objects.Add(dot, a)
    okA = fA.Write(os.path.join(HERE, 'ASSET_LIBRARY_v001.3dm'), 8)

    # 3) SOL_FULL_SCENE_v001 (todo)
    fF, lF = new_file()
    idsF = register_blocks(fF, lF, ALL_BLOCKS)
    scF = Scene()
    build_site(fF, lF, idsF, scF, full=True)
    okF = fF.Write(os.path.join(HERE, 'SOL_FULL_SCENE_v001.3dm'), 8)

    # 4) escena para visor
    os.makedirs(os.path.join(HERE, '_viewer'), exist_ok=True)
    with open(os.path.join(HERE, '_viewer', 'scene_full.js'), 'w', encoding='utf-8') as fp:
        fp.write('const SCENE_MESHES = ')
        json.dump(scF.meshes, fp, separators=(',', ':'))
        fp.write(';\nconst SCENE_LINES = ')
        json.dump(scF.lines, fp, separators=(',', ':'))
        fp.write(';\n')

    tris = sum(len(o['F']) for o in scF.meshes)
    print('MASTER:', okM, '· ASSETS:', okA, '· FULL:', okF)
    print('bloques:', len(ALL_BLOCKS), '· escena full: %d mallas, %d lineas, %d tris' % (len(scF.meshes), len(scF.lines), tris))
