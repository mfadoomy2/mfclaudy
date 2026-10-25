# G3 CLAUDE · todo lo hecho, ordenado

**Proyecto:** viviendas temporales para jóvenes en Ribera de Curtidores 31, El Rastro (Madrid). G3 Proyectos, UEM, curso 2026-27.
**Periodo que cubre:** del 21 de septiembre al 21 de octubre de 2026.
**Ordenado el:** 24 de octubre de 2026.

Esta carpeta reúne todo lo que se ha producido trabajando con IA (Claude y, en algunos tramos, Codex y ChatGPT) para G3: cuadernos, láminas, modelos Rhino, scripts, verificaciones e imágenes. Está ordenada por fases, en el orden en que se hicieron, que coincide con las entregas del curso.

Este documento es el índice y el resumen. El relato largo, con todas las decisiones y la guía de cada archivo Rhino, está en **`00_MEMORIA_INTEGRAL_DEL_PROCESO_2026-10-20.md`** (en esta misma carpeta, con las rutas ya actualizadas).

---

## Índice

1. Cómo está ordenada la carpeta
2. El proyecto en una página
3. Cronología completa, fase por fase
4. Decisiones que siguen vigentes
5. Lo que se descartó
6. Lo que queda pendiente
7. Qué abrir para cada cosa
8. Notas guardadas en el proyecto de Claude
9. Lo que no está en esta carpeta
10. Cómo se hizo la reorganización

---

## 1. Cómo está ordenada la carpeta

```
G3 Proyectos/
├── 00_LEEME.md                  índice antiguo de la raíz (septiembre)
├── INVESTIGACIÓN/               Fase 1: investigación urbana, QGIS, paneles (no se ha movido, ver §9)
├── MAPPEADOS/                   mapas propios y modelo del radio de 600 m (no se ha movido)
└── G3 CLAUDE/
    ├── 00_LEEME_G3_CLAUDE.md                          ← este documento
    ├── 00_MEMORIA_INTEGRAL_DEL_PROCESO_2026-10-20.md  relato completo + guía de Rhino
    ├── 01_E2_IMAGINARIOS_PERSONAS_Y_MECANISMOS_05-06oct/   226 MB
    ├── 02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/        289 MB
    ├── 03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/         3,9 GB
    ├── 04_P02_LA_HABITACION_16-18oct/                      117 MB
    ├── 05_ACCIONES_TEJIDOS_Y_40_PLANTAS_18oct/             3,9 GB
    ├── 06_FORMAS_DE_VIVIR_Y_AGRUPACIONES_19oct/            771 MB
    ├── 07_UNIDADES_DE_4_Y_PLANOS_TECNICOS_20oct/           309 MB
    ├── 98_COPIAS_DUPLICADAS/                               572 MB
    ├── 99_TEMPORALES/                                       14 MB
    └── _registro_movimientos_2026-10-24.json      de dónde venía cada carpeta
```

En total: 9,9 GB, unos 3.660 archivos y 469 modelos Rhino.

**Contenido de cada fase**

