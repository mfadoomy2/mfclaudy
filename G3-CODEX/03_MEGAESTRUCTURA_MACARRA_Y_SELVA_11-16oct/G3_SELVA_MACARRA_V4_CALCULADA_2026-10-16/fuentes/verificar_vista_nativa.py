# -*- coding: utf-8 -*-
import Rhino as R, System, os, json
G=R.Geometry;P=G.Point3d;V=G.Vector3d
root=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16'
d=R.RhinoDoc.ActiveDoc
n=0
mp=G.MeshingParameters.FastRenderMesh
for o in d.Objects:
 if isinstance(o.Geometry,G.Brep):
  o.CreateMeshes(G.MeshType.Render,mp,True);n+=1
 a=o.Attributes.Duplicate()
 a.SetUserString('Estado','Anteproyecto con predimensionado preliminar; no certificado')
 d.Objects.ModifyAttributes(o.Id,a,True)
view=d.Views.ActiveView;view.Maximized=True;vp=view.ActiveViewport
vp.SetCameraLocations(P(35,0,12),P(86,-94,52));vp.CameraUp=V.ZAxis;vp.ChangeToParallelProjection(True)
vp.ZoomBoundingBox(G.BoundingBox(P(12,-8,-1),P(60,13,27)))
vp.DisplayMode=R.Display.DisplayModeDescription.FindByName('Shaded')
view.Redraw()
c=R.Display.ViewCapture();c.Width=2600;c.Height=1800;c.ScaleScreenItems=True;c.DrawAxes=False;c.DrawGrid=False;c.DrawGridAxes=False;c.TransparentBackground=False
b=c.CaptureToBitmap(view);b.Save(os.path.join(root,'vistas','08_RHINO_NATIVO.png'),System.Drawing.Imaging.ImageFormat.Png)
d.WriteFile(os.path.join(root,'modelos','SELVA_MACARRA_V4_FINAL.3dm'),R.FileIO.FileWriteOptions())
with open(os.path.join(root,'verificacion','captura_nativa.json'),'w') as f:json.dump({'file':d.Name,'objects':d.Objects.Count,'mode':vp.DisplayMode.EnglishName,'meshed':n,'capture':'08_RHINO_NATIVO.png'},f)
print('VISTA_NATIVA_VERIFICADA')
