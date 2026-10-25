from pathlib import Path
import json,hashlib,math,re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
P=Path(__file__).resolve().parents[1];R=P.parent;L=P/'laminas'
OUT=P/'output/pdf/G3_PLANTAS_NUEVAS_Y_DIAGRAMAS_CORREGIDOS.pdf'
report=json.load(open(P/'verificacion/GEOMETRIA_FINAL.json'));A={a['codigo']:a for a in report['alternativas']}
for name,file in [('Regular','Arial.ttf'),('Bold','Arial Bold.ttf'),('Italic','Arial Italic.ttf')]:pdfmetrics.registerFont(TTFont(name,'/System/Library/Fonts/Supplemental/'+file))

ACCENTS={'habitacion':'habitación','habitaciones':'habitaciones','banos':'baños','bano':'baño','organizacion':'organización','ambito':'ámbito','ambitos':'ámbitos','geometrico':'geométrico','geometricos':'geométricos','acustica':'acústica','acustico':'acústico','correccion':'corrección','revision':'revisión','conexion':'conexión','calibracion':'calibración','decision':'decisión','reticula':'retícula','diagramatico':'diagramático','diagramaticos':'diagramáticos','hipotesis':'hipótesis','generacion':'generación','pequena':'pequeña','todavia':'todavía','mas':'más','unica':'única','matematico':'matemático','automaticamente':'automáticamente','posicion':'posición','distribucion':'distribución','codigo':'código','aqui':'aquí','intencion':'intención','proteccion':'protección','comparacion':'comparación','verificacion':'verificación','limites':'límites','guia':'guía','paginas':'páginas','pagina':'página','manana':'mañana','corporal':'corporal','aislamiento':'aislamiento','fisica':'física','medicion':'medición','estructura':'estructura','implantacion':'implantación','extraccion':'extracción','ventilacion':'ventilación','instalacion':'instalación','instalaciones':'instalaciones','critica':'crítica','optimizador':'optimizador','optimizacion':'optimización','gestión':'gestión','gestion':'gestión','circulacion':'circulación','acreditacion':'acreditación','estadistico':'estadístico','grafico':'gráfico','graficas':'gráficas','estadistica':'estadística','publico':'público','relacion':'relación','autonomia':'autonomía','escenas':'escenas','numero':'número','informacion':'información','reunion':'reunión','seria':'sería','patinillos':'patinillos','tecnica':'técnica','tecnicos':'técnicos','comun':'común','comunes':'comunes','comuna':'comuna','geometria':'geometría','leccion':'lección','trasmision':'trasmisión','transmision':'transmisión','control':'control','grafica':'gráfica','razon':'razón','dimension':'dimensión','geometrica':'geométrica'}
def es(t):
 def word(m):
  w=m.group();before=m.string[m.start()-1:m.start()] if m.start() else '';after=m.string[m.end():m.end()+1];after2=m.string[m.end()+1:m.end()+2]
  if before in ['/', '_'] or after in ['/', '_'] or (after=='.' and after2.isalpha()):return w
  a=ACCENTS.get(w.lower(),w)
  return a.capitalize() if w[:1].isupper() and not w.isupper() else a.upper() if w.isupper() else a
 return re.sub(r'[A-Za-z]+',word,str(t))

W,H=landscape(A3);M=44;INK=HexColor('#263d35');BG=HexColor('#faf8f2');ACC=HexColor('#b94c6c');MUT=HexColor('#687b70')
ST=ParagraphStyle('body',fontName='Regular',fontSize=12,leading=17.5,textColor=INK,spaceAfter=12)
SM=ParagraphStyle('small',parent=ST,fontSize=9,leading=12)
HEAD=ParagraphStyle('head',parent=ST,fontName='Bold',fontSize=15,leading=20)
pages=[];provenance=[];bounds=[]
def add(title,kind,**kw):pages.append(dict(title=title,kind=kind,**kw))
def original(folder,name,title,note):
 path=R/folder/(name+'.png');assert path.exists();provenance.append({'tipo':'antecedente_original','archivo':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'nota':note});add(title,'image',path=path,note=note,tag='ANTECEDENTE DIAGRAMATICO / NO ES PLANTA VIGENTE')
