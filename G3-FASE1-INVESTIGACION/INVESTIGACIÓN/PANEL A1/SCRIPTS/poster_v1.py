"""PANEL A1 · RIBERA 31 · ATLAS DE INVESTIGACIÓN (594 × 841 mm, vertical)."""
import sys, json, math, pickle
sys.path.insert(0, "/home/claude/g3/a1"); sys.path.insert(0, "/home/claude/g3")
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
from kit import *
import plates as PL
import os
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
exec(open(D + "codificacion_fachadas.py").read())   # -> C (codificación de 42 fachadas)
COD = C
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
assert len(JUMPS) == MN["saltos_total"] and sum(j[2] >= 2 for j in JUMPS) == MN["saltos_ge2"], (len(JUMPS), sum(j[2] >= 2 for j in JUMPS))

def cod(c): return c.replace("W", "O")
def fnum(v, d=0):
    s = f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s

P = Poster()
M = 14.0; CWID = PW - 2 * M

# =====================================================================================  CABECERA
def cabecera():
    y0 = 14
    P.t(M - 1.2, y0 + 1, "ATLAS DE INVESTIGACIÓN · G3 · VIVIENDA TEMPORAL PARA JÓVENES · EL RASTRO, MADRID", "monob", 9, INK, va="top")
    # título monumental
    P.t(M - 2.5, y0 + 66, "RIBERA", "title", 238, INK, z=60)
    P.t(M - 2.5 + textw("RIBERA", "title", 238) + 6, y0 + 66, "31", "title", 238, RED, z=61)
    # subtítulo
    P.para(M, y0 + 70.5, "Una calle que baja 37 metros en 580, un solar que no está vacío y un sol de invierno que solo llega arriba. "
           "Siete mapeados, 42 fachadas, 23 panorámicas y un modelo de sombras leídos a la vez.", 10.5, "condm", INK, 125, ls=1.2)
    # bloque derecho: ficha + índice
    x = 330; w = PW - M - x
    P.rect(x, y0 + 4, w, 74, fc=INK, z=20)
    P.t(x + 4, y0 + 10.5, "FICHA", "monob", 7.5, YELLOW)
    ficha = [("Parcela", "Ribera de Curtidores 31 · 28005 Madrid"), ("Situación", "El Rastro · Embajadores · Centro"),
             ("Encargo", "Vivienda temporal para jóvenes"), ("Curso", "G3 · Proyectos · UEM · 2026-27"),
             ("Autor", "Adam Ihab"), ("Fecha", "24-09-2026"), ("SRC", "ETRS89 · UTM 30N (EPSG:25830)")]
    for i, (a, b) in enumerate(ficha):
        P.t(x + 4, y0 + 16 + i * 4.4, a.upper(), "mono", 6.3, GREY)
        P.t(x + 27, y0 + 16 + i * 4.4, b, "r", 7.6, WHITE)
    P.t(x + 4, y0 + 51, "ÍNDICE", "monob", 7.5, YELLOW)
    idx = [("01", "MAPEADOS · 7 capas", CYAN), ("02", "RADIO · 500 m a pie", PINK), ("03", "LA CALLE DESPLEGADA", YELLOW),
           ("04", "PATRONES · P01–P11", GREEN), ("05", "SOL · TIEMPO · CRITERIOS", ORANGE)]
    for i, (n, s, c) in enumerate(idx):
        yy = y0 + 53.5 + i * 4.4
        P.rect(x + 4, yy, 7, 3.8, fc=c, z=25); P.t(x + 7.5, yy + 3.05, n, "monob", 6.5, INK, ha="center", z=26)
        P.t(x + 13, yy + 3.1, s, "cond", 8.6, WHITE, z=26)
    # certeza
    xc = x + 95
    P.t(xc, y0 + 51, "CERTEZA", "monob", 7.5, YELLOW)
    for i, (l, s) in enumerate([("A", "medido: catastro, OSM, SV"), ("B", "inferido: lectura visual, modelo"), ("C", "hipótesis de proyecto")]):
        yy = y0 + 53.5 + i * 5.8
        P.rect(xc, yy, 6, 4.6, fc=LEVEL[l], z=25); P.t(xc + 3, yy + 3.6, l, "monob", 8, INK if l != "B" else WHITE, ha="center", z=26)
        P.t(xc + 8, yy + 3.4, s, "r", 7, WHITE, z=26)
    P.t(xc, y0 + 74, "Cada dato del panel lleva su nivel.", "i", 6.6, GREY)

# =====================================================================================  BANDA DE CIFRAS
def cifras():
    y = 95; h = 19
    items = [("650,9", "m²", "superficie de parcela", "A", YELLOW), ("14,93", "m", "frente a Ribera", "A", WHITE),
             ("49,48", "m", "fondo: una corrala", "A", PINK), ("25,8", "m", "ancho de calle en el 31", "A", WHITE),
             ("6,8", "%", "pendiente frente al 31", "A", CYAN), ("0,17", "h", "sol medio en suelo · 21-dic", "B", INK),
             ("3.204", "", "viviendas catastrales en 200 m", "A", WHITE), ("339", "m", "a la boca de metro más próxima", "A", BLUE),
             ("418", "", "comercios OSM en 500 m", "A", WHITE), ("30/39", "", "huecos con balcón propio", "B", GREEN)]
    wcell = CWID / len(items)
    for i, (v, u, lab, lvl, c) in enumerate(items):
        x = M + i * wcell
        dark = c in (INK, BLUE)
        P.rect(x, y, wcell - 1.2, h, fc=c, ec=INK, lw=0.8, z=20)
        tc = WHITE if dark else INK
        P.t(x + 2.2, y + 10.8, v, "title", 29, tc, z=22)
        vw = textw(v, "title", 29) + 1.6
        P.t(x + 2.2 + vw, y + 10.8, u, "cond", 11, tc, z=22)
        P.t(x + 2.2, y + 15.4, lab, "condm", 7.6, tc, z=22)
        P.t(x + wcell - 3.4, y + 3.4, lvl, "monob", 6.5, tc, ha="right", z=22)

# =====================================================================================  01 MAPEADOS
MAPH = 232.0
S_MAP = MAPH / 1180.0  # mm por metro
MX0, MY0 = M, 128
XMIN = PL.X0 + PL.OFFX / PL.PXM
YMAX = CY + 590
def W2P(x, y): return MX0 + (x - XMIN) * S_MAP, MY0 + (YMAX - y) * S_MAP

