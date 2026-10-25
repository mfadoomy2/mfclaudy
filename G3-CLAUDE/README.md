# G3 · trabajo hecho con Claude

Viviendas temporales para jóvenes en Ribera de Curtidores 31, El Rastro (Madrid). G3 Proyectos, UEM, 2026-27.

Esta carpeta es una de las partes del repo (archivo **G3 IA**):

- `G3-CLAUDE/` ← esta carpeta
- `G3-CODEX/`
- `G3-FASE1-INVESTIGACION/`
- `G3-SIN-ATRIBUIR/`

## Qué hay

- 162 archivos subidos tal cual y 2 archivos grandes partidos en trozos de 24 MiB.
- 1 archivos demasiado pesados para GitHub: cada uno tiene aquí una ficha `*.FICHA.md` en su sitio.

| Carpeta | Archivos |
|---|---|
| `00_LEEME_G3_CLAUDE.md` | 1 |
| `02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct` | 25 |
| `03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct` | 80 |
| `05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct` | 9 |
| `06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct` | 2 |
| `07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct` | 46 |
| `_registro_movimientos_2026-10-24.json` | 1 |

## Por dónde empezar

- `00_LEEME_G3_CLAUDE.md`: índice y cronología completa del proyecto.
- La memoria larga del proceso (escrita con ChatGPT/Codex) está en el repo `G3-CODEX/`: `00_MEMORIA_INTEGRAL_DEL_PROCESO_2026-10-20.md`.

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
