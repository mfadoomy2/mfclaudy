from pathlib import Path
import json,hashlib,zipfile
import rhino3dm as rh
import pymupdf
P=Path(__file__).resolve().parents[1]
models=sorted(p for p in (P/'modelos_2d').glob('*.3dm') if not p.name.startswith('._'));assert len(models)==16,len(models)
report=[]
for path in models:
 m=rh.File3dm.Read(str(path));assert m and len(m.Objects)>0
 for o in m.Objects:
  assert o.Geometry.IsValid,path
  b=o.Geometry.GetBoundingBox();assert abs(b.Min.Z)<1e-8 and abs(b.Max.Z)<1e-8,path
 report.append({'archivo':path.name,'objetos_validos':len(m.Objects),'z':0,'bytes':path.stat().st_size})
pdf=P/'output/pdf/G3_PLANTAS_CORREGIDAS_Y_PRUEBA_PARCELA.pdf';d=pymupdf.open(pdf);assert len(d)==52
assert all(p.get_text().strip() for p in d)
a=json.loads((P/'verificacion/CONTROL_GEOMETRICO.json').read_text())['plantas'];assert sum(x['accesos_dormitorios_disco90'] for x in a)==52;assert sum(x['accesos_banos_disco90'] for x in a)==26
(P/'verificacion/CONTROL_ARCHIVOS.json').write_text(json.dumps({'modelos':report,'pdf_paginas':len(d),'pdf_bytes':pdf.stat().st_size,'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'control':'Geometria valida y Z=0 por rhino3dm; PDF renderizado y revisado. No revision visual nativa Rhino.'},ensure_ascii=False,indent=2))
keep_sources=['geometria.py','laminas.py','parcela.py','laminas_parcela.py','documento.py','lengua.py','revisar.py','empaquetar.py','BASE_ANTES.py','ANTECEDENTES.json','PARCELA_REAL.geojson','CONTEXTO_CATASTRAL.geojson']
files=[P/'LEEME.md',pdf]+models
files += [p for p in (P/'laminas').iterdir() if not p.name.startswith('._') and p.suffix in ['.svg','.png']]
files += [P/'fuentes'/n for n in keep_sources]
files += [p for p in (P/'fuentes/antecedentes').iterdir() if not p.name.startswith('._')]
files += [P/'verificacion'/n for n in ['CONTROL_GEOMETRICO.json','ENCAJE_PARCELA.json','CONTROL_ARCHIVOS.json','INDICE_ACTUAL.json']]
manifest=[{'archivo':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files]
(P/'MANIFIESTO.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));files.append(P/'MANIFIESTO.json')
out=P/'G3_REVISION_PLANTAS_Y_PARCELA.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for f in files:z.write(f,f.relative_to(P))
with zipfile.ZipFile(out) as z:assert z.testzip() is None;assert len(z.namelist())==len(files)
print(json.dumps({'modelos_2d':len(models),'paginas':len(d),'zip_archivos':len(files),'zip_bytes':out.stat().st_size,'pdf':str(pdf),'zip':str(out)},ensure_ascii=False))
