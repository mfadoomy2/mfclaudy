# -*- coding: utf-8 -*-
"""FASE FINAL - MOTOR CLIMATICO (CLI-01..CLI-10) sobre la baseline v006.

Consume los campos de _reclima9/_data (build 12) y produce en B_DATOS/:
  cli_stats.json  - estadisticas por escenario/hora/estado, deltas, colas, sombra,
                    invierno, sensibilidades (viento, k_veg, canopy seco, sin agua)
  *.csv           - zonas, cinta, spots, categorias UTCI
Todo calculo nuevo queda etiquetado con su nivel (A/B/C) y su hipotesis.
"""
import csv
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
RC = os.path.normpath(os.path.join(BASE, '..'))
MONT = os.path.normpath(os.path.join(RC, '..'))
F9 = os.path.join(RC, 'FASE_03B9_HYPERDETAIL_V006')
CLI = os.path.join(F9, '_reclima9', '_data')
AUD = os.path.join(F9, '_reaudit9', '_data')
OUT = os.path.join(BASE, '01_CLIMA_Y_CONFORT', 'B_DATOS')
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402


def L(n, d=CLI):
    return np.load(os.path.join(d, n))


def J(n, d=CLI):
    with open(os.path.join(d, n), encoding='utf-8') as f:
        return json.load(f)


# ---------------------------------------------------------------- mascaras
walk25 = L('walk.npy', AUD)            # 0.25 m
cause25 = L('cause.npy', AUD)
walk = walk25[::2, ::2]                # 0.5 m (mismo submuestreo que clima_run)
cause = cause25[::2, ::2]
ny, nx = L('u_E2_16_B.npy').shape
walk = walk[:ny, :nx]
cause = cause[:ny, :nx]
CELLA = 0.25                            # m2 por celda clima (0.5 x 0.5)
W = walk.astype(bool)
NW = int(W.sum())

FAM_ORDER = ['CONTEXT', 'STRUCTURE', 'RIBBON', 'PODS', 'CANOPY', 'PLANTER',
             'VEGETATION', 'FURNITURE', 'WATER']

# UTCI: clases oficiales de estres por calor
UTCI_CLASES = [(-99, 26, 'SIN ESTRÉS / LEVE'), (26, 32, 'MODERADO'),
               (32, 38, 'FUERTE'), (38, 46, 'MUY FUERTE'), (46, 99, 'EXTREMO')]


def stats_field(a, mask=W):
    v = a[mask]
    v = v[np.isfinite(v)]
    return dict(media=round(float(v.mean()), 2), p50=round(float(np.median(v)), 2),
                p05=round(float(np.percentile(v, 5)), 2),
                p95=round(float(np.percentile(v, 95)), 2),
                min=round(float(v.min()), 2), max=round(float(v.max()), 2))


def utci_cats(u, mask=W):
    v = u[mask]
    v = v[np.isfinite(v)]
    out = {}
    for lo, hi, nombre in UTCI_CLASES:
        out[nombre] = round(float(((v >= lo) & (v < hi)).sum() * CELLA), 0)
    return out


R = dict(baseline='v006 build 12', celda_m=0.5, area_pisable_m2=round(NW * CELLA, 0))

# ================================================= CLI-03/04 · MRT y UTCI por escenario
esc_stats = {}
for e in ('E1', 'E2', 'E3'):
    for h in ('14', '16', '18'):
        for st in ('A', 'B'):
            key = f'{e}_{h}_{st}'
            u = L(f'u_{e}_{h}_{st}.npy')
            t = L(f'f_{e}_{h}_{st}_Tmrt.npy')
            esc_stats[key] = dict(UTCI=stats_field(u), MRT=stats_field(t),
                                  UTCI_categorias_m2=utci_cats(u))
u4 = L('u_E4_16_B.npy')
esc_stats['E4_16_B'] = dict(UTCI=stats_field(u4), UTCI_categorias_m2=utci_cats(u4))
R['escenarios'] = esc_stats

# deltas B-A por escenario a las 16h
deltas = {}
for e in ('E1', 'E2', 'E3'):
    dU = L(f'u_{e}_16_B.npy') - L(f'u_{e}_16_A.npy')
    dM = L(f'f_{e}_16_B_Tmrt.npy') - L(f'f_{e}_16_A_Tmrt.npy')
    deltas[e] = dict(dUTCI=stats_field(dU), dMRT=stats_field(dM),
                     m2_mejora_1K=round(float(((dU < -1) & W).sum() * CELLA), 0),
                     m2_mejora_3K=round(float(((dU < -3) & W).sum() * CELLA), 0),
                     m2_empeora_05K=round(float(((dU > 0.5) & W).sum() * CELLA), 0))
