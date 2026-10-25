from pathlib import Path
import math,json,csv,zipfile,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch
from shapely.geometry import Point,Polygon,LineString,box
from shapely.affinity import rotate,translate,scale
from shapely.ops import unary_union
import rhino3dm as rh
P=Path(__file__).resolve().parents[1];R=P.parent
# Read only the definitions of the previous study. Never execute its output-writing block.
base_source=P/'fuentes/BASE_ANTES.py'
src=base_source.read_text().split('F=[A,B,C3]')[0]
ns={'__file__':str(base_source)};exec(src,ns)
C=ns['C'];draw=ns['draw'];line=ns['line'];txt=ns['txt'];tf=ns['tf'];rounded=ns['rounded']
BASE=ns['base'];VEST=ns['vest'];WARD=ns['WARD'];BED=box(.25,2.00,1.50,4.00);DESK=box(.025,.10,1.825,1.0);STOOL=Point(.95,1.50).buffer(.23);DOOR=ns['DOOR']
# Small circular bow, 0.60 m maximum projection beyond y=4.30.
BC=(1.80,3.65);BR=1.25
bow=Point(*BC).buffer(BR,quad_segs=96).intersection(box(0,4.18,4,5.1))
ROOM=unary_union([BASE,VEST,bow]).buffer(.04).buffer(-.04)
SEAT=Point(*BC).buffer(1.17,quad_segs=96).difference(Point(*BC).buffer(.60,quad_segs=96)).intersection(box(.4,4.04,3.3,5.0))
a0=math.asin((4.30-BC[1])/BR)
angles=np.linspace(a0,math.pi-a0,120)
ARC=LineString([(BC[0]+BR*math.cos(a),BC[1]+BR*math.sin(a)) for a in angles])
WIN=ARC.buffer(.065)
TEXTILE=LineString([(BC[0]+(BR+.18)*math.cos(a),BC[1]+(BR+.18)*math.sin(a)) for a in angles])
FURN={'cama':BED,'mesa_A1':DESK,'vestidor':WARD,'bow_asiento':SEAT,'taburete_en_uso':STOOL}
TARGETS={'entrada':(2.6,.65),'cama':(2.2,3.0),'vestidor':(3.65,3.1),'bow':(2.4,3.55),'dibujar':(.95,1.50)}
privfree=ROOM.difference(unary_union([BED,DESK,WARD,SEAT])).buffer(-.4)
pparts=[privfree] if privfree.geom_type=='Polygon' else list(privfree.geoms)
proot=next((p for p in pparts if p.covers(Point(TARGETS['entrada']))),None)
privcheck={k:bool(proot is not None and proot.buffer(.002).covers(Point(v))) for k,v in TARGETS.items()}
assert all(privcheck.values()),privcheck
assert sum(a.intersection(b).area for i,a in enumerate(FURN.values()) for j,b in enumerate(FURN.values()) if j>i)<1e-6

def polys(g):return [g] if g.geom_type=='Polygon' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']
def parts(g):return [g] if g.geom_type=='LineString' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='LineString']
def geom(f):return unary_union([f['core']]+[tf(ROOM,r) for r in f['rooms']])
def transformed(g,fam,T):return T(g)

def pod(T):
 # The bathrooms are at the outer edge. A 1.30 m portal and a screen form a dogleg.
 baths0=[box(2.1,-2.1,3.9,-.1),box(2.1,.1,3.9,2.1)]
 shell0=rounded(-.1,-2.28,4.08,2.28,.18)
 doors0=[box(1.9,y-.45,2.3,y+.45) for y in [-1.1,1.1]]
 screen0=box(.99,-.8,1.11,.8)
 partition0=box(-.06,-2.28,.06,2.28).difference(box(-.1,-.65,.1,.65))
 return {'floor':T(shell0),'baths':[T(b) for b in baths0],'doors':[T(d) for d in doors0], 'screen':T(screen0),'partition':T(partition0),'approaches':[T(Point(1.6,y)) for y in [-1.1,1.1]],'outside_view':T(Point(-.7,0)),'door_centres':[T(Point(2.1,y)) for y in [-1.1,1.1]],'T':T,'baths0':baths0}
