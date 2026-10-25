# -*- coding: utf-8 -*-
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '_FORENSIC_PROCESS')))
import flog

flog.event(fase='E03', tipo_evento='cierre_fase',
           objetivo='E03 completa (E03-0..E03-7) sobre v003 congelada',
           resultado=('Tanda hero: 14/14 renders 2560x1600 (7 camaras x mediodia/tarde) en hero_E03. '
                      'Checks automaticos par8 tanda 2: FALLOS 0 (dLum vs E02 max +2.6% <8; H1 ROI sombra '
                      '32.2%>=30; H4-tarde contraste 61.2%>=15; chorros 24px>=3). Ronda unica global E03-6: '
                      'niebla +presencia via atmos_config (micro 5-8 sprites, D2.2-5.5, op 0.12-0.26; columnas '
                      '12 sprites op 0.26-0.08) — sin retoques vista a vista. Veredicto direccion: 13 OK / 1 OK '
                      'con reserva tecnica (H7: las columnas de vapor no se leen con billboard+blending normal '
                      'sobre suelo claro; exigen volumetrica real -> HANDOFF_D5_VRAY.md) / 0 NO-OK. '
                      'Entregas: HOJA_CONTACTO_E03.jpg, COMPARATIVA_E02_E03.jpg (6 pares), ATMOSFERA_NOTES.md, '
                      '_checks_e03.json, HANDOFF_D5_VRAY.md, REGISTRO_E03.md, pipeline reproducible '
                      '(atmos_prep --ejecutar-e03 / render_e03 / checks_e03 / boards_e03 / viewer_e03). '
                      'Frontera: ningun .3dm tocado, v003 congelada, capa E03 en scene_extra.js. '
                      'Previo a E03 (misma orden): aclaracion documental 03B.6 registrada en EVT-000107 '
                      '(27 discos nuevos + 7 recotados = 34 con rol; mantenimiento 56/133 -> 1/160; Carlos III '
                      'presencia consolidada con posicion G2+ pendiente de verificacion municipal).'),
           runs_asociados=[])
print('ok')
