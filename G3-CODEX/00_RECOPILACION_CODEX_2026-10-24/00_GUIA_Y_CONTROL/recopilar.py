from pathlib import Path
import os,json,hashlib,concurrent.futures,time,collections,shutil
ROOT=Path('/Volumes/T7/G3 Proyectos');DEST=ROOT/'G3 CODEX';CONTROL=DEST/'00_GUIA_Y_CONTROL';START=time.time()
scan=json.loads((CONTROL/'INVENTARIO_INICIAL.json').read_text()) if (CONTROL/'INVENTARIO_INICIAL.json').exists() else json.loads(Path('/tmp/g3_archive_scan.json').read_text())
movfile=ROOT/'G3 CLAUDE/_registro_movimientos_2026-10-24.json'
mov=json.loads(movfile.read_text()) if movfile.exists() else []
relocated={Path(x['de']).name:ROOT.parent/x['a'] for x in mov}
# Source paths can change due to a concurrent organization; preserve original-to-current provenance.
if movfile.exists():shutil.copyfile(movfile,CONTROL/'REGISTRO_REUBICACION_PREEXISTENTE.json')
def category(n):
 if n.lower().endswith('.zip'):return '08_PAQUETES_ZIP_ORIGINALES'
 if n.startswith(('INVESTIG','MAPPEADOS','G3_REFERENCIAS','G3_SOL_')):return '01_INVESTIGACION_PARCELA_Y_REFERENCIAS'
 if n.startswith(('G3_P02_','G3_UNIDAD_AISLADA')):return '03_HABITACION_Y_UNIDAD_P02'
 if n.startswith(('G3_40_','G3_ATLAS_40','G3_CORRECCION_40','G3_TEJID','G3_UNIDAD_TEJIDO','G3_MAPA_ACTIVIDADES','G3_ACCIONES')):return '04_ACCIONES_TEJIDOS_Y_CATALOGOS'
 if n.startswith(('G3_CENTROS','G3_CONTINUIDAD','G3_DECIDIR','G3_DOCUMENTO_PLANTAS','G3_MODELOS_HERENCIA','G3_PLANTAS_FORMAS','G3_UNIDADES_4','G3_UNIONES')):return '05_NUEVAS_UNIDADES_UNIONES_Y_PARCELA'
 if n.startswith(('G3_PLANOS_TECNICOS','MEGAESTRUCTURA_MACARRA_PLANOS','G3_RHINO_EN_VIVO')):return '06_PLANOS_TECNICOS_Y_RHINO'
 if n.startswith(('IMAGINARIOS','G3_MECANISMOS','G3_E2_','G3_ORGANIZACION')):return '07_IMAGINARIOS_MECANISMOS_Y_ORGANIZACION'
 if n.startswith(('G3_CONJUNTO','G3_UNIDAD','G3_REVISION','G3_SELVA','G3_ESTUDIO_JUSTIFICACION','MEGAESTRUCTURA_CLAUDE')):return '02_PRIMERAS_UNIDADES_COMPLEJO_Y_LUZ'
 return '99_AUXILIARES_Y_DOCUMENTOS_HISTORICOS'
