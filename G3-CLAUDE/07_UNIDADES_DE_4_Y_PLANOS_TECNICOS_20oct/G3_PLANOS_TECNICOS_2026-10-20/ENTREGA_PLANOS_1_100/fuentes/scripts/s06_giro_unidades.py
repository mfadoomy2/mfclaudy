#! python3
# G3 · unidades V01-V03: se gira cada unidad +90 grados sobre su propio centro para que quede recta,
# con la entrada y las habitaciones hacia la calle (poniente, -X, igual que E02) y los baños al fondo (levante).
import Rhino, json, System, math, traceback
from Rhino.Geometry import Point3d, Vector3d, Transform, BoundingBox
OUT = '/Volumes/T7/G3_RHINO/out/'
log = {'unidades': {}, 'errores': []}
try:
    doc = None
    for d in Rhino.RhinoDoc.OpenDocuments():
        if (d.Name or '').startswith('TRES_UNIDADES_COMPACTADAS'):
            doc = d
    if doc is None:
        raise Exception('documento de unidades no abierto')
    def top(la):
        cur = la
        while cur.ParentLayerId != System.Guid.Empty:
            cur = doc.Layers.FindId(cur.ParentLayerId)
        return cur.Name
    groups = {}
    for o in doc.Objects:
        t = top(doc.Layers[o.Attributes.LayerIndex])
        if t.startswith('V0'):
            groups.setdefault(t, []).append(o)
    for name, objs in sorted(groups.items()):
        # centro: caja de los suelos (capa 00_SUELO) o de todo
        bb = BoundingBox.Empty
        for o in objs:
            if doc.Layers[o.Attributes.LayerIndex].Name.endswith('00_SUELO'):
                bb.Union(o.Geometry.GetBoundingBox(True))
        if not bb.IsValid:
            for o in objs: bb.Union(o.Geometry.GetBoundingBox(True))
        c = Point3d(bb.Center.X, bb.Center.Y, 0)
        T = Transform.Rotation(math.radians(90), Vector3d.ZAxis, c)
        n = 0
        for o in objs:
            if doc.Objects.Transform(o.Id, T, True) != System.Guid.Empty:
                n += 1
        log['unidades'][name] = {'objetos': n, 'centro': [round(c.X, 3), round(c.Y, 3)], 'caja_suelo_antes': [round(bb.Min.X, 3), round(bb.Min.Y, 3), round(bb.Max.X, 3), round(bb.Max.Y, 3)]}
    doc.Views.Redraw()
    log['guardado'] = bool(doc.Save()); log['ruta'] = doc.Path
    for v in doc.Views:
        vp = v.ActiveViewport
        if vp.Name == 'Top':
            vp.ZoomExtents(); v.Redraw()
            bmp = v.CaptureToBitmap(System.Drawing.Size(2400, 1000))
            if bmp: bmp.Save(OUT + 's06_top.png')
except Exception:
    log['errores'].append(traceback.format_exc())
json.dump(log, open(OUT + 's06.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('G3 s06', log)
