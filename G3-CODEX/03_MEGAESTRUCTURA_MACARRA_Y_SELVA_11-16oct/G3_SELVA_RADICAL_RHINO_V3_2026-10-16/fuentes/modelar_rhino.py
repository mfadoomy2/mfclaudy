# -*- coding: utf-8 -*-
# Runs inside Rhino 8 with RhinoCommon. It writes NEW files, never the current document.
from __future__ import unicode_literals
import Rhino as R, System, math, json, os, time, traceback
from System.Drawing import Color
from System.Collections.Generic import List
G=R.Geometry;D=R.DocObjects;P=G.Point3d;V=G.Vector3d;T=G.Transform
ROOT=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_RADICAL_RHINO_V3_2026-10-16'
S=json.load(open(os.path.join(ROOT,'fuentes','disposicion.json')))
F=R.FileIO.File3dm();F.Settings.ModelUnitSystem=R.UnitSystem.Meters
F.Settings.ModelAbsoluteTolerance=.001;F.Settings.ModelAngleToleranceRadians=math.radians(.1)
LAY={};MAT={};CAP=None;COUNTS={};ERRORS=[];META={'start':time.time(),'units':[],'people':[],'details':{},'source_people':u'/Volumes/T7/PERSONAS.3dm'}
COL={'MARFIL':(225,220,197),'AMARILLO':(224,183,24),'MAGENTA':(183,35,105),'CIAN':(46,145,165),'MADERA':(173,128,82),'CORCHO':(179,149,107),'VERDE':(114,153,131),'HOJAS':(64,106,68),'ACERO':(80,88,87),'BLANCO':(238,233,217),'VIDRIO':(185,210,199),'GRIS':(180,179,173),'TIERRA':(79,70,55),'NEGRO':(47,54,52),'LUZ':(255,228,166),'LINO':(209,202,177)}
def status(msg):
 with open(os.path.join(ROOT,'verificacion','progreso.txt'),'a') as f:f.write(time.strftime('%H:%M:%S')+' '+msg+'\n')
 print(msg)
def layer(name,col='MARFIL',visible=True):
 if name not in LAY:
  l=D.Layer();l.Name=name;l.Color=Color.FromArgb(*COL[col]);l.IsVisible=visible;F.AllLayers.Add(l);LAY[name]=F.AllLayers.Count-1
 return LAY[name]
def material(col,transparent=0):
 key=col+str(transparent)
 if key not in MAT:
  m=D.Material();m.Name=key;m.DiffuseColor=Color.FromArgb(*COL[col]);m.Transparency=transparent;m.Shine=30 if col in ['VIDRIO','ACERO','MAGENTA','AMARILLO'] else 8
  if col=='LUZ':m.EmissionColor=Color.FromArgb(*COL[col])
  F.AllMaterials.Add(m);MAT[key]=F.AllMaterials.Count-1
 return MAT[key]
def attrs(name,la,col='MARFIL',alpha=0):
 a=D.ObjectAttributes();a.Name=name;a.LayerIndex=layer(la,col);a.MaterialIndex=material(col,alpha);a.MaterialSource=D.ObjectMaterialSource.MaterialFromObject;a.ObjectColor=Color.FromArgb(*COL[col]);a.ColorSource=D.ObjectColorSource.ColorFromObject
 a.SetUserString('Proyecto','SELVA RADICAL V3');a.SetUserString('Estado','Anteproyecto geometrico; secciones por calcular')
 return a
def emit(g,name,la,col='MARFIL',alpha=0):
 global CAP
 if g is None:ERRORS.append('NULL '+name);return
 if not g.IsValid:
  if isinstance(g,G.Mesh):g.Faces.CullDegenerateFaces();g.Vertices.CombineIdentical(True,True);g.Normals.ComputeNormals()
  if not g.IsValid:ERRORS.append('INVALID '+name);return
 a=attrs(name,la,col,alpha)
 if CAP is not None:CAP[0].append(g);CAP[1].append(a)
 else:F.Objects.Add(g,a)
 COUNTS[la]=COUNTS.get(la,0)+1
 return g

def point(a):return a if isinstance(a,P) else P(*a)
def line(a,b,r,name,la='02_ESTRUCTURA_RAMAS',col='MARFIL'):
 a=point(a);b=point(b);v=b-a
 if v.Length<.0005:return
 return emit(G.Cylinder(G.Circle(G.Plane(a,v),r),v.Length).ToBrep(True,True),name,la,col)
def path(pts,r,name,la='02_ESTRUCTURA_RAMAS',col='MARFIL'):
 pts=[point(p) for p in pts]
 cr=G.Curve.CreateInterpolatedCurve(pts,3) if len(pts)>3 else G.PolylineCurve(pts)
 pipes=G.Brep.CreatePipe(cr,r,False,G.PipeCapMode.Round,True,.002,.05)
 for i,b in enumerate(pipes or []):emit(b,name+' '+str(i),la,col)
def tapered(pts,rr,name):
 pts=[point(p) for p in pts];cr=G.Curve.CreateInterpolatedCurve(pts,3);profiles=[]
 for i in range(9):
  t=cr.Domain.ParameterAt(i/8.0);p=cr.PointAt(t);v=cr.TangentAt(t);rad=rr[0]+(rr[1]-rr[0])*i/8.0
  profiles.append(G.Circle(G.Plane(p,v),rad).ToNurbsCurve())
 bb=G.Brep.CreateFromLoft(profiles,P.Unset,P.Unset,G.LoftType.Normal,False)
 if bb:
  b=bb[0].CapPlanarHoles(.001) or bb[0];emit(b,name,'02_ESTRUCTURA_RAMAS')
def box(x,y,z,w,d,h,name,la='20_MOBILIARIO',col='MADERA'):
 if min(w,d,h)<.00001:return
 return emit(G.Box(G.Plane.WorldXY,G.Interval(x,x+w),G.Interval(y,y+d),G.Interval(z,z+h)).ToBrep(),name,la,col)
def ball(x,y,z,r,name,la='21_ACCESORIOS',col='ACERO',scale=None):
 b=G.Sphere(P(x,y,z),r).ToBrep()
 if scale:b.Transform(T.Scale(G.Plane(P(x,y,z),V.ZAxis),scale[0],scale[1],scale[2]))
 return emit(b,name,la,col)
def roundcurve(x,y,w,d,rad,z=0):
 p=[P(x,y,z),P(x+w,y,z),P(x+w,y+d,z),P(x,y+d,z),P(x,y,z)]
 c=G.PolylineCurve(p)
 return G.Curve.CreateFilletCornersCurve(c,rad,.001,.02) or c

def flat_curves(curves,z,h,name,la,col):
 breps=G.Brep.CreatePlanarBreps(curves,.002)
 for i,b in enumerate(breps or []):
  ex=b.Faces[0].CreateExtrusion(G.LineCurve(P(0,0,0),P(0,0,h)),True)
  if ex:emit(ex,name+' '+str(i),la,col)
def extrude_curve(cr,h,name,la,col):
 e=G.Extrusion.Create(cr,h,True)
 if e:emit(e.ToBrep(),name,la,col)
