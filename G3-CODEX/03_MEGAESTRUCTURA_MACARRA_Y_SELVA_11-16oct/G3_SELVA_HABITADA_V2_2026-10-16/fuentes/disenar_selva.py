from pathlib import Path
import json, math, copy
import numpy as np
import rhino3dm as r
from shapely.geometry import Polygon, box, LineString, shape
from shapely.ops import triangulate, unary_union
from shapely.affinity import translate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch, Rectangle, Arc
from matplotlib.collections import PolyCollection, LineCollection
R=Path(__file__).resolve().parents[1];V=R/'vistas';M=R/'modelos';Q=R/'verificacion'
SRC=R/'fuentes'/'geometria'
site=shape(json.loads((SRC/'parcela_local.geojson').read_text())['geometry'])
C={'suelo':'#d9cfad','estructura':'#e2e3cd','borde':'#dfba28','piel':'#a8b1a0','vidrio':'#bad7c7','tecnico':'#be2776','agua':'#269baf','interior':'#ede7d6','mueble':'#b47c51','nucleo':'#808d8c','parcela':'#a39989','contexto':'#c4c1b8','membrana':'#93b7a4','traccion':'#8b8d82'}
def rgb(h):return tuple(int(h[i:i+2],16) for i in (1,3,5))
def parts(g):return [g] if g.geom_type=='Polygon' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']
class Model:
 def __init__(self):self.items=[]
 def mesh(self,v,f,layer,name):
  if len(f):self.items.append(dict(v=np.asarray(v,float).tolist(),f=[[int(i) for i in a] for a in f],layer=layer,name=name))
 def prism(self,p,z,h,layer,name):
  for poly in parts(p):
   if poly.area<1e-7:continue
   vs=[];fs=[]
   def face(pts):
    k=len(vs);vs.extend(pts);fs.append(list(range(k,k+len(pts))))
   for t in triangulate(poly):
    if not poly.covers(t.representative_point()):continue
    pts=list(t.exterior.coords)[:-1];face([(x,y,z) for x,y in reversed(pts)]);face([(x,y,z+h) for x,y in pts])
   for ring in [poly.exterior]+list(poly.interiors):
    pp=list(ring.coords)
    for a,b in zip(pp,pp[1:]):face([(a[0],a[1],z),(b[0],b[1],z),(b[0],b[1],z+h),(a[0],a[1],z+h)])
   self.mesh(vs,fs,layer,name)
 def rect(self,x,y,w,d,z,h,layer,name):self.prism(box(x,y,x+w,y+d),z,h,layer,name)
 def rod(self,a,b,rad,layer,name,n=8):
  a=np.array(a,float);b=np.array(b,float);d=b-a
  if np.linalg.norm(d)<1e-6:return
  d/=np.linalg.norm(d);u=np.cross(d,[0,0,1] if abs(d[2])<.95 else [0,1,0]);u/=np.linalg.norm(u);vv=np.cross(d,u)
  vs=[p+rad*(math.cos(t)*u+math.sin(t)*vv) for p in [a,b] for t in np.linspace(0,2*math.pi,n,endpoint=False)]
  ff=[[i,(i+1)%n,(i+1)%n+n,i+n] for i in range(n)]
  for i in range(1,n-1):ff.extend([[0,i+1,i],[n,n+i,n+i+1]])
  self.mesh(vs,ff,layer,name)
 def chain(self,pts,rad,layer,name):
  for a,b in zip(pts,pts[1:]):self.rod(a,b,rad,layer,name)
 def add(self,other,x,y,z,prefix):
  for it in other.items:
   a=copy.deepcopy(it);a['v']=(np.array(a['v'])+[x,y,z]).tolist();a['name']=prefix+' '+a['name'];self.items.append(a)
 def save(self,name,context=False):
  doc=r.File3dm();doc.Settings.ModelUnitSystem=r.UnitSystem.Meters;layers={}
  for k,c in C.items():
   la=r.Layer();la.Name=k;la.Color=(*rgb(c),255);layers[k]=doc.Layers.Add(la)
  for it in self.items:
   me=r.Mesh()
   for v in it['v']:me.Vertices.Add(*v)
   for f in it['f']:
    if len(f)==3:me.Faces.AddFace(*f)
    elif len(f)==4:me.Faces.AddFace(*f)
    else:
     for j in range(1,len(f)-1):me.Faces.AddFace(f[0],f[j],f[j+1])
   me.Faces.CullDegenerateFaces();me.Normals.ComputeNormals();at=r.ObjectAttributes();at.LayerIndex=layers[it['layer']];at.Name=it['name'];doc.Objects.AddMesh(me,at)
  doc.Write(str(M/(name+'.3dm')),8)
  (M/(name+'.json')).write_text(json.dumps(self.items,separators=(',',':')))
  return len(doc.Objects)

