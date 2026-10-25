import Rhino as R, os, time
root=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_RADICAL_RHINO_V3_2026-10-16'
d=R.RhinoDoc.ActiveDoc;mp=R.Geometry.MeshingParameters.FastRenderMesh;n=0
for o in d.Objects:
 if isinstance(o.Geometry,R.Geometry.Brep):
  o.CreateMeshes(R.Geometry.MeshType.Render,mp,False);n+=1
 if n%3000==0 and n>0:
  with open(os.path.join(root,'verificacion','mallas_render.txt'),'w') as f:f.write(str(n))
d.Views.Redraw()
execfile(os.path.join(root,'fuentes','capturar_revision.py'))
print('MALLAS_LISTAS',n)
