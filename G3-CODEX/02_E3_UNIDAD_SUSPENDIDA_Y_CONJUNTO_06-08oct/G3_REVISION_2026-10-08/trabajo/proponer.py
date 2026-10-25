import rhino3dm as r,numpy as np,json,pathlib,math,collections
from shapely.geometry import Polygon,Point,box,LineString
from shapely.ops import unary_union
from shapely.geometry.polygon import orient
from shapely import constrained_delaunay_triangles
B=pathlib.Path('/Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08')
PAL={'acero':'#363b42','vidrio':'#c8e6e5','ventana':'#93c7d0','madera':'#d9b587','privado':'#dedfdd','comun':'#42bfb0','barrio':'#ff7158','escalera':'#e8ae47','tecnico':'#9d879f','suelo':'#edeeec','cubierta':'#626c71'}
def rgb(c):return tuple(int(c[i:i+2],16) for i in [1,3,5])
def rounded(x,y,w,h,rad):return box(x+rad,y+rad,x+w-rad,y+h-rad).buffer(rad,quad_segs=12)
def corner(w,d,R=1.15):return box(0,0,w,d).difference(box(0,0,R,R).difference(Point(R,R).buffer(R,quad_segs=24)))
def arcpts(cx,cy,R,a,b,n=24):return np.array([[cx+R*math.cos(t),cy+R*math.sin(t)] for t in np.linspace(a,b,n)])
class Model:
 def __init__(self):self.f=r.File3dm();self.f.Settings.ModelUnitSystem=r.UnitSystem.Meters;self.f.Settings.ModelAbsoluteTolerance=.001;self.layers={};self.parts=[]
 def layer(self,name,color):
  if name not in self.layers:
   l=r.Layer();l.Name=name;l.Color=rgb(PAL.get(color,color))+(255,);mat=r.Material();mat.Name=name;mat.DiffuseColor=l.Color;mat.Transparency=.28 if color in ['vidrio','ventana'] else 0;mi=self.f.Materials.Add(mat);l.RenderMaterialIndex=mi;self.layers[name]=self.f.Layers.Add(l)
  return self.layers[name]
 def solid(self,p,z0,z1,layer,color='privado',name='',render=True):
  if p.is_empty:return
  if p.geom_type!='Polygon':
   for q in p.geoms:self.solid(q,z0,z1,layer,color,name,render)
   return
  if p.area<1e-7 or z1-z0<1e-6:return
  p=orient(p.simplify(.00001,preserve_topology=True),sign=1.0)
  pts=[r.Point3d(x,y,z0) for x,y in p.exterior.coords];cr=r.PolylineCurve(pts);ex=r.Extrusion.Create(cr,z1-z0,True)
  if ex is None:raise RuntimeError('No extrusion: '+layer)
  for h in p.interiors:ex.AddInnerProfile(r.PolylineCurve([r.Point3d(x,y,z0) for x,y in h.coords]))
  at=r.ObjectAttributes();at.LayerIndex=self.layer(layer,color);at.Name=name or layer;at.SetUserString('Estado','Anteproyecto; dimensiones de proyecto, prestaciones por justificar');self.f.Objects.Add(ex,at)
  if render:self.parts.append({'polygon':list(p.exterior.coords),'holes':[list(h.coords) for h in p.interiors],'z':[z0,z1],'layer':layer,'color':PAL.get(color,color),'name':name})
 def rect(self,x,y,w,d,z0,z1,layer,color='privado',name=''):self.solid(box(x,y,x+w,y+d),z0,z1,layer,color,name)
 def rod(self,a,b,R,layer,color='acero',n=8):
  a=np.array(a);b=np.array(b);d=b-a;d=d/np.linalg.norm(d);u=np.cross(d,[0,0,1] if abs(d[2])<.95 else [1,0,0]);u/=np.linalg.norm(u);v=np.cross(d,u);angles=np.linspace(0,2*np.pi,n,endpoint=False);vs=np.array([p+R*(np.cos(t)*u+np.sin(t)*v) for p in [a,b] for t in angles]);fs=[]
  for i in range(n):fs.extend([[i,(i+1)%n,(i+1)%n+n],[i,(i+1)%n+n,i+n]])
  for i in range(1,n-1):fs.extend([[0,i+1,i],[n,n+i,n+i+1]])
  mesh=r.Mesh()
  for p in vs:mesh.Vertices.Add(*p)
  for f in fs:mesh.Faces.AddFace(*f)
  mesh.Normals.ComputeNormals();at=r.ObjectAttributes();at.LayerIndex=self.layer(layer,color);at.Name=layer;self.f.Objects.AddMesh(mesh,at);self.parts.append({'triangles':vs[np.array(fs)].tolist(),'layer':layer,'color':PAL.get(color,color)})
 def save(self,name):
  path=B/(name+'.3dm');self.f.Write(str(path),8);(B/'trabajo'/(name+'.json')).write_text(json.dumps(self.parts,ensure_ascii=False));print(name,len(self.f.Objects),flush=True)

