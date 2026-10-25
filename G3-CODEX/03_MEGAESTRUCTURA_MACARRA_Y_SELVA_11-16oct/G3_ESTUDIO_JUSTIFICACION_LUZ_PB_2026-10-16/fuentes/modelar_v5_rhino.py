# -*- coding: utf-8 -*-
# Runs inside Rhino 8 with RhinoCommon. It writes NEW files, never the current document.
from __future__ import unicode_literals
import Rhino as R, System, math, json, os, time, traceback
from System.Drawing import Color
from System.Collections.Generic import List
G=R.Geometry;D=R.DocObjects;P=G.Point3d;V=G.Vector3d;T=G.Transform
ROOT=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16'
S=json.load(open(os.path.join(ROOT,'calculo','ESTRUCTURA_RESULTADOS.json')))
DEFS={};RENDER={};MP=G.MeshingParameters.FastRenderMesh;MP.RefineGrid=True;MP.SimplePlanes=True;MP.Tolerance=.008
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
 if col=='VIDRIO' and transparent==0:transparent=.85
 key=col+str(transparent)
 if key not in MAT:
  m=D.Material();m.Name=key;m.DiffuseColor=Color.FromArgb(*COL[col]);m.Transparency=transparent;m.Shine=30 if col in ['VIDRIO','ACERO','MAGENTA','AMARILLO'] else 8
  if col=='LUZ':m.EmissionColor=Color.FromArgb(*COL[col])
  F.AllMaterials.Add(m);MAT[key]=F.AllMaterials.Count-1
 return MAT[key]
def attrs(name,la,col='MARFIL',alpha=0):
 a=D.ObjectAttributes();a.Name=name;a.LayerIndex=layer(la,col);a.MaterialIndex=material(col,alpha);a.MaterialSource=D.ObjectMaterialSource.MaterialFromObject;a.ObjectColor=Color.FromArgb(*COL[col]);a.ColorSource=D.ObjectColorSource.ColorFromObject
 a.SetUserString('Proyecto','SELVA V5 ENSAYO LUZ Y PROGRAMA');a.SetUserString('Estado','Anteproyecto con predimensionado preliminar; no certificado')
 return a
