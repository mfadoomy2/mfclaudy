# HEIGHT_SYSTEM v2 — FASE 03B.6

**Principio (mandato 03B.6): MANDA LA GEOMETRÍA APROBADA ACTUAL.** Este documento describe la
realidad construida del modelo v003; no impone un ideal previo. El HEIGHT_SYSTEM de 03A queda
superado como norma y conservado como archivo histórico.

## Bandas reales del dosel (medidas en v003)

| Banda | Cota (m) | Contenido |
|---|---|---|
| Suelo activo | 0.00 – 0.85 | pavimento, splash 0.03, canaleta 0.08 (cruces), tuberías 0.32, bancos 0.45, respaldos 0.85, bordillos/jardineras 0.60 |
| Cuerpo peatonal | 0.85 – 2.55 | pods (puertas), lab 0–3.5, tótems, registros 1.1, **poda de formación: ninguna copa baja de 2.55** |
| Dosel bajo | 4.2 – 5.6 | discos S/M perimetrales (los que trabajan), discos sombra-corredor a 5.0, brazos de mástil 5.4–6.4 |
| Cinta | 5.78 – 6.00 | tablero (6.00 pisable); barandilla completa: rodapié 6.10, travesaño 6.55, pasamanos 7.05 |
| Dosel medio | 6.1 – 7.4 | discos M/L del núcleo, balsas elevadas (B-C3b subida a 7.6), fuste de ascensor 0–7.4 |
| Dosel alto | 8.2 – 8.5 | discos XL y **sombra-cinta a 8.30** (regla: todo disco que cruza el tablero sube aquí) |
| Estructura | 7.5 – 11.0 | loops (LOOP_Z 7.5–11), redes tensadas z−0.4…−2.2 |
| Técnica | 10.5 | depósitos-toro (plataforma de inspección a 8.78 + pates) |

## Cotas nuevas en v003
- **Escaleras reales**: 35 CH de 0.171 / huella 0.29, en 2 tramos (18+17) + meseta a +3.09; llegada +6.00.
- **Ascensores-cápsula** (C1-O, C2-N, C3-E): fuste 0–7.4, cabina 0.15–3.3, embarque +5.97.
- **Carlos III**: grada 0.4 + pedestal hasta 2.8 + volumen ecuestre hasta ≈6.2 (G2+, r. respeto 8 m).
- **Gálibo bajo escalera**: faldón cerrado donde el paso libre es <2.20.

## Anomalías v002 resueltas
- Copas de ARBOL_A con base <2.55 → clamp `min_base` en `_lobed_crown` (V-025/V-030/V-067).
- Balsa B-C3b tocaba pasamanos (7.05) → cota 7.6 (V-06x).
- 7 discos atravesaban el tablero (5.2<cota<8.3 sobre el eje) → 8.30 con rol sombra-cinta.

Regla de mantenimiento del documento: si la geometría aprobada cambia, se re-mide y se re-escribe
esta tabla; nunca al revés.
