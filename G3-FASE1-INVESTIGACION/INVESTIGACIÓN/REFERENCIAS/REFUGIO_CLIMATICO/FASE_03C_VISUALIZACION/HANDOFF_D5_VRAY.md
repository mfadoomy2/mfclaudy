# HANDOFF E03 → RENDER DEFINITIVO (D5 / V-Ray, máquina del autor)

Base: `FASE_03B6_RESOLUCION\SOL_PRESENTATION_MASTER_v001.3dm` (v003). Cámaras/luces:
`atmos_config.json`. Cada efecto del visor E03 tiene equivalencia directa:

| Visor E03 (aprox.) | Render definitivo |
|---|---|
| Sprites de niebla (billboard alpha 0.08-0.18, tinte #EAF6F2) | volumétrica real (VRayEnvironmentFog / D5 fog local) SOLO en las 42+8 boquillas; densidad baja, anisotropía 0.6 hacia el sol |
| Columnas de vapor H7 (8 sprites apilados) | 3 emisores volumétricos cilíndricos sobre C1/C2/C3, z 14-18, ruido animado |
| Chorros splash (cilindros alpha + esfera) | agua real con espuma (foam) + caustics ON en la lámina de 3 cm |
| Coronas de chapoteo (sprite) | partículas de impacto o decal animado |
| Goteo de embudos (dash lines) | hilos de agua con gravedad + ripples en el punto de caída |
| POD alpha+emisivo 0.74 | transmission/SSS real (TPU lechoso #F3C4D5, IOR 1.42, absorción rosa) |
| Canopy alpha+emisivo 0.5 | membrana two-sided translucency + lámina de microalgas con SSS verde (D15) |
| Reloj emisivo +0.35 en tarde | exposición real de contraluz; el reloj debe seguir legible (criterio §8) |
| Granito data-URL 2 texturas | material completo con juntas 5.4 m, roughness 0.16 en mojado (-34 % de valor) |
| PERSON2 low-poly | población real (escaneados/3d people) EXACTAMENTE en las posiciones de `scene_extra.js` (validadas contra obstáculos v003) |
| Refino §7.1 pendiente | alocasias: palas 14+ segmentos con curvatura (no se rehorneó la escena v003 congelada) |
| Carlos III proxy bronce/granito | modelo detallado del monumento REAL (posición v003 G2+ pendiente de plano municipal) |

Reglas que NO se negocian en el definitivo: nada nocturno, sin lens flares, paleta E02 (6 hex ±8 ΔHSL),
niebla legible solo en contraluz (nunca gris plomo), el reloj de Correos siempre legible.
