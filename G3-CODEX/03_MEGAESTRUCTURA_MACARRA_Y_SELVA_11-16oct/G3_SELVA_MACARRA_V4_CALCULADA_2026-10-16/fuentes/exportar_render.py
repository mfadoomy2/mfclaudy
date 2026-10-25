# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import Rhino as R, json, os
G=R.Geometry;T=G.Transform
ROOT=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16'
finalpath=os.path.join(ROOT,'modelos','SELVA_MACARRA_CALCULADA_V4.3dm')
MP=G.MeshingParameters.FastRenderMesh
def status(s):print(s)
F=R.FileIO.File3dm.Read(finalpath)
status('RENDER: exportar triangulacion exacta del Rhino, sin reinterpretacion de imagen')
objmap={str(o.Attributes.ObjectId):o for o in F.Objects};idef={str(d.Id):d for d in F.AllInstanceDefinitions}
batches={}
def rendergeom(g,a,xfm):
 if isinstance(g,G.InstanceReferenceGeometry):
  dd=idef[str(g.ParentIdefId)]
  for oid in dd.GetObjectIds():
   ob=objmap[str(oid)];rendergeom(ob.Geometry,ob.Attributes,xfm*g.Xform)
  return
 meshes=[]
 if isinstance(g,G.Brep):
  for face in g.Faces:
   m=face.GetMesh(G.MeshType.Render)
   if m:meshes.append(m.DuplicateMesh())
  if not meshes:meshes=list(G.Mesh.CreateFromBrep(g,MP) or [])
 elif isinstance(g,G.Mesh):meshes=[g.DuplicateMesh()]
 if not meshes:return
 key=str(a.LayerIndex)+'_'+str(a.MaterialIndex)
 if key not in batches:
  mat=next(m for m in F.AllMaterials if m.Index==a.MaterialIndex);col=mat.DiffuseColor
  batches[key]={'vertices':[],'faces':[],'color':[col.R/255.,col.G/255.,col.B/255.],'alpha':mat.Transparency,'layer':next(l.Name for l in F.AllLayers if l.Index==a.LayerIndex)}
 b=batches[key]
 for m in meshes:
  m.Transform(xfm);off=len(b['vertices']);b['vertices'].extend([[float(v.X),float(v.Y),float(v.Z)] for v in m.Vertices])
  for face in m.Faces:b['faces'].append([off+face.A,off+face.B,off+face.C] if face.IsTriangle else [off+face.A,off+face.B,off+face.C,off+face.D])
for ob in F.Objects:
 if not ob.Attributes.IsInstanceDefinitionObject:rendergeom(ob.Geometry,ob.Attributes,T.Identity)
with open(os.path.join(ROOT,'fuentes','geometria_render.json'),'w') as f:json.dump(batches,f,separators=(',',':'))
print('EXPORTACION_RENDER_V4_LISTA')
