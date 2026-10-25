# G3 IA

Todo el trabajo de G3 hecho con IA, una sola copia de cada archivo, separado por la IA que lo hizo y preparado para GitHub.

Preparado el 2026-10-25.

## Repos

| Carpeta | Qué es | Tandas | Archivos | GB |
|---|---|---|---|---|
| `REPO_G3-CLAUDE` | Lo hecho con Claude | 2 | 164 | 0.39 |
| `REPO_G3-CODEX` | Lo hecho con ChatGPT/Codex, más su recopilación del 24-10 | 29 | 2776 | 2.54 |
| `REPO_G3-FASE1-INVESTIGACION` | Fase 1: INVESTIGACIÓN y MAPPEADOS (grupo, con Codex y Claude) | 30 | 2911 | 2.99 |
| `REPO_G3-SIN-ATRIBUIR` | Sin autor documentado (vistas previas temporales); no hace falta subirlo | 1 | 36 | 0.01 |

## Cómo subir

Cada repo tiene su `COMO_SUBIR.md`. En resumen: crea el repo en GitHub, **Add file → Upload files**, arrastra el contenido de `TANDA_001`, confirma, y sigue con la `TANDA_002`, etc.

Límites que se respetan: 100 archivos por subida y 25 MiB por archivo en el navegador; GitHub bloquea cualquier archivo de más de 100 MiB; recomienda repos de menos de 1–5 GB.

## NO_SUBIR (se queda solo en el T7)

- `PESADOS/`: 33 archivos (10.2 GB) de más de 100 MiB, o zips de carpetas que ya están subidas. Cada uno tiene una ficha `.FICHA.md` en su repo.
- `ORIGINALES_TROCEADOS/`: los originales enteros de los archivos que se suben partidos en trozos de 24 MiB.
- `DUPLICADOS_INTERNOS/`: 1178 copias idénticas (1.8 GB). En cada repo, `_GITHUB/DUPLICADOS.tsv` dice cuál se conserva.
- `REGENERABLES/`: 603 archivos (1.0 GB): `.npy`, `.pyc`, `__pycache__`, copias `.blend1`.
- `DUPLICADOS_G3_CODEX…/`: la copia que hizo Codex el 24-10 (18.4 GB). Cada archivo de esta copia tiene su original, idéntico, en G3 IA (en un repo o en NO_SUBIR); lo único propio de Codex se ha llevado a `REPO_G3-CODEX/…/00_RECOPILACION_CODEX_2026-10-24/`. **Se puede borrar.**
- `_ESTRUCTURA_ANTIGUA_…`: las carpetas antiguas, ya vacías. Se pueden borrar.

## Trabajar en local después de subir

Las tandas reparten los archivos para poder subirlos. Para volver a tener cada repo como un árbol normal (QGIS y Rhino necesitan sus rutas relativas):

```sh
python3 JUNTAR_TANDAS.py REPO_G3-CODEX --unir
```

También puedes clonar el repo de GitHub y ejecutar `python3 _GITHUB/unir_trozos.py`.

## Deshacer

Para devolver todo a como estaba antes (G3 CLAUDE, G3 CODEX, INVESTIGACIÓN y MAPPEADOS):

```sh
python3 "../_PREPARAR_G3_IA/g3ia.py" "/Volumes/T7/G3 Proyectos" deshacer
```

El registro de cada movimiento está en `_trabajo/movimientos.json`.

## Cómo se ha decidido qué hizo cada IA

- Por el historial de las conversaciones con Claude y las notas del proyecto, carpeta a carpeta (la lista está en `g3ia.py`, en `REGLAS`).
- El 20-10, Codex/ChatGPT trabajó hasta las 02:22 (compactación y giro de 90°) y Claude retomó a las 02:56 (E02 recta, entrega 1:100, secciones, planos de la megaestructura). Lo que se creó o modificó a partir de esa hora se atribuye a Claude.
- Cada archivo lleva su motivo en `_GITHUB/INVENTARIO.tsv` de su repo.
