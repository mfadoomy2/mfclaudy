"""La célula privada: el átomo de todas las unidades.

Marco local: suelo libre interior; la puerta está en el muro y=0 (el común queda en y<0)
y la fachada exterior en el muro superior y=D. Medidas en metros.

Regla de anchura: cama (1,25) + paso (0,65) + tablero abierto (1,80) = 3,70 m.
Por debajo de esa anchura el tablero abierto corta el acceso a la cama.
"""
import math

from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

from geo import (CAMA, T_CELDA, TABLERO, Pieza, arco, puerta_batiente,
                 puerta_corredera, segmento_circular)

R_VEST = 1.10        # radio libre del vestidor cóncavo
R_PERSONA = 0.60     # hueco donde se está de pie dentro del vestidor
SAGITA_BOW = 0.65
ASIENTO_BOW = 0.50


def _bow(p, x0, x1, y):
    """Bow en el muro y (fachada), entre x0 y x1; sale hacia +y. Asiento concéntrico por dentro."""
    seg, pts, (cx, cy, r) = segmento_circular((x1, y), (x0, y), SAGITA_BOW)
    a = [math.degrees(math.atan2(q[1] - cy, q[0] - cx)) for q in (pts[0], pts[-1])]
    asiento = LineString(arco(cx, cy, r - ASIENTO_BOW, min(a), max(a), 32))
    p.bows.append({'arco': LineString(pts), 'segmento': seg, 'asiento': asiento})
    p.muebles.append(('asiento bow', asiento, 'proy'))
    p.destinos['bow'] = Point((x0 + x1) / 2, y - 0.05)
    return seg


def _vestidor(p, cx, y):
    """Vestidor cóncavo transitable que asoma por el muro y hacia -y (hacia el común)."""
    dis = Polygon([(cx, y)] + arco(cx, y, R_VEST, 180, 360, 64))
    corona = dis.difference(Point(cx, y).buffer(R_PERSONA, 96))
    rm = (R_VEST + R_PERSONA) / 2
    p.muebles.append(('barra', LineString(arco(cx, y, rm, 180, 360, 48)), 'proy'))
    p.muebles.append(('frente ropa', LineString(arco(cx, y, R_PERSONA, 180, 360, 48)), 'proy_d'))
    for a in range(189, 356, 9):
        t = math.radians(a)
        c = (cx + rm * math.cos(t), y + rm * math.sin(t))
        d = 0.19
        p.muebles.append(('percha', LineString([(c[0] - d * math.cos(t), c[1] - d * math.sin(t)),
                                               (c[0] + d * math.cos(t), c[1] + d * math.sin(t))]), 'fino'))
    p.obstaculos.append(corona)
    p.destinos['vestidor'] = Point(cx, y - 0.15)
    return dis


def _tablero(p, x_pared, y0, hacia=+1):
    """Tablero 1,80 x 0,90 con bisagra en el canto corto, sobre la pared x=x_pared; abre hacia +x o -x.
    Plegado queda vertical contra la pared (7 cm). El taburete va en el lado largo de abajo."""
    L, A = TABLERO
    x1 = x_pared + hacia * L
    abierto = box(min(x_pared, x1), y0, max(x_pared, x1), y0 + A)
    plegado = box(min(x_pared, x_pared + hacia * 0.07), y0, max(x_pared, x_pared + hacia * 0.07), y0 + A)
    p.muebles.append(('tablero plegado', plegado, 'corte_mueble'))
    p.muebles.append(('tablero abierto', abierto.exterior, 'proy_d'))
    p.muebles.append(('bisagra', LineString([(x_pared, y0), (x_pared, y0 + A)]), 'grueso'))
    sx = x_pared + hacia * L * 0.5
    silla = Point(sx, y0 - 0.32).buffer(0.20, 32)
    p.muebles.append(('taburete', silla.exterior, 'proy'))
    p.tablero_abierto, p.tablero_plegado, p.silla = abierto, plegado, silla
    p.destinos['tablero'] = Point(sx, y0 - 0.32)


