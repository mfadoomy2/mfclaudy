# G3 · Lo que se hizo mal, lo que ya existe y lo que falta

25 de octubre de 2026. Auditoría hecha antes de dibujar nada nuevo, leyendo el repositorio entero. Cada error lleva su fuente para poder comprobarlo. Las reglas de la derecha son las que aplico a partir de ahora; si alguna se rompe, el trabajo no se entrega.

Fuentes principales: `G3_HISTORIA_COMPLETA_DEL_PROYECTO.md` (§§ 8–43), `G3-CLAUDE/00_LEEME_G3_CLAUDE.md` (§§ 4–6), `G3-CODEX/00_RECOPILACION_CODEX_2026-10-24/TODO_EL_PROCESO_G3.md` (reglas vigentes y decisiones rechazadas), `G3_CORRECCION_40_2026-10-18/LEER_PRIMERO.md`, `G3_DECIDIR_UNIDAD_PARCELA_2026-10-19/EMPEZAR_AQUI.md`, `G3_MODELOS_HERENCIA_MACARRA_2026-10-19/HERENCIA_Y_PLANTA_BAJA.md`, `G3_REFERENCIAS_RURALEX_COCINA_2026-10-18/LECTURA_Y_CAMBIO_DE_CRITERIO.md`, `MEGAESTRUCTURA_CLAUDE/LEEME.md`, `G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/MEMORIA_TECNICA_Y_RAZON_DE_LA_FORMA.md`, `G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16/LEEME.md`, `TEXTO_INICIAL_USUARIO.txt` y el enunciado (`G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/fuentes/enunciado.txt`).

---

## 1. Errores de método (los que causaron todos los demás)

| # | Qué pasó | Dónde | Regla desde hoy |
|---|---|---|---|
| M1 | **Trabajar desde la imagen lejana.** El conjunto se veía potente y las habitaciones no funcionaban al acercarse (P02: camas que no caben, muebles amontonados, entradas que obligan a esquivar). | Historia §§ 9, 41; carpetas `04_P02_*` | Se empieza por la célula a 1:50 y con el cuerpo dentro. No se dibuja un conjunto con una célula sin validar. |
| M2 | **Multiplicar antes de validar.** Los fallos de una habitación se copiaron en 40 modelos y hubo que señalarlos una y otra vez. | Historia §§ 22, 41; `G3_40_UNIDADES_3D_COTA0` | Primero una célula y una unidad comprobadas de cerca, después las variantes. Cada variante hereda una célula ya validada. |
| M3 | **Corregir homogeneizando.** Para arreglar errores se aplicó la misma habitación a todas: se perdieron el vestidor transitable y la ventana habitable, y las 40 quedaron iguales. | Historia § 23; `G3_CORRECCION_40/LEER_PRIMERO.md` (armario de 55 cm, asiento de 55 cm) | Ninguna corrección puede quitar una prestación vigente. Las variantes tienen que diferenciarse por **cómo se vive**, no por giros o desplazamientos. |
| M4 | **Variantes falsas.** La variante B solía ser la A con un giro o un cambio de tamaño; 40 nombres no eran 40 hipótesis. | Historia §§ 19, 30; `EMPEZAR_AQUI.md` | Cada iteración declara qué forma de convivir pone a prueba y en qué se distingue de las demás. Si no se distingue, no se presenta. |
| M5 | **Geometría válida ≠ arquitectura válida.** Sólidos cerrados, "cero solapes" o un disco que pasa no demuestran que se viva bien. | Historia § 41; `LEER_PRIMERO` de la corrección | Las comprobaciones automáticas se presentan como lo que son (pruebas parciales con alcance declarado) y siempre se revisa el dibujo a ojo, de cerca. |
| M6 | **Autoridad prestada.** "Calculada", "FINAL", cifras con decimales o diagramas de colores parecían justificar cosas que no justificaban; los cálculos de la V4 se usaron para otras geometrías. | Historia §§ 8, 37, 41; memoria V4 | Ningún número viaja de una versión a otra. Todo cálculo se rotula con su geometría y su alcance. |
| M7 | **Ideas convertidas en solución demasiado pronto.** Dormitorios precolocados en las esquinas y luego un "tejido" que los unía; pentágono sin razón. | Historia § 18 | Las posiciones salen de una razón escrita (luz, ruido, agua, acceso), no al revés. |
| M8 | **No acumular las correcciones.** Baños en el centro, cajas delante de la escalera, confusión de giros… volvían en cada generación. | Historia §§ 26, 41 | Esta lista se relee antes de cada entrega y cada regla tiene una comprobación. |
| M9 | **Hablar cuando se pedía hacer, o generar en masa cuando se quería discutir.** | Historia § 39 | "Go / venga / hazlo" = producir. Cuando se discute una habitación, no se genera un catálogo. |
| M10 | **Investigación como repertorio de objetos.** La acampada metió bicis, tendederos y lonas en la casa sin escala ni lugar. | Historia §§ 3, 22 | Cada acción se resuelve a la escala que le toca (célula, casa, grupo, edificio, barrio), con su lugar y su tiempo. |

