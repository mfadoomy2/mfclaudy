from pathlib import Path
import sys,json,math,contextlib,io,hashlib
import numpy as np
import rhino3dm as rh
from shapely.geometry import Point,Polygon,LineString,box,shape
from shapely.geometry.polygon import orient
from shapely.affinity import translate,rotate
from shapely.ops import unary_union,triangulate,nearest_points
from shapely import constrained_delaunay_triangles
P=Path(__file__).resolve().parents[1];R=P.parent
sys.path.insert(0,str(P/'fuentes/base_geometry/fuentes'))
with contextlib.redirect_stdout(io.StringIO()):import geometria as G
S=json.loads((P/'fuentes/ENCAJE_PARCELA.json').read_text())
parcel=shape(json.loads((P/'fuentes/PARCELA_REAL.geojson').read_text())['geometry'])
COL={'00_SUELO':(218,207,180),'01_MUROS':(200,211,192),'02_COLCHON':(239,230,207),'03_ROBLE':(161,102,63),'04_VESTIDOR':(105,139,117),'05_ASIENTO':(185,86,124),'06_VIDRIO':(120,183,184),'07_ACERO':(228,185,36),'08_COSTILLAS':(224,220,195),'09_MEMBRANAS':(138,181,164),'10_CABLES':(102,107,103),'11_ENERGIA':(189,58,132),'12_AGUA':(47,157,176),'13_METAL':(69,85,79),'14_COCINA':(166,66,68),'15_BANOS':(151,176,179),'16_PERSONAS':(90,111,104),'17_CUBIERTA_TERMICA':(221,213,187),'18_LUCERNARIOS':(170,206,192),'90_CONTEXTO':(160,162,157),'91_PARCELA':(127,146,120),'19_SOPORTE_PB':(219,215,188),'20_COMUN_EDIFICIO':(168,118,74),'21_NUCLEO_VERTICAL':(89,153,167)}
TOP=['09_MEMBRANAS','17_CUBIERTA_TERMICA','18_LUCERNARIOS','08_COSTILLAS','10_CABLES']
H=2.75
def roofmesh(pol,ht,step=.55):
 v=[];fa=[];x,y,X,Y=pol.bounds
 for xx in np.arange(x,X,step):
  for yy in np.arange(y,Y,step):
   cut=pol.intersection(box(xx,yy,min(X,xx+step),min(Y,yy+step)))
   for pp in G.polys(cut):
    for t in constrained_delaunay_triangles(pp).geoms:
     if t.area<1e-8:continue
     co=list(t.exterior.coords)[:3];i=len(v);v.extend([[a,b,ht(a,b)] for a,b in co]);fa.append([i,i+1,i+2])
 return v,fa
allreport=[];native=[]
if '--site-only' in sys.argv and (P/'verificacion/GEOMETRIA_3D.json').exists():allreport=[a for a in json.loads((P/'verificacion/GEOMETRIA_3D.json').read_text()) if not a['sitio']]
people=rh.File3dm.Read(str(P/'fuentes/personas_seleccionadas.3dm'))

def polys(g):return G.polys(g)
def curve(co,z):
 pts=[]
 for x,y in co:
  q=rh.Point3d(x,y,z)
  if not pts or q.DistanceTo(pts[-1])>1e-5:pts.append(q)
 if len(pts)<4:return None
 if pts[-1].DistanceTo(pts[0])<1e-5:pts[-1]=pts[0]
 else:pts.append(pts[0])
 return rh.PolylineCurve(pts)

