# -*- coding: utf-8 -*-
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '_FORENSIC_PROCESS')))
import flog

flog.event(fase='03B7', tipo_evento='hito',
           objetivo='DETAILING CERRADO: ronda unica de correccion tras controles 50m/10m/2m/50cm',
           resultado=('Controles ronda 1 (16 tomas, 4 dianas x 4 distancias, _control/): funcionaban abrazaderas/'
                      'valvulas/pletinas (gotas, mastiles), balaustres+fascia belvedere, costillas canopy, bancos '
                      'canto+patas, juntas pavimento, alocasias/gramineas. TRES fallos visuales detectados y '
                      'corregidos por regla en UNA ronda: (1) Carlos III no se leia como grupo ecuestre y la peana '
                      'LEVITABA 1.1 m (bug v003 visible al acercarse: mk.box z=base, peana z1.6 sobre grada 0.5) '
                      '-> grupo coherente: peana apoyada, caballo PISANDO la peana (3 patas + mano alzada), cuello/'
                      'cabeza, jinete con brazo y bicornio; (2) VEG2_TREPADORA era una cadena de ESFERAS (enunciado: '
                      'no bolas verdes) -> helice + abanicos foliares adheridos + derrame con guias; (3) la bola-'
                      'arbusto vivia DENTRO del bloque de mastil (tiesto+esfera) -> mata de abanicos en el tiesto. '
                      'VEG2_BAJA tambien pierde sus 2 esferas (abanicos bajos + 14 gramineas). Ronda 2 (8 tomas): '
                      'grupo ecuestre legible a 10 m y 2 m, trepadoras como enredadera real, cero esferas en escena. '
                      'Tras la correccion: _probe7 y invest_urbano v004 = CERO penetraciones (79 edificios). '
                      '29 familias enriquecidas. Los controles a 50 cm sostienen la lectura (viewer clay/material; '
                      'materiales finales seran de la campana post-v004).'),
           runs_asociados=['EVT-000128', 'EVT-000129'])
print('ok')
