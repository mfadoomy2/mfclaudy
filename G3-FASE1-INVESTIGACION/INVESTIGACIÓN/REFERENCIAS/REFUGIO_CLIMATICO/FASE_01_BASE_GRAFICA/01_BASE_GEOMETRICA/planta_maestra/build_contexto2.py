"""Procesa el 2o lote OSM (plaza, fuentes, monumentos, arboles, farolas) al mismo CRS local."""
import json
import math
import os

LAT0, LON0 = 40.41690, -3.70350
M_LAT = 110574.0
M_LON = 111320.0 * math.cos(math.radians(LAT0))
SCRATCH = r'C:\Users\IRAXX_~1\AppData\Local\Temp\claude\C--Users-iraxx-c0wouln-OneDrive-Documentos-iraxxxdios-ARQUITECTURA-xxxmiguelxxx-Monteserin\c4200da3-0ae3-4130-a8d5-509af52344d7\scratchpad'


def project(lat, lon):
    return round((lon - LON0) * M_LON, 2), round((lat - LAT0) * M_LAT, 2)


data = json.load(open(os.path.join(SCRATCH, 'sol_osm2.json'), encoding='utf-8'))
nodes = {}
for el in data['elements']:
    if el['type'] == 'node':
        nodes[el['id']] = el

squares, fountains, monuments, trees, lamps, platforms, stations = [], [], [], [], [], [], []
for el in data['elements']:
    t = el.get('tags', {})
    if el['type'] == 'way':
        pts = [project(nodes[n]['lat'], nodes[n]['lon']) for n in el['nodes'] if n in nodes and 'lat' in nodes[n]]
        if t.get('place') == 'square':
            squares.append({'name': t.get('name', ''), 'pts': pts})
        elif t.get('amenity') == 'fountain':
            fountains.append({'name': t.get('name', ''), 'pts': pts})
        elif t.get('railway') == 'platform':
            platforms.append({'name': t.get('name', ''), 'pts': pts})
    elif el['type'] == 'node' and t:
        x, y = project(el['lat'], el['lon'])
        item = {'name': t.get('name', ''), 'x': x, 'y': y}
        if t.get('amenity') == 'fountain':
            fountains.append(item)
        elif 'historic' in t or t.get('tourism') == 'artwork':
            item['kind'] = t.get('historic', 'artwork')
            monuments.append(item)
        elif t.get('natural') == 'tree':
            trees.append(item)
        elif t.get('highway') == 'street_lamp':
            lamps.append(item)
        elif t.get('railway') == 'station':
            stations.append(item)

out = {
    'squares': squares, 'fountains': fountains, 'monuments': monuments,
    'trees': trees, 'lamps': lamps, 'platforms': platforms, 'stations': stations,
}
dst = os.path.join(os.path.dirname(__file__), 'contexto_sol2.json')
json.dump(out, open(dst, 'w', encoding='utf-8'), ensure_ascii=False)
print('plazas:', [(s['name'], len(s['pts'])) for s in squares])
print('fuentes:', fountains)
print('monumentos:', monuments)
print('arboles:', len(trees), 'farolas:', len(lamps), 'estaciones:', stations)
