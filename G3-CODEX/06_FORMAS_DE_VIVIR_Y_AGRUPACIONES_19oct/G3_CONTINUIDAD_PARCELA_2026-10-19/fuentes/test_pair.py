import geometria as G
for f in G.F[6:]:
 free=f['common'].difference(f['solid']).buffer(-.45)
 root=next((p for p in G.polys(free) if p.covers(G.Point(f['entry']['inside']))),None)
 print('EMPTY',f['mode'],[root.covers(p) if root else False for p in f['approaches']])
 for i in range(len(f['furniture'])):
  obs=G.unary_union([g for j,g in enumerate(f['furniture']) if j!=i]);fr=f['common'].difference(f['solid']).difference(obs).buffer(-.45)
  ro=next((p for p in G.polys(fr) if p.covers(G.Point(f['entry']['inside']))),None)
  n=sum(ro.covers(p) if ro else False for p in f['approaches'])
  if n>4:print('REMOVE',i,n,f['furniture'][i].bounds)
 print('INPRIVATE',[(i,round(g.intersection(f['priv']).area,3),round(g.intersection(f['solid']).area,3)) for i,g in enumerate(f['furniture'])])
