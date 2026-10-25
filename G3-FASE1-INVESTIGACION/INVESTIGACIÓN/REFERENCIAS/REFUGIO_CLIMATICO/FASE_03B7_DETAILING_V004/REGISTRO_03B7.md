# REGISTRO — FASE 03B.7 · RAMA v004 (URBANO + DETAILING EXTREMO)

## 2026-08-11 — EJECUCIÓN COMPLETA (orden del autor: PAUSA 03D → rama v003→v004)

v003 queda **congelada e intacta** en `FASE_03B6_RESOLUCION\`. Todo lo de esta fase vive aquí.
La tanda Cycles en curso se dejó terminar y se archivó como `..\03D_PRE_V004_BASELINE_V003\`
(14/14, QA 13/14 con H4_tarde documentada sin iterar, por orden expresa).

### Cadena canónica v004
`make_v004.py` (datos: v003→v004) → `geometria_maestra_v004.json` (+`_v004_diff.json`)
→ `build_all_03b7.py` + `detailing_03b7.py` → `MASTER_ARCHITECTURE_v004.3dm`,
`SOL_FULL_SCENE_v003.3dm`, `SOL_PRESENTATION_MASTER_v002.3dm`, `ASSET_LIBRARY_v003.3dm`,
`_viewer\scene_full.js`. Metadatos `sistema/familia/version` por objeto (auditoría municipal futura).

### A · Conflictos urbanos (informe: `URBAN_INTEGRATION_REPORT.md`)
v003 medida: 439 mallas hasta 10.1 m dentro de El Corte Inglés; 173 sobre la Estación (edificio
real 20×7 tratado como punto). v004: **EDGE_GUARD por regla** (recorte de loops→pórtico-galería,
empuje de cinta a plaza, anclajes por huella real, guardas por familia con alcances medidos).
Resultado verificado (invest_urbano + módulo A12 independiente): **0 penetraciones / 79 edificios**.
Figura B: atrio de la Estación + belvedere + media luna de Carmen + aprons + dosel abierto.

### B · Detailing (informe: `DETAILING_REPORT.md`, métricas: `METRICAS_DETALLE_v004.json`)
7 997 → **16 529 objetos** (+107 %), 19_DETALLE = 3 466 piezas / 149k tris; 1 468 pletinas,
116 juntas, 42 luminarias… Vegetación v2 sin esferas; Carlos III grupo ecuestre coherente
(la peana v003 levitaba 1.1 m — visible solo al acercarse). 24 controles a 50m/10m/2m/50cm
(`_control\`) con UNA ronda de corrección (estatua, trepadora, bola del mástil).

### C · Reauditoría (`_reaudit7\`, PDF: `AUDIT_V004_MASTER.pdf`)
11 iteraciones REGENERAR→REAUDITAR: 25 RED → **0 RED / 28 YELLOW / 20 GREEN** (las YELLOW son
la misma clase documentada del cierre v003). Nuevo módulo **A12-EDIFICIOS**. Reglas nuevas
reutilizables: `snap_facade` (CR-2: cerrado a 2 cm o abierto ≥1.5 — los márgenes 0.5-0.8
fabricaban ranuras-trampa), `MASTS_XY = posiciones FINALES` para toda guarda posterior,
convergencia iterada de guardas del árbol, fragmentos mínimos 2.4/1.8 m, uniones constructivas
del despiece declaradas por nombre en A10, pavimento enrasado ≤6 cm = pisable.

### D · Clima (`_reclima7\`, PDF: `CLIMATE_V004_MASTER.pdf`)
Mismo método 03B.5B (PVGIS + UTCI oficial). Cierre con las MISMAS 2 RED de decisión que v003
(CL-002 hotspots, CL-004 cinta cálida) + 3 YELLOW. **Deltas honestos v003→v004**: sombra crítica
pisable 43.8→36.6 %, refugio efectivo con niebla 4 837→4 452 m², hotspots 4 629→5 707 m².
Atribución (3 causas): ① parte de la sombra v003 era FICTICIA (la proyectaban elementos dentro
de edificios o volando la Estación); ② apertura DELIBERADA del dosel sobre la Estación (diseño B);
③ el follaje v2 (abanicos) es más poroso en el vóxel que las copas macizas v003 — efecto de
representación, no de proyecto (la copa real es densa; pendiente de calibrar k_veg por LAI en
la siguiente pasada climática).

### Entregables
`03B7_V003_V004_BEFORE_AFTER.pdf` (A edificio · B metro · C zooms) · `AUDIT_V004_MASTER.pdf` ·
`CLIMATE_V004_MASTER.pdf` · `DETAILING_REPORT.md` · `URBAN_INTEGRATION_REPORT.md` ·
`METRICAS_DETALLE_v004.json` · `_v004_diff.json` · `_reaudit7\ISSUES_REGISTER.md` + métricas ·
masters .3dm v004 · `_control\` (24 tomas) · `_beforeafter\` (8 pares).

### ABIERTO (decisiones del autor, no defectos)
- Hotspots CL-002 (5 707 m², 17 zonas identificadas) y cinta cálida CL-004: ampliar dosel /
  niebla / aceptar como paso — misma decisión pendiente desde v003.
- Calibrar densidad foliar v2 en el vóxel climático (k_veg por LAI) para que la comparación
  climática entre versiones sea entre iguales.
- Posición G2+ de Carlos III sigue pendiente de plano municipal (DEC-0006).
- Campaña final de render (03D) sobre este modelo, cuando el autor la ordene.

**VEREDICTO: V004 READY FOR MUNICIPAL ANALYSIS** (0 RED geométricas; clima con las mismas
decisiones documentadas con las que se aprobó v003; 0 penetraciones urbanas verificadas de
forma independiente; detalle informacional trazable pieza a pieza).
