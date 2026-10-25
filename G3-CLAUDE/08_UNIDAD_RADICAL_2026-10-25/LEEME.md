# 08 · Unidad radical (25 de octubre de 2026)

Carpeta de trabajo de Claude Code a partir de la corrección de Adam: la unidad sale de cómo vive la juventud hoy, contado en 150 escenas, y de lo que esas escenas tienen en común. Aquí están las escenas, su análisis, seis unidades modeladas en 3D con sus estados y escenas dentro, dieciséis cuerpos, cinco uniones de 40 en la parcela real y diez diagramas de lo previo a la arquitectura.

## Por dónde empezar

1. `00_LO_QUE_NO_SE_REPITE.md` — errores de todo el proceso, lo que ya existe y las reglas vigentes. Se relee antes de cada trabajo.
2. `01_150_ESCENAS.md` — las 150 escenas, el conteo y la lectura de lo común; `escenas.csv` es el dato.
3. `G3_UNIDAD_RADICAL_MODELOS_Y_DIAGRAMAS_A3.pdf` — todo junto, en A3 apaisado.
4. `modelos/UNIDADES_H1_H6.3dm` y `modelos/UNIONES_U1_U5.3dm` — Rhino 8, metros. Mallas de estudio con capas por unidad, estado (membrana abierta / media / cerrada / verano / dividida) y escena; vistas guardadas. No son sólidos constructivos.

## Qué hay

| Carpeta / archivo | Contenido |
|---|---|
| `vistas/unidades/` | Axonometrías de H1–H6: abierta, cerrada, media, verano, cortada a +1,60; escenas de capacidad E042/E058/E096 en todas; diez escenas habitadas en H3; vista de conjunto |
| `vistas/uniones/` | U1–U5 con los vecinos del Catastro, solas y desde Ribera de Curtidores |
| `planos/` | Planta y dos secciones 1:25 de cada unidad; planta y sección 1:250 de cada unión. Blanco y negro, corte negro, proyección fina |
| `diagramas/` | D01–D10 en PNG y SVG editable |
| `verificacion/` | `UNIDADES.json`, `UNIONES.json`, `CUERPOS_X_UNIDADES.json` y `.md` |
| `fuentes/` | Todo el código: `geom3d.py` (primitivas), `cuerpos.py` (catálogo), `unidades.py` (H1–H6), `escenas3d.py`, `uniones.py` (U1–U5 y parcela), `render.py`, `rhino_out.py`, `matriz_cuerpos.py`, `diagramas.py`, `generar_unidades.py`, `montar_pdf.py`, `contar_escenas.py`; `celula.py` / `piezas.py` / `geo.py` son las pruebas anteriores de la célula de 14,5 m² (descartadas por el mínimo de 15 m²) |

Para regenerar todo: `python3 fuentes/generar_unidades.py && python3 fuentes/matriz_cuerpos.py && python3 fuentes/uniones.py && python3 fuentes/diagramas.py && python3 fuentes/montar_pdf.py` (necesita trimesh, manifold3d, networkx, shapely, scipy, matplotlib, rhino3dm, reportlab).

## Las seis unidades

Todas con 15 m² de superficie privada (3,45 × 4,35), el mínimo de la unidad privativa de coliving según las NN.UU. de Madrid 2023 citadas en `G3_unidad_v3_memoria.md` (contrastar con el texto oficial).

| | Qué es | Qué pone a prueba |
|---|---|---|
| H1 · La cama con canto | Habitación 3 × 5 con suelo duro; plataforma-cama 2,4 × 2,4 con canto duro, repisa de cabecera, dosel textil, cajones, armario-maleta, banco y óculo | La unidad-cama dentro de una habitación convencional |
| H2 · El casco | Cápsula de doble piel (0,25) con todo el suelo blando, canto-repisa perimetral, esclusa acústica, ventana con contraventana y óculo | Lo único insonorizado del edificio |
| H3 · La superficie silenciosa | Plinto + superficie blanda + canto bajo (asiento, 0,45) + canto alto (mesa, 0,72) + aro con membrana graduable + hueco al cielo + armario-maleta | Superstudio a 15 m²: sin muebles, sin habitación |
| H4 · El turno | H3 con dos entradas, dos armarios, membrana divisible, dos huecos al cielo y repisa de relevo | Una superficie para dos personas a horas distintas |
| H5 · La mochila y el dock | 15 m² marcados, bastidor, enchufe, armario-maleta y colchón; la tienda la trae cada una | Sol literal: el edificio solo da soporte |
| H6 · La topografía | Relieve blando con concha cálida, lomo-respaldo fresco, meseta dura para el portátil y cúpula textil con óculo | La superficie que no es plana y se adapta al cuerpo |

Resultado de la matriz de cuerpos (de 160): H3 156 · H4 156 · H2 154 · H6 129 · H1 100 · H5 87.

## Las cinco uniones

| | Unidades | Con cielo en vertical | Niveles |
|---|---|---|---|
| U1 · El campo | 40 | 12 | 3 bandejas completas a +22,6 / +28,8 / +35,0 |
| U2 · Las terrazas | 33 | 26 | 10 terrazas de +16,4 a +25,7 y una bandeja alta |
| U3 · Los racimos de comisión | 40 | 10 | 8 racimos alternando oeste y este, de +16,4 a +38,1 |
| U4 · La torre de turnos | 20 superficies (40 personas) | 4 | 5 niveles sobre el frente |
| U5 · La plaza-acampada | 40 docks | 2 | 3 plazas a +22,6 / +28,8 / +35,0 |

El dato duro: en una bandeja de la parcela (650,9 m², 15 m de ancho) caben 14 superficies H3 con canto y paso o 19 docks H5. Cuarenta superficies con cielo propio no caben en una parcela de 15 m de ancho sin escalonarlas: U2 es la que más cielo da, y no llega a 40.

## Lo que no está demostrado

Aislamiento acústico de la membrana y del casco (DB-HR), estructura (troncos y bandejas sin calcular), instalaciones, evacuación, accesibilidad completa y la normativa de coliving. Las medidas de los cuerpos son hipótesis; las 53 escenas marcadas como hipótesis no están en la investigación del repositorio.
