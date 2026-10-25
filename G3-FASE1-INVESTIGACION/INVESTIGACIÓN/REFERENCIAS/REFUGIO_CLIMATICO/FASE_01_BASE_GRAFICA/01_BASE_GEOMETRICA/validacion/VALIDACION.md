# VALIDACIÓN DE LA PLANTA MAESTRA — FASE 01

Imágenes generadas:
- `validacion_A_orientacion_maestra.png` — planta maestra proyectada sobre la cenital 0F53E6F0 (afín por 3 puntos de control: esquinas de fachada de la Casa de Correos + pico de la media luna).
- `validacion_B_espejo_como_foto.png` — ídem con la planta espejada E-O (orden de clústeres tal como lo compuso la IA en esa foto).
- `validacion_C_composicion.png` — panel norte-arriba: dibujo matriz / HR01 / FE9A5E6E / planta maestra.

## Resultados

### Coincide ✅
- **Topología**: 3 clústeres encadenados O-E por una cinta continua con 5–6 bucles; anillo doble en el centro; gran óvalo en un extremo; clúster fragmentado con máxima densidad de cápsulas en el otro. Coincide con dibujo matriz, HR01, FE9A5E6E y F295448F.
- **Banda libre ante la Real Casa de Correos**: 14,8 m desde fachada (la cenital 0F53E6F0 muestra 15–20 m). ✓
- **Claros de monumentos**: Carlos III 9,1 m · Mariblanca 9,2 m · bocas de metro y marquesinas de Cercanías intactas. ✓
- **Trenes de cápsulas en bordes exteriores** (O y SE) y racimos a media altura junto a los nudos. ✓
- **Extensión**: 163 × 51 m dentro de una plaza de ≈180 × 95 m; arbolado existente (OSM) conservado. ✓

### Desviaciones documentadas ⚠️
1. **Espejo E-O de 0F53E6F0**: la foto es sur-arriba (el reloj cae al 54% desde la izquierda ⇒ izquierda = este) y la IA conservó el orden izquierda-derecha del dibujo ⇒ en esa única imagen el gran anillo queda al este. Se adopta el orden del dibujo matriz en convención norte-arriba (gran anillo al O), coherente con las 4 referencias norte-arriba y funcionalmente mejor: el clúster mayor cae en la zona más ancha de la plaza. → `05_LOG/decisiones.md#D3`.
2. **La plaza de 0F53E6F0 está estirada** ~20–30 % hacia el este respecto a la geometría real (OSM). El overlay A/B no puede cerrar simultáneamente fachada y extremos: la desviación es del render, no de la planta. El contexto de la BASE MAESTRA es OSM (verdad geométrica).
3. **Proporción de la banda**: dibujo matriz ≈2,2:1; planta maestra 3,2:1. El fondo útil real entre banda de Correos y paseo del arco norte es ≈50 m, lo que aplana la composición. Inevitable y asumido.
4. **Fuentes**: 0F53E6F0 muestra las 2 fuentes pre-2023 (foto base antigua). El Sol actual no tiene fuentes; los claros se asignan a Carlos III, Mariblanca y cruces peatonales. → `decisiones.md#D2`.
5. **Densidad de dosel**: discos+balsas = 1.890 m² (17 % de la plaza). Los renders sugieren más masa de sombra; el dimensionado real de sombra es salida de los estudios solares/UTCI de FASE 02 (los discos son G2/G3 en posición). Anotado en `incertidumbres.md`.

## Conclusión
La planta maestra es fiel a la geometría dominante del proyecto y respeta el espacio urbano real. Se considera VALIDADA para servir de fuente de verdad de Fase 01, con las incertidumbres listadas.
