#! python3
# G3 · megaestructura: cortes horizontales completos a +1,20 m sobre cada nivel de tableros
import Rhino, json, traceback
from Rhino.Geometry import Point3d, Vector3d, Plane
PATH = '/Users/adam/Downloads/MEGAESTRUCTURA_MACARRA/modelo/MEGAESTRUCTURA_MACARRA.3dm'
OUT = '/Volumes/T7/G3_RHINO/out/mega/NIVELES_MEGA.json'
LEVELS = json.load(open('/Volumes/T7/G3_RHINO/mega_niveles.json'))
res = {'levels': LEVELS, 'cuts': [], 'errors': []}
try:
    f = Rhino.FileIO.File3dm.Read(PATH)
    layers = {la.Index: la.Name for la in f.AllLayers}
    objs = [(layers.get(ob.Attributes.LayerIndex, '?'), ob.Attributes.Name or '', ob.Geometry, ob.Geometry.GetBoundingBox(True)) for ob in f.Objects if isinstance(ob.Geometry, Rhino.Geometry.Mesh)]
    for L in LEVELS:
        z = L['cut']; pl = Plane(Point3d(0, 0, z), Vector3d.ZAxis)
        for la, nm, g, bb in objs:
            if bb.Min.Z > z or bb.Max.Z < z: continue
            cv = Rhino.Geometry.Intersect.Intersection.MeshPlane(g, pl)
            if cv:
                res['cuts'].append({'level': L['id'], 'layer': la, 'name': nm, 'polys': [[[round(p.X, 4), round(p.Y, 4)] for p in c] for c in cv]})
except Exception:
    res['errors'].append(traceback.format_exc())
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print('G3 s13', len(res['cuts']), res['errors'][:1])
