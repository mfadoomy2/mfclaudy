#! python3
import Rhino, json, os
OUT = '/Volumes/T7/G3_RHINO/out/00_docs.json'
docs = []
for d in Rhino.RhinoDoc.OpenDocuments():
    docs.append({'name': d.Name, 'path': d.Path, 'runtime': d.RuntimeSerialNumber, 'objects': d.Objects.Count,
                 'layers': [l.FullPath for l in d.Layers if not l.IsDeleted][:80], 'modified': d.Modified,
                 'active': d.RuntimeSerialNumber == Rhino.RhinoDoc.ActiveDoc.RuntimeSerialNumber})
json.dump(docs, open(OUT, 'w'), indent=1)
print('G3 docs ok', len(docs))
