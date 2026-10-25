# G3 CODEX · Todo el proceso, archivos y decisiones

Recopilación: **24 de octubre de 2026**. Proyecto de Adam: vivienda colectiva para jóvenes en Ribera de Curtidores 31, El Rastro, Madrid. Carpeta de archivo: `/Volumes/T7/G3 Proyectos/G3 CODEX`.

Este documento explica el recorrido del proyecto y permite encontrar sus archivos: investigación, referencias, imaginarios, mecanismos, megaestructura, unidad y habitación, programa por acciones, tejidos, catálogos, correcciones, agrupaciones, parcela, luz, planta baja, modelos y documentación técnica. Incluye los ensayos rechazados porque explican el proceso. **Archivar un resultado no equivale a aprobar su diseño o sus cálculos.**

La recopilación conserva los archivos completos; no es solo un resumen ni una selección de imágenes. Los originales y sus paquetes quedan separados por etapas. No se deduplican ni se borran revisiones por el hecho de parecerse. El inventario y las huellas SHA-256 permiten comprobar cada copia. Los `.md`, scripts y datos históricos se conservan sin reescribir sus contenidos.

## Índice de lectura

1. [Estado al cerrar esta recopilación](#estado-al-cerrar-esta-recopilación).
2. [Mapa de carpetas](#mapa-de-carpetas).
3. [Qué hemos hecho y por qué](#qué-hemos-hecho-y-por-qué).
4. [Reglas que siguen vigentes](#reglas-que-siguen-vigentes).
5. [Programa y escalas de convivencia](#programa-y-escalas-de-convivencia).
6. [Últimas revisiones técnicas y giros](#últimas-revisiones-técnicas-y-giros).
7. [Cómo retomar el proyecto](#cómo-retomar-el-proyecto).
8. [Alcance, fuentes y control del archivo](#alcance-fuentes-y-control-del-archivo).
9. [Catálogo de todas las carpetas y paquetes](#catálogo-de-todas-las-carpetas-y-paquetes).
10. [Memoria de desarrollo conservada](#memoria-de-desarrollo-conservada).

## Estado al cerrar esta recopilación

El trabajo tiene una base extensa de investigación y numerosos ensayos. No hay una de las cuarenta plantas declarada ganadora definitiva por Adam. La familia más reciente de unidades de cuatro y los ensayos E01/E02/E03 continúan siendo anteproyecto. La capacidad objetivo de cuarenta residentes y el presupuesto provisional de unos 1.500 m² necesitan un cómputo completo que incluya servicios comunes, núcleos, estructura y circulaciones.

La última corrección explícita sobre orientación es: **girar las unidades dentro del complejo y mantener la parcela, planta baja, escalera, ascensor y conexiones generales; ajustar las uniones para reconectarlas como antes.** El ensayo en que se giró todo el complejo fue una interpretación equivocada y está rechazado. Se conserva como registro, no como alternativa vigente.

El usuario también ha cuestionado el tamaño de todas las unidades. Los intentos de compactación, sus JSON y sus plantas se archivan, pero el nombre `COMPACTADAS`, `CORREGIDA`, `FINAL` o `CALCULADA` no acredita que el problema esté resuelto. En particular, las verificaciones parciales de recorridos no sustituyen comprobar el cruce entre baños, dormitorios, estructura y mobiliario en el modelo correspondiente.

Hay una entrega nativa posterior denominada `E02_RECTA_HABITACIONES_A_LA_CALLE.3dm` y un juego de plantas/secciones en `ENTREGA_PLANOS_1_100`. Su LEEME describe una E02 recta con dos habitaciones hacia la calle. **Ese contenido no demuestra que todos los dormitorios tengan orientación a calle o que se haya cumplido íntegramente la última instrucción.** La recopilación comprueba la existencia e integridad de archivos; no ejecuta otra corrección arquitectónica ni sustituye una revisión del modelo.

### Archivos para empezar

- [Entrega reunida de planos, secciones y modelos](<06_PLANOS_TECNICOS_Y_RHINO/G3_PLANOS_TECNICOS_2026-10-20/ENTREGA_PLANOS_1_100>).
- [Plantas técnicas reunidas 1:100](<06_PLANOS_TECNICOS_Y_RHINO/G3_PLANOS_TECNICOS_2026-10-20/ENTREGA_PLANOS_1_100/G3_PLANOS_TECNICOS_1_100.pdf>).
- [Secciones técnicas reunidas](<06_PLANOS_TECNICOS_Y_RHINO/G3_PLANOS_TECNICOS_2026-10-20/ENTREGA_PLANOS_1_100/G3_SECCIONES_TECNICAS.pdf>).
- [Tres unidades aisladas V01 / V02 / V03](<06_PLANOS_TECNICOS_Y_RHINO/G3_PLANOS_TECNICOS_2026-10-20/ENTREGA_PLANOS_1_100/modelos/TRES_UNIDADES_COMPACTADAS_GIRO90.3dm>).
- [E02 recta: revisión posterior conservada](<06_PLANOS_TECNICOS_Y_RHINO/G3_PLANOS_TECNICOS_2026-10-20/ENTREGA_PLANOS_1_100/modelos/E02_RECTA_HABITACIONES_A_LA_CALLE.3dm>).
- [Documentación de la megaestructura a 1:200](<06_PLANOS_TECNICOS_Y_RHINO/MEGAESTRUCTURA_MACARRA_PLANOS_2026-10-20/G3_MEGAESTRUCTURA_MACARRA_PLANOS_1_200.pdf>).
- [Índice de modelos Rhino](<00_GUIA_Y_CONTROL/INDICE_MODELOS_RHINO.md>) y [documentos, dibujos y fuentes](<00_GUIA_Y_CONTROL/INDICE_DOCUMENTOS_Y_FUENTES.md>).

## Mapa de carpetas

| Carpeta | Contenido |
|---|---|
| `00_GUIA_Y_CONTROL` | Índices, procedencia, inventarios, verificación de copias, duplicados conservados y herramienta de restauración. |
| `01_INVESTIGACION_PARCELA_Y_REFERENCIAS` | Barrio, Catastro, QGIS, mapas, referentes, lectura de Ruralex/cocina y cuaderno de Sol. |
| `02_PRIMERAS_UNIDADES_COMPLEJO_Y_LUZ` | Células suspendidas, conjuntos, revisión inicial, V2/V3/V4, unidad aislada y documentación de luz/planta baja. |
| `03_HABITACION_Y_UNIDAD_P02` | Habitaciones, cama/mesa/vestidor/bow, plantas y secciones P02, modelos, apoyos, materiales y texturas. |
| `04_ACCIONES_TEJIDOS_Y_CATALOGOS` | Mapas de actividad, reglas, diagramas, cuarenta propuestas y variantes, traducción a plantas, modelos y correcciones. |
| `05_NUEVAS_UNIDADES_UNIONES_Y_PARCELA` | V01/V02/V03 diferenciadas, nuevas organizaciones, casas de cuatro y ocho, encuentros, continuidad, herencia macarra y encaje. |
| `06_PLANOS_TECNICOS_Y_RHINO` | Instantáneas nativas, extracciones medidas, planos/secciones, planta baja pública, revisiones, giros, documentación de megaestructura y scripts. |
| `07_IMAGINARIOS_MECANISMOS_Y_ORGANIZACION` | Exploraciones iniciales, mecanismos en parcela, personas y organización del conjunto. |
| `08_PAQUETES_ZIP_ORIGINALES` | ZIP históricos completos, aunque repitan materiales que existen sueltos. |
| `90_FUENTES_EXTERNAS_APORTADAS` | Referencia original de megaestructura, PERSONAS.3dm y texto inicial localizados fuera del proyecto. |
| `99_AUXILIARES_Y_DOCUMENTOS_HISTORICOS` | Memoria anterior íntegra, índice anterior, modelos de Engel, temporales y salidas auxiliares. |

Los nombres y estructuras interiores de cada entrega se conservan. Las carpetas terminadas en ` 2` se guardan como copias históricas diferenciadas; no se presupone que sean idénticas.

## Qué hemos hecho y por qué

### 1. Leer el lugar antes de imponer un edificio

Se reunió investigación de Ribera de Curtidores 31, la vida del Rastro, frentes, comercio, mercado dominical, patrones, materialidad y temporalidades. Se trabajó con cartografía catastral, GML/GeoJSON, bases QGIS, coordenadas y entorno. Se produjeron compendios, paneles, mapas y un megapanel de cinco A3. Se preservan también fotografías, capas y proyectos editables, no solo las láminas finales.

La investigación distingue dato observado/medido, inferencia e hipótesis. Las alturas deducidas de plantas catastrales no equivalen a un levantamiento. El frente a calle del polígono local usado en los ensayos mide aproximadamente **14,98 m**. Los **20,17 m** eran la extensión transversal máxima del contorno, y los **49,48 m** su extensión longitudinal en esos ejes; no deben etiquetarse como longitud de fachada. Estas cifras describen aquel contorno de trabajo y no una nueva medición topográfica.

### 2. Investigar la acampada como organización

Se buscaron referencias de cooperación, vivienda y juventud, con interés en Instagram/TikTok y fuentes del movimiento de vivienda. Adam señaló `@inquilinato_madrid`; aparece también `@acampada26s`. La intención era comprender cómo convivir, cocinar, mantener, compartir recursos y tener intimidad. No se elaboró una encuesta representativa de toda la generación Z. El personaje de proyecto y muchas acciones son hipótesis situadas.

La crítica arquitectónica debía aparecer en el reparto de recursos, la propiedad/gestión propuestas, la posibilidad de encuentro voluntario y el derecho a retirarse. Una lona o un aspecto precario no bastaban para trasladar la acampada a una vivienda permanente.

### 3. Explorar mecanismos y la megaestructura macarra

Se generaron imaginarios, mecanismos, combinaciones y pruebas de estructura suspendida. Se estudiaron células curvas, caracoles, altillos, puentes, plataformas, bandejas, troncos/ramas y fachadas textiles. La referencia macarra funciona por enlaces que se ensanchan y se habitan, no por una acumulación de cápsulas decoradas.

Los dibujos del profesor se aportaron como inspiración. Adam rechazó llevar literalmente a proyecto un único gran muro lateral con todas las piezas colgadas: prefería zigzag, ramificación, cruces y una radicalidad materialmente defendible. También rechazó el nombre «selva habitada»; se conserva únicamente en nombres históricos.

Las V2, V3 y V4 desarrollaron conjuntos, estructura, envolvente, programa y comprobaciones. Los cálculos asociados a una geometría no se trasladan automáticamente a otra. La referencia original de megaestructura se declara fantástica; no es una estructura calculada por el hecho de poseer piezas modeladas.

### 4. Aislar la unidad y descubrir problemas de uso

Se extrajo la unidad P02 para verla con detalle. Las revisiones se centraron en entradas bloqueadas, camas frente a puertas, muebles sobredimensionados, piezas flotantes y dificultades de lectura. Se hicieron plantas, secciones, modelos de habitación curva, unidad orgánica, apoyos corregidos y pruebas de materiales/colores a origen.

Se discutieron camas redondas, colchón sin plataforma de mayor diámetro, armario cóncavo transitable, mesa de dibujo plegable por canto corto, taburete y apoyos metálicos de pared. La prioridad era que el cuerpo pudiera entrar, trabajar, vestirse y acceder a la ventana, no que la forma fuese extraña por sí sola. La cama rectangular y las medidas reales regresaron como control de habitabilidad.

La ventana habitable se concretó como una **bow/bay window pequeña, elegante y curva**, con profundidad y asiento dentro de la concavidad. Un panel de vidrio no cumple esa idea. El vestidor tampoco es una circunferencia pintada: necesita espacio interior y acceso real a la ropa.

### 5. Replantear la forma desde acciones y relaciones

La lectura de Ruralex y de su cuaderno llevó a exigir coherencia entre programa, forma, estructura, instalaciones y detalle. No se quería copiar su silueta ni reducir una casa completa por un factor de escala. El trabajo pasó a mapear situaciones y proximidades antes de fijar paredes.

Se dibujaron mapas de actividad, conflictos, horarios, recorridos y atractores en una retícula. Adam rechazó colocar de entrada cuatro retiros en las esquinas porque predeterminaba la planta anterior. También cuestionó un pentágono arbitrario y el giro automático de habitaciones sobre un centro común. El interés estaba en el **tejido de cosas que pasan**, no en justificar a posteriori una planta ya decidida.

Se formularon acciones como llegar/salir, preparar/comer, acompañarse, hablar en confianza, mojar/secar, guardar/mantener y trabajar. Palabras como «desplegar/reparar» debían traducirse a actividades y objetos concretos; no valían como programa sin explicación.

### 6. Producir alternativas y comprobar qué no funcionaba

Se acordaron **20 propuestas × 2 variantes = 40 plantas**. Las colecciones y sus documentos se conservaron junto con series posteriores, atlas y un paquete denominado `80_PLANTAS`. La existencia de ese nombre no cambia lo acordado ni acredita ochenta organizaciones distintas.

Se tradujeron diagramas a formas, se modelaron variantes a cota cero y se añadieron habitaciones, conexiones orgánicas y detalles. Las críticas detectaron demasiado suelo —en fases se llegaba a unos 208–260 m² por unidad—, excesiva similitud, puertas en posiciones imposibles, elementos sin función, dormitorios interiores, obstáculos, tendederos en zonas de paso y huecos de luz enfrentados a paredes.

La corrección fue reconocer la homogeneización y recuperar organizaciones vinculadas a modos de vida. No se eligió una de las cuarenta como solución definitiva. El catálogo es material de proceso y comparación, no una prueba de cuarenta viviendas igualmente válidas.

### 7. Diferenciar V01, V02 y V03; estudiar uniones de ocho

Las nuevas familias intentaron mantener iguales prestaciones privadas sin repetir todo el espacio común: continuidad, ámbitos diferenciados y cruce/encuentro. Se estudiaron uniones dramáticas y otras casi imperceptibles, hasta una casa común de ocho.

Se trabajó con E01_ENCUENTRO, E02_COMUNA y E03_DOS_CLAROS, distintos en intensidad de lo compartido y autonomía de los grupos. Se recuperaron vestidor transitable y bow pequeña. Los baños debían participar del borde de la casa, sin convertirse en una isla central ni abrirse directamente al salón. Se hicieron nuevos documentos con sus diagramas de origen, excluyendo las plantas homogeneizadas de la entrega de esa fase; el archivo histórico conserva ambas etapas separadas.

### 8. Volver a la parcela, la luz y la herencia macarra

Se estudiaron posiciones sobre parcela y la relación con núcleo, galerías, patios, frentes y medianeras. La pregunta era cómo conservar el mecanismo de conexiones habitadas de la megaestructura al sumar unidades. Un encaje de siluetas no prueba luz, estructura, evacuación o convivencia.

Se apuntó para después un complejo que arranque más estrecho y se abra arriba, y cuya forma responda al sol mediante recortes, giros y vacíos. Adam pidió no desarrollar aún aquella forma final mientras se trabajaba la unidad. Las menciones a Grasshopper/Galápagos eran una dirección futura: no hay que convertirlas en una optimización solar ejecutada.

### 9. Poblar la planta baja y abrirla al barrio

La planta baja dejó de concebirse como vivienda privada. Se probaron sala/comedor/cocina del edificio, taller y cuidados, con aseos/almacenaje en un borde continuo y salida de escalera libre. Adam cuestionó expresamente el bloque de baños delante de las escaleras y la necesidad/cantidad de aseos inferiores.

Después se amplió el programa: biblioteca, coworking, sala de estudio transformable en exposición dominical, punto vecinal, reparación y costura, intercambio de objetos/herramientas, fuente y asientos. Se dibujaron estado cotidiano y domingo. Esta ampliación es una propuesta propia del proyecto; no se atribuye como lista literal a Ruralex ni sustituye el control de superficies total.

### 10. Pasar a documentación medida

Adam pidió dibujo arquitectónico en blanco y negro, sin render ni imagen generada: plantas calculadas desde el Rhino, ventanas convencionales, cotas, ejes, material seccionado negro, proyecciones discontinuas y tipografía Ibarra. Se guardaron estados de usuario antes de revisar, se extrajeron perfiles/secciones con RhinoCommon y se generaron PDF/SVG vectoriales y un archivo de planos/layouts.

Se retiraron sofás mal situados, se revisaron baños como borde, se desplazaron reservas de instalaciones fuera de huecos y se incorporaron puertas y medidas de cama/mesa. Se conservaron errores de API y scripts porque explican la ejecución. Hay estados de geometría, escenas de dibujo y exports distintos: no todo archivo de la carpeta representa la misma iteración.

Posteriormente se reunieron plantas y secciones y se produjo documentación de la megaestructura a 1:200. El archivo conserva esas entregas completas y sus fuentes, sin presentarlas como proyecto de ejecución.

## Reglas que siguen vigentes

- Radicalidad con razón espacial, material, climática y constructiva. No copiar la forma de Ruralex.
- Preservar lo que funciona de la megaestructura: soporte y piel separados, textiles, cruces, enlaces que se ensanchan y recorridos habitados.
- Una habitación privada por residente en las hipótesis domésticas de cuatro; compartir por elección, no por imposición.
- Entradas, puertas y circulación libres: no introducir muebles, pilares, bicicletas, pantallas o ropa en un paso necesario.
- Mantener medidas reales. La corrección de superficie se hace redistribuyendo, no reduciendo camas, personas, puertas o mesas por igual.
- En las revisiones medidas aparecen camas de **1,25 × 2,00 m** y mesas de **1,80 × 0,90 m**. No son medidas universales de todas las versiones históricas.
- Mesa de dibujo con bisagra por el canto corto y posición plegada legible; apoyos/mecanismos necesarios, sin patas permanentes que contradigan el sistema.
- Armario empotrado cóncavo y vestidor verdaderamente transitable.
- Bow pequeña con asiento cóncavo, apertura y profundidad; preservar intimidad y relación voluntaria con el común.
- Baños integrados en el contorno o espesor de servicios; no isla en la estancia ni puertas expuestas al salón.
- No colocar instalaciones delante o a través de ventanas como si no existieran. Un patinillo dibujado no demuestra dimensionado hidráulico.
- Diferenciar V01/V02/V03 por la convivencia y las acciones, sin volver a homogeneizarlas.
- La planta baja sirve al edificio y al barrio; no fijar cantidades de aseos sin estudiar uso, enunciado y necesidad.
- No afirmar simetría global donde solo hay ejes de referencia o simetría local de una bow.
- Los catálogos aislados se compararon a cota cero; los ensayos elevados tenían otra sección. No mezclar cotas de entregas distintas.
- Personas importadas desde su archivo al modelo de arquitectura; no construir la vivienda dentro de PERSONAS.3dm.
- Girar **unidades**, manteniendo parcela, planta baja y núcleo; reconectar como estaba. El giro del conjunto completo está descartado.

## Programa y escalas de convivencia

| Escala | Actividades/espacios discutidos | Condición de diseño |
|---|---|---|
| Personal | Dormir, dibujar/trabajar con A1, videollamar, vestirse, guardar, cargar móvil, sentarse en la bow, retirarse. | Intimidad, entrada fluida, luz exterior y mobiliario a tamaño real. |
| Casa de cuatro | Preparar/comer, estar acompañadas, conversar, limpieza, baño, almacenaje cotidiano. | El común debe estar equipado sin convertirse en pasillo ni bloquear dormitorios. |
| Casa/comuna de ocho | Cocina/comedor compartidos o duplicados según ensayo, trabajo/reunión, umbral o continuidad. | Comparar autonomía, simultaneidad, ruido, intimidad y superficie; no solo silueta. |
| Edificio de unas cuarenta | Acceso, escalera/ascensor, circulaciones, lavandería/logística, herramientas, cuidados, recursos y mantenimiento. | Determinar qué se comparte en grupo y qué a escala de todo el edificio. |
| Barrio / planta baja | Biblioteca, coworking, estudio/exposición, punto vecinal, taller, cocina/comedor, intercambio, plaza, fuente y asientos. | Acceso público legible; gestionar horarios, ruido, limpieza y convivencia con residentes. |

La exposición dominical conecta con los ritmos del Rastro: una misma sala puede estudiar entre semana y mostrar trabajos de residentes o vecinas los domingos. Las mesas/paneles móviles requieren almacenaje real y recorridos libres en ambos estados.

Los planos de PB de aquella revisión rotulan biblioteca de **53,05 m²**, estudio/exposición de **67,09 m²**, cuatro puestos de coworking y ocho de estudio. Son superficies geométricas de esa hipótesis, no un programa normativo definitivo. Al añadirlas cambia el presupuesto de superficie, de gestión y de instalaciones. La fuente se ensayó con radio exterior 0,85 m y asiento discontinuo a su alrededor; no se dimensionó un sistema hidráulico completo.

## Últimas revisiones técnicas y giros

### Cómo distinguir los juegos

1. `instantaneas/`: estados guardados de los documentos del usuario, conservados antes de modificaciones.
2. `modelos/TRES_UNIDADES_REVISION_TECNICA.3dm` y `E02_REVISION_TECNICA.3dm`: revisión anterior al giro, con cambios de baños, puertas y reservas de instalaciones.
3. `modelos/TRES_UNIDADES_COMPACTADAS_GIRO90.3dm`: iteración de redistribución/giro de las unidades aisladas. Sus fuentes y medidas no equivalen a una validación completa.
4. `E02_GIRO90_ENSAYO_NO_ENCAJADO.3dm`: giro rígido de todo el conjunto; **rechazado por la corrección del usuario**. No usar para continuar la ordenación.
5. `planos_E02_recta/` y `E02_RECTA_HABITACIONES_A_LA_CALLE.3dm`: revisión posterior que conserva la dirección del conjunto y núcleo, según su documentación. Revisar contra la instrucción de giro unitario antes de darla por aceptada.
6. `ENTREGA_PLANOS_1_100/`: reunión posterior de plantas y secciones, con modelos y scripts. Es la puerta de entrada documental más completa localizada, pero no elimina las revisiones anteriores.
7. `PLANOS_EDITABLES_Y_LAYOUTS_1_100.3dm`: archivo de curvas/textos/layouts generado en una etapa anterior. No asumir que sus layouts ya incorporan todo cambio posterior de plantas/secciones.

### Qué dicen los datos de compactación conservados

`COMPACTACION_Y_GIRO90.json` contiene resultados de una iteración, no las medidas definitivas de todas las láminas posteriores:

| Familia | Suelo original registrado (m²) | Suelo en esa iteración (m²) | Caja del suelo tras giro (m), sin convertirla en ancho de calle |
|---|---:|---:|---|
| V01 | 122,70 | 122,70 | 13,40 × 12,83 |
| V02 | 126,26 | 121,49 | 14,30 × 12,98 |
| V03 | 117,56 | 121,08 | 15,40 × 15,40 |

V01 no se compactó en ese registro y V03 creció en superficie, aunque se redujera su caja envolvente respecto a los brazos iniciales. Por eso no es correcto afirmar que todas quedaron más pequeñas o que ya se resolvió el problema dimensional. Las cifras de cotas exteriores, suelo geométrico y caja envolvente son magnitudes distintas.

El mismo JSON informa `all_bedrooms_face_street: false`. El giro no puede presentarse como garantía de orientación a calle de todos los dormitorios. El ensayo global rechazado registró 25,81 m transversales y unos 60,90 m² de vivienda fuera del polígono en aquella posición; son resultados de ese ensayo erróneo, **no una imposibilidad de girar y reconectar unidades individualmente**.

### Cómo se dibujó

Geometría extraída con RhinoCommon: perfiles, tapas y secciones a alturas definidas. Proyección vectorial con medidas del modelo, grosores en papel y tipografía Ibarra Real Nova. En los primeros juegos se usaron 10 mm de papel por metro real para 1:100. Los formatos cambiaron por ensayo; comprobar cada PDF y su JSON de escalas. Imprimir a 100 %, sin «ajustar a página».

Material cortado en negro, carpinterías/equipo con línea fina, proyecciones superiores discontinuas y ejes de referencia de trazo y punto. Las fuentes incluyen la escena vectorial y una variante estática de Ibarra en cursiva. Un PDF vectorial puede tener una miniatura PNG para revisión: esa miniatura no es la fuente métrica.

No se certifican cálculo estructural actualizado, evacuación, accesibilidad normativa, huecos de ascensor de fabricante, soleamiento anual, acústica ni instalaciones dimensionadas. Los ensayos y reservas de conductos se conservan con su alcance original.

## Cómo retomar el proyecto

1. Abrir la entrega reunida de plantas/secciones junto al modelo correspondiente, comprobar que ambos pertenecen a la misma revisión y guardar otra copia antes de editar.
2. Medir suelo, perímetro, ancho/profundidad y equipamiento, y cotejar con el enunciado real y el presupuesto de cuarenta residentes.
3. Revisar primero una unidad: cuatro dormitorios privados con luz, vestidor y bow; servicios de borde; llegada y uso real de sala/cocina.
4. Dentro del complejo, girar solo los objetos de unidad previstos. Conservar núcleo, PB y recorrido general; construir las uniones necesarias sin introducir obstáculos o trayectos muertos.
5. Comprobar posición sobre parcela, cielo visible, ventanas frente a obstáculos, relación con calle/medianeras, sección y usos compartidos. No equiparar encaje geométrico a derecho a abrir huecos.
6. Rehacer transferencia de cargas y detalles del soporte/envolvente solo cuando la distribución quede fijada. Los cálculos antiguos no respaldan automáticamente los cambios.
7. Regenerar plantas, secciones y cómputo de superficies desde el mismo Rhino; actualizar la selección de entrega y registrar descartes.

Este orden recoge el plan original: **investigación → acciones/conflictos → unidad → uniones → parcela y sección → soporte, conexiones y fachada textil → documentación**. No comenzar otra colección por cantidad si antes no está resuelta la habitabilidad.

## Alcance, fuentes y control del archivo

### Cobertura

Se tomó un inventario inicial de **7.664 archivos / 18.390.559.343 bytes** del proyecto, antes de la reorganización concurrente. Se copiaron sus contenidos por categorías conservando las entregas completas. El recuento final, entradas externas y huellas están en `00_GUIA_Y_CONTROL/VERIFICACION_RECOPILACION.json` e `INVENTARIO_ARCHIVOS_SHA256.json`.

Durante esta recopilación otra organización trasladó las carpetas históricas a `G3 CLAUDE`. Se localizó su registro de movimientos para recuperar las rutas de origen; **G3 CODEX no atribuye esos movimientos a esta copia ni altera el contenido de G3 CLAUDE**. El registro se conserva para explicar la procedencia. Los archivos de INVESTIGACIÓN/MAPPEADOS que seguían en la raíz también se incluyen.

Se guardan como fuentes externas localizadas la carpeta original de megaestructura en Downloads, PERSONAS.3dm y el texto inicial adjunto. También se recuperaron el Rhino original `G3_unidad_suspendida_7.3dm` y `G3_Acampada_Sol_conversacion.md` dentro de `Downloads/descargas 2`. Algunos adjuntos históricos ya no están en sus rutas conocidas: cuatro HEIC y dos capturas temporales. No se inventan sustitutos ni se declara que hayan sido recuperados. Ver `FUENTES_NO_LOCALIZADAS.json` para el resultado definitivo de búsqueda de las rutas aportadas.

Se excluyen de las copias de contenido los archivos auxiliares de Finder `.DS_Store` y `._*` (AppleDouble), registrados aparte. Sí se conservan fuentes, materiales, texturas, imágenes, vídeos si los hay, modelos, ZIP, PDF, SVG, PSD, bases/cartografía, scripts, datos y variantes, aunque estén repetidos. Las cachés o bloqueos existentes dentro de las entregas también se registran; no deben confundirse con un modelo utilizable.

### Autoría y referencias

La dirección y las decisiones de proyecto son de Adam. Las propuestas y automatizaciones son trabajo asistido desarrollado a lo largo de las conversaciones. Las páginas y material de Ruralex, cocina de 3D Warehouse, libros y otros referentes se conservan como material de referencia con su procedencia: no son autoría de este proyecto ni documentación para redistribuir como propia.

Referencias explícitas del proceso:

- [Ruralex, Ira XXX Dios](https://iraxxxdios.com/Ruralex).
- [Cuaderno público de Ruralex](https://publuu.com/flip-book/935496/2051536/page/1).
- [Cocina de 3D Warehouse](https://3dwarehouse.sketchup.com/model/891b572f-78a3-418e-b9d5-cb61abbfe7fe/Cocina).
- Cuentas de investigación señaladas: `@inquilinato_madrid` y `@acampada26s`. El archivo no afirma una investigación audiovisual exhaustiva ni vigencia de todas las publicaciones.

### Rutas y restauración

Este documento y los índices nuevos enlazan al interior de G3 CODEX. Los documentos/script originales conservan sus rutas históricas por integridad: algunas ya apuntan a ubicaciones movidas, a Downloads o a dependencias de ejecución. Consultar `MAPA_CARPETAS.json`, el inventario con origen/destino y `restaurar_estructura_original.py` para reconstruir una copia con los nombres originales. **No ejecutar scripts históricos a ciegas:** pueden escribir en rutas antiguas o regenerar modelos.

El control SHA-256 acredita copia idéntica, no la validez del diseño. Duplicados idénticos se listan sin borrarlos. Fuentes no encontradas y cualquier error de copia se separan expresamente en los informes.

## Catálogo de todas las carpetas y paquetes

Cada fila corresponde a una entrada del inventario inicial. El tamaño es contenido lógico, sin AppleDouble, no el espacio ocupado por clústeres del disco.

| Etapa / carpeta o paquete | Archivos iniciales | GB decimales | Lectura |
|---|---:|---:|---|
| [00_LEEME.md](<99_AUXILIARES_Y_DOCUMENTOS_HISTORICOS/00_LEEME.md>) | 1 | 0.0000 | Histórico o auxiliar conservado. |
| [G3_40_PLANTAS_DESDE_TEJIDOS_2026-10-18](<04_ACCIONES_TEJIDOS_Y_CATALOGOS/G3_40_PLANTAS_DESDE_TEJIDOS_2026-10-18>) | 211 | 0.0248 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_40_UNIDADES_3D_COTA0_2026-10-18](<04_ACCIONES_TEJIDOS_Y_CATALOGOS/G3_40_UNIDADES_3D_COTA0_2026-10-18>) | 407 | 2.1697 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_80_PLANTAS_2026-10-18.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_80_PLANTAS_2026-10-18.zip>) | 1 | 0.0531 | Paquete histórico completo. |
| [G3_ACCIONES_DIBUJADAS_2026-10-20](<04_ACCIONES_TEJIDOS_Y_CATALOGOS/G3_ACCIONES_DIBUJADAS_2026-10-20>) | 38 | 0.0549 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_ATLAS_40_PLANTAS_2026-10-18](<04_ACCIONES_TEJIDOS_Y_CATALOGOS/G3_ATLAS_40_PLANTAS_2026-10-18>) | 228 | 0.0305 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_CENTROS_PARA_CONVIVIR_2026-10-19](<05_NUEVAS_UNIDADES_UNIONES_Y_PARCELA/G3_CENTROS_PARA_CONVIVIR_2026-10-19>) | 2 | 0.0094 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_CONJUNTO](<02_PRIMERAS_UNIDADES_COMPLEJO_Y_LUZ/G3_CONJUNTO>) | 3 | 0.0205 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_CONTINUIDAD_PARCELA_2026-10-19](<05_NUEVAS_UNIDADES_UNIONES_Y_PARCELA/G3_CONTINUIDAD_PARCELA_2026-10-19>) | 187 | 0.0782 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_CORRECCION_40_2026-10-18](<04_ACCIONES_TEJIDOS_Y_CATALOGOS/G3_CORRECCION_40_2026-10-18>) | 532 | 1.1907 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_DECIDIR_UNIDAD_PARCELA_2026-10-19](<05_NUEVAS_UNIDADES_UNIONES_Y_PARCELA/G3_DECIDIR_UNIDAD_PARCELA_2026-10-19>) | 8 | 0.0029 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_DOCUMENTACION_LUZ_PB_V5_2026-10-16.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_DOCUMENTACION_LUZ_PB_V5_2026-10-16.zip>) | 1 | 0.1866 | Paquete histórico completo. |
| [G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS_2026-10-19](<05_NUEVAS_UNIDADES_UNIONES_Y_PARCELA/G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS_2026-10-19>) | 113 | 0.0346 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_E2_PERSONAS_A0_REFINADO_2026-10-06](<07_IMAGINARIOS_MECANISMOS_Y_ORGANIZACION/G3_E2_PERSONAS_A0_REFINADO_2026-10-06>) | 21 | 0.0245 | Histórico o auxiliar conservado. |
| [G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16](<02_PRIMERAS_UNIDADES_COMPLEJO_Y_LUZ/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16>) | 83 | 0.5782 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16 2](<02_PRIMERAS_UNIDADES_COMPLEJO_Y_LUZ/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16 2>) | 65 | 0.5758 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_MAPA_ACTIVIDADES_PARCELA_2026-10-18](<04_ACCIONES_TEJIDOS_Y_CATALOGOS/G3_MAPA_ACTIVIDADES_PARCELA_2026-10-18>) | 18 | 0.0026 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_MAPA_ACTIVIDADES_PARCELA_2026-10-18 2](<04_ACCIONES_TEJIDOS_Y_CATALOGOS/G3_MAPA_ACTIVIDADES_PARCELA_2026-10-18 2>) | 17 | 0.0024 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_MECANISMOS_EN_PARCELA_17_DIBUJOS.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_MECANISMOS_EN_PARCELA_17_DIBUJOS.zip>) | 1 | 0.0391 | Paquete histórico completo. |
| [G3_MECANISMOS_EN_PARCELA_2026-10-05](<07_IMAGINARIOS_MECANISMOS_Y_ORGANIZACION/G3_MECANISMOS_EN_PARCELA_2026-10-05>) | 41 | 0.0461 | Histórico o auxiliar conservado. |
| [G3_MEMORIA_INTEGRAL_DEL_PROCESO_2026-10-20.md](<99_AUXILIARES_Y_DOCUMENTOS_HISTORICOS/G3_MEMORIA_INTEGRAL_DEL_PROCESO_2026-10-20.md>) | 1 | 0.0002 | Histórico o auxiliar conservado. |
| [G3_MODELOS_HERENCIA_MACARRA_2026-10-19](<05_NUEVAS_UNIDADES_UNIONES_Y_PARCELA/G3_MODELOS_HERENCIA_MACARRA_2026-10-19>) | 115 | 0.5450 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_ORGANIZACION_PARCELA_2026-10-06](<07_IMAGINARIOS_MECANISMOS_Y_ORGANIZACION/G3_ORGANIZACION_PARCELA_2026-10-06>) | 3 | 0.0028 | Histórico o auxiliar conservado. |
| [G3_P02_A_REVISADA_2026-10-18](<03_HABITACION_Y_UNIDAD_P02/G3_P02_A_REVISADA_2026-10-18>) | 12 | 0.0006 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_P02_A_REVISADA_DIBUJOS_Y_RHINO.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_P02_A_REVISADA_DIBUJOS_Y_RHINO.zip>) | 1 | 0.0004 | Paquete histórico completo. |
| [G3_P02_CORREGIDA_APOYOS_2026-10-18](<03_HABITACION_Y_UNIDAD_P02/G3_P02_CORREGIDA_APOYOS_2026-10-18>) | 7 | 0.0062 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_P02_HABITACION_CURVA_2026-10-18](<03_HABITACION_Y_UNIDAD_P02/G3_P02_HABITACION_CURVA_2026-10-18>) | 6 | 0.0174 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_P02_MATERIALES_ORIGEN_2026-10-18](<03_HABITACION_Y_UNIDAD_P02/G3_P02_MATERIALES_ORIGEN_2026-10-18>) | 17 | 0.0496 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_P02_MATERIALES_Y_TEXTURAS_000.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_P02_MATERIALES_Y_TEXTURAS_000.zip>) | 1 | 0.0121 | Paquete histórico completo. |
| [G3_P02_MODELO_COMPLETO_EDITABLE.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_P02_MODELO_COMPLETO_EDITABLE.zip>) | 1 | 0.0008 | Paquete histórico completo. |
| [G3_P02_MODELO_PLANTA_COMPLETA_2026-10-18](<03_HABITACION_Y_UNIDAD_P02/G3_P02_MODELO_PLANTA_COMPLETA_2026-10-18>) | 11 | 0.0023 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_P02_PLANTAS_SECCIONES_2026-10-18](<03_HABITACION_Y_UNIDAD_P02/G3_P02_PLANTAS_SECCIONES_2026-10-18>) | 31 | 0.0038 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_P02_TRES_PLANTAS_NUEVE_SECCIONES.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_P02_TRES_PLANTAS_NUEVE_SECCIONES.zip>) | 1 | 0.0031 | Paquete histórico completo. |
| [G3_P02_TRES_PLANTAS_SEIS_SECCIONES.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_P02_TRES_PLANTAS_SEIS_SECCIONES.zip>) | 1 | 0.0015 | Paquete histórico completo. |
| [G3_P02_UNIDAD_ORGANICA_2026-10-18](<03_HABITACION_Y_UNIDAD_P02/G3_P02_UNIDAD_ORGANICA_2026-10-18>) | 8 | 0.0006 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_P02_UNIDAD_ORGANICA_PLANTA_Y_SECCIONES.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_P02_UNIDAD_ORGANICA_PLANTA_Y_SECCIONES.zip>) | 1 | 0.0004 | Paquete histórico completo. |
| [G3_PLANOS_TECNICOS_2026-10-20](<06_PLANOS_TECNICOS_Y_RHINO/G3_PLANOS_TECNICOS_2026-10-20>) | 134 | 0.1988 | Documentación y fuentes de distintas revisiones; verificar correspondencia. |
| [G3_PLANTAS_FORMAS_DE_VIVIR_2026-10-19](<05_NUEVAS_UNIDADES_UNIONES_Y_PARCELA/G3_PLANTAS_FORMAS_DE_VIVIR_2026-10-19>) | 25 | 0.0043 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_PLANTAS_FORMAS_DE_VIVIR_2026-10-19.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_PLANTAS_FORMAS_DE_VIVIR_2026-10-19.zip>) | 1 | 0.0019 | Paquete histórico completo. |
| [G3_PRIMER_MAPA_ACTIVIDADES_Y_PARCELA.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_PRIMER_MAPA_ACTIVIDADES_Y_PARCELA.zip>) | 1 | 0.0015 | Paquete histórico completo. |
| [G3_REFERENCIAS_RURALEX_COCINA_2026-10-18](<01_INVESTIGACION_PARCELA_Y_REFERENCIAS/G3_REFERENCIAS_RURALEX_COCINA_2026-10-18>) | 298 | 0.1512 | Investigación y referencias; no resultado arquitectónico final. |
| [G3_REVISION_2026-10-08](<02_PRIMERAS_UNIDADES_COMPLEJO_Y_LUZ/G3_REVISION_2026-10-08>) | 82 | 0.1367 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_RHINO_EN_VIVO](<06_PLANOS_TECNICOS_Y_RHINO/G3_RHINO_EN_VIVO>) | 1 | 0.0000 | Documentación y fuentes de distintas revisiones; verificar correspondencia. |
| [G3_SELVA_HABITADA_V2_2026-10-16](<02_PRIMERAS_UNIDADES_COMPLEJO_Y_LUZ/G3_SELVA_HABITADA_V2_2026-10-16>) | 51 | 0.0815 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_SELVA_HABITADA_V2_2026-10-16.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_SELVA_HABITADA_V2_2026-10-16.zip>) | 1 | 0.0369 | Paquete histórico completo. |
| [G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16](<02_PRIMERAS_UNIDADES_COMPLEJO_Y_LUZ/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16>) | 70 | 1.9117 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_SELVA_RADICAL_RHINO_V3_2026-10-16](<02_PRIMERAS_UNIDADES_COMPLEJO_Y_LUZ/G3_SELVA_RADICAL_RHINO_V3_2026-10-16>) | 23 | 0.4073 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_SOL_SELVA_2026-10-11](<01_INVESTIGACION_PARCELA_Y_REFERENCIAS/G3_SOL_SELVA_2026-10-11>) | 3 | 0.0082 | Investigación y referencias; no resultado arquitectónico final. |
| [G3_TEJIDOS_A_PLANTA_40_2026-10-18](<04_ACCIONES_TEJIDOS_Y_CATALOGOS/G3_TEJIDOS_A_PLANTA_40_2026-10-18>) | 435 | 0.0378 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_TEJIDO_REGLAS_ALTERNATIVAS_EDITABLE.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_TEJIDO_REGLAS_ALTERNATIVAS_EDITABLE.zip>) | 1 | 0.0016 | Paquete histórico completo. |
| [G3_TEJIDO_REGLAS_Y_ALTERNATIVAS_2026-10-18](<04_ACCIONES_TEJIDOS_Y_CATALOGOS/G3_TEJIDO_REGLAS_Y_ALTERNATIVAS_2026-10-18>) | 22 | 0.0026 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_TEJIDO_REGLAS_Y_ALTERNATIVAS_2026-10-18 2](<04_ACCIONES_TEJIDOS_Y_CATALOGOS/G3_TEJIDO_REGLAS_Y_ALTERNATIVAS_2026-10-18 2>) | 21 | 0.0024 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_UNIDAD](<02_PRIMERAS_UNIDADES_COMPLEJO_Y_LUZ/G3_UNIDAD>) | 14 | 0.0857 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_UNIDADES_4_PERSONAS_2026-10-20](<05_NUEVAS_UNIDADES_UNIONES_Y_PARCELA/G3_UNIDADES_4_PERSONAS_2026-10-20>) | 4 | 0.0284 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_UNIDAD_AISLADA_DETALLE_2026-10-16](<03_HABITACION_Y_UNIDAD_P02/G3_UNIDAD_AISLADA_DETALLE_2026-10-16>) | 56 | 0.4536 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_UNIDAD_TEJIDO_ACTIVIDADES_2026-10-18](<04_ACCIONES_TEJIDOS_Y_CATALOGOS/G3_UNIDAD_TEJIDO_ACTIVIDADES_2026-10-18>) | 17 | 0.0029 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_UNIDAD_TEJIDO_ACTIVIDADES_2026-10-18 2](<04_ACCIONES_TEJIDOS_Y_CATALOGOS/G3_UNIDAD_TEJIDO_ACTIVIDADES_2026-10-18 2>) | 17 | 0.0029 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_UNIDAD_TEJIDO_ACTIVIDADES_EDITABLE.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_UNIDAD_TEJIDO_ACTIVIDADES_EDITABLE.zip>) | 1 | 0.0021 | Paquete histórico completo. |
| [G3_UNIONES_COMUNAS_2026-10-19](<05_NUEVAS_UNIDADES_UNIONES_Y_PARCELA/G3_UNIONES_COMUNAS_2026-10-19>) | 30 | 0.0160 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [G3_UNIONES_COMUNAS_2026-10-19.zip](<08_PAQUETES_ZIP_ORIGINALES/G3_UNIONES_COMUNAS_2026-10-19.zip>) | 1 | 0.0064 | Paquete histórico completo. |
| [IMAGINARIOS_G3_16_DIBUJOS.zip](<08_PAQUETES_ZIP_ORIGINALES/IMAGINARIOS_G3_16_DIBUJOS.zip>) | 1 | 0.0520 | Paquete histórico completo. |
| [IMAGINARIOS_G3_2026-10-05](<07_IMAGINARIOS_MECANISMOS_Y_ORGANIZACION/IMAGINARIOS_G3_2026-10-05>) | 21 | 0.0538 | Histórico o auxiliar conservado. |
| [INVESTIGACIÓN](<01_INVESTIGACION_PARCELA_Y_REFERENCIAS/INVESTIGACIÓN>) | 3993 | 4.2890 | Investigación y referencias; no resultado arquitectónico final. |
| [MAPPEADOS](<01_INVESTIGACION_PARCELA_Y_REFERENCIAS/MAPPEADOS>) | 10 | 4.2711 | Investigación y referencias; no resultado arquitectónico final. |
| [MEGAESTRUCTURA_CLAUDE](<02_PRIMERAS_UNIDADES_COMPLEJO_Y_LUZ/MEGAESTRUCTURA_CLAUDE>) | 51 | 0.2800 | Ensayos y revisiones; comparar con decisiones vigentes. |
| [MEGAESTRUCTURA_MACARRA_PLANOS_2026-10-20](<06_PLANOS_TECNICOS_Y_RHINO/MEGAESTRUCTURA_MACARRA_PLANOS_2026-10-20>) | 30 | 0.0469 | Documentación y fuentes de distintas revisiones; verificar correspondencia. |
| [MODELOS_ENGEL_p93-94](<99_AUXILIARES_Y_DOCUMENTOS_HISTORICOS/MODELOS_ENGEL_p93-94>) | 5 | 0.0174 | Histórico o auxiliar conservado. |
| [_tmp_prev](<99_AUXILIARES_Y_DOCUMENTOS_HISTORICOS/_tmp_prev>) | 36 | 0.0113 | Histórico o auxiliar conservado. |
| [output](<99_AUXILIARES_Y_DOCUMENTOS_HISTORICOS/output>) | 13 | 0.0154 | Histórico o auxiliar conservado. |

