import rhino3dm as r3
from shapely.geometry import box, Polygon, MultiPolygon, LineString, Point
from shapely.ops import unary_union
from geo import *

m = r3.File3dm()
m.Settings.ModelUnitSystem = r3.UnitSystem.Meters
m.Settings.ModelAbsoluteTolerance = 0.001

def layer(name, rgb, parent=None):
    L = r3.Layer(); L.Name = name; L.Color = (*rgb, 255)
    if parent is not None:
        L.ParentLayerId = m.Layers.FindIndex(parent).Id
    return m.Layers.Add(L)

root = layer('N19B_REDUCIDA', (40, 40, 40))
LY = {}
for nm, col in [('00_PARCELA', (20, 20, 20)), ('01_ZOCALO_PB_indicativo', (255, 196, 0)),
                ('02_NUCLEO_MASTIL', (230, 30, 60)), ('03_FORJADOS', (150, 150, 150)),
                ('04_MUROS_RACIMOS', (60, 60, 60)), ('05_HABITACIONES_suelo', (0, 170, 140)),
                ('06_COMUN_suelo', (255, 120, 0)), ('07_BANOS_COCINA', (0, 120, 255)),
                ('08_MOBILIARIO', (120, 90, 200)), ('09_PLATAFORMA', (255, 60, 150)),
                ('10_ESTRUCTURA_indicativa', (230, 30, 60)), ('11_ROTULOS', (0, 0, 0)),
                ('12_VIDRIO', (90, 200, 255))]:
    LY[nm] = layer(nm, col, 0)

def attrs(lname, name=None):
    a = r3.ObjectAttributes(); a.LayerIndex = LY[lname]
    if name: a.Name = name
    return a

def pieces(g):
    if g.is_empty: return []
    if g.geom_type == 'Polygon': return [g]
    return [p for p in getattr(g, 'geoms', []) if p.geom_type == 'Polygon' and p.area > 1e-5]

def split_holes(poly):
    """Corta polígonos con agujeros en franjas verticales para que cada parte sea extruible."""
    out = []
    for p in pieces(poly):
        if len(p.interiors) == 0:
            out.append(p); continue
        xs = sorted(set(round(x, 4) for ring in [p.exterior] + list(p.interiors) for x, _ in ring.coords))
        for a, b in zip(xs[:-1], xs[1:]):
            if b - a < 1e-4: continue
            for q in pieces(p.intersection(box(a, -1e4, b, 1e4))):
                out += split_holes(q) if len(q.interiors) else [q]
    return out

def extrude(poly, z0, h, lname, name=None):
    n = 0
    for p in split_holes(poly):
        p = p.simplify(0.0005)
        if p.area < 1e-5: continue
        pts = [r3.Point3d(x, y, Z0 + z0) for x, y in p.exterior.coords]
        crv = r3.Polyline(pts).ToNurbsCurve()
        ex = r3.Extrusion.Create(crv, -h, True)  # rhino3dm: altura negativa = hacia +Z en curvas antihorarias
        if ex is None: continue
        bb = ex.GetBoundingBox()
        if bb.Min.Z < Z0 + z0 - 1e-3:
            ex = r3.Extrusion.Create(crv, h, True)
        m.Objects.AddExtrusion(ex, attrs(lname, name)); n += 1
    return n

def curve(g, z, lname, name=None):
    for p in pieces(g) if g.geom_type in ('Polygon', 'MultiPolygon') else []:
        pts = [r3.Point3d(x, y, Z0 + z) for x, y in p.exterior.coords]
        m.Objects.AddCurve(r3.Polyline(pts).ToNurbsCurve(), attrs(lname, name))
    if g.geom_type == 'LineString':
        pts = [r3.Point3d(x, y, Z0 + z) for x, y in g.coords]
        m.Objects.AddCurve(r3.Polyline(pts).ToNurbsCurve(), attrs(lname, name))

def dot(txt, x, y, z):
    m.Objects.AddTextDot(txt, r3.Point3d(x, y, Z0 + z), attrs('11_ROTULOS'))

# parcela (en la cota de la plaza)
curve(PARCELA, 0, '00_PARCELA', 'Catastro 0134911VK4703C · 651 m²')

pt = planta_tipo()

