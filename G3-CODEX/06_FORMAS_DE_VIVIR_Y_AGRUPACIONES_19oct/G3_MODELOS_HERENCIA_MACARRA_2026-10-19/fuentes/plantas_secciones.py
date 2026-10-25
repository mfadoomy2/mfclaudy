from pathlib import Path
import json,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection,PolyCollection
P=Path(__file__).resolve().parents[1]
for code in ['E01_ENCUENTRO','E02_COMUNA','E03_DOS_CLAROS']:
 d=json.loads((P/'fuentes'/(code+'_render.json')).read_text());colors=d['colors']
 def cuts(ax,axis,value,projection):
  for ob in d['objects']:
   if ob['layer'] in ['90_CONTEXTO','16_PERSONAS']:continue
   vv=np.asarray(ob['vertices']);lines=[]
   for face in ob['faces']:
    co=vv[face];ds=co[:,axis]-value
    if ds.min()>1e-6 or ds.max()<-1e-6:continue
    pp=[]
    for a,b,da,db in zip(co,np.roll(co,-1,axis=0),ds,np.roll(ds,-1)):
     if da*db<0:pp.append(a+(b-a)*da/(da-db))
     elif abs(da)<1e-6:pp.append(a)
    pp=np.unique(np.round(pp,5),axis=0) if len(pp) else []
    if len(pp)==2:lines.append([[q[projection[0]],q[projection[1]]] for q in pp])
   if lines:ax.add_collection(LineCollection(lines,colors=[tuple(a/255*.65 for a in colors[ob['layer']])],linewidths=.55))
 for z,name in [(1.20,'PB'),(5.40,'VIVIENDA')]:
  fig,ax=plt.subplots(figsize=(16,8),facecolor='#faf8f2');ax.set_facecolor('#faf8f2')
  floor=0 if z<4 else 4.2
  for ob in d['objects']:
   if ob['layer'] in ['90_CONTEXTO','16_PERSONAS','06_VIDRIO']:continue
   vv=np.asarray(ob['vertices']);caps=[]
   for face in ob['faces']:
    co=vv[face]
    if np.ptp(co[:,2])<1e-5 and floor-.01<=co[0,2]<=floor+1.0:caps.append(co[:,:2])
   if caps:ax.add_collection(PolyCollection(caps,facecolors=[(.94,.92,.87) if ob['layer']=='91_PARCELA' else tuple(a/255 for a in colors[ob['layer']])],edgecolors='none',alpha=.75))
  cuts(ax,2,z,[0,1])
  if name=='PB':
   for x,y,t in [(17,1.5,'SALA COMÚN'),(25.5,-2.0,'TALLER'),(33,-.05,'COMEDOR'),(35.5,-5.0,'COCINA / ALMACÉN'),(25,7.6,'CUIDADOS'),(28.6,-7.0,'ASEOS EN BORDE'),(47,-4.5,'ESCALERA'),(51,-3.4,'ASCENSOR')]:ax.text(x,y,t,fontsize=7,color='#263d35',ha='center')
   path=[(12,1),(22,1),(29,1),(37,1),(45,-1),(51,-1.8)]
   for a,b in zip(path[:-1],path[1:]):ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':'#b94c6c','lw':1.1})
  ax.set_xlim(9,62);ax.set_ylim(-10,14);ax.set_aspect('equal');ax.axis('off')
  fig.suptitle(code+' / '+('PLANTA BAJA COMÚN / cota 0' if name=='PB' else 'PRIMER GRUPO DE VIVIENDAS / cota +4,20'),x=.04,y=.97,ha='left',fontsize=18,color='#263d35')
  fig.text(.04,.035,'Dibujo de la geometría 3D del ensayo. PB sin dormitorios. Dimensiones de estudio; no acredita cumplimiento normativo ni iluminación.',fontsize=9,color='#263d35')
  fig.savefig(P/'vistas'/(code+'_PLANTA_'+name+'.svg'));fig.savefig(P/'vistas'/(code+'_PLANTA_'+name+'.png'),dpi=155);plt.close(fig)
 for value,name in [(0.,'COMUN'),(-3.45,'NUCLEO')]:
  fig,ax=plt.subplots(figsize=(17,6),facecolor='#faf8f2');ax.set_facecolor('#faf8f2');cuts(ax,1,value,[0,2]);ax.set_xlim(10,56);ax.set_ylim(-1.4,10.4);ax.set_aspect('equal');ax.axis('off')
  for z,t in [(0,'0,00 / común edificio'),(4.2,'+4,20 / viviendas')]:
   ax.plot([10,55],[z,z],color='#b94c6c',lw=.45,ls='--');ax.text(10,z+.13,t,fontsize=8,color='#b94c6c')
  fig.suptitle(code+' / SECCIÓN '+name+' / plano Y = '+str(value)+' m',x=.04,y=.97,ha='left',fontsize=17,color='#263d35')
  fig.text(.04,.035,'Sección calculada por intersección de los elementos dibujados. Apoyos y cubiertas nuevos son hipótesis, sin cálculo transferido de la versión anterior.',fontsize=9,color='#263d35')
  fig.savefig(P/'vistas'/(code+'_SECCION_'+name+'.svg'));fig.savefig(P/'vistas'/(code+'_SECCION_'+name+'.png'),dpi=155);plt.close(fig)
 print(code,'plantas y secciones',flush=True)
