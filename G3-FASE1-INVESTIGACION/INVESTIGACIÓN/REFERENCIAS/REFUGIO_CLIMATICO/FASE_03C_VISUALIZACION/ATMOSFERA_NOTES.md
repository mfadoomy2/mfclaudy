# ATMOSFERA_NOTES — E03 (2026-08-11) · escena v003 congelada

Veredicto por cámara según §8 (técnicos automáticos en `_checks_e03.json` + checklist de dirección).
Se rellena tras la tanda y se revisa tras la ronda única E03-6.

## Método de la capa atmosférica
- Niebla: 321 sprites billboard (42 boquillas de suelo + 8 de barandilla de cinta + 3 columnas H7),
  blending normal, tinte #EAF6F2, deriva +X determinista. Regla anti-humo: se lee sobre fondo
  oscuro, casi desaparece sobre cielo (calibrada contra 12CA810C / 29A08040).
- Agua viva: 10 chorros de splash con corona-sprite y espuma perimetral (§7.2), 12 goteos de
  embudo (los discos ≤6.0 más bajos, línea dash + mini-corona), 3 mangueras en huerto C1 + 1 en
  viveros del istmo (v003), 2 rebosaderos (B-C2a, B-C3a). Calibrada contra FBDF10B9 / 24D82F58.
- Población: 40 PERSON2 low-poly en 8 programas (posiciones deterministas seed 1926, validadas
  contra 2.145 bbox de obstáculos v003; los peatones proxy v002 se ocultan en E03). Un caminante
  anclado al tramo H5 de la cinta.
- Luz: presets mediodía/tarde de atmos_config §4; reloj emisivo +0.35 en tarde (§7.3).
- Refinos: §7.2 y §7.3 aplicados; §7.4 y §7.5 ya eran GEOMETRÍA v003; §7.1 (alocasia 14 seg)
  NO aplicado — exigiría rehornear la escena congelada → pasa al handoff (HANDOFF_D5_VRAY.md).

## Notas por cámara (tanda 1 revisada + ronda global E03-6 de niebla; checks en `_checks_e03.json`)

| Cám | Veredicto | Qué funciona | Qué no / nota |
|---|---|---|---|
| H1 banda Correos | **OK** | alfombra de sombra real (ROI 32.2 % ≥30), río rosa de tuberías, caminante en la cinta, splash al borde | niebla tímida en tanda 1 → corregida en la ronda global |
| H2 huerto C1 | **OK — la mejor** | bancales+tutores, manguera con arco de agua, óculo del canopy, cinta+escalera al fondo, luz moteada | — |
| H3 splash | **OK** | chorros con cabeza (24 px), coronas, figuras dentro de la lámina, cinta cruzando | reflejos reales quedan para D5/V-Ray |
| H4 reloj (tarde) | **OK con nota** | contraste torre/cielo 61 % ≥15, reloj emisivo legible, persona en cinta a contraluz | Correos es proxy plano (contexto OSM); **Carlos III entra en encuadre como silueta de bronce a contraluz — presente, no ocultado**; el detalle del monumento es del render definitivo |
| H5 CINTA v003 | **OK** | tablero + barandilla 3 niveles en diagonal, escalera conmutada al fondo, discos sombra-cinta +8.30, dosel C2, caminante anclado | el ascensor C2-N queda medio ocluido por un pod flotante R-N desde este eje; la medianera de Preciados ocupa la esquina sup-izq (es el contexto real; no se maquilla) |
| H6 cúpula | **OK con nota** | ETFE con retícula, óculo, tropicales bajo la pérgola, persona en escala | alocasia 1er plano low-poly (refino §7.1 → handoff) |
| H7 aérea | **OK con reserva técnica** | composición equivalente a 0F53E6F0 (tres campos + cúpula + pods + trazas rosas); velos de niebla presentes tras la ronda | **las 3 columnas de vapor no se leen como columnas ni tras la ronda global**: un billboard con blending normal y tinte blanco sobre suelo/cubiertas claras es invisible por construcción (la misma regla anti-humo que protege el resto de vistas). Diagnóstico honesto: exigen volumétrica real → fila dedicada en `HANDOFF_D5_VRAY.md`. Falla 1 criterio de dirección (<2 → no procede NO-OK; regla §8, ronda única consumida) |

Balance final: 13 vistas OK / 1 OK-con-reserva (H7) / 0 NO-OK. Checks automáticos tanda 2: 14/14,
FALLOS: 0 (`_checks_e03.json`).
