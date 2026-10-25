# VEGETATION_ASSET_REPORT — FASE 03B.8 §7-§10

"Una maceta con cuatro triángulos verdes no es una planta." — resuelto con ASSETS REALES.

## Assets externos (licencias en `ASSET_PROVENANCE.csv` + `_assets_veg/provenance.json`)

| Rol | Asset | Fuente | Licencia | Tris H/M/F |
|---|---|---|---|---|
| HELECHO | fern_02 (fotoescaneo) | Poly Haven | CC0 | 4995/1198/475 |
| ALOCASIA | anthurium_botany_01 | Poly Haven | CC0 | 5013/3772/3772 |
| CALATHEA | calathea_orbifolia_01 | Poly Haven | CC0 | 4995/1195/583 |
| GRAMÍNEA | grass_medium_02 | Poly Haven | CC0 | 4994/2201/2201 |
| ARBUSTO | shrub_04 | Poly Haven | CC0 | 5000/1412/1412 |
| MACETA | potted_plant_01 (fotoescaneo) | Poly Haven | CC0 | 16804 (uso HERO puntual) |
| MONSTERA | monstera (Isa Lousberg) | poly.pizza | CC0 | 5000/1200/341 |
| POTHOS colgante | pothos (Isa Lousberg) | poly.pizza | CC0 | 3680/1200/260 |
| JUNCO humedal | cattail (Poly by Google) | poly.pizza | **CC-BY 3.0** (atribución anotada) | 1146/—/261 |

Pipeline: `veg_assets.py` — GLTF/GLB → trimesh (transformadas de escena aplicadas), Y-up→Z-up,
escala a altura real de especie, base a z=0, limpieza de caras degeneradas en origen,
decimación `fast_simplification` a 3 LOD → `_veg_blocks.json` → BLOQUES `VEGA_<ROL>_{H,M,F}`
(instancias, geometría pesada UNA vez por LOD).

## Sistema LOD (§8)

`lod_veg(x,y)`: **HERO** <14 m del corazón de plaza (primeros planos), **MID** <62 m,
**FAR** perímetro. La selección es automática por posición de instancia.

## Dónde se plantó qué (§9)

- Tiestos de mástil: helecho/calathea/gramínea ×2 por tiesto, giro variable — sobre TIERRA real.
- Jardineras de banco: gramínea/helecho alternados sobre **cama de plantación** (nada brota
  del granito desnudo).
- Estancias tropicales: alocasia/calathea/monstera (antes: abanicos procedurales).
- Colgantes de aros y cinta: pothos real colgando del punto de cuelgue.
- Balsas: junco (cattail) en la orilla + nenúfares procedurales en la lámina.
- Huerto: cultivos procedurales v2 (tomatera con tutores/lechuga/aromática) — sin asset digno,
  se mantienen y LEEN bien en las tomas.
- Árboles: `arbol_v2` procedural (tronco+ramas+abanicos) — sin fotoescaneo CC0 de árbol
  urbano completo disponible; candidato a mejora en la siguiente pasada.

## Macetas / jardineras (§10)

Tiesto de mástil v2: vaso con espesor + labio torico + sustrato a su nivel + collarín del
fuste + 3 mechinales + gotero de acometida. Jardineras lineales: coronación + mechinales
(03B.7) + cierre CR-2 contra fachada. Bancos: testeros de remate en los extremos.
