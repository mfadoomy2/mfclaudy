from pathlib import Path
import math,json,pickle,uuid
import numpy as np
import rhino3dm as rh
from shapely.geometry import Point,Polygon,LineString,box
from shapely.ops import unary_union
from shapely.affinity import rotate,translate
from shapely.geometry.polygon import orient
P=Path(__file__).resolve().parents[1];D=pickle.load(open(P/'datos/GEOMETRIA_3D.pkl','rb'))
MATS={'cal':('#d6dec9',0),'corcho':('#c2a47b',0),'madera':('#af815b',0),'lino':('#e7d9b5',0),'acero':('#434e4c',0),'inox':('#9da8a5',0),'vidrio':('#b6dcd6',.72),'rosa':('#c8447e',0),'azul':('#187c83',0),'blanco':('#ece9df',0),'ceramica':('#c2c9b7',0),'textil':('#cf7a9b',.15),'caucho':('#323c38',0)}
def color(h):return tuple(int(h[i:i+2],16) for i in (1,3,5))+(255,)
def polys(g):return [g] if g.geom_type=='Polygon' else [x for x in getattr(g,'geoms',[]) if x.geom_type=='Polygon']
def clean(coords,z):
 pts=[]
 for x,y in coords:
  q=rh.Point3d(float(x),float(y),z)
  if not pts or q.DistanceTo(pts[-1])>1e-5:pts.append(q)
 if len(pts)>2 and pts[-1].DistanceTo(pts[0])<1e-5:pts[-1]=pts[0]
 return rh.PolylineCurve(pts) if len(pts)>2 else None
class Model:
 def __init__(self,code):
  self.f=rh.File3dm();self.f.Settings.ModelUnitSystem=rh.UnitSystem.Meters;self.f.Settings.ModelAbsoluteTolerance=.001;self.layers={};self.mi={};self.records=[];self.code=code
  for name,(h,t) in MATS.items():
   m=rh.Material();m.Name=name;m.DiffuseColor=color(h);m.Transparency=t;m.Shine=90 if name in ['inox','vidrio'] else 12;self.mi[name]=self.f.Materials.Add(m)
 def layer(self,name,mat,visible=True):
  if name not in self.layers:
   l=rh.Layer();l.Name=name;l.Color=color(MATS[mat][0]);l.Visible=visible;self.layers[name]=self.f.Layers.Add(l)
  return self.layers[name]
 def add(self,g,name,layer,mat,xf=None,visible=True,support=''):
  if not g:return
  if xf:g.Transform(xf)
  if not g.IsValid:raise ValueError((self.code,name,'invalid'))
  a=rh.ObjectAttributes();a.Name=name;a.LayerIndex=self.layer(layer,mat,visible);a.MaterialIndex=self.mi[mat];a.MaterialSource=rh.ObjectMaterialSource.MaterialFromObject;a.ObjectColor=color(MATS[mat][0]);a.ColorSource=rh.ObjectColorSource.ColorFromObject;a.SetUserString('Apoyo',support);a.SetUserString('Unidad',self.code)
  self.f.Objects.Add(g,a);bb=g.GetTightBoundingBox();self.records.append({'name':name,'layer':layer,'zmin':bb.Min.Z,'zmax':bb.Max.Z,'support':support})
 def ex(self,g,z,h,name,layer,mat,xf=None,visible=True,support=''):
  for j,p in enumerate(polys(g)):
   if p.area<1e-7:continue
   pp=orient(p,sign=1);crv=clean(pp.exterior.coords,0)
   if not crv:continue
   ex=rh.Extrusion.Create(crv,h,True)
   for ring in pp.interiors:
    inner=clean(ring.coords,0)
    if inner:
     inner.Transform(ex.GetProfileTransformation(0).TryGetInverse())
     if not ex.AddInnerProfile(inner):raise ValueError('inner')
   ex.SetUserString('ExpectedVolume',str(p.area*h));ex.SetUserString('InnerProfiles',str(len(pp.interiors)))
   ex.Transform(rh.Transform.Translation(0,0,z))
   self.add(ex,name+(' '+str(j) if j else ''),layer,mat,xf,visible,support)
 def rod(self,a,b,r,name,layer,mat,xf=None):
  a=rh.Point3d(*a);b=rh.Point3d(*b);v=rh.Vector3d(b.X-a.X,b.Y-a.Y,b.Z-a.Z);plane=rh.Plane(a,v);circle=rh.Circle(r);circle.Plane=plane;g=rh.Cylinder(circle,a.DistanceTo(b)).ToBrep(True,True);self.add(g,name,layer,mat,xf,support='unión entre sus dos extremos')
 def box(self,x,y,z,w,h,depth,name,layer,mat,xf=None,visible=True,support=''):
  self.ex(box(x,y,x+w,y+h),z,depth,name,layer,mat,xf,visible,support)
 def sphere(self,p,r,name,layer,mat,xf=None):self.add(rh.Sphere(rh.Point3d(*p),r).ToBrep(),name,layer,mat,xf,support='apoyado o unido al elemento contiguo')

