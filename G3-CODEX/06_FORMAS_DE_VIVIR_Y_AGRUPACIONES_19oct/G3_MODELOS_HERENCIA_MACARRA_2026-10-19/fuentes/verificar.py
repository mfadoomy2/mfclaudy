from pathlib import Path
import rhino3dm as r,json,hashlib,shutil
P=Path(__file__).resolve().parents[1]
models=sorted(p for p in (P/'modelos').glob('*.3dm') if not p.name.startswith('._'))
assert len(models)==23,len(models)
report=[]
for path in models:
 m=r.File3dm.Read(str(path));assert m and all(o.Geometry.IsValid for o in m.Objects),path
 beds=[];floors=[];extrusions=0
 for ob in m.Objects:
  if isinstance(ob.Geometry,r.Extrusion):
   extrusions+=1;assert ob.Geometry.IsSolid,(path,ob.Attributes.Name)
  if 'colchon 125x200' in ob.Attributes.Name:beds.append(ob.Geometry.GetBoundingBox().Min.Z)
  if 'Suelo continuo a cota 0' in ob.Attributes.Name:floors.append(ob.Geometry.GetBoundingBox().Max.Z)
 if path.name.startswith('E'):
  assert beds and all(abs(z-4.32)<.002 for z in beds),(path,beds)
  assert floors and all(abs(z-4.2)<.002 for z in floors)
 else:
  assert all(abs(z-.12)<.002 for z in beds),(path,beds)
 report.append({'archivo':path.name,'objetos':len(m.Objects),'extrusiones_solidas':extrusions,'invalidos':0,'suelo_vivienda_z':floors,'colchones':len(beds),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
st=json.loads((P/'verificacion/GEOMETRIA_3D.json').read_text());assert len(st)==11
for a in st:
 if a['sitio']:
  assert a['PB_viviendas']==0 and a['cota_primera_vivienda']==4.2
  assert a['caja_ante_escalera_retirada'] and all(a['recorridos_PB90'].values())
  assert a['invasion_parcela_m2']<.001
out={'modelos':report,'ocho_modelos_aislados':8,'ensayos_parcela':3,'copias_interior':11,'catalogo':1,'capacidad_ensayos':'8 residentes en cada ensayo; no son tres edificios completos de 40','regla_PB':'Sin viviendas; servicios integrados en borde, sin caja ante escalera','alcance':'Geometria valida, extrusiones cerradas, cotas y comprobacion parcial de recorridos; no certifica normativa, estructura o iluminacion.'}
(P/'verificacion/CONTROL_FINAL.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));shutil.copyfile(P/'modelos/E02_COMUNA_INTERIOR.3dm',P/'verificacion/E02_REVISION_NATIVA.3dm')
print('VALIDADOS',len(models),'modelos; PB sin dormitorios y sin caja ante escalera; 3 ensayos con rutas PB90 conectadas')
