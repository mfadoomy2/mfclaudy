# Instrucciones para Claude Code

Proyecto de arquitectura G3 (UEM): viviendas temporales para 40 jóvenes en Ribera de Curtidores 31, El Rastro, Madrid. Autor: Adam.

## Cómo orientarte

- Lee primero `README.md`, después `G3_HISTORIA_COMPLETA_DEL_PROYECTO.md` y `G3-CLAUDE/00_LEEME_G3_CLAUDE.md`.
- El trabajo está separado por la IA que lo hizo: `G3-CLAUDE/`, `G3-CODEX/`, `G3-FASE1-INVESTIGACION/`, `G3-SIN-ATRIBUIR/`. Las mismas carpetas de fase aparecen en `G3-CLAUDE` y `G3-CODEX`; mira las dos para tener la fase completa.
- Los archivos `*.parteNNNdeMMM` son trozos: ejecuta `python3 <carpeta>/_GITHUB/unir_trozos.py` antes de abrir esos modelos.
- Los `*.FICHA.md` describen modelos que no están en GitHub porque pesan más de 100 MiB. No inventes su contenido: usa la ficha y los archivos que cita.
- Los `.3dm` se leen con la librería Python `rhino3dm` (`pip install rhino3dm`).
- Las rutas absolutas `/Volumes/T7/...` que aparecen en documentos y scripts son del disco del autor. Tradúcelas con `<carpeta>/_GITHUB/MAPA_RUTAS.tsv`.
- Los nombres «FINAL», «CORREGIDA» o «CALCULADA» pertenecen a su versión; no significan que esa solución esté aprobada.

## Criterios del proyecto

- Todo lo que se proponga debe cumplir el Código Técnico de la Edificación y justificarse con criterio técnico y fuentes.
- Distinguir siempre dato medido, lectura e hipótesis; nunca inventar datos.
- Paneles y documentos: fondo blanco, colores vivos, títulos discretos, sin eslóganes ni encabezados tipo etiqueta, sin figuras humanas dibujadas. Planos técnicos en blanco y negro, al estilo de los P01–P06.
- Cuando se trabaje sobre un Rhino concreto, seguir en ese mismo archivo en vez de crear otro.
