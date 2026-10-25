# -*- coding: utf-8 -*-
"""FASE FINAL - CAMPANA_VISUAL.pdf: la campana de imagen final integrada como
evidencia espacial (§23-§24, §45). Cycles/OptiX sobre la escena v006 build 12."""
import os
import sys

import matplotlib.image as mpimg

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
import refugio_editorial as E  # noqa: E402

OUT = os.path.join(BASE, '09_RENDERS_Y_REPRESENTACION')
IMG = os.path.join(OUT, '_pipeline', 'hero_FINAL')

# (archivo, tipo, titulo, caption)
PLAN = [
    ('H1_tarde.png', 'HERO', 'La sala de estar urbana',
     'Vista general a nivel de ojo: la cinta, los mástiles y el dosel de hojas sobre el '
     'vacío central conservado. Cámara H1 (1,65 m), tarde.'),
    ('H7_tarde.png', 'HERO', 'Sol desde el aire',
     'Aérea general: el anillo de la cinta, las tres copas C1-C2-C3 y el claro '
     'ceremonial. Cámara H7, tarde.'),
    ('H4_tarde.png', 'HERO', 'El reloj sigue mandando',
     'Hacia Casa de Correos: el dosel enmarca la torre del reloj desde el corredor '
     'visual protegido. Cámara H4, tarde.'),
    ('F1_INTERIOR_DOSEL_tarde.png', 'EXPERIENCIA', 'Debajo de las hojas',
     'Interior del dosel C1: la luz que llega filtrada por las hojas con cámara de '
     'microalgas. Los −28 K de MRT del CLI-03 se ven así. Cámara F1.'),
    ('F3_ATRIO_ESTACION_tarde.png', 'EXPERIENCIA', 'La puerta climática',
     'El atrio del Metro con su marquesina volada: la primera sombra que encuentran '
     '73 millones de viajeros al año. Cámara F3.'),
    ('F4_CARLOS_III_tarde.png', 'EXPERIENCIA', 'El rey en su jardín',
     'Carlos III con el refugio detrás: el monumento conserva su presencia con el '
     'nuevo fondo vegetal. Cámara F4.'),
    ('H5_tarde.png', 'EXPERIENCIA', 'Caminar a seis metros',
     'Sobre la cinta: el mirador en movimiento (CLI-09: 38 °C UTCI — mirador, no '
     'estancia). Cámara H5 a cota de tablero.'),
    ('H3_mediodia.png', 'AGUA', 'La lámina jugable',
     'El splash y los estanques al mediodía: 2.250 m² de agua que evaporan 1.367 kW. '
     'Cámara H3, mediodía.'),
    ('F2_HUERTO_tarde.png', 'VEGETACIÓN', 'El programa más protegido',
     'El huerto C1 (−5,9 K de UTCI, 83 % de sombra): maíz por fases, goteo y mulch '
     'del modelo v006. Cámara F2.'),
    ('F5_DETALLE_NUDO_tarde.png', 'DETALLE', 'El nudo que lo sostiene todo',
     'Mástil-hoja con cables, casquillos y tensores del hiperdetalle 03B.9: el modelo '
     'aguanta la cámara a dos metros. Cámara F5.'),
    ('H2_tarde.png', 'HERO', 'El frente oeste',
     'Las copas C1 desde poniente con la escalera-viga y las jardineras de borde. '
     'Cámara H2, tarde.'),
    ('H6_tarde.png', 'EXPERIENCIA', 'Entre mástiles',
     'El bosque estructural a la altura del peatón, con los pods rosa como faros de '
     'programa. Cámara H6.'),
    ('H1_clay.png', 'ANALÍTICO', 'La sombra, sin maquillaje',
     'CLAY analítico: mismo encuadre que la portada, material neutro — la geometría '
     'de la sombra tal cual la calcula CLI-01, sin color que la disimule.'),
    ('H7_clay.png', 'ANALÍTICO', 'El patrón de sombra desde el aire',
     'CLAY aéreo con el sol PSA de la tarde crítica: la evidencia espacial del mapa '
     'shade_crit_B — cada mancha de este render existe en el ráster, y viceversa.'),
    ('H7_mediodia.png', 'ANALÍTICO', 'Mediodía contra tarde',
     'La misma aérea al mediodía: las sombras cortas explican por qué la ventana '
     'crítica de la tarde gobierna el diseño del dosel.'),
]

doc = E.Doc(os.path.join(OUT, 'CAMPANA_VISUAL.pdf'), 'CAMPAÑA VISUAL FINAL', '09 · RENDERS')
E.portada(doc, 'La campaña final',
          'Quince imágenes Cycles/OptiX sobre la geometría v006 congelada: héroes que '
          'presentan, experiencias que sitúan, analíticos que demuestran y un detalle '
          'que resiste. Ninguna es decoración: cada caption remite a su análisis.',
          '09 · RENDERS Y REPRESENTACIÓN',
          [('IMÁGENES', str(len(PLAN))), ('MOTOR', 'Cycles · OptiX'),
           ('ESCENA', 'v006 build 12'), ('RESOLUCIÓN', '2560×1600')],
          img=os.path.join(IMG, 'H1_tarde.png'), num='CV')

pendientes = []
i = 0
while i < len(PLAN):
    p = doc.page('CAMPAÑA VISUAL')
    y = E.A4H - 0.9
    for _ in range(2):                      # 2 imagenes por pagina
        if i >= len(PLAN):
            break
        fn, tipo, titulo, cap = PLAN[i]
        ruta = os.path.join(IMG, fn)
        if not os.path.exists(ruta):
            pendientes.append(fn)
            i += 1
            continue
        p.text(E.MX, y, tipo, size=6.4, color=E.MAGENTA, tracked=True, weight='bold')
        p.text(E.MX + 1.7, y, titulo, size=10.5, weight='bold')
        y -= 0.16
        ax = p.axes(E.MX, y - 4.35, E.A4W - 2 * E.MX, 4.3)
        ax.imshow(mpimg.imread(ruta), aspect='auto')
        ax.set_xticks([]); ax.set_yticks([])
        y -= 4.48
        y = p.caption(E.MX, y, '', cap, wrap=110, size=6.8)
        y -= 0.12
        i += 1
    doc.add(p)
doc.close()
print('CAMPANA_VISUAL ok', doc.folio, 'pp | pendientes:', pendientes)
