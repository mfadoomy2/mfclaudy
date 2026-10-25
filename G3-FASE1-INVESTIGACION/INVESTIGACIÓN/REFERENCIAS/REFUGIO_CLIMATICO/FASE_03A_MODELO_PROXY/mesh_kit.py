# -*- coding: utf-8 -*-
"""Primitivas de malla (V,F) para el proxy 3D. Coordenadas del proyecto: 1u=1m, +Z arriba."""
import math


def _merge(objs):
    V, F = [], []
    for (v, f) in objs:
        off = len(V)
        V += v
        F += [(a + off, b + off, c + off) for (a, b, c) in f]
    return V, F


def cylinder(p0, p1, r, n=10):
    """Cilindro entre dos puntos 3D."""
    ax = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
    L = math.sqrt(sum(a * a for a in ax)) or 1e-9
    az = tuple(a / L for a in ax)
    ref = (0, 0, 1) if abs(az[2]) < 0.95 else (1, 0, 0)
    ux = (az[1] * ref[2] - az[2] * ref[1], az[2] * ref[0] - az[0] * ref[2], az[0] * ref[1] - az[1] * ref[0])
    m = math.sqrt(sum(a * a for a in ux)) or 1e-9
    ux = tuple(a / m for a in ux)
    uy = (az[1] * ux[2] - az[2] * ux[1], az[2] * ux[0] - az[0] * ux[2], az[0] * ux[1] - az[1] * ux[0])
    V, F = [], []
    for (cx, cy, cz) in (p0, p1):
        for k in range(n):
            a = 2 * math.pi * k / n
            V.append((cx + r * (math.cos(a) * ux[0] + math.sin(a) * uy[0]),
                      cy + r * (math.cos(a) * ux[1] + math.sin(a) * uy[1]),
                      cz + r * (math.cos(a) * ux[2] + math.sin(a) * uy[2])))
    for k in range(n):
        k2 = (k + 1) % n
        F.append((k, k2, n + k2))
        F.append((k, n + k2, n + k))
    # tapas
    V.append(p0); V.append(p1)
    c0, c1 = len(V) - 2, len(V) - 1
    for k in range(n):
        k2 = (k + 1) % n
        F.append((c0, k2, k))
        F.append((c1, n + k, n + k2))
    return V, F


def sphere(c, r, nu=12, nv=8):
    V, F = [], []
    for j in range(nv + 1):
        ph = math.pi * j / nv
        for i in range(nu):
            th = 2 * math.pi * i / nu
            V.append((c[0] + r * math.sin(ph) * math.cos(th),
                      c[1] + r * math.sin(ph) * math.sin(th),
                      c[2] + r * math.cos(ph)))
    for j in range(nv):
        for i in range(nu):
            i2 = (i + 1) % nu
            a = j * nu + i
            b = j * nu + i2
            cc = (j + 1) * nu + i2
            d = (j + 1) * nu + i
            F.append((a, b, cc)); F.append((a, cc, d))
    return V, F


def pill(c, length, dia, rot_deg, z=None):
    """Capsula horizontal (pildora): eje segun rot, longitud total incl. casquetes."""
    r = dia / 2.0
    zc = c[2] if z is None else z
    a = math.radians(rot_deg)
    dx, dy = math.cos(a), math.sin(a)
    h = max(length - dia, 0.01) / 2.0
    p0 = (c[0] - dx * h, c[1] - dy * h, zc)
    p1 = (c[0] + dx * h, c[1] + dy * h, zc)
    return _merge([cylinder(p0, p1, r, 12), sphere(p0, r, 10, 6), sphere(p1, r, 10, 6)])


def disc_sag(c, r, cota, sag=None, n=16, rings=3):
    """Disco-canopy: aro perimetral a 'cota', centro deprimido (embudo de drenaje)."""
    if sag is None:
        sag = max(0.25, r * 0.18)
    V, F = [], []
    for j in range(rings + 1):
        f = j / rings
        rr = r * f
        zz = cota - sag * (1 - f) ** 1.6
        for i in range(n):
            a = 2 * math.pi * i / n
            V.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a), zz))
    for j in range(rings):
        for i in range(n):
            i2 = (i + 1) % n
            a = j * n + i
            b = j * n + i2
            cc = (j + 1) * n + i2
            d = (j + 1) * n + i
            F.append((a, cc, b)); F.append((a, d, cc))
    return V, F


def torus(c, R, r, n=20, m=8):
    V, F = [], []
    for i in range(n):
        a = 2 * math.pi * i / n
        for j in range(m):
            b = 2 * math.pi * j / m
            V.append((c[0] + (R + r * math.cos(b)) * math.cos(a),
                      c[1] + (R + r * math.cos(b)) * math.sin(a),
                      c[2] + r * math.sin(b)))
    for i in range(n):
        for j in range(m):
            a = i * m + j
            b = ((i + 1) % n) * m + j
            cc = ((i + 1) % n) * m + (j + 1) % m
            d = i * m + (j + 1) % m
            F.append((a, b, cc)); F.append((a, cc, d))
    return V, F


