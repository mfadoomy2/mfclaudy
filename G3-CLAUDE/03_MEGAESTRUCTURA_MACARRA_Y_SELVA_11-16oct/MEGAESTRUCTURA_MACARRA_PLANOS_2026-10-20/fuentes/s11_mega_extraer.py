#! python3
# G3 · megaestructura macarra: extracción métrica para plantas (cortes a +1,20 de cada estancia, piezas, contornos, ejes y recorridos)
import Rhino, System, json, math, traceback
from Rhino.Geometry import Point3d, Vector3d, Plane, BoundingBox
PATH = '/Users/adam/Downloads/MEGAESTRUCTURA_MACARRA/modelo/MEGAESTRUCTURA_MACARRA.3dm'
VER = '/Volumes/T7/G3_RHINO/out/mega/verificacion.json'
OUT = '/Volumes/T7/G3_RHINO/out/mega/EXTRACCION_MEGA_PLANTAS.json'
res = {'errors': [], 'cuts': [], 'decks': [], 'pieces': [], 'outlines': [], 'curves': [], 'trunk_cuts': []}
def P(pl): return [[round(p.X, 4), round(p.Y, 4)] for p in pl]
try:
    ver = json.load(open(VER, encoding='utf-8'))
    S = ver['spaces']
    f = Rhino.FileIO.File3dm.Read(PATH)
    layers = {la.Index: la.Name for la in f.AllLayers}
    objs = []
    for ob in f.Objects:
        g = ob.Geometry; la = layers.get(ob.Attributes.LayerIndex, '?'); nm = ob.Attributes.Name or ''
        if isinstance(g, Rhino.Geometry.PolylineCurve):
            ok, pl = g.TryGetPolyline()
            res['curves'].append({'layer': la, 'name': nm, 'pts': [[round(p.X, 4), round(p.Y, 4), round(p.Z, 4)] for p in pl]}); continue
        if not isinstance(g, Rhino.Geometry.Mesh): continue
        objs.append((la, nm, g, g.GetBoundingBox(True)))
    # 1. cortes a +1,20 sobre cada estancia
    for s in S:
        cx, cy, cz = s['c']; R = s['r'] * 1.45 + 3.0; z = cz + 1.20
        pl = Plane(Point3d(0, 0, z), Vector3d.ZAxis)
        for la, nm, g, bb in objs:
            if la == '06_MEGATRONCOS': continue
            if bb.Min.Z > z or bb.Max.Z < z: continue
            if bb.Max.X < cx - R or bb.Min.X > cx + R or bb.Max.Y < cy - R or bb.Min.Y > cy + R: continue
            cv = Rhino.Geometry.Intersect.Intersection.MeshPlane(g, pl)
            if cv:
                res['cuts'].append({'i': s['id'], 'z': z, 'layer': la, 'name': nm, 'polys': [P(c) for c in cv]})
        # troncos al mismo nivel (sin recorte: se recorta al dibujar)
        for la, nm, g, bb in objs:
            if la != '06_MEGATRONCOS' or bb.Min.Z > z or bb.Max.Z < z: continue
            cv = Rhino.Geometry.Intersect.Intersection.MeshPlane(g, pl)
            if cv: res['trunk_cuts'].append({'i': s['id'], 'z': z, 'name': nm, 'polys': [P(c) for c in cv]})
    # 2. tableros: contorno exacto a media altura del tablero (0,27 de canto)
    for la, nm, g, bb in objs:
        if la != '01_SUELOS_HABITABLES': continue
        i = int(nm[1:3]); z = S[i]['c'][2] - .135
        cv = Rhino.Geometry.Intersect.Intersection.MeshPlane(g, Plane(Point3d(0, 0, z), Vector3d.ZAxis))
        res['decks'].append({'i': i, 'name': nm, 'top': bb.Max.Z, 'bottom': bb.Min.Z, 'polys': [P(c) for c in cv] if cv else []})
    # 3. piezas sueltas (peldaños, descansillos, mobiliario, máquinas, depósitos, agua, luz): una por componente desconectado
    for la, nm, g, bb in objs:
        if la not in ('03_ESCALERAS_PELDANOS', '04_DESCANSILLOS', '19_MOBILIARIO', '16_MAQUINARIA', '13_DEPOSITOS_CRISTAL', '14_AGUA', '18_LUZ'): continue
        parts = g.SplitDisjointPieces() or [g]
        for m in parts:
            b = m.GetBoundingBox(True)
            pts = [Point3d(v.X, v.Y, 0) for v in m.Vertices]
            hull = []
            try:
                pc = Rhino.Geometry.PointCloud(pts)
                # contorno de la pieza en planta: GetOutlines exacto de la malla
                ol = m.GetOutlines(Plane.WorldXY)
                hull = [P(o) for o in ol] if ol else []
            except Exception as e:
                res['errors'].append(nm + ' ' + str(e))
            res['pieces'].append({'layer': la, 'name': nm, 'z': [round(b.Min.Z, 4), round(b.Max.Z, 4)], 'outline': hull})
    # 4. contornos en planta de lo que queda por encima o por debajo (velas, galerías, células, anclajes, conductos)
    for la, nm, g, bb in objs:
        if la not in ('10_MEMBRANAS', '12_CONDUCTOS_CIAN', '08_CELULAS_PERFORADAS'): continue
        ol = g.GetOutlines(Plane.WorldXY)
        res['outlines'].append({'layer': la, 'name': nm, 'z': [round(bb.Min.Z, 4), round(bb.Max.Z, 4)], 'polys': [P(o) for o in ol] if ol else []})
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
    print('G3 s11', len(res['cuts']), len(res['decks']), len(res['pieces']), len(res['outlines']), len(res['curves']), res['errors'][:2])
except Exception:
    res['errors'].append(traceback.format_exc())
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
    print(traceback.format_exc())
