# -*- coding: utf-8 -*-
"""SISTEMA EDITORIAL DEL REFUGIO CLIMATICO — libreria compartida de maquetacion.

ADN grafico: traduccion del sistema IRAXXXDIOS (dossieres Stepanka/Tachov) al Refugio:
  - serif Georgia: display en negrita, cuerpo de texto libro;
  - versalitas espaciadas (tracking manual con thin-spaces) para kickers/cabeceras/pies;
  - acento MAGENTA IRAXXXDIOS + paleta propia del Refugio (verdes, rosa modulo, agua);
  - listas con raya magenta, fichas etiqueta-en-margen, tablas de cabecera rosa,
    paneles tintados, chips de certeza A/B/C (§5 del mandato);
  - retícula: A4 vertical, margenes 16/14 mm, 12 columnas virtuales.

Toda cifra publicada pasa por Doc.metric() -> se registra en _metrics/*.jsonl para
FINAL_METRICS_REGISTRY.csv. No existe la cifra huerfana.
"""
import json
import os
import textwrap

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.font_manager  # noqa: E402,F401
import numpy as np  # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))       # ANALISIS_FINALES_.../
RC = os.path.normpath(os.path.join(BASE, '..'))               # REFUGIO_CLIMATICO/
F9 = os.path.join(RC, 'FASE_03B9_HYPERDETAIL_V006')
METRICS_DIR = os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_metrics')
os.makedirs(METRICS_DIR, exist_ok=True)

# ============================================================ PALETA
INK = '#1c1c1c'
PAPER = '#ffffff'
PANEL = '#f6f3ee'          # panel tintado calido (como los cuadros de los dossieres)
HAIR = '#cfcac2'           # filete fino
GRAYTX = '#8a8a8a'         # texto secundario / fuentes
MAGENTA = '#e5007e'        # acento IRAXXXDIOS
ROSA = '#f2a0c0'           # modulos rosa del proyecto
GREEN = '#1f6f50'          # verde profundo refugio
LEAF = '#7fbf9e'           # verde hoja
PALEGREEN = '#e9f3ed'
AGUA = '#2e7f9e'           # azul-verde agua
PALEAGUA = '#e4f0f5'
AMBER = '#c98a00'          # nivel B (inferido)
# niveles de conocimiento (§5): A medido/calculado · B inferido · C hipotesis/escenario
NIVEL = {'A': dict(c=GREEN, tx='MEDIDO / CALCULADO'),
         'B': dict(c=AMBER, tx='INFERIDO'),
         'C': dict(c=GRAYTX, tx='HIPÓTESIS / ESCENARIO')}

SERIF = 'Georgia'
plt.rcParams.update({
    'font.family': SERIF, 'text.color': INK, 'axes.edgecolor': HAIR,
    'axes.labelcolor': INK, 'xtick.color': GRAYTX, 'ytick.color': GRAYTX,
    'pdf.fonttype': 42, 'svg.fonttype': 'none',
})

# A4 vertical en pulgadas
A4W, A4H = 8.27, 11.69
MX, MTOP, MBOT = 0.63, 0.55, 0.55        # margenes en fraccion de pulgada... (16mm/14mm)


def track(s, sp=' '):
    """Versalitas espaciadas: intercala thin-spaces (tracking manual)."""
    return sp.join(list(s.upper()))


def _x(fig, inch):
    return inch / A4W


def _y(fig, inch):
    return inch / A4H


