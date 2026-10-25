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
for plate in A['plates']:
 for h,xx in enumerate([-3.6,-1.2,1.2,3.6],1):
  cx,f,z=plate['cx'],plate['front'],plate['z'];n=(0,1,0);samples=[(cx+xx+dx,f+6.89,z+1.35+dz) for dx,dz in [(0,0),(-.6,-.35),(.6,-.35),(-.6,.35),(.6,.35)]]
  skyval=float(np.mean([sky(p,n,[base]) for p in samples]));rz=2.2+2.1*math.sqrt(1-(xx/4.8)**2);rn=Vector((2.1*xx/(4.8**2*math.sqrt(1-(xx/4.8)**2)),0,1)).normalized();rp=Vector((cx+xx,f+5.65,z+rz))+rn*.10
  rows.append({'unit':plate['id'],'room':'H'+str(h),'z':z,'orientation':'norte','window_point':samples[0],'sky_v5':round(skyval,3),'sky_roof_v5':round(sky(rp,rn,[base]),3),'sun_window':{date:solar(samples[0],n,[base],date) for date in sun},'sun_roof':{date:solar(rp,rn,[base],date) for date in sun},'room_nominal_m2':2.4*3.9,'room_clear_geometric_approx_m2':2.31*3.81})
 print('V5',plate['id'],[r['sky_v5'] for r in rows[-4:]],flush=True)
res={'rows':rows,'method':'Misma metrica geometrica de cielo de V4, nueva geometria V5; velas de verano recogidas. Todos los puntos de fachada al norte, a 1.35m. No certifica iluminacion interior.','room_logic':'4 habitaciones al norte, servicios al sur, paso transversal1.20m; cuerpo9.60x7.50. Terraza frontal1.40m nominal sin mobiliario en paso.','source_model':'SELVA_V5_LUZ_Y_PLANTA_BAJA.3dm','location':{'lat':lat,'lon':lon,'grid_convergence_deg':gamma},'excluded':'Transmitancias, interreflexiones, vegetacion, muebles, barandillas y elementos muy finos; sin archivo meteorologico ni iluminancia; no verificar sDA/UDI/DF.', 'mesh_faces':fb}
(R/'calculo/LUZ_V5_40_HABITACIONES.json').write_text(json.dumps(res,indent=2));print('FIN_V5',flush=True)
