# Ribera 31 · mecanismos en parcela

Esta revisión contiene diez dibujos de desarrollo, seis vistas geométricas y un esquema de habitantes/programa. Es un cuaderno de hipótesis, no un anteproyecto resuelto. Abrir `ABRIR_GALERIA.html`.

## Cuatro arranques que cambian la organización

| Hipótesis | Operación espacial | Qué redistribuye | Qué habría que resolver |
|---|---|---|---|
| A · Costillas y vacíos | Cuerpos transversales separados por ranuras abiertas al cielo; borde grueso de servicios | Cada grupo accede a una estancia compartida entre cuerpos; las instalaciones dejan de repetirse como pequeños pisos completos | Dimensionar vacíos, luces estructurales, intimidad y protección acústica |
| B · Sección entrelazada | Dos secuencias escalonadas; habitaciones y estancias comunes se relacionan entre niveles | La casa se organiza por relaciones en sección y por ritmos, con accesos propios a lo privado | Continuidad accesible, iluminación y evacuación; el dibujo generado ha alterado los niveles del tanteo |
| C · Dos apoyos | Núcleos permanentes y cuerpos habitados que salvan el suelo común | El terreno estrecho puede recibir un taller, reunión y ayuda vecinal sin atravesar dormitorios | Coste de las grandes luces, sección real de las cerchas y profundidad útil de los apoyos |
| D · Soporte y relevo | Pórticos persistentes y piezas sustituibles; reserva material y acceso de mantenimiento | Los habitantes pueden reparar y modificar el cerramiento interior sin rehacer toda la casa | Compatibilidad de juntas, aislamiento, incendio, gestión del banco de piezas |

**La apuesta más fértil de este cuaderno es combinar C y D como investigación:** liberar una parte del suelo mediante apoyos claros y hacer reparables los componentes domésticos. La habitación bisagra ensaya cómo negociar una estancia común sin perder el cuarto propio. Esa combinación todavía no está dibujada como una quinta volumetría.

## Seis mecanismos de desarrollo

- **Habitación bisagra:** las camas y puertas privadas permanecen. Particiones gruesas cambian estudio, trabajo colectivo y cuidados. Su ámbito de giro se reserva; no invade una puerta ni el recorrido de salida.
- **Condensador de tres estados:** paneles recogidos en bolsillos reales, bancos telescópicos y mesas almacenables. La transformación precisa sitio para guardar lo que se retira.
- **Metabolismo del Rastro:** recibir → revisar → reparar → almacenar → instalar → devolver. El montacargas transporta piezas; no desplaza casas ocupadas. La reutilización no presume automáticamente aptitud estructural.
- **Luz como bien común:** subir a una cubierta compartida, conservar ranuras de cielo y ensayar toldos estacionales. No se atribuyen horas de sol a estas imágenes.
- **Cuerpos y turnos:** sonido y descanso necesitan separación; producir no obliga a vivir permanentemente dentro del taller; participar no obliga a estar siempre disponible.
- **Frente real:** fotomontaje exploratorio colocado sobre la fotografía de FANG Decoración entre el vecino amarillo bajo y el vecino rojo alto. La imagen no es un levantamiento.

## Programa y habitantes

El enunciado original propone aproximadamente 1.500 m² y unas 20 unidades o 40 habitantes; permite discutir el número de unidades. Se ensaya aquí 40 habitaciones individuales, con aseo y comunes contabilizados aparte: **720 m² de ámbito privado y aseo, 440 m² de programa compartido y 340 m² de circulación, estructura y envolvente**. Son áreas de proyecto provisionales. La cabida detallada de las 40 plazas no está comprobada en las cuatro volumetrías.

Los nombres, edades y situaciones de Irene, Laura, Andrea, Jairo, Ariel e Iona se transcriben del MD aportado. El propio documento advierte que son testimonios, no un censo. Las necesidades espaciales asociadas son una interpretación de proyecto. Los cuerpos dibujados son ficticios y no retratan a esas personas. Se evita convertir los turnos de la acampada en camas compartidas obligatoriamente.

La sala común cambia con el horario; la habitación privada permanece. La gobernanza propuesta incluye acceso voluntario a tareas, turnos revisables, protocolos de entrada y relevo, presupuesto común de mantenimiento y un ámbito privado inviolable. La forma arquitectónica, por sí sola, no garantiza la desmercantilización: la tenencia y las reglas de gestión requerirán desarrollo propio.

## Qué es exacto y qué es interpretación

**Vistas 01–06:** proyección numérica del polígono catastral y del OBJ urbano original. Coordenadas locales en metros: X = E − 439984; Y = N − 4473229,4; Z = cota − 622,6. Vecinos extraídos del modelo de 8.291 piezas. Se retira la nave 40028001 bajo la hipótesis de solar libre. Los originales no se modifican. El terreno se simplifica a una cota de referencia: no reproduce la pendiente de la maqueta.

Las huellas nuevas están recortadas por intersección geométrica con la parcela: área fuera de parcela = 0 en las cuatro hipótesis. Esto verifica la implantación horizontal, no la normativa, la estructura ni la habitabilidad. La superficie geométrica del GeoJSON difiere ligeramente de los 651 m² catastrales documentados; ambos valores constan en `geometria/verificacion.json`.

