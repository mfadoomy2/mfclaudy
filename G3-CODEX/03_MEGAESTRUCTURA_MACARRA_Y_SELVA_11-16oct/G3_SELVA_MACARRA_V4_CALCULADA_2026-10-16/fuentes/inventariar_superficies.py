from pathlib import Path
import json,math,collections,rhino3dm as r
from shapely.geometry import Polygon,MultiPoint,box
from shapely.ops import unary_union
R=Path(__file__).resolve().parents[1];S=json.loads((R/'calculo/ESTRUCTURA_RESULTADOS.json').read_text());f=r.File3dm.Read(str(R/'modelos/SELVA_MACARRA_V4_FINAL.3dm'))
byz=collections.defaultdict(list);rows=[]
def add(poly,z,cat,name):
 byz[round(z,4)].append(poly);rows.append({'element':name,'category':cat,'z':round(z,4),'area_m2':poly.area})
for p in S['plates']:add(Polygon(p['outline']),p['z'],'bandejas',p['id'])
for o in f.Objects:
 if o.Attributes.IsInstanceDefinitionObject:continue
 name=o.Attributes.Name or '';la=f.Layers.FindIndex(o.Attributes.LayerIndex).Name
 include=(name=='COM suelo' or la=='07_GALERIAS' or (la=='09_ESCALERAS' and any(t in name for t in ['rellano','meseta intermedia','tramo A','tramo B','Enlace huella','Descansillo enlace'])))
 if not include:continue
 g=o.Geometry
 if not isinstance(g,r.Brep):continue
 pts=[(v.Location.X,v.Location.Y) for v in g.Vertices];poly=MultiPoint(pts).convex_hull
 if poly.area<.001:continue
 z=g.GetBoundingBox().Max.Z
 add(poly,z,'comunes' if name=='COM suelo' else 'galerias' if la=='07_GALERIAS' else 'escaleras',name)
cat={}
for row in rows:cat[row['category']]=cat.get(row['category'],0)+row['area_m2']
union=sum(unary_union(ps).area for ps in byz.values())
res={'method':'Proyeccion horizontal de bandejas, suelos comunes, galerias y cada huella/meseta; union por cota para eliminar duplicados coplanares. No computo urbanistico ni superficie construida normativa.','sum_before_union_m2':sum(cat.values()),'union_by_height_m2':union,'categories_before_union_m2':cat,'bodies_inside_plates_m2':652.8,'ground_communal_m2':149.64,'not_added_again':'652.8m2 de pabellones ya incluidos en bandejas. Ascensores, huecos y espesor de cerramientos requieren criterio de computo independiente.','elements':rows}
(R/'calculo/INVENTARIO_SUPERFICIES.json').write_text(json.dumps(res,indent=2,ensure_ascii=False))
md='# Inventario geométrico de superficies\n\nLas diez bandejas, incluyendo los pabellones y sus terrazas, suman **%.2f m²**. Dentro de ellas hay 652,80 m² de huella de pabellones; no se vuelven a sumar.\n\n'%cat['bandejas']
for k,v in cat.items():md+='- %s: %.2f m² antes de descontar encuentros.\n'%(k,v)
md+='\nLa unión de las proyecciones horizontales por cota da **%.2f m²** de superficies de suelo modeladas. Se suman huellas y mesetas a sus cotas y se eliminan encuentros coplanares; no es una superficie construida urbanística ni acredita los 1.500 m² del enunciado. Los huecos de ascensor, cerramientos y reglas de cómputo requieren un criterio explícito. Tampoco se demuestra que todos los encuentros de circulación sean correctos por medir su área.\n'%union
md+='\nSe entregan todos los elementos en INVENTARIO_SUPERFICIES.json para revisar el cómputo sin ocultar terrazas o escaleras.\n'
(R/'INVENTARIO_SUPERFICIES.md').write_text(md)
print(cat,union,flush=True)
