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
  pts=[rh.Point3d(float(x)-cx,float(y)-cy,0) for x,y in coords]
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
 f.Strings['Documento']='Exploración de planta 2D; no modelo 3D ni proyecto ejecutivo'
 f.Strings['Código']=d['code'];f.Strings['Origen']='Centro de envolvente XY; toda geometría Z=0; metros'
 dest=P/'modelos'/f'{d["code"]}_PLANTA_2D.3dm';assert f.Write(str(dest),8)
 read=rh.File3dm.Read(str(dest));assert read and len(read.Objects)>0
 invalid=sum(not o.Geometry.IsValid for o in read.Objects)
 assert invalid==0
 reports.append({'code':d['code'],'objects':len(read.Objects),'invalid':invalid,'unit':'metres','type':'2D contours; not 3D','native_rhino_visual_check':False})
(P/'verificacion/CAD_40.json').write_text(json.dumps(reports,indent=2))
pdf=fitz.open(P/'output/pdf/G3_40_PLANTAS_ATLAS_A3.pdf');assert len(pdf)==48
for i,page in enumerate(pdf):
 pix=page.get_pixmap(matrix=fitz.Matrix(.85,.85),alpha=False);pix.save(P/'verificacion'/f'pagina_{i+1:02}.png')
for chunk in range(4):
 canvas=Image.new('RGB',(1600,1800),'white');draw=ImageDraw.Draw(canvas)
 for j in range(12):
  k=chunk*12+j;im=Image.open(P/'verificacion'/f'pagina_{k+1:02}.png');im.thumbnail((390,550));x=(j%4)*400;y=(j//4)*600;canvas.paste(im,(x,y+22));draw.text((x+8,y+5),str(k+1),fill='black')
 canvas.save(P/'verificacion'/f'pdf_contacto_{chunk+1}.jpg')
report={'pdf_pages':len(pdf),'a3_landscape':all(abs(p.rect.width-1190.55)<1 for p in pdf),'plans':len(ds),'families':len(set(d['code'][:2] for d in ds)),'png':len([q for q in (P/'plantas').glob('*.png') if not q.name.startswith('._')]),'svg':len([q for q in (P/'plantas').glob('*.svg') if not q.name.startswith('._')]),'cad':len(reports),'shared_connections_4_of_4':sum(d['connections']==4 for d in ds),'bed_furniture_conflicts':sum(len(d['geometry_conflicts']) for d in ds),'area_range_m2':[min(d['floor'].area for d in ds),max(d['floor'].area for d in ds)],'holes':{d['code']:len(d['holes']) for d in ds if d['holes']},'limits':['No solar or daylight simulation','No regulatory verification','No 3D model','External entry route not verified','No wall or structure thickness','All exceed previous total area target']}
assert report['png']==report['svg']==report['cad']==report['plans']==40
(P/'verificacion/VERIFICACION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,indent=2))
