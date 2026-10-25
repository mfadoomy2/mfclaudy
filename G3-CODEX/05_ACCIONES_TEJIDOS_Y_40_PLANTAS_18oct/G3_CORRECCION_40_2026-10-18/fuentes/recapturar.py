# -*- coding: utf-8 -*-
import Rhino,scriptcontext as sc,System,os,json,traceback
from System.Drawing import Color
from System.Drawing.Imaging import ImageFormat
P=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG=os.path.join(P,'verificacion','rhino.log')
def log(s):
 with open(LOG,'a') as f:f.write(str(s)+'\n')
 Rhino.RhinoApp.WriteLine(str(s))
def capture(doc,code,mode):
 view=doc.Views.ActiveView;view.Maximized=True;vp=view.ActiveViewport
 vp.DisplayMode=Rhino.Display.DisplayModeDescription.FindByName('G3_MATERIALES_REVISION')
 temporary=[]
 if mode=='PLANTA':
  for ob in list(doc.Objects):
   if doc.Layers[ob.Attributes.LayerIndex].Name.startswith('02_') and ob.Geometry.GetBoundingBox(True).Min.Z>=2.19 and not ob.IsHidden:
    doc.Objects.Hide(ob.Id,True);temporary.append(ob.Id)
 bb=Rhino.Geometry.BoundingBox.Empty
 for ob in doc.Objects:
  if not ob.IsHidden and doc.Layers[ob.Attributes.LayerIndex].IsVisible:bb.Union(ob.Geometry.GetBoundingBox(True))
 c=bb.Center;diag=bb.Diagonal.Length;vp.ChangeToParallelProjection(True)
 if mode=='PLANTA':eye=Rhino.Geometry.Point3d(c.X,c.Y,c.Z+diag*2);up=Rhino.Geometry.Vector3d.YAxis
 else:eye=Rhino.Geometry.Point3d(c.X+diag*.55,c.Y-diag*.8,c.Z+diag*.9);up=Rhino.Geometry.Vector3d.ZAxis
 vp.SetCameraLocations(c,eye)
 try:vp.CameraUp=up
 except:pass
 vp.ZoomBoundingBox(bb)
 vi=Rhino.DocObjects.ViewportInfo(vp)
 halfx=max(abs((pt-c)*vp.CameraX) for pt in bb.GetCorners())
 halfy=max(abs((pt-c)*vp.CameraY) for pt in bb.GetCorners())
 halfh=max(halfy,halfx/(1800.0/1600.0))*1.12
 fr=vi.GetFrustum()
 vi.SetFrustum(-halfh*1800.0/1600.0,halfh*1800.0/1600.0,-halfh,halfh,fr[-2],fr[-1])
 vp.SetViewProjection(vi,True);doc.Views.Redraw();Rhino.RhinoApp.Wait()
 cap=Rhino.Display.ViewCapture();cap.Width=1800;cap.Height=1600;cap.ScaleScreenItems=False;cap.DrawAxes=False;cap.DrawGrid=False;cap.DrawGridAxes=False;cap.TransparentBackground=False
 bmp=cap.CaptureToBitmap(view)
 if bmp is None:raise Exception('No bitmap')
 bmp.Save(os.path.join(P,'vistas',code+'_'+mode+'.png'),ImageFormat.Png);bmp.Dispose()
 for oid in temporary:doc.Objects.Show(oid,True)
 doc.Views.Redraw()
 return Rhino.DocObjects.ViewInfo(vp)
try:
 f=Rhino.FileIO.File3dm();f.Settings.ModelUnitSystem=Rhino.UnitSystem.Meters
 scratch=os.path.join(P,'verificacion','VISTAS_'+System.Guid.NewGuid().ToString('N')+'.3dm');f.Write(scratch,8)
 result=Rhino.RhinoDoc.Open(scratch);doc=result[0] if isinstance(result,tuple) else result;sc.doc=doc
 files=sorted(os.path.join(P,'modelos_listos',n) for n in os.listdir(os.path.join(P,'modelos_listos')) if n.endswith('.3dm') and not n.startswith('._'))
 for path in files:
  for ob in list(doc.Objects):doc.Objects.Delete(ob,True)
  f=Rhino.FileIO.File3dm.Read(path);lm={};mm={}
  for l in f.Layers:
   li=doc.Layers.FindByFullPath(l.Name,True)
   if li<0:li=doc.Layers.Add(l)
   doc.Layers[li].IsVisible=l.IsVisible;lm[l.Index]=li
  for mi,mat in enumerate(f.Materials):mm[mi]=doc.Materials.Add(mat)
  for ob in f.Objects:
   a=ob.Attributes.Duplicate();a.LayerIndex=lm[a.LayerIndex]
   if a.MaterialIndex in mm:a.MaterialIndex=mm[a.MaterialIndex]
   doc.Objects.Add(ob.Geometry,a)
  code=os.path.basename(path).split('_')[0]
  capture(doc,code,'PLANTA');capture(doc,code,'AXON');doc.Modified=False;log('VISTA_FINAL '+code)
 log('VISTAS_FINALES_41')
except:log(traceback.format_exc())
