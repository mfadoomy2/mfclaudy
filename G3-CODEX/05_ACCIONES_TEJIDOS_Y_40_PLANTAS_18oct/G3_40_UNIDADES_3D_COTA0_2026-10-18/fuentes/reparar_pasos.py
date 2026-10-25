from pathlib import Path
import pickle,sys,json,math
from shapely.geometry import Point,LineString,box
from shapely.ops import unary_union,nearest_points
from shapely.affinity import rotate,translate
P=Path(__file__).resolve().parents[1];D=pickle.load(open(P/'datos/GEOMETRIA_3D.pkl','rb'));src=P.parent/'G3_TEJIDOS_A_PLANTA_40_2026-10-18/fuentes/tejido_planta.py';sys.path.insert(0,str(src.parent));g={'__file__':str(src)};exec(src.read_text().split('plans=[];reports=[]')[0],g);astar=g['astar']
def polys(g):return [g] if g.geom_type=='Polygon' else [p for p in g.geoms if p.geom_type=='Polygon']
def xf(geom,r):return translate(rotate(translate(geom,-1.05,0),r['angle'],origin=(0,0)),*r['door'])
def nav(d):
 obs=unary_union([d['walls3d'].difference(d['doors3d'])]+[r[k] for r in d['rooms'] for k in ['bed','desk','ward']]+[xf(box(1.08,5,3.88,5.40),r) for r in d['rooms']]+[it['poly'] for it in d['items'] if not it['name'].startswith('B')]+[d['task'],d['dry']])
 walk=d['floor3d'].difference(obs).buffer(-.45);cs=polys(walk);pts=[xf(Point(1.05,.65),r) for r in d['rooms']];best=max(cs,key=lambda c:sum(c.distance(p)<.05 for p in pts));return best,pts,[c for c,p in enumerate(pts) if best.distance(p)>.05]
def walls(d):
 fl=d['floor3d'];w=fl.buffer(.12).difference(fl)
 for r in d['rooms']:w=w.union(r['poly'].buffer(.12).difference(r['poly']))
 for it in d['items']:
  if it['name'].startswith('B'):w=w.union(it['poly'].buffer(.10,join_style=2).difference(it['poly']))
 d['walls3d']=w
out=[]
for d in D:
 private=unary_union([r['poly'] for r in d['rooms']]);solids=unary_union([private]+[it['poly'] for it in d['items']]+[d['task'],d['dry']]);fixes=0
 for it in range(7):
  best,pts,bad=nav(d)
  if not bad:break
  candidates=best.difference(solids.buffer(.95));bounds=d['floor3d'].buffer(4).bounds
  for j in bad:
   r=d['rooms'][j];a=math.radians(r['angle']);probe=Point(r['door'][0]+math.sin(a),r['door'][1]-math.cos(a))
   if probe.distance(solids)<.72:
    dx=-math.sin(a)*1.6;dy=math.cos(a)*1.6
    for key in ['poly','bed','desk','chair','ward']:r[key]=translate(r[key],dx,dy)
    r['door']=(r['door'][0]+dx,r['door'][1]+dy);r['window']=[(x+dx,y+dy) for x,y in r['window']]
    private=unary_union([rr['poly'] for rr in d['rooms']]);solids=unary_union([private]+[ii['poly'] for ii in d['items']]+[d['task'],d['dry']]);d['floor3d']=d['floor3d'].union(private)
    cuts=[xf(box(.45,-.30,1.55,.30),rr) for rr in d['rooms']]
    for ii in d['items']:
     if ii['name'].startswith('B'):x,y,X,Y=ii['poly'].bounds;cuts.append(box(x+.55,y-.25,x+1.55,y+.25))
    ex,ey,ea=d['entry3d'];cuts.append(translate(rotate(box(-.75,-.4,.75,.4),ea,origin=(0,0)),ex,ey));d['doors3d']=unary_union(cuts);d['windows3d']=unary_union([xf(box(1.15,5.25,3.8,5.70),rr) for rr in d['rooms']]);walls(d)
    bounds=d['floor3d'].buffer(5).bounds;candidates=best.difference(solids.buffer(.95));fixes+=1
   start=Point(r['door'][0]+math.sin(a)*1.0,r['door'][1]-math.cos(a)*1.0);q=nearest_points(start,candidates)[1];route=astar((start.x,start.y),(q.x,q.y),solids.buffer(.69),bounds);path=route.buffer(1.05,cap_style=1,join_style=1);d['floor3d']=d['floor3d'].union(path).buffer(.0001).buffer(-.0001);d['routes3d'].append(route);fixes+=1
  d['shared3d']=d['floor3d'].difference(private);walls(d)
 best,pts,bad=nav(d);assert not bad,(d['code'],bad)
 overlap=sum(d['rooms'][i]['poly'].intersection(d['rooms'][j]['poly']).area for i in range(4) for j in range(i));assert overlap<.001
 out.append({'code':d['code'],'connected_room_inside_d090':4,'private_overlap_m2':overlap,'local_repairs':fixes,'entry_distance_to_connected_component':best.distance(Point(*d['entry3d'][:2]))});print(d['code'],fixes,flush=True)
pickle.dump(D,open(P/'datos/GEOMETRIA_3D.pkl','wb'));(P/'verificacion/RECORRIDOS.json').write_text(json.dumps(out,indent=2));print('40_CON_PASOS_REVISADOS',flush=True)
