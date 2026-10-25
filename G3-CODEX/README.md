# G3 · trabajo hecho con ChatGPT/Codex

Viviendas temporales para jóvenes en Ribera de Curtidores 31, El Rastro (Madrid). G3 Proyectos, UEM, 2026-27.

Esta carpeta es una de las partes del repo (archivo **G3 IA**):

- `G3-CLAUDE/`
- `G3-CODEX/` ← esta carpeta
- `G3-FASE1-INVESTIGACION/`
- `G3-SIN-ATRIBUIR/`

## Qué hay

- 2770 archivos subidos tal cual y 6 archivos grandes partidos en trozos de 24 MiB.
- 26 archivos demasiado pesados para GitHub: cada uno tiene aquí una ficha `*.FICHA.md` en su sitio.

| Carpeta | Archivos |
|---|---|
| `00_MEMORIA_INTEGRAL_DEL_PROCESO_2026-10-20.md` | 1 |
| `00_RECOPILACION_CODEX_2026-10-24` | 32 |
| `01_E2_IMAGINARIOS_PERSONAS_Y_MECANISMOS_05-06oct` | 81 |
| `02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct` | 56 |
| `03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct` | 226 |
| `04_P02_LA_HABITACION_16-18oct` | 95 |
| `05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct` | 1720 |
| `06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct` | 440 |
| `07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct` | 124 |
| `98_COPIAS_DUPLICADAS` | 1 |

## Por dónde empezar

- `00_MEMORIA_INTEGRAL_DEL_PROCESO_2026-10-20.md`: relato completo, decisiones y guía de los Rhino.
- `00_RECOPILACION_CODEX_2026-10-24/TODO_EL_PROCESO_G3.md`: resumen de Codex del 24-10.
- Ojo: las rutas de esos documentos son las antiguas del disco; `_GITHUB/MAPA_RUTAS.tsv` dice dónde está ahora cada archivo.

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
