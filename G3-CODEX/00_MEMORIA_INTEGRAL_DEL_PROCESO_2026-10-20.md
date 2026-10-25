# G3 · Memoria integral del proceso y guía de archivos Rhino

**Fecha de corte: 20 de octubre de 2026.**
**Proyecto: vivienda colectiva en Ribera de Curtidores 31, El Rastro, Madrid.**
**Autoría de las decisiones e intenciones: Adam. Desarrollo y asistencia: conversaciones y archivos del proyecto.**

Este documento reúne el proceso desde su arranque documentado hasta el punto actual: investigación urbana, acampada, megaestructura, unidad doméstica, acciones, tejidos, catálogos, correcciones, agrupaciones, planta baja y planos técnicos. Incluye las decisiones rechazadas y los problemas que siguen abiertos, porque también explican cómo hemos llegado aquí.

Es una memoria consolidada, no una transcripción literal de todas las conversaciones. Se apoya en el historial disponible, las memorias del proyecto y los archivos localizados en disco. La existencia de un archivo no demuestra que su arquitectura esté resuelta. Las fechas de las carpetas identifican entregas, no necesariamente el día exacto de cada conversación. Las cifras históricas se atribuyen a su versión y no se trasladan automáticamente a otra.

> **Estado actual decisivo:** Adam ha cuestionado el tamaño de las unidades, especialmente V02, y ha pedido revisar también las demás. Esa revisión dimensional y de encaje está pendiente. Los planos técnicos existentes registran geometría previa; no deben presentarse como si ya incorporasen una compactación resuelta.

## Índice

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

## 1. Punto de partida y encargo

El proyecto busca una vivienda colectiva para jóvenes con una posición crítica frente a la dificultad de acceder a la vivienda, el aislamiento doméstico y la privatización de recursos. La acampada funciona como referencia de organización y cooperación, no como una imagen que copiar literalmente ni como estándar técnico de vivienda permanente.

La dirección expresada por Adam es una arquitectura **macarra, radical, entrelazada, con telas, cruces, conexiones y recorridos que se convierten en lugares**. La radicalidad debe sostenerse con distribución, medidas, estructura, detalles, mantenimiento y funcionamiento cotidiano. No basta una forma espectacular ni una planta convencional con curvas añadidas.

La escala de trabajo se ha formulado como habitación personal → unidad de cuatro → convivencia de ocho → comunidad de unas cuarenta personas → barrio. Cuatro personas por unidad es una hipótesis comparable que se ha utilizado durante el desarrollo, no una ley que justifique cualquier superficie. También se trabajó con un objetivo provisional de unos 1.500 m²; debe comprobarse con el enunciado y un cómputo completo. Los antecedentes de 32 unidades pertenecen a una etapa anterior y no equivalen a las diez viviendas de cuatro de ensayos posteriores.

El usuario prefiere llamar al edificio **complejo**. El nombre «selva habitada» fue rechazado; aparece aquí solo porque permanece en nombres históricos de carpetas y archivos.

## 2. Investigación de parcela y barrio: el arranque documentado

En septiembre se reunió investigación de Ribera de Curtidores 31 y El Rastro: contexto urbano, actividades, frentes, patrones materiales, comercio, temporalidad del mercado, relación público/privado, fotos propias, cartografía y referencia catastral.

La carpeta de investigación documenta un compendio de 43 páginas, un recorrido de Street View con 23 panorámicas y 11 registros históricos del número 31, un censo de 42 frentes, originales GML catastrales y derivados GeoJSON en EPSG:25830. Son recuentos documentados en su LEEME, no una nueva auditoría independiente de cada fuente. Existen archivos QGIS, CSV, figuras, alzados y datos de sombras/sol por altura.

La investigación distingue tres niveles útiles: **A, medido; B, inferido por modelo o lectura visual; C, hipótesis**. No se debe dibujar una hipótesis formal como si fuese un dato observado.

El megapanel de cinco A3 y sus versiones PDF/PNG/PSD sintetizan esa base. La maqueta del entorno y las exploraciones sobre mecanismos pertenecen también al proceso de relación entre lugar y proyecto. No sustituyen el levantamiento de la parcela ni una ordenación urbanística comprobada.

Rutas principales:

- `INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/`: compendio, datos, figuras y scripts.
- `INVESTIGACIÓN/01_ENCARGO_Y_TEXTO_BASE/`: protocolo y texto de partida.
- `INVESTIGACIÓN/PANEL_FINAL_5xA3/`: síntesis gráfica urbana.
- `MAPPEADOS/`: mapas propios y modelo del entorno.

## 3. Acampada: qué se investigó y qué se tradujo

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

## 4. Recorrido cronológico: de la célula al problema actual

### 4.1. Primeras células suspendidas y agrupaciones, primeros días de octubre

Se estudiaron la unidad suspendida, sus variantes, el caracol, altillo, aperturas, bloque de vidrio, acero grafito y piezas curvas. La variante F2 —esquina curva y ala semicircular— fue un antecedente apreciado. Se compararon alternativas de escalera y ventana, mesas de trabajo/comida y baño curvo.

La revisión del 8 de octubre reconstruyó unidades y conjuntos y propuso alternativas de dúplex y una planta. Detectó que conectar objetos mediante plataformas no bastaba para construir convivencia. Aquel conjunto seguía demasiado lineal y con exceso de superficie; es un antecedente parcial, no el proyecto final.

### 4.2. Megaestructura macarra y rechazo de una única verticalidad

Adam pidió mantener el zigzag, las ramificaciones, los claros y una complejidad casi laberíntica. Las fotos y dibujos del profesor —gran muro lateral, plataforma superior y piezas colgadas— se aportaron como estímulo, pero Adam rechazó convertirlos en la solución literal: no quería concentrar toda la organización en un solo lateral vertical.

La pregunta pasó a ser cómo escalar mecanismos y proporciones a vivienda colectiva, conservando solo lo que mantiene función. Colgar, apoyar, enlazar, cubrir y recorrer debían adquirir una razón material y espacial.

### 4.3. V2, V3 y V4, 11–16 de octubre

Se produjeron cuadernos, imágenes y modelos del complejo; las versiones iniciales fueron criticadas por alejarse de la megaestructura de referencia. Adam pidió orden, cálculo y detalles que sostuvieran la radicalidad.

La V4 ensayó diez pabellones para cuarenta residentes sobre tres grupos de soportes ramificados, con ascensores y escaleras. Su documentación contiene un modelo elástico lineal preliminar de barras y comprobaciones de subsistemas, además de detalles de nudo, bandeja/envolvente y ascensor. «Calculada» en el nombre no significa estructura certificada. Sus comprobaciones no validan los modelos posteriores, que cambiaron geometría, cargas y distribución.

La V4 fue un antecedente formal útil, pero sus habitaciones eran demasiado pequeñas en esa etapa. Se pidió situar el conjunto con contexto y extraer una unidad P02 para verla de cerca.

### 4.4. P02: el cuerpo y el mobiliario desmienten la imagen, 16–18 de octubre

Al acercarse aparecieron camas mal encajadas, muebles junto a puertas, tamaños incoherentes, piezas flotando y problemas de lectura. Adam pidió corregir la habitación antes de seguir repitiendo unidades y situar el modelo a cota cero.

Se exploraron camas redondas, colchón sin pedestal mayor, armarios cóncavos, mesas de dibujo plegables, taburetes, dos pequeños slabs metálicos junto a la cama con carga del móvil, almacenamiento integrado y ventanas habitables. Algunas ideas siguen como antecedentes y no están desarrolladas técnicamente en todas las versiones.

Se hicieron distintas plantas y secciones. Adam rechazó soluciones que bloqueaban el acceso, el armario o la mesa. Pidió simetría y equivalencia entre habitaciones en una fase, y después cuestionó que eso condujera a una planta rígida con pasillo central.

Los modelos con piezas flotando se corrigieron buscando apoyos y niveles coherentes. No se considera resuelto un interior porque desde lejos parezca convincente.

### 4.5. Ruralex y cambio de método, 18 de octubre

Adam aportó Ruralex y una cocina de 3D Warehouse. Ruralex se estudió como relación entre programa, diagramas, estructura, instalaciones, envolvente y detalle. El registro local documenta lectura de su publicación visual; no se obtuvo un modelo nativo editable de Ruralex ni se verificaron todos sus cálculos.

No se ha demostrado que Ruralex naciera de un algoritmo de atractores. Ese método es una interpretación propia del proyecto G3. Tampoco se debe atribuir a Ruralex la biblioteca o el coworking que estamos inventando para nuestra parcela.

La cocina se inspeccionó mediante su ficha y vista pública; no consta una importación efectiva del modelo CAD descargado. Los muebles modelados son desarrollos propios/esquemáticos, no una copia nativa del archivo del enlace.

El cambio importante: dejar de decidir primero la silueta y empezar por **acciones, objetos, cuerpos, proximidades, conflictos, tiempos y recorridos**.

Referencias aportadas:

- [Ruralex, Ira XXX Dios](https://iraxxxdios.com/Ruralex).
- [Cocina, 3D Warehouse](https://3dwarehouse.sketchup.com/model/891b572f-78a3-418e-b9d5-cb61abbfe7fe/Cocina).

### 4.6. Tejido de cosas que pasan

Adam imaginó una hoja completa con retícula, puntos y relaciones que se cruzan; de ese tejido deberían surgir lugares. Rechazó un diagrama pentagonal sin fundamento y también colocar de antemano cuatro retiros en las esquinas, porque reproducía la planta anterior disfrazada de análisis.

Se discutió cómo justificar por qué una acción está junto a otra y por qué una distancia o una posición concreta. Las relaciones deben tener motivos —ruido, agua, intimidad, duración, traslado, luz— y no obedecer solo a composición gráfica.

No hay objetividad absoluta: pesos, umbrales y coordenadas son decisiones que hay que declarar y comparar. Un diagrama no demuestra por sí mismo una distribución correcta.

### 4.7. Veinte propuestas por dos variantes, y una segunda serie

Adam confirmó expresamente **20 propuestas × 2 variantes = 40 plantas**. Después pidió más ensayos, aparte de los ya hechos, derivados de las formas y relaciones de los diagramas, no de copiar Ruralex.

Se generaron varias series: atlas inicial, traducción del tejido a otras cuarenta plantas, documentación ampliada y bases Rhino 2D. No son una única colección inequívoca de cuarenta casos: existen series diferentes con códigos parecidos. Las publicaciones de hasta 88 páginas pertenecen a ese ciclo de exploración.

Las traducciones literales llegaron a unidades de unos 208–260 m², según la conversación y los ensayos, excesivas para la hipótesis de cuatro habitantes. La separación elástica de huellas y las conexiones gastaban demasiado suelo. Los documentos de la serie reconocen que cambiar deformaciones no equivale a inventar cuarenta organizaciones sociales independientes.

### 4.8. Modelar las cuarenta y corregirlas

Adam pidió modelar todas, sin apilar, con conexiones orgánicas y pavimento a Z=0. Se generó un catálogo 3D y archivos individuales.

La inspección cercana reveló fallos generalizados: soportes u objetos en medio, bicicleta y tendedero dentro de la vivienda sin razón, dormitorios interiores, ventanas hacia muros, accesos sobre curvas y espacios sobredimensionados. N01A, N01B y N04A fueron ejemplos; Adam aclaró que el problema afectaba al conjunto.

La corrección reconstruyó el catálogo alrededor de cuatro habitaciones con ventanas exteriores, accesos rectos, eliminación de objetos impropios y pruebas de pasos. Su documentación registra unas huellas interiores geométricas de 112,86–113,72 m² y dormitorios de 16,36 m² en esa versión. Se retiró la cama redonda y se utilizaron colchones rectangulares.

Pero se perdió el vestidor verdaderamente transitable y la ventana habitable profunda. Además, las cuarenta quedaron demasiado parecidas. Es un error de proceso reconocido: corregir no debía borrar la diversidad de cómo se vive.

### 4.9. Recuperar prestaciones y diversidad, 19 de octubre

Se produjeron V01, V02 y V03, recuperando vestidor y ventana. V01 ensayaba continuidad; V02, dos ámbitos desplazados y conectados; V03, una organización alrededor de un centro. V02 se consideró prometedora por permitir distintos ritmos de actividad, sin proclamarse elegida final.

La primera ventana profunda resultaba demasiado grande. Adam precisó que quería una **bow o bay pequeña, elegante y curva, en cuya concavidad se pueda sentar el cuerpo**. No un panel, un simple hueco ni un banco pegado a una ventana plana.

Se hicieron agrupaciones de ocho: umbral compartido, encuentro dramático y continuidad de comuna. Las pruebas V01/V03 no debían ser solo dos casas tocándose: había que reorganizar cocinas, mesas, accesos y apropiación del espacio común.

Adam rechazó los baños como isla central dentro del círculo habitable. Se rehízo un borde de servicios con llegada filtrada. El documento único debía incluir únicamente plantas nuevas corregidas y sus antecedentes diagramáticos, manteniendo sus diferencias, no el catálogo homogeneizado como propuesta vigente.

### 4.10. Del interior a soporte, planta baja y acceso real

Se modelaron las nuevas organizaciones y tres ensayos sobre parcela: E01_ENCUENTRO, E02_COMUNA y E03_DOS_CLAROS. Se añadieron bandejas, soportes ramificados, cubiertas y membranas, escalera, ascensor y galerías.

Adam pidió que la planta baja no fuera una vivienda triste aislada, sino parte de la vida común y del barrio. Rechazó una caja sin sentido delante de la escalera y cuestionó los aseos colocados abajo. La corrección llevó los servicios al borde y despejó la descarga de la escalera.

La cota +4,20 m de vivienda es un ensayo de sección, no un resultado de optimización solar ni una altura urbanística aprobada.

### 4.11. Tres unidades aisladas y dibujo propio, 20 de octubre

Adam pidió las tres unidades de cuatro personas juntas en un solo Rhino, con cubierta, para sacar sus planos. También pidió abrir el catálogo de cuarenta y después cuestionó su utilidad en la entrega por su semejanza. No se seleccionó automáticamente una de aquellas cuarenta como solución final.

Quería contar el proceso desde sus propios planos: acciones y vida cotidiana sobre formas reales, no dibujos genéricos. Se ensayó un lenguaje gráfico blanco y negro, rápido, sucio, superpuesto, con Ibarra. Las primeras imágenes sin geometría de referencia se descartaron. Los dibujos por IA son material narrativo, no documentación métrica.

### 4.12. Planos técnicos medidos y ampliación pública

La petición cambió expresamente a planos arquitectónicos calculados y medidos desde Rhino: tres unidades de cuatro y E02_COMUNA/E02_REVISION_NATIVA de ocho sobre pilares, con escala física, ventanas convencionales, ejes, cotas, grosores, negro en corte y discontinuas en proyección.

Se guardaron instantáneas del estado del usuario, se extrajo geometría nativa, se revisaron modelos en copias y se generaron PDF/SVG vectoriales y un Rhino de láminas editables. Se retiraron sofás, se trabajó el baño como perímetro continuo y se llevaron montantes al borde de servicios para evitar ventanas.

Después Adam pidió más programa público sobre la parcela: coworking, biblioteca, estudio/exposición dominical, fuente y asientos. Se incorporó una ampliación de planta baja a E02 y dos estados de uso. Al decir «también V02», aclaró que se refería a **V02 de cuatro personas**, que ya está incluida como plano individual; no equivale a E02_COMUNA.

El último giro es la revisión de tamaño: frente de parcela de unos 15 m y unidades que parecen demasiado extensas. No está resuelta todavía esa compactación.

## 5. Programa: acciones antes que habitaciones etiquetadas

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

## 6. La unidad: prestaciones que no deben desaparecer al compactar

### Habitación individual

Cada residente necesita un retiro propio. Equivalencia de prestaciones no exige que las cuatro esquinas se resuelvan por colocaciones arbitrariamente distintas ni que todo el edificio sea simétrico. La cama no debe quedar frente al hueco bloqueando la entrada. Puertas sobre tramos rectos y giros fluidos; acceso simultáneo a cama, ropa y trabajo.

La cama redonda se exploró, pero no es un requisito final obligatorio. El criterio es un colchón bien dimensionado, sin plataforma inferior de mayor huella que robe circulación. En los modelos recientes figura cama de 1,25 × 2,00 m.

### Mesa de dibujo

El tablero reciente mide 1,80 × 0,90 m. Debe poder plegarse/articularse por su **canto corto**, con soporte mural y bloqueo a distintos ángulos. No se representa como mesa fija con patas permanentes. Hay que revisar uso abierto, plegado, taburete y entrada al mismo tiempo. El herraje resistente y su anclaje todavía requieren cálculo y detalle.

El panel independiente para exponer proyectos en el dormitorio se eliminó por petición expresa. Eso no impide colgar referencias directamente en pared junto al trabajo. Los paneles móviles de una exposición pública en planta baja tienen otra función y fueron pedidos después.

### Vestidor cóncavo transitable

No basta un armario empotrado de 55 cm. El cuerpo entra en el nicho y sigue la curva; la ropa ocupa profundidad real alrededor. El espesor de almacenaje y el espacio de paso no se cuentan dos veces. Tiene que seguir siendo accesible con cama y mesa en uso.

### Bow/bay pequeña

La pared y la ventana forman un pequeño saliente curvo con concavidad interior y asiento adaptado. Debe verse en planta y sección dónde se sienta el cuerpo, cómo llega, dónde quedan piernas, vidrio, protección y tela. El retiro mirando fuera puede coexistir con vida colectiva: ofrecer intimidad no implica prohibir el encuentro.

### Baños

No pueden ser una isla central dentro del salón ni cajas sueltas dentro de otra caja. Deben integrarse en el contorno o borde de servicios, con acceso filtrado y sin puertas de WC expuestas directamente al estar. No se admite resolver una planta incorrecta añadiendo una pantalla que obstruya el paso.

### Estar, cocina y llegada

El espacio común no se reduce a cocina/comedor ni a un vacío sobrante. Debe permitir actividades diferentes y una llegada reconocible. El sofá no es obligatorio: se retiró de los planos técnicos recientes. No se coloca en la entrada para «llenar» un hueco.

Bicicleta, tendedero, taller y logística no deben convertirse en obstáculos permanentes domésticos. Parte de ese programa corresponde a la escala del edificio o de la planta baja.

## 7. Lo aprendido con los catálogos

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

## 8. Agregación: qué compartimos y qué heredamos

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

## 9. Parcela, luz y forma futura

Adam quiere viviendas que busquen la calle y diferentes orientaciones, no un conjunto longitudinal impuesto mirando siempre al edificio vecino. La luz se estudia sobre **la parcela y el contexto reales**, no sobre un complejo anterior tratado como dato inmutable.

Hay que separar: sol directo, cielo visible, iluminación interior, ventilación, privacidad y sobrecalentamiento. Una banda exterior libre de 3 m o una vista sin cubierta no resuelven esos cinco asuntos.

La idea futura de Adam es que la forma parezca un diagrama de entrada del sol: recortar, girar, desplazar y abrir vacíos; arranque más esbelto y expansión superior como hipótesis de árbol. Se guardó para más adelante, priorizando la unidad. Galápagos u otros optimizadores son posibilidades planteadas, no herramientas ya ejecutadas con un óptimo demostrado.

En el archivo local utilizado, el frente a calle entre (13,28; −7,50) y (12,07; 7,43) mide **14,97895 m**, aproximadamente 14,98 m. La extensión del polígono en ejes de archivo es aproximadamente **49,48 × 20,17 m**; esa última cifra no es el ancho del frente. La superficie catastral local ronda **650,91 m²**. Hay pequeñas diferencias según contorno nativo o polígono fuente; no deben ocultarse bajo una falsa precisión de levantamiento.

La corrección reciente ha añadido la cota del frente real a los PDF. El Rhino de layouts fue generado antes de esa última corrección de acotación: hay que sincronizarlo. La coincidencia de un lado con 15 m no valida todos los límites, escala urbana o encaje del edificio.

## 10. Planta baja pública: ampliación más reciente

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

## 11. Planos técnicos: qué existe y qué falta corregir

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

### Medidas leídas en el informe técnico actual

Estas cifras describen el modelo existente antes de la compactación pedida; no son objetivos aprobados ni superficies útiles normativas. La caja envolvente en XY mide extremos, no la superficie de un rectángulo realmente construido.

| Caso | Pavimento geométrico | Extensión exterior en ejes del archivo | Estado |
|---|---:|---|---|
| V01_U | 122.66 m² | 12,97 × 13,53 m | Pendiente de revisión dimensional/encaje. |
| V02_U | 126.22 m² | 13,12 × 15,33 m | Pendiente de revisión dimensional/encaje. |
| V03_U | 117.52 m² | 17,23 × 17,23 m | Pendiente de revisión dimensional/encaje. |
| E02 | 251.36 m² | 39,30 × 14,81 m | Pendiente de revisión dimensional/encaje. |

La queja de Adam sobre unos 17 m en V02 se conserva como señal del problema. El informe consultado registra aproximadamente 15,33 m en V02 y 17,23 m en V03; puede haber versiones o cotas distintas visibles. No procede corregir esa discrepancia inventando una nueva medida: hay que revisar el archivo y la cota concreta. V03 tiene menos área pero mayor extensión: forma, área y encaje no son intercambiables.

La corrección pendiente debe redistribuir espacios y comprobar el encaje a escala real. **No reducir globalmente camas, mesas, puertas, personas o espesores para hacer que quepa una silueta.** Tampoco convertir la medida de fachada en una cota de toda la parcela.

## 12. Decisiones vigentes y asuntos abiertos

### Decisiones que hay que conservar

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

### Decisiones rechazadas o sustituidas

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

### Orden lógico para continuar en el trabajo principal

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

## 13. Guía rápida: qué Rhino abrir y para qué

Las rutas son absolutas y están enlazadas. Si el lector Markdown no abre directamente un `.3dm`, copiar la ruta y usar **Archivo → Abrir** en Rhino, o **Ir → Ir a la carpeta** en Finder. Los nombres «FINAL», «CORREGIDA» o «CALCULADA» pertenecen a sus versiones y no significan aprobación actual del proyecto.

### Referencia original de la megaestructura

[MEGAESTRUCTURA_MACARRA.3dm](</Users/adam/Downloads/MEGAESTRUCTURA_MACARRA/modelo/MEGAESTRUCTURA_MACARRA.3dm>)

- **Ruta completa:** `/Users/adam/Downloads/MEGAESTRUCTURA_MACARRA/modelo/MEGAESTRUCTURA_MACARRA.3dm`.
- **Qué contiene:** Referencia macarra original: red, soporte, conexiones y piel. Antecedente fantástico; no estructura certificada.
- **Localización al redactar:** archivo presente.

### Unidad suspendida de partida

[G3_unidad_suspendida_7.3dm](</Users/adam/Downloads/G3_unidad_suspendida_7.3dm>)

- **Ruta completa:** `/Users/adam/Downloads/G3_unidad_suspendida_7.3dm`.
- **Qué contiene:** Modelo aportado al inicio de la conversación; variantes de unidad suspendida. Antecedente, no unidad actual V02.
- **Localización al redactar:** ruta histórica aportada; archivo no localizado ahora.

### Personas

[PERSONAS.3dm](</Volumes/T7/PERSONAS.3dm>)

- **Ruta completa:** `/Volumes/T7/PERSONAS.3dm`.
- **Qué contiene:** Biblioteca de figuras. Tomar personas para los modelos de arquitectura; no modelar el edificio dentro de este archivo.
- **Localización al redactar:** archivo presente.

### Unidad suspendida histórica

[G3_unidad_suspendida.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_UNIDAD/G3_unidad_suspendida.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_UNIDAD/G3_unidad_suspendida.3dm`.
- **Qué contiene:** Etapa de caracol, vidrio, altillo y variantes; incluye el desarrollo histórico F2 según sus memorias.
- **Localización al redactar:** archivo presente.

### Conjuntos históricos

[G3_conjunto_opciones.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_CONJUNTO/G3_conjunto_opciones.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_CONJUNTO/G3_conjunto_opciones.3dm`.
- **Qué contiene:** Alternativas tempranas de agregación. Conservación como antecedente.
- **Localización al redactar:** archivo presente.

### Megaestructura libre

[MEGA_A_LIBRE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/MEGAESTRUCTURA_CLAUDE/MEGA_A_LIBRE.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/MEGAESTRUCTURA_CLAUDE/MEGA_A_LIBRE.3dm`.
- **Qué contiene:** Ensayo histórico libre de megaestructura; no confundir con la referencia original de Downloads.
- **Localización al redactar:** archivo presente.

### Megaestructura en Ribera

[MEGA_B_RIBERA31_1a1.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/MEGAESTRUCTURA_CLAUDE/MEGA_B_RIBERA31_1a1.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/MEGAESTRUCTURA_CLAUDE/MEGA_B_RIBERA31_1a1.3dm`.
- **Qué contiene:** Ensayo histórico de implantación a escala de archivo; requiere contraste con la parcela y decisiones posteriores.
- **Localización al redactar:** archivo presente.

### V4 conjunto en parcela

[SELVA_MACARRA_V4_EN_PARCELA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/SELVA_MACARRA_V4_EN_PARCELA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/SELVA_MACARRA_V4_EN_PARCELA.3dm`.
- **Qué contiene:** Diez pabellones/cuarenta residentes, soportes ramificados, contexto, escaleras y ascensores. Antecedente; la distribución posterior ha cambiado.
- **Localización al redactar:** archivo presente.

### V4 unidad independiente

[UNIDAD_GRAN_BOVEDA_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/UNIDAD_GRAN_BOVEDA_EDITABLE.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/UNIDAD_GRAN_BOVEDA_EDITABLE.3dm`.
- **Qué contiene:** Pabellón aislado de cuatro habitaciones para inspección; antecedente anterior a las nuevas unidades.
- **Localización al redactar:** archivo presente.

### P02 detallada

[UNIDAD_P02_DETALLADA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/modelos/UNIDAD_P02_DETALLADA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/modelos/UNIDAD_P02_DETALLADA.3dm`.
- **Qué contiene:** Unidad P02 aislada y detallada de la etapa V4. Sirve para seguir las críticas de mobiliario, no para sustituir V01/V02/V03.
- **Localización al redactar:** archivo presente.

### P02 interior

[UNIDAD_P02_INTERIOR_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/modelos/UNIDAD_P02_INTERIOR_EDITABLE.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/modelos/UNIDAD_P02_INTERIOR_EDITABLE.3dm`.
- **Qué contiene:** Interior accesible de la P02 histórica para estudiar habitación y equipamiento.
- **Localización al redactar:** archivo presente.

### Ensayo de habitación curva

[HABITACION_CURVA_ENSAYO_A.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_HABITACION_CURVA_2026-10-18/HABITACION_CURVA_ENSAYO_A.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_HABITACION_CURVA_2026-10-18/HABITACION_CURVA_ENSAYO_A.3dm`.
- **Qué contiene:** Prueba de habitación y geometrías curvas; antecedente de cama, armario y mesa.
- **Localización al redactar:** archivo presente.

### Primer catálogo 3D de cuarenta

[CATALOGO_40_UNIDADES_COTA0.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/CATALOGO_40_UNIDADES_COTA0.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/CATALOGO_40_UNIDADES_COTA0.3dm`.
- **Qué contiene:** Cuarenta modelos separados a cota cero. Versión con los fallos posteriormente criticados; archivo de proceso.
- **Localización al redactar:** archivo presente.

### Catálogo de cuarenta corregidas

[CATALOGO_40_CORREGIDAS_COTA0.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/CATALOGO_40_CORREGIDAS_COTA0.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/CATALOGO_40_CORREGIDAS_COTA0.3dm`.
- **Qué contiene:** Cuarenta unidades compactadas/corregidas, separadas en XY. La homogeneización y las prestaciones perdidas impiden tratarlas como selección definitiva.
- **Localización al redactar:** archivo presente.

### Habitación del catálogo corregido

[HABITACION_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/HABITACION_CORREGIDA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/HABITACION_CORREGIDA.3dm`.
- **Qué contiene:** Prototipo privado de esa corrección: útil para comparar con el vestidor y la bow recuperados después.
- **Localización al redactar:** archivo presente.

### Todas las nuevas organizaciones en 3D

[TODAS_LAS_PLANTAS_3D_COTA0.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/TODAS_LAS_PLANTAS_3D_COTA0.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/TODAS_LAS_PLANTAS_3D_COTA0.3dm`.
- **Qué contiene:** Ocho organizaciones nuevas: unidades de cuatro y agrupaciones de ocho. Separadas a cota cero; no edificio apilado.
- **Localización al redactar:** archivo presente.

### V01 individual

[V01_U_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V01_U_3D.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V01_U_3D.3dm`.
- **Qué contiene:** Cuatro residentes, organización continua, habitación con vestidor y bow; anterior a revisión técnica del 20.
- **Localización al redactar:** archivo presente.

### V02 individual

[V02_U_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V02_U_3D.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V02_U_3D.3dm`.
- **Qué contiene:** Cuatro residentes, dos ámbitos desplazados. Es la V02 aclarada por Adam; pendiente de revisar tamaño.
- **Localización al redactar:** archivo presente.

### V03 individual

[V03_U_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V03_U_3D.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V03_U_3D.3dm`.
- **Qué contiene:** Cuatro residentes, organización de cruce, servicios al borde en esta etapa; extensión actual requiere revisión.
- **Localización al redactar:** archivo presente.

### V02 pareja

[V02_P_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V02_P_3D.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V02_P_3D.3dm`.
- **Qué contiene:** Pareja de ocho con dos ámbitos y umbral; no es la unidad V02_U.
- **Localización al redactar:** archivo presente.

### E01 sobre parcela

[E01_ENCUENTRO_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E01_ENCUENTRO_INTERIOR.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E01_ENCUENTRO_INTERIOR.3dm`.
- **Qué contiene:** Agrupación de ocho, encuentro ampliado, apoyos, planta baja y núcleo; copia preparada para ver interior.
- **Localización al redactar:** archivo presente.

### E02 sobre parcela

[E02_COMUNA_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E02_COMUNA_INTERIOR.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E02_COMUNA_INTERIOR.3dm`.
- **Qué contiene:** Casa común de ocho sobre apoyos con planta baja, escalera y ascensor. Base elegida para documentación.
- **Localización al redactar:** archivo presente.

### E02 revisión nativa anterior

[E02_REVISION_NATIVA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/verificacion/E02_REVISION_NATIVA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/verificacion/E02_REVISION_NATIVA.3dm`.
- **Qué contiene:** Copia nativa de verificación usada en la selección del usuario. Puede no contener cambios posteriores de programa público.
- **Localización al redactar:** archivo presente.

### E03 sobre parcela

[E03_DOS_CLAROS_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E03_DOS_CLAROS_INTERIOR.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E03_DOS_CLAROS_INTERIOR.3dm`.
- **Qué contiene:** Ensayo de ocho con dos ámbitos relacionados, soportes y programa común inferior.
- **Localización al redactar:** archivo presente.

### Tres unidades con cubiertas

[UNIDADES_4_PERSONAS_TODAS_CON_CUBIERTA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_UNIDADES_4_PERSONAS_2026-10-20/UNIDADES_4_PERSONAS_TODAS_CON_CUBIERTA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_UNIDADES_4_PERSONAS_2026-10-20/UNIDADES_4_PERSONAS_TODAS_CON_CUBIERTA.3dm`.
- **Qué contiene:** V01, V02 y V03, cuatro residentes cada una, separadas y a Z=0, con cubiertas. Documento trabajado por Adam; no incluye solar ni parejas.
- **Localización al redactar:** archivo presente.

### Tres unidades revisadas técnicamente

[TRES_UNIDADES_REVISION_TECNICA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/TRES_UNIDADES_REVISION_TECNICA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/TRES_UNIDADES_REVISION_TECNICA.3dm`.
- **Qué contiene:** Copia con revisión de perímetro de baños, puertas, sofás retirados y montantes en servicios. NO compactada todavía tras la última queja dimensional.
- **Localización al redactar:** archivo presente.

### E02 con programa público ampliado

[E02_REVISION_TECNICA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/E02_REVISION_TECNICA.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/E02_REVISION_TECNICA.3dm`.
- **Qué contiene:** Ocho residentes elevados más biblioteca, estudio/exposición, coworking, fuente y programa público de PB. Dos estados en capas alternativas; anteproyecto.
- **Localización al redactar:** archivo presente.

### Planos y layouts editables

[PLANOS_EDITABLES_Y_LAYOUTS_1_100.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/PLANOS_EDITABLES_Y_LAYOUTS_1_100.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/PLANOS_EDITABLES_Y_LAYOUTS_1_100.3dm`.
- **Qué contiene:** Dibujo 2D en metros con seis layouts 1:100, tramas, líneas y textos. No modelo 3D. Pendiente de sincronizar última cota de frente y futura compactación.
- **Localización al redactar:** archivo presente.

### Estado del usuario: tres unidades

[TRES_UNIDADES_ESTADO_USUARIO.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/instantaneas/TRES_UNIDADES_ESTADO_USUARIO.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/instantaneas/TRES_UNIDADES_ESTADO_USUARIO.3dm`.
- **Qué contiene:** Instantánea conservada antes de revisión; incluye trabajo/curvas del usuario. No es la copia técnica limpia.
- **Localización al redactar:** archivo presente.

### Estado del usuario: E02

[E02_ESTADO_USUARIO.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/instantaneas/E02_ESTADO_USUARIO.3dm>)

- **Ruta completa:** `/Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/instantaneas/E02_ESTADO_USUARIO.3dm`.
- **Qué contiene:** Instantánea del documento abierto, anterior a actualización de PB y programa público. Respaldo, no versión recomendada de distribución.
- **Localización al redactar:** archivo presente.


### Convenciones para interpretar los archivos

- `U`: unidad de cuatro en estas familias; `P`: pareja; `D`: encuentro ampliado; `S`: continuidad compartida. Son convenciones de estas series, no de todo archivo del proyecto.
- `_INTERIOR`: copia/configuración para leer el interior, no necesariamente una arquitectura distinta.
- `_PLANTA_2D` y `modelos_2d`: curvas/base de planta, no un edificio 3D constructivo.
- `_PREVIA_SOLIDA` o `MALLAS`: copia de visualización; no sustituye automáticamente a geometría editable de origen.
- `fuentes/personas_seleccionadas`: figuras auxiliares importadas, no viviendas.
- `ENTREGA` y carpetas anidadas pueden contener copias empaquetadas; no contarlas como proyectos diferentes.
- `verificacion` puede contener copias diagnósticas; no asumir que su fecha o nombre las convierte en el modelo vigente.

## 14. Documentos y fuentes para retomar el hilo

- [Investigación urbana](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/LEEME.md>).
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

## 15. Inventario de todos los Rhino localizados

Este inventario comprueba **presencia de archivos**, no abre ni valida cada modelo. Se excluyen los auxiliares AppleDouble `._*`. Incluye copias, antecedentes y algunos archivos auxiliares de investigación para no perder rutas. La descripción se basa en memorias/documentos de su serie y en el nombre; los casos sin documentación suficiente se identifican como tales. Las copias deben compararse antes de elegir cuál editar.

**488 archivos .3dm presentes bajo la raíz del proyecto al redactar.** Las rutas externas importantes se han añadido en la guía rápida.

### G3_40_UNIDADES_3D_COTA0_2026-10-18

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [CATALOGO_40_UNIDADES_COTA0.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/CATALOGO_40_UNIDADES_COTA0.3dm>) | Cuarenta modelos separados a cota cero. Versión con los fallos posteriormente criticados; archivo de proceso. | 189.81 MB |
| [ENTREGA/CATALOGO_40_UNIDADES_COTA0.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/CATALOGO_40_UNIDADES_COTA0.3dm>) | Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 860.87 MB |
| [ENTREGA/habitaciones/HABITACION_A_DETALLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/habitaciones/HABITACION_A_DETALLE.3dm>) | Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 0.57 MB |
| [ENTREGA/habitaciones/HABITACION_B_DETALLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/habitaciones/HABITACION_B_DETALLE.3dm>) | Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 0.55 MB |
| [ENTREGA/modelos/N01A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N01A_UNIDAD_3D.3dm>) | Caso N01A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 12.04 MB |
| [ENTREGA/modelos/N01B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N01B_UNIDAD_3D.3dm>) | Caso N01B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.40 MB |
| [ENTREGA/modelos/N02A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N02A_UNIDAD_3D.3dm>) | Caso N02A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.69 MB |
| [ENTREGA/modelos/N02B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N02B_UNIDAD_3D.3dm>) | Caso N02B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.51 MB |
| [ENTREGA/modelos/N03A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N03A_UNIDAD_3D.3dm>) | Caso N03A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.47 MB |
| [ENTREGA/modelos/N03B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N03B_UNIDAD_3D.3dm>) | Caso N03B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.38 MB |
| [ENTREGA/modelos/N04A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N04A_UNIDAD_3D.3dm>) | Caso N04A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.58 MB |
| [ENTREGA/modelos/N04B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N04B_UNIDAD_3D.3dm>) | Caso N04B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.48 MB |
| [ENTREGA/modelos/N05A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N05A_UNIDAD_3D.3dm>) | Caso N05A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.68 MB |
| [ENTREGA/modelos/N05B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N05B_UNIDAD_3D.3dm>) | Caso N05B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.59 MB |
| [ENTREGA/modelos/N06A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N06A_UNIDAD_3D.3dm>) | Caso N06A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.63 MB |
| [ENTREGA/modelos/N06B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N06B_UNIDAD_3D.3dm>) | Caso N06B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.54 MB |
| [ENTREGA/modelos/N07A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N07A_UNIDAD_3D.3dm>) | Caso N07A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.59 MB |
| [ENTREGA/modelos/N07B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N07B_UNIDAD_3D.3dm>) | Caso N07B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.46 MB |
| [ENTREGA/modelos/N08A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N08A_UNIDAD_3D.3dm>) | Caso N08A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.63 MB |
| [ENTREGA/modelos/N08B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N08B_UNIDAD_3D.3dm>) | Caso N08B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.61 MB |
| [ENTREGA/modelos/N09A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N09A_UNIDAD_3D.3dm>) | Caso N09A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.60 MB |
| [ENTREGA/modelos/N09B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N09B_UNIDAD_3D.3dm>) | Caso N09B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.73 MB |
| [ENTREGA/modelos/N10A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N10A_UNIDAD_3D.3dm>) | Caso N10A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.50 MB |
| [ENTREGA/modelos/N10B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N10B_UNIDAD_3D.3dm>) | Caso N10B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.63 MB |
| [ENTREGA/modelos/N11A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N11A_UNIDAD_3D.3dm>) | Caso N11A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.77 MB |
| [ENTREGA/modelos/N11B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N11B_UNIDAD_3D.3dm>) | Caso N11B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.67 MB |
| [ENTREGA/modelos/N12A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N12A_UNIDAD_3D.3dm>) | Caso N12A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.55 MB |
| [ENTREGA/modelos/N12B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N12B_UNIDAD_3D.3dm>) | Caso N12B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.41 MB |
| [ENTREGA/modelos/N13A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N13A_UNIDAD_3D.3dm>) | Caso N13A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.72 MB |
| [ENTREGA/modelos/N13B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N13B_UNIDAD_3D.3dm>) | Caso N13B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.58 MB |
| [ENTREGA/modelos/N14A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N14A_UNIDAD_3D.3dm>) | Caso N14A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.78 MB |
| [ENTREGA/modelos/N14B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N14B_UNIDAD_3D.3dm>) | Caso N14B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.68 MB |
| [ENTREGA/modelos/N15A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N15A_UNIDAD_3D.3dm>) | Caso N15A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.65 MB |
| [ENTREGA/modelos/N15B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N15B_UNIDAD_3D.3dm>) | Caso N15B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.54 MB |
| [ENTREGA/modelos/N16A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N16A_UNIDAD_3D.3dm>) | Caso N16A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.58 MB |
| [ENTREGA/modelos/N16B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N16B_UNIDAD_3D.3dm>) | Caso N16B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.67 MB |
| [ENTREGA/modelos/N17A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N17A_UNIDAD_3D.3dm>) | Caso N17A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.51 MB |
| [ENTREGA/modelos/N17B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N17B_UNIDAD_3D.3dm>) | Caso N17B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.62 MB |
| [ENTREGA/modelos/N18A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N18A_UNIDAD_3D.3dm>) | Caso N18A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.53 MB |
| [ENTREGA/modelos/N18B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N18B_UNIDAD_3D.3dm>) | Caso N18B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.47 MB |
| [ENTREGA/modelos/N19A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N19A_UNIDAD_3D.3dm>) | Caso N19A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.59 MB |
| [ENTREGA/modelos/N19B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N19B_UNIDAD_3D.3dm>) | Caso N19B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.49 MB |
| [ENTREGA/modelos/N20A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N20A_UNIDAD_3D.3dm>) | Caso N20A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.57 MB |
| [ENTREGA/modelos/N20B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/ENTREGA/modelos/N20B_UNIDAD_3D.3dm>) | Caso N20B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Copia dentro de paquete ENTREGA. | 4.69 MB |
| [N19B_REDUCIDA_2026-10-18/G3_N19B_REDUCIDA_PARCELA_2026-10-18.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/N19B_REDUCIDA_2026-10-18/G3_N19B_REDUCIDA_PARCELA_2026-10-18.3dm>) | Caso N19B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 1.18 MB |
| [detalles_habitacion/HABITACION_A_DETALLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/detalles_habitacion/HABITACION_A_DETALLE.3dm>) | Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 0.57 MB |
| [detalles_habitacion/HABITACION_B_DETALLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/detalles_habitacion/HABITACION_B_DETALLE.3dm>) | Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 0.55 MB |
| [modelos/N01A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N01A_UNIDAD_3D.3dm>) | Caso N01A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 11.65 MB |
| [modelos/N01B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N01B_UNIDAD_3D.3dm>) | Caso N01B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.09 MB |
| [modelos/N02A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N02A_UNIDAD_3D.3dm>) | Caso N02A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.38 MB |
| [modelos/N02B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N02B_UNIDAD_3D.3dm>) | Caso N02B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.20 MB |
| [modelos/N03A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N03A_UNIDAD_3D.3dm>) | Caso N03A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.17 MB |
| [modelos/N03B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N03B_UNIDAD_3D.3dm>) | Caso N03B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.08 MB |
| [modelos/N04A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N04A_UNIDAD_3D.3dm>) | Caso N04A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.28 MB |
| [modelos/N04B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N04B_UNIDAD_3D.3dm>) | Caso N04B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.16 MB |
| [modelos/N05A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N05A_UNIDAD_3D.3dm>) | Caso N05A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.36 MB |
| [modelos/N05B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N05B_UNIDAD_3D.3dm>) | Caso N05B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.28 MB |
| [modelos/N06A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N06A_UNIDAD_3D.3dm>) | Caso N06A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.33 MB |
| [modelos/N06B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N06B_UNIDAD_3D.3dm>) | Caso N06B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.23 MB |
| [modelos/N07A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N07A_UNIDAD_3D.3dm>) | Caso N07A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.28 MB |
| [modelos/N07B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N07B_UNIDAD_3D.3dm>) | Caso N07B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.15 MB |
| [modelos/N08A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N08A_UNIDAD_3D.3dm>) | Caso N08A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.33 MB |
| [modelos/N08B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N08B_UNIDAD_3D.3dm>) | Caso N08B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.29 MB |
| [modelos/N09A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N09A_UNIDAD_3D.3dm>) | Caso N09A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.29 MB |
| [modelos/N09B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N09B_UNIDAD_3D.3dm>) | Caso N09B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.41 MB |
| [modelos/N10A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N10A_UNIDAD_3D.3dm>) | Caso N10A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.20 MB |
| [modelos/N10B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N10B_UNIDAD_3D.3dm>) | Caso N10B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.33 MB |
| [modelos/N11A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N11A_UNIDAD_3D.3dm>) | Caso N11A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.45 MB |
| [modelos/N11B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N11B_UNIDAD_3D.3dm>) | Caso N11B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.35 MB |
| [modelos/N12A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N12A_UNIDAD_3D.3dm>) | Caso N12A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.24 MB |
| [modelos/N12B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N12B_UNIDAD_3D.3dm>) | Caso N12B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.10 MB |
| [modelos/N13A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N13A_UNIDAD_3D.3dm>) | Caso N13A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.40 MB |
| [modelos/N13B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N13B_UNIDAD_3D.3dm>) | Caso N13B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.26 MB |
| [modelos/N14A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N14A_UNIDAD_3D.3dm>) | Caso N14A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.46 MB |
| [modelos/N14B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N14B_UNIDAD_3D.3dm>) | Caso N14B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.36 MB |
| [modelos/N15A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N15A_UNIDAD_3D.3dm>) | Caso N15A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.35 MB |
| [modelos/N15B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N15B_UNIDAD_3D.3dm>) | Caso N15B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.24 MB |
| [modelos/N16A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N16A_UNIDAD_3D.3dm>) | Caso N16A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.27 MB |
| [modelos/N16B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N16B_UNIDAD_3D.3dm>) | Caso N16B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.36 MB |
| [modelos/N17A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N17A_UNIDAD_3D.3dm>) | Caso N17A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.21 MB |
| [modelos/N17B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N17B_UNIDAD_3D.3dm>) | Caso N17B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.31 MB |
| [modelos/N18A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N18A_UNIDAD_3D.3dm>) | Caso N18A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.23 MB |
| [modelos/N18B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N18B_UNIDAD_3D.3dm>) | Caso N18B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.16 MB |
| [modelos/N19A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N19A_UNIDAD_3D.3dm>) | Caso N19A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.29 MB |
| [modelos/N19B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N19B_UNIDAD_3D.3dm>) | Caso N19B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.18 MB |
| [modelos/N20A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N20A_UNIDAD_3D.3dm>) | Caso N20A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.27 MB |
| [modelos/N20B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos/N20B_UNIDAD_3D.3dm>) | Caso N20B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.38 MB |
| [modelos_finales/N01A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N01A_UNIDAD_3D.3dm>) | Caso N01A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 12.04 MB |
| [modelos_finales/N01B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N01B_UNIDAD_3D.3dm>) | Caso N01B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.40 MB |
| [modelos_finales/N02A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N02A_UNIDAD_3D.3dm>) | Caso N02A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.69 MB |
| [modelos_finales/N02B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N02B_UNIDAD_3D.3dm>) | Caso N02B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.51 MB |
| [modelos_finales/N03A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N03A_UNIDAD_3D.3dm>) | Caso N03A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.47 MB |
| [modelos_finales/N03B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N03B_UNIDAD_3D.3dm>) | Caso N03B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.38 MB |
| [modelos_finales/N04A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N04A_UNIDAD_3D.3dm>) | Caso N04A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.58 MB |
| [modelos_finales/N04B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N04B_UNIDAD_3D.3dm>) | Caso N04B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.48 MB |
| [modelos_finales/N05A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N05A_UNIDAD_3D.3dm>) | Caso N05A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.68 MB |
| [modelos_finales/N05B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N05B_UNIDAD_3D.3dm>) | Caso N05B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.59 MB |
| [modelos_finales/N06A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N06A_UNIDAD_3D.3dm>) | Caso N06A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.63 MB |
| [modelos_finales/N06B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N06B_UNIDAD_3D.3dm>) | Caso N06B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.54 MB |
| [modelos_finales/N07A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N07A_UNIDAD_3D.3dm>) | Caso N07A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.59 MB |
| [modelos_finales/N07B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N07B_UNIDAD_3D.3dm>) | Caso N07B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.46 MB |
| [modelos_finales/N08A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N08A_UNIDAD_3D.3dm>) | Caso N08A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.63 MB |
| [modelos_finales/N08B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N08B_UNIDAD_3D.3dm>) | Caso N08B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.61 MB |
| [modelos_finales/N09A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N09A_UNIDAD_3D.3dm>) | Caso N09A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.60 MB |
| [modelos_finales/N09B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N09B_UNIDAD_3D.3dm>) | Caso N09B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.73 MB |
| [modelos_finales/N10A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N10A_UNIDAD_3D.3dm>) | Caso N10A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.50 MB |
| [modelos_finales/N10B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N10B_UNIDAD_3D.3dm>) | Caso N10B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.63 MB |
| [modelos_finales/N11A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N11A_UNIDAD_3D.3dm>) | Caso N11A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.77 MB |
| [modelos_finales/N11B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N11B_UNIDAD_3D.3dm>) | Caso N11B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.67 MB |
| [modelos_finales/N12A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N12A_UNIDAD_3D.3dm>) | Caso N12A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.55 MB |
| [modelos_finales/N12B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N12B_UNIDAD_3D.3dm>) | Caso N12B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.41 MB |
| [modelos_finales/N13A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N13A_UNIDAD_3D.3dm>) | Caso N13A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.72 MB |
| [modelos_finales/N13B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N13B_UNIDAD_3D.3dm>) | Caso N13B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.58 MB |
| [modelos_finales/N14A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N14A_UNIDAD_3D.3dm>) | Caso N14A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.78 MB |
| [modelos_finales/N14B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N14B_UNIDAD_3D.3dm>) | Caso N14B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.68 MB |
| [modelos_finales/N15A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N15A_UNIDAD_3D.3dm>) | Caso N15A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.65 MB |
| [modelos_finales/N15B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N15B_UNIDAD_3D.3dm>) | Caso N15B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.54 MB |
| [modelos_finales/N16A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N16A_UNIDAD_3D.3dm>) | Caso N16A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.58 MB |
| [modelos_finales/N16B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N16B_UNIDAD_3D.3dm>) | Caso N16B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.67 MB |
| [modelos_finales/N17A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N17A_UNIDAD_3D.3dm>) | Caso N17A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.51 MB |
| [modelos_finales/N17B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N17B_UNIDAD_3D.3dm>) | Caso N17B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.62 MB |
| [modelos_finales/N18A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N18A_UNIDAD_3D.3dm>) | Caso N18A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.53 MB |
| [modelos_finales/N18B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N18B_UNIDAD_3D.3dm>) | Caso N18B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.47 MB |
| [modelos_finales/N19A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N19A_UNIDAD_3D.3dm>) | Caso N19A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.59 MB |
| [modelos_finales/N19B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N19B_UNIDAD_3D.3dm>) | Caso N19B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.49 MB |
| [modelos_finales/N20A_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N20A_UNIDAD_3D.3dm>) | Caso N20A. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.57 MB |
| [modelos_finales/N20B_UNIDAD_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/modelos_finales/N20B_UNIDAD_3D.3dm>) | Caso N20B. Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. | 4.69 MB |
| [verificacion/SESION_REVISION.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_40_UNIDADES_3D_COTA0_2026-10-18/verificacion/SESION_REVISION.3dm>) | Primera modelización 3D de la serie de cuarenta a cota cero; anterior a correcciones y cuestionada por el usuario. Archivo de comprobación; contrastar con modelo principal. | 28.53 MB |
### G3_ATLAS_40_PLANTAS_2026-10-18

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [modelos/01A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/01A_PLANTA_2D.3dm>) | Caso 01A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/01B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/01B_PLANTA_2D.3dm>) | Caso 01B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.06 MB |
| [modelos/02A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/02A_PLANTA_2D.3dm>) | Caso 02A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/02B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/02B_PLANTA_2D.3dm>) | Caso 02B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.06 MB |
| [modelos/03A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/03A_PLANTA_2D.3dm>) | Caso 03A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/03B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/03B_PLANTA_2D.3dm>) | Caso 03B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.07 MB |
| [modelos/04A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/04A_PLANTA_2D.3dm>) | Caso 04A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/04B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/04B_PLANTA_2D.3dm>) | Caso 04B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.07 MB |
| [modelos/05A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/05A_PLANTA_2D.3dm>) | Caso 05A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/05B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/05B_PLANTA_2D.3dm>) | Caso 05B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.07 MB |
| [modelos/06A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/06A_PLANTA_2D.3dm>) | Caso 06A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.09 MB |
| [modelos/06B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/06B_PLANTA_2D.3dm>) | Caso 06B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.07 MB |
| [modelos/07A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/07A_PLANTA_2D.3dm>) | Caso 07A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.09 MB |
| [modelos/07B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/07B_PLANTA_2D.3dm>) | Caso 07B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.07 MB |
| [modelos/08A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/08A_PLANTA_2D.3dm>) | Caso 08A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.09 MB |
| [modelos/08B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/08B_PLANTA_2D.3dm>) | Caso 08B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.07 MB |
| [modelos/09A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/09A_PLANTA_2D.3dm>) | Caso 09A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/09B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/09B_PLANTA_2D.3dm>) | Caso 09B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/10A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/10A_PLANTA_2D.3dm>) | Caso 10A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/10B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/10B_PLANTA_2D.3dm>) | Caso 10B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.07 MB |
| [modelos/11A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/11A_PLANTA_2D.3dm>) | Caso 11A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/11B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/11B_PLANTA_2D.3dm>) | Caso 11B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.07 MB |
| [modelos/12A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/12A_PLANTA_2D.3dm>) | Caso 12A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.09 MB |
| [modelos/12B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/12B_PLANTA_2D.3dm>) | Caso 12B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.07 MB |
| [modelos/13A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/13A_PLANTA_2D.3dm>) | Caso 13A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.09 MB |
| [modelos/13B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/13B_PLANTA_2D.3dm>) | Caso 13B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/14A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/14A_PLANTA_2D.3dm>) | Caso 14A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.09 MB |
| [modelos/14B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/14B_PLANTA_2D.3dm>) | Caso 14B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.07 MB |
| [modelos/15A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/15A_PLANTA_2D.3dm>) | Caso 15A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.10 MB |
| [modelos/15B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/15B_PLANTA_2D.3dm>) | Caso 15B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/16A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/16A_PLANTA_2D.3dm>) | Caso 16A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/16B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/16B_PLANTA_2D.3dm>) | Caso 16B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/17A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/17A_PLANTA_2D.3dm>) | Caso 17A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/17B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/17B_PLANTA_2D.3dm>) | Caso 17B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.06 MB |
| [modelos/18A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/18A_PLANTA_2D.3dm>) | Caso 18A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.09 MB |
| [modelos/18B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/18B_PLANTA_2D.3dm>) | Caso 18B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.07 MB |
| [modelos/19A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/19A_PLANTA_2D.3dm>) | Caso 19A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
| [modelos/19B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/19B_PLANTA_2D.3dm>) | Caso 19B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.07 MB |
| [modelos/20A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/20A_PLANTA_2D.3dm>) | Caso 20A. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.09 MB |
| [modelos/20B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_ATLAS_40_PLANTAS_2026-10-18/modelos/20B_PLANTA_2D.3dm>) | Caso 20B. Primera serie: base de planta 2D de una alternativa del atlas; antecedente sin validación de implantación. | 0.08 MB |
### G3_CONJUNTO

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [G3_conjunto_opciones.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_CONJUNTO/G3_conjunto_opciones.3dm>) | Alternativas tempranas de agregación. Conservación como antecedente. | 16.99 MB |
### G3_CONTINUIDAD_PARCELA_2026-10-19

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [modelos_2d/V01_D_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V01_D_CORREGIDA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.68 MB |
| [modelos_2d/V01_D_PARCELA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V01_D_PARCELA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.41 MB |
| [modelos_2d/V01_S_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V01_S_CORREGIDA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.67 MB |
| [modelos_2d/V01_S_PARCELA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V01_S_PARCELA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.40 MB |
| [modelos_2d/V01_U_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V01_U_CORREGIDA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.34 MB |
| [modelos_2d/V01_U_PARCELA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V01_U_PARCELA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.21 MB |
| [modelos_2d/V02_P_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V02_P_CORREGIDA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.70 MB |
| [modelos_2d/V02_P_PARCELA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V02_P_PARCELA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.42 MB |
| [modelos_2d/V02_U_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V02_U_CORREGIDA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.35 MB |
| [modelos_2d/V02_U_PARCELA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V02_U_PARCELA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.22 MB |
| [modelos_2d/V03_D_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V03_D_CORREGIDA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.71 MB |
| [modelos_2d/V03_D_PARCELA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V03_D_PARCELA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.44 MB |
| [modelos_2d/V03_S_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V03_S_CORREGIDA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.69 MB |
| [modelos_2d/V03_S_PARCELA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V03_S_PARCELA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.43 MB |
| [modelos_2d/V03_U_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V03_U_CORREGIDA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.36 MB |
| [modelos_2d/V03_U_PARCELA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_CONTINUIDAD_PARCELA_2026-10-19/modelos_2d/V03_U_PARCELA.3dm>) | Ensayo 2D de planta corregida o posición sobre parcela; revisar código y límites de encaje/luz. | 0.23 MB |
### G3_CORRECCION_40_2026-10-18

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [CATALOGO_40_CORREGIDAS_COTA0.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/CATALOGO_40_CORREGIDAS_COTA0.3dm>) | Cuarenta unidades compactadas/corregidas, separadas en XY. La homogeneización y las prestaciones perdidas impiden tratarlas como selección definitiva. | 312.67 MB |
| [ENTREGA/CATALOGO_40_CORREGIDAS_COTA0.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/CATALOGO_40_CORREGIDAS_COTA0.3dm>) | Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 312.67 MB |
| [ENTREGA/HABITACION_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/HABITACION_CORREGIDA.3dm>) | Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 0.26 MB |
| [ENTREGA/modelos/N01A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N01A_CORREGIDA.3dm>) | Caso N01A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.94 MB |
| [ENTREGA/modelos/N01B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N01B_CORREGIDA.3dm>) | Caso N01B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.90 MB |
| [ENTREGA/modelos/N02A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N02A_CORREGIDA.3dm>) | Caso N02A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.93 MB |
| [ENTREGA/modelos/N02B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N02B_CORREGIDA.3dm>) | Caso N02B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.92 MB |
| [ENTREGA/modelos/N03A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N03A_CORREGIDA.3dm>) | Caso N03A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.95 MB |
| [ENTREGA/modelos/N03B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N03B_CORREGIDA.3dm>) | Caso N03B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.91 MB |
| [ENTREGA/modelos/N04A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N04A_CORREGIDA.3dm>) | Caso N04A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.91 MB |
| [ENTREGA/modelos/N04B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N04B_CORREGIDA.3dm>) | Caso N04B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.91 MB |
| [ENTREGA/modelos/N05A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N05A_CORREGIDA.3dm>) | Caso N05A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.92 MB |
| [ENTREGA/modelos/N05B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N05B_CORREGIDA.3dm>) | Caso N05B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.98 MB |
| [ENTREGA/modelos/N06A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N06A_CORREGIDA.3dm>) | Caso N06A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.94 MB |
| [ENTREGA/modelos/N06B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N06B_CORREGIDA.3dm>) | Caso N06B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.97 MB |
| [ENTREGA/modelos/N07A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N07A_CORREGIDA.3dm>) | Caso N07A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.95 MB |
| [ENTREGA/modelos/N07B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N07B_CORREGIDA.3dm>) | Caso N07B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.91 MB |
| [ENTREGA/modelos/N08A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N08A_CORREGIDA.3dm>) | Caso N08A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.91 MB |
| [ENTREGA/modelos/N08B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N08B_CORREGIDA.3dm>) | Caso N08B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.97 MB |
| [ENTREGA/modelos/N09A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N09A_CORREGIDA.3dm>) | Caso N09A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.94 MB |
| [ENTREGA/modelos/N09B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N09B_CORREGIDA.3dm>) | Caso N09B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.91 MB |
| [ENTREGA/modelos/N10A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N10A_CORREGIDA.3dm>) | Caso N10A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.91 MB |
| [ENTREGA/modelos/N10B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N10B_CORREGIDA.3dm>) | Caso N10B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.91 MB |
| [ENTREGA/modelos/N11A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N11A_CORREGIDA.3dm>) | Caso N11A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.93 MB |
| [ENTREGA/modelos/N11B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N11B_CORREGIDA.3dm>) | Caso N11B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.98 MB |
| [ENTREGA/modelos/N12A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N12A_CORREGIDA.3dm>) | Caso N12A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.95 MB |
| [ENTREGA/modelos/N12B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N12B_CORREGIDA.3dm>) | Caso N12B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.90 MB |
| [ENTREGA/modelos/N13A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N13A_CORREGIDA.3dm>) | Caso N13A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.92 MB |
| [ENTREGA/modelos/N13B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N13B_CORREGIDA.3dm>) | Caso N13B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.91 MB |
| [ENTREGA/modelos/N14A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N14A_CORREGIDA.3dm>) | Caso N14A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.97 MB |
| [ENTREGA/modelos/N14B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N14B_CORREGIDA.3dm>) | Caso N14B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.98 MB |
| [ENTREGA/modelos/N15A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N15A_CORREGIDA.3dm>) | Caso N15A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.94 MB |
| [ENTREGA/modelos/N15B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N15B_CORREGIDA.3dm>) | Caso N15B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.96 MB |
| [ENTREGA/modelos/N16A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N16A_CORREGIDA.3dm>) | Caso N16A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.91 MB |
| [ENTREGA/modelos/N16B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N16B_CORREGIDA.3dm>) | Caso N16B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.91 MB |
| [ENTREGA/modelos/N17A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N17A_CORREGIDA.3dm>) | Caso N17A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.93 MB |
| [ENTREGA/modelos/N17B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N17B_CORREGIDA.3dm>) | Caso N17B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.98 MB |
| [ENTREGA/modelos/N18A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N18A_CORREGIDA.3dm>) | Caso N18A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.94 MB |
| [ENTREGA/modelos/N18B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N18B_CORREGIDA.3dm>) | Caso N18B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.96 MB |
| [ENTREGA/modelos/N19A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N19A_CORREGIDA.3dm>) | Caso N19A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.91 MB |
| [ENTREGA/modelos/N19B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N19B_CORREGIDA.3dm>) | Caso N19B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.91 MB |
| [ENTREGA/modelos/N20A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N20A_CORREGIDA.3dm>) | Caso N20A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.93 MB |
| [ENTREGA/modelos/N20B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/ENTREGA/modelos/N20B_CORREGIDA.3dm>) | Caso N20B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Copia dentro de paquete ENTREGA. | 1.97 MB |
| [HABITACION_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/HABITACION_CORREGIDA.3dm>) | Prototipo privado de esa corrección: útil para comparar con el vestidor y la bow recuperados después. | 0.25 MB |
| [modelos/N01A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N01A_CORREGIDA.3dm>) | Caso N01A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.94 MB |
| [modelos/N01B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N01B_CORREGIDA.3dm>) | Caso N01B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.90 MB |
| [modelos/N02A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N02A_CORREGIDA.3dm>) | Caso N02A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.92 MB |
| [modelos/N02B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N02B_CORREGIDA.3dm>) | Caso N02B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.92 MB |
| [modelos/N03A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N03A_CORREGIDA.3dm>) | Caso N03A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.95 MB |
| [modelos/N03B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N03B_CORREGIDA.3dm>) | Caso N03B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.90 MB |
| [modelos/N04A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N04A_CORREGIDA.3dm>) | Caso N04A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.90 MB |
| [modelos/N04B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N04B_CORREGIDA.3dm>) | Caso N04B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.90 MB |
| [modelos/N05A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N05A_CORREGIDA.3dm>) | Caso N05A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.92 MB |
| [modelos/N05B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N05B_CORREGIDA.3dm>) | Caso N05B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.98 MB |
| [modelos/N06A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N06A_CORREGIDA.3dm>) | Caso N06A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.94 MB |
| [modelos/N06B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N06B_CORREGIDA.3dm>) | Caso N06B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.97 MB |
| [modelos/N07A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N07A_CORREGIDA.3dm>) | Caso N07A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.95 MB |
| [modelos/N07B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N07B_CORREGIDA.3dm>) | Caso N07B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos/N08A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N08A_CORREGIDA.3dm>) | Caso N08A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos/N08B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N08B_CORREGIDA.3dm>) | Caso N08B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.97 MB |
| [modelos/N09A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N09A_CORREGIDA.3dm>) | Caso N09A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.94 MB |
| [modelos/N09B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N09B_CORREGIDA.3dm>) | Caso N09B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos/N10A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N10A_CORREGIDA.3dm>) | Caso N10A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.90 MB |
| [modelos/N10B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N10B_CORREGIDA.3dm>) | Caso N10B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.90 MB |
| [modelos/N11A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N11A_CORREGIDA.3dm>) | Caso N11A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.92 MB |
| [modelos/N11B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N11B_CORREGIDA.3dm>) | Caso N11B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.97 MB |
| [modelos/N12A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N12A_CORREGIDA.3dm>) | Caso N12A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.94 MB |
| [modelos/N12B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N12B_CORREGIDA.3dm>) | Caso N12B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.90 MB |
| [modelos/N13A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N13A_CORREGIDA.3dm>) | Caso N13A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos/N13B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N13B_CORREGIDA.3dm>) | Caso N13B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos/N14A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N14A_CORREGIDA.3dm>) | Caso N14A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.97 MB |
| [modelos/N14B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N14B_CORREGIDA.3dm>) | Caso N14B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.98 MB |
| [modelos/N15A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N15A_CORREGIDA.3dm>) | Caso N15A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.94 MB |
| [modelos/N15B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N15B_CORREGIDA.3dm>) | Caso N15B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.96 MB |
| [modelos/N16A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N16A_CORREGIDA.3dm>) | Caso N16A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos/N16B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N16B_CORREGIDA.3dm>) | Caso N16B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos/N17A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N17A_CORREGIDA.3dm>) | Caso N17A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.93 MB |
| [modelos/N17B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N17B_CORREGIDA.3dm>) | Caso N17B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.97 MB |
| [modelos/N18A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N18A_CORREGIDA.3dm>) | Caso N18A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.94 MB |
| [modelos/N18B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N18B_CORREGIDA.3dm>) | Caso N18B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.96 MB |
| [modelos/N19A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N19A_CORREGIDA.3dm>) | Caso N19A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos/N19B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N19B_CORREGIDA.3dm>) | Caso N19B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos/N20A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N20A_CORREGIDA.3dm>) | Caso N20A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.93 MB |
| [modelos/N20B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos/N20B_CORREGIDA.3dm>) | Caso N20B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.97 MB |
| [modelos_listos/HABITACION_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/HABITACION_CORREGIDA.3dm>) | Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 0.26 MB |
| [modelos_listos/N01A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N01A_CORREGIDA.3dm>) | Caso N01A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.94 MB |
| [modelos_listos/N01B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N01B_CORREGIDA.3dm>) | Caso N01B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.90 MB |
| [modelos_listos/N02A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N02A_CORREGIDA.3dm>) | Caso N02A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.93 MB |
| [modelos_listos/N02B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N02B_CORREGIDA.3dm>) | Caso N02B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.92 MB |
| [modelos_listos/N03A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N03A_CORREGIDA.3dm>) | Caso N03A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.95 MB |
| [modelos_listos/N03B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N03B_CORREGIDA.3dm>) | Caso N03B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos_listos/N04A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N04A_CORREGIDA.3dm>) | Caso N04A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos_listos/N04B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N04B_CORREGIDA.3dm>) | Caso N04B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos_listos/N05A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N05A_CORREGIDA.3dm>) | Caso N05A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.92 MB |
| [modelos_listos/N05B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N05B_CORREGIDA.3dm>) | Caso N05B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.98 MB |
| [modelos_listos/N06A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N06A_CORREGIDA.3dm>) | Caso N06A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.94 MB |
| [modelos_listos/N06B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N06B_CORREGIDA.3dm>) | Caso N06B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.97 MB |
| [modelos_listos/N07A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N07A_CORREGIDA.3dm>) | Caso N07A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.95 MB |
| [modelos_listos/N07B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N07B_CORREGIDA.3dm>) | Caso N07B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos_listos/N08A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N08A_CORREGIDA.3dm>) | Caso N08A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos_listos/N08B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N08B_CORREGIDA.3dm>) | Caso N08B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.97 MB |
| [modelos_listos/N09A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N09A_CORREGIDA.3dm>) | Caso N09A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.94 MB |
| [modelos_listos/N09B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N09B_CORREGIDA.3dm>) | Caso N09B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos_listos/N10A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N10A_CORREGIDA.3dm>) | Caso N10A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos_listos/N10B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N10B_CORREGIDA.3dm>) | Caso N10B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos_listos/N11A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N11A_CORREGIDA.3dm>) | Caso N11A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.93 MB |
| [modelos_listos/N11B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N11B_CORREGIDA.3dm>) | Caso N11B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.98 MB |
| [modelos_listos/N12A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N12A_CORREGIDA.3dm>) | Caso N12A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.95 MB |
| [modelos_listos/N12B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N12B_CORREGIDA.3dm>) | Caso N12B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.90 MB |
| [modelos_listos/N13A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N13A_CORREGIDA.3dm>) | Caso N13A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.92 MB |
| [modelos_listos/N13B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N13B_CORREGIDA.3dm>) | Caso N13B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos_listos/N14A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N14A_CORREGIDA.3dm>) | Caso N14A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.97 MB |
| [modelos_listos/N14B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N14B_CORREGIDA.3dm>) | Caso N14B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.98 MB |
| [modelos_listos/N15A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N15A_CORREGIDA.3dm>) | Caso N15A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.94 MB |
| [modelos_listos/N15B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N15B_CORREGIDA.3dm>) | Caso N15B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.96 MB |
| [modelos_listos/N16A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N16A_CORREGIDA.3dm>) | Caso N16A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos_listos/N16B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N16B_CORREGIDA.3dm>) | Caso N16B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos_listos/N17A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N17A_CORREGIDA.3dm>) | Caso N17A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.93 MB |
| [modelos_listos/N17B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N17B_CORREGIDA.3dm>) | Caso N17B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.98 MB |
| [modelos_listos/N18A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N18A_CORREGIDA.3dm>) | Caso N18A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.94 MB |
| [modelos_listos/N18B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N18B_CORREGIDA.3dm>) | Caso N18B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.96 MB |
| [modelos_listos/N19A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N19A_CORREGIDA.3dm>) | Caso N19A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos_listos/N19B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N19B_CORREGIDA.3dm>) | Caso N19B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.91 MB |
| [modelos_listos/N20A_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N20A_CORREGIDA.3dm>) | Caso N20A. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.93 MB |
| [modelos_listos/N20B_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/modelos_listos/N20B_CORREGIDA.3dm>) | Caso N20B. Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. | 1.97 MB |
| [verificacion/SESION_CORRECCION.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/verificacion/SESION_CORRECCION.3dm>) | Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Archivo de comprobación; contrastar con modelo principal. | 0.01 MB |
| [verificacion/SESION_CORRECCION_1c4ea68cc597433d87a44c583ff773c7.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/verificacion/SESION_CORRECCION_1c4ea68cc597433d87a44c583ff773c7.3dm>) | Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Archivo de comprobación; contrastar con modelo principal. | 0.01 MB |
| [verificacion/SESION_CORRECCION_75611b911f3e4c869caf1b300c88c5c2.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/verificacion/SESION_CORRECCION_75611b911f3e4c869caf1b300c88c5c2.3dm>) | Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Archivo de comprobación; contrastar con modelo principal. | 0.01 MB |
| [verificacion/SESION_CORRECCION_863485d8ac2b4fb4a7f316c07e29935b.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/verificacion/SESION_CORRECCION_863485d8ac2b4fb4a7f316c07e29935b.3dm>) | Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Archivo de comprobación; contrastar con modelo principal. | 0.01 MB |
| [verificacion/VISTAS_f2bf5a7cc79547a9bc7d70f36e384cbd.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_CORRECCION_40_2026-10-18/verificacion/VISTAS_f2bf5a7cc79547a9bc7d70f36e384cbd.3dm>) | Serie de cuarenta corregidas: modelo de unidad o habitación. Antecedente demasiado homogeneizado; no selección final. Archivo de comprobación; contrastar con modelo principal. | 0.01 MB |
### G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS_2026-10-19

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [modelos_2d/V01_D_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS_2026-10-19/modelos_2d/V01_D_CORREGIDA.3dm>) | Nueva organización 2D con servicios al borde; antecedente de los modelos posteriores. | 0.67 MB |
| [modelos_2d/V01_S_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS_2026-10-19/modelos_2d/V01_S_CORREGIDA.3dm>) | Nueva organización 2D con servicios al borde; antecedente de los modelos posteriores. | 0.67 MB |
| [modelos_2d/V01_U_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS_2026-10-19/modelos_2d/V01_U_CORREGIDA.3dm>) | Nueva organización 2D con servicios al borde; antecedente de los modelos posteriores. | 0.34 MB |
| [modelos_2d/V02_P_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS_2026-10-19/modelos_2d/V02_P_CORREGIDA.3dm>) | Nueva organización 2D con servicios al borde; antecedente de los modelos posteriores. | 0.70 MB |
| [modelos_2d/V02_U_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS_2026-10-19/modelos_2d/V02_U_CORREGIDA.3dm>) | Nueva organización 2D con servicios al borde; antecedente de los modelos posteriores. | 0.35 MB |
| [modelos_2d/V03_D_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS_2026-10-19/modelos_2d/V03_D_CORREGIDA.3dm>) | Nueva organización 2D con servicios al borde; antecedente de los modelos posteriores. | 0.73 MB |
| [modelos_2d/V03_S_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS_2026-10-19/modelos_2d/V03_S_CORREGIDA.3dm>) | Nueva organización 2D con servicios al borde; antecedente de los modelos posteriores. | 0.71 MB |
| [modelos_2d/V03_U_CORREGIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS_2026-10-19/modelos_2d/V03_U_CORREGIDA.3dm>) | Nueva organización 2D con servicios al borde; antecedente de los modelos posteriores. | 0.36 MB |
### G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [fuentes/personas_seleccionadas.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16/fuentes/personas_seleccionadas.3dm>) | Figuras humanas auxiliares seleccionadas del archivo de personas; no arquitectura. | 4.14 MB |
| [modelos/PLANTA_BAJA_V5_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16/modelos/PLANTA_BAJA_V5_EDITABLE.3dm>) | Modelo de estudio de luz/planta baja relacionado con V4; antecedente, no validación del proyecto actual. | 17.14 MB |
| [modelos/SELVA_V5_LUZ_Y_PLANTA_BAJA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16/modelos/SELVA_V5_LUZ_Y_PLANTA_BAJA.3dm>) | Modelo de estudio de luz/planta baja relacionado con V4; antecedente, no validación del proyecto actual. | 148.32 MB |
| [modelos/UNIDAD_V5_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16/modelos/UNIDAD_V5_INTERIOR.3dm>) | Modelo de estudio de luz/planta baja relacionado con V4; antecedente, no validación del proyecto actual. | 7.81 MB |
| [modelos/UNIDAD_V5_NORTE_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16/modelos/UNIDAD_V5_NORTE_EDITABLE.3dm>) | Modelo de estudio de luz/planta baja relacionado con V4; antecedente, no validación del proyecto actual. | 7.81 MB |
### G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16 2

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [fuentes/personas_seleccionadas.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/98_COPIAS_DUPLICADAS/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16 2/fuentes/personas_seleccionadas.3dm>) | Figuras humanas auxiliares seleccionadas del archivo de personas; no arquitectura. | 4.14 MB |
| [modelos/PLANTA_BAJA_V5_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/98_COPIAS_DUPLICADAS/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16 2/modelos/PLANTA_BAJA_V5_EDITABLE.3dm>) | Copia de la carpeta de estudio de luz/PB; comparar con original antes de editar. | 17.14 MB |
| [modelos/SELVA_V5_LUZ_Y_PLANTA_BAJA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/98_COPIAS_DUPLICADAS/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16 2/modelos/SELVA_V5_LUZ_Y_PLANTA_BAJA.3dm>) | Copia de la carpeta de estudio de luz/PB; comparar con original antes de editar. | 148.32 MB |
| [modelos/UNIDAD_V5_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/98_COPIAS_DUPLICADAS/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16 2/modelos/UNIDAD_V5_INTERIOR.3dm>) | Copia de la carpeta de estudio de luz/PB; comparar con original antes de editar. | 7.81 MB |
| [modelos/UNIDAD_V5_NORTE_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/98_COPIAS_DUPLICADAS/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16 2/modelos/UNIDAD_V5_NORTE_EDITABLE.3dm>) | Copia de la carpeta de estudio de luz/PB; comparar con original antes de editar. | 8.47 MB |
### G3_MODELOS_HERENCIA_MACARRA_2026-10-19

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [fuentes/personas_seleccionadas.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/fuentes/personas_seleccionadas.3dm>) | Figuras humanas auxiliares seleccionadas del archivo de personas; no arquitectura. | 4.14 MB |
| [modelos/E01_ENCUENTRO.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E01_ENCUENTRO.3dm>) | Ensayo sobre parcela con vivienda elevada, apoyos, núcleo y planta baja común. Modelo 3D de estudio con envolvente y soporte; no calculado integralmente. | 6.40 MB |
| [modelos/E01_ENCUENTRO_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E01_ENCUENTRO_INTERIOR.3dm>) | Agrupación de ocho, encuentro ampliado, apoyos, planta baja y núcleo; copia preparada para ver interior. | 6.40 MB |
| [modelos/E02_COMUNA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E02_COMUNA.3dm>) | Ensayo sobre parcela con vivienda elevada, apoyos, núcleo y planta baja común. Modelo 3D de estudio con envolvente y soporte; no calculado integralmente. | 5.84 MB |
| [modelos/E02_COMUNA_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E02_COMUNA_INTERIOR.3dm>) | Casa común de ocho sobre apoyos con planta baja, escalera y ascensor. Base elegida para documentación. | 5.84 MB |
| [modelos/E03_DOS_CLAROS.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E03_DOS_CLAROS.3dm>) | Ensayo sobre parcela con vivienda elevada, apoyos, núcleo y planta baja común. Modelo 3D de estudio con envolvente y soporte; no calculado integralmente. | 6.56 MB |
| [modelos/E03_DOS_CLAROS_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/E03_DOS_CLAROS_INTERIOR.3dm>) | Ensayo de ocho con dos ámbitos relacionados, soportes y programa común inferior. | 6.56 MB |
| [modelos/TODAS_LAS_PLANTAS_3D_COTA0.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/TODAS_LAS_PLANTAS_3D_COTA0.3dm>) | Ocho organizaciones nuevas: unidades de cuatro y agrupaciones de ocho. Separadas a cota cero; no edificio apilado. | 26.34 MB |
| [modelos/V01_D_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V01_D_3D.3dm>) | Ocho residentes, sala de encuentro ampliada. Modelo 3D de estudio con envolvente y soporte; no calculado integralmente. | 4.27 MB |
| [modelos/V01_D_3D_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V01_D_3D_INTERIOR.3dm>) | Ocho residentes, sala de encuentro ampliada. Copia para lectura de interior. | 4.27 MB |
| [modelos/V01_S_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V01_S_3D.3dm>) | Ocho residentes, continuidad de comuna. Modelo 3D de estudio con envolvente y soporte; no calculado integralmente. | 3.69 MB |
| [modelos/V01_S_3D_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V01_S_3D_INTERIOR.3dm>) | Ocho residentes, continuidad de comuna. Copia para lectura de interior. | 3.69 MB |
| [modelos/V01_U_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V01_U_3D.3dm>) | Cuatro residentes, organización continua, habitación con vestidor y bow; anterior a revisión técnica del 20. | 2.14 MB |
| [modelos/V01_U_3D_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V01_U_3D_INTERIOR.3dm>) | Cuatro residentes, común continuo. Copia para lectura de interior. | 2.14 MB |
| [modelos/V02_P_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V02_P_3D.3dm>) | Pareja de ocho con dos ámbitos y umbral; no es la unidad V02_U. | 4.42 MB |
| [modelos/V02_P_3D_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V02_P_3D_INTERIOR.3dm>) | Ocho residentes, pareja con umbral. Copia para lectura de interior. | 4.42 MB |
| [modelos/V02_U_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V02_U_3D.3dm>) | Cuatro residentes, dos ámbitos desplazados. Es la V02 aclarada por Adam; pendiente de revisar tamaño. | 3.28 MB |
| [modelos/V02_U_3D_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V02_U_3D_INTERIOR.3dm>) | Cuatro residentes, dos ámbitos desplazados. Copia para lectura de interior. | 3.28 MB |
| [modelos/V03_D_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V03_D_3D.3dm>) | Ocho residentes, encuentro diagonal ampliado. Modelo 3D de estudio con envolvente y soporte; no calculado integralmente. | 4.36 MB |
| [modelos/V03_D_3D_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V03_D_3D_INTERIOR.3dm>) | Ocho residentes, encuentro diagonal ampliado. Copia para lectura de interior. | 4.36 MB |
| [modelos/V03_S_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V03_S_3D.3dm>) | Ocho residentes, continuidad diagonal. Modelo 3D de estudio con envolvente y soporte; no calculado integralmente. | 4.30 MB |
| [modelos/V03_S_3D_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V03_S_3D_INTERIOR.3dm>) | Ocho residentes, continuidad diagonal. Copia para lectura de interior. | 4.30 MB |
| [modelos/V03_U_3D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V03_U_3D.3dm>) | Cuatro residentes, organización de cruce, servicios al borde en esta etapa; extensión actual requiere revisión. | 2.75 MB |
| [modelos/V03_U_3D_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/V03_U_3D_INTERIOR.3dm>) | Cuatro residentes, cruce y servicios al borde. Copia para lectura de interior. | 2.75 MB |
| [verificacion/E02_REVISION_NATIVA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/verificacion/E02_REVISION_NATIVA.3dm>) | Copia nativa de verificación usada en la selección del usuario. Puede no contener cambios posteriores de programa público. | 5.84 MB |
### G3_P02_A_REVISADA_2026-10-18

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [P02_A_REVISADA_HABITACION_Y_UMBRAL.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_A_REVISADA_2026-10-18/P02_A_REVISADA_HABITACION_Y_UMBRAL.3dm>) | Revisión intermedia de planta P02; antecedente de las nuevas organizaciones. | 0.06 MB |
### G3_P02_CORREGIDA_APOYOS_2026-10-18

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [P02_CORREGIDA_COMPLETA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_CORREGIDA_APOYOS_2026-10-18/P02_CORREGIDA_COMPLETA.3dm>) | Corrección intermedia de apoyos/niveles de P02, anterior a la revisión por tejidos. | 2.84 MB |
| [P02_CORREGIDA_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_CORREGIDA_APOYOS_2026-10-18/P02_CORREGIDA_INTERIOR.3dm>) | Corrección intermedia de apoyos/niveles de P02, anterior a la revisión por tejidos. | 2.84 MB |
### G3_P02_HABITACION_CURVA_2026-10-18

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [HABITACION_CURVA_ENSAYO_A.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_HABITACION_CURVA_2026-10-18/HABITACION_CURVA_ENSAYO_A.3dm>) | Prueba de habitación y geometrías curvas; antecedente de cama, armario y mesa. | 0.04 MB |
| [P02_V4_BASE_SIN_MOBILIARIO_VISIBLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_HABITACION_CURVA_2026-10-18/P02_V4_BASE_SIN_MOBILIARIO_VISIBLE.3dm>) | Ensayo de habitación curva o base P02 sin mobiliario visible; comparar con memoria de esa fase. | 16.40 MB |
### G3_P02_MATERIALES_ORIGEN_2026-10-18

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [P02_COMPLETA_MATERIALES_000.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_MATERIALES_ORIGEN_2026-10-18/P02_COMPLETA_MATERIALES_000.3dm>) | P02 con recuperación de materiales/colores del origen; no revisión final de planta. | 22.07 MB |
| [P02_INTERIOR_MATERIALES_000.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_MATERIALES_ORIGEN_2026-10-18/P02_INTERIOR_MATERIALES_000.3dm>) | P02 con recuperación de materiales/colores del origen; no revisión final de planta. | 22.16 MB |
### G3_P02_MODELO_PLANTA_COMPLETA_2026-10-18

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [P02_UNIDAD_COMPLETA_ESTUDIO.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_MODELO_PLANTA_COMPLETA_2026-10-18/P02_UNIDAD_COMPLETA_ESTUDIO.3dm>) | Modelo completo intermedio P02 para explorar distribución; no compactación reciente. | 0.80 MB |
| [P02_UNIDAD_COMPLETA_INTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/04_P02_LA_HABITACION_16-18oct/G3_P02_MODELO_PLANTA_COMPLETA_2026-10-18/P02_UNIDAD_COMPLETA_INTERIOR.3dm>) | Modelo completo intermedio P02 para explorar distribución; no compactación reciente. | 0.80 MB |
### G3_PLANOS_TECNICOS_2026-10-20

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [instantaneas/E02_ESTADO_USUARIO.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/instantaneas/E02_ESTADO_USUARIO.3dm>) | Instantánea del documento abierto, anterior a actualización de PB y programa público. Respaldo, no versión recomendada de distribución. | 11.40 MB |
| [instantaneas/TRES_UNIDADES_ESTADO_USUARIO.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/instantaneas/TRES_UNIDADES_ESTADO_USUARIO.3dm>) | Instantánea conservada antes de revisión; incluye trabajo/curvas del usuario. No es la copia técnica limpia. | 28.62 MB |
| [modelos/E02_GIRO90_ENSAYO_NO_ENCAJADO.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/E02_GIRO90_ENSAYO_NO_ENCAJADO.3dm>) | Archivo de proyecto localizado; contenido específico no reabierto ni validado para esta memoria. | 7.56 MB |
| [modelos/E02_REVISION_TECNICA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/E02_REVISION_TECNICA.3dm>) | Ocho residentes elevados más biblioteca, estudio/exposición, coworking, fuente y programa público de PB. Dos estados en capas alternativas; anteproyecto. | 7.59 MB |
| [modelos/PLANOS_EDITABLES_Y_LAYOUTS_1_100.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/PLANOS_EDITABLES_Y_LAYOUTS_1_100.3dm>) | Dibujo 2D en metros con seis layouts 1:100, tramas, líneas y textos. No modelo 3D. Pendiente de sincronizar última cota de frente y futura compactación. | 2.05 MB |
| [modelos/TRES_UNIDADES_COMPACTADAS_GIRO90.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/TRES_UNIDADES_COMPACTADAS_GIRO90.3dm>) | Archivo de proyecto localizado; contenido específico no reabierto ni validado para esta memoria. | 9.23 MB |
| [modelos/TRES_UNIDADES_REVISION_TECNICA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_PLANOS_TECNICOS_2026-10-20/modelos/TRES_UNIDADES_REVISION_TECNICA.3dm>) | Copia con revisión de perímetro de baños, puertas, sofás retirados y montantes en servicios. NO compactada todavía tras la última queja dimensional. | 10.24 MB |
### G3_PLANTAS_FORMAS_DE_VIVIR_2026-10-19

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [DOS_UNIDADES_PLANTA_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_PLANTAS_FORMAS_DE_VIVIR_2026-10-19/DOS_UNIDADES_PLANTA_EDITABLE.3dm>) | Ensayo 2D de vida común, habitación o pareja; anterior al ajuste de bow y servicios. | 0.55 MB |
| [HABITACION_PLANTA_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_PLANTAS_FORMAS_DE_VIVIR_2026-10-19/HABITACION_PLANTA_EDITABLE.3dm>) | Ensayo 2D de vida común, habitación o pareja; anterior al ajuste de bow y servicios. | 0.07 MB |
| [V01_PLANTA_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_PLANTAS_FORMAS_DE_VIVIR_2026-10-19/V01_PLANTA_EDITABLE.3dm>) | Ensayo 2D de vida común, habitación o pareja; anterior al ajuste de bow y servicios. | 0.27 MB |
| [V02_PLANTA_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_PLANTAS_FORMAS_DE_VIVIR_2026-10-19/V02_PLANTA_EDITABLE.3dm>) | Ensayo 2D de vida común, habitación o pareja; anterior al ajuste de bow y servicios. | 0.28 MB |
| [V03_PLANTA_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_PLANTAS_FORMAS_DE_VIVIR_2026-10-19/V03_PLANTA_EDITABLE.3dm>) | Ensayo 2D de vida común, habitación o pareja; anterior al ajuste de bow y servicios. | 0.29 MB |
### G3_REVISION_2026-10-08

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [01_UNIDAD_reconstruida.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08/01_UNIDAD_reconstruida.3dm>) | Reconstrucción/propuesta de revisión temprana; no sustituye desarrollos posteriores. | 24.95 MB |
| [02_CONJUNTOS_reconstruidos.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08/02_CONJUNTOS_reconstruidos.3dm>) | Reconstrucción/propuesta de revisión temprana; no sustituye desarrollos posteriores. | 13.65 MB |
| [03_MODULO_D_duplex_propuesto.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08/03_MODULO_D_duplex_propuesto.3dm>) | Reconstrucción/propuesta de revisión temprana; no sustituye desarrollos posteriores. | 1.52 MB |
| [04_MODULO_S_una_planta.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08/04_MODULO_S_una_planta.3dm>) | Reconstrucción/propuesta de revisión temprana; no sustituye desarrollos posteriores. | 0.50 MB |
| [05_CONJUNTO_propuesto_32_40.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08/05_CONJUNTO_propuesto_32_40.3dm>) | Reconstrucción/propuesta de revisión temprana; no sustituye desarrollos posteriores. | 2.39 MB |
| [G3_REVISION_2026-10-08/01_UNIDAD_reconstruida.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08/G3_REVISION_2026-10-08/01_UNIDAD_reconstruida.3dm>) | Reconstrucción/propuesta de revisión temprana; no sustituye desarrollos posteriores. | 24.95 MB |
| [G3_REVISION_2026-10-08/02_CONJUNTOS_reconstruidos.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08/G3_REVISION_2026-10-08/02_CONJUNTOS_reconstruidos.3dm>) | Reconstrucción/propuesta de revisión temprana; no sustituye desarrollos posteriores. | 13.65 MB |
| [G3_REVISION_2026-10-08/03_MODULO_D_duplex_propuesto.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08/G3_REVISION_2026-10-08/03_MODULO_D_duplex_propuesto.3dm>) | Reconstrucción/propuesta de revisión temprana; no sustituye desarrollos posteriores. | 1.52 MB |
| [G3_REVISION_2026-10-08/04_MODULO_S_una_planta.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08/G3_REVISION_2026-10-08/04_MODULO_S_una_planta.3dm>) | Reconstrucción/propuesta de revisión temprana; no sustituye desarrollos posteriores. | 0.50 MB |
| [G3_REVISION_2026-10-08/05_CONJUNTO_propuesto_32_40.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08/G3_REVISION_2026-10-08/05_CONJUNTO_propuesto_32_40.3dm>) | Reconstrucción/propuesta de revisión temprana; no sustituye desarrollos posteriores. | 2.39 MB |
### G3_SELVA_HABITADA_V2_2026-10-16

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [modelos/01_UNIDAD_U4.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_HABITADA_V2_2026-10-16/modelos/01_UNIDAD_U4.3dm>) | Etapa V2 de exploración del complejo; antecedente posteriormente revisado. | 0.46 MB |
| [modelos/02_SELVA_EN_PARCELA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_HABITADA_V2_2026-10-16/modelos/02_SELVA_EN_PARCELA.3dm>) | Etapa V2 de exploración del complejo; antecedente posteriormente revisado. | 5.64 MB |
### G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [fuentes/personas_seleccionadas.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/fuentes/personas_seleccionadas.3dm>) | Figuras humanas auxiliares seleccionadas del archivo de personas; no arquitectura. | 4.14 MB |
| [modelos/D01_NUDO_RAMIFICADO_1a1.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/D01_NUDO_RAMIFICADO_1a1.3dm>) | Detalle de nudo ramificado con brida, tubos, cartelas y pernos; estudio de encuentro, no certificación. | 1.33 MB |
| [modelos/D02_ENVOLVENTE_Y_BANDEJA_1a1.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/D02_ENVOLVENTE_Y_BANDEJA_1a1.3dm>) | Detalle de bandeja, capas de envolvente y desagüe de la etapa correspondiente. | 0.70 MB |
| [modelos/D03_ASCENSOR_COMPLETO.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/D03_ASCENSOR_COMPLETO.3dm>) | Ascensor aislado: cabina, guías, máquina, foso y rellanos de estudio; sin fabricante validado. | 1.59 MB |
| [modelos/PREVIA_SOLIDA_MALLAS.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/PREVIA_SOLIDA_MALLAS.3dm>) | Copia de lectura/visualización mediante mallas; no sustituye por sí sola al modelo editable de origen. | 125.51 MB |
| [modelos/SELVA_MACARRA_V4_EN_PARCELA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/SELVA_MACARRA_V4_EN_PARCELA.3dm>) | Diez pabellones/cuarenta residentes, soportes ramificados, contexto, escaleras y ascensores. Antecedente; la distribución posterior ha cambiado. | 161.30 MB |
| [modelos/SELVA_MACARRA_V4_FINAL.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/SELVA_MACARRA_V4_FINAL.3dm>) | Etapa V4 con predimensionado preliminar; cálculo no transferible a geometrías nuevas. | 138.00 MB |
| [modelos/UNIDAD_GRAN_BOVEDA_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/UNIDAD_GRAN_BOVEDA_EDITABLE.3dm>) | Pabellón aislado de cuatro habitaciones para inspección; antecedente anterior a las nuevas unidades. | 8.01 MB |
### G3_SELVA_RADICAL_RHINO_V3_2026-10-16

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [fuentes/personas_seleccionadas.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_RADICAL_RHINO_V3_2026-10-16/fuentes/personas_seleccionadas.3dm>) | Figuras humanas auxiliares seleccionadas del archivo de personas; no arquitectura. | 4.14 MB |
| [modelos/ARCHIVO_INTERMEDIO_V4_ANTERIOR.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_RADICAL_RHINO_V3_2026-10-16/modelos/ARCHIVO_INTERMEDIO_V4_ANTERIOR.3dm>) | Etapa V3 del complejo o geometría de apoyo; antecedente previo a V4. | 131.65 MB |
| [modelos/SELVA_RADICAL_COMPLETA_V3.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_RADICAL_RHINO_V3_2026-10-16/modelos/SELVA_RADICAL_COMPLETA_V3.3dm>) | Etapa V3 del complejo o geometría de apoyo; antecedente previo a V4. | 241.00 MB |
| [modelos/UNIDAD_CURVA_U4_DETALLE_V3.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_SELVA_RADICAL_RHINO_V3_2026-10-16/modelos/UNIDAD_CURVA_U4_DETALLE_V3.3dm>) | Etapa V3 del complejo o geometría de apoyo; antecedente previo a V4. | 7.01 MB |
### G3_TEJIDOS_A_PLANTA_40_2026-10-18

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [modelos/N01A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N01A_PLANTA_2D.3dm>) | Caso N01A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N01B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N01B_PLANTA_2D.3dm>) | Caso N01B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.09 MB |
| [modelos/N02A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N02A_PLANTA_2D.3dm>) | Caso N02A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N02B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N02B_PLANTA_2D.3dm>) | Caso N02B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.08 MB |
| [modelos/N03A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N03A_PLANTA_2D.3dm>) | Caso N03A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N03B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N03B_PLANTA_2D.3dm>) | Caso N03B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.09 MB |
| [modelos/N04A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N04A_PLANTA_2D.3dm>) | Caso N04A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N04B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N04B_PLANTA_2D.3dm>) | Caso N04B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.09 MB |
| [modelos/N05A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N05A_PLANTA_2D.3dm>) | Caso N05A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.10 MB |
| [modelos/N05B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N05B_PLANTA_2D.3dm>) | Caso N05B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.10 MB |
| [modelos/N06A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N06A_PLANTA_2D.3dm>) | Caso N06A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.10 MB |
| [modelos/N06B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N06B_PLANTA_2D.3dm>) | Caso N06B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.09 MB |
| [modelos/N07A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N07A_PLANTA_2D.3dm>) | Caso N07A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.10 MB |
| [modelos/N07B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N07B_PLANTA_2D.3dm>) | Caso N07B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.09 MB |
| [modelos/N08A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N08A_PLANTA_2D.3dm>) | Caso N08A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N08B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N08B_PLANTA_2D.3dm>) | Caso N08B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.08 MB |
| [modelos/N09A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N09A_PLANTA_2D.3dm>) | Caso N09A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N09B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N09B_PLANTA_2D.3dm>) | Caso N09B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.10 MB |
| [modelos/N10A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N10A_PLANTA_2D.3dm>) | Caso N10A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N10B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N10B_PLANTA_2D.3dm>) | Caso N10B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.09 MB |
| [modelos/N11A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N11A_PLANTA_2D.3dm>) | Caso N11A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N11B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N11B_PLANTA_2D.3dm>) | Caso N11B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.08 MB |
| [modelos/N12A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N12A_PLANTA_2D.3dm>) | Caso N12A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N12B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N12B_PLANTA_2D.3dm>) | Caso N12B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.09 MB |
| [modelos/N13A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N13A_PLANTA_2D.3dm>) | Caso N13A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.10 MB |
| [modelos/N13B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N13B_PLANTA_2D.3dm>) | Caso N13B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.10 MB |
| [modelos/N14A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N14A_PLANTA_2D.3dm>) | Caso N14A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N14B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N14B_PLANTA_2D.3dm>) | Caso N14B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.09 MB |
| [modelos/N15A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N15A_PLANTA_2D.3dm>) | Caso N15A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N15B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N15B_PLANTA_2D.3dm>) | Caso N15B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.10 MB |
| [modelos/N16A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N16A_PLANTA_2D.3dm>) | Caso N16A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N16B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N16B_PLANTA_2D.3dm>) | Caso N16B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.10 MB |
| [modelos/N17A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N17A_PLANTA_2D.3dm>) | Caso N17A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.10 MB |
| [modelos/N17B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N17B_PLANTA_2D.3dm>) | Caso N17B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.09 MB |
| [modelos/N18A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N18A_PLANTA_2D.3dm>) | Caso N18A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N18B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N18B_PLANTA_2D.3dm>) | Caso N18B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.10 MB |
| [modelos/N19A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N19A_PLANTA_2D.3dm>) | Caso N19A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.10 MB |
| [modelos/N19B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N19B_PLANTA_2D.3dm>) | Caso N19B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.09 MB |
| [modelos/N20A_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N20A_PLANTA_2D.3dm>) | Caso N20A. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.11 MB |
| [modelos/N20B_PLANTA_2D.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/G3_TEJIDOS_A_PLANTA_40_2026-10-18/modelos/N20B_PLANTA_2D.3dm>) | Caso N20B. Segunda serie: contorno/base 2D derivado del tejido de acciones; no unidad 3D ni solución final. | 0.10 MB |
### G3_UNIDAD

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [G3_unidad_suspendida.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_UNIDAD/G3_unidad_suspendida.3dm>) | Etapa de caracol, vidrio, altillo y variantes; incluye el desarrollo histórico F2 según sus memorias. | 24.18 MB |
| [G3_unidad_suspendida_v1_caracol_2026-10-07.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_UNIDAD/G3_unidad_suspendida_v1_caracol_2026-10-07.3dm>) | Variante histórica de unidad suspendida; caracol, altillo y envolvente según etapa. | 0.80 MB |
| [G3_unidad_suspendida_v3_2026-10-07.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_UNIDAD/G3_unidad_suspendida_v3_2026-10-07.3dm>) | Variante histórica de unidad suspendida; caracol, altillo y envolvente según etapa. | 4.61 MB |
| [G3_unidad_suspendida_v4_2026-10-07.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_UNIDAD/G3_unidad_suspendida_v4_2026-10-07.3dm>) | Variante histórica de unidad suspendida; caracol, altillo y envolvente según etapa. | 20.28 MB |
| [G3_unidad_suspendida_v5a_2026-10-08.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_UNIDAD/G3_unidad_suspendida_v5a_2026-10-08.3dm>) | Variante histórica de unidad suspendida; caracol, altillo y envolvente según etapa. | 23.41 MB |
### G3_UNIDADES_4_PERSONAS_2026-10-20

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [UNIDADES_4_PERSONAS_TODAS_CON_CUBIERTA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/G3_UNIDADES_4_PERSONAS_2026-10-20/UNIDADES_4_PERSONAS_TODAS_CON_CUBIERTA.3dm>) | V01, V02 y V03, cuatro residentes cada una, separadas y a Z=0, con cubiertas. Documento trabajado por Adam; no incluye solar ni parejas. | 27.07 MB |
### G3_UNIDAD_AISLADA_DETALLE_2026-10-16

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [UNIDAD_P02_DETALLADA_ENTREGA/modelos/D02_ENVOLVENTE_Y_BANDEJA_1a1.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/UNIDAD_P02_DETALLADA_ENTREGA/modelos/D02_ENVOLVENTE_Y_BANDEJA_1a1.3dm>) | Detalle de bandeja, capas de envolvente y desagüe de la etapa correspondiente. | 0.70 MB |
| [UNIDAD_P02_DETALLADA_ENTREGA/modelos/UNIDAD_P02_DETALLADA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/UNIDAD_P02_DETALLADA_ENTREGA/modelos/UNIDAD_P02_DETALLADA.3dm>) | Unidad P02 o detalle asociado a V4; antecedente de las revisiones del interior. | 20.07 MB |
| [UNIDAD_P02_DETALLADA_ENTREGA/modelos/UNIDAD_P02_INTERIOR_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/UNIDAD_P02_DETALLADA_ENTREGA/modelos/UNIDAD_P02_INTERIOR_EDITABLE.3dm>) | Unidad P02 o detalle asociado a V4; antecedente de las revisiones del interior. | 17.07 MB |
| [UNIDAD_P02_DETALLADA_ENTREGA/modelos/UNIDAD_P02_PREVIA_SOLIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/UNIDAD_P02_DETALLADA_ENTREGA/modelos/UNIDAD_P02_PREVIA_SOLIDA.3dm>) | Copia de lectura/visualización mediante mallas; no sustituye por sí sola al modelo editable de origen. | 13.92 MB |
| [modelos/D02_ENVOLVENTE_Y_BANDEJA_1a1.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/modelos/D02_ENVOLVENTE_Y_BANDEJA_1a1.3dm>) | Detalle de bandeja, capas de envolvente y desagüe de la etapa correspondiente. | 0.70 MB |
| [modelos/UNIDAD_P02_DETALLADA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/modelos/UNIDAD_P02_DETALLADA.3dm>) | Unidad P02 aislada y detallada de la etapa V4. Sirve para seguir las críticas de mobiliario, no para sustituir V01/V02/V03. | 19.43 MB |
| [modelos/UNIDAD_P02_INTERIOR_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/modelos/UNIDAD_P02_INTERIOR_EDITABLE.3dm>) | Interior accesible de la P02 histórica para estudiar habitación y equipamiento. | 17.07 MB |
| [modelos/UNIDAD_P02_PREVIA_SOLIDA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/modelos/UNIDAD_P02_PREVIA_SOLIDA.3dm>) | Copia de lectura/visualización mediante mallas; no sustituye por sí sola al modelo editable de origen. | 13.92 MB |
| [verificacion/historico/UNIDAD_P02_COMPLETA_EDITABLE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/G3_UNIDAD_AISLADA_DETALLE_2026-10-16/verificacion/historico/UNIDAD_P02_COMPLETA_EDITABLE.3dm>) | Unidad P02 o detalle asociado a V4; antecedente de las revisiones del interior. Archivo de comprobación; contrastar con modelo principal. | 21.77 MB |
### G3_UNIONES_COMUNAS_2026-10-19

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [V01_D_PLANTA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_UNIONES_COMUNAS_2026-10-19/V01_D_PLANTA.3dm>) | Ensayo 2D de ocho residentes: encuentro ampliado o continuidad común; no implantación definitiva. | 0.57 MB |
| [V01_S_PLANTA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_UNIONES_COMUNAS_2026-10-19/V01_S_PLANTA.3dm>) | Ensayo 2D de ocho residentes: encuentro ampliado o continuidad común; no implantación definitiva. | 0.57 MB |
| [V03_D_PLANTA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_UNIONES_COMUNAS_2026-10-19/V03_D_PLANTA.3dm>) | Ensayo 2D de ocho residentes: encuentro ampliado o continuidad común; no implantación definitiva. | 0.64 MB |
| [V03_S_PLANTA.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/G3_UNIONES_COMUNAS_2026-10-19/V03_S_PLANTA.3dm>) | Ensayo 2D de ocho residentes: encuentro ampliado o continuidad común; no implantación definitiva. | 0.62 MB |
### INVESTIGACIÓN

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03A_MODELO_PROXY/PILOT_FRAGMENT.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03A_MODELO_PROXY/PILOT_FRAGMENT.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 1.32 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03A_MODELO_PROXY/SOL_REFUGIO_3D_PROXY_v001.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03A_MODELO_PROXY/SOL_REFUGIO_3D_PROXY_v001.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 1.39 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B6_RESOLUCION/ASSET_LIBRARY_v002.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B6_RESOLUCION/ASSET_LIBRARY_v002.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 0.70 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B6_RESOLUCION/MASTER_ARCHITECTURE_v003.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B6_RESOLUCION/MASTER_ARCHITECTURE_v003.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 5.33 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B6_RESOLUCION/SOL_FULL_SCENE_v002.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B6_RESOLUCION/SOL_FULL_SCENE_v002.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 5.41 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B6_RESOLUCION/SOL_PRESENTATION_MASTER_v001.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B6_RESOLUCION/SOL_PRESENTATION_MASTER_v001.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 5.41 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B7_DETAILING_V004/ASSET_LIBRARY_v003.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B7_DETAILING_V004/ASSET_LIBRARY_v003.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 1.16 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B7_DETAILING_V004/MASTER_ARCHITECTURE_v004.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B7_DETAILING_V004/MASTER_ARCHITECTURE_v004.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 10.95 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B7_DETAILING_V004/SOL_FULL_SCENE_v003.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B7_DETAILING_V004/SOL_FULL_SCENE_v003.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 11.08 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B7_DETAILING_V004/SOL_PRESENTATION_MASTER_v002.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B7_DETAILING_V004/SOL_PRESENTATION_MASTER_v002.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 11.08 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B8_PURGE_MICRODETAIL_V005/ASSET_LIBRARY_v004.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B8_PURGE_MICRODETAIL_V005/ASSET_LIBRARY_v004.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 2.95 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B8_PURGE_MICRODETAIL_V005/MASTER_ARCHITECTURE_v005.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B8_PURGE_MICRODETAIL_V005/MASTER_ARCHITECTURE_v005.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 12.65 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B8_PURGE_MICRODETAIL_V005/SOL_FULL_SCENE_v004.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B8_PURGE_MICRODETAIL_V005/SOL_FULL_SCENE_v004.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 12.82 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B8_PURGE_MICRODETAIL_V005/SOL_PRESENTATION_MASTER_v003.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B8_PURGE_MICRODETAIL_V005/SOL_PRESENTATION_MASTER_v003.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 12.82 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B9_HYPERDETAIL_V006/ASSET_LIBRARY_v005.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B9_HYPERDETAIL_V006/ASSET_LIBRARY_v005.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 11.31 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B9_HYPERDETAIL_V006/MASTER_ARCHITECTURE_v006.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B9_HYPERDETAIL_V006/MASTER_ARCHITECTURE_v006.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 21.66 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B9_HYPERDETAIL_V006/SOL_FULL_SCENE_v005.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B9_HYPERDETAIL_V006/SOL_FULL_SCENE_v005.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 21.90 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B9_HYPERDETAIL_V006/SOL_PRESENTATION_MASTER_v004.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B9_HYPERDETAIL_V006/SOL_PRESENTATION_MASTER_v004.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 21.90 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B_MODELO_MAESTRO/ASSET_LIBRARY_v001.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B_MODELO_MAESTRO/ASSET_LIBRARY_v001.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 0.63 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B_MODELO_MAESTRO/MASTER_ARCHITECTURE_v002.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B_MODELO_MAESTRO/MASTER_ARCHITECTURE_v002.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 2.74 MB |
| [REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B_MODELO_MAESTRO/SOL_FULL_SCENE_v001.3dm](</Volumes/T7/G3 Proyectos/INVESTIGACIÓN/REFERENCIAS/REFUGIO_CLIMATICO/FASE_03B_MODELO_MAESTRO/SOL_FULL_SCENE_v001.3dm>) | Base/derivado de investigación, contexto o referencia. El uso concreto requiere consultar su carpeta; no es una vivienda actual. | 2.83 MB |
### MAPPEADOS

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [elrastro radio 600m.3dm](</Volumes/T7/G3 Proyectos/MAPPEADOS/elrastro radio 600m.3dm>) | Modelo cartográfico/contextual del entorno; comprobar unidades, origen y procedencia antes de implantar. | 2578.10 MB |
### MEGAESTRUCTURA_CLAUDE

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [MEGA_A_LIBRE.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/MEGAESTRUCTURA_CLAUDE/MEGA_A_LIBRE.3dm>) | Ensayo histórico libre de megaestructura; no confundir con la referencia original de Downloads. | 44.46 MB |
| [MEGA_B_RIBERA31_1a1.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/MEGAESTRUCTURA_CLAUDE/MEGA_B_RIBERA31_1a1.3dm>) | Ensayo histórico de implantación a escala de archivo; requiere contraste con la parcela y decisiones posteriores. | 130.28 MB |
### MODELOS_ENGEL_p93-94

