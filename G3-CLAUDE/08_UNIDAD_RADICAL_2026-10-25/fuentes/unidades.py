"""Las seis unidades (H1–H6), cada una con sus estados. Metros. Origen local: esquina de la
superficie privada; la entrada mira a −y.

Superficie privada: 3,45 × 4,35 = 15,0 m² (mínimo normativo de la unidad privativa, NN.UU. Madrid 2023
según G3_unidad_v3_memoria.md; comprobar con el texto oficial).
"""
import math

import numpy as np
from shapely.geometry import Polygon

from geom3d import (Pieza, COL, caja, cilindro, elipsoide, extruir, anillo, rect, elipse, union, resta,
                    relieve, tela_vertical, tubo, mover, girar_z)

SX, SY = 3.45, 4.35          # superficie privada
Z_SUP = 0.45                 # cota de la superficie blanda (asiento)
Z_MESA = 0.72                # cota del canto alto (mesa, repisa)
H_MEMB = 2.40                # altura del aro de la membrana
Z_CIELO = 2.60               # plano del cielo (hueco en la bandeja superior)


def _escalon_entrada(x0, y0, ancho=0.90, fondo=0.30, capa='entrada'):
    return [Pieza('escalón', caja(x0, y0 - fondo, 0, ancho, fondo, Z_SUP / 2), COL['canto'], capa)]


def _cielo(x0, y0, dx, dy, hueco, capa, estado_verano=False):
    losa = extruir(rect(x0, y0, dx, dy).difference(hueco), Z_CIELO, 0.05)
    p = [Pieza('plano del cielo', losa, COL['cielo'], capa + '::cielo', 0.55)]
    if estado_verano:
        p.append(Pieza('tela de verano', extruir(hueco.buffer(0.1), Z_CIELO + 0.15, 0.02), COL['membrana'], capa + '::cielo', 0.5))
    return p


