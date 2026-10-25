from pathlib import Path
import sys,pickle,json,csv,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch
from shapely.geometry import shape,LineString
P=Path(__file__).resolve().parents[1]; R=P.parent
sys.path.insert(0,str(R/'G3_CORRECCION_40_2026-10-18/fuentes'))
import geometria as G
D=pickle.load(open(R/'G3_CORRECCION_40_2026-10-18/datos/GEOMETRIA_CORREGIDA.pkl','rb'))
parcel=shape(json.load(open(R/'G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16/fuentes/parcela_local.geojson'))['geometry'])
def fill(ax,g,c,ec='none',lw=.4):
 for p in G.polys(g):
  ax.add_patch(Patch(np.array(p.exterior.coords),facecolor=c,edgecolor=ec,lw=lw))
  for h in p.interiors:ax.add_patch(Patch(np.array(h.coords),facecolor='#faf8f2',edgecolor=ec,lw=lw))
def draw(ax,d):
 fill(ax,d['floor'],'#e8e2d4')
 for r in d['rooms']:
  fill(ax,r['poly'],'#cbd8cd')
  for g,c in [(G.BED,'#b6a07d'),(G.DESK,'#ba8665'),(G.WARD,'#698478'),(G.SEAT,'#c47898')]:fill(ax,G.tf(g,r),c)
  fill(ax,r['window'],'#259b9c')
 for b in d['program']['baths']:fill(ax,b,'#8799a5')
 for k in ['kitchen','fridge']:fill(ax,d['program'][k],'#78866b')
 for k in ['sofa','table']:fill(ax,d['program'][k],'#c47898')
 e=G.tf(G.Point(0,1.4),d['entry']);ax.plot(e.x,e.y,'o',color='#bd4a3d',ms=3)
 ax.set_aspect('equal');ax.axis('off')
rows=[]
for d in D:
 p=d['floor'];xy=np.array(p.minimum_rotated_rectangle.exterior.coords);ls=[np.linalg.norm(xy[i+1]-xy[i]) for i in range(4)]
 rows.append(dict(codigo=d['code'],suelo_geometrico_m2=round(p.area,2),envolvente_estudio_m2=round(p.buffer(.12).area,2),rectangulo_ancho_min_m=round(min(ls),2),rectangulo_largo_m=round(max(ls),2),ocupacion_rectangulo_pct=round(100*p.area/p.minimum_rotated_rectangle.area,1),perimetro_m=round(p.length,2),ventanas_comunes=len(d['common_windows']),vestidor_transitable='NO',ventana_habitable_profunda='NO',luz_en_parcela='PENDIENTE',pareja_unidades='PENDIENTE'))
with open(P/'COMPARACION_40.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
fig,axs=plt.subplots(8,5,figsize=(18,27),facecolor='#faf8f2')
for ax,d,row in zip(axs.flat,D,rows):
 draw(ax,d);ax.set_xlim(-10,10);ax.set_ylim(-10,10)
 ax.set_title(f"{d['code']}   {row['suelo_geometrico_m2']:.1f} m²\nR. envolvente {row['rectangulo_ancho_min_m']:.1f} × {row['rectangulo_largo_m']:.1f} m",fontsize=9,loc='left',color='#263d35')
fig.suptitle('40 PLANTAS / UNA MISMA MEDIDA',x=.04,y=.987,ha='left',fontsize=23,color='#263d35')
fig.text(.04,.963,'Comparación geométrica de las versiones corregidas. Todos los recuadros muestran 20 × 20 m.\nMismo dormitorio repetido; vestidor transitable y ventana profunda pendientes en las 40.',fontsize=11,color='#263d35')
fig.text(.04,.017,'Verde claro: privado · turquesa: ventanas · rosa: asiento y estar · azul: baños · punto rojo: acceso\nEl rectángulo mide extensión, no prueba encaje en parcela. Sin evaluación solar ni puntuación de calidad.',fontsize=10,color='#263d35')
fig.subplots_adjust(left=.035,right=.975,top=.94,bottom=.045,hspace=.3,wspace=.12)
fig.savefig(P/'01_COMPARACION_40.png',dpi=135);fig.savefig(P/'01_COMPARACION_40.svg');plt.close(fig)
# Deliberately separate drawings at the same metre scale; no invented implantation.
choices=[]
for criterion in [lambda r:r['rectangulo_ancho_min_m'],lambda r:r['ocupacion_rectangulo_pct'],lambda r:-r['perimetro_m']]:
 for row in sorted(rows,key=criterion):
  if row['codigo'] not in choices:choices.append(row['codigo']);break
fig,axs=plt.subplots(4,1,figsize=(16,14),facecolor='#faf8f2')
minx,miny,maxx,maxy=parcel.bounds;cx=(minx+maxx)/2;cy=(miny+maxy)/2
p=G.translate(parcel,-cx,-cy);fill(axs[0],p,'#cbd8cd','#263d35',1)
axs[0].set_title(f'PARCELA / {parcel.area:.1f} m² de polígono catastral local',loc='left',fontsize=13)
for ax,code in zip(axs[1:],choices):
 d=next(d for d in D if d['code']==code);draw(ax,d)
 row=next(r for r in rows if r['codigo']==code)
 ax.set_title(f'{code} / {row["suelo_geometrico_m2"]:.1f} m² · rectángulo {row["rectangulo_ancho_min_m"]:.1f} × {row["rectangulo_largo_m"]:.1f} m',loc='left',fontsize=12)
for ax in axs:
 ax.set_xlim(-28,28);ax.set_ylim(-11,11);ax.set_aspect('equal');ax.axis('off')
 ax.plot([-25,-20],[-9,-9],color='#263d35',lw=3);ax.text(-25,-10,'5 m',fontsize=9)
fig.suptitle('ANTES DE REPETIR, COMPARAR TAMAÑOS',x=.06,y=.99,ha='left',fontsize=21,color='#263d35')
fig.text(.06,.015,'Misma escala métrica en las cuatro franjas. Plantas sin orientar ni colocar en parcela.\nTres extremos geométricos para contrastar: menor ancho envolvente, menor ocupación del rectángulo y mayor perímetro.\nNo son las tres mejores plantas. Catastro local: no sustituye levantamiento, alturas ni parámetros urbanísticos.',fontsize=10,color='#263d35')
fig.subplots_adjust(left=.06,right=.95,top=.93,bottom=.1,hspace=.4)
fig.savefig(P/'02_ESCALA_PARCELA.png',dpi=145);fig.savefig(P/'02_ESCALA_PARCELA.svg');plt.close(fig)
result={'unidades':len(D),'parcela_poligono_m2':round(parcel.area,2),'parcela_extension_xy_m':[round(maxx-minx,2),round(maxy-miny,2)],'tres_contrastes_geometricos':choices,'ancho_rectangulo_unidades_rango_m':[min(r['rectangulo_ancho_min_m'] for r in rows),max(r['rectangulo_ancho_min_m'] for r in rows)],'largo_rectangulo_unidades_rango_m':[min(r['rectangulo_largo_m'] for r in rows),max(r['rectangulo_largo_m'] for r in rows)],'advertencia':'Sin implantacion, sin calculo de luz ni estructura; rectangulos no demuestran imposibilidad de encaje.'}
(P/'RESULTADO.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False))