## Memoria de desarrollo conservada

A continuación se incorpora el cuerpo narrativo de la memoria del **20 de octubre de 2026**, hasta su guía de fuentes/modelos. Sus observaciones describen el estado conocido en ese corte. Los apartados anteriores aclaran las revisiones posteriores encontradas y tienen prioridad para entender el archivo actual. No es una transcripción literal de todas las conversaciones.

La memoria histórica completa, incluido su inventario largo de `.3dm`, se conserva sin cambios en la carpeta 99. En este documento se han redirigido sus enlaces al archivo nuevo cuando se conoce la correspondencia. Los originales permanecen intactos.

---

## G3 · Memoria integral del proceso y guía de archivos Rhino

**Fecha de corte: 20 de octubre de 2026.**
**Proyecto: vivienda colectiva en Ribera de Curtidores 31, El Rastro, Madrid.**
**Autoría de las decisiones e intenciones: Adam. Desarrollo y asistencia: conversaciones y archivos del proyecto.**

Este documento reúne el proceso desde su arranque documentado hasta el punto actual: investigación urbana, acampada, megaestructura, unidad doméstica, acciones, tejidos, catálogos, correcciones, agrupaciones, planta baja y planos técnicos. Incluye las decisiones rechazadas y los problemas que siguen abiertos, porque también explican cómo hemos llegado aquí.