def bloque01():
    P.header(M, 116, CWID, "01", "MAPEADOS · SIETE CAPAS SOBRE EL MISMO PUNTO", CYAN, "A",
             "Fuente: MAPPEADOS/ (QGIS 3.40, GeoPDF) · inventario OSM 600 m · georreferencia exacta por GPTS")
    # --- mapa completo
    im = Image.open("/home/claude/g3/a1/hi/MAPA_COMPLETO.png").convert("RGB")
    pxm = PL.PXM
    top = (PL.Y0 - YMAX) * pxm; hpx = 1180 * pxm
    im = im.crop((0, int(round(top)), im.size[0], int(round(top + hpx))))
    im = Image.blend(im, Image.new("RGB", im.size, (243, 239, 230)), 0.18)
    wmm = im.size[0] / pxm * S_MAP
    P.img(np.asarray(im), MX0, MY0, wmm, MAPH, z=3)
    P.rect(MX0, MY0, wmm, MAPH, ec=INK, lw=1.0, z=30)
    ax = P.ax
    # anillos
    for r, lab in [(100, "100 m · 1'15\""), (200, "200 m · 2'30\""), (300, "300 m · 3'45\""), (400, "400 m · 5'"), (500, "500 m · 6'15\"")]:
        cx, cy = W2P(CX, CY)
        rr = r * S_MAP
        P.circ(cx, cy, rr, ec=RED, lw=1.1 if r == 400 else 0.55, ls=(0, (4, 2)) if r != 400 else "-", z=12)
        ang = math.radians(-58)
        P.t(cx + rr * math.cos(ang) + 0.6, cy + rr * math.sin(ang), lab, "monob", 6.2, RED, z=40,
            bbox=dict(fc=PAPER, ec="none", pad=0.4))
    # sectores 16
    cx, cy = W2P(CX, CY)
    for s in range(16):
        a = math.radians(s * 22.5 + 11.25)
        P.line([cx + 100 * S_MAP * math.sin(a), cx + 500 * S_MAP * math.sin(a)],
               [cy - 100 * S_MAP * math.cos(a), cy - 500 * S_MAP * math.cos(a)], RED, 0.25, z=11, alpha=0.6)
    # eje de Ribera
    xs, ys = zip(*[W2P(x, y) for x, y in CL.coords])
    P.line(xs, ys, YELLOW, 5.5, z=13, alpha=0.95)
    P.line(xs, ys, INK, 0.5, z=14, ls=(0, (2, 1.5)))
    # estaciones Street View
    for i, e in enumerate(META["estaciones"]):
        x, y = TR.transform(e["lon"], e["lat"]); px_, py_ = W2P(x, y)
        P.circ(px_, py_, 1.35, fc=WHITE, ec=INK, lw=0.5, z=22)
        side = -1 if i % 2 else 1
        P.t(px_ + side * 2.6, py_ + 0.9, f"S{i+1:02d}", "monob", 5.0, INK, ha="left" if side > 0 else "right", z=23)
    # parcela
    pts = [W2P(x, y) for x, y in PARCELA.exterior.coords]
    P.poly(pts, fc=RED, ec=INK, lw=0.6, z=25)
    P.t(cx + 6, cy - 5, "31", "title", 26, RED, z=40, bbox=dict(fc=PAPER, ec=RED, lw=0.8, pad=0.8))
    # metro (bocas) y estaciones nombradas
    D0 = pickle.load(open("/home/claude/g3/a1/osm.pkl", "rb"))
    seen = {}
    for f in D0["feats"]:
        if f["sub"] == "railway=subway_entrance":
            g = WKT.loads(f["wkt"]); x, y = g.x, g.y
            if abs(y - CY) > 585: continue
            px_, py_ = W2P(x, y)
            if px_ > MX0 + wmm - 2: continue
            P.rect(px_ - 1.6, py_ - 1.6, 3.2, 3.2, fc=BLUE, ec=WHITE, lw=0.4, z=26)
            P.t(px_, py_ + 1.05, "M", "monob", 4.6, WHITE, ha="center", z=27)
            nm = f["nom"] or ""
            d = math.hypot(x - CX, y - CY)
            if nm and (nm not in seen or d < seen[nm][0]): seen[nm] = (d, px_, py_)
    for nm, (d, px_, py_) in seen.items():
        P.t(px_ + 2.5, py_ - 2.2, f"{nm.upper()} · {fnum(d)} m", "monob", 5.6, BLUE, z=41, bbox=dict(fc=PAPER, ec="none", pad=0.3))
    # norte y escala
    nx, ny = MX0 + wmm - 12, MY0 + 16
    P.poly([(nx, ny - 9), (nx - 3.2, ny + 2), (nx, ny), (nx + 3.2, ny + 2)], fc=INK, z=40)
    P.t(nx, ny + 7, "N", "title", 16, INK, ha="center", z=40)
    sx, sy = MX0 + 8, MY0 + MAPH - 8
    for i in range(5):
        P.rect(sx + i * 20 * S_MAP * 5 / 5 * 5 / 5, sy, 0, 0)
    for i in range(4):
        P.rect(sx + i * 50 * S_MAP, sy, 50 * S_MAP, 1.8, fc=INK if i % 2 == 0 else WHITE, ec=INK, lw=0.4, z=40)
    for i, v in enumerate([0, 50, 100, 150, 200]):
        P.t(sx + v * S_MAP, sy - 1.2, f"{v}", "monob", 5.5, INK, ha="center", z=40)
    P.t(sx + 200 * S_MAP + 2, sy + 1.8, "m · 1:4.540 en A1", "monob", 5.5, INK, z=40)
    # leyenda del mapa (cartela)
    lx, ly = MX0 + 4, MY0 + 4
    P.rect(lx, ly, 70, 40, fc=PAPER, ec=INK, lw=0.6, z=35)
    P.t(lx + 3, ly + 6, "MAPA COMPLETO + LECTURA", "cond", 10, INK, z=36)
    leg = [(RED, "anillos 100 m · tiempo a 80 m/min en línea recta"), (YELLOW, "eje de Ribera de Curtidores · 658 m"),
           (WHITE, "S01–S23 · estaciones Street View (cada 40/20 m)"), (BLUE, "M · bocas de metro (OSM)"), (RED, "parcela nº 31 (catastro)")]
    for i, (c, s) in enumerate(leg):
        yy = ly + 11 + i * 5.6
        P.rect(lx + 3, yy - 2.6, 5, 3.2, fc=c, ec=INK, lw=0.4, z=36)
        P.t(lx + 10, yy, s, "r", 6.4, INK, z=36)
    return wmm

