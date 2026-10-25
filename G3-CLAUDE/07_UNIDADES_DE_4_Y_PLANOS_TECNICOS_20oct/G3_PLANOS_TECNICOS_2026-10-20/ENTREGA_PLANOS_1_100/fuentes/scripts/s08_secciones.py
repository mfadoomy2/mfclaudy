#! python3
# G3 · secciones verticales exactas desde Rhino: corte (BrepPlane / MeshPlane) + proyección visible (HiddenLineDrawing) de lo que queda detrás del plano.
import Rhino, System, json, math, traceback
from Rhino.Geometry import Point3d, Vector3d, Plane, Transform, BoundingBox
DEF = '/Volumes/T7/G3_RHINO/secciones_def.json'
OUT = '/Volumes/T7/G3_RHINO/out/SECCIONES_2026-10-20_RHINO.json'
SKIP = ('90_CONTEXTO', '91_PARCELA', '16_PERSONAS')
res = {'sections': [], 'errors': []}

def pl(curve):
    ok, pp = curve.TryGetPolyline()
    if ok: return [[p.X, p.Y, p.Z] for p in pp]
    L = curve.GetLength(); n = max(2, min(8000, int(math.ceil(L / .015))))
    return [[curve.PointAt(t).X, curve.PointAt(t).Y, curve.PointAt(t).Z] for t in curve.DivideByCount(n, True)]

def top(doc, la):
    cur = la
    while cur.ParentLayerId != System.Guid.Empty:
        cur = doc.Layers.FindId(cur.ParentLayerId)
    return cur.Name

try:
    defs = json.load(open(DEF, encoding='utf-8'))
    docs = {d.Name: d for d in Rhino.RhinoDoc.OpenDocuments()}
    for sd in defs:
        doc = next((d for k, d in docs.items() if (k or '').startswith(sd['doc'])), None)
        if doc is None:
            res['errors'].append('sin documento ' + sd['doc']); continue
        tol = doc.ModelAbsoluteTolerance
        O = Point3d(*sd['origin']); n = Vector3d(*sd['normal']); xd = Vector3d(*sd['xdir'])
        cut = Plane(O, n)
        keep = Plane(O, -n)   # Brep.Trim conserva lo opuesto a la normal del cortador: lo que queda detrás del plano de corte
        out = {'def': sd, 'cut': [], 'beyond_bbox_uv': None, 'hld': [], 'hld_bbox': None, 'objects_beyond': 0}
        hp = Rhino.Geometry.HiddenLineDrawingParameters()
        hp.AbsoluteTolerance = tol; hp.IncludeTangentEdges = False; hp.IncludeHiddenCurves = False
        vi = Rhino.DocObjects.ViewportInfo()
        vi.ChangeToParallelProjection(True)
        vi.SetCameraLocation(O - n * 300.0); vi.SetCameraDirection(n); vi.SetCameraUp(Vector3d.ZAxis)
        vi.SetFrustum(-60, 60, -30, 30, 1, 2000)
        try: vi.SetScreenPort(0, 2400, 0, 1200, 0, 0)
        except Exception: pass
        hp.SetViewport(vi)
        uvb = [1e9, 1e9, -1e9, -1e9]
        for o in doc.Objects:
            la = doc.Layers[o.Attributes.LayerIndex]
            if la.Name in SKIP: continue
            if sd['doc'].startswith('TRES') and not top(doc, la).startswith(sd['code'] + '__'): continue
            g = o.Geometry
            if isinstance(g, (Rhino.Geometry.Curve, Rhino.Geometry.TextDot, Rhino.Geometry.AnnotationBase, Rhino.Geometry.Point)): continue
            bb = g.GetBoundingBox(True)
            corners = bb.GetCorners()
            d = [n * (Vector3d(c) - Vector3d(O)) for c in corners]
            dmin, dmax = min(d), max(d)
            if dmax < -1e-4: continue          # todo delante del plano: no se ve
            name = o.Attributes.Name or ''; info = {'name': name, 'layer': la.Name, 'id': str(o.Id)}
            brep = g.ToBrep() if isinstance(g, Rhino.Geometry.Extrusion) else (g if isinstance(g, Rhino.Geometry.Brep) else None)
            mesh = g if isinstance(g, Rhino.Geometry.Mesh) else None
            # 1. corte
            if dmin < 0 < dmax:
                curves = []
                if brep is not None:
                    ok, cv, pts = Rhino.Geometry.Intersect.Intersection.BrepPlane(brep, cut, tol)
                    if ok and cv:
                        curves = [pl(c) for c in Rhino.Geometry.Curve.JoinCurves(cv, tol * 2)]
                elif mesh is not None:
                    for pp in Rhino.Geometry.Intersect.Intersection.MeshPlane(mesh, cut) or []:
                        curves.append([[p.X, p.Y, p.Z] for p in pp])
                if curves:
                    out['cut'].append(dict(info, curves=curves, z=[bb.Min.Z, bb.Max.Z]))
            # 2. proyección de lo que queda detrás
            geo = None
            if brep is not None:
                if dmin < 0 < dmax:
                    parts = brep.Trim(keep, tol)
                    geo = list(parts) if parts else []
                else:
                    geo = [brep]
            elif mesh is not None:
                if dmin < 0 < dmax:
                    parts = mesh.Split(cut) or []
                    geo = [m for m in parts if n * (Vector3d(m.GetBoundingBox(True).Center) - Vector3d(O)) > 0]
                else:
                    geo = [mesh]
            for gg in geo or []:
                hp.AddGeometry(gg, Transform.Identity, str(o.Id))
                b2 = gg.GetBoundingBox(True)
                for c in b2.GetCorners():
                    u = xd * (Vector3d(c) - Vector3d(O)); v = c.Z
                    uvb = [min(uvb[0], u), min(uvb[1], v), max(uvb[2], u), max(uvb[3], v)]
                out['objects_beyond'] += 1
        out['beyond_bbox_uv'] = uvb
        hld = Rhino.Geometry.HiddenLineDrawing.Compute(hp, True)
        hb = [1e9, 1e9, -1e9, -1e9]
        if hld is not None:
            for seg in hld.Segments:
                if seg.SegmentVisibility != Rhino.Geometry.HiddenLineDrawingSegment.Visibility.Visible: continue
                c = seg.CurveGeometry
                if c is None: continue
                c = c.DuplicateCurve()
                pp = pl(c)
                for p in pp:
                    hb = [min(hb[0], p[0]), min(hb[1], p[1]), max(hb[2], p[0]), max(hb[3], p[1])]
                src = ''
                try:
                    src = str(seg.ParentCurve.SourceObject.Tag)
                except Exception: pass
                try: sil = str(seg.ParentCurve.SilhouetteType)
                except Exception: sil = ''
                out['hld'].append({'pts': [[round(p[0], 5), round(p[1], 5), round(p[2], 5)] for p in pp], 'src': src, 'sil': sil})
        out['hld_bbox'] = hb
        res['sections'].append(out)
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
    print('G3 s08', [(s['def']['code'] + s['def']['id'], len(s['cut']), len(s['hld'])) for s in res['sections']], res['errors'][:3])
except Exception:
    res['errors'].append(traceback.format_exc())
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
    print(traceback.format_exc())
