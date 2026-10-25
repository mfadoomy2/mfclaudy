#! python3
import Rhino, json, System
OUT='/Volumes/T7/G3_RHINO/out/'
paths={'E02':'/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/E02_RECTA_HABITACIONES_A_LA_CALLE.3dm',
       'UNI':'/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/TRES_UNIDADES_COMPACTADAS_GIRO90.3dm'}
rep={}
for k,p in paths.items():
    res=Rhino.RhinoDoc.Open(p)
    doc=res[0] if isinstance(res,tuple) else res
    if doc is None:
        rep[k]='no se abre'; continue
    bad=[o.Attributes.Name for o in doc.Objects if not o.Geometry.IsValid]
    rep[k]={'objects':doc.Objects.Count,'invalid':len(bad),'invalid_names':bad[:20]}
    for v in doc.Views:
        if v.ActiveViewport.Name=='Perspective':
            v.ActiveViewport.ZoomExtents(); v.Redraw()
            bmp=v.CaptureToBitmap(System.Drawing.Size(1800,1000))
            if bmp: bmp.Save(OUT+'s01_'+k+'_persp.png')
        if v.ActiveViewport.Name=='Top':
            v.ActiveViewport.ZoomExtents(); v.Redraw()
            bmp=v.CaptureToBitmap(System.Drawing.Size(1800,1000))
            if bmp: bmp.Save(OUT+'s01_'+k+'_top.png')
json.dump(rep,open(OUT+'s01.json','w'),indent=1)
print('G3 s01 ok',rep)
