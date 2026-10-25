from pathlib import Path
import math,json
P=Path(__file__).parent
src=P.parent/'G3_P02_HABITACION_CURVA_2026-10-18/crear.py'
s=src.read_text();s=s[s.index('import math,json'):s.index('# source V4 copy')];s=s.replace('P=Path(__file__).parent;', '')
s=s.replace("box(1.6,.13,1.6,.8,.75,.045", "box(1.65,.13,1.8,.9,.75,.045").replace("box(1.6,.13,1.6,.045,.75,.8", "box(1.65,.13,1.4,.045,.75,.9")
s=s.replace("box(0,4.68,4,.12,0,.65,'pared','Antepecho norte / hueco sin carpinteria definitiva')", "box(1.65,4.68,2.35,.12,0,.65,'pared','Antepecho norte');box(0,4.68,.25,.12,0,.65,'pared','Antepecho extremo');box(.25,4.8,1.4,.55,-.16,.16,'suelo','Ventana habitable / suelo');box(.25,4.8,1.4,.55,0,.45,'mesa','Banco ventana 1.40x0.55');box(.25,5.35,1.4,.06,.45,.15,'pared','Antepecho ventana')")
s=s.replace("m.Write(str(P/'HABITACION_CURVA_ENSAYO_A.3dm'),8)", '')
s=s.replace('circle(2.4,1.3,.2','circle(2.35,1.48,.21').replace('Mesa desplegada1.60x0.80','Mesa desplegada1.80x0.90')
exec(s)
add(r.PolylineCurve([r.Point3d(2.65+1.15*math.cos(t),3.55+1.15*math.sin(t),1.0) for t in [math.radians(15+i*145/48) for i in range(49)]]),'ropa','Cabecero envolvente / perfil esquematico')
# drawing reference panel beside desk, not overhead
box(3.55,.15,.06,1.05,.85,1.05,'ropa','Moodboard lateral fijo / junto a tablero')
# hinged leaf extends towards work position but not crossing entrance
prism([(3.55,1.2),(3.05,1.45),(3.08,1.5),(3.58,1.25)],.9,.85,'ropa','Panel articulado / posicion orientada al dibujo')
box(3.05,.13,.4,.9,.75,.06,'mesa','Banda horizontal fija / utiles y carga por resolver')
# collective threshold and shared workspace are a fragment, no full unit claim
box(0,-1.6,4,1.6,-.16,.16,'suelo','Umbral compartido / paso1.60nominal')
box(0,-5.6,4,4,-.16,.16,'suelo','Fragmento estancia comun / programa restante no resuelto')
box(.8,-4.3,2.4,1.1,.75,.06,'mesa','Mesa compartida para comer o maquetas')
for x in [1.2,2.8]:
 for y in [-4.7,-2.75]:circle(x,y,.22,0,.45,'mesa','Asiento comun esquematico')
box(3.4,-1.45,.55,1.1,0,.45,'mesa','Banco de encuentro fuera del paso lateral')
# schematic ridge frame curves, roof omitted to inspect interior
for x in [.15,3.85]:
 pts=[r.Point3d(x,y,z) for y,z in [(0,2.75),(.3,3.05),(1.3,3.65),(1.65,3.65),(2.1,2.9),(4.8,2.75)]];add(r.PolylineCurve(pts),'reserva','Perfil cresta / cubierta pendiente')
assert m.Write(str(P/'P02_A_REVISADA_HABITACION_Y_UMBRAL.3dm'),8)
check=r.File3dm.Read(str(P/'P02_A_REVISADA_HABITACION_Y_UMBRAL.3dm'));assert not any(not o.Geometry.IsValid for o in check.Objects)
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Rectangle,Circle,Arc
bg='#f6f3e9';ink='#24594e';blue='#65a7b5';pink='#b7789c';green='#b8d3bc'
def init(title,size=(12,12)):
 fig,ax=plt.subplots(figsize=size);fig.patch.set_facecolor(bg);ax.set_facecolor(bg);ax.set_aspect('equal');ax.axis('off');ax.set_title(title,loc='left',fontsize=18,pad=25,color=ink);return fig,ax
def save(fig,name):
 fig.savefig(P/(name+'.png'),dpi=180,bbox_inches='tight');fig.savefig(P/(name+'.svg'),bbox_inches='tight');plt.close(fig)
