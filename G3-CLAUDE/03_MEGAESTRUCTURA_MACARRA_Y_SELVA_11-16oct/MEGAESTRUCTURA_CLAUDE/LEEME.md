# MEGAESTRUCTURA · G3 · Claude

Dos modelos Rhino (metros, Rhino 7/8):

- **MEGA_B_RIBERA31_1a1.3dm**: la megaestructura en la parcela de Ribera de Curtidores 31, a escala real. Usa las coordenadas locales del modelo del Centro: origen en el eje de la calle frente al n.º 31 (UTM 439984,0 / 4473229,4) y Z absoluta (plaza a +622,90). Incluye el contexto real (edificios del Geoportal y MDT 5 m del IGN). Se puede pegar encima de `CENTRO_MADRID_3D_terreno.3dm` y encaja.
- **MEGA_A_LIBRE.3dm**: la versión por libre, sin parcela. Tres fustes y la trenza subiendo en espiral triple.

Las texturas están en `texturas/`. Los materiales apuntan a `/Volumes/T7/G3 Proyectos/G3 CLAUDE/03_MEGAESTRUCTURA_MACARRA_Y_SELVA_11-16oct/MEGAESTRUCTURA_CLAUDE/texturas`. Las imágenes `vista_*.png` son vistas previas rápidas, no un render de Rhino.

## La idea

La acampada de Sol funcionaba con **tiendas** (lo íntimo) bajo **toldos y carpas** (lo común), unidas por **calles y claros**, y con la organización a la vista: comisiones, comedor Pulmón, cuidados, plan de lluvia. La megaestructura traslada eso a un edificio sin fachada.

- **Fustes de hueso** (estructura y servicios). Cada fuste es una lámina perforada que se abre abajo en una **raíz-cueva** (comedor Pulmón y asamblea en A, taller en B) y arriba en una trompeta con mástil y trípode. Por dentro sube el ascensor (hueco de vidrio). Por fuera suben los haces de instalaciones: magenta para energía y datos, cian para agua.
- **Claros**: plataformas comunes en medios niveles alternos de +2,10 m, con tablero de madera, cercha perimetral amarilla y viguetas al collar del fuste. Cada comuna tiene en su claro el núcleo húmedo pegado al fuste, la cocina y la mesa común.
- **Trenza**: escaleras que saltan de un fuste al otro cruzando el vacío, con galerías cubiertas por membrana sobre arcos donde caben.
- **Refugios-tienda**: la nueva unidad, que sustituye a la «casa de los Sims». Es la tienda de Sol hecha permanente. Cuelga fuera del claro, a 0 / ±2 / ±3 peldaños, y se llega por su propia pasarela. Va en dos bloques editables:
  - individual: 4,40 × 3,30 m
  - doble: 6,20 × 3,30 m

  Sus capas, de dentro a fuera:
  1. suelo de madera sobre cuna de acero;
  2. piel de policarbonato celular de 40 mm, aislante y translúcida;
  3. **célula de hueso perforada**, que es la estructura (celdas pequeñas abajo por rigidez, grandes arriba por luz);
  4. sobretecho de lona tensada sobre la cumbrera, con cables de alero (cámara ventilada, como una tienda de verdad).

  La puerta da al claro y el ventanal a la vista. La sección crece de la puerta (baja y estrecha) al ventanal (alta y ancha).
- **Carpa colectiva** arriba. Hay una tienda de punto alto por fuste (Engel p. 93): el anillo cuelga del mástil y los anclajes van a mástiles cortos con tornapunta. Entre fustes, una tienda central cuelga de un **cable portante** tendido entre las cabezas de mástil. Las retenidas van al lado opuesto. Las formas se han hallado **por densidad de fuerzas** (equilibrio real): doble curvatura anticlástica y cables de borde con flecha. No son superficies dibujadas a mano.
- **Agua** (la lógica de la referencia de los vasos y goteos): punto bajo de cada membrana → cadena de lluvia → bajante cian → **aljibes enterrados** entre las raíces, con óculos de vidrio en la plaza. Bajo algunas comunas cuelga una ampolla de vidrio que alimenta por gravedad los inodoros del núcleo de la comuna de abajo (solo han cabido 1 en B y 6 en A).
- **Raíces**: el fuste se abre bajo la plaza en 7-9 raíces de hueso, que acaban en encepados amarillos con 4 micropilotes hasta −9 m.

