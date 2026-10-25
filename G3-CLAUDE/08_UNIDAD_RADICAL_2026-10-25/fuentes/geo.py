"""Geometría de las unidades: piezas, muros, huecos, mobiliario y comprobaciones.

Unidades en metros. Cotas interiores libres: los muros crecen hacia fuera de cada pieza.
"""
import math
from dataclasses import dataclass, field

import numpy as np
from shapely import affinity
from shapely.geometry import LineString, MultiPolygon, Point, Polygon, box
from shapely.ops import unary_union

# Espesores de estudio (no son especificación constructiva)
T_CELDA = 0.12      # tabique de celda: doble placa + aislante, entramado ligero
T_SERV = 0.10       # tabique húmedo
T_ENV = 0.30        # envolvente

# Medidas que no se reducen (decisiones vigentes del proyecto)
CAMA = (1.25, 2.00)
TABLERO = (1.80, 0.90)


def arco(cx, cy, r, a0, a1, n=48):
    """Puntos de un arco (grados, antihorario)."""
    ts = np.linspace(math.radians(a0), math.radians(a1), n)
    return [(cx + r * math.cos(t), cy + r * math.sin(t)) for t in ts]


def semidisco(cx, cy, r, a0, a1, n=48):
    return Polygon([(cx, cy)] + arco(cx, cy, r, a0, a1, n))