def roundbox(x,y,w,h,rad=.32):return box(x+rad,y+rad,x+w-rad,y+h-rad).buffer(rad,quad_segs=5)
# Four own rooms, two wet rooms, a shared centre and an internal cross passage.
rooms=[roundbox(0,0,3.7,3.8,.55),roundbox(7.6,0,3.7,3.8,.55),roundbox(0,5.4,3.7,3.8,.55),roundbox(7.6,5.4,3.7,3.8,.55)]
wet=[box(3.7,0,5.65,2.6),box(5.65,0,7.6,2.6)]
common=box(3.7,2.6,7.6,9.2);passages=[box(0,3.8,3.7,5.4),box(7.6,3.8,11.3,5.4)]
unit=Model();foot=unary_union(rooms+wet+[common]+passages)
unit.prism(foot,-.25,.25,'suelo','U4 bandeja 102.86 m2 brutos')
for x in [0.15,3.7,7.6,11.15]:unit.rod([x,.15,-.45],[x,9.05,-.45],.11,'borde','Viga de bandeja seccion por calcular')
for y in [.15,4.6,9.05]:unit.rod([.15,y,-.45],[11.15,y,-.45],.12,'borde','Viga de borde')
for i,p in enumerate(rooms):
 x0,y0,x1,y1=p.bounds;lower=i<2;dy=(y1-.2 if lower else y0-.05)
 opening=box(x0+1.4,dy,x0+2.4,dy+.3)
 window=box(x0+.6,y0-.1 if lower else y1-.2,x1-.6,y0+.2 if lower else y1+.1)
 wall=p.difference(p.buffer(-.12)).difference(opening).difference(window)
 unit.prism(wall,0,2.7,'piel',f'H{i+1} cerramiento y puerta 1.0 m')
 # windows with opaque parapet; no glass facade facing a party wall is assumed validated.
 wp=p.difference(p.buffer(-.12)).intersection(window)
 unit.prism(wp,0,.85,'piel',f'H{i+1} antepecho');unit.prism(wp,.85,1.8,'vidrio',f'H{i+1} ventana a vacio propio por comprobar')
 # door leaf indicated open into the own room; head above passage.
 unit.rect(x0+1.4,(y1-1.1 if lower else y0+.12),.05,1,0,2.1,'interior',f'H{i+1} hoja abierta')
 unit.prism(p,2.7,.12,'piel',f'H{i+1} cubierta termica')
 unit.rect(x0+.27,y0+.3,1.1,2.0,0,.42,'mueble',f'H{i+1} cama 1.10 x 2.00')
 unit.rect(x0+2.78,y0+(1.2 if lower else .27),.65,2.1,0,2.3,'interior',f'H{i+1} armario')
 unit.rect(x0+(1.6 if lower else .35),y0+(.3 if lower else 2.8),1.4,.6,.73,.06,'mueble',f'H{i+1} mesa 1.40 x 0.60')
