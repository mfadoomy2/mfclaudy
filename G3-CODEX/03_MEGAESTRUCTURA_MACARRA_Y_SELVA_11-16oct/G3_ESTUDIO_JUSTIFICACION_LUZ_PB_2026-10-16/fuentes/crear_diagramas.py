from pathlib import Path
import json,math,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PP,Rectangle,Circle
from matplotlib.collections import LineCollection
from shapely.geometry import Polygon,box,shape
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1];S=R.parent/'G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16';A=json.loads((R/'calculo/ESTRUCTURA_RESULTADOS.json').read_text());old=json.loads((R/'calculo/LUZ_40_HABITACIONES.json').read_text());new=json.loads((R/'calculo/LUZ_V5_40_HABITACIONES.json').read_text());site=shape(json.loads((R/'fuentes/parcela_local.geojson').read_text())['geometry']);context=json.loads((R/'fuentes/contexto_original.json').read_text())['context']
bg='#f7f4eb';ink='#253a33';jade='#85b6a1';pink='#c43f79';yellow='#dfb52e';grey='#c7cbc6';plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':ink,'axes.labelcolor':ink,'axes.titlecolor':ink})
def fig(w=14,h=8):
 f,a=plt.subplots(figsize=(w,h),facecolor=bg);a.set_facecolor(bg);return f,a
def save(f,name):f.savefig(R/'diagramas'/name,dpi=170,bbox_inches='tight',facecolor=bg);plt.close(f)
def poly(a,g,**kw):
 for p in ([g] if g.geom_type=='Polygon' else [q for q in g.geoms if q.geom_type=='Polygon']):
  x,y=p.exterior.xy;a.fill(x,y,**kw)
  for r in p.interiors:a.fill(*r.xy,color=bg)
# Site from supplied context projected triangles; courtyard holes retained by union.
f,a=fig(15,9)
for c in context:
 v=c['vertices'];polys=[]
 for i in range(0,len(v),3):
  p=Polygon([(x,y) for x,y,z in v[i:i+3]])
  if p.area>.001:polys.append(p)
 if polys:poly(a,unary_union(polys),fc=grey,ec='#a4aca6',lw=.4)
poly(a,site,fc='#f5edc8',ec=pink,lw=2)
for p in A['plates']:
 a.plot(*np.array(p['outline']).T,color=yellow,alpha=.45,lw=1)
for b in A['bays']:
 a.add_patch(Rectangle((b['x']-4.8,b['front']-.7),9.6,7.5,facecolor=jade,alpha=.7,edgecolor=ink));a.text(b['x'],b['front']+2.8,'AB C'.replace(' ','')[A['bays'].index(b)]+'\n'+str(len(b['levels']))+' pabellones',ha='center',va='center',fontsize=13)
a.annotate('N de cuadrícula',(8,18),(8,12),arrowprops={'arrowstyle':'->','lw':2},ha='center');a.text(5,-3,'Ribera de Curtidores',rotation=90,ha='center',va='center');a.annotate('acceso desde el frente',(13,-4),(5,-13),arrowprops={'arrowstyle':'->','color':pink},color=pink)
a.set_xlim(2,67);a.set_ylim(-22,24);a.set_aspect('equal');a.set_xlabel('X local / este de cuadrícula (m)');a.set_ylabel('Y local / norte de cuadrícula (m)');a.set_title('Una parcela profunda entre cuerpos altos',loc='left',fontsize=21,pad=18);a.grid(alpha=.1)
save(f,'01_PARCELA_Y_CONTEXTO.png')
# Direct geometric metric comparability.
units=sorted(set(r['unit'] for r in old['rows']));oo=np.array([[next(r['sky_v4_clear_sail'] for r in old['rows'] if r['unit']==u and r['room']=='H'+str(h)) for h in range(1,5)] for u in units]);nn=np.array([[next(r['sky_v5'] for r in new['rows'] if r['unit']==u and r['room']=='H'+str(h)) for h in range(1,5)] for u in units])
f,axs=plt.subplots(1,2,figsize=(15,9),facecolor=bg)
for ax,vals,title in zip(axs,[oo,nn],['V4 / dos habitaciones al sur y dos al norte','V5 / cuatro habitaciones al norte']):
 im=ax.imshow(vals,cmap='YlGnBu',vmin=0,vmax=100,aspect='auto');ax.set_xticks(range(4),['H1','H2','H3','H4']);ax.set_yticks(range(10),[u+' / +'+str(next(p['z'] for p in A['plates'] if p['id']==u)) for u in units]);ax.set_title(title,fontsize=15,pad=13)
 for i in range(10):
  for j in range(4):ax.text(j,i,f'{vals[i,j]:.1f}',ha='center',va='center',color='white' if vals[i,j]>55 else ink,fontsize=11)
