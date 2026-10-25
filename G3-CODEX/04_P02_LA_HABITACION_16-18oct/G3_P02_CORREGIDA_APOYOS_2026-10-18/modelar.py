from pathlib import Path
import math,json
import rhino3dm as r
from shapely.geometry import Polygon,box,Point,LineString
from shapely.ops import unary_union,triangulate
from shapely.geometry.polygon import orient
P=Path(__file__).parent;m=r.File3dm();m.Settings.ModelUnitSystem=r.UnitSystem.Meters;m.Settings.ModelAbsoluteTolerance=.001
cols={'01_SUELO':(221,216,194,255),'02_PAREDES':(139,177,157,255),'03_COLCHONES':(246,241,225,255),'04_MESAS_RESERVAS':(102,169,182,255),'05_ARMARIOS_RESERVAS':(183,119,156,255),'06_VIDRIOS':(139,203,211,160),'07_CUBIERTA':(179,192,167,255),'08_CUBIERTA_LUCERNARIO':(107,184,196,180),'09_GUIAS_FLUJO':(48,133,88,255),'10_P03_P04_REFERENCIA_OCULTA':(147,153,148,255),'11_PERIMETRO_V4_OCULTO':(193,122,83,255),'12_BANOS_RESERVAS':(211,180,206,255)};layers={};render=[]
for k,col in cols.items():
 l=r.Layer();l.Name=k;l.Color=col;l.Visible='OCULT' not in k;layers[k]=m.Layers.Add(l)
def add(g,k,name):
 if g is None:raise ValueError(name)
 a=r.ObjectAttributes();a.LayerIndex=layers[k];a.Name=name;a.ObjectColor=cols[k];a.ColorSource=r.ObjectColorSource.ColorFromObject;a.SetUserString('Estado','Estudio de planta completa; no dimensionado constructivo');m.Objects.Add(g,a)
def parts(g):return [g] if g.geom_type=='Polygon' else [q for q in g.geoms if q.geom_type=='Polygon']
def polyline(coords,z):return r.PolylineCurve([r.Point3d(x,y,z) for x,y in coords])
def solid(g,z,h,k,name):
 for pol in parts(g):
  pol=orient(pol,sign=1.0)
  ex=r.Extrusion.Create(polyline(pol.exterior.coords,z),h,True)
  for hole in pol.interiors:ex.AddInnerProfile(polyline(hole.coords,z))
  add(ex,k,name)
  # cache exact wall side/top polygons for visual inspection
  if 'OCULT' not in k and k not in ['06_VIDRIOS','09_GUIAS_FLUJO']:
   for ring in [pol.exterior]+list(pol.interiors):
    co=list(ring.coords)
    for a,b in zip(co[:-1],co[1:]):render.append(([(a[0],a[1],z),(b[0],b[1],z),(b[0],b[1],z+h),(a[0],a[1],z+h)],k))
   for tr in triangulate(pol):
    if pol.covers(tr.representative_point()):render.append(([(x,y,z+h) for x,y in list(tr.exterior.coords)[:3]],k))
def rect(x,y,w,d,z,h,k,name):solid(box(x,y,x+w,y+d),z,h,k,name)
rooms=[]
for x,y,name in [(-6.2,-2,'H1'),(2.2,-2,'H2'),(-6.2,4.9,'H3'),(2.2,4.9,'H4')]:
 pol=box(x+.55,y+.55,x+3.45,y+3.35).buffer(.55,resolution=12);rooms.append((x,y,name,pol))
common=Polygon([(-2.2,-2.2),(2.2,-2.2),(2.2,1.9),(6.5,1.9),(6.5,4.9),(2.2,4.9),(2.2,9),(-2.2,9),(-2.2,4.9),(-7.8,4.9),(-7.8,1.9),(-2.2,1.9)])
# outer garment niches visually sketched before are now actual floor bulges
niches=[]
for x,y,name,pol in rooms:
 cx=x if x<0 else x+4;cy=y+2;disk=Point(cx,cy).buffer(.6,resolution=24);clip=box(cx-.7,cy-.8,cx,cy+.8) if x<0 else box(cx,cy-.8,cx+.7,cy+.8);niches.append(disk.intersection(clip))
