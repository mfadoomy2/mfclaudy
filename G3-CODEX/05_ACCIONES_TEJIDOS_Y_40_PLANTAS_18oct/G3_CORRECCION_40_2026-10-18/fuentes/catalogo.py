from pathlib import Path
import rhino3dm as r,json
P=Path(__file__).resolve().parents[1]
files=sorted((P/'modelos_listos' if (P/'modelos_listos').exists() else P/'modelos').glob('N*_CORREGIDA.3dm'));assert len(files)==40
master=r.File3dm();master.Settings.ModelUnitSystem=r.UnitSystem.Meters;master.Settings.ModelAbsoluteTolerance=.001
materials={};reports=[]
for i,path in enumerate(files):
 f=r.File3dm.Read(str(path));code=path.name.split('_')[0];dx=(i%5)*36;dy=-(i//5)*36;xf=r.Transform.Translation(dx,dy,0)
 parent=r.Layer();parent.Name=code;parent.Color=(85,109,91,255);pi=master.Layers.Add(parent);lm={};mm={}
 for l in f.Layers:
  child=r.Layer();child.Name=l.Name;child.Color=l.Color;child.Visible=l.Visible;child.ParentLayerId=master.Layers[pi].Id;lm[l.Index]=master.Layers.Add(child)
 for j,m in enumerate(f.Materials):
  if m.Name not in materials:materials[m.Name]=master.Materials.Add(m)
  mm[j]=materials[m.Name]
 for ob in f.Objects:
  g=ob.Geometry;g.Transform(xf);a=ob.Attributes;a.LayerIndex=lm[a.LayerIndex]
  if a.MaterialIndex in mm:a.MaterialIndex=mm[a.MaterialIndex]
  master.Objects.Add(g,a)
 a=r.ObjectAttributes();a.LayerIndex=pi;master.Objects.AddTextDot(code,r.Point3d(dx,dy-11,0),a)
 reports.append({'code':code,'offset':[dx,dy,0],'objects':len(f.Objects)})
master.Strings['Estado']='40 ALTERNATIVAS CORREGIDAS. Metros, acabado z=0. No apiladas. Cada raíz de capas es una unidad. Las vistas nombradas se ajustan en Rhino.'
master.Strings['Validacion']='Comprobación geométrica de pasos, huecos, dimensiones y sólidos. Sin validación solar en parcela ni cálculo estructural.'
assert master.Write(str(P/'CATALOGO_40_CORREGIDAS_COTA0.3dm'),8)
(P/'verificacion/CATALOGO.json').write_text(json.dumps(reports,indent=2));print('CATALOGO_40',len(master.Objects),flush=True)
