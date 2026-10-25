from pathlib import Path
import math,json,csv,zipfile,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch
from shapely.geometry import Point,Polygon,LineString,box
from shapely.affinity import rotate,translate,scale
from shapely.ops import unary_union
import rhino3dm as rh
P=Path(__file__).resolve().parents[1];R=P.parent
# Read only the definitions of the previous study. Never execute its output-writing block.
base_source=P/'fuentes/BASE_ANTES.py'
src=base_source.read_text().split('F=[A,B,C3]')[0]
ns={'__file__':str(base_source)};exec(src,ns)
C=ns['C'];draw=ns['draw'];line=ns['line'];txt=ns['txt'];tf=ns['tf'];rounded=ns['rounded']
BASE=ns['base'];VEST=ns['vest'];WARD=ns['WARD'];BED=box(.25,2.00,1.50,4.00);DESK=box(.025,.10,1.825,1.0);STOOL=Point(.95,1.50).buffer(.23);DOOR=ns['DOOR']
# Small circular bow, 0.60 m maximum projection beyond y=4.30.
BC=(1.80,3.65);BR=1.25
bow=Point(*BC).buffer(BR,quad_segs=96).intersection(box(0,4.18,4,5.1))
ROOM=unary_union([BASE,VEST,bow]).buffer(.04).buffer(-.04)
SEAT=Point(*BC).buffer(1.17,quad_segs=96).difference(Point(*BC).buffer(.60,quad_segs=96)).intersection(box(.4,4.04,3.3,5.0))
a0=math.asin((4.30-BC[1])/BR)
angles=np.linspace(a0,math.pi-a0,120)
ARC=LineString([(BC[0]+BR*math.cos(a),BC[1]+BR*math.sin(a)) for a in angles])
WIN=ARC.buffer(.065)
TEXTILE=LineString([(BC[0]+(BR+.18)*math.cos(a),BC[1]+(BR+.18)*math.sin(a)) for a in angles])
FURN={'cama':BED,'mesa_A1':DESK,'vestidor':WARD,'bow_asiento':SEAT,'taburete_en_uso':STOOL}
TARGETS={'entrada':(2.6,.65),'cama':(2.2,3.0),'vestidor':(3.65,3.1),'bow':(2.4,3.55),'dibujar':(.95,1.50)}
privfree=ROOM.difference(unary_union([BED,DESK,WARD,SEAT])).buffer(-.4)
pparts=[privfree] if privfree.geom_type=='Polygon' else list(privfree.geoms)
proot=next((p for p in pparts if p.covers(Point(TARGETS['entrada']))),None)
privcheck={k:bool(proot is not None and proot.buffer(.002).covers(Point(v))) for k,v in TARGETS.items()}
assert all(privcheck.values()),privcheck
assert sum(a.intersection(b).area for i,a in enumerate(FURN.values()) for j,b in enumerate(FURN.values()) if j>i)<1e-6