Es una memoria consolidada, no una transcripción literal de todas las conversaciones. Se apoya en el historial disponible, las memorias del proyecto y los archivos localizados en disco. La existencia de un archivo no demuestra que su arquitectura esté resuelta. Las fechas de las carpetas identifican entregas, no necesariamente el día exacto de cada conversación. Las cifras históricas se atribuyen a su versión y no se trasladan automáticamente a otra.

> **Estado descrito por la memoria del 20 de octubre, no una nueva comprobación:** Adam ha cuestionado el tamaño de las unidades, especialmente V02, y ha pedido revisar también las demás. Esa revisión dimensional y de encaje está pendiente. Los planos técnicos existentes registran geometría previa; no deben presentarse como si ya incorporasen una compactación resuelta.

### Índice

1. Punto de partida y encargo.
2. Investigación de parcela y barrio.
3. Acampada y traducción a vivienda.
4. Evolución cronológica y correcciones.
5. Programa y acciones.
6. Unidad: habitación, vestidor, bow, mesa, servicios y común.
7. Tejidos, cuarenta alternativas y pérdida de diversidad.
8. Agregación y herencia de la megaestructura.
9. Luz, parcela y forma futura.
10. Planta baja pública.
11. Documentación técnica y medidas actuales.
12. Decisiones, descartes y pendientes.
13. Guía rápida de Rhino con rutas completas.
14. Fuentes y documentos para continuar.
15. Inventario de todos los .3dm localizados en la carpeta del proyecto.

