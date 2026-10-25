# -*- coding: utf-8 -*-
"""
FASE 03B.5B — preparacion del clima real de Madrid centro.
Fuentes descargadas (no clima generico):
  · PVGIS v5.2 TMY   lat 40.4169 lon -3.7035 (Puerta del Sol) -> T2m, RH, G(h), Gb(n), Gd(h), IR(h), WS10m, WD10m, SP
  · PVGIS v5.2 serie horaria 2005-2020 (SARAH2 + ERA5) -> extremos reales de ola de calor
Produce _clima/escenarios.json con los 4 escenarios de trabajo, y el registro de procedencia.
"""
import csv
import json
import math
import os
import datetime as dt

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CL = os.path.join(HERE, '_clima')
LAT, LON, ELEV = 40.4169, -3.7035, 665.0

# ------------------------------------------------------------------ TMY
def read_tmy():
    p = os.path.join(CL, 'PVGIS_TMY_40.4169_-3.7035.csv')
    rows = []
    with open(p, encoding='utf-8') as f:
        lines = f.read().splitlines()
    i0 = next(i for i, l in enumerate(lines) if l.startswith('time(UTC)'))
    hdr = lines[i0].split(',')
    for l in lines[i0 + 1:]:
        if not l or not l[0].isdigit():
            break
        v = l.split(',')
        d = dict(zip(hdr, v))
        t = dt.datetime.strptime(d['time(UTC)'], '%Y%m%d:%H%M')
        rows.append(dict(t=t, month=t.month, day=t.day, hour=t.hour,
                         Ta=float(d['T2m']), RH=float(d['RH']), Gh=float(d['G(h)']),
                         Bn=float(d['Gb(n)']), Dh=float(d['Gd(h)']), IR=float(d['IR(h)']),
                         WS=float(d['WS10m']), WD=float(d['WD10m']), P=float(d['SP'])))
    return rows


def read_series():
    p = os.path.join(CL, 'PVGIS_HOURLY_2005_2020.csv')
    rows = []
    with open(p, encoding='utf-8') as f:
        lines = f.read().splitlines()
    i0 = next(i for i, l in enumerate(lines) if l.startswith('time,'))
    for l in lines[i0 + 1:]:
        if not l or not l[0].isdigit():
            break
        v = l.split(',')
        t = dt.datetime.strptime(v[0], '%Y%m%d:%H%M')
        rows.append(dict(t=t, Bi=float(v[1]), Di=float(v[2]), Ri=float(v[3]),
                         Hsun=float(v[4]), Ta=float(v[5]), WS=float(v[6])))
    return rows


# ------------------------------------------------------------------ psicrometria
def psat(T):
    """presion de vapor de saturacion [Pa] — Buck (1981), sobre agua."""
    return 611.21 * math.exp((18.678 - T / 234.5) * (T / (257.14 + T)))


def pvap(T, RH):
    return RH / 100.0 * psat(T)


def dewpoint(T, RH):
    e = pvap(T, RH)
    if e <= 0:
        return -60.0
    a, b = 17.62, 243.12
    g = math.log(e / 611.21)
    return b * g / (a - g)


def wetbulb(T, RH, P=94000.0):
    """temperatura de bulbo humedo [C] por iteracion sobre la ecuacion psicrometrica."""
    e = pvap(T, RH)
    lo, hi = -20.0, T
    for _ in range(60):
        w = (lo + hi) / 2
        # psicrometro: e = es(Tw) - gamma*P*(T - Tw), gamma ~ 6.53e-4 /K (aspirado)
        est = psat(w) - 6.53e-4 * P * (T - w)
        if est > e:
            hi = w
        else:
            lo = w
    return (lo + hi) / 2


def lambda_v(T):
    """calor latente de vaporizacion del agua [J/kg] — Regnault, valido 0-100 C."""
    return (2500.8 - 2.36 * T + 0.0016 * T ** 2 - 0.00006 * T ** 3) * 1000.0


def abs_humidity(T, RH, P=94000.0):
    """razon de mezcla [kg_v/kg_as]"""
    e = pvap(T, RH)
    return 0.622 * e / max(P - e, 1.0)


