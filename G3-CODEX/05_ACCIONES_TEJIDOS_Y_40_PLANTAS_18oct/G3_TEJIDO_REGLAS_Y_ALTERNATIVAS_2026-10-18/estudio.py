from pathlib import Path
import json,csv,math,textwrap
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
P=Path(__file__).parent;bg='#fbfaf4';ink='#2f3c36';cyan='#10a3aa';pink='#ce3d80';gold='#b98c24';purple='#8056a8';red='#cf4b3a'
actions=[('Dormir','Cama, cuerpo tumbado, acceso a ropa y aseo.','Silencio, intimidad, oscuridad controlable; horario variable.'),('Vestirse','Cuerpo de pie, abrir almacenamiento, cambiar ropa.','Privacidad; luz localizada; no invadir cama o puerta.'),('Ducharse','Cuerpo mojado, toalla, cambio seco.','Agua, extracción, intimidad; transición seca.'),('Secar ropa','Prendas húmedas ocupan volumen durante horas.','Ventilación y humedad controlada; no dormitorio como secadero.'),('Guardar ropa','Ropa limpia, sucia y de temporada.','Acceso próximo a vestirse; capacidad por comprobar.'),('Entrevista en vídeo','Persona sentada, portátil, voz y fondo de cámara.','Intimidad visual, conexión y control acústico.'),('Cocinar','Preparar, abrir equipos, cocinar, recoger.','Agua, extracción, higiene y usos simultáneos.'),('Comer','Una o varias personas; comida y apoyos.','Puede ser individual o compartido; no convivencia obligatoria.'),('Conversar en grupo','Voces, varias posturas, duración variable.','Encuentro voluntario y derecho a retirarse.'),('Hablar en privado','Dos personas, voz y escucha.','Confidencialidad, salida discreta; no consulta sanitaria.'),('Dibujar','Tablero1,80×0,90m y persona trabajando.','Luz de tarea y referencias; trabajo puede quedar montado.'),('Guardar maqueta','Objeto frágil, dimensiones variables.','Capacidad y traslado sin atravesar usos incompatibles.'),('Cortar maqueta','Herramientas, recortes y superficie resistente.','Ruido y limpieza; materiales/adhesivos específicos por estudiar.'),('Coser una tela','Pieza extendida, máquina o herramientas.','Acceso, apoyo y almacenamiento; tamaño real pendiente.'),('Reparar bicicleta','Bici, herramientas, grasa y maniobra.','Trabajo sucio separado de preparación de comida.'),('Llegar con cargas','Compra, mochila o material voluminoso.','Paso y giros sin ocupar permanentemente circulación.'),('Recibir una visita','Esperar, saludar, acordar acceso.','Control de intimidad; no enseñar dormitorios desde llegada.'),('Salir con prisa','Abrigo, llaves, pertenencias y recorrido.','Camino libre; no supone una segunda puerta.'),('Limpiar y recoger','Agua, útiles, residuos y tiempo de trabajo.','Almacenamiento accesible, reparto de tareas y presupuesto.'),('Guardar herramientas','Útiles de reparación, seguridad y devolución.','Acceso próximo a trabajos; no armario de ropa.')]
ids=[f'A{i+1:02}' for i in range(len(actions))]
# typed relationships authored as explicit design hypotheses, not observed behavior
rels=[]
def rel(a,b,t,reason,scene):rels.append(dict(a=f'A{a:02}',b=f'A{b:02}',tipo=t,razon=reason,escena=scene))
for a,b,reason,sc in [(2,5,'Alcanzar ropa mientras te vistes.','S09'),(3,2,'Cambiarse con intimidad y transición seca.','S01/S09'),(3,4,'Gestionar textiles húmedos sin recorrer espacios secos.','S01'),(7,8,'Trasladar comida sin rodeos.','S05'),(11,12,'Guardar trabajo frágil sin desmontarlo o transportarlo lejos.','S04'),(13,12,'Dejar piezas y materiales a mano.','S04'),(14,20,'Tomar y devolver herramientas.','S07'),(15,20,'Tomar y devolver herramientas.','S15'),(16,5,'Dejar pertenencias; capacidad y tipo de almacenamiento a revisar.','S01'),(16,17,'Resolver la llegada de una visita.','S10'),(18,5,'Recoger pertenencias al salir; no implica misma puerta que recibir.','S09'),(7,19,'Recoger después de preparar comida.','S14')]:rel(a,b,'PROXIMIDAD',reason,sc)
for a,b,reason,sc in [(1,7,'Cocinar de madrugada puede interrumpir descanso.','S05/S08'),(1,13,'Corte nocturno y descanso son simultáneos.','S04'),(1,9,'Las voces del grupo pueden impedir retirarse.','S08'),(6,7,'La entrevista necesita voz inteligible y privacidad.','S03/S05'),(6,9,'No exponer una entrevista a conversación ajena.','S03'),(10,9,'Confidencialidad frente a presencia del grupo.','S06'),(4,1,'La humedad no debe resolverse invadiendo el descanso.','S01/S16'),(15,7,'Separar grasa, residuos y herramientas de preparación de comida.','S15/S05')]:rel(a,b,'PROTEGER',reason,sc)
for a,b,reason,sc in [(6,11,'Mesa potencialmente compartible por horario si equipo y postura funcionan.','S03/S04'),(14,13,'Apoyo de trabajo compartible tras limpieza y almacenamiento.','S07/S04'),(8,11,'Sólo si no obliga a desmontar continuamente el trabajo.','S05/S04'),(10,6,'Lugar reservado potencialmente compartible por turnos.','S06/S03')]:rel(a,b,'POR_TURNOS',reason,sc)
for a,b,reason,sc in [(1,3,'Recorrido útil, pero proximidad puede introducir ruido.','S16'),(8,9,'Comer y conversar pueden coincidir, sin obligar a hacerlo.','S05'),(16,18,'Una misma puerta puede servir; las acciones son distintas.','S15'),(11,14,'Compartir superficie depende de tamaño, suciedad y persistencia.','S04/S07')]:rel(a,b,'CONDICIONAL',reason,sc)
(P/'ACCIONES.json').write_text(json.dumps([dict(id=id,accion=q[0],ocupacion=q[1],condiciones=q[2]) for id,q in zip(ids,actions)],ensure_ascii=False,indent=2));(P/'RELACIONES.json').write_text(json.dumps(rels,ensure_ascii=False,indent=2))
with open(P/'RELACIONES.csv','w') as f:w=csv.DictWriter(f,fieldnames=list(rels[0]));w.writeheader();w.writerows(rels)
def setup(title,size=(16.54,11.69)):
 f,a=plt.subplots(figsize=size);f.patch.set_facecolor(bg);a.set_facecolor(bg);a.set_title(title,loc='left',fontsize=20,color=ink,pad=22);return f,a
