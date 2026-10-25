# Leyenda del inventario físico

P = punto; L = línea; A = área/polígono. El ID corto no sustituye el ID OSM.
Los nombres provienen del inventario. Si no hay nombre propio se muestra una descripción del tipo; no se inventan nombres.
Se conserva exactamente la geometría del inventario previo, sin nuevo recorte ni nueva comprobación de campo.
La clasificación principal sirve para dibujar sin duplicados. Todas las categorías originales siguen en `temas`.

| Código | Categoría | Puntos | Líneas | Polígonos |
|---|---|---:|---:|---:|
| EMP | Emplazamiento | 1 | 0 | 0 |
| PAT | Patrimonio y cultura | 85 | 1 | 7 |
| TRA | Transporte | 130 | 33 | 6 |
| COM | Comercio y actividad | 540 | 47 | 7 |
| MOB | Mobiliario y servicios de calle | 508 | 3 | 4 |
| ACC | Accesibilidad y elementos de calle | 718 | 119 | 0 |
| UMB | Accesos y umbrales | 1386 | 6 | 7 |
| BAR | Barreras | 69 | 203 | 5 |
| INF | Infraestructura | 13 | 76 | 1 |
| EQU | Equipamientos y locales | 465 | 36 | 20 |
| EDI | Edificios | 1 | 0 | 1338 |
| VER | Espacio público y verde | 1035 | 12 | 130 |
| VIA | Calles y recorridos | 12 | 902 | 6 |
| DIR | Portales y direcciones | 89 | 0 | 0 |
| OTR | Otros elementos físicos | 0 | 0 | 0 |

## Etiquetas y DXF

El mapa muestra `etiqueta` = ID + nombre. QGIS oculta colisiones para mantener la lectura: acercar el zoom, filtrar una categoría o usar `id_mapa` como campo de etiqueta.
El DXF automático conserva TODOS los textos (uno por objeto), aunque se solapen. Son entidades TEXT editables, no atributos ocultos ni contornos de letras. No se truncan nombres.
DXF: metros, EPSG:25830, plano Z=0. G_P_* / G_L_* / G_A_* = geometrías; T_P_* / T_L_* / T_A_* = textos. LEYENDA queda a la derecha del dibujo.
No usar el DXF como levantamiento topográfico: conserva la precisión y limitaciones del inventario OSM/local.
Para otra exportación manual desde QGIS: Proyecto > Importar/Exportar > Exportar proyecto a DXF, seleccionar las tres capas etiquetadas, CRS EPSG:25830 y escala adecuada (p. ej. 1:1000). Las etiquetas se exportan como TEXT/MTEXT. Guardar una capa como DXF no equivale a exportar las etiquetas del proyecto.
La exportación manual puede omitir etiquetas por colisión; el DXF generado por este script no las omite.
Documentación: https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/qgis/vectorgeneral.html#export-layers-to-dxf

## Repetir sin descargar

Ejecutar ETIQUETAS_Y_DXF_QGIS.py. Se regeneran SOLO los archivos de QGIS_ETIQUETADO; no se modifican el inventario original ni el catálogo.
Conservar registro_ids.json: mantiene los IDs de cada objeto al repetir y añade nuevos sin reutilizar identificadores.
El proyecto nuevo se guarda aparte. No se cierra ni sobrescribe el proyecto abierto. Abrir INVENTARIO_ETIQUETADO.qgz para verlo.