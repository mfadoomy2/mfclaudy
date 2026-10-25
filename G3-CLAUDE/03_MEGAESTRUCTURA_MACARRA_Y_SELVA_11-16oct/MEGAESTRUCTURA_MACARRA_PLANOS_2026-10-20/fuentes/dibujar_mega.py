# -*- coding: utf-8 -*-
# Megaestructura macarra · plantas técnicas 1:200 desde la extracción de Rhino (cortes, contornos, piezas, ejes y recorridos).
import json, math, re, collections, html
from pathlib import Path
from shapely.geometry import Polygon, LineString, Point, MultiPolygon, box
from shapely.ops import unary_union
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

P = Path('/home/claude/mega'); OUT = P / 'planos'; OUT.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('Ibarra', '/home/claude/giro/IbarraRealNova-Italic-400.ttf'))
E = json.load(open('/mnt/user-data/uploads/T7/G3_RHINO/out/mega/EXTRACCION_MEGA_PLANTAS.json'))
V = json.load(open('/mnt/user-data/uploads/T7/G3_RHINO/out/mega/verificacion.json'))
SP = V['spaces']; LK = V['links']
K = 5.0   # 1:200 · 5 mm de papel por metro

def clean(g): return g if g.is_valid else g.buffer(0)
def polys(g): return [g] if g.geom_type == 'Polygon' else [p for p in getattr(g, 'geoms', []) if p.geom_type == 'Polygon']
def num(v, d=2): return f'{v:.{d}f}'.replace('.', ',')
def cota(z): return ('+' if z >= 0 else '−') + num(abs(z))
def title(s): return s[:1] + s[1:].lower()

# ------------------------------------------------------------------ datos medidos
DECK = {}; DECKZ = {}
for d in E['decks']:
    ring = max(d['polys'], key=len); DECK[d['i']] = clean(Polygon(ring)); DECKZ[d['i']] = (d['bottom'], d['top'])
CUTS = collections.defaultdict(list)
for c in E['cuts']: CUTS[c['i']].append(c)
TCUT = collections.defaultdict(list)
for c in E['trunk_cuts']: TCUT[c['i']].append(c)
PIECES = collections.defaultdict(list)
for p in E['pieces']: PIECES[p['layer']].append(p)
OUTL = collections.defaultdict(list)
for o in E['outlines']: OUTL[o['layer']].append(o)
CURV = collections.defaultdict(list)
for c in E['curves']: CURV[c['layer']].append(c)
ROUTE = {c['name']: c['pts'] for c in CURV['91_RECORRIDO_CONTINUO']}

def est_of(name):
    m = re.match(r'E(\d\d)_', name); return int(m.group(1)) if m else None
def link_of(name):
    m = re.match(r'R(\d\d)_', name); return int(m.group(1)) if m else None

# troncos: eje del tronco = curva de 40 puntos cuyo arranque coincide con el centro del haz de nervios
TRUNK = {}
for c in CURV['90_EJES_EDITABLES']:
    if c['name'].startswith('T'):
        TRUNK.setdefault(c['name'][:3], []).append(c['pts'])
TR = {}
for t, cs in sorted(TRUNK.items()):
    c40 = [c for c in cs if len(c) == 40]
    cx = sum(c[0][0] for c in c40) / len(c40); cy = sum(c[0][1] for c in c40) / len(c40)
    main = min(c40, key=lambda c: math.hypot(c[0][0] - cx, c[0][1] - cy))
    branches = [c for c in cs if len(c) == 22]
    TR[t] = {'axis': main, 'root': main[0], 'top': main[-1], 'branches': branches}
# estancias servidas por cada tronco: estancia a la que llega cada rama
for t, d in TR.items():
    d['serves'] = sorted(set(min(range(len(SP)), key=lambda i: math.dist(b[-1][:2], SP[i]['c'][:2]) + abs(b[-1][2] - (SP[i]['c'][2] - .8))) for b in d['branches']))

