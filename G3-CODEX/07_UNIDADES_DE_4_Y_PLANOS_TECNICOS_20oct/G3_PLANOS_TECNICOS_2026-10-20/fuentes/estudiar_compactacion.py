import sys,contextlib,io,json
from shapely.geometry import box,Point,LineString
from shapely.ops import unary_union
from shapely.affinity import translate
from pathlib import Path
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P.parent/'G3_MODELOS_HERENCIA_MACARRA_2026-10-19/fuentes/base_geometry/fuentes'))
with contextlib.redirect_stdout(io.StringIO()):import geometria as G
compact={}
for fam in ['V01','V02','V03']:
 u=G.U[fam]
 if fam=='V01':
  for r in u['rooms']:r['q']=(r['q'][0],1.8 if r['q'][1]>0 else -1.8)
  u['core']=G.rounded(-6.4,-1.8,5.3,1.8,.24)
 elif fam=='V02':
  for r in u['rooms']:
   x,y=r['q'];r['q']=(x,2.25 if y==2.7 else -2.25 if y==-2.7 else y)
  u['core']=unary_union([G.rounded(-6.4,-1.2,-.02,2.25,.3),G.rounded(.02,-2.25,5.35,1.2,.3),G.rounded(-.8,-.7,.8,.7,.15)])
  u['kitchen']=translate(u['kitchen'],yoff=.45);u['table']=translate(u['table'],yoff=-.55)
 else:
  for r,q in zip(u['rooms'],[(1.8,2.8),(2.8,-.15),(-.15,-2.8),(-2.8,-1.8)]):r['q']=q
  c=Point(0,0).buffer(3.65,quad_segs=80)
  for r in u['rooms']:
   ap=G.tf(Point(2.6,-.45),r);c=c.union(LineString([(0,0),(ap.x,ap.y)]).buffer(.85)).union(G.tf(box(1.85,-1.1,3.35,.1),r))
  u['core']=c;u['kitchen']=translate(u['kitchen'],xoff=-.4,yoff=.4)
  obank=u['bank'];u['bank']=G.pod(lambda g:translate(obank['T'](g),-1.8,1.8));u['core']=u['core'].union(LineString([(0,0),(-3.2,3.2)]).buffer(.80))
 with contextlib.redirect_stdout(io.StringIO()):f=G.allcase(fam)
 print(fam,json.dumps(f['audit']),f['floor'].bounds)
 print('furniturevswalls',unary_union(f['furniture']).intersection(f['solid']).area)
 furniture=f['kitchens']+f['tables']+f['chairs']
 common=f['common'];free=common.difference(f['solid']).difference(unary_union(furniture)).buffer(-.45)
 root=next((p for p in G.polys(free) if p.buffer(.003).covers(Point(f['entry']['inside']))),None)
 print('WITHOUTSOFA',[(root is not None and root.buffer(.003).covers(p)) for p in f['approaches']], 'badfurn',unary_union(furniture).intersection(f['solid']).area,'outside',unary_union(furniture).difference(f['floor']).area)
 fr=f['common'].difference(f['solid']).buffer(-.45)
 rr=next((p for p in G.polys(fr) if p.buffer(.003).covers(Point(f['entry']['inside']))),None)
 print('EMPTY reachable',[(rr is not None and rr.buffer(.003).covers(p)) for p in f['approaches']],'entry',f['entry']['inside'])
 from shapely.affinity import rotate
 import random,math
 random.seed(20261020)
 allowed=f['common'].difference(f['solid']).simplify(.003,preserve_topology=True).buffer(-.04)
 walkbase=f['common'].difference(f['solid']).simplify(.003,preserve_topology=True).buffer(-.45)
 targets=f['approaches']+[p for b in f['banks'] for p in b['approaches']]
 # Search movable equipment only; all four private rooms stay at true size.
 kt=unary_union(f['kitchens']);tc=unary_union(f['tables']+f['chairs']);kc=kt.centroid;cc=tc.centroid
 def candidates(g,c,n):
  out=[]
  for ang in [0,90,180,270]:
   rg=rotate(g,ang,origin=(c.x,c.y))
   for k in range(n):
    x=round(random.uniform(-5,4.3)*4)/4;y=round(random.uniform(-2,2)*4)/4
    gg=translate(rg,xoff=x-c.x,yoff=y-c.y)
    if allowed.covers(gg):out.append((gg,(x-c.x,y-c.y,ang),Point(x,y).distance(c)))
  return sorted(out,key=lambda a:a[2])
 ks=candidates(kt,kc,500);ts=candidates(tc,cc,700);best=None
 print('search',fam,len(ks),len(ts),flush=True)
 for kg,kpar,kcost in ks:
  kfree=walkbase.difference(kg.buffer(.45))
  kr=next((p for p in G.polys(kfree) if p.covers(Point(f['entry']['inside']))),None)
  if kr is None or not all(kr.covers(p) for p in targets):continue
  for tg,tpar,tcost in ts:
   if best and kcost+tcost>=best[0]:continue
   if kg.intersection(tg).area>1e-6:continue
   free=kfree.difference(tg.buffer(.45))
   root=next((p for p in G.polys(free) if p.buffer(.003).covers(Point(f['entry']['inside']))),None)
   if root is not None and all(root.buffer(.003).covers(p) for p in targets):
    best=(kcost+tcost,kpar,tpar);break
  if best:break
 if not best:raise RuntimeError(('NO SOLUTION',fam))
 print('SOLUTION',fam,best,flush=True)
 def trans(g,par,c):return translate(rotate(g,par[2],origin=(c.x,c.y)),xoff=par[0],yoff=par[1])
 f['kitchens']=[trans(g,best[1],kc) for g in f['kitchens']];f['tables']=[trans(g,best[2],cc) for g in f['tables']];f['chairs']=[trans(g,best[2],cc) for g in f['chairs']];f['sofas']=[]
 compact[fam]={'rooms':[r['r'] for r in f['rooms']],'core':f['core'].wkt,'floor':f['floor'].wkt,'solid':f['solid'].wkt,'windows':[g.wkt for g in f['windows']],'doors':[g.wkt for g in f['doors']],'kitchens':[g.wkt for g in f['kitchens']],'tables':[g.wkt for g in f['tables']],'chairs':[g.wkt for g in f['chairs']],'entry':{k:(v.wkt if hasattr(v,'wkt') else v) for k,v in f['entry'].items()},'area':f['floor'].area,'bounds':f['floor'].bounds,'furniture_moves':{'kitchen':best[1],'table_chairs':best[2],'kitchen_origin':list(kc.coords)[0],'table_origin':list(cc.coords)[0]},'paths90':True,'bank_delta':[-1.8,1.8] if fam=='V03' else [0,0]}

 (P/'verificacion/COMPACTACION.json').write_text(json.dumps(compact,ensure_ascii=False,indent=2))
