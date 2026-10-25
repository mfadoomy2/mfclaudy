import json
from pathlib import Path
from shapely.geometry import Polygon,Point,LineString
from shapely.ops import unary_union,polygonize
P=Path(__file__).resolve().parents[1];d=json.loads((P/'verificacion/EXTRACCION_REVISION_RHINO.json').read_text())[2];pb=json.loads((P/'verificacion/PROGRAMA_PUBLICO_PB.json').read_text())
def reg(o):
 ps=[p for p in o['profiles'] if len(p)>3 and Point(p[0][:2]).distance(Point(p[-1][:2]))<.002]
 if ps:
  p=Polygon([q[:2] for q in ps[0]],[[q[:2] for q in p] for p in ps[1:]])
  return p if p.is_valid else p.buffer(0)
 out=Polygon()
 for p in o['sections']:
  if len(p)>3 and Point(p[0][:2]).distance(Point(p[-1][:2]))<.002:
   g=Polygon([q[:2] for q in p]);out=out.symmetric_difference(g if g.is_valid else g.buffer(0))
 return out
routes=[('principal',LineString(pb['route']).buffer(.75,cap_style=2)),('biblioteca',LineString(pb['library_route']).buffer(.65,cap_style=2))]
results=[]
for state in ['diario','domingo']:
 bad=[]
 for o in d['objects']:
  la=o['layer'];n=o['name'];z0=o['bbox'][0][2];z1=o['bbox'][1][2]
  if z0>=2.2 or z1<=0 or la not in ['01_MUROS','15_BANOS','19_SOPORTE_PB','20_COMUN_EDIFICIO','21_NUCLEO_VERTICAL','25_PUBLICO_FIJO','26_ESTUDIO_DIARIO','27_EXPOSICION_DOMINGO','29_AGUA_Y_PAISAJE']:continue
  if la==('27_EXPOSICION_DOMINGO' if state=='diario' else '26_ESTUDIO_DIARIO'):continue
  if n.startswith(('Dintel','Techo')) or 'marco' in n.lower():continue
  g=reg(o)
  for title,route in routes:
   ov=g.intersection(route).area
   if ov>.005:bad.append({'object':n,'layer':la,'route':title,'overlap_m2':round(ov,4)})
 results.append({'state':state,'collisions':bad})
report={'route_scope':'Altura libre considerada 2.20m. Recorrido principal 1.50m y rama biblioteca 1.30m, respecto a geometria nativa con perfiles/secciones disponibles. No certifica normativa, aforo ni todos los movimientos interiores.','results':results}
(P/'verificacion/AUDITORIA_RECORRIDOS_PB.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))
