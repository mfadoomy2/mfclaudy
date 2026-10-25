# -*- coding: utf-8 -*-
"""FASE FINAL - MOTOR AGUA+ECOLOGIA (AGU-01..03) sobre v006.

Balance hidrico diario del dia punta, hidrozonas de riego por necesidad de especie,
biodiversidad/estacionalidad del masterplan, y el cruce AGUA x CLIMA:
litros por unidad de beneficio de cada mecanismo.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
RC = os.path.normpath(os.path.join(BASE, '..'))
MONT = os.path.normpath(os.path.join(RC, '..'))
F9 = os.path.join(RC, 'FASE_03B9_HYPERDETAIL_V006')
OUT = os.path.join(BASE, '04_AGUA_ECOLOGIA_Y_VEGETACION', 'B_DATOS')
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402


def J(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


agua = J(os.path.join(F9, '_reclima9', '_data', 'agua.json'))
veg = J(os.path.join(F9, '_reclima9', '_data', 'vegetacion.json'))
mets = J(os.path.join(F9, '_reclima9', '_data', 'metricas.json'))
refugio = J(os.path.join(F9, '_reclima9', '_data', 'refugio.json'))
vclima = J(os.path.join(F9, '_veg_clima.json'))
with open(os.path.join(F9, 'BOTANICAL_MASTERPLAN_v001.csv'), encoding='utf-8-sig') as f:
    plan = list(csv.DictReader(f))

R = dict(baseline='v006 build 12')

# ---------------------------------------------------------------- 1 · balance dia punta
# evaporacion de laminas (agua.json, E2 16h extrapolado por perfil diario del propio json)
evap_laminas_m3 = agua['m3_dia']                       # 24.43 (ya integrado a dia)
# riego: evapotranspiracion vegetal medida (punta 425 L/h) -> dia equivalente 8 h de punta
# (perfil solar) x ineficiencia de riego por goteo 1.30 (perdidas+percolacion)  [INFERIDO B]
et_veg_dia_m3 = veg['L_h'] * 8 / 1000.0
riego_dia_m3 = round(et_veg_dia_m3 * 1.30, 1)
# nebulizacion: 210 L/h en dias secos, 6 h de operacion tipica  [ESCENARIO C]
neb_dia_m3 = round(210 * 6 / 1000.0, 2)
total_punta = round(evap_laminas_m3 + riego_dia_m3 + neb_dia_m3, 1)
R['balance_dia_punta_m3'] = dict(
    evaporacion_laminas=evap_laminas_m3, riego_vegetal=riego_dia_m3,
    nebulizacion=neb_dia_m3, total=total_punta,
    nota='dia punta E2: laminas MEDIDAS (Penman por elemento, integradas por el modelo); '
         'riego = ET vegetal x1,30 de ineficiencia (B); niebla 6 h de operacion (C).')
R['almacenamiento'] = dict(
    V_depositos_m3=agua['V_dep_m3'],
    autonomia_dias_laminas=agua['autonomia_dias'],
    autonomia_dias_total=round(agua['V_dep_m3'] / total_punta, 1),
    nota='autonomia frente a corte de red con demanda de dia punta completa')
R['recirculacion'] = dict(
    perdida_real='solo la evaporacion: el splash y estanques recirculan por las mains '
                 'enterradas; la reposicion diaria es el propio balance evaporativo',
    mains_polilineas=4)

# dia medio (E1): escala por depresion psicrometrica aproximada Penman ~ (1-RH)·f(T)
# E1: Ta 27.6 RH 26.4 vs E2: 34.7/15.0 -> factor ~0.62  [INFERIDO B]
R['balance_dia_medio_m3'] = dict(total=round(evap_laminas_m3 * 0.62 + riego_dia_m3 * 0.85, 1),
                                 factor='0,62 laminas · 0,85 riego (dia tipico E1)')

# ---------------------------------------------------------------- 2 · hidrozonas
NEED_L = {'alta': 6.0, 'media': 3.5, 'baja': 1.5, 'muy baja': 0.8, 'acuatica': 0.0}
hidro = {}
for p_ in plan:
    need = p_['necesidad_hidrica'].strip().lower()
    hidro.setdefault(need, []).append(p_['especie'])
R['hidrozonas'] = {k: dict(especies=v, dosis_L_m2_dia=NEED_L.get(k, 3.5))
                   for k, v in hidro.items()}

# ---------------------------------------------------------------- 3 · biodiversidad
estrategia = {}
for p_ in plan:
    estrategia.setdefault(p_['estrategia_estacional'].strip().lower(), []).append(p_['especie'])
R['estacionalidad'] = {k: len(v) for k, v in estrategia.items()}
import re


def _h(p_):
    m = re.search(r'[\d.]+', p_['altura_adulta_m'] or '0')
    return float(m.group()) if m else 0.0


R['biodiversidad'] = dict(
    especies=len(plan),
    estratos=dict(arboreo=len([p_ for p_ in plan if _h(p_) >= 4]),
                  arbustivo=len([p_ for p_ in plan if 1.0 <= _h(p_) < 4]),
                  herbaceo=len([p_ for p_ in plan if _h(p_) < 1.0])),
    acuaticas=len([p_ for p_ in plan if 'acuat' in p_['necesidad_hidrica'].lower()
                   or 'Nymphaea' in p_['especie'] or 'Typha' in p_['especie']]),
    nota_honesta='las tropicales de sotobosque (Monstera, Alocasia, Calathea) viven del '
                 'microclima del dosel: fuera de el no sobreviven al invierno de Madrid. '
                 'Son una APUESTA condicionada al rendimiento del refugio (C).')

# ---------------------------------------------------------------- 4 · AGUA x CLIMA
ref_m2 = refugio['clases']['REFUGIO EFECTIVO']['m2']
ref_m2_neb = refugio['clases']['REFUGIO EFECTIVO']['m2_neb']
R['eficiencia'] = dict(
    L_dia_por_m2_refugio=round(total_punta * 1000 / ref_m2_neb, 1),
    mecanismos=[
        dict(mecanismo='Sombra estructural', L_dia=0, beneficio='−10,9 K MRT / 3.876 m2',
             L_por_m2_beneficio=0.0,
             lectura='el mecanismo dominante no consume agua: es geometria'),
        dict(mecanismo='Laminas + splash', L_dia=int(evap_laminas_m3 * 1000),
             beneficio='−0,43 K aire (latente) + superficies frias',
             L_por_m2_beneficio=round(evap_laminas_m3 * 1000 / ref_m2, 1),
             lectura='el termino mas caro en litros; parte es recreativo (splash jugable)'),
        dict(mecanismo='Nebulizacion', L_dia=int(neb_dia_m3 * 1000),
             beneficio='+501 m2 de refugio en dia seco',
             L_por_m2_beneficio=round(neb_dia_m3 * 1000 / 501, 1),
             lectura='2,5 L/dia por m2 de refugio anadido: el agua mas rentable del sistema'),
        dict(mecanismo='Riego vegetal', L_dia=int(riego_dia_m3 * 1000),
             beneficio='286 kW latentes + paisaje + biodiversidad',
             L_por_m2_beneficio=None,
             lectura='su retorno principal no es termico: es ecologico y social'),
    ],
    nota='persona-hora protegida por litro se calcula en 10_SINTESIS con el modelo de '
         'uso (SOC); aqui solo ratios geometricos A/B.')

with open(os.path.join(OUT, 'agu_stats.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)

# CSV de elementos de agua
with open(os.path.join(OUT, 'elementos_agua.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(agua['rows'][0].keys()))
    w.writeheader(); w.writerows(agua['rows'])

flog.event(fase='FINAL', tipo_evento='motor_agua',
           objetivo='AGU: balance hidrico dia punta/medio, hidrozonas, biodiversidad, agua x clima',
           resultado='dia punta %.1f m3 (laminas %.1f + riego %.1f + niebla %.2f); '
                     'autonomia total %.1f dias; %.1f L/dia por m2 de refugio'
                     % (total_punta, evap_laminas_m3, riego_dia_m3, neb_dia_m3,
                        R['almacenamiento']['autonomia_dias_total'],
                        R['eficiencia']['L_dia_por_m2_refugio']))
print(json.dumps(R['balance_dia_punta_m3'], ensure_ascii=False))
print(json.dumps(R['almacenamiento'], ensure_ascii=False))
print(json.dumps(R['eficiencia']['L_dia_por_m2_refugio'], ensure_ascii=False))
