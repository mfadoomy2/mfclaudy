from pathlib import Path
import zipfile,hashlib,json,shutil
from PIL import Image
root=Path(__file__).resolve().parents[1]
images=sorted((root/'vistas').glob('0*.png'))
assert len(images)==5,len(images)
for im in images:
    with Image.open(im) as a:
        assert a.size==(2800,2100)
        a.verify()
files=[root/'modelo/MEGAESTRUCTURA_MACARRA.3dm',root/'LEEME.md',root/'verificacion.json',root/'auditoria_archivo.json']+images+sorted((root/'fuentes').glob('*.py'))
manifest={str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(root/'MANIFIESTO_SHA256.json').write_text(json.dumps(manifest,indent=2))
files.append(root/'MANIFIESTO_SHA256.json')
zpath=root.parent/'MEGAESTRUCTURA_MACARRA_ENTREGA.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
    for f in files:z.write(f,str(Path(root.name)/f.relative_to(root)))
with zipfile.ZipFile(zpath) as z:assert z.testzip() is None
backup=Path('/Users/adam/Downloads/MEGAESTRUCTURA_MACARRA_ENTREGA.zip')
shutil.copy2(zpath,backup)
print(json.dumps({'zip':str(zpath),'backup':str(backup),'files':len(files),'bytes':zpath.stat().st_size,'verified':True}))
