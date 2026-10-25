"""PANEL A1 · RIBERA 31 · v2 — fondo blanco, tintas vivas, capas en multiplicación, calle en pendiente."""
import sys, json, math, pickle, os
sys.path.insert(0, "/home/claude/g3/a1"); sys.path.insert(0, "/home/claude/g3")
import numpy as np
from PIL import Image, ImageOps
from kit import *
from matplotlib.patches import Rectangle, FancyBboxPatch, Ellipse, Wedge, Circle, RegularPolygon
from matplotlib.transforms import Affine2D
import plates as PL
os.chdir("/home/claude/g3")
from base import CL, PARCELA, META, T as TR
from shapely.geometry import Point
from shapely import wkt as WKT

D = "/home/claude/g3/datos/"
MET = json.load(open("/home/claude/g3/a1/metrics.json"))
MN = json.load(open(D + "metricas_nuevas.json"))
FAC = json.load(open(D + "fachadas_index.json"))
FR = json.load(open(D + "frentes_ribera.json"))
PAT = json.load(open(D + "patrones.json"))
SOL = json.load(open(D + "sol_por_altura.json"))
SOMB = np.load(D + "sombras.npz")
exec(open(D + "codificacion_fachadas.py").read()); COD = C
CX, CY = PL.C
S31a, S31b = CL.project(Point(439996, 4473236.8)), CL.project(Point(439997.3, 4473221.9))
FI = {f["rc"]: f for f in FAC}
JUMPS = []
for _sd in "EW":
    _L = sorted([f for f in FR if f["side"] == _sd and f["s1"] - f["s0"] > 0.5], key=lambda f: f["s0"])
    for _a, _b in zip(_L, _L[1:]):
        if _b["s0"] - _a["s1"] < 3 and _a["rc"] in FI and _b["rc"] in FI:
            _h1, _h2 = FI[_a["rc"]]["plantas_frente"], FI[_b["rc"]]["plantas_frente"]
            JUMPS.append((_sd, _a["s1"], abs(_h1 - _h2), _h1, _h2))
assert len(JUMPS) == MN["saltos_total"] and sum(j[2] >= 2 for j in JUMPS) == MN["saltos_ge2"]
AL = [(a[0], a[1] - 2.5) for a in MN["alt_perfil"]]   # cota de suelo = altitud de cámara SV − 2,5 m (B)
def zs(s): return float(np.interp(s, [a[0] for a in AL], [a[1] for a in AL]))

def cod(c): return c.replace("W", "O")
def fnum(v, d=0): return f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
DARK = (RED, BLUE, VIOLET, INK, DGREY, GREEN, PINK, ORANGE)

P = Poster()
M = 14.0; CWID = PW - 2 * M

# ---------------------------------------------------------------- utilidades "locas pero exactas"
def rot_rect(x, y, w, h, ang, fc, z=30, ec="none", lw=0, alpha=1):
    r = Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha)
    r.set_transform(Affine2D().rotate_deg_around(x, y + h / 2, -ang) + P.ax.transData)
    P.ax.add_patch(r); return r

def header(x, y, num, title, color, ang, lvl=None, sub=None, w=CWID):
    tw = textw(title, "title", 25)
    rot_rect(x - 1, y - 1, tw + 25, 11.5, ang, color, z=30)
    tc = INK if color in (YELLOW, CYAN, LIME, ORANGE, GREEN, PINK) else WHITE
    P.t(x + 2, y + 8.6, num, "title", 25, tc, rot=ang, rotation_mode="anchor", z=32)
    P.t(x + 17, y + 8.6, title, "title", 25, tc, rot=ang, rotation_mode="anchor", z=32)
    P.line([x, x + w], [y + 13.2, y + 13.2], INK, 1.4, z=29)
    if sub: P.t(x + w, y + 11.4, sub, "condm", 9.2, INK, ha="right", z=31)
    if lvl: P.tag(x + w, y + 5.5, lvl, anchor="right")

def sticker(cx, cy, r, shape, color, big, unit, lab, lvl, ang):
    tc = WHITE if color in DARK else INK
    if shape == "circle":
        P.ax.add_patch(Circle((cx, cy), r, fc=color, ec=INK, lw=1.0, zorder=60))
    elif shape == "star":
        n = 14; pts = []
        for i in range(2 * n):
            rr = r if i % 2 == 0 else r * 0.80
            a = math.pi * i / n + math.radians(ang)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        P.poly(pts, fc=color, ec=INK, lw=1.0, z=60)
    elif shape == "square":
        r_ = Rectangle((cx - r, cy - r * 0.72), 2 * r, 1.44 * r, fc=color, ec=INK, lw=1.0, zorder=60)
        r_.set_transform(Affine2D().rotate_deg_around(cx, cy, -ang) + P.ax.transData); P.ax.add_patch(r_)
    elif shape == "pill":
        r_ = FancyBboxPatch((cx - r * 1.25, cy - r * 0.62), 2.5 * r, 1.24 * r, boxstyle=f"round,pad=0,rounding_size={r*0.62}",
                            fc=color, ec=INK, lw=1.0, zorder=60)
        r_.set_transform(Affine2D().rotate_deg_around(cx, cy, -ang) + P.ax.transData); P.ax.add_patch(r_)
    import textwrap
    size = r * 2.05
    bw = textw(big, "title", size); uw = textw(unit, "cond", r * 0.95) if unit else 0
    tr = Affine2D().rotate_deg_around(cx, cy, -ang)
    def put(x, y, txt, f, sz, ha="left", va="baseline"):
        (xx, yy) = tr.transform((x, y))
        P.t(xx, yy, txt, f, sz, tc, ha=ha, va=va, rot=ang, rotation_mode="anchor", z=61)
    x0 = cx - (bw + uw + 0.8) / 2
    put(x0, cy + 1.2, big, "title", size)
    if unit: put(x0 + bw + 0.8, cy + 1.2, unit, "cond", r * 0.95)
    lab2 = "\n".join(textwrap.wrap(lab, 15))
    put(cx, cy + 2.8, lab2, "b", 6.8, ha="center", va="top")
    put(cx, cy - r * 0.52, lvl, "monob", 6.5, ha="center")

# ==================================================================== CABECERA
def cabecera():
    y0 = 10
    P.t(M, y0 + 2, "ATLAS DE INVESTIGACIÓN · G3 · VIVIENDA TEMPORAL PARA JÓVENES · EL RASTRO, MADRID · 24-09-2026", "monob", 9, INK, va="top")
    P.t(M - 2.5, y0 + 66, "RIBERA", "title", 240, INK, z=40)
    x31 = M - 2.5 + textw("RIBERA", "title", 240) + 4
    P.t(x31, y0 + 70, "31", "title", 262, RED, rot=-5, rotation_mode="anchor", z=41)
    # subtítulo en franja amarilla inclinada
    sub = "una calle que baja 37 m · un solar que no está vacío · un sol de invierno que solo llega arriba"
    rot_rect(M - 1, y0 + 69.5, textw(sub, "cond", 13) + 6, 7.4, 1.2, YELLOW, z=42)
    P.t(M + 2, y0 + 75.2, sub, "cond", 13, INK, rot=1.2, rotation_mode="anchor", z=43)
    # ficha
    x = 352; w = PW - M - x
    P.rect(x, y0 + 6, w, 66, fc=BLUE, z=20)
    P.t(x + 5, y0 + 13, "FICHA", "monob", 8, YELLOW, z=21)
    ficha = [("Parcela", "Ribera de Curtidores 31 · 28005 Madrid"), ("Situación", "El Rastro · Embajadores · Centro"),
             ("Encargo", "Vivienda temporal para jóvenes"), ("Curso", "G3 · Proyectos · UEM · 2026-27"),
             ("Autor", "Adam Ihab"), ("SRC", "ETRS89 · UTM 30N (EPSG:25830)")]
    for i, (a, b) in enumerate(ficha):
        P.t(x + 5, y0 + 19 + i * 4.4, a.upper(), "mono", 6.3, CYAN, z=21)
        P.t(x + 28, y0 + 19 + i * 4.4, b, "r", 7.8, WHITE, z=21)
    P.t(x + 5, y0 + 49, "ÍNDICE", "monob", 8, YELLOW, z=21)
    idx = [("01", "MAPEADOS · 7 capas", CYAN), ("02", "RADIO · 500 m", PINK), ("03", "LA CALLE QUE BAJA", YELLOW),
           ("04", "PATRONES · P01–P11", GREEN), ("05", "SOL · TIEMPO · CRITERIOS", ORANGE)]
    for i, (n, s, c) in enumerate(idx):
        yy = y0 + 51.5 + i * 3.9
        P.rect(x + 5, yy, 6.5, 3.3, fc=c, z=25); P.t(x + 8.25, yy + 2.65, n, "monob", 6.2, INK, ha="center", z=26)
        P.t(x + 13.5, yy + 2.7, s, "cond", 8.2, WHITE, z=26)
    xc = x + 88
    P.t(xc, y0 + 49, "CERTEZA", "monob", 8, YELLOW, z=21)
    for i, (l, s) in enumerate([("A", "medido: catastro, OSM, SV, MER"), ("B", "inferido: lectura visual, modelo"), ("C", "hipótesis de proyecto")]):
        yy = y0 + 51.5 + i * 5.2
        P.rect(xc, yy, 5.5, 4.2, fc=LEVEL[l], ec=WHITE, lw=0.5, z=25); P.t(xc + 2.75, yy + 3.3, l, "monob", 7.5, INK if l != "B" else WHITE, ha="center", z=26)
        P.t(xc + 7.5, yy + 3.2, s, "r", 7, WHITE, z=26)

