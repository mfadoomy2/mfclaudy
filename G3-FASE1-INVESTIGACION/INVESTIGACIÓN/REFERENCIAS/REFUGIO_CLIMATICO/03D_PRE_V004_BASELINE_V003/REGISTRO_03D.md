# REGISTRO — FASE 03D · VISUALIZACIÓN FINAL

## 2026-08-11 — ARRANQUE (orden del autor tras aprobar E03 como PREVIS)
Separación oficial: **E03 = PREVIS/VALIDACIÓN** (cerrada) · **03D = VISUALIZACIÓN FINAL**.
Arquitectura **v003 CONGELADA** — 03D es representación pura.

### Descubrimiento de pipeline
En esta máquina hay **Blender 5.0.1 + 2× RTX 5070 Ti (OptiX)** y Rhino 8 → la producción final
puede ejecutarse LOCALMENTE con Cycles (path tracing físico), además del handoff D5/V-Ray para
la máquina del autor. Se hacen las dos cosas.

### Producción Cycles (vía A)
- `bl_scene.py` (build+render): importa la escena v003 horneada + capa E03 validada, fusiona
  8.310 mallas en 24 cubos de material (539 K tris), tinte por instancia horneado en atributo de
  color (variación real de vegetación/canopy/pods), curvas para cables y goteo, **volumétricas
  reales** para las 42+8 boquillas y las 3 columnas H7, cielo físico + **sol PSA real**
  (`SUN_03D.json`: mediodía 69.48°/165.65°, tarde 45.30°/257.85° — el 30° de E03 era aproximación),
  perspectiva aérea por volumen acotado, AgX Punchy, DoF f/8, 7 cámaras (fov vertical).
- **Incidencias y lecciones (registradas con bisección)**:
  1. `Sky NISHITA` no existe en Blender 5 → `MULTIPLE_SCATTERING`.
  2. **Frame negro**: el volumen de MUNDO infinito mata cámara y cielo en Cycles 5.0 →
     bisección Workbench/Cycles-sin-volumen lo aisló; solución = **volumen ACOTADO** (caja).
  3. **Lavado pastel**: los hex sRGB entraban como lineales → conversión sRGB→lineal en `hexc()`
     (misma trampa aplica a cualquier motor: documentado en brief y MATERIAL_SPEC).
  4. Sin `--factory-startup` los nombres de nodo se localizan (es) y rompen los scripts.
  5. Calibración: sol 3.2/2.2, fondo 0.38, atmósfera 0.00045, exposición −0.35/−0.45.
- Prueba H5/H1 aprobada: paleta E02 real, jerarquía H5 (tablero oscuro → barandilla clara →
  dosel translúcido luminoso → vegetación saturada → fondo atmosférico), sombra moteada física.
- **Tanda final**: 14 vistas 2560×1600, 160 samples adaptativos + OpenImageDenoise, GPU OptiX.

### Handoff (vía B)
`03D_RENDER_BRIEF.md` (cámaras+luces+jerarquía+QA) · `MATERIAL_SPEC_03D.json` ·
`ASSET_MANIFEST_03D.md` (roles vegetales E02 → assets, personas fotográficas, Correos real,
Carlos III del monumento real con posición G2+ pendiente de plano municipal) ·
`PEOPLE_PLACEMENT_03D.csv` (38 posiciones validadas) · `EFFECTS_03D.csv` ·
`gh_scripts_named_views_03d.py` (7 vistas nombradas en Rhino 8) · `SUN_03D.json`.

### QA
`checks_03d.py` = QA técnico heredado de E03 (tamaño, rango tonal, ROI sombra H1, contraste H4).
**El juicio visual manda; los checks solo detectan roturas** (orden explícita del autor).

---

## CIERRE COMO BASELINE (2026-08-11 · orden PAUSA 03D)

- Tanda Cycles completada **14/14** (H1–H7 × mediodía/tarde, 2560×1600, ~6 min/frame, 2× RTX 5070 Ti OptiX).
- QA técnico (`checks_03d.py` → `_checks_03d.json`): **13/14 OK**. **H4_tarde NO cumple** el criterio
  heredado de contraste torre/cielo (6.8 % < 15 %). Por orden expresa de PAUSA **no se itera ni se
  postproduce**: queda documentado como estado real del baseline.
- Estado de esta carpeta: **`03D_PRE_V004 / BASELINE_VISUAL_v003`**. Nada de lo aquí producido es
  entregable final: es el testigo visual de v003 y el banco de pruebas del pipeline Cycles
  (lecciones consolidadas: sky MULTIPLE_SCATTERING, volumen ATMOSFERA acotado, hexc sRGB→lineal,
  sensor_fit VERTICAL, `--factory-startup`). La campaña final de render se ejecutará sobre el
  modelo definitivo **post-v004** reutilizando `bl_scene.py` + `SUN_03D.json` + `MATERIAL_SPEC_03D.json`.