foot=unary_union([common]+[q[3] for q in rooms]+niches)
solid(foot,-.18,.18,'01_SUELO','Suelo completo / espesor indicativo180mm')
# perimeter wall with explicit entry and window gaps
walls=foot.boundary.buffer(.06,cap_style=2)
openings=[box(-8,2.75,-7.6,4.05),box(-2,8.85,2,9.2)]
for x,y,name,pol in rooms:
 dx=x+2 if x<0 else x+.2
 openings.append(box(dx-.05,y-.2,dx+1.85,y+.2) if y<0 else box(dx-.05,y+3.7,dx+1.85,y+4.1))
walls=walls.difference(unary_union(openings));solid(walls,0,2.75,'02_PAREDES','Envolvente / cerramiento esquematico120mm')
# windows low sill and glass
for x,y,name,pol in rooms:
 north=y>0;dx=x+2 if x<0 else x+.2;wy=y+3.9 if north else y
 rect(dx,wy-.04,1.8,.08,0,.65,'02_PAREDES',name+' antepecho');rect(dx,wy-.025,1.8,.05,.65,1.8,'06_VIDRIOS',name+' hueco propio')
 # room partitions only on common-facing boundary, opening at documented position
 inner=pol.boundary.buffer(.06).intersection(common.buffer(.1))
 doorx=(x+.65 if x<0 else x+3.35) if north else (x+3.1 if x<0 else x+.9);doory=y if north else y+3.9
 inner=inner.difference(box(doorx-.5,doory-.2,doorx+.5,doory+.2));solid(inner,0,2.75,'02_PAREDES',name+' tabiques / puerta libre1m')
 rect(doorx-.5,doory-.04,1,.08,2.2,.55,'02_PAREDES',name+' dintel acceso')
 # mattress only, no larger platform
 bx=x+1.3 if x<0 else x+2.7;by=y+2.7;solid(Point(bx,by).buffer(1.05,resolution=48),0,.22,'03_COLCHONES',name+' colchon circular diametro2.10 / sin plataforma')
 dy=y+.15;rect(dx,dy,1.4,.9,.75,.045,'04_MESAS_RESERVAS',name+' tablero inclinable / posicion horizontal');rect(dx+1.4,dy,.4,.9,.75,.045,'04_MESAS_RESERVAS',name+' banda fija');solid(Point(dx+.9,dy+1.35).buffer(.2),0,.45,'04_MESAS_RESERVAS',name+' taburete reserva')
 rect(dx+1.85,dy,.05,.9,0,1.85,'05_ARMARIOS_RESERVAS',name+' panel lateral apoyado en suelo')
 for px in [dx+.1,dx+1.3,dx+1.7]:
  for py in [dy+.1,dy+.8]:rect(px,py,.05,.05,0,.75,'04_MESAS_RESERVAS',name+' pata tablero')
 cx=x if x<0 else x+4;cy=y+2
 # niche storage reserve at the outer arc, with no claim of walk-in capacity
 theta=[math.pi/2+i*math.pi/24 for i in range(25)] if x<0 else [-math.pi/2+i*math.pi/24 for i in range(25)]
 for t in [theta[0],theta[-1]]:
  px=cx+.46*math.cos(t);py=cy+.46*math.sin(t);solid(Point(px,py).buffer(.025),0,1.7,'05_ARMARIOS_RESERVAS',name+' soporte barra ropa')
 co=[(cx+.46*math.cos(t),cy+.46*math.sin(t)) for t in theta];add(polyline(co,1.7),'05_ARMARIOS_RESERVAS',name+' barra curva / nicho no transitable comprobado')
 # route centerlines, not sole clearance proof
 add(polyline([(doorx,3.4),(doorx,doory+(.6 if north else -.6))],.02),'09_GUIAS_FLUJO',name+' recorrido indicativo')
