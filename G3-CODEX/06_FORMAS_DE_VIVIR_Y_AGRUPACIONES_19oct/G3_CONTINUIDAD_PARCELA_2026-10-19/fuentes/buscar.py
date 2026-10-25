import geometria as G
import contextlib,io
from shapely.geometry import box,Point
from shapely.ops import unary_union
f=G.F[2]
free=f['common'].difference(f['solid']).buffer(-.45)
root=next((p for p in G.polys(free) if p.covers(Point(f['entry']['inside']))),None)
print('EMPTY', [root.covers(p) if root else False for p in f['approaches']])
u=G.U['V03']; best=[]
# Search furniture only within shared area, maintain full dimensions and a connected 90cm route.
for tx in [-1.4,-.8,-.2,.4,1.0]:
 for ty in [-1.4,-.8,-.2,.4,1.0]:
  for vertical in [True,False]:
   table=box(tx,ty,tx+(.85 if vertical else 1.6),ty+(1.6 if vertical else .85))
   for sx,sy,sv in [(-2.6,-.8,True),(-2.3,-1.65,False),(-.8,1.8,False),(1.0,1.,True),(-2.5,.3,True)]:
    sofa=box(sx,sy,sx+(.75 if sv else 1.9),sy+(1.9 if sv else .75))
    u['table']=table;u['sofa']=sofa
    with contextlib.redirect_stdout(io.StringIO()):a=G.allcase('V03')
    aa=a['audit']
    score=aa['accesos_dormitorios_disco90']+aa['accesos_banos_disco90']
    if score==6 and aa['solapes_muebles_m2']==0 and aa['muebles_fuera_suelo_m2']==0:
     print('FOUND',tx,ty,vertical,sx,sy,sv);raise SystemExit
print('NONE')
