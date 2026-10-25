from pathlib import Path
import json,math,rhino3dm as r
R=Path(__file__).resolve().parents[1];d=r.File3dm();d.Settings.ModelUnitSystem=r.UnitSystem.Meters
cache=json.loads((R/'fuentes/geometria_render.json').read_text())
for key,b in cache.items():
 if b['layer']=='90_CONTEXTO':continue
 co=tuple(round(c*255) for c in b['color'])+(255,)
 l=r.Layer();l.Name=b['layer']+'_'+key;l.Color=co;li=d.Layers.Add(l)
 m=r.Material();m.Name=l.Name;m.DiffuseColor=co;m.Transparency=b['alpha'];mi=d.Materials.Add(m)
 mesh=r.Mesh()
 for v in b['vertices']:mesh.Vertices.Add(*v)
 for f in b['faces']:mesh.Faces.AddFace(*f)
 mesh.Normals.ComputeNormals();mesh.Compact()
 a=r.ObjectAttributes();a.LayerIndex=li;a.MaterialIndex=mi;a.MaterialSource=r.ObjectMaterialSource.MaterialFromObject;a.Name='Previa de malla exacta / '+b['layer'];a.SetUserString('Origen','Triangulacion de SELVA_MACARRA_V4_FINAL.3dm; editar el archivo Brep original')
 d.Objects.AddMesh(mesh,a)
d.Write(str(R/'modelos/PREVIA_SOLIDA_MALLAS.3dm'),8);print('PREVIA_SOLIDA_LISTA',flush=True)
