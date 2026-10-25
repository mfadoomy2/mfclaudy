Leyenda de colores / qué proyecto estás viendo

Los dos proyectos guardados tienen simbologías distintas. La columna I corresponde al inventario inicial por temas; la columna E, al proyecto etiquetado por categoría principal.


# Leyenda de colores / qué proyecto estás viendo

<b>I:</b> INVENTARIO_FISICO_600M.qgz. <b>E:</b> QGIS_ETIQUETADO/INVENTARIO_ETIQUETADO.qgz. La leyenda coloreada es funcional; el resto del documento utiliza texto negro sobre blanco.

Código y categoría

EMP  Emplazamiento

PAT  Patrimonio y cultura

TRA  Transporte

COM  Comercio y actividad

MOB  Mobiliario y servicios de calle

ACC  Accesibilidad y elementos de calle

UMB  Accesos y umbrales

BAR  Barreras

INF  Infraestructura

EQU  Equipamientos y locales

EDI  Edificios

VER  Espacio público y verde

VIA  Calles y recorridos

DIR  Portales y direcciones

OTR  Otros elementos físicos

Si todos los puntos aparecen rojos

En el grupo 00_INVENTARIO_COMPLETO, el rojo #dc2b1f significa «todos los puntos», no «todos son comercios». Las líneas son #555555 y las áreas, #d8d8d8 con borde #777777. Los grupos temáticos iniciales están desactivados al crearlos; un mismo objeto puede figurar en varios si se activan.

En el proyecto etiquetado

El color representa cat_codigo y no el nombre individual. Cada objeto tiene una categoría principal según la prioridad del script. El resto de sus temas se conserva en el campo temas. Los polígonos usan opacidad del 35 %, por lo que se ven más claros sobre blanco. Los códigos permiten distinguir categorías con colores parecidos.

Qué identifica cada símbolo y cada código


# Qué identifica cada símbolo y cada código

<b>P</b> = punto; <b>L</b> = línea; <b>A</b> = área o polígono. El prefijo de id_mapa indica geometría, no categoría. Por ejemplo, P02511 es «La Latina», categoría TRA. El ID cartográfico no es el ID de OpenStreetMap.

<b>etiqueta:</b> ID + nombre. <b>nombre_mapa:</b> nombre o descripción disponible. <b>cat_codigo:</b> código de categoría. <b>subtipo:</b> etiqueta OSM de referencia. <b>osm_tipo + osm_id:</b> identidad en la fuente. Los números siguientes son registros del archivo local, no un censo de personas o actividades.

Categoría

EMP  Emplazamiento

PAT  Patrimonio y cultura

TRA  Transporte

COM  Comercio y actividad

MOB  Mobiliario y servicios de calle

ACC  Accesibilidad y elementos de calle

UMB  Accesos y umbrales

BAR  Barreras

INF  Infraestructura

EQU  Equipamientos y locales

EDI  Edificios

VER  Espacio público y verde

VIA  Calles y recorridos

DIR  Portales y direcciones

OTR  Otros elementos físicos

<b>Total:</b> 5.052 puntos. 1.438 líneas y 1.531 polígonos; 8.021 registros.

Precauciones al leer los nombres de categoría

<b>UMB</b> incluye objetos con entrada, puerta o información wheelchair: no todos son portales. <b>ACC</b> agrupa pasos, escaleras, ascensores, semáforos y farolas: no expresa un nivel de accesibilidad. <b>PAT</b> procede de historic o tourism: no equivale a protección patrimonial. <b>VER</b> incluye leisure, natural y landuse: no garantiza vegetación ni acceso público.

COM agrupa shop, craft y office; MOB incluye bancos, papeleras, fuentes, aparcabicis, reciclaje y aseos; EQU recoge otros amenity; INF incluye man_made, emergency y power. EDI se asigna por building. Para saber qué es un objeto concreto, consultar etiqueta, temas y tags_json. El subtipo único puede no recoger todas sus funciones.

Mostrar el nombre de cada punto en QGIS


# Mostrar el nombre de cada punto en QGIS

1. Abrir el proyecto que ya contiene las etiquetas

Guarda primero cualquier cambio de tu proyecto abierto. Después usa <b>Proyecto &gt; Abrir</b> y selecciona <b>INVENTARIO_ETIQUETADO.qgz</b> dentro de INVESTIGACIÓN / QGIS_ETIQUETADO. No necesitas descargar ni volver a ejecutar el inventario completo.

El script principal genera el proyecto etiquetado como archivo independiente, pero no lo abre en la ventana activa. Seguir en INVENTARIO_FISICO_600M.qgz explica que aparezcan los colores iniciales y falten los campos añadidos.

2. Activar o comprobar las etiquetas