def polys(g):return [g] if g.geom_type=='Polygon' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']
def parts(g):return [g] if g.geom_type=='LineString' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='LineString']
def geom(f):return unary_union([f['core']]+[tf(ROOM,r) for r in f['rooms']])
def transformed(g,fam,T):return T(g)
def make(fam,mode):
 f=ns['A'] if fam=='V01' else ns['C3'];basefloor=geom(f)
 if fam=='V01':
  shift=14.6 if mode=='D' else 10.6
  T=lambda g:translate(scale(g,xfact=-1,yfact=1,origin=(0,0)),shift,0)
  cx=shift/2;cy=0
  # A real hall in D, a modest continuous widening in S: no duplicated entry doors.
  if mode=='D':link=rounded(4.6,-3.2,shift-4.6,3.2,1.30);entrycut=box(cx-.8,-3.5,cx+.8,-2.9);inside=(cx,-2.5);outside=(cx,-4.1)
  else:link=rounded(3.4,-2.4,shift-3.4,2.4,.60).union(rounded(2.0,1.2,shift-2.0,2.7,.25));entrycut=box(cx-.8,2.45,cx+.8,2.95);inside=(cx,1.7);outside=(cx,3.6)
 else:
  shift=12.0 if mode=='D' else 11.4
  T=lambda g:translate(rotate(g,180,origin=(0,0)),shift,shift)
  cx=cy=shift/2
  diagonal=LineString([(2.5,2.5),(shift-2.5,shift-2.5)])
  if mode=='D':link=diagonal.buffer(1.8).union(Point(cx,cy).buffer(3.05,quad_segs=64))
  else:link=diagonal.buffer(2.25,quad_segs=64)
  # Main entry perpendicular to the communal diagonal, through its south-east side.
  u=np.array([1,-1])/math.sqrt(2);reach=3.05 if mode=='D' else 2.25
  ep=np.array([cx,cy])+u*reach
  entrycut=LineString([tuple(ep+np.array([-.7,-.7])),tuple(ep+np.array([.7,.7]))]).buffer(.24,cap_style=2)
  inside=tuple(ep-u*.8);outside=tuple(ep+u*1.0)
 rooms=[]
 for unit,tr in [('A',lambda g:g),('B',T)]:
  for i,r0 in enumerate(f['rooms']):
   r=dict(r0)
   if fam=='V01' and mode=='S' and i==1:r['q']=(r['q'][0],r['q'][1]+.9)
   rooms.append({'id':f'H{len(rooms)+1:02d}','procedencia':f'{unit}{i+1}','r':r,'T':tr,'poly':tr(tf(ROOM,r))})
 priv=unary_union([r['poly'] for r in rooms])
 floor=unary_union([f['core'],T(f['core']),priv,link])
 assert floor.geom_type=='Polygon'
 common=floor.difference(priv)
 baths=f['baths']+[T(b) for b in f['baths']]
 # All kitchens, dining and work areas belong to eight residents, regardless of retained duplication.
 if fam=='V01':
  kitchens=[box(-6.24,-1.5,-5.64,1.5)]
  utility=[T(f['kitchen'])]
  work=[f['table']]
 else:
  kitchens=[f['kitchen'],T(f['kitchen'])];utility=[];work=[]
 # Shared table, 8 chairs. Keep the approach around the ends clear.
 table0=box(-1.6,-.45,1.6,.45)
 if fam=='V01':
  table=translate(table0,cx,cy)
  chairs=[Point(cx+x,cy+y).buffer(.21) for x in [-1.25,-.42,.42,1.25] for y in [-.85,.85]]
  sofas=[T(f['table'])]
  loungechairs=[T(Point(-4.0,y).buffer(.27)) for y in [1.0,-1.15]]
  if mode=='D':sofas.append(box(cx-1.1,2.15,cx+1.1,2.85))
 else:
  table=translate(rotate(table0,45,origin=(0,0)),cx,cy)
  chairs=[translate(rotate(Point(x,y).buffer(.21),45,origin=(0,0)),cx,cy) for x in [-1.25,-.42,.42,1.25] for y in [-.85,.85]]
  # Existing tables become work tables; existing small sofas become quiet secondary stays.
  work=[f['table'],T(f['table'])];sofas=[f['sofa'],T(f['sofa'])];loungechairs=[]
 commonfurn=kitchens+utility+work+[table]+chairs+sofas+loungechairs
 walls=unary_union([floor.boundary.buffer(.06)]+[r['poly'].boundary.buffer(.06) for r in rooms]+[b.boundary.buffer(.06) for b in baths])
 doors=[entrycut];wins=[]
 for r in rooms:
  doors.append(r['T'](tf(DOOR,r['r'])));wins.append(r['T'](tf(WIN,r['r'])))
 for j,b in enumerate(f['baths']):
  x,y,X,Y=b.bounds;d=box(x+.65,y-.15,x+1.6,y+.15);doors += [d,T(d)]
 # Exterior common glazing: intervals along perimeter, keeping doors and private walls clear.
 boundary=floor.boundary.difference(priv.buffer(.15)).difference(unary_union(baths+kitchens+utility).buffer(.2)).difference(entrycut.buffer(.3))
 wincommon=[]
 for seg in parts(boundary):
  if seg.length<1.1:continue
  mid=seg.length/2
  # Follow the boundary curve, including rounded corners.
  pts=[seg.interpolate(t) for t in np.linspace(max(0,mid-.65),min(seg.length,mid+.65),30)]
  wc=LineString([p.coords[0] for p in pts]).buffer(.13)
  if wc.intersection(priv).area<1e-6:wincommon.append(wc)
 wins+=wincommon
 solid=walls.difference(unary_union(doors)).difference(unary_union(wins))
 # Continuous common circulation: do not allow a shortcut through a bedroom.
 free=common.difference(solid).difference(unary_union(baths+commonfurn)).buffer(-.45)
 components=polys(free);root=next((p for p in components if p.buffer(.002).covers(Point(inside))),None)
 approaches=[r['T'](tf(Point(2.6,-.6),r['r'])) for r in rooms]
 reachable=[bool(root is not None and root.buffer(.002).covers(a)) for a in approaches]
 # Outward strips follow each small bow in its local outward direction.
 strips=[r['T'](tf(box(.72,5.08,2.88,8.08),r['r'])) for r in rooms]
 clear=[g.intersection(floor).area<1e-5 for g in strips]
 overlays=sum(a['poly'].intersection(b['poly']).area for i,a in enumerate(rooms) for j,b in enumerate(rooms) if j>i)
 outsidef=unary_union(baths+commonfurn).difference(floor).area
 # furniture conflict is only meaningful for different separate objects.
 collisions=sum(a.intersection(b).area for i,a in enumerate(commonfurn) for j,b in enumerate(commonfurn) if j>i)
 code=fam+'_'+mode
 audit={'codigo':code,'modo':'union dramatica' if mode=='D' else 'continuidad comun','habitantes':8,'dormitorios':8,'suelo_m2':round(floor.area,2),'envolvente_estudio_m2':round(floor.buffer(.12).area,2),'suelo_sobre_dos_unidades_m2':round(floor.area-2*basefloor.area,2),'comun_sin_privados_ni_banos_m2':round(common.difference(unary_union(baths)).area,2),'entradas_al_ambito_comun':1,'cocinas_compartidas':len(kitchens),'mesas_comer_8':1,'banos':4,'puertas_alcanzables_disco90':sum(reachable),'alcanzables':reachable,'bow_exterior_franja3m':sum(clear),'bow_libres':clear,'solape_privados_m2':round(overlays,6),'muebles_fuera_suelo_m2':round(outsidef,6),'solape_muebles_comunes_m2':round(collisions,6),'asoleo_parcela':'NO VERIFICADO'}
 print(json.dumps(audit,ensure_ascii=False),flush=True)
 return locals()
