# MAINTENANCE_PROTOCOL — FASE 03B.6 (CR-6)

Mandato: PROTOCOLO antes que mudanza. Los 56 componentes señalados como inaccesibles en 03B.5
no se re-implantan en masa; se les da **medio de acceso, hueco de paso o pieza técnica**, y solo
se recolocan los que además rompían otra regla (gotas, viveros, E-3).

## Clases de acceso
- **A0 (0–2.0 m)**: manual a pie. Splash, bancos, respaldos, canaleta, registros, huerto, tótems.
- **A1 (2.0–4.5 m)**: escalera manual apoyada en punto firme fuera de corredor. NEB (cabezal 4.0),
  brazos bajos de mástil, trepadoras, gotas (cono a 2.25).
- **A2 (>4.5 m)**: PEMP ligera (brazo articulado ≤250 kg/m²) estacionada EN corredor (≥3.0 m
  garantizados por 03A) fuera de horario de uso, o pates/plataforma fija donde hay poste.

## Piezas técnicas añadidas en v003
1. **Plataforma 1.2×1.2 + pates cada 0.40 m en los 6 postes de depósito** (+10.5): inspección del
   toro y del riser sin PEMP.
2. **3 registros técnicos 1.2×0.8×1.1** junto a cada cluster (C1 −69.5,15.5 · C2 12.5,31.5 ·
   C3 78,12): llaves de corte, filtrado y purga.
3. **Línea de recirculación por cluster** (tubo Ø0.18 a +0.26) registro → estanque → red: el agua
   de las láminas de microalgas ya no depende solo de las gotas (CL-006: 4.82 días de autonomía).
4. **Gotas re-espaciadas a 2.7 m entre centros** (hueco ≥1.1 m): paso de operario con herramienta.
5. **Viveros re-implantados** (62.5,19.5 / 59.5,10.5 / 55.5,16.5) con pasillo de servicio ≥1.5 m
   respecto al racimo de pods R-C3.
6. **Puertas de jardinera**: servicio D-C1-1 (−72,17) y apertura del bolsillo V-023 (6.9,−4.1).
7. **Nebulizadores de barandilla de la cinta** (8 uds): cabezal a +7.35 accesible desde el tablero.

## Rutinas
| Elemento | Frecuencia | Clase | Vía |
|---|---|---|---|
| Lámina microalgas (discos) | 14 días | A2 | PEMP desde corredor más próximo; embudo central drena a bajante |
| Cabezales NEB | 30 días | A1 | escalera manual, poste con guard de metro (nunca en boca) |
| Depósitos-toro | 90 días | A2 fija | pates + plataforma del poste |
| Gotas / cono de llenado | 30 días | A1 | hueco 1.1 m entre gotas |
| Registros + recirculación | 30 días | A0 | tapa practicable |
| Redes tensadas | 180 días | A2 | PEMP; revisar tensores en nudos de loop |
| Poda de formación (base copa ≥2.55) | 365 días | A1/A2 | según porte |

## Pendiente (documentado, no modelado)
- Drenaje del tablero de la cinta: limpieza de sumideros en los 8 puntos bajos (se documenta en
  03B6_BEFORE_AFTER; no se modela tubería en v003).
- La obstrucción medida por 03B.5 en D-C1-1 (holgura 0.50) no procede de las jardineras del JSON
  (vértice más cercano a 7.45 m); la reauditoría v003 arbitra si persiste y con qué geometría.
