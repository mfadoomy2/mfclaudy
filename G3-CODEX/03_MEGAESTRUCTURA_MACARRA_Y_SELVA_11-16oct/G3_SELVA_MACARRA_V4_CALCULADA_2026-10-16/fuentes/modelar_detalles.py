# -*- coding: utf-8 -*-
# Runs inside Rhino 8 with RhinoCommon. It writes NEW files, never the current document.
from __future__ import unicode_literals
import Rhino as R, System, math, json, os, time, traceback
from System.Drawing import Color
from System.Collections.Generic import List
G=R.Geometry;D=R.DocObjects;P=G.Point3d;V=G.Vector3d;T=G.Transform
ROOT=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16'
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
 a.SetUserString('Proyecto','SELVA MACARRA V4 CALCULADA');a.SetUserString('Estado','Anteproyecto con predimensionado preliminar; no certificado')
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
 source=R.FileIO.File3dm.Read(os.path.join(ROOT,'modelos','SELVA_MACARRA_V4_FINAL.3dm'))
 # A structural node developed at real scale in metres.
 def tube(a,b,Dia,t,name):
  a=point(a);b=point(b);v=b-a;cy=G.Cylinder(G.Circle(G.Plane(a,v),Dia/2),v.Length);e=G.Extrusion.CreatePipeExtrusion(cy,Dia/2-t,True,True)
  if e:emit(e.ToBrep(),name,'27_DETALLES_TECNICOS','MARFIL')
 def hexnut(x,y,z,rad,h,name):
  pts=[P(x+rad*math.cos(j*math.pi/3),y+rad*math.sin(j*math.pi/3),z) for j in range(7)];extrude_curve(G.PolylineCurve(pts),h,name,'04_UNIONES','ACERO')
 sc=S['section_scale'];dia=.7112*sc;tt=.025*sc;br=.3556*sc;bt=.016*sc
 tube((0,0,-1.2),(0,0,1.2),dia,tt,'Tronco CHS D%.1f t%.1f'%(dia*1000,tt*1000))
 for a,b in [((0,0,.4),(-1.6,0,2)),((0,0,.4),(1.6,0,2)),((0,0,.4),(0,1.6,2))]:tube(a,b,br,bt,'Rama CHS D%.1f t%.1f'%(br*1000,bt*1000))
 for z in [.27,.39]:
  outer=G.Circle(P(0,0,z),.65).ToNurbsCurve();inner=G.Circle(P(0,0,z),dia/2).ToNurbsCurve();flat_curves([outer,inner],z,.035,'Brida anular 35 mm','04_UNIONES','ACERO')
 for j in range(16):
  a=2*math.pi*j/16;x=.57*math.cos(a);y=.57*math.sin(a);line((x,y,.23),(x,y,.50),.015,'Perno M30 clase8.8','04_UNIONES','ACERO');hexnut(x,y,.45,.026,.025,'Tuerca hexagonal M30');hexnut(x,y,.245,.026,.025,'Tuerca hexagonal M30')
 for j in range(8):
  a=j*math.pi/4;pts=[P(.46*math.cos(a),.46*math.sin(a),-.1),P(.65*math.cos(a),.65*math.sin(a),.27),P(.46*math.cos(a),.46*math.sin(a),.27)]
  b=G.Brep.CreateFromCornerPoints(pts[0],pts[1],pts[2],.001);v=V(-math.sin(a)*.018,math.cos(a)*.018,0);e=b.Faces[0].CreateExtrusion(G.LineCurve(P.Origin,P(v.X,v.Y,0)),True)
  emit(e,'Cartela rigidizadora18mm','04_UNIONES','ACERO')
 opts=R.FileIO.File3dmWriteOptions();opts.Version=8;opts.SaveRenderMeshes=True
 F.Write(os.path.join(ROOT,'modelos','D01_NUDO_RAMIFICADO_1a1.3dm'),opts)
 # A separate 1:1 layered envelope and deck connection.
 F=R.FileIO.File3dm();F.Settings.ModelUnitSystem=R.UnitSystem.Meters;LAY={};MAT={}
 z=0
 for name,h,col in [('Interior contrachapado18mm',.018,'MADERA'),('Aislamiento corcho160mm lambda0.040',.160,'CORCHO'),('Tablero estructural18mm',.018,'MADERA'),('Membrana impermeable2mm',.002,'NEGRO'),('Camara ventilada30mm',.030,'MARFIL'),('Piel exterior aluminio1.2mm',.0012,'VERDE')]:
  box(0,0,z,2.0,1.4,h,name,'29_ENVOLVENTE_ESTRATOS',col);z+=h+.09
 tube((0,-.2,-.35),(2,-.2,-.35),.4064*sc,.020*sc,'Viga principal bandeja calculada')
 box(0,-.35,-.10,2,.55,.012,'Placa reparto12mm','04_UNIONES','ACERO');box(0,-.35,-.088,2,.55,.015,'Banda separacion elastomerica15mm','29_ENVOLVENTE_ESTRATOS','NEGRO');box(0,-.35,-.073,2,.55,.12,'Forjado CLT120mm','29_ENVOLVENTE_ESTRATOS','MADERA')
 for x in [.2,.65,1.1,1.55,1.85]:
  for y in [-.25,.05]:line((x,y,-.2),(x,y,.08),.012,'Perno conexionM24','04_UNIONES','ACERO');hexnut(x,y,.06,.02,.02,'TuercaM24')
 path([(2.05,0,.1),(2.12,0,.05),(2.12,0,-.5),(2.12,0,-1.0)],.05,'Colector lluvia DN100','22_INSTALACIONES','CIAN');line((2.12,0,.04),(2.4,0,.04),.025,'RebosaderoDN50','22_INSTALACIONES','CIAN')
 F.Write(os.path.join(ROOT,'modelos','D02_ENVOLVENTE_Y_BANDEJA_1a1.3dm'),opts)
 # Flatten a pavilion and an elevator into independent editable files, keeping source materials/layers.
 objmap={str(o.Attributes.ObjectId):o for o in source.Objects};idef={str(d.Id):d for d in source.AllInstanceDefinitions}
 def basefile():
  out=R.FileIO.File3dm();out.Settings.ModelUnitSystem=R.UnitSystem.Meters;out.Settings.ModelAbsoluteTolerance=.001
  for l in source.AllLayers:
   ll=D.Layer();ll.Name=l.Name;ll.CopyAttributesFrom(l);out.AllLayers.Add(ll)
  for m in source.AllMaterials:out.AllMaterials.Add(D.Material(m))
  return out
 def flatadd(out,g,a,xfm):
  if isinstance(g,G.InstanceReferenceGeometry):
   for oid in idef[str(g.ParentIdefId)].GetObjectIds():
    ob=objmap[str(oid)];flatadd(out,ob.Geometry,ob.Attributes,xfm*g.Xform)
  else:
   gg=g.Duplicate();gg.Transform(xfm);aa=a.Duplicate();aa.ObjectId=System.Guid.NewGuid();aa.Mode=D.ObjectMode.Normal;out.Objects.Add(gg,aa)
 out=basefile();pp=next(d for d in source.AllInstanceDefinitions if d.Name=='PABELLON_4_REFUGIOS')
 for oid in pp.GetObjectIds():
  ob=objmap[str(oid)];flatadd(out,ob.Geometry,ob.Attributes,T.Identity)
 out.Write(os.path.join(ROOT,'modelos','UNIDAD_GRAN_BOVEDA_EDITABLE.3dm'),opts)
 out=basefile()
 for ob in source.Objects:
  if not ob.Attributes.IsInstanceDefinitionObject and ob.Attributes.Name.startswith('ASC1'):
   flatadd(out,ob.Geometry,ob.Attributes,T.Translation(-29.3,3.0,0))
 out.Write(os.path.join(ROOT,'modelos','D03_ASCENSOR_COMPLETO.3dm'),opts)
 with open(os.path.join(ROOT,'verificacion','detalles_completos.txt'),'w') as f:f.write('D01 D02 D03 y unidad generados como archivos independientes editables en metros.')
 print('DETALLES_V4_LISTOS')
except Exception:
 with open(os.path.join(ROOT,'verificacion','ERROR_DETALLES.txt'),'w') as f:f.write(traceback.format_exc())
 raise