F=[make(fam,m) for fam in ['V01','V03'] for m in ['D','S']]
(P/'DATOS_INICIALES.json').write_text(json.dumps([f['audit'] for f in F],ensure_ascii=False,indent=2))
# The following are geometric study checks, not regulatory compliance.
for f in F:
 a=f['audit'];assert a['puertas_alcanzables_disco90']==8,a
 assert a['bow_exterior_franja3m']==8,a
 assert a['solape_privados_m2']==0 and a['muebles_fuera_suelo_m2']==0 and a['solape_muebles_comunes_m2']==0,a

def render(ax,f,labels=True,routes=True):
 draw(ax,f['floor'],C['floor'])
 # Same floor colour across former unit boundaries is intentional.
 for r in f['rooms']:
  draw(ax,r['poly'],C['private'])
  for k,g in FURN.items():draw(ax,r['T'](tf(g,r['r'])),C['ward'] if k=='vestidor' else C['seat'] if k=='bow_asiento' else C['bed'] if k=='cama' else C['desk'],ec='#52675b',lw=.3)
  draw(ax,r['T'](tf(WIN,r['r'])),C['glass'])
  line(ax,r['T'](tf(TEXTILE,r['r'])),C['seat'],1.0,'--')
  draw(ax,r['T'](tf(box(1.05,.015,2.05,.055),r['r'])),C['desk'])
  if labels:
   pt=r['poly'].representative_point();txt(ax,pt.x,pt.y,r['id'],7)
 draw(ax,f['solid'],C['wall'])
 for wc in f['wincommon']:draw(ax,wc,C['glass'])
 # Equip the four sanitary reserves symbolically; no new bathroom manoeuvre claim.
 for unit,T in [('A',lambda g:g),('B',f['T'])]:
  for b in f['f']['baths']:
   draw(ax,T(b),C['bath']);x,y,X,Y=b.bounds
   for g,col in [(box(x+.05,Y-.9,x+.85,Y-.05),'#dce7e6'),(Point(X-.35,Y-.48).buffer(.22),'#faf8f2'),(box(x+.05,y+.2,x+.45,y+.55),'#faf8f2')]:draw(ax,T(g),col,C['wall'],.3)
 for k in f['kitchens']:draw(ax,k,C['ward'],C['wall'])
 for k in f['utility']:draw(ax,k,'#9ca596',C['wall'])
 for k in f['work']:draw(ax,k,C['desk'],C['wall'])
 draw(ax,f['table'],C['desk'],C['wall'])
 for ch in f['chairs']+f['loungechairs']:draw(ax,ch,C['desk'],C['wall'])
 for sofa in f['sofas']:draw(ax,sofa,C['seat'],C['wall'])
 if routes:
  # End points only: avoids inventing straight routes through objects.
  for p in f['approaches']:ax.plot(p.x,p.y,'o',ms=2,color=C['route'])
  ax.annotate('',xy=f['inside'],xytext=f['outside'],arrowprops={'arrowstyle':'->','color':C['route'],'lw':1.6})
 if labels:
  cx,cy=f['cx'],f['cy'];txt(ax,cx,cy,'COMER / REUNIRSE\n8 PERSONAS',6,c='white')
  for k in f['kitchens']:pt=k.centroid;txt(ax,pt.x,pt.y,'cocina\ncomún',6)
  for k in f['utility']:pt=k.centroid;txt(ax,pt.x,pt.y,'despensa\ncomún',5)
  for k in f['work']:pt=k.centroid;txt(ax,pt.x,pt.y,'trabajo\ncomún',5,c='white')
  for k in f['sofas']:pt=k.centroid;txt(ax,pt.x,pt.y,'estar',6,c='white')
 for t in ax.texts:t.set_clip_on(True)
 ax.set_aspect('equal');ax.axis('off')

