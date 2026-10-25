from pathlib import Path
import math,pickle,json,sys
import rhino3dm as rh
import numpy as np
from shapely.geometry import Point,Polygon,LineString,box
from shapely.ops import unary_union
import geometria as G
from primitivas import Model,clean,polys
P=Path(__file__).resolve().parents[1]

def tr(r):
 # Local mirrors are handled by a proper reflection, not by changing measured furniture sizes.
 refl=rh.Transform.Mirror(rh.Point3d(1.65,0,0),rh.Vector3d(1,0,0)) if r.get('mirror') else rh.Transform.Identity()
 t=rh.Transform.Translation(-r['dc'],0,0)
 t=rh.Transform.Multiply(rh.Transform.Rotation(math.radians(r['phi']),rh.Vector3d(0,0,1),rh.Point3d(0,0,0)),rh.Transform.Multiply(t,refl))
 return rh.Transform.Multiply(rh.Transform.Translation(*r['q'],0),t)

def stool(m,x,y,xf=None,z=.45,layer='06_ESTAR_COMER'):
 for dx,dy in [(-.12,-.12),(-.12,.12),(.12,-.12),(.12,.12)]:m.rod((x+dx,y+dy,0),(x+dx,y+dy,z-.035),.016,'pata taburete apoyada',layer,'acero',xf)
 m.ex(Point(x,y).buffer(.21,resolution=24),z-.035,.035,'asiento taburete',layer,'corcho',xf,support='cuatro patas a z=0')

def glazing(m,x0,x1,y,sill,top,xf,name,layer='07_LUZ_Y_TELAS'):
 # Flush frames and real transparent infill, with sill and head borne by the wall.
 m.box(x0,y-.015,sill,x1-x0,.03,top-sill,name+' vidrio',layer,'vidrio',xf,support='carpintería perimetral anclada a jambas')
 for x in [x0,(x0+x1)/2,x1-.035]:m.box(x,y-.04,sill,.035,.08,top-sill,name+' montante',layer,'acero',xf,support='antepecho y dintel')
 for z in [sill,top-.035]:m.box(x0,y-.04,z,x1-x0,.08,.035,name+' travesaño',layer,'acero',xf,support='jambas y montantes')

