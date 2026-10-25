# -*- coding: utf-8 -*-
"""FASE FINAL - PDFs TEC-01..02 + CONSTRUCCION_SINTESIS_INTEGRADA sobre v006."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
sys.path.insert(0, os.path.join(BASE, '01_CLIMA_Y_CONFORT', '_scripts'))
import refugio_editorial as E  # noqa: E402
from cli_common import cabecera_analisis  # noqa: E402

OUT = os.path.join(BASE, '05_CONSTRUCCION_ESTRUCTURA_Y_MANTENIMIENTO')
with open(os.path.join(OUT, 'B_DATOS', 'tec_stats.json'), encoding='utf-8') as f:
    R = json.load(f)
FUENTE = 'FUENTE: escena v006 build 12 (15.197 mallas) + _reaudit9/a9_maint.json + tec_engine.py'

# ================================================================ TEC-01 · INVENTARIO
doc = E.Doc(os.path.join(OUT, 'TEC-01_INVENTARIO_Y_FAMILIAS.pdf'),
            'TEC-01 · INVENTARIO', '05 · CONSTRUCCIÓN')
E.portada(doc, 'De qué está hecho\nel refugio',
          'Inventario completo de la escena v006 por familia constructiva: cantidades '
          'reales del modelo, no estimaciones. La base de toda medición, presupuesto y '
          'plan de mantenimiento.',
          'TEC-01 · CONSTRUCCIÓN Y ESTRUCTURA',
          [('MALLAS', doc.metric('TEC01-M1', 15197, 'ud', 'A', 'len(mesh) escena', 'tec_stats.json')),
           ('HOJAS DE DOSEL', '93'), ('NEBULIZADORES', '42'),
           ('PUNTOS A9', '160')], num='TEC-01')
p, y = cabecera_analisis(
    doc, 'TEC-01', 'Quince mil piezas con nombre',
    '¿Qué cantidades reales de cada sistema constructivo contiene el modelo aprobado?',
    'Reconstrucción interceptada de la escena v006 (el mismo load_scene de la '
    'auditoría) y conteo por familia: mallas totales y anclas de instancia únicas por '
    'bloque. Todo objeto tiene nombre y capa: no hay geometría anónima.',
    'build_all_03b9 vía audit_core.load_scene (build 12).', 'A',
    'El conteo de instancias solo aplica a bloques colocados con place(); las familias '
    'de detalle emitidas por add_mesh cuentan por malla.')
top = [(k, v) for k, v in R['inventario'].items()][:14]
rows = [[k, str(v['mallas']), str(v['instancias'] or '—')] for k, v in top]
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['FAMILIA', 'MALLAS', 'INSTANCIAS'],
            rows, col_w=[3.6, 1.7, 1.7], size=7.2)
p.text(E.MX, y - 0.02, FUENTE, size=5.4, color=E.GRAYTX)
doc.add(p)
doc.close()
print('TEC-01 ok', doc.folio, 'pp')

# ================================================================ TEC-02 · MATRIZ
doc = E.Doc(os.path.join(OUT, 'TEC-02_MATRIZ_MANTENIMIENTO.pdf'),
            'TEC-02 · MANTENIMIENTO', '05 · CONSTRUCCIÓN')
E.portada(doc, 'Quién cuida qué,\ncada cuánto',
          'La matriz componente  ›  función  ›  acceso  ›  frecuencia  ›  riesgo, con las '
          'cantidades del modelo y el acceso de mantenimiento auditado punto a punto.',
          'TEC-02 · CONSTRUCCIÓN Y ESTRUCTURA',
          [('COMPONENTES', str(len(R['matriz']))), ('PUNTOS AUDITADOS', '160'),
           ('SIN ACCESO', '1 de 160'), ('RIESGO ALTO', 'ascensores (equidad)')], num='TEC-02')
p, y = cabecera_analisis(
    doc, 'TEC-02', 'La matriz de mantenimiento',
    '¿Puede mantenerse cada sistema, con qué medios, con qué frecuencia y qué pasa si no?',
    'Cantidades MEDIDAS en la escena; acceso por punto del módulo A9 de la auditoría '
    '(holgura, distancia a pisable, necesidad de plataforma); frecuencias y vidas útiles '
    'INFERIDAS por analogía con equipamiento urbano comparable.',
    'a9_maint.json (160 puntos) + matriz_mantenimiento.csv.', 'B',
    'Las frecuencias son plan inicial, no contrato: el roadmap municipal las convierte '
    'en SLA tras el piloto.')
rows = [[m_['componente'] + ' (×%s)' % m_['n'], m_['acceso'], m_['frecuencia'],
         m_['vida'], m_['riesgo']] for m_ in R['matriz']]
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['COMPONENTE', 'ACCESO', 'FRECUENCIA', 'VIDA', 'RIESGO'],
            rows, col_w=[1.75, 1.75, 1.45, 0.85, 1.2], size=6.4)
doc.add(p)

p = doc.page('TEC-02 · HALLAZGO A9')
y = E.A4H - 1.0
y = p.kicker(y, 'TEC-02.2 · EL PUNTO CIEGO (§43)')
y = p.title(y, '159 de 160 puntos con acceso. ¿Y el 160?', size=16)
y = p.dashlist(E.MX, y - 0.02, [
    ('BOMBA-1 (−70,0 · 22,0) no tiene acceso auditado:', 'holgura 0,0 m — quedó '
     'encajonada entre la jardinera perimetral y el murete del vivero en el detailing '
     'v006. Las otras dos bombas (BOMBA-2, BOMBA-3) tienen 4 m de distancia practicable '
     'y gálibo de sobra.'),
    ('Consecuencia:', 'es el único punto del sistema hídrico cuyo mantenimiento exigiría '
     'desmontar elementos. Riesgo operativo real si esa bomba sirve la recirculación '
     'del cuadrante oeste.'),
    ('Modificación potencial documentada (§54, NO implementada):', 'desplazar BOMBA-1 '
     '1,5 m al norte o practicar registro en el murete. Se deja al proyecto de '
     'ejecución con prioridad ALTA.'),
], wrap=86, gap=0.12)
doc.metric('TEC02-M1', '159/160', 'puntos', 'A', 'acceso A9 auditado', 'a9_maint.json')
y -= 0.08
y = p.panel(E.MX, y, E.A4W - 2 * E.MX, 1.0, 'PARA EL DOSSIER MUNICIPAL')
p.text(E.MX + 0.16, y, 'El proyecto se modeló hasta el tornillo con la pregunta «¿quién '
       'mantiene esto?» integrada en la auditoría (módulo A9): 160 puntos técnicos '
       'georreferenciados, 159 con acceso verificado, tapas de registro cada 9 m en la '
       'red enterrada y un único punto ciego, identificado y con corrección trivial.',
       size=8.4, wrap=94)
doc.add(p)
doc.close()
print('TEC-02 ok', doc.folio, 'pp')

# ================================================================ SINTESIS
doc = E.Doc(os.path.join(OUT, 'CONSTRUCCION_SINTESIS_INTEGRADA.pdf'),
            'CONSTRUCCIÓN · SÍNTESIS', '05 · CONSTRUCCIÓN')
E.portada(doc, '¿Se puede construir\ny mantener?',
          'Síntesis técnica: el kit de piezas, su acceso, sus vidas útiles y las '
          'dependencias entre sistemas — cruzado con clima, agua y coste.',
          '05 · CONSTRUCCIÓN · SÍNTESIS',
          [('VEREDICTO CORTO', 'SÍ — KIT REPETITIVO'),
           ('FAMILIAS HERO', '12 sistemas'), ('ACCESO', '159/160'),
           ('DEPENDENCIA CRÍTICA', 'ascensores + cámara microalgas')], num='S-05')
p = doc.page('SÍNTESIS')
y = E.A4H - 1.0
y = p.kicker(y, 'S-05.1 · LO QUE LOS CRUCES ENSEÑAN')
y = p.title(y, 'Un kit de partes que se deja cuidar', size=17)
y = p.dashlist(E.MX, y - 0.02, [
    ('Construcción × clima:', 'los dos únicos componentes cuyo fallo tiene efecto '
     'climático inmediato son la cámara de microalgas (+6,9 K local si se seca) y la '
     'nebulización (−501 m² de refugio). Ambos están en la banda de frecuencia más '
     'corta de la matriz: quincenal y trimestral. El mantenimiento ES política climática.'),
    ('Construcción × equidad:', 'el riesgo ALTO no es estructural sino social: 3 '
     'ascensores sostienen la accesibilidad del nivel +6. SLA <48 h o cuarto aparato.'),
    ('Repetición = mantenibilidad:', '93 hojas de dosel idénticas en 3 tamaños, 42 '
     'nebulizadores iguales, 6 escaleras de la misma familia: el almacén de repuestos '
     'es corto y el conocimiento de cuadrilla, transferible.'),
    ('La red enterrada como seguro:', 'tapas cada 9 m y purgas estacionales: la '
     'hidráulica se diseñó para repararse sin levantar la plaza — la lección de las '
     'obras eternas de Sol está incorporada.'),
], wrap=88, gap=0.12)
doc.add(p)
doc.close()
print('SINTESIS TEC ok', doc.folio, 'pp')