## 2. Errores concretos de la unidad

| Error | Fuente | Regla / comprobación |
|---|---|---|
| Cama delante de la puerta o cortando la entrada | Historia § 9 | La proyección de la puerta no toca la cama; paso de 0,60 a la cama con el tablero **abierto**. |
| Mesa junto a la puerta (alternativa C) | Historia § 11 | El tablero no se coloca en la llegada. |
| Tablero con patas o "plegable" sin mecanismo | Historia § 11 | Bisagra por el canto corto en la pared, plegado vertical legible, taburete en el lado largo. |
| **Cama + tablero abierto no caben uno al lado del otro** con menos de 3,65 m de ancho (1,25 + 0,60 + 1,80). Muchas habitaciones lo incumplían en uso aunque cupieran plegadas. | Detectado hoy al comprobar | Regla de anchura de 3,65 m o tablero y cama en secuencia, no en paralelo. |
| Vestidor convertido en armario de 55 cm | `CORRECCION_40/LEER_PRIMERO.md`; `EMPEZAR_AQUI.md` | Vestidor en el que se entra: hueco de pie de Ø 1,20 rodeado de ropa. |
| Ventana habitable como panel plano o asiento de 55 cm | Historia § 15; `EMPEZAR_AQUI.md` | Bow pequeña, cóncava por dentro, con el cuerpo sentado en la concavidad; se comprueba en sección. |
| Bow gigante (otra habitación) | Historia § 24 | Bow pequeña: cuerda ≈ 1,7 m, sale ≈ 0,65 m. |
| Cama redonda con plataforma sobredimensionada | Historia § 10 | Colchón sin base mayor; la cama redonda queda descartada si quita el vestidor. |
| Panel expositivo en el dormitorio | Historia § 14 | Se pega en la pared; no hay panel. |
| Baños en isla, en el círculo de convivencia o con la puerta al estar | Historia §§ 12, 26 | Baños en el borde de servicios; la puerta del WC no se ve desde la mesa ni desde el estar (prueba de línea de visión). |
| Sofá de relleno en la entrada | Historia § 32 | No hay sofá salvo que tenga un sitio con razón. |
| Centro vacío llamado "estancia" | Historia § 12 | El común se dibuja con su uso (comer, estar sin cocinar, recibir). |
| Bici y tendedero en medio de la casa | Historia § 22 | Bici y taller a escala de edificio; secar en un recinto ventilado, nunca en el paso ni en el dormitorio. |
| Habitación en medio del estar, sin fachada; ventanas frente a una pared | Historia § 22; diagnóstico B (26 de 36 refugios con fachada vecina a < 4 m) | Cada célula tiene fachada exterior. Se comprueba la distancia al obstáculo más próximo. |
| Puertas en curvas | Historia § 22 | Puertas solo en tramos rectos. |
| Pilar en medio sin razón | Historia §§ 22, 27 | Ningún apoyo dentro de una habitación, un paso o una entrada. |
| Objetos flotando y cubiertas explotadas | Historia § 39 | Todo apoya; las vistas explotadas se rotulan como tales. |
| Instalaciones cruzando ventanas | Historia § 32 | Montantes en el borde de servicios, nunca delante de un hueco. |
| Unidades enormes (208–300 m² para cuatro; cajas de hasta 17 m) | Historia §§ 21, 35 | Presupuesto: **≥ 15 m² útiles por célula** (mínimo normativo, ver § 8) y ≈ 95–110 m² por unidad de cuatro. Se reduce redistribuyendo, nunca encogiendo camas, mesas ni puertas. |
| Habitaciones por debajo del mínimo: N19B reducida con 4 × 12,02 m² | `N19B_REDUCIDA_2026-10-18/G3_N19B_REDUCIDA_A3.pdf` | Ninguna célula por debajo de 15 m² útiles. |
| Reducir a escala para que quepa | Historia § 7 | Prohibido escalar. |
| Simetría global dibujada donde no la hay | Historia § 32 | Solo ejes de referencia o simetría local de la bow. |

