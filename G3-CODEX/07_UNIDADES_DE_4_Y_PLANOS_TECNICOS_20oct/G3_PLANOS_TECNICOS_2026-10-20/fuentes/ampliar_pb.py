from pathlib import Path
import json,math,uuid
import rhino3dm as r
from shapely.geometry import Polygon,Point,LineString,box,shape
from shapely.geometry.polygon import orient
from shapely.affinity import rotate,translate
from shapely.ops import unary_union
from shapely import wkt
P=Path(__file__).resolve().parents[1];F=P/'modelos/E02_REVISION_TECNICA.3dm'
m=r.File3dm.Read(str(F))
for ob in list(m.Objects):
    la=m.Layers.FindIndex(ob.Attributes.LayerIndex).Name
    if la in ['25_PUBLICO_FIJO','26_ESTUDIO_DIARIO','27_EXPOSICION_DOMINGO','29_AGUA_Y_PAISAJE'] or ob.Attributes.Name.startswith(('Envolvente publica','Carpinteria publica','Antepecho publico','Dintel publico','Dintel acceso publico','Cubierta publica','Pavimento publico','Corredera publica','Pavimento continuo PB','Lucernario publico')):
        m.Objects.Delete(ob.Attributes.Id)
parcel=shape(json.loads((P.parent/'G3_MODELOS_HERENCIA_MACARRA_2026-10-19/fuentes/PARCELA_REAL.geojson').read_text())['geometry'])
def pieces(g):return [g] if g.geom_type=='Polygon' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']
def li(name):
    la=next((l for l in m.Layers if l.Name==name),None)
    if la:return la.Index
    la=r.Layer();la.Name=name;la.Color=(0,0,0,255);idx=m.Layers.Add(la)
    if name.startswith('27_'):m.Layers[idx].Visible=False
    return idx
L={k:li(k) for k in ['00_SUELO','01_MUROS','06_VIDRIO','13_METAL','17_CUBIERTA_TERMICA','22_PUERTAS','25_PUBLICO_FIJO','26_ESTUDIO_DIARIO','27_EXPOSICION_DOMINGO','29_AGUA_Y_PAISAJE']}
inventory=[];obstacles=[]
def solid(g,z,h,layer,name,obstacle=False):
    assert parcel.buffer(.005).covers(g),('fuera parcela',name,round(g.difference(parcel).area,6))
    for p in pieces(g):
        if p.area<1e-7:continue
        p=orient(p.simplify(.0005,preserve_topology=True),sign=1)
        cv=lambda ring:r.PolylineCurve([r.Point3d(x,y,0) for x,y in ring.coords])
        e=r.Extrusion.Create(cv(p.exterior),h,True)
        for ho in p.interiors:assert e.AddInnerProfile(cv(ho))
        assert e is not None;e.Transform(r.Transform.Translation(0,0,z));assert e.IsSolid and e.IsValid
        a=r.ObjectAttributes();a.LayerIndex=L[layer];a.Name=name;a.SetUserString('Estado','Programa PB de anteproyecto; geometria medida, sin verificacion normativa ni estructural')
        m.Objects.AddExtrusion(e,a)
    inventory.append({'name':name,'layer':layer,'z':z,'height':h,'footprint':g.wkt})
    if obstacle:obstacles.append(g)
def chair(x,y,layer='25_PUBLICO_FIJO',name='Silla publica'):
    seat=Point(x,y).buffer(.22,quad_segs=24);solid(seat,.43,.04,layer,name,True)
    for dx,dy in [(-.13,-.13),(.13,-.13),(-.13,.13),(.13,.13)]:solid(box(x+dx-.015,y+dy-.015,x+dx+.015,y+dy+.015),0,.43,layer,'Pata '+name)
def table(x,y,w,d,layer,name):
    top=box(x-w/2,y-d/2,x+w/2,y+d/2);solid(top,.74,.04,layer,name,True)
    for dx in [-w/2+.10,w/2-.10]:
        for dy in [-d/2+.10,d/2-.10]:solid(box(x+dx-.025,y+dy-.025,x+dx+.025,y+dy+.025),0,.74,layer,'Apoyo '+name)