def note(ax,text,p,q):ax.annotate(text,p,q,fontsize=10,color=ink,arrowprops=dict(arrowstyle='-',color=ink),bbox=dict(fc=bg,ec='none',pad=2))
fig,ax=init('A revisada / retiro privado y encuentro compartido')
ax.add_patch(Rectangle((0,-5.6),4,4,fc='#d8e0cc',ec=ink,lw=2));ax.add_patch(Rectangle((0,-1.6),4,1.6,fc='#efe4ba',ec=ink,lw=2));ax.add_patch(Polygon(outline,fc='#e3e3d4',ec=ink,lw=3));ax.add_patch(Rectangle((.25,4.8),1.4,.55,fc='#cce3dc',ec=ink,lw=2));ax.text(.95,5.05,'VENTANA / BANCO',ha='center',fontsize=8)
ax.add_patch(Rectangle((.22,.15),1.05,4.2,fc=green,alpha=.55));ax.plot([.3,1.3],[0,0],color=bg,lw=7);ax.annotate('',(.8,1),(.8,-1.3),arrowprops=dict(arrowstyle='->',color=ink,lw=2));ax.text(.7,2.7,'ACCESO LATERAL LIBRE',ha='center',rotation=90,fontsize=9,color=ink)
ax.add_patch(Circle((2.65,3.55),1.1,fc='#d9b780',ec=ink));ax.add_patch(Circle((2.65,3.55),1.05,fc='#fffdf5',ec=ink));ax.add_patch(Arc((2.65,3.55),2.3,2.3,theta1=15,theta2=160,color=pink,lw=6));ax.text(2.65,3.55,'CAMA\nØ 2,10',ha='center',va='center',fontsize=12)
for ty in [3.2,3.7]:ax.add_patch(Rectangle((3.55,ty),.25,.25,fc=blue))
ax.add_patch(Arc((4,1.9),1.7,1.7,theta1=-78,theta2=78,lw=5,color=pink));note(ax,'ROPA EN ARCO\ncierre + espejo por desarrollar',(4.7,1.9),(5.5,2.4))
ax.add_patch(Rectangle((1.65,.13),1.8,.9,fc=blue,ec=ink));ax.plot([3.05,3.05],[.13,1.03],color=bg,lw=2);ax.text(2.35,.55,'DIBUJO\n1,40 × 0,90',ha='center',va='center',fontsize=9);ax.text(3.25,.55,'FIJO',ha='center',rotation=90,fontsize=8)
ax.add_patch(Circle((2.35,1.48),.21,fc=blue));ax.add_patch(Rectangle((1.9,1.03),.9,.9,fill=False,ec=blue,ls='--'));ax.plot([3.55,3.55],[.15,1.2],color=pink,lw=5);ax.plot([3.55,3.05],[1.2,1.45],color=pink,lw=3);note(ax,'MOODBOARD LATERAL\nfijo + hoja orientable',(3.3,1.32),(5.4,.5))
note(ax,'CABECERO + DOS BANDEJAS\nluz y carga pendientes',(3.6,4.05),(5.4,4.6))
ax.add_patch(Rectangle((3.4,-1.45),.55,1.1,fc=blue));note(ax,'BANCO DE ENCUENTRO\nfuera del acceso lateral',(3.65,-.8),(5.3,-1.1));ax.text(1.7,-.8,'UMBRAL COMPARTIDO\n1,60 m nominal',ha='center',fontsize=10)
ax.add_patch(Rectangle((.8,-4.3),2.4,1.1,fc=blue,ec=ink));ax.text(2,-3.75,'MESA COMÚN\n2,40 × 1,10',ha='center',fontsize=11)
for x in [1.2,2.8]:
 for y in [-4.7,-2.75]:ax.add_patch(Circle((x,y),.22,fc=blue))
