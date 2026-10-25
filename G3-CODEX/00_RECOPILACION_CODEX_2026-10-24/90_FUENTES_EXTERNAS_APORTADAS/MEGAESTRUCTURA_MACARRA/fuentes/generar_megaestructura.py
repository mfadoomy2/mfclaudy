from pathlib import Path
import numpy as np, math, random, json, pickle, gzip, time
from collections import defaultdict,Counter
import rhino3dm as rh
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'modelo'; OUT.mkdir(exist_ok=True)
SEED=11873;rng=np.random.default_rng(SEED);random.seed(SEED);TAU=2*math.pi
V=lambda a:np.array(a,dtype=float)
COLORS={
'01_SUELOS_HABITABLES':(226,223,205),'02_BORDES_AMARILLOS':(236,245,18),'03_ESCALERAS_PELDANOS':(245,246,41),'04_DESCANSILLOS':(206,218,184),'05_BARANDILLAS':(225,237,221),'06_MEGATRONCOS':(210,199,165),'07_COSTILLAS':(233,222,190),'08_CELULAS_PERFORADAS':(237,227,207),'09_TENSORES':(194,216,211),'10_MEMBRANAS':(146,207,190),'11_NERVIOS_MAGENTA':(246,12,133),'12_CONDUCTOS_CIAN':(73,192,199),'13_DEPOSITOS_CRISTAL':(98,198,205),'14_AGUA':(23,138,154),'15_NODULOS_TACTILES':(228,217,192),'16_MAQUINARIA':(72,86,83),'17_UNIONES_COBRE':(175,105,64),'18_LUZ':(239,247,148),'19_MOBILIARIO':(124,157,149),'20_ANCLAJES':(111,132,126),'21_PARTITURAS':(172,214,196)}
B={};curves=[];counts=Counter();routes=[]
def batch(layer,part):
 k=layer+'::'+part
 if k not in B:B[k]={'layer':layer,'name':part,'v':[],'f':[]}
 return B[k]
def mesh(v,f,layer,part):
 b=batch(layer,part);n=len(b['v']);b['v'].extend(np.asarray(v,float).tolist());b['f'].extend([[n+int(i) for i in face] for face in f]);counts['mesh_components']+=1

def unit(v):
 a=np.array(v,float);return a/max(np.linalg.norm(a),1e-10)
def frame(t):
 t=unit(t);a=np.array([0.,0.,1.]) if abs(t[2])<.91 else np.array([0.,1.,0.]);u=unit(np.cross(t,a));return u,np.cross(t,u)
def tube(points,radius,layer,part,sides=7,centerline=False):
 p=np.array(points,float);N=len(p)
 if N<2:return
 rr=np.broadcast_to(radius,(N,)) if np.isscalar(radius) else np.array(radius)
 v=[];f=[]
 for i in range(N):
  t=p[min(i+1,N-1)]-p[max(0,i-1)];u,w=frame(t)
  for j in range(sides):v.append(p[i]+rr[i]*(math.cos(TAU*j/sides)*u+math.sin(TAU*j/sides)*w))
 for i in range(N-1):
  for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;c=(i+1)*sides+(j+1)%sides;d=(i+1)*sides+j;f.extend([(a,b,c),(a,c,d)])
 v.extend([p[0],p[-1]]);a=len(v)-2;b=a+1
 for j in range(sides):f.extend([(a,(j+1)%sides,j),(b,(N-1)*sides+j,(N-1)*sides+(j+1)%sides)])
 mesh(v,f,layer,part);counts['tubes']+=1
 if centerline:curves.append((layer,part,p.tolist()))
def beam(a,b,r,layer,part,sides=7):tube([a,b],r,layer,part,sides)
def curve3(a,b,c,n=16):
 a,b,c=V(a),V(b),V(c);return np.array([(1-t)**2*a+2*t*(1-t)*b+t*t*c for t in np.linspace(0,1,n)])
