# Qué heredamos de la megaestructura macarra

Revisión de proyecto del 19.10.2026. Modelos nuevos, sin modificar los originales.

La referencia principal comprobada es `/Users/adam/Downloads/MEGAESTRUCTURA_MACARRA/modelo/MEGAESTRUCTURA_MACARRA.3dm`: 1.707 objetos y 23 capas. Se han revisado también sus vistas de conjunto y detalle. Su documento declara una arquitectura fantástica, sin cálculo estructural. La versión V4 es otro desarrollo posterior; sus cálculos no validan los modelos de esta entrega.

## La pérdida que había que reconocer

Las últimas plantas conservaban la habitación individual, el vestidor y la bow, pero tendían a hacer una casa cerrada con dormitorios alrededor de una sala. La referencia original organizaba una red de enlaces que se ensanchan y se vuelven lugares. Habíamos desarrollado mejor el interior doméstico que la relación entre casas, recorrido y soporte.

Los ocho modelos 3D conservan esas plantas para que se puedan juzgar y editar. Los tres ensayos sobre la parcela comprueban distintas formas de compartir; no son tres edificios completos para cuarenta habitantes ni una solución final de iluminación.

## Anatomía y organización: transferencias distintas

| Mecanismo de la referencia | Traducción en esta entrega | Qué falta o qué se descarta |
|---|---|---|
| Enlace que se ensancha y se habita | E01: encuentro mayor; E02: continuidad de una casa de ocho; E03: dos ámbitos y un umbral. | Todavía no constituyen la doble trenza vertical de toda la megaestructura. La unión debe juzgarse por usos y recorridos, además de su forma. |
| Suelo, soporte y piel separados | Bandeja con cordones y diagonales, apoyos bajo la vivienda, techos privados y sobretechos separados. | Los tubos y uniones nuevos son hipótesis. No tienen un dimensionado estructural propio. |
| Troncos y ramas | En los ensayos de parcela los troncos soportan la bandeja desde la planta baja y ramifican bajo el suelo superior. | No se introducen en el centro de habitaciones o accesos. Falta comprobar cargas, estabilidad, uniones y cimentación. |
| Tiendas íntimas dentro de una infraestructura común | Habitación individual cerrada, vestidor transitable, bow pequeña con asiento cóncavo y tablero por canto corto. | La igualdad de prestación privada es intencionada; no obliga a repetir la organización colectiva. |
| Telas con funciones diferentes | Sobretecho individual ventilado; cubierta común más alta y plegada; cámara y paños translúcidos separados del techo privado. | Son superficies diseñadas para comparar espacialmente. No se ha realizado búsqueda de forma por equilibrio, pretensado, análisis de viento o drenaje. |
| Organización visible | Conducciones cian y magenta, estructura de borde y acceso colectivo legible. | Los colores no prueban funcionamiento. No se copian órganos inventados como instalaciones reales. |
| Agua suspendida y depósitos | No se multiplican por las casas. | La necesidad, carga, higiene y mantenimiento deben justificar cada depósito antes de incorporarlo. |
| Laberinto de cotas y vistas | Galería a la vivienda desde la escalera y ascensor; planta baja compartida bajo las bandejas. | Aún no se apilan los grupos ni se resuelve la forma completa. No se inventa una red de escaleras que termine sin descarga a calle. |

## La planta baja cambia el proyecto

La corrección del usuario es clara: en estos tres ensayos la planta baja no es vivienda privada. Es infraestructura común del conjunto, con relación a la calle. Se modelan sala, comedor y cocina del edificio, taller y cuidados. Cocina, almacenaje y aseos se integran en una franja continua del borde sur, con llegada lateral a los WC. La salida de escalera queda abierta, sin bloque de baños enfrente. Los núcleos y el programa no se concentran como una isla en el centro de la sala.

La primera vivienda se sitúa a +4,20 m. La secuencia es calle -> planta baja común -> escalera o ascensor -> galería -> casa compartida -> habitación. La cota +4,20 es una hipótesis geométrica para probar la sección; no un resultado de soleamiento ni una altura de ordenación aprobada.

