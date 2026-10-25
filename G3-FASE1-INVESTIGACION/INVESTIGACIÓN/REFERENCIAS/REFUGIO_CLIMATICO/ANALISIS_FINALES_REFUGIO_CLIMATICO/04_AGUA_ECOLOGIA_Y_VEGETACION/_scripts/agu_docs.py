# -*- coding: utf-8 -*-
"""FASE FINAL - PDFs AGU-01..03 + AGUA_SINTESIS_INTEGRADA sobre v006."""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
sys.path.insert(0, os.path.join(BASE, '01_CLIMA_Y_CONFORT', '_scripts'))
import refugio_editorial as E  # noqa: E402
from cli_common import cabecera_analisis  # noqa: E402

OUT = os.path.join(BASE, '04_AGUA_ECOLOGIA_Y_VEGETACION')
with open(os.path.join(OUT, 'B_DATOS', 'agu_stats.json'), encoding='utf-8') as f:
    R = json.load(f)
FUENTE = 'FUENTE: _reclima9/agua.json + BOTANICAL_MASTERPLAN_v001.csv + agu_engine.py · v006 build 12'


def cab(doc, cid, titulo, pregunta, metodo, datos, nivel, lim):
    return cabecera_analisis(doc, cid, titulo, pregunta, metodo, datos, nivel, lim)


# ================================================================ AGU-01 · BALANCE
doc = E.Doc(os.path.join(OUT, 'AGU-01_BALANCE_HIDRICO.pdf'), 'AGU-01 · BALANCE HÍDRICO', '04 · AGUA')
E.portada(doc, 'El presupuesto\nde agua',
          'Cuánta agua consume el refugio el peor día del verano, de dónde sale, cuánta '
          'se recircula y cuántos días aguanta un corte de red.',
          'AGU-01 · AGUA, ECOLOGÍA Y VEGETACIÓN',
          [('DÍA PUNTA', doc.metric('AGU01-M1', 30.1, 'm³/día', 'B',
            'laminas medidas + riego ETx1.3 + niebla 6h', 'agu_stats.json')),
           ('DÍA MEDIO', '%.1f m³' % R['balance_dia_medio_m3']['total']),
           ('DEPÓSITOS', '99,8 m³'), ('AUTONOMÍA', '3,3 días')], num='AGU-01')
p, y = cab(doc, 'AGU-01', 'Treinta metros cúbicos el peor día',
           '¿Cuál es la demanda real de agua del sistema completo y su autonomía ante fallo?',
           'Evaporación de cada lámina por Penman con su exposición solar real (MEDIDA en '
           'el modelo, integrada a día); riego = evapotranspiración vegetal ×1,30 de '
           'ineficiencia de goteo (B); nebulización 6 h de operación en día seco (C). '
           'Almacenamiento: depósitos-gota medidos en la escena (99,8 m³).',
           'agua.json (por elemento), vegetacion.json, agu_engine.py.', 'B',
           'El perfil horario del riego se toma como 8 h-punta equivalentes; la niebla '
           'solo opera en día seco (su consumo anual es una fracción del nominal).')
bal = R['balance_dia_punta_m3']
rows = [['Evaporación de láminas y splash', '%.1f m³' % bal['evaporacion_laminas'], 'A/B',
         'reposición de lo que el sol evapora; el splash es además juego'],
        ['Riego de la capa vegetal', '%.1f m³' % bal['riego_vegetal'], 'B',
         'goteo por hidrozonas; ET medida ×1,30'],
        ['Nebulización (día seco)', '%.2f m³' % bal['nebulizacion'], 'C',
         '6 h de operación; 0 en día húmedo'],
        ['TOTAL DÍA PUNTA', '%.1f m³' % bal['total'], '—',
         'equivale a ~12 viviendas medias de Madrid']]
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['TÉRMINO', 'DEMANDA', 'NIVEL', 'LECTURA'],
            rows, col_w=[2.3, 1.1, 0.6, 3.0], size=7.4)
y -= 0.08
x = E.MX
p.bignum(x, y, '99,8', 'm³', 'almacenamiento en los depósitos-gota'); x += 2.1
p.bignum(x, y, '3,3', 'días', 'autonomía total ante corte de red (día punta)'); x += 2.1
p.bignum(x, y, '18,7', 'm³', 'demanda del día medio (E1)')
doc.metric('AGU01-M2', 3.3, 'días', 'B', 'V_dep/total punta', 'agu_stats.json')
y -= 1.15
y = p.panel(E.MX, y, E.A4W - 2 * E.MX, 1.0, 'RECIRCULACIÓN')
p.text(E.MX + 0.16, y, 'La única pérdida real es la evaporación: splash, estanques y '
       'balsas recirculan por las 4 conducciones principales enterradas con registro '
       'cada 9 m. No hay vertido de servicio: el sistema repone, no consume en flujo.',
       size=8.2, wrap=94)
