# -*- coding: utf-8 -*-
"""FASE FINAL - S00: determinar la baseline vigente y congelarla en un snapshot con hashes.

Baseline = FASE_03B9_HYPERDETAIL_V006 (cerrada 2026-08-13, veredicto V006 HYPERDETAIL PASS,
auditoria build 12: 0 RED / 26 YELLOW / 18 GREEN, clima re-ejecutado en _reclima9 con k_veg
por especie). Este script NO decide: verifica que esa baseline existe, la hashea y la registra.
"""
import datetime
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))          # REFUGIO_CLIMATICO/
MONT = os.path.normpath(os.path.join(ROOT, '..'))                      # Monteserin/
F9 = os.path.join(ROOT, 'FASE_03B9_HYPERDETAIL_V006')
OUT = os.path.normpath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402


def sha256(path, buf=1 << 20):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(buf)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


VIGENTES = {
    'geometria': ['geometria_maestra_v006.json', '_v006_diff.json'],
    'maestros': ['MASTER_ARCHITECTURE_v006.3dm', 'SOL_FULL_SCENE_v005.3dm',
                 'SOL_PRESENTATION_MASTER_v004.3dm', 'ASSET_LIBRARY_v005.3dm'],
    'generadores': ['build_all_03b9.py', 'detailing_03b9.py', 'veg_assets.py', 'purge_scan.py'],
    'auditoria': ['_reaudit9/audit_core.py', '_reaudit9/audit_run.py', '_reaudit9/audit_report.py',
                  '_reaudit9/_data/summary.json', '_reaudit9/_data/issues.json'],
    'clima': ['_reclima9/clima_core.py', '_reclima9/clima_run.py', '_reclima9/clima_run2.py',
              '_reclima9/clima_report.py', '_reclima9/_data/metricas.json',
              '_reclima9/_data/vegetacion.json', '_veg_clima.json'],
    'botanica': ['BOTANICAL_MASTERPLAN_v001.csv', 'ASSET_PROVENANCE.csv', '_veg_blocks.json'],
    'informes': ['HYPERDETAIL_REPORT.md', 'SELF_CRITIQUE_V006.md',
                 'AUDIT_V006_MASTER.pdf', 'CLIMATE_V006_MASTER.pdf'],
}

snap = {
    'proyecto': 'REFUGIO CLIMATICO PUERTA DEL SOL',
    'fase': 'FINAL-ANALISIS',
    'baseline': 'v006 / FASE_03B9_HYPERDETAIL_V006 (build 12)',
    'veredicto_baseline': 'V006 HYPERDETAIL PASS (0 RED / 26 YELLOW / 18 GREEN)',
    'timestamp': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
    'archivos': {},
    'faltantes': [],
}

for grupo, files in VIGENTES.items():
    for rel in files:
        p = os.path.join(F9, rel)
        if not os.path.exists(p):
            snap['faltantes'].append(rel)
            continue
        st = os.stat(p)
        snap['archivos'][rel] = {
            'grupo': grupo, 'bytes': st.st_size,
            'mtime': datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds'),
            'sha256': sha256(p),
        }

# resumen de auditoria y clima vigentes (las cifras canon de las que TODO analisis debe partir)
with open(os.path.join(F9, '_reaudit9', '_data', 'summary.json'), encoding='utf-8') as f:
    snap['auditoria_vigente'] = json.load(f)
with open(os.path.join(F9, '_reclima9', '_data', 'metricas.json'), encoding='utf-8') as f:
    snap['clima_vigente'] = json.load(f)

dst = os.path.join(OUT, 'BASELINE_SNAPSHOT.json')
with open(dst, 'w', encoding='utf-8') as f:
    json.dump(snap, f, ensure_ascii=False, indent=1)

flog.event(fase='FINAL', tipo_evento='snapshot_baseline',
           objetivo='FASE FINAL: congelar baseline v006 (build 12) como fuente geometrica unica',
           resultado='%d archivos hasheados, %d faltantes. Snapshot: %s'
                     % (len(snap['archivos']), len(snap['faltantes']),
                        os.path.relpath(dst, MONT)),
           parametros={'baseline': snap['baseline'], 'faltantes': snap['faltantes']})

print('BASELINE:', snap['baseline'])
print('hasheados:', len(snap['archivos']), '| faltantes:', snap['faltantes'])
print('auditoria:', snap['auditoria_vigente'].get('counts'))
print('clima: dMRT=%.1f dUTCI=%.2f refugio=%.0f m2' % (
    snap['clima_vigente']['dMRT'], snap['clima_vigente']['dUTCI'], snap['clima_vigente']['m2_refugio']))