def pegatinas():
    y = 103
    S = [(30, y - 1, 14.5, "circle", YELLOW, "650,9", "m²", "superficie de parcela", "A", -8),
         (80, y + 2, 12.5, "square", PINK, "49,48", "m", "de fondo: una corrala", "A", 4),
         (126, y - 1, 13, "circle", LIME, "14,93", "m", "de frente a Ribera", "A", 10),
         (174, y + 2, 12.5, "pill", CYAN, "6,8", "%", "de pendiente frente al 31", "A", -5),
         (224, y - 2, 15, "star", INK, "0,17", "h", "de sol en el suelo el 21-dic", "B", 7),
         (270, y + 2, 12.5, "circle", ORANGE, "25,8", "m", "de ancho de calle", "A", -9),
         (318, y - 1, 13.5, "square", BLUE, "3.204", "", "viviendas catastrales en 200 m", "A", -3),
         (368, y + 1, 13.5, "circle", RED, "339", "m", "a la boca de metro más próxima", "A", 6),
         (416, y - 2, 14, "star", GREEN, "30/39", "", "huecos con balcón propio", "B", -6),
         (462, y + 2, 13, "circle", VIOLET, "418", "", "comercios OSM en 500 m", "A", 9),
         (521, y - 1, 13, "pill", YELLOW, "−37", "m", "de Cascorro a la Ronda", "B", -4)]
    for s in S: sticker(*s)

# ==================================================================== 01 MAPEADOS
MAPH = 214.0; S_MAP = MAPH / 1180.0
MX0, MY0 = M, 136
XMIN = PL.X0 + PL.OFFX / PL.PXM
YMAX = CY + 590
def W2P(x, y): return MX0 + (x - XMIN) * S_MAP, MY0 + (YMAX - y) * S_MAP

def bloque01():
    header(M, 118.5, "01", "MAPEADOS · SIETE CAPAS SOBRE UN PUNTO", CYAN, -1.4, "A",
           "MAPPEADOS/ · QGIS 3.40 GeoPDF · inventario OSM 600 m · MER 2021 · georreferencia exacta por GPTS")
    im = Image.open("/home/claude/g3/a1/hi/MAPA_COMPLETO.png").convert("RGB")
    pxm = PL.PXM; top = (PL.Y0 - YMAX) * pxm; hpx = 1180 * pxm
    im = im.crop((0, int(round(top)), im.size[0], int(round(top + hpx))))
    wmm = im.size[0] / pxm * S_MAP
    # bloque de sombra desplazado (brutal)
    P.rect(MX0 + 3.5, MY0 + 3.5, wmm, MAPH, fc=PINK, z=2)
    P.img(np.asarray(im), MX0, MY0, wmm, MAPH, z=3)
    P.rect(MX0, MY0, wmm, MAPH, ec=INK, lw=1.2, z=30)
    cx, cy = W2P(CX, CY)
    for r, lab in [(100, "100 m · 1'15\""), (200, "200 m · 2'30\""), (300, "300 m · 3'45\""), (400, "400 m · 5'"), (500, "500 m · 6'15\"")]:
        rr = r * S_MAP
        P.circ(cx, cy, rr, ec=RED, lw=1.3 if r == 400 else 0.7, ls=(0, (4, 2)) if r != 400 else "-", z=12)
        a = math.radians(-38)
        P.t(cx + rr * math.cos(a), cy + rr * math.sin(a), lab, "monob", 6.0, WHITE, ha="center", va="center", z=40,
            rot=38 - 90 + 90 - 38 + 0, bbox=dict(fc=RED, ec="none", pad=0.5))
    for s in range(16):
        a = math.radians(s * 22.5 + 11.25)
        P.line([cx + 100 * S_MAP * math.sin(a), cx + 500 * S_MAP * math.sin(a)],
               [cy - 100 * S_MAP * math.cos(a), cy - 500 * S_MAP * math.cos(a)], RED, 0.3, z=11, alpha=0.7)
    xs, ys = zip(*[W2P(x, y) for x, y in CL.coords])
    P.line(xs, ys, YELLOW, 6.5, z=13)
    P.line(xs, ys, INK, 0.6, z=14, ls=(0, (2, 1.5)))
    for i, e in enumerate(META["estaciones"]):
        x, y = TR.transform(e["lon"], e["lat"]); px_, py_ = W2P(x, y)
        P.circ(px_, py_, 1.3, fc=WHITE, ec=INK, lw=0.5, z=22)
        if i % 2 == 0 and i not in (12,):
            P.t(px_ - 2.4, py_ + 0.9, f"S{i+1:02d}", "monob", 5.0, INK, ha="right", z=23, bbox=dict(fc=WHITE, ec="none", pad=0.15))
    P.poly([W2P(x, y) for x, y in PARCELA.exterior.coords], fc=RED, ec=INK, lw=0.7, z=25)
    P.t(cx + 9, cy + 3, "31", "title", 30, WHITE, z=40, rot=-6, rotation_mode="anchor", bbox=dict(fc=RED, ec=INK, lw=1, pad=0.6))
    D0 = pickle.load(open("/home/claude/g3/a1/osm.pkl", "rb"))
    seen = {}
    for f in D0["feats"]:
        if f["sub"] == "railway=subway_entrance":
            g = WKT.loads(f["wkt"]); x, y = g.x, g.y
            if abs(y - CY) > 585: continue
            px_, py_ = W2P(x, y)
            if px_ > MX0 + wmm - 2: continue
            P.rect(px_ - 1.7, py_ - 1.7, 3.4, 3.4, fc=BLUE, ec=WHITE, lw=0.5, z=26)
            P.t(px_, py_ + 1.1, "M", "monob", 4.8, WHITE, ha="center", z=27)
            nm = f["nom"] or ""; d = math.hypot(x - CX, y - CY)
            if nm and (nm not in seen or d < seen[nm][0]): seen[nm] = (d, px_, py_)
    for nm, (d, px_, py_) in seen.items():
        P.t(px_ + 2.6, py_ - 2.4, f"{nm.upper()} · {fnum(d)} m", "monob", 5.6, WHITE, z=41, bbox=dict(fc=BLUE, ec="none", pad=0.35))
    nx, ny = MX0 + wmm - 12, MY0 + 16
    P.poly([(nx, ny - 9), (nx - 3.4, ny + 2), (nx, ny), (nx + 3.4, ny + 2)], fc=INK, z=40)
    P.t(nx, ny + 7.5, "N", "title", 17, INK, ha="center", z=40)
    sx, sy = MX0 + 8, MY0 + MAPH - 8
    P.rect(sx - 2, sy - 5.5, 200 * S_MAP + 30, 10, fc=WHITE, z=39)
    for i in range(4):
        P.rect(sx + i * 50 * S_MAP, sy, 50 * S_MAP, 1.8, fc=INK if i % 2 == 0 else WHITE, ec=INK, lw=0.4, z=40)
    for v in [0, 50, 100, 150, 200]:
        P.t(sx + v * S_MAP, sy - 1.3, f"{v}", "monob", 5.5, INK, ha="center", z=40)
    P.t(sx + 200 * S_MAP + 2, sy + 1.8, f"m · 1:{fnum(1000 / S_MAP)}", "monob", 5.5, INK, z=40)
    lx, ly = MX0 + 4, MY0 + 4
    P.rect(lx, ly, 72, 38, fc=WHITE, ec=INK, lw=0.8, z=35)
    P.t(lx + 3, ly + 6.2, "MAPA COMPLETO + LECTURA", "title", 11.5, INK, z=36)
    leg = [(RED, "anillos 100 m · minutos a 80 m/min en línea recta"), (YELLOW, "eje de Ribera de Curtidores · 658 m"),
           (WHITE, "S01–S23 · estaciones Street View (40 / 20 m)"), (BLUE, "M · bocas de metro (OSM)"), (RED, "parcela nº 31 (catastro)")]
    for i, (c, s) in enumerate(leg):
        yy = ly + 11.5 + i * 5.3
        P.rect(lx + 3, yy - 2.6, 5, 3.2, fc=c, ec=INK, lw=0.4, z=36); P.t(lx + 10, yy, s, "r", 6.4, INK, z=36)
    return wmm

