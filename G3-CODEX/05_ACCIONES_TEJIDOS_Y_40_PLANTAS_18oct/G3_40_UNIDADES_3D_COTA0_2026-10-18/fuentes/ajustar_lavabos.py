from pathlib import Path
import pickle,json
import rhino3dm as rh
P=Path(__file__).resolve().parents[1];D=pickle.load(open(P/'datos/GEOMETRIA_3D.pkl','rb'));out=[]
for d in D:
 fpath=P/'modelos_finales'/f'{d["code"]}_UNIDAD_3D.3dm';f=rh.File3dm.Read(str(fpath));b=d['floor3d'].bounds;cx=(b[0]+b[2])/2;cy=(b[1]+b[3])/2;count=0
 for obj in f.Objects:
  if 'lavabo' not in obj.Attributes.Name:continue
  geom=obj.Geometry;bb=geom.GetBoundingBox();px=(bb.Min.X+bb.Max.X)/2+cx;py=(bb.Min.Y+bb.Max.Y)/2+cy
  bath=min([it for it in d['items'] if it['name'].startswith('B')],key=lambda it:it['poly'].centroid.distance(__import__('shapely').geometry.Point(px,py)))
  x,y,X,Y=bath['poly'].bounds;anchor=rh.Point3d(x+.1-cx,y+.25-cy,0);scale=rh.Transform.Scale(rh.Plane(anchor,rh.Vector3d(0,0,1)),.5/.6,.4/.45,1)
  geom.Transform(scale);geom.Transform(rh.Transform.Translation(0,-.13,0));expected=geom.GetUserString('ExpectedVolume')
  if expected:geom.SetUserString('ExpectedVolume',str(float(expected)*(.5/.6)*(.4/.45)))
  count+=1
 assert f.Write(str(fpath),8);out.append({'code':d['code'],'adjusted_washbasin_parts':count,'cabinet_mm':[500,400]})
(P/'verificacion/LAVABOS.json').write_text(json.dumps(out,indent=2));print('80_LAVABOS_AJUSTADOS')