for i,p in enumerate(wet):
 x0,y0,x1,y1=p.bounds;op=box(x0+.45,2.4,x0+1.4,2.7)
 unit.prism(p.difference(p.buffer(-.1)).difference(op),0,2.5,'interior',f'B{i+1} aseo ducha 5.07 brutos')
 unit.rect(x0+.13,.13,.9,.9,.01,.08,'agua',f'B{i+1} ducha')
 unit.rect(x0+1.05,.18,.48,.68,.0,.43,'interior',f'B{i+1} WC')
 unit.rect(x0+.15,1.45,.55,.45,.8,.1,'agua',f'B{i+1} lavabo')
unit.rect(3.9,8.4,3.5,.65,0,.9,'tecnico','Cocina al fondo libera umbral transversal')
unit.rect(5.15,5.55,1.0,1.8,.75,.06,'mueble','Mesa cuatro personas')
for y in [5.7,6.7]:
 for x in [4.6,6.4]:unit.rect(x,y,.43,.43,0,.45,'interior','Silla')
unit.rect(6.8,2.85,.6,.75,0,.42,'interior','Banco estar fuera del paso')
# Curved outer ribs around the private refuges: geometric rather than decorative cables.
for i,p in enumerate(rooms):
 cx,cy=p.centroid.x,p.centroid.y
 for t in np.linspace(0,1,10,endpoint=False):
  ep=p.exterior.interpolate(t,normalized=True)
  dx,dy=ep.x-cx,ep.y-cy;ln=math.hypot(dx,dy)
  ex,ey=ep.x+.03*dx/ln,ep.y+.03*dy/ln
  pts=[[cx+.35*dx,cy+.35*dy,-.72],[cx+.8*dx,cy+.8*dy,-.45],[ex,ey,-.2],[ex,ey,0],[ex,ey,2.96]]
  unit.chain(pts,.026,'estructura','Costilla por exterior; intrados bajo bandeja')
# Centre weather shell and curved exoskeleton, with two independent doors on west/east.
for x in [3.7,7.6]:
 for y0,y1 in [(2.6,3.8),(5.4,9.2)]:unit.rect(x-.04,y0,.08,y1-y0,0,2.7,'vidrio','Piel centro comun')
unit.rect(3.7,9.1,3.9,.1,0,2.7,'vidrio','Centro comun frente abierto al vacio')
for y in [2.65,4.6,6.7,9.1]:
 pts=[[3.7+3.9*t,y,2.75+.5*math.sin(math.pi*t)] for t in np.linspace(0,1,17)]
 unit.chain(pts,.045,'estructura','Costilla curva de cubierta comun')
for x in [.1,3.55,7.75,11.2]:
 pts=[[x,9.0*t,2.72+.28*math.sin(math.pi*t)] for t in np.linspace(0,1,15)]
 unit.chain(pts,.038,'estructura','Costilla de proteccion sustituible')
verts=[[3.7+3.9*t,y,2.77+.5*math.sin(math.pi*t)] for y in [2.6,9.2] for t in np.linspace(0,1,17)]
unit.mesh(verts,[[i,i+1,i+18,i+17] for i in range(16)],'membrana','Cubierta comun curva; membrana exterior no sustituye envolvente')
unit.chain([[5.65,.0,-.42],[5.65,2.6,-.42],[5.65,8.7,-.42]],.065,'agua','Reserva drenaje pendiente y diametro por calcular')
unit.save('01_UNIDAD_U4')

