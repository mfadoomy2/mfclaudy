# G3 · Fase 1, investigación de la parcela y el barrio

Viviendas temporales para jóvenes en Ribera de Curtidores 31, El Rastro (Madrid). G3 Proyectos, UEM, 2026-27.

Esta carpeta es una de las partes del repo (archivo **G3 IA**):

- `G3-CLAUDE/`
- `G3-CODEX/`
- `G3-FASE1-INVESTIGACION/` ← esta carpeta
- `G3-SIN-ATRIBUIR/`

## Qué hay

- 2898 archivos subidos tal cual y 13 archivos grandes partidos en trozos de 24 MiB.
- 6 archivos demasiado pesados para GitHub: cada uno tiene aquí una ficha `*.FICHA.md` en su sitio.

| Carpeta | Archivos |
|---|---|
| `INVESTIGACIÓN` | 2903 |
| `MAPPEADOS` | 8 |

## Por dónde empezar

- `INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/`: compendio de 43 páginas, datos y figuras.
- `INVESTIGACIÓN/PANEL_FINAL_5xA3/` y `INVESTIGACIÓN/PANEL A1/`: paneles del grupo.

## Archivos partidos

Para reconstruir los archivos grandes después de clonar:

```sh
python3 _GITHUB/unir_trozos.py
```

## Control

- `_GITHUB/INVENTARIO.tsv`: cada archivo, su tamaño, su SHA-256 y por qué se atribuye a esta IA.
- `_GITHUB/MAPA_RUTAS.tsv`: ruta antigua en el disco T7 → ruta en este repo.
- `_GITHUB/DUPLICADOS.tsv`: copias idénticas quitadas y cuál se conserva.
- `_GITHUB/NO_SUBIDOS.tsv`: lo que se queda solo en el disco y por qué.

Preparado el 2026-10-25.
