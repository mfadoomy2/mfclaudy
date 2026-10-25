from pathlib import Path
import json,math,textwrap
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Ellipse,Rectangle,Polygon,PathPatch
from matplotlib.path import Path as MPath
P=Path(__file__).parent;bg='#fbfaf5';ink='#333e39';pink='#ce3885';cyan='#12aeb1';violet='#8055b3';gold='#d4a026';green='#4b9b70'
# Rectangular graphic support, NOT site or floor footprint. Manual hypotheses, editable.
nodes={'E':(3,35),'D1':(24,17),'D2':(76,17),'D3':(24,53),'D4':(76,53),'C':(51,35),'K':(54,58),'W':(29,35),'T':(75,34),'R':(47,12),'A':(50,45)}
labels={'E':'llegar / salir','D1':'retiro 1','D2':'retiro 2','D3':'retiro 3','D4':'retiro 4','C':'estar acompañadas','K':'preparar / comer','W':'mojar / secar','T':'desplegar / reparar','R':'guardar / mantener','A':'hablar en confianza'}
colors={'llegada':green,'concentracion':violet,'encuentro':pink,'recursos':cyan}
routes=[('S01','llegada',['E','W','R','D1']),('S02','llegada',['E','C','A']),('S03','concentracion',['E','D3']),('S04','concentracion',['D2','T','R']),('S05','encuentro',['K','C','W']),('S06','encuentro',['C','A']),('S07','recursos',['R','T','W']),('S08','llegada',['E','W','D4']),('S09','llegada',['D1','R','E']),('S10','encuentro',['E','A','C']),('S11','recursos',['D4','W','R']),('S12','concentracion',['D3','T']),('S13','encuentro',['E','C','D2']),('S14','recursos',['K','W','R']),('S15','llegada',['E','R','T']),('S16','llegada',['D1','W','D1'])]
(P/'NODOS_Y_RECORRIDOS.json').write_text(json.dumps({'frame':'100x70 unidades graficas; no metros ni limite de vivienda','positions':nodes,'labels':labels,'routes':routes,'placement':'Hipotesis manual; cuatro retiros reflejados sobre dos ejes; sin optimizacion ni comprobacion de distancias'},ensure_ascii=False,indent=2))
def setup(title,subtitle):
 f,a=plt.subplots(figsize=(16.54,11.69));f.patch.set_facecolor(bg);a.set_facecolor(bg);a.set_aspect('equal');a.set_xlim(-5,106);a.set_ylim(-12,80);a.axis('off');a.set_title(title,loc='left',fontsize=21,color=ink,pad=18);a.text(0,76,subtitle,fontsize=10,color=ink)
 # full fine lattice with cross points, for user-requested populated field
 for x in np.arange(0,101,2):a.plot([x,x],[0,70],color='#d5dcd4',lw=.28,zorder=0)
 for y in np.arange(0,71,2):a.plot([0,100],[y,y],color='#d5dcd4',lw=.28,zorder=0)
 xx,yy=np.meshgrid(np.arange(0,101,4),np.arange(0,71,4));a.scatter(xx,yy,s=2,color='#b3beb4',zorder=1)
 a.add_patch(Rectangle((0,0),100,70,fill=False,ec=ink,lw=.7));return f,a
def save(f,n):
 f.savefig(P/(n+'.png'),dpi=190,bbox_inches='tight',facecolor=bg);f.savefig(P/(n+'.svg'),bbox_inches='tight',facecolor=bg);plt.close(f)
def curve(a,seq,color,offset=0,alpha=.7,lw=1.2):
 pts=[nodes[n] for n in seq]
 for j,(p,q) in enumerate(zip(pts[:-1],pts[1:])):
  x,y=p;X,Y=q;dx=X-x;dy=Y-y;d=max(math.hypot(dx,dy),.01);nx=-dy/d;ny=dx/d;bend=offset+2.5*((j%2)*2-1)
  path=MPath([(x,y),(x+dx*.33+nx*bend,y+dy*.33+ny*bend),(x+dx*.68+nx*bend,y+dy*.68+ny*bend),(X,Y)],[MPath.MOVETO,MPath.CURVE4,MPath.CURVE4,MPath.CURVE4]);a.add_patch(PathPatch(path,fill=False,ec=color,lw=lw,alpha=alpha,zorder=3))
def points(a):
 for k,(x,y) in nodes.items():
  a.scatter([x],[y],s=45 if k[0]!='D' else 30,c=[pink if k in ['C','K','A'] else ink],edgecolors=bg,linewidths=.7,zorder=7);a.text(x+1.2,y+1.2,k+' / '+labels[k],fontsize=8,color=ink,zorder=8,bbox=dict(fc=bg,ec='none',pad=.6,alpha=.85))
