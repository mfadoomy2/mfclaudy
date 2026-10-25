import Rhino as R,json,os
m=R.Display.DisplayModeDescription.FindByName('Rendered');a=m.DisplayAttributes;vals={}
for n in dir(a):
 if any(t in n for t in ['Shad','Surf','Mesh','Draw','Fill','Back']):
  try:vals[str(n)]=str(getattr(a,n))
  except:pass
with open(u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/verificacion/modo.json','w') as f:json.dump(vals,f)