def bloque01b(wmm):
    """Axonometría explotada: láminas en MULTIPLICACIÓN, desplazadas en zigzag."""
    R = MET["rings"]; L = MET["longitudes_500"]; sum5 = lambda k: sum(R[k])
    sub = lambda k: dict(MET["subtipos"][k])
    cols = [CYAN, INK, BLUE, PINK, VIOLET, GREEN, ORANGE]
    alph = [0.55, 0.62, 1, 1, 1, 1, 0.85]
    info = [
        ("01", "EDIFICIOS", f"{fnum(sum5('edificios'))} polígonos en 500 m · ocupan el {fnum(MET['bld_area_500']/(math.pi*500**2)*100,1)} % del círculo"),
        ("02", "CALLES Y RECORRIDOS", f"{fnum(L['highway=footway']/1000,1)} km de aceras y sendas · {fnum(L['highway=living_street']/1000,1)} km de convivencia · {fnum(L['highway=steps'])} m de escaleras"),
        ("03", "TRANSPORTE", f"{sub('transporte')['railway=subway_entrance']} bocas de metro, {sub('transporte')['highway=bus_stop']} paradas de bus en 500 m · ninguna en 100 m"),
        ("04", "COMERCIO Y ACTIVIDAD", f"{sum5('comercio')} en 500 m · {sub('comercio')['shop=vacant']} locales vacíos · {sub('comercio')['shop=antiques']} anticuarios"),
        ("05", "EQUIPAMIENTOS Y LOCALES", f"{sum5('equipamientos')} en 500 m · {sub('equipamientos')['amenity=restaurant']} restaurantes · {sub('equipamientos')['amenity=bar']} bares · colegio a 110 m"),
        ("06", "ESPACIO PÚBLICO Y VERDE", f"{sum5('arboles')} árboles · {fnum(MET['verde_m2_500']/10000,2)} ha de parque, jardín y plaza ({fnum(MET['verde_m2_500']/(math.pi*500**2)*100,1)} %)"),
        ("07", "RUIDO", "lo que MAPA COMPLETO añade a MAPA 6: isófonas del Mapa Estratégico de Ruido de Madrid 2021 (MER 2021)"),
    ]
    x0, x1 = MX0 + wmm + 2, PW - M
    ytop, ybot = MY0 - 1, MY0 + MAPH + 1
    pw = 248.0; iw, ih = Image.open("/home/claude/g3/a1/hi/iso_0.png").size; ph = pw * ih / iw
    n = 7; d = (ybot - ytop - ph) / (n - 1)
    dxs = [-14, 14, -10, 16, -16, 10, -4]
    cxb = x0 + 154
    # lienzo de multiplicación
    RES = 9.0  # px/mm
    X0c, Y0c = x0, ytop
    Wc, Hc = int((x1 - x0) * RES), int((ybot - ytop) * RES)
    canvas = np.ones((Hc, Wc, 3), np.float32)
    def hexf(h): return np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)], np.float32)
    from PIL import Image as I2, ImageDraw
    centers = []
    for k in range(n):
        yk = ybot - ph - k * d; xk = cxb - pw / 2 + dxs[k]
        centers.append((xk + pw / 2, yk + ph / 2, xk, yk))
        a = np.asarray(I2.open(f"/home/claude/g3/a1/hi/iso_{k}.png").resize((int(pw * RES), int(ph * RES)), I2.LANCZOS))[..., 3] / 255.0
        # lámina: tinte del plano (elipse) + dibujo
        ell = I2.new("L", (int(pw * RES), int(ph * RES)), 0)
        ImageDraw.Draw(ell).ellipse((1, 1, int(pw * RES) - 2, int(ph * RES) - 2), fill=255)
        e = np.asarray(ell) / 255.0
        col = hexf(cols[k])
        A = np.clip(a * alph[k] + e * 0.10, 0, 1)[..., None]
        ox, oy = int((xk - X0c) * RES), int((yk - Y0c) * RES)
        hh, ww = A.shape[:2]
        sl = canvas[oy:oy + hh, ox:ox + ww]
        A = A[:sl.shape[0], :sl.shape[1]]
        sl *= (1 - A + A * col)
    rgba = np.dstack([canvas, (canvas.min(2) < 0.995).astype(np.float32)])
    P.img(rgba, X0c, Y0c, Wc / RES, Hc / RES, z=100)
    for k, (cxk, cyk, xk, yk) in enumerate(centers):
        P.ax.add_patch(Ellipse((cxk, cyk), pw, ph, fc="none", ec=cols[k], lw=1.3, zorder=101))
        P.ax.add_patch(Ellipse((cxk, cyk), 3.8, 1.9, fc=RED, ec=INK, lw=0.4, zorder=130))
    xs = [c[0] for c in centers]; ys = [c[1] for c in centers]
    P.line(xs, ys, RED, 1.6, z=125)
    P.line([xs[-1], xs[-1]], [ys[-1], ytop + 1], RED, 1.6, z=125)
    P.t(xs[-1] + 2.5, ytop + 3.4, "EJE DEL Nº 31", "title", 11, RED, z=140)
    # etiquetas: al borde izquierdo o derecho de cada lámina según el zigzag
    for k, (cxk, cyk, xk, yk) in enumerate(centers):
        num, name, txt = info[k]
        left = dxs[k] < 0
        tx = xk + 2 if left else xk + pw - 2
        ha = "left" if left else "right"
        tyy = cyk + 2.4
        tag_w = textw(name, "title", 12) + 12
        bx = tx if left else tx - tag_w
        rot_rect(bx, tyy - 6.2, tag_w, 7.2, 0, cols[k], z=150)
        tc = WHITE if cols[k] in (INK, BLUE, VIOLET, PINK, GREEN, ORANGE) else INK
        P.t(bx + 1.6, tyy - 0.8, num, "monob", 7, tc, z=151)
        P.t(bx + 9.5, tyy - 0.8, name, "title", 12, tc, z=151)
        P.para(bx if left else tx - 82, tyy + 1.8, txt, 6.4, "b", INK, 68, ls=1.12, z=151, ha="left",
               bbox=dict(fc=WHITE, ec="none", pad=0.35, alpha=0.92))
    P.t(x1, ybot + 3.2, "Láminas = diferencia píxel a píxel entre MAPA 1…6 y COMPLETO (220 ppp), r = 560 m, dimétrica −32° · ×0,46, superpuestas en multiplicación.",
        "i", 6.2, DGREY, ha="right", va="top", z=140)

