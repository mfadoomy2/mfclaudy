"""Láminas vectoriales y datos reproducibles. No modifica fuentes ni catálogos."""
from pathlib import Path
import sys,json,math,datetime,hashlib
from zoneinfo import ZoneInfo
from collections import Counter
ROOT=Path('/Volumes/T7/G3 Proyectos/INVESTIGACIÓN');BASE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'CATALOGO_EDITORIAL_RIBERA/work/deps'))
from shapely.geometry import shape,Point,box,mapping
from shapely.ops import transform,unary_union
from pyproj import Transformer,Geod
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color,black,white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader,PdfWriter

DATA=BASE/'DATOS';DATA.mkdir(exist_ok=True)
SOURCE=ROOT/'CATALOGO_PATRONES_600M/DATOS/ambito_osm_recortado.geojson'
T=Transformer.from_crs(4326,25830,always_xy=True);INV=Transformer.from_crs(25830,4326,always_xy=True)
LON,LAT=-3.707172,40.407576;CX,CY=T.transform(LON,LAT);center=Point(CX,CY)
geod=Geod(ellps='GRS80');items=[];seen=set()
for f in json.loads(SOURCE.read_text())['features']:
 pr=f['properties'];oid=pr['osm_id']
 if oid in seen:continue
 seen.add(oid);g=transform(T.transform,shape(f['geometry']))
 if not g.is_valid:g=g.buffer(0)
 if not g.is_empty:items.append((g,pr))
disc=center.buffer(600,resolution=256)
buildings=[(g,pr) for g,pr in items if pr.get('building') and g.geom_type in ('Polygon','MultiPolygon')]
built=unary_union([g for g,pr in buildings]).intersection(disc)
trees=[(g,pr) for g,pr in items if pr.get('natural')=='tree' and g.geom_type=='Point' and disc.covers(g)]
benches=[(g.representative_point(),pr) for g,pr in items if pr.get('amenity')=='bench' and disc.covers(g.representative_point())]
water=[(g.representative_point(),pr) for g,pr in items if pr.get('amenity')=='drinking_water' and disc.covers(g.representative_point())]
ornamental=[(g.representative_point(),pr) for g,pr in items if pr.get('amenity')=='fountain' and disc.covers(g.representative_point())]
roads=[(g,pr) for g,pr in items if pr.get('highway') and g.geom_type in ('LineString','MultiLineString')]
axis=unary_union([g for g,pr in roads if pr.get('name')=='Calle de la Ribera de Curtidores' or 'Ribera de Curtidores' in pr.get('name','')])
BLUE='#326b88';RED='#ae443a';GREEN='#397665';LIGHT='#e6e2dc';INK='#222222'
finished=[];stats={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'crs':'EPSG:25830','anchor':[LON,LAT]}

