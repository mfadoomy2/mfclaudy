from pathlib import Path
import json,hashlib,zipfile,shutil
import rhino3dm as rh
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parents[1];E=P/'ENTREGA'
# Regenerate contact sheets after the corrected final top-view framing.
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',21)
for half in range(2):
 sheet=Image.new('RGB',(2100,1330),'#f8f6f0');dr=ImageDraw.Draw(sheet)
 for j in range(20):
  i=half*20+j;code=f'N{i//2+1:02}{"AB"[i%2]}';im=Image.open(E/'vistas'/f'{code}_PLANTA.png');im.thumbnail((408,282));x=(j%5)*420;y=(j//5)*330;sheet.paste(im,(x+(420-im.width)//2,y+32));dr.text((x+14,y+5),code,font=font,fill='#253d35')
 sheet.save(E/'vistas'/f'CONTACTO_PLANTA_{half+1}.jpg',quality=95)
for p in (P/'fuentes').glob('*.py'):
 if not p.name.startswith('._') and p.name not in ['auditar_recorridos.py','prueba_nativa.py']:shutil.copyfile(p,E/'fuentes'/p.name)
for name in ['NATIVO_ENTREGA.json','NATIVO_VERIFICACION_ULTIMA.json','CARROS_ACCESO.json']:
 shutil.copyfile(P/'verificacion'/name,E/'verificacion'/name)
models=sorted(p for p in (E/'modelos').glob('*.3dm') if not p.name.startswith('._'));assert len(models)==40
reports=[];hashes=[]
for p in models+list((E/'habitaciones').glob('HABITACION_*.3dm')):
 f=rh.File3dm.Read(str(p));assert f is not None;invalid=[];nonsolid=[];ranges=[]
 for o in f.Objects:
  g=o.Geometry
  if not g.IsValid:invalid.append(o.Attributes.Name)
  if hasattr(g,'IsSolid') and not g.IsSolid:nonsolid.append(o.Attributes.Name)
  b=g.GetTightBoundingBox();ranges.append((b.Min.Z,b.Max.Z))
 assert not invalid and not nonsolid,(p,invalid,nonsolid)
 floors=[o.Geometry.GetTightBoundingBox() for o in f.Objects if o.Attributes.Name.startswith('forjado')]
 assert floors and all(abs(b.Max.Z)<1e-6 and abs(b.Min.Z+.22)<1e-6 for b in floors)
 assert min(b[0] for b in ranges)>-.221 and max(b[1] for b in ranges)<3.17
 h=hashlib.sha256(p.read_bytes()).hexdigest();hashes.append(h);reports.append({'file':p.relative_to(E).as_posix(),'objects':len(f.Objects),'invalid':invalid,'open_solids':nonsolid,'floor_z':0,'sha256':h})
assert len(set(hashes[:40]))==40
master=rh.File3dm.Read(str(E/'CATALOGO_40_UNIDADES_COTA0.3dm'));floors={}
for o in master.Objects:
 assert o.Geometry.IsValid
 if o.Attributes.Name.startswith('forjado continuo'):floors[o.Attributes.GetUserString('Unidad')]=o.Geometry.GetTightBoundingBox()
assert len(floors)==40 and len(master.NamedViews)==41
assert all(abs(b.Max.Z)<1e-6 for b in floors.values())
vals=list(floors.items())
for i,(code,a) in enumerate(vals):
 for code2,b in vals[:i]:assert a.Max.X<b.Min.X or b.Max.X<a.Min.X or a.Max.Y<b.Min.Y or b.Max.Y<a.Min.Y,(code,code2)
native=json.load(open(E/'verificacion/NATIVO_VERIFICACION_ULTIMA.json'));assert len(native)==40 and all(not q['invalid'] and not q['open_solids'] for q in native)
vol=json.load(open(E/'verificacion/NATIVO_ENTREGA.json'));assert len(vol)==40 and all(not q['adjusted_basin_volume_errors'] for q in vol)
review={'units_3d':40,'isolated_rooms':2,'master_file_objects':len(master.Objects),'named_views':41,'floor_z_all':0,'no_xy_overlap_between_catalog_units':True,'all_geometry_valid':True,'individual_solid_geometries_closed':True,'native_volume_checks':'base perforated profiles + updated slabs and basins passed','interior_use_points':'160 rooms, body diameter0.80m; clear landing diameter1.40m','shared_room_entrances':'40 units, body diameter0.90m, including plotted furniture','visual_review':'40 native axons and 40 native top views inspected; wide top views reframed; two actual isolated rooms inspected','construction_ready':False,'remaining':['surface reduction','structural sizing','hardware loads and complete kinematics','daylight and ventilation','code compliance']}
(E/'verificacion/ENTREGA_COMPROBADA.json').write_text(json.dumps(review,ensure_ascii=False,indent=2));(E/'verificacion/MODELOS_FINALES.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
manifest={}
for q in sorted(E.rglob('*')):
 if not q.is_file() or q.name.startswith('._') or '__pycache__' in q.parts or q.suffix in ['.3dmbak','.bak'] or q.name=='MANIFIESTO_SHA256.json':continue
 manifest[q.relative_to(E).as_posix()]={'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}
(E/'MANIFIESTO_SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
zip_path=P/'G3_40_UNIDADES_3D_COTA0_ENTREGA.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for name in manifest:z.write(E/name,name)
 z.write(E/'MANIFIESTO_SHA256.json','MANIFIESTO_SHA256.json')
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 for name,meta in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==meta['sha256']
 assert sum(n.startswith('modelos/') and n.endswith('.3dm') for n in z.namelist())==40
result={'zip':str(zip_path),'zip_bytes':zip_path.stat().st_size,'files':len(manifest)+1,'units':40,'isolated_rooms':2,'master_objects':len(master.Objects),'crc_and_all_sha256':'passed','zip_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest()};(P/'verificacion/PAQUETE_FINAL.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
