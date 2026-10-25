# DECISIONES DE FASE 01
Registro razonado. Ninguna decisión se ha tomado en silencio.

**D1 — La planta 2D es la fuente de verdad; el 3D deriva de ella.** `geometria_maestra.json` (1 u = 1 m, origen lat 40.41690 / lon −3.70350, +X este, +Y norte) alimenta la planta SVG, el OBJ y la axonometría. Cualquier corrección se hace en el generador, nunca en los derivados.

**D2 — El contexto es el Sol REAL post-2023 (OSM, ODbL).** La cenital 0F53E6F0 se generó sobre una foto aérea antigua: muestra las dos fuentes pre-reforma y calzada con tráfico. El Sol actual no tiene fuentes; los "claros conservados" se asignan a Carlos III, Mariblanca, Km 0, bocas de metro/Cercanías y cruces peatonales históricos.

**D3 — Orden de clústeres del dibujo matriz (gran anillo al OESTE).** 0F53E6F0 es sur-arriba (el reloj cae al 54 % desde la izquierda ⇒ izquierda = este) y la IA conservó el orden izquierda-derecha del dibujo, dejando esa única imagen en espejo E-O. Se adopta la convención norte-arriba del dibujo matriz y de las 4 referencias cenitales restantes. Además funciona mejor: el clúster mayor (C2) cae en la zona más ancha de la plaza.

**D4 — Materialidad unificada para la base:** estructura tubular clara (blanco-crema/turquesa en representación) con acentos de cobre en la red hidráulica; hinchables como familia única "cápsula neumática rosa" (subtipos esfera/píldora/toro). Las referencias oscilan entre bambú, acero blanco, cobre y cromo según iteración: la decisión es REPRESENTACIONAL, no constructiva (form-finding y material real → Fase 02).

**D5 — Estratos verticales:** suelo público continuo / dosel +5–10 m / cinta +4–6 m / infraestructura +10–12 m. Fuente: sección 12069BE7 + cota "altura máxima 10 m" de las láminas técnicas del linaje portuario.

**D6 — Posiciones inferidas (G3):** LAB 02 (borde NE de C3), cúpula geodésica (nudo central-este), depósitos elevados (3 grupos en puntos altos), splash pad (claro central sur de C2), red hidráulica principal. Ninguna referencia los sitúa en el Sol real.

**D7 — Cinta única.** Las referencias muestran a veces pasarela peatonal (~4–6 m) y a veces carril logístico (~8–10 m). Se modela UNA cinta-recorrido continua G2; el desdoblamiento (si procede) se estudiará en Fase 02.

**D8 — Densidad de dosel no dimensionada.** Discos+balsas = 1.890 m² (17 % de la plaza). El dimensionado real de sombra será salida de los estudios solares/UTCI de Fase 02; los discos son componentes reposicionables.

**D9 — Paleta anclada a muestras.** Cada color de `paleta.json` cita su fuente (k-means global + muestreo dirigido por regiones). Scripts reproducibles en `02_SISTEMA_GRAFICO/paleta/`.

**D10 — Formatos:** P01 a 1:500 en A1 apaisado con columna técnica de 150 mm; P02 en axonometría militar 32° (planta verdadera, alturas reales, sin explosión: la comprensión no la necesitaba).

**D11 — `Maqueta/` (escultura-reloj) queda FUERA de Fase 01.** Es un flujo de trabajo activo e independiente (modificado el mismo día de esta auditoría); relación probable con el proyecto por el motivo del reloj, pero no es geometría del Refugio. No se ha tocado.

**D12 — Rasgos de iteración excluidos:** helipuertos y raíl recto inferior (HR11), pasarela diagonal única (8F526890), muelle con barcos (HR08), lámina de mar (HR12), campo de burbujas sin dosel (237EAF1C), emplazamiento portuario de las láminas técnicas. Registrados como variantes D; sus SISTEMAS (leyenda de componentes) sí se heredan.

**D13 — Duplicados:** `AFB4423F… (1).png` y `F295448F… (1).png` son copias exactas; se ignoran (no se borran).

**D14 — Régimen MAXIMALISTA de representación (revisión del autor, 2026-08-07).** El primer P01 se juzgó "plano bonito pero no iraxxxdios": demasiado limpio, contexto parcelado que parecía interior de edificios, cinta como tubito. Se adopta el régimen maximalista para las láminas de planta: zoom 1:300 con la plaza llenando el campo; contexto como costra tramada a 45° sin divisiones interiores; loops como haz de 3 anillos con traviesas c/2 m, nudos y redes tensadas; cinta de doble carril con traviesas y **coordenadas reales x y +z cosidas al trazado**; discos como mallas radiales; cápsulas con gajos y válvula; enjambre de micro-cotas rosas con **distancias reales**; cadena de cotas perimetral con borde-muralla y ticks; vegetación en garabato + campos de puntos; vapor en espiral + halo punteado; figuras, vencejos y libélulas; bloques de nota flotantes con líder. Paleta y certezas G1–G4 del manual SIN cambios: el desorden es de densidad, no de sistema. Toda cifra dibujada sale de `geometria_maestra.json` (punk pero honesto). v1 archivada en `_archivo_v1\`. P02 y futuras láminas de Fase 02 adoptarán este régimen cuando el autor valide P01 v2.
