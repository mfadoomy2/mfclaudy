from pathlib import Path
import sys,json,math,contextlib,io
import rhino3dm as r
from shapely.geometry import Polygon,Point,LineString,box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union,polygonize
from shapely.affinity import translate,rotate,scale

P=Path(__file__).resolve().parents[1];OLD=P.parent/'G3_MODELOS_HERENCIA_MACARRA_2026-10-19'
sys.path.insert(0,str(OLD/'fuentes/base_geometry/fuentes'))
with contextlib.redirect_stdout(io.StringIO()):import geometria as G
DATA=json.loads((P/'verificacion/EXTRACCION_RHINO.json').read_text())
UINFO=json.loads((P.parent/'G3_UNIDADES_4_PERSONAS_2026-10-20/verificacion/CONTROL.json').read_text())['propuestas']
SITE=json.loads((OLD/'fuentes/ENCAJE_PARCELA.json').read_text())

def clean(p):return p if p.is_valid else p.buffer(0)
def region(ob):
    if ob['profiles']:
        ps=[p for p in ob['profiles'] if len(p)>3 and Point(p[0][:2]).distance(Point(p[-1][:2]))<.002]
        if ps:return clean(Polygon([q[:2] for q in ps[0]],[[q[:2] for q in p] for p in ps[1:]]))
    caps=[]
    for face in ob['caps']:
        outer=next((p['points'] for p in face if p['outer']),None)
        if outer:caps.append(clean(Polygon([q[:2] for q in outer],[[q[:2] for q in p['points']] for p in face if not p['outer']])))
    if caps:return unary_union(caps)
    out=Polygon();lines=[]
    for pp in ob['sections']:
        if len(pp)>3 and Point(pp[0][:2]).distance(Point(pp[-1][:2]))<.002:out=out.symmetric_difference(clean(Polygon([q[:2] for q in pp])))
        elif len(pp)>1:lines.append(LineString([q[:2] for q in pp]))
    if lines:out=out.union(unary_union(list(polygonize(unary_union(lines)))))
    return out

def copyattr(layer,name,color=(0,0,0,255)):
    a=r.ObjectAttributes();a.LayerIndex=layer;a.Name=name;a.ObjectColor=color;a.ColorSource=r.ObjectColorSource.ColorFromObject
    return a
def solid(m,poly,z,h,layer,name):
    for p in G.polys(clean(poly)):
        if p.area<1e-8:continue
        p=p.simplify(.0005,preserve_topology=True)
        p=Polygon(p.exterior,[ring.coords for ring in p.interiors if Polygon(ring).area>1e-6])
        p=orient(p,sign=1)
        cr=lambda ring:r.PolylineCurve([r.Point3d(x,y,0) for x,y in ring.coords])
        ex=r.Extrusion.Create(cr(p.exterior),h,True)
        if ex is None:
            if p.area<1e-6:continue
            raise ValueError((name,p.area,p.bounds,cr(p.exterior).IsValid))
        for hole in p.interiors:assert ex.AddInnerProfile(cr(hole))
        ex.Transform(r.Transform.Translation(0,0,z));assert ex.IsValid and ex.IsSolid
        m.Objects.AddExtrusion(ex,copyattr(layer,name))

