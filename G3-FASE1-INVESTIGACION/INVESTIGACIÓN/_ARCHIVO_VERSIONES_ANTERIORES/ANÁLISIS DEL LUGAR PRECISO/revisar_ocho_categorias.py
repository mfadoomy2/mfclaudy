from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw
from pypdf import PdfReader
B=Path(__file__).parent;O=B/'CATEGORIAS_01_08';O.mkdir(exist_ok=True);R=O/'REFERENCIAS';R.mkdir(exist_ok=True)
S=B.parent/'REFERENCIAS/REFUGIO_CLIMATICO/ANALISIS_FINALES_REFUGIO_CLIMATICO'
POP='/Users/adam/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/bin/pdftoppm'
manifest=[]
for folder in sorted(S.iterdir()):
 if not folder.is_dir() or folder.name[:2] not in [f'{i:02}' for i in range(1,9)]:continue
 images=[]
 for f in sorted(folder.glob('*.pdf')):
  if f.name.startswith('._'):continue
  pdf=PdfReader(f);prefix=R/(folder.name[:2]+'_'+f.stem)
  prefix.with_suffix('.txt').write_text('\n\n'.join(f'PÁGINA {i+1}\n'+p.extract_text() for i,p in enumerate(pdf.pages)),encoding='utf-8')
  subprocess.run([POP,'-f','2','-scale-to','800','-jpeg',str(f),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  ims=sorted(R.glob(prefix.name+'-*.jpg'));images+=ims
  manifest.append({'category':folder.name,'source':str(f),'pages':len(pdf.pages),'rendered':len(ims)})
 for start in range(0,len(images),12):
  board=Image.new('RGB',(1200,1380),'#ddd');draw=ImageDraw.Draw(board)
  for j,path in enumerate(images[start:start+12]):
   im=Image.open(path);im.thumbnail((290,420));x=j%4*300;y=j//4*460;board.paste(im,(x,y+30));draw.text((x+2,y+3),path.stem[:39],fill='black')
  board.save(R/f'CONTACTO_{folder.name[:2]}_{start//12+1}.jpg')
 print(folder.name,len(images),flush=True)
(O/'REFERENCIAS_ANALIZADAS.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(O/'ESTADO.json').write_text(json.dumps({'estado':'referencias leidas y renderizadas','categorias_previstas':8,'completadas':[]}))