def room(m,r):
 xf=tr(r);L='03_DORMITORIOS';F='04_DESCANSO_ALMACENAJE';T='05_DIBUJO_PLEGABLE';W='07_LUZ_Y_TELAS'
 m.ex(G.BED,0,.06,'somier ventilado de igual huella 1250x2000',F,'madera',xf,support='suelo z=0')
 m.ex(G.BED,.06,.20,'colchón 1250x2000 mm',F,'lino',xf,support='somier continuo')
 m.ex(box(.80,3.60,1.75,3.92).buffer(.035),.26,.085,'almohada apoyada',F,'blanco',xf,support='colchón z=.26')
 m.ex(box(.67,2.13,1.88,2.80),.26,.012,'manta doblada',F,'textil',xf,support='colchón')
 # Concave storage consumes 0.55m maximum depth rather than a second walk-in room.
 for z in [0,.08,.55,1.05,2.20]:m.ex(G.WARD,z,.028,'armario cóncavo estante',F,'madera',xf,support='costados y fondo anclados al muro')
 for y in [2.0,3.67]:m.box(2.75,y,.028,.55,.025,2.20,'costado armario',F,'madera',xf,support='zócalo a suelo')
 m.box(3.275,2.0,.03,.025,1.70,2.20,'fondo armario',F,'madera',xf,support='muro lateral continuo')
 m.rod((3.02,2.07,1.77),(3.02,3.61,1.77),.014,'barra ropa',F,'inox',xf)
 for y in [2.1,3.6]:m.rod((3.02,y,1.77),(3.02,y,2.20),.009,'suspensión barra ropa',F,'inox',xf)
 # Short 900mm hinge on left wall, 1800mm projection. Board has no floor legs.
 board=rh.Extrusion.Create(clean(G.DESK.exterior.coords,1.15-.03),.03,True)
 board.Transform(rh.Transform.Rotation(math.radians(12),rh.Vector3d(0,1,0),rh.Point3d(.025,0,1.15)))
 m.add(board,'tablero dibujo 1800x900 a 12 grados',T,'madera',xf,support='bisagra de canto corto 900 + dos puntales bloqueables a muro')
 m.rod((.025,.25,1.15),(.025,1.15,1.15),.017,'bisagra mural 900mm',T,'inox',xf)
 for y in [.36,1.04]:
  m.box(.015,y-.05,.38,.028,.10,.85,'pletina anclaje mesa',T,'acero',xf,support='fijación a refuerzo interior del muro')
  m.rod((.04,y,.43),(1.70,y,.75),.021,'puntal telescópico bloqueado',T,'acero',xf)
  m.sphere((.04,y,.43),.029,'rótula mural',T,'inox',xf);m.sphere((1.70,y,.75),.029,'rótula tablero',T,'inox',xf)
 m.box(.03,.25,1.15,.03,.9,1.80,'tablero plegado ESTADO ALTERNATIVO','90_MESA_PLEGADA_OCULTA','madera',xf,False,support='bisagra mural; activar ocultando tablero abierto y puntales')
 stool(m,1.0,.94,xf,z=.44,layer=T)
 for z in [.40,.61]:m.box(.02,3.35,z,.50,.30,.012,'slab noche USB',F,'inox',xf,support='pletina al muro junto al cabecero, fuera del recorrido')
 m.box(.015,3.35,.38,.025,.30,.25,'pletina slabs noche',F,'acero',xf,support='muro lateral')
 m.box(.015,3.43,.68,.025,.10,.07,'toma USB-C propuesta',F,'blanco',xf,support='caja empotrada y canalización a definir')
 m.ex(G.SEAT,0,.40,'cajón asiento ventana 2100x550',W,'madera',xf,support='suelo del mirador, sin piezas suspendidas')
 m.ex(G.SEAT,.40,.065,'cojín asiento ventana',W,'lino',xf,support='cajón inferior')
 glazing(m,.75,2.85,5.16,.47,2.55,xf,'ventana EXTERIOR dormitorio')
 m.rod((.72,5.34,2.68),(2.9,5.34,2.68),.016,'carril textil EXTERIOR',W,'acero',xf)
 for x in [.72,2.90]:m.rod((x,5.18,2.68),(x,5.34,2.68),.013,'ménsula carril textil',W,'acero',xf)
 # Fabric is gathered at one end: the window is not modelled permanently covered.
 for i in range(6):
  x=.73+i*.085;p=Polygon([(x,5.33),(x+.04,5.39),(x+.08,5.33),(x+.08,5.339),(x+.04,5.399),(x,5.339)])
  m.ex(p,.48,2.16,'tela exterior recogida',W,'textil',xf,support='anillas y carril a z=2.68')
  m.rod((x+.04,5.34,2.68),(x+.04,5.39,2.64),.008,'anilla suspensión tela',W,'inox',xf)
 # Pocket leaf is wholly beside a straight 1000mm opening, with no swing in the room.
 m.box(1.0,.015,.015,1.0,.04,2.10,'corredera dormitorio ABIERTA',L,'madera',xf,support='dos carros al carril mural')
 m.box(.95,-.005,2.15,2.17,.09,.05,'carril puerta sobre tramo RECTO',L,'acero',xf,support='dintel recto y refuerzo de jambas')
 for x in [1.12,1.86]:m.rod((x,.035,2.10),(x,.035,2.15),.012,'carro puerta dormitorio',L,'inox',xf)
 m.rod((1.9,.07,.95),(1.9,.07,1.15),.012,'tirador corredera dormitorio',L,'inox',xf)