def fields(a):
 for k in ['D1','D2','D3','D4']:
  x,y=nodes[k];a.add_patch(Ellipse((x,y),20,18,fc=violet,alpha=.055,ec=violet,lw=1,zorder=1));a.add_patch(Ellipse((x,y),14,12,fill=False,ec=violet,lw=.6,ls='--',alpha=.4))
 for k,w,h,c in [('C',31,22,pink),('K',24,17,gold),('T',23,16,cyan),('W',18,13,cyan),('A',17,12,pink),('R',23,12,green)]:
  x,y=nodes[k];a.add_patch(Ellipse((x,y),w,h,fc=c,alpha=.07,ec=c,lw=1,zorder=1))
f,a=setup('01 / Un tejido de cosas que pasan','Marco rectangular de trabajo: no es una planta. Puntos = acciones; hilos = secuencias; manchas = ámbitos provisionales de uso.')
fields(a)
for i,(id,typ,seq) in enumerate(routes):curve(a,seq,colors[typ],offset=(i%5-2)*1.8,alpha=.65,lw=1.1)
points(a)
for i,(k,c) in enumerate(colors.items()):a.plot([i*25,i*25+4],[-5,-5],color=c,lw=2);a.text(i*25+5,-5,k,va='center',fontsize=10,color=ink)
a.text(0,-9,'Los hilos se curvan para distinguir secuencias, no para diseñar pasillos. Cruce gráfico ≠ encuentro deseable.',fontsize=10,color=ink);save(f,'01_TEJIDO_GENERAL')
f,a=setup('02 / Al cruzarse, aparecen exigencias','Mismos puntos y soporte. Tres cruces se amplían como problemas espaciales; todavía no son habitaciones.')
fields(a)
for i in [2,4,3,7,6,14]:id,typ,seq=routes[i];curve(a,seq,colors[typ],offset=(i%3-1)*2,alpha=.8,lw=1.7)
points(a)
for label,center,txtpos,text in [('X1',(40,45),(4,73),'S03 × S05 / hablar en privado mientras otras cocinan'),('X2',(65,25),(42,-5),'S04 × S08 / dejar trabajo montado y permitir retirarse'),('X3',(58,17),(48,73),'S07 × S15 / reparar sin ocupar la llegada')]:
 x,y=center;a.add_patch(Circle(center,4,fill=False,ec=pink,lw=1.5));a.text(x,y,label,ha='center',va='center',fontsize=10,color=pink);a.annotate(text,center,txtpos,fontsize=9,color=ink,arrowprops=dict(arrowstyle='-',color=pink),bbox=dict(fc=bg,ec='none',pad=2))
a.text(0,-10,'Acceso, intimidad, sonido, humedad y luz definirán qué cruces se comparten, se separan o cambian de horario.',fontsize=10,color=ink);save(f,'02_CRUCES_QUE_PRODUCEN_LUGARES')
# Same coordinates across time, not different plans, select real scene subsets
for title,ids,name in [('09:00 / entrevista + desayuno',['S03','S05'],'03A_TIEMPO_MANANA'),('20:30 / comer + acompañar + retirarse',['S05','S10','S08'],'03B_TIEMPO_TARDE'),('01:20 / entrega + lavado + descanso',['S04','S11','S16'],'03C_TIEMPO_NOCHE')]:
 f,a=setup('03 / '+title,'Mismo marco y posiciones. Escena simultánea hipotética: la intensidad cambia; no obliga a ocupar todo a la vez.')
 fields(a)
 for i,(id,typ,seq) in enumerate(routes):
  curve(a,seq,colors[typ],offset=(i%5-2)*1.8,alpha=.85 if id in ids else .04,lw=2.2 if id in ids else .5)
 points(a);a.text(0,-6,'Secuencias activas: '+' · '.join(ids),fontsize=12,color=pink);a.text(0,-10,'Las personas y los horarios son ficticios, para contrastar. No datos observados ni simulación de ocupación.',fontsize=10,color=ink);save(f,name)
