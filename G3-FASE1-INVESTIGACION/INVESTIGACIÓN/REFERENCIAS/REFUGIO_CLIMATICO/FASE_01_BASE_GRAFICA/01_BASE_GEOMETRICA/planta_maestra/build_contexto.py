"""Extrae el contexto urbano real de Puerta del Sol desde OSM (Overpass JSON)
y lo proyecta a coordenadas metricas locales.

Sistema de coordenadas del proyecto (BASE MAESTRA):
  - 1 unidad = 1 metro
  - origen (0,0) = centro aproximado de la plaza (lat 40.41690, lon -3.70350)
  - +X = este, +Y = norte  (en SVG se invierte Y al dibujar)
"""
import json
import math
import os

LAT0, LON0 = 40.41690, -3.70350
M_PER_DEG_LAT = 110574.0
M_PER_DEG_LON = 111320.0 * math.cos(math.radians(LAT0))

SRC = r'C:\Users\IRAXX_~1\AppData\Local\Temp\claude\C--Users-iraxx-c0wouln-OneDrive-Documentos-iraxxxdios-ARQUITECTURA-xxxmiguelxxx-Monteserin\c4200da3-0ae3-4130-a8d5-509af52344d7\scratchpad\sol_osm.json'
DST = os.path.join(os.path.dirname(__file__), 'contexto_sol.json')


def project(lat, lon):
    return round((lon - LON0) * M_PER_DEG_LON, 2), round((lat - LAT0) * M_PER_DEG_LAT, 2)


def main():
    data = json.load(open(SRC, encoding='utf-8'))
    nodes = {}
    ways = []
    entrances = []
    for el in data['elements']:
        if el['type'] == 'node':
            nodes[el['id']] = (el.get('lat'), el.get('lon'))
            if el.get('tags', {}).get('railway') == 'subway_entrance':
                entrances.append(el)
        elif el['type'] == 'way':
            ways.append(el)

    buildings, highways = [], []
    for w in ways:
        tags = w.get('tags', {})
        pts = []
        for nid in w['nodes']:
            if nid in nodes and nodes[nid][0] is not None:
                pts.append(project(*nodes[nid]))
        if len(pts) < 2:
            continue
        if 'building' in tags:
            buildings.append({
                'name': tags.get('name', ''),
                'levels': tags.get('building:levels', ''),
                'pts': pts,
            })
        elif 'highway' in tags:
            highways.append({
                'name': tags.get('name', ''),
                'kind': tags['highway'],
                'pts': pts,
            })

    metro = []
    for e in entrances:
        x, y = project(e['lat'], e['lon'])
        metro.append({'name': e.get('tags', {}).get('name', ''), 'x': x, 'y': y})

    out = {
        'crs': '1u=1m, origen lat40.41690 lon-3.70350, +X este +Y norte',
        'buildings': buildings,
        'highways': highways,
        'metro_entrances': metro,
    }
    json.dump(out, open(DST, 'w', encoding='utf-8'), ensure_ascii=False)

    xs = [p[0] for b in buildings for p in b['pts']]
    ys = [p[1] for b in buildings for p in b['pts']]
    print('edificios:', len(buildings), 'calles:', len(highways), 'bocas metro:', len(metro))
    print('bbox edificios: X %.0f..%.0f  Y %.0f..%.0f' % (min(xs), max(xs), min(ys), max(ys)))
    named = sorted({b['name'] for b in buildings if b['name']})
    print('edificios con nombre:', ' | '.join(named[:20]))
    print('bocas:', ' | '.join(m['name'] or ('(%.0f,%.0f)' % (m['x'], m['y'])) for m in metro[:15]))
    hnames = sorted({h['name'] for h in highways if h['name']})
    print('calles:', ' | '.join(hnames[:30]))


if __name__ == '__main__':
    main()
