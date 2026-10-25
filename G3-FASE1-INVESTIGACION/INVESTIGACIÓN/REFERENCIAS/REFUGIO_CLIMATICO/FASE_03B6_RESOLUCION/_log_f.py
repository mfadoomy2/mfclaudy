# -*- coding: utf-8 -*-
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '_FORENSIC_PROCESS')))
import flog

flog.event(fase='03B6', tipo_evento='aclaracion_documental',
           objetivo='Reconciliar recuentos tras aprobacion de 03B.6 (orden del usuario, sin cambio geometrico)',
           resultado=('Recuentos VERIFICADOS contra geometria_maestra_v003.json y a9_maint.json: '
                      'discos NUEVOS = 27 (23 sombra-cinta +8.30, 4 sombra-corredor +5.0); re-cotados = 7; '
                      'total con rol v003 = 34. La cifra "30 discos nuevos con rol" de 03B6_SINTESIS.md era '
                      'erronea (mezclaba nuevos y re-cotados) -> corregida. Mantenimiento: v002 56/133 sin '
                      'acceso -> v003 1/160 (el 1 = DISC-23 CANOPY/BAJANTE, holgura 2.06, YELLOW); la linea '
                      '"46+ -> 0" del PDF (P3) era erronea -> corregida y PDF regenerado. Carlos III: se '
                      'reformula en sintesis/diff/PDF como PRESENCIA CONSOLIDADA en v003 con posicion y escala '
                      'G2+ PENDIENTES de verificacion municipal (el JSON ya lo decia: fuente 0F53E6F0, '
                      'pendiente plano municipal). Sin errores geometricos: no se toca el modelo.'),
           runs_asociados=[])
print('ok')
