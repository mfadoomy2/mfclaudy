from pathlib import Path
import json,re,hashlib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
P=Path(__file__).resolve().parents[1];R=P.parent;L=P/'laminas';O=P/'output/pdf/G3_PLANTAS_CORREGIDAS_Y_PRUEBA_PARCELA.pdf'
A=json.loads((P/'verificacion/CONTROL_GEOMETRICO.json').read_text())['plantas'];S=json.loads((P/'verificacion/ENCAJE_PARCELA.json').read_text())['resultados']
old=json.loads((P/'fuentes/ANTECEDENTES.json').read_text())
for orig in old['paginas']:
 if orig['imagen']:orig['imagen']=str(P/'fuentes/antecedentes'/Path(orig['imagen']).name)
for orig in old['fuentes_originales']:orig['archivo']=str(P/'fuentes/antecedentes'/Path(orig['archivo']).name)
from lengua import es
for n,f in [('Regular','Arial.ttf'),('Bold','Arial Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/System/Library/Fonts/Supplemental/'+f))
W,H=landscape(A3);M=42;INK=HexColor('#263d35');BG=HexColor('#faf8f2');ROSE=HexColor('#b94c6c')
ST=ParagraphStyle('body',fontName='Regular',fontSize=12,leading=18,textColor=INK);SM=ParagraphStyle('small',parent=ST,fontSize=9,leading=13);HEAD=ParagraphStyle('head',parent=ST,fontName='Bold',fontSize=16,leading=23)
pages=[]
def add(title,kind,**kw):pages.append(dict(title=title,kind=kind,**kw))
add('CORREGIR LA UNIDAD / CONTRASTAR LA PARCELA','cover')
add('Cómo se vive: diferencias que conviene conservar','criteria')
add('La habitación: vestidor, bow y tablero A1','image',path=L/'HABITACION_ACTUAL.svg',note='18,35 m² de geometría privada. Cama 1,25 x 2,00 m, tablero 1,80 x 0,90 m. La prueba corporal de 80 cm conecta entrada, cama, vestidor y bow; no equivale a accesibilidad normativa.')
add('Servicios integrados en el borde','image',path=L/'DETALLE_SERVICIOS.svg',note='Dos ámbitos de baño de 3,40 m² geométricos; paso nominal 1,20 x 2,00 m, con ancho libre aproximado de 1,08 m entre muros. Puertas laterales, sin pantalla suelta ni vestíbulo de estancia. Aparatos esquemáticos; sus maniobras y accesibilidad siguen por desarrollar.')
add('Tres unidades / misma escala / distinta convivencia','image',path=L/'COMPARACION_UNIDADES.svg',note='Se repite una prestación privada, no toda la organización. V01 es continua, V02 diferencia dos ámbitos y V03 coloca el estar en el cruce central.')
NAMES={'V01_U':'V01 / convivencia continua','V02_U':'V02 / dos ámbitos','V03_U':'V03 / cruce central','V02_P':'V02 / dos grupos y un umbral','V01_D':'V01 / encuentro mayor','V01_S':'V01 / una casa de ocho','V03_D':'V03 / plaza entre estancias','V03_S':'V03 / continuidad diagonal'}
TEXT={
'V01_U':['Cocinar, comer y estar se suceden en una sala continua. Facilita encontrarse sin reservar una sala a cada actividad.','Los servicios se absorben en el extremo oeste: el suelo baja de 134,17 a 122,70 m² respecto a la corrección anterior. No se reducen las habitaciones.','La mesa de cuatro gira; quedan pasos hasta las puertas con los asientos representados. El conflicto pendiente es conversar o cocinar mientras alguien duerme.'],
'V02_U':['El ámbito izquierdo sirve para comer o estar más tranquila; el derecho reúne cocina y conversación. El estrechamiento permite graduar la relación, aunque hoy no aísla el sonido.','Servicios compactos en el borde izquierdo. El suelo baja de 137,67 a 126,26 m² respecto a la versión anterior.','Escena de contraste: una persona prepara comida tarde y otra trabaja o cena al otro lado. Falta desarrollar el cierre entre ámbitos si se necesita silencio real.'],
'V03_U':['El estar ocupa el cruce. Cocinar queda en el borde sureste y comer al suroeste; los baños se integran en el borde noroeste.','Se desplazan los dormitorios norte y oeste y se reconstruyen sus llegadas. La curva organiza el espacio; el último tramo de cada puerta sigue siendo recto.','El sofá se centra sin cortar las llegadas. La exposición de cuatro puertas al estar es mayor que en V02: requiere estudiar intimidad y acústica antes de elegir.'],
'V02_P':['Dos grupos de cuatro mantienen comedor y cocina propios; comparten un umbral que admite encuentros breves.','Sirve para comparar convivencia con autonomía frente a una casa totalmente fusionada. El umbral no se convierte en un baño ni almacén.','Dos cocinas y dos comedores son una decisión de gestión y superficie, no una necesidad universal. No equivale a compartirlo todo.'],
'V01_D':['Una sala mayor para ocho admite comer juntas, recibir y reunirse. Cocina principal, apoyo de despensa y trabajo quedan repartidos en los antiguos ámbitos.','Los servicios se integran en ambos extremos. Un sofá adicional refuerza que el encuentro no sea solo comedor.','La unión cuesta más suelo que V01_S. Se mantiene como referencia de encuentro intenso, no como ganadora automática por ser más espectacular.'],
'V01_S':['Una casa de ocho sin puerta entre antiguas unidades: cocinar, trabajar, comer y estar forman un continuo.','Dos dormitorios se desplazan 0,90 m para liberar la llegada. Se conservan ocho vestidores transitables y ocho bow pequeñas.','Es la referencia de comunidad con menor suelo entre las cuatro uniones V01/V03. Esa ventaja no resuelve su acceso en la posición ensayada sobre la parcela.'],
'V03_D':['Dos estancias circulares se relacionan a través de una plaza. Los baños permanecen en los bordes exteriores.','Se separan más los grupos para que la mesa no bloquee la unión. La mesa de ocho se dispone horizontal y desplazada 1,50 m respecto al centro de la plaza.','El acceso se lleva al borde suroeste de la primera estancia. El encuentro es amplio, pero aumenta el suelo a 279,46 m² y no encaja en la posición de parcela ensayada.'],
'V03_S':['La sala diagonal enlaza dos cruces centrales; la mesa de ocho gira 45 grados y se desplaza 1,50 m para liberar la continuidad.','Los tableros individuales quedan en las habitaciones: se retiran dos mesas de apoyo que competían con los recorridos compartidos.','Mantiene dos cocinas y dos estancias locales. La continuidad espacial no garantiza que se forme un único grupo; queda como alternativa, con encaje de parcela no resuelto.']}
for a in A:
 code=a['codigo'];add(NAMES[code]+' / relaciones y decisiones','case',code=code,path=L/(code+'_DIAGRAMA_NUEVO.svg'),text=TEXT[code]);add(NAMES[code]+' / planta corregida','image',path=L/(code+'_PLANTA_CORREGIDA.svg'),note=f"{a['habitantes']} residentes / {a['suelo_m2']:.2f} m² de suelo geométrico / {a['envolvente_estudio_m2']:.2f} m² de envolvente de estudio. Las comprobaciones corresponden a esta geometría 2D, no a un modelo construido.")