| Carpeta | Qué hay dentro |
|---|---|
| **01 · E2** | `IMAGINARIOS_G3_2026-10-05` (16 imágenes «la acampada que permanece» + galería) y su zip · `G3_MECANISMOS_EN_PARCELA_2026-10-05` (17 dibujos: cuatro arranques A–D en la parcela) y su zip · `G3_E2_PERSONAS_A0_REFINADO_2026-10-06` (imágenes del A0: carpa-programa, explotadas 2011/2026, edificio programático, objetos y donaciones) |
| **02 · E3** | `MODELOS_ENGEL_p93-94` (tiendas de Engel en Rhino y apiladas) · `G3_ORGANIZACION_PARCELA_2026-10-06` (lámina de organización en parcela + organización vertical para 40) · `G3_UNIDAD` (unidad suspendida v1 a v5) · `G3_CONJUNTO` (8 agrupaciones) · `G3_REVISION_2026-10-08` (revisión: módulo dúplex D, módulo de una planta S, conjunto 32/40) · `ATLAS_PABELLONES_2026-10-08 (antes output)` |
| **03 · Megaestructura** | `G3_SOL_SELVA_2026-10-11` (cuaderno de 15 págs.) · `MEGAESTRUCTURA_CLAUDE` (megaestructura A libre y B en Ribera 31, vistas, texturas) · `G3_SELVA_HABITADA_V2` (+zip) · `G3_SELVA_RADICAL_RHINO_V3` · `G3_SELVA_MACARRA_V4_CALCULADA` · `G3_UNIDAD_AISLADA_DETALLE` (P02) · `G3_ESTUDIO_JUSTIFICACION_LUZ_PB` (+zip de documentación) · `MEGAESTRUCTURA_MACARRA_PLANOS_2026-10-20` (planos 1:200 de la megaestructura de referencia) |
| **04 · P02** | Siete carpetas `G3_P02_*` y cinco zips: habitación curva, plantas y secciones (tres plantas × seis/nueve secciones), versión A revisada, unidad orgánica, modelo de planta completa, corrección de apoyos, materiales y texturas |
| **05 · Acciones y 40** | `G3_REFERENCIAS_RURALEX_COCINA` · `G3_MAPA_ACTIVIDADES_PARCELA` (+zip) · `G3_UNIDAD_TEJIDO_ACTIVIDADES` (+zip) · `G3_TEJIDO_REGLAS_Y_ALTERNATIVAS` (+zip) · `G3_ATLAS_40_PLANTAS` · `G3_40_PLANTAS_DESDE_TEJIDOS` · `G3_TEJIDOS_A_PLANTA_40` · `G3_80_PLANTAS_2026-10-18.zip` · `G3_40_UNIDADES_3D_COTA0` (incluye `N19B_REDUCIDA_2026-10-18`) · `G3_CORRECCION_40` |
| **06 · Formas de vivir** | `G3_DECIDIR_UNIDAD_PARCELA` · `G3_PLANTAS_FORMAS_DE_VIVIR` (+zip) · `G3_UNIONES_COMUNAS` (+zip) · `G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS` · `G3_CENTROS_PARA_CONVIVIR` · `G3_CONTINUIDAD_PARCELA` · `G3_MODELOS_HERENCIA_MACARRA` (V01/V02/V03, E01/E02/E03) |
| **07 · Planos** | `G3_UNIDADES_4_PERSONAS` · `G3_ACCIONES_DIBUJADAS` · `G3_PLANOS_TECNICOS` (planos 1:100, secciones, compactación y giro, E02 recta) · `G3_RHINO_EN_VIVO` (script que lista los Rhino abiertos) |
| **98 · Duplicados** | Las cuatro carpetas que acababan en « 2». Son casi idénticas a su original (ver §10). |
| **99 · Temporales** | `_tmp_prev`: 36 vistas previas `rs-01…rs-36.png` del 19-10. |

---

## 2. El proyecto en una página

**El encargo.** Edificio de viviendas temporales para jóvenes de unos 1.500 m², con unas 20 unidades o 40 habitantes y los espacios comunes necesarios. Anteproyecto con desarrollos de estructura, envolvente, energía y sistemas. Escalas 1:500, 1:200, 1:100 y 1:50. Maqueta 1:250. Tres fases y seis entregas, más dossier A3 y dos paneles A1 finales.

**La parcela.** Catastro 0134911VK4703C. Solar sin edificar de unos 651 m², 49,5 m de fondo y un frente a la calle de 14,98 m. Entre 10 y 20 m de ancho. La calle baja un 7 % (≈ 1,1 m de desnivel en el frente). Cota de la calle ≈ 622,6–622,9 m.

| Dato de la parcela | Valor | Consecuencia |
|---|---|---|
| Medianera sur | +22 m de media, +28,2 como máximo | Es la que quita el sol |
| Sol de invierno (21-dic) | 0,1 h a +1,5 m · 1,7 h a +19,5 · 4,0 h a +22,5 · todo el día desde +28,5 | Por debajo de +16 m el invierno casi no tiene sol |
| Ruido | Isófonas MER 2021 sobre el eje de la calle; el 46 % de la encuesta sufre ruido en casa | El silencio es un lujo |
| Domingo | 651 puestos en Ribera de 2.186 en el Rastro (29,8 %) | La calle vive en dos estados |

**El habitante.** Juventud de clase obrera que va a vivir en Madrid. El sueldo medio joven es de 1.191 €/mes; el 30 % son 357 €, que en Lavapiés-Embajadores (25,5–25,7 €/m²) alquilan unos 14 m². Una habitación en Madrid cuesta entre 575 y 689 €. De cada 40 jóvenes, 19 trabajan y 15 de ellos en servicios, a turnos. El 50,2 % de las personas de 25 a 34 años vive con sus padres. Fuentes en §8.