def scale_bar(ax,x,y):line(ax,LineString([(x,y),(x+5,y)]),'#263d35',2);txt(ax,x+2.5,y-.4,'5 m',8)
DESC={
'V01_D':('V01 / UNA SALA EN EL ENCUENTRO','Un espacio común para ocho concentra comida y reunión. El encuentro se reconoce como una pieza mayor.','Gana capacidad colectiva; añade 26,96 m² de suelo frente a dos V01 con la nueva bow.'),
'V01_S':('V01 / UNA SOLA CASA COMPARTIDA','Desaparecen las antiguas entradas entre piezas. Cocina, trabajo, comedor y estar pertenecen al mismo grupo.','Dos dormitorios se desplazan 0,90 m para liberar el paso. La unión añade 6,94 m².'),
'V03_D':('V03 / UNA PLAZA ENTRE DOS ANILLOS','Dos cocinas comunes y dos recorridos alrededor de los servicios desembocan en una sala para ocho.','La separación conserva ventanas, pero aumenta mucho suelo y recorrido.'),
'V03_S':('V03 / UN INTERIOR QUE SE PROLONGA','El espacio colectivo continúa entre los servicios, sin puerta ni umbral doméstico en el encuentro.','No basta con borrar puertas: el comedor obliga a ensanchar la continuidad. Sigue siendo costoso.')}
for f in F:
 fig,ax=plt.subplots(figsize=(17,12),facecolor='#faf8f2');render(ax,f)
 x,y,X,Y=f['floor'].bounds;cx=(x+X)/2;cy=(y+Y)/2
 # All full-plan sheets show an identical model window: 36 m × 32 m.
 ax.set_xlim(cx-18,cx+18);ax.set_ylim(cy-16,cy+16)
 scale_bar(ax,cx-17,cy-14.7)
 title,sub,crit=DESC[f['code']]
 fig.suptitle(title,x=.045,y=.975,ha='left',fontsize=22,color='#263d35')
 a=f['audit'];fig.text(.045,.925,f"8 residentes · 8 habitaciones privadas · 4 baños · {a['suelo_m2']:.2f} m² de suelo geométrico\n{sub}",fontsize=11,color='#263d35')
 fig.text(.045,.035,crit+'\nPuntos rojos: aproximaciones conectadas con disco de 90 cm. No son recorridos rectos dibujados.\nBow: 8 frentes despejados en planta. Luz, acústica, estructura y parcela pendientes.',fontsize=10,color='#263d35')
 fig.subplots_adjust(top=.85,bottom=.12,left=.045,right=.97)
 fig.savefig(P/(f['code']+'_PLANTA.png'),dpi=150);fig.savefig(P/(f['code']+'_PLANTA.svg'));plt.close(fig)
