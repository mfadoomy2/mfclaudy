# -*- coding: utf-8 -*-
"""FASE FINAL - S01: inventario recursivo del corpus del Refugio Climatico.

Recorre Monteserin/ y clasifica cada archivo relevante: fase, tipo, autoridad, vigencia,
dependencia geometrica y necesidad de regeneracion. Excluye la Maqueta (otro proyecto),
librerias de terceros y cachés. Output: 00_CORPUS_MANIFEST.csv + resumen JSON.
"""
import csv
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..'))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))          # REFUGIO_CLIMATICO/
MONT = os.path.normpath(os.path.join(ROOT, '..'))                      # Monteserin/
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402

# --- ambitos incluidos (relativos a Monteserin) y su papel
AMBITOS = {
    'REFUGIO_CLIMATICO': 'proyecto',
    '_FORENSIC_PROCESS': 'forense',
    'LIBRO_PROCESO': 'genealogia',
    'LAMINA_A1': 'genealogia',
}
EXCLUIR_DIRS = {'__pycache__', 'node_modules', '.git', '.obsidian', 'graphify-out',
                'ANALISIS_FINALES_REFUGIO_CLIMATICO'}
EXCLUIR_FILES = {'three.min.js', 'desktop.ini', 'Thumbs.db'}
EXT_IGNORAR = {'.pyc', '.tmp', '.lock', '.rar', '.zip'}

TIPOS = {
    '.pdf': 'PDF', '.md': 'MARKDOWN', '.json': 'JSON', '.csv': 'CSV', '.npy': 'NPY',
    '.png': 'IMAGEN', '.jpg': 'IMAGEN', '.jpeg': 'IMAGEN', '.webp': 'IMAGEN', '.svg': 'SVG',
    '.py': 'SCRIPT', '.3dm': 'MODELO', '.obj': 'MODELO', '.glb': 'ASSET3D', '.gltf': 'ASSET3D',
    '.bin': 'ASSET3D', '.js': 'JS', '.html': 'HTML', '.txt': 'TEXTO', '.blend': 'BLENDER',
    '.jsonl': 'LOG',
}

# fase por primer segmento bajo REFUGIO_CLIMATICO
FASE_GEOM = {   # version geometrica sobre la que se apoya cada fase
    'FASE_01_BASE_GRAFICA': 'v001-2D', 'FASE_03A_MODELO_PROXY': 'proxy',
    'FASE_03B_MODELO_MAESTRO': 'v001-v002', 'FASE_03B5_AUDITORIA': 'v002',
    'FASE_03B5B_CLIMA': 'v002', 'FASE_03B6_RESOLUCION': 'v003',
    'FASE_03C_VISUALIZACION': 'v002-v003', '03D_PRE_V004_BASELINE_V003': 'v003',
    'FASE_03B7_DETAILING_V004': 'v004', 'FASE_03B8_PURGE_MICRODETAIL_V005': 'v005',
    'FASE_03B9_HYPERDETAIL_V006': 'v006',
}
VIGENTE_FASE = 'FASE_03B9_HYPERDETAIL_V006'

# palabras clave -> contenido
CONTENIDO = [
    ('audit', 'auditoria'), ('clima', 'clima'), ('climate', 'clima'), ('mrt', 'clima'),
    ('utci', 'clima'), ('solar', 'clima'), ('shadow', 'clima'), ('mist', 'clima'),
    ('water', 'agua'), ('agua', 'agua'), ('veg', 'vegetacion'), ('botanic', 'vegetacion'),
    ('path', 'movilidad'), ('width', 'movilidad'), ('access', 'movilidad'),
    ('metro', 'transporte'), ('maint', 'mantenimiento'), ('collision', 'auditoria'),
    ('purge', 'purga'), ('render', 'render'), ('view', 'visuales'), ('screenshot', 'qa-visual'),
    ('micro', 'qa-visual'), ('provenance', 'assets'), ('masterplan', 'vegetacion'),
    ('geometria', 'geometria'), ('build', 'generador'), ('detailing', 'generador'),
    ('critique', 'informe'), ('report', 'informe'), ('registro', 'registro'),
    ('decision', 'registro'), ('issues', 'auditoria'), ('flog', 'forense'),
]


