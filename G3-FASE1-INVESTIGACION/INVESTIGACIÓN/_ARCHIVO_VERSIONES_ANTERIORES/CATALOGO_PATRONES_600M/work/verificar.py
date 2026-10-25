from pathlib import Path
from PIL import Image,ImageDraw
from pypdf import PdfReader
import json,xml.etree.ElementTree as ET
out=Path(__file__).resolve().parents[1]
qa=out/'work/verificacion'
pdf=PdfReader(out/'CATALOGO_PATRONES_EL_RASTRO_600M.pdf')
assert len(pdf.pages)==65
assert all(abs(float(p.mediabox.width)-595.276)<.1 and abs(float(p.mediabox.height)-841.89)<.1 for p in pdf.pages)
svgs=list(out.glob('P*/P*.svg'));assert len(svgs)==50
for p in svgs:ET.parse(p)
assert len(list(out.glob('P*/FICHA.md')))==25
obs=json.loads((out/'DATOS/observaciones_verificadas.json').read_text())
assert len(obs)==53 and all(o['distance_m']<=600 for o in obs)
for o in obs:
 with Image.open(o['photo']) as im:im.verify()
pages=sorted(qa.glob('p-*.jpg'));assert len(pages)==65,len(pages)
for start in range(0,65,15):
 sheet=Image.new('RGB',(1500,2180),'#dddddd');d=ImageDraw.Draw(sheet)
 for j,p in enumerate(pages[start:start+15]):
  im=Image.open(p);im.thumbnail((480,402))
  x=(j%3)*500+(500-im.width)//2;y=(j//3)*436+20
  sheet.paste(im,(x,y));d.text(((j%3)*500+10,y-16),str(start+j+1),fill='black')
 sheet.save(qa/f'contacto-{start//15+1}.jpg',quality=85)
(qa/'resultado.json').write_text(json.dumps({'paginas':65,'A4_vertical':True,'fichas':25,'SVG_validos':50,'fotos_verificadas':53,'dentro_radio':True},indent=2))
print('VALIDADO: 65 páginas A4, 25 fichas, 50 SVG, 53 imágenes. Contactos generados.')