class Plate:
 def __init__(self,n,name,title,subtitle):
  self.n=n;self.path=BASE/f'{n:02d}_{name}.pdf';self.c=canvas.Canvas(str(self.path),pagesize=(595.276,841.89));self.c.setTitle(title);self.c.setAuthor('Investigación G3')
  self.text(40,807,'RIBERA DE CURTIDORES / ANÁLISIS DEL LUGAR',9)
  self.text(40,777,f'{n:02d} / {title}',22)
  self.para(subtitle,40,754,515,10.5)
 def text(self,x,y,s,size=10,col=INK,font='Times-Roman'):
  self.c.setFillColor(HexColor(col));self.c.setFont(font,size);self.c.drawString(x,y,str(s))
 def para(self,s,x,y,w=515,size=10.5):
  p=Paragraph(s,ParagraphStyle('p',fontName='Times-Roman',fontSize=size,leading=size*1.3,textColor=HexColor(INK)));_,h=p.wrap(w,1000)
  assert y-h>25,(self.path,y,h);p.drawOn(self.c,x,y-h);return y-h
 def line(self,pts,color=INK,width=.6,dash=None):
  c=self.c;c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.setDash(dash or [])
  if not pts:return
  p=c.beginPath();p.moveTo(*pts[0])
  for q in pts[1:]:p.lineTo(*q)
  c.drawPath(p);c.setDash()
 def geom(self,g,cv,fill=None,stroke='#c7c3bd',width=.25):
  if g.is_empty:return
  if hasattr(g,'geoms'):
   for z in g.geoms:self.geom(z,cv,fill,stroke,width)
  elif g.geom_type=='Polygon':
   p=self.c.beginPath()
   for r in [g.exterior,*g.interiors]:
    pts=[cv(*q) for q in r.coords];p.moveTo(*pts[0])
    for q in pts[1:]:p.lineTo(*q)
    p.close()
   self.c.setStrokeColor(HexColor(stroke));self.c.setLineWidth(width)
   if fill:self.c.setFillColor(HexColor(fill))
   self.c.drawPath(p,fill=bool(fill),stroke=bool(width),fillMode=0)
  elif g.geom_type in ('LineString','LinearRing'):self.line([cv(*q) for q in g.coords],stroke,width)
 def dot(self,x,y,r,col,fill=True):
  self.c.setFillColor(HexColor(col));self.c.setStrokeColor(HexColor(col));self.c.setLineWidth(.6);self.c.circle(x,y,r,fill=int(fill),stroke=1)
 def map(self,x=45,y=342,size=490,r=640,field=None):
  k=size/(2*r);cv=lambda a,b:(x+(a-CX+r)*k,y+(b-CY+r)*k)
  clip=box(CX-r,CY-r,CX+r,CY+r)
  if field:
   for geom,col in field:self.geom(geom,cv,col,col,0)
  for g,pr in buildings:
   if g.intersects(clip):self.geom(g.intersection(clip),cv,LIGHT)
  if not axis.is_empty:self.geom(axis.intersection(clip),cv,stroke='#777777',width=.8)
  for rad in [100,300,600]:
   if rad>r:continue
   self.c.setStrokeColor(HexColor('#aaaaaa'));self.c.setLineWidth(.35);self.c.setDash(2,3);self.c.circle(*cv(CX,CY),rad*k,fill=0,stroke=1);self.c.setDash();self.text(*cv(CX+rad*.71,CY+rad*.71),str(rad)+' m',7)
  self.line([(x+size-12,y+size-32),(x+size-12,y+size-12)],width=.8)
  self.line([(x+size-16,y+size-19),(x+size-12,y+size-12),(x+size-8,y+size-19)],width=.8)
  self.text(x+size-15,y+size-8,'N',8)
  self.line([(x+6,y+8),(x+6+100*k,y+8)],width=1.2)
  for xx in [x+6,x+6+100*k]:self.line([(xx,y+5),(xx,y+11)])
  self.text(x+6,y+16,'100 m',7.5)
  xx,yy=cv(CX,CY);self.line([(xx-4,yy),(xx+4,yy)],RED,1);self.line([(xx,yy-4),(xx,yy+4)],RED,1)
  return cv,clip
 def footer(self,ref,method):
  self.para(method,40,102,515,8.5)
  self.para('Referencia de lenguaje: '+ref+'. Base blanca, geometría repetida, variable y conclusión explícitas.',40,64,515,8)
  self.text(40,27,'INVESTIGACIÓN G3 / 23.09.2026',8);self.text(534,27,str(self.n),8)
 def save(self):
  self.c.save();finished.append(self.path)
  writer=PdfWriter()
  for f in finished:writer.append(str(f))
  with (BASE/'ANALISIS_DEL_LUGAR_PRECISO.pdf').open('wb') as f:writer.write(f)
  (BASE/'ESTADO.json').write_text(json.dumps({'completadas':[p.name for p in finished],'total_previsto':5,'datos':stats},ensure_ascii=False,indent=2))
  print('GUARDADO',self.path.name,flush=True)

# 01. Publicación climatológica de AEMET, transcripción de T, TM, Tm y R.
climate={'station':'Madrid, Retiro','id':'3195','period':'1981-2010','url':'https://www.aemet.es/es/serviciosclimaticos/datosclimatologicos/valoresclimatologicos?l=3195',
 'T':[6.3,7.9,11.2,12.9,16.7,22.2,25.6,25.1,20.9,15.1,9.9,6.9],
 'TM':[9.8,12,16.3,18.2,22.2,28.2,32.1,31.3,26.4,19.4,13.5,10],
 'Tm':[2.7,3.7,6.2,7.7,11.3,16.1,19,18.8,15.4,10.7,6.3,3.6],
 'R':[33,34,25,45,50,21,12,10,22,60,58,51]}
