import rhino3dm as r, json, collections, pathlib
from PIL import Image,ImageOps,ImageDraw
base=pathlib.Path('/Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08')
paths=['/Users/adam/Downloads/G3_unidad_suspendida_7.3dm','/Users/adam/Downloads/G3_conjunto_opciones_1.3dm']
for path in paths:
 f=r.File3dm.Read(path); layers={l.Index:l for l in f.Layers}; counts=collections.Counter(); out={}
 for o in f.Objects:
  i=o.Attributes.LayerIndex; k=layers[i].FullPath; counts[type(o.Geometry).__name__]+=1
  b=o.Geometry.GetBoundingBox()
  item=out.setdefault(k,{'n':0,'types':{},'min':[1e20]*3,'max':[-1e20]*3,'names':[]})
  item['n']+=1; t=type(o.Geometry).__name__; item['types'][t]=item['types'].get(t,0)+1
  for a,axis in enumerate('XYZ'):
   item['min'][a]=min(item['min'][a],getattr(b.Min,axis));item['max'][a]=max(item['max'][a],getattr(b.Max,axis))
  if o.Attributes.Name and len(item['names'])<4:item['names'].append(o.Attributes.Name)
 data={'path':path,'units':str(f.Settings.ModelUnitSystem),'objects':len(f.Objects),'types':dict(counts),'layers':out,'views':[v.Name for v in f.Views]}
 (base/'trabajo'/(pathlib.Path(path).stem+'.json')).write_text(json.dumps(data,indent=2,ensure_ascii=False))
 print(path,data['units'],data['objects'],counts)
 for k,v in out.items():print(k,v['n'],[round(x,2) for x in v['min']],[round(x,2) for x in v['max']],v['types'])
files=sorted(pathlib.Path('/Users/adam/Downloads/cosas').glob('*.jpg'))
canvas=Image.new('RGB',(2000,1000),'white');d=ImageDraw.Draw(canvas)
for i,p in enumerate(files):
 im=Image.open(p);im.thumbnail((380,435));x=(i%5)*400+(400-im.width)//2;y=(i//5)*500+30
 canvas.paste(im,(x,y));d.text(((i%5)*400+10,(i//5)*500+475),f'{i+1:02} {p.stem[:12]}',fill='black')
canvas.save(base/'vistas/referencias_contacto.jpg')
