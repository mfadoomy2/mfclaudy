"""N19B reducida: racimo de 4 personas y su colocación en Ribera de Curtidores 31.
Coordenadas locales de la parcela: origen = eje de la calle frente al n.º 31
(ETRS89 UTM30N X=439984.0, Y=4473229.4), x hacia el fondo (este), y al norte. Metros.
"""
import math
from shapely.geometry import Polygon, box, Point, LineString
from shapely.ops import unary_union
from shapely.affinity import translate, scale, rotate

# ---------------------------------------------------------------- parcela
_C = ("440005.56 4473242.07 440025.56 4473234.35 440031.17 4473232.18 440035.69 4473232.16 "
      "440045.45 4473232.12 440045.55 4473223.74 440042.92 4473223.53 440031.2 4473222.58 "
      "440023.35 4473221.94 440019.61 4473221.92 440016.95 4473221.93 440011.35 4473221.98 "
      "440004.72 4473221.94 440002.5 4473221.93 440001.18 4473221.92 440000.9 4473221.92 "
      "439997.28 4473221.9 439996.07 4473236.83 440004.5 4473236.94 440005.56 4473242.07").split()
X0, Y0 = 439984.0, 4473229.4
PARCELA = Polygon([(float(_C[i]) - X0, float(_C[i + 1]) - Y0) for i in range(0, len(_C), 2)])
# lindero norte (para el retranqueo de 2 m de vistas rectas, art. 582 CC)
LINDERO_N = LineString([(12.07, 7.43), (20.5, 7.54), (21.56, 12.67), (41.56, 4.95), (47.17, 2.78),
                        (51.69, 2.76), (61.45, 2.72)])

# ---------------------------------------------------------------- dimensiones del racimo
W, D = 11.10, 10.80          # caja exterior
EXT, INT = 0.30, 0.10        # muro de fachada / tabique
RW, RD = 3.433, 3.50         # habitación útil (ancho x fondo)

def _room_frame(kind):
    """Devuelve función (u,v)->(x,y) local del racimo C1 y dims (Wu, Dv).
    canónico: ventana en v=0; puerta en el muro v=Dv (tipo O) o en el lateral u=Wu (tipo S)."""
    if kind == 'H1':  # NO, ventana norte, puerta sur
        return (lambda u, v: (0.30 + u, 10.50 - v)), RW, RD, 'O'
    if kind == 'H2':
        return (lambda u, v: (3.833 + u, 10.50 - v)), RW, RD, 'O'
    if kind == 'H3':
        return (lambda u, v: (7.367 + u, 10.50 - v)), RW, RD, 'O'
    if kind == 'H4':  # SO, ventana oeste (calle), puerta norte
        return (lambda u, v: (0.30 + v, 0.30 + u)), RD, RW, 'S'
    if kind == 'H3E':  # NE con ventana al este (para C2 tras el espejo se usa en su NE)
        return (lambda u, v: (10.80 - v, 10.50 - u)), RD, RW, 'S'
    raise KeyError(kind)

def _poly(fr, pts):
    return Polygon([fr(u, v) for u, v in pts])

