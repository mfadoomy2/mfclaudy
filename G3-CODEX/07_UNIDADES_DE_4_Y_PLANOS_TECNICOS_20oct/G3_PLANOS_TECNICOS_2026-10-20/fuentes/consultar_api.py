import Rhino,System
p='/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/verificacion/API_RHINO.txt'
with open(p,'w') as f:
 for tp in [Rhino.DocObjects.Font,Rhino.DocObjects.DimensionStyle,Rhino.Geometry.TextEntity]:
  t=System.Type.GetType(tp.__module__+'.'+tp.__name__+', RhinoCommon')
  f.write(str(tp)+'\n'+str(tp.__doc__)+'\n')
  if t:
   for c in t.GetConstructors():f.write(str(c)+'\n')
