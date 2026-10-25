from pathlib import Path
import pickle,json,math,heapq
import numpy as np
from shapely.geometry import Point,LineString,box,Polygon
from shapely.ops import unary_union,nearest_points
from shapely.affinity import rotate,translate
from shapely import contains_xy
P=Path(__file__).resolve().parents[1];ROOT=P.parent
D=pickle.load(open(ROOT/'G3_TEJIDOS_A_PLANTA_40_2026-10-18/datos/geometrias.pkl','rb'))
def xf(g,r):return translate(rotate(translate(g,-1.05,0),r['angle'],origin=(0,0)),*r['door'])
def poly(g):return [g] if g.geom_type=='Polygon' else [x for x in g.geoms if x.geom_type=='Polygon']
def smooth(line,rad=.9):
 pts=np.array(line.simplify(.22).coords);out=[pts[0]]
 for j in range(1,len(pts)-1):
  a,b,c=pts[j-1],pts[j],pts[j+1];u=a-b;v=c-b;lu=np.linalg.norm(u);lv=np.linalg.norm(v)
  if min(lu,lv)<1e-5:continue
  cut=min(rad,lu*.4,lv*.4);s=b+u/lu*cut;e=b+v/lv*cut;out.append(s)
  for t in np.linspace(0,1,9)[1:]:out.append((1-t)**2*s+2*(1-t)*t*b+t*t*e)
 out.append(pts[-1]);return LineString(out)
reports=[]
for d in D:
 for r in d['rooms']:
  base=box(.35,.35,3.85,4.05).buffer(.35,resolution=16)
  niche=Point(0,3.0).buffer(1.45,resolution=40).intersection(box(-1.6,1.5,.05,4.5))
  bay=box(1.05,4.25,3.90,5.35).buffer(.12,join_style=1).intersection(box(.9,4.2,4.05,5.47))
  local=unary_union([base,niche,bay]);r['local3d']=local;r['poly']=xf(local,r)
  r['bed']=xf(Point(2.85,3.15).buffer(1.05,resolution=64) if d['variant']=='A' else box(2.45,2.15,3.7,4.15),r)
  clothes=Point(0,3.0).buffer(1.35,resolution=40).difference(Point(0,3.0).buffer(.85,resolution=40)).intersection(box(-1.5,1.5,0,4.5));r['ward']=xf(clothes,r);r['desk']=xf(box(2.4,.25,4.2,1.15),r);r['chair']=xf(Point(3.25,1.65).buffer(.22),r)
  r['window']=[tuple(xf(Point(x,5.47),r).coords)[0] for x in [1.15,3.8]]
 private=unary_union([r['poly'] for r in d['rooms']]);ob=unary_union([private]+[it['poly'] for it in d['items']]+[d['task'],d['dry']])
 routes=[];usedr=[]
 for original in d['routes']:
  best=original
  for rad in [1.2,.9,.6,.3]:
   q=smooth(original,rad)
   # A smooth centreline must keep at least .50m from modeled solids except at shared-zone terminals.
   if q.buffer(.49).intersection(ob).area<.01:best=q;break
  routes.append(best);usedr.append(best.equals(original))
 # Widen/smooth connections rather than keep the jagged route lattice as a wall.
 network=unary_union([g.buffer(.90,resolution=20,cap_style=1,join_style=1) for g in routes])
 common=d['shared'].union(network).buffer(.30,resolution=16,join_style=1).buffer(-.30,resolution=16,join_style=1)
 floor=common.union(private).buffer(.0001).buffer(-.0001);shared=floor.difference(private)
 d['rooms3d']=d['rooms'];d['floor3d']=floor;d['shared3d']=shared;d['routes3d']=routes
 # Walls lie outside useful room outlines; never shrink them to insert thickness.
 walls=floor.buffer(.12,join_style=1).difference(floor)
 for r in d['rooms']:walls=walls.union(r['poly'].buffer(.12).difference(r['poly']))
 for it in d['items']:
  if it['name'].startswith('B'):walls=walls.union(it['poly'].buffer(.10,join_style=2).difference(it['poly']))
 doors=[];windows=[]
 for r in d['rooms']:
  doors.append(xf(box(.45,-.3,1.55,.30),r));windows.append(xf(box(1.15,5.25,3.80,5.70),r))
 for it in d['items']:
  if it['name'].startswith('B'):x,y,X,Y=it['poly'].bounds;doors.append(box(x+.55,y-.25,x+1.55,y+.25))
 # Entry snapped to the remodelled outer boundary near the previous entry.
 q=nearest_points(d['arrival'],floor.boundary)[1];boundary=min([p.exterior for p in poly(floor)],key=lambda ring:ring.distance(q));t=boundary.project(q);a=boundary.interpolate(max(0,t-.2));b=boundary.interpolate(min(boundary.length,t+.2));ang=math.degrees(math.atan2(b.y-a.y,b.x-a.x));d['entry3d']=(q.x,q.y,ang)
 doors.append(translate(rotate(box(-.75,-.4,.75,.4),ang,origin=(0,0)),q.x,q.y));doorcuts=unary_union(doors);wincuts=unary_union(windows)
 d['walls3d']=walls;d['doors3d']=doorcuts;d['windows3d']=wincuts
 # Physical obstacles include walls, expanded storage, seating and common chairs.
 obstacles=[walls.difference(doorcuts)]+[r[k] for r in d['rooms'] for k in ['bed','desk','ward']]+[it['poly'] for it in d['items'] if not it['name'].startswith('B')]+[it['poly'].boundary.buffer(.1) for it in d['items'] if it['name'].startswith('B')]+[d['task'],d['dry']]
 for r in d['rooms']:obstacles.append(xf(box(1.08,5.0,3.88,5.40),r))
 # Check full private door -> desk approach / bedside / wardrobe / bay using a 0.80m body envelope.
 checks=[]
 for r in d['rooms']:
  usable=r['poly'].difference(unary_union([r['bed'],r['desk'],r['ward'],xf(box(1.08,5.0,3.88,5.40),r)]));walk=usable.buffer(-.40)
  components=poly(walk);pts=[xf(Point(*xy),r) for xy in [(1.05,.65),(3.25,1.65),(1.2,2.8),(-.25,3.0),(1.5,4.50)]]
  counts=[sum(c.distance(p)<.12 for p in pts) for c in components];ok=max(counts+[0])==len(pts)
  landing=xf(Point(1.05,1.05).buffer(.70),r);obs=unary_union([r['bed'],r['desk'],r['ward']]);clear=landing.intersection(obs).area<1e-5
  checks.append({'room':r['id'],'five_use_points_connected_d080':ok,'landing_d140_clear':clear,'bed_desk_overlap_m2':r['bed'].intersection(r['desk']).area,'bed_clothes_overlap_m2':r['bed'].intersection(r['ward']).area})
 d['audit3d']=checks;reports.append({'code':d['code'],'old_floor_m2':round(d['floor'].area,2),'floor3d_m2':round(floor.area,2),'floor_z':0,'rooms':checks,'routes_not_smoothed':sum(usedr)})
 print(d['code'],checks,flush=True)
pickle.dump(D,open(P/'datos/GEOMETRIA_3D.pkl','wb'));(P/'verificacion/ESPACIO.json').write_text(json.dumps(reports,indent=2));print('PREPARADO_40',flush=True)
