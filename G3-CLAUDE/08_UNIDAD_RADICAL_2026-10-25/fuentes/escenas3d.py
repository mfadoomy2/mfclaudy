"""Escenas habitadas: cuerpos y objetos colocados dentro de las unidades.

Las diez escenas de prueba van en H3 (coordenadas locales de H3). Las tres escenas de capacidad
(E042 dos en la cama, E058 previa de seis, E096 tres días sin salir) se colocan en todas las unidades
a partir de su rectángulo blando.
"""
import math

from geom3d import Pieza, COL, caja, cilindro, mover
from cuerpos import MEDIO, por_id, colocar_cuerpo, Cuerpo


def portatil(x, y, z, rot=0, capa='escena'):
    base = caja(x - 0.165, y - 0.115, z, 0.33, 0.23, 0.015)
    pant = caja(x - 0.165, y + 0.10, z, 0.33, 0.015, 0.22)
    p = [Pieza('portátil', base, COL['canto'], capa), Pieza('pantalla', pant, COL['cielo'], capa)]
    if rot:
        from geom3d import girar_z
        for q in p:
            q.malla = girar_z(q.malla, rot, (x, y, z))
    return p


def movil(x, y, z, capa='escena'):
    return [Pieza('móvil', caja(x - 0.035, y - 0.075, z, 0.07, 0.15, 0.008), COL['cielo'], capa)]


def plato(x, y, z, capa='escena'):
    return [Pieza('plato', cilindro(x, y, z, 0.13, 0.02, 24), COL['suelo'], capa)]


def bolsa(x, y, z, capa='escena'):
    return [Pieza('bolsa de comida', caja(x - 0.15, y - 0.12, z, 0.3, 0.24, 0.28), COL['dock'], capa)]


def altavoz(x, y, z, capa='escena'):
    return [Pieza('altavoz', cilindro(x, y, z, 0.05, 0.16, 16), COL['canto'], capa)]


# --- las diez escenas de H3 -------------------------------------------------
# cada escena: (id, título, estado de membrana, función que devuelve piezas dado (z_top, capa))

def _E006(z, capa):
    c = por_id('C07')
    p = [colocar_cuerpo(c, 'sentada_suelo', 1.0, 1.4, z, 0, capa=capa)]
    p += portatil(1.0, 2.0, z + 0.25, capa=capa)
    return p


def _E029(z, capa):
    p = [colocar_cuerpo(por_id('C02'), 'reclinada', 1.7, 2.9, z, 90, capa=capa)]
    p += plato(1.45, 2.4, z + 0.05, capa=capa) + portatil(1.9, 1.6, z + 0.02, capa=capa)
    return p


def _E035(z, capa):
    c = por_id('C05')
    p = [colocar_cuerpo(c, 'sentada_suelo', 2.95, 1.0, z, 0, capa=capa)]
    p += portatil(3.45 + 0.30 + 0.17, 1.0, 0.72, 90, capa=capa)   # en el canto alto
    return p


def _E042(z, capa):
    c = por_id('C11')
    return [colocar_cuerpo(c, 'tumbada', 1.7, 1.55, z, 0, capa=capa),
            colocar_cuerpo(c, 'de_lado', 1.7, 2.25, z, 0, color=COL['cuerpo2'], capa=capa)]


def _E058(z, capa):
    p = []
    ids = ['C01', 'C02', 'C05', 'C06', 'C10', 'C14']
    for k, cid in enumerate(ids):
        a = 2 * math.pi * k / 6
        p.append(colocar_cuerpo(por_id(cid), 'sentada_suelo', 1.725 + 1.0 * math.cos(a), 2.175 + 1.1 * math.sin(a), z, 0,
                                color=COL['cuerpo'] if k % 2 else COL['cuerpo2'], capa=capa))
    p += altavoz(1.725, 2.175, z, capa=capa) + movil(2.1, 2.0, z + 0.01, capa=capa)
    return p


def _E096(z, capa):
    p = [colocar_cuerpo(por_id('C12'), 'de_lado', 1.7, 2.6, z, 0, capa=capa)]
    p += bolsa(1.725, -0.55, 0.0, capa=capa) + movil(1.0, 2.3, z + 0.01, capa=capa)
    return p


def _E117(z, capa):
    p = [colocar_cuerpo(por_id('C08'), 'reclinada', 1.5, 3.2, z, 0, capa=capa)]
    p += portatil(2.5, 3.2, z + 0.02, 90, capa=capa)
    return p


