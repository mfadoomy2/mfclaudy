from pathlib import Path
import math,json
import rhino3dm as r
P=Path(__file__).parent;m=r.File3dm();m.Settings.ModelUnitSystem=r.UnitSystem.Meters;m.Settings.ModelAbsoluteTolerance=.001
colors={'suelo':(223,217,195,255),'pared':(125,172,154,255),'cama':(242,198,113,255),'ropa':(182,117,156,255),'mesa':(93,157,174,255),'reserva':(206,89,115,255)}
li={}
for k,col in colors.items():
 l=r.Layer();l.Name=k;l.Color=col;li[k]=m.Layers.Add(l)
def add(g,k,name):
 a=r.ObjectAttributes();a.LayerIndex=li[k];a.Name=name;a.SetUserString('Estado','Ensayo espacial; mobiliario indicativo sin detalle constructivo');m.Objects.Add(g,a)
def prism(poly,z,h,k,name):
 pts=[r.Point3d(x,y,z) for x,y in poly];pts.append(pts[0]);curve=r.PolylineCurve(pts);ex=r.Extrusion.Create(curve,h,True);add(ex,k,name)
def box(x,y,w,d,z,h,k,name):prism([(x,y),(x+w,y),(x+w,y+d),(x,y+d)],z,h,k,name)
def circle(cx,cy,rad,z,h,k,name):
 pl=r.Plane(r.Point3d(cx,cy,z),r.Vector3d(0,0,1));ex=r.Extrusion.Create(r.Circle(r.Point3d(cx,cy,z),rad).ToNurbsCurve(),h,True);add(ex,k,name)
arc=[(4+1.15*math.cos(t),1.9+1.15*math.sin(t)) for t in [-math.pi/2+i*math.pi/48 for i in range(49)]]
outline=[(0,0),(4,0),(4,.75)]+arc[1:]+[(4,4.8),(0,4.8)]
prism(outline,-.16,.16,'suelo','Suelo / rectangulo4x4.8 mas abside armario')
box(0,0,.3,.12,0,2.7,'pared','Jamba entrada');box(1.3,0,2.7,.12,0,2.7,'pared','Muro sur / puerta libre1m')
box(0,.12,.12,4.68,0,2.7,'pared','Pared oeste');box(0,4.68,4,.12,0,.65,'pared','Antepecho norte / hueco sin carpinteria definitiva')
box(4,0,.12,.75,0,2.7,'pared','Pared este baja');box(4,3.05,.12,1.75,0,2.7,'pared','Pared este alta')
outer=[(4+1.27*math.cos(-math.pi/2+i*math.pi/48),1.9+1.27*math.sin(-math.pi/2+i*math.pi/48)) for i in range(49)]
prism(arc+outer[::-1],0,2.7,'pared','Envolvente convexa / nicho concavo interior')
circle(2.65,3.55,1.1,0,.22,'cama','Plataforma circular diametro2.20m');circle(2.65,3.55,1.05,.22,.22,'cama','Colchon circular diametro2.10m / comparar con cuerpo real')
# rail following niche, actual smooth NURBS circle arc
railpts=[r.Point3d(4+.85*math.cos(-1.35+i*2.7/32),1.9+.85*math.sin(-1.35+i*2.7/32),1.7) for i in range(33)]
add(r.PolylineCurve(railpts),'ropa','Barra curva a1.70m / esquema')
for i in range(9):
 t=-1.2+i*.3;cx=4+.87*math.cos(t);cy=1.9+.87*math.sin(t);box(cx-.12,cy-.07,.24,.14,.55,1.05,'ropa','Reserva prendas / no mueble definitivo')
box(1.6,.13,1.6,.8,.75,.045,'mesa','Mesa desplegada1.60x0.80 / reserva de trabajo');circle(2.4,1.3,.2,0,.48,'mesa','Taburete indicativo diametro0.40')
box(3.55,3.72,.25,.35,.55,.025,'mesa','Bandeja pared inferior / carga por resolver');box(3.55,3.72,.25,.35,.8,.025,'mesa','Bandeja pared superior')
# alternative folded drawing board hidden layer
l=r.Layer();l.Name='ALTERNATIVA_MESA_PLEGADA';l.Color=(93,157,174,255);l.Visible=False;li['plegada']=m.Layers.Add(l);box(1.6,.13,1.6,.045,.75,.8,'plegada','Mesa plegada / alternativa no simultanea')
for name,loc,tgt in [('PLANTA',(2,2,18),(2,2,0)),('INTERIOR',(9,-10,10),(2,2,1))]:
 v=r.ViewInfo();v.Name=name;vp=v.Viewport;vp.SetCameraLocation(r.Point3d(*loc));vp.SetCameraDirection(r.Vector3d(*(tgt[i]-loc[i] for i in range(3))));vp.SetCameraUp(r.Vector3d(0,1,0) if name=='PLANTA' else r.Vector3d(0,0,1));vp.TargetPoint=r.Point3d(*tgt);vp.ChangeToParallelProjection(True);vp.Extents(.5,r.BoundingBox(r.Point3d(-.2,-.2,-.2),r.Point3d(5.5,5,3)));m.NamedViews.Add(v)
