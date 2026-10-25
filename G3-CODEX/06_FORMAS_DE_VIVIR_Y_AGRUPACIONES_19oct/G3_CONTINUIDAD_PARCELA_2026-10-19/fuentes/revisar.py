from pathlib import Path
import pymupdf as fitz
from PIL import Image,ImageOps,ImageDraw
import json
P=Path(__file__).resolve().parents[1];doc=fitz.open(P/'output/pdf/G3_PLANTAS_CORREGIDAS_Y_PRUEBA_PARCELA.pdf');dest=P/'verificacion/pdf';dest.mkdir(exist_ok=True)
assert len(doc)==52
for i,p in enumerate(doc):
 assert abs(p.rect.width-1190.55)<1 and abs(p.rect.height-841.89)<1
 pix=p.get_pixmap(matrix=fitz.Matrix(.6,.6),alpha=False);pix.save(dest/f'{i+1:02d}.png')
for start in [0,16,32,48]:
 contact=Image.new('RGB',(1600,1200),'#e8e5de');d=ImageDraw.Draw(contact)
 for n in range(start,min(start+16,len(doc))):
  im=Image.open(dest/f'{n+1:02d}.png');im.thumbnail((395,273));x=((n-start)%4)*400;y=((n-start)//4)*300;contact.paste(im,(x,y));d.text((x+8,y+278),f'{n+1:02d}',fill='black')
 contact.save(dest/f'CONTACTO_{start+1:02d}.png')
for n in [3,4,7,22,25,32,33]:doc[n-1].get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False).save(dest/f'DETALLE_{n:02d}.png')
print('PDF',len(doc),'pages; all rendered; key pages high resolution')
