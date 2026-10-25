# -*- coding: utf-8 -*-
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '_FORENSIC_PROCESS')))
import flog

flog.event(fase='03D', tipo_evento='hito',
           objetivo='STOP 03D — tanda baseline archivada como 03D_PRE_V004 / BASELINE_VISUAL_v003',
           resultado=('Tanda Cycles 14/14 completada (H1-H7 x mediodia/tarde, 2560x1600, ~6 min/frame, '
                      '2x RTX 5070 Ti OptiX, tarea b3lox88c1). QA minimo checks_03d.py: 13/14 OK; H4_tarde '
                      'incumple contraste torre/cielo heredado (6.8% < 15%) y por orden de PAUSA queda '
                      'DOCUMENTADO sin iterar (fix trivial de np.bool_ en el propio check, registrado). '
                      'Carpeta renombrada FASE_03D_RENDER_FINAL -> 03D_PRE_V004_BASELINE_V003 (rutas '
                      'internas HERE-relativas, intactas). TODO se conserva: bl_scene.py, SUN_03D.json, '
                      'MATERIAL_SPEC_03D.json, brief, manifiestos, 14 heroes y _checks_03d.json. '
                      'La campana final se ejecutara sobre el modelo definitivo post-v004.'),
           runs_asociados=[])
print('ok')
