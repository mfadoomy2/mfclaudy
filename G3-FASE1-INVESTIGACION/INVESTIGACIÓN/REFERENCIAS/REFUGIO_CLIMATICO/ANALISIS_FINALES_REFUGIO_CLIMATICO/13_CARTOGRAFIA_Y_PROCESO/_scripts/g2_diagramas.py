# -*- coding: utf-8 -*-
"""DIAGRAMAS DE SISTEMA v006 — lo que un mapa no puede explicar: el ciclo del agua, la
cadena energetica del confort, el arbol de familias, la linea de tiempo de versiones, el
ciclo del proceso y el arbol de decision municipal. Dibujados, no fotografiados."""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
sys.path.insert(0, os.path.join(BASE, '12_ANEXOS_DATOS_Y_METODO', '_scripts'))
import refugio_editorial as E  # noqa: E402
from comp_core import Comp, MXW, CL, BD, AU  # noqa: E402

OUT = os.path.join(BASE, '13_CARTOGRAFIA_Y_PROCESO')
c = Comp(os.path.join(OUT, 'DIAGRAMAS_DE_SISTEMA_v006.pdf'), 'DIAGRAMAS DE SISTEMA',
         'DIAGRAMÁTICA v006')

E.portada(c.doc, 'Diagramas\nde sistema',
          'Lo que un mapa no puede explicar: cómo circula el agua, cómo se convierte la '
          'radiación en confort, de qué está hecho el kit de partes, cómo evolucionó el '
          'modelo versión a versión, cómo funciona el ciclo de trabajo y qué debe decidir '
          'el Ayuntamiento en cada fase.',
          'DIAGRAMÁTICA TÉCNICA · SEIS SISTEMAS EXPLICADOS',
          [('DIAGRAMAS', '6'), ('BASELINE', 'v006 · build 12'),
           ('DATOS', 'medidos, no ilustrativos'), ('FORMATO', 'A4 vertical')],
          num='DIAGRAMAS')


def caja(ax, x, y, w, h, texto, fc=E.PANEL, ec=E.HAIR, size=7.4, tc=None, bold=False,
         lw=0.8):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.0,rounding_size=0.02',
                                fc=fc, ec=ec, lw=lw, zorder=3))
    ax.text(x + w / 2, y + h / 2, texto, ha='center', va='center', size=size,
            color=tc or E.INK, family=E.SERIF, zorder=4,
            weight='bold' if bold else 'normal', linespacing=1.35)


def flecha(ax, x1, y1, x2, y2, color=None, lw=1.1, texto='', size=5.4, curva=0.0):
    from matplotlib.patches import FancyArrowPatch
    color = color or E.GRAYTX
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), color=color, lw=lw, zorder=2,
                                 arrowstyle='-|>', mutation_scale=8,
                                 connectionstyle='arc3,rad=%.2f' % curva))
    if texto:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.012, texto, ha='center', va='bottom',
                size=size, color=color, family=E.SERIF, zorder=5)


def lienzo(alto):
    ax = c.p.axes(E.MX, c.y - alto, MXW, alto)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    c.y -= alto + 0.12
    return ax


# ============================================================ 1 · CICLO DEL AGUA
c.seccion('D-01 · CICLO DEL AGUA', 'De la red al aire, y lo que vuelve', size=16,
          sub='Los caudales son los medidos en el día punta; los porcentajes, la parte de '
              'cada término en el total de 30,1 m³.')