def unit(fam):
 old={'V01':ns['A'],'V02':ns['B'],'V03':ns['C3']}[fam]
 rooms=[dict(r) for r in old['rooms']]
 if fam=='V01':
  core=rounded(-6.4,-1.8,5.3,1.8,.24);Tp=lambda g:translate(rotate(g,180,origin=(0,0)),-6.4,0)
  kitchen=box(-6.12,1.05,-3.25,1.65);table=box(-1.25,-.8,-.4,.8);sofa=old['sofa']
  entry=old['entry']
 elif fam=='V02':
  core=unary_union([rounded(-6.4,-1.2,-.02,2.7,.3),rounded(.02,-2.7,5.35,1.2,.3),rounded(-.8,-.7,.8,.7,.15)])
  Tp=lambda g:translate(rotate(g,180,origin=(0,0)),-6.4,.15)
  kitchen=box(-6.12,2.02,-3.3,2.62);table=box(.4,-1.6,2.,-.75);sofa=old['sofa'];entry=old['entry']
 else:
  core=Point(0,0).buffer(3.25,quad_segs=80)
  for r in rooms:core=core.union(tf(box(1.85,-1.1,3.35,.10),r))
  Tp=lambda g:translate(rotate(g,135,origin=(0,0)),-6.4/math.sqrt(2),6.4/math.sqrt(2))
  connector=rotate(box(3.0,-.7,6.5,.7),135,origin=(0,0));core=core.union(connector)
  kitchen=translate(rotate(box(-1.2,-.3,1.2,.3),45,origin=(0,0)),1.8,-1.8)
  table=box(-1.35,-.45,.25,.4);sofa=box(-1.4,1.25,.6,2.05)
  ep=np.array([1,1])*3.25/math.sqrt(2)
  cut=LineString([tuple(ep+[-.65,.65]),tuple(ep+[.65,-.65])]).buffer(.2,cap_style=2)
  entry={'cut':cut,'inside':(1.65,1.65),'outside':(2.95,2.95)}
 bank=pod(Tp)
 floor=unary_union([core,bank['floor']]+[tf(ROOM,r) for r in rooms])
 return locals()
