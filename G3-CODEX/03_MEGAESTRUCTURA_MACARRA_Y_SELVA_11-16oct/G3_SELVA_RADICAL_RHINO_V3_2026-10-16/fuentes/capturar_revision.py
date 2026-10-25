# -*- coding: utf-8 -*-
import Rhino as R, System, os, json
G=R.Geometry;P=G.Point3d;V=G.Vector3d
root=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_RADICAL_RHINO_V3_2026-10-16'
d=R.RhinoDoc.ActiveDoc;view=d.Views.ActiveView;view.Maximized=True;vp=view.ActiveViewport
vp.SetCameraLocations(P(35,0,12),P(86,-94,62));vp.CameraUp=V.ZAxis;vp.ChangeToParallelProjection(True)
vp.ZoomBoundingBox(G.BoundingBox(P(12,-8,-1),P(59,13,27)))
vp.DisplayMode=R.Display.DisplayModeDescription.FindByName('Rendered')
view.Redraw()
c=R.Display.ViewCapture();c.Width=2600;c.Height=1800;c.ScaleScreenItems=True;c.DrawAxes=False;c.DrawGrid=False;c.DrawGridAxes=False;c.TransparentBackground=False
b=c.CaptureToBitmap(view)
b.Save(os.path.join(root,'vistas','00_REVISION_AXONOMETRIA.png'),System.Drawing.Imaging.ImageFormat.Png)
with open(os.path.join(root,'verificacion','captura_nativa.json'),'w') as f:json.dump({'file':d.Name,'objects':d.Objects.Count,'mode':vp.DisplayMode.EnglishName,'capture':'00_REVISION_AXONOMETRIA.png'},f)
print('CAPTURA_REVISION_LISTA')
