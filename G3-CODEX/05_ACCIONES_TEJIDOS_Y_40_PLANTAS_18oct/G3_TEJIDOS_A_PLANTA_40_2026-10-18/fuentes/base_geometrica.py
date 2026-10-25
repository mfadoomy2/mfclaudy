from pathlib import Path
import math,json,csv,random,textwrap
import numpy as np
from shapely.geometry import Point,Polygon,box,LineString
from shapely.ops import unary_union,nearest_points,triangulate
from shapely.affinity import rotate,translate
from shapely.geometry.polygon import orient
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PatchPolygon,Rectangle,Circle,Arc
from matplotlib.path import Path as MP
from matplotlib.patches import PathPatch
P=Path(__file__).resolve().parents[1]
BG='#faf8f0';INK='#253d35';PINK='#c94088';CYAN='#179fa8';GOLD='#d4ae4e';ROOM='#dce8da';WET='#e5cee0';WOOD='#dfc591'
# door anchor x,y; room rotates from outward local +Y; hub network is circulation support only
F=[
('Dos orillas',[( -2.8,3,0),(2.8,3,0),(-2.8,-3,180),(2.8,-3,180)],[(0,0)],'Dos pares privados frente a una estancia continua.','Cruzar la sala puede exponer las entradas.'),
('Cruz ramificada',[(0,3.8,0),(3.8,0,-90),(0,-3.8,180),(-3.8,0,90)],[(0,0)],'Cuatro ramas con acceso desde un centro compartido.','La separación acústica depende de los umbrales.'),
('Peine abierto',[(0,0,0),(5.4,0,0),(10.8,0,0),(16.2,0,0)],[(0,-2.2),(5.4,-2.2),(10.8,-2.2),(16.2,-2.2)],'Habitaciones a un borde; cocina y estar a otro.','Longitud de recorridos y mucha fachada.'),
('Doble peine',[(0,2.8,0),(5.4,2.8,0),(2.7,-2.8,180),(8.1,-2.8,180)],[(0,0),(4,0),(8,0)],'Dos bordes desplazados; encuentros en los ensanchamientos.','Evitar que la conexión vuelva a ser un pasillo.'),
('Molinete',[( -2,3.8,0),(3.8,2,-90),(2,-3.8,180),(-3.8,-2,90)],[(0,0)],'Las entradas giran alrededor del estar.','Giros y vistas hacia puertas privadas.'),
('Codo doméstico',[(0,0,0),(5.4,0,0),(9,-4,-90),(9,-9.4,-90)],[(0,-2),(5,-2),(7,-5),(7,-9)],'Dos brazos conectados por cocina y estancia en el codo.','El extremo puede quedar demasiado alejado.'),
('Herradura',[( -5,0,90),(-2.8,5,0),(2.8,5,0),(5,0,-90)],[(0,0),(0,3)],'Vacío de llegada abierto entre dos alas.','Vigilar que el vacío no consuma el espacio común.'),
('Cadena oblicua',[(-6,3,35),(-2,-3,180),(4,3,-20),(8,-3,180)],[(-6,0),(-1,0),(4,0),(8,0)],'Cambios de dirección separan focos de actividad.','Recorridos sinuosos y piezas difíciles de construir.'),
('Dos racimos',[(-5,3,0),(-5,-3,180),(5,3,0),(5,-3,180)],[(-5,0),(0,0),(5,0)],'Dos parejas privadas con varios lugares de encuentro.','Puede duplicar superficie y reforzar grupos cerrados.'),
('Puente habitado',[(-7,2,55),(-7,-2,125),(7,2,-55),(7,-2,-125)],[(-6,0),(0,0),(6,0)],'Estar y cocinar se despliegan a lo largo de una conexión.','Longitud y dependencia de una conexión única.'),
('Corola asimétrica',[(0,4.2,0),(4.3,1.4,-70),(1.5,-4.3,160),(-4.3,-.6,100)],[(0,0)],'Ramas orientadas con ángulos diferentes.','No asumir que los giros mejoran la luz.'),
('Abanico', [(-5,2.8,45),(-1.8,4.8,15),(2.8,4.7,-15),(6,2.8,-45)],[(0,0),(3,0)],'Borde privado desplegado alrededor del ámbito común.','Mayor perímetro y posibles sombras entre alas.'),
('Archipiélago', [(-5,4,20),(5,4,-20),(-5,-4,160),(5,-4,200)],[(-2,0),(2,0),(0,2),(0,-2)],'Islas privadas con continuidades compartidas entre ellas.','Intersticios residuales si no admiten usos concretos.'),
('Espina en S',[(-5,3,30),(-2,-3,180),(3,5,-15),(7,-1,-120)],[(-5,0),(-1,0),(2,2),(6,2)],'El recorrido se ensancha y cambia de dirección.','Orientación y distancias menos intuitivas.'),
('Dos patios',[(-5,4,0),(5,4,0),(-5,-4,180),(5,-4,180)],[(-4,0),(4,0),(0,0)],'Dos vacíos dividen encuentro y concentración.','Los patios son hipótesis; su luz no está calculada.'),
('Cuatro umbrales',[(-3.4,3.8,10),(3.4,3.8,-10),(-3.4,-3.8,170),(3.4,-3.8,190)],[(-2,0),(2,0)],'Entradas retranqueadas hacia ámbitos comunes distintos.','Mucho espacio de transición si no se ocupa bien.'),
('Triángulo con bifurcación',[(-4,-2,130),(4,-2,-130),(-2.8,5,0),(2.8,5,0)],[(0,0),(0,2)],'Tres direcciones de estancia, una con pareja de habitaciones.','Jerarquía desigual entre las cuatro habitaciones.'),
('Zigzag',[(0,0,25),(5,-1,180),(10,2,0),(15,0,-160)],[(0,-2),(5,1),(10,-1),(15,2)],'Alternancia de retiros y lugares compartidos.','El recorrido puede crecer sin aportar estancia.'),
('Bandas permeables',[(-3,3,0),(3,3,0),(-6,-1,90),(6,-1,-90)],[(0,-1),(0,1)],'Una banda social y otra doméstica con cruces cortos.','Proteger el descanso respecto de los usos abiertos.'),
('Patio desplazado',[(-4,3,25),(3,5,-5),(-4,-4,155),(5,-3,-130)],[(-1,0),(2,1),(0,-2)],'Un vacío descentrado produce lugares de tamaños distintos.','No confundir irregularidad con buen aprovechamiento.')]