### 1. Punto de partida y encargo

El proyecto busca una vivienda colectiva para jóvenes con una posición crítica frente a la dificultad de acceder a la vivienda, el aislamiento doméstico y la privatización de recursos. La acampada funciona como referencia de organización y cooperación, no como una imagen que copiar literalmente ni como estándar técnico de vivienda permanente.

La dirección expresada por Adam es una arquitectura **macarra, radical, entrelazada, con telas, cruces, conexiones y recorridos que se convierten en lugares**. La radicalidad debe sostenerse con distribución, medidas, estructura, detalles, mantenimiento y funcionamiento cotidiano. No basta una forma espectacular ni una planta convencional con curvas añadidas.

La escala de trabajo se ha formulado como habitación personal → unidad de cuatro → convivencia de ocho → comunidad de unas cuarenta personas → barrio. Cuatro personas por unidad es una hipótesis comparable que se ha utilizado durante el desarrollo, no una ley que justifique cualquier superficie. También se trabajó con un objetivo provisional de unos 1.500 m²; debe comprobarse con el enunciado y un cómputo completo. Los antecedentes de 32 unidades pertenecen a una etapa anterior y no equivalen a las diez viviendas de cuatro de ensayos posteriores.

El usuario prefiere llamar al edificio **complejo**. El nombre «selva habitada» fue rechazado; aparece aquí solo porque permanece en nombres históricos de carpetas y archivos.

