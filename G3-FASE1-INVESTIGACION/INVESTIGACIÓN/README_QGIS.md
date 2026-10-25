# ARCHIVOS PARA QGIS

Los archivos de esta carpeta constituyen una base inicial y no un levantamiento completo.

## Sistema de coordenadas

Las coordenadas están en WGS84. En los GeoJSON se declara CRS84, con orden Longitud, Latitud. En los CSV las columnas se denominan Latitud y Longitud.

## Contenido

- `flujos_peatonales_y_actividades.csv` contiene eventos y horarios confirmados por el Ayuntamiento. La frecuencia horaria y la intensidad real requieren conteos de campo.
- `plantilla_observacion_campo.csv` sirve para registrar observaciones repetidas en los mismos puntos.
- `corralas_y_tipologias_historicas.geojson` contiene una selección inicial de referencias. No es un inventario completo.
- `ocupacion_temporal_rastro.geojson` contiene un eje esquemático. No debe usarse como límite legal ni como geometría definitiva del mercado.

## Uso recomendado

Importar primero los archivos y mantener visible el campo `Estado_Dato` o `Precision_Geometria`. No simbolizar como medición confirmada ningún valor marcado como pendiente, previsto, aproximado o no medido. Sustituir el eje preliminar por la geometría oficial o por un levantamiento antes de calcular superficies o densidades.
