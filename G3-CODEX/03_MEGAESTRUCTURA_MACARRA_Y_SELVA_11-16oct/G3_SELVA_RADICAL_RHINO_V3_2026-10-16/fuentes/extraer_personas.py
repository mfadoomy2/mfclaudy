from pathlib import Path
import rhino3dm as r, json, collections
R=Path(__file__).resolve().parents[1]
d=r.File3dm.Read('/Volumes/T7/PERSONAS.3dm')
a=[]
for i,o in enumerate(d.Objects):
 g=o.Geometry
 if isinstance(g,r.Mesh) and not o.Attributes.IsInstanceDefinitionObject:
  b=g.GetBoundingBox();a.append({'i':i,'layer':o.Attributes.LayerIndex,'name':o.Attributes.Name,'min':[b.Min.X,b.Min.Y,b.Min.Z],'max':[b.Max.X,b.Max.Y,b.Max.Z],'f':g.Faces.Count})
(R/'verificacion/personas_inventario.json').write_text(json.dumps(a))
print('top meshes',len(a),'by layer',collections.Counter(x['layer'] for x in a))
for x in a[:55]:print(x)
print('groups',len(d.Groups))
for g in list(d.Groups)[:20]:print(g.Index,g.Name)
# Selected complete figures only; the source library is never changed.
clusters=json.loads((R/'verificacion/personas_clusters.json').read_text())
select=[19,20,25,30,34,42,43,45,17,18,27,29]
out=r.File3dm();out.Settings.ModelUnitSystem=r.UnitSystem.Meters
summary=[]
for k in select:
 item=next(x for x in clusters if x['cluster']==k);mes=r.Mesh()
 for idx in item['indices']:mes.Append(d.Objects[idx].Geometry)
 lo=item['min'];hi=item['max'];mes.Transform(r.Transform.Translation(-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]))
 mes.Faces.CullDegenerateFaces();mes.Normals.ComputeNormals()
 at=r.ObjectAttributes();at.Name='POSE_%02d'%k;out.Objects.AddMesh(mes,at)
 summary.append({'pose':k,'source_indices':item['indices'],'height':hi[2]-lo[2],'faces':mes.Faces.Count})
out.Write(str(R/'fuentes/personas_seleccionadas.3dm'),8)
(R/'verificacion/personas_procedencia.json').write_text(json.dumps({'source':'/Volumes/T7/PERSONAS.3dm','normalization':'translation to feet at z0; original proportions and scale preserved','figures':summary},indent=2))
print('EXPORTED',len(summary))
