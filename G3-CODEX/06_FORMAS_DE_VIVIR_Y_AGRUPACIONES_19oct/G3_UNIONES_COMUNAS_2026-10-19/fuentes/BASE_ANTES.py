from pathlib import Path
import math,json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch,Arc
from shapely.geometry import Point,Polygon,LineString,box
from shapely.affinity import rotate,translate
from shapely.ops import unary_union,nearest_points
import rhino3dm as rh
P=Path(__file__).resolve().parents[1]
C={'floor':'#eee8da','private':'#d8e1d1','wall':'#465c51','bed':'#c3a783','desk':'#b47c56','ward':'#779486','seat':'#c07196','glass':'#299a9d','bath':'#a0b7bf','route':'#b54651'}
def rounded(x,y,X,Y,r=.18):return box(x+r,y+r,X-r,Y-r).buffer(r,quad_segs=16)
base=rounded(0,0,3.35,4.3,.18)
vest=Point(3.25,3.1).buffer(1.45,quad_segs=48).intersection(box(3.15,1.5,5,4.7))
bay=rounded(.55,4.1,3.15,5.5,.18)
ROOM=unary_union([base,vest,bay]).buffer(.10).buffer(-.10)
WARD=Point(3.25,3.1).buffer(1.45,quad_segs=48).difference(Point(3.25,3.1).buffer(.90,quad_segs=48)).intersection(box(3.25,1.5,5,4.7))
BED=box(.25,2.15,1.50,4.15);DESK=box(.025,.25,1.825,1.15);STOOL=Point(.95,1.65).buffer(.23)
SEAT=rounded(.65,4.35,1.95,5.35,.1)
DOOR=box(2.10,-.20,3.10,.20);WIN=box(.80,5.36,2.90,5.62)
FURN={'cama':BED,'mesa_A1':DESK,'ropa':WARD,'rincon_ventana':SEAT,'taburete_en_uso':STOOL}
TARGETS={'entrada':(2.6,.65),'junto_cama':(2.2,3.0),'vestidor':(3.65,3.1),'ventana':(2.55,4.8),'dibujar':(.95,1.65)}
def tf(g,r):return translate(rotate(translate(g,-2.6,0),r['phi'],origin=(0,0)),*r['q'])
def rr(q,phi):return {'q':q,'phi':phi}
def draw(ax,g,c,ec='none',lw=.5,alpha=1):
 if g.is_empty:return
 if g.geom_type=='Polygon':ps=[g]
 else:ps=[p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']
 for p in ps:
  ax.add_patch(Patch(np.array(p.exterior.coords),facecolor=c,edgecolor=ec,lw=lw,alpha=alpha))
  for h in p.interiors:ax.add_patch(Patch(np.array(h.coords),facecolor='#faf8f2',edgecolor=ec,lw=lw))
def line(ax,g,c,lw=1,ls='-'):
 if g.is_empty:return
 for l in ([g] if g.geom_type=='LineString' else getattr(g,'geoms',[])):
  if l.geom_type=='LineString':x,y=l.xy;ax.plot(x,y,color=c,lw=lw,ls=ls)
def txt(ax,x,y,t,size=8,c='#263d35',ha='center'):ax.text(x,y,t,fontsize=size,color=c,ha=ha,va='center')
def private(ax,r,labels=True):
 draw(ax,tf(ROOM,r),C['private'])
 for k,g in FURN.items():draw(ax,tf(g,r),C['ward'] if k=='ropa' else C['bed'] if k=='cama' else C['seat'] if k=='rincon_ventana' else C['desk'],ec='#687566',lw=.35)
 draw(ax,tf(WIN,r),C['glass'])
 # Open sliding door parked to left of its straight opening.
 draw(ax,tf(box(1.05,.015,2.05,.055),r),C['desk'])
 if labels:
  for x,y,t in [(2.45,2.05,'dormir'),(3.66,3.1,'vestirse'),(2.52,4.65,'mirar\nfuera')]:
   p=tf(Point(x,y),r);txt(ax,p.x,p.y,t,6)
 # Proposed outside textile rail around front of the bay, not a drying line.
 line(ax,tf(LineString([(.65,5.73),(3.15,5.73)]),r),C['seat'],1.6,'--')

def family(code,name,core,rooms,baths,kitchen,table,sofa,entry,hyp,links):
 core=core.union(unary_union(baths).buffer(.08,join_style=2))
 privatepolys=[tf(ROOM,r) for r in rooms];floor=unary_union([core]+privatepolys)
 # No fillet that changes the private programme: common shape is already round.
 walls=unary_union([p.boundary.buffer(.06) for p in privatepolys]+[floor.boundary.buffer(.06)])
 doors=unary_union([tf(DOOR,r) for r in rooms]+[entry['cut']])
 # Bath doors on their south edge, parking outside the clear opening.
 bd=[]
 for b in baths:
  x,y,X,Y=b.bounds;bd.append(box(x+.65,y-.15,x+1.60,y+.15));walls=walls.union(b.boundary.buffer(.06))
 doors=doors.union(unary_union(bd))
 wins=unary_union([tf(WIN,r) for r in rooms])
 # Common glazing candidates are explicitly cut at exposed perimeter, excluding private rooms.
 common_boundary=core.boundary.difference(unary_union(privatepolys).buffer(.15)).difference(entry['cut'].buffer(.2)).difference(unary_union(baths+[kitchen]).buffer(.15))
 # Chosen by exposed segments, actual light remains unverified.
 wincommon=[]
 for seg in getattr(common_boundary,'geoms',[common_boundary]):
  if seg.geom_type=='LineString' and seg.length>.85:
   mid=seg.interpolate(.5,normalized=True);a=seg.interpolate(max(0,seg.length/2-.55));b=seg.interpolate(min(seg.length,seg.length/2+.55))
   cut=LineString([a,b]).buffer(.13,cap_style=2)
   if cut.intersects(entry['cut'].buffer(.2)):continue
   if cut.intersects(unary_union(baths).buffer(.15)):continue
   wincommon.append(cut)
 wins=wins.union(unary_union(wincommon))
 solid=walls.difference(doors).difference(wins)
 common=core.difference(unary_union(privatepolys)).difference(unary_union(baths))
 tx,ty,tX,tY=table.bounds
 chairs=[Point(x,y).buffer(.21) for x in [tx+.35,tX-.35] for y in [ty-.35,tY+.35]]
 furn=[kitchen,table,sofa]+chairs
 obs=solid.union(unary_union(baths+furn))
 free=floor.difference(obs).buffer(-.45)
 components=[free] if free.geom_type=='Polygon' else [p for p in getattr(free,'geoms',[]) if p.geom_type=='Polygon']
 entrypoint=Point(*entry['inside']);comp=next((p for p in components if p.buffer(.002).covers(entrypoint)),None)
 approaches=[tf(Point(2.6,-.6),r) for r in rooms]
 audit={'codigo':code,'suelo_geometrico_m2':round(floor.area,2),'envolvente_estudio_m2':round(floor.buffer(.12).area,2),'habitacion_geometrica_m2':round(ROOM.area,2),'comun_sin_banos_ni_privados_m2':round(common.area,2),'puertas_privadas_conectadas_disco90':sum(bool(comp is not None and comp.buffer(.002).covers(pt)) for pt in approaches),'solape_habitaciones_m2':round(sum(privatepolys[i].intersection(privatepolys[j]).area for i in range(4) for j in range(i+1,4)),6),'ventanas_comunes_candidatas':len(wincommon),'luz_parcela':'PENDIENTE','acustica':'PENDIENTE','alcanzables':[bool(comp is not None and comp.buffer(.002).covers(pt)) for pt in approaches],'mobiliario_fuera_suelo_m2':round(unary_union(baths+furn).difference(floor).area,6)}
 return locals()
A=family('V01','UN ESPACIO CONTINUO',unary_union([rounded(-6.4,-1.8,5.3,1.8,.24),rounded(-1.95,-.1,1.9,2.05,.12)]),[rr((-2.65,1.8),0),rr((2.65,1.8),0),rr((-2.65,-1.8),180),rr((2.65,-1.8),180)], [box(-1.8,-.05,-.1,1.95),box(.05,-.05,1.75,1.95)],box(-6.24,-1.25,-5.64,1.3),box(-4.8,-.6,-3.2,.25),box(3.65,-1.5,5.05,-.7),{'cut':box(5.1,-.6,5.5,.6),'inside':(4.65,.15),'outside':(6.0,.15)},'Cocinar y estar comparten un ámbito continuo; los baños filtran vistas, pero el sonido todavía puede alcanzar cuatro puertas.',['A07+A08 próximos','A01/A09: protección pendiente','A16+A17 umbral lateral'])
B=family('V02','DOS AMBITOS CONECTADOS',unary_union([rounded(-6.4,-1.2,-.02,2.7,.3),rounded(.02,-2.7,5.35,1.2,.3),rounded(-.8,-.7,.8,.7,.15)]),[rr((-2.65,2.7),0),rr((2.65,1.2),0),rr((-2.65,-1.2),180),rr((2.65,-2.7),180)], [box(-1.83,.7,-.13,2.7),box(.13,-2.7,1.83,-.7)],box(-6.23,-.75,-5.63,1.75),box(-4.8,-.6,-3.2,.25),box(3.6,-1.7,5.1,-.85),{'cut':box(5.15,-.4,5.55,.8),'inside':(4.65,.2),'outside':(6,.2)},'Cocina-comedor y estar ocupan dos ámbitos; una conexión con cierre propuesto permite graduar la relación. No acredita aislamiento acústico.',['A07+A08 en un ámbito','A09 en el segundo','A06 protegido en dormitorio'])
# Annular route: bedrooms occupy cardinal directions, entry lies diagonally.
C3=family('V03','DOS CAMINOS ALREDEDOR',Point(0,0).buffer(3.9,quad_segs=80),[rr((0,3.65),0),rr((3.65,0),-90),rr((0,-3.65),180),rr((-3.65,0),90)], [box(-1.8,-.9,-.1,1.1),box(.05,-.9,1.75,1.1)],translate(rotate(box(-1.2,-.3,1.2,.3),45),-2.35,2.35),box(-2.1,-2.7,-.5,-1.85),box(.6,-3.2,2.2,-2.4),{'cut':box(2.1,2.1,3.4,3.4),'inside':(2.35,2.35),'outside':(3.4,3.4)},'Dos caminos rodean los servicios. El recorrido permite elegir dónde pasar; no debe convertir los dormitorios en escaparate.',['A16/A18 recorrido alternativo','A07+A08 próximos','A09 junto a borde exterior'])
F=[A,B,C3]
# Private use audit with desk/stool in use; user point is the stool centre so exclude stool from obstacles.
privobs=unary_union([BED,DESK,WARD,SEAT]);fr=ROOM.difference(privobs).buffer(-.4)
cs=[fr] if fr.geom_type=='Polygon' else list(getattr(fr,'geoms',[]));root=next((p for p in cs if p.buffer(.001).covers(Point(TARGETS['entrada']))),None)
privcheck={k:bool(root is not None and root.buffer(.001).covers(Point(v))) for k,v in TARGETS.items()}
print('ROOM',ROOM.area,'PRIVATE',privcheck)
print(json.dumps([f['audit'] for f in F],ensure_ascii=False,indent=2))
# Export all exact 2D curves, in metres, without a fake structural 3D model.
def export(f):
 m=rh.File3dm();m.Settings.ModelUnitSystem=rh.UnitSystem.Meters;m.Settings.ModelAbsoluteTolerance=.001
 def add(g,name,col):
  layer=rh.Layer();layer.Name=name;layer.Color=tuple(int(col[i:i+2],16) for i in (1,3,5))+(255,);idx=m.Layers.Add(layer)
  polys=[g] if g.geom_type=='Polygon' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']
  for p in polys:
   for ring in [p.exterior]+list(p.interiors):
    pts=[]
    for x,y in ring.coords:
     pt=rh.Point3d(x,y,0)
     if not pts or pt.DistanceTo(pts[-1])>1e-5:pts.append(pt)
    if len(pts)<4:continue
    pts[-1]=pts[0]
    cv=rh.PolylineCurve(pts)
    if not cv.IsValid:raise ValueError(name)
    a=rh.ObjectAttributes();a.LayerIndex=idx;a.Name=name;m.Objects.AddCurve(cv,a)
 add(f['floor'],'00_SUELO',C['floor']);add(f['solid'],'01_MUROS_CORTE',C['wall']);add(f['wins'],'02_HUECOS',C['glass'])
 for i,r in enumerate(f['rooms']):
  for k,g in FURN.items():add(tf(g,r),f'H{i+1}_{k}',C['seat'] if k=='rincon_ventana' else C['ward'] if k=='ropa' else C['desk'])
 for i,g in enumerate(f['baths']+f['furn']):add(g,f'COMUN_{i}',C['bath'])
 m.Strings['Alcance']='Estudio 2D; suelo z=0. Sin calculo solar, estructural ni cumplimiento normativo.'
 path=P/(f['code']+'_PLANTA_EDITABLE.3dm');m.Write(str(path),8)
 check=rh.File3dm.Read(str(path));assert len(check.Objects)>20 and all(o.Geometry.IsValid for o in check.Objects)
 return len(check.Objects)
def saveplan(f):
 fig,ax=plt.subplots(figsize=(13,12),facecolor='#faf8f2')
 draw(ax,f['floor'],C['floor'])
 for r in f['rooms']:private(ax,r)
 draw(ax,f['solid'],C['wall'])
 for w in f['wincommon']:draw(ax,w,C['glass'])
 for j,b in enumerate(f['baths']):
  draw(ax,b,C['bath']);x,y,X,Y=b.bounds
  draw(ax,box(x+.05,Y-.9,x+.85,Y-.05),'#dce8e5',C['wall']);draw(ax,Point(X-.35,Y-.48).buffer(.22),'#faf8f2',C['wall']);draw(ax,box(x+.05,y+.2,x+.45,y+.55),'#faf8f2',C['wall'])
  txt(ax,x+.9,y+1.05,'baño\n3,40 m²',6)
 for k,c in [('kitchen',C['ward']),('table',C['desk']),('sofa',C['seat'])]:draw(ax,f[k],c,C['wall'])
 for chair in f['chairs']:draw(ax,chair,C['desk'],C['wall'])
 # Kitchen modules and sink/induction.
 k=f['kitchen'];x,y,X,Y=k.bounds
 
 if f['code']!='V03':
  draw(ax,box(x+.07,y+.15,X-.07,y+.65),'#dce8e5',C['wall']);draw(ax,box(x+.07,Y-.6,X-.07,Y-.15),'#33463f')
 else:
  draw(ax,translate(rotate(box(-.9,-.22,-.4,.22),45,origin=(0,0)),-2.35,2.35),'#dce8e5',C['wall']);draw(ax,translate(rotate(box(.4,-.22,.9,.22),45,origin=(0,0)),-2.35,2.35),'#33463f')
 for i,r in enumerate(f['rooms']):
  p=tf(Point(1.0,2.6),r);txt(ax,p.x,p.y,f'H{i+1}',9)
  a=tf(Point(2.6,-.6),r);b=tf(Point(2.6,.7),r);line(ax,LineString([a,b]),C['route'],1.2,'--')
 ex,ey=f['entry']['outside'];ix,iy=f['entry']['inside'];ax.annotate('',xy=(ix,iy),xytext=(ex,ey),arrowprops=dict(arrowstyle='->',color=C['route'],lw=1.6));txt(ax,ex,ey-.35,'ENTRADA',7)
 # Explicit transformable threshold only for two-focus proposal.
 if f['code']=='V02':line(ax,LineString([(0,-.65),(0,.65)]),C['route'],1.8,'--');txt(ax,0,.9,'cierre\npropuesto',6)
 x,y,X,Y=f['floor'].bounds
 ax.set_xlim(x-1.4,X+1.4);ax.set_ylim(y-1.1,Y+1.0);ax.set_aspect('equal');ax.axis('off')
 fig.suptitle(f["code"]+' / '+f['name'],x=.055,y=.975,ha='left',fontsize=20,color='#263d35')
 fig.text(.055,.925,f"4 personas · {f['audit']['suelo_geometrico_m2']:.2f} m² de suelo geométrico · habitación {ROOM.area:.2f} m²\nLa superficie incluye huellas de divisiones; no es superficie útil normativa.",fontsize=10,color='#263d35')
 fig.text(.055,.045,f['hyp']+'\n'+' / '.join(f['links'])+'\nVentanas exteriores dentro de la unidad aislada. Falta luz en parcela, acústica y estructura.',fontsize=9,color='#263d35',wrap=True)
 # Scale in model metres.
 line(ax,LineString([(x,y-.6),(x+5,y-.6)]),'#263d35',2);txt(ax,x+2.5,y-.9,'5 m',8)
 fig.subplots_adjust(top=.88,bottom=.12,left=.06,right=.96)
 fig.savefig(P/(f['code']+'_PLANTA.png'),dpi=150);fig.savefig(P/(f['code']+'_PLANTA.svg'));plt.close(fig)
for f in F:
 f['audit']['frentes_ventana_privada_libres_3m']=sum(tf(box(.8,5.65,2.9,8.65),r).intersection(f['floor']).area<1e-5 for r in f['rooms'])
 assert f['audit']['puertas_privadas_conectadas_disco90']==4
 assert f['audit']['solape_habitaciones_m2']==0
 assert f['audit']['mobiliario_fuera_suelo_m2']==0
 assert f['audit']['frentes_ventana_privada_libres_3m']==4
 f['audit']['objetos_3dm_2d']=export(f);saveplan(f)
assert all(privcheck.values())
# Room study at an identical plotting scale with furniture in use vs board folded.
fig,axs=plt.subplots(1,3,figsize=(20,10),facecolor='#faf8f2')
r=rr((2.6,0),0)
for i,ax in enumerate(axs[:2]):
 private(ax,r,False)
 if i==1:
  draw(ax,DESK,C['private']);draw(ax,box(.07,.25,.12,1.15),C['desk']);draw(ax,STOOL,C['private']);draw(ax,Point(.65,.75).buffer(.23),C['desk'])
  line(ax,DESK.boundary,'#9cafa0',.5,'--')
 walls=ROOM.boundary.buffer(.06).difference(DOOR).difference(WIN);draw(ax,walls,C['wall'])
 # Bodies and curved approach indicate use, not fixed furniture.
 for k,pt in TARGETS.items():
  if k=='dibujar' and i==1:continue
  ax.add_patch(plt.Circle(pt,.20,fill=False,color=C['route'],lw=.8))
 line(ax,LineString([(2.6,-.4),(2.6,1.45),(2.6,3.1),(3.65,3.1)]),C['route'],1,'--')
 line(ax,LineString([(2.6,3.1),(2.55,4.8)]),C['route'],1,'--')
 txt(ax,.88,3.0,'colchón\n1,25 × 2,00',8);txt(ax,.95,.68,'mesa 1,80 × 0,90' if i==0 else 'tablero vertical',8)
 txt(ax,3.83,3.15,'vestidor\ntransitable',8);txt(ax,1.25,4.85,'rincón\n1,30 × 1,00',8)
 txt(ax,2.6,-.55,'puerta 1,00',8)
 ax.set_xlim(-.5,6.2);ax.set_ylim(-.9,6);ax.set_aspect('equal');ax.axis('off');ax.set_title('01 / DIBUJAR Y VESTIRSE' if i==0 else '02 / MESA RECOGIDA',loc='left',fontsize=13)
# Longitudinal section through habitable window; no exploded ceiling.
ax=axs[2]
draw(ax,box(0,-.2,5.5,0),C['bed']);draw(ax,box(0,3,5.5,3.15),C['wall'])
draw(ax,box(5.44,0,5.56,.45),C['wall']);draw(ax,box(5.44,2.65,5.56,3),C['wall'])
line(ax,LineString([(5.5,.45),(5.5,2.65)]),C['glass'],2)
draw(ax,box(4.35,0,5.35,.39),C['bed']);draw(ax,box(4.35,.39,5.35,.47),C['seat'])
# Supported backrest, seat and diagrammatic person.
line(ax,LineString([(5.25,.47),(5.35,1.25)]),C['seat'],6)
ax.add_patch(plt.Circle((5.0,1.28),.12,fill=False,color='#263d35'))
line(ax,LineString([(5,1.15),(4.85,.65),(4.4,.55),(4.2,.47)]),'#263d35',1.5)
line(ax,LineString([(5.8,.5),(5.8,2.85)]),C['seat'],2,'--')
line(ax,LineString([(5.6,2.85),(5.83,2.85)]),C['wall'],1)
txt(ax,4.75,-.5,'1,00 m de apoyo',8);txt(ax,3.0,2.5,'altura libre 3,00 m',9);txt(ax,5.8,1.6,'tela',8)
ax.set_xlim(-.5,6.2);ax.set_ylim(-.9,6);ax.set_aspect('equal');ax.axis('off');ax.set_title('03 / SECCIÓN POR EL RINCÓN',loc='left',fontsize=13)
fig.suptitle('HABITACIÓN / RECUPERAR ESPESOR PARA VIVIR',x=.04,y=.97,ha='left',fontsize=21,color='#263d35')
fig.text(.04,.9,f'{ROOM.area:.2f} m² geométricos · armario curvo: 55 cm para ropa y radio interior 90 cm · bay de ventana: 1,40 m de fondo máximo\nAcceso al rincón por el lado del colchón de asiento; mesa abatible por canto corto de 90 cm. Tablero vertical: estado alternativo.',fontsize=11,color='#263d35')
fig.text(.04,.035,'Plantas y sección esquemática a igual escala métrica. La sección pasa por el asiento, no por el paso lateral.\nCírculos: cuerpos en posiciones de uso. La prueba de recorrido usa disco de 80 cm; no acredita accesibilidad normativa.\nLa bisagra, el bloqueo de la mesa, la protección del vidrio y el anclaje de las telas requieren detalle constructivo.',fontsize=10,color='#263d35')
fig.subplots_adjust(left=.04,right=.97,top=.82,bottom=.12,wspace=.22)
fig.savefig(P/'00_HABITACION_DOS_ESTADOS_Y_SECCION.png',dpi=140);fig.savefig(P/'00_HABITACION_DOS_ESTADOS_Y_SECCION.svg');plt.close(fig)
room_file=rh.File3dm();room_file.Settings.ModelUnitSystem=rh.UnitSystem.Meters;room_file.Settings.ModelAbsoluteTolerance=.001
for name,g in [('SUELO',ROOM),('MUROS',ROOM.boundary.buffer(.06).difference(DOOR).difference(WIN))]+list(FURN.items()):
 layer=rh.Layer();layer.Name=name;idx=room_file.Layers.Add(layer)
 for poly in ([g] if g.geom_type=='Polygon' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']):
  for ring in [poly.exterior]+list(poly.interiors):
   pts=[]
   for x,y in ring.coords:
    pt=rh.Point3d(x,y,0)
    if not pts or pt.DistanceTo(pts[-1])>1e-5:pts.append(pt)
   if len(pts)<4:continue
   pts[-1]=pts[0];cv=rh.PolylineCurve(pts);assert cv.IsValid
   at=rh.ObjectAttributes();at.LayerIndex=idx;at.Name=name;room_file.Objects.AddCurve(cv,at)
room_file.Strings['Alcance']='Estudio 2D, cotas en metros, suelo z=0, estado mesa abierta.'
room_file.Write(str(P/'HABITACION_PLANTA_EDITABLE.3dm'),8)
report={'habitacion':{'area_m2':round(ROOM.area,2),'recorridos_disco80':privcheck,'colisiones_muebles_m2':round(sum(a.intersection(b).area for i,a in enumerate(FURN.values()) for j,b in enumerate(FURN.values()) if j>i),6)},'familias':[f['audit'] for f in F]}
(P/'VERIFICACION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
with open(P/'COMPARACION.csv','w') as out:
 w=csv.DictWriter(out,fieldnames=F[0]['audit']);w.writeheader();w.writerows(f['audit'] for f in F)
