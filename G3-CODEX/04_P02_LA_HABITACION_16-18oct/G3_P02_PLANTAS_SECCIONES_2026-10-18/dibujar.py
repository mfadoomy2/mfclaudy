from pathlib import Path
import math,json
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Rectangle,Circle,Arc
P=Path(__file__).parent
bg='#f6f3e9';ink='#23594e';bed='#e1bd87';blue='#67a9b7';pink='#b7789c';green='#acd1b8'
variants=[dict(id='A',name='Cresta sobre el dibujo',w=4,h=4.8,bed=(2.65,3.55),desk=(1.65,.18),niche=1.15,win=False,roof=[(0,2.75),(.2,3.05),(1.3,3.65),(1.65,3.65),(2.1,2.9),(4.8,2.75)]),dict(id='B',name='Ventana para habitar',w=4.4,h=4.8,bed=(3.05,3.55),desk=(.18,1.6),niche=.95,win=True,roof=[(0,2.7),(2.8,2.8),(3.6,3.3),(4.8,3.3)]),dict(id='C',name='Dos alas y un centro libre',w=4.6,h=4.6,bed=(3.4,3.35),desk=(.18,.18),niche=1.05,win=True,roof=[(0,3.45),(.65,3.45),(1.3,2.8),(2.6,2.65),(3.4,3.1),(4.6,3.1)])]

def dim(ax,p,q,label,off=.2):
 ax.annotate('',q,p,arrowprops=dict(arrowstyle='|-|',color=ink,lw=.8));x=(p[0]+q[0])/2;y=(p[1]+q[1])/2;ax.text(x,y-off,label,ha='center',va='top',fontsize=9,color=ink,bbox=dict(fc=bg,ec='none',pad=1))
def setup(title):
 fig,ax=plt.subplots(figsize=(12,10));fig.patch.set_facecolor(bg);ax.set_facecolor(bg);ax.set_aspect('equal');ax.axis('off');ax.set_title(title,loc='left',fontsize=20,pad=25,color=ink);return fig,ax
def save(fig,name):
 fig.savefig(P/(name+'.png'),dpi=170,bbox_inches='tight',facecolor=bg);fig.savefig(P/(name+'.svg'),bbox_inches='tight',facecolor=bg);plt.close(fig)
