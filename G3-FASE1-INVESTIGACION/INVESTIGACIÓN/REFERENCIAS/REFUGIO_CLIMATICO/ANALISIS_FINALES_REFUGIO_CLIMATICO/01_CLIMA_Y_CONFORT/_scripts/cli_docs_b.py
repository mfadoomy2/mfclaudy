# -*- coding: utf-8 -*-
"""FASE FINAL - PDFs analiticos CLI-06..CLI-10 (vegetacion, agua, viento, programa, fallos)."""
import csv
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
import refugio_editorial as E  # noqa: E402
from cli_common import cabecera_analisis, mapa_doble, FUENTE, W, geo  # noqa: E402

OUT = os.path.join(BASE, '01_CLIMA_Y_CONFORT')
with open(os.path.join(OUT, 'B_DATOS', 'cli_stats.json'), encoding='utf-8') as f:
    R = json.load(f)

# ================================================================ CLI-06 · VEGETACION
doc = E.Doc(os.path.join(OUT, 'CLI-06_VEGETACION.pdf'), 'CLI-06 · VEGETACIÓN', '01 · CLIMA')
E.portada(doc, 'Vegetación y clima',
          'Qué hace de verdad la capa vegetal en el balance térmico: LAI por especie, '
          'transmitancia, evapotranspiración y una sensibilidad honesta al dato bibliográfico.',
          'CLI-06 · CLIMA Y CONFORT',
          [('ESPECIES', '17 reales'), ('ÁRBOLES', '20 (6+14)'),
           ('EVAPOTRANSPIRACIÓN', doc.metric('CLI06-M1', 425, 'L/h', 'B',
            'Penman por copa, kc 0.65', '_reclima9/vegetacion.json')),
           ('POTENCIA LATENTE', '286 kW')], num='CLI-06')
p, y = cabecera_analisis(
    doc, 'CLI-06', 'La vegetación no da la sombra: da lo demás',
    '¿Cuánto aporta la capa vegetal al clima del refugio y cuán sensible es el resultado '
    'al LAI bibliográfico?',
    'Cada especie entra al vóxel climático con su k_veg=0,5·LAI/3 (Beer–Lambert '
    'volumétrico); el arbolado OSM existente (Platanus, k 0,750) se distingue del nuevo '
    '(Celtis, k 0,633) por ancla. Evapotranspiración Penman con kc 0,65 por copa. '
    'Sensibilidad: k_veg ±30 % re-trazando la transmitancia solar del 15-jul.',
    '_veg_clima.json (17 especies), vegetacion.json, kvA/kvB.npy, sens_kveg (motor).',
    'B',
    'El LAI de cada especie es bibliográfico (ESTIMADO); las copas del término '
    'evapotranspirativo son cilindros del masterplan, no la silueta del asset.')
rows = [[b['bloque'], str(b['n']), '%.1f' % b['LAI'], '%.3f' % b['tau'],
         '%.0f' % b['L_h'], '%.1f' % b['kW']]
        for b in json.load(open(os.path.join(BASE, '..', 'FASE_03B9_HYPERDETAIL_V006',
                                             '_reclima9', '_data', 'vegetacion.json'),
                                encoding='utf-8'))['rows']]
y = p.tabla(E.MX, y - 0.05, E.A4W - 2 * E.MX,
            ['DOSEL ARBOLADO', 'N', 'LAI', 'TAU COPA', 'L/H', 'KW'],
            rows, col_w=[2.6, 0.5, 0.7, 1.1, 0.9, 0.9], size=7.4)
