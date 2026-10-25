from pathlib import Path
import math,json
import numpy as np
from PIL import Image
import rhino3dm as r
P=Path(__file__).parent;T=P/'texturas';T.mkdir(exist_ok=True)
rng=np.random.default_rng(18);n=768;y,x=np.mgrid[0:n,0:n]
wood=np.clip(8*np.sin(y*.15+2*np.sin(x*.014))+4*np.sin(y*.63)+rng.normal(0,2,(n,n)),-18,18);fabric=rng.normal(0,2,(n,n))+2*np.sin(x*2.4)+2*np.cos(y*2.2);cork=rng.normal(0,8,(n,n))
for name,base,noise in [('ROBLE',(190,149,103),wood),('LINO',(234,226,205),fabric),('CORCHO',(178,139,99),cork)]:
 im=np.clip(np.array(base)[None,None,:]+noise[:,:,None],0,255).astype('uint8');Image.fromarray(im).save(T/(name+'.png'))
src=P.parent/'G3_P02_CORREGIDA_APOYOS_2026-10-18/P02_CORREGIDA_INTERIOR.3dm';old=r.File3dm.Read(str(src));out=r.File3dm();out.Settings.ModelUnitSystem=r.UnitSystem.Meters;out.Settings.ModelAbsoluteTolerance=.001
mats={};spec=[('ROBLE',(190,149,103),0,'ROBLE',10),('SALVIA',(114,158,133),0,None,10),('LINO',(234,226,205),0,'LINO',3),('TURQUESA',(57,148,164),0,None,40),('CORCHO',(178,139,99),0,'CORCHO',5),('VIDRIO',(157,208,218),.72,None,90),('CUBIERTA',(219,212,191),0,None,10),('ACERO',(77,90,91),0,None,95),('BANOS',(209,179,197),0,None,20),('ROSA',(177,105,147),0,None,20)]
for name,col,alpha,texture,shine in spec:
 ma=r.Material();ma.Name=name;ma.DiffuseColor=(*col,255);ma.Transparency=alpha;ma.Shine=shine
 if texture:
  tex=r.Texture();tex.FileName=str((T/(texture+'.png')).resolve());tex.Enabled=True;ma.SetBitmapTexture(tex)
 mats[name]=out.Materials.Add(ma)
for l in old.Layers:
 ll=r.Layer();ll.Name=l.Name;ll.Color=l.Color;ll.Visible=l.Visible;ll.RenderMaterialIndex=mats['SALVIA'];out.Layers.Add(ll)
# upper wall extensions hide with roof in editing state
l=r.Layer();l.Name='13_CIERRES_SUPERIORES_OCULTAR_CON_CUBIERTA';l.Color=(114,158,133,255);l.Visible=False;upper=out.Layers.Add(l)
floors=[o.Geometry.GetBoundingBox() for o in old.Objects if o.Attributes.Name and o.Attributes.Name.startswith('Suelo completo')];bb=floors[0];cx=(bb.Min.X+bb.Max.X)/2;cy=(bb.Min.Y+bb.Max.Y)/2;xf=r.Transform.Translation(-cx,-cy,0)
for o in old.Objects:
 g=o.Geometry.Duplicate();a=r.ObjectAttributes();a.LayerIndex=o.Attributes.LayerIndex;a.Name=o.Attributes.Name;name=a.Name or '';layer=old.Layers.FindIndex(a.LayerIndex).Name
 # use explicit Breps to avoid ambiguous lightweight-extrusion preview caches
 if isinstance(g,r.Extrusion):g=g.ToBrep(True)
 if layer=='09_GUIAS_FLUJO':continue
 if '10_P03' in layer or '11_PERIMETRO' in layer:
  continue # supplied as separate file later, no references hanging above main unit
 mat='SALVIA'
 if layer=='01_SUELO':mat='ROBLE'
 elif layer=='03_COLCHONES':mat='LINO'
 elif layer=='04_MESAS_RESERVAS':mat='ACERO' if 'pata' in name else 'TURQUESA'
 elif layer=='05_ARMARIOS_RESERVAS':mat='CORCHO' if 'panel' in name else 'ROSA'
 elif layer in ['06_VIDRIOS','08_CUBIERTA_LUCERNARIO']:mat='VIDRIO'
 elif layer=='07_CUBIERTA':mat='CUBIERTA'
 elif layer=='12_BANOS_RESERVAS':mat='BANOS'
 if name=='Cierre pared hasta cubierta':a.LayerIndex=upper
 a.MaterialIndex=mats[mat];a.MaterialSource=r.ObjectMaterialSource.MaterialFromObject;a.ColorSource=r.ObjectColorSource.ColorFromMaterial;a.SetUserString('Material',mat);g.Transform(xf);out.Objects.Add(g,a)
# active viewport and named views, tightly framed at origin
for name,loc,tgt in [('01_INTERIOR',(17,-21,20),(0,0,0)),('02_PLANTA',(0,0,26),(0,0,0)),('03_NORTE',(17,20,16),(0,0,1))]:
 v=r.ViewInfo();v.Name=name;vp=v.Viewport;vp.SetCameraLocation(r.Point3d(*loc));vp.SetCameraDirection(r.Vector3d(*(tgt[i]-loc[i] for i in range(3))));vp.SetCameraUp(r.Vector3d(0,1,0) if 'PLANTA' in name else r.Vector3d(0,0,1));vp.TargetPoint=r.Point3d(*tgt);vp.ChangeToParallelProjection(True);vp.Extents(.85,r.BoundingBox(r.Point3d(-7.8,-6,-.2),r.Point3d(7.8,6,4)));out.NamedViews.Add(v)
 if name=='01_INTERIOR':out.Views.Add(v)
for l in out.Layers:
 if l.Name in ['07_CUBIERTA','08_CUBIERTA_LUCERNARIO','06_VIDRIOS']:l.Visible=False
assert out.Write(str(P/'P02_INTERIOR_MATERIALES_000.3dm'),8)
for l in out.Layers:
 if l.Name in ['07_CUBIERTA','08_CUBIERTA_LUCERNARIO','06_VIDRIOS'] or l.Index==upper:l.Visible=True
assert out.Write(str(P/'P02_COMPLETA_MATERIALES_000.3dm'),8)
for f in P.glob('P02*.3dm'):
 if f.name.startswith('._'):continue
 check=r.File3dm.Read(str(f));assert sum(not o.Geometry.IsValid for o in check.Objects)==0
 # floor center is origin, finished top at0
 fs=[o.Geometry.GetBoundingBox() for o in check.Objects if (o.Attributes.Name or '').startswith('Suelo completo')];b=fs[0];assert abs(b.Min.X+b.Max.X)<1e-5 and abs(b.Min.Y+b.Max.Y)<1e-5 and abs(b.Max.Z)<1e-5
(P/'VERIFICACION.json').write_text(json.dumps({'translation':[-cx,-cy,0],'origin':'Centro de caja de suelo X/Y; acabado suelo Z0','objects':len(out.Objects),'materials':len(out.Materials),'invalid':0,'floating_reference_platforms_removed_from_main':True},indent=2));print('MATERIALES_Y_ORIGEN_VERIFICADOS',len(out.Objects))
