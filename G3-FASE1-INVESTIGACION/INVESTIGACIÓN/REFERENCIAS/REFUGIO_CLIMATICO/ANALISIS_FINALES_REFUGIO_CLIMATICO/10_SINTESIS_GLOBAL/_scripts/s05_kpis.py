# -*- coding: utf-8 -*-
"""FASE FINAL - S05: indicadores cruzados nuevos (§18) + INDICADORES_CRUZADOS.pdf."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
RC = os.path.normpath(os.path.join(BASE, '..'))
MONT = os.path.normpath(os.path.join(RC, '..'))
F9 = os.path.join(RC, 'FASE_03B9_HYPERDETAIL_V006')
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
sys.path.insert(0, os.path.join(BASE, '01_CLIMA_Y_CONFORT', '_scripts'))
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402
import refugio_editorial as E  # noqa: E402
from cli_common import cabecera_analisis  # noqa: E402

OUT = os.path.join(BASE, '10_SINTESIS_GLOBAL')
os.makedirs(os.path.join(OUT, 'B_DATOS'), exist_ok=True)


def J(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


mets = J(os.path.join(F9, '_reclima9', '_data', 'metricas.json'))
aud = J(os.path.join(F9, '_reaudit9', '_data', 'summary.json'))
soc = J(os.path.join(BASE, '06_USO_SOCIAL_Y_EXPERIENCIA', 'B_DATOS', 'soc_stats.json'))
agu = J(os.path.join(BASE, '04_AGUA_ECOLOGIA_Y_VEGETACION', 'B_DATOS', 'agu_stats.json'))
eco = J(os.path.join(BASE, '07_ECONOMIA_OPERACION_Y_ESCENARIOS', 'B_DATOS', 'eco_stats.json'))
mob = J(os.path.join(BASE, '02_MOVILIDAD_Y_ACCESIBILIDAD', 'B_DATOS', 'mob_stats.json'))
pat = J(os.path.join(BASE, '08_PATRIMONIO_VISUALES_Y_PAISAJE_URBANO', 'B_DATOS', 'pat_stats.json'))
a1 = J(os.path.join(F9, '_reaudit9', '_data', 'a1_paths.json'))

# ---------------------------------------------------------------- COBERTURA REAL (nuevo)
# sombra x flujo: fraccion del FLUJO peatonal (no de la superficie) que camina en sombra.
sh = np.load(os.path.join(F9, '_reclima9', '_data', 'shade_crit_B.npy'))
shA = np.load(os.path.join(F9, '_reclima9', '_data', 'shade_crit_A.npy'))
X0, Y0, CS = -112, -45, 0.5
ny, nx = sh.shape
ejes = {r['id']: r for r in J(os.path.join(F9, '_reaudit9', '_data', 'a5_access.json'))['rows']}
flujo_w = {e['id']: e['w_p05'] for e in ejes.values()
           if 'CINTA' not in e['id'].upper()}   # la cinta es ruta de tablero, no transito a suelo
wsum = sum(flujo_w.values())
cob_B = cob_A = 0.0
detalle = []
for p_ in a1['paths']:
    xs = [r['x'] for r in p_['rows']]
    ys = [r['y'] for r in p_['rows']]
    sB, sA, n = 0.0, 0.0, 0
    for x, y in zip(xs, ys):
        j = int((x - X0) / CS); i = int((y - Y0) / CS)
        if 0 <= i < ny and 0 <= j < nx and np.isfinite(sh[i, j]):
            sB += sh[i, j]; sA += np.nan_to_num(shA[i, j]); n += 1
    if not n:
        continue
    w = flujo_w.get(p_['id'], 0) / wsum
    detalle.append(dict(eje=p_['id'], sombra_media_B=round(sB / n, 3),
                        sombra_media_A=round(sA / n, 3), peso_flujo=round(w, 3)))
    cob_B += w * sB / n
    cob_A += w * sA / n

ph = soc['personas_hora']['escenarios']
KPI = [
    dict(nombre='EFICIENCIA ESPACIAL DEL REFUGIO',
         formula='m² de refugio efectivo / m² de suelo ocupado por el proyecto',
         valor='%.1f' % (3876.0 / (aud['area_ambito'] * aud['ocupacion'] / 100.0)),
         unidad='m²/m²', nivel='A',
         lectura='cada metro de suelo que el proyecto ocupa produce ~4 m² de refugio: '
                 'la sombra trabaja en voladizo, no en planta'),
    dict(nombre='COBERTURA REAL DE TRÁNSITO (sombra × flujo)',
         formula='Σ (peso de flujo por eje × sombra media sobre su traza)',
         valor='%.1f %% (antes %.1f %%)' % (100 * cob_B, 100 * cob_A),
         unidad='% del flujo', nivel='B',
         lectura='el peatón MEDIO en tránsito camina en sombra el %.1f %% de su cruce '
                 '(antes %.1f %%): ×%.0f — la cara amable de D-015; los ejes no están '
                 'sombreados del todo, pero tampoco a cero' % (100 * cob_B, 100 * cob_A, cob_B / cob_A)),
    dict(nombre='EFICIENCIA HÍDRICA SOCIAL',
         formula='litros de agua totales / persona-hora protegida (BASE)',
         valor='%.1f' % (agu['balance_dia_punta_m3']['total'] * 1000 /
                         ph['BASE']['personas_hora_protegidas_dia']),
         unidad='L/p·h', nivel='C',
         lectura='13,9 L por persona-hora protegida — una cisterna y media; en HIGH '
                 'baja a 3,1 L: el agua rinde más cuanta más gente protege'),
    dict(nombre='EFICIENCIA DE MANTENIMIENTO',
         formula='personas-hora protegidas/año (BASE) / horas anuales de conservación',
         valor='%.0f' % (ph['BASE']['personas_hora_protegidas_dia'] * 93 / 6000.0),
         unidad='p·h por hora de trabajo', nivel='C',
         lectura='cada hora de cuadrilla compra ~33 personas-hora de confort: la '
                 'conservación no es gasto muerto, es producción de refugio'),
    dict(nombre='VISIBILIDAD EFECTIVA DEL RELOJ',
         formula='visibilidad ponderada por potencial de estancia (vis × IPE)',
         valor='%.1f %% (41,5 %% por superficie)' % pat['ponderada']['RELOJ']['pct_ponderado_uso'],
         unidad='%', nivel='B',
         lectura='la métrica clásica sobreestima la experiencia real del patrimonio: '
                 'D-003 nace de este indicador'),
    dict(nombre='COSTE POR PERSONA-HORA (25 AÑOS)',
         formula='(CAPEX + 25·OPEX+fondo) / p·h acumuladas',
         valor='4,9 (1,1–29)', unidad='€/p·h', nivel='C',
         lectura='el indicador de decisión municipal: umbral propuesto 8 €/p·h con '
                 'regla de validación en piloto'),
    dict(nombre='ROBUSTEZ AL FALLO',
         formula='fracción del ΔUTCI que sobrevive al peor fallo combinado',
         valor='~66', unidad='%', nivel='B',
         lectura='ningún modo de fallo devuelve la plaza al estado actual (D-009)'),
]

with open(os.path.join(OUT, 'B_DATOS', 'kpis.json'), 'w', encoding='utf-8') as f:
    json.dump(dict(kpis=KPI, cobertura_detalle=detalle), f, ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- PDF
doc = E.Doc(os.path.join(OUT, 'INDICADORES_CRUZADOS.pdf'),
            'INDICADORES CRUZADOS', '10 · SÍNTESIS')
E.portada(doc, 'Siete números\nque no existían',
          'Indicadores inventados a partir de los datos del proyecto (§18): métricas '
          'de cruce que ningún análisis individual podía producir y que ordenan la '
          'decisión municipal.',
          '10 · SÍNTESIS GLOBAL · INDICADORES',
          [('NUEVOS KPI', '7'), ('EL MÁS POTENTE', '4 m² refugio / m² ocupado'),
           ('EL MÁS HONESTO', '€/p·h con horquilla ×26'),
           ('NIVEL', 'A–C declarado')], num='KPI')
p, y = cabecera_analisis(
    doc, 'KPI', 'Métricas de segunda generación',
    '¿Qué se aprende cruzando sistemas que ningún ráster enseña por separado?',
    'Cada indicador declara fórmula, fuentes y nivel. La cobertura real de tránsito se '
    'calcula aquí por primera vez: sombra media sobre la traza de cada eje ponderada '
    'por su peso de flujo.',
    'metricas.json + soc/agu/eco/mob/pat_stats.json + shade_crit_B × a1_paths.', 'B',
    'Los KPI con componentes C (uso, coste) heredan ese nivel y se publican con '
    'horquilla, nunca con decimales de falsa precisión.')
rows = [[k['nombre'], k['valor'] + ' ' + k['unidad'], k['nivel'], k['lectura']]
        for k in KPI]
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['INDICADOR', 'VALOR', 'NIVEL', 'LECTURA'],
            rows, col_w=[1.7, 1.3, 0.5, 3.5], size=6.7)
for k in KPI:
    doc.metric('KPI-' + k['nombre'][:18].replace(' ', '_'), k['valor'], k['unidad'],
               k['nivel'][:1], k['formula'], 'kpis.json')
doc.add(p)
doc.close()

flog.event(fase='FINAL', tipo_evento='kpis',
           objetivo='7 indicadores cruzados nuevos (§18) + INDICADORES_CRUZADOS.pdf',
           resultado='eficiencia espacial %.1f m2/m2; cobertura real transito %.0f%% (antes %.0f%%); '
                     'hidrica %.1f L/ph; mantenimiento ~33 ph/h'
                     % (3876.0 / (aud['area_ambito'] * aud['ocupacion'] / 100.0),
                        100 * cob_B, 100 * cob_A,
                        agu['balance_dia_punta_m3']['total'] * 1000 /
                        ph['BASE']['personas_hora_protegidas_dia']))
print('cobertura real B/A: %.3f / %.3f' % (cob_B, cob_A))
print('detalle ejes:', json.dumps(detalle, ensure_ascii=False)[:400])
print('PDF ok')