def prism(polys,z,h,name,la='01_BANDEJAS',col='MADERA',zfun=None):
 for k,p in enumerate(polys):
  curves=[]
  for arr in [p['outer']]+p['holes']:
   pts=[P(x,y,z if zfun is None else zfun(x,y)) for x,y in arr]
   curves.append(G.PolylineCurve(pts))
  # All gallery polygons are split at the changes of gradient.
  flat_curves(curves,z,h,name+'_'+str(k),la,col)
def surf(points,nu,nv,name,la,col,alpha=0):
 s=G.NurbsSurface.CreateThroughPoints([point(p) for p in points],nu,nv,min(3,nu-1),min(3,nv-1),False,False)
 if s:emit(s.ToBrep(),name,la,col,alpha)

def begin():
 global CAP
 CAP=([],[])
def finish(name,desc):
 global CAP
 geos,ats=CAP;CAP=None
 idx=F.AllInstanceDefinitions.Add(name,desc,P.Origin,geos,ats)
 return F.AllInstanceDefinitions.FindName(name).Id

def inst(id,xf,name,la='10_UNIDADES',col='MARFIL'):
 return emit(G.InstanceReferenceGeometry(id,xf),name,la,col)
def xf(x,y,z,angle=0,center=None):
 rot=T.Rotation(math.radians(angle),V.ZAxis,P(*(center or [0,0,0])))
 return T.Translation(x,y,z)*rot

def chair(x,y,z=0,angle=0):
 inst(CHAIR,xf(x,y,z,angle),'Silla domestica 450 mm','20_MOBILIARIO')
def table(x,y,z,w=1.4,d=.75,name='Mesa de comer'):
 box(x,y,z+.73,w,d,.045,name+' tablero')
 for xx in [x+.08,x+w-.12]:
  for yy in [y+.08,y+d-.12]:line((xx,yy,z),(xx,yy,z+.73),.025,name+' pata','20_MOBILIARIO','ACERO')
def book(x,y,z,w=.04):
 box(x,y,z,w,.15,.22,'Libro','21_ACCESORIOS','VERDE')
def plant(x,y,z,hang=False):
 inst(PLANT,xf(x,y,z),'Maceta y follaje','30_VEGETACION','HOJAS')
 if hang:
  for j in range(3):
   pp=[(x+.1*j,y,z+.18),(x+.15+j*.08,y-.12,z-.3),(x+.05+j*.06,y-.19,z-.8),(x+.15,y-.25,z-1.5-j*.12)]
   path(pp,.006,'Hiedra colgante','30_VEGETACION','HOJAS')
   for k in range(6):
    zz=z-.18-k*.23;dx=(-1 if k%2 else 1)*.12
    surf([(x+dx,y-.14,zz+.09),(x+dx+.11,y-.23,zz),(x+dx+.03,y-.17,zz-.14),(x+dx-.06,y-.12,zz)],2,2,'Hoja hiedra','30_VEGETACION','HOJAS')

def bolt(x,y,z,axis=(0,0,1)):
 v=V(*axis);p=P(x,y,z);line(p,p+v*.035,.018,'Tornillo M20','04_UNIONES','ACERO')
def baseplate(x,y,z,size=.6):
 box(x-size/2,y-size/2,z,size,size,.035,'Placa de anclaje','04_UNIONES','ACERO')
 for dx in [-size*.34,size*.34]:
  for dy in [-size*.34,size*.34]:bolt(x+dx,y+dy,z+.035)
def clamp(a,b):
 a=point(a);b=point(b);v=b-a;v.Unitize();line(a,a+v*.16,.046,'Tensor manguito regulable','05_CABLES','ACERO');line(a+v*.16,b,.009,'Cable inox 18 mm','05_CABLES','ACERO')

def railing(coords,zfun,name='Barandilla',skip=None):
 # Continuous 1.10 m guard with non-climbable vertical infill, toe-board and bolted feet.
 for i in range(len(coords)-1):
  a=coords[i];b=coords[i+1];dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy)
  if L<.025:continue
  if abs(a[0]-b[0])<.00001 and (abs(a[0]-26)<.00001 or abs(a[0]-40)<.00001):continue
  mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
  if skip and skip(mid):continue
  za=zfun(*a);zb=zfun(*b)
  line((a[0],a[1],za+1.10),(b[0],b[1],zb+1.10),.024,name+' pasamanos','08_BARANDILLAS','AMARILLO')
  line((a[0],a[1],za+.11),(b[0],b[1],zb+.11),.018,name+' perfil inferior','08_BARANDILLAS','AMARILLO')
  n=max(1,int(math.ceil(L/1.1)))
  for j in range(n+1):
   f=j/float(n);x=a[0]+f*dx;y=a[1]+f*dy;z=zfun(x,y)
   line((x,y,z),(x,y,z+1.1),.022,name+' montante','08_BARANDILLAS','AMARILLO')
   if i%3==0:box(x-.045,y-.045,z,.09,.09,.012,'Pletina pie montante','04_UNIONES','ACERO')
  n=max(1,int(math.ceil(L/.105)))
  for j in range(1,n):
   f=j/float(n);x=a[0]+f*dx;y=a[1]+f*dy;z=zfun(x,y)
   line((x,y,z+.11),(x,y,z+1.08),.006,name+' barrotes luz menor 100 mm','08_BARANDILLAS','AMARILLO')

def truss(coords,zfun,name):
 # Welded yellow perimeter edge truss; depth 400 mm, diagonals alternate at 0.85 m.
 for i in range(len(coords)-1):
  a=coords[i];b=coords[i+1];L=math.hypot(b[0]-a[0],b[1]-a[1]);n=max(1,int(math.ceil(L/.85)))
  if abs(a[0]-b[0])<.00001 and (abs(a[0]-26)<.00001 or abs(a[0]-40)<.00001):continue
  za=zfun(*a);zb=zfun(*b)
  line((a[0],a[1],za-.09),(b[0],b[1],zb-.09),.038,name+' cordon superior','03_CELOSIAS','AMARILLO')
  line((a[0],a[1],za-.47),(b[0],b[1],zb-.47),.034,name+' cordon inferior','03_CELOSIAS','AMARILLO')
  for j in range(n):
   f=j/float(n);g=(j+1)/float(n);x=a[0]+f*(b[0]-a[0]);y=a[1]+f*(b[1]-a[1]);xx=a[0]+g*(b[0]-a[0]);yy=a[1]+g*(b[1]-a[1])
   line((x,y,zfun(x,y)-(.1 if j%2 else .45)),(xx,yy,zfun(xx,yy)-(.45 if j%2 else .1)),.018,name+' diagonal','03_CELOSIAS','AMARILLO')