add('Superficie y capacidad / la cuenta de 40 residentes','areas')
add('La parcela real / contexto sin la megaestructura anterior','image',path=L/'PARCELA_CONTEXTO.svg',note='Polígono local de 650,91 m², derivado de Catastro. Origen UTM 439984, 4473229.4; EPSG:25830. El norte dibujado es el de cuadrícula. Las huellas vecinas no son alturas medidas.')
for a,s in zip(A,S):
 add(NAMES[a['codigo']]+' / contraste con la parcela','image',path=L/(a['codigo']+'_PARCELA.svg'),note='Prueba por giro y traslación, sin escalar cuerpos ni muebles. El contorno incluye 12 cm de margen de estudio. La banda de 3 m delante de cada bow es una reserva geométrica; no es una prueba de sol o iluminación.')
add('Qué decidimos ahora / luz, acceso y megaestructura','decision')
add('Comprobaciones / alcance de esta revisión','checks')
add('Procedencia / leer los diagramas sin inventar causalidad','sources')
for orig in old['paginas']:
 if orig['titulo'].startswith('D') and orig['imagen']:
  add(orig['titulo']+' / antecedente','image',path=Path(orig['imagen']),note=next((f['nota'] for f in old['fuentes_originales'] if f['archivo']==orig['imagen']),'Diagrama previo de investigación. No es una planta vigente ni una generación matemática exacta de estas plantas.'))