def segmento_circular(p0, p1, sagita, n=40):
    """Segmento circular apoyado en la cuerda p0-p1 que sobresale `sagita` hacia la izquierda del vector p0->p1."""
    (x0, y0), (x1, y1) = p0, p1
    c = math.dist(p0, p1)
    r = (c * c / 4 + sagita * sagita) / (2 * sagita)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    ux, uy = (x1 - x0) / c, (y1 - y0) / c
    nx, ny = -uy, ux                      # normal a la izquierda
    cx, cy = mx - nx * (r - sagita), my - ny * (r - sagita)
    a0 = math.degrees(math.atan2(y0 - cy, x0 - cx))
    a1 = math.degrees(math.atan2(y1 - cy, x1 - cx))
    if a1 < a0:
        a1 += 360
    pts = arco(cx, cy, r, a0, a1, n)
    # el arco debe pasar por el lado de la normal
    mid = pts[len(pts) // 2]
    if (mid[0] - mx) * nx + (mid[1] - my) * ny < 0:
        pts = arco(cx, cy, r, a1 - 360, a0, n)[::-1]
    return Polygon(pts), pts, (cx, cy, r)


@dataclass
class Pieza:
    """Recinto con muro propio (celda, baño, cocina cerrada...)."""
    nombre: str
    tipo: str                    # celda | bano | aseo | cocina | lavadero | patinillo
    suelo: Polygon               # superficie libre interior
    t: float = T_CELDA
    puertas: list = field(default_factory=list)     # [(LineString hueco, tipo, datos)]
    ventanas: list = field(default_factory=list)    # [LineString]
    bows: list = field(default_factory=list)        # [dict con arco y asiento]
    muebles: list = field(default_factory=list)     # [(nombre, geom, estilo)]
    obstaculos: list = field(default_factory=list)  # geoms que ocupan suelo
    destinos: dict = field(default_factory=dict)    # nombre -> Point a alcanzar
    entrada: object = None       # Point justo dentro de la puerta
    acceso_fuera: object = None  # Point justo fuera de la puerta

    def transformar(self, f):
        g = lambda geom: f(geom)
        self.suelo = g(self.suelo)
        self.puertas = [(g(h), tp, {k: (g(v) if hasattr(v, 'geom_type') else v) for k, v in d.items()}) for h, tp, d in self.puertas]
        self.ventanas = [g(v) for v in self.ventanas]
        self.bows = [{k: (g(v) if hasattr(v, 'geom_type') else v) for k, v in b.items()} for b in self.bows]
        self.muebles = [(n, g(m), e) for n, m, e in self.muebles]
        self.obstaculos = [g(o) for o in self.obstaculos]
        self.destinos = {k: g(v) for k, v in self.destinos.items()}
        self.entrada = g(self.entrada) if self.entrada is not None else None
        self.acceso_fuera = g(self.acceso_fuera) if self.acceso_fuera is not None else None
        return self


def colocar(pieza, x=0.0, y=0.0, rot=0.0, espejo=False):
    """Espejo respecto al eje y local, giro (grados) respecto al origen local y traslación."""
    def f(geom):
        if espejo:
            geom = affinity.scale(geom, xfact=-1, yfact=1, origin=(0, 0))
        if rot:
            geom = affinity.rotate(geom, rot, origin=(0, 0))
        return affinity.translate(geom, x, y)
    return pieza.transformar(f)


def puerta_batiente(x0, y0, ancho, bisagra='izq', muro=0.12):
    """Puerta en el muro y=y0 de un recinto cuyo interior está en +y. Abre hacia dentro."""
    hueco = box(x0, y0 - muro - 0.01, x0 + ancho, y0 + 0.01)
    if bisagra == 'izq':
        hx, a0, a1 = x0, 0, 90
    else:
        hx, a0, a1 = x0 + ancho, 90, 180
    hoja = LineString([(hx, y0), (hx, y0 + ancho)])
    pts = arco(hx, y0, ancho, a0, a1, 24)
    barrido = Polygon([(hx, y0)] + pts)
    dentro = Point(x0 + ancho / 2, y0 + 0.30)
    fuera = Point(x0 + ancho / 2, y0 - muro - 0.30)
    return hueco, hoja, barrido, LineString(pts), dentro, fuera


def puerta_corredera(x0, y0, ancho, muro=0.10, lado='izq'):
    """Corredera en el muro y=y0 (interior en +y); la hoja corre dentro del espesor del muro hacia un lado."""
    hueco = box(x0, y0 - muro - 0.01, x0 + ancho, y0 + 0.01)
    ym = y0 - muro / 2
    if lado == 'izq':
        hoja = box(x0 - ancho + 0.05, ym - 0.015, x0 + 0.05, ym + 0.015)
    else:
        hoja = box(x0 + ancho - 0.05, ym - 0.015, x0 + 2 * ancho - 0.05, ym + 0.015)
    dentro = Point(x0 + ancho / 2, y0 + 0.30)
    fuera = Point(x0 + ancho / 2, y0 - muro - 0.30)
    return hueco, hoja, dentro, fuera


# ---------------------------------------------------------------------------
# Comprobación de paso libre por rejilla (cuerpo representado por un disco)

PASO = 0.025


class Rejilla:
    def __init__(self, libre, obst):
        self.libre = libre
        minx, miny, maxx, maxy = libre.bounds
        self.ox, self.oy = minx - 0.1, miny - 0.1
        self.nx = int((maxx - minx + 0.2) / PASO) + 1
        self.ny = int((maxy - miny + 0.2) / PASO) + 1
        xs = self.ox + np.arange(self.nx) * PASO
        ys = self.oy + np.arange(self.ny) * PASO
        X, Y = np.meshgrid(xs, ys)
        from shapely import contains_xy
        zona = libre.difference(unary_union(obst)) if obst else libre
        self.zona = zona
        self.ok = contains_xy(zona, X, Y)

    def erosion(self, r):
        from scipy.ndimage import binary_erosion
        k = int(round(r / PASO))
        yy, xx = np.mgrid[-k:k + 1, -k:k + 1]
        disco = (xx ** 2 + yy ** 2) <= k * k
        return binary_erosion(self.ok, structure=disco, border_value=0)

    def idx(self, p):
        return int(round((p.y - self.oy) / PASO)), int(round((p.x - self.ox) / PASO))

    def alcanzable(self, r, origen, destinos, tolerancia=None):
        """Devuelve {destino: bool}. Un destino se alcanza si el centro del disco llega a menos de `tolerancia`."""
        from scipy.ndimage import label
        er = self.erosion(r)
        lab, _ = label(er)
        tol = tolerancia if tolerancia is not None else r + 0.15
        def comp_cerca(p):
            i, j = self.idx(p)
            k = int(tol / PASO) + 1
            i0, i1 = max(0, i - k), min(lab.shape[0], i + k + 1)
            j0, j1 = max(0, j - k), min(lab.shape[1], j + k + 1)
            if i0 >= i1 or j0 >= j1:
                return set()
            sub = lab[i0:i1, j0:j1]
            yy, xx = np.mgrid[i0:i1, j0:j1]
            m = ((yy - i) ** 2 + (xx - j) ** 2) * PASO * PASO <= tol * tol
            return set(np.unique(sub[m & (sub > 0)]).tolist())
        c0 = comp_cerca(origen)
        return {n: bool(c0 & comp_cerca(p)) for n, p in destinos.items()}

    def cabe_circulo(self, diam):
        return bool(self.erosion(diam / 2).any())
