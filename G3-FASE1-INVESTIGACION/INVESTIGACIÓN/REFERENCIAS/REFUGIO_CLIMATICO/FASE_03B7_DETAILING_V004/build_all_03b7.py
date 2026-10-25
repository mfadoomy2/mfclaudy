# -*- coding: utf-8 -*-
"""
FASE 03B.7 — constructor integral v004 (rama sobre v003; nada aprobado se sobrescribe).
Genera: MASTER_ARCHITECTURE_v004.3dm · ASSET_LIBRARY_v003.3dm · SOL_FULL_SCENE_v003.3dm
        · SOL_PRESENTATION_MASTER_v002.3dm + _viewer/scene_full.js
Fuente XY: geometria_maestra_v004.json.
Reglas NUEVAS v004 (URBAN_CONFLICTS_v003.json — causa raiz: ninguna regla conocia los edificios):
  · EDGE_GUARD: poligonos reales de 33 manzanas + 3 kioscos/estancos + Estacion de Cercanias (106);
    nada del proyecto los penetra; el empuje es tangente a la fachada mas cercana
  · loops RECORTADOS: la elipse se aplana contra la fachada (portico-galeria contra El Corte Ingles)
  · cinta PROYECTADA fuera de fachadas + perfil de anchura (belvedere sobre la Estacion)
  · tren T-O regenerado como tren-portico sobre el arco aplanado
  · figura espacial B: atrio de la Estacion, media luna de Carmen, aprons de estancos
  + todo el conflict_guard v003 (metro, estatua, corredores, poda, puertas, anti-trampa).
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

m = json.load(open(os.path.join(HERE, 'geometria_maestra_v004.json'), encoding='utf-8'))
rng = random.Random(31)

H = dict(SEAT=0.45, BACK=0.85, PLANTER=0.60, CURB=0.60, BRANCH=3.0, MIST=4.0, LOW=5.0,
         RIBBON=6.0, MID=6.75, HIGH=8.5, TANK=10.5, GTANK=1.35)
LOOP_Z = {'C1-L1': 10.0, 'C1-L2': 8.0, 'C1-L3': 8.0, 'C2-L1': 11.0, 'C2-L2': 9.0,
          'C2-L3': 7.5, 'C3-L1': 10.0, 'C3-L2': 8.5}

# ==================== 03B.6 · CONFLICT_GUARD (CR-1/7/8): chequeos cruzados en posicion FINAL ====================
CORR_ALL = [c['pts'] for c in m['circulacion']['corridors']]
MXY = [(e['x'], e['y']) for e in m['contexto']['metro'] if -110 < e['x'] < 100 and -45 < e['y'] < 75]
MASTS_XY = [tuple(p) for p in m['estructura_ligera']['masts']]
EST = m.get('estatua_v003', {'xy': [-28.0, -14.0], 'respeto_r': 8.0})
GUARD_LOG = []


def near_corr(x, y, dmin=2.2):
    for pts in CORR_ALL:
        for i in range(len(pts) - 1):
            ax, ay = pts[i]; bx, by = pts[i + 1]
            vx, vy = bx - ax, by - ay
            L2 = vx * vx + vy * vy or 1e-9
            t = max(0, min(1, ((x - ax) * vx + (y - ay) * vy) / L2))
            if math.hypot(x - (ax + vx * t), y - (ay + vy * t)) < dmin:
                return True
    return False


def metro_bad(x, y, r=0.3):
    """boca de metro invadida fisicamente por un objeto de base <+2.50 (banda 5.5 PROVISIONAL)."""
    for (a, b) in MXY:
        if math.hypot(x - a, y - b) < 5.5 + r:
            return (a, b)
    return None


def guard_xy(x, y, r, tag, corr_min=None, statue=True):
    """(x,y) valido o None: empuja radialmente fuera de boca de metro / zona de respeto; registra todo."""
    mb = metro_bad(x, y, r)
    if mb:
        ux, uy = x - mb[0], y - mb[1]
        L = math.hypot(ux, uy) or 1e-9
        d = 5.5 + r + 0.3
        x2, y2 = mb[0] + ux / L * d, mb[1] + uy / L * d
        GUARD_LOG.append({'tag': tag, 'regla': 'metro', 'de': [round(x, 2), round(y, 2)], 'a': [round(x2, 2), round(y2, 2)]})
        x, y = x2, y2
    if statue:
        ex, ey = EST['xy']
        dd = math.hypot(x - ex, y - ey)
        if dd < EST['respeto_r']:
            ux, uy = x - ex, y - ey
            L = dd or 1e-9
            x2, y2 = ex + ux / L * (EST['respeto_r'] + 0.2), ey + uy / L * (EST['respeto_r'] + 0.2)
            GUARD_LOG.append({'tag': tag, 'regla': 'estatua', 'de': [round(x, 2), round(y, 2)], 'a': [round(x2, 2), round(y2, 2)]})
            x, y = x2, y2
    g = bld_clear(x, y, r + 0.3, tag=None)
    if g is None:
        GUARD_LOG.append({'tag': tag, 'regla': 'edificio-descartado', 'de': [round(x, 2), round(y, 2)]})
        return None
    if abs(g[0] - x) > 0.05 or abs(g[1] - y) > 0.05:
        GUARD_LOG.append({'tag': tag, 'regla': 'edificio', 'de': [round(x, 2), round(y, 2)],
                          'a': [round(g[0], 2), round(g[1], 2)]})
    x, y = g
    if corr_min is not None and near_corr(x, y, corr_min + r):
        GUARD_LOG.append({'tag': tag, 'regla': 'corredor-descartado', 'de': [round(x, 2), round(y, 2)]})
        return None
    return (x, y)


# ==================== 03B.7 · EDGE_GUARD: los BORDES CONSTRUIDOS entran en la regla ====================
URB = m['urbano_v004']
_B = m['contexto']['buildings']
GBLD = [[tuple(p) for p in _B[i]['pts']] for i in URB['guard_edificios']]
KIO = [[tuple(p) for p in _B[i]['pts']] for i in URB['kioscos']]
ESTP = [tuple(p) for p in _B[URB['estacion']]['pts']]
H_KIOSCO = URB['altura_kiosco']


def _pip(x, y, poly):
    n = len(poly)
    d = False
    j = n - 1
    for i in range(n):
        xi, yi = poly[i][0], poly[i][1]
        xj, yj = poly[j][0], poly[j][1]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi):
            d = not d
        j = i
    return d


def _edge_near(x, y, poly):
    """(dist, qx, qy) al borde mas cercano del poligono."""
    best = (1e9, x, y)
    for i in range(len(poly)):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % len(poly)]
        vx, vy = bx - ax, by - ay
        L2 = vx * vx + vy * vy or 1e-9
        t = max(0, min(1, ((x - ax) * vx + (y - ay) * vy) / L2))
        qx, qy = ax + vx * t, ay + vy * t
        d = math.hypot(x - qx, y - qy)
        if d < best[0]:
            best = (d, qx, qy)
    return best


_CENTR = {}


def _escape_radial(x, y, poly, mg):
    """Salida garantizada: desde el centroide del poligono, avanzar hasta quedar fuera + margen.
    (El empuje por normal falla en los VERTICES concavos: t clampado -> direccion arbitraria.)"""
    k = id(poly)
    if k not in _CENTR:
        _CENTR[k] = (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))
    cx0, cy0 = _CENTR[k]
    ux, uy = x - cx0, y - cy0
    L = math.hypot(ux, uy) or 1e-9
    ux, uy = ux / L, uy / L
    for step in [0.5 * k2 for k2 in range(1, 80)]:
        px, py = x + ux * step, y + uy * step
        if not _pip(px, py, poly) and _edge_near(px, py, poly)[0] >= mg:
            return (px, py)
    return None


PLAZA_C = (0.0, 5.0)


def _winding(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
               for i in range(len(poly)))


_WIND = {}


def _empuje(x, y, poly, mg):
    """Empuje HACIA LA PLAZA: candidatos sobre TODAS las aristas (pie + normal exterior x margen);
    se elige el candidato valido mas cercano al centro de la plaza. Robusto en vertices concavos
    (el empuje por arista-mas-cercana metia la cinta en la calle de 2 m tras El Corte Ingles)."""
    k = id(poly)
    if k not in _WIND:
        _WIND[k] = 1.0 if _winding(poly) > 0 else -1.0
    w = _WIND[k]
    best = None
    for i in range(len(poly)):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % len(poly)]
        vx, vy = bx - ax, by - ay
        L2 = vx * vx + vy * vy or 1e-9
        L = math.sqrt(L2)
        t = max(0, min(1, ((x - ax) * vx + (y - ay) * vy) / L2))
        qx, qy = ax + vx * t, ay + vy * t
        nx0, ny0 = (vy / L) * w, (-vx / L) * w        # normal exterior (CCW -> derecha del avance)
        px, py = qx + nx0 * mg, qy + ny0 * mg
        if _pip(px, py, poly) or _edge_near(px, py, poly)[0] < mg - 0.05:
            continue
        dpl = (px - PLAZA_C[0]) ** 2 + (py - PLAZA_C[1]) ** 2
        if best is None or dpl < best[0]:
            best = (dpl, px, py)
    if best:
        return (best[1], best[2])
    g = _escape_radial(x, y, poly, mg)
    return g if g is not None else (x, y)


def bld_clear(x, y, margin, z_base=0.0, tag=None):
    """Devuelve (x,y) fuera de edificios/kioscos/estacion con esa holgura, empujando por la normal
    de la fachada mas cercana (tangencia, no teletransporte), o None si no converge."""
    POLYS = [(p, margin) for p in GBLD] + [(ESTP, max(margin, URB['margen_estacion']['suelo']))]
    if z_base < H_KIOSCO:
        POLYS += [(p, max(margin, URB['margen_kiosco'])) for p in KIO]
    x0, y0 = x, y
    for _ in range(5):
        peor = None
        for (poly, mg) in POLYS:
            d, qx, qy = _edge_near(x, y, poly)
            inside = _pip(x, y, poly)
            pen = (mg + d) if inside else (mg - d)
            if pen > 0.01 and (peor is None or pen > peor[0]):
                peor = (pen, mg, poly)
        if peor is None:
            if tag and (abs(x - x0) > 0.05 or abs(y - y0) > 0.05):
                GUARD_LOG.append({'tag': tag, 'regla': 'edge-guard',
                                  'de': [round(x0, 2), round(y0, 2)], 'a': [round(x, 2), round(y, 2)]})
            return (x, y)
        pen, mg, poly = peor
        x, y = _empuje(x, y, poly, mg + 0.05)
    if tag:
        GUARD_LOG.append({'tag': tag, 'regla': 'edge-guard-sin-salida', 'de': [round(x0, 2), round(y0, 2)]})
    return None


def snap_facade(x, y, half, band=1.5):
    """CR-2 generalizada (03B.7-D it.7): un elemento lineal contra fachada queda CERRADO (borde a
    ~2 cm) o ABIERTO (>= band); las ranuras 0.05-1.5 atrapan. half = semiancho del elemento."""
    best = None
    for poly in GBLD + [ESTP] + KIO:
        d, qx, qy = _edge_near(x, y, poly)
        dd = -d if _pip(x, y, poly) else d
        if best is None or dd < best[0]:
            best = (dd, qx, qy)
    dd, qx, qy = best
    if dd >= band + half:
        return (x, y)
    L = math.hypot(x - qx, y - qy) or 1e-9
    s = -1.0 if dd < 0 else 1.0
    ux, uy = (x - qx) / L * s, (y - qy) / L * s
    t = half + 0.02
    return (qx + ux * t, qy + uy * t)


def in_bld_any(x, y, margin=0.0, z_base=0.0):
    for p in GBLD:
        if _pip(x, y, p) or _edge_near(x, y, p)[0] < margin:
            return True
    if _pip(x, y, ESTP) or _edge_near(x, y, ESTP)[0] < max(margin, 0.5):
        return True
    if z_base < H_KIOSCO:
        for p in KIO:
            if _pip(x, y, p) or _edge_near(x, y, p)[0] < max(margin, URB['margen_kiosco'] - 0.2):
                return True
    return False


def near_main(x, y, dmin=1.9):
    for w in m['agua_clima']['mains']:
        for i in range(len(w) - 1):
            ax, ay = w[i]; bx, by = w[i + 1]
            vx, vy = bx - ax, by - ay
            L2 = vx * vx + vy * vy or 1e-9
            t = max(0, min(1, ((x - ax) * vx + (y - ay) * vy) / L2))
            if math.hypot(x - (ax + vx * t), y - (ay + vy * t)) < dmin:
                return True
    return False


PLANT_PTS = [tuple(q) for p in m['paisaje']['planters'] for q in p['pts']]
CAPS_XY = [(c['cx'], c['cy']) for c in m['programa']['capsules']]


def chaikin(pts):
    n = len(pts)
    closed = math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) < 1.0
    out = []
    for i in range(n - 1):
        a, b = pts[i], pts[i + 1]
        out.append((a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25))
        out.append((a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75))
    if closed:
        out.append(out[0])
    else:
        out = [tuple(pts[0])] + out + [tuple(pts[-1])]
    return out


def _circum(a, b, c):
    la = math.hypot(b[0] - a[0], b[1] - a[1]); lb = math.hypot(c[0] - b[0], c[1] - b[1])
    lc = math.hypot(c[0] - a[0], c[1] - a[1])
    area2 = abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))
    if area2 < 1e-6 or min(la, lb) < 0.05:
        return 1e9
    return la * lb * lc / (2 * area2)


def min_radius(pts):
    return min([_circum(pts[i - 1], pts[i], pts[i + 1]) for i in range(1, len(pts) - 1)] or [1e9])


def smooth_to_radius(pts, rmin=4.75, iters=1200, w=0.35):
    """Suavizado laplaciano selectivo: solo mueve vertices con radio local < rmin (Chaikin no basta,
    converge a la curvatura de la esquina; esto la ENSANCHA de verdad)."""
    closed = math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) < 1.0
    P = [list(p) for p in (pts[:-1] if closed else pts)]
    N = len(P)
    for _ in range(iters):
        moved = False
        newP = [p[:] for p in P]
        for i in range(N):
            if not closed and (i == 0 or i == N - 1):
                continue
            a, b, c = P[(i - 1) % N], P[i], P[(i + 1) % N]
            if _circum(a, b, c) < rmin:
                moved = True
                newP[i][0] = b[0] * (1 - w) + (a[0] + c[0]) / 2 * w
                newP[i][1] = b[1] * (1 - w) + (a[1] + c[1]) / 2 * w
        P = newP
        if not moved:
            break
    out = [tuple(p) for p in P]
    if closed:
        out.append(out[0])
    return out


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
    ('19_DETALLE', (150, 140, 125, 255), 1.0),
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
def _lobed_crown(cz, r, lobes, squash=0.85, min_base=None):
    """min_base (CR-5): poda de formacion — ninguna esfera de copa baja de esa cota (V-025)."""
    parts = []
    if min_base is not None:
        cz = max(cz, min_base + r)
    parts.append(('15_VEGETATION_FULL', mk.sphere((0, 0, cz), r, 10, 8)))
    for k in range(lobes):
        a = 2 * math.pi * k / lobes + 0.4
        rr = r * rng.uniform(0.45, 0.62)
        zz = cz + rng.uniform(-0.3, 0.5) * r * squash
        if min_base is not None:
            zz = max(zz, min_base + rr)
        parts.append(('15_VEGETATION_FULL', mk.sphere((r * 0.72 * math.cos(a), r * 0.72 * math.sin(a), zz), rr, 8, 6)))
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
    parts += _lobed_crown(h * 0.62 + r * 0.5, r, 5, min_base=2.55)
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


def stair_switchback():
    """CR-3a (V-020/035/042/043): escalera REAL de 2 tramos (18+17 CH 0.171 / H 0.29) con meseta 1.50,
    doble pasamanos a 0.95/0.70 ambos lados, zanca cerrada y faldon de proteccion bajo galibo <2.20.
    Local: tramo A en y=0 sube hacia +x; meseta; tramo B en y=-1.55 vuelve; pasarela hacia -y (tablero)."""
    CH, HU, W = 6.0 / 35, 0.29, 1.4
    XA = -2.6
    xa = XA + 18 * HU              # 2.62 fin tramo A
    parts = []
    for k in range(18):
        parts.append(('03_SECONDARY_STRUCTURE', mk.box((XA + HU * (k + 0.5), 0, CH * (k + 1) - 0.025), HU + 0.02, W, 0.05)))
    parts.append(('03_SECONDARY_STRUCTURE', mk.box((xa + 0.75, -0.775, 18 * CH - 0.025), 1.5, 2.95, 0.05)))
    for k in range(17):
        parts.append(('03_SECONDARY_STRUCTURE', mk.box((xa - HU * (k + 0.5), -1.55, CH * (19 + k) - 0.025), HU + 0.02, W, 0.05)))
    xb = xa - 17 * HU              # -2.31 llegada a +6.00
    parts.append(('03_SECONDARY_STRUCTURE', mk.box((xb - 0.1, -2.6, 5.97), 1.4, 0.9, 0.06)))   # pasarela al tablero

    def plate(x0, z0, x1, z1, y0):
        V = [(x0, y0, max(z0 - 0.45, 0.0)), (x0, y0, z0 + 0.02), (x1, y0, z1 + 0.02), (x1, y0, max(z1 - 0.45, 0.0))]
        return (V, [(0, 1, 2), (0, 2, 3)])

    for y0 in (-0.7, 0.7):
        parts.append(('03_SECONDARY_STRUCTURE', plate(XA, 0.0, xa, 18 * CH, y0)))          # zanca cerrada tramo A
    for y0 in (-2.25, -0.85):
        parts.append(('03_SECONDARY_STRUCTURE', plate(xa, 18 * CH, xb, 6.0, y0)))          # zanca cerrada tramo B
    # cierre macizo bajo el tramo A (almacen/jardinera): ninguna celda pisable con galibo <2.50
    parts.append(('03_SECONDARY_STRUCTURE', mk.box((-0.03, 0, 0.45), 5.15, 1.5, 0.9)))
    # doble pasamanos ambos lados, ambos tramos + borde de meseta
    for y0 in (-0.75, 0.75):
        for hh in (0.95, 0.70):
            parts.append(('03_SECONDARY_STRUCTURE', mk.cylinder((XA, y0, hh), (xa, y0, 18 * CH + hh), 0.028, 5)))
    for y0 in (-2.3, -0.8):
        for hh in (0.95, 0.70):
            parts.append(('03_SECONDARY_STRUCTURE', mk.cylinder((xa, y0, 18 * CH + hh), (xb, y0, 6.0 + hh), 0.028, 5)))
    for hh in (0.95, 0.70):
        parts.append(('03_SECONDARY_STRUCTURE', mk.cylinder((xa + 1.5, 0.7, 18 * CH + hh), (xa + 1.5, -2.25, 18 * CH + hh), 0.028, 5)))
    parts.append(('04_MASTS', mk.cylinder((xa + 0.75, -0.775, 0), (xa + 0.75, -0.775, 18 * CH - 0.05), 0.12, 8)))
    parts.append(('04_MASTS', mk.cylinder((xb, -1.55, 0), (xb, -1.55, 5.95), 0.12, 8)))
    return parts


def lift_tower():
    """CR-3b: ASCENSOR-CAPSULA — fuste cilindrico transparente + cabina POD rosa + pasarela al tablero (-y)."""
    parts = [('06_MEMBRANES', mk.cylinder((0, 0, 0), (0, 0, 7.4), 1.2, 18))]
    for zz in (0.1, 3.0, 6.0, 7.35):
        parts.append(('03_SECONDARY_STRUCTURE', mk.torus((0, 0, zz), 1.2, 0.05, 16, 5)))
    for adeg in (0, 90, 180, 270):
        a = math.radians(adeg)
        parts.append(('03_SECONDARY_STRUCTURE', mk.cylinder((1.2 * math.cos(a), 1.2 * math.sin(a), 0),
                                                            (1.2 * math.cos(a), 1.2 * math.sin(a), 7.4), 0.06, 6)))
    parts.append(('08_PINK_MODULES', mk.cylinder((0, 0, 0.15), (0, 0, 2.35), 0.95, 14)))
    parts.append(('08_PINK_MODULES', mk.sphere((0, 0, 2.35), 0.95, 12, 6)))
    parts.append(('03_SECONDARY_STRUCTURE', mk.box((0, -1.7, 5.97), 1.3, 1.3, 0.06)))       # pasarela de embarque +6.00
    parts.append(('13_PIPES', mk.cylinder((0, 0, 7.4), (0, 0, 7.95), 0.09, 6)))
    return parts


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
    'STAIR_SB': stair_switchback(), 'LIFT_TOWER': lift_tower(),
}

_BLOCKS_LEGACY = {
    # E02 — biblioteca vegetal por roles
    'VEG2_ARBOL_A': veg2_arbol('A'), 'VEG2_ARBOL_B': veg2_arbol('B'), 'VEG2_ARBOL_EX': veg2_arbol('EX'),
    'VEG2_TREPADORA': veg2_trepadora(), 'VEG2_BAJA': veg2_baja(), 'VEG2_TROPICAL': veg2_tropical(),
    'VEG2_HUERTO': veg2_huerto(), 'VEG2_ACUATICA': veg2_acuatica(), 'VEG2_COLGANTE': veg2_colgante(),
}
BLOCKS.update(_BLOCKS_LEGACY)

# ==================== 03B.7 §6-§17 · DETAILING LOD B/C de las familias ====================
import detailing_03b7 as DET  # noqa: E402

_det_delta = DET.upgrade_blocks(BLOCKS, mk, rng)


def _blk_reach(name):
    """Alcance horizontal REAL del bloque (max |xy| de sus vertices) — la guarda usa esto, no constantes."""
    r = 0.0
    for (_ly, (V, F)) in BLOCKS[name]:
        for (vx, vy, vz) in V:
            r = max(r, math.hypot(vx, vy))
    return r


ARBOL_REACH = max(_blk_reach('VEG2_ARBOL_A'), _blk_reach('VEG2_ARBOL_B'))
print('detailing: %d familias enriquecidas/sustituidas' % len(_det_delta))


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
    try:   # 03B.7 §24: metadatos para la futura auditoria municipal
        a.SetUserString('sistema', layer)
        a.SetUserString('familia', name)
        a.SetUserString('version', 'v004')
    except Exception:
        pass
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
    try:
        a.SetUserString('familia', name)
        a.SetUserString('version', 'v004')
    except Exception:
        pass
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
    # ---- Carlos III (CR-9 / DEC-0006): consolidado en v003, proxy G2+ sin precision inventada ----
    # 03B.7-C: grupo ecuestre COHERENTE — la peana APOYA en la grada (v003 la dejaba levitar
    # 1.1 m) y el caballo PISA la peana (antes quedaba medio hundido y las patas dentro del bloque).
    ex, ey = EST['xy']
    PTOP = 0.5 + 2.4                                     # grada 0-0.5 + pedestal 0.5-2.9
    body = mk.sphere((0, 0, 0), 1.0, 10, 7)
    Vh = [(ex + vx * 1.55, ey + vy * 0.52, 4.25 + vz * 0.60) for (vx, vy, vz) in body[0]]
    for nm2, VF2 in [('EST_GRADA', mk.box((ex, ey, 0.0), 5.6, 3.8, 0.5)),
                     ('EST_PEDESTAL', mk.box((ex, ey, 0.5), 4.4, 2.6, 2.4)),
                     ('EST_CABALLO', (Vh, body[1])),
                     ('EST_CUELLO', mk.cylinder((ex + 1.05, ey, 4.55), (ex + 1.75, ey, 5.45), 0.24, 7)),
                     ('EST_CABEZA_CAB', mk.cylinder((ex + 1.75, ey, 5.45), (ex + 2.18, ey, 5.18), 0.13, 6)),
                     ('EST_JINETE', mk.cylinder((ex - 0.15, ey, 4.80), (ex - 0.15, ey, 5.72), 0.30, 8)),
                     ('EST_BRAZO', mk.cylinder((ex - 0.15, ey - 0.26, 5.35), (ex + 0.58, ey - 0.44, 5.62), 0.07, 5)),
                     ('EST_CABEZA', mk.sphere((ex - 0.15, ey, 5.92), 0.24, 6, 5))]:
        add_mesh(f, lidx, '00_CONTEXT', nm2, VF2)
        sc.mesh('00_CONTEXT', VF2)
    add_curve(f, lidx, '30_CURVES', 'EST_RESPETO_R8', [(q[0], q[1], 0.05) for q in ell_pts(ex, ey, 8, 8, 0, 40)])
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

    # ---- estructura principal: loops RECORTADOS contra fachadas (03B.7-A1) ----
    LOOPP = {}
    ECI_POLY = next((p for p in GBLD if _pip(-75, 25, p)), None)

    def loop_pts(lp):
        """polilinea cerrada del loop, aplanada contra las fachadas-guard y re-suavizada.
        Devuelve (pts_cerrados, mascara_plana) — la mascara marca el arco-portico contra ECI."""
        if lp['id'] in LOOPP:
            return LOOPP[lp['id']]
        mg = URB['margen_edificio']['loop']
        base = ell_pts(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'], 96)[:-1]
        out, flat = [], []
        for (px, py) in base:
            best = None
            for poly in GBLD:
                d, qx, qy = _edge_near(px, py, poly)
                inside = _pip(px, py, poly)
                pen = (mg + d) if inside else (mg - d)
                if pen > 0.01 and (best is None or pen > best[0]):
                    best = (pen, qx, qy, inside, poly)
            es_eci = False
            if best:
                pen, qx, qy, inside, poly = best
                ux, uy = px - qx, py - qy
                L = math.hypot(ux, uy) or 1e-9
                nx0, ny0 = (ux / L, uy / L) if not inside else (-ux / L, -uy / L)
                px, py = qx + nx0 * mg, qy + ny0 * mg
                es_eci = (poly is ECI_POLY)
            out.append((px, py))
            flat.append(es_eci)
        out.append(out[0]); flat.append(flat[0])

        def clip_once(pp):
            o2 = []
            for (px, py) in pp:
                best = None
                for poly in GBLD:
                    d, qx, qy = _edge_near(px, py, poly)
                    inside = _pip(px, py, poly)
                    pen = (mg + d) if inside else (mg - d)
                    if pen > 0.01 and (best is None or pen > best[0]):
                        best = (pen, poly)
                if best:
                    px, py = _empuje(px, py, best[1], mg)
                o2.append((px, py))
            return o2

        pts = chaikin(out)
        f2 = []
        for i in range(len(out) - 1):
            f2 += [flat[i], flat[i]]
        f2.append(f2[0])
        for _ in range(3):   # el suavizado no puede reinvadir la fachada: clip<->smooth iterado
            pts = smooth_to_radius(pts, 5.0, iters=300)
            pts = clip_once(pts)
        pts = smooth_to_radius(pts, 4.5, iters=120)
        pts = clip_once(pts)
        if len(f2) != len(pts):
            f2 = [False] * len(pts)
        LOOPP[lp['id']] = (pts, f2)
        return LOOPP[lp['id']]

    def poly_off(P2, off):
        n0 = len(P2)
        out = []
        for i in range(n0):
            a0 = P2[i - 1]; b0 = P2[(i + 1) % n0]
            dx, dy = b0[0] - a0[0], b0[1] - a0[1]
            L = math.hypot(dx, dy) or 1e-9
            out.append((P2[i][0] - dy / L * off, P2[i][1] + dx / L * off))
        return out

    for lp in m['estructura_principal']['loops']:
        z = LOOP_Z[lp['id']]
        lpts, _lf = loop_pts(lp)
        P2 = lpts[:-1]
        pts = [(p[0], p[1], z) for p in lpts]
        add_curve(f, lidx, '30_CURVES', 'AXIS_%s' % lp['id'], pts)
        main = mk.tube(pts, 0.30, 12)
        add_mesh(f, lidx, '02_PRIMARY_STRUCTURE', 'PRIMARY_%s' % lp['id'], main)
        sc.mesh('02_PRIMARY_STRUCTURE', main)
        offA, offB = poly_off(P2, 0.75), poly_off(P2, -0.75)
        for ring in (offA, offB):
            pts2 = [(p[0], p[1], z - 0.35) for p in ring + [ring[0]]]
            sat = mk.tube(pts2, 0.10, 8)
            add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'SAT_%s' % lp['id'], sat)
            sc.mesh('03_SECONDARY_STRUCTURE', sat)
        acc = 0.0
        kk = 0
        for i in range(len(P2)):
            acc += math.hypot(P2[i][0] - P2[i - 1][0], P2[i][1] - P2[i - 1][1])
            if acc < 2.4:
                continue
            acc = 0.0
            p0, p1 = offA[i], offB[i]
            trv = mk.cylinder((p0[0], p0[1], z - 0.35), (p1[0], p1[1], z - 0.35), 0.05, 5)
            add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'TRV', trv)
            sc.mesh('03_SECONDARY_STRUCTURE', trv)
            if kk % 3 == 0:
                nd = mk.sphere((P2[i][0], P2[i][1], z), 0.22, 6, 5)
                add_mesh(f, lidx, '02_PRIMARY_STRUCTURE', 'NODE', nd)
                sc.mesh('02_PRIMARY_STRUCTURE', nd)
            kk += 1

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

    # ---- cinta (CR-3): eje suavizado r>=4.7, barandilla completa, escaleras reales, ascensores ----
    rib = [tuple(p) for p in m['circulacion']['ribbon']]
    rib = chaikin(chaikin(rib))                      # densifica y redondea

    def _push_balsas(pts):
        # el tablero no puede entrar en las balsas elevadas (rim + barandilla)
        for p_b in m['agua_clima']['pools']:
            if not (5.0 <= p_b.get('cota', 7) <= 7.3):
                continue
            rr_b = max(p_b['rx'], p_b['ry']) + 1.8
            pts = [((p_b['cx'] + (px0 - p_b['cx']) / (math.hypot(px0 - p_b['cx'], py0 - p_b['cy']) or 1e-9) * rr_b,
                     p_b['cy'] + (py0 - p_b['cy']) / (math.hypot(px0 - p_b['cx'], py0 - p_b['cy']) or 1e-9) * rr_b)
                    if math.hypot(px0 - p_b['cx'], py0 - p_b['cy']) < rr_b else (px0, py0))
                   for (px0, py0) in pts]
        return pts

    def _push_edificios(pts):
        # 03B.7: el tablero NUNCA cruza una fachada; se proyecta al offset y el suavizado
        # lo convierte en tangencia (ECI = el tramo-portico; Estacion = el abrazo-balcon)
        mgc = URB['margen_edificio']['cinta'] + 0.4    # +0.4: bulto del offset en esquinas concavas
        mge = max(mgc, URB['margen_estacion']['cinta'])
        out2 = []
        for (px0, py0) in pts:
            best = None
            for poly in GBLD:
                d, qx, qy = _edge_near(px0, py0, poly)
                inside = _pip(px0, py0, poly)
                pen = (mgc + d) if inside else (mgc - d)
                if pen > 0.01 and (best is None or pen > best[0]):
                    best = (pen, mgc, poly)
            d, qx, qy = _edge_near(px0, py0, ESTP)
            inside = _pip(px0, py0, ESTP)
            pen = (mge + d) if inside else (mge - d)
            if pen > 0.01 and (best is None or pen > best[0]):
                best = (pen, mge, ESTP)
            for poly in KIO:     # el tablero tampoco vuela los estancos (2.2 m de galibo no es digno)
                d, qx, qy = _edge_near(px0, py0, poly)
                inside = _pip(px0, py0, poly)
                pen = (2.0 + d) if inside else (2.0 - d)
                if pen > 0.01 and (best is None or pen > best[0]):
                    best = (pen, 2.0, poly)
            if best:
                pen, mg, poly = best
                px0, py0 = _empuje(px0, py0, poly, mg)
            out2.append((px0, py0))
        return out2

    # suavizar<->empujar iterado: converge a tangencias (balsas + fachadas + Estacion)
    for _ in range(6):
        rib = smooth_to_radius(rib, 4.75, iters=500)
        rib = _push_balsas(rib)
        rib = _push_edificios(rib)
    for _k9 in range(3):     # 03B.7-D (V-028): pulir los quiebros que deja el clip, sin perder holgura
        rib = smooth_to_radius(rib, 4.75, iters=160, w=0.14)
        rib = _push_balsas(rib)
        rib = _push_edificios(rib)
    rib = _push_edificios(_push_edificios(rib))   # doble pasada final: esquinas concavas (ECI)
    _rmin = min_radius(rib)
    GUARD_LOG.append({'tag': 'RIBBON', 'regla': 'radio-final', 'r_min': round(_rmin, 2)})
    GUARD_LOG.append({'tag': 'CINTA', 'regla': 'suavizado+balsas+fachadas', 'radio_min': round(min_radius(rib), 2)})
    n = len(rib)
    add_curve(f, lidx, '30_CURVES', 'RIBBON_AXIS', [(p[0], p[1], H['RIBBON']) for p in rib])
    # perfil de anchura: 1.25 base + belvedere sobre la cabeza de la Estacion (atrio_v004)
    bel = m['atrio_v004']['estacion']['belvedere']
    WH = []
    for (px0, py0) in rib:
        dd0 = math.hypot(px0 - bel['c'][0], py0 - bel['c'][1])
        ff = max(0.0, 1 - dd0 / bel['radio_influencia'])
        WH.append(1.25 + bel['ancho_extra'] * ff * ff)

    def var_strip(pts, half, z0, z1):
        Lp, Rp = [], []
        n0 = len(pts)
        for i, p in enumerate(pts):
            a0 = pts[max(i - 1, 0)]; b0 = pts[min(i + 1, n0 - 1)]
            dx, dy = b0[0] - a0[0], b0[1] - a0[1]
            Ln = math.hypot(dx, dy) or 1e-9
            Lp.append((p[0] - dy / Ln * half[i], p[1] + dx / Ln * half[i]))
            Rp.append((p[0] + dy / Ln * half[i], p[1] - dx / Ln * half[i]))
        V, F = [], []
        for i in range(n0):
            V += [(Lp[i][0], Lp[i][1], z1), (Rp[i][0], Rp[i][1], z1),
                  (Lp[i][0], Lp[i][1], z0), (Rp[i][0], Rp[i][1], z0)]
        for i in range(n0 - 1):
            a = 4 * i
            F += [(a, a + 4, a + 5), (a, a + 5, a + 1),
                  (a + 2, a + 7, a + 6), (a + 2, a + 3, a + 7),
                  (a, a + 6, a + 4), (a, a + 2, a + 6),
                  (a + 1, a + 5, a + 7), (a + 1, a + 7, a + 3)]
        return V, F

    deck = var_strip(rib, WH, H['RIBBON'] - 0.22, H['RIBBON'])
    add_mesh(f, lidx, '02_PRIMARY_STRUCTURE', 'RIBBON_DECK', deck)
    sc.mesh('02_PRIMARY_STRUCTURE', deck)

    def rib_tan(i):
        a0 = rib[max(i - 1, 0)]; b0 = rib[min(i + 1, n - 1)]
        dx, dy = b0[0] - a0[0], b0[1] - a0[1]
        L = math.hypot(dx, dy) or 1e-9
        return dx / L, dy / L

    def rib_side(off):
        out = []
        for i, p in enumerate(rib):
            tx, ty = rib_tan(i)
            out.append((p[0] - ty * off, p[1] + tx * off))
        return out

    def rib_side_w(delta):
        """offset relativo al BORDE variable del tablero (belvedere incluido)."""
        out = []
        for i, p in enumerate(rib):
            tx, ty = rib_tan(i)
            off = WH[i] + delta
            out.append((p[0] - ty * off, p[1] + tx * off))
        return out

    sideP, sideN = rib_side_w(-0.05), [(2 * rib[i][0] - q[0], 2 * rib[i][1] - q[1])
                                       for i, q in enumerate(rib_side_w(-0.05))]
    sideM = rib_side_w(-0.27)  # linea interior: nebulizadores (libres del BALPOST)
    sideC = rib_side_w(0.30)   # linea exterior: colgantes (libres del canto variable)

    # anclajes de escaleras/ascensores: deslizan por la cinta (SIN wrap) y se validan con la
    # HUELLA REAL del bloque transformada (perimetro muestreado), no con rejillas aproximadas
    def _huella(i, s, es_stair):
        """puntos del perimetro del bloque en coordenadas de mundo (mapeo IDENTICO a place())."""
        tx, ty = rib_tan(i)
        rot = math.atan2(ty, tx) + (0 if s > 0 else math.pi)
        ca, sa = math.cos(rot), math.sin(rot)
        off_c = 3.8 if es_stair else 2.9
        bx = rib[i][0] - ty * s * off_c
        by = rib[i][1] + tx * s * off_c
        pts = []
        if es_stair:
            us = [-2.85 + 0.9 * k for k in range(9)]           # -2.85 .. 4.35
            vs = [-3.05 + 0.95 * k for k in range(5)]          # -3.05 .. 0.75 (local y)
            per = [(u, vs[0]) for u in us] + [(u, vs[-1]) for u in us] + \
                  [(us[0], v) for v in vs] + [(us[-1], v) for v in vs]
        else:
            per = [(1.55 * math.cos(a), 1.55 * math.sin(a)) for a in
                   [k * math.pi / 6 for k in range(12)]] + [(0, -2.5)]
        for (u, v) in per:
            pts.append((bx + u * ca - v * sa, by + u * sa + v * ca))
        return pts

    def anchor(tx0, ty0, probes_u, foot_off, corr_dmin, tag):
        es_stair = len(probes_u) > 1
        i0 = min(range(n), key=lambda i: (rib[i][0] - tx0) ** 2 + (rib[i][1] - ty0) ** 2)
        for estricto in (True, False):
            for k in sorted(range(-30, 31), key=abs):
                i = i0 + k
                if i < 2 or i > n - 3:
                    continue
                for s in (1, -1):
                    ok = True
                    for (px_, py_) in _huella(i, s, es_stair):
                        if in_bld_any(px_, py_, 0.5, 0.0):
                            ok = False; break
                        if estricto and (near_corr(px_, py_, corr_dmin - 1.2) or metro_bad(px_, py_, 0.5)
                                         or near_main(px_, py_, 1.2)
                                         or any(math.hypot(px_ - qx, py_ - qy) < 1.4 for (qx, qy) in PLANT_PTS)
                                         or any(math.hypot(px_ - qx, py_ - qy) < 1.6 for (qx, qy) in CAPS_XY)):
                            ok = False; break
                    if ok:
                        if k != 0 or s != 1 or not estricto:
                            GUARD_LOG.append({'tag': tag, 'regla': 'anclaje-deslizado' if estricto else 'anclaje-relajado',
                                              'de': [round(tx0, 1), round(ty0, 1)],
                                              'a': [round(rib[i][0], 1), round(rib[i][1], 1)], 'lado': s})
                        return i, s
        GUARD_LOG.append({'tag': tag, 'regla': 'SIN-ANCLAJE-descartado', 'de': [round(tx0, 1), round(ty0, 1)]})
        return None, None

    GAPS = {1: set(), -1: set()}
    anchors = []
    for (sx, sy) in m['circulacion']['stairs']:
        i, s = anchor(sx, sy, (-2.4, -0.8, 0.8, 2.4, 4.0), 2.8, 3.4, 'STAIR@%.0f,%.0f' % (sx, sy))
        if i is None:
            continue
        anchors.append(('STAIR_SB', i, s))
        for k in range(i - 2, i + 3):
            GAPS[s].add(k % n)
    for (tx0, ty0) in [(-75, 10), (5, 30), (72, 8)]:   # C1-oeste · C2-norte · C3-este
        i, s = anchor(tx0, ty0, (0.0,), 2.9, 3.2, 'LIFT@%d,%d' % (tx0, ty0))
        if i is None:
            continue
        anchors.append(('LIFT_TOWER', i, s))
        for k in range(i - 1, i + 2):
            GAPS[s].add(k % n)

    # barandilla completa (V-036): pasamanos 1.05 + travesano 0.55 + rodapie 0.10, con huecos de embarque
    for off, sgn in ((1.2, 1), (-1.2, -1)):
        side = sideP if sgn > 0 else sideN
        runs, cur = [], []
        for i in range(n):
            if i in GAPS[sgn]:
                if len(cur) > 2:
                    runs.append(cur)
                cur = []
            else:
                cur.append(side[i])
        if len(cur) > 2:
            runs.append(cur)
        for seg in runs:
            for (hh, rr) in ((1.05, 0.045), (0.55, 0.032), (0.10, 0.03)):
                rail = mk.tube([(q[0], q[1], H['RIBBON'] + hh) for q in seg], rr, 6)
                add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'RIBBON_RAIL', rail)
                sc.mesh('03_SECONDARY_STRUCTURE', rail)
            for q in seg[::2]:
                bp = mk.cylinder((q[0], q[1], H['RIBBON']), (q[0], q[1], H['RIBBON'] + 1.05), 0.028, 5)
                add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'BALPOST', bp)
                sc.mesh('03_SECONDARY_STRUCTURE', bp)
                pl = mk.box((q[0], q[1], H['RIBBON'] + 0.002), 0.11, 0.11, 0.012)   # §8 pletina de montante
                add_mesh(f, lidx, '19_DETALLE', 'BALPOST_PLETINA', pl)
                sc.mesh('19_DETALLE', pl)
    # nebulizadores de barandilla (CL-004): 8 uds por el interior del pasamanos
    for i in range(n // 16, n - 1, max(n // 8, 1)):
        q = sideM[i]
        nbp = mk.cylinder((q[0], q[1], H['RIBBON']), (q[0], q[1], H['RIBBON'] + 1.35), 0.03, 5)
        add_mesh(f, lidx, '13_PIPES', 'RIBNEB', nbp)
        sc.mesh('13_PIPES', nbp)
        ms = mk.sphere((q[0], q[1], H['RIBBON'] + 1.15), 0.5, 6, 4)
        add_mesh(f, lidx, '12_MIST', 'RIBNEB_MIST', ms)
        sc.mesh('12_MIST', ms)
    # apoyos (CR-7: nunca en boca de metro; CR-1: nunca pegados a escalera/ascensor)
    ANCHOR_PTS = [rib[i] for (_nm2, i, _s2) in anchors]
    acc = 0.0
    en_salto = False
    for i in range(1, n):
        acc += math.hypot(rib[i][0] - rib[i - 1][0], rib[i][1] - rib[i - 1][1])
        if acc > 12 and any(math.hypot(rib[i][0] - ax0, rib[i][1] - ay0) < 6.5 for (ax0, ay0) in ANCHOR_PTS):
            continue
        if acc > 12 and not near_corr(*rib[i]):
            if metro_bad(rib[i][0], rib[i][1], 0.5) or in_bld_any(rib[i][0], rib[i][1], 0.7, 0.0):
                if not en_salto:
                    GUARD_LOG.append({'tag': 'RIB_SUP', 'regla': 'metro/edificio-salto',
                                      'xy': [round(rib[i][0], 1), round(rib[i][1], 1)]})
                    en_salto = True
                continue
            en_salto = False
            sup = mk.cylinder((rib[i][0], rib[i][1], 0), (rib[i][0], rib[i][1], H['RIBBON'] - 0.22), 0.17, 8)
            cap = mk.cylinder((rib[i][0], rib[i][1], H['RIBBON'] - 0.8), (rib[i][0], rib[i][1], H['RIBBON'] - 0.22), 0.3, 8)
            add_mesh(f, lidx, '02_PRIMARY_STRUCTURE', 'RIB_SUP', sup)
            add_mesh(f, lidx, '02_PRIMARY_STRUCTURE', 'RIB_CAP', cap)
            sc.mesh('02_PRIMARY_STRUCTURE', sup); sc.mesh('02_PRIMARY_STRUCTURE', cap)
            acc = 0.0
    # colocacion de escaleras y ascensores (bloques; -y local = hacia el tablero)
    LIFTS_XY = []
    for (nm2, i, s) in anchors:
        tx, ty = rib_tan(i)
        rot = math.atan2(ty, tx) + (0 if s > 0 else math.pi)
        off_c = 3.8 if nm2 == 'STAIR_SB' else 2.9
        px_, py_ = rib[i][0] - ty * s * off_c, rib[i][1] + tx * s * off_c
        if nm2 == 'LIFT_TOWER':
            LIFTS_XY.append((px_, py_))
        place(f, ids, nm2, px_, py_, 0, rot)
        sc.inst(nm2, px_, py_, 0, rot)
        add_curve(f, lidx, '30_CURVES', '%s_LINK' % nm2, [(rib[i][0], rib[i][1], H['RIBBON']), (px_, py_, H['RIBBON'])])

    # ---- redes tensadas ----
    for lpi, a0, a1 in [(0, 150, 260), (3, -30, 80), (6, 120, 230)]:
        lp = m['estructura_principal']['loops'][lpi]
        z = LOOP_Z[lp['id']]
        nn = 12
        lpts, _lf = loop_pts(lp)
        P2 = lpts[:-1]
        n2 = len(P2)
        cxl = sum(p[0] for p in P2) / n2
        cyl = sum(p[1] for p in P2) / n2
        outer = [P2[int(((a0 + (a1 - a0) * i / nn) % 360) / 360.0 * n2) % n2] for i in range(nn + 1)]
        inner = [(cxl + (p[0] - cxl) * 0.45, cyl + (p[1] - cyl) * 0.45) for p in outer]
        # 03B.7-B: la red no cuelga sobre la Estacion (altura real ~6 m; el velo baja a z-2.2)
        keepn = [i for i in range(nn + 1)
                 if not (_pip(outer[i][0], outer[i][1], ESTP) or _pip(inner[i][0], inner[i][1], ESTP)
                         or _edge_near(outer[i][0], outer[i][1], ESTP)[0] < 1.0)]
        outer = [outer[i] for i in keepn]
        inner = [inner[i] for i in keepn]
        nn = len(outer) - 1
        if nn < 2:
            continue
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
        g = bld_clear(d['cx'], d['cy'], d['r'] + 0.85, z_base=cota - 1.5, tag='DISC_%d' % i)
        if g is None:
            continue
        d['cx'], d['cy'] = g       # el disco reconoce la fachada (y los cables/goteos le siguen)
        place(f, ids, nm, d['cx'], d['cy'], cota, rot)
        sc.inst(nm, d['cx'], d['cy'], cota, rot)
    for lp in m['estructura_principal']['loops']:
        z = LOOP_Z[lp['id']]
        lpts, _lf = loop_pts(lp)
        P2 = lpts[:-1]
        for i in range(0, len(P2), max(1, len(P2) // 12)):
            px, py = P2[i]
            nd = sorted(DISCS, key=lambda dd: (dd['cx'] - px) ** 2 + (dd['cy'] - py) ** 2)[:1]
            if nd and (nd[0]['cx'] - px) ** 2 + (nd[0]['cy'] - py) ** 2 < 42:
                dd = nd[0]
                cota = min(max(dd.get('cota', 6.0), 4.2), H['HIGH'])
                sc.line('05_CABLES', [(px, py, z), (dd['cx'], dd['cy'], cota)])
                add_curve(f, lidx, '05_CABLES', 'LCBL', [(px, py, z), (dd['cx'], dd['cy'], cota)])

    # ---- capsulas ----
    # 03B.7-A1 · TREN-PORTICO: T-O renace sobre el arco de C1-L1 aplanado contra El Corte Ingles
    TREN_XY = []                      # 03B.7-D (V-046/50): los bancos se cortan tambien en el tren
    tp = m['programa'].get('tren_portico')
    if tp:
        lp1 = next(l for l in m['estructura_principal']['loops'] if l['id'] == 'C1-L1')
        lpts, lflat = loop_pts(lp1)
        P2 = lpts[:-1]
        n2 = len(P2)
        runs, cur = [], []
        for i in range(n2):
            if lflat[i]:
                cur.append(i)
            elif cur:
                runs.append(cur); cur = []
        if cur:
            runs.append(cur)
        if runs:
            run = max(runs, key=len)
            # offset hacia el lado PLAZA (el opuesto a ECI)
            offs_in = poly_off(P2, 2.6)
            offs_out = poly_off(P2, -2.6)
            mid = run[len(run) // 2]
            lado = offs_in if (ECI_POLY and _edge_near(*offs_in[mid], ECI_POLY)[0] >
                               _edge_near(*offs_out[mid], ECI_POLY)[0]) else offs_out
            # longitud del arco util y colocacion 3+puerta
            arco = [lado[i] for i in run]
            L_arc = sum(math.hypot(arco[k + 1][0] - arco[k][0], arco[k + 1][1] - arco[k][1])
                        for k in range(len(arco) - 1))
            w = tp['w']
            ncap = min(tp['n'], max(3, int((L_arc - 2.4) // (w + 0.25))))
            puestos = 0
            s_obj = (L_arc - (ncap * w + (ncap - 1) * 0.25 + (max(0, (ncap - 1) // 3)) * 2.15)) / 2
            s_next = s_obj + w / 2
            seguidas = 0
            acc = 0.0
            k = 0
            while puestos < ncap and k < len(arco) - 1:
                seg = math.hypot(arco[k + 1][0] - arco[k][0], arco[k + 1][1] - arco[k][1])
                if acc + seg >= s_next:
                    f0 = (s_next - acc) / (seg or 1e-9)
                    px_ = arco[k][0] + (arco[k + 1][0] - arco[k][0]) * f0
                    py_ = arco[k][1] + (arco[k + 1][1] - arco[k][1]) * f0
                    rotc = math.atan2(arco[k + 1][1] - arco[k][1], arco[k + 1][0] - arco[k][0])
                    if (not in_bld_any(px_, py_, 3.1, 0.0)) and not metro_bad(px_, py_, 1.6):
                        place(f, ids, 'POD_TRAIN', px_, py_, 0, rotc)
                        sc.inst('POD_TRAIN', px_, py_, 0, rotc)
                        TREN_XY.append((px_, py_))
                        puestos += 1
                        seguidas += 1
                    s_next += (w + 0.25) if seguidas < 3 else (w + 2.15)
                    if seguidas >= 3:
                        seguidas = 0
                acc += seg
                k += 1
            GUARD_LOG.append({'tag': 'TREN_PORTICO', 'regla': 'A1', 'capsulas': puestos,
                              'arco_m': round(L_arc, 1)})
    # ---- mastiles (tras el tren: la reubicacion por eje/carmen tambien debe esquivar el TREN) ----
    def _mast_ok(px2, py2):
        """03B.7-D: el mastil (tiesto r0.8) no puede quedar sobre un EJE declarado, la media luna
        de Carmen, el tren-portico ni una capsula — el empuje de fachada dejaba varios encima."""
        if near_corr(px2, py2, 1.75):
            return False
        cl = m['atrio_v004']['carmen']['media_luna_bancos']
        dd = math.hypot(px2 - cl['c'][0], py2 - cl['c'][1])
        ang = math.degrees(math.atan2(py2 - cl['c'][1], px2 - cl['c'][0])) % 360
        if abs(dd - cl['r']) < 1.4 and cl['a0'] <= ang <= cl['a1']:
            return False
        if any(math.hypot(px2 - qx, py2 - qy) < 3.0 for (qx, qy) in TREN_XY):
            return False
        if any(math.hypot(px2 - c2['cx'], py2 - c2['cy']) < max(c2.get('w', 1.8), 1.8) / 2 + 1.9
               for c2 in m['programa']['capsules']):
            return False
        # it.5: dos mastiles reubicados acababan SOLAPADOS en el mismo bolsillo (V-001 canal 0.5 m)
        if any(math.hypot(px2 - ma[0], py2 - ma[1]) < 3.4 for ma in MASTS):
            return False
        return True

    MASTS = []
    for (mx0, my0) in m['estructura_ligera']['masts']:
        g = bld_clear(mx0, my0, 3.2, tag='MAST')   # 3.2 = alcance del brazo (2.9) + margen
        if g is None:
            continue
        if not _mast_ok(g[0], g[1]):
            best = None
            for rr in (1.2, 2.0, 2.8, 3.6):
                for kk in range(8):
                    aa = kk * math.pi / 4 + rr
                    g2 = bld_clear(g[0] + rr * math.cos(aa), g[1] + rr * math.sin(aa), 3.2)
                    if g2 is not None and _mast_ok(g2[0], g2[1]):
                        dd = math.hypot(g2[0] - mx0, g2[1] - my0)
                        if best is None or dd < best[0]:
                            best = (dd, g2)
                if best is not None:
                    break
            if best is None:
                GUARD_LOG.append({'tag': 'MAST', 'regla': 'sin-sitio-descartado',
                                  'de': [round(mx0, 1), round(my0, 1)]})
                continue
            GUARD_LOG.append({'tag': 'MAST', 'regla': 'eje/carmen/tren-reubicado',
                              'de': [round(g[0], 2), round(g[1], 2)],
                              'a': [round(best[1][0], 2), round(best[1][1], 2)]})
            g = best[1]
        MASTS.append(g)
    MASTS_XY[:] = [tuple(g) for g in MASTS]   # 03B.7-D: TODA guarda posterior usa posiciones FINALES
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

    # CR-1 anti-trampa: dos pods sueltos o se tocan o dejan >=0.90 de paso (V-06x PODS 0.50)
    caps_all = m['programa']['capsules']
    POS = {i: [c['cx'], c['cy']] for i, c in enumerate(caps_all)}
    for _pass in range(4):
        moved = False
        for i, ci in enumerate(caps_all):
            if ci.get('id') in ('T-O', 'T-SE'):
                continue
            for j, cj in enumerate(caps_all):
                if j <= i or cj.get('id') in ('T-O', 'T-SE'):
                    continue
                ri, rj = max(ci['w'], 1.8) / 2, max(cj['w'], 1.8) / 2
                dx0, dy0 = POS[j][0] - POS[i][0], POS[j][1] - POS[i][1]
                d0 = math.hypot(dx0, dy0) or 1e-9
                gap = d0 - ri - rj
                if 0.05 < gap < 0.9:
                    need = ri + rj + 0.95
                    POS[j][0] = POS[i][0] + dx0 / d0 * need
                    POS[j][1] = POS[i][1] + dy0 / d0 * need
                    moved = True
                    GUARD_LOG.append({'tag': 'POD_GAP', 'regla': 'anti-trampa 0.90',
                                      'a': [round(POS[j][0], 2), round(POS[j][1], 2)]})
        if not moved:
            break
    for i, c in enumerate(m['programa']['capsules']):
        cid = c.get('id', '')
        rot = math.radians(-c.get('rot', 0))
        if in_bld_any(c['cx'], c['cy'], 0.5, 0.0):    # 03B.7: ninguna capsula dentro de edificio/estacion/kiosco
            GUARD_LOG.append({'tag': 'CAP/%s' % cid, 'regla': 'edificio-retirada',
                              'xy': [round(c['cx'], 1), round(c['cy'], 1)]})
            gi_skip = True
            continue
        if cid in ('T-O', 'T-SE'):
            place(f, ids, 'POD_TRAIN', c['cx'], c['cy'], 0, rot)
            sc.inst('POD_TRAIN', c['cx'], c['cy'], 0, rot)
            TREN_XY.append((c['cx'], c['cy']))
        else:
            dia = max(c['w'], 1.8)
            nm = 'POD_S' if dia < 2.7 else ('POD_M' if dia < 3.9 else 'POD_L')
            px_, py_ = POS[i]
            g = bld_clear(px_, py_, dia / 2 + 0.4, tag=None)   # el anti-trampa no puede meter un pod en fachada
            if g is None:
                continue
            px_, py_ = g
            for (mx2, my2) in MASTS_XY:   # CR-1: un pod nunca contra un mastil (V-070)
                dm2 = math.hypot(px_ - mx2, py_ - my2)
                need = dia / 2 + 1.05
                if 1e-6 < dm2 < need:
                    px_, py_ = mx2 + (px_ - mx2) / dm2 * need, my2 + (py_ - my2) / dm2 * need
                    GUARD_LOG.append({'tag': 'POD/%s' % cid, 'regla': 'mastil', 'a': [round(px_, 2), round(py_, 2)]})
            if cid == 'R-N' and i % 3 == 0:
                zc = 4.5 - (dia / 2 + 0.3)
                place(f, ids, nm, px_, py_, zc, rot)
                sc.inst(nm, px_, py_, zc, rot)
                sc.line('05_CABLES', [(px_, py_, zc + dia + 0.5), (px_ + 1.5, py_ - 1.5, 9.0)])
            else:
                place(f, ids, nm, px_, py_, 0, rot)
                sc.inst(nm, px_, py_, 0, rot)
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
        # §14 balsa con sistema legible: aro inferior + gargola-rebosadero + hilo + pendolas
        rim2 = mk.tube([(q[0], q[1], p['cota'] - 0.22) for q in pts], 0.06, 6)
        add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'BASINRIM2_%s' % p['id'], rim2)
        sc.mesh('03_SECONDARY_STRUCTURE', rim2)
        gx = p['cx'] + p['rx'] * math.cos(0.9)
        gy = p['cy'] + p['ry'] * math.sin(0.9)
        gg = mk.cylinder((gx, gy, p['cota'] - 0.05), (gx + 0.35, gy + 0.2, p['cota'] - 0.18), 0.035, 5)
        add_mesh(f, lidx, '13_PIPES', 'BASIN_GARGOLA_%s' % p['id'], gg)
        sc.mesh('13_PIPES', gg)
        hilo = mk.cylinder((gx + 0.38, gy + 0.22, p['cota'] - 0.2), (gx + 0.42, gy + 0.25, 0.5), 0.014, 4)
        add_mesh(f, lidx, '11_WATER', 'BASIN_HILO_%s' % p['id'], hilo)
        sc.mesh('11_WATER', hilo)
        for adeg in (60, 240):
            qx2 = p['cx'] + p['rx'] * 0.9 * math.cos(math.radians(adeg))
            qy2 = p['cy'] + p['ry'] * 0.9 * math.sin(math.radians(adeg))
            pend = mk.cylinder((qx2, qy2, p['cota']), (qx2, qy2, p['cota'] + 1.7), 0.025, 5)
            add_mesh(f, lidx, '05_CABLES', 'BASIN_PENDOLA_%s' % p['id'], pend)
            sc.mesh('05_CABLES', pend)
        add_curve(f, lidx, '30_CURVES', 'BASIN_AXIS_%s' % p['id'], [(q[0], q[1], p['cota']) for q in pts])
    PONDS_FIN = []                    # 03B.7-D: posiciones FINALES de balsas para guardas posteriores
    for p in m['agua_clima']['ground_ponds']:
        if p['kind'] == 'circle':
            g = bld_clear(p['cx'], p['cy'], p['r'] + 0.16, tag='POND_%s' % p['id'])
            if g is None:
                continue
            # CR-2 (it.9): margen 0.6 dejaba el bordillo a 0.46 de la fachada = ranura-trampa;
            # la balsa CIERRA contra el muro (borde a ~2 cm) o queda ABIERTA >= 1.5
            g = snap_facade(g[0], g[1], p['r'] + 0.14, band=1.5)
            p = dict(p, cx=g[0], cy=g[1])
            PONDS_FIN.append((p['cx'], p['cy'], p['r'] + 0.14))
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
            qs = []
            for q in p['pts']:
                g = bld_clear(q[0], q[1], 0.8)
                if g is not None:
                    qs.append(g)
            if len(qs) < 3:
                continue
            wt = mk.surf(qs, 0.45)
            add_mesh(f, lidx, '11_WATER', 'POND_%s' % p['id'], wt)
            sc.mesh('11_WATER', wt)
    sp = m['agua_clima']['splash']
    spl = mk.surf(ell_pts(sp['cx'], sp['cy'], sp['rx'], sp['ry'], sp['rot'], 32)[:-1], 0.03)
    add_mesh(f, lidx, '11_WATER', 'SPLASH', spl)
    sc.mesh('11_WATER', spl)
    for w in m['agua_clima']['mains']:
        # CR-9 (V-019): la conduccion se ENRASA (canaleta z=0.08) alli donde cruza un corredor
        pts3 = []
        for i in range(len(w) - 1):
            ax, ay = w[i]; bx, by = w[i + 1]
            L = math.hypot(bx - ax, by - ay)
            steps = max(1, int(L / 0.75))
            last = (i == len(w) - 2)
            for k in range(steps + (1 if last else 0)):
                t = k / steps
                x, y = ax + (bx - ax) * t, ay + (by - ay) * t
                g = bld_clear(x, y, 0.5)          # 03B.7: la conduccion bordea las fachadas, no las cruza
                if g is not None:
                    x, y = g
                pts3.append((x, y, -0.12 if near_corr(x, y, 2.4) else 0.32))   # enrasada de verdad: tapa a +0.04
        t = mk.tube(pts3, 0.16, 8)
        add_mesh(f, lidx, '13_PIPES', 'MAIN', t)
        sc.mesh('13_PIPES', t)
        add_curve(f, lidx, '30_CURVES', 'PIPE_AXIS', pts3)
    for (nx, ny) in m['agua_clima']['nebul']:
        g = guard_xy(nx, ny, 0.15, 'NEB_POST')   # CR-7 (V-048/050/051): fuera de bocas de metro
        if g is None:
            continue
        place(f, ids, 'NEB_POST', g[0], g[1], 0)
        sc.inst('NEB_POST', g[0], g[1], 0)
    for t in m['estructura_ligera']['tanks']:
        for k in range(t['n']):
            cx = t['cx'] + k * 2.6
            g = bld_clear(cx, t['cy'], t['r'] + 1.0, tag='TANK')   # margen = alcance real del toro
            if g is None:
                continue
            cx, tcy = g
            t = dict(t, cy=tcy)
            pole = mk.cylinder((cx, t['cy'], 0), (cx, t['cy'], H['TANK'] - 1), 0.18, 8)
            toro = mk.torus((cx, t['cy'], H['TANK']), t['r'], 0.85, 18, 9)
            add_mesh(f, lidx, '04_MASTS', 'TKPOLE', pole)
            add_mesh(f, lidx, '08_PINK_MODULES', 'TANK', toro)
            sc.mesh('04_MASTS', pole); sc.mesh('08_PINK_MODULES', toro)
            sc.line('13_PIPES', [(cx, t['cy'], H['TANK']), (cx, t['cy'], 0.32)])
            add_curve(f, lidx, '13_PIPES', 'RISER', [(cx, t['cy'], H['TANK']), (cx, t['cy'], 0.32)])
            # CR-6: plataforma de inspeccion 1.2x1.2 + pates de acceso en cada poste (56 comp. mantenibles)
            plat = mk.box((cx, t['cy'] + 0.85, H['TANK'] - 1.72), 1.2, 1.2, 0.06)
            add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'TKPLAT', plat)
            sc.mesh('03_SECONDARY_STRUCTURE', plat)
            zz = 2.2   # los pates arrancan sobre la banda de cuerpo (0.05-2.10): no obstruyen el paso
            while zz < H['TANK'] - 1.8:
                pate = mk.cylinder((cx - 0.16, t['cy'] + 0.2, zz), (cx + 0.16, t['cy'] + 0.2, zz), 0.02, 4)
                add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'PATE', pate)
                sc.mesh('03_SECONDARY_STRUCTURE', pate)
                zz += 0.4
    for (dx, dy) in m['estructura_ligera']['drops']:
        g = bld_clear(dx, dy, 0.95, tag='DROP')
        if g is None:
            continue
        place(f, ids, 'DROP_TANK', g[0], g[1], 0)
        sc.inst('DROP_TANK', g[0], g[1], 0)

    # ---- mobiliario ----
    def offs(pts, off):
        out = []
        for j, q in enumerate(pts):
            a0 = pts[max(j - 1, 0)]; b0 = pts[min(j + 1, len(pts) - 1)]
            dxq, dyq = b0[0] - a0[0], b0[1] - a0[1]
            Lq = math.hypot(dxq, dyq) or 1e-9
            out.append((q[0] - dyq / Lq * off, q[1] + dxq / Lq * off))
        return out

    def cut_segs(pts, obst, gap_break):
        """obst = [(x, y, r_clear)]: corta la polilinea al llegar a cualquier obstaculo."""
        keep = [q for q in pts if all(math.hypot(q[0] - ox, q[1] - oy) > orr for (ox, oy, orr) in obst)]
        segs, cur = [], []
        for q in keep:
            if cur and math.hypot(q[0] - cur[-1][0], q[1] - cur[-1][1]) > gap_break:
                segs.append(cur); cur = []
            cur.append(q)
        if cur:
            segs.append(cur)
        return segs, len(pts) - len(keep)

    # muestras de la conduccion principal: los bancos tampoco pueden cabalgar la tuberia (CR-1)
    MAINS_SAMP = []
    for w in m['agua_clima']['mains']:
        for i2 in range(len(w) - 1):
            ax, ay = w[i2]; bx, by = w[i2 + 1]
            L2_ = math.hypot(bx - ax, by - ay)
            st2 = max(1, int(L2_ / 0.75))
            for k2 in range(st2 + 1):
                t2 = k2 / st2
                MAINS_SAMP.append((ax + (bx - ax) * t2, ay + (by - ay) * t2, 0.85))
    OBST_BENCH = ([(mx, my, 1.2) for (mx, my) in MASTS_XY] + MAINS_SAMP
                  + [(EST['xy'][0], EST['xy'][1], 6.0)]    # franja de respeto de la estatua (DEC-0006)
                  + [(tx, ty, 3.0) for (tx, ty) in TREN_XY])   # 03B.7-D: el banco no atraviesa el tren

    for i, b in enumerate(m['programa']['benches']):
        if len(b['pts']) < 3:
            continue
        # CR-1 + 03B.7: el banco se corta en cubas y tuberias; contra fachada CIERRA o ABRE (CR-2)
        bpts = [snap_facade(q[0], q[1], 0.36) for q in b['pts']]
        if len(bpts) < len(b['pts']):
            GUARD_LOG.append({'tag': 'BENCH_%d' % i, 'regla': 'edge-corte',
                              'quitados': len(b['pts']) - len(bpts)})
        if len(bpts) < 3:
            continue
        segs, quitados = cut_segs(bpts, OBST_BENCH, 2.6)
        if quitados:
            GUARD_LOG.append({'tag': 'BENCH_%d' % i, 'regla': 'corte-mastil', 'quitados': quitados})
        for si, seg in enumerate(segs):
            if len(seg) < 3 or sum(math.hypot(seg[k + 1][0] - seg[k][0], seg[k + 1][1] - seg[k][1])
                                   for k in range(len(seg) - 1)) < 1.8:
                continue   # it.8: fragmento de banco <1.8 m = residuo
            s1 = mk.strip(seg, 0.62, 0.12, H['SEAT'])
            add_mesh(f, lidx, '10_FURNITURE', 'BENCH_%d_%d' % (i, si), s1)
            sc.mesh('10_FURNITURE', s1)
            cb = mk.strip(seg, 0.68, H['SEAT'] - 0.025, H['SEAT'] + 0.006)         # §16 canto del asiento
            add_mesh(f, lidx, '19_DETALLE', 'BENCH_CANTO_%d_%d' % (i, si), cb)
            sc.mesh('19_DETALLE', cb)
            for q in seg[::3]:                                                     # §16 patas
                pt = mk.box((q[0], q[1], 0.06), 0.5, 0.12, 0.12)
                add_mesh(f, lidx, '10_FURNITURE', 'BENCH_PATA', pt)
                sc.mesh('10_FURNITURE', pt)
            if i % 2 == 0 and len(seg) >= 4:   # CR-9 (V-027): respaldos construidos en la mitad de los bancos
                bk = mk.strip(offs(seg, 0.27), 0.09, H['SEAT'], H['BACK'])
                add_mesh(f, lidx, '10_FURNITURE', 'BENCHBACK_%d_%d' % (i, si), bk)
                sc.mesh('10_FURNITURE', bk)
    # CR-6 puerta D-C1-1 · V-023 bolsillo · franja de respeto de la estatua · puertas anti-trampa:
    # cada paso estrangulado de 0.50 m entre jardineras (SW + montera) se abre a >=1.5 m (regla CR-2
    # generalizada: una barrera lineal siempre tiene puertas; el 0.50 atrapa, el 1.5 deja pasar)
    GATES_R = [((-72, 17), 1.6), ((6.9, -4.1), 3.0), (tuple(EST['xy']), 6.0),
               ((43.2, 0.3), 2.3), ((45.0, 1.0), 2.0), ((-54, -22), 2.3), ((-57, -17), 2.3), ((-50, -16), 2.3),
               ((-64, -16), 2.3), ((-43, -14), 2.3), ((-70, -13), 2.3)]
    def _snap_mast_pl(q):
        """CR-2 (it.9): jardinera contra mastil — el lecho CIERRA contra el tiesto (gap ~2 cm)
        en vez de dejar pasos de 0.3-0.5 m entre ambos."""
        for (mx3, my3) in MASTS_XY:
            d3 = math.hypot(q[0] - mx3, q[1] - my3)
            if d3 < 3.06:
                L3_ = d3 or 1e-9
                return (mx3 + (q[0] - mx3) / L3_ * 1.60, my3 + (q[1] - my3) / L3_ * 1.60)
        return q

    for i, p in enumerate(m['paisaje']['planters']):
        if len(p['pts']) < 3:
            continue
        # 03B.7-D (V-001/4/5/7): la jardinera + su canto (semiancho 0.76) respetan los EJES declarados
        # con 0.90 de hombro => filtro de corredor 1.66; y el hueco de particion baja a 2.0 para que
        # el puente entre puntos eliminados no tienda cuerdas sobre un eje.
        # CR-2 (it.7): contra fachada la jardinera CIERRA (snap del borde) o ABRE >=1.5 — nunca
        # ranuras-trampa de 0.5 m (V-001/V-006); y sigue respetando puertas y ejes declarados
        keep = [_snap_mast_pl(snap_facade(q[0], q[1], 0.78)) for q in p['pts']]
        keep = [q for q in keep if all(math.hypot(q[0] - gx, q[1] - gy) > gr for ((gx, gy), gr) in GATES_R)
                and not near_corr(q[0], q[1], 1.66)]
        segs, cur = [], []
        for q in keep:
            if cur and math.hypot(q[0] - cur[-1][0], q[1] - cur[-1][1]) > 2.0:
                segs.append(cur); cur = []
            cur.append(q)
        if cur:
            segs.append(cur)
        quitados = len(p['pts']) - len(keep)
        if quitados:
            GUARD_LOG.append({'tag': 'PLANTER_%d' % i, 'regla': 'puerta', 'quitados': quitados})
        for si, seg in enumerate(segs):
            if len(seg) < 3 or sum(math.hypot(seg[k + 1][0] - seg[k][0], seg[k + 1][1] - seg[k][1])
                                   for k in range(len(seg) - 1)) < 2.4:
                continue   # it.8: un fragmento <2.4 m es residuo de filtros, no jardinera (V-001/006)
            s1 = mk.strip(seg, 1.4, 0, H['PLANTER'])
            add_mesh(f, lidx, '09_PLANTERS', 'PLANTER_%d_%d' % (i, si), s1)
            sc.mesh('09_PLANTERS', s1)
            cp = mk.strip(seg, 1.52, H['PLANTER'] - 0.04, H['PLANTER'] + 0.015)   # §16 coronacion/canto
            add_mesh(f, lidx, '19_DETALLE', 'PLANTER_CANTO_%d_%d' % (i, si), cp)
            sc.mesh('19_DETALLE', cp)
            for q in seg[::5]:                                                    # §16 mechinales de drenaje
                wp = mk.cylinder((q[0], q[1], 0.045), (q[0] + 0.75, q[1], 0.035), 0.02, 4)
                add_mesh(f, lidx, '13_PIPES', 'PLANTER_MECHINAL', wp)
                sc.mesh('13_PIPES', wp)
            if full:
                for qi, q in enumerate(seg[::4]):
                    if metro_bad(q[0], q[1], 0.4):   # CR-7 (V-046): nada plantado sobre una boca
                        GUARD_LOG.append({'tag': 'PLANTER_VEG', 'regla': 'metro', 'xy': [round(q[0], 1), round(q[1], 1)]})
                        continue
                    # CR-1 + 03B.7: la veg de jardinera no invade capsulas, ascensores ni FACHADAS
                    if (any(math.hypot(q[0] - cx2, q[1] - cy2) < 2.6 for (cx2, cy2) in CAPS_XY)
                            or any(math.hypot(q[0] - lx2, q[1] - ly2) < 3.2 for (lx2, ly2) in LIFTS_XY)
                            or in_bld_any(q[0], q[1], 2.4, 0.0)):   # alcance real de la pala de alocasia
                        GUARD_LOG.append({'tag': 'PLANTER_VEG', 'regla': 'capsula/ascensor',
                                          'xy': [round(q[0], 1), round(q[1], 1)]})
                        continue
                    nmv = ('VEG2_TROPICAL', 'VEG2_BAJA')[qi % 2]
                    place(f, ids, nmv, q[0], q[1], H['PLANTER'], qi * 0.8)
                    sc.inst(nmv, q[0], q[1], H['PLANTER'], qi * 0.8)
    for k, (vx, vy) in enumerate(m['mantenimiento_v003']['viveros']):   # CR-6: viveros con pasillo de servicio
        g = guard_xy(vx, vy, 1.2, 'NURSERY_%d' % k, corr_min=1.6)
        if g is None:
            g = (vx, vy)
        place(f, ids, 'NURSERY', g[0], g[1], 0, k * 0.9)
        sc.inst('NURSERY', g[0], g[1], 0, k * 0.9)
    for (rx0, ry0) in m['mantenimiento_v003']['registros_tecnicos']:    # CR-6: registros tecnicos 1.2x0.8x1.1
        g = bld_clear(rx0, ry0, 1.0, tag='REGISTRO')
        if g is None:
            continue
        if any(math.hypot(g[0] - qx, g[1] - qy) < 3.2 for (qx, qy) in TREN_XY):
            g2r = next(((g[0] + dxr, g[1] + dyr) for (dxr, dyr) in
                        ((3.2, 0), (-3.2, 0), (0, 3.2), (0, -3.2), (2.3, 2.3), (-2.3, 2.3), (2.3, -2.3), (-2.3, -2.3))
                        if not any(math.hypot(g[0] + dxr - qx, g[1] + dyr - qy) < 3.2 for (qx, qy) in TREN_XY)
                        and not in_bld_any(g[0] + dxr, g[1] + dyr, 1.0, 0.0)), None)
            if g2r is None:
                GUARD_LOG.append({'tag': 'REGISTRO', 'regla': 'tren-descartado', 'de': [round(g[0], 1), round(g[1], 1)]})
                continue
            GUARD_LOG.append({'tag': 'REGISTRO', 'regla': 'tren-reubicado', 'a': [round(g2r[0], 1), round(g2r[1], 1)]})
            g = g2r
        rg = mk.box((g[0], g[1], 0.0), 1.2, 0.8, 1.1)
        add_mesh(f, lidx, '13_PIPES', 'REGISTRO', rg)
        sc.mesh('13_PIPES', rg)
    for line in m['mantenimiento_v003']['recirculacion']:               # CR-6: linea de recirculacion por cluster
        wp = []
        for q in line:
            g = bld_clear(q[0], q[1], 0.8, tag='RECIRC')
            if g is not None:
                wp.append(g)
        if len(wp) < 2:
            continue
        pts3 = [(q[0], q[1], 0.26) for q in wp]
        rt = mk.tube(pts3, 0.09, 6)
        add_mesh(f, lidx, '13_PIPES', 'RECIRC', rt)
        sc.mesh('13_PIPES', rt)
        add_curve(f, lidx, '30_CURVES', 'RECIRC_AXIS', pts3)
    for (tx, ty) in [(-70, -2), (-20, 24), (30, 22), (74, 4)]:
        for (mx2, my2) in MASTS_XY:   # CR-1: el totem no se hinca en la cuba de un mastil
            dt = math.hypot(tx - mx2, ty - my2)
            if dt < 1.5:
                tx = mx2 + (tx - mx2) / (dt or 1e-9) * 1.5
                ty = my2 + (ty - my2) / (dt or 1e-9) * 1.5
                GUARD_LOG.append({'tag': 'TOTEM', 'regla': 'mastil', 'a': [round(tx, 2), round(ty, 2)]})
        g = bld_clear(tx, ty, 0.6, tag='TOTEM')
        if g is None:
            continue
        place(f, ids, 'TOTEM', g[0], g[1], 0)
        sc.inst('TOTEM', g[0], g[1], 0)

    # ---- 03B.7-B · FIGURA ESPACIAL: atrio de la Estacion + media luna de Carmen + aprons ----
    at = m['atrio_v004']
    bx0, by0 = at['estacion']['boca']
    for rr_ in at['estacion']['anillo_pavimento']['r']:
        seg = []
        for a in range(0, 361, 4):
            px_ = bx0 + rr_ * math.cos(math.radians(a))
            py_ = by0 + rr_ * math.sin(math.radians(a))
            if _pip(px_, py_, ESTP) or in_bld_any(px_, py_, 0.1, 0.0):
                if len(seg) > 2:
                    band = mk.strip(seg, 0.14, 0.0, 0.04)
                    add_mesh(f, lidx, '19_DETALLE', 'ATRIO_BANDA', band)
                    sc.mesh('19_DETALLE', band)
                seg = []
            else:
                seg.append((px_, py_))
        if len(seg) > 2:
            band = mk.strip(seg, 0.14, 0.0, 0.04)
            add_mesh(f, lidx, '19_DETALLE', 'ATRIO_BANDA', band)
            sc.mesh('19_DETALLE', band)
    for (sx_, sy_) in at['estacion']['senaletica'] + at['carmen']['senaletica']:
        g = guard_xy(sx_, sy_, 0.3, 'SENAL')
        if g:
            for (pcx, pcy, pcr) in PONDS_FIN:      # it.10: el totem no se hinca en el bordillo de una balsa
                d5 = math.hypot(g[0] - pcx, g[1] - pcy)
                if d5 < pcr + 0.55:
                    L5 = d5 or 1e-9
                    g = (pcx + (g[0] - pcx) / L5 * (pcr + 0.55), pcy + (g[1] - pcy) / L5 * (pcr + 0.55))
                    GUARD_LOG.append({'tag': 'SENAL', 'regla': 'balsa', 'a': [round(g[0], 2), round(g[1], 2)]})
            place(f, ids, 'TOTEM', g[0], g[1], 0)
            sc.inst('TOTEM', g[0], g[1], 0)
    ml = at['carmen']['media_luna_bancos']
    arc = [(ml['c'][0] + ml['r'] * math.cos(math.radians(a)), ml['c'][1] + ml['r'] * math.sin(math.radians(a)))
           for a in range(ml['a0'], ml['a1'] + 1, 6)]
    arc = [q for q in arc if not in_bld_any(q[0], q[1], 0.8, 0.0) and not metro_bad(q[0], q[1], 0.4)
           and not near_corr(q[0], q[1], 1.8)
           and not any(math.hypot(q[0] - pc[0], q[1] - pc[1]) < pc[2] + 1.05 for pc in PONDS_FIN)]
    if len(arc) > 3:
        s1 = mk.strip(arc, 0.62, 0, H['SEAT'])
        add_mesh(f, lidx, '10_FURNITURE', 'BENCH_CARMEN', s1)
        sc.mesh('10_FURNITURE', s1)
        bk = mk.strip(offs(arc, 0.27), 0.09, H['SEAT'], H['BACK'])
        add_mesh(f, lidx, '10_FURNITURE', 'BENCHBACK_CARMEN', bk)
        sc.mesh('10_FURNITURE', bk)
    for ap in at['aprons_kiosco']:
        poly = m['contexto']['buildings'][ap['edif']]['pts']
        cxk = sum(p[0] for p in poly) / len(poly)
        cyk = sum(p[1] for p in poly) / len(poly)
        ring = []
        for p in poly[::max(1, len(poly) // 24)]:
            dd0 = math.hypot(p[0] - cxk, p[1] - cyk) or 1e-9
            s = (dd0 + ap['margen']) / dd0
            ring.append((cxk + (p[0] - cxk) * s, cyk + (p[1] - cyk) * s))
        if len(ring) > 3:
            band = mk.strip(ring + [ring[0]], 0.12, 0.0, 0.04)
            add_mesh(f, lidx, '19_DETALLE', 'APRON_KIOSCO_%d' % ap['edif'], band)
            sc.mesh('19_DETALLE', band)

    # ---- 03B.7 §8/§18/§19/§20 · DETAILING de sitio (cinta, pavimento, Carlos III, contexto) ----
    DET.site_details(lambda layer, nombre, VF: (add_mesh(f, lidx, layer, nombre, VF),
                                                sc.mesh(layer, VF)),
                     sc, mk, m, rib, WH, rib_side_w, in_bld_any, EST, ESTP,
                     m['contexto']['buildings'])

    # ---- vegetacion / personas (solo full) ----
    if full:
        # E02: arboles de sombra multilobulados — CR-1: guard en posicion final + separacion de discos bajos (V-063)
        for i, (tx, ty) in enumerate(m['paisaje']['new_trees']):
            g = guard_xy(tx, ty, 0.4, 'ARBOL_%d' % i, corr_min=2.1)
            if g is None:
                continue
            tx, ty = g
            # 03B.7-D: las CUATRO guardas (disco/cupula/cinta/fachada) se iteran hasta CONVERGER —
            # una sola pasada dejaba que el empuje de fachada devolviera el arbol bajo un disco
            ok_t = False
            for _rep in range(3):
                for d in m['paisaje']['discs']:
                    if d.get('cota', 6) < 7.4:
                        dd2 = math.hypot(tx - d['cx'], ty - d['cy'])
                        need = d['r'] + 3.0          # copa con lobulos: alcance real ~2.8
                        if 1e-6 < dd2 < need:
                            tx = d['cx'] + (tx - d['cx']) / dd2 * need
                            ty = d['cy'] + (ty - d['cy']) / dd2 * need
                            GUARD_LOG.append({'tag': 'ARBOL_%d' % i, 'regla': 'disco-bajo', 'a': [round(tx, 2), round(ty, 2)]})
                dm_ = m['estructura_principal']['dome']
                dd4 = math.hypot(tx - dm_['cx'], ty - dm_['cy'])
                if dd4 < dm_['r'] + 3.0:             # CR-1: ninguna copa contra la cupula-pergola
                    ux, uy = tx - dm_['cx'], ty - dm_['cy']
                    L4 = dd4 or 1e-9
                    tx = dm_['cx'] + ux / L4 * (dm_['r'] + 3.0)
                    ty = dm_['cy'] + uy / L4 * (dm_['r'] + 3.0)
                    GUARD_LOG.append({'tag': 'ARBOL_%d' % i, 'regla': 'cupula', 'a': [round(tx, 2), round(ty, 2)]})
                # CR-1: la copa tampoco puede tocar el tablero de la cinta (deck 5.78-6.00 vs copa hasta 6.8)
                best = None
                for i2 in range(len(rib) - 1):
                    ax, ay = rib[i2]; bx, by = rib[i2 + 1]
                    vx, vy = bx - ax, by - ay
                    L2_ = vx * vx + vy * vy or 1e-9
                    t2 = max(0, min(1, ((tx - ax) * vx + (ty - ay) * vy) / L2_))
                    qx, qy = ax + vx * t2, ay + vy * t2
                    dd3 = math.hypot(tx - qx, ty - qy)
                    if best is None or dd3 < best[0]:
                        best = (dd3, qx, qy)
                _mgc = 1.45 + ARBOL_REACH   # 03B.7-D: borde real del tablero + alcance REAL de la copa v2
                if best and best[0] < _mgc:
                    ux, uy = tx - best[1], ty - best[2]
                    L3 = best[0] or 1e-9
                    tx, ty = best[1] + ux / L3 * _mgc, best[2] + uy / L3 * _mgc
                    GUARD_LOG.append({'tag': 'ARBOL_%d' % i, 'regla': 'cinta', 'a': [round(tx, 2), round(ty, 2)]})
                    if near_corr(tx, ty, 2.1):
                        break
                # comprobacion de copa contra fachadas — margen = alcance REAL del bloque v2
                g4 = bld_clear(tx, ty, ARBOL_REACH + 0.15, tag='ARBOL_%d' % i)
                if g4 is None:
                    break
                tx, ty = g4
                _drib = min(math.hypot(tx - q[0], ty - q[1]) for q in rib)
                if (not near_corr(tx, ty, 2.1)
                        and _drib > _mgc - 0.1
                        and not any(d.get('cota', 6) < 7.4
                                    and 1e-6 < math.hypot(tx - d['cx'], ty - d['cy']) < d['r'] + 2.95
                                    for d in m['paisaje']['discs'])):
                    ok_t = True
                    break
            if not ok_t:
                GUARD_LOG.append({'tag': 'ARBOL_%d' % i, 'regla': 'sin-convergencia-descartado'})
                continue
            nmv = ('VEG2_ARBOL_A', 'VEG2_ARBOL_B')[i % 2]
            place(f, ids, nmv, tx, ty, 0, i * 0.8)
            sc.inst(nmv, tx, ty, 0, i * 0.8)
        for i, t in enumerate(m['contexto']['trees']):
            if -110 < t['x'] < 100 and -45 < t['y'] < 75:
                place(f, ids, 'VEG2_ARBOL_EX', t['x'], t['y'], 0, i * 0.6)
                sc.inst('VEG2_ARBOL_EX', t['x'], t['y'], 0, i * 0.6)
        # trepadoras en la mitad de los mastiles — 03B.7-D: no en mastiles pegados a la cinta
        # (el derrame de la enredadera tocaria los soportes RIB_SUP)
        for i, (mx, my) in enumerate(MASTS):
            if i % 2 == 0:
                d_rib = min(math.hypot(mx - q[0], my - q[1]) for q in rib)
                if d_rib < 2.6:
                    GUARD_LOG.append({'tag': 'TREPADORA_%d' % i, 'regla': 'cinta-omitida'})
                    continue
                place(f, ids, 'VEG2_TREPADORA', mx, my, 0, i * 0.5)
                sc.inst('VEG2_TREPADORA', mx, my, 0, i * 0.5)
        # HUERTO en el interior de C1 (bajo las balsas elevadas, cf. 24D82F58)
        def near_metro_pt(x, y):
            return any(math.hypot(x - a, y - b) < 6.0 for (a, b) in MXY)

        def near_pipe(x, y, dmin=1.2):   # CR-1 (V-057): el huerto respeta la conduccion principal
            for w in m['agua_clima']['mains']:
                for j in range(len(w) - 1):
                    ax, ay = w[j]; bx, by = w[j + 1]
                    vx, vy = bx - ax, by - ay
                    L2 = vx * vx + vy * vy or 1e-9
                    t = max(0, min(1, ((x - ax) * vx + (y - ay) * vy) / L2))
                    if math.hypot(x - (ax + vx * t), y - (ay + vy * t)) < dmin:
                        return True
            return False

        hu = 0
        for gx in range(-62, -40, 4):
            for gy in range(0, 17, 5):
                px_, py_ = gx + (gy % 10) * 0.3, gy + (gx % 8) * 0.2
                if (near_corr(px_, py_, 2.6) or near_metro_pt(px_, py_) or near_pipe(px_, py_)
                        or in_bld_any(px_, py_, 0.8, 0.0)):
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
                px_, py_ = d['cx'] + 0.8, d['cy'] - 0.5   # CR-1 (V-058): chequeo en posicion FINAL
                if not near_corr(px_, py_, 2.4) and not metro_bad(px_, py_, 0.4):
                    place(f, ids, 'VEG2_TROPICAL', px_, py_, 0, tr * 0.7)
                    sc.inst('VEG2_TROPICAL', px_, py_, 0, tr * 0.7)
                    tr += 1
        dm2 = m['estructura_principal']['dome']
        for k in range(3):
            a = 2 * math.pi * k / 3 + 0.8
            px_, py_ = dm2['cx'] + 3.1 * math.cos(a), dm2['cy'] + 3.1 * math.sin(a)
            if not near_corr(px_, py_, 2.2):
                place(f, ids, 'VEG2_TROPICAL', px_, py_, 0, k * 1.3)
                sc.inst('VEG2_TROPICAL', px_, py_, 0, k * 1.3)
        # VEGETACION BAJA junto a bancos — CR-1 (V-059): la mata sale al lado libre, nunca al corredor
        for b in m['programa']['benches']:
            bp = b['pts']
            for j in range(1, len(bp), 3):
                a0 = bp[max(j - 1, 0)]; b0 = bp[min(j + 1, len(bp) - 1)]
                dxq, dyq = b0[0] - a0[0], b0[1] - a0[1]
                Lq = math.hypot(dxq, dyq) or 1e-9
                for sgn in (1, -1):
                    qx, qy = bp[j][0] - dyq / Lq * 1.15 * sgn, bp[j][1] + dxq / Lq * 1.15 * sgn
                    if not near_corr(qx, qy, 1.5):
                        place(f, ids, 'VEG2_BAJA', qx, qy, 0, qx * 0.1)
                        sc.inst('VEG2_BAJA', qx, qy, 0, qx * 0.1)
                        break
        # COLGANTES bajo los aros de los loops grandes y el borde de la cinta
        for lp in m['estructura_principal']['loops']:
            if lp['id'] not in ('C1-L1', 'C2-L1', 'C3-L1'):
                continue
            z = LOOP_Z[lp['id']]
            lpts, _lf = loop_pts(lp)
            P2 = lpts[:-1]
            for i in range(0, len(P2), max(1, len(P2) // 10)):   # CL-004 +15%, sobre el aro RECORTADO
                px_, py_ = P2[i]
                if _pip(px_, py_, ESTP) or _edge_near(px_, py_, ESTP)[0] < 1.5:
                    continue   # 03B.7-B: dosel ABIERTO sobre la Estacion (altura real ~6 m)
                if any(math.hypot(px_ - d['cx'], py_ - d['cy']) < d['r'] + 0.7
                       and abs(z - d.get('cota', 6)) < 2.6 for d in m['paisaje']['discs']):
                    continue
                place(f, ids, 'VEG2_COLGANTE', px_, py_, z - 0.45, i * 0.07)
                sc.inst('VEG2_COLGANTE', px_, py_, z - 0.45, i * 0.07)
        step_c = max((n - 12) // 5, 1)       # CL-004: colgantes de cinta 4 -> 5, solo en tramos rectos
        for i in range(6, n - 6, step_c):
            if _circum(rib[i - 2], rib[i], rib[i + 2]) < 9.0:
                continue
            q = sideC[i]
            if any(math.hypot(q[0] - d['cx'], q[1] - d['cy']) < d['r'] + 0.7
                   and abs(H['RIBBON'] - d.get('cota', 6)) < 2.9 for d in m['paisaje']['discs']):
                continue
            place(f, ids, 'VEG2_COLGANTE', q[0], q[1], H['RIBBON'] - 0.3, i * 0.1)
            sc.inst('VEG2_COLGANTE', q[0], q[1], H['RIBBON'] - 0.3, i * 0.1)
        for (px, py) in [(-70, -8), (-44, -14), (-20, -16), (2, -16), (26, -18), (48, -16), (-2, 30), (14, 40),
                         (-36, 34), (60, 20), (-86, 2), (34, 4), (10, 4), (-14, 18), (72, -2), (-58, 22),
                         (20, 24), (-30, 6), (40, 8), (52, 26)]:
            place(f, ids, 'PERSON', px, py, 0)
            sc.inst('PERSON', px, py, 0)


# ============================================================ EJECUCION
ALL_BLOCKS = list(BLOCKS.keys())

if __name__ == '__main__':
    # 1) MASTER_ARCHITECTURE_v004 (sin vegetacion full ni personas)
    fM, lM = new_file()
    idsM = register_blocks(fM, lM, ALL_BLOCKS)
    scM = Scene()
    build_site(fM, lM, idsM, scM, full=False)
    okM = fM.Write(os.path.join(HERE, 'MASTER_ARCHITECTURE_v004.3dm'), 8)
    n_guard_master = len(GUARD_LOG)

    # 2) ASSET_LIBRARY_v003 (bloques + un ejemplar en malla)
    fA, lA = new_file()
    idsA = register_blocks(fA, lA, ALL_BLOCKS)
    for i, nm in enumerate(ALL_BLOCKS):
        x, y = (i % 7) * 8.0, (i // 7) * 8.0
        place(fA, idsA, nm, x, y, 0)
        dot = r3.TextDot(nm, r3.Point3d(x, y - 2.5, 0))
        a = r3.ObjectAttributes(); a.LayerIndex = lA['30_CURVES']
        fA.Objects.Add(dot, a)
    okA = fA.Write(os.path.join(HERE, 'ASSET_LIBRARY_v003.3dm'), 8)

    # 3) SOL_FULL_SCENE_v003 (todo) — tambien es la base de presentacion
    fF, lF = new_file()
    idsF = register_blocks(fF, lF, ALL_BLOCKS)
    scF = Scene()
    build_site(fF, lF, idsF, scF, full=True)
    okF = fF.Write(os.path.join(HERE, 'SOL_FULL_SCENE_v003.3dm'), 8)
    # 4) SOL_PRESENTATION_MASTER_v002: escena completa consolidada como entrada de presentacion
    okP = fF.Write(os.path.join(HERE, 'SOL_PRESENTATION_MASTER_v002.3dm'), 8)

    # 5) escena para visor + registro del conflict_guard
    os.makedirs(os.path.join(HERE, '_viewer'), exist_ok=True)
    with open(os.path.join(HERE, '_viewer', 'scene_full.js'), 'w', encoding='utf-8') as fp:
        fp.write('const SCENE_MESHES = ')
        json.dump(scF.meshes, fp, separators=(',', ':'))
        fp.write(';\nconst SCENE_LINES = ')
        json.dump(scF.lines, fp, separators=(',', ':'))
        fp.write(';\n')
    with open(os.path.join(HERE, '_guard_log.json'), 'w', encoding='utf-8') as fp:
        json.dump({'nota': 'entradas duplicadas: build master (hasta idx %d) + build full' % n_guard_master,
                   'ajustes': GUARD_LOG}, fp, ensure_ascii=False, indent=1)

    tris = sum(len(o['F']) for o in scF.meshes)
    print('MASTER:', okM, '· ASSETS:', okA, '· FULL:', okF, '· PRES:', okP)
    print('bloques:', len(ALL_BLOCKS), '· escena full: %d mallas, %d lineas, %d tris' % (len(scF.meshes), len(scF.lines), tris))
    print('guard: %d ajustes registrados' % len(GUARD_LOG))