def bath(m,b,i):
 x,y,X,Y=b.bounds;L='08_BANOS_INTEGRADOS'
 m.ex(b,-.012,.012,'acabado baño '+str(i)+' cota 0',L,'ceramica',support='recrecido integrado bajo acabado')
 m.box(x+.04,Y-.86,-.025,.82,.82,.025,'plato ducha enrasado',L,'blanco',support='recrecido bajo cota 0')
 m.box(x+.05,Y-.16,-.006,.78,.025,.006,'canal ducha',L,'inox',support='plato enrasado')
 m.box(x+.89,Y-.83,0,.035,.78,.028,'perfil mampara a suelo',L,'inox',support='suelo')
 m.box(x+.90,Y-.82,.028,.018,.76,1.93,'mampara fija',L,'vidrio',support='perfil a suelo y fijación lateral')
 m.rod((x+.35,Y-.055,1.0),(x+.35,Y-.055,2.12),.014,'columna ducha',L,'inox')
 m.rod((x+.35,Y-.055,2.12),(x+.35,Y-.28,2.12),.015,'brazo rociador',L,'inox')
 m.ex(Point(x+.35,Y-.28).buffer(.09),2.10,.025,'rociador',L,'inox',support='brazo a pared')
 wc=Point(X-.35,Y-.47).buffer(.23,resolution=24)
 m.ex(wc,0,.37,'WC apoyado',L,'blanco',support='suelo')
 m.ex(wc,.37,.03,'asiento WC',L,'lino',support='cuerpo WC')
 m.box(X-.58,Y-.15,0,.46,.12,.78,'cisterna a suelo',L,'blanco',support='suelo y pared posterior')
 m.box(x+.04,y+.15,0,.40,.35,.76,'mueble lavabo 400x350',L,'madera',support='zócalo a suelo')
 outer=box(x+.04,y+.15,x+.44,y+.50);inner=box(x+.10,y+.21,x+.38,y+.43)
 m.ex(outer.difference(inner),.76,.09,'cuba lavabo borde',L,'blanco',support='mueble inferior')
 m.ex(inner,.76,.015,'fondo cuba lavabo',L,'blanco',support='cuba y mueble')
 m.rod((x+.24,y+.46,.84),(x+.24,y+.46,1.0),.014,'grifo lavabo',L,'inox')
 m.rod((x+.24,y+.46,1.0),(x+.24,y+.32,1.0),.014,'caño lavabo',L,'inox')
 # Two 450mm leaves park over the wall portions flanking the 900mm clear opening.
 for j,xx in enumerate([x+.05,x+.05]):
  m.box(xx,y+.015+j*.06,.015,.45,.04,2.10,'hoja baño ABIERTA',L,'madera',support='carros suspendidos')
  for xxx in [xx+.07,xx+.36]:m.rod((xxx,y+.035+j*.06,2.1),(xxx,y+.035+j*.06,2.15),.01,'carro puerta baño',L,'inox')
 m.box(x+.02,y-.005,2.15,1.61,.08,.05,'carril doble baño',L,'acero',support='dintel y pared integrada')

def kitchen(m,d):
 # Programme B is a real mirrored arrangement; the same local carcasses are reflected with it.
 mirror=d['variant']=='B';refl=rh.Transform.Mirror(rh.Point3d(0,0,0),rh.Vector3d(1,0,0)) if mirror else rh.Transform.Identity()
 rot=rh.Transform.Rotation(math.pi/2,rh.Vector3d(0,0,1),rh.Point3d(0,0,0));off=rh.Transform.Translation(3.45,-2.80,0)
 xf=rh.Transform.Multiply(refl,rh.Transform.Multiply(off,rot));L='09_COCINA_EQUIPADA'
 sink=box(.15,.10,.85,.52);work=box(0,0,3.20,.60)
 m.ex(work.difference(sink),.88,.035,'encimera con hueco real fregadero',L,'inox',xf,support='módulos bajos sobre patas')
 for i in range(6):
  x=i*.52;car=box(x+.01,.025,x+.51,.575);inner=box(x+.028,.043,x+.492,.557)
  m.ex(car.difference(inner),.10,.76,'costados módulo cocina',L,'azul',xf,support='cuatro pies regulables')
  m.ex(car,.10,.018,'suelo módulo cocina',L,'azul',xf,support='patas y costados')
  m.box(x+.01,.575,.10,.50,.018,.76,'frente cocina',L,'azul',xf,support='bisagras sobre costados')
  for xx in [x+.08,x+.44]:
   for yy in [.08,.52]:m.rod((xx,yy,0),(xx,yy,.10),.018,'pie regulable cocina',L,'acero',xf)
  m.rod((x+.13,.615,.75),(x+.39,.615,.75),.009,'tirador cocina',L,'inox',xf)
  for xx in [x+.13,x+.39]:m.rod((xx,.59,.75),(xx,.615,.75),.008,'separador tirador',L,'inox',xf)
 m.ex(sink,.72,.015,'fondo fregadero',L,'inox',xf,support='cuba')
 m.ex(sink.buffer(.018).difference(sink),.72,.16,'costados fregadero',L,'inox',xf,support='encimera')
 m.rod((.5,.06,.91),(.5,.06,1.18),.016,'grifo cocina',L,'inox',xf);m.rod((.5,.06,1.18),(.5,.29,1.18),.016,'caño cocina',L,'inox',xf)
 m.box(1.65,.04,.915,.68,.52,.012,'placa inducción',L,'acero',xf,support='encimera')
 for x in [1.82,2.16]:
  for y in [.18,.43]:m.ex(Point(x,y).buffer(.085),.927,.003,'zona inducción',L,'caucho',xf,support='placa')
 m.box(1.65,.596,.25,.65,.02,.47,'frente horno',L,'acero',xf,support='módulo horno')
 # Fridge in world programme coordinates.
 f=d['program']['fridge'];m.ex(f,0,2.02,'frigorífico',L,'blanco',support='patas integradas a suelo')

