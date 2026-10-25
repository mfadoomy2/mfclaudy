from pathlib import Path
import json,collections,rhino3dm as r
R=Path(__file__).resolve().parents[1];out=[]
for p in sorted((R/'modelos').glob('*.3dm')):
 if p.name.startswith('._'):continue
 f=r.File3dm.Read(str(p));assert f,p
 objs=list(f.Objects);counts=collections.Counter(type(o.Geometry).__name__ for o in objs)
 a=dict(file=p.name,objects=len(objs),types=dict(counts),invalid=[str(o.Attributes.Id) for o in objs if not o.Geometry.IsValid],units=str(f.Settings.ModelUnitSystem),layers=len(f.Layers),definitions=len(f.InstanceDefinitions),named_views=[v.Name for v in f.NamedViews])
 a['people_instances']=sum(type(o.Geometry).__name__=='InstanceReference' and o.Attributes.LayerIndex==next((l.Index for l in f.Layers if 'PERSONAS' in l.Name),-99) for o in objs)
 a['pavilions']=sum('gran pabellon' in (o.Attributes.Name or '') for o in objs)
 out.append(a);print(p.name,len(objs),'invalid',len(a['invalid']),flush=True)
(R/'verificacion/auditoria_independiente.json').write_text(json.dumps(out,indent=2))
assert all(not a['invalid'] for a in out)
