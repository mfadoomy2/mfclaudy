#! python3
# G3 · extracción métrica (misma lógica que extraer_revision.py de la revisión anterior, en Python 3)
import Rhino, System, json, os, math, traceback
M = '/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/'
OUT = '/Volumes/T7/G3_RHINO/out/EXTRACCION_2026-10-20_RHINO.json'

def poly(curve):
    ok, pp = curve.TryGetPolyline()
    if ok: return [[p.X, p.Y, p.Z] for p in pp]
    length = curve.GetLength()
    count = max(2, min(16000, int(math.ceil(length / .015))))
    ts = curve.DivideByCount(count, True)
    return [[curve.PointAt(t).X, curve.PointAt(t).Y, curve.PointAt(t).Z] for t in ts]

def loops_face(face):
    return [{'outer': loop.LoopType == Rhino.Geometry.BrepLoopType.Outer, 'points': poly(loop.To3dCurve())} for loop in face.Loops]

def extract(path, code, level):
    f = Rhino.FileIO.File3dm.Read(path)
    out = {'source': path, 'code': code, 'floor_level': level, 'cut_level': level + 1.20, 'units': str(f.Settings.ModelUnitSystem), 'objects': [], 'errors': []}
    layers = {la.Index: la for la in f.AllLayers}
    byid = {la.Id: la for la in f.AllLayers}
    for ob in f.Objects:
        g = ob.Geometry; a = ob.Attributes; la = layers.get(a.LayerIndex)
        if la is None: continue
        parent = []; cur = la
        while cur is not None:
            parent.insert(0, str(cur.Name))
            if cur.ParentLayerId == System.Guid.Empty: break
            cur = byid.get(cur.ParentLayerId)
        if isinstance(g, (Rhino.Geometry.Curve, Rhino.Geometry.TextDot, Rhino.Geometry.AnnotationBase)): continue
        bb = g.GetBoundingBox(True)
        item = {'id': str(a.ObjectId), 'name': str(a.Name or ''), 'layer': str(la.Name), 'parents': parent, 'type': str(g.GetType().Name),
                'bbox': [[bb.Min.X, bb.Min.Y, bb.Min.Z], [bb.Max.X, bb.Max.Y, bb.Max.Z]], 'sections': [], 'profiles': [], 'caps': []}
        try:
            brep = None
            if isinstance(g, Rhino.Geometry.Extrusion):
                for k in range(g.ProfileCount):
                    item['profiles'].append(poly(g.Profile3d(k, 0.0)))
                brep = g.ToBrep()
            elif isinstance(g, Rhino.Geometry.Brep): brep = g
            if brep is not None:
                if not item['profiles']:
                    for face in brep.Faces:
                        uu = face.Domain(0).Mid; vv = face.Domain(1).Mid
                        if abs(face.NormalAt(uu, vv).Z) > .9999:
                            item['caps'].append(loops_face(face))
                if bb.Min.Z < level + 1.20 + .001 and bb.Max.Z > level + 1.20 - .001:
                    ok, curves, points = Rhino.Geometry.Intersect.Intersection.BrepPlane(brep, Rhino.Geometry.Plane(Rhino.Geometry.Point3d(0, 0, level + 1.20), Rhino.Geometry.Vector3d.ZAxis), .001)
                    if ok and curves:
                        for cv in Rhino.Geometry.Curve.JoinCurves(curves, .001): item['sections'].append(poly(cv))
            elif isinstance(g, Rhino.Geometry.Mesh):
                if bb.Min.Z < level + 1.20 and bb.Max.Z > level + 1.20:
                    for pp in Rhino.Geometry.Intersect.Intersection.MeshPlane(g, Rhino.Geometry.Plane(Rhino.Geometry.Point3d(0, 0, level + 1.20), Rhino.Geometry.Vector3d.ZAxis)) or []:
                        item['sections'].append([[p.X, p.Y, p.Z] for p in pp])
                if la.Name in ['19_SOPORTE_PB', '21_NUCLEO_VERTICAL', '09_MEMBRANAS', '18_LUCERNARIOS']:
                    for pp in g.GetOutlines(Rhino.Geometry.Plane.WorldXY) or []: item['profiles'].append([[p.X, p.Y, p.Z] for p in pp])
        except Exception as e:
            out['errors'].append({'name': item['name'], 'error': str(e)})
        out['objects'].append(item)
    return out

try:
    data = [extract(M + 'TRES_UNIDADES_COMPACTADAS_GIRO90.3dm', 'TRES', 0),
            extract(M + 'E02_RECTA_HABITACIONES_A_LA_CALLE.3dm', 'E02', 4.2),
            extract(M + 'E02_RECTA_HABITACIONES_A_LA_CALLE.3dm', 'E02_PB', 0)]
    json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
    print('G3 s07 extraccion', [len(d['objects']) for d in data])
except Exception:
    open('/Volumes/T7/G3_RHINO/out/s07_error.txt', 'w').write(traceback.format_exc())
    print(traceback.format_exc())
