# -*- coding: utf-8 -*-
"""
P02 — AXONOMETRIA MAESTRA · REFUGIO CLIMATICO PUERTA DEL SOL
Lamina A1 apaisada · axonometria militar (planta verdadera, alturas reales, giro 32 grados).
Dibujo tecnico-diagramatico a linea desde geometria_maestra.json + cotas de geometria_3d.json.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, '..', '..', '01_BASE_GEOMETRICA', 'planta_maestra', 'geometria_maestra.json')
m = json.load(open(GEO, encoding='utf-8'))

TURQ, TURQD = '#3E969B', '#2E6E6B'
LIMA, VAGUA, VVEG, VALGA = '#C3D48A', '#8FC7AE', '#6F8F53', '#6E7A45'
ROSA, ROSAI, COBRE = '#E794AC', '#D6577F', '#B08968'
GPIEDRA, GCTX, GTEC = '#EDEAE4', '#B5B1A9', '#33322E'

PW, PH = 841.0, 594.0
MARG = 20.0
COL_W = 150.0
FIELD_X0, FIELD_Y0 = MARG, MARG
FIELD_W = PW - 2 * MARG - COL_W - 10
FIELD_H = PH - 2 * MARG

R = math.radians(32)
SC = 3.1          # mm por metro (~1:322, rotulada como axonometria sin escala + escala grafica)
LOOP_Z = {'C1-L1': 9.0, 'C1-L2': 7.0, 'C1-L3': 7.5, 'C2-L1': 10.0, 'C2-L2': 8.0,
          'C2-L3': 7.0, 'C3-L1': 9.0, 'C3-L2': 7.5}


def P(x, y, z=0.0):
    """proyeccion militar: planta girada R, z vertical verdadero"""
    xr = x * math.cos(R) - y * math.sin(R)
    yr = x * math.sin(R) + y * math.cos(R)
    return (xr * SC, -(yr * SC + z * SC))


# centrar la mancha
pts_test = []
for lp in m['estructura_principal']['loops']:
    pts_test += [P(lp['cx'] + dx, lp['cy'] + dy, 0) for dx in (-lp['rx'], lp['rx']) for dy in (-lp['ry'], lp['ry'])]
pts_test += [P(x, y, 0) for (x, y) in [(-110, -40), (95, -40), (-110, 70), (95, 70)]]
us = [p[0] for p in pts_test]
vs = [p[1] for p in pts_test]
OU = FIELD_X0 + FIELD_W / 2 - (min(us) + max(us)) / 2
OV = FIELD_Y0 + FIELD_H / 2 - (min(vs) + max(vs)) / 2 + 14


def T(x, y, z=0.0):
    u, v = P(x, y, z)
    return (u + OU, v + OV)


def path3(pts, z=0.0, close=False):
    s = 'M ' + ' L '.join('%.2f %.2f' % T(p[0], p[1], (p[2] if len(p) > 2 else z)) for p in pts)
    return s + (' Z' if close else '')


def ell(cx, cy, rx, ry, rot_deg, n=64):
    r = math.radians(rot_deg)
    return [(cx + rx * math.cos(2 * math.pi * i / n) * math.cos(r) - ry * math.sin(2 * math.pi * i / n) * math.sin(r),
             cy + rx * math.cos(2 * math.pi * i / n) * math.sin(r) + ry * math.sin(2 * math.pi * i / n) * math.cos(r))
            for i in range(n + 1)]


S = []
S.append('<svg xmlns="http://www.w3.org/2000/svg" width="841mm" height="594mm" viewBox="0 0 841 594" font-family="Arial">')
S.append('<rect width="841" height="594" fill="#FFFFFF"/>')
S.append('<clipPath id="field"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath>' % (FIELD_X0, FIELD_Y0, FIELD_W, FIELD_H))
S.append('<g clip-path="url(#field)">')

# ---------- SUELO ----------
# pavimento de la plaza (mancha libre aproximada) — poligono del vacio urbano
PLAZA = [(-96, -14), (-80, -26), (-40, -30), (10, -31), (40, -30), (78, -22), (88, 8), (86, 26),
         (60, 34), (40, 44), (20, 55), (0, 62), (-20, 52), (-45, 44), (-70, 32), (-90, 12)]
S.append('<path d="%s" fill="#F8F7F4" stroke="none"/>' % path3(PLAZA, 0, True))

# huellas de contexto proximas (solo linea)
for b in m['contexto']['buildings']:
    if len(b['pts']) >= 3:
        xs = [p[0] for p in b['pts']]
        ys = [p[1] for p in b['pts']]
        if -150 < min(xs) and max(xs) < 180 and -110 < min(ys) and max(ys) < 120:
            S.append('<path d="%s" fill="%s" fill-opacity="0.55" stroke="%s" stroke-width="0.10"/>' % (
                path3(b['pts'], 0, True), GPIEDRA, GCTX))
cc = m['contexto']['casa_correos']
S.append('<path d="%s" fill="#E7E3DB" stroke="#8E8A82" stroke-width="0.18"/>' % path3(cc['pts'], 0, True))
# volumen bajo de Casa de Correos (prisma de linea, 20 m)
for pt in cc['pts'][::6]:
    a0 = T(pt[0], pt[1], 0)
    a1 = T(pt[0], pt[1], 20)
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#B9B3A9" stroke-width="0.08"/>' % (a0[0], a0[1], a1[0], a1[1]))
S.append('<path d="%s" fill="none" stroke="#B9B3A9" stroke-width="0.13"/>' % path3(cc['pts'], 20, True))

# pasos libres
for c in m['circulacion']['corridors']:
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.10" stroke-dasharray="3 2.2"/>' % (path3(c['pts']), GCTX))

# arboles existentes y nuevos (planta a cota 0: circulo + tallo)
for t in m['contexto']['trees']:
    x, y = T(t['x'], t['y'], 0)
    xt, yt = T(t['x'], t['y'], 4.5)
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#9A9A8A" stroke-width="0.10"/>' % (x, y, xt, yt))
    S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="%s" stroke-width="0.10" opacity="0.8"/>' % (xt, yt, 2.0 * SC * 0.8, VVEG))
for (tx, ty) in m['paisaje']['new_trees']:
    x, y = T(tx, ty, 0)
    xt, yt = T(tx, ty, 5.0)
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#6F8F53" stroke-width="0.13"/>' % (x, y, xt, yt))
    S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" fill-opacity="0.35" stroke="%s" stroke-width="0.13"/>' % (xt, yt, 2.4 * SC * 0.8, VVEG, VVEG))

# jardineras y bancos
for p in m['paisaje']['planters']:
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.9" stroke-linecap="round" opacity="0.6"/>' % (path3(p['pts'], 0.4), VVEG))
for b in m['programa']['benches']:
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.6" stroke-linecap="round"/>' % (path3(b['pts'], 0.45), COBRE))

# estanques suelo + splash
for p in m['agua_clima']['ground_ponds']:
    if p['kind'] == 'circle':
        S.append('<path d="%s" fill="%s" fill-opacity="0.7" stroke="#2F7D57" stroke-width="0.13"/>' % (
            path3(ell(p['cx'], p['cy'], p['r'], p['r'], 0), 0.5, True), VALGA))
    else:
        S.append('<path d="%s" fill="%s" fill-opacity="0.7" stroke="#2F7D57" stroke-width="0.13"/>' % (path3(p['pts'], 0.5, True), VALGA))
sp = m['agua_clima']['splash']
S.append('<path d="%s" fill="#BFE9E4" fill-opacity="0.6" stroke="#63BFB4" stroke-width="0.10" stroke-dasharray="1.6 1.2"/>' % (
    path3(ell(sp['cx'], sp['cy'], sp['rx'], sp['ry'], sp['rot']), 0.05, True)))

# LAB
lab = m['programa']['lab']
S.append('<path d="%s" fill="#FFFFFF" fill-opacity="0.8" stroke="#D14E92" stroke-width="0.18" stroke-dasharray="2.2 1.6"/>' % path3(lab['pts'], 0, True))
S.append('<path d="%s" fill="none" stroke="#D14E92" stroke-width="0.13" stroke-dasharray="2.2 1.6"/>' % path3(lab['pts'], 4, True))
for pt in lab['pts'][::10]:
    a0, a1 = T(pt[0], pt[1], 0), T(pt[0], pt[1], 4)
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#D14E92" stroke-width="0.08"/>' % (a0[0], a0[1], a1[0], a1[1]))

# ---------- MASTILES ----------
for (mx, my) in m['estructura_ligera']['masts']:
    a0, a1 = T(mx, my, 0), T(mx, my, 7.5)
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#8A8A88" stroke-width="0.10"/>' % (a0[0], a0[1], a1[0], a1[1]))

# ---------- RED AGUA a +2.2 ----------
for w in m['agua_clima']['mains']:
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.30" stroke-dasharray="2.2 1.6" opacity="0.9"/>' % (path3(w, 2.2), ROSAI))

# ---------- DISCOS (por cota ascendente) ----------
for d in sorted(m['paisaje']['discs'], key=lambda q: q.get('cota', 6)):
    z = float(d.get('cota', 6))
    x, y = T(d['cx'], d['cy'], z)
    x0, y0 = T(d['cx'], d['cy'], 0)
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#9BB86A" stroke-width="0.07" opacity="0.5"/>' % (x0, y0, x, y))
    S.append('<path d="%s" fill="%s" fill-opacity="0.55" stroke="#8FB35B" stroke-width="0.13"/>' % (
        path3(ell(d['cx'], d['cy'], d['r'], d['r'], 0, 40), z, True), LIMA))

# ---------- BALSAS elevadas ----------
for p in m['agua_clima']['pools']:
    S.append('<path d="%s" fill="%s" fill-opacity="0.6" stroke="#4E9B6E" stroke-width="0.18"/>' % (
        path3(ell(p['cx'], p['cy'], p['rx'], p['ry'], p['rot']), p['cota'], True), VAGUA))
    for a in (30, 150, 270):
        px, py = ell(p['cx'], p['cy'], p['rx'] * 0.7, p['ry'] * 0.7, p['rot'], 3)[0]
    # bajante central
    a0, a1 = T(p['cx'], p['cy'], 0), T(p['cx'], p['cy'], p['cota'])
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#4E9B6E" stroke-width="0.10" stroke-dasharray="1 0.8"/>' % (a0[0], a0[1], a1[0], a1[1]))

# ---------- LOOPS ----------
for lp in m['estructura_principal']['loops']:
    z = LOOP_Z[lp['id']]
    w = 0.8 if lp['g'] == 'G1' else 0.55
    op = '1' if lp['g'] == 'G1' else '0.85'
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" stroke-opacity="%s"/>' % (
        path3(ell(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot']), z, True), TURQ, w, op))

# cupula geodesica: base + meridianos
dm = m['estructura_principal']['dome']
S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.25" stroke-opacity="0.9"/>' % (
    path3(ell(dm['cx'], dm['cy'], dm['r'], dm['r'], 0), 0, True), TURQ))
for k in range(5):
    zz = dm['r'] * math.sin((k + 1) * math.pi / 12)
    rr = dm['r'] * math.cos((k + 1) * math.pi / 12)
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.10" stroke-opacity="0.7"/>' % (
        path3(ell(dm['cx'], dm['cy'], rr, rr, 0, 40), zz, True), TURQ))

# ---------- CINTA ----------
rib = m['circulacion']['ribbon']
rib3 = [(x, y, 5.0 + 1.2 * math.sin(i * 0.12)) for i, (x, y) in enumerate(rib)]
S.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.7" stroke-linecap="round" stroke-opacity="0.95"/>' % (path3(rib3), TURQD))
S.append('<path d="%s" fill="none" stroke="#FFFFFF" stroke-width="0.35" stroke-opacity="0.9"/>' % path3(rib3))
for (sx0, sy0) in m['circulacion']['stairs']:
    a0, a1 = T(sx0, sy0, 0), T(sx0, sy0, 4.6)
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="0.35"/>' % (a0[0], a0[1], a1[0], a1[1], TURQD))

# ---------- CAPSULAS ----------
for c in sorted(m['programa']['capsules'], key=lambda q: {'suelo': 0, 'media': 1, 'alta': 2}.get(q.get('cota', 'suelo'), 0)):
    r = max(c['w'], c['h']) / 2
    z = {'suelo': r, 'media': 4.0, 'alta': 8.0}.get(c.get('cota', 'suelo'), r)
    x, y = T(c['cx'], c['cy'], z)
    if c.get('cota') == 'media':
        x0, y0 = T(c['cx'], c['cy'], 0)
        S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#D14E92" stroke-width="0.07" opacity="0.5"/>' % (x0, y0, x, y))
    S.append('<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="%s" fill-opacity="0.65" stroke="#D14E92" stroke-width="0.13"/>' % (
        x, y, c['w'] / 2 * SC, max(c['h'] / 2 * SC * 0.85, c['h'] / 2 * SC - 0.4), ROSA))

# ---------- DEPOSITOS ----------
for t in m['estructura_ligera']['tanks']:
    for k in range(t['n']):
        cx = t['cx'] + k * 2.6
        a0, a1 = T(cx, t['cy'], 0), T(cx, t['cy'], 10.5)
        S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#C23B7E" stroke-width="0.18"/>' % (a0[0], a0[1], a1[0], a1[1]))
        S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" fill-opacity="0.85" stroke="#C23B7E" stroke-width="0.13"/>' % (
            a1[0], a1[1], t['r'] * SC * 0.9, ROSAI))
for (dx, dy) in m['estructura_ligera']['drops']:
    x, y = T(dx, dy, 1.0)
    S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="#7FC7BD" stroke-width="0.13"/>' % (x, y, 0.8 * SC))

S.append('</g>')

# ---------- llamadas de familias ----------
def callout(x_m, y_m, z_m, tx_mm, ty_mm, text, color=GTEC):
    x, y = T(x_m, y_m, z_m)
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="0.10"/>' % (x, y, tx_mm, ty_mm, color))
    S.append('<circle cx="%.2f" cy="%.2f" r="0.7" fill="%s"/>' % (x, y, color))
    anchor = 'end' if tx_mm < x else 'start'
    S.append('<text x="%.1f" y="%.1f" font-size="2.7" fill="%s" text-anchor="%s" font-family="Arial" letter-spacing="0.4">%s</text>' % (
        tx_mm + (-2 if anchor == 'end' else 2), ty_mm - 1.2, color, anchor, text))


lp1 = m['estructura_principal']['loops'][0]
callout(lp1['cx'] - lp1['rx'] * 0.7, lp1['cy'] + lp1['ry'] * 0.6, 9, 135, 118, 'loops estructurales · anillos +7/10 m · G1-G2', TURQD)
callout(-2, 36, 6.2, 150, 88, 'cinta-recorrido continua +4/6 m · transitable · G2', TURQD)
d0 = max(m['paisaje']['discs'], key=lambda q: q['r'])
callout(d0['cx'], d0['cy'], d0.get('cota', 6), 105, 150, 'discos-canopy de microalgas +5/10 m · sombra y filtro · G2/G3', '#7A9A45')
callout(8, 13, 10.5, 300, 74, 'depósitos elevados +10 m · riego por gravedad · G3', '#C23B7E')
p0 = m['agua_clima']['pools'][4]
callout(p0['cx'], p0['cy'], p0['cota'], 470, 96, 'balsas de microalgas elevadas · G2', '#4E9B6E')
callout(72, 2, 2.0, 560, 420, 'tren de cápsulas neumáticas · bordes O y SE · G1', '#D14E92')
callout(30.5, 7, 5.5, 480, 470, 'cúpula geodésica · nudo central · G2', TURQD)
callout(17, -3, 0.05, 330, 480, 'lámina de agua jugable 1-2 cm · G3', '#63BFB4')
callout(-15, 4, 2.2, 130, 430, 'red hidráulica vista · G3', '#C23B7E')
callout(-52, 5, 0.4, 165, 452, 'suelo público continuo: jardineras-banco, estancia, juego', COBRE)
callout(-22, -60, 0, 250, 540, 'REAL CASA DE CORREOS · banda libre 15 m', '#8E8A82')

# ---------- marco + columna ----------
S.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s" stroke-width="0.13"/>' % (FIELD_X0, FIELD_Y0, FIELD_W, FIELD_H, GCTX))
CXL = FIELD_X0 + FIELD_W + 10
S.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.10"/>' % (CXL, MARG, CXL, PH - MARG, GCTX))
TX = CXL + 8


def col_text(y, text, size=3.2, color=GTEC, font='Arial', spacing=0, bold=False):
    S.append('<text x="%.1f" y="%.1f" font-size="%.1f" fill="%s" font-family="%s" letter-spacing="%s"%s>%s</text>' % (
        TX, y, size, color, font, spacing, ' font-weight="600"' if bold else '', text))


col_text(34, 'FASE 01 · DOCUMENTO PILOTO', 3.0, TURQD, 'Bahnschrift', 1.4)
col_text(46, 'REFUGIO CLIMÁTICO', 8.5, GTEC, 'Bahnschrift', 0.5, True)
col_text(56, 'PUERTA DEL SOL · MADRID', 5.2, GTEC, 'Bahnschrift', 0.8)
col_text(70, 'P.02 — AXONOMETRÍA MAESTRA', 5.0, TURQD, 'Bahnschrift', 1.0)
col_text(77, 'Sistema por estratos · axonometría militar 32° · alturas reales', 2.6, '#8a877f')

ly = 96
col_text(ly, 'ESTRATOS DEL SISTEMA', 3.0, TURQD, 'Bahnschrift', 1.4)
estratos = [
    ('+10–12 m', 'depósitos de agua · arcos de red rosa · puntos altos', ROSAI),
    ('+5–10 m', 'discos-canopy · balsas de microalgas · loops', TURQ),
    ('+4–6 m', 'cinta-recorrido transitable · cápsulas suspendidas', TURQD),
    ('+2–4 m', 'toros y cápsulas a media altura · red de riego', ROSA),
    ('±0 m', 'suelo público continuo: jardineras, estanques,', VVEG),
    ('', 'lámina jugable, bancos, arbolado, mangueras', VVEG),
]
for i, (cota, txt, col) in enumerate(estratos):
    yy = ly + 8 + i * 6.2
    if cota:
        S.append('<text x="%.1f" y="%.1f" font-size="3.0" fill="%s" font-family="Bahnschrift">%s</text>' % (TX, yy, col, cota))
    S.append('<text x="%.1f" y="%.1f" font-size="2.6" fill="%s" font-family="Arial">%s</text>' % (TX + 22, yy, GTEC, txt))

cy0 = ly + 8 + len(estratos) * 6.2 + 8
col_text(cy0, 'LECTURA', 3.0, TURQD, 'Bahnschrift', 1.4)
lectura = [
    'No hay forjados: todo el suelo sigue siendo plaza.',
    'La única circulación elevada es la cinta-recorrido.',
    'El agua desciende por gravedad: depósito → balsa →',
    'riego / nebulización / lámina jugable.',
    'La sombra es agua: cada disco es una lámina de',
    'cultivo de microalgas de 2–5 cm.',
    'Los monumentos y los cruces peatonales históricos',
    'permanecen como claros del sistema.',
]
for i, txt in enumerate(lectura):
    col_text(cy0 + 7 + i * 4.6, txt, 2.6)

dy0 = cy0 + 7 + len(lectura) * 4.6 + 8
col_text(dy0, 'CERTEZA GEOMÉTRICA', 3.0, TURQD, 'Bahnschrift', 1.4)
for i, (g, txt, dash, op) in enumerate([
        ('G1', 'confirmado', '', 1.0), ('G2', 'muy probable', '', 0.85),
        ('G3', 'inferido', 'stroke-dasharray="2.2 1.6"', 1.0), ('G4', 'reserva Fase 02', 'stroke-dasharray="0.5 1.2"', 1.0)]):
    yy = dy0 + 7 + i * 5.4
    S.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.6" opacity="%s" %s/>' % (TX, yy - 1, TX + 9, yy - 1, TURQD, op, dash))
    col_text(yy, '&#160;&#160;&#160;&#160;&#160;&#160;%s — %s' % (g, txt), 2.5)

# norte proyectado + escala grafica
nx, nyv = P(0, 1, 0)
L = math.hypot(nx, nyv)
nx, nyv = nx / L, nyv / L
gy = PH - MARG - 52
S.append('<g transform="translate(%.1f %.1f)">' % (TX + 10, gy))
S.append('<circle r="8" fill="none" stroke="%s" stroke-width="0.45"/>' % GTEC)
S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="0.45"/>' % (-6.5 * nx, -6.5 * nyv, 6.5 * nx, 6.5 * nyv, GTEC))
S.append('<path d="M %.2f %.2f L %.2f %.2f L %.2f %.2f" fill="none" stroke="%s" stroke-width="0.45"/>' % (
    6.5 * nx - 2.6 * nx - 1.6 * nyv, 6.5 * nyv - 2.6 * nyv + 1.6 * nx, 6.5 * nx, 6.5 * nyv,
    6.5 * nx - 2.6 * nx + 1.6 * nyv, 6.5 * nyv - 2.6 * nyv - 1.6 * nx, GTEC))
S.append('<text x="10" y="-6" font-size="4" fill="%s" font-family="Bahnschrift">N</text>' % GTEC)
S.append('</g>')
sy = PH - MARG - 32
S.append('<g transform="translate(%.1f %.1f)">' % (TX, sy))
S.append('<line x1="0" y1="0" x2="%.1f" y2="0" stroke="%s" stroke-width="0.4"/>' % (40 * SC, GTEC))
S.append('<rect x="0" y="-1.6" width="%.1f" height="3.2" fill="%s"/><rect x="%.1f" y="-1.6" width="%.1f" height="3.2" fill="%s"/>' % (
    10 * SC, GTEC, 20 * SC, 10 * SC, GTEC))
S.append('<text x="-1" y="7" font-size="2.6" fill="%s">0</text><text x="%.1f" y="7" font-size="2.6" fill="%s">10</text><text x="%.1f" y="7" font-size="2.6" fill="%s">20</text><text x="%.1f" y="7" font-size="2.6" fill="%s">40 m</text>' % (
    GTEC, 10 * SC - 2, GTEC, 20 * SC - 2, GTEC, 40 * SC - 4, GTEC))
S.append('<text x="0" y="12.5" font-size="2.4" fill="#8a877f">planta verdadera (militar) · alturas sin exagerar · escala gráfica en el plano horizontal</text>')
S.append('</g>')

S.append('<text x="%.1f" y="%.1f" font-size="2.6" fill="#8a877f">FASE 01 · 07-2026 · fuente: geometria_maestra.json + geometria_3d.json</text>' % (TX, PH - MARG - 6))
S.append('<text x="%.1f" y="%.1f" font-size="5" fill="%s" font-family="Bahnschrift">P.02</text>' % (PW - MARG - 14, PH - MARG - 6, GTEC))

S.append('</svg>')
out = os.path.join(HERE, 'P02_AXONOMETRIA_MAESTRA.svg')
open(out, 'w', encoding='utf-8').write('\n'.join(S))
print('OK ->', out)
