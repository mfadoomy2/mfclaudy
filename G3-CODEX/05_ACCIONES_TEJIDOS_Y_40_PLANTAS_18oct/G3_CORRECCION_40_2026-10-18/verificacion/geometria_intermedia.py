from pathlib import Path
import pickle,math,json,sys
import numpy as np
from shapely.geometry import Point,Polygon,LineString,box
from shapely.affinity import rotate,translate,scale
from shapely.ops import unary_union
P=Path(__file__).resolve().parents[1]
OLD=P.parent/'G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA'
SOURCE=pickle.load(open(P/'datos/FUENTE_40_ANTERIOR.pkl' if (P/'datos/FUENTE_40_ANTERIOR.pkl').exists() else OLD/'datos/GEOMETRIA_3D.pkl','rb'))

def polys(g):
 return [g] if g.geom_type=='Polygon' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']
def tf(g,r):
 if r.get('mirror'):g=scale(g,xfact=-1,yfact=1,origin=(1.65,0))
 return translate(rotate(translate(g,-r['dc'],0),r['phi'],origin=(0,0)),*r['q'])
def pxy(x,y,r):return tf(Point(x,y),r).coords[0]
def wrap(a):return (a+180)%360-180

# Front wall is exactly straight. Organic sides grow from the wardrobe and window bay.
BASE=Polygon([(0,0),(3.3,0),(3.3,3.8),(3.27,4.02),(3.12,4.2),(.18,4.2),
              (.02,4.04),(-.08,3.8),(-.16,3.35),(-.17,2.8),(-.10,2.25),(0,1.8),(0,0)])
BAY=box(.65,4.08,2.95,5.05).buffer(.08,join_style=1)
ROOM=BASE.union(BAY)
BED=box(1.85,2.00,3.10,4.00)
DESK=box(.025,.25,1.825,1.15)
# Stool parked partly under the drawing board, with a separate use envelope in documentation.
CHAIR=Point(1.0,.94).buffer(.22,resolution=24)
WARD=Polygon([(0,2.0),(.55,2.0),(.53,2.3),(.42,2.7),(.40,3.0),(.49,3.4),(.55,3.7),(0,3.7)])
SEAT=box(.75,4.50,2.85,5.05)
ROOM_OBS=unary_union([BED,DESK,CHAIR,WARD,SEAT])

def program(variant):
 # A and B exchange the shared programme across the vertical axis; local bedroom handedness is independent.
 b1=box(-1.95,1.2,-.25,3.20);b2=box(-.10,1.2,1.60,3.20)
 screen=box(-1.95,.10,.50,.22)
 kitchen=box(2.85,-2.8,3.45,.40);fridge=box(2.80,.55,3.45,1.20)
 sofa=box(-3.15,-2.65,-2.30,-.85);table=box(-.50,-2.30,1.10,-1.45)
 stools=[Point(x,y).buffer(.21,resolution=20) for x in [-.20,.80] for y in [-2.66,-1.09]]
 closet=box(-1.95,.10,-1.35,.22)
 data={'baths':[b1,b2],'screen':screen,'kitchen':kitchen,'fridge':fridge,'sofa':sofa,'table':table,'stools':stools,'utility':closet}
 if variant=='B':
  data={k:[scale(g,xfact=-1,origin=(0,0)) for g in v] if isinstance(v,list) else scale(v,xfact=-1,origin=(0,0)) for k,v in data.items()}
 return data

def room_candidates(core,prog):
 obs=unary_union(prog['baths']+[prog[k] for k in ['screen','kitchen','fridge','sofa','table','utility']]+prog['stools'])
 out=[]
 for deg in np.arange(0,360,5):
  th=math.radians(deg);n=np.array([math.cos(th),math.sin(th)])
  ray=LineString([(0,0),tuple(n*12)])
  cut=ray.intersection(core)
  if cut.is_empty:continue
  end=max([p for p in getattr(cut,'geoms',[cut]) if p.geom_type=='LineString'],key=lambda x:x.length).coords[-1]
  radius=np.linalg.norm(end)+.12
  for mirror in [False,True]:
   r={'q':tuple(n*radius),'phi':float(deg-90),'dc':.75 if mirror else 2.55,'mirror':mirror,'bearing':float(deg)}
   room=tf(ROOM,r)
   if room.intersection(obs).area>.0001:continue
   approach=tf(box(2.0,-1.2,3.10,-.02),r)
   if not core.buffer(.001).covers(tf(box(2.05,-1.50,3.05,-.70),r)):continue
   if approach.intersection(obs).area>.0001:continue
   rays=tf(box(.70,5.14,2.90,11.20),r)
   if rays.intersection(core).area>.0001:continue
   r.update(poly=room,connector=tf(box(1.85,-1.50,3.25,.02),r),approach=approach,ray=rays,door=tf(box(2.05,-.22,3.05,.22),r),window=tf(box(.75,4.90,2.85,5.32),r))
   out.append(r)
 return out