add('PLANTAS NUEVAS / CENTROS PARA CONVIVIR','cover')
add('Guia de lectura','contents')
add('Regla corregida: los aseos quedan fuera del estar','rules')
add('De la investigacion a las ocho organizaciones','lineage')
mp='G3_MAPA_ACTIVIDADES_PARCELA_2026-10-18'
for n,t,cap in [
('01_SITUACIONES_01','D01 / Situaciones 01-08','Escenas ficticias de proyecto. No entrevistas ni retrato estadistico de una generacion.'),
('01_SITUACIONES_09','D02 / Situaciones 09-16','Necesidades, conflictos y critica que orientan decisiones; no prescriben una forma unica.'),
('02_RED_DE_ATRACTORES','D03 / Red inicial de actividades','Relaciones exploratorias. Los nodos no son habitaciones obligatorias ni posiciones en metros.'),
('03_CONFLICTOS_Y_REGLAS','D04 / Conflictos y reglas','Proteger no equivale automaticamente a alejar. Faltan pruebas acusticas, visuales y de uso simultaneo.'),
('04_PARCELA_REAL_SIN_COMPLEJO','D05 / Parcela como antecedente','Base territorial anterior, sin nueva implantacion ni levantamiento de alturas en esta revision.'),
('05_ANTECEDENTE_SOL_PARCELA','D06 / Antecedente solar de parcela','Resultado previo 2,5D con alturas inferidas. No verifica la luz de ninguna planta nueva de este documento.')]:original(mp,n,t,cap)
manual='G3_UNIDAD_TEJIDO_ACTIVIDADES_2026-10-18'
for n,t,cap in [
('01_TEJIDO_GENERAL','D07 / El tejido de cosas que pasan','Antecedente manual. Sus cuatro retiros y posiciones se cuestionaron despues; no se reintroducen como planta.'),
('02_CRUCES_QUE_PRODUCEN_LUGARES','D08 / Cruces que piden proyecto','Las curvas representan relaciones y secuencias; no son recorridos peatonales medidos.'),
('03A_TIEMPO_MANANA','D09 / Actividades por la manana','Escena horaria hipotetica sobre el soporte grafico inicial. No determina la distribucion final.'),
('03B_TIEMPO_TARDE','D10 / Actividades por la tarde','Coexistencia y turnos como preguntas de proyecto, sin suponer que compartir elimina conflictos.'),
('03C_TIEMPO_NOCHE','D11 / Actividades por la noche','Retirarse exige proteccion. La escena no acredita aislamiento ni silencio en las plantas nuevas.'),
('04_CALIBRACION_CORPORAL','D12 / Calibracion corporal de partida','Antecedente de dimensionado. Las medidas vigentes de cama, mesa, vestidor y bow aparecen en las paginas 23-24.')]:original(manual,n,t,cap)
rel='G3_TEJIDO_REGLAS_Y_ALTERNATIVAS_2026-10-18'
for n,t,cap in [
('01_MATRIZ_DE_RELACIONES','D13 / Matriz de relaciones','Veinte acciones y 28 relaciones razonadas. La matriz es una hipotesis editable; lo no definido no se presume compatible.'),
('02_RAZONES_01','D14 / Razones de proximidad y proteccion','Registro original de razones. No convierte distancias graficas en metros ni en criterios normativos.'),
('02_RAZONES_15','D15 / Razones, turnos y condiciones','Compartir requiere tiempo, capacidad y compatibilidad. No obliga a duplicar una sala por cada accion.'),
('03_TEJIDO_1','D16 / Tejido alternativo 1','Resultado original en reticula sin metros. No hay una deduccion automatica y unica desde sus puntos a V01.'),
('03_TEJIDO_2','D17 / Tejido alternativo 2','Otra colocacion de acciones. No se atribuye a esta figura una generacion exacta de V02 que no se ha demostrado.'),
('03_TEJIDO_3','D18 / Tejido alternativo 3','Tercer antecedente. V03 es una traduccion de proyecto; sus reglas de uso y su geometria se declaran aparte.')]:original(rel,n,t,cap)
add('Habitacion vigente: dos estados y vestidor','image',path=L/'HABITACION_ACTUAL.svg',note='18,35 m² geometricos. El vestidor sigue siendo transitable y la mesa se recoge por su canto corto.',tag='DETALLE NUEVO / VIGENTE')
add('Bow window pequena y curva','image',path=R/'G3_UNIONES_COMUNAS_2026-10-19/02_BOW_WINDOW_CURVA.svg',note='Detalle vigente de ventana, sin cambios en esta correccion de banos. Proyeccion 0,60 m; radio de vidrio 1,25 m.',tag='DETALLE VIGENTE / BOW')
add('El filtro de servicios: giro, acceso y vistas','image',path=L/'DETALLE_SERVICIOS.svg',note='Las visuales muestreadas se detienen en un filtro. El disco de 90 cm puede rodearlo y llegar a las puertas.',tag='CORRECCION NUEVA / ASEOS EN BORDE')
add('Tres unidades que conservan diferencias de convivencia','image',path=L/'COMPARACION_UNIDADES.svg',note='Las tres organizaciones mantienen sus diferencias. Lo repetido es una prestacion del dormitorio y el detalle de servicios.',tag='COMPARACION / MISMA ESCALA ENTRE CELDAS')
NAMES={'V01_U':'V01 / Convivencia continua','V02_U':'V02 / Dos ambitos conectados','V03_U':'V03 / Centro libre para estar','V02_P':'V02 / Pareja con umbral','V01_D':'V01 / Encuentro mayor','V01_S':'V01 / Casa comun continua','V03_D':'V03 / Plaza entre estancias','V03_S':'V03 / Continuidad diagonal'}
TEXT={
'V01_U':['A07/A08: preparar y comer se relacionan sin ocupar el dormitorio. A09: estar permanece en el otro extremo.','Los aseos se trasladan al borde de servicios. El espacio central que ocupaban pasa a admitir comida y circulacion.','La cocina se recoloca para no bloquear la entrada al vestibulo. La mesa gira para mantener el paso con sus cuatro asientos.'],
'V02_U':['El campo se diferencia en dos ambitos conectados: preparar/trabajar y comer/estar. No se obliga a participar de la misma actividad.','Los aseos salen de ambos focos y se concentran en el borde. Su filtro no se confunde con el cierre entre actividades.','La cocina y el comedor cambian de posicion al liberar los antiguos lugares de servicio. El control acustico del encuentro sigue pendiente.'],
'V03_U':['Las acciones de estar y reunirse recuperan el centro. A03 se lleva a una pieza de servicios en el borde; no a una isla dentro del circulo.','El radio del espacio comun baja de 3,90 a 3,25 m. Los accesos privados se conectan mediante pequenos ensanchamientos rectos.','El enlace diagonal a servicios mantiene las bow al exterior. Cuesta recorrido y superficie: la forma necesita otra fase de compactacion.'],
'V02_P':['Dos viviendas conservan sus espacios compartidos y se encuentran en un umbral. Es el ensayo con mayor autonomia entre grupos.','La union no introduce un bano ni una instalacion en el centro del encuentro. Los servicios quedan en los extremos exteriores.','No se presenta como comuna totalmente fusionada: conserva dos comedores de cuatro y dos cocinas, conectados por un umbral comun.'],
'V01_D':['El encuentro se convierte en estancia para ocho: recibir, comer y reunirse. A16/A17/A18 se resuelven desde una llegada comun.','Hay una cocina principal, despensa compartida, apoyo de trabajo y estar. Los cuatro aseos se integran en bordes filtrados.','El centro mayor cuesta superficie; no acredita por si solo mejor convivencia. Se conservan ocho dormitorios individuales.'],
'V01_S':['El suelo comun enlaza cocina, trabajo, comida y estar sin una puerta entre antiguas unidades. El comedor admite ocho.','Dos dormitorios se desplazan 0,90 m para liberar la llegada y el rodeo de la mesa. No se comprimen cuerpos ni mobiliario.','Los servicios quedan en los extremos. El acceso visual a sus puertas se filtra, pero la transmision de voces necesita proyecto.'],
'V03_D':['Una estancia mayor pone en relacion dos ambitos circulares libres. Los servicios se desplazan al borde exterior de cada extremo.','Las dos cocinas pertenecen al grupo de ocho. La doble centralidad puede volver a separar grupos; se mantiene como hipotesis a evaluar.','La plaza y las conexiones aumentan mucho el suelo. La intensidad formal no compensa una cuenta de superficies que excede el objetivo.'],
'V03_S':['La convivencia se prolonga por un interior diagonal sin reinstalar aseos en su centro. El comedor de ocho queda en la continuidad.','El tramo se ensancha para rodear la mesa; no se dibuja una conexion estrecha que solo parece funcionar desde lejos.','La union sigue siendo larga y costosa. La proxima compactacion debera cambiar posiciones, no volver a ocupar el centro con servicios.']}
for code in NAMES:
 add(NAMES[code]+' / De relaciones a organizacion','case',code=code,path=L/(code+'_DIAGRAMA_NUEVO.svg'),texts=TEXT[code])
 add(NAMES[code]+' / Planta corregida','image',path=L/(code+'_PLANTA_CORREGIDA.svg'),note='Planta nueva vigente. Los aseos estan en borde; no se incluyen plantas anteriores con islas de banos.',tag='PLANTA NUEVA CORREGIDA / '+code)
