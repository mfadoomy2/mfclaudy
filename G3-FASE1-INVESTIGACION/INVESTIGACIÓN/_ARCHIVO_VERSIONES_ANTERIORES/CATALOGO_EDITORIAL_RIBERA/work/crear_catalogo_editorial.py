"""Edición autónoma A4: evidencia, cartografía y análisis vectorial."""
from pathlib import Path
import ast,json,math,shutil,re,sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
from collections import Counter,defaultdict
from shapely.geometry import shape,Point,box
from shapely.ops import transform,unary_union
from pyproj import Transformer

SRC=Path('/Volumes/T7/G3 Proyectos/INVESTIGACIÓN/CATALOGO_CORREGIDO_RIBERA/work/crear_revision.py')
code=SRC.read_text()
# Reuse the verified observations and drawing primitives without executing the old edition.
exec(compile(code.split('W,H=595.276')[0],str(SRC),'exec'))
tree=ast.parse(code)
for node in tree.body:
 if isinstance(node,ast.FunctionDef) or (isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DIAG' for t in node.targets)):
  exec(compile(ast.Module(body=[node],type_ignores=[]),str(SRC),'exec'))
BASE=ROOT/'CATALOGO_EDITORIAL_RIBERA';WORK=BASE/'work';WORK.mkdir(parents=True,exist_ok=True)
PDF=BASE/'RIBERA_DE_CURTIDORES_PATRONES_Y_MATERIA.pdf'
W,H=595.276,841.89;PAGE=0;manifest=[];pages=[]
C=canvas.Canvas(str(PDF),pagesize=(W,H),pageCompression=1)
C.setTitle('Ribera de Curtidores · Patrones y materia')
C.setAuthor('Investigación G3')
def page(kicker,title):
 global PAGE
 if PAGE:C.showPage()
 PAGE+=1;pages.append({'page':PAGE,'section':kicker,'title':title})
 C.setFillColor(colors.black);C.setStrokeColor(colors.black);C.setDash();C.setLineWidth(.7)
 C.setFont('Times-Roman',9);C.drawString(42,H-34,'RIBERA DE CURTIDORES / INVESTIGACIÓN G3');C.drawRightString(W-42,28,str(PAGE))
 C.bookmarkPage(f'p{PAGE}');C.addOutlineEntry(title,f'p{PAGE}',0)
 p(kicker.upper(),42,H-66,W-84,9)
 return p(title,42,H-86,W-84,23,25,True)-18

# Concise analytical voice. Measurement limits live in the method and source captions.
TEXT=[
('El hueco vertical, la barandilla y la posición en una retícula de plantas forman una unidad reconocible. El balcón corrido reúne varios huecos dentro de un mismo borde.',
 'Siete casos organizan balcones individuales; B08 presenta bandas continuas. La diferencia está en la unidad que da forma al límite entre vivienda y calle.',
 '¿Qué conviene compartir: el borde exterior, la sombra, el acceso o solo la regla de fachada?',
 'Comparar un borde por vivienda y otro colectivo con el mismo programa de 20 unidades. Dibujar privacidad, estancia y mantenimiento.'),
('La pared cambia en su contacto con el suelo: aparecen juntas, placas y machones pétreos. El acceso interrumpe esa banda y define el encuentro con la carpintería.',
 'B01 y B13 tienen una franja baja; B02 reviste casi toda la planta de acceso. B05 concentra las piezas en los bordes del hueco.',
 '¿Qué superficie recibirá apoyo de objetos, roce, limpieza y reposición en la planta baja común?',
 'Resolver una banda por piezas sustituibles. Dibujar juntas, umbral y encuentro con puerta antes de elegir el acabado.'),
('Barras y bastidores forman un plano delante de la carpintería. La puerta enrejada, la reja y la barandilla gradúan la relación visual con el interior.',
 'Astoria combina barras y faldón inferior. Los portales de B09 y B11 mantienen transparencia; el balcón desplaza ese plano hacia el exterior.',
 '¿Qué se debe ver del taller, del acceso doméstico y del espacio común cuando el edificio está cerrado?',
 'Comparar tres densidades de cierre con igual hueco y registrar por separado bastidor, barras, panel y carpintería.'),
('Capotas, toldos y telas colgadas añaden una capa exterior al hueco. Su extensión puede corresponder a una ventana, una serie de balcones o un comercio.',
 'B02 y B13 cubren una unidad; B08 organiza una banda; B15 y B16 extienden el textil sobre el frente comercial. B07 muestra apropiación mediante telas.',
 '¿Cómo puede el edificio admitir regulación individual y mantener una regla colectiva de colocación?',
 'Definir posiciones de despliegue, recogida y sustitución. Estudiar orientación y sombra con las medidas del proyecto.'),
('La actividad comercial se hace visible mediante vidrio, apertura, rótulo y contenido. El umbral regula la relación entre exposición, paso y acceso.',
 'Ranger y Barrabés concentran productos tras vidrio. B05 añade un pequeño apoyo exterior; Paprika reúne plantas junto al frente; Amantis mantiene accesos abiertos.',
 '¿Qué puede aportar la planta baja al Rastro: reparación, intercambio, exposición o almacenaje?',
 'Separar acceso a viviendas, entrada de objetos y zona de exposición. Dibujar el estado abierto y cerrado del mismo programa.'),
('El cableado superficial constituye una trama añadida: sigue líneas de planta, llega a cajas y cambia de dirección alrededor de huecos y esquinas.',
 'La línea horizontal sobre los comercios concentra recorridos. Caja, bajada y esquina son los puntos donde esa continuidad cambia.',
 '¿Dónde se registrarán y ampliarán las instalaciones cuando cambie un local o una unidad doméstica?',
 'Reservar recorridos accesibles y puntos de registro, separando las necesidades del frente comercial y de las viviendas.'),
('El grafiti se concentra en superficies accesibles: persianas, paneles y placas de planta baja. La geometría del soporte condiciona el aspecto de la inscripción.',
 'La lámina de cierre se convierte en un paño gráfico al bajar. En el zócalo, el trazo atraviesa piezas y juntas; en los detalles próximos aparece también el desgaste.',
 '¿Cómo puede una superficie admitir expresión, limpieza o sustitución sin intervenir en toda la fachada?',
 'Comparar una pieza reemplazable, un acabado ensayado para limpieza y un paño de uso gráfico acordado con sus usuarios.'),
('Fondo, borde y base se diferencian por tono, textura o junta. Esa distribución permite leer tanto una unidad de hueco como un orden de varias plantas.',
 'B03 y B15 destacan bandas claras sobre ladrillo. B10 rodea el hueco con un recercado blanco; B12 dibuja un despiece inciso; B09 diferencia el basamento.',
 '¿Qué componente debe expresar la unidad doméstica y cuál debe reconocer lo colectivo?',
 'Comparar el mismo alzado organizado por unidad, por banda horizontal y por pieza de mantenimiento.')]
for ch,txt in zip(CH,TEXT):
 for key,val in zip(('definition','conclusion','question','test'),txt):ch[key]=val

T=Transformer.from_crs(4326,25830,always_xy=True)
CX,CY=T.transform(-3.707172,40.407576)
geo=json.loads((ROOT/'CATALOGO_PATRONES_600M/DATOS/ambito_osm_recortado.geojson').read_text())
items=[];seen=set()
for f in geo['features']:
 pr=f['properties'];oid=pr.get('osm_id')
 if oid in seen:continue
 seen.add(oid);g=transform(T.transform,shape(f['geometry']));items.append((g,pr))
buildings=[(g,pr) for g,pr in items if pr.get('building') and g.geom_type in ('Polygon','MultiPolygon')]
axis=unary_union([g for g,pr in items if 'Ribera' in pr.get('name','') and pr.get('highway')]).intersection(box(CX-350,CY-80,CX+350,CY+400))
corridor=axis.buffer(100,cap_style=2)
core=[(g,pr) for g,pr in buildings if corridor.covers(g.representative_point())]
levels=Counter(str(pr.get('building:levels','Sin dato')) for g,pr in core)
shops=[(g.representative_point(),pr) for g,pr in items if (pr.get('shop') or pr.get('craft')) and corridor.covers(g.representative_point())]
selected=[(g,pr) for g,pr in shops if pr.get('shop') in ('antiques','furniture','second_hand','frame','collector') or pr.get('craft')]
study=sorted({v['source'] for ch in CH for v in ch['cases']})
group=defaultdict(list)
for sid in study:
 s=sources[sid];group[(round(s['lon'],5),round(s['lat'],5))].append(sid)
stations=[]
for i,(pos,ids) in enumerate(sorted(group.items(),key=lambda kv:kv[0][1]),1):
 stations.append(dict(n=i,ids=ids,xy=T.transform(*pos)))
def geomdraw(g,conv,fill=False):
 if g.is_empty:return
 if hasattr(g,'geoms'):
  for z in g.geoms:geomdraw(z,conv,fill)
 elif g.geom_type=='Polygon':
  path=C.beginPath()
  for ring in [g.exterior,*g.interiors]:
   pts=[conv(a,b) for a,b in ring.coords];path.moveTo(*pts[0])
   for q in pts[1:]:path.lineTo(*q)
   path.close()
  C.drawPath(path,fill=int(fill),stroke=1)
 elif g.geom_type in ('LineString','LinearRing'):
  pts=[conv(a,b) for a,b in g.coords]
  if len(pts)>1:
   path=C.beginPath();path.moveTo(*pts[0])
   for q in pts[1:]:path.lineTo(*q)
   C.drawPath(path)
def drawmap(x,y,w,h,ids=None,mode='stations',extent=(-280,-110,280,420),labels=True):
 xmin,ymin,xmax,ymax=extent;k=min(w/(xmax-xmin),h/(ymax-ymin));ox=x+(w-(xmax-xmin)*k)/2;oy=y+(h-(ymax-ymin)*k)/2
 conv=lambda a,b:(ox+(a-CX-xmin)*k,oy+(b-CY-ymin)*k)
 clip=box(CX+xmin,CY+ymin,CX+xmax,CY+ymax)
 C.saveState();path=C.beginPath();path.rect(x,y,w,h);C.clipPath(path,stroke=0)
 C.setLineWidth(.23);C.setStrokeColorRGB(.67,.67,.67)
 for g,pr in buildings:
  if not g.intersects(clip):continue
  C.setFillColorRGB(.9,.9,.9)
  if mode=='levels' and corridor.covers(g.representative_point()):
   lv=str(pr.get('building:levels',''))
   grey={'1':.9,'2':.9,'3':.78,'4':.6,'5':.44,'6':.3}.get(lv,.15 if lv.isdigit() else .95)
   C.setFillColorRGB(grey,grey,grey)
  geomdraw(g.intersection(clip),conv,fill=(mode=='levels'))
 C.setStrokeColor(colors.black);C.setLineWidth(1.2);geomdraw(axis,conv)
 if mode in ('levels','shops'):
  C.setDash(2,2);C.setLineWidth(.6);geomdraw(corridor.boundary.intersection(clip),conv);C.setDash()
 if mode=='shops':
  for pt,pr in shops:
   xx,yy=conv(pt.x,pt.y);chosen=(pr.get('shop') in ('antiques','furniture','second_hand','frame','collector') or pr.get('craft'))
   C.setFillColor(colors.black if chosen else colors.white);C.setStrokeColor(colors.black);C.circle(xx,yy,2.2,fill=1,stroke=1)
 if mode=='stations':
  for st in stations:
   if ids is not None and not set(ids)&set(st['ids']):continue
   xx,yy=conv(*st['xy']);C.setFillColor(colors.white);C.setStrokeColor(colors.black);C.circle(xx,yy,2.4,fill=1,stroke=1)
   if labels:
    side=1 if st['n']%2 else -1
    lx=xx+8 if side==1 else xx-12
    C.setLineWidth(.4);C.line(xx+side*3,yy,xx+side*7,yy+2)
    C.setFillColor(colors.white);C.rect(lx-1,yy,6,8,fill=1,stroke=0)
    C.setFillColor(colors.black);C.setFont('Helvetica',7);C.drawString(lx,yy+1,str(st['n']))
 xx,yy=conv(CX,CY);C.setStrokeColor(colors.black);C.setLineWidth(1);C.line(xx-3,yy,xx+3,yy);C.line(xx,yy-3,xx,yy+3)
 C.restoreState();C.setFillColor(colors.black);C.setStrokeColor(colors.black)
 C.setFont('Helvetica',7);C.drawString(x+w-13,y+h-9,'N');C.line(x+w-11,y+h-27,x+w-11,y+h-12)
 C.line(x+w-11,y+h-12,x+w-14,y+h-18);C.line(x+w-11,y+h-12,x+w-8,y+h-18)
 C.setLineWidth(1);C.line(x+5,y+9,x+5+100*k,y+9);C.line(x+5,y+6,x+5,y+12);C.line(x+5+100*k,y+6,x+5+100*k,y+12)
 C.setFont('Helvetica',7);C.drawString(x+5,y+16,'100 m')
 return k
def locator(ch):
 ids=sorted({v['source'] for v in ch['cases']});drawmap(42,62,190,164,ids)
 y=p('Localización de los casos',253,223,300,11,bold=True)-7
 for st in stations:
  found=set(st['ids'])&set(ids)
  if not found:continue
  bids=sorted({v['front'] for v in ch['cases'] if v['source'] in found})
  y=p(f"{st['n']}. {', '.join(sorted(found))} / {', '.join(bids)}",253,y,300,8.5,10.2)-2
 p('Puntos: cámara de observación. Cruz: Ribera 31, referencia de emplazamiento. Base OSM; ETRS89 / UTM 30N.',253,y-4,300,8,9.5)

# Textures are assigned to the analytical family they help explain.
ASSIGN={'01':[25],'02':[1,9,11,17,18,22,29,32],'03':[6,13,14,19,20,28],'04':[],
        '05':[4,8,10,26,30],'06':[15],'07':[24,31],'08':[2,3,5,7,12,16,21,23,27,33]}
assert sorted(sum(ASSIGN.values(),[]))==list(range(1,34))
MEANINGS=[
 'El pulsador concentra contacto y uso en una pieza pequeña. El despiece debe permitir cuidar esa pieza y su encuentro con el soporte.',
 'La retícula del soporte permanece mientras las inscripciones y la pintura transforman la superficie visible.',
 'La altura del frente, el tamaño de hueco y el basamento construyen una relación próxima con la calle.',
 'La señal perpendicular orienta al peatón. Su soporte puede coordinarse con rótulos y accesos sin invadir el hueco doméstico.',
 'La celosía superior y el paño inferior operan a escalas distintas: repetición de perforaciones y variación de superficie.',
 'La transparencia depende de barra, separación y fondo. La base pétrea fija el plano donde empieza el filtro.',
 'La retícula del suelo admite bandas y marcas que ordenan posiciones. La cifra se registra como elemento visible.',
 'Toldo, macetas y objetos construyen un espesor de uso entre el local y la circulación.',
 'El cambio de cota introduce una secuencia de bordes. La continuidad material puede leerse a través de peldaños diferentes.',
 'El machón separa dos huecos del comercio; el portal contiguo mantiene una identidad de acceso propia.',
 'La pieza grande y el módulo pequeño se encuentran en una banda. El marcador introduce un punto singular dentro de ese orden.',
 'El módulo pequeño del revestimiento contrasta con el marco de carpintería. La jerarquía permite leer el frente a dos distancias.',
 'Barras y panel inferior producen distintos grados de transparencia según la altura del cierre.',
 'El relieve aumenta la complejidad de contacto y limpieza; la capa de pintura registra el uso de sus salientes.',
 'El cableado dibuja una segunda línea sobre arcos y recercados. La instalación negocia con una geometría preexistente.',
 'La vista general conecta el detalle de planta baja con la secuencia de huecos y balcones superiores.',
 'Pila, relieve y encuentro inferior reúnen agua, residuo y contacto. Su configuración organiza el acceso de limpieza.',
 'La proximidad revela grano y junta. Es una referencia para comparar tacto, formato de pieza y precisión del encuentro.',
 'Barras, círculos y rombos forman un módulo; las puntas y el basamento resuelven los extremos de la serie.',
 'La junta cambia de dirección alrededor del hueco circular y la cerrajería añade una segunda geometría.',
 'El recercado pintado hace visible el borde sin modificar el tamaño del hueco. El cierre ofrece otro plano de lectura.',
 'La fuente y la escalera relacionan objeto urbano, desnivel y acceso al edificio en una misma franja de calle.',
 'La medianera ofrece una superficie de gran escala. El grafismo se confronta con la escala próxima del árbol y del basamento.',
 'El pie del cierre concentra cambios de material y pérdidas de acabado. La reposición puede pensarse por componentes.',
 'La esquina prolonga un mismo orden de balcones y bandas hacia dos calles, manteniendo continuidad en el giro.',
 'La carpintería delimita paños de comunicación y exposición. La instalación de obra constituye un estado temporal diferenciado.',
 'La diagonal cambia la lectura del plano exterior frente al vidrio. Su geometría aporta un contraste entre dirección y retícula.',
 'Hoja, bastidor y franja inferior permiten comparar transparencia, escala de acceso y composición del portal.',
 'La vista general relaciona los detalles de contacto con el cuenco, la base y el entorno de escalones.',
 'La densidad del contenido vuelve reconocible el escaparate. El plano de vidrio permite mostrar sin ocupar la acera.',
 'Cuando el cierre baja, la persiana ofrece una superficie gráfica continua bajo la franja del toldo.',
 'Piedra, ladrillo y carpintería se encuentran en el acceso. La posición de cada material distingue borde, campo y arranque.',
 'El módulo pequeño permite leer el pavimento como suma de unidades: cada cambio de tono queda incorporado a la retícula.'
]
LOC={1:'Conjunto fuente F01/F17/F29.',2:'Mercado de la Cebada. Mismo frente que F05.',3:'Frente bajo de Ribera. Serie F03/F15/F21.',5:'Mercado de la Cebada. Mismo frente que F02.',10:'Ribera 10. Frente B07 / RC06.',11:'Mismo punto de detalle que F18.',12:'Farmacia Fuentecilla, Toledo 105. Serie F12/F16.',15:'Frente bajo de Ribera. Serie F03/F15/F21.',16:'Farmacia Fuentecilla, Toledo 105. Serie F12/F16.',17:'Conjunto fuente F01/F17/F29.',18:'Mismo punto de detalle que F11.',21:'Frente bajo de Ribera. Serie F03/F15/F21.',22:'Entorno de Ribera 2 / RC10.',23:'Extremo norte del recorrido / RC11.',29:'Conjunto fuente F01/F17/F29, próximo a Ribera 2.',30:'Ribera 6 / RC08, tramo de Ranger.',32:'Mensajeros de la Paz, Ribera 2.'}
def texture_pages(ch):
 nums=ASSIGN[ch['code']]
 for a in range(0,len(nums),2):
  top=page(f"{ch['code']} / texturas encontradas",ch['title'])
  for j,num in enumerate(nums[a:a+2]):
   d=fields[num-1];title,obs,_,_=FNOTES[num-1];yy=top-j*316
   if num==3:obs='Frente amarillo de poca altura, vanos pequeños, reja y basamento oscuro.'
   p(f"{d['id']} / {title}",42,yy,511,12.5,bold=True)
   img(d['path'],42,yy-279,202,254)
   y=p('Observación',260,yy-28,292,11,bold=True)-5
   y=p(obs,260,y,292,11)-12
   y=p('Relación material',260,y,292,11,bold=True)-5
   y=p(MEANINGS[num-1],260,y,292,11)-12
   p(LOC.get(num,'Registro de campo. Localización exacta sin georreferencia.'),260,y,292,9.3)

def flowline(a,b):
 C.setLineWidth(.7);C.line(*a,*b);ang=math.atan2(b[1]-a[1],b[0]-a[0])
 for off in (-.5,.5):C.line(*b,b[0]-5*math.cos(ang+off),b[1]-5*math.sin(ang+off))
def poly(pts,fill=False):
 q=C.beginPath();q.moveTo(*pts[0])
 for pt in pts[1:]:q.lineTo(*pt)
 q.close();C.drawPath(q,fill=int(fill),stroke=1)

def urban_plate():
 y=page('A1 / tejido y escala','La repetición doméstica dentro del tejido')
 n=len(core);known=sum(v for k,v in levels.items() if k!='Sin dato');mid=sum(levels.get(str(i),0) for i in (4,5,6))
 y=p(f'La franja de 100 m alrededor del eje seleccionado reúne {n} polígonos de edificio. {known} tienen un número de plantas registrado; {mid} de esos registros indican entre cuatro y seis plantas.',42,y,511,12)-10
 drawmap(42,312,285,323,mode='levels')
 p('Plantas registradas',353,625,200,12,bold=True)
 vals=[(str(i),levels.get(str(i),0)) for i in range(1,11) if levels.get(str(i),0)]
 yy=594;mx=max(v for k,v in vals)
 for k,v in vals:
  p(k,353,yy,25,9);C.setFillColor(colors.black);C.rect(378,yy-9,v/mx*135,7,fill=1,stroke=0);p(str(v),519,yy,30,9);yy-=23
 p(f'{levels.get("Sin dato",0)} polígonos sin número de plantas registrado.',353,yy-15,195,10)
 p('Mapa: gris más oscuro = mayor número de plantas; blanco grisáceo = sin dato. Contorno discontinuo = franja de 100 m. Eje negro = Ribera.',42,295,511,9.5)
 y=p('La regla común y la diferencia de altura',42,247,511,14,bold=True)-8
 y=p('La fachada doméstica pertenece a un tejido donde conviven varios rangos de altura. La repetición de huecos puede dar continuidad al frente mientras un acceso colectivo, una esquina o una planta común introducen una variación reconocible.',42,y,511,11)-16
 p('Método: punto interior del polígono dentro de la franja; building:levels de la base OSM archivada. La variable cuenta plantas etiquetadas. Las alturas en metros requieren un levantamiento específico.',42,y,511,9.5)

def matrix_plate():
 y=page('A2 / coincidencias entre familias','La identidad aparece en la combinación')
 p('Cada fila representa un frente y cada columna una familia. El punto marca la evidencia incluida en las fichas; la celda vacía corresponde a una relación sin codificar en esta selección.',42,y,511,11)
 bids=sorted({v['front'] for ch in CH for v in ch['cases']});top=620;dx=42;start=193
 short=['Hueco','Base','Reja','Textil','Local','Cable','Huella','Acabado']
 for j,t in enumerate(short):p(f'{j+1:02d}',start+j*dx-8,top+29,35,10,bold=True)
 for i,b in enumerate(bids):
  yy=top-i*19;p(b,54,yy+4,50,10)
  p(fronts[b][0],102,yy+4,65,9)
  C.setStrokeColorRGB(.83,.83,.83);C.setLineWidth(.3);C.line(171,yy-8,538,yy-8)
  for j,ch in enumerate(CH):
   if any(v['front']==b for v in ch['cases']):C.setFillColor(colors.black);C.circle(start+j*dx,yy,3,fill=1,stroke=0)
 C.setStrokeColor(colors.black)
 y=top-len(bids)*19-20
 for j,t in enumerate(short):
  p(f'{j+1:02d} {t}',54+(j%4)*130,y-(j//4)*20,128,10)
 y-=62
 sets=[{v['front'] for v in ch['cases']} for ch in CH]
 x=len(sets[0]&sets[1]);z=len(sets[4]&sets[6])
 y=p(f'Cruces observados: {x} frentes comparten las fichas de hueco y base; {z} comparten comercio y huella. La comparación permite elegir conjuntos de relaciones para estudiar, manteniendo la identidad de cada caso.',42,y,511,11)-15
 p('Pregunta: ¿qué capas debe resolver una misma decisión? Un zócalo de uso colectivo puede coordinar acceso, exposición, mantenimiento e instalaciones en vez de tratar cada elemento por separado.',42,y,511,11)

def exploded_plate():
 y=page('A3 / despiece de relaciones','Una fachada, varias capas de uso')
 p('El plano del hueco, el bastidor, la barandilla y la tela pueden leerse por separado. El despiece permite asignar a cada capa una función y un ámbito de cuidado.',42,y,511,11)
 # Four transparent analytical planes, separated horizontally; no hidden construction.
 C.setStrokeColor(colors.black);C.setLineWidth(.9)
 for i in range(4):
  ox=62+i*125;oy=394+i*13
  tr=lambda u,v:(ox+u+.23*v,oy+v)
  if i==0:
   poly([tr(0,0),tr(72,0),tr(72,167),tr(0,167)])
   poly([tr(18,18),tr(54,18),tr(54,142),tr(18,142)])
  elif i==1:
   poly([tr(18,18),tr(54,18),tr(54,142),tr(18,142)])
   for yy in (21,80,139):C.line(*tr(20,yy),*tr(52,yy))
   C.line(*tr(36,18),*tr(36,142))
  elif i==2:
   poly([tr(8,17),tr(64,17),tr(64,67),tr(8,67)])
   for xx in range(14,65,7):C.line(*tr(xx,17),*tr(xx,67))
   C.line(*tr(8,23),*tr(64,23))
  else:
   q=C.beginPath();q.moveTo(*tr(10,142));q.lineTo(*tr(62,142));q.curveTo(*tr(55,98),*tr(70,77),*tr(48,63));q.curveTo(*tr(25,65),*tr(14,92),*tr(10,142));C.drawPath(q)
   C.line(*tr(9,144),*tr(64,144))
  p(['01 Campo y hueco','02 Carpintería','03 Barandilla','04 Tela'][i],ox-3,oy-15,121,10,bold=True)
  if i<3:
   C.setDash(2,3);C.line(*tr(72,165),ox+125+.23*165,oy+13+165);C.setDash()
 p('Axonometría analítica sin escala. Separación gráfica entre planos visibles; referencia B07 / RC06. El dibujo identifica capas y conserva su relación con el hueco.',42,341,511,9.5)
 img(sources['RC06']['photo'],42,112,218,182,(.626,.199,.816,.50))
 y=p('Qué se fija y qué se regula',290,292,263,13,bold=True)-7
 y=p('El hueco establece una posición estable. Carpintería y barandilla configuran el límite; la tela introduce una condición ajustable. La coordinación entre capas permite prever sustitución y apropiación.',290,y,263,11)-12
 p('Pregunta: ¿qué puede gestionar una persona y qué debe conservar una regla común para todo el edificio?',290,y,263,11)

def shops_plate():
 y=page('A4 / actividad próxima','Objetos, oficios y planta baja')
 counts=Counter('oficio' if pr.get('craft') else pr.get('shop') for pt,pr in selected)
 p(f'En la franja de estudio figuran {len(shops)} registros OSM de comercio u oficio. {len(selected)} corresponden al grupo de antigüedades, muebles, segunda mano, enmarcación, coleccionismo y oficios.',42,y,511,12)
 drawmap(42,294,299,335,mode='shops')
 yy=617
 names={'antiques':'Antigüedades','furniture':'Muebles','second_hand':'Segunda mano','frame':'Enmarcación','collector':'Coleccionismo','oficio':'Oficios'}
 for k,v in sorted(counts.items(),key=lambda x:-x[1]):
  yy=p(f'{v}  {names.get(k,k)}',362,yy,190,11,bold=True)-9
 p('Punto negro: grupo de objetos y oficios. Círculo blanco: otros comercios. Línea discontinua: franja de 100 m.',355,yy-10,197,9.5)
 y=p('Una cadena de actividades',42,268,511,14,bold=True)-7
 labels=['RECIBIR','REPARAR','MOSTRAR','GUARDAR']
 for i,t in enumerate(labels):
  x=42+i*132;p(t,x,211,118,10,bold=True)
  if i<3:flowline((x+81,191),(x+120,191))
 p('Ensayo de programa: entrada de objetos, superficie de trabajo, exposición y reserva. La cadena plantea una relación posible con las actividades próximas; su dimensionado se desarrolla con comerciantes y residentes.',42,167,511,11)
 p('Fuente: etiquetas shop y craft en la base OSM archivada; un registro es una entidad cartográfica. Fecha del archivo: 21-22/09/2026.',42,89,511,9)

def care_plate():
 y=page('A5 / componente, acceso y cuidado','La repetición también organiza el mantenimiento')
 p('Un componente repetido necesita una forma clara de acceso y sustitución. La matriz relaciona cinco capas observadas con la operación que el proyecto debe resolver.',42,y,511,11)
 rows=[('Zócalo por piezas','Contacto y limpieza','Retirar una pieza','Junta y arranque'),('Carpintería / reja','Uso y conservación','Acceder al bastidor','Encuentro con hueco'),('Toldo / tela','Regular y recoger','Cambiar la capa','Borde de sujeción'),('Cable / registro','Ampliar y revisar','Acceder al trazado','Cruce y derivación'),('Cierre gráfico','Limpiar o renovar','Sustituir un paño','Límite de la pieza')]
 widths=[128,122,123,138];xs=[42,170,292,415]
 for x,w,t in zip(xs,widths,['COMPONENTE','ACCIÓN','ACCESO','DETALLE CLAVE']):p(t,x,615,w-10,9,bold=True)
 for i,row in enumerate(rows):
  yy=580-i*58
  C.setStrokeColorRGB(.75,.75,.75);C.setLineWidth(.4);C.line(42,yy+9,553,yy+9)
  for x,w,t in zip(xs,widths,row):p(t,x,yy,w-12,10.5)
 C.setStrokeColor(colors.black)
 # Enlarged analytical panel: a removable unit and its surrounding fixed grid.
 x,y=76,135
 for r in range(3):
  for j in range(4):
   if (r,j)!=(1,2):rect(x+j*38,y+r*35,34,31)
 C.setDash(2,2);rect(x+76,y+35,34,31);C.setDash()
 rect(x+197,y+57,34,31);flowline((x+112,y+52),(x+188,y+69))
 p('Unidad dentro de una serie',54,113,208,10)
 p('Acceso a la pieza',279,194,225,12,bold=True)
 p('Esquema de sustitución por unidad. El detalle a desarrollar es la junta y la fijación accesible; tamaño y anclaje corresponden al proyecto.',279,175,257,10.5)
 p('Cruce con familias 02, 03, 04, 06 y 07. La matriz expresa criterios de diseño, sin asignar intervalos de mantenimiento no medidos.',42,71,511,9)

y=page('Patrones y materia / septiembre 2026','Ribera de Curtidores')
y=p('Orden doméstico, capas de uso y contacto con la calle',42,y,511,16)-10
drawmap(58,258,478,371,study,extent=(-410,-160,410,480))
p('Un recorrido por fachadas, comercios y encuentros materiales',42,231,511,14,bold=True)
p('Ocho familias reúnen 64 observaciones sobre 18 frentes. Las fotografías, los dibujos y la cartografía sitúan las relaciones que pueden informar un edificio de vivienda colectiva y espacios comunes en el Rastro.',42,201,511,12)
p('Lectura del mapa: puntos numerados = estaciones de cámara; cruz = referencia de Ribera 31. Base OSM en ETRS89 / UTM 30N. Escala gráfica válida en el documento A4.',42,111,511,9.5)

y=page('Sistema de lectura','De la calle a la decisión material')
p('El estudio relaciona tres escalas: el tejido urbano, la composición del frente y el contacto con cada pieza. La pregunta de proyecto aparece al cruzarlas.',42,y,511,12)
for row,(title,items2) in enumerate([('TEJIDO',['Eje y proximidad','Alturas registradas','Actividades próximas']),('FRENTE',['Hueco y balcón','Base y acabado','Instalación y textil']),('PIEZA',['Bastidor y junta','Contacto y huella','Acceso y sustitución'])]):
 yy=598-row*131;p(title,42,yy,130,11,bold=True)
 for j,t in enumerate(items2):p(t,42+j*175,yy-35,158,12)
 if row<2:
  for j in range(3):flowline((99+j*175,yy-61),(99+j*175,yy-98))
y=p('Registro y escala',42,172,511,13,bold=True)-6
p('B identifica un frente; RC y SV, una posición de cámara; F, un registro de campo. Los mapas tienen norte y escala métrica. Los alzados, axonometrías y despieces son esquemas analíticos sin escala. Cada captura conserva su fecha; el detalle de calle describe superficies y relaciones visibles.',42,y,511,11)

y=page('Contenido','Ocho familias y cinco cruces analíticos')
for ch in CH:
 y=p(f"{ch['code']}   {ch['title']}",42,y,511,13,bold=True)-11
y-=12
for t in ['A1 · Tejido y alturas registradas','A2 · Coincidencias entre familias','A3 · Axonometría de capas','A4 · Comercios y cadena de actividades','A5 · Componentes y mantenimiento']:
 y=p(t,42,y,511,11)-8
p('Las texturas encontradas se integran en la familia a la que aportan una observación material. Fuentes, posiciones y correspondencias de archivo se reúnen al final.',42,y-15,511,11)
urban_plate()

EXTRA={'01':matrix_plate,'04':exploded_plate,'05':shops_plate,'07':care_plate}
for ch in CH:
 for half in range(2):
  top=page(f"{ch['code']} / casos {half*4+1}-{half*4+4}",ch['title'])
  p('Ocho frentes por familia. La llamada 1 señala el componente descrito.',42,top,511,10)
  for j,v in enumerate(ch['cases'][half*4:half*4+4]):casecard(ch,v,half*4+j+1,42+(j%2)*267,top-30-(j//2)*303)
 y=page(f"{ch['code']} / despiece, comparación y lugar",ch['title'])
 y=p(ch['definition'],42,y,511,10.8)-13
 a,b,txt=DIAG[ch['diagram']]
 label('D1. '+a,48,y,232);label('D2. '+b,314,y,235)
 sketch(ch['diagram'],62,y-170,0);sketch(ch['diagram'],327,y-170,1)
 y-=184
 y=p(ch['conclusion'],42,y,511,10.5)-9
 y=p('<b>Pregunta.</b> '+ch['question'],42,y,511,10.5)-8
 y=p('<b>Ensayo.</b> '+ch['test'],42,y,511,10.5)
 if y<246:raise ValueError(('Diagram page overflow',ch['code'],y))
 p('Alzados analíticos sin escala. D1 y D2 aíslan la relación visible indicada por los casos.',42,245,511,8)
 locator(ch)
 if ch['code'] in EXTRA:EXTRA[ch['code']]()
 texture_pages(ch)

y=page('Tiempo y uso','El frente durante la actividad y el cierre')
p('La apertura transforma qué capa se ofrece a la calle: vidrio, interior, objetos o cierre gráfico. La estructura del hueco y los elementos fijos del suelo mantienen la posición del uso.',42,y,511,12)
for i,(sid,crop,head) in enumerate([('RC05',(.31,.51,.45,.76),'ACCESO Y EXPOSICIÓN'),('RC01',(.264,.503,.327,.679),'CIERRE Y SUPERFICIE')]):
 x=42+i*267;img(sources[sid]['photo'],x,391,244,220,crop);p(head,x,371,244,11,bold=True)
p('Dos situaciones observadas en locales diferentes: un comercio abierto en RC05 y un cierre gráfico en RC01.',42,335,511,9.5)
y=p('Actividad vinculada al Rastro',42,298,511,14,bold=True)-8
y=p('La información municipal distingue el mercadillo de la actividad de las tiendas. El edificio puede estudiar una planta común capaz de recibir, mostrar, trabajar y guardar objetos, con acceso doméstico independiente.',42,y,511,11)-16
y=p('Pregunta: ¿qué parte queda disponible fuera de la actividad comercial y quién la gestiona? El ensayo consiste en dibujar dos estados del mismo programa, manteniendo paso, acceso y almacenamiento.',42,y,511,11)-15
p('Las imágenes documentan estados puntuales de 2021 y 2022. El dimensionado temporal requiere observación repetida desde la misma posición y acuerdos de uso.',42,y,511,9.5)

y=page('Síntesis','Cinco decisiones para desarrollar el edificio')
for title,txt in [
 ('Una regla común y capas ajustables','Coordinar huecos y accesos con una regla legible. Permitir que textil, rótulo y exposición cambien en posiciones previstas.'),
 ('Un basamento con capacidad de uso','Relacionar contacto, apoyo de objetos y limpieza. Diseñar la pieza que llega al suelo y su encuentro con el portal.'),
 ('Un borde doméstico elegido','Comparar el balcón individual y la banda compartida atendiendo a privacidad, estancia, sombra y gestión.'),
 ('Una planta baja conectada a las actividades próximas','Ensayar recepción, reparación, exposición y reserva como una secuencia; separar esa actividad del acceso cotidiano a viviendas.'),
 ('Un sistema que se pueda cuidar','Resolver juntas, recorridos de instalaciones y sustitución de cierres desde el inicio. La repetición facilita reconocer y mantener componentes.')]:
 y=p(title,42,y,511,14,bold=True)-7;y=p(txt,42,y,511,12)-24
p('Estas decisiones sitúan el anteproyecto entre forma, uso y mantenimiento. Su desarrollo espacial se contrasta con el programa de 20 unidades, 40 habitantes y espacios comunes del enunciado G3.',42,y,511,11)

used=sorted({v['source'] for ch in CH for v in ch['cases']}|{'RC10','RC11'})
for start in range(0,len(used),4):
 top=page('Fuentes visuales','Capturas y posiciones de observación')
 for j,sid in enumerate(used[start:start+4]):
  x=42+(j%2)*267;yy=top-(j//2)*303;s=sources[sid]
  p(f"{sid} / {s['date']}",x,yy,243,12,bold=True);img(s['photo'],x,yy-162,243,144)
  ty=p(f"Cámara: {s['lat']:.7f}, {s['lon']:.7f}",x,yy-175,243,9)
  ty=p(f"© {s['author']}. Coordenada de la posición de observación.",x,ty-5,243,9)
  p(f'<link href="{escape(s["url"],{chr(34):"&quot;"})}">Abrir panorama de referencia</link>',x,ty-8,243,10)

y=page('Registro físico','Frentes del recorrido')
for b in sorted({v['front'] for ch in CH for v in ch['cases']}):
 sid,desc=fronts[b];y=p(f'<b>{b} / {sid}</b>  {escape(desc)}',42,y,511,10.5)-10
p('Los nombres comerciales identifican el frente en la fecha de su fotografía. Las texturas F01-F33 conservan su vínculo con el archivo original en el inventario de esta edición.',42,y-6,511,10)

y=page('Fuentes y método','Base documental y gráfica')
for head,txt in [
 ('Cartografía','Instantánea OSM archivada en la investigación el 21-22/09/2026. Geometrías proyectadas en ETRS89 / UTM 30N. La franja analítica se construye a 100 m del eje representado. Los edificios se incluyen por punto interior y los comercios por su posición cartográfica.'),
 ('Observación de calle','Capturas Google Street View de julio de 2021 y marzo de 2022, con fecha por caso; serie de campo F01-F33. Los registros de campo sin GPS se describen por su contenido y por las correspondencias visuales identificadas.'),
 ('Representación','Fotografías con llamadas sobre componentes visibles; alzados y despieces sin escala; mapas con escala gráfica. El número de plantas procede de la etiqueta building:levels. Estructura, anclajes y dimensiones constructivas se desarrollan mediante documentación técnica y levantamiento.'),
 ('Referencias analíticas','Oviedo: mapas multiescala, axonometría, cruce entre variables y datos localizados; documentos y láminas de las carpetas oviedo, oviedo 1, 2, 3 y 4. Refugio Climático: mapas de estado, relaciones entre sistemas y matriz componente-acceso-mantenimiento; compendio analítico y síntesis técnicas. La edición aplica esos tipos de análisis a Ribera con dibujos propios.'),
 ('Programa','G3 ESP - LA MATERIA DE LO DOMÉSTICO v3.0: vivienda colectiva temporal, 20 unidades, 40 habitantes y espacios comunes. Las relaciones de actividad que se ensayan aquí son hipótesis de proyecto.')]:
 y=p(head,42,y,511,12,bold=True)-5;y=p(txt,42,y,511,10.5)-13
url='https://www.madrid.es/portales/munimadrid/es/Inicio/El-Ayuntamiento/Publicaciones/Mercadillo-en-la-via-publica-El-Rastro/?vgnextchannel=e968e3d5d3e07010VgnVCM100000dc0ca8c0RCRD&vgnextfmt=default&vgnextoid=781192355c51c010VgnVCM2000000c205a0aRCRD'
y=p(f'<link href="{escape(url,{chr(34):"&quot;"})}">Ayuntamiento de Madrid: mercadillo El Rastro</link>',42,y,511,10)-14
p('Edición: septiembre de 2026. Archivo reproducible: datos de observaciones, referencias, fórmulas cartográficas y generador vectorial conservados junto al documento.',42,y,511,9.5)
C.save()
shutil.copy2(PDF,OUT/PDF.name)
(BASE/'indice_paginas.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2))
(BASE/'datos_analiticos.json').write_text(json.dumps({'core_buildings':len(core),'levels':dict(levels),'commerce_records':len(shops),'objects_and_crafts':len(selected),'commerce_groups':dict(Counter('oficio' if pr.get('craft') else pr.get('shop') for pt,pr in selected)),'stations':stations,'texture_assignment':ASSIGN},ensure_ascii=False,indent=2))
(BASE/'casos_y_flechas.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
for ch in CH:
 folder=BASE/(ch['code']+'_'+re.sub(r'[^A-Z0-9]+','_',ch['title'].upper()).strip('_'));folder.mkdir(exist_ok=True)
 (folder/'casos.json').write_text(json.dumps(ch,ensure_ascii=False,indent=2))
 (folder/'texturas.json').write_text(json.dumps([dict(**fields[n-1],analisis=MEANINGS[n-1]) for n in ASSIGN[ch['code']]],ensure_ascii=False,indent=2))
print(json.dumps({'pdf':str(PDF),'pages':PAGE,'families':8,'case_observations':len(manifest),'field_photos':sum(map(len,ASSIGN.values())),'analytical_plates':5,'metric_family_maps':8},ensure_ascii=False))
