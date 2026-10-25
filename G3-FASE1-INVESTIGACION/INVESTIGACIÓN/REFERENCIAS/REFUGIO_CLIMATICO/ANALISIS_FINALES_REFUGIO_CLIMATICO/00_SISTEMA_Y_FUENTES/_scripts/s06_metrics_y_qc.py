# -*- coding: utf-8 -*-
"""FASE FINAL - S06: FINAL_METRICS_REGISTRY.csv + test de consistencia (§41-42)
+ contactos de QC grafico de TODOS los PDFs (§39)."""
import csv
import datetime
import glob
import json
import os
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..'))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
MONT = os.path.normpath(os.path.join(BASE, '..', '..'))
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402

# ---------------------------------------------------------------- registro de metricas
rows = []
for f in sorted(glob.glob(os.path.join(OUT, '_metrics', 'metrics_*.jsonl'))):
    for line in open(f, encoding='utf-8'):
        line = line.strip()
        if line:
            rows.append(json.loads(line))
hoy = datetime.date.today().isoformat()
with open(os.path.join(OUT, 'FINAL_METRICS_REGISTRY.csv'), 'w', encoding='utf-8-sig',
          newline='') as f:
    w = csv.writer(f)
    w.writerow(['id', 'valor', 'unidad', 'estado', 'metodo', 'fuente', 'notas',
                'pdf', 'pagina', 'version_geometrica', 'fecha'])
    for r in rows:
        w.writerow([r['id'], r['valor'], r['unidad'], r['estado'], r['metodo'],
                    r['fuente'], r.get('notas', ''), r['pdf'], r['pagina'],
                    'v006 build 12', hoy])

# consistencia: mismo id con valores distintos (§42)
por_id = {}
conflictos = []
for r in rows:
    k = r['id']
    if k in por_id and str(por_id[k]) != str(r['valor']):
        conflictos.append((k, por_id[k], r['valor'], r['pdf']))
    por_id[k] = r['valor']
print('metricas registradas:', len(rows), '| ids unicos:', len(por_id),
      '| conflictos:', len(conflictos))
for c in conflictos:
    print('  CONFLICTO', c)

# ---------------------------------------------------------------- contactos QC (§39)
QC = os.path.join(OUT, '_qc_contactos')
os.makedirs(QC, exist_ok=True)
pdfs = sorted(glob.glob(os.path.join(BASE, '*', '*.pdf')))
resumen = []
for pdf in pdfs:
    rel = os.path.relpath(pdf, BASE)
    d = fitz.open(pdf)
    n = d.page_count
    # contacto: hasta 8 paginas por hoja, 2 filas x 4 col
    import math as m
    cols, rws = 4, 2
    per = cols * rws
    for hoja in range(m.ceil(n / per)):
        pix0 = d[0].get_pixmap(dpi=40)
        W_, H_ = pix0.width, pix0.height
        sheet = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, W_ * cols, H_ * rws))
        sheet.clear_with(255)
        for k in range(per):
            i = hoja * per + k
            if i >= n:
                break
            px = d[i].get_pixmap(dpi=40)
            x0 = (k % cols) * W_
            y0 = (k // cols) * H_
            px.set_origin(x0, y0)
            sheet.copy(px, px.irect)
        nombre = os.path.splitext(os.path.basename(pdf))[0]
        sheet.save(os.path.join(QC, '%s_hoja%d.png' % (nombre, hoja + 1)))
    resumen.append((rel, n))
    d.close()

print('PDFs en familia:', len(pdfs), '| paginas totales:', sum(n for _, n in resumen))
flog.event(fase='FINAL', tipo_evento='metrics_registry_qc',
           objetivo='FINAL_METRICS_REGISTRY.csv + consistencia + contactos QC',
           resultado='%d metricas (%d ids, %d conflictos); %d PDFs / %d paginas rasterizadas'
                     % (len(rows), len(por_id), len(conflictos), len(pdfs),
                        sum(n for _, n in resumen)))
with open(os.path.join(OUT, '_qc_contactos', '_indice_contactos.json'), 'w',
          encoding='utf-8') as f:
    json.dump(resumen, f, ensure_ascii=False, indent=1)
