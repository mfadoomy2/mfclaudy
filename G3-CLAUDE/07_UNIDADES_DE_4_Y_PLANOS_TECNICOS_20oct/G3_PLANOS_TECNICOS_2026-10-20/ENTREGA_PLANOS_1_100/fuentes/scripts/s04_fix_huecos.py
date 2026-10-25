#! python3
# Repara extrusiones cuyo perfil interior quedo desplazado (huecos fuera de la pieza).
import Rhino, json, System
OUT='/Volumes/T7/G3_RHINO/out/'
tol=0.001
rep=[]
for doc in Rhino.RhinoDoc.OpenDocuments():
    if not doc.Name.startswith(('E02_RECTA','TRES_UNIDADES_COMPACTADAS')): continue
    fixed=0
    for o in list(doc.Objects):
        g=o.Geometry
        if not isinstance(g,Rhino.Geometry.Extrusion) or g.ProfileCount<2: continue
        outer=g.Profile3d(0,0.0)
        ob=outer.GetBoundingBox(True)
        amp=Rhino.Geometry.AreaMassProperties.Compute(outer)
        if amp is None: continue
        oc=amp.Centroid
        inners=[]; bad=False
        for k in range(1,g.ProfileCount):
            c=g.Profile3d(k,0.0)
            cb=c.GetBoundingBox(True)
            inside = cb.Min.X>=ob.Min.X-1e-4 and cb.Max.X<=ob.Max.X+1e-4 and cb.Min.Y>=ob.Min.Y-1e-4 and cb.Max.Y<=ob.Max.Y+1e-4
            if not inside:
                bad=True
                a2=Rhino.Geometry.AreaMassProperties.Compute(c)
                cc=a2.Centroid if a2 else cb.Center
                c=c.DuplicateCurve(); c.Translate(Rhino.Geometry.Vector3d(oc.X-cc.X,oc.Y-cc.Y,0))
            inners.append(c)
        if not bad: continue
        h=g.PathStart.DistanceTo(g.PathEnd); up=g.PathEnd-g.PathStart
        breps=Rhino.Geometry.Brep.CreatePlanarBreps([outer]+inners,tol)
        if not breps: continue
        face=breps[0].Faces[0]
        path=Rhino.Geometry.LineCurve(outer.PointAtStart,outer.PointAtStart+up)
        solid=face.CreateExtrusion(path,True)
        if solid is None or not solid.IsValid: continue
        doc.Objects.Replace(o.Id,solid); fixed+=1
    doc.Views.Redraw()
    rep.append([doc.Name,fixed])
json.dump(rep,open(OUT+'s04.json','w'))
print('G3 s04 huecos reparados',rep)
