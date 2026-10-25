from pathlib import Path
import math,json,pickle,uuid
import numpy as np
import rhino3dm as rh
from shapely.geometry import Point,Polygon,LineString,box
from shapely.ops import unary_union
from shapely.affinity import rotate,translate
from shapely.geometry.polygon import orient
MATS={'cal':('#d6dec9',0),'corcho':('#c2a47b',0),'madera':('#af815b',0),'lino':('#e7d9b5',0),'acero':('#434e4c',0),'inox':('#9da8a5',0),'vidrio':('#b6dcd6',.72),'rosa':('#c8447e',0),'azul':('#187c83',0),'blanco':('#ece9df',0),'ceramica':('#c2c9b7',0),'textil':('#cf7a9b',.15),'caucho':('#323c38',0)}
def color(h):return tuple(int(h[i:i+2],16) for i in (1,3,5))+(255,)
def polys(g):return [g] if g.geom_type=='Polygon' else [x for x in getattr(g,'geoms',[]) if x.geom_type=='Polygon']
def clean(coords,z):
 pts=[]
 for x,y in coords:
  q=rh.Point3d(float(x),float(y),z)
  if not pts or q.DistanceTo(pts[-1])>1e-5:pts.append(q)
 if len(pts)>2 and pts[-1].DistanceTo(pts[0])<1e-5:pts[-1]=pts[0]
 return rh.PolylineCurve(pts) if len(pts)>2 else None
class Model:
 def __init__(self,code):
  self.f=rh.File3dm();self.f.Settings.ModelUnitSystem=rh.UnitSystem.Meters;self.f.Settings.ModelAbsoluteTolerance=.001;self.layers={};self.mi={};self.records=[];self.code=code
  for name,(h,t) in MATS.items():
   m=rh.Material();m.Name=name;m.DiffuseColor=color(h);m.Transparency=t;m.Shine=90 if name in ['inox','vidrio'] else 12;self.mi[name]=self.f.Materials.Add(m)
 def layer(self,name,mat,visible=True):
  if name not in self.layers:
   l=rh.Layer();l.Name=name;l.Color=color(MATS[mat][0]);l.Visible=visible;self.layers[name]=self.f.Layers.Add(l)
  return self.layers[name]
 def add(self,g,name,layer,mat,xf=None,visible=True,support=''):
  if not g:return
  if xf:g.Transform(xf)
  if not g.IsValid:raise ValueError((self.code,name,'invalid'))
  a=rh.ObjectAttributes();a.Name=name;a.LayerIndex=self.layer(layer,mat,visible);a.MaterialIndex=self.mi[mat];a.MaterialSource=rh.ObjectMaterialSource.MaterialFromObject;a.ObjectColor=color(MATS[mat][0]);a.ColorSource=rh.ObjectColorSource.ColorFromObject;a.SetUserString('Apoyo',support);a.SetUserString('Unidad',self.code)
  self.f.Objects.Add(g,a);bb=g.GetTightBoundingBox();self.records.append({'name':name,'layer':layer,'zmin':bb.Min.Z,'zmax':bb.Max.Z,'support':support})
 def ex(self,g,z,h,name,layer,mat,xf=None,visible=True,support=''):
  for j,p in enumerate(polys(g)):
   if p.area<1e-7:continue
   pp=orient(p,sign=1);crv=clean(pp.exterior.coords,0)
   if not crv:continue
   ex=rh.Extrusion.Create(crv,h,True)
   for ring in pp.interiors:
    inner=clean(ring.coords,0)
    if inner:
     inner.Transform(ex.GetProfileTransformation(0).TryGetInverse())
     if not ex.AddInnerProfile(inner):raise ValueError('inner')
   ex.SetUserString('ExpectedVolume',str(p.area*h));ex.SetUserString('InnerProfiles',str(len(pp.interiors)))
   ex.Transform(rh.Transform.Translation(0,0,z))
   self.add(ex,name+(' '+str(j) if j else ''),layer,mat,xf,visible,support)
 def rod(self,a,b,r,name,layer,mat,xf=None):
  a=rh.Point3d(*a);b=rh.Point3d(*b);v=rh.Vector3d(b.X-a.X,b.Y-a.Y,b.Z-a.Z);plane=rh.Plane(a,v);circle=rh.Circle(r);circle.Plane=plane;g=rh.Cylinder(circle,a.DistanceTo(b)).ToBrep(True,True);self.add(g,name,layer,mat,xf,support='unión entre sus dos extremos')
 def box(self,x,y,z,w,h,depth,name,layer,mat,xf=None,visible=True,support=''):
  self.ex(box(x,y,x+w,y+h),z,depth,name,layer,mat,xf,visible,support)
 def sphere(self,p,r,name,layer,mat,xf=None):self.add(rh.Sphere(rh.Point3d(*p),r).ToBrep(),name,layer,mat,xf,support='apoyado o unido al elemento contiguo')

