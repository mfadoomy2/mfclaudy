# Pabellón de bambú: reconstrucción 3D a partir de una imagen de referencia

Carpeta de trabajo del 26 y 27 de octubre de 2026. Es un ejercicio aparte del proyecto G3; no forma parte
de la documentación de la vivienda de Ribera de Curtidores.

La fuente principal es `referencia.png` (render fotográfico de un pabellón orgánico de haces de bambú,
piezas perforadas marfil, paneles translúcidos rojo y ámbar y cubierta de membrana tensada, en un bosque
húmedo). Todo lo que no se ve en esa imagen es hipótesis y está separado en capas propias.

## Archivos

| Archivo | Qué es |
|---|---|
| `PABELLON_BAMBU.3dm` | Modelo Rhino 8. Metros. 1083 objetos, 20 definiciones de bloque, 17,3 MB. |
| `tex_*.png` | Texturas procedurales (bambú, marfil, vidrio rojo, vidrio ámbar, membrana, tarima, banco, agua, suelo con musgo, corteza). Tienen que quedarse junto al `.3dm`: los materiales las referencian por nombre de archivo. |
| `referencia.png` | Imagen de referencia. Se usa como plano frente a la cámara `01_Referencia` (capa 00, apagada) y para la superposición. |
| `generar_pabellon_bambu.py` | Script que genera todo con `rhino3dm`, `numpy`, `scipy`, `pillow` y `matplotlib`, sin Rhino. Tarda unos 2,5 minutos. |
| `vista_01_general.png` | Vista desde la cámara equivalente a la referencia. |
| `superposicion_referencia.png` | La misma vista al 55 % sobre la foto, para comprobar silueta, picos, acceso y reparto de colores. |
| `vista_02_interior.png` | Vista interior hacia el fondo izquierdo. |
| `vista_03_estructura.png` | Vista aérea con membranas y entorno ocultos. |
| `dimensiones_estimadas.json` | Dimensiones del modelo generadas por el script. |

Las vistas de comprobación son del propio script (pintor por profundidad, sin texturas ni transparencia
real). Sirven para verificar geometría y proporciones, no son renders. Las líneas finas del terreno son un
artefacto del dibujo.

## Sistema de referencia y escala

- X: izquierda a derecha de la fachada principal. Y: profundidad desde el acceso hacia el interior. Z: altura.
- Origen: centro del acceso principal a cota de pavimento.
- Parámetro maestro `ANCHO_TOTAL = 10,0 m`. Todas las dimensiones derivan del factor `S = ANCHO_TOTAL / 10`,
  así que la escala global se cambia en una línea sin alterar proporciones ni organización.
- Cámara de referencia: posición (0,30, −8,20, 1,95), objetivo (0,00, 2,00, 1,70), lente equivalente 30 mm,
  encuadre con la proporción de la imagen (1491 × 1055). Está guardada como vista con nombre `01_Referencia`.
  Se ajustó en dos iteraciones por superposición con la foto.

## Dimensiones estimadas (hipótesis de trabajo, no medidas verificadas)

| Magnitud | Valor | Cómo se obtuvo |
|---|---|---|
| Anchura total de la estructura (X) | 10,2 m | parámetro maestro + abombamiento derecho |
| Profundidad (Y) | 6,5 m | proporción en planta estimada; el fondo no es visible |
| Altura del anillo superior | 3,3 a 3,8 m (media 3,55) | más alto a la izquierda, baja hacia la derecha, como en la foto |
| Altura máxima (remates de mástil) | 4,9 m | picos ajustados a la superposición |
| Cubierta de membrana | 6,7 × 4,4 m, 0,8 m de desnivel entre picos y valles | relajación entre bordes y picos |
| Acceso central | 3,2 m de anchura entre pies, 3,1 m de altura libre | comparación con los bancos y la tarima |
| Cañas | Ø 64 a 96 mm (media 80), nudos cada 27 a 36 cm, conicidad 8 % | rango provisional del encargo |
| Haces | 3 a 8 cañas; radio de haz 4 a 9 cm | según lo visible en cada familia |
| Piezas perforadas | espesor 30 mm, 2033 agujeros de Ø 4 a 19 cm, canto achaflanado 6 mm | hipótesis 20 a 40 mm |
| Tarima | tablas de 14 cm, junta 12 mm, 4 cm de canto, cota +0,12 m | despiece real por tablas |
| Bancos | asiento a 0,45 m sobre tarima, 0,51 m de fondo (3 tablas), pies cada 1,1 m | referencia ergonómica del encargo |
| Elemento de agua | Ø 1,24 m, borde a 0,55 m, lámina de agua a 0,50 m | proporción con el acceso |
| Apoyos | 41 bases: placa 34 × 34 cm, casquillo 32 cm, 4 pernos, cartelas | ensamblaje visible en la foto, detalle propuesto |
| Anclajes de vientos | a 2,2 m fuera del perímetro, 8 unidades | hipótesis |

