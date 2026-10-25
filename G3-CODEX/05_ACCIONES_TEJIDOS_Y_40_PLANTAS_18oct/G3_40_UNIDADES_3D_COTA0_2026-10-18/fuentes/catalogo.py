from pathlib import Path
import rhino3dm as r,json,math
P=Path(__file__).resolve().parents[1];files=sorted(q for q in (P/'modelos_finales').glob('N*_UNIDAD_3D.3dm') if not q.name.startswith('._'));assert len(files)==40
master=r.File3dm();master.Settings.ModelUnitSystem=r.UnitSystem.Meters;master.Settings.ModelAbsoluteTolerance=.001;materials={};report=[]
for i,p in enumerate(files):
 f=r.File3dm.Read(str(p));code=p.name.split('_')[0];offset=((i%5)*60,-(i//5)*60,0);tr=r.Transform.Translation(*offset);root=r.Layer();root.Name=code;root.Color=(90,110,95,255);rootidx=master.Layers.Add(root);rootid=master.Layers[rootidx].Id;layer_map={}
 for layer in f.Layers:
  l=r.Layer();l.Name=layer.Name;l.Color=layer.Color;l.Visible=layer.Visible;l.ParentLayerId=rootid;layer_map[layer.Index]=master.Layers.Add(l)
 mat_map={}
 for matidx,mat in enumerate(f.Materials):
  if mat.Name not in materials:materials[mat.Name]=master.Materials.Add(mat)
  mat_map[matidx]=materials[mat.Name]
 invalid=0;floorbounds=None
 for obj in f.Objects:
  geom=obj.Geometry;geom.Transform(tr);a=obj.Attributes;a.LayerIndex=layer_map[a.LayerIndex]
  if a.MaterialIndex in mat_map:a.MaterialIndex=mat_map[a.MaterialIndex]
  if not geom.IsValid:invalid+=1
  master.Objects.Add(geom,a)
  if a.Name.startswith('forjado'):floorbounds=geom.GetBoundingBox()
 assert invalid==0
 a=r.ObjectAttributes();a.LayerIndex=rootidx;master.Objects.AddTextDot(code,r.Point3d(offset[0],offset[1]-23,0),a)
 v=r.ViewInfo();v.Name=code;v.Viewport.SetCameraLocation(r.Point3d(offset[0]+28,offset[1]-32,35));v.Viewport.SetCameraDirection(r.Vector3d(-28,32,-34));v.Viewport.SetCameraUp(r.Vector3d(0,0,1));master.NamedViews.Add(v)
 report.append({'code':code,'offset_xy_m':offset[:2],'finished_floor_z':0,'objects':len(f.Objects),'invalid':invalid})
master.Strings['Abrir']='40 alternativas separadas 60m en XY, todas con suelo Z=0. No apiladas. Capas por código. Vistas nombradas por unidad.'
assert master.Write(str(P/'CATALOGO_40_UNIDADES_COTA0.3dm'),8)
f=r.File3dm.Read(str(P/'CATALOGO_40_UNIDADES_COTA0.3dm'));assert len(f.NamedViews)==40
(P/'verificacion/CATALOGO.json').write_text(json.dumps({'units':report,'objects':len(f.Objects),'named_views':len(f.NamedViews),'grid_spacing_m':60,'all_finished_floors_z':0},indent=2));print('CATALOGO',len(f.Objects),'objetos')