(DATA/'clima_AEMET_3195.json').write_text(json.dumps(climate,indent=2))
p=Plate(1,'CLIMA_DE_REFERENCIA','Calor y lluvia: el ciclo anual','Madrid-Retiro, AEMET 3195. Normales 1981-2010: referencia histórica, no clima medido en Ribera ni episodio extremo actual.')
p.text(45,701,'TEMPERATURA DEL AIRE / °C',11);xs=[65+i*43 for i in range(12)];months=['E','F','M','A','M','J','J','A','S','O','N','D']
for t in range(0,36,5):
 y=455+t*6;p.line([(60,y),(550,y)],'#dddddd',.4);p.text(40,y-3,t,8)
for key,col,dash in [('TM',RED,None),('T',INK,None),('Tm',BLUE,[3,2])]:
 p.line(list(zip(xs,[455+t*6 for t in climate[key]])),col,1.6,dash)
 for x,t in zip(xs,climate[key]):p.dot(x,455+t*6,1.5,col)
for x,m in zip(xs,months):p.text(x-3,440,m,9)
p.text(45,419,'TM: media de máximas diarias',9,RED);p.text(245,419,'T: media',9);p.text(360,419,'Tm: media de mínimas diarias',9,BLUE)
p.text(45,386,'PRECIPITACIÓN MEDIA / mm por mes',11)
for r in [0,20,40,60]:
 y=222+r*2.1;p.line([(60,y),(550,y)],'#dddddd',.4);p.text(39,y-3,r,8)
for x,r,m in zip(xs,climate['R'],months):
 p.c.setFillColor(HexColor(BLUE));p.c.rect(x-10,222,20,r*2.1,fill=1,stroke=0);p.text(x-6,228+r*2.1,r,8);p.text(x-3,207,m,9)
p.para('<b>Lectura para el edificio.</b> Julio reúne una media de máximas de 32,1 °C y 12 mm de lluvia; agosto, 31,3 °C y 10 mm. Conviene ensayar protección solar regulable y una estrategia de agua que no dependa de lluvia estival. En invierno, comprobar la entrada de sol antes de fijar una protección permanente.',45,180,505,10.5)
p.footer('CLI-05 AIRE y CLI-07 AGUA','Fuente: AEMET, normales de Retiro 1981-2010, consultadas el 23/09/2026. La estación no representa la temperatura superficial ni el microclima de cada calle. URL y valores completos: DATOS/clima_AEMET_3195.json.');p.save()

# 02. NOAA: cálculo solar geométrico aproximado, sin refracción.
def solar(dt):
 u=dt.astimezone(datetime.timezone.utc);hr=u.hour+u.minute/60+u.second/3600
 ga=2*math.pi/365*(u.timetuple().tm_yday-1+(hr-12)/24)
 eq=229.18*(.000075+.001868*math.cos(ga)-.032077*math.sin(ga)-.014615*math.cos(2*ga)-.040849*math.sin(2*ga))
 dec=.006918-.399912*math.cos(ga)+.070257*math.sin(ga)-.006758*math.cos(2*ga)+.000907*math.sin(2*ga)-.002697*math.cos(3*ga)+.00148*math.sin(3*ga)
 ha=math.radians((hr*60+eq+4*LON)/4-180);lat=math.radians(LAT)
 alt=math.asin(math.sin(lat)*math.sin(dec)+math.cos(lat)*math.cos(dec)*math.cos(ha))
 az=(math.degrees(math.atan2(math.sin(ha),math.cos(ha)*math.sin(lat)-math.tan(dec)*math.cos(lat)))+180)%360
 return az,math.degrees(alt)
dates=[(3,21,'21 marzo',GREEN),(6,21,'21 junio',RED),(12,21,'21 diciembre',BLUE)];solarrows=[]
p=Plate(2,'GEOMETRIA_SOLAR','De dónde llega el sol','Posición de estudio: 40,407576 N / 3,707172 O. Año 2026. Hora civil Europe/Madrid, incluido el cambio horario.')
p.text(45,699,'TRAYECTORIA SOLAR / azimut y elevación geométrica',11)
for alt in [0,15,30,45,60,75,90]:
 y=440+alt*2.35;p.line([(62,y),(550,y)],'#dddddd',.35);p.text(38,y-3,str(alt)+'°',8)
