# HEIGHT_SYSTEM — REFUGIO CLIMÁTICO PUERTA DEL SOL
## Familia coherente de cotas · Fase 03A · 2026-08-07

Derivado de la medición sistemática de 17 renders interiores/sección (workflow de 4 analistas,
patrones de escala: persona 1,70 · farola fernandina 4,5–5 · planta madrileña 3,5 · banco 0,45).
Unidades: **metros**. Certeza: **CONFIRMED** (medible contra patrón claro en ≥2 imágenes) /
**INFERRED** (proporción indirecta o 1 imagen) / **SPECULATIVE** (sin información suficiente).

## Parámetros globales

| Parámetro | Valor | Rango obs. | Certeza | Fuente principal |
|---|---|---|---|---|
| `H_PERSON` | **1.70** | — | CONFIRMED | patrón |
| `H_WATER_FILM` | **0.03** | 0.03–0.15 | CONFIRMED | FBDF10B9, láminas técnicas (2–5 cm) |
| `H_PLANTING_BED` | **0.25** | 0.15–0.30 | CONFIRMED | 24D82F58 (bancales) |
| `H_SEATING` | **0.45** | 0.42–0.48 | CONFIRMED | universal en 8 imágenes |
| `H_POND_CURB` | **0.60** | 0.30–1.00 | CONFIRMED | 8DB970F0, 1C334300 (tipo 0.60) |
| `H_PLANTER` | **0.60** | 0.55–0.90 | CONFIRMED | 12CA810C, 29A08040 |
| `H_BENCH_BACK` | **0.85** | 0.80–0.90 | CONFIRMED | 29A08040 |
| `H_GROUND_TANK` | **1.35** | 1.2–1.5 | CONFIRMED | 24D82F58, 79405914 (depósito de suelo) |
| `H_CLEAR_MIN` | **3.00** | 2.8–3.2 | CONFIRMED | 12069BE7 (gálibo peatonal bajo bandejas) |
| `H_BRANCH_START` | **3.00** | 2.6–3.5 | CONFIRMED | 12069BE7, 79405914, FE41AB82 (arranque ramificación mástil) |
| `H_MISTING` | **4.00** | 3.5–5.0 | CONFIRMED | boquillas en bordes de capa baja y mástiles |
| `H_LOW_CANOPY` | **5.00** | 4.0–5.5 | CONFIRMED | cara inferior discos capa baja; calibrada con fernandina |
| `H_RIBBON` | **6.00** | 5.5–6.5 | CONFIRMED | 24D82F58 (pasarela vs PB de Casa de Correos) |
| `H_MID_CANOPY` | **6.75** | 6.0–7.5 | CONFIRMED | FE41AB82 (6–7), 29A08040, 999C4F45 |
| `H_LOGISTIC_RAIL` | **7.50** | 6.5–9 | INFERRED | 281A44BD (monorraíl 6.5–7.5), 1C334300 — *iteración: ver dudas* |
| `H_HIGH_CANOPY` | **8.50** | 8–9.5 | INFERRED | segunda piel 8–9 (FE41AB82); outliers 9–12 = SPECULATIVE |
| `H_PRIMARY_LOOP` | **8.0–11.0** (por loop) | 7–12 | INFERRED | tubo-cinta/arcos en clave 8–12; asignación por loop abajo |
| `H_TANK_TOWER` | **5.75** | 5–6 | INFERRED | 24D82F58 (torre de depósitos apilados) |
| `H_TANK_ELEV` | **10.50** | 10–12 | INFERRED | láminas técnicas (altura máx 10) + cenitales; riego por gravedad |
| `H_DOME_APEX` | **8.00** | — | SPECULATIVE | cúpula sólo en cenitales; sin patrón interior |
| `H_TREE_NEW` | **5.00** (copa 3.5–6.5) | 3.5–6 | CONFIRMED | árboles jóvenes de huerto/jardinera |
| `H_TREE_EXIST` | **7.00** | 5–8 | INFERRED | arbolado de calle existente |
| `H_LOW_VEGETATION` | **1.20** sobre contenedor | 0.5–2.5 | CONFIRMED | herbáceas/alocasias |
| `H_NURSERY_TOWER` | **3.00** | 3.0 | CONFIRMED | 79405914 (baldas cada 0.7–0.9) |
| `H_TOTEM` | **1.35** | 1.2–1.5 | INFERRED | tótems de datos/señalética |

## Diámetros de la familia rosa

| Pieza | Valor | Certeza | Nota |
|---|---|---|---|
| `D_POD_PEDESTRIAN` | **Ø2.25** | CONFIRMED | esferas de campo peatonal (8DB970F0) |
| `D_POD_TYPE` | **Ø3.25** | CONFIRMED | cápsula/esfera tipo (1C334300, B5C822AC, FE41AB82); apoyo 0–0.5 |
| `D_POD_LARGE` | **Ø4.5** | INFERRED | sólo en gridshell (8DB970F0) |
| `POD_TRAIN` (cápsula-depósito horizontal) | **Ø2.4 × 5.5, apoyo 0.3** | CONFIRMED | A2BD2AAA — **corrige la hipótesis de Fase 01: los trenes O y SE van APOYADOS en suelo** |
| `D_TANK_UNIT` | **Ø2.0** | INFERRED | cuerpo de torre de depósitos |
| `PIPE_TRUNK` | **Ø0.35** | CONFIRMED | tubo troncal rosa |
| `PIPE_HOSE` | **Ø0.09** | CONFIRMED | manguera manejable |

## Cotas de eje por loop (INFERRED — familia, no por pieza)

| Loop | Cota eje | Lógica |
|---|---|---|
| C1-L1 | 10.0 | loop mayor oeste, clave alta |
| C1-L2 / C1-L3 | 8.0 | lazos menores |
| C2-L1 | 11.0 | anillo exterior del nudo central (punto más alto del proyecto) |
| C2-L2 | 9.0 | anillo interior |
| C2-L3 | 7.5 | lazo de enganche |
| C3-L1 | 10.0 | loop este mayor |
| C3-L2 | 8.5 | loop solapado |

## Reglas de composición vertical (síntesis de los 4 lotes)
1. Zócalo modular 0.45: asiento 0.45 → jardinera 0.60 → respaldo 0.85 → barandilla 1.05.
2. Estrato libre peatonal: nada fijo entre 1.05 y 3.00 salvo cápsulas y vegetación.
3. Cielo verde en TRES capas escalonadas ~2 m: 5.0 / 6.75 / 8.5.
4. Nebulización emite a 4.0 (borde de capa baja) y humedece el estrato 0–3.
5. Recorrido elevado único a 6.0 (entre capa baja y media: se camina ENTRE hojas).
6. El agua siempre baja: 10.5 (depósito) → 8.5/6.75/5.0 (balsas-canopy) → 4.0 (niebla) → 0.60 (estanques) → 0.03 (lámina).
7. Gálibo mínimo bajo cualquier elemento firme sobre paso: 3.00.

## Dudas de altura (registradas en dudas_geometricas.md)
- Carril logístico (7.5) vs pasarela (6.0): ¿una o dos infraestructuras? Proxy: SOLO pasarela; carril = capa apagada.
- Cotas 9–12 de algunos discos: ¿capa 4a real o exageración de render? Proxy: máx 8.5 salvo balsas de C2.
- Cúpula: apex 8.0 especulativo.
- Esferas colgadas a 4–5 (999C4F45): minoritarias; proxy las mantiene sólo en racimo C2-N (2 ud).