def clasifica(rel, ext, seg0, seg1):
    tipo = TIPOS.get(ext, ext.lstrip('.').upper() or 'OTRO')
    low = rel.lower()
    contenido = next((c for k, c in CONTENIDO if k in low), 'general')
    fase = seg1 if seg0 == 'REFUGIO_CLIMATICO' else seg0
    geom = FASE_GEOM.get(seg1, '') if seg0 == 'REFUGIO_CLIMATICO' else ''

    # autoridad
    if tipo == 'MODELO':
        aut = 'MAESTRO'
    elif tipo == 'SCRIPT':
        aut = 'SCRIPT'
    elif tipo in ('JSON', 'CSV', 'NPY'):
        aut = 'DATO'
    elif tipo == 'PDF' or tipo == 'MARKDOWN':
        aut = 'INFORME'
    elif tipo in ('IMAGEN', 'SVG'):
        aut = 'FIGURA'
    elif tipo == 'LOG':
        aut = 'REGISTRO'
    else:
        aut = 'APOYO'

    # vigencia
    if seg0 == '_FORENSIC_PROCESS':
        vig = 'VIGENTE'          # el forense nunca caduca
    elif seg0 in ('LIBRO_PROCESO', 'LAMINA_A1'):
        vig = 'GENEALOGIA'
    elif seg1 == VIGENTE_FASE:
        vig = 'VIGENTE'
    elif seg1 in FASE_GEOM:
        vig = 'HISTORICO'
    else:
        vig = 'HISTORICO'

    # depende de geometria?
    dep_geom = 'SI' if (contenido in ('auditoria', 'clima', 'movilidad', 'agua', 'vegetacion',
                                      'visuales', 'mantenimiento', 'transporte', 'qa-visual',
                                      'render')
                        and aut in ('DATO', 'INFORME', 'FIGURA')) else 'NO'

    # regenerar: analisis dependiente de geometria sobre version < v006
    if vig == 'VIGENTE' or aut in ('SCRIPT', 'MAESTRO', 'REGISTRO'):
        regen = 'NO'
    elif dep_geom == 'SI' and geom not in ('v006', ''):
        regen = 'SI'
    else:
        regen = 'NO'

    reutilizable = 'SI' if (vig == 'VIGENTE' or aut in ('SCRIPT', 'REGISTRO')
                            or vig == 'GENEALOGIA') else 'COMO-HISTORIA'
    return tipo, contenido, fase, geom, aut, vig, dep_geom, regen, reutilizable


rows = []
stats = {}
for seg0, papel in AMBITOS.items():
    base = os.path.join(MONT, seg0)
    if not os.path.isdir(base):
        continue
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in EXCLUIR_DIRS]
        for fn in filenames:
            if fn in EXCLUIR_FILES:
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext in EXT_IGNORAR:
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, MONT).replace('\\', '/')
            segs = rel.split('/')
            seg1 = segs[1] if len(segs) > 1 else ''
            try:
                st = os.stat(p)
            except OSError:
                continue
            tipo, contenido, fase, geom, aut, vig, dep, regen, reuse = clasifica(
                rel, ext, seg0, seg1)
            rows.append([rel, tipo, fase, geom,
                         datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d'),
                         st.st_size, contenido, aut, vig, dep, regen, reuse])
            k = (tipo, vig)
            stats[k] = stats.get(k, 0) + 1

rows.sort(key=lambda r: r[0])
dst = os.path.join(OUT, '00_CORPUS_MANIFEST.csv')
with open(dst, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['ruta', 'tipo', 'fase', 'version_geometrica', 'fecha_mod', 'bytes',
                'contenido', 'autoridad', 'vigencia', 'depende_geometria',
                'debe_regenerarse', 'reutilizable'])
    w.writerows(rows)

resumen = {
    'total_archivos': len(rows),
    'por_tipo_vigencia': {f'{t}|{v}': n for (t, v), n in sorted(stats.items())},
    'regenerar': sum(1 for r in rows if r[10] == 'SI'),
    'vigentes': sum(1 for r in rows if r[8] == 'VIGENTE'),
}
with open(os.path.join(OUT, '00_CORPUS_MANIFEST_resumen.json'), 'w', encoding='utf-8') as f:
    json.dump(resumen, f, ensure_ascii=False, indent=1)

flog.event(fase='FINAL', tipo_evento='corpus_manifest',
           objetivo='Inventario recursivo del corpus (Refugio + forense + genealogia)',
           resultado='%d archivos catalogados; %d vigentes; %d marcados para regenerar'
                     % (resumen['total_archivos'], resumen['vigentes'], resumen['regenerar']))
print(json.dumps(resumen, ensure_ascii=False, indent=1)[:1200])
