# -*- coding: utf-8 -*-
"""
FASE 03B.7 â€” constructor integral v004 (rama sobre v003; nada aprobado se sobrescribe).
03B.8 Â· Genera: MASTER_ARCHITECTURE_v006.3dm Â· ASSET_LIBRARY_v005.3dm Â· SOL_FULL_SCENE_v005.3dm
        Â· SOL_PRESENTATION_MASTER_v004.3dm + _viewer/scene_full.js
Fuente XY: geometria_maestra_v006.json.
Reglas NUEVAS v004 (URBAN_CONFLICTS_v003.json â€” causa raiz: ninguna regla conocia los edificios):
  Â· EDGE_GUARD: poligonos reales de 33 manzanas + 3 kioscos/estancos + Estacion de Cercanias (106);
    nada del proyecto los penetra; el empuje es tangente a la fachada mas cercana
  Â· loops RECORTADOS: la elipse se aplana contra la fachada (portico-galeria contra El Corte Ingles)
  Â· cinta PROYECTADA fuera de fachadas + perfil de anchura (belvedere sobre la Estacion)
  Â· tren T-O regenerado como tren-portico sobre el arco aplanado
  Â· figura espacial B: atrio de la Estacion, media luna de Carmen, aprons de estancos
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

m = json.load(open(os.path.join(HERE, 'geometria_maestra_v006.json'), encoding='utf-8'))
rng = random.Random(31)

H = dict(SEAT=0.45, BACK=0.85, PLANTER=0.60, CURB=0.60, BRANCH=3.0, MIST=4.0, LOW=5.0,
         RIBBON=6.0, MID=6.75, HIGH=8.5, TANK=10.5, GTANK=1.35)
LOOP_Z = {'C1-L1': 10.0, 'C1-L2': 8.0, 'C1-L3': 8.0, 'C2-L1': 11.0, 'C2-L2': 9.0,
          'C2-L3': 7.5, 'C3-L1': 10.0, 'C3-L2': 8.5}

# ==================== 03B.6 Â· CONFLICT_GUARD (CR-1/7/8): chequeos cruzados en posicion FINAL ====================
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


# ==================== 03B.7 Â· EDGE_GUARD: los BORDES CONSTRUIDOS entran en la regla ====================
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
    # 03B.8 D-30/D-33 Â· TIESTO v2: vaso con espesor, borde, tierra, collarin del fuste,
    # mechinales y acometida de riego â€” no un cilindro con dardos.
    parts = [('04_MASTS', mk.cylinder((0, 0, 0), (0, 0, H['BRANCH']), 0.12, 9))]
    parts.append(('09_PLANTERS', mk.cylinder((0, 0, 0), (0, 0, 0.55), 0.80, 14)))       # vaso exterior
    parts.append(('09_PLANTERS', mk.torus((0, 0, 0.55), 0.765, 0.045, 16, 6)))          # borde/labio
    parts.append(('19_DETALLE', mk.cylinder((0, 0, 0.470), (0, 0, 0.505), 0.72, 14)))   # tierra/sustrato
    parts.append(('19_DETALLE', mk.cylinder((0, 0, 0.505), (0, 0, 0.62), 0.19, 10)))    # collarin del fuste
    for a9 in (0.4, 2.49, 4.59):                                                        # mechinales
        parts.append(('13_PIPES', mk.cylinder((0.78 * math.cos(a9), 0.78 * math.sin(a9), 0.06),
                                              (0.86 * math.cos(a9), 0.86 * math.sin(a9), 0.045), 0.018, 4)))
    parts.append(('13_PIPES', mk.cylinder((0.145, 0, 0.62), (0.42, 0, 0.52), 0.016, 4)))  # gotero al sustrato
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
    """min_base (CR-5): poda de formacion â€” ninguna esfera de copa baja de esa cota (V-025)."""
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
    # 03B.8 D-05: la "bola de niebla" volumetrica NO es geometria del master (era el diamante
    # cian flotante de las capturas). El poste lleva CABEZAL real: anillo de boquillas.
    return [('13_PIPES', mk.cylinder((0, 0, 0), (0, 0, H['MIST']), 0.045, 6)),
            ('13_PIPES', mk.sphere((0, 0, H['MIST']), 0.10, 6, 4)),
            ('19_DETALLE', mk.torus((0, 0, H['MIST'] - 0.07), 0.085, 0.02, 10, 4)),
            ('19_DETALLE', mk.cylinder((0.085, 0, H['MIST'] - 0.07), (0.13, 0, H['MIST'] - 0.09), 0.014, 4)),
            ('19_DETALLE', mk.cylinder((-0.085, 0, H['MIST'] - 0.07), (-0.13, 0, H['MIST'] - 0.09), 0.014, 4)),
            ('19_DETALLE', mk.cylinder((0, 0.085, H['MIST'] - 0.07), (0, 0.13, H['MIST'] - 0.09), 0.014, 4)),
            ('19_DETALLE', mk.cylinder((0, -0.085, H['MIST'] - 0.07), (0, -0.13, H['MIST'] - 0.09), 0.014, 4))]


def totem():
    return [('10_FURNITURE', mk.box((0, 0, 0), 0.45, 0.14, 1.35)),
            ('13_PIPES', mk.sphere((0, 0.0, 1.42), 0.06, 5, 4))]


def _viga(p0, p1, w, h):
    """viga-cajon inclinada entre dos puntos (seccion w x h, canto hacia abajo)."""
    (x0, y0, z0), (x1, y1, z1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    Lh = math.hypot(dx, dy) or 1e-9
    hx, hy = -dy / Lh * w / 2, dx / Lh * w / 2
    V = []
    for (px, py, pz) in (p0, p1):
        for sh in (1, -1):
            for sv in (0.0, -h):
                V.append((px + hx * sh, py + hy * sh, pz + sv))
    F = [(0, 1, 3), (0, 3, 2), (4, 7, 5), (4, 6, 7), (0, 2, 6), (0, 6, 4),
         (1, 5, 7), (1, 7, 3), (0, 4, 5), (0, 5, 1), (2, 3, 7), (2, 7, 6)]
    return (V, F)


def stair_switchback():
    """03B.8 Â§5 v3 â€” LA ESCALERA COMO UNA PIEZA (D-01/21/22/23/40/41):
    zancas-VIGA continuas (no chapas sueltas), meseta con vigas de borde y 2 apoyos, dado de
    arranque, barandilla CONTINUA arranque->meseta->tramo B con jog en el pozo y remates, y
    pasarela de embarque con vigas, mensulas al poste y junta contra el tablero.
    Local: tramo A en y=0 sube hacia +x; meseta al este; tramo B en y=-1.55 vuelve subiendo."""
    CH, HU, W = 6.0 / 35, 0.29, 1.4
    XA = -2.6
    xa = XA + 18 * HU              # 2.62 fin tramo A (z 3.086)
    xb = xa - 17 * HU              # -2.31 llegada a +6.00
    zm = 18 * CH
    parts = []
    for k in range(18):
        parts.append(('03_SECONDARY_STRUCTURE', mk.box((XA + HU * (k + 0.5), 0, CH * (k + 1) - 0.025), HU + 0.02, W, 0.05)))
    parts.append(('03_SECONDARY_STRUCTURE', mk.box((xa + 0.75, -0.775, zm - 0.025), 1.5, 2.95, 0.05)))
    for k in range(17):
        parts.append(('03_SECONDARY_STRUCTURE', mk.box((xa - HU * (k + 0.5), -1.55, CH * (19 + k) - 0.025), HU + 0.02, W, 0.05)))
    # ---- zancas-viga continuas por AMBOS bordes de AMBOS tramos + bordes de meseta
    for y0 in (-0.68, 0.68):
        parts.append(('02_PRIMARY_STRUCTURE', _viga((XA, y0, 0.04), (xa, y0, zm + 0.02), 0.09, 0.37)))
    for y0 in (-2.23, -0.87):
        parts.append(('02_PRIMARY_STRUCTURE', _viga((xa, y0, zm + 0.02), (xb, y0, 6.02), 0.09, 0.37)))
    for (pa, pb) in (((xa, 0.68, zm + 0.02), (xa + 1.46, 0.68, zm + 0.02)),
                     ((xa + 1.46, 0.68, zm + 0.02), (xa + 1.46, -2.23, zm + 0.02)),
                     ((xa + 1.46, -2.23, zm + 0.02), (xa, -2.23, zm + 0.02))):
        parts.append(('02_PRIMARY_STRUCTURE', _viga(pa, pb, 0.09, 0.30)))
    # ---- apoyos: dado de arranque + 2 pies de meseta con placa + poste de cabeza
    parts.append(('03_SECONDARY_STRUCTURE', mk.box((XA - 0.22, 0, 0.10), 0.5, 1.55, 0.20)))   # dado arranque
    for (px9, py9) in ((xa + 0.75, -0.775), (xa + 1.32, -2.05)):
        parts.append(('04_MASTS', mk.cylinder((px9, py9, 0), (px9, py9, zm - 0.05), 0.12, 8)))
        parts.append(('19_DETALLE', mk.cylinder((px9, py9, 0), (px9, py9, 0.03), 0.24, 10)))
    parts.append(('04_MASTS', mk.cylinder((xb, -1.55, 0), (xb, -1.55, 5.95), 0.13, 8)))
    parts.append(('19_DETALLE', mk.cylinder((xb, -1.55, 0), (xb, -1.55, 0.03), 0.26, 10)))
    # cierre macizo bajo el tramo A (almacen/jardinera): ninguna celda pisable con galibo <2.50
    parts.append(('03_SECONDARY_STRUCTURE', mk.box((-0.03, 0, 0.45), 5.15, 1.5, 0.9)))
    # ---- pasarela de embarque: losa + vigas de borde + mensulas al poste + junta al tablero
    parts.append(('03_SECONDARY_STRUCTURE', mk.box((xb - 0.1, -2.6, 5.97), 1.4, 0.9, 0.06)))
    for y0 in (-2.17, -3.03):
        parts.append(('02_PRIMARY_STRUCTURE', _viga((xb - 0.78, y0, 6.0), (xb + 0.58, y0, 6.0), 0.08, 0.24)))
    for sx9 in (-0.55, 0.35):
        parts.append(('03_SECONDARY_STRUCTURE', _viga((xb, -1.62, 5.80), (xb + sx9, -2.95, 5.96), 0.06, 0.10)))
    parts.append(('19_DETALLE', mk.box((xb - 0.1, -3.02, 6.012), 1.4, 0.10, 0.030)))          # junta con el tablero (sobre las juntas de tabla)
    # ---- barandilla CONTINUA (montantes desde huella + pasamanos como polilinea unica por lado)
    def _rail_path(lado):
        pts = []
        if lado == 'ext':                      # arranque A (+y) -> meseta este -> tramo B (-y) -> pasarela
            for k in range(0, 19, 2):
                pts.append((XA + HU * k, 0.68, CH * k + 0.96))
            pts += [(xa + 1.38, 0.68, zm + 0.96), (xa + 1.38, -2.23, zm + 0.96)]
            for k in range(0, 18, 2):
                pts.append((xa - HU * k, -2.23, CH * (18 + k) + 0.96))
            pts += [(xb - 0.72, -2.23, 6.96 - 0.96 + 0.96)]
        else:                                  # lado del POZO: A interior -> jog -> B interior
            for k in range(0, 19, 2):
                pts.append((XA + HU * k, -0.68, CH * k + 0.96))
            pts += [(xa + 0.12, -0.68, zm + 0.96), (xa + 0.12, -0.87, zm + 0.96)]
            for k in range(0, 18, 2):
                pts.append((xa - HU * k, -0.87, CH * (18 + k) + 0.96))
            pts += [(xb - 0.72, -0.87, 6.96)]
        return pts

    for lado in ('ext', 'int'):
        path = _rail_path(lado)
        parts.append(('03_SECONDARY_STRUCTURE', mk.tube(path, 0.030, 6)))                     # pasamanos
        parts.append(('03_SECONDARY_STRUCTURE', mk.tube([(p[0], p[1], p[2] - 0.34) for p in path], 0.022, 5)))
        for p in path[::2]:
            parts.append(('03_SECONDARY_STRUCTURE', mk.cylinder((p[0], p[1], p[2] - 0.94), (p[0], p[1], p[2]), 0.024, 5)))
        p0, p1 = path[0], path[1]
        L0 = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) or 1e-9
        ux0, uy0 = (p0[0] - p1[0]) / L0, (p0[1] - p1[1]) / L0
        parts.append(('03_SECONDARY_STRUCTURE', mk.tube([(p0[0], p0[1], p0[2]),
                                                         (p0[0] + ux0 * 0.10, p0[1] + uy0 * 0.10, p0[2] - 0.16),
                                                         (p0[0] + ux0 * 0.12, p0[1] + uy0 * 0.12, p0[2] - 0.40),
                                                         (p0[0] + ux0 * 0.06, p0[1] + uy0 * 0.06, p0[2] - 0.60)],
                                                        0.028, 5)))                            # remate de arranque
    return parts


def lift_tower():
    """CR-3b: ASCENSOR-CAPSULA â€” fuste cilindrico transparente + cabina POD rosa + pasarela al tablero (-y)."""
    parts = [('06_MEMBRANES', mk.cylinder((0, 0, 0), (0, 0, 7.4), 1.2, 18))]
    for zz in (0.1, 3.0, 6.0, 7.35):
        parts.append(('03_SECONDARY_STRUCTURE', mk.torus((0, 0, zz), 1.2, 0.05, 16, 5)))
    for adeg in (0, 90, 180, 270):
        a = math.radians(adeg)
        parts.append(('03_SECONDARY_STRUCTURE', mk.cylinder((1.2 * math.cos(a), 1.2 * math.sin(a), 0),
                                                            (1.2 * math.cos(a), 1.2 * math.sin(a), 7.4), 0.06, 6)))
    parts.append(('08_PINK_MODULES', mk.cylinder((0, 0, 0.15), (0, 0, 2.35), 0.95, 14)))
    parts.append(('08_PINK_MODULES', mk.sphere((0, 0, 2.35), 0.95, 12, 6)))
    # 03B.8 Â§15 Â· embarques REALES: losa + umbral + rampa de acceso en ambas cotas
    parts.append(('03_SECONDARY_STRUCTURE', mk.box((0, -1.7, 5.97), 1.3, 1.3, 0.06)))       # pasarela +6.00
    parts.append(('19_DETALLE', mk.box((0, -1.18, 6.028), 1.25, 0.12, 0.018)))              # umbral superior
    parts.append(('19_DETALLE', mk.box((0, 1.24, 0.012), 1.25, 0.34, 0.024)))               # umbral/rampa inferior
    parts.append(('02_PRIMARY_STRUCTURE', _viga((0.55, -1.62, 5.99), (0.55, -2.30, 5.99), 0.07, 0.20)))
    parts.append(('02_PRIMARY_STRUCTURE', _viga((-0.55, -1.62, 5.99), (-0.55, -2.30, 5.99), 0.07, 0.20)))
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
    # E02 â€” biblioteca vegetal por roles
    'VEG2_ARBOL_A': veg2_arbol('A'), 'VEG2_ARBOL_B': veg2_arbol('B'), 'VEG2_ARBOL_EX': veg2_arbol('EX'),
    'VEG2_TREPADORA': veg2_trepadora(), 'VEG2_BAJA': veg2_baja(), 'VEG2_TROPICAL': veg2_tropical(),
    'VEG2_HUERTO': veg2_huerto(), 'VEG2_ACUATICA': veg2_acuatica(), 'VEG2_COLGANTE': veg2_colgante(),
}
BLOCKS.update(_BLOCKS_LEGACY)

# ==================== 03B.7 Â§6-Â§17 Â· DETAILING LOD B/C de las familias ====================
import detailing_03b9 as DET  # noqa: E402

_det_delta = DET.upgrade_blocks(BLOCKS, mk, rng)

# ==================== 03B.8 Â§7-Â§9 Â· VEGETACION REAL: assets externos (CC0/CC-BY) con 3 LOD ====
# Fuente y licencias: _assets_veg/provenance.json + ASSET_PROVENANCE.csv. Conversion: veg_assets.py.
VEG_ROLES = {}
try:
    with open(os.path.join(HERE, '_veg_blocks.json'), encoding='utf-8') as _fvb:
        _VB = json.load(_fvb)
    # 03B.9 §2: VARIANTES anti-clon horneadas por rol+LOD — espejo, escala joven (0.86) y
    # ejemplar maduro (1.12): ninguna planta se repite identica al lado de su gemela.
    def _var_veg(piezas, mirror=False, s=1.0):
        out = []
        for p in piezas:
            V2 = [[(-v[0] if mirror else v[0]) * s, v[1] * s, v[2] * s] for v in p[1]]
            F2 = [tuple(reversed(ff)) if mirror else tuple(ff) for ff in p[2]]
            out.append((p[0], (V2, F2)))
        return out

    for _rol, _dd in _VB.items():
        for _lodk, _suf in (('hero', 'H'), ('mid', 'M'), ('far', 'F')):
            base = _dd[_lodk]
            BLOCKS['VEGA_%s_%s' % (_rol, _suf)] = _var_veg(base)
            BLOCKS['VEGA_%s_%s_B' % (_rol, _suf)] = _var_veg(base, mirror=True)
            BLOCKS['VEGA_%s_%s_C' % (_rol, _suf)] = _var_veg(base, s=0.86)
            if _suf == 'H':
                BLOCKS['VEGA_%s_%s_D' % (_rol, _suf)] = _var_veg(base, mirror=True, s=1.12)
        VEG_ROLES[_rol] = _dd['alto']
    print('veg assets: %d roles x 3 LOD x variantes registrados' % len(_VB))
except Exception as _e:
    print('AVISO veg assets no cargados:', repr(_e))


def lod_veg(x, y):
    """HERO en el corazon de la plaza (primeros planos), MID en el ambito, FAR en el perimetro."""
    d = math.hypot(x - 0.0, y - 5.0)
    return 'H' if d < 14.0 else ('M' if d < 62.0 else 'F')


def _blk_reach(name):
    """Alcance horizontal REAL del bloque (max |xy| de sus vertices) â€” la guarda usa esto, no constantes."""
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
    try:   # 03B.7 Â§24: metadatos para la futura auditoria municipal
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


_PLACED = set()   # 03B.8 Â§3: dedupe central â€” una instancia EXACTAMENTE repetida es un ERROR, no diseÃ±o


def place(f, ids, name, x, y, z, rot=0.0, lidx=None):
    key = (id(f), name, round(x, 2), round(y, 2), round(z, 2), round(rot, 3))
    if key in _PLACED:
        GUARD_LOG.append({'tag': name, 'regla': 'instancia-duplicada-suprimida',
                          'xy': [round(x, 1), round(y, 1)]})
        return
    _PLACED.add(key)
    tr = r3.Transform.Translation(x, y, z)
    if rot:
        tr = r3.Transform.Multiply(tr, r3.Transform.Rotation(rot, r3.Vector3d(0, 0, 1), r3.Point3d(0, 0, 0)))
    ir = r3.InstanceReference(ids[name], tr)
    a = r3.ObjectAttributes(); a.Name = name
    try:
        a.SetUserString('familia', name)
        a.SetUserString('version', 'v006')
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
    # 03B.7-C: grupo ecuestre COHERENTE â€” la peana APOYA en la grada (v003 la dejaba levitar
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
    # 03B.8 D-42: la franja de respeto r8 es un DATO de auditoria (DEC-0006), no un circulo
    # dibujado en el suelo del master â€” fuera de la geometria entregable.
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
        Devuelve (pts_cerrados, mascara_plana) â€” la mascara marca el arco-portico contra ECI."""
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

    # 03B.8 (S08/S11 Â· D-17/D-34 y 215 duplicados medidos): el clip/empuje AMONTONA puntos del
    # eje en los tramos pegados a fachada -> postes apilados, tubos degenerados y "tres filas"
    # de barandilla. RE-MUESTREO a paso uniforme: la densidad del eje deja de depender de la
    # historia de empujes.
    def _resample_axis(P, paso=0.65):
        pts = [P[0]]
        for q in P[1:]:
            if math.hypot(q[0] - pts[-1][0], q[1] - pts[-1][1]) > 1e-6:
                pts.append(q)
        cerrado = math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) < 1.5
        if cerrado:
            pts.append(pts[0])
        d = [0.0]
        for k in range(1, len(pts)):
            d.append(d[-1] + math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1]))
        L = d[-1]
        nn = max(24, int(round(L / paso)))
        out = []
        j = 0
        for k in range(nn):
            s = L * k / nn if cerrado else L * k / (nn - 1)
            while j < len(d) - 2 and d[j + 1] < s:
                j += 1
            t = (s - d[j]) / ((d[j + 1] - d[j]) or 1e-9)
            out.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * t,
                        pts[j][1] + (pts[j + 1][1] - pts[j][1]) * t))
        return out

    rib = _resample_axis(rib, 0.65)
    rib = _push_edificios(rib)      # las cuerdas del resample cortan la esquina concava: re-empuje
    rib = _resample_axis(rib, 0.65)
    rib = _push_edificios(rib)
    rib = _resample_axis(rib, 0.65)   # SIEMPRE terminar re-muestreado: el empuje APILA en esquinas

    def _out_pt(p9):
        """empuje PUNTUAL final (normal de arista, sin sesgo-plaza): filetea la esquina concava
        sin apilar â€” la cuerda del resample cortaba hasta 1.1 m el angulo de ECI."""
        x9, y9 = p9
        mgc9 = URB['margen_edificio']['cinta']
        mge9 = URB['margen_estacion']['cinta']
        for _ in range(3):
            best = None
            for (poly, mg9) in [(p8, mgc9) for p8 in GBLD] + [(ESTP, mge9)]:
                d9, qx9, qy9 = _edge_near(x9, y9, poly)
                ins = _pip(x9, y9, poly)
                pen = (mg9 + d9) if ins else (mg9 - d9)
                if pen > 0.01 and (best is None or pen > best[0]):
                    best = (pen, qx9, qy9, ins, mg9)
            if best is None:
                return (x9, y9)
            _pen, qx9, qy9, ins, mg9 = best
            L9 = math.hypot(x9 - qx9, y9 - qy9) or 1e-9
            s9 = -1.0 if ins else 1.0
            x9 = qx9 + (x9 - qx9) / L9 * s9 * (mg9 + 0.02)
            y9 = qy9 + (y9 - qy9) / L9 * s9 * (mg9 + 0.02)
        return (x9, y9)

    rib = [_out_pt(p) for p in rib]
    _rmin = min_radius(rib)
    GUARD_LOG.append({'tag': 'RIBBON', 'regla': 'radio-final+resample-0.65', 'r_min': round(_rmin, 2),
                      'n_puntos': len(rib)})
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

    SUPS_XY = []      # 03B.9: posiciones FINALES de soportes de cinta (guarda para mastiles)
    GAPS = {1: set(), -1: set()}
    anchors = []
    for (sx, sy) in m['circulacion']['stairs']:
        i, s = anchor(sx, sy, (-2.4, -0.8, 0.8, 2.4, 4.0), 2.8, 3.4, 'STAIR@%.0f,%.0f' % (sx, sy))
        if i is None:
            continue
        anchors.append(('STAIR_SB', i, s))
        for k in range(i - 2, i + 3):
            GAPS[s].add(k % n)
    for (tx0, ty0) in [(-75, 10), (5, 30), (72, 8)]:   # C1-oeste Â· C2-norte Â· C3-este
        i, s = anchor(tx0, ty0, (0.0,), 2.9, 3.2, 'LIFT@%d,%d' % (tx0, ty0))
        if i is None:
            continue
        anchors.append(('LIFT_TOWER', i, s))
        for k in range(i - 1, i + 2):
            GAPS[s].add(k % n)

    # 03B.8 Â§6 Â· BARANDILLA v2: pasamanos 1.05 + travesano 0.55 + rodapie 0.10, huecos de embarque,
    # y REMATES REALES: ningun rail nace ni muere en el aire (D-02/D-20/D-23). Cada tramo abierto
    # termina en montante final + gancho pasamanos->travesano; los fragmentos <1.6 m se descartan.
    def _rail_run(seg, cerrado):
        z0 = H['RIBBON']
        if len(seg) < 3:
            return
        L_seg = sum(math.hypot(seg[k + 1][0] - seg[k][0], seg[k + 1][1] - seg[k][1])
                    for k in range(len(seg) - 1))
        if not cerrado and L_seg < 1.6:
            GUARD_LOG.append({'tag': 'RAIL', 'regla': 'fragmento-descartado', 'L': round(L_seg, 2)})
            return
        pts_c = seg + ([seg[0]] if cerrado else [])
        for (hh, rr) in ((1.05, 0.045), (0.55, 0.032), (0.10, 0.03)):
            rail = mk.tube([(q[0], q[1], z0 + hh) for q in pts_c], rr, 6)
            add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'RIBBON_RAIL', rail)
            sc.mesh('03_SECONDARY_STRUCTURE', rail)
        postes = seg[::2]
        if not cerrado:   # 03B.9: el montante FINAL ya lo pone el remate — sin duplicar en extremos
            postes = [q for q in postes if q is not seg[0] and q is not seg[-1]]
        vistos_bp = set()   # 03B.9: el offset PLEGADO en la concava de la Estacion apilaba postes
        for q in postes:
            kbp = (round(q[0], 2), round(q[1], 2))
            if kbp in vistos_bp:
                continue
            vistos_bp.add(kbp)
            bp = mk.cylinder((q[0], q[1], z0), (q[0], q[1], z0 + 1.05), 0.028, 5)
            add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'BALPOST', bp)
            sc.mesh('03_SECONDARY_STRUCTURE', bp)
            pl = mk.box((q[0], q[1], z0 + 0.002), 0.11, 0.11, 0.012)
            add_mesh(f, lidx, '19_DETALLE', 'BALPOST_PLETINA', pl)
            sc.mesh('19_DETALLE', pl)
        if not cerrado:
            for (ex_, ey_, nx_, ny_) in ((seg[0][0], seg[0][1],
                                          seg[0][0] - seg[1][0], seg[0][1] - seg[1][1]),
                                         (seg[-1][0], seg[-1][1],
                                          seg[-1][0] - seg[-2][0], seg[-1][1] - seg[-2][1])):
                Ln = math.hypot(nx_, ny_) or 1e-9
                ux_, uy_ = nx_ / Ln, ny_ / Ln
                ep = mk.cylinder((ex_, ey_, z0), (ex_, ey_, z0 + 1.05), 0.034, 6)   # montante final
                add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'BALPOST_FIN', ep)
                sc.mesh('03_SECONDARY_STRUCTURE', ep)
                gancho = mk.tube([(ex_, ey_, z0 + 1.05),
                                  (ex_ + ux_ * 0.10, ey_ + uy_ * 0.10, z0 + 0.97),
                                  (ex_ + ux_ * 0.14, ey_ + uy_ * 0.14, z0 + 0.80),
                                  (ex_ + ux_ * 0.10, ey_ + uy_ * 0.10, z0 + 0.62),
                                  (ex_, ey_, z0 + 0.55)], 0.040, 6)                 # retorno al travesano
                add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'RAIL_REMATE', gancho)
                sc.mesh('03_SECONDARY_STRUCTURE', gancho)
                plf = mk.box((ex_, ey_, z0 + 0.002), 0.13, 0.13, 0.014)
                add_mesh(f, lidx, '19_DETALLE', 'BALPOST_PLETINA', plf)
                sc.mesh('19_DETALLE', plf)

    for sgn in (1, -1):
        side = sideP if sgn > 0 else sideN
        if not GAPS[sgn]:
            _rail_run(side, cerrado=True)
            continue
        runs, cur = [], []
        for i in range(n):
            if i in GAPS[sgn]:
                if len(cur) > 2:
                    runs.append(cur)
                cur = []
            else:
                cur.append(side[i])
        if len(cur) > 2:
            if runs and 0 not in GAPS[sgn] and (n - 1) not in GAPS[sgn]:
                runs[0] = cur + runs[0]      # el circuito es cerrado: une el final con el principio
            else:
                runs.append(cur)
        for seg in runs:
            _rail_run(seg, cerrado=False)
    # nebulizadores de barandilla (CL-004): posts con BOQUILLA real; la niebla volumetrica es del
    # render (scene_extra), no del master (D-05/D-38: fuera bolas cian flotantes del modelo)
    for i in range(n // 16, n - 1, max(n // 8, 1)):
        q = sideM[i]
        nbp = mk.cylinder((q[0], q[1], H['RIBBON']), (q[0], q[1], H['RIBBON'] + 1.35), 0.03, 5)
        add_mesh(f, lidx, '13_PIPES', 'RIBNEB', nbp)
        sc.mesh('13_PIPES', nbp)
        tip = mk.cylinder((q[0], q[1], H['RIBBON'] + 1.35), (q[0], q[1], H['RIBBON'] + 1.43), 0.055, 8)
        add_mesh(f, lidx, '19_DETALLE', 'RIBNEB_BOQUILLA', tip)
        sc.mesh('19_DETALLE', tip)
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
            SUPS_XY.append((rib[i][0], rib[i][1]))
            # 03B.8 D-06: NUDO cabeza-tablero (placa de transferencia + placa base con pernos)
            nud = mk.box((rib[i][0], rib[i][1], H['RIBBON'] - 0.275), 0.62, 0.62, 0.055)
            add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'SUP_NUDO', nud)
            sc.mesh('03_SECONDARY_STRUCTURE', nud)
            pb = mk.cylinder((rib[i][0], rib[i][1], 0), (rib[i][0], rib[i][1], 0.035), 0.34, 10)
            add_mesh(f, lidx, '19_DETALLE', 'SUP_PLACA', pb)
            sc.mesh('19_DETALLE', pb)
            for a6 in (0.6, 2.17, 3.74, 5.31):
                pn = mk.cylinder((rib[i][0] + 0.26 * math.cos(a6), rib[i][1] + 0.26 * math.sin(a6), 0.035),
                                 (rib[i][0] + 0.26 * math.cos(a6), rib[i][1] + 0.26 * math.sin(a6), 0.075), 0.02, 5)
                add_mesh(f, lidx, '19_DETALLE', 'SUP_PERNO', pn)
                sc.mesh('19_DETALLE', pn)
            acc = 0.0
    # 03B.8 D-03/10/19/37 Â· CABLE con lectura constructiva: tubo con FLECHA (catenaria aprox),
    # anclaje en AMBOS extremos (orejeta + casquillo) y regla dura: un tensor jamas cruza el
    # volumen peatonal del tablero (la "varilla que atraviesa la plataforma" de S11).
    def emit_cable(p0, p1, nombre):
        span = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        for t in (0.15, 0.35, 0.5, 0.65, 0.85):
            qx = p0[0] + (p1[0] - p0[0]) * t
            qy = p0[1] + (p1[1] - p0[1]) * t
            qz = p0[2] + (p1[2] - p0[2]) * t
            dmin2 = min((qx - r0[0]) ** 2 + (qy - r0[1]) ** 2 for r0 in rib[::3])
            if dmin2 < (2.1) ** 2 and (H['RIBBON'] - 0.25) < qz < (H['RIBBON'] + 2.2):
                GUARD_LOG.append({'tag': nombre, 'regla': 'cable-cruza-tablero-descartado',
                                  'xy': [round(qx, 1), round(qy, 1)]})
                return False
        sag = min(0.35, 0.045 * span)
        pts = []
        for k in range(7):
            t = k / 6
            pts.append((p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t,
                        p0[2] + (p1[2] - p0[2]) * t - sag * 4 * t * (1 - t)))
        cb = mk.tube(pts, 0.016, 5)
        add_mesh(f, lidx, '05_CABLES', nombre, cb)
        sc.mesh('05_CABLES', cb)
        # 03B.9 §12: TERMINALES reales en ambos extremos — casquillo + en el extremo BAJO
        # ademas tensor de cuerpo hexagonal y horquilla con pasador (detalle 1:5 posible)
        ext = sorted(((p0[0], p0[1], p0[2], p1[0], p1[1], p1[2]),
                      (p1[0], p1[1], p1[2], p0[0], p0[1], p0[2])), key=lambda e: e[2])
        for j9, (ex9, ey9, ez9, ox9, oy9, oz9) in enumerate(ext):
            L9 = math.sqrt((ox9 - ex9) ** 2 + (oy9 - ey9) ** 2 + (oz9 - ez9) ** 2) or 1e-9
            ux9, uy9, uz9 = (ox9 - ex9) / L9, (oy9 - ey9) / L9, (oz9 - ez9) / L9
            csq = mk.cylinder((ex9, ey9, ez9), (ex9 + ux9 * 0.12, ey9 + uy9 * 0.12, ez9 + uz9 * 0.12), 0.033, 6)
            add_mesh(f, lidx, '19_DETALLE', nombre + '_ANCLA', csq)
            sc.mesh('19_DETALLE', csq)
            if j9 == 0:   # extremo bajo: tensor + horquilla + pasador
                t0 = (ex9 + ux9 * 0.16, ey9 + uy9 * 0.16, ez9 + uz9 * 0.16)
                t1 = (ex9 + ux9 * 0.40, ey9 + uy9 * 0.40, ez9 + uz9 * 0.40)
                tb = mk.cylinder(t0, t1, 0.028, 6)
                add_mesh(f, lidx, '19_DETALLE', nombre + '_TENSOR', tb)
                sc.mesh('19_DETALLE', tb)
                hx9, hy9 = -uy9, ux9
                Lh9 = math.hypot(hx9, hy9) or 1e-9
                hx9, hy9 = hx9 / Lh9, hy9 / Lh9
                for s9 in (0.035, -0.035):
                    pl9 = mk.cylinder((ex9 + hx9 * s9, ey9 + hy9 * s9, ez9),
                                      (ex9 + ux9 * 0.10 + hx9 * s9, ey9 + uy9 * 0.10 + hy9 * s9,
                                       ez9 + uz9 * 0.10), 0.012, 4)
                    add_mesh(f, lidx, '19_DETALLE', nombre + '_HORQ', pl9)
                    sc.mesh('19_DETALLE', pl9)
                ps9 = mk.cylinder((ex9 + hx9 * 0.05, ey9 + hy9 * 0.05, ez9 + uz9 * 0.05),
                                  (ex9 - hx9 * 0.05, ey9 - hy9 * 0.05, ez9 + uz9 * 0.05), 0.011, 5)
                add_mesh(f, lidx, '19_DETALLE', nombre + '_PASADOR', ps9)
                sc.mesh('19_DETALLE', ps9)
        return True

    def place_veg(rol, x, y, z=0.0, rot=0.0):
        """03B.9: asset real, LOD por distancia y VARIANTE determinista por posicion
        (espejo/joven/maduro) — rompe la clonacion sin aleatoriedad no reproducible."""
        # 03B.9 §26 (V-001/V-002 RAIZ REAL): ninguna planta frondosa con las FRONDAS sobre un
        # eje declarado (alcance ~0.6-0.9) ni dentro del gálibo del tren
        if rol not in ('NENUFAR', 'JUNCO', 'JUNCO2') and near_corr(x, y, 1.55):
            GUARD_LOG.append({'tag': 'VEG_' + rol, 'regla': 'eje-omitida', 'xy': [round(x, 1), round(y, 1)]})
            return True
        if any(math.hypot(x - qx9, y - qy9) < 3.0 for (qx9, qy9) in TREN_XY):
            GUARD_LOG.append({'tag': 'VEG_' + rol, 'regla': 'tren-omitida', 'xy': [round(x, 1), round(y, 1)]})
            return True
        suf = lod_veg(x, y)
        h9 = int(abs(x * 73.1) + abs(y * 37.7))
        var = ('', '_B', '_C', '_D')[h9 % 4]
        nm9 = 'VEGA_%s_%s%s' % (rol, suf, var)
        if nm9 not in BLOCKS:
            nm9 = 'VEGA_%s_%s' % (rol, suf)
        if nm9 not in BLOCKS:
            return False
        place(f, ids, nm9, x, y, z, rot + (h9 % 7) * 0.83)
        sc.inst(nm9, x, y, z, rot + (h9 % 7) * 0.83)
        return True

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
    # 03B.8: ORDEN correcto de guardas de disco â€” fachada, LUEGO separacion disco-disco, y
    # fachada otra vez (la separacion sola los devolvia contra ECI y viceversa)
    for i, d in enumerate(DISCS):
        cota0 = min(max(d.get('cota', 6.0), 4.2), H['HIGH'])
        g = bld_clear(d['cx'], d['cy'], d['r'] + 0.85, z_base=cota0 - 1.5, tag='DISC_%d' % i)
        if g is not None:
            d['cx'], d['cy'] = g
    for _sep in range(3):
        movido = False
        for i1_ in range(len(DISCS)):
            for i2_ in range(i1_ + 1, len(DISCS)):
                d1, d2 = DISCS[i1_], DISCS[i2_]
                if abs(d1.get('cota', 6) - d2.get('cota', 6)) > 0.3:
                    continue
                dd_ = math.hypot(d2['cx'] - d1['cx'], d2['cy'] - d1['cy'])
                need_ = (d1['r'] + d2['r']) * 0.62
                if 1e-6 < dd_ < need_:
                    ux_, uy_ = (d2['cx'] - d1['cx']) / dd_, (d2['cy'] - d1['cy']) / dd_
                    emp_ = (need_ - dd_) / 2
                    d1['cx'] -= ux_ * emp_; d1['cy'] -= uy_ * emp_
                    d2['cx'] += ux_ * emp_; d2['cy'] += uy_ * emp_
                    movido = True
        if not movido:
            break
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
                emit_cable((px, py, z), (dd['cx'], dd['cy'], cota), 'LCBL')

    # ---- capsulas ----
    # 03B.7-A1 Â· TREN-PORTICO: T-O renace sobre el arco de C1-L1 aplanado contra El Corte Ingles
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
                    Lcap = tp.get('L_capsula', 5.3)   # 03B.8 D-12: el paso usa la LONGITUD real del
                    s_next += (Lcap + 0.30) if seguidas < 3 else (Lcap + 2.15)   # bloque, no el ancho

                    if seguidas >= 3:
                        seguidas = 0
                acc += seg
                k += 1
            GUARD_LOG.append({'tag': 'TREN_PORTICO', 'regla': 'A1', 'capsulas': puestos,
                              'arco_m': round(L_arc, 1)})
    # ---- mastiles (tras el tren: la reubicacion por eje/carmen tambien debe esquivar el TREN) ----
    def _mast_ok(px2, py2):
        """03B.7-D: el mastil (tiesto r0.8) no puede quedar sobre un EJE declarado, la media luna
        de Carmen, el tren-portico ni una capsula â€” el empuje de fachada dejaba varios encima."""
        if near_corr(px2, py2, 2.60):   # 03B.9 §26: cara del tiesto (r0.8) a >=1.8 del eje
            return False
        cl = m['atrio_v004']['carmen']['media_luna_bancos']
        dd = math.hypot(px2 - cl['c'][0], py2 - cl['c'][1])
        ang = math.degrees(math.atan2(py2 - cl['c'][1], px2 - cl['c'][0])) % 360
        if abs(dd - cl['r']) < 1.4 and cl['a0'] <= ang <= cl['a1']:
            return False
        if any(math.hypot(px2 - qx, py2 - qy) < 3.0 for (qx, qy) in TREN_XY):
            return False
        # 03B.9 (V-042): el tiesto (r0.8) tampoco abraza un soporte de cinta (r0.3)
        if any(math.hypot(px2 - sx9, py2 - sy9) < 1.25 for (sx9, sy9) in SUPS_XY):
            return False
        if any(math.hypot(px2 - c2['cx'], py2 - c2['cy']) < max(c2.get('w', 1.8), 1.8) / 2 + 1.9
               for c2 in m['programa']['capsules']):
            return False
        # it.5: dos mastiles reubicados acababan SOLAPADOS en el mismo bolsillo (V-001 canal 0.5 m)
        if any(math.hypot(px2 - ma[0], py2 - ma[1]) < 3.4 for ma in MASTS):
            return False
        # 03B.8: el tiesto (r0.8) no pisa una balsa ni su bordillo
        for p8 in m['agua_clima']['ground_ponds']:
            if p8.get('kind') == 'circle':
                if math.hypot(px2 - p8['cx'], py2 - p8['cy']) < p8['r'] + 1.25:
                    return False
            else:
                pp8 = p8.get('pts', [])
                if pp8:
                    cx8 = sum(q8[0] for q8 in pp8) / len(pp8)
                    cy8 = sum(q8[1] for q8 in pp8) / len(pp8)
                    r8 = max(math.hypot(q8[0] - cx8, q8[1] - cy8) for q8 in pp8)
                    if math.hypot(px2 - cx8, py2 - cy8) < r8 + 1.15:
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
        # 03B.9 §26 (V-001/V-002): las frondas del tiesto alcanzan ~1.2 m — junto a un EJE
        # declarado las plantas se orientan al lado CONTRARIO y se usa especie compacta.
        az_eje = None
        if near_corr(mx, my, 3.1):
            for kk8 in range(12):
                aa8 = kk8 * math.pi / 6
                if near_corr(mx + 1.6 * math.cos(aa8), my + 1.6 * math.sin(aa8), 1.2):
                    az_eje = aa8
                    break
        if az_eje is None:
            duo = ((0.40, rot + 0.7, ('HELECHO', 'CALATHEA', 'GRAMINEA')[i % 3]),
                   (0.36, rot + 3.4, ('GRAMINEA', 'HELECHO', 'CALATHEA')[(i + 1) % 3]))
        else:
            duo = ((0.34, az_eje + math.pi - 0.55, 'GRAMINEA'),
                   (0.30, az_eje + math.pi + 0.55, 'GRAMINEA'))
            GUARD_LOG.append({'tag': 'MAST_PLANTA', 'regla': 'eje-lado-contrario',
                              'xy': [round(mx, 1), round(my, 1)]})
        for (rr9, aa9, rol9) in duo:
            place_veg(rol9, mx + rr9 * math.cos(aa9), my + rr9 * math.sin(aa9), 0.50, aa9 * 1.7)
        for dd in nd:
            cota = min(max(dd.get('cota', 6.0), 4.2), H['HIGH'])
            emit_cable((mx, my, H['BRANCH']), (dd['cx'], dd['cy'], cota), 'CBL')

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
        # Â§14 balsa con sistema legible: aro inferior + gargola-rebosadero + hilo + pendolas
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
            # 03B.9 (V-048): el snap puede clavar el bordillo en un poligono oblicuo (Estacion);
            # bld_clear tiene la ULTIMA palabra (identidad si no hay violacion)
            g2 = bld_clear(g[0], g[1], p['r'] + 0.16, tag='POND_POSTSNAP_%s' % p['id'])
            if g2 is not None:
                g = g2
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
                    px_, py_ = p['cx'] + p['r'] * 0.72 * math.cos(a), p['cy'] + p['r'] * 0.72 * math.sin(a)
                    if not place_veg(('JUNCO', 'JUNCO2')[k % 2], px_, py_, H['CURB'] - 0.12, k * 1.1):
                        place(f, ids, 'VEG2_ACUATICA', px_, py_, H['CURB'] - 0.12, k * 1.1)
                        sc.inst('VEG2_ACUATICA', px_, py_, H['CURB'] - 0.12, k * 1.1)
                # 03B.9 §7 · MICROECOSISTEMA: nenufares en grupos de edades, tallos emergentes,
                # borde de rizoma y juncos a densidades variables — no "agua + 5 hojas"
                for (fx7, fy7, fr7) in ((0.30, -0.20, 0.7), (-0.36, 0.10, 2.3), (0.05, 0.42, 4.1)):
                    px_, py_ = p['cx'] + p['r'] * fx7, p['cy'] + p['r'] * fy7
                    if not place_veg('NENUFAR', px_, py_, H['CURB'] - 0.13, fr7):   # nenufar REAL
                        place(f, ids, 'VEG2_ACUATICA', px_, py_, H['CURB'] - 0.12, fr7)
                        sc.inst('VEG2_ACUATICA', px_, py_, H['CURB'] - 0.12, fr7)
                for k7 in range(7):                                          # tallos emergentes
                    a7 = 2 * math.pi * k7 / 7 + p['cx'] * 0.3
                    rr7 = p['r'] * (0.35 + 0.25 * ((k7 * 5) % 3) / 2)
                    ex7, ey7 = p['cx'] + rr7 * math.cos(a7), p['cy'] + rr7 * math.sin(a7)
                    st7 = mk.cylinder((ex7, ey7, H['CURB'] - 0.14),
                                      (ex7 + 0.05, ey7 + 0.03, H['CURB'] + 0.45 + 0.2 * (k7 % 3)), 0.012, 4)
                    add_mesh(f, lidx, '15_VEGETATION_FULL', 'POND_EMERGENTE', st7)
                    sc.mesh('15_VEGETATION_FULL', st7)
                for k7 in range(5):                                          # borde de rizoma
                    a7 = 2 * math.pi * k7 / 5 + 1.1
                    ex7, ey7 = p['cx'] + p['r'] * 0.88 * math.cos(a7), p['cy'] + p['r'] * 0.88 * math.sin(a7)
                    rz7 = mk.sphere((ex7, ey7, H['CURB'] - 0.13), 0.09, 5, 4)
                    add_mesh(f, lidx, '15_VEGETATION_FULL', 'POND_RIZOMA', rz7)
                    sc.mesh('15_VEGETATION_FULL', rz7)
                place_veg('JUNCO', p['cx'] - p['r'] * 0.55, p['cy'] + p['r'] * 0.48, H['CURB'] - 0.12, 2.9)
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
    spl = mk.surf(ell_pts(sp['cx'], sp['cy'], sp['rx'], sp['ry'], sp['rot'], 32)[:-1], 0.022)
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
                pts3.append((x, y, -0.18))   # 03B.8 D-47: la MAIN va ENTERRADA en todo el trazado
        t = mk.tube(pts3, 0.16, 8)
        add_mesh(f, lidx, '13_PIPES', 'MAIN', t)
        sc.mesh('13_PIPES', t)
        add_curve(f, lidx, '30_CURVES', 'PIPE_AXIS', pts3)
        acc_m = 0.0
        for i3 in range(1, len(pts3)):        # linea de TAPAS de registro: el trazado sigue legible
            acc_m += math.hypot(pts3[i3][0] - pts3[i3 - 1][0], pts3[i3][1] - pts3[i3 - 1][1])
            if acc_m >= 9.0:
                acc_m = 0.0
                if not in_bld_any(pts3[i3][0], pts3[i3][1], 0.3, 0.0):
                    tp9 = mk.box((pts3[i3][0], pts3[i3][1], 0.006), 0.38, 0.38, 0.012)
                    add_mesh(f, lidx, '19_DETALLE', 'MAIN_TAPA', tp9)
                    sc.mesh('19_DETALLE', tp9)
    for (nx, ny) in m['agua_clima']['nebul']:
        g = guard_xy(nx, ny, 0.15, 'NEB_POST')   # CR-7 (V-048/050/051): fuera de bocas de metro
        if g is None:
            continue
        # 03B.8 (QA i1): el poste NO se hinca en una balsa ni en su bordillo
        for (pcx, pcy, pcr) in PONDS_FIN:
            d7 = math.hypot(g[0] - pcx, g[1] - pcy)
            if d7 < pcr + 0.45:
                L7 = d7 or 1e-9
                g = (pcx + (g[0] - pcx) / L7 * (pcr + 0.45), pcy + (g[1] - pcy) / L7 * (pcr + 0.45))
                GUARD_LOG.append({'tag': 'NEB_POST', 'regla': 'balsa', 'a': [round(g[0], 1), round(g[1], 1)]})
        place(f, ids, 'NEB_POST', g[0], g[1], 0)
        sc.inst('NEB_POST', g[0], g[1], 0)
    # 03B.8 D-09/D-43/D-44 Â· TANQUE-TORO con SISTEMA legible: paso >= diametro real (los toros de
    # v004 quedaban entrelazados), TRIPODE de apoyo con horquillas bajo el anillo, bajante central
    # con valvula, rebosadero, indicador de nivel y registro. El donut responde: se sujeta en 3
    # horquillas, descarga por la bajante, esta ahi porque riega su cluster.
    for t in m['estructura_ligera']['tanks']:
        paso_t = t.get('paso', 2 * (t['r'] + 0.85) + 0.60)
        for k in range(t['n']):
            cx = t['cx'] + k * paso_t
            g = bld_clear(cx, t['cy'], t['r'] + 1.0, tag='TANK')   # margen = alcance real del toro
            if g is None:
                continue
            if any(math.hypot(g[0] - ap[0], g[1] - ap[1]) < t['r'] + 2.6 for ap in ANCHOR_PTS):
                GUARD_LOG.append({'tag': 'TANK', 'regla': 'desembarco-descartado',
                                  'xy': [round(g[0], 1), round(g[1], 1)]})
                continue   # 03B.8: el tripode no compite con un desembarco de escalera/ascensor
            cx, tcy = g
            t = dict(t, cy=tcy)
            zt = H['TANK']
            toro = mk.torus((cx, t['cy'], zt), t['r'], 0.85, 18, 9)
            add_mesh(f, lidx, '08_PINK_MODULES', 'TANK', toro)
            sc.mesh('08_PINK_MODULES', toro)
            for a5 in (0.5, 0.5 + 2.094, 0.5 + 4.189):             # tripode bajo el anillo
                px5 = cx + t['r'] * math.cos(a5)
                py5 = t['cy'] + t['r'] * math.sin(a5)
                pole = mk.cylinder((px5, py5, 0), (px5, py5, zt - 0.82), 0.13, 8)
                add_mesh(f, lidx, '04_MASTS', 'TKPOLE', pole)
                sc.mesh('04_MASTS', pole)
                base5 = mk.cylinder((px5, py5, 0), (px5, py5, 0.03), 0.30, 10)
                add_mesh(f, lidx, '19_DETALLE', 'TKPOLE_PLACA', base5)
                sc.mesh('19_DETALLE', base5)
                hq = mk.torus((px5, py5, zt - 0.55), 0.88, 0.05, 12, 5)   # horquilla-abrazadera del tubo
                add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'TK_HORQUILLA', hq)
                sc.mesh('03_SECONDARY_STRUCTURE', hq)
            bajante = mk.cylinder((cx, t['cy'], zt - 0.85), (cx, t['cy'], 0.32), 0.06, 8)
            add_mesh(f, lidx, '13_PIPES', 'TK_BAJANTE', bajante)
            sc.mesh('13_PIPES', bajante)
            brazo = mk.cylinder((cx + t['r'] - 0.8, t['cy'], zt - 0.85), (cx, t['cy'], zt - 0.85), 0.05, 6)
            add_mesh(f, lidx, '13_PIPES', 'TK_TOMA', brazo)
            sc.mesh('13_PIPES', brazo)
            valv = mk.sphere((cx, t['cy'], 1.15), 0.09, 6, 5)
            add_mesh(f, lidx, '19_DETALLE', 'TK_VALVULA', valv)
            sc.mesh('19_DETALLE', valv)
            vol = mk.torus((cx + 0.12, t['cy'], 1.15), 0.09, 0.014, 8, 4)
            add_mesh(f, lidx, '19_DETALLE', 'TK_VOLANTE', vol)
            sc.mesh('19_DETALLE', vol)
            reb = mk.cylinder((cx + t['r'] * 0.5, t['cy'] + t['r'] * 0.62, zt + 0.55),
                              (cx + t['r'] * 0.62, t['cy'] + t['r'] * 0.80, zt - 0.2), 0.035, 5)
            add_mesh(f, lidx, '13_PIPES', 'TK_REBOSADERO', reb)
            sc.mesh('13_PIPES', reb)
            ind = mk.cylinder((cx - t['r'] - 0.02, t['cy'], zt - 0.6), (cx - t['r'] - 0.02, t['cy'], zt + 0.6),
                              0.022, 5)
            add_mesh(f, lidx, '19_DETALLE', 'TK_NIVEL', ind)
            sc.mesh('19_DETALLE', ind)
            reg = mk.cylinder((cx, t['cy'] - t['r'], zt + 0.82), (cx, t['cy'] - t['r'], zt + 0.90), 0.24, 9)
            add_mesh(f, lidx, '19_DETALLE', 'TK_REGISTRO', reg)
            sc.mesh('19_DETALLE', reg)
            # CR-6: plataforma de inspeccion + pates en el poste norte (mantenibilidad conservada)
            plat = mk.box((cx, t['cy'] + t['r'] + 0.35, zt - 1.55), 1.2, 1.2, 0.06)
            add_mesh(f, lidx, '03_SECONDARY_STRUCTURE', 'TKPLAT', plat)
            sc.mesh('03_SECONDARY_STRUCTURE', plat)
            pxn = cx + t['r'] * math.cos(0.5 + 2.094)
            pyn = t['cy'] + t['r'] * math.sin(0.5 + 2.094)
            zz = 2.2   # los pates arrancan sobre la banda de cuerpo (0.05-2.10): no obstruyen el paso
            while zz < zt - 1.6:
                pate = mk.cylinder((pxn - 0.16, pyn + 0.2, zz), (pxn + 0.16, pyn + 0.2, zz), 0.02, 4)
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
            if len(seg) > 4:                                                       # Â§16 canto del asiento
                cb = mk.strip(seg[1:-1], 0.68, H['SEAT'] - 0.025, H['SEAT'] + 0.006)   # 03B.8: sin cunas en los extremos
                add_mesh(f, lidx, '19_DETALLE', 'BENCH_CANTO_%d_%d' % (i, si), cb)
                sc.mesh('19_DETALLE', cb)
            for (qe, qn) in ((seg[0], seg[1]), (seg[-1], seg[-2])):                # 03B.8: TAPA de testero
                qi = (qe[0] * 0.75 + qn[0] * 0.25, qe[1] * 0.75 + qn[1] * 0.25)    # 25% hacia dentro:
                te = mk.box((qi[0], qi[1], H['SEAT'] / 2 + 0.06), 0.14, 0.56, H['SEAT'] - 0.10)  # no invade el eje
                add_mesh(f, lidx, '10_FURNITURE', 'BENCH_TESTERO', te)
                sc.mesh('10_FURNITURE', te)
                for sb20 in (0.14, -0.14):                                 # 03B.9 §20: tornilleria vista
                    pn20 = mk.cylinder((qi[0], qi[1] + sb20, H['SEAT'] - 0.05),
                                       (qi[0], qi[1] + sb20, H['SEAT'] - 0.02), 0.016, 5)
                    add_mesh(f, lidx, '19_DETALLE', 'BENCH_PERNO', pn20)
                    sc.mesh('19_DETALLE', pn20)
            for q in seg[::3]:                                                     # Â§16 patas
                pt = mk.box((q[0], q[1], 0.06), 0.5, 0.12, 0.12)
                add_mesh(f, lidx, '10_FURNITURE', 'BENCH_PATA', pt)
                sc.mesh('10_FURNITURE', pt)
            if i % 2 == 0 and len(seg) >= 4:   # CR-9 (V-027): respaldos construidos en la mitad de los bancos
                bk = mk.strip(offs(seg, 0.27), 0.09, H['SEAT'], H['BACK'])
                add_mesh(f, lidx, '10_FURNITURE', 'BENCHBACK_%d_%d' % (i, si), bk)
                sc.mesh('10_FURNITURE', bk)
    # CR-6 puerta D-C1-1 Â· V-023 bolsillo Â· franja de respeto de la estatua Â· puertas anti-trampa:
    # cada paso estrangulado de 0.50 m entre jardineras (SW + montera) se abre a >=1.5 m (regla CR-2
    # generalizada: una barrera lineal siempre tiene puertas; el 0.50 atrapa, el 1.5 deja pasar)
    GATES_R = [((-72, 17), 1.6), ((6.9, -4.1), 3.0), (tuple(EST['xy']), 6.0),
               ((43.2, 0.3), 2.3), ((45.0, 1.0), 2.0), ((-54, -22), 2.3), ((-57, -17), 2.3), ((-50, -16), 2.3),
               ((-64, -16), 2.3), ((-43, -14), 2.3), ((-70, -13), 2.3)]
    def _snap_mast_pl(q):
        """CR-2 (it.9): jardinera contra mastil â€” el lecho CIERRA contra el tiesto (gap ~2 cm)
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
        # CR-2 (it.7): contra fachada la jardinera CIERRA (snap del borde) o ABRE >=1.5 â€” nunca
        # ranuras-trampa de 0.5 m (V-001/V-006); y sigue respetando puertas y ejes declarados
        def _snap_pond_pl(q8):
            """CR-2 (03B.8): la jardinera contra una balsa CIERRA al bordillo o ABRE >=1.5."""
            for (pcx8, pcy8, pcr8) in PONDS_FIN:
                d8 = math.hypot(q8[0] - pcx8, q8[1] - pcy8)
                if pcr8 + 0.80 < d8 < pcr8 + 0.76 + 1.5:
                    L8 = d8 or 1e-9
                    return (pcx8 + (q8[0] - pcx8) / L8 * (pcr8 + 0.80),
                            pcy8 + (q8[1] - pcy8) / L8 * (pcr8 + 0.80))
            return q8

        keep = [_snap_pond_pl(_snap_mast_pl(snap_facade(q[0], q[1], 0.78))) for q in p['pts']]
        keep = [q for q in keep if all(math.hypot(q[0] - gx, q[1] - gy) > gr for ((gx, gy), gr) in GATES_R)
                and not near_corr(q[0], q[1], 2.05)]   # 03B.9 V-002: cara (centro-0.76) a >=1.29 del eje
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
            cp = mk.strip(seg, 1.52, H['PLANTER'] - 0.04, H['PLANTER'] + 0.015)   # Â§16 coronacion/canto
            add_mesh(f, lidx, '19_DETALLE', 'PLANTER_CANTO_%d_%d' % (i, si), cp)
            sc.mesh('19_DETALLE', cp)
            for q in seg[::5]:                                                    # Â§16 mechinales de drenaje
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
        # 03B.9 (D-29 de S09): la recirculacion tambien va ENTERRADA — tapas en los quiebros
        pts3 = [(q[0], q[1], -0.16) for q in wp]
        rt = mk.tube(pts3, 0.09, 6)
        add_mesh(f, lidx, '13_PIPES', 'RECIRC', rt)
        sc.mesh('13_PIPES', rt)
        add_curve(f, lidx, '30_CURVES', 'RECIRC_AXIS', pts3)
        for q in wp:
            if not in_bld_any(q[0], q[1], 0.3, 0.0):
                tp29 = mk.box((q[0], q[1], 0.006), 0.32, 0.32, 0.012)
                add_mesh(f, lidx, '19_DETALLE', 'RECIRC_TAPA', tp29)
                sc.mesh('19_DETALLE', tp29)
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

    # ---- 03B.7-B Â· FIGURA ESPACIAL: atrio de la Estacion + media luna de Carmen + aprons ----
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

    # ---- 03B.7 Â§8/Â§18/Â§19/Â§20 Â· DETAILING de sitio (cinta, pavimento, Carlos III, contexto) ----
    DET.site_details(lambda layer, nombre, VF: (add_mesh(f, lidx, layer, nombre, VF),
                                                sc.mesh(layer, VF)),
                     sc, mk, m, rib, WH, rib_side_w, in_bld_any, EST, ESTP,
                     m['contexto']['buildings'],
                     anchors_xy=[tuple(rib[i]) for (_n2, i, _s2) in anchors])

    # ---- vegetacion / personas (solo full) ----
    if full:
        # E02: arboles de sombra multilobulados â€” CR-1: guard en posicion final + separacion de discos bajos (V-063)
        for i, (tx, ty) in enumerate(m['paisaje']['new_trees']):
            g = guard_xy(tx, ty, 0.4, 'ARBOL_%d' % i, corr_min=2.1)
            if g is None:
                continue
            tx, ty = g
            # 03B.7-D: las CUATRO guardas (disco/cupula/cinta/fachada) se iteran hasta CONVERGER â€”
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
                # comprobacion de copa contra fachadas â€” margen = alcance REAL del bloque v2
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
            # 03B.9 §3: arbol REAL (olmo urbano CC-BY) con variantes anti-clon; cae al
            # procedural v2 si el asset no cargo
            if not place_veg('ARBOLURB', tx, ty, 0, i * 0.8):
                nmv = ('VEG2_ARBOL_A', 'VEG2_ARBOL_B')[i % 2]
                place(f, ids, nmv, tx, ty, 0, i * 0.8)
                sc.inst(nmv, tx, ty, 0, i * 0.8)
        for i, t in enumerate(m['contexto']['trees']):
            if -110 < t['x'] < 100 and -45 < t['y'] < 75:
                if not place_veg('ARBOLURB', t['x'], t['y'], 0, i * 0.6):
                    place(f, ids, 'VEG2_ARBOL_EX', t['x'], t['y'], 0, i * 0.6)
                    sc.inst('VEG2_ARBOL_EX', t['x'], t['y'], 0, i * 0.6)
        # trepadoras en la mitad de los mastiles â€” 03B.7-D: no en mastiles pegados a la cinta
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
                en_tren = any(math.hypot(px_ - qx, py_ - qy) < 4.5 for (qx, qy) in TREN_XY)
                if en_tren:
                    GUARD_LOG.append({'tag': 'HUERTO_%d_%d' % (gx, gy), 'regla': 'tren-omitido'})
                if (en_tren or near_corr(px_, py_, 2.6) or near_metro_pt(px_, py_)
                        or near_pipe(px_, py_) or in_bld_any(px_, py_, 0.8, 0.0)):
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
                    rolt = ('ALOCASIA', 'CALATHEA', 'MONSTERA', 'MONSTERA2', 'ALOCASIA2')[tr % 5]
                    if not place_veg(rolt, px_, py_, 0, tr * 0.7):
                        place(f, ids, 'VEG2_TROPICAL', px_, py_, 0, tr * 0.7)
                        sc.inst('VEG2_TROPICAL', px_, py_, 0, tr * 0.7)
                    tr += 1
        dm2 = m['estructura_principal']['dome']
        for k in range(3):
            a = 2 * math.pi * k / 3 + 0.8
            px_, py_ = dm2['cx'] + 3.1 * math.cos(a), dm2['cy'] + 3.1 * math.sin(a)
            if not near_corr(px_, py_, 2.2):
                if not place_veg(('MONSTERA2', 'ALOCASIA2', 'CALATHEA')[k % 3], px_, py_, 0, k * 1.3):
                    place(f, ids, 'VEG2_TROPICAL', px_, py_, 0, k * 1.3)
                    sc.inst('VEG2_TROPICAL', px_, py_, 0, k * 1.3)
        # VEGETACION BAJA junto a bancos â€” CR-1 (V-059): la mata sale al lado libre, nunca al corredor
        for b in m['programa']['benches']:
            bp = b['pts']
            for j in range(1, len(bp), 3):
                a0 = bp[max(j - 1, 0)]; b0 = bp[min(j + 1, len(bp) - 1)]
                dxq, dyq = b0[0] - a0[0], b0[1] - a0[1]
                Lq = math.hypot(dxq, dyq) or 1e-9
                for sgn in (1, -1):
                    qx, qy = bp[j][0] - dyq / Lq * 1.15 * sgn, bp[j][1] + dxq / Lq * 1.15 * sgn
                    if not near_corr(qx, qy, 1.9):
                        cama = mk.cylinder((qx, qy, 0), (qx, qy, 0.045), 0.34, 10)   # 03B.8: CAMA de plantacion
                        add_mesh(f, lidx, '19_DETALLE', 'CAMA_PLANTA', cama)          # (nada brota del granito)
                        sc.mesh('19_DETALLE', cama)
                        if not place_veg(('GRAMINEA', 'HELECHO', 'HELECHO2', 'GRAMALTA')[j % 4], qx, qy, 0.04, qx * 0.7):
                            place(f, ids, 'VEG2_BAJA', qx, qy, 0.04, qx * 0.1)
                            sc.inst('VEG2_BAJA', qx, qy, 0.04, qx * 0.1)
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
                if not place_veg('POTHOS', px_, py_, z - 0.05, i * 0.07):
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
            if not place_veg('POTHOS', q[0], q[1], H['RIBBON'] - 0.02, i * 0.1):
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
    okM = fM.Write(os.path.join(HERE, 'MASTER_ARCHITECTURE_v006.3dm'), 8)
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
    okA = fA.Write(os.path.join(HERE, 'ASSET_LIBRARY_v005.3dm'), 8)

    # 3) SOL_FULL_SCENE_v003 (todo) â€” tambien es la base de presentacion
    fF, lF = new_file()
    idsF = register_blocks(fF, lF, ALL_BLOCKS)
    scF = Scene()
    build_site(fF, lF, idsF, scF, full=True)
    okF = fF.Write(os.path.join(HERE, 'SOL_FULL_SCENE_v005.3dm'), 8)
    # 4) SOL_PRESENTATION_MASTER_v002: escena completa consolidada como entrada de presentacion
    okP = fF.Write(os.path.join(HERE, 'SOL_PRESENTATION_MASTER_v004.3dm'), 8)

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
    print('MASTER:', okM, 'Â· ASSETS:', okA, 'Â· FULL:', okF, 'Â· PRES:', okP)
    print('bloques:', len(ALL_BLOCKS), 'Â· escena full: %d mallas, %d lineas, %d tris' % (len(scF.meshes), len(scF.lines), tris))
    print('guard: %d ajustes registrados' % len(GUARD_LOG))