En la capa <b>P · Puntos físicos</b>: botón derecho &gt; <b>Propiedades &gt; Etiquetas &gt; Etiquetas sencillas</b>. En el valor o campo de etiqueta elige <b>etiqueta</b> y pulsa Aplicar. Ese campo muestra el ID y el nombre. Para ver solo el número corto, usa <b>id_mapa</b>; para ver solo el nombre, <b>nombre_mapa</b>.

Las tres capas guardadas ya tienen activado el campo etiqueta. Repite la comprobación en L · Líneas físicas y A · Polígonos físicos solo si deseas mostrar sus nombres también. Si el selector no contiene estos campos, estás en una capa del inventario original, no en la etiquetada.

3. Leer todos los objetos sin amontonar texto

Acércate hasta una manzana o un tramo de calle. QGIS oculta etiquetas que chocan entre sí: que falte un texto en pantalla no significa que falte el punto. Para centrarte en puntos, desactiva temporalmente las etiquetas de líneas y polígonos, no sus datos.

Si necesitas una categoría, usa el filtro de la capa con <b>"cat_codigo" = 'COM'</b> para comercio, por ejemplo. Al terminar, elimina el filtro para recuperar todo. Para saber qué es un punto oculto por otros, usa <b>Identificar objetos espaciales</b> o la tabla de atributos y consulta etiqueta. Una leyenda explica los colores; las etiquetas identifican cada objeto.

4. Recuperar el estilo si has cargado el GPKG directamente

En Propiedades de la capa, abre <b>Estilo &gt; Cargar estilo</b> y elige el QML correspondiente dentro de QGIS_ETIQUETADO: puntos_fisicos.qml, lineas_fisicas.qml o poligonos_fisicos.qml. Carga cada estilo en su propia capa. Así recuperas colores y configuración de etiquetas.

Referencia de interfaz: <link href="https://docs.qgis.org/3.40/en/docs/user_manual/working_with_vector/vector_properties.html">Manual QGIS: propiedades de capas vectoriales y etiquetado</link>. Los nombres exactos de algunos controles pueden variar con la versión y el idioma.

Poner la leyenda en un plano y conservar nombres


# Poner la leyenda en un plano y conservar nombres

Leyenda automática dentro de QGIS

En un diseño de impresión, añade primero un mapa y después <b>Añadir leyenda</b>. Selecciona la leyenda y vincúlala a ese mapa. En «Elementos de leyenda», desactiva la actualización automática si quieres retirar entradas innecesarias. Mantén las capas P, L y A que realmente estés representando; sus categorías aparecerán con código, nombre y símbolo.

Si filtras la leyenda por el contenido del mapa, mostrará solo las categorías presentes en esa vista. Para una clave general de todo el inventario, deja ese filtro desactivado. La leyenda automática responde a la simbología real de las capas; conviene usarla si vas a cambiar colores.

Leyenda preparada para insertar

Junto a esta guía se entregan <b>LEYENDA_ETIQUETADO.svg</b> y <b>LEYENDA_INVENTARIO_INICIAL.svg</b>. En el diseño: <b>Añadir imagen</b>, dibuja un rectángulo, selecciona imagen SVG y busca el archivo adecuado. Mantén las proporciones; una anchura de unos 110-140 mm permite leer sus categorías.

Estos SVG son claves vectoriales fijas: no cargan datos ni etiquetan puntos y no se actualizan al cambiar la simbología. El SVG inicial incluye además la clave de «todos los puntos/líneas/áreas». Usa la versión que corresponda al proyecto abierto.

Nombres en DXF

El archivo existente <b>QGIS_ETIQUETADO/INVENTARIO_CON_NOMBRES.dxf</b> fue generado por el script con un texto por objeto. Las capas <b>G_P_*, G_L_*, G_A_*</b> contienen geometría; <b>T_P_*, T_L_*, T_A_*</b> contienen ID y nombre como TEXT. LEYENDA aparece a la derecha del dibujo. El sistema es EPSG:25830 y las unidades son metros.

En CAD, activa las capas T_* para ver los nombres. Que muchos textos se solapen no significa que se hayan perdido: necesitan organización por escala o categoría. Cambiar una etiqueta en QGIS no actualiza automáticamente ese DXF ya guardado. La leyenda SVG insertada en un diseño de impresión tampoco se incorpora por sí sola al DXF.

Archivos y comprobación

Esta guía se obtiene de los dos scripts guardados, los estilos QML, el proyecto etiquetado y las tablas del GPKG existente. No se han modificado el catálogo, el inventario ni el proyecto QGIS. Los nombres y las categorías conservan la información del archivo local, sin nueva comprobación de campo.

<link href="https://docs.qgis.org/3.40/en/docs/user_manual/print_layout/layout_items/layout_legend.html">Manual QGIS: leyenda del diseño</link><br/><link href="https://docs.qgis.org/3.40/en/docs/user_manual/print_layout/layout_items/layout_image.html">Manual QGIS: imágenes y SVG en el diseño</link>
