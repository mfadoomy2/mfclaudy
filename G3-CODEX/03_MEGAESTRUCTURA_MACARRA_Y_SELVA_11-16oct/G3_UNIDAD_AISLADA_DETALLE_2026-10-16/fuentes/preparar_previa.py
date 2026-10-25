# -*- coding: utf-8 -*-
import Rhino as R, rhinoscriptsyntax as rs, System, os, json
root=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16';d=R.RhinoDoc.ActiveDoc;G=R.Geometry;P=G.Point3d
v=d.Views.ActiveView;v.Maximized=True;vp=v.ActiveViewport
vp.SetCameraLocations(P(0,2.6,1.6),P(17,-22,13));vp.CameraUp=G.Vector3d.ZAxis;vp.ChangeToParallelProjection(True);vp.ZoomBoundingBox(G.BoundingBox(P(-6.5,-2.3,-.8),P(6.5,7.3,5.6)));vp.DisplayMode=R.Display.DisplayModeDescription.FindByName('Rendered');v.Redraw()
c=R.Display.ViewCapture();c.Width=2400;c.Height=1650;c.DrawAxes=False;c.DrawGrid=False;c.DrawGridAxes=False;b=c.CaptureToBitmap(v);b.Save(os.path.join(root,'vistas','05_RHINO_NATIVO.png'),System.Drawing.Imaging.ImageFormat.Png)
d.WriteFile(os.path.join(root,'modelos','UNIDAD_P02_PREVIA_SOLIDA.3dm'),R.FileIO.FileWriteOptions())
with open(os.path.join(root,'verificacion','apertura_nativa.json'),'w') as f:json.dump({'file':d.Name,'objects':d.Objects.Count,'mode':vp.DisplayMode.EnglishName,'geometry':'Previa de mallas; el editable se entrega por separado'},f)
print('UNIDAD_ABIERTA_Y_GUARDADA')
