# Unidad aislada P02 — inspección cercana

16 octubre 2026.

## Abrir

- `modelos/UNIDAD_P02_DETALLADA.3dm`: archivo principal editable, superficies y sólidos Brep/NURBS, centrado en el origen y en metros. Se conserva la escala 1:1 del conjunto. Vista cercana guardada y cotas en la capa oculta `80_COTAS_UNIDAD`.
- `modelos/UNIDAD_P02_INTERIOR_EDITABLE.3dm`: la misma unidad, ocultando cubierta, vela, costillas, vidrio y cables exteriores para inspeccionar la distribución. No se han borrado esos componentes.
- `modelos/UNIDAD_P02_PREVIA_SOLIDA.3dm`: mallas generadas desde los sólidos por RhinoCommon; copia de visualización, no sustituye al editable.
- `modelos/D02_ENVOLVENTE_Y_BANDEJA_1a1.3dm`: detalle separado de la estratificación propuesta. No supone que todo ese desarrollo esté ya resuelto en cada encuentro de la unidad.

## Qué contiene

Pabellón para cuatro personas con cuatro habitaciones, cocina y mesa compartidas, dos baños, mobiliario, carpinterías, luminarias y aparatos sanitarios. Se extraen también su bandeja, viguetas, celosía de borde, barandillas, terraza amueblada, vela, mástiles, tensores, bajantes y tres figuras procedentes de PERSONAS.3dm. No se incluye el árbol completo ni el ascensor del conjunto: se aísla el pabellón y su plataforma para examinarlos.

Huella nominal del recinto doméstico: 9,60 × 6,80 m; altura interior de la bóveda hasta unos 4,30 m; plataforma de ancho nominal 12,40 m, recortada por la parcela en el conjunto. Las dimensiones no se han escalado para producir una imagen más espectacular.

La extracción elimina la losa doméstica coincidente con la bandeja, que duplicaba el suelo, y las piezas de la planta superior que entraban en la primera selección. Se retiran hojas y fragmentos de enredadera que quedaban sin su soporte al aislar la unidad. Los originales del conjunto permanecen intactos.

## Vistas

1. Unidad completa.
2. Interior abierto, retirando visualmente la envolvente exterior.
3. Planta amueblada.
4. Detalle de terraza y borde estructural.
5. Captura del Rhino abierto; el sombreado se comprobó también en pantalla.

Las vistas de Blender proceden de un remallado nuevo de los Breps con RhinoCommon. No se usa una imagen generada por IA ni una interpretación formal alternativa. Se incluyen las fuentes, la geometría triangulada y los registros de comprobación.

## Precisión y alcance

La tolerancia del documento es 1 mm y el remallado de visualización usa una tolerancia de 2 mm. Son parámetros geométricos, no una acreditación de precisión de obra. El modelo conserva el nivel de anteproyecto: algunas pieles se representan con superficies sin espesor desarrollado y los encuentros completos, sellos, herrajes, acústica, habitabilidad y accesibilidad requieren desarrollo. No debe confundirse el detalle visual de tornillos y aparatos con un proyecto listo para fabricación.

Cada pieza puede seleccionarse y editarse sin depender de bloques externos. La comprobación IsValid de los archivos finales no detecta geometrías inválidas; no equivale a una auditoría exhaustiva de interferencias o de normativa.