# ---------------------------------------------------------- 01b axonometría explotada
def bloque01b(wmm):
    x0 = MX0 + wmm + 8; x1 = PW - M
    pw = 186.0; ph = pw * 754 / 1500
    px0 = x1 - pw
    ytop = 128; ybot = 128 + MAPH
    n = 7; d = (ybot - ytop - ph) / (n - 1)
    R = MET["rings"]; sum5 = lambda k: sum(R[k])
    L = MET["longitudes_500"]
    info = [
        ("01", "EDIFICIOS", "#131313", f"{fnum(sum5('edificios'))} polígonos OSM en 500 m · ocupación del círculo {fnum(MET['bld_area_500']/ (math.pi*500**2)*100,1)} %"),
        ("02", "CALLES Y RECORRIDOS", ORANGE, f"{fnum(L['highway=footway']/1000,1)} km de aceras y sendas · {fnum(L['highway=living_street']/1000,1)} km de calles de convivencia · {fnum(L['highway=steps'])} m de escaleras"),
        ("03", "TRANSPORTE", BLUE, f"{MET['subtipos']['transporte'][1][1]} bocas de metro y {MET['subtipos']['transporte'][0][1]} paradas de bus en 500 m · 0 en los primeros 100 m"),
        ("04", "COMERCIO Y ACTIVIDAD", PINK, f"{sum5('comercio')} en 500 m · {dict(MET['subtipos']['comercio'])['shop=vacant']} locales vacíos · {dict(MET['subtipos']['comercio'])['shop=antiques']} anticuarios"),
        ("05", "EQUIPAMIENTOS Y LOCALES", VIOLET, f"{sum5('equipamientos')} en 500 m · {dict(MET['subtipos']['equipamientos'])['amenity=restaurant']} restaurantes, {dict(MET['subtipos']['equipamientos'])['amenity=bar']} bares · colegio a 110 m"),
        ("06", "ESPACIO PÚBLICO Y VERDE", GREEN, f"{sum5('arboles')} árboles · {fnum(MET['verde_m2_500']/10000,2)} ha de parque, jardín y plaza ({fnum(MET['verde_m2_500']/(math.pi*500**2)*100,1)} %)"),
        ("07", "MAPA COMPLETO · TOPOGRAFÍA", CYAN, f"curvas de nivel + mobiliario · {sum5('farolas')} farolas · {sum5('portales')} portales en 500 m"),
    ]
    site = []
    for k in range(n):
        yk = ybot - ph - k * d   # capa 1 abajo
        im = np.asarray(Image.open(f"/home/claude/g3/a1/hi/iso_{k}.png"))
        # lámina: elipse de fondo
        P.ax.add_patch(Ellipse((px0 + pw / 2, yk + ph / 2), pw * 0.995, ph * 0.995, fc=PAPER, ec=info[k][2], lw=0.9, alpha=0.72, zorder=100 + 3 * k))
        P.ax.imshow(im, extent=(px0, px0 + pw, yk + ph, yk), zorder=101 + 3 * k, aspect="auto", interpolation="antialiased", alpha=0.78 if k == 6 else 1)
        cxk, cyk = px0 + pw / 2, yk + ph / 2
        site.append((cxk, cyk))
        P.ax.add_patch(Ellipse((cxk, cyk), 3.4, 1.7, fc=RED, ec=INK, lw=0.4, zorder=102 + 3 * k))
        # etiqueta
        num, name, col, txt = info[k]
        ly = yk + ph / 2 + 1.5
        lx = x0
        P.rect(lx, ly - 6.2, 8, 7, fc=col, z=130); P.t(lx + 4, ly - 1.0, num, "monob", 7, WHITE if col in ("#131313", BLUE, VIOLET) else INK, ha="center", z=131)
        P.t(lx + 10, ly - 1.2, name, "cond", 11, INK, z=131)
        P.para(lx + 10, ly + 0.8, txt, 6.5, "r", DGREY, 44, ls=1.18, z=131)
        # guía hasta la lámina
        ex = px0 + 1.2
        P.line([lx + 10 + textw(name, "cond", 11) + 2, ex], [ly - 4.6, yk + ph / 2], col if col != "#131313" else INK, 0.5, z=129 + 3 * k)
        P.circ(ex, yk + ph / 2, 0.9, fc=col, ec="none", z=129 + 3 * k)
    # eje vertical del 31
    xs = [s[0] for s in site]; ys = [s[1] for s in site]
    P.line(xs, ys, RED, 1.2, z=125)
    P.line([xs[-1], xs[-1]], [ys[-1], ytop + 1], RED, 1.2, z=125)
    P.t(xs[-1] - 2, ytop + 2.5, "EJE DEL Nº 31 · 440.017,8 E / 4.473.229,4 N", "monob", 6, RED, ha="right", z=140, bbox=dict(fc=PAPER, ec="none", pad=0.4))
    P.t(x1, ybot + 1.5, "Láminas: diferencia píxel a píxel entre MAPA 1…6 y COMPLETO (220 ppp), recortadas a r = 560 m y proyectadas en dimétrica (giro −32°, escala vertical 0,5).",
        "i", 6.2, DGREY, ha="right", va="top", z=140)

# =====================================================================================  02 RADIO
THEMES = [("comercio", "comercio", PINK), ("equipamientos", "equipamientos", VIOLET), ("arboles", "árboles", GREEN),
          ("transporte", "transporte", BLUE)]