def _cama(p, g, cabecero='arriba', elevada=False):
    minx, miny, maxx, maxy = g.bounds
    if not elevada:
        p.obstaculos.append(g)
    p.muebles.append(('cama', g.exterior, 'sobre' if elevada else 'proy'))
    alm = {'arriba': box(minx + 0.10, maxy - 0.45, maxx - 0.10, maxy - 0.10),
           'abajo': box(minx + 0.10, miny + 0.10, maxx - 0.10, miny + 0.45)}[cabecero]
    p.muebles.append(('almohada', alm.exterior, 'sobre' if elevada else 'fino'))
    p.muebles.append(('cota cama', g, 'cota_cama'))


def _cargadores(p, x, y):
    """Dos láminas metálicas junto al cabecero, con carga del móvil."""
    for k in (0, 1):
        p.muebles.append(('slab', box(x - 0.02 - k * 0.07, y - 0.30, x - k * 0.07, y), 'corte_mueble'))


def _puerta(p, abierta=False):
    if abierta:
        h, hoja, den, fue = puerta_corredera(0.10, 0, 0.90, muro=T_CELDA, lado='der')
        p.puertas.append((h, 'corredera', {'hoja': hoja}))
    else:
        h, hoja, barr, barr_l, den, fue = puerta_batiente(0.10, 0, 0.80, 'izq', T_CELDA)
        p.puertas.append((h, 'batiente', {'hoja': hoja, 'barrido': barr_l, 'barrido_area': barr}))
    p.entrada, p.acceso_fuera = den, fue


# ---------------------------------------------------------------------------

def celula_tienda(nombre='C', W=3.70, D=3.40, abierta=False):
    """C1 · Tienda. Tablero junto a la bow (luz de frente), paso de 0,60 a la cama con el tablero abierto,
    vestidor que asoma al común con su espalda curva."""
    core = box(0, 0, W, D)
    p = Pieza(nombre, 'celda', core)
    vest = _vestidor(p, W - R_VEST, 0)
    bow = _bow(p, 0.10, 1.80, D)
    p.suelo = unary_union([core, vest, bow])
    _puerta(p, abierta)
    cama = box(W - CAMA[0], D - CAMA[1], W, D)
    _cama(p, cama)
    _cargadores(p, W - CAMA[0] - 0.04, D - 0.12)
    _tablero(p, 0.0, 1.60, +1)
    p.muebles.append(('fondo de cámara', box(0.96, 0.0, W - 2 * R_VEST - 0.04, 0.05), 'textil'))
    p.destinos['cama'] = Point(W - CAMA[0] - 0.30, D - 1.00)
    p.datos = {'clave': 'C4' if abierta else 'C1', 'titulo': 'Se abre al común' if abierta else 'Tienda'}
    return p


def celula_esquina(nombre='C', W=3.70, D=3.60, R=1.70, lado='izq'):
    """C2 · Esquina curva (herencia de la F2). La esquina de fachada se curva y la bow la envuelve:
    asiento en arco con vistas a dos fachadas. Sólo para celdas en esquina de la unidad."""
    q = Polygon([(0, 0), (W, 0), (W, D), (R, D)] + arco(R, D - R, R, 90, 180, 48)[1:] + [(0, D - R)])
    p = Pieza(nombre, 'celda', q)
    vest = _vestidor(p, W - R_VEST, 0)
    pts = arco(R, D - R, R, 98, 172, 40)
    asiento = LineString(arco(R, D - R, R - ASIENTO_BOW, 98, 172, 40))
    p.bows.append({'arco': LineString(pts), 'segmento': None, 'asiento': asiento, 'curva': True})
    p.muebles.append(('asiento bow', asiento, 'proy'))
    p.suelo = unary_union([q, vest])
    _puerta(p)
    cama = box(W - CAMA[0], D - CAMA[1], W, D)
    _cama(p, cama)
    _cargadores(p, W - CAMA[0] - 0.04, D - 0.12)
    _tablero(p, 0.0, 1.20, +1)
    t = math.radians(135)
    p.destinos['bow'] = Point(R + (R - 0.30) * math.cos(t), D - R + (R - 0.30) * math.sin(t))
    p.destinos['cama'] = Point(W - CAMA[0] - 0.30, D - 1.00)
    p.datos = {'clave': 'C2', 'titulo': 'Esquina curva'}
    return p


