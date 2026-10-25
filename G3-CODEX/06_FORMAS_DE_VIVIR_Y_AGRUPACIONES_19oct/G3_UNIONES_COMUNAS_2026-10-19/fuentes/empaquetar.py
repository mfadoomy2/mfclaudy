from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
import rhino3dm as rh
P=Path(__file__).resolve().parents[1]
check=json.load(open(P/'VERIFICACION.json'))
assert len(check['alternativas'])==4
assert all(check['habitacion']['recorridos_disco80'].values())
for a in check['alternativas']:
 assert a['puertas_alcanzables_disco90']==8 and a['bow_exterior_franja3m']==8
 assert a['solape_privados_m2']==a['muebles_fuera_suelo_m2']==a['solape_muebles_comunes_m2']==0
models=[]
for p in sorted(P.glob('*_PLANTA.3dm')):
 if p.name.startswith('._'):continue
 m=rh.File3dm.Read(str(p));assert m and all(o.Geometry.IsValid for o in m.Objects)
 assert m.Settings.ModelUnitSystem==rh.UnitSystem.Meters
 assert all(abs(o.Geometry.GetBoundingBox().Min.Z)<1e-8 and abs(o.Geometry.GetBoundingBox().Max.Z)<1e-8 for o in m.Objects)
 arcs=sum(o.Geometry.ObjectType==rh.ObjectType.Curve and 'VIDRIO_ARCO' in next((l.Name for l in m.Layers if l.Index==o.Attributes.LayerIndex),'') for o in m.Objects)
 assert arcs==8
 models.append({'archivo':p.name,'objetos':len(m.Objects),'arcos_bow':arcs,'geometria_valida':True,'metros':True,'cota':0})
assert len(models)==4
imgs=[]
for p in sorted(P.glob('*.png')):
 if p.name.startswith('._') or p.name=='DEBUG.png':continue
 im=Image.open(p);wh=im.size;im.verify();imgs.append({'archivo':p.name,'dimensiones_px':wh})
assert len(imgs)==8,len(imgs)
(P/'VERIFICACION_ARCHIVOS.json').write_text(json.dumps({'modelos':models,'imagenes':imgs,'revision_nativa_Rhino':False,'revision_relectura_rhino3dm':True},ensure_ascii=False,indent=2))
# Exclude intermediate diagnostics and exFAT sidecars from the actual delivery.
exclude={'DEBUG.png','DATOS_INICIALES.json','MANIFIESTO_SHA256.json'}
files=sorted(p for p in P.rglob('*') if p.is_file() and p.name not in exclude and not any(x.startswith('._') or x=='__pycache__' for x in p.relative_to(P).parts))
manifest={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(P/'MANIFIESTO_SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
files.append(P/'MANIFIESTO_SHA256.json');zp=P.parent/(P.name+'.zip')
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,str(Path(P.name)/p.relative_to(P)))
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 assert all(not Path(n).name.startswith('._') for n in z.namelist())
 for rel,h in manifest.items():assert hashlib.sha256(z.read(P.name+'/'+rel)).hexdigest()==h
print(json.dumps({'zip':str(zp),'archivos':len(files),'bytes':zp.stat().st_size,'modelos':models},ensure_ascii=False))