class Page:
    """Una pagina A4 del sistema. Coordenadas en PULGADAS desde esquina inferior izq."""

    def __init__(self, doc, dark=False):
        self.doc = doc
        self.fig = plt.figure(figsize=(A4W, A4H))
        self.fig.patch.set_facecolor('#101311' if dark else PAPER)
        self.dark = dark
        self.ink = '#f2efe9' if dark else INK

    # ---------- primitivas de coordenadas
    def text(self, x, y, s, size=8.6, color=None, weight='normal', style='normal',
             ha='left', va='top', tracked=False, wrap=None, leading=1.38, family=SERIF):
        color = color or self.ink
        if tracked:
            s = track(s)
        if wrap:
            s = '\n'.join(textwrap.fill(p, wrap) for p in s.split('\n'))
        t = self.fig.text(_x(self.fig, x), _y(self.fig, y), s, size=size, color=color,
                          weight=weight, style=style, ha=ha, va=va, family=family,
                          linespacing=leading)
        return t

    def hline(self, x0, x1, y, color=HAIR, lw=0.7):
        self.fig.add_artist(plt.Line2D([_x(self.fig, x0), _x(self.fig, x1)],
                                       [_y(self.fig, y)] * 2, color=color, lw=lw,
                                       transform=self.fig.transFigure))

    def rect(self, x, y, w, h, fc=PANEL, ec='none', lw=0.7, zorder=1):
        self.fig.add_artist(Rectangle((_x(self.fig, x), _y(self.fig, y)),
                                      _x(self.fig, w), _y(self.fig, h), fc=fc, ec=ec,
                                      lw=lw, zorder=zorder, transform=self.fig.transFigure))

    # ---------- mobiliario de pagina
    def header(self, left, right):
        y = A4H - 0.42
        self.text(MX, y, left, size=6.4, color=GRAYTX, tracked=True, va='center')
        self.text(A4W - MX, y, right, size=6.4, color=GRAYTX, tracked=True,
                  ha='right', va='center')

    def footer(self, folio=None):
        y = 0.38
        self.text(MX, y, 'IRAXXXDIOS · REFUGIO CLIMÁTICO', size=6.4, color=GRAYTX,
                  tracked=True, va='center')
        if folio is not None:
            self.text(A4W - MX, y, str(folio), size=10.5, color=MAGENTA, weight='bold',
                      ha='right', va='center')

    def kicker(self, y, s, x=None):
        self.text(x if x is not None else MX, y, s, size=7.2, color=MAGENTA,
                  weight='bold', tracked=True)
        return y - 0.22

    def title(self, y, s, size=21, x=None, wrap=None):
        t = self.text(x if x is not None else MX, y, s, size=size, weight='bold',
                      wrap=wrap, leading=1.12)
        n = s.count('\n') + (0 if not wrap else max(0, len(s) // wrap))
        return y - (size / 72.0) * 1.35 * (1 + n)

    def subtitle(self, y, s, x=None, wrap=95, size=9.6):
        self.text(x if x is not None else MX, y, s, size=size, color='#4a4a4a',
                  wrap=wrap, leading=1.4)
        lines = len(textwrap.fill(s, wrap).split('\n'))
        return y - 0.19 * lines - 0.12

    def _w_in(self, t):
        """Anchura de un artista de texto en pulgadas (medida real por renderer).
        El renderer se cachea: canvas.draw() por medicion re-rasteriza las imagenes
        de la pagina (lento y con picos de memoria en paginas con renders)."""
        r = getattr(self, '_rend', None)
        if r is None:
            r = self.fig.canvas.get_renderer()
            self._rend = r
        bb = t.get_window_extent(renderer=r)
        return bb.width / self.fig.dpi

    def rich(self, x, y, lead_s, rest, wrap=52, size=8.6, color=None, lead_color=None):
        """Parrafo con lead-in inline en negrita, compuesto con medicion real:
        la primera linea arranca tras el lead; el resto vuelve al margen."""
        color = color or self.ink
        t1 = self.text(x, y, lead_s, size=size, weight='bold', color=lead_color or color)
        w1 = self._w_in(t1) + 0.055
        # UNA sola medicion (la del lead): el hueco restante de la primera linea se
        # convierte a caracteres con el ancho medio del cuerpo y textwrap hace el resto
        char_w = size / 72.0 * 0.472
        libres = max(4, int(wrap - w1 / char_w))
        env = textwrap.wrap(rest, libres, break_long_words=False, break_on_hyphens=False)
        first = env[0] if env else ''
        resto = ' '.join(rest.split()[len(first.split()):]) if first else rest
        if first:
            self.text(x + w1, y, first, size=size, color=color)
        lh = size / 72.0 * 1.38
        y -= lh
        if resto:
            s2 = textwrap.fill(resto, wrap, break_long_words=False, break_on_hyphens=False)
            self.text(x, y, s2, size=size, color=color)
            y -= lh * (s2.count('\n') + 1)
        return y - 0.10

    def body(self, x, y, s, wrap=52, size=8.6, w_bold_lead=False, color=None):
        """Bloque de texto; devuelve la y final. Marca **negritas** simples no soportada:
        usa lead-in con lead()."""
        s2 = '\n'.join(textwrap.fill(p, wrap) if p else '' for p in s.split('\n'))
        self.text(x, y, s2, size=size, wrap=None, color=color)
        lines = s2.count('\n') + 1
        return y - (size / 72.0) * 1.38 * lines - 0.10

    def lead(self, x, y, lead_s, rest, wrap=52, size=8.6):
        """Parrafo con lead-in en negrita (patron de los dossieres)."""
        return self.rich(x, y, lead_s, rest, wrap=wrap, size=size)

    def dashlist(self, x, y, items, wrap=48, size=8.6, gap=0.075, bold_leads=True):
        """Lista con raya magenta; item = (lead, resto) o str. Lead compuesto con medida."""
        for it in items:
            if isinstance(it, tuple):
                lead_s, rest = it
            else:
                lead_s, rest = '', it
            self.text(x, y, '—', size=size, color=MAGENTA, weight='bold')
            if lead_s and bold_leads:
                y = self.rich(x + 0.22, y, lead_s, rest, wrap=wrap, size=size) - gap + 0.10
            else:
                s2 = textwrap.fill(rest, wrap)
                self.text(x + 0.22, y, s2, size=size)
                y -= (size / 72.0) * 1.38 * (s2.count('\n') + 1) + gap
        return y

    def label(self, x, y, s, size=6.2):
        """Etiqueta versalita gris (patron ficha: QUE DICEN LAS BASES / RIESGO / FUENTE)."""
        self.text(x, y, s, size=size, color=GRAYTX, tracked=True, weight='bold')
        return y - 0.16

    def ficha(self, x, y, pares, wcol=2.9, wrap=None, size=8.4):
        """Ficha etiqueta->contenido apilada (columna). pares=[(label, texto)...]"""
        wrap = wrap or int(wcol * 6.6)
        for lab, cuerpo in pares:
            self.text(x, y, lab, size=6.0, color=GRAYTX, tracked=True, weight='bold')
            y -= 0.155
            s2 = textwrap.fill(cuerpo, wrap)
            self.text(x, y, s2, size=size)
            y -= (size / 72.0) * 1.38 * (s2.count('\n') + 1) + 0.11
        return y

    def chip(self, x, y, nivel='A', extra=None):
        """Chip de certeza §5. nivel A/B/C. Devuelve x tras el chip."""
        d = NIVEL[nivel]
        s = track(extra or d['tx'])
        w = 0.115 * len(s) * 0.42 + 0.32
        self.fig.add_artist(FancyBboxPatch(
            (_x(self.fig, x), _y(self.fig, y - 0.075)), _x(self.fig, w), _y(self.fig, 0.17),
            boxstyle='round,pad=0.002,rounding_size=0.006', fc='none', ec=d['c'], lw=0.9,
            transform=self.fig.transFigure))
        self.text(x + 0.07, y + 0.028, nivel + ' · ' + s,
                  size=5.8, color=d['c'], weight='bold', va='center')
        return x + w + 0.12

    def panel(self, x, y, w, h, titulo=None, fc=PANEL):
        self.rect(x, y - h, w, h, fc=fc)
        if titulo:
            self.text(x + 0.16, y - 0.18, titulo, size=6.6, tracked=True, weight='bold')
            return y - 0.42
        return y - 0.16

    def tabla(self, x, y, w, cols, rows, col_w=None, size=7.6, header_color=MAGENTA,
              row_gap=0.055, wrap_last=True):
        """Tabla de cabecera rosa + filetes. cols=[str], rows=[[...]]. Devuelve y final."""
        n = len(cols)
        col_w = col_w or [w / n] * n
        xs = [x + sum(col_w[:i]) for i in range(n)]
        hmaxh = 1
        for cx, cw, c in zip(xs, col_w, cols):
            wrh = max(6, int(cw * 141.0 / 6.0 / 1.9))     # versalitas: ~1,9x mas anchas
            s2 = textwrap.fill(c, wrh, break_long_words=False, break_on_hyphens=False)
            hmaxh = max(hmaxh, s2.count(chr(10)) + 1)
            self.text(cx, y, s2, size=6.0, color=header_color, tracked=True, weight='bold')
        y -= 0.10 + 0.088 * (hmaxh - 1)
        self.hline(x, x + w, y, color=header_color, lw=1.0)
        y -= 0.10
        for row in rows:
            hmax = 1
            for cx, cw, cell in zip(xs, col_w, row):
                s = str(cell)
                # caracteres que caben: ancho / (ancho medio de caracter Georgia)
                # ancho medio ~0.47*size/72 pulgadas; factor 0.92 de seguridad
                wr = max(8, int(cw * 141.0 / size))
                s2 = textwrap.fill(s, wr, break_long_words=False, break_on_hyphens=False)
                self.text(cx, y, s2, size=size)
                hmax = max(hmax, s2.count('\n') + 1)
            y -= (size / 72.0) * 1.32 * hmax + row_gap
            self.hline(x, x + w, y + row_gap * 0.6, color=HAIR, lw=0.4)
        return y - 0.05

    def bignum(self, x, y, valor, unidad, etiqueta, size=26, color=None, wlab=24):
        """Cifra grande de lectura rapida + etiqueta versalita (unidad medida)."""
        color = color or self.ink
        t = self.text(x, y, valor, size=size, weight='bold', color=color)
        if unidad:
            self.text(x + self._w_in(t) + 0.06, y - 0.052, unidad, size=9, color=GRAYTX)
        self.text(x, y - size / 72.0 * 1.25, textwrap.fill(etiqueta, wlab), size=6.2,
                  color=GRAYTX, tracked=False)
        return y - size / 72.0 * 1.25 - 0.35

    def caption(self, x, y, lead_s, rest, fuente=None, wrap=58, size=6.6):
        yy = self.rich(x, y, lead_s, rest, wrap=wrap, size=size, color='#4a4a4a') + 0.06
        if fuente:
            self.text(x, yy, fuente, size=5.6, color=GRAYTX)
            yy -= 0.12
        return yy - 0.06

    # ---------- ejes para mapas y graficos
    def axes(self, x, y, w, h, clean=True):
        """Ejes matplotlib en (x,y,w,h) pulgadas (y = esquina INFERIOR)."""
        ax = self.fig.add_axes([_x(self.fig, x), _y(self.fig, y),
                                _x(self.fig, w), _y(self.fig, h)])
        if clean:
            ax.set_xticks([])
            ax.set_yticks([])
            for s in ax.spines.values():
                s.set_visible(False)
        return ax

    def chart_axes(self, x, y, w, h):
        ax = self.fig.add_axes([_x(self.fig, x), _y(self.fig, y),
                                _x(self.fig, w), _y(self.fig, h)])
        ax.tick_params(labelsize=6, colors=GRAYTX, length=2)
        for sp in ('top', 'right'):
            ax.spines[sp].set_visible(False)
        for sp in ('left', 'bottom'):
            ax.spines[sp].set_color(HAIR)
        ax.grid(axis='y', color=HAIR, lw=0.35, alpha=0.7)
        ax.set_axisbelow(True)
        return ax

    def close(self):
        plt.close(self.fig)


class Doc:
    """Documento PDF del sistema + registro de metricas (§41: ninguna cifra huerfana)."""

    def __init__(self, path, titulo_corto, capitulo=''):
        self.path = path
        self.pdf = PdfPages(path)
        self.titulo = titulo_corto
        self.capitulo = capitulo
        self.folio = 0
        self.metrics = []
        self._mfile = os.path.join(
            METRICS_DIR, 'metrics_%s.jsonl' % os.path.splitext(os.path.basename(path))[0])
        open(self._mfile, 'w').close()

    def page(self, header_right=None, dark=False, folio=True):
        self.folio += 1
        p = Page(self, dark=dark)
        if self.folio > 1 or not dark:
            p.header(self.titulo, header_right if header_right is not None else self.capitulo)
            p.footer(self.folio if folio else None)
        return p

    def add(self, p):
        self.pdf.savefig(p.fig)
        p.close()

    def metric(self, mid, valor, unidad, estado, metodo, fuente, notas=''):
        """Registra una metrica publicada y devuelve el valor formateado."""
        rec = dict(id=mid, valor=valor, unidad=unidad, estado=estado, metodo=metodo,
                   fuente=fuente, notas=notas, pdf=os.path.basename(self.path),
                   pagina=self.folio)
        self.metrics.append(rec)
        with open(self._mfile, 'a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        return valor

    def close(self):
        self.pdf.close()


# ============================================================ DATOS BASE (v006)
AUD_DATA = os.path.join(F9, '_reaudit9', '_data')
CLI_DATA = os.path.join(F9, '_reclima9', '_data')
GRID_EXT = (-112, 100, -45, 78)     # x0,x1,y0,y1 del ambito (auditoria y clima comparten)


def load_geo():
    with open(os.path.join(F9, 'geometria_maestra_v006.json'), encoding='utf-8') as f:
        return json.load(f)


def np_aud(name):
    return np.load(os.path.join(AUD_DATA, name))


def np_cli(name):
    return np.load(os.path.join(CLI_DATA, name))


def js_aud(name):
    with open(os.path.join(AUD_DATA, name), encoding='utf-8') as f:
        return json.load(f)


def js_cli(name):
    with open(os.path.join(CLI_DATA, name), encoding='utf-8') as f:
        return json.load(f)


def draw_context(ax, geo=None, lw=0.5, color='#b9b3aa', fill='#efece6', estacion=True,
                 zorder=1):
    """Huella de contexto OSM (edificios) como base de todo mapa."""
    geo = geo or load_geo()
    for b in geo['contexto']['buildings']:
        pts = b['pts']
        if len(pts) < 4:
            continue
        xs = [p[0] for p in pts] + [pts[0][0]]
        ys = [p[1] for p in pts] + [pts[0][1]]
        ax.fill(xs, ys, fc=fill, ec=color, lw=lw, zorder=zorder)
    ax.set_xlim(GRID_EXT[0], GRID_EXT[1])
    ax.set_ylim(GRID_EXT[2], GRID_EXT[3])
    ax.set_aspect('equal')


def show_raster(ax, arr, cmap, vmin=None, vmax=None, mask=None, alpha=1.0, zorder=2):
    a = np.array(arr, dtype=float)
    if mask is not None:
        a = np.where(mask, a, np.nan)
    im = ax.imshow(a, origin='lower', extent=GRID_EXT, cmap=cmap, vmin=vmin, vmax=vmax,
                   alpha=alpha, zorder=zorder, interpolation='nearest')
    return im


def cbar(page, ax_im, x, y, w, label, ticks=None):
    cax = page.fig.add_axes([_x(page.fig, x), _y(page.fig, y), _x(page.fig, w),
                             _y(page.fig, 0.07)])
    cb = page.fig.colorbar(ax_im, cax=cax, orientation='horizontal')
    cb.ax.tick_params(labelsize=5.4, colors=GRAYTX, length=2)
    cb.outline.set_edgecolor(HAIR)
    if ticks is not None:
        cb.set_ticks(ticks)
    page.text(x, y + 0.16, label, size=5.8, color=GRAYTX, tracked=True)
    return cb


# mapas de color de la casa
import matplotlib.colors as mcolors  # noqa: E402
CMAP_VERDE = mcolors.LinearSegmentedColormap.from_list('rfg_verde', ['#f3f8f4', LEAF, GREEN])
CMAP_AGUA = mcolors.LinearSegmentedColormap.from_list('rfg_agua', [PALEAGUA, AGUA, '#124a5e'])
CMAP_CALOR = mcolors.LinearSegmentedColormap.from_list('rfg_calor', ['#fdf6ee', '#f2b263', '#d94f2a', '#7c1128'])
CMAP_DELTA = mcolors.LinearSegmentedColormap.from_list('rfg_delta', [GREEN, '#f3f5f2', '#c22a52'])
CMAP_ROSA = mcolors.LinearSegmentedColormap.from_list('rfg_rosa', ['#fdf2f7', ROSA, MAGENTA])


def load_img_small(path, maxw=1000):
    """Carga una imagen submuestreada (los PDF no deben pesar 90 MB)."""
    from PIL import Image as _PILImage
    im = _PILImage.open(path).convert('RGB')
    if im.width > maxw:
        im.thumbnail((maxw, int(maxw * im.height / im.width) + 1))
    return np.asarray(im)


def portada(doc, titulo, subtitulo, kicker_s, datos, img=None, num=''):
    """Portada oscura full-bleed del sistema."""
    p = doc.page(dark=True, folio=False)
    if img is not None and os.path.exists(img):
        ax = p.axes(0, 0, A4W, A4H)
        arr = load_img_small(img, 1200)
        ax.imshow(arr, aspect='auto', alpha=0.42)
        ax.set_xticks([]); ax.set_yticks([])
    p.text(MX, A4H - 0.55, 'IRAXXXDIOS  /  REFUGIO CLIMÁTICO', size=6.8, color=ROSA,
           tracked=True, weight='bold')
    if num:
        p.text(A4W - MX, A4H - 0.55, num, size=6.8, color='#8f8b84', tracked=True, ha='right')
    p.text(MX, A4H * 0.52, kicker_s, size=7.4, color=MAGENTA, tracked=True, weight='bold')
    p.text(MX, A4H * 0.52 - 0.28, titulo, size=30, weight='bold', color='#f2efe9',
           leading=1.08)
    p.text(MX, A4H * 0.52 - 0.30 - 0.52 * (titulo.count('\n') + 1), subtitulo, size=9.4,
           color='#c9c4bb', wrap=76, leading=1.45)
    # banda de datos inferior (el valor se encoge si no cabe en su columna)
    xw = (A4W - 2 * MX) / max(1, len(datos))
    for i, (lab, val) in enumerate(datos):
        x = MX + i * xw
        p.text(x, 1.15, lab, size=5.8, color='#8f8b84', tracked=True)
        sz = 9.5
        t = p.text(x, 0.97, val, size=sz, color='#f2efe9', weight='bold')
        while p._w_in(t) > xw - 0.18 and sz > 6.0:
            t.remove()
            sz -= 0.5
            t = p.text(x, 0.97, val, size=sz, color='#f2efe9', weight='bold')
    p.hline(MX, A4W - MX, 1.32, color='#3a3f3b', lw=0.7)
    doc.add(p)