def xform(g,door,ang):return translate(rotate(translate(g,-1.05,0),ang,origin=(0,0)),door[0],door[1])
def pt(x,y,door,ang):p=xform(Point(x,y),door,ang);return (p.x,p.y)
def polygons(g):return [g] if g.geom_type=='Polygon' else [q for q in g.geoms if q.geom_type=='Polygon']
def rounded(w,h,r=.3):return box(r,r,w-r,h-r).buffer(r,resolution=10)
def private(room_id,door,ang,variant,style):
 # identical useful base; niche changes side/depth only where space supports it
 local=rounded(3.8,4.4,.25 if style%3==0 else .45)
 niche=Point(0,3.15).buffer(.9 if variant=='A' else 1.05,resolution=20).intersection(box(-1.2,1.8,0,4.4));local=local.union(niche)
 geom=xform(local,door,ang);bed=Point(2.55,3.15).buffer(1.05,resolution=36) if variant=='A' else box(2.05,2.15,3.3,4.15)
 desk=box(2,.25,3.8,1.15);chair=Point(2.85,1.62).buffer(.2,resolution=16);use=box(2.4,1.15,3.3,2.05)
 # wardrobe occupies outer arc, centre remains as approach; not certified walk-in
 r=.9 if variant=='A' else 1.05;outer=Point(0,3.15).buffer(r-.08).intersection(box(-1.2,1.8,0,4.4));inner=Point(0,3.15).buffer(max(.1,r-.45));ward=outer.difference(inner)
 return dict(id=room_id,door=door,angle=ang,local=local,poly=geom,bed=xform(bed,door,ang),desk=xform(desk,door,ang),chair=xform(chair,door,ang),use=xform(use,door,ang),ward=xform(ward,door,ang),window=[pt(1.25,4.4,door,ang),pt(3.45,4.4,door,ang)],doorline=[pt(.6,0,door,ang),pt(1.5,0,door,ang)],hinge=[pt(3.8,.25,door,ang),pt(3.8,1.15,door,ang)])