def celula_cabina(nombre='C', W=2.70, D=3.40):
    """C3 · Cabina alta. La cama sube a +1,10 (queda 1,55 libre encima con 2,90 de altura de planta)
    y el tablero se abre por debajo de ella: puede quedarse abierto siempre (dibujar sin recoger, T16)
    sin cortar el paso a la bow ni a la cama."""
    core = box(0, 0, W, D)
    p = Pieza(nombre, 'celda', core)
    vest = _vestidor(p, W - R_VEST, 0)
    bow = _bow(p, 0.10, 1.40, D)
    p.suelo = unary_union([core, vest, bow])
    _puerta(p)
    cama = box(W - CAMA[0], D - CAMA[1], W, D)
    _cama(p, cama, elevada=True)
    # cajonera bajo el cabecero; el resto bajo la cama queda para el tablero abierto
    caj = box(W - CAMA[0], D - 0.55, W, D)
    p.obstaculos.append(caj)
    p.muebles.append(('cajonera', caj.exterior, 'proy'))
    # bajo la cama, de pie no se pasa (h libre 0,85): se cuenta como ocupado
    p.obstaculos.append(box(W - CAMA[0], D - CAMA[1], W, D - 0.55))
    # tres peldaños laterales que suben hacia +x hasta la cama
    for k in range(3):
        st = box(W - CAMA[0] - 0.40 + k * 0.0, D - 0.85 - (k + 1) * 0.0, W - CAMA[0], D - 0.10)
    peld = []
    for k in range(3):
        g = box(W - CAMA[0] - 0.42 + k * 0.14, D - 0.90, W - CAMA[0] - 0.42 + (k + 1) * 0.14, D - 0.10)
        peld.append(g)
        p.muebles.append(('peldaño', g.exterior, 'proy'))
    p.obstaculos.append(box(W - CAMA[0] - 0.42, D - 0.90, W - CAMA[0], D - 0.10))
    _cargadores(p, W - 0.05, D - 0.12)
    # tablero con bisagra en la pared derecha, bajo la cama, abriendo hacia -x
    L, A = TABLERO
    y0 = 1.55
    abierto = box(W - L, y0, W, y0 + A)
    plegado = box(W - 0.07, y0, W, y0 + A)
    p.muebles.append(('tablero plegado', plegado, 'corte_mueble'))
    p.muebles.append(('tablero abierto', abierto.exterior, 'proy_d'))
    p.muebles.append(('bisagra', LineString([(W, y0), (W, y0 + A)]), 'grueso'))
    silla = Point(W - L * 0.5, y0 - 0.32).buffer(0.20, 32)
    p.muebles.append(('taburete', silla.exterior, 'proy'))
    p.tablero_abierto, p.tablero_plegado, p.silla = abierto, plegado, silla
    p.destinos['tablero'] = Point(W - L * 0.5, y0 - 0.32)
    p.destinos['cama'] = Point(W - CAMA[0] - 0.62, D - 0.55)
    p.datos = {'clave': 'C3', 'titulo': 'Cabina alta'}
    return p


def celula_abierta(nombre='C', W=3.70, D=3.40):
    """C4 · Se abre al común: paño corredero de 0,90 en lugar de puerta batiente."""
    return celula_tienda(nombre, W, D, abierta=True)


TIPOS = {'C1': celula_tienda, 'C2': celula_esquina, 'C3': celula_cabina, 'C4': celula_abierta}