ax.text(2,-5.3,'COMER / MAQUETAS / TRABAJO ACOMPAÑADO',ha='center',fontsize=8);ax.text(0,-6.2,'Fragmento de relación: una habitación y una estancia común. No es la unidad completa de cuatro personas.',fontsize=10,color=ink)
ax.plot([2.35,2.35],[-5.7,5],color='#ad7351',ls='-.',lw=.8);ax.text(2.35,5.55,'1—1',ha='center',fontsize=10);ax.set_xlim(-.6,8);ax.set_ylim(-6.5,5.8);save(fig,'01_PLANTA_RELACION')
# longitudinal section at x2.35 -- does not intersect window seat, shown separately
fig,ax=init('A revisada / sección 1—1 · compartir, dibujar, dormir',(14,8))
ax.plot([-5.6,4.8],[0,0],color=ink,lw=4);roof=[(0,2.75),(.3,3.05),(1.3,3.65),(1.65,3.65),(2.1,2.9),(4.8,2.75)];ax.plot(*zip(*roof),color=ink,lw=4);ax.plot([.3,1.3],[3.05,3.65],color=blue,lw=6)
ax.plot([-5.6,0],[2.7,2.7],color=ink,lw=2);ax.plot([0,0],[0,2.75],color=ink,lw=3);ax.text(-.2,1.6,'separación\nprivada',ha='right',fontsize=10)
ax.add_patch(Rectangle((-4.3,.75),1.1,.06,fc=blue));ax.add_patch(Rectangle((.13,.75),.9,.045,fc=blue));ax.plot([.13,.87],[.75,1.27],color=blue,lw=3);ax.plot([.13,.13],[.75,1.65],color=blue,ls='--');ax.add_patch(Rectangle((1.27,.43),.42,.05,fc=blue));ax.add_patch(Rectangle((2.49,.0),2.11,.22,fc='#d9b780'));ax.add_patch(Rectangle((2.54,.22),2.01,.22,fc='#fffdf5',ec=ink));ax.plot([4.65,4.65],[0,1.05],color=pink,lw=5)
note(ax,'CRESTA DE LUZ / orientación por comprobar',(1,3.5),(1.7,4.2));note(ax,'mesa inclinable / tres estados alternativos',(.65,1),(0,-.8));ax.text(-3.8,1.1,'mesa común',ha='center',fontsize=11);ax.text(-.8,-.35,'umbral',ha='center',fontsize=10);ax.text(3.55,.7,'cama / cabecero',ha='center',fontsize=10)
for x,z in [(.5,3.15),(1.1,3.5)]:ax.annotate('',(.7,.85),(x,z-.15),arrowprops=dict(arrowstyle='->',color='#c4a046'))
ax.text(-5.5,-1.25,'Corte coherente con planta. Ventana-banco fuera de este corte. Flechas ilustrativas; sin simulación de luz.',fontsize=10,color=ink);ax.set_xlim(-6,5.4);ax.set_ylim(-1.5,4.6);save(fig,'02_SECCION_RELACION')
fig,ax=init('A revisada / alzado del puesto de dibujo',(12,8))
ax.add_patch(Rectangle((0,.75),1.8,.06,fc=blue,ec=ink));ax.plot([1.4,1.4],[.75,.81],color=bg,lw=2);ax.add_patch(Rectangle((1.9,.85),1.05,1.05,fc=pink,alpha=.7));ax.add_patch(Polygon([(1.9,.95),(1.45,1.05),(1.45,1.9),(1.9,1.8)],fc=pink,ec=ink));ax.text(.7,.4,'1,40 m inclinable',ha='center',fontsize=12);ax.text(1.6,.2,'0,40 fijo',ha='center',fontsize=11);ax.text(2.4,2.1,'moodboard lateral\nno invade tablero',ha='center',fontsize=12,color=ink)
ax.text(0,-.4,'Paneles representados en su plano desplegado para explicar la relación visual; posición real en planta.',fontsize=10,color=ink);ax.text(0,-.7,'Pivotes, bloqueos, cables y carga se reservan para desarrollo constructivo.',fontsize=10,color=ink);ax.set_xlim(-.2,4);ax.set_ylim(-1,2.7);save(fig,'03_ALZADO_MOODBOARD')
fig,ax=init('A revisada / sección local de la ventana habitable',(10,8))
ax.plot([0,2],[0,0],color=ink,lw=4);ax.add_patch(Rectangle((1.45,0),.55,.45,fc=blue,ec=ink));ax.plot([2,2],[.45,2.2],color=blue,lw=3);ax.plot([1.45,2],[2.2,2.2],color=ink,lw=3);ax.add_patch(Circle((1.62,1.22),.12,fill=False,ec=ink));ax.plot([1.62,1.68],[1.1,.65],color=ink);ax.plot([1.68,1.25],[.65,.5],color=ink);ax.plot([1.25,1.15],[.5,0],color=ink);ax.text(.1,2.5,'BANCO 1,40 × 0,55 m\ncota asiento 0,45 m',fontsize=14,color=ink);ax.text(0,-.6,'Hueco hacia el patio por verificar; privacidad, protección y carpintería pendientes.',fontsize=10,color=ink);ax.set_xlim(-.2,3.6);ax.set_ylim(-.9,3);save(fig,'04_SECCION_VENTANA')
report={'objects':len(check.Objects),'invalid':0,'room_contour_m2':21.27737814218625+.77,'shared_fragment_m2':16,'threshold_m2':6.4,'note':'No implantado ni repetido en unidad P02; no comprobacion normativa o luminica'};(P/'VERIFICACION.json').write_text(json.dumps(report,indent=2))
(P/'LEEME.md').write_text('''# A revisada · habitación y relación compartida\n\nPlanta, sección longitudinal, alzado del puesto y sección local de ventana. PNG y SVG editables. Rhino de estudio en metros con25+objetos esquemáticos y geometría válida.\n\nLa habitación crece a unos22,05m² de contorno incluido banco de ventana1,40x0,55. Mesa1,80x0,90:1,40m inclinable+0,40m fijo. Moodboard junto al lateral derecho, hoja orientable. CamaØ2,10m, plataformaØ2,20. Banco compartido fuera del paso lateral. Mesa colectiva2,40x1,10 en estancia de16m² y umbral6,4m².\n\nEl fragmento común se dibuja para discutir calidad y convivencia; no significa16m²porcada habitación ni resuelve cocina, baños o agrupación de cuatro. No implantado en P02 ni dimensionado estructuralmente. El perímetro y perfiles son de estudio. No simulación lumínica ni cumplimiento. El panel y la mesa tienen mecanismos pendientes; no mobiliario de fabricación.\n\nEl hueco de ventana y la envolvente norte son reservas: el Rhino no contiene carpintería terminada. El colchón redondo pide comprobar talla y disponibilidad. La franja de entrada permanece libre en los esquemas; revisar todo el recorrido con espesores definitivos.\n''')
print(report)