f.colorbar(im,ax=axs,shrink=.8,label='Cielo exterior visible ponderado (%) / no es iluminancia');f.suptitle('La luz obliga a reorganizar el pabellón',fontsize=23,x=.08,ha='left');f.text(.08,.03,'Estado favorable de velas recogidas. Cambian la distribución y la posición de los huecos; H1-H4 no son ventanas invariables.',fontsize=11)
save(f,'02_COMPARACION_CIELO_40.png')
# Floor diagram of actual V5.
f,a=fig(14,10);a.add_patch(Rectangle((-4.8,-.7),9.6,7.5,fc='#e4ddc7',ec=ink,lw=2))
for i in range(4):
 x=-4.8+2.4*i;a.add_patch(Rectangle((x,2.9),2.4,3.9,fc=jade,ec=ink,lw=1.4));a.add_patch(Rectangle((x+.12,3.6),1.1,2,fc='#faf7ee',ec=ink,lw=.8));a.add_patch(Rectangle((x+.14,6.05),1.1,.55,fc='#c7a875',ec=ink,lw=.6));a.add_patch(Rectangle((x+1.83,4),.48,1.1,fc='#c7a875',ec=ink,lw=.6));a.text(x+1.2,3.15,'H'+str(i+1),ha='center');a.text(x+1.2,5.9,'9,36 m²\nnominales',ha='center',fontsize=10);a.plot([x+.18,x+2.22],[6.79,6.79],color='#2b92b1',lw=5)
 a.annotate('',(x+1.2,6.2),(x+1.2,8.4),arrowprops={'arrowstyle':'->','color':'#2b92b1','lw':2})
a.add_patch(Rectangle((-4.8,1.7),9.6,1.2,fc='#f2d873',ec=ink,lw=1));a.text(0,2.3,'GALERÍA TRANSVERSAL / 1,20 m nominal',ha='center',va='center',fontsize=11)
for x in [-4.8,2.36]:a.add_patch(Rectangle((x,-.7),2.44,2.4,fc='#d6bed1',ec=ink));a.text(x+1.22,.5,'BAÑO',ha='center')
a.add_patch(Rectangle((-2.36,-.7),4.72,2.4,fc='#f1d2b0',ec=ink));a.text(0,.5,'COCINA + MESA',ha='center');a.add_patch(Rectangle((-2.2,-.57),3.6,.62,fc='#c7a875'));a.add_patch(Rectangle((-.7,.65),1.4,.75,fc='#c7a875',ec=ink))
a.annotate('entrada lateral',(-4.8,2.3),(-6.9,2.3),arrowprops={'arrowstyle':'->','color':pink},ha='center',color=pink);a.annotate('entrada lateral',(4.8,2.3),(6.5,2.3),arrowprops={'arrowstyle':'->','color':pink},ha='center',color=pink)
a.plot([-6.2,-6.2,6.2,6.2],[-2.1,6.95,6.95,-2.1],color=yellow,lw=2);a.plot([-6.2,6.2],[-2.1,-2.1],color=yellow,lw=2);a.text(0,-1.42,'GALERÍA EXTERIOR FRONTAL / 1,40 m nominal / sin mesas',ha='center',fontsize=10);a.text(0,8.65,'LUZ DIFUSA DESDE EL PATIO NORTE',ha='center',color='#2b92b1',fontsize=13)
a.annotate('',(-4.8,-2.8),(4.8,-2.8),arrowprops={'arrowstyle':'|-|','color':ink});a.text(0,-3.2,'9,60 m',ha='center');a.set_xlim(-7.5,7.5);a.set_ylim(-3.5,9.2);a.set_aspect('equal');a.axis('off');a.set_title('Una unidad ordenada por su acceso al cielo',loc='left',fontsize=22,pad=20);save(f,'03_UNIDAD_REORGANIZADA.png')
# Section along Y through bay A, conceptual outline tied to actual levels.
f,a=fig(14,9);bay=A['bays'][0]
for z in bay['levels']:
 a.add_patch(Rectangle((-3.9,z-.20),9.05,.20,fc=yellow));a.add_patch(Rectangle((-2.5,z),7.5,4.3,fc=jade,alpha=.22,ec=ink));a.plot([5,5],[z+.1,z+2.2],color='#2b92b1',lw=4)
 for el in [5,15,30,50,70]:
  yy=5+10*math.cos(math.radians(el));zz=z+1.35+10*math.sin(math.radians(el));a.plot([5,yy],[z+1.35,zz],lw=.7,color='#2b92b1',alpha=.35)