# malla de troncos: ejes por las raíces
roots = sorted(TR.items(), key=lambda kv: kv[1]['root'][0])
GX = [(str(j + 1), d['root'][0], t) for j, (t, d) in enumerate(roots)]
rootsy = sorted(TR.items(), key=lambda kv: kv[1]['root'][1])
GY = [('ABCDEF'[j], d['root'][1], t) for j, (t, d) in enumerate(rootsy)]

# conexiones por estancia
ACC = collections.defaultdict(list)
for L in LK: ACC[L['from']].append(L['id'][:3]); ACC[L['to']].append(L['id'][:3])

# extensión total medida
allg = unary_union(list(DECK.values()) + [LineString([p[:2] for p in pts]).buffer(1.3) for pts in ROUTE.values()])
BX = allg.bounds

# ------------------------------------------------------------------ hoja
class Sheet:
    def __init__(s, page, ttl, sub):
        s.page = page; s.width, s.height = 841, 594; s.title = ttl; s.sub = sub; s.ops = []; s.meta = {'page': page, 'scale': 200}
        cx = (BX[0] + BX[2]) / 2; cy = (BX[1] + BX[3]) / 2
        s.ox = 318 - cx * K; s.oy = 322 - cy * K
    def pt(s, p): return [s.ox + p[0] * K, s.oy + p[1] * K]
    def lp(s, pts, lw=.13, dash=None, kind=''):
        if len(pts) > 1: s.ops.append({'type': 'line', 'points': pts, 'lw': lw, 'dash': dash or [], 'kind': kind})
    def line(s, pts, lw=.13, dash=None, kind=''): s.lp([s.pt(p) for p in pts], lw, dash, kind)
    def pp(s, rings, lw=.13, fill=None, kind=''): s.ops.append({'type': 'polygon', 'rings': rings, 'lw': lw, 'fill': fill, 'kind': kind})
    def geom(s, g, lw=.13, fill=None, dash=None, kind=''):
        for p in polys(g):
            rings = [[s.pt(q) for q in r.coords] for r in [p.exterior] + list(p.interiors)]
            if dash:
                for r in rings: s.lp(r, lw, dash, kind)
            else: s.pp(rings, lw, fill, kind)
    def tx(s, p, t, size=2.5, angle=0, align='left', kind='', paper=True, mask=False):
        q = list(p) if paper else s.pt(p)
        if mask:
            w = len(t) * size * .46 + 1.0; x0 = q[0] - (w / 2 if align == 'center' else (w if align == 'right' else 0))
            s.pp([[(x0 - .4, q[1] - .7), (x0 + w, q[1] - .7), (x0 + w, q[1] + size * .82), (x0 - .4, q[1] + size * .82), (x0 - .4, q[1] - .7)]], .01, 1, 'FONDO')
        s.ops.append({'type': 'text', 'point': q, 'text': t, 'height': size, 'angle': angle, 'align': align, 'kind': kind})
    def bubble(s, q, lab, rad=2.1, size=1.9):
        s.pp([[[q[0] + rad * math.cos(t * math.pi / 16), q[1] + rad * math.sin(t * math.pi / 16)] for t in range(33)]], .13, 1, 'EJES')
        s.tx((q[0], q[1] - .7), lab, size, align='center', kind='EJES')
    def frame(s, col, foot):
        W, H = s.width, s.height
        s.lp([(12, 12), (W - 12, 12), (W - 12, H - 12), (12, H - 12), (12, 12)], .13, kind='MARCO')
        s.tx((20, H - 27), s.title, 5.2); s.tx((20, H - 35), s.sub, 2.7)
        s.tx((W - 20, 20), s.page, 4.5, align='right')
        s.tx((20, 20), 'G3 · megaestructura macarra · medida desde Rhino', 2.4)
        s.lp([(20, 61), (W - 20, 61)], .13, kind='MARCO')
        y = 53
        for t in foot: s.tx((20, y), t, 2.5); y -= 6
        x = 640; y = H - 50
        for t, size in col:
            if size == 'gap': y -= 3; continue
            s.tx((x, y), t, size); y -= (6 if size >= 3 else 4.6)
        s.meta['column_bottom_mm'] = y
        # barra gráfica: 10 m = 50 mm a 1:200
        x = W - 75; y = 29
        for i in range(5): s.pp([[(x + i * 10, y), (x + (i + 1) * 10, y), (x + (i + 1) * 10, y + 2), (x + i * 10, y + 2), (x + i * 10, y)]], .13, 0 if i % 2 == 0 else 1, 'ESCALA')
        for i, l in [(0, '0'), (1, '2'), (2, '4'), (5, '10 m')]: s.tx((x + i * 10, y + 4), l, 2.2, align='center')

    # ---------------------------------------------------------- piezas de dibujo
    def grid(s):
        x0, y0, x1, y1 = BX
        for lab, x, t in GX:
            s.line([(x, y0 - 3.0), (x, y1 + 2.5)], .10, [3, .7, .2, .7], 'EJES_MALLA')
            s.bubble(s.pt((x, y1 + 3.6)), lab)
        for lab, y, t in GY:
            s.line([(x0 - 3.0, y), (x1 + 2.5, y)], .10, [3, .7, .2, .7], 'EJES_MALLA')
            s.bubble(s.pt((x0 - 4.1, y)), lab)
        # cadenas de cotas entre ejes
        xs = [x for _, x, _ in GX]; ys = [y for _, y, _ in GY]
        s.chain(xs, y1 + 6.4, 'x'); s.chain(ys, x0 - 7.0, 'y')
    def chain(s, vals, at, axis):
        for a, b in zip(vals[:-1], vals[1:]):
            if axis == 'x': A, B = (a, at), (b, at)
            else: A, B = (at, a), (at, b)
            s.line([A, B], .13, kind='COTAS')
            for q in (A, B):
                pq = s.pt(q); s.lp([(pq[0] - .8, pq[1] - .8), (pq[0] + .8, pq[1] + .8)], .18, kind='COTAS')
            m = s.pt(((A[0] + B[0]) / 2, (A[1] + B[1]) / 2))
            if axis == 'x': s.tx((m[0], m[1] + 1.0), num(b - a), 2.0, align='center', kind='COTAS')
            else: s.tx((m[0] - 1.0, m[1]), num(b - a), 2.0, 90, 'center', 'COTAS')
    def dim(s, a, b, off, axis):
        if axis == 'x':
            A, B = (a[0], off), (b[0], off); s.line([a, (a[0], off)], .08, kind='COTAS'); s.line([b, (b[0], off)], .08, kind='COTAS')
        else:
            A, B = (off, a[1]), (off, b[1]); s.line([a, (off, a[1])], .08, kind='COTAS'); s.line([b, (off, b[1])], .08, kind='COTAS')
        s.line([A, B], .13, kind='COTAS')
        for q in (A, B):
            pq = s.pt(q); s.lp([(pq[0] - .8, pq[1] - .8), (pq[0] + .8, pq[1] + .8)], .18, kind='COTAS')
        m = s.pt(((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)); v = abs(B[0] - A[0]) if axis == 'x' else abs(B[1] - A[1])
        if axis == 'x': s.tx((m[0], m[1] + .9), num(v), 2.0, align='center', kind='COTAS')
        else: s.tx((m[0] - .9, m[1]), num(v), 2.0, 90, 'center', 'COTAS')
    def trunks(s, lw=.18, labels=True):
        for t, d in TR.items():
            s.line([q[:2] for q in d['axis']], lw, [4, .8, .25, .8], 'EJE_TRONCO')
            for b in d['branches']: s.line([q[:2] for q in b], .10, [2.2, .6, .2, .6], 'EJE_RAMA')
            r = d['root']; q = s.pt(r[:2])
            s.lp([(q[0] - 2.4, q[1]), (q[0] + 2.4, q[1])], .13, kind='RAIZ'); s.lp([(q[0], q[1] - 2.4), (q[0], q[1] + 2.4)], .13, kind='RAIZ')
            s.pp([[[q[0] + .67 * K * math.cos(a * math.pi / 16), q[1] + .67 * K * math.sin(a * math.pi / 16)] for a in range(33)]], .25, None, 'RAIZ')
            if labels: s.tx((q[0] + 3.6, q[1] - 4.2), f'{t} · raíz {cota(r[2])}', 2.0, kind='TRONCOS', mask=True)
    def ovalaxes(s, i, lab=True, dims=True):
        c = SP[i]['c']; g = DECK[i]; x0, y0, x1, y1 = g.bounds
        hx = LineString([(x0 - 1.2, c[1]), (x1 + 1.2, c[1])]); hy = LineString([(c[0], y0 - 1.2), (c[0], y1 + 1.2)])
        s.line(list(hx.coords), .10, [3, .6, .2, .6], 'EJE_SIMETRIA'); s.line(list(hy.coords), .10, [3, .6, .2, .6], 'EJE_SIMETRIA')
        for q in [(x1 + 1.2, c[1]), (c[0], y1 + 1.2)]:
            s.bubble(s.pt(q), 'S', 1.5, 1.6)
        if dims:
            ix = g.intersection(LineString([(x0 - 1, c[1]), (x1 + 1, c[1])])); iy = g.intersection(LineString([(c[0], y0 - 1), (c[0], y1 + 1)]))
            if not ix.is_empty:
                bx = ix.bounds; s.dim((bx[0], c[1]), (bx[2], c[1]), y0 - 1.0, 'x')
            if not iy.is_empty:
                by = iy.bounds; s.dim((c[0], by[1]), (c[0], by[3]), x1 + 1.0, 'y')
    def stair(s, L, mode='plan', zcut=None):
        pts = ROUTE.get(L['id'])
        if not pts: return
        eid = int(L['id'][1:3])
        treads = [p for p in PIECES['03_ESCALERAS_PELDANOS'] if p['name'] == L['id']]
        for p in treads:
            for o in p['outline']:
                if len(o) < 3: continue
                above = zcut is not None and p['z'][1] > zcut + .02
                g = clean(Polygon(o))
                s.geom(g, .10 if above else .13, None if above else 1, [1.2, .6] if above else None, 'PELDANO')
        s.line([q[:2] for q in pts], .18, kind='LINEA_DE_HUELLA')
        a, b = pts[-2], pts[-1]; ang = math.atan2(b[1] - a[1], b[0] - a[0]); q = s.pt(b[:2])
        s.pp([[(q[0] + 1.6 * math.cos(ang), q[1] + 1.6 * math.sin(ang)), (q[0] + 1.0 * math.cos(ang + 2.5), q[1] + 1.0 * math.sin(ang + 2.5)), (q[0] + 1.0 * math.cos(ang - 2.5), q[1] + 1.0 * math.sin(ang - 2.5)), (q[0] + 1.6 * math.cos(ang), q[1] + 1.6 * math.sin(ang))]], .13, 0, 'SUBE')
        q0 = s.pt(pts[0][:2]); s.pp([[[q0[0] + .9 * math.cos(t * math.pi / 8), q0[1] + .9 * math.sin(t * math.pi / 8)] for t in range(17)]], .13, 1, 'ARRANQUE')
        mid = pts[len(pts) // 2]; m1 = pts[len(pts) // 2 + 1]; an = math.degrees(math.atan2(m1[1] - mid[1], m1[0] - mid[0]))
        an = (an + 90) % 180 - 90
        return mid, an

def descansillos(s, eids):
    for p in PIECES['04_DESCANSILLOS']:
        if link_of(p['name']) in eids:
            for o in p['outline']:
                if len(o) > 2: s.geom(clean(Polygon(o)), .18, 1, kind='DESCANSILLO')
    for p in PIECES['19_MOBILIARIO']:
        if p['name'].startswith('R') and link_of(p['name']) in eids:
            for o in p['outline']:
                if len(o) > 2: s.geom(clean(Polygon(o)), .13, 1, kind='BANCO_DESCANSILLO')

POCHE = {'05_BARANDILLAS', '07_COSTILLAS', '08_CELULAS_PERFORADAS', '06_MEGATRONCOS', '20_ANCLAJES', '02_BORDES_AMARILLOS', '17_UNIONES_COBRE', '09_TENSORES'}

def estancia(s, i, zcut):
    g = DECK[i]
    s.geom(g, .25, 1, kind='TABLERO')
    # borde: cordón superior del tablero (0,28 m) visto
    s.geom(g.buffer(-.28), .10, None, kind='CORDON')
    # piezas propias de la estancia
    for lay, lw in [('14_AGUA', .10), ('13_DEPOSITOS_CRISTAL', .13), ('19_MOBILIARIO', .18), ('16_MAQUINARIA', .10), ('18_LUZ', .10)]:
        for p in PIECES[lay]:
            if est_of(p['name']) != i: continue
            z0, z1 = p['z']
            for o in p['outline']:
                if len(o) < 3: continue
                pg = clean(Polygon(o))
                if z1 < DECKZ[i][0] - .02:     # bajo el tablero: oculto
                    s.geom(pg, .10, None, [1.0, .6], 'BAJO_TABLERO')
                elif z0 > zcut:                # por encima del corte
                    s.geom(pg, .10, None, [1.8, .8], 'SOBRE_CORTE')
                elif z0 < zcut < z1:
                    pass                       # se dibuja en el corte
                else:
                    s.geom(pg, lw, 1 if lay in ('19_MOBILIARIO',) else None, kind='VISTO')
    # velas y células por encima
    for lay in ('10_MEMBRANAS',):
        for o in OUTL[lay]:
            if est_of(o['name']) != i: continue
            for r in o['polys']:
                if len(r) > 2: s.line(r + [r[0]], .10, [1.8, .8], 'VELA_SOBRE_CORTE')
    # corte a +1,20
    keep = g.buffer(2.5); poche = []; thin = []
    for c in CUTS[i]:
        for r in c['polys']:
            if len(r) < 3: continue
            closed = math.dist(r[0], r[-1]) < .01
            if closed:
                pg = clean(Polygon(r))
                if pg.is_empty or not pg.intersects(keep): continue
                if c['layer'] in POCHE: poche.append(pg)
                else: thin.append((c['layer'], pg))
            else:
                ls = LineString(r)
                if ls.intersects(keep): s.line(r, .25, kind='CORTE')
    for lay, pg in thin: s.geom(pg, .18, 1, kind='CORTE_' + lay)
    if poche: s.geom(unary_union(poche), .18, 0, kind='CORTE_NEGRO')
    for c in TCUT[i]:
        for r in c['polys']:
            if len(r) > 2 and math.dist(r[0], r[-1]) < .01:
                pg = clean(Polygon(r))
                if pg.intersects(g.buffer(6)): s.geom(pg, .25, 0, kind='TRONCO_CORTADO')

def label_est(s, i, extra=True):
    c = SP[i]['c']; g = DECK[i]
    q = s.pt((c[0] + .6, c[1] + .9))
    s.tx(q, f'E{i:02d} · {title(SP[i]["name"])}', 2.4, kind='ESTANCIA', mask=True)
    s.tx((q[0], q[1] - 3.4), f'{cota(DECKZ[i][1])} · {num(g.area, 1)} m²', 2.0, kind='ESTANCIA', mask=True)
    if extra:
        s.tx((q[0], q[1] - 6.4), 'accesos ' + ' · '.join(sorted(ACC[i])), 1.7, kind='ESTANCIA', mask=True)
    # nivel
    t = s.pt((c[0] - .6, c[1] - .6))
    s.pp([[(t[0], t[1]), (t[0] - 1.2, t[1] + 1.4), (t[0] + 1.2, t[1] + 1.4), (t[0], t[1])]], .13, 1, 'NIVEL')

# ------------------------------------------------------------------ PDF / SVG
def pdfpage(c, s):
    c.setPageSize((s.width * mm, s.height * mm)); c.setFillColorRGB(1, 1, 1); c.rect(0, 0, s.width * mm, s.height * mm, fill=1, stroke=0)
    for ob in s.ops:
        c.setStrokeColorRGB(0, 0, 0); c.setFillColorRGB(0, 0, 0)
        if ob['type'] == 'text':
            c.saveState(); c.translate(ob['point'][0] * mm, ob['point'][1] * mm); c.rotate(ob['angle']); c.setFont('Ibarra', ob['height'] * mm)
            {'center': c.drawCentredString, 'right': c.drawRightString}.get(ob['align'], c.drawString)(0, 0, ob['text']); c.restoreState(); continue
        stroke = 0 if ob.get('kind') == 'FONDO' else 1
        c.setLineWidth(ob['lw'] * mm); c.setDash([x * mm for x in ob.get('dash', [])], 0); c.setLineJoin(1); c.setLineCap(0)
        path = c.beginPath(); rings = ob['rings'] if ob['type'] == 'polygon' else [ob['points']]
        for pts in rings:
            path.moveTo(pts[0][0] * mm, pts[0][1] * mm)
            for q in pts[1:]: path.lineTo(q[0] * mm, q[1] * mm)
            if ob['type'] == 'polygon': path.close()
        fill = ob.get('fill'); c.setFillColorRGB(1, 1, 1) if fill == 1 else c.setFillColorRGB(0, 0, 0)
        c.drawPath(path, stroke=stroke, fill=fill is not None, fillMode=0)
    c.showPage()

def svg(s):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.width}mm" height="{s.height}mm" viewBox="0 0 {s.width} {s.height}"><defs><style>@font-face{{font-family:Ibarra;src:url(IbarraRealNova-Italic-400.ttf)}}text{{font-family:Ibarra;font-style:italic}}</style></defs><rect width="100%" height="100%" fill="white"/>']
    for ob in s.ops:
        if ob['type'] == 'text':
            x, y = ob['point']; a = {'left': 'start', 'center': 'middle', 'right': 'end'}[ob['align']]
            out.append(f'<text x="{x:.3f}" y="{s.height - y:.3f}" font-size="{ob["height"]}" text-anchor="{a}" transform="rotate({-ob["angle"]} {x:.3f} {s.height - y:.3f})">{html.escape(ob["text"])}</text>'); continue
        rings = ob['rings'] if ob['type'] == 'polygon' else [ob['points']]
        d = ' '.join('M ' + ' L '.join(f'{x:.3f},{s.height - y:.3f}' for x, y in pts) + (' Z' if ob['type'] == 'polygon' else '') for pts in rings)
        fill = 'none' if ob.get('fill') is None else ('white' if ob['fill'] == 1 else 'black'); st = 'none' if ob.get('kind') == 'FONDO' else 'black'
        out.append(f'<path d="{d}" fill="{fill}" fill-rule="evenodd" stroke="{st}" stroke-width="{ob["lw"]}" stroke-dasharray="{" ".join(map(str, ob.get("dash", [])))}"/>')
    out.append('</svg>'); return '\n'.join(out)

LEYENDA = [('LECTURA DEL DIBUJO', 3.2), ('Negro sólido: material cortado a +1,20 m', 2.4), ('0,25 mm: borde del tablero', 2.4), ('0,18 mm: mobiliario y línea de huella', 2.4),
           ('0,13 mm: peldaños vistos', 2.4), ('Discontinua larga: velas y luces sobre el corte', 2.4), ('Discontinua corta: máquinas bajo el tablero', 2.4),
           ('Trazo-punto grueso: eje del tronco portante', 2.4), ('Trazo-punto fino: ejes de rama y de la malla 1-6 / A-F', 2.4),
           ('S: eje de simetría del óvalo generador', 2.4), ('Círculo blanco: arranque · triángulo: llegada', 2.4), ('gap', 'gap')]
SHEETS = []

# ------------------------------------------------------------------ M01 · planta general
s = Sheet('MG01', 'Megaestructura macarra · planta general', 'PLANTA · E 1:200 · tableros vistos desde arriba · malla de troncos · recorridos')
s.grid()
order = sorted(range(len(SP)), key=lambda i: DECKZ[i][1])
for L in LK: descansillos(s, [int(L['id'][1:3])])
for L in sorted(LK, key=lambda L: min(SP[L['from']]['c'][2], SP[L['to']]['c'][2])):
    pts = ROUTE[L['id']]; s.line([q[:2] for q in pts], .13, kind='LINEA_DE_HUELLA')
for i in order:
    g = DECK[i]; s.geom(g, .25, 1, kind='TABLERO'); s.geom(g.buffer(-.28), .10, None, kind='CORDON')
s.trunks()
for L in LK:
    pts = ROUTE[L['id']]; s.stair(L)
for i in order: s.ovalaxes(i, dims=False); label_est(s, i, extra=False)
for L in LK:
    pts = ROUTE[L['id']]; mid = pts[len(pts) // 2]
    s.tx(s.pt((mid[0], mid[1] - .25)), L['id'][:3], 1.7, align='center', kind='CONEXION', mask=True)
x0, y0, x1, y1 = BX
s.dim((x0, y0), (x1, y0), y0 - 4.0, 'x'); s.dim((x1, y0), (x1, y1), x1 + 9.5, 'y')
col = [('ESTRUCTURA', 3.2)]
for t, d in TR.items():
    col.append((f'{t} · raíz {cota(d["root"][2])} · copa {cota(d["top"][2])} · {len(d["branches"])} ramas', 2.4))
    col.append(('      a ' + ' · '.join(f'E{i:02d}' for i in d['serves']), 2.0))
col += [('gap', 'gap'), ('RECORRIDOS', 3.2), (f'{len(LK)} escaleras entre {len(SP)} estancias', 2.4),
        (f'{sum(L["risers"] for L in LK)} peldaños · contrahuella máx. {num(max(L["rise_max"] for L in LK) * 100, 1)} cm', 2.4),
        (f'Anchos de {num(min(L["width"] for L in LK))} a {num(max(L["width"] for L in LK))} m', 2.4),
        (f'{len(PIECES["04_DESCANSILLOS"])} descansillos habitados con bancos', 2.4), ('Cada escalera: dos tramos y meseta central', 2.4),
        ('gap', 'gap')] + LEYENDA
s.frame(col, ['Tableros dibujados desde arriba: el más alto tapa al más bajo. Cotas de tablero acabado medidas en Rhino.',
              'Malla 1-6 / A-F: ejes por las raíces de los seis troncos. Las ramas no siguen la malla: cada una busca su estancia.',
              'Geometría de malla del modelo MEGAESTRUCTURA_MACARRA.3dm (967 mallas, 1,93 M triángulos), sin redibujar.'])
SHEETS.append(s)

# ------------------------------------------------------------------ M02-M06 · plantas por niveles
BANDS_OLD = [('M02', [0, 1, 2, 13, 3, 14]), ('M03', [4, 15, 16, 5, 6, 17]), ('M04', [7, 18, 8, 19, 9, 20]), ('M05', [10, 21, 11, 22, 12, 23]), ('M06', [24, 27, 26, 25])]
for page, ids in []:
    zs = [DECKZ[i][1] for i in ids]
    s = Sheet(page, f'Megaestructura macarra · estancias {cota(min(zs))} a {cota(max(zs))}', 'PLANTA · E 1:200 · corte a +1,20 m sobre el tablero de cada estancia · peldaños por encima del corte en discontinua')
    s.grid()
    # contexto: tableros de otros niveles
    for j in range(len(SP)):
        if j in ids: continue
        s.geom(DECK[j], .08, None, [.6, .6], 'OTRO_NIVEL')
    s.trunks(lw=.13, labels=False)
    eids = [int(L['id'][1:3]) for L in LK if L['from'] in ids or L['to'] in ids]
    descansillos(s, eids)
    for L in LK:
        if L['from'] in ids or L['to'] in ids:
            lo = L['from'] if SP[L['from']]['c'][2] < SP[L['to']]['c'][2] else L['to']
            zc = (DECKZ[lo][1] + 1.20) if lo in ids else None
            s.stair(L, zcut=zc)
    for i in sorted(ids, key=lambda i: DECKZ[i][1]):
        estancia(s, i, DECKZ[i][1] + 1.20)
    for i in ids: s.ovalaxes(i); label_est(s, i)
    for L in LK:
        if L['from'] in ids or L['to'] in ids:
            pts = ROUTE[L['id']]; mid = pts[len(pts) // 2]; a, b = L['from'], L['to']
            lo, hi = (a, b) if SP[a]['c'][2] < SP[b]['c'][2] else (b, a)
            s.tx(s.pt((mid[0], mid[1] + .35)), f'{L["id"][:3]} · E{lo:02d} a E{hi:02d}', 1.8, align='center', kind='CONEXION', mask=True)
            s.tx(s.pt((mid[0], mid[1] - .55)), f'{L["risers"]} p · {num(L["rise_max"] * 100, 1)} cm · {num(L["width"])} m', 1.6, align='center', kind='CONEXION', mask=True)
    col = [('PROGRAMA', 3.2)]
    for i in sorted(ids, key=lambda i: DECKZ[i][1]):
        seats = sum(1 for p in PIECES['19_MOBILIARIO'] if est_of(p['name']) == i) // 2
        water = any(est_of(p['name']) == i for p in PIECES['14_AGUA'])
        mach = sum(1 for p in PIECES['16_MAQUINARIA'] if est_of(p['name']) == i)
        lights = sum(1 for p in PIECES['18_LUZ'] if est_of(p['name']) == i)
        sails = sum(1 for o in OUTL['10_MEMBRANAS'] if est_of(o['name']) == i)
        col.append((f'E{i:02d} · {title(SP[i]["name"])}', 2.6))
        col.append((f'      {cota(DECKZ[i][1])} · {num(DECK[i].area, 1)} m² · tablero {num((DECKZ[i][1] - DECKZ[i][0]) * 100, 0)} cm', 2.0))
        bits = [f'{seats} bancos con respaldo' if seats else 'sin bancos', f'{sails} velas', f'{mach} cilindros bajo el tablero' if mach else '', f'{lights} luces' if lights else '', 'cuenco de agua y vasijas colgadas' if water else '']
        col.append(('      ' + ' · '.join(b for b in bits if b), 2.0))
        col.append(('      accesos ' + ' · '.join(sorted(ACC[i])), 2.0))
    col += [('gap', 'gap')] + LEYENDA
    s.frame(col, ['Cada estancia se corta a +1,20 m sobre su propio tablero: la planta es escalonada y se lee estancia a estancia.',
                  'Tableros de otros niveles en punteado fino. Troncos cortados a la altura de cada estancia, en negro.',
                  'Escaleras: línea de huella desde el arranque, meseta central, número de peldaños, contrahuella máxima y ancho medidos.'])
    SHEETS.append(s)

c = canvas.Canvas(str(OUT / 'G3_MEGAESTRUCTURA_PLANTAS_1_200.pdf'), pageCompression=1); c.setTitle('Megaestructura macarra · plantas 1:200'); c.setAuthor('G3')
for s in SHEETS:
    pdfpage(c, s)
    (OUT / f'{s.page}_MEGAESTRUCTURA.svg').write_text(svg(s))
c.save()
json.dump({'trunks': {t: {'root': d['root'], 'top': d['top'], 'serves': d['serves']} for t, d in TR.items()},
           'grid_x': GX, 'grid_y': GY, 'deck_area_m2': {f'E{i:02d}': DECK[i].area for i in DECK}, 'deck_top_m': {f'E{i:02d}': DECKZ[i][1] for i in DECK},
           'extent': BX}, open(OUT / 'MEGA_MEDIDAS.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(SHEETS))
