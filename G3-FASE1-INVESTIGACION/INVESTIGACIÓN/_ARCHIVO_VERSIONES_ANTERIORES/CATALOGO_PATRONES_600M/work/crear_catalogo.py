from pathlib import Path
import json,re,math,io,shutil,collections
from xml.sax.saxutils import escape
from PIL import Image,ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader
from shapely.geometry import shape,Point,mapping
from shapely.ops import transform
from pyproj import Transformer
from catalogo_datos import PATTERNS,SOURCES
from dibujos import make,TITLES

BASE=Path(__file__).resolve().parents[2];OUT=BASE/'CATALOGO_PATRONES_600M'
WORK=OUT/'work';DATA=OUT/'DATOS'; QA=WORK/'verificacion';QA.mkdir(exist_ok=True)
T=Transformer.from_crs(4326,25830,always_xy=True);TI=Transformer.from_crs(25830,4326,always_xy=True)
CX,CY=T.transform(-3.707172,40.407576)
old=json.loads((BASE/'PATRONES_STREET_VIEW/inventario_verificado.json').read_text())
obs={r['id']:dict(id=r['id'],title=r['title'],lat=r['lat'],lon=r['lon'],date=r['fecha_imagen'],author=r['author'],url=r['url'],photo=r['foto']) for r in old}
months={'Jan':'enero','Feb':'febrero','Mar':'marzo','Apr':'abril','May':'mayo','Jun':'junio','Jul':'julio','Aug':'agosto','Sep':'septiembre','Oct':'octubre','Nov':'noviembre','Dec':'diciembre'}
for r in json.loads((OUT/'CAPTURAS/registro.json').read_text()):
 ax=r['ax'];u=re.search(r'URL: "([^"]+)"',ax).group(1);lat,lon=map(float,re.search(r'@(-?[\d.]+),(-?[\d.]+)',u).groups())
 title=re.search(r'Title: "(.*?) - Google Maps"',ax).group(1)
 m=re.search(r'Image capture: ([A-Za-z]{3}) (\d{4})',ax)
 if not m:m=re.search(r'text ([A-Za-z]{3}) (\d{4})',ax)
 fallback_dates={'NR01':'enero 2022','NR15':'junio 2025'} # Fechas leídas en las capturas; el registro AX sólo conservó el cambio de estado.
 date=months[m[1]]+' '+m[2] if m else fallback_dates[r['id']]
 obs[r['id']]=dict(id=r['id'],title=title,lat=lat,lon=lon,date=date,author='Google Street View',url=u,photo=str(OUT/'CAPTURAS'/f"{r['id']}.png"))
