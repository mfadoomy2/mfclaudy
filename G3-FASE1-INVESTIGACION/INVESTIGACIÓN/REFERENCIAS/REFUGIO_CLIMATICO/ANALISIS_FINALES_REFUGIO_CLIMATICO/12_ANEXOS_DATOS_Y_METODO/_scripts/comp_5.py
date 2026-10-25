# -*- coding: utf-8 -*-
"""COMPENDIO parte 5: representacion (packs de control) y proceso (IA), que cierran el
volumen antes de los anexos."""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from comp_core import (Comp, E, MXW, BASE)  # noqa: E402

RP = os.path.join(BASE, '09_RENDERS_Y_REPRESENTACION', '_pipeline', 'refpacks')
OUT = os.path.join(BASE, '12_ANEXOS_DATOS_Y_METODO', '_partes')
c = Comp(os.path.join(OUT, 'p5.pdf'), 'COMPENDIO ANALÍTICO', 'XIII · REPRESENTACIÓN Y PROCESO')

# ============================================================ XIII · REPRESENTACION
c.seccion('XIII · REPRESENTACIÓN', 'El modelo como base de control, no como render', size=17,
          sub='La imagen de arquitectura miente con facilidad: basta una lente amable y un '
              'atardecer inventado. Este proyecto separa deliberadamente lo que se MIDE de '
              'lo que se MUESTRA, y publica el mecanismo por el que la segunda no puede '
              'contradecir a la primera.')
c.texto('De cada vista se extraen ocho capas: la imagen base con materiales neutros, dos '
        'lecturas volumétricas (con y sin vegetación), la oclusión ambiental, la '
        'profundidad de cámara, las normales de superficie, las líneas de contorno y las '
        'máscaras por familia de material. Con ese paquete, cualquier tratamiento posterior '
        '—incluido el generativo— queda sujeto a la geometría real: no puede mover un '
        'mástil, ensanchar la pasarela ni inventar un edificio.')
c.tabla(['CAPA', 'QUÉ CONTIENE', 'PARA QUÉ SIRVE'],
        [['beauty', 'materiales base y luz solar real de la tarde crítica',
          'referencia de color, escala y relación con la plaza'],
         ['clay', 'material neutro único', 'lectura volumétrica sin distracción de color'],
         ['clay sin vegetación', 'lo mismo, con el verde retirado',
          'la estructura pura: permite regenerar vegetación sin tocar arquitectura'],
         ['oclusión ambiental', 'sombra propia de contacto', 'refuerzo de volumen y apoyo'],
         ['profundidad', 'distancia a cámara codificada de 0 a 250 m',
          'control geométrico duro: fija la posición de todo en el eje de la vista'],
         ['normales', 'orientación de cada superficie en el espacio de cámara',
          'control de forma: fija la curvatura y la inclinación de cada plano'],
         ['líneas', 'contornos extraídos de profundidad y normales',
          'protege barandillas, costillas y perfiles finos que la profundidad sola pierde'],
         ['máscaras de familia', 'granito, vegetación, rosa, agua, contexto, madera, dosel, '
          'monumento', 'permite intervenir en una familia sin alterar las demás'],
         ['metadatos de cámara', 'posición, objetivo, matriz, campo de visión, focal '
          'equivalente, recortes', 'la vista es reproducible exactamente por cualquiera']],
        [1.3, 2.5, 3.2], size=6.6, titulo='XIII.1 · LAS OCHO CAPAS DE CONTROL')
c.tabla(['NIVEL DE FIDELIDAD', 'ELEMENTOS', 'LIBERTAD CONCEDIDA'],
        [['BLOQUEO DURO', 'arquitectura, cámara, estructura, pasarela, escaleras, '
          'ascensores, doseles, mástiles, módulos, agua construida, edificios, Metro, '
          'monumento y geometría urbana principal',
          'ninguna: cualquier desviación invalida la imagen'],
         ['BLOQUEO BLANDO', 'jardineras, mobiliario, distribución y masa general de la '
          'vegetación', 'variación de densidad y textura dentro de su propia huella'],
         ['LIBERTAD CONTROLADA', 'hojas individuales, ramas pequeñas, personas, vapor, '
          'salpicaduras, reflejos, textura superficial, imperfecciones y atmósfera',
          'total: aquí vive lo fotográfico y lo vivo']],
        [1.45, 3.2, 2.35], size=6.6, titulo='XIII.2 · LA REGLA DE FIDELIDAD, JERÁRQUICA')
c.panel('POR QUÉ ESTO IMPORTA EN UN DOSSIER TÉCNICO',
        'Porque la imagen es la parte del proyecto que más viaja y la que menos se audita. '
        'Al publicar las capas de control junto a las imágenes finales, cualquier lector '
        'puede superponerlas y comprobar que lo que ve corresponde con lo que se ha medido. '
        'Es el mismo principio que rige el resto del compendio: el dato lleva su origen '
        'pegado.', alto=0.95)
# contacto de las 12 vistas
c.espacio(3.4)
cams = [d for d in sorted(os.listdir(RP)) if os.path.isdir(os.path.join(RP, d))]
tw = (MXW - 3 * 0.10) / 4
th = tw * 0.625
x = E.MX
k = 0
for cam in cams:
    f = os.path.join(RP, cam, 'beauty.png')
    if not os.path.exists(f):
        continue
    if k % 4 == 0 and k > 0:
        x = E.MX
        c.y -= th + 0.26
        c.espacio(th + 0.3)
    ax = c.p.axes(x, c.y - th, tw, th)
    ax.imshow(E.load_img_small(f, 460), aspect='auto')
    ax.set_xticks([]); ax.set_yticks([])
    c.p.text(x, c.y + 0.03, cam[:18], size=5.0, tracked=True, color=E.GRAYTX)
    x += tw + 0.10
    k += 1
