import Rhino as R
import scriptcontext as sc
import rhinoscriptsyntax as rs
import System.Drawing as SD
import os,json
P='/Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_MATERIALES_ORIGEN_2026-10-18'
bad=[]
for o in list(sc.doc.Objects):
 if o.IsHidden:continue
 if not o.Geometry.IsValid:
  name=o.Attributes.Name;bad.append(name)
  g=o.Geometry.Duplicate()
  if isinstance(g,R.Geometry.Brep):
   g.Repair(.001)
   if g.IsValid:sc.doc.Objects.Replace(o.Id,g)
visible=[o for o in sc.doc.Objects if not o.IsHidden]
with open(os.path.join(P,'NATIVO_FINAL.json'),'w') as f:json.dump({'bad_before':bad,'bad_after':[o.Attributes.Name for o in visible if not o.Geometry.IsValid]},f)
rs.UnselectAllObjects()
v=sc.doc.Views.ActiveView
sc.doc.Views.Redraw()
opts=R.FileIO.FileWriteOptions();opts.SuppressDialogBoxes=True
sc.doc.WriteFile(os.path.join(P,'P02_INTERIOR_MATERIALES_000.3dm'),opts)
# settled rendered viewport capture
bmp=v.CaptureToBitmap(SD.Size(1800,1500));bmp.Save(os.path.join(P,'RHINO_INTERIOR_FINAL.png'),SD.Imaging.ImageFormat.Png)
print('NATIVO_FINAL_GUARDADO')
