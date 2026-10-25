# 00_INVESTIGACION_COMPLETA · Ribera de Curtidores 31
Documento vigente: `RIBERA_31_COMPENDIO_INVESTIGACION.pdf` (v1, 2026-09-23, 43 páginas, A4).

## Carpetas
- `RECORRIDO_STREETVIEW_2026-09-23/` — 23 panorámicas completas S01–S23 (8192×4096) + 11 históricas del nº 31 + `G3SV_metadatos.json` (panoid, fecha, coordenadas, fechas disponibles).
- `DATOS/CATASTRO_2026-09-23/` — GML originales del Catastro (INSPIRE CP/BU, DNPRC del 31).
- `DATOS/DERIVADOS/` — GeoJSON EPSG:25830 (edificios, partes, parcelas, parcela 31), censo de frentes, sombras (`sombras.npz`, `sombras_resumen.json`, `sol_por_altura.json`), métricas, patrones.
- `DATOS/censo_frentes_ribera.csv` — 42 frentes × rasgos (abrir en Excel/QGIS; unir por `ref_catastral`).
- `FIGURAS/` — mapas y gráficos del documento, alzados rectificados por frente, alzados continuos, serie histórica.
- `SCRIPTS/` — todo el cálculo (Python). Se ejecutaron en el entorno de Claude: ajustar rutas (`/mnt/user-data/...`, `/home/claude/...`) a esta carpeta antes de relanzar.

## Niveles
A medido · B inferido (modelo o lectura visual) · C hipótesis.