def shared(m,d):
 p=d['program'];L='06_ESTAR_COMER'
 for i,b in enumerate(p['baths'],1):bath(m,b,i)
 # Sofa is floor supported. A return at the bathroom wall shields both bathroom doors.
 x,y,X,Y=p['sofa'].bounds
 for xx in [x+.10,X-.10]:
  for yy in [y+.10,Y-.10]:m.rod((xx,yy,0),(xx,yy,.13),.022,'pata sofá',L,'acero')
 m.ex(p['sofa'],.13,.15,'bastidor sofá',L,'madera',support='cuatro patas')
 for j in range(2):m.box(x+.03,y+j*(Y-y)/2+.02,.28,X-x-.06,(Y-y)/2-.04,.16,'cojín estar',L,'rosa',support='bastidor')
 bx=x if d['variant']=='A' else X-.15
 m.box(bx,y,.28,.15,Y-y,.48,'respaldo sofá',L,'rosa',support='bastidor')
 m.ex(p['table'],.735,.035,'mesa comer y trabajo compartido 1600x850',L,'madera',support='cuatro patas')
 x,y,X,Y=p['table'].bounds
 for xx in [x+.1,X-.1]:
  for yy in [y+.1,Y-.1]:m.rod((xx,yy,0),(xx,yy,.735),.023,'pata mesa común',L,'acero')
 for s in p['stools']:stool(m,s.centroid.x,s.centroid.y)
 # Washer is under the kitchen counter; no freestanding laundry rack in the living room.
 kitchen(m,d)
 for w in d['common_windows']:
  phi=math.degrees(math.atan2(w['t'][1],w['t'][0]));xf=rh.Transform.Multiply(rh.Transform.Translation(*w['q'],0),rh.Transform.Rotation(math.radians(phi),rh.Vector3d(0,0,1),rh.Point3d(0,0,0)))
  glazing(m,-w['width']/2,w['width']/2,.06,1.04,2.55,xf,'ventana exterior espacio común')

