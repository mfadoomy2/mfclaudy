import geometria as G
for f in G.F[6:]:
 done=False
 for angle in [0,45,90]:
  for dx in [0,-.5,.5,-1.,1.,-1.5,1.5,-2,2]:
   for dy in [0,-.5,.5,-1,1,-1.5,1.5,-2,2]:
    table=G.translate(G.rotate(G.box(-1.6,-.45,1.6,.45),angle,origin=(0,0)),f['cx']+dx,f['cy']+dy)
    chairs=[G.translate(G.rotate(G.Point(x,y).buffer(.21),angle,origin=(0,0)),f['cx']+dx,f['cy']+dy) for x in [-1.25,-.42,.42,1.25] for y in [-.85,.85]]
    furniture=f['kitchens']+f['sofas']+[table]+chairs
    if G.unary_union(furniture).difference(f['common']).area>1e-5:continue
    if sum(a.intersection(b).area for i,a in enumerate(furniture) for j,b in enumerate(furniture) if j>i)>1e-5:continue
    fr=f['common'].difference(f['solid']).difference(G.unary_union(furniture)).buffer(-.45)
    root=next((p for p in G.polys(fr) if p.covers(G.Point(f['entry']['inside']))),None)
    if root is not None and all(root.covers(p) for p in f['approaches']+[p for b in f['banks'] for p in b['approaches']]):
     print('FOUND',f['mode'],angle,dx,dy);done=True;break
   if done:break
  if done:break
 print('DONE',done)
