# -*- coding: utf-8 -*-
"""
MODELO 3D ESQUEMATICO — REFUGIO CLIMATICO PUERTA DEL SOL · FASE 01
Derivado de ../planta_maestra/geometria_maestra.json (la planta 2D es la fuente de verdad).

Salidas:
  - refugio_fase01.obj / .mtl : malla por grupos-familia (Z arriba, 1u=1m, X este, Y norte)
  - geometria_3d.json         : primitivas con cotas (para axonometria P02 y estudios Fase 02)

LOD 100-200: posicion, escala, forma, altura, familia. Sin detalle constructivo.
Cotas (seccion 12069BE7 + laminas tecnicas: suelo / dosel 5-10 m / infraestructura 10-12 m).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, '..', 'planta_maestra', 'geometria_maestra.json')
m = json.load(open(GEO, encoding='utf-8'))

V = []          # vertices
GROUPS = {}     # nombre -> lista de caras (tuplas de indices, 1-based)


def add_face(group, idx):
    GROUPS.setdefault(group, []).append(idx)


def vtx(x, y, z):
    V.append((round(x, 3), round(y, 3), round(z, 3)))
    return len(V)


def quad(g, a, b, c, d):
    add_face(g, (a, b, c, d))


def tri(g, a, b, c):
    add_face(g, (a, b, c))


def ell_pt(cx, cy, rx, ry, rot_deg, a):
    r = math.radians(rot_deg)
    x, y = rx * math.cos(a), ry * math.sin(a)
    return (cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r))


def tube_along(g, path3, r=0.4, nseg=8):
    """Tubo circular a lo largo de una polilinea 3D."""
    rings = []
    n = len(path3)
    for i, (x, y, z) in enumerate(path3):
        # direccion local
        x0, y0, z0 = path3[max(i - 1, 0)]
        x1, y1, z1 = path3[min(i + 1, n - 1)]
        dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
        L = math.sqrt(dx * dx + dy * dy + dz * dz) or 1
        dx, dy, dz = dx / L, dy / L, dz / L
        # base normal-binormal (aprox, up=Z)
        ux, uy, uz = -dy, dx, 0
        UL = math.sqrt(ux * ux + uy * uy) or 1
        ux, uy = ux / UL, uy / UL
        wx = dy * uz - dz * uy
        wy = dz * ux - dx * uz
        wz = dx * uy - dy * ux
        ring = []
        for k in range(nseg):
            a = 2 * math.pi * k / nseg
            px = x + r * (math.cos(a) * ux + math.sin(a) * wx)
            py = y + r * (math.cos(a) * uy + math.sin(a) * wy)
            pz = z + r * (math.cos(a) * uz + math.sin(a) * wz)
            ring.append(vtx(px, py, pz))
        rings.append(ring)
    for i in range(n - 1):
        for k in range(nseg):
            a, b = rings[i][k], rings[i][(k + 1) % nseg]
            c, d = rings[i + 1][(k + 1) % nseg], rings[i + 1][k]
            quad(g, a, b, c, d)


def disc(g, cx, cy, z, r, nseg=20, th=0.15):
    top = [vtx(*ell_pt(cx, cy, r, r, 0, 2 * math.pi * k / nseg), z + th) for k in range(nseg)]
    bot = [vtx(*ell_pt(cx, cy, r, r, 0, 2 * math.pi * k / nseg), z) for k in range(nseg)]
    ct, cb = vtx(cx, cy, z + th), vtx(cx, cy, z)
    for k in range(nseg):
        tri(g, ct, top[k], top[(k + 1) % nseg])
        tri(g, cb, bot[(k + 1) % nseg], bot[k])
        quad(g, top[k], bot[k], bot[(k + 1) % nseg], top[(k + 1) % nseg])


def slab_ell(g, cx, cy, z, rx, ry, rot, nseg=24, th=0.25):
    top = [vtx(*ell_pt(cx, cy, rx, ry, rot, 2 * math.pi * k / nseg), z + th) for k in range(nseg)]
    bot = [vtx(*ell_pt(cx, cy, rx, ry, rot, 2 * math.pi * k / nseg), z) for k in range(nseg)]
    ct, cb = vtx(cx, cy, z + th), vtx(cx, cy, z)
    for k in range(nseg):
        tri(g, ct, top[k], top[(k + 1) % nseg])
        tri(g, cb, bot[(k + 1) % nseg], bot[k])
        quad(g, top[k], bot[k], bot[(k + 1) % nseg], top[(k + 1) % nseg])


def prism(g, pts, z0, z1):
    """Extrusion vertical de un poligono (triangulacion en abanico)."""
    n = len(pts)
    top = [vtx(p[0], p[1], z1) for p in pts]
    bot = [vtx(p[0], p[1], z0) for p in pts]
    for k in range(1, n - 1):
        tri(g, top[0], top[k], top[k + 1])
        tri(g, bot[0], bot[k + 1], bot[k])
    for k in range(n):
        quad(g, top[k], bot[k], bot[(k + 1) % n], top[(k + 1) % n])


def sphere(g, cx, cy, cz, r, nu=10, nv=6):
    rows = []
    for j in range(nv + 1):
        phi = math.pi * j / nv
        row = []
        for i in range(nu):
            th_ = 2 * math.pi * i / nu
            row.append(vtx(cx + r * math.sin(phi) * math.cos(th_),
                           cy + r * math.sin(phi) * math.sin(th_),
                           cz + r * math.cos(phi)))
        rows.append(row)
    for j in range(nv):
        for i in range(nu):
            a, b = rows[j][i], rows[j][(i + 1) % nu]
            c, d = rows[j + 1][(i + 1) % nu], rows[j + 1][i]
            quad(g, a, b, c, d)


def cyl(g, cx, cy, z0, z1, r, nseg=8):
    top = [vtx(cx + r * math.cos(2 * math.pi * k / nseg), cy + r * math.sin(2 * math.pi * k / nseg), z1) for k in range(nseg)]
    bot = [vtx(cx + r * math.cos(2 * math.pi * k / nseg), cy + r * math.sin(2 * math.pi * k / nseg), z0) for k in range(nseg)]
    for k in range(nseg):
        quad(g, top[k], bot[k], bot[(k + 1) % nseg], top[(k + 1) % nseg])
    ct = vtx(cx, cy, z1)
    for k in range(nseg):
        tri(g, ct, top[k], top[(k + 1) % nseg])


# ---------------------------------------------------------------- cotas por familia
LOOP_Z = {'C1-L1': 9.0, 'C1-L2': 7.0, 'C1-L3': 7.5, 'C2-L1': 10.0, 'C2-L2': 8.0,
          'C2-L3': 7.0, 'C3-L1': 9.0, 'C3-L2': 7.5}

J3D = {'crs': '1u=1m; X este, Y norte, Z arriba; mismo origen que la planta', 'familias': {}}


def reg(fam, item):
    J3D['familias'].setdefault(fam, []).append(item)


# ---------------------------------------------------------------- 00 SUELO
prism('00_SUELO_PLAZA', [(-170, -130), (200, -130), (200, 140), (-170, 140)], -0.3, 0.0)

# ---------------------------------------------------------------- 01 CONTEXTO edificios
for b in m['contexto']['buildings']:
    pts = b['pts'][:-1] if b['pts'][0] == b['pts'][-1] else b['pts']
    if len(pts) < 3 or len(pts) > 80:
        continue
    try:
        lv = float(str(b.get('levels', '') or 0))
    except ValueError:
        lv = 0
    h = lv * 3.2 if lv else 18.0
    if b['name'] == 'Presidencia de la Comunidad de Madrid':
        h = 20.0
    prism('01_CONTEXTO_EDIFICIOS', pts, 0, h)
reg('contexto', dict(nota='edificios OSM extruidos; alturas por building:levels o 18 m por defecto (G3)'))

# ---------------------------------------------------------------- 02 LOOPS estructurales
for lp in m['estructura_principal']['loops']:
    z = LOOP_Z[lp['id']]
    path = []
    n = 64
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        x, y = ell_pt(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'], a)
        path.append((x, y, z + 0.8 * math.sin(2 * a)))   # leve ondulacion del anillo
    tube_along('02_LOOPS', path, r=0.45)
    reg('loops', dict(id=lp['id'], cx=lp['cx'], cy=lp['cy'], rx=lp['rx'], ry=lp['ry'],
                      rot=lp['rot'], z=z, g=lp['g']))

dm = m['estructura_principal']['dome']
sphere('02_LOOPS', dm['cx'], dm['cy'], 0.0, dm['r'], nu=12, nv=6)   # cupula (media esfera visible)
reg('cupula', dict(cx=dm['cx'], cy=dm['cy'], r=dm['r'], g=dm['g']))

# ---------------------------------------------------------------- 03 CINTA-RECORRIDO
rib = m['circulacion']['ribbon']
path3 = []
for i, (x, y) in enumerate(rib):
    z = 5.0 + 1.2 * math.sin(i * 0.12)   # ondulacion 3.8-6.2 m
    path3.append((x, y, z))
tube_along('03_CINTA', path3, r=1.25, nseg=6)
reg('cinta', dict(pts=[[round(p[0], 2), round(p[1], 2), round(p[2], 2)] for p in path3], ancho=2.5, g='G2'))

# ---------------------------------------------------------------- 04 MASTILES
for (mx, my) in m['estructura_ligera']['masts']:
    cyl('04_MASTILES', mx, my, 0, 7.5, 0.12, nseg=6)
reg('mastiles', dict(n=len(m['estructura_ligera']['masts']), h=7.5, g='G2'))

# ---------------------------------------------------------------- 05 DISCOS-CANOPY
for d in m['paisaje']['discs']:
    z = float(d.get('cota', 6.0))
    disc('05_DISCOS', d['cx'], d['cy'], z, d['r'])
    reg('discos', dict(cx=d['cx'], cy=d['cy'], r=d['r'], z=z, g=d.get('g', 'G3')))

# ---------------------------------------------------------------- 06 BALSAS elevadas + estanques
for p in m['agua_clima']['pools']:
    slab_ell('06_BALSAS', p['cx'], p['cy'], p['cota'], p['rx'], p['ry'], p['rot'])
    reg('balsas', dict(**p))
for p in m['agua_clima']['ground_ponds']:
    if p['kind'] == 'circle':
        disc('06_ESTANQUES', p['cx'], p['cy'], 0.0, p['r'], th=0.5)
        reg('estanques', dict(cx=p['cx'], cy=p['cy'], r=p['r'], z=0.5, g=p['g']))
    else:
        prism('06_ESTANQUES', p['pts'][:-1], 0, 0.5)
        reg('estanques', dict(pts=p['pts'], z=0.5, g=p['g']))
sp = m['agua_clima']['splash']
slab_ell('06_ESTANQUES', sp['cx'], sp['cy'], 0.0, sp['rx'], sp['ry'], sp['rot'], th=0.05)
reg('splash', dict(**sp))

# ---------------------------------------------------------------- 07 CAPSULAS
for c in m['programa']['capsules']:
    r = max(c['w'], c['h']) / 2
    z = {'suelo': r, 'media': 4.0, 'alta': 8.0}.get(c.get('cota', 'suelo'), r)
    sphere('07_CAPSULAS', c['cx'], c['cy'], z, r * 0.92)
    reg('capsulas', dict(cx=c['cx'], cy=c['cy'], r=r, z=z, cota=c.get('cota'), g=c.get('g', 'G2')))

# ---------------------------------------------------------------- 08 DEPOSITOS
for t in m['estructura_ligera']['tanks']:
    for k in range(t['n']):
        sphere('08_DEPOSITOS', t['cx'] + k * 2.6, t['cy'], 10.5, t['r'] * 0.9)
        cyl('08_DEPOSITOS', t['cx'] + k * 2.6, t['cy'], 0, 10.5 - t['r'], 0.15, nseg=6)
    reg('depositos', dict(**t, z=10.5))
for (dx, dy) in m['estructura_ligera']['drops']:
    sphere('08_DEPOSITOS', dx, dy, 1.2, 0.8, nu=8, nv=4)

# ---------------------------------------------------------------- 09 LAB + bancos
lab = m['programa']['lab']
prism('09_PROGRAMA', lab['pts'][:-1], 0, 4.0)
reg('lab', dict(pts=lab['pts'], h=4.0, g=lab['g']))
for b in m['programa']['benches']:
    p3 = [(x, y, 0.45) for (x, y) in b['pts']]
    tube_along('09_PROGRAMA', p3, r=0.3, nseg=4)

# ---------------------------------------------------------------- 10 VEGETACION
for t in m['contexto']['trees']:
    cyl('10_ARBOLES_EXIST', t['x'], t['y'], 0, 4.5, 0.18, nseg=5)
    sphere('10_ARBOLES_EXIST', t['x'], t['y'], 5.8, 2.2, nu=8, nv=4)
for (tx, ty) in m['paisaje']['new_trees']:
    cyl('10_ARBOLES_NUEVOS', tx, ty, 0, 5.0, 0.18, nseg=5)
    sphere('10_ARBOLES_NUEVOS', tx, ty, 6.5, 2.6, nu=8, nv=4)
reg('arboles', dict(existentes=len(m['contexto']['trees']), nuevos=len(m['paisaje']['new_trees'])))

# ---------------------------------------------------------------- 11 RED AGUA (tubos)
for w in m['agua_clima']['mains']:
    p3 = [(x, y, 2.2) for (x, y) in w]
    tube_along('11_RED_AGUA', p3, r=0.18, nseg=5)
reg('red_agua', dict(nota='trazado principal G3; nebulizadores como puntos en planta'))

# ---------------------------------------------------------------- salida
MTL = {
    '00_SUELO_PLAZA': (0.96, 0.95, 0.93), '01_CONTEXTO_EDIFICIOS': (0.90, 0.89, 0.86),
    '02_LOOPS': (0.18, 0.66, 0.64), '03_CINTA': (0.10, 0.50, 0.48),
    '04_MASTILES': (0.55, 0.55, 0.55), '05_DISCOS': (0.77, 0.88, 0.55),
    '06_BALSAS': (0.55, 0.81, 0.64), '06_ESTANQUES': (0.39, 0.73, 0.56),
    '07_CAPSULAS': (0.95, 0.48, 0.71), '08_DEPOSITOS': (0.93, 0.37, 0.63),
    '09_PROGRAMA': (0.66, 0.47, 0.29), '10_ARBOLES_EXIST': (0.62, 0.73, 0.56),
    '10_ARBOLES_NUEVOS': (0.37, 0.61, 0.33), '11_RED_AGUA': (0.94, 0.44, 0.68),
}
with open(os.path.join(HERE, 'refugio_fase01.mtl'), 'w') as f:
    for name, (r, g0, b) in MTL.items():
        f.write('newmtl %s\nKd %.2f %.2f %.2f\nd 0.9\n\n' % (name, r, g0, b))

with open(os.path.join(HERE, 'refugio_fase01.obj'), 'w') as f:
    f.write('# REFUGIO CLIMATICO PUERTA DEL SOL - FASE 01 - modelo esquematico LOD100-200\n')
    f.write('# 1 unidad = 1 m; X este, Y norte, Z arriba; origen lat 40.41690 lon -3.70350\n')
    f.write('mtllib refugio_fase01.mtl\n')
    for (x, y, z) in V:
        f.write('v %s %s %s\n' % (x, y, z))
    for gname, faces in GROUPS.items():
        f.write('g %s\nusemtl %s\n' % (gname, gname))
        for fc in faces:
            f.write('f ' + ' '.join(str(i) for i in fc) + '\n')

json.dump(J3D, open(os.path.join(HERE, 'geometria_3d.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('vertices:', len(V), '· grupos:', len(GROUPS))
print('caras:', sum(len(v) for v in GROUPS.values()))
print('OK -> refugio_fase01.obj / .mtl / geometria_3d.json')
