# CLIMATE_ISSUES_REGISTER — FASE 03B.5B

Auditoría climática del modelo aprobado. **2026-08-10 · NADA HA SIDO CORREGIDO · EL MASTER NO SE HA MODIFICADO.**

Condición de evaluación: E2 TARDE CALUROSA, 16:00 h local, 21 de julio · Ta 34,7 °C · HR 15 % · viento 2,7 m/s. Clima real PVGIS v5.2 en 40,4169 N 3,7035 O.

| severidad | nº |
|---|---|
| RED | 2 |
| YELLOW | 3 |
| GREEN | 0 |

## CL-001 · INVIERNO — El dosel bloquea el 43 % de la radiacion de invierno

- **severidad:** YELLOW
- **posición:** afecta a un conjunto, sin posición puntual
- **magnitud:** 21 dic: 2.32 -> 1.32 kWh/m2·dia sobre el suelo del ambito
- **causa:** El dosel es fijo: la lamina de microalgas y la membrana no son estacionales, a diferencia de un arbolado caduco.
- **estrategias posibles (NO aplicadas):** Evaluar desmontaje estacional de una fraccion de discos · sustituir membrana por caduca en los discos sobre las zonas de estancia de invierno · aceptar y documentar la perdida.

## CL-002 · HOTSPOT — Quedan 5707 m2 de suelo pisable en estres termico muy fuerte

- **severidad:** RED
- **posición:** x=-21.8 y=-11.2
- **magnitud:** 17 zonas con UTCI>=38 C en E2 16:00; la mayor de 2636 m2 en (-22, -11) con UTCI 40.7
- **causa:** Zonas sin dosel, sin agua y sin nebulizacion: el proyecto no llega a ellas.
- **estrategias posibles (NO aplicadas):** No corregir todavia; identificadas para decidir si se amplia dosel, se anaden puntos de niebla o se aceptan como zonas de paso.

## CL-003 · AGUA — La mayor parte de la potencia evaporativa del agua esta en altura, no sobre el peaton

- **severidad:** YELLOW
- **posición:** afecta a un conjunto, sin posición puntual
- **magnitud:** Balsas + laminas de microalgas: 1152.8 kW en altura frente a 213.9 kW a nivel de suelo (84 % del total)
- **causa:** La lamina de microalgas de los 67 discos suma 1108 m2, muy por encima de los 399 m2 de agua a nivel de suelo.
- **estrategias posibles (NO aplicadas):** El agua en altura SI aporta: enfria la cara inferior del dosel y por tanto la carga radiante sobre el peaton. Pero no debe contabilizarse como enfriamiento del aire a nivel de calle.

## CL-004 · CINTA — El recorrido elevado es MAS calido que la plaza que sobrevuela

- **severidad:** RED
- **posición:** afecta a un conjunto, sin posición puntual
- **magnitud:** Cinta +6.00: solo 24 % del desarrollo en sombra - MRT 56.5 C - UTCI 37.9, frente a la plaza en estado B: MRT 54.6 C - UTCI 37.5. El viento ayuda (2.45 frente a 1.00 m/s) pero no compensa.
- **causa:** La cinta va a +6.00, por ENCIMA de la capa baja del dosel (discos a 4.2-5.6) y solo por debajo de la capa alta: en la mayor parte de su desarrollo esta al descubierto.
- **estrategias posibles (NO aplicadas):** No corregir todavia. A valorar: discos propios sobre la cinta, bajar tramos bajo la capa media, o aceptarla como recorrido de manana y tarde y no de mediodia.

## CL-005 · AGUA — Las laminas finas se evaporan mas rapido de lo que su calado admite

- **severidad:** YELLOW
- **posición:** afecta a un conjunto, sin posición puntual
- **magnitud:** LAMINA MICROALGAS DISCOS x94: 11.1 mm/dia = 37 % de su calado cada dia de verano. Evaporacion total 24.4 m3/dia frente a 99.8 m3 en los depositos de +10.50: 4.08 dias de autonomia sin reposicion.
- **causa:** Mucha superficie de agua con muy poco calado: la lamina de microalgas suma 1108 m2 a 3 cm.
- **estrategias posibles (NO aplicadas):** Dimensionar reposicion continua o recirculacion. Es un requisito de instalacion, no un defecto geometrico, pero condiciona el funcionamiento climatico real del dosel.

---

## Hotspots y coolspots

| id | x | y | m² | UTCI |
|---|---|---|---|---|
| CL-HOT-002 | -22 | -11 | 2636 | 40.7 |
| CL-HOT-015 | 46 | 47 | 1426 | 40.5 |
| CL-HOT-001 | -103 | -35 | 341 | 40.5 |
| CL-HOT-017 | -15 | 37 | 299 | 40.6 |
| CL-HOT-003 | -105 | -10 | 254 | 40.6 |
| CL-HOT-011 | -21 | 14 | 134 | 40.6 |
| CL-HOT-004 | -68 | -5 | 131 | 40.4 |
| CL-HOT-008 | -12 | 1 | 110 | 40.8 |
| CL-HOT-010 | -33 | 9 | 53 | 40.4 |
| CL-HOT-016 | -44 | 22 | 49 | 40.2 |
| CL-HOT-007 | 31 | 1 | 47 | 39.2 |
| CL-HOT-009 | 86 | 6 | 46 | 40.6 |
| CL-COOL-002 | 11 | 13 | 2941 | 33.4 |
| CL-COOL-003 | -72 | 3 | 139 | 33.8 |
| CL-COOL-006 | -50 | 17 | 46 | 33.2 |
| CL-COOL-005 | -20 | 5 | 32 | 34.1 |
| CL-COOL-001 | -66 | -16 | 28 | 34.6 |
| CL-COOL-004 | -14 | -4 | 28 | 34.5 |