# -*- coding: utf-8 -*-
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '_FORENSIC_PROCESS')))
import flog

flog.event(fase='E03', tipo_evento='hito',
           objetivo='E03-0..E03-3 completados sobre v003 congelada',
           resultado=('E03-0: recalibracion contra 12CA810C (niebla blanca solo en contraluz), FBDF10B9 (coronas + '
                      'lineas rosas sobre granito espejado), 29A08040 (velos de vapor entre discos), 2187306B (mediodia '
                      'duro, reloj siempre legible, estatua presente). E03-1: tex_data2.js (sprite niebla radial + '
                      'corona de chapoteo, data-URL). E03-2: scene_extra.js = 321 sprites (42 boquillas suelo + 8 de '
                      'barandilla de cinta + 3 columnas H7), 191 mallas de agua viva (10 chorros splash + espuma '
                      'perimetral + 12 goteos de embudo + 4 mangueras + 2 rebosaderos) y 40 personas PERSON2 en 8 '
                      'programas, validadas contra 2145 bbox de obstaculos v003; peatones proxy v002 se ocultan. '
                      'E03-3: viewer_e03.html = viewer_e01 + escena v003 (scene_v003.js) + presets mediodia/tarde de '
                      'atmos_config + capa extra + Carlos III en bronce/granito + reloj emisivo +0.35 en tarde (§7.3). '
                      'Refino §7.1 (alocasia 14 seg) NO aplicado: exigiria rehornear la escena v003 congelada; pasa al '
                      'handoff D5/V-Ray. §7.4/7.5 ya construidos en v003. H5 reanclada al eje construido tras 4 '
                      'pruebas (la primera posicion quedaba pegada al pretil; la aproximacion oeste con guinada a la '
                      'plaza es la valida) + caminante determinista anclado al tramo. Servidor 8123 relanzado; leccion '
                      'nueva: --screenshot de Edge falla en silencio con rutas 8.3 (IRAXX_~1) -> usar rutas absolutas '
                      'simples.'),
           runs_asociados=[])
print('ok')