add('Superficies: el coste de cada organizacion','areas')
add('Programa, intimidad y convivencia','programme')
add('Parcela y megaestructura: que se puede afirmar ahora','macro')
add('Comprobaciones y limites del documento','checks')
add('Procedencia y control de versiones','sources')
assert len(pages)==47,len(pages)
# Original diagram pages are included as sources only; no superseded floor plan is embedded.
(P/'verificacion/INDICE_Y_PROCEDENCIA.json').write_text(json.dumps({'paginas':[{'pagina':i+1,'titulo':p['title'],'tipo':p['kind'],'imagen':str(p.get('path',''))} for i,p in enumerate(pages)],'fuentes_originales':provenance,'plantas_nuevas':list(NAMES),'catalogo_homogeneizado_incluido':False},ensure_ascii=False,indent=2))
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1);c.setTitle('G3 - Plantas nuevas y diagramas corregidos');c.setAuthor('G3 - Documento de trabajo')
def para(text,x,y,w,style=ST):
 p=Paragraph(es(text),style);pw,ph=p.wrap(w,H);assert y-ph>48,(text[:60],y,ph);p.drawOn(c,x,y-ph);bounds.append([page,x,y-ph,pw,ph]);return y-ph-12
def blocks(items,x,y,w):
 for text in items:y=para(text,x,y,w)
 return y
