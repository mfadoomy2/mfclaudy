from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
import rhino3dm as rh
P=Path(__file__).resolve().parents[1]
models=[]
for path in sorted(P.glob('*.3dm')):
 if path.name.startswith('._'):continue
 m=rh.File3dm.Read(str(path));assert m and len(m.Objects)>0
 rec={'archivo':path.name,'objetos':len(m.Objects),'geometria_valida':all(o.Geometry.IsValid for o in m.Objects),'metros':m.Settings.ModelUnitSystem==rh.UnitSystem.Meters,'todos_a_z0':all(abs(o.Geometry.GetBoundingBox().Min.Z)<1e-8 and abs(o.Geometry.GetBoundingBox().Max.Z)<1e-8 for o in m.Objects)}
 assert rec['geometria_valida'] and rec['metros'] and rec['todos_a_z0'];models.append(rec)
assert len(models)==5
imgs=[]
for path in sorted(P.glob('*.png')):
 if path.name.startswith('._'):continue
 im=Image.open(path);sz=im.size;im.verify();imgs.append({'archivo':path.name,'tamano':sz})
assert len(imgs)==5
checks=json.load(open(P/'VERIFICACION.json'));assert all(checks['habitacion']['recorridos_disco80'].values())
assert all(f['puertas_privadas_conectadas_disco90']==4 and f['frentes_ventana_privada_libres_3m']==4 for f in checks['familias'])
(P/'VERIFICACION_ARCHIVOS.json').write_text(json.dumps({'modelos_2d':models,'imagenes':imgs,'nativa_Rhino':'NO ejecutada; relectura rhino3dm'},ensure_ascii=False,indent=2))
files=sorted(p for p in P.rglob('*') if p.is_file() and not any(x.startswith('._') or x=='__pycache__' for x in p.relative_to(P).parts) and p.name!='MANIFIESTO_SHA256.json')
manifest={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(P/'MANIFIESTO_SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
files.append(P/'MANIFIESTO_SHA256.json')
zpath=P.parent/(P.name+'.zip')
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for path in files:z.write(path,str(Path(P.name)/path.relative_to(P)))
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 for rel,sha in manifest.items():assert hashlib.sha256(z.read(P.name+'/'+rel)).hexdigest()==sha
print(json.dumps({'modelos':len(models),'imagenes':len(imgs),'archivos_zip':len(files),'zip_bytes':zpath.stat().st_size,'zip':str(zpath)},ensure_ascii=False))
