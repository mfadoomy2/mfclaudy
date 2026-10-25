# G3 · 40 unidades corregidas · 18 octubre 2026

Abrir **CATALOGO_40_CORREGIDAS_COTA0.3dm**. Contiene 40 alternativas separadas en XY, sin apilarlas, con el suelo acabado a Z=0. Cada código tiene una raíz de capas y una vista nombrada. Hay 40 archivos independientes y una habitación aislada para inspeccionar el detalle.

## Qué se ha corregido

- Se reconstruye la distribución de las 40 alternativas, conservando los códigos y usando las posiciones del tejido de actividades como guía de orientación. Las restricciones de tamaño, acceso y frente exterior modifican sus contornos. Son alternativas nuevas de la serie; no son una reducción uniforme de los archivos anteriores.
- Huella interior geométrica: **112,86–113,72 m²**. Envolvente de estudio: **122,18–123,61 m²**. La primera mide el polígono de planta; incluye el lugar de las divisiones interiores y no debe confundirse con superficie útil normativa. La segunda añade 12 cm perimetrales. El pequeño rellano exterior se modela aparte.
- Cuatro habitaciones por unidad, de **16,36 m² geométricos cada una**, incluyendo almacenaje y mirador. Colchones de **1,25 × 2,00 m**, con apoyo de la misma huella. Se retira la cama circular en esta versión para reducir tamaño y liberar el acceso.
- La cama queda al lado opuesto de la puerta. La proyección del hueco de 1,00 m no intersecta el colchón. La mesa queda en el lateral de la entrada y el armario cóncavo se desplaza al lado del recorrido junto a la cama.
- Puertas de dormitorio de **1,00 m** sobre tramos rectos, con hojas correderas aparcadas al lado del hueco. No se colocan las jambas sobre una curva.
- Mesa de dibujo nominal **1,80 × 0,90 m**, inclinada 12°, con bisagra por el canto corto, dos puntales murales y sin patas al suelo. El taburete se muestra aparcado parcialmente bajo la mesa. La aproximación de uso se comprueba por separado. El estado plegado se guarda en una capa oculta; es una representación alternativa, no una simulación completa del mecanismo.
- Armario cóncavo de profundidad máxima 55 cm, con costados, estantes y barra; dos slabs metálicos y toma USB junto a la cama. Los anclajes son una propuesta geométrica, no un producto industrial certificado.
- Ventana exterior en los **160 dormitorios**, con cajón a suelo y asiento de **2,10 × 0,55 m**. La tela se recoge fuera de la ventana y cuelga de carril, anillas y ménsulas; no aparece como una cortina arbitraria en el paso interior.
- Al menos dos ventanas exteriores en el espacio común de cada unidad. Hay huecos reales en el muro a la altura de la carpintería.
- Estar y cocina en un espacio continuo, mesa común para cuatro, sofá y cocina equipada. Se eliminan bicicleta, mesa de reparación y tendedero como objetos permanentes dentro de la vivienda. El eventual programa colectivo de reparación y lavandería debe resolverse en el complejo.
- Dos baños agrupados, conectados al cerramiento y a un retorno que protege sus puertas. Plato enrasado, WC a suelo, lavabo compacto **400 × 350 mm** y hojas telescópicas abiertas. Se mantiene un paso al vestíbulo de baños por el lado del retorno.
- Acceso principal de **1,20 m** en frente recto, puerta abierta hacia el rellano exterior y plataforma a Z=0. No se introduce un soporte aislado en el centro de la vivienda.
- Cubiertas en su posición de proyecto, ocultas por capas para inspeccionar el interior. No se representan piezas explotadas flotando encima de las unidades.

## Qué se ha comprobado

Los archivos JSON de `verificacion/` contienen los resultados por código, no una afirmación genérica de que todo funciona.