def select_rooms(src,core,prog):
 cand=room_candidates(core,prog)
 center=np.mean([src['zones'][k].centroid.coords[0] for k in ['K','M','S','T','E']],axis=0)
 targets=[]
 for r in src['rooms']:
  v=np.array(r['poly'].centroid.coords[0])-center
  targets.append(math.degrees(math.atan2(v[1],v[0]))+({'N19B':12.0}.get(src['code'],0)))
 # Enumerate compatible sets before assigning bedroom identities; avoid pruning all valid four-room sets.
 import itertools
 bad=set()
 for i,a in enumerate(cand):
  for j,b in enumerate(cand[i+1:],i+1):
   if a['poly'].buffer(.13).intersects(b['poly'].buffer(.13)) or a['poly'].intersects(b['approach']) or b['poly'].intersects(a['approach']) or a['ray'].intersects(b['poly']) or b['ray'].intersects(a['poly']):bad.add((i,j))
 best=None
 for ids in itertools.combinations(range(len(cand)),4):
  if any((i,j) in bad for i,j in itertools.combinations(ids,2)):continue
  try:
   candidate_rooms=[cand[j] for j in ids];candidate_floor=unary_union([core]+[r['poly'] for r in candidate_rooms]+[r['connector'] for r in candidate_rooms]);en=entry(candidate_floor,candidate_rooms,prog,core,src)
   candidate_floor=candidate_floor.union(en['pad'])
   if len(common_windows(candidate_floor,unary_union([r['poly'] for r in candidate_rooms]),prog,en))<2:continue
  except RuntimeError:continue
  for perm in itertools.permutations(ids):
   cost=sum((wrap(cand[j]['bearing']-targets[i])/45)**2 for i,j in enumerate(perm))
   if best is None or cost<best[0]:best=(cost,perm)
 if best is None:raise RuntimeError((src['code'],'no four exterior rooms',len(cand)))
 return [dict(cand[j],id='H'+str(i+1),source_bearing=targets[i]) for i,j in enumerate(best[1])],best[0],len(cand)

def entry(floor,rooms,prog,core,src):
 obs=unary_union([r['poly'] for r in rooms]+prog['baths']+[prog[k] for k in ['screen','kitchen','fridge','sofa','table','utility']]+prog['stools'])
 candidates=[]
 for deg in range(0,360,3):
  th=math.radians(deg);n=np.array([math.cos(th),math.sin(th)])
  hit=LineString([(0,0),tuple(n*10)]).intersection(core)
  if hit.geom_type!='LineString':continue
  q=np.array(hit.coords[-1])-n*.65
  r={'q':tuple(q),'phi':deg-90,'dc':0,'mirror':False}
  pad=tf(box(-.80,-.70,.80,1.40),r)
  inside=tf(box(-.45,-1.00,.45,.4),r)
  if pad.intersection(obs).area>.0001 or inside.intersection(obs).area>.0001:continue
  if not core.covers(tf(box(-.45,-.9,.45,-.35),r)):continue
  exterior=tf(box(-.55,1.41,.55,4),r)
  if exterior.intersection(floor).area>.001:continue
  candidates.append((abs(wrap(deg-math.degrees(math.atan2(src['arrival'].centroid.y,src['arrival'].centroid.x)))),r,pad))
 if not candidates:raise RuntimeError((src['code'],'no clear main entry'))
 _,r,pad=min(candidates,key=lambda x:x[0]);r['pad']=pad;r['door']=tf(box(-.62,1.20,.62,1.60),r)
 return r

def common_windows(floor,private,prog,entry):
 windows=[];ring=list(floor.exterior.coords)
 blocked=private.union(unary_union(prog['baths'])).buffer(.2).union(entry['pad'].buffer(.2))
 for a,b in zip(ring,ring[1:]):
  line=LineString([a,b]);length=line.length
  if length<1.00:continue
  mid=line.interpolate(.5,normalized=True);v=np.array(b)-np.array(a);v/=np.linalg.norm(v);n=np.array([-v[1],v[0]])
  if floor.contains(Point(np.array(mid.coords[0])+n*.05)):n=-n
  q=np.array(mid.coords[0]);w=min(1.70,length-.12)
  strip=Polygon([q-v*w/2-n*.2,q+v*w/2-n*.2,q+v*w/2+n*3,q-v*w/2+n*3])
  if strip.intersection(blocked).area>.001:continue
  outward=Polygon([q-v*w/2+n*.20,q+v*w/2+n*.20,q+v*w/2+n*3,q-v*w/2+n*3])
  if outward.intersection(floor).area>.001:continue
  windows.append({'q':tuple(q),'t':tuple(v),'n':tuple(n),'width':w,'cut':Polygon([q-v*w/2-n*.20,q+v*w/2-n*.20,q+v*w/2+n*.30,q-v*w/2+n*.30])})
 return windows