**La tesis (septiembre).** En Ribera 31 el sol, el silencio y el espacio son escasos y el mercado los reparte por renta. El proyecto los reparte en común, en un edificio que no se puede trocear para especular. Temporal quiere decir que la gente rota, no que el derecho sea precario.

**La referencia política (octubre).** La acampada por la vivienda de Sol de 2026: cómo se organiza (calles con nombre, comisiones, asamblea, cocina común, lonas) y qué de eso se puede llevar a un edificio. No como imagen, sino como forma de repartir el espacio, los recursos y el mantenimiento.

**La forma.** Una arquitectura macarra, radical, entrelazada, con telas, cruces y recorridos que se convierten en lugares, sostenida con distribución, medidas, estructura y detalle. El edificio se llama **complejo** (el nombre «selva habitada» se descartó; solo queda en nombres de carpetas).

---

## 3. Cronología completa

### Septiembre · Fase 1 (fuera de esta carpeta, en `INVESTIGACIÓN/`)

- **21–24 sep · Investigación urbana.** Se revisó y consolidó el trabajo previo hecho con Codex en un único compendio de 43 páginas: contexto urbano, recorrido de Street View (23 panorámicas, 11 registros históricos del n.º 31), censo de 42 frentes, Catastro en GML y GeoJSON (EPSG:25830), QGIS, inventario físico de 600 m, patrones de calle P01–P11, sol por alturas. Niveles de certeza: **A** medido, **B** inferido, **C** hipótesis.
- **23 sep · Cerebro de proyectos en Obsidian.** Bóveda `CEREBRO DE PROYECTOS` dentro de `/Volumes/T7/obsidian/creATIveb@bY/`.
- **24 sep · Megapanel 5×A3 y panel A1** del grupo. Material extra: «Home Alone», tipologías del Rastro, encuesta de 34 voces, panel económico del m².
- **25 sep · Corrección de la Fase 1.** Pregunta del jurado: «¿para qué sirve todo esto?». Respuesta adoptada: cada bloque en tres tiempos, **dato → lectura → decisión**.
- **26 sep · Tesis, hilos e ideas.** 12 hilos (habitante real, vivienda como activo, temporal no es precario, lujo común, casa-taller, el domingo como modelo, trabajar con el vacío, arquitectura a la malicia, hablar como se habla ahora, argumentario, preguntas abiertas). De 832 reels guardados y transcritos salieron 16 ideas y un argumento («difícil partición», «el intermediario se queda la diferencia», «internet no tiene bancos», «quien tiene la altura tiene el poder»…).
- **26 sep · Generación Z.** 1.080 publicaciones guardadas (848 reels, 195 carruseles, 37 fotos) clasificadas en 11 dimensiones. Retrato en diez rasgos y un programa de 14 espacios comunes + célula de ≈ 14 m², con unos 1.450–1.550 m² de tanteo.
- **27–29 sep · Maqueta 1:250.** 8.291 edificios del Geoportal y MDT de 5 m del IGN montados en Rhino con origen local (X 439984,0 · Y 4473229,4). Solución final: A3, seis placas de metacrilato de 4 mm cortadas a láser (curvas 622 a 630 m) y ocho piezas de edificios impresas en 3D que encajan en huecos. Los archivos de la maqueta estaban en `Downloads/01.Centro_3D/_MAQUETA_RASTRO/` (ver §9).

### 01 · 4–6 de octubre · Entrega 2: las personas, la plaza y cómo lo resuelven

- **Imaginarios (5-oct).** 16 imágenes generadas con Codex: corrala insumisa, calle en el aire, el sol es común, casa inacabable, cocina-parlamento, derecho a cerrar, domingo, cuidados, casa-taller, fachada, acero, madera, ladrillo, hormigón, pertenecer, la acampada permanece. Con un cuaderno de conexiones y tres «motores» para empezar.
- **Mecanismos en parcela (5-oct).** Cuatro arranques: A costillas y vacíos · B sección entrelazada · C dos apoyos · D soporte y relevo. Diez dibujos, seis vistas geométricas y un esquema de habitantes y programa.
- **Paneles E2 (4–6 oct).** Panel 5×A3 de personas, plaza y tácticas; A0 y libreta A4 con 47 fuentes numeradas; A3 de juventud y vivienda con 24 fuentes; A3 de técnicas de la acampada a partir de 25 publicaciones de TikTok e Instagram. Diez conclusiones, entre ellas:
  - Quien vivirá aquí trabaja, muchas veces a turnos.
  - Por m², la habitación cuesta entre 1,9 y 3,8 veces el piso entero.
  - La acampada vivió con 6,6 m² de plaza por tienda: menos que un dormitorio legal, porque todo lo demás era común.
  - Lo común se dibuja primero (calles con cinta y nombre); las tiendas se colocan después.
  - Lo temporal es la gente que rota; lo que dura es la organización.
