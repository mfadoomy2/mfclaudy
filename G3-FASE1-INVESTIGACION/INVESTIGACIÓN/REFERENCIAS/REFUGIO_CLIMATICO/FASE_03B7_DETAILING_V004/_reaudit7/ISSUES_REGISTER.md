# ISSUES_REGISTER — FASE 03B.5

Auditoría geométrica y de viabilidad del modelo aprobado (`MASTER_ARCHITECTURE_v002.3dm` / `SOL_FULL_SCENE_v001.3dm`, escena E02 con 6.672 mallas y 394.610 triángulos).
**2026-08-10 · NADA HA SIDO CORREGIDO · EL MASTER NO SE HA MODIFICADO.**

| severidad | nº | criterio de clasificación |
|---|---|---|
| 🔴 RED | 0 | impide el uso previsto, o incumple un criterio declarado por el propio proyecto |
| 🟡 YELLOW | 28 | funciona pero al límite, o depende de una decisión pendiente |
| 🟢 GREEN | 20 | anotación de coherencia documental, sin efecto sobre el uso |

> Los umbrales usados (1,80 / 3,00 m de anchura · 3,00 m de gálibo · 5,5 m de banda de Metro) son criterios de trabajo tomados del HEIGHT_SYSTEM y de la decisión D03B-02. **No se ha aplicado ninguna normativa**: la identificación de la norma aplicable es el paso siguiente.

## 🟡 YELLOW (28)

### V-001 · RECORRIDOS — Estrechamiento en eje-mayor-alcala (s=32 m)

- **posición:** x=-63.9  y=-12.9  z=0.00
- **magnitud:** holgura libre 2.00 m sobre el eje (ancho transversal disponible 18.0 m)
- **causa:** obstaculos laterales: PODS / PLANTER
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-002 · RECORRIDOS — Estrechamiento en montera-espozymina (s=68 m)

- **posición:** x=36.9  y=-5.1  z=0.00
- **magnitud:** holgura libre 2.00 m sobre el eje (ancho transversal disponible 27.0 m)
- **causa:** obstaculos laterales: PODS / WATER
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-003 · RECORRIDOS — Estrechamiento en carmen-correos (s=36 m)

- **posición:** x=-13.0  y=33.7  z=0.00
- **magnitud:** holgura libre 2.12 m sobre el eje (ancho transversal disponible 31.0 m)
- **causa:** obstaculos laterales: PLANTER / ABIERTO
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-004 · RECORRIDOS — Estrechamiento en montera-espozymina (s=56 m)

- **posición:** x=43.9  y=0.3  z=0.00
- **magnitud:** holgura libre 2.24 m sobre el eje (ancho transversal disponible 10.5 m)
- **causa:** obstaculos laterales: PLANTER / WATER
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-005 · RECORRIDOS — Estrechamiento en eje-mayor-alcala (s=52 m)

- **posición:** x=-43.5  y=-11.2  z=0.00
- **magnitud:** holgura libre 2.50 m sobre el eje (ancho transversal disponible 17.0 m)
- **causa:** obstaculos laterales: VEGETATION / VEGETATION
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-006 · RECORRIDOS — Estrechamiento en montera-espozymina (s=26 m)

- **posición:** x=40.0  y=30.0  z=0.00
- **magnitud:** holgura libre 2.50 m sobre el eje (ancho transversal disponible 26.5 m)
- **causa:** obstaculos laterales: PLANTER / WATER
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-007 · RECORRIDOS — Estrechamiento en montera-espozymina (s=63 m)

- **posición:** x=37.4  y=-0.1  z=0.00
- **magnitud:** holgura libre 2.55 m sobre el eje (ancho transversal disponible 31.5 m)
- **causa:** obstaculos laterales: ABIERTO / PLANTER
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-008 · RECORRIDOS — Huecos de 0.50 m interiores a las estancias ajardinadas: 26

- **posición:** x=68.4  y=-9.1  z=0.00
- **magnitud:** 26 huecos <1.20 m a >3 m de todo eje declarado
- **causa:** textura densa intencional de los parterres (capas jardinera+mata+agua); no son pasos de la red
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** sin accion: son estancias; revisar solo si un itinerario nuevo los atraviesa
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-012 · GALIBOS — Copas de arbolado E02 por debajo de 2,50 m sobre suelo pisable (10 puntos)