assert len(pages)==52,len(pages)
c=canvas.Canvas(str(O),pagesize=(W,H),pageCompression=1);c.setTitle('G3 - Plantas corregidas y prueba de parcela');c.setAuthor('G3 / Documento de trabajo / 19.10.2026')
boxes=[]
def para(t,x,y,w,style=ST):
 p=Paragraph(es(t),style);_,h=p.wrap(w,H);assert y-h>45,(page,t[:60],y,h);p.drawOn(c,x,y-h);boxes.append([page,x,y-h,w,h]);return y-h-13
def blocks(ts,x,y,w):
 for t in ts:y=para(t,x,y,w)
 return y
def picture(path,x,y,w,h):
 if path.suffix=='.svg':
  d=svg2rlg(str(path));k=min(w/d.width,h/d.height);c.saveState();c.translate(x+(w-d.width*k)/2,y+(h-d.height*k)/2);c.scale(k,k);renderPDF.draw(d,c,0,0);c.restoreState()
 else:
  from reportlab.lib.utils import ImageReader
  from PIL import Image
  im=Image.open(path);iw,ih=im.size;k=min(w/iw,h/ih);c.drawImage(ImageReader(im),x+(w-iw*k)/2,y+(h-ih*k)/2,width=iw*k,height=ih*k,mask='auto')
def table(rows,x,y,widths,fs=11):
 st=ParagraphStyle('t',parent=ST,fontSize=fs,leading=fs+4);t=Table([[Paragraph(es(str(v)),st) for v in r] for r in rows],colWidths=widths);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),HexColor('#dbe5d9')),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#f1ede4'),BG]),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]));_,h=t.wrap(sum(widths),H);assert y-h>55,(page,h);t.drawOn(c,x,y-h);return y-h-20
