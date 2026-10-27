#!/usr/bin/env python3
"""Reconstrucción 3D del pabellón de bambú de la imagen de referencia -> PABELLON_BAMBU.3dm (Rhino 8).

Uso:  python3 generar_pabellon_bambu.py
Salida (misma carpeta): PABELLON_BAMBU.3dm, tex_*.png, vista_01_general.png, vista_02_interior.png,
                        vista_03_estructura.png, superposicion_referencia.png, dimensiones_estimadas.json
Unidades: metros. Ejes: X izquierda-derecha de la fachada, Y profundidad hacia el interior, Z altura.
Origen: centro del acceso principal a cota de pavimento. Parámetro maestro: ANCHO_TOTAL.
Todo se construye con rhino3dm (sin Rhino instalado).
"""
import os, math, json
import numpy as np
import rhino3dm as r
from PIL import Image
from scipy.interpolate import splprep, splev
from scipy.spatial import cKDTree, Delaunay

HERE = os.path.dirname(os.path.abspath(__file__))
OUT3DM = os.path.join(HERE, 'PABELLON_BAMBU.3dm')
REF_IMG = os.path.join(HERE, 'referencia.png')
rng = np.random.default_rng(7)

# =====================================================================
# 0. PARÁMETROS MAESTROS (hipótesis de trabajo, no medidas verificadas)
# =====================================================================
ANCHO_TOTAL = 10.0                 # anchura total aparente de la fachada (parámetro maestro)
S = ANCHO_TOTAL / 10.0             # factor de escala global: todo lo demás se deriva de él
A, B_, H = 4.45 * S, 2.95 * S, 3.55 * S   # semiejes de la planta base y altura media del anillo superior
U_ACCESO = 283.0                   # ángulo en planta del centro del acceso (grados; 0=+X, 90=+Y)
MAST_H = {168: 0.5, 212: 0.6, 258: 0.7, 303: 0.8, 350: 0.75, 32: 0.9, 68: 1.1, 120: 1.1}   # altura de cada mástil sobre el anillo (m, x S)
R_CANA = 0.040 * S                 # radio medio de caña (Ø80 mm; rango 60-100 mm por pieza)
E_PERF = 0.030 * S                 # espesor de las piezas perforadas (hipótesis 20-40 mm)
VISIBLE = (158.0, 388.0)           # rango de ángulos (u) visible desde la cámara; el resto son hipótesis
LENTE_MM, CAM_POS, CAM_TGT = 30.0, (0.3, -8.2, 1.95), (0.0, 2.0, 1.7)   # cámara de referencia (ajustada por superposición)
IMG_W, IMG_H = Image.open(REF_IMG).size

# =====================================================================
# 1. TEXTURAS PROCEDURALES (tex_*.png junto al .3dm)
# =====================================================================
def save(name, arr):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(os.path.join(HERE, name)); return name

