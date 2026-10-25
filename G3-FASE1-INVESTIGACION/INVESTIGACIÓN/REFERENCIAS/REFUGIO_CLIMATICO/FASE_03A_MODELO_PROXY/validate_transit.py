# -*- coding: utf-8 -*-
"""Validacion de transitabilidad del proxy: chequeos automaticos + plano de conflictos.
Genera _validacion/planta_conflictos.png y _validacion/informe.json
"""
import json
import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, '..', 'FASE_01_BASE_GRAFICA', '01_BASE_GEOMETRICA', 'planta_maestra', 'geometria_maestra.json')
m = json.load(open(GEO, encoding='utf-8'))
os.makedirs(os.path.join(HERE, '_validacion'), exist_ok=True)

# ---- overrides F03A (identicos a proxy_build) ----
OV = json.load(open(os.path.join(HERE, 'geometria_overrides_f03a.json'), encoding='utf-8'))
for c in m['circulacion']['corridors']:
    ov = OV['corridors'].get(c['id'])
    if ov:
        c['pts'] = [tuple(p) for p in ov]
METRO_XY = [(e['x'], e['y']) for e in m['contexto']['metro'] if -110 < e['x'] < 100 and -45 < e['y'] < 75]
R_EXCL = OV['metro_exclusion_radius']


def near_metro(x, y, extra=0.0):
    return any(math.hypot(x - mx, y - my) < R_EXCL + extra for (mx, my) in METRO_XY)


m['programa']['capsules'] = [c for c in m['programa']['capsules'] if not near_metro(c['cx'], c['cy'], max(c['w'], 1.8) / 2)]
for p in m['paisaje']['planters']:
    p['pts'] = [q for q in p['pts'] if not near_metro(q[0], q[1], 0.9)]
for b in m['programa']['benches']:
    b['pts'] = [q for q in b['pts'] if not near_metro(q[0], q[1], 0.5)]
m['estructura_ligera']['drops'] = [d for d in m['estructura_ligera']['drops'] if not near_metro(d[0], d[1], 1.0)]
m['estructura_ligera']['masts'] = [p for p in m['estructura_ligera']['masts'] if not near_metro(p[0], p[1], 0.3)]
m['paisaje']['new_trees'] = [t for t in m['paisaje']['new_trees'] if not near_metro(t[0], t[1], 0.4)]
for idx_s, (f0, f1) in OV.get('planter_trim', {}).items():
    pl = m['paisaje']['planters'][int(idx_s)]
    n = len(pl['pts'])
    pl['pts'] = pl['pts'][int(f0 * n):int(f1 * n)]
for pid, (nx_, ny_) in OV.get('pond_moves', {}).items():
    for p in m['agua_clima']['ground_ponds']:
        if p['id'] == pid and p['kind'] == 'circle':
            p['cx'], p['cy'] = nx_, ny_
cy_min = OV.get('capsule_rules', {}).get('T-O_cy_min')
if cy_min is not None:
    m['programa']['capsules'] = [c for c in m['programa']['capsules']
                                 if not (c.get('id') == 'T-O' and c['cy'] < cy_min)]
cx_max = OV.get('capsule_rules', {}).get('T-SE_cx_max')
if cx_max is not None:
    m['programa']['capsules'] = [c for c in m['programa']['capsules']
                                 if not (c.get('id') == 'T-SE' and c['cx'] > cx_max)]
lsh = OV.get('lab_shift')
if lsh:
    m['programa']['lab']['pts'] = [(p[0] + lsh[0], p[1] + lsh[1]) for p in m['programa']['lab']['pts']]
for (old, new) in OV.get('tree_moves', []):
    m['paisaje']['new_trees'] = [tuple(new) if (abs(t[0] - old[0]) < 0.6 and abs(t[1] - old[1]) < 0.6) else t
                                 for t in m['paisaje']['new_trees']]

H_RIBBON = 6.0
CLEAR_MIN = 3.0
PASS_MIN = 3.0    # ancho minimo deseable de paso en corredores principales

# ---------------- obstaculos en suelo (x, y, radio equivalente, tipo) ----------------
obs = []
for i, p in enumerate(m['paisaje']['planters']):
    for q in p['pts'][::2]:
        obs.append((q[0], q[1], 0.9, 'jardinera'))
for b in m['programa']['benches']:
    for q in b['pts'][::2]:
        obs.append((q[0], q[1], 0.5, 'banco'))
for p in m['agua_clima']['ground_ponds']:
    if p['kind'] == 'circle':
        obs.append((p['cx'], p['cy'], p['r'] + 0.2, 'estanque'))
    else:
        xs = [q[0] for q in p['pts']]
        ys = [q[1] for q in p['pts']]
        obs.append((sum(xs) / len(xs), sum(ys) / len(ys), 4.0, 'estanque'))
