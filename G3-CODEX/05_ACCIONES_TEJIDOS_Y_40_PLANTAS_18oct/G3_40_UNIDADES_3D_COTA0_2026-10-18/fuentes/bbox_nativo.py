# -*- coding: utf-8 -*-
import Rhino,os,json
P=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18'
data=json.load(open(os.path.join(P,'datos','CANDIDATOS_BBOX.json')));out=[]
for row in data:
 f=Rhino.FileIO.File3dm.Read(os.path.join(P,'ENTREGA','modelos',row['file']));ids=set(row['ids'])
 for obj in f.Objects:
  if str(obj.Attributes.Id) not in ids:continue
  b=obj.Geometry.GetBoundingBox(True);out.append(dict(file=row['file'],id=str(obj.Attributes.Id),name=obj.Attributes.Name,zmin=b.Min.Z,zmax=b.Max.Z,within_model=(-.221<b.Min.Z and b.Max.Z<3.17)))
json.dump(out,open(os.path.join(P,'ENTREGA','verificacion','BBOX_NATIVO_PRECISO.json'),'w'),indent=2)
Rhino.RhinoApp.WriteLine('BBOX_PRECISO '+str(len(out))+' fuera '+str(sum(not x['within_model'] for x in out)))
