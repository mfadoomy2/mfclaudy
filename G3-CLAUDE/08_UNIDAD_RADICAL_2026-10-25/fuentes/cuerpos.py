"""Catálogo de cuerpos y poses. Los cuerpos son volúmenes de medida (cápsulas y cilindros), no figuras.

Las medidas de partida son hipótesis razonables, no antropometría medida. Cada cuerpo lleva
lo que exige de la unidad: largo y ancho para tumbarse, altura del canto para sentarse y
levantarse, cierre total, zona cálida o fresca, cabida para dos.
"""
import math
from dataclasses import dataclass

import numpy as np
import trimesh

from geom3d import capsula, cilindro, elipsoide, caja, COL, Pieza, girar_z, mover


@dataclass
class Cuerpo:
    id: str
    nombre: str
    estatura: float      # m
    hombros: float       # anchura de hombros / tumbada de lado ≈ espalda
    cadera: float
    grosor: float        # espesor del cuerpo tumbado
    temperatura: str     # 'frio' | 'calor' | 'media'
    libido: str          # 'alta' | 'baja' | 'media'
    movilidad: str       # 'plena' | 'dolor' | 'reducida'
    cierre: str          # 'total' | 'parcial' | 'abierto'  (cuánto necesita cerrarse para vestirse, follar, llorar)
    notas: str = ''

    # Exigencias geométricas derivadas
    @property
    def largo_tumbada(self):
        return self.estatura + 0.25           # pies y cabeza con holgura

    @property
    def ancho_tumbada(self):
        return max(self.hombros, self.cadera) + 0.30   # se da la vuelta sin caerse

    @property
    def ancho_dos(self):
        return 2 * max(self.hombros, self.cadera) + 0.40

    @property
    def canto_sentarse(self):
        # altura de asiento cómoda ≈ 0,26 × estatura; con dolor o movilidad reducida, más alto y con apoyo
        h = 0.26 * self.estatura
        if self.movilidad != 'plena':
            h = max(h, 0.48)
        return (round(h - 0.05, 2), round(h + 0.07, 2))

    @property
    def radio_sentada(self):
        return max(self.cadera, self.hombros) / 2 + 0.05


CATALOGO = [
    Cuerpo('C01', 'alta y delgada', 1.92, 0.46, 0.36, 0.22, 'frio', 'media', 'plena', 'parcial', 'la cama de 2,00 se le queda corta'),
    Cuerpo('C02', 'baja y gorda', 1.56, 0.56, 0.62, 0.34, 'calor', 'media', 'dolor', 'parcial', 'necesita canto alto y ancho para apoyarse'),
    Cuerpo('C03', 'gorda y alta', 1.82, 0.64, 0.70, 0.38, 'calor', 'alta', 'plena', 'total', 'dos cuerpos en 1,25 m no caben'),
    Cuerpo('C04', 'flaca y friolera', 1.64, 0.40, 0.36, 0.20, 'frio', 'baja', 'plena', 'parcial', 'quiere la zona cálida y la membrana cerrada'),
    Cuerpo('C05', 'twink', 1.76, 0.42, 0.34, 0.20, 'media', 'alta', 'plena', 'total', 'recibe; necesita cerrar y que no se oiga'),
    Cuerpo('C06', 'peluda y calurosa', 1.70, 0.50, 0.46, 0.26, 'calor', 'media', 'plena', 'abierto', 'duerme destapada con la membrana abierta y corriente de aire'),
    Cuerpo('C07', 'trans, en transición', 1.74, 0.44, 0.44, 0.22, 'media', 'media', 'plena', 'total', 'se viste y se cuida dentro de la unidad, nunca en un baño compartido; espejo y luz propios'),
    Cuerpo('C08', 'con dolor crónico', 1.68, 0.46, 0.48, 0.26, 'frio', 'baja', 'dolor', 'parcial', 'pasa horas tumbada; necesita apoyo para levantarse y todo al alcance'),
    Cuerpo('C09', 'silla de ruedas', 1.60, 0.46, 0.42, 0.24, 'media', 'media', 'reducida', 'parcial', 'transferencia lateral a la superficie: canto a 0,48–0,50 y 1,50 m de giro'),
    Cuerpo('C10', 'muy musculada', 1.80, 0.58, 0.44, 0.30, 'calor', 'alta', 'plena', 'parcial', 'ancho de hombros 0,58'),
    Cuerpo('C11', 'pareja estable', 1.72, 0.46, 0.42, 0.24, 'media', 'alta', 'plena', 'total', 'dos cuerpos casi todas las noches'),
    Cuerpo('C12', 'con insomnio y ansiedad', 1.66, 0.42, 0.40, 0.22, 'frio', 'baja', 'plena', 'total', 'luz a cualquier hora sin molestar; oscuridad total cuando quiere'),
    Cuerpo('C13', 'embarazada', 1.68, 0.46, 0.52, 0.34, 'calor', 'baja', 'dolor', 'parcial', 'tumbada de lado con apoyo; levantarse con canto'),
    Cuerpo('C14', 'muy baja', 1.48, 0.38, 0.36, 0.20, 'frio', 'media', 'plena', 'parcial', 'el canto a 0,45 le queda alto'),
    Cuerpo('C15', 'sorda', 1.70, 0.44, 0.40, 0.22, 'media', 'media', 'plena', 'parcial', 'la membrana visual importa más que la acústica; luz de aviso'),
    Cuerpo('C16', 'con perro', 1.74, 0.46, 0.42, 0.24, 'media', 'media', 'plena', 'abierto', 'un cuerpo más de 0,40 × 0,70 en la superficie'),
]