def cluster_3d(cl, z, tag):
    curve(cl['footprint'], z, '04_MUROS_RACIMOS')
    extrude(cl['footprint'], z - 0.30, 0.30, '03_FORJADOS', f'forjado {tag}')
    walls, cuts = walls_of(cl)
    solid = cl['footprint'].difference(unary_union([r['rect'] for r in cl['rooms'].values()] +
                                                   [b['rect'] for b in cl['baths'].values()] + [cl['field']]))
    wcut = unary_union([w.buffer(0.35, cap_style=2) for w in cl['windows']])
    extrude(solid.difference(cuts), z, 0.60, '04_MUROS_RACIMOS')                    # 0 - 0,60 (antepecho)
    extrude(solid.difference(cuts).difference(wcut), z + 0.60, 1.50, '04_MUROS_RACIMOS')
    extrude(solid.difference(wcut), z + 2.10, 0.30, '04_MUROS_RACIMOS')            # dinteles de puerta
    extrude(solid, z + 2.40, 0.40, '04_MUROS_RACIMOS')                            # 2,40 - 2,80
    for w in cl['windows']:
        extrude(w.buffer(0.02, cap_style=2), z + 0.60, 1.80, '12_VIDRIO')
    for k, r in cl['rooms'].items():
        curve(r['rect'], z + 0.005, '05_HABITACIONES_suelo', k)
        extrude(r['bed'], z, 0.45, '08_MOBILIARIO', 'cama 1250x2000')
        extrude(r['desk'], z + 0.72, 0.03, '08_MOBILIARIO', 'tablero plegable 1600x700')
        extrude(r['ward'], z, 2.30, '08_MOBILIARIO', 'armario curvo')
        c = r['rect'].centroid; dot(f'{tag}·{k} {r["rect"].area:.1f} m²', c.x, c.y, z + 1.2)
    for k, b in cl['baths'].items():
        curve(b['rect'], z + 0.005, '07_BANOS_COCINA', k)
        extrude(b['shower'], z, 0.02, '07_BANOS_COCINA', 'plato enrasado')
        extrude(b['wc'], z, 0.42, '07_BANOS_COCINA', 'inodoro')
        extrude(b['lav'], z + 0.75, 0.10, '07_BANOS_COCINA', 'lavabo')
    f = cl['furn']
    curve(cl['field'], z + 0.005, '06_COMUN_suelo', 'suelo común')
    extrude(f['counter'], z, 0.90, '07_BANOS_COCINA', 'cocina lineal')
    extrude(f['fridge'], z, 1.90, '07_BANOS_COCINA', 'frigorífico')
    extrude(f['table'], z + 0.72, 0.04, '08_MOBILIARIO', 'mesa común 1600x800')
    for s in f['stools']: extrude(s, z, 0.45, '08_MOBILIARIO', 'taburete')
    extrude(f['sofa'], z, 0.42, '08_MOBILIARIO', 'sofá'); extrude(f['sofa_back'], z + 0.42, 0.38, '08_MOBILIARIO')
    extrude(f['low'], z, 0.35, '08_MOBILIARIO')
    extrude(f['coats'], z, 2.30, '08_MOBILIARIO', 'armario de entrada')
    extrude(f['worktop'], z + 0.72, 0.04, '08_MOBILIARIO', 'mesa de trabajo por turnos')
    for s in cl['shaft']: extrude(s, z, 2.80, '07_BANOS_COCINA', 'patinillo')
    c = cl['field'].centroid; dot(f'{tag} común {cl["field"].area:.1f} m²', c.x, c.y, z + 1.6)

for i, z in enumerate(NIVELES):
    cluster_3d(pt['c1'], z, f'P{i+1}·C1')
    cluster_3d(pt['c2'], z, f'P{i+1}·C2')
    plat = pt['plat']
    extrude(plat, z - 0.25, 0.25, '09_PLATAFORMA', f'plataforma P{i+1}')
    # barandilla 1,10 m (CTE DB SUA 1, desnivel > 6 m) en los bordes libres
    edge = plat.exterior.difference(unary_union([pt['core'], pt['c1']['footprint'], pt['c2']['footprint']]).buffer(0.05))
    for e in getattr(edge, 'geoms', [edge]):
        if e.length > 0.2:
            pts = [r3.Point3d(x, y, Z0 + z + 1.10) for x, y in e.coords]
            m.Objects.AddCurve(r3.Polyline(pts).ToNurbsCurve(), attrs('09_PLATAFORMA', 'barandilla h=1,10'))
    dot(f'+{z:.2f}', XCORE + 2.6, YS + CORE_D + 2.0, z + 0.5)
# cubierta
extrude(pt['c1']['footprint'], NIVELES[-1] + 2.80, 0.30, '03_FORJADOS', 'cubierta C1 +23,50')
extrude(pt['c2']['footprint'], NIVELES[-1] + 2.80, 0.30, '03_FORJADOS', 'cubierta C2 +23,50')
extrude(pt['plat'], CUBIERTA - 0.25, 0.25, '09_PLATAFORMA', 'plataforma cubierta')

