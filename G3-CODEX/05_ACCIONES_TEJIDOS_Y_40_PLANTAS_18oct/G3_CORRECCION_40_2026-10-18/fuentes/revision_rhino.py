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
 # This dedicated scratch document is generated for the correction and can be replaced safely.
 f=Rhino.FileIO.File3dm();f.Settings.ModelUnitSystem=Rhino.UnitSystem.Meters
 scratch=os.path.join(P,'verificacion','SESION_CORRECCION_'+System.Guid.NewGuid().ToString('N')+'.3dm');f.Write(scratch,8)
 result=Rhino.RhinoDoc.Open(scratch);doc=result[0] if isinstance(result,tuple) else result
 if doc is None:raise Exception('No se abre revision')
 sc.doc=doc;view=doc.Views.ActiveView
 mode=Rhino.Display.DisplayModeDescription.FindByName('G3_MATERIALES_REVISION')
 if mode is None:
  mid=Rhino.Display.DisplayModeDescription.CopyDisplayMode(Rhino.Display.DisplayModeDescription.FindByName('Shaded').Id,'G3_MATERIALES_REVISION');mode=Rhino.Display.DisplayModeDescription.GetDisplayMode(mid)
 mode.DisplayAttributes.ShowSurfaceEdges=False;mode.DisplayAttributes.ShowIsoCurves=False;mode.DisplayAttributes.SetFill(Color.FromArgb(248,246,240));Rhino.Display.DisplayModeDescription.UpdateDisplayMode(mode)
 view.ActiveViewport.DisplayMode=mode
 reports=[]
 files=sorted(os.path.join(P,'modelos',n) for n in os.listdir(os.path.join(P,'modelos')) if n.endswith('_CORREGIDA.3dm') and not n.startswith('._'))
 detail=os.path.join(P,'HABITACION_CORREGIDA.3dm')
 if os.path.exists(detail):files.append(detail)
 for path in files:
  for obj in list(doc.Objects):doc.Objects.Delete(obj,True)
  file=Rhino.FileIO.File3dm.Read(path);lm={};mm={}
  for layer in file.Layers:
   li=doc.Layers.FindByFullPath(layer.Name,True)
   if li<0:li=doc.Layers.Add(layer)
   doc.Layers[li].IsVisible=layer.IsVisible;lm[layer.Index]=li
  for mi,mat in enumerate(file.Materials):mm[mi]=doc.Materials.Add(mat)
  bad=[];openparts=[];vol=[];count=0
  for ob in file.Objects:
   g=ob.Geometry;a=ob.Attributes.Duplicate();a.LayerIndex=lm[a.LayerIndex]
   if a.MaterialIndex in mm:a.MaterialIndex=mm[a.MaterialIndex]
   if not g.IsValid:bad.append(a.Name)
   if isinstance(g,(Rhino.Geometry.Extrusion,Rhino.Geometry.Brep)) and not g.IsSolid:openparts.append(a.Name)
   ex=g.GetUserString('ExpectedVolume')
   if ex:
    vp=Rhino.Geometry.VolumeMassProperties.Compute(g)
    if vp is None or abs(abs(vp.Volume)-float(ex))>max(0.00001,float(ex)*.0001):vol.append(a.Name)
   doc.Objects.Add(g,a);count+=1
  code=os.path.basename(path).split('_')[0]
  reports.append(dict(code=code,objects=count,invalid=bad,open_solids=openparts,volume_errors=vol))
  pv=capture(doc,code,'PLANTA');av=capture(doc,code,'AXON');doc.Modified=False
  pv.Name='PLANTA';av.Name='AXONOMETRIA'
  try:pv.DisplayModeId=Rhino.Display.DisplayModeDescription.FindByName('Shaded').Id;av.DisplayModeId=pv.DisplayModeId
  except:pass
  file.Views.Clear();initial=Rhino.DocObjects.ViewInfo(view.ActiveViewport);initial.Name='Perspective'
  try:initial.DisplayModeId=Rhino.Display.DisplayModeDescription.FindByName('Shaded').Id
  except:pass
  file.Views.Add(initial);file.NamedViews.Clear();file.NamedViews.Add(pv);file.NamedViews.Add(av)
  ready=os.path.join(P,'modelos_listos')
  if not os.path.exists(ready):os.makedirs(ready)
  if not file.Write(os.path.join(ready,os.path.basename(path)),8):raise Exception('No se guarda modelo con vistas '+code)
  with open(os.path.join(P,'verificacion','RHINO_NATIVO.json'),'w') as f:json.dump(reports,f,indent=2)
  log('REVISADA '+code+' invalidos='+str(len(bad))+' abiertos='+str(len(openparts))+' volumen='+str(len(vol)))
 doc.Modified=False
 log('REVISION_TERMINADA '+str(len(files)))
except:log(traceback.format_exc())
