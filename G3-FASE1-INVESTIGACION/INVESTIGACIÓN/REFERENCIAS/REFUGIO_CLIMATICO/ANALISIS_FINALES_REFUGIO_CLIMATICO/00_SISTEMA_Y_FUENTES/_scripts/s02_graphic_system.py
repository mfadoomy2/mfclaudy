# -*- coding: utf-8 -*-
"""FASE FINAL - S02: FINAL_GRAPHIC_SYSTEM.pdf — el sistema grafico del Refugio,
traducido del ADN IRAXXXDIOS (Stepanka/Tachov) y demostrado con datos v006 reales."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import refugio_editorial as E  # noqa: E402

OUT = os.path.normpath(os.path.join(HERE, '..', '..'))
doc = E.Doc(os.path.join(OUT, '00_SISTEMA_Y_FUENTES', 'FINAL_GRAPHIC_SYSTEM.pdf'),
            'SISTEMA GRÁFICO FINAL', '00 · SISTEMA')

# ---------------------------------------------------------------- PORTADA
E.portada(doc,
          'Sistema gráfico\ndel Refugio',
          'Manual de la familia editorial de los análisis finales. Traducción del ADN '
          'gráfico IRAXXXDIOS (dossieres Štěpánka y Tachov) al lenguaje del Refugio '
          'Climático: serif editorial, versalitas espaciadas, acento magenta y la paleta '
          'del propio modelo — verdes, rosa, agua.',
          '00 · SISTEMA Y FUENTES',
          [('DOCUMENTO', 'FINAL_GRAPHIC_SYSTEM'), ('BASELINE', 'v006 · build 12'),
           ('FAMILIA', 'Georgia'), ('FORMATO', 'A4 vertical')],
          num='00')

# ---------------------------------------------------------------- TIPOGRAFIA + PALETA
p = doc.page('TIPOGRAFÍA Y PALETA')
y = E.A4H - 1.0
y = p.kicker(y, '00.1 · VOZ TIPOGRÁFICA')
y = p.title(y, 'Una sola familia, cuatro registros')
y = p.subtitle(y, 'Georgia en cuatro usos: display en negrita para títulos, cuerpo de '
                  'libro para el texto, versalitas espaciadas para la navegación y '
                  'cifras grandes para la lectura rápida. La jerarquía nace del tamaño '
                  'y el espaciado, nunca de más familias.')
y -= 0.1
p.text(E.MX, y, 'Display 21-30 pt', size=24, weight='bold'); y -= 0.55
p.text(E.MX, y, 'Subtítulo 9,6 pt — la entradilla que explica qué pregunta responde la página.',
       size=9.6, color='#4a4a4a'); y -= 0.3
p.text(E.MX, y, 'Cuerpo 8,6 pt. El texto corrido se compone en columnas de 48-58 caracteres, '
                'con lead-ins en negrita al estilo de los dossieres de concurso.', size=8.6,
       wrap=88); y -= 0.45
p.text(E.MX, y, E.track('VERSALITAS ESPACIADAS 6-7 PT PARA KICKERS, CABECERAS Y ETIQUETAS'),
       size=6.8, color=E.MAGENTA, weight='bold'); y -= 0.30
p.text(E.MX, y, '41,8', size=30, weight='bold')
p.text(E.MX + 1.05, y - 0.07, '%', size=11, color=E.GRAYTX)
p.text(E.MX, y - 0.55, 'CIFRA DE LECTURA RÁPIDA (BIGNUM)', size=6.0, color=E.GRAYTX, tracked=True)
y -= 0.95

y = p.kicker(y, '00.2 · PALETA')
y = p.title(y, 'La tinta manda; el color significa', size=16)
sw = [('TINTA', E.INK), ('MAGENTA', E.MAGENTA), ('ROSA', E.ROSA),
      ('VERDE', E.GREEN), ('HOJA', E.LEAF), ('AGUA', E.AGUA),
      ('PANEL', E.PANEL), ('FILETE', E.HAIR)]
x = E.MX
for lab, c in sw:
    p.rect(x, y - 0.62, 0.78, 0.5, fc=c, ec=E.HAIR)
    p.text(x, y - 0.75, lab, size=5.0, color=E.GRAYTX, tracked=True)
    p.text(x, y - 0.88, c, size=5.4, color=E.GRAYTX)
    x += 0.87
y -= 1.15
y = p.dashlist(E.MX, y, [
    ('Magenta', 'solo señala: kickers, folios, rayas de lista, cabeceras de tabla. Nunca colorea datos.'),
    ('Verde y agua', 'codifican SIEMPRE beneficio climático y sistema hídrico respectivamente.'),
    ('Rojo-calor', 'reservado a los rásters de calor y a los deltas que empeoran.'),
    ('Rosa módulo', 'es el color del propio proyecto construido (pods, cinta) en mapas y diagramas.'),
], wrap=88)

y -= 0.1
y = p.kicker(y, '00.3 · NIVELES DE CONOCIMIENTO (§5)')
x = E.MX
x = p.chip(x, y - 0.1, 'A'); x = p.chip(x, y - 0.1, 'B'); x = p.chip(x, y - 0.1, 'C')
y -= 0.38
p.text(E.MX, y, 'Todo dato publicado lleva su nivel. A = reproducible desde geometría o dato; '
                'B = derivado por modelo; C = escenario plausible pendiente de validación. '
                'Nunca se presenta C como A.', size=8.6, wrap=88)
doc.add(p)

# ---------------------------------------------------------------- RETICULA + COMPONENTES
p = doc.page('RETÍCULA Y COMPONENTES')
y = E.A4H - 1.0
y = p.kicker(y, '00.4 · RETÍCULA')
y = p.title(y, 'A4 · márgenes 16 mm · 12 columnas virtuales', size=15)
# dibuja la reticula
gx0, gx1 = E.MX, E.A4W - E.MX
for i in range(13):
    xx = gx0 + (gx1 - gx0) * i / 12
    p.fig.add_artist(__import__('matplotlib').pyplot.Line2D(
        [xx / E.A4W] * 2, [(y - 2.1) / E.A4H, (y - 0.25) / E.A4H], color=E.PALEAGUA, lw=3,
        transform=p.fig.transFigure))
p.text(E.MX, y - 0.32, 'Los cuerpos habituales: texto a 2 columnas (6+6), ficha a '
                       '2 columnas con etiqueta en margen, mapa a sangre de caja (8-12 col) '
                       'con leyenda y caption debajo, tercios para bignums.', size=8.6, wrap=88)
y -= 2.3

y = p.kicker(y, '00.5 · FICHA (ETIQUETA EN MARGEN)')
colw = (E.A4W - 2 * E.MX - 0.4) / 2
y2 = p.ficha(E.MX, y, [
    ('QUÉ MEDIMOS', 'Holgura libre de paso sobre cada eje peatonal declarado, en metros.'),
    ('MÉTODO', 'Rásterización de la escena v006 a 0,25 m; banda de cuerpo 0,05–2,10 m; '
               'distancia transversal libre por estación de eje cada 0,5 m.'),
    ('RIESGO', 'Los ejes declarados son abstracciones: dos rozan huellas OSM del contexto.'),
], wcol=colw)
y3 = p.ficha(E.MX + colw + 0.4, y, [
    ('FUENTE', '_reaudit9/_data/a1_paths.json · build 12 · 2026-08-13.'),
    ('CERTEZA', 'A — reproducible ejecutando audit_run.py sobre la baseline congelada.'),
], wcol=colw)
y = min(y2, y3) - 0.12

y = p.kicker(y, '00.6 · TABLA')
y = p.tabla(E.MX, y, E.A4W - 2 * E.MX,
            ['ID', 'PREGUNTA', 'RESULTADO', 'NIVEL'],
            [['CLI-04', '¿Cuánto baja el UTCI en el día p95?',
              '−2,5 K de media; −3,4 K con nebulización', 'A/B'],
             ['AGU-03', '¿Litros por persona-hora protegida?',
              'se construye en 04_AGUA (indicador nuevo)', 'B'],
             ['SOC-02', '¿Personas-hora protegidas al día?',
              'modelo LOW/BASE/HIGH en 06_USO_SOCIAL', 'C']],
            col_w=[0.7, 3.1, 2.6, 0.6])
y -= 0.12
y = p.panel(E.MX, y, E.A4W - 2 * E.MX, 0.78, 'PANEL TINTADO · PARA CONTEXTO, ADVERTENCIAS Y ÁMBITOS AMPLIADOS')
p.text(E.MX + 0.16, y, 'El panel hereda el papel cálido de los dossieres. Se usa para lo que '
                       'no es resultado: contexto, salvedades, definiciones.', size=8.0, wrap=92)
doc.add(p)

# ---------------------------------------------------------------- MAPAS con datos reales
p = doc.page('CARTOGRAFÍA')
y = E.A4H - 1.0
y = p.kicker(y, '00.7 · MAPAS')
y = p.title(y, 'El mapa de la casa: contexto gris, dato en color', size=15)
y = p.subtitle(y, 'Demostración con datos v006 reales (build 12): anchura libre local de la '
                  'auditoría y sombra crítica de la simulación climática. Todo mapa lleva '
                  'norte implícito (Y = norte), leyenda propia y caption con fuente.')
geo = E.load_geo()

ax = p.axes(E.MX, y - 3.55, 3.4, 3.3)
E.draw_context(ax, geo)
width = E.np_aud('width.npy'); plaza = E.np_aud('plaza.npy')
im = E.show_raster(ax, np.clip(width, 0, 12), E.CMAP_VERDE, mask=plaza & (width > 0))
E.cbar(p, im, E.MX, y - 3.85, 1.6, 'ANCHURA LIBRE LOCAL · M')

ax2 = p.axes(E.MX + 3.75, y - 3.55, 3.4, 3.3)
E.draw_context(ax2, geo)
shB = E.np_cli('shade_crit_B.npy')
im2 = E.show_raster(ax2, shB, E.CMAP_AGUA, vmin=0, vmax=1)
E.cbar(p, im2, E.MX + 3.75, y - 3.85, 1.6, 'FRACCIÓN DE SOMBRA · VENTANA CRÍTICA')

y -= 4.15
p.caption(E.MX, y, 'Izquierda:', 'anchura libre local (rásters de la auditoría A1, celda 0,25 m). '
          'Derecha: fracción de sombra en la ventana crítica 15 jun – 15 sep (clima v006, celda 0,5 m).',
          fuente='FUENTE: _reaudit9/_data/width.npy · _reclima9/_data/shade_crit_B.npy · baseline v006 build 12')
doc.add(p)

# ---------------------------------------------------------------- REGLAS
p = doc.page('REGLAS')
y = E.A4H - 1.0
y = p.kicker(y, '00.8 · REGLAS DE DIAGRAMACIÓN')
y = p.title(y, 'Doce reglas para toda la familia', size=15)
y = p.dashlist(E.MX, y - 0.05, [
    ('R1', 'Cada documento abre con portada oscura full-bleed y banda de datos.'),
    ('R2', 'Cada página responde UNA pregunta; la pregunta va en el subtítulo.'),
    ('R3', 'Estructura fija de análisis: PREGUNTA · MÉTODO · DATOS · RESULTADOS · LECTURA · CONCLUSIÓN · LIMITACIONES.'),
    ('R4', 'Toda cifra publicada pasa por Doc.metric() y aparece en FINAL_METRICS_REGISTRY.csv.'),
    ('R5', 'Todo dato lleva nivel A/B/C visible. Nunca C disfrazado de A.'),
    ('R6', 'Los mapas comparten encuadre (ámbito −112..100 × −45..78), contexto gris y celda declarada.'),
    ('R7', 'Verde=beneficio climático, agua=sistema hídrico, calor=carga térmica, rosa=proyecto construido, magenta=navegación.'),
    ('R8', 'Redondeo acorde a certeza: nivel C nunca publica decimales que sugieran precisión.'),
    ('R9', 'Doble lectura: bignums+mapas para 30 segundos; ficha+tabla+notas para 30 minutos.'),
    ('R10', 'Los resultados incómodos se publican con el mismo peso tipográfico que los favorables.'),
    ('R11', 'Renders = evidencia espacial con caption y cámara identificada, nunca decoración.'),
    ('R12', 'Fuentes al pie de cada figura: ruta del dato + versión de geometría + fecha.'),
], wrap=84, gap=0.09)
doc.add(p)

doc.close()
print('FINAL_GRAPHIC_SYSTEM.pdf ok · paginas:', doc.folio, '· metricas registradas:', len(doc.metrics))
