import geometria as G
import json
from shapely.geometry import shape,LineString,Point
from shapely.affinity import translate,rotate
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch
import rhino3dm as rh
P=G.P;R=G.R;L=P/'laminas'
raw=json.loads((P/'fuentes/PARCELA_REAL.geojson').read_text());parcel=shape(raw['geometry']);ox,oy=raw['properties']['origin_utm']
results=json.loads((P/'verificacion/ENCAJE_PARCELA.json').read_text())['resultados']
context=json.loads((P/'fuentes/CONTEXTO_CATASTRAL.geojson').read_text())
ctx=[]
for feat in context['features']:
 g=translate(shape(feat['geometry']),-ox,-oy)
 if g.intersects(G.box(-20,-35,85,40)):ctx.append((g,feat['properties']))

def bg(ax):
 for g,pr in ctx:
  G.draw(ax,g,'#d6d6d0',ec='#b8bcb5',lw=.4)
 G.draw(ax,parcel,'#f9f6e9',ec='#263d35',lw=1.2)
 G.txt(ax,4,0,'RIBERA DE\nCURTIDORES',10)
 ax.annotate('N de cuadrícula',xy=(71,18),xytext=(71,10),arrowprops={'arrowstyle':'->','color':'#263d35'},fontsize=8,ha='center')
 G.line(ax,LineString([(15,-12),(25,-12)]),'#263d35',2);G.txt(ax,20,-14,'10 m',8)
 ax.set_xlim(-4,77);ax.set_ylim(-17,22);ax.set_aspect('equal');ax.axis('off')

def placement(f,row):
 c=f['floor'].buffer(.12).centroid;x,y=row['centro_local_m'];ang=row['rotacion_grados']
 return lambda g:translate(rotate(translate(g,-c.x,-c.y),ang,origin=(0,0)),x,y)

for f,row in zip(G.F,results):
 T=placement(f,row);fig,ax=plt.subplots(figsize=(16,9),facecolor='#faf8f2');bg(ax)
 for g in f['strips']:G.draw(ax,T(g),'#f2c5b5',alpha=.48)
 G.draw(ax,T(f['floor']),'#e8dfcb',ec='#748579',lw=.4)
 for r in f['rooms']:
  G.draw(ax,T(r['poly']),'#cfdcc7')
  for k,g in G.FURN.items():G.draw(ax,T(r['T'](G.tf(g,r['r']))),G.C['bed'] if k=='cama' else G.C['seat'] if k=='bow_asiento' else G.C['desk'])
  G.draw(ax,T(r['T'](G.tf(G.WIN,r['r']))),G.C['glass'])
 for b in f['baths']:G.draw(ax,T(b),G.C['bath'])
 for g in f['furniture']:G.draw(ax,T(g),G.C['desk'])
 G.draw(ax,T(f['solid']),G.C['wall'])
 G.draw(ax,T(f['floor'].buffer(.12)).difference(parcel),'#b82f62')
 ip=T(Point(f['entry']['inside']));op=T(Point(f['entry']['outside']));ax.annotate('',xy=(ip.x,ip.y),xytext=(op.x,op.y),arrowprops={'arrowstyle':'->','color':'#b94c6c','lw':1.7})
 fig.suptitle(row['codigo']+' / prueba a escala 1:1 en la parcela',x=.04,y=.97,ha='left',fontsize=19,color='#263d35')
 status='CONTORNO DENTRO' if row['ajuste_completo'] else 'ENCAJE RECHAZADO EN ESTA POSICIÓN'
 fig.text(.04,.90,f"{status} / {row['area_envolvente_m2']:.2f} m² / fuera: {row['fuera_parcela_m2']:.3f} m²\nLlegada exterior con disco 90 cm desde frente: {'conectada' if row['paso_exterior_90cm_desde_frente'] else 'no conectada en este ensayo'}",fontsize=10,color='#263d35')
 fig.text(.04,.025,'Gris: huellas catastrales del entorno. Salmón: bandas de 3 m delante de las bow, sin cálculo de luz. Rosa fuerte: invasión de parcela.\nNo es una planta edificable validada. Cota vertical sin asignar; no se comprueban altura vecina, retranqueos, estructura ni núcleo.',fontsize=9,color='#263d35')
 fig.subplots_adjust(top=.84,bottom=.10,left=.03,right=.97);fig.savefig(L/(row['codigo']+'_PARCELA.svg'));fig.savefig(L/(row['codigo']+'_PARCELA.png'),dpi=150);plt.close(fig)
 # Site curves in the same local coordinate frame, all Z=0.
 m=rh.File3dm();m.Settings.ModelUnitSystem=rh.UnitSystem.Meters
 def add(g,name,col):
  layer=rh.Layer();layer.Name=name;layer.Color=col;idx=m.Layers.Add(layer)
  for p in G.polys(g):
   for ring in [p.exterior]+list(p.interiors):
    pts=[]
    for x,y in ring.coords:
     pt=rh.Point3d(x,y,0)
     if not pts or pt.DistanceTo(pts[-1])>1e-5:pts.append(pt)
    if len(pts)<4:continue
    if pts[-1].DistanceTo(pts[0])<1e-5:pts[-1]=pts[0]
    else:pts.append(pts[0])
    c=rh.PolylineCurve(pts)
    if not c.IsValid:continue
    a=rh.ObjectAttributes();a.LayerIndex=idx;m.Objects.AddCurve(c,a)
 add(parcel,'PARCELA',(40,65,50,255));add(G.unary_union([g for g,pr in ctx]),'CONTEXTO_CATASTRAL',(180,180,175,255));add(T(f['solid']),'MUROS',(40,65,50,255))
 for b in f['banks']:
  for g in [G.box(.08,1.30,.98,2.20),Point(1.60,1.90).buffer(.22),G.box(1.40,.80,1.85,1.12),G.box(1.02,-2.20,1.92,-1.30),Point(.40,-1.90).buffer(.22),G.box(.15,-1.12,.60,-.80)]:add(T(b['T'](g)),'APARATOS_ESQUEMATICOS',(150,170,175,255))
 for r in f['rooms']:
  for k,g in G.FURN.items():add(T(r['T'](G.tf(g,r['r']))),r['id']+'_'+k,(180,130,80,255))
 m.Strings['Base']='Origen EPSG25830 439984,4473229.4; XY local sin rotacion; Z0 no asigna altura de implantacion.'
 path=P/'modelos_2d'/(row['codigo']+'_PARCELA.3dm');m.Write(str(path),8)
 assert all(o.Geometry.IsValid for o in rh.File3dm.Read(str(path)).Objects)
fig,ax=plt.subplots(figsize=(16,9),facecolor='#faf8f2');bg(ax)
for x,y,label in [(12.7,1,'FRENTE / acceso desde calle'),(39,4,'ESTRECHAMIENTO'),(56,-2,'FONDO')]:
 ax.plot(x,y,'o',color='#b94c6c');G.txt(ax,x,y+3,label,9)
fig.suptitle('PARCELA REAL / 650,91 m² / contexto y restricciones',x=.04,y=.97,ha='left',fontsize=20,color='#263d35')
fig.text(.04,.04,'Base local derivada de Catastro. Las huellas del entorno no son un levantamiento de alturas.\nLa parcela se utiliza como restricción, sin introducir la megaestructura anterior como punto de partida.',fontsize=10,color='#263d35')
fig.subplots_adjust(top=.88,bottom=.12,left=.03,right=.97);fig.savefig(L/'PARCELA_CONTEXTO.svg');fig.savefig(L/'PARCELA_CONTEXTO.png',dpi=160);plt.close(fig)