def build(d):
 m=Model(d['code']);L='02_PAREDES_CONTINUAS'
 floor=d['floor'];walls=d['walls'];door=d['doors'];allwin=d['wincuts'].union(unary_union([w['cut'] for w in d['common_windows']]))
 # Gross structural footprint, with finish at Z=0. No vertical displacement between alternatives.
 m.ex(floor.buffer(.13,join_style=1),-.20,.20,'forjado acabado Z=0','01_SUELO','corcho',support='reserva de forjado, cálculo estructural pendiente')
 m.ex(walls.difference(door),0,.47,'zócalos y antepechos',L,'cal',support='forjado')
 # Bedroom windows start at .47; common windows have a higher sill behind the kitchen.
 commoncuts=unary_union([w['cut'] for w in d['common_windows']])
 m.ex(walls.difference(door).difference(d['wincuts']),.47,.57,'pared hasta antepecho común',L,'cal',support='zócalo')
 m.ex(walls.difference(door).difference(allwin),1.04,1.16,'paredes laterales huecos',L,'cal',support='paños inferiores')
 m.ex(walls.difference(allwin),2.20,.35,'dinteles RECTOS de puertas',L,'cal',support='jambas de cada hueco')
 m.ex(walls,2.55,.45,'coronación continua',L,'cal',support='muros y dinteles; sin certificación estructural')
 for r in d['rooms']:room(m,r)
 shared(m,d)
 ent=d['entry'];xf=tr(ent);A='10_ACCESO_REAL'
 # Exterior threshold is a separate platform, not a patio hidden in the useful housing area.
 m.ex(box(-.8,1.35,.8,2.75),-.20,.20,'rellano exterior acceso Z=0',A,'ceramica',xf,support='plataforma de acceso, conexión al complejo pendiente')
 for x in [-.64,.605]:m.box(x,1.37,0,.035,.07,2.25,'marco acceso a pared RECTA',A,'acero',xf,support='anclado a la jamba del cerramiento')
 m.box(-.64,1.37,2.215,1.28,.07,.035,'travesaño acceso',A,'acero',xf,support='dos jambas unidas al muro')
 m.box(-.64,1.43,.015,.035,1.20,2.18,'puerta acristalada ABIERTA 90 grados',A,'vidrio',xf,support='tres bisagras a la jamba; apertura sobre rellano exterior')
 for z in [.20,1.10,2.0]:m.rod((-.64,1.42,z),(-.64,1.42,z+.065),.018,'bisagra puerta acceso',A,'inox',xf)
 m.rod((-.60,2.50,.95),(-.60,2.50,1.15),.014,'tirador puerta acceso',A,'inox',xf)
 m.ex(floor.buffer(.06),3.0,.15,'cubierta oculta en posición real','91_CUBIERTA_OCULTA','blanco',visible=False,support='muros perimetrales; espesores estructurales aún de estudio')
 for name,cam in [('AXONOMETRIA',(18,-22,22)),('PLANTA',(0,0,40))]:
  v=rh.ViewInfo();v.Name=name;v.Viewport.SetCameraLocation(rh.Point3d(*cam));v.Viewport.SetCameraDirection(rh.Vector3d(-cam[0],-cam[1],-cam[2]+1));v.Viewport.SetCameraUp(rh.Vector3d(0,1,0) if name=='PLANTA' else rh.Vector3d(0,0,1));m.f.NamedViews.Add(v)
 m.f.Strings['Estado']='Corrección arquitectónica de las 40 alternativas: unidades aisladas. Fachadas y pasos comprobados geométricamente; SIN validación normativa, solar en parcela ni cálculo estructural.'
 m.f.Strings['Cambios']='Sin bicicleta ni tendedero interior, sin patios residuales, sin pilares aislados; camas rectangulares, puertas en frentes rectos y cuatro ventanas exteriores.'
 m.f.Strings['Dimensiones']='Metros; acabado z=0; cama 1.25x2m; mesa dibujo 1.8x0.9m; puerta dormitorio 1.0m; acceso 1.2m.'
 dest=P/'modelos'/(d['code']+'_CORREGIDA.3dm');assert m.f.Write(str(dest),8)
 f=rh.File3dm.Read(str(dest));errors=[]
 for o in f.Objects:
  if not o.Geometry.IsValid or (isinstance(o.Geometry,(rh.Extrusion,rh.Brep)) and not o.Geometry.IsSolid):errors.append(o.Attributes.Name)
 assert not errors,errors
 return {'code':d['code'],'objects':len(f.Objects),'invalid_or_open':errors,'floor_z':0,'bbox':[min(o.Geometry.GetTightBoundingBox().Min.Z for o in f.Objects),max(o.Geometry.GetTightBoundingBox().Max.Z for o in f.Objects)]}

if __name__=='__main__':
 codes=set(sys.argv[1:]);data=pickle.load(open(P/'datos'/('GEOMETRIA_MUESTRA.pkl' if '--muestra' in codes else 'GEOMETRIA_CORREGIDA.pkl'),'rb'));codes.discard('--muestra');reports=[]
 for d in data:
  if codes and d['code'] not in codes:continue
  r=build(d);reports.append(r);print(json.dumps(r),flush=True)
 (P/'verificacion/MODELOS.json').write_text(json.dumps(reports,indent=2))