for r in obs.values():
 x,y=T.transform(r['lon'],r['lat']);r['distance_m']=round(math.hypot(x-CX,y-CY));r['sector']=int(((math.degrees(math.atan2(x-CX,y-CY))+375)%360)//30)+1;r['ring']='0-300' if r['distance_m']<=300 else '300-600';r['xy']=(x-CX,y-CY)
 assert r['distance_m']<=600,r
 r['patterns']=[p['id'] for p in PATTERNS if r['id'] in p['evidence']]
unique_sites=len({(r['lat'],r['lon']) for r in obs.values()})
stats=json.loads((DATA/'estadisticas_ambito.json').read_text())
geo=json.loads((DATA/'ambito_osm_recortado.geojson').read_text())
buildings=[];roads=[]
for f in geo['features']:
 p=f['properties'];g=transform(T.transform,shape(f['geometry']))
 if 'building' in p and g.geom_type in ('Polygon','MultiPolygon'):buildings.append((g,p))
 elif p.get('highway') and g.geom_type=='LineString':roads.append((g,p))
sources={s[0]:s for s in SOURCES}
PAGES=[]; W,H=A4; L=40;CW=W-80
pdf=OUT/'CATALOGO_PATRONES_EL_RASTRO_600M.pdf'
c=canvas.Canvas(str(pdf),pagesize=A4,pageCompression=1)
c.setTitle('Catálogo analítico de patrones · El Rastro · radio 600 m')
c.setAuthor('Investigación G3 · elaboración y dibujos asistidos por Codex')
styles={k:ParagraphStyle(k,fontName=f,fontSize=s,leading=lead,textColor='black',spaceAfter=0) for k,f,s,lead in [('body','Times-Roman',10.2,13),('small','Times-Roman',8.1,10.4),('title','Times-Roman',21,24),('head','Times-Bold',12,15),('tiny','Helvetica',7,9)]}
def para(text,y,style='body',x=L,w=CW):
 p=Paragraph(text,styles[style]);_,h=p.wrap(w,1000);p.drawOn(c,x,H-y-h);return y+h
def start(title,section='CATÁLOGO ANALÍTICO · RADIO 600 M'):
 PAGES.append(title);c.setFillColorRGB(0,0,0);c.setFont('Helvetica',7.3);c.drawString(L,H-30,section)
 para(escape(title),49,'title')
def end():
 c.setFont('Times-Roman',7);c.drawString(L,23,'El Rastro y entorno · Consulta 21-22/09/2026 · Fotografías fechadas en cada ficha')
 c.drawRightString(W-L,23,str(len(PAGES)));c.showPage()
imagecache={}
def reader(r):
 k=r['id']
 if k not in imagecache:
  im=Image.open(r['photo']).convert('RGB');b=io.BytesIO();im.save(b,format='JPEG',quality=91,subsampling=0,optimize=True);imagecache[k]=(ImageReader(b),im.size)
 return imagecache[k]
def photo(id,y,x=L,w=CW,maxh=246,marks=()):
 r=obs[id];im,(iw,ih)=reader(r);h=min(maxh,w*ih/iw);ww=h*iw/ih;xx=x+(w-ww)/2
 c.drawImage(im,xx,H-y-h,width=ww,height=h)
 for u,v,n in marks:
  tx=xx+ww*u;ty=H-y-h*v;bx=min(xx+ww-10,max(xx+10,tx+21));by=min(H-y-10,max(H-y-h+12,ty+19))
  c.setStrokeColorRGB(1,1,1);c.setLineWidth(2.8);c.line(bx,by,tx,ty);c.setStrokeColorRGB(0,0,0);c.setLineWidth(.8);c.line(bx,by,tx,ty)
  c.setFillColorRGB(1,1,1);c.circle(bx,by,7,stroke=1,fill=1);c.setFillColorRGB(0,0,0);c.setFont('Helvetica-Bold',7.4);c.drawCentredString(bx,by-2.5,n)
 return y+h
def caption(id,y,case='',text='',width=CW,x=L):
 r=obs[id];s=f"<b>{case} {id}</b> · {escape(r['title'])} · {escape(r['date'])} · {escape(r['author'])}. <link href='{escape(r['url'])}'>Fuente</link>."
 y=para(s,y,'small',x,width)+3
 if text:y=para(escape(re.sub(r'^\d\. ','',text)),y,'small',x,width)
 return y
def plot_map(x,y,size=240,ids=None,route=False,sector=False,labels=False):
 # y is top in PDF coordinates. Geometry is explicitly metric and north-up.
 k=size/1300; xx=x+size/2;yy=H-y-size/2
 c.saveState();c.setLineWidth(.22);c.setStrokeColorRGB(.5,.5,.5)
 for g,p in buildings:
  for pg in ([g] if g.geom_type=='Polygon' else g.geoms):
   pts=[(xx+(a-CX)*k,yy+(b-CY)*k) for a,b in pg.exterior.coords]
   path=c.beginPath();path.moveTo(*pts[0])
   for pt in pts[1:]:path.lineTo(*pt)
   path.close();c.drawPath(path,stroke=1,fill=0)
 c.setStrokeColorRGB(0,0,0);c.setLineWidth(.7);c.circle(xx,yy,600*k)
 if sector:
  c.setDash(2,3)
  for deg in range(15,360,30):
   a=math.radians(deg);c.line(xx,yy,xx+600*k*math.sin(a),yy+600*k*math.cos(a))
  c.circle(xx,yy,300*k);c.setDash()
  for s in range(1,13):
   a=math.radians((s-1)*30);c.setFont('Helvetica-Bold',8);c.drawCentredString(xx+560*k*math.sin(a),yy+560*k*math.cos(a),str(s))
 chosen=[obs[i] for i in ids] if ids is not None else list(obs.values())
 if route:
  ordered=[obs[f'NR{i:02}'] for i in range(2,14)];c.setDash(2,3)
  for a,b in zip(ordered,ordered[1:]+ordered[:1]):c.line(xx+a['xy'][0]*k,yy+a['xy'][1]*k,xx+b['xy'][0]*k,yy+b['xy'][1]*k)
  c.setDash()
 for r in chosen:
  a,b=r['xy'];c.setFillColorRGB(0,0,0);c.circle(xx+a*k,yy+b*k,2.2 if size>200 else 1.5,stroke=0,fill=1)
  if labels:c.setFont('Helvetica',6);c.drawString(xx+a*k+3,yy+b*k+3,r['id'])
 c.setLineWidth(1);c.line(xx-4,yy,xx+4,yy);c.line(xx,yy-4,xx,yy+4)
 c.setFont('Helvetica',7);c.drawString(x+size-13,H-y-7,'N');c.line(x+size-10,H-y-29,x+size-10,H-y-12)
 c.line(x+10,H-y-size+10,x+10+200*k,H-y-size+10);c.drawString(x+10,H-y-size+15,'200 m')
 c.restoreState()

start('Patrones del Rastro y su entorno')
para('Catálogo comparativo, anotado y dibujado',91,'head')
para(f'25 fichas · 50 diagramas vectoriales · {len(obs)} capturas en el archivo · {unique_sites} posiciones de cámara',116)
plot_map(72,153,450,route=True,sector=True)
para('De lo extendido a lo localizado',621,'head')
para('Tejido y orden de fachada → acabados y piezas → capas de uso → tipos localizados y singularidades. El círculo se centra en el punto aproximado de Ribera de Curtidores 31 utilizado en el inventario anterior, no en toda la longitud de la calle.',646)
para('Cobertura territorial de 600 m, no censo visual exhaustivo de cada inmueble. No se afirma que un acabado, una estructura o un motivo sea exclusivo del barrio. Las fotografías abarcan 2016-2025 y no describen automáticamente el estado de 2026.',708)
end()
start('Cómo se ha hecho específico el catálogo')
y=101
for h,t in [
 ('1. Referencias editoriales','REFERENCIAS/IMG_1946.JPG aporta la lógica de inventario de ejemplares. IMG_1947.JPG aporta identificación de partes, letras y comparación entre vistas. Se adopta esa lógica, sin reproducir el contenido médico de las imágenes.'),
 ('2. Un patrón es una relación concreta','Cada ficha nombra la unidad repetida: eje de hueco, junta del zócalo, plano filtrante, marco de reja, banda de pavimento. Las fotografías contienen llamadas numéricas y los dibujos aíslan esa relación.'),
 ('3. Recurrencia y rareza no se mezclan','Se computan posiciones distintas con evidencia positiva, sin contar dos giros como dos casos. Es un mínimo observado, no porcentaje de fachadas. Los casos singulares se identifican como tales.'),
 ('4. Dos niveles de datos','La cartografía cubre el círculo completo según la instantánea local. La revisión visual combina 27 posiciones anteriores y 15 nuevas, con un anillo de doce sectores. Los interiores siguen siendo puntuales y no se inspeccionan patios privados.'),
 ('5. Dibujos analíticos, no levantamientos','Todos los diagramas son originales, vectoriales y esquemáticos. No fijan medidas, espesores, giros reales ni estructuras ocultas. P23 incluye únicamente dimensiones publicadas por el Ayuntamiento, identificadas como documentales.'),
 ('6. Correcciones al atlas anterior','Se elimina «Lectura de proyecto». «Ladrillo y modulación» se divide en ritmo de huecos (P03) y fábrica visible (P07). La placa de calle deja de justificar un supuesto patrón cerámico. Se conserva el atlas anterior sin sobrescribirlo.')]:
 y=para(h,y,'head')+5;y=para(t,y)+16
end()
start('Qué dicen los datos del círculo completo')
y=105
for n,title,body in [
 ('1,131 km²','Área de análisis','Círculo de 600 m en EPSG:25830. Centro aproximado: 40.407576, -3.707172. Cruza áreas del núcleo histórico y del borde de Arganzuela.'),
 ('1.332','Polígonos de edificio con punto interior','Hay 1.370 que intersectan el círculo. Se usa punto representativo para contar sin incluir dos veces geometrías recortadas. No equivalen a viviendas, portales ni fincas catastrales.'),
 ('1.215 / 1.332','Etiqueta building=apartments (91,2 %)','Indica el peso de la vivienda colectiva en el inventario. No acredita una única tipología de planta, fecha ni sistema estructural.'),
 ('381 / 1.332','Edificios con número de plantas (28,6 %)','De los 381 con dato, 251 declaran 4-6 plantas. Los otros 951 no permiten una conclusión de altura. Véase el gráfico de P02.'),
 ('7 / 1.332','Con etiqueta de material (0,5 %)','Seis brick y uno plaster; los demás no tienen dato. No es defendible afirmar que todo el ámbito es de ladrillo. No hay start_date en los 1.332 polígonos.')]:
 y=para(n+' · '+title,y,'head')+5;y=para(body,y)+17
y=para('Fuente y cautela',y,'head')+4
para('Cálculo reproducible sobre los CSV OSM existentes, deduplicado por tipo/ID y recortado geométricamente. La exportación local no conserva huecos interiores en estos polígonos: no se utiliza para contar patios ni para estimar superficie construida neta. No se descargó un censo catastral nuevo.',y)
end()
start('Recorrido: anillo exterior y núcleo interior')
plot_map(66,94,459,ids=[f'NR{i:02}' for i in range(2,14)],route=True,sector=True,labels=True)
y=para('Anillo de doce sectores, en sentido horario',571,'head')+6
y=para('Norte: Duque de Alba → Juanelo → Lavapiés → Provisiones. Sureste y sur: Miguel Servet → Martín de Vargas → Acacias → San Isidoro. Oeste y noroeste: Olmos → Gran Vía de San Francisco → Mediodía Grande → Humilladero/Cebada.',y)+12
y=para('Contraste interior',y,'head')+6
y=para('Se cruza el anillo con las calles del archivo anterior: Curtidores, Cascorro, Vara de Rey, Ruda, Mira el Río, Carnero, Carlos Arniches, Fray Ceferino, Embajadores, Casino, Cabestreros, Oso, Amparo, Sombrerete y Tribulete. Mira el Sol y Escuelas Pías completan tipos y detalles concretos.',y)+12
para('La línea discontinua expresa el orden de inspección de estaciones; no es un itinerario peatonal calculado. Un punto representa una cámara, no la posición exacta de cada objeto visible.',y,'small')
end()
start('Índice: del tejido a la pieza y la excepción')
y=103
for i,p in enumerate(PATTERNS):
 dest=f"pat_{p['id']}";y=para(f"<link href='#{dest}'><b>{p['id']}</b> · {escape(p['title'])}</link>",y,'body')+8
end()
start('Lo común en la muestra: evidencia, no prevalencia')
para('Número mínimo de posiciones distintas con evidencia positiva. La ausencia de una marca no significa ausencia del elemento: las vistas no tienen idéntica orientación, fecha ni visibilidad.',95)
y=144
rank=[]
for p in PATTERNS:
 n=len({(obs[i]['lat'],obs[i]['lon']) for i in p['evidence']});p['n_sites']=n
 secs=sorted({obs[i]['sector'] for i in p['evidence']});p['sectors']=secs
 rank.append((n,p))
for n,p in sorted(rank,key=lambda t:-t[0]):
 para(f"{p['id']} {escape(p['title'])}",y,'small',L,335)
 c.setFillColorRGB(0,0,0);c.rect(391,H-y-8,n*8,6,stroke=0,fill=1);c.setFont('Helvetica',8);c.drawString(395+n*8,H-y-9,str(n));y+=23
end()
for p in PATTERNS:
 folder=OUT/(p['id']+'_'+re.sub(r'[^A-Z0-9]+','_',p['title'].upper()).strip('_')[:55]);folder.mkdir(exist_ok=True)
 p['folder']=str(folder)
 start(p['title'],p['id']+' · '+p['family']);c.bookmarkPage('pat_'+p['id']);c.addOutlineEntry(p['id']+' '+p['title'],'pat_'+p['id'],0)
 para(escape(p['definition']),104,'body')
 for j,(id,marks) in enumerate(p['shots']):
  y=159+j*319;photo(id,y,marks=marks);cap=caption(id,y+250,'A' if j==0 else 'B',p['parts'][j]);assert cap<811,(p['id'],cap)
  target=folder/f'{id}.png'
  if not target.exists():shutil.copy2(obs[id]['photo'],target)
 end()
 start(p['id']+' · Despiece y comparación',p['family'])
 for j,kind in enumerate(p['diagrams']):
  y=99+j*255;para(f"D{j+1}. {escape(TITLES[kind])}",y,'head')
  drawing=make(kind);drawing.draw(c,L,H-y-23)
  (folder/f"{p['id']}_D{j+1}.svg").write_text(drawing.svg(),encoding='utf-8')
 # Specific comparison and limits sit beside a map of only positive observations.
 plot_map(L,624,137,ids=p['evidence'])
 x=193;ww=W-L-x;y=618
 y=para(f"<b>{p['n_sites']} posiciones documentadas</b> · Sectores {', '.join(map(str,p['sectors']))}. Coordenadas de cámara.",y,'small',x,ww)+7
 y=para('<b>Variante / qué comparar.</b> '+escape(p['variation']),y,'small',x,ww)+7
 y=para('<b>Límite.</b> '+escape(p['limit']),y,'small',x,ww)+7
 y=para('Evidencia: '+', '.join(p['evidence'])+('. Fuentes: '+', '.join(p['sources']) if p['sources'] else '')+'.',y,'tiny',x,ww)
 assert y<805,(p['id'],y)
 para('Diagramas sin escala. No son propuestas de edificio ni detalles de ejecución.',787,'tiny')
 (folder/'FICHA.md').write_text('# '+p['id']+' · '+p['title']+'\n\n'+p['definition']+'\n\n'+'\n\n'.join(p['parts'])+'\n\n## Comparación\n\n'+p['variation']+'\n\n## Límites\n\n'+p['limit']+'\n\n## Evidencia\n\n'+'\n'.join(f"- {i}: {obs[i]['title']} · {obs[i]['date']} · {obs[i]['url']}" for i in p['evidence'])+'\n',encoding='utf-8')
 end()
start('Lo que no se convierte en patrón')
photo('SV020',104,w=250,maxh=125);photo('SV036',104,x=306,w=249,maxh=125)
y=para('Placa de calle y colección de imágenes',251,'head')+5
y=para('SV020 muestra señalética cerámica localizada. SV036 muestra objetos enmarcados cuyo material no está confirmado. Ninguno justifica un patrón de azulejos extendido por el radio. Por eso no existe una ficha general de «cerámica, imágenes y ornamento».',y)+21
for title,body in [('Estructura única del barrio','No está demostrada. El entramado se explica como tipo documentado y caso visible; ni el revoco ni el ladrillo visto permiten asignar el sistema resistente oculto a todo un inmueble.'),('«Típico» no significa «exclusivo»','Balcón, reja, zócalo y persiana aparecen también fuera del Rastro. El catálogo muestra su combinación y variaciones locales, no una identidad exclusiva.'),('Habitación y uso social','La ropa tendida, las pantallas y los objetos son visibles. No se deducen composición de hogares, ingresos, rutinas ni satisfacción residencial.'),('Datos sin geometría no son ausencia','El servicio municipal devolvió 2.186 registros de puestos con geometría nula. Se conserva la respuesta para auditoría, pero no se dibujan coordenadas inventadas ni se informa de cero puestos dentro del círculo.')]:
 y=para(title,y,'head')+5;y=para(body,y)+16
end()
start('Conclusiones del catálogo')
y=104
for h,t in [('La unidad predominante del inventario es colectiva','El 91,2 % de los polígonos interiores está etiquetado apartments. Dentro de esa etiqueta coexisten frentes estrechos, bloques mayores, corralas y obras contemporáneas: no es un único sistema constructivo.'),('El orden más repetido se encuentra en las relaciones','Huecos alineados, base diferenciada, planta baja comercial y piezas añadidas se repiten en posiciones distintas. Son más sólidos como objeto de estudio que un supuesto motivo decorativo único.'),('La sección aclara lo que la foto mezcla','Balcón, galería, reja, toldo y filtro exterior ocupan planos diferentes. El zócalo y los huecos bajos cambian respecto al suelo inclinado. La perspectiva por sí sola no explica estas relaciones.'),('La diferencia territorial importa','El anillo incluye avenidas, nodos de tráfico, bloques del sur y calles estrechas del núcleo. La comparación no se limita a la imagen comercial histórica del Rastro.'),('Las singularidades tienen nombre y lugar','Entramado visible en Carlos Arniches, filtros de Vara de Rey, rehabilitación de Escuelas Pías y celosía de Cebada se presentan como casos localizados. Su interés no depende de fingir que dominan el barrio.'),('El límite pendiente está definido','Falta un censo frente a frente con idéntica ficha, observación dominical completa y acceso autorizado a interiores. La cobertura de doce sectores permite comparar el ámbito, pero no certificar que se haya catalogado todo elemento visible.')]:
 y=para(h,y,'head')+5;y=para(t,y)+16
end()
for offset in range(0,len(SOURCES),5):
 start('Fuentes documentales'+(' / continuación' if offset else ''));y=103
 for code,title,desc,url in SOURCES[offset:offset+5]:
  y=para(code+' · '+escape(title),y,'head')+5;y=para(escape(desc),y)+4;y=para(f"<link href='{escape(url)}'>Abrir fuente original</link>",y,'small')+22
 para('Además: fotografías de Google Maps/Street View con atribución y fecha individual; inventario OSM local y dos referencias editoriales aportadas por el usuario. Las páginas y fuentes web se consultaron el 21-22 de septiembre de 2026.',748,'small');end()
ordered=sorted(obs.values(),key=lambda r:(r['id'].startswith('SV'),r['id']))
for offset in range(0,len(ordered),12):
 start('Registro de fotografías y posiciones'+(' / continuación' if offset else ''));y=97
 for r in ordered[offset:offset+12]:
  y=para(f"<b>{r['id']} · {escape(r['title'])}</b> · {escape(r['date'])} · {escape(r['author'])}<br/>{r['lat']:.7f}, {r['lon']:.7f} · {r['distance_m']} m al centro · S{r['sector']} · <link href='{escape(r['url'])}'>Abrir panorama original</link>",y,'small')+13
 end()
c.save()
for r in obs.values():r.pop('xy',None)
(DATA/'observaciones_verificadas.json').write_text(json.dumps(list(obs.values()),ensure_ascii=False,indent=2))
(DATA/'patrones_y_evidencias.json').write_text(json.dumps(PATTERNS,ensure_ascii=False,indent=2))
features=[dict(type='Feature',geometry=dict(type='Point',coordinates=[r['lon'],r['lat']]),properties={k:v for k,v in r.items() if k not in ['lat','lon']}) for r in obs.values()]
(DATA/'observaciones_patrones_QGIS.geojson').write_text(json.dumps(dict(type='FeatureCollection',features=features),ensure_ascii=False))
(DATA/'fuentes_documentales.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2))
(OUT/'LEEME.md').write_text(f'''# Catálogo analítico de patrones · 600 m

Documento principal: CATALOGO_PATRONES_EL_RASTRO_600M.pdf

- 25 fichas específicas; 50 diagramas vectoriales SVG en las carpetas P01-P25.
- {len(obs)} capturas registradas en {unique_sites} posiciones de cámara, todas dentro del círculo.
- 15 capturas nuevas: anillo de doce sectores, Mira el Sol y dos vistas de Escuelas Pías.
- Fotografías seleccionadas y FICHA.md por patrón. Las capturas anteriores se conservan en PATRONES_STREET_VIEW.
- DATOS: GeoJSON de observaciones, ámbito, inventario OSM recortado, estadísticas y respuestas fuente.
- work: scripts reproducibles y comprobaciones editoriales.

Se ha eliminado «Lectura de proyecto» de esta nueva versión. Las referencias editoriales inspiran comparación y anotaciones, no adornos.

Alcance: cobertura territorial con muestreo visual; NO censo exhaustivo de todos los inmuebles. Las estadísticas OSM no son un censo de fachadas ni de estructura. Las fotografías son históricas (2016-2025). Los diagramas son esquemáticos y sin escala, salvo medidas documentales señaladas en P23.

La consulta de puestos municipales devolvió 2.186 registros sin geometría. No se interpreta como cero puestos ni se inventa su geolocalización.
''',encoding='utf-8')
(WORK/'paginas.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2))
print(json.dumps(dict(pdf=str(pdf),pages=len(PAGES),patterns=len(PATTERNS),drawings=50,photos=len(obs),positions=unique_sites),ensure_ascii=False))
