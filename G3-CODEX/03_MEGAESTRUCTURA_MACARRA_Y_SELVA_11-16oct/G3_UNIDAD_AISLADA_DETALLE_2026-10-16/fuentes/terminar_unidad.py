# -*- coding: utf-8 -*-
import Rhino as R,os,System,json
root=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16';d=R.RhinoDoc.ActiveDoc
removed=0
for o in list(d.Objects):
 if d.Layers[o.Attributes.LayerIndex].Name=='07_GALERIAS' or o.Attributes.Name in ['Hoja hiedra','Hiedra colgante'] or (o.Attributes.Name or '').startswith('Hiedra colgante '):
  d.Objects.Delete(o.Id,True);removed+=1
d.Views.Redraw()
v=d.Views.ActiveView;c=R.Display.ViewCapture();c.Width=2400;c.Height=1650;c.DrawAxes=False;c.DrawGrid=False;c.DrawGridAxes=False;b=c.CaptureToBitmap(v);b.Save(os.path.join(root,'vistas','05_RHINO_NATIVO.png'),System.Drawing.Imaging.ImageFormat.Png)
d.WriteFile(os.path.join(root,'modelos','UNIDAD_P02_DETALLADA.3dm'),R.FileIO.FileWriteOptions())
with open(os.path.join(root,'verificacion','apertura_nativa.json'),'w') as f:json.dump({'file':d.Name,'objects':d.Objects.Count,'mode':v.ActiveViewport.DisplayMode.EnglishName,'removed_unanchored_ivy_parts':removed,'capture':'05_RHINO_NATIVO.png'},f)
print('UNIDAD_FINAL_GUARDADA')
