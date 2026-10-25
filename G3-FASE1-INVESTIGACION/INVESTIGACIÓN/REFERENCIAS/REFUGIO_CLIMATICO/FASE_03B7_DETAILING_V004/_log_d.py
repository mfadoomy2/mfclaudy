# -*- coding: utf-8 -*-
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '_FORENSIC_PROCESS')))
import flog

flog.event(fase='03B7', tipo_evento='hito',
           objetivo='REAUDITORIA GEOMETRICA v004: 25 RED -> 0 RED en 11 iteraciones, TODO por regla',
           resultado=('Auditoria clonada a _reaudit7 (A0-A11) + NUEVO modulo A12-EDIFICIOS (medicion '
                      'independiente de penetraciones con alturas reales: la causa raiz del conflicto A entra '
                      'en la auditoria). Iteracion 1: 25R/15Y. Causas raiz resueltas en el GENERADOR: '
                      '(1) mastiles reubicados por EDGE_GUARD aterrizaban sobre ejes declarados, la media luna '
                      'de Carmen, el tren-portico y entre si -> _mast_ok + busqueda de sitio valido + '
                      'MASTS_XY:=posiciones FINALES para toda guarda posterior; (2) el eje montera-espozymina '
                      'cruzaba la cabeza REAL de la Estacion (declarado cuando era un punto) -> re-proyeccion '
                      'DENSIFICADA a 2.75 del offset de fachada validando TODAS las aristas (esquinas); '
                      '(3) CR-2 GENERALIZADA como snap_facade(): jardineras/bancos/balsas contra fachada '
                      'CIERRAN (borde a 2 cm) o ABREN >=1.5 - los margenes 0.6-0.8 fabricaban ranuras-trampa '
                      'de 0.5 m; jardinera cierra tambien contra el tiesto del mastil; fragmentos <2.4/1.8 m '
                      '= residuo de filtros, fuera; (4) arbol: las 4 guardas (disco/cupula/cinta/fachada) '
                      'iteran hasta CONVERGER con margen cinta = 1.45+alcance real del bloque v2; '
                      '(5) trepadora no en mastiles a <2.6 de la cinta; registro tecnico esquiva el tren; '
                      'totem esquiva balsa; verja de Carlos III cenida (3.5x2.6); dintel del portal a 4.7; '
                      'radio minimo de cinta restaurado a 4.75 (habia un quiebro de 0.1 del clip). '
                      'AUDITORIA afinada con honestidad: uniones constructivas del despiece declaradas por '
                      'nombre (fascia/goteron/canaleta EN su tablero; canto EN su banco), pavimento enrasado '
                      '<=6 cm = grafismo pisable (no obstruye bocas ni interpenetra). '
                      'RESULTADO FINAL: 0 RED / 28 YELLOW / 20 GREEN (v003 cerro con ~24 YELLOW de la misma '
                      'clase). invest_urbano + _probe7: CERO penetraciones. ancho_p05 0.71 (fragmentos '
                      'esquina), cobertura 31.5%, galibo_min 2.17 (copa vegetal, doctrina: poda).'),
           runs_asociados=['EVT-000139', 'EVT-000140'])
print('ok')
