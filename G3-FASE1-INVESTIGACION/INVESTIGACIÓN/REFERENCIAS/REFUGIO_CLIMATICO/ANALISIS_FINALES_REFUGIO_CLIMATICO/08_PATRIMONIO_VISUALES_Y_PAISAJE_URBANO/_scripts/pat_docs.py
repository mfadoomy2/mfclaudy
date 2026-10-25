# -*- coding: utf-8 -*-
"""FASE FINAL - PAT-01 + PATRIMONIO_SINTESIS_INTEGRADA sobre v006."""
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

OUT = os.path.join(BASE, '08_PATRIMONIO_VISUALES_Y_PAISAJE_URBANO')
with open(os.path.join(OUT, 'B_DATOS', 'pat_stats.json'), encoding='utf-8') as f:
    R = json.load(f)
geo = E.load_geo()
F9 = os.path.normpath(os.path.join(BASE, '..', 'FASE_03B9_HYPERDETAIL_V006'))
FUENTE = 'FUENTE: _reaudit9/a7_views.json (2.455 puntos, malla 2 m) × ipe.npy · v006 build 12'

doc = E.Doc(os.path.join(OUT, 'PAT-01_VISIBILIDAD_HITOS.pdf'),
            'PAT-01 · VISIBILIDAD', '08 · PATRIMONIO')
E.portada(doc, 'El reloj, la torre\ny la fachada',
          'Cuánto patrimonio se ve con el refugio puesto — medido por superficie, '
          'ponderado por uso real y con el hallazgo incómodo publicado: donde mejor se '
          'está, menos se ve el reloj.',
          'PAT-01 · PATRIMONIO Y VISUALES',
          [('RELOJ (SUPERFICIE)', '41,5 %'),
           ('RELOJ (POR USO)', doc.metric('PAT01-M1', 33.6, '%', 'B',
            'vis x IPE', 'pat_stats.json')),
           ('DESDE ESTANCIA ALTA', '25,5 %'), ('MIRADORES', '896 m²')], num='PAT-01')
p, y = cabecera_analisis(
    doc, 'PAT-01', 'Ver el reloj o estar a gusto: casi nunca ambos',
    '¿Qué visibilidad de los tres hitos queda, y qué visibilidad EXPERIMENTA quien usa '
    'la plaza — no quien la sobrevuela en estadística?',
    'Trazado de rayos de la auditoría A7 (2.455 puntos a 1,60 m contra la escena '
    'completa) para reloj, torre y fachada de Correos; ponderación por el índice de '
    'estancia (SOC-01): pct_ponderado = Σ(vis·IPE)/Σ(IPE).',
    'a7_views.json + ipe.npy.', 'A',
    'El estado actual (sin proyecto) tiene visibilidad cuasi-total desde el vacío '
    'central: la reducción al 41-48 % es real y no se maquilla. No hay análisis del '
    'skyline lejano (corredores desde Alcalá/Arenal exteriores): pendiente declarado.')
rows = [[h, '%s %%' % d['pct_superficie'], '%s %%' % d['pct_ponderado_uso'],
         '%s %%' % d['pct_en_estancia_alta']] for h, d in R['ponderada'].items()]
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['HITO', 'POR SUPERFICIE', 'PONDERADA POR USO', 'DESDE ESTANCIA ALTA'],
            rows, col_w=[1.6, 1.7, 1.9, 1.8], size=7.6)
y -= 0.1
y = p.dashlist(E.MX, y, [
    ('El hallazgo (§43, publicado sin suavizar):', 'la ponderación por uso EMPEORA la '
     'visibilidad del reloj (41,5  ›  33,6 %) y desde la estancia alta cae al 25,5 %. '
     'El mismo dosel que fabrica el confort tapa la contemplación: confort y patrimonio '
     'COMPITEN en este proyecto.'),
    ('La excepción:', 'la fachada completa de Correos aguanta (48 % en todas las '
     'métricas): es demasiado grande para taparla.'),
    ('Los miradores existen:', '896 m² combinan IPE≥0,5 Y vista del reloj (el 30 % de la '
     'estancia buena) — arcos en el borde sur del dosel y el claro central.'),
    ('Modificación potencial documentada (§54, NO implementada):', 'orientar 2-3 líneas '
     'de banco hacia los corredores visuales del reloj costaría cero térmicamente y '
     'subiría la visibilidad ponderada ~5 puntos. Para el proyecto de ejecución.'),
], wrap=86, gap=0.11)
doc.add(p)

