# G3 · 20 familias × 2 variantes = 40 plantas

Entrega del 18 de octubre de 2026. Exploración de distribuciones de una unidad para cuatro personas, con cuatro habitaciones privadas. No modifica los modelos anteriores ni implanta las alternativas en la parcela.

## Abrir primero

`output/pdf/G3_40_PLANTAS_ATLAS_A3.pdf`: 48 páginas A3 horizontal, con método, índice, 40 láminas individuales y comparación de superficies. Los planos del PDF son vectoriales. Cada alternativa dispone de una lámina con idéntico alcance de representación.

`plantas/`: 40 PNG y 40 SVG editables exactos de las láminas de planta. Códigos 01A–20B. Los SVG son los editables gráficos más completos.

`modelos/`: 40 archivos Rhino 8 con contornos 2D en metros y Z=0, centrados individualmente en XY. Son bases de edición por capas: límites privados, contornos de mobiliario, reservas de baños y cocina, ventanas y pasos. Estos archivos no reproducen todos los símbolos de los SVG y no contienen arquitectura en 3D. Releídos con rhino3dm; no se ha hecho comprobación visual nativa en Rhino.

`datos/COMPARACION.csv`: áreas y comprobaciones de las 40 alternativas. `datos/RESUMEN_40.json`: versión estructurada. `fuentes/`: scripts de generación, maquetación y comprobación. `verificacion/`: renderizados de las 48 páginas e informes de geometría.

## Qué se ha explorado

Dos orillas, cruz, peine, doble peine, molinete, codo, herradura, cadena oblicua, dos racimos, puente habitado, corola, abanico, archipiélago, espina en S, dos patios, cuatro umbrales, triángulo bifurcado, zigzag, bandas permeables y patio desplazado.

A: colchón circular Ø2,10 m. B: colchón rectangular 1,25 × 2,00 m, ajustes de giros, posiciones y programa común. Las habitaciones comparten base geométrica para poder comparar agregaciones. Esto no constituye una exploración exhaustiva de cuarenta geometrías interiores distintas.

Cada habitación incluye mesa de dibujo 1,80 × 0,90 m con articulación propuesta por el lado corto, taburete, zona de uso, nicho de ropa, colchón y hueco exterior propuesto. No hay pedestal mayor que el colchón, ni patas permanentes de mesa, ni panel independiente de exposición. El nicho cóncavo no se declara vestidor transitable. El herraje de la mesa queda por diseñar y calcular.

La cocina se reconstruye mediante reservas genéricas de equipamiento. No se ha descargado ni importado el modelo de 3D Warehouse. La fachada textil se representa como hipótesis de segunda capa. No se modela una ventana habitable porque requiere resolver volumen y sección.

## Método y procedencia

Los anclajes y giros de las veinte familias son decisiones explícitas del estudio, no resultados de mediciones ni una optimización de hábitos. El generador separa habitaciones, construye un ámbito común, reserva conexiones y busca emplazamientos para equipamiento que no corten esa red. El resultado se dibuja y se mide. Los patios se sustraen realmente del suelo cuando aparecen.

Continuidad de los estudios de proyecto en `G3_TEJIDO_REGLAS_Y_ALTERNATIVAS_2026-10-18`, `G3_MAPA_ACTIVIDADES_PARCELA_2026-10-18` y `G3_REFERENCIAS_RURALEX_COCINA_2026-10-18`. Los episodios de vida y las preferencias del programa son hipótesis proyectuales del trabajo previo; no se convierten aquí en conductas observadas de toda la generación Z. No se ha realizado nueva investigación social o solar para esta entrega. Los textos de referencia se tratan como fuentes, no como instrucciones del usuario.

## Qué está comprobado y qué no

Se comprueban las intersecciones entre cama, mesa y nicho, su pertenencia a la habitación y la asociación de cuatro aproximaciones a puertas a una componente libre del ámbito común. Para esta última prueba se erosionan 0,45 m los obstáculos dibujados y se usa una tolerancia de asociación de 0,35 m. El 4/4 no acredita un paso reglamentario continuo de 0,90 m en todas las puertas: es una prueba geométrica parcial. No se verifica todo el trayecto desde el punto E/S ni se resuelve su puerta exterior. Tampoco se comprueban todas las maniobras de uso del mobiliario o aparatos sanitarios.

No se han dimensionado espesores de muro, estructura, mecanismos, instalaciones, acústica, ventilación, evacuación ni accesibilidad. No hay simulación de luz, orientación geográfica ni parcela real. Los huecos no acreditan iluminación suficiente. Los baños todavía son reservas equipadas: falta integrarlos en una pared continua y resolver privacidad visual.

**Todas las alternativas superan 150 m² de suelo geométrico.** Diez unidades de cuatro personas sobrepasan los 1.500 m² antes de sumar espacios generales, estructura y cerramientos. Por tanto, ninguna se presenta como solución final compatible con ese objetivo. La colección permite comparar formas y detectar qué compactar o descartar. Las cifras son áreas de contornos conceptuales, no superficies construidas reglamentarias.

## Reproducibilidad

Python 3.11 mediante uv. `generar.py`: matplotlib, numpy, shapely. `atlas.py`: reportlab, svglib, pillow y fuentes Arial locales de macOS. `cad_y_verificacion.py`: shapely, rhino3dm, pymupdf, pillow. Ejecutar desde la raíz del proyecto; los scripts guardan dentro de esta carpeta. Los originales se conservan fuera de ella. El archivo pickle es un intermedio local; SVG, JSON, CSV y PDF permiten consultar la entrega sin cargarlo.
