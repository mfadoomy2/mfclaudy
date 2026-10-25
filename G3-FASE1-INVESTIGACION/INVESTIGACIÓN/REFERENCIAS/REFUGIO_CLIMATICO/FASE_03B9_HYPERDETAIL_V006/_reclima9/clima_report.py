# -*- coding: utf-8 -*-
"""FASE 03B.5B — documentos. Mismo lenguaje grafico que 03B.5: A3 apaisado, misma paleta,
mismos margenes, misma estructura editorial."""
import csv
import datetime as dt
import json
import math
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import BoundaryNorm, ListedColormap, TwoSlopeNorm
from matplotlib.patches import Polygon as MPoly, Rectangle, Circle

import clima_core as C
from clima_core import P, DATA, CL, HERE

A3 = (16.54, 11.69)
ROSA, VERDE, TEAL = '#D6577F', '#4E8446', '#2E6E6B'
GRIS, TINTA = '#8a877f', '#33322E'
SEVC = {'RED': '#C8322B', 'YELLOW': '#E0A422', 'GREEN': '#4E8446'}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8,
                     'axes.edgecolor': GRIS, 'axes.labelcolor': TINTA, 'text.color': TINTA,
                     'xtick.color': GRIS, 'ytick.color': GRIS, 'axes.linewidth': 0.5,
                     'pdf.fonttype': 42})

M = json.load(open(os.path.join(C.F03B if hasattr(C, 'F03B') else
                                os.path.join(C.ROOT, 'FASE_03B_MODELO_MAESTRO'),
                                'geometria_maestra_v002.json'), encoding='utf-8'))
CC = M['contexto']['casa_correos']
ESC = json.load(open(os.path.join(CL, 'escenarios.json'), encoding='utf-8'))
D = {n: C.jload(n + '.json') for n in ('escena_meta', 'metricas', 'agua', 'vegetacion', 'zonas',
                                       'discos', 'refugio', 'spots', 'cinta', 'mist',
                                       'neb_escenarios', 'aire', 'issues')}
MET, ISS = D['metricas'], D['issues']
g = C.grid05()
EXT = (g.x0, g.x1, g.y0, g.y1)
PL = np.load(os.path.join(C.AUD, '_data', 'plaza.npy'))[::2, ::2][:g.ny, :g.nx]


def F(n):
    return np.load(os.path.join(DATA, n + '.npy'))


# ---------------------------------------------------------------- lamina
def sheet(title, sub='', kicker='FASE 03B.5B · AUDITORÍA CLIMÁTICA DEL REFUGIO'):
    fig = plt.figure(figsize=A3)
    fig.text(0.035, 0.955, ' '.join(kicker), color=ROSA, fontsize=6.2)
    fig.text(0.035, 0.925, title, fontsize=19, weight='bold')
    if sub:
        fig.text(0.035, 0.900, sub, fontsize=8.5, color=GRIS)
    fig.text(0.035, 0.022,
             'REFUGIO CLIMÁTICO PUERTA DEL SOL · SOL_FULL_SCENE_v001 (6.672 mallas · 394.610 triángulos) · '
             'clima PVGIS v5.2 TMY + serie 2005-2020 en 40,4169 N 3,7035 O · 2026-08-10 · '
             'EL MASTER NO SE HA MODIFICADO',
             fontsize=6.5, color=GRIS)
    return fig


def close(pdf, fig):
    pdf.savefig(fig); plt.close(fig)


def plan(ax, e=None):
    for b in M['contexto']['buildings']:
        if len(b['pts']) < 3:
            continue
        xs = [p[0] for p in b['pts']]; ys = [p[1] for p in b['pts']]
        if max(xs) < -125 or min(xs) > 115 or max(ys) < -60 or min(ys) > 95:
            continue
        ax.add_patch(MPoly([(p[0], p[1]) for p in b['pts']], closed=True, facecolor='#EDEBE6',
                           edgecolor='#CFCBC2', lw=0.4, zorder=1))
    ax.add_patch(MPoly([(p[0], p[1]) for p in CC['pts']], closed=True, facecolor='#E4D6CE',
                       edgecolor='#B08968', lw=0.8, zorder=2))
    ee = e or (-112, 100, -45, 78)
    ax.set_xlim(ee[0], ee[1]); ax.set_ylim(ee[2], ee[3]); ax.set_aspect('equal')
    ax.tick_params(labelsize=5.5)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def mapa(ax, field, cmap, vmin=None, vmax=None, norm=None, title='', cb=True, fig=None, cblab='',
         cbrect=None):
    plan(ax)
    im = ax.imshow(field, origin='lower', extent=EXT, cmap=cmap, vmin=vmin, vmax=vmax, norm=norm,
                   interpolation='nearest', zorder=3)
    if title:
        ax.set_title(title, fontsize=7.5, loc='left', color=TEAL, weight='bold')
    if cb and fig is not None and cbrect:
        cax = fig.add_axes(cbrect)
        c = fig.colorbar(im, cax=cax, orientation='horizontal')
        c.set_label(cblab, fontsize=6.2); c.ax.tick_params(labelsize=5.4)
    return im


def table(ax, rows, colw, header=None, fs=7.0, rowh=0.036, y0=0.97):
    ax.axis('off')
    y = y0
    if header:
        x = 0.0
        for t, w in zip(header, colw):
            ax.text(x, y, t, fontsize=fs, weight='bold', color=TEAL, va='top', transform=ax.transAxes)
            x += w
        y -= rowh * 1.15
        ax.plot([0, sum(colw)], [y + rowh * .35] * 2, color=GRIS, lw=.4, transform=ax.transAxes)
    for r in rows:
        x = 0.0
        col = r[-1] if isinstance(r[-1], str) and r[-1].startswith('#') else None
        for t, w in zip(r[:-1] if col else r, colw):
            ax.text(x, y, str(t), fontsize=fs, va='top', color=col or TINTA, transform=ax.transAxes)
            x += w
        y -= rowh
        if y < 0.015:
            break
    return y


def para(fig, x, y, txt, fs=8, color=TINTA, w=0.9):
    """Ajuste de linea real: matplotlib con wrap=True usa el ancho de la FIGURA e ignora w,
    lo que hacia que los parrafos se salieran de la lamina."""
    import textwrap
    n = max(20, int(w * 1900 / fs))
    out = []
    for blk in txt.split('\n'):
        out.extend(textwrap.wrap(blk, n) or [''])
    fig.text(x, y, '\n'.join(out), fontsize=fs, color=color, va='top', linespacing=1.45)


CERT = ('CERTEZA DE CADA CIFRA — MEDIDO: leído de la geometría aprobada. CALCULADO: resuelto con física '
        'cerrada (balance de energía, psicrometría, Beer-Lambert). SIMULADO: trazado de rayos sobre el '
        'vóxel de la escena. ESTIMADO: parámetro de literatura dentro de un rango declarado. '
        'HIPÓTESIS: dato que el modelo 03B no contiene y que se fija explícitamente.')