def spiral(m,cx=1.15,cy=1.15,z0=0,h=2.64):
 # 15 equal rises; 14 treads then continuous landing, effective width .84m.
 ri=.14;ro=1.0;step=.435;N=15;end=0;start=end-(N-1)*step
 m.solid(Point(cx,cy).buffer(.105,quad_segs=16),z0,z0+h+.12,'03 Caracol - mastil','acero')
 for k in range(N-1):
  a=start+k*step;b=a+step+.035;pts=np.r_[arcpts(cx,cy,ro,a,b,8),arcpts(cx,cy,ri,b,a,8)];p=Polygon(pts).buffer(-.008).buffer(.008,quad_segs=3);z=z0+(k+1)*h/N
  m.solid(p,z-.045,z,'03 Caracol - peldanos','madera',f'Peldaño {k+1:02}; contrahuella {h/N:.3f} m')
  riser=LineString([[cx+ri*math.cos(a),cy+ri*math.sin(a)],[cx+ro*math.cos(a),cy+ro*math.sin(a)]]).buffer(.012,cap_style=2)
  m.solid(riser,z-h/N,z-.045,'03 Caracol - tabicas','madera')
  for t in np.linspace(a,a+step,5,endpoint=False):
   x=cx+(ro-.012)*math.cos(t);y=cy+(ro-.012)*math.sin(t);m.rod([x,y,z],[x,y,z+.95],.008,'03 Caracol - barrotes')
 pts=[[cx+(ro-.012)*math.cos(t),cy+(ro-.012)*math.sin(t),z0+h/N+(t-start)/(step*(N-1))*h*(N-1)/N+.95] for t in np.linspace(start,0,110)]
 for a,b in zip(pts[:-1],pts[1:]):m.rod(a,b,.024,'03 Caracol - pasamanos','madera')
 m.rect(cx+ri,cy-.43,1.09,.86,z0+h-.12,z0+h,'03 Caracol - desembarco','madera')

def glass_line(m,a,b,z0,z1,openings=[],half=False,layer='06 Bloque de vidrio'):
 a=np.array(a);b=np.array(b);d=b-a;L=np.linalg.norm(d);t=d/L;n=np.array([-t[1],t[0]]);pitch=.10 if half else .20;bw=.09 if half else .19
 for s in np.arange(.035,L-pitch/2,pitch):
  for z in np.arange(z0+.03,z1-.15,.20):
   if any(s<e and s+bw>o and z<t1 and z+.19>t0 for o,e,t0,t1 in openings):continue
   c=a+t*(s+bw/2);p=Polygon([c+t*dt+n*dn for dt,dn in [(-bw/2,-.04),(bw/2,-.04),(bw/2,.04),(-bw/2,.04)]]);m.solid(p,z,z+.19,layer,'vidrio')
