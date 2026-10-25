# G3 · Unidad v3 · datos y criterios (7-10-2026)

Archivo: `G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_UNIDAD/G3_unidad_suspendida.3dm`. Contiene el Módulo A (balcón), el Módulo B (porche bajo el estudio) y la célula F. Copia de la versión anterior: `G3_unidad_suspendida_v1_caracol_2026-10-07.3dm`.

## Tamaño
- Madrid, modificación de las NN.UU. de 2023 (coliving): unidad privativa individual ≥ 15 m²; común ≥ 25 m² + 5 m² por unidad adicional; vivienda nueva ≥ 40 m², o 30 m² en cohousing tipo 2.
- Reparto elegido: 32 unidades de unos 30 m² (24 individuales y 8 dobles = 40 personas).
- Superficie útil del módulo (interior de la carpintería):
  - Planta baja: 4,20 × 4,60 = 19,3 m².
  - Franja del altillo: 4,20 × 2,25 = 9,5 m².
  - Ala del estudio: 2,25 × 2,25 = 5,1 m².
  - **Total ≈ 33,8 m²**, por encima de los ~30 m². Las 8 dobles están sin diseñar.

## Retícula (sale del bloque de vidrio)
- Bloque de 190 + junta de 10 = 200 mm; holgura perimetral de 30 mm; pilar SHS 100.
- Crujías:
  - 2,15 m = 10 bloques.
  - 2,35 m = 11 bloques.
  - Planta 4,30 × 4,70.
  - Ala de 2,35 × 2,35 hacia un lado (L), solo arriba.
- Alturas (por hiladas):
  - Suelo acabado +0,30.
  - Zuncho del altillo +2,74 / +2,90 (12 hiladas debajo).
  - Suelo del altillo +2,94.
  - Zuncho de cubierta +5,54 (13 hiladas en el altillo; 26 hiladas exactas en la doble altura).
  - Cubierta acabada +5,95.
- Alturas libres: planta baja 2,44; altillo 2,60; doble altura 5,24.

## Cerramiento de bloque de vidrio (guía técnica Seves 2025)
- **Bloque:** 1919/8 ES (190×190×80, 2,6 kg). U = 1,4 W/m²K en transparente, con transmisión luminosa del 69 %. Versión satinada para intimidad.
- **Requisito térmico:** DB HE 1, tabla 3.1.1.a, zona D: huecos Ulim = 1,8 W/m²K. Un bloque estándar (U 3,0) no cumple; el ES sí. Que Madrid capital sea D3 está pendiente de confirmar en el Anejo B.
- **Paños:** < 15 m², ancho ≤ 7 m, alto ≤ 6 m. El mayor del modelo, el de doble altura, mide 2,05 × 5,24 = 10,7 m².
- **Ejecución:**
  - Mortero Vetromalta y varilla de acero inoxidable Ø6 en cada junta horizontal y vertical.
  - Perfil U perimetral con junta de dilatación de 5 mm en laterales y cabeza; banda de deslizamiento en la base.
  - Silicona en los contactos.
  - Es autoportante: no carga estructura.
- **Patrón:** franjas transparentes a la altura de los ojos (de +0,80 a +2,10 sobre el suelo en estancia y mesa; de +1,90 a +2,70 sobre el altillo para ver el cielo). El paso de transparente a satinado se hace con un tramado Bayer 4×4, a la manera de la fachada de Hermès. Baño y entrada, satinados enteros.
- **Huecos practicables (DB HS 3):** cada local necesita ventanas o puertas practicables de al menos 1/20 de su superficie útil.
  - Planta baja: hace falta ≥ 0,97 m². Puerta del balcón (A) de 1,00 × 2,42; ventana pivotante (B) de 1,00 × 1,20.
  - Altillo + ala: hace falta ≥ 0,73 m². Ventana pivotante de 1,00 × 1,20 en el testero del ala.
  - Antepechos a 1,10 o más, porque la unidad cuelga a más de 6 m.
  - Cocina: extracción mecánica propia (DB HS 3).
- **Peso:** 2.283 bloques en el Módulo A (unos 91 m² de paño, alrededor de 90 kg/m²), unos **8 t** por unidad. Hay que comprobarlo en el cálculo de los tirantes y la estructura de la que cuelgan.

## Escalera de caracol (DB SUA 1 §4.1, uso restringido)
| Requisito | Exigido | Modelo |
|---|---|---|
| Ancho | ≥ 0,80 | 0,802 |
| Contrahuella | ≤ 0,20 | 0,176 (15 contrahuellas) |
| Huella en el eje | ≥ 0,22 | 0,234 |
| Lado estrecho | ≥ 0,05 | 0,053 |
| Lado ancho | ≤ 0,44 | 0,432 |
| Altura libre (SUA 2) | ≥ 2,10 | 2,42 |

- Solo sube del suelo al altillo.
- Peldaños de roble de 40 mm con canto redondeado de r 8 mm.
- Casquillos de acero apilados (cada uno mide una contrahuella), así que el fuste se lee continuo.
- 4 barrotes Ø16 por peldaño (luz de 87 mm), cada uno atornillado al peldaño y rematado contra el pasamanos.
- Pasamanos helicoidal a 0,95, con poste de arranque y poste de llegada.

## Barreras (DB SUA 1 §3)
- Altillo: 0,98 (desnivel de 2,64 m, por debajo de 6 m).
- Balcón, porche, rellano y miniescalera: 1,10 (desnivel de más de 6 m).
- Barrotes verticales de Ø16 a 110 mm (luz de 94 mm, menos de 100); sin elementos escalables entre 30 y 50 cm.

## Miniescalera entre unidades (uso general)
- Huella 0,30; contrahuella 0,175; 2C + H = 0,65.
- 3 peldaños; ancho de 1,20 m, por encima de 1,00 (tabla 4.1, Residencial Vivienda).
- Peldaños de chapa plegada con canto redondeado.

## Variantes
- **A:** balcón de 1,05 m bajo el alero, con la puerta corredera en la crujía 2. Cubierta cerrada y no transitable.
- **B:** sin balcón y con ventana pivotante delante. La terraza es el porche que queda bajo el ala del estudio, cubierto, de 2,25 × 2,25 más el rellano, y se comparte con la unidad vecina por la miniescalera.

## Pendiente
- Cálculo de estructura (tirantes de Ø30, bandeja, pórtico) con el peso real del vidrio.
- Verificación de DB HE completa (K global, control solar q_sol;jul) con HULC.
- DB SI entre unidades.
- Itinerario accesible (ascensor) para las unidades adaptadas.

## Fuentes
- CTE DB SUA, DB HE, DB HS (codigotecnico.org).
- Seves Glass Block, Guía técnica 2025/3.
- Andersen, «Cómo afecta al coliving las nuevas normas urbanísticas de Madrid».
- Oikonomopoulou et al., TU Delft, Crystal Houses (sistema de vidrio colado pegado).
