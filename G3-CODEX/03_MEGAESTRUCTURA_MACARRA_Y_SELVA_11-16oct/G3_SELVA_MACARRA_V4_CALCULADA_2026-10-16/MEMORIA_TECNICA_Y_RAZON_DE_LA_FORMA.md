# Selva macarra V4 | Memoria técnica y razón de la forma

16 de octubre de 2026. Anteproyecto y predimensionado reproducible. El nombre del archivo «calculada» identifica la existencia de un modelo analítico preliminar; no significa edificio certificado ni proyecto de ejecución.

## Decisiones que ordenan la radicalidad

Diez grandes pabellones, repartidos en tres grupos de árboles, sustituyen el apilamiento uniforme rechazado. Cada pabellón contiene cuatro refugios privados, cocina y mesa de grupo, y dos baños. Las plataformas se alternan en altura para producir diagonales, perspectivas y vacíos de más de una planta. La bóveda reúne cada grupo en un volumen grande. Las ramas recogen los bordes del forjado y los troncos adelgazan hacia arriba. Una retícula posterior conecta los árboles para controlar la deriva; el frente conserva la apertura y los voladizos.

Cotas por grupo: [3.8, 9.4, 15.0, 20.6]; [6.6, 12.2, 17.8]; [9.4, 15.0, 20.6]. La altura máxima de cubiertas exteriores ronda 25,9 m. La parcela procede del archivo geométrico del proyecto, no de una nueva comprobación urbanística.

## Qué se ha calculado

Pórtico espacial de 358 nodos y 458 elementos de viga de seis grados de libertad por nodo. Modelo elástico lineal de barras con ejes curvos discretizados; pies empotrados y uniones idealizadas rígidas. Perfiles circulares huecos de acero. E=210 GPa, G=81 GPa, fy adoptado=345 MPa por el intervalo de espesores de la propuesta S355. Autopeso del acero incluido. Las secciones y sus ejes se transfieren al Rhino; las curvas NURBS interpolan la discretización analítica.

Hipótesis de carga: 3,6 kN/m² permanentes de suelo, acabados, particiones, cubierta e instalaciones; 5,0 kN/m² variables sobre TODA la bandeja, como ensayo conservador de zonas comunes respecto a dormitorios; además, autopeso de seis viguetas por bandeja y 2,5 kN en cada uno de tres depósitos. Ensayo de viento de ±1,0 kN/m² en las dos direcciones, con momento por aplicación a 2,15 m sobre la planta. Esta presión es una hipótesis de ensayo, no la determinación completa del viento de Madrid.

Se han explorado combinaciones ELS G+Q con viento positivo y negativo y ELU 1,35G+1,5Q; 1,35G+1,5W+1,05Q; 1,35G+1,5Q+0,9W, con los signos aplicables. Las cargas asimétricas de ocupación, torsiones accidentales y fases de montaje aún requieren casos adicionales.

## Resultados que han modificado el diseño

- Árboles sin conexión posterior ni aumento de secciones: deriva máxima de ensayo **295.4 mm**.
- Versión con conexión posterior y secciones afinadas seleccionadas: **35.0 mm** de deriva máxima ELS y **20.9 mm** de desplazamiento vertical máximo para G+Q.
- Interacción preliminar máxima de barras N/Nb + M/Mrd: **0.578**. Se usa cribado de Euler con longitud de cada tramo curvo completo y curva de imperfección conservadora; esto no verifica el pandeo global ni sustituye la normativa de estabilidad.
- Refinamiento de cuatro a ocho segmentos por curva: 35.00 → 34.79 mm de deriva máxima.
- Pruebas del motor: tracción axial y voladizo contrastados con soluciones analíticas; equilibrio global de fuerzas comprobado para cada caso.

La elección la condiciona la rigidez, además de la resistencia. Por ello aparecen la conexión posterior, la profundidad de las ramas y las vigas de bandeja. La disminución de diámetro del tronco responde a la reducción de cargas hacia su extremo superior. Todas las barras se identifican por tipo, diámetro y espesor en `ESTRUCTURA_RESULTADOS.json`.

## Suelo y envolvente

Viguetas secundarias **RHS360x160x10**, cada 1,15 m, luz de ensayo 7,15 m: tensión de flexión ELU 107.3 MPa y flecha ELS 10.6 mm frente a L/300=23.8 mm. Se modelan como perfiles huecos; los extremos, soldaduras y colaboración del tablero deben desarrollarse.

Costillas de bóveda seleccionadas **Ø114.3 × 6.3 mm** cada 0.486 m. Ensayo plano con pies fijos, G=1,0 y Q=1,0 kN/m²: tensión ELU 104.3 MPa y desplazamiento ELS aproximado 21.7 mm. Faltan el pandeo, la acción de la envolvente, succión y el arriostramiento fuera del plano.

Detalle estratificado: contrachapado 18 mm + corcho 160 mm + tablero 18 mm + impermeabilización 2 mm, cámara y piel exterior. Transmitancia unidimensional de ensayo **U=0.224 W/m²K**, con conductividades asumidas. Los puentes térmicos, las carpinterías, la estanqueidad y el comportamiento energético global no están verificados.

## Nudo ramificado

Se desarrolla una brida anular de dos placas de 35 mm, dieciséis M30 8.8 en círculo de radio 0,57 m, cartelas y tubos huecos. Para las fuerzas de referencia del ramal crítico de gravedad: N=96.9 kN; M=508.2 kNm. Reparto elástico simplificado: tracción estimada por perno=117.5 kN, frente a resistencia nominal estimada=323.1 kN. No se han comprobado el efecto palanca de las chapas, las soldaduras, las tensiones locales del casquillo ni la rigidez real de la unión.

