import geometria as G
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point,LineString,box
from shapely.ops import unary_union
import rhino3dm as rh
P=G.P;L=P/'laminas';L.mkdir(exist_ok=True);M=P/'modelos_2d';M.mkdir(exist_ok=True)
NAMES={'V01_U':'V01 / convivencia continua','V02_U':'V02 / dos ambitos conectados','V03_U':'V03 / estar libre en el circulo','V02_P':'V02 / dos viviendas y un umbral','V01_D':'V01 / encuentro mayor','V01_S':'V01 / una casa compartida','V03_D':'V03 / plaza entre dos estancias','V03_S':'V03 / continuidad diagonal'}
WHY={
'V01_U':'Cocinar, comer y estar se enlazan en un ambito continuo. Servicios en el extremo, con llegada filtrada.',
'V02_U':'Se diferencian comer/estar tranquilo y cocinar/convivir. La conexion admite graduar la relacion entre actividades.',
'V03_U':'El antiguo centro de servicios queda libre para estar. Los aseos se llevan a un borde conectado en diagonal.',
'V02_P':'Dos grupos conservan accesos a sus espacios compartidos. El umbral permite encuentro sin atravesar la casa vecina.',
'V01_D':'Una sala mayor recibe a ocho. La cocina, trabajo y estancia pertenecen al grupo, sin puertas entre antiguas unidades.',
'V01_S':'Dos dormitorios se desplazan 0,90 m y el comedor se integra en la continuidad de una vivienda de ocho.',
'V03_D':'El encuentro se ensancha como plaza interior. Los servicios de cada extremo quedan fuera del ambito principal.',
'V03_S':'Una estancia diagonal prolonga la convivencia. Conserva diferencia entre lugares sin reinstalar banos en su centro.'}

def render(ax,f,diagram=False):
 G.draw(ax,f['floor'],G.C['floor'])
 for b in f['banks']:G.draw(ax,b['floor'],'#dbe3e3')
 for r in f['rooms']:
  G.draw(ax,r['poly'],G.C['private'])
  if not diagram:
   for k,g in G.FURN.items():G.draw(ax,r['T'](G.tf(g,r['r'])),G.C['seat'] if k=='bow_asiento' else G.C['ward'] if k=='vestidor' else G.C['desk'] if k in ['mesa_A1','taburete_en_uso'] else G.C['bed'],ec='#698073',lw=.3)
   G.draw(ax,r['T'](G.tf(G.WIN,r['r'])),G.C['glass']);G.line(ax,r['T'](G.tf(G.TEXTILE,r['r'])),G.C['seat'],.9,'--')
  p=r['poly'].representative_point();G.txt(ax,p.x,p.y,r['id'],8)
 if not diagram:
  G.draw(ax,f['solid'],G.C['wall'])
  for w in f['wc']:G.draw(ax,w,G.C['glass'])
  for bank in f['banks']:
   for b0 in f['u']['bank']['baths0']:
    x,y,X,Y=b0.bounds
    G.draw(ax,bank['T'](b0),G.C['bath'])
    fixtures=[box(.08,1.30,.98,2.20),Point(1.60,1.90).buffer(.22),box(1.40,.80,1.85,1.12)] if y>0 else [box(1.02,-2.20,1.92,-1.30),Point(.40,-1.90).buffer(.22),box(.15,-1.12,.60,-.80)]
    for g in fixtures:G.draw(ax,bank['T'](g),'#faf8f2',G.C['wall'],.3)
   p=bank['floor'].centroid;G.txt(ax,p.x,p.y,'SERVICIOS\nEN BORDE',7)
  for k in f['kitchens']:G.draw(ax,k,G.C['ward'],G.C['wall'])
  for k in f['utility']:G.draw(ax,k,'#97a99c',G.C['wall'])
  for k in f['work']+f['tables']:G.draw(ax,k,G.C['desk'],G.C['wall'])
  for k in f['chairs']:G.draw(ax,k,G.C['desk'],G.C['wall'])
  for k in f['sofas']:G.draw(ax,k,G.C['seat'],G.C['wall'])
  G.draw(ax,f['solid'],G.C['wall'])
  for p in f['approaches']:ax.plot(p.x,p.y,'o',ms=2,color=G.C['route'])
 else:
  # These are new diagrams of interpretation, not reconstructed original generative coordinates.
  food=f['tables'][0].centroid if f['tables'] else f['kitchens'][0].centroid
  talk=f['sofas'][0].centroid;cook=f['kitchens'][0].centroid
  for p,t,c in [(food,'comer',G.C['desk']),(cook,'preparar',G.C['ward']),(talk,'estar',G.C['seat'])]:
   ax.plot(p.x,p.y,'o',ms=7,color=c);G.txt(ax,p.x,p.y+.45,t,8)
  G.line(ax,LineString([food,cook]),'#218a83',1.3)
  G.line(ax,LineString([food,talk]),'#218a83',1.3)
  for r in f['rooms']:
   p=r['T'](G.tf(G.BED.centroid,r['r']));G.line(ax,LineString([p,talk]),'#bf5a78',.6,'--')
  for b in f['banks']:
   p=b['floor'].centroid;ax.plot(p.x,p.y,'s',ms=7,color='#7996a3');G.txt(ax,p.x,p.y+.5,'aseo / paso',8)
 ax.annotate('',xy=f['entry']['inside'],xytext=f['entry']['outside'],arrowprops={'arrowstyle':'->','color':G.C['route'],'lw':1.5})
 for text in ax.texts:text.set_clip_on(True)
 ax.set_aspect('equal');ax.axis('off')