- **A0 refinado (6-oct).** Imágenes de la carpa-programa, las explotadas 2011 y 2026 y los objetos y donaciones.

### 02 · 6–8 de octubre · Entrega 3: la unidad y su agrupación

- **Corrección del 6-oct** (audio transcrito). Lo que se pidió: explicar cómo se habita («mi casa es…»), definir qué es fijo y qué se mueve, entender cómo funciona sola una unidad antes de agruparla, y no perder de vista el análisis.
- **La unidad y la carpa (6-oct).** «Mi casa es una tienda dentro de una carpa.» Retícula de 1,20 m (palé europeo), plaza de 2,40 × 6,00 = 14,4 m², carpas de 10 personas, cuatro carpas en altura, planta común a +19,20 y azotea por encima del sol de invierno. Estructura leída en Engel. Del soviético (Narkomfin) se coge el gradiente de colectivización y se deja la comuna impuesta.
- **Organización en la parcela (6-oct).** Lectura del tablero de Pinterest «organización» (14 pines) y de las tensadas de Engel (pp. 67, 72–73, 88–89, 93, 95, 97–107). Propuesta v1: dos mástiles de celosía, 40 cápsulas, redes comunes por planta y carpa a +21.
- **Organización vertical para 40 (6-oct).** Tu lista: espacio grande para cada uno, comunes para trabajar, unidades suspendidas de verdad unidas por miniescaleras de 2–3 escalones, terraza y minijardín, doble altura, «nada formal». Tanteo: anillo A de 8 posiciones + línea B de 4, 42 módulos, ≈ 1.460 m², y genes para Galápagos.
- **Engel pp. 93–94** modeladas en Rhino y apiladas sobre la parcela.
- **Unidad v3 (7-oct).** 32 unidades de unos 30 m² (24 individuales + 8 dobles = 40 personas). Cerramiento de bloque de vidrio Seves 1919/8 ES (U = 1,4), retícula de 200 mm, escalera de caracol verificada con DB SUA, barreras, miniescalera de 3 peldaños. Variantes A (balcón) y B (porche bajo el estudio).
- **Unidad v5 (8-oct).** Siete variantes: dos ventanas (guillotina o corredera exterior), tres escaleras (lineal con estantería, caracol bajo el altillo, unidad + 1 crujía) y dos «fuera del cubo». La favorita fue la **F2: esquina curva y ala semicircular**.
- **Conjunto: 8 agrupaciones (8-oct).** A estantería · B peine en desfase · C apilado cruzado · D racimos de cuatro · E linterna · F andamio con cápsulas · G muro habitado y plaza desplegable · H síntesis. B fue la única con todas las unidades con 6,7 m libres o más delante; G, la que más suelo dio al barrio (422 m² de plaza). Todas pedían 5 niveles (34–37 m).
- **Revisión (8-oct).** «La unidad no es todavía el vecindario»: se estaba repitiendo una casa autónoma y uniéndola con plataformas. Propuesta: diseñar a la vez el ámbito propio, el umbral y la casa de grupo. Módulo dúplex D, módulo de una planta S y conjunto de 32/40.

### 03 · 11–16 de octubre · La megaestructura macarra