Los apoyos transmiten esfuerzos importantes al suelo. Las placas y encepados del Rhino son reservas geométricas; no se ha dimensionado una cimentación con capacidad geotécnica. Las reacciones se entregan para que ese siguiente cálculo parta de datos, en lugar de atribuir capacidad a raíces decorativas.

## Velas, lluvia y mantenimiento

La cubierta textil es una protección exterior adicional. Sus anclajes transmiten viento y pretensado a las bandejas. Ensayo elemental de cable parabólico de 5,25 m, flecha 0,60 m, franja tributaria de 2 m y presión 1,0 kN/m²: tensión ELU aproximada **18.9 kN**. La propuesta dibuja tensores y manguitos; queda pendiente el análisis no lineal de membrana, el pretensado y la respuesta aerodinámica. Los tirantes principales se representan de Ø18 mm, superiores al Ø16 mm del ensayo; deben comprobarse sus terminales y pretensado.

Una vela recoge aproximadamente 81.9 m². Lluvia de ensayo 100 mm/h: **2.275 L/s** por vela y **22.75 L/s** para el conjunto. A media sección y pendiente 1 %, con n=0,011, Manning da 3.05 L/s para DN100, 19.38 para DN200 y 35.14 para DN250. Son comprobaciones hidráulicas ideales, no sustituyen HS5, accesorios, mantenimiento, lluvia local ni el cálculo de bajantes.

En el modelo hay ramales DN100, rebosaderos DN50 y montantes de lluvia DN200; saneamiento DN110 y bandeja eléctrica se mantienen diferenciados. Tres depósitos suspendidos de unos 250 L apoyan el riego, con su carga añadida al modelo analítico. No se presupone la conexión real con una red municipal sin su comprobación.

## Programa, ascensores y límites de privacidad

40 residentes en diez grupos. Las habitaciones son privadas; cocina, estar y baños se comparten por grupo; las terrazas, talleres, cantina, aula y lavandería forman la infraestructura del conjunto. Los accesos a los pabellones se sitúan en el paso transversal lateral; el frente acristalado no exige cruzar una cocina para entrar.

Los tres ascensores resuelven las cotas alternadas de cada grupo de árboles, con cabinas propuestas de 1,40 × 1,60 m, puertas nominales de 0,90 m, guías, contrapesos, máquina, botoneras, foso y rellanos. Las escaleras diagonales permiten recorrer el conjunto; las escaleras de extremo se separan de las habitaciones. El fondo no se considera otra calle: la descarga debe volver al frente oeste por el recorrido de suelo.

La reconstrucción formal de la gran bóveda modifica la unidad V2. Las células dibujadas ahora son compactas, aproximadamente 8 m² útiles geométricos, y no conservan los 12 m² de aquella versión. La distribución accesible de baño y habitaciones, acústica y habitabilidad deben revisarse antes de dar por cerrada la tipología.

Las diez bandejas suman **1104.25 m²** en proyección horizontal, incluyendo viviendas y terrazas. No se deben sumar de nuevo los suelos de los pabellones que ya están dentro de esas bandejas. Se entrega un inventario geométrico aparte para programa de planta baja, escaleras, galerías y núcleos. La unión de superficies de suelo por cota, contando peldaños y mesetas y descontando encuentros coplanares, suma 1549.57 m². Este inventario no equivale al cómputo normativo. Su comparación completa con los 1.500 m² aproximados del enunciado sigue abierta; no se atribuye automáticamente una exención a las superficies exteriores.

## Qué significa y qué no acredita este estudio

Permite relacionar forma, cargas, secciones y desplazamientos y reproducir las decisiones de predimensionado. No certifica la seguridad del edificio. Permanecen pendientes segundo orden, pandeo global, imperfecciones, estabilidad de montaje, vibración y confort dinámico, fatiga, todas las uniones, fuego, cimentación, viento de sitio y membranas, compartimentación, evacuación hasta calle y accesibilidad completa. El modelo de arquitectura tampoco cuenta como comprobación integral de interferencias.

## Fuentes de referencia y archivos de cálculo

- CTE DB-SE-AE, acciones: https://www.codigotecnico.org/pdf/Documentos/SE/DBSE-AE.pdf
- CTE DB-SE-A, acero: https://www.codigotecnico.org/pdf/Documentos/SE/DBSE-A.pdf
- CTE DB-SUA: https://www.codigotecnico.org/pdf/Documentos/SUA/DBSUA.pdf
- CTE DB-SI: https://www.codigotecnico.org/pdf/Documentos/SI/DBSI.pdf
- Enunciado del taller: copia de `lectura/enunciado.txt`, viviendas temporales para jóvenes en El Rastro, aproximadamente 1.500 m², número libre cercano a veinte unidades o cuarenta habitantes y desarrollo de anteproyecto.
- Modelo analítico completo: `calculo/ESTRUCTURA_RESULTADOS.json`.
- Cálculos locales: `calculo/SUBSISTEMAS_RESULTADOS.json`.
- Fuentes reproducibles: `fuentes/calcular_estructura.py`, `fuentes/calcular_subsistemas.py`, `fuentes/modelar_v4_rhino.py` y `fuentes/modelar_detalles.py`.
