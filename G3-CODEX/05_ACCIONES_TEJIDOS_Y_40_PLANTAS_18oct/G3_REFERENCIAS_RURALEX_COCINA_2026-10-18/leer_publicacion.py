from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json
import pymupdf
from PIL import Image,ImageDraw
P=Path(__file__).parent/'lectura_privada';P.mkdir(exist_ok=True)
# Public page assets of the 96-page viewer; original PDF has no download link.
base='https://d1uiew9hysv4w7.cloudfront.net/935496/2051536/txt/2051536_{}_1200.webp'
def read(n):
 try:
  f=P/f'{n:03}.webp'
  if not f.exists():f.write_bytes(urllib.request.urlopen(base.format(n),timeout=30).read())
  Image.open(f).convert('RGB').save(P/f'{n:03}.png');return [n,'ok']
 except Exception as e:return [n,str(e)]
with ThreadPoolExecutor(max_workers=6) as pool:
 result=list(pool.map(read,range(1,97)))
(P/'registro.json').write_text(json.dumps(result,indent=2));print(result,flush=True)
for start in range(1,97,16):
 sheet=Image.new('RGB',(2000,2000),'white');draw=ImageDraw.Draw(sheet)
 for n in range(start,min(start+16,97)):
  f=P/f'{n:03}.png'
  if not f.exists():continue
  im=Image.open(f);im.thumbnail((490,470));i=n-start;x=i%4*500;y=i//4*500;sheet.paste(im,(x,y+22));draw.text((x+8,y+5),str(n),fill='black')
 sheet.save(P/f'CONTACTO_{start:03}.jpg')
print('LECTURA_LISTA',flush=True)