def reserve_routes(common,rooms):
 from collections import deque
 from shapely import contains_xy
 allowed=common.buffer(-.51)
 if allowed.is_empty:return None
 components=polygons(allowed)
 entries=[]
 for rr in rooms:
  a=math.radians(rr['angle']);d=rr['door'];entries.append(Point(d[0]+math.sin(a)*.8,d[1]-math.cos(a)*.8))
 co=max(components,key=lambda c:sum(c.distance(p)<.2 for p in entries))
 if sum(co.distance(p)<.2 for p in entries)<4:return None
 minx,miny,maxx,maxy=co.bounds;step=.27
 xs=np.arange(minx,maxx,step);ys=np.arange(miny,maxy,step)
 xx,yy=np.meshgrid(xs,ys);mask=contains_xy(co,xx,yy);valid=list(zip(*np.where(mask)))
 if not valid:return None
 def nearest(p):return min(valid,key=lambda ij:(xs[ij[1]]-p.x)**2+(ys[ij[0]]-p.y)**2)
 root=nearest(co.centroid);parents={root:None};q=deque([root])
 while q:
  i,j=q.popleft()
  for ni,nj in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
   if ni<0 or nj<0 or ni>=len(ys) or nj>=len(xs) or not mask[ni,nj] or (ni,nj) in parents:continue
   parents[(ni,nj)]=(i,j);q.append((ni,nj))
 routes=[]
 for e in entries:
  dest=nearest(e)
  if dest not in parents:return None
  pts=[(e.x,e.y)];cur=dest
  while cur is not None:pts.append((xs[cur[1]],ys[cur[0]]));cur=parents[cur]
  routes.append(LineString(pts).simplify(.03).buffer(.53,join_style=1))
 return unary_union(routes)

def choose_pack(common,targets,seed,reserved):
 rng=np.random.default_rng(seed);minx,miny,maxx,maxy=common.bounds;grid=[(x,y) for x in np.arange(minx,maxx,.55) for y in np.arange(miny,maxy,.55)];rng.shuffle(grid);occupied=[];items=[];inside=common.buffer(-.10);approachinside=common.buffer(.02)
 specs=[('B1',2.1,2.4),('B2',2.1,2.4),('K',3.6,.7),('F',.7,.7),('M',1.8,.9),('S',2.4,.85),('G',1.4,.5)]
 # reserve only actual furniture; positions evaluated for usable approaches and walkable connectivity later
 for name,w,h in specs:
  best=None;cost=1e12
  for rot in [0,90]:
   ww,hh=(w,h) if rot==0 else (h,w)
   for x,y in grid:
    g=box(x,y,x+ww,y+hh)
    if not inside.covers(g):continue
    if g.intersects(reserved):continue
    if any(g.buffer(.22).intersects(o) for o in occupied):continue
    # baths need approach outside its chosen south/west edge; counters .9 aisle; table seat zone
    if name.startswith('B'):approach=box(x+.55,y-.95,x+1.55,y+.02) if rot==0 else box(x-.95,y+.55,x+.02,y+1.55)
    elif name=='K':approach=box(x,y-.95,x+ww,y+.02) if rot==0 else box(x-.95,y,x+.02,y+hh)
    elif name=='M':approach=g.buffer(.6,join_style=2)
    elif name=='S':approach=box(x,y-.9,x+ww,y) if rot==0 else box(x-.9,y,x,y+hh)
    else:approach=g.buffer(.15)
    if not approachinside.covers(approach):continue
    if any(approach.intersects(o) for o in occupied):continue
    if any(g.intersects(it['approach']) for it in items):continue
    tx,ty=targets[name];d=(g.centroid.x-tx)**2+(g.centroid.y-ty)**2
    if name in ['K','B1','B2']:d+=g.centroid.distance(common.boundary)*1.5
    if d<cost:best=dict(name=name,poly=g,approach=approach,angle=rot,x=x,y=y,w=ww,h=hh);cost=d
  if best is None:
   print('PACK_RETRY',name,round(common.area,1),flush=True);return None
  occupied.append(best['poly']);items.append(best)
 return items

