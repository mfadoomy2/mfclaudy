# -*- coding: utf-8 -*-
"""
P01 — PLANTA GENERAL · REFUGIO CLIMATICO PUERTA DEL SOL
Lamina A1 apaisada (841x594 mm) · escala 1:500 · norte arriba.
Generada desde geometria_maestra.json segun 02_MANUAL_GRAFICO (paleta, grosores, certezas, reticula).
Unidades del SVG: mm de papel. 1 m real = 2 mm de papel (1:500).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, '..', '..', '01_BASE_GEOMETRICA', 'planta_maestra', 'geometria_maestra.json')
m = json.load(open(GEO, encoding='utf-8'))

# ------------- paleta (manual) -------------
TURQ, TURQD = '#3E969B', '#2E6E6B'
LIMA, VAGUA, VVEG, VALGA = '#C3D48A', '#8FC7AE', '#6F8F53', '#6E7A45'
ROSA, ROSAI, COBRE = '#E794AC', '#D6577F', '#B08968'
GPIEDRA, GCTX, GTEC = '#EDEAE4', '#B5B1A9', '#33322E'

# ------------- marco de lamina -------------
PW, PH = 841.0, 594.0           # A1 apaisado mm
MARG = 20.0
COL_W = 150.0                   # columna tecnica derecha
FIELD_X0, FIELD_Y0 = MARG, MARG
FIELD_W = PW - 2 * MARG - COL_W - 10
FIELD_H = PH - 2 * MARG
SCALE = 2.0                     # mm por metro (1:500)
# ventana del plano en metros (centrada en la mancha util)
CX, CY = 5.0, 8.0               # centro geometrico aproximado de la vista
WX = FIELD_W / SCALE            # ancho en m
WY = FIELD_H / SCALE


def T(p):
    x, y = p[0], p[1]
    return (FIELD_X0 + (x - (CX - WX / 2)) * SCALE,
            FIELD_Y0 + ((CY + WY / 2) - y) * SCALE)


def path_of(pts, close=False):
    s = 'M ' + ' L '.join('%.2f %.2f' % T(p) for p in pts)
    return s + (' Z' if close else '')


def ell(cx, cy, rx, ry, rot_deg, n=72):
    r = math.radians(rot_deg)
    return [(cx + rx * math.cos(2 * math.pi * i / n) * math.cos(r) - ry * math.sin(2 * math.pi * i / n) * math.sin(r),
             cy + rx * math.cos(2 * math.pi * i / n) * math.sin(r) + ry * math.sin(2 * math.pi * i / n) * math.cos(r))
            for i in range(n + 1)]


# grosores 1:500 A1 (mm papel)
W008, W010, W013, W018, W025, W035, W050 = 0.08, 0.10, 0.13, 0.18, 0.25, 0.35, 0.50
G3DASH = 'stroke-dasharray="2.2 1.6"'

S = []
S.append('<svg xmlns="http://www.w3.org/2000/svg" width="841mm" height="594mm" viewBox="0 0 841 594" font-family="Arial">')
S.append('<rect width="841" height="594" fill="#FFFFFF"/>')

# ---------- recorte del campo ----------
S.append('<clipPath id="field"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath>' % (FIELD_X0, FIELD_Y0, FIELD_W, FIELD_H))
S.append('<g clip-path="url(#field)">')

# ---------- CONTEXTO ----------
S.append('<g id="CONTEXTO">')
for h in m['contexto']['highways']:
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f"/>' % (path_of(h['pts']), GCTX, W008))
for b in m['contexto']['buildings']:
    if len(b['pts']) >= 3:
        S.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%.2f"/>' % (path_of(b['pts'], True), GPIEDRA, GCTX, W010))
cc = m['contexto']['casa_correos']['pts']
S.append('<path d="%s" fill="#E7E3DB" stroke="#8E8A82" stroke-width="%.2f"/>' % (path_of(cc, True), W018))
for t in m['contexto']['trees']:
    x, y = T((t['x'], t['y']))
    S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="%s" stroke-width="%.2f" opacity="0.8"/><circle cx="%.2f" cy="%.2f" r="0.28" fill="%s"/>' % (
        x, y, 1.8 * SCALE * 0.9, VVEG, W010, x, y, VVEG))
for e in m['contexto']['metro']:
    x, y = T((e['x'], e['y']))
    S.append('<rect x="%.2f" y="%.2f" width="4.4" height="4.4" fill="#FFFFFF" stroke="#5B5B8F" stroke-width="%.2f"/>' % (x - 2.2, y - 2.2, W018))
    S.append('<path d="M %.2f %.2f v -2.2 l 1.1 1.35 1.1 -1.35 v 2.2" fill="none" stroke="#5B5B8F" stroke-width="%.2f"/>' % (x - 1.1, y + 1.15, W013))
S.append('</g>')

# ---------- CIRCULACION: pasos libres ----------
S.append('<g id="CIRCULACION_pasos" fill="none" stroke="%s" stroke-width="%.2f" stroke-dasharray="3 2.2" opacity="0.9">' % (GCTX, W010))
for c in m['circulacion']['corridors']:
    S.append('<path d="%s"/>' % path_of(c['pts']))
S.append('</g>')

# ---------- PAISAJE ----------
S.append('<g id="PAISAJE">')
for p in m['paisaje']['planters']:
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round" opacity="0.75" %s/>' % (
        path_of(p['pts']), VVEG, 1.4 * SCALE * 0.5, G3DASH if p['g'] == 'G3' else ''))
for d in m['paisaje']['discs']:
    x, y = T((d['cx'], d['cy']))
    r = d['r'] * SCALE
    dash = G3DASH if d.get('g') == 'G3' else ''
    S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" fill-opacity="0.55" stroke="#8FB35B" stroke-width="%.2f" %s/>' % (x, y, r, LIMA, W013, dash))
    # nervaduras radiales finas (4 radios)
    for a in (0, 45, 90, 135):
        ar = math.radians(a)
        S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#8FB35B" stroke-width="%.2f" opacity="0.6"/>' % (
            x - r * math.cos(ar), y - r * math.sin(ar), x + r * math.cos(ar), y + r * math.sin(ar), W008))
for (tx, ty) in m['paisaje']['new_trees']:
    x, y = T((tx, ty))
    S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="%s" stroke-width="%.2f"/><circle cx="%.2f" cy="%.2f" r="0.35" fill="%s"/>' % (
        x, y, 2.4 * SCALE * 0.9, VVEG, W013, x, y, VVEG))
S.append('</g>')

# ---------- AGUA / CLIMA ----------
S.append('<g id="AGUA_CLIMA">')
for p in m['agua_clima']['pools']:
    S.append('<path d="%s" fill="%s" fill-opacity="0.55" stroke="#4E9B6E" stroke-width="%.2f"/>' % (
        path_of(ell(p['cx'], p['cy'], p['rx'], p['ry'], p['rot']), True), VAGUA, W013))
for p in m['agua_clima']['ground_ponds']:
    if p['kind'] == 'circle':
        x, y = T((p['cx'], p['cy']))
        S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" fill-opacity="0.7" stroke="#2F7D57" stroke-width="%.2f"/>' % (
            x, y, p['r'] * SCALE, VALGA, W013))
    else:
        S.append('<path d="%s" fill="%s" fill-opacity="0.7" stroke="#2F7D57" stroke-width="%.2f" %s/>' % (
            path_of(p['pts'], True), VALGA, W013, G3DASH if p['g'] == 'G3' else ''))
sp = m['agua_clima']['splash']
S.append('<path d="%s" fill="#BFE9E4" fill-opacity="0.6" stroke="#63BFB4" stroke-width="%.2f" %s/>' % (
    path_of(ell(sp['cx'], sp['cy'], sp['rx'], sp['ry'], sp['rot']), True), W010, G3DASH))
for w in m['agua_clima']['mains']:
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" %s/>' % (path_of(w), ROSAI, W025, G3DASH))
for (nx, ny) in m['agua_clima']['nebul']:
    x, y = T((nx, ny))
    S.append('<circle cx="%.2f" cy="%.2f" r="0.45" fill="%s"/>' % (x, y, ROSAI))
S.append('</g>')

# ---------- ESTRUCTURA LIGERA ----------
S.append('<g id="ESTRUCTURA_LIGERA">')
for (mx, my) in m['estructura_ligera']['masts']:
    x, y = T((mx, my))
    S.append('<circle cx="%.2f" cy="%.2f" r="0.4" fill="#7A7A7A"/>' % (x, y))
for t in m['estructura_ligera']['tanks']:
    for k in range(t['n']):
        x, y = T((t['cx'] + k * 2.6, t['cy']))
        r = t['r'] * SCALE
        S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" fill-opacity="0.8" stroke="#C23B7E" stroke-width="%.2f" %s/>' % (x, y, r, ROSAI, W013, G3DASH))
        S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#C23B7E" stroke-width="%.2f"/>' % (x - r, y, x + r, y, W008))
for (dx, dy) in m['estructura_ligera']['drops']:
    x, y = T((dx, dy))
    S.append('<circle cx="%.2f" cy="%.2f" r="1.6" fill="none" stroke="#7FC7BD" stroke-width="%.2f"/>' % (x, y, W013))
S.append('</g>')

# ---------- ESTRUCTURA PRINCIPAL ----------
S.append('<g id="ESTRUCTURA_PRINCIPAL" fill="none">')
for lp in m['estructura_principal']['loops']:
    w = W035 if lp['g'] == 'G1' else W025
    op = '1.0' if lp['g'] == 'G1' else '0.85'
    S.append('<path d="%s" stroke="%s" stroke-width="%.2f" stroke-opacity="%s"/>' % (
        path_of(ell(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot']), True), TURQ, w * 2.2, op))
dm = m['estructura_principal']['dome']
x, y = T((dm['cx'], dm['cy']))
S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" stroke="%s" stroke-width="%.2f" fill="none" stroke-opacity="0.85"/>' % (x, y, dm['r'] * SCALE, TURQ, W018))
for a in range(0, 360, 30):
    ar = math.radians(a)
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%.2f" opacity="0.5"/>' % (
        x, y, x + dm['r'] * SCALE * math.cos(ar), y + dm['r'] * SCALE * math.sin(ar), TURQ, W008))
S.append('</g>')

# ---------- CIRCULACION: cinta ----------
rib = m['circulacion']['ribbon']
S.append('<path id="cinta" d="%s" fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round" stroke-opacity="0.92"/>' % (path_of(rib), TURQD, 2.5 * SCALE * 0.7))
S.append('<path d="%s" fill="none" stroke="#FFFFFF" stroke-width="%.2f" stroke-opacity="0.9"/>' % (path_of(rib), W025))
for (sx0, sy0) in m['circulacion']['stairs']:
    x, y = T((sx0, sy0))
    S.append('<rect x="%.2f" y="%.2f" width="4.4" height="2.6" fill="%s" transform="rotate(18 %.2f %.2f)"/>' % (x - 2.2, y - 1.3, TURQD, x, y))

# ---------- PROGRAMA ----------
S.append('<g id="PROGRAMA">')
for c in m['programa']['capsules']:
    x, y = T((c['cx'], c['cy']))
    w2, h2 = c['w'] * SCALE, c['h'] * SCALE
    dash = G3DASH if c.get('g') == 'G3' else ''
    S.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s" fill-opacity="0.65" stroke="#D14E92" stroke-width="%.2f" transform="rotate(%.1f %.2f %.2f)" %s/>' % (
        x - w2 / 2, y - h2 / 2, w2, h2, h2 / 2, ROSA, W013, -c.get('rot', 0), x, y, dash))
lab = m['programa']['lab']
S.append('<path d="%s" fill="#FFFFFF" fill-opacity="0.8" stroke="#D14E92" stroke-width="%.2f" %s/>' % (path_of(lab['pts'], True), W018, G3DASH))
for b in m['programa']['benches']:
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round"/>' % (path_of(b['pts']), COBRE, W035 * 2))
S.append('</g>')

# ---------- HITOS ----------
hit = m['contexto']['hitos']
for key, lbl in [('carlos_iii', 'Carlos III'), ('mariblanca', 'Mariblanca'), ('km0', 'Km 0'), ('oso_madrono', 'Oso y Madroño')]:
    x, y = T(hit[key])
    S.append('<circle cx="%.2f" cy="%.2f" r="1.0" fill="%s"/>' % (x, y, GTEC))
    S.append('<circle cx="%.2f" cy="%.2f" r="2.0" fill="none" stroke="%s" stroke-width="%.2f"/>' % (x, y, GTEC, W008))

# ---------- rotulos dentro del campo ----------
def label(x_m, y_m, text, size=2.8, color=GTEC, anchor='middle', spacing=0.6, font='Arial', rot=0):
    x, y = T((x_m, y_m))
    tr = ' transform="rotate(%.1f %.1f %.1f)"' % (rot, x, y) if rot else ''
    S.append('<text x="%.1f" y="%.1f" font-size="%.1f" fill="%s" text-anchor="%s" letter-spacing="%.1f" font-family="%s"%s>%s</text>' % (
        x, y, size, color, anchor, spacing, font, tr, text))


label(-22, -60, 'REAL CASA DE CORREOS', 3.2, '#8E8A82')
label(-22, -65, 'Presidencia de la Comunidad de Madrid', 2.2, '#A5A199')
label(-25.2, -41.5, 'reloj', 2.0, '#8E8A82')
label(-112, 28, 'Calle del Arenal', 2.4, '#A5A199', rot=-16)
label(-42, 76, 'Calle de Preciados', 2.4, '#A5A199', rot=72)
label(1, 92, 'Calle del Carmen', 2.4, '#A5A199', rot=88)
label(42, 86, 'Calle de la Montera', 2.4, '#A5A199', rot=-72)
label(106, 26, 'Calle de Alcalá', 2.4, '#A5A199', rot=-10)
label(104, -26, 'Carrera de San Jerónimo', 2.4, '#A5A199', rot=-20)
label(25, -52, 'Calle de Espoz y Mina', 2.2, '#A5A199', rot=83)
label(47, -54, 'Calle de Carretas', 2.2, '#A5A199', rot=80)
label(-116, -24, 'Calle Mayor', 2.4, '#A5A199', rot=-10)
label(-28, -18.5, 'Carlos III', 2.0)
label(-90, -9, 'Mariblanca', 2.0)
label(80, 26.5, 'Oso y Madroño', 2.0)
# clusters
label(-52, 5, 'C1', 5.0, TURQD, 'middle', 1.2, 'Bahnschrift')
label(8, 13, 'C2', 5.0, TURQD, 'middle', 1.2, 'Bahnschrift')
label(56, 8, 'C3', 5.0, TURQD, 'middle', 1.2, 'Bahnschrift')
label(30.5, 0.2, 'cúpula', 2.0, TURQD)
label(48, 19, 'LAB 02', 2.0, '#D14E92')
label(17, -9, 'lámina de agua', 2.0, '#63BFB4')

S.append('</g>')  # fin clip

# ---------- marco y columna tecnica ----------
S.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s" stroke-width="%.2f"/>' % (FIELD_X0, FIELD_Y0, FIELD_W, FIELD_H, GCTX, W013))
CXL = FIELD_X0 + FIELD_W + 10
S.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.2f"/>' % (CXL, MARG, CXL, PH - MARG, GCTX, W010))
TX = CXL + 8


def col_text(y, text, size=3.2, color=GTEC, font='Arial', spacing=0, bold=False):
    S.append('<text x="%.1f" y="%.1f" font-size="%.1f" fill="%s" font-family="%s" letter-spacing="%s"%s>%s</text>' % (
        TX, y, size, color, font, spacing, ' font-weight="600"' if bold else '', text))


col_text(34, 'FASE 01 · DOCUMENTO PILOTO', 3.0, TURQD, 'Bahnschrift', 1.4)
col_text(46, 'REFUGIO CLIMÁTICO', 8.5, GTEC, 'Bahnschrift', 0.5, True)
col_text(56, 'PUERTA DEL SOL · MADRID', 5.2, GTEC, 'Bahnschrift', 0.8)
col_text(70, 'P.01 — PLANTA GENERAL', 5.4, TURQD, 'Bahnschrift', 1.2)
col_text(77, 'Implantación · contexto real (OSM) · escala 1:500 (A1)', 2.6, '#8a877f')

# leyenda
ly = 94
col_text(ly, 'LEYENDA', 3.0, TURQD, 'Bahnschrift', 1.4)
legend = [
    ('loop', TURQ, 'loop estructural (anillos C1–C3)'),
    ('cinta', TURQD, 'cinta-recorrido elevada (+4/6 m)'),
    ('disc', LIMA, 'disco-canopy de microalgas (+5/10 m)'),
    ('pool', VAGUA, 'balsa de microalgas elevada'),
    ('pond', VALGA, 'estanque de cultivo en suelo'),
    ('splash', '#BFE9E4', 'lámina de agua jugable (1–2 cm)'),
    ('caps', ROSA, 'cápsula neumática (suelo / media altura)'),
    ('tank', ROSAI, 'depósito de agua elevado (+10 m)'),
    ('main', ROSAI, 'red hidráulica principal vista'),
    ('neb', ROSAI, 'nebulizador'),
    ('planter', VVEG, 'jardinera-banco curva'),
    ('tree', VVEG, 'árbol existente ∕ nuevo'),
    ('bench', COBRE, 'banco de madera en arco'),
    ('mast', '#7A7A7A', 'mástil ramificado'),
    ('metro', '#5B5B8F', 'boca de Metro / Cercanías'),
    ('hito', GTEC, 'monumento conservado'),
]
for i, (kind, col, txt) in enumerate(legend):
    yy = ly + 8 + i * 6.4
    if kind == 'loop':
        S.append('<ellipse cx="%.1f" cy="%.1f" rx="4.2" ry="2.4" fill="none" stroke="%s" stroke-width="0.7"/>' % (TX + 4, yy - 1, col))
    elif kind == 'cinta':
        S.append('<path d="M %.1f %.1f c 2.4 -2.6 5 2.6 8 -1.4" fill="none" stroke="%s" stroke-width="1.3" stroke-linecap="round"/>' % (TX, yy - 0.6, col))
    elif kind in ('disc',):
        S.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="%s" fill-opacity="0.55" stroke="#8FB35B" stroke-width="0.25"/>' % (TX + 4, yy - 1, col))
    elif kind == 'pool':
        S.append('<ellipse cx="%.1f" cy="%.1f" rx="3.4" ry="1.9" fill="%s" fill-opacity="0.55" stroke="#4E9B6E" stroke-width="0.25"/>' % (TX + 4, yy - 1, col))
    elif kind == 'pond':
        S.append('<circle cx="%.1f" cy="%.1f" r="2.2" fill="%s" fill-opacity="0.7" stroke="#2F7D57" stroke-width="0.25"/>' % (TX + 4, yy - 1, col))
    elif kind == 'splash':
        S.append('<ellipse cx="%.1f" cy="%.1f" rx="3.2" ry="1.7" fill="%s" fill-opacity="0.8" stroke="#63BFB4" stroke-width="0.25" stroke-dasharray="0.9 0.7"/>' % (TX + 4, yy - 1, col))
    elif kind == 'caps':
        S.append('<rect x="%.1f" y="%.1f" width="6" height="3" rx="1.5" fill="%s" fill-opacity="0.65" stroke="#D14E92" stroke-width="0.25"/>' % (TX + 1, yy - 2.5, col))
    elif kind == 'tank':
        S.append('<circle cx="%.1f" cy="%.1f" r="2" fill="%s" fill-opacity="0.85"/><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#fff" stroke-width="0.4"/>' % (TX + 4, yy - 1, col, TX + 2, yy - 1, TX + 6, yy - 1))
    elif kind == 'main':
        S.append('<path d="M %.1f %.1f h 8" stroke="%s" stroke-width="0.6" stroke-dasharray="2.2 1.6"/>' % (TX, yy - 1, col))
    elif kind == 'neb':
        S.append('<circle cx="%.1f" cy="%.1f" r="0.7" fill="%s"/>' % (TX + 4, yy - 1, col))
    elif kind == 'planter':
        S.append('<path d="M %.1f %.1f a 4 4 0 0 1 8 0" fill="none" stroke="%s" stroke-width="1" stroke-linecap="round"/>' % (TX, yy, col))
    elif kind == 'tree':
        S.append('<circle cx="%.1f" cy="%.1f" r="2.2" fill="none" stroke="%s" stroke-width="0.3"/><circle cx="%.1f" cy="%.1f" r="0.4" fill="%s"/>' % (TX + 4, yy - 1, col, TX + 4, yy - 1, col))
    elif kind == 'bench':
        S.append('<path d="M %.1f %.1f a 5 5 0 0 1 8 0" fill="none" stroke="%s" stroke-width="0.8"/>' % (TX, yy, col))
    elif kind == 'mast':
        S.append('<circle cx="%.1f" cy="%.1f" r="0.5" fill="%s"/>' % (TX + 4, yy - 1, col))
    elif kind == 'metro':
        S.append('<rect x="%.1f" y="%.1f" width="3.6" height="3.6" fill="none" stroke="%s" stroke-width="0.35"/>' % (TX + 2.2, yy - 2.8, col))
    elif kind == 'hito':
        S.append('<circle cx="%.1f" cy="%.1f" r="0.8" fill="%s"/><circle cx="%.1f" cy="%.1f" r="1.6" fill="none" stroke="%s" stroke-width="0.2"/>' % (TX + 4, yy - 1, col, TX + 4, yy - 1, col))
    col_text(yy, '&#160;&#160;&#160;&#160;&#160;&#160;' + txt, 2.6)

# certezas
cy0 = ly + 8 + len(legend) * 6.4 + 6
col_text(cy0, 'CERTEZA GEOMÉTRICA', 3.0, TURQD, 'Bahnschrift', 1.4)
for i, (g, txt, dash, op) in enumerate([
        ('G1', 'confirmado en varias referencias', '', 1.0),
        ('G2', 'muy probable', '', 0.85),
        ('G3', 'inferido (discontinua)', 'stroke-dasharray="2.2 1.6"', 1.0),
        ('G4', 'reserva Fase 02 (punteada)', 'stroke-dasharray="0.5 1.2"', 1.0)]):
    yy = cy0 + 7 + i * 5.6
    S.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.6" opacity="%s" %s/>' % (TX, yy - 1, TX + 9, yy - 1, TURQD, op, dash))
    col_text(yy, '&#160;&#160;&#160;&#160;&#160;&#160;%s — %s' % (g, txt), 2.5)

# datos clave
dy0 = cy0 + 7 + 4 * 5.6 + 7
col_text(dy0, 'DATOS', 3.0, TURQD, 'Bahnschrift', 1.4)
datos = [
    'superficie de la plaza · 10.957 m²',
    'extensión de la intervención · 163 × 51 m',
    'dosel (discos + balsas) · 1.890 m²',
    'loops estructurales · 8 + cúpula',
    'cápsulas neumáticas · 38',
    'árboles · 39 existentes + 20 nuevos',
    'banda libre ante Casa de Correos · 15 m',
    'altura máxima del sistema · 12 m',
]
for i, txt in enumerate(datos):
    col_text(dy0 + 7 + i * 5.2, txt, 2.6)

# norte + escala grafica
ny = PH - MARG - 52
S.append('<g transform="translate(%.1f %.1f)">' % (TX + 10, ny))
S.append('<circle r="8" fill="none" stroke="%s" stroke-width="0.45"/>' % GTEC)
S.append('<path d="M 0 6.5 L 0 -6.5 M 0 -6.5 L -2.4 -2.6 M 0 -6.5 L 2.4 -2.6" stroke="%s" stroke-width="0.45" fill="none"/>' % GTEC)
S.append('<text x="10" y="-6" font-size="4" fill="%s" font-family="Bahnschrift">N</text>' % GTEC)
S.append('</g>')
sy = PH - MARG - 32
S.append('<g transform="translate(%.1f %.1f)">' % (TX, sy))
S.append('<line x1="0" y1="0" x2="80" y2="0" stroke="%s" stroke-width="0.4"/>' % GTEC)
for k in range(4):
    if k % 2 == 0:
        S.append('<rect x="%d" y="-1.6" width="20" height="3.2" fill="%s"/>' % (k * 20, GTEC))
S.append('<text x="-1" y="7" font-size="2.6" fill="%s">0</text><text x="18" y="7" font-size="2.6" fill="%s">10</text><text x="38" y="7" font-size="2.6" fill="%s">20</text><text x="74" y="7" font-size="2.6" fill="%s">40 m</text>' % (GTEC, GTEC, GTEC, GTEC))
S.append('<text x="0" y="12.5" font-size="2.4" fill="#8a877f">escala 1:500 en A1 · norte arriba · base contexto: OpenStreetMap (ODbL)</text>')
S.append('</g>')

# creditos
S.append('<text x="%.1f" y="%.1f" font-size="2.6" fill="#8a877f">FASE 01 · 07-2026 · fuente: geometria_maestra.json (1 u = 1 m)</text>' % (TX, PH - MARG - 6))
S.append('<text x="%.1f" y="%.1f" font-size="5" fill="%s" font-family="Bahnschrift">P.01</text>' % (PW - MARG - 14, PH - MARG - 6, GTEC))

S.append('</svg>')
out = os.path.join(HERE, 'P01_PLANTA_GENERAL_500.svg')
open(out, 'w', encoding='utf-8').write('\n'.join(S))
print('OK ->', out)
