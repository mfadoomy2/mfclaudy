import Rhino as R
import scriptcontext as sc
import System.Drawing as SD
import os,json
P='/Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_MATERIALES_ORIGEN_2026-10-18';fixed=[]
for o in list(sc.doc.Objects):
 if not o.Geometry.IsValid and isinstance(o.Geometry,R.Geometry.Brep):
  mm=R.Geometry.Mesh();arr=R.Geometry.Mesh.CreateFromBrep(o.Geometry,R.Geometry.MeshingParameters.QualityRenderMesh)
  for q in arr:mm.Append(q)
  mm.Vertices.CombineIdentical(True,True);mm.Normals.ComputeNormals();mm.Compact()
  if not mm.IsValid:raise Exception('No se pudo reparar '+o.Attributes.Name)
  a=o.Attributes.Duplicate();a.SetUserString('Reparacion','Cerramiento reconstruido como malla nativa por defecto topologico de Brep');sc.doc.Objects.AddMesh(mm,a);sc.doc.Objects.Delete(o.Id,True);fixed.append(a.Name)
visible=[o for o in sc.doc.Objects if not o.IsHidden];bad=[o.Attributes.Name for o in visible if not o.Geometry.IsValid]
if bad:raise Exception(str(bad))
opt=R.FileIO.FileWriteOptions();opt.SuppressDialogBoxes=True
sc.doc.WriteFile(os.path.join(P,'P02_INTERIOR_MATERIALES_000.3dm'),opt)
for l in sc.doc.Layers:
 if l.Name in ['07_CUBIERTA','08_CUBIERTA_LUCERNARIO','06_VIDRIOS','13_CIERRES_SUPERIORES_OCULTAR_CON_CUBIERTA']:l.IsVisible=True;l.CommitChanges()
sc.doc.WriteFile(os.path.join(P,'P02_COMPLETA_MATERIALES_000.3dm'),opt)
for l in sc.doc.Layers:
 if l.Name in ['07_CUBIERTA','08_CUBIERTA_LUCERNARIO','06_VIDRIOS','13_CIERRES_SUPERIORES_OCULTAR_CON_CUBIERTA']:l.IsVisible=False;l.CommitChanges()
sc.doc.Views.Redraw();sc.doc.WriteFile(os.path.join(P,'P02_INTERIOR_MATERIALES_000.3dm'),opt)
bmp=sc.doc.Views.ActiveView.CaptureToBitmap(SD.Size(2200,1700));bmp.Save(os.path.join(P,'RHINO_INTERIOR_FINAL.png'),SD.Imaging.ImageFormat.Png)
with open(os.path.join(P,'NATIVO_FINAL.json'),'w') as f:json.dump({'invalid_visible':bad,'repaired_as_mesh':fixed,'native_saved_both':True},f)
print('REVISION_FINAL_SIN_INVALIDOS')
