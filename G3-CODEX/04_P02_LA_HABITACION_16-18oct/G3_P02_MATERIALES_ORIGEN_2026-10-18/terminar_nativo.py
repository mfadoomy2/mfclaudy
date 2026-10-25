import Rhino as R
import rhinoscriptsyntax as rs
import scriptcontext as sc
import System.Drawing as SD
import json,os
P='/Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_MATERIALES_ORIGEN_2026-10-18'
# attach native bitmap textures and real-world mapping
for mat in sc.doc.Materials:
 if mat.Name in ['ROBLE','LINO','CORCHO']:
  mat.SetBitmapTexture(os.path.join(P,'texturas',mat.Name+'.png'));mat.CommitChanges()
for ob in list(sc.doc.Objects):
 if ob.IsHidden:continue
 name=ob.Attributes.GetUserString('Material')
 if name in ['ROBLE','LINO','CORCHO']:
  mp=R.Render.TextureMapping.CreateBoxMapping(R.Geometry.Plane.WorldXY,R.Geometry.Interval(-.5,.5),R.Geometry.Interval(-.5,.5),R.Geometry.Interval(0,1),True)
  ob.SetTextureMapping(1,mp)
# native regenerated render meshes
rs.Command('_RefreshShade _All _Enter',False)
rs.UnselectAllObjects()
v=next((q for q in sc.doc.Views if q.ActiveViewport.Name=='01_INTERIOR'),sc.doc.Views.ActiveView)
sc.doc.Views.ActiveView=v
if v:
 
 if not v.Maximized:v.Maximized=True
 v=sc.doc.Views.ActiveView
 v.ActiveViewport.SetCameraLocations(R.Geometry.Point3d(0,0,0),R.Geometry.Point3d(16,-20,24))
 v.ActiveViewport.CameraUp=R.Geometry.Vector3d(0,0,1)
 v.ActiveViewport.ZoomExtents()
 mode=R.Display.DisplayModeDescription.FindByName('Rendered')
 if mode:v.ActiveViewport.DisplayMode=mode
 v.ActiveViewport.ConstructionGridVisible=False;v.ActiveViewport.ConstructionAxesVisible=False
 sc.doc.Views.Redraw()
opt=R.FileIO.FileWriteOptions();opt.SuppressDialogBoxes=True
sc.doc.WriteFile(os.path.join(P,'P02_INTERIOR_MATERIALES_000.3dm'),opt)
# save diagnostic and a native bitmap, no abstract stand-in
visible=[o for o in sc.doc.Objects if not o.IsHidden]
report={'native_objects':len(visible),'invalid':sum(not o.Geometry.IsValid for o in visible),'materials':sc.doc.Materials.Count,'saved':True,'bad_names':[o.Attributes.Name for o in visible if not o.Geometry.IsValid]}
with open(os.path.join(P,'REVISION_NATIVA.json'),'w') as f:json.dump(report,f)
try:
 capture=R.Display.ViewCapture();capture.Width=2000;capture.Height=1600;capture.ScaleScreenItems=False;capture.DrawAxes=False;capture.DrawGrid=False;capture.DrawGridAxes=False
 bmp=capture.CaptureToBitmap(v);bmp.Save(os.path.join(P,'RHINO_INTERIOR.png'),SD.Imaging.ImageFormat.Png)
except Exception as ex:
 with open(os.path.join(P,'captura_error.txt'),'w') as f:f.write(str(ex))
print('P02_MATERIALES_NATIVO_LISTO')
