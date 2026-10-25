import json, math
from shapely.geometry import shape, LineString, Point, Polygon, MultiPolygon
from pyproj import Transformer
T=Transformer.from_crs(4326,25830,always_xy=True); Ti=Transformer.from_crs(25830,4326,always_xy=True)
CL_LL=[[-3.707398, 40.4107728], [-3.7073983, 40.4107101], [-3.7073857, 40.4104051], [-3.7073812, 40.4102963], [-3.7073789, 40.4102361], [-3.7073764, 40.4099075], [-3.7073111, 40.409861], [-3.7073112, 40.4098265], [-3.707312, 40.4094098], [-3.7073129, 40.4093381], [-3.7073162, 40.4090896], [-3.7073162, 40.4089448], [-3.7073161, 40.4085183], [-3.7073525, 40.4079636], [-3.7073588, 40.407784], [-3.7073554, 40.4077559], [-3.7072733, 40.4070758], [-3.7072659, 40.4070146], [-3.7072484, 40.4068953], [-3.7071292, 40.4060971], [-3.7071252, 40.4059975], [-3.7071127, 40.4058366], [-3.7071075, 40.4057392], [-3.7071014, 40.4056914], [-3.7070944, 40.4056362], [-3.7069946, 40.4053079], [-3.7068813, 40.4048919]]
CL=LineString([T.transform(*p) for p in CL_LL])
SITE_LL=(-3.707172,40.407576); SITE=Point(T.transform(*SITE_LL))
PARCELA=shape(json.load(open("datos/parcela_31.geojson"))["features"][0]["geometry"])
BLD=[(shape(f["geometry"]),f["properties"]) for f in json.load(open("datos/catastro_edificios.geojson"))["features"]]
PRT=[(shape(f["geometry"]),f["properties"]) for f in json.load(open("datos/catastro_partes.geojson"))["features"]]
META=json.load(open("/mnt/user-data/uploads/G3 Proyectos/INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/RECORRIDO_STREETVIEW_2026-09-23/G3SV_metadatos.json"))
def cam(e): return T.transform(e["lon"],e["lat"])
def polys(g): return list(g.geoms) if isinstance(g,MultiPolygon) else [g]
