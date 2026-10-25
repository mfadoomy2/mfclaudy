import geometria as G
f=G.F[2]
for x in G.np.arange(-2.7,2,.2):
 for y in G.np.arange(-2.5,2.3,.2):
  for v in [False,True]:
   sf=G.box(x,y,x+(.75 if v else 1.9),y+(1.9 if v else .75))
   obs=f['kitchens']+f['tables']+f['chairs']+[sf]
   if sf.difference(f['common']).area>1e-6 or sf.intersection(f['solid']).area>1e-6:continue
   if any(sf.intersection(g).area>1e-6 for g in obs[:-1]):continue
   fr=f['common'].difference(f['solid']).difference(G.unary_union(obs)).buffer(-.45)
   ro=next((p for p in G.polys(fr) if p.covers(G.Point(1.65,1.65))),None)
   if ro is not None and all(ro.covers(p) for p in f['approaches']+[p for b in f['banks'] for p in b['approaches']]):print('FOUND',x,y,v);raise SystemExit
print('NONE')