def noise2(h, w, scale, seed):
    g = np.random.default_rng(seed).random((max(2, h // scale + 2), max(2, w // scale + 2)))
    return np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(float) / 255

def streaks(h, w, nx, seed):
    n = np.random.default_rng(seed).random((h // 2, max(2, nx)))
    return np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)) / 255

def tex_bambu():  # tesela = 1,32 m de caña (4 nudos) x perímetro
    h, w = 1024, 256; y = np.arange(h)[:, None]
    base = np.array([204., 160., 86.])
    img = base[None, None, :] * (0.80 + 0.26 * streaks(h, w, 18, 1) + 0.10 * noise2(h, w, 48, 2))[..., None]
    img[..., 2] *= 0.9 + 0.2 * streaks(h, w, 30, 3)          # vetas longitudinales con matiz
    img *= (1 - 0.12 * (noise2(h, w, 3, 4) > 0.9))[..., None]  # marcas pequeñas
    for k in range(4):
        d = np.abs(y - (k * 256 + 128))
        img[(d < 9)[:, 0]] *= 0.55; img[((d >= 9) & (d < 15))[:, 0]] *= 1.10
    return save('tex_bambu.png', img)

def tex_marfil():
    S_ = 512
    img = np.ones((S_, S_, 3)) * np.array([236., 228., 212.]) * (0.93 + 0.1 * noise2(S_, S_, 6, 11) + 0.04 * noise2(S_, S_, 60, 12))[..., None]
    img *= (1 - 0.08 * (noise2(S_, S_, 2, 13) > 0.88))[..., None]   # porosidad fina
    return save('tex_marfil.png', img)

def tex_vidrio(name, base, line, seed, n=70):
    S_ = 512; g = np.random.default_rng(seed); seeds = g.random((n, 2)) * S_
    pts = np.concatenate([seeds + np.array([ox, oy]) for ox in (-S_, 0, S_) for oy in (-S_, 0, S_)])
    yy, xx = np.mgrid[0:S_, 0:S_]; q = np.stack([xx.ravel(), yy.ravel()], 1)
    d, i = cKDTree(pts).query(q, k=2)
    d1, d2 = d[:, 0].reshape(S_, S_), d[:, 1].reshape(S_, S_)
    edge = np.clip((4.0 - (d2 - d1)) / 4.0, 0, 1)
    var = (g.random(n) * 0.35 + 0.8)[(i[:, 0] % n).reshape(S_, S_)]
    img = np.array(base, float)[None, None, :] * var[..., None] * (0.8 + 0.4 * noise2(S_, S_, 20, seed + 1))[..., None]
    img = img * (1 - edge[..., None]) + np.array(line, float)[None, None, :] * edge[..., None]
    return save(name, img)

def tex_membrana():
    S_ = 512; y = np.arange(S_)[:, None]; x = np.arange(S_)[None, :]
    img = np.ones((S_, S_, 3)) * 250 - (((x % 16 == 0) | (y % 16 == 0)).astype(float) * 10)[..., None]
    img *= (0.96 + 0.08 * noise2(S_, S_, 24, 5))[..., None]
    return save('tex_membrana.png', img)

def tex_madera(name, base, plank, seed):
    S_ = 512; y = np.arange(S_)[:, None]; g = np.random.default_rng(seed); row = y // plank
    tint = (g.random(S_ // plank + 1) * 0.3 + 0.78)[row[:, 0]][:, None]
    grain = 0.72 + 0.5 * np.asarray(Image.fromarray((g.random((S_ // 24, S_)) * 255).astype(np.uint8)).resize((S_, S_), Image.BICUBIC)) / 255
    img = np.array(base, float)[None, None, :] * (tint * grain)[..., None] * (0.9 + 0.2 * noise2(S_, S_, 40, seed + 1))[..., None]
    img[(y % plank < 2)[:, 0]] = [38, 28, 18]
    return save(name, img)

def tex_agua():
    S_ = 512; y = np.arange(S_)[:, None] - S_ / 2; x = np.arange(S_)[None, :] - S_ / 2; rr = np.hypot(x, y)
    rip = np.sin(rr / 7.0) * np.exp(-rr / 150) + 0.4 * np.sin(np.hypot(x - 60, y + 40) / 6) * np.exp(-np.hypot(x - 60, y + 40) / 90)
    img = np.array([70., 92., 104.])[None, None, :] * (1 + 0.35 * rip)[..., None] + (np.clip(1 - rr / 256, 0, 1) * 28)[..., None]
    return save('tex_agua.png', img)

def tex_suelo():
    S_ = 1024
    img = np.ones((S_, S_, 3)) * np.array([62., 48., 36.]) * (0.65 + 0.7 * noise2(S_, S_, 6, 21))[..., None]
    moss = np.clip((noise2(S_, S_, 48, 22) - 0.42) * 4, 0, 1) * (0.5 + 0.5 * noise2(S_, S_, 8, 23))
    img = img * (1 - moss[..., None]) + np.array([80., 122., 44.])[None, None, :] * (0.7 + 0.6 * noise2(S_, S_, 3, 24))[..., None] * moss[..., None]
    img[noise2(S_, S_, 2, 25) > 0.94] = [150, 132, 100]
    return save('tex_suelo_musgo.png', img)

def tex_corteza():
    h, w = 1024, 256
    img = np.array([96., 86., 76.])[None, None, :] * (0.55 + 0.9 * streaks(h, w, 12, 31))[..., None] * (0.85 + 0.3 * noise2(h, w, 16, 32))[..., None]
    return save('tex_corteza.png', img)

print('Texturas...')
T_BAMBU = tex_bambu(); T_MARFIL = tex_marfil(); T_CORTEZA = tex_corteza()
T_ROJO = tex_vidrio('tex_vidrio_rojo.png', (176, 12, 30), (64, 0, 10), 41)
T_AMAR = tex_vidrio('tex_vidrio_ambar.png', (234, 178, 40), (118, 68, 10), 43, n=55)
T_MEMB = tex_membrana(); T_TARIMA = tex_madera('tex_tarima.png', (150, 104, 60), 512, 61)
T_BANCO = tex_madera('tex_banco.png', (172, 122, 70), 128, 63); T_AGUA = tex_agua(); T_SUELO = tex_suelo()

# =====================================================================
# 2. ARCHIVO, CAPAS, MATERIALES
# =====================================================================
f = r.File3dm()
f.Settings.ModelUnitSystem = r.UnitSystem.Meters; f.Settings.ModelAbsoluteTolerance = 0.001

LAYER_DEFS = [('00_Referencia_y_camaras', (120, 120, 120)), ('01_Curvas_maestras', (120, 90, 40)), ('02_Bambu_principal', (210, 165, 90)),
              ('03_Bambu_secundario', (190, 150, 90)), ('04_Nudos_y_abrazaderas', (150, 155, 160)), ('05_Apoyos', (120, 125, 130)),
              ('06_Cables_y_tensores', (200, 200, 200)), ('07_Membranas', (240, 240, 240)), ('08_Piezas_perforadas', (236, 228, 212)),
              ('09_Paneles_rojos', (176, 12, 30)), ('10_Paneles_ambar', (234, 178, 40)), ('11_Pavimento', (150, 104, 60)),
              ('12_Bancos', (172, 122, 70)), ('13_Elemento_de_agua', (70, 92, 104)), ('14_Dispositivos_visibles', (160, 160, 165)),
              ('15_Entorno', (70, 55, 40)), ('16_Elementos_ocultos_propuestos', (255, 0, 255))]
L = {}
def layer(name, rgb, parent=None, visible=True):
    Ly = r.Layer(); Ly.Name = name; Ly.Color = (rgb[0], rgb[1], rgb[2], 255); Ly.Visible = visible
    if parent is not None: Ly.ParentLayerId = f.Layers[L[parent]].Id
    L[name if parent is None else parent + '/' + name] = f.Layers.Add(Ly)
for name, rgb in LAYER_DEFS: layer(name, rgb)
for name, rgb in LAYER_DEFS[1:16]:  # subcapas de hipótesis con el mismo nombre que la capa observada
    layer(name, rgb, parent='16_Elementos_ocultos_propuestos')
layer('Cimentacion_propuesta', (255, 0, 255), parent='16_Elementos_ocultos_propuestos', visible=False)
f.Layers[L['00_Referencia_y_camaras']].Visible = False

def texture(fn, ttype):
    t = r.Texture(); t.FileName = fn; t.TextureType = ttype; return t

def material(name, rgb, tex=None, transp=0.0, refl=0.0, shine=0.0, emis=None, metallic=0.0, rough=0.6, opacity=None, ior=1.5):
    m = r.Material(); m.Name = name; m.DiffuseColor = (rgb[0], rgb[1], rgb[2], 255)
    m.Transparency = transp; m.Reflectivity = refl; m.Shine = shine
    if emis: m.EmissionColor = (emis[0], emis[1], emis[2], 255)
    if tex: m.SetBitmapTexture(texture(tex, r.TextureType.Bitmap))
    m.ToPhysicallyBased(); p = m.PhysicallyBased
    p.BaseColor = (rgb[0], rgb[1], rgb[2], 255); p.Metallic = metallic; p.Roughness = rough
    p.Opacity = (1.0 - transp) if opacity is None else opacity; p.OpacityIOR = ior
    if emis: p.EmissionColor = (emis[0], emis[1], emis[2], 255)
    return f.Materials.Add(m)

M = {
    'bambu': material('Bambu dorado (satinado humedo)', (204, 160, 86), T_BAMBU, shine=0.3, refl=0.08, rough=0.38),
    'marfil': material('Pieza perforada marfil mate [interpretacion: compuesto mineral]', (236, 228, 212), T_MARFIL, rough=0.85),
    'rojo': material('Panel translucido rojo rubi [material no verificado]', (176, 12, 30), T_ROJO, transp=0.45, refl=0.25, shine=0.7, rough=0.15),
    'ambar': material('Panel translucido ambar [material no verificado]', (234, 178, 40), T_AMAR, transp=0.45, refl=0.25, shine=0.7, rough=0.15),
    'membrana': material('Membrana transparente tensada', (250, 250, 250), T_MEMB, transp=0.6, refl=0.15, shine=0.6, rough=0.2),
    'acero': material('Acero gris plateado (humedo)', (198, 202, 208), refl=0.55, shine=0.8, metallic=0.9, rough=0.35),
    'tarima': material('Tarima madera humeda', (150, 104, 60), T_TARIMA, shine=0.35, refl=0.12, rough=0.45),
    'banco': material('Banco madera', (172, 122, 70), T_BANCO, shine=0.3, refl=0.08, rough=0.5),
    'madera_osc': material('Madera oscura borde pila', (84, 56, 32), shine=0.3, rough=0.5),
    'agua': material('Agua', (70, 92, 104), T_AGUA, transp=0.3, refl=0.6, shine=0.95, rough=0.03),
    'cable': material('Cable acero', (190, 190, 195), shine=0.4, metallic=0.8, rough=0.4),
    'led': material('LED magenta', (230, 30, 140), emis=(230, 30, 140)),
    'vidrio': material('Vidrio recipiente suspendido [interpretacion]', (220, 235, 240), transp=0.8, refl=0.3, shine=0.9, rough=0.05),
    'suelo': material('Terreno humedo con musgo', (62, 48, 36), T_SUELO, refl=0.1, rough=0.9),
    'corteza': material('Corteza', (96, 86, 76), T_CORTEZA, rough=0.9),
    'referencia': material('Imagen de referencia', (255, 255, 255), 'referencia.png', rough=1.0),
}

def attrs(lay, mat, name=None, hidden=False):
    a = r.ObjectAttributes()
    a.LayerIndex = L['16_Elementos_ocultos_propuestos/' + lay] if (hidden and ('16_Elementos_ocultos_propuestos/' + lay) in L) else L[lay]
    a.MaterialIndex = M[mat]; a.MaterialSource = r.ObjectMaterialSource.MaterialFromObject
    if name: a.Name = name
    return a

def is_hidden(u):  # ángulo (grados) fuera del rango visible desde la cámara -> hipótesis
    u = u % 360
    return not (VISIBLE[0] <= u <= VISIBLE[1] or VISIBLE[0] <= u + 360 <= VISIBLE[1])

# ----------------------------------------------------------------- vista previa
PREVIEW = []  # (polígono Nx3, color, alpha, capa)
PREV_COL = {'bambu': (205, 160, 85), 'marfil': (236, 228, 212), 'rojo': (170, 15, 30), 'ambar': (232, 178, 40), 'membrana': (245, 245, 245),
            'acero': (185, 190, 196), 'tarima': (140, 98, 58), 'banco': (170, 120, 70), 'madera_osc': (84, 56, 32), 'agua': (80, 100, 110),
            'cable': (200, 200, 200), 'led': (230, 30, 140), 'vidrio': (210, 230, 240), 'suelo': (62, 50, 38), 'corteza': (95, 85, 75), 'referencia': (255, 255, 255)}
PREV_ALPHA = {'rojo': 0.7, 'ambar': 0.7, 'membrana': 0.45, 'vidrio': 0.5, 'agua': 0.85}
STATS = {}

XY_MAP = r.TextureMapping.CreatePlaneMapping(r.Plane.WorldXY(), r.Interval(0, 1), r.Interval(0, 1), r.Interval(0, 1))

def make_mesh(V, F, UV):
    m = r.Mesh()
    for p in V: m.Vertices.Add(float(p[0]), float(p[1]), float(p[2]))
    for fc in F:
        if len(fc) == 4: m.Faces.AddFace(int(fc[0]), int(fc[1]), int(fc[2]), int(fc[3]))
        else: m.Faces.AddFace(int(fc[0]), int(fc[1]), int(fc[2]))
    m.SetTextureCoordinates(XY_MAP, r.Transform.Identity(), False)
    tc = m.TextureCoordinates
    for i, uv in enumerate(UV): tc[i] = r.Point2f(float(uv[0]), float(uv[1]))
    m.Normals.ComputeNormals(); m.Compact()
    return m

def add_mesh(V, F, UV, lay, mat, name=None, hidden=False, preview_step=1):
    if len(F) == 0: return
    f.Objects.AddMesh(make_mesh(V, F, UV), attrs(lay, mat, name, hidden))
    STATS[lay] = STATS.get(lay, 0) + len(F)
    V = np.asarray(V)
    for fc in F[::preview_step]:
        Q = V[list(fc)]
        if len(fc) == 4 and np.max(np.linalg.norm(Q - np.roll(Q, 1, 0), axis=1)) > 0.7:
            n_ = int(min(6, np.ceil(np.max(np.linalg.norm(Q - np.roll(Q, 1, 0), axis=1)) / 0.5)))
            for a in range(n_):
                for b in range(n_):
                    bl = lambda u_, v_: (1 - u_) * (1 - v_) * Q[0] + u_ * (1 - v_) * Q[1] + u_ * v_ * Q[2] + (1 - u_) * v_ * Q[3]
                    PREVIEW.append((np.array([bl(a / n_, b / n_), bl((a + 1) / n_, b / n_), bl((a + 1) / n_, (b + 1) / n_), bl(a / n_, (b + 1) / n_)]), PREV_COL[mat], PREV_ALPHA.get(mat, 1.0), lay))
        else: PREVIEW.append((Q, PREV_COL[mat], PREV_ALPHA.get(mat, 1.0), lay))

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
    if closed:
        b = np.cross(T[-1], T[0]); nb = np.linalg.norm(b)
        Ne = N[-1] if nb < 1e-9 else rot(N[-1], b, math.acos(np.clip(T[-1] @ T[0], -1, 1)))
        Ne -= (Ne @ T[0]) * T[0]; Ne /= np.linalg.norm(Ne)
        phi = math.atan2(np.cross(N[0], Ne) @ T[0], N[0] @ Ne)
        for i in range(n): N[i] = rot(N[i], T[i], -phi * i / n)
    return T, N, np.cross(T, N)

def arclen(P):
    return np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])

def resample(P, s_new, closed=False):
    """Puntos de la polilínea P en las longitudes de arco s_new (interpolación lineal)."""
    Pp = np.vstack([P, P[:1]]) if closed else P
    s = arclen(Pp)
    return np.stack([np.interp(s_new, s, Pp[:, k]) for k in range(3)], 1), s[-1]

def rings(P, closed, profile, radii, roll=0.0):
    T, N, B = frames(P, closed); n = len(P)
    idx = list(range(n)) + ([0] if closed else [])
    c, sn = math.cos(roll), math.sin(roll)
    out = []
    for i in idx:
        out.append([P[i] + radii[i] * ((a * c - b * sn) * N[i] + (a * sn + b * c) * B[i]) for (a, b) in profile])
    return np.array(out), T, N, B

def quads(rows, k, base=0):
    return [(base + i * k + j, base + (i + 1) * k + j, base + (i + 1) * k + j + 1, base + i * k + j + 1) for i in range(rows - 1) for j in range(k - 1)]

CIRC = lambda nseg: [(math.cos(2 * math.pi * k / nseg), math.sin(2 * math.pi * k / nseg)) for k in range(nseg + 1)]

def sweep(P, profile, lay, mat, closed=False, radii=None, uv_scale=(1.0, 1.0), roll=0.0, name=None, hidden=False, preview_step=1, hollow=0.0):
    """Barre un perfil (lista de (a,b); cerrado si el primero == último) por la polilínea P. hollow>0: extremos huecos (pared = hollow*radio)."""
    P = np.asarray(P, float); n = len(P)
    rad = np.ones(n) if radii is None else np.asarray(radii, float)
    R, T, N, B = rings(P, closed, profile, rad, roll)
    Pr = np.vstack([P, P[:1]]) if closed else P; s = arclen(Pr); k = len(profile)
    V = list(R.reshape(-1, 3)); UV = [(s[i] * uv_scale[0], j / (k - 1) * uv_scale[1]) for i in range(len(R)) for j in range(k)]
    F = quads(len(R), k)
    if hollow > 0 and not closed:  # interior hueco en los extremos expuestos
        for end in (0, -1):
            i0 = 0 if end == 0 else n - 1
            depth = min(0.22 * S, s[-1] * 0.3); i1 = int(np.searchsorted(s, depth)) if end == 0 else int(np.searchsorted(s, s[-1] - depth)) - 1
            i1 = max(1, min(n - 2, i1))
            sub = P[i0:i1 + 1] if end == 0 else P[i1:i0 + 1][::-1]
            if len(sub) < 2: continue
            Ri, _, _, _ = rings(sub, False, profile, rad[[i0] * len(sub)] * (1 - hollow), roll)
            base = len(V); V += list(Ri.reshape(-1, 3)); UV += [(0.0, j / (k - 1)) for _ in range(len(Ri)) for j in range(k)]
            F += quads(len(Ri), k, base)
            outer = (i0 * k)  # anillo exterior del extremo
            F += [(outer + j, outer + j + 1, base + j + 1, base + j) for j in range(k - 1)]
    add_mesh(V, F, UV, lay, mat, name, hidden, preview_step)

def xform_at(p, n, xdir=None):
    """Transformación que lleva el plano XY del origen al punto p con normal n."""
    p = np.asarray(p, float); n = np.asarray(n, float); n = n / np.linalg.norm(n)
    if xdir is None:
        a = np.array([0, 0, 1.]) if abs(n[2]) < 0.9 else np.array([1, 0, 0.]); xdir = np.cross(a, n)
    xdir = np.asarray(xdir, float); xdir -= (xdir @ n) * n; xdir /= np.linalg.norm(xdir); ydir = np.cross(n, xdir)
    pl = r.Plane(r.Point3d(*p), r.Vector3d(*xdir), r.Vector3d(*ydir))
    return r.Transform.PlaneToPlane(r.Plane.WorldXY(), pl), (xdir, ydir, n)

# ----------------------------------------------------------------- geometría de bloques (mallas locales)
def box_mesh(cx, cy, cz, sx, sy, sz, mat, lay):
    c = np.array([cx, cy, cz]); h = np.array([sx, sy, sz]) / 2
    V = [c + h * np.array([a, b, d]) for d in (-1, 1) for b in (-1, 1) for a in (-1, 1)]
    F = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (1, 3, 7, 5), (0, 4, 6, 2)]
    return (V, F, [(0, 0)] * 8, lay, mat)

def ring_mesh(ro, ri, z0, z1, nseg, mat, lay):  # anillo (banda) entre radios ro>ri, de z0 a z1, eje Z
    V = []; F = []
    for z in (z0, z1):
        for rad in (ro, ri):
            V += [(rad * math.cos(a), rad * math.sin(a), z) for a in np.linspace(0, 2 * math.pi, nseg, endpoint=False)]
    def q(r0, r1, flip=False):
        return [((r0 + i, r0 + (i + 1) % nseg, r1 + (i + 1) % nseg, r1 + i) if not flip else (r0 + i, r1 + i, r1 + (i + 1) % nseg, r0 + (i + 1) % nseg)) for i in range(nseg)]
    F += q(0, 2 * nseg) + q(nseg, 3 * nseg, True) + q(0, nseg, True) + q(2 * nseg, 3 * nseg)
    return (V, F, [(0, 0)] * len(V), lay, mat)

def cyl_mesh(rad, z0, z1, nseg, mat, lay, cx=0.0, cy=0.0):
    V = [(cx + rad * math.cos(a), cy + rad * math.sin(a), z) for z in (z0, z1) for a in np.linspace(0, 2 * math.pi, nseg, endpoint=False)]
    V += [(cx, cy, z0), (cx, cy, z1)]; c0, c1 = 2 * nseg, 2 * nseg + 1
    F = [(i, (i + 1) % nseg, nseg + (i + 1) % nseg, nseg + i) for i in range(nseg)]
    F += [(c0, (i + 1) % nseg, i) for i in range(nseg)] + [(c1, nseg + i, nseg + (i + 1) % nseg) for i in range(nseg)]
    return (V, F, [(0, 0)] * len(V), lay, mat)

def hex_nut(cx, cy, z0, z1, rad, mat, lay): return cyl_mesh(rad, z0, z1, 6, mat, lay, cx, cy)

def sphere_mesh(rad, mat, lay, cz=0.0, nu=16, nv=8):
    V = [(rad * math.cos(b) * math.cos(a), rad * math.cos(b) * math.sin(a), cz + rad * math.sin(b)) for j in range(nv + 1) for b in [math.pi * j / nv - math.pi / 2] for a in np.linspace(0, 2 * math.pi, nu, endpoint=False)]
    F = [(j * nu + i, j * nu + (i + 1) % nu, (j + 1) * nu + (i + 1) % nu, (j + 1) * nu + i) for j in range(nv) for i in range(nu)]
    return (V, F, [(0, 0)] * len(V), lay, mat)

def shift(part, dx, dy, dz):
    V, F, UV, lay, mat = part; return ([(x + dx, y + dy, z + dz) for x, y, z in V], F, UV, lay, mat)

def swap_yz(part):  # gira la pieza: su eje Z pasa a Y
    V, F, UV, lay, mat = part; return ([(x, z, y) for x, y, z in V], F, UV, lay, mat)

BLOCKS = {}
def block(name, parts):
    """Define un bloque (instancia) a partir de piezas (V,F,UV,capa,material)."""
    if name in BLOCKS: return BLOCKS[name]
    geo = []; att = []
    for (V, F, UV, lay, mat) in parts:
        geo.append(make_mesh(V, F, UV)); att.append(attrs(lay, mat))
    idx = f.InstanceDefinitions.Add(name, 'Componente repetido del pabellon', '', '', r.Point3d(0, 0, 0), tuple(geo), tuple(att))
    BLOCKS[name] = (f.InstanceDefinitions[idx].Id, parts); return BLOCKS[name]

def place(name, p, n, lay, xdir=None, hidden=False, tag=None):
    bid, parts = BLOCKS[name]
    xf, (xd, yd, nd) = xform_at(p, n, xdir)
    a = attrs(lay, 'acero', tag or name, hidden); a.MaterialSource = r.ObjectMaterialSource.MaterialFromLayer
    f.Objects.AddInstanceObject(r.InstanceReference(bid, xf), a)
    STATS['instancias'] = STATS.get('instancias', 0) + 1
    p = np.asarray(p, float); Mx = np.stack([xd, yd, nd], 1)
    for (V, F, UV, lay_, mat) in parts:
        Vw = np.asarray(V) @ Mx.T + p
        for fc in F[::2]: PREVIEW.append((Vw[list(fc)], PREV_COL[mat], 1.0, lay))

def def_blocks(rb):
    """Bloques para un radio de haz rb: abrazadera, apoyo, cimentación, remate, tensor, anclaje, pie de banco."""
    k = f'{rb:.3f}'; LA = '04_Nudos_y_abrazaderas'; LP = '05_Apoyos'; LC = '06_Cables_y_tensores'
    if 'ABR_' + k not in BLOCKS:
        band = [ring_mesh(rb + 0.012, rb + 0.004, -0.03, 0.03, 20, 'acero', LA)]
        for sx in (1, -1):  # orejetas con tornillo y tuerca a ambos lados
            band.append(box_mesh(sx * (rb + 0.035), 0, 0, 0.05, 0.012, 0.06, 'acero', LA))
            for sz in (-0.018, 0.018):
                band.append(shift(swap_yz(cyl_mesh(0.005, -0.016, 0.016, 8, 'acero', LA)), sx * (rb + 0.035), 0, sz))
                band.append(shift(swap_yz(hex_nut(0, 0, -0.022, -0.016, 0.009, 'acero', LA)), sx * (rb + 0.035), 0, sz))
        block('ABR_' + k, band)
    if 'APOYO_' + k not in BLOCKS:
        parts = [box_mesh(0, 0, 0.01, 0.34, 0.34, 0.02, 'acero', LP),                      # placa base
                 ring_mesh(rb + 0.02, rb + 0.012, 0.02, 0.34, 20, 'acero', LP),            # casquillo vertical
                 ring_mesh(rb + 0.03, rb + 0.02, 0.26, 0.32, 20, 'acero', LP),             # banda de cierre
                 cyl_mesh(rb + 0.012, 0.02, 0.1, 20, 'acero', LP)]                         # fondo del casquillo
        for (x, y) in ((0.13, 0.13), (-0.13, 0.13), (0.13, -0.13), (-0.13, -0.13)):
            parts.append(cyl_mesh(0.007, 0.02, 0.05, 8, 'acero', LP, x, y)); parts.append(hex_nut(x, y, 0.02, 0.034, 0.012, 'acero', LP))
        for a in (0, 90, 180, 270):  # cartelas
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            V = [(ca * (rb + 0.02), sa * (rb + 0.02), 0.02), (ca * 0.15, sa * 0.15, 0.02), (ca * (rb + 0.02), sa * (rb + 0.02), 0.22)]
            V += [(x - sa * 0.006, y + ca * 0.006, z) for x, y, z in V]
            parts.append((V, [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], [(0, 0)] * 6, LP, 'acero'))
        block('APOYO_' + k, parts)
    if 'CIMENTACION' not in BLOCKS:
        block('CIMENTACION', [box_mesh(0, 0, -0.22, 0.6, 0.6, 0.4, 'acero', LP)])
    if 'REMATE_' + k not in BLOCKS:
        block('REMATE_' + k, [ring_mesh(rb + 0.015, rb - 0.005, -0.1, 0.02, 20, 'acero', LA), cyl_mesh(rb - 0.005, 0.0, 0.03, 20, 'acero', LA),
                              cyl_mesh(0.012, 0.03, 0.12, 8, 'acero', LA), sphere_mesh(0.055, 'acero', LA, 0.17), swap_yz(ring_mesh(0.03, 0.018, -0.006, 0.006, 12, 'acero', LC))])
    if 'TENSOR' not in BLOCKS:
        block('TENSOR', [cyl_mesh(0.012, -0.08, 0.08, 10, 'acero', LC), ring_mesh(0.02, 0.011, -0.125, -0.08, 10, 'acero', LC),
                         ring_mesh(0.02, 0.011, 0.08, 0.125, 10, 'acero', LC), hex_nut(0, 0, -0.095, -0.08, 0.016, 'acero', LC), hex_nut(0, 0, 0.08, 0.095, 0.016, 'acero', LC)])
    if 'ANCLAJE' not in BLOCKS:
        block('ANCLAJE', [cyl_mesh(0.03, -0.1, 0.25, 10, 'acero', LP), ring_mesh(0.05, 0.03, 0.25, 0.3, 12, 'acero', LP), box_mesh(0, 0, 0.005, 0.2, 0.2, 0.01, 'acero', LP)])
    if 'PIE_BANCO' not in BLOCKS:
        block('PIE_BANCO', [cyl_mesh(0.025, 0.0, 0.33, 10, 'acero', '12_Bancos'), box_mesh(0, 0, 0.005, 0.12, 0.12, 0.01, 'acero', '12_Bancos'), box_mesh(0, 0, 0.335, 0.14, 0.3, 0.01, 'acero', '12_Bancos')])
    if 'GRAPA' not in BLOCKS:
        block('GRAPA', [box_mesh(0, 0, 0.008, 0.03, 0.05, 0.016, 'acero', LA)])

def add_curve(P, lay, closed=False, degree=3, hidden=False, name=None):
    pts = r.Point3dList(len(P) + (1 if closed else 0))
    for p in P: pts.Add(float(p[0]), float(p[1]), float(p[2]))
    if closed: pts.Add(float(P[0][0]), float(P[0][1]), float(P[0][2]))
    c = r.NurbsCurve.Create(False, degree, pts)
    a = r.ObjectAttributes(); a.LayerIndex = L['16_Elementos_ocultos_propuestos/' + lay] if hidden else L[lay]
    if name: a.Name = name
    f.Objects.AddCurve(c, a)

# =====================================================================
# 3. ENVOLVENTE PARAMÉTRICA (u = ángulo en planta en grados, v = 0 suelo .. 1 anillo superior)
# =====================================================================
def env_raw(u, v):
    u = np.radians(np.asarray(u, float)); v = np.asarray(v, float); vc = np.clip(v, 0, 1)
    rr = 1 + 0.14 * np.sin(np.pi * vc) - 0.30 * v ** 2
    rr = rr * (1 + 0.05 * np.sin(3 * u + 0.7) * (1 - vc))                 # irregularidad orgánica
    rr = rr * (1 + 0.09 * np.sin(np.pi * vc) * np.maximum(np.cos(u), 0) ** 1.5)  # abombamiento del lateral derecho
    z = H * v * (1 + 0.06 * np.cos(u - math.radians(200)))                # anillo más alto a la izquierda, desciende hacia la derecha
    return np.stack([A * rr * np.cos(u), B_ * rr * np.sin(u), z], -1)

ORIGEN = env_raw(U_ACCESO, 0.0) * np.array([1, 1, 0])   # el origen del modelo es el centro del acceso a cota 0
def env(u, v): return env_raw(u, v) - ORIGEN
CENTRO = (env(0, 0.5) + env(180, 0.5)) / 2

def env_normal(u, v):
    du = env(np.asarray(u, float) + 0.5, v) - env(np.asarray(u, float) - 0.5, v); dv = env(u, np.asarray(v, float) + 0.01) - env(u, np.asarray(v, float) - 0.01)
    n = np.cross(du, dv); n = n / np.linalg.norm(n, axis=-1, keepdims=True)
    c = env(u, v) - CENTRO
    out = np.sign(np.sum(n[..., :2] * c[..., :2], -1))
    return n * np.where(out == 0, 1, out)[..., None]

def metric(u, v):  # metros por grado (horizontal) y por unidad de v (vertical) en ese punto
    return np.linalg.norm(env(u + 0.5, v) - env(u - 0.5, v)), np.linalg.norm(env(u, v + 0.01) - env(u, v - 0.01)) * 100

wrap = lambda d: (d + 180) % 360 - 180

class Cell:
    """Elipse irregular en el espacio (u, v): radio normalizado modulado por armónicos (conserva asimetrías)."""
    def __init__(self, uc, vc, du, dv, seed, a_cos=0.0, a_sin=0.0):
        self.uc, self.vc, self.du, self.dv = uc, vc, du, dv
        g = np.random.default_rng(seed); self.h = [(g.uniform(0.03, 0.08), g.uniform(0, 6.28)), (g.uniform(0.02, 0.05), g.uniform(0, 6.28))]
        self.a_cos, self.a_sin = a_cos, a_sin
    def rho(self, t):
        return 1 + self.h[0][0] * np.sin(2 * t + self.h[0][1]) + self.h[1][0] * np.sin(3 * t + self.h[1][1]) + self.a_cos * np.cos(t) + self.a_sin * np.sin(t)
    def inside(self, u, v):
        x, y = wrap(u - self.uc) / self.du, (v - self.vc) / self.dv
        return np.hypot(x, y) < self.rho(np.arctan2(y, x))
    def angle(self, u, v): return math.degrees(math.atan2((v - self.vc) / self.dv, wrap(u - self.uc) / self.du))
    def boundary(self, n=180):
        t = np.linspace(0, 2 * math.pi, n, endpoint=False); rho = self.rho(t)
        u = self.uc + self.du * rho * np.cos(t); v = self.vc + self.dv * rho * np.sin(t)
        if v.min() >= 0: return u, np.clip(v, 0, 1.0), True
        ok = v >= 0; k0 = int(np.argmin(ok))      # empezar justo después del tramo enterrado
        order = [(k0 + i) % n for i in range(n)]; u, v, ok = u[order], v[order], ok[order]
        i0 = int(np.argmax(ok)); i1 = n - int(np.argmax(ok[::-1]))
        return u[i0:i1], np.clip(v[i0:i1], 0, 1.0), False

# Celdas. Ángulos en grados (0 = +X derecha, 90 = fondo, U_ACCESO = frente). Las del fondo (u 25-155) son hipótesis.
ABIERTAS = {'O1_anillo_izq': Cell(221, 0.46, 25, 0.44, 1), 'O2_acceso': Cell(U_ACCESO, 0.30, 24, 0.62, 2, a_cos=0.10),
            'O3_hueco_der': Cell(331, 0.42, 15, 0.36, 3), 'O4_arco_trasero': Cell(95, 0.30, 22, 0.52, 4),
            'O5_anillo_tras_der': Cell(40, 0.45, 13, 0.32, 5), 'O6_anillo_tras_izq': Cell(145, 0.45, 13, 0.32, 6)}
BANDAS = {'O1_anillo_izq': (Cell(221, 0.48, 33, 0.50, 11), (95, 290)), 'O2_acceso': (Cell(U_ACCESO, 0.30, 29, 0.74, 12, a_cos=0.08), (60, 200)),
          'O3_hueco_der': (Cell(331, 0.42, 20, 0.46, 13), (-50, 120)), 'O4_arco_trasero': (Cell(95, 0.30, 28, 0.62, 14), (0, 180))}
ROJAS = {'R1_lente_der': Cell(6, 0.45, 11, 0.38, 21)}
AMBAR = {'Y1_izq_alta': Cell(182, 0.62, 21, 0.30, 31), 'Y2_centro_der': Cell(313, 0.56, 7, 0.28, 32), 'Y3_tras': Cell(118, 0.60, 12, 0.30, 33), 'Y4_tras': Cell(62, 0.60, 12, 0.30, 34)}
PILARES = [258, 352, 18, 65, 118, 165]
MASTILES = [168, 212, 258, 303, 350, 32, 68, 120]

def ang_in(a, rg): return (wrap(a - rg[0]) % 360) <= ((rg[1] - rg[0]) % 360)

def classify(u, v):
    for c in ABIERTAS.values():
        if c.inside(u, v): return None
    zone = 'marfil'
    for c in AMBAR.values():
        if c.inside(u, v): zone = 'ambar'
    for key, (outer, rg) in BANDAS.items():
        if outer.inside(u, v) and not ABIERTAS[key].inside(u, v) and ang_in(outer.angle(u, v), rg): zone = 'rojo'
    for c in ROJAS.values():
        if c.inside(u, v): zone = 'rojo'
    return zone

# =====================================================================
# 4. ESQUELETO DE CURVAS Y HACES DE BAMBÚ (familias A-F)
# =====================================================================
print('Bambu...')
RIB_PTS = []   # puntos 3D de todos los ejes (para distancias de los agujeros a los bordes)
FEET = []      # (punto, tangente ascendente, radio de haz, oculto)

def lift_feet(P, zmin=0.12 * S):
    """Recorta la polilínea para que empiece/termine a zmin: las cañas entran en el casquillo, no en el suelo."""
    P = np.asarray(P, float)
    for end in (0, 1):
        Q = P if end == 0 else P[::-1]
        if Q[0, 2] < zmin:
            k = int(np.argmax(Q[:, 2] >= zmin))
            if k > 0:
                t = (zmin - Q[k - 1, 2]) / (Q[k, 2] - Q[k - 1, 2] + 1e-9); p0 = Q[k - 1] + t * (Q[k] - Q[k - 1])
                Q = np.vstack([p0, Q[k:]])
        P = Q if end == 0 else Q[::-1]
    return P

def culm(P, closed, rc, lay, mat='bambu', hidden=False, name=None, hollow=True):
    """Una caña: muestreo denso con anillos extra en los nudos, engrosamiento de nudo, conicidad y vetas (UV)."""
    P = np.asarray(P, float); Pr = np.vstack([P, P[:1]]) if closed else P; Ltot = arclen(Pr)[-1]
    if Ltot < 0.05: return
    nl = rng.uniform(0.27, 0.36) * S; ph = rng.uniform(0, nl)
    s = list(np.arange(0, Ltot, 0.10 * S))
    for sn in np.arange(ph, Ltot, nl): s += [sn - 0.03 * S, sn, sn + 0.03 * S]
    s = np.array(sorted(set(np.clip(s, 0, Ltot - 1e-6)))); Q, _ = resample(P, s, closed)
    taper = 1 - 0.08 * (s / Ltot) if not closed else np.ones(len(Q))
    nodes = np.zeros(len(Q))
    for sn in np.arange(ph, Ltot, nl): nodes += np.exp(-((s - sn) ** 2) / (2 * (0.018 * S) ** 2))
    radii = rc * taper * (1 + 0.11 * nodes)
    sweep(Q, CIRC(10), lay, mat, closed, radii, uv_scale=(1 / (1.32 * S), 1.0), roll=rng.uniform(0, 6.28), name=name, hidden=hidden,
          preview_step=2, hollow=0.28 if (hollow and not closed) else 0.0)

def bundle(P, closed, name, nculm=4, family='02_Bambu_principal', clamp_every=0.65, twist=0.5, feet=False, rc=None, hidden=None):
    """Haz de cañas individuales alrededor de un eje; abrazaderas (bloques) y apoyos."""
    P = np.asarray(P, float)
    if feet and not closed: P = lift_feet(P)
    if hidden is None:
        c = P.mean(0) - CENTRO; hidden = is_hidden(math.degrees(math.atan2(c[1], c[0])))
    RIB_PTS.append(P)
    add_curve(P[::2] if len(P) > 12 else P, '01_Curvas_maestras', closed, hidden=hidden, name=name)
    rc = rc or R_CANA
    rb = 0.0 if nculm == 1 else rc * (1.0 if nculm <= 3 else 1.5 if nculm <= 5 else 2.0 if nculm <= 7 else 2.3)  # radio del haz
    n_outer = nculm if nculm <= 5 else (5 if nculm <= 7 else 6)   # cañas exteriores; el resto van dentro del haz
    T, N, B = frames(P, closed); s = arclen(np.vstack([P, P[:1]]) if closed else P)[:len(P)]
    for c in range(nculm):
        rci = rc * rng.uniform(0.8, 1.2)           # cañas de distinto diámetro (Ø 64-96 mm)
        inner = c >= n_outer
        ang0 = (2 * math.pi * c / n_outer if not inner else 2 * math.pi * (c - n_outer) / max(nculm - n_outer, 1) + 0.5) + rng.uniform(-0.25, 0.25)
        ang = ang0 + twist * s
        if closed:
            ang = ang0 + 2 * math.pi * np.round(twist * s[-1] / (2 * math.pi)) * s / (s[-1] + s[-1] / len(P))
        rbi = rb * rng.uniform(0.92, 1.08) * (0.42 if inner else 1.0)
        Pc = P + rbi * (np.cos(ang)[:, None] * N + np.sin(ang)[:, None] * B)
        culm(Pc, closed, rci, family, hidden=hidden, name=f'{name} cana {c + 1}')
    if nculm > 1:
        Rb = round(rb + rc, 3); def_blocks(Rb)
        total = s[-1] + (np.linalg.norm(P[0] - P[-1]) if closed else 0)
        for sc in np.arange(0.30, total - 0.15, clamp_every * S):
            i = int(np.searchsorted(s, sc)) % len(P)
            place(f'ABR_{Rb:.3f}', P[i], T[i], '04_Nudos_y_abrazaderas', hidden=hidden, tag=f'abrazadera {name}')
        if feet and not closed:
            for i, sign in ((0, 1), (-1, -1)): FEET.append((P[i], T[i] * sign, Rb, hidden))
    return P

# --- A. Haces superiores de fachada: anillo de cubierta (descendente de izquierda a derecha) y haces que bajan a la derecha
u_ring = np.linspace(0, 360, 320, endpoint=False)
P_RING = bundle(env(u_ring, 1.0), True, 'A_anillo_superior', nculm=8, clamp_every=0.5, twist=0.25)
t = np.linspace(0, 1, 160)
bundle(env(195 + 60 * t, 0.90 - 0.04 * np.sin(np.pi * t)), False, 'A_haz_superior_frontal', nculm=5, twist=0.4)
t = np.linspace(0, 1, 170)
bundle(env(300 + 58 * t, 0.92 * (1 - t ** 3) ** 0.7), False, 'A_haz_descenso_derecho', nculm=6, twist=0.3, feet=True)

# --- B. Arcos del acceso: borde del hueco, banda exterior, arco interior (profundidad) y riostras
def cell_rib(cell, name, nculm, n=180, family='02_Bambu_principal', feet=True, twist=0.5, offset_in=0.0, scale=1.0):
    u, v, closed = cell.boundary(n); P = env(u, v)
    if offset_in or scale != 1.0:
        c3 = env(cell.uc, max(cell.vc, 0.25)); nrm = env_normal(u, v)
        P = c3 + (P - c3) * scale - nrm * offset_in
    return bundle(P, closed, name, nculm, family, twist=twist, feet=feet and not closed), (u, v)

P_O2, (u_o2, v_o2) = cell_rib(ABIERTAS['O2_acceso'], 'B_arco_acceso', 7)
cell_rib(BANDAS['O2_acceso'][0], 'B_arco_acceso_banda_exterior', 5)
P_O2i, _ = cell_rib(ABIERTAS['O2_acceso'], 'B_arco_acceso_interior', 4, offset_in=0.55 * S, scale=0.93)
for k in np.linspace(0.12, 0.88, 5):
    i = int(k * (len(P_O2) - 1)); j = int(k * (len(P_O2i) - 1))
    culm(np.array([P_O2[i], P_O2i[j]]), False, R_CANA * 0.7, '03_Bambu_secundario', name='B_riostra_acceso')
    RIB_PTS.append(np.array([P_O2[i], P_O2i[j]]))

# --- C. Costillas laterales: bordes del resto de celdas y pilares con giro
for key, c in ABIERTAS.items():
    if key != 'O2_acceso': cell_rib(c, 'C_' + key, 6 if 'anillo_izq' in key else 4)
for key, (outer, _) in BANDAS.items():
    if key != 'O2_acceso': cell_rib(outer, 'C_' + key + '_banda_exterior', 4)
for key, c in list(ROJAS.items()) + list(AMBAR.items()):
    cell_rib(c, 'C_' + key, 3, n=130, twist=0.8)
for u0 in PILARES:
    v = np.linspace(0, 1, 60); bundle(env(u0 + 12 * v, v), False, f'C_pilar_{u0}', 4, twist=0.3, feet=True)

# --- D. Bordes inferiores: carriles de base entre apoyos (sin los tramos de los arcos pasantes)
ug = np.linspace(0, 360, 720, endpoint=False)
openbottom = [c for c in ABIERTAS.values() if -c.vc / c.dv > -1]
keep = np.array([not any(c.inside(u, 0.0) for c in openbottom) for u in ug])
start = int(np.argmin(keep)); segs = []; cur = []
for k in range(720):
    i = (start + k) % 720
    if keep[i]: cur.append(ug[i])
    elif cur: segs.append(cur); cur = []
if cur: segs.append(cur)
for n_, seg in enumerate(segs):
    seg = np.array(seg); tt = (seg - seg[0]) / max(seg[-1] - seg[0], 1e-6)
    P = bundle(env(seg, 0.035 + 0.04 * np.sin(np.pi * tt)), False, f'D_borde_inferior_{n_}', 3, twist=0.0, feet=True)
    s = arclen(P)
    for sc in np.arange(1.6 * S, s[-1] - 0.8, 1.7 * S):
        i = min(int(np.searchsorted(s, sc)), len(P) - 1)
        FEET.append((P[i], np.array([0, 0, 1.0]), round(R_CANA * 2, 3), is_hidden(seg[min(i, len(seg) - 1)])))

# --- Mástiles (continuación de costillas sobre el anillo) con remate y orejeta para cables
mast_tops = {}
RB_MAST = round(R_CANA * 2, 3); def_blocks(RB_MAST)
for u0 in MASTILES:
    prim = env(u0, 1.0); out = env_normal(u0, 1.0); out[2] = 0; out /= np.linalg.norm(out)
    top = prim + np.array([0, 0, MAST_H[u0] * S]) + out * 0.18 * S
    tt = np.linspace(0, 1, 16)[:, None]; ctrl = prim + np.array([0, 0, 0.35 * S]) - out * 0.05
    P = (1 - tt) ** 2 * prim + 2 * (1 - tt) * tt * ctrl + tt ** 2 * top
    bundle(P, False, f'A_mastil_{u0}', 3, clamp_every=0.3, twist=0.0)
    place(f'REMATE_{RB_MAST:.3f}', top, [0, 0, 1], '04_Nudos_y_abrazaderas', hidden=is_hidden(u0), tag=f'remate mastil {u0}')
    mast_tops[u0] = top + np.array([0, 0, 0.1])

# --- E. Montantes agrupados junto a los apoyos (cañas cortas inclinadas atadas al haz)
for (p, t_up, Rb, hidden) in FEET:
    if abs(t_up[2]) > 0.95: continue                      # solo en pies de arcos y pilares
    side = np.cross(t_up, [0, 0, 1]); side[2] = 0; side /= (np.linalg.norm(side) + 1e-9)
    for sgn in (1, -1):
        base = np.array([p[0], p[1], 0.12 * S]) + side * sgn * (Rb + R_CANA * 0.8 + 0.01)
        top = base + np.array([0, 0, rng.uniform(0.5, 0.8) * S]) + t_up * np.array([1, 1, 0]) * 0.08
        culm(np.array([base, top]), False, R_CANA * 0.8, '03_Bambu_secundario', hidden=hidden, name='E_montante_apoyo')
        def_blocks(round(R_CANA * 0.8, 3)); place(f'ABR_{round(R_CANA * 0.8, 3):.3f}', base + [0, 0, 0.35 * S], [0, 0, 1], '04_Nudos_y_abrazaderas', hidden=hidden, tag='atadura montante')

# --- F. Elementos secundarios que subdividen paneles (cañas sueltas entre bordes)
SECUNDARIAS = [((200, 0.95), (236, 0.98)), ((196, 0.55), (186, 0.92)), ((300, 0.95), (318, 0.86)), ((345, 0.9), (356, 0.6)),
               ((5, 0.9), (16, 0.55)), ((252, 0.9), (262, 0.55)), ((300, 0.2), (312, 0.05)), ((160, 0.9), (172, 0.3))]
for (ua, va), (ub, vb) in SECUNDARIAS:
    tt = np.linspace(0, 1, 30); P = env(ua + (ub - ua) * tt, va + (vb - va) * tt + 0.03 * np.sin(np.pi * tt))
    culm(P, False, R_CANA * 0.75, '03_Bambu_secundario', hidden=is_hidden((ua + ub) / 2), name='F_secundaria'); RIB_PTS.append(P)

# --- Apoyos (bloques) y cimentación propuesta
for (p, t_up, Rb, hidden) in FEET:
    g = np.array([p[0], p[1], 0.0]); def_blocks(Rb)
    place(f'APOYO_{Rb:.3f}', g, [0, 0, 1], '05_Apoyos', xdir=[t_up[0], t_up[1], 0] if abs(t_up[2]) < 0.99 else None, hidden=hidden, tag='apoyo')
    a = attrs('05_Apoyos', 'acero', 'cimentacion propuesta'); a.LayerIndex = L['16_Elementos_ocultos_propuestos/Cimentacion_propuesta']
    f.Objects.AddInstanceObject(r.InstanceReference(BLOCKS['CIMENTACION'][0], r.Transform.Translation(float(g[0]), float(g[1]), 0.0)), a)

# =====================================================================
# 5. PANELES: piezas perforadas (agujeros reales, espesor) y paneles rojo/ámbar
# =====================================================================
print('Paneles perforados...')
RIB_TREE = cKDTree(np.vstack(RIB_PTS))
PER = 2 * math.pi * math.sqrt((A * A + B_ * B_) / 2); KU = PER / 360.0   # metros por grado (medio)

def boundary_points():
    pts = []
    for c in list(ABIERTAS.values()) + [b[0] for b in BANDAS.values()] + list(ROJAS.values()) + list(AMBAR.values()):
        u, v, _ = c.boundary(240); pts.append(np.stack([u % 360, np.clip(v, 0.004, 0.996)], 1))
    return np.vstack(pts)

def panel_points(step=0.13 * S):
    us = np.arange(0, 360, step / KU); vs = np.arange(0.01, 0.995, step / H)
    U, Vv = np.meshgrid(us, vs); U = U + rng.uniform(-0.3, 0.3, U.shape) * step / KU; Vv = Vv + rng.uniform(-0.3, 0.3, Vv.shape) * step / H
    return np.stack([U.ravel() % 360, np.clip(Vv.ravel(), 0.005, 0.995)], 1)

# agujeros: lanzamiento de dardos en 3D, radio según distancia al borde más cercano y campo de densidad
HOLES = []  # (u, v, radio, centro3d)
cand = panel_points(0.05 * S); rng.shuffle(cand)
dens = lambda u, v: 0.55 + 0.45 * math.sin(math.radians(u) * 2.3 + v * 7.1) * math.cos(v * 4.0 + math.radians(u) * 0.8)
acc_c = []; acc_r = []; acc_tree = None
for (u, v) in cand:
    if classify(u, v) != 'marfil': continue
    p = env(u, v); d_edge = RIB_TREE.query(p)[0]
    if d_edge < 0.075 * S: continue
    if rng.random() > dens(u, v) + 0.15: continue
    rad = np.clip(0.02 * S + 0.12 * S * (d_edge - 0.08 * S) / 0.5, 0.02 * S, 0.095 * S) * rng.uniform(0.55, 1.0)
    if rng.random() < 0.18: rad *= 0.6              # agrupaciones de huecos pequeños
    if d_edge < rad + 0.05 * S: continue
    if acc_tree is not None:
        near = acc_tree.query_ball_point(p, rad + 0.095 * S + 0.025 * S)
        if any(np.linalg.norm(p - acc_c[j]) < rad + acc_r[j] + 0.022 * S for j in near): continue
    if any(np.linalg.norm(p - acc_c[j]) < rad + acc_r[j] + 0.022 * S for j in range(len(acc_c) - (len(acc_c) % 25), len(acc_c))): continue
    acc_c.append(p); acc_r.append(rad); HOLES.append((u, v, rad, p))
    if len(acc_c) % 25 == 0: acc_tree = cKDTree(np.array(acc_c))
    if len(HOLES) >= 3200: break
HOLE_TREE = cKDTree(np.array([h[3] for h in HOLES])); HOLE_R = np.array([h[2] for h in HOLES])
print('  agujeros:', len(HOLES))

def triangulate(points_uv, extra_rings=None):
    """Delaunay en coordenadas ~métricas (u*KU, v*H) con duplicado de la costura u=0/360."""
    P = points_uv.copy()
    if extra_rings is not None: P = np.vstack([P, extra_rings])
    nP = len(P)
    lo = np.where(P[:, 0] < 12)[0]; hi = np.where(P[:, 0] > 348)[0]
    Pd = np.vstack([P, P[lo] + [360, 0], P[hi] - [360, 0]]); src = np.concatenate([np.arange(nP), lo, hi])
    tri = Delaunay(np.stack([Pd[:, 0] * KU, Pd[:, 1] * H], 1))
    T = tri.simplices; cen = Pd[T].mean(1)
    keep = (cen[:, 0] >= 0) & (cen[:, 0] < 360)
    return P, src[T[keep]], cen[keep]

RING_N = 14; EDGE_C = 0.006 * S
base_pts = np.vstack([panel_points(), boundary_points()])
P3 = env(base_pts[:, 0], base_pts[:, 1]); d, j = HOLE_TREE.query(P3)
base_pts = base_pts[d > HOLE_R[j] + EDGE_C + 0.03 * S]          # quitar puntos de malla dentro de los agujeros
ring_uv = []
for hi, (u, v, rad, p) in enumerate(HOLES):
    ku, kv = metric(u, v)
    for a in np.linspace(0, 2 * math.pi, RING_N, endpoint=False):
        ring_uv.append(((u + (rad + EDGE_C) * math.cos(a) / ku) % 360, v + (rad + EDGE_C) * math.sin(a) / kv))
ring_uv = np.array(ring_uv); nbase = len(base_pts)
Puv, TRI, CEN = triangulate(base_pts, ring_uv)
zones = np.array([classify(c[0], c[1]) or 'none' for c in CEN])
cen3 = env(CEN[:, 0], CEN[:, 1]); d, j = HOLE_TREE.query(cen3); in_hole = d < HOLE_R[j] + EDGE_C * 0.5
hidden_cen = np.array([is_hidden(c[0]) for c in CEN])

def build_panel(zone, thick, tile, lay, mat, name, with_holes):
    sel = (zones == zone) & (~in_hole if with_holes else np.ones(len(zones), bool))
    for hidden in (False, True):
        T = TRI[sel & (hidden_cen == hidden)]
        if len(T) == 0: continue
        used = np.unique(T); remap = {int(k): i for i, k in enumerate(used)}
        Pu = Puv[used]; P3 = env(Pu[:, 0], Pu[:, 1]); N3 = env_normal(Pu[:, 0], Pu[:, 1])
        UV = [(p[0] * KU / tile, p[1] * H / tile) for p in Pu]
        if thick <= 0:
            add_mesh(list(P3), [tuple(remap[int(k)] for k in t) for t in T], UV, lay, mat, name, hidden); continue
        n = len(used); V = list(P3 + N3 * thick / 2) + list(P3 - N3 * thick / 2); UV = UV + UV
        F = [tuple(remap[int(k)] for k in t) for t in T] + [tuple(n + remap[int(k)] for k in t[::-1]) for t in T]
        if with_holes:  # paredes achaflanadas de cada agujero cuyo anillo esté completo en esta malla
            for hi, (u, v, rad, c3) in enumerate(HOLES):
                if is_hidden(u) != hidden: continue
                ids = [nbase + hi * RING_N + k for k in range(RING_N)]
                if not all(i in remap for i in ids): continue
                nrm = env_normal(u, v); base = len(V)
                top = [remap[i] for i in ids]; bot = [n + remap[i] for i in ids]
                dirs = [P3[remap[i]] - c3 for i in ids]; dirs = [d_ - (d_ @ nrm) * nrm for d_ in dirs]; dirs = [d_ / np.linalg.norm(d_) for d_ in dirs]
                V += [c3 + rad * d_ + nrm * (thick / 2 - EDGE_C) for d_ in dirs] + [c3 + rad * d_ - nrm * (thick / 2 - EDGE_C) for d_ in dirs]
                UV += [UV[remap[i]] for i in ids] * 2
                mt = [base + k for k in range(RING_N)]; mb = [base + RING_N + k for k in range(RING_N)]
                for k in range(RING_N):
                    k2 = (k + 1) % RING_N
                    F += [(top[k], top[k2], mt[k2], mt[k]), (mt[k], mt[k2], mb[k2], mb[k]), (mb[k], mb[k2], bot[k2], bot[k])]
        add_mesh(V, F, UV, lay, mat, name, hidden)

build_panel('marfil', E_PERF, 2.0 * S, '08_Piezas_perforadas', 'marfil', 'Pieza perforada marfil', True)
build_panel('rojo', 0.0, 1.3 * S, '09_Paneles_rojos', 'rojo', 'Panel translucido rojo', False)
build_panel('ambar', 0.0, 1.3 * S, '10_Paneles_ambar', 'ambar', 'Panel translucido ambar', False)
# sujeciones perimetrales de los paneles de color: grapas (bloque) a lo largo de sus bordes
for c in [BANDAS[k][0] for k in BANDAS] + list(ROJAS.values()) + list(AMBAR.values()):
    u, v, _ = c.boundary(40)
    for k in range(0, len(u), 3):
        if classify(u[k] + 0.6, v[k]) in ('rojo', 'ambar') or classify(u[k] - 0.6, v[k]) in ('rojo', 'ambar'):
            nrm = env_normal(u[k], v[k]); place('GRAPA', env(u[k], v[k]) + nrm * (R_CANA * 2 + 0.04), nrm, '04_Nudos_y_abrazaderas', hidden=is_hidden(u[k]), tag='grapa panel')

# =====================================================================
# 6. CUBIERTA: membrana relajada entre picos y valles, cordón de borde, cables y tensores
# =====================================================================
print('Cubierta...')
NR, NT = 20, 160
keys = sorted(mast_tops.keys()); tops = np.array([mast_tops[k] for k in keys])
c_roof = CENTRO.copy(); c_roof[2] = H
def edge_profile(th):
    """Altura del borde y radio normalizado entre mástiles vecinos (festoneado con flecha)."""
    ang = np.array([(th - k) % 360 for k in keys]); i0 = int(np.argmin(ang)); i1 = (i0 + 1) % len(keys) if keys[(i0 + 1) % len(keys)] != keys[i0] else i0
    i1 = int(np.argmin(np.array([(k - th) % 360 for k in keys])))
    span = (keys[i1] - keys[i0]) % 360 or 360; t_ = ang[i0] / span
    z = (1 - t_) * tops[i0][2] + t_ * tops[i1][2] - 0.38 * S * math.sin(math.pi * t_) ** 1.2
    return z, 1.10 - 0.07 * math.sin(math.pi * t_)
V = [c_roof.copy()]; fixed = [False]; zfix = [0.0]
for j in range(1, NR + 1):
    for i in range(NT):
        th = 360 * i / NT; ze, rho_e = edge_profile(th); rho = rho_e * j / NR
        p = env(th, 1.0); xy = c_roof[:2] + rho * (p[:2] - c_roof[:2])
        V.append(np.array([xy[0], xy[1], H])); fixed.append(j == NR); zfix.append(ze)
V = np.array(V); fixed = np.array(fixed); zfix = np.array(zfix)
for top in tops:  # picos: vértices cercanos a cada mástil quedan fijados
    d = np.linalg.norm(V[:, :2] - top[:2], axis=1); near = d < 0.3 * S
    fixed[near] = True; zfix[near] = top[2] - 0.06 * S
idx = lambda j, i: 1 + (j - 1) * NT + (i % NT)
nb = [[] for _ in range(len(V))]
for i in range(NT): nb[0].append(idx(1, i)); nb[idx(1, i)].append(0)
for j in range(1, NR + 1):
    for i in range(NT):
        a = idx(j, i); nb[a] += [idx(j, i + 1), idx(j, i - 1)]
        if j < NR: nb[a].append(idx(j + 1, i)); nb[idx(j + 1, i)].append(a)
nbi = [np.array(x) for x in nb]; free = np.where(~fixed)[0]
z = np.where(fixed, zfix, H + 0.2 * S)
for it in range(500):  # relajación tipo membrana (laplaciana sobre z)
    znew = z.copy()
    for a in free: znew[a] = z[nbi[a]].mean()
    z = znew
V[:, 2] = z
F = [(0, idx(1, i), idx(1, i + 1)) for i in range(NT)]
F += [(idx(j, i), idx(j + 1, i), idx(j + 1, i + 1), idx(j, i + 1)) for j in range(1, NR) for i in range(NT)]
add_mesh(list(V), F, [(p[0] / (1.5 * S), p[1] / (1.5 * S)) for p in V], '07_Membranas', 'membrana', 'Membrana de cubierta', preview_step=1)
edge = np.array([V[idx(NR, i)] for i in range(NT)])
sweep(edge, [(a * 0.012, b * 0.012) for a, b in CIRC(6)], '06_Cables_y_tensores', 'cable', closed=True, uv_scale=(1, 1), name='Cordon de borde membrana')
for u0, top in mast_tops.items():   # vientos a anclajes exteriores con tensor y anclaje
    anc = env(u0, 0.0) * np.array([1, 1, 0]); out = anc - c_roof * np.array([1, 1, 0]); out /= np.linalg.norm(out)
    anc = anc + out * 2.2 * S; d = anc - top; dn = d / np.linalg.norm(d)
    sweep(np.array([top, anc + [0, 0, 0.28]]), [(a * 0.008, b * 0.008) for a, b in CIRC(6)], '06_Cables_y_tensores', 'cable', uv_scale=(1, 1), name=f'viento mastil {u0}', hidden=is_hidden(u0))
    place('TENSOR', anc + [0, 0, 0.28] - dn * 0.35, dn, '06_Cables_y_tensores', hidden=is_hidden(u0), tag='tensor')
    place('ANCLAJE', anc, [0, 0, 1], '05_Apoyos', hidden=is_hidden(u0), tag='anclaje viento')
for a_, b_ in zip(keys, keys[1:] + keys[:1]):   # cables superiores entre picos (con flecha)
    pa, pb = mast_tops[a_], mast_tops[b_]; tt = np.linspace(0, 1, 12)[:, None]
    P = (1 - tt) * pa + tt * pb - np.array([0, 0, 0.18 * S]) * np.sin(np.pi * tt)
    sweep(P, [(a * 0.006, b * 0.006) for a, b in CIRC(6)], '06_Cables_y_tensores', 'cable', uv_scale=(1, 1), name='cable entre picos', hidden=is_hidden(a_) and is_hidden(b_))

# =====================================================================
# 7. INTERIOR: pavimento con despiece, bancos, elemento de agua, recipiente suspendido
# =====================================================================
print('Interior...')
def smooth_closed(pts, n=160):
    pts = np.asarray(pts, float); tck, _ = splprep([pts[:, 0], pts[:, 1]], s=0, per=True)
    x, y = splev(np.linspace(0, 1, n, endpoint=False), tck); return np.stack([x, y], 1)

C0 = CENTRO[:2]
deck = smooth_closed(C0 + np.array([(-2.9, -1.3), (-1.0, -2.75), (1.6, -3.05), (3.3, -1.9), (3.7, 0.5), (2.5, 2.3), (0.0, 2.6), (-2.3, 1.9), (-3.3, 0.3)]) * S)
def x_range(y):
    xs = []
    for i in range(len(deck)):
        a, b = deck[i], deck[(i + 1) % len(deck)]
        if (a[1] - y) * (b[1] - y) <= 0 and a[1] != b[1]:
            xs.append(a[0] + (y - a[1]) / (b[1] - a[1]) * (b[0] - a[0]))
    return (min(xs), max(xs)) if len(xs) >= 2 else None
V = []; F = []; UV = []
y0 = deck[:, 1].min() + 0.01; W_T, GAP, Z0, Z1 = 0.14 * S, 0.012 * S, 0.08 * S, 0.12 * S
while y0 + W_T < deck[:, 1].max():
    r0, r1 = x_range(y0), x_range(y0 + W_T)
    if r0 and r1:
        xl, xr = max(r0[0], r1[0]), min(r0[1], r1[1]); x = xl
        while x < xr - 0.2:
            xe = min(x + rng.uniform(1.6, 3.0) * S, xr)
            c = [(x, y0), (xe, y0), (xe, y0 + W_T), (x, y0 + W_T)]; b = len(V)
            V += [(px, py, Z1) for px, py in c] + [(px, py, Z0) for px, py in c]
            UV += [(px / S, py / S) for px, py in c] * 2
            F += [(b, b + 1, b + 2, b + 3), (b + 4, b + 7, b + 6, b + 5)] + [(b + i, b + 4 + i, b + 4 + (i + 1) % 4, b + (i + 1) % 4) for i in range(4)]
            x = xe + GAP
    y0 += W_T + GAP
add_mesh(V, F, UV, '11_Pavimento', 'tarima', 'Tarima: tablas')

def bench(path_xy, name, hidden=False):
    tck, _ = splprep([path_xy[:, 0], path_xy[:, 1]], s=0, k=min(3, len(path_xy) - 1)); n = 44
    bx, by = splev(np.linspace(0, 1, n), tck); Pb = np.stack([bx, by, np.full(n, 0.12 * S + 0.45 * S - 0.03 * S)], 1)
    T, N, B = frames(Pb, False); side = np.cross(T, [0, 0, 1]); side /= np.linalg.norm(side, axis=1)[:, None]
    for off in (-0.17, 0.0, 0.17):   # tres tablas de asiento (despiece según curvatura)
        P = Pb + side * off * S
        sweep(P, [(-0.075 * S, -0.03 * S), (0.075 * S, -0.03 * S), (0.075 * S, 0.03 * S), (-0.075 * S, 0.03 * S), (-0.075 * S, -0.03 * S)], '12_Bancos', 'banco', uv_scale=(1, 0.3), name=name + ' tabla', hidden=hidden)
    for p in Pb[3::9]: place('PIE_BANCO', [p[0], p[1], 0.12 * S], [0, 0, 1], '12_Bancos', hidden=hidden, tag='pie banco')
bench(C0 + np.array([(1.6, 2.6), (2.7, 1.9), (3.3, 0.8), (3.3, -0.4)]) * S, 'Banco derecho sinuoso')
bench(C0 + np.array([(-1.6, 2.7), (0.0, 2.95), (1.2, 2.7)]) * S, 'Banco fondo [hipotesis]', hidden=True)
bench(C0 + np.array([(-3.4, 1.2), (-3.1, 2.1), (-2.4, 2.6)]) * S, 'Banco izquierdo [parcial]')

# elemento circular con agua (borde de madera, recipiente, lámina de agua) y recipiente suspendido
PC = np.array([*(C0 + np.array([-1.85, -1.9]) * S), 0.0]); RW = 0.62 * S
circ = np.array([[PC[0] + RW * math.cos(a), PC[1] + RW * math.sin(a), 0.55 * S] for a in np.linspace(0, 2 * math.pi, 48, endpoint=False)])
sweep(circ, [(a * 0.055 * S, b * 0.055 * S) for a, b in CIRC(10)], '13_Elemento_de_agua', 'madera_osc', closed=True, uv_scale=(1, 1), name='Borde de madera')
Vc, Fc, UVc, _, _ = cyl_mesh(RW - 0.01 * S, 0.03 * S, 0.52 * S, 48, 'madera_osc', '13_Elemento_de_agua', PC[0], PC[1])
add_mesh(Vc, Fc, UVc, '13_Elemento_de_agua', 'madera_osc', 'Recipiente')
Vw = [(PC[0] + (RW - 0.03 * S) * math.cos(a), PC[1] + (RW - 0.03 * S) * math.sin(a), 0.50 * S) for a in np.linspace(0, 2 * math.pi, 48, endpoint=False)] + [(PC[0], PC[1], 0.50 * S)]
add_mesh(Vw, [(i, (i + 1) % 48, 48) for i in range(48)], [((x - PC[0]) / (1.3 * S) + 0.5, (y - PC[1]) / (1.3 * S) + 0.5) for x, y, _ in Vw], '13_Elemento_de_agua', 'agua', 'Lamina de agua')
z_l = 2.3 * S; Pf = np.array([[PC[0], PC[1], z_l], [PC[0], PC[1], z_l + 0.62 * S]])
sweep(Pf, CIRC(18), '13_Elemento_de_agua', 'vidrio', radii=[0.025 * S, 0.22 * S], uv_scale=(1, 1), name='Recipiente suspendido (embudo) [interpretacion]')
Vr, Fr, UVr, _, _ = ring_mesh(0.235 * S, 0.215 * S, z_l + 0.60 * S, z_l + 0.65 * S, 24, 'acero', '13_Elemento_de_agua')
add_mesh([(x + PC[0], y + PC[1], zz) for x, y, zz in Vr], Fr, UVr, '13_Elemento_de_agua', 'acero', 'Aro del recipiente')
z_roof_here = H + 0.25 * S
for a in (90, 210, 330):
    q = np.array([PC[0] + 0.22 * S * math.cos(math.radians(a)), PC[1] + 0.22 * S * math.sin(math.radians(a)), z_l + 0.64 * S])
    sweep(np.array([q, [PC[0] + 0.05 * math.cos(math.radians(a)), PC[1] + 0.05 * math.sin(math.radians(a)), z_roof_here]]), [(x * 0.004, y * 0.004) for x, y in CIRC(5)], '06_Cables_y_tensores', 'cable', uv_scale=(1, 1), name='suspension recipiente')
sweep(np.array([[PC[0], PC[1], 0.75 * S], [PC[0], PC[1], z_l]]), [(x * 0.012 * S, y * 0.012 * S) for x, y in CIRC(8)], '13_Elemento_de_agua', 'vidrio', uv_scale=(1, 1), name='Prolongacion estrecha inferior')

# =====================================================================
# 8. DISPOSITIVOS VISIBLES (lateral derecho): dos piezas circulares metálicas y caja gris con soportes
# =====================================================================
LD = '14_Dispositivos_visibles'
for (u0, v0, rad) in ((356, 0.56, 0.24), (9, 0.24, 0.22)):
    p = env(u0, v0); nrm = env_normal(u0, v0); xf, (xd, yd, nd) = xform_at(p, nrm); Mx = np.stack([xd, yd, nd], 1)
    Vs, Fs, UVs, _, _ = sphere_mesh(rad * S, 'acero', LD)
    add_mesh([np.asarray(v) @ Mx.T + p + nrm * 0.05 * S for v in Vs], Fs, UVs, LD, 'acero', 'Pieza circular metalica')
    Vb, Fb, UVb, _, _ = ring_mesh(rad * S * 0.5, rad * S * 0.4, -0.02, 0.06, 16, 'acero', LD)
    add_mesh([np.asarray(v) @ Mx.T + p for v in Vb], Fb, UVb, LD, 'acero', 'Soporte pieza circular')
p0 = env(347, 0.26); nrm = env_normal(347, 0.26); pb = p0 + nrm * (0.07 * S + 0.05); xf, (xd, yd, nd) = xform_at(pb, nrm, [0, 0, 1]); Mx = np.stack([xd, yd, nd], 1)
for part in [box_mesh(0, 0, 0, 0.26 * S, 0.40 * S, 0.14 * S, 'acero', LD), box_mesh(0, 0, -0.085 * S, 0.14 * S, 0.5 * S, 0.03 * S, 'acero', LD), box_mesh(0, 0, 0.075 * S, 0.22 * S, 0.3 * S, 0.01 * S, 'acero', LD)]:
    Vb, Fb, UVb, _, _ = part; add_mesh([np.asarray(v) @ Mx.T + pb for v in Vb], Fb, UVb, LD, 'acero', 'Caja gris / soporte')
for key in ('O2_acceso', 'R1_lente_der'):   # tiras LED magenta observadas junto a dos haces
    c = BANDAS[key][0] if key in BANDAS else ROJAS[key]; u, v, closed = c.boundary(150)
    P = env(u, v) + env_normal(u, v) * (R_CANA * 2.5 + 0.02)
    sweep(P, [(a * 0.01, b * 0.01) for a, b in CIRC(8)], LD, 'led', closed, uv_scale=(1, 1), name='Tira LED ' + key)

# =====================================================================
# 9. ENTORNO, REFERENCIA Y CÁMARAS
# =====================================================================
print('Entorno...')
V = [(0, 0, -0.01)]; F = []
for j in range(1, 13):
    rad = 20 * j / 12; V += [(rad * math.cos(a), rad * math.sin(a), -0.01) for a in np.linspace(0, 2 * math.pi, 72, endpoint=False)]
F = [(0, 1 + i, 1 + (i + 1) % 72) for i in range(72)]
for j in range(11):
    b0, b1 = 1 + j * 72, 1 + (j + 1) * 72; F += [(b0 + i, b1 + i, b1 + (i + 1) % 72, b0 + (i + 1) % 72) for i in range(72)]
add_mesh(V, F, [(x / 4, y / 4) for x, y, _ in V], '15_Entorno', 'suelo', 'Terreno')
g = np.random.default_rng(5)
for k in range(18):
    for _ in range(80):
        x, y = g.uniform(-17, 17), g.uniform(-4, 19)
        if (y > 8.5) or (abs(x) > 8.5 and y > -2): break
    h = g.uniform(11, 16); lean = g.normal(0, 0.35, 2)
    P = np.array([[x, y, -0.2], [x + lean[0] * 0.5, y + lean[1] * 0.5, h * 0.5], [x + lean[0], y + lean[1], h]])
    sweep(P, CIRC(10), '15_Entorno', 'corteza', radii=[0.26, 0.17, 0.09], uv_scale=(0.25, 1), name=f'Tronco {k + 1}')

def camera_basis(pos, tgt):
    pos, tgt = np.array(pos, float), np.array(tgt, float); fw = tgt - pos; fw /= np.linalg.norm(fw)
    rt = np.cross(fw, [0, 0, 1]); rt /= np.linalg.norm(rt); return pos, fw, rt, np.cross(rt, fw)

def named_view(name, pos, tgt, lens):
    vi = r.ViewInfo(); vi.Name = name; vp = vi.Viewport
    pos, fw, rt, up = camera_basis(pos, tgt)
    vp.ChangeToPerspectiveProjection(float(np.linalg.norm(np.array(tgt) - pos)), True, lens)
    vp.SetCameraLocation(r.Point3d(*pos)); vp.SetCameraDirection(r.Vector3d(*fw)); vp.SetCameraUp(r.Vector3d(*up))
    hw = 0.05 * math.tan(math.atan(18.0 / lens)); vp.SetFrustum(-hw, hw, -hw / (IMG_W / IMG_H), hw / (IMG_W / IMG_H), 0.05, 500.0)
    f.NamedViews.Add(vi); f.Views.Add(vi)
VISTAS = {'01_Referencia': (CAM_POS, CAM_TGT, LENTE_MM), '02_Interior': ((1.2 * S, 1.2 * S, 1.55), (-2.0 * S, 4.2 * S, 1.6), 24.0),
          '03_Estructura': ((9.0 * S, -11.0 * S, 7.5 * S), (0.0, 2.2 * S, 1.6), 35.0)}
for name, (pos, tgt, lens) in VISTAS.items(): named_view(name, pos, tgt, lens)
pos, fw, rt, up = camera_basis(CAM_POS, CAM_TGT); D = 45.0; hw = D * math.tan(math.atan(18.0 / LENTE_MM)); hh = hw / (IMG_W / IMG_H)
c = pos + fw * D; Vq = [c - rt * hw - up * hh, c + rt * hw - up * hh, c + rt * hw + up * hh, c - rt * hw + up * hh]
f.Objects.AddMesh(make_mesh(Vq, [(0, 1, 2, 3)], [(0, 1), (1, 1), (1, 0), (0, 0)]), attrs('00_Referencia_y_camaras', 'referencia', 'Imagen de referencia (plano frente a la camara 01_Referencia)'))
add_curve(np.array([pos, np.array(CAM_TGT)]), '00_Referencia_y_camaras', degree=1, name='Eje camara 01_Referencia')

# =====================================================================
# 10. GUARDAR, VISTAS DE COMPROBACIÓN Y SUPERPOSICIÓN
# =====================================================================
ok = f.Write(OUT3DM, 8)
print('3dm escrito:', ok, f'{os.path.getsize(OUT3DM) / 1e6:.1f} MB', 'objetos:', len(f.Objects), 'bloques:', len(f.InstanceDefinitions))
print('caras por capa:', json.dumps({k: int(v) for k, v in STATS.items()}, ensure_ascii=False))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
light = np.array([-0.4, -0.5, 0.75]); light /= np.linalg.norm(light)

def render(path, pos, tgt, lens, hide=(), bg=None, alpha_mult=1.0, size=(IMG_W, IMG_H)):
    pos, fw, rt, up = camera_basis(pos, tgt); fl = 1.0 / math.tan(math.atan(18.0 / lens)); asp = size[0] / size[1]
    polys = []; cols = []; depth = []
    for P, col, al, lay in PREVIEW:
        if any(lay.startswith(h) for h in hide): continue
        d = P - pos; z = d @ fw
        if np.any(z < 0.2): continue
        xs = (d @ rt) / z * fl; ys = (d @ up) / z * fl * asp
        if xs.max() < -1.1 or xs.min() > 1.1 or ys.max() < -1.1 or ys.min() > 1.1: continue
        nrm = np.cross(P[1] - P[0], P[2] - P[0]); nn = np.linalg.norm(nrm)
        sh = 0.45 + 0.55 * abs(nrm @ light) / nn if nn > 1e-12 else 0.7
        polys.append(np.stack([xs, ys], 1)); cols.append((*(np.array(col) / 255 * sh), al * alpha_mult)); depth.append(z.mean())
    order = np.argsort(depth)[::-1]
    fig = plt.figure(figsize=(size[0] / 100, size[1] / 100), dpi=100); ax = fig.add_axes([0, 0, 1, 1]); ax.set_facecolor((0.84, 0.87, 0.84))
    if bg is not None: ax.imshow(bg, extent=[-1, 1, -1, 1], aspect='auto', zorder=0)
    ax.add_collection(PolyCollection([polys[i] for i in order], facecolors=[cols[i] for i in order], edgecolors='none', antialiased=True, zorder=1))
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.axis('off'); fig.savefig(path); plt.close(fig)
    return len(polys)

import pickle; pickle.dump(PREVIEW, open(os.environ.get('PREVIEW_PKL', '/tmp/preview_pabellon.pkl'), 'wb'))
ref = np.asarray(Image.open(REF_IMG).convert('RGB'))
n1 = render(os.path.join(HERE, 'vista_01_general.png'), CAM_POS, CAM_TGT, LENTE_MM, hide=('00_',))
render(os.path.join(HERE, 'superposicion_referencia.png'), CAM_POS, CAM_TGT, LENTE_MM, hide=('00_', '15_'), bg=ref, alpha_mult=0.55)
render(os.path.join(HERE, 'vista_02_interior.png'), *VISTAS['02_Interior'], hide=('00_',))
render(os.path.join(HERE, 'vista_03_estructura.png'), *VISTAS['03_Estructura'], hide=('00_', '07_', '15_'))
print('vistas OK, poligonos vista general:', n1)

bb = np.vstack([P for P, _, _, lay in PREVIEW if not lay.startswith(('15_', '00_'))])
dims = {'ancho_total_X_m': round(float(bb[:, 0].max() - bb[:, 0].min()), 2), 'profundidad_Y_m': round(float(bb[:, 1].max() - bb[:, 1].min()), 2),
        'altura_max_Z_m': round(float(bb[:, 2].max()), 2), 'altura_anillo_media_m': H, 'anchura_acceso_m': round(float(np.linalg.norm(P_O2[0] - P_O2[-1])), 2),
        'altura_acceso_m': round(float(P_O2[:, 2].max()), 2), 'diametro_cana_mm': [round(R_CANA * 2 * 0.8 * 1000), round(R_CANA * 2 * 1.2 * 1000)],
        'espesor_pieza_perforada_mm': E_PERF * 1000, 'agujeros': len(HOLES), 'altura_asiento_m': 0.45 * S, 'apoyos': len(FEET),
        'camara_referencia': {'posicion': CAM_POS, 'objetivo': CAM_TGT, 'lente_mm': LENTE_MM}}
json.dump(dims, open(os.path.join(HERE, 'dimensiones_estimadas.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps(dims, ensure_ascii=False))