for page,p in enumerate(pages,1):
 c.setFillColor(BG);c.rect(0,0,W,H,fill=1,stroke=0);c.setFillColor(INK);c.setFont('Bold',20);c.drawString(M,H-45,es(p['title']));c.setLineWidth(.5);c.setStrokeColor(INK);c.line(M,H-62,W-M,H-62);c.setFont('Regular',8);c.drawString(M,25,'G3 / 19.10.2026 / Plantas nuevas corregidas + ensayo de parcela');c.drawRightString(W-M,25,f'{page:02d} / {len(pages)}')
 k=p['kind']
 if k=='cover':
  para('Investigación > actividades y conflictos > unidad > unión > parcela > megaestructura',M,H-95,W-2*M,HEAD)
  picture(L/'COMPARACION_UNIDADES.svg',M,180,W-2*M,470)
  blocks(['<b>Ocho plantas corregidas.</b> Servicios compactos en borde, recorridos revisados y habitación con vestidor transitable y bow curva pequeña.','<b>Continuidad del plan original.</b> Pruebas a escala 1:1 sobre la parcela real. Se distinguen encaje de contorno, llegada desde calle y reserva exterior de las ventanas.','<b>Lectura:</b> páginas 2-22, unidad y uniones; 23-31, parcela; 32-34, decisiones y control; 35-52, los 18 diagramas de procedencia.'],M,175,W-2*M)
 elif k=='criteria':
  rows=[['Situación concreta de proyecto','V01 / continua','V02 / dos ámbitos','V03 / cruce'],['Cocinar tarde mientras otra persona descansa','Encuentro fácil; cocina y charla comparten la misma sala. Necesita control del ruido.','Puede separar temporalmente trabajo tranquilo y preparación. El estrechamiento no aísla por sí solo.','Cocina lateral, pero los cuatro accesos privados se relacionan con el estar.'],['Cenar cuatro / recibir una visita','Mesa en la secuencia cotidiana; el estar permanece al otro extremo.','Dos lugares reconocibles permiten recibir sin apropiarse de toda la casa.','Mayor centralidad de la estancia, con comedor fuera de los pasos radiales.'],['Retirarse sin dejar de vivir en grupo','Bow y tablero privados; llegada directa desde el común.','Mayor posibilidad de graduar participación entre ámbitos.','La retirada tiene una llegada más expuesta; es un conflicto a proyectar.'],['Compartir ocho sin repetir una vivienda dos veces','D y S ensayan una sola casa; S utiliza menos suelo.','P conserva dos grupos y comparte el umbral.','D y S crean relación diagonal, a costa de mayor extensión.']]
  y=table(rows,M,H-95,[225,293,293,293],11)
  para('Son escenas y juicios de proyecto, no resultados de entrevistas o una medición sociológica. La acampada aporta negociación, cuidados y uso colectivo; no obliga a trasladar literalmente objetos de un campamento al salón.',M,y,W-2*M)
  para('Reglas comunes: ninguna isla de baños en el estar; una habitación por persona; acceso libre; vestidor transitable; bow cóncava para sentarse; puerta en tramo recto; fachada textil como dispositivo por desarrollar.',M,y-85,W-2*M,HEAD)
 elif k=='image':
  picture(p['path'],M,95,W-2*M,H-183);para(p['note'],M,80,W-2*M,SM)
 elif k=='case':
  a=next(a for a in A if a['codigo']==p['code']);picture(p['path'],M,120,740,H-220)
  y=blocks(p['text'],810,H-103,335)
  y=para(f"<b>{a['habitantes']} residentes</b><br/>{a['suelo_m2']:.2f} m² suelo<br/>{a['envolvente_estudio_m2']:.2f} m² envolvente de estudio",810,y,335)
  para(f"<b>Control 2D:</b> {a['accesos_dormitorios_disco90']}/{a['habitantes']} llegadas privadas y {a['accesos_banos_disco90']}/{a['banos']} llegadas a baños conectadas con disco de 90 cm.",810,y,335)
  para('Diagrama nuevo de interpretación: proximidades y conflictos. Las líneas no representan recorridos peatonales ni una deducción matemática desde los diagramas originales.',M,88,740,SM)
 elif k=='areas':
  rows=[['Planta','Personas','Suelo m²','Envolvente m²','Aproximaciones privadas / baños']]
  for a in A:rows.append([a['codigo'],a['habitantes'],f"{a['suelo_m2']:.2f}",f"{a['envolvente_estudio_m2']:.2f}",f"{a['accesos_dormitorios_disco90']}/{a['habitantes']} y {a['accesos_banos_disco90']}/{a['banos']}"])
  y=table(rows,M,H-95,[170,120,195,220,399])
  y=para('El suelo geométrico incluye huellas de divisiones y no equivale a superficie útil normativa. La envolvente es el suelo expandido 12 cm: un comparador de estudio, no medición ejecutiva.',M,y,W-2*M)
  para('<b>40 residentes / objetivo provisional de 1.500 m²:</b> cinco V01_S suman 1.348,55 m² de envolvente; quedan 151,45 m² para el resto. Cinco V01_D suman 1.454,95 m², con 45,05 m² restantes. No se han incluido ascensor, escaleras, estructura, instalaciones generales y programa común del complejo: ninguna cuenta demuestra aún que el conjunto quepa.',M,y-8,W-2*M)
 elif k=='decision':
  rows=[['Prueba en parcela','Hallazgo','Consecuencia de diseño'],['Contorno a escala real','Seis ensayos quedan dentro. V03_D y V03_S invaden 5,44 y 4,15 m² en las posiciones obtenidas.','Mantener esas dos como alternativas espaciales; no venderlas como implantaciones resueltas. La búsqueda no prueba imposibilidad global.'],['Llegada exterior desde calle','En las posiciones ensayadas conectan V01_U, V02_U y V01_D con el disco exterior de 90 cm.','Las otras posiciones requieren nueva puerta o enlace de acceso. Caber geométricamente no basta.'],['Luz y orientación','Solo 0-2 bandas de 3 m por planta quedan enteramente en la parcela. Una banda puede salir a calle o a propiedad vecina: no significan lo mismo.','Distinguir frente libre, medianera, hueco propio y cielo en sección. La reserva no equivale a iluminación medida.'],['Forma de la megaestructura','V01_S es la referencia de compartir con menor suelo; V02 conserva graduación de actividades.','Ensayar una organización derivada de ambas prestaciones sobre la parcela, sin copiar toda su silueta ni apilar estas posiciones automáticamente.']]
  y=table(rows,M,H-95,[205,420,479],11)
  para('<b>El siguiente dibujo sigue el plan original:</b> sección del lugar + accesos + habitaciones hacia frentes realmente abiertos. Después se incorporan soporte, conexiones y telas según luz, protección y mantenimiento. La idea de crecer hacia arriba queda como hipótesis, pendiente de alturas y estructura.',M,y,W-2*M,HEAD)
 elif k=='checks':
  rows=[['Verificado en esta entrega','Límite de esa comprobación'],['8 plantas, 52 habitaciones y 26 baños representados.','Son 8 ensayos alternativos, no 52 dormitorios a construir juntos.'],['52 llegadas privadas y 26 llegadas a baños conectadas con disco de 90 cm.','No acredita accesibilidad legal, evacuación o maniobras dentro del baño.'],['Cero solapes entre habitaciones, muebles comunes y muros; entrada exterior sin muro atravesado.','Geometría 2D de los elementos representados. No sustituye modelado constructivo.'],['52 bandas delante de las bow libres de la propia planta.','No considera luz interior, altura vecina o sombras de plantas superiores.'],['Visuales muestreadas hacia la posición de los WC interceptadas por cerramientos.','No afirma que todas las puertas de baño sean invisibles desde todo el estar.'],['8 modelos de plantas y 8 ensayos de parcela reabiertos con geometría válida. Todo a Z=0.','Son curvas editables, no una actualización 3D ni una revisión nativa visual en Rhino.'],['Parcela y contexto con coordenadas conservadas; escala 1:1.','Faltan alturas medidas, definición urbanística, acceso vertical, soleamiento y estructura.']]
  table(rows,M,H-95,[552,552],11)
 elif k=='sources':
  blocks(['<b>Geometría vigente.</b> fuentes/geometria.py, fuentes/laminas.py y modelos_2d/. Los archivos anteriores se conservan en sus carpetas; no se sobrescriben.','<b>Parcela.</b> G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16/fuentes/parcela_local.geojson. Contexto: INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/DATOS/DERIVADOS/catastro_partes_400m.geojson.','<b>Búsqueda de encaje.</b> Rotación y traslación de la envolvente a escala 1:1. Optimización heurística de invasión y ajuste con margen de 5 cm. Solo se informa de las posiciones obtenidas.'],M,H-105,520)
  blocks(['<b>18 diagramas originales / páginas 35-52.</b> Situaciones, red, conflictos, parcela, tejido, horarios, calibración, matriz y alternativas. Se reproducen como procedencia, no como plantas vigentes.','<b>Traducción arquitectónica.</b> Las decisiones añadidas se explican en páginas 6-21. No existe una derivación automática única desde esos puntos a V01, V02 o V03.','<b>Control.</b> CONTROL_GEOMETRICO.json y ENCAJE_PARCELA.json conservan valores y alcance. Esta revisión sustituye las ocho plantas del documento anterior, no incorpora el catálogo homogeneizado de 40.'],W/2+18,H-105,520)
  para('Ruralex permanece como referencia metodológica previa. Estas plantas no se atribuyen a su autor ni se presentan como copia de su forma. No se han añadido nuevas fuentes de campo en esta revisión.',M,180,W-2*M)
 c.showPage()
c.save()
(P/'verificacion/INDICE_ACTUAL.json').write_text(json.dumps([{'pagina':i+1,'titulo':p['title'],'tipo':p['kind'],'fuente':str(p.get('path',''))} for i,p in enumerate(pages)],ensure_ascii=False,indent=2))
(P/'verificacion/CAJAS_TEXTO.json').write_text(json.dumps(boxes))
print(O,len(pages),O.stat().st_size)
