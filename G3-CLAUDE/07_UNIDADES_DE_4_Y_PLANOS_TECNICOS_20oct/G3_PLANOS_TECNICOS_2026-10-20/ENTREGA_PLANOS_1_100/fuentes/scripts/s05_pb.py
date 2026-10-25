#! python3
# G3 · relleno de la planta baja en E02_RECTA (documento abierto). Idempotente: borra lo que creó antes.
import Rhino, json, System, traceback
from Rhino.Geometry import Point3d, Vector3d, Plane, Circle, Cylinder, Brep, PolylineCurve, LineCurve, BoundingBox
OUT = '/Volumes/T7/G3_RHINO/out/'
DATA = '/Volumes/T7/G3_RHINO/pb_items.json'
TAG = 'g3_pb'
log = {'creados': 0, 'borrados': 0, 'errores': [], 'choques': [], 'capas_nuevas': []}
try:
    doc = None
    for d in Rhino.RhinoDoc.OpenDocuments():
        if (d.Name or '').startswith('E02_RECTA'):
            doc = d
    if doc is None:
        raise Exception('E02_RECTA no está abierto')
    tol = doc.ModelAbsoluteTolerance
    # 1. borrar la versión anterior de este relleno
    old = [o.Id for o in doc.Objects if o.Attributes.GetUserString(TAG)]
    for i in old:
        doc.Objects.Delete(i, True)
    log['borrados'] = len(old)
    # 2. objetos existentes para el control de choques
    skip = ('90_CONTEXTO', '91_PARCELA', '00_SUELO', '16_PERSONAS')
    exist = []
    for o in doc.Objects:
        la = doc.Layers[o.Attributes.LayerIndex]
        if la.Name in skip:
            continue
        exist.append((o.Attributes.Name or '', la.Name, o.Geometry.GetBoundingBox(True), o.Geometry))
    items = json.load(open(DATA, encoding='utf-8'))
    for it in items:
        li = doc.Layers.FindByFullPath(it['layer'], -1)
        if li < 0:
            la = doc.Layers.FindName(it['layer'])
            li = la.Index if la else -1
        if li < 0:
            li = doc.Layers.Add(it['layer'], System.Drawing.Color.Gray)
            log['capas_nuevas'].append(it['layer'])
        z0, h = it['z0'], it['h']
        solids = []
        if 'circle' in it:
            c = Circle(Plane(Point3d(it['circle'][0], it['circle'][1], z0), Vector3d.ZAxis), it['r'])
            solids.append(Cylinder(c, h).ToBrep(True, True))
        else:
            for ring in it['rings']:
                crv = PolylineCurve([Point3d(x, y, z0) for x, y in ring])
                bb = Brep.CreatePlanarBreps(crv, tol)
                if not bb:
                    log['errores'].append(it['name'] + ' / sin cara'); continue
                f = bb[0].Faces[0]
                s = f.CreateExtrusion(LineCurve(Point3d(ring[0][0], ring[0][1], z0), Point3d(ring[0][0], ring[0][1], z0 + h)), True)
                if s is None or not s.IsValid:
                    log['errores'].append(it['name'] + ' / extrusión'); continue
                if s.IsSolid and s.SolidOrientation == Rhino.Geometry.BrepSolidOrientation.Inward:
                    s.Flip()
                solids.append(s)
        for s in solids:
            at = Rhino.DocObjects.ObjectAttributes()
            at.LayerIndex = li
            at.Name = it['name']
            at.SetUserString(TAG, 'relleno planta baja 2026-10-20')
            doc.Objects.AddBrep(s, at)
            log['creados'] += 1
            # choques reales: intersección de sólidos con lo existente cuyo bbox se cruza
            b = s.GetBoundingBox(True)
            for name, lay, eb, g in exist:
                if eb.Min.X < b.Max.X - .005 and eb.Max.X > b.Min.X + .005 and eb.Min.Y < b.Max.Y - .005 and eb.Max.Y > b.Min.Y + .005 and eb.Min.Z < b.Max.Z - .005 and eb.Max.Z > b.Min.Z + .005:
                    gb = g.ToBrep() if isinstance(g, Rhino.Geometry.Extrusion) else g
                    hit = False
                    if isinstance(gb, Brep):
                        ok, cv, pt = Rhino.Geometry.Intersect.Intersection.BrepBrep(s, gb, tol)
                        hit = ok and cv is not None and len(cv) > 0
                    elif isinstance(gb, Rhino.Geometry.Mesh):
                        hit = True
                    if hit:
                        log['choques'].append([it['name'], lay, name, round(eb.Min.Z, 2), round(eb.Max.Z, 2)])
    doc.Views.Redraw()
    # 3. guardar
    saved = False
    try:
        saved = doc.Save()
    except Exception as e:
        log['errores'].append('Save: ' + str(e))
    if not saved:
        opt = Rhino.FileIO.FileWriteOptions()
        saved = doc.WriteFile(doc.Path, opt)
    log['guardado'] = bool(saved); log['ruta'] = doc.Path
    # 4. capturas
    for v in doc.Views:
        vp = v.ActiveViewport
        if vp.Name == 'Top':
            vp.ZoomBoundingBox(BoundingBox(Point3d(11, -9, 0), Point3d(63, 14, 5)))
            v.Redraw()
            bmp = v.CaptureToBitmap(System.Drawing.Size(2400, 1100))
            if bmp: bmp.Save(OUT + 's05_top.png')
        if vp.Name == 'Perspective':
            vp.ZoomBoundingBox(BoundingBox(Point3d(11, -9, 0), Point3d(63, 14, 5)))
            v.Redraw()
            bmp = v.CaptureToBitmap(System.Drawing.Size(2400, 1300))
            if bmp: bmp.Save(OUT + 's05_persp.png')
except Exception:
    log['errores'].append(traceback.format_exc())
json.dump(log, open(OUT + 's05.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('G3 s05', log['creados'], log['errores'][:2])