def bloque02():
    y0 = 368
    P.header(M, y0, CWID, "02", "RADIO · LO QUE HAY A 500 M, EN 16 DIRECCIONES Y 5 ANILLOS", PINK, "A",
             "Fuente: INVENTARIO_FISICO_600M.gpkg (OSM, 8.021 elementos) · centro: centroide de la parcela")
    # ---- rosa de 64 barras
    cx, cy, R0, R1 = M + 56, y0 + 62, 8, 45
    for r in (100, 200, 300, 400, 500):
        pass
    maxv = max(sum(MET["sectores"][k][s]) for k, _, _ in THEMES for s in range(16))
    scale = lambda v: R0 + (R1 - R0) * math.sqrt(v / maxv)
    for rv in (5, 20, 45, 80):
        rr = scale(rv); P.circ(cx, cy, rr, ec=GREY, lw=0.3, z=8, ls=(0, (1, 1)))
        P.t(cx + 0.6, cy - rr - 0.4, str(rv), "mono", 5, DGREY, z=9)
    for s in range(16):
        a0 = s * 22.5 - 11.25
        for j, (k, lab, col) in enumerate(THEMES):
            v = sum(MET["sectores"][k][s])
            aa = a0 + 1.2 + j * 5.0
            # matplotlib Wedge: ángulos antihorarios desde el este; nuestro acimut horario desde el norte, y invertido
            th1 = 90 - (aa + 4.6); th2 = 90 - aa
            w = Wedge((cx, cy), scale(v), -th2, -th1, width=scale(v) - R0, fc=col, ec="none", zorder=12)
            P.ax.add_patch(w)
            if v >= 40:
                am = math.radians(aa + 2.3)
                P.t(cx + (scale(v) + 1.8) * math.sin(am), cy - (scale(v) + 1.8) * math.cos(am), str(v), "monob", 5.2, col,
                    ha="center", va="center", z=20)
    for s, lab in [(0, "N"), (4, "E"), (8, "S"), (12, "O")]:
        a = math.radians(s * 22.5)
        P.t(cx + (R1 + 5) * math.sin(a), cy - (R1 + 5) * math.cos(a), lab, "title", 13, INK, ha="center", va="center")
    P.circ(cx, cy, R0 - 1, fc=RED, ec=INK, lw=0.5, z=15)
    P.t(cx, cy, "31", "title", 12, WHITE, ha="center", va="center", z=16)
    # eje Ribera N-S
    P.line([cx, cx], [cy - R1 - 1, cy + R1 + 1], YELLOW, 1.4, z=11, alpha=0.9)
    P.t(M, y0 + 118, "ROSA · 16 sectores × 4 temas · elementos en 0–500 m · radio = raíz de n", "monob", 5.8, INK)
    for j, (k, lab, col) in enumerate(THEMES):
        P.rect(M + j * 27, y0 + 120.5, 3.4, 3.4, fc=col); P.t(M + 4.5 + j * 27, y0 + 123.3, lab, "r", 6.6)
    # ---- matriz de densidad por anillo
    hx, hy = M + 124, y0 + 18
    rows = [("comercio", "comercio", PINK), ("equipamientos", "equipamientos", VIOLET), ("arboles", "árboles", GREEN),
            ("bancos", "bancos", GREEN), ("transporte", "paradas / bocas", BLUE), ("portales", "portales", ORANGE),
            ("farolas", "farolas", YELLOW), ("patrimonio", "patrimonio", RED), ("barreras", "barreras", DGREY),
            ("edificios", "edificios", INK)]
    rings = [0, 100, 200, 300, 400, 500]
    areas = [math.pi * (rings[i + 1] ** 2 - rings[i] ** 2) / 10000 for i in range(5)]
    cw, ch = 19.5, 8.6
    P.t(hx, hy - 2, "DENSIDAD · elementos por hectárea en cada anillo", "monob", 5.8, INK)
    for i in range(5):
        P.t(hx + 30 + i * cw + cw / 2, hy + 3, f"{rings[i]}–{rings[i+1]}", "monob", 5.6, INK, ha="center")
    for r_, (k, lab, col) in enumerate(rows):
        vals = [MET["rings"][k][i] / areas[i] for i in range(5)]
        mx = max(vals) or 1
        yy = hy + 5 + r_ * ch
        P.t(hx, yy + ch * 0.62, lab, "cond", 8.5, INK)
        P.t(hx + 29, yy + ch * 0.62, str(sum(MET["rings"][k])), "monob", 5.6, DGREY, ha="right")
        for i, v in enumerate(vals):
            a = 0.08 + 0.92 * (v / mx)
            P.rect(hx + 30 + i * cw, yy, cw - 0.8, ch - 0.8, fc=col, alpha=a, z=6)
            tc = WHITE if a > 0.55 and col not in (YELLOW,) else INK
            P.t(hx + 30 + i * cw + cw / 2, yy + ch * 0.62, fnum(v, 1), "monob", 6.2, tc, ha="center", z=7)
            if v == mx:
                P.rect(hx + 30 + i * cw, yy, cw - 0.8, ch - 0.8, ec=INK, lw=1.0, z=8)
    P.t(hx, hy + 5 + 10 * ch + 3.5, "Recuadro = anillo de máxima densidad de cada fila. Tono relativo a la fila.", "i", 6.2, DGREY)
    # ---- escalera de distancias
    lx0, lx1 = M + 262, PW - M - 4
    ly = y0 + 22
    near = MET["nearest"]
    keys = [("alimentación", "alimentación", PINK), ("árbol", "árbol", GREEN), ("banco", "banco", GREEN), ("bar/café", "bar / café", VIOLET),
            ("colegio", "colegio CEIP Emilia Pardo Bazán", VIOLET), ("deporte", "pista deportiva", GREEN), ("farmacia", "farmacia", VIOLET),
            ("supermercado", "supermercado", PINK), ("juegos infantiles", "juegos infantiles", GREEN), ("fuente de beber", "fuente de beber", CYAN),
            ("bus", "parada bus · El Rastro", BLUE), ("universidad", "Univ. Carlos III · Pta. de Toledo", VIOLET), ("plaza", "plaza General Vara del Rey", GREEN),
            ("bici pública", "BiciMAD", BLUE), ("mercado", "mercado de San Fernando", PINK), ("salud", "centro de salud Lavapiés", VIOLET),
            ("metro (boca)", "metro · Puerta de Toledo (L5)", BLUE)]
    dmax = 400.0
    sx = lambda d: lx0 + 58 + (lx1 - lx0 - 58) * d / dmax
    P.t(lx0, y0 + 16, "A CUÁNTO ESTÁ · distancia en línea recta desde el centroide de la parcela", "monob", 5.8, INK)
    for m_ in range(0, 401, 50):
        P.line([sx(m_), sx(m_)], [ly, ly + 17 * 5.0 + 1], GREY, 0.3, z=4, ls=(0, (1, 1.2)) if m_ % 100 else "-")
        P.t(sx(m_), ly + 17 * 5.0 + 4.2, f"{m_}", "monob", 5.4, INK, ha="center")
        if m_ % 100 == 0:
            P.t(sx(m_), ly + 17 * 5.0 + 7.6, f"{m_/80:.2f}".replace(".", ",") + " min", "mono", 5, DGREY, ha="center")
    P.rect(sx(0), ly - 1, sx(400) - sx(0), 17 * 5.0 + 2, fc="none", ec=INK, lw=0.4)
    P.rect(sx(0), ly - 1, sx(100) - sx(0), 17 * 5.0 + 2, fc=RED, alpha=0.07, z=2)
    for i, (k, lab, col) in enumerate(keys):
        d = near[k]["d"]; yy = ly + 2 + i * 5.0
        P.t(lx0 + 56, yy + 1.1, lab, "condm", 7.4, INK, ha="right")
        P.line([sx(0), sx(d)], [yy, yy], col, 2.2, z=10)
        P.circ(sx(d), yy, 1.3, fc=col, ec=INK, lw=0.4, z=11)
        P.t(sx(d) + 2.2, yy + 1.0, f"{fnum(d,0)} m", "monob", 5.8, INK, z=12)
    P.t(lx0, ly + 17 * 5.0 + 12, "Minutos a 80 m/min sin rodeos: cota inferior del tiempo real. Todo lo cotidiano cae dentro de 5 minutos; el metro, fuera.",
        "i", 6.3, DGREY)

