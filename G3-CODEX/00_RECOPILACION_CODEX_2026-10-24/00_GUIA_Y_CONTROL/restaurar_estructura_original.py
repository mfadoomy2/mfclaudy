"""Reconstruct a new copy of the original project layout from this archive.
Never overwrites the source project or an existing destination.
"""
from pathlib import Path
import argparse,json,shutil,hashlib
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--destination',required=True,type=Path)
p.add_argument('--include-external',action='store_true')
a=p.parse_args();archive=Path(__file__).resolve().parents[1]
if a.destination.exists():p.error('La carpeta de destino debe ser nueva; no se sobrescribe nada.')
rows=json.loads((archive/'00_GUIA_Y_CONTROL/INVENTARIO_ARCHIVOS_SHA256.json').read_text())
a.destination.mkdir(parents=True)
for row in rows:
 if row['origin']=='project_root':rel=Path(row['source_relative'])
 elif a.include_external:rel=Path('__FUENTES_EXTERNAS__')/Path(*Path(row['destination']).parts[1:])
 else:continue
 if rel.is_absolute() or '..' in rel.parts:raise ValueError('Ruta no valida: '+str(rel))
 source=archive/row['destination'];target=a.destination/rel;target.parent.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(source,target)
 h=hashlib.sha256()
 with target.open('rb') as f:
  for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
 if h.hexdigest()!=row['sha256']:raise RuntimeError('Error de integridad: '+str(target))
print('Copia restaurada y verificada:',a.destination)
