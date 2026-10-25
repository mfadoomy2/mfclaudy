# -*- coding: utf-8 -*-
"""03B6_BEFORE_AFTER.pdf — comparacion integral v002 (auditada) vs v003 (corregida)."""
import json
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
A_OLD = os.path.join(ROOT, 'FASE_03B5_AUDITORIA', '_data')
A_NEW = os.path.join(HERE, '_reaudit', '_data')
CBA = json.load(open(os.path.join(HERE, '_clima_beforeafter.json'), encoding='utf-8'))
M = json.load(open(os.path.join(HERE, 'geometria_maestra_v003.json'), encoding='utf-8'))
a4 = json.load(open(os.path.join(A_NEW, 'a4_ribbon.json'), encoding='utf-8'))
a5n = json.load(open(os.path.join(A_NEW, 'a5_access.json'), encoding='utf-8'))
a5o = json.load(open(os.path.join(A_OLD, 'a5_access.json'), encoding='utf-8'))
a9n = json.load(open(os.path.join(A_NEW, 'a9_maint.json'), encoding='utf-8'))
a9o = json.load(open(os.path.join(A_OLD, 'a9_maint.json'), encoding='utf-8'))
a10n = json.load(open(os.path.join(A_NEW, 'a10_collisions.json'), encoding='utf-8'))
a10o = json.load(open(os.path.join(A_OLD, 'a10_collisions.json'), encoding='utf-8'))
spo = json.load(open(os.path.join(ROOT, 'FASE_03B5B_CLIMA', '_data', 'spots.json'), encoding='utf-8'))
spn = json.load(open(os.path.join(HERE, '_reclima', '_data', 'spots.json'), encoding='utf-8'))
sn = json.load(open(os.path.join(A_NEW, 'summary.json'), encoding='utf-8'))

INK, PINK, GRN, ORG = '#1A1A1A', '#D6577F', '#6F8F53', '#D98E32'


def rows_maint(a):
    rr = a if isinstance(a, list) else a.get('rows', a.get('maint', []))
    tot = len(rr)
    mal = sum(1 for r in rr if not r.get('acceso'))
    return tot, mal


def sheet(pdf, title, sub=''):
    fig = plt.figure(figsize=(16.54, 11.69))
    fig.patch.set_facecolor('#F7F4EE')
    fig.text(0.03, 0.965, 'FASE 03B.6 — BEFORE / AFTER  ·  v002 auditada → v003 corregida', fontsize=9,
             color=PINK, family='monospace')
    fig.text(0.03, 0.925, title, fontsize=21, color=INK, family='monospace', weight='bold')
    if sub:
        fig.text(0.03, 0.900, sub, fontsize=9.5, color='#555', family='monospace')
    fig.text(0.97, 0.965, 'REFUGIO CLIMATICO · PUERTA DEL SOL · 2026-08-11', fontsize=8,
             color='#777', family='monospace', ha='right')
    return fig


def tabla(ax, filas, col_w, y0=0.96, dy=0.052, fs=9.3, header=None):
    ax.axis('off')
    y = y0
    if header:
        x = 0.0
        for h, w in zip(header, col_w):
            ax.text(x, y, h, fontsize=fs, family='monospace', weight='bold', color=PINK,
                    transform=ax.transAxes, va='top')
            x += w
        y -= dy
    for fila in filas:
        x = 0.0
        for c, w in zip(fila, col_w):
            col = INK
            s = str(c)
            if s.startswith('++'):
                col, s = GRN, s[2:]
            elif s.startswith('--'):
                col, s = '#B03030', s[2:]
            ax.text(x, y, s, fontsize=fs, family='monospace', color=col,
                    transform=ax.transAxes, va='top')
            x += w
        y -= dy
    return y


