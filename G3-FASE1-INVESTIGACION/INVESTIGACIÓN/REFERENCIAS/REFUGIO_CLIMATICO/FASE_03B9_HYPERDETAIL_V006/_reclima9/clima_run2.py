# -*- coding: utf-8 -*-
"""
FASE 03B.5B — fase 2: agua, vegetacion, sinergias, indice de refugio, zonas de programa,
cinta +6, hotspots y registro de incidencias.
Se apoya en los campos escritos por clima_run.py.
"""
import datetime as dt
import json
import math
import os
import sys
import time

import numpy as np
from scipy import ndimage as ndi

import clima_core as C
from clima_core import P, SIGMA, DATA, CL

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
T0 = time.time()


def log(*a):
    print('[%6.1fs]' % (time.time() - T0), *a, flush=True)


ESC = json.load(open(os.path.join(CL, 'escenarios.json'), encoding='utf-8'))
META = C.jload('escena_meta.json')
MIST = C.jload('mist.json')
mesh, M = C.load_scene()
g = C.grid05()
PLAZA25 = np.load(os.path.join(C.AUD, '_data', 'plaza.npy'))
WALK25 = np.load(os.path.join(C.AUD, '_data', 'walk.npy'))
PLAZA = PLAZA25[::2, ::2][:g.ny, :g.nx]
WALK = WALK25[::2, ::2][:g.ny, :g.nx]
II, JJ = np.where(PLAZA)
XS = g.x0 + (JJ + 0.5) * C.VS
YS = g.y0 + (II + 0.5) * C.VS
NP_ = len(XS)
CELLA = C.VS ** 2
WALKF = WALK[II, JJ]


def L(name):
    f = np.load(os.path.join(DATA, name))
    return f[II, JJ]


ISSUES = []


def issue(sev, cat, title, mag, causa, estr, x=None, y=None, metric=None, tipo=''):
    ISSUES.append(dict(id='CL-%03d' % (len(ISSUES) + 1), sev=sev, cat=cat, title=title,
                       magnitud=mag, causa=causa, estrategias=estr,
                       x=None if x is None else round(float(x), 1),
                       y=None if y is None else round(float(y), 1),
                       metric=metric, tipo=tipo))


# ================================================================ 7 · AGUA
log('7 · masas de agua: superficie, volumen, evaporacion y potencia latente')
esc = ESC['escenarios']['E2']['horas']['16:00']
Ta, RH, u10, Bn, Dh, IR = esc['Ta'], esc['RH'], esc['WS'], esc['Bn'], esc['Dh'], esc['IR']
uped = C.wind_at(u10)
elev = ESC and None
_e, _a = C.sun_position(dt.datetime(2019, 7, 21, 16 - C.TZ, 30))
sinel = math.sin(math.radians(_e))

waters = []


def add_water(kind, ident, area, depth, cx, cy, z, expuesto, nota=''):
    """expuesto: fraccion de radiacion directa que recibe la lamina (0-1). CALCULADO/MEDIDO."""
    G = Bn * sinel * expuesto + Dh * (0.95 if z > 3 else 0.6)
    Rn = (1 - P('alb_agua')) * G + P('eps_agua') * IR - P('eps_agua') * SIGMA * (Ta + 273.15) ** 4
    E = float(C.penman_open_water(max(Rn, 0.0), Ta, RH, uped))      # kg/m2/s
    lam = float(C.lambda_v(Ta))
    waters.append(dict(kind=kind, id=ident, area=round(area, 1), depth=depth,
                       vol=round(area * depth, 1), sv=round(1.0 / depth, 2),
                       cx=cx, cy=cy, z=z, expuesto=round(expuesto, 2),
                       Rn=round(Rn, 0), E_kg_m2_h=round(E * 3600, 3),
                       L_h=round(E * 3600 * area, 1),
                       kW=round(E * area * lam / 1000.0, 2), nota=nota))


sp = M['agua_clima']['splash']
add_water('SPLASH', sp['id'], math.pi * sp['rx'] * sp['ry'], 0.03, sp['cx'], sp['cy'], 0.03, 1.0,
          'lamina jugable de 3 cm; profundidad MEDIDA en el modelo (z=0.03)')
for p_ in M['agua_clima']['ground_ponds']:
    if p_['kind'] == 'circle':
        add_water('ESTANQUE', p_['id'], math.pi * p_['r'] ** 2, 0.48, p_['cx'], p_['cy'], 0.48, 0.85,
                  'bordillo 0.60 MEDIDO, lamina a 0.48 MEDIDA -> calado 0.48 HIPOTESIS')
    else:
        pts = np.array(p_['pts'], float)
        ar = 0.5 * abs(np.dot(pts[:, 0], np.roll(pts[:, 1], 1)) - np.dot(pts[:, 1], np.roll(pts[:, 0], 1)))
        add_water('ESTANQUE', p_['id'], ar, 0.45, float(pts[:, 0].mean()), float(pts[:, 1].mean()), 0.45, 0.85,
                  'lamina rinon a z=0.45 MEDIDA; calado HIPOTESIS')
