# PANEL A1 · RIBERA 31 · ATLAS DE INVESTIGACIÓN

G3 · Proyectos · UEM · Vivienda temporal para jóvenes · Ribera de Curtidores 31, El Rastro (Madrid)
Versión vigente: **v2 (24-09-2026)**. Formato A1 vertical, 594 × 841 mm, PDF vectorial con imágenes embebidas.

## Contenido de la carpeta

| Archivo / carpeta | Qué es |
|---|---|
| `RIBERA31_PANEL_A1.pdf` | Panel A1 v2 (el que vale). Imprimir al 100 %. |
| `RIBERA31_PANEL_A1_100ppp.png` | Vista previa ráster a 100 ppp. |
| `VERSIONES_ANTERIORES/RIBERA31_PANEL_A1_v1.pdf` | v1: fondo crema y capa 07 mal rotulada como topografía. **No usar.** |
| `DATOS/metrics.json` | Recuentos del inventario OSM por anillo (100–500 m) y por sector de 22,5°, más cercano de cada tipo, longitudes de viario y superficie verde en 500 m. |
| `DATOS/resumen_radio_500m.json` | Lo mismo en versión corta, lista para citar. |
| `DATOS/calle_pendiente_sol_medianeras.json` | Perfil de cota de Ribera, pendiente por tramo, sol del 21-dic por cota con el umbral del 50 %, y saltos entre medianeras. |
| `DATOS/georef.json` | Georreferencia de los 7 PDF de MAPPEADOS, leída de sus puntos GPTS (GeoPDF de QGIS). |
| `LAMINAS_AXONOMETRIA/iso_0…6.png` | Las 7 láminas de la axonometría explotada (máscara con transparencia). |
| `SCRIPTS/` | Código que genera todo (ver abajo). |
| `FUENTES_TIPOGRAFICAS/` | Archivo (varias instancias) y Space Mono, licencia SIL OFL. |

## Bloques del panel y de dónde sale cada dato

Nivel de certeza: **A** medido · **B** inferido · **C** hipótesis de proyecto.

1. **01 · Mapeados.** El MAPA COMPLETO con anillos de 100 a 500 m, los minutos a 80 m/min en línea recta, el eje de Ribera, las estaciones S01–S23 y las bocas de metro de OSM. Al lado, una axonometría explotada de las 7 capas. Cada lámina es la diferencia píxel a píxel entre un mapa y el anterior: MAPA 1…6 y COMPLETO, rasterizados a 220 ppp y recortados a r = 560 m. Van en dimétrica (giro −32°, escala vertical 0,46) y superpuestas en multiplicación. La capa 07 es el **ruido**: son las isófonas del Mapa Estratégico de Ruido de Madrid 2021 (MER 2021), lo que MAPA COMPLETO añade a MAPA 6. Nivel A.
2. **02 · Radio.** Rosa de 16 sectores × 4 temas, tabla de densidad por hectárea en 5 anillos y escalera de distancias. Sale de `INVENTARIO_FISICO_600M.gpkg` (OSM, 8.021 elementos) con centro en el centroide de la parcela (440.017,8 E / 4.473.229,4 N, EPSG:25830). Distancias en línea recta. Nivel A: es lo que el inventario contiene, no la completitud real de la calle.
3. **03 · La calle que baja.** 580 m de Ribera con las dos aceras abatidas: la oeste hacia arriba y la este hacia abajo, invertida. Las fotos son alzados rectificados de Street View 2021-22. Encima van el año catastral de cada frente y los 11 rasgos codificados. Todo se apoya en el perfil de cota real a la misma escala: de Cascorro, 647,0 m, a la Ronda de Toledo, 610,0 m (−36,9 m). Dentro del eje, una franja de color da la pendiente de cada tramo. La cota es la altitud de la cámara de Street View menos 2,5 m, así que es nivel B y tiene ruido local.
4. **04 · Patrones.** P01–P11, cada uno con su caso, proporción n/N, pregunta y micro-calle de posiciones. P01–P09 son lectura visual (B). P10 (9/28 medianeras con salto de 2 plantas o más) y P11 (19/44 frentes posteriores a 1960) salen del catastro (A).
5. **05 · Sol · tiempo · criterios.** Horas de sol por cota en tres fechas y mapas de sombra del suelo del solar, con el modelo 2,5D propio (PB 4,0 m + 3,1 m por planta, nivel B). Sección norte-sur por el frente con el rayo de mediodía solar. El solar en Street View de 2008 a 2022. Red que une hallazgos H-01…H-08, patrones y criterios C1–C7 (nivel C).

## Correcciones respecto al compendio A4

- **H-02, sol de invierno.** El 21-dic, el 50 % del solar recibe 2 h de sol o más a partir de **21,1 m** de cota, no «entre 19,5 y 22,6 m». A 19,5 m solo llega al 33,4 % del solar y a 22,6 m al 65,2 %; los 21,1 m salen de interpolar linealmente entre esas dos cotas y caen dentro de la planta P6.
- **Distancias del bloque 02.** Se miden desde el centroide de la parcela, no desde su borde.

## Cómo regenerarlo

Los scripts se escribieron en el espacio de trabajo de Claude, así que las rutas absolutas (`/home/claude/...`, `/mnt/user-data/uploads/...`) hay que cambiarlas por las de esta carpeta. Dependencias: numpy, pillow, matplotlib, shapely, pyproj y poppler (`pdftoppm`).

1. Rasterizar el recorte de cada PDF de `MAPPEADOS/` a 220 ppp: `pdftoppm -r 220 -x 2046 -y 0 -W 3753 -H 3526`.
2. `georef.py`: lee los GPTS de los PDF y produce `georef.json`. Todos los mapas comparten el mismo marco, x 438.659–441.777 e y 4.472.626–4.473.847 (EPSG:25830).
3. `layers.py`: diferencias entre mapas consecutivos. Después, `plates.py` genera las láminas dimétricas.
4. `osm.py` y `metrics.py`: métricas del inventario OSM, que van a `metrics.json`.
5. `poster2.py`: compone el panel. Usa `kit.py` (primitivas en mm y paleta) y los datos del compendio (`00_INVESTIGACION_COMPLETA/DATOS` y `FIGURAS`).

## Fuentes

- Catastro INSPIRE WFS + OVC (consulta del 23-09-2026).
- `MAPPEADOS/` e `INVENTARIO_FISICO_600M.gpkg` (OpenStreetMap vía QGIS 3.40, 21/22-09-2026).
- Mapa Estratégico de Ruido de Madrid 2021 (Ayuntamiento de Madrid).
- Google Street View 2008–2022: 23 estaciones y 11 fechas del nº 31.
- Modelo de sombras y alzados rectificados propios; scripts en `00_INVESTIGACION_COMPLETA/SCRIPTS`.
