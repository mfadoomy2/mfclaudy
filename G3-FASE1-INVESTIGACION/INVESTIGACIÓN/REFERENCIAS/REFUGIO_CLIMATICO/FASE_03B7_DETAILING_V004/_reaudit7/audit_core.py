# -*- coding: utf-8 -*-
"""
FASE 03B.5 — nucleo de auditoria.
Reconstruye EN MEMORIA la escena aprobada (SOL_FULL_SCENE / MASTER_ARCHITECTURE v002)
con nombre + capa + coordenadas de mundo por objeto, y ofrece el rasterizado
comun (rejilla 0.25 m) que usan todos los analisis.

NO escribe nada sobre el modelo maestro. Solo lee.
Fuente: build_all_03b.build_site(full=True) con add_mesh/place/add_curve interceptados.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))            # _reaudit7 vive un nivel mas abajo
F03B = os.path.join(ROOT, 'FASE_03B7_DETAILING_V004')              # 03B.7: audita el generador v004
F03A = os.path.join(ROOT, 'FASE_03A_MODELO_PROXY')
DATA = os.path.join(HERE, '_data')
MAPS = os.path.join(HERE, '_maps')

# --------------------------------------------------------------- parametros de auditoria
CELL = 0.25                    # m/celda de la rejilla de analisis
BODY_LO, BODY_HI = 0.05, 2.10  # banda de cuerpo peatonal (obstruccion al paso)
EYE_Z = 1.65                   # altura de ojo para el analisis visual
H_PERSON = 1.70                # persona de referencia (HEIGHT_SYSTEM)
SHOULDER = 0.55                # ancho de hombros
WHEELCHAIR = (0.80, 1.20)      # silla de ruedas (ancho x largo)

# capas que NO obstruyen fisicamente el paso
NON_SOLID = {'12_MIST', '16_PEOPLE_PROXY', '17_METRO_CLEARANCES', '30_CURVES'}
# capas que no forman parte del proyecto (contexto urbano existente)
CONTEXT = {'00_CONTEXT', '01_GROUND'}

# familia sintetica por capa/nombre -> para la matriz de colisiones
FAMILY_OF_LAYER = {
    '00_CONTEXT': 'CONTEXT', '01_GROUND': 'GROUND',
    '02_PRIMARY_STRUCTURE': 'STRUCTURE', '03_SECONDARY_STRUCTURE': 'STRUCTURE',
    '04_MASTS': 'STRUCTURE', '05_CABLES': 'CABLE', '06_MEMBRANES': 'CANOPY',
    '07_CANOPIES': 'CANOPY', '08_PINK_MODULES': 'PODS', '09_PLANTERS': 'PLANTER',
    '10_FURNITURE': 'FURNITURE', '11_WATER': 'WATER', '12_MIST': 'MIST',
    '13_PIPES': 'WATER', '14_VEGETATION_PROXY': 'VEGETATION',
    '15_VEGETATION_FULL': 'VEGETATION', '16_PEOPLE_PROXY': 'PEOPLE',
    '17_METRO_CLEARANCES': 'METRO_CLEARANCE', '30_CURVES': 'CURVE',
    '19_DETALLE': 'DETAIL',
}


# =============================================================== 1 · ESCENA
def load_scene():
    """Devuelve (objs, M) con objs = [{kind,layer,name,V,F|pts,anchor}] en coords de mundo."""
    sys.path.insert(0, F03B)
    sys.path.insert(0, F03A)
    cwd = os.getcwd()
    os.chdir(F03B)
    try:
        import build_all_03b7 as B
    finally:
        os.chdir(cwd)

    objs = []

    def _add_mesh(f, lidx, layer, name, VF):
        V, F = VF
        if F:
            objs.append(dict(kind='mesh', layer=layer, name=name, block='',
                             V=np.asarray(V, dtype=np.float64), F=np.asarray(F, dtype=np.int32),
                             anchor=None))

    def _place(f, ids, name, x, y, z, rot=0.0, lidx=None):
        ca, sa = math.cos(rot), math.sin(rot)
        for (layer, (V, F)) in B.BLOCKS[name]:
            if not F:
                continue
            A = np.asarray(V, dtype=np.float64)
            Vt = np.column_stack([A[:, 0] * ca - A[:, 1] * sa + x,
                                  A[:, 0] * sa + A[:, 1] * ca + y,
                                  A[:, 2] + z])
            objs.append(dict(kind='mesh', layer=layer, name=name, block=name,
                             V=Vt, F=np.asarray(F, dtype=np.int32), anchor=(x, y, z)))

    def _add_curve(f, lidx, layer, name, pts):
        objs.append(dict(kind='curve', layer=layer, name=name, block='',
                         pts=np.asarray([(p[0], p[1], p[2] if len(p) > 2 else 0.0) for p in pts],
                                        dtype=np.float64), anchor=None))

    class _NullScene:
        def inst(self, *a, **k): pass
        def mesh(self, *a, **k): pass
        def line(self, *a, **k): pass

    B.add_mesh, B.place, B.add_curve = _add_mesh, _place, _add_curve
    f, lidx = B.new_file()
    ids = {n: None for n in B.ALL_BLOCKS}
    B.build_site(f, lidx, ids, _NullScene(), full=True)
    return objs, B.m, B


def obj_family(o):
    n = o['name']
    if n.startswith('LEAF'):
        return 'CANOPY'
    if n.startswith('POD') or n in ('TANK',):
        return 'PODS'
    if n.startswith('VEG2') or n.startswith('TREE') or n in ('TROPICAL', 'SHRUB', 'AQUATIC', 'CLIMBER'):
        return 'VEGETATION'
    if n.startswith('RIBBON') or n.startswith('RIB_') or n in ('STRINGER', 'STEP', 'BALPOST'):
        return 'RIBBON'
    if n.startswith('DROP') or n in ('NEB_POST', 'MAIN', 'RISER', 'TKPOLE'):
        return 'WATER'
    return FAMILY_OF_LAYER.get(o['layer'], 'OTHER')


# =============================================================== 2 · REJILLA
class Grid:
    def __init__(self, x0, y0, x1, y1, cell=CELL):
        self.cell = cell
        self.x0, self.y0 = x0, y0
        self.nx = int(math.ceil((x1 - x0) / cell))
        self.ny = int(math.ceil((y1 - y0) / cell))
        self.x1, self.y1 = x0 + self.nx * cell, y0 + self.ny * cell
        # centros de celda
        self.xs = x0 + (np.arange(self.nx) + 0.5) * cell
        self.ys = y0 + (np.arange(self.ny) + 0.5) * cell

    def shape(self):
        return (self.ny, self.nx)

    def ij(self, x, y):
        return (int((y - self.y0) / self.cell), int((x - self.x0) / self.cell))

    def xy(self, i, j):
        return (self.x0 + (j + 0.5) * self.cell, self.y0 + (i + 0.5) * self.cell)

    def extent(self):
        return (self.x0, self.x1, self.y0, self.y1)

    def inside(self, i, j):
        return 0 <= i < self.ny and 0 <= j < self.nx


def tris_of(o):
    """(T,3,3) triangulos del objeto en coords de mundo."""
    V, F = o['V'], o['F']
    if F.shape[1] == 3:
        return V[F]
    q = V[F]
    return np.concatenate([q[:, (0, 1, 2), :], q[:, (0, 2, 3), :]], axis=0)


def rasterize(grid, tris, zlo=None, zhi=None, mode='mask', out=None):
    """Proyecta triangulos sobre la rejilla.
    mode 'mask'  -> booleano de cobertura (triangulos cuyo rango z corta [zlo,zhi])
    mode 'zmin'  -> minimo z de la superficie interpolada (triangulos con zmax>=zlo)
    mode 'zmax'  -> maximo z
    """
    ny, nx, cell, gx0, gy0 = grid.ny, grid.nx, grid.cell, grid.x0, grid.y0
    if out is None:
        out = (np.zeros((ny, nx), dtype=bool) if mode == 'mask'
               else np.full((ny, nx), np.inf if mode == 'zmin' else -np.inf))
    if len(tris) == 0:
        return out
    tz0, tz1 = tris[:, :, 2].min(1), tris[:, :, 2].max(1)
    if mode == 'mask':
        keep = (tz1 >= zlo) & (tz0 <= zhi)
    elif mode == 'zmin':
        keep = tz1 >= zlo
    else:
        keep = tz0 <= zhi if zhi is not None else np.ones(len(tris), bool)
    tris = tris[keep]
    if len(tris) == 0:
        return out

    bx0 = np.maximum(np.floor((tris[:, :, 0].min(1) - gx0) / cell).astype(int), 0)
    bx1 = np.minimum(np.ceil((tris[:, :, 0].max(1) - gx0) / cell).astype(int), nx - 1)
    by0 = np.maximum(np.floor((tris[:, :, 1].min(1) - gy0) / cell).astype(int), 0)
    by1 = np.minimum(np.ceil((tris[:, :, 1].max(1) - gy0) / cell).astype(int), ny - 1)

    for t in range(len(tris)):
        j0, j1, i0, i1 = bx0[t], bx1[t], by0[t], by1[t]
        if j1 < j0 or i1 < i0:
            continue
        P = tris[t]
        xs = gx0 + (np.arange(j0, j1 + 1) + 0.5) * cell
        ys = gy0 + (np.arange(i0, i1 + 1) + 0.5) * cell
        X, Y = np.meshgrid(xs, ys)
        ax, ay = P[0, 0], P[0, 1]
        v0x, v0y = P[1, 0] - ax, P[1, 1] - ay
        v1x, v1y = P[2, 0] - ax, P[2, 1] - ay
        den = v0x * v1y - v1x * v0y
        if abs(den) < 1e-12:
            continue
        px, py = X - ax, Y - ay
        u = (px * v1y - v1x * py) / den
        v = (v0x * py - px * v0y) / den
        tol = 1e-9
        m = (u >= -tol) & (v >= -tol) & (u + v <= 1 + tol)
        if not m.any():
            continue
        if mode == 'mask':
            sub = out[i0:i1 + 1, j0:j1 + 1]
            sub |= m
        else:
            z = P[0, 2] + u * (P[1, 2] - P[0, 2]) + v * (P[2, 2] - P[0, 2])
            sub = out[i0:i1 + 1, j0:j1 + 1]
            if mode == 'zmin':
                np.minimum(sub, np.where(m, z, np.inf), out=sub)
            else:
                np.maximum(sub, np.where(m, z, -np.inf), out=sub)
    return out


# =============================================================== 3 · REGISTRO DE INCIDENCIAS
class Issues:
    def __init__(self):
        self.rows = []
        self._n = 0

    def add(self, sev, cat, title, x=None, y=None, z=None, mag='', cause='', strat='',
            ref='', metric=None):
        self._n += 1
        vid = 'V-%03d' % self._n
        self.rows.append(dict(id=vid, sev=sev, cat=cat, title=title,
                              x=None if x is None else round(float(x), 2),
                              y=None if y is None else round(float(y), 2),
                              z=None if z is None else round(float(z), 2),
                              magnitud=mag, causa=cause, estrategias=strat, ref=ref,
                              metric=metric))
        return vid

    def by_sev(self, s):
        return [r for r in self.rows if r['sev'] == s]

    def save(self, path):
        json.dump(self.rows, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def jdump(name, obj):
    p = os.path.join(DATA, name)
    json.dump(obj, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1,
              default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
    return p


def jload(name):
    return json.load(open(os.path.join(DATA, name), encoding='utf-8'))


# =============================================================== 4 · UTILIDADES GEOMETRICAS
def poly_len(pts):
    p = np.asarray(pts, dtype=float)[:, :2]
    return float(np.hypot(*(p[1:] - p[:-1]).T).sum())


def resample(pts, step):
    """Remuestrea una polilinea 2D a paso constante. Devuelve (P, S) puntos y abscisa."""
    p = np.asarray(pts, dtype=float)[:, :2]
    d = np.hypot(*(p[1:] - p[:-1]).T)
    s = np.concatenate([[0], np.cumsum(d)])
    L = s[-1]
    ss = np.arange(0, L + 1e-9, step)
    return np.column_stack([np.interp(ss, s, p[:, 0]), np.interp(ss, s, p[:, 1])]), ss


def tangents(P):
    T = np.gradient(P, axis=0)
    n = np.hypot(T[:, 0], T[:, 1])
    n[n == 0] = 1
    return T / n[:, None]


def normals(P):
    T = tangents(P)
    return np.column_stack([-T[:, 1], T[:, 0]])


def seg_point_dist(px, py, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    L2 = vx * vx + vy * vy
    if L2 <= 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / L2))
    return math.hypot(px - (ax + vx * t), py - (ay + vy * t))