## 3. Errores del conjunto y de la parcela

| Error | Fuente | Regla |
|---|---|---|
| Copiar el muro/plataforma del profesor; concentrar toda la verticalidad en un lateral | Historia § 6 | Soporte repartido (troncos), sin un muro dominante. |
| Copiar la silueta de Ruralex o atribuirle atractores | Historia § 16 | Se toma su método (programa, diagrama, estructura, instalaciones, detalle juntos), nunca su forma. |
| Girar el complejo entero cuando se pedía girar unidades | Historia § 36 | Se giran unidades; parcela, planta baja, escalera y ascensor se quedan. |
| Leer mal el frente de parcela (cotas de 20,17 y 49,48 tomadas como fachada) | Historia § 34 | El frente a calle es el lado oeste: **14,98 m**. |
| Vivienda abajo, a oscuras (MEGA B: 24 de 36 refugios sin sol el 21-dic) | `00_LEEME_G3_CLAUDE.md` § 3 | Viviendas por encima de +16/+20 m o justificadas una a una. |
| Primera vivienda a +4,20 sin justificación solar | `HERENCIA_Y_PLANTA_BAJA.md` | La cota de la vivienda sale del estudio de sol, no de la geometría. |
| Caja delante de la escalera; aseos de planta baja sin justificar | Historia § 28 | La descarga de la escalera queda libre; los aseos de planta baja se justifican por ocupación. |
| Telas como decorado (velas no generadas, hypares sin forma) | `MEGAESTRUCTURA_CLAUDE/LEEME.md`; Historia § 37 | Cada tela dice qué ventana protege, quién la acciona, cómo drena y cómo se mantiene. |
| Depósitos y "órganos" inventados | `HERENCIA_Y_PLANTA_BAJA.md` | Ningún depósito sin carga, uso y mantenimiento. |
| Apoyos en voladizo desde la cercha (11 en B, 17 en A) | `MEGAESTRUCTURA_CLAUDE/LEEME.md` | El camino de cargas se dibuja completo hasta la cimentación. |
| Superficie que no cuadra con los ≈ 1.500 m² del enunciado (B: 1.190 útiles; 5 × V01_S ya 1.349 m² sin común) | `MEGAESTRUCTURA_CLAUDE/LEEME.md`; `HERENCIA_Y_PLANTA_BAJA.md` | Cómputo único y con el mismo criterio de medición para todo. |
| El nombre "selva habitada" | Historia § 6 | Se dice **complejo**. |

## 4. Errores de producción gráfica

- Imágenes bonitas de **otra** casa: todo dibujo sale de nuestras plantas y del Rhino (Historia §§ 31, 38).
- Imagen generada usada como plano: lo expresivo es relato; lo técnico es medido (Historia § 31).
- Eslóganes, encabezados tipo etiqueta, estilo garabato y figuras humanas dibujadas en paneles (`00_LEEME_G3_CLAUDE.md` § 5; `CLAUDE.md`).
- Planos técnicos: blanco y negro, Ibarra, corte negro, proyección fina, discontinua sobre el corte, como P01–P06.
- Diagramas: fondo blanco, colores vivos, títulos discretos.

## 5. Lo que ya está hecho y no se rehace