La escalera tiene dos tramos de doce contrahuellas de 17,5 cm y meseta a +2,10 m. El ascensor incluye cabina en la parada superior, hueco, guías, foso y puertas; la puerta inferior se representa cerrada cuando la cabina está arriba. Son geometrías de estudio, sin selección de fabricante o comprobación normativa.

La llegada superior se lleva al extremo este, al lado del núcleo, por un paso de servicios con puertas de baño laterales. Se llega a los dormitorios sin atravesar baños. Esta decisión mejora la conexión física pero obliga a valorar la calidad de esa llegada: el filtro de servicio no debería convertirse en la identidad principal de la casa.

## Tres ensayos, la misma capacidad

- **E01_ENCUENTRO:** ocho personas, derivado de V01_D. Una estancia de reunión mayor entre dos ámbitos domésticos. Permite probar el cruce como un lugar, aunque cuesta más superficie.
- **E02_COMUNA:** ocho personas, derivado de V01_S. Una casa continua; es la referencia de compartir con menor suelo entre estas tres agrupaciones. Sigue teniendo una dirección longitudinal fuerte.
- **E03_DOS_CLAROS:** ocho personas, derivado de V02_P. Dos grupos de cuatro con cocina y comedor propios y un umbral de encuentro. Aporta elección y autonomía, con más duplicación de programa.

Mi criterio: usar E02 para revisar la intensidad de lo compartido, E03 para conservar capacidad de retirarse y E01 para estudiar cuándo el recorrido merece ensancharse en una estancia. Ninguna gana por parecerse más a la silueta de la referencia.

## Superficie y luz: asuntos abiertos

Una planta baja común consume superficie y recursos. La cuenta anterior de cinco V01_S ya sumaba unos 1.348,55 m² de envolvente de estudio para cuarenta personas, antes del programa general, núcleos y estructura. No se puede añadir todo el común inferior y seguir afirmando que cabe en 1.500 m². El siguiente ajuste debe decidir qué se comparte por grupo y qué pertenece al edificio, reduciendo duplicaciones sin perder intimidad.

Los ocho modelos aislados siguen con suelo a cota 0 para compararlos. Los tres ensayos de parcela tienen suelo común a 0 y vivienda a +4,20. No deben confundirse sus cotas.

El contexto 3D usa huellas catastrales y alturas hipotéticas de plantas por 3,10 m. No es un levantamiento. Varias bow siguen necesitando comprobar cielo visible y edificios enfrentados; la luz cenital de las salas tampoco acredita iluminación de los dormitorios. No se declara resuelto el sol, ni se ha optimizado el conjunto vertical.

## Abrir y editar

`modelos/TODAS_LAS_PLANTAS_3D_COTA0.3dm`: ocho plantas juntas, separadas y sin apilar. Los originales individuales están en la misma carpeta. Cada archivo tiene una copia `_INTERIOR` con las cubiertas ocultas. Los cuerpos principales son extrusiones editables; telas, tubos y personas son mallas separadas por capas.

`E01`, `E02` y `E03`: ensayos con parcela, planta baja común, primera vivienda, galería y núcleo. Activar `90_CONTEXTO` para ver los vecinos de altura hipotética. El archivo completo muestra las cubiertas; `_INTERIOR` permite ver las habitaciones.

`vistas/`: imágenes de la geometría, plantas y secciones. `INDICE_VISUAL.html`: acceso a todas las comparaciones. `verificacion/`: comprobaciones y alcance. Los modelos son de anteproyecto, no documentación de ejecución.


## Decisión pendiente: aseo de planta baja

Se dibujaron dos como hipótesis de apoyo al uso prolongado del espacio común, no como una exigencia comprobada del enunciado. La cantidad no está justificada ni aceptada; no debe fijarse como programa definitivo. Se ha retirado el volumen aislado de la llegada de escalera. El debate sobre necesidad, cantidad y carácter del aseo inferior sigue abierto.