**Dibujos 07–16:** generación con referencias locales mediante image_gen.imagegen. Hay cambios de detalle, proporciones y niveles respecto a la base, especialmente B. No son planos métricos ni detalles constructivos certificados; las cotas o escalas dibujadas por el generador no deben medirse. El botón de comparación permite contrastar cada alternativa con su modelo.

**17:** esquema vectorial de programa, editable en SVG y datos JSON. Suma comprobada: 1.500 m². La división en áreas sigue siendo una decisión proyectual.

Los cuatro tanteos arrojan aproximadamente 1.378, 1.374, 1.487 y 1.534 m² de superficie horizontal bruta esquemática respectivamente. No son cuatro edificios con un programa idéntico ya distribuido. A y B necesitan ampliación o ajuste para aproximarse al objetivo. La altura de 21,1 m del análisis solar previo no se convierte aquí en una altura urbanística autorizada.

## Fuentes que cambian los dibujos

- MD aportado: `/Users/adam/Downloads/G3_Acampada_Sol_conversacion.md`, leído completo. Se usa como investigación proporcionada, no como verificación independiente de las noticias que narra.
- Enunciado: `/Users/adam/Downloads/G3 ESP - LA MATERIA DE LO DOMÉSTICO v3.0.pdf`, nueve páginas.
- Megapanel y guía: `INVESTIGACIÓN/PANEL_FINAL_5xA3/`; parcela y frente: `00_INVESTIGACION_COMPLETA/FIGURAS/F01_parcela.png`, `F13_frente31.jpg`; GeoJSON en `DATOS/DERIVADOS/parcela_31.geojson`.
- Geometría: `/Users/adam/Downloads/01.Centro_3D/_MAQUETA_RASTRO/CENTRO_MADRID_8291_edificios_coord-locales.obj` y documentación `G3_maqueta_Ribera31_proceso.md`.
- Libretas, hilos e ideas del archivo Obsidian: soporte lento/pieza rápida, lujo sensorial, herramientas comunes, economía del Rastro, pertenencia sin permanencia, temporalidades y datos que deciden la sección. Programa de Generación Z leído completo.

### Pinterest de Adam

Lectura visual de una muestra de siete tableros, no una descarga exhaustiva de todos los pines:

- [Machine aesthetics / paper architecture](https://tr.pinterest.com/mfadoomy/machine-aesthetics-paper-architecture/): instrumentos, articulaciones, tensiones y despieces.
- [El poder de la representación](https://tr.pinterest.com/mfadoomy/el-poder-de-la-representaci%C3%B3n/): interferencia entre planta, sección, textura y programa.
- [Formfinding](https://tr.pinterest.com/mfadoomy/formfinding/): sistemas espaciales y modelos de organización.
- [Maquinaria](https://tr.pinterest.com/mfadoomy/maquinaria/): densidad técnica y piezas con función.
- [Composiciones](https://tr.pinterest.com/mfadoomy/composiciones/): trazas, notación, capas y escalas.
- [I.A.RTE.FACTO](https://tr.pinterest.com/mmcchia/iartefacto/): materia, ensamblaje y edición.

Referencias visuales directas conservadas solo como fuentes: [planta/sección HKU](https://tr.pinterest.com/pin/1136877499698383093/) y [notación de Bil Smith](https://tr.pinterest.com/pin/1136877499711867410/). También se inspeccionó [Instrument Eight, Nat Chard](https://tr.pinterest.com/pin/1136877499700090747/). Las propuestas no son obras de esos autores.

- [Buhardilla estudio](https://tr.pinterest.com/mfadoomy/buhardilla-estudio/): membranas domésticas, espacio de estudio y rincones; revisado como contraste final.

### Lecturas arquitectónicas

- [Mori Art Museum · Metabolism](https://www.mori.art.museum/english/contents/metabolism/minute/index.html): relación entre permanencia, cambio y crecimiento. Se traduce aquí en reparación y sustitución de piezas.
- [MoMA · Architectural drawings of the Russian avant-garde](https://www.moma.org/documents/moma_catalogue_2145_300062983.pdf): Melnikov y la transformación de los espacios colectivos. La referencia se toma como una operación de proyecto, no como un repertorio de fachadas.
- [ICOMOS · Soviet Heritage](https://openarchive.icomos.org/3031/1/HR_Special_2006_Soviet_Heritage.pdf): documentación de clubes y espacios colectivos.
- [CCA · Lessons from social condensers](https://www.cca.qc.ca/en/search/details/library/publication/1382525541): lectura de la institución colectiva como generadora de relaciones espaciales.

## Archivos editables

- `geometria/variantes_y_contexto.obj`: contexto y cuatro hipótesis identificadas por nombre; están superpuestas. Activar solo una a la vez. Unidades: metros.
- `geometria/parcela_local.geojson`: huella y origen de coordenadas.
- `geometria/*.svg`: vistas y programa vectoriales.
- `geometria/construir.py`, `programa.py`: fuentes reproducibles.
- `prompts.json`: instrucciones exactas de los diez dibujos generados.
- Los PNG generados son raster; no se presentan como un modelo BIM ni un plano editable por capas.
