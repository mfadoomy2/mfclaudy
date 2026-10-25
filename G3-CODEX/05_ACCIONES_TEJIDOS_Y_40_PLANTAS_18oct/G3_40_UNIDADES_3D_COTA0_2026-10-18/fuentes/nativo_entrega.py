# -*- coding: utf-8 -*-
import Rhino,scriptcontext as sc,System,os,json,traceback,math
from System.Drawing import Size,Color
from System.Drawing.Imaging import ImageFormat
P=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18'
def log(s):
 with open(os.path.join(P,'verificacion','nativo.log'),'a') as f:f.write(str(s)+'\n')
 Rhino.RhinoApp.WriteLine(str(s))
try:
 files=sorted([os.path.join(P,'modelos_finales',n) for n in os.listdir(os.path.join(P,'modelos_finales')) if n.endswith('_UNIDAD_3D.3dm') and not n.startswith('._')])
 reports=[]
 for path in files:
  file=Rhino.FileIO.File3dm.Read(path);invalid=[];open_solids=[];volume_errors=[]
  for obj in file.Objects:
   g=obj.Geometry
   if not g.IsValid:invalid.append(obj.Attributes.Name)
   if 'borde lavabo' in obj.Attributes.Name or obj.Attributes.Name.startswith('forjado continuo'):
    props=Rhino.Geometry.VolumeMassProperties.Compute(g.ToBrep())
    if props is None or abs(abs(props.Volume)-float(g.GetUserString('ExpectedVolume')))>0.00001:volume_errors.append(obj.Attributes.Name)

   if isinstance(g,Rhino.Geometry.Extrusion) or isinstance(g,Rhino.Geometry.Brep):
    if not g.IsSolid:open_solids.append(obj.Attributes.Name)
  reports.append(dict(file=os.path.basename(path),objects=len(list(file.Objects)),invalid=invalid,open_solids=open_solids,volume_reference="NATIVO_SOLIDOS.json",adjusted_basin_volume_errors=volume_errors))
  log(os.path.basename(path)+' validado')
 with open(os.path.join(P,'verificacion','NATIVO_ENTREGA.json'),'w') as f:json.dump(reports,f,indent=2)
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
  vp.ZoomBoundingBox(bb);doc.Views.Redraw();Rhino.RhinoApp.Wait()
  cap=Rhino.Display.ViewCapture();cap.Width=1900;cap.Height=1400;cap.ScaleScreenItems=False;cap.DrawAxes=False;cap.DrawGrid=False;cap.DrawGridAxes=False;cap.TransparentBackground=False
  bmp=cap.CaptureToBitmap(view)
  if bmp is None:raise Exception('Captura nula '+code)
  bmp.Save(os.path.join(P,'vistas',code+'_'+mode+'.png'),ImageFormat.Png);bmp.Dispose()
 details=sorted([os.path.join(P,'detalles_habitacion',n) for n in os.listdir(os.path.join(P,'detalles_habitacion')) if n.endswith('.3dm') and not n.startswith('._')])
 for path in details:
  for obj in list(doc.Objects):doc.Objects.Delete(obj,True)
  file=Rhino.FileIO.File3dm.Read(path)
  for obj in file.Objects:
   att=obj.Attributes.Duplicate();name=next(l for l in file.Layers if l.Index==att.LayerIndex).Name;li=doc.Layers.FindByFullPath(name,True)
   if li<0:li=doc.Layers.Add(next(l for l in file.Layers if l.Index==att.LayerIndex))
   att.LayerIndex=li;doc.Objects.Add(obj.Geometry,att)
  code=os.path.basename(path).split('_DETALLE')[0];capture(code,'AXON');capture(code,'PLANTA');doc.Modified=False;log('HABITACION_AISLADA '+code)
 # Leave an actual finished unit in the working view; no changes to the user's source model.
 for obj in list(doc.Objects):doc.Objects.Delete(obj,True)
 file=Rhino.FileIO.File3dm.Read(files[0])
 for obj in file.Objects:doc.Objects.Add(obj.Geometry,obj.Attributes.Duplicate())
 capture('N01A','AXON');doc.Modified=False
 Rhino.RhinoDoc.Open(files[0])
 log('ENTREGA_NATIVA_LISTA')
except Exception:
 log(traceback.format_exc())
