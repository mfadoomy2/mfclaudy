from pathlib import Path
import bpy,json,math,csv,numpy as np,pandas as pd,pvlib
from pyproj import Transformer,Proj
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];S=R.parent/'G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16';A=json.loads((S/'calculo/ESTRUCTURA_RESULTADOS.json').read_text());cache=json.loads((S/'fuentes/geometria_render.json').read_text())
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
 for h,(xx,yy,sg) in enumerate([(-3.14,0,-1),(3.14,0,-1),(-3.14,6.8,1),(3.14,6.8,1)],1):
  cx,f,z=plate['cx'],plate['front'],plate['z'];n=(0,sg,0);samples=[(cx+xx+dx,f+yy+sg*.09,z+1.35+dz) for dx,dz in [(0,0),(-.6,-.35),(.6,-.35),(-.6,.35),(.6,.35)]]
  vals={k:np.mean([sky(p,n,t) for p in samples]) for k,t in [('sky_context',[ctx]),('sky_v4_clear_sail',[base]),('sky_v4_opaque_sail',[base,sail])]}
  ry=1.65 if sg<0 else 5.45;rz=2.2+2.1*math.sqrt(1-(xx/4.8)**2);rn=Vector((2.1*xx/(4.8**2*math.sqrt(1-(xx/4.8)**2)),0,1)).normalized();rp=Vector((cx+xx,f+ry,z+rz))+rn*.10
  vals['sky_roof_aperture_clear_sail']=sky(rp,rn,[base]);vals['sky_roof_aperture_opaque_sail']=sky(rp,rn,[base,sail]);vals['sky_v4_1024_check']=sky(samples[0],n,[base],1024);vals['sky_v4_512_centre']=sky(samples[0],n,[base],512)
  ss={date:solar(samples[0],n,[base],date) for date in sun};rs={date:solar(rp,rn,[base],date) for date in sun}
  row={'unit':plate['id'],'room':'H'+str(h),'bay':plate['bay'],'z':z,'orientation':'sur' if sg<0 else 'norte','window_point':samples[0],'roof_aperture_point':list(rp),'roof_aperture_normal':list(rn),**{k:round(float(v),3) for k,v in vals.items()},'sun_window_clear_sail':ss,'sun_roof_clear_sail':rs}
  rows.append(row)
 print(plate['id'],[(r['room'],r['sky_v4_clear_sail'],r['sky_roof_aperture_clear_sail']) for r in rows[-4:]],flush=True)
report={'method':'Trazado geometrico de rayos BVH, cielo uniforme superior ponderado por coseno de incidencia; 5 muestras por fachada, 512 direcciones; control a 1024 en punto central. No es factor de luz diurna, sDA, UDI ni lux.','north':'Ejes locales asumidos alineados a EPSG:25830: +X este, +Y norte de cuadricula. Se entrega sensibilidad pendiente a convergencia meridiana; no se ha contrastado replanteo topografico.','location':{'lat':lat,'lon':lon,'grid_convergence_deg':gamma},'occluder_layers':opaque,'sail':'Dos extremos geometricos: vela omitida (limite favorable) y opaca (desfavorable). No se dispone de transmitancia medida.','sun':'pvlib SPA, Europe/Madrid, paso15min, elevacion aparente>1deg, punto central exterior. Son intervalos discretos sin nubes ni reflexiones.','roof':'Ensayo de nuevo hueco sobre cada cuarto; punto exterior a la boveda, sin valorar transmision, superficie efectiva ni distribucion interior. No se suman los porcentajes de fachada y cubierta.','rows':rows,'mesh_counts':{'context_faces':fc,'opaque_faces':fb},'max_sampling_difference_pp':max(abs(r['sky_v4_1024_check']-r['sky_v4_512_centre']) for r in rows)}
(R/'calculo/LUZ_40_HABITACIONES.json').write_text(json.dumps(report,indent=2))
keys=['unit','room','z','orientation','sky_context','sky_v4_clear_sail','sky_v4_opaque_sail','sky_roof_aperture_clear_sail','sky_roof_aperture_opaque_sail']
with (R/'calculo/LUZ_40_HABITACIONES.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:r[k] for k in keys} for r in rows)
print('FIN_LUZ',report['max_sampling_difference_pp'],flush=True)