# ------------------------------------------------------------------ analisis
def main():
    tmy = read_tmy()
    ser = read_series()
    out = {}

    # --- ventana critica 15 jun - 15 sep
    def crit(r):
        m, d = r['t'].month, r['t'].day
        return (m == 6 and d >= 15) or m in (7, 8) or (m == 9 and d <= 15)

    tc = [r for r in tmy if crit(r)]
    sc = [r for r in ser if crit(r)]
    print('TMY horas totales %d · ventana critica %d h (%d dias)' % (len(tmy), len(tc), len(tc) / 24))

    Ta = np.array([r['Ta'] for r in tc])
    RH = np.array([r['RH'] for r in tc])
    WS = np.array([r['WS'] for r in tc])
    print('TMY ventana critica: Ta media %.1f  max %.1f  p95 %.1f | RH media %.0f%%  min %.0f%% | WS media %.2f m/s'
          % (Ta.mean(), Ta.max(), np.percentile(Ta, 95), RH.mean(), RH.min(), WS.mean()))

    # tarde (12-18 UTC ~ 14-20 local verano)
    tard = [r for r in tc if 12 <= r['hour'] <= 18]
    Tt = np.array([r['Ta'] for r in tard]); Rt = np.array([r['RH'] for r in tard])
    Wt = np.array([r['WS'] for r in tard]); Dt = np.array([r['WD'] for r in tard])
    print('TMY tarde critica (12-18 UTC): Ta %.1f (p95 %.1f) · RH %.0f%% · WS %.2f m/s' %
          (Tt.mean(), np.percentile(Tt, 95), Rt.mean(), Wt.mean()))
    # direccion dominante de viento en la tarde critica
    hist = np.histogram(Dt % 360, bins=np.arange(0, 361, 45))[0]
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO']
    dom = int(np.argmax(hist))
    print('   viento dominante tarde: %s (%.0f %% de las horas)' % (dirs[dom], 100 * hist[dom] / hist.sum()))

    # --- extremo real 2005-2020
    sT = np.array([r['Ta'] for r in sc])
    print('SERIE 2005-2020 ventana critica: Ta max absoluta %.1f  p99 %.1f  p95 %.1f' %
          (sT.max(), np.percentile(sT, 99), np.percentile(sT, 95)))
    # dia mas calido por media de maximas diurnas
    byday = {}
    for r in sc:
        byday.setdefault(r['t'].date(), []).append(r['Ta'])
    dmax = {d: max(v) for d, v in byday.items()}
    hot = sorted(dmax.items(), key=lambda q: -q[1])[:8]
    print('   dias mas calidos del registro real:')
    for d, v in hot:
        print('     %s  Tmax %.1f C' % (d, v))
    HOTDAY = hot[0][0]
    hd = sorted([r for r in ser if r['t'].date() == HOTDAY], key=lambda r: r['t'])
    print('   perfil del dia %s:' % HOTDAY)
    print('     ' + ' '.join('%02dh:%.0f' % (r['t'].hour, r['Ta']) for r in hd[6:22]))

    # humedad del dia de ola de calor: se conserva la razon de mezcla tipica de tarde critica
    # (las olas de calor en Madrid son adveccion seca: el punto de rocio se mantiene bajo)
    tds = [dewpoint(r['Ta'], r['RH']) for r in tard]
    td_med = float(np.median(tds))
    td_p25 = float(np.percentile(tds, 25))
    print('   punto de rocio tarde critica TMY: mediana %.1f C  p25 %.1f C' % (td_med, td_p25))

    # --- perfiles horarios medios de la ventana critica (para escenario "verano normal")
    prof = {}
    for h in range(24):
        hh = [r for r in tc if r['hour'] == h]
        prof[h] = dict(Ta=float(np.mean([r['Ta'] for r in hh])),
                       RH=float(np.mean([r['RH'] for r in hh])),
                       Bn=float(np.mean([r['Bn'] for r in hh])),
                       Dh=float(np.mean([r['Dh'] for r in hh])),
                       Gh=float(np.mean([r['Gh'] for r in hh])),
                       IR=float(np.mean([r['IR'] for r in hh])),
                       WS=float(np.mean([r['WS'] for r in hh])))

    # dia despejado representativo del TMY dentro de la ventana (para radiacion de diseno)
    bydayT = {}
    for r in tc:
        bydayT.setdefault((r['month'], r['day']), []).append(r)
    best, bestv = None, -1
    for k, v in bydayT.items():
        if len(v) != 24:
            continue
        g = sum(r['Gh'] for r in v)
        if g > bestv:
            best, bestv = k, g
    clear = sorted(bydayT[best], key=lambda r: r['hour'])
    print('   dia mas despejado de la ventana TMY: %02d-%02d  (%.1f kWh/m2 dia horizontal)' % (best[1], best[0], bestv / 1000))

    # ---- ESCENARIOS
    def sc_from(hour_prof, label, desc, ta_off=0.0, rh_over=None, ws_over=None):
        h14 = hour_prof[12]        # 12 UTC = 14 h local (CEST)
        h16 = hour_prof[14]
        h18 = hour_prof[16]
        d = {}
        for nm, hp in (('14:00', h14), ('16:00', h16), ('18:00', h18)):
            Taa = hp['Ta'] + ta_off
            RHh = rh_over(Taa, hp) if callable(rh_over) else (rh_over if rh_over else hp['RH'])
            RHh = max(5.0, min(100.0, RHh))
            d[nm] = dict(Ta=round(Taa, 2), RH=round(RHh, 1),
                         Bn=round(hp['Bn'], 1), Dh=round(hp['Dh'], 1), Gh=round(hp['Gh'], 1),
                         IR=round(hp['IR'], 1), WS=round(ws_over or hp['WS'], 2),
                         Twb=round(wetbulb(Taa, RHh), 2), Td=round(dewpoint(Taa, RHh), 2))
        return dict(label=label, desc=desc, horas=d)

    # escenario 1: verano normal = perfil medio de la ventana critica del TMY
    E1 = sc_from(prof, 'E1 · VERANO NORMAL',
                 'Perfil horario medio de la ventana 15 jun–15 sep del TMY PVGIS (12 anos reales seleccionados).')

    # escenario 2: tarde calurosa = p95 de temperatura de tarde, radiacion de dia despejado
    prof2 = {h: dict(prof[h]) for h in prof}
    off95 = float(np.percentile(Tt, 95) - Tt.mean())
    cl = {r['hour']: r for r in clear}
    for h in prof2:
        if h in cl:
            prof2[h]['Bn'] = cl[h]['Bn']; prof2[h]['Dh'] = cl[h]['Dh']; prof2[h]['Gh'] = cl[h]['Gh']

    def rh_conserva(Taa, hp):
        """RH recalculada conservando el punto de rocio mediano de la tarde critica."""
        return 100.0 * psat(td_med) / psat(Taa)

    E2 = sc_from(prof2, 'E2 · TARDE CALUROSA',
                 'Temperatura = p95 de las tardes de la ventana critica (+%.1f K sobre la media); radiacion del dia '
                 'mas despejado del TMY; humedad conservando el punto de rocio mediano (%.1f C).' % (off95, td_med),
                 ta_off=off95, rh_over=rh_conserva)

    # escenario 3: ola de calor = dia real mas calido 2005-2020
    hdmap = {r['t'].hour: r for r in hd}
    prof3 = {h: dict(prof[h]) for h in prof}
    for h in prof3:
        if h in hdmap:
            prof3[h]['Ta'] = hdmap[h]['Ta']
            prof3[h]['WS'] = hdmap[h]['WS']
        if h in cl:
            prof3[h]['Bn'] = cl[h]['Bn']; prof3[h]['Dh'] = cl[h]['Dh']; prof3[h]['Gh'] = cl[h]['Gh']

    def rh_seca(Taa, hp):
        return 100.0 * psat(td_p25) / psat(Taa)

    E3 = sc_from(prof3, 'E3 · OLA DE CALOR',
                 'Dia real mas calido del registro PVGIS 2005-2020 en estas coordenadas (%s, Tmax %.1f C); radiacion '
                 'de cielo despejado; humedad conservando el punto de rocio del p25 de tardes criticas (%.1f C), '
                 'coherente con adveccion seca.' % (HOTDAY, hot[0][1], td_p25),
                 rh_over=rh_seca)

    esc = dict(
        fuente=dict(
            dataset_1='PVGIS v5.2 TMY (typical meteorological year)',
            dataset_2='PVGIS v5.2 seriescalc horaria 2005-2020, base de radiacion PVGIS-SARAH2, temperatura ERA5',
            lat=LAT, lon=LON, elev_m=ELEV,
            descarga=dt.date.today().isoformat(),
            url_tmy='https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat=40.4169&lon=-3.7035&outputformat=csv',
            url_serie='https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?lat=40.4169&lon=-3.7035&startyear=2005&endyear=2020&outputformat=csv&components=1',
            anos_tmy={m: y for m, y in [(1, 2013), (2, 2010), (3, 2008), (4, 2007), (5, 2020), (6, 2008),
                                        (7, 2012), (8, 2007), (9, 2015), (10, 2012), (11, 2018), (12, 2017)]},
            nota_uhi='ERA5/SARAH2 resuelve ~30 km: NO contiene la isla de calor urbana de Madrid centro. '
                     'Los valores de Ta son de fondo regional; el efecto UHI se trata como hipotesis separada '
                     'y se somete a analisis de sensibilidad. NO se ha aplicado ningun ajuste oculto.'),
        ventana_critica=dict(desde='06-15', hasta='09-15', horas=len(tc),
                             Ta_media=round(float(Ta.mean()), 2), Ta_max=round(float(Ta.max()), 2),
                             Ta_p95=round(float(np.percentile(Ta, 95)), 2),
                             RH_media=round(float(RH.mean()), 1), RH_min=round(float(RH.min()), 1),
                             WS_media=round(float(WS.mean()), 2),
                             tarde_Ta=round(float(Tt.mean()), 2), tarde_Ta_p95=round(float(np.percentile(Tt, 95)), 2),
                             tarde_RH=round(float(Rt.mean()), 1), tarde_WS=round(float(Wt.mean()), 2),
                             viento_dom=dirs[dom], viento_dom_pct=round(100 * float(hist[dom]) / hist.sum(), 1),
                             Td_mediana=round(td_med, 2), Td_p25=round(td_p25, 2)),
        extremo_real=dict(dia=str(HOTDAY), Tmax=round(hot[0][1], 2),
                          top8=[[str(d), round(v, 2)] for d, v in hot],
                          Ta_p99_serie=round(float(np.percentile(sT, 99)), 2)),
        dia_despejado_tmy=dict(mes=best[0], dia=best[1], kWh_m2_dia=round(bestv / 1000, 2)),
        perfil_horario_critico=prof,
        escenarios=dict(E1=E1, E2=E2, E3=E3),
    )
    json.dump(esc, open(os.path.join(CL, 'escenarios.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    print('\nESCENARIOS DE TRABAJO (hora local CEST = UTC+2)')
    for k in ('E1', 'E2', 'E3'):
        e = esc['escenarios'][k]
        print(' %s' % e['label'])
        for hh, v in e['horas'].items():
            print('   %s  Ta %5.1f C · RH %4.1f %% · Twb %5.1f C · Bn %5.0f · Dh %4.0f · IR %4.0f W/m2 · WS %.2f m/s'
                  % (hh, v['Ta'], v['RH'], v['Twb'], v['Bn'], v['Dh'], v['IR'], v['WS']))
    print('\nDepresion de bulbo humedo disponible (limite fisico del enfriamiento evaporativo):')
    for k in ('E1', 'E2', 'E3'):
        e = esc['escenarios'][k]
        v = e['horas']['16:00']
        print('   %-22s 16:00  Ta-Twb = %.1f K' % (e['label'], v['Ta'] - v['Twb']))


if __name__ == '__main__':
    main()