# mapa de miradores
p = doc.page('PAT-01 · MIRADORES')
y = E.A4H - 1.0
y = p.kicker(y, 'PAT-01.2 · EL MAPA DE LOS MIRADORES')
y = p.title(y, 'Dónde se puede estar bien Y ver el reloj', size=16)
with open(os.path.join(F9, '_reaudit9', '_data', 'a7_views.json'), encoding='utf-8') as f:
    a7 = json.load(f)
ipe = np.load(os.path.join(BASE, '06_USO_SOCIAL_Y_EXPERIENCIA', 'B_DATOS', 'ipe.npy'))
pts = np.array(a7['pts']); vis = np.array(a7['vis']['RELOJ'], bool)
X0, Y0, CS = -112, -45, 0.5
w = np.array([ipe[int((py - Y0) / CS), int((px - X0) / CS)]
              if 0 <= int((py - Y0) / CS) < ipe.shape[0] and 0 <= int((px - X0) / CS) < ipe.shape[1]
              else np.nan for px, py in pts])
w = np.nan_to_num(w)
ax = p.axes(E.MX, y - 3.4, 5.2, 3.25)
E.draw_context(ax, geo)
ax.scatter(pts[~vis][:, 0], pts[~vis][:, 1], s=1.2, c='#ddd6cc')
ax.scatter(pts[vis & (w < 0.5)][:, 0], pts[vis & (w < 0.5)][:, 1], s=1.6, c=E.PALEAGUA)
mir = vis & (w >= 0.5)
ax.scatter(pts[mir][:, 0], pts[mir][:, 1], s=3.2, c=E.MAGENTA)
ax.plot(-25.2, -34.35, '*', ms=12, c=E.INK)
p.caption(E.MX, y - 3.65, 'Magenta: los 896 m² de mirador (estancia + vista del reloj ★).',
          'Gris: sin vista. Agua pálida: vista sin calidad de estancia. La contemplación '
          'cómoda del reloj es un recurso ESCASO del proyecto: se cartografía para '
          'protegerlo en la ejecución.', fuente=FUENTE, wrap=95)
doc.add(p)
doc.close()
print('PAT-01 ok', doc.folio, 'pp')

# síntesis breve
doc = E.Doc(os.path.join(OUT, 'PATRIMONIO_SINTESIS_INTEGRADA.pdf'),
            'PATRIMONIO · SÍNTESIS', '08 · PATRIMONIO')
E.portada(doc, '¿Respeta el lugar?',
          'Síntesis patrimonial: visibilidad de los hitos, atrio del Metro, distancia '
          'de respeto a las fachadas y el trade-off confort-contemplación.',
          '08 · PATRIMONIO · SÍNTESIS',
          [('VEREDICTO CORTO', 'RESPETA, CON UN COSTE VISUAL MEDIDO'),
           ('PENETRACIONES', '0 (auditado)'), ('AIRE A FACHADAS', '~2,0 m ECI'),
           ('COSTE', 'reloj −38 % ponderado')], num='S-08')
p = doc.page('SÍNTESIS')
y = E.A4H - 1.0
y = p.kicker(y, 'S-08.1 · LO QUE LOS CRUCES ENSEÑAN')
y = p.title(y, 'Tocar Sol sin tocar Sol', size=17)
y = p.dashlist(E.MX, y - 0.02, [
    ('Cero contacto físico:', 'la auditoría A12 verifica 0 penetraciones en volumetría '
     'construida real (35 edificios, alturas reales); el aire libre a la fachada del '
     'ECI es ~2,0 m y los zócalos de contexto se emiten por arista para no invadir '
     'las bocacalles (build 12).'),
    ('El atrio del Metro se trata como umbral,', 'no como obstáculo: marquesina volada '
     'hacia la aproximación, bolardos luminosos, canal de drenaje recortado contra el '
     'polígono real de la estación.'),
    ('El coste patrimonial verdadero es VISUAL', 'y está medido: el reloj pasa de '
     'visibilidad cuasi-total a 41,5 % de superficie (33,6 % ponderada por uso). Los '
     '896 m² de mirador son la moneda de cambio cartografiada.'),
    ('Patrimonio × clima (el cruce de fondo):', 'el proyecto apuesta a que una plaza '
     'USABLE en agosto vale más que una postal permanente. Es una decisión política '
     'legítima — y este dossier la deja tomada con números, no con adjetivos.'),
], wrap=88, gap=0.12)
doc.add(p)
doc.close()
print('SINTESIS PAT ok', doc.folio, 'pp')