### 2. Investigación de parcela y barrio: el arranque documentado

En septiembre se reunió investigación de Ribera de Curtidores 31 y El Rastro: contexto urbano, actividades, frentes, patrones materiales, comercio, temporalidad del mercado, relación público/privado, fotos propias, cartografía y referencia catastral.

La carpeta de investigación documenta un compendio de 43 páginas, un recorrido de Street View con 23 panorámicas y 11 registros históricos del número 31, un censo de 42 frentes, originales GML catastrales y derivados GeoJSON en EPSG:25830. Son recuentos documentados en su LEEME, no una nueva auditoría independiente de cada fuente. Existen archivos QGIS, CSV, figuras, alzados y datos de sombras/sol por altura.

La investigación distingue tres niveles útiles: **A, medido; B, inferido por modelo o lectura visual; C, hipótesis**. No se debe dibujar una hipótesis formal como si fuese un dato observado.

El megapanel de cinco A3 y sus versiones PDF/PNG/PSD sintetizan esa base. La maqueta del entorno y las exploraciones sobre mecanismos pertenecen también al proceso de relación entre lugar y proyecto. No sustituyen el levantamiento de la parcela ni una ordenación urbanística comprobada.

Rutas principales:

- `INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/`: compendio, datos, figuras y scripts.
- `INVESTIGACIÓN/01_ENCARGO_Y_TEXTO_BASE/`: protocolo y texto de partida.
- `INVESTIGACIÓN/PANEL_FINAL_5xA3/`: síntesis gráfica urbana.
- `MAPPEADOS/`: mapas propios y modelo del entorno.

### 3. Acampada: qué se investigó y qué se tradujo

Adam pidió ir a fuentes del movimiento de vivienda, especialmente Instagram y TikTok, y descartó usar como base los medios televisivos consultados antes de esa corrección. Indicó expresamente **@inquilinato_madrid**; también se trabajó con **@acampada26s**, textos de la acampada y una lectura crítica desde medios afines.

El cuaderno de Sol distingue publicaciones originales leídas, descripciones de reels y vídeos no revisados íntegramente. No hay una muestra suficiente para describir estadísticamente a toda la generación Z. Las acciones y personas de proyecto son hipótesis situadas, no resultados de una encuesta representativa.

Lo que interesa trasladar:

- Acogida, orientación y llegada sin invadir intimidad.
- Recursos compartidos, herramientas, comida, logística y mantenimiento.
- Comisiones, responsabilidades y acuerdos de uso.
- Espacios apropiables junto a recorridos que nunca se bloquean.
- Encuentro voluntario y derecho a retirarse.
- Capacidad de montar, reparar, recoger y transformar.
- Relación con vecinas, comercios y barrio.
- Protección climática como tarea material y colectiva.

Lo que no se traslada sin rediseñar: una lona de emergencia como cerramiento de vivienda permanente; una proporción inventada de tiendas/carpa como regla arquitectónica; ocupación máxima obligatoria; pasillos usados como almacén; apariencia de precariedad sin resolver confort, higiene o seguridad.

La crítica debe aparecer en cómo se reparte el espacio, qué puede compartirse y quién mantiene las cosas. No se agota en símbolos de protesta o una fachada textil.

### 4. Recorrido cronológico: de la célula al problema actual

#### 4.1. Primeras células suspendidas y agrupaciones, primeros días de octubre

Se estudiaron la unidad suspendida, sus variantes, el caracol, altillo, aperturas, bloque de vidrio, acero grafito y piezas curvas. La variante F2 —esquina curva y ala semicircular— fue un antecedente apreciado. Se compararon alternativas de escalera y ventana, mesas de trabajo/comida y baño curvo.

La revisión del 8 de octubre reconstruyó unidades y conjuntos y propuso alternativas de dúplex y una planta. Detectó que conectar objetos mediante plataformas no bastaba para construir convivencia. Aquel conjunto seguía demasiado lineal y con exceso de superficie; es un antecedente parcial, no el proyecto final.

#### 4.2. Megaestructura macarra y rechazo de una única verticalidad

Adam pidió mantener el zigzag, las ramificaciones, los claros y una complejidad casi laberíntica. Las fotos y dibujos del profesor —gran muro lateral, plataforma superior y piezas colgadas— se aportaron como estímulo, pero Adam rechazó convertirlos en la solución literal: no quería concentrar toda la organización en un solo lateral vertical.

La pregunta pasó a ser cómo escalar mecanismos y proporciones a vivienda colectiva, conservando solo lo que mantiene función. Colgar, apoyar, enlazar, cubrir y recorrer debían adquirir una razón material y espacial.

#### 4.3. V2, V3 y V4, 11–16 de octubre

Se produjeron cuadernos, imágenes y modelos del complejo; las versiones iniciales fueron criticadas por alejarse de la megaestructura de referencia. Adam pidió orden, cálculo y detalles que sostuvieran la radicalidad.

La V4 ensayó diez pabellones para cuarenta residentes sobre tres grupos de soportes ramificados, con ascensores y escaleras. Su documentación contiene un modelo elástico lineal preliminar de barras y comprobaciones de subsistemas, además de detalles de nudo, bandeja/envolvente y ascensor. «Calculada» en el nombre no significa estructura certificada. Sus comprobaciones no validan los modelos posteriores, que cambiaron geometría, cargas y distribución.

La V4 fue un antecedente formal útil, pero sus habitaciones eran demasiado pequeñas en esa etapa. Se pidió situar el conjunto con contexto y extraer una unidad P02 para verla de cerca.

#### 4.4. P02: el cuerpo y el mobiliario desmienten la imagen, 16–18 de octubre

Al acercarse aparecieron camas mal encajadas, muebles junto a puertas, tamaños incoherentes, piezas flotando y problemas de lectura. Adam pidió corregir la habitación antes de seguir repitiendo unidades y situar el modelo a cota cero.

Se exploraron camas redondas, colchón sin pedestal mayor, armarios cóncavos, mesas de dibujo plegables, taburetes, dos pequeños slabs metálicos junto a la cama con carga del móvil, almacenamiento integrado y ventanas habitables. Algunas ideas siguen como antecedentes y no están desarrolladas técnicamente en todas las versiones.

Se hicieron distintas plantas y secciones. Adam rechazó soluciones que bloqueaban el acceso, el armario o la mesa. Pidió simetría y equivalencia entre habitaciones en una fase, y después cuestionó que eso condujera a una planta rígida con pasillo central.

Los modelos con piezas flotando se corrigieron buscando apoyos y niveles coherentes. No se considera resuelto un interior porque desde lejos parezca convincente.

#### 4.5. Ruralex y cambio de método, 18 de octubre

Adam aportó Ruralex y una cocina de 3D Warehouse. Ruralex se estudió como relación entre programa, diagramas, estructura, instalaciones, envolvente y detalle. El registro local documenta lectura de su publicación visual; no se obtuvo un modelo nativo editable de Ruralex ni se verificaron todos sus cálculos.

No se ha demostrado que Ruralex naciera de un algoritmo de atractores. Ese método es una interpretación propia del proyecto G3. Tampoco se debe atribuir a Ruralex la biblioteca o el coworking que estamos inventando para nuestra parcela.

La cocina se inspeccionó mediante su ficha y vista pública; no consta una importación efectiva del modelo CAD descargado. Los muebles modelados son desarrollos propios/esquemáticos, no una copia nativa del archivo del enlace.

El cambio importante: dejar de decidir primero la silueta y empezar por **acciones, objetos, cuerpos, proximidades, conflictos, tiempos y recorridos**.

Referencias aportadas:

- [Ruralex, Ira XXX Dios](https://iraxxxdios.com/Ruralex).
- [Cocina, 3D Warehouse](https://3dwarehouse.sketchup.com/model/891b572f-78a3-418e-b9d5-cb61abbfe7fe/Cocina).

#### 4.6. Tejido de cosas que pasan

Adam imaginó una hoja completa con retícula, puntos y relaciones que se cruzan; de ese tejido deberían surgir lugares. Rechazó un diagrama pentagonal sin fundamento y también colocar de antemano cuatro retiros en las esquinas, porque reproducía la planta anterior disfrazada de análisis.

Se discutió cómo justificar por qué una acción está junto a otra y por qué una distancia o una posición concreta. Las relaciones deben tener motivos —ruido, agua, intimidad, duración, traslado, luz— y no obedecer solo a composición gráfica.

No hay objetividad absoluta: pesos, umbrales y coordenadas son decisiones que hay que declarar y comparar. Un diagrama no demuestra por sí mismo una distribución correcta.

#### 4.7. Veinte propuestas por dos variantes, y una segunda serie

Adam confirmó expresamente **20 propuestas × 2 variantes = 40 plantas**. Después pidió más ensayos, aparte de los ya hechos, derivados de las formas y relaciones de los diagramas, no de copiar Ruralex.

Se generaron varias series: atlas inicial, traducción del tejido a otras cuarenta plantas, documentación ampliada y bases Rhino 2D. No son una única colección inequívoca de cuarenta casos: existen series diferentes con códigos parecidos. Las publicaciones de hasta 88 páginas pertenecen a ese ciclo de exploración.

Las traducciones literales llegaron a unidades de unos 208–260 m², según la conversación y los ensayos, excesivas para la hipótesis de cuatro habitantes. La separación elástica de huellas y las conexiones gastaban demasiado suelo. Los documentos de la serie reconocen que cambiar deformaciones no equivale a inventar cuarenta organizaciones sociales independientes.

#### 4.8. Modelar las cuarenta y corregirlas

Adam pidió modelar todas, sin apilar, con conexiones orgánicas y pavimento a Z=0. Se generó un catálogo 3D y archivos individuales.

La inspección cercana reveló fallos generalizados: soportes u objetos en medio, bicicleta y tendedero dentro de la vivienda sin razón, dormitorios interiores, ventanas hacia muros, accesos sobre curvas y espacios sobredimensionados. N01A, N01B y N04A fueron ejemplos; Adam aclaró que el problema afectaba al conjunto.

La corrección reconstruyó el catálogo alrededor de cuatro habitaciones con ventanas exteriores, accesos rectos, eliminación de objetos impropios y pruebas de pasos. Su documentación registra unas huellas interiores geométricas de 112,86–113,72 m² y dormitorios de 16,36 m² en esa versión. Se retiró la cama redonda y se utilizaron colchones rectangulares.

Pero se perdió el vestidor verdaderamente transitable y la ventana habitable profunda. Además, las cuarenta quedaron demasiado parecidas. Es un error de proceso reconocido: corregir no debía borrar la diversidad de cómo se vive.

#### 4.9. Recuperar prestaciones y diversidad, 19 de octubre

Se produjeron V01, V02 y V03, recuperando vestidor y ventana. V01 ensayaba continuidad; V02, dos ámbitos desplazados y conectados; V03, una organización alrededor de un centro. V02 se consideró prometedora por permitir distintos ritmos de actividad, sin proclamarse elegida final.

La primera ventana profunda resultaba demasiado grande. Adam precisó que quería una **bow o bay pequeña, elegante y curva, en cuya concavidad se pueda sentar el cuerpo**. No un panel, un simple hueco ni un banco pegado a una ventana plana.

Se hicieron agrupaciones de ocho: umbral compartido, encuentro dramático y continuidad de comuna. Las pruebas V01/V03 no debían ser solo dos casas tocándose: había que reorganizar cocinas, mesas, accesos y apropiación del espacio común.

Adam rechazó los baños como isla central dentro del círculo habitable. Se rehízo un borde de servicios con llegada filtrada. El documento único debía incluir únicamente plantas nuevas corregidas y sus antecedentes diagramáticos, manteniendo sus diferencias, no el catálogo homogeneizado como propuesta vigente.

#### 4.10. Del interior a soporte, planta baja y acceso real

Se modelaron las nuevas organizaciones y tres ensayos sobre parcela: E01_ENCUENTRO, E02_COMUNA y E03_DOS_CLAROS. Se añadieron bandejas, soportes ramificados, cubiertas y membranas, escalera, ascensor y galerías.

Adam pidió que la planta baja no fuera una vivienda triste aislada, sino parte de la vida común y del barrio. Rechazó una caja sin sentido delante de la escalera y cuestionó los aseos colocados abajo. La corrección llevó los servicios al borde y despejó la descarga de la escalera.

La cota +4,20 m de vivienda es un ensayo de sección, no un resultado de optimización solar ni una altura urbanística aprobada.

#### 4.11. Tres unidades aisladas y dibujo propio, 20 de octubre

Adam pidió las tres unidades de cuatro personas juntas en un solo Rhino, con cubierta, para sacar sus planos. También pidió abrir el catálogo de cuarenta y después cuestionó su utilidad en la entrega por su semejanza. No se seleccionó automáticamente una de aquellas cuarenta como solución final.

Quería contar el proceso desde sus propios planos: acciones y vida cotidiana sobre formas reales, no dibujos genéricos. Se ensayó un lenguaje gráfico blanco y negro, rápido, sucio, superpuesto, con Ibarra. Las primeras imágenes sin geometría de referencia se descartaron. Los dibujos por IA son material narrativo, no documentación métrica.

#### 4.12. Planos técnicos medidos y ampliación pública

La petición cambió expresamente a planos arquitectónicos calculados y medidos desde Rhino: tres unidades de cuatro y E02_COMUNA/E02_REVISION_NATIVA de ocho sobre pilares, con escala física, ventanas convencionales, ejes, cotas, grosores, negro en corte y discontinuas en proyección.

Se guardaron instantáneas del estado del usuario, se extrajo geometría nativa, se revisaron modelos en copias y se generaron PDF/SVG vectoriales y un Rhino de láminas editables. Se retiraron sofás, se trabajó el baño como perímetro continuo y se llevaron montantes al borde de servicios para evitar ventanas.

Después Adam pidió más programa público sobre la parcela: coworking, biblioteca, estudio/exposición dominical, fuente y asientos. Se incorporó una ampliación de planta baja a E02 y dos estados de uso. Al decir «también V02», aclaró que se refería a **V02 de cuatro personas**, que ya está incluida como plano individual; no equivale a E02_COMUNA.

El último giro es la revisión de tamaño: frente de parcela de unos 15 m y unidades que parecen demasiado extensas. No está resuelta todavía esa compactación.

### 5. Programa: acciones antes que habitaciones etiquetadas

Las veinte acciones del estudio no son veinte recintos ni veinte personas. Varias acciones pueden compartir un lugar por horarios; una acción puede repetirse en varios lugares. No todas tienen que estar dentro de cada casa.

| Código | Acción | Exigencias que afectan al espacio |
|---|---|---|
| A01 | Dormir | Intimidad, silencio, oscuridad controlable, acceso despejado. |
| A02 | Vestirse | Cuerpo de pie, ropa accesible, recorrido sin chocar con cama o puerta. |
| A03 | Ducharse | Agua, extracción, intimidad y transición seca. |
| A04 | Secar ropa | Tiempo, ventilación y humedad; no tender en medio del paso. |
| A05 | Guardar ropa | Capacidad real, acceso y relación con vestirse. |
| A06 | Entrevista o llamada en vídeo | Fondo, voz, intimidad, conexión y control acústico. |
| A07 | Cocinar | Preparación, apertura de equipos, limpieza y simultaneidad. |
| A08 | Comer | Apoyo individual o compartido, sin convivencia obligatoria. |
| A09 | Conversar en grupo | Encuentro voluntario y posibilidad de retirarse. |
| A10 | Hablar en privado | Confidencialidad y llegada discreta. |
| A11 | Dibujar | Tablero A1 grande, postura, luz de tarea y material que puede quedar montado. |
| A12 | Guardar maqueta | Objetos frágiles, volumen y traslado. |
| A13 | Cortar maqueta | Superficie resistente, ruido, recortes y limpieza. |
| A14 | Coser una tela | Extensión de pieza, herramientas y almacenamiento. |
| A15 | Reparar bicicleta | Maniobra y suciedad; no junto a preparar comida. |
| A16 | Llegar con cargas | Compra, mochila, materiales, giros y descarga. |
| A17 | Recibir visita | Umbral, espera y control de intimidad. |
| A18 | Salir con prisa | Llaves, abrigo y recorrido libre; llegar/salir pueden compartir acceso. |
| A19 | Limpiar y recoger | Útiles, residuos, agua, tiempo y reparto de tareas. |
| A20 | Guardar herramientas | Capacidad, seguridad, devolución y cercanía al trabajo. |

Se reclamaron escenas más concretas ligadas a la acampada: llegar tarde con material, dibujar mientras otra persona duerme, desplegar una pancarta temporalmente, reparar una tela, recibir a alguien sin exponer el dormitorio, cocinar mientras se organiza una actividad. «Desplegar/reparar» no debía quedarse en una etiqueta abstracta: hay que decir qué se despliega, cuánto ocupa, durante cuánto tiempo y dónde se guarda.

Las relaciones que justifican proximidad o separación son: compartir agua/extracción, trasladar objetos, ruido, confidencialidad, humedad, suciedad, duración, horarios, luz y posibilidad de dejar un trabajo montado. Los pesos de esas relaciones siguen siendo hipótesis de diseño.

### 6. La unidad: prestaciones que no deben desaparecer al compactar

#### Habitación individual

Cada residente necesita un retiro propio. Equivalencia de prestaciones no exige que las cuatro esquinas se resuelvan por colocaciones arbitrariamente distintas ni que todo el edificio sea simétrico. La cama no debe quedar frente al hueco bloqueando la entrada. Puertas sobre tramos rectos y giros fluidos; acceso simultáneo a cama, ropa y trabajo.

La cama redonda se exploró, pero no es un requisito final obligatorio. El criterio es un colchón bien dimensionado, sin plataforma inferior de mayor huella que robe circulación. En los modelos recientes figura cama de 1,25 × 2,00 m.

#### Mesa de dibujo

El tablero reciente mide 1,80 × 0,90 m. Debe poder plegarse/articularse por su **canto corto**, con soporte mural y bloqueo a distintos ángulos. No se representa como mesa fija con patas permanentes. Hay que revisar uso abierto, plegado, taburete y entrada al mismo tiempo. El herraje resistente y su anclaje todavía requieren cálculo y detalle.

El panel independiente para exponer proyectos en el dormitorio se eliminó por petición expresa. Eso no impide colgar referencias directamente en pared junto al trabajo. Los paneles móviles de una exposición pública en planta baja tienen otra función y fueron pedidos después.

#### Vestidor cóncavo transitable

No basta un armario empotrado de 55 cm. El cuerpo entra en el nicho y sigue la curva; la ropa ocupa profundidad real alrededor. El espesor de almacenaje y el espacio de paso no se cuentan dos veces. Tiene que seguir siendo accesible con cama y mesa en uso.

#### Bow/bay pequeña

La pared y la ventana forman un pequeño saliente curvo con concavidad interior y asiento adaptado. Debe verse en planta y sección dónde se sienta el cuerpo, cómo llega, dónde quedan piernas, vidrio, protección y tela. El retiro mirando fuera puede coexistir con vida colectiva: ofrecer intimidad no implica prohibir el encuentro.

#### Baños

No pueden ser una isla central dentro del salón ni cajas sueltas dentro de otra caja. Deben integrarse en el contorno o borde de servicios, con acceso filtrado y sin puertas de WC expuestas directamente al estar. No se admite resolver una planta incorrecta añadiendo una pantalla que obstruya el paso.

#### Estar, cocina y llegada

El espacio común no se reduce a cocina/comedor ni a un vacío sobrante. Debe permitir actividades diferentes y una llegada reconocible. El sofá no es obligatorio: se retiró de los planos técnicos recientes. No se coloca en la entrada para «llenar» un hueco.

Bicicleta, tendedero, taller y logística no deben convertirse en obstáculos permanentes domésticos. Parte de ese programa corresponde a la escala del edificio o de la planta baja.

### 7. Lo aprendido con los catálogos

1. Un tejido de relaciones no se puede construir literalmente sin ajustar cuerpos, recorridos, luces y superficies.
2. Cuarenta siluetas no equivalen a cuarenta maneras de vivir.
3. Separar todas las huellas para evitar solapes puede producir viviendas gigantes.
4. Compactar imponiendo la misma solución puede borrar el objetivo de investigar diversidad.
5. Una prueba de disco de paso en 2D no es una certificación de accesibilidad.
6. Una ventana exterior en una unidad aislada puede quedar frente a un muro al agruparla.
7. Un objeto geométricamente válido puede estar mal colocado o no tener función.
8. La corrección de habitaciones debe comprobarse de cerca antes de multiplicarse.
9. Las cuarenta sirven para contar ensayos y errores; no tienen que ocupar la entrega como cuarenta propuestas finales equivalentes.
10. Ninguna fue elegida automáticamente como definitiva. V01/V02/V03 posteriores son nuevas organizaciones y también están abiertas a revisión.

### 8. Agregación: qué compartimos y qué heredamos

Se probaron unidades independientes con umbral común, sala de encuentro ampliada y continuidad casi imperceptible entre dos casas, como una comuna de ocho. El criterio de comparación es capacidad, privacidad, cocina, servicios, simultaneidad, superficie añadida y calidad del recorrido; no solo intensidad de la forma.

Códigos recientes:

- **V01_U:** unidad de cuatro con común continuo.
- **V02_U:** unidad de cuatro con dos ámbitos desplazados y conectados.
- **V03_U:** unidad de cuatro con organización de cruce; servicios trasladados del centro al borde en revisiones posteriores.
- **V02_P:** pareja de ocho con dos ámbitos y umbral.
- **V01_D / V03_D:** unión con encuentro más reconocible/ampliado.
- **V01_S / V03_S:** unión de continuidad común, sin mantener el límite doméstico anterior como frontera interior.
- **E01_ENCUENTRO:** ensayo de agrupación sobre parcela.
- **E02_COMUNA:** ensayo de ocho personas sobre pilares, elegido por Adam para documentar junto a las tres unidades de cuatro.
- **E03_DOS_CLAROS:** ensayo sobre parcela con dos ámbitos relacionados.

La megaestructura aporta mecanismos: soporte separado de suelo y piel; ramas que recogen bandejas; enlaces que se ensanchan como estancias; diversidad de cotas y vistas; habitación íntima dentro de infraestructura colectiva; telas de sombra, protección y expresión; posibilidad de mantenimiento.

No se heredan automáticamente depósitos suspendidos, órganos técnicos inventados, tubos por ventanas ni una estructura solo porque tenga aspecto de árbol. Cada elemento debe justificar carga, recorrido, uso y acceso para reparación.

Los soportes nuevos no están validados por el cálculo de V4. El conjunto completo de cuarenta personas todavía necesita una sección y agregación propias. Los tres E0x no son tres torres terminadas.

### 9. Parcela, luz y forma futura

Adam quiere viviendas que busquen la calle y diferentes orientaciones, no un conjunto longitudinal impuesto mirando siempre al edificio vecino. La luz se estudia sobre **la parcela y el contexto reales**, no sobre un complejo anterior tratado como dato inmutable.

Hay que separar: sol directo, cielo visible, iluminación interior, ventilación, privacidad y sobrecalentamiento. Una banda exterior libre de 3 m o una vista sin cubierta no resuelven esos cinco asuntos.

La idea futura de Adam es que la forma parezca un diagrama de entrada del sol: recortar, girar, desplazar y abrir vacíos; arranque más esbelto y expansión superior como hipótesis de árbol. Se guardó para más adelante, priorizando la unidad. Galápagos u otros optimizadores son posibilidades planteadas, no herramientas ya ejecutadas con un óptimo demostrado.

En el archivo local utilizado, el frente a calle entre (13,28; −7,50) y (12,07; 7,43) mide **14,97895 m**, aproximadamente 14,98 m. La extensión del polígono en ejes de archivo es aproximadamente **49,48 × 20,17 m**; esa última cifra no es el ancho del frente. La superficie catastral local ronda **650,91 m²**. Hay pequeñas diferencias según contorno nativo o polígono fuente; no deben ocultarse bajo una falsa precisión de levantamiento.

La corrección reciente ha añadido la cota del frente real a los PDF. El Rhino de layouts fue generado antes de esa última corrección de acotación: hay que sincronizarlo. La coincidencia de un lado con 15 m no valida todos los límites, escala urbana o encaje del edificio.

### 10. Planta baja pública: ampliación más reciente

Adam pidió más densidad de actividades y cosas públicas sobre la parcela, con coworking, biblioteca, sala de estudio que los domingos recibe trabajos y exposiciones vecinales, fuente y lugares para sentarse. El programa añadido es una propuesta propia, no una lista copiada de Ruralex.

En la copia técnica de E02 se ha incorporado:

| Programa | Geometría/capacidad de estudio registrada | Funcionamiento propuesto |
|---|---|---|
| Biblioteca | 53,05 m² de huella y cuatro asientos de lectura | Consulta, intercambio de libros y trabajo tranquilo. |
| Sala de estudio/exposición | 67,09 m² de huella, cuatro mesas y ocho sillas | Estudio cotidiano; mesas plegadas y paneles móviles el domingo. |
| Coworking abierto | Cuatro puestos | Trabajo bajo el ámbito elevado, sin otra caja cerrada. |
| Cocina y comedor comunes | Comedor de ocho en el ensayo | Comida, encuentros y apoyo a actividades. |
| Reparación y costura | Bancos de trabajo y herramientas | Coser, arreglar, mantener recursos compartidos. |
| Punto vecinal | Mesa de atención/encuentro | Apoyo, intercambio y organización. |
| Intercambio y almacenaje | Armarios y reserva para paneles/mesas | Recoger lo móvil sin ocupar pasos. |
| Fuente | Lámina de agua, borde y tres bancos curvos discontinuos | Encuentro y estancia exterior. |
| Plaza abierta | Uso flexible | Actividades temporales y extensión de muestras. |
| Servicios y núcleo | Borde de servicios, escalera y ascensor | Apoyo al uso común y acceso superior. |

Biblioteca y sala de estudio llevan huecos y lucernarios propuestos. No se han supuesto ventanas practicables sobre cualquier medianera. La cubierta pública es una geometría de anteproyecto; su luz, estructura, impermeabilización y mantenimiento están por desarrollar.

Se dibujan dos estados con la misma envolvente: **diario** y **domingo**. En 3D las capas `26_ESTUDIO_DIARIO` y `27_EXPOSICION_DOMINGO` son alternativas; no hay que encender ambas y presentar mesas/paneles solapados como un estado simultáneo.

La auditoría registrada comprueba un recorrido principal nominal de 1,50 m y una rama de biblioteca de 1,30 m contra la geometría de perfiles/secciones disponible, considerando altura libre de 2,20 m; no registra colisiones en los dos estados. Su alcance es limitado: no certifica todos los movimientos interiores, accesibilidad reglamentaria, aforo o evacuación.

La fuente tiene una reserva de acometida bajo pavimento; no consta cálculo hidráulico. No se debe sumar esta ampliación al edificio sin revisar el presupuesto global de superficie, construcción y mantenimiento.

### 11. Planos técnicos: qué existe y qué falta corregir

La carpeta `G3_PLANOS_TECNICOS_2026-10-20` contiene instantáneas del usuario, revisiones 3D, geometría extraída mediante RhinoCommon, escenas vectoriales, PDF, SVG y un Rhino 2D con layouts.

Criterios usados:

- Escala física 1:100: un metro de modelo equivale a 10 mm de papel.
- Tres unidades en A3 horizontal y agrupación/parcela en A2 horizontal.
- Ibarra Real Nova; el PDF utiliza la variante itálica disponible.
- Muros y piezas cortadas en negro; carpintería y equipamiento en línea fina; elementos sobre el corte discontinuos.
- Cotas calculadas desde coordenadas extraídas; ejes X/Y de referencia, no falsos ejes estructurales.
- Simetría local de las bow donde corresponde; no se acredita simetría global de las tres unidades.
- Ventanas dibujadas como carpinterías arquitectónicas, no manchas de render.
- Sofás retirados; mobiliario privado conservado.
- Patinillos y montantes concentrados en servicios, retirando conducciones de huecos de fachada.

Se generaron seis láminas: V01, V02, V03, E02 elevado, planta baja diaria y planta baja dominical. Los PDF son vectoriales derivados de la geometría; no son renders ni imágenes generativas. El archivo 2D de Rhino contiene seis layouts bloqueados a 1:100 según el informe guardado.

**Cuidado con los estados de archivo:** quedan un P05 antiguo de planta baja, informes de errores de intentos previos y vistas anteriores. La revisión no está empaquetada ni cerrada como entrega final. Los informes de éxito posteriores no convierten todos los archivos de la carpeta en vigentes. La última cota de frente de calle debe propagarse al Rhino de layouts.

#### Medidas leídas en el informe técnico actual

Estas cifras describen el modelo existente antes de la compactación pedida; no son objetivos aprobados ni superficies útiles normativas. La caja envolvente en XY mide extremos, no la superficie de un rectángulo realmente construido.

| Caso | Pavimento geométrico | Extensión exterior en ejes del archivo | Estado |
|---|---:|---|---|
| V01_U | 122.66 m² | 12,97 × 13,53 m | Pendiente de revisión dimensional/encaje. |
| V02_U | 126.22 m² | 13,12 × 15,33 m | Pendiente de revisión dimensional/encaje. |
| V03_U | 117.52 m² | 17,23 × 17,23 m | Pendiente de revisión dimensional/encaje. |
| E02 | 251.36 m² | 39,30 × 14,81 m | Pendiente de revisión dimensional/encaje. |

La queja de Adam sobre unos 17 m en V02 se conserva como señal del problema. El informe consultado registra aproximadamente 15,33 m en V02 y 17,23 m en V03; puede haber versiones o cotas distintas visibles. No procede corregir esa discrepancia inventando una nueva medida: hay que revisar el archivo y la cota concreta. V03 tiene menos área pero mayor extensión: forma, área y encaje no son intercambiables.

La corrección pendiente debe redistribuir espacios y comprobar el encaje a escala real. **No reducir globalmente camas, mesas, puertas, personas o espesores para hacer que quepa una silueta.** Tampoco convertir la medida de fachada en una cota de toda la parcela.

### 12. Decisiones vigentes y asuntos abiertos

#### Decisiones que hay que conservar

- Radicalidad constante, con razones de uso y construcción.
- Complejo como red de relaciones; no apilamiento repetido sin vida común.
- Habitaciones personales y derecho a intimidad.
- Vestidor transitable cóncavo y pequeña bow con asiento integrado.
- Tablero de dibujo grande articulado por canto corto, sin patas fijas.
- Acceso fluido y puertas que no choquen con cama/armario.
- Baños integrados en borde, sin isla sanitaria central ni caja frente a escalera.
- Telas con función climática y espacial, no cortinas arbitrarias cortando el paso.
- Planta baja ligada al conjunto y al barrio.
- Diferencias entre V01/V02/V03; no nueva homogeneización cosmética.
- Documentación técnica métrica para planos; dibujo expresivo separado como relato del proceso.
- Originales y PERSONAS.3dm preservados: las figuras se importan al modelo arquitectónico, no se construye dentro del archivo de personas.

#### Decisiones rechazadas o sustituidas

- Copiar literalmente el muro/plataforma colgante del profesor.
- Copiar la silueta de Ruralex o llamarla resultado de atractores.
- Pentágono arbitrario o cuatro retiros precolocados como pretendido análisis neutral.
- Series enormes sin relación demostrable con cómo se vive.
- Cubiertas y objetos flotando en la vista de una unidad construida.
- Bicicleta/tendedero colocados permanentemente en medio de la casa.
- Habitaciones sin frente exterior o ventanas tapadas por otras paredes.
- Puertas en curvas mal resueltas y camas interceptando la entrada.
- Plataforma de cama sobredimensionada.
- Ventana «habitable» representada solo por un panel.
- Panel expositivo independiente mal integrado en dormitorios.
- Baños insulares dentro de la convivencia.
- Sofá como relleno del acceso.
- Presentar cuarenta alternativas semejantes como cuarenta hipótesis plenamente distintas.
- Presentar cálculos de una versión como prueba de otra.

#### Orden lógico para continuar en el trabajo principal

1. Verificar parcela, frente a calle, contexto y dimensiones del modelo realmente abierto.
2. Revisar área y extensión de las tres unidades; acordar un presupuesto espacial defendible para cuatro personas y cuarenta en total.
3. Compactar relaciones y superficie común sin perder prestaciones privadas ni reducir artificialmente mobiliario.
4. Comprobar entrada, pasos, giro, vestidor, mesa en uso/plegada y bow mediante planta y sección.
5. Revisar baños y cocina con equipamiento real y filtros de privacidad.
6. Probar agregación de dos unidades con luz y entradas, no solo contacto de perímetros.
7. Contrastar la planta baja ampliada con el nuevo presupuesto de superficie y con la estructura superior.
8. Estudiar iluminación con vecinos y otras unidades, sol de invierno/verano y condiciones interiores.
9. Resolver soporte, uniones, cimentación, membranas, drenaje y mantenimiento para la geometría elegida.
10. Comprobar normativa, evacuación, accesibilidad, instalaciones, acústica y energía para esa versión concreta.
11. Sincronizar 3D, planos, cotas, layouts y documento de proceso.
12. Seleccionar qué ensayos cuentan el argumento de la entrega y cuáles quedan como archivo crítico.

Esta lista registra el punto de continuidad; no significa que esas operaciones se hayan ejecutado desde esta conversación lateral. Para redactar esta memoria se han leído archivos y se ha creado únicamente este Markdown, sin modificar los Rhino.

### 13. Guía rápida: qué Rhino abrir y para qué

Las rutas son absolutas y están enlazadas. Si el lector Markdown no abre directamente un `.3dm`, copiar la ruta y usar **Archivo → Abrir** en Rhino, o **Ir → Ir a la carpeta** en Finder. Los nombres «FINAL», «CORREGIDA» o «CALCULADA» pertenecen a sus versiones y no significan aprobación actual del proyecto.

#### Referencia original de la megaestructura

[MEGAESTRUCTURA_MACARRA.3dm](</Volumes/T7/G3 Proyectos/G3 CODEX/90_FUENTES_EXTERNAS_APORTADAS/MEGAESTRUCTURA_MACARRA/modelo/MEGAESTRUCTURA_MACARRA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CODEX/90_FUENTES_EXTERNAS_APORTADAS/MEGAESTRUCTURA_MACARRA/modelo/MEGAESTRUCTURA_MACARRA.3dm`.
- **Qué contiene:** Referencia macarra original: red, soporte, conexiones y piel. Antecedente fantástico; no estructura certificada.
- **Localización al redactar:** archivo presente.

#### Unidad suspendida de partida

[G3_unidad_suspendida_7.3dm recuperado](<90_FUENTES_EXTERNAS_APORTADAS/G3_unidad_suspendida_7.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CODEX/90_FUENTES_EXTERNAS_APORTADAS/G3_unidad_suspendida_7.3dm`.
- **Qué contiene:** Modelo aportado al inicio de la conversación; variantes de unidad suspendida. Antecedente, no unidad actual V02.
- **Localización al redactar:** ruta histórica aportada; archivo no localizado ahora.

#### Personas

[PERSONAS.3dm](</Volumes/T7/G3 Proyectos/G3 CODEX/90_FUENTES_EXTERNAS_APORTADAS/PERSONAS.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CODEX/90_FUENTES_EXTERNAS_APORTADAS/PERSONAS.3dm`.
- **Qué contiene:** Biblioteca de figuras. Tomar personas para los modelos de arquitectura; no modelar el edificio dentro de este archivo.
- **Localización al redactar:** archivo presente.

#### Unidad suspendida histórica

[G3_unidad_suspendida.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_UNIDAD/G3_unidad_suspendida.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_UNIDAD/G3_unidad_suspendida.3dm`.
- **Qué contiene:** Etapa de caracol, vidrio, altillo y variantes; incluye el desarrollo histórico F2 según sus memorias.
- **Localización al redactar:** archivo presente.

#### Conjuntos históricos

[G3_conjunto_opciones.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_CONJUNTO/G3_conjunto_opciones.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_CONJUNTO/G3_conjunto_opciones.3dm`.
- **Qué contiene:** Alternativas tempranas de agregación. Conservación como antecedente.
- **Localización al redactar:** archivo presente.

#### Megaestructura libre

[MEGA_A_LIBRE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/MEGAESTRUCTURA_CLAUDE/MEGA_A_LIBRE.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/MEGAESTRUCTURA_CLAUDE/MEGA_A_LIBRE.3dm`.
- **Qué contiene:** Ensayo histórico libre de megaestructura; no confundir con la referencia original de Downloads.
- **Localización al redactar:** archivo presente.

#### Megaestructura en Ribera

[MEGA_B_RIBERA31_1a1.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/MEGAESTRUCTURA_CLAUDE/MEGA_B_RIBERA31_1a1.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/MEGAESTRUCTURA_CLAUDE/MEGA_B_RIBERA31_1a1.3dm`.
- **Qué contiene:** Ensayo histórico de implantación a escala de archivo; requiere contraste con la parcela y decisiones posteriores.
- **Localización al redactar:** archivo presente.

#### V4 conjunto en parcela

[SELVA_MACARRA_V4_EN_PARCELA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/SELVA_MACARRA_V4_EN_PARCELA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/SELVA_MACARRA_V4_EN_PARCELA.3dm`.
- **Qué contiene:** Diez pabellones/cuarenta residentes, soportes ramificados, contexto, escaleras y ascensores. Antecedente; la distribución posterior ha cambiado.
- **Localización al redactar:** archivo presente.

#### V4 unidad independiente

[UNIDAD_GRAN_BOVEDA_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/UNIDAD_GRAN_BOVEDA_EDITABLE.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/UNIDAD_GRAN_BOVEDA_EDITABLE.3dm`.
- **Qué contiene:** Pabellón aislado de cuatro habitaciones para inspección; antecedente anterior a las nuevas unidades.
- **Localización al redactar:** archivo presente.

#### P02 detallada

[UNIDAD_P02_DETALLADA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/modelos/UNIDAD_P02_DETALLADA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/modelos/UNIDAD_P02_DETALLADA.3dm`.
- **Qué contiene:** Unidad P02 aislada y detallada de la etapa V4. Sirve para seguir las críticas de mobiliario, no para sustituir V01/V02/V03.
- **Localización al redactar:** archivo presente.

#### P02 interior

[UNIDAD_P02_INTERIOR_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/modelos/UNIDAD_P02_INTERIOR_EDITABLE.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/modelos/UNIDAD_P02_INTERIOR_EDITABLE.3dm`.
- **Qué contiene:** Interior accesible de la P02 histórica para estudiar habitación y equipamiento.
- **Localización al redactar:** archivo presente.

#### Ensayo de habitación curva

[HABITACION_CURVA_ENSAYO_A.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_HABITACION_CURVA_2026-10-18/HABITACION_CURVA_ENSAYO_A.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_HABITACION_CURVA_2026-10-18/HABITACION_CURVA_ENSAYO_A.3dm`.
- **Qué contiene:** Prueba de habitación y geometrías curvas; antecedente de cama, armario y mesa.
- **Localización al redactar:** archivo presente.

#### Primer catálogo 3D de cuarenta

[CATALOGO_40_UNIDADES_COTA0.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/CATALOGO_40_UNIDADES_COTA0.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/CATALOGO_40_UNIDADES_COTA0.3dm`.
- **Qué contiene:** Cuarenta modelos separados a cota cero. Versión con los fallos posteriormente criticados; archivo de proceso.
- **Localización al redactar:** archivo presente.

#### Catálogo de cuarenta corregidas

[CATALOGO_40_CORREGIDAS_COTA0.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/CATALOGO_40_CORREGIDAS_COTA0.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/CATALOGO_40_CORREGIDAS_COTA0.3dm`.
- **Qué contiene:** Cuarenta unidades compactadas/corregidas, separadas en XY. La homogeneización y las prestaciones perdidas impiden tratarlas como selección definitiva.
- **Localización al redactar:** archivo presente.

#### Habitación del catálogo corregido

[HABITACION_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/HABITACION_CORREGIDA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/HABITACION_CORREGIDA.3dm`.
- **Qué contiene:** Prototipo privado de esa corrección: útil para comparar con el vestidor y la bow recuperados después.
- **Localización al redactar:** archivo presente.

#### Todas las nuevas organizaciones en 3D

[TODAS_LAS_PLANTAS_3D_COTA0.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/TODAS_LAS_PLANTAS_3D_COTA0.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/TODAS_LAS_PLANTAS_3D_COTA0.3dm`.
- **Qué contiene:** Ocho organizaciones nuevas: unidades de cuatro y agrupaciones de ocho. Separadas a cota cero; no edificio apilado.
- **Localización al redactar:** archivo presente.

#### V01 individual

[V01_U_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V01_U_3D.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V01_U_3D.3dm`.
- **Qué contiene:** Cuatro residentes, organización continua, habitación con vestidor y bow; anterior a revisión técnica del 20.
- **Localización al redactar:** archivo presente.

#### V02 individual

[V02_U_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V02_U_3D.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V02_U_3D.3dm`.
- **Qué contiene:** Cuatro residentes, dos ámbitos desplazados. Es la V02 aclarada por Adam; pendiente de revisar tamaño.
- **Localización al redactar:** archivo presente.

#### V03 individual

[V03_U_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V03_U_3D.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V03_U_3D.3dm`.
- **Qué contiene:** Cuatro residentes, organización de cruce, servicios al borde en esta etapa; extensión actual requiere revisión.
- **Localización al redactar:** archivo presente.

#### V02 pareja

[V02_P_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V02_P_3D.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V02_P_3D.3dm`.
- **Qué contiene:** Pareja de ocho con dos ámbitos y umbral; no es la unidad V02_U.
- **Localización al redactar:** archivo presente.

#### E01 sobre parcela

[E01_ENCUENTRO_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E01_ENCUENTRO_INTERIOR.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E01_ENCUENTRO_INTERIOR.3dm`.
- **Qué contiene:** Agrupación de ocho, encuentro ampliado, apoyos, planta baja y núcleo; copia preparada para ver interior.
- **Localización al redactar:** archivo presente.

#### E02 sobre parcela

[E02_COMUNA_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E02_COMUNA_INTERIOR.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E02_COMUNA_INTERIOR.3dm`.
- **Qué contiene:** Casa común de ocho sobre apoyos con planta baja, escalera y ascensor. Base elegida para documentación.
- **Localización al redactar:** archivo presente.

#### E02 revisión nativa anterior

[E02_REVISION_NATIVA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/verificacion/E02_REVISION_NATIVA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/verificacion/E02_REVISION_NATIVA.3dm`.
- **Qué contiene:** Copia nativa de verificación usada en la selección del usuario. Puede no contener cambios posteriores de programa público.
- **Localización al redactar:** archivo presente.

#### E03 sobre parcela

[E03_DOS_CLAROS_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E03_DOS_CLAROS_INTERIOR.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E03_DOS_CLAROS_INTERIOR.3dm`.
- **Qué contiene:** Ensayo de ocho con dos ámbitos relacionados, soportes y programa común inferior.
- **Localización al redactar:** archivo presente.

#### Tres unidades con cubiertas

[UNIDADES_4_PERSONAS_TODAS_CON_CUBIERTA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_UNIDADES_4_PERSONAS_2026-10-20/UNIDADES_4_PERSONAS_TODAS_CON_CUBIERTA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_UNIDADES_4_PERSONAS_2026-10-20/UNIDADES_4_PERSONAS_TODAS_CON_CUBIERTA.3dm`.
- **Qué contiene:** V01, V02 y V03, cuatro residentes cada una, separadas y a Z=0, con cubiertas. Documento trabajado por Adam; no incluye solar ni parejas.
- **Localización al redactar:** archivo presente.

#### Tres unidades revisadas técnicamente

[TRES_UNIDADES_REVISION_TECNICA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/TRES_UNIDADES_REVISION_TECNICA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/TRES_UNIDADES_REVISION_TECNICA.3dm`.
- **Qué contiene:** Copia con revisión de perímetro de baños, puertas, sofás retirados y montantes en servicios. NO compactada todavía tras la última queja dimensional.
- **Localización al redactar:** archivo presente.

#### E02 con programa público ampliado

[E02_REVISION_TECNICA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/E02_REVISION_TECNICA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/E02_REVISION_TECNICA.3dm`.
- **Qué contiene:** Ocho residentes elevados más biblioteca, estudio/exposición, coworking, fuente y programa público de PB. Dos estados en capas alternativas; anteproyecto.
- **Localización al redactar:** archivo presente.

#### Planos y layouts editables

[PLANOS_EDITABLES_Y_LAYOUTS_1_100.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/PLANOS_EDITABLES_Y_LAYOUTS_1_100.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/PLANOS_EDITABLES_Y_LAYOUTS_1_100.3dm`.
- **Qué contiene:** Dibujo 2D en metros con seis layouts 1:100, tramas, líneas y textos. No modelo 3D. Pendiente de sincronizar última cota de frente y futura compactación.
- **Localización al redactar:** archivo presente.

#### Estado del usuario: tres unidades

[TRES_UNIDADES_ESTADO_USUARIO.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/instantaneas/TRES_UNIDADES_ESTADO_USUARIO.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/instantaneas/TRES_UNIDADES_ESTADO_USUARIO.3dm`.
- **Qué contiene:** Instantánea conservada antes de revisión; incluye trabajo/curvas del usuario. No es la copia técnica limpia.
- **Localización al redactar:** archivo presente.

#### Estado del usuario: E02

[E02_ESTADO_USUARIO.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/instantaneas/E02_ESTADO_USUARIO.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/instantaneas/E02_ESTADO_USUARIO.3dm`.
- **Qué contiene:** Instantánea del documento abierto, anterior a actualización de PB y programa público. Respaldo, no versión recomendada de distribución.
- **Localización al redactar:** archivo presente.


#### Convenciones para interpretar los archivos

- `U`: unidad de cuatro en estas familias; `P`: pareja; `D`: encuentro ampliado; `S`: continuidad compartida. Son convenciones de estas series, no de todo archivo del proyecto.
- `_INTERIOR`: copia/configuración para leer el interior, no necesariamente una arquitectura distinta.
- `_PLANTA_2D` y `modelos_2d`: curvas/base de planta, no un edificio 3D constructivo.
- `_PREVIA_SOLIDA` o `MALLAS`: copia de visualización; no sustituye automáticamente a geometría editable de origen.
- `fuentes/personas_seleccionadas`: figuras auxiliares importadas, no viviendas.
- `ENTREGA` y carpetas anidadas pueden contener copias empaquetadas; no contarlas como proyectos diferentes.
- `verificacion` puede contener copias diagnósticas; no asumir que su fecha o nombre las convierte en el modelo vigente.

### 14. Documentos y fuentes para retomar el hilo

- [Investigación urbana](</Volumes/T7/G3 Proyectos/G3 CODEX/01_INVESTIGACION_PARCELA_Y_REFERENCIAS/INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/LEEME.md>).
- [Unidad antigua v5](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_UNIDAD/G3_unidad_v5_memoria.md>).
- [Acampada y traducciones](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SOL_SELVA_2026-10-11/CUADERNO_SOL_SELVA.md>).
- [Predimensionado histórico V4](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/MEMORIA_TECNICA_Y_RAZON_DE_LA_FORMA.md>).
- [Luz y planta baja de V4](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16/DOSSIER_EDITABLE.md>).
- [Lectura de Ruralex y cocina](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_REFERENCIAS_RURALEX_COCINA_2026-10-18/LECTURA_Y_CAMBIO_DE_CRITERIO.md>).
- [Acciones](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDO_REGLAS_Y_ALTERNATIVAS_2026-10-18/ACCIONES_PARA_DISCUTIR.md>).
- [Segunda serie desde tejidos](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/LEEME.md>).
- [Corrección de cuarenta](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/LEER_PRIMERO.md>).
- [Diagnóstico de homogeneización](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_DECIDIR_UNIDAD_PARCELA_2026-10-19/EMPEZAR_AQUI.md>).
- [Nuevas formas de vivir](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_PLANTAS_FORMAS_DE_VIVIR_2026-10-19/LEER_PRIMERO.md>).
- [Uniones comunas](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_UNIONES_COMUNAS_2026-10-19/ANALISIS_Y_LECTURA.md>).
- [Reglas contra baños centrales](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS_2026-10-19/REGLAS_DE_PROYECTO.md>).
- [Encaje y continuidad](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/LEEME.md>).
- [Herencia macarra y PB](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/HERENCIA_Y_PLANTA_BAJA.md>).
- [Tres unidades con cubierta](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_UNIDADES_4_PERSONAS_2026-10-20/LEEME.md>).
- [Dibujos de acciones: límites](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_ACCIONES_DIBUJADAS_2026-10-20/CRITERIO_CORREGIDO.md>).
- [Medidas técnicas actuales](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/verificacion/ESCALAS_Y_MEDIDAS.json>).
- [Programa público nuevo](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/verificacion/PROGRAMA_PUBLICO_PB.json>).
- [Layouts 1:100](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/verificacion/LAYOUTS_RHINO.json>).
- [Recorridos públicos: alcance](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/verificacion/AUDITORIA_RECORRIDOS_PB.json>).

El índice antiguo de la raíz menciona una bóveda de Obsidian en `/Volumes/T7/obsidian/creATIveb@bY/CEREBRO DE PROYECTOS/`. Este documento no afirma que toda esa bóveda esté sincronizada. No se ha reorganizado ni modificado Obsidian para esta petición.

