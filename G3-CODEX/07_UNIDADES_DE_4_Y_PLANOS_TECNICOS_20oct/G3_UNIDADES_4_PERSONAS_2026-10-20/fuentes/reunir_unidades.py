from pathlib import Path
import sys,json,contextlib,io,collections,hashlib
import rhino3dm as r
from shapely.geometry.polygon import orient

P=Path(__file__).resolve().parents[1]
SRC=P.parent/'G3_MODELOS_HERENCIA_MACARRA_2026-10-19'
sys.path.insert(0,str(SRC/'fuentes/base_geometry/fuentes'))
with contextlib.redirect_stdout(io.StringIO()):import geometria as G
m=r.File3dm();m.Settings.ModelUnitSystem=r.UnitSystem.Meters
m.Settings.ModelAbsoluteTolerance=.001
report=[]

def thick_mesh(g,thickness):
    # Weld identical coordinates before identifying the genuine boundary edges.
    vertices=[];lookup={};remap={}
    for i,v in enumerate(g.Vertices):
        key=tuple(round(float(x),6) for x in (v.X,v.Y,v.Z))
        if key not in lookup:lookup[key]=len(vertices);vertices.append(key)
        remap[i]=lookup[key]
    faces=[];edges=collections.Counter();direct={}
    for f in g.Faces:
        ids=[remap[x] for x in (f[:3] if f[2]==f[3] else f)]
        faces.append(ids)
        for a,b in zip(ids,ids[1:]+ids[:1]):edges[tuple(sorted((a,b)))]+=1;direct[tuple(sorted((a,b)))]=(a,b)
    n=len(vertices);out=r.Mesh()
    for x,y,z in vertices:out.Vertices.Add(x,y,z)
    for x,y,z in vertices:out.Vertices.Add(x,y,z-thickness)
    for ids in faces:
        out.Faces.AddFace(*ids);out.Faces.AddFace(*[i+n for i in reversed(ids)])
    for edge,count in edges.items():
        if count==1:
            a,b=direct[edge];out.Faces.AddFace(b,a,a+n,b+n)
    out.Normals.ComputeNormals();out.Compact()
    assert out.IsValid and out.IsClosed,('cubierta abierta',thickness)
    return out

def addsolid(poly,z,h,layer,name,T):
    for p in G.polys(poly):
        if p.area<1e-7:continue
        p=orient(p,sign=1)
        cr=lambda ring:r.PolylineCurve([r.Point3d(x,y,0) for x,y in ring.coords])
        e=r.Extrusion.Create(cr(p.exterior),h,True)
        for ring in p.interiors:assert e.AddInnerProfile(cr(ring))
        e.Transform(r.Transform.Translation(0,0,z));e.Transform(T)
        a=r.ObjectAttributes();a.LayerIndex=layer;a.Name=name
        m.Objects.AddExtrusion(e,a)

def view(name,bounds,mode):
    x,y,X,Y=bounds;cx=(x+X)/2;cy=(y+Y)/2;span=max(X-x,Y-y)
    v=r.ViewInfo();v.Name=name;vp=v.Viewport
    if mode=='planta':loc=(cx,cy,span*2);up=(0,1,0);target=(cx,cy,0)
    elif mode=='alzado':loc=(cx,cy-span*2,2);up=(0,0,1);target=(cx,cy,2)
    else:loc=(cx+span*.8,cy-span,span*.85);up=(0,0,1);target=(cx,cy,1.4)
    vp.SetCameraLocation(r.Point3d(*loc));vp.SetCameraDirection(r.Vector3d(*[target[i]-loc[i] for i in range(3)]));vp.SetCameraUp(r.Vector3d(*up));vp.TargetPoint=r.Point3d(*target);vp.ChangeToParallelProjection(True)
    vp.Extents(.15,r.BoundingBox(r.Point3d(x-1,y-1,-.6),r.Point3d(X+1,Y+1,5.1)))
    m.NamedViews.Add(v)
    return v