# Same metric frame in every cell, comparison deliberately excludes different crop scales.
fig,axs=plt.subplots(2,2,figsize=(20,18),facecolor='#faf8f2')
for ax,f in zip(axs.flat,F):
 render(ax,f,labels=False,routes=False);x,y,X,Y=f['floor'].bounds;cx=(x+X)/2;cy=(y+Y)/2
 ax.set_xlim(cx-18,cx+18);ax.set_ylim(cy-16,cy+16)
 title=DESC[f['code']][0];ax.set_title(title+'\n'+str(f['audit']['suelo_m2'])+' m² / 8 residentes',fontsize=13,loc='left',color='#263d35')
 scale_bar(ax,cx-16.5,cy-14)
fig.suptitle('CUATRO FORMAS DE COMPARTIR / V01 Y V03',x=.035,y=.985,ha='left',fontsize=24,color='#263d35')
fig.text(.035,.95,'Misma escala métrica en las cuatro celdas. Verde: ámbitos privados. Beige continuo: ámbito de ocho residentes.\nRosa: estar y pequeñas bow windows. Azul: baños. Turquesa: huecos exteriores propuestos.',fontsize=12,color='#263d35')
fig.text(.035,.018,'Las antiguas unidades son puntos de partida geométricos. El programa común y los accesos se reorganizan al juntarlas.\nNo son cuatro edificios implantados ni un resultado de optimización solar.',fontsize=11,color='#263d35')
fig.subplots_adjust(top=.9,bottom=.06,left=.035,right=.98,hspace=.20,wspace=.08)
fig.savefig(P/'00_COMPARACION_CUATRO.png',dpi=140);fig.savefig(P/'00_COMPARACION_CUATRO.svg');plt.close(fig)
# Close-ups reveal the actual change in the seam; all four use a 12×12 m window.
fig,axs=plt.subplots(2,2,figsize=(17,17),facecolor='#faf8f2')
for ax,f in zip(axs.flat,F):
 render(ax,f,labels=True,routes=True);ax.set_xlim(f['cx']-6,f['cx']+6);ax.set_ylim(f['cy']-6,f['cy']+6)
 ax.set_title(f['code']+' / EL ENCUENTRO AUMENTADO',loc='left',fontsize=12,color='#263d35')