doc.add(p)
doc.close()
print('AGU-01 ok', doc.folio, 'pp')

# ================================================================ AGU-02 · ECOLOGIA
doc = E.Doc(os.path.join(OUT, 'AGU-02_ECOLOGIA_Y_VEGETACION.pdf'),
            'AGU-02 · ECOLOGÍA', '04 · AGUA')
E.portada(doc, 'Un ecosistema\nen cuatro estratos',
          '17 especies reales en estratos arbóreo, arbustivo, herbáceo y acuático; '
          'hidrozonas por necesidad, estrategia estacional y una apuesta tropical que '
          'se declara como lo que es: condicionada al microclima del dosel.',
          'AGU-02 · AGUA, ECOLOGÍA Y VEGETACIÓN',
          [('ESPECIES', '17'), ('ESTRATOS', '4'),
           ('PERENNES/CADUCAS', '%d/%d' % (R['estacionalidad'].get('perenne', 0),
                                           R['estacionalidad'].get('caduca', 0))),
           ('HIDROZONAS', str(len(R['hidrozonas'])))], num='AGU-02')
p, y = cab(doc, 'AGU-02', 'Especies de verdad, riesgos de verdad',
           '¿Qué comunidad vegetal sostiene el refugio, con qué agua y qué sobrevive a qué?',
           'Masterplan botánico de 17 especies reales (nombre, hábito, LAI, necesidad '
           'hídrica, tolerancias, estacionalidad); hidrozonas de riego por clase de '
           'necesidad; estratificación por altura adulta.',
           'BOTANICAL_MASTERPLAN_v001.csv + _veg_clima.json.', 'A',
           'La supervivencia de las tropicales de sotobosque bajo dosel es una hipótesis '
           'agronómica (C) que el piloto debe validar antes del despliegue completo.')
b = R['biodiversidad']
x = E.MX
p.bignum(x, y, str(b['especies']), '', 'especies reales (ninguna inventada)'); x += 1.9
p.bignum(x, y, '%d·%d·%d' % (b['estratos']['arboreo'], b['estratos']['arbustivo'],
                             b['estratos']['herbaceo']), '',
         'árboreo · arbustivo · herbáceo'); x += 2.3
p.bignum(x, y, str(b['acuaticas']), '', 'especies acuáticas en balsas')
y -= 1.15
rows = []
for k, v in R['hidrozonas'].items():
    rows.append([k.upper(), '%.1f L/m²·día' % v['dosis_L_m2_dia'],
                 ', '.join(s.split()[0] for s in v['especies'][:6]) +
                 ('…' if len(v['especies']) > 6 else '')])
y = p.tabla(E.MX, y, E.A4W - 2 * E.MX, ['HIDROZONA', 'DOSIS', 'ESPECIES (GÉNERO)'],
            rows, col_w=[1.4, 1.3, 4.3], size=7.3)
y -= 0.08
y = p.panel(E.MX, y, E.A4W - 2 * E.MX, 1.3, 'LA APUESTA TROPICAL, DECLARADA (§43)')
p.text(E.MX + 0.16, y, b['nota_honesta'] + ' El plan de contingencia es la sustitución '
       'por sciófilas de clima templado (Fatsia, Aspidistra, helechos rústicos) sin '
       'cambiar jardineras ni riego: la infraestructura es agnóstica a la especie.',
       size=8.2, wrap=94)
doc.add(p)
doc.close()
print('AGU-02 ok', doc.folio, 'pp')

# ================================================================ AGU-03 · AGUA x CLIMA
doc = E.Doc(os.path.join(OUT, 'AGU-03_AGUA_X_CLIMA.pdf'), 'AGU-03 · AGUA × CLIMA', '04 · AGUA')
E.portada(doc, 'Litros por kelvin',
          'El cruce que ordena las decisiones: cuánta agua consume cada mecanismo '
          'climático y cuánto beneficio devuelve por litro.',
          'AGU-03 · AGUA, ECOLOGÍA Y VEGETACIÓN',
          [('AGUA/REFUGIO', doc.metric('AGU03-M1', 6.9, 'L/día·m²', 'B',
            'total punta / m2 refugio con niebla', 'agu_stats.json')),
           ('MÁS RENTABLE', 'NIEBLA: 2,5 L/m²·día'),
           ('GRATIS', 'SOMBRA: 0 L'), ('NIVEL', 'B')], num='AGU-03')