bal = BD['agu_stats']['balance_dia_punta_m3']
ax = lienzo(6.7)
caja(ax, 0.02, 0.80, 0.20, 0.11, 'RED MUNICIPAL\nacometida', fc='white', bold=True)
caja(ax, 0.02, 0.62, 0.20, 0.11, 'DEPÓSITOS\nautonomía 3,3 días', fc=E.PALEAGUA)
caja(ax, 0.28, 0.80, 0.20, 0.11, 'GRUPO DE PRESIÓN\ny filtración')
caja(ax, 0.28, 0.62, 0.20, 0.11, 'RECIRCULACIÓN\nenterrada, con tapas', fc=E.PALEAGUA)
flecha(ax, 0.22, 0.855, 0.28, 0.855)
flecha(ax, 0.12, 0.80, 0.12, 0.735)
flecha(ax, 0.22, 0.675, 0.28, 0.675)
flecha(ax, 0.38, 0.80, 0.38, 0.735)
usos = [('LÁMINAS Y ESTANQUES\n%.1f m³/día' % bal['evaporacion_laminas'], E.PALEAGUA, 0.56),
        ('RIEGO · 17 ESPECIES\n%.1f m³/día' % bal['riego_vegetal'], E.PALEGREEN, 0.36),
        ('NEBULIZACIÓN\n%.2f m³/día · solo día seco' % bal['nebulizacion'], '#f2e8f0', 0.16)]
for tx, col, yy in usos:
    caja(ax, 0.56, yy, 0.30, 0.115, tx, fc=col)
    flecha(ax, 0.48, 0.675, 0.56, yy + 0.058, curva=0.12)
caja(ax, 0.56, 0.80, 0.30, 0.11, 'SPLASH JUGABLE\nlámina de 3 cm', fc=E.PALEAGUA)
flecha(ax, 0.48, 0.855, 0.56, 0.855)
caja(ax, 0.90, 0.36, 0.085, 0.55, 'A T M Ó S F E R A\n\nevaporación\n1.367 kW\n\n−1,09 K\nde aire local',
     fc='white', ec=E.AGUA, size=5.8)
for yy in (0.855, 0.618, 0.418, 0.218):
    flecha(ax, 0.86, yy, 0.90, 0.62, color=E.AGUA, curva=-0.18)
caja(ax, 0.02, 0.30, 0.46, 0.10, 'DRENAJE · sumideros y canales › retorno a recirculación',
     fc='white')
flecha(ax, 0.56, 0.36, 0.48, 0.35, curva=0.1)
flecha(ax, 0.25, 0.30, 0.25, 0.235, color=E.GRAYTX)
caja(ax, 0.02, 0.12, 0.46, 0.10, 'PROTOCOLO DE SEQUÍA · corte por orden inverso al valor irreemplazable',
     fc=E.PANEL, ec=E.MAGENTA)
ax.text(0.5, 0.045, 'niebla  ›  láminas ornamentales  ›  herbáceas  ›  arbustos  ›  NUNCA el arbolado',
        ha='center', size=6.4, color=E.MAGENTA, family=E.SERIF, weight='bold')
c.y = c.p.caption(E.MX, c.y, 'El agua es termostato, no estructura.',
                  'El núcleo del confort —la sombra— funciona con los depósitos vacíos. '
                  'Todo lo que este diagrama describe compra el margen fino: superficies '
                  'frías, juego, ecología y los 501 m² adicionales de la nebulización. Su '
                  'coste anual (unos 9.000 €) es ruido frente a los 200.000 € de mano de '
                  'obra de conservación.', wrap=108)

# ============================================================ 2 · CADENA DEL CONFORT
c.seccion('D-02 · CADENA DEL CONFORT', 'Cómo la radiación se convierte en sensación')
ax = lienzo(6.5)
ax.text(0.02, 0.95, 'ENTRADA', size=6.0, color=E.GRAYTX, family=E.SERIF)
caja(ax, 0.02, 0.80, 0.17, 0.12, 'SOL\n936 W/m² directa\n117 difusa', fc='#fdf0dc', bold=True)
caja(ax, 0.02, 0.62, 0.17, 0.12, 'AIRE\n33 °C · 16 % HR\n2,9 m/s', fc='white')
ax.text(0.24, 0.95, 'FILTROS DEL PROYECTO', size=6.0, color=E.GRAYTX, family=E.SERIF)
filtros = [('DOSEL\ntransmitancia 0,12\n− 85 % del efecto', E.PALEGREEN, 0.80),
           ('VEGETACIÓN\nBeer-Lambert por especie\nk 0,25 – 0,75', E.PALEGREEN, 0.62),
           ('AGUA\nevaporación\n1.367 kW', E.PALEAGUA, 0.44),
           ('NIEBLA\nisoentálpica\ncondicional', '#f2e8f0', 0.26)]
