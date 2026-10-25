from pathlib import Path
import json,math,sys,contextlib,io,re,shutil
import rhino3dm as r
from shapely.geometry import Polygon,Point,box,LineString
from shapely.affinity import translate,rotate
from shapely.ops import unary_union
from shapely.geometry.polygon import orient
from shapely import wkt
P=Path(__file__).resolve().parents[1];OLD=P.parent/'G3_MODELOS_HERENCIA_MACARRA_2026-10-19'
sys.path.insert(0,str(OLD/'fuentes/base_geometry/fuentes'))
with contextlib.redirect_stdout(io.StringIO()):import geometria as G
C=json.loads((P/'verificacion/COMPACTACION.json').read_text());D=json.loads((P/'verificacion/EXTRACCION_REVISION_RHINO.json').read_text());M=json.loads((P/'verificacion/REVISION_GEOMETRICA.json').read_text())
UINFO=json.loads((P.parent/'G3_UNIDADES_4_PERSONAS_2026-10-20/verificacion/CONTROL.json').read_text())['propuestas']
# Keep the previous measured revision intact and create a new, explicit iteration.
source=P/'modelos/TRES_UNIDADES_REVISION_TECNICA.3dm';m=r.File3dm.Read(str(source));report=[]
def reg(o):
 ps=[q for q in o['profiles'] if len(q)>3 and Point(q[0][:2]).distance(Point(q[-1][:2]))<.002]
 if ps:
  g=Polygon([q[:2] for q in ps[0]],[[q[:2] for q in p] for p in ps[1:]]);return g if g.is_valid else g.buffer(0)
 out=[]
 for face in o['caps']:
  p=next((a['points'] for a in face if a['outer']),None)
  if p:
   g=Polygon([q[:2] for q in p],[[q[:2] for q in a['points']] for a in face if not a['outer']]);out.append(g if g.is_valid else g.buffer(0))
 return unary_union(out)
def parts(g):return [g] if g.geom_type=='Polygon' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']
def add(g,z,h,layer,name):
 for p in parts(g):
  if p.area<1e-7:continue
  p=orient(p.simplify(.0005,True),sign=1);cv=lambda ring:r.PolylineCurve([r.Point3d(x,y,0) for x,y in ring.coords])
  e=r.Extrusion.Create(cv(p.exterior),h,True)
  for hole in p.interiors:assert e.AddInnerProfile(cv(hole))
  e.Transform(r.Transform.Translation(0,0,z));assert e.IsValid and e.IsSolid
  a=r.ObjectAttributes();a.LayerIndex=layer;a.Name=name;m.Objects.AddExtrusion(e,a)
