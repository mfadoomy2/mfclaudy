from pathlib import Path
import json, math
import numpy as np
from shapely.geometry import shape,box,LineString,Polygon
from shapely.ops import unary_union,triangulate
from shapely.affinity import translate,rotate
R=Path(__file__).resolve().parents[1]
SRC=Path('/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_HABITADA_V2_2026-10-16/fuentes/geometria')
site=shape(json.loads((SRC/'parcela_local.geojson').read_text())['geometry'])
def rb(x,y,w,h,r=.55):return box(x+r,y+r,x+w-r,y+h-r).buffer(r,quad_segs=12)
rooms=[rb(0,0,3.7,3.8),rb(6.6,0,3.7,3.8),rb(0,5.4,3.7,3.8),rb(6.6,5.4,3.7,3.8)]
foot=unary_union(rooms+[box(3.7,0,6.6,9.2),box(0,3.8,10.3,5.4)])
def polygons(p):return [p] if p.geom_type=='Polygon' else [q for q in getattr(p,'geoms',[]) if q.geom_type=='Polygon']
def encode(p):
 a=[]
 for q in polygons(p):
  if q.area<1e-6:continue
  a.append({'outer':list(q.exterior.coords),'holes':[list(r.coords) for r in q.interiors],'triangles':[list(t.exterior.coords)[:3] for t in triangulate(q) if q.covers(t)],'area':q.area})
 return a
units=[];decks=[];terraces=[];paths=[]
levels=[3.8,7.8,11.8,15.8,19.8]
for k,z in enumerate(levels):
 items=[]
 for j in range(2):
  x=([20.0,20.6,19.9,20.5,20.1][k] if j==0 else [32.0,32.5,32.1,32.7,32.3][k])
  y=([-3.5,-2.1,-3.1,-1.9,-2.8][k] if j==0 else [-4.6,-4.7,-4.8,-4.7,-4.65][k])
  ang=([-3.0,3.5,-2,3,-2.5][k] if j==0 else [-1,1.2,-1.4,.8,-1][k])
  def tr(p):return translate(rotate(p,ang,origin=(5.15,4.6)),xoff=x,yoff=y)
  # Fit by reducing the small rotation and shifting, preserving room dimensions.
  pp=tr(foot)
  for _ in range(25):
   if pp.difference(site).area<1e-7:break
   ang*=.8;y-=.035;pp=tr(foot)
  assert pp.difference(site).area<1e-6
  th=math.radians(ang)
  def pt(a,b):return [x+5.15+(a-5.15)*math.cos(th)-(b-4.6)*math.sin(th), y+4.6+(a-5.15)*math.sin(th)+(b-4.6)*math.cos(th)]
  zz=z+(.6 if j else 0)
  u={'id':'U%02d'%(2*k+j+1),'x':x,'y':y,'z':zz,'angle':ang,'foot':encode(pp),'entry':pt(0 if j==0 else 10.3,4.6),'side':j,'accessible':k==0 and j==0}
  u['rooms']=[encode(tr(q)) for q in rooms]
  units.append(u);items.append(pp)
  terr=pp.buffer(.48,join_style=1).intersection(site).difference(pp)
  terraces.append({'unit':u['id'],'z':zz,'shape':encode(terr)})
 main=LineString([(18.6,-5.9),(23.0,-6.0),(28,-6.15),(32,-6.3),(37,-6.1),(42,-5.9),(45,-5.4),(49,-5),(54,-4.5)])
 shape_g=main.buffer(.96,cap_style=2,join_style=1)
 branches=[]
 for u in units[-2:]:
  ex,ey=u['entry']
  x=ex-1.02 if u['side']==0 else ex+1.02
  line=LineString([(x,-5.85 if u['side']==0 else -5.2),(x,ey),(ex,ey)])
  branches.append(line);shape_g=unary_union([shape_g,line.buffer(.90,cap_style=2,join_style=1)])
 # Lift/stair landing approach, all at left level.
 shape_g=unary_union([shape_g,box(17.1,-4.55,19.45,-2.65),LineString([(18.6,-3.1),(19,-2),(units[-2]['entry'][0]-1.02,units[-2]['entry'][1])]).buffer(.9,cap_style=2)])
 for pp in items:shape_g=shape_g.difference(pp)
 shape_g=shape_g.intersection(site)
 pieces=[]
 for a,b in [(-100,26),(26,40),(40,100)]:pieces.extend(encode(shape_g.intersection(box(a,-100,b,100))))
 decks.append({'level':k,'z_left':z,'z_right':z+.6,'shape':pieces})
 paths.append({'level':k,'main':list(main.coords),'branches':[list(t.coords) for t in branches]})
# Community rooms remain separate from homes; the narrow tail is for services and connection.
program=[]
for k,z in [(0,0),(1,4.4),(2,12.4),(3,20.4)]:
 p=box(45.8,-3.7,52.8,1.2).intersection(site)
 program.append({'id':['CUIDADOS_LAVADO','CANTINA','TALLER','AULA'][k],'z':z,'shape':encode(p),'area':p.area})
# Site/context cache for native rendering, without touching originals.
ctx=np.load(SRC/'contexto.npz');tri=ctx['tri'];ids=ctx['ids'];context=[]
for id in sorted(set(ids)):
 ts=tri[ids==id];cent=ts.reshape(-1,3).mean(0)
 if -8<cent[0]<78 and -28<cent[1]<35:
  context.append({'id':id,'vertices':ts.reshape(-1,3).tolist()})
# Conservative floor-area inventory: counts horizontal stair projections, lift shafts and all outdoor floors.
core_front=box(13.9,-6.9,19.25,.9).area
core_rear=box(54.0,-5.9,57.2,.6).area
areas={'unidades_brutas':10*foot.area,'programa_comunitario':sum(p['area'] for p in program),'galerias_abiertas':sum(sum(p['area'] for p in q['shape']) for q in decks),'terrazas_unidades':sum(sum(p['area'] for p in q['shape']) for q in terraces),'nucleos_reserva_maxima':6*(core_front+core_rear)}
areas['total_con_reserva_maxima']=sum(areas.values())
a={'site':encode(site),'site_area':site.area,'unit_area':foot.area,'unit_foot':encode(foot),'room_local':[encode(p) for p in rooms],'units':units,'decks':decks,'terraces':terraces,'paths':paths,'program':program,'context':context,'areas':areas,'levels':levels,'people_source':'/Volumes/T7/PERSONAS.3dm'}
(R/'fuentes/disposicion.json').write_text(json.dumps(a,separators=(',',':')))
(R/'verificacion/encaje.json').write_text(json.dumps({'people':40,'units':len(units),'outside_unit_area':sum(sum(p['area'] for p in u['foot'])-Polygon(u['foot'][0]['outer']).intersection(site).area for u in units),'areas':areas,'levels_left':levels,'levels_right':[z+.6 for z in levels]},indent=2))
print('SPEC',len(units),'unit area',foot.area,'AREAS',areas)