- **Giro del 11-oct.** Los profesores no quieren la unidad anterior («casa de los Sims»). Nueva dirección: una megaestructura radical y casi ilegible desde fuera (contra la gentrificación y el reconocimiento), con estructura e instalaciones vistas, ligada a Sol, con telas que tengan sentido estructural.
- **Cuaderno Sol → selva (11-oct).** 15 páginas con fuentes primarias de Acampada26S y del Sindicato de Inquilinas; separa observaciones de hipótesis.
- **Megaestructura A (libre) y B (en Ribera 31, 1:1).** B tiene 36 refugios.
- **Diagnóstico de luz de B (12-oct).** El 21 de diciembre, 24 de los 36 refugios no reciben sol directo; 17 no llegan al mínimo de la UNE-EN 17037 en marzo; 26 tienen una fachada vecina a menos de 4 m. Conclusión: la vivienda tiene que ir por encima de +18/+20 m y lo de abajo debe ser común o planta abierta al Rastro.
- **V2 (16-oct).** Unidad U4 para cuatro personas (≈ 11,30 × 9,20 m, ≈ 103 m² brutos, habitaciones de ≈ 12 m²) y diez unidades en la parcela. 13 láminas y guion de exposición.
- **V3.** Versión radical modelada en Rhino.
- **V4 «calculada».** Diez pabellones para 40 residentes sobre tres grupos de soportes ramificados, con ascensores y escaleras. Modelo elástico lineal preliminar de barras y detalles de nudo, bandeja y ascensor. No es una estructura certificada, y sus cálculos no sirven para los modelos posteriores.
- **P02 aislada.** Se extrajo una unidad de la V4 para verla de cerca.
- **Justificación de luz y planta baja.** Dossier de 18 páginas.
- **Planos de la megaestructura de referencia (20-oct).** 20 láminas 1:200: 6 troncos (T00–T05) con sus cotas y 28 bandejas (E00–E27) entre +2,0 y unos +49 m, con sus superficies.

### 04 · 16–18 de octubre · P02: el cuerpo y el mobiliario

Al acercarse a la P02 aparecieron camas mal encajadas, muebles junto a las puertas, piezas flotando y tamaños incoherentes. Se probaron camas redondas, armarios cóncavos, mesas de dibujo plegables, ventanas habitables y slabs de carga junto a la cama. Series: habitación curva, tres plantas × seis y × nueve secciones, versión A revisada, unidad orgánica, planta completa, corrección de apoyos (nada flotando) y materiales y texturas.

### 05 · 18 de octubre · Acciones, tejidos y las 40 plantas

- **Ruralex y cocina.** Ruralex se estudió como relación entre programa, diagrama, estructura, instalaciones y detalle. **Cambio de método:** dejar de decidir primero la silueta y empezar por acciones, objetos, cuerpos, proximidades, conflictos, tiempos y recorridos.
- **Mapa de actividades y parcela.** Situaciones, red de atractores, conflictos y reglas, parcela real sin el complejo.
- **20 acciones** (A01 dormir … A20 guardar herramientas) con lo que pide cada una al espacio. Tejido general, cruces que producen lugares, tiempos de mañana, tarde y noche, calibración corporal. Se rechazaron el pentágono sin fundamento y los cuatro retiros puestos de antemano.
- **40 plantas desde tejidos** (20 propuestas × 2 variantes; hechas con otra IA). Atlas de 48 págs., segunda serie, 80 plantas y catálogo 3D a cota 0.
- **Lectura y elección (Claude).** Las plantas salían de 208–260 m² en el PDF y de 258–326 m² en el 3D: 10 pisos daban 2.600–3.000 m². Ranking: 1 **N19B** (cuatro retiros dispersos), 2 N07B, 3 N03B. Se eligió N19B como base.
- **N19B reducida.** Racimo para 4 de 11,10 × 10,80 m (119,9 m² construidos, 103,8 útiles), habitaciones de 12,02 m², dos racimos por planta con un núcleo-mástil entre ellos, 1.654,9 m² en total. Comprobado dentro del Catastro, con vistas (art. 582 CC), evacuación y escalera.
- **Corrección de las 40.** Se rehicieron con cuatro habitaciones con ventana exterior, accesos rectos y colchones rectangulares (≈ 113 m² y dormitorios de 16,36 m²). **Error reconocido:** se perdieron el vestidor transitable y la ventana habitable, y las 40 quedaron demasiado parecidas.

### 06 · 19 de octubre · Formas de vivir y agrupaciones

- **Decidir unidad y parcela.** Diagnóstico de la homogeneización.
- **V01 / V02 / V03.** Recuperan el vestidor y la ventana. V01: continuidad · V02: dos ámbitos desplazados (prometedora) · V03: alrededor de un centro. La ventana pasa a ser una **bow pequeña y curva para sentarse**.
- **Uniones comunas** (agrupaciones de ocho): umbral compartido, encuentro, continuidad.
- **Documento de plantas nuevas corregidas** (47 págs.; el mismo PDF que está en el proyecto de Claude). Reglas: nada de baños como isla en el centro.
- **Centros para convivir** (30 págs.) y **continuidad y prueba en la parcela** (52 págs.).
- **Herencia macarra.** Ocho organizaciones en 3D y tres ensayos sobre la parcela: **E01 Encuentro**, **E02 Comuna** (elegida para documentar) y **E03 Dos claros**. Bandejas, soportes ramificados, membranas, escalera, ascensor y planta baja.