for p_ in M['agua_clima']['pools']:
    add_water('BALSA ELEVADA', p_['id'], math.pi * p_['rx'] * p_['ry'], 0.30,
              p_['cx'], p_['cy'], p_['cota'], 1.0,
              'balsa sobre estructura a cota %.1f MEDIDA; calado 0.30 HIPOTESIS' % p_['cota'])
DISCS = M['paisaje']['discs']
a_film = sum(math.pi * (0.82 * d['r']) ** 2 for d in DISCS)
add_water('LAMINA MICROALGAS', 'DISCOS x%d' % len(DISCS), a_film, 0.03,
          0.0, 10.0, 6.0, 1.0,
          'D15: lamina de 2-5 cm en TODOS los discos, radio 0.82r MEDIDO en el bloque LEAF; '
          'espesor 0.03 HIPOTESIS (rango 0.02-0.05)')

tot_area = sum(w['area'] for w in waters)
tot_L = sum(w['L_h'] for w in waters)
tot_kW = sum(w['kW'] for w in waters)
suelo = [w for w in waters if w['z'] < 1.0]
elev_w = [w for w in waters if w['z'] >= 1.0]
log('   %d masas · superficie total %.0f m2 (%.1f %% del ambito) · %.0f L/h · %.1f kW latentes'
    % (len(waters), tot_area, 100 * tot_area / (NP_ * CELLA), tot_L, tot_kW))
log('   a nivel de suelo: %.0f m2 · %.0f L/h · %.1f kW   |   en altura: %.0f m2 · %.0f L/h · %.1f kW'
    % (sum(w['area'] for w in suelo), sum(w['L_h'] for w in suelo), sum(w['kW'] for w in suelo),
       sum(w['area'] for w in elev_w), sum(w['L_h'] for w in elev_w), sum(w['kW'] for w in elev_w)))
# cierre de masa: cuanta lamina se pierde al dia y si el deposito da para reponerla
HORAS_SOL = 12.0
for w in waters:
    w['mm_dia'] = round(w['E_kg_m2_h'] * HORAS_SOL, 1)
    w['pct_calado_dia'] = round(100 * (w['E_kg_m2_h'] * HORAS_SOL / 1000.0) / w['depth'], 1)
    w['m3_dia'] = round(w['L_h'] * HORAS_SOL / 1000.0, 2)
V_DEP = 6 * math.pi * 2.1 ** 2 * 1.2
tot_m3_dia = sum(w['m3_dia'] for w in waters)
log('   CIERRE DE MASA: %.1f m3/dia de evaporacion frente a %.1f m3 almacenados en los depositos '
    'de +10.50 -> autonomia %.2f dias sin reposicion de red'
    % (tot_m3_dia, V_DEP, V_DEP / max(tot_m3_dia, 1e-9)))
peor_w = max(waters, key=lambda w: w['pct_calado_dia'])
log('   lamina que antes se agota: %s %s -> %.1f mm/dia = %.0f %% de su calado cada dia'
    % (peor_w['kind'], peor_w['id'], peor_w['mm_dia'], peor_w['pct_calado_dia']))
C.jdump('agua.json', dict(rows=waters, m3_dia=round(tot_m3_dia, 2), V_dep_m3=round(V_DEP, 1),
                          autonomia_dias=round(V_DEP / max(tot_m3_dia, 1e-9), 2), total_area=tot_area, total_L_h=tot_L, total_kW=tot_kW,
                          suelo_kW=sum(w['kW'] for w in suelo), elev_kW=sum(w['kW'] for w in elev_w),
                          escenario='E2 16:00', Ta=Ta, RH=RH, uped=round(uped, 2)))

# ================================================================ 8 · VEGETACION
log('8 · vegetacion: sombra y evapotranspiracion')
# 03B.9: el arbolado ya es el asset ARBOLURB (VEGA_*); copa/LAI del BOTANICAL_MASTERPLAN
# (Celtis nuevo h9 d5 · Platanus OSM existente h12 d8, distinguidos por ancla)
CROWN = {'VEG2_ARBOL_A': (2.1, 5.2), 'VEG2_ARBOL_B': (1.9, 6.2), 'VEG2_ARBOL_EX': (2.7, 7.2),
         'ARBOLURB_NUEVO (Celtis)': (2.5, 9.0), 'ARBOLURB_EX (Platanus OSM)': (4.0, 12.0)}
LAI = {'VEG2_ARBOL_A': 2.8, 'VEG2_ARBOL_B': 2.8, 'VEG2_ARBOL_EX': 3.2,
       'ARBOLURB_NUEVO (Celtis)': 3.8, 'ARBOLURB_EX (Platanus OSM)': 4.5}
cnt = {}
for o in mesh:
    b8 = o['block']
    if b8.startswith('VEGA_ARBOLURB'):
        b8 = 'ARBOLURB_EX (Platanus OSM)' if C._es_arbol_existente(o) else 'ARBOLURB_NUEVO (Celtis)'
    if b8 in CROWN and o.get('anchor'):
        cnt.setdefault(b8, set()).add((round(o['anchor'][0], 2), round(o['anchor'][1], 2)))