def image(path,x,y,w,h):
 if path.suffix.lower()=='.svg':
  d=svg2rlg(str(path));assert d and d.width and d.height,path
  k=min(w/d.width,h/d.height);c.saveState();c.translate(x+(w-d.width*k)/2,y+(h-d.height*k)/2);c.scale(k,k);renderPDF.draw(d,c,0,0);c.restoreState()
 else:
  from PIL import Image
  im=Image.open(path);iw,ih=im.size;k=min(w/iw,h/ih);c.drawImage(ImageReader(im),x+(w-iw*k)/2,y+(h-ih*k)/2,width=iw*k,height=ih*k,mask='auto')
def table(data,x,y,widths,fs=11):
 styles=ParagraphStyle('table',parent=ST,fontSize=fs,leading=fs+4)
 dat=[[Paragraph(es(str(v)),styles) for v in row] for row in data]
 t=Table(dat,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),HexColor('#dbe5d9')),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#f2eee4'),HexColor('#faf8f2')]),('LINEBELOW',(0,0),(-1,0),.6,MUT),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]));tw,th=t.wrap(sum(widths),H);assert y-th>60,(page,th);t.drawOn(c,x,y-th);return y-th-20
for page,p in enumerate(pages,1):
 c.setFillColor(BG);c.rect(0,0,W,H,fill=1,stroke=0);c.setFillColor(INK);c.setFont('Bold',19);c.drawString(M,H-47,es(p['title']));c.setStrokeColor(MUT);c.setLineWidth(.5);c.line(M,H-62,W-M,H-62)
 c.setFont('Regular',8.5);c.setFillColor(MUT);c.drawString(M,28,'G3 / Revisión 19.10.2026 / Plantas nuevas, servicios en borde');c.drawRightString(W-M,28,f'{page:02d} / {len(pages)}')
 kind=p['kind']
 if kind=='cover':
  y=H-105;y=para('Ocho organizaciones nuevas, con sus antecedentes diagramaticos y la correccion de los banos.',M,y,W-2*M,HEAD)
  image(L/'COMPARACION_UNIDADES.svg',M,150,W-2*M,480)
  blocks(['<b>Contenido vigente:</b> V01, V02, V03; pareja V02; uniones V01 y V03 en version dramatica y continua. Habitacion con vestidor y bow curva pequena.','<b>Regla:</b> los banos no ocupan el centro de los lugares de convivencia. El catalogo homogeneizado y las plantas anteriores quedan fuera.'],M,135,W-2*M)
 elif kind=='contents':
  rows=[['Paginas','Contenido'],['03-04','Regla de correccion y cadena de decisiones'],['05-10','D01-D06 / situaciones, conflictos, parcela y antecedente solar'],['11-16','D07-D12 / tejido manual, horarios y calibracion de partida'],['17-22','D13-D18 / matriz, razones y tres tejidos alternativos'],['23-26','Habitacion vigente, bow, filtro de servicios y comparacion de unidades'],['27-32','V01, V02 y V03: lectura relacional y planta nueva'],['33-34','V02: pareja con umbral, corregida'],['35-42','V01 y V03: cuatro uniones nuevas corregidas'],['43-47','Superficies, convivencia, parcela, verificacion y procedencia']]
  table(rows,M,H-95,[100,W-2*M-100]);para('Los antecedentes se reproducen completos como diagramas de origen. Las ocho plantas que se muestran son las corregidas en esta revision; no se reproducen las plantas homogeneizadas.',M,200,W-2*M)
 elif kind=='rules':
  items=['<b>1 / Centro para convivir.</b> Ningun aseo como isla en el centro del estar, el circulo habitable o la sala comun. Esta es una regla explicita del proyecto.','<b>2 / Servicios en borde.</b> Se agrupan en una prolongacion de servicio ligada al perimetro. La llegada atraviesa un vestibulo y un filtro, manteniendo paso libre.','<b>3 / La correccion cambia mas que una etiqueta.</b> Se retiran las islas, se ajustan cocina, mesas, estar y recorridos. V03 reduce el radio del ambito principal para recuperar parte del suelo.','<b>4 / Diversidad de convivencia.</b> V01 enlaza; V02 diferencia dos ambitos; V03 ensaya una estancia libre con conexiones radiales. No se reducen a giros de una misma planta.','<b>5 / Prestaciones personales.</b> Una habitacion por residente, vestidor transitable, tablero A1 por canto corto y bow pequena con asiento curvo.','<b>6 / No se esconde el coste.</b> Los vestibulos y bordes de servicio aumentan superficie. La compatibilidad con 40 residentes y 1.500 m² sigue abierta.']
  blocks(items[:3],M,H-105,515);blocks(items[3:],W/2+20,H-105,515)
  para('La regla queda guardada en REGLAS_DE_PROYECTO.md y en la nota de continuidad solicitada por el usuario. No implica que el resto del proyecto este resuelto.',M,180,W-2*M)
 elif kind=='lineage':
  rows=[['Origen','Que aporta','Que no determina'],['D01-D06 / situaciones y lugar','Necesidades, conflictos, acceso a recursos, preguntas de luz.','No prescribe habitaciones, metros ni una forma de edificio.'],['D07-D12 / tejido manual','Cruces, duraciones, posibilidad de coexistir.','Las posiciones iniciales de retiro fueron cuestionadas; no se fijan como planta.'],['D13-D18 / matriz y tres tejidos','Razones para acercar, proteger o compartir por turnos.','No es un optimizador de vivienda ni una prueba de luz o sonido.'],['Diagramas nuevos / paginas 27-42','Hacen explicita la interpretacion espacial de cada organizacion.','Son una lectura añadida ahora, no pruebas de una generacion automatica exacta.'],['Plantas nuevas / esta revision','Dimensionan cuerpos, muebles, accesos, bordes y agrupaciones.','No acreditan normativa, estructura, acustica o implantacion.']]
  table(rows,M,H-95,[225,420,457],11)
  para('Se conserva la trazabilidad sin inventar un parentesco matematico: los tres tejidos no producen por si solos una unica V01, V02 o V03. La decision arquitectonica intermedia se explica en cada ficha.',M,160,W-2*M)
 elif kind=='image':
  c.setFillColor(ACC);c.setFont('Bold',8.5);c.drawString(M,H-82,es(p.get('tag','')))
  image(p['path'],M,91,W-2*M,H-190)
  para(p['note'],M,77,W-2*M,SM)
 elif kind=='case':
  a=A[p['code']];image(p['path'],M,110,735,H-220)
  y=H-100;y=para('DECISIONES DE ORGANIZACION',815,y,330,HEAD)
  y=blocks(p['texts'],815,y,330)
  y=para(f"<b>{a['habitantes']} residentes</b><br/>{a['suelo_m2']:.2f} m² de suelo geometrico<br/>{a['envolvente_estudio_m2']:.2f} m² de envolvente de estudio",815,y,330)
  y=para(f"<b>Comprobacion parcial:</b> {a['accesos_dormitorios_disco90']}/{a['habitantes']} puertas privadas y {a['accesos_banos_disco90']}/{a['banos']} aproximaciones a aseos conectadas con disco de 90 cm.",815,y,330)
  para('Diagrama nuevo de interpretacion: verde = proximidad; rosa = conflicto por resolver. No son recorridos peatonales ni prueba acustica.',M,81,735,SM)
 elif kind=='areas':
  rows=[['Organizacion','Residentes','Suelo geometrico','Envolvente estudio','Servicios en borde']]
  for code,a in A.items():rows.append([code,str(a['habitantes']),f"{a['suelo_m2']:.2f} m²",f"{a['envolvente_estudio_m2']:.2f} m²",f"{a['aseos_en_borde']}/{a['banos']}"])
  yy=table(rows,M,H-95,[180,130,235,245,312],11)
  para('El suelo incluye huellas de divisiones y no equivale a superficie util normativa. La envolvente es el poligono de suelo expandido 12 cm; no sustituye medicion ejecutiva de estructura o cerramientos.',M,yy,W-2*M)
  para('<b>Advertencia de dimensionado:</b> cinco V01_S sumarian aproximadamente 1.471 m² de envolvente de estudio; cinco V03_D, 1.677 m². El primer caso deja un margen insuficiente para dar por resuelto el conjunto; el segundo supera la hipotesis de 1.500 m². Corregir los banos no acredita que el programa quepa.',M,yy-80,W-2*M)
 elif kind=='programme':
  blocks(['<b>Lo privado.</b> Dormir, vestirse, guardar ropa, trabajar en el tablero individual y retirarse en la bow. La cama no ocupa el eje de entrada.','<b>Lo compartido dentro de una unidad.</b> Preparar comida, comer, conversar, recibir y limpiar. El vestibulo de aseos es una transicion de servicio, no una estancia central.','<b>En V02_P.</b> Se conserva autonomia de dos grupos y un umbral comun. No se presenta como fusion completa: hay dos comedores y dos cocinas.'],M,H-105,515)
  blocks(['<b>En V01_D y V01_S.</b> La llegada, comida, trabajo y estancia pertenecen al grupo de ocho. Los dormitorios mantienen autonomia sin exigir atravesar otra habitacion.','<b>En V03_D y V03_S.</b> El centro de cada ambito vuelve a ser habitable. Las cocinas duplicadas y la longitud del encuentro pueden seguir generando dos subgrupos: es una hipotesis por estudiar.','<b>Acustica y vistas.</b> El filtro visual de aseos no es aislamiento acustico. Falta estudiar conversacion nocturna, intimidad de las puertas privadas y control material de los limites.'],W/2+20,H-105,515)
  para('Comuna es aqui una pregunta espacial y de gestion: compartir requiere acuerdos de uso, cuidado y retirada. Una planta abierta no garantiza esos acuerdos ni obliga a estar siempre en grupo.',M,190,W-2*M,HEAD)
 elif kind=='macro':
  blocks(['<b>La parcela entra como restriccion real.</b> D05 y D06 se conservan como antecedentes. No se han implantado estas ocho plantas ni actualizado las alturas del entorno.','<b>La escala no se corrige encogiendo cuerpos.</b> La compactacion siguiente debe revisar posiciones, cantidad de vestibulo, concentracion de instalaciones y reparto de programa entre unidad y complejo.','<b>La cuenta de 40 residentes.</b> Cuatro personas por unidad y ocho por agrupacion siguen siendo hipotesis comparables. No se afirma que una agrupacion equivalga a una planta completa.'],M,H-105,515)
  blocks(['<b>Relacion con la megaestructura.</b> Soporte y conexiones deberan mantener los bordes privados abiertos, sostener los lugares comunes y permitir acceso sin atravesar viviendas ajenas. Aqui no hay un calculo estructural nuevo.','<b>Fachada textil.</b> La bow necesita control propio; las estancias comunes requieren otros panos segun orientacion y uso. Apertura, recogida y mantenimiento deben formar parte de la seccion.','<b>Prioridad de la proxima fase.</b> Compactar los servicios manteniendolos fuera del centro, contrastar la parcela y probar luz en seccion. No volver a una isla sanitaria para salvar superficie.'],W/2+20,H-105,515)
 elif kind=='checks':
  rows=[['Comprobado en esta revision','Pendiente'],['8 organizaciones nuevas: 3 unidades y 5 agrupaciones.','Implantacion en parcela, alturas y ordenacion urbana.'],['52 accesos privados y 26 aproximaciones a aseos conectados con disco de 90 cm.','Maniobras completas dentro del baño, apertura de equipos y accesibilidad normativa.'],['26 baños en borde; ninguno como isla en el centro del estar.','Extraccion, saneamiento, patinillos y otras instalaciones.'],['52 franjas de 3 m delante de bow libres de la propia planta.','Sol, cielo visible, luz interior y edificios o niveles vecinos.'],['Cero solape entre habitaciones y entre muebles comunes representados.','Acustica, capacidad real de almacenaje, convivencia y simultaneidad completa.'],['Visuales muestreadas hacia las puertas de aseo interceptadas por filtros o cerramientos.','Todos los puntos de vista, dispositivos y estados de puerta.'],['Ocho archivos 3DM reabiertos con geometria valida y Z=0.','Revision nativa visual en Rhino y detalle constructivo/estructural.']]
  table(rows,M,H-95,[551,551],11)
 elif kind=='sources':
  items=['<b>Antecedentes D01-D06.</b> G3_MAPA_ACTIVIDADES_PARCELA_2026-10-18: seis laminas originales. Sus escenas son hipotesis, y el antecedente solar no se recalcula.','<b>Antecedentes D07-D12.</b> G3_UNIDAD_TEJIDO_ACTIVIDADES_2026-10-18: tejido manual, cruces, tres horarios y calibracion. Se explicita la revision posterior de las posiciones iniciales.','<b>Antecedentes D13-D18.</b> G3_TEJIDO_REGLAS_Y_ALTERNATIVAS_2026-10-18: matriz, dos registros de razones y tres tejidos. Se conserva su caracter grafico, sin metros.','<b>Revision geometrica.</b> fuentes/geometria.py y fuentes/laminas.py de esta carpeta. Fuentes de partida preservadas en BASE_ANTES.py. Ocho plantas vigentes en modelos_2d/.','<b>Control de procedencia.</b> INDICE_Y_PROCEDENCIA.json guarda las rutas y SHA-256 de los 18 diagramas originales. GEOMETRIA_FINAL.json registra resultados por organizacion.','<b>Excluido expresamente.</b> Catalogo de 40 plantas homogeneizadas, plantas anteriores con baños centrales y comparaciones que muestren esas plantas como soluciones vigentes. No se han incluido modelos o diagramas ajenos atribuidos a Ruralex.']
  blocks(items[:3],M,H-105,515);blocks(items[3:],W/2+20,H-105,515)
 c.showPage()
c.save();(P/'verificacion/CAJAS_TEXTO.json').write_text(json.dumps(bounds));print(json.dumps({'pdf':str(OUT),'paginas':len(pages),'antecedentes_originales':len(provenance),'plantas_nuevas':len(A),'bytes':OUT.stat().st_size},ensure_ascii=False))
