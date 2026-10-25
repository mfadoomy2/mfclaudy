# ISSUES_REGISTER â€” FASE 03B.5

AuditorÃ­a geomÃ©trica y de viabilidad del modelo aprobado (`MASTER_ARCHITECTURE_v002.3dm` / `SOL_FULL_SCENE_v001.3dm`, escena E02 con 6.672 mallas y 394.610 triÃ¡ngulos).
**2026-08-10 Â· NADA HA SIDO CORREGIDO Â· EL MASTER NO SE HA MODIFICADO.**

| severidad | nÂº | criterio de clasificaciÃ³n |
|---|---|---|
| ðŸ”´ RED | 5 | impide el uso previsto, o incumple un criterio declarado por el propio proyecto |
| ðŸŸ¡ YELLOW | 28 | funciona pero al lÃ­mite, o depende de una decisiÃ³n pendiente |
| ðŸŸ¢ GREEN | 18 | anotaciÃ³n de coherencia documental, sin efecto sobre el uso |

> Los umbrales usados (1,80 / 3,00 m de anchura Â· 3,00 m de gÃ¡libo Â· 5,5 m de banda de Metro) son criterios de trabajo tomados del HEIGHT_SYSTEM y de la decisiÃ³n D03B-02. **No se ha aplicado ninguna normativa**: la identificaciÃ³n de la norma aplicable es el paso siguiente.

## ðŸ”´ RED (5)

### V-001 Â· RECORRIDOS â€” Estrechamiento en eje-mayor-alcala (s=52 m)

- **posiciÃ³n:** x=-44.0  y=-11.2  z=0.00
- **magnitud:** holgura libre 1.12 m sobre el eje (ancho transversal disponible 17.2 m)
- **causa:** obstaculos laterales: VEGETATION / PLANTER
- **severidad:** RED
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral Â· reducir radio de jardinera Â· desplazar el eje del corredor
- **evidencia:** capÃ­tulo A1 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-002 Â· RECORRIDOS â€” Estrechamiento en carmen-correos (s=36 m)

- **posiciÃ³n:** x=-13.0  y=33.7  z=0.00
- **magnitud:** holgura libre 1.12 m sobre el eje (ancho transversal disponible 30.5 m)
- **causa:** obstaculos laterales: VEGETATION / ABIERTO
- **severidad:** RED
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral Â· reducir radio de jardinera Â· desplazar el eje del corredor
- **evidencia:** capÃ­tulo A1 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-040 Â· COLISIONES â€” Interpenetracion PODSÃ—VEGETATION: POD_TRAIN Ã— VEGA_HELECHO_M

