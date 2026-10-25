from pathlib import Path
import pickle,json,math
from shapely.geometry import Point,box
from shapely.ops import unary_union
from shapely.affinity import rotate,translate
P=Path(__file__).resolve().parents[1];D=pickle.load(open(P/'datos/GEOMETRIA_3D.pkl','rb'));reports=[]
def xf(g,r):return translate(rotate(translate(g,-1.05,0),r['angle'],origin=(0,0)),*r['door'])
def ps(g):return [g] if g.geom_type=='Polygon' else [p for p in g.geoms if p.geom_type=='Polygon']
for d in D:
 furniture=[r[k] for r in d['rooms'] for k in ['bed','desk','ward']]+[xf(Point(3.25,1.65).buffer(.23),r) for r in d['rooms']]+[xf(box(1.08,5,3.88,5.40),r) for r in d['rooms']]+[xf(box(1.6,.025,2.7,.07),r) for r in d['rooms']]+[xf(box(3.85,1.82,4.2,2.18),r) for r in d['rooms']]+[it['poly'] for it in d['items'] if not it['name'].startswith('B')]+[d['task'],d['dry']]
 table=next(it['poly'] for it in d['items'] if it['name']=='M');x,y,X,Y=table.bounds
 for xx in [x+.4,X-.4]:
  for yy in [y-.34,Y+.34]:furniture.append(Point(xx,yy).buffer(.23))
 obstacles=unary_union(furniture+[d['walls3d'].difference(d['doors3d'])]);walk=d['floor3d'].difference(obstacles).buffer(-.45);comps=ps(walk);entrypts=[xf(Point(1.05,.65),r) for r in d['rooms']];component=max(comps,key=lambda c:sum(c.distance(q)<.05 for q in entrypts));connected=sum(component.distance(q)<.05 for q in entrypts)
 rooms=[]
 for r in d['rooms']:
  obs=unary_union([r['bed'],r['desk'],r['ward'],xf(Point(3.25,1.65).buffer(.23),r),xf(box(1.08,5,3.88,5.40),r),xf(box(1.6,.025,2.7,.07),r),xf(box(3.85,1.82,4.2,2.18),r)])
  free=r['poly'].difference(obs).buffer(-.40);cc=ps(free);pts=[xf(Point(*p),r) for p in [(1.05,.65),(2.5,1.60),(1.2,2.8),(-.25,3),(1.5,4.5)]];n=max([sum(c.distance(q)<.10 for q in pts) for c in cc]+[0]);rooms.append({'room':r['id'],'five_approaches_connected_body080':n==5,'clear_entry_landing_d140':obs.intersection(xf(Point(1.05,1.05).buffer(.7),r)).area<1e-5})
 reports.append({'code':d['code'],'floor_z':0,'area_m2':round(d['floor3d'].area,2),'four_bedrooms_connected_body090':connected==4,'entry_to_component_distance_m':component.distance(Point(*d['entry3d'][:2])),'rooms':rooms})
assert len(reports)==40;assert all(r['four_bedrooms_connected_body090'] and all(q['five_approaches_connected_body080'] and q['clear_entry_landing_d140'] for q in r['rooms']) for r in reports)
(P/'verificacion/AUDITORIA_FINAL_ESPACIO.json').write_text(json.dumps(reports,indent=2));print('40_UNIDADES_160_HABITACIONES_PASAN',min(r['area_m2'] for r in reports),max(r['area_m2'] for r in reports))