fig.suptitle('NO ES SOLO UN PUENTE / QUÉ OCURRE AL JUNTARSE',x=.04,y=.985,ha='left',fontsize=21,color='#263d35')
fig.text(.04,.94,'Mesa de 3,20 × 0,90 m para ocho. Sin puertas entre las antiguas unidades.\nEl uso cambia: recibir, comer, trabajar y estar pertenecen a un ámbito colectivo.',fontsize=12,color='#263d35')
fig.subplots_adjust(top=.89,bottom=.04,left=.04,right=.97,hspace=.15,wspace=.12)
fig.savefig(P/'01_ENCUENTROS_CERCA.png',dpi=140);fig.savefig(P/'01_ENCUENTROS_CERCA.svg');plt.close(fig)
# Bow detail: a genuine circular glass line, curved cushion and a body seated inside the curve.
fig,axs=plt.subplots(1,2,figsize=(16,8),facecolor='#faf8f2');ax=axs[0]
draw(ax,ROOM,C['private']);draw(ax,ROOM.boundary.buffer(.06).difference(DOOR).difference(WIN),C['wall']);draw(ax,SEAT,C['seat']);draw(ax,WIN,C['glass']);line(ax,TEXTILE,C['seat'],1,'--')
line(ax,LineString([(1.78,4.48),(1.95,4.16),(2.25,4.10)]),'#263d35',2)
ax.add_patch(plt.Circle((1.80,4.62),.105,fill=False,color='#263d35'))
# Dimension the cap projection from the previous flat facade plane.
line(ax,LineString([(.5,4.3),(3.15,4.3)]),'#7b8f82',.7,'--')
line(ax,LineString([(3.22,4.3),(3.22,4.9)]),'#263d35',.8);txt(ax,3.46,4.6,'0,60 m',9)
txt(ax,1.8,5.35,'vidrio curvo / cuerda ≈ 2,14 m',10);txt(ax,1.8,3.85,'asiento curvo / fondo central 0,57 m\naproximación desde el dormitorio',10)
ax.set_xlim(.2,3.8);ax.set_ylim(3.3,5.65);ax.set_aspect('equal');ax.axis('off');ax.set_title('PLANTA / ACURRUCARSE EN LA CURVA',loc='left',fontsize=13)
ax=axs[1]
draw(ax,box(0,-.15,2.9,0),C['bed']);draw(ax,box(2.15,0,2.78,.40),C['bed']);draw(ax,box(2.15,.40,2.78,.46),C['seat']);draw(ax,box(2.80,0,2.9,.80),C['wall']);draw(ax,box(2.80,2.65,2.9,3),C['wall'])
line(ax,LineString([(2.85,.80),(2.85,2.65)]),C['glass'],2);line(ax,LineString([(2.70,.46),(2.78,.80)]),C['seat'],6)
ax.add_patch(plt.Circle((2.48,1.15),.105,fill=False,color='#263d35'));line(ax,LineString([(2.48,1.04),(2.40,.58),(2.15,.51),(1.95,.46)]),'#263d35',1.5)
line(ax,LineString([(3.05,.8),(3.05,2.8)]),C['seat'],1,'--');txt(ax,1.4,2.4,'antepecho 0,80 m\nvidrio por encima',10);txt(ax,1.3,-.4,'asiento a 0,46 m / proyección de fachada 0,60 m',9)
ax.set_xlim(-.2,3.5);ax.set_ylim(-.6,3.2);ax.set_aspect('equal');ax.axis('off');ax.set_title('SECCIÓN / UNA VENTANA PEQUEÑA',loc='left',fontsize=13)
fig.suptitle('BOW WINDOW / CURVA, PEQUEÑA Y HABITABLE',x=.04,y=.97,ha='left',fontsize=22,color='#263d35')
fig.text(.04,.88,'Radio de vidrio 1,25 m. La cara interior del asiento acompaña la concavidad; desaparece el cajón rectangular.\nLa habitación baja de 20,56 a '+format(ROOM.area,'.2f')+' m² geométricos al sustituir el mirador profundo.',fontsize=11,color='#263d35')
fig.text(.04,.025,'Detalle de intención y dimensiones de estudio. Faltan carpintería, protección, vidrio, juntas y anclajes.\nLa postura se comprueba después con un cuerpo real o modelo articulado; no es certificación ergonómica.',fontsize=10,color='#263d35')
fig.subplots_adjust(top=.79,bottom=.1,left=.04,right=.97,wspace=.2)
fig.savefig(P/'02_BOW_WINDOW_CURVA.png',dpi=150);fig.savefig(P/'02_BOW_WINDOW_CURVA.svg');plt.close(fig)