META=[]
for kind,src,extract in [('U','TRES_UNIDADES_ESTADO_USUARIO.3dm',DATA[0]),('E02','E02_ESTADO_USUARIO.3dm',DATA[1])]:
    m=r.File3dm.Read(str(P/'instantaneas'/src));levels=0 if kind=='U' else 4.2
    # Keep the native model and user geometry; the separate snapshot retains
    # transient Make2D/silhouette curves which are not part of the 3D revision.
    remove=[o.Attributes.Id for o in m.Objects if isinstance(o.Geometry,(r.Curve,r.TextDot))]
    for id in remove:m.Objects.Delete(id)
    cases=['V01_U','V02_U','V03_U'] if kind=='U' else ['V01_S']
    for j,code in enumerate(cases):
        f=next(f for f in G.F if f['audit']['codigo']==code)
        if kind=='U':
            tx,ty,_=UINFO[j]['traslacion'];T=lambda g,tx=tx,ty=ty:translate(g,tx,ty)
            root=next(l for l in m.Layers if l.Name.startswith(code[:3]+'__'))
            objs=[o for o in extract['objects'] if o['parents'][0].startswith(code[:3]+'__')]
        else:
            row=next(a for a in SITE['resultados'] if a['codigo']==code);cent=f['floor'].buffer(.12).centroid;xx,yy=row['centro_local_m'];ang=row['rotacion_grados']
            T=lambda g,cx=cent.x,cy=cent.y,xx=xx,yy=yy,ang=ang:translate(rotate(translate(g,-cx,-cy),ang,origin=(0,0)),xx,yy)
            root=None;objs=extract['objects']
        def layer(name,color=(100,100,100,255)):
            found=next((l for l in m.Layers if l.Name==name and (root is None or l.ParentLayerId==root.Id)),None)
            if found:return found.Index
            l=r.Layer();l.Name=name;l.Color=color
            if root:l.ParentLayerId=root.Id
            return m.Layers.Add(l)
        wallidx=layer('01_MUROS');dooridx=layer('22_PUERTAS');shaftidx=layer('23_PATINILLOS');mepidx=layer('24_MONTANTES_EN_SERVICIOS')
        if kind=='U':
            floor=unary_union([region(o) for o in objs if o['name'].startswith('Suelo continuo')])
        else:floor=unary_union([region(o) for o in objs if o['name'].startswith('Suelo continuo')])
        basewalls=[o for o in objs if o['name'].startswith('Muros con huecos reales')]
        W=unary_union([region(o) for o in basewalls])
        assert not W.is_empty
        service=unary_union([T(b['floor']) for b in f['banks']]);priv=T(f['priv'])
        patch=service.buffer(.14).difference(priv.buffer(.015))
        baths=[];newwalls=[];shafts=[];doors=[]
        cutdoors=T(unary_union(f['doors']))
        if kind=='E02':
            bentry=max(f['banks'],key=lambda b:T(b['floor']).centroid.x)
            ecut=T(bentry['T'](box(2.,-.52,2.42,.52)));cutdoors=cutdoors.union(ecut)
        for bi,b in enumerate(f['banks']):
            bt=lambda g,b=b:T(b['T'](g))
            # The wet-room perimeter reaches the actual enclosing contour;
            # the former nested rear/side shells are removed.
            for s in [1,-1]:
                vol=bt(b['floor'].intersection(b['T'](box(-2,.60,4,4))) if False else box(-2,.60,4,4)) if s==1 else bt(box(-2,-4,4,-.60))
                vol=vol.intersection(T(b['floor']))
                baths.append(vol);newwalls.append(vol.boundary.buffer(.06))
            for k,(sx,sy) in enumerate([(1.97,2.28),(.03,-2.28)]):
                pp=bt(Point(sx,sy));foot=bt(box(sx-.09,sy-.09,sx+.09,sy+.09))
                assert baths[-2+k].buffer(-.02).covers(foot)
                windows=T(unary_union(f['windows']))
                assert foot.distance(windows)>.12
                shell=foot.difference(foot.buffer(-.025));solid(m,shell,levels,2.75,shaftidx,'Patinillo integrado P'+str(bi*2+k+1))
                pipe=pp.buffer(.055,quad_segs=24);solid(m,pipe,levels-.18,3.0,mepidx,'Bajante DN110 en patinillo / reserva de trazado')
                af=bt(Point(sx+.05,sy+.05));solid(m,af.buffer(.0125),levels-.18,3.0,mepidx,'Montante AF en patinillo / sin dimensionado hidraulico')
                shafts.append({'id':'P'+str(bi*2+k+1),'foot':foot.wkt,'center':list(pp.coords)[0],'window_clearance_m':round(foot.distance(windows),3)})
            # Replace the round proxy with an actual measured pan footprint:
            # 0.38 x 0.65 including cistern; clear front to basin is 0.62 m.
            sanitaryidx=layer('15_BANOS')
            for cx,cy,sign in [(1.60,1.98,1),(.40,-1.98,-1)]:
                pan=scale(Point(cx,cy).buffer(1,quad_segs=40),xfact=.19,yfact=.24,origin=(cx,cy))
                inner=scale(Point(cx,cy).buffer(1,quad_segs=40),xfact=.14,yfact=.175,origin=(cx,cy))
                cis=box(cx-.19,2.22,cx+.19,2.39) if sign==1 else box(cx-.19,-2.39,cx+.19,-2.22)
                base=scale(Point(cx,cy).buffer(1,quad_segs=24),xfact=.10,yfact=.165,origin=(cx,cy))
                solid(m,bt(base),levels,.32,sanitaryidx,'Sanitario WC / apoyo')
                solid(m,bt(pan),levels+.32,.025,sanitaryidx,'Sanitario WC / fondo')
                solid(m,bt(pan.difference(inner)),levels+.345,.075,sanitaryidx,'Sanitario WC / aro')
                solid(m,bt(cis),levels+.40,.45,sanitaryidx,'Sanitario WC / cisterna')
            # Pocket sliding doors keep the compact wet rooms free of a swing
            # that otherwise crosses the shower footprint.
            for k,(x0,x1,yy,pocket) in enumerate([(.15,1.05,.60,1),(.95,1.85,-.60,-1)]):
                leaf=bt(box(x0,yy-.018,x1,yy+.018));solid(m,leaf,levels,2.10,dooridx,'Corredera bano B'+str(bi*2+k+1))
                a=bt(Point(x0,yy));z=bt(Point(x1,yy));end=bt(Point(x1+.90,yy) if pocket==1 else Point(x0-.90,yy))
                doors.append({'type':'sliding','p0':list(a.coords)[0],'p1':list(z.coords)[0],'pocket_end':list(end.coords)[0],'id':'B'+str(bi*2+k+1)})
        newwalls.append(floor.boundary.buffer(.06).intersection(service.buffer(.14)))
        Wnew=W.difference(patch).union(unary_union(newwalls).intersection(patch).difference(cutdoors))
        # Preserve all already-modelled wall openings away from the service
        # adjustment; only this measured footprint is rebuilt as closed solids.
        for o in basewalls:m.Objects.Delete(r.UUID(o['id']) if hasattr(r,'UUID') else __import__('uuid').UUID(o['id']))
        solid(m,Wnew,levels,2.75,wallidx,'Muros continuos revisados / banos integrados')
        local_bow=[]
        for room in f['rooms']:
            rt=lambda g,room=room:T(room['T'](G.tf(g,room['r'])))
            # A closed physical leaf is independent of the conventional open
            # swing symbol used in the measured plan.
            x,y,X,Y=G.DOOR.bounds;cy=(y+Y)/2
            hinge=rt(Point(x+.05,cy));tip=rt(Point(X-.05,cy));op=rt(Point(x+.05,cy+.90))
            leaf=LineString([hinge,tip]).buffer(.018,cap_style=2)
            solid(m,leaf,levels,2.10,dooridx,'Hoja dormitorio '+room['id'])
            doors.append({'type':'hinged','hinge':list(hinge.coords)[0],'closed':list(tip.coords)[0],'open':list(op.coords)[0],'id':room['id']})
            a=rt(Point(1.80,4.12));z=rt(Point(1.80,5.55));local_bow.append({'id':'S'+room['id'][1:],'p0':list(a.coords)[0],'p1':list(z.coords)[0]})
        # Actual entry node, same approach as the native model.
        if kind=='U':
            a=T(Point(f['entry']['inside']));b=T(Point(f['entry']['outside']));path=LineString([a,b]);pp=floor.boundary.intersection(path)
            candidates=[pp] if pp.geom_type=='Point' else [q for q in getattr(pp,'geoms',[]) if q.geom_type=='Point']
            c=min(candidates,key=lambda p:p.distance(a));dx,dy=b.x-a.x,b.y-a.y;norm=math.hypot(dx,dy);nx,ny=-dy/norm,dx/norm;width=1.20 if j<2 else 1.10
            p0=Point(c.x-nx*(width/2-.05),c.y-ny*(width/2-.05));p1=Point(c.x+nx*(width/2-.05),c.y+ny*(width/2-.05));po=Point(p0.x-dx/norm*(width-.10),p0.y-dy/norm*(width-.10))
        else:
            p0=T(bentry['T'](Point(2.18,-.47)));p1=T(bentry['T'](Point(2.18,.47)));po=T(bentry['T'](Point(1.24,-.47)))
        solid(m,LineString([p0,p1]).buffer(.018,cap_style=2),levels,2.10,dooridx,'Hoja acceso principal')
        doors.append({'type':'hinged','hinge':list(p0.coords)[0],'closed':list(p1.coords)[0],'open':list(po.coords)[0],'id':'E'})
        # A centreline only describes a reference datum. The entire unit is
        # explicitly checked before any global axis is called a symmetry.
        cx,cy=floor.centroid.coords[0]
        sx=floor.symmetric_difference(scale(floor,xfact=-1,yfact=1,origin=(cx,cy))).area
        sy=floor.symmetric_difference(scale(floor,xfact=1,yfact=-1,origin=(cx,cy))).area
        META.append({'code':code if kind=='U' else 'E02','level':levels,'floor':floor.wkt,'wall_cut':Wnew.wkt,'baths':[b.wkt for b in baths],'doors':doors,'shafts':shafts,'bow_axes':local_bow,'global_symmetry_x':sx<.001,'global_symmetry_y':sy<.001,'native_wall_area_before':W.area,'native_wall_area_after':Wnew.area,'source_objects':len(objs),'roof_not_redesigned':True})
    # Obsolete facade risers are removed throughout each native document;
    # the private bow seats and dining chairs are retained.
    deleted=[]
    for o in list(m.Objects):
        name=o.Attributes.Name.lower()
        if 'sofa' in name or 'sofá' in name or 'conducto energia visible propuesta' in name or 'bajante propuesta' in name or name.startswith('pie wc') or name.startswith('taza wc esquema'):
            deleted.append(o.Attributes.Name);m.Objects.Delete(o.Attributes.Id)
    if kind=='E02':
        # The open document still contained the older detached PB toilets.
        # Bring over only the already-revised continuous south service edge
        # from the latest saved E02; retain the user's housing, core and site.
        remove_prefix=('Aseo de uso comun en borde sur','WC PB esquematico','Banco de taller colectivo','Apoyo banco taller','Cocina de todo el edificio')
        for o in list(m.Objects):
            if o.Attributes.Name.startswith(remove_prefix):m.Objects.Delete(o.Attributes.Id)
        latest=r.File3dm.Read(str(OLD/'modelos/E02_COMUNA_INTERIOR.3dm'))
        add_prefix=('Banco de taller colectivo','Apoyo banco taller','Cocina integrada en franja sur','Almacenaje integrado con cocina','Pared continua de servicios sur','WC PB en borde','Techo continuo cocina','Techo de franja','Cubierta franja','Cubierta continua servicios')
        for ob in latest.Objects:
            if ob.Attributes.Name.startswith(add_prefix):
                lname=latest.Layers.FindIndex(ob.Attributes.LayerIndex).Name
                idx=next(l.Index for l in m.Layers if l.Name==lname)
                a=copyattr(idx,ob.Attributes.Name);m.Objects.Add(ob.Geometry.Duplicate(),a)
    for la in m.Layers:
        if la.Name in ['Make2D','Visible','Hidden','Curves','SceneSilhouetteCurves']:la.Visible=False
    dest=P/'modelos'/('TRES_UNIDADES_REVISION_TECNICA.3dm' if kind=='U' else 'E02_REVISION_TECNICA.3dm')
    assert m.Write(str(dest),8)
    ck=r.File3dm.Read(str(dest));bad=[o.Attributes.Name for o in ck.Objects if not o.Geometry.IsValid];assert not bad,bad
    print(dest.name,len(ck.Objects),'validos; retirados:',len(deleted))
(P/'verificacion/REVISION_GEOMETRICA.json').write_text(json.dumps(META,ensure_ascii=False,indent=2))