p, y = cab(doc, 'AGU-03', 'No todos los litros enfrían igual',
           '¿Qué mecanismo climático consume más agua y cuál devuelve más por litro?',
           'Ratio demanda diaria / beneficio de cada mecanismo, con los beneficios '
           'medidos en CLI-03/04/07 y las demandas de AGU-01.',
           'agu_stats.json/eficiencia (cruce de motores).', 'B',
           'Los ratios usan el m² de refugio como denominador común; el ratio por '
           'persona-hora se calcula en 10_SINTESIS con el modelo de uso.')
rows = [[m['mecanismo'], ('%d L' % m['L_dia']) if m['L_dia'] else '0 L',
         m['beneficio'],
         ('%.1f' % m['L_por_m2_beneficio']) if m['L_por_m2_beneficio'] else '—',
         m['lectura']] for m in R['eficiencia']['mecanismos']]
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['MECANISMO', 'L/DÍA', 'BENEFICIO', 'L/M²', 'LECTURA'],
            rows, col_w=[1.35, 0.75, 1.9, 0.6, 2.4], size=6.9)
y -= 0.1
y = p.dashlist(E.MX, y, [
    ('La jerarquía es clara:', 'sombra (gratis) > niebla (2,5 L/m²·día en su ventana) > '
     'láminas (6,3 L/m²·día, con valor recreativo añadido) > riego (retorno ecológico, '
     'no térmico).'),
    ('Consecuencia operativa:', 'en sequía severa el protocolo corta primero la niebla '
     'ornamental y protege el riego de arbolado — el orden inverso al beneficio térmico '
     'instantáneo, porque un árbol muerto tarda 15 años en volver.'),
    ('El agua es el OPEX dominante del clima', 'pero 30 m³/día punta ~ 66 €/día a tarifa '
     'no doméstica de Madrid: el coste está en el mantenimiento, no en el consumo (07).'),
], wrap=86, gap=0.1)
doc.add(p)
doc.close()
print('AGU-03 ok', doc.folio, 'pp')

# ================================================================ SINTESIS
doc = E.Doc(os.path.join(OUT, 'AGUA_SINTESIS_INTEGRADA.pdf'), 'AGUA · SÍNTESIS', '04 · AGUA')
E.portada(doc, '¿Es sostenible\nel agua del refugio?',
          'Síntesis del sistema hídrico-ecológico: balance, autonomía, hidrozonas, '
          'biodiversidad y el cruce agua × clima × vegetación.',
          '04 · AGUA · SÍNTESIS',
          [('VEREDICTO CORTO', 'SÍ, CON PROTOCOLO DE SEQUÍA'),
           ('DÍA PUNTA', '30,1 m³'), ('AUTONOMÍA', '3,3 días'),
           ('AGUA/REFUGIO', '6,9 L/día·m²')], num='S-04')
p = doc.page('SÍNTESIS')
y = E.A4H - 1.0
y = p.kicker(y, 'S-04.1 · LO QUE LOS CRUCES ENSEÑAN')
y = p.title(y, 'Un sistema que puede tener sed sin morir', size=17)
y = p.dashlist(E.MX, y - 0.02, [
    ('Agua × clima:', 'el 100 % del confort estructural (sombra, −10,9 K MRT) funciona '
     'con los depósitos vacíos. El agua compra el margen fino: −1,1 K de aire, +501 m² '
     'de refugio, superficies frías. El refugio degrada, no colapsa.'),
    ('Agua × vegetación:', 'el riego (4,4 m³/día) es el 15 % de la demanda pero el único '
     'término IRREVERSIBLE: el resto se repone al abrir la llave; un arbolado perdido, '
     'no. Prioridad de sequía: árboles > arbustos > herbáceas > láminas > niebla.'),
    ('Vegetación × clima (honestidad):', 'la capa vegetal aporta el 21 % del calor '
     'latente y ±1 punto de sombra: su justificación es ecológica y social tanto como '
     'térmica, y así se presenta al Ayuntamiento — sin inflar su papel climático.'),
    ('Dimensionado verificado:', 'los 99,8 m³ de depósito cubren 3,3 días punta o ~5 '
     'días medios: suficiente para cualquier corte urbano plausible; insuficiente para '
     'una sequía decretada — para eso está el protocolo, no el tanque.'),
], wrap=88, gap=0.12)
y -= 0.08
y = p.panel(E.MX, y, E.A4W - 2 * E.MX, 1.05, 'PARA EL DOSSIER MUNICIPAL')
p.text(E.MX + 0.16, y, 'Demanda punta 30,1 m³/día (~12 viviendas), autonomía 3,3 días, '
       'pérdida real limitada a la evaporación, protocolo de sequía con jerarquía '
       'explícita y una capa vegetal cuya infraestructura admite sustitución de especies '
       'sin obra. El agua no es el talón de Aquiles del proyecto: es su termostato.',
       size=8.4, wrap=94)
doc.add(p)
doc.close()
print('SINTESIS AGU ok', doc.folio, 'pp')