def _ring_quadrant(cu, cv, r0, r1, a0, a1, n=24):
    pts = [(cu + r1 * math.cos(a0 + (a1 - a0) * i / n), cv + r1 * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    pts += [(cu + r0 * math.cos(a1 - (a1 - a0) * i / n), cv + r0 * math.sin(a1 - (a1 - a0) * i / n)) for i in range(n + 1)]
    return pts

def furnish(kind):
    fr, Wu, Dv, dt = _room_frame(kind)
    rect = _poly(fr, [(0, 0), (Wu, 0), (Wu, Dv), (0, Dv)])
    desk = _poly(fr, [(0.15, 0), (1.75, 0), (1.75, 0.70), (0.15, 0.70)])          # tablero plegable 1600x700
    bed = _poly(fr, [(Wu - 1.25, 0.35), (Wu, 0.35), (Wu, 2.35), (Wu - 1.25, 2.35)])  # colchón 1250x2000
    pillow = _poly(fr, [(Wu - 1.15, 0.42), (Wu - 0.10, 0.42), (Wu - 0.10, 0.72), (Wu - 1.15, 0.72)])
    ward = _poly(fr, _ring_quadrant(1.25, Dv - 1.25, 0.65, 1.25, math.pi / 2, math.pi))  # armario curvo
    chair = Point(fr(0.95, 1.05)).buffer(0.22)
    win = LineString([fr(0.30, 0), fr(Wu - 0.30, 0)])
    if dt == 'O':
        door = LineString([fr(Wu - 1.10, Dv), fr(Wu - 0.30, Dv)])
    else:
        door = LineString([fr(Wu, Dv - 1.10), fr(Wu, Dv - 0.30)])
    free = Point(fr(1.40 if dt == 'O' else 1.35, 1.50)).buffer(0.75)  # círculo libre Ø1,50
    return dict(rect=rect, desk=desk, bed=bed, pillow=pillow, ward=ward, chair=chair, win=win, door=door, free=free)

def cluster_local(mirror=False, ne_east=False):
    """Racimo en coordenadas locales (0..W, 0..D). Sur = medianera. Oeste = fachada principal
    (calle en C1). Este = plataforma/núcleo. mirror=True lo refleja (C2)."""
    rooms = {k: furnish(k) for k in ('H1', 'H2', 'H3', 'H4')}
    b1 = box(8.95, 0.30, 10.80, 2.40)
    b2 = box(7.00, 0.30, 8.85, 2.40)
    interior = box(EXT, EXT, W - EXT, D - EXT)
    solids = unary_union([r['rect'] for r in rooms.values()] + [b1, b2])
    field = interior.difference(solids.buffer(INT, join_style=2))
    field = max(field.geoms, key=lambda g: g.area) if field.geom_type != 'Polygon' else field
    # equipamiento común
    counter = box(3.833, 0.30, 6.30, 0.95)
    fridge = box(6.30, 0.30, 6.90, 0.95)
    hob = box(5.10, 0.42, 5.70, 0.85)
    sink = box(4.10, 0.45, 4.80, 0.85)
    table = box(4.50, 2.55, 6.10, 3.35)
    stools = [Point(x, y).buffer(0.21) for x in (4.9, 5.7) for y in (2.18, 3.72)] + [Point(4.12, 2.95).buffer(0.21), Point(6.48, 2.95).buffer(0.21)]
    sofa = box(0.70, 6.05, 2.90, 6.90)
    sofa_back = box(0.70, 6.65, 2.90, 6.90)
    low = box(1.30, 5.05, 2.30, 5.55)
    coats = box(10.20, 2.50, 10.80, 3.40)   # armario de entrada / consigna
    worktop = box(7.40, 4.05, 9.60, 4.75)  # mesa de trabajo común (turnos)
    # baños: plato, inodoro, lavabo (esquemático)
    def bath(bx, flip):
        x0, y0, x1, y1 = bx.bounds
        shower = box(x0, y0, x0 + 0.90, y0 + 1.20) if not flip else box(x1 - 0.90, y0, x1, y0 + 1.20)
        wc = (box(x1 - 0.55, y0, x1 - 0.15, y0 + 0.65) if not flip else box(x0 + 0.15, y0, x0 + 0.55, y0 + 0.65))
        lav = (box(x1 - 0.50, y1 - 1.15, x1, y1 - 0.55) if not flip else box(x0, y1 - 1.15, x0 + 0.50, y1 - 0.55))
        door = LineString([(x0 + 0.20, y1), (x0 + 0.95, y1)]) if not flip else LineString([(x1 - 0.95, y1), (x1 - 0.20, y1)])
        return dict(rect=bx, shower=shower, wc=wc, lav=lav, door=door)
    baths = {'B1': bath(b1, False), 'B2': bath(b2, True)}
    entry = LineString([(W - EXT, 5.60), (W - EXT, 6.50)])
    windows = [r['win'] for r in rooms.values()]
    windows.append(LineString([(EXT, 4.20), (EXT, 6.60)]))            # estar a la calle
    shaft = [box(7.00, 0.30, 7.25, 0.70), box(10.55, 0.30, 10.80, 0.70)]
    furn = dict(counter=counter, fridge=fridge, hob=hob, sink=sink, table=table, stools=stools,
                sofa=sofa, sofa_back=sofa_back, low=low, coats=coats, worktop=worktop)
    cl = dict(rooms=rooms, baths=baths, field=field, interior=interior, entry=entry, windows=windows,
              furn=furn, shaft=shaft, footprint=box(0, 0, W, D))
    if ne_east:
        # tras el espejo la H3 queda en la esquina NE: su ventana pasa al este (retranqueo norte < 2 m)
        pass
    if mirror:
        cl = _map(cl, lambda g: scale(g, xfact=-1, yfact=1, origin=(W / 2, 0)))
        if ne_east:
            # H1 reflejada ocupa la esquina NE (x 7.367..10.8): ventana este, puerta sur
            r = furnish('H3E')
            cl['rooms']['H1'] = r
            cl['windows'][0] = r['win']
    return cl

def _map(obj, f):
    if isinstance(obj, dict):
        return {k: _map(v, f) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_map(v, f) for v in obj]
    return f(obj)

def place(cl, dx, dy):
    return _map(cl, lambda g: translate(g, dx, dy))

def walls_of(cl):
    """Muros = huella menos huecos útiles; con puertas abiertas (para planta)."""
    solid = cl['footprint']
    holes = unary_union([r['rect'] for r in cl['rooms'].values()] + [b['rect'] for b in cl['baths'].values()] + [cl['field']])
    w = solid.difference(holes)
    cuts = []
    for r in cl['rooms'].values():
        cuts.append(r['door'].buffer(0.16, cap_style=2))
    for b in cl['baths'].values():
        cuts.append(b['door'].buffer(0.16, cap_style=2))
    cuts.append(cl['entry'].buffer(0.36, cap_style=2))
    return w.difference(unary_union(cuts)), unary_union(cuts)

# ---------------------------------------------------------------- planta tipo
YS = -7.30                       # cara de la medianera sur (dentro del lindero en todo el frente)
XC1 = 13.40                      # fachada a la calle
CORE_W, CORE_D = 5.20, 5.20
XCORE = XC1 + W                  # 24.50
XC2 = XCORE + CORE_W             # 29.70

def planta_tipo():
    c1 = place(cluster_local(False), XC1, YS)
    c2 = place(cluster_local(True, ne_east=True), XC2, YS)
    core = box(XCORE, YS, XCORE + CORE_W, YS + CORE_D)
    core_in = box(XCORE + 0.30, YS + 0.30, XCORE + CORE_W - 0.30, YS + CORE_D - 0.30)
    # escalera protegida: 2 tramos de 1,05 m (CTE DB SI 3 / SUA 1), ascensor accesible 1,10 x 1,40 (DB SUA 9)
    sx0 = XCORE + 0.30; sy0 = YS + 0.30
    stair = box(sx0, sy0, sx0 + 2.30, sy0 + 4.60)
    flight_a = box(sx0, sy0 + 1.15, sx0 + 1.05, sy0 + 1.15 + 2.24)
    flight_b = box(sx0 + 1.25, sy0 + 1.15, sx0 + 2.30, sy0 + 1.15 + 2.24)
    treads = [LineString([(sx0, sy0 + 1.15 + 0.28 * i), (sx0 + 1.05, sy0 + 1.15 + 0.28 * i)]) for i in range(9)] + \
             [LineString([(sx0 + 1.25, sy0 + 1.15 + 0.28 * i), (sx0 + 2.30, sy0 + 1.15 + 0.28 * i)]) for i in range(9)]
    lift = box(sx0 + 2.50, sy0 + 2.55, sx0 + 4.60, sy0 + 4.60)       # hueco 2,10 x 2,05
    cabin = box(sx0 + 2.80, sy0 + 2.80, sx0 + 3.90, sy0 + 4.20)       # cabina 1,10 x 1,40
    riser = box(sx0 + 2.50, sy0, sx0 + 4.60, sy0 + 0.90)               # patinillo de instalaciones (bajantes, ventilación)
    # plataforma de planta (abierta, bajo la tela) entre los dos racimos, hasta el lindero norte con 0,5 m
    plat = box(XCORE, YS + CORE_D, XCORE + CORE_W, 20).intersection(PARCELA.buffer(-0.5, join_style=2))
    # vacío de fondo (terrazas comunes / patio-huerto en PB)
    back = PARCELA.difference(box(0, -20, XC2 + W, 30)).buffer(-0.01)
    return dict(c1=c1, c2=c2, core=core, core_in=core_in, stair=stair, flights=[flight_a, flight_b], treads=treads,
                lift=lift, cabin=cabin, riser=riser, plat=plat, back=back)

# niveles (sobre la plaza, +0 = 622,90)
Z0 = 622.90
NIVELES = [8.00, 11.10, 14.20, 17.30, 20.40]
FF = 3.10            # suelo a suelo
CUBIERTA = 23.50
ZOCALO_H = 4.50
