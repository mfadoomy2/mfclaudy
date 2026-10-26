#!/usr/bin/env python3
"""Genera PABELLON_BAMBU.3dm (Rhino 8) con texturas a partir de la foto de referencia.

Uso:  python3 generar_pabellon_bambu.py
Salida (misma carpeta): PABELLON_BAMBU.3dm, tex_*.png, preview_pabellon.png
Unidades: metros. Todo se construye con rhino3dm (sin Rhino instalado).
"""
import os, math
import numpy as np
import rhino3dm as r
from PIL import Image, ImageDraw
from scipy.interpolate import splprep, splev
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
OUT3DM = os.path.join(HERE, 'PABELLON_BAMBU.3dm')
rng = np.random.default_rng(7)

# =====================================================================
# 1. TEXTURAS PROCEDURALES (se guardan junto al .3dm con nombre tex_*)
# =====================================================================
def save(name, arr):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(os.path.join(HERE, name))
    return name

def noise2(h, w, scale, seed):
    g = np.random.default_rng(seed).random((max(2, h // scale + 2), max(2, w // scale + 2)))
    im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(im).astype(float) / 255

def streaks(h, w, nx, seed):  # ruido estirado en vertical (vetas)
    n = np.random.default_rng(seed).random((h // 2, max(2, nx)))
    return np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)) / 255

def tex_bambu():
    h, w = 1024, 256
    y = np.arange(h)[:, None]
    img = np.array([206., 166., 92.])[None, None, :] * (0.78 + 0.3 * streaks(h, w, 14, 1) + 0.12 * noise2(h, w, 40, 2))[..., None]
    for k in range(4):  # 4 nudos por tesela (tesela = 1.32 m -> nudo cada 33 cm)
        d = np.abs(y - (k * 256 + 128))
        img[(d < 8)[:, 0]] *= 0.6
        img[((d >= 8) & (d < 13))[:, 0]] *= 1.12
    return save('tex_bambu.png', img)

def tex_corteza():
    h, w = 1024, 256
    img = np.array([96., 86., 76.])[None, None, :] * (0.55 + 0.9 * streaks(h, w, 12, 31))[..., None] * (0.85 + 0.3 * noise2(h, w, 16, 32))[..., None]
    return save('tex_corteza.png', img)

def tex_perforado():
    S = 1024
    circles = []
    for _ in range(6000):
        rad = rng.uniform(9, 44); x = rng.uniform(0, S); y = rng.uniform(0, S)
        ok = True
        for (cx, cy, cr) in circles:
            dx = abs(x - cx); dx = min(dx, S - dx); dy = abs(y - cy); dy = min(dy, S - dy)
            if dx * dx + dy * dy < (rad + cr + 7) ** 2:
                ok = False; break
        if ok: circles.append((x, y, rad))
        if len(circles) >= 430: break
    imA = Image.new('L', (S, S), 0); dA = ImageDraw.Draw(imA)
    imC = Image.new('RGB', (S, S), (242, 234, 220)); dC = ImageDraw.Draw(imC)
    for (x, y, rad) in circles:
        for ox in (-S, 0, S):
            for oy in (-S, 0, S):
                cx, cy = x + ox, y + oy
                dC.ellipse([cx - rad - 4, cy - rad - 4, cx + rad + 4, cy + rad + 4], fill=(208, 196, 178))
                dC.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(70, 58, 48))
                dA.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=255)
    col = np.asarray(imC).astype(float) * (0.92 + 0.16 * noise2(S, S, 10, 3))[..., None]
    save('tex_perforado_color.png', col)
    imA.save(os.path.join(HERE, 'tex_perforado_alfa.png'))  # blanco = transparente (agujero)
    return 'tex_perforado_color.png', 'tex_perforado_alfa.png'

def tex_vidrio(name, base, line, seed, n=70):
    S = 512; g = np.random.default_rng(seed); seeds = g.random((n, 2)) * S
    pts = np.concatenate([seeds + np.array([ox, oy]) for ox in (-S, 0, S) for oy in (-S, 0, S)])
    yy, xx = np.mgrid[0:S, 0:S]; q = np.stack([xx.ravel(), yy.ravel()], 1)
    d, i = cKDTree(pts).query(q, k=2)
    d1, d2 = d[:, 0].reshape(S, S), d[:, 1].reshape(S, S)
    edge = np.clip((4.5 - (d2 - d1)) / 4.5, 0, 1)
    cell = (i[:, 0] % n).reshape(S, S)
    var = (g.random(n) * 0.35 + 0.8)[cell]
    img = np.array(base, float)[None, None, :] * var[..., None] * (0.8 + 0.4 * noise2(S, S, 20, seed + 1))[..., None]
    img = img * (1 - edge[..., None]) + np.array(line, float)[None, None, :] * edge[..., None]
    return save(name, img)

def tex_membrana():
    S = 512; y = np.arange(S)[:, None]; x = np.arange(S)[None, :]
    img = np.ones((S, S, 3)) * 248 - (((x % 16 == 0) | (y % 16 == 0)).astype(float) * 14)[..., None]
    img *= (0.95 + 0.1 * noise2(S, S, 16, 5))[..., None]
    return save('tex_membrana.png', img)

def tex_madera():
    S = 512; y = np.arange(S)[:, None]; x = np.arange(S)[None, :]
    g = np.random.default_rng(11); plank = 64; row = y // plank
    tint = (g.random(S // plank + 1) * 0.3 + 0.8)[row[:, 0]][:, None]
    grain = 0.75 + 0.5 * np.asarray(Image.fromarray((g.random((S // 20, S)) * 255).astype(np.uint8)).resize((S, S), Image.BICUBIC)) / 255
    img = np.array([178., 126., 72.])[None, None, :] * (tint * grain)[..., None]
    off = (g.random(S // plank + 1) * 512).astype(int)[row[:, 0]][:, None]
    gap = (y % plank < 3) | (((x + off) % 256) < 3)
    img[gap] = [42, 30, 20]
    return save('tex_madera.png', img)

def tex_agua():
    S = 512; y = np.arange(S)[:, None] - S / 2; x = np.arange(S)[None, :] - S / 2; rr = np.hypot(x, y)
    rip = np.sin(rr / 6.0) * np.exp(-rr / 160)
    img = np.array([88., 108., 118.])[None, None, :] * (1 + 0.35 * rip)[..., None] + (np.clip(1 - rr / 256, 0, 1) * 30)[..., None]
    return save('tex_agua.png', img)

def tex_suelo():
    S = 1024
    img = np.ones((S, S, 3)) * np.array([64., 50., 38.]) * (0.65 + 0.7 * noise2(S, S, 6, 21))[..., None]
    moss = np.clip((noise2(S, S, 48, 22) - 0.42) * 4, 0, 1) * (0.5 + 0.5 * noise2(S, S, 8, 23))
    img = img * (1 - moss[..., None]) + np.array([80., 122., 44.])[None, None, :] * (0.7 + 0.6 * noise2(S, S, 3, 24))[..., None] * moss[..., None]
    img[noise2(S, S, 2, 25) > 0.94] = [150, 132, 100]
    return save('tex_suelo_musgo.png', img)

print('Texturas...')
T_BAMBU = tex_bambu(); T_CORTEZA = tex_corteza()
T_PERF, T_PERF_A = tex_perforado()
T_ROJO = tex_vidrio('tex_vidrio_rojo.png', (178, 14, 32), (70, 0, 12), 41)
T_AMAR = tex_vidrio('tex_vidrio_amarillo.png', (236, 184, 44), (120, 70, 10), 43, n=55)
T_MEMB = tex_membrana(); T_MADERA = tex_madera(); T_AGUA = tex_agua(); T_SUELO = tex_suelo()

# =====================================================================
# 2. ARCHIVO, CAPAS Y MATERIALES
# =====================================================================
f = r.File3dm()
f.Settings.ModelUnitSystem = r.UnitSystem.Meters
f.Settings.ModelAbsoluteTolerance = 0.001

def layer(name, rgb):
    L = r.Layer(); L.Name = name; L.Color = (rgb[0], rgb[1], rgb[2], 255)
    return f.Layers.Add(L)

L = {k: layer(k, c) for k, c in [
    ('00_Ejes_bambu', (120, 90, 40)), ('01_Bambu', (210, 170, 95)), ('02_Panel_blanco_perforado', (230, 225, 210)),
    ('03_Panel_rojo', (180, 20, 40)), ('04_Panel_amarillo', (235, 180, 40)), ('05_Membrana_cubierta', (240, 240, 240)),
    ('06_Acero', (160, 165, 170)), ('07_Madera_tarima_banco', (170, 120, 70)), ('08_Agua', (90, 120, 140)),
    ('09_Cables', (200, 200, 200)), ('10_LED_magenta', (230, 30, 140)), ('11_Vidrio_lampara', (200, 230, 240)),
    ('12_Terreno', (70, 55, 40)), ('13_Arboles', (90, 80, 70))]}

def texture(fn, ttype):
    t = r.Texture(); t.FileName = fn; t.TextureType = ttype
    # WrapU/WrapV son Repeat por defecto (sin setter en rhino3dm)
    return t

def material(name, rgb, tex=None, alpha=None, transp=0.0, refl=0.0, shine=0.0, emis=None):
    m = r.Material(); m.Name = name; m.DiffuseColor = (rgb[0], rgb[1], rgb[2], 255)
    m.Transparency = transp; m.Reflectivity = refl; m.Shine = shine
    if emis: m.EmissionColor = (emis[0], emis[1], emis[2], 255)
    if tex: m.SetBitmapTexture(texture(tex, r.TextureType.Bitmap))
    if alpha: m.SetTransparencyTexture(texture(alpha, r.TextureType.Transparency))
    return f.Materials.Add(m)

M = {
    'bambu': material('Bambu', (206, 166, 92), T_BAMBU, shine=0.25),
    'perforado': material('Panel blanco perforado', (242, 234, 220), T_PERF, alpha=T_PERF_A),
    'rojo': material('Panel vidrio rojo', (178, 14, 32), T_ROJO, transp=0.30, refl=0.2, shine=0.6),
    'amarillo': material('Panel vidrio amarillo', (236, 184, 44), T_AMAR, transp=0.30, refl=0.2, shine=0.6),
    'membrana': material('Membrana PTFE', (248, 248, 248), T_MEMB, transp=0.35),
    'acero': material('Acero galvanizado', (205, 208, 212), refl=0.6, shine=0.9),
    'madera': material('Madera tarima', (178, 126, 72), T_MADERA, shine=0.2),
    'madera_osc': material('Madera oscura', (92, 62, 36), shine=0.2),
    'agua': material('Agua', (88, 108, 118), T_AGUA, refl=0.5, shine=0.9, transp=0.1),
    'cable': material('Cable', (215, 210, 200), shine=0.3),
    'led': material('LED magenta', (230, 30, 140), emis=(230, 30, 140)),
    'vidrio': material('Vidrio', (220, 235, 240), transp=0.8, refl=0.3, shine=0.9),
    'suelo': material('Suelo humedo musgo', (64, 50, 38), T_SUELO, refl=0.15),
    'corteza': material('Corteza', (96, 86, 76), T_CORTEZA),
}

def attrs(lay, mat, name=None):
    a = r.ObjectAttributes(); a.LayerIndex = L[lay]; a.MaterialIndex = M[mat]
    a.MaterialSource = r.ObjectMaterialSource.MaterialFromObject
    if name: a.Name = name
    return a

PREVIEW = []  # (array Nx3 de polígonos, color rgb, alpha) para la vista previa
PREV_COL = {'bambu': (205, 165, 92), 'perforado': (240, 232, 216), 'rojo': (175, 15, 30), 'amarillo': (235, 182, 40),
            'membrana': (245, 245, 245), 'acero': (190, 195, 200), 'madera': (170, 120, 70), 'madera_osc': (90, 60, 35),
            'agua': (90, 110, 120), 'cable': (215, 210, 200), 'led': (230, 30, 140), 'vidrio': (210, 230, 240),
            'suelo': (62, 50, 38), 'corteza': (95, 85, 75)}
PREV_ALPHA = {'rojo': 0.75, 'amarillo': 0.75, 'membrana': 0.75, 'vidrio': 0.5}

# ---------------------------------------------------------------- mallas
XY_MAP = r.TextureMapping.CreatePlaneMapping(r.Plane.WorldXY(), r.Interval(0, 1), r.Interval(0, 1), r.Interval(0, 1))

def add_mesh(V, F, UV, lay, mat, name=None, preview_step=1):
    m = r.Mesh()
    for p in V: m.Vertices.Add(float(p[0]), float(p[1]), float(p[2]))
    for fc in F:
        if len(fc) == 4: m.Faces.AddFace(int(fc[0]), int(fc[1]), int(fc[2]), int(fc[3]))
        else: m.Faces.AddFace(int(fc[0]), int(fc[1]), int(fc[2]))
    m.SetTextureCoordinates(XY_MAP, r.Transform.Identity(), False)  # crea la lista; luego se sobrescribe
    tc = m.TextureCoordinates
    for i, uv in enumerate(UV): tc[i] = r.Point2f(float(uv[0]), float(uv[1]))
    m.Normals.ComputeNormals(); m.Compact()
    f.Objects.AddMesh(m, attrs(lay, mat, name))
    V = np.asarray(V)
    for fc in F[::preview_step]: PREVIEW.append((V[list(fc)], PREV_COL[mat], PREV_ALPHA.get(mat, 1.0)))

def rot(v, axis, th):
    axis = axis / np.linalg.norm(axis); c, s = math.cos(th), math.sin(th)
    return v * c + np.cross(axis, v) * s + axis * (axis @ v) * (1 - c)

def frames(P, closed):
    n = len(P)
    T = (np.roll(P, -1, 0) - np.roll(P, 1, 0)) if closed else np.gradient(P, axis=0)
    T = T / (np.linalg.norm(T, axis=1)[:, None] + 1e-12)
    N = np.zeros_like(P)
    a = np.array([0, 0, 1.]) if abs(T[0] @ np.array([0, 0, 1.])) < 0.9 else np.array([1, 0, 0.])
    n0 = np.cross(T[0], a); N[0] = n0 / np.linalg.norm(n0)
    for i in range(1, n):
        b = np.cross(T[i - 1], T[i]); nb = np.linalg.norm(b)
        N[i] = N[i - 1] if nb < 1e-9 else rot(N[i - 1], b, math.acos(np.clip(T[i - 1] @ T[i], -1, 1)))
        N[i] -= (N[i] @ T[i]) * T[i]; N[i] /= np.linalg.norm(N[i])
    if closed:  # repartir el desfase de cierre
        b = np.cross(T[-1], T[0]); nb = np.linalg.norm(b)
        Ne = N[-1] if nb < 1e-9 else rot(N[-1], b, math.acos(np.clip(T[-1] @ T[0], -1, 1)))
        Ne -= (Ne @ T[0]) * T[0]; Ne /= np.linalg.norm(Ne)
        phi = math.atan2(np.cross(N[0], Ne) @ T[0], N[0] @ Ne)
        for i in range(n): N[i] = rot(N[i], T[i], -phi * i / n)
    return T, N, np.cross(T, N)

def arclen(P):
    return np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])

CIRC = lambda nseg: [(math.cos(2 * math.pi * k / nseg), math.sin(2 * math.pi * k / nseg)) for k in range(nseg + 1)]

def sweep_mesh(P, profile, lay, mat, closed=False, radii=None, uv_scale=(1.0, 1.0), roll=0.0, name=None, preview_step=1):
    """Barre un perfil 2D (lista de (a,b), cerrado = primero==último) a lo largo de la polilínea P."""
    P = np.asarray(P, float); T, N, B = frames(P, closed); n = len(P)
    rad = np.ones(n) if radii is None else np.asarray(radii, float)
    Pr = np.vstack([P, P[:1]]) if closed else P
    s = arclen(Pr); idx = list(range(n)) + ([0] if closed else [])
    k = len(profile); V = []; UV = []; F = []
    for row, i in enumerate(idx):
        c, sn = math.cos(roll), math.sin(roll)
        for j, (a, b) in enumerate(profile):
            a2, b2 = a * c - b * sn, a * sn + b * c
            V.append(P[i] + rad[i] * (a2 * N[i] + b2 * B[i])); UV.append((s[row] * uv_scale[0], j / (k - 1) * uv_scale[1]))
    for row in range(len(idx) - 1):
        for j in range(k - 1):
            F.append((row * k + j, (row + 1) * k + j, (row + 1) * k + j + 1, row * k + j + 1))
    add_mesh(V, F, UV, lay, mat, name, preview_step)

def tube(P, radius, lay, mat, closed=False, nseg=10, uv_scale=(1 / 1.32, 1.0), radii=None, roll=0.0, name=None, preview_step=1):
    rr = None if radii is None else np.asarray(radii)
    prof = CIRC(nseg)
    if rr is None: prof = [(a * radius, b * radius) for a, b in prof]
    sweep_mesh(P, prof, lay, mat, closed, rr, uv_scale, roll, name, preview_step)

def plane_at(p, n):
    return r.Plane(r.Point3d(*map(float, p)), r.Vector3d(*map(float, n)))

def cylinder(p, n, rad, h, mat, lay='06_Acero', centered=True):
    """Cilindro Brep con eje n (unitario) que empieza en p (o centrado en p)."""
    p = np.asarray(p, float); n = np.asarray(n, float); n /= np.linalg.norm(n)
    base = p - n * h / 2 if centered else p
    b = r.Cylinder(r.Circle(r.Point3d(0, 0, 0), rad), h).ToBrep(True, True)
    b.Transform(r.Transform.PlaneToPlane(r.Plane.WorldXY(), plane_at(base, n)))
    f.Objects.AddBrep(b, attrs(lay, mat))
    # vista previa: prisma de 8 lados
    T, N, Bn = frames(np.array([base, base + n * h]), False)
    ring = lambda c: [c + rad * (math.cos(a) * N[0] + math.sin(a) * Bn[0]) for a in np.linspace(0, 2 * math.pi, 9)]
    r0, r1 = ring(base), ring(base + n * h)
    for i in range(8): PREVIEW.append((np.array([r0[i], r1[i], r1[i + 1], r0[i + 1]]), PREV_COL[mat], 1.0))

def sphere(p, rad, mat, lay='06_Acero'):
    f.Objects.AddBrep(r.Brep.CreateFromSphere(r.Sphere(r.Point3d(*map(float, p)), rad)), attrs(lay, mat))
    p = np.asarray(p, float)
    for i in range(6):
        for j in range(6):
            a0, a1 = 2 * math.pi * i / 6, 2 * math.pi * (i + 1) / 6; b0, b1 = math.pi * j / 6 - math.pi / 2, math.pi * (j + 1) / 6 - math.pi / 2
            pt = lambda a, b: p + rad * np.array([math.cos(b) * math.cos(a), math.cos(b) * math.sin(a), math.sin(b)])
            PREVIEW.append((np.array([pt(a0, b0), pt(a1, b0), pt(a1, b1), pt(a0, b1)]), PREV_COL[mat], 1.0))

def add_curve(P, lay, closed=False, degree=3):
    pts = r.Point3dList(len(P) + (1 if closed else 0))
    for p in P: pts.Add(float(p[0]), float(p[1]), float(p[2]))
    if closed: pts.Add(float(P[0][0]), float(P[0][1]), float(P[0][2]))
    c = r.NurbsCurve.Create(False, degree, pts)
    a = r.ObjectAttributes(); a.LayerIndex = L[lay]; f.Objects.AddCurve(c, a)

# =====================================================================
# 3. ENVOLVENTE PARAMÉTRICA (u = ángulo en planta en grados, v = 0 suelo .. 1 anillo superior)
# =====================================================================
A, B_, H = 4.6, 3.0, 3.6  # semiejes en planta y altura del anillo de cubierta

def env(u, v):
    u = np.radians(np.asarray(u, float)); v = np.asarray(v, float)
    rr = 1 + 0.14 * np.sin(np.pi * np.clip(v, 0, 1)) - 0.30 * v ** 2
    rr = rr * (1 + 0.05 * np.sin(3 * u + 0.7) * (1 - np.clip(v, 0, 1)))
    return np.stack([A * rr * np.cos(u), B_ * rr * np.sin(u), H * v + 0.12 * np.sin(2 * u) * v], -1)

def env_normal(u, v):
    du = (env(u + 0.5, v) - env(u - 0.5, v)); dv = (env(u, v + 0.01) - env(u, v - 0.01))
    n = np.cross(du, dv); n = n / np.linalg.norm(n, axis=-1, keepdims=True)
    # orientar hacia fuera (alejándose del eje)
    p = env(u, v); out = np.sign(np.sum(n[..., :2] * p[..., :2], -1))
    return n * np.where(out == 0, 1, out)[..., None]

wrap = lambda d: (d + 180) % 360 - 180

class Cell:  # elipse en el espacio (u, v)
    def __init__(self, uc, vc, du, dv): self.uc, self.vc, self.du, self.dv = uc, vc, du, dv
    def inside(self, u, v): return (wrap(u - self.uc) / self.du) ** 2 + ((v - self.vc) / self.dv) ** 2 < 1
    def angle(self, u, v): return math.degrees(math.atan2((v - self.vc) / self.dv, wrap(u - self.uc) / self.du))
    def boundary(self, n=160):
        """Polilínea 3D del borde (recortado a v en [0,1]); devuelve (puntos, cerrada)."""
        k = -self.vc / self.dv
        if k > -1:  # toca el suelo: arco abierto de pie a pie
            t0 = math.asin(k); t = np.linspace(t0, math.pi - t0, n)
            closed = False
        else:
            t = np.linspace(0, 2 * math.pi, n, endpoint=False); closed = True
        u = self.uc + self.du * np.cos(t); v = np.clip(self.vc + self.dv * np.sin(t), 0, 1.0)
        return env(u, v), closed, u, v

# Celdas (ángulos en grados: 0 = +x derecha, 90 = +y fondo, 270 = frente/cámara)
ABIERTAS = {  # huecos: arcos y anillos pasantes
    'O1_anillo_izq': Cell(222, 0.45, 26, 0.44), 'O2_arco_entrada': Cell(280, 0.30, 19, 0.55),
    'O3_hueco_der': Cell(330, 0.40, 16, 0.36), 'O4_arco_trasero': Cell(90, 0.30, 22, 0.52),
    'O5_anillo_tras_der': Cell(40, 0.45, 14, 0.33), 'O6_anillo_tras_izq': Cell(140, 0.45, 14, 0.33)}
BANDAS = {  # (celda interior, celda exterior, rango angular rojo)
    'O1_anillo_izq': (Cell(222, 0.47, 34, 0.50), (95, 290)), 'O2_arco_entrada': (Cell(280, 0.30, 25, 0.66), (60, 200)),
    'O3_hueco_der': (Cell(330, 0.40, 21, 0.45), (-50, 120)), 'O4_arco_trasero': (Cell(90, 0.30, 28, 0.62), (0, 180))}
ROJAS = {'R1_lente_der': Cell(5, 0.45, 12, 0.38)}
AMARILLAS = {'Y1_izq': Cell(180, 0.62, 22, 0.30), 'Y2_centro_der': Cell(306, 0.55, 9, 0.30),
             'Y3_tras': Cell(115, 0.60, 12, 0.30), 'Y4_tras': Cell(65, 0.60, 12, 0.30)}
PILARES = [258, 352, 18, 65, 118, 165]      # costillas de pie a anillo, con giro
MASTILES = [165, 210, 258, 303, 352, 30, 65, 118]
MAST_H = 1.0

def ang_in(a, rng_):
    a0, a1 = rng_; return (wrap(a - a0) % 360) <= ((a1 - a0) % 360)

def classify(u, v):
    for c in ABIERTAS.values():
        if c.inside(u, v): return None
    zone = 'perforado'
    for c in AMARILLAS.values():
        if c.inside(u, v): zone = 'amarillo'
    for key, (outer, rng_) in BANDAS.items():
        if outer.inside(u, v) and not ABIERTAS[key].inside(u, v) and ang_in(outer.angle(u, v), rng_): zone = 'rojo'
    for c in ROJAS.values():
        if c.inside(u, v): zone = 'rojo'
    return zone

# ---------------------------------------------------------------- paneles
print('Paneles...')
NU, NV = 360, 44
PER = 2 * math.pi * math.sqrt((A * A + B_ * B_) / 2)  # perímetro aprox. para escalar texturas
TILE = {'perforado': 2.0, 'rojo': 1.3, 'amarillo': 1.3}
buckets = {k: ([], [], {}) for k in TILE}
for i in range(NU):
    for j in range(NV):
        u0, u1 = i * 360 / NU, (i + 1) * 360 / NU; v0, v1 = j / NV, (j + 1) / NV
        z = classify((u0 + u1) / 2, (v0 + v1) / 2)
        if z is None: continue
        Vl, Fl, vmap = buckets[z]; ids = []
        for (uu, vv) in [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]:
            key = (round(uu, 4), round(vv, 5))
            if key not in vmap:
                vmap[key] = len(Vl); Vl.append((env(uu, vv), (PER * (uu / 360) / TILE[z], H * vv / TILE[z])))
            ids.append(vmap[key])
        Fl.append(tuple(ids))
for z, (Vl, Fl, _) in buckets.items():
    add_mesh([p for p, _ in Vl], Fl, [t for _, t in Vl], {'perforado': '02_Panel_blanco_perforado', 'rojo': '03_Panel_rojo', 'amarillo': '04_Panel_amarillo'}[z], z, 'Panel ' + z, preview_step=1)

# ---------------------------------------------------------------- haces de bambú
print('Bambu...')
RB, RC = 0.072, 0.042  # radio del haz y radio de cada caña

def bundle(P, closed, name, nculm=4, clamp_every=0.65, twist=0.5, feet=False):
    P = np.asarray(P, float)
    add_curve(P[::3] if len(P) > 12 else P, '00_Ejes_bambu', closed)
    T, N, B = frames(P, closed); s = arclen(np.vstack([P, P[:1]]) if closed else P)[:len(P)]
    for c in range(nculm):
        ang = 2 * math.pi * c / nculm + twist * s
        if closed:  # el giro debe cerrar en vuelta completa
            ang = 2 * math.pi * c / nculm + 2 * math.pi * np.round(twist * s[-1] / (2 * math.pi)) * s / (s[-1] + s[-1] / len(P))
        Pc = P + RB * (np.cos(ang)[:, None] * N + np.sin(ang)[:, None] * B)
        tube(Pc, RC, '01_Bambu', 'bambu', closed, nseg=10, roll=rng.uniform(0, 6.28), name=f'{name} cana {c + 1}', preview_step=2)
    total = s[-1] + (np.linalg.norm(P[0] - P[-1]) if closed else 0)
    for sc in np.arange(0.35, total - 0.2, clamp_every):
        i = int(np.searchsorted(s, sc)) % len(P)
        cylinder(P[i], T[i], RB + RC + 0.012, 0.07, 'acero')
    if feet and not closed:
        for i, sign in ((0, 1), (-1, -1)):
            foot(P[i], T[i] * sign)

def foot(p, t_up):
    p = np.asarray(p, float); g = np.array([p[0], p[1], 0.0])
    cylinder(g + [0, 0, -0.02], [0, 0, 1], 0.19, 0.03, 'acero', centered=False)   # placa
    cylinder(g, [0, 0, 1], 0.13, 0.26, 'acero', centered=False)                   # pedestal
    cylinder(p + t_up * 0.22, t_up, RB + RC + 0.02, 0.2, 'acero')                 # manguito del haz

ribs = []  # (puntos, cerrada, nombre)
for key, c in ABIERTAS.items():
    P, closed, _, _ = c.boundary(170); ribs.append((P, closed, key))
for key, (outer, _) in BANDAS.items():
    P, closed, _, _ = outer.boundary(190); ribs.append((P, closed, key + '_exterior'))
for key, c in list(ROJAS.items()) + list(AMARILLAS.items()):
    P, closed, _, _ = c.boundary(120); ribs.append((P, closed, key))
for Pp, closed, name in ribs:
    bundle(Pp, closed, name, feet=not closed)

# pilares con giro (pie -> anillo) y continuación como mástil
mast_tops = {}
for u0 in PILARES:
    v = np.linspace(0, 1, 50); P = env(u0 + 12 * v, v)
    bundle(P, False, f'pilar_{u0}', twist=0.3, feet=False); foot(P[0], np.array([0, 0, 1.0]))
for u0 in MASTILES:
    prim = env(u0, 1.0); out = env_normal(u0, 1.0); out[2] = 0; out /= np.linalg.norm(out)
    top = prim + np.array([0, 0, MAST_H]) + out * 0.18
    t = np.linspace(0, 1, 14)[:, None]; ctrl = prim + np.array([0, 0, 0.35]) - out * 0.05
    P = (1 - t) ** 2 * prim + 2 * (1 - t) * t * ctrl + t ** 2 * top
    bundle(P, False, f'mastil_{u0}', nculm=3, clamp_every=0.3, twist=0.0)
    cylinder(top - [0, 0, 0.05], [0, 0, 1], RB + RC, 0.1, 'acero'); sphere(top + [0, 0, 0.08], 0.07, 'acero')
    mast_tops[u0] = top

# anillo superior y carril de base (sin los tramos de los arcos pasantes)
P = env(np.linspace(0, 360, 300, endpoint=False), 1.0); bundle(P, True, 'anillo_superior', nculm=5, clamp_every=0.5, twist=0.3)
ug = np.linspace(0, 360, 720, endpoint=False)
openbottom = [c for c in ABIERTAS.values() if -c.vc / c.dv > -1]
keep = np.array([not any(c.inside(u, 0.0) for c in openbottom) for u in ug])
# segmentar
start = int(np.argmin(keep)); segs = []; cur = []
for k in range(720):
    i = (start + k) % 720
    if keep[i]: cur.append(ug[i])
    elif cur: segs.append(cur); cur = []
if cur: segs.append(cur)
for n_, seg in enumerate(segs):
    P = env(np.array(seg), 0.02); bundle(P, False, f'carril_base_{n_}', nculm=3, clamp_every=0.8, twist=0.0)
    for sc in np.arange(0.0, arclen(P)[-1] + 0.1, 1.6):
        i = min(int(np.searchsorted(arclen(P), sc)), len(P) - 1); foot(P[i], np.array([0, 0, 1.0]))

# ---------------------------------------------------------------- cubierta de membrana
print('Cubierta...')
NR, NT = 16, 144
tops = np.array(list(mast_tops.values()))
def roof_z(x, y, rho):
    d = np.hypot(tops[:, 0] - x, tops[:, 1] - y)
    z = H + 0.12 + np.sum(0.78 * np.exp(-(d / 1.15) ** 2)) - 0.9 * max(rho - 1, 0) - 0.08 * (1 - rho) ** 2
    return min(z, H + MAST_H - 0.06)
V = []; UV = []; F = []
for j in range(NR + 1):
    rho = 1.16 * j / NR
    for i in range(NT):
        th = 360 * i / NT; p = env(th, 1.0); c = np.array([0.1, 0.2, H])
        x, y = c[0] + rho * (p[0] - c[0]), c[1] + rho * (p[1] - c[1])
        V.append((x, y, roof_z(x, y, rho))); UV.append((x / 1.5, y / 1.5))
for j in range(NR):
    for i in range(NT):
        a, b = j * NT + i, j * NT + (i + 1) % NT
        F.append((a, b, b + NT, a + NT))
add_mesh(V, F, UV, '05_Membrana_cubierta', 'membrana', 'Membrana cubierta', preview_step=1)

# cables: vientos de cada mástil a anclaje en el suelo + cables de cumbrera entre mástiles
for u0, top in mast_tops.items():
    anc = np.array([A * 1.34 * math.cos(math.radians(u0)), B_ * 1.34 * math.sin(math.radians(u0)), 0.0])
    tube(np.array([top, anc]), 0.008, '09_Cables', 'cable', nseg=6, uv_scale=(1, 1), name=f'viento_{u0}')
    cylinder(anc + [0, 0, -0.08], [0, 0, 1], 0.035, 0.3, 'acero', centered=False)
keys = list(mast_tops.keys())
for a_, b_ in zip(keys, keys[1:] + keys[:1]):
    pa, pb = mast_tops[a_], mast_tops[b_]; mid = (pa + pb) / 2 - [0, 0, 0.25]
    tube(np.array([pa, mid, pb]), 0.006, '09_Cables', 'cable', nseg=6, uv_scale=(1, 1))

# ---------------------------------------------------------------- tiras LED magenta
for key in ('O2_arco_entrada', 'R1_lente_der'):
    c = (BANDAS[key][0] if key in BANDAS else ROJAS[key]); P, closed, u, v = c.boundary(150)
    P = P + env_normal(u, v) * (RB + RC + 0.03)
    tube(P, 0.01, '10_LED_magenta', 'led', closed, nseg=8, uv_scale=(1, 1), name='LED ' + key)

# ---------------------------------------------------------------- interior: tarima, banco, pila, lámpara
print('Interior...')
def smooth_closed(pts, n=120):
    pts = np.asarray(pts, float); tck, _ = splprep([pts[:, 0], pts[:, 1]], s=0, per=True)
    x, y = splev(np.linspace(0, 1, n, endpoint=False), tck); return np.stack([x, y], 1)

deck = smooth_closed([(-2.9, -1.3), (-1.0, -2.75), (1.5, -3.0), (3.3, -1.9), (3.7, 0.5), (2.5, 2.3), (0.0, 2.6), (-2.3, 1.9), (-3.3, 0.3)])
n = len(deck); cx, cy = deck.mean(0)
V = [(x, y, 0.12) for x, y in deck] + [(cx, cy, 0.12)] + [(x, y, 0.0) for x, y in deck] + [(cx, cy, 0.0)]
UV = [(x / 1.0, y / 1.0) for x, y, _ in V]
F = [(i, (i + 1) % n, n) for i in range(n)] + [((i + 1) % n + n + 1, i + n + 1, 2 * n + 1) for i in range(n)]
F += [(i, i + n + 1, (i + 1) % n + n + 1, (i + 1) % n) for i in range(n)]
add_mesh(V, F, UV, '07_Madera_tarima_banco', 'madera', 'Tarima', preview_step=1)

# banco curvo a la derecha
tck, _ = splprep([[0.6, 1.6, 2.5, 3.0], [2.0, 1.6, 0.7, -0.6]], s=0)
bx, by = splev(np.linspace(0, 1, 40), tck); Pb = np.stack([bx, by, np.full(40, 0.34)], 1)
rect = [(-0.27, -0.2), (0.27, -0.2), (0.27, 0.2), (-0.27, 0.2), (-0.27, -0.2)]
sweep_mesh(Pb, rect, '07_Madera_tarima_banco', 'madera', uv_scale=(1, 1), name='Banco curvo')
for p in Pb[::13]: cylinder([p[0], p[1], 0.12], [0, 0, 1], 0.04, 0.14, 'acero', centered=False)

# pila de agua circular (izquierda) con lámpara-embudo de vidrio colgada encima
PC = np.array([-1.75, -0.5, 0.0])
cylinder(PC + [0, 0, 0.12], [0, 0, 1], 0.62, 0.42, 'madera_osc', lay='07_Madera_tarima_banco', centered=False)
cylinder(PC + [0, 0, 0.52], [0, 0, 1], 0.66, 0.05, 'acero', centered=False)
V = [(PC[0] + 0.6 * math.cos(a), PC[1] + 0.6 * math.sin(a), 0.56) for a in np.linspace(0, 2 * math.pi, 48, endpoint=False)] + [(PC[0], PC[1], 0.56)]
UV = [((x - PC[0]) / 1.2 + 0.5, (y - PC[1]) / 1.2 + 0.5) for x, y, _ in V]
add_mesh(V, [(i, (i + 1) % 48, 48) for i in range(48)], UV, '08_Agua', 'agua', 'Agua pila')
lampz = 2.25; top_r = roof_z(PC[0], PC[1], 0.5)
tube(np.array([[PC[0], PC[1], top_r], [PC[0], PC[1], lampz + 0.7]]), 0.01, '06_Acero', 'acero', nseg=6, uv_scale=(1, 1))
cone = [(0.0, 0.0)] + [(0.0, 0.0)]  # perfil cónico: radios 0 -> 0.24 a lo largo del eje vertical
Pc = np.array([[PC[0], PC[1], lampz], [PC[0], PC[1], lampz + 0.65]])
tube(Pc, 1.0, '11_Vidrio_lampara', 'vidrio', nseg=16, radii=[0.03, 0.24], uv_scale=(1, 1), name='Lampara embudo vidrio')
cylinder(PC + [0, 0, lampz + 0.65], [0, 0, 1], 0.25, 0.05, 'acero', centered=False)
tube(np.array([[PC[0], PC[1], 0.56], [PC[0], PC[1], lampz]]), 0.012, '11_Vidrio_lampara', 'vidrio', nseg=6, uv_scale=(1, 1), name='Chorro de agua')

# esferas y caja eléctrica en el ala derecha
for (u0, v0) in ((355, 0.55), (8, 0.22)):
    sphere(env(u0, v0) + env_normal(u0, v0) * 0.1, 0.25, 'acero')
p0 = env(347, 0.25); nrm = env_normal(347, 0.25); tt = np.cross([0, 0, 1], nrm); tt /= np.linalg.norm(tt); up = np.cross(nrm, tt)
corners = [p0 + a * tt * 0.17 + b * up * 0.24 + c * nrm * 0.07 for c in (0, 1) for b in (-1, 1) for a in (-1, 1)]
V = corners; F = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (1, 5, 7, 3), (0, 2, 6, 4)]
add_mesh(V, F, [(0, 0)] * 8, '06_Acero', 'acero', 'Caja electrica')

# ---------------------------------------------------------------- terreno y árboles
print('Terreno...')
V = [(0, 0, -0.01)]; F = []
for j in range(1, 13):
    rad = 18 * j / 12
    V += [(rad * math.cos(a), rad * math.sin(a), -0.01) for a in np.linspace(0, 2 * math.pi, 72, endpoint=False)]
F = [(0, 1 + i, 1 + (i + 1) % 72) for i in range(72)]
for j in range(11):
    b0, b1 = 1 + j * 72, 1 + (j + 1) * 72
    F += [(b0 + i, b1 + i, b1 + (i + 1) % 72, b0 + (i + 1) % 72) for i in range(72)]
add_mesh(V, F, [(x / 4, y / 4) for x, y, _ in V], '12_Terreno', 'suelo', 'Terreno')
g = np.random.default_rng(5)
for k in range(18):
    for _ in range(50):
        x, y = g.uniform(-16, 16), g.uniform(-6, 17)
        if (y > 5.5) or (abs(x) > 8.5 and y > -3): break
    h = g.uniform(11, 16); lean = g.normal(0, 0.35, 2)
    P = np.array([[x, y, -0.2], [x + lean[0] * 0.5, y + lean[1] * 0.5, h * 0.5], [x + lean[0], y + lean[1], h]])
    tube(P, 1.0, '13_Arboles', 'corteza', nseg=10, radii=[0.26, 0.17, 0.09], uv_scale=(0.25, 1), name=f'Tronco {k + 1}')

# =====================================================================
# 4. GUARDAR + VISTA PREVIA
# =====================================================================
ok = f.Write(OUT3DM, 8)
print('3dm escrito:', ok, OUT3DM, f'{os.path.getsize(OUT3DM) / 1e6:.1f} MB', 'objetos:', len(f.Objects))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
cam = np.array([0.8, -13.5, 2.6]); tgt = np.array([0.0, 0.4, 1.7]); light = np.array([-0.4, -0.5, 0.75]); light /= np.linalg.norm(light)
fw = tgt - cam; fw /= np.linalg.norm(fw); rt = np.cross(fw, [0, 0, 1]); rt /= np.linalg.norm(rt); upv = np.cross(rt, fw)
fl = 1.9; polys = []; cols = []; depth = []
for P, col, al in PREVIEW:
    d = P - cam; z = d @ fw
    if np.any(z < 0.3): continue
    xs = (d @ rt) / z * fl; ys = (d @ upv) / z * fl
    nrm = np.cross(P[1] - P[0], P[2] - P[0]); nn = np.linalg.norm(nrm)
    sh = 0.45 + 0.55 * abs(nrm @ light) / nn if nn > 1e-12 else 0.7
    polys.append(np.stack([xs, ys], 1)); cols.append((*(np.array(col) / 255 * sh), al)); depth.append(z.mean())
order = np.argsort(depth)[::-1]
fig = plt.figure(figsize=(14, 9.5), dpi=90); ax = fig.add_subplot(111); ax.set_facecolor((0.82, 0.85, 0.82))
ax.add_collection(PolyCollection([polys[i] for i in order], facecolors=[cols[i] for i in order], edgecolors='none', antialiased=True))
ax.set_xlim(-1.05, 1.05); ax.set_ylim(-0.55, 0.85); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0); fig.savefig(os.path.join(HERE, 'preview_pabellon.png'))
print('preview OK, poligonos:', len(polys))
