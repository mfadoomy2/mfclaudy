"""Compila las capturas inspeccionadas de Street View en un atlas documentado."""
from pathlib import Path
import csv, json, re, shutil
from datetime import datetime
from collections import Counter
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

BASE=Path(__file__).resolve().parent
ORIG=BASE/'00_CAPTURAS_ORIGINALES'
QA=BASE/'_verificacion'
QA.mkdir(exist_ok=True)
rows={r['id']:r for r in json.loads((BASE/'registro_capturas.json').read_text()) if r['date'] and r['id']!='SV039'}
for i,title,lat,lon,date,author,heading in [
 (1,'Antigüedades Barranco / Ribera de Curtidores',40.4076084,-3.7071688,'Aug 2016','D Online',0),
 (2,'5 C. de San Cayetano',40.4091249,-3.7068618,'Mar 2022','Google',41.94),
 (3,'5 C. de San Cayetano',40.4091249,-3.7068618,'Mar 2022','Google',90),
]:
 id=f'SV{i:03d}'
 rows[id]=dict(id=id,title=title,date=date,author=author,url=f'https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}&heading={heading}',lat=lat,lon=lon,file=str(ORIG/f'{id}.png'))
AUTHORS={'SV007':'José María','SV008':'José María','SV011':'Jaime Pulido Zazo','SV012':'Jaime Pulido Zazo','SV029':'Virtualy','SV034':'Oscar Duran','SV038':'D Online'}
MONTHS={'Jan':'enero','Feb':'febrero','Mar':'marzo','May':'mayo','Jun':'junio','Jul':'julio','Aug':'agosto','Sep':'septiembre','Dec':'diciembre'}
CAPTIONS={
1:'Cuadros expuestos junto al acceso de una tienda de antigüedades. Concurren persiana metálica, zócalo, losas y bolardos.',
2:'Calle estrecha con pavimento de piezas pequeñas, bandas laterales y bolardos. Rótulos de muebles y marcos bajo viviendas.',
3:'Portal residencial junto a local comercial, reja de cierre, ladrillo visto, balcones y conducciones exteriores. No confundir la muestra de marcos con azulejos.',
4:'Vara de Rey 12: paneles oscuros de lamas, hojas en distintas posiciones y barandillas. La movilidad se infiere de su disposición, no de una secuencia temporal.',
5:'Adoquines, bordillo curvo, farola de varios brazos y coches ocupando el borde. Cambia la escala entre calle y plaza.',
6:'Arbolado alineado, bancos visibles al fondo y borde ocupado por aparcamiento. Una sola imagen no mide frecuencia de estancia ni confort térmico.',
7:'Patio del Museo de Artes y Tradiciones Populares: pies derechos, tornapuntas, madera y apoyos pétreos, junto a cerramientos añadidos. Es un equipamiento rehabilitado.',
8:'Vista complementaria del mismo patio: organización perimetral, apoyos repetidos y cerramientos de distintas intervenciones. La fotografía no permite diagnosticar uniones ni capacidad estructural.',
9:'Embajadores: base pétrea y revoco claro, balcones oscuros y cierres pintados en planta baja. Separación entre base expuesta y plantas residenciales.',
10:'Cruce de Embajadores y Tribulete: bordillos, sumidero, bolardos, farola y señal de aparcamiento. Alternan calzada asfaltada y pavimentos peatonales.',
11:'Corrala de Sombrerete: galerías corridas, pantallas verdes, ropa tendida y estructura oscura sobre paramentos cálidos. Imagen de 2016, no diagnóstico actual.',
12:'Segunda orientación de Sombrerete: galerías con pantallas, muro de borde con grafitis, arbolado y pavimento. Vista de contexto para relacionar fachada doméstica y espacio exterior.',
13:'Cascorro: furgoneta abierta, cajas y carros junto al frente comercial. Escena puntual de logística; no demuestra por sí sola el ciclo del mercado dominical.',
14:'La Ruda: revoco rugoso, base de piezas pétreas, marcos de huecos y escaparates. Los límites entre acabados son más fiables que la identificación exacta de la piedra.',
15:'Detalle de balcones poco salientes: barrotes verticales y franja inferior de volutas. Cableado recorre la línea entre plantas.',
16:'Mira el Río Alta: almoneda con toldo verde, rótulo, persiana y silla colocada en el umbral. El frente combina exposición, protección y acceso.',
17:'Mira el Río Alta: aceras estrechas, bolardos, calzada y locales con apertura directa. Ventanas y balcones se sitúan inmediatamente sobre el comercio.',
18:'Mira el Río Baja: toldo, escaparate enrejado y objetos apoyados fuera del local. La acera actúa como zona de transición y exige comprobar el paso libre.',
19:'Carnero: cierres con grafiti, toldo, zócalo, bajante, haces de cables y farol mural superpuestos en una misma fachada.',
20:'Placa de la calle del Carnero: juntas de piezas cerámicas, ilustración y texto. Evidencia clara de cerámica localizada, no de un revestimiento dominante en todo el barrio.',
21:'Carlos Arniches: tienda de telas con rótulos y escaparate multicolor, frente a vivienda con base rojiza y huecos enrejados.',
22:'Campillo del Mundo Nuevo: espacio abierto, arbolado y pavimentos diferenciados. El poste incorpora una restricción de estacionamiento con horario.',
23:'Detalle legible: «DOMINGOS Y FESTIVOS DE 0 A 16 H.». Es la restricción visible en enero de 2022; no se equipara al horario de venta ni se afirma su vigencia actual.',
24:'Rodas: planos ocre y gris, cierre azul, revoco y ladrillo. Los cambios de color delimitan piezas y usos, sin permitir deducir pigmentos o códigos exactos.',
25:'Fray Ceferino González: zócalo oscuro continuo, revoco rosado, balcones y persianas. El encuentro con el suelo concentra cierres y redes añadidas.',
26:'Peña de Francia: huecos bajos enrejados, balcones con macetas, farol mural y bandas de pavimento. Los elementos protegen y median entre interior y calle.',
27:'Casino: ventanas a distintas cotas respecto de la acera, rejas, macetas y base pétrea. La pendiente obliga a estudiar la sección, no solo el alzado.',
28:'Casino: sombra de arbolado, alcorques, rejillas, pavimento, cerramiento y acceso a un nivel inferior. Imagen puntual, sin medición acústica ni térmica.',
29:'Interior del mercado de San Fernando: puestos, cierres, mesas y acabados lavables en torno a un espacio común. Referencia interior diferenciada del registro de calle.',
30:'Tribulete: jardineras repetidas, cierres pintados, repintes y aparatos de climatización en fachada. La vegetación se combina con instalaciones visibles.',
31:'Cabestreros: puerta de madera con dibujo geométrico, reja y cierre de local, rótulo y balcones. Conviven carpinterías domésticas y dispositivos comerciales.',
32:'Travesía de Cabestreros: ladrillo, revoco, aparatos exteriores y bajantes. El pavimento cambia por bandas y aparecen reparaciones y objetos en el borde.',
33:'Amparo: fachada roja con cercos claros y rejería negra, local naranja y rótulos superpuestos. No se infiere la identidad personal de los residentes o comerciantes.',
34:'Mesón de Paredes: escaparate de minerales, viviendas con vegetación y comercios especializados. La imagen documenta esta actividad en diciembre de 2019.',
35:'Oso: desconchados y repintes sobre una base rugosa, ladrillo de relleno y grandes rejas. Las causas del deterioro no se diagnostican mediante la fotografía.',
36:'Oso: conjunto de imágenes enmarcadas en fachada y una pequeña pieza decorativa. No se confirma cerámica en todos los objetos; sí una composición por adición.',
37:'Santa Ana: fachada rojiza, marcos comerciales rojos, rótulos de tableros y molduras y banderines entre fachadas. La decoración temporal corresponde a agosto de 2018.',
38:'Taller de bordado en Encomienda: escaparate como límite entre calle e interior, mobiliario y objetos expuestos. Es una referencia interior de enero de 2017.',
}
CATS=[
('01_ZOCALOS_Y_REVESTIMIENTOS','Zócalos y revestimientos',[9,14,25,27],
 'Se repite una base diferenciada del cuerpo superior: piezas de apariencia pétrea, revoco o pintura más oscura, con juntas y alturas variables.',
 'Interpretación: la franja baja concentra contacto, instalaciones y mantenimiento. Propuesta: diseñar un zócalo reparable y registrar sus encuentros con puertas y huecos bajos.'),
('02_LADRILLO_Y_MODULACION','Ladrillo y modulación de fachada',[2,3],
 'El ladrillo y los huecos repetidos conviven con una planta baja comercial de módulos distintos. Dos vistas del mismo punto no cuentan como dos casos independientes; véanse también SV016 y SV032.',
 'Propuesta: diferenciar la modulación doméstica de la comercial y resolver su encuentro. No deducir espesores, estructura ni capacidad portante de la imagen.'),
('03_COLOR_Y_CONTRASTE','Color y contraste por capas',[24,33,37],
 'Ocres, rojizos y tonos claros se combinan con metales oscuros y acentos intensos en comercios. La recurrencia es una relación entre capas, no una paleta única.',
 'Propuesta: ordenar base, cuerpo, huecos y elementos móviles mediante contrastes legibles. Los colores de Street View dependen de la luz, la fecha y el procesado; no son mediciones colorimétricas.'),
('04_CERAMICA_Y_ORNAMENTO','Cerámica, imágenes y ornamento',[20,36],
 'La placa de Carnero muestra cerámica identificable. En Oso se observa una composición de piezas enmarcadas cuyo material no siempre puede confirmarse.',
 'Estado: ejemplos localizados; no se demuestra un patrón barrial de azulejos continuos. Propuesta: estudiar señalización, escala de la pieza y sustitución puntual antes de adoptar un motivo decorativo.'),
('05_CERRAJERIA_Y_CARPINTERIA','Cerrajería y carpintería',[15,26,31],
 'Barrotes, volutas, rejas de huecos bajos y puertas trabajadas aparecen en calles diferentes. Su geometría varía con la posición y el uso del hueco.',
 'Propuesta: proyectar protección, ventilación, visibilidad y privacidad conjuntamente. La reja observada no acredita por sí sola cumplimiento de accesibilidad o evacuación.'),
('06_FILTROS_Y_APROPIACION','Filtros y apropiación doméstica',[4,11],
 'Las lamas de Vara de Rey y las pantallas de Sombrerete median entre interior y exterior. Comparten una función de filtro aunque pertenecen a edificios y épocas distintas.',
 'Propuesta: proporcionar filtros regulables, lugares para plantas y soluciones de secado compatibles con el paso. No inferir rutinas, ocupación ni consentimiento colectivo a partir de una imagen.'),
('07_PATIOS_Y_GALERIAS','Patios, galerías y estructura',[7,8,12],
 'La repetición de apoyos y recorridos perimetrales organiza el patio del museo. Sombrerete aporta un contraste residencial. El museo rehabilitado no representa por sí solo la vivienda tradicional en uso.',
 'Propuesta: estudiar la sección calle-portal-patio-galería-vivienda y separar circulación de estancia. Estas vistas permiten una lectura espacial, no una evaluación estructural ni un diagnóstico de habitabilidad.'),
('08_COMERCIO_Y_UMBRAL','Comercio, objetos y umbral',[1,16,18,34,38],
 'Almonedas, antigüedades y talleres muestran objetos y mobiliario cerca del acceso. El límite comercial combina persiana, toldo, escaparate y exposición.',
 'Propuesta: prever almacenamiento y una banda de exposición reversible manteniendo acceso residencial y paso accesible. Una escena de objetos usados no demuestra un balance ambiental ni una cadena de reparación.'),
('09_ROTULOS_Y_EQUIPAMIENTOS','Rótulos y equipamientos cotidianos',[21,29],
 'La información comercial ocupa frisos, toldos y escaparates; el mercado interior añade mesas y puestos alrededor de un espacio compartido.',
 'Propuesta: reservar soportes modificables para información y uso, evitando que cada cambio de actividad implique rehacer la fachada. SV029 es interior y no se contabiliza como frente de calle.'),
('10_PAVIMENTOS_Y_ACCESIBILIDAD','Pavimentos y accesibilidad',[10,17,32],
 'Se repiten pavimentos por bandas, piezas pequeñas en calzada, losas en bordes, bolardos y drenaje. Las secciones oscilan entre vías abiertas y calles estrechas.',
 'Propuesta: levantar cotas, anchos libres, pendientes y encuentros. La fotografía permite localizar conflictos potenciales, pero no certificar dimensiones ni cumplimiento normativo.'),
('11_VERDE_Y_MOBILIARIO','Verde y mobiliario urbano',[5,6,28,30],
 'Árboles, alcorques, jardineras, farolas y bancos forman sistemas repetidos. Cambian el suelo y el borde disponible para caminar o permanecer.',
 'Propuesta: relacionar sombra, asiento y recorridos con suelo permeable y mantenimiento. No extrapolar sombra anual, especies vegetales o confort medido de estas vistas puntuales.'),
('12_INSTALACIONES_Y_DESGASTE','Instalaciones, desgaste y superposición',[19,35],
 'Cables, bajantes, cajas, faroles, grafitis y repintes se superponen a superficies anteriores. La misma condición aparece en SV015, SV030 y SV032.',
 'Propuesta: prever registros accesibles, recorridos de instalaciones y capas reemplazables. Desconchados y manchas son observaciones; humedad, antigüedad y causas requieren comprobación.'),
('13_TIEMPO_Y_LOGISTICA','Tiempo, logística y cambio de uso',[13,22,23],
 'Cascorro aporta una escena de carga; Campillo aporta una restricción explícita de estacionamiento los domingos y festivos. Son evidencias distintas y complementarias.',
 'Propuesta: mantener accesos domésticos y almacenamiento durante cambios de uso de la calle. Faltan capturas verificadas del montaje, los puestos abiertos y la limpieza en el mismo punto.'),
]

