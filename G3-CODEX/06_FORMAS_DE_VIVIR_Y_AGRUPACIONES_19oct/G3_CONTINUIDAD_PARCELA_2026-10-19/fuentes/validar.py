import geometria as G
for f in G.F:
 a=f['audit'];ray=G.LineString([f['entry']['inside'],f['entry']['outside']])
 print(a['codigo'],'entry_wall',round(ray.intersection(f['solid']).length,3),'furnwall',round(G.unary_union(f['furniture']).intersection(f['solid']).area,4),'outsidein',f['floor'].covers(G.Point(f['entry']['outside'])))
for f in [G.F[2],G.F[6]]:
 print(f['audit']['codigo'])
 for x,y in [(3.4,3.1),(3.4,3.3),(3.5,3.1),(-2.8,-3.7),(-3,-3.8),(-2.9,-3.4)]:
  p=G.Point(x,y);print(x,y,'inside',f['floor'].covers(p),'privdist',round(p.distance(f['priv']),2))
