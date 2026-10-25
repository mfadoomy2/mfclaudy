import rhino3dm as r,collections,json,pathlib,numpy as np
base=pathlib.Path('/Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08')
for short in ['unidad_suspendida_7','conjunto_opciones_1']:
 f=r.File3dm.Read('/Users/adam/Downloads/G3_'+short+'.3dm'); layers={l.Index:l for l in f.Layers};counts=collections.defaultdict(lambda:collections.Counter()); bad=[]
 for o in f.Objects:
  g=o.Geometry;l=layers[o.Attributes.LayerIndex];root=l.FullPath.split('::')[0];c=counts[root];c['objects']+=1
  if isinstance(g,r.Mesh):
   c['meshes']+=1;c['faces']+=len(g.Faces);c['vertices']+=len(g.Vertices)
   if not g.IsClosed:c['open']+=1
   if not g.IsValid:c['invalid']+=1;bad.append(str(o.Attributes.Id))
 print(short,json.dumps(counts,indent=2,ensure_ascii=False))
 (base/'trabajo'/('auditoria_'+short+'.json')).write_text(json.dumps({'counts':counts,'invalid_ids':bad},indent=2,ensure_ascii=False))
print('api', [x for x in dir(r.Mesh) if any(q in x.lower() for q in ['normal','compact','cull','append','face'])])