for c in m['programa']['capsules']:
    cid = c.get('id', '')
    dia = max(c['w'], 1.8)
    if cid in ('T-O', 'T-SE'):
        obs.append((c['cx'], c['cy'], 2.9, 'capsula-tren'))
    elif not (cid == 'R-N'):
        obs.append((c['cx'], c['cy'], dia / 2 + 0.2, 'capsula'))
for (dx, dy) in m['estructura_ligera']['drops']:
    obs.append((dx, dy, 0.95, 'deposito-gota'))
for (mx, my) in m['estructura_ligera']['masts']:
    obs.append((mx, my, 0.25, 'mastil'))
for t in m['estructura_ligera']['tanks']:
    for k in range(t['n']):
        obs.append((t['cx'] + k * 2.6, t['cy'], 0.4, 'poste-deposito'))
for (tx, ty) in m['paisaje']['new_trees']:
    obs.append((tx, ty, 0.3, 'arbol'))
for t in m['contexto']['trees']:
    obs.append((t['x'], t['y'], 0.35, 'arbol-existente'))
lab_pts = [(p[0], p[1]) for p in m['programa']['lab']['pts']]
lab_c = (sum(p[0] for p in lab_pts) / len(lab_pts), sum(p[1] for p in lab_pts) / len(lab_pts))
for ldx in (-5, 0, 5):
    obs.append((lab_c[0] + ldx, lab_c[1], 3.5, 'LAB'))
dm = m['estructura_principal']['dome']
obs.append((dm['cx'], dm['cy'], dm['r'], 'cupula'))

# soportes de cinta (reproducir la logica del builder)
rib = m['circulacion']['ribbon']
CORR = [c['pts'] for c in m['circulacion']['corridors']]


def dist_to_corridor(x, y):
    best = 1e9
    for pts in CORR:
        for i in range(len(pts) - 1):
            ax, ay = pts[i]
            bx, by = pts[i + 1]
            vx, vy = bx - ax, by - ay
            L2 = vx * vx + vy * vy or 1e-9
            t = max(0, min(1, ((x - ax) * vx + (y - ay) * vy) / L2))
            best = min(best, math.hypot(x - (ax + vx * t), y - (ay + vy * t)))
    return best


sups = []
acc = 0.0
for i in range(1, len(rib)):
    acc += math.hypot(rib[i][0] - rib[i - 1][0], rib[i][1] - rib[i - 1][1])
    if acc > 12:
        x, y = rib[i]
        if dist_to_corridor(x, y) >= 2.2:
            sups.append((x, y))
            obs.append((x, y, 0.3, 'soporte-cinta'))
            acc = 0.0

# ---------------- CHK1: ancho de paso en corredores ----------------
informe = dict(chk1_corredores=[], chk2_galibo=[], chk3_metro=[], chk4_soportes=dict(total=len(sups), junto_corredor=0),
               chk5_ocupacion=None)
viol_pts = []
for c in m['circulacion']['corridors']:
    pts = c['pts']
    worst = 1e9
    worst_p = None
    worst_kind = ''
    for i in range(len(pts) - 1):
        ax, ay = pts[i]
        bx, by = pts[i + 1]
        L = math.hypot(bx - ax, by - ay)
        for k in range(int(L / 2) + 1):
            t = k / max(int(L / 2), 1)
            px, py = ax + (bx - ax) * t, ay + (by - ay) * t
            dmin = 1e9
            dkind = ''
            for (ox, oy, orad, kind) in obs:
                if kind in ('arbol', 'arbol-existente', 'mastil'):
                    continue   # esbeltos: chequeo aparte chk1b (>=0.8 m al fuste)
                d = math.hypot(px - ox, py - oy) - orad
                if d < dmin:
                    dmin = d
                    dkind = '%s(%.0f,%.0f)' % (kind, ox, oy)
            if dmin < worst:
                worst = dmin
                worst_p = (px, py)
                worst_kind = dkind
    paso = worst * 2  # ancho libre = 2 x distancia al obstaculo mas cercano
    ok = paso >= PASS_MIN
    informe['chk1_corredores'].append(dict(id=c['id'], paso_min_m=round(paso, 2), ok=ok,
                                           punto=[round(worst_p[0], 1), round(worst_p[1], 1)], culpable=worst_kind))
    if not ok:
        viol_pts.append((worst_p, 'paso %.1f m' % paso))

