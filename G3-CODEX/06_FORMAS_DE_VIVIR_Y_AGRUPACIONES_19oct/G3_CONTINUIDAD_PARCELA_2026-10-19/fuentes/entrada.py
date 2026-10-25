import geometria as G
f=G.F[2]
for p in G.polys(f['free']):
 print('PART',p.area,p.representative_point().wkt,'reaches',[p.covers(g) for g in f['approaches']])
for x,y in [(2.4,2.6),(2.5,2),(2.4,1),(2.7,2.5),(1.65,1.65)]:
 p=G.Point(x,y);print(x,y,'floor',p.distance(f['floor']),'wall',p.distance(f['solid']),'furn',min(p.distance(g) for g in f['furniture']),'free',p.distance(f['free']))
