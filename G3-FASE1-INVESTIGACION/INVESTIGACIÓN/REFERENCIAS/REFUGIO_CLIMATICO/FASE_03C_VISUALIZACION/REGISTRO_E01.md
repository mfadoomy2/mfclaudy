# REGISTRO — FASE 03C · E01 (materialidad + dirección de arte)
2026-08-07 · interpretación/criterio → acción → resultado → lectura → rectificación
Geometría 03B congelada: cero cambios geométricos (las arrugas POD son deformación de visor, no tocan los .3dm).

## Trazabilidad técnica (pruebas fallidas incluidas)
1. **Criterio**: PBR real (transmission/ior) según MATERIAL_SPEC. **Acción**: visor MeshPhysicalMaterial + PMREM + sombras. **Resultado**: en navegador vivo todo OK; en headless ni sombras ni textura. **Lectura**: dos fallos independientes. **Rectificaciones**:
   - Texturas file:// bloqueadas por Chromium en WebGL headless (probado flag `--allow-file-access-from-files`: NO funciona en headless=new; probado HTTP local: tampoco, por timing con virtual-time-budget) → **solución: texturas embebidas como data-URL** (`tex_data.js`) + 30 frames de asentamiento. Testigo de diagnóstico (quad verde/rojo) confirmó la carga.
   - **PMREMGenerator corrompe el pase de sombras** en headless (SwiftShader): test mínimo cubo+plano demostró que las sombras SÍ funcionan sin env → **solución: sin environment map** (queda tras `?env=1` para navegador vivo) y las translucideces pasan de transmission física a **alfa + emisivo tenue** (aproximación de visor documentada; la transmisión real la dará D5/V-Ray en tu máquina con este mismo SPEC).
   - Bug propio: `shoot()` anteponía `file:///` a la URL http (pantallazo de ERR_FILE_NOT_FOUND) → corregido.
2. **Criterio anti-globo (D03B-05)**: arrugas de inflado visibles. **Acción**: desplazamiento de vértices por ruido 3D determinista (2 octavas, 0.030+0.055 m, escala ±35% por instancia) sólo en envolventes POD/TANK. **Resultado**: costuras + arrugas legibles en primer plano (MATPREV_pod). **Lectura**: suficiente para E01.
3. **Iteración de paleta**: la 1ª pasada con alfa+emisivo viró a verdes botella, madera chocolate y magenta caliente. **Rectificación**: pastelización (canopy #C6DC90 em.0.45 · madera #BFA078 · red #E06B9C · POD #F2B3CC · veg #6F9E59) + exposición 1.20 + hemisferio 0.85.
4. **Humedad real**: textura de granito 3200px con despiece 1.8 m a 7° + moteado + **mojado pintado en los 42 nebulizadores, splash, estanques y trazas de la red** (color −28%, roughness 0.82→0.20). Resultado visible: anillo húmedo del splash en V13 y bandas en V05/V06.
5. Cámara V10 nació pegada a un soporte de la cúpula (todo marrón) → movida a (22,−4); cámara MATPREV_pod tapada por fuste → recolocada.

## Decisiones visuales (resumen para tu revisión)
- **Tríada material**: madera miel clara (estructura portante cálida y doméstica) + verdes lima translúcidos con emisión suave (el "cielo verde" luminoso) + rosas chicle pastel en dos intensidades (cápsulas claras F2B3CC / red técnica E06B9C, para que el SISTEMA hidráulico se distinga del PROGRAMA).
- **La sombra como argumento**: la alfombra de sombra del dosel sobre el granito (V05) es la imagen climática del proyecto; el sol alto de verano la produce sola.
- **Humedad localizada, no barniz**: sólo moja donde el sistema moja.
- **Contexto neutro cálido** que cede todo el color a la intervención.

## Las 6 cámaras — qué funciona / qué no / qué cambiar antes de E02
- **V07 reloj** ✓ madera+rosa+sombras, escala peatonal. ✗ la torre del reloj apenas protagoniza (contexto plano pálido). → E02: dar material mínimo a Casa de Correos (dos tonos + esfera de reloj) y quizá descentrar cámara 3 m oeste.
- **V06 bajo C1** ✓ intradós luminoso con nervios, doble tono lámina/membrana. ✗ tira a verde-azulado (teal) visto a contraluz; poca vegetación colgante. → E02: virar hue +8° a lima y trepadoras colgando del aro.
- **V13 splash** ✓ lámina reflectante, anillo húmedo, sombras del dosel. ✗ sin chapoteo/figuras de agua ni niebla (E03). → mantener cámara.
- **V10 cúpula** ✓ la pérgola Ø13 a +3.2 con óculo LEE perfECTA — D03B-04 validada visualmente. ✗ interior vacío de programa. → E02: vegetación de sombra bajo la cúpula.
- **V19 sobre cinta** ✓ barandilla, tanque rosa, tropicales desde arriba, profundidad. ✗ el toro del depósito en primerísimo plano distrae. → recuadrar +2 m adelante.
- **V05 banda Correos** ✓ LA imagen del argumento climático (sombra proyectada + tren de cápsulas). ✗ cielo quemado arriba (bajar exposición a 1.1 en esta cámara o degradado de cielo). → ajuste puntual.

## Transversales pendientes para E02/E03 (no bloquean la dirección de arte)
Vegetación = lollipops (E02 la sustituye) · vapor casi invisible (E03) · personas cilindro (E02/03) · membrana de cúpula sin patrón geodésico visible (menor).
