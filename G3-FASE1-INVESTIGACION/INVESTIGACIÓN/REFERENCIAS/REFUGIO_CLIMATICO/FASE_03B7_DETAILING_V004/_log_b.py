# -*- coding: utf-8 -*-
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '_FORENSIC_PROCESS')))
import flog

flog.event(fase='03B7', tipo_evento='hito',
           objetivo='DETAILING WAVE 1 INTEGRADO: LOD B/C en 28 familias + detalle de sitio, urbano sigue LIMPIO',
           resultado=('detailing_03b7.upgrade_blocks enriquece/sustituye 28 familias (mastiles: placa+pernos+'
                      'abrazaderas+valvula; pods: costuras+pletinas+ventanas; gotas: tapa+valvula+rebosadero; '
                      'escalera: 35 narices+montantes+pletina+luminaria; ascensor: jambas+botonera+caseton+rejillas; '
                      'vegetacion v2 con ramificacion real y especies §7.1/§17; discos: kingpost+tensores+manguitos+'
                      'goteo). site_details añade fascia/goteron/canaletas/juntas/sumideros/LED de cinta, retícula '
                      'de pavimento+registros+alcorques, Carlos III v2 (molduras/patas/bicornio/verja), Correos '
                      '(3 filas de huecos+portada+balcon), costillas de Estacion, cornisas de kioscos. Ganchos '
                      'inline: pletinas de balaustre, canto+mechinales de jardinera, canto+patas de banco, '
                      'aro+gargola+pendolas de balsa. DOS regresiones detectadas por sonda y corregidas POR REGLA: '
                      '(1) copa arbol v2 alcanza 3.9 m > margen fijo 3.0 -> margen = alcance real del bloque '
                      '(_blk_reach, autoadaptativo); (2) kiosco 74 (Carmen, 76 m2) faltaba en la lista MANUAL de '
                      'kioscos-guard -> lista derivada por regla del barrido (area<80 en ambito). '
                      'invest_urbano v004 final: CERO penetraciones en 79 edificios del ambito con la escena '
                      'detallada horneada. Masters ~11.5 MB (v003 ~7 MB): el detalle es geometria real.'),
           runs_asociados=['EVT-000121'])
print('ok')