### 07 · 20–21 de octubre · Unidades de cuatro y planos técnicos

- **Tres unidades de cuatro** juntas en un Rhino con cubierta, a Z = 0.
- **Acciones dibujadas.** Ensayo de dibujo expresivo en blanco y negro sobre plantas reales. Son relato, no documentación métrica.
- **Planos técnicos 1:100** medidos desde Rhino: P01 V01, P02 V02, P03 V03, P04 E02 elevado, P05/P06 planta baja diaria y de domingo, y secciones S01–S04. Ibarra Real Nova, negro en corte, sin color.
- **Planta baja pública** (E02): biblioteca de 53,05 m², sala de estudio y exposición de domingo de 67,09 m², coworking, cocina y comedor, reparación y costura, punto vecinal, fuente y plaza.
- **Después de la memoria del 20-oct** (no recogido en ella):
  - **Compactación y giro de 90°.** V01 se queda en 122,7 m²; V02 pasa de 126,3 a 121,5 m²; V03 pasa de 117,6 a 121,1 m². Ninguna tiene todavía todas las habitaciones a la calle. **E02 girada no cabe**: quedan 60,9 m² fuera de la parcela; haría falta recomponerla.
  - **E02 recta, habitaciones a la calle** (tu petición del 20-oct): 285,86 m² de pavimento, 13 puertas, 14 ventanas, camas de 1,25 × 2,00 y tableros de 1,80 × 0,90. Planta baja de 650,93 m² con un frente de 14,98 m.
  - **Paquete `ENTREGA_PLANOS_1_100`** con planos, secciones y el Rhino compactado.

---

## 4. Decisiones que siguen vigentes

- Radicalidad constante, siempre con razones de uso y construcción.
- El complejo como red de relaciones, no un apilamiento repetido.
- Habitación propia para cada residente y derecho a retirarse.
- Vestidor cóncavo transitable y bow pequeña con asiento.
- Tablero de dibujo de 1,80 × 0,90 abatible por el canto corto, sin patas fijas. Cama de 1,25 × 2,00.
- Puertas que no choquen con la cama ni con el armario; acceso fluido.
- Baños en el borde de servicios: ni isla central ni caja delante de la escalera.
- Telas con función climática y espacial.
- Planta baja unida al conjunto y al barrio, con dos estados: diario y domingo.
- Mantener las diferencias entre V01, V02 y V03.
- Planos técnicos en blanco y negro y medidos; el dibujo expresivo, aparte, como relato.
- Todo debe cumplir el CTE y argumentarse con criterio técnico.

## 5. Lo que se descartó

Copiar literalmente el muro y la plataforma del profesor · copiar la silueta de Ruralex · el pentágono y los cuatro retiros precolocados · el nombre «selva habitada» · cubiertas y objetos flotando · bici y tendedero en medio de la casa · habitaciones sin fachada · camas que cortan la entrada · la ventana habitable como simple panel · el panel expositivo en los dormitorios · baños en isla · el sofá como relleno de la entrada · presentar las 40 parecidas como 40 propuestas distintas · usar los cálculos de una versión para justificar otra · la unidad tipo «casa de los Sims» · las escaleras plegables · el jardín encima de cada unidad · las frases tipo eslogan y los encabezados en los paneles · el estilo «garabato» y las figuras humanas dibujadas.

## 6. Lo que queda pendiente

1. Revisar el tamaño de las unidades (sobre todo V02) con el frente real de ≈ 15 m, sin reducir camas, mesas ni puertas para que quepa.
2. Recomponer E02 para que quepa en la parcela con las habitaciones a la calle.
3. Comprobar entrada, pasos, giro, vestidor, mesa abierta y plegada y bow, en planta y en sección.
4. Agregación de dos unidades con luz y entradas reales.
5. Luz: viviendas por encima de +16/+20 m o justificación de las que queden por debajo.
6. Estructura, uniones, cimentación, membranas, drenaje y mantenimiento de la geometría elegida.
7. Normativa: altura y fondo del Centro Histórico; figura legal (vivienda compartida o coliving); DB SI, SUA, HE y HS; accesibilidad.
8. Sincronizar el 3D, los planos, las cotas y los layouts (el Rhino de layouts no tiene la última cota del frente).
9. Elegir qué ensayos cuentan el argumento de la entrega y cuáles quedan como archivo.

