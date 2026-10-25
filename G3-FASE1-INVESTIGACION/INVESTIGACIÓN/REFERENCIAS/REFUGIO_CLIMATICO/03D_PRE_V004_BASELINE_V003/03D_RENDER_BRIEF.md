# FASE 03D — VISUALIZACIÓN FINAL · BRIEF Y HANDOFF (2026-08-11)

**E03 = PREVIS/VALIDACIÓN (aprobada y cerrada) · 03D = VISUALIZACIÓN FINAL.**
Arquitectura **v003 CONGELADA** — nada de lo que sigue toca geometría; todo es representación.

Dos vías, mismas cámaras/luces/criterios:
- **A. Producción local Cycles** (esta máquina, RTX 5070 Ti/OptiX): `bl_scene.py` → `SOL_03D.blend` →
  `hero_03D\` — path tracing físico, GI, volumétricas reales, cielo físico + sol PSA. Es la tanda 03D entregada.
- **B. Render definitivo D5/V-Ray** (máquina del autor): este brief + `SOL_PRESENTATION_MASTER_v001.3dm`
  + `gh_scripts\named_views_03d.py` (vistas nombradas en Rhino) + assets de biblioteca (personas
  fotográficas, vegetación hi-poly, Carlos III detallado) — lo que Cycles-local no puede dar con proxies.

## 1 · CÁMARAS (idénticas en A y B; fov = VERTICAL)
| ID | cam (x,y,z) | target | fov | luz ppal | intención |
|---|---|---|---|---|---|
| H1 | (−2, −18, 1.65) | (6, 16, 5.0) | 62 | mediodía | alfombra de sombra + río rosa; exp −0.1 extra |
| H2 | (−56, 2, 1.65) | (−44, 18, 5.5) | 68 | mediodía | huerto productivo bajo dosel |
| H3 | (24, −10, 1.65) | (14, −1, 1.2) | 66 | mediodía | agua viva total; f/5.6 |
| H4 | (6, 8, 1.65) | (−25.2, −36.5, 15) | 58 | **tarde** | proyecto contra Correos; reloj legible; Carlos III en plano medio |
| H5 | (−12.8, 28.8, 7.55) | (10, 26, 6.5) | 63 | mediodía | LA CINTA v003: tablero→escalera→dosel |
| H6 | (22, −4, 1.65) | (33, 5, 4.5) | 68 | mediodía | cúpula-pérgola habitada |
| H7 | (0, −80, 42) | (2, 12, 0) | 55 | mediodía | HERO aérea: tres campos + columnas de vapor |

## 2 · LUCES (PSA real 21-jul, validado vs PVGIS)
- **mediodía 14:00 CEST**: elevación **69.48°**, azimut **165.65°** (N→E). Sol 3.2 (Cycles W/m²
  relativo) #FFF2DB; cielo físico (Nishita/multiple-scattering, altitud 650 m); exposición −0.35 AgX Punchy.
- **tarde 17:30 CEST**: elevación **45.30°**, azimut **257.85°**. Sol 2.2 #FFCC94; exposición −0.45;
  reloj de Correos con emisivo reforzado. *(El 30° de E03 era aproximación; el valor real es 45.3°.)*
- Perspectiva aérea: volumen ACOTADO sobre la plaza (460×350×60 m, densidad 0.00045, anisotropía 0.35).
  **Lección Blender 5: el volumen de MUNDO infinito rinde negro — usar siempre caja acotada.**

## 3 · MATERIALES (physically-based; spec ejecutable en `bl_scene.py`, tabla en `MATERIAL_SPEC_03D.json`)
Claves: **todos los hex de la paleta E01/E02 se convierten sRGB→lineal** (el lavado pastel de la
primera prueba era exactamente ese bug — misma trampa aplica en cualquier motor).
- Granito Sol: mapas color+roughness E01 (juntas 5.4 m), proyección planar mundo; en B: escaneo real.
- Canopy: membrana translúcida (transmission 0.55, IOR 1.35) + variación de tinte por disco → luminosa
  a contraluz SIN emisivo falso. Lámina de microalgas: vidrio verde (transmission 0.85).
- POD: TPU rosa — transmission 0.6 + SSS rosa 0.12 + **microarruga** (bump noise 6.5/0.22) + variación
  por cápsula. En B: costuras y tensión de patrón (el proxy no las tiene).
- Maderas 3 valores (jerarquía): primaria #A98F72 · secundaria/barandillas #C0A886 · tablero #8F7355.
- Vegetación: hoja con SSS foliar + **tinte aleatorio por instancia** (±35 %); troncos corteza aparte
  (heurística de esbeltez). En B: especies reales E02 (`ASSET_MANIFEST_03D.md`).
- Bronce Carlos III metallic 0.92/rough 0.38 + granito del pedestal. ETFE cúpula transmission 0.88.
- Aguas: splash/estanques vidrio IOR 1.33 rough 0.03; chorros+espuma blancos; tubería rosa #E06B9C.
- Niebla = **volumétrica real** (Principled Volume): 42 boquillas (esferas 2×2.2 m, ρ 0.05, g 0.55)
  + 8 en barandilla de cinta + **3 columnas H7** (ρ 0.028, z 5–19 m). Nunca humo gris: tinte #EAF6F2.

## 4 · JERARQUÍA DE H5 (encargo explícito)
tablero cálido oscuro (primer término) → barandilla clara (ritmo) → dosel verde translúcido (protagonista
luminoso) → vegetación saturada (contrapunto) → granito neutro abajo → fondo desaturado por atmósfera.
Separación por VALOR y saturación, no por línea. DoF f/8 foco en la escalera.

## 5 · QA
- **Técnico (se conserva de E03)**: `checks_03d.py` — 14/14 >30 KB, ROI de sombra H1 ≥30 % bajo p35,
  contraste torre/cielo H4-tarde ≥15 %, luminancia sin explotar.
- **Visual (manda el juicio, no el script)**: checklist §8 de dirección por vista + comparación 1:1
  contra las 6 referencias de calibración. El juicio visual NUNCA lo sustituye el QA automático.

## 6 · LO QUE SOLO PUEDE DAR LA VÍA B (D5/V-Ray + biblioteca)
personas fotográficas (posiciones EXACTAS en `PEOPLE_PLACEMENT_03D.csv`) · vegetación hi-poly por
especies · Carlos III modelado del monumento real · fachadas de contexto con huecos/carpinterías ·
caustics del splash · costuras del POD · granito escaneado.