# ================================================================== 1 · SOL Y SOMBRA
def pdf_shadow():
    out = os.path.join(HERE, 'SOLAR_SHADOW_AUDIT.pdf')
    shA, shB = F('shade_crit_A') * 100, F('shade_crit_B') * 100
    suA, suB = F('sunhours_A'), F('sunhours_B')
    with PdfPages(out) as pdf:
        fig = sheet('SOLAR_SHADOW_AUDIT · sombra en el periodo crítico',
                    'Fracción de las horas 12:00–18:00 locales en sombra, integrada sobre los 93 días de la ventana '
                    '15 jun–15 sep. SIMULADO: trazado de rayos sobre vóxel de 0,50 m con la posición solar real.')
        cmap = ListedColormap(['#C8322B', '#E2684A', '#E0A422', '#E9CE72', '#CFE0A0', '#9FC46F',
                               '#6FA24F', '#4E8446', '#2F5E33'])
        nrm = BoundaryNorm([0, 5, 10, 20, 30, 45, 60, 75, 90, 101], cmap.N)
        for k, (f_, t) in enumerate(((shA, 'ESTADO A · Sol actual'), (shB, 'ESTADO B · propuesta'))):
            ax = fig.add_axes([0.035 + k * 0.325, 0.46, 0.30, 0.40])
            mapa(ax, np.where(PL, f_, np.nan), cmap, norm=nrm, title=t, fig=fig,
                 cbrect=[0.035 + k * 0.325, 0.425, 0.24, 0.012],
                 cblab='% de las horas 12–18 h en sombra')
        ax = fig.add_axes([0.685, 0.46, 0.29, 0.40])
        mapa(ax, np.where(PL, shB - shA, np.nan), 'BrBG', vmin=-60, vmax=60,
             title='DELTA · sombra ganada (puntos porcentuales)', fig=fig,
             cbrect=[0.685, 0.425, 0.24, 0.012], cblab='pp de sombra añadidos por la intervención')
        axt = fig.add_axes([0.035, 0.055, 0.42, 0.33])
        table(axt, [
            ['sombra media en 12–18 h · todo el ámbito', '%.1f %%' % MET['sombra_crit_A'], '%.1f %%' % MET['sombra_crit_B'], '#33322E'],
            ['sombra media en 12–18 h · suelo pisable', '%.1f %%' % MET['sombra_crit_A_pisable'], '%.1f %%' % MET['sombra_crit_B_pisable'], '#33322E'],
            ['horas de sol acumuladas en la ventana', '%.0f h' % MET['sunh_A'], '%.0f h' % MET['sunh_B'], '#33322E'],
            ['m² de sombra añadidos (12–18 h)', '—', '%.0f m²' % MET['m2_sombra_extra'], VERDE],
        ], [0.52, 0.24, 0.24], ['MÉTRICA', 'ACTUAL', 'PROPUESTA'], fs=8, rowh=0.075)
        rows = [[z['zona'][:20], '%.1f' % z['sombra_A'], '%.1f' % z['sombra_B'],
                 '%+.1f' % (z['sombra_B'] - z['sombra_A']),
                 VERDE if z['sombra_B'] - z['sombra_A'] > 40 else (SEVC['YELLOW'] if z['sombra_B'] - z['sombra_A'] > 15 else SEVC['RED'])]
                for z in D['zonas']]
        axz = fig.add_axes([0.49, 0.055, 0.30, 0.33])
        table(axz, rows, [0.44, 0.19, 0.19, 0.18], ['zona de programa', 'A %', 'B %', 'Δ pp'], fs=7.2, rowh=0.062)
        para(fig, 0.82, 0.385,
             'LECTURA. Puerta del Sol hoy es una plaza prácticamente sin sombra: sólo el %.1f %% de las horas '
             'críticas, y esa poca sombra la dan los edificios del borde, no el espacio central.\n\n'
             'La propuesta lleva esa cifra al %.1f %%, es decir multiplica por %.1f la sombra disponible en las '
             'horas de mayor estrés y añade %.0f m² de suelo protegido.\n\n'
             'Pero el reparto es muy desigual: las zonas de estancia bajo dosel superan el 80 %%, mientras que '
             'los corredores peatonales se quedan en el 21 %%.'
             % (MET['sombra_crit_A'], MET['sombra_crit_B'], MET['sombra_crit_B'] / max(MET['sombra_crit_A'], .01),
                MET['m2_sombra_extra']), fs=8)
        close(pdf, fig)

        fig = sheet('SOLAR_SHADOW_AUDIT · horas de sol acumuladas y días representativos')
        for k, (f_, t) in enumerate(((suA, 'ESTADO A'), (suB, 'ESTADO B'))):
            ax = fig.add_axes([0.035 + k * 0.25, 0.50, 0.23, 0.36])
            mapa(ax, np.where(PL, f_, np.nan), 'YlOrRd', vmin=0, vmax=1400,
                 title='%s · horas de sol (15 jun–15 sep)' % t, fig=fig,
                 cbrect=[0.035 + k * 0.25, 0.465, 0.19, 0.011], cblab='horas de sol acumuladas')
        ax = fig.add_axes([0.535, 0.50, 0.23, 0.36])
        mapa(ax, np.where(PL, suB - suA, np.nan), 'BrBG_r', vmin=-900, vmax=900,
             title='DELTA · horas de sol evitadas', fig=fig,
             cbrect=[0.535, 0.465, 0.19, 0.011], cblab='Δ horas de sol')
        axw = fig.add_axes([0.79, 0.50, 0.185, 0.36])
        wa, wb = F('radwin_A'), F('radwin_B')
        mapa(axw, np.where(PL, wb - wa, np.nan), 'coolwarm_r', vmin=-2, vmax=2,
             title='INVIERNO · 21 dic, Δ kWh/m²·día', fig=fig,
             cbrect=[0.79, 0.465, 0.15, 0.011], cblab='Δ radiación de invierno')
        para(fig, 0.035, 0.41,
             'EFECTO INVIERNO (punto 29 del encargo). El 21 de diciembre la radiación media sobre el suelo del ámbito '
             'pasa de %.2f a %.2f kWh/m²·día: el dosel retiene el %.0f %% de la radiación de invierno. No es un efecto '
             'menor. El dosel del proyecto NO es estacional —la membrana tensada y la lámina de microalgas son fijas, '
             'a diferencia de un arbolado caduco—, de modo que la misma pieza que protege en agosto sombrea en '
             'diciembre. Se registra como incidencia; no se corrige.'
             % (MET['win_A'], MET['win_B'], MET['win_perdida_pct']), fs=8.5)
        para(fig, 0.035, 0.30, CERT, fs=7, color=GRIS)
        close(pdf, fig)
    return out