R['deltas_16h'] = deltas

# ---------------------------------------------------------------- cola positiva (empeora)
dU2 = L('u_E2_16_B.npy') - L('u_E2_16_A.npy')
dM2 = L('f_E2_16_B_Tmrt.npy') - L('f_E2_16_A_Tmrt.npy')
peor = (dU2 > 0.5) & W
att = {}
if peor.any():
    cp = cause[peor]
    for i, fam in enumerate(FAM_ORDER, start=1):
        n = int((cp == i).sum())
        if n:
            att[fam] = round(n * CELLA, 0)
    att['ABIERTO'] = round(int((cp == 0).sum()) * CELLA, 0)
# donde: centroides de los 3 mayores clusters (etiquetado sencillo)
from scipy import ndimage as ndi  # noqa: E402
lab, nl = ndi.label(peor)
clusters = []
if nl:
    sizes = ndi.sum(peor, lab, range(1, nl + 1))
    orden = np.argsort(sizes)[::-1][:5]
    cys, cxs = np.mgrid[0:ny, 0:nx]
    for k in orden:
        m = lab == (k + 1)
        if sizes[k] * CELLA < 4:
            continue
        cx = float(cxs[m].mean()) * 0.5 + (-112) + 0.25
        cy = float(cys[m].mean()) * 0.5 + (-45) + 0.25
        clusters.append(dict(x=round(cx, 1), y=round(cy, 1),
                             m2=round(float(sizes[k]) * CELLA, 0),
                             dUTCI_medio=round(float(dU2[m].mean()), 2),
                             dMRT_medio=round(float(dM2[m].mean()), 2)))
R['cola_positiva_E2_16'] = dict(m2=round(float(peor.sum() * CELLA), 0),
                                atribucion_m2=att, clusters=clusters,
                                nota='celdas pisables donde la propuesta EMPEORA el UTCI '
                                     '>0,5 K en E2/16h; atribucion por raster de causa')

# ================================================= CLI-01/02 · SOMBRA + RADIACION
shA, shB = L('shade_crit_A.npy'), L('shade_crit_B.npy')
radA, radB = L('rad_A.npy'), L('rad_B.npy')
winA, winB = L('radwin_A.npy'), L('radwin_B.npy')
sunA, sunB = L('sunhours_A.npy'), L('sunhours_B.npy')
R['sombra'] = dict(
    critica_A=stats_field(shA), critica_B=stats_field(shB),
    m2_sombra50_A=round(float(((shA >= 0.5) & W).sum() * CELLA), 0),
    m2_sombra50_B=round(float(((shB >= 0.5) & W).sum() * CELLA), 0),
    sunhours=dict(A=stats_field(sunA), B=stats_field(sunB)),
)
R['radiacion'] = dict(
    verano_kWh_m2=dict(A=stats_field(radA), B=stats_field(radB),
                       reduccion_pct=round(100 * (1 - float(radB[W].mean()) /
                                                  float(radA[W].mean())), 1)),
    invierno_kWh_m2_dia=dict(A=stats_field(winA), B=stats_field(winB),
                             perdida_pct=round(100 * (1 - float(winB[W].mean()) /
                                                      float(winA[W].mean())), 1),
                             nota='21-dic: coste invernal de la sombra estival. '
                                  'Se publica con el mismo peso que el beneficio (§43).'),
    invierno_m2_conservan50=round(float(((winB >= 0.5 * winA) & W & (winA > 0.1)).sum() * CELLA), 0),
)

# ================================================= CLI-08 · VIENTO (sensibilidad honesta)
# El modelo usa el MISMO viento de escenario para A y B (limitacion declarada).
# Sensibilidad: si la estructura redujera el viento peatonal un 25/50 %, cuanto UTCI-B se pierde.
from pythermalcomfort.models import utci as UTCI  # noqa: E402
ESC = J(os.path.join(RC, 'FASE_03B5B_CLIMA', '_clima', 'escenarios.json').replace(CLI + os.sep, ''), d='') if False else None
with open(os.path.join(RC, 'FASE_03B5B_CLIMA', '_clima', 'escenarios.json'), encoding='utf-8') as f:
    ESC = json.load(f)
