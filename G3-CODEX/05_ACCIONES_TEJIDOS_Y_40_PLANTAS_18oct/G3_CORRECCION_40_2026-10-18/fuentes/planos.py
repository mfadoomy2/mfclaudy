from pathlib import Path
import pickle,json,csv,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch,Arc
import geometria as G
P=Path(__file__).resolve().parents[1]
COL={'floor':'#efe7d8','wall':'#576b5e','bed':'#e2d7b6','desk':'#ae7651','ward':'#a8b9a5','seat':'#c682a0','glass':'#3b9d9d','walk':'#188b7f'}
def shape(ax,g,c,ec='none',lw=.4,alpha=1):
 for p in G.polys(g):
  ax.add_patch(Patch(np.array(p.exterior.coords),facecolor=c,edgecolor=ec,lw=lw,alpha=alpha))
  for h in p.interiors:ax.add_patch(Patch(np.array(h.coords),facecolor='white',edgecolor=ec,lw=lw))
def label(ax,p,text,size=7,c='#263b32'):
 x,y=p.centroid.coords[0];ax.text(x,y,text,ha='center',va='center',fontsize=size,color=c)
def sheet(d):
 fig,ax=plt.subplots(figsize=(13,12),facecolor='#faf8f2');ax.set_facecolor('#faf8f2')
 shape(ax,d['floor'],COL['floor'])
 shape(ax,G.tf(G.box(-.8,1.35,.8,2.75),d['entry']),'#dce0d2',ec='#889582')
 windows=d['wincuts'].union(G.unary_union([w['cut'] for w in d['common_windows']]))
 shape(ax,d['walls'].difference(d['doors']).difference(windows),COL['wall'])
 for i,r in enumerate(d['rooms']):
  for poly,c in [(G.BED,COL['bed']),(G.DESK,COL['desk']),(G.WARD,COL['ward']),(G.SEAT,COL['seat']),(G.CHAIR,'#ae9271')]:shape(ax,G.tf(poly,r),c,ec='#5b5b4c')
  shape(ax,r['window'],COL['glass'],alpha=.6)
  label(ax,r['poly'],r['id']+' · '+format(r['poly'].area,'.1f')+' m²',8)
  # Every door has a straight jamb and its open leaf is visibly beside it.
  shape(ax,G.tf(G.box(1.,.015,2.,.055),r),COL['desk'])
  line=G.tf(G.LineString([(2.55,-.70),(2.55,.8),(2.35,1.60),(2.35,4.05)]),r)
  x,y=line.xy;ax.plot(x,y,color=COL['walk'],lw=.7,ls='--',alpha=.75)
 p=d['program']
 for b in p['baths']:
  shape(ax,b,'#d7ded6');x,y,X,Y=b.bounds
  shape(ax,G.box(x+.04,Y-.86,x+.86,Y-.04),'#b9c9cc',ec='#5b6c6b')
  shape(ax,G.Point(X-.35,Y-.47).buffer(.23),'#f9f8ee',ec='#5b6c6b')
  shape(ax,G.box(x+.04,y+.15,x+.44,y+.50),'#b5a18a')
  label(ax,b,'BAÑO\n'+format(b.area,'.1f')+' m²',6)
 for k,c in [('kitchen','#6d9691'),('fridge','#e9ebdf'),('sofa',COL['seat']),('table',COL['desk'])]:shape(ax,p[k],c,ec='#687065')
 for s in p['stools']:shape(ax,s,'#ae9271')
 for w in d['common_windows']:shape(ax,w['cut'],COL['glass'],alpha=.65)
 label(ax,G.Point(-1.3,-1.5) if d['variant']=='A' else G.Point(1.3,-1.5),'ESTAR',8)
 label(ax,p['table'],'COMER\nTRABAJAR',6,c='white')
 ep=G.tf(G.Point(0,2.05),d['entry']);label(ax,ep,'ENTRADA\n1,20 m',7)
 X0,Y0,X1,Y1=d['floor'].bounds;ax.set_xlim(X0-.7,X1+.7);ax.set_ylim(Y0-1.2,Y1+.7);ax.set_aspect('equal');ax.axis('off')
 fig.suptitle(d['code']+'  /  '+d['family'],x=.07,y=.97,ha='left',fontsize=17,fontweight='bold',color='#253c30')
 a=G.audit(d)
 fig.text(.07,.925,'4 habitantes · suelo '+str(a['new_floor_m2'])+' m² · envolvente '+str(a['gross_envelope_m2'])+' m² · acabado Z = 0',fontsize=9,color='#425d4b')
 fig.text(.07,.055,'Cama 1,25 × 2,00 m  /  Mesa de dibujo 1,80 × 0,90 m  /  Puerta dormitorio 1,00 m\nTelas exteriores recogidas. Taburetes de dibujo aparcados bajo mesa. Planta de unidad aislada: no acredita luz en parcela.',fontsize=8,color='#425d4b',linespacing=1.6)
 # Scale bar is drawn in model metres.
 x=X0+.2;y=Y0-.65
 for j in range(5):shape(ax,G.box(x+j,y,x+j+1,y+.065),'#364f3f' if j%2==0 else '#b6c1af')
 ax.text(x,y-.16,'0',fontsize=7);ax.text(x+5,y-.16,'5 m',fontsize=7,ha='right')
 fig.savefig(P/'vistas'/(d['code']+'_PLANO.png'),dpi=150,facecolor=fig.get_facecolor());fig.savefig(P/'vistas'/(d['code']+'_PLANO.svg'),facecolor=fig.get_facecolor());plt.close(fig)

if __name__=='__main__':
 D=pickle.load(open(P/'datos/GEOMETRIA_CORREGIDA.pkl','rb'))
 for d in D:sheet(d)
 print('40_PLANOS_EQUIPADOS',flush=True)