a.plot([-5,-5],[0,25],color=ink,lw=6);a.text(-5.6,12,'sur / medianera próxima',rotation=90,va='center');a.text(15,12,'norte / patio y obstrucciones',rotation=90,va='center');a.set_xlim(-7,18);a.set_ylim(0,30);a.set_aspect('equal');a.set_xlabel('Y local / m');a.set_ylabel('Z / m');a.set_title('La cubierta de arriba también tapa el cielo',loc='left',fontsize=21);a.text(-6,28.5,'Esquema interpretativo: rayos ilustrativos, no trazas exactas del BVH.',fontsize=10);save(f,'04_SECCION_Y_ENTRADA_DE_LUZ.png')
# Ground programme and actual path.
f,a=fig(16,8);poly(a,site,fc='#ede8d8',ec=ink,lw=1.5)
route=json.loads((R/'fuentes/recorrido_suelo.json').read_text())
for p in route:a.fill(*np.array(p['outer']).T,fc=yellow,alpha=.45)
labels=['A / COMER Y RECIBIR','B / REPARAR Y LAVAR','C / CUIDAR Y APRENDER']
for i,b in enumerate(A['bays']):
 x,y=b['x']-4.3,b['front'];a.add_patch(Rectangle((x,y),8.6,5.8,fc='#f9f6ec',ec=ink,lw=1.5));a.text(b['x'],y+6.3,labels[i],ha='center',fontsize=11,weight='bold')
 if i==0:
  a.add_patch(Rectangle((x+.3,y+.3),8,2.3,fc='#edc39b'));a.text(b['x'],y+1.3,'12 plazas\ncomedor',ha='center',fontsize=10);a.add_patch(Rectangle((x+.3,y+4.65),4.3,.9,fc='#bd9b70'));a.text(x+2.4,y+5.05,'cocina / despensa',ha='center',fontsize=9)
 elif i==1:
  a.add_patch(Rectangle((x+.3,y+.4),4.4,3.6,fc='#d6bd94'));a.text(x+2.5,y+2,'taller\ny reparación',ha='center',fontsize=10);a.add_patch(Rectangle((x+5,y+4.2),3.3,1.5,fc='#b5d0d1'));a.text(x+6.6,y+4.9,'3 lavadoras',ha='center',fontsize=9);a.add_patch(Rectangle((x+.3,y+4.3),3.8,1.4,fc='#c5d7b8'));a.text(x+2.2,y+5,'bicis / útiles',ha='center',fontsize=9)
 else:
  a.add_patch(Rectangle((x+.2,y+.3),8.1,2.3,fc='#c0d9cb'));a.text(b['x'],y+1.3,'6 puestos de apoyo\nlectura / aula breve',ha='center',fontsize=9);a.add_patch(Rectangle((x+.2,y+3),3.6,2.7,fc='#d8bfd3'));a.text(x+2,y+4.3,'cuidados\ny mediación',ha='center',fontsize=9)
 if i in [0,2]:a.add_patch(Rectangle((b['x']+1.78,y+3.28),2.52,2.52,fc='#c0ccd9'));a.text(b['x']+3.05,y+4.5,'aseo',ha='center',fontsize=9)
 a.annotate('',(b['x'],y+.15),(b['x'],y-1.3),arrowprops={'arrowstyle':'->','color':pink,'lw':2})
 a.text(b['x'],y-1.9,'49,88 m² brutos',ha='center',fontsize=10)