# núcleo-mástil: PB a +26,10
TOP = CUBIERTA + 2.60
core_walls = pt['core'].difference(pt['core_in'])
lift_walls = pt['lift'].difference(pt['lift'].buffer(-0.15, join_style=2))
xin0, yin0, xin1, yin1 = pt['core_in'].bounds
door_stair = box(xin0 + 0.15, yin1 - 0.05, xin0 + 1.05, yin1 + 0.40)
door_lift = box(pt['cabin'].bounds[0], yin1 - 0.05, pt['cabin'].bounds[2], yin1 + 0.40)
levels_all = [0.0] + NIVELES + [CUBIERTA]
zz = 0.0
for zl in levels_all:
    pass
# muros del núcleo con huecos en cada nivel servido
prev = 0.0
for zl in levels_all:
    if zl - prev > 0.01:
        extrude(core_walls, prev, zl - prev, '02_NUCLEO_MASTIL')
    extrude(core_walls.difference(door_stair).difference(door_lift), zl, 2.10, '02_NUCLEO_MASTIL')
    prev = zl + 2.10
extrude(core_walls, prev, TOP - prev, '02_NUCLEO_MASTIL')
extrude(lift_walls, 0, TOP, '02_NUCLEO_MASTIL', 'hueco ascensor')
extrude(pt['riser'], 0, TOP, '07_BANOS_COCINA', 'patinillo general')
# escalera: dos tramos por planta (9 contrahuellas de ~0,17 m)
fa, fb = pt['flights']
for a, b in zip(levels_all[:-1], levels_all[1:]):
    h = b - a; n = int(round(h / 0.175)); n += n % 2; rise = h / n; half = n // 2
    tread = (fa.bounds[3] - fa.bounds[1]) / half
    for s in range(half):
        y0 = fa.bounds[3] - (s + 1) * tread   # tramo A sube hacia el sur
        extrude(box(fa.bounds[0], y0, fa.bounds[2], y0 + tread), a + s * rise, rise, '02_NUCLEO_MASTIL')
    mid = a + half * rise
    extrude(box(xin0, yin0, xin0 + 2.30, fa.bounds[1]), mid - 0.20, 0.20, '02_NUCLEO_MASTIL', 'meseta')
    for s in range(half):
        y0 = fb.bounds[1] + s * tread         # tramo B sube hacia el norte
        extrude(box(fb.bounds[0], y0, fb.bounds[2], y0 + tread), mid + s * rise, rise, '02_NUCLEO_MASTIL')
    extrude(box(xin0, fa.bounds[3], xin0 + 2.30, yin1), b - 0.20, 0.20, '02_NUCLEO_MASTIL', 'meseta de planta')
dot('núcleo-mástil: escalera protegida + ascensor + bajantes', XCORE + 2.6, YS + 2.6, TOP + 0.5)

# zócalo PB (indicativo): bajo los dos racimos; el paso bajo la plataforma queda libre (pasaje al patio de fondo)
for k in ('c1', 'c2'):
    extrude(pt[k]['footprint'], 0, ZOCALO_H, '01_ZOCALO_PB_indicativo', 'zócalo social PB (indicativo)')
extrude(unary_union([pt['c1']['footprint'], pt['core'], pt['c2']['footprint']]), ZOCALO_H - 0.30, 0.30,
        '03_FORJADOS', 'forjado de la plaza alta +4,50')
# estructura indicativa del nivel abierto +4,50 / +8,00: soportes en esquinas y centros de lado
for k in ('c1', 'c2'):
    x0, y0, x1, y1 = pt[k]['footprint'].bounds
    for x in (x0 + 0.2, (x0 + x1) / 2, x1 - 0.2):
        for y in (y0 + 0.2, (y0 + y1) / 2, y1 - 0.2):
            if x == (x0 + x1) / 2 and y == (y0 + y1) / 2: continue
            extrude(box(x - 0.15, y - 0.15, x + 0.15, y + 0.15), ZOCALO_H, NIVELES[0] - 0.30 - ZOCALO_H,
                    '10_ESTRUCTURA_indicativa', 'soporte (sin dimensionar)')
dot('PB zócalo +0,00 · plaza alta abierta +4,50', XC1 + 2, YS + 2, ZOCALO_H + 0.5)

out = 'G3_N19B_REDUCIDA_PARCELA_2026-10-18.3dm'
m.Write(out, 8)
print('objetos', len(m.Objects))
