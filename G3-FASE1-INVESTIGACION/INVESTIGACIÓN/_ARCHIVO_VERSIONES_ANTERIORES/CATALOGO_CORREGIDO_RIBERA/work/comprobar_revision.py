from pathlib import Path
from PIL import Image,ImageDraw
from pypdf import PdfReader
import json,hashlib
base=Path('/Volumes/T7/G3 Proyectos/INVESTIGACIÓN/CATALOGO_CORREGIDO_RIBERA')
pdf=base/'CATALOGO_CORREGIDO_RIBERA.pdf'
r=PdfReader(pdf)
assert len(r.pages)==54
assert all(abs(float(p.mediabox.width)-595.276)<.01 and abs(float(p.mediabox.height)-841.89)<.01 for p in r.pages)
text='\n'.join(p.extract_text() for p in r.pages)
for i in range(1,34): assert f'F{i:02d}' in text
cases=json.loads((base/'casos_y_flechas.json').read_text())
assert len(cases)==64
for cat in {c['category'] for c in cases}:
    cc=[c for c in cases if c['category']==cat]
    assert len(cc)==len({c['front'] for c in cc})==8
photos=sorted((base/'work/qa').glob('p-*.jpg'))
for start in range(0,len(photos),12):
    sheet=Image.new('RGB',(1000,1450),'#dddddd'); d=ImageDraw.Draw(sheet)
    for j,path in enumerate(photos[start:start+12]):
        im=Image.open(path); im.thumbnail((242,444)); x=6+(j%4)*250;y=20+(j//4)*480
        sheet.paste(im,(x,y)); d.text((x,y-15),path.stem,fill='black')
    sheet.save(base/f'work/qa/contacto_{start//12+1}.jpg',quality=90)
copy=Path('/Users/adam/Documents/Codex/2026-09-21/crr/outputs')/pdf.name
assert hashlib.sha256(pdf.read_bytes()).digest()==hashlib.sha256(copy.read_bytes()).digest()
print(json.dumps({'pages':len(r.pages),'A4':True,'field_photos':33,'case_observations':len(cases),'fronts':len({c['front'] for c in cases}),'rendered_pages':len(photos),'copy_hash_equal':True}))
