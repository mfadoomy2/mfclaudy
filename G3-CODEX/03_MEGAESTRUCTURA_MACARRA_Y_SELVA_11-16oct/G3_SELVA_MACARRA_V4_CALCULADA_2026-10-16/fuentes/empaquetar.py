from pathlib import Path
import json,hashlib,zipfile,time
R=Path(__file__).resolve().parents[1]
exclude={'exportar_render.py','diagnostico_vista.py','api_mallas.json','PREVIA_V4.png'}
files=[]
for p in sorted(R.rglob('*')):
 if not p.is_file() or p.name.startswith('._') or p.name in exclude:continue
 if any(x in p.parts for x in ['__pycache__','historico']):continue
 if p.suffix in ['.zip','.rhl','.blend1','.3dmbak']:continue
 if p.name=='MANIFIESTO.json':continue
 files.append(p)
manifest=[]
for p in files:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 manifest.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':h.hexdigest()})
m=R/'MANIFIESTO.json';m.write_text(json.dumps({'files':manifest,'note':'Excluye bloqueos, metadatos AppleDouble, versiones previas y fallos historicos.'},indent=2));files.append(m)
z=R/'SELVA_MACARRA_V4_ENTREGA.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as f:
 for p in files:f.write(p,str(p.relative_to(R)))
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 assert len(f.namelist())==len(files)
print('ZIP VERIFICADO',len(files),z.stat().st_size,flush=True)
