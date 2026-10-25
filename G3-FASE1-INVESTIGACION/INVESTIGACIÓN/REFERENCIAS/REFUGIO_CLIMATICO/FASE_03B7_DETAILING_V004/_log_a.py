# -*- coding: utf-8 -*-
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '_FORENSIC_PROCESS')))
import flog

flog.event(fase='03B7', tipo_evento='hito',
           objetivo='FASE URBANA v004 LIMPIA: conflictos A y B resueltos por regla',
           resultado=('Medicion inicial (URBAN_CONFLICTS_v003.json): 439 mallas hasta 10.1 m dentro de El Corte '
                      'Ingles (133), 173 sobre la Estacion de Cercanias (106, edificio real de 20x7 que v003 '
                      'trataba como punto), arboles v003 dentro del edif 71, franjas E/N en 110/117/124/131. '
                      'CAUSA RAIZ: ninguna regla conocia los poligonos de edificio. SOLUCION v004 (build_all_03b7): '
                      'EDGE_GUARD con 33 manzanas+3 kioscos+estacion; loops RECORTADOS contra fachada (clip<->smooth '
                      'iterado; el arco aplanado de C1-L1 = portico-galeria con tren T-O regenerado encima); cinta '
                      'proyectada con empuje HACIA LA PLAZA (candidatos en todas las aristas — el empuje por '
                      'arista-mas-cercana falla en vertices concavos y metia el eje en la calle de 2 m tras ECI); '
                      'belvedere de anchura variable sobre la cabeza de la Estacion; anclajes validados con la '
                      'HUELLA REAL transformada del bloque (las rejillas de sondas fallaban por el espejo s=-1) y '
                      'deslizamiento sin wrap (una escalera se teletransportaba de -84 a +82). Sondeo final '
                      '_probe7: CERO penetraciones; eje a +3.05 de ECI; 6 escaleras + 3 ascensores anclados sanos. '
                      'Figura B construida: atrio radial + belvedere + senaletica en Estacion, media luna en '
                      'Carmen, aprons en estancos, dosel abierto (colgantes/red recortados sobre la Estacion).'),
           runs_asociados=['EVT-000112', 'EVT-000113', 'EVT-000118'])
print('ok')