- **posiciÃ³n:** x=-58.0  y=11.9  z=0.19
- **magnitud:** 7 voxeles de 0.20 m (0.056 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** desplazar la instancia Â· reducir el radio de la copa Â· excluir la posicion en el generador
- **evidencia:** capÃ­tulo A10 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-041 Â· COLISIONES â€” Interpenetracion PODSÃ—VEGETATION: POD_TRAIN Ã— VEG2_HUERTO

- **posiciÃ³n:** x=-57.5  y=11.2  z=0.13
- **magnitud:** 7 voxeles de 0.20 m (0.056 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** desplazar la instancia Â· reducir el radio de la copa Â· excluir la posicion en el generador
- **evidencia:** capÃ­tulo A10 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-042 Â· COLISIONES â€” Interpenetracion PLANTERÃ—RIBBON: MAST_2 Ã— RIB_SUP

- **posiciÃ³n:** x=8.1  y=24.9  z=0.28
- **magnitud:** 7 voxeles de 0.20 m (0.056 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** desplazar la instancia Â· reducir el radio de la copa Â· excluir la posicion en el generador
- **evidencia:** capÃ­tulo A10 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

## ðŸŸ¡ YELLOW (28)

### V-003 Â· RECORRIDOS â€” Estrechamiento en eje-mayor-alcala (s=32 m)

- **posiciÃ³n:** x=-63.4  y=-12.8  z=0.00
- **magnitud:** holgura libre 2.00 m sobre el eje (ancho transversal disponible 17.8 m)
- **causa:** obstaculos laterales: PODS / PLANTER
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral Â· reducir radio de jardinera Â· desplazar el eje del corredor
- **evidencia:** capÃ­tulo A1 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-004 Â· RECORRIDOS â€” Estrechamiento en montera-espozymina (s=67 m)

- **posiciÃ³n:** x=37.0  y=-4.1  z=0.00
- **magnitud:** holgura libre 2.00 m sobre el eje (ancho transversal disponible 26.8 m)
- **causa:** obstaculos laterales: PODS / WATER
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral Â· reducir radio de jardinera Â· desplazar el eje del corredor
- **evidencia:** capÃ­tulo A1 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-005 Â· RECORRIDOS â€” Estrechamiento en carmen-correos (s=67 m)

- **posiciÃ³n:** x=-20.9  y=5.2  z=0.00
- **magnitud:** holgura libre 2.12 m sobre el eje (ancho transversal disponible 7.5 m)
- **causa:** obstaculos laterales: PLANTER / PLANTER
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral Â· reducir radio de jardinera Â· desplazar el eje del corredor
- **evidencia:** capÃ­tulo A1 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-006 Â· RECORRIDOS â€” Estrechamiento en montera-espozymina (s=56 m)

- **posiciÃ³n:** x=43.9  y=0.3  z=0.00
- **magnitud:** holgura libre 2.24 m sobre el eje (ancho transversal disponible 10.5 m)
- **causa:** obstaculos laterales: PLANTER / WATER
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral Â· reducir radio de jardinera Â· desplazar el eje del corredor
- **evidencia:** capÃ­tulo A1 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-007 Â· RECORRIDOS â€” Estrechamiento en montera-espozymina (s=26 m)

- **posiciÃ³n:** x=40.0  y=30.0  z=0.00
- **magnitud:** holgura libre 2.50 m sobre el eje (ancho transversal disponible 29.5 m)
- **causa:** obstaculos laterales: PLANTER / WATER
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral Â· reducir radio de jardinera Â· desplazar el eje del corredor
- **evidencia:** capÃ­tulo A1 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-008 Â· RECORRIDOS â€” Huecos de 0.50 m interiores a las estancias ajardinadas: 20

- **posiciÃ³n:** x=17.9  y=-5.1  z=0.00
- **magnitud:** 20 huecos <1.20 m a >3 m de todo eje declarado
- **causa:** textura densa intencional de los parterres (capas jardinera+mata+agua); no son pasos de la red
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** sin accion: son estancias; revisar solo si un itinerario nuevo los atraviesa
- **evidencia:** capÃ­tulo A1 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-011 Â· GALIBOS â€” Copas de arbolado E02 por debajo de 2,50 m sobre suelo pisable (11 puntos)

- **posiciÃ³n:** x=58.6  y=22.1  z=2.31
- **magnitud:** 3.4 m2 de suelo pisable bajo copa a menos de 2,50 m Â· minimo 2.31 m Â· bloques implicados: VEG2_TROPICAL Â· envolvente de cabeza de la persona de referencia 1,85 m
- **causa:** los bloques VEG2_ARBOL_A/B/EX generan la copa como esfera lobulada sin faldon libre de tronco: la copa arranca a 0.62Â·h y el lobulo inferior baja hasta 2,21 m
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** poda de formacion a 2,20â€“2,50 m (practica normal de arbolado urbano) Â· o elevar el centro de copa en el bloque VEG2_ARBOL. NO es incumplimiento de la regla 7 del HEIGHT_SYSTEM: una copa no es Â«elemento firmeÂ». Se registra para que la decision sea explicita.
- **evidencia:** capÃ­tulo A2 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-013 Â· ALTURAS â€” H_SEATING fuera de rango declarado

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** declarado 0.45 (rango [0.42, 0.48]) Â· construido 0.64
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capÃ­tulo A3 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-015 Â· ALTURAS â€” H_GROUND_TANK fuera de rango declarado

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** declarado 1.35 (rango [1.2, 1.5]) Â· construido 2.31
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capÃ­tulo A3 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-016 Â· ALTURAS â€” H_NURSERY_TOWER fuera de rango declarado

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** declarado 3.0 (rango [3.0, 3.0]) Â· construido 3.32
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capÃ­tulo A3 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-017 Â· ALTURAS â€” H_CLEAR_MIN fuera de rango declarado

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** declarado 3.0 (rango [2.8, 3.2]) Â· construido 2.8
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capÃ­tulo A3 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-020 Â· ALTURAS â€” FAMILIA_DOSEL fuera de rango declarado

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** declarado 5.0/6.75/8.5 (rango ['Â±0.30', '']) Â· construido 28 de 94 discos fuera
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capÃ­tulo A3 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-023 Â· CINTA â€” Radio de curvatura minimo de la cinta 0.0 m

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** radio minimo 0.0 m (p01 0.5 m) para un tablero de 2.50 m de ancho
- **causa:** la traza se genero como polilinea de 371 puntos sin control de curvatura
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** suavizar la generatriz en 30_CURVES manteniendo los puntos de acometida de escalera
- **evidencia:** capÃ­tulo A4 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-025 Â· ACCESIBILIDAD â€” Itinerario eje-mayor-alcala accesible salvo puntos criticos

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** ancho minimo 1.12 m (p05 3.39 m)
- **causa:** estrechamientos puntuales
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** liberar los estrechamientos listados en A1
- **evidencia:** capÃ­tulo A5 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-026 Â· ACCESIBILIDAD â€” Itinerario carmen-correos accesible salvo puntos criticos

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** ancho minimo 1.12 m (p05 2.57 m)
- **causa:** estrechamientos puntuales
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** liberar los estrechamientos listados en A1
- **evidencia:** capÃ­tulo A5 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-027 Â· ACCESIBILIDAD â€” Itinerario montera-espozymina accesible salvo puntos criticos

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** ancho minimo 1.50 m (p05 2.34 m)
- **causa:** estrechamientos puntuales
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** liberar los estrechamientos listados en A1
- **evidencia:** capÃ­tulo A5 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-030 Â· METRO â€” Acceso Cercanías: 1 elementos a nivel de boca dentro de la banda 5,5 m

- **posiciÃ³n:** x=57.0  y=-5.4  z=0.00
- **magnitud:** obstaculo fisico mas proximo a 5.49 m (VEGA_HELECHO_M) Â· ancho libre frontal minimo 5.75 m Â· familias VEGETATION
- **causa:** la banda de exclusion de D03B-02 se aplico a discos y mastiles, pero la vegetacion E02 y las piezas menores se implantaron despues con reglas propias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** auditar la banda contra el criterio real de Metro de Madrid Â· retirar los invasores a nivel de boca Â· mantener libre el frente de evacuacion
- **evidencia:** capÃ­tulo A6 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-033 Â· METRO â€” Acceso Alcalá: 1 elementos a nivel de boca dentro de la banda 5,5 m

- **posiciÃ³n:** x=46.9  y=18.9  z=0.00
- **magnitud:** obstaculo fisico mas proximo a 4.75 m (LAB02) Â· ancho libre frontal minimo 6.75 m Â· familias PODS
- **causa:** la banda de exclusion de D03B-02 se aplico a discos y mastiles, pero la vegetacion E02 y las piezas menores se implantaron despues con reglas propias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** auditar la banda contra el criterio real de Metro de Madrid Â· retirar los invasores a nivel de boca Â· mantener libre el frente de evacuacion
- **evidencia:** capÃ­tulo A6 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-034 Â· METRO â€” Acceso Alcalá: 1 elementos a nivel de boca dentro de la banda 5,5 m

- **posiciÃ³n:** x=40.2  y=12.0  z=0.00
- **magnitud:** obstaculo fisico mas proximo a 5.16 m (VEG2_TROPICAL) Â· ancho libre frontal minimo 5.75 m Â· familias VEGETATION
- **causa:** la banda de exclusion de D03B-02 se aplico a discos y mastiles, pero la vegetacion E02 y las piezas menores se implantaron despues con reglas propias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** auditar la banda contra el criterio real de Metro de Madrid Â· retirar los invasores a nivel de boca Â· mantener libre el frente de evacuacion
- **evidencia:** capÃ­tulo A6 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-038 Â· MANTENIMIENTO â€” BOMBEO: 1 de 3 componentes sin acceso de mantenimiento

- **posiciÃ³n:** x=-70.0  y=22.0  z=0.00
- **magnitud:** holgura pisable adyacente mediana 0.00 m (se requieren 0.90 m)
- **causa:** el elemento queda rodeado de jardinera/vegetacion/agua o sin superficie de apoyo para plataforma elevadora
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reservar un area tecnica de 2.5x2.5 m junto a cada unidad Â· pasarela tecnica Â· acceso desde la cinta
- **evidencia:** capÃ­tulo A9 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-039 Â· MANTENIMIENTO â€” CANOPY / BAJANTE: 1 de 94 componentes sin acceso de mantenimiento

- **posiciÃ³n:** x=2.1  y=7.1  z=8.50
- **magnitud:** holgura pisable adyacente mediana 2.24 m (se requieren 2.50 m)
- **causa:** el elemento queda rodeado de jardinera/vegetacion/agua o sin superficie de apoyo para plataforma elevadora
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reservar un area tecnica de 2.5x2.5 m junto a cada unidad Â· pasarela tecnica Â· acceso desde la cinta
- **evidencia:** capÃ­tulo A9 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-043 Â· COLISIONES â€” Interpenetracion DETAILÃ—VEGETATION: BENCH_CANTO_1_0 Ã— VEGA_HELECHO_H

- **posiciÃ³n:** x=-1.7  y=8.8  z=0.44
- **magnitud:** 6 voxeles de 0.20 m (0.048 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia Â· reducir el radio de la copa Â· excluir la posicion en el generador
- **evidencia:** capÃ­tulo A10 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-044 Â· COLISIONES â€” Interpenetracion DETAILÃ—VEGETATION: LIFT_TOWER Ã— VEGA_HELECHO_F

- **posiciÃ³n:** x=77.0  y=5.5  z=0.74
- **magnitud:** 6 voxeles de 0.20 m (0.048 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia Â· reducir el radio de la copa Â· excluir la posicion en el generador
- **evidencia:** capÃ­tulo A10 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-045 Â· COLISIONES â€” Interpenetracion DETAILÃ—WATER: DECK_JUNTAS Ã— BASIN_B-C1a

- **posiciÃ³n:** x=-56.0  y=9.0  z=6.00
- **magnitud:** 6 voxeles de 0.20 m (0.048 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia Â· reducir el radio de la copa Â· excluir la posicion en el generador
- **evidencia:** capÃ­tulo A10 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-046 Â· COLISIONES â€” Interpenetracion CABLEÃ—STRUCTURE: LCBL Ã— PRIMARY_C2-L2

- **posiciÃ³n:** x=17.7  y=5.1  z=8.86
- **magnitud:** 6 voxeles de 0.20 m (0.048 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia Â· reducir el radio de la copa Â· excluir la posicion en el generador
- **evidencia:** capÃ­tulo A10 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-047 Â· COLISIONES â€” Interpenetracion CABLEÃ—STRUCTURE: LCBL Ã— SAT_C3-L2

- **posiciÃ³n:** x=62.1  y=-2.4  z=8.24
- **magnitud:** 6 voxeles de 0.20 m (0.048 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia Â· reducir el radio de la copa Â· excluir la posicion en el generador
- **evidencia:** capÃ­tulo A10 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-048 Â· COLISIONES â€” Interpenetracion PODSÃ—VEGETATION: POD_TRAIN Ã— VEGA_GRAMINEA_M

- **posiciÃ³n:** x=-59.2  y=9.4  z=0.18
- **magnitud:** 6 voxeles de 0.20 m (0.048 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia Â· reducir el radio de la copa Â· excluir la posicion en el generador
- **evidencia:** capÃ­tulo A10 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-049 Â· COLISIONES â€” Interpenetracion RIBBONÃ—WATER: RIBBON_DECK Ã— BASIN_B-C1a

- **posiciÃ³n:** x=-56.0  y=9.0  z=6.00
- **magnitud:** 6 voxeles de 0.20 m (0.048 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia Â· reducir el radio de la copa Â· excluir la posicion en el generador
- **evidencia:** capÃ­tulo A10 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

## ðŸŸ¢ GREEN (18)

### V-009 Â· RECORRIDOS â€” La red peatonal principal se mantiene continua a 3,00 m de holgura

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** con exigencia de 3,00 m continuos sigue conectado el 77 % del suelo libre en 1 componentes (el mayor de 7849 m2); a 1,80 m, el 87 %
- **causa:** â€”
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capÃ­tulo A1 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-010 Â· ACCESIBILIDAD â€” El plano de plaza es horizontal en todo el ambito

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** cota 0.00 en toda la superficie construida: 0 %% de pendiente longitudinal y transversal a nivel de suelo
- **causa:** el modelo 03B resuelve la plaza como plano unico
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** verificar en fases posteriores la pendiente real de evacuacion de agua superficial (0 %% no drena)
- **evidencia:** capÃ­tulo A5 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-012 Â· GALIBOS â€” Ningun cable tensado invade el estrato peatonal

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** 37 cables comprobados Â· cota minima absoluta 7.80 m (anclaje de mastil en H_BRANCH_START 3.00)
- **causa:** â€”
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capÃ­tulo A2 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-014 Â· ALTURAS â€” H_BENCH_BACK declarado pero no construido

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** NO construido: respaldo
- **causa:** decision de proyecto (D9 / simplificacion 03B)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** retirar del HEIGHT_SYSTEM o marcarlo como reserva
- **evidencia:** capÃ­tulo A3 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-018 Â· ALTURAS â€” H_TANK_TOWER declarado pero no construido

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** NO construido: torre de depositos apilados
- **causa:** decision de proyecto (D9 / simplificacion 03B)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** retirar del HEIGHT_SYSTEM o marcarlo como reserva
- **evidencia:** capÃ­tulo A3 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-019 Â· ALTURAS â€” H_LOGISTIC_RAIL declarado pero no construido

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** NO construido: carril logistico (G4 apagada, D9)
- **causa:** decision de proyecto (D9 / simplificacion 03B)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** retirar del HEIGHT_SYSTEM o marcarlo como reserva
- **evidencia:** capÃ­tulo A3 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-021 Â· CINTA â€” Escaleras reales: 37 CH de 0.162 m, meseta y doble pasamanos

- **posiciÃ³n:** x=-73.3  y=-2.0  z=3.00
- **magnitud:** CH=0.162 m Â· H=0.290 m Â· 2CH+H=0.61 m Â· 2 tramos + meseta 1.50 Â· zanca cerrada
- **causa:** regla corregida en 03B.6: bloque STAIR_SB sustituye a la zanca inclinada de v002
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** â€”
- **evidencia:** capÃ­tulo A4 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-022 Â· ACCESIBILIDAD â€” La cota +6.00 dispone de 3 ascensores-capsula ademas de 6 escaleras

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** 3 LIFT_TOWER medidos en la escena (C1-O, C2-N, C3-E); embarque a +5.97
- **causa:** regla corregida en 03B.6: ascensores integrados en los nodos de la cinta
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** definir cabina/maquinaria en fase de proyecto tecnico
- **evidencia:** capÃ­tulo A4/A5 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-024 Â· CINTA â€” La rasante de la cinta es plana y continua

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** 519 m a cota +6.00 constante: pendiente longitudinal 0.0 % y transversal 0.0 %; galibo bajo tablero 5.78 m
- **causa:** â€”
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** revisar no obstante la pendiente transversal: 0.0 %% implica que el tablero no evacua agua
- **evidencia:** capÃ­tulo A4 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-028 Â· ACCESIBILIDAD â€” Barandilla de cinta completa: pasamanos 1.05 + travesano 0.55 + rodapie 0.10

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** niveles de tubo medidos en RIBBON_RAIL: [6.1, 6.5, 7.0]
- **causa:** regla corregida en 03B.6
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** â€”
- **evidencia:** capÃ­tulo A5 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-029 Â· METRO â€” Acceso Centro Comercial queda fuera del ambito de intervencion

- **posiciÃ³n:** x=-79.3  y=66.7  z=0.00
- **magnitud:** elemento de proyecto mas proximo a nivel de boca: 45.74 m
- **causa:** situado fuera de la envolvente del proyecto
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capÃ­tulo A6 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-031 Â· METRO â€” Acceso Carretas queda fuera del ambito de intervencion

- **posiciÃ³n:** x=-3.3  y=-27.7  z=0.00
- **magnitud:** elemento de proyecto mas proximo a nivel de boca: 24.50 m
- **causa:** situado fuera de la envolvente del proyecto
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capÃ­tulo A6 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-032 Â· METRO â€” Acceso Mayor conserva la vertical libre

- **posiciÃ³n:** x=-84.2  y=-20.6  z=0.00
- **magnitud:** cielo abierto sobre la boca; estructura aerea mas proxima a 11.01 m (cota 7.55)
- **causa:** â€”
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capÃ­tulo A6 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-035 Â· DENSIDAD â€” Sector (-62,5): E02 anadio +4.5 pp de ocupacion

- **posiciÃ³n:** x=-61.9  y=5.1  z=0.00
- **magnitud:** MASTER 14.0 % â†’ E02 18.4 % Â· holgura mediana 2.7 m Â· cubierto 84 %
- **causa:** densificacion vegetal E02 (huerto de C1 / tropicales de C2 / arbolado)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** aclarar 1 de cada 3 filas de huerto, como ya anoto el propio REGISTRO_E02
- **evidencia:** capÃ­tulo A8 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-036 Â· DENSIDAD â€” Sector (-42,5): E02 anadio +3.6 pp de ocupacion

- **posiciÃ³n:** x=-41.9  y=5.1  z=0.00
- **magnitud:** MASTER 10.3 % â†’ E02 13.8 % Â· holgura mediana 3.5 m Â· cubierto 53 %
- **causa:** densificacion vegetal E02 (huerto de C1 / tropicales de C2 / arbolado)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** aclarar 1 de cada 3 filas de huerto, como ya anoto el propio REGISTRO_E02
- **evidencia:** capÃ­tulo A8 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-037 Â· DENSIDAD â€” La densificacion E02 no compromete la ocupacion global de suelo

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** ocupacion del ambito 7.8 % (MASTER 7.3 %): +0.5 pp Â· superficie libre 10339 m2 de 11214 m2
- **causa:** la vegetacion E02 se implanto sobre jardineras y bajo dosel, no sobre el suelo de paso
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion; el problema de densidad, donde existe, es local y de cobertura aerea, no de ocupacion global
- **evidencia:** capÃ­tulo A8 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-050 Â· PERSONA â€” Ningun punto pisable produce impacto de cabeza con el volumen humano de 1,70 m

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** galibo minimo absoluto sobre suelo pisable 2.17 m > 1,85 m de envolvente de cabeza; los 11 incumplimientos de galibo lo son respecto al criterio propio de 3,00 m, no por choque fisico
- **causa:** â€”
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** decidir si 3,00 m sigue siendo el criterio o si bajo dosel se admite un valor menor documentado
- **evidencia:** capÃ­tulo A11 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-051 Â· EDIFICIOS â€” Ningun solido del proyecto penetra volumetria construida (35 edificios, alturas reales)

- **posiciÃ³n:** sin posiciÃ³n puntual (afecta a un conjunto)
- **magnitud:** eje de cinta a 3.79 m de la manzana mas proxima (regla 2.65 m)
- **causa:** â€”
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** EDGE_GUARD v004 verificado de forma independiente por la auditoria
- **evidencia:** capÃ­tulo A12 Â· secciÃ³n automÃ¡tica y captura en `VIABILITY_AUDIT_MASTER.pdf`

---

## CÃ³mo se reproduce

```bash
python audit_run.py      # mide y escribe _data/
python audit_report.py   # arma los PDF, el CSV y este registro
```

El motor reconstruye la escena en memoria interceptando `add_mesh` / `place` / `add_curve` de `build_all_03b.py`: audita exactamente la geometrÃ­a que produce el modelo aprobado, sin abrir ni escribir ningÃºn `.3dm`.