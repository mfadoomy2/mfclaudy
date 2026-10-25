# REGISTRO — FASE 03B (del proxy al modelo arquitectónico editable)
2026-08-07 · expectativa → acción → resultado → interpretación → rectificación
**ESTADO: FASE 03B APROBADA Y CERRADA POR EL AUTOR (2026-08-07).**

## D03B-05 — CONCLUSIÓN METODOLÓGICA (decisión del autor, Opción ②)
**La generación IA 3D (Tripo) se descarta para la familia POD**: no aporta suficiente valor frente
al sistema paramétrico para justificar dependencia de plataforma, coste por generación y pérdida de
editabilidad. `PINK_POD_BASE` queda establecido como **MASTER geométrico definitivo** de la familia.
El 20–25 % de detalle visual restante (arrugas, tensión superficial, costuras, asimetrías,
imperfecciones) se resolverá en 03C prioritariamente mediante: material · normal maps ·
bump/displacement controlado · roughness · translucencia · pequeñas deformaciones geométricas
NO destructivas · variación entre instancias. No activar suscripción ni nuevos intentos de Tripo.
Los multiview packs y el mapeo del workflow quedan ARCHIVADOS en `tripo\` para posible reutilización
futura; la vía se considera cerrada en el estado actual.

## Decisiones de revisión aplicadas
- **D03B-01** trenes apoyados (cota semántica + apoyo 0.3 en v002); **P01 regenerado como v2.2** desde v002 (v2.1 archivada). Corregido también el borde norte del polígono gráfico (duda 8).
- **D03B-02** claro de metro r 5.5 mantenido (exclusiones consolidadas en v002).
- **D03B-03** LAB junto a viveros aceptado (centroide ≈ 60,16, junto a las 3 torres-vivero).
- **D03B-04 cúpula**: solución de **APERTURA + MODIFICACIÓN DE APOYO** — se conserva posición y Ø13 (fidelidad a F295448F) pero el casquete arranca a **+3.2** sobre 6 apoyos perimetrales con óculo cenital Ø3: la cúpula pasa de obstáculo a pérgola atravesable (gálibo ≥3.0). Cambio geométrico mínimo; el corredor de Montera mantiene además su rodeo validado (doble seguridad).
- Dudas resueltas autónomamente (ver `geometria_maestra_v002.json → resoluciones_03b`): una sola cinta (+6), sin 4ª capa de dosel, materialidad madera laminada/bambú + nudos acero + red rosa TPU, lámina de microalgas en TODOS los discos, Sol sin fuentes, 2 esferas colgadas en C2-N.

## Construcción
- `geometria_maestra_v002.json` = Fase01 + overrides aprobados + decisiones (la de Fase 01 INTACTA).
- **28 bloques Rhino** (instanciados con rotación vía `Transform.Multiply`): 9 variantes LEAF_CANOPY (S1,S2,M1,M2,MT,OV,L1,LT,XL — aro+nervios+membrana con flecha+lámina de agua+embudo+bajante+orejetas), 3 mástiles (1/2/3 brazos con cuba y boquilla), PODs S/M/L con gajos/válvula/pies/aro de puerta, POD_TRAIN zunchado con cunas, DROP_TANK, NURSERY, 3 árboles, TROPICAL/SHRUB/AQUATIC/CLIMBER, PERSON, NEB_POST, TOTEM.
- Estructura: haz triple por loop (Ø0.60 + satélites) con traviesas c/2.4 y nudos c/7; cinta con barandilla y montantes, 38 soportes con capitel fuera de corredores, 6 escaleras de zanca; redes tensadas (cables + velo); depósitos torales a +10.5 con bajante.
- **Curvas generatrices editables** en capa `30_CURVES` (ejes de loops, cinta, tuberías, aros de balsa) + cables como curvas: los scripts `gh_scripts/` las convierten en Pipes NURBS dentro de Rhino.
- Archivos: `MASTER_ARCHITECTURE_v002.3dm` (arquitectura sin vegetación full), `ASSET_LIBRARY_v001.3dm` (28 masters + ejemplar + TextDot), `SOL_FULL_SCENE_v001.3dm` (todo, 4.076 mallas · 277k tris en visor).

## Validación
- 20 vistas humanas clay a 1.65 (V01–V20, incluye V07 y V20 con el reloj visible) + clay overview aérea y axonométrica + 9 vistas de test material (madera cálida, rosa/verde translúcido, agua) — checks A–H revisados: transitable, público, estancias, cielo visible, vegetación acompaña, cápsulas de la familia, estructura legible, reloj presente.
- **6 secciones arquitectónicas** (S01/S02 longitudinales + S03–S06 transversales) cortadas del modelo real por familias con alzado en profundidad y niveles del HEIGHT_SYSTEM → `SECCIONES_03B.pdf`. La verticalidad queda verificada: dosel 5/6.75/8.5, cinta +6, depósitos +10.5, gálibo 3.0.
- `03B_REFERENCE_COMPARISON.pdf`: 10 pares (8 clay + 2 material) — cada render se explica como vista de un mismo proyecto.

## Tripo
- 5 **multiview packs** generados (FRONT/LEFT/BACK/RIGHT × 1024px, fondo neutro, mismo objeto por construcción — se renderiza el propio bloque paramétrico orbitando la cámara).
- Template real localizado: `api_tripo3_1_multiview_to_model` (Tripo H3.1; nodos LoadImage 44=front, 45=left, 46=back). Imágenes del POD ya subidas a Comfy Cloud.
- **Generación NO lanzada**: pasarela de gasto (~63 créditos/pieza ≈ 315 créditos las 5). A la espera de confirmación explícita del autor. El PINK_POD_BASE paramétrico ya resuelve ~75 % de la necesidad (gajos, válvula, apoyos, amarres, puerta); Tripo aporta el detalle orgánico de la pieza héroe de primer plano.

## Adenda — lanzamiento del POD (aprobado por el autor)
- Expectativa: generar el POD con `api_tripo3_1_multiview_to_model` (~63 créditos autorizados).
- Acción: `run_template` con confirm y las 3 vistas subidas (44=FRONT, 45=LEFT, 46=BACK).
- Resultado: **rechazado por la plataforma — "Partner-node workflows require a paid subscription"**. Autenticación OAuth correcta, entorno production: el bloqueo es la falta de suscripción de pago del workspace Comfy Cloud. **0 créditos consumidos.**
- Interpretación: no es fallo del pack ni del workflow (verificados); es plan de cuenta.
- Entregado en su lugar: `TRIPO_POD_EVALUATION.pdf` con el pack multiview, la versión paramétrica, su aplicación en el modelo (racimo C2-N) y el análisis de qué aportaría Tripo (~20-25 % restante: arrugas de membrana inflada, asimetría orgánica, detalle de costura — sólo relevante en primeros planos de 03C).
- Decisión pendiente del autor: ① suscribir el workspace y regenerar sólo el POD, o ② descartar Tripo para la familia POD (criterio declarado: no insistir por inercia).
- Tiempos: preparación de packs y subidas ~25 min; limpieza no ejecutada.

## Errores y rectificaciones
- `get_template_schema` devolvió slots:null → mapeo por inspección del JSON del template (10 nodos).
- Guardia `__main__` añadida a build_all_03b para reutilizar las familias en tripo_packs sin reconstruir.
- Rutas con `..` sin normalizar rompían PIL en Windows (MAX_PATH) → normpath.