def save(f,n):
 for ext in ['png','svg']:f.savefig(P/(n+'.'+ext),dpi=180,bbox_inches='tight',facecolor=bg)
 plt.close(f)
# explicit full relation matrix: blank != compatible
f,a=setup('01 / Antes de colocar puntos: qué relación tiene cada acción');N=len(ids);M=np.zeros((N,N));typeval={'PROXIMIDAD':1,'PROTEGER':2,'POR_TURNOS':3,'CONDICIONAL':4}
for rr in rels:i=ids.index(rr['a']);j=ids.index(rr['b']);M[i,j]=M[j,i]=typeval[rr['tipo']]
from matplotlib.colors import ListedColormap,BoundaryNorm
cm=ListedColormap(['#f0f0e8',cyan,pink,gold,purple]);a.imshow(M,cmap=cm,norm=BoundaryNorm(np.arange(-.5,5),5));a.set_xticks(range(N),ids,fontsize=8,rotation=90);a.set_yticks(range(N),[ids[i]+' '+actions[i][0] for i in range(N)],fontsize=9);a.set_xticks(np.arange(-.5,N,1),minor=True);a.set_yticks(np.arange(-.5,N,1),minor=True);a.grid(which='minor',color=bg,lw=1);a.tick_params(which='both',length=0)
for x,(s,c) in enumerate([('Proximidad',cyan),('Proteger',pink),('Por turnos',gold),('Condicional',purple)]):f.text(.16+x*.2,.025,s,color=c,fontsize=12)
f.text(.16,.065,'Gris = relación no definida, no compatibilidad demostrada. Colores = hipótesis justificadas, no resultados de entrevistas.',fontsize=10,color=ink);save(f,'01_MATRIZ_DE_RELACIONES')
# full auditable reasons in two readable panels
for start in [0,14]:
 f,a=setup('02 / Razones de las relaciones · '+('1 de 2' if start==0 else '2 de 2'),(16.54,13));a.axis('off');a.set_xlim(0,1);a.set_ylim(0,1)
 for i,rr in enumerate(rels[start:start+14]):
  y=.97-i*.067;co=[cyan,pink,gold,purple][typeval[rr['tipo']]-1];a.text(0,y,rr['a']+' × '+rr['b'],color=co,fontsize=11,fontweight='bold');a.text(.14,y,rr['tipo']+' / '+rr['razon'],color=ink,fontsize=10);a.text(.14,y-.025,'Situación de partida: '+rr['escena'],fontsize=8,color='#6a766c');a.plot([0,1],[y-.04,y-.04],c='#d5ddd3',lw=.6)
 save(f,'02_RAZONES_'+str(start+1).zfill(2))