def glass_arc(m,cx,cy,R,a,b,z0,z1,band=None):
 length=R*(b-a);N=math.floor(length/.10);delta=(b-a)/N
 for k in range(N):
  ang=a+(k+.5)*delta;t=np.array([-math.sin(ang),math.cos(ang)]);n=np.array([math.cos(ang),math.sin(ang)]);c=np.array([cx,cy])+R*n
  p=Polygon([c+t*dt+n*dn for dt,dn in [(-.045,-.04),(.045,-.04),(.045,.04),(-.045,.04)]])
  for z in np.arange(z0+.03,z1-.15,.20):
   if band and z<band[1] and z+.19>band[0]:continue
   m.solid(p,z,z+.19,'06 Curvas - medio bloque por validar','vidrio')

def unit(kind='D'):
 m=Model();w=4.7;depth=4.7 if kind=='D' else 6.2;fp=corner(w,depth);loft=unary_union([box(0,2.35,w,4.7),box(2.35,0,w,2.35),Point(3.525,0).buffer(1.175,quad_segs=24).intersection(box(2.35,-1.175,4.7,0))]);roof=fp.union(loft) if kind=='D' else fp;H=5.44 if kind=='D' else 2.76
 m.solid(fp,-.24,0,'01 Bandeja - apoyo en porticos','acero');m.solid(fp.buffer(-.12),0,.035,'02 Suelo','madera')
 m.solid(roof,H,H+.24,'08 Cubierta','cubierta')
 if kind=='D':m.solid(loft,2.44,2.64,'02 Altillo L - sin triangulos superpuestos','madera');spiral(m)
 # rear service wall and side planes, front corner in glass
 m.rect(0,depth-.20,w,.20,.035,H,'05 Espalda aislada y registrable','privado')
 m.rect(.01,1.15,.18,depth-1.15,.035,H,'05 Testero opaco','privado')
 m.rect(w-.18,2.2,.18,depth-2.2,.035,H,'05 Testero opaco','privado')
 # Side window: one split at loft elevation, opening part downstairs.
 m.rect(w-.08,.1,.08,2.1,.12,2.42,'07 Ventana lateral - practicable','ventana')
 m.rect(w-.08,.1,.08,2.1,2.64,H,'07 Ventana lateral - fijo','ventana')
 for yy in [.08,2.2]:m.rect(w-.13,yy,.13,.06,0,H,'07 Marcos laterales','acero')
 m.rect(w-.13,.08,.13,2.18,2.44,2.64,'07 Travesano','acero')
 glass_arc(m,1.15,1.15,1.15,math.pi,1.5*math.pi,0,H)
 # front entrance and sliding door, with serviceable pocket shown.
 glass_line(m,[1.15,0],[w,0],0,H,[(1.05,2.15,0,2.24)]+([(1.20,3.56,2.64,H+.1)] if kind=='D' else []))
 m.rect(2.2,-.045,1.05,.035,0,2.23,'07 Hoja corredera - posicion cerrada','ventana')
 m.rect(2.14,-.08,.06,.16,0,2.3,'07 Marcos','acero');m.rect(3.25,-.08,.06,.16,0,2.3,'07 Marcos','acero');m.rect(2.14,-.08,1.17,.16,2.24,2.3,'07 Marcos','acero')
 m.rect(3.31,.05,1.1,.16,.05,2.3,'07 Reserva bolsillo - detalle pendiente','tecnico')
 if kind=='D':
  glass_arc(m,3.525,0,1.175,math.pi,2*math.pi,2.64,H,(3.54,4.64))
  for a,b in zip(arcpts(3.525,0,1.175,math.pi,2*math.pi,13)[:-1],arcpts(3.525,0,1.175,math.pi,2*math.pi,13)[1:]):
   p=LineString([a,b]).buffer(.025,cap_style=2);m.solid(p,3.54,4.64,'07 Ventana del ala - facetas','ventana')
  # close upper front straight portions missing from semicircle
  # Bay remains openly connected to the study; no wall across its mouth.
  # bathroom, kitchen and movable table under side window
  bath=rounded(.2,2.55,1.55,1.95,.22);walls=bath.difference(bath.buffer(-.08));walls=walls.difference(box(1.6,2.9,1.85,3.8));m.solid(walls,.04,2.36,'04 Bano - capsula con puerta','barrio')
  m.rect(.32,3.48,.85,.85,.04,.1,'04 Ducha','privado');m.solid(Point(1.3,4.02).buffer(.23),.04,.44,'04 WC','privado');m.rect(.4,2.69,.7,.45,.72,.84,'04 Lavabo','privado')
  m.rect(3.99,2.55,.56,1.95,.04,.9,'04 Cocina privada','privado');m.rect(3.96,2.55,.62,1.95,.9,.94,'04 Encimera','acero')
  m.solid(rounded(3.4,.68,.7,1.4,.06),.73,.77,'04 Mesa lateral','madera');m.rect(4.23,.68,.27,1.4,.04,.45,'04 Banco','madera')
  for y in [.8,1.68]:m.solid(rounded(2.99,y,.43,.43,.07),.40,.46,'04 Sillas - posicion uso','madera')
  for x in [.35,3.05]:
   m.solid(rounded(x,2.43,1.0,2.0,.08),2.7,3.13,'04 Dormir - dos camas','privado');m.rect(x+.05,4.05,.9,.33,3.13,3.23,'04 Almohadas','privado')
  m.rect(2.05,3.1,.1,1.32,2.64,4.24,'04 Filtro de descanso','tecnico')
  m.solid(rounded(2.65,-.57,1.55,.58,.10),3.37,3.42,'04 Mesa de estudio del ala','madera')
  edge=LineString([(0,2.35),(2.35,2.35),(2.35,1.60)]);m.solid(edge.buffer(.022,cap_style=2),3.62,3.68,'03 Barrera altillo - pasamanos','acero')
  for d in np.arange(0,edge.length,.105):
   p=edge.interpolate(d);m.rod([p.x,p.y,2.64],[p.x,p.y,3.66],.008,'03 Barrera altillo - barrotes')
 else:
  bath=rounded(.23,4.0,2.0,1.96,.18);m.solid(bath.difference(bath.buffer(-.10)).difference(box(1.30,3.85,2.2,4.2)),.04,2.55,'04 Bano adaptable - verificar giro','barrio')
  m.rect(.38,5,.9,.8,.04,.1,'04 Ducha','privado');m.solid(Point(1.72,5.55).buffer(.24),.04,.45,'04 WC','privado')
  m.rect(.2,2.0,.6,1.8,.04,.9,'04 Cocina privada','privado')
  m.solid(rounded(2.65,3.85,1.55,2.05,.09),.08,.5,'04 Cama','privado');m.rect(2.72,5.5,1.4,.35,.5,.61,'04 Almohada','privado');m.rect(2.38,3.5,.10,2.4,.04,1.55,'04 Filtro dormitorio','tecnico')
  m.solid(rounded(3.48,.72,.72,1.45,.06),.73,.77,'04 Mesa y estudio','madera');m.solid(rounded(2.91,1.2,.44,.44,.08),.4,.46,'04 Silla','madera');m.solid(rounded(.35,.62,1.45,.75,.2),.05,.5,'04 Estar','madera')
 # structural posts with explicit load path to tray, no dangling suspension rods
 for x,y in [(0,1.15),(1.15,0),(w,0),(w,depth),(0,depth)]:m.rect(x-.05,y-.05,.1,.1,-.24,H+.1,'01 Portico secundario - seccion provisional','acero')
 # Shaft reserves and grilles are spatial reservations, not fake sized ducts.
 m.rect(.18,depth-.42,.4,.22,.05,H,'09 Reserva tecnica registrable','tecnico')
 return m,{'kind':kind,'floor_gross':fp.area,'loft_gross':loft.area if kind=='D' else 0,'height':H+.24,'width':w,'depth':depth,'footprint':list(fp.exterior.coords),'loft':list(loft.exterior.coords) if kind=='D' else []}
if __name__=='__main__':
 allstats={}
 for kind,name in [('D','03_MODULO_D_duplex_propuesto'),('S','04_MODULO_S_una_planta')]:
  m,stats=unit(kind);m.save(name);allstats[kind]=stats
 (B/'trabajo/modulos_datos.json').write_text(json.dumps(allstats,indent=2))
