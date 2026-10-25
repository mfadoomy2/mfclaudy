import rhino3dm as r,numpy as np,json,pathlib,hashlib,time
from shapely.geometry import LineString,Polygon
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
 print('sidescaps',len(sides),len(caps),len(lines));
 if not lines or not caps:return None
 polys=list(polygonize(unary_union(lines)))
 print('polys',len(polys));
 if not polys:return None
 # Polygonize emits both annulus and inner island: use cap winding to retain physical interiors.
 # Extruded rings are identified from nested exterior loops, using even-odd containment.
 loops=[Polygon(p.exterior) for p in polys]
 keep=[p for i,p in enumerate(polys) if sum(q.contains(p.representative_point()) for j,q in enumerate(loops) if j!=i and q.area>loops[i].area)==0]
 region=unary_union(keep)
 area=sum(Polygon(p[:,:2]).area for p in caps)/2
 print('areas',area,region.area);
 if abs(area-region.area)<max(1e-4,region.area*1e-5):return None
 m=r.Mesh();lookup={}
 def v(a):
  k=tuple(round(float(x),6) for x in a)
  if k not in lookup:lookup[k]=m.Vertices.Add(*k)
  return lookup[k]
 for f in sides:m.Faces.AddFace(*[v(vs[i]) for i in f])
 for poly in keep:
  for tr in constrained_delaunay_triangles(poly).geoms:
   pts=np.array(tr.exterior.coords)[:3];sgn=(pts[1,0]-pts[0,0])*(pts[2,1]-pts[0,1])-(pts[1,1]-pts[0,1])*(pts[2,0]-pts[0,0])
   if sgn<0:pts=pts[::-1]
   m.Faces.AddFace(*[v([*p,zs[0]]) for p in pts[::-1]])
   m.Faces.AddFace(*[v([*p,zs[1]]) for p in pts])
 m.Normals.ComputeNormals();m.Compact()
 if not m.IsValid or not m.IsClosed:
  if region.area>10: print('REJECT',m.IsValid,m.IsClosed,area,region.area,len(lines),len(polys),len(keep),flush=True)
  return None
 return m,{'old_cap_area_one_side':area,'new_cap_area_one_side':region.area,'vertices_before':len(g.Vertices),'vertices_after':len(m.Vertices)}

f=r.File3dm.Read('/Users/adam/Downloads/G3_unidad_suspendida_7.3dm')
for o in f.Objects:
 l=f.Layers.FindIndex(o.Attributes.LayerIndex)
 if 'Fuera del cubo 2' in l.FullPath and l.Name=='Cubierta':
  print('TEST',o.Attributes.Id); print(repair(o.Geometry))
