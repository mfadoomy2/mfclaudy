"""Mide el vacio real de la plaza: para un abanico de direcciones desde el origen,
distancia al edificio mas cercano. Localiza la Real Casa de Correos."""
import json
import math
import os

ctx = json.load(open(os.path.join(os.path.dirname(__file__), 'contexto_sol.json'), encoding='utf-8'))


def seg_ray(px, py, dx, dy, ax, ay, bx, by):
    # interseccion rayo (p+t*d) con segmento a-b; devuelve t o None
    ex, ey = bx - ax, by - ay
    den = dx * ey - dy * ex
    if abs(den) < 1e-12:
        return None
    t = ((ax - px) * ey - (ay - py) * ex) / den
    s = ((ax - px) * dy - (ay - py) * dx) / den
    if t > 0 and 0 <= s <= 1:
        return t
    return None


for ang in range(0, 360, 15):
    dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    best = None
    for b in ctx['buildings']:
        pts = b['pts']
        for i in range(len(pts) - 1):
            t = seg_ray(0, 0, dx, dy, *pts[i], *pts[i + 1])
            if t and (best is None or t < best):
                best = t
    print('az %3d (E=0,N=90): %s m' % (ang, '%.0f' % best if best else '—'))

print()
for b in ctx['buildings']:
    n = b['name']
    if n and ('Correos' in n or 'Presidencia' in n or 'Comunidad' in n):
        xs = [p[0] for p in b['pts']]
        ys = [p[1] for p in b['pts']]
        print('EDIFICIO:', n, ' bbox X %.0f..%.0f Y %.0f..%.0f' % (min(xs), max(xs), min(ys), max(ys)))