Los valores exactos del modelo están en `dimensiones_estimadas.json` (el campo `ancho_total_X_m` de ese
archivo incluye los anclajes de los vientos; la anchura de la estructura es la de la tabla).

## Qué es observado, qué es estimado y qué es propuesto

Observado en la imagen y reconstruido (capas 01 a 14, mitad delantera, ángulos 158° a 28° de la planta):
- Anillo superior continuo que desciende de izquierda a derecha y haz paralelo que baja hasta el suelo por
  la derecha (familia A).
- Gran acceso central irregular con arco exterior, banda exterior, arco interior retranqueado 0,55 m y cinco
  riostras entre ambos, que dan espesor real al marco (familia B).
- Anillo grande de la izquierda, hueco de la derecha y sus bandas rojas concéntricas; lente roja vertical del
  extremo derecho; celdas ámbar alta izquierda y centro derecha (familia C).
- Carriles de base curvos entre apoyos (familia D), montantes cortos agrupados en cada pie de arco o pilar
  (familia E) y cañas sueltas que subdividen los paños (familia F).
- Ocho mástiles con remate esférico y orejeta, vientos a anclajes, cables entre picos y cordón de borde.
- Tarima de madera, banco sinuoso de la derecha y tramo parcial de la izquierda, pila circular con agua y
  recipiente translúcido suspendido con prolongación estrecha hacia abajo.
- Dos piezas circulares metálicas y caja gris con soporte en el lateral derecho; dos tiras magenta.

Estimado: todas las dimensiones (tabla anterior), la forma exacta de cada celda (elipses irregulares con
armónicos y asimetría controlada) y la posición de la cámara.

Propuesto para zonas no visibles (capa `16_Elementos_ocultos_propuestos`, con subcapas del mismo nombre que
las observadas): arco trasero, dos anillos traseros, celdas ámbar del fondo, banco del fondo, costillas,
abrazaderas, apoyos y cables de la mitad posterior. Continúan las mismas familias sin reflejar la fachada.
La subcapa `Cimentacion_propuesta` (apagada) contiene una zapata de 60 × 60 × 40 cm bajo cada apoyo: es una
hipótesis gráfica, no un cálculo.

## Organización del modelo

Capas 00 a 16 tal como se pidieron. Cada haz tiene su curva de eje NURBS en `01_Curvas_maestras` (nombre de
familia y elemento) y cada caña es un objeto propio con nombre (`B_arco_acceso cana 3`, etc.).

Bloques (instancias), 546 colocadas: abrazadera por radio de haz (banda, dos orejetas, tornillos y tuercas),
apoyo por radio de haz (placa, casquillo, banda de cierre, pernos, cartelas), remate de mástil, tensor con
dos anillas y tuercas, anclaje de viento, pie de banco, grapa de panel, zapata propuesta. Editar la
definición del bloque actualiza todas las instancias.

Materiales (uno por objeto, con parámetros físicos de rugosidad, metalicidad y opacidad además del color
básico): bambú dorado satinado con nudos y vetas en la textura, marfil mate con porosidad fina
(etiquetado como interpretación de compuesto mineral), rojo rubí y ámbar translúcidos con red oscura de
filamentos en la textura (material no verificado), membrana transparente blanquecina, acero gris plateado,
tarima húmeda, banco, madera oscura, agua con ondas, cable, LED magenta emisivo, vidrio, suelo con musgo,
corteza. Las coordenadas de textura están baked en las mallas: la veta sigue la longitud de cañas y tablas
(una tesela de bambú = 1,32 m = 4 nudos).