| Archivo / ruta enlazada | Qué contiene o cómo interpretarlo | Tamaño |
|---|---|---:|
| [Engel_estructuras_G3.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/MODELOS_ENGEL_p93-94/Engel_estructuras_G3.3dm>) | Estudio estructural auxiliar asociado a referencias Engel; no es una unidad del complejo. | 9.41 MB |
| [Engel_p93-94_estructuras_tienda.3dm](</Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/MODELOS_ENGEL_p93-94/Engel_p93-94_estructuras_tienda.3dm>) | Estudio estructural auxiliar asociado a referencias Engel; no es una unidad del complejo. | 4.22 MB |

---

## Cierre del registro

El avance real es haber pasado de una imagen de megaestructura y una suma de objetos a discutir prestaciones privadas, acciones simultáneas, diferencias de convivencia, agregación y vida pública en la parcela. El problema actual sigue siendo arquitectónico: **hacer que esa ambición quepa, funcione y reciba luz sin vaciarla de carácter**.

No hay todavía un complejo definitivo de cuarenta personas con distribución, implantación, luz, estructura e instalaciones integralmente validadas. Tampoco se ha cerrado una selección definitiva entre las unidades actuales. La última instrucción de diseño que queda registrada es revisar los tamaños de V02 y de las demás plantas, conservando el cuerpo y el mobiliario a escala real.