U={k:unit(k) for k in ['V01','V02','V03']}
def allcase(fam,mode='U'):
 u=U[fam];rooms=[];banks=[]
 if mode=='U':trans=[lambda g:g];link=Polygon();entry=u['entry'];core=u['core'];cx=cy=0
 else:
  if fam=='V01':
   shift=14.6 if mode=='D' else 10.6;T=lambda g:translate(scale(g,xfact=-1,yfact=1,origin=(0,0)),shift,0);cx=shift/2;cy=0
   if mode=='D':link=rounded(4.6,-3.2,shift-4.6,3.2,1.3);entry={'cut':box(cx-.8,-3.5,cx+.8,-2.9),'inside':(cx,-2.5),'outside':(cx,-4.1)}
   else:link=rounded(3.4,-2.4,shift-3.4,2.4,.60).union(rounded(2.0,1.2,shift-2.0,2.7,.25));entry={'cut':box(cx-.8,2.45,cx+.8,2.95),'inside':(cx,1.7),'outside':(cx,3.6)}
  elif fam=='V02':
   shift=13.7;T=lambda g:translate(scale(g,xfact=-1,yfact=1,origin=(0,0)),shift,0);cx=shift/2;cy=.2
   link=box(5.35,-.45,shift-5.35,.85).union(Point(cx,.2).buffer(1.3)).union(box(cx-.65,-1.8,cx+.65,.2))
   entry={'cut':box(cx-.65,-2.0,cx+.65,-1.6),'inside':(cx,-1.0),'outside':(cx,-2.7)}
  else:
   shift=12.0 if mode=='D' else 11.4;T=lambda g:translate(rotate(g,180,origin=(0,0)),shift,shift);cx=cy=shift/2
   diagonal=LineString([(2.2,2.2),(shift-2.2,shift-2.2)])
   link=diagonal.buffer(1.8).union(Point(cx,cy).buffer(3.05,quad_segs=64)) if mode=='D' else diagonal.buffer(2.25,quad_segs=64)
   d=np.array([1,-1])/math.sqrt(2);reach=3.05 if mode=='D' else 2.25;ep=np.array([cx,cy])+d*reach
   entry={'cut':LineString([tuple(ep+[-.7,-.7]),tuple(ep+[.7,.7])]).buffer(.24,cap_style=2),'inside':tuple(ep-d*.8),'outside':tuple(ep+d*1.)}
  trans=[lambda g:g,T];core=unary_union([u['core'],T(u['core']),link])
 for tr in trans:
  for i,r0 in enumerate(u['rooms']):
   r=dict(r0)
   if fam=='V01' and mode=='S' and i==1:r['q']=(r['q'][0],r['q'][1]+.9)
   rooms.append({'id':f'H{len(rooms)+1:02d}','r':r,'T':tr,'poly':tr(tf(ROOM,r))})
  b=u['bank'];banks.append({'floor':tr(b['floor']),'baths':[tr(g) for g in b['baths']],'doors':[tr(g) for g in b['doors']],'screen':tr(b['screen']),'partition':tr(b['partition']),'approaches':[tr(g) for g in b['approaches']],'door_centres':[tr(g) for g in b['door_centres']],'view':tr(b['outside_view']),'T':lambda g,tr=tr,b=b:tr(b['T'](g))})
 priv=unary_union([r['poly'] for r in rooms]);floor=unary_union([core,priv]+[b['floor'] for b in banks]);assert floor.geom_type=='Polygon'
 baths=[g for b in banks for g in b['baths']]
 # The service vestibules are excluded from the principal living area.
 service=unary_union([b['floor'] for b in banks]);living=floor.difference(priv).difference(service)
 common=floor.difference(priv).difference(unary_union(baths))
 kitchens=[u['kitchen']];utility=[];work=[];sofas=[u['sofa']]
 tables=[u['table']];chairs=[]
 if mode=='U':
  tx,ty,tX,tY=tables[0].bounds
  chairs=[Point(x,y).buffer(.21) for x in [tx+.35,tX-.35] for y in [ty-.35,tY+.35]] if tX-tx>tY-ty else [Point(x,y).buffer(.21) for x in [tx-.35,tX+.35] for y in [ty+.35,tY-.35]]
 else:
  kitchens += [trans[1](u['kitchen'])] if fam!='V01' else []
  if fam=='V01':utility=[trans[1](u['kitchen'])];work=[u['table']];sofas=[trans[1](u['table'])]
  else:work=[u['table'],trans[1](u['table'])];sofas=[u['sofa'],trans[1](u['sofa'])]
  if fam=='V02':
   tables=[];chairs=[] # two dining tables remain, one in each shared focus, plus shared threshold.
   tables=[u['table'],trans[1](u['table'])];work=[]
   for tb in tables:
    tx,ty,tX,tY=tb.bounds;chairs += [Point(x,y).buffer(.21) for x in [tx+.35,tX-.35] for y in [ty-.35,tY+.35]]
  else:
   tb=box(-1.6,-.45,1.6,.45);tables=[translate(tb,cx,cy) if fam=='V01' else translate(rotate(tb,45,origin=(0,0)),cx,cy)]
   chairs=[translate(rotate(Point(x,y).buffer(.21),0 if fam=='V01' else 45,origin=(0,0)),cx,cy) for x in [-1.25,-.42,.42,1.25] for y in [-.85,.85]]
   if fam=='V01' and mode=='D':sofas.append(box(cx-1.1,2.15,cx+1.1,2.85))
 furniture=kitchens+utility+work+sofas+tables+chairs
 walls=unary_union([floor.boundary.buffer(.06)]+[r['poly'].boundary.buffer(.06) for r in rooms]+[b.boundary.buffer(.06) for b in baths]+[b['partition'] for b in banks]+[b['screen'] for b in banks])
 doors=[entry['cut']]+[r['T'](tf(DOOR,r['r'])) for r in rooms]+[g for b in banks for g in b['doors']]
 windows=[r['T'](tf(WIN,r['r'])) for r in rooms]
 # Bath/pod exterior windows are not used as room daylight sources.
 boundary=floor.boundary.difference(priv.buffer(.15)).difference(service.buffer(.15)).difference(unary_union(kitchens+utility).buffer(.2)).difference(entry['cut'].buffer(.3))
 wc=[]
 for seg in parts(boundary):
  if seg.length<1.1:continue
  mid=seg.length/2;ls=LineString([seg.interpolate(t).coords[0] for t in np.linspace(max(0,mid-.65),min(seg.length,mid+.65),25)])
  g=ls.buffer(.13)
  if g.intersection(priv).area<1e-5:wc.append(g)
 windows+=wc;solid=walls.difference(unary_union(doors)).difference(unary_union(windows))
 free=common.difference(solid).difference(unary_union(furniture)).buffer(-.45)
 root=next((g for g in polys(free) if g.buffer(.002).covers(Point(entry['inside']))),None)
 approaches=[r['T'](tf(Point(2.6,-.6),r['r'])) for r in rooms]
 reachable=[bool(root is not None and root.buffer(.002).covers(g)) for g in approaches]
 ba=[p for b in banks for p in b['approaches']];br=[bool(root is not None and root.buffer(.002).covers(p)) for p in ba]
 strips=[r['T'](tf(box(.72,5.08,2.88,8.08),r['r'])) for r in rooms];clear=[g.intersection(floor).area<1e-5 for g in strips]
 # Each bath must share a measurable boundary with the outside of the floor.
 ext=[b.boundary.intersection(floor.boundary.buffer(.23)).length for b in baths]
 # Sample visibility from named living viewpoints, with the actual screens, portal and bath walls.
 sight=[]
 viewpoints=[Point(entry['inside']),Point(cx,cy)] if mode!='U' else [tables[0].centroid,sofas[0].centroid]
 for bank in banks:
  local=bank['view'];views=viewpoints+[local]
  for dc in bank['door_centres']:
   sight.extend(LineString([vp,dc]).intersection(solid).length>.01 for vp in views)
 overlap=sum(a['poly'].intersection(b['poly']).area for i,a in enumerate(rooms) for j,b in enumerate(rooms) if j>i)
 audit={'codigo':fam+'_'+mode,'habitantes':len(rooms),'suelo_m2':round(floor.area,2),'envolvente_estudio_m2':round(floor.buffer(.12).area,2),'banos':len(baths),'aseos_en_borde':sum(e>.3 for e in ext),'longitud_contacto_exterior_banos_m':[round(e,2) for e in ext],'accesos_dormitorios_disco90':sum(reachable),'accesos_banos_disco90':sum(br),'dormitorios_ok':reachable,'banos_ok':br,'bow_exterior_3m':sum(clear),'bow_ok':clear,'lineas_visuales_muestreadas_filtradas':sum(sight),'lineas_visuales_muestreadas':len(sight),'solape_habitaciones_m2':round(overlap,6),'muebles_fuera_suelo_m2':round(unary_union(furniture).difference(floor).area,6),'solapes_muebles_m2':round(sum(a.intersection(b).area for i,a in enumerate(furniture) for j,b in enumerate(furniture) if j>i),6),'servicios_fuera_ambito_principal':living.intersection(unary_union(baths)).area<1e-7}
 print(json.dumps(audit,ensure_ascii=False),flush=True)
 return locals()
F=[allcase(k) for k in ['V01','V02','V03']]+[allcase('V02','P')]+[allcase(k,m) for k in ['V01','V03'] for m in ['D','S']]
(P/'verificacion/PROVISIONAL.json').write_text(json.dumps([f['audit'] for f in F],ensure_ascii=False,indent=2))
for f in F:
 a=f['audit']
 assert a['aseos_en_borde']==a['banos']
 assert a['accesos_dormitorios_disco90']==a['habitantes']
 assert a['accesos_banos_disco90']==a['banos']
 assert a['bow_exterior_3m']==a['habitantes']
 assert a['lineas_visuales_muestreadas_filtradas']==a['lineas_visuales_muestreadas']
 assert a['solape_habitaciones_m2']==a['muebles_fuera_suelo_m2']==a['solapes_muebles_m2']==0
 assert a['servicios_fuera_ambito_principal']
(P/'verificacion/GEOMETRIA_FINAL.json').write_text(json.dumps({'habitacion_m2':round(ROOM.area,2),'habitacion_recorridos80':privcheck,'alternativas':[f['audit'] for f in F]},ensure_ascii=False,indent=2))
