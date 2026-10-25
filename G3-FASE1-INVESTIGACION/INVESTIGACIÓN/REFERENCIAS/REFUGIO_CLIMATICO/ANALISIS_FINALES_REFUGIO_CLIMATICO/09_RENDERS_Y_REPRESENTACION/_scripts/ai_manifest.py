# -*- coding: utf-8 -*-
"""FASE FINAL - AI_IMAGE_GENERATION_MANIFEST.csv: una fila por vista con intencion,
controles, locks, luz, poblacion, atmosfera y destino editorial. El piloto es H1."""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(BASE, '09_RENDERS_Y_REPRESENTACION')
MONT = os.path.normpath(os.path.join(BASE, '..', '..'))
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402

CTRL = 'beauty+depth+normal+edges+id_mat+clay_sinveg+CAMERA_METADATA.json'
HARD = ('arquitectura, camara, estructura, pasarela, escaleras, ascensores, canopies, '
        'mastiles, pods, agua construida, edificios, Metro, Carlos III, geometria urbana')

ROWS = [
    dict(camera_id='H1', piloto='SI — LA VISTA DEL METODO',
         intencion='la sala de estar urbana: primera imagen del proyecto, nivel de ojo',
         luz='tarde dorada de julio, sol bajo lateral', estacion_hora='mediados de julio · 19:00',
         poblacion='densa y diversa: estancia en bancos, ninos en splash, paseantes',
         atmosfera='calida, ligera calima, vegetacion exuberante pero contenida en sus huellas',
         libertad='follaje, personas, vapor de niebla, reflejos en lamina, patina del granito',
         objetivo='portada del ANALISIS GLOBAL y de la familia entera',
         pdf_destino='REFUGIO_CLIMATICO_ANALISIS_GLOBAL + INDICE + portadas'),
    dict(camera_id='H7', piloto='no',
         intencion='la propuesta completa desde el aire: orden de copas, cinta y claro',
         luz='tarde, sombras largas legibles', estacion_hora='julio · 18:30',
         poblacion='media, granulada (escala urbana)', atmosfera='clara, Madrid al fondo',
         libertad='follaje, gente diminuta, trafico lejano', objetivo='ATMOSFERA seccion 01',
         pdf_destino='ANALISIS_GLOBAL §01 + REFERENCE_PACKS'),
    dict(camera_id='H4', piloto='no',
         intencion='el corredor visual protegido: el dosel enmarca Correos y el reloj',
         luz='tarde con el reloj iluminado', estacion_hora='julio · 19:30',
         poblacion='fluida en el eje, estancia en los bordes', atmosfera='reverente, patrimonial',
         libertad='cielo, banderas, gente, palomas', objetivo='COMPARACION patrimonio §13',
         pdf_destino='ANALISIS_GLOBAL §13 + PAT-01'),
    dict(camera_id='F1_INTERIOR_DOSEL', piloto='no',
         intencion='estar debajo: la luz filtrada por hojas y microalgas (los -28 K visibles)',
         luz='contraluz filtrado, motas', estacion_hora='agosto · 16:00 (hora critica)',
         poblacion='2-3 figuras en sombra, reposo', atmosfera='verde, acuosa, refugio',
         libertad='follaje TOTAL, causticas de microalgas, polvo en luz',
         objetivo='EXPLICACION del mecanismo (CLI-03)', pdf_destino='ANALISIS_GLOBAL §05-II + CLIMA_SINTESIS'),
    dict(camera_id='H3', piloto='no',
         intencion='el agua jugable al mediodia critico: la plaza que refresca jugando',
         luz='mediodia duro (contraste maximo)', estacion_hora='agosto · 14:00',
         poblacion='ninos + familias en splash', atmosfera='vital, salpicaduras, brillos',
         libertad='agua viva, gotas, reflejos, ropa de verano', objetivo='ATMOSFERA agua',
         pdf_destino='AGU-01 + ANALISIS_GLOBAL §08'),
    dict(camera_id='F2_HUERTO', piloto='no',
         intencion='el programa mas protegido: huerto productivo bajo el dosel (-5,9 K)',
         luz='manana suave', estacion_hora='septiembre · 10:00 (maiz alto)',
         poblacion='2 vecinos cuidando bancales', atmosfera='domestica, fertil',
         libertad='cultivos, herramientas, tierra, mariposas', objetivo='EVIDENCIA social',
         pdf_destino='SOC-02 + AGU-02'),
    dict(camera_id='F3_ATRIO_ESTACION', piloto='no',
         intencion='la puerta climatica: salir del Metro a la sombra',
         luz='tarde, contraste boca/plaza', estacion_hora='julio · 18:00 (punta)',
         poblacion='flujo denso saliendo, mezcla de edades', atmosfera='urbana, dinamica',
         libertad='gente en movimiento, senaletica luminosa', objetivo='EVIDENCIA cadena Metro x clima',
         pdf_destino='URB-01 + ANALISIS_GLOBAL §14'),
    dict(camera_id='F4_CARLOS_III', piloto='no',
         intencion='el rey en su jardin: el monumento con el nuevo fondo vegetal',
         luz='tarde calida', estacion_hora='junio · 19:00',
         poblacion='turistas fotografiando, estancia perimetral', atmosfera='iconica renovada',
         libertad='cielo, palomas, personas', objetivo='COMPARACION patrimonio',
         pdf_destino='PAT-01 + PATRIMONIO_SINTESIS'),
    dict(camera_id='H5', piloto='no',
         intencion='caminar a +6: el mirador en movimiento sobre el jardin',
         luz='atardecer', estacion_hora='julio · 20:30',
         poblacion='paseantes en la cinta, plaza viva abajo', atmosfera='panoramica, dorada',
         libertad='cielo, ciudad al fondo, gente', objetivo='ATMOSFERA cinta (y su honestidad: mirador, no estancia)',
         pdf_destino='CLI-09 + MOVILIDAD_SINTESIS'),
    dict(camera_id='H6', piloto='no',
         intencion='el bosque estructural con los pods rosa como faros de programa',
         luz='tarde', estacion_hora='julio · 18:00',
         poblacion='media, apropiacion informal (skate lejos, lectura)', atmosfera='lúdica seria',
         libertad='gente, sombras vegetales, textura granito', objetivo='ATMOSFERA §06',
         pdf_destino='ANALISIS_GLOBAL §06'),
    dict(camera_id='H2', piloto='no',
         intencion='el frente oeste con la escalera-viga: la escala del kit de partes',
         luz='manana lateral', estacion_hora='junio · 11:00',
         poblacion='ligera', atmosfera='constructiva, nitida',
         libertad='cielo, vegetacion de borde', objetivo='EVIDENCIA tecnica',
         pdf_destino='TEC-01 + CONSTRUCCION_SINTESIS'),
    dict(camera_id='F5_DETALLE_NUDO', piloto='no',
         intencion='el nudo mastil-hoja 1:5: cables, casquillos, tensores — el modelo aguanta la camara',
         luz='tarde rasante que dibuje la tornilleria', estacion_hora='julio · 19:00',
         poblacion='ninguna', atmosfera='material, precisa',
         libertad='patina, reflejos metalicos, cielo', objetivo='EVIDENCIA constructiva',
         pdf_destino='TEC-02 + IA_EN_EL_REFUGIO (proceso)'),
]

