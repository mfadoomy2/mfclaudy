"""Anade las building RELATIONS (multipoligonos: Casa de Correos, etc.) a contexto_sol.json
y genera una vista previa PNG del contexto completo."""
import json
import math
import os

LAT0, LON0 = 40.41690, -3.70350
M_LAT = 110574.0
M_LON = 111320.0 * math.cos(math.radians(LAT0))
HERE = os.path.dirname(__file__)
SCRATCH = r'C:\Users\IRAXX_~1\AppData\Local\Temp\claude\C--Users-iraxx-c0wouln-OneDrive-Documentos-iraxxxdios-ARQUITECTURA-xxxmiguelxxx-Monteserin\c4200da3-0ae3-4130-a8d5-509af52344d7\scratchpad'


def project(lat, lon):
    return round((lon - LON0) * M_LON, 2), round((lat - LAT0) * M_LAT, 2)


data = json.load(open(os.path.join(SCRATCH, 'sol_osm3.json'), encoding='utf-8'))
nodes, ways, rels = {}, {}, []
for el in data['elements']:
    if el['type'] == 'node':
        nodes[el['id']] = (el.get('lat'), el.get('lon'))
    elif el['type'] == 'way':
        ways[el['id']] = el
    elif el['type'] == 'relation':
        rels.append(el)


def chain(members):
    """Une ways 'outer' en anillos."""
    segs = []
    for m in members:
        if m['type'] == 'way' and m['role'] in ('outer', '') and m['ref'] in ways:
            nds = ways[m['ref']]['nodes']
            segs.append(list(nds))
    rings = []
    while segs:
        ring = segs.pop(0)
        changed = True
        while changed and ring[0] != ring[-1]:
            changed = False
            for i, s in enumerate(segs):
                if s[0] == ring[-1]:
                    ring += s[1:]; segs.pop(i); changed = True; break
                if s[-1] == ring[-1]:
                    ring += list(reversed(s))[1:]; segs.pop(i); changed = True; break
                if s[-1] == ring[0]:
                    ring = s + ring[1:]; segs.pop(i); changed = True; break
                if s[0] == ring[0]:
                    ring = list(reversed(s)) + ring[1:]; segs.pop(i); changed = True; break
        rings.append(ring)
    return rings


rel_buildings = []
for r in rels:
    name = r.get('tags', {}).get('name', '')
    for ring in chain(r.get('members', [])):
        pts = [project(*nodes[n]) for n in ring if n in nodes and nodes[n][0] is not None]
        if len(pts) >= 3:
            rel_buildings.append({'name': name, 'levels': '', 'pts': pts})

ctx_path = os.path.join(HERE, 'contexto_sol.json')
ctx = json.load(open(ctx_path, encoding='utf-8'))
have = {(b['name'], len(b['pts'])) for b in ctx['buildings']}
added = 0
for b in rel_buildings:
    ctx['buildings'].append(b)
    added += 1
json.dump(ctx, open(ctx_path, 'w', encoding='utf-8'), ensure_ascii=False)
print('relations anadidas:', added)
for b in rel_buildings:
    if b['name']:
        xs = [p[0] for p in b['pts']]; ys = [p[1] for p in b['pts']]
        if -150 < min(xs) and max(xs) < 200 and -150 < min(ys) and max(ys) < 150:
            print('  ', b['name'], 'X %.0f..%.0f Y %.0f..%.0f' % (min(xs), max(xs), min(ys), max(ys)))

# ---- preview ----
from PIL import Image, ImageDraw

W, H = 1800, 1300
X0, X1 = -170, 200   # metros
Y0, Y1 = -120, 140
sx = W / (X1 - X0)
sy = H / (Y1 - Y0)
s = min(sx, sy)


def T(p):
    return ((p[0] - X0) * s, (Y1 - p[1]) * s)


img = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(img)
for hgw in ctx['highways']:
    d.line([T(p) for p in hgw['pts']], fill=(200, 200, 200), width=2)
for b in ctx['buildings']:
    if len(b['pts']) >= 3:
        d.polygon([T(p) for p in b['pts']], fill=(228, 226, 222), outline=(140, 140, 140))
ctx2 = json.load(open(os.path.join(HERE, 'contexto_sol2.json'), encoding='utf-8'))
for t in ctx2['trees']:
    x, y = T((t['x'], t['y']))
    d.ellipse([x - 3, y - 3, x + 3, y + 3], outline=(80, 160, 80))
for m in ctx2['monuments']:
    if abs(m['x']) < 200 and abs(m['y']) < 150 and m['name'] in (
            'Estatua de la Mariblanca', 'Kilómetro Cero', 'Reloj de la Puerta del Sol'):
        x, y = T((m['x'], m['y']))
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(220, 60, 120))
for e in ctx['metro_entrances']:
    x, y = T((e['x'], e['y']))
    d.rectangle([x - 5, y - 5, x + 5, y + 5], outline=(0, 0, 200), width=2)
# origen
x, y = T((0, 0))
d.line([x - 10, y, x + 10, y], fill=(255, 0, 0), width=2)
d.line([x, y - 10, x, y + 10], fill=(255, 0, 0), width=2)
img.save(os.path.join(HERE, 'preview_contexto.png'))
print('preview guardada')