for id,r in rows.items():
 if 'lat' not in r:
  m=re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)',r['url'])
  if not m:raise ValueError(id)
  r['lat'],r['lon']=map(float,m.groups())
 r['url']=r['url'] if r['url'].startswith('https:') else 'https://'+r['url']
 r['author']=r.get('author',AUTHORS.get(id,'Google Street View'))
 date=' '.join(r['date'].split()[:2])
 r['fecha_imagen']=' '.join(MONTHS.get(s,s) for s in date.split())
 r['observacion']=CAPTIONS[int(id[2:])]
 r['calidad']='Inspeccionada visualmente; lectura a escala de pantalla'
 r['categorias']=[folder for folder,title,ids,obs,pr in CATS if int(id[2:]) in ids]
 assert r['categorias'], id
 r['precision']='Coordenada de cámara de la panorámica, no del objeto observado'
 # Se retira únicamente la barra del navegador; se conservan los créditos y la imagen.
 with Image.open(r['file']) as im:
  clean=im.crop((0,106,im.width,im.height))
  for folder in r['categorias']:
   target=BASE/folder;target.mkdir(exist_ok=True)
   clean.save(target/f'{id}.png')
 r['foto']=str(BASE/r['categorias'][0]/f'{id}.png')

ordered=[rows[k] for k in sorted(rows)]
sites=len({(r['lat'],r['lon']) for r in ordered})
assert len(ordered)==38
(BASE/'inventario_verificado.json').write_text(json.dumps(ordered,ensure_ascii=False,indent=2),encoding='utf-8')
with (BASE/'puntos_observados_QGIS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 fields=['id','title','lat','lon','fecha_imagen','author','observacion','calidad','precision','url','foto']
 writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(ordered)
geo={'type':'FeatureCollection','features':[{'type':'Feature','geometry':{'type':'Point','coordinates':[r['lon'],r['lat']]},'properties':{k:v for k,v in r.items() if k not in {'file','lat','lon'}}} for r in ordered]}
(BASE/'puntos_observados_QGIS.geojson').write_text(json.dumps(geo,ensure_ascii=False,indent=2),encoding='utf-8')

for folder,title,ids,obs,pr in CATS:
 lines=[f'# {title}', '',obs,'',pr,'','## Evidencias']
 for i in ids:
  r=rows[f'SV{i:03d}'];lines+=['',f"### {r['id']} - {r['title']}",r['observacion'],f"Fecha: {r['fecha_imagen']}. Autor: {r['author']}.",f"Cámara: {r['lat']}, {r['lon']}. {r['precision']}.",r['url']]
 (BASE/folder/'LECTURA.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

W,H=A4;M=38;WIDTH=W-2*M
pdf=BASE/'ATLAS_PATRONES_STREET_VIEW_EL_RASTRO.pdf'
c=canvas.Canvas(str(pdf),pagesize=A4)
c.setTitle('El Rastro - Atlas visual de patrones observados')
c.setAuthor('Investigación G3 - observaciones sobre Google Maps / Street View')
styles={
 'body':ParagraphStyle('body',fontName='Times-Roman',fontSize=10.5,leading=13.5),
 'small':ParagraphStyle('small',fontName='Times-Roman',fontSize=8,leading=10),
 'title':ParagraphStyle('title',fontName='Times-Bold',fontSize=21,leading=24),
 'head':ParagraphStyle('head',fontName='Times-Bold',fontSize=12,leading=15),
}
page=0
def para(text,y,style='body',width=WIDTH,x=M):
 p=Paragraph(text,styles[style]);_,h=p.wrap(width,H);p.drawOn(c,x,y-h);return y-h-8
def start(title,kicker='EL RASTRO / INVESTIGACIÓN VISUAL'):
 global page
 page+=1
 c.setFont('Times-Roman',8);c.drawString(M,H-24,kicker)
 c.setFont('Times-Roman',8);c.drawString(M,20,'Google Maps / Street View. Autor y fecha por imagen. Consulta '+datetime.now().strftime('%d/%m/%Y'))
 c.drawRightString(W-M,20,str(page))
 return para(escape(title),H-43,'title')-4
def end():c.showPage()
def photo(r,y):
 im=Image.open(r['foto']);height=min(240,WIDTH*im.height/im.width)
 image_width=height*im.width/im.height
 c.drawImage(r['foto'],(W-image_width)/2,y-height,width=image_width,height=height)
 y-=height+5
 y=para(f"<b>{r['id']} · {escape(r['title'])}</b> | {escape(r['fecha_imagen'])} | {escape(r['author'])}",y,'small')
 y=para(escape(r['observacion']),y,'small')
 y=para(f"Cámara WGS84: {r['lat']:.7f}, {r['lon']:.7f}. <link href='{escape(r['url'])}'>Abrir la vista original</link>.",y,'small')
 return y-6

y=start('Patrones materiales y formas de habitar')
y=para('El Rastro y su entorno. Atlas fotográfico comentado para el proyecto de Ribera de Curtidores 31.',y)
y=para(f'<b>{len(ordered)} capturas · {sites} posiciones de cámara · {len(CATS)} categorías</b>',y)
y=photo(rows['SV016'],y-8)
y=para('<b>Alcance real.</b> Muestreo visual dirigido de calles, plazas y referencias de la investigación. No es un recorrido exhaustivo de los miles de entidades del inventario OSM. Cada punto de este atlas está documentado; los demás permanecen sin revisar.',y)
y=para('Las imágenes consultadas abarcan de agosto de 2016 a marzo de 2022. La fecha de consulta no actualiza la fotografía. No se ha comprobado sistemáticamente que cada panorámica sea la más reciente disponible.',y)
y=para('Fondo blanco y texto negro; el color se conserva únicamente en las fotografías como dato de observación. Se mantienen las atribuciones visibles de Google Maps y de los colaboradores.',y)
end()
y=start('Cómo leer la evidencia')
for title,body in [
 ('1. Observación','Se describen formas, posiciones, acabados aparentes, objetos y textos realmente visibles. No se asigna composición química a un material ni identidad o situación social a una persona.'),
 ('2. Recurrencia','Un motivo se considera recurrente en esta muestra cuando aparece en posiciones distintas. Dos giros de una misma panorámica no equivalen a dos casos. No se calculan porcentajes de todo el barrio.'),
 ('3. Interpretación','La función sugerida de un zócalo, filtro o umbral es una lectura arquitectónica; debe contrastarse con uso, mantenimiento y medición in situ.'),
 ('4. Aplicación','Las propuestas para vivienda joven son hipótesis de proyecto: no prescripciones normativas ni conclusiones causales demostradas.'),
 ('5. Geolocalización','Las coordenadas sitúan la cámara. El objeto puede estar en otra fachada, al otro lado de la calle o dentro de un inmueble. El título automático de Google no siempre es la dirección del objeto fotografiado.'),
 ('6. Cobertura','Las vías principales y transversales seleccionadas incluyen Curtidores, San Cayetano, Vara de Rey, Carlos Arniches, Embajadores, Sombrerete, Cascorro, La Ruda, Mira el Río Alta y Baja, Carnero, Rodas, Fray Ceferino, Peña de Francia, Casino, Tribulete, Cabestreros, Amparo, Mesón de Paredes, Oso, Santa Ana y Encomienda.'),
 ('7. Límites','No se han documentado todos los edificios, patios privados o portales. Faltan secuencias completas del mercado en domingo, detalle suficiente de azulejos comerciales, mediciones de accesibilidad, ruido y temperatura. Las vistas generales no sustituyen fotografías de detalle ni una inspección física.'),
 ('8. Especificidad','Los patrones registrados son locales en cuanto a su evidencia, pero no se demuestra que sean exclusivos o necesarios solo en El Rastro. Para afirmarlo haría falta comparar barrios y verificar usos.'),
]:
 y=para(escape(title),y,'head');y=para(escape(body),y)
end()

for folder,title,ids,obs,proposal in CATS:
 for offset in range(0,len(ids),2):
  selected=ids[offset:offset+2]
  y=start(title+(' / continuación' if offset else ''),folder.split('_')[0]+' / CATÁLOGO DE PATRONES')
  if offset==0:y=para(escape(obs),y)
  for i in selected:y=photo(rows[f'SV{i:03d}'],y)
  y=para('<b>Lectura de proyecto.</b> '+escape(proposal),y)
  if y<34:raise RuntimeError(f'Contenido desbordado {title} {offset}: {y}')
  end()

y=start('Patrones cruzados y decisiones')
for title,body in [
 ('Una base estable y capas que cambian','SV009, SV014, SV019 y SV025 muestran zócalos junto a cierres, cables y rótulos. Hipótesis: separar la base duradera de las piezas de desgaste y de los soportes modificables, con uniones registrables.'),
 ('El umbral trabaja','SV001, SV016 y SV018 muestran objetos junto a accesos; SV013 añade logística. Hipótesis: diseñar una reserva de almacenamiento y exposición que no absorba el vestíbulo residencial ni el paso público.'),
 ('La domesticidad necesita filtros graduados','SV004, SV011, SV026 y SV027 relacionan calle, galería, reja y vivienda. Hipótesis: combinar distancia, visibilidad y elementos regulables; la convivencia no debe depender de mantener siempre abierto el interior.'),
 ('El suelo organiza situaciones distintas','SV010, SV017, SV022 y SV028 muestran cruces, calles estrechas, plazas y bordes verdes. Hipótesis: dibujar secciones que integren pendientes, drenaje, estancia y paso, con cotas obtenidas por levantamiento.'),
 ('La identidad también se construye por adición','SV020, SV021, SV031, SV036 y SV037 reúnen cerámica puntual, rótulos, carpinterías y decoración temporal. Hipótesis: habilitar soportes para modificación y apropiación; no reducir la identidad a copiar un azulejo.'),
 ('El tiempo deja requisitos físicos','SV023 documenta una restricción semanal en una fecha concreta, y SV013 una escena de reparto. Hipótesis: estudiar acceso, carga, residuos y descanso en varios horarios antes de dimensionar espacios.'),
]:
 y=para(escape(title),y,'head');y=para(escape(body),y)
end()
y=start('Qué falta para cerrar la investigación')
for title,body in [
 ('Recorrido exhaustivo','Cruzar el inventario OSM completo con puntos efectivamente vistos, agrupar duplicados de fachada y anotar ausencia de cobertura. Este atlas no sustituye esa auditoría entidad por entidad.'),
 ('Materiales y cerámica','Fotografías frontales con escala de zócalos, juntas, azulejos, carpinterías y rejas. Comprobar material, acabado, reparación y continuidad. La cerámica aquí queda localizada, no generalizada.'),
 ('Temporalidad del mercado','Volver al mismo punto durante montaje, actividad, desmontaje y jornada laborable. Registrar fecha, orientación y franjas, sin inferir patrones temporales a partir de imágenes de años diferentes.'),
 ('Uso y habitabilidad','Medir paso libre, cotas de ventanas, altura de zócalos, profundidad de umbrales y galerías. Contrastar con observación de estancia y entrevistas voluntarias; la fotografía no explica por sí sola cómo se vive.'),
 ('Comparación','Añadir un tramo de control de otro barrio para distinguir soluciones madrileñas generales de concentraciones específicas del Rastro.'),
 ('Aplicación inmediata en QGIS','Cargar puntos_observados_QGIS.geojson. Cada captura enlaza a su imagen y a la panorámica. Filtrar por categorías y fecha; contar posiciones distintas, no filas repetidas. Las coordenadas son de cámara, no levantamientos de elementos.'),
]:
 y=para(escape(title),y,'head');y=para(escape(body),y)
end()

for startidx in range(0,len(ordered),12):
 y=start('Registro de fuentes y coordenadas'+(' / continuación' if startidx else ''))
 y=para('Latitud, longitud de cámara (WGS84). Los enlaces abren la vista conservada; la fuente conserva sus derechos. Fecha indicada: captura fotográfica.',y,'small')
 for r in ordered[startidx:startidx+12]:
  y=para(f"<b>{r['id']} · {escape(r['title'])}</b><br/>{r['lat']:.7f}, {r['lon']:.7f} · {escape(r['fecha_imagen'])} · {escape(r['author'])}<br/><link href='{escape(r['url'])}'>Google Maps / Street View - abrir fuente</link>",y,'small')
 end()
c.save()

# Contactos para verificación visual, no como sustituto de las fotografías del atlas.
for block in range(0,len(ordered),12):
 sheet=Image.new('RGB',(1200,4*225),'white');draw=ImageDraw.Draw(sheet)
 for j,r in enumerate(ordered[block:block+12]):
  im=Image.open(r['foto']);im.thumbnail((390,194))
  x=(j%3)*400;y=(j//3)*225
  sheet.paste(im,(x,y));draw.text((x+5,y+198),r['id']+' '+r['title'][:42],fill='black')
 sheet.save(QA/f'contacto_{block//12+1}.jpg')
(BASE/'LEEME.md').write_text(f'''# Atlas visual de patrones

{len(ordered)} capturas verificadas, {sites} posiciones de cámara y {len(CATS)} categorías. Alcance: muestreo dirigido; no inventario exhaustivo.

- ATLAS_PATRONES_STREET_VIEW_EL_RASTRO.pdf: fotografías grandes, lecturas, conclusiones y fuentes.
- Carpetas 01 a 13: fotografías sin barra del navegador y LECTURA.md.
- 00_CAPTURAS_ORIGINALES: capturas originales preservadas.
- puntos_observados_QGIS.geojson y .csv: posiciones de cámara, observaciones, fechas, fotos y enlaces.
- inventario_verificado.json: registro depurado; usar este y no el registro de captura bruto para análisis.
- _verificacion: imágenes auxiliares de control editorial.

Fechas fotográficas: 2016-2022. Las vistas son observaciones históricas. No se afirma actualidad, exhaustividad o exclusividad barrial.
Las vistas generales no sustituyen fotografías de detalle ni una inspección física. No se generaron fotografías ni se reconstruyeron texturas con IA.
Se han conservado atribuciones y créditos de Google Maps y sus colaboradores. Los objetos enmarcados de Oso no se clasifican automáticamente como azulejos.
''',encoding='utf-8')
print(json.dumps({'pdf':str(pdf),'pages':page,'photos':len(ordered),'positions':sites,'categories':len(CATS)},ensure_ascii=False))