# ---------------- CHK1b: esbeltos (arboles/mastiles) a >=0.8 m del eje de paso ----------------
informe['chk1b_esbeltos'] = []
for c in m['circulacion']['corridors']:
    pts = c['pts']
    for (ox, oy, orad, kind) in obs:
        if kind not in ('arbol', 'arbol-existente', 'mastil'):
            continue
        dd = 1e9
        for i in range(len(pts) - 1):
            ax, ay = pts[i]
            bx, by = pts[i + 1]
            vx, vy = bx - ax, by - ay
            L2 = vx * vx + vy * vy or 1e-9
            t = max(0, min(1, ((ox - ax) * vx + (oy - ay) * vy) / L2))
            dd = min(dd, math.hypot(ox - (ax + vx * t), oy - (ay + vy * t)))
        if dd - orad < 0.8:
            informe['chk1b_esbeltos'].append(dict(corredor=c['id'], kind=kind, pos=[round(ox, 1), round(oy, 1)],
                                                  dist=round(dd - orad, 2)))

# ---------------- CHK2: galibo bajo discos sobre corredores ----------------
for d in m['paisaje']['discs']:
    cota = min(max(d.get('cota', 6.0), 4.2), 8.5)
    sag = max(0.25, d['r'] * 0.18)
    bottom = cota - sag
    if dist_to_corridor(d['cx'], d['cy']) < d['r'] and bottom < CLEAR_MIN:
        informe['chk2_galibo'].append(dict(disco=[d['cx'], d['cy']], bajo=round(bottom, 2)))
        viol_pts.append(((d['cx'], d['cy']), 'galibo %.1f' % bottom))

# ---------------- CHK3: claros de metro ----------------
for e in m['contexto']['metro']:
    if not (-110 < e['x'] < 100 and -45 < e['y'] < 75):
        continue
    bad = []
    for (ox, oy, orad, kind) in obs:
        if kind in ('arbol-existente', 'mastil', 'soporte-cinta'):
            continue   # reubicables a nivel proxy; los mastiles se retiran del claro en el builder
        if abs(ox - e['x']) < 3.5 + orad and abs(oy - e['y']) < 3.5 + orad:
            bad.append('%s(%.0f,%.0f)' % (kind, ox, oy))
    informe['chk3_metro'].append(dict(boca=e.get('name', ''), pos=[e['x'], e['y']], invasores=bad, ok=not bad))
    if bad:
        viol_pts.append(((e['x'], e['y']), 'metro: ' + ','.join(bad[:2])))

# ---------------- CHK5: ocupacion de suelo ----------------
area_obs = sum(math.pi * orad ** 2 for (_, _, orad, k) in obs if k not in ('mastil', 'arbol-existente'))
informe['chk5_ocupacion'] = dict(area_obstaculos_m2=int(area_obs), plaza_m2=10957,
                                 porcentaje=round(100 * area_obs / 10957, 1))

# ---------------- plano de conflictos ----------------
W, Hh = 1800, 1200
X0, X1, Y0, Y1 = -110, 100, -50, 80
s = min(W / (X1 - X0), Hh / (Y1 - Y0))


def T(p):
    return ((p[0] - X0) * s, (Y1 - p[1]) * s)


img = Image.new('RGB', (W, Hh), 'white')
dr = ImageDraw.Draw(img)
for b in m['contexto']['buildings']:
    if len(b['pts']) >= 3:
        dr.polygon([T(p) for p in b['pts']], fill=(238, 236, 231), outline=(200, 197, 190))
for c in m['circulacion']['corridors']:
    dr.line([T(p) for p in c['pts']], fill=(140, 190, 235), width=14)
for (ox, oy, orad, kind) in obs:
    x, y = T((ox, oy))
    r = max(orad * s, 2)
    col = (111, 143, 83) if 'jardinera' in kind or 'arbol' in kind else (
        (231, 148, 172) if 'capsula' in kind or 'deposito' in kind else (150, 150, 150))
    dr.ellipse([x - r, y - r, x + r, y + r], outline=col, width=2)
rp = [T(p) for p in rib]
dr.line(rp, fill=(46, 110, 107), width=5)
for (p, txt) in viol_pts:
    x, y = T(p)
    dr.ellipse([x - 14, y - 14, x + 14, y + 14], outline=(220, 30, 30), width=4)
    dr.text((x + 16, y - 8), txt, fill=(220, 30, 30))
dr.text((20, 20), 'VALIDACION DE TRANSITABILIDAD - azul: corredores · verde oscuro: cinta · rojo: conflictos', fill=(60, 60, 60))
img.save(os.path.join(HERE, '_validacion', 'planta_conflictos.png'))

json.dump(informe, open(os.path.join(HERE, '_validacion', 'informe.json'), 'w', encoding='utf-8'), indent=1)
print(json.dumps(informe['chk1_corredores'], indent=1))
print('galibo malos:', len(informe['chk2_galibo']))
print('metro:', [(x['boca'], x['ok'], x['invasores']) for x in informe['chk3_metro']])
print('ocupacion suelo: %s%%' % informe['chk5_ocupacion']['porcentaje'])
print('violaciones dibujadas:', len(viol_pts))
