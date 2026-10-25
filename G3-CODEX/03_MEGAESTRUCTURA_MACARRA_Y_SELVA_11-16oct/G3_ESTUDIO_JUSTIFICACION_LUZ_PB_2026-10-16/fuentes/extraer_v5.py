from pathlib import Path
import rhino3dm as r,json
R=Path(__file__).resolve().parents[1];f=r.File3dm.Read(str(R/'modelos/SELVA_V5_LUZ_Y_PLANTA_BAJA.3dm'));objs={str(o.Attributes.Id):o for o in f.Objects};defs={str(d.Id):d for d in f.InstanceDefinitions}
def base():
 out=r.File3dm();out.Settings.ModelUnitSystem=r.UnitSystem.Meters;out.Settings.ModelAbsoluteTolerance=.001
 for l in f.Layers:
  ll=r.Layer();ll.Name=l.Name;ll.Color=l.Color;ll.Visible=l.Visible;out.Layers.Add(ll)
 for m in f.Materials:
  mm=r.Material();mm.Name=m.Name;mm.DiffuseColor=m.DiffuseColor;mm.Transparency=m.Transparency;out.Materials.Add(mm)
 return out
def att(a):
 aa=r.ObjectAttributes();aa.Name=a.Name;aa.LayerIndex=a.LayerIndex;aa.MaterialIndex=a.MaterialIndex;aa.MaterialSource=a.MaterialSource;aa.ObjectColor=a.ObjectColor;aa.ColorSource=a.ColorSource;return aa
def flat(out,g,a,xf,filterfn=None):
 if isinstance(g,r.InstanceReference):
  for oid in defs[str(g.ParentIdefId)].GetObjectIds():
   ob=objs[str(oid)];flat(out,ob.Geometry,ob.Attributes,r.Transform.Multiply(xf,g.Xform),filterfn)
 else:
  gg=g.Duplicate();gg.Transform(xf)
  if filterfn and not filterfn(gg,a):return
  out.Objects.Add(gg,att(a))
out=base();dd=next(d for d in f.InstanceDefinitions if d.Name=='PABELLON_4_REFUGIOS')
for oid in dd.GetObjectIds():
 ob=objs[str(oid)];flat(out,ob.Geometry,ob.Attributes,r.Transform.Identity())
p=json.loads((R/'calculo/ESTRUCTURA_RESULTADOS.json').read_text())['plates'][3]
for ob in f.Objects:
 if (ob.Attributes.Name or '').startswith('P04 bandeja curvilinea'):flat(out,ob.Geometry,ob.Attributes,r.Transform.Translation(-p['cx'],-p['front'],-p['z']))
for name,loc,tgt in [('01_NORTE_Y_HABITACIONES',(15,22,16),(0,3,1.5)),('02_PLANTA',(0,3,35),(0,3,0))]:
 v=r.ViewInfo();v.Name=name;vp=v.Viewport;vp.SetCameraLocation(r.Point3d(*loc));vp.SetCameraDirection(r.Vector3d(*(tgt[i]-loc[i] for i in range(3))));vp.SetCameraUp(r.Vector3d(0,1,0) if 'PLANTA' in name else r.Vector3d(0,0,1));vp.TargetPoint=r.Point3d(*tgt);vp.ChangeToParallelProjection(True);vp.Extents(.6,r.BoundingBox(r.Point3d(-6.3,-2.2,-.5),r.Point3d(6.3,7,4.5)));out.NamedViews.Add(v)
out.Write(str(R/'modelos/UNIDAD_V5_NORTE_EDITABLE.3dm'),8)
for l in out.Layers:
 if l.Name in ['12_CUBIERTAS','13_COSTILLAS','14_VIDRIOS']:l.Visible=False
out.Write(str(R/'modelos/UNIDAD_V5_INTERIOR.3dm'),8)
out=base()
def pb(g,a):
 la=f.Layers.FindIndex(a.LayerIndex).Name
 if la in ['90_CONTEXTO','28_CIMENTACION','00_PARCELA']:return False
 bb=g.GetBoundingBox();return bb.Min.Z>=-.25 and bb.Max.Z<=3.15
for ob in f.Objects:
 if not ob.Attributes.IsInstanceDefinitionObject:flat(out,ob.Geometry,ob.Attributes,r.Transform.Identity(),pb)
out.Write(str(R/'modelos/PLANTA_BAJA_V5_EDITABLE.3dm'),8)
report=[]
for pp in sorted((R/'modelos').glob('*.3dm')):
 if pp.name.startswith('._'):continue
 d=r.File3dm.Read(str(pp));a={'file':pp.name,'objects':len(d.Objects),'invalid':sum(not o.Geometry.IsValid for o in d.Objects),'units':str(d.Settings.ModelUnitSystem)};report.append(a);print(a,flush=True)
(R/'verificacion/modelos.json').write_text(json.dumps(report,indent=2));assert all(not a['invalid'] for a in report)
