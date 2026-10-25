from pathlib import Path
import rhino3dm as r,json,collections,math
R=Path(__file__).resolve().parents[1];S=R.parent/'G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16';src=r.File3dm.Read(str(S/'modelos/SELVA_MACARRA_V4_FINAL.3dm'))
p=json.loads((S/'calculo/ESTRUCTURA_RESULTADOS.json').read_text())['plates'][1];cx,fy,z=p['cx'],p['front'],p['z'];move=r.Transform.Translation(-cx,-fy,-z)
out=r.File3dm();out.Settings.ModelUnitSystem=r.UnitSystem.Meters;out.Settings.ModelAbsoluteTolerance=.001
for l in src.Layers:
 ll=r.Layer();ll.Name=l.Name;ll.Color=l.Color;ll.Visible=True;out.Layers.Add(ll)
for m in src.Materials:
 mm=r.Material();mm.Name=m.Name;mm.DiffuseColor=m.DiffuseColor;mm.Transparency=m.Transparency;mm.Shine=m.Shine;out.Materials.Add(mm)
lookup={str(o.Attributes.Id):o for o in src.Objects};defs={str(d.Id):d for d in src.InstanceDefinitions};batches={};notes=[]
def bake(g,a,xf):
 if a.Name=='Pavimento domestico':return # The terrace plate already supplies the domestic floor; avoid coincident solids.
 if isinstance(g,r.InstanceReference):
  dd=defs[str(g.ParentIdefId)]
  for oid in dd.GetObjectIds():
   ob=lookup[str(oid)];bake(ob.Geometry,ob.Attributes,r.Transform.Multiply(xf,g.Xform))
  return
 gg=g.Duplicate();gg.Transform(xf);aa=r.ObjectAttributes();aa.LayerIndex=a.LayerIndex;aa.MaterialIndex=a.MaterialIndex;aa.MaterialSource=a.MaterialSource;aa.Name=a.Name;aa.ObjectColor=a.ObjectColor;aa.ColorSource=a.ColorSource;aa.SetUserString('Origen','Unidad P02 extraida del modelo V4; sin escalado');out.Objects.Add(gg,aa)
 meshes=[]
 if isinstance(g,r.Brep):meshes=[m for f in g.Faces if (m:=f.GetMesh(r.MeshType.Render)) is not None]
 elif isinstance(g,r.Mesh):meshes=[g]
 key=str(a.LayerIndex)+'_'+str(a.MaterialIndex)
 if key not in batches:
  mat=src.Materials.FindIndex(a.MaterialIndex);col=mat.DiffuseColor;la=src.Layers.FindIndex(a.LayerIndex).Name
  batches[key]={'layer':la,'color':[v/255 for v in col[:3]],'alpha':mat.Transparency,'vertices':[],'faces':[]}
 b=batches[key]
 for m in meshes:
  mm=m.Duplicate();mm.Transform(xf);off=len(b['vertices']);b['vertices'].extend([[v.X,v.Y,v.Z] for v in mm.Vertices])
  for face in mm.Faces:b['faces'].append([off+i for i in (face[:3] if face[2]==face[3] else face)])
for ob in src.Objects:
 if ob.Attributes.IsInstanceDefinitionObject:continue
 g,a=ob.Geometry,ob.Attributes;name=a.Name or '';
 if name=='Hoja hiedra' or name.startswith('Hiedra colgante'):continue
 la=src.Layers.FindIndex(a.LayerIndex).Name
 if name=='P02 gran pabellon':bake(g,a,move);notes.append(name);continue
 if la in ['90_CONTEXTO','00_PARCELA','25_URBANIZACION','17_NUCLEOS','18_ASCENSOR','19_ASCENSOR_VIDRIO','26_ARRIOSTRAMIENTO','28_CIMENTACION','09_ESCALERAS','07_GALERIAS','02_ESTRUCTURA_RAMAS']:continue
 if la=='08_BARANDILLAS' and not name.startswith('P02'):continue
 if la in ['01_BANDEJAS','03_CELOSIAS'] and not name.startswith('P02'):continue
 if la=='10_UNIDADES':continue
 if isinstance(g,r.InstanceReference):
  x,y,zz=g.Xform.M03,g.Xform.M13,g.Xform.M23
  inside=(cx-6.3<x<cx+6.3 and fy-2.2<y<fy+7.2 and z-.7<zz<z+5.4)
 else:
  bb=g.GetBoundingBox();x,y,zz=(bb.Min.X+bb.Max.X)/2,(bb.Min.Y+bb.Max.Y)/2,(bb.Min.Z+bb.Max.Z)/2
  inside=(cx-6.3<x<cx+6.3 and fy-2.2<y<fy+7.2 and z-.7<zz<z+5.4 and bb.Max.Z-bb.Min.Z<6 and bb.Min.Z>=z-.7 and bb.Max.Z<=z+5.35)
 if inside:bake(g,a,move);notes.append(name)
for name,loc,tgt in [('01_UNIDAD_COMPLETA',(17,-20,13),(0,2.7,1.5)),('02_INTERIOR',(9,-13,9),(0,3.2,1.3)),('03_PLANTA',(0,3,30),(0,3,0)),('04_ENCUENTROS',(9,-8,3),(3,1,0))]:
 v=r.ViewInfo();v.Name=name;vp=v.Viewport;vp.SetCameraLocation(r.Point3d(*loc));vp.SetCameraDirection(r.Vector3d(*(tgt[i]-loc[i] for i in range(3))));vp.SetCameraUp(r.Vector3d(0,1,0) if 'PLANTA' in name else r.Vector3d(0,0,1));vp.TargetPoint=r.Point3d(*tgt);vp.ChangeToParallelProjection(True);vp.Extents(.6,r.BoundingBox(r.Point3d(-6.5,-2.3,-.8),r.Point3d(6.5,7.3,5.6)));out.NamedViews.Add(v)
assert out.Write(str(R/'modelos/UNIDAD_P02_DETALLADA.3dm'),8)
for l in out.Layers:
 if l.Name in ['06_VELAS','12_CUBIERTAS','14_VIDRIOS','13_COSTILLAS']:l.Visible=False
assert out.Write(str(R/'modelos/UNIDAD_P02_INTERIOR_EDITABLE.3dm'),8)
(R/'fuentes/geometria_unidad.json').write_text(json.dumps(batches,separators=(',',':')))
report={'source':str(S/'modelos/SELVA_MACARRA_V4_FINAL.3dm'),'unit':'P02','translation':[-cx,-fy,-z],'scale':1,'objects':len(out.Objects),'invalid':sum(not o.Geometry.IsValid for o in out.Objects),'native_breps':sum(isinstance(o.Geometry,r.Brep) for o in out.Objects),'meshes':sum(isinstance(o.Geometry,r.Mesh) for o in out.Objects),'top_objects_selected':notes,'warning':'Extraccion de anteproyecto; tolerancia geometrica 1mm no acredita precision de fabricacion ni comprobacion integral.'}
(R/'verificacion/extraccion.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print({k:v for k,v in report.items() if k!='top_objects_selected'},flush=True)