| Ya existe | Dónde | Uso hoy |
|---|---|---|
| Investigación del lugar (compendio de 43 págs., QGIS, megapanel 5×A3) | `G3-FASE1-INVESTIGACION/` | Se cita, no se rehace. |
| Crónica de Sol, testimonios, comisiones, bibliografía de vivienda desmercantilizada | `90_FUENTES_EXTERNAS_APORTADAS/G3_Acampada_Sol_conversacion.md` | Fuente de la parte "roja". |
| Habitantes tipo y presupuesto de 14 m² + 20 m² comunes (1.545 m² para 40) | `G3_E2_PERSONAS_A0_REFINADO_2026-10-06/lectura/base.txt` | Base del presupuesto de la célula. |
| Las 20 acciones y sus 28 relaciones (proximidad, proteger, por turnos, condicional) | `G3_TEJIDO_REGLAS_Y_ALTERNATIVAS_2026-10-18/` | Se analizan para encontrar lo común (eso no se había hecho). |
| Diez organizaciones dibujadas desde las acciones | `G3_ACCIONES_DIBUJADAS_2026-10-20/NUEVAS_ORGANIZACIONES/` | No se repiten esos emparejamientos. |
| 40 + 40 plantas, su atlas y su corrección | `05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/` | Archivo crítico; no se genera otro catálogo de ese tipo. |
| V01 / V02 / V03, E01 / E02 / E03 y los planos 1:100 | `06_…`, `07_…` | Siguen siendo la referencia vigente de la unidad de cuatro; lo nuevo se compara con ellas. |
| Megaestructura original, MEGA A, MEGA B y sus planos 1:200 | `90_FUENTES…/MEGAESTRUCTURA_MACARRA/`, `G3-CLAUDE/03_…` | Se toma su gramática; B ya hizo "refugios colgados de claros": no se repite esa operación sin resolver su luz. |
| V4 con modelo de barras y V5 con luz y planta baja | `G3-CODEX/03_…` | Antecedente; sus números no valen para geometrías nuevas. |
| Programa público de planta baja (biblioteca, estudio-exposición, coworking…) | `07_…/G3_PLANOS_TECNICOS…/verificacion/PROGRAMA_PUBLICO_PB.json` | Se mantiene como hipótesis. |
| Sol por alturas en la parcela | `G3_ESTUDIO_JUSTIFICACION_LUZ_PB…/fuentes/originales/SOL_POR_ALTURA_ESTUDIO_PREVIO.json` | Dato para la sección. |

## 6. Lo que falta de verdad

1. Saber **qué tienen en común** las 20 acciones y convertirlo en el foco de la unidad (pedido hoy; no existe).
2. Una célula con **todas** las prestaciones a 15–16 m² útiles (nunca menos de 15), comprobada en uso (tablero abierto, vestidor, bow, cama, puerta) y en sección. Las V01–V03 las tienen, pero a 18,35 m² geométricos por habitación.
3. Unidades que se diferencien por **forma de convivir**, y más radicales que V01–V03, sin perder prestaciones.
4. La megaestructura releída **en la parcela real** con la luz como regla: vivienda arriba, común abajo, troncos y no muro.
5. Estructura e instalaciones con un camino de cargas y de agua dibujado completo.
6. Lo "rojo", manifestante y generación Z traducido a decisiones espaciales, no a imagen ni a eslogan.
7. **Calendario:** la Entrega 4 (3 de noviembre) pide **cuatro propuestas volumétricas** en maquetas 1:250 de materiales distintos y 2 A3. La Entrega 5 (24 de noviembre) pide estructura, envolvente y lugar.

## 7. Un error que yo mismo iba a cometer hoy

Iba a generar unas 24 plantas de golpe con la célula sin cerrar: eso es M2. Además, al comprobarla vi que con 3,20 m de ancho el tablero abierto cortaba el paso a la cama. Por eso el orden es:

1. célula cerrada y comprobada en uso y en sección;
2. unas pocas unidades que se distingan por forma de vida;
3. solo entonces, las iteraciones y la parcela.

Nota: las células C1–C3 de `fuentes/celula.py` (14,48 / 14,60 / 11,08 m²) son pruebas de paso y **no cumplen** el mínimo de 15 m². No se usan hasta rehacerlas.

## 8. Lo que añadió la revisión completa (25-oct, tarde)

Cada punto lleva su tipo: **dato** (medido o leído de una fuente), **lectura** (interpretación mía) o **corrección** (error mío o de una versión anterior).

### Normativa y parcela

- **Dato.** Madrid, modificación de las NN.UU. de 2023 (coliving): unidad privativa individual ≥ 15 m²; común ≥ 25 m² + 5 m² por unidad adicional; cohousing tipo 2 ≥ 30 m². Fuente: `G3-CLAUDE/02_…/G3_UNIDAD/G3_unidad_v3_memoria.md`. Hay que contrastarlo con el texto oficial antes de entregarlo.
- **Dato.** Vecinos, plantas sobre rasante según el Catastro (`CONTEXTO_CATASTRAL.geojson`; distancias mínimas a la parcela 0134911 medidas hoy):
  - norte, Galerías Piquer 0134901: las partes que tocan la parcela tienen 0–2 plantas; las de 7–10 plantas están a 8,8–11,5 m;
  - sur, 0134910 (1928): 7–8 plantas en la propia medianera;
  - este, 0134912 (obra de 2018): la parte que toca la parcela tiene 0 plantas (patio); las de 7–9 plantas están a 7–11 m.