def emit(g,name,la,col='MARFIL',alpha=0):
 global CAP
 if g is None:ERRORS.append('NULL '+name);return
 if not g.IsValid:
  if isinstance(g,G.Mesh):g.Faces.CullDegenerateFaces();g.Vertices.CombineIdentical(True,True);g.Normals.ComputeNormals()
  if not g.IsValid:ERRORS.append('INVALID '+name);return
 a=attrs(name,la,col,alpha)
 if isinstance(g,G.Brep):
  ms=G.Mesh.CreateFromBrep(g,MP)
  if ms and len(ms)==g.Faces.Count:
   for face,m in zip(g.Faces,ms):face.SetMesh(G.MeshType.Render,m)
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
 DEFS[name]=(geos,ats)
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
 v=V(*axis);p=P(x,y,z);line(p,p+v*.035,.015,'Tornillo M30','04_UNIONES','ACERO')
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
 status('PABELLON V5: cuatro habitaciones al frente norte y servicios al sur')
 begin()
 def vault(y,dx=0,dz=0):
  pts=[P(-4.8-dx,y,0),P(-4.8-dx,y,2.20)]+[P(-(4.8+dx)*math.cos(j*math.pi/32),y,2.20+(2.1+dz)*math.sin(j*math.pi/32)) for j in range(33)]+[P(4.8+dx,y,0)]
  return G.Curve.CreateInterpolatedCurve(pts,3)
 for ya,yb,col,la,al in [(-.7,.7,'VERDE','12_CUBIERTAS',0),(.7,1.3,'VIDRIO','14_VIDRIOS',.88),(1.3,1.7,'VERDE','12_CUBIERTAS',0),(1.7,2.9,'VIDRIO','14_VIDRIOS',.88),(2.9,5.0,'VERDE','12_CUBIERTAS',0),(5.0,5.9,'VIDRIO','14_VIDRIOS',.88),(5.9,6.8,'VERDE','12_CUBIERTAS',0)]:
  for b in G.Brep.CreateFromLoft([vault(ya),vault((ya+yb)/2),vault(yb)],P.Unset,P.Unset,G.LoftType.Normal,False):emit(b,'V5 piel termica / banda cenital',la,col,al)
 for j in range(17):
  cr=vault(-.7+7.5*j/16,.07,.05)
  for b in G.Brep.CreatePipe(cr,.05715,False,G.PipeCapMode.Flat,True,.002,.05):emit(b,'V5 costilla exocasco CHS114.3x6.3','13_COSTILLAS')
 for t in [j*math.pi/18 for j in range(1,18)]:
  x=-4.89*math.cos(t);zz=2.2+2.17*math.sin(t);line((x,-.7,zz),(x,6.8,zz),.018,'V5 lama longitudinal','13_COSTILLAS')
 for y in [-.67,6.77]:
  arch=[P(-4.8,y,0),P(-4.8,y,2.2)]+[P(-4.8*math.cos(j*math.pi/32),y,2.2+2.1*math.sin(j*math.pi/32)) for j in range(33)]+[P(4.8,y,0),P(-4.8,y,0)]
  for b in G.Brep.CreatePlanarBreps(G.PolylineCurve(arch),.001):emit(b,'V5 testero acristalado','14_VIDRIOS','VIDRIO',.88)
 for x in [-4.8,-2.4,0,2.4,4.8]:
  h=2.2+2.1*math.sqrt(max(0,1-(x/4.8)**2));line((x,6.78,0),(x,6.78,h),.035,'V5 montante norte','15_CARPINTERIAS')
 def privacywall(a,b,y,t,tag,zbase=0):
  def hh(x):return 2.2+2.1*math.sqrt(max(0,1-(x/4.8)**2))-.03
  top=[P(b-(b-a)*j/16,y,hh(b-(b-a)*j/16)) for j in range(17)]
  seg=[G.LineCurve(P(a,y,zbase),P(b,y,zbase)),G.LineCurve(P(b,y,zbase),top[0]),G.Curve.CreateInterpolatedCurve(top,3),G.LineCurve(top[-1],P(a,y,zbase))]
  cc=G.Curve.JoinCurves(seg,.001)[0]
  for face in G.Brep.CreatePlanarBreps(cc,.001) or []:emit(face.Faces[0].CreateExtrusion(G.LineCurve(P.Origin,P(0,t,0)),True),tag,'11_ENVOLVENTE_OPACA','LINO')
 for i in range(4):
  x=-4.8+i*2.4;tag='V5 H%d'%(i+1)
  if i>0:
   h=2.2+2.1*math.sqrt(max(0,1-(x/4.8)**2))-.03;box(x-.045,2.9,0,.09,3.9,h,tag+' separacion hasta cubierta','11_ENVOLVENTE_OPACA','LINO')
  privacywall(x,x+.20,2.9,.09,tag+' umbral cerrado');privacywall(x+1.2,x+2.4,2.9,.09,tag+' umbral lateral');privacywall(x+.2,x+1.2,2.9,.09,tag+' sobrepuerta',2.17)
  box(x+1.22,2.99,0,1.0,.035,2.14,tag+' puerta corredera recogida','15_CARPINTERIAS','MADERA');line((x+.18,2.94,2.2),(x+2.3,2.94,2.2),.018,tag+' guia corredera','15_CARPINTERIAS','ACERO')
  box(x+.12,3.6,.10,1.10,2,.25,tag+' cama');extrude_curve(roundcurve(x+.12,3.6,1.10,2,.07,.35),.2,tag+' colchon','20_MOBILIARIO','BLANCO');ball(x+.66,5.25,.62,.19,tag+' almohada','20_MOBILIARIO','BLANCO',(2,1,.3))
  table(x+.14,6.05,0,1.10,.55,tag+' estudio junto a luz norte');chair(x+.7,5.45,0,180)
  box(x+1.83,4.0,0,.48,1.1,2.15,tag+' armario');line((x+1.80,4.15,1),(x+1.80,4.15,1.18),.008,tag+' tirador armario','21_ACCESORIOS')
  for j in range(3):book(x+.24+j*.09,6.1,.79)
  box(x+.13,6.62,.2,.15,.03,.12,tag+' enchufe','22_INSTALACIONES','BLANCO');inst(LAMP,xf(x+1.4,5.65,0),tag+' lectura','23_ILUMINACION')
  box(x+.05,6.69,.05,.13,.025,2.1,tag+' contraventana apilada','15_CARPINTERIAS','MADERA')
 for x in [-4.8,4.71]:box(x,-.7,0,.09,2.4,2.15,'V5 lateral aseo','16_BANOS','BLANCO')
 for x in [-2.45,2.36]:box(x,-.7,0,.09,2.4,2.35,'V5 separacion aseo-casa comun','16_BANOS','BLANCO')
 for x in [-4.71,2.45]:
  box(x,1.64,0,.3,.08,2.35,'V5 bano umbral','16_BANOS','BLANCO');box(x+1.3,1.64,0,.96,.08,2.35,'V5 bano umbral','16_BANOS','BLANCO');box(x+.3,1.64,2.16,1.0,.08,.19,'V5 bano dintel','15_CARPINTERIAS','MADERA');box(x+1.33,1.73,0,.93,.035,2.14,'V5 bano hoja recogida','15_CARPINTERIAS','MADERA')
  box(x+.1,-.56,.015,.90,.9,.03,'V5 ducha','16_BANOS','GRIS');line((x+.4,-.54,.8),(x+.4,-.54,2.0),.012,'V5 columna ducha','22_INSTALACIONES','ACERO');ball(x+1.65,-.05,.30,.24,'V5 taza WC','16_BANOS','BLANCO',(.85,1.25,1));box(x+1.4,-.47,0,.45,.13,.75,'V5 cisterna','16_BANOS','BLANCO');box(x+.1,.85,.8,.5,.4,.06,'V5 lavabo','16_BANOS','BLANCO')
 for i in range(5):box(-2.2+i*.72,-.57,0,.7,.62,.86,'V5 cocina frente sur oscuro')
 box(-2.22,-.60,.86,3.64,.68,.045,'V5 encimera','20_MOBILIARIO','BLANCO');box(-2,-.5,.91,.6,.45,.008,'V5 fregadero','21_ACCESORIOS','ACERO');path([(-1.7,-.1,.92),(-1.7,-.1,1.2),(-1.7,-.35,1.2)],.012,'V5 grifo cocina','22_INSTALACIONES','ACERO')
 for x in [.4,.8]:emit(G.Cylinder(G.Circle(P(x,-.25,.92),.13),.008).ToBrep(True,True),'V5 induccion','21_ACCESORIOS','NEGRO')
 table(-.7,.65,0,1.4,.75,'V5 mesa cuatro');chair(-1.1,1.0,0,-90);chair(1.15,1.0,0,90);chair(-.3,1.52,0,0);chair(.7,1.52,0,0)
 for y in [1.0,2.3,5.4]:line((0,y,4.0),(0,y,2.65),.005,'V5 cable luz','23_ILUMINACION','ACERO');ball(0,y,2.52,.12,'V5 luz comun','23_ILUMINACION','LUZ')
 line((-4.5,-.1,-.28),(4.5,-.1,-.28),.055,'V5 colector humedo sur DN110','22_INSTALACIONES','MAGENTA')
 for x in [-4.8,4.8]:box(x,1.74,0,.025,1.12,2.16,'V5 acceso lateral a galeria1.20','14_VIDRIOS','VIDRIO');line((x,1.7,2.2),(x,2.9,2.2),.02,'V5 guia acceso','15_CARPINTERIAS','ACERO')
 PAV_DATA=CAP;PAV=finish('PABELLON_4_REFUGIOS','V5 cuatro refugios al norte; franja sur humeda y galeria de 1.20m')
 status('ESTRUCTURA: reproducir exactamente los ejes y secciones calculados')
 def chs(a,b,dia,t,name,la='02_ESTRUCTURA_RAMAS',col='MARFIL'):
  a=point(a);b=point(b);v=b-a;cy=G.Cylinder(G.Circle(G.Plane(a,v),dia/2),v.Length);e=G.Extrusion.CreatePipeExtrusion(cy,dia/2-t,True,True)
  if e:emit(e.ToBrep(),name,la,col)
 def curved_chs(pts,group,name):
  cr=G.Curve.CreateInterpolatedCurve([point(p) for p in pts],3);outer=[];inner=[]
  for j,p in enumerate(pts):
   ee=group[max(0,min(len(group)-1,j))];rr=ee['D']/2;tt=ee['t'];ok,tpar=cr.ClosestPoint(point(p));pl=G.Plane(point(p),cr.TangentAt(tpar));outer.append(G.Circle(pl,rr).ToNurbsCurve());inner.append(G.Circle(pl,rr-tt).ToNurbsCurve())
  ob=G.Brep.CreateFromLoft(outer,P.Unset,P.Unset,G.LoftType.Normal,False)[0];ib=G.Brep.CreateFromLoft(inner,P.Unset,P.Unset,G.LoftType.Normal,False)[0];ib.Flip();pieces=[ob,ib]
  for j in [0,-1]:pieces.extend(G.Brep.CreatePlanarBreps([outer[j],inner[j]],.001))
  joined=G.Brep.JoinBreps(pieces,.003)
  for b in joined or []:emit(b,name,'02_ESTRUCTURA_RAMAS','MARFIL')

 # Primary members use the same nodal geometry, diameter and wall thickness as the FE model.
 nn=S['nodes'];els=S['elements'];i=0
 while i<len(els):
  el=els[i];kind=el['kind'];group=els[i:i+4]
  if kind in ['TRONCO','RAMA'] and len(group)==4 and all(e['kind']==kind for e in group) and all(group[j]['j']==group[j+1]['i'] for j in range(3)):
   pts=[nn[group[0]['i']]]+[nn[e['j']] for e in group]
   # A smooth pipe interpolates the converged four-segment analysis axis.
   curved_chs(pts,group,kind+' CHS hueco D%.1f t%.1f mm'%(el['D']*1000,el['t']*1000))
   i+=4
  else:
   chs(nn[el['i']],nn[el['j']],el['D'],el['t'],kind+' D%.1f t%.1f mm'%(el['D']*1000,el['t']*1000),'02_ESTRUCTURA_RAMAS' if 'ARRIO' not in kind else '26_ARRIOSTRAMIENTO','MARFIL' if 'ARRIO' not in kind else 'ACERO');i+=1
 # Full wall thickness shown on a real hollow CHS detail, not only assigned as metadata.
 def hollow(a,b,D,t,name):
  a=point(a);b=point(b);v=b-a;cyl=G.Cylinder(G.Circle(G.Plane(a,v),D/2),v.Length);e=G.Extrusion.CreatePipeExtrusion(cyl,D/2-t,True,True)
  if e:emit(e.ToBrep(),name,'27_DETALLES_TECNICOS','MARFIL')
 for r in S['reactions']:
  x,y,z=r['position'];box(x-1.15,y-1.15,-.85,2.3,2.3,.80,'Encepado a verificar con geotecnia','28_CIMENTACION','GRIS');box(x-.85,y-.85,0,1.7,1.7,.08,'Placa base 80 mm','04_UNIONES','ACERO')
  for j in range(16):
   th=2*math.pi*j/16;xx=x+.70*math.cos(th);yy=y+.70*math.sin(th);line((xx,yy,-.7),(xx,yy,.15),.024,'Anclaje M48','04_UNIONES','ACERO');bolt(xx,yy,.14)
 # Modelled node flanges at branch origins with sixteen bolt shanks/nuts.
 origins=[]
 for el in els:
  if el['kind']=='RAMA' and el['i'] not in origins:origins.append(el['i'])
 # Only genuine branch starts share at least three outgoing rays; internal FE mesh nodes do not get fake connections.
 branchstarts={e['i']:sum(t['i']==e['i'] and t['kind']=='RAMA' for t in els) for e in els if e['kind']=='RAMA'}
 for idx,nbranches in branchstarts.items():
  if nbranches<3:continue
  x,y,z=nn[idx];line((x,y,z-.04),(x,y,z+.04),.65,'Nudo tronco-ramas casquillo','04_UNIONES','MARFIL')
  for j in range(16):
   th=j*math.pi/8;bolt(x+.57*math.cos(th),y+.57*math.sin(th),z+.045)
 status('BANDEJAS: diez cotas entrelazadas en tres arboles de convivencia')
 PEOPLE=R.FileIO.File3dm.Read(os.path.join(ROOT,'fuentes','personas_seleccionadas.3dm'));POSE={}
 for ob in PEOPLE.Objects:
  begin();emit(ob.Geometry.Duplicate(),'Figura procedente de PERSONAS.3dm','40_PERSONAS','NEGRO');POSE[int(ob.Attributes.Name.split('_')[1])]=finish(ob.Attributes.Name,'Figura original suministrada; escala conservada')
 def person(pose,x,y,z,angle=0,act='Habitar'):
  inst(POSE[pose],xf(x,y,z,angle),'Persona '+act,'40_PERSONAS','NEGRO');META['people'].append({'pose':pose,'position':[x,y,z],'activity':act})
 for p in S['plates']:
  cx,f,z=p['cx'],p['front'],p['z'];outline=p['outline'];poly=[{'outer':outline,'holes':[]}]
  prism(poly,z,-.20,p['id']+' bandeja curvilinea','01_BANDEJAS','MADERA');inst(PAV,xf(cx,f,z),p['id']+' gran pabellon','10_UNIDADES')
  truss(outline,lambda x,y:z,p['id'])
  for dx in [-3.45,-2.30,-1.15,1.15,2.30,3.45]:
   xx=cx+dx;outer=G.PolylineCurve([P(xx-.08,f-.25,z-.57),P(xx+.08,f-.25,z-.57),P(xx+.08,f-.25,z-.21),P(xx-.08,f-.25,z-.21),P(xx-.08,f-.25,z-.57)]);inner=G.PolylineCurve([P(xx-.07,f-.25,z-.56),P(xx+.07,f-.25,z-.56),P(xx+.07,f-.25,z-.22),P(xx-.07,f-.25,z-.22),P(xx-.07,f-.25,z-.56)])
   face=G.Brep.CreatePlanarBreps([outer,inner],.001)[0];joist=face.Faces[0].CreateExtrusion(G.LineCurve(P.Origin,P(0,7.15,0)),True);emit(joist,'Vigueta RHS360x160x10 paso1.15m','32_VIGUETAS','AMARILLO')
  # Clear access from the central terrace and side lift; no guard is placed across a connection.
  def gate(q):return (abs(q[0]-(cx+5.3))<1.5 and q[1]<f+1.3) or (abs(q[0]-(cx-5.3))<1.5 and q[1]<f+1.3)
  railing(outline,lambda x,y:z,p['id'],gate)
  # V5: la galeria frontal queda libre; sin mesas en el paso de 1.40m.
  for x,y in [(cx-4.7,f-.5),(cx+4.8,f+5.9)]:plant(x,y,z,True)
  person(25,cx-3.0,f+4.7,z,90,'habitacion norte');person(30,cx+.9,f+2.2,z,200,'galeria domestica');person(19,cx+1.4,f-.9,z,30,'terraza')
  # Partial anticlastic canopies above each pavilion, tied to deck outriggers.
  zc=z+4.6;corners=[(cx-5.25,f-.8,zc+.7),(cx+5.25,f-.8,zc-.15),(cx+5.25,f+7.0,zc+.65),(cx-5.25,f+7,zc-.12)]
  pts=[]
  for a in range(7):
   u=a/6.
   for b in range(7):
    v=b/6.;ww=[(1-u)*(1-v),u*(1-v),u*v,(1-u)*v];q=[sum(ww[k]*corners[k][d] for k in range(4)) for d in range(3)];q[2]-=.23*math.sin(math.pi*u)*math.sin(math.pi*v);pts.append(q)
  layer('06_VELAS_ESTADO_VERANO','VERDE',False)
  surf(pts,7,7,p['id']+' vela desplegada solo estado verano','06_VELAS_ESTADO_VERANO','VERDE',.42)
  fold=[]
  for ia in range(15):
   yy=f-.8+7.8*ia/14.;fold.extend([(cx-5.2,yy,zc+.2+.10*math.sin(ia*math.pi)),(cx-4.85,yy,zc+.2-.10*math.sin(ia*math.pi))])
  surf(fold,15,2,p['id']+' vela recogida invierno','06_VELAS_RECOGIDAS','VERDE')
  for j,(x,y,zz) in enumerate(corners):
   line((x,y,z),(x,y,zz),.045,'Mastil vela','06_VELAS');clamp((x,y,zz),(cx+(-4.5 if x<cx else 4.5),f+.2 if y<f else f+6.4,z+.1));baseplate(x,y,z,.30)
  # The two low corners collect rainwater; each has an overflow independent of the primary drain.
  for x,y,zz in [corners[1],corners[3]]:
   line((x,y,z+.1),(x,y,zz),.05,'Bajante lluvia DN100','22_INSTALACIONES','CIAN');line((x,y,zz-.06),(x+.25,y,zz-.06),.025,'Rebosadero DN50','22_INSTALACIONES','CIAN')
  # Actual thermal build-up detail at the centre-front sill, legible in the detail file.
  META['units'].append({'id':p['id'],'people':4,'z':z,'body_m2':72.0,'plate_m2':p['area']})
 # Yellow stairs braid across the three bays instead of making five flat floors.
 status('CONEXIONES: escaleras diagonales y acceso independiente por ascensores')
 bybay=[[p for p in S['plates'] if p['bay']==b] for b in range(3)]
 links=[]
 for b in [0,1]:
  for a in bybay[b]:
   candidates=[q for q in bybay[b+1] if 1.5<abs(q['z']-a['z'])<3.5]
   if not candidates:continue
   q=min(candidates,key=lambda q:abs(q['z']-a['z']))
   if any({l['a'],l['b']}=={a['id'],q['id']} for l in links):continue
   start=[a['cx']+2.4,a['front']-1.5,a['z']];end=[q['cx']-2.4,q['front']-1.3,q['z']]
   if end[2]<start[2]:start,end=end,start
   dx=end[0]-start[0];dy=end[1]-start[1];L=math.hypot(dx,dy);n=int(math.ceil((end[2]-start[2])/.175));rise=(end[2]-start[2])/n;direction=V(dx/L,dy/L,0);side=V(-dy/L,dx/L,0);landing=1.2;run=L-2*landing;tread=run/(n-1)
   if tread<.28: # Extend endpoints within terraces to obtain real treads.
    extra=(.28*(n-1)-run)/2;start[0]-=direction.X*extra;start[1]-=direction.Y*extra;end[0]+=direction.X*extra;end[1]+=direction.Y*extra;L+=2*extra;run=L-2*landing;tread=run/(n-1)
   def rectangle_center(pt,w,d,z,name):
    xx,yy=pt;aa=P(xx,yy,z);b=G.Box(G.Plane(aa,direction,side),G.Interval(-d/2,d/2),G.Interval(-w/2,w/2),G.Interval(-.12,0)).ToBrep();emit(b,name,'09_ESCALERAS','AMARILLO')
   rectangle_center((start[0]+direction.X*.6,start[1]+direction.Y*.6),1.3,1.2,start[2],'Descansillo enlace')
   rectangle_center((end[0]-direction.X*.6,end[1]-direction.Y*.6),1.3,1.2,end[2],'Descansillo enlace')
   for j in range(n):
    dist=landing+j*tread;xx=start[0]+direction.X*dist;yy=start[1]+direction.Y*dist;zz=start[2]+(j+1)*rise;rectangle_center((xx,yy),1.3,max(.28,tread),zz,'Enlace huella %.0f contrahuella %.0f mm'%(tread*1000,rise*1000))
   for sg in [-1,1]:
    aa=P(start[0],start[1],start[2])+side*(sg*.67);bb=P(end[0],end[1],end[2])+side*(sg*.67);line(aa,bb,.08,'Zanca puente escalera','09_ESCALERAS');line(aa+V(0,0,1.1),bb+V(0,0,1.1),.024,'Pasamanos puente','08_BARANDILLAS','AMARILLO')
    for j in range(n+1):
     t=j/float(n);q0=aa+(bb-aa)*t;line(q0,q0+V(0,0,1.1),.008,'Barrote puente','08_BARANDILLAS','AMARILLO')
   links.append({'a':a['id'],'b':q['id'],'risers':n,'rise':rise,'tread':tread,'width':1.3})
 # Three small glazed lifts belong to the three staggered inhabited trees.
 def lift(ex,ey,stops,tag):
  w,d=2.3,2.15;cz=stops[0];top=max(stops)+3.7
  box(ex-.1,ey-.1,-1.2,w+.2,d+.2,.2,tag+' foso','18_ASCENSOR','GRIS')
  for x in [ex,ex+w]:
   for y in [ey,ey+d]:box(x-.04,y-.04,-1,.08,.08,top+1.1,tag+' montante','18_ASCENSOR','MAGENTA')
  for z in [0]+stops+[top]:
   for a,b in [((ex,ey,z),(ex+w,ey,z)),((ex+w,ey,z),(ex+w,ey+d,z)),((ex,ey+d,z),(ex+w,ey+d,z))]:line(a,b,.035,tag+' travesano','18_ASCENSOR','MAGENTA')
  box(ex+w,ey,-1,.015,d,top+1,tag+' vidrio fondo','19_ASCENSOR_VIDRIO','VIDRIO');box(ex,ey,-1,w,.015,top+1,tag+' vidrio lateral','19_ASCENSOR_VIDRIO','VIDRIO');box(ex,ey+d,-1,w,.015,top+1,tag+' vidrio lateral','19_ASCENSOR_VIDRIO','VIDRIO')
  for y in [ey+.17,ey+d-.17]:box(ex+.3,y,-1,.07,.07,top+.8,tag+' guia','18_ASCENSOR','ACERO')
  # Door faces west. Clear cabin depth 1.60 along x, width 1.40 along y.
  cx,cy=ex+.34,ey+.38;box(cx-.06,cy-.06,cz-.14,1.72,1.52,.14,tag+' cabina suelo','18_ASCENSOR','GRIS');box(cx-.06,cy-.06,cz+2.25,1.72,1.52,.08,tag+' cabina techo','18_ASCENSOR','MARFIL')
  box(cx+1.6,cy,cz,.03,1.4,2.25,tag+' cabina fondo','19_ASCENSOR_VIDRIO','VIDRIO');box(cx,cy,cz,1.6,.03,2.25,tag+' cabina lado','19_ASCENSOR_VIDRIO','VIDRIO');box(cx,cy+1.4,cz,1.6,.03,2.25,tag+' cabina lado','19_ASCENSOR_VIDRIO','VIDRIO')
  line((cx+.2,cy+.1,cz+.9),(cx+1.4,cy+.1,cz+.9),.018,tag+' pasamanos','18_ASCENSOR','ACERO');box(cx+1.54,cy+.3,cz+.8,.035,.22,.45,tag+' botonera','18_ASCENSOR','ACERO')
  for j in range(6):ball(cx+1.50,cy+.35+(j%2)*.1,cz+.88+(j//2)*.09,.016,tag+' boton','18_ASCENSOR','LUZ')
  for z in [0]+stops:
   box(ex-.03,ey,z,.10,.55,2.3,tag+' jamba','18_ASCENSOR','MAGENTA');box(ex-.03,ey+1.52,z,.10,.63,2.3,tag+' jamba','18_ASCENSOR','MAGENTA');box(ex-.03,ey+.55,z+2.15,.10,.97,.15,tag+' dintel','18_ASCENSOR','MAGENTA')
   if abs(z-cz)>.01:
    for y in [ey+.58,ey+1.03]:box(ex-.025,y,z,.025,.448,2.14,tag+' hoja automatica','18_ASCENSOR','ACERO')
   else:
    box(ex-.025,ey+.13,z,.025,.44,2.14,tag+' hoja abierta','18_ASCENSOR','ACERO');box(ex-.025,ey+1.48,z,.025,.44,2.14,tag+' hoja abierta','18_ASCENSOR','ACERO')
   box(ex-2.0,ey-.17,z-.17,2.0,1.65,.17,tag+' rellano giro','07_GALERIAS','MADERA');box(ex-.08,ey+.58,z-.02,.12,.9,.02,tag+' umbral enrasado','18_ASCENSOR','ACERO');box(ex-.1,ey+.28,z+.92,.04,.12,.24,tag+' llamada','18_ASCENSOR','ACERO')
  box(ex+1.8,ey+.25,6,.16,1.2,2.0,tag+' contrapeso','18_ASCENSOR','ACERO');line((ex+1.2,ey+.3,top-.6),(ex+1.2,ey+1.6,top-.6),.16,tag+' traccion','18_ASCENSOR','ACERO')
  for y in [ey+.6,ey+.75,ey+.9]:line((cx+1.35,y,cz+2.33),(cx+1.35,y,top-.6),.006,tag+' cable','18_ASCENSOR','ACERO')
  person(34,cx+.8,cy+.7,cz,90,'ascensor')
 for b,bb in enumerate(S['bays']):lift(bb['x']+5.9,bb['front']-1.63,bb['levels'],'ASC%d'%(b+1))
 status('PLANTA BAJA V5: tres casas comunes diferenciadas y umbral protegido')
 for b,bb in enumerate(S['bays']):
  cx=bb['x'];f=bb['front'];tag='PB_'+['A_CANTINA','B_REPARAR_LAVAR','C_ESTUDIAR_CUIDAR'][b];zz=.005
  box(cx-4.3,f,-.15,8.6,5.8,.155,tag+' suelo enrasado','24_COMUNES','MADERA')
  for y in [f,f+5.8]:
   if y==f:
    box(cx-4.3,y,zz,3.6,.04,2.7,tag+' vidrio fijo','14_VIDRIOS','VIDRIO');box(cx+.7,y,zz,3.6,.04,2.7,tag+' vidrio fijo','14_VIDRIOS','VIDRIO');box(cx+.72,y-.04,zz,1.3,.025,2.25,tag+' puerta recogida1.20','14_VIDRIOS','VIDRIO')
   else:box(cx-4.3,y,zz,8.6,.04,2.7,tag+' vidrio posterior','14_VIDRIOS','VIDRIO')
  for x in [cx-4.3,cx+4.18]:box(x,f,zz,.12,5.8,2.7,tag+' lateral','24_COMUNES','CORCHO')
  box(cx-4.3,f,2.705,8.6,5.8,.15,tag+' cubierta','12_CUBIERTAS','VERDE')
  if b in [0,2]:
   wx=cx+1.78;wy=f+3.28
   box(wx,wy,zz,.10,2.52,2.5,tag+' aseo2.40x2.40 separacion','24_COMUNES','BLANCO');box(wx,wy,zz,.3,.10,2.5,tag+' aseo umbral','24_COMUNES','BLANCO');box(wx+1.3,wy,zz,1.22,.10,2.5,tag+' aseo umbral','24_COMUNES','BLANCO');box(wx+1.35,wy+.12,zz,.95,.035,2.15,tag+' aseo corredera','15_CARPINTERIAS','MADERA')
   box(wx,wy+2.40,zz,2.52,.10,2.5,tag+' fondo opaco aseo','24_COMUNES','BLANCO');line((cx+4.02,f+4.8,.75),(cx+4.02,f+5.5,.75),.018,tag+' apoyo sanitario','21_ACCESORIOS','ACERO');ball(cx+3.65,f+5.12,.31,.24,tag+' WC','16_BANOS','BLANCO',(.9,1.25,1));box(cx+3.42,f+5.55,zz,.46,.14,.75,tag+' cisterna','16_BANOS','BLANCO');box(cx+1.98,f+3.55,.8,.45,.5,.06,tag+' lavabo libre inferior','16_BANOS','BLANCO');path([(cx+2.1,f+3.8,.86),(cx+2.1,f+3.8,1.05),(cx+2.25,f+3.8,1.05)],.012,tag+' grifo','22_INSTALACIONES','ACERO')
  if b==0:
   for i in range(5):box(cx-4+i*.72,f+5.0,zz,.70,.65,.86,tag+' cocina cooperativa')
   box(cx-4.05,f+4.97,.87,3.7,.72,.045,tag+' encimera','20_MOBILIARIO','BLANCO');box(cx-3.8,f+5.1,.92,.65,.45,.02,tag+' fregadero','21_ACCESORIOS','ACERO')
   for xx in [cx-3.7,cx-1.15,cx+1.4]:
    table(xx,f+.85,zz,1.4,.75,tag+' mesa cuatro')
    for xx2 in [xx+.3,xx+1.0]:chair(xx2,f+.43,zz,0);chair(xx2,f+2.1,zz,180)
   box(cx-.1,f+4.65,zz,1.0,.7,1.85,tag+' despensa-frio','20_MOBILIARIO','BLANCO')
  elif b==1:
   box(cx-4.0,f+.6,.85,.70,3.7,.07,tag+' banco herramientas');table(cx-2.4,f+1.2,zz,2.0,1.0,tag+' reparacion')
   for xx in [cx+1.2,cx+2.0,cx+2.8]:box(xx,f+4.6,zz,.7,.7,.9,tag+' lavadora','24_COMUNES','BLANCO');ball(xx+.35,f+4.57,.5,.23,tag+' tambor','24_COMUNES','ACERO',(1,.15,1))
   box(cx+.7,f+4.2,zz,3.45,.09,2.4,tag+' cierre acustico lavanderia','24_COMUNES','LINO')
   for xx in [cx-3.8,cx-2.9,cx-2.0]:line((xx,f+4.6,.1),(xx,f+5.5,.6),.025,tag+' soporte bicicletas','21_ACCESORIOS','ACERO')
   for h in [.5,1.2,1.9]:box(cx+2.8,f+.5,h,.8,2.6,.04,tag+' herramienta y limpieza')
  else:
   ox=cx-4.1;oy=f+3.0
   box(ox+3.6,oy,zz,.10,2.7,2.5,tag+' cuidados pared privacidad','24_COMUNES','LINO');box(ox,oy,zz,2.4,.10,2.5,tag+' cuidados frente','24_COMUNES','LINO');box(ox+2.55,oy+.1,zz,.95,.035,2.15,tag+' cuidados corredera','15_CARPINTERIAS','MADERA');table(ox+.3,oy+1.5,zz,1.3,.65,tag+' atencion discreta');chair(ox+.8,oy+.9,zz,0)
   for xx in [cx-3.8,cx-.9,cx+1.9]:
    table(xx,f+.55,zz,1.6,.65,tag+' estudio dos puestos');chair(xx+.4,f+1.6,zz,180);chair(xx+1.2,f+1.6,zz,180)
   for h in [.4,1.0,1.6,2.2]:box(cx-.1,f+4.8,h,1.4,.4,.04,tag+' biblioteca')
  for xx in [cx-3.9,cx+3.8]:plant(xx,f+2.65,zz)
  person(42,cx-1.3,f+2.5,zz,30,'PB residente '+tag);person(45,cx+.6,f+2.2,zz,160,'PB residente '+tag);person(19,cx-2.8,f+.3,zz,60,'PB visitante '+tag);person(30,cx+2.7,f+2.5,zz,90,'PB visitante '+tag)
  for xx in [cx-2,cx+2]:plant(xx,f-1.4,0)
 # Residential threshold remains free of a shop; small welcome table beyond the clear path.
 box(17.5,-4.7,0,1.1,.5,.8,'PB acogida tras umbral residencial','24_COMUNES','MADERA');box(17.5,-4.7,1.0,1.1,.04,1.0,'PB tablon tareas y horarios','24_COMUNES','CORCHO')
 # Two independent end stairs, outside the domestic pavilions, keep all flights clear.
 def core(x,y,levels,tag):
  levels=[0]+levels
  for z in levels:
   box(x,y,z-.16,2.8,1.3,.16,tag+' rellano','09_ESCALERAS','MADERA')
   box(x,y+6.0,z-.16,2.8,1.3,.16,tag+' rellano opuesto','09_ESCALERAS','MADERA')
  for z0,z1 in zip(levels,levels[1:]):
   total=int(math.ceil((z1-z0)/.175));total+=total%2;nh=total//2;rise=(z1-z0)/total;run=(nh-1)*.28
   for j in range(nh):
    box(x+.08,y+1.3+j*.28,z0+(j+1)*rise-.1,1.2,.29,.10,tag+' tramo A','09_ESCALERAS','AMARILLO')
    box(x+1.50,y+1.3+(nh-1-j)*.28,z0+(nh+j+1)*rise-.1,1.2,.29,.10,tag+' tramo B','09_ESCALERAS','AMARILLO')
   box(x+.08,y+1.3+run+.28,z0+nh*rise-.15,2.62,1.3,.15,tag+' meseta intermedia','09_ESCALERAS','MADERA')
   for xx in [x+.1,x+1.25]:
    line((xx,y+1.3,z0+.1),(xx,y+1.3+run,z0+nh*rise),.06,tag+' zanca A','09_ESCALERAS');line((xx,y+1.3,z0+1.1),(xx,y+1.3+run,z0+nh*rise+1.1),.024,tag+' pasamanos A','08_BARANDILLAS','AMARILLO')
   for xx in [x+.1,x+1.25]:
    for j in range(nh):
     yy=y+1.3+j*.28;zz=z0+(j+1)*rise;line((xx,yy,zz),(xx,yy,zz+1.1),.01,tag+' montante barandillaA','08_BARANDILLAS','AMARILLO')
   for xx in [x+1.53,x+2.66]:
    for j in range(nh):
     yy=y+1.3+(nh-1-j)*.28;zz=z0+(nh+j+1)*rise;line((xx,yy,zz),(xx,yy,zz+1.1),.01,tag+' montante barandillaB','08_BARANDILLAS','AMARILLO')
    line((xx,y+1.3+run,z0+nh*rise),(xx,y+1.3,z1),.06,tag+' zanca B','09_ESCALERAS');line((xx,y+1.3+run,z0+nh*rise+1.1),(xx,y+1.3,z1+1.1),.024,tag+' pasamanos B','08_BARANDILLAS','AMARILLO')
  top=levels[-1]+3.2
  for xx in [x,x+2.8]:
   door_side=(tag=='ESC_ESTE' and xx==x) or (tag=='ESC_OESTE' and xx==x+2.8)
   if not door_side:box(xx,y,0,.10,7.3,top,tag+' lateral fijo','17_NUCLEOS','VIDRIO')
   else:
    yy=y+(2.7 if tag=='ESC_ESTE' else .6)
    box(xx,y,0,.10,yy-y,top,tag+' lateral tramo1','17_NUCLEOS','VIDRIO');box(xx,yy+1.05,0,.10,y+7.3-yy-1.05,top,tag+' lateral tramo2','17_NUCLEOS','VIDRIO')
    for z,zz in zip(levels,levels[1:]+[top]):
     if zz>z+2.2:box(xx,yy,z+2.2,.10,1.05,zz-z-2.2,tag+' dintel lateral','17_NUCLEOS','VIDRIO')
     box(xx-.015,yy+.02,z,.035,1.0,2.17,tag+' puerta lateral operable','15_CARPINTERIAS','VERDE')
  for z in levels:
   if tag=='ESC_ESTE':
    box(x-.04,y+2.7,z,.035,1.05,2.17,'ESC_ESTE puerta lateral oeste','15_CARPINTERIAS','VERDE');box(x-1.5,y+2.6,z-.17,1.5,1.4,.17,'ESC_ESTE rellano oeste','07_GALERIAS','MADERA')
   box(x,y-.05,z,.1,.08,3.0,tag+' jamba','17_NUCLEOS','MARFIL');box(x+1.25,y-.05,z,1.55,.08,3.0,tag+' frente','17_NUCLEOS','MARFIL');box(x+.15,y-.05,z+2.2,1.1,.08,.8,tag+' dintel','17_NUCLEOS','MARFIL');box(x+.17,y-.015,z,1.04,.035,2.17,tag+(' puerta salida suelo' if z==0 else ' panel fijo superior'),'15_CARPINTERIAS','VERDE');line((x+.3,y-.06,z+1),(x+1.1,y-.06,z+1),.015,tag+' barra salida','21_ACCESORIOS','ACERO')
 core(13.9,-6.3,S['bays'][0]['levels'],'ESC_OESTE')
 core(57.0,-5.8,[3.13,6.26]+S['bays'][2]['levels'],'ESC_ESTE')
 # Landings connect each end stair to its nearest platform without entering a sleeping room.
 for p in S['plates']:
  if p['bay'] not in [0,2]:continue
  z=p['z'];cx=p['cx'];f=p['front']
  if p['bay']==0:
   box(16.7,-6.25,z-.17,1.4,3.0,.17,'Salida oeste galeria','07_GALERIAS','MADERA');box(16.9,-3.25,z-.17,1.3,f+2.9+3.25,.17,'Ramal oeste junto a unidad','07_GALERIAS','MADERA');box(17.5,f+1.75,z-.17,max(.3,cx-4.8-17.5),1.3,.17,'Entrada lateral oeste','07_GALERIAS','MADERA')
  else:box(54.0,-2.95,z-.17,3.0,1.30,.17,'Enlace salida este detras ascensor','07_GALERIAS','MADERA')
 # Ground plane and exact parcel edge, not an invented second street.
 prism(json.load(open(os.path.join(ROOT,'fuentes','recorrido_suelo.json'))),.005,.025,'Recorrido suelo hasta frente oeste','25_URBANIZACION','MADERA')
 q=json.load(open(os.path.join(ROOT,'fuentes','parcela_local.geojson')))
 prism([{'outer':q['geometry']['coordinates'][0],'holes':[]}],-.35,.35,'Parcela real','00_PARCELA','GRIS');box(12.8,-1,0,6,2,.03,'Acceso desde calle','00_PARCELA','MADERA');person(19,15,-.1,.03,30,'entrada')
 # Registered risers remain outside the elevator shafts and sleeping volumes.
 for b,bb in enumerate(S['bays']):
  x=bb['x']-2.6;y=bb['front']-1.65;top=max(bb['levels'])+5.5
  line((x,y,-.7),(x,y,top),.10,'LLUVIA montante DN200','22_INSTALACIONES','CIAN')
  line((x+.32,y,-.7),(x+.32,y,top+.3),.055,'SANITARIO montante DN110 ventilado','22_INSTALACIONES','MAGENTA')
  box(x+.52,y-.05,0,.12,.10,top,'Bandeja electrica registrable separada','22_INSTALACIONES','ACERO')
  for z in range(1,int(top),2):
   line((x-.14,y,z),(x+.55,y,z),.015,'Mensula servicios','04_UNIONES','ACERO')
  for p in [q for q in S['plates'] if q['bay']==b]:
   cx,f,z=p['cx'],p['front'],p['z']
   for xx,yy in [(cx+5.25,f-.8),(cx-5.25,f+7.)]:
    path([(xx,yy,z+.1),(xx,yy,z-.55),(xx+(x-xx)*.5,yy+(y-yy)*.5,z-.62),(x,y,z-.70)],.05,'LLUVIA ramal DN100 con caida','22_INSTALACIONES','CIAN')
   path([(cx,f+6.6,z-.29),(cx,f+3.4,z-.5),(x+.32,y,z-.75)],.055,'SANITARIO ramal DN110 registrable','22_INSTALACIONES','MAGENTA')
 path([(46,-6.05,-.70),(41,-5.6,-.76),(33.4,-4.95,-.85),(27,-4.2,-.92),(20.8,-3.45,-1.0),(13.5,-.5,-1.10)],.125,'LLUVIA colector enterradoDN250 pendiente hacia calle','22_INSTALACIONES','CIAN')
 for bb in S['bays']:
  x=bb['x']-2.6;y=bb['front']-1.65;zz=-1.0+(x-20.8)*(.3/25.2);line((x,y,-.7),(x,y,zz),.10,'Union bajante-colector lluvia','22_INSTALACIONES','CIAN')
 # Three suspended rain buffers, 250 L each; 2.5 kN added explicitly to the FE loads.
 for p in [q for q in S['plates'] if q['id'] in ['P02','P05','P08']]:
  x=p['cx']+3.8;y=p['front']-1.0;z=p['z'];profiles=[]
  for dz,rr in [(-.55,.31),(-.75,.39),(-1.15,.39),(-1.65,.12),(-1.8,.03)]:profiles.append(G.Circle(P(x,y,z+dz),rr).ToNurbsCurve())
  tank=G.Brep.CreateFromLoft(profiles,P.Unset,P.Unset,G.LoftType.Normal,False)[0];tank=tank.CapPlanarHoles(.001) or tank;emit(tank,'Deposito pluvial250L carga2.5kN','31_AGUA','CIAN',.25)
  for j in range(3):
   a=j*2*math.pi/3;line((x+.42*math.cos(a),y+.42*math.sin(a),z-.25),(x+.32*math.cos(a),y+.32*math.sin(a),z-.75),.005,'Suspension deposito','05_CABLES','ACERO')
  line((x,y,z-.3),(x,y,z-.6),.025,'Entrada deposito DN50','22_INSTALACIONES','CIAN');line((x,y,z-1.8),(x,y,z-1.95),.015,'Valvula riego','22_INSTALACIONES','ACERO')
 # Detailed technical assembly, placed separately in its own file, not floating beside the building.
 status('DETALLES: seccion CHS, nudo atornillado y envolvente estratificada')
 layer('90_CONTEXTO','GRIS',True)
 context=json.load(open(os.path.join(ROOT,'fuentes','contexto_original.json')))['context']
 for ct in context:
  me=G.Mesh()
  for q in ct['vertices']:me.Vertices.Add(*q)
  for j in range(0,len(ct['vertices']),3):me.Faces.AddFace(j,j+1,j+2)
  me.Faces.CullDegenerateFaces();me.Normals.ComputeNormals();emit(me,'Vecino '+ct['id'],'90_CONTEXTO','GRIS')
 # Named views are framed on the new staggered form.
 for name,loc,tgt in [('01_MACARRA_AXONOMETRIA',(85,-100,64),(35,-1,12)),('02_FRENTE_ZIGZAG',(35,-100,16),(35,-1,12)),('03_ARBOL_Y_NUDOS',(8,-35,25),(24,0,11)),('04_ASCENSOR',(57,-18,15),(54,-3,10)),('05_PLANTA',(35,-1,100),(35,-1,0))]:
  vi=D.ViewInfo();vi.Name=name;vp=vi.Viewport;vp.SetCameraLocation(P(*loc));vp.SetCameraDirection(P(*tgt)-P(*loc));vp.SetCameraUp(V.YAxis if name=='05_PLANTA' else V.ZAxis);vp.TargetPoint=P(*tgt);vp.ChangeToParallelProjection(True);vp.Extents(1.5,G.BoundingBox(P(12,-8,-1),P(60,12,26)));F.AllNamedViews.Add(vi)
  if name=='01_MACARRA_AXONOMETRIA':
   vi.Name='Perspective';vi.Maximized=True;vi.DisplayModeId=R.Display.DisplayModeDescription.FindByName('Rendered').Id;F.AllViews.Add(vi)
 opts=R.FileIO.File3dmWriteOptions();opts.Version=8;opts.SaveRenderMeshes=True
 finalpath=os.path.join(ROOT,'modelos','SELVA_V5_LUZ_Y_PLANTA_BAJA.3dm')
 if not F.Write(finalpath,opts):raise Exception('No se pudo guardar el conjunto')
 # Exact render cache, generated recursively from the same Rhino Breps and supplied mesh figures.
 F=R.FileIO.File3dm.Read(finalpath)
 status('RENDER: exportar triangulacion exacta del Rhino, sin reinterpretacion de imagen')
 objmap={str(o.Attributes.ObjectId):o for o in F.Objects};idef={str(d.Id):d for d in F.AllInstanceDefinitions}
 batches={}
 def rendergeom(g,a,xfm):
  if isinstance(g,G.InstanceReferenceGeometry):
   dd=idef[str(g.ParentIdefId)]
   for oid in dd.GetObjectIds():
    ob=objmap[str(oid)];rendergeom(ob.Geometry,ob.Attributes,xfm*g.Xform)
   return
  meshes=[]
  if isinstance(g,G.Brep):
   for face in g.Faces:
    m=face.GetMesh(G.MeshType.Render)
    if m:meshes.append(m.DuplicateMesh())
   if not meshes:meshes=list(G.Mesh.CreateFromBrep(g,MP) or [])
  elif isinstance(g,G.Mesh):meshes=[g.DuplicateMesh()]
  if not meshes:return
  key=str(a.LayerIndex)+'_'+str(a.MaterialIndex)
  if key not in batches:
   mat=next(m for m in F.AllMaterials if m.Index==a.MaterialIndex);col=mat.DiffuseColor
   batches[key]={'vertices':[],'faces':[],'color':[col.R/255.,col.G/255.,col.B/255.],'alpha':mat.Transparency,'layer':next(l.Name for l in F.AllLayers if l.Index==a.LayerIndex)}
  b=batches[key]
  for m in meshes:
   m.Transform(xfm);off=len(b['vertices']);b['vertices'].extend([[float(v.X),float(v.Y),float(v.Z)] for v in m.Vertices])
   for face in m.Faces:b['faces'].append([off+face.A,off+face.B,off+face.C] if face.IsTriangle else [off+face.A,off+face.B,off+face.C,off+face.D])
 for ob in F.Objects:
  if not ob.Attributes.IsInstanceDefinitionObject:rendergeom(ob.Geometry,ob.Attributes,T.Identity)
 import clr
 clr.AddReference('Newtonsoft.Json')
 from Newtonsoft.Json import JsonConvert
 System.IO.File.WriteAllText(os.path.join(ROOT,'fuentes','geometria_render.json'),JsonConvert.SerializeObject(batches))
 with open(os.path.join(ROOT,'verificacion','construccion_nativa.json'),'w') as f:json.dump({'counts':COUNTS,'errors':ERRORS,'people':META['people'],'links':links,'seconds':time.time()-META['start'],'native_version':str(R.RhinoApp.Version)},f,indent=2)
 status('TERMINADO V4 errores='+str(len(ERRORS)))
except Exception:
 with open(os.path.join(ROOT,'verificacion','ERROR_RHINO.txt'),'w') as f:f.write(traceback.format_exc())
 print(traceback.format_exc());raise
