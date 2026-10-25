# -*- coding: utf-8 -*-
import Rhino,scriptcontext as sc,System,os,json,traceback
from System.Drawing.Imaging import ImageFormat
P=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18'
E=os.path.join(P,'ENTREGA')
def log(s):
 with open(os.path.join(P,'verificacion','catalogo_nativo.log'),'a') as f:f.write(str(s)+'\n')
 Rhino.RhinoApp.WriteLine(str(s))
try:
 result=Rhino.RhinoDoc.Open(os.path.join(E,'CATALOGO_40_UNIDADES_COTA0.3dm'));doc=result[0] if isinstance(result,tuple) else result;sc.doc=doc
 view=doc.Views.Find('Perspective',False) or doc.Views.ActiveView;view.Maximized=True;vp=view.ActiveViewport;vp.DisplayMode=Rhino.Display.DisplayModeDescription.FindByName('G3_MATERIALES_REVISION')
 bounds={};allbox=Rhino.Geometry.BoundingBox.Empty
 for obj in doc.Objects:
  if not doc.Layers[obj.Attributes.LayerIndex].IsVisible:continue
  code=obj.Attributes.GetUserString('Unidad')
  bb=obj.Geometry.GetBoundingBox(True);allbox.Union(bb)
  if code:
   if code not in bounds:bounds[code]=Rhino.Geometry.BoundingBox.Empty
   b=bounds[code];b.Union(bb);bounds[code]=b
 def position(bb):
  c=bb.Center;d=bb.Diagonal.Length;vp.ChangeToParallelProjection(True);vp.SetCameraLocations(c,Rhino.Geometry.Point3d(c.X+d*.7,c.Y-d*.85,c.Z+d*1.15));vp.ZoomBoundingBox(bb)
 def capture(name):
  doc.Views.Redraw();Rhino.RhinoApp.Wait();cap=Rhino.Display.ViewCapture();cap.Width=2300;cap.Height=1700;cap.DrawAxes=False;cap.DrawGrid=False;cap.DrawGridAxes=False;bmp=cap.CaptureToBitmap(view);bmp.Save(os.path.join(E,'vistas',name+'.png'),ImageFormat.Png);bmp.Dispose()
 position(allbox);doc.NamedViews.Add('00_TODAS_A_COTA_0',vp.Id);capture('CATALOGO_TODAS_COTA_0')
 for code,bb in sorted(bounds.items()):position(bb);doc.NamedViews.Add(code,vp.Id)
 position(bounds['N01A']);capture('CATALOGO_N01A');doc.Views.Redraw()
 Rhino.RhinoApp.RunScript('_Save',False)
 log('CATALOGO_ABIERTO_40_UNIDADES_41_VISTAS')
 with open(os.path.join(E,'verificacion','CATALOGO_NATIVO.json'),'w') as f:json.dump(dict(units=len(bounds),named_views=doc.NamedViews.Count,objects=len(list(doc.Objects)),finished_floor_z=0,saved_by_native_save=True),f,indent=2)
except Exception:log(traceback.format_exc())