macro=Model();macro.prism(site,-.25,.25,'parcela','Parcela de archivo 650.913 m2 datum simplificado')
levels=[4.2,8.4,12.6,16.8,21.0];records=[];galeries=[];program=[]
cores=[box(14,-6.8,18.8,-1.0),box(54,-5.0,58.8,.8)]
# Two separate service/stair supports, no single inhabited sidewall.
for ci,p in enumerate(cores):
 x,y,x1,y1=p.bounds
 for z in [0]+levels:
  macro.prism(p.difference(box(x+.15,y+1.15,x+2.65,y+5.7)),z-.2,.2,'nucleo',f'N{ci+1} meseta con hueco de escalera')
  macro.rect(x+2.8,y+.2,1.8,1.9,z,3.2,'agua',f'N{ci+1} ascensor reserva sin cabina verificada')
  for xx,yy in [(x,y),(x1,y),(x,y1),(x1,y1)]:macro.rod([xx,yy,z],[xx,yy,z+4.2],.11,'estructura',f'N{ci+1} montante')
 for k,z in enumerate([0]+levels[:-1]):
  rise=levels[k]-z;ns=24;nh=ns//2;rr=rise/ns
  for j in range(nh):
   macro.rect(x+.2,y+1.15+j*.28,1.1,.29,z+j*rr,.12,'borde',f'N{ci+1} tramo A')
   macro.rect(x+1.45,y+1.15+(nh-1-j)*.28,1.1,.29,z+rise/2+j*rr,.12,'borde',f'N{ci+1} tramo B')
  macro.rect(x+.2,y+1.15+nh*.28,2.35,1.1,z+rise/2-.15,.15,'borde',f'N{ci+1} meseta intermedia')
for k,z in enumerate(levels):
 placements=[(19.8,[-3.4,-2.8,-4.6,-3,-4.2][k]),([32,32.15,31.5,32.1,31.8][k],-5)]
 main=LineString([(18.8,-1.9),(19,-6),(43.9,-6),(45.6,-4.5),(54.0,-4.5)]).buffer(.9,cap_style=2,join_style=2)
 connectors=[]
 for j,(x,y) in enumerate(placements):
  tag=f'U{k*2+j+1:02}';macro.add(unit,x,y,z,tag)
  pp=translate(foot,xoff=x,yoff=y)
  # Entry through a lateral vestibule onto the cross-passage; nobody traverses a bedroom.
  ex,ey=(x,y+4.6) if j==0 else (x+11.3,y+4.6)
  path=LineString([(19,-6),(19,ey),(ex,ey)]) if j==0 else LineString([(45.6,-4.5),(45.6,ey),(ex,ey)])
  connectors.append(path.buffer(.8,cap_style=2,join_style=2).difference(pp))
  records.append({'id':tag,'x':x,'y':y,'z':z,'personas':4,'m2_brutos':pp.area,'fuera_parcela':pp.difference(site).area,'puerta':[ex,ey,z]})
  # Tree branches beneath the deck, repeated at each floor, joining distributed trunks.
  for ax,ay in [(20,-4.6),(31.25,-3.7),(43.8,-1.8)]:
   if x-.5<=ax<=x+11.8:
    for bx,by in [(x+.2,y+.2),(x+11.1,y+9)]:
     macro.rod([ax,ay,z-.85],[bx,by,z-.48],.08,'estructura',tag+' rama soporte - dimensionar')
  for xx,yy in [(x+.12,y+.12),(x+11.18,y+9.08)]:
   macro.rod([xx,yy,z-.4],[xx,yy,z+3.15],.027,'traccion',tag+' tirante a marco superior; verificar anclajes')
 deck=unary_union([main]+connectors).intersection(site)
 # Remove private footprints from public gallery; record independent geometry.
 for x,y in placements:deck=deck.difference(translate(foot,xoff=x,yoff=y))
 galeries.append((z,deck));macro.prism(deck,z-.17,.17,'borde',f'G{k+1} galeria y ramales nominal 1.8 / 1.6 m')
 # open-side handrail concept, interrupted at entrance neighborhoods
 for poly in parts(deck):
  coords=list(poly.exterior.coords)
  for a,b in zip(coords,coords[1:]):
   ln=LineString([a,b]);mid=ln.interpolate(.5,normalized=True)
   if any(translate(foot,xoff=x,yoff=y).distance(mid)<.12 for x,y in placements):continue
   macro.rod([*a,z+1.1],[*b,z+1.1],.023,'estructura','Barandilla conceptual sin certificacion')
   for t in np.arange(0,ln.length,1.2):
    pp=ln.interpolate(t);macro.rod([pp.x,pp.y,z],[pp.x,pp.y,z+1.1],.02,'estructura','Montante barandilla')
