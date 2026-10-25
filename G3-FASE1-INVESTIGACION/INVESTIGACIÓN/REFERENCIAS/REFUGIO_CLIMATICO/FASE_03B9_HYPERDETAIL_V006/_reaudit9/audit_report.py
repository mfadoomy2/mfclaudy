# -*- coding: utf-8 -*-
"""
FASE 03B.5 â€” generacion de documentos de auditoria.
Lee _data/*.json + *.npy y produce los 8 PDF + CSV + ISSUES_REGISTER.md.
"""
import csv
import json
import math
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Polygon as MPoly, Rectangle, Circle

import audit_core as C
from audit_core import CELL, DATA, HERE

A3 = (16.54, 11.69)          # A3 apaisado
ROSA, VERDE, TEAL = '#D6577F', '#4E8446', '#2E6E6B'
GRIS, TINTA = '#8a877f', '#33322E'
SEVC = {'RED': '#C8322B', 'YELLOW': '#E0A422', 'GREEN': '#4E8446'}
DOT = {'RED': 'â— RED', 'YELLOW': 'â— YELLOW', 'GREEN': 'â— GREEN'}   # DejaVu no trae los emoji
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8,
                     'axes.edgecolor': GRIS, 'axes.labelcolor': TINTA,
                     'text.color': TINTA, 'xtick.color': GRIS, 'ytick.color': GRIS,
                     'axes.linewidth': 0.5, 'pdf.fonttype': 42})

# ------------------------------------------------------------------ datos
D = {n: C.jload(n) for n in ('a1_paths.json', 'a2_clear.json', 'a2_cables.json', 'a3_heights.json',
                             'a4_ribbon.json', 'a5_access.json', 'a6_metro.json', 'a7_views.json',
                             'a8_density.json', 'a9_maint.json', 'a10_collisions.json',
                             'a11_person.json', 'issues.json', 'summary.json')}
ISSUES = D['issues.json']
SUM = D['summary.json']
OCC = np.load(os.path.join(DATA, 'occ.npy'))
WALK = np.load(os.path.join(DATA, 'walk.npy'))
PLAZA = np.load(os.path.join(DATA, 'plaza.npy'))
WIDTH = np.load(os.path.join(DATA, 'width.npy'))
CLEAR = np.load(os.path.join(DATA, 'clear.npy'))
GRID = C.Grid(-112, -45, 100, 78)
EXT = GRID.extent()
M = json.load(open(os.path.join(C.F03B, 'geometria_maestra_v006.json'), encoding='utf-8'))
CC = M['contexto']['casa_correos']

_SCENE = {}


def scene():
    if 'objs' not in _SCENE:
        o, m, b = C.load_scene()
        _SCENE['objs'] = [q for q in o if q['kind'] == 'mesh']
        for q in _SCENE['objs']:
            q['fam'] = C.obj_family(q)
            q['bb'] = (q['V'].min(0), q['V'].max(0))
    return _SCENE['objs']


# ------------------------------------------------------------------ helpers de lamina
def sheet(pdf, title, kicker='FASE 03B.5 Â· AUDITORÃA GEOMÃ‰TRICA Y DE VIABILIDAD', sub=''):
    fig = plt.figure(figsize=A3)
    fig.text(0.035, 0.955, ' '.join(kicker), color=ROSA, fontsize=6.2)
    fig.text(0.035, 0.925, title, fontsize=19, weight='bold')
    if sub:
        fig.text(0.035, 0.902, sub, fontsize=8.5, color=GRIS)
    fig.text(0.035, 0.022, 'REFUGIO CLIMÃTICO PUERTA DEL SOL Â· MASTER_ARCHITECTURE_v002 / SOL_FULL_SCENE_v001 Â· '
                           'mediciÃ³n sobre la geometrÃ­a aprobada Â· 2026-08-10 Â· EL MASTER NO SE HA MODIFICADO',
             fontsize=6.5, color=GRIS)
    return fig


def close(pdf, fig):
    pdf.savefig(fig); plt.close(fig)