# physical use calibration separate from field; no arbitrary conversion of graphic units
f,a=plt.subplots(figsize=(16.54,11.69));f.patch.set_facecolor(bg);a.set_facecolor(bg);a.set_aspect('equal');a.set_xlim(-.4,10.5);a.set_ylim(-1.2,5.4);a.axis('off');a.set_title('04 / Cuerpos, objetos y movimientos dan tamaño al tejido',loc='left',fontsize=20,color=ink,pad=20)
# short-edge wall-mounted desk: hinge length 0.9 along y, reach1.8 x
for x in np.arange(0,10.1,.25):a.plot([x,x],[-.5,4.7],color='#d5dcd4',lw=.35)
for y in np.arange(-.5,4.71,.25):a.plot([0,10],[y,y],color='#d5dcd4',lw=.35)
a.plot([.3,.3],[.3,3.6],color=ink,lw=4);a.add_patch(Rectangle((.3,.6),1.8,.9,fc=cyan,alpha=.45,ec=ink));a.plot([.3,.3],[.6,1.5],color=pink,lw=5);a.add_patch(Rectangle((.8,1.5),.9,.9,fill=False,ec=cyan,ls='--'));a.add_patch(Circle((1.25,1.95),.2,fc=cyan));a.text(.3,3.95,'DIBUJAR / tablero 1,80 × 0,90 m',fontsize=11,color=ink);a.text(.45,.9,'canto corto\ncontra pared',fontsize=9,color=ink);a.text(.3,.05,'Reserva de cuerpo por comprobar\ncon altura y mecanismo reales',fontsize=9,color=ink)
a.add_patch(Circle((4.5,1.5),1.05,fc='#e4c999',ec=ink));a.add_patch(Circle((4.5,1.5),1.6,fill=False,ec=violet,ls='--'));a.text(4.5,1.5,'COLCHÓN\nØ 2,10 m',ha='center',va='center',fontsize=11,color=ink);a.text(3.2,3.95,'DORMIR / comprobar acceso y ropa',fontsize=11,color=ink);a.text(3.1,-.45,'Anillo discontinuo: ensayo de paso,\nno un margen normativo',fontsize=9,color=ink)
a.add_patch(Ellipse((8,1.6),1.5,.8,fc=pink,alpha=.4,ec=ink));
for xx,yy in [(7.3,.8),(8.7,.8),(8,2.55)]:a.add_patch(Circle((xx,yy),.24,fc=pink,alpha=.4))
a.text(6.65,3.95,'ESTAR / 3 cuerpos + apoyo',fontsize=11,color=ink);a.text(6.65,-.45,'No equivale a una sala equipada:\ncomprobar posturas y paso alrededor.',fontsize=9,color=ink)
a.text(.1,-1.05,'Esta lámina sí usa metros. El marco de puntos anterior no tiene escala métrica asignada. Retícula: 0,25 m.',fontsize=10,color=ink);save(f,'04_CALIBRACION_CORPORAL')
(P/'IDEA_FUTURA_COMPLEJO_SOL.md').write_text('''# Línea futura: forma solar del complejo\nIdea de Adam, guardada18.10.2026. No desarrollar ahora: prioridad unidad.\n\nExplorar una geometría que se recorte, separe, gire y escalone para repartir mejor el acceso a luz, arrancando esbelta y abriéndose arriba como hipótesis. Telas protagonistas como regulación y expresión. El gráfico solar previo por altura no es una silueta edificable ni dice dónde recortar: hace falta mapa3D de cielo, vecinos y nuevas unidades. Evaluar especialmente viviendas peor expuestas, verano, circulación, estructura y límites de parcela. No imponer el complejo longitudinal anterior.\n\nEste archivo está en la carpeta de proyecto. No se ha creado ni reorganizado un vault de Obsidian ni actualizado memorias globales.\n''')
(P/'LEER_PRIMERO.md').write_text('''# Unidad · tejido de actividades\n\nSeis láminas PNG+SVG. No modifica Rhino ni propone perímetro de vivienda. Marco100x70unidades gráficas con retícula: soporte para cruzar situaciones, no parcela ni metros. Nodos y recorridos son hipótesis manuales editables enJSON; las curvas distinguen secuencias y no son pasillos ni trayectorias medidas. Radios de manchas elegidos para lectura gráfica, no áreas calculadas. No optimización o simulación.\n\n01: campo general.02: tres conflictos que necesitan proyecto.03A/B/C: mismos puntos por mañana, tarde y noche.04: calibración de cuerpo/objeto en metros, separada del soporte abstracto. Los cuatro retiros están reflejados sobre dos ejes como regla de arranque; no hay cuatro cuartos ya definidos. El resto de actividades puede romper esa simetría, a discutir.\n\nE=entrada/salida; D1..D4=retiros; C=estar; K=preparar/comer; W=humedad/secado; T=trabajo/reparación; R=almacenamiento/mantenimiento; A=conversación reservada. No es una habitación por nodo: algunos lugares se compartirán por horario y otros se distribuirán.\n\nS01..S16 remiten a las situaciones ficticias del mapa anterior, no entrevistas. Relación con Acampada es temática; no observaciones de estas personas. La geometría de cada lugar deberá crecer desde usos medidos, y sus separaciones comprobar sonido, intimidad, luz, ventilación y movimiento. Se necesita redibujar relaciones si al dimensionarlas no caben; no comprimir cuerpos para salvar un diagrama.\n\nRegla de transición a planta: ubicar eventos; calibrar envolventes de uso; superponer actividades compatibles; separar incompatibles; reservar acceso continuo; ajustar geometría; comprobar luz y construcción. El próximo resultado aún no es una planta acabada.\n\nLa idea solar del complejo se guarda en IDEA_FUTURA_COMPLEJO_SOL.md sin desarrollarla. No se trabaja en Obsidian.\n''')
print('6 laminas PNG+SVG; modelo sin modificar')
