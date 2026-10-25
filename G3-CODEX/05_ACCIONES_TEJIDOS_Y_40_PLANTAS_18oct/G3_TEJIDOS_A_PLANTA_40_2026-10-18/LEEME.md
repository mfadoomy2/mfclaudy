# Segunda serie · Del tejido a 40 plantas

20 propuestas con dos variantes cada una, **adicionales** a la primera serie de 40. Se conservan separadas. Punto de partida: los tres diagramas del estudio `G3_TEJIDO_REGLAS_Y_ALTERNATIVAS_2026-10-18`, cuyos JSON se copian sin modificar a `datos/FUENTE_*`.

## Abrir

- `output/pdf/G3_40_PLANTAS_DESDE_TEJIDOS_A3.pdf`: diagrama original, traslación y planta para cada alternativa, con índice, método y comparación.
- `plantas/N01A_PLANTA.svg` a `N20B_PLANTA.svg`: 40 planos gráficos editables completos. También 40 PNG.
- `plantas/*_TRAZA.*`: 40 parejas de diagrama y transformación, en PNG y SVG.
- `plantas/*_PROGRAMA.png`: 40 mapas adicionales de usos sobre el suelo.
- `modelos/*_PLANTA_2D.3dm`: 40 bases de contornos 2D en metros, Z=0, con el centro de su envolvente en XY=0. No contienen arquitectura en 3D ni todos los símbolos del SVG. Comprobación por relectura con rhino3dm; no comprobación nativa visual en Rhino.
- `datos/COMPARACION.csv`: superficies y desplazamientos desde anclajes. `*_ACCIONES_UBICADAS.json`: coordenadas de las distintas localizaciones de cada acción.
- `verificacion/`: informes y páginas renderizadas. `fuentes/`: scripts completos.

## Cómo se ha hecho y qué no demuestra

Los puntos de los tejidos 1–3 son anclajes espaciales, convertidos desde una retícula sin metros mediante una hipótesis de 0,94 m por paso y deformaciones declaradas en el código. Los veinte ensayos cambian esa deformación y el ajuste; A/B cambia colchón y algunas proporciones de las huellas. **No son veinte grafos nuevos ni veinte hipótesis sociales independientes.**

Cuatro espacios privados comienzan en los anclajes A01, A06, A10 y A11. Esa repetición es una decisión nueva: dormir, vestirse, guardar, entrevista y dibujar se repiten en las cuatro habitaciones. No se pretende que una habitación sea sólo de entrevista o sólo de dibujo. Cada una contiene el mismo programa privado.

Las huellas se separan elásticamente para impedir solapes. Se usa una holgura conservadora de 2 m entre cajas: permite buscar rutas pero gasta suelo. El trazado de conexiones usa una malla de 0,27 m y un ancho nominal de 1,20 m. Las marcas rosas en las trazas muestran desplazamientos entre el anclaje y la huella ajustada. Se añaden enlaces físicos para que el suelo sea continuo. **Las líneas de conflicto PROTEGER no se convierten automáticamente en pasillos.** Las relaciones acústicas y visuales no están resueltas por este trazado.

Cocinar/comer, ducharse/secar y el enlace entre trabajo y herramientas se representan como relaciones funcionales. Cortar/coser comparten apoyo por turnos; llegar/recibir/salir comparten umbral. La bicicleta se representa en la reserva de reparación. El tendido tiene reserva propia; capacidad y ventilación no están calculadas. Los restantes equipamientos y filtros son hipótesis de proyecto.

Las habitaciones conservan la base geométrica de la primera serie para mantener dimensiones de camas y mesas comparables. Por tanto, la novedad principal es la **organización a partir del campo de acciones**, no cuarenta muebles distintos. Mesa de dibujo 1,80 × 0,90 m, articulada por el canto corto; herraje y bloqueo sin dimensionar. No hay pedestal mayor que el colchón ni panel independiente para proyectos. El nicho cóncavo no acredita un vestidor transitable.

## Resultado crítico

La traducción produce mucho recorrido y supera ampliamente la superficie disponible si se repite para cuarenta residentes. **No hay una vivienda final seleccionada o declarada apta.** El resultado muestra por qué un diagrama de relaciones no puede construirse literalmente sin consolidar acciones y convertir algunos cruces en estancia. No se utiliza una silueta de Ruralex como generador.

Las áreas son suelo geométrico conceptual, sin espesores de paredes, estructura, ni servicios generales. No existe implantación en parcela, orientación cardinal ni cálculo de iluminación. Las ventanas y textiles son propuestas sin validar; tampoco se resuelve la ventana habitable. Los baños equipados son reservas que exigen integración posterior en cerramientos y filtros visuales.

Se verifica continuidad del suelo, ausencia de solapes entre espacios privados y colisiones cama/mesa/armario, además de una prueba parcial de asociación de las cuatro aproximaciones a puertas a una componente libre. Esto **no verifica** accesibilidad, evacuación, puerta exterior, maniobras completas, aislamiento, instalaciones ni cálculo estructural. El 4/4 no debe presentarse como una certificación reglamentaria.

La cocina se dibuja con equipamiento genérico; no se ha descargado ni importado el modelo de 3D Warehouse.

## Relación entre acciones y lugares

A01 dormir, A02 vestirse y A05 guardar ropa → cuatro habitaciones. A06 entrevista y A11 dibujar → cuatro mesas privadas por horarios. A10 hablar en privado → habitación disponible con acuerdo de acceso; no hay consulta independiente. A03 ducharse → B1/B2. A04 secar → D. A07 cocinar y A19 recoger → K. A08 comer → M. A09 conversar en grupo → S. A12 guardar maqueta, A13 cortar y A14 coser → T, con almacenamiento por resolver. A15 reparar bicicleta y A20 guardar herramientas → R. A16 llegar, A17 recibir y A18 salir → E.

Las acciones son hipótesis del proyecto a partir del trabajo previo, no conductas observadas de toda la generación Z. Una acción puede ocupar varios lugares y un lugar puede admitir varias acciones. Las copias de documentos de referencia son fuentes, no instrucciones del usuario.
