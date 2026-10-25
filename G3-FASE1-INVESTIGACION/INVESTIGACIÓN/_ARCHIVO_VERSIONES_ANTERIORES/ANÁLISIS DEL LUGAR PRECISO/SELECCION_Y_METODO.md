# Selección y método de las cinco láminas

## Lectura de las referencias

El inventario conservado identifica 182 PDF de Refugio Climático y 643 páginas, incluidas revisiones y duplicados. Se revisó visualmente la panorámica disponible de sus familias y las páginas del compendio; se consultaron los métodos de sombra, vegetación y potencial de estancia. No se hizo una auditoría independiente de los resultados numéricos del proyecto de referencia. REFERENCIAS_REVISADAS.json conserva los títulos y rutas del inventario para retomar el trabajo.

## Qué se toma y qué se adapta

| Familia de referencia | Decisión para Ribera |
|---|---|
| Aire, radiación y clima | 01: gráfico temporal con fuente primaria AEMET; 02: posición solar calculada. La estación y el horizonte libre se declaran. |
| Atlas horario de sombras | 02: tres fechas sobre idéntica base y escala. Se muestra la dirección del sol; no se calculan sombras sin alturas. |
| Bordes, ocupación y suelo libre | 03: unión de huellas, áreas métricas y tres radios comparables. |
| Vegetación y ecología | 04: puntos registrados y distancia al árbol más próximo; sin copiar LAI, radios de copa o enfriamiento de Sol. |
| Potencial de estancia y agua | 05: bancos y puntos de agua sobre la misma base; distancias localizables, sin ponderaciones arbitrarias de confort. |
| UTCI, MRT y temperatura superficial | Relevantes, pero necesitan geometría 3D, radiación, materiales, meteorología y un modelo validado. No se asignan grados por intuición. |
| Viento | Requiere dirección/velocidad de entrada, rugosidad y volúmenes; una flecha sobre la calle no demostraría ventilación. |
| Movilidad y accesibilidad | La distancia recta publicada no se presenta como recorrido. Una red accesible necesita cruces, peldaños, pendientes y continuidad comprobados. |
| Agua: balance y enfriamiento | Ubicar una fuente no demuestra disponibilidad, caudal, potabilidad o enfriamiento. Esas variables requieren comprobación. |
| Patrimonio y visibilidad | Requiere bienes y protecciones documentados, observadores y obstáculos precisos. No se asume desde la apariencia de fachada. |
| Estructura, economía y mantenimiento de la propuesta | Son análisis de un proyecto definido; no se trasladan las piezas ni los costes de otro emplazamiento. |

## Lenguaje gráfico

Base cartográfica fija; norte y escala gráfica; variable con unidades; tres radios concéntricos; leyenda junto al dibujo; datos resumidos debajo; conclusión vinculada a una decisión. Color funcional azul/verde/ocre/rojo, fondo blanco y sin marcos decorativos. No se usan mapas de Puerta del Sol como mapas de Ribera.

## Datos y precisión

- Centro aproximado de referencia: longitud -3.707172, latitud 40.407576. No es un levantamiento ni un límite de parcela confirmado.
- Fuente espacial: CATALOGO_PATRONES_600M/DATOS/ambito_osm_recortado.geojson. Se registra su SHA256; se eliminan repeticiones por osm_id.
- Áreas y distancias: EPSG:25830; unión de huellas antes de medir para no sumar solapes. Círculos aproximados por 1.024 segmentos. El error cartográfico de origen no desaparece al calcular más decimales.
- Arbolado: natural=tree, solo puntos. Las alineaciones tree_row no se cuentan como un solo árbol ni se convierten en árboles supuestos.
- Trama de proximidad: celdas de 20 m dentro de 300 m; valor en el centroide de cada celda respecto a árboles del inventario de 600 m. El valor no es constante en el terreno dentro de la celda. Las huellas se superponen para facilitar la lectura, sin clasificar el resto como espacio público.
- Estancia: bancos, drinking_water y fountain se mantienen separados. Geometrías no puntuales se representan por un punto interior para localizar el recurso. No se certifica apertura o funcionamiento actual.
- Clima: AEMET Madrid-Retiro, 1981-2010, referencia histórica explícita. No se presenta como normal 1991-2020 ni como temperatura contemporánea del solar.
- Sol: aproximación NOAA, fechas 21/03, 21/06 y 21/12 de 2026; hora Europe/Madrid convertida a UTC. Azimut desde el norte verdadero; radios geodésicos proyectados. Se omiten refracción, nubosidad, relieve y obstáculos. No equivale a cálculo de radiación ni a un modelo de sombras.

## Fuentes primarias

- AEMET: https://www.aemet.es/es/serviciosclimaticos/datosclimatologicos/valoresclimatologicos?l=3195
- NOAA: https://gml.noaa.gov/grad/solcalc/solareqns.PDF
- Cartografía: © colaboradores de OpenStreetMap, ODbL, https://www.openstreetmap.org/copyright

## Para seguir con precisión

Primero confirmar solar y alturas inmediatas. Después incorporar terreno, copas y obstáculos medidos al cálculo de sombras. Usar esa sombra y meteorología documentada para confort, no la cercanía a árboles como sustituto de una temperatura.