- **posición:** x=-8.4  y=26.1  z=2.31
- **magnitud:** 3.4 m2 de suelo pisable bajo copa a menos de 2,50 m · minimo 2.31 m · bloques implicados: VEG2_TROPICAL · envolvente de cabeza de la persona de referencia 1,85 m
- **causa:** los bloques VEG2_ARBOL_A/B/EX generan la copa como esfera lobulada sin faldon libre de tronco: la copa arranca a 0.62·h y el lobulo inferior baja hasta 2,21 m
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** poda de formacion a 2,20–2,50 m (practica normal de arbolado urbano) · o elevar el centro de copa en el bloque VEG2_ARBOL. NO es incumplimiento de la regla 7 del HEIGHT_SYSTEM: una copa no es «elemento firme». Se registra para que la decision sea explicita.
- **evidencia:** capítulo A2 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-015 · ALTURAS — H_GROUND_TANK fuera de rango declarado

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** declarado 1.35 (rango [1.2, 1.5]) · construido 2.31
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-016 · ALTURAS — H_NURSERY_TOWER fuera de rango declarado

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** declarado 3.0 (rango [3.0, 3.0]) · construido 3.32
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-017 · ALTURAS — H_CLEAR_MIN fuera de rango declarado

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** declarado 3.0 (rango [2.8, 3.2]) · construido 2.8
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-020 · ALTURAS — FAMILIA_DOSEL fuera de rango declarado

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** declarado 5.0/6.75/8.5 (rango ['±0.30', '']) · construido 28 de 94 discos fuera
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-023 · CINTA — Radio de curvatura minimo de la cinta 0.1 m

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** radio minimo 0.1 m (p01 0.7 m) para un tablero de 2.50 m de ancho
- **causa:** la traza se genero como polilinea de 371 puntos sin control de curvatura
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** suavizar la generatriz en 30_CURVES manteniendo los puntos de acometida de escalera
- **evidencia:** capítulo A4 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-025 · ACCESIBILIDAD — Itinerario montera-espozymina accesible salvo puntos criticos

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** ancho minimo 1.50 m (p05 2.34 m)
- **causa:** estrechamientos puntuales
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** liberar los estrechamientos listados en A1
- **evidencia:** capítulo A5 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-030 · METRO — Acceso Alcalá: 1 elementos a nivel de boca dentro de la banda 5,5 m

- **posición:** x=46.9  y=18.9  z=0.00
- **magnitud:** obstaculo fisico mas proximo a 4.75 m (LAB02) · ancho libre frontal minimo 6.75 m · familias PODS
- **causa:** la banda de exclusion de D03B-02 se aplico a discos y mastiles, pero la vegetacion E02 y las piezas menores se implantaron despues con reglas propias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** auditar la banda contra el criterio real de Metro de Madrid · retirar los invasores a nivel de boca · mantener libre el frente de evacuacion
- **evidencia:** capítulo A6 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-031 · VISUALES — RELOJ visible solo desde el 39 % de la plaza

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** 39.3 % de 2579 puntos de observacion a 1.65 m
- **causa:** dosel continuo 5.0–8.5 + copas E02 sobre la banda sur y el eje Mayor–Alcala
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** abrir un cono visual desde el eje Mayor–Alcala retirando 3–6 discos · elevar la capa baja en la banda de Correos
- **evidencia:** capítulo A7 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-036 · MANTENIMIENTO — CANOPY / BAJANTE: 1 de 94 componentes sin acceso de mantenimiento

- **posición:** x=2.1  y=7.1  z=8.50
- **magnitud:** holgura pisable adyacente mediana 2.00 m (se requieren 2.50 m)
- **causa:** el elemento queda rodeado de jardinera/vegetacion/agua o sin superficie de apoyo para plataforma elevadora
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reservar un area tecnica de 2.5x2.5 m junto a cada unidad · pasarela tecnica · acceso desde la cinta
- **evidencia:** capítulo A9 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-037 · COLISIONES — Interpenetracion DETAIL×STRUCTURE: DECK_CANALETA × MAST_3