def tube(pts, r, n=8):
    """Tubo circular a lo largo de una polilinea 3D (transporte paralelo simple)."""
    if len(pts) < 2:
        return [], []
    V, F = [], []
    prev_u = None
    rings = 0
    for i, p in enumerate(pts):
        if i == 0:
            d = (pts[1][0] - p[0], pts[1][1] - p[1], pts[1][2] - p[2])
        elif i == len(pts) - 1:
            d = (p[0] - pts[i - 1][0], p[1] - pts[i - 1][1], p[2] - pts[i - 1][2])
        else:
            d = (pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1], pts[i + 1][2] - pts[i - 1][2])
        L = math.sqrt(sum(a * a for a in d)) or 1e-9
        az = tuple(a / L for a in d)
        if prev_u is None:
            ref = (0, 0, 1) if abs(az[2]) < 0.95 else (1, 0, 0)
            ux = (az[1] * ref[2] - az[2] * ref[1], az[2] * ref[0] - az[0] * ref[2], az[0] * ref[1] - az[1] * ref[0])
        else:
            ux = (prev_u[1] * az[2] - prev_u[2] * az[1], prev_u[2] * az[0] - prev_u[0] * az[2], prev_u[0] * az[1] - prev_u[1] * az[0])
            ux = (az[1] * ux[2] - az[2] * ux[1], az[2] * ux[0] - az[0] * ux[2], az[0] * ux[1] - az[1] * ux[0])
        m0 = math.sqrt(sum(a * a for a in ux)) or 1e-9
        ux = tuple(a / m0 for a in ux)
        uy = (az[1] * ux[2] - az[2] * ux[1], az[2] * ux[0] - az[0] * ux[2], az[0] * ux[1] - az[1] * ux[0])
        prev_u = ux
        for k in range(n):
            a = 2 * math.pi * k / n
            V.append((p[0] + r * (math.cos(a) * ux[0] + math.sin(a) * uy[0]),
                      p[1] + r * (math.cos(a) * ux[1] + math.sin(a) * uy[1]),
                      p[2] + r * (math.cos(a) * ux[2] + math.sin(a) * uy[2])))
        rings += 1
    for i in range(rings - 1):
        for k in range(n):
            k2 = (k + 1) % n
            a = i * n + k
            b = i * n + k2
            cc = (i + 1) * n + k2
            d = (i + 1) * n + k
            F.append((a, b, cc)); F.append((a, cc, d))
    return V, F


def strip(pts, width, z0, z1):
    """Franja vertical extruida a lo largo de polilinea 2D (jardineras, bancos, muros)."""
    if len(pts) < 2:
        return [], []
    hw = width / 2.0
    left, right = [], []
    for i, p in enumerate(pts):
        if i == 0:
            d = (pts[1][0] - p[0], pts[1][1] - p[1])
        elif i == len(pts) - 1:
            d = (p[0] - pts[i - 1][0], p[1] - pts[i - 1][1])
        else:
            d = (pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1])
        L = math.hypot(*d) or 1e-9
        nx, ny = -d[1] / L, d[0] / L
        left.append((p[0] + nx * hw, p[1] + ny * hw))
        right.append((p[0] - nx * hw, p[1] - ny * hw))
    V, F = [], []
    m = len(pts)
    for (px, py) in left:
        V.append((px, py, z0)); V.append((px, py, z1))
    for (px, py) in right:
        V.append((px, py, z0)); V.append((px, py, z1))
    for i in range(m - 1):
        a0, a1 = 2 * i + 1, 2 * (i + 1) + 1          # left top
        b0, b1 = 2 * m + 2 * i + 1, 2 * m + 2 * (i + 1) + 1  # right top
        F.append((a0, a1, b1)); F.append((a0, b1, b0))       # tapa superior
        la0, la1 = 2 * i, 2 * (i + 1)
        F.append((la0, la1, a1)); F.append((la0, a1, a0))    # cara izq
        rb0, rb1 = 2 * m + 2 * i, 2 * m + 2 * (i + 1)
        F.append((rb0, b1, rb1)); F.append((rb0, b0, b1))    # cara der
    return V, F


def surf(poly, z):
    """Superficie horizontal por abanico desde el centroide (poligonos convexos/estrellados)."""
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    V = [(cx, cy, z)] + [(p[0], p[1], z) for p in poly]
    F = []
    for i in range(1, len(poly) + 1):
        j = i % len(poly) + 1
        F.append((0, i, j))
    return V, F


def box(c, dx, dy, dz, rot_deg=0):
    a = math.radians(rot_deg)
    ca, sa = math.cos(a), math.sin(a)
    V = []
    for sz in (0, 1):
        for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            x, y = sx * dx / 2, sy * dy / 2
            V.append((c[0] + x * ca - y * sa, c[1] + x * sa + y * ca, c[2] + sz * dz))
    F = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7)]
    for i in range(4):
        j = (i + 1) % 4
        F.append((i, j, 4 + j)); F.append((i, 4 + j, 4 + i))
    return V, F


def ell_pts(cx, cy, rx, ry, rot_deg, n=40):
    r = math.radians(rot_deg)
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = rx * math.cos(a), ry * math.sin(a)
        out.append((cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)))
    out.append(out[0])
    return out


def merge(objs):
    return _merge(objs)
