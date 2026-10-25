# -*- coding: utf-8 -*-
"""FASE FINAL - ECO-01..02 + ECONOMIA_SINTESIS_INTEGRADA sobre v006."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
sys.path.insert(0, os.path.join(BASE, '01_CLIMA_Y_CONFORT', '_scripts'))
import refugio_editorial as E  # noqa: E402
from cli_common import cabecera_analisis  # noqa: E402

OUT = os.path.join(BASE, '07_ECONOMIA_OPERACION_Y_ESCENARIOS')
with open(os.path.join(OUT, 'B_DATOS', 'eco_stats.json'), encoding='utf-8') as f:
    R = json.load(f)
FUENTE = 'FUENTE: eco_engine.py · fuentes externas en fuentes_externas.csv (URL/institución/fecha)'

# ================================================================ ECO-01 · CAPEX/OPEX
doc = E.Doc(os.path.join(OUT, 'ECO-01_CAPEX_OPEX_CICLO_DE_VIDA.pdf'),
            'ECO-01 · CAPEX / OPEX', '07 · ECONOMÍA')
cap = R['capex_MEUR']; opx = R['opex_kEUR_ano']
E.portada(doc, 'Lo que cuesta\ny lo que come',
          'Primer modelo económico del refugio: inversión por analogía declarada, '
          'operación por componentes y fondo de reposición por ciclo de vida. Nivel C '
          'en CAPEX y B/C en OPEX — medido, no optimizado.',
          'ECO-01 · ECONOMÍA Y OPERACIÓN',
          [('CAPEX', '%.1f–%.1f M€' % (cap['total_con_25pct']['low'], cap['total_con_25pct']['high'])),
           ('OPEX', '%d–%d k€/año' % (opx['total']['low'], opx['total']['high'])),
           ('REPOSICIÓN', '%.2f M€/año' % opx['fondo_reposicion_MEUR_ano']),
           ('NIVEL', 'C / B')], num='ECO-01')
p, y = cabecera_analisis(
    doc, 'ECO-01', 'Doce millones, bien contados',
    '¿Qué orden de inversión y de operación exige el refugio — sin proyecto de '
    'ejecución todavía, pero con las cantidades REALES del modelo v006?',
    'CAPEX por partida con analogías declaradas (membrana €/m² sobre los 4.186 m² de '
    'sombra reales; pasarela €/m² sobre los 733 m medidos; aparatos por unidad) + 25 % '
    'de honorarios e imprevistos. OPEX por componente sobre la matriz TEC-02. Fondo de '
    'reposición = Σ(valor/vida útil).',
    'tec_stats.json (cantidades), agua/energía de AGU-01, benchmark Sevilla (F-05).', 'C',
    'NO es un presupuesto: es un orden de magnitud para decidir si seguir. El proyecto '
    'de ejecución lo sustituirá. El IVA no está incluido.')
rows = [[c['partida'], '%.1f' % c['low'], '%.1f' % c['base'], '%.1f' % c['high']]
        for c in cap['partidas']]
rows.append(['SUBTOTAL', '%.1f' % cap['subtotal']['low'], '%.1f' % cap['subtotal']['base'],
             '%.1f' % cap['subtotal']['high']])
rows.append(['TOTAL (+25 % honorarios e imprevistos)', '%.1f' % cap['total_con_25pct']['low'],
             '%.1f' % cap['total_con_25pct']['base'], '%.1f' % cap['total_con_25pct']['high']])
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['PARTIDA CAPEX (M€)', 'LOW', 'BASE', 'HIGH'],
            rows, col_w=[4.3, 0.9, 0.9, 0.9], size=7.0)
doc.metric('ECO01-M1', cap['total_con_25pct']['base'], 'M€', 'C', 'CAPEX BASE por analogia',
           'eco_stats.json')
y -= 0.06
p.text(E.MX, y, 'Contexto público citable: Sevilla instala toldos ligeros en 30 calles por '
       '1,70 M€ (4 años) y sombra el puente de San Telmo por 1,1 M€ (F-05). El Refugio es '
       'otra categoría: infraestructura permanente con agua, vegetación y nivel visitable.',
       size=7.6, wrap=100, color='#4a4a4a')
doc.add(p)

p = doc.page('ECO-01 · OPERACIÓN')
y = E.A4H - 1.0
y = p.kicker(y, 'ECO-01.2 · OPEX Y CICLO DE VIDA')
y = p.title(y, 'Doscientos setenta y seis mil al año, y un fondo', size=16)
rows = [[o['partida'], str(o['low']), str(o['base']), str(o['high']), o['metodo']]
        for o in opx['partidas']]
rows.append(['TOTAL OPEX (k€/año)', str(opx['total']['low']), str(opx['total']['base']),
             str(opx['total']['high']), '—'])
y = p.tabla(E.MX, y, E.A4W - 2 * E.MX,
            ['PARTIDA OPEX (K€/AÑO)', 'LOW', 'BASE', 'HIGH', 'MÉTODO'],
            rows, col_w=[2.2, 0.55, 0.6, 0.6, 3.0], size=6.6)
doc.metric('ECO01-M2', opx['total']['base'], 'k€/año', 'B', 'OPEX BASE por componentes', 'eco_stats.json')
y -= 0.08
y = p.dashlist(E.MX, y, [
    ('El agua NO es el coste:', '9 k€/año de consumo frente a 90 k€ de jardinería y '
     '110 k€ de limpieza+membrana. El OPEX del refugio es MANO DE OBRA, no recurso.'),
    ('El fondo de reposición (0,21 M€/año)', 'financia membranas (18 años), pods (10), '
     'nebulizadores (7) y renovación de ascensores (20): el ciclo de vida se paga desde '
     'el día uno o se paga triple en el año quince.'),
    ('Comparado con el CAPEX,', 'operar el refugio 25 años cuesta ~12 M€ (OPEX+fondo): '
     'tanto como construirlo. El dossier lo dice ahora, no en la primera avería.'),
], wrap=86, gap=0.1)
doc.add(p)
doc.close()
print('ECO-01 ok', doc.folio, 'pp')

# ================================================================ ECO-02 · COMERCIO
doc = E.Doc(os.path.join(OUT, 'ECO-02_ESCENARIOS_DE_COMERCIO.pdf'),
            'ECO-02 · COMERCIO', '07 · ECONOMÍA')
com = R['comercio']['escenarios']
E.portada(doc, 'El comercio,\nsin cuentos',
          'No decimos «el comercio mejorará»: modelamos tres escenarios con cada '
          'hipótesis a la vista y anclados en los contadores reales de Preciados y en '
          'los 73 millones de viajeros de la estación de Sol.',
          'ECO-02 · ECONOMÍA Y OPERACIÓN',
          [('LOW', '%d €/día' % com['LOW']['gasto_incremental_eur_dia']),
           ('BASE', '%d €/día' % com['BASE']['gasto_incremental_eur_dia']),
           ('HIGH', '%d €/día' % com['HIGH']['gasto_incremental_eur_dia']),
           ('NIVEL', 'C — ESCENARIO')], num='ECO-02')
p, y = cabecera_analisis(
    doc, 'ECO-02', 'Flujo × tiempo × exposición × conversión × ticket',
    '¿Qué gasto incremental plausible genera una plaza donde por fin apetece quedarse?',
    'Modelo de 5 factores sobre flujo base 60.000/día: flujo adicional atraído, tiempo '
    'adicional de estancia (SOC-02), exposición comercial de ese tiempo, conversión '
    'hipotética y ticket medio hipotético. Tres escenarios completos, nunca un número '
    'suelto.',
    'F-01 (Metro Sol 73 M/año), F-03 (Preciados 13.800/día), F-04 (aforos abiertos '
    'Ayto), SOC-02.', 'C',
    'Todo el modelo es HIPÓTESIS de escenario: sirve para dimensionar el interés '
    'económico de validar con datos reales (aforos F-04 + panel de comercio), no para '
    'prometer facturación.')
rows = [[k, '+%.0f %%' % v['flujo_adicional_pct'], '+%d min' % v['tiempo_adicional_min'],
         '%.0f %%' % (100 * v['exposicion']), '%.1f %%' % v['conversion_pct'],
         '%.0f €' % v['ticket_eur'],
         '%d €/día' % v['gasto_incremental_eur_dia'],
         '%.0f k€' % v['gasto_temporada_93d_keur']] for k, v in com.items()]
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['ESC', 'FLUJO', 'TIEMPO', 'EXPO', 'CONV', 'TICKET', '€/DÍA', 'TEMPORADA'],
            rows, col_w=[0.7, 0.85, 0.85, 0.7, 0.75, 0.8, 1.15, 1.1], size=7.0)
doc.metric('ECO02-M1', com['BASE']['gasto_incremental_eur_dia'], '€/día', 'C',
           'modelo 5 factores BASE', 'eco_stats.json')
y -= 0.1
y = p.dashlist(E.MX, y, [
    ('Ni en el escenario HIGH', 'el gasto incremental (6.900 €/día ~ 640 k€/temporada) '
     '«paga» el proyecto: el refugio se justifica por personas-hora protegidas, no por '
     'caja comercial. Decirlo evita el argumento débil.'),
    ('Lo que sí es sólido:', 'la ecuación confort › permanencia › exposición existe en la '
     'literatura de espacio público; su MAGNITUD aquí es incógnita medible con los '
     'aforos oficiales (F-04) antes/después del piloto.'),
], wrap=86, gap=0.1)
doc.add(p)
doc.close()
print('ECO-02 ok', doc.folio, 'pp')

# ================================================================ SINTESIS
doc = E.Doc(os.path.join(OUT, 'ECONOMIA_SINTESIS_INTEGRADA.pdf'),
            'ECONOMÍA · SÍNTESIS', '07 · ECONOMÍA')
E.portada(doc, '¿Cuánto vale\nuna hora de sombra?',
          'Síntesis económica: inversión, operación, comercio y el indicador que lo '
          'ordena todo — el coste por persona-hora protegida.',
          '07 · ECONOMÍA · SÍNTESIS',
          [('CAPEX BASE', '11,9 M€'), ('OPEX+FONDO', '~0,49 M€/año'),
           ('€/P·H (BASE, 25 AÑOS)', 'véase cálculo'), ('NIVEL', 'C')], num='S-07')
p = doc.page('SÍNTESIS')
y = E.A4H - 1.0
y = p.kicker(y, 'S-07.1 · EL INDICADOR QUE ORDENA')
y = p.title(y, 'Coste por persona-hora protegida', size=17)
capex_base = R['capex_MEUR']['total_con_25pct']['base']
anual = R['opex_kEUR_ano']['total']['base'] / 1000.0 + R['opex_kEUR_ano']['fondo_reposicion_MEUR_ano']
coste_25a = capex_base + 25 * anual
ph_temporada = dict(LOW=33000, BASE=200000, HIGH=890000)
y = p.tabla(E.MX, y, E.A4W - 2 * E.MX,
            ['ESCENARIO USO', 'P·H/TEMPORADA', 'P·H EN 25 AÑOS', '€ / PERSONA-HORA'],
            [[k, f'{v:,}'.replace(',', '.'), f'{v*25:,}'.replace(',', '.'),
              '%.1f €' % (coste_25a * 1e6 / (v * 25))] for k, v in ph_temporada.items()],
            col_w=[1.6, 1.8, 1.8, 1.8], size=7.6)
y -= 0.08
y = p.dashlist(E.MX, y, [
    ('En el escenario BASE,', 'cada persona-hora de calor severo evitado cuesta ~4,9 € '
     'contando construcción y 25 años de operación. En HIGH baja a ~1,1 €; en LOW sube '
     'a ~29 €. La horquilla ES el mensaje: el retorno depende del USO, y el uso se '
     'valida con el piloto antes de comprometer el CAPEX completo.'),
    ('La comparación honesta:', 'una marquesina de autobús con sombra cuesta ~8-15 k€ y '
     'protege a decenas; el refugio protege a miles con servicios que una marquesina no '
     'da (agua, vegetación, mirador, atrio). No hay coste por p·h publicado en España '
     'para compararse: este dossier propone el indicador y su método.'),
    ('Regla de decisión sugerida al Ayuntamiento:', 'si el piloto (fase C) mide ≥60 % '
     'del uso BASE, el despliegue completo opera por debajo de 8 €/p·h — umbral '
     'defendible frente al coste sanitario del calor.'),
], wrap=88, gap=0.12)
doc.metric('S07-M1', round(coste_25a * 1e6 / (ph_temporada['BASE'] * 25), 1), '€/p·h', 'C',
           '(CAPEX+25a OPEX)/(p·h BASE 25a)', 'eco_stats.json + soc_stats.json')
doc.add(p)
doc.close()
print('SINTESIS ECO ok', doc.folio, 'pp')
