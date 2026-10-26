# Pabellón de bambú (modelo 3D a partir de foto de referencia)

Carpeta generada el 26-10-2026. Modelo de un pabellón de haces de bambú con paneles
perforados blancos, vidrieras rojas y amarillas y cubierta de membrana, reproducido
a partir de una imagen de referencia (render fotográfico, bosque húmedo).

Es un ejercicio aparte del proyecto G3; no forma parte de la documentación de la vivienda
de Ribera de Curtidores.

## Archivos

| Archivo | Qué es |
|---|---|
| `PABELLON_BAMBU.3dm` | Modelo Rhino 8, unidades en metros, 615 objetos, 9,6 MB. Ábrelo directamente. |
| `tex_*.png` | Texturas (bambú, perforado color + alfa, vidrio rojo, vidrio amarillo, membrana, madera, agua, suelo con musgo, corteza). Deben quedarse en la misma carpeta que el `.3dm`: los materiales las referencian por nombre de archivo. |
| `generar_pabellon_bambu.py` | Script que genera todo (texturas + geometría + vista previa) con `rhino3dm`, `numpy`, `pillow`, `scipy`, `matplotlib`. Sin Rhino instalado. |
| `preview_pabellon.png` | Vista previa de comprobación renderizada desde el script (sin texturas, solo colores). |

## Cómo está construido

- Envolvente paramétrica (planta ovalada 9,2 × 6,0 m, anillo superior a 3,6 m, mástiles hasta 4,6 m).
  Cada hueco, banda roja y celda amarilla es una elipse en el espacio (ángulo, altura) de esa envolvente;
  su borde es una costilla de bambú.
- Costillas: haces de 3 a 5 cañas (radio de caña 4,2 cm, haz 7,2 cm) con giro suave, abrazaderas de acero
  cada 0,5–0,8 m, pedestales y placas de acero en los pies.
- Cubierta: membrana tensada con picos en los 8 mástiles, cables de cumbrera entre mástiles y vientos
  a anclajes en el suelo.
- Interior: tarima de madera, banco curvo, pila circular de agua con embudo de vidrio colgado y chorro,
  dos esferas de acero y caja eléctrica en el ala derecha, tiras LED magenta en el arco de entrada y en la lente roja.
- Entorno: terreno húmedo con musgo (disco de 36 m) y 18 troncos detrás y a los lados.

## Capas

`00_Ejes_bambu` (curvas NURBS de eje de cada haz) · `01_Bambu` · `02_Panel_blanco_perforado` · `03_Panel_rojo` ·
`04_Panel_amarillo` · `05_Membrana_cubierta` · `06_Acero` · `07_Madera_tarima_banco` · `08_Agua` · `09_Cables` ·
`10_LED_magenta` · `11_Vidrio_lampara` · `12_Terreno` · `13_Arboles`.

## Avisos

- Las cañas, paneles, membrana, tarima y troncos son mallas con coordenadas de textura propias; las abrazaderas,
  pedestales, esferas y cilindros son sólidos (Brep). Si quieres cañas NURBS, usa `Pipe` sobre las curvas de la
  capa `00_Ejes_bambu` (radio 0,042 m por caña, o 0,11 m para el haz completo).
- Los paneles perforados usan textura de transparencia (`tex_perforado_alfa.png`, blanco = agujero); se ve en los
  modos Renderizado y Raytraced, no en Sombreado.
- Las medidas son estimación a ojo sobre la foto, no datos medidos. No hay helechos ni vegetación baja.
- Para regenerar con cambios: edita el script y ejecuta `python3 generar_pabellon_bambu.py` (unos 25 s).
