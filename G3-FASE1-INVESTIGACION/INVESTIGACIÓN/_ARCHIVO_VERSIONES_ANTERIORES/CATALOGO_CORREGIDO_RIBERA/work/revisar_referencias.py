from pathlib import Path
import hashlib,json,subprocess
from pypdf import PdfReader
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw
from collections import Counter
R=Path('/Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS')
O=Path('/Volumes/T7/G3 Proyectos/INVESTIGACIÓN/CATALOGO_EDITORIAL_RIBERA/work/referencias')
O.mkdir(parents=True,exist_ok=True)
inventory=[]; shots=[]; seen=set()
files=sorted(p for p in R.rglob('*.pdf') if not p.name.startswith('._'))
def render(pair):
 i,f=pair
 d=PdfReader(f); item={'id':i,'path':str(f),'pages':len(d.pages),'titles':[p.extract_text()[:180] for p in d.pages]}
 full=f.parent.name=='oviedo' or f.name=='REFUGIO_CLIMATICO_COMPENDIO_ANALITICO.pdf'
 count=len(d.pages) if full else 1
 subprocess.run(['/Users/adam/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/bin/pdftoppm','-scale-to','440','-png','-f','1','-l',str(count),str(f),str(O/f'r{i:03}')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 return item
with ThreadPoolExecutor(max_workers=4) as pool:
 inventory=list(pool.map(render,enumerate(files)))
for item in inventory:
 i=item['id'];f=Path(item['path'])
 for path in sorted(O.glob(f'r{i:03}-*.png')):
  j=int(path.stem.split('-')[-1])-1
  im=Image.open(path).convert('RGB');digest=hashlib.sha256(im.tobytes()).hexdigest()
  if digest in seen:continue
  seen.add(digest);name=path.name;shots.append({'file':name,'ref':i,'page':j+1,'path':str(f)})
for start in range(0,len(shots),24):
 sheet=Image.new('RGB',(1440,1800),'#dddddd');dr=ImageDraw.Draw(sheet)
 for k,s in enumerate(shots[start:start+24]):
  im=Image.open(O/s['file']);im.thumbnail((230,402));x=5+(k%6)*240;y=20+(k//6)*450
  sheet.paste(im,(x,y));dr.text((x,y-15),s['file'],fill='black')
 sheet.save(O/f'contacto_{start//24+1:02}.jpg',quality=88)
(O/'inventario.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
(O/'vistas.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2))
print({'files':len(files),'pages':sum(x['pages'] for x in inventory),'unique_views':len(shots),'contact_sheets':(len(shots)+23)//24})
