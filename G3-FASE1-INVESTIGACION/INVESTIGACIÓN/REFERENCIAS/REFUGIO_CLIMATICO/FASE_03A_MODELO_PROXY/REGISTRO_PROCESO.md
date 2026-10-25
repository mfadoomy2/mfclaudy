# REGISTRO DEL PROCESO — FASE 03A (modelo proxy transitable)
2026-08-07 · continúa la trazabilidad de 05_LOG de Fase 01

## E01 — Análisis
- Re-escaneo completo de DIBUJO3: sin archivos nuevos desde Fase 01 (61 conocidos, todos 14-07-2026).
- Referencia canónica de implantación fijada por el autor: `0F53E6F0`.
- Workflow de 4 analistas midió 17 renders interiores → 120+ cotas con método y certeza (base del HEIGHT_SYSTEM). Patrones: persona 1.70, farola fernandina 4.5–5, planta madrileña 3.5, banco 0.45.
- **Corrección de interpretación**: los trenes de cápsulas O/SE son depósitos-cápsula horizontales APOYADOS (Ø2.4×5.5, apoyo 0.3, CONFIRMED A2BD2AAA) — en P01 se asumieron a media altura. Registrado en HEIGHT_SYSTEM.

## E02 — Alturas y familias
- `HEIGHT_SYSTEM.md`: 24 parámetros globales + diámetros rosa + cota por loop, cada uno con certeza y fuente. Regla clave: tres capas de dosel 5.0/6.75/8.5, gálibo 3.0, cinta 6.0, agua por gravedad 10.5→0.
- 22 familias inventariadas → `KIT_OF_PARTS_STRATEGY.md` (estrategias A–E, 5 piezas candidatas a Tripo, resto paramétrico).

## E03 — Proxy (SOL_REFUGIO_3D_PROXY_v001.3dm)
- Constructor `proxy_build.py` (rhino3dm 8.32): XY exactas de `geometria_maestra.json`, Z del HEIGHT_SYSTEM. 17 capas, ~690 mallas, 82k triángulos, nombres CANOPY_LF_001/PINK_POD_014/etc., metros, personas 1.70 (18 ud), claros de metro como volúmenes.
- Errores y arreglos: ramas mástil→disco de hasta 11 m (absurdas) → radio máx 4.5 m; boquillas Ø1 m flotantes → Ø0.3 sin postes; torre del reloj invisible → Casa de Correos 17 m + torre 12 m + reloj + cupulín; copas flotando → recentradas; escaleras-torre macizas → zancas.

## E04 — Vistas humanas
- Visor clay three.js (local, sin CDN) + Edge headless; 21 cámaras a 1.65 m (accesos, bajo dosel, agua, cinta, hacia el reloj, aérea, axonometría).
- 3 cámaras nacieron dentro de manzanas OSM (huellas cóncavas: la manzana Preciados-Carmen baja hasta y≈+27) → recolocadas; hallazgo anotado (duda 8).

## E05 — Validación y corrección (5 iteraciones)
- Chequeos automáticos: ancho de paso (≥3 m) en 5 corredores, gálibo, claros de metro (r 5.5), esbeltos (≥0.8 m), soportes de cinta fuera de corredores, ocupación de suelo.
- Iteración 1: 4/5 corredores fallaban; bocas de Carmen/Cercanías/Alcalá invadidas. Culpables identificados automáticamente (tren SE sobre el eje, jardineras C2 sobre Preciados, diagonal de Carmen por el núcleo denso, estanque-riñón sobre Montera).
- Iteraciones 2–5: re-trazado de corredores por los huecos reales; puertas en orlas; recorte de colas de trenes (5 cáps); E-3 movido; LAB reubicado dos veces (bocas de Alcalá dentro del campo C3); árboles del eje movidos 4–5 m al sur; exclusión r5.5 en bocas.
- **Resultado final: 5/5 corredores CUMPLEN (3.68–6.83 m), gálibo 0 fallos, 7/7 bocas libres, esbeltos 0, ocupación 10.6 %.**
- Todo cambio vive en `geometria_overrides_f03a.json` (propuesta v1.1): la planta maestra de Fase 01 NO se ha tocado.

## E07/08 — Fragmento piloto
- Zona: nudo C2, caja (−4,−2)–(28,31) (32×33 m), la mejor documentada (12CA810C/29A08040/999C4F45).
- `PILOT_FRAGMENT.3dm`: 874 mallas, 58k tris. Discos con 10 nervios, aro y embudo de drenaje con bajante; mástiles ramificados en 2 tramos con cuba-jardinera; bancos con respaldo (0.45/0.85); estanque con murete, oleaje y parches de alga; cápsulas con gajos, válvula y amarres (2 colgadas); red rosa con goteros y abanicos de nebulización + vapor; cinta con barandilla de montantes y escalera de zancas y 16 peldaños; árbol de 3 ramas.
- 8 vistas (recorrido, bajo hojas, estancia, cápsulas, veg+estructura, hacia Correos, elevada, axono) → `PILOT_REFERENCE_COMPARISON.pdf` con su referencia más próxima y comparación de escala/densidad/altura/materialidad/espacio.
- Limitación anotada: el fragmento aislado no incluye contexto → VISTA06 no ve la Casa de Correos (validada en V07 del proxy completo).

## Decisiones de herramienta
- rhino3dm (Python) para escribir .3dm reales con capas/bloques/nombres — sin Rhino en esta máquina; los .3dm abren en el Rhino del autor.
- Grasshopper no ejecutable aquí: el paramétrico vive en los scripts (deterministas, misma fuente JSON); traducción a GH en 03B.
- Tripo: NO se ha generado nada — sólo lista y specs de input pack (KIT_OF_PARTS_STRATEGY).
- Render clay: three.js local + Edge headless (`--virtual-time-budget`), cámara por URL.
