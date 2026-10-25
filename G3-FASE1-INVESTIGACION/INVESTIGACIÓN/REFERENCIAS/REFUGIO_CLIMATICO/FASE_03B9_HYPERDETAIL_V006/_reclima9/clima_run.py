# -*- coding: utf-8 -*-
"""
FASE 03B.5B — motor de auditoria climatica.
ESTADO A (Sol actual: edificios + arbolado existente) vs ESTADO B (propuesta).
Misma geometria urbana, misma orientacion, mismo clima, misma rejilla. La intervencion
es la unica variable.
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
TMY = C.__dict__  # placeholder


# ---------------------------------------------------------------- TMY horario
def read_tmy():
    p = os.path.join(CL, 'PVGIS_TMY_40.4169_-3.7035.csv')
    lines = open(p, encoding='utf-8').read().splitlines()
    i0 = next(i for i, l in enumerate(lines) if l.startswith('time(UTC)'))
    hdr = lines[i0].split(',')
    rows = []
    for l in lines[i0 + 1:]:
        if not l or not l[0].isdigit():
            break
        d = dict(zip(hdr, l.split(',')))
        t = dt.datetime.strptime(d['time(UTC)'], '%Y%m%d:%H%M')
        rows.append(dict(t=t, m=t.month, d=t.day, h=t.hour, Ta=float(d['T2m']), RH=float(d['RH']),
                         Gh=float(d['G(h)']), Bn=float(d['Gb(n)']), Dh=float(d['Gd(h)']),
                         IR=float(d['IR(h)']), WS=float(d['WS10m']), WD=float(d['WD10m'])))
    return rows


HOURS = read_tmy()
log('TMY cargado: %d horas' % len(HOURS))

# ---------------------------------------------------------------- escena / rejilla
mesh, M = C.load_scene()
g = C.grid05()
VOX = {'A': np.load(os.path.join(DATA, 'voxA.npy')), 'B': np.load(os.path.join(DATA, 'voxB.npy'))}
KV = {'A': np.load(os.path.join(DATA, 'kvA.npy')), 'B': np.load(os.path.join(DATA, 'kvB.npy'))}
log('escena %d mallas · %d triangulos · rejilla %dx%d a %.2f m'
    % (len(mesh), sum(len(o['F']) for o in mesh), g.nx, g.ny, C.VS))

# --- ambito: el MISMO de 03B.5, remuestreado a 0.5 m
PLAZA25 = np.load(os.path.join(C.AUD, '_data', 'plaza.npy'))
WALK25 = np.load(os.path.join(C.AUD, '_data', 'walk.npy'))
PLAZA = PLAZA25[::2, ::2][:g.ny, :g.nx]
WALK = WALK25[::2, ::2][:g.ny, :g.nx]
if PLAZA.shape != (g.ny, g.nx):
    z = np.zeros((g.ny, g.nx), bool); z[:PLAZA.shape[0], :PLAZA.shape[1]] = PLAZA; PLAZA = z
    z = np.zeros((g.ny, g.nx), bool); z[:WALK.shape[0], :WALK.shape[1]] = WALK; WALK = z
CELLA = C.VS ** 2
II, JJ = np.where(PLAZA)
XS = g.x0 + (JJ + 0.5) * C.VS
YS = g.y0 + (II + 0.5) * C.VS
NP_ = len(XS)
log('ambito %d celdas = %.0f m2 (03B.5: 11.014 m2) · suelo pisable %.0f m2'
    % (NP_, NP_ * CELLA, WALK.sum() * CELLA))


def tofield(vals, fill=np.nan):
    f = np.full((g.ny, g.nx), fill, float)
    f[II, JJ] = vals
    return f


# ================================================================ 1 · SVF y difusa
log('1 · factor de vision de cielo y transmision difusa (145 direcciones)')
SKD, SKW = C.sky_dirs(8)
log('   %d direcciones de cielo, suma de pesos %.4f' % (len(SKD), SKW.sum()))
SKY = {}
for est in ('A', 'B'):
    for hname, hz in (('grd', 0.05), ('ped', P('h_mrt'))):
        dtf = np.zeros(NP_)
        fr = {0: np.zeros(NP_), 1: np.zeros(NP_), 2: np.zeros(NP_), 3: np.zeros(NP_),
              4: np.zeros(NP_), 5: np.zeros(NP_)}
        for k in range(len(SKD)):
            if SKD[k][2] <= 0.03:
                continue
            tau, free, fc = C.transmittance(VOX[est], g, XS, YS, hz, SKD[k], want_first=True, kv=KV[est])
            dtf += SKW[k] * tau             # transmision difusa de onda corta
            for cl in fr:
                fr[cl] += SKW[k] * (fc == cl)
        tot = sum(fr.values())
        for cl in fr:
            fr[cl] /= np.maximum(tot, 1e-9)
        # para onda larga el cielo es SOLO lo que se ve sin nada delante
        svf = fr[0]
        f_can = fr[2] + fr[3] + fr[5]       # dosel, cupula y redes: emiten como superficie
        SKY[(est, hname)] = dict(svf=svf, dtf=dtf, f_can=f_can, f_op=fr[1], f_veg=fr[4])
        log('   estado %s @%s: SVF(onda larga) %.3f · DTF(difusa) %.3f · frac dosel %.3f · opaco %.3f · vegetal %.3f'
            % (est, hname, svf.mean(), dtf.mean(), f_can.mean(), fr[1].mean(), fr[4].mean()))
np.save(os.path.join(DATA, 'svf_B_ped.npy'), tofield(SKY[('B', 'ped')]['svf']))
np.save(os.path.join(DATA, 'svf_A_ped.npy'), tofield(SKY[('A', 'ped')]['svf']))

# ================================================================ 2 · SOL Y SOMBRA
log('2 · horas de sol y sombra')


def crit(r):
    return (r['m'] == 6 and r['d'] >= 15) or r['m'] in (7, 8) or (r['m'] == 9 and r['d'] <= 15)


CRIT = [r for r in HOURS if crit(r)]
DAYS = sorted({(r['m'], r['d']) for r in CRIT})
SAMPLE = DAYS[::3]
log('   ventana critica %d dias · geometria solar muestreada en %d dias (cada 3)' % (len(DAYS), len(SAMPLE)))


def nearest_sample(md):
    return min(SAMPLE, key=lambda s: abs((s[0] * 31 + s[1]) - (md[0] * 31 + md[1])))


ASSIGN = {d: nearest_sample(d) for d in DAYS}
YEAR = 2019   # ano civil de referencia para la geometria solar (solo posicion del sol)

# --- cache de transmitancia directa por (dia muestra, hora) y estado
def sun_at(m, d, h):
    return C.sun_position(dt.datetime(YEAR, m, d, h, 30))


TAUC = {'A': {}, 'B': {}}
SUNPOS = {}
nc = 0
for (m, d) in SAMPLE:
    for h in range(3, 21):
        e, a = sun_at(m, d, h)
        if e <= 1.0:
            continue
        SUNPOS[(m, d, h)] = (e, a)
        v = C.sun_vector(e, a)
        for est in ('A', 'B'):
            tau, _ = C.transmittance(VOX[est], g, XS, YS, 0.05, v, kv=KV[est])
            TAUC[est][(m, d, h)] = tau.astype(np.float32)
        nc += 1
    if len(TAUC['B']) % 90 < 18:
        log('   ... %d posiciones solares calculadas' % nc)
log('   %d posiciones solares × 2 estados' % nc)

# --- horas de sol acumuladas en la ventana critica (umbral tau>=0.5 = "al sol")
SUNH = {'A': np.zeros(NP_), 'B': np.zeros(NP_)}
SUNH_CRIT = {'A': np.zeros(NP_), 'B': np.zeros(NP_)}   # 12-18 local = 10-16 UTC
NDAY = {}
for d in DAYS:
    s = ASSIGN[d]
    NDAY[s] = NDAY.get(s, 0) + 1
for est in ('A', 'B'):
    for (m, dd) in SAMPLE:
        w = NDAY[(m, dd)]
        for h in range(3, 21):
            k = (m, dd, h)
            if k not in TAUC[est]:
                continue
            sun = (TAUC[est][k] >= 0.5).astype(np.float32)
            SUNH[est] += w * sun
            if 10 <= h <= 15:
                SUNH_CRIT[est] += w * sun
for est in ('A', 'B'):
    log('   estado %s: horas de sol medias %.0f h en la ventana (%.1f h/dia) · en 12-18 local %.0f h'
        % (est, SUNH[est].mean(), SUNH[est].mean() / len(DAYS), SUNH_CRIT[est].mean()))

NCRIT_H = 6 * len(DAYS)
SHADE_CRIT = {e: 1.0 - SUNH_CRIT[e] / NCRIT_H for e in ('A', 'B')}
for e in ('A', 'B'):
    np.save(os.path.join(DATA, 'shade_crit_%s.npy' % e), tofield(SHADE_CRIT[e]))
    np.save(os.path.join(DATA, 'sunhours_%s.npy' % e), tofield(SUNH[e]))

# ================================================================ 3 · RADIACION ACUMULADA
log('3 · radiacion solar incidente acumulada sobre el suelo')
RAD = {'A': np.zeros(NP_), 'B': np.zeros(NP_)}       # Wh/m2 acumulados en la ventana
BYDAYH = {}
for r in CRIT:
    BYDAYH.setdefault(((r['m'], r['d']), r['h']), []).append(r)
for est in ('A', 'B'):
    dtf = SKY[(est, 'grd')]['dtf']
    for d in DAYS:
        s = ASSIGN[d]
        for h in range(3, 21):
            rr = BYDAYH.get((d, h))
            if not rr:
                continue
            r = rr[0]
            k = (s[0], s[1], h)
            if k not in TAUC[est]:
                continue
            e, a = SUNPOS[k]
            sinel = math.sin(math.radians(e))
            RAD[est] += r['Bn'] * sinel * TAUC[est][k] + r['Dh'] * dtf
for e in ('A', 'B'):
    np.save(os.path.join(DATA, 'rad_%s.npy' % e), tofield(RAD[e] / 1000.0))
DRAD = RAD['B'] - RAD['A']
np.save(os.path.join(DATA, 'rad_delta.npy'), tofield(DRAD / 1000.0))
log('   estado A %.0f kWh/m2 · estado B %.0f kWh/m2 · reduccion media %.1f %% (%.0f kWh/m2)'
    % (RAD['A'].mean() / 1000, RAD['B'].mean() / 1000,
       100 * (1 - RAD['B'].mean() / RAD['A'].mean()), (RAD['A'].mean() - RAD['B'].mean()) / 1000))

# --- radiacion de invierno (21 dic) para comprobar el efecto estacional
log('   invierno: 21 de diciembre')
WRAD = {'A': np.zeros(NP_), 'B': np.zeros(NP_)}
dec = [r for r in HOURS if r['m'] == 12 and r['d'] == 21]
for est in ('A', 'B'):
    dtf = SKY[(est, 'grd')]['dtf']
    for r in dec:
        e, a = C.sun_position(dt.datetime(YEAR, 12, 21, r['h'], 30))
        if e <= 1:
            continue
        tau, _ = C.transmittance(VOX[est], g, XS, YS, 0.05, C.sun_vector(e, a), kv=KV[est])
        WRAD[est] += r['Bn'] * math.sin(math.radians(e)) * tau + r['Dh'] * dtf
for e in ('A', 'B'):
    np.save(os.path.join(DATA, 'radwin_%s.npy' % e), tofield(WRAD[e] / 1000.0))
log('   21-dic: A %.2f kWh/m2·dia · B %.2f · perdida %.0f %%'
    % (WRAD['A'].mean() / 1000, WRAD['B'].mean() / 1000, 100 * (1 - WRAD['B'].mean() / max(WRAD['A'].mean(), 1e-9))))

# ================================================================ 4 · DOSEL disco a disco
log('4 · rendimiento de cada disco de dosel')
DISCS = M['paisaje']['discs']
COVER = np.zeros((len(DISCS), NP_), np.uint16)     # horas de sombra proyectada por disco
for (m, dd) in SAMPLE:
    w = NDAY[(m, dd)]
    for h in range(10, 16):                        # 12-18 local
        k = (m, dd, h)
        if k not in SUNPOS:
            continue
        e, a = SUNPOS[k]
        te = math.tan(math.radians(e))
        av = math.radians(a)
        for i, D in enumerate(DISCS):
            cota = min(max(D.get('cota', 6.0), 4.2), 8.5)
            sx = D['cx'] - (cota / te) * math.sin(av)
            sy = D['cy'] - (cota / te) * math.cos(av)
            r = D['r']
            sel = ((XS - sx) ** 2 + (YS - sy) ** 2) <= r * r
            COVER[i][sel] += w
TOT = COVER.sum(0)
disc_rows = []
for i, D in enumerate(DISCS):
    cota = min(max(D.get('cota', 6.0), 4.2), 8.5)
    area = math.pi * D['r'] ** 2
    cov = COVER[i]
    hsum = cov.sum() * CELLA                       # m2·h de sombra proyectada dentro del ambito
    uniq = ((cov > 0) & (TOT == cov)).sum() * CELLA
    onwalk = (cov > 0) & WALK[II, JJ]
    disc_rows.append(dict(id=i + 1, cx=D['cx'], cy=D['cy'], r=D['r'], cota=cota, area=area,
                          m2h=float(hsum), m2_util=float(uniq),
                          m2_suelo=float((cov > 0).sum() * CELLA),
                          m2_pisable=float(onwalk.sum() * CELLA),
                          h_medias=float(cov[cov > 0].mean()) if (cov > 0).any() else 0.0))
disc_rows.sort(key=lambda q: -q['m2h'])
ef = np.array([q['m2h'] / q['area'] for q in disc_rows])
log('   67 discos · sombra proyectada total %.0f m2·h · eficiencia (m2h/m2 disco) mediana %.0f · min %.0f · max %.0f'
    % (sum(q['m2h'] for q in disc_rows), np.median(ef), ef.min(), ef.max()))
C.jdump('discos.json', disc_rows)

# ================================================================ 5 · BALANCE DE SUPERFICIE + MRT + UTCI
log('5 · balance de superficie, MRT y UTCI por escenario')
from pythermalcomfort.models import utci as UTCI  # noqa: E402

# clasificacion de superficie del suelo (MEDIDO sobre la geometria)
CAUSE25 = np.load(os.path.join(C.AUD, '_data', 'cause.npy'))
CA = CAUSE25[::2, ::2][:g.ny, :g.nx]
FAM_ORDER = ['CONTEXT', 'STRUCTURE', 'RIBBON', 'PODS', 'CANOPY', 'PLANTER', 'VEGETATION', 'FURNITURE', 'WATER']
sur = np.zeros(NP_, np.uint8)          # 0 granito · 1 agua · 2 vegetacion
lab = CA[II, JJ]
sur[lab == FAM_ORDER.index('WATER') + 1] = 1
sur[lab == FAM_ORDER.index('VEGETATION') + 1] = 2
sur[lab == FAM_ORDER.index('PLANTER') + 1] = 2
# zona humeda: splash + entorno 3 m de estanques
sp = M['agua_clima']['splash']
wet = (((XS - sp['cx']) / sp['rx']) ** 2 + ((YS - sp['cy']) / sp['ry']) ** 2) <= 1.0
for p_ in M['agua_clima']['ground_ponds']:
    if p_['kind'] == 'circle':
        wet |= ((XS - p_['cx']) ** 2 + (YS - p_['cy']) ** 2) <= (p_['r'] + 2.0) ** 2
log('   superficie: granito %d · agua %d · vegetal %d · humeda(splash/estanque) %d celdas'
    % ((sur == 0).sum(), (sur == 1).sum(), (sur == 2).sum(), wet.sum()))

NEB = np.array(M['agua_clima']['nebul'], float)


def mist_field(u_ped, wd_deg):
    """Cobertura de nebulizacion con deriva por viento. Devuelve fraccion 0-1 por celda.
    La nube se modela como elipse alargada a favor del viento: la deriva es
    Ld = u * t_caida, con t_caida = h/v_sed y v_sed la velocidad de sedimentacion de la gota."""
    h = P('neb_altura')
    v_sed = 0.30                       # m/s, gota de ~40 um evaporandose (ESTIMADO)
    t_f = h / v_sed
    Ld = float(u_ped) * t_f            # deriva horizontal [m]
    r0 = P('neb_radio')
    wr = math.radians((wd_deg + 180.0) % 360.0)   # WD = de donde viene -> hacia donde va
    ux, uy = math.sin(wr), math.cos(wr)
    cov = np.zeros(NP_)
    a_semi = r0 + Ld / 2.0
    b_semi = r0
    for (nx_, ny_) in NEB:
        cx = nx_ + ux * Ld / 2.0
        cy = ny_ + uy * Ld / 2.0
        dx = XS - cx; dy = YS - cy
        u_ = dx * ux + dy * uy
        v_ = -dx * uy + dy * ux
        q = (u_ / a_semi) ** 2 + (v_ / b_semi) ** 2
        cov = np.maximum(cov, np.exp(-2.0 * q))    # perfil gaussiano, no circulo duro
    return cov, Ld


RES = {}
for ename in ('E1', 'E2', 'E3'):
    e_ = ESC['escenarios'][ename]
    for hh in ('14:00', '16:00', '18:00'):
        v = e_['horas'][hh]
        Ta, RH, Bn, Dh, IR, u10 = v['Ta'], v['RH'], v['Bn'], v['Dh'], v['IR'], v['WS']
        uped = C.wind_at(u10)
        hloc = int(hh[:2])
        e_sun, a_sun = C.sun_position(dt.datetime(YEAR, 7, 21, hloc - C.TZ, 30))
        sv = C.sun_vector(e_sun, a_sun)
        sinel = max(math.sin(math.radians(e_sun)), 0.0)
        for est in ('A', 'B'):
            tau_g, _ = C.transmittance(VOX[est], g, XS, YS, 0.05, sv, kv=KV[est])
            tau_p, _ = C.transmittance(VOX[est], g, XS, YS, P('h_mrt'), sv, kv=KV[est])
            dtf_g = SKY[(est, 'grd')]['dtf']; svf_g = SKY[(est, 'grd')]['svf']
            dtf_p = SKY[(est, 'ped')]['dtf']; svf_p = SKY[(est, 'ped')]['svf']

            # --- temperatura de la hoja-canopy: elemento delgado, dos caras, con la
            #     lamina de microalgas evaporando por la cara superior (D15). CALCULADO.
            G_top = Bn * sinel + Dh
            Sabs_c = (1 - P('alb_canopy') - P('tau_canopy')) * G_top
            Ld_bot_c = P('eps_sup') * SIGMA * (Ta + 273.15 + 12.0) ** 4     # ve el pavimento caliente
            Rn_c = Sabs_c + P('eps_sup') * (IR + Ld_bot_c) - 2 * P('eps_sup') * SIGMA * (Ta + 273.15) ** 4
            LE_c = float(C.penman_open_water(max(Rn_c, 0.0), Ta, RH, C.wind_at(u10, 6.0)) * C.lambda_v(Ta))
            Tcan = float(C.thin_element_temp(Sabs_c, IR, Ld_bot_c, Ta, C.wind_at(u10, 6.0), LE=LE_c))
            Tcan_seco = float(C.thin_element_temp(Sabs_c, IR, Ld_bot_c, Ta, C.wind_at(u10, 6.0), LE=0.0))
            Top = Ta + 8.0        # fachada/estructura soleada (ESTIMADO, igual en A y B)
            Tveg = Ta + 2.0       # follaje transpirando (ESTIMADO, igual en A y B)

            def Ldown(svf, fcan, fop, fveg):
                """Infrarrojo descendente compuesto: cada fraccion del hemisferio emite a SU
                temperatura. Un rayo que atraviesa el dosel NO ve cielo frio."""
                return (svf * IR
                        + fcan * P('eps_sup') * SIGMA * (Tcan + 273.15) ** 4
                        + fop * P('eps_sup') * SIGMA * (Top + 273.15) ** 4
                        + fveg * P('eps_sup') * SIGMA * (Tveg + 273.15) ** 4)

            S = SKY[(est, 'grd')]
            G_grd = Bn * sinel * tau_g + Dh * dtf_g                 # global sobre el suelo
            alb = np.where(sur == 1, P('alb_agua'), np.where(sur == 2, P('alb_veg'), P('alb_granito')))
            alb = np.where(wet & (sur == 0), P('alb_granito_hum'), alb)
            Ld_grd = Ldown(S['svf'], S['f_can'], S['f_op'], S['f_veg'])

            LE = np.zeros(NP_)
            Rn0 = (1 - alb) * G_grd + P('eps_sup') * Ld_grd - P('eps_sup') * SIGMA * (Ta + 273.15) ** 4
            ev_w = C.penman_open_water(np.maximum(Rn0, 0), Ta, RH, uped)
            LE = np.where((sur == 1) | (wet & (sur == 0)), ev_w * C.lambda_v(Ta), LE)
            LE = np.where(sur == 2, 0.6 * ev_w * C.lambda_v(Ta), LE)   # vegetacion: 60 % de lamina libre
            Ts = C.surface_temp((1 - alb) * G_grd, Ld_grd, Ta, uped, LE=LE)

            # --- MRT a 1.10 m
            Sp = SKY[(est, 'ped')]
            D_sky = Dh * dtf_p + Sp['f_can'] * P('alb_canopy') * G_top * 0.5
            R_grd = alb * G_grd
            L_sky = Ldown(Sp['svf'], Sp['f_can'], Sp['f_op'], Sp['f_veg'])
            L_grd = P('eps_sup') * SIGMA * (Ts + 273.15) ** 4
            Tmrt = C.mrt(Bn, tau_p, e_sun, D_sky, R_grd, L_sky, L_grd)

            key = (ename, hh, est)
            RES[key] = dict(Ta=Ta, RH=RH, u10=u10, uped=uped, elev=e_sun, Tcan=Tcan,
                            Tcan_seco=Tcan_seco, LE_can=LE_c,
                            G=G_grd, Ts=Ts, Tmrt=Tmrt, tau=tau_p, svf=svf_p)
        rb = RES[(ename, hh, 'B')]
        log('   %s %s Ta %.1f elev %4.1f | A: Ts %.1f Tmrt %.1f | B: Ts %.1f Tmrt %.1f | dosel %.1f C '
            '(seco seria %.1f, la lamina de algas lo enfria %.1f K)'
            % (ename, hh, Ta, e_sun, RES[(ename, hh, 'A')]['Ts'].mean(), RES[(ename, hh, 'A')]['Tmrt'].mean(),
               rb['Ts'].mean(), rb['Tmrt'].mean(), rb['Tcan'], rb['Tcan_seco'], rb['Tcan_seco'] - rb['Tcan']))

# ================================================================ 6 · UTCI
log('6 · UTCI (polinomio oficial Brode et al. 2012, via pythermalcomfort)')
UT = {}
for (ename, hh, est), r in RES.items():
    va = max(r['u10'], 0.5)
    sub = slice(None, None, 3)          # UTCI es caro: se evalua 1 de cada 3 celdas y se interpola
    tm = r['Tmrt'][sub]
    res = UTCI(tdb=r['Ta'], tr=tm, v=va, rh=r['RH'], limit_inputs=False)
    val = np.array(res.utci if hasattr(res, 'utci') else res, dtype=float)
    full = np.interp(np.arange(NP_), np.arange(NP_)[sub], val)
    UT[(ename, hh, est)] = full
for ename in ('E1', 'E2', 'E3'):
    for hh in ('16:00',):
        a, b = UT[(ename, hh, 'A')], UT[(ename, hh, 'B')]
        log('   %s %s  UTCI  A %.1f  B %.1f  delta %+.2f K' % (ename, hh, a.mean(), b.mean(), (b - a).mean()))

# --- E4: nebulizacion activa (Ta y RH locales modificados de forma isoentalpica)
log('   E4 · nebulizacion activa: enfriamiento evaporativo local por saturacion adiabatica')
e3 = ESC['escenarios']['E2']['horas']['16:00']
Ta0, RH0, u10 = e3['Ta'], e3['RH'], e3['WS']
uped = C.wind_at(u10)
wd_dom = {'N': 0, 'NE': 45, 'E': 90, 'SE': 135, 'S': 180, 'SO': 225, 'O': 270, 'NO': 315}[
    ESC['ventana_critica']['viento_dom']]
cov, Ld = mist_field(uped, wd_dom)
Twb0 = float(C.wetbulb(Ta0, RH0))
eta = P('neb_eficiencia')
dT_mist = cov * eta * (Ta0 - Twb0)
Ta_m = Ta0 - dT_mist
w0 = 0.622 * C.pvap(Ta0, RH0) / (94000 - C.pvap(Ta0, RH0))
h0 = 1006 * Ta0 + w0 * (2501000 + 1860 * Ta0)
w_m = (h0 - 1006 * Ta_m) / (2501000 + 1860 * Ta_m)
e_m = 94000 * w_m / (0.622 + w_m)
RH_m = np.clip(100 * e_m / C.psat(Ta_m), 0, 100)
log('   deriva de la nube %.1f m (u=%.2f m/s, viento %s) · cobertura>0.3: %.0f m2 · '
    'Twb %.1f C · dT max %.2f K · RH pasa de %.0f%% a %.0f%%'
    % (Ld, uped, ESC['ventana_critica']['viento_dom'], (cov > 0.3).sum() * CELLA, Twb0,
       dT_mist.max(), RH0, RH_m.max()))
rB = RES[('E2', '16:00', 'B')]
sub = slice(None, None, 3)
res4 = UTCI(tdb=Ta_m[sub], tr=rB['Tmrt'][sub], v=max(u10, 0.5), rh=RH_m[sub], limit_inputs=False)
v4 = np.array(res4.utci if hasattr(res4, 'utci') else res4, float)
UT[('E4', '16:00', 'B')] = np.interp(np.arange(NP_), np.arange(NP_)[sub], v4)
np.save(os.path.join(DATA, 'mist_cov.npy'), tofield(cov))
np.save(os.path.join(DATA, 'mist_dT.npy'), tofield(dT_mist))
log('   UTCI E2/16h  B sin niebla %.1f  ->  con niebla %.1f  (delta %+.2f K en zona cubierta)'
    % (UT[('E2', '16:00', 'B')].mean(), UT[('E4', '16:00', 'B')].mean(),
       (UT[('E4', '16:00', 'B')] - UT[('E2', '16:00', 'B')])[cov > 0.3].mean()))

for k in list(RES):
    for f in ('G', 'Ts', 'Tmrt', 'tau', 'svf'):
        np.save(os.path.join(DATA, 'f_%s_%s_%s_%s.npy' % (k[0], k[1][:2], k[2], f)), tofield(RES[k][f]))
for k in UT:
    np.save(os.path.join(DATA, 'u_%s_%s_%s.npy' % (k[0], k[1][:2], k[2])), tofield(UT[k]))

C.jdump('escena_meta.json', dict(
    mallas=len(mesh), triangulos=int(sum(len(o['F']) for o in mesh)),
    celdas=NP_, area_ambito=NP_ * CELLA, area_pisable=float(WALK.sum() * CELLA),
    cell=C.VS, voxel=C.VS, sky_dirs=len(SKD),
    dias_ventana=len(DAYS), dias_muestra=len(SAMPLE), posiciones_solares=nc))
C.jdump('mist.json', dict(n=len(NEB), caudal_L_h=P('neb_caudal_L_h'), eficiencia=eta,
                          deriva_m=Ld, Twb=Twb0, Ta0=Ta0, RH0=RH0, uped=uped,
                          wd=ESC['ventana_critica']['viento_dom'],
                          area_cubierta=float((cov > 0.3).sum() * CELLA),
                          dT_max=float(dT_mist.max()), dT_medio_cubierto=float(dT_mist[cov > 0.3].mean())))
log('OK fase 1/2 — campos base escritos en _data/')
