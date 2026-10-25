# FASE 03C — MATERIALIDAD, VEGETACIÓN, ATMÓSFERA Y VISUALIZACIÓN
## Plan de fase · preparado 2026-08-07 · pendiente de arranque

**Punto de partida (INTOCABLE):** `SOL_FULL_SCENE_v001.3dm` + `geometria_maestra_v002.json` +
`ASSET_LIBRARY_v001.3dm` + HEIGHT_SYSTEM. La geometría aprobada NO se rediseña; sólo se admiten
las *pequeñas deformaciones no destructivas* de D03B-05 (jitter de instancia, arrugado de shader).

---

## A · SISTEMA DE MATERIALES
Base: D14 (madera laminada/bambú + nudos acero + red rosa TPU) + paleta del manual gráfico.

| Familia | Material | Estrategia del 20-25 % restante (D03B-05) |
|---|---|---|
| POD / trenes / depósitos rosas | TPU translúcido rosa | **normal map de arrugas de inflado + bump de costura en gajos + roughness variable + translucencia (transmission/SSS ligera) + jitter de escala/rotación por instancia (ya determinista en build) + micro-deformación no destructiva (lattice suave por instancia si el motor lo permite)** |
| Discos-canopy | membrana verde translúcida + lámina de agua viva 2-5 cm | doble cara, transmission alta, caustics falsas por textura, oleaje como normal map animable |
| Estructura (loops, cinta, mástiles) | madera laminada clara / bambú tecnológico | veta anisotrópica suave, nudos y herrajes en acero claro, roughness 0.5-0.6 |
| Aros, tensores, herrajes | acero claro / cobre en red hidráulica de detalle | metalness 1, roughness 0.25 / 0.35 |
| Agua (balsas, estanques, splash) | verde-alga en masa, lámina clara en splash | absorción por profundidad, espuma de borde en splash |
| Membranas / cúpula | ETFE lechoso | transmission 0.6, roughness 0.3 |
| Suelo | granito Sol existente | teselado real post-2023, charcos/mojado en zona de nebulización (roughness map) |
| Contexto | fachadas neutras cálidas | flat + AO, sin competir con la intervención |

Entregable A: `MATERIAL_SPEC.json` (por capa/familia: baseColor, roughness, metalness, transmission,
normal/bump, variación por instancia) consumible por el visor PBR de sesión y traducible a
Rhino/D5/Enscape/V-Ray en la máquina del autor.

## B · VEGETACIÓN FINAL (VEG_FULL)
- Salto de VEG_MEDIUM → biblioteca real por especie-rol: árbol existente (plátano/acacia), árbol
  nuevo ligero, trepadoras en mástiles y cables (recorrido real por la curva), tropical de sombra
  (alocasia/platanera bajo discos), herbáceas de jardinera, hortícola del huerto (24D82F58),
  colgantes desde bandejas, acuáticas de estanque, microalgas en masa de agua.
- SIEMPRE instancias/bloques con capa `15_VEGETATION_FULL` apagable; proxies conservados.
- Densidad dirigida por la planta (no scattering aleatorio): la densidad de puntos de P01 es el mapa.

## C · ATMÓSFERA
- Nebulización: volúmenes ligeros/billboards en los 42 puntos reales + deriva bajo discos (12_MIST).
- Luz: sol de verano Madrid (15 jun–15 sep, mediodía y tarde dorada), luz filtrada verde bajo el
  dosel, sombra proyectada del sistema sobre el granito.
- Humedad: pavimento mojado en radio de nebulización, gotas en membranas y cápsulas.
- Gente y uso: siluetas/assets en corredores y estancias (manguera-comba, riego, chapoteo).

## D · VISUALIZACIÓN
- **Pipeline de sesión (borradores):** visor PBR (three.js: transmission real, sombras, AO, fog)
  sobre `scene_full.js` + MATERIAL_SPEC → tandas de vistas para dirección de arte.
- **Pipeline final (máquina del autor):** Rhino + D5/Enscape/V-Ray con los .3dm por bloques
  (materiales por capa se asignan una sola vez gracias a la disciplina de capas 00-30).
- Set de cámaras heredado y validado: V01–V20 + secciones + cenital 0F53E6F0-equivalente + las 8
  del piloto. Objetivo: la serie definitiva "mismo proyecto que los renders" para la memoria.

## Etapas propuestas (a validar al arrancar)
E01 MATERIAL_SPEC + visor PBR y 6 vistas de dirección de arte → revisión ·
E02 biblioteca VEG_FULL + densidades → revisión ·
E03 atmósfera (niebla/mojado/luz) → revisión ·
E04 tanda final de visualización + láminas (régimen maximalista donde toque) ·
E05 registro y cierre. STOP entre etapas mayores.

## Reglas heredadas
No rediseñar geometría aprobada · no Tripo (D03B-05) · clay first ya cumplido · bloques siempre ·
certezas CONFIRMED/INFERRED/SPECULATIVE vivas · registro continuo · P01/P02 sólo se tocan si un
cambio material altera la leyenda.
