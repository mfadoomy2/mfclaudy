from pathlib import Path
import pickle,json,math,sys
import rhino3dm as rh
P=Path(__file__).resolve().parents[1];s=P/'fuentes/modelar.py';ns={'__file__':str(s)};exec(s.read_text().split('reports=[]')[0],ns);Model=ns['Model'];xfroom=ns['xfroom'];D=pickle.load(open(P/'datos/GEOMETRIA_3D.pkl','rb'));results=[];(P/'modelos_finales').mkdir(exist_ok=True)
for d in D:
 m=Model(d['code']);K='09_COCINA';L='03_HABITACIONES';it=next(x for x in d['items'] if x['name']=='K');x,y,X,Y=it['poly'].bounds
 for j in range(6):
  for xx in [x+j*.6+.09,x+j*.6+.51]:
   for yy in [y+.10,Y-.10]:m.rod((xx,yy,0),(xx,yy,.115),.018,'pie regulable módulo cocina',K,'acero')
  for xx in [x+j*.6+.13,x+j*.6+.47]:m.rod((xx,y+.005,.75),(xx,y+.04,.75),.009,'separador tirador cocina',K,'inox')
 it=next(x for x in d['items'] if x['name']=='F');x,y,X,Y=it['poly'].bounds
 for z in [1.0,1.4]:m.rod((x+.08,y-.02,z),(x+.08,y+.015,z),.012,'soporte tirador frigorífico',K,'inox')
 for r in d['rooms']:
  tr=xfroom(r)
  for z in [1.,1.15]:m.rod((1.68,.055,z),(1.68,.085,z),.01,'separador tirador puerta',L,'inox',tr)
 bb=d['floor3d'].bounds;shift=rh.Transform.Translation(-(bb[0]+bb[2])/2,-(bb[1]+bb[3])/2,0)
 f=rh.File3dm.Read(str(P/'modelos'/f'{d["code"]}_UNIDAD_3D.3dm'));layers={l.Name:l.Index for l in f.Layers};mi={mat.Name:i for i,mat in enumerate(f.Materials)};count=0
 for obj in m.f.Objects:
  geom=obj.Geometry;geom.Transform(shift);a=obj.Attributes;a.LayerIndex=layers[m.f.Layers[a.LayerIndex].Name];a.MaterialIndex=mi[m.f.Materials[a.MaterialIndex].Name];f.Objects.Add(geom,a);count+=1
 assert f.Write(str(P/'modelos_finales'/f'{d["code"]}_UNIDAD_3D.3dm'),8)
 results.append({'code':d['code'],'added_supported_details':count,'objects':len(f.Objects)})
(P/'verificacion/APOYOS_DETALLE.json').write_text(json.dumps(results,indent=2));print('APOYOS_40_COMPLETADOS')
