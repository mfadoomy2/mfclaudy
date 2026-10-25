from pathlib import Path
import rhino3dm as r
P=Path(__file__).resolve().parents[1]
codes=['V01_U','V02_U','V03_U','V02_P','V01_D','V01_S','V03_D','V03_S']
m=r.File3dm();m.Settings.ModelUnitSystem=r.UnitSystem.Meters
for i,code in enumerate(codes):
 src=r.File3dm.Read(str(P/'modelos'/(code+'_3D_INTERIOR.3dm')))
 par=r.Layer();par.Name=code;pi=m.Layers.Add(par);parent=m.Layers[pi].Id;layers={};mats={}
 for j,mat in enumerate(src.Materials):mats[j]=m.Materials.Add(mat)
 for l in src.Layers:
  a=r.Layer();a.Name=l.Name;a.Color=l.Color;a.Visible=l.Visible;a.ParentLayerId=parent;layers[l.Index]=m.Layers.Add(a)
 bs=[o.Geometry.GetBoundingBox() for o in src.Objects];cx=(min(b.Min.X for b in bs)+max(b.Max.X for b in bs))/2;cy=(min(b.Min.Y for b in bs)+max(b.Max.Y for b in bs))/2
 tx=i%4*42-cx;ty=-(i//4)*42-cy;T=r.Transform.Translation(tx,ty,0)
 for o in src.Objects:
  g=o.Geometry.Duplicate();g.Transform(T);a=r.ObjectAttributes();a.Name=o.Attributes.Name;a.ColorSource=r.ObjectColorSource.ColorFromObject;a.ObjectColor=o.Attributes.ObjectColor;a.MaterialSource=r.ObjectMaterialSource.MaterialFromObject;a.LayerIndex=layers[o.Attributes.LayerIndex];a.MaterialIndex=mats.get(o.Attributes.MaterialIndex,-1);m.Objects.Add(g,a)
 m.Objects.AddTextDot(code,r.Point3d(i%4*42,-(i//4)*42-15,0),r.ObjectAttributes())
v=r.ViewInfo();v.Name='01_CATALOGO';vp=v.Viewport;loc=(63,-20,170);tgt=(63,-20,0);vp.SetCameraLocation(r.Point3d(*loc));vp.SetCameraDirection(r.Vector3d(0,0,-1));vp.SetCameraUp(r.Vector3d(0,1,0));vp.TargetPoint=r.Point3d(*tgt);vp.ChangeToParallelProjection(True);vp.Extents(.3,r.BoundingBox(r.Point3d(-22,-62,-1),r.Point3d(148,20,5)));m.NamedViews.Add(v)
p=P/'modelos/TODAS_LAS_PLANTAS_3D_COTA0.3dm';assert m.Write(str(p),8)
check=r.File3dm.Read(str(p));assert all(o.Geometry.IsValid for o in check.Objects);print(p,len(check.Objects))