a.text(14,-4,'umbral\nresidencial',ha='center',fontsize=10);a.annotate('',(16,-4),(11,-4),arrowprops={'arrowstyle':'->','color':pink,'lw':2});a.set_xlim(10,64);a.set_ylim(-9,13);a.set_aspect('equal');a.set_xlabel('X local / m');a.set_ylabel('Y local / m');a.set_title('Poblar el suelo sin convertir el paso en una sala',loc='left',fontsize=22,pad=18);a.text(11,11.6,'Zonificación de uso propuesta sobre las tres piezas modeladas. No sustituye plano de evacuación ni reparto útil cerrado.',fontsize=10);save(f,'05_PLANTA_BAJA_PROGRAMADA.png')
# Schedule: illustrative operational rule, not observed counts.
uses=['acogida','comedor','reparación','lavandería','lectura breve','cuidados reservables','asamblea con reserva','silencio residencial'];times=['07-10','10-14','14-17','17-21','21-23','23-07'];matrix=np.array([[1,2,0,1,1,1,0,1],[1,1,2,2,2,2,0,1],[1,2,1,1,1,1,0,1],[1,1,2,2,2,2,2,1],[1,1,0,1,1,1,0,2],[0,0,0,0,0,1,0,2]])
f,a=fig(14,7);a.imshow(matrix.T,cmap='YlGnBu',vmin=0,vmax=2,aspect='auto');a.set_yticks(range(len(uses)),uses);a.set_xticks(range(len(times)),times);a.set_title('La planta baja cambia por horario y por acuerdo',loc='left',fontsize=22,pad=16)
for i in range(len(uses)):
 for j in range(len(times)):a.text(j,i,['cerrado','disponible','prioritario'][matrix[j,i]],ha='center',va='center',fontsize=10,color='white' if matrix[j,i]==2 else ink)
f.text(.05,.01,'Hipótesis de gestión: cuidados no implica atención profesional permanente. Taller y asamblea no ocupan el mismo recinto a la vez.',fontsize=10);f.tight_layout();save(f,'06_HORARIOS_Y_CONVIVENCIA.png')
# Winter previous values, without presenting them as a new measurement.
prev=json.loads((R/'fuentes/originales/SOL_POR_ALTURA_ESTUDIO_PREVIO.json').read_text());f,a=fig(13,7)
for date,col in [('2026-12-21',pink),('2026-03-21',jade),('2026-06-21',yellow)]:
 z=sorted(float(k) for k in prev[date]);v=[prev[date][str(int(k)) if k.is_integer() else str(k)]['media'] for k in z];a.plot(v,z,'o-',color=col,label=date,lw=2)
a.set_xlabel('Horas medias de sol directo en la parcela');a.set_ylabel('Altura de muestreo / m');a.set_title('El estudio previo ya obligaba a pensar en sección',loc='left',fontsize=21);a.legend();a.grid(alpha=.2);f.text(.08,.01,'Modelo anterior 2,5D de septiembre: alturas inferidas de plantas catastrales. No equivale al cálculo 3D por habitación de V4/V5.',fontsize=10);save(f,'07_SOL_POR_ALTURA_PREVIO.png')
print('DIAGRAMAS_LISTOS',flush=True)