y -= 0.1
sens = R['sens_kveg']['resultado']
y = p.kicker(y, 'CLI-06.2 · SENSIBILIDAD LAI ±30 % (LOW / BASE / HIGH)')
y = p.tabla(E.MX, y, E.A4W - 2 * E.MX,
            ['HORA 15-JUL', 'SOMBRA LOW', 'SOMBRA BASE', 'SOMBRA HIGH', 'LECTURA'],
            [[h, '%.1f %%' % sens[h]['LOW']['pct_sombra'],
              '%.1f %%' % sens[h]['BASE']['pct_sombra'],
              '%.1f %%' % sens[h]['HIGH']['pct_sombra'],
              'la sombra apenas se mueve'] for h in sorted(sens)],
            col_w=[1.2, 1.2, 1.2, 1.2, 2.0], size=7.4)
doc.metric('CLI06-M2', '±1', 'p.p.', 'B', 'sens k_veg +-30% sobre fraccion de sombra',
           'cli_stats.json/sens_kveg')
y -= 0.08
y = p.dashlist(E.MX, y, [
    ('Hallazgo honesto:', 'la sombra del refugio es estructural. Quitar o poner un 30 % '
     'de LAI mueve la fracción de sombra ±1 punto. La vegetación NO es el parasol.'),
    ('Su papel real:', '286 kW de calor latente (el 21 % del total evaporativo), '
     'superficies frías (Tveg~Ta+2 frente a granito Ta+20), biodiversidad y la '
     'experiencia del jardín (06_USO_SOCIAL).'),
    ('Consecuencia de diseño:', 'una sequía que degrade el LAI no colapsa el refugio '
     'térmico; degrada el confort fino y el paisaje. Vulnerabilidad acotada.'),
], wrap=86, gap=0.1)
doc.add(p)
doc.close()
print('CLI-06 ok', doc.folio, 'pp')

# ================================================================ CLI-07 · AGUA
doc = E.Doc(os.path.join(OUT, 'CLI-07_AGUA.pdf'), 'CLI-07 · AGUA', '01 · CLIMA')
E.portada(doc, 'El agua que enfría',
          'Evaporación de láminas y splash, nebulización de alta presión, cámara de '
          'microalgas: cuánto enfría cada término y cuánta agua consume hacerlo.',
          'CLI-07 · CLIMA Y CONFORT',
          [('EVAPORACIÓN TOTAL', doc.metric('CLI07-M1', 2034, 'L/h', 'B',
            'suma de terminos agua', '_reclima9/metricas.json')),
           ('POTENCIA', '1.367 kW'), ('NIEBLA', '210 L/h · 141 kW'),
           ('REFUGIO EXTRA', '+501 m²')], num='CLI-07')
p, y = cabecera_analisis(
    doc, 'CLI-07', 'Kilovatios líquidos',
    '¿Cuánto enfriamiento compra cada litro y qué términos del sistema hídrico rinden más?',
    'Penman lámina libre por elemento de agua (splash, estanques, balsas) con su '
    'exposición solar real; nebulización isoentálpica con deriva por viento (gota 40 μm, '
    'eficiencia 0,55) evaluada en 9 escenarios caudal×clima; microalgas como lámina '
    'confinada del canopy (CLI-10 estudia su fallo).',
    'agua.json, neb_escenarios.json, mist_cov/mist_dT.npy, refugio.json.', 'B',
    'Penman es un techo teórico bajo cielo despejado; la deriva de niebla usa viento '
    'dominante constante; el balance diario completo (riego incluido) vive en 04_AGUA.')
mist = E.np_cli('mist_dT.npy')
ax = p.axes(E.MX, y - 3.1, 4.4, 2.95)
E.draw_context(ax, geo)
im = E.show_raster(ax, np.where(mist > 0.02, mist, np.nan), E.CMAP_AGUA, vmin=0, vmax=3)
E.cbar(p, im, E.MX, y - 3.4, 1.7, 'ΔTA NEBULIZACIÓN · K')
neb = list(csv.DictReader(open(os.path.join(OUT, 'B_DATOS', 'neb_escenarios.csv'),
                               encoding='utf-8-sig')))
