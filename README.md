# G3 · Ribera de Curtidores 31

Viviendas temporales para 40 jóvenes en Ribera de Curtidores 31, El Rastro (Madrid). G3 Proyectos, Universidad Europea de Madrid, curso 2026-27. Autor: Adam.

Este repo reúne todo el trabajo del proyecto hecho con IA, una sola copia de cada archivo, separado por la IA que lo hizo.

## Carpetas

| Carpeta | Qué es |
|---|---|
| [`G3-CLAUDE/`](G3-CLAUDE/) | Lo hecho con Claude: unidad suspendida, Engel, organización en parcela, 8 agrupaciones, megaestructura en Ribera 31 y diagnóstico de luz, lectura de las 40 plantas y N19B reducida, cuaderno de 30 páginas, E02 recta, entrega de planos 1:100 y secciones, planos 1:200 de la megaestructura. |
| [`G3-CODEX/`](G3-CODEX/) | Lo hecho con ChatGPT/Codex: imaginarios, mecanismos, Sol-selva, V2–V4, P02, tejidos, 40 y 80 plantas, formas de vivir, unidades de 4, base de los planos técnicos, memoria integral del 20-10 y recopilación del 24-10. |
| [`G3-FASE1-INVESTIGACION/`](G3-FASE1-INVESTIGACION/) | Fase 1: investigación de la parcela y el barrio (compendio, QGIS, megapanel 5×A3, panel A1, referencias) y mapas propios. |
| [`G3-SIN-ATRIBUIR/`](G3-SIN-ATRIBUIR/) | Vistas previas temporales sin autor documentado. |

Las carpetas de fase (`01_E2…` a `07_UNIDADES…`) se repiten dentro de `G3-CLAUDE` y `G3-CODEX`: cada una contiene solo lo que hizo esa IA en esa fase.

## Por dónde empezar

1. [`G3_HISTORIA_COMPLETA_DEL_PROYECTO.md`](G3_HISTORIA_COMPLETA_DEL_PROYECTO.md): la historia del proyecto, lo pensado, probado y corregido.
2. [`G3-CLAUDE/00_LEEME_G3_CLAUDE.md`](G3-CLAUDE/00_LEEME_G3_CLAUDE.md): índice y cronología completa, decisiones vigentes, descartes y pendientes.
3. [`G3-CODEX/00_MEMORIA_INTEGRAL_DEL_PROCESO_2026-10-20.md`](G3-CODEX/00_MEMORIA_INTEGRAL_DEL_PROCESO_2026-10-20.md): relato largo del proceso y guía de los modelos Rhino.

## Archivos grandes

- Los archivos de 25 a 100 MiB están partidos en trozos `*.parteNNNdeMMM`. Para reconstruirlos:
  ```sh
  for d in G3-CLAUDE G3-CODEX G3-FASE1-INVESTIGACION G3-SIN-ATRIBUIR; do python3 $d/_GITHUB/unir_trozos.py; done
  ```
- Los de más de 100 MiB (catálogos Rhino de las 40, modelo del radio de 600 m, renders, zips de entrega) no caben en GitHub. Se quedan en el disco del autor (`G3 Proyectos/G3 IA/NO_SUBIR/` en el T7) y aquí cada uno tiene una ficha `*.FICHA.md` en su sitio, con su tamaño, su SHA-256, sus capas, objetos, medidas y vistas guardadas.

## Control

En cada carpeta, `_GITHUB/` tiene:
- `INVENTARIO.tsv`: cada archivo, su tamaño, su SHA-256 y por qué se atribuye a esa IA.
- `MAPA_RUTAS.tsv`: ruta antigua en el disco (`/Volumes/T7/…`) → ruta en este repo.
- `DUPLICADOS.tsv`: copias idénticas que no se han subido y cuál se conserva.
- `NO_SUBIDOS.tsv`: lo que se queda solo en el disco y por qué.

[`G3_IA_ORGANIZACION_EN_EL_DISCO.md`](G3_IA_ORGANIZACION_EN_EL_DISCO.md) explica cómo está guardado todo en el disco del autor.
