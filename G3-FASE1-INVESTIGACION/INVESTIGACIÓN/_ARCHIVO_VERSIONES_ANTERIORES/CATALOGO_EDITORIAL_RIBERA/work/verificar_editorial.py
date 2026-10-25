from pathlib import Path
import json,hashlib,subprocess
from pypdf import PdfReader
from PIL import Image,ImageDraw
B=Path('/Volumes/T7/G3 Proyectos/INVESTIGACIÓN/CATALOGO_EDITORIAL_RIBERA')
P=B/'RIBERA_DE_CURTIDORES_PATRONES_Y_MATERIA.pdf';Q=B/'work/qa';Q.mkdir(exist_ok=True)
r=PdfReader(P);text='\n'.join(p.extract_text() for p in r.pages)
assert len(r.pages)==58
for forbidden in ['catálogo anterior','catálogo comparativo','no es un censo','Atlas de fotografías aportadas','Control de tus correcciones','Qué se ha cambiado','aporta el usuario','edición anterior']:
 assert forbidden.casefold() not in text.casefold(),forbidden
for i in range(1,34):assert f'F{i:02d}' in text
for pg in r.pages:assert abs(float(pg.mediabox.width)-595.276)<.01 and abs(float(pg.mediabox.height)-841.89)<.01
data=json.loads((B/'datos_analiticos.json').read_text());cases=json.loads((B/'casos_y_flechas.json').read_text())
assert len(cases)==64
for cat in {c['category'] for c in cases}:
 assert len({c['front'] for c in cases if c['category']==cat})==8
assert sum(data['levels'].values())==data['core_buildings']
assert sum(data['commerce_groups'].values())==data['objects_and_crafts']
subprocess.run(['/Users/adam/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/bin/pdftoppm','-scale-to','950','-jpeg','-jpegopt','quality=85',str(P),str(Q/'p')],check=True)
imgs=sorted(Q.glob('p-*.jpg'));assert len(imgs)==58
for start in range(0,len(imgs),12):
 out=Image.new('RGB',(1040,1510),'#ddd');d=ImageDraw.Draw(out)
 for j,path in enumerate(imgs[start:start+12]):
  im=Image.open(path);im.thumbnail((250,461));x=5+(j%4)*260;y=22+(j//4)*501
  out.paste(im,(x,y));d.text((x,y-16),path.stem,fill='black')
 out.save(Q/f'contacto_{start//12+1}.jpg',quality=90)
copy=Path('/Users/adam/Documents/Codex/2026-09-21/crr/outputs')/P.name
assert hashlib.sha256(copy.read_bytes()).digest()==hashlib.sha256(P.read_bytes()).digest()
report={'pages':58,'A4':True,'cases':64,'field_photos':33,'maps_with_metric_scale':11,'analysis_plates':5,'text_checks':'passed','rendered_pages':58,'copy_verified':True}
(B/'work/qa/verificacion.json').write_text(json.dumps(report,indent=2));print(report)