def xfroom(r):
 move=rh.Transform.Translation(-1.05,0,0);rot=rh.Transform.Rotation(math.radians(r['angle']),rh.Vector3d(0,0,1),rh.Point3d(0,0,0));offset=rh.Transform.Translation(float(r['door'][0]),float(r['door'][1]),0);return rh.Transform.Multiply(offset,rh.Transform.Multiply(rot,move))

def stool(m,x,y,seat=.44,layer='06_MOBILIARIO',xf=None):
 for dx,dy in [(-.13,-.13),(.13,-.13),(.13,.13),(-.13,.13)]:m.rod((x+dx,y+dy,0),(x+dx,y+dy,seat-.035),.018,'pata taburete',layer,'acero',xf)
 m.ex(Point(x,y).buffer(.23,resolution=24),seat-.035,.035,'asiento taburete',layer,'madera',xf,support='cuatro patas hasta el suelo')

def room_detail(m,r,variant):
 tr=xfroom(r);L='03_HABITACIONES';F='04_CAMAS_Y_ROPA';T='05_MESAS_PLEGABLES';W='07_VENTANAS_TEXTILES'
 # mattress on ventilated platform of equal footprint, floor supported, no larger pedestal
 bed=Point(2.85,3.15).buffer(1.05,resolution=64) if variant=='A' else box(2.45,2.15,3.70,4.15)
 m.ex(bed,0,.055,'apoyo ventilado colchón, misma huella',F,'madera',tr,support='suelo z=0')
 m.ex(bed,.055,.205,'colchón Ø2100' if variant=='A' else 'colchón 1250x2000',F,'lino',tr,support='apoyo ventilado')
 pillow=box(2.40,3.82,3.30,4.08).buffer(.055).intersection(bed.buffer(-.015));m.ex(pillow,.26,.095,'almohada apoyada',F,'blanco',tr,support='colchón z=.26')
 # concave walk-in arc, no storage obstruction of its inner passage
 arc=Point(0,3).buffer(1.37,resolution=48).difference(Point(0,3).buffer(.85,resolution=48)).intersection(box(-1.5,1.5,0,4.5))
 m.ex(arc,0,.09,'zócalo continuo armario',F,'madera',tr,support='suelo')
 m.ex(arc,2.25,.045,'coronación armario cóncavo',F,'madera',tr,support='costillas radiales')
 for a in [90,120,150,180,210,240,270]:
  th=math.radians(a);v=(math.cos(th),math.sin(th));rr=LineString([(v[0]*.86,3+v[1]*.86),(v[0]*1.35,3+v[1]*1.35)]).buffer(.013,cap_style=2)
  m.ex(rr,.09,2.16,'costilla armario',F,'madera',tr,support='zócalo hasta coronación')
 for a,b in zip(np.linspace(92,268,29)[:-1],np.linspace(92,268,29)[1:]):
  aa,bb=math.radians(a),math.radians(b);m.rod((1.08*math.cos(aa),3+1.08*math.sin(aa),1.76),(1.08*math.cos(bb),3+1.08*math.sin(bb),1.76),.014,'barra curva ropa',F,'inox',tr)
 for a in [110,140,170,200,230,255]:
  th=math.radians(a);x=1.08*math.cos(th);y=3+1.08*math.sin(th);m.rod((x,y,2.25),(x,y,1.76),.008,'suspensión barra al techo de armario',F,'inox',tr)
 # fold-up drawing board, short edge at wall x=4.2, no floor legs
 board=rh.Extrusion.Create(clean(box(2.4,.25,4.2,1.15).exterior.coords,1.15-.032),.032,True);tilt=rh.Transform.Rotation(math.radians(-12),rh.Vector3d(0,1,0),rh.Point3d(4.2,0,1.15));board.Transform(tilt);m.add(board,'tablero 1800x900 inclinado 12 grados',T,'madera',tr,support='bisagra canto corto + dos puntales regulables')
 m.rod((4.19,.25,1.15),(4.19,1.15,1.15),.018,'bisagra canto corto 900mm',T,'inox',tr)
 for y in [.38,1.02]:
  m.box(4.19,y-.055,.38,.035,.11,.9,'pletina mural mesa',T,'acero',tr,support='anclada al muro de habitación')
  z=1.15+(2.48-4.2)*math.sin(math.radians(12))-.035
  m.rod((4.19,y,.45),(2.48,y,z),.022,'puntal regulable bloqueado',T,'acero',tr)
  for x,zz in [(4.19,.45),(2.48,z)]:m.sphere((x,y,zz),.035,'rótula puntal',T,'inox',tr)
 # alternate closed position is a hidden study layer, never simultaneously visible
 m.box(4.15,.25,1.15,.032,.9,1.8,'mesa plegada, estado alternativo', '90_ESTADO_MESAS_PLEGADAS_OCULTO','madera',tr,False,'bisagra mural; activar ocultando tablero abierto')
 stool(m,3.25,1.65,.46,'06_MOBILIARIO',tr)
 for z in [.44,.64]:m.box(3.85,1.82,z,.35,.36,.012,'slab metálico de noche',F,'inox',tr,support='ménsulas al muro x=4.2')
 m.box(4.18,1.82,.42,.025,.36,.25,'pletina soporte slabs',F,'acero',tr,support='fijación continua al muro')
 m.box(4.16,1.94,.70,.04,.10,.07,'toma USB-C',F,'blanco',tr,support='muro; canalización interior')
 # supported bay seat; meaningful volume, glazing closes at the outer face
 m.box(1.08,5.0,0,2.8,.4,.39,'cajón estructural ventana habitable',W,'madera',tr,support='suelo continuo de la bahía')
 m.box(1.08,5.0,.39,2.8,.4,.055,'cojín ventana',W,'lino',tr,support='cajón inferior')
 m.box(1.15,5.455,.46,2.65,.022,2.08,'vidrio ventana habitable',W,'vidrio',tr,support='marco perimetral')
 for x in [1.13,2.47,3.78]:m.box(x,5.42,.44,.035,.08,2.12,'montante ventana',W,'acero',tr,support='antepecho y dintel')
 for z in [.44,2.54]:m.box(1.13,5.42,z,2.69,.08,.035,'travesaño ventana',W,'acero',tr,support='montantes')
 # exterior fabric on a supported rail, pleats modelled as closed thin strips
 m.rod((1.10,5.68,2.65),(3.85,5.68,2.65),.018,'guía textil exterior',W,'acero',tr)
 for x in [1.10,3.85]:m.rod((x,5.43,2.65),(x,5.68,2.65),.014,'ménsula guía textil',W,'acero',tr)
 for i in range(17):
  x=1.12+i*.16;g=Polygon([(x,5.67),(x+.08,5.73),(x+.16,5.67),(x+.16,5.679),(x+.08,5.739),(x,5.679)])
  m.ex(g,.48,2.15,'pliegue textil guiado',W,'textil',tr,support='anillas al carril a z=2.65');m.rod((x+.08,5.68,2.65),(x+.08,5.73,2.63),.008,'anilla soporte textil',W,'inox',tr)
 # open sliding door, no swing across entry, track fixed to wall
 m.box(1.60,.025,.015,1.10,.045,2.10,'hoja corredera ABIERTA',L,'madera',tr,support='dos carros suspendidos del carril mural')
 m.box(.43,.015,2.14,2.30,.075,.055,'carril puerta habitación',L,'acero',tr,support='muro sobre dintel')
 for x in [1.7,2.55]:m.rod((x,.05,2.115),(x,.05,2.16),.012,'carro puerta',L,'inox',tr)
 m.rod((1.68,.085,.98),(1.68,.085,1.18),.014,'tirador corredera',L,'inox',tr)

