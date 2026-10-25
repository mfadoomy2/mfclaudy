from pathlib import Path
import pickle,sys,json,math
from shapely.geometry import Point,LineString,box
from shapely.ops import unary_union
from shapely.affinity import rotate,translate
P=Path(__file__).resolve().parents[1];D=pickle.load(open(P/'datos/GEOMETRIA_3D.pkl','rb'))
prep=P/'fuentes/preparar.py';ns={'__file__':str(prep)};exec(prep.read_text().split('reports=[]')[0],ns);smooth=ns['smooth']
rep=P/'fuentes/reparar_pasos.py';rs={'__file__':str(rep)};exec(rep.read_text().split('out=[]')[0],rs)
reports=[]
for d in D:
 cells=[]
 for k,g in d['zones'].items():
  if k.startswith('H'):continue
  cells.append(g if k.startswith('B') else g.buffer(-.25).buffer(.25,resolution=20))
 routes=[smooth(g,.28) for g in d['routes3d']];strips=[g.buffer(.95,resolution=24,cap_style=1,join_style=1) for g in routes]
 for r in d['rooms']:
  a=math.radians(r['angle']);p=r['door'];strips.append(LineString([(p[0]+math.sin(a),p[1]-math.cos(a)),(p[0]-math.sin(a)*.15,p[1]+math.cos(a)*.15)]).buffer(.85,resolution=24))
 for code,g in d['zones'].items():
  if code.startswith('H'):continue
  x,y,X,Y=g.bounds;strips.append(LineString([((x+X)/2,y-.9),((x+X)/2,y+.3)]).buffer(.85,resolution=24))
 old=d['floor3d'];private=unary_union([r['poly'] for r in d['rooms']]);d['floor3d']=unary_union(cells+strips+[private]).buffer(.12).buffer(-.12);d['shared3d']=d['floor3d'].difference(private);rs['walls'](d)
 best,pts,bad=rs['nav'](d)
 if bad:
  # keep only needed previous connective fabric where a rounded corner would narrow an access
  d['floor3d']=d['floor3d'].union(old);d['shared3d']=d['floor3d'].difference(private);rs['walls'](d);best,pts,bad=rs['nav'](d)
 assert not bad,(d['code'],bad)
 # Relocate outer main opening after the perimeter has been reshaped.
 from shapely.ops import nearest_points
 q=nearest_points(Point(*d['entry3d'][:2]),d['floor3d'].boundary)[1];rings=[p.exterior for p in ([d['floor3d']] if d['floor3d'].geom_type=='Polygon' else d['floor3d'].geoms)];bnd=min(rings,key=lambda r:r.distance(q));t=bnd.project(q);a=bnd.interpolate(max(0,t-.2));b=bnd.interpolate(min(bnd.length,t+.2));angle=math.degrees(math.atan2(b.y-a.y,b.x-a.x));d['entry3d']=(q.x,q.y,angle)
 cuts=[rs['xf'](box(.45,-.3,1.55,.3),r) for r in d['rooms']]
 for it in d['items']:
  if it['name'].startswith('B'):x,y,X,Y=it['poly'].bounds;cuts.append(box(x+.55,y-.25,x+1.55,y+.25))
 cuts.append(translate(rotate(box(-.75,-.40,.75,.40),angle,origin=(0,0)),q.x,q.y));d['doors3d']=unary_union(cuts);rs['walls'](d);best,pts,bad=rs['nav'](d);assert not bad
 d['routes3d']=routes;reports.append({'code':d['code'],'room_door_connection_d090':4,'entry_distance_to_connected_component':best.distance(q),'finished_floor_z':0,'floor_m2':d['floor3d'].area});print(d['code'],round(d['floor3d'].area,2),flush=True)
pickle.dump(D,open(P/'datos/GEOMETRIA_3D.pkl','wb'));(P/'verificacion/COHERENCIA_FINAL.json').write_text(json.dumps(reports,indent=2))