---

## 7. Qué abrir para cada cosa

Rutas desde `G3 CLAUDE/`.

| Para… | Abrir |
|---|---|
| Entender todo el proceso | `00_MEMORIA_INTEGRAL_DEL_PROCESO_2026-10-20.md` |
| Ver los imaginarios | `01_…/IMAGINARIOS_G3_2026-10-05/ABRIR_GALERIA.html` |
| Los cuatro mecanismos | `01_…/G3_MECANISMOS_EN_PARCELA_2026-10-05/ABRIR_GALERIA.html` |
| Organización en parcela y vertical | `02_…/G3_ORGANIZACION_PARCELA_2026-10-06/*.pdf` |
| Unidad suspendida (F2) | `02_…/G3_UNIDAD/G3_unidad_suspendida.3dm` · memorias v3 y v5 |
| Las 8 agrupaciones | `02_…/G3_CONJUNTO/G3_conjunto_opciones.3dm` |
| Acampada → proyecto | `03_…/G3_SOL_SELVA_2026-10-11/CUADERNO_SOL_SELVA.pdf` |
| Megaestructura en Ribera | `03_…/MEGAESTRUCTURA_CLAUDE/MEGA_B_RIBERA31_1a1.3dm` |
| V4 en la parcela | `03_…/G3_SELVA_MACARRA_V4_CALCULADA_2026-10-16/modelos/SELVA_MACARRA_V4_EN_PARCELA.3dm` |
| Luz y planta baja | `03_…/G3_ESTUDIO_JUSTIFICACION_LUZ_PB_2026-10-16/output/pdf/DOSSIER_G3_JUSTIFICACION_LUZ_Y_PLANTA_BAJA.pdf` |
| Planos de la megaestructura | `03_…/MEGAESTRUCTURA_MACARRA_PLANOS_2026-10-20/G3_MEGAESTRUCTURA_MACARRA_PLANOS_1_200.pdf` |
| Las 20 acciones | `05_…/G3_TEJIDO_REGLAS_Y_ALTERNATIVAS_2026-10-18/ACCIONES_PARA_DISCUTIR.md` |
| Atlas de las 40 | `05_…/G3_ATLAS_40_PLANTAS_2026-10-18/output/pdf/G3_40_PLANTAS_ATLAS_A3.pdf` |
| N19B reducida | `05_…/G3_40_UNIDADES_3D_COTA0_2026-10-18/N19B_REDUCIDA_2026-10-18/` |
| Plantas nuevas corregidas | `06_…/G3_DOCUMENTO_PLANTAS_NUEVAS_CORREGIDAS_2026-10-19/output/pdf/G3_PLANTAS_NUEVAS_Y_DIAGRAMAS_CORREGIDOS.pdf` |
| V01/V02/V03 y E01/E02/E03 | `06_…/G3_MODELOS_HERENCIA_MACARRA_2026-10-19/modelos/` |
| Las tres unidades de cuatro | `07_…/G3_UNIDADES_4_PERSONAS_2026-10-20/UNIDADES_4_PERSONAS_TODAS_CON_CUBIERTA.3dm` |
| **Planos 1:100 actuales** | `07_…/G3_PLANOS_TECNICOS_2026-10-20/ENTREGA_PLANOS_1_100/` |
| E02 recta, habitaciones a la calle | `07_…/G3_PLANOS_TECNICOS_2026-10-20/planos_E02_recta/` · `modelos/E02_RECTA_HABITACIONES_A_LA_CALLE.3dm` |
| Layouts editables 1:100 | `07_…/G3_PLANOS_TECNICOS_2026-10-20/modelos/PLANOS_EDITABLES_Y_LAYOUTS_1_100.3dm` |

Casi todas las carpetas tienen su propio `LEEME.md`, `LEER_PRIMERO.md` o `EMPEZAR_AQUI.md` con el detalle.

---

## 8. Notas guardadas en el proyecto de Claude

Estas notas están en el proyecto **G3 PROYECTOS** de Claude (carpeta `claude/`), no en el disco. Se resumen arriba; el texto completo con todas las fuentes está allí.