m.Write(str(P/'HABITACION_CURVA_ENSAYO_A.3dm'),8)
# source V4 copy with intrusive furnishings hidden, not altered
source=P.parent/'G3_UNIDAD_AISLADA_DETALLE_2026-10-16/modelos/UNIDAD_P02_DETALLADA.3dm';base=r.File3dm.Read(str(source))
for l in base.Layers:
 if l.Name in ['20_MOBILIARIO','21_ACCESORIOS','23_ILUMINACION','30_VEGETACION','40_PERSONAS','12_CUBIERTAS','14_VIDRIOS','06_VELAS']:l.Visible=False
base.Write(str(P/'P02_V4_BASE_SIN_MOBILIARIO_VISIBLE.3dm'),8)
area=19.2+math.pi*1.15**2/2
report={'prototype':'Una habitacion experimental independiente; no implantada ni repetida en P02','source':str(source),'clear_envelope_area_m2':area,'rectangle_m':[4,4.8],'niche_radius_m':1.15,'bed_diameter_m':2.1,'door_nominal_m':1,'objects':len(m.Objects),'invalid':sum(not o.Geometry.IsValid for o in m.Objects),'warning':'Sin validacion normativa, estructura, luz interior ni mecanismos; no multiplicar area por4 como dimension final de unidad'}
(P/'VERIFICACION.json').write_text(json.dumps(report,indent=2));print(report)
# plotted true same outline and occupied geometry
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Circle,Rectangle,Arc
fig,ax=plt.subplots(figsize=(11,10));fig.patch.set_facecolor('#f6f3e9');ax.set_facecolor('#f6f3e9');ax.add_patch(Polygon(outline,fc='#e4e3d3',ec='#205b50',lw=3));ax.add_patch(Rectangle((.22,.1),1.08,4.3,fc='#aad1bd',alpha=.5));ax.add_patch(Circle((2.65,3.55),1.1,fc='#dfb77e',ec='#9e774e'));ax.add_patch(Circle((2.65,3.55),1.05,fc='#faf8ef',ec='#9e774e'));ax.add_patch(Rectangle((1.6,.13),1.6,.8,fc='#62a7b5'));ax.add_patch(Circle((2.4,1.3),.2,fc='#62a7b5'));ax.add_patch(Arc((4,1.9),1.7,1.7,theta1=-78,theta2=78,color='#b5759c',lw=4))
for i in range(9):
 t=-1.2+i*.3;cx=4+.87*math.cos(t);cy=1.9+.87*math.sin(t);ax.add_patch(Rectangle((cx-.12,cy-.07),.24,.14,fc='#b5759c'))
ax.plot([.3,1.3],[0,0],color='#f6f3e9',lw=7);ax.annotate('ENTRADA / 1,00 m nominal',(.8,.05),(.1,-.6),arrowprops={'arrowstyle':'->'},fontsize=10);ax.text(.72,2.3,'RECORRIDO LIBRE',rotation=90,ha='center',fontsize=10,color='#205b50');ax.text(2.65,3.55,'CAMA REDONDA\nØ 2,10 m',ha='center',va='center',fontsize=12);ax.text(2.4,.5,'DIBUJO\n1,60 × 0,80',ha='center',va='center',fontsize=10);ax.annotate('ROPA EN ARCO\nnicho R 1,15 m',(4.6,2.4),(5.4,3.4),arrowprops={'arrowstyle':'->'},fontsize=10);ax.text(2,5.2,'HUECO NORTE POR ESTUDIAR',ha='center',color='#205b50',fontsize=11);ax.set_title('P02 / ensayo de una habitación que deforma su envolvente',loc='left',fontsize=16,pad=22);ax.text(0,-1.05,f'{area:.2f} m² interiores geométricos de contorno · ensayo independiente, sin implantar en la unidad',fontsize=10);ax.set_xlim(-.5,7);ax.set_ylim(-1.3,5.6);ax.set_aspect('equal');ax.axis('off');fig.savefig(P/'PLANTA_ENSAYO_A.png',dpi=180,bbox_inches='tight');plt.close(fig)
(P/'LEEME.md').write_text('''# P02 · Habitación curva / ensayo A\n\nVariante espacial aislada; no sustituye ni modifica la P02 original. La base V4 adjunta conserva su geometría con muebles y cubiertas ocultos para revisar.\n\nEnsayo: rectángulo libre de contorno4,00x4,80m más nicho semicircularR1,15m; superficie geométrica21,28m² antes de ajustar acabados. Colchón circularØ2,10m y plataformaØ2,20m. Acceso1m nominal, franja lateral libre de cama y mesa. Mesa desplegada1,60x0,80m y tabureteindicativo. Plegado en capa alternativa oculta. Nicho de ropa con barra curva y volúmenes de reserva, sin detalle de carpintería. Dos bandejas pared, alimentación pendiente.\n\nNo se ha multiplicado porcuatro ni comprobado implantación en megastructura. No es reforma terminada de P02. Esta superficie es deliberadamente generosa para descubrir qué aporta cada abultamiento; siguiente comparación: compactar conservando entrada y uso de mesa, valorar cama rectangular en plataforma curva y calcular consecuencias para el resto de unidad. Cama circular necesita textil específico y comprobar talla real de usuario. No hay simulación lumínica ni dimensionado constructivo ni validación normativa.\n''')
