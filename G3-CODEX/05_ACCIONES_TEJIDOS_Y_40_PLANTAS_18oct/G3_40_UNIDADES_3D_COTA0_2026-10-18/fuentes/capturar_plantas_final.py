# -*- coding: utf-8 -*-
import Rhino,scriptcontext as sc,System,os,json,traceback,math
from System.Drawing import Size,Color
from System.Drawing.Imaging import ImageFormat
P=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18'
def log(s):
 with open(os.path.join(P,'verificacion','nativo.log'),'a') as f:f.write(str(s)+'\n')
 Rhino.RhinoApp.WriteLine(str(s))
try:
 files=sorted([os.path.join(P,'ENTREGA','modelos',n) for n in os.listdir(os.path.join(P,'ENTREGA','modelos')) if n.endswith('_UNIDAD_3D.3dm') and not n.startswith('._')])
 # Mac opens a separate document window, preserving the user's edited source document.
 result=Rhino.RhinoDoc.Open(os.path.join(P,'verificacion','SESION_REVISION.3dm'));doc=result[0] if isinstance(result,tuple) else result
 if doc is None:raise Exception('No se abre documento de revision')
 sc.doc=doc
 view=doc.Views.Find('Perspective',False) or doc.Views.ActiveView;view.Maximized=True
 shaded=Rhino.Display.DisplayModeDescription.FindByName('G3_MATERIALES_REVISION')
 if shaded is None:
  mode_id=Rhino.Display.DisplayModeDescription.CopyDisplayMode(Rhino.Display.DisplayModeDescription.FindByName('Shaded').Id,'G3_MATERIALES_REVISION');shaded=Rhino.Display.DisplayModeDescription.GetDisplayMode(mode_id)
 shaded.DisplayAttributes.ShowSurfaceEdges=False;shaded.DisplayAttributes.ShowIsoCurves=False;shaded.DisplayAttributes.SetFill(Color.FromArgb(248,246,240));Rhino.Display.DisplayModeDescription.UpdateDisplayMode(shaded)
 view.ActiveViewport.DisplayMode=shaded
 doc.Views.Redraw()
 def capture(code,mode):
  vp=view.ActiveViewport;bb=Rhino.Geometry.BoundingBox.Empty
  for obj in doc.Objects:
   if not obj.IsHidden and doc.Layers[obj.Attributes.LayerIndex].IsVisible:bb.Union(obj.Geometry.GetBoundingBox(True))
  c=bb.Center;diag=bb.Diagonal.Length
  vp.ChangeToParallelProjection(True)
  if mode=='PLANTA':
   eye=Rhino.Geometry.Point3d(c.X,c.Y,c.Z+diag*2);up=Rhino.Geometry.Vector3d.YAxis
  else:
   eye=Rhino.Geometry.Point3d(c.X+diag*.7,c.Y-diag*.85,c.Z+diag*1.15);up=Rhino.Geometry.Vector3d.ZAxis
  vp.SetCameraLocations(c,eye)
  try:vp.CameraUp=up
  except:pass
  vp.ZoomBoundingBox(bb);vp.Magnify(.60,True);doc.Views.Redraw();Rhino.RhinoApp.Wait()
  cap=Rhino.Display.ViewCapture();cap.Width=1900;cap.Height=1400;cap.ScaleScreenItems=False;cap.DrawAxes=False;cap.DrawGrid=False;cap.DrawGridAxes=False;cap.TransparentBackground=False
  bmp=cap.CaptureToBitmap(view)
  if bmp is None:raise Exception('Captura nula '+code)
  bmp.Save(os.path.join(P,'ENTREGA','vistas',code+'_'+mode+'.png'),ImageFormat.Png);bmp.Dispose()
 for idx,path in enumerate(files):
  if True:
   for obj in list(doc.Objects):doc.Objects.Delete(obj,True)
   file=Rhino.FileIO.File3dm.Read(path)
   for obj in file.Objects:
    att=obj.Attributes.Duplicate();doc.Objects.Add(obj.Geometry,att)
  code=os.path.basename(path).split('_')[0]
  capture(code,'PLANTA')
  doc.Modified=False
  log('CAPTURA_CORREGIDA '+code)
 log('40_PLANTAS_SIN_RECORTES')
except Exception:
 log(traceback.format_exc())
