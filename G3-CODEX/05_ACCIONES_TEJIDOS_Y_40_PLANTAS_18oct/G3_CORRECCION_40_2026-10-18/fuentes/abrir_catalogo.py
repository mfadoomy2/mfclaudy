# -*- coding: utf-8 -*-
import Rhino,scriptcontext as sc,System,os,json,traceback
from System.Drawing.Imaging import ImageFormat
P=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def log(s):
 with open(os.path.join(P,'verificacion','catalogo_nativo.log'),'a') as f:f.write(str(s)+'\n')
 Rhino.RhinoApp.WriteLine(str(s))
try:
 result=Rhino.RhinoDoc.Open(os.path.join(P,'CATALOGO_40_CORREGIDAS_COTA0.3dm'));doc=result[0] if isinstance(result,tuple) else result;sc.doc=doc
 view=doc.Views.ActiveView;view.Maximized=True;vp=view.ActiveViewport;vp.DisplayMode=Rhino.Display.DisplayModeDescription.FindByName('G3_MATERIALES_REVISION')
 bounds={};whole=Rhino.Geometry.BoundingBox.Empty
 for ob in doc.Objects:
  if not doc.Layers[ob.Attributes.LayerIndex].IsVisible:continue
  b=ob.Geometry.GetBoundingBox(True);whole.Union(b);code=ob.Attributes.GetUserString('Unidad')
  if code:
   if code not in bounds:bounds[code]=Rhino.Geometry.BoundingBox.Empty
   bb=bounds[code];bb.Union(b);bounds[code]=bb
 def frame(bb,plan=False):
  c=bb.Center;d=bb.Diagonal.Length;vp.ChangeToParallelProjection(True)
  eye=Rhino.Geometry.Point3d(c.X,c.Y,c.Z+d*2) if plan else Rhino.Geometry.Point3d(c.X+d*.55,c.Y-d*.8,c.Z+d*.9)
  vp.SetCameraLocations(c,eye)
  try:vp.CameraUp=Rhino.Geometry.Vector3d.YAxis if plan else Rhino.Geometry.Vector3d.ZAxis
  except:pass
  vp.ZoomBoundingBox(bb);vi=Rhino.DocObjects.ViewportInfo(vp);hx=max(abs((pt-c)*vp.CameraX) for pt in bb.GetCorners());hy=max(abs((pt-c)*vp.CameraY) for pt in bb.GetCorners());h=max(hy,hx/(1800.0/1600))*1.12;fr=vi.GetFrustum();vi.SetFrustum(-h*1800/1600,h*1800/1600,-h,h,fr[-2],fr[-1]);vp.SetViewProjection(vi,True)
 def capture(name):
  doc.Views.Redraw();Rhino.RhinoApp.Wait();cap=Rhino.Display.ViewCapture();cap.Width=1800;cap.Height=1600;cap.DrawAxes=False;cap.DrawGrid=False;cap.DrawGridAxes=False;bmp=cap.CaptureToBitmap(view);bmp.Save(os.path.join(P,'vistas',name+'.png'),ImageFormat.Png);bmp.Dispose()
 frame(whole,True);doc.NamedViews.Add('00_TODAS_COTA_0',vp.Id);capture('CATALOGO_TODAS_COTA_0')
 for code,bb in sorted(bounds.items()):frame(bb);doc.NamedViews.Add(code,vp.Id)
 frame(bounds['N01A']);capture('CATALOGO_N01A');Rhino.RhinoApp.RunScript('_Save',False)
 with open(os.path.join(P,'verificacion','CATALOGO_NATIVO.json'),'w') as f:json.dump(dict(units=len(bounds),views=doc.NamedViews.Count,objects=len(list(doc.Objects)),native_saved=True),f,indent=2)
 log('CATALOGO_CORREGIDO_ABIERTO_40_UNIDADES_41_VISTAS')
except:log(traceback.format_exc())