for tx, col, yy in filtros:
    caja(ax, 0.24, yy, 0.22, 0.12, tx, fc=col)
    flecha(ax, 0.19, 0.86 if yy > 0.6 else 0.68, 0.24, yy + 0.06, curva=0.1)
ax.text(0.51, 0.95, 'BALANCE', size=6.0, color=E.GRAYTX, family=E.SERIF)
caja(ax, 0.51, 0.62, 0.21, 0.30,
     'BALANCE RADIATIVO\n\nonda corta directa,\ndifusa y reflejada\n+\nonda larga de cielo,\n'
     'suelo y superficies\n\nrayo que atraviesa dosel:\ntransmite sol, no ve cielo',
     fc='white', ec=E.MAGENTA, size=6.7)
for yy in (0.86, 0.68, 0.50, 0.32):
    flecha(ax, 0.46, yy, 0.51, 0.77, curva=-0.12)
ax.text(0.77, 0.95, 'SALIDA', size=6.0, color=E.GRAYTX, family=E.SERIF)
caja(ax, 0.77, 0.78, 0.21, 0.14, 'MRT\n65,2 › 54,3 °C\nΔ −10,9 K', fc='#fdece4', bold=True)
caja(ax, 0.77, 0.58, 0.21, 0.14, 'UTCI\n40,0 › 37,4 °C\nΔ −2,5 K', fc='#fdece4', bold=True)
caja(ax, 0.77, 0.38, 0.21, 0.14, 'AIRE LOCAL\nΔ −1,09 K\n(sensible + latente)', fc='white')
flecha(ax, 0.72, 0.80, 0.77, 0.85)
flecha(ax, 0.72, 0.72, 0.77, 0.65)
flecha(ax, 0.72, 0.66, 0.77, 0.45, curva=-0.1)
caja(ax, 0.24, 0.06, 0.74, 0.14,
     'PROPORCIÓN MEDIDA DEL BENEFICIO:  radiación ≈ 90 %   ·   aire ≈ 10 %',
     fc=E.PANEL, ec=E.MAGENTA, size=7.4, bold=True)
c.y = c.p.caption(E.MX, c.y, 'La sombra no baja la temperatura: cambia lo que el cuerpo recibe.',
                  'Este diagrama explica por qué el proyecto invierte en geometría y no en '
                  'refrigeración: a 33 °C de aire, la diferencia entre sol y sombra son '
                  'unos 25 K de temperatura radiante. El aire apenas se mueve — y este '
                  'dossier no promete otra cosa.', wrap=108)

# ============================================================ 3 · ARBOL DE FAMILIAS
c.seccion('D-03 · KIT DE PARTES', 'De qué está hecho: 15.197 piezas con nombre')
fam = BD['tec_stats'].get('familias', [])
ax = lienzo(6.1)
if fam:
    tot = sum(f.get('n_objetos', 0) for f in fam) or 1
    y0 = 0.92
    for f in fam[:13]:
        n = f.get('n_objetos', 0)
        w = 0.62 * n / max(x.get('n_objetos', 1) for x in fam)
        ax.barh(y0, w, height=0.052, left=0.30, color=E.GREEN, zorder=3)
        ax.text(0.285, y0, f.get('familia', '')[:34], ha='right', va='center', size=6.0,
                family=E.SERIF)
        ax.text(0.30 + w + 0.01, y0, '%s uds · %.1f %%' % ('{:,}'.format(n).replace(',', '.'),
                                                           100.0 * n / tot),
                ha='left', va='center', size=5.6, color=E.GRAYTX, family=E.SERIF)
        y0 -= 0.068
c.y = c.p.caption(E.MX, c.y, 'Un kit repetitivo es un kit mantenible.',
                  '93 hojas iguales en tres tamaños, 42 nebulizadores idénticos, mástiles '
                  'de familia única: el almacén de repuestos es corto y la cuadrilla de '
                  'conservación se forma una sola vez. La repetición no es pobreza formal, '
                  'es la condición de que el proyecto sobreviva veinticinco años.', wrap=108)