Vistas con nombre: `01_Referencia`, `02_Interior`, `03_Estructura`.

## Cómo está construido

- Envolvente paramétrica (ángulo en planta, altura normalizada) con abombamiento del lateral derecho,
  irregularidad orgánica y anillo inclinado. Cada hueco, banda y celda de color es una elipse irregular en
  ese espacio; su borde se convierte en costilla y la clasificación de zonas da los paños.
- Cañas: barrido de perfil circular sobre el eje remuestreado, con anillos extra en los nudos
  (engrosamiento 11 %), conicidad, diámetro distinto por caña y extremos huecos (pared interior y sección
  anular) en las puntas expuestas. Haces de 3 a 8 cañas con giro suave y cañas interiores en los gruesos.
- Piezas perforadas: triangulación Delaunay del paño con los bordes de las celdas como contornos, agujeros
  por lanzamiento de dardos en 3D (radio según distancia al borde más cercano y campo de densidad, con
  agrupaciones de huecos pequeños), dos caras separadas 30 mm y paredes de agujero achaflanadas.
- Membrana: malla polar relajada (laplaciano sobre la altura) con picos fijos en los mástiles, borde
  festoneado con flecha entre mástiles y cordón perimetral.
- Tarima: tablas individuales recortadas al contorno, con juntas longitudinales y testas desplazadas.

## Comprobación

Con la cámara `01_Referencia` sobre la foto (`superposicion_referencia.png`): coinciden la anchura y altura
aparentes, los cuatro picos visibles, la pendiente del anillo, el anillo izquierdo, el hueco y la lente roja
de la derecha, el abombamiento derecho y la posición de los apoyos delanteros. El acceso queda unos 25 cm
más a la izquierda y algo más ancho que en la foto. Las dos piezas circulares metálicas quedan algo más
altas que en la imagen.

Revisado en el modelo: mallas con normales calculadas y compactadas, cañas que terminan dentro de los
casquillos (no entran en el suelo), cables que parten de las orejetas de los remates y acaban en tensor y
anclaje, abrazaderas centradas en el eje de cada haz, sin objetos sueltos fuera de capa. Las cañas de haces
que se cruzan sí se intersecan entre sí, como en la referencia; no se han resuelto esos encuentros con piezas
de unión específicas.

## Límites conocidos

- Las cañas, paneles, membrana y tarima son mallas; las curvas de eje son NURBS. Para cañas NURBS: `Pipe`
  sobre `01_Curvas_maestras` con los radios de la tabla.
- La membrana no tiene arrugas, gotas ni refuerzos de dobladillo modelados; es una sola capa.
- Los filamentos oscuros de los paneles de color son textura, no geometría; las sujeciones perimetrales son
  grapas en bloque.
- Las perforaciones no cruzan de un paño a otro; los cantos exteriores de las piezas perforadas quedan dentro
  de los haces y no están modelados.
- Tornillería solo en abrazaderas, apoyos y tensores (componentes repetidos); no hay tornillería singular en
  los nudos próximos a la cámara.
- Entorno simplificado: disco de terreno y 18 troncos, sin helechos ni vegetación baja.
- Los radios de curvatura de algunas costillas (anillo izquierdo, banda del acceso) son difíciles de obtener
  con caña natural de Ø 80 mm; se conserva la forma visual y la solución constructiva queda pendiente.
- No se ha podido consultar el uso restante de la cuenta desde esta sesión: no se indican porcentajes.

## Regenerar

Editar los parámetros del bloque 0 del script (anchura, altura del anillo, radio de caña, espesor de piezas,
cámara) o las celdas de la sección 3, y ejecutar `python3 generar_pabellon_bambu.py`. El script reescribe
el `.3dm`, las texturas, las vistas y el JSON.
