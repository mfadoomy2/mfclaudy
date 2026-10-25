import rhino3dm as r,json,pathlib,collections,hashlib
B=pathlib.Path('/Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08');out={}
# Correct annotation, not geometry. Actual common stair step is 3 / 18.
p=B/'02_CONJUNTOS_reconstruidos.3dm';f=r.File3dm.Read(str(p));renamed=0
for o in f.Objects:
 if 'escalera abierta (uso general: C 0,175' in o.Attributes.Name:
  o.Attributes.Name=o.Attributes.Name.replace('C 0,175','C 0,1667');renamed+=1
f.Write(str(p),8)
for p in B.glob('*.3dm'):
 if p.name.startswith('.') or 'reparad' in p.name:continue
 f=r.File3dm.Read(str(p));counts=collections.Counter(type(o.Geometry).__name__ for o in f.Objects);bad=[str(o.Attributes.Id) for o in f.Objects if not o.Geometry.IsValid];openex=[str(o.Attributes.Id) for o in f.Objects if isinstance(o.Geometry,r.Extrusion) and not o.Geometry.IsSolid]
 out[p.name]={'objects':len(f.Objects),'types':dict(counts),'invalid':bad,'non_solid_extrusions':openex,'bytes':p.stat().st_size}
for src,dst in [('G3_unidad_suspendida_7.3dm','01_UNIDAD_reconstruida.3dm'),('G3_conjunto_opciones_1.3dm','02_CONJUNTOS_reconstruidos.3dm')]:
 a=r.File3dm.Read('/Users/adam/Downloads/'+src);b=r.File3dm.Read(str(B/dst));aa={str(o.Attributes.Id):o for o in a.Objects};bb={str(o.Attributes.Id):o for o in b.Objects};errs=[]
 for k in aa.keys()&bb.keys():
  x=aa[k].Geometry.GetBoundingBox();y=bb[k].Geometry.GetBoundingBox();errs.append(max(abs(getattr(u,v)-getattr(w,v)) for u,w in [(x.Min,y.Min),(x.Max,y.Max)] for v in 'XYZ'))
 out[dst]['missing_ids']=list(aa.keys()-bb.keys());out[dst]['added_ids']=list(bb.keys()-aa.keys());out[dst]['max_bbox_change_m']=max(errs);out[dst]['original_sha256']=hashlib.sha256(pathlib.Path('/Users/adam/Downloads/'+src).read_bytes()).hexdigest()
out['annotation_changes_common_stair_this_check']=renamed
out['annotation_common_stair_corrected_names']=sum('C 0,1667' in o.Attributes.Name for o in r.File3dm.Read(str(B/'02_CONJUNTOS_reconstruidos.3dm')).Objects)
(B/'VERIFICACION.json').write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out,indent=2,ensure_ascii=False))
# Remove only intermediate outputs produced by this run whose names overstated the repair.
for name in ['01_UNIDAD_reparada.3dm','02_CONJUNTOS_reparados.3dm']:
 p=B/name
 if p.exists():p.unlink()
