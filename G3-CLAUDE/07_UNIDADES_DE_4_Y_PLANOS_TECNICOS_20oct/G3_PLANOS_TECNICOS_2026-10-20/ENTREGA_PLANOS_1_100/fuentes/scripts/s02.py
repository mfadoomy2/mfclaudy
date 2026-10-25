#! python3
import Rhino, json, System
OUT='/Volumes/T7/G3_RHINO/out/'
res=[]
for d in Rhino.RhinoDoc.OpenDocuments():
    if not d.Name.startswith(('E02_RECTA','TRES_UNIDADES_COMPACTADAS')): continue
    pb=None
    for o in d.Objects:
        if d.Layers[o.Attributes.LayerIndex].Name=='91_PARCELA': pb=o.Geometry.GetBoundingBox(True)
    allb=Rhino.Geometry.BoundingBox.Empty
    far=[]
    for o in d.Objects:
        b=o.Geometry.GetBoundingBox(True)
        c=b.Center
        la=d.Layers[o.Attributes.LayerIndex].FullPath
        if pb is not None:
            if c.X<pb.Min.X-5 or c.X>pb.Max.X+5 or c.Y<pb.Min.Y-5 or c.Y>pb.Max.Y+5:
                far.append([o.Attributes.Name,la,[round(c.X,2),round(c.Y,2),round(c.Z,2)],str(o.Id)])
    res.append({'doc':d.Name,'far':far[:200],'nfar':len(far)})
json.dump(res,open(OUT+'s02.json','w'),indent=1)
print('G3 s02 ok',[ (r['doc'],r['nfar']) for r in res])