# ============================================================ 4 · LINEA DE TIEMPO
c.seccion('D-04 · EVOLUCIÓN DEL MODELO', 'Seis versiones, cada una por una razón medida')
ax = lienzo(4.9)
VERS = [('v001-002', 'geometría maestra\ny kit de partes', '6.857 objetos\n89 pasos <1,20 m'),
        ('v003', 'resolución de\nla auditoría', 'cinta, ascensores\nguardas cruzadas'),
        ('v004', 'conflictos urbanos\ny detailing', 'módulo A12 nuevo\n0 penetraciones'),
        ('v005', 'purga forense\ny microdetalle', '443 duplicados › 0\n48 defectos resueltos'),
        ('v006', 'botánica real e\nhiperdetalle', '0 RED · 26 YELLOW\n15.197 mallas'),
        ('FINAL', 'regeneración\nanalítica', '279 análisis\n48 métricas')]
ax.plot([0.06, 0.94], [0.62, 0.62], '-', color=E.HAIR, lw=1.4, zorder=1)
for i, (v, que, res) in enumerate(VERS):
    x = 0.06 + i * (0.88 / (len(VERS) - 1))
    col = E.MAGENTA if v in ('v006', 'FINAL') else E.GREEN
    ax.plot(x, 0.62, 'o', ms=8, mfc='white', mec=col, mew=1.8, zorder=4)
    ax.text(x, 0.70, v, ha='center', size=7.2, weight='bold', family=E.SERIF, color=col)
    ax.text(x, 0.55, que, ha='center', va='top', size=6.6, family=E.SERIF,
            linespacing=1.4)
    ax.text(x, 0.36, res, ha='center', va='top', size=5.5, family=E.SERIF,
            color=E.GRAYTX, linespacing=1.4)
ax.text(0.5, 0.90, 'CADA VERSIÓN EXISTE PORQUE UNA AUDITORÍA DEMOSTRÓ QUE LA ANTERIOR FALLABA',
        ha='center', size=6.6, color=E.MAGENTA, family=E.SERIF, weight='bold')
ax.text(0.5, 0.14, 'La numeración no es cosmética: entre v002 y v006 el modelo se regeneró '
        'por completo doce veces solo en la última fase.',
        ha='center', size=6.2, color=E.GRAYTX, family=E.SERIF)
c.y = c.p.caption(E.MX, c.y, 'El proyecto no se dibujó: se generó, se midió y se rehizo.',
                  'La trazabilidad completa de este proceso vive en el registro forense, '
                  'con más de doscientos cuarenta eventos fechados que incluyen los errores '
                  'y sus rectificaciones.', wrap=108)

# ============================================================ 5 · CICLO DE TRABAJO
c.seccion('D-05 · EL CICLO DE TRABAJO', 'Ni prompt ni proyecto: un bucle con medición')
ax = lienzo(6.9)
ETAPAS = ['ENTRADA\nintención y\nrestricciones', 'LECTURA\ncontexto real',
          'HIPÓTESIS\nconfiguración', 'GENERACIÓN\nmodelo completo',
          'MEDICIÓN\nauditoría\nindependiente', 'ERROR\nlo que la\nintuición no vio',
          'DIAGNÓSTICO\ncausa raíz', 'RECTIFICACIÓN\ndel generador',
          'AUDITORÍA\nse remide todo', 'CONOCIMIENTO\ncambia la\nsiguiente decisión']
n = len(ETAPAS)
cx, cy, r = 0.5, 0.52, 0.36
for i, et in enumerate(ETAPAS):
    a = math.pi / 2 - 2 * math.pi * i / n
    x = cx + r * math.cos(a) * 1.28
    y = cy + r * math.sin(a) * 0.92
    hum = i in (0, 9)
    caja(ax, x - 0.085, y - 0.052, 0.17, 0.104, et,
         fc='white' if hum else E.PANEL,
         ec=E.MAGENTA if hum else E.HAIR, size=6.2, bold=hum)
    a2 = math.pi / 2 - 2 * math.pi * (i + 0.5) / n
    x2 = cx + r * math.cos(a2) * 1.28
    y2 = cy + r * math.sin(a2) * 0.92
    ax.plot(x2, y2, marker=(3, 0, math.degrees(a2) - 90), ms=5, color=E.GRAYTX, zorder=2)
