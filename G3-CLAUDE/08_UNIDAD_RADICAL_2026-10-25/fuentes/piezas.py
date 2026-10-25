"""Piezas de servicio y mobiliario común. Mismo marco local que la célula: puerta en y=0, interior en +y."""
import math

from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

from geo import T_SERV, Pieza, arco, puerta_corredera


def _inodoro(x, y, giro=0):
    """Inodoro 0,38 x 0,68 con cisterna, apoyado en la pared y (se dibuja hacia +y desde y)."""
    tanque = box(x - 0.19, y, x + 0.19, y + 0.16)
    taza = Point(x, y + 0.42).buffer(0.19, 32)
    taza = Polygon([(x - 0.19, y + 0.16), (x + 0.19, y + 0.16)] + arco(x, y + 0.42, 0.19, 0, -180, 24)[::-1] if False else
                   [(x - 0.19, y + 0.16), (x + 0.19, y + 0.16), (x + 0.19, y + 0.42)] + arco(x, y + 0.42, 0.19, 0, 180, 24)[1:] + [(x - 0.19, y + 0.42)])
    return [tanque, taza]


def bano(nombre, W=1.75, D=2.30, puerta_x=0.10):
    """Baño completo: ducha a lo ancho del fondo (1,75 x 0,85), inodoro y lavabo. Corredera sin barrido interior."""
    p = Pieza(nombre, 'bano', box(0, 0, W, D), t=T_SERV)
    h, hoja, den, fue = puerta_corredera(puerta_x, 0, 0.80, muro=T_SERV, lado='izq' if puerta_x > 0.5 else 'der')
    p.puertas.append((h, 'corredera', {'hoja': hoja}))
    p.entrada, p.acceso_fuera = den, fue
    ducha = box(0, D - 0.85, W, D)
    p.muebles.append(('plato ducha', ducha.exterior, 'proy'))
    p.muebles.append(('mampara', LineString([(0.0, D - 0.85), (W * 0.55, D - 0.85)]), 'grueso'))
    p.muebles.append(('desagüe', Point(W * 0.75, D - 0.42).buffer(0.04, 12).exterior, 'fino'))
    for g in _inodoro(W - 0.32, 0.0):
        g = box(W - 0.16 - 0.0, 0, W, 0)  # marcador vacío para no romper el bucle
    # inodoro contra la pared derecha, mirando a -x
    tan = box(W - 0.16, 0.45, W, 0.83)
    taza = Polygon([(W - 0.16, 0.45), (W - 0.16, 0.83), (W - 0.42, 0.83)] + arco(W - 0.42, 0.64, 0.19, 90, 270, 24)[1:] + [(W - 0.42, 0.45)])
    p.muebles += [('cisterna', tan.exterior, 'proy'), ('inodoro', taza.exterior, 'proy')]
    p.obstaculos += [tan, taza]
    lav = box(0, 0.75, 0.45, 1.30)
    p.muebles += [('lavabo', lav.exterior, 'proy'), ('pila', Point(0.24, 1.025).buffer(0.15, 24).exterior, 'fino')]
    p.obstaculos.append(lav)
    p.destinos['inodoro'] = Point(W - 0.75, 0.64)
    p.destinos['ducha'] = Point(W * 0.75, D - 0.50)
    p.datos = {'titulo': 'baño'}
    return p


def aseo(nombre, W=1.30, D=1.75, puerta_x=0.25):
    """Aseo: inodoro y lavabo (la segunda ducha va en el baño completo)."""
    p = Pieza(nombre, 'aseo', box(0, 0, W, D), t=T_SERV)
    h, hoja, den, fue = puerta_corredera(puerta_x, 0, 0.80, muro=T_SERV, lado='der')
    p.puertas.append((h, 'corredera', {'hoja': hoja}))
    p.entrada, p.acceso_fuera = den, fue
    tan = box(W / 2 - 0.19, D - 0.16, W / 2 + 0.19, D)
    taza = Polygon([(W / 2 - 0.19, D - 0.16), (W / 2 + 0.19, D - 0.16), (W / 2 + 0.19, D - 0.42)]
                   + arco(W / 2, D - 0.42, 0.19, 0, -180, 24)[1:] + [(W / 2 - 0.19, D - 0.42)])
    lav = box(0, 0.55, 0.40, 1.05)
    p.muebles += [('cisterna', tan.exterior, 'proy'), ('inodoro', taza.exterior, 'proy'),
                  ('lavabo', lav.exterior, 'proy'), ('pila', Point(0.21, 0.80).buffer(0.13, 24).exterior, 'fino')]
    p.obstaculos += [tan, taza, lav]
    p.destinos['inodoro'] = Point(W / 2, D - 0.95)
    p.datos = {'titulo': 'aseo'}
    return p


def lavadero(nombre, W=1.30, D=2.00, puerta_x=0.25):
    """Lavar y secar (A04): lavadora, pila y tendedero en un recinto con extracción y fachada. No en el dormitorio."""
    p = Pieza(nombre, 'lavadero', box(0, 0, W, D), t=T_SERV)
    h, hoja, den, fue = puerta_corredera(puerta_x, 0, 0.80, muro=T_SERV, lado='der')
    p.puertas.append((h, 'corredera', {'hoja': hoja}))
    p.entrada, p.acceso_fuera = den, fue
    lav = box(W - 0.62, D - 0.62, W, D)
    p.muebles += [('lavadora', lav.exterior, 'proy'), ('tambor', Point(W - 0.31, D - 0.31).buffer(0.20, 24).exterior, 'fino')]
    p.obstaculos.append(lav)
    for k in range(5):
        y = 0.55 + k * 0.22
        p.muebles.append(('tendedero (sobre)', LineString([(0.10, y), (W - 0.70, y)]), 'sobre'))
    p.destinos['lavadora'] = Point(W - 0.35, D - 1.00)
    p.datos = {'titulo': 'lavar y secar'}
    return p