# Editable Rhino drawings, one model per alternative, entirely at Z=0.
def export(f):
 m=rh.File3dm();m.Settings.ModelUnitSystem=rh.UnitSystem.Meters;m.Settings.ModelAbsoluteTolerance=.001
 def add(g,name,col):
  l=rh.Layer();l.Name=name;l.Color=tuple(int(col[i:i+2],16) for i in (1,3,5))+(255,);ix=m.Layers.Add(l)
  for p in polys(g):
   for ring in [p.exterior]+list(p.interiors):
    pts=[]
    for x,y in ring.coords:
     q=rh.Point3d(x,y,0)
     if not pts or q.DistanceTo(pts[-1])>1e-5:pts.append(q)
    if len(pts)<4:continue
    pts[-1]=pts[0];c=rh.PolylineCurve(pts);assert c.IsValid
    a=rh.ObjectAttributes();a.Name=name;a.LayerIndex=ix;m.Objects.AddCurve(c,a)
 add(f['floor'],'00_SUELO_COTA0',C['floor']);add(f['solid'],'01_MUROS',C['wall'])
 for r in f['rooms']:
  for k,g in FURN.items():add(r['T'](tf(g,r['r'])),r['id']+'_'+k,C['seat'] if k=='bow_asiento' else C['ward'] if k=='vestidor' else C['desk'])
  # Export the glazing as an analytic arc in addition to its symbolic cut.
  pts=[r['T'](tf(Point(*ARC.coords[i]),r['r'])) for i in [0,len(ARC.coords)//2,-1]]
  arc=rh.Arc(*[rh.Point3d(p.x,p.y,0) for p in pts]);cv=arc.ToNurbsCurve();assert cv.IsValid
  l=rh.Layer();l.Name=r['id']+'_VIDRIO_ARCO';l.Color=(41,154,157,255);ix=m.Layers.Add(l);a=rh.ObjectAttributes();a.LayerIndex=ix;m.Objects.AddCurve(cv,a)
 for i,g in enumerate(f['baths']):add(g,f'BANO_{i+1}',C['bath'])
 for i,g in enumerate(f['commonfurn']):add(g,f'COMUN_{i+1}',C['desk'])
 for i,g in enumerate(f['wincommon']):add(g,f'VENTANA_COMUN_{i+1}',C['glass'])
 m.Strings['Alcance']='Planta de estudio de convivencia, metros, suelo Z=0. Sin implantacion ni calculo solar/estructural.'
 path=P/(f['code']+'_PLANTA.3dm');assert m.Write(str(path),8)
 native=rh.File3dm.Read(str(path));assert native and all(o.Geometry.IsValid for o in native.Objects)
 assert all(abs(o.Geometry.GetBoundingBox().Max.Z)<1e-8 and abs(o.Geometry.GetBoundingBox().Min.Z)<1e-8 for o in native.Objects)
 return len(native.Objects)
for f in F:f['audit']['objetos_rhino_2d']=export(f)
report={'habitacion':{'suelo_m2':round(ROOM.area,2),'bow_proyeccion_m':.6,'radio_vidrio_m':1.25,'cuerda_vidrio_m':round(2*BR*math.cos(a0),2),'recorridos_disco80':privcheck},'alternativas':[f['audit'] for f in F]}
(P/'VERIFICACION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
with open(P/'COMPARACION.csv','w') as out:
 w=csv.DictWriter(out,fieldnames=F[0]['audit']);w.writeheader();w.writerows(f['audit'] for f in F)
# Eight residents in three different moments, without pretending these are surveyed lifestyles.
f=F[1]
meal=[(g.centroid.x,g.centroid.y) for g in f['chairs']]
parallel=[]
for ri in [0,4]:p=f['rooms'][ri]['T'](tf(Point(.95,1.50),f['rooms'][ri]['r']));parallel.append(p.coords[0])
parallel += [(-4.4,.60),(-3.6,.60)]
parallel += [(g.centroid.x,g.centroid.y) for g in f['loungechairs']]
parallel += [(-5.0,.9),(15.8,1.1)]
night=[]
for r in f['rooms'][:6]:p=r['T'](tf(BED.centroid,r['r']));night.append(p.coords[0])
night += [(g.centroid.x,g.centroid.y) for g in f['loungechairs']]
assert len(meal)==len(parallel)==len(night)==8
fig,axs=plt.subplots(3,1,figsize=(17,15),facecolor='#faf8f2')
for ax,pts,title,caption in zip(axs,[meal,parallel,night],['01 / CENAR LAS OCHO','02 / HACER COSAS DISTINTAS','03 / SEIS DESCANSAN, DOS CONVERSAN'],['Una mesa y un ámbito de llegada compartidos.','2 dibujan en privado + 2 trabajan juntas + 2 están + 2 cocinan o recogen.','La estancia en un extremo permite otra intensidad; falta comprobar el ruido hacia dormitorios.']):
 render(ax,f,labels=False,routes=False)
 for x,y in pts:ax.add_patch(plt.Circle((x,y),.20,facecolor='#b74453',edgecolor='#faf8f2',lw=.6))
 x,y,X,Y=f['floor'].bounds;ax.set_xlim(x-.6,X+.6);ax.set_ylim(-7.5,8.5);ax.set_title(title+'\n'+caption,loc='left',fontsize=12,color='#263d35')
fig.suptitle('V01 CONTINUA / LA MISMA CASA EN TRES MOMENTOS',x=.04,y=.985,ha='left',fontsize=22,color='#263d35')
fig.text(.04,.02,'Puntos rojos: ocho residentes, contadas una sola vez en cada escena. Situaciones inventadas de proyecto.\nEl ensayo nocturno identifica un conflicto acústico pendiente; no demuestra que esté resuelto.',fontsize=11,color='#263d35')
fig.subplots_adjust(left=.04,right=.97,top=.92,bottom=.06,hspace=.2)
fig.savefig(P/'03_OCHO_PERSONAS_TRES_MOMENTOS.png',dpi=140);fig.savefig(P/'03_OCHO_PERSONAS_TRES_MOMENTOS.svg');plt.close(fig)