def context_plan(ax, buildings=True, extent=None, lw=0.4):
    ax.set_facecolor('white')
    if buildings:
        for b in M['contexto']['buildings']:
            if len(b['pts']) < 3:
                continue
            xs = [p[0] for p in b['pts']]; ys = [p[1] for p in b['pts']]
            if max(xs) < -125 or min(xs) > 115 or max(ys) < -60 or min(ys) > 95:
                continue
            ax.add_patch(MPoly([(p[0], p[1]) for p in b['pts']], closed=True,
                               facecolor='#EDEBE6', edgecolor='#CFCBC2', lw=lw, zorder=1))
        ax.add_patch(MPoly([(p[0], p[1]) for p in CC['pts']], closed=True,
                           facecolor='#E4D6CE', edgecolor='#B08968', lw=0.8, zorder=2))
    e = extent or (-112, 100, -45, 78)
    ax.set_xlim(e[0], e[1]); ax.set_ylim(e[2], e[3])
    ax.set_aspect('equal'); ax.tick_params(labelsize=6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def table(ax, rows, colw, header=None, fs=7.2, rowh=0.032, y0=0.97, hcolor=TEAL):
    ax.axis('off')
    y = y0
    if header:
        x = 0.0
        for t, w in zip(header, colw):
            ax.text(x, y, t, fontsize=fs, weight='bold', color=hcolor, va='top',
                    transform=ax.transAxes)
            x += w
        y -= rowh * 1.15
        ax.plot([0, sum(colw)], [y + rowh * 0.35] * 2, color=GRIS, lw=0.4, transform=ax.transAxes)
    for r in rows:
        x = 0.0
        col = r[-1] if isinstance(r[-1], str) and r[-1].startswith('#') else None
        cells = r[:-1] if col else r
        for t, w in zip(cells, colw):
            ax.text(x, y, str(t), fontsize=fs, va='top', color=col or TINTA,
                    transform=ax.transAxes)
            x += w
        y -= rowh
        if y < 0.02:
            break
    return y


def para(fig, x, y, txt, w=0.42, fs=8, color=TINTA, weight='normal'):
    fig.text(x, y, txt, fontsize=fs, color=color, va='top', wrap=True, weight=weight,
             linespacing=1.45)


# ------------------------------------------------------------------ seccion automatica
def draw_section(ax, axis, val, half=6.0, xr=None, zr=(0, 12), person_at=None, title=''):
    """Corte real del modelo: axis 'x' o 'y' en la cota val; dibuja (eje libre, z)."""
    objs = scene()
    ai = 0 if axis == 'x' else 1
    hi = 1 - ai
    FAMC = {'STRUCTURE': '#A87840', 'CANOPY': '#7E9B46', 'PODS': '#D6577F', 'VEGETATION': '#4E8446',
            'WATER': '#2F7D57', 'PLANTER': '#4E7040', 'FURNITURE': '#8A5A2B', 'RIBBON': '#8A5A2B',
            'CONTEXT': '#C3BFB7', 'PEOPLE': '#33322E', 'MIST': '#8FC7AE'}
    segs = {}
    for o in objs:
        if o['layer'] in ('12_MIST',):
            continue
        bb0, bb1 = o['bb']
        if bb1[ai] < val or bb0[ai] > val:
            continue
        T = C.tris_of(o)
        a = T[:, :, ai]
        cross = (a.min(1) <= val) & (a.max(1) >= val)
        if not cross.any():
            continue
        col = FAMC.get(o['fam'], GRIS)
        L = segs.setdefault(col, [])
        for t in T[cross]:
            pts = []
            for k in range(3):
                p, q = t[k], t[(k + 1) % 3]
                if (p[ai] - val) * (q[ai] - val) <= 0 and abs(q[ai] - p[ai]) > 1e-12:
                    f = (val - p[ai]) / (q[ai] - p[ai])
                    if -1e-9 <= f <= 1 + 1e-9:
                        pts.append((p[hi] + (q[hi] - p[hi]) * f, p[2] + (q[2] - p[2]) * f))
            if len(pts) >= 2:
                L.append([pts[0], pts[1]])
    from matplotlib.collections import LineCollection
    for col, L in segs.items():
        ax.add_collection(LineCollection(L, colors=col, linewidths=0.45, alpha=0.95))
    for z, lab in ((0, 'Â±0.00'), (2.10, '+2.10 cabeza'), (3.0, '+3.00 gÃ¡libo mÃ­n.'),
                   (5.0, '+5.00'), (6.0, '+6.00 cinta'), (6.75, '+6.75'), (8.5, '+8.50'), (10.5, '+10.50')):
        if zr[0] <= z <= zr[1]:
            ax.axhline(z, color=TEAL, lw=0.3, ls=(0, (6, 4)), alpha=0.55, zorder=0)
            ax.text(xr[1] - 0.4 if xr else 0, z + 0.08, lab, fontsize=5.4, color=TEAL, ha='right')
    if person_at is not None:
        px = person_at
        ax.add_patch(Rectangle((px - 0.14, 0), 0.28, 1.45, facecolor='#33322E', alpha=0.85, zorder=6))
        ax.add_patch(Circle((px, 1.58), 0.12, facecolor='#33322E', alpha=0.85, zorder=6))
        ax.plot([px - 0.9, px + 0.9], [1.70, 1.70], color='#33322E', lw=0.5, ls=':', zorder=6)
        ax.text(px + 0.22, 1.74, '1.70', fontsize=5.5, color='#33322E')
    if xr:
        ax.set_xlim(*xr)
    ax.set_ylim(*zr); ax.set_aspect('equal')
    ax.tick_params(labelsize=5.5)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    if title:
        ax.set_title(title, fontsize=7, loc='left', color=TEAL)


# ================================================================== 1 Â· PATH_WIDTH_MAP
def pdf_paths():
    A1 = D['a1_paths.json']
    out = os.path.join(HERE, 'PATH_WIDTH_MAP.pdf')
    with PdfPages(out) as pdf:
        fig = sheet(pdf, 'PATH_WIDTH_MAP Â· anchura libre de la red peatonal',
                    sub='Anchura libre local = 2 Ã— distancia al obstÃ¡culo mÃ¡s prÃ³ximo en la banda de cuerpo 0,05â€“2,10 m. '
                        'Rejilla 0,25 m. ClasificaciÃ³n provisional del propio anÃ¡lisis (sin norma aplicada todavÃ­a).')
        ax = fig.add_axes([0.035, 0.30, 0.63, 0.585])
        context_plan(ax)
        bounds = [0, 0.8, 1.2, 1.8, 2.5, 3.0, 4.0, 5.0, 6.5, 40]
        cols = ['#7A1F1A', '#C8322B', '#E2684A', '#E0A422', '#E9CE72', '#D5DFA6', '#AFC981', '#7FAA5C', '#4E8446']
        cmap = ListedColormap(cols); norm = BoundaryNorm(bounds, cmap.N)
        Wm = np.where(WALK, WIDTH, np.nan)
        im = ax.imshow(Wm, origin='lower', extent=EXT, cmap=cmap, norm=norm, interpolation='nearest', zorder=3)
        ax.imshow(np.where(OCC & PLAZA, 1.0, np.nan), origin='lower', extent=EXT,
                  cmap=ListedColormap(['#6E6A62']), alpha=0.85, zorder=4, interpolation='nearest')
        for p in A1['paths']:
            X = [r['x'] for r in p['rows']]; Y = [r['y'] for r in p['rows']]
            ax.plot(X, Y, color='white', lw=2.4, zorder=5, alpha=0.9)
            ax.plot(X, Y, color=TINTA, lw=0.9, zorder=6)
            ax.text(X[0], Y[0], ' ' + p['id'], fontsize=6.2, color=TINTA, zorder=7, weight='bold')
        for q in A1['narrow'][:18]:
            c = SEVC['RED'] if q['w'] < 1.8 else (SEVC['YELLOW'] if q['w'] < 3.0 else SEVC['GREEN'])
            ax.plot(q['x'], q['y'], 'o', ms=4.5, mfc='none', mec=c, mew=1.2, zorder=8)
            ax.text(q['x'] + 1.2, q['y'] + 1.2, '%.1f' % q['w'], fontsize=5.6, color=c, zorder=8, weight='bold')
        for k, v in A1['access'].items():
            ax.plot(v[0], v[1], 's', ms=4, color=TEAL, zorder=8)
        cax = fig.add_axes([0.035, 0.255, 0.42, 0.014])
        cb = fig.colorbar(im, cax=cax, orientation='horizontal', spacing='proportional')
        cb.set_label('anchura libre local (m)   Â·   ROJO <1,80     ÃMBAR 1,80â€“3,00     VERDE >3,00', fontsize=6.5)
        cb.ax.tick_params(labelsize=5.5)

        axt = fig.add_axes([0.70, 0.42, 0.275, 0.47])
        rows = [[p['id'][:19], '%.0f' % p['long'], '%.2f' % p['w_min'], '%.2f' % p['w_p05'],
                 '%.1f' % p['w_p50'], '%.2f' % p['wl_min']] for p in A1['paths']]
        table(axt, rows, [0.34, 0.11, 0.14, 0.13, 0.13, 0.15],
              ['recorrido', 'L(m)', 'mÃ­n', 'p05', 'p50', 'holg.mÃ­n'], fs=6.8, rowh=0.045)
        axt.text(0, 0.68, 'ANCHURA TRANSVERSAL medida por rayos perpendiculares al eje declarado;\n'
                          'Â«holg. mÃ­nÂ» = anchura libre local mÃ­nima sobre el eje.', fontsize=6.2,
                 color=GRIS, va='top', transform=axt.transAxes)
        rows2 = [['%.2f m' % f['w'], '%d' % f['comp'], '%.0f mÂ²' % f['big'], '%.0f %%' % (100 * f['cover'])]
                 for f in A1['frag']]
        table(axt, rows2, [0.26, 0.20, 0.30, 0.24],
              ['umbral', 'comp>20mÂ²', 'mayor', '% suelo'], fs=6.6, rowh=0.042, y0=0.60)
        axt.text(0, 0.24, 'FRAGMENTACIÃ“N: nÃºmero de componentes conectadas del suelo libre\n'
                          'al exigir esa anchura mÃ­nima continua.', fontsize=6.2, color=GRIS,
                 va='top', transform=axt.transAxes)
        bin_ = A1.get('bottleneck_ambito', {})
        bt = sorted(A1['bottleneck'].items(), key=lambda q: q[1])
        bi = sorted(bin_.items(), key=lambda q: q[1])
        table(axt, [['libre (puede rodear por la calle)', '%.2f m' % bt[0][1], '%.2f m' % bt[-1][1]],
                    ['obligando a cruzar el Ã¡mbito', '%.2f m' % (bi[0][1] if bi else 0),
                     '%.2f m' % (bi[-1][1] if bi else 0)]], [0.52, 0.24, 0.24],
              ['cuello de botella entre los 10 accesos', 'peor par', 'mejor par'], fs=6.4, rowh=0.046, y0=0.19)
        axt.text(0, 0.055, 'Maximin sobre la rejilla: anchura del punto mÃ¡s estrecho del mejor\n'
                           'camino posible entre cada par de accesos. La red estÃ¡ holgadamente\n'
                           'conectada; el problema no es la capacidad global sino los puntos\n'
                           'locales listados en la pÃ¡gina 2.', fontsize=6.2, color=GRIS,
                 va='top', transform=axt.transAxes)

        axp = fig.add_axes([0.035, 0.055, 0.94, 0.165])
        off = 0
        for p in A1['paths']:
            s = np.array([r['s'] for r in p['rows']]) + off
            w = np.array([r['w_local'] for r in p['rows']])
            axp.fill_between(s, 0, w, color=VERDE, alpha=0.20, lw=0)
            axp.plot(s, w, color=TEAL, lw=0.8)
            axp.axvline(off, color=GRIS, lw=0.4, ls=':')
            axp.text(off + 1, 10.6, p['id'], fontsize=6, color=TINTA)
            off += p['long'] + 12
        for th, c, lab in ((1.8, SEVC['RED'], '1,80'), (3.0, SEVC['YELLOW'], '3,00')):
            axp.axhline(th, color=c, lw=0.7, ls='--')
            axp.text(off, th, ' ' + lab, fontsize=6, color=c, va='center')
        axp.set_ylim(0, 12); axp.set_xlim(-2, off + 4)
        axp.set_ylabel('holgura libre (m)', fontsize=6.5)
        axp.set_xlabel('abscisa acumulada por recorrido (m) Â· holgura libre local sobre el eje declarado', fontsize=6.5)
        axp.tick_params(labelsize=6)
        for s_ in ('top', 'right'):
            axp.spines[s_].set_visible(False)
        close(pdf, fig)

        # pagina 2 â€” estrechamientos
        fig = sheet(pdf, 'PATH_WIDTH_MAP Â· estrechamientos sobre los ejes, pasos estrangulados y bolsas')
        axt = fig.add_axes([0.035, 0.30, 0.30, 0.575])
        rows = []
        for q in D['a1_paths.json']['narrow'][:24]:
            c = SEVC['RED'] if q['w'] < 1.8 else (SEVC['YELLOW'] if q['w'] < 3.0 else SEVC['GREEN'])
            rows.append([q['path'][:15], '%.0f' % q['s'], '%.0f,%.0f' % (q['x'], q['y']),
                         '%.2f' % q['w'], c])
        table(axt, rows, [0.36, 0.13, 0.28, 0.23],
              ['sobre el eje declarado', 's(m)', 'x,y', 'holgura'], fs=6.6, rowh=0.036)
        axk = fig.add_axes([0.355, 0.30, 0.32, 0.575])
        ck = D['a1_paths.json'].get('choke', [])
        table(axk, [['%.2f' % q['w'], '%.0f,%.0f' % (q['x'], q['y']), q['causa'][:24], SEVC['RED']]
                    for q in ck[:24]], [0.19, 0.26, 0.55],
              ['pasos estrangulados <1,20 m', 'x,y', 'entre familias'], fs=6.6, rowh=0.036)
        axk.text(0, 0.02, '%d pasos por debajo de 1,20 m de holgura en todo el Ã¡mbito\n(deduplicados a 2 m).'
                 % len(ck), fontsize=6.4, color=GRIS, va='top', transform=axk.transAxes)
        axp = fig.add_axes([0.685, 0.30, 0.29, 0.575])
        context_plan(axp)
        axp.imshow(np.where(WALK, WIDTH, np.nan), origin='lower', extent=EXT, cmap='RdYlGn',
                   vmin=0, vmax=8, interpolation='nearest', zorder=3, alpha=0.85)
        if ck:
            axp.scatter([q['x'] for q in ck], [q['y'] for q in ck], s=5, c='#7A1F1A', marker='o',
                        zorder=7, linewidths=0)
        for q in D['a1_paths.json']['pockets'][:14]:
            axp.plot(q['cx'], q['cy'], 'x', ms=7, color='#4B2E83', mew=1.6, zorder=8)
            axp.text(q['cx'] + 1.5, q['cy'], '%.0f mÂ²' % q['area'], fontsize=5.5, color='#4B2E83', zorder=8)
        axp.set_title('â— pasos <1,20 m   âœ• bolsas sin conexiÃ³n', fontsize=7, loc='left', color=TEAL)
        para(fig, 0.035, 0.26,
             'CRITERIO: se mide la geometrÃ­a, no la norma. El umbral 1,80 m se usa como referencia de trabajo '
             '(cruce de dos personas / silla + peatÃ³n) y 3,00 m como umbral de holgura para un espacio pÃºblico de esta '
             'intensidad de uso. La determinaciÃ³n normativa aplicable (Orden VIV/561/2010 y ordenanza municipal) queda '
             'pendiente de la fase de verificaciÃ³n normativa: aquÃ­ sÃ³lo se localiza y cuantifica.', w=0.9, fs=8)
        close(pdf, fig)
    return out


# ================================================================== 2 Â· CLEAR_HEIGHT_MAP
def pdf_clear():
    A2, CB = D['a2_clear.json'], D['a2_cables.json']
    out = os.path.join(HERE, 'CLEAR_HEIGHT_MAP.pdf')
    with PdfPages(out) as pdf:
        fig = sheet(pdf, 'CLEAR_HEIGHT_MAP Â· altura libre sobre el suelo pisable',
                    sub='Distancia vertical desde el pavimento hasta la cara inferior del primer elemento '
                        '(dosel, loops, estructura, cables, depÃ³sitos, vegetaciÃ³n, cinta). SÃ³lo celdas pisables.')
        ax = fig.add_axes([0.035, 0.20, 0.63, 0.685])
        context_plan(ax)
        Cm = np.where(WALK, CLEAR, np.nan)
        bounds = [0, 2.2, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 9.0, 12.0]
        cols = ['#7A1F1A', '#C8322B', '#E2684A', '#E0A422', '#E9CE72', '#CFE0A0', '#9FC46F',
                '#6FA24F', '#4E8446', '#2F5E33']
        cmap = ListedColormap(cols); norm = BoundaryNorm(bounds, cmap.N)
        im = ax.imshow(Cm, origin='lower', extent=EXT, cmap=cmap, norm=norm, interpolation='nearest', zorder=3)
        ax.imshow(np.where(WALK & ~np.isfinite(CLEAR), 1.0, np.nan), origin='lower', extent=EXT,
                  cmap=ListedColormap(['#F2F6FA']), zorder=2, interpolation='nearest')
        ax.imshow(np.where(OCC & PLAZA, 1.0, np.nan), origin='lower', extent=EXT,
                  cmap=ListedColormap(['#6E6A62']), alpha=0.8, zorder=4, interpolation='nearest')
        for q in A2['low'][:40]:
            ax.plot(q['x'], q['y'], 'o', ms=3.6, mfc='none', mec='#7A1F1A', mew=1.0, zorder=8)
        if CB:
            ax.scatter([q['x'] for q in CB], [q['y'] for q in CB], s=1.2, c='#4B2E83', zorder=7, marker='.')
        cax = fig.add_axes([0.035, 0.155, 0.42, 0.014])
        cb = fig.colorbar(im, cax=cax, orientation='horizontal', spacing='proportional')
        cb.set_label('altura libre (m)  Â·  blanco = cielo abierto  Â·  âœ• violeta = cable por debajo de 3,00 m', fontsize=6.5)
        cb.ax.tick_params(labelsize=5.5)
        s = A2['stats']
        para(fig, 0.035, 0.115,
             'Suelo pisable en el Ã¡mbito: %.0f mÂ². Bajo algÃºn elemento: %.0f mÂ² (%.0f %%). Mediana del gÃ¡libo: %.2f m.\n\n'
             'HALLAZGO CENTRAL DEL CAPÃTULO. La regla 7 del HEIGHT_SYSTEM exige 3,00 m Â«bajo cualquier elemento FIRME sobre '
             'pasoÂ». Separando las dos cosas: bajo elemento firme el gÃ¡libo sÃ³lo baja de 3,00 m en %.1f mÂ² de los %.0f mÂ² '
             'cubiertos (%.2f %%), con mÃ­nimo %.2f m, y todo ello ocurre bajo las zancas de las escaleras de la cinta. '
             'El mÃ­nimo absoluto de %.2f m NO es estructura: son copas de arbolado E02 (VEG2_ARBOL_A), %.1f mÂ² por debajo '
             'de 2,50 m â€” una cuestiÃ³n de poda de formaciÃ³n, no de gÃ¡libo estructural. El dosel, los loops, la cinta y las '
             'cÃ¡psulas cumplen.'
             % (s['area_libre'], s['area_cubierta'], s['pct_cubierta'], s['p50'],
                s['area_firme_bajo3'], s['area_cubierta'], 100 * s['area_firme_bajo3'] / max(s['area_cubierta'], 1),
                s['minimo_firme'], s['minimo'], s['area_veg_bajo250']),
             w=0.62, fs=8)
        axt = fig.add_axes([0.70, 0.55, 0.275, 0.335])
        rows = [['%.2f' % q['h'], '%.0f,%.0f' % (q['x'], q['y']), '%.2f' % q['area'], (q['obj'] or 'â€”')[:14],
                 SEVC['RED'] if q['h'] < 2.5 else SEVC['YELLOW']] for q in A2['low_firme'][:14]]
        table(axt, rows, [0.16, 0.24, 0.16, 0.44],
              ['FIRME  h', 'x,y', 'mÂ²', 'elemento'], fs=6.6, rowh=0.062)
        axv = fig.add_axes([0.70, 0.30, 0.275, 0.22])
        rows = [['%.2f' % q['h'], '%.0f,%.0f' % (q['x'], q['y']), '%.2f' % q['area'], (q['obj'] or 'â€”')[:14],
                 SEVC['YELLOW']] for q in A2['low_veg'][:9]]
        table(axv, rows, [0.16, 0.24, 0.16, 0.44],
              ['VEG.  h', 'x,y', 'mÂ²', 'bloque'], fs=6.6, rowh=0.095)
        close(pdf, fig)

        # secciones en los mÃ­nimos
        low = (A2['low_firme'][:2] + A2['low_veg'][:2])[:4]
        if low:
            fig = sheet(pdf, 'CLEAR_HEIGHT_MAP Â· secciones automÃ¡ticas en los mÃ­nimos de gÃ¡libo',
                        sub='Corte real del modelo con la persona de referencia de 1,70 m. '
                            'Arriba: mÃ­nimos bajo elemento firme. Abajo: mÃ­nimos bajo copa de arbolado.')
            for k, q in enumerate(low):
                ax = fig.add_axes([0.035 + (k % 2) * 0.49, 0.50 - (k // 2) * 0.42, 0.44, 0.34])
                draw_section(ax, 'y', q['y'], xr=(q['x'] - 11, q['x'] + 11), zr=(0, 10),
                             person_at=q['x'],
                             title='corte y = %.1f Â· mÃ­nimo %.2f m en x = %.1f Â· %s' % (q['y'], q['h'], q['x'], q['obj'] or 'â€”'))
            close(pdf, fig)
    return out


# ================================================================== 3 Â· ACCESSIBILITY_PRECHECK
def pdf_access():
    A5, A4r = D['a5_access.json'], D['a4_ribbon.json']
    out = os.path.join(HERE, 'ACCESSIBILITY_PRECHECK.pdf')
    with PdfPages(out) as pdf:
        fig = sheet(pdf, 'ACCESSIBILITY_PRECHECK Â· quÃ© itinerarios pueden funcionar como accesibles',
                    sub='PRE-CHEQUEO GEOMÃ‰TRICO. No es un certificado normativo: identifica quÃ© trazas tienen '
                        'geometrÃ­a compatible con un itinerario accesible y cuÃ¡les claramente no.')
        ax = fig.add_axes([0.035, 0.32, 0.60, 0.555])
        context_plan(ax)
        ok = WALK & (WIDTH >= 1.80)
        cond = WALK & (WIDTH >= 1.20) & (WIDTH < 1.80)
        no = WALK & (WIDTH < 1.20)
        for mk_, c, z in ((ok, '#9FC46F', 3), (cond, '#E0A422', 4), (no, '#C8322B', 5)):
            ax.imshow(np.where(mk_, 1.0, np.nan), origin='lower', extent=EXT,
                      cmap=ListedColormap([c]), zorder=z, interpolation='nearest')
        ax.imshow(np.where(OCC & PLAZA, 1.0, np.nan), origin='lower', extent=EXT,
                  cmap=ListedColormap(['#6E6A62']), alpha=0.8, zorder=6, interpolation='nearest')
        for p in D['a1_paths.json']['paths']:
            ax.plot([r['x'] for r in p['rows']], [r['y'] for r in p['rows']], color=TINTA, lw=0.9, zorder=7)
        RIB = np.asarray(M['circulacion']['ribbon'], float)
        ax.plot(RIB[:, 0], RIB[:, 1], color=ROSA, lw=1.6, zorder=8)
        for s in A4r['stairs']:
            ax.plot(s['x'], s['y'], '^', ms=6, color=ROSA, mec='white', mew=0.5, zorder=9)
        ax.set_title('verde â‰¥1,80 m Â· Ã¡mbar 1,20â€“1,80 Â· rojo <1,20 Â· rosa = cinta +6,00 (â–² escaleras)',
                     fontsize=7, loc='left', color=TEAL)
        axt = fig.add_axes([0.66, 0.55, 0.315, 0.33])
        rows = []
        for r in A5['rows']:
            c = SEVC['RED'] if r['veredicto'].startswith('NO') else (SEVC['GREEN'] if r['veredicto'] == 'APTO' else SEVC['YELLOW'])
            rows.append([r['id'][:18], '%.2f' % r['w_min'], '%.0f%%' % r['pct_w_ge_180'],
                         '%.1f' % r['pend_pct'], r['veredicto'][:14], c])
        table(axt, rows, [0.30, 0.13, 0.13, 0.11, 0.33],
              ['itinerario', 'ancho mÃ­n', '% â‰¥1,80', 'pend %', 'veredicto'], fs=6.8, rowh=0.075)
        axg = fig.add_axes([0.66, 0.32, 0.315, 0.19])
        st = A4r['stairs'][0]
        n = 16
        for k in range(n):
            t = k / (n - 1)
            axg.add_patch(Rectangle((t * (st['huella'] * (n - 1)) - 0.16, t * 5.78 - 0.05), 0.32, 0.05,
                                    facecolor='#A87840', edgecolor='none'))
        axg.plot([0, st['huella'] * (n - 1)], [0, 5.78], color=ROSA, lw=1.0)
        axg.add_patch(Rectangle((-0.9 - 0.14, 0), 0.28, 1.45, facecolor='#33322E'))
        axg.add_patch(Circle((-0.9, 1.58), 0.12, facecolor='#33322E'))
        axg.set_xlim(-2, 7.5); axg.set_ylim(0, 6.6); axg.set_aspect('equal')
        axg.tick_params(labelsize=5.5)
        axg.set_title('escalera de la cinta tal como estÃ¡ construida: CH %.3f Â· H %.3f Â· %.0f%%'
                      % (st['contrahuella'], st['huella'], st['pendiente_pct']), fontsize=6.6, loc='left', color=SEVC['RED'])
        for s_ in ('top', 'right'):
            axg.spines[s_].set_visible(False)
        para(fig, 0.035, 0.275,
             'LECTURA. El plano de plaza es horizontal en todo el Ã¡mbito (cota 0,00 en toda la superficie construida): '
             'no hay pendientes que evaluar a nivel de suelo, y la accesibilidad a cota 0 depende exclusivamente de anchura, '
             'obstÃ¡culos y giros. El Ãºnico cambio de nivel del proyecto es la cinta a +6,00, resuelto con 6 escaleras de '
             'contrahuella 0,385 m y pendiente 91 %% (42Â°), sin barandilla, sin meseta y sin ningÃºn medio alternativo: '
             'geomÃ©tricamente la cota +6,00 no es accesible y, tal como estÃ¡, tampoco es una escalera utilizable.\n\n'
             'Bordes sin protecciÃ³n detectados: %d estanques con bordillo de 0,60 m sin barandilla ni cambio de textura, '
             'y la barandilla de la cinta (1,05 m) sin travesaÃ±o intermedio ni rodapiÃ©.\n\n'
             'CÃ­rculo de giro: se comprueba Ã˜1,50 m sobre el eje de cada recorrido (columna Â«%% â‰¥1,80Â» y el mapa verde). '
             'La banda Ã¡mbar admite un peatÃ³n pero no el cruce con silla de ruedas.'
             % sum(1 for e in A5['edges'] if e['tipo'] == 'estanque'), w=0.93, fs=8)
        close(pdf, fig)
    return out


# ================================================================== 4 Â· METRO
def pdf_metro():
    A6 = D['a6_metro.json']
    out = os.path.join(HERE, 'METRO_CLEARANCE_AUDIT.pdf')
    with PdfPages(out) as pdf:
        fig = sheet(pdf, 'METRO_CLEARANCE_AUDIT Â· accesos de Metro y CercanÃ­as',
                    sub='La banda de 5,5 m usada en 03B (D03B-02) se AUDITA, no se asume como obligaciÃ³n normativa. '
                        'Se mide la distancia real al elemento de proyecto mÃ¡s prÃ³ximo y el ancho libre frontal.')
        ax = fig.add_axes([0.035, 0.30, 0.52, 0.575])
        context_plan(ax)
        ax.imshow(np.where(WALK, WIDTH, np.nan), origin='lower', extent=EXT, cmap='Greys_r',
                  vmin=0, vmax=10, interpolation='nearest', zorder=3, alpha=0.35)
        for r in A6['rows']:
            c = SEVC['GREEN'] if r['d_suelo'] >= 5.5 else (SEVC['YELLOW'] if r['d_suelo'] >= 2.0 else SEVC['RED'])
            if not r['en_ambito']:
                c = GRIS
            ax.add_patch(Circle((r['x'], r['y']), A6['band'], facecolor='none', edgecolor=c, lw=0.9,
                                ls='--', zorder=6))
            ax.plot(r['x'], r['y'], 'o', ms=5, color=c, mec='white', mew=0.6, zorder=7)
            ax.text(r['x'] + 2, r['y'] + 2, '%s\n%.2f m' % (r['name'], min(r['d_suelo'], 99)), fontsize=5.8,
                    color=c, zorder=7, weight='bold')
        axt = fig.add_axes([0.585, 0.30, 0.39, 0.575])
        rows = []
        for r in A6['rows']:
            c = GRIS if not r['en_ambito'] else (SEVC['GREEN'] if r['d_suelo'] >= 5.5 else
                                                 (SEVC['YELLOW'] if r['d_suelo'] >= 2.0 else SEVC['RED']))
            rows.append([r['name'][:13], '%.0f,%.0f' % (r['x'], r['y']), 'sÃ­' if r['en_ambito'] else 'fuera',
                         '%.2f' % min(r['d_suelo'], 99), '%d' % r['n_banda_suelo'], '%.1f' % r['libre_min'],
                         '%d' % r['n_banda_aereo'], ('%.1f' % r['galibo']) if r['galibo'] else 'cielo', c])
        table(axt, rows, [0.17, 0.14, 0.10, 0.11, 0.10, 0.12, 0.10, 0.12],
              ['acceso', 'x,y', 'Ã¡mbito', 'd suelo', 'n suelo', 'frontal', 'n aÃ©reo', 'gÃ¡libo'],
              fs=6.4, rowh=0.055)
        y = 0.52
        for r in A6['rows']:
            if not r['en_ambito'] or not r['invasores']:
                continue
            axt.text(0, y, '%s â–¸ ' % r['name'] + ' Â· '.join('%s %.2f m (z%.1f)' % (q[0][:11], q[2], q[3])
                                                            for q in r['invasores'][:5]),
                     fontsize=5.9, color=TINTA, va='top', transform=axt.transAxes)
            y -= 0.031
        para(fig, 0.035, 0.26,
             'CRITERIO. Se separan dos cosas que en planta se confunden. (a) OBSTÃCULO A NIVEL DE BOCA: elemento cuya base estÃ¡ '
             'por debajo de +2,50 m, es decir con el que se puede tropezar o que estrecha el frente de evacuaciÃ³n â€” es la medida '
             'que importa. (b) ESTRUCTURA AÃ‰REA: loops, dosel y cinta que cruzan sobre el acceso; en planta aparecen Â«a 0,09 mÂ» '
             'pero pasan a +10,00 m y no invaden nada, sÃ³lo cubren. Se mide ademÃ¡s el ancho libre frontal mÃ­nimo en 24 direcciones '
             'y el gÃ¡libo sobre la vertical de la boca.\n\n'
             'INTERPRETACIÃ“N. La exclusiÃ³n de 5,5 m (D03B-02) se aplicÃ³ a discos y mÃ¡stiles, pero la vegetaciÃ³n E02 y las piezas '
             'menores se implantaron despuÃ©s con reglas propias. ACCIÃ“N PENDIENTE: contrastar con el criterio real de Metro de Madrid '
             '(evacuaciÃ³n, ventilaciÃ³n, accesos de emergencia y mantenimiento) antes de mover nada. La banda de 5,5 m NO se '
             'interpreta aquÃ­ como obligaciÃ³n normativa.', w=0.93, fs=8)
        close(pdf, fig)
    return out


# ================================================================== 5 Â· VISUALES
def pdf_views():
    A7 = D['a7_views.json']
    out = os.path.join(HERE, 'VIEW_CORREOS_CLOCK.pdf')
    P = np.array(A7['pts'])
    with PdfPages(out) as pdf:
        fig = sheet(pdf, 'VIEW_CORREOS_CLOCK Â· visibilidad de la Real Casa de Correos, la torre y el reloj',
                    sub='Rejilla de observadores a 1,65 m sobre suelo pisable (%d puntos, paso 2 m). '
                        'Trazado de rayo contra el modelo completo. La membrana ETFE de la cÃºpula se considera translÃºcida.'
                        % A7['n'])
        for k, tgt in enumerate(('CORREOS', 'TORRE', 'RELOJ')):
            ax = fig.add_axes([0.035 + k * 0.322, 0.40, 0.30, 0.47])
            context_plan(ax)
            v = np.array(A7['vis'][tgt])
            ax.scatter(P[~v, 0], P[~v, 1], s=2.2, c='#C8322B', marker='s', zorder=5, linewidths=0)
            ax.scatter(P[v, 0], P[v, 1], s=2.2, c='#4E8446', marker='s', zorder=6, linewidths=0)
            ax.plot(-25.23, -34.35, '*', ms=13, color=ROSA, mec='white', mew=0.6, zorder=9)
            ax.set_title('%s â€” visible desde %.1f %%' % (tgt, A7['pct'][tgt]), fontsize=8.5,
                         loc='left', color=TEAL, weight='bold')
        axb = fig.add_axes([0.035, 0.29, 0.30, 0.075])
        axb.barh([2, 1, 0], [A7['pct'][t] for t in ('CORREOS', 'TORRE', 'RELOJ')],
                 color=[VERDE, TEAL, ROSA], height=0.6)
        axb.set_yticks([2, 1, 0]); axb.set_yticklabels(['Casa de Correos', 'torre', 'reloj'], fontsize=6.5)
        axb.set_xlim(0, 100); axb.set_xlabel('% de puntos de observaciÃ³n con visiÃ³n directa', fontsize=6.5)
        axb.tick_params(labelsize=6)
        for s_ in ('top', 'right'):
            axb.spines[s_].set_visible(False)
        for i_, t in enumerate(('CORREOS', 'TORRE', 'RELOJ')):
            axb.text(A7['pct'][t] + 1.5, 2 - i_, '%.1f %%' % A7['pct'][t], fontsize=6.5, va='center', color=TINTA)
        para(fig, 0.38, 0.30,
             'CRITERIO. Objetivos: fachada principal de la Real Casa de Correos a +8,50; cuerpo de la torre a +22,00; '
             'esfera del reloj a +26,50 (posiciÃ³n del modelo de contexto). Un punto cuenta como Â«veÂ» si el segmento '
             'ojoâ†’objetivo no atraviesa ningÃºn vÃ³xel ocupado de 0,50 m (dosel, estructura, cÃ¡psulas, vegetaciÃ³n, contexto).\n\n'
             'INTERPRETACIÃ“N: el reloj es el compromiso urbano explÃ­cito del proyecto (V07 y V20 de 03B lo verifican como '
             'vista puntual). Este mapa mide otra cosa: desde quÃ© porcentaje de la plaza se mantiene esa relaciÃ³n. '
             'La caÃ­da se concentra bajo el dosel continuo y tras las copas E02.', w=0.58, fs=8)
        close(pdf, fig)
    return out


# ================================================================== 6 Â· COLISIONES
def pdf_collisions():
    A10 = D['a10_collisions.json']
    out = os.path.join(HERE, 'COLLISION_REPORT.pdf')
    with PdfPages(out) as pdf:
        fig = sheet(pdf, 'COLLISION_REPORT Â· comprobaciÃ³n sistemÃ¡tica entre familias',
                    sub='VÃ³xeles de 0,20 m. Se distingue el contacto intencionado (apoyo, anclaje, plantaciÃ³n) '
                        'de la interpenetraciÃ³n accidental.')
        fams = sorted(set([p['a'] for p in A10['pairs']] + [p['b'] for p in A10['pairs']]))
        ax = fig.add_axes([0.035, 0.40, 0.40, 0.47])
        Mx = np.full((len(fams), len(fams)), np.nan)
        Ix = np.zeros((len(fams), len(fams)), bool)
        for p in A10['pairs']:
            i, j = fams.index(p['a']), fams.index(p['b'])
            Mx[i, j] = Mx[j, i] = p['vol']
            Ix[i, j] = Ix[j, i] = p['intencionado']
        im = ax.imshow(Mx, cmap='OrRd', norm=matplotlib.colors.LogNorm(vmin=1e-3, vmax=max(np.nanmax(Mx), 1e-2)))
        ax.set_xticks(range(len(fams))); ax.set_yticks(range(len(fams)))
        ax.set_xticklabels(fams, rotation=90, fontsize=6); ax.set_yticklabels(fams, fontsize=6)
        for i in range(len(fams)):
            for j in range(len(fams)):
                if np.isfinite(Mx[i, j]):
                    ax.text(j, i, 'â—' if Ix[i, j] else 'â–²', ha='center', va='center',
                            fontsize=5.5, color='#2b2b2b' if Ix[i, j] else '#7A1F1A')
        fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02).set_label('volumen de solape (mÂ³)', fontsize=6.5)
        ax.set_title('â— contacto intencionado    â–² revisar', fontsize=7, loc='left', color=TEAL)
        axt = fig.add_axes([0.47, 0.40, 0.50, 0.47])
        rows = [[p['a'][:11], p['b'][:11], '%d' % p['voxels'], '%.2f' % p['vol'],
                 'intencionado' if p['intencionado'] else 'REVISAR',
                 '#2b2b2b' if p['intencionado'] else SEVC['RED']] for p in A10['pairs'][:26]]
        table(axt, rows, [0.20, 0.20, 0.13, 0.14, 0.33],
              ['familia A', 'familia B', 'vÃ³xeles', 'mÂ³', 'lectura'], fs=6.8, rowh=0.036)
        axh = fig.add_axes([0.035, 0.055, 0.94, 0.28])
        axh.axis('off')
        rows = [[h['pair'][:24], h['a'][:16], h['b'][:16], '%.0f,%.0f,%.1f' % (h['x'], h['y'], h['z']),
                 '%d' % h['voxels'], '%.3f' % h['vol']] for h in A10['hot'][:22]]
        table(axh, rows, [0.19, 0.16, 0.16, 0.17, 0.09, 0.10],
              ['par', 'objeto A', 'objeto B', 'x,y,z', 'vÃ³x', 'mÂ³'], fs=6.6, rowh=0.042, y0=0.95)
        axh.text(0.52, 0.95, 'CONTACTOS INTENCIONADOS reconocidos: mÃ¡stilâ†”disco (anclaje), estructuraâ†”cinta (apoyo), '
                             'jardineraâ†”vegetaciÃ³n (plantaciÃ³n),\nestructuraâ†”agua (bajantes y aros de balsa), '
                             'estructuraâ†”cÃ¡psula (cunas y pies). El resto se marca para revisiÃ³n.',
                 fontsize=6.4, color=GRIS, va='top', transform=axh.transAxes)
        close(pdf, fig)
    return out


# ================================================================== 7 Â· MANTENIMIENTO
def pdf_maint():
    A9 = D['a9_maint.json']
    out = os.path.join(HERE, 'MAINTENANCE_ACCESS.pdf')
    with PdfPages(out) as pdf:
        fig = sheet(pdf, 'MAINTENANCE_ACCESS Â· acceso geomÃ©trico a los componentes tÃ©cnicos',
                    sub='Para cada componente se busca la mejor superficie pisable a â‰¤4 m. Criterio de trabajo: '
                        '0,90 m de holgura para operaciÃ³n manual; 2,50 m para plataforma elevadora si el elemento estÃ¡ en altura.')
        ax = fig.add_axes([0.035, 0.30, 0.56, 0.575])
        context_plan(ax)
        ax.imshow(np.where(WALK, 1.0, np.nan), origin='lower', extent=EXT,
                  cmap=ListedColormap(['#EFF3EC']), zorder=2, interpolation='nearest')
        MK = {'DEPOSITO +10.5': 'D', 'DEPOSITO DE SUELO': 'o', 'NEBULIZADOR +4.0': '.', 'VIVERO': 's',
              'CANOPY / BAJANTE': '^', 'BOMBEO': 'P', 'BAJANTE/RISER': 'v'}
        for q in A9:
            c = SEVC['GREEN'] if q['acceso'] else SEVC['RED']
            ax.plot(q['x'], q['y'], MK.get(q['cat'], 'o'), ms=4.6 if q['cat'] != 'NEBULIZADOR +4.0' else 6,
                    color=c, mec='white', mew=0.35, zorder=7)
        h = [plt.Line2D([], [], marker=v, ls='', color=GRIS, label=k, ms=5) for k, v in MK.items()]
        ax.legend(handles=h, fontsize=5.8, loc='lower left', ncol=3, frameon=False)
        ax.set_title('verde = acceso suficiente Â· rojo = sin acceso', fontsize=7, loc='left', color=TEAL)
        axt = fig.add_axes([0.62, 0.45, 0.355, 0.425])
        cats = sorted(set(q['cat'] for q in A9))
        rows = []
        for c_ in cats:
            sub = [q for q in A9 if q['cat'] == c_]
            nb = [q for q in sub if not q['acceso']]
            col = SEVC['RED'] if len(nb) > len(sub) * 0.5 else (SEVC['YELLOW'] if nb else SEVC['GREEN'])
            rows.append([c_[:20], '%d' % len(sub), '%d' % len(nb),
                         '%.2f' % np.median([q['holgura'] for q in sub]),
                         'sÃ­' if sub[0]['requiere_plataforma'] else 'no', col])
        table(axt, rows, [0.36, 0.11, 0.13, 0.20, 0.20],
              ['componente', 'uds', 'sin acc.', 'holgura med.', 'plataforma'], fs=6.8, rowh=0.075)
        axl = fig.add_axes([0.62, 0.30, 0.355, 0.13])
        bad = sorted([q for q in A9 if not q['acceso']], key=lambda q: q['holgura'])[:12]
        table(axl, [[q['id'][:16], '%.0f,%.0f' % (q['x'], q['y']), '%.2f' % q['holgura'],
                     '%.1f' % q['z']] for q in bad], [0.34, 0.24, 0.21, 0.21],
              ['peores casos', 'x,y', 'holgura', 'z elem.'], fs=6.5, rowh=0.072)
        para(fig, 0.035, 0.26,
             'CRITERIO / INTERPRETACIÃ“N. El modelo 03B no contiene ninguna reserva de Ã¡rea tÃ©cnica: los depÃ³sitos de +10,50, '
             'los 42 nebulizadores, las bajantes de los 67 discos y los viveros se implantaron por lÃ³gica de composiciÃ³n. '
             'Este chequeo sÃ³lo mide si, con la geometrÃ­a E02 puesta, queda sitio para llegar. Un componente marcado en rojo '
             'no significa Â«imposible de mantenerÂ», significa Â«no hay superficie de apoyo suficiente sin retirar vegetaciÃ³n o mobiliarioÂ». '
             'ACCIÃ“N PENDIENTE: definir el protocolo de mantenimiento (Â¿desde la cinta? Â¿plataforma sobre pavimento? Â¿desmontaje de mÃ³dulos?) '
             'antes de decidir quÃ© se mueve.', w=0.93, fs=8)
        close(pdf, fig)
    return out


# ================================================================== 8 Â· MASTER
def pdf_master():
    out = os.path.join(HERE, 'VIABILITY_AUDIT_MASTER.pdf')
    A1, A2, A3h, A4r = D['a1_paths.json'], D['a2_clear.json'], D['a3_heights.json'], D['a4_ribbon.json']
    A6, A7, A8, A9, A10 = (D['a6_metro.json'], D['a7_views.json'], D['a8_density.json'],
                           D['a9_maint.json'], D['a10_collisions.json'])
    red = [r for r in ISSUES if r['sev'] == 'RED']
    yel = [r for r in ISSUES if r['sev'] == 'YELLOW']
    grn = [r for r in ISSUES if r['sev'] == 'GREEN']
    with PdfPages(out) as pdf:
        # --- portada / resumen ejecutivo
        fig = sheet(pdf, 'VIABILITY_AUDIT_MASTER', sub='AuditorÃ­a geomÃ©trica y de viabilidad del modelo aprobado. '
                                                       'Fase 03B.5 Â· previa a E03 Â· NO se ha modificado la geometrÃ­a maestra.')
        axs = fig.add_axes([0.035, 0.52, 0.44, 0.35]); axs.axis('off')
        s = SUM
        table(axs, [
            ['objetos de malla auditados', '%d' % s['objetos']],
            ['triÃ¡ngulos', '%d' % s['tris']],
            ['Ã¡mbito de proyecto', '%.0f mÂ²' % s['area_ambito']],
            ['suelo libre a nivel de cuerpo', '%.0f mÂ² (%.0f %%)' % (s['area_libre'], 100 * s['area_libre'] / s['area_ambito'])],
            ['ocupaciÃ³n de suelo', '%.1f %%' % s['ocupacion']],
            ['superficie cubierta por dosel/cinta', '%.1f %%' % s['cobertura']],
            ['holgura libre mediana del suelo pisable', '%.2f m' % s['ancho_p50']],
            ['holgura libre, percentil 5', '%.2f m  (5 %% del suelo, junto a bordes)' % s['ancho_p05']],
            ['cuello de botella mÃ­nimo entre accesos', '%.2f m' % (s['cuello_min'] or 0)],
            ['gÃ¡libo mÃ­n. bajo elemento firme', '%.2f m' % D['a2_clear.json']['stats']['minimo_firme']],
            ['gÃ¡libo mÃ­n. bajo copa de arbolado', '%.2f m' % s['galibo_min']],
            ['visibilidad del reloj', '%.1f %% de la plaza' % s['vis']['RELOJ']],
        ], [0.62, 0.38], ['MAGNITUD MEDIDA', 'VALOR'], fs=8.4, rowh=0.072)
        axc = fig.add_axes([0.52, 0.60, 0.20, 0.26])
        axc.pie([len(red), len(yel), len(grn)], colors=[SEVC['RED'], SEVC['YELLOW'], SEVC['GREEN']],
                startangle=90, wedgeprops=dict(width=0.42, edgecolor='white'))
        axc.text(0, 0, '%d\nincidencias' % len(ISSUES), ha='center', va='center', fontsize=11, weight='bold')
        axc.set_title('RED %d   Â·   YELLOW %d   Â·   GREEN %d' % (len(red), len(yel), len(grn)), fontsize=8.5, color=TEAL)
        axk = fig.add_axes([0.74, 0.52, 0.235, 0.35]); axk.axis('off')
        cats = {}
        for r in ISSUES:
            cats.setdefault(r['cat'], [0, 0, 0])
            cats[r['cat']][['RED', 'YELLOW', 'GREEN'].index(r['sev'])] += 1
        table(axk, [[k[:14], str(v[0]), str(v[1]), str(v[2])] for k, v in sorted(cats.items(), key=lambda q: -q[1][0])],
              [0.46, 0.18, 0.18, 0.18], ['capÃ­tulo', 'RED', 'AMB', 'GRN'], fs=7.6, rowh=0.062)
        para(fig, 0.035, 0.47,
             'QUÃ‰ ES ESTE DOCUMENTO. Una mediciÃ³n del modelo aprobado, no un rediseÃ±o. Todos los nÃºmeros salen de reconstruir '
             'en memoria la misma escena que produce SOL_FULL_SCENE_v001 (6.672 mallas / 394.610 triÃ¡ngulos) y medirla con una '
             'rejilla de 0,25 m, un vÃ³xel de 0,20 m para colisiones y un vÃ³xel de 0,50 m para el trazado de rayos visuales.\n\n'
             'QUÃ‰ NO ES. No se ha aplicado ninguna norma. Los umbrales 1,80 / 3,00 m de anchura, 3,00 m de gÃ¡libo y 5,5 m de banda '
             'de Metro son criterios de trabajo â€”los dos primeros del propio HEIGHT_SYSTEM, el tercero de la decisiÃ³n D03B-02â€”, '
             'y se usan para clasificar y localizar, no para certificar. La identificaciÃ³n de la normativa aplicable es el paso '
             'siguiente y deliberadamente no se hace aquÃ­.\n\n'
             'NADA SE HA CORREGIDO. Cada hallazgo se registra con posiciÃ³n, magnitud, causa, severidad y estrategias posibles, '
             'y espera revisiÃ³n. El master estÃ¡ intacto.', w=0.93, fs=8.6)

        r4 = D['a4_ribbon.json']; a2s = D['a2_clear.json']['stats']; a8 = D['a8_density.json']['global_']
        a9 = D['a9_maint.json']
        n9 = sum(1 for q in a9 if not q['acceso'])
        concl = [
            ('RED', 'La cota +6,00 no tiene ningÃºn acceso utilizable.',
             'Las 6 escaleras tienen contrahuella 0,385 m, huella 0,424 m y 91 % de pendiente (2CH+H = 1,19 m frente a los '
             '0,62â€“0,65 de la regla de comodidad); no hay barandilla, ni meseta, ni rampa, ni ascensor. Es el hallazgo mÃ¡s '
             'grave y el Ãºnico que invalida por sÃ­ solo una parte del programa: 519 m de paseo por el dosel sin forma de subir.'),
            ('RED', 'La estructura sÃ­ respeta el gÃ¡libo; el arbolado no.',
             'Bajo elemento firme el gÃ¡libo sÃ³lo baja de 3,00 m en %.1f mÂ² (%.2f %% del suelo cubierto), y siempre bajo las '
             'zancas de escalera. El mÃ­nimo absoluto de %.2f m son copas de VEG2_ARBOL_A: poda de formaciÃ³n, no estructura. '
             'La regla 7 del HEIGHT_SYSTEM se cumple.' % (a2s['area_firme_bajo3'],
                                                          100 * a2s['area_firme_bajo3'] / max(a2s['area_cubierta'], 1),
                                                          a2s['minimo'])),
            ('YELLOW', 'El HEIGHT_SYSTEM ha dejado de describir el modelo.',
             '32 de los 67 discos de dosel caen fuera de la familia declarada 5,00 / 6,75 / 8,50 (Â±0,30 m), y 3 parÃ¡metros '
             'declarados no estÃ¡n construidos. Antes de E03 conviene decidir si manda el documento o el modelo.'),
            ('YELLOW', 'El mantenimiento no tiene sitio reservado.',
             '%d de %d componentes tÃ©cnicos no tienen superficie de apoyo suficiente: los 6 depÃ³sitos de suelo, los 3 viveros '
             'y 37 de los 67 discos. No es Â«imposible de mantenerÂ», es que no hay Ã¡rea tÃ©cnica proyectada.' % (n9, len(a9))),
            ('YELLOW', 'La visibilidad del reloj se conserva en algo mÃ¡s de un tercio de la plaza.',
             'Reloj %.0f %%, torre %.0f %%, Casa de Correos %.0f %% de %d puntos de observaciÃ³n a 1,65 m. Es una decisiÃ³n de '
             'proyecto, no un error: el dosel es el argumento del refugio. Se mide para que la renuncia sea consciente.'
             % (s['vis']['RELOJ'], s['vis']['TORRE'], s['vis']['CORREOS'], D['a7_views.json']['n'])),
            ('GREEN', 'La plaza no se ha densificado con E02 y la red peatonal es holgada.',
             'La ocupaciÃ³n de suelo pasÃ³ del %.1f %% (MASTER) al %.1f %% con toda la vegetaciÃ³n E02 puesta: +%.1f puntos. '
             'El %.0f %% del suelo libre sigue conectado exigiendo 3,00 m continuos, y el peor par de accesos tiene un cuello '
             'de %.2f m. Los problemas de paso son locales, no sistÃ©micos.'
             % (a8['ocup_master'], a8['ocup'], a8['ocup'] - a8['ocup_master'],
                100 * D['a1_paths.json']['frag'][6]['cover'], s['cuello_min'] or 0)),
        ]
        yy = 0.325
        fig.text(0.035, yy + 0.028, 'LO QUE DICE LA MEDICIÃ“N', fontsize=9.5, weight='bold', color=TEAL)
        for sev, t, d in concl:
            fig.text(0.035, yy, 'â—', fontsize=9, color=SEVC[sev], va='top')
            fig.text(0.052, yy, t, fontsize=8.8, weight='bold', va='top')
            fig.text(0.052, yy - 0.017, d, fontsize=7.8, color=TINTA, va='top', wrap=True)
            yy -= 0.049
        close(pdf, fig)

        # --- 1 recorridos + 2 galibos
        fig = sheet(pdf, '1 Â· RECORRIDOS   |   2 Â· GÃLIBOS')
        ax = fig.add_axes([0.035, 0.46, 0.44, 0.40]); context_plan(ax)
        ax.imshow(np.where(WALK, WIDTH, np.nan), origin='lower', extent=EXT, cmap='RdYlGn',
                  vmin=0, vmax=8, interpolation='nearest', zorder=3)
        for p in A1['paths']:
            ax.plot([r['x'] for r in p['rows']], [r['y'] for r in p['rows']], color=TINTA, lw=0.8, zorder=5)
        ax.set_title('anchura libre local (m) Â· rojo <1,8 Â· verde >6', fontsize=7, loc='left', color=TEAL)
        ax2 = fig.add_axes([0.51, 0.46, 0.44, 0.40]); context_plan(ax2)
        ax2.imshow(np.where(WALK, CLEAR, np.nan), origin='lower', extent=EXT, cmap='RdYlGn',
                   vmin=2, vmax=9, interpolation='nearest', zorder=3)
        ax2.set_title('altura libre (m) Â· rojo <3,0', fontsize=7, loc='left', color=TEAL)
        axt = fig.add_axes([0.035, 0.055, 0.44, 0.35])
        table(axt, [[p['id'][:20], '%.0f' % p['long'], '%.2f' % p['w_min'], '%.2f' % p['w_p05'],
                     '%.1f' % p['w_p50'], '%d' % p['eje_bloqueado']] for p in A1['paths']],
              [0.34, 0.12, 0.14, 0.13, 0.13, 0.14],
              ['recorrido', 'L', 'mÃ­n', 'p05', 'p50', 'eje bloq.'], fs=7.2, rowh=0.075)
        axt.text(0, 0.32, 'Estrechamientos <3,00 m: %d Â· el mÃ¡s estrecho %.2f m.\n'
                          'Bolsas de suelo sin conexiÃ³n: %d.\nCuello de botella mÃ­nimo entre accesos: %.2f m.'
                 % (sum(1 for q in A1['narrow'] if q['w'] < 3.0),
                    min(q['w'] for q in A1['narrow']) if A1['narrow'] else 0,
                    len(A1['pockets']), min(A1['bottleneck'].values())),
                 fontsize=7.6, va='top', transform=axt.transAxes)
        axg = fig.add_axes([0.51, 0.055, 0.44, 0.35])
        table(axg, [['%.2f m' % q['h'], '%.0f,%.0f' % (q['x'], q['y']), '%.1f mÂ²' % q['area'], (q['obj'] or 'â€”')[:18]]
                    for q in (A2['low_firme'][:4] + A2['low_veg'][:5])], [0.16, 0.22, 0.16, 0.46],
              ['gÃ¡libo', 'x,y', 'Ã¡rea', 'elemento'], fs=7.2, rowh=0.062)
        axg.text(0, 0.34, 'MÃ­nimo absoluto %.2f m (H_CLEAR_MIN declarado 3,00 m).\n'
                          '%d manchas por debajo de 3,00 m sobre suelo pisable.\n'
                          '%d muestras de cable tensado por debajo de 3,00 m.'
                 % (A2['stats']['minimo'], len(A2['low']), len(D['a2_cables.json'])),
                 fontsize=7.6, va='top', transform=axg.transAxes)
        close(pdf, fig)

        # --- 3 alturas
        fig = sheet(pdf, '3 Â· ALTURAS Â· HEIGHT_SYSTEM contra la geometrÃ­a construida')
        axt = fig.add_axes([0.035, 0.28, 0.50, 0.585])
        rows = []
        for r in A3h['rows']:
            c = {'OK': SEVC['GREEN'], 'FUERA': SEVC['RED'], 'N/C': GRIS}[r['estado']]
            rows.append([r['param'][:20], str(r['declarado'])[:12],
                         '%sâ€“%s' % (r['rango'][0], r['rango'][1]),
                         ('no construido' if r['construido'] is None else str(r['construido'])), r['estado'], c])
        table(axt, rows, [0.26, 0.14, 0.11, 0.28, 0.12],
              ['parÃ¡metro', 'declarado', 'rango', 'construido', 'estado'], fs=7.0, rowh=0.040)
        axh = fig.add_axes([0.57, 0.55, 0.40, 0.31])
        cot = np.array(A3h['cotas_discos'])
        axh.hist(cot, bins=np.arange(4.0, 8.8, 0.25), color=VERDE, alpha=0.75, edgecolor='white', lw=0.4)
        for z, lab in ((5.0, 'H_LOW 5,00'), (6.75, 'H_MID 6,75'), (8.5, 'H_HIGH 8,50')):
            axh.axvline(z, color=ROSA, lw=1.0)
            axh.text(z, axh.get_ylim()[1] * 0.95, ' ' + lab, fontsize=6, color=ROSA, rotation=90, va='top')
        axh.set_xlabel('cota de implantaciÃ³n de los 67 discos de dosel (m)', fontsize=6.5)
        axh.set_ylabel('nÂº discos', fontsize=6.5); axh.tick_params(labelsize=6)
        for s_ in ('top', 'right'):
            axh.spines[s_].set_visible(False)
        nfuera = sum(1 for r in A3h['rows'] if r['estado'] == 'FUERA')
        nnc = sum(1 for r in A3h['rows'] if r['estado'] == 'N/C')
        para(fig, 0.57, 0.50,
             'HALLAZGO PRINCIPAL. El HEIGHT_SYSTEM declara un cielo verde en TRES capas escalonadas (5,00 / 6,75 / 8,50) y '
             'la resoluciÃ³n D10 fija 8,50 como mÃ¡ximo. La geometrÃ­a construida no obedece a esa familia: las cotas de los '
             'discos se leen una a una del JSON y se recortan al intervalo [4,20 Â· 8,50], de modo que 32 de los 67 discos '
             'caen a mÃ¡s de Â±0,30 m de cualquiera de las tres capas. No es necesariamente un error â€”puede ser una decisiÃ³n '
             'de composiciÃ³nâ€” pero significa que el HEIGHT_SYSTEM ya no describe el modelo: describe una intenciÃ³n anterior.\n\n'
             'RESTO DEL CONTRASTE. %d parÃ¡metros fuera de su rango declarado y %d declarados pero no construidos '
             '(H_BENCH_BACK: no hay respaldos; H_TANK_TOWER: no hay torre de depÃ³sitos apilados; H_LOGISTIC_RAIL: '
             'reserva G4 apagada por D9 â€” este Ãºltimo es coherente con la decisiÃ³n tomada). Los fuera de rango son '
             'menores y todos por exceso: el depÃ³sito de suelo mide 2,25 m de altura total frente a los 1,35 m declarados '
             '(la cota 1,35 describe el cuerpo, no el cono superior), la torre de vivero 3,32 m frente a 3,00 m, y el '
             'arbolado existente llega a 8,51 m frente al rango 5â€“8.\n\n'
             'Lo importante no es cada desviaciÃ³n aislada sino que el documento de cotas y el modelo han divergido: '
             'conviene decidir cuÃ¡l de los dos manda antes de E03.' % (nfuera, nnc), w=0.40, fs=8)
        close(pdf, fig)

        # --- 4 cinta
        fig = sheet(pdf, '4 Â· CINTA / PASARELA ELEVADA')
        ax = fig.add_axes([0.035, 0.52, 0.45, 0.35]); context_plan(ax)
        RIB = np.asarray(M['circulacion']['ribbon'], float)
        ax.imshow(np.where(WALK, 1.0, np.nan), origin='lower', extent=EXT,
                  cmap=ListedColormap(['#EFF3EC']), zorder=2, interpolation='nearest')
        ax.plot(RIB[:, 0], RIB[:, 1], color=ROSA, lw=2.0, zorder=6)
        for s_ in A4r['stairs']:
            c = SEVC['RED'] if s_['d_top_a_cinta'] > 3.0 else SEVC['YELLOW']
            ax.plot(s_['x'], s_['y'], '^', ms=7, color=c, mec='white', mew=0.5, zorder=8)
            ax.text(s_['x'] + 1.5, s_['y'] + 1.5, '%.1f m' % s_['d_top_a_cinta'], fontsize=5.6, color=c, zorder=8)
        ax.set_title('traza de la cinta (+6,00) y las 6 escaleras Â· distancia coronaciÃ³nâ†’eje', fontsize=7,
                     loc='left', color=TEAL)
        axp = fig.add_axes([0.52, 0.62, 0.45, 0.25])
        pr = A4r['prof']
        S_ = [q['s'] for q in pr]
        axp.fill_between(S_, [q['bajo'] for q in pr], [q['z'] for q in pr], color='#A87840', alpha=0.85, lw=0)
        axp.plot(S_, [q['z'] + 1.05 for q in pr], color=GRIS, lw=0.6)
        axp.axhline(3.0, color=TEAL, lw=0.5, ls='--')
        axp.text(2, 3.15, 'gÃ¡libo mÃ­n. 3,00', fontsize=6, color=TEAL)
        axp.fill_between(S_, 0, 0.05, color='#BFBBB2')
        for s_ in A4r['stairs']:
            k = int(np.argmin([math.hypot(q['x'] - s_['x'], q['y'] - s_['y']) for q in pr]))
            axp.plot([pr[k]['s']], [6.0], '^', ms=6, color=ROSA)
        axp.set_ylim(0, 9); axp.set_xlim(0, S_[-1])
        axp.set_xlabel('desarrollo de la cinta (m)', fontsize=6.5); axp.set_ylabel('cota (m)', fontsize=6.5)
        axp.tick_params(labelsize=6)
        for s2 in ('top', 'right'):
            axp.spines[s2].set_visible(False)
        axp.set_title('PERFIL LONGITUDINAL Â· cota constante +6,00 Â· pendiente 0,0 %', fontsize=7, loc='left', color=TEAL)
        axt = fig.add_axes([0.035, 0.055, 0.45, 0.42])
        table(axt, [
            ['desarrollo total', '%.0f m' % A4r['long']],
            ['cota de rasante', '+6,00 m constante'],
            ['pendiente longitudinal', '0,0 % (plana en todo el desarrollo)'],
            ['pendiente transversal', '0,0 % (sin peralte ni pendiente de desagÃ¼e)'],
            ['ancho total del tablero', '2,50 m'],
            ['ancho Ãºtil entre barandillas', '%.2f m' % A4r['ancho_util']],
            ['altura de barandilla', '1,05 m (sin travesaÃ±o ni rodapiÃ©)'],
            ['gÃ¡libo bajo el tablero', '%.2f m' % A4r['galibo_bajo']],
            ['soportes', '%d montantes Ã˜0,34 con capitel' % A4r['n_soportes']],
            ['radio de curvatura mÃ­nimo', '%.1f m (p01 %.1f m)' % (A4r['radio_min_abs'], A4r['radio_min'])],
            ['cambios de nivel', '1 (0,00 â†’ +6,00)'],
            ['puntos de acceso', '6 escaleras Â· 0 rampas Â· 0 ascensores'],
            ['contrahuella', '0,385 m'],
            ['huella', '0,424 m'],
            ['2CH + H', '1,194 m (regla de comodidad: 0,62â€“0,65)'],
            ['pendiente de escalera', '90,9 % Â· 42,3Â°'],
            ['barandilla de escalera', 'no modelada'],
        ], [0.42, 0.58], ['PARÃMETRO DE LA CINTA', 'VALOR MEDIDO'], fs=7.4, rowh=0.052)
        axsec = fig.add_axes([0.52, 0.055, 0.45, 0.42])
        draw_section(axsec, 'x', float(RIB[len(RIB) // 2][0]), xr=(float(RIB[len(RIB) // 2][1]) - 12,
                                                                  float(RIB[len(RIB) // 2][1]) + 12),
                     zr=(0, 11), person_at=float(RIB[len(RIB) // 2][1]),
                     title='secciÃ³n transversal por la cinta (x = %.1f)' % RIB[len(RIB) // 2][0])
        close(pdf, fig)

        # --- 5-6-7 en una lamina
        fig = sheet(pdf, '5 Â· ACCESIBILIDAD   |   6 Â· METRO   |   7 Â· VISUALES')
        axa = fig.add_axes([0.035, 0.50, 0.29, 0.36]); axa.axis('off')
        table(axa, [[r['id'][:17], '%.2f' % r['w_min'], r['veredicto'][:13],
                     SEVC['RED'] if r['veredicto'].startswith('NO') else (SEVC['GREEN'] if r['veredicto'] == 'APTO' else SEVC['YELLOW'])]
                    for r in D['a5_access.json']['rows']],
              [0.40, 0.20, 0.40], ['itinerario', 'ancho mÃ­n', 'pre-chequeo'], fs=7.2, rowh=0.085)
        axm = fig.add_axes([0.355, 0.50, 0.29, 0.36]); axm.axis('off')
        table(axm, [[r['name'][:12], '%.2f' % min(r['d_suelo'], 99), '%d' % r['n_banda_suelo'],
                     '%d' % r['n_banda_aereo'],
                     GRIS if not r['en_ambito'] else (SEVC['GREEN'] if r['d_suelo'] >= 5.5 else
                                                      (SEVC['YELLOW'] if r['d_suelo'] >= 2 else SEVC['RED']))]
                    for r in A6['rows']], [0.36, 0.22, 0.21, 0.21],
              ['acceso Metro', 'd suelo', 'n suelo', 'n aÃ©reo'], fs=7.2, rowh=0.085)
        axv = fig.add_axes([0.68, 0.50, 0.29, 0.36]); axv.axis('off')
        table(axv, [[k, '%.1f %%' % v, SEVC['RED'] if v < 20 else (SEVC['YELLOW'] if v < 40 else SEVC['GREEN'])]
                    for k, v in A7['pct'].items()], [0.46, 0.54],
              ['objetivo visual', '% de la plaza'], fs=7.6, rowh=0.09)
        axv.text(0, 0.55, 'Puntos de observaciÃ³n: %d a 1,65 m.\nMembrana ETFE tratada como translÃºcida.\n'
                          'Dosel y copas E02 como opacos.' % A7['n'], fontsize=7, va='top',
                 color=GRIS, transform=axv.transAxes)
        axd = fig.add_axes([0.035, 0.055, 0.44, 0.38]); context_plan(axd)
        sec = A8['sectors']
        vmax = max(q['ocup'] for q in sec)
        for q in sec:
            c = plt.cm.OrRd(min(q['ocup'] / max(vmax, 1e-6), 1.0))
            axd.add_patch(Rectangle((q['x'] - 10, q['y'] - 10), 20, 20, facecolor=c, alpha=0.75,
                                    edgecolor='white', lw=0.4, zorder=4))
            axd.text(q['x'], q['y'], '%.0f' % q['ocup'], fontsize=5.4, ha='center', va='center',
                     zorder=5, color='#333')
        axd.set_title('8 Â· DENSIDAD â€” ocupaciÃ³n de suelo por sector de 20Ã—20 m (%)', fontsize=7, loc='left', color=TEAL)
        axdt = fig.add_axes([0.51, 0.055, 0.46, 0.38])
        rows = [['%.0f,%.0f' % (q['x'], q['y']), '%.0f' % q['ocup'], '%.0f' % q['ocup_master'],
                 '+%.0f' % q['delta_e02'], '%.0f' % q['cubierto'], '%.1f' % q['w_p50'],
                 max(['STRUCTURE', 'CANOPY', 'VEGETATION', 'PODS', 'PLANTER', 'FURNITURE', 'WATER'],
                     key=lambda ff: q['f_' + ff])[:9],
                 SEVC['RED'] if q['ocup'] >= 55 else (SEVC['YELLOW'] if q['ocup'] >= 40 else SEVC['GREEN'])]
                for q in sec[:16]]
        table(axdt, rows, [0.15, 0.10, 0.12, 0.10, 0.12, 0.11, 0.30],
              ['sector', 'ocup%', 'MASTER%', 'Î”E02', 'cub.%', 'ancho', 'familia dominante'], fs=6.8, rowh=0.055)
        axdt.text(0, 0.06, 'Global: ocupaciÃ³n %.1f %% (MASTER %.1f %%) Â· superficie cubierta %.1f %%.'
                  % (A8['global_']['ocup'], A8['global_']['ocup_master'], A8['global_']['cubierto']),
                  fontsize=7.2, va='top', transform=axdt.transAxes)
        close(pdf, fig)

        # --- 9-10 + 11 persona
        fig = sheet(pdf, '9 Â· MANTENIMIENTO   |   10 Â· COLISIONES   |   11 Â· PERSONA DE REFERENCIA')
        axm = fig.add_axes([0.035, 0.50, 0.44, 0.36]); axm.axis('off')
        cats = sorted(set(q['cat'] for q in A9))
        table(axm, [[c_[:22], '%d' % len([q for q in A9 if q['cat'] == c_]),
                     '%d' % len([q for q in A9 if q['cat'] == c_ and not q['acceso']]),
                     '%.2f' % np.median([q['holgura'] for q in A9 if q['cat'] == c_]),
                     SEVC['RED'] if len([q for q in A9 if q['cat'] == c_ and not q['acceso']]) >
                     len([q for q in A9 if q['cat'] == c_]) * 0.5 else SEVC['YELLOW']] for c_ in cats],
              [0.42, 0.16, 0.20, 0.22], ['componente', 'uds', 'sin acceso', 'holgura med.'], fs=7.4, rowh=0.085)
        axc = fig.add_axes([0.51, 0.50, 0.46, 0.36]); axc.axis('off')
        table(axc, [[p['a'][:11], p['b'][:11], '%.2f' % p['vol'],
                     'intencionado' if p['intencionado'] else 'REVISAR',
                     '#2b2b2b' if p['intencionado'] else SEVC['RED']] for p in A10['pairs'][:12]],
              [0.24, 0.24, 0.18, 0.34], ['familia A', 'familia B', 'mÂ³', 'lectura'], fs=7.4, rowh=0.076)
        pers = D['a11_person.json']
        axp = fig.add_axes([0.035, 0.055, 0.44, 0.38])
        table(axp, [[q['id'], q['modo'][:11], '%.2f' % q['ancho'],
                     ('%.2f' % q['galibo']) if q['galibo'] else 'cielo',
                     ('cuerpo ' + ('âœ“' if q['pasa_cuerpo'] else 'âœ—') + ' cabeza ' + ('âœ“' if q['pasa_cabeza'] else 'âœ—') +
                      ' silla ' + ('âœ“' if q['pasa_silla'] else 'âœ—') + ' cruce ' + ('âœ“' if q['pasa_cruce'] else 'âœ—')),
                     SEVC['RED'] if not (q['pasa_cuerpo'] and q['pasa_cabeza']) else SEVC['YELLOW']]
                    for q in pers[:16]], [0.10, 0.17, 0.12, 0.12, 0.49],
              ['ID', 'medido', 'ancho', 'gÃ¡libo', 'volumen humano 1,70 m'], fs=6.6, rowh=0.052)
        axp.text(0, 0.055, 'Las incidencias de PASO se miden en el propio punto; las de OBJETO (colisiÃ³n, mantenimiento,\n'
                           'metro) en su entorno de 2,5 m â€” allÃ­ lo que se comprueba es si cabe una persona junto a la pieza.',
                 fontsize=6.2, color=GRIS, va='top', transform=axp.transAxes)
        axs2 = fig.add_axes([0.51, 0.055, 0.46, 0.38])
        rr = [q for q in pers if not q['pasa_cabeza'] or not q['pasa_cuerpo']]
        q0 = rr[0] if rr else (pers[0] if pers else None)
        if q0:
            draw_section(axs2, 'y', q0['y'], xr=(q0['x'] - 10, q0['x'] + 10), zr=(0, 9), person_at=q0['x'],
                         title='secciÃ³n automÃ¡tica en %s (x=%.1f, y=%.1f)' % (q0['id'], q0['x'], q0['y']))
        close(pdf, fig)

        # --- registro de incidencias (paginado)
        per = 26
        for pg in range(0, len(ISSUES), per):
            fig = sheet(pdf, 'ISSUES_REGISTER Â· V-001â€¦V-%03d  (%dâ€“%d)' % (len(ISSUES), pg + 1, min(pg + per, len(ISSUES))),
                        sub='NADA SE HA CORREGIDO. Cada incidencia queda registrada con posiciÃ³n, magnitud, causa y '
                            'estrategias posibles, a la espera de revisiÃ³n.')
            axi = fig.add_axes([0.035, 0.05, 0.94, 0.83]); axi.axis('off')
            y = 0.985
            for r in ISSUES[pg:pg + per]:
                c = SEVC[r['sev']]
                pos = ('(%.0f, %.0f)' % (r['x'], r['y'])) if r['x'] is not None else 'â€”'
                axi.text(0.0, y, r['id'], fontsize=7.2, weight='bold', color=c, va='top', transform=axi.transAxes)
                axi.text(0.037, y, r['sev'], fontsize=6.4, color=c, va='top', transform=axi.transAxes)
                axi.text(0.075, y, r['cat'][:13], fontsize=6.4, color=GRIS, va='top', transform=axi.transAxes)
                axi.text(0.155, y, pos, fontsize=6.4, color=GRIS, va='top', transform=axi.transAxes)
                axi.text(0.215, y, r['title'][:88], fontsize=7.0, va='top', transform=axi.transAxes)
                axi.text(0.215, y - 0.0155, 'magnitud: ' + str(r['magnitud'])[:120], fontsize=6.2,
                         color=TINTA, va='top', transform=axi.transAxes)
                axi.text(0.215, y - 0.029, 'causa: ' + str(r['causa'])[:120], fontsize=6.2,
                         color=GRIS, va='top', transform=axi.transAxes)
                y -= 0.0378
            close(pdf, fig)
    return out


# ================================================================== CSV + MD
def write_csv():
    p = os.path.join(HERE, 'VIABILITY_METRICS.csv')
    rows = []
    s = SUM
    for k, v, u in [('objetos_malla', s['objetos'], 'ud'), ('triangulos', s['tris'], 'ud'),
                    ('area_ambito', s['area_ambito'], 'm2'), ('area_libre_cuerpo', s['area_libre'], 'm2'),
                    ('ocupacion_suelo', s['ocupacion'], '%'), ('cobertura_dosel', s['cobertura'], '%'),
                    ('ancho_libre_p05', s['ancho_p05'], 'm'), ('ancho_libre_p50', s['ancho_p50'], 'm'),
                    ('cuello_botella_min', s['cuello_min'], 'm'),
                    ('galibo_min', s['galibo_min'], 'm'), ('galibo_p05', s['galibo_p05'], 'm'),
                    ('vis_correos', s['vis']['CORREOS'], '%'), ('vis_torre', s['vis']['TORRE'], '%'),
                    ('vis_reloj', s['vis']['RELOJ'], '%'),
                    ('incidencias_RED', s['counts']['RED'], 'ud'),
                    ('incidencias_YELLOW', s['counts']['YELLOW'], 'ud'),
                    ('incidencias_GREEN', s['counts']['GREEN'], 'ud')]:
        rows.append(['GLOBAL', 'resumen', k, v, u, ''])
    for q in D['a1_paths.json']['paths']:
        for k in ('long', 'w_min', 'w_p05', 'w_p25', 'w_p50', 'w_p75', 'w_max', 'wl_min', 'eje_bloqueado'):
            rows.append(['A1_RECORRIDOS', q['id'], k, round(q[k], 3), 'm' if k != 'eje_bloqueado' else 'ud', ''])
    for q in D['a2_clear.json']['low'][:60]:
        rows.append(['A2_GALIBOS', q['obj'] or 'sin_id', 'altura_libre', round(q['h'], 3), 'm',
                     'x=%.1f y=%.1f area=%.1f' % (q['x'], q['y'], q['area'])])
    for q in D['a3_heights.json']['rows']:
        rows.append(['A3_ALTURAS', q['param'], 'declarado_vs_construido', q['construido'], 'm',
                     'decl=%s estado=%s' % (q['declarado'], q['estado'])])
    r4 = D['a4_ribbon.json']
    for k in ('long', 'ancho_util', 'galibo_bajo', 'radio_min_abs', 'pend_long_pct', 'pend_transv_pct'):
        rows.append(['A4_CINTA', 'RIBBON', k, round(r4[k], 3), 'm' if 'pend' not in k else '%', ''])
    for k, v in (('contrahuella', r4['stairs'][0]['contrahuella']), ('huella', r4['stairs'][0]['huella']),
                 ('pendiente_pct', r4['stairs'][0]['pendiente_pct'])):
        rows.append(['A4_CINTA', 'ESCALERA', k, round(v, 4), 'm' if k != 'pendiente_pct' else '%', ''])
    for q in D['a5_access.json']['rows']:
        rows.append(['A5_ACCESIBILIDAD', q['id'], 'veredicto', q['veredicto'], '',
                     'w_min=%.2f pct180=%.0f' % (q['w_min'], q['pct_w_ge_180'])])
    for q in D['a6_metro.json']['rows']:
        rows.append(['A6_METRO', q['name'], 'd_min_obstaculo_nivel_boca', q['d_suelo'], 'm',
                     'en_ambito=%s n_banda_suelo=%d frontal=%.1f' % (q['en_ambito'], q['n_banda_suelo'], q['libre_min'])])
        rows.append(['A6_METRO', q['name'], 'd_min_estructura_aerea', q['d_aereo'], 'm',
                     'z=%s n_banda_aereo=%d galibo=%s' % (q['z_aereo'], q['n_banda_aereo'], q['galibo'])])
    for k, v in D['a7_views.json']['pct'].items():
        rows.append(['A7_VISUALES', k, 'pct_visibilidad', round(v, 2), '%', 'n=%d' % D['a7_views.json']['n']])
    for q in D['a8_density.json']['sectors']:
        rows.append(['A8_DENSIDAD', 'sector_%.0f_%.0f' % (q['x'], q['y']), 'ocupacion', round(q['ocup'], 2), '%',
                     'master=%.1f delta=%.1f cubierto=%.1f' % (q['ocup_master'], q['delta_e02'], q['cubierto'])])
    for q in D['a9_maint.json']:
        rows.append(['A9_MANTENIMIENTO', q['id'], 'holgura_adyacente', round(q['holgura'], 2), 'm',
                     'cat=%s acceso=%s z=%.1f' % (q['cat'], q['acceso'], q['z'])])
    for q in D['a10_collisions.json']['pairs']:
        rows.append(['A10_COLISIONES', '%s x %s' % (q['a'], q['b']), 'volumen_solape', round(q['vol'], 4), 'm3',
                     'intencionado=%s voxeles=%d' % (q['intencionado'], q['voxels'])])
    for r in ISSUES:
        rows.append(['ISSUES', r['id'], r['sev'], r['metric'] if r['metric'] is not None else '', '',
                     '%s | %s' % (r['cat'], r['title'])])
    with open(p, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['bloque', 'elemento', 'metrica', 'valor', 'unidad', 'nota'])
        w.writerows(rows)
    return p, len(rows)


def write_md():
    p = os.path.join(HERE, 'ISSUES_REGISTER.md')
    red = [r for r in ISSUES if r['sev'] == 'RED']
    yel = [r for r in ISSUES if r['sev'] == 'YELLOW']
    grn = [r for r in ISSUES if r['sev'] == 'GREEN']
    L = ['# ISSUES_REGISTER â€” FASE 03B.5', '',
         'AuditorÃ­a geomÃ©trica y de viabilidad del modelo aprobado (`MASTER_ARCHITECTURE_v002.3dm` / '
         '`SOL_FULL_SCENE_v001.3dm`, escena E02 con 6.672 mallas y 394.610 triÃ¡ngulos).',
         '**2026-08-10 Â· NADA HA SIDO CORREGIDO Â· EL MASTER NO SE HA MODIFICADO.**', '',
         '| severidad | nÂº | criterio de clasificaciÃ³n |', '|---|---|---|',
         '| ðŸ”´ RED | %d | impide el uso previsto, o incumple un criterio declarado por el propio proyecto |' % len(red),
         '| ðŸŸ¡ YELLOW | %d | funciona pero al lÃ­mite, o depende de una decisiÃ³n pendiente |' % len(yel),
         '| ðŸŸ¢ GREEN | %d | anotaciÃ³n de coherencia documental, sin efecto sobre el uso |' % len(grn), '',
         '> Los umbrales usados (1,80 / 3,00 m de anchura Â· 3,00 m de gÃ¡libo Â· 5,5 m de banda de Metro) son criterios de '
         'trabajo tomados del HEIGHT_SYSTEM y de la decisiÃ³n D03B-02. **No se ha aplicado ninguna normativa**: '
         'la identificaciÃ³n de la norma aplicable es el paso siguiente.', '']
    for sev, ttl in (('RED', 'ðŸ”´ RED'), ('YELLOW', 'ðŸŸ¡ YELLOW'), ('GREEN', 'ðŸŸ¢ GREEN')):
        sub = [r for r in ISSUES if r['sev'] == sev]
        if not sub:
            continue
        L += ['## %s (%d)' % (ttl, len(sub)), '']
        for r in sub:
            pos = ('x=%.1f  y=%.1f' % (r['x'], r['y'])) + (('  z=%.2f' % r['z']) if r['z'] is not None else '') \
                if r['x'] is not None else 'sin posiciÃ³n puntual (afecta a un conjunto)'
            L += ['### %s Â· %s â€” %s' % (r['id'], r['cat'], r['title']), '',
                  '- **posiciÃ³n:** %s' % pos,
                  '- **magnitud:** %s' % r['magnitud'],
                  '- **causa:** %s' % r['causa'],
                  '- **severidad:** %s' % r['sev'],
                  '- **estrategias posibles (no aplicadas):** %s' % r['estrategias'],
                  '- **evidencia:** capÃ­tulo %s Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`' % r['ref'],
                  '']
    L += ['---', '', '## CÃ³mo se reproduce', '',
          '```bash', 'python audit_run.py      # mide y escribe _data/', 'python audit_report.py   # arma los PDF, el CSV y este registro', '```', '',
          'El motor reconstruye la escena en memoria interceptando `add_mesh` / `place` / `add_curve` de '
          '`build_all_03b.py`: audita exactamente la geometrÃ­a que produce el modelo aprobado, sin abrir ni escribir '
          'ningÃºn `.3dm`.']
    open(p, 'w', encoding='utf-8').write('\n'.join(L))
    return p


if __name__ == '__main__':
    outs = []
    for fn in (pdf_paths, pdf_clear, pdf_access, pdf_metro, pdf_views, pdf_collisions, pdf_maint, pdf_master):
        o = fn()
        outs.append(o)
        print('OK', os.path.basename(o), os.path.getsize(o) // 1024, 'KB', flush=True)
    p, n = write_csv()
    print('OK', os.path.basename(p), n, 'filas')
    print('OK', os.path.basename(write_md()))