veg_rows = []
tot_proj = 0.0
for b, pts in cnt.items():
    r, h = CROWN[b]
    n = len(pts)
    proj = n * math.pi * r ** 2
    tot_proj += proj
    Rn = (1 - P('alb_veg')) * (Bn * sinel + Dh) + P('eps_sup') * IR - P('eps_sup') * SIGMA * (Ta + 273.15) ** 4
    E0 = float(C.penman_open_water(max(Rn, 0), Ta, RH, uped))
    kc = 0.65                                  # coeficiente de cultivo arbolado urbano bien regado
    E = E0 * kc
    lam = float(C.lambda_v(Ta))
    k_sp = LAI[b] / 6.0                        # 03B.9: k_veg por especie (k = 0.5*LAI/3.0)
    veg_rows.append(dict(bloque=b, n=n, r_copa=r, h=h, LAI=LAI[b],
                         proy_m2=round(proj, 1), tau=round(math.exp(-k_sp * 2 * r), 3),
                         E_kg_m2_h=round(E * 3600, 3), L_h=round(E * 3600 * proj, 1),
                         kW=round(E * proj * lam / 1000, 2)))
otras = [o for o in mesh if (o['block'].startswith('VEG2_') or o['block'].startswith('VEGA_'))
         and not o['block'].startswith('VEGA_ARBOLURB') and o['block'] not in CROWN]
n_otras = len({(round(o['anchor'][0], 2), round(o['anchor'][1], 2), o['block']) for o in otras})
veg_kW = sum(v['kW'] for v in veg_rows)
veg_L = sum(v['L_h'] for v in veg_rows)
log('   arbolado: %d ejemplares · proyeccion de copa %.0f m2 (%.1f %% del ambito) · %.0f L/h · %.1f kW'
    % (sum(v['n'] for v in veg_rows), tot_proj, 100 * tot_proj / (NP_ * CELLA), veg_L, veg_kW))
log('   otras masas vegetales (huerto, tropicales, bajas, colgantes, trepadoras): %d instancias' % n_otras)
C.jdump('vegetacion.json', dict(rows=veg_rows, otras=n_otras, proy_m2=tot_proj, L_h=veg_L, kW=veg_kW))

# ================================================================ 9 · NEBULIZACION — 3 escenarios
log('9 · nebulizacion: escenarios bajo / nominal / maximo')
neb = np.array(M['agua_clima']['nebul'], float)
mist_rows = []
for lab, q, eta in (('BAJO', 3.0, 0.20), ('NOMINAL', 5.0, 0.35), ('MAXIMO', 8.0, 0.50)):
    for ename in ('E1', 'E2', 'E3'):
        v = ESC['escenarios'][ename]['horas']['16:00']
        Tw = float(C.wetbulb(v['Ta'], v['RH']))
        dep = v['Ta'] - Tw
        mflow = len(neb) * q / 3600.0                       # kg/s
        lam = float(C.lambda_v(v['Ta']))
        kW = mflow * lam / 1000.0
        dT = eta * dep
        # comprobacion de cierre: masa de agua necesaria para saturar el aire tratado
        up = C.wind_at(v['WS'])
        # volumen de aire tratado: seccion de la nube x velocidad
        A_cloud = len(neb) * math.pi * P('neb_radio') ** 2
        mair = 1.16 * up * (A_cloud / len(neb)) ** 0.5 * 2.5 * len(neb)   # kg/s (aprox)
        dT_bal = (mflow * lam) / (mair * 1005.0) if mair > 0 else 0
        mist_rows.append(dict(escenario=lab, clima=ename, q_L_h=q, eta=eta,
                              Ta=v['Ta'], RH=v['RH'], Twb=round(Tw, 2), depresion=round(dep, 2),
                              L_h=round(len(neb) * q, 1), kW=round(kW, 2),
                              dT_psicrometrico=round(dT, 2), dT_balance_masa=round(dT_bal, 2),
                              dT_aplicado=round(min(dT, dT_bal), 2)))
for r in mist_rows:
    if r['clima'] == 'E2':
        log('   %-8s q=%.1f L/h·boq  eta=%.2f  ->  %.0f L/h  %.1f kW  dT psicrom %.2f K  dT por balance de masa %.2f K'
            % (r['escenario'], r['q_L_h'], r['eta'], r['L_h'], r['kW'], r['dT_psicrometrico'], r['dT_balance_masa']))
C.jdump('neb_escenarios.json', mist_rows)