e2 = ESC['escenarios']['E2']['horas']['16:00']
tm = L('f_E2_16_B_Tmrt.npy')[W]
sub = slice(None, None, 5)
sens_v = {}
for fac, tag in ((1.0, 'BASE'), (0.75, 'VIENTO -25%'), (0.5, 'VIENTO -50%')):
    va = max(e2['WS'] * fac, 0.5)
    res = UTCI(tdb=e2['Ta'], tr=tm[sub], v=va, rh=e2['RH'], limit_inputs=False)
    val = np.asarray(res.utci if hasattr(res, 'utci') else res, float)
    sens_v[tag] = round(float(np.nanmean(val)), 2)
R['sens_viento'] = dict(
    UTCI_B_E2_16=sens_v,
    nota='HIPOTESIS (C): el modelo no resuelve el abrigo del viento por la estructura; '
         'si el viento efectivo bajo el dosel cayera 25-50 %, el UTCI-B medio subiria '
         f"{round(sens_v['VIENTO -25%'] - sens_v['BASE'], 2)} / "
         f"{round(sens_v['VIENTO -50%'] - sens_v['BASE'], 2)} K. "
         'Requiere CFD o medicion en prototipo para resolverse.')

# ================================================= CLI-06 · SENSIBILIDAD k_veg (LAI +-30 %)
sys.path.insert(0, os.path.join(F9, '_reclima9'))
import clima_core as CC  # noqa: E402
g = CC.grid05()
voxB = L('voxB.npy', os.path.join(F9, '_reclima9', '_data'))
kvB = L('kvB.npy', os.path.join(F9, '_reclima9', '_data'))
# malla de puntos pisables (con el walk 0.5 propio del clima)
ys25, xs25 = np.where(W)
XS = (-112) + (np.arange(nx) + 0.5) * 0.5
YS = (-45) + (np.arange(ny) + 0.5) * 0.5
Xw = XS[xs25]; Yw = YS[ys25]
sens_k = {}
import datetime as dt  # noqa: E402
for h in (14, 16, 18):
    e_sun, a_sun = CC.sun_position(dt.datetime(2026, 7, 15, h, 30))
    v = CC.sun_vector(e_sun, a_sun)
    fila = {}
    for fac, tag in ((0.7, 'LOW'), (1.0, 'BASE'), (1.3, 'HIGH')):
        tau, _ = CC.transmittance(voxB, g, Xw, Yw, 0.05, v, kv=kvB * fac)
        fila[tag] = dict(tau_medio=round(float(tau.mean()), 3),
                         pct_sombra=round(100 * float((tau < 0.5).mean()), 1))
    sens_k['%02d:30' % h] = fila
R['sens_kveg'] = dict(
    posiciones='15-jul 14:30/16:30/18:30 (sol real PSA)',
    resultado=sens_k,
    nota='INFERIDO (B): LAI bibliografico +-30 % -> variacion de tau y de fraccion en sombra '
         'sobre suelo pisable. La sombra del proyecto es mayormente ESTRUCTURAL: la banda '
         'vegetal solo mueve la sombra unos puntos porcentuales.')

# ================================================= CLI-10 · CANOPY SECO (tau 0.12 -> 0.25)
tauB = L('f_E2_16_B_tau.npy')
Gb = L('f_E2_16_B_G.npy')
# celdas bajo dosel: cobertura del canopy (raster de auditoria) submuestreado
cob25 = None
try:
    # el audit_run guarda canopy en cause? no: usa la fraccion de dosel del clima (dtf/f_can)
    pass
except Exception:
    pass
# aproximacion: celdas con tau bajo pero no opacas (0.05 < tau < 0.35) = bajo canopy hoja
under = (tauB > 0.02) & (tauB < 0.40) & W
dtau_canopy = 0.25 - 0.12
dS = dtau_canopy * e2['Bn'] * math.sin(math.radians(35.0))   # elevacion tipica 16h julio
a_k, eps_p, SIG = 0.70, 0.97, 5.67e-8
Tm_under = L('f_E2_16_B_Tmrt.npy')[under]
Tm_k = Tm_under + 273.15
dMRT_dry = (a_k * dS) / (4 * eps_p * SIG * np.maximum(Tm_k, 1) ** 3)
R['canopy_seco'] = dict(
    m2_bajo_dosel=round(float(under.sum() * CELLA), 0),
    dMRT_medio_K=round(float(dMRT_dry.mean()), 2),
    dUTCI_aprox_K=round(float(dMRT_dry.mean()) * 0.35, 2),
    hipotesis='HIPOTESIS (C): camara de microalgas seca -> tau_canopy pasa de 0,12 a 0,25 '
              '(rango declarado en PARAMS). Linealizacion radiativa sobre las celdas bajo '
              'dosel; factor dUTCI/dMRT ~0,35 tipico a 33 C y viento 2 m/s.')

