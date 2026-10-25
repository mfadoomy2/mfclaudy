# KIT_OF_PARTS_STRATEGY — REFUGIO CLIMÁTICO PUERTA DEL SOL
## Fase 03A · 2026-08-07

Estrategias: **A** Rhino directo · **B** Rhino+Grasshopper (paramétrico) · **C** Tripo (IA 3D) ·
**D** Asset existente · **E** Híbrido (Tripo → limpieza → Rhino)

En esta fase los generadores paramétricos son los scripts Python (`proxy_build.py` + `mesh_kit.py`,
deterministas, fuente XY = `geometria_maestra.json`); en 03B se traducen a Grasshopper donde aporte
edición en vivo. Las curvas maestras (ejes de loops, cinta, redes) viajan ya como curvas en el .3dm.

| # | Familia | Estrategia | Por qué / cómo |
|---|---|---|---|
| 01 | PRIMARY STRUCTURE (loops, arcos, cinta portante) | **B** | curvas maestras → pipe/sweep; ejes editables en capa 02; NUNCA mesh congelada |
| 02 | SECONDARY STRUCTURE (ramificaciones, aros de disco, zancas) | **B** | generadas desde 01 por reglas (arranque a 3.0, brazos a discos ≤4.5 m) |
| 03 | LEAF CANOPY (discos-hoja verdes) | **B** | `LEAF_CANOPY_MASTER` paramétrico (ver abajo); 67 instancias por parámetros |
| 04 | TENSIONED MEMBRANE (redes, velos, cúpula) | **B** | superficies regladas entre anillos; form-finding real en Fase 02 |
| 05 | MAST (mástiles ramificados) | **B** | familia única: fuste Ø0.26, ramificación a 3.0, 2-3 brazos |
| 06 | CABLE (tensores) | **A** | líneas/pipes Ø 8-12 mm; jamás Tripo |
| 07 | PINK POD (cápsula neumática) | **E** | master paramétrico proxy (esfera/píldora/toro con gajos) + UNA pieza héroe Tripo para primer plano |
| 08 | PLANTER (jardineras corridas) | **B** | strip de sección 1.4×0.60 sobre arcos offset de los loops |
| 09 | PLANTER BENCH (banco-jardinera) | **B** | sección compuesta asiento 0.45 + respaldo 0.85 sobre las mismas curvas |
| 10 | TREE (árboles) | **D** | assets de vegetación (proxy + full); jamás modelar hojas a mano |
| 11 | LOW VEGETATION | **D** | scattering de assets sobre jardineras/orlas; capa apagable |
| 12 | VERTICAL NURSERY (torres-vivero 3.0, baldas c/0.8) | **A** | cajas + baldas simples; detalle en 03B |
| 13 | WATER BASIN (balsas elevadas y estanques) | **B** | elipses/riñones + murete 0.60; lámina como superficie |
| 14 | MISTING SYSTEM (boquillas) | **A**+bloque | bloque `MIST_NOZZLE` Ø0.15 sobre puntos de la red |
| 15 | WATER PIPE (troncal Ø0.35, mangueras Ø0.09) | **B** | curvas de red → pipe; la red ES dibujo del proyecto |
| 16 | SENSOR / TERMINAL / TOTEM (1.35) | **A**+bloque | cilindros/placas simples; catálogo en 03B |
| 17 | GROUND TANK (depósito suelo 1.35 / gota 2.2) | **E** | proxy revolución + héroe Tripo (depósito-gota zunchado) |
| 18 | ELEVATED TANK (toro TPU en torre a 10.5) | **B** | toro paramétrico + fuste; bajante = familia 15 |
| 19 | STAIR / ACCESS (zancas a cinta) | **B** | 6 ud sobre la cinta |
| 20 | DOME (cúpula geodésica Ø13) | **B** | teselación geodésica paramétrica; SPECULATIVE, puede caer en v1.1 |
| 21 | LAB PAVILION (vidrio curvo) | **A** | muro-cinta 3.5 + cubierta; interior en 03B |
| 22 | CONTEXT (Casa de Correos, manzanas) | **A** | extrusiones OSM; Casa de Correos con torre y reloj algo más fieles en 03B |

## LEAF_CANOPY_MASTER (familia 03) — parámetros
`Length` 3–12 · `Width` 0.8·Length–Length · `Height` (cota aro) 4.2–8.5 ·
`CentralDrop` 0.18·R (embudo de drenaje, cf. 8F402100) · `EdgeElevation` ±0.3 ·
`Rotation` libre · `MembraneSag` 0.05–0.12·R · `RimDiameter` 0.12 ·
`NumberOfRibs` 8–12 · `WaterDepth` 0.02–0.05 (lámina de microalgas)
Variantes: LF-S (Ø3), LF-M (Ø5), LF-L (Ø8), LF-XL (Ø12, sólo C2).

## PIEZAS PROPUESTAS PARA TRIPO (lista exacta — NADA se envía aún)
1. `TRIPO_PINK_POD_01` — cápsula-esfera Ø3.25 con gajos, válvula superior y faldón de amarre (pieza héroe, primer plano).
2. `TRIPO_PINK_POD_TRAIN_01` — cápsula-depósito horizontal Ø2.4×5.5 con zunchos y conectores (los trenes O/SE).
3. `TRIPO_DROP_TANK_01` — depósito-gota transparente zunchado 2.2 m (58089CE5).
4. `TRIPO_SPECIAL_PLANTER_01` — jardinera-cuba de madera Ø1.5 con mástil integrado (12CA810C).
5. `TRIPO_MIST_HEAD_01` — cabezal de nebulización con brida (35950EB8) para primeros planos.
Regla: un objeto claro por generación, multiview FRONT/LEFT/BACK/RIGHT del MISMO objeto, sin oclusiones,
fondo neutro; después IMPORT→SCALE→CLEAN→REMESH→NORMALS→MANIFOLD→ORIGIN→BLOCK→ASSET_LIBRARY.

## PIEZAS PARAMÉTRICAS (lista exacta)
Loops (8) + cinta + soportes + escaleras · discos LEAF_CANOPY (67) · mástiles (≈100) + ramas + cables ·
membranas/redes (3 sectores + cúpula) · jardineras (13 tramos) + bancos (5 arcos) · balsas (6) +
estanques (5) + splash · red de agua (troncales 4 + risers) + boquillas (42) · depósitos elevados (6) ·
torres-vivero · tótems · contexto OSM.

## MODELOS SEPARADOS (03B)
`MASTER_ARCHITECTURE.3dm` (geometría limpia por capas) · `ASSET_LIBRARY.3dm` (bloques master) ·
`SOL_FULL_SCENE.3dm` (linked blocks) · `SOL_ANALYSIS.3dm` (ligero para simulación).
En 03A se entrega `SOL_REFUGIO_3D_PROXY_v001.3dm` + `PILOT_FRAGMENT.3dm`.