# Main trunks start at real ground, not dangling roots; loads must still be calculated.
for x,y in [(20,-4.6),(31.25,-3.7),(43.8,-1.8),(24.5,7.4)]:
 macro.chain([[x,y,0],[x+.25,y+.15,7.3],[x-.15,y-.1,14.5],[x,y,25.1]],.19,'estructura','Tronco principal marfil apoyado en suelo')
 macro.chain([[x+.3,y,0],[x+.55,y+.15,7.3],[x+.15,y-.1,14.5],[x+.3,y,25.1]],.055,'tecnico','Montante de servicios visible con registros por desarrollar')
# Usable collective programs, elevated commerce, ground entry free of retail.
program_specs=[('Acogida y cuidados',box(33,-4.8,39,-1.0),0),('Lavanderia y limpieza',box(40,-4.8,45,-.8),0),('Tecnica y almacen',box(46,-3.5,51,1),0),('Cantina y reparto',box(46,-3.5,53.4,2.0),4.2),('Taller y herramientas',box(46,-3.5,53.4,2.0),12.6),('Cowork y aula',box(46,-3.5,53.4,2.0),21.0)]
for name,p,z in program_specs:
 macro.prism(p,z-.2,.2,'suelo',name+' suelo');x0,y0,x1,y1=p.bounds
 macro.prism(p.difference(p.buffer(-.12)).difference(box(x0+.8,y0-.2,x0+2.0,y0+.2)),z,2.7,'vidrio',name+' cerramiento esquematico')
 macro.prism(p,z+2.7,.15,'membrana',name+' cubierta')
 program.append({'nombre':name,'z':z,'m2_brutos':p.area})
 for y in np.arange(y0+1,y1-1,1.8):macro.rect(x0+2,y,3,.75,z+.75,.08,'mueble',name+' mesa de ensayo')
# Open public assembly terrace in the wider wedge, only where not conflicting with units.
terr=box(21.5,6.7,27.5,9.0).intersection(site)
macro.prism(terr,8.23,.17,'borde','Claro abierto para reunion en cota 8.4')
# Connect its south side to west vestibule without passing through the group.
extra=LineString([(19,1.8),(19,8),(21.5,8)]).buffer(.8,cap_style=2).intersection(site)
macro.prism(extra,8.23,.17,'borde','Ramal del claro');galeries[1]=(8.4,unary_union([galeries[1][1],extra,terr]))
# Top sail field: asymmetric but anchored, inside parcel, no uniform mega-umbrella.
for x,y,w,d in [(19.8,-4.2,11.3,9.2),(31.8,-5,11.3,9.2),(46,-3.5,7.4,5.5),(21.5,6.7,6,2.3)]:
 z=24.4 if x!=21.5 else 11.3
 vv=[[x,y,z],[x+w,y,z+.7],[x+w,y+d,z],[x,y+d,z+1.2]]
 macro.mesh(vv,[[0,1,2],[0,2,3]],'membrana','Vela colectiva exterior; desague en esquinas bajas')
 for a,b in [(0,1),(1,2),(2,3),(3,0),(0,2)]:macro.rod(vv[a],vv[b],.04,'estructura','Borde tensado')
 for v in vv:macro.rod([v[0],v[1],v[2]-.9],v,.035,'traccion','Puntal y amarre de vela')
# ground approach remains a real path from street; the rear is not an invented street exit.
approach=LineString([(12.8,0),(19,0),(19,-6),(43.9,-6),(45.6,-4.5),(54,-4.5)]).buffer(.9,cap_style=2).intersection(site)
macro.prism(approach,0,.015,'borde','Entrada y recorrido en suelo; sin comercio en umbral')
# context retained in independent layer from existing triangle cache
ct=np.load(SRC/'contexto.npz');tri=ct['tri'];ids=ct['ids']
for id in sorted(set(ids)):
 ts=tri[ids==id];center=ts.reshape(-1,3).mean(axis=0)
 if -8<center[0]<78 and -28<center[1]<35:
  vv=ts.reshape(-1,3);macro.mesh(vv,np.arange(len(vv)).reshape(-1,3),'contexto','Vecino '+id+' malla original')