def build(src):
 idx=int(src['code'][1:3])-1
 # Small deformations are computed from action positions, rather than a random contour.
 pts=np.array([src['zones'][k].centroid.coords[0] for k in ['K','M','S','T','R','E']]);std=np.std(pts,axis=0)
 sx=1+float(np.clip((std[0]-std[1])*.004,0,.015));sy=1+float(np.clip((std[1]-std[0])*.004,0,.015))
 core=box(-2.85,-2.60,2.85,2.60).buffer(.65,resolution=24)
 core=scale(core,xfact=sx,yfact=sy,origin=(0,0))
 prog=program(src['variant'])
 # Keep the actual technical programme wholly inside the shared floor.
 core=core.union(unary_union(prog['baths']+[prog['utility'],prog['kitchen'],prog['fridge']]).buffer(.12,join_style=1)).buffer(.08).buffer(-.08)
 rooms,cost,nc=select_rooms(src,core,prog)
 private=unary_union([r['poly'] for r in rooms]);floor=unary_union([core,private]+[r['connector'] for r in rooms]).buffer(.12).buffer(-.12)
 if floor.geom_type!='Polygon':raise RuntimeError('disconnected')
 if floor.interiors:floor=Polygon(floor.exterior)
 ent=entry(floor,rooms,prog,core,src);floor=floor.union(ent['pad'])
 if floor.interiors:floor=Polygon(floor.exterior)
 windows=common_windows(floor,private,prog,ent)
 walls=floor.buffer(.12,join_style=1).difference(floor)
 for r in rooms:walls=walls.union(r['poly'].boundary.buffer(.06,cap_style=2,join_style=1))
 for b in prog['baths']:walls=walls.union(b.buffer(.075,join_style=2).difference(b))
 walls=walls.union(prog['screen'])
 ret=box(-1.95,.10,-1.83,1.25)
 if src['variant']=='B':ret=scale(ret,xfact=-1,origin=(0,0))
 walls=walls.union(ret)
 cuts=[r['door'] for r in rooms]+[ent['door']]
 bathdoors=[]
 for b in prog['baths']:
  x,y,X,Y=b.bounds;bd=box(x+.55,y-.20,x+1.45,y+.20);cuts.append(bd);bathdoors.append(bd)
 wincuts=[r['window'] for r in rooms]
 return {'code':src['code'],'variant':src['variant'],'family':src['family'],'core':core,'floor':floor,'rooms':rooms,'private':private,'program':prog,'entry':ent,'walls':walls,'doors':unary_union(cuts),'bathdoors':bathdoors,'wincuts':unary_union(wincuts),'common_windows':windows,'source_cost':cost,'source_area':src['floor3d'].area,'candidates':nc}

def audit(d):
 rooms=d['rooms'];pr=d['program'];floor=d['floor'];walls=d['walls'].difference(d['doors'])
 furniture=unary_union([pr[k] for k in ['screen','kitchen','fridge','sofa','table','utility']]+pr['baths']+pr['stools'])
 walkfloor=floor.union(tf(box(-.8,1.35,.8,2.75),d['entry']))
 public=walkfloor.difference(unary_union([d['private'],walls,furniture])).buffer(-.45)
 pts=[tf(Point(2.55,-.65),r) for r in rooms]+[tf(Point(0,1.0),d['entry'])]
 comps=polys(public);connected=any(all(c.buffer(.001).contains(p) for p in pts) for c in comps)
 privatechecks=[]
 for r in rooms:
  walk=tf(ROOM.difference(ROOM_OBS),r).difference(walls).buffer(-.40)
  points=[tf(Point(*p),r) for p in [(2.55,.65),(1.1,2.7),(1.15,4.05),(2.3,1.36),(1.1,1.63)]]
  ok=any(all(c.buffer(.001).contains(p) for p in points) for c in polys(walk))
  outer_clear=r['ray'].difference(r['poly']).intersection(floor).area<.001
  doorstraight=LineString([pxy(2.05,0,r),pxy(3.05,0,r)]).difference(r['poly'].boundary.buffer(.001)).length<.001
  privatechecks.append({'id':r['id'],'area_m2':round(r['poly'].area,2),'circulation_d080':ok,'window_outward_strip_clear_6m':outer_clear,'straight_door_segment_1000mm':doorstraight})
 return {'code':d['code'],'old_floor_m2':round(d['source_area'],2),'new_floor_m2':round(floor.area,2),'gross_envelope_m2':round(floor.buffer(.12).area,2),'private_each_m2':round(ROOM.area,2),'public_d090_connected':connected,'common_exterior_windows':len(d['common_windows']),'rooms':privatechecks,'holes':len(floor.interiors),'room_overlap_m2':sum(a['poly'].intersection(b['poly']).area for i,a in enumerate(rooms) for b in rooms[i+1:])}

if __name__=='__main__':
 codes=set(sys.argv[1:]);data=[];reports=[]
 for src in SOURCE:
  if codes and src['code'] not in codes:continue
  d=build(src);data.append(d);report=audit(d);reports.append(report);print(json.dumps(report),flush=True)
 pickle.dump(data,open(P/'datos'/('GEOMETRIA_MUESTRA.pkl' if codes else 'GEOMETRIA_CORREGIDA.pkl'),'wb'))
 (P/'verificacion/ESPACIO.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
