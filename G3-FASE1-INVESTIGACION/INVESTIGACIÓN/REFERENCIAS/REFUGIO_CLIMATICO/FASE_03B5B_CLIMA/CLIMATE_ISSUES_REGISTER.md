# CLIMATE_ISSUES_REGISTER — FASE 03B.5B

Auditoría climática del modelo aprobado. **2026-08-10 · NADA HA SIDO CORREGIDO · EL MASTER NO SE HA MODIFICADO.**

Condición de evaluación: E2 TARDE CALUROSA, 16:00 h local, 21 de julio · Ta 34,7 °C · HR 15 % · viento 2,7 m/s. Clima real PVGIS v5.2 en 40,4169 N 3,7035 O.

| severidad | nº |
|---|---|
| RED | 2 |
| YELLOW | 4 |
| GREEN | 0 |

## CL-001 · INVIERNO — El dosel bloquea el 48 % de la radiacion de invierno

- **severidad:** YELLOW
- **posición:** afecta a un conjunto, sin posición puntual
- **magnitud:** 21 dic: 2.34 -> 1.21 kWh/m2·dia sobre el suelo del ambito
- **causa:** El dosel es fijo: la lamina de microalgas y la membrana no son estacionales, a diferencia de un arbolado caduco.
- **estrategias posibles (NO aplicadas):** Evaluar desmontaje estacional de una fraccion de discos · sustituir membrana por caduca en los discos sobre las zonas de estancia de invierno · aceptar y documentar la perdida.

## CL-002 · HOTSPOT — Quedan 4884 m2 de suelo pisable en estres termico muy fuerte

- **severidad:** RED
- **posición:** x=-8.8 y=-13.2
- **magnitud:** 24 zonas con UTCI>=38 C en E2 16:00; la mayor de 1756 m2 en (-9, -13) con UTCI 40.8
- **causa:** Zonas sin dosel, sin agua y sin nebulizacion: el proyecto no llega a ellas.
- **estrategias posibles (NO aplicadas):** No corregir todavia; identificadas para decidir si se amplia dosel, se anaden puntos de niebla o se aceptan como zonas de paso.

## CL-003 · AGUA — La mayor parte de la potencia evaporativa del agua esta en altura, no sobre el peaton

- **severidad:** YELLOW
- **posición:** afecta a un conjunto, sin posición puntual
- **magnitud:** Balsas + laminas de microalgas: 942.9 kW en altura frente a 213.9 kW a nivel de suelo (82 % del total)
- **causa:** La lamina de microalgas de los 67 discos suma 772 m2, muy por encima de los 399 m2 de agua a nivel de suelo.
- **estrategias posibles (NO aplicadas):** El agua en altura SI aporta: enfria la cara inferior del dosel y por tanto la carga radiante sobre el peaton. Pero no debe contabilizarse como enfriamiento del aire a nivel de calle.

## CL-004 · CINTA — El recorrido elevado es MAS calido que la plaza que sobrevuela

- **severidad:** RED
- **posición:** afecta a un conjunto, sin posición puntual
- **magnitud:** Cinta +6.00: solo 21 % del desarrollo en sombra - MRT 57.7 C - UTCI 38.2, frente a la plaza en estado B: MRT 53.7 C - UTCI 37.3. El viento ayuda (2.45 frente a 1.00 m/s) pero no compensa.
- **causa:** La cinta va a +6.00, por ENCIMA de la capa baja del dosel (discos a 4.2-5.6) y solo por debajo de la capa alta: en la mayor parte de su desarrollo esta al descubierto.
- **estrategias posibles (NO aplicadas):** No corregir todavia. A valorar: discos propios sobre la cinta, bajar tramos bajo la capa media, o aceptarla como recorrido de manana y tarde y no de mediodia.

## CL-005 · RECORRIDOS — Los corredores peatonales apenas mejoran

- **severidad:** YELLOW
- **posición:** afecta a un conjunto, sin posición puntual
- **magnitud:** Los 5 corredores declarados suman 2197 m2 y solo pasan de 4.2 a 21.5 % de sombra critica; dUTCI -1.07 K frente a -5.99 K bajo dosel.
- **causa:** La regla near_corr del generador mantiene los corredores LIBRES de dosel y mastiles: la misma decision que garantiza la transitabilidad los deja al sol.
- **estrategias posibles (NO aplicadas):** Decidir si el refugio debe cubrir tambien el movimiento o solo la estancia.

## CL-006 · AGUA — Las laminas finas se evaporan mas rapido de lo que su calado admite

- **severidad:** YELLOW
- **posición:** afecta a un conjunto, sin posición puntual
- **magnitud:** LAMINA MICROALGAS DISCOS x67: 11.1 mm/dia = 37 % de su calado cada dia de verano. Evaporacion total 20.7 m3/dia frente a 99.8 m3 en los depositos de +10.50: 4.82 dias de autonomia sin reposicion.
- **causa:** Mucha superficie de agua con muy poco calado: la lamina de microalgas suma 772 m2 a 3 cm.
- **estrategias posibles (NO aplicadas):** Dimensionar reposicion continua o recirculacion. Es un requisito de instalacion, no un defecto geometrico, pero condiciona el funcionamiento climatico real del dosel.

---

## Hotspots y coolspots

| id | x | y | m² | UTCI |
|---|---|---|---|---|
| CL-HOT-002 | -9 | -13 | 1756 | 40.8 |
| CL-HOT-020 | 45 | 43 | 1049 | 40.7 |
| CL-HOT-015 | -72 | 24 | 362 | 40.7 |
| CL-HOT-001 | -104 | -35 | 236 | 40.7 |
| CL-HOT-023 | -4 | 37 | 203 | 40.7 |
| CL-HOT-003 | -106 | -11 | 190 | 40.7 |
| CL-HOT-012 | -42 | 17 | 171 | 40.6 |
| CL-HOT-024 | -36 | 35 | 154 | 40.6 |
| CL-HOT-010 | -12 | 2 | 94 | 40.8 |
| CL-HOT-014 | -18 | 17 | 88 | 40.6 |
| CL-HOT-021 | 3 | 26 | 60 | 40.6 |
| CL-HOT-022 | -25 | 31 | 57 | 40.8 |
| CL-COOL-002 | 31 | 14 | 2050 | 33.5 |
| CL-COOL-001 | -52 | -0 | 460 | 34.1 |
| CL-COOL-003 | -49 | 5 | 356 | 33.3 |
| CL-COOL-006 | -63 | 20 | 160 | 32.9 |
| CL-COOL-005 | -20 | 5 | 34 | 34.3 |
| CL-COOL-004 | -14 | -4 | 28 | 34.4 |