def build(f,code,site=False,kind=0):
 f=dict(f);m=rh.File3dm();m.Settings.ModelUnitSystem=rh.UnitSystem.Meters;m.Settings.ModelAbsoluteTolerance=.001
 layers={};matids={};cache=[];stat={'codigo':code,'base':f['audit']['codigo'],'residentes':len(f['rooms']),'cota_suelo':4.2 if site else 0,'sitio':site}
 for k,c in COL.items():
  ma=rh.Material();ma.Name=k;ma.DiffuseColor=(*c,255);ma.Transparency=.7 if k=='06_VIDRIO' else .22 if k=='09_MEMBRANAS' else .0;ma.Shine=45 if k in ['07_ACERO','13_METAL'] else 5;matids[k]=m.Materials.Add(ma)
  la=rh.Layer();la.Name=k;la.Color=(*c,255);layers[k]=m.Layers.Add(la)
 Tr=lambda g:g;X=rh.Transform.Identity()
 if site:
  row=next(a for a in S['resultados'] if a['codigo']==f['audit']['codigo']);c=f['floor'].buffer(.12).centroid;cx,cy=c.x,c.y;x,y=row['centro_local_m'];ang=row['rotacion_grados']
  Tr=lambda g,cx=cx,cy=cy,x=x,y=y,ang=ang:translate(rotate(translate(g,-cx,-cy),ang,origin=(0,0)),x,y)
  a=math.radians(ang);ca,sa=math.cos(a),math.sin(a);X=rh.Transform.Identity();X.M00=ca;X.M01=-sa;X.M10=sa;X.M11=ca;X.M03=x-ca*cx+sa*cy;X.M13=y-sa*cx-ca*cy;X.M23=4.2
  if site:
   bank=max(f['banks'],key=lambda b:Tr(b['floor']).centroid.x)
   newcut=bank['T'](box(2.0,-.52,2.42,.52));inside=bank['T'](Point(1.40,0));outside=bank['T'](Point(2.95,0))
   solid=f['solid'].union(f['entry']['cut'].intersection(f['floor'].boundary.buffer(.06))).difference(newcut)
   entry={'cut':newcut,'inside':(inside.x,inside.y),'outside':(outside.x,outside.y)}
   f.update(solid=solid,entry=entry)
   fr=f['common'].difference(solid).difference(unary_union(f['furniture'])).buffer(-.45)
   root=next((p for p in polys(fr) if p.buffer(.002).covers(inside)),None)
   assert root is not None and all(root.buffer(.002).covers(p) for p in f['approaches']+[p for b in f['banks'] for p in b['approaches']]),code
   stat['entrada_revisada']='Acceso superior desde nucleo este y galeria al paso de servicios; la llegada desde calle transcurre por la planta baja comun.'
  front=LineString([(12.07,7.43),(13.28,-7.50)]);walkable=parcel.union(front.buffer(2.0,cap_style=2));env=Tr(f['floor'].buffer(.12));extfree=walkable.buffer(-.45).difference(env.buffer(.45));op=Tr(Point(f['entry']['outside']));root=next((p for p in polys(extfree) if p.buffer(.005).covers(op)),None)
  stat['invasion_parcela_m2']=round(env.difference(parcel).area,6);stat['paso_exterior90_desde_frente_en_cota_vivienda']=bool(root is not None and root.distance(LineString([(12.07,7.43),(13.28,-7.5)]))<.451)
  stat['llegada_principal']='Calle -> planta baja comun -> escalera o ascensor -> galeria -> vivienda a +4.20 m'
  stat['dormitorios_en_planta_baja']=0
 def Hpt(pt):
  x,y,z=pt;return [X.M00*x+X.M01*y+X.M03,X.M10*x+X.M11*y+X.M13,z+X.M23]
 def attrs(k,name):
  a=rh.ObjectAttributes();a.LayerIndex=layers[k];a.MaterialIndex=matids[k];a.MaterialSource=rh.ObjectMaterialSource.MaterialFromObject;a.ObjectColor=(*COL[k],255);a.ColorSource=rh.ObjectColorSource.ColorFromObject;a.Name=name;a.SetUserString('Estado','Geometria de estudio; sin calculo estructural ni comprobacion normativa');return a
 def addgeo(g,k,name,world=False):
  assert g is not None and g.IsValid,(code,k,name)
  g=g.Duplicate()
  if not world:g.Transform(X)
  assert g.IsValid,(code,k,name)
  m.Objects.Add(g,attrs(k,name))
 def mesh(v,fa,k,name,world=False):
  if not len(fa):return
  me=rh.Mesh()
  for q in v:me.Vertices.Add(*q)
  for q in fa:me.Faces.AddFace(*q)
  me.Normals.ComputeNormals();me.Compact();addgeo(me,k,name,world)
  cache.append({'layer':k,'name':name,'vertices':v if world else [Hpt(q) for q in v],'faces':fa})
 def cachepoly(g,z,h,k,name,world=False):
  verts=[];faces=[]
  for pol in polys(g):
   for ring in [pol.exterior]+list(pol.interiors):
    co=list(ring.coords)
    for a,b in zip(co[:-1],co[1:]):
     i=len(verts);verts.extend([[*a,z],[*b,z],[*b,z+h],[*a,z+h]]);faces.append([i,i+1,i+2,i+3])
   for t in constrained_delaunay_triangles(pol).geoms:
    if t.area<1e-9:continue
    co=list(t.exterior.coords)[:3];i=len(verts);verts.extend([[x,y,z+h] for x,y in co]);faces.append([i,i+1,i+2])
    i=len(verts);verts.extend([[x,y,z] for x,y in co]);faces.append([i+2,i+1,i])
  cache.append({'layer':k,'name':name,'vertices':verts if world else [Hpt(q) for q in verts],'faces':faces})
 def solid(g,z,h,k,name,world=False):
  g=g.simplify(.003,preserve_topology=True)
  for i,pol in enumerate(polys(g)):
   if pol.area<1e-7:continue
   pol=orient(pol,sign=1.0)
   pol=Polygon(pol.exterior,[ho.coords for ho in pol.interiors if Polygon(ho).area>1e-5])
   cr=curve(pol.exterior.coords,0)
   if cr is None:continue
   ex=rh.Extrusion.Create(cr,h,True)
   for ho in pol.interiors:
    q=curve(ho.coords,0)
    if q and not ex.AddInnerProfile(q):raise ValueError((name,pol.area,Polygon(ho).area,q.IsClosed))
   ex.Transform(rh.Transform.Translation(0,0,z));addgeo(ex,k,name+f'_{i}',world)
  cachepoly(g,z,h,k,name,world)
 def tube(points,r,k,name,world=False):
  # Connected tube mesh, with circular sections normal to each segment.
  pp=np.asarray(points,float);vv=[];ff=[]
  for i,p in enumerate(pp):
   d=pp[min(i+1,len(pp)-1)]-pp[max(0,i-1)];d/=np.linalg.norm(d);ref=np.array([0,0,1.]) if abs(d[2])<.95 else np.array([1.,0,0]);u=np.cross(d,ref);u/=np.linalg.norm(u);v=np.cross(d,u)
   for a in np.linspace(0,2*math.pi,10,endpoint=False):vv.append(list(p+r*(u*math.cos(a)+v*math.sin(a))))
   if i:
    for j in range(10):q=(i-1)*10+j;qn=(i-1)*10+(j+1)%10;ff.append([q,qn,qn+10,q+10])
  mesh(vv,ff,k,name,world)
 def slab(g,z,k,name,h=.04):solid(g,z,h,k,name)
 # Floor finish is exactly Z=0. The steel tray remains underneath, not in the circulation volume.
 solid(f['floor'],-.18,.18,'00_SUELO','Suelo continuo a cota 0')
 solid(f['solid'],0,H,'01_MUROS','Muros con huecos reales')
 for i,door in enumerate(f['doors'][1:]):solid(f['walls'].intersection(door).difference(f['windows'][0] if False else Polygon()),2.15,.60,'01_MUROS',f'Dintel_{i}')
 # Room assemblies have real supporting bases, a wall-hinged board and a concave seating shell.
 for room in f['rooms']:
  rt=lambda g:room['T'](G.tf(g,room['r']));rid=room['id']
  solid(rt(G.BED.buffer(-.03)),0,.12,'13_METAL',rid+' base a suelo');solid(rt(G.BED),.12,.24,'02_COLCHON',rid+' colchon 125x200')
  for j in range(2):solid(rt(box(.35,3.45+j*.02,1.36,3.80+j*.02)),.36+j*.045,.045,'02_COLCHON',rid+' almohada')
  solid(rt(G.SEAT),0,.42,'04_VESTIDOR',rid+' carcasa asiento bow apoyada');solid(rt(G.SEAT.buffer(-.025)),.42,.06,'05_ASIENTO',rid+' cojin concavo')
  for z in [.10,1.95,2.25]:solid(rt(G.WARD),z,.035,'03_ROBLE',rid+' balda curva')
  outer=Point(3.25,3.1).buffer(1.43).difference(Point(3.25,3.1).buffer(1.39)).intersection(box(3.25,1.5,5,4.7));solid(rt(outer),.1,2.19,'04_VESTIDOR',rid+' respaldo curvo armario')
  for a in np.linspace(-math.pi/2,math.pi/2,9):
   p0=(3.25+1.18*math.cos(a),3.1+1.18*math.sin(a));p1=(3.25+1.18*math.cos(a+.12),3.1+1.18*math.sin(a+.12));p=rt(Point(*p0));q=rt(Point(*p1));tube([(p.x,p.y,1.7),(q.x,q.y,1.7)],.018,'13_METAL',rid+' barra ropa curva')
  solid(rt(G.DESK),.75,.035,'03_ROBLE',rid+' tablero 180x90 bisagra canto corto')
  # Two triangular brackets hold the full cantilever; no table legs.
  for y in [.22,.86]:
   pts=[rt(Point(.045,y)),rt(Point(1.40,y)),rt(Point(.045,y))];tube([(pts[0].x,pts[0].y,.75),(pts[1].x,pts[1].y,.72),(pts[2].x,pts[2].y,.40)],.018,'13_METAL',rid+' escuadra plegable')
  p=rt(Point(.05,.55));q=rt(Point(.05,.10));s=rt(Point(.05,1.0));tube([(q.x,q.y,.75),(s.x,s.y,.75)],.025,'13_METAL',rid+' eje bisagra')
  solid(rt(G.STOOL),.43,.045,'05_ASIENTO',rid+' taburete asiento')
  for dx,dy in [(-.13,-.13),(.13,-.13),(-.13,.13),(.13,.13)]:
   p=rt(Point(.95+dx,1.50+dy));tube([(p.x,p.y,0),(p.x,p.y,.43)],.013,'13_METAL',rid+' pata taburete')
  # Curved glazing between seat/sill and lintel, same bow outline as plan.
  solid(rt(G.WIN).intersection(room['poly'].boundary.buffer(.10)),.48,1.95,'06_VIDRIO',rid+' vidrio curvo bow')
  solid(room['poly'].boundary.buffer(.06).intersection(rt(G.WIN)),0,.42,'01_MUROS',rid+' antepecho bow')
  solid(room['poly'].boundary.buffer(.06).intersection(rt(G.WIN)),2.43,.32,'01_MUROS',rid+' dintel bow')
  for z in [.48,2.43]:
   co=list(G.ARC.coords);world=[rt(Point(*q)) for q in co[::8]];tube([(p.x,p.y,z) for p in world],.023,'13_METAL',rid+' perfil curvo')
  # Individual ceiling protects the private room from the shared high roof.
  solid(room['poly'],2.75,.14,'17_CUBIERTA_TERMICA',rid+' techo privado aislado, espesor de estudio')
  # Ribbed outer garment follows the full concave outline, rather than a rectangular box.
  rp=room['poly'].representative_point();bd=room['poly'].boundary
  hroom=lambda x,y:2.99+.62*math.exp(-((x-rp.x)**2+(y-rp.y)**2)/5)
  for j in range(14):
   bp=bd.interpolate(j*bd.length/14)
   pts=[(bp.x+(rp.x-bp.x)*u,bp.y+(rp.y-bp.y)*u) for u in np.linspace(0,1,9)]
   tube([(x,y,hroom(x,y)-.035) for x,y in pts],.025,'08_COSTILLAS',rid+' costilla bajo tela')
   tube([(bp.x,bp.y,2.89),(bp.x,bp.y,hroom(bp.x,bp.y)-.035)],.018,'08_COSTILLAS',rid+' apoyo corto sobre techo privado')
  v,fa=roofmesh(room['poly'].simplify(.015),hroom)
  mesh(v,fa,'09_MEMBRANAS',rid+' sobretecho textil con camara ventilada')
 # Bathroom equipment. Footprints are schematic and match the plan; no invented accessibility claim.
 for i,b in enumerate(f['banks']):
  T=b['T']
  solid(b['floor'],2.75,.14,'17_CUBIERTA_TERMICA','Techo completo de servicios')
  for sign in [1,-1]:
   shower=box(.08,1.30,.98,2.20) if sign==1 else box(1.02,-2.20,1.92,-1.30)
   wc=Point(1.6,1.9) if sign==1 else Point(.4,-1.9);sink=box(1.4,.80,1.85,1.12) if sign==1 else box(.15,-1.12,.60,-.80)
   solid(T(shower),0,.035,'15_BANOS','Plato ducha 90x90');solid(T(wc.buffer(.15)),0,.32,'15_BANOS','Pie WC');solid(T(wc.buffer(.22)),.32,.1,'15_BANOS','Taza WC esquema');solid(T(sink),0,.80,'15_BANOS','Lavabo con apoyo')
   sp=T(shower.centroid);tube([(sp.x,sp.y,.04),(sp.x,sp.y,2.1)],.014,'12_AGUA','Ducha')
 # Common pieces remain within the audited footprints.
 for j,g in enumerate(f['kitchens']+f['utility']):
  solid(g,0,.85,'14_COCINA','Mueble cocina zocalo continuo');solid(g,.85,.045,'03_ROBLE','Encimera')
  x,y,X0,Y=g.bounds;axis=X0-x>Y-y
  if axis and X0-x>1.5:
   sink=box(x+.18,y+.12,x+.72,min(Y-.08,y+.49));hob=box(X0-.75,y+.06,X0-.15,min(Y-.05,y+.55));solid(sink,.895,.012,'13_METAL','Fregadero');solid(hob,.895,.008,'13_METAL','Placa cocina')
 for j,g in enumerate(f['tables']+f['work']):
  solid(g,.73,.045,'03_ROBLE','Mesa comun tablero');x,y,X0,Y=g.bounds
  corners=list(g.buffer(-.10,join_style=2).minimum_rotated_rectangle.exterior.coords)[:4]
  for xx,yy in corners:tube([(xx,yy,0),(xx,yy,.73)],.022,'13_METAL','Pata mesa comun dentro de huella')
 for j,g in enumerate(f['chairs']):
  solid(g,.43,.045,'05_ASIENTO','Asiento comedor');p=g.centroid
  for dx,dy in [(-.10,-.10),(.10,-.10),(-.10,.10),(.10,.10)]:tube([(p.x+dx,p.y+dy,0),(p.x+dx,p.y+dy,.43)],.012,'13_METAL','Pata silla')
 for j,g in enumerate(f['sofas']):
  solid(g,0,.15,'13_METAL','Base sofa');solid(g.buffer(-.035),.15,.28,'05_ASIENTO','Asiento sofa');x,y,X0,Y=g.bounds;back=box(x,y,X0,y+.14) if X0-x>Y-y else box(x,y,x+.14,Y);solid(back,.43,.35,'05_ASIENTO','Respaldo sofa')
 for w in f['wc']:solid(w.intersection(f['floor'].boundary.buffer(.08)),.45,1.95,'06_VIDRIO','Paño comun operable')
 # Steel tray: yellow perimeter and alternating diagonals, directly under the occupied floor.
 for poly in polys(f['floor']):
  co=list(poly.exterior.simplify(.08).coords)
  tube([(x,y,-.22) for x,y in co],.035,'07_ACERO','Cordon superior bandeja');tube([(x,y,-.52) for x,y in co],.035,'07_ACERO','Cordon inferior bandeja')
  n=max(4,int(poly.exterior.length/.85))
  for i in range(n):
   a=poly.exterior.interpolate(i*poly.exterior.length/n);b=poly.exterior.interpolate((i+1)*poly.exterior.length/n);tube([(a.x,a.y,-.52),(b.x,b.y,-.22)],.018,'07_ACERO','Diagonal bandeja')
 # Common roof height is a designed hypothesis, not a force-form solution.
 x0,y0,x1,y1=f['core'].bounds
 def mainht(x,y):
  u=(x-x0)/max(.1,x1-x0);v=(y-y0)/max(.1,y1-y0)
  if kind==1:return 3.85+.65*math.sin(math.pi*u)*math.cos(math.pi*v)
  return 4.05+.78*math.sin((4 if kind==2 else 2)*math.pi*u)*(2*v-1)
 # A field of small edge masts branches above head height. None are placed in the audited passage.
 border=f['floor'].boundary.difference(f['priv'].buffer(.18)).difference(f['entry']['cut'].buffer(.40))
 supports=[]
 for seg in G.parts(border):
  if seg.length<.8:continue
  for t in np.linspace(.15,.85,max(1,int(seg.length/3))):
   pt=seg.interpolate(t*seg.length)
   if all(pt.distance(p)>.9 for p in supports) and pt.distance(unary_union(f['furniture']))>.14:
    trial=f['common'].difference(f['solid']).difference(unary_union(f['furniture']+[p.buffer(.13) for p in supports+[pt]])).buffer(-.45)
    root=next((p for p in polys(trial) if p.buffer(.002).covers(Point(f['entry']['inside']))),None)
    if root is not None and all(root.buffer(.002).covers(p) for p in f['approaches']+[q for b in f['banks'] for q in b['approaches']]):supports.append(pt)
 for i,p in enumerate(supports):
  tube([(p.x,p.y,-.52),(p.x,p.y,mainht(p.x,p.y)+.05)],.055,'08_COSTILLAS','Mastil en borde sin pilar central')
  ref=f['common'].representative_point();dx,dy=ref.x-p.x,ref.y-p.y;norm=max(1,math.hypot(dx,dy));dx/=norm;dy/=norm
  for sign in [-1,1]:
   a=(p.x+dx*.5-dy*sign*.4,p.y+dy*.5+dx*sign*.4);b=(p.x+dx-dy*sign*.65,p.y+dy+dx*sign*.65)
   tube([(p.x,p.y,2.8),(*a,mainht(*a)-.25),(*b,mainht(*b)-.04)],.035,'08_COSTILLAS','Rama sobre circulacion')
  if i%2==0:
   tube([(p.x+.08,p.y,-.48),(p.x+.08,p.y,3.65)],.018,'11_ENERGIA','Conducto energia visible propuesta');tube([(p.x-.08,p.y,-.48),(p.x-.08,p.y,3.65)],.025,'12_AGUA','Bajante propuesta')
 # Common canopy cells follow the connected common spaces, rising at places of gathering.
 cells=[f['core'].difference(f['priv']).difference(unary_union(f['baths']))]
 if kind==2:
  mid=f['floor'].centroid.x;cells=[cells[0].intersection(box(-100,-100,mid,100)),cells[0].intersection(box(mid,-100,100,100))]
 for ii,cell in enumerate(cells):
  for pol in polys(cell):
   pol=pol.simplify(.025);ht=mainht
   v,fa=roofmesh(pol,ht)
   mesh(v,fa,'09_MEMBRANAS','Vela comun / geometria exploratoria sin equilibrio calculado')
   # Weather layer under the additional textile; translucent above gathering areas.
   mesh([[xx,yy,zz-.22] for xx,yy,zz in v],fa,'18_LUCERNARIOS','Cubierta comun bajo sobretecho textil')
   co=list(pol.exterior.coords);tube([(xx,yy,ht(xx,yy)) for xx,yy in co],.018,'10_CABLES','Cable de borde comun')
   # Seal the elevated weather roof with clerestory glazing, above the private ceiling.
   vv=[];ff=[]
   for a,b in zip(co[:-1],co[1:]):
    j=len(vv);vv.extend([[*a,H],[*b,H],[*b,ht(*b)-.22],[*a,ht(*a)-.22]]);ff.append([j,j+1,j+2,j+3])
   mesh(vv,ff,'06_VIDRIO','Claraboya perimetral de sala comun')
 # Figures sourced from supplied PERSONAS file, grounded and away from clear passage.
 reserved=unary_union(f['furniture']+[f['solid']]);stand=f['common'].difference(reserved.buffer(.40)).buffer(-.30)
 if not stand.is_empty:
  points=[]
  for po in polys(stand):
   pp=po.representative_point()
   if all(pp.distance(q)>1.0 for q in points):points.append(pp)
  for j,p in enumerate(points[:min(4,len(f['rooms']))]):
   src=list(people.Objects)[3 if j%2==0 else 4].Geometry.Duplicate();src.Transform(rh.Transform.Translation(p.x,p.y,0));addgeo(src,'16_PERSONAS','Persona de PERSONAS.3dm apoyada en cota 0')
   if isinstance(src,rh.Mesh):
    vv=[[q.X,q.Y,q.Z] for q in src.Vertices];ff=[]
    for face in src.Faces:ff.append([face[0],face[1],face[2]] if face[2]==face[3] else list(face));
    cache.append({'layer':'16_PERSONAS','name':'Persona','vertices':[Hpt(q) for q in vv],'faces':ff})
 if site:
  solid(parcel,-.18,.18,'91_PARCELA','Planta baja comun a cota 0',True)
  wp=Tr(f['floor']);bx,by,bX,bY=wp.bounds
  # New main supports are below the housing, leaving its interior free of trunks.
  roots=[]
  for i in range(4):
   desired=Point(bx+(bX-bx)*(i+.5)/4,(-2.8 if i%2==0 else 2.3))
   foot=nearest_points(wp,desired)[0];roots.append(foot)
   solid(foot.buffer(.30),0,.045,'07_ACERO','Placa de apoyo de estudio, sin cimentacion calculada',True)
   tube([(foot.x,foot.y,.045),(foot.x,foot.y,2.65)],.16,'19_SOPORTE_PB','Tronco bajo vivienda',True)
   for dx,dy in [(-2.5,-2.5),(-2.5,2.5),(2.5,-2.5),(2.5,2.5)]:
    target=nearest_points(wp,Point(foot.x+dx,foot.y+dy))[0]
    tube([(foot.x,foot.y,2.35),((foot.x+target.x)/2,(foot.y+target.y)/2,3.20),(target.x,target.y,3.68)],.09,'19_SOPORTE_PB','Rama hasta bandeja inferior',True)
  # Ground level belongs to the whole building. No private bedroom is placed here.
  for g,name in [(box(16,-.8,20,.0),'Sala comun / sofa'),(box(18,3,22,3.8),'Sala comun / segundo sofa')]:
   solid(g,0,.42,'05_ASIENTO',name,True)
  for x in [23.5,26.5]:
   solid(box(x,-3.4,x+2.3,-2.7),.86,.065,'20_COMUN_EDIFICIO','Banco de taller colectivo',True)
   for xx in [x+.15,x+2.15]:solid(box(xx,-3.35,xx+.08,-2.75),0,.86,'13_METAL','Apoyo banco taller',True)
  solid(box(34,-5.42,38,-4.77),0,.88,'14_COCINA','Cocina integrada en franja sur',True)
  solid(box(31.65,-5.42,33.85,-4.77),0,2.35,'20_COMUN_EDIFICIO','Almacenaje integrado con cocina y servicios',True)
  communal_table=box(30,-1.7,33.6,-.75);solid(communal_table,.73,.05,'20_COMUN_EDIFICIO','Mesa colectiva del edificio',True)
  for xx in [30.15,33.45]:
   for yy in [-1.55,-.90]:tube([(xx,yy,0),(xx,yy,.73)],.035,'13_METAL','Apoyo mesa PB',True)
  for xx in [30.4,31.3,32.2,33.1]:
   for yy in [-2.15,-.30]:
    solid(Point(xx,yy).buffer(.21),.43,.045,'05_ASIENTO','Asiento comedor PB',True)
    tube([(xx,yy,0),(xx,yy,.43)],.045,'13_METAL','Apoyo asiento PB',True)
  care=G.rounded(23.0,6.5,27.0,9.0,.35).intersection(parcel.buffer(-.15))
  carewall=care.boundary.buffer(.07).difference(box(23.9,6.2,25.1,6.8));solid(carewall,0,2.65,'01_MUROS','Cuidados y conversacion reservada / uso comun',True);solid(care,2.65,.14,'17_CUBIERTA_TERMICA','Techo cuidados PB',True)
  service=parcel.buffer(-.07).intersection(box(25.5,-9,38.1,-4.75))
  servicewall=service.boundary.buffer(.06).difference(box(28.05,-4.95,29.15,-4.5)).difference(box(31.65,-5.55,38.2,-4.5))
  leftbath=box(25.60,-7.20,28.0,-4.82);rightbath=box(29.2,-7.20,31.60,-4.82)
  internal=unary_union([LineString([(28.,-7.3),(28.,-4.75)]).buffer(.06),LineString([(29.2,-7.3),(29.2,-4.75)]).buffer(.06),LineString([(31.6,-7.3),(31.6,-4.75)]).buffer(.06)])
  side_doors=unary_union([box(27.8,-6.65,28.2,-5.65),box(29.,-6.05,29.4,-5.05)])
  servicewall=servicewall.union(internal.difference(side_doors))
  solid(servicewall,0,2.6,'15_BANOS','Pared continua de servicios sur / sin caja ante escalera',True)
  solid(service,2.6,.14,'17_CUBIERTA_TERMICA','Techo continuo cocina almacenaje aseos en borde sur',True)
  for x,y in [(26.1,-6.75),(31.05,-6.75)]:
   solid(Point(x,y).buffer(.22),0,.42,'15_BANOS','WC PB en borde, acceso lateral',True)
  # The stair approach stays empty; this ground level contains no detached toilet block there.
  # Two real flights reach +4.20: 24 risers x 0.175 m, nominal tread 0.28 m.
  sx=45.2;sy=-5.1;run=12*.28
  for j in range(12):
   z=(j+1)*.175;solid(box(sx+j*.28,sy,sx+(j+1)*.28,sy+1.2),z-.12,.12,'07_ACERO','Escalera primer tramo',True)
   z=2.1+(j+1)*.175;xx=sx+run-(j+1)*.28;solid(box(xx,sy+1.4,xx+.28,sy+2.6),z-.12,.12,'07_ACERO','Escalera segundo tramo',True)
  solid(box(sx+run,sy,sx+run+1.2,sy+2.6),1.98,.12,'07_ACERO','Meseta +2.10',True)
  for yy in [sy+.05,sy+1.15]:
   tube([(sx,yy,-.1),(sx+run,yy,2.0)],.055,'13_METAL','Zanca primer tramo',True)
   tube([(sx,yy,1.1),(sx+run,yy,3.2)],.022,'13_METAL','Pasamanos primer tramo',True)
  for yy in [sy+1.45,sy+2.55]:
   tube([(sx+run,yy,2.0),(sx,yy,4.1)],.055,'13_METAL','Zanca segundo tramo',True)
   tube([(sx+run,yy,3.2),(sx,yy,5.3)],.022,'13_METAL','Pasamanos segundo tramo',True)
  # Lift with lower and upper doors, real cabin at the upper stop and guide rails.
  shaft=box(50,-4.5,52.1,-2.4);shwall=shaft.boundary.buffer(.045).difference(box(50.50,-2.55,51.60,-2.25))
  solid(shwall,-1.1,8.30,'06_VIDRIO','Hueco de ascensor de estudio con foso',True)
  solid(box(50.3,-4.2,51.8,-2.65),4.05,.15,'21_NUCLEO_VERTICAL','Cabina ascensor / piso a +4.20',True)
  cab=box(50.3,-4.2,51.8,-2.65);solid(cab.boundary.buffer(.025).difference(box(50.45,-2.8,51.65,-2.4)),4.2,2.2,'06_VIDRIO','Cabina ascensor con puerta abierta',True)
  for xx in [50.15,51.95]:tube([(xx,-4.3,-1.1),(xx,-4.3,7.1)],.025,'13_METAL','Guia ascensor',True)
  for z in [0,4.2]:
   solid(box(50.43,-2.48,50.50,-2.38),z,2.2,'21_NUCLEO_VERTICAL','Jamba ascensor',True);solid(box(51.60,-2.48,51.67,-2.38),z,2.2,'21_NUCLEO_VERTICAL','Jamba ascensor',True);solid(box(50.43,-2.48,51.67,-2.38),z+2.2,.12,'21_NUCLEO_VERTICAL','Dintel ascensor',True)
  landing=box(44,-3.7,52.3,.50).difference(box(45.2,-5.3,50,-2.5)).difference(shaft)
  ep=Tr(Point(f['entry']['outside']));ip=Tr(Point(f['entry']['inside']))
  bridge=LineString([(ip.x,ip.y),(ep.x,ep.y),(44.8,ep.y),(45,-1.0)]).buffer(.75,cap_style=2)
  upper=unary_union([landing,bridge]).difference(wp.buffer(-.03));assert upper.difference(parcel).area<.01,(code,upper.difference(parcel).area)
  solid(upper,4.05,.15,'07_ACERO','Galeria y rellano a +4.20',True)
  # The ground-floor landing door stays closed while the cabin is upstairs.
  solid(box(50.50,-2.46,51.60,-2.42),0,2.10,'06_VIDRIO','Puerta cerrada ascensor en planta baja',True)
  for side in [sy+.05,sy+1.15]:
   for j in range(0,13):
    xx=sx+j*.28;zz=j*.175;tube([(xx,side,zz),(xx,side,zz+1.10)],.012,'13_METAL','Montante escalera primer tramo',True)
  for side in [sy+1.45,sy+2.55]:
   for j in range(0,13):
    xx=sx+run-j*.28;zz=2.1+j*.175;tube([(xx,side,zz),(xx,side,zz+1.10)],.012,'13_METAL','Montante escalera segundo tramo',True)
  # Rails leave the connection and stair opening unobstructed.
  rail=upper.boundary.difference(wp.buffer(.15)).difference(box(43.9,-3.8,45.3,-2.35)).difference(shaft.buffer(.15))
  for seg in G.parts(rail):
   if seg.length<.10:continue
   pts=list(seg.simplify(.05).coords);tube([(x,y,5.30) for x,y in pts],.022,'13_METAL','Barandilla galeria superior',True)
   for q in np.arange(0,seg.length,.9):
    a=seg.interpolate(q);tube([(a.x,a.y,4.20),(a.x,a.y,5.30)],.018,'13_METAL','Montante barandilla',True)
  # Ground-level circulation audit includes the new supports and ground programme.
  obs=[p.buffer(.16) for p in roots]+[box(16,-.8,20,0),box(18,3,22,3.8),box(23.5,-3.4,25.8,-2.7),box(26.5,-3.4,28.8,-2.7),box(34,-5.42,38,-4.77),box(31.65,-5.42,33.85,-4.77),communal_table,care.buffer(.07),servicewall,leftbath,rightbath,box(45.2,-5.1,49.76,-2.5),shaft]
  obs += [Point(xx,yy).buffer(.21) for xx in [30.4,31.3,32.2,33.1] for yy in [-2.15,-.30]]
  pbfree=walkable.difference(unary_union(obs)).buffer(-.45);pbroot=next((g for g in polys(pbfree) if g.buffer(.002).covers(Point(11.6,0))),None)
  targets={'ascensor':(51,-1.8),'escalera':(44.7,-4.5),'cuidados':(24.5,5.9),'aseo1':(28.6,-6.15),'aseo2':(28.6,-5.55),'sala':(21,1.5),'taller':(26,-1.8)}
  stat['recorridos_PB90']={k:bool(pbroot is not None and pbroot.buffer(.002).covers(Point(v))) for k,v in targets.items()}
  assert all(stat['recorridos_PB90'].values()),(code,stat['recorridos_PB90'])
  for j,(px,py) in enumerate([(18,1.7),(29,.8),(47,-1.2)]):
   src=list(people.Objects)[3+j].Geometry.Duplicate();src.Transform(rh.Transform.Translation(px,py,0));addgeo(src,'16_PERSONAS','Uso compartido planta baja',True)
   vv=[[q.X,q.Y,q.Z] for q in src.Vertices];ff=[list(fa) if fa[2]!=fa[3] else list(fa[:3]) for fa in src.Faces];cache.append({'layer':'16_PERSONAS','name':'Persona PB','vertices':vv,'faces':ff})
  stat['PB_programa']=['sala comun','comedor y cocina del edificio','taller','cuidados','aseos en borde','ascensor','escalera']
  stat['caja_ante_escalera_retirada']=True;stat['PB_servicios']='Cocina almacenaje y aseos integrados en borde sur; llegada a escalera libre';stat['PB_viviendas']=0;stat['cota_primera_vivienda']=4.2;stat['escalera']={'contrahuellas':24,'altura':.175,'huella_nominal':.28,'ancho_nominal':1.2,'rellano_intermedio':2.1};stat['galeria_m2']=round(upper.area,2)
  stat['seguridad_pendiente']='Seccion de altura, evacuacion, accesibilidad normativa, uniones, pandeo y cimentacion. Los troncos no se calculan en esta entrega.'

  context=json.loads((P/'fuentes/CONTEXTO_CATASTRAL.geojson').read_text());ox,oy=S['origen_utm']
  for j,feat in enumerate(context['features']):
   g=translate(shape(feat['geometry']),-ox,-oy)
   if not g.intersects(box(-5,-20,80,23)):continue
   floors=feat['properties'].get('plantas_sr',0)
   try:h=max(.4,float(floors)*3.1)
   except:h=9.3
   solid(g,-.65,h,'90_CONTEXTO','Altura hipotetica plantas Catastro x3.1m',True)
 # Named views; complete and cutaway files use the same built geometry.
 bounds=Tr(f['floor']).bounds;x,y,X0,Y=bounds;cx=(x+X0)/2;cy=(y+Y)/2;span=max(X0-x,Y-y)
 for name,loc,tgt in [('01_INTERIOR_AXO',(cx+span*.8,cy-span,span*.80),(cx,cy,5.2 if site else 1)),('02_PLANTA',(cx,cy,span*2),(cx,cy,0)),('03_FACHADA',(cx,cy-span*2,3),(cx,cy,1.5))]:
  view=rh.ViewInfo();view.Name=name;vp=view.Viewport;vp.SetCameraLocation(rh.Point3d(*loc));vp.SetCameraDirection(rh.Vector3d(*(tgt[i]-loc[i] for i in range(3))));vp.SetCameraUp(rh.Vector3d(0,1,0) if name=='02_PLANTA' else rh.Vector3d(0,0,1));vp.TargetPoint=rh.Point3d(*tgt);vp.ChangeToParallelProjection(True);vp.Extents(.3,rh.BoundingBox(rh.Point3d(x-.8,y-.8,-.6),rh.Point3d(X0+.8,Y+.8,9.4 if site else 4.9)));m.NamedViews.Add(view)
 for k in ['90_CONTEXTO']:m.Layers[layers[k]].Visible=False
 m.Strings['Descripcion']='Modelo 3D de estudio, suelo Z=0, sin apilar. Soporte, luz y telas exploratorios; los calculos antiguos no validan esta geometria nueva.'
 full=P/'modelos'/(code+'.3dm');assert m.Write(str(full),8)
 for k in TOP:m.Layers[layers[k]].Visible=False
 interior=P/'modelos'/(code+'_INTERIOR.3dm');assert m.Write(str(interior),8)
 chk=rh.File3dm.Read(str(full));assert all(o.Geometry.IsValid for o in chk.Objects)
 stat.update(objetos=len(chk.Objects),invalidos=0,suelo_m2=round(f['floor'].area,2),archivo=str(full),interior=str(interior),soportes_borde=len(supports),huella_local=list(bounds),entrada=f['entry'],modelos_originales_modificados=False)
 stat['entrada']={k:(list(v) if isinstance(v,tuple) else v.wkt) for k,v in stat['entrada'].items()}
 allreport.append(stat);(P/'fuentes'/(code+'_render.json')).write_text(json.dumps({'objects':cache,'bounds':([min(bounds[0],44),min(bounds[1],-6.7),max(bounds[2],52.3),max(bounds[3],9)] if site else bounds),'site':site,'colors':COL,'code':code},separators=(',',':')))
 print(code,len(chk.Objects),stat.get('paso_exterior90'),flush=True)
 return m,cache,stat

if '--site-only' not in sys.argv:
 for f in G.F:build(f,f['audit']['codigo']+'_3D',kind=2 if f['audit']['codigo']=='V02_P' else 0)
for code,base,kind in [('E01_ENCUENTRO','V01_D',0),('E02_COMUNA','V01_S',1),('E03_DOS_CLAROS','V02_P',2)]:
 f=next(f for f in G.F if f['audit']['codigo']==base);build(f,code,True,kind)
(P/'verificacion/GEOMETRIA_3D.json').write_text(json.dumps(allreport,ensure_ascii=False,indent=2))
