"""Genera todo lo de las unidades: vistas, planos B/N, escenas, matriz de cuerpos y el .3dm.

Salida: ../modelos/UNIDADES_H1_H6.3dm · ../vistas/unidades/*.png · ../planos/*.png · ../verificacion/*.json|md
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom3d import Pieza, COL, caja, mover
from cuerpos import CATALOGO, colocar_cuerpo, MEDIO
from unidades import UNIDADES, SX, SY
from escenas3d import ESCENAS_H3, capacidad
from render import axon, cortar, planta_bn, seccion_bn
from rhino_out import Escritor

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
D_MOD, D_VIS, D_PLA, D_VER = [os.path.join(RAIZ, d) for d in ('modelos', 'vistas/unidades', 'planos', 'verificacion')]
for d in (D_MOD, D_VIS, D_PLA, D_VER):
    os.makedirs(d, exist_ok=True)

SEP = 9.0   # separación entre unidades en el .3dm


def z_apoyo(info):
    bx, by, bw, bh = info['blando']
    zf = info.get('z_fn')
    zb = info['z_blando']
    suelo = info.get('suelo_duro')

    def f(x, y):
        dentro = bx <= x <= bx + bw and by <= y <= by + bh
        if zf is not None:
            return zf(x, y) if dentro else 0.0
        if dentro:
            return zb
        return 0.0 if suelo is not None or info['id'] in ('H3', 'H4', 'H1', 'H5') else zb
    return f


def main():
    w = Escritor('G3 · unidades H1–H6 · 25-10-2026 · metros. Mallas de estudio: no son sólidos constructivos.')
    resumen = []
    todas = []
    for k, f in enumerate(UNIDADES):
        base, estados, info = f()
        uid, nombre = info['id'], info['nombre']
        tit = f'{uid} · {nombre}'
        print(uid, nombre)
        # vistas
        axon(base + estados['abierta'], f'{D_VIS}/{uid}_abierta.png', titulo=tit, subtitulo='membrana abierta · axonometría')
        axon(base + estados['cerrada'], f'{D_VIS}/{uid}_cerrada.png', titulo=tit, subtitulo='membrana cerrada')
        if 'media' in estados:
            axon(base + estados['media'], f'{D_VIS}/{uid}_media.png', titulo=tit, subtitulo='membrana media')
        axon(cortar(base + estados['abierta'], 1.60), f'{D_VIS}/{uid}_cortada_160.png', titulo=tit, subtitulo='cortada a +1,60 m · membrana abierta')
        axon(cortar(base + estados['cerrada'], 1.60), f'{D_VIS}/{uid}_cortada_160_cerrada.png', titulo=tit, subtitulo='cortada a +1,60 m · membrana cerrada')
        if 'verano' in estados:
            axon(base + estados['abierta'] + estados['verano'], f'{D_VIS}/{uid}_verano.png', titulo=tit, subtitulo='verano: membrana abierta y tela sobre el cielo')
        if 'dividida' in estados:
            axon(base + estados['dividida'], f'{D_VIS}/{uid}_dividida.png', titulo=tit, subtitulo='los dos turnos coinciden: membrana dividida')
        # planos B/N
        cx, cy = info['centro']
        planta_bn(base + estados['cerrada'], 1.20, f'{D_PLA}/{uid}_planta_1_25.png', escala=25, hoja_cm=(42.0, 29.7), titulo=f'{tit} · planta',
                  nota='corte a +1,20 · negro: cortado · fino: proyección por debajo · cuerpos en 0,18')
        seccion_bn(base + estados['cerrada'], f'{D_PLA}/{uid}_seccion_1_25.png', origen=[cx, cy, 0], normal=[0, 1, 0], escala=25, hoja_cm=(42.0, 29.7),
                   titulo=f'{tit} · sección transversal por el centro', nota='mirando a +y')
        seccion_bn(base + estados['cerrada'], f'{D_PLA}/{uid}_seccion_long_1_25.png', origen=[cx, cy, 0], normal=[1, 0, 0], escala=25, hoja_cm=(42.0, 29.7),
                   titulo=f'{tit} · sección longitudinal por el centro', nota='mirando a +x')
        # escenas de capacidad
        cap = capacidad(info, z_apoyo(info))
        for eid, piezas in cap.items():
            est = 'abierta' if eid == 'E058' else 'cerrada'
            axon(cortar(base + estados[est] + piezas, 1.75), f'{D_VIS}/{uid}_{eid}.png', titulo=tit,
                 subtitulo={'E042': 'E042 · dos cuerpos en la superficie', 'E058': 'E058 · previa de seis', 'E096': 'E096 · tres días sin salir, membrana cerrada'}[eid] + ' · cortada a +1,75')
        # al .3dm
        dx = k * SEP
        pref = f'{uid}::'
        for p in base:
            w.malla(p.copia(dx=dx))
        for est, piezas in estados.items():
            for p in piezas:
                w.malla(p.copia(dx=dx))
        for eid, piezas in cap.items():
            for p in piezas:
                q = p.copia(dx=dx)
                q.capa = f'{uid}::escenas::{eid}'
                w.malla(q)
        if uid == 'H3':
            for eid, titulo, est, fn in ESCENAS_H3:
                piezas = fn(info['z_blando'], f'{uid}::escenas::{eid}')
                axon(cortar(base + estados[est] + piezas, 1.75), f'{D_VIS}/{uid}_escena_{eid}.png', titulo=f'{eid} · {titulo}',
                     subtitulo=f'{tit} · membrana {est} · cortada a +1,75', ancho_cm=24, alto_cm=16)
                for p in piezas:
                    w.malla(p.copia(dx=dx))
        resumen.append({k2: v for k2, v in info.items() if k2 != 'z_fn'} | dict(
            area_blanda=round(info['area_blanda'], 2), area_huella=round(info['area_huella'], 2),
            estados=list(estados.keys()), triangulos=int(sum(len(p.malla.faces) for p in base))))
        todas += [p.copia(dx=dx) for p in base + estados['abierta']]
    # vista de conjunto
    axon(todas, f'{D_VIS}/00_las_seis_unidades.png', titulo='H1–H6 · las seis unidades a la misma escala', subtitulo='membranas abiertas · 15 m² de superficie privada cada una (salvo H5, que marca 15 m² y da un colchón de 2,1 × 2,1)',
         ancho_cm=40, alto_cm=16, az=200, el=28)
    # catálogo de cuerpos en el .3dm
    for i, c in enumerate(CATALOGO):
        x = i * 1.2
        for j, pose in enumerate(['tumbada', 'sentada_suelo', 'de_pie']):
            w.malla(colocar_cuerpo(c, pose, x, -8 - j * 2.8, 0, 90 if pose == 'tumbada' else 0, capa='CUERPOS::' + c.id, nombre=f'{c.id} {c.nombre} · {pose}'))
    w.vista('conjunto', (-20, -25, 18), (22, 2, 1))
    for k, f in enumerate(UNIDADES):
        w.vista(f'H{k + 1}', (k * SEP - 8, -9, 7), (k * SEP + SX / 2, SY / 2, 0.8))
    ruta = w.guardar(f'{D_MOD}/UNIDADES_H1_H6.3dm')
    print('3dm', ruta)
    json.dump(resumen, open(f'{D_VER}/UNIDADES.json', 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
