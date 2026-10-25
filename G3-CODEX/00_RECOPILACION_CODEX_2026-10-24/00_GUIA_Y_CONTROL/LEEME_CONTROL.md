# Control de recopilación

- `VERIFICACION_RECOPILACION.json`: recuentos, tamaño, fuentes no localizadas y errores.
- `INVENTARIO_ARCHIVOS_SHA256.json`: origen real, ruta original, destino, bytes y SHA-256 de cada archivo.
- `INVENTARIO_INICIAL.json`: situación al comenzar, antes del movimiento concurrente de carpetas.
- `MAPA_CARPETAS.json`: nombre original → categoría nueva.
- `REGISTRO_REUBICACION_PREEXISTENTE.json`: registro encontrado del traslado de material a G3 CLAUDE; este archivo explica el cambio de rutas y no atribuye el traslado a G3 CODEX.
- `DUPLICADOS_IDENTICOS_CONSERVADOS.json`: coincidencias por contenido, sin borrar ninguna copia.
- `FUENTES_NO_LOCALIZADAS.json`: adjuntos externos ausentes en sus rutas conocidas.
- `EXCLUSIONES_METADATA_APPLE.json`: `.DS_Store` y `._*`; metadatos de Finder, no contenido de proyecto.
- `COMPROBACION_FINAL.json`: integridad de índices, cobertura del inventario inicial y vínculos.

## Restaurar nombres originales

Para reconstruir una copia separada con las carpetas en su estructura anterior:

```sh
python3 restaurar_estructura_original.py --destination "/ruta/nueva/G3_reconstruido"
```

La carpeta elegida no puede existir. `--include-external` añade los originales externos en `__FUENTES_EXTERNAS__`. Se copia y verifica el contenido; no se restablecen rutas absolutas de otros discos, aplicaciones, fuentes de sistema o dependencias de Python.

El script `recopilar.py` documenta la operación realizada en este Mac; no debe ejecutarse rutinariamente para consultar el archivo. Los scripts históricos de proyecto pueden contener escrituras a rutas antiguas.