Cada carga tiene su camino hasta el suelo:

> tablero → cercha → rama de hueso, péndola o puntal → fuste → raíz → micropilotes

**Por qué no se lee desde fuera.** No hay plantas tipo, ni ventanas repetidas, ni fachada: cada refugio tiene su cota, su giro y su vista, y la envolvente es la suma de lonas, hueso, cables y membranas. Es la idea de que lo que no se puede encasillar tampoco se puede reconocer automáticamente.

Aviso honesto (también lo dice el cuaderno): la forma por sí sola no frena un desalojo. Eso lo hacen la tenencia (cooperativa en cesión de uso) y las reglas contra la especulación.

## Modelo B en números (comprobados sobre el modelo)

- **Residentes:** 41 en 34 refugios de comuna, más 1 refugio de invitados y 2 de cuidados y estudio. En total, 29 individuales y 7 dobles. Las comunas son de 3 a 7 personas.
- **Superficies:** refugios ≈ 564 m², claros ≈ 512 m², núcleos ≈ 41 m², cuevas ≈ 71 m². Total útil ≈ 1.190 m², más la trenza, las pasarelas y la plaza cubierta. El enunciado pide ≈ 1.500 m² construidos.
- **Alturas:** último claro a +23,10. Los mástiles llegan a +36,50 (la medianera sur está a +25,8 / +28,5).
- **Escaleras:** criterios CTE DB SUA 1.
  - contrahuella 0,175, huella 0,28, 2C+H = 0,63;
  - tramos de 12 (2,10 m) como máximo;
  - ancho libre 1,20 m, barandilla 1,10 m de malla inox.

  De la plaza al primer claro hay 24 peldaños en dos tramos con meseta de 1,20.
- **Accesibilidad:** ascensor en cada fuste, con parada en todos sus claros. En cada comuna hay un refugio enrasado con el claro.
- **Vistas:** ventanas a 2 m o más de linderos que no dan a la calle, y vistas oblicuas a 0,60 m o más (art. 582 del Código Civil). Cada refugio tiene al menos 3 m de vista libre.
- **Comprobaciones automáticas de choques** entre claros, refugios, escaleras con su gálibo de 2,20 m, núcleos, velas y ampollas. El detalle está en `verificacion_B.json`.

**Pendiente** (lo dice el propio JSON):
- algunos apoyos se quedan en voladizo desde la cercha (11 en B y 17 en A);
- las velas (hypares de 4 puntos sobre los claros) no se han generado en esta versión, así que la capa `09_VELAS` está vacía en los dos modelos;
- la superficie útil de B (≈ 1.190 m²) queda por debajo de los ≈ 1.500 m² del enunciado;
- en un par de claros no cabe la mesa o la cocina;
- la normativa de altura del casco histórico;
- el cálculo estructural real, que no se ha hecho.

## Modelo A (libre) en números

- **Fustes:** tres, a 29,4 / 26,1 / 22,8 m, con mástiles hasta +40.
- **Claros:** 14, desfasados 1,05 m entre fustes. La trenza sube en espiral triple: 13 escaleras de 6, 12 y 18 contrahuellas.
- **Refugios:** 42 refugios con 47 plazas (33 individuales y 9 dobles).
- **Superficies:** claros ≈ 824 m² y refugios ≈ 663 m². Total útil ≈ 1.690 m².
- **Abajo:** las raíces de los tres fustes rodean el estanque común (agua «flor de la vida»).

El detalle está en `verificacion_A.json`.

## Capas

- `00_CONTEXTO` (sólo B)
- `01_FUSTES` (hueso y raíces)
- `02_ASCENSORES`
- `02_ESTRUCTURA` (péndolas, puntales, tirantes)
- `03_CLAROS`
- `04_REFUGIOS` (bloques `REFUGIO_INDIVIDUAL` y `REFUGIO_DOBLE`, más los accesos)
- `05_NUCLEOS_HUMEDOS`
- `06_TRENZA`
- `07_PLANTA_BAJA`
- `08_CARPA_COLECTIVA`
- `09_VELAS`
- `10_AGUA`
- `10_INSTALACIONES`
- `11_ROTULOS`

Hay vistas guardadas en cada archivo.
