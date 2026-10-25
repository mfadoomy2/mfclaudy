from pathlib import Path
import pickle,json
import rhino3dm as rh
P=Path(__file__).resolve().parents[1];src=P/'fuentes/modelar.py';ns={'__file__':str(src)};exec(src.read_text().split('reports=[]')[0],ns);Model=ns['Model'];D=pickle.load(open(P/'datos/GEOMETRIA_3D.pkl','rb'));records=[]
for d in D:
 m=Model(d['code']);ex,ey,angle=d['entry3d'];tr=rh.Transform.Multiply(rh.Transform.Translation(ex,ey,0),rh.Transform.Rotation(__import__('math').radians(angle),rh.Vector3d(0,0,1),rh.Point3d(0,0,0)))
 for x in [1.0,2.0]:m.rod((x,-.02,2.15),(x,-.02,2.26),.012,'carro suspensión corredera acceso','10_ACCESO','inox',tr)
 bb=d['floor3d'].bounds;shift=rh.Transform.Translation(-(bb[0]+bb[2])/2,-(bb[1]+bb[3])/2,0);p=P/'modelos_finales'/f'{d["code"]}_UNIDAD_3D.3dm';f=rh.File3dm.Read(str(p));li=next(i for i,l in enumerate(f.Layers) if l.Name=='10_ACCESO');mi=next(i for i,mat in enumerate(f.Materials) if mat.Name=='inox')
 for o in m.f.Objects:
  geom=o.Geometry;geom.Transform(shift);a=o.Attributes;a.LayerIndex=li;a.MaterialIndex=mi;f.Objects.Add(geom,a)
 assert f.Write(str(p),8);records.append({'code':d['code'],'track_z':[2.24,2.28],'door_leaf_top_z':2.165,'hanger_z':[2.15,2.26],'hangers':2})
(P/'verificacion/CARROS_ACCESO.json').write_text(json.dumps(records,indent=2));print('80_CARROS_ACCESO')
