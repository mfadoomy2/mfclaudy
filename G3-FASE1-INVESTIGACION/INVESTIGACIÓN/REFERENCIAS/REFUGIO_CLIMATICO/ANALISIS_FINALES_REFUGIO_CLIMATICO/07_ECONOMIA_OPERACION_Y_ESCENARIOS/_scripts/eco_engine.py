# -*- coding: utf-8 -*-
"""FASE FINAL - MOTOR ECONOMICO (ECO-01..03) sobre v006.

CAPEX por analogia declarada (C), OPEX por componentes (B/C), escenarios de comercio
LOW/BASE/HIGH (C) y ciclo de vida. TODAS las fuentes externas con URL/institucion/fecha.
Ninguna extrapolacion se presenta como hecho.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
RC = os.path.normpath(os.path.join(BASE, '..'))
MONT = os.path.normpath(os.path.join(RC, '..'))
OUT = os.path.join(BASE, '07_ECONOMIA_OPERACION_Y_ESCENARIOS', 'B_DATOS')
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402

FUENTES = [
    dict(id='F-01', dato='Estacion Sol (Metro): >73 millones de viajeros en 2024 (+11,5%)',
         url='https://www.eldiario.es/madrid/somos/metro-madrid-bate-record-historico-viajeros-son-diez-estaciones-utilizadas_1_11969185.html',
         institucion='Metro de Madrid via elDiario.es', fecha='2025-01', licencia='prensa',
         resolucion='anual por estacion'),
    dict(id='F-02', dato='Metro de Madrid: 715,2 M viajes 2024 (record historico)',
         url='https://www.comunidad.madrid/noticias/2025/01/16/comunidad-madrid-bate-record-historico-usuarios-metro-715-millones-viajes-2024-incremento-8-respecto-ano-anterior',
         institucion='Comunidad de Madrid', fecha='2025-01-16', licencia='nota oficial',
         resolucion='anual red'),
    dict(id='F-03', dato='Calle Preciados: ~13.800 peatones/dia de media; picos 21.200-26.300 en rebajas',
         url='https://www.tcgroupsolutions.com/recurso/calles-comerciales-espana/',
         institucion='TC Group Solutions (contadores) + reasonwhy.es', fecha='2024-2025',
         licencia='informe comercial', resolucion='diaria por punto de conteo'),
    dict(id='F-04', dato='Aforos peatonales oficiales disponibles (portal de datos abiertos)',
         url='https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=695cd64d6f9b9610VgnVCM1000001d4a900aRCRD',
         institucion='Ayuntamiento de Madrid', fecha='continuo', licencia='datos abiertos',
         resolucion='horaria por punto'),
    dict(id='F-05', dato='Sevilla: toldos en 30 calles del centro, 1.703.228 EUR (4 anos); puente San Telmo 1,1 M EUR',
         url='https://www.sevilla.org/actualidad/noticias/2026/el-gobierno-de-jose-luis-sanz-amplia-las-zonas-de-sombra-en-sevilla-toldos-en-30-calles-del-centro-y-en-el-puente-de-san-telmo',
         institucion='Ayuntamiento de Sevilla', fecha='2026-03', licencia='nota oficial',
         resolucion='contrato'),
    dict(id='F-06', dato='Tarifas de agua Canal de Isabel II 2025-2026 (BOCM 31-05-2025); uso comercial sin subida',
         url='https://www.bocm.es/boletin/CM_Orden_BOCM/2025/05/31/BOCM-20250531-3.PDF',
         institucion='BOCM / Canal de Isabel II', fecha='2025-05-31', licencia='boletin oficial',
         resolucion='bloque tarifario'),
]

# ---------------------------------------------------------------- CAPEX (C)
CAPEX = [
    dict(partida='Dosel estructural (80 mastiles, 93 hojas, cables, microalgas)',
         low=2.5, base=3.8, high=5.2,
         analogia='membrana tensada + estructura 600-1.200 EUR/m2 proyectado sobre 4.186 m2 de sombra'),
    dict(partida='Cinta elevada (733 m, tablero 2,5 m, 43 soportes, barandilla)',
         low=1.6, base=2.1, high=2.9, analogia='pasarela urbana 900-1.500 EUR/m2 de tablero'),
    dict(partida='Ascensores (3) + escaleras (6)', low=0.7, base=0.9, high=1.2,
         analogia='aparato urbano exterior 150-250 kEUR/ud + obra'),
    dict(partida='Sistema de agua (laminas, splash, red enterrada, bombas, niebla, depositos)',
         low=0.8, base=1.1, high=1.6, analogia='fuentes transitables municipales comparables'),
    dict(partida='Vegetacion, jardineras, suelos y mobiliario', low=0.6, base=0.9, high=1.3,
         analogia='jardineria intensiva de centro historico'),
    dict(partida='Pods, atrio Metro, iluminacion, control', low=0.5, base=0.7, high=1.0,
         analogia='equipamiento ligero + BMS'),
]
sub = {k: round(sum(p[k] for p in CAPEX), 1) for k in ('low', 'base', 'high')}
CAPEX_TOTAL = {k: round(sub[k] * 1.25, 1) for k in sub}   # +25% honorarios/imprevistos/IVA no incl.

# ---------------------------------------------------------------- OPEX (B/C)
OPEX = [
    dict(partida='Agua (temporada critica + riego anual)', low=6, base=9, high=14,
         metodo='~3.000 m3/ano x 2,0-3,0 EUR/m3 (bloque no domestico BOCM, pendiente bloque exacto)'),
    dict(partida='Energia (bombas, niebla alta presion, 3 ascensores, iluminacion)',
         low=10, base=15, high=22, metodo='60-110 MWh/ano x 0,15-0,20 EUR/kWh'),
    dict(partida='Mantenimiento ascensores (SLA <48 h)', low=9, base=12, high=18,
         metodo='3 uds x contrato urbano 3-6 kEUR/ud/ano'),
    dict(partida='Jardineria intensiva (17 especies, hidrozonas)', low=60, base=90, high=130,
         metodo='plantilla + reposicion 5-8% anual'),
    dict(partida='Limpieza + membrana + camara de microalgas', low=70, base=110, high=160,
         metodo='quincenal camara (TEC-02), semestral membrana, diario suelo'),
    dict(partida='Inspecciones, seguros y gestion', low=25, base=40, high=60,
         metodo='matriz TEC-02 + estandar municipal'),
]
OPEX_TOTAL = {k: int(sum(p[k] for p in OPEX)) for k in ('low', 'base', 'high')}

# fondo de reposicion (ciclo de vida): componentes / vida util de TEC-02
REPOSICION = [
    ('Membrana dosel', 3.8 * 0.45, 18), ('Pods (membrana)', 0.35, 10),
    ('Nebulizadores', 0.12, 7), ('Ascensores (renovacion)', 0.6, 20),
    ('Mobiliario', 0.25, 15), ('Bombas y valvulas', 0.2, 12),
]
fondo = sum(v / vida for _, v, vida in REPOSICION)

# ---------------------------------------------------------------- COMERCIO (C)
# flujo adicional x tiempo adicional x exposicion x conversion x ticket — 3 escenarios
COM = {}
for esc, (dflujo, dtiempo_min, expo, conv, ticket) in dict(
        LOW=(0.02, 3, 0.5, 0.010, 12.0),
        BASE=(0.05, 6, 0.6, 0.015, 15.0),
        HIGH=(0.10, 10, 0.7, 0.020, 18.0)).items():
    base_flujo = 60000
    extra_visitas = base_flujo * dflujo
    gasto_dia = extra_visitas * expo * conv * ticket
    # el tiempo adicional actua sobre los que YA estan: mas exposicion de escaparate
    gasto_tiempo = base_flujo * 0.25 * (dtiempo_min / 60.0) * 0.10 * conv * ticket * 60
    COM[esc] = dict(flujo_adicional_pct=100 * dflujo, tiempo_adicional_min=dtiempo_min,
                    exposicion=expo, conversion_pct=100 * conv, ticket_eur=ticket,
                    gasto_incremental_eur_dia=int(gasto_dia + gasto_tiempo),
                    gasto_temporada_93d_keur=round((gasto_dia + gasto_tiempo) * 93 / 1000, 0))

R = dict(baseline='v006 build 12', fuentes=FUENTES,
         capex_MEUR=dict(partidas=CAPEX, subtotal=sub, total_con_25pct=CAPEX_TOTAL,
                         nivel='C — analogia declarada, sin proyecto de ejecucion'),
         opex_kEUR_ano=dict(partidas=OPEX, total=OPEX_TOTAL,
                            fondo_reposicion_MEUR_ano=round(fondo, 2),
                            nivel='B/C segun partida'),
         comercio=dict(escenarios=COM, ancla_flujo='60.000/dia (hipotesis BASE, ver F-03/F-04)',
                       nivel='C — modelo de escenarios, jamas un hecho'),
         contexto=dict(sevilla_toldos_MEUR=1.70, sevilla_calles=30,
                       sol_metro_viajeros_M=73, preciados_peatones_dia=13800))

with open(os.path.join(OUT, 'eco_stats.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
import csv
with open(os.path.join(OUT, 'fuentes_externas.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(FUENTES[0].keys()))
    w.writeheader(); w.writerows(FUENTES)

flog.event(fase='FINAL', tipo_evento='motor_economia',
           objetivo='ECO: CAPEX/OPEX/comercio LOW-BASE-HIGH con fuentes externas registradas',
           resultado='CAPEX %s MEUR; OPEX %s kEUR/ano + fondo %.2f MEUR/ano; comercio BASE %d EUR/dia; %d fuentes'
                     % (CAPEX_TOTAL, OPEX_TOTAL, fondo,
                        COM['BASE']['gasto_incremental_eur_dia'], len(FUENTES)))
print('CAPEX MEUR:', CAPEX_TOTAL)
print('OPEX kEUR/ano:', OPEX_TOTAL, '+ fondo reposicion %.2f MEUR/ano' % fondo)
print('comercio (EUR/dia):', {k: v['gasto_incremental_eur_dia'] for k, v in COM.items()})