def bath(m,it):
 x,y,X,Y=it['poly'].bounds;L='08_BANOS'
 m.ex(it['poly'],-.012,.012,'pavimento baño antideslizante',L,'ceramica',support='forjado; misma cota 0, acabado incluido')
 # shower flush with floor, tray/channel and glazed screen supported on U-profile
 m.box(x+.10,Y-1,-.025,.9,.9,.025,'plato enrasado ducha',L,'blanco',support='recrecido bajo cota de suelo')
 m.box(x+.12,Y-.20,-.006,.85,.025,.006,'canal de ducha',L,'inox',support='plato ducha')
 m.box(x+1.01,Y-.96,.025,.018,.86,1.95,'mampara ducha',L,'vidrio',support='perfil inferior y fijación lateral')
 m.box(x+.99,Y-.97,0,.055,.89,.025,'perfil base mampara',L,'inox',support='plato')
 m.rod((x+.38,Y-.06,1.05),(x+.38,Y-.06,2.1),.014,'columna ducha',L,'inox')
 m.rod((x+.38,Y-.06,2.1),(x+.38,Y-.30,2.1),.016,'brazo rociador',L,'inox')
 m.ex(Point(x+.38,Y-.30).buffer(.10),2.08,.025,'rociador ducha',L,'inox',support='brazo a pared')
 # floor-supported wc, cistern and seat
 wc=Point(X-.45,Y-.60).buffer(.25,resolution=30);m.ex(wc,0,.37,'cuerpo WC apoyado',L,'blanco',support='suelo');m.ex(wc,.37,.035,'asiento WC',L,'lino',support='cuerpo cerámico')
 m.box(X-.68,Y-.16,.0,.46,.13,.80,'cisterna WC',L,'blanco',support='suelo y pared')
 m.box(x+.10,y+.25,0,.60,.45,.78,'mueble lavabo',L,'madera',support='suelo')
 basin=box(x+.10,y+.25,x+.70,y+.70).difference(box(x+.18,y+.33,x+.62,y+.62));m.ex(basin,.78,.10,'borde lavabo',L,'blanco',support='mueble inferior');m.box(x+.18,y+.33,.78,.44,.29,.015,'fondo lavabo',L,'blanco',support='mueble')
 m.rod((x+.40,y+.68,.78),(x+.40,y+.68,1.01),.015,'grifo lavabo',L,'inox');m.rod((x+.40,y+.68,1.01),(x+.40,y+.53,1.01),.014,'caño lavabo',L,'inox')
 for xx in [x+.025,x+1.575]:
  m.box(xx,y+.025,.015,.50,.045,2.10,'hoja corredera baño ABIERTA',L,'madera',support='carros en guía superior');m.rod((xx+.25,y+.05,2.10),(xx+.25,y+.05,2.17),.012,'carro puerta baño',L,'inox')
 m.box(x,y+.015,2.14,2.1,.075,.055,'carril doble baño',L,'acero',support='muro sobre vano')

