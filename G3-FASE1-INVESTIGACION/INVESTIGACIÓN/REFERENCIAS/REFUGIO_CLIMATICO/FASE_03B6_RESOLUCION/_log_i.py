# -*- coding: utf-8 -*-
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '_FORENSIC_PROCESS')))
import flog

flog.event(fase='03B7', tipo_evento='cambio_prioridad',
           objetivo='PAUSA 03D (orden del autor) + apertura de rama v004',
           resultado=('03D se pausa ANTES de completar la tanda final: la tanda Cycles en curso se deja terminar '
                      'SOLO como test/baseline visual de v003 y se archiva como 03D_PRE_V004 / BASELINE_VISUAL_v003 '
                      '(QA minimo de validez de archivos; sin iteraciones nuevas, sin postpro, no son renders '
                      'finales). Se conserva todo: brief, MATERIAL_SPEC_03D, ASSET_MANIFEST, CSVs de personas/'
                      'efectos, vistas nombradas, QA, bl_scene.py, SOL_03D.blend, renders. Motivo: antes de la '
                      'visualizacion final se abre la rama arquitectonica FASE 03B.7 -> v004 (v003 INTACTA como '
                      'baseline validada): resolver 2 conflictos urbanos (A: interferencia con edificio; B: '
                      'Metro/Cercanias/estancos como figura espacial abrazada), salto radical de detalle (LOD '
                      'A/B/C), reauditoria completa y preparacion de auditoria municipal integral. La campana '
                      'final de render se retomara sobre el modelo definitivo post-v004.'),
           runs_asociados=[])
print('ok')
