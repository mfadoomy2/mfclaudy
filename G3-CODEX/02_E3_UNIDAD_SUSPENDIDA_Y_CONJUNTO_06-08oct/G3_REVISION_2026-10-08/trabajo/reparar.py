import rhino3dm as r,numpy as np,json,pathlib,hashlib,time
from shapely.geometry import LineString,Polygon
from shapely.geometry.polygon import orient
from shapely.ops import polygonize,unary_union
from shapely import constrained_delaunay_triangles
B=pathlib.Path('/Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08')
def repair(g):
 vs=np.array([[p.X,p.Y,p.Z] for p in g.Vertices]); zs=np.unique(np.round(vs[:,2],5))
 if len(zs)!=2:return None
 fs=[list(g.Faces[i]) for i in range(len(g.Faces))];sides=[];caps=[];lines=[]
 for f in fs:
  f=f[:3] if f[2]==f[3] else f
  p=vs[f]
  if np.ptp(p[:,2])<1e-5:caps.append(p)
  else:
   sides.append(f)
   for i in range(len(f)):
    a,b=p[i],p[(i+1)%len(f)]
    if abs(a[2]-zs[0])<1e-5 and abs(b[2]-zs[0])<1e-5 and np.linalg.norm(a[:2]-b[:2])>1e-6:
     lines.append(LineString([a[:2],b[:2]]))
 if not lines or not caps:return None
 polys=list(polygonize(unary_union(lines)))
 if not polys:return None
 # Polygonize emits both annulus and inner island: use cap winding to retain physical interiors.
 # Extruded rings are identified from nested exterior loops, using even-odd containment.
 loops=[Polygon(p.exterior) for p in polys]
 keep=[p for i,p in enumerate(polys) if sum(q.contains(p.representative_point()) for j,q in enumerate(loops) if j!=i and q.area>loops[i].area)==0]
 region=unary_union(keep)
 area=sum(Polygon(p[:,:2]).area for p in caps)/2
 if abs(area-region.area)>max(1e-4,region.area*1e-5):return None
 if region.geom_type!='Polygon' or len(region.interiors)>0:return None
 # Rebuild as an editable capped extrusion, keeping the exact sampled side contour.
 region=orient(region,sign=1.0)
 pts=[r.Point3d(x,y,float(zs[0])) for x,y in region.exterior.coords]
 curve=r.PolylineCurve(pts)
 ex=r.Extrusion.Create(curve,float(zs[1]-zs[0]),True)
 if ex is None or not ex.IsValid or not ex.IsSolid:return None
 bb0=g.GetBoundingBox();bb1=ex.GetBoundingBox()
 error=max(abs(getattr(a,k)-getattr(b,k)) for a,b in [(bb0.Min,bb1.Min),(bb0.Max,bb1.Max)] for k in 'XYZ')
 if error>2e-5:return None
 return ex,{'area_profile':region.area,'vertices_before':len(g.Vertices),'bbox_error_m':error}
for name in ['unidad_suspendida_7','conjunto_opciones_1']:
 src=pathlib.Path('/Users/adam/Downloads/G3_'+name+'.3dm');f=r.File3dm.Read(str(src));fix=[];start=time.time()
 for o in list(f.Objects):
  l=f.Layers.FindIndex(o.Attributes.LayerIndex);g=o.Geometry
  if not isinstance(g,r.Mesh) or l.Name=='Contexto':continue
  result=repair(g)
  if result:
   m,stats=result;att=o.Attributes;oid=str(att.Id);f.Objects.Delete(att.Id);att.SetUserString('G3_revision','Extrusion solida editable; contorno lateral original conservado');f.Objects.Add(m,att);fix.append({'id':oid,'layer':l.FullPath,**stats})
 for l in f.Layers:
  if 'posición abierta' in l.Name:l.Visible=False
 # Normalization of shading only; existing materials and design colors retained.
 dst=B/('01_UNIDAD_reconstruida.3dm' if name.startswith('unidad') else '02_CONJUNTOS_reconstruidos.3dm');f.Write(str(dst),8)
 check=r.File3dm.Read(str(dst));report={'source':str(src),'sha256_source':hashlib.sha256(src.read_bytes()).hexdigest(),'output':str(dst),'objects_source':len(f.Objects),'objects_output':len(check.Objects),'reconstructions':fix,'elapsed':time.time()-start}
 (B/'trabajo'/('reparaciones_'+name+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(name,'REPAIRED',len(fix),'objects',len(check.Objects),'seconds',round(time.time()-start),flush=True)
