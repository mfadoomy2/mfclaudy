from pathlib import Path
import json,math
import fitz
from PIL import Image,ImageOps,ImageDraw
import rhino3dm as rh
P=Path(__file__).resolve().parents[1];V=P/'verificacion';T=V/'paginas';T.mkdir(exist_ok=True)
pdf=P/'output/pdf/G3_PLANTAS_NUEVAS_Y_DIAGRAMAS_CORREGIDOS.pdf';d=fitz.open(pdf);assert len(d)==47
for i,p in enumerate(d):
 assert abs(p.rect.width-1190.551)<1 and abs(p.rect.height-841.89)<1
 text=p.get_text();assert text.strip() and '\ufffd' not in text
 pix=p.get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False);pix.save(T/f'{i+1:02d}.png')
for start in range(0,47,12):
 sheet=Image.new('RGB',(4*600,3*455),'#dedfd7');draw=ImageDraw.Draw(sheet)
 for j,i in enumerate(range(start,min(start+12,47))):
  im=Image.open(T/f'{i+1:02d}.png');im.thumbnail((580,415));x=(j%4)*600+(600-im.width)//2;y=(j//4)*455+25
  sheet.paste(im,(x,y));draw.text(((j%4)*600+15,(j//4)*455+5),f'PAGINA {i+1:02d}',fill='#263d35')
 sheet.save(V/f'CONTACTO_{start//12+1}.jpg',quality=90)
models=[]
for p in sorted((P/'modelos_2d').glob('*.3dm')):
 if p.name.startswith('._'):continue
 m=rh.File3dm.Read(str(p));assert m and all(o.Geometry.IsValid for o in m.Objects)
 assert m.Settings.ModelUnitSystem==rh.UnitSystem.Meters
 assert all(abs(o.Geometry.GetBoundingBox().Min.Z)<1e-8 and abs(o.Geometry.GetBoundingBox().Max.Z)<1e-8 for o in m.Objects)
 models.append({'archivo':p.name,'objetos':len(m.Objects),'geometria_valida':True,'metros':True,'z0':True})
assert len(models)==8
ind=json.load(open(V/'INDICE_Y_PROCEDENCIA.json'));assert len(ind['fuentes_originales'])==18 and len(ind['plantas_nuevas'])==8
summary={'pdf':str(pdf),'paginas':len(d),'formato':'A3 horizontal','diagramas_originales':18,'diagramas_nuevos_lectura':8,'plantas_nuevas_corregidas':8,'modelos':models,'renderizadas':47,'plantas_anteriores_incluidas':False,'revision_visual':'PENDIENTE inspeccion de contactos y paginas clave'}
(V/'REVISION_PDF.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in summary.items() if k!='modelos'},ensure_ascii=False))