# free placements on discrete graphic lattice. No corner assignments or fixed entry.
near=np.array([(ids.index(r['a']),ids.index(r['b'])) for r in rels if r['tipo']=='PROXIMIDAD']);protect=np.array([(ids.index(r['a']),ids.index(r['b'])) for r in rels if r['tipo']=='PROTEGER']);slots=np.array([(x,y) for x in range(13) for y in range(9)])
def metrics(p):
 dn=np.abs(p[near[:,0]]-p[near[:,1]]).sum(1);dp=np.abs(p[protect[:,0]]-p[protect[:,1]]).sum(1)
 return np.array([np.maximum(dn-3,0).sum(),np.maximum(5-dp,0).sum(),dn.sum()],float)
def optimize(seed,w):
 rng=np.random.default_rng(seed);p=slots[rng.choice(len(slots),N,False)].copy();best=p.copy();score=float(metrics(p)@w);bs=score
 for it in range(4200):
  q=p.copy();i=int(rng.integers(N))
  if rng.random()<.3:j=int(rng.integers(N));q[[i,j]]=q[[j,i]]
  else:
   pos=slots[int(rng.integers(len(slots)))];matches=np.flatnonzero((q==pos).all(1))
   if len(matches):q[matches[0]]=q[i]
   q[i]=pos
  ns=float(metrics(q)@w);temp=3*(1-it/4200)+.04
  if ns<score or rng.random()<math.exp(min(0,(score-ns)/temp)):p=q;score=ns
  if score<bs:best=p.copy();bs=score
 return best
pool=[]
for weights in [np.array([3,1,.03]),np.array([1,4,.03]),np.array([2,2,.1])]:
 for seed in range(6):
  pos=optimize(100+seed,weights);pool.append((pos,metrics(pos),weights.tolist(),100+seed))
# select by declared alternative priorities, not a sole optimum or final design
chosen=[min(pool,key=lambda q:float(q[1]@np.array([2,2,.1])))]
# Retain compliant candidates, then diversify relational distance patterns;
# mere translation, rotation or reflection does not count as new organization.
def pattern(item):
 pp=item[0];return np.abs(pp[:,None,:]-pp[None,:,:]).sum(2)
valid=[q for q in pool if q[1][0]==0 and q[1][1]==0 and q[1][2]<=chosen[0][1][2]+3]
for k in range(2):
 candidates=[q for q in valid if all(not np.array_equal(q[0],c[0]) for c in chosen)]
 chosen.append(max(candidates,key=lambda q:min(np.abs(pattern(q)-pattern(c)).sum() for c in chosen)))