def furniture(m,d):
 L='06_MOBILIARIO';K='09_COCINA'
 for it in d['items']:
  name=it['name'];x,y,X,Y=it['poly'].bounds
  if name.startswith('B'):bath(m,it)
  elif name=='K':
   sink=box(x+.15,y+.10,x+.75,Y-.10);m.ex(it['poly'].difference(sink),.88,.04,'encimera con hueco de fregadero',K,'inox',support='módulos bajos')
   for j in range(6):
    xx=x+j*.6;m.ex(box(xx+.015,y+.025,xx+.585,Y-.025).difference(box(xx+.033,y+.043,xx+.567,Y-.043)),.10,.76,'costados módulo cocina',K,'azul',support='zócalo');m.box(xx+.015,y+.025,.10,.57,Y-y-.05,.018,'fondo módulo cocina',K,'azul',support='zócalo');m.box(xx+.015,y+.025,.025,.57,Y-y-.05,.075,'zócalo cocina',K,'acero',support='suelo');m.rod((xx+.13,y+.005,.75),(xx+.47,y+.005,.75),.009,'tirador cocina',K,'inox')
   m.ex(sink,.73,.012,'fondo fregadero',K,'inox',support='cuba');m.ex(sink.buffer(.018).difference(sink),.73,.15,'paredes cuba',K,'inox',support='fondo y encimera')
   m.rod((x+.45,Y-.04,.90),(x+.45,Y-.04,1.18),.018,'grifo cocina',K,'inox');m.rod((x+.45,Y-.04,1.18),(x+.45,Y-.25,1.18),.018,'caño cocina',K,'inox')
   m.box(x+1.85,y+.05,.92,.70,.60,.012,'placa cocina',K,'acero',support='encimera')
   for xx in [x+2.02,x+2.35]:
    for yy in [y+.22,y+.48]:m.ex(Point(xx,yy).buffer(.09),.932,.004,'zona inducción',K,'caucho',support='placa')
   m.box(x+1.83,y-.006,.26,.58,.025,.45,'frente horno',K,'acero',support='módulo cocina')
  elif name=='F':
   m.ex(it['poly'],0,1.92,'frigorífico',K,'blanco',support='suelo');m.rod((x+.08,y-.02,.90),(x+.08,y-.02,1.5),.012,'tirador frigorífico',K,'inox')
  elif name in ['M','G']:
   if name=='G':m.ex(it['poly'],0,.9,'armario herramientas',L,'madera',support='suelo');continue
   m.ex(it['poly'],.72,.035,'mesa común',L,'madera',support='cuatro patas')
   for xx in [x+.1,X-.1]:
    for yy in [y+.1,Y-.1]:m.rod((xx,yy,0),(xx,yy,.72),.025,'pata mesa',L,'acero')
   for xx in [x+.4,X-.4]:
    for yy in [y-.34,Y+.34]:stool(m,xx,yy)
  elif name=='S':
   for xx in [x+.12,X-.12]:
    for yy in [y+.12,Y-.12]:m.rod((xx,yy,0),(xx,yy,.14),.025,'pata sofá',L,'acero')
   m.ex(it['poly'],.14,.15,'bastidor sofá',L,'madera',support='cuatro patas')
   for j in range(3):m.box(x+j*.8+.015,y+.02,.29,.77,.69,.16,'cojín sofá',L,'rosa',support='bastidor')
   m.box(x,Y-.17,.29,2.4,.17,.51,'respaldo sofá',L,'rosa',support='bastidor')
 # common making table and drying rack with continuous supports
 x,y,X,Y=d['task'].bounds;m.ex(d['task'],.86,.04,'mesa cortar coser',L,'corcho',support='patas metálicas')
 for xx in [x+.1,X-.1]:
  for yy in [y+.1,Y-.1]:m.rod((xx,yy,0),(xx,yy,.86),.022,'pata mesa trabajo',L,'acero')
 x,y,X,Y=d['dry'].bounds
 for xx in [x,X]:
  for yy in [y,Y]:m.rod((xx,yy,0),(xx,yy,1.55),.016,'poste tendedero',L,'acero')
 for yy in np.linspace(y,Y,4):m.rod((x,float(yy),1.55),(X,float(yy),1.55),.005,'línea tendido',L,'inox')
 for xx in [x,X]:m.rod((xx,y,1.55),(xx,Y,1.55),.014,'travesaño tendedero',L,'acero')
 # bicycle schematic connected tires/frame, tires meet ground
 x,y,X,Y=d['zones']['R'].bounds
 for xx in [x+.65,x+1.85]:
  for a,b in zip(np.linspace(0,2*math.pi,33)[:-1],np.linspace(0,2*math.pi,33)[1:]):m.rod((xx+.30*math.cos(a),y+.65,.33+.30*math.sin(a)),(xx+.30*math.cos(b),y+.65,.33+.30*math.sin(b)),.03,'neumático bicicleta',L,'caucho')
 for a,b in [((x+.65,y+.65,.33),(x+1.15,y+.65,.85)),((x+1.15,y+.65,.85),(x+1.85,y+.65,.33)),((x+.65,y+.65,.33),(x+1.85,y+.65,.33)),((x+1.15,y+.65,.85),(x+1.15,y+.65,1.0))]:m.rod(a,b,.025,'cuadro bicicleta',L,'azul')
 m.box(x+1.05,y+.55,1.0,.25,.20,.035,'sillín bicicleta',L,'caucho',support='tija')