def _membrana_estados(track, z0, z1, capa, cerrada_pts=None):
    """Devuelve dict estado → piezas. `track` es la lista de puntos del aro (cerrado)."""
    pts = list(track)
    n = len(pts)
    estados = {}
    estados['cerrada'] = [Pieza('membrana cerrada', tela_vertical(pts, z0, z1 - z0), COL['membrana'], capa + '::membrana_cerrada', 0.42)]
    mitad = pts[n // 4: 3 * n // 4 + 1]
    estados['media'] = [Pieza('membrana media', tela_vertical(mitad, z0, z1 - z0, cerrada=False), COL['membrana'], capa + '::membrana_media', 0.42)]
    recog = []
    for k in range(4):
        x, y = pts[int(k * n / 4 + n / 8) % n]
        recog.append(Pieza('membrana recogida', cilindro(x, y, z0, 0.11, z1 - z0, 16), COL['membrana2'], capa + '::membrana_abierta', 0.9))
    estados['abierta'] = recog
    return estados


def _aro_y_postes(track, z1, capa, n_postes=4):
    pts = list(track)
    p = [Pieza('aro de la membrana', tubo([(x, y, z1) for x, y in pts] + [(pts[0][0], pts[0][1], z1)], 0.03), COL['plinto'], capa + '::estructura')]
    n = len(pts)
    for k in range(n_postes):
        x, y = pts[int(k * n / n_postes + n / (2 * n_postes)) % n]
        p.append(Pieza('poste', cilindro(x, y, 0, 0.035, z1, 12), COL['plinto'], capa + '::estructura'))
        if k == 0:
            p.append(Pieza('enchufes y luz', caja(x - 0.05, y - 0.05, 0.2, 0.1, 0.1, 0.9), COL['dock'], capa + '::dock'))
    return p


def _dock(x, y, capa, rot=0):
    """Armario-maleta: 0,60 × 0,60 × 2,00, con la maleta dentro."""
    arm = caja(x, y, 0, 0.6, 0.6, 2.0)
    maleta = caja(x + 0.1, y + 0.1, 0.05, 0.4, 0.25, 0.65)
    return [Pieza('armario-maleta', arm, COL['dock'], capa + '::dock', 0.85), Pieza('maleta', maleta, COL['canto'], capa + '::dock')]


# ---------------------------------------------------------------------------

def H1_cama_con_canto():
    """H1 · La cama con canto. Habitación de 3,0 × 5,0 con suelo duro; dentro, una plataforma-cama
    2,4 × 2,4 con canto duro y dosel. Lo más cercano a la unidad-cama."""
    capa = 'H1_cama_con_canto'
    p = []
    # habitación: suelo y tres muros ligeros
    p.append(Pieza('suelo', caja(-0.0, 0.0, -0.05, 3.0, 5.0, 0.05), COL['suelo'], capa + '::suelo'))
    for (x0, y0, dx, dy) in [(-0.08, 0, 0.08, 5.0), (3.0, 0, 0.08, 5.0), (-0.08, 5.0, 3.16, 0.08)]:
        p.append(Pieza('tabique', caja(x0, y0, 0, dx, dy, 2.5), COL['muro'], capa + '::muros', 0.75))
    # frente con puerta de 0,90
    p.append(Pieza('tabique frente', caja(-0.08, -0.08, 0, 1.0, 0.08, 2.5), COL['muro'], capa + '::muros', 0.75))
    p.append(Pieza('tabique frente', caja(1.9, -0.08, 0, 1.18, 0.08, 2.5), COL['muro'], capa + '::muros', 0.75))
    # plataforma-cama
    bx, by, b = 0.30, 2.45, 2.4
    p.append(Pieza('plataforma', caja(bx, by, 0, b, b, Z_SUP - 0.12), COL['plinto'], capa + '::plinto'))
    p.append(Pieza('cajones', caja(bx + 0.05, by - 0.02, 0.08, b - 0.1, 0.02, 0.25), COL['dock'], capa + '::dock'))
    blando = rect(bx + 0.25, by + 0.25, b - 0.5, b - 0.5, 0.08)
    p.append(Pieza('superficie blanda 1,9 × 1,9', extruir(blando, Z_SUP - 0.12, 0.12), COL['blando'], capa + '::superficie'))
    p.append(Pieza('canto', anillo(rect(bx, by, b, b), 0.25, Z_SUP - 0.12, 0.12), COL['canto'], capa + '::canto'))
    p.append(Pieza('repisa de cabecera', caja(bx, by + b - 0.25, Z_SUP, b, 0.25, Z_MESA - Z_SUP), COL['canto'], capa + '::canto'))
    # dosel: postes y telas
    track = [(bx, by), (bx + b, by), (bx + b, by + b), (bx, by + b)]
    tr = list(rect(bx - 0.05, by - 0.05, b + 0.1, b + 0.1).exterior.coords)[:-1]
    # densificar el rectángulo para los estados
    dens = []
    for a, c in zip(tr, tr[1:] + tr[:1]):
        for t in np.linspace(0, 1, 12, endpoint=False):
            dens.append((a[0] + (c[0] - a[0]) * t, a[1] + (c[1] - a[1]) * t))
    p += _aro_y_postes(dens, 2.30, capa)
    estados = _membrana_estados(dens, Z_SUP, 2.30, capa)
    # resto de la habitación: armario-maleta, banco, hueco al cielo
    p += _dock(2.35, 0.05, capa)
    p.append(Pieza('banco', caja(0.0, 0.0, 0, 0.45, 1.6, Z_SUP), COL['canto'], capa + '::canto'))
    cielo = _cielo(-0.08, -0.08, 3.16, 5.16, elipse(bx + b / 2, by + b / 2, 0.8, 0.8), capa)
    p += cielo
    estados['verano'] = _cielo(-0.08, -0.08, 3.16, 5.16, elipse(bx + b / 2, by + b / 2, 0.8, 0.8), capa, True)[1:]
    info = dict(id='H1', nombre='La cama con canto', blando=(bx + 0.25, by + 0.25, b - 0.5, b - 0.5), z_blando=Z_SUP,
                suelo_duro=(0, 0, 3.0, 5.0), huella=(3.08, 5.08), area_blanda=(b - 0.5) ** 2, area_huella=3.16 * 5.16,
                cierre='dosel textil (visual, no acústico)', cielo='óculo Ø 1,6 sobre la cama', sonido='tabiques ligeros', centro=(bx + b / 2, by + b / 2))
    return p, estados, info


def H2_casco():
    """H2 · El casco. Lo único insonorizado del edificio: cápsula de doble piel (0,25) con todo el suelo
    blando, canto-repisa perimetral, esclusa acústica, ventana con contraventana y óculo al cielo."""
    capa = 'H2_casco'
    t = 0.25
    H = 2.55
    p = []
    ext = rect(-t, -t, SX + 2 * t, SY + 2 * t, 0.35)
    intr = rect(0, 0, SX, SY, 0.15)
    casco = extruir(ext, 0, H + t)
    hueco = extruir(intr, -0.01, H + 0.01)
    casco = resta(casco, hueco)
    # puerta en −y, ventana en +x, óculo arriba
    casco = resta(casco, caja(SX / 2 - 0.45, -t - 0.1, 0, 0.9, t + 0.2, 2.1))
    casco = resta(casco, caja(SX - 0.1, 1.2, 0.72, t + 0.2, 1.6, 1.5))
    casco = resta(casco, cilindro(SX / 2, SY / 2, H - 0.1, 0.75, t + 0.3))
    p.append(Pieza('casco de doble piel', casco, COL['muro'], capa + '::casco', 0.8))
    p.append(Pieza('superficie blanda 3,45 × 4,35', extruir(intr, 0, 0.14), COL['blando'], capa + '::superficie'))
    p.append(Pieza('canto-repisa', anillo(intr, 0.30, 0.14, Z_SUP - 0.14), COL['canto'], capa + '::canto'))
    p.append(Pieza('repisa alta', caja(0, SY - 0.30, Z_SUP, SX, 0.30, Z_MESA - Z_SUP), COL['canto'], capa + '::canto'))
    # esclusa acústica
    esc = resta(extruir(rect(SX / 2 - 0.75, -t - 1.4, 1.5, 1.4 + 0.05), 0, 2.3), extruir(rect(SX / 2 - 0.55, -t - 1.2, 1.1, 1.4), -0.01, 2.2))
    esc = resta(esc, caja(SX / 2 - 0.45, -t - 1.5, 0, 0.9, 0.3, 2.1))
    p.append(Pieza('esclusa acústica', esc, COL['muro'], capa + '::casco', 0.8))
    # contraventana y óculo
    estados = {
        'abierta': [Pieza('contraventana abierta', caja(SX + t, 2.85, 0.72, 0.04, 1.6, 1.5), COL['membrana2'], capa + '::membrana_abierta', 0.9),
                    Pieza('óculo abierto', cilindro(SX / 2, SY / 2, H + t, 0.78, 0.02), COL['cielo'], capa + '::membrana_abierta', 0.3)],
        'cerrada': [Pieza('contraventana cerrada', caja(SX + 0.02, 1.2, 0.72, 0.04, 1.6, 1.5), COL['membrana2'], capa + '::membrana_cerrada', 0.9),
                    Pieza('óculo tapado', cilindro(SX / 2, SY / 2, H - 0.05, 0.78, 0.03), COL['membrana'], capa + '::membrana_cerrada', 0.8)],
    }
    estados['media'] = [estados['abierta'][0], estados['cerrada'][1]]
    p += _dock(SX - 0.65, 0.05, capa)
    info = dict(id='H2', nombre='El casco', blando=(0, 0, SX, SY), z_blando=0.14, suelo_duro=None,
                huella=(SX + 2 * t, SY + 2 * t + 1.4), area_blanda=SX * SY, area_huella=(SX + 2 * t) * (SY + 2 * t + 1.4),
                cierre='total: doble piel y esclusa', cielo='óculo Ø 1,5', sonido='aislado (doble piel 0,25; DB-HR por comprobar)', centro=(SX / 2, SY / 2))
    return p, estados, info


def _superficie_base(capa, con_ledge=True, dos_entradas=False):
    """Plinto + superficie blanda + canto bajo (asiento) + canto alto (mesa) + entrada."""
    p = []
    p.append(Pieza('plinto', caja(0, 0, 0, SX, SY, Z_SUP - 0.12), COL['plinto'], capa + '::plinto'))
    p.append(Pieza('superficie blanda 3,45 × 4,35', caja(0, 0, Z_SUP - 0.12, SX, SY, 0.12), COL['blando'], capa + '::superficie'))
    ring = rect(-0.30, -0.30, SX + 0.6, SY + 0.6, 0.10)
    canto = anillo(ring, 0.30, 0, Z_SUP)
    gaps = [caja(SX / 2 - 0.45, -0.35, -0.01, 0.9, 0.4, 1)]
    if dos_entradas:
        gaps.append(caja(SX / 2 - 0.45, SY - 0.05, -0.01, 0.9, 0.4, 1))
    canto = resta(canto, *gaps)
    p.append(Pieza('canto bajo · asiento y paso', canto, COL['canto'], capa + '::canto'))
    p.append(Pieza('escalón', caja(SX / 2 - 0.45, -0.30, 0, 0.9, 0.30, Z_SUP / 2), COL['canto'], capa + '::canto'))
    if dos_entradas:
        p.append(Pieza('escalón', caja(SX / 2 - 0.45, SY, 0, 0.9, 0.30, Z_SUP / 2), COL['canto'], capa + '::canto'))
    if con_ledge:
        for x0 in (-0.30 - 0.35, SX + 0.30):
            p.append(Pieza('canto alto · mesa y repisa', caja(x0, -0.30, 0, 0.35, SY + 0.6, Z_MESA), COL['canto'], capa + '::canto'))
    return p


def H3_superficie():
    """H3 · La superficie silenciosa. 15 m² de suelo blando sin muebles, canto bajo (asiento) y canto alto
    (mesa) alrededor, membrana acústica y visual graduable en un aro, hueco propio al cielo."""
    capa = 'H3_superficie'
    p = _superficie_base(capa)
    track = list(elipse(SX / 2, SY / 2, SX / 2 + 0.52, SY / 2 + 0.52, 64).exterior.coords)[:-1]
    p += _aro_y_postes(track, H_MEMB, capa)
    estados = _membrana_estados(track, Z_SUP, H_MEMB, capa)
    hueco = elipse(SX / 2, SY / 2, 1.0, 0.7)
    p += _cielo(-0.7, -0.6, SX + 1.4, SY + 1.2, hueco, capa)
    estados['verano'] = _cielo(-0.7, -0.6, SX + 1.4, SY + 1.2, hueco, capa, True)[1:]
    p += _dock(-0.65 - 0.6, SY - 0.3, capa)
    info = dict(id='H3', nombre='La superficie silenciosa', blando=(0, 0, SX, SY), z_blando=Z_SUP, suelo_duro=None,
                huella=(SX + 1.3, SY + 0.6), area_blanda=SX * SY, area_huella=(SX + 1.3) * (SY + 0.6),
                cierre='membrana graduable: abierta, media, cerrada', cielo='hueco 2,0 × 1,4 en la bandeja superior',
                sonido='membrana acústica (por caracterizar) + distancia', centro=(SX / 2, SY / 2))
    return p, estados, info


def H4_turno():
    """H4 · El turno. La misma superficie usada por dos personas a horas distintas: dos entradas, dos
    armarios-maleta, membrana divisible por el medio, dos huecos al cielo."""
    capa = 'H4_turno'
    p = _superficie_base(capa, con_ledge=True, dos_entradas=True)
    # dos mitades de color: cálida (noche) y fresca (día)
    p = [q for q in p if not q.nombre.startswith('superficie blanda')]
    p.append(Pieza('superficie · turno de noche', caja(0, 0, Z_SUP - 0.12, SX, SY / 2, 0.12), COL['blando_calido'], capa + '::superficie'))
    p.append(Pieza('superficie · turno de día', caja(0, SY / 2, Z_SUP - 0.12, SX, SY / 2, 0.12), COL['blando_fresco'], capa + '::superficie'))
    track = list(elipse(SX / 2, SY / 2, SX / 2 + 0.52, SY / 2 + 0.52, 64).exterior.coords)[:-1]
    p += _aro_y_postes(track, H_MEMB, capa)
    estados = _membrana_estados(track, Z_SUP, H_MEMB, capa)
    # división central (cuando coinciden los dos turnos)
    div = tela_vertical([(-0.3, SY / 2), (SX + 0.3, SY / 2)], Z_SUP, H_MEMB - Z_SUP, cerrada=False)
    estados['dividida'] = estados['cerrada'] + [Pieza('membrana divisoria', div, COL['membrana2'], capa + '::membrana_dividida', 0.6)]
    p.append(Pieza('aro divisorio', tubo([(-0.3, SY / 2, H_MEMB), (SX + 0.3, SY / 2, H_MEMB)], 0.03), COL['plinto'], capa + '::estructura'))
    h1, h2 = elipse(SX / 2, SY * 0.27, 0.8, 0.55), elipse(SX / 2, SY * 0.73, 0.8, 0.55)
    p += _cielo(-0.7, -0.6, SX + 1.4, SY + 1.2, h1.union(h2), capa)
    estados['verano'] = _cielo(-0.7, -0.6, SX + 1.4, SY + 1.2, h1.union(h2), capa, True)[1:]
    p += _dock(-0.65 - 0.6, -0.3, capa)
    p += _dock(-0.65 - 0.6, SY - 0.3, capa)
    p.append(Pieza('repisa de relevo', caja(SX + 0.65, SY / 2 - 0.6, Z_MESA, 0.35, 1.2, 0.04), COL['dock'], capa + '::dock'))
    info = dict(id='H4', nombre='El turno', blando=(0, 0, SX, SY), z_blando=Z_SUP, suelo_duro=None,
                huella=(SX + 1.3, SY + 0.6), area_blanda=SX * SY, area_huella=(SX + 1.3) * (SY + 0.6),
                cierre='membrana graduable y divisible', cielo='dos huecos 1,6 × 1,1', sonido='membrana + horario pactado', centro=(SX / 2, SY / 2),
                personas=2)
    return p, estados, info


def H5_mochila_y_dock():
    """H5 · La mochila y el dock. El edificio solo da el soporte: 15 m² marcados en el suelo, un bastidor,
    enchufe, armario-maleta y un colchón; la membrana es la tienda de cada una."""
    capa = 'H5_mochila_y_dock'
    p = []
    p.append(Pieza('15 m² marcados', caja(0, 0, -0.02, SX, SY, 0.02), COL['suelo'], capa + '::suelo'))
    for (x, y) in [(0, 0), (SX, 0), (SX, SY), (0, SY)]:
        p.append(Pieza('poste del bastidor', cilindro(x, y, 0, 0.035, H_MEMB, 12), COL['plinto'], capa + '::estructura'))
    p.append(Pieza('bastidor', tubo([(0, 0, H_MEMB), (SX, 0, H_MEMB), (SX, SY, H_MEMB), (0, SY, H_MEMB), (0, 0, H_MEMB)], 0.03), COL['plinto'], capa + '::estructura'))
    p.append(Pieza('colchón 2,1 × 2,1', caja(0.6, 1.0, 0, 2.1, 2.1, 0.12), COL['blando'], capa + '::superficie'))
    p += _dock(SX - 0.6, SY - 0.6, capa)
    p.append(Pieza('enchufes y luz', caja(SX - 0.08, SY - 0.75, 0.2, 0.08, 0.1, 0.9), COL['dock'], capa + '::dock'))
    p.append(Pieza('gancho', tubo([(SX / 2, SY / 2, H_MEMB), (SX / 2, SY / 2, H_MEMB - 0.5)], 0.015), COL['plinto'], capa + '::estructura'))
    # la tienda (membrana propia)
    tienda = elipsoide(1.65, 2.05, 0.0, 1.25, 1.25, 1.35)
    tienda = resta(tienda, caja(0, 0, -2, 4, 5, 2))
    tienda_in = elipsoide(1.65, 2.05, 0.0, 1.21, 1.21, 1.31)
    tienda = resta(tienda, tienda_in)
    estados = {
        'cerrada': [Pieza('tienda 2,5 × 2,5', tienda, COL['membrana'], capa + '::membrana_cerrada', 0.5)],
        'abierta': [Pieza('tienda plegada', caja(SX - 1.3, SY - 0.55, 0, 0.6, 0.25, 0.25), COL['membrana2'], capa + '::membrana_abierta', 0.9)],
    }
    estados['media'] = [Pieza('tienda abierta por un lado', resta(tienda, caja(0, 0, 0, 2.0, 2.05, 1.0)), COL['membrana'], capa + '::membrana_media', 0.5)]
    info = dict(id='H5', nombre='La mochila y el dock', blando=(0.6, 1.0, 2.1, 2.1), z_blando=0.12, suelo_duro=(0, 0, SX, SY),
                huella=(SX, SY), area_blanda=2.1 * 2.1, area_huella=SX * SY,
                cierre='la tienda propia (visual)', cielo='abierto: no hay techo propio', sonido='ninguno', centro=(1.65, 2.05))
    return p, estados, info


def H6_topografia():
    """H6 · La topografía. La superficie no es plana: una concha cálida para tumbarse, un lomo-respaldo,
    una meseta dura para el portátil y una cúpula textil con óculo. Superstudio a 15 m², con cuerpo."""
    capa = 'H6_topografia'
    p = []
    cx, cy = 1.55, 1.95

    def z(x, y):
        base = 0.42
        concha = -0.22 * math.exp(-(((x - cx) / 1.05) ** 2 + ((y - cy) / 0.8) ** 2))
        lomo = 0.33 * math.exp(-((x - SX + 0.05) / 0.55) ** 2) * (0.5 + 0.5 * math.tanh((y - 1.2) / 0.5))
        lomo2 = 0.28 * math.exp(-((y - SY + 0.05) / 0.5) ** 2)
        return base + concha + lomo + lomo2

    p.append(Pieza('relieve blando', relieve(0, 0, SX, SY, z, 44, 56, base=0.0), COL['blando'], capa + '::superficie'))
    def z_concha(x, y):
        dentro = ((x - cx) / 0.95) ** 2 + ((y - cy) / 0.72) ** 2 <= 1
        return z(x, y) + (0.008 if dentro else -0.08)
    p.append(Pieza('concha cálida', relieve(cx - 1.0, cy - 0.78, 2.0, 1.56, z_concha, 30, 26, base=0.05), COL['blando_calido'], capa + '::superficie'))
    p.append(Pieza('lomo fresco', relieve(SX - 0.5, 1.3, 0.5, SY - 1.3, lambda x, y: z(x, y) + 0.008, 8, 30, base=0.05), COL['blando_fresco'], capa + '::superficie'))
    p.append(Pieza('meseta dura · portátil', caja(0.0, SY - 0.9, 0, 1.1, 0.9, Z_MESA), COL['canto'], capa + '::canto'))
    p.append(Pieza('canto de entrada', caja(SX / 2 - 0.45, -0.3, 0, 0.9, 0.3, 0.22), COL['canto'], capa + '::canto'))
    # cúpula textil con óculo
    def cupula(*recortes):
        sol = elipsoide(SX / 2, SY / 2, 0.0, SX / 2 + 0.55, SY / 2 + 0.55, 2.55)
        sol = resta(sol, caja(-2, -2, -3, 8, 9, 3), cilindro(SX / 2, SY / 2, 2.0, 0.75, 1.0), *recortes)
        inner = elipsoide(SX / 2, SY / 2, 0.0, SX / 2 + 0.52, SY / 2 + 0.52, 2.52)
        return resta(sol, inner)
    estados = {
        'cerrada': [Pieza('cúpula cerrada', cupula(caja(SX / 2 - 0.5, -1.0, 0, 1.0, 1.0, 2.0)), COL['membrana'], capa + '::membrana_cerrada', 0.42)],
        'abierta': [Pieza('cúpula abierta', cupula(caja(-3, -3, -0.1, 9, 3 + SY / 2 + 0.2, 1.9)), COL['membrana'], capa + '::membrana_abierta', 0.42)],
        'media': [Pieza('cúpula media', cupula(caja(-3, -3, -0.1, 3 + SX / 2 + 0.2, 9, 1.9)), COL['membrana'], capa + '::membrana_media', 0.42)],
    }
    estados['verano'] = [Pieza('óculo tapado', cilindro(SX / 2, SY / 2, 2.58, 0.9, 0.02), COL['membrana'], capa + '::cielo', 0.5)]
    p.append(Pieza('óculo', cilindro(SX / 2, SY / 2, 2.52, 0.78, 0.015), COL['cielo'], capa + '::cielo', 0.3))
    p += _dock(SX + 0.7, SY - 0.6, capa)
    info = dict(id='H6', nombre='La topografía', blando=(0, 0, SX, SY), z_blando=0.42, suelo_duro=None,
                huella=(SX + 1.1, SY + 1.1), area_blanda=SX * SY, area_huella=(SX + 1.1) * (SY + 1.1),
                cierre='cúpula textil con paso', cielo='óculo Ø 1,5', sonido='cúpula (por caracterizar)', centro=(cx, cy),
                z_fn=z)
    return p, estados, info


UNIDADES = [H1_cama_con_canto, H2_casco, H3_superficie, H4_turno, H5_mochila_y_dock, H6_topografia]