out = os.path.join(HERE, '03B6_BEFORE_AFTER.pdf')
with PdfPages(out) as pdf:
    # ---------------- P1 · RESUMEN EJECUTIVO ----------------
    fig = sheet(pdf, 'RESUMEN EJECUTIVO', 'las dos auditorias (03B.5 geometrica + 03B.5B climatica) re-ejecutadas integramente sobre v003')
    ax = fig.add_axes([0.04, 0.10, 0.44, 0.76])
    v2c, v3c = {'RED': 36, 'YELLOW': 22, 'GREEN': 15}, sn['counts']
    tot_o, mal_o = rows_maint(a9o)
    tot_n, mal_n = rows_maint(a9n)
    filas = [
        ('Incidencias ROJAS', '36', '++0'),
        ('Incidencias AMARILLAS', '22', '26'),
        ('Incidencias VERDES', '15', '++19'),
        ('Itinerarios APTOS', '2 de 6', '++6 de 6'),
        ('Cinta: acceso accesible', 'NO (0 medios)', '++3 ascensores'),
        ('Escaleras: contrahuella', '0.385 m (91%)', '++0.171 m (35 CH)'),
        ('Cinta: radio minimo', '2.29 m', '++4.84 m'),
        ('Cinta: barandilla', 'solo pasamanos', '++3 niveles'),
        ('Boca Cercanias: invasores', '5 en banda', '++0 fisicos'),
        ('Colisiones no intencionadas', str(len(a10o.get('hot', []))), '++%d' % len(a10n.get('hot', []))),
        ('Mantenimiento sin acceso', '%d de %d' % (mal_o, tot_o), '++%d de %d' % (mal_n, tot_n)),
        ('Carlos III', 'ausente', '++presente (G2+ pdte. verif. municipal)'),
    ]
    tabla(ax, filas, [0.52, 0.24, 0.24], header=('GEOMETRIA (03B.5)', 'v002', 'v003'))
    ax2 = fig.add_axes([0.53, 0.10, 0.44, 0.76])
    c2, c3 = CBA['v002'], CBA['v003']
    filas2 = [
        ('Sombra critica (ambito)', '%.1f %%' % c2['sombra']['B_pct'], '++%.1f %%' % c3['sombra']['B_pct']),
        ('Sombra EXCLUSIVA', '%.1f %%' % c2['sombra']['exclusiva_pct'], '++%.1f %%' % c3['sombra']['exclusiva_pct']),
        ('MRT media E2 16h', '%.1f C' % c2['E2']['Tmrt_B'], '++%.1f C' % c3['E2']['Tmrt_B']),
        ('UTCI media E2 16h', '%.1f C' % c2['E2']['UTCI_B'], '++%.1f C' % c3['E2']['UTCI_B']),
        ('m2 con UTCI >= 40 C (E2)', '%.0f' % c2['E2']['m2_UTCI_B_ge40'], '++%.0f' % c3['E2']['m2_UTCI_B_ge40']),
        ('Refugio efectivo', '%.0f m2 (36.4%%)' % c2['metricas']['m2_refugio'], '++%.0f m2 (39.1%%)' % c3['metricas']['m2_refugio']),
        ('Poblacion beneficiada', '%.1f %%' % c2['metricas']['pct_beneficiada'], '++%.1f %%' % c3['metricas']['pct_beneficiada']),
        ('CINTA: sombra', '%.0f %%' % c2['cinta']['pct_sombra'], '++%.0f %%' % c3['cinta']['pct_sombra']),
        ('CINTA: MRT', '%.1f C' % c2['cinta']['MRT'], '++%.1f C' % c3['cinta']['MRT']),
        ('CINTA: UTCI', '%.1f C' % c2['cinta']['UTCI'], '++%.1f C' % c3['cinta']['UTCI']),
        ('Hotspots (uds / m2)', '%d / %.0f' % (len(spo['hot']), spo.get('hot_m2', 0)), '++%d / %.0f' % (len(spn['hot']), spn.get('hot_m2', 0))),
        ('Invierno: perdida solar', '%.1f %%' % c2['invierno']['perdida_pct'], '--%.1f %%' % c3['invierno']['perdida_pct']),
    ]
    tabla(ax2, filas2, [0.46, 0.27, 0.27], header=('CLIMA (03B.5B)', 'v002', 'v003'))
    fig.text(0.04, 0.055, 'VEREDICTO GEOMETRICO: 0 incidencias rojas tras 9 iteraciones REGENERAR->REAUDITAR. '
                          'VEREDICTO CLIMATICO: mejora en todos los frentes salvo invierno (-1.9 pts, precio de 27 discos nuevos, acotado por las 2 ventanas de invierno).',
             fontsize=9.5, family='monospace', color=INK)
    pdf.savefig(fig); plt.close(fig)

    # ---------------- P2 · PLANTA DE CAMBIOS ----------------
    fig = sheet(pdf, 'QUE CAMBIO Y DONDE', 'planta v003: cada cambio es una REGLA del generador, no un parche puntual')
    ax = fig.add_axes([0.03, 0.06, 0.70, 0.82])
    ax.set_facecolor('#F7F4EE')
    for c in M['circulacion']['corridors']:
        P = np.array(c['pts'], float)
        ax.plot(P[:, 0], P[:, 1], '-', color='#9AA7B0', lw=5, alpha=0.5, zorder=1)
    prof = np.array([(r['x'], r['y']) for r in a4['prof']])
    ax.plot(prof[:, 0], prof[:, 1], '-', color=PINK, lw=2.2, zorder=3)
    for d in M['paisaje']['discs']:
        rol = d.get('rol_v003', '')
        col = ORG if 'cinta' in rol else (GRN if 'corredor' in rol else '#C9C2B4')
        z = 4 if rol else 2
        ax.add_patch(Circle((d['cx'], d['cy']), d['r'], fc=col, ec='none', alpha=0.75 if rol else 0.35, zorder=z))
    for (sx, sy) in M['circulacion']['stairs']:
        ax.plot(sx, sy, 's', ms=9, mfc='#5B4A3A', mec='white', zorder=6)
    for (lx, ly, lbl) in [(-75, 10, 'ASC C1-O'), (5, 30, 'ASC C2-N'), (72, 8, 'ASC C3-E')]:
        ax.plot(lx, ly, '^', ms=13, mfc=PINK, mec='white', zorder=6)
        ax.annotate(lbl, (lx, ly), textcoords='offset points', xytext=(6, 7), fontsize=7.5, family='monospace')
    ex, ey = M['estatua_v003']['xy']
    ax.plot(ex, ey, '*', ms=17, mfc='#8A6D3B', mec='white', zorder=6)
    ax.add_patch(Circle((ex, ey), 8, fill=False, ec='#8A6D3B', ls=':', lw=1.2, zorder=5))
    ax.annotate('CARLOS III + r8', (ex, ey), textcoords='offset points', xytext=(8, -13), fontsize=7.5, family='monospace')
    for (vx, vy) in M['mantenimiento_v003']['viveros']:
        ax.plot(vx, vy, 'D', ms=7, mfc=GRN, mec='white', zorder=6)
    for (rx, ry) in M['mantenimiento_v003']['registros_tecnicos']:
        ax.plot(rx, ry, 'P', ms=8, mfc='#D6577F', mec='white', zorder=6)
    for ln in M['mantenimiento_v003']['recirculacion']:
        P = np.array(ln, float)
        ax.plot(P[:, 0], P[:, 1], '--', color=PINK, lw=1.0, alpha=0.7, zorder=4)
    for e in M['contexto']['metro']:
        if -110 < e['x'] < 100 and -45 < e['y'] < 75:
            ax.add_patch(Circle((e['x'], e['y']), 5.5, fill=False, ec='#5B5B8F', lw=1.0, alpha=0.6, zorder=5))
    ax.annotate('escalera reubicada\n(44,-6)->(46,-7) V-020', (46.1, -7), textcoords='offset points',
                xytext=(10, -22), fontsize=7.5, family='monospace', color='#5B4A3A')
    ax.annotate('eje por el sur\nde la estatua', (-28, -18.6), textcoords='offset points',
                xytext=(-70, -14), fontsize=7.5, family='monospace', color='#556')
    ax.annotate('E-3 fuera de boca\nCarmen', (10.4, 20.4), textcoords='offset points',
                xytext=(-86, 6), fontsize=7.5, family='monospace', color='#556')
    ax.set_xlim(-110, 100); ax.set_ylim(-45, 75); ax.set_aspect('equal'); ax.axis('off')
    axl = fig.add_axes([0.74, 0.10, 0.24, 0.76])
    tabla(axl, [
        ('leyenda',), ('— rosa: cinta v003 (r>=4.7, tangente a balsas)',),
        ('o naranja: sombra-CINTA +8.30 (23 nuevos + 7 recotados)',),
        ('o verde: discos sombra-CORREDOR +5.0 (4 nuevos)',), ('cuadrado: 6 escaleras reales 35CH',),
        ('triangulo: 3 ascensores-capsula',), ('estrella: Carlos III + resp. r8',),
        ('rombo: viveros re-implantados (istmo)',), ('P: registros tecnicos + recirculacion --',),
        ('circulo azul: bandas de boca 5.5 (PROVISIONAL)',), ('',),
        ('otras reglas sin dibujo:',), ('· puertas en trenes (retirada de capsulas)',),
        ('· poda min 2.55 en copas A',), ('· respaldos en 50% de bancos',),
        ('· canaleta enrasada en cruces (V-019)',), ('· bancos cortados en cubas y tuberias',),
        ('· gotas a 3.05 m · pates desde 2.2 m',), ('· plataformas de deposito + puerta D-C1-1',),
        ('· NEB fuera de bocas y de ejes',), ('· colgantes +15% (fuera del canto)',),
        ('· 8 nebulizadores de barandilla',), ('· conos visuales + 2 ventanas de invierno',),
    ], [1.0], dy=0.036, fs=8.2)
    pdf.savefig(fig); plt.close(fig)

    # ---------------- P3 · POR QUE / QUE MEJORO / QUE EMPEORO / ABIERTO ----------------
    fig = sheet(pdf, 'POR QUE · QUE MEJORO · QUE EMPEORO · QUE QUEDA ABIERTO')
    ax = fig.add_axes([0.04, 0.06, 0.44, 0.82])
    tabla(ax, [
        ('POR QUE (causas raiz CR-1..CR-9)',), ('',),
        ('CR-1 no habia chequeo cruzado entre familias',), ('   -> conflict_guard en posicion FINAL (44 ajustes)',), ('',),
        ('CR-2 toda barrera lineal necesita puertas',), ('   -> trenes: retirada de capsulas (posiciones intactas)',),
        ('   -> jardineras: 10 puertas anti-trampa',), ('',),
        ('CR-3 la cinta se dibujo sin proyecto de acceso',), ('   -> escaleras reales + ascensores + barandilla',),
        ('   -> radio >=4.7 (laplaciano selectivo, no Chaikin)',), ('',),
        ('CR-4 near_corr excluia el frescor de los corredores',), ('   -> derogacion aerea: sombra SOBRE el movimiento',), ('',),
        ('CR-5 HEIGHT_SYSTEM describia un ideal, no lo construido',), ('   -> HEIGHT_SYSTEM_v2: manda la geometria aprobada',), ('',),
        ('CR-6 mantenimiento: protocolo antes que mudanza',), ('   -> MAINTENANCE_PROTOCOL + piezas tecnicas',), ('',),
        ('CR-7 metro: banda 5.5 PROVISIONAL, bocas libres',), ('   -> guard para toda familia con base <+2.50',), ('',),
        ('CR-8 sombra vs visuales vs invierno sin arbitro',), ('   -> conos intencionados + 2 ventanas de invierno',), ('',),
        ('CR-9 deudas menores con nombre propio',), ('   -> canaleta, respaldos, Carlos III (DEC-0006)',),
    ], [1.0], dy=0.0285, fs=8.6)
    ax2 = fig.add_axes([0.53, 0.06, 0.44, 0.82])
    tabla(ax2, [
        ('QUE MEJORO',), ('',),
        ('· 36 rojas -> 0 (todas las familias de causa)',),
        ('· 6/6 itinerarios APTOS; cinta accesible (3 asc.)',),
        ('· Cercanias: de 5 invasores a boca limpia',),
        ('· mantenimiento: de 56/133 sin acceso a 1/160',),
        ('  (el 1: DISC-23 canopy, holgura 2.06 — YELLOW)',),
        ('· colisiones reales: resueltas o intencionadas doc.',),
        ('· sombra critica +2.7 pts; exclusiva +2.5 pts',),
        ('· MRT cinta -3.5 K; UTCI cinta -0.8 K (CL-004)',),
        ('· refugio efectivo +308 m2; beneficiada +3.1 pts',),
        ('· UTCI>=40: -290 m2 en E2; hotspot mayor -171 m2',),
        ('· coolspot istmo (viveros) 460 -> 968 m2',), ('',),
        ('QUE EMPEORO',), ('',),
        ('-- invierno: perdida 48.2 -> 50.1 % (+1.9 pts):',),
        ('   27 discos nuevos; acotado por las 2 ventanas',),
        ('-- agua: 1722 -> 2034 L/h (+18%): 8 neb de cinta;',),
        ('   compensado con recirculacion por cluster',),
        ('-- vis reloj 38.6 -> 34.9 % global: se acepta;',),
        ('   la red de 9 conos intencionados esta protegida',), ('',),
        ('QUE QUEDA ABIERTO (documentado, no oculto)',), ('',),
        ('· 10 huecos 0.5 interiores a parterres (textura)',),
        ('· 26 amarillas (menores o preexistentes)',),
        ('· drenaje del tablero: documentado, no modelado',),
        ('· banda de metro sigue PROVISIONAL (plano oficial)',),
        ('· estatua: precision pendiente de plano municipal',),
        ('· CL-006 autonomia de agua: ahora con recirculacion,',),
        ('  dimensionado fino en proyecto tecnico',),
    ], [1.0], dy=0.0285, fs=8.6)
    pdf.savefig(fig); plt.close(fig)

    # ---------------- P4 · CLIMA GRAFICO ----------------
    fig = sheet(pdf, 'CLIMA v002 vs v003 — condicion de diseno E2 (tarde calurosa, 16:00)')
    mets = [('Sombra critica %', c2['sombra']['B_pct'], c3['sombra']['B_pct']),
            ('MRT media C', c2['E2']['Tmrt_B'], c3['E2']['Tmrt_B']),
            ('UTCI media C', c2['E2']['UTCI_B'], c3['E2']['UTCI_B']),
            ('UTCI>=40 (x100 m2)', c2['E2']['m2_UTCI_B_ge40'] / 100, c3['E2']['m2_UTCI_B_ge40'] / 100),
            ('Refugio (x100 m2)', c2['metricas']['m2_refugio'] / 100, c3['metricas']['m2_refugio'] / 100),
            ('Beneficiada %', c2['metricas']['pct_beneficiada'], c3['metricas']['pct_beneficiada']),
            ('Cinta sombra %', c2['cinta']['pct_sombra'], c3['cinta']['pct_sombra']),
            ('Cinta MRT C', c2['cinta']['MRT'], c3['cinta']['MRT']),
            ('Invierno perdida %', c2['invierno']['perdida_pct'], c3['invierno']['perdida_pct'])]
    ax = fig.add_axes([0.06, 0.12, 0.88, 0.72])
    xs = np.arange(len(mets))
    ax.bar(xs - 0.18, [m[1] for m in mets], 0.34, color='#C9C2B4', label='v002')
    ax.bar(xs + 0.18, [m[2] for m in mets], 0.34, color=PINK, label='v003')
    for x, m in zip(xs, mets):
        ax.text(x - 0.18, m[1] + 0.6, '%.1f' % m[1], ha='center', fontsize=8, family='monospace')
        ax.text(x + 0.18, m[2] + 0.6, '%.1f' % m[2], ha='center', fontsize=8, family='monospace', color=PINK)
    ax.set_xticks(xs)
    ax.set_xticklabels([m[0] for m in mets], fontsize=8.2, family='monospace', rotation=14)
    ax.legend(frameon=False, fontsize=10)
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_facecolor('#F7F4EE')
    fig.text(0.06, 0.055, 'Metodo: mismos scripts 03B.5B clonados (originales intactos), PVGIS identico, lecciones aplicadas '
                          '(optica por BLOQUE, SVF sin membrana como cielo, sombra EXCLUSIVA recalculada). Voxelizacion A/B regenerada para v003.',
             fontsize=8.8, family='monospace', color='#555')
    pdf.savefig(fig); plt.close(fig)

print('PDF:', out, os.path.getsize(out))
