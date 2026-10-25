import geometria as G
import matplotlib.pyplot as plt
from shapely.geometry import Point,LineString,box
P=G.P;L=P/'laminas';fig,axs=plt.subplots(1,3,figsize=(19,10),facecolor='#faf8f2')
for i,ax in enumerate(axs[:2]):
 G.draw(ax,G.ROOM,G.C['private'])
 for k,g in G.FURN.items():
  if i==1 and k in ['mesa_A1','taburete_en_uso']:continue
  G.draw(ax,g,G.C['ward'] if k=='vestidor' else G.C['seat'] if k=='bow_asiento' else G.C['desk'] if k in ['mesa_A1','taburete_en_uso'] else G.C['bed'],ec='#697d6e')
 if i==1:
  G.draw(ax,box(.07,.10,.12,1.0),G.C['desk']);G.draw(ax,Point(.65,.7).buffer(.23),G.C['desk']);G.line(ax,G.DESK.boundary,'#91a496',.6,'--')
 G.draw(ax,G.ROOM.boundary.buffer(.06).difference(G.DOOR).difference(G.WIN),G.C['wall']);G.draw(ax,G.WIN,G.C['glass']);G.line(ax,G.TEXTILE,G.C['seat'],1,'--')
 G.line(ax,LineString([(2.6,-.2),(2.6,1.5),(2.4,3.55)]),G.C['route'],1,'--');G.line(ax,LineString([(2.6,3.1),(3.65,3.1)]),G.C['route'],1,'--')
 for pt in G.TARGETS.values():ax.add_patch(plt.Circle(pt,.18,fill=False,color='#af4e65',lw=.7))
 G.txt(ax,.88,3.,'cama\n1,25 x 2,00',8);G.txt(ax,.9,.5,'mesa\n1,80 x 0,90' if i==0 else 'mesa\nrecogida',8);G.txt(ax,3.65,3.1,'vestirse',8);G.txt(ax,1.8,4.6,'bow',8)
 ax.set_xlim(-.45,5.1);ax.set_ylim(-.6,5.4);ax.set_aspect('equal');ax.axis('off');ax.set_title('01 / MESA ABIERTA' if i==0 else '02 / MESA RECOGIDA',loc='left',fontsize=12)
ax=axs[2];G.draw(ax,G.ROOM,G.C['private']);G.draw(ax,G.WARD,G.C['ward']);G.draw(ax,G.ROOM.boundary.buffer(.06).difference(G.DOOR).difference(G.WIN),G.C['wall'])
ax.add_patch(plt.Circle((3.65,3.1),.20,fill=False,color='#af4e65'))
G.line(ax,LineString([(3.25,3.1),(4.15,3.1)]),'#263d35',.8);G.txt(ax,3.6,2.8,'radio libre\n0,90 m',9)
G.line(ax,LineString([(4.15,3.1),(4.7,3.1)]),'#263d35',.8);G.txt(ax,4.47,3.48,'ropa\n0,55 m',9)
ax.set_xlim(2.6,5.0);ax.set_ylim(1.4,4.7);ax.set_aspect('equal');ax.axis('off');ax.set_title('03 / VESTIDOR TRANSITABLE',loc='left',fontsize=12)
fig.suptitle('HABITACION ACTUAL / VESTIDOR Y BOW PEQUENA',x=.04,y=.97,ha='left',fontsize=22,color='#263d35')
fig.text(.04,.89,f'{G.ROOM.area:.2f} m² geometricos. El colchon y la mesa conservan su tamano real. La bow sustituye el mirador rectangular.\nEl recorrido de entrada se mantiene al lado de la cama. La bisagra del tablero queda en su canto corto.',fontsize=11,color='#263d35')
fig.text(.04,.025,'Dos estados alternativos; no se superponen muebles plegados y abiertos en un mismo uso.\nLos circulos son posiciones de cuerpo de estudio. El mecanismo del tablero y el detalle de carpinteria siguen pendientes.',fontsize=10,color='#263d35');fig.subplots_adjust(left=.04,right=.97,top=.80,bottom=.1,wspace=.18)
fig.savefig(L/'HABITACION_ACTUAL.png',dpi=170);fig.savefig(L/'HABITACION_ACTUAL.svg');plt.close(fig)