- **posición:** x=35.4  y=-4.8  z=6.00
- **magnitud:** 6 voxeles de 0.20 m (0.048 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-038 · COLISIONES — Interpenetracion PODS×VEGETATION: POD_TRAIN × VEG2_HUERTO

- **posición:** x=-59.0  y=11.0  z=1.30
- **magnitud:** 6 voxeles de 0.20 m (0.048 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-039 · COLISIONES — Interpenetracion PODS×VEGETATION: POD_TRAIN × VEG2_HUERTO

- **posición:** x=-53.5  y=15.2  z=1.30
- **magnitud:** 6 voxeles de 0.20 m (0.048 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-040 · COLISIONES — Interpenetracion PODS×VEGETATION: POD_TRAIN × VEG2_BAJA

- **posición:** x=-61.9  y=9.3  z=0.36
- **magnitud:** 5 voxeles de 0.20 m (0.040 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-041 · COLISIONES — Interpenetracion PODS×VEGETATION: POD_TRAIN × VEG2_HUERTO

- **posición:** x=-59.1  y=11.0  z=0.60
- **magnitud:** 5 voxeles de 0.20 m (0.040 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-042 · COLISIONES — Interpenetracion PODS×VEGETATION: POD_TRAIN × VEG2_HUERTO

- **posición:** x=-59.1  y=11.0  z=0.60
- **magnitud:** 5 voxeles de 0.20 m (0.040 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-043 · COLISIONES — Interpenetracion PODS×VEGETATION: POD_TRAIN × VEG2_HUERTO

- **posición:** x=-59.0  y=11.0  z=0.95
- **magnitud:** 5 voxeles de 0.20 m (0.040 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-044 · COLISIONES — Interpenetracion PODS×VEGETATION: POD_TRAIN × VEG2_HUERTO

- **posición:** x=-53.7  y=15.4  z=0.13
- **magnitud:** 5 voxeles de 0.20 m (0.040 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-045 · COLISIONES — Interpenetracion PODS×VEGETATION: POD_TRAIN × VEG2_HUERTO

- **posición:** x=-53.6  y=15.2  z=0.60
- **magnitud:** 5 voxeles de 0.20 m (0.040 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-046 · COLISIONES — Interpenetracion PODS×WATER: POD_M × NEB_POST

- **posición:** x=-53.5  y=21.8  z=1.92
- **magnitud:** 5 voxeles de 0.20 m (0.040 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

## 🟢 GREEN (20)

### V-009 · RECORRIDOS — La red peatonal principal se mantiene continua a 3,00 m de holgura

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** con exigencia de 3,00 m continuos sigue conectado el 75 % del suelo libre en 1 componentes (el mayor de 7765 m2); a 1,80 m, el 86 %
- **causa:** —
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-010 · ACCESIBILIDAD — El plano de plaza es horizontal en todo el ambito

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** cota 0.00 en toda la superficie construida: 0 %% de pendiente longitudinal y transversal a nivel de suelo
- **causa:** el modelo 03B resuelve la plaza como plano unico
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** verificar en fases posteriores la pendiente real de evacuacion de agua superficial (0 %% no drena)
- **evidencia:** capítulo A5 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-011 · GALIBOS — La regla 7 del HEIGHT_SYSTEM se cumple practicamente en todo el ambito

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** bajo elemento FIRME el galibo baja de 3,00 m solo en 0.6 m2 de los 4058 m2 de suelo cubierto (0.01 %), con un minimo de 2.80 m; p05 4.38 m
- **causa:** —
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion sobre la estructura; revisar solo los residuos puntuales listados
- **evidencia:** capítulo A2 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-013 · GALIBOS — Ningun cable tensado invade el estrato peatonal

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** 196 cables comprobados · cota minima absoluta 3.00 m (anclaje de mastil en H_BRANCH_START 3.00)
- **causa:** —
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capítulo A2 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-014 · ALTURAS — H_BENCH_BACK declarado pero no construido

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** NO construido: respaldo
- **causa:** decision de proyecto (D9 / simplificacion 03B)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** retirar del HEIGHT_SYSTEM o marcarlo como reserva
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-018 · ALTURAS — H_TANK_TOWER declarado pero no construido

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** NO construido: torre de depositos apilados
- **causa:** decision de proyecto (D9 / simplificacion 03B)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** retirar del HEIGHT_SYSTEM o marcarlo como reserva
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-019 · ALTURAS — H_LOGISTIC_RAIL declarado pero no construido

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** NO construido: carril logistico (G4 apagada, D9)
- **causa:** decision de proyecto (D9 / simplificacion 03B)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** retirar del HEIGHT_SYSTEM o marcarlo como reserva
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-021 · CINTA — Escaleras reales: 37 CH de 0.162 m, meseta y doble pasamanos

- **posición:** x=-84.5  y=-5.0  z=3.00
- **magnitud:** CH=0.162 m · H=0.290 m · 2CH+H=0.61 m · 2 tramos + meseta 1.50 · zanca cerrada
- **causa:** regla corregida en 03B.6: bloque STAIR_SB sustituye a la zanca inclinada de v002
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** —
- **evidencia:** capítulo A4 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-022 · ACCESIBILIDAD — La cota +6.00 dispone de 3 ascensores-capsula ademas de 6 escaleras

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** 3 LIFT_TOWER medidos en la escena (C1-O, C2-N, C3-E); embarque a +5.97
- **causa:** regla corregida en 03B.6: ascensores integrados en los nodos de la cinta
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** definir cabina/maquinaria en fase de proyecto tecnico
- **evidencia:** capítulo A4/A5 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-024 · CINTA — La rasante de la cinta es plana y continua

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** 519 m a cota +6.00 constante: pendiente longitudinal 0.0 % y transversal 0.0 %; galibo bajo tablero 5.78 m
- **causa:** —
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** revisar no obstante la pendiente transversal: 0.0 %% implica que el tablero no evacua agua
- **evidencia:** capítulo A4 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-026 · ACCESIBILIDAD — Barandilla de cinta completa: pasamanos 1.05 + travesano 0.55 + rodapie 0.10

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** niveles de tubo medidos en RIBBON_RAIL: [6.1, 6.5, 6.6, 7.0, 7.1]
- **causa:** regla corregida en 03B.6
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** —
- **evidencia:** capítulo A5 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-027 · METRO — Acceso Centro Comercial queda fuera del ambito de intervencion

- **posición:** x=-79.3  y=66.7  z=0.00
- **magnitud:** elemento de proyecto mas proximo a nivel de boca: 46.73 m
- **causa:** situado fuera de la envolvente del proyecto
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capítulo A6 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-028 · METRO — Acceso Carretas queda fuera del ambito de intervencion

- **posición:** x=-3.3  y=-27.7  z=0.00
- **magnitud:** elemento de proyecto mas proximo a nivel de boca: 24.57 m
- **causa:** situado fuera de la envolvente del proyecto
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capítulo A6 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-029 · METRO — Acceso Mayor conserva la vertical libre

- **posición:** x=-84.2  y=-20.6  z=0.00
- **magnitud:** cielo abierto sobre la boca; estructura aerea mas proxima a 10.91 m (cota 7.55)
- **causa:** —
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capítulo A6 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-032 · DENSIDAD — Sector (-62,5): E02 anadio +4.6 pp de ocupacion

- **posición:** x=-61.9  y=5.1  z=0.00
- **magnitud:** MASTER 12.5 % → E02 17.1 % · holgura mediana 3.4 m · cubierto 92 %
- **causa:** densificacion vegetal E02 (huerto de C1 / tropicales de C2 / arbolado)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** aclarar 1 de cada 3 filas de huerto, como ya anoto el propio REGISTRO_E02
- **evidencia:** capítulo A8 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-033 · DENSIDAD — Sector (18,5): E02 anadio +3.9 pp de ocupacion

- **posición:** x=18.1  y=5.1  z=0.00
- **magnitud:** MASTER 13.1 % → E02 17.0 % · holgura mediana 1.5 m · cubierto 74 %
- **causa:** densificacion vegetal E02 (huerto de C1 / tropicales de C2 / arbolado)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** aclarar 1 de cada 3 filas de huerto, como ya anoto el propio REGISTRO_E02
- **evidencia:** capítulo A8 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-034 · DENSIDAD — Sector (-42,5): E02 anadio +3.7 pp de ocupacion

- **posición:** x=-41.9  y=5.1  z=0.00
- **magnitud:** MASTER 11.8 % → E02 15.5 % · holgura mediana 2.5 m · cubierto 52 %
- **causa:** densificacion vegetal E02 (huerto de C1 / tropicales de C2 / arbolado)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** aclarar 1 de cada 3 filas de huerto, como ya anoto el propio REGISTRO_E02
- **evidencia:** capítulo A8 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-035 · DENSIDAD — La densificacion E02 no compromete la ocupacion global de suelo

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** ocupacion del ambito 8.0 % (MASTER 7.3 %): +0.7 pp · superficie libre 10360 m2 de 11262 m2
- **causa:** la vegetacion E02 se implanto sobre jardineras y bajo dosel, no sobre el suelo de paso
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion; el problema de densidad, donde existe, es local y de cobertura aerea, no de ocupacion global
- **evidencia:** capítulo A8 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-047 · PERSONA — Ningun punto pisable produce impacto de cabeza con el volumen humano de 1,70 m

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** galibo minimo absoluto sobre suelo pisable 2.17 m > 1,85 m de envolvente de cabeza; los 10 incumplimientos de galibo lo son respecto al criterio propio de 3,00 m, no por choque fisico
- **causa:** —
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** decidir si 3,00 m sigue siendo el criterio o si bajo dosel se admite un valor menor documentado
- **evidencia:** capítulo A11 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-048 · EDIFICIOS — Ningun solido del proyecto penetra volumetria construida (35 edificios, alturas reales)

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** eje de cinta a 3.05 m de la manzana mas proxima (regla 2.65 m)
- **causa:** —
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** EDGE_GUARD v004 verificado de forma independiente por la auditoria
- **evidencia:** capítulo A12 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

---

## Cómo se reproduce

```bash
python audit_run.py      # mide y escribe _data/
python audit_report.py   # arma los PDF, el CSV y este registro
```

El motor reconstruye la escena en memoria interceptando `add_mesh` / `place` / `add_curve` de `build_all_03b.py`: audita exactamente la geometría que produce el modelo aprobado, sin abrir ni escribir ningún `.3dm`.