yy = p.ficha(E.MX + 4.75, y - 0.1, [
    ('RESULTADO', 'La nube de niebla deriva con el viento y cubre ~%s m² efectivos; '
     'baja el aire local hasta 2-3 K en la zona cubierta y añade +501 m² de refugio.' %
     '1.100'),
    ('COSTE', '210 L/h en el escenario BASE — el 10 %% del agua evaporativa total. '
     'El término más eficiente por litro del sistema (04_AGUA lo cuantifica).'),
    ('RIESGO', 'Con humedad alta la depresión psicrométrica se hunde: en E1-húmedo el '
     'ΔT aplicado cae a 0,13 K. La niebla es un arma de día seco.'),
], wcol=2.7, wrap=36)
p.text(E.MX, y - 3.7, FUENTE, size=5.4, color=E.GRAYTX)
y = y - 4.0
y = p.kicker(y, 'CLI-07.2 · NUEVE ESCENARIOS DE NEBULIZACIÓN')
y = p.tabla(E.MX, y, E.A4W - 2 * E.MX,
            ['ESCENARIO', 'CLIMA', 'L/H', 'ΔT PSICR.', 'ΔT APLICADO'],
            [[n['escenario'], n['clima'], n['L_h'], n['dT_psicrometrico'] + ' K',
              n['dT_aplicado'] + ' K'] for n in neb],
            col_w=[1.3, 0.9, 0.9, 1.4, 1.4], size=7.2)
doc.add(p)
doc.close()
print('CLI-07 ok', doc.folio, 'pp')

# ================================================================ CLI-08 · VIENTO
doc = E.Doc(os.path.join(OUT, 'CLI-08_VIENTO.pdf'), 'CLI-08 · VIENTO', '01 · CLIMA')
E.portada(doc, 'Viento: el término\nno resuelto',
          'El modelo aplica el mismo viento a la plaza actual y a la propuesta. Este '
          'documento declara esa limitación, la acota con una sensibilidad y define '
          'qué haría falta para cerrarla.',
          'CLI-08 · CLIMA Y CONFORT',
          [('ESTADO', 'PENDIENTE DE CFD'), ('VIENTO E2', '%.1f m/s' % 2.9),
           ('SENSIBILIDAD −25 %', '+0,36 K UTCI'), ('SENSIBILIDAD −50 %', '+0,55 K UTCI')],
          num='CLI-08')
p, y = cabecera_analisis(
    doc, 'CLI-08', 'Qué pasaría si el dosel frena el viento',
    '¿Cuánto confort se perdería si la estructura abriga el viento que el UTCI da por '
    'disponible?',
    'El UTCI de CLI-04 usa el viento de escenario PVGIS idéntico en A y B (limitación '
    'declarada). Sensibilidad: recomputo del UTCI-B en E2/16h con viento −25 % y −50 % '
    'sobre la MRT real de la propuesta.',
    'sens_viento (motor final), u_E2_16_B + f_E2_16_B_Tmrt.', 'C',
    'Resolver el abrigo aerodinámico real requiere CFD urbano o medición en prototipo '
    '(roadmap municipal, fase B). Este documento acota el riesgo, no lo cierra.')
sv = R['sens_viento']['UTCI_B_E2_16']
x = E.MX
p.bignum(x, y, '%.1f' % sv['BASE'], '°C', 'UTCI-B medio E2/16h con viento de escenario'); x += 2.4
p.bignum(x, y, '+0,36', 'K', 'si el viento efectivo cae un 25 %'); x += 2.4
p.bignum(x, y, '+0,55', 'K', 'si cae un 50 % (abrigo fuerte)')
y -= 1.2
doc.metric('CLI08-M1', 0.55, 'K', 'C', 'UTCI(v x0.5) - UTCI(v) sobre MRT_B E2/16', 'cli_stats.json')
y = p.dashlist(E.MX, y, [
    ('El signo importa:', 'en verano, menos viento = peor confort. Si el dosel abriga '
     'con fuerza, hasta 0,55 K del beneficio de −2,5 K se devolverían.'),
    ('El neto sigue siendo claramente positivo', 'incluso en la cota pesimista '
     '(−2,5 + 0,55 = −1,95 K), porque el mecanismo dominante es radiativo.'),
    ('La geometría juega a favor:', 'el dosel es de hojas discontinuas a 8-12 m con '
     'porosidad alta; no es una bóveda cerrada. El caso −50 % es deliberadamente duro.'),
    ('Cierre pendiente:', 'CFD urbano de 2 direcciones dominantes o anemometría en el '
     'piloto (fase B del roadmap). Hasta entonces, este término se publica como C.'),
], wrap=86, gap=0.1)
doc.add(p)
doc.close()
print('CLI-08 ok', doc.folio, 'pp')

