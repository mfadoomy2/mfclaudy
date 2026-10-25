"""Primitivas de modelado para las unidades (metros). Mallas trimesh; booleanos con manifold."""
import math
from dataclasses import dataclass, field

import numpy as np
import trimesh
from shapely.geometry import Polygon, Point

# Colores del proyecto (fondo blanco, colores vivos)
COL = {
    'blando': '#F4A6C6',      # superficie blanda (cama / suelo-cama)
    'blando_calido': '#F26B8A',
    'blando_fresco': '#9BD3F2',
    'canto': '#2B2B2B',       # borde duro: mesa, repisa, asiento
    'membrana': '#36C5D1',    # tela acústica y visual
    'membrana2': '#1F7A8C',
    'cielo': '#FFD23F',       # hueco al cielo, vela
    'dock': '#F26A1B',        # armario-maleta, enchufes
    'plinto': '#C9C9C9',      # soporte, plataforma, estructura
    'muro': '#9A9A9A',
    'suelo': '#ECECEC',
    'cuerpo': '#D81B8A',
    'cuerpo2': '#7B2CBF',
    'parcela': '#F7F2E8',
    'vecino': '#D8D8D8',
    'comision': '#2DC653',
    'tronco': '#8B5A2B',
}


@dataclass
class Pieza:
    nombre: str
    malla: trimesh.Trimesh
    color: str = COL['plinto']
    capa: str = 'varios'        # ruta de capa "H3::superficie"
    alpha: float = 1.0

    def copia(self, nombre=None, capa=None, dx=0, dy=0, dz=0):
        m = self.malla.copy()
        m.apply_translation([dx, dy, dz])
        return Pieza(nombre or self.nombre, m, self.color, capa or self.capa, self.alpha)


def mover(malla, dx=0, dy=0, dz=0):
    m = malla.copy()
    m.apply_translation([dx, dy, dz])
    return m


def girar_z(malla, grados, centro=(0, 0, 0)):
    m = malla.copy()
    m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(grados), [0, 0, 1], centro))
    return m


def girar(malla, grados, eje, centro=(0, 0, 0)):
    m = malla.copy()
    m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(grados), eje, centro))
    return m


def caja(x0, y0, z0, dx, dy, dz):
    """Caja por esquina mínima y dimensiones."""
    m = trimesh.creation.box((dx, dy, dz))
    m.apply_translation([x0 + dx / 2, y0 + dy / 2, z0 + dz / 2])
    return m


def cilindro(cx, cy, z0, r, h, n=48):
    m = trimesh.creation.cylinder(radius=r, height=h, sections=n)
    m.apply_translation([cx, cy, z0 + h / 2])
    return m


def elipsoide(cx, cy, cz, rx, ry, rz, n=3):
    m = trimesh.creation.icosphere(subdivisions=n)
    m.apply_scale([rx, ry, rz])
    m.apply_translation([cx, cy, cz])
    return m


def capsula(cx, cy, cz, largo, r, eje='x', n=24):
    """Cápsula (cuerpo tumbado) de longitud total `largo` y radio r, centrada."""
    m = trimesh.creation.capsule(height=max(largo - 2 * r, 0.01), radius=r, count=[n, n])
    # trimesh la crea a lo largo de z
    if eje == 'x':
        m.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 1, 0]))
    elif eje == 'y':
        m.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
    m.apply_translation([cx, cy, cz])
    return m


def extruir(poligono, z0, h):
    if poligono.geom_type == 'MultiPolygon':
        return trimesh.util.concatenate([extruir(g, z0, h) for g in poligono.geoms])
    m = trimesh.creation.extrude_polygon(poligono, h)
    m.apply_translation([0, 0, z0])
    return m


def anillo(poligono_ext, ancho, z0, h):
    """Corona entre el polígono y su contracción `ancho` (canto perimetral)."""
    interior = poligono_ext.buffer(-ancho)
    return extruir(poligono_ext.difference(interior), z0, h)


def rect(x0, y0, dx, dy, radio=0.0):
    p = Polygon([(x0, y0), (x0 + dx, y0), (x0 + dx, y0 + dy), (x0, y0 + dy)])
    if radio > 0:
        p = p.buffer(-radio).buffer(radio, join_style=1)
    return p


def elipse(cx, cy, rx, ry, n=64):
    return Polygon([(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in np.linspace(0, 2 * math.pi, n, endpoint=False)])


def union(*mallas):
    mallas = [m for m in mallas if m is not None]
    if len(mallas) == 1:
        return mallas[0]
    try:
        return trimesh.boolean.union(mallas, engine='manifold')
    except Exception:
        return trimesh.util.concatenate(mallas)


def resta(a, *bs):
    try:
        return trimesh.boolean.difference([a, *bs], engine='manifold')
    except Exception:
        return a


def relieve(x0, y0, dx, dy, z_fn, nx=40, ny=50, base=0.0):
    """Sólido entre z=base y la función z_fn(x,y) (relieve blando)."""
    xs = np.linspace(x0, x0 + dx, nx)
    ys = np.linspace(y0, y0 + dy, ny)
    X, Y = np.meshgrid(xs, ys)
    Z = np.vectorize(z_fn)(X, Y)
    top = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    bot = np.column_stack([X.ravel(), Y.ravel(), np.full(X.size, base)])
    nv = top.shape[0]
    v = np.vstack([top, bot])
    faces = []
    idx = lambda i, j: i * nx + j
    for i in range(ny - 1):
        for j in range(nx - 1):
            a, b, c, d = idx(i, j), idx(i, j + 1), idx(i + 1, j + 1), idx(i + 1, j)
            faces += [[a, b, c], [a, c, d]]                     # tapa
            faces += [[nv + a, nv + c, nv + b], [nv + a, nv + d, nv + c]]  # fondo
    # laterales
    borde = [idx(0, j) for j in range(nx)] + [idx(i, nx - 1) for i in range(1, ny)] + \
            [idx(ny - 1, j) for j in range(nx - 2, -1, -1)] + [idx(i, 0) for i in range(ny - 2, 0, -1)]
    for k in range(len(borde)):
        a, b = borde[k], borde[(k + 1) % len(borde)]
        faces += [[a, nv + a, b], [b, nv + a, nv + b]]
    m = trimesh.Trimesh(vertices=v, faces=np.array(faces), process=True)
    m.fix_normals()
    return m


def tela_vertical(path_pts, z0, h, grosor=0.02, cerrada=True):
    """Membrana colgada: extrusión fina a lo largo de una polilínea (o anillo)."""
    from shapely.geometry import LineString, LinearRing
    ls = LinearRing(path_pts) if cerrada else LineString(path_pts)
    p = ls.buffer(grosor / 2, cap_style=2, join_style=2)
    return extruir(p, z0, h)


def tubo(pts, r=0.03, n=12):
    """Tubo a lo largo de una polilínea 3D (barras, cables, percha)."""
    partes = []
    for a, b in zip(pts[:-1], pts[1:]):
        a, b = np.array(a, float), np.array(b, float)
        L = np.linalg.norm(b - a)
        if L < 1e-6:
            continue
        c = trimesh.creation.cylinder(radius=r, height=L, sections=n)
        d = (b - a) / L
        R = trimesh.geometry.align_vectors([0, 0, 1], d)
        c.apply_transform(R)
        c.apply_translation((a + b) / 2)
        partes.append(c)
    return trimesh.util.concatenate(partes)


def area(poligono):
    return poligono.area