# ================================================================ 10 · EFECTO SOBRE LA TEMPERATURA DEL AIRE
log('10 · efecto a escala plaza sobre la temperatura del AIRE (no confundir con MRT)')
TsA = L('f_E2_16_A_Ts.npy'); TsB = L('f_E2_16_B_Ts.npy')
hc = float(C.h_conv(uped))
HA = hc * (TsA - Ta); HB = hc * (TsB - Ta)
dH = float(np.nansum(HA - HB) * CELLA)                      # W menos de calor sensible al aire
# flujo de aire que barre la plaza: seccion transversal x velocidad
Wc = 100.0; Hmix = 10.0
mdot = 1.16 * uped * Wc * Hmix
dTa_sensible = dH / (mdot * 1005.0)
kW_lat_suelo = sum(w['kW'] for w in suelo) + veg_kW
dTa_lat = kW_lat_suelo * 1000 / (mdot * 1005.0)
log('   calor sensible del pavimento: A %.0f kW · B %.0f kW · reduccion %.0f kW'
    % (np.nansum(HA) * CELLA / 1000, np.nansum(HB) * CELLA / 1000, dH / 1000))
log('   flujo de aire sobre la plaza %.0f kg/s (u=%.2f m/s, seccion %.0fx%.0f m)' % (mdot, uped, Wc, Hmix))
log('   -> descenso de temperatura del AIRE por menor calor sensible: %.2f K' % dTa_sensible)
log('   -> descenso adicional por calor latente de agua+vegetacion a nivel de suelo: %.2f K' % dTa_lat)
aire = dict(dH_kW=round(dH / 1000, 1), mdot=round(mdot, 0), dTa_sensible=round(dTa_sensible, 2),
            dTa_latente=round(dTa_lat, 2), dTa_total=round(dTa_sensible + dTa_lat, 2),
            hipotesis='Volumen de control: seccion transversal de %0.f m de ancho x %.0f m de altura de mezcla, '
                      'barrida a la velocidad peatonal media. ESTIMADO de orden de magnitud, no CFD.' % (Wc, Hmix))
C.jdump('aire.json', aire)

# ================================================================ 11 · INDICE DE REFUGIO
log('11 · indice de refugio climatico (formula documentada)')
UA = L('u_E2_16_A.npy'); UB = L('u_E2_16_B.npy'); U4 = L('u_E4_16_B.npy')
dU = UB - UA
dU4 = U4 - UA
MRTA = L('f_E2_16_A_Tmrt.npy'); MRTB = L('f_E2_16_B_Tmrt.npy')
SH = L('shade_crit_B.npy'); SHA = L('shade_crit_A.npy')


# Escala oficial de estres termico UTCI (Brode et al. 2012):
#   9-26 sin estres | 26-32 moderado | 32-38 fuerte | 38-46 muy fuerte | >46 extremo
UTCI_BINS = [26.0, 32.0, 38.0, 46.0]


def categoria(u):
    return np.digitize(u, UTCI_BINS)


def clasifica(ua, ub):
    """El salto de CATEGORIA de la escala UTCI es el criterio: no es un umbral inventado,
    es la clasificacion oficial de estres termico. Un punto es REFUGIO EFECTIVO si el
    proyecto lo saca de su banda de estres y ademas gana al menos 3 K."""
    du = ub - ua
    cl = np.zeros(len(du), np.uint8)
    cl[du <= -1.0] = 1
    cl[du <= -3.0] = 2
    baja = categoria(ub) < categoria(ua)
    cl[(du <= -3.0) & baja] = 3
    return cl


CLS = clasifica(UA, UB)
CLS4 = clasifica(UA, U4)
np.save(os.path.join(DATA, 'refugio.npy'), np.where(PLAZA, 0, np.nan))
f = np.full((g.ny, g.nx), np.nan); f[II, JJ] = CLS; np.save(os.path.join(DATA, 'refugio.npy'), f)
f4 = np.full((g.ny, g.nx), np.nan); f4[II, JJ] = CLS4; np.save(os.path.join(DATA, 'refugio_neb.npy'), f4)
lab = ['SIN MEJORA', 'MEJORA LEVE', 'MEJORA MODERADA', 'REFUGIO EFECTIVO']
ref = {}
for k in range(4):
    a = float((CLS == k).sum() * CELLA); a4 = float((CLS4 == k).sum() * CELLA)
    ref[lab[k]] = dict(m2=round(a, 0), pct=round(100 * a / (NP_ * CELLA), 1),
                       m2_neb=round(a4, 0), pct_neb=round(100 * a4 / (NP_ * CELLA), 1))
    log('   %-18s %6.0f m2 (%4.1f %%)   con nebulizacion: %6.0f m2 (%4.1f %%)'
        % (lab[k], a, 100 * a / (NP_ * CELLA), a4, 100 * a4 / (NP_ * CELLA)))