def _E134(z, capa):
    p = []
    for k, (cid, y) in enumerate([('C03', 1.3), ('C10', 2.2), ('C14', 3.1)]):
        p.append(colocar_cuerpo(por_id(cid), 'sentada_suelo', 2.6, y, z, 0, color=COL['cuerpo'] if k % 2 else COL['cuerpo2'], capa=capa))
    p += portatil(3.45 + 0.30 + 0.17, 2.2, 0.72, 90, capa=capa)
    return p


def _E140(z, capa):
    p = [colocar_cuerpo(por_id('C04'), 'boca_abajo', 1.7, 2.3, z, 90, capa=capa)]
    p.append(Pieza('tableta', caja(1.55, 3.3, z + 0.02, 0.3, 0.2, 0.01), COL['cielo'], capa))
    return p


def _E149(z, capa):
    p = [colocar_cuerpo(por_id('C15'), 'reclinada', 1.7, 2.8, z, 90, capa=capa),
         colocar_cuerpo(por_id('C16'), 'de_pie', 1.725, -0.75, 0.0, 0, color=COL['cuerpo2'], capa=capa)]
    p.append(Pieza('perro', caja(1.3, 0.3, z, 0.7, 0.4, 0.3), COL['cuerpo2'], capa))
    return p


ESCENAS_H3 = [
    ('E006', 'entrevista de trabajo desde la cama hecha; la membrana cerrada detrás es el fondo de cámara', 'media', _E006),
    ('E029', 'cena en la cama viendo una serie, plato sobre la rodilla, luz apagada', 'cerrada', _E029),
    ('E035', 'juego online con cascos y micro hasta las 3; el portátil sobre el canto alto', 'cerrada', _E035),
    ('E042', 'una amiga sin sitio donde dormir: dos cuerpos en la superficie', 'cerrada', _E042),
    ('E058', 'previa: seis personas sentadas en la superficie, un altavoz pequeño', 'abierta', _E058),
    ('E096', 'tres días sin salir; la comida se deja en el escalón de entrada', 'cerrada', _E096),
    ('E117', 'asamblea online del comité de barrio desde la cama, cámara apagada', 'media', _E117),
    ('E134', 'partido entre tres en una pantalla de 13 pulgadas apoyada en el canto', 'abierta', _E134),
    ('E140', 'dibujar con la tableta boca abajo', 'media', _E140),
    ('E149', 'puerta abierta a propósito: alguien entra a hablar; el perro en la superficie', 'abierta', _E149),
]


# --- escenas de capacidad para cualquier unidad -----------------------------

def capacidad(info, z_de):
    """Devuelve dict escena → piezas, usando el rectángulo blando de la unidad. z_de(x, y) da la cota de apoyo."""
    bx, by, bw, bh = info['blando']
    cx, cy = bx + bw / 2, by + bh / 2
    along = 0 if bw >= bh else 90         # eje largo
    out = {}
    c = por_id('C11')
    sep = 0.62
    if along == 0:
        out['E042'] = [colocar_cuerpo(c, 'tumbada', cx, cy - sep / 2, z_de(cx, cy - sep / 2), 0, capa='escena'),
                       colocar_cuerpo(c, 'de_lado', cx, cy + sep / 2, z_de(cx, cy + sep / 2), 0, color=COL['cuerpo2'], capa='escena')]
    else:
        out['E042'] = [colocar_cuerpo(c, 'tumbada', cx - sep / 2, cy, z_de(cx - sep / 2, cy), 90, capa='escena'),
                       colocar_cuerpo(c, 'de_lado', cx + sep / 2, cy, z_de(cx + sep / 2, cy), 90, color=COL['cuerpo2'], capa='escena')]
    p = []
    for k, cid in enumerate(['C01', 'C02', 'C05', 'C06', 'C10', 'C14']):
        a = 2 * math.pi * k / 6
        x, y = cx + 1.0 * math.cos(a), cy + 1.05 * math.sin(a)
        p.append(colocar_cuerpo(por_id(cid), 'sentada_suelo', x, y, z_de(x, y), 0, color=COL['cuerpo'] if k % 2 else COL['cuerpo2'], capa='escena'))
    out['E058'] = p
    out['E096'] = [colocar_cuerpo(por_id('C12'), 'de_lado', cx, cy, z_de(cx, cy), along, capa='escena')]
    return out