# bathroom reservations with doors facing distribution
for x in [-2.1,.1]:
 pol=box(x,-2.1,x+2,.2);wall=pol.boundary.buffer(.06).difference(box(x+.5,0,x+1.5,.4));solid(wall,0,2.5,'12_BANOS_RESERVAS','Bano reserva / apertura nominal1m');rect(x+.15,-1.8,.8,.9,.0,.04,'12_BANOS_RESERVAS','Ducha reserva');solid(Point(x+1.5,-1.3).buffer(.22),0,.42,'12_BANOS_RESERVAS','Inodoro volumen reserva')
# kitchen and living fragments shown in plan
rect(-1.95,8.2,3.9,.6,0,.9,'04_MESAS_RESERVAS','Cocina lineal reserva / equipamiento pendiente');rect(-.9,7.25,1.8,.75,.75,.05,'04_MESAS_RESERVAS','Mesa cocina');rect(-1,4.55,2,.55,0,.42,'04_MESAS_RESERVAS','Sala de estar / asiento esquematico fuera del acceso')

for px in [-.8,.8]:
 for py in [7.35,7.9]:rect(px,py,.06,.06,0,.75,'04_MESAS_RESERVAS','Pata mesa cocina')
rect(-2,8.94,4,.12,0,.25,'02_PAREDES','Antepecho hueco norte')
for px in [-2,1.94]:rect(px,8.94,.06,.12,.25,2.5,'02_PAREDES','Jamba norte')
rect(-2,8.94,4,.12,2.75,.15,'02_PAREDES','Dintel norte a cubierta')
rect(-2,8.97,4,.05,.25,2.5,'06_VIDRIOS','Hueco lateral norte propuesto')
# actual proposed roof height from longitudinal section, native editable triangle meshes
profile=[(-2.2,2.75),(1.9,2.9),(4.2,2.9),(5.4,3.85),(6.3,3.85),(7,2.9),(9,2.9)]
def ht(y):
 for (a,b),(c,d) in zip(profile[:-1],profile[1:]):
  if a<=y<=c:return b+(d-b)*(y-a)/(c-a)
 return profile[0][1] if y<profile[0][0] else profile[-1][1]
# close all perimeter and partition walls to roof; split segments at ridge changes
upperwalls=walls
for x,y,name,pol in rooms:
 north=y>0;doorx=(x+.65 if x<0 else x+3.35) if north else (x+3.1 if x<0 else x+.9);doory=y if north else y+3.9
 inner=pol.boundary.buffer(.06).intersection(common.buffer(.1)).difference(box(doorx-.5,doory-.2,doorx+.5,doory+.2));upperwalls=unary_union([upperwalls,inner])
for lo,hi in zip([p[0] for p in profile[:-1]],[p[0] for p in profile[1:]]):
 for pol in parts(upperwalls.intersection(box(-10,lo,10,hi))):
  for tri in triangulate(pol):
   if tri.area<1e-8 or not pol.covers(tri.representative_point()):continue
   co=list(tri.exterior.coords)[:3];mesh=r.Mesh()
   for zmode in [0,1]:
    for x,y in co:mesh.Vertices.Add(x,y,ht(y) if zmode else 2.75)
   mesh.Faces.AddFace(0,2,1);mesh.Faces.AddFace(3,4,5)
   for i,j in [(0,1),(1,2),(2,0)]:mesh.Faces.AddFace(i,j,j+3,i+3)
   mesh.Normals.ComputeNormals();mesh.Compact()
   if mesh.IsValid:add(mesh,'02_PAREDES','Cierre pared hasta cubierta')
# window headers close upper gap
for x,y,name,pol in rooms:
 dx=x+2 if x<0 else x+.2;wy=y+3.9 if y>0 else y;rect(dx,wy-.04,1.8,.08,2.45,.3,'02_PAREDES',name+' dintel ventana')
