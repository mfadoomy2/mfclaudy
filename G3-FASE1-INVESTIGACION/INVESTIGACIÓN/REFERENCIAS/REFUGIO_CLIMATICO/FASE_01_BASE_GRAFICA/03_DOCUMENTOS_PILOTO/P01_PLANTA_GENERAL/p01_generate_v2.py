# -*- coding: utf-8 -*-
"""
P01 v2 — PLANTA GENERAL · REFUGIO CLIMATICO PUERTA DEL SOL
Regimen MAXIMALISTA (estetica iraxxxdios): desorden dentro del orden.
Misma geometria validada (geometria_maestra.json) + misma paleta del manual;
cambia la REPRESENTACION: enjambre de cotas, mallas, traviesas, cables, coordenadas,
garabatos vegetales, vapor, fauna, bloques de nota. A1 apaisada · 1:300 · norte arriba.
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
GEO_V2 = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'FASE_03B_MODELO_MAESTRO', 'geometria_maestra_v002.json'))
GEO = GEO_V2 if os.path.exists(GEO_V2) else os.path.join(HERE, '..', '..', '01_BASE_GEOMETRICA', 'planta_maestra', 'geometria_maestra.json')
m = json.load(open(GEO, encoding='utf-8'))
rng = random.Random(1926)

TURQ, TURQD = '#3E969B', '#2E6E6B'
LIMA, VAGUA, VVEG, VALGA = '#C3D48A', '#8FC7AE', '#6F8F53', '#6E7A45'
ROSA, ROSAI, COBRE = '#E794AC', '#D6577F', '#B08968'
GPIEDRA, GCTX, GTEC = '#EDEAE4', '#B5B1A9', '#33322E'
SPLASHC = '#63BFB4'

PW, PH = 841.0, 594.0
# LAMINA-ATLAS a sangre completa: el dibujo ES la lamina; la informacion vive dentro
FIELD_X0, FIELD_Y0 = 0.0, 0.0
FIELD_W, FIELD_H = PW, PH
SCALE = 3.6                     # ~1:278, rotulada 1:300 aprox — la plaza llena el A1
CX, CY = -6.0, 20.0


def T(p):
    return (FIELD_X0 + FIELD_W / 2 + (p[0] - CX) * SCALE,
            FIELD_Y0 + FIELD_H / 2 - (p[1] - CY) * SCALE)


def path_of(pts, close=False):
    s = 'M ' + ' L '.join('%.2f %.2f' % T(p) for p in pts)
    return s + (' Z' if close else '')


def ell(cx, cy, rx, ry, rot_deg, n=72, a0=0, a1=360):
    r = math.radians(rot_deg)
    out = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        x, y = rx * math.cos(a), ry * math.sin(a)
        out.append((cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)))
    return out


def on_ell(cx, cy, rx, ry, rot_deg, a_deg):
    r = math.radians(rot_deg)
    a = math.radians(a_deg)
    x, y = rx * math.cos(a), ry * math.sin(a)
    return (cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r))


S = []
S.append('<svg xmlns="http://www.w3.org/2000/svg" width="841mm" height="594mm" viewBox="0 0 841 594" font-family="Arial">')
S.append('<rect width="841" height="594" fill="#FFFFFF"/>')
S.append('<clipPath id="field"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath>' % (FIELD_X0, FIELD_Y0, FIELD_W, FIELD_H))

def catmull_rom(pts, seg=8):
    P0 = list(pts) + [pts[0], pts[1]]
    out = []
    for i in range(1, len(P0) - 2):
        p0, p1, p2, p3 = P0[i - 1], P0[i], P0[i + 1], P0[i + 2]
        for t in [j / seg for j in range(seg)]:
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((round(x, 2), round(y, 2)))
    return out


PLAZA_RAW = [(-96, -14), (-84, -24), (-60, -29), (-30, -31), (10, -31), (40, -30), (70, -25), (84, -16),
             (88, 4), (86, 22), (72, 28), (56, 34), (40, 44), (26, 50), (10, 57), (-4, 58), (-20, 52),
             (-34, 48), (-50, 42), (-66, 34), (-82, 22), (-92, 8)]
PLAZA = catmull_rom(PLAZA_RAW, 6)
S.append('<clipPath id="plaza"><path d="%s"/></clipPath>' % path_of(PLAZA, True))

S.append('<g clip-path="url(#field)">')

# ============================================================ CONTEXTO: masa + trama
S.append('<g id="ctx-masa">')
for b in m['contexto']['buildings']:
    if len(b['pts']) >= 3:
        S.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.07"/>' % (path_of(b['pts'], True), GPIEDRA, '#DDD8D0'))
S.append('</g>')
# trama 45 sobre el contexto (clip por edificios via mascara simple: rayas sobre todo, luego plaza en blanco)
S.append('<g id="ctx-hatch" stroke="#D5CFC5" stroke-width="0.06" opacity="0.6">')
for k in range(-80, 260):
    x0 = FIELD_X0 - 250 + k * 3.4
    S.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (x0, FIELD_Y0 + FIELD_H + 5, x0 + FIELD_H + 10, FIELD_Y0 - 5))
S.append('</g>')
# la plaza vuelve a blanco
S.append('<path d="%s" fill="#FFFFFF"/>' % path_of(PLAZA, True))
# calles: vuelven a blanco sobre la trama
S.append('<g stroke="#FFFFFF" stroke-width="2.8" fill="none" stroke-linecap="round">')
for h in m['contexto']['highways']:
    S.append('<path d="%s"/>' % path_of(h['pts']))
S.append('</g>')
S.append('<g stroke="#C9C3B8" stroke-width="0.08" fill="none">')
for h in m['contexto']['highways']:
    S.append('<path d="%s"/>' % path_of(h['pts']))
S.append('</g>')
# contorno de manzana por encima de la trama
S.append('<g id="ctx-borde" fill="none" stroke="#B9B3A8" stroke-width="0.09">')
for b in m['contexto']['buildings']:
    if len(b['pts']) >= 3:
        S.append('<path d="%s"/>' % path_of(b['pts'], True))
S.append('</g>')
cc = m['contexto']['casa_correos']
S.append('<path d="%s" fill="#E7E2D9" stroke="#8E8A82" stroke-width="0.30"/>' % path_of(cc['pts'], True))

# ---- borde-regla del vacio de plaza (muralla con ticks rojos) ----
S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.5"/>' % (path_of(PLAZA, True), GTEC))
S.append('<g stroke="%s" stroke-width="0.10">' % ROSAI)
per_pts = []
for i in range(len(PLAZA)):
    a = PLAZA[i]
    b = PLAZA[(i + 1) % len(PLAZA)]
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    n = max(2, int(L / 2.2))
    for k in range(n):
        t = k / n
        px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        nx, ny = (b[1] - a[1]) / L, -(b[0] - a[0]) / L
        p1 = T((px, py))
        p2 = T((px + nx * 1.1, py + ny * 1.1))
        S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (p1[0], p1[1], p2[0], p2[1]))
    per_pts.append((a, b, L))
S.append('</g>')
# cadena de cotas perimetrales
S.append('<g font-size="1.5" fill="%s">' % ROSAI)
for (a, b, L) in per_pts:
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    nx, ny = (b[1] - a[1]) / L, -(b[0] - a[0]) / L
    p = T((mx + nx * 2.8, my + ny * 2.8))
    ang = -math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    S.append('<text x="%.1f" y="%.1f" text-anchor="middle" transform="rotate(%.1f %.1f %.1f)">%.2f</text>' % (
        p[0], p[1], ang, p[0], p[1], L))
S.append('</g>')

# ---- despiece de pavimento (bandas finas siguiendo el eje de la plaza) ----
S.append('<g clip-path="url(#plaza)" stroke="#D8D3CA" stroke-width="0.05" opacity="0.85">')
ang = math.radians(7)
for k in range(-70, 75):
    off = k * 1.8
    x0, y0 = -120, off - 120 * math.tan(ang)
    x1, y1 = 120, off + 120 * math.tan(ang)
    p0, p1 = T((x0, y0)), T((x1, y1))
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (p0[0], p0[1], p1[0], p1[1]))
S.append('</g>')

# ---- arboles existentes: garabatos grises ----
def scribble(cx, cy, r, col, w, jitter=0.5, turns=26, op=0.9):
    pts = []
    a = rng.uniform(0, 6.28)
    for i in range(turns):
        a += rng.uniform(0.6, 1.7)
        rr = r * (0.25 + 0.75 * rng.random())
        pts.append((cx + rr * math.cos(a) + rng.uniform(-jitter, jitter),
                    cy + rr * math.sin(a) + rng.uniform(-jitter, jitter)))
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" opacity="%.2f" stroke-linejoin="round"/>' % (
        path_of(pts), col, w, op))


for t in m['contexto']['trees']:
    scribble(t['x'], t['y'], 2.1, '#A9B29B', 0.09, 0.5, 22, 0.8)
    p = T((t['x'], t['y']))
    S.append('<circle cx="%.2f" cy="%.2f" r="0.3" fill="#8E9B82"/>' % (p[0], p[1]))

# metro
for e in m['contexto']['metro']:
    x, y = T((e['x'], e['y']))
    S.append('<rect x="%.2f" y="%.2f" width="5" height="5" fill="#FFFFFF" stroke="#5B5B8F" stroke-width="0.22"/>' % (x - 2.5, y - 2.5))
    S.append('<path d="M %.2f %.2f v -2.6 l 1.3 1.6 1.3 -1.6 v 2.6" fill="none" stroke="#5B5B8F" stroke-width="0.18"/>' % (x - 1.3, y + 1.3))
    if e.get('name'):
        S.append('<text x="%.1f" y="%.1f" font-size="1.6" fill="#5B5B8F">%s</text>' % (x + 3.2, y + 0.6, e['name']))

# pasos libres
S.append('<g fill="none" stroke="#9A9A92" stroke-width="0.14" stroke-dasharray="3.4 2.4">')
for c in m['circulacion']['corridors']:
    S.append('<path d="%s"/>' % path_of(c['pts']))
S.append('</g>')

# ============================================================ CAPAS DE PROYECTO
# ---- vegetacion nueva: garabatos densos + campos de puntos ----
for (tx, ty) in m['paisaje']['new_trees']:
    scribble(tx, ty, 2.7, VVEG, 0.13, 0.6, 30, 0.9)
    scribble(tx, ty, 1.6, '#4E7040', 0.09, 0.4, 16, 0.85)
for p in m['paisaje']['planters']:
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round" opacity="0.8"/>' % (
        path_of(p['pts']), VVEG, 1.4 * SCALE * 0.45))
    # matas punteadas a lo largo
    for q in p['pts'][::3]:
        if rng.random() < 0.8:
            for _ in range(7):
                px = q[0] + rng.uniform(-1.6, 1.6)
                py = q[1] + rng.uniform(-1.6, 1.6)
                pp = T((px, py))
                S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" opacity="0.6"/>' % (pp[0], pp[1], rng.uniform(0.12, 0.3), VVEG))

# ---- balsas y estanques con oleaje ----
for p in m['agua_clima']['pools']:
    e0 = ell(p['cx'], p['cy'], p['rx'], p['ry'], p['rot'])
    S.append('<path d="%s" fill="%s" fill-opacity="0.5" stroke="#4E9B6E" stroke-width="0.22"/>' % (path_of(e0, True), VAGUA))
    for f in (0.75, 0.5, 0.28):
        S.append('<path d="%s" fill="none" stroke="#4E9B6E" stroke-width="0.07" opacity="0.8"/>' % (
            path_of(ell(p['cx'], p['cy'], p['rx'] * f, p['ry'] * f, p['rot'] + rng.uniform(-6, 6)), True)))
    lbl = T((p['cx'], p['cy'] - p['ry'] - 1.6))
    S.append('<text x="%.1f" y="%.1f" font-size="1.6" fill="#4E9B6E" text-anchor="middle">%s · +%.1f · lám 2-5 cm</text>' % (
        lbl[0], lbl[1], p['id'], p['cota']))
for p in m['agua_clima']['ground_ponds']:
    if p['kind'] == 'circle':
        x, y = T((p['cx'], p['cy']))
        S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" fill-opacity="0.66" stroke="#2F7D57" stroke-width="0.2"/>' % (x, y, p['r'] * SCALE, VALGA))
        S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="#FFFFFF" stroke-width="0.09" opacity="0.6"/>' % (x, y, (p['r'] - 0.7) * SCALE))
        S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="#FFFFFF" stroke-width="0.07" opacity="0.45"/>' % (x, y, (p['r'] - 1.4) * SCALE))
    else:
        S.append('<path d="%s" fill="%s" fill-opacity="0.66" stroke="#2F7D57" stroke-width="0.2" stroke-dasharray="2.6 1.8"/>' % (path_of(p['pts'], True), VALGA))
sp = m['agua_clima']['splash']
S.append('<path d="%s" fill="#BFE9E4" fill-opacity="0.55" stroke="%s" stroke-width="0.14" stroke-dasharray="1.4 1"/>' % (
    path_of(ell(sp['cx'], sp['cy'], sp['rx'], sp['ry'], sp['rot']), True), SPLASHC))
for _ in range(46):
    a = rng.uniform(0, 6.28)
    rr = math.sqrt(rng.random())
    px = sp['cx'] + rr * sp['rx'] * 0.92 * math.cos(a)
    py = sp['cy'] + rr * sp['ry'] * 0.92 * math.sin(a)
    pp = T((px, py))
    S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" opacity="0.55"/>' % (pp[0], pp[1], rng.uniform(0.1, 0.35), SPLASHC))

# ---- discos-canopy: mallas radiales ----
for d in m['paisaje']['discs']:
    x, y = T((d['cx'], d['cy']))
    r = d['r'] * SCALE
    S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" fill-opacity="0.5" stroke="#8FB35B" stroke-width="0.16"/>' % (x, y, r, LIMA))
    nrad = 10 if d['r'] > 2.4 else 8
    for k in range(nrad):
        a = 2 * math.pi * k / nrad + 0.3
        S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#8FB35B" stroke-width="0.06" opacity="0.85"/>' % (
            x, y, x + r * math.cos(a), y + r * math.sin(a)))
    for f in (0.62, 0.3):
        S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="#8FB35B" stroke-width="0.06" opacity="0.85"/>' % (x, y, r * f))
    S.append('<circle cx="%.2f" cy="%.2f" r="0.35" fill="#6E8B3D"/>' % (x, y))

# ---- redes tensadas dentro de los loops grandes (malla en sector) ----
def net(lp, a0, a1, f_in=0.45, nn=9):
    ptsA = [on_ell(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'], a0 + (a1 - a0) * i / nn) for i in range(nn + 1)]
    ptsB = [on_ell(lp['cx'], lp['cy'], lp['rx'] * f_in, lp['ry'] * f_in, lp['rot'], a0 + (a1 - a0) * i / nn) for i in range(nn + 1)]
    S.append('<g stroke="%s" stroke-width="0.07" opacity="0.8" fill="none">' % TURQ)
    for i in range(nn + 1):
        pa, pb = T(ptsA[i]), T(ptsB[i])
        S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (pa[0], pa[1], pb[0], pb[1]))
        if i < nn:
            pa2, pb2 = T(ptsA[i + 1]), T(ptsB[i + 1])
            S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (pa[0], pa[1], pb2[0], pb2[1]))
            S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (pb[0], pb[1], pa2[0], pa2[1]))
    for pt in ptsA + ptsB:
        pp = T(pt)
        S.append('<circle cx="%.2f" cy="%.2f" r="0.16" fill="%s" stroke="none"/>' % (pp[0], pp[1], TURQ))
    S.append('</g>')


LOOPS = m['estructura_principal']['loops']
net(LOOPS[0], 150, 260)
net(LOOPS[3], -30, 80)
net(LOOPS[6], 120, 230)

# ---- LOOPS: haz de anillos + traviesas + mastiles + cotas ----
for lp in LOOPS:
    g1 = lp['g'] == 'G1'
    for off, w, op in ((0.9, 0.30, 0.95), (0.0, 0.5 if g1 else 0.34, 1.0), (-0.9, 0.30, 0.95)):
        S.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" stroke-opacity="%.2f"/>' % (
            path_of(ell(lp['cx'], lp['cy'], lp['rx'] + off, lp['ry'] + off, lp['rot']), True), TURQ, w, op))
    per = int(2 * math.pi * (lp['rx'] + lp['ry']) / 2 / 2.0)
    for k in range(per):
        a = 360 * k / per
        pa = T(on_ell(lp['cx'], lp['cy'], lp['rx'] + 0.9, lp['ry'] + 0.9, lp['rot'], a))
        pb = T(on_ell(lp['cx'], lp['cy'], lp['rx'] - 0.9, lp['ry'] - 0.9, lp['rot'], a))
        S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="0.09"/>' % (pa[0], pa[1], pb[0], pb[1], TURQ))
    # cotas de diametro
    for adeg in (25, 205):
        p0 = T(on_ell(lp['cx'], lp['cy'], lp['rx'] + 2.6, lp['ry'] + 2.6, lp['rot'], adeg))
        S.append('<text x="%.1f" y="%.1f" font-size="1.7" fill="%s" text-anchor="middle">%s · Ø%.0f×%.0f · %s</text>' % (
            p0[0], p0[1], ROSAI, lp['id'], lp['rx'] * 2, lp['ry'] * 2, lp['g']))

dm = m['estructura_principal']['dome']
x, y = T((dm['cx'], dm['cy']))
R = dm['r'] * SCALE
S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="%s" stroke-width="0.3"/>' % (x, y, R, TURQ))
for k in range(12):
    a = math.pi * k / 6
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="0.07"/>' % (
        x - R * math.cos(a), y - R * math.sin(a), x + R * math.cos(a), y + R * math.sin(a), TURQ))
for f in (0.8, 0.55, 0.28):
    S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="%s" stroke-width="0.07"/>' % (x, y, R * f, TURQ))

# ---- mastiles + abanicos de cables ----
MASTS = m['estructura_ligera']['masts']
for (mx, my) in MASTS:
    p = T((mx, my))
    S.append('<circle cx="%.2f" cy="%.2f" r="0.42" fill="#FFFFFF" stroke="#6B6B68" stroke-width="0.14"/>' % (p[0], p[1]))
    S.append('<circle cx="%.2f" cy="%.2f" r="0.12" fill="#6B6B68"/>' % (p[0], p[1]))
DISCS = m['paisaje']['discs']
for (mx, my) in MASTS[::2]:
    near = sorted(DISCS, key=lambda dd: (dd['cx'] - mx) ** 2 + (dd['cy'] - my) ** 2)[:3]
    p0 = T((mx, my))
    for dd in near:
        if (dd['cx'] - mx) ** 2 + (dd['cy'] - my) ** 2 < 130:
            p1 = T((dd['cx'], dd['cy']))
            S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#8A8A85" stroke-width="0.05" opacity="0.75"/>' % (
                p0[0], p0[1], p1[0], p1[1]))

# ---- CINTA: doble carril + traviesas + coordenadas ----
rib = m['circulacion']['ribbon']


def offset_poly(pts, off):
    out = []
    n = len(pts)
    for i in range(n):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        out.append((pts[i][0] - dy / L * off, pts[i][1] + dx / L * off))
    return out


ribA = offset_poly(rib, 1.0)
ribB = offset_poly(rib, -1.0)
S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.34"/>' % (path_of(ribA), TURQD))
S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.34"/>' % (path_of(ribB), TURQD))
S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.10" stroke-dasharray="1.2 1.2"/>' % (path_of(rib), TURQD))
for i in range(0, len(rib) - 1, 2):
    pa, pb = T(ribA[i]), T(ribB[i])
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="0.10"/>' % (pa[0], pa[1], pb[0], pb[1], TURQD))
# coordenadas reales cosidas al recorrido
S.append('<g font-size="1.35" fill="%s">' % ROSAI)
for i in range(4, len(rib) - 4, 11):
    x0, y0 = rib[i]
    z = 5.0 + 1.2 * math.sin(i * 0.12)
    dx = rib[i + 1][0] - rib[i - 1][0]
    dy = rib[i + 1][1] - rib[i - 1][1]
    angt = -math.degrees(math.atan2(dy, dx))
    if angt > 90 or angt < -90:
        angt += 180
    p = T((x0 - dy * 0.06, y0 + dx * 0.06))
    S.append('<text x="%.1f" y="%.1f" transform="rotate(%.1f %.1f %.1f)">%.0f %.0f +%.1f</text>' % (
        p[0], p[1], angt, p[0], p[1], x0, y0, z))
S.append('</g>')
for (sx0, sy0) in m['circulacion']['stairs']:
    x, y = T((sx0, sy0))
    S.append('<g transform="rotate(20 %.2f %.2f)">' % (x, y))
    for k in range(5):
        S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="0.12"/>' % (
            x - 2.4 + k * 1.2, y - 1.5, x - 2.4 + k * 1.2, y + 1.5, TURQD))
    S.append('</g>')

# ---- red hidraulica + goteo + nebulizadores con abanico ----
for w in m['agua_clima']['mains']:
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.30" stroke-dasharray="2.6 1.4"/>' % (path_of(w), ROSAI))
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.10"/>' % (path_of(offset_poly(w, 0.45)), ROSA))
for (nx, ny) in m['agua_clima']['nebul']:
    p = T((nx, ny))
    S.append('<circle cx="%.2f" cy="%.2f" r="0.28" fill="%s"/>' % (p[0], p[1], ROSAI))
    for adeg in (-35, 0, 35):
        a = math.radians(adeg - 90)
        S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="0.06" opacity="0.8"/>' % (
            p[0], p[1], p[0] + 1.5 * math.cos(a), p[1] + 1.5 * math.sin(a), ROSAI))

# ---- vapor: espirales + halos punteados sobre C1/C2/C3 ----
def vapor(cx, cy, rad):
    for _ in range(3):
        pts = []
        a = rng.uniform(0, 6.28)
        rr = 0.4
        px, py = cx + rng.uniform(-3, 3), cy + rng.uniform(-3, 3)
        for i in range(30):
            a += 0.55
            rr += 0.16
            pts.append((px + rr * math.cos(a), py + rr * math.sin(a)))
        S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.09" opacity="0.6"/>' % (path_of(pts), SPLASHC))
    for _ in range(int(rad * 14)):
        a = rng.uniform(0, 6.28)
        rr = rad * math.sqrt(rng.random())
        p = T((cx + rr * math.cos(a) * 1.3, cy + rr * math.sin(a)))
        S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" opacity="%.2f"/>' % (
            p[0], p[1], rng.uniform(0.08, 0.3), SPLASHC, rng.uniform(0.15, 0.45)))


vapor(-52, 12, 6)
vapor(6, 20, 8)
vapor(58, 10, 5)

# ---- capsulas: gajos + valvula + amarres ----
for c in m['programa']['capsules']:
    x, y = T((c['cx'], c['cy']))
    w2, h2 = c['w'] * SCALE, c['h'] * SCALE
    rot = -c.get('rot', 0)
    S.append('<g transform="rotate(%.1f %.2f %.2f)">' % (rot, x, y))
    S.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s" fill-opacity="0.6" stroke="#D14E92" stroke-width="0.16"/>' % (
        x - w2 / 2, y - h2 / 2, w2, h2, h2 / 2, ROSA))
    for f in (-0.25, 0, 0.25):
        S.append('<path d="M %.2f %.2f C %.2f %.2f %.2f %.2f %.2f %.2f" fill="none" stroke="#D14E92" stroke-width="0.07" opacity="0.9"/>' % (
            x + w2 * f, y - h2 / 2, x + w2 * f - 0.5, y, x + w2 * f + 0.5, y, x + w2 * f, y + h2 / 2))
    S.append('<circle cx="%.2f" cy="%.2f" r="0.2" fill="#B03A73"/>' % (x, y - h2 / 2 + 0.4))
    S.append('</g>')

# ---- depositos: doble anillo + radios + bajante ----
for t in m['estructura_ligera']['tanks']:
    for k in range(t['n']):
        x, y = T((t['cx'] + k * 2.6, t['cy']))
        r = t['r'] * SCALE
        S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" fill-opacity="0.85" stroke="#C23B7E" stroke-width="0.18"/>' % (x, y, r, ROSAI))
        S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="#FFFFFF" stroke-width="0.09"/>' % (x, y, r * 0.6))
        for kk in range(6):
            a = math.pi * kk / 3
            S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#FFFFFF" stroke-width="0.07"/>' % (
                x, y, x + r * 0.92 * math.cos(a), y + r * 0.92 * math.sin(a)))
    p0 = T((t['cx'], t['cy']))
    S.append('<text x="%.1f" y="%.1f" font-size="1.6" fill="%s" text-anchor="middle">%s +10.5 · 2×Ø%.1f</text>' % (
        p0[0], p0[1] - t['r'] * SCALE - 1.4, ROSAI, t['id'], t['r'] * 2))
for (dx, dy) in m['estructura_ligera']['drops']:
    x, y = T((dx, dy))
    S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="#7FC7BD" stroke-width="0.16"/>' % (x, y, 0.8 * SCALE))
    S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="#7FC7BD" stroke-width="0.07"/>' % (x, y, 0.5 * SCALE))

# ---- LAB + bancos ----
lab = m['programa']['lab']
S.append('<path d="%s" fill="#FFFFFF" fill-opacity="0.85" stroke="#D14E92" stroke-width="0.26" stroke-dasharray="2.6 1.8"/>' % path_of(lab['pts'], True))
S.append('<path d="%s" fill="none" stroke="#D14E92" stroke-width="0.08"/>' % path_of([(p[0], p[1]) for p in offset_poly(lab['pts'], 0.8)], True))
labc = T((51, 26))
S.append('<text x="%.1f" y="%.1f" font-size="1.9" fill="#D14E92" text-anchor="middle" letter-spacing="0.5">LAB 02 · MICROALGAE RESEARCH · G3</text>' % (labc[0], labc[1]))
for b in m['programa']['benches']:
    S.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.55" stroke-linecap="round"/>' % (path_of(b['pts']), COBRE))
    S.append('<path d="%s" fill="none" stroke="#FFFFFF" stroke-width="0.10"/>' % path_of(b['pts']))

# ---- hitos ----
hit = m['contexto']['hitos']
for key, lbl in [('carlos_iii', 'CARLOS III'), ('mariblanca', 'MARIBLANCA'), ('km0', 'KM 0'), ('oso_madrono', 'OSO Y MADROÑO')]:
    x, y = T(hit[key])
    S.append('<circle cx="%.2f" cy="%.2f" r="1.1" fill="%s"/><circle cx="%.2f" cy="%.2f" r="2.3" fill="none" stroke="%s" stroke-width="0.1"/><circle cx="%.2f" cy="%.2f" r="3.1" fill="none" stroke="%s" stroke-width="0.06" stroke-dasharray="0.7 0.7"/>' % (
        x, y, GTEC, x, y, GTEC, x, y, GTEC))
    S.append('<text x="%.1f" y="%.1f" font-size="1.7" fill="%s" text-anchor="middle" letter-spacing="0.8">%s</text>' % (x, y + 5.2, GTEC, lbl))

# ---- enjambre de micro-cotas entre elementos (distancias reales) ----
S.append('<g stroke="%s" stroke-width="0.07" fill="%s" font-size="1.35">' % (ROSAI, ROSAI))
anchors = [(d['cx'], d['cy']) for d in DISCS[::2]]
anchors += [(c['cx'], c['cy']) for c in m['programa']['capsules'][::3]]
anchors += MASTS[::5]
for _ in range(110):
    a = anchors[rng.randrange(len(anchors))]
    b = anchors[rng.randrange(len(anchors))]
    dxy = math.hypot(b[0] - a[0], b[1] - a[1])
    if 3.5 < dxy < 16:
        pa, pb = T(a), T(b)
        S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" opacity="0.55"/>' % (pa[0], pa[1], pb[0], pb[1]))
        for (px, py) in (pa, pb):
            S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" opacity="0.8"/>' % (px - 0.5, py - 0.5, px + 0.5, py + 0.5))
        mx0, my0 = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
        angd = -math.degrees(math.atan2(pb[1] - pa[1], pb[0] - pa[0]))
        if angd > 90 or angd < -90:
            angd += 180
        S.append('<text x="%.1f" y="%.1f" text-anchor="middle" transform="rotate(%.1f %.1f %.1f)">%.2f</text>' % (
            mx0, my0 - 0.4, angd, mx0, my0, dxy))
S.append('</g>')

# ---- etiquetas de cota de discos (muestra) ----
S.append('<g font-size="1.35" fill="#6E8B3D">')
for d in DISCS[::4]:
    p = T((d['cx'] + d['r'] * 0.5, d['cy'] + d['r'] * 0.5))
    S.append('<text x="%.1f" y="%.1f">Ø%.1f +%.1f</text>' % (p[0], p[1], d['r'] * 2, d.get('cota', 6)))
S.append('</g>')

# ---- fauna y figuras ----
def person(px, py):
    p = T((px, py))
    S.append('<g stroke="%s" stroke-width="0.10" fill="none"><circle cx="%.2f" cy="%.2f" r="0.28" fill="%s" stroke="none"/><line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/><line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/><line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/></g>' % (
        GTEC, p[0], p[1] - 0.8, GTEC,
        p[0], p[1] - 0.5, p[0], p[1] + 0.4,
        p[0], p[1] + 0.4, p[0] - 0.35, p[1] + 1.0,
        p[0], p[1] + 0.4, p[0] + 0.35, p[1] + 1.0))


def swift(px, py, s=1.0):
    p = T((px, py))
    S.append('<path d="M %.2f %.2f q %.2f %.2f %.2f %.2f q %.2f %.2f %.2f %.2f" fill="none" stroke="%s" stroke-width="0.12"/>' % (
        p[0] - 1.6 * s, p[1], 1.2 * s, -1.1 * s, 1.6 * s, 0, 0.4 * s, -1.1 * s, 1.6 * s, 0, GTEC))


def dragonfly(px, py):
    p = T((px, py))
    S.append('<g stroke="%s" stroke-width="0.09" fill="none">' % GTEC)
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (p[0], p[1] - 1.1, p[0], p[1] + 1.3))
    for sgn in (-1, 1):
        S.append('<ellipse cx="%.2f" cy="%.2f" rx="1.15" ry="0.3" transform="rotate(%d %.2f %.2f)"/>' % (
            p[0] + sgn * 1.1, p[1] - 0.4, sgn * 18, p[0] + sgn * 1.1, p[1] - 0.4))
        S.append('<ellipse cx="%.2f" cy="%.2f" rx="0.95" ry="0.26" transform="rotate(%d %.2f %.2f)"/>' % (
            p[0] + sgn * 0.95, p[1] + 0.25, sgn * -14, p[0] + sgn * 0.95, p[1] + 0.25))
    S.append('</g>')


for (px, py) in [(-70, -8), (-44, -14), (-20, -20), (2, -16), (26, -20), (48, -16), (-2, 34), (14, 44),
                 (-36, 38), (60, 24), (-88, 4), (34, 6), (10, 6), (-14, 22), (74, 0), (-60, 26)]:
    person(px + rng.uniform(-1.5, 1.5), py + rng.uniform(-1.5, 1.5))
for (px, py) in [(-30, 52), (-6, 56), (30, 48), (66, 30), (-70, 34), (18, 62)]:
    swift(px, py, rng.uniform(0.8, 1.3))
for (px, py) in [(-38, 20), (20, 28), (52, 2), (30, -4)]:
    dragonfly(px, py)

# ---- bloques de nota flotantes ----
def note(x_m, y_m, lines, color=GTEC, lead_to=None):
    x, y = T((x_m, y_m))
    if lead_to:
        p2 = T(lead_to)
        S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="0.09"/>' % (x, y, p2[0], p2[1], color))
        S.append('<circle cx="%.2f" cy="%.2f" r="0.5" fill="%s"/>' % (p2[0], p2[1], color))
    for i, ln in enumerate(lines):
        S.append('<text x="%.1f" y="%.1f" font-size="1.7" fill="%s" font-family="Consolas, monospace">%s</text>' % (
            x, y + i * 2.3, color, ln))


note(-104, -32, ['C1 · GRAN LOOP OESTE', 'Ø52×40 · 14 discos · 2 balsas', 'tren T-O 12 caps · red tensada', 'mastiles c/6.5 · nebul x14'], TURQD, (-72, 2))
note(-16, 72, ['C2 · NUDO CENTRAL · anillo doble', 'Ø42/28 · 21 discos · vapor max', 'cupula geodesica Ø13 · G2', 'racimo N 6 caps · deposito D-C2'], TURQD, (2, 34))
note(78, 48, ['C3 · ESTE · 2 loops solapados', 'balsas mayores 10×6 · LAB 02', 'tren T-SE 13 caps en U · G1', 'viveros + racimo NE'], TURQD, (62, 22))
note(-104, 56, ['CINTA-RECORRIDO', 'desarrollo 480 m · 6 bucles', 'cota +4/6 · ancho 2.5', 'coordenadas x y +z en m'], '#1B5E5A', (-52, 30))
note(36, -44, ['AGUA POR GRAVEDAD', 'deposito +10.5 → balsa +6/8', '→ riego/nebulizacion/lamina 0', 'red rosa vista Ø90-160 mm'], '#C23B7E', (14, -8))

# ---- grid topografico de esquina (+ cruces) ----
S.append('<g stroke="#B9C4CE" stroke-width="0.07" opacity="0.8">')
for gx in range(-100, 101, 20):
    for gy in range(-40, 81, 20):
        p = T((gx, gy))
        if FIELD_X0 + 4 < p[0] < FIELD_X0 + FIELD_W - 4 and FIELD_Y0 + 4 < p[1] < FIELD_Y0 + FIELD_H - 4:
            S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/><line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (
                p[0] - 1.1, p[1], p[0] + 1.1, p[1], p[0], p[1] - 1.1, p[0], p[1] + 1.1))
S.append('</g>')

# ---- rotulos de calles ----
def label(x_m, y_m, text, size=2.6, color='#A5A199', rot=0, spacing=0.8):
    x, y = T((x_m, y_m))
    tr = ' transform="rotate(%.1f %.1f %.1f)"' % (rot, x, y) if rot else ''
    S.append('<text x="%.1f" y="%.1f" font-size="%.1f" fill="%s" text-anchor="middle" letter-spacing="%.1f"%s>%s</text>' % (
        x, y, size, color, spacing, tr, text))


label(-22, -52, 'REAL CASA DE CORREOS', 3.0, '#8E8A82')
label(-22, -56.4, 'PRESIDENCIA DE LA COMUNIDAD DE MADRID · RELOJ · KM 0', 1.7, '#A5A199')
label(-100, 30, 'CALLE DEL ARENAL', 2.2, '#A5A199', -16)
label(-40, 72, 'CALLE DE PRECIADOS', 2.2, '#A5A199', 72)
label(1, 84, 'CALLE DEL CARMEN', 2.2, '#A5A199', 88)
label(41, 80, 'CALLE DE LA MONTERA', 2.2, '#A5A199', -72)
label(98, 22, 'CALLE DE ALCALÁ', 2.2, '#A5A199', -10)
label(96, -28, 'CARRERA DE SAN JERÓNIMO', 2.0, '#A5A199', -20)
label(24, -46, 'ESPOZ Y MINA', 1.9, '#A5A199', 83)
label(46, -48, 'CARRETAS', 1.9, '#A5A199', 80)
label(-104, -22, 'CALLE MAYOR', 2.2, '#A5A199', -10)

S.append('</g>')  # fin field clip

# ============================================================ INFORMACION DENTRO DE LA LAMINA
# ---- regla de coordenadas en el filo superior (sin marco) ----
S.append('<g font-size="1.6" fill="#8a96a4">')
for gx in range(-120, 121, 20):
    p = T((gx, 0))
    if 8 < p[0] < PW - 8:
        S.append('<line x1="%.1f" y1="2" x2="%.1f" y2="4.4" stroke="#8a96a4" stroke-width="0.1"/>' % (p[0], p[0]))
        S.append('<text x="%.1f" y="7.6" text-anchor="middle">%d</text>' % (p[0], gx))
for gy in range(-60, 101, 20):
    p = T((0, gy))
    if 8 < p[1] < PH - 14:
        S.append('<line x1="2" y1="%.1f" x2="4.4" y2="%.1f" stroke="#8a96a4" stroke-width="0.1"/>' % (p[1], p[1]))
        S.append('<text x="5.6" y="%.1f">%d</text>' % (p[1] + 0.6, gy))
S.append('</g>')

# ---- TITULO como acontecimiento tipografico (arriba-izquierda, film a sangre) ----
S.append('<path d="M 0 14 L 302 14 L 296 92 L 0 96 Z" fill="#FFFFFF" fill-opacity="0.82"/>')
S.append('<line x1="0" y1="14.6" x2="301" y2="14.6" stroke="%s" stroke-width="0.45"/>' % ROSAI)
S.append('<text x="16" y="26" font-size="3.4" fill="%s" font-family="Bahnschrift" letter-spacing="2.6">FASE 01 · DOCUMENTO PILOTO · P.01</text>' % ROSAI)
S.append('<text x="15" y="52" font-size="21" fill="%s" font-family="Bahnschrift" font-weight="600" letter-spacing="0.6">REFUGIO CLIMÁTICO</text>' % GTEC)
S.append('<text x="15" y="76" font-size="21" font-family="Bahnschrift" font-weight="600" letter-spacing="0.6" fill="none" stroke="%s" stroke-width="0.32">PUERTA DEL SOL</text>' % TURQD)
S.append('<text x="16" y="88" font-size="3.3" fill="%s" font-family="Consolas, monospace">PLANTA GENERAL · 1:300 (A1) · norte arriba · contexto real OSM · fuente geometria_maestra.json · 07-2026</text>' % GTEC)
# hilo que baja del titulo al primer loop (el plano y la cartela son la misma cosa)
p_c1 = T((-52, 30))
S.append('<path d="M 120 92 C 130 %.0f, %.0f %.0f, %.2f %.2f" fill="none" stroke="%s" stroke-width="0.12"/>' % (
    (92 + p_c1[1]) / 2, (120 + p_c1[0]) / 2, p_c1[1] - 20, p_c1[0], p_c1[1], ROSAI))

# ---- LEYENDA como marginalia (film vertical a sangre, filo derecho) ----
LX = PW - 52
S.append('<path d="M %.1f 0 L %.1f 0 L %.1f %.1f L %.1f %.1f Z" fill="#FFFFFF" fill-opacity="0.78"/>' % (
    LX - 4, PW, PW, PH, LX - 1, PH))
S.append('<line x1="%.1f" y1="0" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.3"/>' % (LX - 3.2, LX - 0.4, PH, TURQD))
S.append('<text x="%.1f" y="16" font-size="3.2" fill="%s" font-family="Bahnschrift" letter-spacing="2.4">LEYENDA</text>' % (LX + 2, TURQD))
legend = [
    (TURQ, 'loop estructural', 'haz de 3 anillos · traviesas c/2 m'),
    (TURQ, 'red tensada', 'malla de cables con nudos'),
    (TURQD, 'cinta-recorrido', 'doble carril +4/6 · coordenadas x y +z'),
    ('#8FB35B', 'disco-canopy', 'malla radial Ø3–8 · lám. microalgas'),
    ('#4E9B6E', 'balsa elevada', 'oleaje · cota +6/8'),
    ('#2F7D57', 'estanque de cultivo', 'en suelo · murete 45 cm'),
    (SPLASHC, 'lámina jugable', '+ vapor de nebulización'),
    ('#D14E92', 'cápsula neumática', 'gajos y válvula · suelo/media'),
    ('#C23B7E', 'depósito +10.5', 'radios = zunchos TPU'),
    (ROSAI, 'red hidráulica vista', 'boquillas en abanico'),
    (ROSAI, 'micro-cotas', 'distancias reales en metros'),
    (VVEG, 'vegetación', 'garabato = copa · puntos = matas'),
    (COBRE, 'banco-jardinera', 'madera en arco'),
    ('#6B6B68', 'mástil ramificado', '+ abanico de cables'),
    ('#5B5B8F', 'Metro / Cercanías', 'bocas conservadas'),
    (GTEC, 'monumento', 'triple diana · figuras y fauna'),
]
yy = 24
for (col, t1, t2) in legend:
    S.append('<circle cx="%.1f" cy="%.1f" r="1.15" fill="%s"/>' % (LX + 4, yy - 1, col))
    S.append('<text x="%.1f" y="%.1f" font-size="2.5" fill="%s" font-weight="bold">%s</text>' % (LX + 7.5, yy, GTEC, t1))
    S.append('<text x="%.1f" y="%.1f" font-size="2.1" fill="#6d6a63">%s</text>' % (LX + 7.5, yy + 3.1, t2))
    yy += 8.6
yy += 5
S.append('<text x="%.1f" y="%.1f" font-size="3.2" fill="%s" font-family="Bahnschrift" letter-spacing="2.4">CERTEZA</text>' % (LX + 2, yy, TURQD))
yy += 7
for (g, txt, dash, op) in [('G1', 'confirmado', '', 1.0), ('G2', 'muy probable', '', 0.85),
                           ('G3', 'inferido', 'stroke-dasharray="2.2 1.6"', 1.0),
                           ('G4', 'reserva F02', 'stroke-dasharray="0.5 1.2"', 1.0)]:
    S.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.55" opacity="%s" %s/>' % (
        LX + 2, yy - 1, LX + 9, yy - 1, TURQD, op, dash))
    S.append('<text x="%.1f" y="%.1f" font-size="2.3" fill="%s">%s — %s</text>' % (LX + 11, yy, GTEC, g, txt))
    yy += 5.4
yy += 5
S.append('<text x="%.1f" y="%.1f" font-size="3.2" fill="%s" font-family="Bahnschrift" letter-spacing="2.4">ESTRATOS</text>' % (LX + 2, yy, TURQD))
yy += 7
for (cota, txt, col) in [('+10/12', 'depósitos · red alta', ROSAI), ('+5/10', 'discos · balsas · loops', TURQ),
                         ('+4/6', 'cinta-recorrido', TURQD), ('+2/4', 'cápsulas media · riego', ROSA),
                         ('±0', 'suelo público continuo', VVEG)]:
    S.append('<text x="%.1f" y="%.1f" font-size="2.5" fill="%s" font-family="Bahnschrift">%s</text>' % (LX + 2, yy, col, cota))
    S.append('<text x="%.1f" y="%.1f" font-size="2.1" fill="#6d6a63">%s</text>' % (LX + 15, yy, txt))
    yy += 5.2

# ---- mini-seccion estratigrafica dibujada (anclada abajo, sobre el circulo P.01) ----
gy0 = PH - 52                  # linea de suelo
mm_m = 6.2                     # mm de papel por metro de seccion (altura total ~78 mm)
sec_top = gy0 - 12 * mm_m - 10
if sec_top > yy + 16:
    x0s = LX + 4
    x1s = PW - 8
    xc = (x0s + x1s) / 2

    def zy(z):
        return gy0 - z * mm_m

    S.append('<text x="%.1f" y="%.1f" font-size="3.2" fill="%s" font-family="Bahnschrift" letter-spacing="2.4">SECCIÓN TIPO</text>' % (LX + 2, sec_top - 4, TURQD))
    # niveles
    for z, col in [(12, ROSAI), (10.5, ROSAI), (8, TURQ), (5, TURQ), (4, TURQD), (0, GTEC)]:
        S.append('<line x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="0.08" stroke-dasharray="1.2 1"/>' % (
            x0s, zy(z), x1s, zy(z), col))
        S.append('<text x="%.1f" y="%.2f" font-size="1.8" fill="%s" font-family="Consolas, monospace">+%.1f</text>' % (x1s - 7, zy(z) - 0.7, col, z))
    # suelo
    S.append('<line x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="0.5"/>' % (x0s, gy0, x1s, gy0, GTEC))
    # mastil ramificado
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#6B6B68" stroke-width="0.3"/>' % (xc, gy0, xc, zy(7.5)))
    for dx in (-4.5, 4.5):
        S.append('<path d="M %.2f %.2f Q %.2f %.2f %.2f %.2f" fill="none" stroke="#6B6B68" stroke-width="0.18"/>' % (
            xc, zy(6), xc + dx * 0.6, zy(7.4), xc + dx, zy(8)))
    # discos a dos cotas
    for dx, z, rw in ((-4.5, 8, 6.5), (4.5, 6.4, 5.2)):
        S.append('<ellipse cx="%.2f" cy="%.2f" rx="%.1f" ry="1.1" fill="%s" fill-opacity="0.6" stroke="#8FB35B" stroke-width="0.16"/>' % (
            xc + dx, zy(z), rw, LIMA))
        S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#4E9B6E" stroke-width="0.1" stroke-dasharray="0.7 0.7"/>' % (
            xc + dx, zy(z) + 1.1, xc + dx, gy0))
    # deposito alto + bajante
    S.append('<circle cx="%.2f" cy="%.2f" r="2.6" fill="%s" fill-opacity="0.85" stroke="#C23B7E" stroke-width="0.16"/>' % (xc - 9, zy(10.5), ROSAI))
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#C23B7E" stroke-width="0.22"/>' % (xc - 9, zy(10.5) + 2.6, xc - 9, gy0))
    S.append('<path d="M %.2f %.2f q 3 2 6 0" fill="none" stroke="%s" stroke-width="0.16" stroke-dasharray="1 0.8"/>' % (xc - 9, zy(2.2), ROSAI))
    # cinta
    S.append('<rect x="%.2f" y="%.2f" width="7" height="1.2" rx="0.6" fill="%s"/>' % (xc + 6, zy(5) - 0.6, TURQD))
    S.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="0.18"/>' % (xc + 9.5, zy(5) + 0.6, xc + 9.5, gy0, TURQD))
    # capsula en suelo + persona
    S.append('<ellipse cx="%.2f" cy="%.2f" rx="3" ry="2" fill="%s" fill-opacity="0.65" stroke="#D14E92" stroke-width="0.16"/>' % (xc - 14, gy0 - 2, ROSA))
    S.append('<circle cx="%.2f" cy="%.2f" r="0.5" fill="%s"/><line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="0.16"/>' % (
        xc + 13, gy0 - 2.9, GTEC, xc + 13, gy0 - 2.4, xc + 13, gy0, GTEC))
    # nebulizacion
    for k in range(9):
        S.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" opacity="0.4"/>' % (
            xc + rng.uniform(-6, 6), zy(3.2) + rng.uniform(-2.5, 2.5), rng.uniform(0.15, 0.4), SPLASHC))

# ---- NORTE + ESCALA como mobiliario dentro de la plaza (vacio SE) ----
nx0, ny0 = T((56, -20))
S.append('<g transform="translate(%.2f %.2f)">' % (nx0, ny0))
S.append('<circle r="7" fill="none" stroke="%s" stroke-width="0.35"/>' % GTEC)
S.append('<circle r="9.4" fill="none" stroke="%s" stroke-width="0.1" stroke-dasharray="0.8 0.8"/>' % GTEC)
S.append('<path d="M 0 5.6 L 0 -5.6 M 0 -5.6 L -2 -2.2 M 0 -5.6 L 2 -2.2" stroke="%s" stroke-width="0.35" fill="none"/>' % GTEC)
S.append('<text x="8" y="-7" font-size="3.6" fill="%s" font-family="Bahnschrift">N</text>' % GTEC)
S.append('</g>')
sx0, sy0v = T((36, -26))
S.append('<g transform="translate(%.2f %.2f)">' % (sx0, sy0v))
S.append('<line x1="0" y1="0" x2="%.1f" y2="0" stroke="%s" stroke-width="0.35"/>' % (20 * SCALE, GTEC))
S.append('<rect x="0" y="-1.3" width="%.1f" height="2.6" fill="%s"/><rect x="%.1f" y="-1.3" width="%.1f" height="2.6" fill="%s"/>' % (
    5 * SCALE, GTEC, 10 * SCALE, 5 * SCALE, GTEC))
S.append('<text x="-1" y="5.6" font-size="2.2" fill="%s">0</text><text x="%.1f" y="5.6" font-size="2.2" fill="%s">5</text><text x="%.1f" y="5.6" font-size="2.2" fill="%s">10</text><text x="%.1f" y="5.6" font-size="2.2" fill="%s">20 m</text>' % (
    GTEC, 5 * SCALE - 1, GTEC, 10 * SCALE - 2, GTEC, 20 * SCALE - 4, GTEC))
S.append('</g>')

# ---- TICKER de datos en el filo inferior (film a sangre) ----
S.append('<rect x="0" y="%.1f" width="%.1f" height="10.5" fill="#FFFFFF" fill-opacity="0.8"/>' % (PH - 10.5, PW))
S.append('<line x1="0" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.3"/>' % (PH - 10.5, PW, PH - 10.5, TURQD))
ticker = ('PLAZA 10.957 M² · INTERVENCIÓN 163×51 M · DOSEL 1.890 M² · 67 DISCOS · 6 BALSAS · 5 ESTANQUES · '
          '8 LOOPS + CÚPULA · CINTA 480 M / 6 BUCLES · 38 CÁPSULAS · 13 DEPÓSITOS · 42 BOQUILLAS · 98 MÁSTILES · '
          '39+20 ÁRBOLES · BANDA CORREOS 15 M · ALTURA MÁX 12 M · AGUA POR GRAVEDAD')
S.append('<text x="10" y="%.1f" font-size="2.5" fill="%s" font-family="Consolas, monospace" letter-spacing="0.35">%s</text>' % (PH - 6.2, GTEC, ticker))
S.append('<text x="10" y="%.1f" font-size="1.9" fill="#8a877f" font-family="Consolas, monospace">REFUGIO CLIMÁTICO PUERTA DEL SOL · FASE 01 · 07-2026 · iraxxxdios · contexto OpenStreetMap (ODbL) · toda cifra dibujada procede de geometria_maestra.json (1 u = 1 m)</text>' % (PH - 2.4))

# ---- circulo-marca magenta con numeracion (esquina inferior derecha) ----
S.append('<circle cx="%.1f" cy="%.1f" r="13" fill="none" stroke="#E0218A" stroke-width="0.8"/>' % (PW - 26, PH - 26))
S.append('<circle cx="%.1f" cy="%.1f" r="10.6" fill="#FFFFFF" fill-opacity="0.75" stroke="none"/>' % (PW - 26, PH - 26))
S.append('<text x="%.1f" y="%.1f" font-size="7.2" fill="%s" font-family="Bahnschrift" font-weight="600" text-anchor="middle">P.01</text>' % (PW - 26, PH - 24.4, GTEC))
S.append('<text x="%.1f" y="%.1f" font-size="1.8" fill="#E0218A" font-family="Bahnschrift" letter-spacing="0.6" text-anchor="middle">IRAXXXDIOS</text>' % (PW - 26.6, PH - 18.6))

S.append('</svg>')
out = os.path.join(HERE, 'P01_PLANTA_GENERAL_500.svg')
open(out, 'w', encoding='utf-8').write('\n'.join(S))
print('OK v2 ->', out)