# ==================================================================== 02 RADIO
THEMES = [("comercio", "comercio", PINK), ("equipamientos", "equipamientos", VIOLET), ("arboles", "árboles", GREEN), ("transporte", "transporte", BLUE)]
def bloque02(y0):
    header(M, y0, "02", "RADIO · QUÉ HAY A 500 M", PINK, 1.2, "A",
           "INVENTARIO_FISICO_600M.gpkg (OSM, 8.021 elementos) · centro: centroide de la parcela")
    cx, cy, R0, R1 = M + 60, y0 + 64, 8, 38
    maxv = max(sum(MET["sectores"][k][s]) for k, _, _ in THEMES for s in range(16))
    scale = lambda v: R0 + (R1 - R0) * math.sqrt(v / maxv)
    P.circ(cx, cy, R1 + 3, fc=YELLOW, ec="none", z=3)
    for rv in (5, 20, 45, 80, 134):
        rr = scale(rv); P.circ(cx, cy, rr, ec=INK, lw=0.3, z=8, ls=(0, (1, 1.2)))
    for rv in (20, 80):
        P.t(cx + 0.8, cy - scale(rv) - 0.5, str(rv), "monob", 5.2, INK, z=9)
    for s in range(16):
        a0 = s * 22.5 - 11.25
        for j, (k, lab, col) in enumerate(THEMES):
            v = sum(MET["sectores"][k][s]); aa = a0 + 1.2 + j * 5.0
            P.ax.add_patch(Wedge((cx, cy), scale(v), aa - 90, aa + 4.6 - 90, width=scale(v) - R0, fc=col, ec="none", zorder=12))
            if v >= 40:
                am = math.radians(aa + 2.3)
                P.t(cx + (scale(v) + 2.0) * math.sin(am), cy - (scale(v) + 2.0) * math.cos(am), str(v), "monob", 5.4, col, ha="center", va="center", z=20,
                    bbox=dict(fc=WHITE, ec="none", pad=0.1))
    for s, lab in [(0, "N"), (4, "E"), (8, "S"), (12, "O")]:
        a = math.radians(s * 22.5)
        P.t(cx + (R1 + 6.5) * math.sin(a), cy - (R1 + 6.5) * math.cos(a), lab, "title", 14, INK, ha="center", va="center")
    P.line([cx, cx], [cy - R1 - 2, cy + R1 + 2], INK, 0.8, z=11, ls=(0, (3, 1.5)))
    P.circ(cx, cy, R0 - 1, fc=RED, ec=INK, lw=0.6, z=15)
    P.t(cx, cy, "31", "title", 13, WHITE, ha="center", va="center", z=16)
    P.para(M, y0 + 112.5, "ROSA · 16 sectores × 4 temas · 0–500 m · radio = raíz de n\ndiscontinua: eje de Ribera (N–S)", 6.0, "monob", INK, 80)
    for j, (k, lab, col) in enumerate(THEMES):
        P.rect(M + (j % 2) * 30, y0 + 18 + (j // 2) * 5, 3.6, 3.6, fc=col); P.t(M + 5 + (j % 2) * 30, y0 + 21 + (j // 2) * 5, lab, "b", 6.8)
    # matriz
    hx, hy = M + 126, y0 + 21
    rows = [("comercio", "comercio", PINK), ("equipamientos", "equipamientos", VIOLET), ("arboles", "árboles", GREEN), ("bancos", "bancos", LIME),
            ("transporte", "paradas / bocas", BLUE), ("portales", "portales", ORANGE), ("farolas", "farolas", YELLOW),
            ("patrimonio", "patrimonio", RED), ("barreras", "barreras", DGREY), ("edificios", "edificios", CYAN)]
    rings = [0, 100, 200, 300, 400, 500]
    areas = [math.pi * (rings[i + 1] ** 2 - rings[i] ** 2) / 10000 for i in range(5)]
    cw, ch = 19.5, 8.0
    P.t(hx, hy - 3.5, "DENSIDAD · elementos por hectárea en cada anillo", "monob", 6, INK)
    for i in range(5):
        P.t(hx + 31 + i * cw + cw / 2, hy + 2.6, f"{rings[i]}–{rings[i+1]} m", "monob", 5.6, INK, ha="center")
    for r_, (k, lab, col) in enumerate(rows):
        vals = [MET["rings"][k][i] / areas[i] for i in range(5)]; mx = max(vals) or 1
        yy = hy + 4.5 + r_ * ch
        P.t(hx, yy + ch * 0.62, lab, "cond", 8.8, INK)
        P.t(hx + 30, yy + ch * 0.62, str(sum(MET["rings"][k])), "monob", 5.6, DGREY, ha="right")
        for i, v in enumerate(vals):
            a = 0.12 + 0.88 * (v / mx)
            P.rect(hx + 31 + i * cw, yy, cw - 0.9, ch - 0.9, fc=col, alpha=a, z=6)
            tc = WHITE if a > 0.6 and col not in (YELLOW, LIME, CYAN) else INK
            P.t(hx + 31 + i * cw + cw / 2, yy + ch * 0.62, fnum(v, 1), "monob", 6.3, tc, ha="center", z=7)
            if v == mx: P.rect(hx + 31 + i * cw - 0.3, yy - 0.3, cw - 0.3, ch - 0.3, ec=INK, lw=1.4, z=8)
    P.t(hx, hy + 4.5 + 10 * ch + 3.8, "Marco negro = anillo de máxima densidad de la fila; tono relativo a la fila.", "i", 6.3, DGREY)
    # escalera
    lx0, lx1 = M + 264, PW - M - 2
    ly = y0 + 24; step = 4.75
    near = MET["nearest"]
    keys = [("alimentación", "alimentación", PINK), ("árbol", "árbol", GREEN), ("banco", "banco", LIME), ("bar/café", "bar / café", VIOLET),
            ("colegio", "colegio CEIP Emilia Pardo Bazán", VIOLET), ("deporte", "pista deportiva", GREEN), ("farmacia", "farmacia", VIOLET),
            ("supermercado", "supermercado", PINK), ("juegos infantiles", "juegos infantiles", GREEN), ("fuente de beber", "fuente de beber", CYAN),
            ("bus", "parada bus · El Rastro", BLUE), ("universidad", "Univ. Carlos III · Pta. de Toledo", VIOLET), ("plaza", "plaza General Vara del Rey", GREEN),
            ("bici pública", "BiciMAD", BLUE), ("mercado", "mercado de San Fernando", PINK), ("salud", "centro de salud Lavapiés", VIOLET),
            ("metro (boca)", "metro · Puerta de Toledo (L5)", RED)]
    sx = lambda d: lx0 + 60 + (lx1 - lx0 - 60) * d / 400.0
    P.t(lx0, y0 + 19.5, "A CUÁNTO ESTÁ · línea recta desde el centroide de la parcela", "monob", 6, INK)
    hgt = len(keys) * step
    P.rect(sx(0), ly - 2, sx(100) - sx(0), hgt + 1, fc=YELLOW, z=2)
    P.t(sx(50), ly + hgt + 9.5, "todo lo cotidiano: < 1'15\"", "cond", 8, INK, ha="center")
    for m_ in range(0, 401, 50):
        P.line([sx(m_), sx(m_)], [ly - 2, ly + hgt - 1], INK if m_ % 100 == 0 else GREY, 0.3, z=4)
        P.t(sx(m_), ly + hgt + 2.4, f"{m_}", "monob", 5.4, INK, ha="center")
        if m_ % 100 == 0 and m_:
            P.t(sx(m_), ly + hgt + 5.6, f"{m_/80:.2f}".replace(".", ",") + "'", "mono", 5, DGREY, ha="center")
    for i, (k, lab, col) in enumerate(keys):
        d = near[k]["d"]; yy = ly + i * step
        P.t(lx0 + 58, yy + 1.1, lab, "condm", 7.6, INK, ha="right")
        P.line([sx(0), sx(d)], [yy, yy], col, 2.6, z=10)
        P.circ(sx(d), yy, 1.5, fc=col, ec=INK, lw=0.5, z=11)
        P.t(sx(d) + 2.4, yy + 1.1, f"{fnum(d,0)} m", "monob", 6, INK, z=12)
    P.t(lx1, ly + hgt + 9.5, "minutos a 80 m/min sin rodeos = cota inferior", "i", 6.2, DGREY, ha="right")
    return y0 + 118

# ==================================================================== 03 LA CALLE QUE BAJA
SS = 565.0 / 580.0
def bloque03(y0):
    header(M, y0, "03", "LA CALLE QUE BAJA · 580 M DE RIBERA DESPLEGADOS SOBRE SU PENDIENTE", YELLOW, -0.9, "A/B",
           "alzados rectificados de 23 panorámicas SV 2021-22 · cotas de cámara SV − 2,5 m (B)")
    X = lambda s: M + s * SS
    z0 = zs(0)
    drop = lambda s: (z0 - zs(s)) * SS          # mm que baja el eje respecto a Cascorro (misma escala que las fotos)
    hs = 36.5 * SS; rh = 1.45; nr = 11; tab = 2.0; band = 9.0
    stack = nr * rh + tab + 0.6
    yA0 = y0 + 16 + hs + stack             # borde superior del eje en s = 0
    ya = lambda s: yA0 + drop(s)           # borde superior del eje
    yb_ = lambda s: yA0 + band + drop(s)   # borde inferior del eje
    pts = sorted(set([0.0, 580.0] + [a[0] for a in AL if a[0] < 580]))
    def along(s0, s1, off, h, top=True):
        ss = [s0] + [p for p in pts if s0 < p < s1] + [s1]
        base = ya if top else yb_
        up = [(X(s), base(s) + off) for s in ss]
        dn = [(X(s), base(s) + off + h) for s in ss[::-1]]
        return up + dn
    # ---- fotos cizalladas por la pendiente
    PXM = 2600 / 160.0
    for side in "WE":
        strips = [np.asarray(Image.open(f"/home/claude/g3/fig/strips/continuo_{side}_{a}_{a+160}.jpg").convert("RGB")) for a in (0, 160, 320, 480)]
        full = np.concatenate(strips, 1)[:, :int(580 * PXM)]
        if side == "E": full = full[::-1]
        Hh, Ww = full.shape[:2]
        dmax = drop(580) / SS * PXM
        can = np.zeros((Hh + int(dmax) + 2, Ww, 4), np.uint8)
        cols_s = (np.arange(Ww) + 0.5) / PXM
        off = np.array([int(round(drop(s) / SS * PXM)) for s in cols_s])
        for o in np.unique(off):
            m = off == o
            can[o:o + Hh, m, :3] = full[:, m]; can[o:o + Hh, m, 3] = 255
        topmm = ya(0) - stack - hs if side == "W" else yb_(0) + stack
        P.img(can, X(0), topmm, 580 * SS, can.shape[0] / PXM * SS, z=3)
    # ---- línea de cota de Cascorro (horizontal) y cota final: la bajada se ve
    P.line([X(0), X(580) + 3.5], [ya(0), ya(0)], RED, 0.9, z=2, ls=(0, (5, 2)))
    P.t(X(580) + 1, ya(0) - 1.5, "horizontal de Cascorro", "monob", 5.2, RED, ha="right", z=21, bbox=dict(fc=WHITE, ec="none", pad=0.2))
    xe = X(580) + 3.5
    P.line([xe, xe], [ya(0), ya(580)], RED, 1.4, z=20)
    for yy in (ya(0), ya(580)): P.line([xe - 1.5, xe + 1.5], [yy, yy], RED, 1.4, z=20)
    P.t(xe + 1.6, (ya(0) + ya(580)) / 2, f"−{fnum(z0 - zs(580),1)} m", "title", 13, RED, rot=90, ha="center", va="bottom", z=21)
    # ---- tiras de año y código de rasgos (paralelogramos que siguen la pendiente)
    def epoch(y): return RED if y < 1900 else (ORANGE if y < 1960 else (CYAN if y < 2000 else VIOLET))
    rasgos = [("pb_com", "PB comercial", PINK), ("cierre", "cierre enrollable", RED), ("grafiti", "grafiti", ORANGE),
              ("zocalo", "zócalo", DGREY), ("balcon", "balcón propio", GREEN), ("recercado", "recercado", BLUE),
              ("toldo_alto", "textil alto", YELLOW), ("vegetal", "plantas", LIME), ("alero", "alero / cornisa", VIOLET),
              ("instal", "instalaciones", CYAN), ("expo", "exposición en acera", PINK)]
    def val(c, k):
        v = COD[c].get(k)
        if k == "balcon": return None if v is None else (1 if v in ("ind", "mixto") else 0)
        return v
    for f in FAC:
        if f["s0"] > 580: continue
        s0, s1 = f["s0"] + 0.15, min(f["s1"], 580) - 0.15
        W = f["side"] == "W"
        if W: P.poly(along(s0, s1, -stack, tab, True), fc=epoch(f["anio"]), z=8)
        else: P.poly(along(s0, s1, stack - tab, tab, False), fc=epoch(f["anio"]), z=8)
        for j, (k, lab, col) in enumerate(rasgos):
            v = val(f["codigo"], k)
            off = (-stack + tab + 0.3 + j * rh) if W else (stack - tab - 0.3 - (j + 1) * rh)
            pp = along(s0, s1, off + 0.15, rh - 0.3, W)
            if v == 1: P.poly(pp, fc=col, z=8)
            elif v == 0: P.poly(pp, fc=LGREY, z=8)
            else: P.poly(pp, fc="none", ec=GREY, lw=0.2, hatch="/////", z=8)
        # código de fachada sobre la tira
        sm = (s0 + s1) / 2
        yy = (ya(sm) - stack + tab * 0.78) if W else (yb_(sm) + stack - tab * 0.22)
        if s1 - s0 > 6:
            P.t(X(sm), yy, f"{cod(f['codigo'])}·{f['anio']}", "monob", 3.8, WHITE if epoch(f["anio"]) in (RED, VIOLET) else INK, ha="center", z=9)
    # ---- eje: banda negra en pendiente con cinta de pendiente
    P.poly(along(0, 580, 0, band, True), fc=INK, z=10)
    for a, b in zip(AL, AL[1:]):
        if a[0] >= 580: break
        b0 = min(b[0], 580); g = (a[1] - b[1]) / (b[0] - a[0]) * 100
        c = YELLOW if g < 4 else (ORANGE if g < 7 else (RED if g < 9 else PINK))
        P.poly(along(a[0], b0, band - 2.6, 2.6, True), fc=c, z=11)
        if b0 - a[0] >= 30:
            P.t(X((a[0] + b0) / 2), ya((a[0] + b0) / 2) + band - 0.55, f"{fnum(g,1)} %", "monob", 4.4, INK, ha="center", z=12)
    for s in range(0, 581, 20):
        big = s % 100 == 0
        P.line([X(s), X(s)], [ya(s), ya(s) + (3.2 if big else 1.6)], WHITE, 0.6, z=12)
        if big and s < 580: P.t(X(s) + 0.8, ya(s) + 3.0, f"{s}", "monob", 5.4, WHITE, z=12, va="center")
    for i, e in enumerate(META["estaciones"]):
        if e["s_m"] > 580: continue
        s = e["s_m"]
        P.circ(X(s), ya(s) + 5.4, 0.55, fc=CYAN, ec="none", z=13)
    P.t(X(1.5), ya(0) - stack - hs + 5.5, "CASCORRO · 647,0 m", "title", 11, WHITE, z=21, bbox=dict(fc=INK, ec="none", pad=0.6))
    P.t(X(578.5), yb_(580) + stack + hs - 2.5, "RONDA DE TOLEDO · 610,0 m", "title", 11, WHITE, ha="right", z=21, bbox=dict(fc=INK, ec="none", pad=0.6))
    # ---- el 31
    s31 = (S31a + S31b) / 2
    P.poly([(X(S31a), ya(S31a)), (X(S31b), ya(S31b)), (X(S31b), yb_(S31b) + stack + hs), (X(S31a), yb_(S31a) + stack + hs)],
           fc="none", ec=RED, lw=2.0, z=22)
    P.poly(along(S31a, S31b, 0, band, True), fc=RED, z=14)
    P.t(X(s31), ya(s31) + 7.2, "31", "title", 12, WHITE, ha="center", z=15)
    P.t(X(S31b) + 2, yb_(S31b) + stack + hs - 2.5, "Nº 31 · la nave comercial 2008–2022 no figura en catastro", "cond", 8.2, WHITE, z=30,
        bbox=dict(fc=RED, ec="none", pad=0.6))
    P.t(X(401), yb_(401) + 2.5, "6,8 % = 1,0 m de desnivel\nen los 14,93 m de frente del 31", "title", 10, RED, z=30, va="top")
    # ---- leyendas en los triángulos vacíos que deja la pendiente
    # arriba-derecha: acera O + rasgos
    lx = X(452); ly = y0 + 18
    P.t(lx, ly, "ACERA OESTE · PARES · abatida hacia arriba", "title", 10.5, INK)
    P.t(lx, ly + 4, "ACERA ESTE · IMPARES · abatida hacia abajo", "title", 10.5, INK)
    for j, (k, lab, col) in enumerate(rasgos):
        cx_ = lx + (j % 4) * 27.5; cy_ = ly + 8 + (j // 4) * 4.1
        P.rect(cx_, cy_ - 2.4, 3.2, 2.6, fc=col, z=20); P.t(cx_ + 4.3, cy_, lab, "r", 6.3, INK, z=20)
    # abajo-izquierda: épocas
    ex, ey = X(0), yb_(0) + stack + hs + 6
    P.t(ex, ey, "AÑO CATASTRAL DEL FRENTE", "monob", 6, INK)
    for i, (c, s) in enumerate([(RED, "antes de 1900 · 15"), (ORANGE, "1900–1959 · 10"), (CYAN, "1960–1999 · 13"), (VIOLET, "2000 o después · 6")]):
        P.rect(ex + (i % 2) * 38, ey + 2 + (i // 2) * 4.4, 4, 3, fc=c); P.t(ex + 5.5 + (i % 2) * 38, ey + 4.6 + (i // 2) * 4.4, s, "r", 6.6)
    P.t(ex, ey + 14.5, "cinta del eje · pendiente por tramo:", "monob", 5.6, INK)
    for i, (c, s) in enumerate([(YELLOW, "< 4 %"), (ORANGE, "4–7 %"), (RED, "7–9 %"), (PINK, "> 9 %")]):
        P.rect(ex + i * 19, ey + 16.5, 4, 2.6, fc=c); P.t(ex + 5.2 + i * 19, ey + 18.8, s, "monob", 5.6)
    P.para(ex, ey + 23.5, "Rasgos: color = presente · gris = ausente · rayado = no legible (árbol, obra, recorte). 44 frentes en catastro, 42 legibles. "
           "Fotos, pendiente y planta a la misma escala (1:1.027).", 6.3, "i", DGREY, 72)
    return yb_(580) + stack + hs + 3

# ==================================================================== 04 PATRONES
def bloque04(y0):
    header(M, y0, "04", "PATRONES · ONCE RESPUESTAS QUE LA CALLE YA DA", GREEN, 1.3, "A/B",
           "patrón = 8 o más casos independientes · B lectura visual · A catastro")
    cols = 11; gap = 3.2; w = (CWID - gap * (cols - 1)) / cols
    pals = [GREEN, RED, INK, BLUE, YELLOW, LIME, VIOLET, CYAN, PINK, ORANGE, RED]
    fields = {"P01": ("balcon", "ind"), "P02": ("cierre", 1), "P03": ("zocalo", 1), "P04": ("recercado", 1), "P05": ("toldo_alto", 1),
              "P06": ("vegetal", 1), "P07": ("alero", 1), "P08": ("instal", 1), "P09": ("expo", 1)}
    extra = [dict(id="P10", nombre="Salto de altura entre vecinos", pregunta="¿Hay una cornisa que continuar?", n=9, N=28),
             dict(id="P11", nombre="Sustitución parcela a parcela", pregunta="¿De cuándo es lo construido?", n=19, N=44)]
    allp = PAT + extra
    photo_h = 21; jit = [0, 3, -1, 2.5, 0.5, -1.5, 2, 0, 3, -1, 1.5]
    yend = 0
    for i, p in enumerate(allp):
        x = M + i * (w + gap); y = y0 + 17 + jit[i]
        col = pals[i]; tc = WHITE if col in DARK else INK
        yi = y + 9
        # foto o diagrama
        if p["id"] in fields:
            cs = p["casos"][0]
            im = Image.open(f"/home/claude/g3/fig/panel/{p['id']}_{cs}_fit.jpg").convert("RGB")
            W_, H_ = im.size; nh = int(W_ / (w / photo_h)); tp = max(0, (H_ - nh) // 2)
            P.img(np.asarray(im.crop((0, tp, W_, tp + nh))), x, yi, w, photo_h, z=5)
            P.t(x + w - 1, yi + photo_h - 1.2, cod(cs), "monob", 5.5, WHITE, ha="right", z=12, bbox=dict(fc=INK, ec="none", pad=0.3))
        elif p["id"] == "P10":
            P.rect(x, yi, w, photo_h, fc=INK, z=4)
            L = sorted([f for f in FAC if f["side"] == "W" and f["s0"] < 420], key=lambda f: f["s0"])
            s0 = L[0]["s0"]; s1 = L[-1]["s1"]; sc_ = (w - 2) / (s1 - s0)
            for f in L:
                hh = f["plantas_frente"] * 1.9
                P.rect(x + 1 + (f["s0"] - s0) * sc_, yi + photo_h - 2 - hh, (f["s1"] - f["s0"]) * sc_, hh, fc=GREY, ec=INK, lw=0.2, z=6)
            for (sd, sj, dj, h1, h2) in JUMPS:
                if sd == "W" and dj >= 2 and sj < 420:
                    xx = x + 1 + (sj - s0) * sc_
                    P.line([xx, xx], [yi + photo_h - 2 - h1 * 1.9, yi + photo_h - 2 - h2 * 1.9], ORANGE, 1.8, z=8)
            P.t(x + 1.2, yi + 3.3, "acera O · 0–420 m · plantas", "monob", 4.6, WHITE, z=9)
        else:
            P.rect(x, yi, w, photo_h, fc=INK, z=4)
            bins = {}
            for yr in (f["anio"] for f in FR): b = (yr // 10) * 10; bins[b] = bins.get(b, 0) + 1
            a0, a1 = 1840, 2025
            for b, nn in bins.items():
                xx = x + 1 + (b - a0) / (a1 - a0) * (w - 2)
                for k in range(nn):
                    P.rect(xx, yi + photo_h - 4.5 - (k + 1) * 1.9, (w - 2) / 18.5 - 0.2, 1.7, fc=RED if b < 1960 else YELLOW, z=6)
            for yr in (1850, 1900, 1950, 2000):
                P.t(x + 1 + (yr - a0) / (a1 - a0) * (w - 2), yi + photo_h - 1, str(yr), "monob", 4.2, WHITE, ha="center", z=7)
            P.t(x + 1.2, yi + 3.3, "44 frentes por década", "monob", 4.6, WHITE, z=9)
        # cabecera de tarjeta superpuesta a la foto (loca)
        rot_rect(x - 0.8, y, w + 1.6, 9.5, (-2 if i % 2 else 2), col, z=14)
        P.t(x + 1.2, y + 7.6, p["id"], "title", 17, tc, rot=(-2 if i % 2 else 2), rotation_mode="anchor", z=15)
        pct = round(100 * p["n"] / p["N"])
        P.t(x + w / 2 + 3, yi + photo_h - 2, f"{pct}%", "title", 34, WHITE, z=13, ha="center",
            path_effects=[__import__("matplotlib.patheffects", fromlist=["x"]).withStroke(linewidth=2.2, foreground=col)])
        P.para(x, yi + photo_h + 2.2, p["nombre"], 8.4, "cond", INK, 24, ls=1.02)
        yw = yi + photo_h + 10.5
        per = 13; cell = w / per
        for k in range(p["N"]):
            r, c = divmod(k, per)
            P.rect(x + c * cell + 0.2, yw + r * 2.4, cell - 0.4, 2.0, fc=col if k < p["n"] else LGREY, z=6)
        yq = yw + 4 * 2.4 + 0.4
        lv = "A" if p["id"] in ("P10", "P11") else "B"
        P.t(x, yq + 2.5, f"{p['n']} / {p['N']}", "monob", 6.5, INK); P.t(x + w, yq + 2.5, lv, "monob", 6.5, LEVEL[lv], ha="right")
        P.para(x, yq + 3.8, p["pregunta"], 6.6, "i", DGREY, 27, ls=1.1)
        ym = yq + 12
        P.line([x, x + w], [ym, ym], INK, 0.5)
        if p["id"] in fields:
            k, v = fields[p["id"]]
            for f in FAC:
                if f["s0"] > 580: continue
                if COD[f["codigo"]].get(k) == v:
                    xx = x + f["s0"] / 580 * w; ww = max(0.5, (min(f["s1"], 580) - f["s0"]) / 580 * w)
                    P.rect(xx, ym - 1.6 if f["side"] == "W" else ym + 0.2, ww, 1.4, fc=col, z=7)
        elif p["id"] == "P10":
            for (sd, sj, dj, h1, h2) in JUMPS:
                if dj >= 2: P.rect(x + sj / 580 * w - 0.35, ym - 1.6 if sd == "W" else ym + 0.2, 0.7, 1.4, fc=col, z=7)
        else:
            for f in FR:
                if f["anio"] >= 1960 and f["s0"] <= 580:
                    xx = x + f["s0"] / 580 * w; ww = max(0.5, (min(f["s1"], 580) - f["s0"]) / 580 * w)
                    P.rect(xx, ym - 1.6 if f["side"] == "W" else ym + 0.2, ww, 1.4, fc=col, z=7)
        P.line([x + S31a / 580 * w] * 2, [ym - 2.3, ym + 2.3], RED, 0.9, z=8)
        yend = max(yend, ym + 3)
    P.t(M, yend + 3.2, "Micro-calle bajo cada patrón: dónde aparecen los casos en los 580 m (arriba acera O, abajo acera E) · trazo rojo = nº 31.", "i", 6.3, DGREY)
    return yend + 4

# ==================================================================== 05 SOL · TIEMPO · CRITERIOS
def bloque05(y0):
    header(M, y0, "05", "SOL · TIEMPO · CRITERIOS", ORANGE, -1.2, "B/C",
           "modelo 2,5D propio · PB 4,0 m + 3,1 m/planta (B) · paso 15 min · celdas 1 m · NOAA")
    yb = y0 + 17; ybot = PH - 16; hb = ybot - yb
    # 5a
    x = M; w = 150
    P.t(x, yb + 2.5, "HORAS DE SOL SOBRE LA PARCELA SEGÚN LA COTA", "title", 10.5)
    cotas = ["0", "4", "7.1", "10.2", "13.3", "16.4", "19.5", "22.6", "25.7"]
    labs = ["suelo", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8 · cub."]
    dates = [("2026-12-21", "21 dic", BLUE), ("2026-03-21", "21 mar", ORANGE), ("2026-06-21", "21 jun", YELLOW)]
    gx = x + 17; gw = 84; gy = yb + 8; gh = hb - 15
    rowh = gh / len(cotas); hmax = 15
    for i, c in enumerate(cotas):
        yy = gy + gh - (i + 1) * rowh
        P.t(gx - 1.5, yy + rowh * 0.5, labs[i], "condm", 6.8, INK, ha="right")
        P.t(gx - 1.5, yy + rowh * 0.5 + 2.3, f"{c.replace('.', ',')} m", "mono", 4.6, DGREY, ha="right")
        bh = (rowh - 1.0) / 3
        for j, (dk, dl, col) in enumerate(dates):
            v = SOL[dk][c]["media"]
            P.rect(gx, yy + 0.5 + j * bh, v / hmax * gw, bh * 0.88, fc=col, ec=INK if col == YELLOW else "none", lw=0.25, z=8)
        vd = SOL["2026-12-21"][c]
        P.t(gx + gw + 2, yy + rowh * 0.5 + 0.6, f"{fnum(vd['media'],2)} h", "monob", 5.6, BLUE)
        P.t(gx + gw + 15, yy + rowh * 0.5 + 0.6, f"{fnum(vd['pct_2h'],1)} %", "monob", 5.6, BLUE)
        P.rect(gx + gw + 28, yy + rowh * 0.5 - 1.3, vd['pct_2h'] / 100 * 16, 2, fc=BLUE, z=6)
        P.rect(gx + gw + 28, yy + rowh * 0.5 - 1.3, 16, 2, ec=BLUE, lw=0.3, z=6)
    P.t(gx + gw + 2, gy - 1.2, "21-DIC · media · solar con 2 h o más", "monob", 4.8, BLUE)
    for hh in range(0, 16, 3):
        P.line([gx + hh / hmax * gw] * 2, [gy, gy + gh], GREY, 0.25, z=5, ls=(0, (1, 1)))
        P.t(gx + hh / hmax * gw, gy + gh + 3, f"{hh} h", "monob", 5, INK, ha="center")
    p1, p2 = SOL["2026-12-21"]["19.5"]["pct_2h"], SOL["2026-12-21"]["22.6"]["pct_2h"]
    z50 = 19.5 + (50 - p1) / (p2 - p1) * 3.1
    zp = lambda z: gy + gh - rowh * (0.5 + np.interp(z, [0, 4, 7.1, 10.2, 13.3, 16.4, 19.5, 22.6, 25.7], range(9)))
    P.line([gx, gx + gw + 46], [zp(z50), zp(z50)], RED, 1.2, z=12, ls=(0, (3, 1.5)))
    P.t(gx + gw + 47, zp(z50) + 0.8, f"{fnum(z50,1)} m", "monob", 5.8, RED, z=13, bbox=dict(fc=WHITE, ec="none", pad=0.2))
    P.t(x, yb + 6.6, f"— — {fnum(z50,1)} m: cota a la que el 50 % del solar recibe 2 h de sol el 21-dic (interp. lineal P6–P7)", "cond", 6.8, RED)
    for j, (dk, dl, col) in enumerate(dates):
        P.rect(gx + 82 + j * 16, yb + 0.1, 3.4, 3, fc=col, ec=INK, lw=0.2); P.t(gx + 86.5 + j * 16, yb + 2.5, dl, "monob", 5.6)
    # 5b
    x2 = M + w + 6; w2 = 190
    P.t(x2, yb + 2.5, "SUELO DEL SOLAR · HORAS DE SOL", "title", 10.5)
    X_, Y_ = SOMB["X"], SOMB["Y"]
    from matplotlib.path import Path as MP
    inside = MP(np.array(PARCELA.exterior.coords)).contains_points(np.c_[X_.ravel(), Y_.ravel()]).reshape(X_.shape)
    bx0, by0, bx1, by1 = PARCELA.bounds
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("sol", ["#12005E", BLUE, CYAN, YELLOW, "#FFFFFF"])
    mw = 44; mh = mw * (by1 - by0 + 4) / (bx1 - bx0 + 4)
    summ = json.load(open(D + 'sombras_resumen.json'))['parcela']
    for j, (dk, dl, col) in enumerate(dates):
        h_ = SOMB[f"h_{dk}"]
        sel = (X_ >= bx0 - 2) & (X_ <= bx1 + 2) & (Y_ >= by0 - 2) & (Y_ <= by1 + 2)
        ii = np.where(sel.any(1))[0]; jj = np.where(sel.any(0))[0]
        sub = h_[ii[0]:ii[-1] + 1, jj[0]:jj[-1] + 1]; ins = inside[ii[0]:ii[-1] + 1, jj[0]:jj[-1] + 1]
        rgba = cmap(np.clip(sub / 12, 0, 1)); rgba[~ins, 3] = 0.10
        if Y_[ii[0], 0] < Y_[ii[-1], 0]: rgba = rgba[::-1]
        xx = x2 + j * (mw + 4); yy = yb + 6
        P.img(rgba, xx, yy, mw, mh, z=6, interp="nearest"); P.rect(xx, yy, mw, mh, ec=INK, lw=0.4, z=7)
        P.t(xx, yy + mh + 3.2, f"{dl} · media {fnum(summ[dk]['media_parcela_h'],2)} h", "monob", 5.4, INK)
    bx_ = x2 + 3 * (mw + 4)
    for k in range(12): P.rect(bx_, yb + 6 + mh - (k + 1) * mh / 12, 3, mh / 12, fc=cmap(k / 11), z=6)
    P.t(bx_ + 4, yb + 6 + mh, "0 h", "monob", 5); P.t(bx_ + 4, yb + 8, "12 h", "monob", 5)
    P.para(bx_ + 12, yb + 5, "N arriba; calle a la izquierda, fondo a la derecha. 21-dic: 0 % del solar con 4 h de sol; 2,9 % con 2 h.", 6, "i", DGREY, 21, ls=1.15)
    sy0 = ybot - 2; ssc = 0.78
    ys_ = lambda z: sy0 - z * ssc
    xs_ = lambda s: x2 + 12 + s * ssc
    Hs = 25.7; tx = xs_(14.93 + 36)
    P.t(tx, ys_(Hs) - 2.5, "SECCIÓN N–S POR EL FRENTE · rayo a mediodía solar", "title", 9.5)
    P.line([xs_(-12), xs_(14.93 + 20)], [ys_(0), ys_(0)], INK, 1.0)
    P.rect(xs_(-12), ys_(4 + 2 * 3.1), 12 * ssc, (4 + 2 * 3.1) * ssc, fc=GREY, ec=INK, lw=0.4, z=6)
    P.t(xs_(-6), ys_(4 + 2 * 3.1) - 1, "N · 3 pl.", "monob", 4.8, INK, ha="center")
    P.rect(xs_(0), ys_(0) - 1.0, 14.93 * ssc, 1.0, fc=RED, z=7)
    P.t(xs_(7.46), ys_(0) + 3.0, "31 · 14,93 m", "monob", 5.2, RED, ha="center")
    P.rect(xs_(14.93), ys_(Hs), 12 * ssc, Hs * ssc, fc=GREY, ec=INK, lw=0.4, z=6)
    P.t(xs_(14.93 + 13) + 1, ys_(Hs) + 2, "S · 8 pl.\n25,7 m (B)", "monob", 4.8, INK, va="top")
    for i, (alt, dl, col) in enumerate([(26.15, "21 dic · 26,2°", BLUE), (49.59, "21 mar · 49,6°", ORANGE), (73.03, "21 jun · 73,0°", "#D4B200")]):
        t_ = math.tan(math.radians(alt)); z0 = Hs - 14.93 * t_
        xa, ya = xs_(14.93), ys_(Hs)
        if z0 >= 0: xb, yb2 = xs_(0), ys_(z0)
        else: xb, yb2 = xs_(14.93 - Hs / t_), ys_(0)
        L = 7.0
        P.line([xa + L * math.cos(math.radians(alt)), xb], [ya - L * math.sin(math.radians(alt)), yb2], col, 1.1, z=9)
        P.t(tx, ys_(Hs) + 2 + i * 4.2, dl + (f" · sol en el frente desde {fnum(z0,1)} m" if z0 > 0 else " · sol hasta el suelo"), "monob", 5.0, col, z=9)
        if z0 > 0: P.line([xs_(0), xs_(0)], [ys_(0), ys_(z0)], col, 2.6, z=8)
    P.para(tx, ys_(Hs) + 15, "Geometría (A) sobre alturas por plantas (B): al mediodía del 21-dic el vecino sur deja en sombra el frente hasta 18,4 m.", 6.2, "i", INK, 52, ls=1.15)
    # 5c
    x3 = x2 + w2 + 6; w3 = PW - M - x3
    P.t(x3, yb + 2.5, "EL SOLAR EN EL TIEMPO · Street View 2008–2022", "title", 10.5)
    fechas = [("2008-8", "2008 · chimeneas y hogar"), ("2013-10", "2013 · liquidación"), ("2018-8", "2018 · Fang Decoración"), ("2021-7", "2021 · nave tras el atrio")]
    tw = (w3 - 3 * 2.5) / 4; th = 15.5
    for i, (fk, lab) in enumerate(fechas):
        im = Image.open(f"/home/claude/g3/vistas/hist/{fk}.jpg").convert("RGB")
        W_, H_ = im.size; nh = int(W_ * th / tw); tp = max(0, (H_ - nh) // 2)
        xx = x3 + i * (tw + 2.5)
        P.img(np.asarray(im.crop((0, tp, W_, tp + nh))), xx, yb + 5.5, tw, th, z=5)
        P.rect(xx, yb + 5.5, tw, th, ec=INK, lw=0.5, z=6)
        P.t(xx, yb + 5.5 + th + 3.0, lab, "monob", 5.0, INK)
    ny0 = yb + 5.5 + th + 9
    P.t(x3, ny0, "DE LA EVIDENCIA AL CRITERIO · hallazgos > patrones > criterios v1 (C)", "title", 9.5)
    H = ["H-01 el solar no está vacío", "H-02 el sol de invierno solo llega arriba", "H-03 entre 3 y 10 plantas", "H-04 hueco con balcón propio",
         "H-05 planta baja que se cierra", "H-06 tienda en la acera", "H-07 la calle desciende", "H-08 denso y sin estancia"]
    Pp = ["P01", "P02", "P05", "P08", "P09", "P10", "P11"]
    Cc = ["C1 volumen por sol", "C2 PB de dos estados", "C3 umbral en pendiente", "C4 comunes arriba", "C5 balcón + textil", "C6 fondo de corrala", "C7 segunda trama"]
    ny = ny0 + 2.0; nh = ybot + 2 - ny
    hx = x3; hw = 50; px_ = x3 + 92; cx_ = PW - M - 36
    Hy = {h[:4]: ny + (i + 0.5) * nh / len(H) for i, h in enumerate(H)}
    Py = {p: ny + (i + 0.5) * nh / len(Pp) for i, p in enumerate(Pp)}
    Cy = {c[:2]: ny + (i + 0.5) * nh / len(Cc) for i, c in enumerate(Cc)}
    for h in H: P.t(hx, Hy[h[:4]] + 1, h, "condm", 6.6, INK)
    pcol = dict(zip([p["id"] for p in PAT] + ["P10", "P11"], [GREEN, RED, INK, BLUE, YELLOW, LIME, VIOLET, CYAN, PINK, ORANGE, RED]))
    for p in Pp:
        P.rect(px_ - 5, Py[p] - 2.0, 10, 3.4, fc=pcol[p], z=20)
        P.t(px_, Py[p] + 0.55, p, "monob", 5.4, WHITE if pcol[p] in DARK else INK, ha="center", z=21)
    for c in Cc:
        P.rect(cx_ - 1.5, Cy[c[:2]] - 2.1, 37.5, 3.5, fc=ORANGE, z=20); P.t(cx_ + 0.3, Cy[c[:2]] + 0.55, c, "condm", 6.4, INK, z=21)
    HP = [("H-04", "P01"), ("H-05", "P02"), ("H-06", "P09"), ("H-03", "P10"), ("H-01", "P11")]
    PC = [("P01", "C5"), ("P05", "C5"), ("P02", "C2"), ("P08", "C7"), ("P10", "C1"), ("P11", "C1"), ("P11", "C6")]
    HC = [("H-02", "C1"), ("H-07", "C3"), ("H-08", "C4"), ("H-05", "C2"), ("H-01", "C6")]
    for a, b in HP: P.curve((hx + hw, Hy[a]), (px_ - 5, Py[b]), pcol[b], 1.3, z=12)
    for a, b in PC: P.curve((px_ + 5, Py[a]), (cx_ - 1.5, Cy[b]), pcol[a], 1.3, z=12)
    for a, b in HC: P.curve((hx + hw, Hy[a]), (cx_ - 1.5, Cy[b]), INK, 0.6, z=11, alpha=0.8)

def pie():
    y = PH - 5.5
    P.t(M, y - 3.4, "FUENTES · Catastro INSPIRE WFS + OVC (23-09-2026) · MAPPEADOS/ e INVENTARIO_FISICO_600M.gpkg (OpenStreetMap vía QGIS, 21/22-09-2026) · MER 2021 (Ayto. de Madrid) · "
        "Google Street View 2008–2022 (23 estaciones + 11 fechas del nº 31) · modelo de sombras y alzados rectificados propios.", "r", 6.2, INK)
    P.t(M, y, "Distancias en línea recta; recuentos OSM = lo que el inventario contiene (A). Alturas por plantas catastrales con PB 4,0 m + 3,1 m (B). Cotas de calle desde la altitud de cámara SV (B).",
        "i", 5.9, DGREY)
    P.t(PW - M, y, "RIBERA 31 · PANEL A1 · v2", "monob", 7, RED, ha="right")

if __name__ == "__main__":
    cabecera(); pegatinas()
    wmm = bloque01(); bloque01b(wmm)
    y2 = MY0 + MAPH + 8
    e2 = bloque02(y2)
    e3 = bloque03(e2 + 2)
    e4 = bloque04(e3 + 1)
    print("y", y2, e2, e3, e4)
    bloque05(e4 + 1)
    pie()
    out = "/home/claude/g3/a1/RIBERA31_PANEL_A1_v2"
    P.save(out + ".pdf", out + "_preview.png", dpi=50)
    print("ok")
