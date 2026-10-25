# -*- coding: utf-8 -*-
import Rhino as R, System, os,json,clr
from System.Drawing import Color
clr.AddReference('Newtonsoft.Json')
from Newtonsoft.Json import JsonConvert
root=u'/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16';G=R.Geometry;D=R.DocObjects
F=R.FileIO.File3dm.Read(os.path.join(root,'modelos','UNIDAD_P02_DETALLADA.3dm'));batches={};preview=R.FileIO.File3dm();preview.Settings.ModelUnitSystem=R.UnitSystem.Meters
for l in F.AllLayers:
 ll=D.Layer();ll.Name=l.Name;ll.Color=l.Color;ll.IsVisible=True;preview.AllLayers.Add(ll)
for m in F.AllMaterials:preview.AllMaterials.Add(D.Material(m))
mp=G.MeshingParameters.FastRenderMesh;mp.Tolerance=.002;mp.RefineGrid=True
for ob in F.Objects:
 g=ob.Geometry;a=ob.Attributes
 if a.Name=='Hoja hiedra' or (a.Name or '').startswith('Hiedra colgante'):continue
 if isinstance(g,G.Brep):ms=list(G.Mesh.CreateFromBrep(g,mp) or [])
 elif isinstance(g,G.Mesh):ms=[g.DuplicateMesh()]
 else:continue
 key=str(a.LayerIndex)+'_'+str(a.MaterialIndex)
 if key not in batches:
  mat=next(m for m in F.AllMaterials if m.Index==a.MaterialIndex);co=mat.DiffuseColor;la=next(l.Name for l in F.AllLayers if l.Index==a.LayerIndex)
  batches[key]={'layer':la,'color':[co.R/255.,co.G/255.,co.B/255.],'alpha':mat.Transparency,'vertices':[],'faces':[]}
 b=batches[key]
 for m in ms:
  m.Normals.ComputeNormals();off=len(b['vertices']);b['vertices'].extend([[float(v.X),float(v.Y),float(v.Z)] for v in m.Vertices])
  for f in m.Faces:b['faces'].append([off+f.A,off+f.B,off+f.C] if f.IsTriangle else [off+f.A,off+f.B,off+f.C,off+f.D])
  aa=a.Duplicate();aa.ObjectId=System.Guid.NewGuid();preview.Objects.AddMesh(m,aa)
System.IO.File.WriteAllText(os.path.join(root,'fuentes','geometria_unidad.json'),JsonConvert.SerializeObject(batches))
opt=R.FileIO.File3dmWriteOptions();opt.Version=8;preview.Write(os.path.join(root,'modelos','UNIDAD_P02_PREVIA_SOLIDA.3dm'),opt)
with open(os.path.join(root,'verificacion','mallas_nativas.json'),'w') as f:json.dump({'batches':len(batches),'vertices':sum(len(b['vertices']) for b in batches.values()),'faces':sum(len(b['faces']) for b in batches.values()),'source':'Breps remallados con RhinoCommon, sin depender de caches previas','tolerance_m':.002},f)
print('MALLAS_COMPLETAS_UNIDAD')