# split at each profile breakpoint to avoid triangles bridging crease
for lo,hi in zip([p[0] for p in profile[:-1]],[p[0] for p in profile[1:]]):
 for pol in parts(foot.intersection(box(-10,lo,10,hi))):
  for tr in triangulate(pol):
   if tr.area<1e-8 or not pol.covers(tr.representative_point()):continue
   mesh=r.Mesh();pts=[(x,y,ht(y)) for x,y in list(tr.exterior.coords)[:3]]
   for pt in pts:mesh.Vertices.Add(*pt)
   mesh.Faces.AddFace(0,1,2);mesh.Normals.ComputeNormals();mesh.Compact();key='08_CUBIERTA_LUCERNARIO' if lo==5.4 else '07_CUBIERTA';add(mesh,key,'Cubierta segun seccion / superficie sin espesor ni calculo')
# exact prior slabs hidden for comparison, translated to P02
S=json.load(open(P.parent/'G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/calculo/ESTRUCTURA_RESULTADOS.json'));p2=S['plates'][1]
for p in S['plates'][2:4]:solid(Polygon([(x-p2['cx'],y-p2['front']) for x,y in p['outline']]),p['z']-p2['z']-.22,.22,'10_P03_P04_REFERENCIA_OCULTA',p['id']+' plataforma original V4 / ocultar para editar')
add(polyline([(x-p2['cx'],y-p2['front']) for x,y in p2['outline']],0),'11_PERIMETRO_V4_OCULTO','Plataforma P02 V4 / referencia exacta')
for name,loc,tgt in [('01_AXONOMETRIA',(20,-24,20),(0,3,0)),('02_PLANTA',(0,3,30),(0,3,0)),('03_NORTE',(15,22,17),(0,3,1))]:
 v=r.ViewInfo();v.Name=name;vp=v.Viewport;vp.SetCameraLocation(r.Point3d(*loc));vp.SetCameraDirection(r.Vector3d(*(tgt[i]-loc[i] for i in range(3))));vp.SetCameraUp(r.Vector3d(0,1,0) if name=='02_PLANTA' else r.Vector3d(0,0,1));vp.TargetPoint=r.Point3d(*tgt);vp.ChangeToParallelProjection(True);vp.Extents(.5,r.BoundingBox(r.Point3d(-8.2,-2.5,-.3),r.Point3d(7,9.3,4.2)));m.NamedViews.Add(v)
assert m.Write(str(P/'P02_CORREGIDA_COMPLETA.3dm'),8)
for l in m.Layers:
 if l.Name in ['07_CUBIERTA','08_CUBIERTA_LUCERNARIO','06_VIDRIOS']:l.Visible=False
assert m.Write(str(P/'P02_CORREGIDA_INTERIOR.3dm'),8)
check=r.File3dm.Read(str(P/'P02_CORREGIDA_INTERIOR.3dm'));invalid=sum(not o.Geometry.IsValid for o in check.Objects);assert invalid==0
(P/'VERIFICACION.json').write_text(json.dumps({'objects':len(check.Objects),'invalid':invalid,'units':'metres','footprint_m2':foot.area,'status':'Modelo de estudio de ultima planta; no nueva propuesta simetrica ni basada en atractores','roofs':'Superficies trianguladas editables, sin espesor ni estructura','originals_modified':False},indent=2))
# clear inspection image generated from same geometric primitives, roof suppressed
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(15,11));ax=fig.add_subplot(111,projection='3d');fig.patch.set_facecolor('#f6f3e9');ax.set_facecolor('#f6f3e9')
for verts,k in render:
 co=tuple(v/255 for v in cols[k][:3]);ax.add_collection3d(Poly3DCollection([verts],facecolors=[co],edgecolors='none',alpha=1))
ax.set_xlim(-8.3,7);ax.set_ylim(-2.5,9.5);ax.set_zlim(-.2,4);ax.set_box_aspect((15.3,12,4.2));ax.view_init(57,-60);ax.set_axis_off();ax.set_title('P02 / modelo completo de estudio · cubierta y vidrio ocultos',loc='left',color='#24594e',fontsize=17);fig.savefig(P/'VISTA_INTERIOR_MODELO.png',dpi=170,bbox_inches='tight');print('MODELOS_VALIDOS',len(check.Objects),'objetos',foot.area,'m2')