- **Corrección.** Dije que el vecino norte tenía 1–2 plantas y que el este no tenía edificación. Lo bajo es solo la franja que toca la parcela: a menos de 12 m hay 7–10 plantas al norte y 7–9 al este. La parcela es un pozo con edificios altos por tres lados.
- **Dato.** Sol el 21 de diciembre (`SOL_POR_ALTURA_ESTUDIO_PREVIO.json`, modelo 2,5D con alturas estimadas):
  - porcentaje de la parcela con ≥ 2 h de sol: 16,5 % a +16,4 m; 33,4 % a +19,5 m; 65,2 % a +22,6 m; 100 % a +25,7 m;
  - a +4 m solo llega al 6,7 %.
  - **Lectura:** el 50 % se alcanza hacia +21 m (interpolación lineal).
- **Dato.** E02 girada 90° no cabe en la parcela: 60,9 m² quedan fuera (`G3-CODEX/07_…/verificacion/COMPACTACION_Y_GIRO90.json`). La E02 recta (8 personas) mide 285,9 m² geométricos a +4,20.
- **Dato.** Presupuesto del enunciado: ≈ 1.500 m². Con la «casa común continua» (5 × 8), Centros para convivir da 1.471 m² de envolvente, sin escaleras, zócalo ni estructura. Ya no queda margen.

### Encuesta (34 respuestas, `más investigación…/encuesta/Untitled form-2.csv`)

- **Dato. Quién responde:**
  - 13 tienen 20 años; 28 estudian; 27 viven con su familia;
  - 26 buscan quedarse **más de 3 años**: el usuario real pide estabilidad, no temporalidad.
- **Dato. Qué actividad pide más espacio en casa:**
  - descansar 16;
  - ordenador, estudio o trabajo creativo 12;
  - cocinar 2.
- **Dato. Qué les frustra de su casa:**
  - el **aislamiento acústico, 15 de 34**;
  - la luz natural, 5.
- **Dato. Qué lujo elegirían:**
  - gran ventanal con vistas y luz, 17;
  - terraza o balcón, 11;
  - silencio, 5;
  - muebles flexibles, **1**.
- **Dato. Qué compartirían sí o sí:**
  - azotea o huerto, 30;
  - ocio o estar, 27;
  - lavandería, 22;
  - coworking, 18;
  - cocina y comedor comunitarios, **10**.
- **Dato. Cómo quieren vivir:** 18 prefieren un apartamento privado aunque sea pequeño; 7 prefieren algo compacto con grandes zonas comunes.
- **Lectura. Lo que se dibujó y la encuesta no respalda:**
  - el centro de la casa de cuatro es una cocina-comedor común;
  - el mobiliario es abatible.
  - Lo que sí respalda: descanso protegido del ruido, puesto de trabajo propio, ventana grande y cubierta compartida.

### Las 20 acciones: de dónde vienen

- **Dato.** Las A01–A20 (`G3_TEJIDO_REGLAS_Y_ALTERNATIVAS_2026-10-18/ACCIONES.json`) salen de 16 escenas S01–S16 (`G3_MAPA_ACTIVIDADES_PARCELA_2026-10-18/SITUACIONES.csv`). Las escenas son **inventadas**, como dice el propio Centros para convivir. Su origen declarado:
  - 8 de «hipótesis»;
  - 4 de las comisiones de la acampada;
  - 2 de «lluvia»;
  - 1 de «pulmón»;
  - 1 de «urbanismo».
- **Dato.** Ninguna acción sale de la encuesta. Codex lo advierte («hipótesis de proyecto y no resultados de una encuesta»).
- **Dato.** Las 28 relaciones son:
  - 12 de proximidad, 8 de protección, 4 por turnos y 4 condicionales;
  - en 4 de las 8 de protección lo protegido es **dormir**.
- **Dato.** Cada escena lleva hora (00:40, 01:20, 02:10, 07:15, 22:45…). El atractor más repetido es el descanso, en 6 de 16 escenas.
- **Dato.** Muchas «críticas» de las escenas hablan del derecho a no participar o a retirarse: S05, S06, S08, S09, S13, S16.
- **Lectura. Lo común:**
  - las acciones no son raras, son las de cualquier casa;
  - lo que se repite es el **choque de horarios** (una duerme mientras otra trabaja, cocina o habla);
  - y el **derecho a retirarse sin desaparecer**.
  - La encuesta confirma por otro camino ese mismo conflicto: el ruido es la primera queja y descansar, la primera necesidad.