def build(fi,v):
 name,anchors,hubs,logic,risk=F[fi];variant='AB'[v];anchors=[list(a) for a in anchors];hubs=[tuple(h) for h in hubs]
 # B changes branching as well as furnishings: asymmetric aperture and hubs shifted, not rigid rotation
 if v:
  anchors=[[x+( .45 if j%2 else -.45),y+(.65 if j<2 else -.45),ang+(8 if j%2 else -8)] for j,(x,y,ang) in enumerate(anchors)]
  hubs=[(x+.6*(j%2),y+.45) for j,(x,y) in enumerate(hubs)]
 # increase separation only until private geometries no longer overlap
 for fac in np.arange(1,1.81,.08):
  aa=[(x*fac,y*fac,ang) for x,y,ang in anchors];rooms=[private('H'+str(j+1),(x,y),ang,variant,fi) for j,(x,y,ang) in enumerate(aa)]
  if all(rooms[i]['poly'].buffer(.14).intersection(rooms[j]['poly'].buffer(.14)).area<.005 for i in range(4) for j in range(i)):break
 else:raise ValueError(('rooms overlap',fi,v))
 hp=unary_union([Point(*h) for h in hubs]);core=None;items=None
 for radius in [3.35,3.7,4.05,4.4,4.75,5.1,5.5,6.0,6.5,7.0,7.5]:
  core=hp.buffer(radius,resolution=20)
  if len(hubs)>1:core=core.union(LineString(hubs).buffer(1.1,cap_style=1,join_style=1))
  paths=[]
  for rr in rooms:
   d=Point(rr['door']);q=nearest_points(d,hp)[1];paths.append(LineString([d,q]).buffer(.9,cap_style=1))
  shared=unary_union([core]+paths).difference(unary_union([r['poly'] for r in rooms]))
  # courtyard trials: genuine exterior voids, not just painted shapes
  holes=[]
  if fi in [6,14,19] and radius>=3.7:
   centers=[(-3.3,0),(3.3,0)] if fi==14 else [(0,1.2 if fi==19 else 1.5)]
   for hx,hy in centers:
    hole=Point(hx,hy).buffer(.95 if fi==14 else 1.05,resolution=28)
    if shared.buffer(-.9).covers(hole):shared=shared.difference(hole);holes.append(hole)
  reserved=reserve_routes(shared,rooms)
  if reserved is None:continue
  c=shared.centroid;minx,miny,maxx,maxy=shared.bounds
  # variant changes public relations and wet core position
  targets={'B1':(c.x-2.2,c.y+(2 if v else -2)),'B2':(c.x,c.y+(2 if v else -2)),'K':(c.x+2,c.y+(-2 if v else 2)),'F':(c.x+2.7,c.y+(-2 if v else 2)),'M':(c.x+1,c.y),'S':(c.x-1.5,c.y),'G':(c.x-2,c.y)}
  items=choose_pack(shared,targets,fi*2+v+18,reserved)
  if items:break
 if not items:raise ValueError(('pack fail',fi,v))
 floor=shared.union(unary_union([r['poly'] for r in rooms]));baths=[it['poly'] for it in items if it['name'].startswith('B')];obstacles=[it['poly'] for it in items]
 # walkable centre space for a disc of diameter0.90m, furniture geometry only. Not full accessibility.
 free=shared.difference(unary_union(obstacles));walk=free.buffer(-.45)
 # choose arrival boundary on common, excluding bedroom-facing edges; no location from old P02
 perimeter=floor.boundary.intersection(shared.boundary.buffer(.03));coords=[]
 if not perimeter.is_empty:
  length=perimeter.length
  for t in np.linspace(0,max(0,length-.01),200):
   q=perimeter.interpolate(float(t));
   if any(q.distance(r['poly'])<.8 for r in rooms):continue
   if q.distance(unary_union(obstacles))<1.2:continue
   coords.append(q)
 if not coords:coords=[shared.representative_point()]
 c=shared.centroid;arrival=min(coords,key=lambda p:p.x if not v else -p.y)
 # door approach just outward from bedroom into shared
 entries=[]
 for rr in rooms:
  ang=math.radians(rr['angle']);d=rr['door'];entries.append(Point(d[0]+math.sin(ang)*.8,d[1]-math.cos(ang)*.8))
 comps=polygons(walk) if not walk.is_empty else []
 joined=0;pick=None
 for comp in comps:
  hit=sum(comp.distance(q)<.35 for q in entries)
  if hit>joined:joined=hit;pick=comp
 geom_conflicts=[]
 for rr in rooms:
  for k in ['bed','desk','chair','ward']:
   if rr[k].difference(rr['poly']).area>.02:geom_conflicts.append(rr['id']+' '+k+' fuera')
  for a,b in [('bed','desk'),('bed','ward'),('desk','ward'),('chair','bed')]:
   if rr[a].intersection(rr[b]).area>.002:geom_conflicts.append(rr['id']+' '+a+'/'+b)
 entryok=arrival.distance(floor.boundary)<.1
 # fold desk .9 wide pivot; vertical envelope1.8m cannot be proven in plan
 data=dict(code=f'{fi+1:02}{variant}',family=name,logic=logic,risk=risk,variant=variant,rooms=rooms,shared=shared,floor=floor,items=items,arrival=arrival,entries=entries,holes=holes,walk=walk,connections=joined,reserved=reserved,geometry_conflicts=geom_conflicts,entry_on_boundary=entryok,radius=radius)
 return data

