# Análisis del lugar preciso

Trabajo incremental. Todos los resultados, datos, scripts y revisiones se guardan aquí. Los catálogos anteriores permanecen intactos.

## Selección de referencias y entregas

Se adopta el lenguaje analítico de Refugio Climático: cartografía métrica repetida, variable explícita, escala compartida, gráficos vinculados al mapa y conclusión espacial. Fondo blanco; el color solo codifica datos. Los resultados de Puerta del Sol no se trasladan a Ribera.

1. Clima de referencia: estación Madrid-Retiro; temperatura y lluvia mensuales. Fuente primaria AEMET. No es una medición en el solar.
2. Geometría solar: trayectoria para la posición de estudio, fechas y horas declaradas. No equivale a sombra sobre la calle.
3. Ocupación edificada: unión de huellas OSM, superficie y relación lleno/vacío. No se deduce permeabilidad del suelo.
4. Arbolado: localización registrada y distancias en planta. Sin inventar copas ni temperaturas.
5. Estancia y agua: bancos, fuentes y distancias geométricas. No se certifican potabilidad, acceso o funcionamiento actual.

## Referencias consideradas

CLI-01 SOMBRA, CLI-02 RADIACION, CLI-03 MRT, CLI-04 UTCI, CLI-05 AIRE, CLI-06 VEGETACION, CLI-07 AGUA, CLI-08 VIENTO, CLI-09 CONFORT POR PROGRAMA, CLI-10 ESCENARIOS DE FALLO; movilidad y accesibilidad; contexto y transporte; agua y ecología; material y mantenimiento; uso social; economía; patrimonio; atlas de sombras por hora y compendio analítico.

## Criterio de precisión

UTCI, temperatura radiante, temperatura de pavimento y viento local requieren entradas climáticas y geométricas que aquí aún no están verificadas. No se fabricarán mapas con grados ni velocidades. Los cálculos cartográficos se harán en EPSG:25830 sobre el archivo OSM existente, conservando la precisión de esa fuente. Centro de referencia aproximado: -3.707172, 40.407576. No sustituye el límite de parcela.

## Continuación

Cada PDF individual se guarda al finalizar. El PDF conjunto se actualiza después de cada lámina. El archivo ESTADO.json registra lo completado. Para un análisis de sombras real: completar alturas verificadas, terreno y volúmenes; para confort térmico: añadir meteorología, materiales y validación.