for j,fam in enumerate(['V01','V02','V03']):
 c=C[fam];old=G.F[j];tx,ty,_=UINFO[j]['traslacion'];root=next(l for l in m.Layers if l.Name.startswith(fam+'__'));ls={l.Name:l.Index for l in m.Layers if l.ParentLayerId==root.Id};oblist=[o for o in m.Objects if o.Attributes.LayerIndex in ls.values()]
 loc=lambda g:translate(g,-tx,-ty);world=lambda g:translate(g,tx,ty)
 native=[o for o in D[0]['objects'] if o['parents'][0].startswith(fam+'__')];oldwalls=unary_union([loc(reg(o)) for o in native if o['layer']=='01_MUROS' and 'Muros continuos revisados' in o['name']])
 oldservice=unary_union([b['floor'] for b in old['banks']]);bdx,bdy=c['bank_delta'];service=translate(oldservice,bdx,bdy);oldwalls=translate(oldwalls.intersection(oldservice.buffer(.14)),bdx,bdy);private=unary_union([G.tf(G.ROOM,rr) for rr in c['rooms']]);patch=service.buffer(.14).difference(private.buffer(.015))
 walls=wkt.loads(c['solid']).difference(patch).union(oldwalls.intersection(patch))
 # Existing shafts and wet fixtures are retained at their measured size and location.
 roomd={f'H{i+1:02d}':(rr['q'][0]-old['rooms'][i]['r']['q'][0],rr['q'][1]-old['rooms'][i]['r']['q'][1]) for i,rr in enumerate(c['rooms'])}
 km=c['furniture_moves']['kitchen'];tm=c['furniture_moves']['table_chairs'];ko=c['furniture_moves']['kitchen_origin'];to=c['furniture_moves']['table_origin'];kp={'V01':(0,0),'V02':(0,.45),'V03':(-.4,.4)}[fam];tp=(0,-.55) if fam=='V02' else (0,0)
 for o in oblist:
  n=o.Attributes.Name;la=m.Layers.FindIndex(o.Attributes.LayerIndex).Name;rid=n[:3]
  if rid in roomd:
   dx,dy=roomd[rid];o.Geometry.Transform(r.Transform.Translation(dx,dy,0));continue
  if la in ['00_SUELO','01_MUROS','06_VIDRIO','07_ACERO','08_COSTILLAS','09_MEMBRANAS','10_CABLES','18_LUCERNARIOS']:
   m.Objects.Delete(o.Attributes.Id);continue
  if la=='17_CUBIERTA_TERMICA' and 'servicios' not in n:m.Objects.Delete(o.Attributes.Id);continue
  if la in ['15_BANOS','23_PATINILLOS','24_MONTANTES_EN_SERVICIOS'] or (la=='17_CUBIERTA_TERMICA' and 'servicios' in n) or (la=='22_PUERTAS' and n.startswith('Corredera bano')):
   o.Geometry.Transform(r.Transform.Translation(bdx,bdy,0));continue
  if n.startswith(('Mueble cocina','Encimera','Fregadero','Placa cocina')):par,org,pre=km,ko,kp
  elif n.startswith(('Mesa comun','Pata mesa comun','Asiento comedor','Pata silla')):par,org,pre=tm,to,tp
  else:continue
  o.Geometry.Transform(r.Transform.Translation(*pre,0));o.Geometry.Transform(r.Transform.Rotation(math.radians(par[2]),r.Vector3d(0,0,1),r.Point3d(org[0]+tx,org[1]+ty,0)));o.Geometry.Transform(r.Transform.Translation(par[0],par[1],0))
 floor=wkt.loads(c['floor']);add(world(floor),-.18,.18,ls['00_SUELO'],'Suelo continuo / redistribucion compacta')
 add(world(walls),0,2.75,ls['01_MUROS'],'Muros continuos / habitaciones recolocadas a tamano real')
 # Common glazed openings, below/above-cut spandrels and actual door lintels.
 wc=unary_union([wkt.loads(g) for g in c['windows'][4:]]).intersection(floor.boundary.buffer(.065))
 for name,z,h,la in [('Vidrio comun compacto',.90,1.45,'06_VIDRIO'),('Antepecho comun compacto',0,.90,'01_MUROS'),('Dintel comun compacto',2.35,.40,'01_MUROS')]:add(world(wc),z,h,ls[la],name)
 for dg in c['doors']:
  portal=wkt.loads(dg).intersection(unary_union([floor.boundary.buffer(.06),private.boundary.buffer(.06)]))
  add(world(portal),2.15,.60,ls['01_MUROS'],'Dintel acceso / cota medida')
 common=floor.difference(private).difference(service)
 add(world(common),2.75,.14,ls['17_CUBIERTA_TERMICA'],'Cubierta comun compacta / espesor de estudio')
 add(world(floor.boundary.buffer(.055)), -.39,.20,ls['07_ACERO'],'Bandeja perimetral recompuesta / sin calculo estructural')
 # Metadata follows the same rigid translations as actual room assemblies.
 for door in M[j]['doors']:
  dx,dy=roomd.get(door['id'],(bdx,bdy) if door['id'].startswith('B') else (0,0))
  for key in ['p0','p1','pocket_end','hinge','closed','open']:
   if key in door:door[key]=[door[key][0]+dx,door[key][1]+dy]
 for i,ax in enumerate(M[j]['bow_axes']):
  dx,dy=roomd[f'H{i+1:02d}']
  for key in ['p0','p1']:ax[key]=[ax[key][0]+dx,ax[key][1]+dy]
 # Rotate real geometry by +90 degrees, then place each isolated proposal at its catalogue position.
 pivot=world(floor).centroid;rot=r.Transform.Rotation(math.pi/2,r.Vector3d(0,0,1),r.Point3d(pivot.x,pivot.y,0))
 rotated=rotate(world(floor),90,origin=(pivot.x,pivot.y));bx,by,bX,bY=rotated.bounds;sx=j*28-bx;sy=-by
 def pp(p):return [pivot.x-(p[1]-pivot.y)+sx,pivot.y+(p[0]-pivot.x)+sy]
 for o in list(m.Objects):
  if o.Attributes.LayerIndex in ls.values():o.Geometry.Transform(rot);o.Geometry.Transform(r.Transform.Translation(sx,sy,0));assert o.Geometry.IsValid
 for door in M[j]['doors']:
  for key in ['p0','p1','pocket_end','hinge','closed','open']:
   if key in door:door[key]=pp(door[key])
 for ax in M[j]['bow_axes']:
  for key in ['p0','p1']:ax[key]=pp(ax[key])
 for shaft in M[j]['shafts']:shaft['center']=pp([shaft['center'][0]+bdx,shaft['center'][1]+bdy])
 M[j]['floor']=translate(rotated,sx,sy).wkt;M[j]['wall_cut']=translate(rotate(world(walls),90,origin=(pivot.x,pivot.y)),sx,sy).wkt
 M[j]['roof_not_redesigned']=False;M[j]['compact_iteration']=True;M[j]['rotation_degrees']=90
 report.append({'code':fam,'original_floor_m2':old['floor'].area,'compact_floor_m2':floor.area,'floor_bbox_after_rotation_m':[bX-bx,bY-by],'room_floor_m2':G.ROOM.area,'beds_m':[1.25,2.0],'desks_m':[1.8,.9],'programme_clearance_90cm_checked':c['paths90'],'all_bedrooms_face_street':False,'roof_scope':'Common roof recomposed; structure and connections require recalculation.'})
