from pathlib import Path
import math,json
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,Polygon,FancyBboxPatch,Arc
P=Path(__file__).parent;bg='#f6f3e9';ink='#24594e';blue='#68a7b5';pink='#b7789c';green='#d9e4ce';gold='#d7b56f'
def start(title,size=(14,12)):
 f,a=plt.subplots(figsize=size);f.patch.set_facecolor(bg);a.set_facecolor(bg);a.set_aspect('equal');a.axis('off');a.set_title(title,loc='left',fontsize=18,pad=25,color=ink);return f,a
def save(f,n):
 for ext in ['png','svg']:f.savefig(P/(n+'.'+ext),dpi=170,bbox_inches='tight')
 plt.close(f)
def txt(a,t,x,y,sz=10):a.text(x,y,t,ha='center',va='center',fontsize=sz,color=ink)
def arrow(a,pts,c=ink):
 a.plot(*zip(*pts),color=c,lw=2);a.annotate('',pts[-1],pts[-2],arrowprops=dict(arrowstyle='->',color=c,lw=2))
rooms=[(-6.2,-2,False,'H1'),(2.2,-2,False,'H2'),(-6.2,4.9,True,'H3'),(2.2,4.9,True,'H4')]
f,a=start('P02 / cuatro refugios y una sala compartida · ensayo de planta completa')
# common geometry separate from bedrooms
common=[(-2.2,-2.2),(2.2,-2.2),(2.2,1.9),(6.5,1.9),(6.5,4.9),(2.2,4.9),(2.2,9),(-2.2,9),(-2.2,4.9),(-7.8,4.9),(-7.8,1.9),(-2.2,1.9)]
a.add_patch(Polygon(common,fc='#e7e4d2',ec=ink,lw=2));a.add_patch(Rectangle((-7.8,2.75),14.3,1.3,fc='#c2dac7',alpha=.7));txt(a,'FRANJA DE ACCESO LIBRE / 1,30 m nominal',-.2,3.38,10)
for x,y,north,name in rooms:
 a.add_patch(FancyBboxPatch((x,y),4,3.9,boxstyle='round,pad=0,rounding_size=.55',fc='#e0e6d9',ec=ink,lw=2))
 # beds away from room door; desk on opposite outer frontage
 bx=x+1.3 if x<0 else x+2.7;by=y+2.7
 a.add_patch(Circle((bx,by),1.1,fc='#ddbf8d',ec=ink));a.add_patch(Circle((bx,by),1.05,fc='#fffdf5',ec=ink));txt(a,'Ø2,10',bx,by,9)
 dx=x+2 if x<0 else x+.2;dy=y+.15
 a.add_patch(Rectangle((dx,dy),1.8,.9,fc=blue,ec=ink));a.plot([dx+1.4,dx+1.4],[dy,dy+.9],color=bg,lw=2);a.plot([dx+1.86,dx+1.86],[dy,dy+.85],color=pink,lw=3)
 sy=dy+1.35;a.add_patch(Circle((dx+.9,sy),.2,fc=blue))
 # niches projecting towards exterior sides, private entrance at inner edge of common cross
 cx=x if x<0 else x+4;cy=y+2 if not north else y+1.9
 a.add_patch(Arc((cx,cy),1.2,1.5,theta1=90 if x<0 else -90,theta2=270 if x<0 else 90,color=pink,lw=5))
 doorx=(x+.65 if x<0 else x+3.35) if north else (x+3.1 if x<0 else x+.9);doory=y if north else y+3.9;a.plot([doorx-.5,doorx+.5],[doory,doory],color=bg,lw=7)
 txt(a,name,x+2,y+1.95,13);arrow(a,[(doorx,3.4),(doorx,doory+(.35 if north else -.35))],pink)
 # frontage light proposals
 yy=y+3.9 if north else y;a.plot([dx,dx+1.8],[yy,yy],color=blue,lw=5)