def cyl(a,b,r,layer,part):beam(a,b,r,layer,part,12)
def box(center,dx,dy,dz,layer,part,ang=0):
 c=V(center);u=V([math.cos(ang),math.sin(ang),0]);w=V([-math.sin(ang),math.cos(ang),0]);v=[c+u*sx*dx/2+w*sy*dy/2+V([0,0,sz*dz/2]) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 faces=[(0,2,3),(0,3,1),(4,5,7),(4,7,6),(0,1,5),(0,5,4),(2,6,7),(2,7,3),(0,4,6),(0,6,2),(1,3,7),(1,7,5)];mesh(v,faces,layer,part)
def ellipsoid(c,r,layer,part,nu=18,nv=10):
 c=V(c);v=[];f=[]
 for j in range(nv+1):
  b=math.pi*j/nv
  for i in range(nu):a=TAU*i/nu;v.append(c+V(r)*V([math.sin(b)*math.cos(a),math.sin(b)*math.sin(a),math.cos(b)]))
 for j in range(nv):
  for i in range(nu):a=j*nu+i;b=j*nu+(i+1)%nu;c1=(j+1)*nu+i;d=(j+1)*nu+(i+1)%nu
  # avoid degenerate poles
  
 for j in range(nv):
  for i in range(nu):
   a=j*nu+i;b=j*nu+(i+1)%nu;c1=(j+1)*nu+i;d=(j+1)*nu+(i+1)%nu
   if j>0:f.append((a,b,c1))
   if j<nv-1:f.append((b,d,c1))
 mesh(v,f,layer,part)
def ring(c,r,layer,part,normal=(0,0,1),thick=.05,n=40):
 c=V(c);u,v=frame(normal);p=[c+r*(math.cos(a)*u+math.sin(a)*v) for a in np.linspace(0,TAU,n+1)];tube(p,thick,layer,part,6)
def disk(poly,thick,layer,part):
 p=np.array(poly);N=len(p);cen=p.mean(0);v=np.vstack([p,p-V([0,0,thick]),cen,cen-V([0,0,thick])]);f=[]
 for j in range(N):k=(j+1)%N;f.extend([(2*N,j,k),(2*N+1,N+k,N+j),(j,N+j,N+k),(j,N+k,k)])
 mesh(v,f,layer,part)
coords=[(-39,-13,2),(-27,-5,5.2),(-9,-9,8.7),(8,-2,12),(26,-8,15.1),(39,4,18.7),(24,12,22),(6,14,25.2),(-12,8,28.9),(-29,16,32.1),(-17,26,35.7),(3,25,39.1),(20,25,42.6),(-31,10,9),(-18,15,12.4),(-3,5,15.8),(12,-20,18.6),(32,-23,22.1),(18,-12,25.5),(0,-15,29.1),(-20,-10,32.4),(-35,-3,36),(-17,-2,39.4),(-3,-1,42.9),(14,5,46.2),(30,13,49.6),(3,14,49.4),(-13,17,46.2)]
labels=['UMBRAL DE CONTRABANDO','PLAZA DE LOS NERVIOS','TALLER DEL RESIDUO','FORO DESDOBLADO','ESTANCIA DE AGUA','MIRADOR ROTO','BAÑERA SUSPENDIDA','JARDÍN ELECTROMECÁNICO','BIBLIOTECA DE RUIDOS','BALCÓN DE LA RAÍZ','INVERNADERO IMPOSIBLE','TEATRO DE HILOS','CÁMARA DE LLUVIA','CUEVA COMÚN','COCINA DEL MICELIO','CRUCE HABITADO','FÁBRICA DE VIBRACIÓN','DEPÓSITO MUTANTE','SALA DE REPOSO','HABITACIÓN COLGADA','ARCHIVO DE PIELES','CAPILLA DEL CABLE','SALA DE GLISSANDI','PLAZA FISURADA','TORRE DE CONTACTO','FARO DESOBEDIENTE','NIDO ALTO','OBSERVATORIO POROSO']
NODES=[]
for i,c in enumerate(coords):
 NODES.append({'id':i,'c':V(c),'r':float(rng.uniform(4.2,6.8)),'aspect':float(rng.uniform(.72,1.20)),'phase':float(rng.uniform(0,TAU)),'name':labels[i]})
edges=[(i,i+1) for i in range(12)]+[(1,13),(13,14),(14,15),(15,3),(4,16),(16,17),(17,18),(18,19),(19,20),(20,21),(21,22),(22,23),(23,24),(24,25),(24,26),(23,27),(27,10),(15,6),(18,7),(8,20),(11,22),(12,24),(9,21),(14,2)]
adj=defaultdict(list)
for a,b in edges:adj[a].append(b);adj[b].append(a)
def radial(node,a):return node['r']*(1+.13*math.sin(3*a+node['phase'])+.075*math.cos(5*a-node['phase']))
def perimeter(node,a,z=0):
 r=radial(node,a);return node['c']+V([r*math.cos(a),r*node['aspect']*math.sin(a),z])
def at_entrance(i,a,tol=.34):
 for j in adj[i]:
  d=NODES[j]['c']-NODES[i]['c'];b=math.atan2(d[1],d[0]);dif=abs((a-b+math.pi)%TAU-math.pi)
  if dif<tol:return True
 return False

def build_deck(node):
 i=node['id'];part=f'E{i:02d}_{node["name"]}';c=node['c'];r=node['r'];angles=np.linspace(0,TAU,73)[:-1];p=np.array([perimeter(node,a) for a in angles]);disk(p,.27,'01_SUELOS_HABITABLES',part)
 # yellow edge truss, ivory subfloor lattice
 tube(np.vstack([p,p[0]]),.14,'02_BORDES_AMARILLOS',part,8)
 low=p-V([0,0,.92]);tube(np.vstack([low,low[0]]),.085,'02_BORDES_AMARILLOS',part,6)
 for j in range(0,72,2):
  k=(j+2)%72;beam(p[j],low[j],.055,'02_BORDES_AMARILLOS',part);beam(p[j],low[k],.045,'02_BORDES_AMARILLOS',part)
 for j in range(0,72,6):
  q=c+V([0,0,-.9]);beam(q,low[j],.12,'07_COSTILLAS',part)
 # boards / seams with irregular radial directions
 for j in range(36):
  a=j*TAU/36;u=perimeter(node,a);b=c+(u-c)*rng.uniform(.15,.35);beam(b+V([0,0,.012]),u+V([0,0,.012]),.012,'21_PARTITURAS',part,5)
 # guardrails have openings wherever the circulation meets the platform
 for j,a in enumerate(angles):
  k=(j+1)%72
  if at_entrance(i,a) or at_entrance(i,angles[k]):continue
  q=p[j];qq=p[k];beam(q,q+V([0,0,1.1]),.025,'05_BARANDILLAS',part,5);beam(q+V([0,0,1.1]),qq+V([0,0,1.1]),.028,'05_BARANDILLAS',part,5)
  beam(q+V([0,0,.55]),qq+V([0,0,.55]),.010,'09_TENSORES',part,5)
 # inhabited furniture in edge pockets, leaving middle and entrances empty
 for k in range(3):
  a=node['phase']+k*2.1
  if at_entrance(i,a,.5):continue
  q=perimeter(node,a)*.0+c+(perimeter(node,a)-c)*.64
  box(q+V([0,0,.38]),1.7,.72,.55,'19_MOBILIARIO',part,a+math.pi/2)
  box(q+V([math.cos(a)*.28,math.sin(a)*.28,.98]),1.7,.12,.75,'19_MOBILIARIO',part,a+math.pi/2)
  ellipsoid(q+V([0,0,.85]),(.21,.21,.12),'11_NERVIOS_MAGENTA',part,12,6)
 # scalloped tactile organs at rims, perforated armor and exciter cores
 for k in range(2+(i%3)):
  a=node['phase']+.5+k*1.72
  if at_entrance(i,a,.45):continue
  q=c+(perimeter(node,a)-c)*.81+V([0,0,1.3]);rr=.6+rng.random()*.45
  for zeta in range(7):
   z=(zeta/6-.5)*rr*2;rad=max(.15,rr*math.sqrt(max(.01,1-(z/rr)**2)))
   ring(q+V([0,0,z]),rad,'15_NODULOS_TACTILES',part,thick=.045,n=24)
  for t in range(12):
   aa=t*TAU/12;p1=[]
   for b in np.linspace(.1,math.pi-.1,15):p1.append(q+V([rr*math.sin(b)*math.cos(aa),rr*.8*math.sin(b)*math.sin(aa),rr*math.cos(b)]))
   tube(p1,.038,'15_NODULOS_TACTILES',part,5)
  ellipsoid(q,(rr*.4,rr*.38,rr*.55),'11_NERVIOS_MAGENTA',part,16,10)
  beam(q-V([0,0,rr]),q-V([0,0,1.5]),.07,'17_UNIONES_COBRE',part)

# Perforated architectural web: each curved quad is a ring around a real opening.
def perforated_grid(grid,layer,part):
 grid=np.array(grid);ny,nx=grid.shape[:2]
 for y in range(ny-1):
  for x in range(nx-1):
   q=np.array([grid[y,x],grid[y,x+1],grid[y+1,x+1],grid[y+1,x]]);center=q.mean(0);inset=center+(q-center)*rng.uniform(.59,.81);v=np.vstack([q,inset]);f=[]
   for k in range(4):j=(k+1)%4;f.extend([(k,j,4+j),(k,4+j,4+k)])
   mesh(v,f,layer,part)
   if (x+y)%3==0:tube(np.vstack([inset,inset[0]]),.018,'07_COSTILLAS',part,5)

def build_shell(node):
 i=node['id'];c=node['c'];r=node['r'];part=f'E{i:02d}_CAVERNAS_Y_VELAS'
 # Two to four asymmetrical vaulted wall fragments, not a continuous dome.
 for petal in range(2+i%3):
  a=node['phase']+petal*2.31;span=rng.uniform(.55,1.15)
  if at_entrance(i,a,.55):a+=.75
  h=rng.uniform(4.5,8.4);grid=[]
  for j in range(12):
   t=j/11;row=[]
   for k in range(9):
    u=k/8;aa=a+(u-.5)*span;rad=radial(node,aa)*(1-.37*math.sin(math.pi*t/1.7))
    q=c+V([rad*math.cos(aa),rad*node['aspect']*math.sin(aa),h*t]);q[:2]+=t*t*V([math.cos(a+.8),math.sin(a+.8)])[:2]*r*.58;row.append(q)
   grid.append(row)
  grid=np.array(grid);perforated_grid(grid,'08_CELULAS_PERFORADAS',part)
  for k in [0,4,8]:tube(grid[:,k],np.linspace(.18,.055,12),'07_COSTILLAS',part,7,True)
  for j in [0,5,11]:tube(grid[j],.085,'07_COSTILLAS',part,7)
  # transparent twisted sail stretched from independent, unequal boundaries
  p0=grid[-1,0];p1=grid[-1,-1];p2=c+V([math.cos(a+1.0)*r*.34,math.sin(a+1.0)*r*.3,h*.68]);p3=c+V([math.cos(a-1.2)*r*.82,math.sin(a-1.2)*r*.62,h*1.18]);g=[]
  for j in range(17):
   v=j/16
   for k in range(21):
    u=k/20;q=(1-u)*(1-v)*p0+u*(1-v)*p1+u*v*p2+(1-u)*v*p3;q[2]-=1.5*math.sin(math.pi*u)*math.sin(math.pi*v);g.append(q)
  f=[]
  for j in range(16):
   for k in range(20):b=j*21+k;f.extend([(b,b+1,b+22),(b,b+22,b+21)])
  mesh(g,f,'10_MEMBRANAS',part)
  g=np.array(g).reshape(17,21,3)
  for row in [g[0],g[-1],g[:,0],g[:,-1]]:tube(row,.035,'09_TENSORES',part,5)
  for k in range(0,21,4):tube(g[:,k],.016,'09_TENSORES',part,5)
  for j in range(0,17,4):tube(g[j],.013,'09_TENSORES',part,5)
  # suspension mast, spreaders, cables and clamp collars
  base=perimeter(node,a+span*.55,-.8);top=p1+V([0,0,1.3]);beam(base,top,.06,'20_ANCLAJES',part)
  for q in [p0,p2,p3]:beam(top,q,.020,'09_TENSORES',part,5)
  for t in [.08,.58,.94]:q=base+(top-base)*t;ring(q,.14,'17_UNIONES_COBRE',part,normal=top-base,thick=.035,n=12)


def build_stairs(a,b,eid):
 A=NODES[a];D=NODES[b]
 if A['c'][2]>D['c'][2]:A,D=D,A;a,b=b,a
 ca,cb=A['c'],D['c'];d=cb-ca;dh=unit([d[0],d[1],0]);side=V([-dh[1],dh[0],0]);a0=math.atan2(dh[1]/A['aspect'],dh[0]);b0=math.atan2(-dh[1]/D['aspect'],-dh[0]);start=ca+(perimeter(A,a0)-ca)*.70;end=cb+(perimeter(D,b0)-cb)*.70;start[2]=ca[2];end[2]=cb[2]
 dz=end[2]-start[2];nt=max(2,math.ceil(dz/.145));width=float(rng.uniform(1.8,2.6));bulge=(-1 if eid%2 else 1)*rng.uniform(.7,2.5)
 # one landing, then two continuous flights. Plateau around the central 12%.
 def elevation(t):
  if t<.44:return dz*(t/.44)*.5
  if t>.56:return dz*(.5+(t-.56)/.44*.5)
  return dz*.5
 points=[]
 for t in np.linspace(0,1,nt+1):
  q=start+(end-start)*t+side*bulge*math.sin(math.pi*t);q[2]=start[2]+elevation(t);points.append(q)
 part=f'R{eid:02d}_E{a:02d}_E{b:02d}'
 for j in range(nt):
  p,q=points[j],points[j+1];tan=q-p;ll=np.linalg.norm(tan[:2]);ang=math.atan2(tan[1],tan[0]);cc=(p+q)/2;cc[2]=q[2]-.075
  box(cc,max(.12,ll+.06),width,.15,'03_ESCALERAS_PELDANOS',part,ang);counts['treads']+=1
  # Yellow leading nosing and paired fasteners.
  yy=V([-math.sin(ang),math.cos(ang),0]);front=q.copy();front[2]=q[2]+.015;beam(front-yy*width*.5,front+yy*width*.5,.025,'02_BORDES_AMARILLOS',part,5)
 for sign in [-1,1]:
  rail=[];stringer=[]
  for j,q in enumerate(points):
   tang=points[min(j+1,nt)]-points[max(0,j-1)];s=unit([-tang[1],tang[0],0]);base=q+s*width*.5*sign;rail.append(base+V([0,0,1.10]));stringer.append(base-V([0,0,.23]));
   if j%2==0:beam(base,base+V([0,0,1.10]),.022,'05_BARANDILLAS',part,5)
  tube(rail,.03,'05_BARANDILLAS',part,6);tube(stringer,.12,'02_BORDES_AMARILLOS',part,7)
  # Independent nerves follow under the stair without occupying its walking plane.
  for cable in range(3):
   p=np.array(stringer)+V([0,0,-.35-cable*.13]);p[:,0]+=sign*.14; tube(p,.045 if cable else .07,'11_NERVIOS_MAGENTA',part,7,True)
 for t in [.2,.46,.72]:
  j=min(nt-1,int(t*nt));q=points[j]-V([0,0,.3]);support=q-V([.5,-.7,2.0]);beam(support,q-side*width*.5,.075,'07_COSTILLAS',part);beam(support,q+side*width*.5,.075,'07_COSTILLAS',part)
 center=points[len(points)//2];routes.append({'id':part,'from':a,'to':b,'width':width,'risers':nt,'rise_max':max(float(points[j+1][2]-points[j][2]) for j in range(nt)),'start':start.tolist(),'end':end.tolist(),'centerline':[q.tolist() for q in points]})
 curves.append(('CIRCULACION',part,[q.tolist() for q in points]));counts['stair_connections']+=1

def build_megatrunks():
 # Six primary trees thread the different rooms. Irregular branching replaces a grid of columns.
 trees=[((-31,-5,-5),[1,8,20,21,22]),((-10,1,-7),[2,14,15,8,27]),((12,-9,-5),[3,4,16,18,19,24]),((29,7,-6),[5,6,12,25]),((1,20,-4),[7,10,11,26]),((-29,19,-3),[13,9,10,27])]
 for t,(root,ids) in enumerate(trees):
  root=V(root);part=f'T{t:02d}_ARBOL_PORTANTE';top=NODES[ids[-1]]['c'];mid=(root+top)/2+V([rng.uniform(-3,3),rng.uniform(-4,4),0]);tr=curve3(root,mid,top,40);tube(tr,np.linspace(.67,.19,40),'06_MEGATRONCOS',part,12,True)
  for s,idx in enumerate(ids):
   node=NODES[idx];target=node['c']-V([0,0,.8]);h=(target[2]-root[2])/(top[2]-root[2]+.01);h=np.clip(h*.76,.05,.88);branch=tr[int(h*39)];mid=(branch+target)/2-V([0,0,2.7]);path=curve3(branch,mid,target,22);tube(path,np.linspace(.43,.14,22),'06_MEGATRONCOS',part,10,True)
   for j in range(4):
    a=node['phase']+j*TAU/4;tip=perimeter(node,a,-.7);stem=path[10];p=curve3(stem,(stem+tip)/2-V([0,0,1.3]),tip,18);tube(p,np.linspace(.20,.065,18),'07_COSTILLAS',part,8)
    # branching, perforated fillet under each cantilever
    grid=[]
    for yy in range(7):
     u=yy/6;row=[]
     for xx in range(8):
      v=xx/7;pa=path[min(21,10+int(v*10))];pb=p[min(17,int(v*17))];q=pa*(1-u)+pb*u;row.append(q)
     grid.append(row)
    perforated_grid(grid,'08_CELULAS_PERFORADAS',part)
  # Roots splay into an invented foundation landscape.
  for j in range(7):
   a=j*TAU/7+t;end=root+V([math.cos(a)*rng.uniform(5,10),math.sin(a)*rng.uniform(4,8),rng.uniform(-1,3)]);p=curve3(root,root+V([math.cos(a)*2,math.sin(a)*2,-2]),end,18);tube(p,np.linspace(.31,.08,18),'06_MEGATRONCOS',part,8)
   cyl(end-V([0,0,1.4]),end+V([0,0,.4]),.10,'20_ANCLAJES',part);box(end-V([0,0,1.4]),.7,.7,.15,'02_BORDES_AMARILLOS',part,a)
  for k in range(7):
   pts=tr.copy();pts[:,0]+=math.cos(k*TAU/7)*(.72+.07*k);pts[:,1]+=math.sin(k*TAU/7)*(.72+.07*k);pts[:,0]+=.21*np.sin(np.linspace(0,5*math.pi,len(pts))+k);tube(pts,.048+k%3*.017,'11_NERVIOS_MAGENTA',part,7,True)
  # collars and fine stave ribs make the trunk legible at close range.
  for j in range(2,39,4):ring(tr[j],.64*(1-j/65),'17_UNIONES_COBRE',part,normal=tr[min(j+1,39)]-tr[j-1],thick=.046,n=16)

def build_water(node):
 i=node['id'];part=f'E{i:02d}_HIDRAULICA_FANTASTICA';c=node['c'];r=node['r'];a=node['phase']+.8;q=c+V([math.cos(a)*r*.38,math.sin(a)*r*.3,.15]);rr=r*.36
 # Shallow bowl and its fluid surface, without closing pedestrian connections.
 ring(q+V([0,0,.35]),rr,'13_DEPOSITOS_CRISTAL',part,thick=.095,n=64)
 p=[q+V([rr*.96*math.cos(a),rr*.96*math.sin(a),.2]) for a in np.linspace(0,TAU,65)[:-1]];disk(p,.07,'14_AGUA',part)
 for k in range(7):
  wave=[]
  for a in np.linspace(0,TAU,100):rad=rr*(.1+k*.12)*(1+.035*math.sin(6*a+k));wave.append(q+V([rad*math.cos(a),rad*math.sin(a),.225+.015*math.sin(12*a)]))
  tube(wave,.011,'21_PARTITURAS',part,5)
 # Hanging vessels with irregular neck/belly profiles, glazed shells and inner liquid.
 for k in range(2):
  aa=a+k*2.4;top=perimeter(node,aa,-.45);length=rng.uniform(3.4,6.5);profile=[];vv=[];ff=[];N=25;M=24
  for j in range(N):
   t=j/(N-1);rad=.11+(.65+random.random()*.01)*math.sin(math.pi*t)**2*(.4+t);z=top[2]-length*t
   for m in range(M):ang=m*TAU/M;vv.append([top[0]+rad*math.cos(ang),top[1]+rad*math.sin(ang),z])
  for j in range(N-1):
   for m in range(M):aa=j*M+m;b=j*M+(m+1)%M;cc=(j+1)*M+m;dd=(j+1)*M+(m+1)%M;ff.extend([(aa,b,dd),(aa,dd,cc)])
  mesh(vv,ff,'13_DEPOSITOS_CRISTAL',part);ellipsoid(top-V([0,0,length*.70]),(.43,.43,length*.23),'14_AGUA',part,24,14)
  for h in [.07,.25,.63,.84]:ring(top-V([0,0,length*h]),.15+.65*math.sin(math.pi*h)**2*(.4+h),'17_UNIONES_COBRE',part,thick=.03,n=20)
  for h in range(4):ellipsoid(top-V([0,0,length+.4+h*.6]),(.08,.08,.15),'13_DEPOSITOS_CRISTAL',part,10,6)
  p=curve3(top,top+V([2,-1,1.5]),q,28);tube(p,.13,'12_CONDUCTOS_CIAN',part,10,True)


def machinery(node):
 i=node['id'];c=node['c'];r=node['r'];part=f'E{i:02d}_INSTALACIONES';aa=node['phase']+1.5;base=perimeter(node,aa,-1.1)
 # Invention: subfloor sonic engine; flanges, finned housings, valves, cables.
 for k in range(3):
  q=base+V([k*.62,0,-.5]);cyl(q-V([0,0,.4]),q+V([0,0,.4]),.26,'16_MAQUINARIA',part)
  for zz in np.linspace(-.45,.45,7):ring(q+V([0,0,zz]),.30,'17_UNIONES_COBRE',part,thick=.032,n=16)
  top=q+V([0,0,.56]);ring(top,.20,'11_NERVIOS_MAGENTA',part,thick=.04,n=16)
  for b in range(4):beam(top,top+V([math.cos(b*math.pi/2)*.2,math.sin(b*math.pi/2)*.2,0]),.018,'11_NERVIOS_MAGENTA',part,5)
 for k in range(5):
  start=c+V([math.cos(aa)*r*.5,math.sin(aa)*r*.5,-1.2-k*.13]);end=perimeter(node,aa+2+k*.12,1.5);p=curve3(start,(start+end)/2+V([0,0,-2.5]),end,30);tube(p,.038 if k else .075,'11_NERVIOS_MAGENTA',part,7,True)
 for k in range(3):
  a=aa+k*1.9;loc=perimeter(node,a,2.5+rng.random()*2);cyl(loc,loc+V([0,0,1.2]),.042,'20_ANCLAJES',part);ellipsoid(loc+V([0,0,1.28]),(.16,.16,.20),'18_LUZ',part,10,8)
 # random angled whip antennae above canopy
 if i%3==0:
  top=c+V([0,0,8]);anchor=perimeter(node,aa,0)
  beam(anchor,top,.055,'20_ANCLAJES',part)
  for k in range(10):end=top+V([math.cos(k*.4+aa)*rng.uniform(1,4),math.sin(k*.4+aa)*rng.uniform(1,3),rng.uniform(.5,3)]);beam(top,end,.022,'09_TENSORES',part,5);ellipsoid(end,(.065,.065,.1),'18_LUZ',part,8,5)

def build_connective_spaces():
 # Connections themselves become inhabited: wide landings, porticoes, hanging galleries.
 for eid,route in enumerate(routes):
  path=np.array(route['centerline']);mid=len(path)//2;c=path[mid];tang=unit(path[min(mid+1,len(path)-1)]-path[max(0,mid-1)]);u=unit([tang[0],tang[1],0]);side=np.array([-u[1],u[0],0]);part=f"R{eid:02d}_ESPACIO_ENTRE_CONEXIONES"
  if eid%3==0:
   radius=rng.uniform(2.5,4.3);poly=[]
   for a in np.linspace(0,TAU,49)[:-1]:
    q=c+u*math.cos(a)*2.0+side*math.sin(a)*radius*(1+.15*math.sin(3*a+eid));q[2]=c[2];poly.append(q)
   disk(poly,.23,'04_DESCANSILLOS',part);tube(poly+[poly[0]],.10,'02_BORDES_AMARILLOS',part,7);counts['inhabited_landings']+=1
   # two benches on the widened outer pockets, clear stair through the middle
   for sign in [-1,1]:box(c+side*radius*.76*sign+V([0,0,.35]),1.8,.6,.5,'19_MOBILIARIO',part,math.atan2(u[1],u[0]))
  if eid%2==0 or eid in [3,7,11]:
   length=len(path);grid=[];width=route['width']*.8
   for j in range(0,length):
    t=j/(length-1);height=3.3+1.8*math.sin(math.pi*t)+.65*math.sin(3*math.pi*t+eid);row=[]
    for k in range(13):
     v=k/12;qq=path[j]+side*((v-.5)*width*2.4)+V([0,0,height+1.5*(v-.5)*math.sin(t*math.pi*2+eid)-.8*math.sin(math.pi*v)]);row.append(qq)
    grid.append(row)
   grid=np.array(grid);vv=grid.reshape(-1,3);ff=[]
   for j in range(length-1):
    for k in range(12):a=j*13+k;ff.extend([(a,a+1,a+14),(a,a+14,a+13)])
   mesh(vv,ff,'10_MEMBRANAS',part)
   for k in [0,6,12]:tube(grid[:,k],.055,'07_COSTILLAS',part,6)
   for j in range(0,length,4):
    tube(grid[j],.045,'07_COSTILLAS',part,6)
    for sign,k in [(-1,0),(1,12)]:
     foot=path[j]+side*sign*width*.64;arch=curve3(foot,grid[j,k]+side*sign*.3,grid[j,k],12);tube(arch,np.linspace(.10,.038,12),'07_COSTILLAS',part,7)
     for cable in range(3):beam(foot+V([0,0,.3*cable]),grid[min(j+3,length-1),k],.011,'09_TENSORES',part,5)
   counts['covered_galleries']+=1
  # Further fluid and signal circuits sag between connections, rather than forming regular service trays.
  if eid%4==0:
   a=path[0]-V([0,0,.8]);b=path[-1]-V([0,0,.8]);p=curve3(a,(a+b)/2-V([0,0,4.0+eid%5]),b,40);tube(p,.11,'12_CONDUCTOS_CIAN',part,9,True)
   for j in range(3,39,5):ring(p[j],.16,'17_UNIONES_COBRE',part,normal=p[j+1]-p[j-1],thick=.035,n=12)

def write_files():
 d=rh.File3dm();d.Settings.ModelUnitSystem=rh.UnitSystem.Meters;d.Settings.ModelAbsoluteTolerance=.001;d.Settings.ModelAngleToleranceDegrees=.1;d.ApplicationName='Megaestructura Macarra / Adam'
 layers={};mats={}
 for layer,color in COLORS.items():
  mat=rh.Material();mat.Name=layer;mat.DiffuseColor=(*color,255);mat.SpecularColor=(180,180,180,255);mat.Shine=45
  if layer in ['10_MEMBRANAS','13_DEPOSITOS_CRISTAL']:mat.Transparency=.34 if layer=='10_MEMBRANAS' else .58
  if layer=='18_LUZ':mat.EmissionColor=(*color,255)
  mi=d.Materials.Add(mat);mats[layer]=mi;la=rh.Layer();la.Name=layer;la.Color=(*color,255);layers[layer]=d.Layers.Add(la)
 la=rh.Layer();la.Name='90_EJES_EDITABLES';la.Color=(250,60,135,255);la.Visible=False;axis=d.Layers.Add(la)
 la=rh.Layer();la.Name='91_RECORRIDO_CONTINUO';la.Color=(255,235,15,255);la.Visible=False;route_layer=d.Layers.Add(la)
 errors=[];totalv=totalf=0
 # Filter degenerate generated web faces, then validate each mesh.
 for key,b in B.items():
  v=np.asarray(b['v'],dtype=np.float32).astype(float);f=np.asarray(b['f'],dtype=np.int32);vec=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]);f=f[np.linalg.norm(vec,axis=1)>1e-7];b['v']=v.astype(np.float32);b['f']=f
  if not len(f):continue
  m=rh.Mesh()
  for p in v:m.Vertices.Add(*p)
  for face in f:m.Faces.AddFace(*(int(x) for x in face))
  m.Normals.ComputeNormals();m.Compact()
  if not m.IsValid:errors.append((key,m.IsValidWithLog))
  at=rh.ObjectAttributes();at.LayerIndex=layers[b['layer']];at.Name=b['name'];at.MaterialIndex=mats[b['layer']];at.MaterialSource=rh.ObjectMaterialSource.MaterialFromObject;at.ColorSource=rh.ObjectColorSource.ColorFromLayer;at.SetUserString('sistema',b['layer']);at.SetUserString('pieza',b['name']);at.SetUserString('edicion','malla editable por vértices; Explode para islas desconectadas');d.Objects.AddMesh(m,at);totalv+=len(v);totalf+=len(f)
 for layer,name,p in curves:
  at=rh.ObjectAttributes();at.LayerIndex=route_layer if layer=='CIRCULACION' else axis;at.Name=name;d.Objects.AddPolyline([rh.Point3d(*q) for q in p],at)
 # Rhino saved views.
 for name,eye,target in [('01_AXONOMETRIA',(116,-142,102),(0,3,23)),('02_REVERSO',(-110,95,88),(0,3,23)),('03_PLANTA',(0,3,180),(0,3,20)),('04_ALZADO',(0,-170,28),(0,3,28)),('05_INTERIOR',(24,-35,26),(3,0,22))]:
  view=rh.ViewInfo();view.Name=name;vp=view.Viewport;vp.SetCameraLocation(rh.Point3d(*eye));vp.SetCameraDirection(rh.Vector3d(*(V(target)-V(eye))));vp.SetCameraUp(rh.Vector3d(0,1,0) if name=='03_PLANTA' else rh.Vector3d(0,0,1))
  vp.SetFrustum(-65,65,-48,48,1,600);d.NamedViews.Add(view)
  if name=='01_AXONOMETRIA':d.Views.Add(view)
 path=OUT/'MEGAESTRUCTURA_MACARRA.3dm';ok=d.Write(str(path),8)
 serialnodes=[{**n,'c':n['c'].tolist()} for n in NODES];report={'seed':SEED,'unit':'m','spaces':serialnodes,'links':routes,'connected':True,'mesh_objects':len(B),'vertices':totalv,'triangles':totalf,'counts':dict(counts),'invalid_meshes':errors,'written':ok,'layers':list(COLORS),'notes':'Fantasía espacial. Geometría nueva derivada de las tres imágenes; no reconstrucción exacta ni cálculo constructivo.'}
 # Audit graph connectivity rather than claiming it from appearance.
 visited={0};todo=[0]
 while todo:
  for j in adj[todo.pop()]:
   if j not in visited:visited.add(j);todo.append(j)
 report['connected']=len(visited)==len(NODES);report['reachable_spaces']=len(visited)
 (ROOT/'verificacion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 with gzip.open(OUT/'geometria_render.pkl.gz','wb') as f:pickle.dump({'batches':B,'colors':COLORS,'nodes':serialnodes,'routes':routes},f,protocol=5)
 print(json.dumps({k:v for k,v in report.items() if k not in ['spaces','links','layers']},ensure_ascii=False),flush=True)

if __name__=='__main__':
 t=time.time()
 for node in NODES:
  build_deck(node);build_shell(node);machinery(node)
  if node['id'] in [4,5,6,12,16,17,25]:build_water(node)
  print('Estancia',node['id'],'componentes',sum(len(b['f']) for b in B.values()),flush=True)
 for i,(a,b) in enumerate(edges):build_stairs(a,b,i)
 build_connective_spaces();build_megatrunks();write_files();print('SECONDS',time.time()-t,flush=True)
