import Rhino,json,os
D=Rhino.RhinoDoc.ActiveDoc
out=[]
for o in D.Objects:
 g=o.Geometry
 if isinstance(g,Rhino.Geometry.TextEntity):
  b=g.GetBoundingBox(True)
  out.append({'text':g.PlainText,'height':g.TextHeight,'font':g.Font.EnglishFamilyName,'bbox':[[b.Min.X,b.Min.Y],[b.Max.X,b.Max.Y]],'valid':g.IsValid})
with open('/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/verificacion/TEXTOS_NATIVOS.json','w') as f:json.dump(out,f,ensure_ascii=True)