def frame(ax,f):
 x,y,X,Y=f['floor'].bounds;dx=X-x;dy=Y-y
 pad=.9;ax.set_xlim(x-pad,X+pad);ax.set_ylim(y-pad,Y+pad)
 G.line(ax,LineString([(x,y-.5),(x+5,y-.5)]),'#263d35',2);G.txt(ax,x+2.5,y-.8,'5 m',8)
for f in G.F:
 for diagram in [False,True]:
  fig,ax=plt.subplots(figsize=(16,10.5),facecolor='#faf8f2');render(ax,f,diagram);frame(ax,f)
  code=f['audit']['codigo'];fig.suptitle(NAMES[code]+(' / lectura relacional' if diagram else ' / planta corregida'),x=.04,y=.975,ha='left',fontsize=20,color='#263d35')
  a=f['audit'];fig.text(.04,.91,f"{a['habitantes']} residentes / {a['suelo_m2']:.2f} m² de suelo geometrico / {a['envolvente_estudio_m2']:.2f} m² de envolvente de estudio\n{WHY[code]}",fontsize=10,color='#263d35')
  foot='Lineas verdes: proximidad interpretada. Rosas: conflicto que exige proteccion. No son pasillos ni aislamiento comprobado.' if diagram else 'Puntos rojos: aproximaciones privadas. Aseos en borde con paso corto y puertas laterales. Sin calculo solar, acustico ni estructural.'
  fig.text(.04,.025,foot,fontsize=9,color='#263d35');fig.subplots_adjust(left=.04,right=.97,top=.83,bottom=.09)
  name=code+('_DIAGRAMA_NUEVO' if diagram else '_PLANTA_CORREGIDA')
  fig.savefig(L/(name+'.png'),dpi=170);fig.savefig(L/(name+'.svg'));plt.close(fig)
 # Curve export corresponding to the final new plans, not the superseded bathroom islands.
 m=rh.File3dm();m.Settings.ModelUnitSystem=rh.UnitSystem.Meters;m.Settings.ModelAbsoluteTolerance=.001
 def add(g,name,col):
  l=rh.Layer();l.Name=name;l.Color=tuple(int(col[i:i+2],16) for i in (1,3,5))+(255,);idx=m.Layers.Add(l)
  for p in G.polys(g):
   for ring in [p.exterior]+list(p.interiors):
    pts=[]
    for x,y in ring.coords:
     q=rh.Point3d(x,y,0)
     if not pts or q.DistanceTo(pts[-1])>1e-5:pts.append(q)
    if len(pts)<4:continue
    pts[-1]=pts[0];c=rh.PolylineCurve(pts);assert c.IsValid
    a=rh.ObjectAttributes();a.Name=name;a.LayerIndex=idx;m.Objects.AddCurve(c,a)
 add(f['floor'],'00_SUELO',G.C['floor']);add(f['solid'],'01_MUROS_Y_FILTROS',G.C['wall'])
 for i,b in enumerate(f['banks']):
  add(b['floor'],f'SERVICIOS_{i+1}',G.C['bath'])
  for g in [box(.08,1.30,.98,2.20),Point(1.60,1.90).buffer(.22),box(1.40,.80,1.85,1.12),box(1.02,-2.20,1.92,-1.30),Point(.40,-1.90).buffer(.22),box(.15,-1.12,.60,-.80)]:add(b['T'](g),f'APARATOS_ESQUEMATICOS_{i+1}',G.C['bath'])
 for r in f['rooms']:
  for k,g in G.FURN.items():add(r['T'](G.tf(g,r['r'])),r['id']+'_'+k,G.C['seat'] if k=='bow_asiento' else G.C['ward'] if k=='vestidor' else G.C['desk'])
  add(r['T'](G.tf(G.WIN,r['r'])),r['id']+'_VIDRIO',G.C['glass'])
 for i,g in enumerate(f['furniture']):add(g,f'COMUN_{i+1}',G.C['desk'])
 m.Strings['Regla']='Banos en borde de servicios, nunca isla central en estar. Plantas de estudio; sin cumplimiento normativo certificado.'
 out=M/(f['audit']['codigo']+'_CORREGIDA.3dm');m.Write(str(out),8);chk=rh.File3dm.Read(str(out));assert all(o.Geometry.IsValid for o in chk.Objects)
