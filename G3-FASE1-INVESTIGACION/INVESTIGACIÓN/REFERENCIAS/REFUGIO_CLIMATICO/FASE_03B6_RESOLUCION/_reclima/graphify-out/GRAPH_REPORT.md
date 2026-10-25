# Graph Report - _reclima  (2026-08-11)

## Corpus Check
- 19 files · ~23,357 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 98 nodes · 194 edges · 10 communities (8 shown, 2 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- clima_report.py
- P
- clima_prep.py
- clima_run2.py
- clima_core.py
- penman_open_water
- build_voxels
- mrt
- sky_dirs
- lambda_v

## God Nodes (most connected - your core abstractions)
1. `P()` - 14 edges
2. `sheet()` - 12 edges
3. `close()` - 12 edges
4. `para()` - 12 edges
5. `table()` - 11 edges
6. `F()` - 9 edges
7. `mapa()` - 8 edges
8. `pdf_master()` - 8 edges
9. `plan()` - 7 edges
10. `pdf_shadow()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `crit()`  [INFERRED]
  clima_prep.py → clima_run.py
- `pdf_master()` --calls--> `P()`  [EXTRACTED]
  clima_report.py → clima_core.py
- `pdf_veg()` --calls--> `P()`  [EXTRACTED]
  clima_report.py → clima_core.py
- `add_water()` --calls--> `P()`  [EXTRACTED]
  clima_run2.py → clima_core.py
- `Ldown()` --calls--> `P()`  [EXTRACTED]
  clima_run.py → clima_core.py

## Import Cycles
- None detected.

## Communities (10 total, 2 thin omitted)

### Community 0 - "clima_report.py"
Cohesion: 0.33
Nodes (20): close(), F(), mapa(), para(), pdf_atlas(), pdf_master(), pdf_mist(), pdf_mrt() (+12 more)

### Community 1 - "P"
Cohesion: 0.11
Nodes (15): h_conv(), P(), Transmitancia solar de cada punto (X,Y,Z) en la direccion dvec. Devuelve (tau,…, perfil logaritmico de 10 m a la altura z., coeficiente de conveccion superficie-aire [W/m2K] — McAdams para placa rugosa., Resuelve el balance de energia de una superficie: Sabs + eps*Ldown -…, Temperatura de un elemento delgado suspendido en aire (hoja-canopy): conveccion…, surface_temp() (+7 more)

### Community 2 - "clima_prep.py"
Cohesion: 0.21
Nodes (14): abs_humidity(), dewpoint(), lambda_v(), main(), psat(), pvap(), presion de vapor de saturacion [Pa] — Buck (1981), sobre agua., temperatura de bulbo humedo [C] por iteracion sobre la ecuacion psicrometrica. (+6 more)

### Community 3 - "clima_run2.py"
Cohesion: 0.22
Nodes (7): add_water(), categoria(), clasifica(), L(), El salto de CATEGORIA de la escala UTCI es el criterio: no es un umbral…, expuesto: fraccion de radiacion directa que recibe la lamina (0-1).…, zona()

### Community 5 - "penman_open_water"
Cohesion: 0.47
Nodes (6): dewpoint(), penman_open_water(), psat(), pvap(), Evaporacion de lamina libre [kg/m2/s] — Penman (1948). CALCULADO. Rn [W/m2]…, wetbulb()

### Community 6 - "build_voxels"
Cohesion: 0.50
Nodes (4): build_voxels(), class_of(), estado 'A' = contexto existente (edificios + arbolado OSM) · 'B' = A +…, Clase optica del objeto. La hoja-canopy es un CONJUNTO (aro + nervios +…

### Community 7 - "mrt"
Cohesion: 0.50
Nodes (4): mrt(), proj_area_factor(), factor de area proyectada de una persona de pie frente al haz directo (Fanger)., Temperatura radiante media [C]. Modelo de dos hemisferios (F_sky = F_grd =…

### Community 8 - "sky_dirs"
Cohesion: 0.50
Nodes (4): vector unitario hacia el sol en el sistema del modelo (+X este, +Y norte, +Z…, devuelve (dirs, pesos) con pesos = cos(theta)*dOmega / pi (suma 1 en cielo…, sky_dirs(), sun_vector()

## Knowledge Gaps
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `P()` connect `P` to `clima_report.py`, `clima_run2.py`, `clima_core.py`, `mrt`?**
  _High betweenness centrality (0.266) - this node is a cross-community bridge._
- **Why does `crit()` connect `clima_prep.py` to `P`?**
  _High betweenness centrality (0.250) - this node is a cross-community bridge._
- **Should `P` be split into smaller, more focused modules?**
  _Cohesion score 0.10952380952380952 - nodes in this community are weakly interconnected._