# =====================================================================================  03 CALLE DESPLEGADA
SS = 565.0 / 580.0    # mm por metro de eje
def bloque03():
    y0 = 496
    P.header(M, y0, CWID, "03", "LA CALLE DESPLEGADA · 580 M DE RIBERA, AMBAS ACERAS ABATIDAS", YELLOW, "A/B",
             "Alzados rectificados de 23 panorámicas (Street View 2021-22) sobre planos de fachada del catastro")
    X = lambda s: M + s * SS
    hs = 36.5 * SS   # altura de banda de foto (36,5 m)
    yW = y0 + 13; yAxisTop = yW + hs + 26; yAxisBot = yAxisTop + 12; yE = yAxisBot + 26
    # fotos
    for side, yy, flip in (("W", yW, False), ("E", yE, True)):
        for a in (0, 160, 320, 480):
            im = Image.open(f"/home/claude/g3/fig/strips/continuo_{side}_{a}_{a+160}.jpg")
            s1 = min(a + 160, 580)
            if s1 < a + 160:
                im = im.crop((0, 0, int(im.size[0] * (s1 - a) / 160), im.size[1]))
            if flip: im = ImageOps.flip(im)
            P.img(np.asarray(im), X(a), yy, (s1 - a) * SS, hs, z=3)
        P.rect(X(0), yy, 580 * SS, hs, ec=INK, lw=0.6, z=6)
    # rótulos de acera
    P.t(X(0) + 1.5, yW + 4, "ACERA OESTE · PARES · abatida hacia arriba", "cond", 9, WHITE, z=30, bbox=dict(fc=INK, ec="none", pad=0.8))
    P.t(X(0) + 1.5, yE + hs - 2, "ACERA ESTE · IMPARES · abatida hacia abajo (lectura invertida)", "cond", 9, WHITE, z=30, bbox=dict(fc=INK, ec="none", pad=0.8))
    # códigos de fachada y año
    def epoch(y):
        return RED if y < 1900 else (ORANGE if y < 1960 else (CYAN if y < 2000 else VIOLET))
    for f in FAC:
        s0, s1 = f["s0"], min(f["s1"], 580)
        if s0 > 580: continue
        if f["side"] == "W":
            ytab = yW - 0.2; P.rect(X(s0) + 0.15, yW + hs, (s1 - s0) * SS - 0.3, 2.2, fc=epoch(f["anio"]), z=8)
            P.t((X(s0) + X(s1)) / 2, yW + hs + 1.75, f"{cod(f['codigo'])}·{f['anio']}", "monob", 3.9, INK if epoch(f['anio']) in (CYAN, ORANGE) else WHITE, ha="center", z=9)
        else:
            P.rect(X(s0) + 0.15, yE - 2.2, (s1 - s0) * SS - 0.3, 2.2, fc=epoch(f["anio"]), z=8)
            P.t((X(s0) + X(s1)) / 2, yE - 0.45, f"{cod(f['codigo'])}·{f['anio']}", "monob", 3.9, INK if epoch(f['anio']) in (CYAN, ORANGE) else WHITE, ha="center", z=9)
    # código de barras de rasgos
    rasgos = [("pb_com", "PB comercial", PINK), ("cierre", "cierre enrollable", RED), ("grafiti", "grafiti", ORANGE),
              ("zocalo", "zócalo", DGREY), ("balcon", "balcón propio", GREEN), ("recercado", "recercado", BLUE),
              ("toldo_alto", "textil alto", YELLOW), ("vegetal", "plantas", GREEN), ("alero", "alero / cornisa", VIOLET),
              ("instal", "instalaciones", CYAN), ("expo", "exposición en acera", PINK)]
    rh = 2.0
    def val(c, k):
        v = COD[c].get(k)
        if k == "balcon":
            return None if v is None else (1 if v in ("ind", "mixto") else 0)
        return v
    for side in "WE":
        for j, (k, lab, col) in enumerate(rasgos):
            if side == "W": yy = yW + hs + 2.6 + j * rh
            else: yy = yE - 2.6 - (j + 1) * rh
            for f in FAC:
                if f["side"] != side or f["s0"] > 580: continue
                v = val(f["codigo"], k); s0, s1 = f["s0"], min(f["s1"], 580)
                if v == 1: P.rect(X(s0) + 0.15, yy + 0.15, (s1 - s0) * SS - 0.3, rh - 0.3, fc=col, z=8)
                elif v == 0: P.rect(X(s0) + 0.15, yy + 0.15, (s1 - s0) * SS - 0.3, rh - 0.3, fc=LGREY, z=8)
                else: P.rect(X(s0) + 0.15, yy + 0.15, (s1 - s0) * SS - 0.3, rh - 0.3, fc="none", ec=GREY, lw=0.2, hatch="/////", z=8)
    # leyenda de rasgos a la derecha del eje? -> en el hueco sobre el eje, lado derecho (s 540–580 sin fachadas W)
    lx = X(535)
    for j, (k, lab, col) in enumerate(rasgos):
        yy = yW + hs + 2.6 + j * rh
        P.t(lx, yy + rh * 0.8, lab, "condm", 5.6, INK, z=12)
    for j, (k, lab, col) in enumerate(rasgos):
        yy = yE - 2.6 - (j + 1) * rh
        P.t(lx, yy + rh * 0.8, lab, "condm", 5.6, INK, z=12)
    # eje con cadenamiento
    P.rect(X(0), yAxisTop, 580 * SS, yAxisBot - yAxisTop, fc=INK, z=10)
    for s in range(0, 581, 20):
        big = s % 100 == 0
        P.line([X(s), X(s)], [yAxisTop, yAxisTop + (3 if big else 1.5)], WHITE, 0.5, z=11)
        if big: P.t(X(s) + 0.6, yAxisTop + 3.1, f"{s} m", "monob", 5.4, WHITE, z=12, va="center")
    for i, e in enumerate(META["estaciones"]):
        if e["s_m"] > 580: continue
        P.rect(X(e["s_m"]) - 0.35, yAxisBot - 4.6, 0.7, 4.6, fc=YELLOW, z=12)
        P.t(X(e["s_m"]), yAxisBot - 5.1, f"S{i+1:02d}", "monob", 4.3, YELLOW, ha="center", z=12)
    # perfil de cota (dentro del eje)
    al = MN["alt_perfil"]
    zs = [a[1] for a in al]; zmin, zmax = 611, 650
    xs = [X(a[0]) for a in al if a[0] <= 580]; ys = [yAxisTop + 5.5 + (zmax - a[1]) / (zmax - zmin) * 0 for a in al if a[0] <= 580]
    P.t(X(2), yAxisBot - 1.2, "CASCORRO · 649,5 m", "monob", 5.2, CYAN, z=13)
    P.t(X(578), yAxisBot - 1.2, "RONDA DE TOLEDO · 612,5 m", "monob", 5.2, CYAN, ha="right", z=13)
    # el 31
    P.rect(X(S31a), yE - 30, (S31b - S31a) * SS, yE + hs - (yE - 30), fc="none", ec=RED, lw=1.6, z=20)
    P.rect(X(S31a), yAxisTop, (S31b - S31a) * SS, yAxisBot - yAxisTop, fc=RED, z=14)
    P.t((X(S31a) + X(S31b)) / 2, yAxisTop + 8.7, "31", "title", 13, WHITE, ha="center", z=15)
    P.t(X(S31b) + 1.5, yE + hs - 3, "Nº 31 · solar: la nave comercial (2008–2022) no está en catastro", "cond", 8, RED, z=30,
        bbox=dict(fc=PAPER, ec="none", pad=0.5))
    # leyenda épocas
    ex = X(0); ey = yE + hs + 5.2
    P.t(ex, ey, "AÑO CATASTRAL DEL FRENTE", "monob", 5.8, INK)
    for i, (c, s) in enumerate([(RED, "antes de 1900 · 15"), (ORANGE, "1900–1959 · 10"), (CYAN, "1960–1999 · 13"), (VIOLET, "2000 o después · 6")]):
        P.rect(ex + 42 + i * 34, ey - 2.6, 4, 3, fc=c); P.t(ex + 47 + i * 34, ey, s, "r", 6.5)
    P.t(ex + 185, ey, "RASGOS · color = presente · gris = ausente · rayado = no legible (árbol, obra, recorte). Frentes = 44 (catastro); legibles = 42.",
        "r", 6.5, INK)
    P.t(PW - M, ey, "Escala horizontal y vertical iguales · 1:1.030 en A1", "monob", 5.8, DGREY, ha="right")
    return ey