CAMPOS = ['camera_id', 'piloto', 'intencion', 'controles', 'hard_lock', 'soft_lock',
          'libertad', 'luz', 'estacion_hora', 'poblacion', 'atmosfera', 'objetivo',
          'pdf_destino']
dst = os.path.join(OUT, 'AI_IMAGE_GENERATION_MANIFEST.csv')
with open(dst, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=CAMPOS)
    w.writeheader()
    for r in ROWS:
        r2 = dict(r)
        r2['controles'] = '_pipeline/refpacks/%s/ · %s' % (r['camera_id'], CTRL)
        r2['hard_lock'] = HARD
        r2['soft_lock'] = 'jardineras, mobiliario, distribucion y masa vegetal (dentro de id_mat)'
        w.writerow({k: r2.get(k, '') for k in CAMPOS})

flog.event(fase='FINAL', tipo_evento='ai_manifest',
           objetivo='AI_IMAGE_GENERATION_MANIFEST.csv: 12 vistas, piloto H1, locks jerarquicos',
           resultado='12 filas con intencion/controles/locks/luz/poblacion/atmosfera/destino; '
                     'regla: pack->generacion->comprobacion geometrica->correccion->final; '
                     'metodo se congela SOLO tras el piloto H1')
print('manifest: 12 filas · piloto = H1')
