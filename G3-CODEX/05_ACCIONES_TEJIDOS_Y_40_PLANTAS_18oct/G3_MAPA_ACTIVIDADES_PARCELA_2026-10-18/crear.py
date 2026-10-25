from pathlib import Path
import json,math,textwrap,csv,shutil
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon,Circle,FancyArrowPatch
from shapely.geometry import shape,Point
P=Path(__file__).parent;D=P.parent/'INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/DATOS/DERIVADOS';bg='#faf8f1';ink='#283730';pink='#d14b8f';cyan='#35aeb1';gold='#d6ae38';green='#5c9b72'
# Fictional design scenes, not interview findings
scenes=[
('S01','00:40 / volver empapadas','Dos vuelven de ayudar a recoger materiales. Ropa mojada, zapatos y lona; otra persona duerme.','Llegar → dejar → cambiarse → secar','Secado y ducha cerca de llegada; ruido lejos del descanso.','La cooperación no debe dejarte durmiendo entre humedad.','recursos','descanso','lluvia'),
('S02','02:10 / una amiga sin habitación','Una amiga necesita pasar la noche. Quien la recibe tiene una entrega a las nueve.','Acoger → guardar → dormir → salir','Acogida con intimidad y duración acordada; sin ocupar evacuación.','Una casa puede apoyar una emergencia sin normalizarla.','encuentro','descanso','hipotesis'),
('S03','09:00 / entrevista y desayuno','Entrevista por videollamada; al lado se prepara desayuno y suena la cafetera.','Conectar → hablar → concentrarse','Lugar privado con conexión y control acústico.','Buscar trabajo no debería exigir pagar otro espacio.','descanso','encuentro','hipotesis'),
('S04','01:20 / entrega y turno temprano','Una persona corta una maqueta; otra necesita dormir para entrar a trabajar a las seis.','Desplegar → cortar → dejar → dormir','Superficie resistente y almacenamiento; separar ruido y descanso.','La flexibilidad no consiste en desmontar tu trabajo cada noche.','hacer','descanso','hipotesis'),
('S05','20:30 / cocinar para muchas','Cuatro cocinan doce raciones. Alguien sólo quiere calentar su táper y marcharse.','Preparar → cocinar → servir → recoger','Cocina colectiva y uso individual simultáneo, sin bloquear paso.','Compartir debe ampliar opciones, no imponer una comida común.','encuentro','recursos','pulmon'),
('S06','19:10 / conflicto sin público','Dos residentes necesitan mediación mientras el resto está en la sala.','Llegar → hablar → escuchar → salir','Conversación reservada y salida discreta; no aislamiento obligatorio.','Lo común también necesita confidencialidad.','cuidado','encuentro','comisiones'),
('S07','18:00 / reparar una tela','Se cose una pieza seca de protección mientras alguien busca herramientas para su bici.','Desmontar → extender → reparar → guardar','Mesa de reparación, herramientas y acceso de mantenimiento.','Una fachada de tela necesita trabajo, tiempo y presupuesto.','hacer','recursos','lluvia'),
('S08','22:45 / no quiero participar','Hay cena y conversación. Una residente quiere ducharse y acostarse sin explicar nada.','Entrar → asearse → retirarse','Acceso a cuarto y baño sin atravesar la reunión.','La comunidad no puede exigir disponibilidad constante.','descanso','encuentro','hipotesis'),
('S09','07:15 / intimidad con prisas','Dos tienen horarios distintos; una necesita vestirse mientras otra sigue dormida.','Buscar ropa → vestirse → salir','Luz localizada, armario accesible y circulación sin rodear cama.','La intimidad se mide también en no interrumpir a otra persona.','descanso','recursos','hipotesis'),
('S10','16:20 / acompañar sin interrogar','Una amiga viene desbordada; quiere compañía tranquila, sin ser observada por toda la casa.','Recibir → sentarse → acompañar','Rincón protegido próximo al estar, sin exposición ni encierro.','Cuidar no equivale a improvisar una consulta sanitaria.','cuidado','encuentro','comisiones'),
('S11','23:30 / lavar después del trabajo','Se acaba la ropa limpia; lavar ahora coincide con quien ya duerme.','Clasificar → lavar → secar → guardar','Separación acústica, almacenamiento y horario acordado.','Los horarios domésticos deben admitir trabajos incompatibles.','recursos','descanso','hipotesis'),
('S12','15:00 / calor y videollamada','Una habitación se recalienta; cerrar la tela quita vista y parte de la luz del escritorio.','Sombrear → ventilar → seguir trabajando','Control individual de tela y luz; estudiar aire, calor y deslumbramiento.','El confort no puede depender de aguantar o gastar más.','descanso','recursos','hipotesis'),
('S13','21:00 / intimidad afectiva','Una residente recibe a su pareja; otras quieren seguir usando la sala y la cocina.','Recibir → estar → retirarse','Privacidad visual y acústica; acuerdos sin vigilancia.','Compartir vivienda no elimina la vida íntima.','descanso','encuentro','hipotesis'),
('S14','11:30 / quién recoge hoy','Tras una actividad compartida quedan platos, basura y una tela que revisar. Nadie tiene tiempo.','Limpiar → reparar → repartir tareas','Equipos accesibles; responsabilidades y presupuesto explícitos.','La sostenibilidad del grupo no se sostiene con trabajo invisible.','recursos','cuidado','comisiones'),
('S15','18:40 / llegar cargada','Una persona llega con compra y material voluminoso; otra lleva la bici.','Llegar → subir → girar → guardar','Recorrido continuo, giros y aparcamiento fuera del paso.','La accesibilidad se comprueba con cuerpos y cargas reales.','recursos','hacer','urbanismo'),
('S16','13:00 / descansar enferma','Una residente necesita reposo mientras hay trabajo compartido y cocina en marcha.','Asearse → beber → descansar → pedir ayuda','Descanso con control de luz y acceso próximo a aseo.','El cuidado debe permitir retirarse sin desaparecer del grupo.','descanso','cuidado','comisiones')]
rows=[dict(zip(['id','titulo','escena','acciones','condicion','critica','atractor','tension','origen'],s)) for s in scenes]
(P/'SITUACIONES.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
with open(P/'SITUACIONES.csv','w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def fig(title,size):
 f,a=plt.subplots(figsize=size);f.patch.set_facecolor(bg);a.set_facecolor(bg);a.axis('off');a.set_title(title,loc='left',fontsize=22,color=ink,pad=22);return f,a
def save(f,n):
 for ext in ['png','svg']:f.savefig(P/(n+'.'+ext),dpi=170,bbox_inches='tight',facecolor=bg)
 plt.close(f)
for start in [0,8]:
 f,a=fig('Situaciones de proyecto / '+('01–08' if start==0 else '09–16'),(16,16));a.set_xlim(0,2);a.set_ylim(0,4.35)
 a.text(0,4.24,'Escenas ficticias para contrastar · no entrevistas ni hábitos universales · no son estancias predeterminadas',fontsize=11,color=ink)
 for i,s in enumerate(rows[start:start+8]):
  x=i%2;y=3-i//2;a.add_patch(Rectangle((x+.01,y+.025),.96,.95,fc='#ffffff',ec='#c9d1c5',lw=1));a.text(x+.04,y+.90,s['id']+'  '+s['titulo'],fontsize=13,fontweight='bold',color=pink)
  yy=y+.79
  for content,col,fs in [(s['escena'],ink,11),(s['acciones'],cyan,10),('NECESITA / '+s['condicion'],ink,10),('CRÍTICA / '+s['critica'],pink,10)]:
   text=textwrap.fill(content,66);a.text(x+.04,yy,text,va='top',fontsize=fs,color=col,linespacing=1.4);yy-=.045*(text.count('\n')+1)+.065
 save(f,'01_SITUACIONES_'+str(start+1).zfill(2))
# network of relationships: points are activity places; no coordinates in site
f,a=fig('Atractores / relaciones que necesitan lugar, sin dibujar paredes',(15,12));a.set_xlim(-7.5,7.5);a.set_ylim(-5.4,5.4)
pos={'encuentro':(0,2.9),'descanso':(-4,-.8),'cuidado':(4,-.8),'hacer':(-3.8,-3.6),'recursos':(3.8,-3.6)};labels={'encuentro':'ESTAR + COCINAR','descanso':'RETIRO + CONCENTRACIÓN','cuidado':'ACOMPAÑAR + CONVERSAR','hacer':'DIBUJAR + REPARAR','recursos':'LAVAR + GUARDAR + MANTENER'}
links=[('encuentro','descanso','separar ruido / permitir retiro',pink),('encuentro','cuidado','cercanía con confidencialidad',cyan),('descanso','hacer','separar corte / conservar trabajo',pink),('hacer','recursos','herramientas y almacenamiento',cyan),('cuidado','recursos','tareas y responsabilidades',cyan),('encuentro','recursos','cocinar / limpiar / repartir',cyan)]
for u,v,t,c in links:
 x,y=pos[u];xx,yy=pos[v];a.plot([x,xx],[y,yy],color=c,lw=2,alpha=.7);a.text((x+xx)/2,(y+yy)/2,textwrap.fill(t,23),ha='center',fontsize=9,color=ink,bbox=dict(fc=bg,ec='none',pad=2))
for k,(x,y) in pos.items():
 a.add_patch(Circle((x,y),.7,fc='#e5eadc',ec=ink,lw=2));a.text(x,y,labels[k].replace(' + ','\n'),ha='center',va='center',fontsize=10,color=ink);ids=[s['id'] for s in rows if s['atractor']==k];a.text(x,y-.95,' · '.join(ids),ha='center',fontsize=9,color=ink)
a.text(0,4.65,'Las distancias del dibujo no son metros. Un atractor puede tener varias localizaciones y cambiar por horario.',ha='center',fontsize=11,color=ink)
a.text(0,-5,'Rosa: conflicto que pide mediación espacial o temporal. Turquesa: proximidad útil, siempre condicionada.',ha='center',fontsize=10,color=ink);save(f,'02_RED_DE_ATRACTORES')
# pairwise sample conflicts with own design interpretation, no fake score
pairs=[('S01','S16','Secar y ducharse / dormir enferma','Separar ruido y humedad; proximidad a ayuda sin exposición.'),('S03','S05','Entrevista / cocinar para varias','Conexión privada y separación acústica; no prohibir cocinar.'),('S04','S08','Entrega nocturna / derecho al retiro','Reserva de trabajo que pueda quedarse montada, fuera del acceso.'),('S02','S13','Acoger una noche / intimidad','Lugar temporal acordado; no resolverlo ocupando dormitorio ajeno.'),('S07','S15','Reparar / llegar con cargas','Herramientas cerca, material fuera del recorrido.'),('S10','S06','Acompañar / mediar un conflicto','Mismo lugar podría servir por turnos si hay confidencialidad.'),('S11','S09','Lavar tarde / salir temprano','Capacidad y almacenamiento; separación acústica y horarios.'),('S12','S03','Cerrar tela por calor / trabajar','Control climático y luz simultáneos; no asumir tela siempre abierta.')]
f,a=fig('Cruces / el conflicto produce una exigencia de proyecto',(16,10));a.set_xlim(0,1);a.set_ylim(0,1)
for i,(u,v,t,res) in enumerate(pairs):
 y=.92-i*.108;a.text(.015,y,u+' × '+v,fontsize=13,color=pink,fontweight='bold');a.text(.18,y,t,fontsize=12,color=ink);a.text(.18,y-.04,res,fontsize=10,color=ink);a.plot([.01,.99],[y-.065,y-.065],color='#c9d1c5',lw=.7)
a.text(.01,.015,'Hipótesis de diseño. No son puntuaciones ni resultados de una encuesta. Revisar con personas y dimensiones de uso.',fontsize=10,color=ink);save(f,'03_CONFLICTOS_Y_REGLAS')
# Real raw cadastral site: NO previously generated complex geometry
parcel=shape(json.load(open(D/'parcela_31.geojson'))['features'][0]['geometry']);ox,oy=439984,4473229.4
from shapely.affinity import translate
parcel=translate(parcel,-ox,-oy);f,a=fig('Parcela real / soporte de investigación, sin complejo previo',(15,12));a.set_aspect('equal');a.axis('on')
parts=json.load(open(D/'catastro_partes_400m.geojson'))['features'];bounds=parcel.buffer(45)
for feature in parts:
 g=translate(shape(feature['geometry']),-ox,-oy)
 if not g.intersects(bounds):continue
 n=feature['properties'].get('plantas_sr');col='#c6cfca' if not n else plt.cm.Greys(.15+min(n,10)*.055)
 gs=[g] if g.geom_type=='Polygon' else list(g.geoms)
 for q in gs:a.add_patch(Polygon(np.array(q.exterior.coords),fc=col,ec='#a9b1ab',lw=.4))
a.add_patch(Polygon(np.array(parcel.exterior.coords),fc='#f2d9e4',ec=pink,lw=2.5));co=list(parcel.exterior.coords);front=[co[16],co[17]];a.plot(*zip(*front),color=pink,lw=6);a.text(8,-.4,'CALLE\nRibera de Curtidores',ha='center',fontsize=11,color=ink)
# study sample grid only no daylight claim
for x in np.arange(16,62,4):
 for y in np.arange(-6,13,4):
  if parcel.contains(Point(x,y)):a.plot(x,y,'.',color=cyan,ms=5)
a.annotate('N de cuadrícula',(10,29),(10,19),arrowprops=dict(arrowstyle='->',color=ink),ha='center',fontsize=11,color=ink)
a.text(37,32,'651 m² catastrales / referencia 0134911VK4703C',ha='center',fontsize=12,color=ink)
a.text(37,-24,'Puntos turquesa: muestreo propuesto; todavía NO hay valores de luz. Edificios: partes catastrales, sin proyecto nuevo.',ha='center',fontsize=9,color=ink)
a.text(37,-27,'Base de septiembre de 2026. Alturas, desnivel, nave existente y acceso requieren contraste y levantamiento.',ha='center',fontsize=9,color=ink)
a.set_xlim(2,77);a.set_ylim(-30,35);a.set_xlabel('X local / este de cuadrícula (m)');a.set_ylabel('Y local / norte de cuadrícula (m)');save(f,'04_PARCELA_REAL_SIN_COMPLEJO')
# inherited parcel-only solar baseline clearly separated from new design
sun=json.load(open(D/'sol_por_altura.json'));f,a=plt.subplots(figsize=(13,9));f.patch.set_facecolor(bg);a.set_facecolor(bg)
for date,c in [('2026-12-21',pink),('2026-03-21',cyan),('2026-06-21',gold)]:
 vals=sorted((float(z),v['media']) for z,v in sun[date].items());a.plot([v[1] for v in vals],[v[0] for v in vals],'-o',c=c,label=date)
a.set_title('Antecedente solar de la parcela / no es luz de una vivienda',loc='left',fontsize=18,color=ink,pad=20);a.set_xlabel('Horas medias de sol directo geométrico en la parcela');a.set_ylabel('Cota de muestreo / m');a.legend();a.grid(alpha=.15);f.text(.1,.015,'Modelo 2,5D previo, alturas inferidas por plantas. No lux, cielo visible ni simulación interior. No autoriza una altura edificable.',fontsize=9,color=ink);save(f,'05_ANTECEDENTE_SOL_PARCELA')
shutil.copyfile(D/'parcela_31.geojson',P/'PARCELA_CATASTRAL_ORIGINAL.geojson')
print('6 laminas PNG+SVG + situaciones CSV/JSON + parcela original',flush=True)
