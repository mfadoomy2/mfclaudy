# -*- coding: utf-8 -*-
"""
GEOMETRIA MAESTRA — REFUGIO CLIMATICO PUERTA DEL SOL · FASE 01
Fuente de verdad geometrica. 1 unidad = 1 metro. +X este, +Y norte. Origen: lat 40.41690, lon -3.70350.

Genera:
  - geometria_maestra.json  (todos los elementos, por familia, con clase de certeza G1-G4)
  - planta_maestra.svg      (master de trabajo por capas; el eje Y se invierte al emitir SVG)

Certeza:
  G1 confirmado en varias referencias · G2 muy probable · G3 inferido · G4 desconocido/reserva
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(3407)  # determinista

# ------------------------------------------------------------------ utilidades
def ell(cx, cy, rx, ry, rot_deg, n=72):
    """Puntos de una elipse rotada."""
    r = math.radians(rot_deg)
    pts = []
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        x, y = rx * math.cos(a), ry * math.sin(a)
        pts.append((round(cx + x * math.cos(r) - y * math.sin(r), 2),
                    round(cy + x * math.sin(r) + y * math.cos(r), 2)))
    return pts


def on_ell(cx, cy, rx, ry, rot_deg, a_deg):
    r = math.radians(rot_deg)
    a = math.radians(a_deg)
    x, y = rx * math.cos(a), ry * math.sin(a)
    return (cx + x * math.cos(r) - y * math.sin(r),
            cy + x * math.sin(r) + y * math.cos(r))


def catmull_rom(pts, seg=12):
    """Suaviza una polilinea (Catmull-Rom)."""
    if len(pts) < 3:
        return pts
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in [j / seg for j in range(seg)]:
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((round(x, 2), round(y, 2)))
    out.append(pts[-1])
    return out


def inside_ell(px, py, cx, cy, rx, ry, rot_deg, margin=0.0):
    r = math.radians(-rot_deg)
    dx, dy = px - cx, py - cy
    x = dx * math.cos(r) - dy * math.sin(r)
    y = dx * math.sin(r) + dy * math.cos(r)
    return (x / (rx - margin)) ** 2 + (y / (ry - margin)) ** 2 <= 1.0


# ------------------------------------------------------------------ CONTEXTO (OSM, G1)
ctx = json.load(open(os.path.join(HERE, 'contexto_sol.json'), encoding='utf-8'))
ctx2 = json.load(open(os.path.join(HERE, 'contexto_sol2.json'), encoding='utf-8'))

WIN = (-170, -130, 200, 140)  # x0 y0 x1 y1 ventana de trabajo


def in_win(x, y):
    return WIN[0] <= x <= WIN[2] and WIN[1] <= y <= WIN[3]


buildings = [b for b in ctx['buildings'] if any(in_win(*p) for p in b['pts'])]
highways = [h for h in ctx['highways'] if any(in_win(*p) for p in h['pts'])]
metro = [m for m in ctx['metro_entrances'] if in_win(m['x'], m['y'])]
trees_exist = [t for t in ctx2['trees'] if in_win(t['x'], t['y'])]
lamps = [l for l in ctx2['lamps'] if in_win(l['x'], l['y'])]

# hito clave
CASA_CORREOS = next(b for b in buildings if b['name'] == 'Presidencia de la Comunidad de Madrid')
RELOJ = (-25.23, -37.47)
KM0 = (-26.11, -30.16)
MARIBLANCA = (-89.94, -4.45)
CARLOS_III = (-28.0, -14.0)   # G2: posicion estimada frente a Casa de Correos (cenital 0F53E6F0)
OSO_MADRONO = (80.0, 22.0)    # G2: inicio de Alcala, frente norte

# ------------------------------------------------------------------ ESTRUCTURA PRINCIPAL (loops)
LOOPS = [
    dict(id='C1-L1', cx=-52, cy=10, rx=26, ry=20, rot=18, g='G1',
         nota='gran loop oval oeste (dibujo 00 / 0F53E6F0 / FE9A5E6E)'),
    dict(id='C1-L2', cx=-69, cy=-1, rx=11.5, ry=8.5, rot=-14, g='G2', nota='lazo menor SW'),
    dict(id='C1-L3', cx=-31, cy=30, rx=10, ry=7.5, rot=28, g='G2', nota='lazo menor NE'),
    dict(id='C2-L1', cx=8, cy=18, rx=21, ry=16.5, rot=-8, g='G1', nota='anillo exterior del nudo central'),
    dict(id='C2-L2', cx=8, cy=18, rx=14, ry=11, rot=-8, g='G1', nota='anillo interior (anillo doble)'),
    dict(id='C2-L3', cx=-15, cy=5, rx=9, ry=6.5, rot=16, g='G2', nota='lazo de enganche SW del nudo central'),
    dict(id='C3-L1', cx=56, cy=13, rx=17, ry=13, rot=10, g='G1', nota='loop este mayor'),
    dict(id='C3-L2', cx=70, cy=7, rx=11, ry=9, rot=-18, g='G2', nota='loop este solapado'),
]
DOME = dict(id='CUPULA', cx=30.5, cy=7, r=6.5, g='G2', nota='cupula geodesica del nudo central (F295448F/HR10)')

# ------------------------------------------------------------------ CIRCULACION: cinta-recorrido (G2)
RIBBON_CTRL = [
    (-81, -2), (-78, 12), (-68, 24), (-52, 32), (-38, 27), (-31, 14),
    (-38, 0), (-52, -6), (-66, 0), (-70, 12),               # bucle C1
    (-58, 26), (-40, 32), (-24, 30), (-12, 34), (2, 36),    # istmo N
    (16, 32), (26, 22), (24, 8), (12, 0), (-2, 2), (-10, 12), (-4, 24),  # bucle C2
    (10, 28), (24, 30), (36, 24), (40, 12), (36, 2),        # salida C2-E
    (46, -2), (58, -1), (68, 4), (74, 14), (66, 22),        # bucle C3 sur
    (54, 26), (44, 20), (48, 8), (60, 2), (72, 2), (82, 8),  # remate este
]
RIBBON = catmull_rom(RIBBON_CTRL, seg=10)

# escaleras/accesos a la cinta (G3)
STAIRS = [(-84, 0), (-38, 24), (4, 34), (26, 20), (44, -1), (80, 7)]

# pasos libres conservados (G1, logica urbana)
CORRIDORS = [
    dict(id='eje-mayor-alcala', pts=[(-95, -8), (-60, -10), (-20, -12), (20, -10), (60, -8), (88, 0)],
         nota='eje historico Mayor-Alcala frente a Casa de Correos: banda libre'),
    dict(id='preciados-carretas', pts=[(-33, 55), (-24, 30), (-10, 5), (2, -15), (7, -30)],
         nota='diagonal Preciados-Carretas'),
    dict(id='carmen-correos', pts=[(6, 64), (4, 40), (0, 10), (-8, -12)], nota='diagonal Carmen-eje'),
    dict(id='montera-espozymina', pts=[(40, 55), (38, 30), (30, -2), (24, -28)], nota='diagonal Montera-Espoz y Mina'),
    dict(id='arenal-alcala', pts=[(-93, 6), (-70, 30), (-30, 40), (10, 42), (48, 32), (85, 22)],
         nota='arco norte peatonal'),
]

# ------------------------------------------------------------------ PAISAJE: discos-canopy (G2 tipologia, G3 posicion)
def pack_discs(loop, radii, margin=1.2):
    """Coloca discos dentro de una elipse con espiral aurea determinista."""
    placed = []
    golden = math.pi * (3 - math.sqrt(5))
    n_try = 240
    ri = 0
    for k in range(n_try):
        if ri >= len(radii):
            break
        rad = radii[ri]
        t = (k + 0.5) / n_try
        rr = math.sqrt(t)
        a = k * golden
        px = loop['cx'] + rr * (loop['rx'] - rad - margin) * math.cos(a)
        py = loop['cy'] + rr * (loop['ry'] - rad - margin) * math.sin(a)
        if not inside_ell(px, py, loop['cx'], loop['cy'], loop['rx'], loop['ry'], loop['rot'], margin=rad * 0.5):
            continue
        ok = True
        for q in placed:
            d = math.hypot(px - q['cx'], py - q['cy'])
            if d < (rad + q['r']) * 0.82:   # ~18% de solape admisible (capas a distinta cota)
                ok = False
                break
        if ok:
            placed.append(dict(cx=round(px, 2), cy=round(py, 2), r=rad,
                               cota=round(5.0 + 5.0 * rng.random(), 1)))
            ri += 1
    return placed


DISCS = []
for lp, radii in [
    (LOOPS[0], [4.0, 3.2, 2.8, 2.6, 2.5, 2.4, 2.2, 2.1, 2.0, 1.9, 1.8, 1.7, 1.6, 3.6]),   # C1
    (LOOPS[3], [4.2, 3.6, 3.0, 2.8, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1, 2.0, 1.9, 1.8, 1.7, 1.6, 3.2, 2.9]),  # C2 ext
    (LOOPS[4], [3.0, 2.4, 2.0, 1.8]),                                     # C2 int
    (LOOPS[6], [3.8, 3.2, 2.8, 2.6, 2.3, 2.1, 2.0, 1.8, 1.7]),            # C3
    (LOOPS[7], [2.8, 2.2, 1.9, 1.7, 1.6]),
]:
    for dsc in pack_discs(lp, radii):
        dsc['loop'] = lp['id']
        DISCS.append(dsc)
# discos de orla exteriores (transicion) — a lo largo de arcos de los loops grandes
for lp, angs in [(LOOPS[0], [200, 225, 250, 155]), (LOOPS[3], [60, 90, 120]), (LOOPS[6], [300, 330, 30])]:
    for a in angs:
        px, py = on_ell(lp['cx'], lp['cy'], lp['rx'] + 4.5, lp['ry'] + 4.5, lp['rot'], a)
        DISCS.append(dict(cx=round(px, 2), cy=round(py, 2), r=1.8, cota=4.5, loop=lp['id'] + '-orla'))
# discos de istmo: cosen C1-C2 y C2-C3 (G3)
for (px, py, r) in [(-30, 14, 2.2), (-24, 9, 1.7), (-19, 16, 1.5), (-26, 20, 1.4),
                    (36, 15, 1.9), (41, 9, 1.6), (43, 18, 1.5), (33, 3, 1.6)]:
    DISCS.append(dict(cx=px, cy=py, r=r, cota=5.0, loop='istmo'))

# balsas de microalgas elevadas dentro de anillos (G2) — las grandes manchas verdes de las cenitales
POOLS = [
    dict(id='B-C1a', kind='oval', cx=-56, cy=14, rx=9.5, ry=5.5, rot=25, g='G2', cota=6.0),
    dict(id='B-C1b', kind='oval', cx=-45, cy=6, rx=6.5, ry=4.0, rot=-10, g='G2', cota=7.5),
    dict(id='B-C2a', kind='oval', cx=3, cy=21, rx=8.5, ry=5.0, rot=-8, g='G2', cota=6.5),
    dict(id='B-C2b', kind='oval', cx=14, cy=12, rx=6.0, ry=4.0, rot=20, g='G2', cota=8.0),
    dict(id='B-C3a', kind='oval', cx=54, cy=15, rx=10.0, ry=6.0, rot=12, g='G2', cota=6.0),
    dict(id='B-C3b', kind='oval', cx=68, cy=6, rx=7.0, ry=4.5, rot=-15, g='G2', cota=7.0),
]
# estanques en suelo (G2): circulares con murete + rinones
GROUND_PONDS = [
    dict(id='E-1', kind='circle', cx=-38, cy=18, r=3.5, g='G2'),
    dict(id='E-2', kind='circle', cx=-9, cy=26, r=3.0, g='G2'),
    dict(id='E-3', kind='circle', cx=20, cy=26, r=3.5, g='G2'),
    dict(id='E-4', kind='circle', cx=48, cy=6, r=3.0, g='G2'),
    dict(id='E-5', kind='kidney', pts=catmull_rom([(24, -2), (30, -4), (36, -2), (38, 2), (33, 3), (27, 2), (24, -2)], 8), g='G3'),
    dict(id='E-6', kind='kidney', pts=catmull_rom([(-30, 2), (-25, 0), (-21, 2), (-22, 5), (-27, 5.5), (-30, 2)], 8), g='G3'),
]
SPLASH = dict(id='splash', cx=17, cy=-3, rx=9, ry=5.5, rot=-5, g='G3',
              nota='lamina de agua jugable 1-2 cm (FBDF10B9/558C20E3); posicion inferida en el claro central')

# ------------------------------------------------------------------ PROGRAMA: capsulas rosas
def capsule_chain(loop, a0, a1, n, rr_off, size=(3.2, 2.0), cota='media'):
    out = []
    for i in range(n):
        a = a0 + (a1 - a0) * i / max(n - 1, 1)
        px, py = on_ell(loop['cx'], loop['cy'], loop['rx'] + rr_off, loop['ry'] + rr_off, loop['rot'], a)
        ang = math.degrees(math.atan2(
            on_ell(loop['cx'], loop['cy'], loop['rx'], loop['ry'], loop['rot'], a + 4)[1] - py,
            on_ell(loop['cx'], loop['cy'], loop['rx'], loop['ry'], loop['rot'], a + 4)[0] - px))
        out.append(dict(cx=round(px, 2), cy=round(py, 2), w=size[0], h=size[1],
                        rot=round(ang, 1), cota=cota))
    return out


CAPSULES = []
# tren oeste (G1: 0F53E6F0/HR01 borde occidental)
for c in capsule_chain(LOOPS[0], 120, 245, 12, 2.6, (3.4, 2.1), 'media'):
    c['id'] = 'T-O'; c['g'] = 'G1'; CAPSULES.append(c)
# arco U sureste (G1: 0F53E6F0/F295448F)
for c in capsule_chain(LOOPS[7], 150, 345, 13, 2.4, (3.2, 2.0), 'media'):
    c['id'] = 'T-SE'; c['g'] = 'G1'; CAPSULES.append(c)
# racimo norte C2 (G2)
for i, (dx, dy, r) in enumerate([(-3, 1, 1.9), (0.5, 2.5, 1.5), (3, 0, 2.1), (0, -2, 1.4), (5.5, 2, 1.6), (-5.5, -1, 1.3)]):
    CAPSULES.append(dict(id='R-N', g='G2', cx=16 + dx, cy=33 + dy, w=2 * r, h=2 * r, rot=0, cota='suelo'))
# racimo C1 interior (G2)
for i, (dx, dy, r) in enumerate([(0, 0, 1.7), (3, 1.5, 1.3), (-2.5, 2.5, 1.2), (1, -2.8, 1.5)]):
    CAPSULES.append(dict(id='R-C1', g='G2', cx=-64 + dx, cy=22 + dy, w=2 * r, h=2 * r, rot=0, cota='suelo'))
# racimo C3-NE viveros (G3)
for i, (dx, dy, r) in enumerate([(0, 0, 1.6), (3.2, 0.8, 1.3), (1.2, 2.8, 1.2)]):
    CAPSULES.append(dict(id='R-C3', g='G3', cx=66 + dx, cy=20 + dy, w=2 * r, h=2 * r, rot=0, cota='suelo'))

LAB = dict(id='LAB02', pts=catmull_rom([(42, 26), (48, 29), (55, 29.5), (60, 27), (58, 23.5), (51, 23), (45, 23.5), (42, 26)], 8),
           g='G3', nota='LAB 02 Microalgae Research (25A4B1BF); posicion en Sol inferida')

# salon urbano: bancos en arcos concentricos (G2 tipologia)
BENCHES = []
for rr, a0, a1 in [(8.5, 200, 300), (11, 205, 295), (13.5, 215, 285)]:
    arc = []
    for a in range(int(a0), int(a1) + 1, 6):
        arc.append(tuple(round(v, 2) for v in on_ell(8, 18, rr, rr * 0.8, -8, a)))
    BENCHES.append(dict(id='bancos-C2S', pts=arc, g='G2'))
for rr, a0, a1 in [(11, 95, 185), (13.5, 105, 175)]:
    arc = []
    for a in range(int(a0), int(a1) + 1, 6):
        arc.append(tuple(round(v, 2) for v in on_ell(-52, 10, rr, rr * 0.75, 18, a)))
    BENCHES.append(dict(id='bancos-C1', pts=arc, g='G2'))

# ------------------------------------------------------------------ ESTRUCTURA LIGERA
MASTS = []
for lp in [LOOPS[0], LOOPS[3], LOOPS[4], LOOPS[6], LOOPS[7]]:
    per = 2 * math.pi * math.sqrt((lp['rx'] ** 2 + lp['ry'] ** 2) / 2)
    n = max(8, int(per / 6.5))
    for i in range(n):
        a = 360 * i / n
        px, py = on_ell(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'], a)
        MASTS.append((round(px, 2), round(py, 2)))
for d in DISCS[::3]:
    MASTS.append((round(d['cx'] + 1.2, 2), round(d['cy'] - 1.0, 2)))

# depositos elevados (G3 posicion, G2 sistema)
TANKS = [
    dict(id='D-C1', cx=-72, cy=22, r=2.2, n=2, g='G3'),
    dict(id='D-C2', cx=7, cy=38, r=2.2, n=2, g='G3'),
    dict(id='D-C3', cx=77, cy=17, r=2.0, n=2, g='G3'),
]
# depositos-gota en suelo (G2 tipologia)
DROPS = [(-44, 22), (-42.5, 24), (-41, 26), (10, 8), (12, 6.5), (52, 20), (54, 21.5)]

# ------------------------------------------------------------------ AGUA: red principal rosa (G3)
WATER_MAINS = [
    catmull_rom([(-70, 24), (-62, 20), (-52, 22), (-44, 16), (-38, 10), (-30, 6)], 8),
    catmull_rom([(15, 36), (10, 30), (6, 24), (2, 18), (6, 10), (12, 4), (14, -2)], 8),
    catmull_rom([(76, 16), (70, 12), (62, 10), (54, 8), (48, 6)], 8),
    catmull_rom([(-30, 6), (-16, 4), (-2, 2), (12, 4)], 8),   # espina central en suelo
]
NEBUL = []
for lp in [LOOPS[0], LOOPS[3], LOOPS[6]]:
    n = 14
    for i in range(n):
        a = 360 * i / n
        px, py = on_ell(lp['cx'], lp['cy'], lp['rx'] * 0.82, lp['ry'] * 0.82, lp['rot'], a)
        NEBUL.append((round(px, 2), round(py, 2)))

# ------------------------------------------------------------------ PAISAJE suelo: jardineras + arboles nuevos
PLANTERS = []
for lp, offs in [(LOOPS[0], 3.0), (LOOPS[3], 3.2), (LOOPS[6], 3.0)]:
    for a0, a1 in [(15, 90), (140, 210), (250, 320)]:
        arc = []
        for a in range(a0, a1 + 1, 5):
            arc.append(tuple(round(v, 2) for v in on_ell(lp['cx'], lp['cy'], lp['rx'] + offs, lp['ry'] + offs, lp['rot'], a)))
        PLANTERS.append(dict(pts=arc, w=1.4, g='G3'))

NEW_TREES = []
for (tx, ty) in [(-78, 20), (-74, 28), (-60, 34), (-44, 34), (-20, 36), (-6, 40), (22, 36),
                 (34, 30), (46, 26), (64, 24), (76, 20), (-84, 8), (-30, -2), (-18, -6),
                 (34, -6), (44, -8), (58, -4), (30, 14), (-46, -8), (-58, -8)]:
    NEW_TREES.append((tx, ty))

# ------------------------------------------------------------------ DESPLAZAMIENTO GLOBAL DE LA INTERVENCION
# La intervencion baja 5 m hacia el sur para despejar el paseo del arco norte (cf. 0F53E6F0)
DY = -5.0


def _shift_pts(pts):
    return [(round(p[0], 2), round(p[1] + DY, 2)) for p in pts]


for lp in LOOPS:
    lp['cy'] = round(lp['cy'] + DY, 2)
DOME['cy'] = round(DOME['cy'] + DY, 2)
RIBBON = _shift_pts(RIBBON)
RIBBON_CTRL = _shift_pts(RIBBON_CTRL)
STAIRS = _shift_pts(STAIRS)
MASTS = _shift_pts(MASTS)
DROPS = _shift_pts(DROPS)
NEBUL = _shift_pts(NEBUL)
NEW_TREES = _shift_pts(NEW_TREES)
WATER_MAINS = [_shift_pts(w) for w in WATER_MAINS]
for coll in (DISCS,):
    for d in coll:
        d['cy'] = round(d['cy'] + DY, 2)
for p in POOLS:
    p['cy'] = round(p['cy'] + DY, 2)
for p in GROUND_PONDS:
    if p['kind'] == 'circle':
        p['cy'] = round(p['cy'] + DY, 2)
    else:
        p['pts'] = _shift_pts(p['pts'])
SPLASH['cy'] = round(SPLASH['cy'] + DY, 2)
for c in CAPSULES:
    c['cy'] = round(c['cy'] + DY, 2)
LAB['pts'] = _shift_pts(LAB['pts'])
for b in BENCHES:
    b['pts'] = _shift_pts(b['pts'])
for t in TANKS:
    t['cy'] = round(t['cy'] + DY, 2)
for pl in PLANTERS:
    pl['pts'] = _shift_pts(pl['pts'])

# certezas por familia donde no van elemento a elemento
for d in DISCS:
    d.setdefault('g', 'G3' if d['loop'] == 'istmo' else 'G2')

# ------------------------------------------------------------------ SALIDA JSON
model = dict(
    crs='1u=1m; origen lat 40.41690 lon -3.70350; +X este +Y norte',
    contexto=dict(
        buildings=buildings, highways=highways, metro=metro,
        trees=trees_exist, lamps=lamps,
        hitos=dict(reloj=RELOJ, km0=KM0, mariblanca=MARIBLANCA,
                   carlos_iii=CARLOS_III, oso_madrono=OSO_MADRONO),
        casa_correos=CASA_CORREOS,
    ),
    estructura_principal=dict(loops=LOOPS, dome=DOME),
    estructura_ligera=dict(masts=MASTS, tanks=TANKS, drops=DROPS),
    circulacion=dict(ribbon=RIBBON, ribbon_ctrl=RIBBON_CTRL, stairs=STAIRS, corridors=CORRIDORS),
    paisaje=dict(discs=DISCS, planters=PLANTERS, new_trees=NEW_TREES),
    programa=dict(capsules=CAPSULES, lab=LAB, benches=BENCHES),
    agua_clima=dict(pools=POOLS, ground_ponds=GROUND_PONDS, splash=SPLASH,
                    mains=WATER_MAINS, nebul=NEBUL),
    instalaciones=dict(nota='reserva Fase 02: bombeo, drenaje, electricidad, sensores',
                       bombeo_reserva=[(-70, 22), (15, 34), (76, 14)], g='G4'),
)
json.dump(model, open(os.path.join(HERE, 'geometria_maestra.json'), 'w', encoding='utf-8'), ensure_ascii=False)

# ------------------------------------------------------------------ SVG
def Y(y):
    return -y  # norte arriba


def path_of(pts, close=False):
    d = 'M ' + ' L '.join('%.2f %.2f' % (p[0], Y(p[1])) for p in pts)
    return d + (' Z' if close else '')


S = []
S.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-170 -140 370 270" font-family="Arial">')
S.append('<rect x="-170" y="-140" width="370" height="270" fill="#FFFFFF"/>')

# CONTEXTO
S.append('<g id="CONTEXTO">')
S.append('<g id="ctx-calles" stroke="#C9C7C2" stroke-width="0.3" fill="none">')
for h in highways:
    S.append('<path d="%s"/>' % path_of(h['pts']))
S.append('</g>')
S.append('<g id="ctx-edificios" fill="#EFEDE9" stroke="#B9B6B0" stroke-width="0.25">')
for b in buildings:
    if len(b['pts']) >= 3:
        S.append('<path d="%s"/>' % path_of(b['pts'], close=True))
S.append('</g>')
S.append('<path id="ctx-casa-correos" d="%s" fill="#E4E1DB" stroke="#8E8A82" stroke-width="0.5"/>' % path_of(CASA_CORREOS['pts'], close=True))
S.append('<g id="ctx-arboles-existentes" fill="none" stroke="#9DBB8F" stroke-width="0.25">')
for t in trees_exist:
    S.append('<circle cx="%.2f" cy="%.2f" r="1.8"/>' % (t['x'], Y(t['y'])))
S.append('</g>')
S.append('<g id="ctx-metro" fill="none" stroke="#5B5B8F" stroke-width="0.4">')
for m in metro:
    S.append('<rect x="%.2f" y="%.2f" width="3" height="3"/>' % (m['x'] - 1.5, Y(m['y']) - 1.5))
S.append('</g>')
S.append('<g id="ctx-hitos" fill="#4A4A4A">')
for (hx, hy), lbl in [(CARLOS_III, 'CIII'), (MARIBLANCA, 'MB'), (KM0, 'KM0'), (OSO_MADRONO, 'OM')]:
    S.append('<circle cx="%.2f" cy="%.2f" r="0.9"/>' % (hx, Y(hy)))
S.append('</g>')
S.append('</g>')

# PAISAJE (debajo de estructura para que los anillos se lean encima)
S.append('<g id="PAISAJE">')
S.append('<g id="pai-discos" fill="#C5E08C" fill-opacity="0.5" stroke="#8FB35B" stroke-width="0.25">')
for d in DISCS:
    S.append('<circle cx="%.2f" cy="%.2f" r="%.2f"/>' % (d['cx'], Y(d['cy']), d['r']))
S.append('</g>')
S.append('<g id="pai-jardineras" fill="none" stroke="#7FB069" stroke-width="1.2" stroke-opacity="0.65" stroke-linecap="round">')
for p in PLANTERS:
    S.append('<path d="%s"/>' % path_of(p['pts']))
S.append('</g>')
S.append('<g id="pai-arboles-nuevos" fill="none" stroke="#5E9C55" stroke-width="0.35">')
for (tx, ty) in NEW_TREES:
    S.append('<circle cx="%.2f" cy="%.2f" r="2.2"/><circle cx="%.2f" cy="%.2f" r="0.3"/>' % (tx, Y(ty), tx, Y(ty)))
S.append('</g>')
S.append('</g>')

# AGUA / CLIMA
S.append('<g id="AGUA_CLIMA">')
S.append('<g id="agua-balsas-elevadas" fill="#8CCFA4" fill-opacity="0.55" stroke="#4E9B6E" stroke-width="0.3">')
for p in POOLS:
    S.append('<path d="%s"/>' % path_of(ell(p['cx'], p['cy'], p['rx'], p['ry'], p['rot']), close=True))
S.append('</g>')
S.append('<g id="agua-estanques-suelo" fill="#63B98F" fill-opacity="0.6" stroke="#2F7D57" stroke-width="0.35">')
for p in GROUND_PONDS:
    if p['kind'] == 'circle':
        S.append('<circle cx="%.2f" cy="%.2f" r="%.2f"/>' % (p['cx'], Y(p['cy']), p['r']))
    else:
        S.append('<path d="%s"/>' % path_of(p['pts'], close=True))
S.append('</g>')
S.append('<path id="agua-splash" d="%s" fill="#BFE9E4" fill-opacity="0.7" stroke="#63BFB4" stroke-width="0.3" stroke-dasharray="1 0.7"/>' % path_of(ell(SPLASH['cx'], SPLASH['cy'], SPLASH['rx'], SPLASH['ry'], SPLASH['rot']), close=True))
S.append('<g id="agua-red-principal" fill="none" stroke="#F06FAE" stroke-width="0.5" stroke-opacity="0.9">')
for w in WATER_MAINS:
    S.append('<path d="%s"/>' % path_of(w))
S.append('</g>')
S.append('<g id="agua-nebulizadores" fill="#F06FAE">')
for (nx, ny) in NEBUL:
    S.append('<circle cx="%.2f" cy="%.2f" r="0.35"/>' % (nx, Y(ny)))
S.append('</g>')
S.append('</g>')

# ESTRUCTURA LIGERA
S.append('<g id="ESTRUCTURA_LIGERA">')
S.append('<g id="lig-mastiles" fill="#7A7A7A">')
for (mx, my) in MASTS:
    S.append('<circle cx="%.2f" cy="%.2f" r="0.3"/>' % (mx, Y(my)))
S.append('</g>')
S.append('<g id="lig-depositos-elevados" fill="#EE5FA0" fill-opacity="0.75" stroke="#C23B7E" stroke-width="0.3">')
for t in TANKS:
    for k in range(t['n']):
        S.append('<circle cx="%.2f" cy="%.2f" r="%.2f"/>' % (t['cx'] + k * 2.6, Y(t['cy']), t['r']))
S.append('</g>')
S.append('<g id="lig-depositos-gota" fill="none" stroke="#7FC7BD" stroke-width="0.35">')
for (dx, dy) in DROPS:
    S.append('<circle cx="%.2f" cy="%.2f" r="0.8"/>' % (dx, Y(dy)))
S.append('</g>')
S.append('</g>')

# ESTRUCTURA PRINCIPAL
S.append('<g id="ESTRUCTURA_PRINCIPAL" fill="none">')
for lp in LOOPS:
    S.append('<path id="%s" d="%s" stroke="#2FA9A4" stroke-width="%s" stroke-opacity="0.95"/>' % (
        lp['id'], path_of(ell(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot']), close=True),
        '1.6' if lp['g'] == 'G1' else '1.1'))
S.append('<circle id="CUPULA" cx="%.2f" cy="%.2f" r="%.2f" stroke="#2FA9A4" stroke-width="0.8" stroke-dasharray="1.2 0.8"/>' % (DOME['cx'], Y(DOME['cy']), DOME['r']))
S.append('</g>')

# CIRCULACION
S.append('<g id="CIRCULACION">')
S.append('<path id="cir-cinta" d="%s" fill="none" stroke="#1B7F7A" stroke-width="2.4" stroke-opacity="0.85" stroke-linecap="round"/>' % path_of(RIBBON))
S.append('<path id="cir-cinta-borde" d="%s" fill="none" stroke="#FFFFFF" stroke-width="0.5" stroke-opacity="0.9"/>' % path_of(RIBBON))
S.append('<g id="cir-escaleras" fill="#1B7F7A">')
for (sx0, sy0) in STAIRS:
    S.append('<rect x="%.2f" y="%.2f" width="2.4" height="1.4" transform="rotate(20 %.2f %.2f)"/>' % (sx0 - 1.2, Y(sy0) - 0.7, sx0, Y(sy0)))
S.append('</g>')
S.append('<g id="cir-pasos-libres" fill="none" stroke="#9A9A9A" stroke-width="0.35" stroke-dasharray="2.2 1.6">')
for c in CORRIDORS:
    S.append('<path d="%s"/>' % path_of(catmull_rom(c['pts'], 8)))
S.append('</g>')
S.append('</g>')

# PROGRAMA
S.append('<g id="PROGRAMA">')
S.append('<g id="prg-capsulas" fill="#F27BB4" fill-opacity="0.65" stroke="#D14E92" stroke-width="0.3">')
for c in CAPSULES:
    S.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" transform="rotate(%.1f %.2f %.2f)"/>' % (
        c['cx'] - c['w'] / 2, Y(c['cy']) - c['h'] / 2, c['w'], c['h'], c['h'] / 2,
        -c.get('rot', 0), c['cx'], Y(c['cy'])))
S.append('</g>')
S.append('<path id="prg-lab" d="%s" fill="#FFFFFF" fill-opacity="0.75" stroke="#D14E92" stroke-width="0.5"/>' % path_of(LAB['pts'], close=True))
S.append('<g id="prg-bancos" fill="none" stroke="#A8794A" stroke-width="0.7" stroke-linecap="round">')
for b in BENCHES:
    S.append('<path d="%s"/>' % path_of(b['pts']))
S.append('</g>')
S.append('</g>')

S.append('</svg>')
open(os.path.join(HERE, 'planta_maestra.svg'), 'w', encoding='utf-8').write('\n'.join(S))

# metricas de control
area_discs = sum(math.pi * d['r'] ** 2 for d in DISCS)
area_pools = sum(math.pi * p['rx'] * p['ry'] for p in POOLS)
print('elementos: loops %d · discos %d · capsulas %d · mastiles %d · balsas %d · arboles nuevos %d' % (
    len(LOOPS), len(DISCS), len(CAPSULES), len(MASTS), len(POOLS), len(NEW_TREES)))
print('superficie discos-canopy: %.0f m2 · balsas elevadas: %.0f m2 (plaza ~10.957 m2)' % (area_discs, area_pools))
print('OK -> geometria_maestra.json + planta_maestra.svg')