for az in [60,90,120,150,180,210,240,270,300]:
 x=62+(az-45)/270*488;p.line([(x,440),(x,660)],'#eeeeee',.3);p.text(x-9,425,str(az)+'°',8)
for mo,day,name,col in dates:
 points=[]
 for minute in range(0,1440,5):
  dt=datetime.datetime(2026,mo,day,minute//60,minute%60,tzinfo=ZoneInfo('Europe/Madrid'));az,el=solar(dt)
  if el>=0:points.append((62+(az-45)/270*488,440+el*2.35))
 p.line(points,col,1.5)
 for hour in [9,12,15,18]:
  az,el=solar(datetime.datetime(2026,mo,day,hour,tzinfo=ZoneInfo('Europe/Madrid')))
  solarrows.append({'date':f'2026-{mo:02}-{day:02}','hour_local':hour,'azimuth_deg':round(az,4),'elevation_deg':round(el,4)})
  if el>=0:
   x,y=62+(az-45)/270*488,440+el*2.35;p.dot(x,y,2,col);p.text(x+4,y+5,str(hour)+'h',8,col)
for j,(mo,day,name,col) in enumerate(dates):
 x=45+j*176;p.text(x,397,name,11,col);cv,clip=p.map(x,216,154,180)
 for hour in [9,12,15,18]:
  az,el=solar(datetime.datetime(2026,mo,day,hour,tzinfo=ZoneInfo('Europe/Madrid')))
  if el<0:continue
  lo,la,_=geod.fwd(LON,LAT,az,135);ex,ey=T.transform(lo,la);a=cv(CX,CY);b=cv(ex,ey)
  p.line([a,b],col,.9);p.dot(*b,2,col);p.text(b[0]+3,b[1]+2,str(hour),7,col)
p.para('<b>Los radios apuntan hacia el sol, no hacia la sombra.</b> E = 90°, S = 180°, O = 270°. El arco invernal es más bajo: una protección fija debe comprobarse también en diciembre. Para un mapa real de sombras faltan alturas, terreno y obstáculos verificados; estas curvas no los suponen.',45,190,505,10)
p.footer('CLI-01 SOMBRA y SHADOW_HOURLY_ATLAS','Método NOAA, General Solar Position Calculations: gml.noaa.gov/grad/solcalc/solareqns.PDF. Aproximación astronómica; sin nubes, refracción ni obstáculos. Radios convertidos geodésicamente a EPSG:25830; minimapas con igual escala.');p.save()
(DATA/'posiciones_solares.json').write_text(json.dumps(solarrows,indent=2))

# 03. Unión geométrica: evita doble contabilización de solapes.
occup=[]
for rad in [100,300,600]:
 d=center.buffer(rad,resolution=256);a=built.intersection(d).area
 occup.append({'radius_m':rad,'area_m2':d.area,'building_union_m2':a,'fraction':a/d.area})
stats['occupation']=occup
p=Plate(3,'TEJIDO_Y_VACIOS','Cuánto suelo ocupa la edificación','Huellas cartográficas en un radio de 600 m. Superficies calculadas en ETRS89 / UTM 30N; centro aproximado de Ribera 31.')
cv,clip=p.map(102,322,390,640)
p.para('Gris: huella de edificio. Blanco: superficie no ocupada por esas huellas. Círculos: radios de 100, 300 y 600 m. Cruz roja: referencia de estudio. El blanco incluye calles y patios; no significa suelo público ni permeable.',45,310,505,9)
p.text(45,271,'OCUPACIÓN POR RADIO / misma definición en los tres ámbitos',11)
for i,row in enumerate(occup):
 y=242-i*29;p.text(45,y,str(row['radius_m'])+' m',10);p.c.setFillColor(HexColor('#e5e5e5'));p.c.rect(99,y-2,300,10,fill=1,stroke=0);p.c.setFillColor(HexColor('#656565'));p.c.rect(99,y-2,300*row['fraction'],10,fill=1,stroke=0);p.text(413,y,f"{row['fraction']*100:.1f} % / {row['building_union_m2']/10000:.2f} ha",10)
p.para('<b>Lectura.</b> La ocupación sube del 37,4 % en 600 m al 49,9 % en 100 m. La proximidad está más ocupada según esta base. Para hacer habitable un vacío hay que verificar acceso, proporción vertical, luz y ventilación; superficie libre no equivale a calidad climática.',45,151,505,10)
p.footer('URB-02 BORDES Y FACHADAS y mapas de ocupación del compendio','Base: archivo OSM local 21-22/09/2026; unión de geometrías building, recorte circular métrico y cálculo de áreas. Sin alturas supuestas, sin parcelario catastral. Las geometrías conservan la precisión del archivo fuente.');p.save()

# 04. Distancia a árboles: magnitud cartográfica, no temperatura ni copa.
treeunion=unary_union([g for g,pr in trees]);nearest=sorted([(center.distance(g),g,pr) for g,pr in trees],key=lambda v:v[0])
treecounts=[sum(center.distance(g)<=r for g,pr in trees) for r in [100,300,600]]
from shapely.strtree import STRtree
tg=[g for g,pr in trees];treeindex=STRtree(tg);field=[];fielddata=[];inner=center.buffer(300,resolution=128)
distancecolors=['#d4e8df','#a1c8b7','#e8d4ab','#c39770']
for dx in range(-300,300,20):
 for dy in range(-300,300,20):
  square=box(CX+dx,CY+dy,CX+dx+20,CY+dy+20).intersection(inner)
  if square.is_empty:continue
  point=square.centroid;near=tg[int(treeindex.nearest(point))];dd=point.distance(near);cl=0 if dd<=10 else 1 if dd<=25 else 2 if dd<=50 else 3
  field.append((square,distancecolors[cl]));fielddata.append({'type':'Feature','geometry':mapping(transform(INV.transform,square)),'properties':{'distancia_arbol_m':round(dd,2),'clase':cl,'muestreo':'centro_celda_20m'}})
(DATA/'distancia_arbolado_20m.geojson').write_text(json.dumps({'type':'FeatureCollection','features':fielddata}))
stats['trees']={'counts_100_300_600':treecounts,'nearest_distance_m':nearest[0][0],'nearest_osm_id':nearest[0][2]['osm_id']}
p=Plate(4,'ARBOLADO_Y_PROXIMIDAD','Dónde está el arbolado registrado','Puntos natural=tree del archivo local. Comparación entre Ribera y su entorno; no se atribuye una copa a un punto sin dimensiones.')
cv,clip=p.map(102,322,390,640,field=field)
for g,pr in trees:p.dot(*cv(g.x,g.y),1.6,GREEN)
dist,g,pr=nearest[0];p.line([cv(CX,CY),cv(g.x,g.y)],RED,1.2);p.dot(*cv(g.x,g.y),3,RED,False)
p.para('Dentro de 300 m: distancia al árbol registrado más cercano, muestreada en celdas de 20 m. Puntos: árboles, no copas. Gris: edificios. El color mide proximidad, no temperatura ni sombra.',45,310,505,9)
for i,(col,txt) in enumerate(zip(distancecolors,['≤10 m','10-25 m','25-50 m','>50 m'])):
 x=45+i*124;p.c.setFillColor(HexColor(col));p.c.rect(x,266,15,8,fill=1,stroke=0);p.text(x+21,266,txt,9)
for i,(r,count) in enumerate(zip([100,300,600],treecounts)):
 x=45+i*174;p.text(x,233,str(count),24,GREEN);p.text(x,216,f'árboles a ≤ {r} m',10)
p.para(f'<b>Referencia:</b> {dist:.0f} m en línea recta al registro más próximo ({pr["osm_id"]}). Recuentos acumulados. La trama permite localizar sectores más alejados del arbolado registrado; no acredita un recorrido accesible.',45,197,505,10)
p.para('<b>Implicación.</b> Verificar copa, estado, relación con el sol y posibilidad de estancia antes de apoyar el acceso o espacio común en un árbol cercano.',45,144,505,10)
p.footer('CLI-06 VEGETACION y AGU-02 ECOLOGIA','OSM local; puntos únicos por osm_id dentro del círculo de 600 m. Se excluyen tree_row del recuento individual y se conserva su información en la base original. Distancia euclídea en EPSG:25830. Ausencia cartográfica no demuestra ausencia física.');p.save()

# 05. Dos recursos observables, sin índice de confort inventado.
p=Plate(5,'ESTANCIA_Y_AGUA','Sentarse y encontrar agua','Bancos y puntos de agua cartografiados en el mismo radio de 600 m. Recursos a verificar para relacionar planta baja, calle y estancia.')
cv,clip=p.map(102,322,390,640)
for g,pr in benches:
 x,y=cv(g.x,g.y);p.c.setFillColor(HexColor(INK));p.c.rect(x-1.4,y-1.4,2.8,2.8,fill=1,stroke=0)
for g,pr in ornamental:p.dot(*cv(g.x,g.y),2.5,BLUE,False)
for i,(g,pr) in enumerate(sorted(water,key=lambda z:center.distance(z[0])),1):
 p.dot(*cv(g.x,g.y),2.6,BLUE)
for i,(g,pr) in enumerate(sorted(water,key=lambda z:center.distance(z[0]))[:3],1):
 x,y=cv(g.x,g.y);dx,dy={1:(-26,-9),2:(14,9),3:(14,-16)}[i];lx,ly=x+dx,y+dy
 p.line([(x,y),(lx+6,ly+3)],BLUE,.55);p.c.setFillColor(white);p.c.rect(lx-1,ly-2,16,11,fill=1,stroke=0);p.text(lx,ly,'F'+str(i),8,BLUE)
p.para('Cuadrado negro: banco. Círculo azul lleno: amenity=drinking_water. Círculo azul vacío: fuente ornamental, amenity=fountain. El código cartográfico no acredita funcionamiento, potabilidad o acceso actual.',45,310,505,9)
p.text(45,271,f'{len(benches)} bancos',18);p.text(220,271,f'{len(water)} agua de beber*',18,BLUE);p.text(422,271,f'{len(ornamental)} ornamentales',13,BLUE)
nearwater=sorted(water,key=lambda z:center.distance(z[0]))[:3];resources=[]
for i,(g,pr) in enumerate(nearwater,1):
 dis=center.distance(g);y=241-(i-1)*20;p.text(45,y,f'F{i}',10,BLUE);p.text(80,y,f'{dis:.0f} m en línea recta',10);p.text(267,y,pr['osm_id'],9)
 resources.append({'label':f'F{i}','osm_id':pr['osm_id'],'distance_m':dis,'coordinates_4326':list(INV.transform(g.x,g.y))})
nb=min(benches,key=lambda z:center.distance(z[0]));stats['stay']={'benches':len(benches),'drinking_water':len(water),'ornamental':len(ornamental),'nearest_bench_m':center.distance(nb[0]),'nearest_water':resources}
p.para(f'<b>Implicación.</b> El banco registrado más cercano queda a {center.distance(nb[0]):.0f} m en planta. Ensayar un umbral donde detenerse y disponer de agua exige comprobar también sombra, paso libre y gestión. El mapa localiza recursos; no calcula afluencia ni confort térmico.',45,167,505,10)
p.footer('SOC-01 POTENCIAL DE ESTANCIA y CLI-07 AGUA','OSM local; selección por amenity, un registro por osm_id. Distancias euclídeas, no recorridos por la red. *Etiqueta drinking_water: condición declarada en OSM, pendiente de comprobación local. No se aplica el índice ponderado IPE de la referencia.');p.save()

(DATA/'metricas.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
out=[]
for kind,series in [('arbol',trees),('banco',benches),('agua_beber',water),('fuente_ornamental',ornamental)]:
 for g,pr in series:out.append({'type':'Feature','geometry':mapping(transform(INV.transform,g)),'properties':{'tipo':kind,'osm_id':pr['osm_id'],'nombre':pr.get('name',''),'distancia_centro_m':round(center.distance(g),2)}})
(DATA/'recursos_localizados.geojson').write_text(json.dumps({'type':'FeatureCollection','features':out},ensure_ascii=False))
assert len(finished)==5
assert all(len(PdfReader(f).pages)==1 for f in finished)
print(json.dumps(stats,ensure_ascii=False),flush=True)
