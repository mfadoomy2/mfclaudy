# -*- coding: utf-8 -*-
"""FASE FINAL - S08: cierre forense del paquete analitico."""
import csv
import glob
import io
import json
import os
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
MONT = os.path.normpath(os.path.join(BASE, '..', '..'))
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402

pdfs = sorted(glob.glob(os.path.join(BASE, '*/*.pdf'))) + \
    glob.glob(os.path.join(BASE, '*.pdf'))
pp = 0
for f in pdfs:
    d = fitz.open(f); pp += d.page_count; d.close()
man = list(csv.DictReader(io.open(os.path.join(BASE, '00_SISTEMA_Y_FUENTES',
                                               'MANIFIESTO_ENTREGA_FINAL.csv'),
                                  encoding='utf-8-sig')))
met = list(csv.DictReader(io.open(os.path.join(BASE, '00_SISTEMA_Y_FUENTES',
                                               'FINAL_METRICS_REGISTRY.csv'),
                                  encoding='utf-8-sig')))
snap = json.load(io.open(os.path.join(BASE, '00_SISTEMA_Y_FUENTES',
                                      'BASELINE_SNAPSHOT.json'), encoding='utf-8'))

flog.event(fase='FINAL', tipo_evento='cierre',
           objetivo='FASE FINAL DE ANALISIS COMPLETA — paquete analitico del Refugio Climatico',
           resultado=(
               'Carpeta ANALISIS_FINALES_REFUGIO_CLIMATICO sobre baseline CONGELADA v006 '
               'build 12 (29 archivos con SHA-256; auditoria 0 RED / 26 YELLOW / 18 GREEN; '
               'clima re-ejecutado con k_veg por especie). '
               'ENTREGADO: %d PDFs (%d paginas) en 12 carpetas tematicas + %d entregables '
               'hasheados en MANIFIESTO_ENTREGA_FINAL.csv. '
               'SISTEMA: 00_CORPUS_MANIFEST (2.486 archivos inventariados), '
               'ANALYSIS_MASTER_REGISTER (279 analisis catalogados), CROSS_ANALYSIS_MATRIX, '
               'FINAL_METRICS_REGISTRY (%d metricas con script/dato/nivel/pagina, 0 conflictos), '
               'DISCOVERIES_REGISTER (D-001..D-015 con metodo cientifico), '
               'FINAL_GRAPHIC_SYSTEM (ADN IRAXXXDIOS traducido al Refugio). '
               'ANALITICOS: 23 individuales + 8 sintesis tematicas + INDICADORES_CRUZADOS. '
               'GLOBAL: REFUGIO_CLIMATICO_ANALISIS_GLOBAL.pdf (21 pp) con resumen ejecutivo, '
               '9 cadenas interdisciplinares DATO->HIPOTESIS->COMPROBACION->CONCLUSION, '
               'mapas propios de D-015/D-003, FAQ del tecnico municipal esceptico (11 ataques), '
               'auditoria de certeza conclusion a conclusion y roadmap A-E con monitorizacion. '
               'IA: IA_EN_EL_REFUGIO_CLIMATICO.pdf (proceso real, solo Refugio). '
               'VISUAL: objetivo REDIRIGIDO por el usuario a base de control geometrico — '
               '12 reference packs (beauty/clay/clay_sinveg/ao/depth/normal/edges/id_mat + '
               'CAMERA_METADATA) con regla de fidelidad jerarquica HARD/SOFT/FREEDOM y '
               'AI_IMAGE_GENERATION_MANIFEST.csv; piloto H1 pendiente por decision del usuario. '
               'CORRECCIONES DE LA PASADA ADVERSARIAL: ratio x12 justificado con valores sin '
               'redondear (1,9->23,3 %%, cinta fuera del denominador de transito), denominadores '
               'ambito/pisable etiquetados en 4 documentos, 27 glifos fuera de Georgia '
               'sustituidos, bucle infinito de cadenas corregido, medicion de texto optimizada '
               '(10 min -> 3,5 s). VEREDICTO DEL PROYECTO: VIABLE CON CONDICIONES.'
               % (len(pdfs), pp, len(man), len(met))),
           parametros={'baseline': snap['baseline'], 'pdfs': len(pdfs), 'paginas': pp,
                       'entregables': len(man), 'metricas': len(met),
                       'reference_packs': 12, 'hallazgos': 15})
print('CIERRE REGISTRADO · %d PDFs · %d paginas · %d entregables · %d metricas'
      % (len(pdfs), pp, len(man), len(met)))