1. Geometría válida, sólidos cerrados y límites verticales en los archivos 3DM.
2. Comprobación nativa de los volúmenes esperados de las extrusiones. La validez de un sólido por sí sola no detecta todos los errores en huecos.
3. Conexión de la entrada con los cuatro accesos privados mediante un disco de 90 cm, descontando paredes y muebles comunes.
4. Conexión de cinco aproximaciones de uso en cada habitación mediante un disco de 80 cm, descontando cama, mesa, almacenaje, asiento y taburete aparcado. Se comprueba la aproximación de uso de la mesa, aunque el taburete se representa guardado.
5. Aproximaciones a lavabo, WC y ducha mediante disco de 80 cm en los dos baños de cada unidad. El ensayo usa los muebles compactos efectivamente modelados.
6. Frente recto de las puertas y cama fuera de la proyección del acceso. Cero superposición de habitaciones entre sí.
7. Franja exterior despejada delante de cada ventana privada, hasta aproximadamente 6 m desde su fachada, dentro de la unidad aislada. Para ventanas comunes se comprueba una franja de 3 m.
8. Capturas nativas superiores y axonométricas de los 40 modelos, y una habitación aislada. En las vistas superiores se ocultan temporalmente los remates de muro y dinteles para leer las entradas; esos elementos permanecen modelados en los 3DM. Los PNG de Rhino muestran la geometría entregada. Los planos SVG son dibujos derivados de esa misma planta.

Estos ensayos tienen una escala y unos puntos de uso definidos. No simulan todos los movimientos del cuerpo, la apertura de cada electrodoméstico ni todos los estados simultáneos del mobiliario.

## Escala del complejo

Se mantiene la hipótesis de **10 viviendas de 4 personas = 40 residentes**. Diez envolventes de esta serie suman aproximadamente 1.230 m². Frente a la hipótesis previa de 1.500 m², queda una bolsa aproximada de 270 m² para estudiar accesos, estructura y otros espacios. Esa resta es un presupuesto inicial, no demuestra que el conjunto quepa en la parcela. No se decide aquí que una unidad equivalga a una planta entera.

La organización se ha compactado alrededor de un espacio común continuo. Los dormitorios buscan perímetro exterior, y las separaciones y giros siguen la orientación de los puntos de actividad hasta donde permiten los pasos y las fachadas. La distribución de cocina y servicios A/B cambia de lado. N19B estudia un ajuste angular adicional de 12° para evitar coincidir con otra alternativa.

## Alcance que sigue abierto

Esta entrega corrige las unidades aisladas. **No acredita asoleo, iluminación natural suficiente ni ventilación de un edificio implantado en la parcela.** Falta estudiar medianeras, unidades vecinas, orientación real y sección del conjunto. Las vistas sin cubierta no son simulaciones de luz.

Tampoco incluye un cálculo estructural, definición ejecutiva de forjado y envolvente, instalaciones completas, comprobación del enunciado ni justificación normativa de accesibilidad o evacuación. Los espesores de muros, cubierta y suelo son reservas de estudio. No se entrega como proyecto listo para construir.

## Archivos y reproducción

- `CATALOGO_40_CORREGIDAS_COTA0.3dm`: catálogo con vistas por código.
- `modelos/`: 40 viviendas independientes con vistas cercanas y materiales.
- `HABITACION_CORREGIDA.3dm`: habitación aislada con los mismos muebles y medidas.
- `vistas/`: plantas, axonometrías, planos PNG/SVG y hojas de contacto.
- `datos/SUPERFICIES.csv`: magnitudes medidas por unidad.
- `datos/GEOMETRIA_CORREGIDA.pkl`: geometría 2D exacta usada para el modelo y la comprobación.
- `datos/FUENTE_40_ANTERIOR.pkl`: copia del dato geométrico anterior para conservar la procedencia.
- `fuentes/`: scripts de geometría, modelado, planos, captura y catálogo. El modelo puede reconstruirse desde el pickle corregido con `modelar.py`. Necesita Python 3.11, rhino3dm, shapely y numpy; los planos también necesitan matplotlib. Los scripts de revisión nativa requieren Rhino.

Las curvas y sólidos de los 3DM son editables. Materiales y colores son de visualización; no se han aplicado texturas fotográficas ni se han importado los modelos de Ruralex o de 3D Warehouse. El archivo PERSONAS.3dm y los originales anteriores se conservan.