assert m.Write(str(P/'modelos/TRES_UNIDADES_COMPACTADAS_GIRO90.3dm'),8)
# A rigid rotation of the complex is kept separately as an explicit fit test.
e=r.File3dm.Read(str(P/'modelos/E02_REVISION_TECNICA.3dm'))
floorobs=[o for o in D[1]['objects'] if o['name'].startswith('Suelo continuo')];ef=unary_union([reg(o) for o in floorobs]);ec=ef.centroid;tr=r.Transform.Rotation(math.pi/2,r.Vector3d(0,0,1),r.Point3d(ec.x,ec.y,0))
for o in e.Objects:
 la=e.Layers.FindIndex(o.Attributes.LayerIndex).Name
 if la in ['90_CONTEXTO','91_PARCELA']:continue
 o.Geometry.Transform(tr)
e.Strings['ENSAYO']='GIRO RIGIDO 90 GRADOS: NO ENCAJA EN LA PARCELA. No usar como distribucion resuelta.'
assert e.Write(str(P/'modelos/E02_GIRO90_ENSAYO_NO_ENCAJADO.3dm'),8)
parcel=unary_union([reg(o) for o in D[2]['objects'] if o['layer']=='91_PARCELA']);ef90=rotate(ef,90,origin=(ec.x,ec.y));outside=ef90.difference(parcel).area
for door in M[3]['doors']:
 for key in ['p0','p1','pocket_end','hinge','closed','open']:
  if key in door:door[key]=[ec.x-(door[key][1]-ec.y),ec.y+(door[key][0]-ec.x)]
for ax in M[3]['bow_axes']:
 for key in ['p0','p1']:ax[key]=[ec.x-(ax[key][1]-ec.y),ec.y+(ax[key][0]-ec.x)]
for shaft in M[3]['shafts']:
 p=shaft['center'];shaft['center']=[ec.x-(p[1]-ec.y),ec.y+(p[0]-ec.x)]
M[3]['rigid_rotation_test_only']=True;M[3]['outside_parcel_m2']=outside
(P/'verificacion/REVISION_GEOMETRICA_GIRO90.json').write_text(json.dumps(M,ensure_ascii=False,indent=2))
report.append({'code':'E02_GIRO90','floor_bbox_after_rotation_m':[ef90.bounds[2]-ef90.bounds[0],ef90.bounds[3]-ef90.bounds[1]],'outside_parcel_m2':outside,'parcel_max_transverse_extent_m':parcel.bounds[3]-parcel.bounds[1],'fits_parcel':False,'scope':'Rigid rotation only. Recomposition and a new vertical-access/structural solution are necessary.'})
(P/'verificacion/COMPACTACION_Y_GIRO90.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))
