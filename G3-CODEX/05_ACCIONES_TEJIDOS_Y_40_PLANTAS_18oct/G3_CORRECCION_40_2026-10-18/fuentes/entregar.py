from pathlib import Path
import json,hashlib,zipfile,shutil,pickle
import rhino3dm as rh
from PIL import Image,ImageDraw,ImageFont
import geometria as G
P=Path(__file__).resolve().parents[1];E=P/'ENTREGA'
reports=json.loads((P/'verificacion/RHINO_NATIVO.json').read_text())
assert len(reports)==41 and all(not (r['invalid'] or r['open_solids'] or r['volume_errors']) for r in reports)
data=pickle.load(open(P/'datos/GEOMETRIA_CORREGIDA.pkl','rb'));assert len(data)==40
assert len({d['floor'].wkb for d in data})==40
expected={f'N{i:02d}{v}' for i in range(1,21) for v in 'AB'}
files=sorted((P/'modelos_listos').glob('N*_CORREGIDA.3dm'));assert {f.stem.split('_')[0] for f in files}==expected
check=[]
for path in files+[P/'modelos_listos/HABITACION_CORREGIDA.3dm']:
 f=rh.File3dm.Read(str(path));assert f and len(f.Views)==1 and len(f.NamedViews)==2
 assert f.Settings.ModelUnitSystem==rh.UnitSystem.Meters
 invalid=[];bounds=[]
 for ob in f.Objects:
  g=ob.Geometry;bb=g.GetTightBoundingBox();bounds.append(bb)
  assert g.IsValid,(path.name,ob.Attributes.Name)
  assert not isinstance(g,(rh.Brep,rh.Extrusion)) or g.IsSolid,(path.name,ob.Attributes.Name)
  assert bb.Min.Z>=-.201 and bb.Max.Z<=3.151,(path.name,ob.Attributes.Name,bb.Min.Z,bb.Max.Z)
  assert not any(term in ob.Attributes.Name.lower() for term in ['bicicleta','tendedero','pilar aislado'])
 floor=[o for o in f.Objects if o.Attributes.Name.startswith('forjado acabado')];assert len(floor)==1 and abs(floor[0].Geometry.GetTightBoundingBox().Max.Z)<.00001
 code=path.stem.split('_')[0]
 for suffix in ['PLANTA','AXON']:
  im=P/'vistas'/(code+'_'+suffix+'.png');assert im.exists()
  with Image.open(im) as picture:picture.verify()
 # The final native file was written after its model source, in the same validation pass as its images.
 src=P/'modelos'/path.name if code!='HABITACION' else P/'HABITACION_CORREGIDA.3dm'
 assert path.stat().st_mtime>=src.stat().st_mtime,(code,'outdated native file')
 check.append({'file':path.name,'objects':len(f.Objects),'invalid':0,'open_solids':0,'initial_views':1,'named_views':2,'floor_top_z':0})
master=rh.File3dm.Read(str(P/'CATALOGO_40_CORREGIDAS_COTA0.3dm'))
assert master and len(master.NamedViews)==41
assert len(master.Objects)==sum(c['objects'] for c in check if c['file'].startswith('N'))+40
floors=[o for o in master.Objects if o.Attributes.Name.startswith('forjado acabado')];assert len(floors)==40
assert all(abs(o.Geometry.GetTightBoundingBox().Max.Z)<.00001 for o in floors)
for i,a in enumerate(floors):
 A=a.Geometry.GetTightBoundingBox()
 for b in floors[i+1:]:
  B=b.Geometry.GetTightBoundingBox()
  assert A.Max.X<B.Min.X or B.Max.X<A.Min.X or A.Max.Y<B.Min.Y or B.Max.Y<A.Min.Y
for suffix in ['PLANTA','AXON']:
 for page in range(2):
  sheet=Image.new('RGB',(2500,1900),(248,246,240));draw=ImageDraw.Draw(sheet)
  try:font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',24)
  except:font=ImageFont.load_default()
  for j,path in enumerate(files[page*20:(page+1)*20]):
   code=path.stem.split('_')[0];im=Image.open(P/'vistas'/(code+'_'+suffix+'.png')).convert('RGB');im.thumbnail((490,420));x=(j%5)*500+(500-im.width)//2;y=(j//5)*475+35;sheet.paste(im,(x,y));draw.text(((j%5)*500+18,(j//5)*475+6),code,fill=(50,72,58),font=font)
  sheet.save(P/'vistas'/('CONTACTO_'+suffix+'_'+str(page+1)+'.jpg'),quality=94)
summary={'units':40,'bedrooms':160,'distinct_plan_shapes':40,'native_files':check,'catalog_objects':len(master.Objects),'catalog_named_views':41,'all_floors_z':0,'native_validation_count':41,'native_volume_errors':0,'claims_not_covered':['solar en parcela','calculo estructural','cumplimiento normativo','proyecto de ejecucion']}
(P/'verificacion/ENTREGA_COMPROBADA.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
assert not E.exists(),'La instantánea de entrega ya existe; no se sustituye automáticamente.'
for folder in ['modelos','vistas','datos','fuentes','verificacion']:(E/folder).mkdir(parents=True,exist_ok=True)
for path in files:shutil.copyfile(path,E/'modelos'/path.name)
shutil.copyfile(P/'modelos_listos/HABITACION_CORREGIDA.3dm',E/'HABITACION_CORREGIDA.3dm')
for name in ['CATALOGO_40_CORREGIDAS_COTA0.3dm','LEER_PRIMERO.md']:shutil.copyfile(P/name,E/name)
for folder in ['datos','vistas']:
 for path in (P/folder).iterdir():
  if not path.is_file() or path.name.startswith('._') or path.name in ['GEOMETRIA_MUESTRA.pkl','DIAGNOSTICO_N01A.png']:continue
  shutil.copyfile(path,E/folder/path.name)
for path in (P/'fuentes').glob('*.py'):
 if path.name=='unir_prueba.py' or path.name.startswith('._'):continue
 shutil.copyfile(path,E/'fuentes'/path.name)
for name in ['ESPACIO_FINAL.json','MODELOS.json','RHINO_NATIVO.json','CATALOGO_NATIVO.json','ENTREGA_COMPROBADA.json']:
 shutil.copyfile(P/'verificacion'/name,E/'verificacion'/name)
manifest={str(f.relative_to(E)):hashlib.sha256(f.read_bytes()).hexdigest() for f in E.rglob('*') if f.is_file() and not any(part.startswith('._') or part=='__pycache__' for part in f.relative_to(E).parts)}
(E/'MANIFIESTO_SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
dest=P/'G3_40_UNIDADES_CORREGIDAS.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(E.rglob('*')):
  if f.is_file() and not any(part.startswith('._') or part=='__pycache__' for part in f.relative_to(E).parts):z.write(f,'G3_40_UNIDADES_CORREGIDAS/'+str(f.relative_to(E)))
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 for name,h in manifest.items():assert hashlib.sha256(z.read('G3_40_UNIDADES_CORREGIDAS/'+name)).hexdigest()==h
result={'zip':str(dest),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'files':len(manifest)+1,'units':40,'bedrooms':160,'native_views_catalog':41,'gross_range_m2':[122.18,123.61]}
(P/'verificacion/PAQUETE_FINAL.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result),flush=True)
