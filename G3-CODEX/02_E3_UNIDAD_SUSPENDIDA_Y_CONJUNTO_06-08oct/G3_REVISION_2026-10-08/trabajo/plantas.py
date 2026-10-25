from proponer import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch
from shapely.affinity import scale,translate

def poly(ax,p,c,ec='#353b3f',lw=.55,alpha=1):
 if p.is_empty:return
 if p.geom_type!='Polygon':
  for q in p.geoms:poly(ax,q,c,ec,lw,alpha)
  return
 ax.add_patch(Patch(np.array(p.exterior.coords),facecolor=c,edgecolor=ec,lw=lw,alpha=alpha))
 for h in p.interiors:ax.add_patch(Patch(np.array(h.coords),facecolor='white',edgecolor=ec,lw=lw))
def modplan(ax,parts,upper=False):
 for p in parts:
  if 'polygon' not in p:continue
  lay=p['layer'];z0,z1=p['z']
  if any(x in lay for x in ['08','09','mastil','Portico']):continue
  if upper:
   ok=z0<3.55 and z1>2.55
   if 'Caracol' in lay and not 'barrote' in lay and not 'pasamanos' in lay:ok=True
   if not ok:continue
  else:
   if z0>1.30 or z1<-.25:continue
   if 'Altillo' in lay or 'Cubierta' in lay:continue
  col=p['color'];poly(ax,Polygon(p['polygon'],p['holes']),col,lw=.4)
 ax.set_aspect('equal');ax.set(xlim=(-.6,5.3),ylim=(6.8,-1.7));ax.axis('off')
 ax.annotate('',xy=(4.7,-1.45),xytext=(0,-1.45),arrowprops={'arrowstyle':'|-|','lw':.6});ax.text(2.35,-1.53,'4,70 m',ha='center',fontsize=9)
fig,axs=plt.subplots(1,3,figsize=(15,9),facecolor='white')
D=json.loads((B/'trabajo/03_MODULO_D_duplex_propuesto.json').read_text());S=json.loads((B/'trabajo/04_MODULO_S_una_planta.json').read_text())
for ax,p,up,title in [(axs[0],D,False,'D / COTA ±0,00'),(axs[1],D,True,'D / COTA +2,64'),(axs[2],S,False,'S / UNA PLANTA')]:
 modplan(ax,p,up);ax.set_title(title,loc='left',fontsize=14,weight='bold')