def tag(ax,text,p,q):ax.annotate(text,p,q,fontsize=10,color=ink,arrowprops=dict(arrowstyle='-',color=ink),bbox=dict(fc=bg,ec='none',pad=2))
def plan(v):
 w,h=v['w'],v['h'];fig,ax=setup(f"{v['id']} / {v['name']} · planta")
 r=v['niche'];cy=1.95;arc=[(w+r*math.cos(t),cy+r*math.sin(t)) for t in np.linspace(-math.pi/2,math.pi/2,65)];outline=[(0,0),(w,0),(w,cy-r)]+arc[1:]+[(w,h),(0,h)]
 ax.add_patch(Polygon(outline,fc='#e4e3d3',ec=ink,lw=3))
 bx,by=v['bed'];ax.add_patch(Circle((bx,by),1.1,fc=bed,ec='#a27d50'));ax.add_patch(Circle((bx,by),1.05,fc='#fffdf5',ec='#a27d50'));ax.text(bx,by,'CAMA\nØ 2,10',ha='center',va='center',fontsize=12)
 dx,dy=v['desk'];rot=v['id']=='B';dw,dd=(.9,1.8) if rot else (1.8,.9)
 ax.add_patch(Rectangle((dx,dy),dw,dd,fc=blue,ec=ink,lw=.8));ax.text(dx+dw/2,dy+dd/2,'DIBUJO\n1,80 × 0,90',ha='center',va='center',fontsize=10,rotation=90 if rot else 0)
 sx,sy=(dx+1.35,dy+.9) if rot else (dx+.9,dy+1.35);ax.add_patch(Circle((sx,sy),.21,fc=blue));ax.add_patch(Rectangle((sx-.45,sy-.45),.9,.9,fill=False,ec=blue,ls='--'));ax.text(sx,sy-.65,'reserva de uso',ha='center',fontsize=8,color=ink)
 ax.add_patch(Arc((w,cy),2*(r-.28),2*(r-.28),theta1=-80,theta2=80,color=pink,lw=5));tag(ax,'NICHO DE ROPA\nbarra curva + cierre pendiente',(w+r-.25,cy),(w+r+.3,cy+.5))
 # door shifts to left except C where desk occupies left
 door=(.25,1.25) if v['id']!='C' else (2.15,3.15)
 ax.plot(door,[0,0],color=bg,lw=8);ax.annotate('',(sum(door)/2,.75),(sum(door)/2,-.45),arrowprops=dict(arrowstyle='->',lw=2,color=ink));ax.text(sum(door)/2,-.65,'ENTRADA 1,00 m',ha='center',fontsize=9)
 if v['id']=='A':
  ax.add_patch(Rectangle((.22,.15),1.05,4.2,fc=green,alpha=.4));ax.text(.74,2.5,'PASO LATERAL',rotation=90,ha='center',fontsize=9,color=ink)
 else:
  ax.annotate('',(2.1,2.05),(sum(door)/2,.35),arrowprops=dict(arrowstyle='->',lw=3,color=green));ax.text(2.05,2,'CENTRO LIBRE',ha='center',fontsize=9,color=ink)
 if v['win']:
  wx=.25 if v['id']=='B' else .3
  ax.add_patch(Rectangle((wx,h),1.5,.65,fc='#d0e8df',ec=ink,lw=2));ax.text(wx+.75,h+.3,'VENTANA / BANCO',ha='center',fontsize=8)
 else:ax.plot([.4,1.6],[h,h],color=blue,lw=5)
 # integrated headboard, wall trays, split drafting board and panel movement
 ax.add_patch(Arc((bx,by),2.3,2.3,theta1=15,theta2=160,color=pink,lw=6))
 for ty in [by-.35,by+.15]:ax.add_patch(Rectangle((w-.36,ty),.32,.25,fc=blue,ec=ink,lw=.7))
 if rot:
  ax.plot([dx,dx+dw],[dy+1.4,dy+1.4],color=bg,lw=2)
 else:ax.plot([dx+1.4,dx+1.4],[dy,dy+dd],color=bg,lw=2)
 ax.plot([.1,.65],[3.1,3.45],color=pink,lw=2);ax.add_patch(Arc((.1,3.1),1.1,1.1,theta1=0,theta2=90,color=pink,ls='--'))
 tag(ax,'CABECERO + BANDEJAS / luz y carga',(bx+.7,by+.7),(w+.6,h+.7))
 ax.text(dx,dy-.17,'1,40 inclinable + 0,40 fijo',fontsize=8,color=ink)
 # pin up along west wall, fold movement hint
 ax.plot([.1,.1],[3.1,4.2],color=pink,lw=4);tag(ax,'PANELES PARA PLANOS',(.1,3.6),(-1.65,3.9))
 ax.plot([w-.4,w+r+.1],[cy,cy],ls='-.',color='#b56b4b',lw=1);ax.text(w+r+.15,cy,'3—3',fontsize=9,color='#b56b4b')
 # section traces correspond x=deskcenter, y=bedcenter
 cutx=dx+dw/2;ax.plot([cutx,cutx],[-.15,h+.15],ls='-.',color='#b56b4b',lw=1);ax.text(cutx,h+.8,'1—1 / dibujo y cubierta',ha='center',fontsize=9,color='#b56b4b')
 ax.plot([-.15,w+.15],[by,by],ls='-.',color='#b56b4b',lw=1);ax.text(w+.25,by,'2—2',fontsize=9,color='#b56b4b')
 dim(ax,(0,-.95),(w,-.95),f'{w:.2f} m');area=w*h+math.pi*r*r/2+(1.5*.65 if v['win'] else 0)
 ax.text(-.5,-1.65,f'Contorno geométrico: {area:.2f} m² · cama y tablero a escala · espesores por desarrollar',fontsize=10,color=ink)
 ax.text(-.5,-1.95,'Ensayo aislado de habitación / no implantado en P02 / luz propuesta, sin simulación',fontsize=9,color=ink)
 ax.set_xlim(-1.8,w+r+2);ax.set_ylim(-2.2,h+1.1);save(fig,v['id']+'_01_PLANTA');return area

