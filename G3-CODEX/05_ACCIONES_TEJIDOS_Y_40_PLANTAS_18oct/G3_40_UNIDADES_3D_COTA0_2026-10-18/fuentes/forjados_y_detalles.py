from pathlib import Path
import pickle,json,copy
import rhino3dm as rh
from shapely.geometry import box,Point
from shapely.ops import unary_union
P=Path(__file__).resolve().parents[1];src=P/'fuentes/modelar.py';ns={'__file__':str(src)};exec(src.read_text().split('reports=[]')[0],ns);Model=ns['Model'];room_detail=ns['room_detail'];D=pickle.load(open(P/'datos/GEOMETRIA_3D.pkl','rb'));records=[]
for d in D:
 p=P/'modelos_finales'/f'{d["code"]}_UNIDAD_3D.3dm';f=rh.File3dm.Read(str(p));m=Model(d['code']);m.ex(d['floor3d'].buffer(.13,resolution=20),-.22,.22,'forjado continuo, acabado z=0','01_SUELO','corcho',support='incluye apoyo bajo todos los muros perimetrales')
 bb=d['floor3d'].bounds;tr=rh.Transform.Translation(-(bb[0]+bb[2])/2,-(bb[1]+bb[3])/2,0);idx=next(i for i,l in enumerate(f.Layers) if l.Name=='01_SUELO');matidx=next(i for i,x in enumerate(f.Materials) if x.Name=='corcho')
 for o in list(f.Objects):
  if o.Attributes.Name.startswith('forjado continuo'):f.Objects.Delete(o.Attributes.Id)
 for o in m.f.Objects:
  geom=o.Geometry;geom.Transform(tr);a=o.Attributes;a.LayerIndex=idx;a.MaterialIndex=matidx;f.Objects.Add(geom,a)
 assert f.Write(str(p),8);records.append({'code':d['code'],'slab_outside_finish_outline_m':.13,'wall_thickness_m':.12,'floor_z':0})
(P/'detalles_habitacion').mkdir(exist_ok=True)
for variant in ['A','B']:
 d=next(d for d in D if d['variant']==variant);r=copy.copy(d['rooms'][0]);r['angle']=0;r['door']=(1.05,0);r['poly']=r['local3d'];floor=r['poly'];walls=floor.buffer(.12).difference(floor);doors=box(.45,-.3,1.55,.3);windows=box(1.15,5.25,3.8,5.7);m=Model('HABITACION_'+variant)
 m.ex(floor.buffer(.13),-.22,.22,'forjado habitación, acabado 0','01_SUELO','corcho',support='apoyo continuo bajo suelo y muros')
 m.ex(walls.difference(doors),0,.44,'antepechos y jambas','02_CERRAMIENTOS','cal',support='forjado')
 m.ex(walls.difference(doors.union(windows)),.44,1.76,'cerramiento','02_CERRAMIENTOS','cal',support='paños inferiores')
 m.ex(walls.difference(windows),2.2,.35,'dinteles','02_CERRAMIENTOS','cal',support='jambas');m.ex(walls,2.55,.45,'coronación','02_CERRAMIENTOS','cal',support='paños laterales')
 room_detail(m,r,variant);m.ex(floor,3,.16,'cubierta en posición real','91_CUBIERTA_OCULTA','blanco',visible=False,support='muros')
 assert m.f.Write(str(P/'detalles_habitacion'/f'HABITACION_{variant}_DETALLE.3dm'),8)
(P/'verificacion/APOYO_MUROS_Y_FORJADO.json').write_text(json.dumps(records,indent=2));print('FORJADOS_40_Y_2_HABITACIONES_LISTOS')