results=[]
for number,(p,met,w,seed) in enumerate(chosen,1):
 f,a=setup(f'03 / Tejido {number} · posiciones libres bajo reglas explícitas');a.set_aspect('equal');a.set_xlim(-.7,17);a.set_ylim(-1.6,9.8);a.axis('off')
 for x in range(13):a.plot([x,x],[0,8],c='#d7dfd5',lw=.45)
 for y in range(9):a.plot([0,12],[y,y],c='#d7dfd5',lw=.45)
 xx,yy=np.meshgrid(range(13),range(9));a.scatter(xx,yy,s=5,c='#bdc9bd');viol=[]
 for rr in rels:
  i,j=ids.index(rr['a']),ids.index(rr['b']);x,y=p[i];X,Y=p[j];d=abs(X-x)+abs(Y-y);t=rr['tipo'];bad=(t=='PROXIMIDAD' and d>3) or (t=='PROTEGER' and d<5)
  if bad:viol.append(rr['a']+'–'+rr['b'])
  col=red if bad else [cyan,pink,gold,purple][typeval[t]-1];alpha=.8 if t in ['PROXIMIDAD','PROTEGER'] else .25
  bend=.15*((i+j)%3-1);path=MPath([(x,y),(x+(X-x)*.3,y+(Y-y)*.3+bend),(x+(X-x)*.7,y+(Y-y)*.7+bend),(X,Y)],[1,4,4,4]);a.add_patch(PathPatch(path,ec=col,fc='none',lw=1.4 if bad else .9,alpha=alpha,ls='--' if t in ['POR_TURNOS','CONDICIONAL'] else '-'))
 for i,(x,y) in enumerate(p):a.scatter([x],[y],c=bg,ec=ink,s=130,zorder=5);a.text(x,y,ids[i][1:],ha='center',va='center',fontsize=7,color=ink,zorder=6)
 for i,(id,ac) in enumerate(zip(ids,actions)):a.text(12.6,8.7-i*.45,id+'  '+ac[0],fontsize=8,color=ink)
 a.text(0,9.2,'Retícula abstracta: no metros, orientación, paredes ni perímetro de vivienda. Todos los nodos pueden moverse.',fontsize=10,color=ink)
 a.text(0,-.6,f'Incumplimientos de prueba: {len(viol)} · '+(', '.join(viol) if viol else 'ninguno en estas reglas gráficas'),fontsize=9,color=red if viol else ink)
 a.text(0,-1.1,'Rojo = umbral gráfico incumplido. Separar puntos NO acredita aislamiento acústico, higiene ni privacidad.',fontsize=9,color=ink)
 save(f,f'03_TEJIDO_{number}')
 results.append({'alternative':number,'positions':{id:p[i].tolist() for i,id in enumerate(ids)},'metrics':met.tolist(),'violations':viol,'seed':seed,'generation_weights':w})
(P/'RESULTADOS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
(P/'METODO.json').write_text(json.dumps({'all_positions_free':True,'grid':'13x9 discrete graphic slots, no metres','near_rule':'Manhattan distance <=3 graphic steps, hypothesis','protect_rule':'Manhattan distance >=5 graphic steps, proxy hypothesis only','objective_metrics':['sum of near excess steps','sum of protective separation deficits','total near distances'],'search':'18 simulated annealing runs,4200 iterations each; no global optimum guarantee','turn_and_conditional_relations':'Displayed, not used to impose closeness. Need duration and compatibility checks.','weights':'Declared generation devices, not measured social priorities. Final candidates satisfy graph limits and are diversified by pairwise distance patterns, excluding simple coordinate copies.','excluded':['actual footprints','wall thickness','acoustics','daylight','entry location','resident count','circulation obstacles','building regulations']},indent=2))
# all action facts/hypotheses readable editable text
md=['# Acciones antes de lugares','Estas20acciones no equivalen a20espacios ni a20personas. Una acción puede repetirse en varias personas/lugares. No fija cuatro habitaciones.']
for id,q in zip(ids,actions):md.extend(['',f'## {id} · {q[0]}',q[1],q[2]])
(P/'ACCIONES_PARA_DISCUTIR.md').write_text('\n\n'.join(md))
print('6 laminas;18busquedas; reglas y resultados guardados',[(q['alternative'],q['metrics'],len(q['violations'])) for q in results])
