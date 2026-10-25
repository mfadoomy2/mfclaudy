# G3 · Documentación, luz y planta baja · 16.10.2026

Empieza por output/pdf/DOSSIER_G3_JUSTIFICACION_LUZ_Y_PLANTA_BAJA.pdf: 18 páginas A3 horizontal. Incluye el guion de defensa en página 17 y fuentes en página 18.

## Modelos
- modelos/SELVA_V5_LUZ_Y_PLANTA_BAJA.3dm: conjunto con contexto, propuesta de luz y planta baja. Nuevo archivo; conserva los anteriores.
- modelos/UNIDAD_V5_NORTE_EDITABLE.3dm: unidad aislada.
- modelos/UNIDAD_V5_INTERIOR.3dm: misma unidad con cubierta y vidrio ocultos para inspección.
- modelos/PLANTA_BAJA_V5_EDITABLE.3dm: extracción de las piezas programáticas.
Metros. Relectura independiente: 11.097 objetos válidos en el conjunto; 240 en cada unidad; 703 en planta baja. Ver verificacion/modelos.json.

## Documentación y estudio previo
fuentes/originales contiene el compendio del lugar (43 páginas), el cuaderno Sol–Selva (15 páginas), enunciado, memoria V4, registro de fuentes y textos primarios archivados. No se ha reescrito el pasado como si la V5 ya estuviera justificada antes.
DOSSIER_EDITABLE.md y fuentes/crear_dossier.py permiten editar el nuevo documento.

## Cálculo de luz
calculo/COMPARACION_40_HABITACIONES.csv y los JSON conservan los resultados por habitación. Los porcentajes son apertura geométrica de cielo en el exterior del hueco; no son lux ni cumplimiento. Ver métodos en fuentes/analizar*.py. El JSON de render es la malla del modelo nuevo; el análisis V4 requiere su caché original en la carpeta V4 referenciada por el script. No mover rutas sin adaptarlas.
V4: mediana 15,86%, 14 posiciones por debajo del 5%. V5: mediana 58,93%, una por debajo del 5% (P01-H3). El 5% sólo prioriza revisión. La distribución y los puntos cambian entre versiones.

## Límites que condicionan la siguiente decisión
No hay simulación interior anual ni transmitancias medidas. P01-H3 y plantas bajas son prioritarias; si no funcionan, reducir ocupación o retirar/desplazar piezas. No se ha recalculado estructura V5: resultados estructurales heredados son de V4. Habitabilidad, normativa urbanística, evacuación, accesibilidad, topografía, nave existente, cimentación e instalaciones pendientes. El modelo de suelo es plano, aunque el estudio previo advierte posible desnivel. Los seis puestos abajo son de apoyo/lectura breve; no se justifica jornada completa con luz natural. No es proyecto de ejecución.

## Imágenes y verificación
Los renders muestran geometría del modelo, no imágenes generadas. Transparencias gráficas, no ópticas certificadas. verificacion incluye registros, revisión geométrica y páginas renderizadas. El paquete excluye archivos AppleDouble y duplicados de la revisión de páginas para reducir peso.