# living pocket and kitchen
zone=FancyBboxPatch((-2.05,4.2),4.1,2.55,boxstyle='round,pad=0,rounding_size=.65',fc=green,ec=ink,lw=1);a.add_patch(zone);txt(a,'SALA DE ESTAR\nindependiente de la cocina',0,5.7,12);a.plot([-.9,.9],[4.95,4.95],color=pink,lw=9);txt(a,'asientos por desarrollar',0,4.5,8)
a.add_patch(Rectangle((-2.05,7.1),4.1,1.75,fc='#eee0bc',ec=ink));a.add_patch(Rectangle((-1.95,8.2),3.9,.6,fc=gold));a.add_patch(Rectangle((-.9,7.25),1.8,.75,fc=blue));txt(a,'COCINA + COMER',0,7.95,10)
# wet rooms
for x in [-2.1,.1]:a.add_patch(Rectangle((x,-2.1),2,2.3,fc='#dfcede',ec=ink));txt(a,'BAÑO\nreserva',x+1,-.95,10)
txt(a,'DISTRIBUCIÓN / sin muebles',0,1,9)
arrow(a,[(-8.4,3.4),(-5.8,3.4),(-.3,3.4)]);txt(a,'ENTRADA Y SALIDA\npor conexión oeste V4',-8,5.5,10);a.plot([-7.2,-7.2],[1.9,4.9],ls='--',color=ink);txt(a,'adaptación del\nramal pendiente',-7.7,.7,9)
a.add_patch(Rectangle((-6.2,-2.1),12.4,9.05,fill=False,ec='#b66946',ls='--',lw=1.7));txt(a,'Discontinuo naranja: caja envolvente de la plataforma V4 (referencia, no límite aprobado)',0,-3.05,10)
a.plot([0,0],[-2.4,9.3],ls='-.',color='#b66946');txt(a,'1—1',0,9.6);a.plot([-6.6,6.6],[6.8,6.8],ls='-.',color='#b66946');txt(a,'2—2',7,6.8)
txt(a,'Cada habitación: 4,00 × 3,90 m de caja antes de curvas/espesores. No son 22 m²; se ha recompactado el ensayo.',0,-3.6,10);txt(a,'No implantado en parcela. La ampliación exige revisar estructura, separaciones y programa. Mobiliario esquemático.',0,-4.05,10)
a.set_xlim(-9.7,8);a.set_ylim(-4.6,10);save(f,'01_PLANTA_UNIDAD_COMPLETA')
# actual existing slab comparisons in longitudinal section local to P02 front
s=json.load(open(P.parent/'G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/calculo/ESTRUCTURA_RESULTADOS.json'));p2=s['plates'][1];p3=s['plates'][2];p4=s['plates'][3]
f,a=start('P02 / sección 1—1 · la plataforma superior condiciona la luz',(15,9))
a.plot([-2.2,9],[9.4,9.4],color=ink,lw=5);a.plot([-2.2,-2.2],[9.4,12.15],color=ink,lw=3);roof=[(-2.2,12.15),(1.9,12.3),(4.2,12.3),(5.4,13.25),(6.3,13.25),(7,12.3),(9,12.3)];a.plot(*zip(*roof),color=ink,lw=4);a.plot([5.4,6.3],[13.25,13.25],color=blue,lw=6)
for p in [p3,p4]:
 yy=[pt[1]-p2['front'] for pt in p['outline']];a.add_patch(Rectangle((min(yy),p['z']-.22),max(yy)-min(yy),.22,fc='#98a29c'));txt(a,p['id']+' / plataforma V4',1,p['z']+.35,11)
