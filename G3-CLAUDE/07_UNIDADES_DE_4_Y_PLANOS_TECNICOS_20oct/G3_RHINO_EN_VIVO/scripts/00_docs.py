#! python3
import Rhino, json, os
OUT = '/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_RHINO_EN_VIVO/salida/00_docs.json'
docs = []
for d in Rhino.RhinoDoc.OpenDocuments():
    docs.append({'name': d.Name, 'path': d.Path, 'runtime': d.RuntimeSerialNumber, 'objects': d.Objects.Count,
                 'layers': [l.FullPath for l in d.Layers if not l.IsDeleted][:80], 'modified': d.Modified,
                 'active': d.RuntimeSerialNumber == Rhino.RhinoDoc.ActiveDoc.RuntimeSerialNumber})
json.dump(docs, open(OUT, 'w'), indent=1)
print('G3 docs ok', len(docs))
