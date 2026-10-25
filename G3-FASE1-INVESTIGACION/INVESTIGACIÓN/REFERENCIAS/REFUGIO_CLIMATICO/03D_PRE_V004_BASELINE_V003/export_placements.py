# -*- coding: utf-8 -*-
"""03D: exporta a CSV las posiciones VALIDADAS de la capa E03 (personas y efectos) para la via B (D5/V-Ray)."""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
C3 = os.path.normpath(os.path.join(HERE, '..', 'FASE_03C_VISUALIZACION'))
V3 = os.path.normpath(os.path.join(HERE, '..', 'FASE_03B6_RESOLUCION'))
M = json.load(open(os.path.join(V3, 'geometria_maestra_v003.json'), encoding='utf-8'))
CFG = json.load(open(os.path.join(C3, 'atmos_config.json'), encoding='utf-8'))
txt = open(os.path.join(C3, '_viewer', 'scene_extra.js'), encoding='utf-8').read()
a = txt.index('const EXTRA_MESHES = ') + len('const EXTRA_MESHES = ')
XM = json.loads(txt[a:txt.index(';\nconst EXTRA_LINES')])

# personas: agrupar partes por centroide XY (una persona = 3-4 partes a <0.6 m)
pers = []
for o in XM:
    if o.get('layer') != '18_PEOPLE2':
        continue
    xs = [v[0] for v in o['V']]; ys = [v[1] for v in o['V']]; zs = [v[2] for v in o['V']]
    pers.append((sum(xs) / len(xs), sum(ys) / len(ys), min(zs), max(zs), o['color']))
grupos = []
for p in pers:
    for g in grupos:
        if abs(p[0] - g[0][0]) < 0.75 and abs(p[1] - g[0][1]) < 0.75:
            g.append(p)
            break
    else:
        grupos.append([p])
with open(os.path.join(HERE, 'PEOPLE_PLACEMENT_03D.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['id', 'x', 'y', 'z_base', 'altura_aprox', 'pose_estimada', 'tinte'])
    for i, g in enumerate(grupos):
        cx = sum(p[0] for p in g) / len(g)
        cy = sum(p[1] for p in g) / len(g)
        z0 = min(p[2] for p in g)
        h = max(p[3] for p in g) - z0
        pose = 'nino' if h < 1.1 else ('sentado' if h < 1.45 else ('cuclillas' if h < 1.2 else 'de_pie/andando'))
        w.writerow(['P%02d' % (i + 1), round(cx, 2), round(cy, 2), round(z0, 2), round(h, 2), pose, g[0][4]])
print('personas:', len(grupos))

with open(os.path.join(HERE, 'EFFECTS_03D.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['tipo', 'x', 'y', 'z', 'parametro'])
    for (nx, ny) in M['agua_clima']['nebul']:
        w.writerow(['boquilla_niebla', round(nx, 2), round(ny, 2), 4.0, 'nube r3, 5 L/h'])
    for (ccx, ccy) in CFG['niebla']['columnas_h7']['centros']:
        w.writerow(['columna_vapor', ccx, ccy, '5-19', 'volumetrica, ρ baja'])
    sp = M['agua_clima']['splash']
    w.writerow(['splash', sp['cx'], sp['cy'], 0.03, '10 chorros 0.5-1.6 m + espuma perimetral'])
    for p in M['agua_clima']['pools']:
        if p['id'] in CFG['agua_viva']['rebosaderos']:
            w.writerow(['rebosadero', p['cx'], p['cy'], p['cota'], p['id']])
    for ln in M['mantenimiento_v003']['recirculacion']:
        w.writerow(['recirculacion', ln[0][0], ln[0][1], 0.26, 'linea por cluster'])
print('efectos ok')