| Fecha | Nota |
|---|---|
| 26-sep | Tesis e hilos · Argumento e ideas · Generación Z y programa · Pendiente de volcar a Obsidian (Atocha, Covibar, libreta 02) |
| 29-sep | Maqueta 1:250 Ribera 31 · proceso |
| 6-oct | E2 personas, plaza y tácticas (28 fuentes) · E2 A0 y libreta (47 fuentes, 10 conclusiones) · E2 A3 juventud y vivienda (24 fuentes) · E2 técnicas de la acampada (25 publicaciones) · Transcripción de la corrección del 6-oct · E3 la unidad y la carpa · Organización en la parcela · Organización vertical para 40 |
| 7–8 oct | Unidad v3 · Unidad v5 · Conjunto: 8 agrupaciones |
| 12-oct | Megaestructura B · diagnóstico de luz |
| 18-oct | 40 plantas desde tejidos · lectura y elección · N19B reducida |
| — | Engel, *Sistemas de estructuras* · texto por página (referencia) · `G3_PLANTAS_NUEVAS_Y_DIAGRAMAS_CORREGIDOS.pdf` |

---

## 9. Lo que no está en esta carpeta

- **`INVESTIGACIÓN/` y `MAPPEADOS/`** se quedan en la raíz de `G3 Proyectos`. Son la base de la Fase 1, mezclan trabajo del grupo y mapas propios, y los proyectos QGIS se enlazan entre sí por rutas relativas (`MAPPEADOS/INVENTARIO_FISICO_600M.qgz` lee `../INVESTIGACIÓN/…`). Si se mueven las dos juntas a la misma carpeta, siguen funcionando.
- **Bóveda de Obsidian:** `/Volumes/T7/obsidian/creATIveb@bY/CEREBRO DE PROYECTOS/`.
- **Maqueta 1:250:** sus archivos estaban en `Downloads/01.Centro_3D/_MAQUETA_RASTRO/`. Esa carpeta de Descargas está ahora vacía; si se movió a otro sitio, no está en `G3 Proyectos`.
- **Referencias fuera:** `PERSONAS.3dm` en la raíz del T7; `MEGAESTRUCTURA_MACARRA.3dm` original en `Downloads/MEGAESTRUCTURA_MACARRA/`.
- **Láminas PDF/PSD de la Entrega 2** (A0, A3 de juventud, A3 de técnicas, panel 5×A3): no están en el T7. Sus fuentes sí están en las notas del proyecto de Claude.

---

## 10. Cómo se hizo la reorganización

- Se **movieron** 66 carpetas, zips y archivos desde la raíz de `G3 Proyectos` (65) más la memoria integral, que se ha renombrado `00_MEMORIA_INTEGRAL…`. No se ha copiado ni borrado nada. La lista exacta de origen y destino está en `_registro_movimientos_2026-10-24.json`.
- Carpetas renombradas: `output` → `ATLAS_PABELLONES_2026-10-08 (antes output)`; `G3_MEMORIA_INTEGRAL_DEL_PROCESO_2026-10-20.md` → `00_MEMORIA_INTEGRAL_DEL_PROCESO_2026-10-20.md`.
- **Rutas actualizadas:** 617 rutas absolutas en 76 archivos `.md`, `.py`, `.html` y `.txt` (la memoria integral y los scripts) apuntan ya a la nueva ubicación. Las 27 rutas de la guía de Rhino de la memoria se han comprobado una a una y abren. Los `.json` de verificación no se han tocado: son registros de lo que se hizo y conservan las rutas originales.
- **Duplicados** (`98_COPIAS_DUPLICADAS`):
  - `…LUZ_PB… 2`: el Rhino `UNIDAD_V5_NORTE_EDITABLE.3dm` es distinto del original y le falta `verificacion/paginas`.
  - `…MAPA_ACTIVIDADES… 2`: le falta `CONTACTO_REVISION.jpg`.
  - `…TEJIDO_REGLAS… 2`: le falta `CONTACTO.jpg`.
  - `…UNIDAD_TEJIDO_ACTIVIDADES… 2`: idéntica al original.
  - Se pueden borrar cuando quieras; antes, comprueba cuál de los dos Rhino de la V5 norte quieres conservar.
- En la raíz quedan archivos ocultos `._*` de macOS (metadatos del disco T7). No se ven en el Finder y no molestan.
- Si algún Rhino de estas carpetas estaba abierto mientras se movía, ciérralo y vuelve a abrirlo desde su nueva ubicación antes de guardar.
