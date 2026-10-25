# GEOMETRY_PURGE_REPORT — FASE 03B.8 §3

Escáner: `purge_scan.py` (escena interceptada completa, ~14.100 mallas + 69 curvas).
Clasificación CORRECTO / INTENCIONADO / SOSPECHOSO / ERROR. Criterio: **"no existe el error
en el modelo"**, no "no se ve en el render". Iterado junto al juicio visual (7 builds).

## Baseline v005-build0 (heredado de v004) → final v005

| Clase | build 0 | final | Resolución |
|---|---|---|---|
| Duplicados exactos | **443** | **0** | causa raíz: el clip/empuje del eje APILABA puntos en los tramos de fachada (215 postes clavados unos sobre otros) → re-muestreo uniforme del eje a 0.65 m tras el empuje, con filete puntual de esquinas cóncavas (ECI y Estación); dedupe central en `place()` para instancias |
| Z-fighting real | **33** | **0** | juntas de tablero fuera de los desembarcos; junta de pasarela sobre-cota; canaleta de pie fuera de la pletina; tapa/marco de registro separados; splash bajo la placa; discos misma-cota separados en el ORDEN correcto (fachada→separación→fachada) |
| Curvas casi-cero / de construcción visibles | 8 | **0** | círculo de respeto r8 fuera del máster (queda como dato de auditoría); falsos positivos de longitud XY corregidos en el escáner (3D) |
| Enterrados | 0 | 0 | — |
| Flotantes (ERROR) | 46 | **5** | agrupación por instancia de bloque (las piezas altas de un bloque no son flotantes); quedan 5 tropicales procedurales sobre jardineras elevadas — SOSPECHOSO documentado |
| Triángulos degenerados (ERROR) | 1.397 obj | **~49 obj** | dos clases INTENCIONADAS documentadas: costuras polares de primitivas del kit (esferas/conos N-seg, invisibles y uniformes) y slivers de fotoescaneo (limpiados en origen con `nondegenerate_faces`); el resto son costuras de abanico del huerto procedural — pendiente menor |

## Reglas nuevas (§4: nada termina sin explicación)

- **Barandilla**: cada tramo abierto termina en montante final + gancho pasamanos→travesaño +
  pletina; fragmentos <1.6 m se descartan; circuito cerrado se une (sin costura).
- **Cables**: tubo con flecha catenaria + casquillo de anclaje en AMBOS extremos; un tensor
  jamás cruza el volumen peatonal del tablero (descartado y registrado si lo haría).
- **Rebosaderos**: rematan en boquilla goteadora (el agua en vuelo no es geometría).
- **Niebla**: los volúmenes proxy (bolas cian) salen del máster; los postes llevan cabezal
  de anillo de boquillas real. La niebla volumétrica pertenece al render (scene_extra).
- **Mains enterradas** (−0.18) con línea de tapas de registro cada 9 m: trazado legible sin
  manguera gigante sobre el granito.
- **Instancia duplicada = suprimida y registrada** (dedupe central en `place()`).

Datos completos por objeto: `_purge_scan.json`. Ajustes registrados: `_guard_log.json`.