# =====================================================================================  04 PATRONES
def bloque04(ystart):
    y0 = ystart + 5
    P.header(M, y0, CWID, "04", "PATRONES · ONCE RESPUESTAS QUE LA CALLE YA DA", GREEN, "A/B",
             "Regla: patrón = 8 o más casos independientes · nivel B lectura visual · nivel A catastro")
    cols = 11; gap = 3.4; w = (CWID - gap * (cols - 1)) / cols
    pals = [GREEN, RED, DGREY, BLUE, YELLOW, GREEN, VIOLET, CYAN, PINK, ORANGE, RED]
    fields = {"P01": ("balcon", "ind"), "P02": ("cierre", 1), "P03": ("zocalo", 1), "P04": ("recercado", 1), "P05": ("toldo_alto", 1),
              "P06": ("vegetal", 1), "P07": ("alero", 1), "P08": ("instal", 1), "P09": ("expo", 1)}
    # P10 / P11
    extra = [dict(id="P10", nombre="Salto de altura entre vecinos", pregunta="¿Hay una cornisa que continuar?", n=9, N=28),
             dict(id="P11", nombre="Sustitución parcela a parcela", pregunta="¿De cuándo es lo construido?", n=19, N=44)]
    allp = PAT + extra
    photo_h = 24
    for i, p in enumerate(allp):
        x = M + i * (w + gap); y = y0 + 14
        col = pals[i]
        P.rect(x, y, w, 7.5, fc=col, z=10)
        P.t(x + 1.5, y + 6.2, p["id"], "title", 17, WHITE if col in (RED, BLUE, VIOLET, DGREY, GREEN) else INK, z=11)
        pct = round(100 * p["n"] / p["N"])
        P.t(x + w - 1.2, y + 6.2, f"{pct}%", "title", 17, WHITE if col in (RED, BLUE, VIOLET, DGREY, GREEN) else INK, ha="right", z=11)
        P.para(x, y + 9, p["nombre"], 8.2, "cond", INK, 24, ls=1.05)
        # imagen o diagrama
        yi = y + 18
        if p["id"] in fields:
            cs = p["casos"][0]
            im = Image.open(f"/home/claude/g3/fig/panel/{p['id']}_{cs}_fit.jpg").convert("RGB")
            W_, H_ = im.size; tgt = w / photo_h
            nh = int(W_ / tgt); top = max(0, (H_ - nh) // 2)
            im = im.crop((0, top, W_, top + nh))
            P.img(np.asarray(im), x, yi, w, photo_h, z=5)
            P.t(x + 1, yi + photo_h - 1.2, cod(cs), "monob", 5.5, WHITE, z=12, bbox=dict(fc=INK, ec="none", pad=0.3))
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
                    P.line([xx, xx], [yi + photo_h - 2 - h1 * 1.9, yi + photo_h - 2 - h2 * 1.9], RED, 1.6, z=8)
            P.t(x + 1.2, yi + 3.5, "acera O · 0–420 m · plantas de frente", "monob", 4.6, WHITE, z=9)
        else:  # P11
            P.rect(x, yi, w, photo_h, fc=INK, z=4)
            ys_ = sorted(f["anio"] for f in FR)
            a0, a1 = 1840, 2025
            for yr in ys_:
                pass
            bins = {}
            for yr in ys_:
                b = (yr // 10) * 10; bins[b] = bins.get(b, 0) + 1
            for b, n in bins.items():
                xx = x + 1 + (b - a0) / (a1 - a0) * (w - 2)
                for k in range(n):
                    P.rect(xx, yi + photo_h - 4 - (k + 1) * 1.9, (w - 2) / 18.5 - 0.2, 1.7, fc=RED if b < 1960 else YELLOW, z=6)
            for yr in (1850, 1900, 1950, 2000):
                xx = x + 1 + (yr - a0) / (a1 - a0) * (w - 2)
                P.t(xx, yi + photo_h - 1, str(yr), "monob", 4.2, WHITE, ha="center", z=7)
            P.t(x + 1.2, yi + 3.5, "44 frentes por década", "monob", 4.6, WHITE, z=9)
        # waffle n/N
        yw = yi + photo_h + 2.2
        per = 13; cell = w / per
        for k in range(p["N"]):
            r, c = divmod(k, per)
            P.rect(x + c * cell + 0.2, yw + r * 2.4, cell - 0.4, 2.0, fc=col if k < p["n"] else LGREY, z=6)
        rows_ = 4
        yq = yw + rows_ * 2.4 + 0.6
        P.t(x, yq + 2.5, f"{p['n']} / {p['N']}", "monob", 6.4, INK)
        P.t(x + w, yq + 2.5, "A" if p["id"] in ("P10", "P11") else "B", "monob", 6.4, LEVEL["A" if p["id"] in ("P10", "P11") else "B"], ha="right")
        P.para(x, yq + 3.8, p["pregunta"], 6.6, "i", DGREY, 27, ls=1.12)
        # micro-calle: dónde aparece
        ym = yq + 11.5
        P.line([x, x + w], [ym, ym], INK, 0.4)
        if p["id"] in fields:
            k, v = fields[p["id"]]
            for f in FAC:
                if f["s0"] > 580: continue
                vv = COD[f["codigo"]].get(k)
                ok = (vv == v) or (k == "balcon" and vv in ("ind",) and v == "ind")
                if ok:
                    xx = x + f["s0"] / 580 * w; ww = max(0.5, (min(f["s1"], 580) - f["s0"]) / 580 * w)
                    P.rect(xx, ym - 1.6 if f["side"] == "W" else ym + 0.2, ww, 1.4, fc=col, z=7)
        elif p["id"] == "P10":
            for (sd, sj, dj, h1, h2) in JUMPS:
                if dj >= 2:
                    xx = x + sj / 580 * w
                    P.rect(xx - 0.35, ym - 1.6 if sd == "W" else ym + 0.2, 0.7, 1.4, fc=col, z=7)
        else:
            for f in FR:
                if f["anio"] >= 1960 and f["s0"] <= 580:
                    xx = x + f["s0"] / 580 * w; ww = max(0.5, (min(f["s1"], 580) - f["s0"]) / 580 * w)
                    P.rect(xx, ym - 1.6 if f["side"] == "W" else ym + 0.2, ww, 1.4, fc=col, z=7)
        xs31 = x + S31a / 580 * w
        P.line([xs31, xs31], [ym - 2.2, ym + 2.2], RED, 0.8, z=8)
    P.t(M, ym + 5.5, "Micro-calle bajo cada patrón: posición de los casos a lo largo de los 580 m (arriba acera O, abajo acera E); trazo rojo = nº 31.",
        "i", 6.3, DGREY)
    return ym + 7

# =====================================================================================  05 SOL · TIEMPO · CRITERIOS
def bloque05(ystart):
    y0 = ystart + 3
    P.header(M, y0, CWID, "05", "SOL · TIEMPO · CRITERIOS", ORANGE, "B/C",
             "Modelo 2,5D propio: PB 4,0 m + 3,1 m/planta (B) · paso 15 min · celdas 1 m · NOAA")
    yb = y0 + 14; ybot = PH - 14 - 10
    hb = ybot - yb
    # ---------- 5a sol por altura
    x = M; w = 150
    P.t(x, yb + 3, "HORAS DE SOL SOBRE LA PARCELA SEGÚN LA COTA", "cond", 10)
    cotas = ["0", "4", "7.1", "10.2", "13.3", "16.4", "19.5", "22.6", "25.7"]
    labs = ["suelo", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8 · cub."]
    dates = [("2026-12-21", "21 dic", BLUE), ("2026-03-21", "21 mar", ORANGE), ("2026-06-21", "21 jun", YELLOW)]
    gx = x + 17; gw = 84; gy = yb + 8; gh = hb - 14
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
    # umbral 50 % en invierno: interpolación lineal entre 19,5 m (33,4 %) y 22,6 m (65,2 %)
    p1, p2 = SOL["2026-12-21"]["19.5"]["pct_2h"], SOL["2026-12-21"]["22.6"]["pct_2h"]
    z50 = 19.5 + (50 - p1) / (p2 - p1) * 3.1
    zpos = lambda z: gy + gh - rowh * (0.5 + np.interp(z, [0, 4, 7.1, 10.2, 13.3, 16.4, 19.5, 22.6, 25.7], range(9)))
    yz = zpos(z50)
    P.line([gx - 16, gx + gw + 46], [yz, yz], RED, 1.0, z=12, ls=(0, (3, 1.5)))
    P.line([gx - 16, gx - 8], [ybot + 2.2, ybot + 2.2], RED, 1.0, ls=(0, (3, 1.5)))
    P.t(gx - 6, ybot + 3.2, f"cota a la que el 50 % del solar recibe 2 h de sol el 21-dic: {fnum(z50,1)} m (interpolación lineal entre P6 y P7)", "cond", 7.2, RED)
    for j, (dk, dl, col) in enumerate(dates):
        P.rect(gx + 82 + j * 16, yb + 0.6, 3.4, 3, fc=col, ec=INK, lw=0.2); P.t(gx + 86.5 + j * 16, yb + 3, dl, "monob", 5.6)
    # ---------- 5b mapas de sombra + sección
    x2 = M + w + 6; w2 = 190
    P.t(x2, yb + 3, "SUELO DEL SOLAR · HORAS DE SOL", "cond", 10)
    X_, Y_ = SOMB["X"], SOMB["Y"]
    from matplotlib.path import Path as MP
    pp = MP(np.array(PARCELA.exterior.coords))
    inside = pp.contains_points(np.c_[X_.ravel(), Y_.ravel()]).reshape(X_.shape)
    bx0, by0, bx1, by1 = PARCELA.bounds
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("sol", ["#1A1A40", BLUE, CYAN, YELLOW, "#FFF6B0"])
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
        P.img(rgba, xx, yy, mw, mh, z=6, interp="nearest")
        P.rect(xx, yy, mw, mh, ec=INK, lw=0.3, z=7)
        P.t(xx, yy + mh + 3.2, f"{dl} · media {fnum(summ[dk]['media_parcela_h'],2)} h", "monob", 5.4, INK)
    bx_ = x2 + 3 * (mw + 4)
    for k in range(12):
        P.rect(bx_, yb + 6 + mh - (k + 1) * mh / 12, 3, mh / 12, fc=cmap(k / 11), z=6)
    P.t(bx_ + 4, yb + 6 + mh, "0 h", "monob", 5); P.t(bx_ + 4, yb + 8, "12 h", "monob", 5)
    P.para(bx_ + 12, yb + 5, "N arriba; calle a la izquierda, fondo de parcela a la derecha. 21-dic: 0 % del solar con 4 h de sol; 2,9 % con 2 h.",
           6, "i", DGREY, 21, ls=1.15)
    # sección N–S por el frente
    sy0 = ybot - 3; ssc = 0.78
    ys_ = lambda z: sy0 - z * ssc
    xs_ = lambda s: x2 + 12 + s * ssc
    P.t(xs_(14.93 + 36), ys_(25.7) - 2.5, "SECCIÓN N–S POR EL FRENTE · rayo a mediodía solar", "cond", 9)
    P.line([xs_(-12), xs_(14.93 + 20)], [ys_(0), ys_(0)], INK, 1.0)
    P.rect(xs_(-12), ys_(4 + 2 * 3.1), 12 * ssc, (4 + 2 * 3.1) * ssc, fc=GREY, ec=INK, lw=0.4, z=6)
    P.t(xs_(-6), ys_(4 + 2 * 3.1) - 1, "N · 3 pl.", "monob", 4.8, INK, ha="center")
    P.rect(xs_(0), ys_(0) - 1.0, 14.93 * ssc, 1.0, fc=RED, z=7)
    P.t(xs_(7.46), ys_(0) + 3.0, "31 · 14,93 m", "monob", 5.2, RED, ha="center")
    Hs = 25.7
    P.rect(xs_(14.93), ys_(Hs), 12 * ssc, Hs * ssc, fc=GREY, ec=INK, lw=0.4, z=6)
    P.t(xs_(14.93 + 13) + 1, ys_(Hs) + 2, "S · 8 pl.\n25,7 m (B)", "monob", 4.8, INK, va="top")
    tx = xs_(14.93 + 36)
    for i, (alt, dl, col) in enumerate([(26.15, "21 dic · 26,2°", BLUE), (49.59, "21 mar · 49,6°", ORANGE), (73.03, "21 jun · 73,0°", "#C9A400")]):
        t_ = math.tan(math.radians(alt))
        z0 = Hs - 14.93 * t_
        xa, ya = xs_(14.93), ys_(Hs)
        if z0 >= 0: xb, yb_ = xs_(0), ys_(z0)
        else:
            d = Hs / t_; xb, yb_ = xs_(14.93 - d), ys_(0)
        L = 7.0; ca = math.cos(math.radians(alt)); sa = math.sin(math.radians(alt))
        P.line([xa + L * ca, xb], [ya - L * sa, yb_], col, 1.0, z=9)
        P.t(tx, ys_(Hs) + 2 + i * 4.2, dl + (f" · sol en el frente desde {fnum(z0,1)} m" if z0 > 0 else " · sol hasta el suelo"),
            "monob", 5.0, col, z=9)
        if z0 > 0:
            P.line([xs_(0), xs_(0)], [ys_(0), ys_(z0)], col, 2.4, z=8, alpha=0.9)
    P.para(tx, ys_(Hs) + 15, "Geometría pura (A) sobre alturas por plantas (B): al mediodía del 21-dic el vecino sur deja en sombra el frente hasta 18,4 m.",
           6.2, "i", INK, 52, ls=1.15)
    # ---------- 5c tiempo + criterios
    x3 = x2 + w2 + 6; w3 = PW - M - x3
    P.t(x3, yb + 3, "EL SOLAR EN EL TIEMPO · Street View 2008–2022", "cond", 10)
    fechas = [("2008-8", "2008 · chimeneas y hogar"), ("2013-10", "2013 · liquidación"), ("2018-8", "2018 · Fang Decoración"), ("2021-7", "2021 · nave tras el atrio")]
    tw = (w3 - 3 * 2.5) / 4; th = 15.5
    for i, (fk, lab) in enumerate(fechas):
        im = Image.open(f"/home/claude/g3/vistas/hist/{fk}.jpg").convert("RGB")
        W_, H_ = im.size
        nh = int(W_ * th / tw); tp = max(0, (H_ - nh) // 2)
        im = im.crop((0, tp, W_, tp + nh))
        xx = x3 + i * (tw + 2.5)
        P.img(np.asarray(im), xx, yb + 5.5, tw, th, z=5)
        P.rect(xx, yb + 5.5, tw, th, ec=INK, lw=0.4, z=6)
        P.t(xx, yb + 5.5 + th + 3.0, lab, "monob", 5.0, INK)
    ny0 = yb + 5.5 + th + 8.5
    P.t(x3, ny0, "DE LA EVIDENCIA AL CRITERIO · hallazgos > patrones > criterios v1 (C)", "cond", 9.5)
    H = ["H-01 el solar no está vacío", "H-02 el sol de invierno solo llega arriba", "H-03 entre 3 y 10 plantas", "H-04 hueco con balcón propio",
         "H-05 planta baja que se cierra", "H-06 tienda en la acera", "H-07 la calle desciende", "H-08 denso y sin estancia"]
    Pp = ["P01", "P02", "P05", "P08", "P09", "P10", "P11"]
    Cc = ["C1 volumen por sol", "C2 PB de dos estados", "C3 umbral en pendiente", "C4 comunes arriba", "C5 balcón + textil",
          "C6 fondo de corrala", "C7 segunda trama"]
    ny = ny0 + 2.0; nh = ybot - ny
    hx = x3; hw = 50; px_ = x3 + 92; cx_ = PW - M - 36
    Hy = {h[:4]: ny + (i + 0.5) * nh / len(H) for i, h in enumerate(H)}
    Py = {p: ny + (i + 0.5) * nh / len(Pp) for i, p in enumerate(Pp)}
    Cy = {c[:2]: ny + (i + 0.5) * nh / len(Cc) for i, c in enumerate(Cc)}
    for h in H:
        P.t(hx, Hy[h[:4]] + 1, h, "condm", 6.6, INK)
    pcol = dict(zip([p["id"] for p in PAT] + ["P10", "P11"], [GREEN, RED, DGREY, BLUE, YELLOW, GREEN, VIOLET, CYAN, PINK, ORANGE, RED]))
    for p in Pp:
        P.rect(px_ - 5, Py[p] - 2.0, 10, 3.4, fc=pcol[p], z=20)
        P.t(px_, Py[p] + 0.55, p, "monob", 5.4, WHITE if pcol[p] in (RED, BLUE, VIOLET, DGREY, GREEN) else INK, ha="center", z=21)
    for c in Cc:
        P.rect(cx_ - 1.5, Cy[c[:2]] - 2.1, 37.5, 3.5, fc=ORANGE, z=20); P.t(cx_ + 0.3, Cy[c[:2]] + 0.55, c, "condm", 6.4, INK, z=21)
    HP = [("H-04", "P01"), ("H-05", "P02"), ("H-06", "P09"), ("H-03", "P10"), ("H-01", "P11")]
    PC = [("P01", "C5"), ("P05", "C5"), ("P02", "C2"), ("P08", "C7"), ("P10", "C1"), ("P11", "C1"), ("P11", "C6")]
    HC = [("H-02", "C1"), ("H-07", "C3"), ("H-08", "C4"), ("H-05", "C2"), ("H-01", "C6")]
    for a, b in HP: P.curve((hx + hw, Hy[a]), (px_ - 5, Py[b]), pcol[b], 1.1, z=12)
    for a, b in PC: P.curve((px_ + 5, Py[a]), (cx_ - 1.5, Cy[b]), pcol[a], 1.1, z=12)
    for a, b in HC: P.curve((hx + hw, Hy[a]), (cx_ - 1.5, Cy[b]), INK, 0.6, z=11, alpha=0.75)

# =====================================================================================  PIE
def pie():
    y = PH - 9
    P.line([M, PW - M], [y - 4.5, y - 4.5], INK, 0.8)
    P.t(M, y, "FUENTES · Catastro INSPIRE WFS + OVC (consulta 23-09-2026) · MAPPEADOS/ e INVENTARIO_FISICO_600M.gpkg (OpenStreetMap vía QGIS, 21/22-09-2026) · "
        "Google Street View 2008–2022 (23 estaciones + 11 fechas del nº 31) · modelo de sombras y alzados rectificados propios (scripts en 00_INVESTIGACION_COMPLETA/SCRIPTS).",
        "r", 6.4, INK)
    P.t(PW - M, y, "RIBERA 31 · PANEL A1 · v1", "monob", 6.4, RED, ha="right")
    P.t(M, y + 3.6, "Las distancias son en línea recta; los recuentos OSM dependen de la completitud del mapa (A = lo que el inventario contiene). Alturas por plantas catastrales con hipótesis PB 4,0 m + 3,1 m (B).",
        "i", 6.0, DGREY)

if __name__ == "__main__":
    cabecera(); cifras()
    wmm = bloque01(); bloque01b(wmm)
    bloque02()
    ey = bloque03()
    y4 = bloque04(ey)
    bloque05(y4)
    pie()
    out = "/home/claude/g3/a1/RIBERA31_PANEL_A1"
    P.save(out + ".pdf", out + "_preview.png", dpi=50)
    print("ok", ey, y4)
