"""Auditoría reproducible de la instantánea OSM local; no actualiza los originales."""
from pathlib import Path
import csv,json,math,urllib.request,urllib.parse
from collections import Counter
from shapely import wkt
from shapely.geometry import Point,mapping,shape
from shapely.ops import transform,unary_union
from pyproj import Transformer

BASE=Path(__file__).resolve().parents[2]
OUT=BASE/'CATALOGO_PATRONES_600M'
DATA=OUT/'DATOS'; DATA.mkdir(parents=True,exist_ok=True)
T=Transformer.from_crs(4326,25830,always_xy=True)
TI=Transformer.from_crs(25830,4326,always_xy=True)
C=Point(*T.transform(-3.707172,40.407576)); AOI=C.buffer(600,quad_segs=180)
rows=[]
for name in ['PUNTOS','LINEAS','POLIGONOS']:
 with (BASE/f'COORDENADAS_{name}_600M.csv').open(encoding='utf-8-sig') as f:
  for r in csv.DictReader(f):
   g=transform(T.transform,wkt.loads(r['geometria_wkt']))
   if not g.is_valid:g=g.buffer(0)
   if g.is_empty or not g.intersects(AOI):continue
   tags=json.loads(r['tags_json']); p=g.representative_point()
   dx,dy=p.x-C.x,p.y-C.y
   sector=int(((math.degrees(math.atan2(dx,dy))+360+15)%360)//30)+1
   rows.append(dict(id=r['osm_tipo']+'/'+r['osm_id'],tags=tags,g=g,inside=AOI.covers(p),sector=sector,ring='0-300' if p.distance(C)<=300 else '300-600',name=r['nombre']))
unique={r['id']:r for r in rows}; rows=list(unique.values())
b=[r for r in rows if 'building' in r['tags'] and r['g'].geom_type in ('Polygon','MultiPolygon')]
bi=[r for r in b if r['inside']]
urban=[r for r in rows if r['inside']]
foot=unary_union([r['g'].intersection(AOI) for r in b])
stats=dict(centre_wgs84=[-3.707172,40.407576],radius_m=600,crs_metric='EPSG:25830',area_m2=round(AOI.area),entities_intersecting=len(rows),building_polygons_intersecting=len(b),building_representative_point_inside=len(bi),building_union_m2=round(foot.area),building_union_pct=round(100*foot.area/AOI.area,1),building_types=dict(Counter(r['tags']['building'] for r in bi)),levels=dict(Counter(r['tags'].get('building:levels','NO_DATO') for r in bi)),material=dict(Counter(r['tags'].get('building:material','NO_DATO') for r in bi)),start_date=dict(Counter(r['tags'].get('start_date','NO_DATO') for r in bi)),roof_shape=dict(Counter(r['tags'].get('roof:shape','NO_DATO') for r in bi)),shops=dict(Counter(r['tags']['shop'] for r in urban if 'shop' in r['tags'])),craft=dict(Counter(r['tags']['craft'] for r in urban if 'craft' in r['tags'])),sector_buildings=dict(Counter(r['sector'] for r in bi)),notes=['Instantánea local OSM ya existente; no censo catastral ni levantamiento actualizado.','Intersección geométrica con círculo métrico; conteos de edificios por punto representativo interior.','OSM puede dividir o agrupar un inmueble; polígonos no equivalen a viviendas, portales ni parcelas.','Ocupación es unión de huellas OSM recortadas, no edificabilidad. Los patios ausentes en la geometría pueden sobreestimarla.'])
(DATA/'estadisticas_ambito.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
features=[]
for r in rows:
 props=dict(osm_id=r['id'],nombre=r['name'],sector=r['sector'],anillo=r['ring'],punto_interior=r['inside'],**r['tags'])
 features.append(dict(type='Feature',geometry=mapping(transform(TI.transform,r['g'].intersection(AOI))),properties=props))
(DATA/'ambito_osm_recortado.geojson').write_text(json.dumps(dict(type='FeatureCollection',features=features),ensure_ascii=False))
(DATA/'radio_600m.geojson').write_text(json.dumps(dict(type='FeatureCollection',features=[dict(type='Feature',geometry=mapping(transform(TI.transform,AOI)),properties={'centro':'Ribera de Curtidores 31, punto aproximado del inventario anterior','radio_m':600})])))
# Posiciones de muestreo: nombres y coordenadas existentes; la calle se verificará en Street View.
for sector in range(1,13):
 outer=[r for r in rows if r['sector']==sector and r['ring']=='300-600' and r['inside'] and r['g'].geom_type=='LineString' and r['tags'].get('highway') in ['residential','pedestrian','tertiary','secondary','living_street'] and r['tags'].get('name')]
 ranked=sorted(outer,key=lambda r:abs(r['g'].representative_point().distance(C)-470))
 print('SECTOR',sector,[(r['name'],[round(v,7) for v in TI.transform(*r['g'].representative_point().coords[0])]) for r in ranked[:3]])
# API municipal documentada: sólo cartografía pública y sin información personal.
service='https://sigma.madrid.es/hosted/rest/services/GEOPORTAL/PUESTOS_RASTRO/MapServer/11'
try:
 features=[]; offset=0
 while True:
  params=urllib.parse.urlencode(dict(f='geojson',where='1=1',outFields='*',returnGeometry='true',outSR=4326,resultOffset=offset,resultRecordCount=1000))
  with urllib.request.urlopen(service+'/query?'+params,timeout=40) as response: obj=json.load(response)
  part=obj.get('features',[])
  if not part:break
  features.extend(part); offset+=len(part)
  if len(part)<1000:break
 filtered=[f for f in features if f.get('geometry') and transform(T.transform,shape(f['geometry'])).intersects(AOI)]
 stats['puestos_sin_geometria']=sum(not f.get('geometry') for f in features)
 (DATA/'registro_puestos_municipales_sin_recorte.json').write_text(json.dumps(dict(type='FeatureCollection',features=features),ensure_ascii=False))
 if filtered:(DATA/'puestos_municipales_600m.geojson').write_text(json.dumps(dict(type='FeatureCollection',features=filtered),ensure_ascii=False))
 stats['puestos_municipales_total_servicio']=len(features)
 stats['puestos_municipales_intersectan_600m']=len(filtered) if stats['puestos_sin_geometria']<len(features) else None
 stats['puestos_fuente']=service;stats['puestos_limite']='Registros del servicio municipal. La consulta devuelve atributos pero no geometrías: no se puede dar un recuento recortado a 600 m ni equipararlo a vendedores activos.'
except Exception as exc:stats['puestos_error']=str(exc)
(DATA/'estadisticas_ambito.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
print(json.dumps(stats,ensure_ascii=False,indent=2))