for ax in [axs[0],axs[2]]:ax.annotate('Entrada desde el común',xy=(2.7,-.12),xytext=(2.5,-.8),ha='center',fontsize=8,arrowprops={'arrowstyle':'->','lw':.6})
axs[0].text(.95,3.45,'baño',ha='center',fontsize=8);axs[0].text(4.22,3.4,'cocina',ha='center',rotation=90,fontsize=7);axs[1].text(3.5,-.25,'estudio',ha='center',fontsize=8);axs[1].text(1.1,1.15,'doble\naltura',ha='center',fontsize=9)
fig.text(.055,.96,'DOS TIPOS, UN MISMO LENGUAJE',fontsize=22,weight='bold');fig.text(.055,.91,'Plantas de proyecto extraídas de las piezas del modelo · medidas en metros · distribución por contrastar a 1:50',fontsize=11);fig.text(.055,.035,'D: dos ámbitos de cama, no dos dormitorios acústicamente independientes. S: sin escalera interior; accesibilidad del baño pendiente.',fontsize=10);fig.subplots_adjust(top=.83,bottom=.09,wspace=.10);fig.savefig(B/'vistas/plantas_modulos.png',dpi=170);plt.close(fig)
site=Polygon(json.loads(pathlib.Path('/Volumes/T7/G3 Proyectos/G3 CLAUDE/01_E2_IMAGINARIOS_PERSONAS_Y_MECANISMOS_05-06oct/G3_MECANISMOS_EN_PARCELA_2026-10-05/geometria/parcela_local.geojson').read_text())['geometry']['coordinates'][0]);stats=json.loads((B/'trabajo/conjunto_datos.json').read_text());md=json.loads((B/'trabajo/modulos_datos.json').read_text());parts=json.loads((B/'trabajo/05_CONJUNTO_propuesto_32_40.json').read_text())
fig,axs=plt.subplots(3,1,figsize=(16,13))
for ax,k,title in [(axs[0],-1,'01 / SUELO DEL BARRIO'),(axs[1],0,'02 / PLANTA DE OCHO UNIDADES S'),(axs[2],3,'03 / OCHO DÚPLEX, DOS GRUPOS DE OCHO PERSONAS')]:
 poly(ax,site,'#f5f5f2',lw=1.5)
 for p in parts:
  if 'polygon' not in p:continue
  l=p['layer'];z0,z1=p['z'];z=0 if k==-1 else [4.5,7.5,10.5,13.5][k]
  if k==-1:
   if not l.startswith('09') and not l.startswith('07'):continue
   if z0>1 or z1<0:continue
  else:
   if not (l.startswith('04 Calle') or l.startswith('06 Cocina') or l.startswith('07 Nucleo')):continue
   if z0>z+.1 or z1<z:continue
  poly(ax,Polygon(p['polygon'],p.get('holes',[])),p['color'],lw=.5)
 if k>=0:
  for u in stats['unidades']:
   if u['z']!=[4.5,7.5,10.5,13.5][k]:continue
   p=translate(scale(Polygon(md[u['tipo']]['footprint']),1,-1,origin=(0,0)),xoff=u['x']);poly(ax,p,'#e1eeee',lw=.8);ax.text(u['x']+2.35,-3,u['id']+'\n'+str(u['residentes'])+' pers.',ha='center',fontsize=8)
   ax.plot([u['x']+2.7,u['x']+2.7],[0,1],color='#d86f53',lw=1.3)
  ax.text(57.4,-2,'COCINA\nSALÓN\n49,0 m² bruto',ha='center',va='center',fontsize=8)
  ax.annotate('Galería libre 1,80 m',xy=(45,.9),xytext=(44,5),ha='center',fontsize=9,arrowprops={'arrowstyle':'->','lw':.7})
  ax.text(25.5,3.2,'ESTAR EXTERIOR',ha='center',fontsize=8)
  if k==3:ax.text(33,-9,'Casa 4: D401–D404 / Casa 5: D405–D408. Cocina-salón compartida por ambos grupos: punto por mejorar.',ha='center',fontsize=9)
 else:
  for x,y,t in [(19,-3.5,'CANTINA'),(31,-4.5,'TALLER'),(41,-4.4,'LAVAR'),(48.5,-4,'CUIDADOS'),(57.3,-3,'SERVICIOS')]:ax.text(x,y,t,ha='center',fontsize=8)
  ax.text(23,7,'INTERCAMBIO / ASAMBLEA EXTERIOR',ha='center',fontsize=8)
 ax.text(33.8,4.8,'NÚCLEO',ha='center',fontsize=8)
 ax.set_aspect('equal');ax.set(xlim=(9,65),ylim=(-10,15));ax.axis('off');ax.set_title(title,loc='left',fontsize=15,weight='bold')
 ax.annotate('N',xy=(63,10),xytext=(63,5),ha='center',arrowprops={'arrowstyle':'->','lw':1});ax.text(10.6,0,'RIBERA DE CURTIDORES',rotation=90,ha='center',fontsize=8)
fig.text(.055,.965,'EL COMÚN TIENE DIRECCIÓN Y PUERTAS',fontsize=22,weight='bold');fig.text(.055,.936,'Perímetro de la parcela incorporado sin escalar · no se presupone salida a través del patio vecino',fontsize=11);fig.text(.055,.025,'Hipótesis: datum de acceso plano +622,60 m. El desnivel real del frente y la normativa urbanística deben incorporarse al siguiente desarrollo.',fontsize=10);fig.subplots_adjust(top=.89,bottom=.065,hspace=.12);fig.savefig(B/'vistas/plantas_conjunto.png',dpi=160);plt.close(fig)
