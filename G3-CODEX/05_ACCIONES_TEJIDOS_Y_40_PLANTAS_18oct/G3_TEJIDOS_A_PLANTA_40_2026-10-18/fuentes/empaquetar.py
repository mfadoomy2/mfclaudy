from pathlib import Path
import hashlib,json,zipfile
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parents[1];root=P.parent
first=root/'G3_ATLAS_40_PLANTAS_2026-10-18'
# A readable two-example preview. All 40 alternatives remain in the atlas and separate files.
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',28)
preview=Image.new('RGB',(2100,1550),'#faf8f0');dr=ImageDraw.Draw(preview)
for j,code in enumerate(['N02A','N09B']):
 x=j*1050;dr.text((x+25,18),code+' / tejido → planta',font=font,fill='#253d35')
 for suffix,yy,hh in [('TRAZA',65,480),('PLANTA',555,950)]:
  im=Image.open(P/'plantas'/f'{code}_{suffix}.png').convert('RGB');im.thumbnail((1020,hh));preview.paste(im,(x+(1050-im.width)//2,yy+(hh-im.height)//2))
preview.save(P/'output/VISTA_DIAGRAMA_PLANTA.jpg',quality=94)
qa={'graphic_review':'All 88 pages rendered and inspected via 4 contact sheets; individual plans and traces also inspected','count_new':40,'count_preserved':40,'cad_new':40,'svg_main_new':40,'scope':'exploratory plans, not validated building design','visual_review_date':'2026-10-18'}
(P/'verificacion/REVISION_GRAFICA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
package=root/'G3_80_PLANTAS_2026-10-18.zip';manifest={};files=[]
for prefix,folder in [('01_PRIMERA_SERIE_40',first),('02_TEJIDOS_A_PLANTA_40',P)]:
 for q in sorted(folder.rglob('*')):
  if not q.is_file() or q.name.startswith('._') or '__pycache__' in q.parts or q.name=='contacto_borrador.jpg':continue
  name=prefix+'/'+q.relative_to(folder).as_posix();files.append((q,name));manifest[name]={'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}
readme='''# 80 plantas / dos series conservadas

01_PRIMERA_SERIE_40: primer atlas de 20 familias de agregación con dos variantes, 48 páginas.
02_TEJIDOS_A_PLANTA_40: segunda serie adicional, 20 propuestas × 2 variantes, 88 páginas. Cada planta está precedida por su diagrama de origen y los ajustes dimensionales.

Abrir primero 02_TEJIDOS_A_PLANTA_40/output/pdf/G3_40_PLANTAS_DESDE_TEJIDOS_A3.pdf.

Incluye 80 planos principales en PNG/SVG, 80 bases de contornos Rhino 2D, diagramas, datos, scripts y comprobaciones. Los SVG son los editables gráficos más completos. Los Rhino no son modelos 3D ni incluyen todos los símbolos del SVG.

Ambas series son exploratorias y superan el objetivo previo de superficie. La segunda ocupa aproximadamente 208–260 m² por unidad y produce exceso de recorridos. No se acredita ajuste a parcela, luz, estructura, accesibilidad ni normativa. Consultar LEEME.md de cada serie.

Las pruebas intermedias de traducción no se incluyen como propuestas adicionales. MANIFIESTO_SHA256.json permite verificar los archivos empaquetados. No se incluyen metadatos AppleDouble.
'''
with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 z.writestr('LEER_PRIMERO.md',readme);z.writestr('MANIFIESTO_SHA256.json',json.dumps(manifest,indent=2))
 for q,name in files:z.write(q,name)
with zipfile.ZipFile(package) as z:
 assert z.testzip() is None
 for name,meta in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==meta['sha256']
 names=z.namelist();mainpng=[n for n in names if n.endswith('_PLANTA.png')];mainsvg=[n for n in names if n.endswith('_PLANTA.svg')];cad=[n for n in names if n.endswith('_PLANTA_2D.3dm')]
 assert len(mainpng)==len(mainsvg)==len(cad)==80
report={'zip':str(package),'bytes':package.stat().st_size,'files':len(files)+2,'main_plan_png':len(mainpng),'main_plan_svg':len(mainsvg),'cad_2d':len(cad),'crc_test':'passed','sha256_all_files':'passed','zip_sha256':hashlib.sha256(package.read_bytes()).hexdigest()}
(P/'verificacion/PAQUETE_FINAL.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
