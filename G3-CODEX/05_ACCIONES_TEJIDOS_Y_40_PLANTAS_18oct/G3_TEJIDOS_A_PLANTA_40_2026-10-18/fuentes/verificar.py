from pathlib import Path
import pickle,json,math,csv
import rhino3dm as rh
import fitz
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parents[1];ds=pickle.load(open(P/'datos/geometrias.pkl','rb'))
layers=[('00_SUELO',(224,207,167,255)),('01_PRIVADO',(156,190,149,255)),('02_MOBILIARIO',(202,112,165,255)),('03_COCINA',(23,159,168,255)),('04_BANOS',(175,138,169,255)),('05_PUERTAS_Y_VENTANAS',(25,155,160,255)),('06_TEXTIL',(201,64,136,255)),('07_RED_PASO',(170,207,188,255))]
reports=[]
for d in ds:
 f=rh.File3dm();f.Settings.ModelUnitSystem=rh.UnitSystem.Meters;f.Settings.ModelAbsoluteTolerance=.001;li={}
 for name,color in layers:
  layer=rh.Layer();layer.Name=name;layer.Color=color;li[name[:2]]=f.Layers.Add(layer)
 bb=d['floor'].bounds;cx=(bb[0]+bb[2])/2;cy=(bb[1]+bb[3])/2
 def curve(coords,layer,name):
  a=rh.ObjectAttributes();a.LayerIndex=li[layer];a.Name=name
  pts=[]
  for x,y in coords:
   q=rh.Point3d(float(x)-cx,float(y)-cy,0)
   if not pts or q.DistanceTo(pts[-1])>1e-5:pts.append(q)
  if len(pts)>2 and pts[-1].DistanceTo(pts[0])<1e-5:pts[-1]=pts[0]

  if len(pts)>1:f.Objects.AddCurve(rh.PolylineCurve(pts),a)
 def geo(g,layer,name):
  ps=[g] if g.geom_type=='Polygon' else list(g.geoms)
  for p in ps:
   if p.geom_type!='Polygon':continue
   curve(p.exterior.coords,layer,name)
   for ring in p.interiors:curve(ring.coords,layer,name+' vacío')
 geo(d['floor'],'00','Contorno suelo conceptual')
 for room in d['rooms']:
  geo(room['poly'],'01',room['id']+' perímetro')
  for key in ['bed','desk','chair','ward','use']:geo(room[key],'02',room['id']+' '+key)
  for key in ['window','doorline','hinge']:curve(room[key],'05',room['id']+' '+key)
  angle=math.radians(room['angle']);off=(-math.sin(angle)*.35,math.cos(angle)*.35)
  curve([(x+off[0],y+off[1]) for x,y in room['window']],'06',room['id']+' reserva textil')
 for it in d['items']:geo(it['poly'],'04' if it['name'].startswith('B') else '03',it['name']+' reserva de equipamiento')
 geo(d['reserved'].intersection(d['shared']),'07','Red de paso reservada')
 if 'task' in d:
  geo(d['task'],'02','Mesa cortar coser')
  geo(d['dry'],'02','Reserva secar')
 f.Strings['Documento']='Exploración de planta 2D; no modelo 3D ni proyecto ejecutivo'
 f.Strings['Código']=d['code'];f.Strings['Origen']='Centro de envolvente XY; toda geometría Z=0; metros'
 dest=P/'modelos'/f'{d["code"]}_PLANTA_2D.3dm';assert f.Write(str(dest),8)
 read=rh.File3dm.Read(str(dest));assert read and len(read.Objects)>0
 invalid=sum(not o.Geometry.IsValid for o in read.Objects)
 assert invalid==0
 reports.append({'code':d['code'],'objects':len(read.Objects),'invalid':invalid,'unit':'metres','type':'2D contours; not 3D','native_rhino_visual_check':False})
(P/'verificacion/CAD_40.json').write_text(json.dumps(reports,indent=2))
actual=[]
for d in ds:
 parts=[d['floor']] if d['floor'].geom_type=='Polygon' else list(d['floor'].geoms)
 substantive=[p for p in parts if p.area>.02]
 conf=[]
 for r in d['rooms']:
  for key in ['bed','desk','chair','ward']:
   if r[key].difference(r['poly']).area>.02:conf.append(r['id']+' '+key+' fuera')
  for a,b in [('bed','desk'),('bed','ward'),('desk','ward'),('chair','bed')]:
   if r[a].intersection(r[b]).area>.002:conf.append(r['id']+' '+a+'/'+b)
 private_overlaps=sum(d['rooms'][i]['poly'].intersection(d['rooms'][j]['poly']).area for i in range(4) for j in range(i))
 actual.append({'code':d['code'],'floor_components_over_002_m2':len(substantive),'connections':d['connections'],'furniture_conflicts':conf,'private_overlap_m2':private_overlaps,'entry_on_boundary':d['entry_on_boundary']})
 actionmap={key:[[round(p.x,3),round(p.y,3)] for p in points] for key,points in d['action_map'].items()}
 (P/'datos'/f'{d["code"]}_ACCIONES_UBICADAS.json').write_text(json.dumps(actionmap,indent=2))
assert len(ds)==40 and all(d['connections']==4 for d in ds)
assert all(a['floor_components_over_002_m2']==1 and a['private_overlap_m2']<.001 and not a['furniture_conflicts'] for a in actual)
(P/'verificacion/AUDITORIA_GEOMETRIA.json').write_text(json.dumps(actual,indent=2))
pdf=fitz.open(P/'output/pdf/G3_40_PLANTAS_DESDE_TEJIDOS_A3.pdf')
for i,page in enumerate(pdf):
 assert abs(page.rect.width-1190.55)<1
 page.get_pixmap(matrix=fitz.Matrix(.7,.7),alpha=False).save(P/'verificacion'/f'pagina_{i+1:03}.png')
for chunk in range(math.ceil(len(pdf)/24)):
 sheet=Image.new('RGB',(1800,1920),'white');draw=ImageDraw.Draw(sheet)
 for j in range(24):
  k=chunk*24+j
  if k>=len(pdf):break
  im=Image.open(P/'verificacion'/f'pagina_{k+1:03}.png');im.thumbnail((442,290));x=(j%4)*450;y=(j//4)*320;sheet.paste(im,(x,y+20));draw.text((x+5,y+3),str(k+1),fill='black')
 sheet.save(P/'verificacion'/f'contacto_pdf_{chunk+1}.jpg')
report={'count':40,'families':20,'variants_each':2,'pdf_pages':len(pdf),'plan_png':len([q for q in (P/'plantas').glob('*_PLANTA.png') if not q.name.startswith('._')]),'plan_svg':len([q for q in (P/'plantas').glob('*_PLANTA.svg') if not q.name.startswith('._')]),'traces':len([q for q in (P/'plantas').glob('*_TRAZA.png') if not q.name.startswith('._')]),'cad':len(reports),'all_floor_connected':True,'private_furniture_collisions':0,'four_entry_proxies_connected':40,'area_min':min(d['floor'].area for d in ds),'area_max':max(d['floor'].area for d in ds),'status':'exploratory; not an approved housing layout','unverified':['daylight','site','structure','accessibility','fire evacuation','complete door and fixture use','acoustic protection','compliance with previous 1500m2 target']}
(P/'verificacion/VERIFICACION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,indent=2))