# Service detail makes both the spatial separation and the route legible.
f=G.F[0];b=f['banks'][0];fig,ax=plt.subplots(figsize=(11,9),facecolor='#faf8f2');render(ax,f)
x,y,X,Y=b['floor'].bounds;ax.set_xlim(x-.4,X+1.5);ax.set_ylim(y-.6,Y+.6)
for dc in b['door_centres']:
 ray=LineString([b['view'],dc]);hit=ray.intersection(f['solid']);pts=[]
 for g in ([hit] if hit.geom_type=='LineString' else getattr(hit,'geoms',[])):
  if g.geom_type=='LineString' and not g.is_empty:pts += [Point(*g.coords[0]),Point(*g.coords[-1])]
 if pts:
  stop=min(pts,key=lambda p:p.distance(b['view']));G.line(ax,LineString([b['view'],stop]),'#b94c6c',1,'--');ax.plot(stop.x,stop.y,'x',color='#b94c6c',ms=6)
G.txt(ax,X+.8,0,'estar\nfuera del\nvestibulo',10)
fig.suptitle('SERVICIOS EN BORDE / FILTRAR SIN BLOQUEAR',x=.05,y=.98,ha='left',fontsize=17,color='#263d35')
fig.text(.05,.025,'Las puertas laterales evitan el acceso frontal al WC. El paso se comprueba con disco de 90 cm.\nSe verifican aproximaciones a puertas. Las maniobras completas dentro del bano quedan pendientes.',fontsize=9,color='#263d35')
fig.subplots_adjust(top=.90,bottom=.10);fig.savefig(L/'DETALLE_SERVICIOS.png',dpi=170);fig.savefig(L/'DETALLE_SERVICIOS.svg');plt.close(fig)
# Units compared without normalizing their silhouette size.
fig,axs=plt.subplots(1,3,figsize=(21,11),facecolor='#faf8f2')
for ax,f in zip(axs,G.F[:3]):
 render(ax,f);x,y,X,Y=f['floor'].bounds;cx=(x+X)/2;cy=(y+Y)/2;ax.set_xlim(cx-11,cx+11);ax.set_ylim(cy-11,cy+11);ax.set_title(NAMES[f['audit']['codigo']],loc='left',fontsize=12)
fig.suptitle('TRES ORGANIZACIONES / CENTROS PARA CONVIVIR',x=.03,y=.98,ha='left',fontsize=22,color='#263d35');fig.text(.03,.025,'Misma escala en las tres celdas. Los bloques de servicio son perifericos; no son el centro de las salas.',fontsize=11)
fig.subplots_adjust(top=.90,bottom=.08,left=.03,right=.98,wspace=.10);fig.savefig(L/'COMPARACION_UNIDADES.png',dpi=150);fig.savefig(L/'COMPARACION_UNIDADES.svg');plt.close(fig)