a.add_patch(Rectangle((7.25,10.15),.75,.06,fc=blue));a.plot([9,9],[9.4,12.3],color=blue,lw=4);txt(a,'sala',5.4,10.3,12);txt(a,'cocina',8,10.7,11);txt(a,'baños',-1,10.3,11);txt(a,'paso',3.2,9.85,10)
arrow(a,[(5.85,13.25),(5.85,14.78)],'#b65a4d');txt(a,'HUECO CENTRAL:\nP03 lo obstruye',3.4,13.6,11);arrow(a,[(10.5,14.5),(9.02,11.7),(7.2,10.8)],'#b59439');txt(a,'Captación lateral propuesta\nrequiere estudiar vecinos y P05/P08',11,15.8,10)
a.set_xlim(-3,13);a.set_ylim(8.7,22);a.set_yticks([9.4,15,20.6]);a.yaxis.set_visible(True);a.spines[['top','right','bottom']].set_visible(False);a.spines['left'].set_visible(True);a.set_ylabel('Z absoluta / m',color=ink);txt(a,'Posiciones de plataformas leídas del modelo V4. Cubierta nueva hipotética; flechas no son simulación solar.',4.3,8.9,10);save(f,'02_SECCION_OBSTRUCCION_REAL')
f,a=start('P02 / sección 2—2 · abrir la sala hacia el borde norte',(15,8))
a.plot([-6.2,6.2],[9.4,9.4],color=ink,lw=4);a.plot([-6.2,-2.2,0,2.2,6.2],[12.2,12.2,13.25,12.2,12.2],color=ink,lw=4)
# P03 x range true relative center P02
xs=[q[0]-p2['cx'] for q in p3['outline']];a.add_patch(Rectangle((min(xs),14.78),max(xs)-min(xs),.22,fc='#98a29c'));txt(a,'P03 sobre P02 / posición real V4',0,15.4,12)
for x in [-4.9,4.9]:a.add_patch(Rectangle((x-.68,9.62),1.36,.22,fc='#fffdf5',ec=ink));txt(a,'habitación',x,10.6,11)
txt(a,'sala',0,10.6,12);a.plot([-2.1,2.1],[11.4,11.4],color=blue,lw=4);txt(a,'hueco de fachada hacia +Y\n(ver planta y sección longitudinal)',0,11.9,10)
txt(a,'Las cuatro habitaciones conservan huecos propios. No se propone iluminarlas a través de la sala.',0,8.6,11);a.set_xlim(-7.5,7.5);a.set_ylim(8,16);save(f,'03_SECCION_SALA_HABITACIONES')
(P/'LEEME.md').write_text('''# P02 · unidad orgánica / ensayo de organización completa\n\nTres dibujos PNG+SVG. Se vuelve al acceso oeste V4: ramal a ylocal2,75..4,05m, cota9,40m. En esta propuesta el cruce compartido permite llegar a las cuatro habitaciones, baños, sala y cocina. La conexión oeste necesita adaptación geométrica; no se certifica continuidad o evacuación. No se inventa segunda salida. Banco de acceso eliminado.\n\nCuatro habitaciones en cajas4x3,9m con esquinas curvas y reservas de ropa, camaØ2,10 y mesa1,80x0,90. Recompactación del ensayo22m²; no son aquellos dormitorios completos trasplantados. La ropa y mobiliario requieren comprobación de uso. Sala separada de cocina. Acceso central sin muebles; asientos de sala fuera de la franja verde.\n\nAUMENTO IMPORTANTE: la nueva organización supera el cuerpo domésticoV4 de65,28m² y su plataforma de110,53m². No está implantada en parcela ni conectada o calculada estructuralmente. Se compara la caja envolvente de plataforma V4 con la nueva planta para no ocultarlo. Si esta organización se elige, habrá que redimensionar la macroestructura y posiblemente reducir número de unidades; no afirmar que cabe.\n\nSecciones: P03z15,00 y P04z20,60, coordenadas reales del resultado estructuralV4; P02z9,40. La sección longitudinal evidencia que el lucernario central queda bajo P03. Se propone buscar apertura lateral norte en el tramo de sala/cocina que sobresale, pero aún no se ha comparado con vecinos ni con unidades de otros árboles. No prueba suficiencia de luz. La cubierta es una hipótesis y las flechas ilustrativas. No cumplimiento urbanístico, estructural, térmico, lumínico o de accesibilidad.\n''')
print('3 dibujos completos PNG+SVG')
