# -*- coding: utf-8 -*-
"""
E03 — preparado, NO ejecutado. Guardia dura: sin --ejecutar-e03 no genera nada.
Al ejecutar (tras el OK del autor) hara, en este orden (E03_EXECUTION_PLAN.md §0):
  1) texturas de efecto (sprite niebla radial, corona, gota) -> _viewer/tex_data2.js (data-URL)
  2) scene_extra.js: niebla (42 boquillas + 3 columnas), agua viva (chorros/goteo/mangueras/rebosaderos),
     poblacion PERSON2 por programa (posiciones deterministas validadas contra obstaculos)
  3) viewer_e03.html = viewer_e01 + capa extra + presets de luz (atmos_config.json)
  4) render de las 7 camaras hero x2 luces a 2560x1600
Todo parametrizado por atmos_config.json. Los .3dm NO se tocan.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, 'atmos_config.json'), encoding='utf-8'))

if '--ejecutar-e03' not in sys.argv:
    print('E03 PREPARADO pero NO ejecutado (falta OK del autor).')
    print('Plan: E03_EXECUTION_PLAN.md · Config valida: %d camaras hero, %d boquillas de niebla micro (rango sprites %s).' % (
        len(CFG['camaras_hero']),
        42,
        CFG['niebla']['micro']['sprites_por_boquilla']))
    print('Para ejecutar tras el reset: python atmos_prep.py --ejecutar-e03')
    sys.exit(0)

# ==================================================================
# IMPLEMENTACION E03 (arranque oficial 2026-08-11, sobre v003 CONGELADA)
# E03-1: texturas -> tex_data2.js · E03-2: scene_extra.js · E03-3: viewer_e03.html
# ==================================================================
import base64
import io
import math
import random

from PIL import Image, ImageDraw, ImageFilter

V3 = os.path.normpath(os.path.join(HERE, '..', 'FASE_03B6_RESOLUCION'))
VIEW = os.path.join(HERE, '_viewer')
M = json.load(open(os.path.join(V3, 'geometria_maestra_v003.json'), encoding='utf-8'))
A4 = json.load(open(os.path.join(V3, '_reaudit', '_data', 'a4_ribbon.json'), encoding='utf-8'))
PROF = [(r['x'], r['y']) for r in A4['prof']]          # eje CONSTRUIDO de la cinta (1 m)
rng = random.Random(1926)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', 'FASE_03A_MODELO_PROXY')))
import mesh_kit as mk  # noqa: E402

# ---------------- E03-1 · texturas de efecto ----------------
def _uri(im):
    b = io.BytesIO(); im.save(b, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


def gen_tex():
    S = 128
    # sprite de niebla: nucleo radial suave + ruido (legible en contraluz, casi nada sobre cielo)
    im = Image.new('RGBA', (S, S), (255, 255, 255, 0))
    px = im.load()
    for y in range(S):
        for x in range(S):
            d = math.hypot(x - S/2, y - S/2) / (S/2)
            a = max(0.0, 1 - d) ** 2.2
            n = 0.75 + 0.25 * math.sin(x * 0.33 + 2 * math.sin(y * 0.21)) * math.cos(y * 0.27)
            px[x, y] = (234, 246, 242, int(255 * a * n))
    mist = im.filter(ImageFilter.GaussianBlur(3))
    # corona de chapoteo: anillo + radios
    im2 = Image.new('RGBA', (S, S), (255, 255, 255, 0))
    dr = ImageDraw.Draw(im2)
    for k in range(3):
        r0 = 26 + k * 14
        dr.ellipse([S/2 - r0, S/2 - r0*0.45, S/2 + r0, S/2 + r0*0.45],
                   outline=(223, 242, 238, 200 - 55*k), width=4 - k)
    for a in range(0, 360, 24):
        x1 = S/2 + 18*math.cos(math.radians(a)); y1 = S/2 + 8*math.sin(math.radians(a))
        x2 = S/2 + 52*math.cos(math.radians(a)); y2 = S/2 + 23*math.sin(math.radians(a))
        dr.line([x1, y1, x2, y2], fill=(240, 250, 248, 160), width=2)
    corona = im2.filter(ImageFilter.GaussianBlur(1))
    with open(os.path.join(VIEW, 'tex_data2.js'), 'w', encoding='utf-8') as f:
        f.write('const MIST_URI = "%s";\nconst CORONA_URI = "%s";\n' % (_uri(mist), _uri(corona)))
    return True


# ---------------- obstaculos: bbox 2D de la escena v003 en banda de cuerpo ----------------
def load_obstacles():
    txt = open(os.path.join(VIEW, 'scene_v003.js'), encoding='utf-8').read()
    a = txt.index('const SCENE_MESHES = ') + len('const SCENE_MESHES = ')
    b = txt.index(';\nconst SCENE_LINES')
    meshes = json.loads(txt[a:b])
    solid = []
    SKIP = {'12_MIST', '17_METRO_CLEARANCES', '01_GROUND', '16_PEOPLE_PROXY', '05_CABLES'}
    for o in meshes:
        if o['layer'] in SKIP:
            continue
        xs = [v[0] for v in o['V']]; ys = [v[1] for v in o['V']]; zs = [v[2] for v in o['V']]
        if min(zs) < 2.05 and max(zs) > 0.08:
            solid.append((min(xs) - 0.22, min(ys) - 0.22, max(xs) + 0.22, max(ys) + 0.22))
    return meshes, solid


def libre(x, y, OB):
    return not any(x0 <= x <= x1 and y0 <= y <= y1 for (x0, y0, x1, y1) in OB)


# ---------------- E03-2 · capa extra ----------------
SPR, MESHX, LINX = [], [], []


def spr(x, y, z, d, op, tex='mist', tint='#EAF6F2'):
    SPR.append(dict(x=round(x, 2), y=round(y, 2), z=round(z, 2), d=round(d, 2),
                    op=round(op, 3), tex=tex, tint=tint))


def mx(VF, color, op=1.0, em=None, emi=0.0, rough=0.6, layer='EXTRA', shadow=True):
    V, F = VF
    MESHX.append(dict(layer=layer, color=color, op=op, em=em or color, emi=emi, rough=rough,
                      sh=bool(shadow), V=[[round(a, 3) for a in v] for v in V], F=F))


def lnx(p0, p1, color='#DFF2EE', op=0.75):
    LINX.append(dict(a=[round(v, 3) for v in p0], b=[round(v, 3) for v in p1], color=color, op=op))


def build_extra(OB):
    cN = CFG['niebla']['micro']
    # --- niebla micro: 42 boquillas de suelo (v003) + 8 de barandilla de cinta
    NEB = [tuple(p) for p in M['agua_clima']['nebul']]
    n8 = max(len(PROF) // 8, 1)
    RIBNEB = [(PROF[i][0], PROF[i][1], 7.1) for i in range(len(PROF)//16, len(PROF)-1, n8)][:8]
    nspr = 0
    for (bx, by) in NEB:
        for k in range(rng.randint(*cN['sprites_por_boquilla'])):
            capa = cN['capas']['baja_z'] if rng.random() < 0.62 else cN['capas']['alta_z']
            spr(bx + rng.uniform(*cN['deriva_x_m']) + rng.uniform(-0.9, 0.9),
                by + rng.uniform(-0.9, 0.9), rng.uniform(*capa),
                rng.uniform(*cN['diametro_m']), rng.uniform(*cN['opacidad']))
            nspr += 1
    for (bx, by, bz) in RIBNEB:
        for k in range(5):
            spr(bx + rng.uniform(0.2, 0.9), by + rng.uniform(-0.7, 0.7),
                bz + rng.uniform(-0.8, 0.4), rng.uniform(1.6, 3.2), rng.uniform(0.10, 0.18))
            nspr += 1
    # --- columnas de vapor (H7)
    cc = CFG['niebla']['columnas_h7']
    for (ccx, ccy) in cc['centros']:
        for k in range(cc['sprites']):
            f = k / (cc['sprites'] - 1)
            z = 5.5 + f * (rng.uniform(*cc['z_max']) - 5.5)
            op = cc['opacidad'][0] + (cc['opacidad'][1] - cc['opacidad'][0]) * f
            spr(ccx + rng.uniform(-1.5, 1.5) + f * 1.8, ccy + rng.uniform(-1.5, 1.5),
                z, 4.0 + 6.0 * f, op)
            nspr += 1
    # --- agua viva: splash
    sp = M['agua_clima']['splash']
    ch = CFG['agua_viva']['splash_chorros']
    for k in range(ch['n']):
        a = 2 * math.pi * k / ch['n'] + 0.4
        r = rng.uniform(0.25, 0.62)
        px_ = sp['cx'] + sp['rx'] * r * math.cos(a)
        py_ = sp['cy'] + sp['ry'] * r * math.sin(a)
        h = rng.uniform(*ch['altura_m'])
        mx(mk.cylinder((px_, py_, 0.03), (px_, py_, h), 0.045, 6), ch['color'], op=0.55,
           em='#FFFFFF', emi=0.25, rough=0.05, shadow=False)
        mx(mk.sphere((px_, py_, h), 0.09, 6, 4), '#FFFFFF', op=0.75, em='#FFFFFF', emi=0.3, shadow=False)
        spr(px_, py_, 0.10, rng.uniform(0.7, 1.1), 0.5, tex='corona')
    # espuma de borde (§7.2)
    per = mk.ell_pts(sp['cx'], sp['cy'], sp['rx'], sp['ry'], sp['rot'], 40)
    mx(mk.tube([(p[0], p[1], 0.05) for p in per], 0.06, 6), '#FFFFFF', op=0.30,
       em='#FFFFFF', emi=0.2, rough=0.3, shadow=False)
    # --- goteo de embudos: 12 discos mas bajos sobre estancia
    DIS = sorted([d for d in M['paisaje']['discs'] if d.get('cota', 6.0) <= 6.0],
                 key=lambda d: d.get('cota', 6.0))[:CFG['agua_viva']['goteo_discos']['n_discos']]
    for d in DIS:
        z0 = d.get('cota', 6.0) - 0.62
        z = z0
        while z > 0.35:
            lnx((d['cx'], d['cy'], z), (d['cx'], d['cy'], max(z - 0.13, 0.15)))
            z -= 0.24
        spr(d['cx'], d['cy'], 0.08, 0.55, 0.42, tex='corona')
    # --- mangueras: 3 huerto C1 + 1 viveros (istmo v003)
    HU = [(-56, 6), (-48, 11), (-52, 15)]
    VV = [tuple(CFG_VIVEROS[0])]
    for (hx, hy) in HU + VV:
        L = rng.uniform(*CFG['agua_viva']['mangueras']['arco_alcance_m'])
        aa = rng.uniform(0, 6.28)
        ux, uy = math.cos(aa), math.sin(aa)
        pts = [(hx, hy, 0.05), (hx + ux*0.3, hy + uy*0.3, 0.55), (hx + ux*0.8, hy + uy*0.8, 0.95)]
        mx(mk.tube(pts, 0.035, 5), '#E06B9C', rough=0.4)                      # manguera rosa
        arc = []
        for t in range(9):
            f = t / 8
            arc.append((hx + ux*(0.8 + f*L), hy + uy*(0.8 + f*L), 0.95 + 1.1*f - 2.2*f*f))
        mx(mk.tube(arc, 0.022, 5), '#DFF2EE', op=0.6, em='#FFFFFF', emi=0.2, rough=0.05, shadow=False)
        spr(hx + ux*(0.8 + L), hy + uy*(0.8 + L), 0.1, 0.6, 0.4, tex='corona')
    # --- rebosaderos B-C2a / B-C3a
    for p in M['agua_clima']['pools']:
        if p['id'] in CFG['agua_viva']['rebosaderos']:
            a = 0.9
            ex_ = p['cx'] + p['rx'] * math.cos(a); ey_ = p['cy'] + p['ry'] * math.sin(a)
            z = p['cota']
            while z > 0.3:
                lnx((ex_, ey_, z), (ex_, ey_, max(z - 0.3, 0.1)), op=0.85)
                z -= 0.42
            mx(mk.cylinder((ex_, ey_, 0.02), (ex_, ey_, 0.06), 0.5, 10), '#DFF2EE', op=0.5,
               em='#FFFFFF', emi=0.15, rough=0.1, shadow=False)
    return nspr


# ---------------- poblacion PERSON2 (deterministas + validadas) ----------------
def persona(pose, x, y, z0, rot, tint, esc=1.0):
    """low-poly: piernas + torso + cabeza; poses del plan §5."""
    ca, sa = math.cos(rot), math.sin(rot)
    P = []

    def T(vf):
        V, F = vf
        V2 = [((vx*ca - vy*sa)*esc + x, (vx*sa + vy*ca)*esc + y, vz*esc + z0) for (vx, vy, vz) in V]
        P.append((V2, F))
    if pose == 'sentado':
        T(mk.cylinder((0, 0.0, 0.45), (0, 0, 1.12), 0.155, 7))
        T(mk.cylinder((0.16, -0.09, 0.45), (0.30, -0.09, 0.10), 0.06, 5))
        T(mk.cylinder((0.16, 0.09, 0.45), (0.30, 0.09, 0.10), 0.06, 5))
        T(mk.sphere((0, 0, 1.27), 0.105, 6, 5))
    elif pose == 'cuclillas':
        T(mk.cylinder((0, 0, 0.32), (0, 0, 0.86), 0.16, 7))
        T(mk.sphere((0.1, -0.1, 0.24), 0.09, 5, 4))
        T(mk.sphere((0.1, 0.1, 0.24), 0.09, 5, 4))
        T(mk.sphere((0, 0, 1.0), 0.10, 6, 5))
    elif pose == 'andando':
        T(mk.cylinder((0.14, 0, 0.0), (0.03, 0, 0.80), 0.065, 5))
        T(mk.cylinder((-0.15, 0, 0.02), (-0.02, 0, 0.80), 0.065, 5))
        T(mk.cylinder((0, 0, 0.78), (0.03, 0, 1.48), 0.15, 7))
        T(mk.sphere((0.04, 0, 1.62), 0.105, 6, 5))
    else:   # de_pie / nino
        T(mk.cylinder((0.0, -0.085, 0.0), (0, -0.085, 0.80), 0.065, 5))
        T(mk.cylinder((0.0, 0.085, 0.0), (0, 0.085, 0.80), 0.065, 5))
        T(mk.cylinder((0, 0, 0.78), (0, 0, 1.48), 0.155, 7))
        T(mk.sphere((0, 0, 1.62), 0.105, 6, 5))
    for vf in P:
        mx(vf, tint, rough=0.85, layer='18_PEOPLE2')


def build_people(OB):
    rep = CFG['poblacion']['reparto']
    tintes = ['#8A8078', '#7C7770', '#948B7E', '#6E6A66', '#9A8F86', '#877F72']
    puestas = 0

    def tinte():
        return tintes[rng.randrange(len(tintes))]

    def try_place(px_, py_):
        return libre(px_, py_, OB)
    # splash: ninos saltando + de pie (dentro de la lamina, permitido)
    sp = M['agua_clima']['splash']
    for k in range(rep['splash']):
        a = rng.uniform(0, 6.28); r = rng.uniform(0.3, 0.85)
        px_ = sp['cx'] + sp['rx']*r*math.cos(a); py_ = sp['cy'] + sp['ry']*r*math.sin(a)
        if k < 4:
            persona('nino', px_, py_, 0.14, rng.uniform(0, 6.28), '#A88C74', esc=0.58)
            spr(px_, py_, 0.08, 0.5, 0.45, tex='corona')
        else:
            persona('de_pie', px_, py_, 0.0, rng.uniform(0, 6.28), tinte())
        puestas += 1
    # bancos: sentados sobre el borde de un banco
    bpts = [q for b in M['programa']['benches'] for q in b['pts'][1::2]]
    rng.shuffle(bpts)
    n = 0
    for q in bpts:
        if n >= rep['bancos']:
            break
        persona('sentado', q[0], q[1], 0.0, rng.uniform(0, 6.28), tinte())
        n += 1; puestas += 1
    # corredores: andando sobre los ejes v003
    CORRS = [c['pts'] for c in M['circulacion']['corridors']]
    n = 0
    intentos = 0
    while n < rep['corredores'] and intentos < 400:
        intentos += 1
        pts = CORRS[rng.randrange(len(CORRS))]
        i = rng.randrange(len(pts) - 1)
        f = rng.random()
        px_ = pts[i][0] + (pts[i+1][0] - pts[i][0]) * f + rng.uniform(-0.8, 0.8)
        py_ = pts[i][1] + (pts[i+1][1] - pts[i][1]) * f + rng.uniform(-0.8, 0.8)
        if not try_place(px_, py_):
            continue
        d = math.atan2(pts[i+1][1] - pts[i][1], pts[i+1][0] - pts[i][0])
        persona('andando', px_, py_, 0.0, d + (0 if rng.random() < 0.5 else math.pi), tinte())
        n += 1; puestas += 1
    # cinta: andando por el tablero construido (+6.00); uno anclado al tramo de H5 (C2-N)
    i_h5 = min(range(len(PROF)), key=lambda i: (PROF[i][0] - 0.0)**2 + (PROF[i][1] - 30.7)**2)
    idxs = [i_h5] + [int(len(PROF) * f) for f in (0.14, 0.33, 0.55, 0.80)][:rep['cinta'] - 1]
    for i in idxs:
        i = max(1, min(i, len(PROF) - 2))
        d = math.atan2(PROF[i+1][1] - PROF[i-1][1], PROF[i+1][0] - PROF[i-1][0])
        persona('andando', PROF[i][0] + rng.uniform(-0.4, 0.4), PROF[i][1] + rng.uniform(-0.4, 0.4),
                6.0, d, tinte())
        puestas += 1
    # cupula, viveros, claros
    dm = M['estructura_principal']['dome']
    n = 0; intentos = 0
    while n < rep['cupula'] and intentos < 200:
        intentos += 1
        a = rng.uniform(0, 6.28); r = rng.uniform(1.5, dm['r'] - 1.5)
        px_ = dm['cx'] + r*math.cos(a); py_ = dm['cy'] + r*math.sin(a)
        if try_place(px_, py_):
            persona(('de_pie', 'cuclillas')[n % 2], px_, py_, 0.0, rng.uniform(0, 6.28), tinte())
            n += 1; puestas += 1
    for (vx, vy) in CFG_VIVEROS[:rep['viveros']]:
        for dx, dy in ((1.4, 0.3), (-1.2, 0.8), (0.4, -1.4)):
            if try_place(vx + dx, vy + dy):
                persona('cuclillas', vx + dx, vy + dy, 0.0, rng.uniform(0, 6.28), tinte())
                puestas += 1
                break
    CLAROS = [(31, 14), (-20, -4), (-2, 22), (56, 2)]
    for (cx0, cy0) in CLAROS[:rep['claros']]:
        for _ in range(30):
            px_, py_ = cx0 + rng.uniform(-4, 4), cy0 + rng.uniform(-4, 4)
            if try_place(px_, py_):
                persona('de_pie', px_, py_, 0.0, rng.uniform(0, 6.28), tinte())
                puestas += 1
                break
    # huerto: en cuclillas junto a los bancales (zona -62..-40 / 0..17, validada)
    n = 0; intentos = 0
    while n < rep['huerto'] and intentos < 300:
        intentos += 1
        px_, py_ = rng.uniform(-61, -41), rng.uniform(1, 16)
        if try_place(px_, py_):
            persona('cuclillas', px_, py_, 0.0, rng.uniform(0, 6.28), tinte())
            n += 1; puestas += 1
    return puestas


CFG_VIVEROS = M['mantenimiento_v003']['viveros']

# ---------------- ejecucion ----------------
gen_tex()
print('E03-1 tex_data2.js OK')
_, OB = load_obstacles()
print('obstaculos en banda de cuerpo: %d bbox' % len(OB))
nspr = build_extra(OB)
npers = build_people(OB)
with open(os.path.join(VIEW, 'scene_extra.js'), 'w', encoding='utf-8') as f:
    f.write('const EXTRA_SPRITES = '); json.dump(SPR, f, separators=(',', ':'))
    f.write(';\nconst EXTRA_MESHES = '); json.dump(MESHX, f, separators=(',', ':'))
    f.write(';\nconst EXTRA_LINES = '); json.dump(LINX, f, separators=(',', ':'))
    f.write(';\n')
xs = [s['x'] for s in SPR]; ys = [s['y'] for s in SPR]
print('E03-2 scene_extra.js OK · sprites %d (bbox x %.0f..%.0f y %.0f..%.0f) · mallas extra %d · lineas %d · personas %d'
      % (len(SPR), min(xs), max(xs), min(ys), max(ys), len(MESHX), len(LINX), npers))
print('luces:', ', '.join(CFG['luces'].keys()), '· camaras hero:', len(CFG['camaras_hero']))
