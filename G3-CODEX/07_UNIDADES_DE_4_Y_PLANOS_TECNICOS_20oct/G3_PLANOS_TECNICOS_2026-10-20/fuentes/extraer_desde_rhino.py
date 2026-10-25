# -*- coding: utf-8 -*-
import Rhino
import System
import json, os, math, traceback
ROOT = u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20'

def poly(curve):
    ok, pp = curve.TryGetPolyline()
    if ok: return [[p.X,p.Y,p.Z] for p in pp]
    # Equal-length samples preserve curved carpentry and bow geometry to a
    # maximum 15 mm chord; no perspective or rasterization is involved.
    length = curve.GetLength()
    count = max(2, min(16000,int(math.ceil(length/.015))))
    ts = curve.DivideByCount(count,True)
    return [[curve.PointAt(t).X,curve.PointAt(t).Y,curve.PointAt(t).Z] for t in ts]

def loops_face(face):
    return [{'outer':loop.LoopType==Rhino.Geometry.BrepLoopType.Outer,'points':poly(loop.To3dCurve())} for loop in face.Loops]

def extract(path,code,level):
    f=Rhino.FileIO.File3dm.Read(path)
    out={'source':path,'code':code,'floor_level':level,'cut_level':level+1.20,'units':str(f.Settings.ModelUnitSystem),'objects':[],'errors':[]}
    layers={la.Index:la for la in f.AllLayers}
    for ob in f.Objects:
        g=ob.Geometry;a=ob.Attributes;la=layers.get(a.LayerIndex)
        if la is None:continue
        parent=[];cur=la
        while cur is not None:
            parent.insert(0,unicode(cur.Name))
            if cur.ParentLayerId==System.Guid.Empty:break
            cur=next((l for l in layers.values() if l.Id==cur.ParentLayerId),None)
        if isinstance(g,(Rhino.Geometry.Curve,Rhino.Geometry.TextDot,Rhino.Geometry.AnnotationBase)):continue
        bb=g.GetBoundingBox(True)
        item={'id':str(a.ObjectId),'name':unicode(a.Name or ''), 'layer':unicode(la.Name),'parents':parent,'type':str(g.GetType().Name),'bbox':[[bb.Min.X,bb.Min.Y,bb.Min.Z],[bb.Max.X,bb.Max.Y,bb.Max.Z]],'sections':[],'profiles':[],'caps':[]}
        try:
            brep=None
            if isinstance(g,Rhino.Geometry.Extrusion):
                for k in range(g.ProfileCount):
                    item['profiles'].append(poly(g.Profile3d(k,0.0)))
                brep=g.ToBrep()
            elif isinstance(g,Rhino.Geometry.Brep):brep=g
            if brep is not None:
                if not item['profiles']:
                    for face in brep.Faces:
                        uu=face.Domain(0).Mid;vv=face.Domain(1).Mid
                        if abs(face.NormalAt(uu,vv).Z)>.9999:
                            item['caps'].append(loops_face(face))
                if bb.Min.Z<level+1.20+.001 and bb.Max.Z>level+1.20-.001:
                    success,curves,points=Rhino.Geometry.Intersect.Intersection.BrepPlane(brep,Rhino.Geometry.Plane(Rhino.Geometry.Point3d(0,0,level+1.20),Rhino.Geometry.Vector3d.ZAxis),.001)
                    if success and curves:
                        for cv in Rhino.Geometry.Curve.JoinCurves(curves,.001):item['sections'].append(poly(cv))
            elif isinstance(g,Rhino.Geometry.Mesh):
                # Exact mesh/plane intersection for masts and pipe cuts.
                if bb.Min.Z<level+1.20 and bb.Max.Z>level+1.20:
                    for pp in Rhino.Geometry.Intersect.Intersection.MeshPlane(g,Rhino.Geometry.Plane(Rhino.Geometry.Point3d(0,0,level+1.20),Rhino.Geometry.Vector3d.ZAxis)) or []:item['sections'].append([[p.X,p.Y,p.Z] for p in pp])
                if la.Name in ['19_SOPORTE_PB','21_NUCLEO_VERTICAL']:
                    for pp in g.GetOutlines(Rhino.Geometry.Plane.WorldXY) or []:item['profiles'].append([[p.X,p.Y,p.Z] for p in pp])
        except Exception as e:out['errors'].append({'name':item['name'],'error':unicode(e)})
        out['objects'].append(item)
    return out

def ascii_json(value):
    if isinstance(value,dict):return {ascii_json(k):ascii_json(v) for k,v in value.items()}
    if isinstance(value,list):return [ascii_json(v) for v in value]
    if isinstance(value,(str,unicode,System.String)):return unicode(value).encode("ascii","replace")
    return value

try:
    data=[]
    data.append(extract(os.path.join(ROOT,'instantaneas','TRES_UNIDADES_ESTADO_USUARIO.3dm'),'TRES',0))
    data.append(extract(os.path.join(ROOT,'instantaneas','E02_ESTADO_USUARIO.3dm'),'E02',4.2))
    data.append(extract(os.path.join(ROOT,'instantaneas','E02_ESTADO_USUARIO.3dm'),'E02_PB',0))
    with open(os.path.join(ROOT,'verificacion','EXTRACCION_RHINO.json'),'w') as stream:json.dump(ascii_json(data),stream,ensure_ascii=True)
    print('G3: extraccion metrica terminada. Objetos: '+str([len(d['objects']) for d in data]))
except:
    with open(os.path.join(ROOT,'verificacion','ERROR_RHINO.txt'),'w') as stream:stream.write(traceback.format_exc())
    print(traceback.format_exc())