# ================================================================ CLI-09 · PROGRAMA
doc = E.Doc(os.path.join(OUT, 'CLI-09_CONFORT_POR_PROGRAMA.pdf'),
            'CLI-09 · PROGRAMA', '01 · CLIMA')
E.portada(doc, 'Confort por programa',
          'No un ráster: la experiencia térmica de cada uso — bancos, huerto, cinta, '
          'agua, accesos, atrio del Metro — con su sombra, su UTCI y su grado de refugio.',
          'CLI-09 · CLIMA Y CONFORT',
          [('PROGRAMAS', '9 zonas'), ('MEJOR', 'HUERTO −5,9 K'),
           ('CINTA', '−?'), ('ATRIO METRO', 'véase ficha')], num='CLI-09')
with open(os.path.join(OUT, 'B_DATOS', 'zonas_programa.csv'), encoding='utf-8-sig') as f:
    zrows = list(csv.DictReader(f))
p, y = cabecera_analisis(
    doc, 'CLI-09', 'Nueve maneras de estar en Sol',
    '¿Qué siente quien usa cada programa: quien espera al Metro, quien cultiva el '
    'huerto, quien camina la cinta a 6 m?',
    'Máscaras de programa sobre los campos de CLI-03/04: media zonal de sombra, MRT, '
    'UTCI y fracción de refugio; la cinta se evalúa en sus 186 estaciones a cota de '
    'tablero (+7,1 m) con su propio viento.',
    'zonas.json, cinta.json, spots.json (build 12).', 'A',
    'Las zonas son máscaras geométricas del programa arquitectónico; el uso real '
    'dependerá del comportamiento (06_USO_SOCIAL modela, no afirma).')
rows = [[z['zona'], z['m2'], z['sombra_B'] + ' %', z['UTCI_A'] + '›' + z['UTCI_B'],
         z['dUTCI'] + ' K', z['refugio_pct'] + ' %'] for z in zrows]
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['PROGRAMA', 'M²', 'SOMBRA B', 'UTCI A›B', 'ΔUTCI', 'REFUGIO'],
            rows, col_w=[2.15, 0.75, 1.0, 1.25, 0.95, 0.9], size=7.2)
doc.metric('CLI09-M1', -5.9, 'K', 'A', 'dUTCI zona HUERTO C1', 'zonas.json')
y -= 0.1
cin = R['cinta_resumen']
y = p.kicker(y, 'CLI-09.2 · LA CINTA: CAMINAR A SEIS METROS')
y = p.dashlist(E.MX, y, [
    ('La cinta es la paradoja del proyecto:', 'solo el 22,6 %% de sus 186 estaciones va '
     'en sombra y su UTCI medio (38,0 °C) es apenas mejor que la plaza actual. A cota '
     'de tablero el viento sube (2,4 m/s frente a 1,0 a nivel de suelo) y compensa parte.'),
    ('Lectura:', 'la cinta NO es un programa de estancia térmica: es un mirador en '
     'movimiento. Su papel climático es dar sombra A LOS DE ABAJO, no a sus usuarios.'),
    ('Candidato de mejora documentado (§54):', 'sombra ligera sobre los tramos sur de la '
     'cinta — se documenta como modificación potencial, NO se implementa.'),
], wrap=86, gap=0.1)
doc.metric('CLI09-M2', 22.6, '%', 'A', 'estaciones de cinta en sombra', 'cinta.json')
doc.metric('CLI09-M3', 38.0, '°C', 'A', 'UTCI medio de la cinta E2/16', 'cinta.json')
doc.add(p)
doc.close()
print('CLI-09 ok', doc.folio, 'pp')

