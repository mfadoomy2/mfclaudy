# -*- coding: utf-8 -*-
import Rhino,os,time,json,traceback
P=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18'
t=time.time()
try:
 f=Rhino.FileIO.File3dm.Read(os.path.join(P,'modelos','N01A_CORREGIDA.3dm'))
 bs=[]
 for o in f.Objects:
  layer=next(l for l in f.Layers if l.Index==o.Attributes.LayerIndex)
  if layer.Name.startswith('02_'):bs.append(o.Geometry.ToBrep() if isinstance(o.Geometry,Rhino.Geometry.Extrusion) else o.Geometry.DuplicateBrep())
 u=Rhino.Geometry.Brep.CreateBooleanUnion(bs,.001)
 result=dict(seconds=time.time()-t,input=len(bs),output=len(u) if u else 0,valid=all(b.IsValid and b.IsSolid for b in u) if u else False)
except:result={'error':traceback.format_exc()}
with open(os.path.join(P,'verificacion','PRUEBA_UNION.json'),'w') as out:json.dump(result,out)
Rhino.RhinoApp.WriteLine(str(result))