# ================================================= CLI-07 · SIN AGUA (fallo hidrico)
aire = J('aire.json')
refugio = J('refugio.json')
neb = J('neb_escenarios.json')
agua = J('agua.json')
mets = J('metricas.json')
R['sin_agua'] = dict(
    dTa_latente_perdida_K=aire['dTa_latente'],
    refugio_m2_sin_neb=refugio['clases']['REFUGIO EFECTIVO']['m2'],
    refugio_m2_con_neb=refugio['clases']['REFUGIO EFECTIVO']['m2_neb'],
    perdida_neb_m2=refugio['clases']['REFUGIO EFECTIVO']['m2_neb'] -
                   refugio['clases']['REFUGIO EFECTIVO']['m2'],
    agua_total_L_h=mets['agua_L_h'],
    nota='INFERIDO (B): sin agua se pierden el termino latente del aire (-0,43 K de los '
         '-1,09 K), la nebulizacion (-501 m2 de refugio) y la evapotranspiracion queda '
         'limitada al agua del sustrato (dias). La sombra estructural (el grueso del '
         'beneficio MRT) NO depende del agua.')

# ================================================= CSVs de programa
zonas = J('zonas.json')
with open(os.path.join(OUT, 'zonas_programa.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(zonas[0].keys()))
    w.writeheader(); w.writerows(zonas)
cinta = J('cinta.json')
n = cinta['n']
with open(os.path.join(OUT, 'cinta_estaciones.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    keys = [k for k, v in cinta.items() if isinstance(v, list) and len(v) == n]
    w.writerow(['i'] + keys)
    for i in range(n):
        w.writerow([i] + [cinta[k][i] for k in keys])
spots = J('spots.json')
with open(os.path.join(OUT, 'spots.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['tipo', 'id', 'x', 'y', 'm2', 'UTCI', 'sombra'])
    for tipo, lst in spots.items():
        for s in (lst if isinstance(lst, list) else []):
            w.writerow([tipo, s.get('id'), s.get('x'), s.get('y'), s.get('m2'),
                        s.get('UTCI'), s.get('sombra')])
with open(os.path.join(OUT, 'neb_escenarios.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(neb[0].keys()))
    w.writeheader(); w.writerows(neb)

R['zonas_resumen'] = [dict(zona=z['zona'], m2=z['m2'], dUTCI=z['dUTCI'],
                           refugio_pct=z.get('refugio_pct')) for z in zonas]
R['cinta_resumen'] = {k: (round(v, 2) if isinstance(v, float) else v)
                      for k, v in cinta.items() if not isinstance(v, list)}
R['metricas_canon'] = mets

with open(os.path.join(OUT, 'cli_stats.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)

flog.event(fase='FINAL', tipo_evento='motor_clima',
           objetivo='CLI-01..10: estadisticas, deltas, colas, invierno y sensibilidades sobre v006',
           resultado=('pisable %.0f m2; dUTCI E2/16 %.2f K; empeora>0.5K %.0f m2; sombra critica '
                      '%.1f%%->%.1f%%; invierno -%.1f%%; sens viento -50%%: %+0.2f K; '
                      'kveg LOW/HIGH sombra 16h %.1f/%.1f%%')
                     % (R['area_pisable_m2'], deltas['E2']['dUTCI']['media'],
                        R['cola_positiva_E2_16']['m2'],
                        100 * float(shA[W].mean()), 100 * float(shB[W].mean()),
                        R['radiacion']['invierno_kWh_m2_dia']['perdida_pct'],
                        sens_v['VIENTO -50%'] - sens_v['BASE'],
                        sens_k['16:30']['LOW']['pct_sombra'], sens_k['16:30']['HIGH']['pct_sombra']))
print(json.dumps({k: R[k] for k in ('area_pisable_m2', 'deltas_16h', 'cola_positiva_E2_16',
                                    'sens_viento', 'canopy_seco')}, ensure_ascii=False, indent=1)[:2200])