# ================================================================ CLI-10 · FALLOS
doc = E.Doc(os.path.join(OUT, 'CLI-10_ESCENARIOS_DE_FALLO.pdf'),
            'CLI-10 · FALLOS', '01 · CLIMA')
E.portada(doc, 'Cuando algo falla',
          'El refugio sin nebulización, sin agua, con la cámara de microalgas seca, en '
          'ola de calor y con la vegetación degradada: cuánto beneficio sobrevive a cada '
          'fallo y cuál es el mínimo garantizado.',
          'CLI-10 · CLIMA Y CONFORT',
          [('MÍNIMO GARANTIZADO', 'la sombra estructural'),
           ('PEOR FALLO', 'canopy seco: +6,9 K MRT local'),
           ('OLA DE CALOR', 'ΔUTCI −2,0 K'), ('NIVEL', 'B/C declarado')], num='CLI-10')
p, y = cabecera_analisis(
    doc, 'CLI-10', 'Ingeniería del fallo',
    '¿Qué parte del beneficio climático sobrevive a cada modo de fallo del sistema?',
    'Composición de los términos ya medidos: E3 simulado (ola de calor); niebla OFF por '
    'diferencia refugio/refugio_neb; sin agua por supresión de términos latentes; canopy '
    'seco por linealización radiativa (tau 0,12 › 0,25); vegetación por sensibilidad LAI.',
    'cli_stats.json (motor), refugio.json, aire.json, PARAMS de clima_core.', 'B',
    'Los modos de fallo no simulan dinámica transitoria (cuánto tarda en secarse una '
    'cámara); son estados estacionarios pesimistas.')
rows = [
    ['Sin nebulización', 'válvulas cerradas / avería', '−501 m² de refugio (queda 3.876)', 'A'],
    ['Sin agua total', 'corte de red + depósitos vacíos', '−0,43 K de aire + niebla OFF; la sombra persiste', 'B'],
    ['Canopy seco', 'cámara de microalgas vacía', '+6,9 K MRT bajo 700 m² de dosel (~+2,4 K UTCI local)', 'C'],
    ['Ola de calor E3', 'Ta 38 °C, RH 10 %', 'ΔUTCI −2,0 K (rinde, pero la cola positiva crece a 1.175 m²)', 'A'],
    ['Vegetación −30 %', 'sequía / plaga / poda dura', 'sombra −1 p.p.; se pierde confort fino y 1/3 del latente vegetal', 'B'],
]
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['MODO DE FALLO', 'CAUSA TIPO', 'EFECTO CLIMÁTICO', 'NIVEL'],
            rows, col_w=[1.5, 1.65, 3.35, 0.5], size=7.3)
doc.metric('CLI10-M1', 6.9, 'K', 'C', 'dMRT bajo dosel con tau_canopy 0.25', 'cli_stats.json/canopy_seco')
y -= 0.12
y = p.panel(E.MX, y, E.A4W - 2 * E.MX, 1.25, 'EL MÍNIMO GARANTIZADO')
p.text(E.MX + 0.16, y, 'El refugio se diseñó para degradarse bien: el mecanismo dominante '
       '(sombra estructural, −10,9 K de MRT) no consume agua, no depende de bombas y no '
       'se seca. Todos los modos de fallo estudiados erosionan el margen — ninguno '
       'devuelve la plaza al estado A. El peor caso combinado (seco+ola de calor) '
       'conserva del orden de dos tercios del beneficio UTCI.', size=8.2, wrap=92)
doc.add(p)
doc.close()
print('CLI-10 ok', doc.folio, 'pp')