c.y -= th + 0.34
c.y = c.p.caption(E.MX, c.y, 'Las doce vistas de control.',
                  'Siete generales y cinco de detalle, cada una con su paquete de ocho '
                  'capas y sus metadatos de cámara. Cubren la plaza completa, el interior '
                  'del dosel, el huerto, el atrio del Metro, el monumento y el nudo '
                  'constructivo a escala de detalle.', wrap=108)

# ============================================================ XIV · PROCESO
c.seccion('XIV · EL PROCESO', 'Cómo se hizo, con los errores incluidos')
c.texto('Este proyecto se produjo con asistencia de inteligencia artificial, y el dossier '
        'lo declara porque la forma de usarla determina la fiabilidad de lo que se '
        'entrega. La tesis del proceso es que NO fue una secuencia de instrucción y '
        'resultado, sino un ciclo con medición y rectificación en cada vuelta.')
c.tabla(['ETAPA DEL CICLO', 'QUÉ OCURRE', 'QUIÉN DECIDE'],
        [['Entrada', 'el arquitecto fija intención, restricciones y criterio de calidad',
          'humano'],
         ['Lectura', 'se interpreta el contexto real: cartografía, clima, normativa, '
          'preexistencias', 'máquina, verificado'],
         ['Hipótesis', 'se propone una configuración geométrica concreta', 'ambos'],
         ['Generación', 'un generador determinista produce el modelo completo desde '
          'parámetros', 'máquina'],
         ['Medición', 'auditoría geométrica y simulación física INDEPENDIENTES del '
          'generador', 'máquina'],
         ['Error', 'la medición encuentra lo que la intuición no vio', 'máquina'],
         ['Diagnóstico', 'se busca la causa raíz, no el síntoma', 'ambos'],
         ['Rectificación', 'se corrige el generador, no el resultado', 'máquina'],
         ['Regeneración', 'el modelo entero se vuelve a producir', 'máquina'],
         ['Auditoría', 'se vuelve a medir todo, incluidos los módulos que ya pasaban',
          'máquina'],
         ['Conocimiento', 'el hallazgo se documenta y cambia la siguiente decisión',
          'humano']],
        [1.35, 4.3, 1.35], size=6.6, titulo='XIV.1 · EL CICLO, ETAPA POR ETAPA')
c.texto('La consecuencia práctica de este ciclo es que los errores no se ocultan: se '
        'convierten en instrumentos. Estos son algunos de los que cambiaron el proyecto o '
        'el propio método de análisis.')
c.tabla(['ERROR REAL', 'CÓMO SE DETECTÓ', 'QUÉ CAMBIÓ'],
        [['Cuatro auditorías consecutivas devolvieron resultados idénticos sobre un modelo '
          'que había cambiado', 'sospecha ante la coincidencia byte a byte de los '
          'resultados', 'se descubrió que el redireccionamiento de la auditoría había '
          'fallado en silencio: estaba midiendo la versión anterior. Regla nueva: '
          'desconfiar de un resultado que no cambia cuando la entrada sí lo ha hecho'],
         ['La marquesina del atrio penetraba 2,43 m en la estación',
          'módulo independiente de interferencia con volumetrías reales',
          'la boca del Metro está SOBRE la huella del edificio: «delante de la boca» era '
          'dentro. Se voló la marquesina hacia la plaza'],
         ['El zócalo de un edificio de contexto cortaba una calle en el ráster peatonal',
          'una incidencia roja persistente que tres hipótesis no explicaron',
          'se rastreó hasta el triángulo culpable: una banda cerrada sobre una huella '
          'cóncava puentea los entrantes. Se pasó a emisión por arista'],
         ['Nenúfares del tamaño de la balsa entera',
          'revisión visual de cercanía',
          'un asset plano no puede normalizarse por altura: se añadió tope de diámetro'],
         ['Árboles flotando un metro sobre el suelo',
          'inspección de la campaña visual',
          'la simplificación de la malla lejana se comía la base del tronco: se re-apoya '
          'cada nivel de detalle por separado'],
         ['Un ratio publicado como «×12» con cifras redondeadas que daban ×10,5',
          'revisión crítica del propio cliente',
          'el ratio era correcto con valores sin redondear, pero la formulación era '
          'engañosa; además destapó que la pasarela estaba mal incluida en el denominador. '
          'Se corrigieron ambas cosas y se auditaron todos los denominadores del paquete']],
        [1.9, 1.85, 3.25], size=6.4, titulo='XIV.2 · SEIS ERRORES QUE ENSEÑARON ALGO')
c.panel('LO QUE LA MÁQUINA NO DECIDIÓ',
        'Ninguna de las decisiones de proyecto es automática. La forma de las copas, la '
        'altura de la pasarela, la elección de dejar el centro vacío, la apuesta botánica, '
        'el criterio de reversibilidad y la decisión de publicar los resultados incómodos '
        'son decisiones de autor. Lo que la máquina aportó fue capacidad de medir, de '
        'detectar contradicciones, de encontrar fallos del propio instrumento y de '
        'sostener la trazabilidad de más de doscientos análisis — no criterio.', alto=1.05)

n = c.cerrar()
print('COMPENDIO parte 5 ok:', n, 'pp')