C.jdump('refugio.json', dict(clases=ref, dU_medio=float(dU.mean()), dU4_medio=float(dU4.mean()),
                             formula='Clasificacion por DELTA-UTCI en la condicion de diseno (E2 tarde calurosa, '
                                     '16:00 local, sol de 21 de julio). SIN MEJORA: dUTCI > -1 K. LEVE: -3 < dUTCI <= -1. '
                                     'MODERADA: dUTCI <= -3 K. REFUGIO EFECTIVO: dUTCI <= -3 K Y ADEMAS el punto BAJA DE '
                                     'CATEGORIA en la escala oficial de estres termico UTCI (26-32 moderado / 32-38 fuerte / '
                                     '38-46 muy fuerte). El criterio no es un umbral inventado: es el salto de banda de la '
                                     'clasificacion UTCI. No se suman efectos de sombra, agua y niebla por separado: UTCI ya '
                                     'integra Ta, MRT, viento y humedad en un unico indice.'))

# ================================================================ 12 · ZONAS DE PROGRAMA
log('12 · fichas climaticas por zona de programa')


def zona(nombre, msk):
    if msk.sum() == 0:
        return None
    return dict(zona=nombre, m2=round(float(msk.sum() * CELLA), 0),
                sombra_A=round(float(SHA[msk].mean() * 100), 1),
                sombra_B=round(float(SH[msk].mean() * 100), 1),
                MRT_A=round(float(MRTA[msk].mean()), 1), MRT_B=round(float(MRTB[msk].mean()), 1),
                dMRT=round(float((MRTB - MRTA)[msk].mean()), 1),
                UTCI_A=round(float(UA[msk].mean()), 1), UTCI_B=round(float(UB[msk].mean()), 1),
                dUTCI=round(float(dU[msk].mean()), 2),
                UTCI_neb=round(float(U4[msk].mean()), 1),
                agua=bool(np.any([math.hypot(XS[msk].mean() - w['cx'], YS[msk].mean() - w['cy']) < 15
                                  for w in waters if w['z'] < 1.5])),
                neb=bool(L('mist_cov.npy')[msk].mean() > 0.15),
                refugio_pct=round(float((CLS[msk] >= 2).mean() * 100), 1))


ZON = []


def near(px, py, r):
    return ((XS - px) ** 2 + (YS - py) ** 2) <= r * r


msk = np.zeros(NP_, bool)
for b in M['programa']['benches']:
    for q in b['pts']:
        msk |= near(q[0], q[1], 2.0)
ZON.append(zona('BANCOS (estancia)', msk))
msk = np.zeros(NP_, bool)
for gx in range(-62, -40, 4):
    for gy in range(0, 17, 5):
        msk |= near(gx, gy, 2.0)
ZON.append(zona('HUERTO C1', msk))
ZON.append(zona('SPLASH PAD', (((XS - sp['cx']) / sp['rx']) ** 2 + ((YS - sp['cy']) / sp['ry']) ** 2) <= 1.4))
dm = M['estructura_principal']['dome']
ZON.append(zona('CUPULA-PERGOLA', near(dm['cx'], dm['cy'], dm['r'])))
msk = np.zeros(NP_, bool)
for (vx, vy) in [(64, 18), (67, 14), (61, 12)]:
    msk |= near(vx, vy, 3.0)
ZON.append(zona('VIVEROS C3', msk))
msk = np.zeros(NP_, bool)
for d in DISCS:
    msk |= near(d['cx'], d['cy'], d['r'])
ZON.append(zona('BAJO DOSEL', msk))
msk = np.zeros(NP_, bool)
for p_ in M['agua_clima']['ground_ponds']:
    if p_['kind'] == 'circle':
        msk |= near(p_['cx'], p_['cy'], p_['r'] + 3)
ZON.append(zona('ESTANQUES', msk))
CORR = M['circulacion']['corridors']
msk = np.zeros(NP_, bool)
for c in CORR:
    pts = np.array(c['pts'], float)
    for i in range(len(pts) - 1):
        for t in np.linspace(0, 1, 40):
            p = pts[i] + (pts[i + 1] - pts[i]) * t
            msk |= near(p[0], p[1], 2.5)
ZON.append(zona('CORREDORES', msk))
msk = np.zeros(NP_, bool)
for (nx_, ny_) in neb:
    msk |= near(nx_, ny_, 3.0)
ZON.append(zona('BAJO NEBULIZACION', msk))
ZON = [z for z in ZON if z]
for z in ZON:
    log('   %-20s %5.0f m2 · sombra %4.1f→%4.1f %% · MRT %.1f→%.1f (%+.1f) · UTCI %.1f→%.1f (%+.2f)'
        % (z['zona'], z['m2'], z['sombra_A'], z['sombra_B'], z['MRT_A'], z['MRT_B'], z['dMRT'],
           z['UTCI_A'], z['UTCI_B'], z['dUTCI']))
C.jdump('zonas.json', ZON)

