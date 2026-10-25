from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parents[1]
files=[]
for p in sorted(R.rglob('*')):
 if not p.is_file() or p.name.startswith('._') or p.suffix in ['.rhl','.zip','.blend1','.3dmbak']:continue
 if p.name in ['UNIDAD_P02_COMPLETA_EDITABLE.3dm','MANIFIESTO.json','diagnosticar_modo.py','modo.json']:continue
 if '__pycache__' in p.parts or 'historico' in p.parts:continue
 files.append(p)
manifest=[]
for p in files:manifest.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
m=R/'MANIFIESTO.json';m.write_text(json.dumps(manifest,indent=2));files.append(m)
z=R/'UNIDAD_P02_DETALLADA_ENTREGA.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as f:
 for p in files:f.write(p,str(p.relative_to(R)))
with zipfile.ZipFile(z) as f:assert f.testzip() is None
print('ZIP_VERIFICADO',len(files),z.stat().st_size,flush=True)
