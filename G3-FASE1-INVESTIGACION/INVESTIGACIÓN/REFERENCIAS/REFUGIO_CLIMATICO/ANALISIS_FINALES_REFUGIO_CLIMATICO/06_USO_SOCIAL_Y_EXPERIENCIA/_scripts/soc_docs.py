# -*- coding: utf-8 -*-
"""FASE FINAL - PDFs SOC-01..02 + USO_SOCIAL_SINTESIS_INTEGRADA sobre v006."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
sys.path.insert(0, os.path.join(BASE, '01_CLIMA_Y_CONFORT', '_scripts'))
import refugio_editorial as E  # noqa: E402
from cli_common import cabecera_analisis  # noqa: E402

OUT = os.path.join(BASE, '06_USO_SOCIAL_Y_EXPERIENCIA')
with open(os.path.join(OUT, 'B_DATOS', 'soc_stats.json'), encoding='utf-8') as f:
    R = json.load(f)
geo = E.load_geo()
FUENTE = 'FUENTE: soc_engine.py sobre v006 build 12 (IPE explícito, pesos declarados)'

# ================================================================ SOC-01 · IPE
doc = E.Doc(os.path.join(OUT, 'SOC-01_POTENCIAL_DE_ESTANCIA.pdf'),
            'SOC-01 · POTENCIAL DE ESTANCIA', '06 · USO SOCIAL')
E.portada(doc, 'Dónde querrá\nquedarse la gente',
          'Un índice de potencial de estancia con la fórmula a la vista: sombra, '
          'confort, asiento, agua y efecto borde. No es una caja negra: cada peso está '
          'declarado y su sensibilidad, medida.',
          'SOC-01 · USO SOCIAL Y EXPERIENCIA',
          [('IPE MEDIO', str(R['ipe']['media'])),
           ('ESTANCIA ALTA', doc.metric('SOC01-M1', R['ipe']['m2_alto'], 'm²', 'B',
            'celdas IPE>=0.6', 'soc_stats.json')),
           ('ESTABILIDAD PESOS', 'Jaccard ≥ %.2f' % R['sensibilidad_pesos']['jaccard_min']),
           ('NIVEL', 'B')], num='SOC-01')
p, y = cabecera_analisis(
    doc, 'SOC-01', 'El índice que se deja auditar',
    '¿Qué zonas de la plaza reúnen las condiciones que hacen que la gente se quede?',
    R['formula'] + '. Capas: sombra crítica (CLI-01), UTCI E2/16h normalizado (CLI-04), '
    'proximidad a %d líneas de banco y %d puntos de agua (escena v006), efecto borde '
    'Gehl a jardineras/mobiliario. Sensibilidad: cada peso ±50 %%, estabilidad Jaccard '
    'del conjunto IPE≥0,6.' % (R['capas']['bancos'], R['capas']['puntos_agua']),
    'ipe.npy + soc_stats.json.', 'B',
    'El IPE predice CONDICIONES, no comportamiento: el uso real depende de gestión, '
    'programación y estación. Se valida con conteos en el piloto (roadmap).')
ipe = np.load(os.path.join(OUT, 'B_DATOS', 'ipe.npy'))
ax = p.axes(E.MX, y - 3.2, 4.7, 3.05)
E.draw_context(ax, geo)
im = E.show_raster(ax, ipe, E.CMAP_VERDE, vmin=0, vmax=0.8)
E.cbar(p, im, E.MX, y - 3.5, 1.7, 'ÍNDICE DE POTENCIAL DE ESTANCIA · 0-0,8')
yy = p.ficha(E.MX + 5.05, y - 0.1, [
    ('LECTURA', 'La estancia alta (%d m², IPE≥0,6) dibuja tres arcos: bancos bajo dosel, '
     'borde de balsas y huerto-vivero. Coinciden con el refugio térmico: el proyecto '
     'quiere que te quedes exactamente donde te protege.' % R['ipe']['m2_alto']),
    ('ROBUSTEZ', 'Variando cada peso ±50 %%, el conjunto de estancia alta conserva '
     'Jaccard ≥ %.2f: el mapa no es un artefacto de los pesos.' % R['sensibilidad_pesos']['jaccard_min']),
], wcol=2.45, wrap=33)
p.text(E.MX, y - 3.8, FUENTE, size=5.4, color=E.GRAYTX)
doc.add(p)
doc.close()
print('SOC-01 ok', doc.folio, 'pp')

# ================================================================ SOC-02 · PERSONAS-HORA
doc = E.Doc(os.path.join(OUT, 'SOC-02_PERSONAS_HORA_PROTEGIDAS.pdf'),
            'SOC-02 · PERSONAS-HORA', '06 · USO SOCIAL')
ph = R['personas_hora']['escenarios']
E.portada(doc, '¿A cuánta gente\nprotege esto?',
          'El indicador municipal por excelencia: personas-hora de estrés térmico '
          'evitado al día. Tres escenarios con todas las hipótesis sobre la mesa — '
          'nunca una extrapolación vestida de hecho.',
          'SOC-02 · USO SOCIAL Y EXPERIENCIA',
          [('LOW', '%s p·h/día' % f"{ph['LOW']['personas_hora_protegidas_dia']:,}".replace(',', '.')),
           ('BASE', '%s p·h/día' % f"{ph['BASE']['personas_hora_protegidas_dia']:,}".replace(',', '.')),
           ('HIGH', '%s p·h/día' % f"{ph['HIGH']['personas_hora_protegidas_dia']:,}".replace(',', '.')),
           ('NIVEL', 'C — ESCENARIO')], num='SOC-02')
p, y = cabecera_analisis(
    doc, 'SOC-02', 'Personas-hora, no porcentajes',
    '¿Cuántas horas humanas de calor severo evita el refugio en un día de verano?',
    'p·h = afluencia × fracción que se detiene × estancia media × fracción de estancia '
    'en refugio. La fracción en refugio = 36 % de suelo × factor de concentración '
    '(quien se para, elige el confort: el IPE alto está dentro del refugio).',
    'soc_stats.json/personas_hora + refugio.json.', 'C',
    R['personas_hora']['hipotesis'])
rows = [[k, f"{e['afluencia']:,}".replace(',', '.'), '%.0f %%' % (100 * e['se_detiene']),
         '%d min' % e['estancia_min'], '%.0f %%' % (100 * e['frac_estancia_en_refugio']),
         f"{e['personas_hora_protegidas_dia']:,}".replace(',', '.')]
        for k, e in ph.items()]
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['ESCENARIO', 'AFLUENCIA/DÍA', 'SE DETIENE', 'ESTANCIA', 'EN REFUGIO', 'P·H/DÍA'],
            rows, col_w=[1.1, 1.4, 1.1, 1.0, 1.1, 1.3], size=7.4)
doc.metric('SOC02-M1', ph['BASE']['personas_hora_protegidas_dia'], 'p·h/día', 'C',
           'modelo LOW/BASE/HIGH', 'soc_stats.json')
y -= 0.1
y = p.dashlist(E.MX, y, [
    ('En temporada crítica (93 días),', 'el escenario BASE acumula ~200.000 personas-hora '
     'protegidas por verano; el HIGH, ~890.000. El LOW honesto: ~33.000.'),
    ('El indicador es conservador:', 'no cuenta al peatón en tránsito (que también gana '
     '−2,5 K durante su cruce) ni el efecto nocturno de las superficies no recalentadas.'),
    ('Cómo se valida:', 'conteos de estancia georreferenciados en el piloto (fase C del '
     'roadmap) convierten este C en un A en una temporada.'),
], wrap=86, gap=0.1)
y -= 0.06
y = p.panel(E.MX, y, E.A4W - 2 * E.MX, 1.15, 'CÓMO CAMBIARÍA LA EXPERIENCIA DE PUERTA DEL SOL (§15)')
p.text(E.MX + 0.16, y, 'Hoy Sol es un lugar de PASO con 3,4 % de sombra: la estancia '
       'media estival se mide en segundos y la plaza se vacía de 14 a 19 h. El refugio '
       'la convierte en un lugar donde detenerse es térmicamente racional: 1.956 m² de '
       'estancia de alta calidad, agua jugable, un huerto y un mirador. El cambio no es '
       'estético: es de FUNCIÓN — de rotonda peatonal a sala de estar urbana.',
       size=8.4, wrap=94)
doc.add(p)
doc.close()
print('SOC-02 ok', doc.folio, 'pp')

# ================================================================ SINTESIS
doc = E.Doc(os.path.join(OUT, 'USO_SOCIAL_SINTESIS_INTEGRADA.pdf'),
            'USO SOCIAL · SÍNTESIS', '06 · USO SOCIAL')
E.portada(doc, '¿Para quién es\neste refugio?',
          'Síntesis social: potencial de estancia, personas-hora, equidad de acceso y '
          'las fronteras honestas entre lo que el modelo predice y lo que solo el uso '
          'real demostrará.',
          '06 · USO SOCIAL · SÍNTESIS',
          [('VEREDICTO CORTO', 'ESTANCIA DONDE PROTEGE'),
           ('ESTANCIA ALTA', '1.956 m²'), ('P·H BASE', '2.160/día'),
           ('EQUIDAD', 'PMR: 3 ascensores')], num='S-06')
p = doc.page('SÍNTESIS')
y = E.A4H - 1.0
y = p.kicker(y, 'S-06.1 · LO QUE LOS CRUCES ENSEÑAN')
y = p.title(y, 'La estancia sigue al confort — por diseño', size=17)
y = p.dashlist(E.MX, y - 0.02, [
    ('Uso × clima (la correlación buscada, medida):', 'el 90,7 % de la superficie de '
     'estancia alta (IPE≥0,6) cae dentro de la clase REFUGIO EFECTIVO. No es casual: '
     'bancos, agua y borde se proyectaron bajo el dosel. El proyecto no da sombra a la '
     'plaza: da sombra a las RAZONES de quedarse.'),
    ('Uso × movilidad (la fricción evitada):', 'la estancia alta apenas toca los ejes '
     'de paso auditados: quedarse y cruzar no compiten por el mismo suelo.'),
    ('Uso × equidad:', 'a nivel de suelo, el refugio es universal. El nivel +6 depende '
     'de 3 ascensores; y el confort del huerto/vivero — el mejor de la plaza (−5,9 K) — '
     'pide gestión que lo mantenga público y no privatizado por programa.'),
    ('La frontera honesta:', 'todo lo anterior es POTENCIAL (B/C). El comportamiento '
     'real de Madrid — turista, vecino, adolescente, persona mayor — se mide en el '
     'piloto o no se sabe. El plan de monitorización convierte esta incógnita en dato.'),
], wrap=88, gap=0.12)
doc.add(p)
doc.close()
print('SINTESIS SOC ok', doc.folio, 'pp')