def section1(v):
 h=v['h'];fig,ax=setup(f"{v['id']} / sección 1—1 · mesa y entrada de luz")
 roof=v['roof'];ax.plot([0,h],[0,0],color=ink,lw=5);ax.plot([0,0],[0,roof[0][1]],color=ink,lw=3);ax.plot([h,h],[0,roof[-1][1]],color=ink,lw=3)
 ax.plot(*zip(*roof),color=ink,lw=5);ax.plot([p[0] for p in roof],[p[1]+.14 for p in roof],color=ink,lw=1)
 if v['win']:
  ax.add_patch(Rectangle((h,.45),.65,.12,fc=blue));ax.plot([h+.65,h+.65],[.57,2.2],color=blue,lw=2);ax.plot([h,h+.65],[2.2,2.2],color=ink,lw=2);ax.text(h+.3,2.35,'banco',ha='center',fontsize=9)
 if v['id']=='B':
  # longitudinal cut intersects rotated desk; actual length along y
  start=1.6;end=3.4;ax.add_patch(Rectangle((start,.75),end-start,.05,fc=blue));ax.plot([start,start],[.75,1.65],color=blue,ls='--');seatx=2.5
 else:
  start=.18;end=1.08;ax.add_patch(Rectangle((start,.75),end-start,.05,fc=blue));ang=math.radians(35);ax.plot([start,start+.9*math.cos(ang)],[.75,.75+.9*math.sin(ang)],color=blue,lw=3);ax.plot([start,start],[.75,1.65],color=blue,ls='--');seatx=1.53
 ax.add_patch(Rectangle((seatx-.2,.43),.4,.05,fc=blue));ax.plot([seatx,seatx],[0,.43],color=blue)
 # selected roof opening
 if v['id']=='A':p,q=(.25,3.08),(1.25,3.62)
 elif v['id']=='B':p,q=(3.6,3.3),(4.75,3.3)
 else:p,q=(.08,3.45),(.62,3.45)
 ax.plot([p[0],q[0]],[p[1],q[1]],color='#72bfc5',lw=6)
 for t in [.25,.65]:
  x=p[0]+t*(q[0]-p[0]);z=p[1]+t*(q[1]-p[1]);ax.annotate('',(max(.4,x-.6),.9),(x,z-.12),arrowprops=dict(arrowstyle='->',color='#c5a343',lw=1.3))
 tag(ax,'LUZ CENITAL / dirección por verificar',q,(2,4.05));tag(ax,('tablero / corte longitudinal\nplegado discontinuo esquemático' if v['id']=='B' else 'tablero horizontal + inclinación 35°\nplegado discontinuo / mecanismo pendiente'),(end,.8),(1.8,-.7))
 dim(ax,(h+.35,0),(h+.35,max(z for _,z in roof)),f"máx. {max(z for _,z in roof):.2f} m",off=.1)
 ax.text(0,-1.25,'Corte por el eje del tablero. Flechas de luz ilustrativas; sin prueba de obstrucción del conjunto.',fontsize=10,color=ink)
 ax.set_xlim(-.5,h+1.4);ax.set_ylim(-1.5,4.5);save(fig,v['id']+'_02_SECCION_DIBUJO')
def section2(v):
 w=v['w'];fig,ax=setup(f"{v['id']} / sección 2—2 · cama, intimidad y pared")
 by=v['bed'][1];height=float(np.interp(by,[p[0] for p in v['roof']],[p[1] for p in v['roof']]));ax.plot([0,w],[0,0],color=ink,lw=5);ax.plot([0,0],[0,height],color=ink,lw=3);ax.plot([w,w],[0,height],color=ink,lw=3);ax.plot([0,w],[height,height],color=ink,lw=4)
 bx=v['bed'][0];ax.add_patch(Rectangle((bx+.83,0),.15,1.05,fc=pink,ec=ink));ax.add_patch(Rectangle((bx-1.1,0),2.2,.22,fc=bed,ec=ink));ax.add_patch(Rectangle((bx-1.05,.22),2.1,.22,fc='#fffdf5',ec=ink));ax.add_patch(Rectangle((w-.32,.55),.32,.025,fc=blue));ax.add_patch(Rectangle((w-.32,.8),.32,.025,fc=blue));ax.plot([.12,.12],[.8,2.1],color=pink,lw=4)
 dim(ax,(0,-.3),(bx-1.1,-.3),f'{bx-1.1:.2f} m hasta plataforma')
 tag(ax,'DOS BANDEJAS METÁLICAS\ncarga e iluminación por resolver',(w-.2,.8),(w+.35,1.3));tag(ax,'PANEL PARA PLANOS / giro por estudiar',(.12,1.5),(-.2,3.8));ax.text(bx,.65,'colchón Ø 2,10 / plataforma Ø 2,20',ha='center',fontsize=10)
 ax.text(0,-1,'La altura corresponde al perfil de cubierta de esta variante en la posición del corte.',fontsize=10,color=ink);ax.text(0,-1.3,'No representa una comprobación estructural, acústica, de habitabilidad ni de accesibilidad.',fontsize=9,color=ink)
 ax.set_xlim(-.5,w+2.5);ax.set_ylim(-1.5,4.3);save(fig,v['id']+'_03_SECCION_CAMA')
