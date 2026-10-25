from pathlib import Path
import bpy,json,math,csv,numpy as np,pandas as pd,pvlib
from pyproj import Transformer,Proj
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];S=R.parent/'G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16';A=json.loads((S/'calculo/ESTRUCTURA_RESULTADOS.json').read_text());cache=json.loads((R/'fuentes/geometria_render.json').read_text())
opaque=['90_CONTEXTO','01_BANDEJAS','07_GALERIAS','12_CUBIERTAS','11_ENVOLVENTE_OPACA','24_COMUNES','17_NUCLEOS','02_ESTRUCTURA_RAMAS','26_ARRIOSTRAMIENTO','03_CELOSIAS','32_VIGUETAS','09_ESCALERAS','18_ASCENSOR','13_COSTILLAS']
def tree(layers):
 vs=[];fs=[]
 for b in cache.values():
  if b['layer'] not in layers:continue
  off=len(vs);vs.extend(b['vertices']);fs.extend([[off+i for i in f] for f in b['faces']])
 return BVHTree.FromPolygons(vs,fs,all_triangles=False),len(vs),len(fs)
ctx,nc,fc=tree(['90_CONTEXTO']);base,nb,fb=tree(opaque);sail,_,_=tree(['06_VELAS'])
print('BVH',nc,fc,nb,fb,flush=True)
def sky(p,n,trees,N=512):
 p=Vector(p);n=Vector(n).normalized();num=den=0.
 for i in range(N):
  zz=(i+.5)/N;rr=math.sqrt(1-zz*zz);az=i*2.399963229728653;d=Vector((rr*math.cos(az),rr*math.sin(az),zz));w=max(0,d.dot(n))
  if w<1e-9:continue
  den+=w
  if all(t.ray_cast(p,d,500)[0] is None for t in trees):num+=w
 return 100*num/den
origin=json.loads((S/'fuentes/parcela_local.geojson').read_text())['properties']['origin_utm'];lon,lat=Transformer.from_crs(25830,4326,always_xy=True).transform(origin[0]+35,origin[1]);sun={}
gamma=Proj('EPSG:25830').get_factors(lon,lat).meridian_convergence
for date in ['2026-12-21','2026-03-21','2026-06-21']:
 tt=pd.date_range(date+' 06:00',date+' 22:00',freq='15min',tz='Europe/Madrid',inclusive='left');pos=pvlib.solarposition.get_solarposition(tt,lat,lon,altitude=622.6)
 sun[date]=[(str(t),Vector((math.sin(math.radians(a-gamma))*math.cos(math.radians(e)),math.cos(math.radians(a-gamma))*math.cos(math.radians(e)),math.sin(math.radians(e))))) for t,a,e in zip(tt,pos.azimuth,pos.apparent_elevation) if e>1]
def solar(p,n,trees,date):
 pp=Vector(p);nn=Vector(n);ts=[]
 for t,d in sun[date]:
  if nn.dot(d)>0 and all(tr.ray_cast(pp,d,500)[0] is None for tr in trees):ts.append(t)
 return {'hours':len(ts)*.25,'times':ts}
rows=[]
for i,b in enumerate(A['bays']):
 for face,yy,n in [('sur',b['front']-.08,(0,-1,0)),('norte',b['front']+5.88,(0,1,0))]:
  for dx in [-2.8,0,2.8]:
   pp=(b['x']+dx,yy,1.35);rows.append({'bay':'ABC'[i],'face':face,'dx':dx,'point':pp,'sky_percent':round(sky(pp,n,[base]),3)})
print(rows,flush=True)
(R/'calculo/LUZ_PLANTA_BAJA.json').write_text(json.dumps({'method':'Metrica exterior de cielo, no iluminancia interior; misma geometria V5.','rows':rows},indent=2))