def patinillo(x, y, a=0.55, b=0.55):
    return box(x, y, x + a, y + b)


# --------------------------------------------------------------- mobiliario del común

def cocina_lineal(x0, y0, L, hacia='+y', fondo=0.65):
    """Bancada lineal de cocina con fregadero, placa y nevera. Devuelve (muebles, obstáculos).
    hacia: lado al que mira quien cocina respecto a la línea de pared (x0,y0)-(x0+L,y0)."""
    s = 1 if hacia == '+y' else -1
    y1 = y0 + s * fondo
    banc = box(x0, min(y0, y1), x0 + L, max(y0, y1))
    nev = box(x0, min(y0, y1), x0 + 0.65, max(y0, y1))
    yc = (y0 + y1) / 2
    m = [('bancada', banc.exterior, 'proy'), ('nevera', nev.exterior, 'proy'),
         ('nevera x', LineString([(x0, min(y0, y1)), (x0 + 0.65, max(y0, y1))]), 'fino'),
         ('fregadero', box(x0 + 0.95, yc - 0.20, x0 + 1.75, yc + 0.20).exterior, 'fino')]
    for i in range(2):
        for j in range(2):
            m.append(('fuego', Point(x0 + L - 0.70 + i * 0.30, yc - 0.13 + j * 0.26).buffer(0.09, 16).exterior, 'fino'))
    m.append(('extracción (sobre)', box(x0 + L - 0.90, min(y0, y1), x0 + L - 0.20, max(y0, y1)).exterior, 'sobre'))
    return m, [banc], banc


def cocina_vertical(x0, y0, L, hacia='+x', fondo=0.65):
    """Igual que cocina_lineal pero sobre una pared vertical x=x0, de y0 a y0+L."""
    s = 1 if hacia == '+x' else -1
    x1 = x0 + s * fondo
    banc = box(min(x0, x1), y0, max(x0, x1), y0 + L)
    xc = (x0 + x1) / 2
    m = [('bancada', banc.exterior, 'proy'),
         ('nevera', box(min(x0, x1), y0, max(x0, x1), y0 + 0.65).exterior, 'proy'),
         ('nevera x', LineString([(min(x0, x1), y0), (max(x0, x1), y0 + 0.65)]), 'fino'),
         ('fregadero', box(xc - 0.20, y0 + 0.95, xc + 0.20, y0 + 1.75).exterior, 'fino')]
    for i in range(2):
        for j in range(2):
            m.append(('fuego', Point(xc - 0.13 + j * 0.26, y0 + L - 0.70 + i * 0.30).buffer(0.09, 16).exterior, 'fino'))
    m.append(('extracción (sobre)', box(min(x0, x1), y0 + L - 0.90, max(x0, x1), y0 + L - 0.20).exterior, 'sobre'))
    return m, [banc], banc


def mesa(cx, cy, L=2.00, A=0.90, giro=0, plazas=6):
    """Mesa con taburetes (círculos). giro en grados."""
    from shapely import affinity
    t = box(cx - L / 2, cy - A / 2, cx + L / 2, cy + A / 2)
    m = [('mesa', t, 'proy')]
    obst = [t]
    n_lado = plazas // 2
    for k in range(n_lado):
        x = cx - L / 2 + L * (k + 0.5) / n_lado
        for s in (-1, 1):
            c = Point(x, cy + s * (A / 2 + 0.28)).buffer(0.19, 24)
            m.append(('taburete', c, 'proy'))
    if giro:
        m = [(n, affinity.rotate(g, giro, origin=(cx, cy)), e) for n, g, e in m]
        obst = [affinity.rotate(g, giro, origin=(cx, cy)) for g in obst]
    m = [(n, g.exterior if hasattr(g, 'exterior') else g, e) for n, g, e in m]
    return m, obst, Point(cx, cy)


def grada(x0, y0, L, escalones=3, huella=0.45, hacia='+y'):
    """Grada doméstica (estar sin sofá, asamblea pequeña): escalones de 0,45 de huella y 0,40 de altura.
    hacia: dirección en la que se sube."""
    m, obst = [], []
    for k in range(escalones):
        if hacia == '+y':
            g = box(x0, y0 + k * huella, x0 + L, y0 + (k + 1) * huella)
        elif hacia == '-y':
            g = box(x0, y0 - (k + 1) * huella, x0 + L, y0 - k * huella)
        elif hacia == '+x':
            g = box(x0 + k * huella, y0, x0 + (k + 1) * huella, y0 + L)
        else:
            g = box(x0 - (k + 1) * huella, y0, x0 - k * huella, y0 + L)
        m.append(('grada +%.2f' % (0.40 * (k + 1)), g.exterior, 'proy'))
        obst.append(g)
    u = unary_union(obst)
    return m, obst, u


def banco_entrada(x0, y0, L, fondo=0.40, vertical=False):
    """Banco y percheros de llegada (A16 llegar con cargas, A18 salir con prisa)."""
    g = box(x0, y0, x0 + fondo, y0 + L) if vertical else box(x0, y0, x0 + L, y0 + fondo)
    return [('banco y percheros', g.exterior, 'proy')], [g]


def armario(x0, y0, L, fondo=0.60, vertical=False, nombre='armario común'):
    g = box(x0, y0, x0 + fondo, y0 + L) if vertical else box(x0, y0, x0 + L, y0 + fondo)
    minx, miny, maxx, maxy = g.bounds
    m = [(nombre, g.exterior, 'proy'), (nombre + ' x', LineString([(minx, miny), (maxx, maxy)]), 'fino')]
    return m, [g]
