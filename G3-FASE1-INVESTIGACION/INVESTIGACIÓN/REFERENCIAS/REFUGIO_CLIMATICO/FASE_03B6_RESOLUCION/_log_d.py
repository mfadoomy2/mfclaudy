# -*- coding: utf-8 -*-
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '_FORENSIC_PROCESS')))
import flog

flog.event(fase='03B6', tipo_evento='hito',
           objetivo='Reauditoria geometrica 03B.5 completa sobre v003: convergencia',
           resultado=('8 iteraciones REGENERAR->REAUDITAR (EVT-000064..094). Resultado final: RED 0, YELLOW 26, '
                      'GREEN 19 (v002: RED 36 / YELLOW 22 / GREEN 15). Itinerarios: 6/6 APTO, cinta APTO CON '
                      'ASCENSOR (3 uds); v002 tenia montera NO APTO y cinta NO APTO. Correcciones de METODO del '
                      'auditor clonado (originales intactos), cada una documentada en el codigo: (1) escaleras y '
                      'ascensores MEDIDOS sobre bloques STAIR_SB/LIFT_TOWER en vez de asumidos; (2) radio de cinta '
                      'sobre el eje CONSTRUIDO; (3) barandilla medida por niveles de tubo; (4) maint_check sin '
                      'break en la primera celda (artefacto 0.707); (5) viveros desde el JSON v003; (6) colision '
                      'intra-bloque y contactos de diseno documentados (tren-jardinera, lab-mastil) = intencionados; '
                      '(7) paso estrangulado exige dos paredes enfrentadas + dos aperturas (la piel de un objeto '
                      'aislado y el rincon concavo daban WIDTH=0.50 por construccion del raster; v002 arrastraba '
                      'esa clase de falsos pasos); (8) relevancia de red: huecos interiores a parterres se agregan '
                      'en YELLOW explicito (10 uds), no se ocultan. Hallazgo clave del proceso: la regeneracion '
                      'uniforme de trenes violaba los recortes de metro de 03A (POD_TRAIN a 0.22 m de Cercanias); '
                      'se sustituyo por puertas POR RETIRADA de capsulas conservando posiciones aprobadas.'),
           runs_asociados=['EVT-000064', 'EVT-000075', 'EVT-000079', 'EVT-000082', 'EVT-000086', 'EVT-000089', 'EVT-000093'])
print('ok')
