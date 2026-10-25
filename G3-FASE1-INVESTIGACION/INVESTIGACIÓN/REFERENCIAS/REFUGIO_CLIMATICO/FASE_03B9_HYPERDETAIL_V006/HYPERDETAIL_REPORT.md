# HYPERDETAIL_REPORT — FASE 03B.9 · v005 → v006

Criterio de la fase: **"¿cuánto puedo acercarme antes de dejar de descubrir cosas?"**
Métrica: calidad perceptiva + coherencia física (no número de objetos).

## §2-§9 · BOTÁNICA (prioridad absoluta)
- **BOTANICAL_MASTERPLAN_v001.csv**: 17 especies REALES con hábito, altura, LAI, hídrica,
  tolerancia, estrategia estacional, uso y ubicación. Sin especies inventadas.
- **19 roles de asset** (9 de v005 + 10 nuevos del agente botánico, todo CC0/CC-BY en
  `ASSET_PROVENANCE.csv` + `_assets_veg2/provenance2.json`): por fin hay **árbol real**
  (olmo), monstera grande fenestrada, alocasia de pala, nenúfar, sedge, maíz por fases de
  crecimiento, segundo helecho, segundo arbusto fotoescaneado, gramínea alta.
- **Variantes anti-clon horneadas** por rol y LOD (espejo / joven 0.86 / maduro 1.12) con
  selección determinista por posición: dos plantas vecinas nunca son idénticas.
- **Balsa = microecosistema**: nenúfares en grupos de edades (diámetro real 1.3 m), juncos
  de dos especies, tallos emergentes, bultos de rizoma en la orilla.
- **Huerto**: mulch, línea de goteo con gotero por planta, plántula joven, hoja caída,
  maíz en fases junto a los cajones, tutores y etiquetas (de 03B.7/8).
- **LOD**: HERO<14 m / MID<62 / FAR perímetro; FAR re-basado a z=0 (los árboles ya no flotan).

## §10/§33 · VEGETACIÓN ≠ CLIMA — CLIMA RE-EJECUTADO
`_veg_clima.json`: por especie LAI → k_veg → transmitancia + volumen equivalente
(cilindro altura×diámetro). El modelo visual (miles de hojas) y el físico (extinción
volumétrica) quedan SEPARADOS y ligados por metadatos. **La simulación completa se
RE-EJECUTÓ sobre v006** (`_reclima9/`, CLIMATE_V006_MASTER.pdf): el vóxel de vegetación
lleva ahora un campo k_veg POR ESPECIE (Beer-Lambert con k acumulado por rayo, no un 0.40
global), el arbolado OSM existente se identifica por ancla (Platanus k=0.750) frente al
nuevo (Celtis k=0.633), y la evapotranspiración usa copa/LAI del masterplan
(20 árboles + 295 masas: 425 L/h · 286 kW vegetales). Resultados: sombra crítica
3.4 % → 42.3 %, ΔMRT −10.9 K medio (−28.2 K en refugio), ΔUTCI −2.6 K (−3.4 K con
nebulización), 3 876 m² de refugio (45.6 % del ámbito beneficiado).

## §11-§24 · CONSTRUCTIVO
- **Cables**: casquillo en ambos extremos + en el bajo tensor de cuerpo + horquilla con
  pasador (detalle 1:5 posible). Catenaria física de v005 se mantiene.
- **Canopy**: membrana panelizada (8 costuras radiales), rulo de borde, CÁMARA DE MICROALGAS
  con anillo, racores de entrada/salida y tapa de inspección por disco.
- **Cinta**: junta de dilatación transversal cada 18 m + tapa de mantenimiento cada 36 m
  (fuera de desembarcos), sobre el despiece/canaletas/sumideros/LED de fases previas.
- **Ascensor**: guías verticales, hojas de puerta con sensor en ambas cotas, umbral-guía,
  foso perimetral, ventilación de casetón, cuadro técnico.
- **Pods**: cinchas verticales, 4 ojales de base, refuerzo de corona, punto de inflado
  (sobre costuras/válvula/pletinas previas).
- **Depósitos-gota**: brida, purga con llave, placa de identificación.
- **Mobiliario**: testeros con tornillería vista.
- **Atrio Metro**: marquesina de boca con postes y placas, 6 bolardos luminosos, canal de
  drenaje perimetral.
- **Fachadas**: Correos con zócalo/puerta/15 marcos de hueco; ECI con cornisa y zócalo
  perimetrales.
- **Hidráulica**: mains y recirculación ENTERRADAS con líneas de tapas (trazado legible);
  tanque con filtro conceptual (bajante/válvula/volante/nivel/registro de 03B.8).

## §25-§26 · Purga continua y CERO RED
Purga tras cada build (8 builds): TOTAL ERROR 191 → **22** (4 dups de pletina en pliegue
cóncavo, 9 costuras de abanico PRIMARY/SAT, 6 tropicales sobre jardinera elevada,
3 tuberías ENTERRADAS a propósito — todo documentado, nada oculto).
**V-001/V-002 (1.12 m) resueltos por regla local** (planta compacta orientada al lado
contrario del eje). La reauditoría completa terminó en **0 RED · 26 YELLOW · 18 GREEN**
tras cuatro correcciones quirúrgicas más:
- **Marquesina del atrio**: la boca vive SOBRE la huella de la Estación; la marquesina
  vuela ahora hacia la plaza (+4.5 m) y protege la aproximación (penetraba 2.43 m).
- **Zócalo/cornisa del ECI por ARISTA**: una banda mitered cerrada sobre el footprint OSM
  cóncavo puenteaba los entrantes y su tapa (z 0.90) cortaba la bocacalle de Arenal en el
  raster peatonal; además el corredor declarado arenal-alcala roza la esquina del polígono
  (dato v002). Emisión por arista + omisión de aristas a <1.5 m del corredor (trasera sin
  cámaras: coste visual cero).
- **Canal del atrio**: el semianillo moría 0.63 m DENTRO del polígono declarado de la
  Estación; ahora se recorta contra ese polígono (el criterio del módulo A12, no el proxy).
- **Huerto**: cajón implantado en la ruta del tren de pods (V-037) → guarda de distancia
  4.5 m (7 cajones omitidos y registrados en el guard log; 15 supervivientes).

## §27-§29 · 30 microscenes + adversarial
120 tomas (30 puntos × 10m/2m/50cm/15cm) en `_micro/` (116 válidas), iteradas 2 veces.
Autocrítica y correcciones en `SELF_CRITIQUE_V006.md` (nenúfar gigante, recirc en superficie,
olmos flotando, postes apilados — todos corregidos).

## Entregables
Masters v006 (.3dm ×4) · geometria_maestra_v006.json + _v006_diff.json ·
BOTANICAL_MASTERPLAN_v001.csv · BOTANICAL_CONTACT_SHEET.pdf · ASSET_PROVENANCE.csv ·
_veg_clima.json · V005_V006_CLOSE_RANGE.pdf · SELF_CRITIQUE_V006.md · AUDIT_V006_MASTER.pdf ·
forense completo. v005 intacta.