mapping={r['name']:category(r['name'])+'/'+r['name'] for r in scan}
(CONTROL/'MAPA_CARPETAS.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2))
tasks=[];excluded=[];missing=[]
def add_path(src,dest,origin):
 if not src.exists():missing.append({'source':str(src),'reason':'No localizado en la ruta referenciada'});return
 if src.is_file():tasks.append((src,dest,origin));return
 for dp,ds,fs in os.walk(src,followlinks=False):
  for name in list(ds):
   if name.startswith('._') or name=='.DS_Store':excluded.append(str(Path(dp)/name));ds.remove(name)
  for name in fs:
   q=Path(dp)/name
   if name.startswith('._') or name=='.DS_Store':excluded.append(str(q));continue
   tasks.append((q,dest/q.relative_to(src),origin))
for row in scan:
 src=ROOT/row['name']
 if not src.exists():src=relocated.get(row['name'],src)
 add_path(src,DEST/mapping[row['name']],'project_root')
externals=[
('/Users/adam/Downloads/MEGAESTRUCTURA_MACARRA','MEGAESTRUCTURA_MACARRA'),
('/Volumes/T7/PERSONAS.3dm','PERSONAS.3dm'),
('/Users/adam/Downloads/descargas 2/G3_unidad_suspendida_7.3dm','G3_unidad_suspendida_7.3dm'),
('/Users/adam/Downloads/descargas 2/G3_Acampada_Sol_conversacion.md','G3_Acampada_Sol_conversacion.md'),
('/Users/adam/.codex/attachments/ddfe3ff1-447c-40c0-98eb-149e5ef70b9e/Pasted text.txt','TEXTO_INICIAL_USUARIO.txt'),
]
for letter,name in [('C','CA22FB89-E973-4534-8520-FB4A05DCCF8D.heic'),('B','B3E7AD85-74BF-4862-A0C5-505105E40992.heic'),('C','C71C6164-A230-4E80-8E28-AD012CD630B0.heic'),('C','C6DA58C4-602D-4B57-A7F7-D165961EC4C9.heic')]:externals.append(('/Users/adam/Pictures/Photos Library.photoslibrary/originals/'+letter+'/'+name,'FOTOS_PROFESOR/'+name))
for path,name in externals:add_path(Path(path),DEST/'90_FUENTES_EXTERNAS_APORTADAS'/name,'explicit_project_input')
for path in ['/var/folders/42/wl0sblcn6qn7v18qnlr1t_3c0000gn/T/TemporaryItems/NSIRD_screencaptureui_uQJhO2/Screenshot 2026-10-18 at 16.19.59.png','/var/folders/42/wl0sblcn6qn7v18qnlr1t_3c0000gn/T/TemporaryItems/NSIRD_screencaptureui_UA73d1/Screenshot 2026-10-18 at 18.30.10.png']:add_path(Path(path),DEST/'90_FUENTES_EXTERNAS_APORTADAS/CAPTURAS_USUARIO'/Path(path).name,'explicit_project_input')
(CONTROL/'FUENTES_NO_LOCALIZADAS.json').write_text(json.dumps(missing,ensure_ascii=False,indent=2));(CONTROL/'EXCLUSIONES_METADATA_APPLE.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2))
(CONTROL/'INVENTARIO_INICIAL.json').write_text(json.dumps(scan,ensure_ascii=False,indent=2))
expected_tasks=list(tasks)
prior=json.loads((CONTROL/'INVENTARIO_ARCHIVOS_SHA256.json').read_text()) if (CONTROL/'INVENTARIO_ARCHIVOS_SHA256.json').exists() else []
known={r['destination']:r for r in prior}
tasks=[t for t in tasks if str(t[1].relative_to(DEST)) not in known]
print('COPY_START',len(tasks),sum(s.stat().st_size for s,d,o in tasks),flush=True)
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for buf in iter(lambda:f.read(4*1024*1024),b''):h.update(buf)
 return h.hexdigest()
def copy_one(task):
 src,dst,origin=task;dst.parent.mkdir(parents=True,exist_ok=True)
 for attempt in range(3):
  before=src.stat();h=hashlib.sha256();count=0
  with src.open('rb') as a,dst.open('wb') as b:
   for buf in iter(lambda:a.read(4*1024*1024),b''):h.update(buf);b.write(buf);count+=len(buf)
  after=src.stat()
  if (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns):break
 else:raise RuntimeError('Archivo cambiante: '+str(src))
 dh=digest(dst)
 if dh!=h.hexdigest() or count!=dst.stat().st_size:raise RuntimeError('Copia no identica: '+str(src))
 try:os.utime(dst,ns=(after.st_atime_ns,after.st_mtime_ns))
 except OSError:pass
 return {'source':str(src),'source_relative':str(Path(*dst.relative_to(DEST).parts[1:])) if origin=='project_root' else None,'destination':str(dst.relative_to(DEST)),'bytes':count,'sha256':dh,'verified':True,'origin':origin,'source_mtime_ns':after.st_mtime_ns,'symlink_source':str(src.readlink()) if src.is_symlink() else None}
rows=list(known.values());errors=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 fut={pool.submit(copy_one,t):t for t in tasks}
 for i,f in enumerate(concurrent.futures.as_completed(fut),1):
  try:rows.append(f.result())
  except Exception as e:errors.append({'source':str(fut[f][0]),'error':str(e)})
  if i%250==0:print('PROGRESS',i,'/',len(tasks),'GB',round(sum(r['bytes'] for r in rows)/1e9,2),'seconds',round(time.time()-START),flush=True)
rows.sort(key=lambda r:r['destination']);(CONTROL/'INVENTARIO_ARCHIVOS_SHA256.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
groups=collections.defaultdict(list)
for row in rows:groups[row['sha256']].append(row['destination'])
(CONTROL/'DUPLICADOS_IDENTICOS_CONSERVADOS.json').write_text(json.dumps([{'sha256':h,'paths':p} for h,p in groups.items() if len(p)>1],ensure_ascii=False,indent=2))
report={'date':'2026-10-24','source':str(ROOT),'destination':str(DEST),'source_project_files_expected':sum(r['files'] for r in scan),'files_expected':len(expected_tasks),'files_copied_verified':len(rows),'project_files_verified':sum(r['origin']=='project_root' for r in rows),'bytes_verified':sum(r['bytes'] for r in rows),'copy_errors':errors,'missing_external_sources':missing,'excluded_Apple_metadata_entries':len(excluded),'elapsed_seconds':round(time.time()-START,2),'originals_changed':False,'verification':'Every copied file: SHA-256 of source stream compared to a fresh read of destination; size and source stability checked.'}
(CONTROL/'VERIFICACION_RECOPILACION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('DONE',json.dumps(report,ensure_ascii=False),flush=True)