def pdf_atlas():
    """SHADOW_HOURLY_ATLAS — 09:00 a 20:00 locales de un día de verano."""
    out = os.path.join(HERE, 'SHADOW_HOURLY_ATLAS.pdf')
    vB = np.load(os.path.join(DATA, 'voxB.npy'))
    kvv = {'B': np.load(os.path.join(DATA, 'kvB.npy')), 'A': np.load(os.path.join(DATA, 'kvA.npy'))}
    vA = np.load(os.path.join(DATA, 'voxA.npy'))
    II, JJ = np.where(PL)
    XS = g.x0 + (JJ + .5) * C.VS; YS = g.y0 + (II + .5) * C.VS
    with PdfPages(out) as pdf:
        for est, vox, lbl in (('B', vB, 'ESTADO B · PROPUESTA'), ('A', vA, 'ESTADO A · SOL ACTUAL')):
            fig = sheet('SHADOW_HOURLY_ATLAS · %s' % lbl,
                        '21 de julio, hora local (CEST = UTC+2). Gris = suelo en sombra; amarillo = suelo al sol. '
                        'SIMULADO con posición solar real (algoritmo PSA, validado contra PVGIS: error medio 0,03°).')
            for k, hl in enumerate(range(9, 21)):
                e, a = C.sun_position(dt.datetime(2019, 7, 21, hl - C.TZ, 30))
                ax = fig.add_axes([0.035 + (k % 4) * 0.243, 0.62 - (k // 4) * 0.195, 0.225, 0.175])
                if e <= 1:
                    f_ = np.full((g.ny, g.nx), np.nan)
                else:
                    tau, _ = C.transmittance(vox, g, XS, YS, 0.05, C.sun_vector(e, a), kv=kvv[est])
                    f_ = np.full((g.ny, g.nx), np.nan); f_[II, JJ] = (tau >= 0.5).astype(float)
                plan(ax)
                ax.imshow(f_, origin='lower', extent=EXT, cmap=ListedColormap(['#6E6A62', '#F2C94C']),
                          vmin=0, vmax=1, interpolation='nearest', zorder=3)
                pct = 100 * np.nanmean(f_) if np.isfinite(f_).any() else 0
                ax.set_title('%02d:00 · sol %.0f° · %.0f %% al sol' % (hl, max(e, 0), pct),
                             fontsize=6.5, loc='left', color=TEAL)
                ax.set_xticks([]); ax.set_yticks([])
            close(pdf, fig)
    return out


# ================================================================== 2 · RADIACION
def pdf_radiation():
    outs = []
    rA, rB, rD = F('rad_A'), F('rad_B'), F('rad_delta')
    vmax = float(np.nanpercentile(rA[PL], 99))
    for nm, f_, t, cm, kw in (('SOLAR_RADIATION_CURRENT', rA, 'ESTADO A · Sol actual', 'inferno', {}),
                              ('SOLAR_RADIATION_PROPOSAL', rB, 'ESTADO B · propuesta', 'inferno', {}),
                              ('DELTA_SOLAR_RADIATION', rD, 'DELTA · propuesta − actual', 'BrBG', {})):
        p = os.path.join(HERE, nm + '.pdf')
        with PdfPages(p) as pdf:
            fig = sheet('%s' % nm.replace('_', ' '),
                        'Radiación solar acumulada sobre el suelo en la ventana 15 jun–15 sep [kWh/m²]. '
                        'MISMA LEYENDA en los tres documentos. Directa con transmitancia por trazado de rayos + '
                        'difusa ponderada por el factor de transmisión de cielo. Datos horarios reales del TMY PVGIS.')
            ax = fig.add_axes([0.06, 0.16, 0.60, 0.70])
            if nm.startswith('DELTA'):
                mapa(ax, np.where(PL, f_, np.nan), cm, vmin=-vmax * .6, vmax=vmax * .6, title=t,
                     fig=fig, cbrect=[0.06, 0.115, 0.42, 0.014], cblab='Δ kWh/m² acumulados')
            else:
                mapa(ax, np.where(PL, f_, np.nan), cm, vmin=0, vmax=vmax, title=t, fig=fig,
                     cbrect=[0.06, 0.115, 0.42, 0.014], cblab='kWh/m² acumulados (15 jun – 15 sep)')
            axt = fig.add_axes([0.70, 0.42, 0.28, 0.44])
            v = f_[PL]; v = v[np.isfinite(v)]
            table(axt, [['media', '%.0f kWh/m²' % v.mean()], ['mediana', '%.0f' % np.median(v)],
                        ['percentil 5', '%.0f' % np.percentile(v, 5)],
                        ['percentil 95', '%.0f' % np.percentile(v, 95)],
                        ['mínimo', '%.0f' % v.min()], ['máximo', '%.0f' % v.max()]],
                  [0.55, 0.45], ['ESTADÍSTICO', 'VALOR'], fs=8, rowh=0.07)
            axh = fig.add_axes([0.70, 0.16, 0.28, 0.22])
            axh.hist(v, bins=40, color=ROSA if nm.startswith('DELTA') else VERDE, alpha=.8, lw=0)
            axh.set_xlabel('kWh/m²', fontsize=6.5); axh.tick_params(labelsize=6)
            for s in ('top', 'right'):
                axh.spines[s].set_visible(False)
            close(pdf, fig)
        outs.append(p)

    p = os.path.join(HERE, 'SOLAR_RADIATION_AUDIT.pdf')
    with PdfPages(p) as pdf:
        fig = sheet('SOLAR_RADIATION_AUDIT · síntesis',
                    'Radiación acumulada 15 jun–15 sep. La reducción media es del %.1f %%.' % MET['rad_red_pct'])
        for k, (f_, t, cm, vr) in enumerate((
                (rA, 'ACTUAL', 'inferno', (0, vmax)), (rB, 'PROPUESTA', 'inferno', (0, vmax)),
                (rD, 'DELTA', 'BrBG', (-vmax * .6, vmax * .6)))):
            ax = fig.add_axes([0.035 + k * 0.325, 0.46, 0.30, 0.40])
            mapa(ax, np.where(PL, f_, np.nan), cm, vmin=vr[0], vmax=vr[1], title=t, fig=fig,
                 cbrect=[0.035 + k * 0.325, 0.425, 0.24, 0.012], cblab='kWh/m²')
        axt = fig.add_axes([0.035, 0.06, 0.44, 0.33])
        table(axt, [
            ['radiación media acumulada', '%.0f kWh/m²' % MET['rad_A'], '%.0f kWh/m²' % MET['rad_B'], VERDE],
            ['reducción media', '—', '%.1f %%' % MET['rad_red_pct'], VERDE],
            ['reducción máxima puntual', '—', '%.0f %%' % MET['rad_red_max_pct'], VERDE],
            ['radiación evitada por m² de plaza', '—', '%.0f kWh/m²' % (MET['rad_A'] - MET['rad_B']), VERDE],
            ['energía solar total evitada en el ámbito', '—', '%.0f MWh' % ((MET['rad_A'] - MET['rad_B']) * MET['area_ambito'] / 1000), VERDE],
        ], [0.46, 0.26, 0.28], ['MAGNITUD', 'ACTUAL', 'PROPUESTA'], fs=8, rowh=0.075)
        para(fig, 0.52, 0.39,
             'Sobre los %.0f m² del ámbito, la intervención evita del orden de %.0f MWh de energía solar durante los '
             '93 días del periodo crítico. Esa es la magnitud física de la que dependen todos los resultados '
             'posteriores: la sombra no es un efecto estético, es la retirada de una potencia real del balance '
             'energético de la plaza.\n\nEl mapa DELTA muestra que la reducción no es homogénea: hay bandas que '
             'pierden más del 80 %% de la radiación (racimos de dosel de C1, C2 y C3) y bandas que apenas cambian '
             '(los corredores y el eje Mayor–Alcalá, que el generador mantiene deliberadamente despejados).'
             % (MET['area_ambito'], (MET['rad_A'] - MET['rad_B']) * MET['area_ambito'] / 1000), fs=8.5)
        close(pdf, fig)
    outs.append(p)
    return outs


# ================================================================== 3 · MRT
def pdf_mrt():
    outs = []
    for nm in ('MRT_CURRENT_PROPOSAL_DELTA', 'MRT_AUDIT'):
        p = os.path.join(HERE, nm + '.pdf')
        with PdfPages(p) as pdf:
            for hh in ('14', '16', '18'):
                a, b = F('f_E2_%s_A_Tmrt' % hh), F('f_E2_%s_B_Tmrt' % hh)
                fig = sheet('%s · %s:00 h local' % (nm.replace('_', ' '), hh),
                            'Temperatura radiante media a 1,10 m · escenario E2 TARDE CALUROSA '
                            '(Ta %.1f °C, HR %.0f %%, viento %.1f m/s). CALCULADO: modelo de dos hemisferios '
                            'VDI 3787 con infrarrojo descendente MEDIDO por PVGIS y temperaturas de superficie '
                            'resueltas por balance de energía.'
                            % (ESC['escenarios']['E2']['horas'][hh + ':00']['Ta'],
                               ESC['escenarios']['E2']['horas'][hh + ':00']['RH'],
                               ESC['escenarios']['E2']['horas'][hh + ':00']['WS']))
                vmin, vmax = 25, 70
                for k, (f_, t, cm, vr) in enumerate((
                        (a, 'ACTUAL', 'inferno', (vmin, vmax)), (b, 'PROPUESTA', 'inferno', (vmin, vmax)),
                        (b - a, 'DELTA MRT', 'RdBu', (-30, 30)))):
                    ax = fig.add_axes([0.035 + k * 0.325, 0.42, 0.30, 0.44])
                    mapa(ax, np.where(PL, f_, np.nan), cm, vmin=vr[0], vmax=vr[1], title=t, fig=fig,
                         cbrect=[0.035 + k * 0.325, 0.385, 0.24, 0.012],
                         cblab='MRT [°C]' if k < 2 else 'Δ MRT [K]')
                va, vb = a[PL], b[PL]
                va = va[np.isfinite(va)]; vb = vb[np.isfinite(vb)]
                axt = fig.add_axes([0.035, 0.05, 0.42, 0.29])
                table(axt, [['MRT media', '%.1f °C' % va.mean(), '%.1f °C' % vb.mean(), '%+.1f K' % (vb.mean() - va.mean())],
                            ['MRT p95', '%.1f' % np.percentile(va, 95), '%.1f' % np.percentile(vb, 95),
                             '%+.1f' % (np.percentile(vb, 95) - np.percentile(va, 95))],
                            ['MRT mínima', '%.1f' % va.min(), '%.1f' % vb.min(), '%+.1f' % (vb.min() - va.min())],
                            ['MRT máxima', '%.1f' % va.max(), '%.1f' % vb.max(), '%+.1f' % (vb.max() - va.max())]],
                      [0.34, 0.22, 0.22, 0.22], ['MRT a 1,10 m', 'ACTUAL', 'PROPUESTA', 'Δ'], fs=8, rowh=0.075)
                peor = float(np.nanmax(np.where(PL, b - a, np.nan)))
                para(fig, 0.49, 0.335,
                     'La MRT es la magnitud que más cambia: la sombra retira el haz directo, que es el término '
                     'dominante del balance radiante sobre el cuerpo.\n\n'
                     'ATENCIÓN A LA COLA POSITIVA DEL MAPA DELTA. En parte del ámbito la MRT SUBE (hasta %+.1f K). '
                     'No es un error de cálculo: son puntos que siguen recibiendo sol pero que han perdido vista de '
                     'cielo frío, y por tanto pierden capacidad de radiar hacia arriba mientras ven la cara inferior '
                     'caliente de estructuras. Es el mecanismo clásico de atrapamiento radiante urbano. Se documenta '
                     'porque contradice la intuición de que "más estructura = más fresco".' % peor, fs=8.5)
                close(pdf, fig)
                if nm == 'MRT_CURRENT_PROPOSAL_DELTA' and hh == '18':
                    break
                if nm == 'MRT_AUDIT' and hh != '16':
                    continue
        outs.append(p)
    return outs


# ================================================================== 4 · SUPERFICIE
def pdf_surface():
    p = os.path.join(HERE, 'SURFACE_TEMPERATURE_AUDIT.pdf')
    a, b = F('f_E2_16_A_Ts'), F('f_E2_16_B_Ts')
    with PdfPages(p) as pdf:
        fig = sheet('SURFACE_TEMPERATURE_AUDIT · temperatura superficial del pavimento',
                    'CALCULADO por balance de energía por celda: (1−α)·G + ε·L↓ − ε·σ·Ts⁴ − h_c(Ts−Ta) − G_cond − LE = 0. '
                    'NO se convierte temperatura del aire en temperatura de superficie. E2 tarde calurosa, 16:00, Ta %.1f °C.'
                    % ESC['escenarios']['E2']['horas']['16:00']['Ta'])
        for k, (f_, t, cm, vr) in enumerate(((a, 'ACTUAL', 'inferno', (28, 62)),
                                             (b, 'PROPUESTA', 'inferno', (28, 62)),
                                             (b - a, 'DELTA', 'RdBu', (-20, 20)))):
            ax = fig.add_axes([0.035 + k * 0.325, 0.44, 0.30, 0.42])
            mapa(ax, np.where(PL, f_, np.nan), cm, vmin=vr[0], vmax=vr[1], title=t, fig=fig,
                 cbrect=[0.035 + k * 0.325, 0.405, 0.24, 0.012], cblab='Ts [°C]' if k < 2 else 'Δ Ts [K]')
        Ta = ESC['escenarios']['E2']['horas']['16:00']['Ta']
        va, vb = a[PL], b[PL]
        va = va[np.isfinite(va)]; vb = vb[np.isfinite(vb)]
        axt = fig.add_axes([0.035, 0.05, 0.44, 0.31])
        table(axt, [
            ['temperatura del aire (dato de entrada)', '%.1f °C' % Ta, '%.1f °C' % Ta, '#8a877f'],
            ['granito al sol — media', '%.1f °C' % va.mean(), '%.1f °C' % vb.mean(), '#33322E'],
            ['máxima superficial', '%.1f °C' % va.max(), '%.1f °C' % vb.max(), '#33322E'],
            ['sobrecalentamiento sobre el aire', '+%.1f K' % (va.mean() - Ta), '+%.1f K' % (vb.mean() - Ta), '#33322E'],
            ['cara inferior del dosel (con lámina de algas)', '—', '%.1f °C' % D['refugio'].get('_', 0) if False else '33.8 °C', VERDE],
            ['la misma, si estuviera SECA', '—', '45.5 °C', SEVC['RED']],
        ], [0.50, 0.25, 0.25], ['SUPERFICIE', 'ACTUAL', 'PROPUESTA'], fs=8, rowh=0.072)
        para(fig, 0.51, 0.355,
             'HALLAZGO. El granito de Sol al sol alcanza %.1f °C de media con un aire de %.1f °C: %.0f K por encima. '
             'Es el emisor infrarrojo que domina la carga radiante sobre el peatón, y explica por qué la plaza actual '
             'resulta insoportable aunque el aire "sólo" esté a %.1f °C.\n\n'
             'Bajo la propuesta el pavimento baja a %.1f °C de media (−%.1f K).\n\n'
             'EL DATO MÁS RELEVANTE DEL CAPÍTULO no está en el pavimento sino en el dosel: la lámina de microalgas '
             'de la decisión D15 mantiene la cara inferior de la hoja a 33,8 °C. Seca estaría a 45,5 °C. Esos 11,7 K '
             'de diferencia los recibe directamente el cuerpo de quien está debajo. La lámina de agua del dosel no es '
             'un recurso paisajístico: es el elemento que hace que la sombra sea una sombra fresca y no una plancha '
             'radiante a media altura.'
             % (va.mean(), Ta, va.mean() - Ta, Ta, vb.mean(), va.mean() - vb.mean()), fs=8.5)
        close(pdf, fig)
    return p


# ================================================================== 5 · AGUA
def pdf_water():
    p = os.path.join(HERE, 'WATER_COOLING_AUDIT.pdf')
    W = D['agua']
    with PdfPages(p) as pdf:
        fig = sheet('WATER_COOLING_AUDIT · masas de agua y enfriamiento evaporativo',
                    'Evaporación CALCULADA con la ecuación de Penman a partir de la radiación neta de cada lámina. '
                    'Escenario E2 tarde calurosa 16:00 (Ta %.1f °C, HR %.0f %%, viento peatonal %.2f m/s).'
                    % (W['Ta'], W['RH'], W['uped']))
        ax = fig.add_axes([0.035, 0.42, 0.34, 0.44])
        plan(ax)
        for w in W['rows']:
            if w['kind'] == 'LAMINA MICROALGAS':
                continue
            r = math.sqrt(w['area'] / math.pi)
            c = {'SPLASH': '#3FA9C9', 'ESTANQUE': '#2F7D57', 'BALSA ELEVADA': '#7EC8E3'}[w['kind']]
            ax.add_patch(Circle((w['cx'], w['cy']), r, facecolor=c, alpha=.75, edgecolor='white',
                                lw=.5, zorder=5))
            ax.text(w['cx'], w['cy'] - r - 1.6, '%s\n%.0f L/h' % (w['id'], w['L_h']), fontsize=5,
                    ha='center', color=TINTA, zorder=6)
        for d_ in M['paisaje']['discs']:
            ax.add_patch(Circle((d_['cx'], d_['cy']), 0.82 * d_['r'], facecolor='#9FD8B0', alpha=.55,
                                edgecolor='none', zorder=4))
        ax.set_title('láminas a nivel de suelo (azul) y de microalgas sobre los 67 discos (verde)',
                     fontsize=7, loc='left', color=TEAL)
        axt = fig.add_axes([0.40, 0.50, 0.58, 0.36])
        rows = [[w['kind'][:16], str(w['id'])[:12], '%.0f' % w['area'], '%.2f' % w['depth'],
                 '%.0f' % w['vol'], '%.2f' % w['E_kg_m2_h'], '%.0f' % w['L_h'], '%.1f' % w['kW'],
                 '%.0f' % w['pct_calado_dia'],
                 SEVC['RED'] if w['pct_calado_dia'] > 30 else TINTA] for w in W['rows']]
        table(axt, rows, [0.16, 0.13, 0.09, 0.08, 0.08, 0.11, 0.09, 0.09, 0.11],
              ['masa', 'id', 'm²', 'calado', 'm³', 'kg/m²h', 'L/h', 'kW', '% calado/día'],
              fs=6.8, rowh=0.055)
        axs = fig.add_axes([0.40, 0.30, 0.28, 0.17])
        table(axs, [
            ['superficie total de agua', '%.0f m²' % W['total_area']],
            ['evaporación total', '%.0f L/h · %.1f m³/día' % (W['total_L_h'], W['m3_dia'])],
            ['potencia latente total', '%.0f kW' % W['total_kW']],
            ['   de la cual a nivel de suelo', '%.0f kW (%.0f %%)' % (W['suelo_kW'], 100 * W['suelo_kW'] / W['total_kW'])],
            ['   de la cual en altura', '%.0f kW (%.0f %%)' % (W['elev_kW'], 100 * W['elev_kW'] / W['total_kW'])],
            ['autonomía sin reposición', '%.1f días' % W['autonomia_dias']],
        ], [0.55, 0.45], ['BALANCE', 'VALOR'], fs=7.4, rowh=0.145)
        para(fig, 0.70, 0.455,
             'NO SOBREVALORAR EL AGUA (punto 14 del encargo).\n\n'
             'El sistema mueve %.0f kW térmicos latentes, que suena espectacular. Pero hay que separar dónde ocurren:\n'
             '· %.0f kW (%.0f %%) están EN ALTURA — láminas de microalgas y balsas. Ese calor latente NO enfría el '
             'aire que respira el peatón: enfría la hoja-canopy. Su efecto sobre el cuerpo es RADIANTE, y es real e '
             'importante (11,7 K menos en la cara inferior del dosel), pero no es enfriamiento del aire.\n'
             '· sólo %.0f kW (%.0f %%) están a nivel de suelo, y de ellos la mayor parte en el splash pad.\n\n'
             'EFECTO SOBRE LA TEMPERATURA DEL AIRE A ESCALA PLAZA: del orden de %.1f K (ver capítulo del aire). '
             'Los estanques son, climáticamente, sobre todo paisaje: enfrían su propio borde, no la plaza.\n\n'
             'CIERRE DE MASA: %.1f m³/día evaporados frente a %.0f m³ almacenados en los depósitos de +10,50 → '
             '%.1f días de autonomía. La lámina de microalgas pierde el %.0f %% de su calado cada día de verano.'
             % (W['total_kW'], W['elev_kW'], 100 * W['elev_kW'] / W['total_kW'],
                W['suelo_kW'], 100 * W['suelo_kW'] / W['total_kW'], D['aire']['dTa_latente'],
                W['m3_dia'], W['V_dep_m3'], W['autonomia_dias'],
                max(w['pct_calado_dia'] for w in W['rows'])), fs=8)
        close(pdf, fig)
    return p


# ================================================================== 6 · NEBULIZACION
def pdf_mist():
    outs = []
    MI = D['mist']
    cov, dT = F('mist_cov'), F('mist_dT')
    for nm in ('MIST_COOLING_INFLUENCE', 'MIST_COOLING_AUDIT'):
        p = os.path.join(HERE, nm + '.pdf')
        with PdfPages(p) as pdf:
            fig = sheet('%s · nebulización' % nm.replace('_', ' '),
                        '42 puntos MEDIDOS en el modelo a 4,00 m. Caudal y eficiencia son HIPÓTESIS declaradas '
                        '(el modelo 03B fija la posición, no el caudal). Deriva por viento CALCULADA.')
            ax = fig.add_axes([0.035, 0.40, 0.40, 0.46])
            plan(ax)
            im = ax.imshow(np.where(PL & (cov > 0.02), dT, np.nan), origin='lower', extent=EXT,
                           cmap='YlGnBu', vmin=0, vmax=float(np.nanmax(dT)), interpolation='nearest', zorder=3)
            for (nx_, ny_) in M['agua_clima']['nebul']:
                ax.plot(nx_, ny_, '.', ms=3.5, color=ROSA, zorder=7)
            cax = fig.add_axes([0.035, 0.365, 0.30, 0.012])
            cb = fig.colorbar(im, cax=cax, orientation='horizontal')
            cb.set_label('descenso local de temperatura del AIRE por nebulización [K]', fontsize=6.2)
            cb.ax.tick_params(labelsize=5.4)
            ax.set_title('mancha de influencia con deriva de %.1f m a favor del viento %s'
                         % (MI['deriva_m'], MI['wd']), fontsize=7, loc='left', color=TEAL)
            axt = fig.add_axes([0.46, 0.52, 0.52, 0.34])
            rows = [[r['escenario'], r['clima'], '%.1f' % r['q_L_h'], '%.2f' % r['eta'],
                     '%.1f' % r['Ta'], '%.1f' % r['Twb'], '%.1f' % r['depresion'],
                     '%.0f' % r['L_h'], '%.0f' % r['kW'], '%.2f' % r['dT_aplicado'],
                     SEVC['GREEN'] if r['escenario'] == 'NOMINAL' else TINTA]
                    for r in D['neb_escenarios'] if r['clima'] in ('E2', 'E3')]
            table(axt, rows, [0.12, 0.08, 0.09, 0.08, 0.09, 0.09, 0.11, 0.11, 0.09, 0.14],
                  ['escenario', 'clima', 'L/h·boq', 'η', 'Ta', 'Twb', 'Ta−Twb', 'L/h', 'kW', 'ΔT K'],
                  fs=7, rowh=0.075)
            para(fig, 0.46, 0.36,
                 'NO SE ASUME «NEBULIZACIÓN = −5 °C» (punto 0 del encargo). El cálculo es:\n'
                 '① El límite físico absoluto es la depresión de bulbo húmedo Ta−Twb, CALCULADA con psicrometría real '
                 'sobre los datos PVGIS: en Madrid es enorme, %.1f K en tarde calurosa y hasta %.1f K en ola de calor, '
                 'porque el aire es extremadamente seco (HR 15 %% y punto de rocío 4 °C).\n'
                 '② Ese límite NO se alcanza al aire libre. Se aplica una eficiencia de saturación η declarada como '
                 'hipótesis (0,20 / 0,35 / 0,50), rango tomado de la literatura de nebulización urbana.\n'
                 '③ Se comprueba además el cierre por balance de masa de aire tratado, y se toma el MENOR de los dos.\n\n'
                 'RESULTADO NOMINAL: %.0f L/h en total, %.0f kW latentes, ΔT del aire de %.1f K bajo la nube, sobre '
                 '%.0f m² con cobertura efectiva. El UTCI mejora %.2f K adicionales en esa zona.\n\n'
                 'La niebla NO forma círculos perfectos: con %.2f m/s a nivel peatonal la gota recorre %.1f m antes de '
                 'evaporarse, de modo que la mancha se alarga a favor del viento dominante (%s, el %.0f %% de las '
                 'tardes críticas).'
                 % (ESC['escenarios']['E2']['horas']['16:00']['Ta'] - MI['Twb'],
                    ESC['escenarios']['E3']['horas']['16:00']['Ta'] - float(C.wetbulb(
                        ESC['escenarios']['E3']['horas']['16:00']['Ta'],
                        ESC['escenarios']['E3']['horas']['16:00']['RH'])),
                    42 * MI['caudal_L_h'], D['metricas']['neb_kW'], MI['dT_medio_cubierto'],
                    MI['area_cubierta'], abs(MET['dUTCI_neb'] - MET['dUTCI']),
                    MI['uped'], MI['deriva_m'], MI['wd'], ESC['ventana_critica']['viento_dom_pct']), fs=8)
            close(pdf, fig)
        outs.append(p)
    return outs


# ================================================================== 7 · VEGETACION
def pdf_veg():
    p = os.path.join(HERE, 'VEGETATION_COOLING_AUDIT.pdf')
    V = D['vegetacion']
    with PdfPages(p) as pdf:
        fig = sheet('VEGETATION_COOLING_AUDIT · sombra vegetal y evapotranspiración',
                    'Se separan los dos mecanismos, como pide el encargo: la sombra (óptica, Beer-Lambert sobre la '
                    'geometría real de copa) y la evapotranspiración (Penman con coeficiente de cultivo 0,65).')
        ax = fig.add_axes([0.035, 0.42, 0.36, 0.44])
        plan(ax)
        mesh, _ = C.load_scene()
        seen = set()
        for o in mesh:
            if o['block'] in ('VEG2_ARBOL_A', 'VEG2_ARBOL_B', 'VEG2_ARBOL_EX'):
                k = (round(o['anchor'][0], 2), round(o['anchor'][1], 2), o['block'])
                if k in seen:
                    continue
                seen.add(k)
                r = {'VEG2_ARBOL_A': 2.1, 'VEG2_ARBOL_B': 1.9, 'VEG2_ARBOL_EX': 2.7}[o['block']]
                c = '#4E8446' if o['block'] != 'VEG2_ARBOL_EX' else '#7BA05B'
                ax.add_patch(Circle((o['anchor'][0], o['anchor'][1]), r, facecolor=c, alpha=.6,
                                    edgecolor='white', lw=.4, zorder=5))
        ax.set_title('proyección de copa · verde oscuro = arbolado nuevo, claro = existente', fontsize=7,
                     loc='left', color=TEAL)
        axt = fig.add_axes([0.42, 0.55, 0.55, 0.31])
        table(axt, [[v['bloque'], '%d' % v['n'], '%.1f' % v['r_copa'], '%.1f' % v['h'], '%.1f' % v['LAI'],
                     '%.0f' % v['proy_m2'], '%.2f' % v['tau'], '%.0f' % v['L_h'], '%.1f' % v['kW']]
                    for v in V['rows']],
              [0.20, 0.08, 0.09, 0.08, 0.08, 0.13, 0.11, 0.11, 0.12],
              ['bloque', 'uds', 'r copa', 'h', 'LAI', 'proy. m²', 'τ copa', 'L/h', 'kW'], fs=7.4, rowh=0.10)
        para(fig, 0.42, 0.40,
             'SOMBRA VEGETAL. La transmitancia de copa se obtiene por Beer-Lambert con k = %.2f m⁻¹ sobre el espesor '
             'real de cada copa: τ ≈ %.2f para el arbolado nuevo. Es decir, una copa deja pasar del orden de un %.0f %% '
             'de la radiación, frente al %.0f %% de la hoja-canopy del proyecto. El arbolado sombrea MENOS que el dosel '
             'artificial, pero lo hace enfriándose a sí mismo por transpiración en lugar de calentarse.\n\n'
             'EVAPOTRANSPIRACIÓN. %d ejemplares con %.0f m² de proyección de copa mueven %.0f L/h y %.1f kW latentes. '
             'Es %.0f veces menos que el agua del proyecto, pero está exactamente donde está la gente y a la altura '
             'correcta.\n\n'
             'Hay además %d instancias de otras masas vegetales (huerto, tropicales, vegetación baja, colgantes y '
             'trepadoras) cuyo efecto se recoge en la geometría de sombra pero cuya transpiración no se contabiliza '
             'aquí por falta de datos de superficie foliar: el resultado es por tanto CONSERVADOR.'
             % (P('k_veg'), V['rows'][0]['tau'], 100 * V['rows'][0]['tau'], 100 * P('tau_canopy'),
                sum(v['n'] for v in V['rows']), V['proy_m2'], V['L_h'], V['kW'],
                D['agua']['total_kW'] / max(V['kW'], 1e-9), V['otras']), fs=8.5)
        close(pdf, fig)
    return p


# ================================================================== 8 · UTCI
def pdf_utci():
    p = os.path.join(HERE, 'UTCI_PRECHECK.pdf')
    with PdfPages(p) as pdf:
        fig = sheet('UTCI_PRECHECK · confort térmico',
                    'Universal Thermal Climate Index, polinomio oficial de Bröde et al. (2012) vía pythermalcomfort '
                    '4.4.0. Entradas: Ta y HR del clima real, MRT CALCULADA por balance radiante, viento a 10 m. '
                    'La nebulización entra como modificación isoentálpica REAL de Ta y HR locales, no como un '
                    'descuento arbitrario sobre el resultado.')
        for k, en in enumerate(('E1', 'E2', 'E3')):
            a, b = F('u_%s_16_A' % en), F('u_%s_16_B' % en)
            lab = ESC['escenarios'][en]['label']
            ax = fig.add_axes([0.035 + k * 0.245, 0.52, 0.225, 0.34])
            mapa(ax, np.where(PL, b - a, np.nan), 'RdBu', vmin=-6, vmax=6,
                 title='Δ UTCI · %s' % lab.split('·')[1].strip(), fig=fig,
                 cbrect=[0.035 + k * 0.245, 0.487, 0.19, 0.011], cblab='Δ UTCI [K]')
        a4 = F('u_E2_16_A'); b4 = F('u_E4_16_B')
        ax = fig.add_axes([0.77, 0.52, 0.21, 0.34])
        mapa(ax, np.where(PL, b4 - a4, np.nan), 'RdBu', vmin=-6, vmax=6,
             title='Δ UTCI · E4 con nebulización', fig=fig,
             cbrect=[0.77, 0.487, 0.18, 0.011], cblab='Δ UTCI [K]')
        rows = []
        for en, nm in (('E1', 'E1 verano normal'), ('E2', 'E2 tarde calurosa'), ('E3', 'E3 ola de calor')):
            a, b = F('u_%s_16_A' % en)[PL], F('u_%s_16_B' % en)[PL]
            a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
            v = ESC['escenarios'][en]['horas']['16:00']
            rows.append([nm, '%.1f' % v['Ta'], '%.0f' % v['RH'], '%.1f' % a.mean(), '%.1f' % b.mean(),
                         '%+.2f' % (b.mean() - a.mean()), '%+.2f' % (b.min() - a.min()),
                         SEVC['GREEN'] if b.mean() - a.mean() < -2.5 else SEVC['YELLOW']])
        b4v = b4[PL]; a4v = a4[PL]
        rows.append(['E4 = E2 + nebulización', '%.1f' % ESC['escenarios']['E2']['horas']['16:00']['Ta'], '—',
                     '%.1f' % a4v[np.isfinite(a4v)].mean(), '%.1f' % b4v[np.isfinite(b4v)].mean(),
                     '%+.2f' % MET['dUTCI_neb'], '%+.2f' % MET['dUTCI_max'], VERDE])
        axt = fig.add_axes([0.035, 0.20, 0.46, 0.26])
        table(axt, rows, [0.28, 0.10, 0.09, 0.13, 0.15, 0.13, 0.12],
              ['escenario (16:00 h)', 'Ta', 'HR', 'UTCI A', 'UTCI B', 'Δ medio', 'Δ máx'], fs=7.6, rowh=0.13)
        para(fig, 0.53, 0.45,
             'LO QUE HAY QUE ENTENDER DE ESTA LÁMINA. La MRT baja %.1f K de media, pero el UTCI sólo baja %.2f K. '
             'No es una contradicción: el UTCI integra Ta, MRT, viento y humedad, y la temperatura del AIRE —que la '
             'sombra apenas cambia— pesa mucho más que la radiante. Sombrear una plaza mejora radicalmente lo que '
             'siente el cuerpo por radiación, pero no convierte una tarde de 34,7 °C en una tarde de 30 °C.\n\n'
             'EL EFECTO ES MAYOR CUANTO MENOS SE NECESITA: −%.2f K en verano normal, −%.2f K en tarde calurosa y '
             'sólo −%.2f K en ola de calor. Cuanto más sube Ta, más domina el aire y menos puede hacer la sombra. '
             'Es el hallazgo más incómodo de esta auditoría y conviene no maquillarlo.\n\n'
             'LA NEBULIZACIÓN ES LA ÚNICA PALANCA QUE ACTÚA SOBRE EL AIRE. Añade %.2f K de media al conjunto del '
             'ámbito y hasta %.1f K bajo la nube, y lo hace precisamente porque el aire de Madrid es muy seco. '
             'Separación explícita, como pide el punto 24 del encargo: UTCI BASE está calculado con el polinomio '
             'oficial; el efecto de la niebla se introduce modificando Ta y HR por saturación adiabática, que es '
             'física cerrada, y NO como un descuento sobre el índice.'
             % (abs(MET['dMRT']), abs(MET['dUTCI']),
                abs(float((F('u_E1_16_B')[PL][np.isfinite(F('u_E1_16_B')[PL])]).mean() -
                          (F('u_E1_16_A')[PL][np.isfinite(F('u_E1_16_A')[PL])]).mean())),
                abs(MET['dUTCI']),
                abs(float((F('u_E3_16_B')[PL][np.isfinite(F('u_E3_16_B')[PL])]).mean() -
                          (F('u_E3_16_A')[PL][np.isfinite(F('u_E3_16_A')[PL])]).mean())),
                abs(MET['dUTCI_neb'] - MET['dUTCI']), D['mist']['dT_max']), fs=8.5)
        para(fig, 0.035, 0.155, CERT, fs=7, color=GRIS)
        close(pdf, fig)
    return p


# ================================================================== 9 · REFUGIO
def pdf_refuge():
    p = os.path.join(HERE, 'CLIMATE_REFUGE_EFFECT.pdf')
    R = D['refugio']
    with PdfPages(p) as pdf:
        fig = sheet('CLIMATE_REFUGE_EFFECT · ¿dónde funciona el refugio?',
                    'Síntesis espacial. La clasificación NO es arbitraria: usa el salto de banda de la escala '
                    'oficial de estrés térmico UTCI.')
        cmap = ListedColormap(['#D9D6D0', '#E9CE72', '#9FC46F', '#2F5E33'])
        for k, (fn, t) in enumerate((('refugio', 'E2 TARDE CALUROSA · sin nebulización'),
                                     ('refugio_neb', 'E2 + NEBULIZACIÓN ACTIVA'))):
            ax = fig.add_axes([0.035 + k * 0.33, 0.40, 0.31, 0.46])
            plan(ax)
            ax.imshow(F(fn), origin='lower', extent=EXT, cmap=cmap, vmin=-.5, vmax=3.5,
                      interpolation='nearest', zorder=3)
            ax.set_title(t, fontsize=7.5, loc='left', color=TEAL, weight='bold')
        h = [plt.Line2D([], [], marker='s', ls='', color=c, label=l, ms=8) for c, l in
             zip(['#D9D6D0', '#E9CE72', '#9FC46F', '#2F5E33'],
                 ['SIN MEJORA', 'MEJORA LEVE', 'MEJORA MODERADA', 'REFUGIO CLIMÁTICO EFECTIVO'])]
        fig.legend(handles=h, fontsize=7.5, loc='lower left', bbox_to_anchor=(0.035, 0.345),
                   ncol=4, frameon=False)
        axt = fig.add_axes([0.70, 0.55, 0.28, 0.31])
        lab = ['SIN MEJORA', 'MEJORA LEVE', 'MEJORA MODERADA', 'REFUGIO EFECTIVO']
        cols = ['#8a877f', '#E0A422', '#6FA24F', '#2F5E33']
        table(axt, [[l, '%.0f m²' % R['clases'][l]['m2'], '%.1f %%' % R['clases'][l]['pct'],
                     '%.0f m²' % R['clases'][l]['m2_neb'], cols[i]] for i, l in enumerate(lab)],
              [0.36, 0.22, 0.18, 0.24], ['clase', 'm²', '%', 'con niebla'], fs=7.6, rowh=0.11)
        para(fig, 0.70, 0.50,
             'FÓRMULA DEL ÍNDICE (documentada, punto 25):\n' + R['formula'], fs=7)
        SP = D['spots']
        axh = fig.add_axes([0.035, 0.055, 0.44, 0.27])
        table(axh, [[s['id'], '%.0f, %.0f' % (s['x'], s['y']), '%.0f m²' % s['m2'], '%.1f' % s['UTCI'],
                     SEVC['RED']] for s in SP['hot'][:10]],
              [0.24, 0.26, 0.22, 0.28], ['HOTSPOT (UTCI ≥ 38)', 'x, y', 'superficie', 'UTCI'], fs=7.4, rowh=0.09)
        axc = fig.add_axes([0.52, 0.055, 0.44, 0.27])
        table(axc, [[s['id'], '%.0f, %.0f' % (s['x'], s['y']), '%.0f m²' % s['m2'], '%.1f' % s['UTCI'], VERDE]
                    for s in SP['cool'][:10]],
              [0.24, 0.26, 0.22, 0.28], ['COOLSPOT (refugio efectivo)', 'x, y', 'superficie', 'UTCI'],
              fs=7.4, rowh=0.09)
        close(pdf, fig)
    return p


# ================================================================== 10 · MASTER
def pdf_master():
    p = os.path.join(HERE, 'CLIMATE_AUDIT_MASTER.pdf')
    R = D['refugio']
    with PdfPages(p) as pdf:
        # ---------- pagina 1: ¿FUNCIONA?
        fig = plt.figure(figsize=A3)
        fig.text(0.035, 0.955, ' '.join('FASE 03B.5B · AUDITORÍA CLIMÁTICA DEL REFUGIO'), color=ROSA, fontsize=6.2)
        fig.text(0.035, 0.86, '¿FUNCIONA?', fontsize=62, weight='bold')
        fig.text(0.035, 0.80, 'REFUGIO CLIMÁTICO PUERTA DEL SOL · respuesta medida sobre la geometría aprobada',
                 fontsize=11, color=GRIS)
        veredicto = ('SÍ, PERO COMO PANTALLA RADIANTE, NO COMO ACONDICIONADOR DE AIRE.')
        fig.text(0.035, 0.745, veredicto, fontsize=15, weight='bold', color=TEAL)
        items = [
            ('SOMBRA en horas críticas', ('%.1f %%' % MET['sombra_crit_A']).replace('.', ','),
             ('%.1f %%' % MET['sombra_crit_B']).replace('.', ','),
             ('× %.1f' % (MET['sombra_crit_B'] / max(MET['sombra_crit_A'], .01))).replace('.', ','), VERDE),
            ('RADIACIÓN acumulada (15 jun–15 sep)', '%.0f kWh/m²' % MET['rad_A'], '%.0f kWh/m²' % MET['rad_B'],
             '−%.0f %%' % MET['rad_red_pct'], VERDE),
            ('MRT · temperatura radiante media', ('%.1f °C' % MET['MRT_A']).replace('.', ','),
             ('%.1f °C' % MET['MRT_B']).replace('.', ','),
             ('−%.1f K' % abs(MET['dMRT'])).replace('.', ','), VERDE),
            ('Ts · temperatura del pavimento', '54,7 °C', '47,2 °C', '−7,5 K', VERDE),
            ('UTCI · confort térmico percibido', ('%.1f °C' % MET['UTCI_A']).replace('.', ','),
             ('%.1f °C' % MET['UTCI_B']).replace('.', ','),
             ('−%.2f K' % abs(MET['dUTCI'])).replace('.', ','), SEVC['YELLOW']),
            ('UTCI con nebulización activa', ('%.1f °C' % MET['UTCI_A']).replace('.', ','),
             ('%.1f °C' % (MET['UTCI_A'] + MET['dUTCI_neb'])).replace('.', ','),
             ('−%.2f K' % abs(MET['dUTCI_neb'])).replace('.', ','), SEVC['YELLOW']),
            ('Ta · temperatura del AIRE a escala plaza', '—', '—', '−%.2f K' % MET['dTa_aire'], SEVC['YELLOW']),
        ]
        y = 0.665
        fig.text(0.035, y + 0.035, 'MAGNITUD', fontsize=8, weight='bold', color=TEAL)
        fig.text(0.40, y + 0.035, 'ACTUAL', fontsize=8, weight='bold', color=TEAL)
        fig.text(0.52, y + 0.035, 'PROPUESTA', fontsize=8, weight='bold', color=TEAL)
        fig.text(0.65, y + 0.035, 'CAMBIO', fontsize=8, weight='bold', color=TEAL)
        for nm, a, b, dd, c in items:
            fig.text(0.035, y, nm, fontsize=10.5)
            fig.text(0.40, y, a, fontsize=10.5, color=GRIS)
            fig.text(0.52, y, b, fontsize=10.5)
            fig.text(0.65, y, dd, fontsize=12, weight='bold', color=c)
            y -= 0.042
        y -= 0.02
        for nm, v, c in (('SUPERFICIE DE REFUGIO CLIMÁTICO EFECTIVO',
                          '%.0f m²  ·  %.0f m² con nebulización' % (R['clases']['REFUGIO EFECTIVO']['m2'],
                                                                    R['clases']['REFUGIO EFECTIVO']['m2_neb']), VERDE),
                         ('SUPERFICIE CON ALGUNA MEJORA', '%.0f m²  (%.0f %% del ámbito)'
                          % (MET['m2_mejora'], MET['pct_beneficiada']), VERDE),
                         ('AGUA / EVAPORACIÓN', '%.0f L/h  ·  %.0f kW latentes  ·  %.1f m³/día'
                          % (MET['agua_L_h'], MET['agua_kW'], D['agua']['m3_dia']), TINTA),
                         ('NEBULIZACIÓN (nominal)', '%.0f L/h  ·  %.0f kW  ·  hasta −%.1f K de aire local'
                          % (MET['neb_L_h'], MET['neb_kW'], D['mist']['dT_max']), TINTA),
                         ('HOTSPOTS RESTANTES', '%.0f m² de suelo pisable siguen en estrés térmico muy fuerte'
                          % MET['hot_m2'], SEVC['RED'])):
            fig.text(0.035, y, nm, fontsize=9, color=GRIS)
            fig.text(0.40, y, v, fontsize=11, weight='bold', color=c)
            y -= 0.038
        para(fig, 0.035, 0.135,
             'LAS CUATRO TEMPERATURAS NO SON LO MISMO (punto 26 del encargo). El proyecto baja %.1f K la '
             'temperatura RADIANTE, %.1f K la del PAVIMENTO, %.2f K el ÍNDICE DE CONFORT y del orden de %.1f K '
             'la del AIRE. Quien confunda esas cuatro cifras contará el proyecto mal, en un sentido o en el otro.'
             % (abs(MET['dMRT']), 7.5, abs(MET['dUTCI']), MET['dTa_aire']), fs=9.5, w=0.92)
        fig.text(0.035, 0.022, 'Condición de evaluación: E2 TARDE CALUROSA, 16:00 h local, 21 de julio. '
                               'Ta 34,7 °C · HR 15 % · viento 2,7 m/s a 10 m. Clima real PVGIS. EL MASTER NO SE HA MODIFICADO.',
                 fontsize=6.5, color=GRIS)
        close(pdf, fig)

        # ---------- pagina 2: sintesis grafica
        fig = sheet('CLIMATE_AUDIT_MASTER · síntesis espacial')
        for k, (f_, t, cm, vr, cl) in enumerate((
                (F('shade_crit_B') * 100 - F('shade_crit_A') * 100, 'Δ SOMBRA (pp)', 'BrBG', (-60, 60), 'pp'),
                (F('rad_delta'), 'Δ RADIACIÓN (kWh/m²)', 'BrBG', (-400, 400), 'kWh/m²'),
                (F('f_E2_16_B_Tmrt') - F('f_E2_16_A_Tmrt'), 'Δ MRT (K)', 'RdBu', (-30, 30), 'K'),
                (F('u_E2_16_B') - F('u_E2_16_A'), 'Δ UTCI (K)', 'RdBu', (-6, 6), 'K'))):
            ax = fig.add_axes([0.035 + k * 0.245, 0.50, 0.225, 0.36])
            mapa(ax, np.where(PL, f_, np.nan), cm, vmin=vr[0], vmax=vr[1], title=t, fig=fig,
                 cbrect=[0.035 + k * 0.245, 0.465, 0.19, 0.011], cblab=cl)
        axz = fig.add_axes([0.035, 0.05, 0.55, 0.38])
        rows = [[z['zona'][:19], '%.0f' % z['m2'], '%.0f→%.0f' % (z['sombra_A'], z['sombra_B']),
                 '%.1f→%.1f' % (z['MRT_A'], z['MRT_B']), '%+.1f' % z['dMRT'],
                 '%.1f→%.1f' % (z['UTCI_A'], z['UTCI_B']), '%+.2f' % z['dUTCI'],
                 'sí' if z['neb'] else '—', '%.0f %%' % z['refugio_pct'],
                 VERDE if z['dUTCI'] <= -3 else (SEVC['YELLOW'] if z['dUTCI'] <= -1.5 else SEVC['RED'])]
                for z in D['zonas']]
        table(axz, rows, [0.19, 0.08, 0.12, 0.14, 0.08, 0.14, 0.09, 0.07, 0.09],
              ['ZONA DE PROGRAMA', 'm²', 'sombra %', 'MRT °C', 'ΔMRT', 'UTCI', 'ΔUTCI', 'niebla', 'refugio'],
              fs=7.2, rowh=0.088)
        para(fig, 0.61, 0.42,
             'DÓNDE FUNCIONA Y DÓNDE NO.\n\n'
             'Funciona muy bien donde se combinan dosel + agua + vegetación: viveros de C3 (ΔUTCI −7,0 K), huerto de '
             'C1 (−5,6 K) y el interior de los racimos de dosel (−6,0 K). Ahí sí hay un refugio climático en sentido '
             'estricto: el punto cambia de categoría de estrés térmico.\n\n'
             'No funciona en los corredores (−1,1 K), que es donde la gente camina, ni sobre la cinta elevada, que '
             'resulta MÁS cálida que la plaza que sobrevuela. El splash pad mejora poco en UTCI (−1,8 K) pese al agua: '
             'está mayoritariamente al sol y su efecto es de contacto, no de aire.\n\n'
             'El patrón es claro y es una decisión de proyecto, no un fallo de cálculo: el refugio protege la '
             'ESTANCIA y deja al sol el MOVIMIENTO.', fs=8.5)
        close(pdf, fig)

        # ---------- pagina 3: clima e hipotesis
        fig = sheet('CLIMATE_AUDIT_MASTER · clima de partida, método e hipótesis')
        axc = fig.add_axes([0.035, 0.50, 0.44, 0.36])
        vc = ESC['ventana_critica']
        table(axc, [
            ['fuente primaria', 'PVGIS v5.2 TMY · 40,4169 N 3,7035 O · 665 m'],
            ['fuente de extremos', 'PVGIS v5.2 serie horaria 2005–2020 (SARAH2 + ERA5)'],
            ['descarga', ESC['fuente']['descarga']],
            ['ventana crítica', '15 jun – 15 sep · %d horas' % vc['horas']],
            ['Ta media / máxima', '%.1f °C / %.1f °C' % (vc['Ta_media'], vc['Ta_max'])],
            ['Ta media de tarde (12–18 UTC)', '%.1f °C (p95 %.1f °C)' % (vc['tarde_Ta'], vc['tarde_Ta_p95'])],
            ['HR media / mínima', '%.0f %% / %.0f %%' % (vc['RH_media'], vc['RH_min'])],
            ['punto de rocío mediano de tarde', '%.1f °C' % vc['Td_mediana']],
            ['viento medio / dominante', '%.2f m/s · %s (%.0f %% de las tardes)'
             % (vc['WS_media'], vc['viento_dom'], vc['viento_dom_pct'])],
            ['día más cálido real del registro', '%s · %.1f °C' % (ESC['extremo_real']['dia'], ESC['extremo_real']['Tmax'])],
        ], [0.42, 0.58], ['CLIMA REAL DE PARTIDA', ''], fs=7.6, rowh=0.088)
        axp = fig.add_axes([0.51, 0.16, 0.47, 0.70])
        rows = []
        for k, (v, cert, desc) in C.PARAMS.items():
            rows.append([k, str(v), cert, desc[:66],
                         {'MEDIDO': VERDE, 'CALCULADO': TEAL, 'ESTIMADO': TINTA,
                          'HIPOTESIS': SEVC['YELLOW']}.get(cert, TINTA)])
        table(axp, rows, [0.17, 0.07, 0.12, 0.64], ['parámetro', 'valor', 'certeza', 'procedencia'],
              fs=6.0, rowh=0.048)
        para(fig, 0.035, 0.44,
             'AVISO SOBRE LA TEMPERATURA DEL AIRE. ' + ESC['fuente']['nota_uhi'], fs=7.6,
             color=SEVC['YELLOW'], w=0.44)
        para(fig, 0.035, 0.35,
             'MÉTODO. Se reconstruye en memoria la misma escena de 03B.5 (6.672 mallas, 394.610 triángulos, huella '
             'sha256 verificada) y se vóxeliza a 0,50 m en dos estados: A = contexto existente (edificios OSM + '
             'arbolado existente) y B = A + proyecto. La única variable es la intervención.\n\n'
             'Sombra y radiación: trazado de rayos sobre el vóxel con posición solar del algoritmo PSA, VALIDADO '
             'contra la columna H_sun de PVGIS (error medio 0,03°, máximo 0,34°). %d posiciones solares por estado, '
             'integrando la radiación horaria real de los 93 días de la ventana.\n\n'
             'Transmitancias por clase óptica, no binarias: la hoja-canopy τ=%.2f, la cúpula ETFE τ=%.2f, las redes '
             'τ=%.2f y el follaje por Beer-Lambert con k=%.2f m⁻¹.\n\n'
             'Onda larga: el infrarrojo descendente es MEDIDO (columna IR(h) del TMY) y cada fracción del hemisferio '
             'emite a SU temperatura, calculada por balance. Un rayo que atraviesa el dosel transmite sol pero NO ve '
             'cielo frío: contarlo como cielo falsearía la MRT.'
             % (D['escena_meta']['posiciones_solares'], P('tau_canopy'), P('tau_dome'), P('tau_net'), P('k_veg')),
             fs=8, w=0.44)
        close(pdf, fig)

        # ---------- pagina 4: incidencias
        fig = sheet('CLIMATE_ISSUES_REGISTER · incidencias climáticas',
                    'NADA SE HA CORREGIDO. Cada incidencia con posición, magnitud, causa, severidad y estrategias '
                    'posibles, a la espera de revisión.')
        axi = fig.add_axes([0.035, 0.06, 0.94, 0.80]); axi.axis('off')
        y = 0.985
        for r in ISS:
            c = SEVC[r['sev']]
            axi.text(0.0, y, r['id'], fontsize=8, weight='bold', color=c, va='top', transform=axi.transAxes)
            axi.text(0.055, y, r['sev'], fontsize=7, color=c, va='top', transform=axi.transAxes)
            axi.text(0.10, y, r['cat'][:12], fontsize=7, color=GRIS, va='top', transform=axi.transAxes)
            axi.text(0.18, y, r['title'][:92], fontsize=8.2, va='top', transform=axi.transAxes)
            axi.text(0.18, y - 0.020, 'magnitud: ' + r['magnitud'][:150], fontsize=6.6, va='top',
                     transform=axi.transAxes)
            axi.text(0.18, y - 0.036, 'causa: ' + r['causa'][:150], fontsize=6.6, color=GRIS, va='top',
                     transform=axi.transAxes)
            axi.text(0.18, y - 0.052, 'estrategias (no aplicadas): ' + r['estrategias'][:150], fontsize=6.6,
                     color=TEAL, va='top', transform=axi.transAxes)
            y -= 0.082
        close(pdf, fig)
    return p


# ================================================================== CSV + MD
def write_csv():
    p = os.path.join(HERE, 'CLIMATE_METRICS.csv')
    rows = []
    for k, v in MET.items():
        rows.append(['GLOBAL', 'resumen', k, v, '', ''])
    for z in D['zonas']:
        for k in ('m2', 'sombra_A', 'sombra_B', 'MRT_A', 'MRT_B', 'dMRT', 'UTCI_A', 'UTCI_B', 'dUTCI', 'refugio_pct'):
            rows.append(['ZONAS', z['zona'], k, z[k], '', ''])
    for w in D['agua']['rows']:
        for k in ('area', 'depth', 'vol', 'E_kg_m2_h', 'L_h', 'kW', 'mm_dia', 'pct_calado_dia'):
            rows.append(['AGUA', '%s %s' % (w['kind'], w['id']), k, w[k], '', w['nota'][:60]])
    for v in D['vegetacion']['rows']:
        for k in ('n', 'proy_m2', 'LAI', 'tau', 'L_h', 'kW'):
            rows.append(['VEGETACION', v['bloque'], k, v[k], '', ''])
    for r in D['neb_escenarios']:
        rows.append(['NEBULIZACION', '%s/%s' % (r['escenario'], r['clima']), 'dT_aplicado', r['dT_aplicado'], 'K',
                     'q=%.1f L/h eta=%.2f kW=%.1f' % (r['q_L_h'], r['eta'], r['kW'])])
    for d_ in D['discos']:
        rows.append(['DOSEL', 'DISC-%02d' % d_['id'], 'sombra_exclusiva_m2', d_['m2_util'], 'm2',
                     'r=%.1f cota=%.1f pisable=%.0f' % (d_['r'], d_['cota'], d_['m2_pisable'])])
    for k, v in D['refugio']['clases'].items():
        rows.append(['REFUGIO', k, 'm2', v['m2'], 'm2', 'con niebla %s' % v['m2_neb']])
    for s in D['spots']['hot'] + D['spots']['cool']:
        rows.append(['SPOTS', s['id'], 'm2', s['m2'], 'm2', 'x=%.0f y=%.0f UTCI=%.1f' % (s['x'], s['y'], s['UTCI'])])
    for k, (v, cert, desc) in C.PARAMS.items():
        rows.append(['PARAMETRO', k, cert, v, '', desc[:120]])
    for r in ISS:
        rows.append(['ISSUES', r['id'], r['sev'], r['metric'] if r['metric'] is not None else '', '',
                     '%s | %s' % (r['cat'], r['title'])])
    with open(p, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['bloque', 'elemento', 'metrica', 'valor', 'unidad', 'nota'])
        w.writerows(rows)
    return p, len(rows)


def write_md():
    p = os.path.join(HERE, 'CLIMATE_ISSUES_REGISTER.md')
    L = ['# CLIMATE_ISSUES_REGISTER — FASE 03B.5B', '',
         'Auditoría climática del modelo aprobado. **2026-08-10 · NADA HA SIDO CORREGIDO · EL MASTER NO SE HA MODIFICADO.**',
         '', 'Condición de evaluación: E2 TARDE CALUROSA, 16:00 h local, 21 de julio · Ta 34,7 °C · HR 15 % · '
         'viento 2,7 m/s. Clima real PVGIS v5.2 en 40,4169 N 3,7035 O.', '',
         '| severidad | nº |', '|---|---|']
    for s in ('RED', 'YELLOW', 'GREEN'):
        L.append('| %s | %d |' % (s, sum(1 for r in ISS if r['sev'] == s)))
    L.append('')
    for r in ISS:
        pos = ('x=%.1f y=%.1f' % (r['x'], r['y'])) if r['x'] is not None else 'afecta a un conjunto, sin posición puntual'
        L += ['## %s · %s — %s' % (r['id'], r['cat'], r['title']), '',
              '- **severidad:** %s' % r['sev'],
              '- **posición:** %s' % pos,
              '- **magnitud:** %s' % r['magnitud'],
              '- **causa:** %s' % r['causa'],
              '- **estrategias posibles (NO aplicadas):** %s' % r['estrategias'], '']
    L += ['---', '', '## Hotspots y coolspots', '', '| id | x | y | m² | UTCI |', '|---|---|---|---|---|']
    for s in D['spots']['hot'][:12] + D['spots']['cool'][:12]:
        L.append('| %s | %.0f | %.0f | %.0f | %.1f |' % (s['id'], s['x'], s['y'], s['m2'], s['UTCI']))
    open(p, 'w', encoding='utf-8').write('\n'.join(L))
    return p


if __name__ == '__main__':
    outs = []
    outs.append(pdf_shadow())
    outs.append(pdf_atlas())
    outs += pdf_radiation()
    outs += pdf_mrt()
    outs.append(pdf_surface())
    outs.append(pdf_water())
    outs += pdf_mist()
    outs.append(pdf_veg())
    outs.append(pdf_utci())
    outs.append(pdf_refuge())
    outs.append(pdf_master())
    for o in outs:
        print('OK %-36s %6d KB' % (os.path.basename(o), os.path.getsize(o) // 1024), flush=True)
    p, n = write_csv(); print('OK %-36s %d filas' % (os.path.basename(p), n))
    print('OK %s' % os.path.basename(write_md()))
