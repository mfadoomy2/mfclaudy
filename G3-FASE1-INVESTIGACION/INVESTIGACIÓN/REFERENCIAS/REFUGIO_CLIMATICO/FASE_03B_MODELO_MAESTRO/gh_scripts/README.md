# gh_scripts — definiciones paramétricas para Rhino/Grasshopper

Grasshopper no es ejecutable en el entorno de construcción (los .3dm se generan con rhino3dm).
El paramétrico vive en dos niveles:

1. **Los generadores Python de la fase** (`build_all_03b.py` + `mesh_kit.py`): deterministas,
   leen `geometria_maestra_v002.json` y regeneran TODO el modelo. Cambiar un parámetro
   (cota de loop, Ø de disco, sección) y re-ejecutar = el "Grasshopper" de esta fase.
2. **Estos scripts RhinoPython** (ejecutar DENTRO de Rhino con `RunPythonScript`): convierten
   las curvas generatrices de la capa `30_CURVES` en geometría NURBS nativa (pipes/sweeps
   reales, editables con historial), sustituyendo las mallas proxy donde se desee.

## Scripts
- `regen_pipes.py` — selecciona las curvas de `30_CURVES` (ejes de loops, cinta, tuberías,
  bajantes) y `05_CABLES` y genera Pipes NURBS con las secciones del proyecto
  (loop Ø0.60, satélites Ø0.20, tubería Ø0.32, cable Ø0.016).
- `leaf_canopy_gh.py` — reconstruye un LEAF_CANOPY como superficie NURBS (revolución
  deformada + nervios pipe) desde los parámetros L/W/drop/sag/ribs; úsalo para sustituir
  cualquier variante de bloque por la versión NURBS.

## Traducción a Grasshopper (03C)
Los dos scripts están escritos con `rhinoscriptsyntax`, trasladables 1:1 a GHPython.
La definición GH canónica debe tomar como inputs: la curva eje (o los 9 parámetros del
LEAF_CANOPY_MASTER) y devolver el Brep — misma lógica, mismos nombres de parámetros.
