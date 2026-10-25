from pathlib import Path
import json,rhino3dm as r
R=Path(__file__).resolve().parents[1]
f=r.File3dm.Read(str(R/'modelos/SELVA_MACARRA_V4_FINAL.3dm'))
for l in f.Layers:
 if l.Name=='90_CONTEXTO':l.Visible=True
l=r.Layer();l.Name='91_LIMITE_PARCELA';l.Color=(220,40,95,255);ix=f.Layers.Add(l)
p=json.loads((R/'fuentes/parcela_local.geojson').read_text())['geometry']['coordinates'][0]
a=r.ObjectAttributes();a.LayerIndex=ix;a.Name='Limite de parcela de proyecto / cota terreno';a.ObjectColor=(220,40,95,255);a.ColorSource=r.ObjectColorSource.ColorFromObject
f.Objects.AddCurve(r.PolylineCurve([r.Point3d(x,y,.08) for x,y,*_ in p]),a)
for name,loc,tgt in [('09_IMPLANTACION_CONTEXTO',(110,-100,110),(41,4,12)),('10_PARCELA_CENITAL',(37,3,150),(37,3,0))]:
 v=r.ViewInfo();v.Name=name;vp=v.Viewport;vp.SetCameraLocation(r.Point3d(*loc));vp.SetCameraDirection(r.Vector3d(*(tgt[i]-loc[i] for i in range(3))));vp.SetCameraUp(r.Vector3d(0,1,0) if 'CENITAL' in name else r.Vector3d(0,0,1));vp.TargetPoint=r.Point3d(*tgt);vp.ChangeToParallelProjection(True);vp.Extents(.6,r.BoundingBox(r.Point3d(9,-39,-1),r.Point3d(83,58,51)));f.NamedViews.Add(v)
assert f.Write(str(R/'modelos/SELVA_MACARRA_V4_EN_PARCELA.3dm'),8)
print('MODELO CON CONTEXTO GUARDADO')