n=macro.save('02_SELVA_EN_PARCELA')
# measurable checks, explicitly limited to footprints and program.
pairs=[]
for k in range(5):
 a,b=records[2*k:2*k+2];pairs.append(translate(foot,xoff=a['x'],yoff=a['y']).intersection(translate(foot,xoff=b['x'],yoff=b['y'])).area)
areas={'unidad_bruta':foot.area,'habitacion_util_aprox':rooms[0].buffer(-.12).area,'comun_central_bruto':common.area,'aseos_brutos':sum(p.area for p in wet),'pasajes_internos_brutos':sum(p.area for p in passages),'unidades_total':sum(a['m2_brutos'] for a in records),'nucleos_reserva_total':sum(p.area for p in cores)*6,'programa_comunitario':sum(p['m2_brutos'] for p in program),'galerias_y_claros_abiertos':sum(p.area for z,p in galeries)}
areas['cerrado_y_nucleos_estudio']=areas['unidades_total']+areas['nucleos_reserva_total']+areas['programa_comunitario']
audit={'version':'v2 16 octubre 2026: cocina al fondo, paso libre, costillas exteriores, huecos de escalera; no proyecto de ejecucion','parcela_m2':site.area,'residentes':40,'unidades':10,'niveles':levels,'coronacion_velas':25.6,'area_fuera_unidades_m2':sum(a['fuera_parcela'] for a in records),'solapes_entre_unidades_por_nivel_m2':pairs,'areas_m2':areas,'modelo_objetos':n,'no_verificado':['estructura y anclajes','fuego y compartimentacion','itinerario accesible completo y aseos','luz y ventilacion entre vecinos','cota real de calle','envolvente energetica','viabilidad urbanistica de altura y edificabilidad','interferencias tridimensionales completas'],'unidades_datos':records,'programa':program}
(Q/'comprobacion.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in audit.items() if k not in ['unidades_datos','no_verificado']},ensure_ascii=False,indent=2))
# Drawings from exact generated geometry, separate from AI imagery.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
BG='#f5f2e9';INK='#25342f'
def base(title,subtitle,size=(16,10)):
 fig,ax=plt.subplots(figsize=size);fig.patch.set_facecolor(BG);ax.set_facecolor(BG);fig.suptitle(title,x=.06,y=.96,ha='left',fontsize=23,fontweight='bold',color=INK);fig.text(.06,.9,subtitle,fontsize=11,color=INK);return fig,ax
def poly(ax,p,fill,alpha=1,lw=.7):
 for pp in parts(p):ax.add_patch(Patch(np.array(pp.exterior.coords),facecolor=fill,edgecolor=INK,linewidth=lw,alpha=alpha))
def end(fig,ax,name):
 ax.set_aspect('equal');ax.axis('off');fig.savefig(V/(name+'.png'),dpi=160,facecolor=BG,bbox_inches='tight');fig.savefig(V/(name+'.svg'),facecolor=BG,bbox_inches='tight');plt.close(fig)
fig,ax=base('U4 / cuatro refugios alrededor de una casa comun','PLANTA DE ENSAYO · medidas en metros · ninguna circulacion general atraviesa las habitaciones')
for i,p in enumerate(rooms):
 poly(ax,p,C['piel']);x,y,x1,y1=p.bounds;ax.text(x+2.0,y+1.85,f'H{i+1}\n12.1 m² utiles\naprox.',ha='center',va='center',fontsize=10)
 poly(ax,box(x+.27,y+.3,x+1.37,y+2.3),C['mueble']);poly(ax,box(x+2.78,y+(1.2 if i<2 else .27),x+3.43,y+(3.3 if i<2 else 2.37)),C['interior']);poly(ax,box(x+(1.6 if i<2 else .35),y+(.3 if i<2 else 2.8),x+(3.0 if i<2 else 1.75),y+(.9 if i<2 else 3.4)),C['mueble'])
for p in wet:poly(ax,p,C['agua']);ax.text(p.centroid.x,1.3,'DUCHA\nASEO',ha='center',fontsize=9)
poly(ax,common,'#d9ddbe');ax.text(5.65,4.55,'COCINAR\nESTAR\nCOMER',ha='center',va='center',fontsize=11)
for p in passages:poly(ax,p,'#e3c849');ax.arrow(p.bounds[0]+.15,4.6,p.bounds[2]-p.bounds[0]-.3,0,head_width=.13,length_includes_head=True,color=INK)
poly(ax,box(3.9,8.4,7.4,9.05),C['tecnico']);poly(ax,box(5.15,5.55,6.15,7.35),C['mueble']);poly(ax,box(6.8,2.85,7.4,3.6),C['interior'])
# Clear door gaps and swinging leaf arcs.
for i,p in enumerate(rooms):
 x0,y0,x1,y1=p.bounds;yy=y1 if i<2 else y0
 ax.plot([x0+1.4,x0+2.4],[yy,yy],color=BG,lw=4)
 ax.plot([x0+1.4,x0+1.4],[yy,yy+(-1 if i<2 else 1)],color=INK,lw=.8)
 ax.add_patch(Arc((x0+1.4,yy),2,2,theta1=270 if i<2 else 0,theta2=360 if i<2 else 90,color=INK,lw=.6))
for p in wet:
 x0,y0,x1,y1=p.bounds
 ax.plot([x0+.45,x0+1.4],[2.6,2.6],color=BG,lw=4)
 poly(ax,box(x0+.13,.13,x0+1.03,1.03),'#e5eded',lw=.5)
 poly(ax,box(x0+1.05,.18,x0+1.53,.86),'#e5eded',lw=.5)
for x in [4.65,6.4]:
 for y in [5.7,6.7]:poly(ax,box(x,y,x+.43,y+.43),C['interior'],lw=.4)
ax.plot([0,11.3],[4.6,4.6],color=INK,lw=.8,linestyle='--')
ax.text(-.35,4.6,'UMBRAL\n1.60 m',ha='right',va='center');ax.text(11.65,4.6,'ENLACE\nPOSIBLE',ha='left',va='center')
ax.annotate('',(0,-.65),(11.3,-.65),arrowprops={'arrowstyle':'|-|','color':INK});ax.text(5.65,-.95,'11.30 m',ha='center');ax.annotate('',(-.65,0),(-.65,9.2),arrowprops={'arrowstyle':'|-|','color':INK});ax.text(-.9,7.1,'9.20 m',rotation=90)
ax.text(0,10.1,'102.86 m² brutos aprox. / 4 personas / 2 aseos / centro comun 25.74 m² brutos',fontsize=11)
ax.set_xlim(-2,14);ax.set_ylim(-1.5,11);end(fig,ax,'01_UNIDAD_PLANTA')
fig,ax=base('La parcela manda la transformacion','HUELLA DOCUMENTADA · 650.91 m² · se conservan los linderos; no se inventa una salida trasera',(17,8))
for id in sorted(set(ids)):
 ts=tri[ids==id];ps=[Polygon(t[:,:2]) for t in ts if Polygon(t[:,:2]).area>.1]
 if ps:poly(ax,unary_union(ps),'#d9d6cd',.65,.3)
poly(ax,site,'#f5eddb');z,deck=galeries[0];poly(ax,deck,C['borde'])
for p in cores:poly(ax,p,C['nucleo']);ax.text(p.centroid.x,p.centroid.y,'ESC\nASC',ha='center',va='center',fontsize=8)
for rec in records[:2]:
 poly(ax,translate(foot,xoff=rec['x'],yoff=rec['y']),C['piel']);ax.text(rec['x']+5.65,rec['y']+4.6,rec['id']+' / 4',ha='center',va='center')
for name,p,zz in program_specs:
 if zz==4.2:poly(ax,p,C['tecnico']);ax.text(p.centroid.x,p.centroid.y,'CANTINA\nREPARTO',ha='center',fontsize=8)
ax.text(8,-1,'RIBERA DE\nCURTIDORES',rotation=90,ha='center',va='center');ax.annotate('entrada residencial',(13,0),(7,9),arrowprops={'arrowstyle':'->'},fontsize=10)
ax.plot([14,24],[-11,-11],color=INK,lw=3);ax.text(19,-12,'10 m',ha='center');ax.set_xlim(5,65);ax.set_ylim(-13,16);end(fig,ax,'02_PARCELA_IMPLANTACION')
fig,ax=base('De objeto enorme a vecindario que cabe','COMPARACION DE ENVOLVENTES · mismos metros · el edificio se recompone; no se miniaturizan personas ni peldaños',(16,8))
poly(ax,box(0,0,90.274,66.466),'#d8d9d0');poly(ax,box(100,0,149.48,25.6),'#afbeb0')
ax.text(45,69,'ORIGINAL / 90.27 × 61.27 × 66.47 m',ha='center',fontsize=11);ax.text(124.7,27,'V2 / parcela 49.48 m de fondo\nvelas hasta +25.60 m',ha='center',fontsize=11)
ax.text(45,32,'28 plataformas\n36 enlaces\n903 peldaños',ha='center',fontsize=16);ax.text(124.7,11,'10 U4 / 40 personas\n5 cotas de acceso',ha='center',fontsize=13)
ax.text(0,-8,'Escalar a 0.22 para acercarse al ancho estrecho dejaria los pasos originales de 1.81–2.57 m en solo 0.40–0.57 m.',fontsize=10)
ax.set_xlim(-2,154);ax.set_ylim(-12,75);end(fig,ax,'03_CAMBIO_ESCALA')
# Axonometric mesh projection: camera depth sorted, faithful geometry.
def axon(model,name,title,eye=(1,-1,.9),exclude=(),lim=None):
 E=np.array(eye,float);E/=np.linalg.norm(E);U=np.cross([0,0,1],E);U/=np.linalg.norm(U);UP=np.cross(E,U)
 polys=[];cols=[];dep=[]
 for it in model.items:
  if it['layer'] in exclude:continue
  vv=np.array(it['v']);cc=np.array(rgb(C[it['layer']]))/255
  for f in it['f']:
   pts=vv[f];normal=np.cross(pts[1]-pts[0],pts[2]-pts[0]);norm=np.linalg.norm(normal)
   if norm<1e-8:continue
   shade=.7+.3*abs(np.dot(normal/norm,np.array([.2,-.4,.9])))
   polys.append(np.column_stack([pts@U,pts@UP]));cols.append(np.clip(cc*shade,0,1));dep.append(pts.mean(axis=0)@E)
 order=np.argsort(dep);fig,ax=base(title,'PROYECCION DEL MODELO EDITABLE · geometria de ensayo, sin alteracion generativa',(16,11))
 ax.add_collection(PolyCollection([polys[i] for i in order],facecolors=[cols[i] for i in order],edgecolors='none'))
 allp=np.vstack(polys);a=allp.min(axis=0);b=allp.max(axis=0);ax.set_xlim(a[0]-1,b[0]+1);ax.set_ylim(a[1]-1,b[1]+1)
 if lim:ax.set_xlim(*lim[0]);ax.set_ylim(*lim[1])
 end(fig,ax,name)
# Own-room roofs omitted solely for cutaway visual.
cut=Model();cut.items=[a for a in unit.items if 'cubierta termica' not in a['name'] and a['layer']!='membrana']
axon(cut,'04_UNIDAD_AXONOMETRIA','Una unidad contiene ya un vecindario',eye=(1,-1,1.1))
axon(macro,'05_CONJUNTO_GEOMETRIA','Selva habitada / geometria de control v2',eye=(1,-1,.9),exclude=('contexto',))
# Context side roofs can obscure the object; separate honest context projection.
axon(macro,'06_CONTEXTO_GEOMETRIA','La selva dentro de la manzana',eye=(1,-1,1.8))