try:
 status('INICIO: biblioteca de componentes y materiales')
 # Repeated detailed furniture blocks.
 begin()
 box(-.21,-.21,.43,.42,.42,.045,'Asiento','20_MOBILIARIO','MADERA')
 box(-.21,.17,.48,.42,.045,.35,'Respaldo','20_MOBILIARIO','MADERA')
 for x in [-.17,.17]:
  for y in [-.17,.17]:line((x,y,0),(x,y,.43),.016,'Pata silla','20_MOBILIARIO','ACERO')
 CHAIR=finish('MOB_SILLA','Silla con asiento respaldo y cuatro patas')
 begin()
 # Cylindrical flower pot, earth and twelve curved leaves, all actual geometry.
 emit(G.Cone(G.Plane(P(0,0,0),V.ZAxis),.38,.24).ToBrep(True),'Maceta','30_VEGETACION','CORCHO')
 emit(G.Cylinder(G.Circle(P(0,0,.33),.21),.025).ToBrep(True,True),'Tierra','30_VEGETACION','TIERRA')
 for j in range(14):
  a=j*2.399;h=.55+.2*math.sin(j);rr=.34+.14*math.cos(j*1.5);dx=math.cos(a);dy=math.sin(a);side=.095
  pts=[]
  for i in range(5):
   t=i/4.0;cx=dx*rr*t;cy=dy*rr*t;cz=.35+h*math.sin(t*1.65);ww=side*math.sin(math.pi*t)
   pts.extend([(cx-dy*ww,cy+dx*ww,cz),(cx+dy*ww,cy-dx*ww,cz+.015)])
  surf(pts,5,2,'Hoja nervada','30_VEGETACION','HOJAS')
 PLANT=finish('VEG_MACETA','Maceta con follaje NURBS')
 # Smooth tubular bedside luminaire.
 begin();line((0,0,0),(0,0,1.5),.014,'Pie lampara','23_ILUMINACION','ACERO')
 emit(G.Cone(G.Plane(P(0,0,1.8),-V.ZAxis),.27,.17).ToBrep(True),'Pantalla','23_ILUMINACION','LINO')
 ball(0,0,1.55,.07,'Bombilla','23_ILUMINACION','LUZ');LAMP=finish('LUZ_LAMPARA','Lampara completa con pantalla')
 # Room module with curved roof, clear opening and material layers.
 begin();status('HABITACION: cerramiento curvo, carpinteria y mobiliario')
 outer=roundcurve(0,0,3.7,3.8,.55);inner=roundcurve(.14,.14,3.42,3.52,.41)
 ring=G.Brep.CreatePlanarBreps([outer,inner],.001)[0]
 wall=ring.Faces[0].CreateExtrusion(G.LineCurve(P.Origin,P(0,0,2.35)),True)
 cutters=[G.Box(G.BoundingBox(P(1.35,3.45,-.01),P(2.4,4.1,2.18))).ToBrep(),G.Box(G.BoundingBox(P(.58,-.2,.7),P(3.12,.3,2.26))).ToBrep()]
 for cut in cutters:
  result=G.Brep.CreateBooleanDifference(wall,cut,.001)
  if result:wall=result[0]
 emit(wall,'H cerramiento curvo aislado espesor 140 mm','11_ENVOLVENTE_OPACA','CORCHO')
 # Native lofted roof, two skins separated by 60 mm; ribs remain outside.
 for dz,col,la in [(0,'VERDE','12_CUBIERTAS'),(-.06,'LINO','12_CUBIERTAS')]:
  sections=[]
  for y in [.05,1.0,2.7,3.75]:
   pts=[P(1.85+1.82*math.sin(-math.pi/2+j*math.pi/24),y,2.35+.79*math.cos(-math.pi/2+j*math.pi/24)+dz) for j in range(25)]
   sections.append(G.Curve.CreateInterpolatedCurve(pts,3))
  for b in G.Brep.CreateFromLoft(sections,P.Unset,P.Unset,G.LoftType.Normal,False):emit(b,'H cubierta curva doble piel','12_CUBIERTAS',col)
 for y in [.05,.48,.92,1.36,1.8,2.24,2.68,3.12,3.75]:
  pts=[(1.85+1.86*math.sin(-math.pi/2+j*math.pi/24),y,2.35+.85*math.cos(-math.pi/2+j*math.pi/24)) for j in range(25)]
  path(pts,.023,'H costilla curva exterior','13_COSTILLAS')
 for th in [-1.3,-.8,-.3,.3,.8,1.3]:
  x=1.85+1.87*math.sin(th);z=2.35+.86*math.cos(th)
  line((x,0,z),(x,3.8,z),.012,'H arriostramiento longitudinal','13_COSTILLAS')
 # Arched end glazing above the wall, framed in exact matching curves.
 for y in [.07,3.73]:
  arc=[P(1.85+1.82*math.sin(-math.pi/2+j*math.pi/30),y,2.35+.78*math.cos(-math.pi/2+j*math.pi/30)) for j in range(31)]
  cr=G.PolylineCurve(arc+[arc[0]])
  for b in G.Brep.CreatePlanarBreps(cr,.001) or []:emit(b,'H luneto vidrio','14_VIDRIOS','VIDRIO',.62)
 for x in [.58,1.85,3.12]:box(x-.025,.035,.67,.05,.06,1.62,'H montante ventana','15_CARPINTERIAS','MARFIL')
 for z in [.67,2.26]:box(.55,.035,z,2.6,.06,.045,'H travesano ventana','15_CARPINTERIAS')
 for x in [.61,1.88]:box(x,.065,.72,1.21,.018,1.49,'H ventana laminada','14_VIDRIOS','VIDRIO')
 # Door leaf, frame, hinges and lever, open 25 degrees into the room.
 box(1.30,3.61,0,.05,.16,2.21,'H jamba puerta','15_CARPINTERIAS','MADERA');box(2.40,3.61,0,.05,.16,2.21,'H jamba puerta','15_CARPINTERIAS','MADERA');box(1.30,3.61,2.18,1.15,.16,.05,'H dintel puerta','15_CARPINTERIAS','MADERA')
 # Leaf turns inward around left hinge; hardware follows the same transform.
 old=CAP;begin();box(1.35,3.65,0,1.05,.045,2.15,'H puerta 1.05 nominal','15_CARPINTERIAS','MADERA')
 line((2.25,3.60,1.0),(2.25,3.51,1.0),.012,'H manilla eje','21_ACCESORIOS');line((2.25,3.51,1),(2.36,3.51,1),.012,'H manilla palanca','21_ACCESORIOS')
 leaf=CAP;CAP=old;rot=T.Rotation(math.radians(-25),V.ZAxis,P(1.35,3.65,0))
 for g,a in zip(*leaf):g.Transform(rot);CAP[0].append(g);CAP[1].append(a)
 for z in [.25,1.75]:line((1.35,3.68,z),(1.35,3.68,z+.075),.012,'H bisagra','21_ACCESORIOS')
 # Bed: frame, slats, mattress, folded duvet, pillow, bedside storage.
 box(.26,.32,.12,1.14,2.08,.23,'H cama bastidor 1.10 x 2.00')
 for y in [.37+i*.16 for i in range(13)]:box(.29,y,.36,1.08,.055,.018,'H somier lama','20_MOBILIARIO','LINO')
 extrude_curve(roundcurve(.28,.34,1.10,2.0,.09,.38),.20,'H colchon','20_MOBILIARIO','BLANCO')
 box(.3,1.0,.59,1.06,1.27,.04,'H edredon','20_MOBILIARIO','LINO');ball(.83,.66,.65,.22,'H almohada','20_MOBILIARIO','BLANCO',(2.0,1,.3))
 box(1.48,.4,0,.42,.43,.48,'H mesilla');line((1.77,.37,.32),(1.88,.37,.32),.008,'H tirador mesilla','21_ACCESORIOS')
 # Desk, task chair and shelving.
 table(1.95,.30,0,1.4,.60,'H mesa estudio 1.40 x 0.60');chair(2.63,1.23,0,180)
 box(2.8,1.6,0,.65,1.45,2.32,'H armario')
 for yy in [1.62,2.31]:box(2.785,yy,.08,.018,.69,2.21,'H frente armario','20_MOBILIARIO','LINO');line((2.76,yy+.48,.95),(2.76,yy+.48,1.12),.008,'H tirador armario','21_ACCESORIOS')
 for z in [1.45,1.8]:box(1.7,.16,z,1.0,.23,.035,'H balda libros')
 for j in range(9):book(1.76+j*.07,.18,1.49,.04)
 # Socket, reading light and computer are geometric components.
 box(2.1,.16,.98,.09,.02,.07,'H enchufe doble','22_INSTALACIONES','BLANCO')
 box(2.2,.46,.81,.55,.035,.34,'H pantalla ordenador','21_ACCESORIOS','ACERO');box(2.2,.40,.78,.55,.23,.018,'H teclado','21_ACCESORIOS','ACERO')
 inst(LAMP,xf(1.62,1.15,0),'H lampara lectura','23_ILUMINACION')
 ROOM=finish('HABITACION_CURVA_12M2','Refugio privado con cerramiento curvo, puerta, cama, estudio y almacenamiento')
 # Wet room detailed block, exact 1.45 x 2.60 envelope, sliding door outside.
 begin()
 box(0,0,0,1.45,2.6,.035,'B pavimento continuo','16_BANOS','GRIS')
 box(0,0,.035,.08,2.6,2.5,'B tabique lateral','16_BANOS','BLANCO');box(1.37,0,.035,.08,2.6,2.5,'B tabique lateral','16_BANOS','BLANCO');box(0,0,.035,1.45,.08,2.5,'B cierre fondo','16_BANOS','BLANCO')
 box(.09,.10,.04,1.25,.9,.025,'B ducha enrasada','16_BANOS','GRIS');box(.17,.17,.065,1.04,.035,.009,'B canal drenaje','22_INSTALACIONES','ACERO')
 box(0.08,1.02,.05,.56,.08,1.95,'B mampara fija','14_VIDRIOS','VIDRIO')
 line((1.26,.4,1.05),(1.26,.4,2.12),.015,'B columna ducha','22_INSTALACIONES','ACERO');line((1.26,.4,2.12),(.95,.4,2.12),.012,'B rociador','22_INSTALACIONES','ACERO');ball(.95,.4,2.11,.07,'B alcachofa','22_INSTALACIONES','ACERO',(1,1,.2))
 ball(.91,1.55,.30,.25,'B taza inodoro','16_BANOS','BLANCO',(.8,1.3,1));ball(.91,1.55,.48,.24,'B asiento','16_BANOS','LINO',(.8,1.25,.12));box(.68,1.89,.05,.48,.16,.79,'B cisterna','16_BANOS','BLANCO')
 box(.13,1.9,.78,.5,.48,.06,'B lavabo','16_BANOS','BLANCO');path([(.35,2.22,.83),(.35,2.22,1.03),(.35,2.04,1.07),(.35,2.04,.98)],.012,'B grifo','22_INSTALACIONES','ACERO')
 box(.11,2.47,1.12,.58,.015,.78,'B espejo','16_BANOS','VIDRIO');box(.1,2.55,0,.91,.035,2.13,'B puerta corredera 0.90','15_CARPINTERIAS','MADERA');line((.4,2.5,.95),(.4,2.5,1.1),.009,'B tirador','21_ACCESORIOS');line((.08,2.57,2.17),(1.35,2.57,2.17),.015,'B guia puerta','15_CARPINTERIAS','ACERO')
 BATH=finish('BANO_DUCHA','Bano individual con puerta corredera ducha WC lavabo y griferia')
 # Domestic U4 block, intended to be edited with BlockEdit in Rhino.
 begin();status('UNIDAD U4: ensamblaje de cuatro refugios y casa comun')
 prism(S['unit_foot'],-.22,.22,'U4 suelo','01_BANDEJAS','MADERA')
 for i,(x,y,ang) in enumerate([(0,0,0),(6.6,0,0),(3.7,9.2,180),(10.3,9.2,180)]):inst(ROOM,xf(x,y,0,ang),'H%02d refugio privado'%(i+1),'10_UNIDADES')
 for x in [3.7,5.15]:inst(BATH,xf(x,0,0),'Bano de grupo','16_BANOS')
 # Lowered secondary beams remain entirely below the usable floor.
 for x in [.25,3.7,6.6,10.05]:line((x,.25,-.37),(x,8.95,-.37),.10,'U4 viga secundaria','03_CELOSIAS','AMARILLO')
 # Central living room: full glazing and double curved roof.
 for x in [3.72,6.58]:
  for y,h in [(2.65,1.15),(5.4,3.8)]:box(x-.02,y,0,.04,h,2.75,'U4 vidrio centro comun','14_VIDRIOS','VIDRIO')
 box(3.72,9.12,0,2.86,.035,2.75,'U4 frente comun','14_VIDRIOS','VIDRIO')
 for y in [2.65,4.6,6.7,9.13]:
  path([(3.72+2.86*j/16.,y,2.76+.39*math.sin(math.pi*j/16.)) for j in range(17)],.04,'U4 arco centro comun','13_COSTILLAS')
 pts=[(3.72+2.86*i/6.,2.65+(9.13-2.65)*j/4.,2.78+.39*math.sin(math.pi*i/6.)) for i in range(7) for j in range(5)]
 surf(pts,7,5,'U4 cubierta centro comun','12_CUBIERTAS','VERDE',.2)
 # Separate glazed entry doors preserve the domestic boundary.
 for x in [.03,10.27]:
  box(x,3.82,0,.035,1.0,2.18,'U4 puerta acceso corredera','14_VIDRIOS','VIDRIO');line((x,4.65,.94),(x,4.65,1.12),.012,'U4 tirador acceso','21_ACCESORIOS')
 # Kitchen located at far end, continuous clear cross passage at y3.8-5.4.
 for i in range(4):
  x=3.82+i*.64;box(x,8.45,0,.62,.63,.86,'C cocina mueble bajo');box(x,8.435,.06,.6,.018,.76,'C puerta mueble','20_MOBILIARIO','LINO');line((x+.18,8.40,.73),(x+.43,8.40,.73),.007,'C tirador','21_ACCESORIOS')
 box(3.8,8.42,.86,2.68,.68,.045,'C encimera','20_MOBILIARIO','BLANCO')
 box(3.88,8.49,.909,.6,.5,.006,'C fregadero inox','21_ACCESORIOS','ACERO');box(3.95,8.56,.918,.46,.36,.004,'C seno fregadero','21_ACCESORIOS','GRIS');path([(4.22,8.97,.91),(4.22,8.97,1.18),(4.22,8.75,1.2),(4.22,8.70,1.08)],.012,'C grifo cisne','22_INSTALACIONES','ACERO')
 for x in [5.54,5.96]:emit(G.Cylinder(G.Circle(P(x,8.77,.911),.14),.008).ToBrep(True,True),'C placa induccion','21_ACCESORIOS','NEGRO')
 box(6.03,7.65,0,.48,.65,1.9,'C frigorifico','20_MOBILIARIO','LINO');line((6,7.77,1.0),(6,7.77,1.3),.01,'C tirador frigorifico','21_ACCESORIOS')
 table(4.74,5.65,0,.82,1.60,'C mesa cuatro');chair(4.23,6.0,0,-90);chair(4.23,6.85,0,-90);chair(6.05,6.0,0,90);chair(6.05,6.85,0,90)
 for y in [5.95,6.75]:
  for x in [4.94,5.35]:emit(G.Cylinder(G.Circle(P(x,y,.79),.11),.012).ToBrep(True,True),'C plato','21_ACCESORIOS','BLANCO')
 box(5.9,2.85,.05,.55,.7,.4,'C banco umbral');plant(6.1,7.1,0)
 # Luminaires and exposed services along the wet-room edge.
 for x,y in [(5.15,4.5),(5.15,6.4),(5.15,8.0)]:
  line((x,y,2.8),(x,y,2.25),.005,'C suspension luminaria','23_ILUMINACION','ACERO');ball(x,y,2.18,.11,'C luz domestica','23_ILUMINACION','LUZ')
 for x in [3.8,5.15,6.5]:line((x,.15,-.30),(x,2.7,-.30),.035,'U4 ramal agua registrable','22_INSTALACIONES','CIAN')
 line((5.15,.1,-.34),(5.15,9.0,-.30),.055,'U4 colector desague pendiente','22_INSTALACIONES','CIAN')
 U4=finish('U4_CASA_COMUN_4_PERSONAS','Cuatro habitaciones privadas y centro comun, dos banos y cocina; editar con BlockEdit')
 status('PERSONAS: importar solo figuras extraidas de la biblioteca suministrada')
 people=R.FileIO.File3dm.Read(os.path.join(ROOT,'fuentes','personas_seleccionadas.3dm'));POSE={}
 for ob in people.Objects:
  begin();g=ob.Geometry.Duplicate();emit(g,'Figura original '+ob.Attributes.Name,'40_PERSONAS','NEGRO');pid=finish(ob.Attributes.Name,'Figura extraida de PERSONAS.3dm; escala y proporciones conservadas');POSE[int(ob.Attributes.Name.split('_')[1])]=pid
 def person(pose,x,y,z,angle=0,activity='Caminar'):
  inst(POSE[pose],xf(x,y,z,angle),'Persona '+activity,'40_PERSONAS','NEGRO');META['people'].append({'pose':pose,'position':[x,y,z],'activity':activity})
 # Main scene, closed floor = ten domestic groups; the generation image is the formal reference.
 status('CONJUNTO: plataformas curvas y unidades giradas')
 prism(S['site'],-.50,.5,'Solar Ribera31','00_PARCELA','GRIS')
 for u in S['units']:
  inst(U4,xf(u['x'],u['y'],u['z'],u['angle'],[5.15,4.6,0]),u['id']+' casa de cuatro','10_UNIDADES')
  META['units'].append({'id':u['id'],'level':u['z'],'people':4,'angle':u['angle']})
  # World coordinates for local detail and people.
  th=math.radians(u['angle'])
  def up(x,y,z=0):return (u['x']+5.15+(x-5.15)*math.cos(th)-(y-4.6)*math.sin(th),u['y']+4.6+(x-5.15)*math.sin(th)+(y-4.6)*math.cos(th),u['z']+z)
  for x,y,pose,ang in [(5.2,7.7,30,180),(1.9,2.5,25,110)]:
   q=up(x,y);person(pose,*q,angle=ang+u['angle'],activity=u['id']+' vida domestica')
  # Splayed perimeter support ribs and suspension fittings, never through a room.
  for x in [.1,10.2]:
   for y in [.2,9.0]:
    a=up(x,y,-.35);b=up(x,y,3.25);clamp(a,b)
  # Local external sail over the centre; top floor has tall, visibly anchored masts.
  top=u['id'] in ['U09','U10'];lift=4.75 if top else 3.34
  corners=[up(-.18,-.15,lift+.65 if top else lift+.15),up(10.48,-.15,lift+.15),up(10.48,9.35,lift+.75 if top else lift+.18),up(-.18,9.35,lift+.08)]
  # Two separate hypar sails, leaving a longitudinal open seam for sky and smoke.
  for half in [0,1]:
   local=[(-.18,.15),(4.95,.15),(4.95,9.05),(-.18,9.05)] if half==0 else [(5.35,.15),(10.48,.15),(10.48,9.05),(5.35,9.05)]
   cp=[up(x,y,lift+(.6 if top and i in [0,2] else .1 if i in [0,2] else -.12)) for i,(x,y) in enumerate(local)]
   pts=[]
   for i in range(7):
    a=i/6.
    for j in range(9):
     b=j/8.;vv=[(1-a)*(1-b),a*(1-b),a*b,(1-a)*b];q=[sum(vv[k]*cp[k][d] for k in range(4)) for d in range(3)];q[2]-=.18*math.sin(math.pi*a)*math.sin(math.pi*b);pts.append(q)
   surf(pts,7,9,u['id']+' vela anticlástica','06_VELAS','VERDE',.40)
   for i in range(4):
    a=cp[i];b=cp[(i+1)%4];mid=[(a[d]+b[d])/2 for d in range(3)];mid[2]-=.10
    path([a,[(2*a[d]+b[d])/3 for d in range(3)],mid,[(a[d]+2*b[d])/3 for d in range(3)],b],.012,'Borde tensado vela','05_CABLES','ACERO')
    low=(a[0],a[1],u['z']-.2);line(low,a,.032,'Mastil vela','06_VELAS');baseplate(a[0],a[1],u['z'],.22)
  # Fixtures to pull the membrane edges away from the domestic shell.
  for x,y in [(-.15,.15),(10.45,.15),(-.15,9.0),(10.45,9.0)]:
   q=up(x,y);plant(q[0],q[1],q[2],True)
 status('GALERIAS: perfil continuo con pendientes y celosias amarillas')
 def floorz(x,y,z):return z+.6*max(0,min(1,(x-26.0)/14.0))
 for deck in S['decks']:
  z=deck['z_left'];zf=lambda x,y:floorz(x,y,z)
  prism(deck['shape'],z,-.19,'Galeria G'+str(deck['level']+1),'07_GALERIAS','MADERA',zf)
  # Edges adjacent to a private foot are not balustraded across a threshold.
  doors=[u['entry'] for u in S['units'] if abs(u['z']-z)<.01 or abs(u['z']-z-.6)<.01]
  feet=[p['outer'] for u in S['units'] if abs(u['z']-z)<.01 or abs(u['z']-z-.6)<.01 for p in u['foot']]
  def near_private(q):
   for pp in feet:
    for a,b in zip(pp,pp[1:]):
     dx=b[0]-a[0];dy=b[1]-a[1];l=dx*dx+dy*dy;t=max(0,min(1,((q[0]-a[0])*dx+(q[1]-a[1])*dy)/l)) if l else 0
     if math.hypot(q[0]-a[0]-t*dx,q[1]-a[1]-t*dy)<.13:return True
   return False
  for p in deck['shape']:
   railing(p['outer'],zf,'G'+str(deck['level']+1),near_private);truss(p['outer'],zf,'G'+str(deck['level']+1))
  for x,y,pose in [(23,-6.0,19),(35,-6.1,43),(49,-5.0,42)]:person(pose,x,y,zf(x,y),30,'recorrer galeria')
 for terr in S['terraces']:
  z=terr['z'];prism(terr['shape'],z,-.16,'Terraza '+terr['unit'],'01_BANDEJAS','MADERA')
  for p in terr['shape']:
   truss(p['outer'],lambda x,y:z,'Bandeja '+terr['unit'])
   # Guard removed at the two domestic entrances and the gallery connections.
   u=next(t for t in S['units'] if t['id']==terr['unit']);ex,ey=u['entry']
   railing(p['outer'],lambda x,y:z,'Terraza',lambda q:abs(q[0]-ex)<1.5 and abs(q[1]-ey)<1.0)
 status('ARBOLES PORTANTES: troncos curvos ramificados y anclajes')
 # Primary trees stand outside domestic room footprints. Branch fans carry front edges.
 for ti,(x,y) in enumerate([(24.8,-4.76),(37.3,-5.10),(24.0,7.65),(37.5,5.65)]):
  pts=[(x-.6,y,.05),(x-.35,y+.08,4.5),(x+.2,y-.05,10),(x-.15,y+.05,16),(x,y,24.3)]
  tapered(pts,[.33,.15],'ARBOL %d tronco NURBS'%(ti+1));baseplate(x-.6,y,0,.95)
  for k,z in enumerate(S['levels']):
   zz=z+(.6 if ti in [1,3] else 0)
   u=S['units'][2*k+(ti%2)];p=u['foot'][0]['outer'];minx=min(v[0] for v in p);maxx=max(v[0] for v in p);miny=min(v[1] for v in p);maxy=max(v[1] for v in p)
   ey=(miny-.1 if ti<2 else maxy+.12)
   for bx in [minx+.6,maxx-.6]:
    tapered([(x,y,zz-2.45),(x+(bx-x)*.23,y+(ey-y)*.1,zz-1.6),(x+(bx-x)*.65,y+(ey-y)*.5,zz-.80),(bx,ey,zz-.48)],[.17,.075],'ARBOL %d rama planta%d'%(ti+1,k+1))
    baseplate(bx,ey,zz-.44,.30)
  # Visible magenta infrastructure is parallel to the tree, not hidden in arbitrary roots.
  path([(a+.55,b+.1,c) for a,b,c in pts],.065,'Montante pluvial registrable','22_INSTALACIONES','MAGENTA')
  for z in [1,4,7,10,13,16,19,22]:
   line((x+.45,y,z),(x+.69,y,z),.014,'Abrazadera montante','04_UNIONES','ACERO')
 status('NUCLEOS: escaleras completas y ascensor detallado')
 # Main stair, two flights per storey. Upper rear stair tracks right-platform levels.
 def stairs(x,y,levels,tag):
  levels=[0]+levels
  for k,z in enumerate(levels):
   box(x,y,z-.18,3.0,1.5,.18,tag+' rellano acceso','09_ESCALERAS','GRIS')
   box(x,y+4.8,z-.18,3.0,1.5,.18,tag+' rellano llegada','09_ESCALERAS','GRIS')
   if k==len(levels)-1:continue
   dz=levels[k+1]-z;rise=dz/22.;tread=.30
   for j in range(11):
    zz=z+(j+1)*rise;box(x+.1,y+1.5+j*tread,zz-.10,1.2,tread+.015,.10,tag+' tramo A huella300','09_ESCALERAS','AMARILLO')
    zz=z+dz/2+(j+1)*rise;box(x+1.7,y+1.5+(10-j)*tread,zz-.10,1.2,tread+.015,.10,tag+' tramo B huella300','09_ESCALERAS','AMARILLO')
   box(x+.1,y+4.8,z+dz/2-.18,2.8,1.4,.18,tag+' meseta intermedia','09_ESCALERAS','GRIS')
   # Sloping stringers and continuous handrails along both flights.
   for xx in [x+.12,x+1.28]:
    line((xx,y+1.5,z+.08),(xx,y+4.8,z+dz/2),.065,tag+' zanca A','09_ESCALERAS','MARFIL')
    line((xx,y+1.5,z+1.10),(xx,y+4.8,z+dz/2+1.10),.025,tag+' pasamanos A','08_BARANDILLAS','AMARILLO')
   for xx in [x+1.72,x+2.88]:
    line((xx,y+4.8,z+dz/2+.08),(xx,y+1.5,z+dz),.065,tag+' zanca B','09_ESCALERAS')
    line((xx,y+4.8,z+dz/2+1.10),(xx,y+1.5,z+dz+1.10),.025,tag+' pasamanos B','08_BARANDILLAS','AMARILLO')
   for j in range(23):
    yy=y+1.5+3.3*j/22.;zz=z+rise+(dz/2-rise)*j/22.
    for xx in [x+.12,x+1.28]:line((xx,yy,zz),(xx,yy,zz+1.08),.008,tag+' barrotes A','08_BARANDILLAS','AMARILLO')
    zz=z+dz-(dz/2-rise)*j/22.
    for xx in [x+1.72,x+2.88]:line((xx,yy,zz),(xx,yy,zz+1.08),.008,tag+' barrotes B','08_BARANDILLAS','AMARILLO')
  # Enclosure geometry with door openings; performance is to be specified in the fire project.
  top=levels[-1]+3.4
  box(x-.12,y,-.2,.12,6.3,top+.2,tag+' pared lateral','17_NUCLEOS','MARFIL');box(x+3,y,-.2,.12,6.3,top+.2,tag+' pared lateral','17_NUCLEOS','MARFIL');box(x,y+6.25,0,3,.10,top,tag+' frente fondo','17_NUCLEOS','MARFIL')
  for z in levels:
   box(x,y-.07,z,1.7,.10,3.3,tag+' frente opaco','17_NUCLEOS','MARFIL');box(x+2.75,y-.07,z,.25,.10,3.3,tag+' jamba','17_NUCLEOS','MARFIL');box(x+1.7,y-.07,z+2.2,1.05,.10,1.10,tag+' dintel','17_NUCLEOS','MARFIL')
   box(x+1.72,y-.01,z,.98,.045,2.17,tag+' puerta salida','15_CARPINTERIAS','VERDE');line((x+1.8,y-.08,z+1.0),(x+2.53,y-.08,z+1.0),.016,tag+' barra salida','21_ACCESORIOS','ACERO')
  return levels
 stairs(14.0,-6.5,S['levels'],'N1')
 stairs(54.0,-5.7,[z+.6 for z in S['levels']],'N2')
 # Front lift: 1.40 x 1.60 clear cabin, 0.90 m clear centre opening.
 ex,ey=17.05,-6.80;shaftw,shaftd=2.3,2.35;liftstops=[0]+S['levels'];top=liftstops[-1]+3.7
 box(ex-.15,ey-.15,-1.25,2.6,2.65,.25,'ASC foso losa','18_ASCENSOR','GRIS')
 for xx in [ex,ex+shaftw]:
  for yy in [ey,ey+shaftd]:
   box(xx-.045,yy-.045,-1.0,.09,.09,top+1.1,'ASC montante SHS90','18_ASCENSOR','MAGENTA')
 for z in [-.8]+liftstops+[top]:
  for a,b in [((ex,ey,z),(ex+shaftw,ey,z)),((ex,ey,z),(ex,ey+shaftd,z)),((ex+shaftw,ey,z),(ex+shaftw,ey+shaftd,z))]:line(a,b,.038,'ASC travesano','18_ASCENSOR','MAGENTA')
 # Two side glazing planes and one rear, segmented to keep all landing doors free.
 box(ex,ey,-.8,.015,shaftd,top+.8,'ASC vidrio lateral','19_ASCENSOR_VIDRIO','VIDRIO');box(ex+shaftw,ey,-.8,.015,shaftd,top+.8,'ASC vidrio lateral','19_ASCENSOR_VIDRIO','VIDRIO');box(ex,ey,-.8,shaftw,.015,top+.8,'ASC vidrio posterior','19_ASCENSOR_VIDRIO','VIDRIO')
 # Guides, counterweight and buffers are real distinct objects.
 for xx in [ex+.16,ex+2.1]:
  box(xx,ey+.38,-.9,.075,.075,top+.7,'ASC guia vertical','18_ASCENSOR','ACERO')
  for z in range(0,int(top),2):box(xx-.05,ey+.31,z,.18,.12,.06,'ASC soporte guia','04_UNIONES','ACERO')
 box(ex+.4,ey+.12,7.3,.9,.14,2.2,'ASC contrapeso','18_ASCENSOR','ACERO')
 for xx in [ex+.68,ex+1.58]:
  line((xx,ey+.32,-1.0),(xx,ey+.32,-.45),.08,'ASC amortiguador foso','18_ASCENSOR','MAGENTA')
 # Cabin stands at +3.80 for inspection, with open doors and no cabin duplicated on other floors.
 cz=3.8;cx=ex+.44;cy=ey+.46
 box(cx-.08,cy-.08,cz-.15,1.56,1.76,.15,'ASC cabina suelo','18_ASCENSOR','GRIS');box(cx-.08,cy-.08,cz+2.23,1.56,1.76,.10,'ASC techo cabina','18_ASCENSOR','MARFIL')
 box(cx-.035,cy,cz,.035,1.6,2.23,'ASC cabina lateral','19_ASCENSOR_VIDRIO','VIDRIO');box(cx+1.4,cy,cz,.035,1.6,2.23,'ASC cabina lateral','19_ASCENSOR_VIDRIO','VIDRIO');box(cx,cy,cz,1.4,.035,2.23,'ASC cabina fondo','19_ASCENSOR_VIDRIO','VIDRIO')
 line((cx+.08,cy+.10,cz+.90),(cx+1.32,cy+.10,cz+.90),.018,'ASC pasamanos cabina','18_ASCENSOR','ACERO')
 box(cx+1.35,cy+.45,cz+.8,.025,.24,.46,'ASC botonera cabina','18_ASCENSOR','ACERO')
 for j in range(6):ball(cx+1.32,cy+.52+(j%2)*.11,cz+.87+(j//2)*.09,.018,'ASC boton cabina','18_ASCENSOR','LUZ')
 for z in liftstops:
  doorx=ex+.70;doorY=ey+shaftd
  box(ex+.1,doorY,z,.52,.12,2.3,'ASC jamba landing','18_ASCENSOR','MAGENTA');box(ex+1.67,doorY,z,.53,.12,2.3,'ASC jamba landing','18_ASCENSOR','MAGENTA');box(ex+.62,doorY,z+2.15,1.05,.12,.15,'ASC dintel puerta','18_ASCENSOR','MAGENTA')
  if abs(z-cz)>.01:
   for xx in [doorx,doorx+.45]:box(xx,doorY+.025,z,.448,.025,2.14,'ASC puerta automatica cerrada','18_ASCENSOR','ACERO')
  else:
   box(doorx-.42,doorY+.025,z,.42,.025,2.14,'ASC hoja abierta izquierda','18_ASCENSOR','ACERO');box(doorx+.90,doorY+.025,z,.42,.025,2.14,'ASC hoja abierta derecha','18_ASCENSOR','ACERO')
  box(doorx,doorY+.15,z-.025,.9,.18,.025,'ASC umbral enrasado','18_ASCENSOR','ACERO');box(ex+.18,doorY+.13,z+.91,.12,.035,.25,'ASC pulsador rellano','18_ASCENSOR','ACERO');ball(ex+.24,doorY+.17,z+1.03,.024,'ASC llamada','18_ASCENSOR','LUZ')
  box(ex+.95,doorY+.14,z+2.36,.46,.035,.16,'ASC indicador planta','18_ASCENSOR','NEGRO')
  box(ex-.02,doorY+.15,z-.18,2.42,1.80,.18,'ASC rellano giro 1.80','07_GALERIAS','MADERA')
  # Route from the lift lobby to the west domestic branch at same elevation.
  box(18.55,-2.95,z-.17,.9,1.4,.17,'ASC enlace rellano-galeria','07_GALERIAS','MADERA')
 # Motor and traction wheels in overhead, with actual ropes to cabin/counterweight.
 line((ex+.7,ey+.6,top-.6),(ex+1.55,ey+.6,top-.6),.20,'ASC maquina traccion','18_ASCENSOR','ACERO')
 for xx in [ex+.8,ex+.95,ex+1.1,ex+1.25]:line((xx,ey+.6,cz+2.4),(xx,ey+.6,top-.6),.006,'ASC cable traccion','18_ASCENSOR','ACERO')
 person(34,cx+.7,cy+.8,cz,0,'usar ascensor')
 META['details']['lift']={'clear_cabin':[1.4,1.6],'clear_door':.90,'pit_depth':1.0,'stops':liftstops,'cabin_level':cz,'overhead':3.7}
 # Distributed community rooms with doors and actual use-specific furnishings.
 status('PROGRAMA: cantina taller aula cuidados y lavanderia')
 for pr in S['program']:
  z=pr['z'];p=pr['shape'];prism(p,z-.2,.2,pr['id']+' suelo','24_COMUNES','MADERA')
  x,y=45.8,-3.7;w,d=7.0,4.9
  for xx in [x,x+w]:box(xx,y,z,.08,d,2.85,pr['id']+' lateral','14_VIDRIOS','VIDRIO')
  box(x,y+d,z,w,.08,2.85,pr['id']+' fondo','14_VIDRIOS','VIDRIO')
  box(x,y,z,w,.08,1.05,pr['id']+' antepecho','24_COMUNES','CORCHO');box(x+1.0,y-.01,z,.9,.035,2.2,pr['id']+' puerta','14_VIDRIOS','VIDRIO')
  for xx in [x,x+2.33,x+4.66,x+7]:line((xx,y,z),(xx,y,z+3.1),.045,pr['id']+' montante','24_COMUNES')
  if pr['id']=='CUIDADOS_LAVADO':
   for j in range(3):
    xx=x+.25+j*.7;box(xx,y+3.95,z,.64,.65,.88,'COM lavadora','24_COMUNES','BLANCO');ball(xx+.32,y+3.92,z+.45,.23,'COM tambor lavadora','24_COMUNES','ACERO',(1,.08,1));box(xx+.4,y+3.92,z+.77,.12,.02,.06,'COM mando lavadora','24_COMUNES','NEGRO')
   table(x+.4,y+.5,z,2.4,.8,'COM acogida');box(x+5,y+3,z,1.5,.7,.45,'COM banco cuidados');plant(x+6.3,y+3.8,z)
  else:
   for yy in [y+.8,y+2.9]:
    table(x+1.2,yy,z,3.3,.85,pr['id']+' mesa comun')
    for xx in [x+1.7,x+2.7,x+3.7]:chair(xx,yy-.5,z,0);chair(xx,yy+1.35,z,180)
   for j in range(10):book(x+.2+j*.12,y+4.3,z+1.2)
   for h in [.5,1.1,1.7,2.3]:box(x+.1,y+4.2,z+h,2.3,.35,.045,'COM estanteria herramientas')
  # Curved perforated roof for larger rooms with two ventilation clerestories.
  pts=[(x+w*i/8.,y+d*j/4.,z+2.85+.45*math.sin(math.pi*i/8.)) for i in range(9) for j in range(5)]
  surf(pts,9,5,pr['id']+' cubierta','12_CUBIERTAS','VERDE',.12)
  plant(x+.6,y+3.7,z,True);plant(x+6.1,y+.6,z,True)
  person(45,x+5.1,y+2.3,z,20,pr['id']);person(25,x+3.2,y+1.9,z,150,pr['id'])
 # Ground public path, seating, bicycle stands and planted edges.
 box(12.6,-1.1,.015,6.4,2.0,.025,'Acceso principal sin escalon','00_PARCELA','MADERA')
 for j in range(5):
  x=20+j*1.05;path([(x,-4.9,0),(x,-4.9,.7),(x+.52,-4.9,.7),(x+.52,-4.9,0)],.022,'Aparcabicis U','25_URBANIZACION','ACERO')
 for x in [26,29,42,51]:plant(x,-3.7,0)
 for x,y in [(13.4,.1),(19,-5.7),(33,-6),(49,-4.8)]:person(19,x,y,0,45,'planta baja y llegada')
 # Context preserved in an independent, initially hidden layer for uncluttered opening.
 status('CONTEXTO Y ARCHIVOS: generar modelos de conjunto y unidad')
 layer('90_CONTEXTO','GRIS',False)
 for ct in S['context']:
  m=G.Mesh()
  for v in ct['vertices']:m.Vertices.Add(*v)
  for i in range(0,len(ct['vertices']),3):m.Faces.AddFace(i,i+1,i+2)
  m.Faces.CullDegenerateFaces();m.Normals.ComputeNormals();emit(m,'Edificio vecino '+ct['id'],'90_CONTEXTO','GRIS')
 # Editable reference axes and exact parcel curve, hidden unless requested.
 layer('91_EJES_CONTROL','CIAN',False)
 for u in S['units']:
  a=u['entry'];emit(G.LineCurve(P(a[0],a[1],u['z']),P(a[0],a[1],u['z']+2.2)),u['id']+' acceso','91_EJES_CONTROL','CIAN')
 # Views stored directly in the 3dm file.
 def savedview(name,loc,target):
  vi=D.ViewInfo();vi.Name=name;vp=vi.Viewport;vp.SetCameraLocation(P(*loc));vp.SetCameraDirection(P(*target)-P(*loc));vp.SetCameraUp(V.YAxis if name=='05_PLANTA' else V.ZAxis);vp.TargetPoint=P(*target);vp.ChangeToParallelProjection(True);vp.Extents(1.5,G.BoundingBox(P(12,-8,0),P(59,13,27)));F.AllNamedViews.Add(vi)
 savedview('01_AXONOMETRIA_RADICAL',(92,-100,69),(35,0,12))
 savedview('02_FRENTE_HABITADO',(35,-90,20),(35,0,12))
 savedview('03_REVERSO',(80,90,65),(35,0,12))
 savedview('04_DETALLE_ASCENSOR',(8,-19,11),(18,-4.5,4.5))
 savedview('05_PLANTA',(35,0,100),(35,0,0))
 F.ApplicationName='Rhino 8 / SELVA RADICAL V3';F.ApplicationDetails='Native RhinoCommon NURBS Breps, block furniture and selected supplied people.'
 pathout=os.path.join(ROOT,'modelos','SELVA_RADICAL_COMPLETA_V3.3dm');ok=F.Write(pathout,8)
 if not ok:raise Exception('No se ha podido escribir el modelo principal')
 # Standalone editable U4 includes every definition and layer, without extraneous scene objects.
 ids=[ob.Attributes.ObjectId for ob in F.Objects if not ob.Attributes.IsInstanceDefinitionObject]
 for id in ids:F.Objects.Delete(id)
 inst(U4,T.Identity,'U4 UNIDAD COMPLETA','10_UNIDADES')
 F.Write(os.path.join(ROOT,'modelos','UNIDAD_CURVA_U4_DETALLE_V3.3dm'),8)
 META['seconds']=time.time()-META['start'];META['counts_by_layer']=COUNTS;META['geometry_errors']=ERRORS;META['objects_main_before_unit_export']=sum(COUNTS.values());META['architecture']='native NURBS Breps and solids; meshes only supplied people, context and leaves where explicitly noted'
 with open(os.path.join(ROOT,'verificacion','construccion_nativa.json'),'w') as out:json.dump(META,out,indent=2)
 status('TERMINADO '+str(int(META['seconds']))+' segundos; errores='+str(len(ERRORS)))
except Exception as e:
 with open(os.path.join(ROOT,'verificacion','ERROR_RHINO.txt'),'w') as f:f.write(traceback.format_exc())
 status('ERROR '+str(e))
 raise
