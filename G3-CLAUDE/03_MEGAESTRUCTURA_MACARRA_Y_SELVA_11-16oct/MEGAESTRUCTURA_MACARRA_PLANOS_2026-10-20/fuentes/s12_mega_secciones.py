#! python3
# G3 · megaestructura: secciones verticales exactas (MeshPlane) + proyección de líneas ocultas de Rhino de lo que queda detrás.
import Rhino, System, json, math, traceback, sys
from Rhino.Geometry import Point3d, Vector3d, Plane, Transform
PATH = '/Users/adam/Downloads/MEGAESTRUCTURA_MACARRA/modelo/MEGAESTRUCTURA_MACARRA.3dm'
OUT = '/Volumes/T7/G3_RHINO/out/mega/SECCIONES_MEGA_%s.json'
DEFS = [
    {'id': 'A', 'origin': [0, 3.0, 0], 'normal': [0, 1, 0], 'xdir': [1, 0, 0], 'label': 'longitudinal por y = +3,00, mirando a norte'},
    {'id': 'B', 'origin': [0.0, 0, 0], 'normal': [1, 0, 0], 'xdir': [0, -1, 0], 'label': 'transversal por x = 0,00, mirando a levante'},
    {'id': 'C', 'origin': [0, -9.0, 0], 'normal': [0, 1, 0], 'xdir': [1, 0, 0], 'label': 'longitudinal por el eje A de la malla, mirando a norte'},
    {'id': 'D', 'origin': [29.0, 0, 0], 'normal': [-1, 0, 0], 'xdir': [0, 1, 0], 'label': 'transversal por el eje 6 de la malla, mirando a poniente'},
]
which = None
try:
    which = open('/Volumes/T7/G3_RHINO/s12_cual.txt').read().strip()
except Exception:
    pass
f = Rhino.FileIO.File3dm.Read(PATH)
layers = {la.Index: la.Name for la in f.AllLayers}
objs = []
for ob in f.Objects:
    g = ob.Geometry
    if isinstance(g, Rhino.Geometry.Mesh):
        objs.append((str(ob.Id), layers.get(ob.Attributes.LayerIndex, '?'), ob.Attributes.Name or '', g, g.GetBoundingBox(True)))
for sd in DEFS:
    if which and sd['id'] not in which: continue
    res = {'def': sd, 'cut': [], 'hld': [], 'idlayer': {}, 'errors': [], 'beyond_bbox_uv': None}
    try:
        O = Point3d(*sd['origin']); n = Vector3d(*sd['normal']); xd = Vector3d(*sd['xdir'])
        cut = Plane(O, n)
        hp = Rhino.Geometry.HiddenLineDrawingParameters()
        hp.AbsoluteTolerance = 0.002; hp.IncludeTangentEdges = False; hp.IncludeHiddenCurves = False
        vi = Rhino.DocObjects.ViewportInfo(); vi.ChangeToParallelProjection(True)
        vi.SetCameraLocation(O - n * 400.0); vi.SetCameraDirection(n); vi.SetCameraUp(Vector3d.ZAxis)
        vi.SetFrustum(-80, 80, -45, 45, 1, 2000)
        hp.SetViewport(vi)
        uvb = [1e9, 1e9, -1e9, -1e9]
        for oid, la, nm, g, bb in objs:
            res['idlayer'][oid] = [la, nm]
            d = [n * (Vector3d(c) - Vector3d(O)) for c in bb.GetCorners()]
            if max(d) < -1e-4: continue
            geo = [g]
            if min(d) < 0 < max(d):
                for pl in Rhino.Geometry.Intersect.Intersection.MeshPlane(g, cut) or []:
                    res['cut'].append({'id': oid, 'layer': la, 'name': nm, 'pts': [[round(p.X, 4), round(p.Y, 4), round(p.Z, 4)] for p in pl]})
                parts = g.Split(cut) or []
                geo = [m for m in parts if n * (Vector3d(m.GetBoundingBox(True).Center) - Vector3d(O)) > 0]
            for m in geo:
                hp.AddGeometry(m, Transform.Identity, oid)
                for c in m.GetBoundingBox(True).GetCorners():
                    u = xd * (Vector3d(c) - Vector3d(O)); uvb = [min(uvb[0], u), min(uvb[1], c.Z), max(uvb[2], u), max(uvb[3], c.Z)]
        res['beyond_bbox_uv'] = uvb
        hld = Rhino.Geometry.HiddenLineDrawing.Compute(hp, True)
        if hld is not None:
            for seg in hld.Segments:
                if seg.SegmentVisibility != Rhino.Geometry.HiddenLineDrawingSegment.Visibility.Visible: continue
                c = seg.CurveGeometry
                if c is None: continue
                ok, pl = c.TryGetPolyline()
                if ok: pts = [[round(p.X, 4), round(p.Y, 4)] for p in pl]
                else:
                    L = c.GetLength(); k = max(2, min(400, int(L / .05)))
                    pts = [[round(c.PointAt(t).X, 4), round(c.PointAt(t).Y, 4)] for t in c.DivideByCount(k, True)]
                try: src = str(seg.ParentCurve.SourceObject.Tag)
                except Exception: src = ''
                try: sil = str(seg.ParentCurve.SilhouetteType)
                except Exception: sil = ''
                res['hld'].append([pts, src, sil])
    except Exception:
        res['errors'].append(traceback.format_exc())
    json.dump(res, open(OUT % sd['id'], 'w', encoding='utf-8'), ensure_ascii=False)
    print('G3 s12', sd['id'], len(res['cut']), len(res['hld']), res['errors'][:1])