def enclosed(region,doorcut,windows,name,skylights):
    full=region.boundary.buffer(.06);opaque=full.difference(doorcut).difference(windows)
    solid(region,-.10,.10,'00_SUELO','Pavimento publico '+name)
    solid(opaque,0,2.85,'01_MUROS','Envolvente publica '+name,True)
    glazing=full.intersection(windows).difference(doorcut)
    solid(glazing,.45,1.95,'06_VIDRIO','Carpinteria publica '+name)
    solid(glazing,0,.45,'01_MUROS','Antepecho publico '+name,True)
    solid(glazing,2.4,.45,'01_MUROS','Dintel publico '+name)
    solid(full.intersection(doorcut),2.3,.55,'01_MUROS','Dintel acceso publico '+name)
    holes=unary_union(skylights)
    assert region.buffer(-.10).covers(holes)
    solid(region.difference(holes),2.85,.15,'17_CUBIERTA_TERMICA','Cubierta publica '+name)
    for hole in skylights:
        solid(hole.boundary.buffer(.025),2.85,.15,'13_METAL','Lucernario publico / cerco '+name)
        solid(hole,2.98,.02,'06_VIDRIO','Lucernario publico / vidrio '+name)

# Replace the former small care box with the library's enclosing north edge;
# retain the upper housing and vertical core exactly in their positions.
for ob in list(m.Objects):
    n=ob.Attributes.Name
    if n.startswith(('Cuidados y conversacion reservada','Techo cuidados PB')):
        m.Objects.Delete(ob.Attributes.Id)
    elif n.startswith(('Banco de taller colectivo','Apoyo banco taller')) and ob.Geometry.GetBoundingBox().Min.X>26:
        m.Objects.Delete(ob.Attributes.Id)

library=parcel.buffer(-.22).intersection(box(21.65,5.0,31.2,13.0))
libdoor=box(25.30,4.7,26.70,5.30)
libwin=box(22.30,4.8,30.70,5.20)
enclosed(library,libdoor,libwin,'biblioteca',[box(24.0,9.6,25.0,10.8),box(28.0,7.6,29.0,8.8)])
solid(box(25.3,4.985,26.7,5.015),0,2.3,'22_PUERTAS','Corredera publica biblioteca')
lib_shelf=LineString([(22.50,11.65),(30.40,8.60)]).buffer(.20,cap_style=2).intersection(library.buffer(-.15))
solid(lib_shelf,0,1.90,'25_PUBLICO_FIJO','Libreria siguiendo borde norte',True)
solid(box(21.82,5.65,22.18,8.4),0,1.9,'25_PUBLICO_FIJO','Estanteria de intercambio',True)
for x,y in [(23.9,7.2),(28.6,6.6)]:
    table(x,y,1.40,.75,'25_PUBLICO_FIJO','Mesa lectura biblioteca')
    chair(x,y-.80);chair(x,y+.80)

study=parcel.buffer(-.22).intersection(box(53.20,-6.1,62,2.55))
studydoor=box(52.9,-2.70,53.5,-1.10)
studywin=box(52.95,-5.2,53.45,1.9)
enclosed(study,studydoor,studywin,'estudio exposicion',[box(54.65,-2.60,55.55,-.80),box(58.35,-2.60,59.25,-.80)])
solid(box(53.185,-2.7,53.215,-1.1),0,2.3,'22_PUERTAS','Corredera publica estudio')
solid(box(60.50,-5.30,61.10,-2.95),0,2.10,'25_PUBLICO_FIJO','Almacen paneles y mesas plegables',True)
for x in [55.1,58.8]:
    for y in [-4.0,0.0]:
        table(x,y,1.60,.80,'26_ESTUDIO_DIARIO','Mesa plegable sala estudio')
        chair(x,y-.85,'26_ESTUDIO_DIARIO','Silla sala estudio');chair(x,y+.85,'26_ESTUDIO_DIARIO','Silla sala estudio')
for j,(x,y,angle) in enumerate([(55.1,-4.0,25),(58.8,-4.0,-25),(55.1,0,25),(58.8,0,-25),(23.6,3.5,0),(29.2,3.5,0)]):
    panel=translate(rotate(box(-.7,-.04,.7,.04),angle,origin=(0,0)),x,y)
    solid(panel,.10,1.85,'27_EXPOSICION_DOMINGO','Panel movil exposicion '+str(j+1))
    foot=translate(rotate(box(-.45,-.25,.45,.25),angle,origin=(0,0)),x,y)
    solid(foot,0,.06,'27_EXPOSICION_DOMINGO','Base panel exposicion',True)
# Folded tabletop stack is physically present in the Sunday state.
solid(box(60.57,-5.2,61.0,-3.45),.10,.70,'27_EXPOSICION_DOMINGO','Mesas plegadas en almacen')

