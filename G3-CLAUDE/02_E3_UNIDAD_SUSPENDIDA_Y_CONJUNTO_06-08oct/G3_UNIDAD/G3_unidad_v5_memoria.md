# G3 · Unidad v5 · variantes y criterios CTE (8-10-2026)

Archivo: `G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_UNIDAD/G3_unidad_suspendida.3dm`. Tiene 7 variantes, cada una en su capa madre y separadas 12 m en x, más la célula F en x = 88. La versión anterior queda copiada como `G3_unidad_suspendida_v4_2026-10-07.3dm`. Todas llevan materiales PBR asignados por capa: vidrio de bloque traslúcido, acero en grafito y microcemento nuevo para el baño.

## Lo que comparten todas
- **Fachada delantera:** la de la apertura A (hoja oculta en muro de doble piel). Ya no hay mortero en el hueco, porque las juntas y las varillas se cortan en las aberturas.
- **Baño-cápsula:**
  - Pieza curva de microcemento, con muro de 80 y coronación a +2,40, por debajo del altillo.
  - Puerta corredera por fuera y conducto de extracción de Ø100 (DB HS 3).
- **Mesa de comer y de trabajo:**
  - Tablero de 1,60 × 0,80 con cantos redondeados y 4 sillas, en la doble altura (x 2,35–3,95; y 0,95–1,75).
  - Ya no está delante de ninguna puerta. Deja 0,95 m de paso hasta la puerta del balcón.
- **Ventana lateral grande** (fachada x = W, junto a la mesa):
  - Una sola división: un travesaño RHS a la cota del altillo.
  - Arriba, un vidrio grande fijo. Abajo, una hoja grande practicable con hueco libre de 2,13 × 2,44.
  - **Ventilación (DB HS 3):** se piden ≥ 0,97 m² practicables en planta baja. Abriendo 1,20 m salen 2,13 × 1,20 = 2,56 m², así que cumple.
  - **Barrera (DB SUA 1 §3):** como la hoja abre desde el suelo y la caída supera 6 m, lleva por dentro un antepecho de vidrio laminado 10+10 de 1,10 de alto con pasamanos de cuero.

## Ventana · 2 opciones
| | V1 Guillotina (base) | V2 Corredera exterior |
|---|---|---|
| Movimiento | La hoja inferior sube por delante del fijo, dibujada abierta 1,20 | La hoja corre por fuera, en x = W + 0,13, y se aparca delante del paño de la cocina |
| Ventaja | La fachada no cambia al abrir; no necesita sitio a los lados | El hueco queda abierto entero; carril sencillo |
| A comprobar | La hoja es grande (~5,2 m²; con vidrio doble laminado, del orden de 200–250 kg). Tiene que ir contrapesada o motorizada. La clase de estanquidad, con el fabricante | Carril y ménsulas exteriores colgados de la estructura. Estanquidad clase 3 o superior |

## Escalera · 3 opciones (DB SUA 1 §4, uso restringido)
| | E1 Lineal con estantería | E2 Caracol bajo el altillo | E3 Unidad + 1 crujía |
|---|---|---|---|
| Ancho (≥ 0,80) | 0,82 | 0,802 | 0,802 (caracol) |
| Contrahuella (≤ 0,20) | 0,176 × 15 | 0,176 × 15 | 0,176 × 15 |
| Huella (≥ 0,22) | 0,22, recorrido 3,08 | 0,234 en el eje; 0,053 en el lado estrecho (≥ 0,05); 0,432 en el ancho (≤ 0,44) | igual que E2 |
| Altura libre (≥ 2,10) | cumple | 2,42 | 2,42 |
| Idea | Pegada al muro izquierdo, con zanca central RHS y armario-escalera (kaidan-dansu) debajo | El caracol se mete bajo el hueco del altillo y libera la planta. El baño pasa delante, a la izquierda | Crujía añadida de 5 bloques (1,15 m) con rincón de comer de mesa y banco. Unos +5,3 m² útiles |

## Fuera del cubo · 2 opciones
- **F1 · Piezas interiores.** El cubo se queda como está y el interior es el que se vuelve «loco»:
  - Cocina monolítica de cantos redondeados con encimera de acero.
  - Borde del altillo curvo, con 0,45 m de flecha, que vuela sobre la doble altura. Debajo queda una altura libre de 2,46.
  - El vuelo cuelga de tirantes Ø16 y lleva barrera curva de 0,98.
- **F2 · Esquina curva y ala semicircular** (moderno del siglo XX, entre Mendelsohn y Chareau):
  - Esquina delantera izquierda de bloque curvo, R 1,15, concéntrica con el caracol, que sube con rellano.
  - Testero semicircular del ala del estudio, R 1,175, con un frente recto en el que va la ventana pivotante.
  - Forjados, cubierta y bandeja con la misma forma redondeada. Corredera de vidrio exterior en la crujía 2.
  - **Juntas en curva:**
    - Esquina: 9 bloques por hilada; junta de 4 mm por dentro y 18 mm por fuera.
    - Ala: 18 bloques por hilada; junta de 8 mm por dentro y 22 mm por fuera.
    - **Pendiente:** comprobar con la tabla de radios mínimos de Seves. Si la junta exterior sale demasiado ancha, se puede pasar a medio bloque (190 × 90) en las curvas.

## Pendiente
- Radio mínimo del bloque curvo (Seves), punto anterior.
- Estanquidad de la guillotina, de la corredera y del bolsillo de la hoja oculta.
- Cálculo de estructura con el peso real del vidrio, unas 8 t por unidad.
- HE con HULC y confirmación de la zona D3.
- Más adelante: para qué sirve la estructura que rodea la caja (tirantes, bandeja) y cómo se unen los módulos.