# ================================================================ 13 · CINTA +6
log('13 · recorrido elevado +6.00')
RIB = np.asarray(M['circulacion']['ribbon'], float)
step = max(1, len(RIB) // 160)
rx = RIB[::step, 0]; ry = RIB[::step, 1]
vB = np.load(os.path.join(DATA, 'voxB.npy'))
kvB = np.load(os.path.join(DATA, 'kvB.npy'))
_e2, _a2 = C.sun_position(dt.datetime(2019, 7, 21, 16 - C.TZ, 30))
sv = C.sun_vector(_e2, _a2)
tau_r, _ = C.transmittance(vB, g, rx, ry, 6.0 + P('h_mrt'), sv, kv=kvB)
svf_r = np.zeros(len(rx)); dtf_r = np.zeros(len(rx))
SKD, SKW = C.sky_dirs(8)
for k in range(len(SKD)):
    if SKD[k][2] <= 0.03:
        continue
    t_, f_ = C.transmittance(vB, g, rx, ry, 6.0 + P('h_mrt'), SKD[k], kv=kvB)
    svf_r += SKW[k] * f_; dtf_r += SKW[k] * t_
sin2 = math.sin(math.radians(_e2))
G_deck = Bn * sin2 * tau_r + Dh * dtf_r
Ts_deck = C.surface_temp((1 - 0.35) * G_deck, svf_r * IR + (1 - svf_r) * P('eps_sup') * SIGMA * (Ta + 273.15 + 6) ** 4,
                         Ta, C.wind_at(u10, 6.0 + P('h_mrt')))
Tmrt_r = C.mrt(Bn, tau_r, _e2, Dh * dtf_r, 0.35 * G_deck,
               svf_r * IR + (1 - svf_r) * P('eps_sup') * SIGMA * (Ta + 273.15 + 8) ** 4,
               P('eps_sup') * SIGMA * (Ts_deck + 273.15) ** 4)
u_deck = C.wind_at(u10, 6.0 + P('h_mrt'))
from pythermalcomfort.models import utci as UTCI
r_ = UTCI(tdb=Ta, tr=Tmrt_r, v=max(u10, 0.5), rh=RH, limit_inputs=False)
U_deck = np.array(r_.utci if hasattr(r_, 'utci') else r_, float)
log('   cinta: sombra (tau<0.5) %.0f %% del desarrollo · MRT medio %.1f C (plaza B %.1f) · UTCI medio %.1f (plaza B %.1f)'
    % (100 * (tau_r < 0.5).mean(), Tmrt_r.mean(), MRTB.mean(), U_deck.mean(), UB.mean()))
log('   viento a +7.10 m: %.2f m/s frente a %.2f m/s a nivel de suelo' % (u_deck, uped))
C.jdump('cinta.json', dict(n=len(rx), pct_sombra=float(100 * (tau_r < 0.5).mean()),
                           MRT=float(Tmrt_r.mean()), MRT_max=float(Tmrt_r.max()),
                           UTCI=float(U_deck.mean()), UTCI_max=float(U_deck.max()),
                           u_deck=float(u_deck), u_suelo=float(uped),
                           svf=float(svf_r.mean()), tau=float(tau_r.mean()),
                           x=rx.tolist(), y=ry.tolist(), utci=U_deck.tolist(), mrt=Tmrt_r.tolist()))

# ================================================================ 14 · HOTSPOTS / COOLSPOTS
log('14 · hotspots y coolspots')
fU = np.full((g.ny, g.nx), np.nan); fU[II, JJ] = UB
fW = np.zeros((g.ny, g.nx), bool); fW[II, JJ] = WALKF
hot = np.zeros((g.ny, g.nx), bool); hot[II, JJ] = (UB >= 38.0) & WALKF        # estres termico muy fuerte
cool = np.zeros((g.ny, g.nx), bool); cool[II, JJ] = (CLS == 3) & WALKF
HS, CS = [], []
for msk_, out, pref, sev in ((hot, HS, 'CL-HOT', 'RED'), (cool, CS, 'CL-COOL', 'GREEN')):
    lb, nl = ndi.label(msk_)
    if not nl:
        continue
    for k, sl in enumerate(ndi.find_objects(lb), start=1):
        m_ = lb[sl] == k
        a = m_.sum() * CELLA
        if a < 25:
            continue
        ys, xs = np.where(m_)
        cy_, cx_ = sl[0].start + ys.mean(), sl[1].start + xs.mean()
        x, y = g.xy(int(cy_), int(cx_))
        sub = np.full((g.ny, g.nx), False); sub[sl] = m_
        out.append(dict(id='%s-%03d' % (pref, len(out) + 1), x=round(float(x), 1), y=round(float(y), 1),
                        m2=round(float(a), 0),
                        UTCI=round(float(np.nanmean(fU[sub])), 1),
                        sombra=round(float(np.nanmean(np.where(sub[II, JJ], SH, np.nan))), 2) if sub[II, JJ].any() else 0))
HS.sort(key=lambda q: -q['m2']); CS.sort(key=lambda q: -q['m2'])
log('   hotspots (UTCI>=38 en suelo pisable): %d zonas, %.0f m2 en total'
    % (len(HS), sum(h['m2'] for h in HS)))
log('   coolspots (refugio efectivo): %d zonas, %.0f m2 en total' % (len(CS), sum(c['m2'] for c in CS)))
C.jdump('spots.json', dict(hot=HS[:40], cool=CS[:40],
                           hot_m2=sum(h['m2'] for h in HS), cool_m2=sum(c['m2'] for c in CS)))

# ================================================================ 15 · METRICAS + INCIDENCIAS
log('15 · metricas de resultado')
RA = L('rad_A.npy'); RB = L('rad_B.npy')
SUNA = L('sunhours_A.npy'); SUNB = L('sunhours_B.npy')
WA = L('radwin_A.npy'); WB = L('radwin_B.npy')
mets = dict(
    area_ambito=round(NP_ * CELLA, 0), area_pisable=round(float(WALKF.sum() * CELLA), 0),
    sombra_crit_A=round(float(SHA.mean() * 100), 1), sombra_crit_B=round(float(SH.mean() * 100), 1),
    sombra_crit_A_pisable=round(float(SHA[WALKF].mean() * 100), 1),
    sombra_crit_B_pisable=round(float(SH[WALKF].mean() * 100), 1),
    m2_sombra_extra=round(float((SH - SHA).sum() * CELLA), 0),
    rad_A=round(float(RA.mean()), 1), rad_B=round(float(RB.mean()), 1),
    rad_red_pct=round(float(100 * (1 - RB.mean() / RA.mean())), 1),
    rad_red_max_pct=round(float(100 * (1 - (RB / np.maximum(RA, 1e-6)).min())), 1),
    sunh_A=round(float(SUNA.mean()), 0), sunh_B=round(float(SUNB.mean()), 0),
    MRT_A=round(float(MRTA.mean()), 1), MRT_B=round(float(MRTB.mean()), 1),
    dMRT=round(float((MRTB - MRTA).mean()), 2),
    dMRT_refugio=round(float((MRTB - MRTA)[CLS >= 2].mean()), 2) if (CLS >= 2).any() else None,
    dMRT_max=round(float((MRTB - MRTA).min()), 2),
    UTCI_A=round(float(UA.mean()), 1), UTCI_B=round(float(UB.mean()), 1),
    dUTCI=round(float(dU.mean()), 2), dUTCI_neb=round(float(dU4.mean()), 2),
    dUTCI_max=round(float(dU.min()), 2),
    m2_refugio=ref['REFUGIO EFECTIVO']['m2'], m2_refugio_neb=ref['REFUGIO EFECTIVO']['m2_neb'],
    m2_mejora=round(sum(ref[k]['m2'] for k in lab[1:]), 0),
    pct_beneficiada=round(100 * sum(ref[k]['m2'] for k in lab[1:]) / (NP_ * CELLA), 1),
    agua_L_h=round(tot_L, 0), agua_kW=round(tot_kW, 1), agua_suelo_kW=round(sum(w['kW'] for w in suelo), 1),
    veg_L_h=round(veg_L, 0), veg_kW=round(veg_kW, 1),
    neb_L_h=round(42 * 5.0, 0), neb_kW=round([r for r in mist_rows if r['escenario'] == 'NOMINAL' and r['clima'] == 'E2'][0]['kW'], 1),
    dTa_aire=aire['dTa_total'],
    win_A=round(float(WA.mean()), 2), win_B=round(float(WB.mean()), 2),
    win_perdida_pct=round(float(100 * (1 - WB.mean() / max(WA.mean(), 1e-9))), 1),
    hot_m2=sum(h['m2'] for h in HS), cool_m2=sum(c['m2'] for c in CS),
)
for k, v in mets.items():
    log('   %-24s %s' % (k, v))
C.jdump('metricas.json', mets)

# --- incidencias
if mets['win_perdida_pct'] > 40:
    issue('YELLOW', 'INVIERNO', 'El dosel bloquea el %.0f %% de la radiacion de invierno' % mets['win_perdida_pct'],
          '21 dic: %.2f -> %.2f kWh/m2·dia sobre el suelo del ambito' % (mets['win_A'], mets['win_B']),
          'El dosel es fijo: la lamina de microalgas y la membrana no son estacionales, a diferencia de un arbolado caduco.',
          'Evaluar desmontaje estacional de una fraccion de discos · sustituir membrana por caduca en los discos sobre '
          'las zonas de estancia de invierno · aceptar y documentar la perdida.', metric=mets['win_perdida_pct'])
if mets['hot_m2'] > 200:
    h0 = HS[0]
    issue('RED', 'HOTSPOT', 'Quedan %.0f m2 de suelo pisable en estres termico muy fuerte' % mets['hot_m2'],
          '%d zonas con UTCI>=38 C en E2 16:00; la mayor de %.0f m2 en (%.0f, %.0f) con UTCI %.1f'
          % (len(HS), h0['m2'], h0['x'], h0['y'], h0['UTCI']),
          'Zonas sin dosel, sin agua y sin nebulizacion: el proyecto no llega a ellas.',
          'No corregir todavia; identificadas para decidir si se amplia dosel, se anaden puntos de niebla o se '
          'aceptan como zonas de paso.', x=h0['x'], y=h0['y'], metric=mets['hot_m2'])
if sum(w['kW'] for w in elev_w) > sum(w['kW'] for w in suelo):
    issue('YELLOW', 'AGUA', 'La mayor parte de la potencia evaporativa del agua esta en altura, no sobre el peaton',
          'Balsas + laminas de microalgas: %.1f kW en altura frente a %.1f kW a nivel de suelo (%.0f %% del total)'
          % (sum(w['kW'] for w in elev_w), sum(w['kW'] for w in suelo),
             100 * sum(w['kW'] for w in elev_w) / max(tot_kW, 1e-9)),
          'La lamina de microalgas de los 67 discos suma %.0f m2, muy por encima de los %.0f m2 de agua a nivel de suelo.'
          % (a_film, sum(w['area'] for w in suelo)),
          'El agua en altura SI aporta: enfria la cara inferior del dosel y por tanto la carga radiante sobre el peaton. '
          'Pero no debe contabilizarse como enfriamiento del aire a nivel de calle.', metric=sum(w['kW'] for w in elev_w))
cin = C.jload('cinta.json')
if cin['UTCI'] > mets['UTCI_B']:
    issue('RED', 'CINTA', 'El recorrido elevado es MAS calido que la plaza que sobrevuela',
          'Cinta +6.00: solo %.0f %% del desarrollo en sombra - MRT %.1f C - UTCI %.1f, frente a la plaza en '
          'estado B: MRT %.1f C - UTCI %.1f. El viento ayuda (%.2f frente a %.2f m/s) pero no compensa.'
          % (cin['pct_sombra'], cin['MRT'], cin['UTCI'], mets['MRT_B'], mets['UTCI_B'],
             cin['u_deck'], cin['u_suelo']),
          'La cinta va a +6.00, por ENCIMA de la capa baja del dosel (discos a 4.2-5.6) y solo por debajo de la '
          'capa alta: en la mayor parte de su desarrollo esta al descubierto.',
          'No corregir todavia. A valorar: discos propios sobre la cinta, bajar tramos bajo la capa media, o '
          'aceptarla como recorrido de manana y tarde y no de mediodia.', metric=cin['UTCI'])
zc = [z for z in ZON if z['zona'] == 'CORREDORES']
zd = [z for z in ZON if z['zona'] == 'BAJO DOSEL']
if zc and zc[0]['dUTCI'] > -1.5:
    issue('YELLOW', 'RECORRIDOS', 'Los corredores peatonales apenas mejoran',
          'Los 5 corredores declarados suman %.0f m2 y solo pasan de %.1f a %.1f %% de sombra critica; '
          'dUTCI %.2f K frente a %.2f K bajo dosel.'
          % (zc[0]['m2'], zc[0]['sombra_A'], zc[0]['sombra_B'], zc[0]['dUTCI'], zd[0]['dUTCI']),
          'La regla near_corr del generador mantiene los corredores LIBRES de dosel y mastiles: la misma decision '
          'que garantiza la transitabilidad los deja al sol.',
          'Decidir si el refugio debe cubrir tambien el movimiento o solo la estancia.', metric=zc[0]['dUTCI'])
if peor_w['pct_calado_dia'] > 25:
    issue('YELLOW', 'AGUA', 'Las laminas finas se evaporan mas rapido de lo que su calado admite',
          '%s %s: %.1f mm/dia = %.0f %% de su calado cada dia de verano. Evaporacion total %.1f m3/dia frente a '
          '%.1f m3 en los depositos de +10.50: %.2f dias de autonomia sin reposicion.'
          % (peor_w['kind'], peor_w['id'], peor_w['mm_dia'], peor_w['pct_calado_dia'], tot_m3_dia, V_DEP,
             V_DEP / max(tot_m3_dia, 1e-9)),
          'Mucha superficie de agua con muy poco calado: la lamina de microalgas suma %.0f m2 a 3 cm.' % a_film,
          'Dimensionar reposicion continua o recirculacion. Es un requisito de instalacion, no un defecto '
          'geometrico, pero condiciona el funcionamiento climatico real del dosel.',
          metric=peor_w['pct_calado_dia'])
if mets['cool_m2'] < 500:
    issue('YELLOW', 'SINTESIS', 'Muy pocos puntos alcanzan la categoria de refugio efectivo en tarde calurosa',
          'Solo %.0f m2 (%.1f %% del ambito) bajan de categoria UTCI en E2/16:00 sin nebulizacion; con '
          'nebulizacion activa pasan a %.0f m2.'
          % (mets['cool_m2'], 100 * mets['cool_m2'] / mets['area_ambito'], mets['m2_refugio_neb']),
          'Con Ta = 34.7 C el UTCI esta dominado por la temperatura del aire: la sombra baja la MRT 10.8 K de '
          'media pero eso solo mueve el UTCI 2.6 K.',
          'No es corregible con geometria: es el limite fisico de una estrategia basada en sombra. La palanca '
          'con margen es la evaporativa.', metric=mets['cool_m2'])
C.jdump('issues.json', ISSUES)
log('incidencias generadas: %d' % len(ISSUES))
log('OK fase 2/2')