def create(d):
 m=Model(d['code']);floor=d['floor3d'];walls=d['walls3d'];door=d['doors3d'];win=d['windows3d'];L='02_CERRAMIENTOS'
 m.ex(floor,-.22,.22,'forjado continuo, acabado z=0','01_SUELO','corcho',support='reserva estructural; dimensionamiento pendiente')
 # wall levels preserve actual openings; no fake glass over a solid full-height wall
 m.ex(walls.difference(door),0,.44,'muros bajos',L,'cal',support='forjado')
 m.ex(walls.difference(door.union(win)),.44,1.76,'muros laterales puertas y ventanas',L,'cal',support='forjado y paños inferiores')
 m.ex(walls.difference(win),2.20,.35,'dinteles de puertas',L,'cal',support='jambas laterales')
 m.ex(walls,2.55,.45,'cierre superior continuo',L,'cal',support='paños laterales y dinteles')
 for r in d['rooms']:room_detail(m,r,d['variant'])
 furniture(m,d)
 # roofs are at their built position and hidden for inspection, never exploded upwards
 m.ex(floor,3.0,.16,'cubierta en posición construida','91_CUBIERTA_OCULTA','blanco',visible=False,support='muros a z=3.0; sin cálculo estructural')
 # actual entry frame and sliding leaf, on tangent of curved wall
 ex,ey,angle=d['entry3d'];tr=rh.Transform.Multiply(rh.Transform.Translation(ex,ey,0),rh.Transform.Rotation(math.radians(angle),rh.Vector3d(0,0,1),rh.Point3d(0,0,0)))
 for xx in [-.78,.75]:m.box(xx,-.065,0,.03,.13,2.21,'jamba acceso unidad','10_ACCESO','acero',tr,support='suelo y dintel')
 m.box(-.78,-.065,2.20,1.56,.13,.055,'dintel acceso unidad','10_ACCESO','acero',tr,support='dos jambas')
 m.box(.78,-.05,.015,1.45,.045,2.15,'hoja corredera acceso abierta','10_ACCESO','vidrio',tr,support='carril sobre puerta')
 m.box(-.78,-.07,2.24,3.10,.16,.04,'carril acceso','10_ACCESO','acero',tr,support='dintel y soportes a muro')
 # views stored per model at origin, with roof hidden
 bb=floor.bounds;cx=(bb[0]+bb[2])/2;cy=(bb[1]+bb[3])/2
 shift=rh.Transform.Translation(-cx,-cy,0)
 for ob in m.f.Objects:ob.Geometry.Transform(shift)
 for name,cam,up in [('AXONOMETRIA',(26,-30,26),(0,0,1)),('PLANTA',(0,0,55),(0,1,0)),('HABITACIONES',(14,-18,17),(0,0,1))]:
  v=rh.ViewInfo();v.Name=name;v.Viewport.SetCameraLocation(rh.Point3d(*cam));v.Viewport.SetCameraDirection(rh.Vector3d(-cam[0],-cam[1],-cam[2]+1.0));v.Viewport.SetCameraUp(rh.Vector3d(*up));m.f.NamedViews.Add(v)
 m.f.Strings['Alcance']='Unidad 3D, suelo acabado z=0; cubierta y mesa plegada ocultas en posición real. Sin cálculo ni certificación de obra.'
 m.f.Strings['Origen']='Centro XY de envolvente, suelo z=0';m.f.Strings['Procedencia']='Atlas 88 páginas; código '+d['code']+'; habitaciones corregidas y conexiones suavizadas'
 dest=P/'modelos'/f'{d["code"]}_UNIDAD_3D.3dm';assert m.f.Write(str(dest),8)
 re=rh.File3dm.Read(str(dest));invalid=[o.Attributes.Name for o in re.Objects if not o.Geometry.IsValid];assert not invalid,invalid
 return m,{'code':d['code'],'objects':len(re.Objects),'invalid':invalid,'finished_floor_z':0,'floor3d_m2':round(floor.area,2),'records':m.records}

reports=[]
for d in D:
 m,r=create(d);reports.append(r);print(d['code'],r['objects'],'objetos',flush=True)
 (P/'verificacion/MODELOS.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
print('40_MODELOS_3D_GENERADOS',flush=True)