# plotting primitives with holes
from matplotlib.colors import to_rgba
def drawpoly(ax,g,fc,ec=None,lw=1,alpha=1,z=1,hatch=None):
 for p in polygons(g):
  pp=orient(p,sign=1);verts=[];codes=[]
  for ring in [pp.exterior]+list(pp.interiors):
   co=list(ring.coords);verts.extend(co);codes.extend([MP.MOVETO]+[MP.LINETO]*(len(co)-2)+[MP.CLOSEPOLY])
  ax.add_patch(PathPatch(MP(verts,codes),fc=fc,ec=ec or fc,lw=lw,alpha=alpha,zorder=z,hatch=hatch))
def line(ax,pts,c=INK,lw=1,ls='-',z=5):ax.plot(*zip(*pts),c=c,lw=lw,ls=ls,zorder=z)
def label(ax,t,x,y,sz=8,c=INK):ax.text(x,y,t,ha='center',va='center',fontsize=sz,color=c,zorder=12,bbox=dict(fc=BG,ec='none',pad=.5,alpha=.8))
def plotplan(d,path):
 f,ax=plt.subplots(figsize=(13,11));f.patch.set_facecolor(BG);ax.set_facecolor(BG);ax.set_aspect('equal');ax.axis('off');floor=d['floor'];drawpoly(ax,floor,WOOD,INK,lw=1.6)
 drawpoly(ax,d['shared'], '#eee7d2',INK,lw=.5)
 for hole in d['holes']:drawpoly(ax,hole,BG,CYAN,lw=1.3);c=hole.centroid;label(ax,'PATIO',c.x,c.y,7,CYAN)
 for rr in d['rooms']:
  poly=rr['poly'];drawpoly(ax,poly,ROOM,INK,lw=1.3);drawpoly(ax,rr['ward'],'#c8a5bc',INK,lw=.4);drawpoly(ax,rr['bed'],'#fffdf5',INK,lw=.6);drawpoly(ax,rr['desk'],CYAN,INK,lw=.5);drawpoly(ax,rr['chair'],CYAN,INK,lw=.4);drawpoly(ax,rr['use'],'none',CYAN,lw=.5,hatch=None)
  line(ax,rr['doorline'],BG,4);ang=math.radians(rr['angle']);v=np.array([math.cos(ang),math.sin(ang)]);hinge=rr['doorline'][0];guide=np.array(hinge)+.9*np.array([-math.sin(ang),math.cos(ang)]);line(ax,[hinge,guide],PINK,.7)
  line(ax,rr['window'],CYAN,3);line(ax,rr['hinge'],PINK,1.8)
  # reference pasted directly to wall, no standalone display panel
  p1=pt(3.76,1.3,rr['door'],rr['angle']);p2=pt(3.76,1.9,rr['door'],rr['angle']);line(ax,[p1,p2],PINK,1)
  c=poly.centroid;label(ax,rr['id']+f" / {poly.area:.1f} m²",c.x,c.y,8)
  # smooth mattress centre and head pillow, read sleep direction
  pil=xform(box(2.05,3.85,2.95,4.1),rr['door'],rr['angle']);drawpoly(ax,pil,'#ede3d2',INK,lw=.3)
  wc=rr['window'];p=Point((wc[0][0]+wc[1][0])/2,(wc[0][1]+wc[1][1])/2);end=(p.x-math.sin(ang)*.6,p.y+math.cos(ang)*.6);line(ax,[(p.x,p.y),end],CYAN,.5)
 # protected circulation is visible as a subtle hatched area, not an extra wall
 drawpoly(ax,d['reserved'].intersection(d['shared']),'#b9d4cb',None,lw=0,alpha=.25,z=2)
 # furniture and complete wet-room diagram
 for it in d['items']:
  x,y,w,h=it['x'],it['y'],it['w'],it['h'];name=it['name'];g=it['poly'];angle=it['angle']
  if name.startswith('B'):
   drawpoly(ax,g,WET,INK,lw=1)
   if angle==0:
    drawpoly(ax,box(x+.1,y+h-1,x+1,y+h-.1),'#fffefa',CYAN,lw=.5);drawpoly(ax,Point(x+w-.45,y+h-.6).buffer(.23),'#fffefa',INK,lw=.5);drawpoly(ax,box(x+.1,y+.2,x+.7,y+.65),'#fffefa',INK,lw=.5);line(ax,[(x+.6,y),(x+1.5,y)],BG,3);line(ax,[(x+.6,y+.08),(x+1.5,y+.08)],PINK,.7)
   else:
    drawpoly(ax,box(x+w-1,y+.1,x+w-.1,y+1),'#fffefa',CYAN,lw=.5);drawpoly(ax,Point(x+w-.6,y+h-.45).buffer(.23),'#fffefa',INK,lw=.5);drawpoly(ax,box(x+.2,y+.1,x+.65,y+.7),'#fffefa',INK,lw=.5);line(ax,[(x,y+.6),(x,y+1.5)],BG,3);line(ax,[(x+.08,y+.6),(x+.08,y+1.5)],PINK,.7)
   c=g.centroid;label(ax,name+' / 5,0',c.x,c.y,6)
  elif name=='K':
   drawpoly(ax,g,CYAN,INK,lw=.7)
   for frac in [.25,.5,.75]:
    if angle==0:line(ax,[(x+w*frac,y),(x+w*frac,y+h)],INK,.4)
    else:line(ax,[(x,y+h*frac),(x+w,y+h*frac)],INK,.4)
   # sink and four hob rings, actual rectangles
   if angle==0:
    drawpoly(ax,box(x+.15,y+.12,x+.75,y+h-.12),BG,INK,lw=.4)
    for px in [x+2.1,x+2.4]:
     for py in [y+.23,y+.48]:drawpoly(ax,Point(px,py).buffer(.08),BG,INK,lw=.3)
   else:
    drawpoly(ax,box(x+.12,y+.15,x+w-.12,y+.75),BG,INK,lw=.4)
    for px in [x+.23,x+.48]:
     for py in [y+2.1,y+2.4]:drawpoly(ax,Point(px,py).buffer(.08),BG,INK,lw=.3)
  elif name=='F':drawpoly(ax,g,'#ced7d3',INK,lw=.5);c=g.centroid;label(ax,'F',c.x,c.y,7)
  elif name=='M':
   drawpoly(ax,g,'#f4f0e6',INK,lw=.7)
   if angle==0:
    for px in [x+.4,x+1.4]:
     for py in [y-.32,y+h+.32]:drawpoly(ax,Point(px,py).buffer(.18),CYAN,INK,lw=.3)
   else:
    for py in [y+.4,y+1.4]:
     for px in [x-.32,x+w+.32]:drawpoly(ax,Point(px,py).buffer(.18),CYAN,INK,lw=.3)
  elif name=='S':
   drawpoly(ax,g,'#d895ba',INK,lw=.6)
   for frac in [.33,.66]:
    if angle==0:line(ax,[(x+w*frac,y),(x+w*frac,y+h)],INK,.3)
    else:line(ax,[(x,y+h*frac),(x+w,y+h*frac)],INK,.3)
  elif name=='G':drawpoly(ax,g,'#c6aa82',INK,lw=.5);c=g.centroid;label(ax,'G',c.x,c.y,7)
 if 'task' in d:
  drawpoly(ax,d['task'],WOOD,INK,lw=.6);c=d['task'].centroid;label(ax,'CORTAR / COSER',c.x,c.y,6)
  drawpoly(ax,d['dry'],'none',PINK,lw=.7,hatch='///');c=d['dry'].centroid;label(ax,'SECAR',c.x,c.y,6)
  g=d['zones']['R'];x,y,X,Y=g.bounds
  for xx in [x+.65,x+1.85]:drawpoly(ax,Point(xx,y+.65).buffer(.3),'none',INK,lw=.6)
  line(ax,[(x+.65,y+.65),(x+1.2,y+1.15),(x+1.85,y+.65),(x+.65,y+.65)],INK,.5)
 # arrival arrow, explicitly hypothetical edge
 q=d['arrival'];c=d['shared'].representative_point();vec=np.array([c.x-q.x,c.y-q.y]);vec=vec/max(np.linalg.norm(vec),1e-5);start=np.array([q.x,q.y])-vec*1;end=np.array([q.x,q.y])+vec*.7;ax.annotate('',end,start,arrowprops=dict(arrowstyle='->',color=PINK,lw=1.8));label(ax,'E/S',start[0],start[1]-.3,8,PINK)
 # a textile layer independent of wall, along selected truly external facade sections
 for rr in d['rooms']:
  a,b=rr['window'];ang=math.radians(rr['angle']);off=np.array([-math.sin(ang),math.cos(ang)])*.35;aa=np.array(a)+off;bb=np.array(b)+off;ts=np.linspace(0,1,25);pts=[]
  for t in ts:pts.append(aa*(1-t)+bb*t+off/7*math.sin(t*math.pi*10))
  line(ax,pts,PINK,.8,ls='--')
 minx,miny,maxx,maxy=floor.bounds
 # actual whole geometric dimensions
 yy=miny-.8;line(ax,[(minx,yy),(maxx,yy)],INK,.6);line(ax,[(minx,yy-.15),(minx,yy+.15)],INK,.6);line(ax,[(maxx,yy-.15),(maxx,yy+.15)],INK,.6);label(ax,f'{maxx-minx:.2f} m', (minx+maxx)/2,yy-.25,8)
 xx=minx-.8;line(ax,[(xx,miny),(xx,maxy)],INK,.6);label(ax,f'{maxy-miny:.2f} m',xx-.1,(miny+maxy)/2,8)
 ax.set_xlim(minx-1.8,maxx+1.3);ax.set_ylim(miny-1.8,maxy+1.3)
 f.savefig(path,dpi=145,bbox_inches='tight',facecolor=BG);f.savefig(path.with_suffix('.svg'),bbox_inches='tight',facecolor=BG);plt.close(f)

