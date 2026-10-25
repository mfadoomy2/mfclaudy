# -*- coding: utf-8 -*-
"""FASE FINAL - URB-01..02 + CONTEXTO_SINTESIS_INTEGRADA sobre v006."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
sys.path.insert(0, os.path.join(BASE, '01_CLIMA_Y_CONFORT', '_scripts'))
import refugio_editorial as E  # noqa: E402
from cli_common import cabecera_analisis  # noqa: E402

OUT = os.path.join(BASE, '03_CONTEXTO_URBANO_Y_TRANSPORTE')
os.makedirs(os.path.join(OUT, 'B_DATOS'), exist_ok=True)
F9 = os.path.normpath(os.path.join(BASE, '..', 'FASE_03B9_HYPERDETAIL_V006'))
with open(os.path.join(F9, '_reaudit9', '_data', 'a6_metro.json'), encoding='utf-8') as f:
    a6 = json.load(f)
with open(os.path.join(F9, '_reaudit9', '_data', 'a12_edificios.json'), encoding='utf-8') as f:
    a12 = json.load(f)
geo = E.load_geo()
FUENTE = 'FUENTE: _reaudit9/a6_metro.json + a12_edificios.json · v006 build 12'

# ================================================================ URB-01 · TRANSPORTE
doc = E.Doc(os.path.join(OUT, 'URB-01_METRO_Y_CERCANIAS.pdf'),
            'URB-01 · METRO Y CERCANÍAS', '03 · CONTEXTO')
rows_a6 = a6['rows']
en_amb = [r for r in rows_a6 if r.get('en_ambito')]
peor_libre = min((r['libre_min'] for r in en_amb), default=0)
E.portada(doc, 'La plaza que es\nuna estación',
          'Sol es la puerta de un intercambiador: cada acceso de Metro y Cercanías se '
          'audita con su banda de respeto, su holgura real y su gálibo — el proyecto '
          'convive con el transporte, no lo estorba.',
          'URB-01 · CONTEXTO URBANO Y TRANSPORTE',
          [('ACCESOS AUDITADOS', str(len(rows_a6))),
           ('EN ÁMBITO', str(len(en_amb))),
           ('PEOR HOLGURA', doc.metric('URB01-M1', round(peor_libre, 2), 'm', 'A',
            'min libre_min accesos en ambito', 'a6_metro.json')),
           ('BANDA DE RESPETO', '%.1f m' % a6['band'])], num='URB-01')
p, y = cabecera_analisis(
    doc, 'URB-01', 'Cada boca con su banda de respeto',
    '¿Queda cada acceso de Metro/Cercanías con la holgura funcional que exige un '
    'intercambiador con cientos de miles de viajeros?',
    'Módulo A6 de la auditoría: banda de respeto de %.1f m alrededor de cada acceso, '
    'conteo de obstáculos del proyecto en banda (a nivel de suelo y aéreo hasta '
    '%.1f m), holgura mínima y media, gálibo sobre la vertical del acceso.'
    % (a6['band'], a6['zobst']),
    'a6_metro.json (accesos OSM) + escena v006.', 'A',
    'Las posiciones de los accesos proceden de OSM (DATO cuasi-oficial); las bandas de '
    'respeto son CRITERIO DE PROYECTO en ausencia de informe vinculante de Metro de '
    'Madrid — se declara y queda como validación municipal pendiente.')
rows = [[r['name'], 'sí' if r.get('en_ambito') else 'no',
         '%.1f m' % r['libre_min'], '%.1f m' % r['libre_medio'],
         str(r.get('n_banda_suelo', 0)), str(r.get('n_banda_aereo', 0))]
        for r in rows_a6]
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['ACCESO', 'ÁMBITO', 'LIBRE MÍN', 'LIBRE MEDIA', 'OBST. SUELO', 'OBST. AÉREO'],
            rows, col_w=[2.3, 0.7, 1.05, 1.15, 1.0, 0.9], size=6.9)
y -= 0.08
y = p.dashlist(E.MX, y, [
    ('Cero obstáculos en banda', 'en todos los accesos del ámbito: n_banda_suelo = '
     'n_banda_aereo = 0 en build 12 (las versiones v002-v004 tuvieron conflictos: la '
     'genealogía está en el registro de decisiones).'),
    ('El atrio como pieza de proyecto:', 'la boca principal recibe marquesina volada '
     'hacia la aproximación, 6 bolardos luminosos y canal de drenaje — recortados '
     'contra el polígono REAL de la estación (criterio del auditor, no del generador).'),
], wrap=86, gap=0.1)
doc.add(p)
doc.close()
print('URB-01 ok', doc.folio, 'pp')

# ================================================================ URB-02 · BORDES
doc = E.Doc(os.path.join(OUT, 'URB-02_BORDES_Y_FACHADAS.pdf'),
            'URB-02 · BORDES', '03 · CONTEXTO')
E.portada(doc, 'Los bordes:\ndonde el proyecto\ntoca la ciudad',
          'Fachadas, kioscos, servidumbres y continuidad del espacio público — con la '
          'distinción explícita entre dato oficial y criterio provisional del proyecto.',
          'URB-02 · CONTEXTO URBANO Y TRANSPORTE',
          [('PENETRACIONES', doc.metric('URB02-M1', 0, 'ud', 'A',
            'A12 sobre 35 edificios reales', 'a12_edificios.json')),
           ('EDIFICIOS AUDITADOS', str(a12['n_edificios'])),
           ('AIRE A ECI', '~2,0 m'), ('EJES HISTÓRICOS', '6 conservados')], num='URB-02')
p, y = cabecera_analisis(
    doc, 'URB-02', 'Convivir con 35 edificios y 6 ejes',
    '¿Dónde y cómo toca el proyecto los bordes construidos y los recorridos históricos '
    'de Sol?',
    'Módulo A12 (independiente del generador): penetración de cualquier sólido del '
    'proyecto en 35 volumetrías construidas reales con alturas por tipo; regla CR-2 de '
    'fachada (cerrar a ~2 cm o abrir ≥1,5 m: nunca ranuras-trampa); 6 ejes declarados '
    'auditados estación a estación.',
    'a12_edificios.json + a1_paths.json + geometria_maestra_v006/contexto.', 'A',
    'Las servidumbres administrativas (licencias de veladores, accesos de carga, '
    'hidrantes) NO están en el modelo: inventario municipal pendiente para ejecución.')
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['CAPA', 'ESTADO EN V006', 'FUENTE', 'CARÁCTER'],
            [['Huellas de edificio (35)', '0 penetraciones (A12)', 'OSM', 'DATO cuasi-oficial'],
             ['Alturas de contexto', 'tipo: manzana / estación 6,5 / kiosco 4,1', 'OSM+fotos', 'CRITERIO calibrado'],
             ['Accesos Metro/Cercanías', '0 obstáculos en banda', 'OSM', 'DATO cuasi-oficial'],
             ['Bandas de respeto', '5,5 m por acceso', 'proyecto', 'CRITERIO PROVISIONAL'],
             ['Ejes históricos (6)', 'transitables, 0 RED', 'proyecto sobre callejero', 'CRITERIO'],
             ['Kioscos y estancos', 'conservados con margen propio', 'OSM', 'DATO cuasi-oficial'],
             ['Servidumbres administrativas', 'NO MODELADAS', '—', 'PENDIENTE MUNICIPAL']],
            col_w=[1.9, 2.0, 1.2, 1.9], size=7.0)
y -= 0.1
y = p.panel(E.MX, y, E.A4W - 2 * E.MX, 1.2, 'CONTINUIDAD DEL ESPACIO PÚBLICO')
p.text(E.MX + 0.16, y, 'El proyecto no cierra, vallar ni privatiza suelo alguno: el 100 % '
       'del ámbito sigue siendo espacio público 24 h. Los seis corredores históricos '
       '(Mayor-Alcalá, Preciados-Carretas, Carmen-Correos, Montera-Espoz y Mina, '
       'Arenal-Alcalá y el arco norte) conservan trazado y anchura auditada. La '
       'implantación es reversible por diseño: cimentación puntual de mástiles y '
       'pavimento existente conservado bajo las jardineras.', size=8.2, wrap=94)
doc.add(p)
doc.close()
print('URB-02 ok', doc.folio, 'pp')

# ================================================================ SINTESIS
doc = E.Doc(os.path.join(OUT, 'CONTEXTO_SINTESIS_INTEGRADA.pdf'),
            'CONTEXTO · SÍNTESIS', '03 · CONTEXTO')
E.portada(doc, '¿Cabe en Sol?',
          'Síntesis de implantación: transporte, bordes, servidumbres y lo que queda '
          'pendiente de la administración.',
          '03 · CONTEXTO · SÍNTESIS',
          [('VEREDICTO CORTO', 'CABE — Y ES REVERSIBLE'),
           ('CONFLICTOS FÍSICOS', '0'), ('PENDIENTE', 'servidumbres + informe Metro'),
           ('NIVEL', 'A geometría / C administrativo')], num='S-03')
p = doc.page('SÍNTESIS')
y = E.A4H - 1.0
y = p.kicker(y, 'S-03.1 · LO QUE LOS CRUCES ENSEÑAN')
y = p.title(y, 'La implantación está resuelta; la tramitación, no', size=16)
y = p.dashlist(E.MX, y - 0.02, [
    ('Físicamente, el encaje es limpio:', '0 penetraciones sobre 35 edificios, 0 '
     'obstáculos en bandas de Metro, ~2 m de aire a la fachada comercial más sensible, '
     '6 ejes históricos auditados estación a estación. Cuatro versiones costó (v002 › '
     'v006): la genealogía de ese aprendizaje está en 11_IA_Y_PROCESO.'),
    ('Administrativamente, quedan tres puertas:', 'informe vinculante de Metro de '
     'Madrid sobre las bandas de respeto; inventario de servidumbres de superficie '
     '(veladores, carga, hidrantes, eventos); y el régimen de protección del conjunto '
     'histórico. Ninguna es geométrica: todas son de tramitación.'),
    ('Transporte × uso (el cruce estratégico):', 'la mayor estación de cercanías del '
     'centro vierte su público EXACTAMENTE donde el refugio ofrece la primera sombra: '
     'el atrio es la puerta climática de Madrid centro. El dato de afluencia oficial '
     '(07_ECONOMIA) convierte esta intuición en indicador.'),
], wrap=88, gap=0.12)
doc.add(p)
doc.close()
print('SINTESIS URB ok', doc.folio, 'pp')