def cuerpo_malla(c, pose='tumbada', n=16):
    """Volumen del cuerpo en coordenadas locales: tumbada a lo largo de +x, cabeza en +x, apoyada en z=0."""
    r = c.grosor / 2
    if pose in ('tumbada', 'boca_abajo'):
        m = capsula(0, 0, r, c.estatura, max(c.hombros, c.cadera) / 2, eje='x', n=n)
        m.apply_scale([1, 1, c.grosor / max(c.hombros, c.cadera)])
        return m
    if pose == 'de_lado':
        m = capsula(0, 0, c.hombros / 2, c.estatura, c.hombros / 2, eje='x', n=n)
        m.apply_scale([1, c.grosor / c.hombros * 1.3, 1])
        return m
    if pose == 'reclinada':
        # piernas tumbadas + tronco a 40°
        piernas = capsula(-0.45, 0, r, 0.95, c.cadera / 2, eje='x', n=n)
        piernas.apply_scale([1, 1, c.grosor / c.cadera])
        tronco = capsula(0, 0, 0, 0.85, c.hombros / 2, eje='x', n=n)
        tronco.apply_scale([1, 1, c.grosor / c.hombros])
        tronco.apply_transform(trimesh.transformations.rotation_matrix(math.radians(-40), [0, 1, 0]))
        tronco.apply_translation([0.05, 0, r])
        return trimesh.util.concatenate([piernas, tronco])
    if pose == 'sentada':
        # sentada en un canto: muslos horizontales hacia +x, tronco vertical, pies en z=-h_asiento
        rs = c.radio_sentada
        tronco = cilindro(0, 0, 0, rs, 0.62 * c.estatura * 0.9, n=24)
        cabeza = elipsoide(0, 0, 0.62 * c.estatura * 0.9 + 0.12, 0.10, 0.09, 0.12, n=2)
        muslos = caja(0, -rs, 0, 0.45, 2 * rs, 0.16)
        return trimesh.util.concatenate([tronco, cabeza, muslos])
    if pose == 'sentada_suelo':
        rs = c.radio_sentada + 0.12
        tronco = cilindro(0, 0, 0, c.radio_sentada, 0.55 * c.estatura * 0.9, n=24)
        piernas = cilindro(0, 0, 0, rs + 0.15, 0.18, n=24)
        cabeza = elipsoide(0, 0, 0.55 * c.estatura * 0.9 + 0.12, 0.10, 0.09, 0.12, n=2)
        return trimesh.util.concatenate([tronco, piernas, cabeza])
    if pose == 'de_pie':
        m = capsula(0, 0, c.estatura / 2, c.estatura, c.hombros / 2, eje='z', n=n)
        m.apply_scale([c.grosor / c.hombros, 1, 1])
        return m
    raise ValueError(pose)


def colocar_cuerpo(c, pose, x, y, z=0.0, rot=0.0, color=COL['cuerpo'], capa='cuerpos', nombre=None):
    m = cuerpo_malla(c, pose)
    if rot:
        m = girar_z(m, rot)
    m = mover(m, x, y, z)
    return Pieza(nombre or f'{c.id} {pose}', m, color, capa, 0.95)


def por_id(cid):
    return next(c for c in CATALOGO if c.id == cid)


# Cuerpo medio para las escenas (hipótesis): 1,70 m
MEDIO = Cuerpo('C00', 'medio', 1.70, 0.44, 0.40, 0.23, 'media', 'media', 'plena', 'parcial')