for i,code in enumerate(['V01_U','V02_U','V03_U']):
    f=next(f for f in G.F if f['audit']['codigo']==code)
    assert len(f['rooms'])==4
    src=r.File3dm.Read(str(SRC/'modelos'/(code+'_3D.3dm')))
    root=r.Layer();root.Name=f'{code[:3]}__4_PERSONAS';parent=m.Layers.Add(root);pid=m.Layers[parent].Id
    mats={j:m.Materials.Add(mat) for j,mat in enumerate(src.Materials)};layers={}
    for l in src.Layers:
        if l.Name in ['90_CONTEXTO','91_PARCELA','19_SOPORTE_PB','20_COMUN_EDIFICIO','21_NUCLEO_VERTICAL']:continue
        la=r.Layer();la.Name=l.Name;la.Color=l.Color;la.ParentLayerId=pid;la.Visible=True
        la.PlotWeight=.35 if l.Name=='01_MUROS' else .13
        layers[l.Index]=m.Layers.Add(la)
    x,y,X,Y=f['floor'].bounds;tx=i*28-x;ty=-y;T=r.Transform.Translation(tx,ty,0)
    roof_count=0
    for o in src.Objects:
        if o.Attributes.LayerIndex not in layers:continue
        g=o.Geometry.Duplicate();lname=src.Layers.FindIndex(o.Attributes.LayerIndex).Name
        # The secondary textile remains a membrane. The weather roof is a closed
        # faceted mesh, so Rhino sections have an actual roof thickness.
        if lname=='18_LUCERNARIOS' and isinstance(g,r.Mesh):
            g=thick_mesh(g,.12)
            assert g.IsValid and g.IsClosed
            roof_count+=1
        g.Transform(T)
        a=r.ObjectAttributes();a.Name=o.Attributes.Name;a.LayerIndex=layers[o.Attributes.LayerIndex]
        a.ColorSource=r.ObjectColorSource.ColorFromObject;a.ObjectColor=o.Attributes.ObjectColor
        a.MaterialSource=r.ObjectMaterialSource.MaterialFromObject;a.MaterialIndex=mats.get(o.Attributes.MaterialIndex,-1)
        a.SetUserString('Propuesta',code);a.SetUserString('Residentes','4');a.SetUserString('Cota_pavimento','0.00 m')
        m.Objects.Add(g,a)
    wall=next(idx for old,idx in layers.items() if src.Layers.FindIndex(old).Name=='01_MUROS')
    # Common glazing was already modelled between .45 and 2.40. Complete its
    # supporting sill and overhead wall without touching the clear doorways.
    for win in f['wc']:
        footprint=win.intersection(f['walls'])
        addsolid(footprint,0,.45,wall,'Antepecho ventana comun',T)
        addsolid(footprint,2.40,.35,wall,'Dintel ventana comun',T)
    addsolid(f['entry']['cut'].intersection(f['walls']),2.15,.60,wall,'Dintel acceso principal libre hasta 2.15m',T)
    guide=r.Layer();guide.Name='99_REFERENCIAS_NO_IMPRIMIR';guide.ParentLayerId=pid;guide.Visible=False;guide.PlotWeight=-1;gi=m.Layers.Add(guide)
    a=r.ObjectAttributes();a.LayerIndex=gi
    m.Objects.AddTextDot(f'{code[:3]} | 4 personas | suelo {f["floor"].area:.2f} m2',r.Point3d(i*28+5,-1.5,0),a)
    bounds=(x+tx,y+ty,X+tx,Y+ty)
    for mode in ['planta','axo','alzado']:view(code[:3]+'_'+mode.upper(),bounds,mode)
    report.append({'propuesta':code,'residentes':4,'cota_pavimento':0,'suelo_m2':round(f['floor'].area,2),'traslacion':[tx,ty,0],'cubiertas_comunes_solidas':roof_count,'control_2d_heredado':f['audit']})

v=view('00_TODAS_CUBIERTAS',(0,0,74,18),'axo');m.Views.Add(v)
m.Strings['LEEME']='Tres propuestas distintas, cuatro residentes cada una, separadas y a cota 0. Cubiertas visibles. Apagar 08_COSTILLAS,09_MEMBRANAS,10_CABLES,17_CUBIERTA_TERMICA,18_LUCERNARIOS por propuesta para planta interior. Modelo de estudio, no proyecto ejecutivo.'
dest=P/'UNIDADES_4_PERSONAS_TODAS_CON_CUBIERTA.3dm'
assert m.Write(str(dest),8)
check=r.File3dm.Read(str(dest));bad=[o.Attributes.Name for o in check.Objects if not o.Geometry.IsValid]
assert not bad,bad
assert all(o.Geometry.IsSolid for o in check.Objects if isinstance(o.Geometry,(r.Extrusion,r.Brep)))
result={'archivo':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'objetos':len(check.Objects),'invalidos':bad,'propuestas':report,'vistas_guardadas':[v.Name for v in check.NamedViews]}
(P/'verificacion/CONTROL.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='propuestas'},ensure_ascii=False))
