# -*- coding: utf-8 -*-
"""Panel de composicion (dibujo matriz / HR01 / FE9A5E6E / planta maestra) + metricas de holgura."""
import json
import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = r'C:\Users\iraxx_c0wouln\OneDrive\Documentos\iraxxxdios_ARQUITECTURA\xxxmiguelxxx\Monteserin\MONTESERIN IA\MONTESERIN IA\MUTACIONES (DIBUJO + IA)\DIBUJO3 (REFUGIO CLIMATICO)'
GEO = os.path.join(HERE, '..', 'planta_maestra', 'geometria_maestra.json')
PLANTA_PNG = os.path.join(HERE, '..', 'planta_maestra', 'preview_planta.png')

W = 1400
rows = []
for path, label in [
    (os.path.join(BASE, '00_DIBUJO 03.jpg'), '00_DIBUJO 03 (matriz)'),
    (os.path.join(BASE, 'HR01.png'), 'HR01 (cenital arquitectonica)'),
    (os.path.join(BASE, 'IN PROGRESS REFUGIO', 'FE9A5E6E-1209-4D9C-86C1-1E5D22F5D09F.png'), 'FE9A5E6E (cenital pura)'),
    (PLANTA_PNG, 'PLANTA MAESTRA FASE 01 (norte arriba)'),
]:
    im = Image.open(path).convert('RGB')
    h = int(im.height * W / im.width)
    rows.append((im.resize((W, h)), label))

Htot = sum(h.height + 34 for h, _ in rows)
panel = Image.new('RGB', (W, Htot), 'white')
d = ImageDraw.Draw(panel)
y = 0
for im, label in rows:
    d.rectangle([0, y, W, y + 30], fill=(20, 20, 20))
    d.text((10, y + 9), label, fill='white')
    panel.paste(im, (0, y + 34))
    y += im.height + 34
panel.save(os.path.join(HERE, 'validacion_C_composicion.png'))
print('-> validacion_C_composicion.png')

# ---------------- metricas ----------------
m = json.load(open(GEO, encoding='utf-8'))
CORREOS_Y = -33.0
els = []


def ell_pts(cx, cy, rx, ry, rot, n=90):
    r = math.radians(rot)
    return [(cx + rx * math.cos(2 * math.pi * i / n) * math.cos(r) - ry * math.sin(2 * math.pi * i / n) * math.sin(r),
             cy + rx * math.cos(2 * math.pi * i / n) * math.sin(r) + ry * math.sin(2 * math.pi * i / n) * math.cos(r))
            for i in range(n)]


for lp in m['estructura_principal']['loops']:
    els += ell_pts(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'])
els += m['circulacion']['ribbon']
for c in m['programa']['capsules']:
    els.append((c['cx'], c['cy']))

min_y = min(p[1] for p in els)
max_y = max(p[1] for p in els)
min_x = min(p[0] for p in els)
max_x = max(p[0] for p in els)
print('extension intervencion: X %.1f..%.1f (%.0f m) · Y %.1f..%.1f (%.0f m)' % (min_x, max_x, max_x - min_x, min_y, max_y, max_y - min_y))
print('banda libre ante Casa de Correos (fachada y=-33): %.1f m' % (min_y - CORREOS_Y))

mb = m['contexto']['hitos']['mariblanca']
dmb = min(math.hypot(p[0] - mb[0], p[1] - mb[1]) for p in els)
print('distancia minima a Mariblanca: %.1f m' % dmb)
c3 = m['contexto']['hitos']['carlos_iii']
dc3 = min(math.hypot(p[0] - c3[0], p[1] - c3[1]) for p in els)
print('distancia minima a Carlos III: %.1f m' % dc3)

# superficie de dosel total (discos + balsas) vs plaza
a_d = sum(math.pi * d0['r'] ** 2 for d0 in m['paisaje']['discs'])
a_p = sum(math.pi * p['rx'] * p['ry'] for p in m['agua_clima']['pools'])
print('dosel: discos %.0f m2 + balsas %.0f m2 = %.0f m2 (%.0f%% de 10957 m2)' % (a_d, a_p, a_d + a_p, 100 * (a_d + a_p) / 10957))