def section3(v):
 fig,ax=setup(f"{v['id']} / sección 3—3 · vestirse, exponer y cerrar")
 r=v['niche'];w=v['w'];ax.plot([0,2.4+r],[0,0],color=ink,lw=4);ax.plot([2.4+r,2.4+r],[0,2.7],color=ink,lw=4);ax.plot([0,2.4+r],[2.7,2.7],color=ink,lw=4)
 ax.add_patch(Rectangle((2.4+r-.6,.35),.55,1.35,fc=pink,alpha=.6));ax.plot([2.4+r-.45,2.4+r-.15],[1.75,1.75],color=ink,lw=3);ax.text(2.4+r-.3,1.95,'barra',ha='center',fontsize=10)
 ax.plot([2.4,2.4],[0,2.3],color=pink,ls='--');ax.text(2.4,-.25,'cierre curvo / espejo en una hoja',ha='center',fontsize=10,color=ink)
 ax.add_patch(Circle((1.9,1.58),.12,fill=False,ec=ink));ax.plot([1.9,1.9],[.75,1.46],color=ink);ax.plot([1.9,1.6],[.75,0],color=ink);ax.plot([1.9,2.1],[.75,0],color=ink);ax.plot([1.9,2.35],[1.15,1.35],color=ink)
 ax.annotate('luz de probador / sin diseño eléctrico',(2.4+r-.12,2.45),(.2,3.3),arrowprops=dict(arrowstyle='-',color=ink),fontsize=11,color=ink)
 dim(ax,(2.4,-.65),(2.4+r,-.65),f'nicho R {r:.2f} m')
 ax.text(0,-1.2,'Corte radial esquemático del nicho: reserva 0,60 m para ropa; curvatura visible en planta.',fontsize=10,color=ink)
 ax.set_xlim(-.2,5.2);ax.set_ylim(-1.5,3.7);save(fig,v['id']+'_04_SECCION_ARMARIO')
areas={}
for v in variants:areas[v['id']]=plan(v);section1(v);section2(v);section3(v)
(P/'DATOS_VARIANTES.json').write_text(json.dumps({'variants':variants,'areas_contorno':areas,'status':'Hipotesis espacial independiente. Dimensiones nominales. No implantado en P02.'},indent=2))
from PIL import Image,ImageDraw
files=sorted(f for f in P.glob('?_0*.png') if not f.name.startswith('._'));sheet=Image.new('RGB',(2800,1800),bg);draw=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
 im=Image.open(f);im.thumbnail((690,570));sheet.paste(im,((i%4)*700,(i//4)*600));
sheet.save(P/'00_COMPARATIVA_TRES_VARIANTES.png')
(P/'LEEME.md').write_text('''# Tres ensayos de habitación P02\n\n12 dibujos: tres plantas y nueve secciones, en PNG y SVG editable. Cortes identificados en planta. Todos son ensayos aislados derivados de la conversación; no modificaciones de la P02 V4 ni simulaciones de luz. Se conserva el concepto cama circular2,10m, plataforma2,20m y mesa1,80x0,90m.\n\nA: mantiene paso lateral y concentra una cresta cenital sobre dibujo. B: gira la mesa hacia pared oeste y añade una ventana habitable al norte. C: entrada central entre mesa y cama, techo con dos alturas y banco de ventana. El nicho de ropa sobresale al este en las tres. Las áreas son de contorno geométrico sin desarrollo de espesores ni cerramientos. No extrapolar cuatro veces para dimensionar la unidad.\n\nLas posiciones de corte comparten coordenadas con las plantas. La sección de dibujo B atraviesa la longitud del tablero, por eso mide1,80m; en A/C atraviesa su fondo0,90m. Tablero inclinado y plegado son estados alternativos. No hay mecanismos resueltos, cálculo estructural, iluminación interior ni comprobación normativa. Los paneles y bandejas son esquemas. Las flechas de luz no son trazados solares calculados.\n\nPreferencia inicial A por recorrido directo y separación entre entrada, cama y trabajo. B prueba acercar el dibujo al lateral iluminado, pero su conexión con ventana necesita comprobar el cielo real. C integra más el centro y exige revisar privacidad desde puerta y espacio ocupado por persona sentada. Comparar a escala antes de integrar en P02.\n''')
print(areas)
