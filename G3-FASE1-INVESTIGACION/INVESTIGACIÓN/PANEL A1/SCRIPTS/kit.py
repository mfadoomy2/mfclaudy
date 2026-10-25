"""Kit gráfico del panel A1 · Ribera 31 (coordenadas en mm, origen arriba-izquierda)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, Circle, Polygon as MPoly, FancyBboxPatch, Wedge, PathPatch, Ellipse
from matplotlib.path import Path
import numpy as np

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["svg.fonttype"] = "none"
FD = "/home/claude/fonts/"
FONTS = {k: fm.FontProperties(fname=FD + v) for k, v in dict(
    title="ArchCond900.ttf", cond="ArchCond700.ttf", condm="ArchCond500.ttf", r="Arch400.ttf",
    b="Arch700.ttf", i="Arch400i.ttf", mono="Mono400.ttf", monob="Mono700.ttf", blk="ArchBlack.ttf",
    exp="ArchExp900.ttf").items()}

# paleta
PAPER = "#FFFFFF"; INK = "#0A0A0A"; RED = "#FF1E00"; BLUE = "#1030FF"; PINK = "#FF1FA9"
VIOLET = "#7A1BFF"; GREEN = "#00C853"; YELLOW = "#FFE500"; ORANGE = "#FF6A00"; CYAN = "#00B7FF"; LIME = "#A8FF00"
GREY = "#BDBDBD"; LGREY = "#E8E8E8"; DGREY = "#5A5A5A"; WHITE = "#FFFFFF"
LEVEL = {"A": GREEN, "B": BLUE, "C": PINK}

PW, PH = 594.0, 841.0
MM = 72 / 25.4  # pt por mm


class Poster:
    def __init__(self):
        self.fig = plt.figure(figsize=(PW / 25.4, PH / 25.4), facecolor=PAPER)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, PW); self.ax.set_ylim(PH, 0); self.ax.axis("off")
        self.ax.set_facecolor(PAPER)
        self.z = 10

    # ---------- primitivas
    def t(self, x, y, s, f="r", size=8, c=INK, ha="left", va="baseline", rot=0, z=None, ls=1.15, alpha=1, **kw):
        return self.ax.text(x, y, s, fontproperties=FONTS[f], fontsize=size, color=c, ha=ha, va=va,
                            rotation=rot, zorder=z or 50, linespacing=ls, alpha=alpha, **kw)

    def rect(self, x, y, w, h, fc="none", ec="none", lw=0.5, z=5, alpha=1, hatch=None, **kw):
        p = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, lw=lw, zorder=z, alpha=alpha, hatch=hatch, **kw)
        self.ax.add_patch(p); return p

    def line(self, xs, ys, c=INK, lw=0.5, z=20, ls="-", alpha=1, **kw):
        return self.ax.plot(xs, ys, color=c, lw=lw, zorder=z, ls=ls, alpha=alpha, solid_capstyle="butt", **kw)[0]

    def circ(self, x, y, r, fc="none", ec=INK, lw=0.5, z=20, alpha=1, **kw):
        p = Circle((x, y), r, facecolor=fc, edgecolor=ec, lw=lw, zorder=z, alpha=alpha, **kw)
        self.ax.add_patch(p); return p

    def poly(self, pts, fc="none", ec="none", lw=0.5, z=10, alpha=1, **kw):
        p = MPoly(pts, closed=True, facecolor=fc, edgecolor=ec, lw=lw, zorder=z, alpha=alpha, **kw)
        self.ax.add_patch(p); return p

    def img(self, im, x, y, w, h, z=3, alpha=1, interp="antialiased"):
        return self.ax.imshow(im, extent=(x, x + w, y + h, y), zorder=z, alpha=alpha, aspect="auto", interpolation=interp)

    def curve(self, p0, p1, c=INK, lw=0.6, z=15, alpha=1, bend=0.5, horiz=True):
        (x0, y0), (x1, y1) = p0, p1
        if horiz:
            dx = (x1 - x0) * bend
            verts = [(x0, y0), (x0 + dx, y0), (x1 - dx, y1), (x1, y1)]
        else:
            dy = (y1 - y0) * bend
            verts = [(x0, y0), (x0, y0 + dy), (x1, y1 - dy), (x1, y1)]
        pp = PathPatch(Path(verts, [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]), fc="none", ec=c, lw=lw,
                       zorder=z, alpha=alpha, capstyle="butt")
        self.ax.add_patch(pp); return pp

    def tag(self, x, y, lvl, size=5.2, anchor="left"):
        """Etiqueta de certeza A/B/C (y = línea base)."""
        lab = {"A": "A · MEDIDO", "B": "B · INFERIDO", "C": "C · HIPÓTESIS", "A/B": "A/B · MEDIDO + INFERIDO",
               "B/C": "B/C · INFERIDO + HIPÓTESIS"}[lvl]
        col = LEVEL[lvl[0]] if "/" not in lvl else LEVEL[lvl[-1]]
        w = len(lab) * size * 0.62 / MM + 3
        x0 = x if anchor == "left" else x - w
        p = FancyBboxPatch((x0, y - size / MM * 0.95), w, size / MM * 1.35, boxstyle="round,pad=0,rounding_size=1.1",
                           fc="none", ec=col, lw=0.6, zorder=40)
        self.ax.add_patch(p)
        self.t(x0 + w / 2, y - size / MM * 0.28, lab, "monob", size, col, ha="center", va="center")
        return w

    def header(self, x, y, w, num, title, color, lvl=None, sub=None):
        """Cabecera de bloque: número en caja de color + título condensado + filete."""
        self.rect(x, y, 13, 9, fc=color, z=30)
        self.t(x + 6.5, y + 7.3, num, "title", 21, INK if color in (YELLOW, CYAN, PINK, ORANGE, GREEN) else WHITE, ha="center", z=31)
        self.t(x + 16, y + 7.6, title, "title", 24, INK, z=31)
        self.line([x, x + w], [y + 10.2, y + 10.2], INK, 1.2, z=31)
        if sub:
            self.t(x + w, y + 7.4, sub, "condm", 9.5, DGREY, ha="right", z=31)
        if lvl:
            self.tag(x + w, y + 3.2, lvl, anchor="right")

    def para(self, x, y, s, size=7.2, f="r", c=INK, width_chars=60, ls=1.28, **kw):
        import textwrap
        out = []
        for block in s.split("\n"):
            out += textwrap.wrap(block, width_chars) or [""]
        return self.t(x, y, "\n".join(out), f, size, c, va="top", ls=ls, **kw)

    def save(self, pdf, png=None, dpi=60):
        self.fig.savefig(pdf, facecolor=PAPER)
        if png:
            self.fig.savefig(png, dpi=dpi, facecolor=PAPER)

from matplotlib.textpath import TextPath
def textw(s, f="r", size=8):
    """ancho del texto en mm"""
    tp = TextPath((0, 0), s, size=size, prop=FONTS[f])
    return tp.get_extents().width / MM
