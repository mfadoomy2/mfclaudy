# Unidades de cuatro personas — V01 / V02 / V03

Abrir **UNIDADES_4_PERSONAS_TODAS_CON_CUBIERTA.3dm**. Las tres propuestas vigentes están separadas en una fila, sin apilar, con pavimento a Z=0. Unidades del archivo: metros. No incluye las parejas de ocho residentes, el solar ni la planta baja común.

Cada propuesta conserva cuatro dormitorios, vestidores cóncavos transitables, pequeñas bow windows curvas con asiento, camas de 1,25 × 2,00 m, tableros de dibujo de 1,80 × 0,90 m con bisagra por el lado corto, cocina, estancia común y baños en el borde de servicios. Se mantienen materiales y colores.

## Capas y vistas para dibujar

Cada propuesta tiene su capa principal: V01__4_PERSONAS, V02__4_PERSONAS, V03__4_PERSONAS. Apagar las otras dos para trabajar aisladamente.

Vistas guardadas: V01_PLANTA / V01_AXO / V01_ALZADO, y las equivalentes V02 y V03. 00_TODAS_CUBIERTAS muestra el conjunto.

Para una planta interior, apagar dentro de la propuesta las capas 08_COSTILLAS, 09_MEMBRANAS, 10_CABLES, 17_CUBIERTA_TERMICA y 18_LUCERNARIOS. Mantenerlas encendidas para secciones completas y alzados. Las referencias 99_REFERENCIAS_NO_IMPRIMIR están apagadas y no imprimen.

Muros y piezas principales: extrusiones cerradas editables. Cierre común superior: malla cerrada con 12 cm de espesor geométrico. Membrana exterior: superficie textil, por encima del cierre. Techos privados y de servicios: extrusiones cerradas de 14 cm. Los espesores son de estudio y no constituyen una especificación constructiva. La cubierta común es facetada: no es una superficie NURBS lisa. Comprobar las herramientas de extracción de planos sobre una propuesta antes de repetirlas.

Se han completado los antepechos y dinteles de ventanas comunes y el dintel del acceso. Los huecos de las puertas siguen abiertos; las hojas y herrajes de puertas no están desarrollados. No se ha acreditado estanquidad integral, cálculo estructural, normativa ni iluminación solar. Este archivo sirve para desarrollar los dibujos del anteproyecto, no es un modelo ejecutivo.

Superficie geométrica de pavimento: V01 122,70 m²; V02 126,26 m²; V03 117,56 m². Incluye el ámbito común de cada unidad; no equivale a superficie útil normativa.

## Comprobación

Archivo abierto, revisado en vista Rendered y guardado en Rhino 8. 1.383 objetos, sin geometría inválida en la comprobación independiente. Las tres cubiertas comunes tienen malla cerrada. Ver verificacion/CONTROL.json. Se conservan los controles 2D previos de acceso y solapes; no equivalen a una comprobación constructiva completa.
