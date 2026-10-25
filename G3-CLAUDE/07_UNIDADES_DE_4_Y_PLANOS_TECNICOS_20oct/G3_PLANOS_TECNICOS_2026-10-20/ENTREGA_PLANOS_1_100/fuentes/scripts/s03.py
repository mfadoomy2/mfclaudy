#! python3
import Rhino, json, System
OUT='/Volumes/T7/G3_RHINO/out/'
ids=['7030dabc-c448-4b4d-8918-304b0180a831','5cad5fe9-e85c-4797-af04-b06d755ee395','ed0f821c-702c-4273-bb90-bed59cf64f08','edfc4a34-1b4e-424b-b8bb-f93a0c7ab9f6','79a5ae69-3496-414a-9d91-70ba453fbdb2']
doc=[d for d in Rhino.RhinoDoc.OpenDocuments() if d.Name.startswith('E02_RECTA')][0]
out=[]
def pts(c):
    ok,pl=c.TryGetPolyline()
    if ok: return [[round(p.X,3),round(p.Y,3),round(p.Z,3)] for p in pl][:12]
    return [[round(c.PointAt(t).X,3),round(c.PointAt(t).Y,3),round(c.PointAt(t).Z,3)] for t in c.DivideByCount(8,True)]
for i in ids:
    o=doc.Objects.FindId(System.Guid(i)); g=o.Geometry
    it={'name':o.Attributes.Name,'type':g.GetType().Name}
    if isinstance(g,Rhino.Geometry.Extrusion):
        it['path']=[[g.PathStart.X,g.PathStart.Y,g.PathStart.Z],[g.PathEnd.X,g.PathEnd.Y,g.PathEnd.Z]]
        it['profiles']=[pts(g.Profile3d(k,0.0)) for k in range(g.ProfileCount)]
        it['up']=[g.PathTangent.X,g.PathTangent.Y,g.PathTangent.Z]
    b=g.GetBoundingBox(True); it['bbox']=[[b.Min.X,b.Min.Y,b.Min.Z],[b.Max.X,b.Max.Y,b.Max.Z]]
    out.append(it)
json.dump(out,open(OUT+'s03.json','w'),indent=1)
print('G3 s03 ok')