# Open coworking under the raised housing, not a second enclosed box.
solid(box(14.3,5.50,20.25,6.25),.74,.04,'25_PUBLICO_FIJO','Barra coworking cuatro puestos',True)
for x in [14.45,17.25,20.10]:solid(box(x,5.55,x+.06,6.20),0,.74,'13_METAL','Apoyo barra coworking')
for x in [15.05,16.50,17.95,19.40]:chair(x,4.80,name='Silla coworking')
solid(box(13.30,2.85,13.85,4.25),0,1.75,'25_PUBLICO_FIJO','Armario intercambio vecinal',True)
table(36.3,4.00,1.4,.75,'25_PUBLICO_FIJO','Mesa punto vecinal')
chair(36.3,3.2);chair(36.3,4.8)
table(22.4,-5.25,1.30,.80,'25_PUBLICO_FIJO','Banco reparacion y costura')
solid(box(21.5,-6.70,24.0,-6.30),0,1.80,'25_PUBLICO_FIJO','Herramientas compartidas',True)

# A shallow recirculating-water feature and three discontinuous curved seats;
# gaps face the public route. No new service pipe crosses a facade opening.
c=Point(18.0,-3.1);outer=c.buffer(.85,quad_segs=80);inner=c.buffer(.72,quad_segs=80)
solid(outer.difference(inner),0,.28,'29_AGUA_Y_PAISAJE','Borde fuente circuito cerrado',True)
solid(inner,.18,.012,'29_AGUA_Y_PAISAJE','Plano agua fuente')
solid(c.buffer(.055),-.20,.38,'29_AGUA_Y_PAISAJE','Reserva acometida fuente bajo pavimento')
for j,(a,b) in enumerate([(-70,15),(35,110),(230,285)]):
    angles=[math.radians(a+(b-a)*k/64) for k in range(65)]
    coords=[(c.x+1.85*math.cos(t),c.y+1.85*math.sin(t)) for t in angles]+[(c.x+1.42*math.cos(t),c.y+1.42*math.sin(t)) for t in reversed(angles)]
    seat=Polygon(coords);solid(seat,0,.44,'29_AGUA_Y_PAISAJE','Banco curvo fuente '+str(j+1),True)

# Check a continuous 1.50 m public route; no occupancy certification is inferred.
solid(parcel,-.12,.12,'00_SUELO','Pavimento continuo PB a cota cero')
route=LineString([(12.35,1.0),(18.0,1.0),(26.0,1.0),(34.0,1.0),(41.0,.7),(50.7,-1.0),(53.2,-1.9),(57.2,-1.9)])
route_lib=LineString([(26.,1.),(26.,5.0),(26.,6.1)])
walks=unary_union([route.buffer(.75,cap_style=2),route_lib.buffer(.65,cap_style=2)])
bad=[]
for ob in inventory:
    if ob['layer']=='27_EXPOSICION_DOMINGO' or ob['name'].startswith(('Cubierta','Dintel','Corredera','Carpinteria','Pavimento','Lucernario')):continue
    g=wkt.loads(ob['footprint'])
    if ob['z']>=2.3:continue
    overlap=g.intersection(walks).area
    if overlap>.005:bad.append({'name':ob['name'],'overlap_m2':round(overlap,4)})
assert not bad,bad
assert m.Write(str(F),8)
meta={'library_area_m2':round(library.area,2),'study_exhibition_area_m2':round(study.area,2),'cowork_seats':4,'library_reading_seats':4,'study_seats':8,'public_route_nominal_width_m':1.50,'library_branch_nominal_width_m':1.30,'new_programme_only_route_collisions':bad,'route':list(route.coords),'library_route':list(route_lib.coords),'library':library.wkt,'study':study.wkt,'inventory':inventory,'public_doors':[{'type':'sliding','id':'LIB','p0':[25.3,5.0],'p1':[26.7,5.0],'pocket_end':[28.1,5.0]},{'type':'sliding','id':'EST','p0':[53.2,-2.7],'p1':[53.2,-1.1],'pocket_end':[53.2,.5]}],'scope':'Geometria nueva de anteproyecto. El corredor se comprueba contra el nuevo programa; falta reauditar todos los obstaculos existentes y normativa. Sin calculo estructural o de instalaciones.'}
(P/'verificacion/PROGRAMA_PUBLICO_PB.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in meta.items() if k not in ['inventory','library','study','route','library_route','public_doors']},ensure_ascii=False))