- **Lectura. Por qué son como son:**
  - A11–A14 (dibujar, maqueta, cortar, coser) describen a un estudiante de arquitectura, que es el autor, no el demográfico medido;
  - A04, A14 y A15 (secar, coser la tela, reparar la bici) vienen de la acampada y de la fachada textil.
  - Es el error M10 repetido.

### Lo que se repitió en las fases 06–07

- **Lectura. Codex, `G3_ACCIONES_DIBUJADAS_2026-10-20`:**
  - las 20 plantas son imágenes generadas, sin escala, con figuras humanas;
  - casi todas son la **misma** organización: fila de 4 dormitorios con bow y vestidor + banda común + baños en un extremo;
  - Codex lo reconoce: «persisten semejanzas… sobre todo las variantes A»;
  - es M3/M4 otra vez.
- **Lectura. Fase 06:**
  - V01–V03 y las cinco uniones repiten el «trébol» de 4 habitaciones;
  - E01–E03 reducen la megaestructura a una caja de unidades sobre pilotes a +4,20 con una escalera exterior;
  - de la gramática macarra (troncos, bandejas, trenza, velas) solo queda la membrana.
- **Dato. Planos 1:100 de Claude (S01–S04):**
  - son secciones de una sola planta de 2,75 m, con figuras humanas del modelo (`PERSONAS.3dm`);
  - **corrección:** en planos se pueden mantener como escala, pero no en paneles;
  - no hay ninguna sección del edificio completo con la vivienda en altura.
- **Dato.** Los errores de los scripts de Rhino (`ERROR_RHINO.txt`, `LAYOUTS_RHINO_ERROR.json`) dejaron las láminas de Rhino sin montar. Los PDF 1:100 se hicieron fuera de Rhino.
- **Dato.** `G3-SIN-ATRIBUIR/99_TEMPORALES` son 36 vistas del «Refugio sonoro», el Taller de Integración de Fundamentos (septiembre de 2026, `REFERENCIAS/Claude outputs/TALLER_INTEGRACION_A3.pdf`). Es el origen estético de los nervios magenta y cian y de las uniones de la megaestructura.
- **Dato.** `98_COPIAS_DUPLICADAS/…/UNIDAD_V5_NORTE_EDITABLE.3dm` es el mismo modelo que el de la carpeta 03 (240 objetos y 35 capas), guardado una vez más.

### Reglas nuevas

- R1. **Corregida el mismo día por Adam.** La encuesta es contexto, no genera la unidad: sus categorías son viejas (apartamento privado, zonas comunes). La unidad sale de **cómo vive la juventud hoy**, contado en muchas escenas (150, no 20), y de lo que esas escenas tienen en común. La radicalidad es de **programa** (qué contiene la unidad), no solo de forma. Referencias que pone Adam: la unidad infinita de Superstudio y la unidad-cama de María Palacios (misma parcela).
- R2. El conflicto que organiza es **horario y acústico**: descanso protegido frente a trabajo, voz y cocina a otras horas. Se comprueba en planta y en sección (separaciones, DB-HR).
- R3. La vivienda va por encima de ≈ +21 m o se justifica hueco a hueco. Abajo va lo común y lo público.
- R4. El mobiliario «flexible» no es un argumento por sí mismo; lo que se invente tiene que venir de una escena.
- R5. La cubierta y el cielo son programa, no un resto.
- R6. Se sigue usando el mismo Rhino para el mismo trabajo, y cada cifra lleva su fuente y su fecha.
- R7. Las 150 escenas y su análisis están en `01_150_ESCENAS.md` y `escenas.csv`. Cada escena lleva su fuente; las que son hipótesis mías van marcadas como tales.

## 9. Lo que dijo Adam el 25-10 por la noche

- Los modelos 3D de `08_UNIDAD_RADICAL` (H1–H6, U1–U5) valen 0/10: cajas, extrusiones y cápsulas generadas por código, no modelado. También los análisis de Claude son flojos. **No se vuelve a producir 3D así.**
- **Regla:** cuando se modele, alimentarse siempre de los archivos de Codex (`G3-CODEX/`): sus Rhino, medidas, verificaciones y plantas. Lo de Claude (`G3-CLAUDE/`) no es base para nada.
- El traspaso a Codex está en `02_PARA_CODEX_150_ESCENAS_Y_LO_COMUN.md`: las 150 escenas con etiquetas, lo común, por qué, el foco, los cuerpos, la parcela y lo que falta.
