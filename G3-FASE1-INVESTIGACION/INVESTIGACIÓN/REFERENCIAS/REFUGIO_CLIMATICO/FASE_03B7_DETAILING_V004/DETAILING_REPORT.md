# DETAILING_REPORT — FASE 03B.7 · LOD A/B/C sobre v004

Principio: **DETALLE INFORMACIONAL** — cada pieza nueva dice cómo se construye, se monta o se
mantiene el proyecto. Todo generado por regla (`detailing_03b7.py`: `upgrade_blocks` +
`site_details`), sin modelado manual. Metadatos `sistema/familia/version` en cada objeto.

## Métricas (medidas, `METRICAS_DETALLE_v004.json`)

| | v003 | v004 | Δ |
|---|---|---|---|
| Objetos de escena | 7 997 | **16 500+** | ~+107 % |
| Triángulos | 531 194 | **~743 000** | +40 % |
| Capa 19_DETALLE | — | **~3 470 obj / ~149 000 tris** | nueva |
| Capa 05_CABLES (tensores/péndolas) | 0 obj | ~294 obj | nueva en escena |
| Piezas por bloque (ej.) | escalera 35 | **escalera 118** · ascensor 29 · mástil 21–25 · gota 13 | ×2–×3 |

Conexiones LOD B/C nombradas en obra (conteo por interceptación): **1 468 pletinas**,
116 juntas, 42 luminarias, 42 manguitos, 23 sumideros, 22 alcorques, 21 mechinales,
19 registros de pavimento, 12 péndolas, verja (11), 6 gárgolas, aprons, fascia/goterón/canaleta.

## Por familia (qué se añadió)

- **§8 Cinta**: fascia + goterón continuo por ambos bordes, canaletas, junta de tablas cada
  0.62 m, sumideros cada 24 m, luminarias + manguitos cada 12 m, tira LED bajo pasamanos,
  pletina de base en cada montante de balaustrada.
- **§9 Escalera** (35 narices reales): montantes cada 3 huellas en ambos tramos, retorno de
  arranque, pletina de arranque, canaleta al pie, luminaria de meseta.
- **§10 Ascensor**: jambas + dintel + junta de hojas en ambas embocaduras (0.00 y +5.97),
  botonera, casetón técnico con 4 rejillas, pasamanos interior, piso de cabina.
- **§11 Discos-dosel**: kingpost + 3 tensores al aro, aro inferior doble, 6 manguitos
  nervio-aro, rebosadero + 3 puntos de goteo, labio de lámina de agua.
- **§12 Mástiles**: placa base con 4 pernos, casquillo de transición, abrazaderas, válvula de
  riego, collar; la bola-arbusto del tiesto se sustituye por mata foliar.
- **§13 Pods**: costuras meridianas y paralelas (tensión de membrana), válvula, 3 pletinas de
  pata; POD_TRAIN además: anillos de ventana, marco de puerta, faldón de base.
- **§14 Balsas elevadas**: aro inferior, gárgola-rebosadero con hilo de agua, péndolas.
- **§15 Gotas**: tapa sobre el ápice, válvula con volante, rebosadero, indicador de nivel,
  3 pletinas de pata. NEB: collar + válvula + cabezal cónico. Tótem: pantalla + base.
- **§16 Mobiliario**: canto de asiento y patas en bancos; coronación + mechinales de drenaje
  en jardineras.
- **§17 Vegetación v2 — especies reales, cero esferas**: árbol con tronco + ramas + abanicos
  foliares (`arbol_v2`, base libre 2.55); alocasia de palas curvas 14-seg (§7.1); gramíneas
  (14 hojas); trepadora = hélice + follaje adherido + derrame con guías; colgante = guías con
  hojas-quad; huerto con 3 cultivos + etiqueta; nenúfares con flor.
- **§18 Pavimento**: despiece 5.4 m enrasado (juntas H/V ≤1.4 cm, pisables), 8 registros con
  marco, alcorques en los árboles nuevos.
- **§19 Carlos III v2**: grupo ecuestre coherente (peana APOYADA — v003 la dejaba levitar
  1.1 m —, caballo pisando la peana con mano alzada, jinete con brazo y bicornio), 2 molduras,
  cola, **verja ceñida 3.5×2.6** (10 postes + doble riel).
- **§20 Contexto**: Correos con 3 filas × 15 huecos + portada + balcón + cornisa; Estación con
  costillas cada 2.6 m + espina + dintel-portal (gálibo 4.7); kioscos con cornisa + rótulo.

## Control 50 m / 10 m / 2 m / 50 cm

24 tomas de control (`_control/`, 4 dianas × 4 distancias + 8 reencuadres). Ronda única de
corrección tras el juicio visual: (1) grupo ecuestre reconstruido; (2) trepadora sin esferas;
(3) mata del mástil sin bola. A 50 cm se leen pletinas, pernos, juntas y abrazaderas; a 10 m
se leen los sistemas; a 50 m el conjunto no cambia (el detalle no ensucia la silueta).
El sombreado es del visor de control (clay/material): el juicio material fino pertenece a la
campaña de render post-v004.

## Coste geométrico

Bloques/instancias mantienen el rendimiento (16.5k objetos, 743k tris — Rhino y Cycles lo
digieren sin proxies). Sin optimización de coste por orden expresa (§7 del enunciado).

## Simplificaciones deliberadas (documentadas, no ocultas)

- Canaleta/fascia continuas cruzan el desembarco de escalera/ascensor: en obra se interrumpen;
  a este LOD la unión se declara en la auditoría como unión constructiva (A10 whitelist).
- Juntas de pavimento como relieve de 10–14 mm (grafismo constructivo pisable).
- Tornillería representada como pernos/pletinas ≥2 cm: visualmente relevante, no catálogo.