th = np.linspace(0, 2 * math.pi, 200)
ax.plot(cx + r * np.cos(th) * 1.28, cy + r * np.sin(th) * 0.92, '-', color=E.HAIR, lw=0.9,
        zorder=1)
ax.text(cx, cy + 0.045, 'EL BUCLE', ha='center', size=8.0, weight='bold', family=E.SERIF,
        color=E.MAGENTA)
ax.text(cx, cy - 0.02, 'blanco = decisión humana\ngris = ejecución automática',
        ha='center', va='top', size=5.6, family=E.SERIF, color=E.GRAYTX, linespacing=1.5)
c.y = c.p.caption(E.MX, c.y, 'La máquina mide y regenera; el criterio es humano.',
                  'La forma de las copas, la altura de la pasarela, dejar el centro vacío, '
                  'la apuesta botánica y la decisión de publicar los resultados incómodos '
                  'son decisiones de autor. Lo que el bucle aporta es que ninguna de ellas '
                  'se sostenga sobre una intuición no verificada.', wrap=108)

# ============================================================ 6 · ARBOL DE DECISION
c.seccion('D-06 · ÁRBOL DE DECISIÓN MUNICIPAL', 'Qué se decide en cada fase, y con qué dato')
ax = lienzo(6.5)
caja(ax, 0.34, 0.88, 0.32, 0.09, 'ESTE DOSSIER\n0 RED · viable con condiciones',
     fc=E.PANEL, ec=E.MAGENTA, bold=True, size=6.6)
FASES = [('FASE A · VALIDACIONES', 'informe Metro · servidumbres · CFD', 0.72,
          '¿hay impedimento legal o técnico?'),
         ('FASE B · PROTOTIPO', '1 mástil instrumentado a escala real', 0.55,
          '¿el viento y la transmitancia se comportan?'),
         ('FASE C · PILOTO', 'cuadrante C1 una temporada crítica', 0.38,
          '¿la gente lo usa? ≥60 % del uso BASE'),
         ('FASE E · DESPLIEGUE', 'plaza completa con D-001 y D-015 incorporados', 0.21,
          'con la sombra alta sobre ejes ya resuelta')]
for i, (tit, sub, yy, preg) in enumerate(FASES):
    caja(ax, 0.10, yy, 0.44, 0.10, tit + '\n' + sub, fc='white', size=6.0)
    ax.text(0.57, yy + 0.05, preg, va='center', size=5.9, family=E.SERIF, color=E.GRAYTX)
    if i == 0:
        flecha(ax, 0.50, 0.88, 0.36, yy + 0.10, color=E.MAGENTA)
    else:
        flecha(ax, 0.32, FASES[i - 1][2], 0.32, yy + 0.10, color=E.GREEN, lw=1.3)
        ax.text(0.335, (FASES[i - 1][2] + yy + 0.10) / 2, 'sí', size=5.6, color=E.GREEN,
                family=E.SERIF)
        flecha(ax, 0.10, FASES[i - 1][2] + 0.05, 0.03, FASES[i - 1][2] + 0.05,
               color='#c22a52', lw=1.0)
        ax.text(0.02, FASES[i - 1][2] + 0.075, 'no', size=5.6, color='#c22a52',
                family=E.SERIF)
caja(ax, 0.10, 0.05, 0.80, 0.09,
     'CADA «NO» ES UNA PARADA BARATA: el coste de detenerse en A o B es una fracción '
     'mínima del coste de equivocarse construyendo.', fc=E.PANEL, size=6.4)
c.y = c.p.caption(E.MX, c.y, 'La decisión no es sí o no: es en qué orden se despejan las dudas.',
                  'Las cuatro incertidumbres abiertas —viento, uso real, supervivencia '
                  'vegetal y coste— tienen cada una su fase de validación y su criterio de '
                  'paso. Ninguna de ellas es geométrica: el modelo cierra con cero '
                  'incidencias rojas.', wrap=108)

n = c.cerrar()
print('DIAGRAMAS_DE_SISTEMA ok:', n, 'pp')
