import sqlite3, json, math, collections
from shapely import wkb
from shapely.geometry import shape, Point
from shapely.ops import transform
from pyproj import Transformer
T=Transformer.from_crs(4326,25830,always_xy=True).transform
G='/mnt/user-data/uploads/G3 Proyectos/INVESTIGACIÓN/INVENTARIO_FISICO_600M.gpkg'
c=sqlite3.connect(G)
def gp(b):
    # gpkg header
    flags=b[3]; env=(flags>>1)&7; n={0:0,1:32,2:48,3:48,4:64}[env]
    return wkb.loads(bytes(b[8+n:]))
par=shape(json.load(open('/home/claude/g3/datos/parcela_31.geojson'))['features'][0]['geometry']) if 'features' in json.load(open('/home/claude/g3/datos/parcela_31.geojson')) else shape(json.load(open('/home/claude/g3/datos/parcela_31.geojson'))['geometry'])
C=par.centroid; print('parcel centroid',C.x,C.y)
feats=[]
for t in ['puntos_fisicos','lineas_fisicas','poligonos_fisicos']:
    for fid,g,temas,sub,nom in c.execute(f'select fid,geom,temas,subtipo,nombre from {t}'):
        geo=transform(T,gp(g)); feats.append(dict(t=t,temas=[x.strip() for x in (temas or '').split('|')],sub=sub,nom=nom,g=geo))
import numpy as np
xs=[f['g'].centroid.x for f in feats if f['t']=='puntos_fisicos']; ys=[f['g'].centroid.y for f in feats if f['t']=='puntos_fisicos']
print('pts bbox',min(xs),max(xs),min(ys),max(ys),'center',(min(xs)+max(xs))/2,(min(ys)+max(ys))/2)
d=[math.hypot(x-C.x,y-C.y) for x,y in zip(xs,ys)]; print('max dist from parcel',max(d))
import pickle; pickle.dump(dict(C=(C.x,C.y),feats=[dict(t=f['t'],temas=f['temas'],sub=f['sub'],nom=f['nom'],wkt=f['g'].wkt) for f in feats]),open('osm.pkl','wb'))
subs=collections.Counter((f['temas'][0],f['sub']) for f in feats if 'TRANSPORTE' in f['temas'] or 'PATRIMONIO_Y_CULTURA' in f['temas'])
print(subs.most_common(40))
