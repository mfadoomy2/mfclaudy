# ISSUES_REGISTER — FASE 03B.5

Auditoría geométrica y de viabilidad del modelo aprobado (`MASTER_ARCHITECTURE_v002.3dm` / `SOL_FULL_SCENE_v001.3dm`, escena E02 con 6.672 mallas y 394.610 triángulos).
**2026-08-10 · NADA HA SIDO CORREGIDO · EL MASTER NO SE HA MODIFICADO.**

| severidad | nº | criterio de clasificación |
|---|---|---|
| 🔴 RED | 36 | impide el uso previsto, o incumple un criterio declarado por el propio proyecto |
| 🟡 YELLOW | 22 | funciona pero al límite, o depende de una decisión pendiente |
| 🟢 GREEN | 15 | anotación de coherencia documental, sin efecto sobre el uso |

> Los umbrales usados (1,80 / 3,00 m de anchura · 3,00 m de gálibo · 5,5 m de banda de Metro) son criterios de trabajo tomados del HEIGHT_SYSTEM y de la decisión D03B-02. **No se ha aplicado ninguna normativa**: la identificación de la norma aplicable es el paso siguiente.

## 🔴 RED (36)

### V-001 · RECORRIDOS — Estrechamiento en preciados-carretas (s=54 m)

- **posición:** x=-15.6  y=-1.1  z=0.00
- **magnitud:** holgura libre 0.00 m sobre el eje (ancho transversal disponible 0.0 m)
- **causa:** obstaculos laterales: WATER / WATER
- **severidad:** RED
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-002 · RECORRIDOS — Estrechamiento en montera-espozymina (s=62 m)

- **posición:** x=41.6  y=-5.0  z=0.00
- **magnitud:** holgura libre 0.00 m sobre el eje (ancho transversal disponible 0.0 m)
- **causa:** obstaculos laterales: RIBBON / RIBBON
- **severidad:** RED
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-003 · RECORRIDOS — Estrechamiento en carmen-correos (s=73 m)

- **posición:** x=-18.7  y=-0.3  z=0.00
- **magnitud:** holgura libre 0.50 m sobre el eje (ancho transversal disponible 17.8 m)
- **causa:** obstaculos laterales: FURNITURE / WATER
- **severidad:** RED
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-004 · RECORRIDOS — Estrechamiento en montera-espozymina (s=56 m)

- **posición:** x=43.0  y=0.3  z=0.00
- **magnitud:** holgura libre 1.00 m sobre el eje (ancho transversal disponible 2.0 m)
- **causa:** obstaculos laterales: PLANTER / PLANTER
- **severidad:** RED
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-009 · RECORRIDOS — Paso estrangulado a 0.50 m entre PLANTER

- **posición:** x=-53.6  y=-22.1  z=0.00
- **magnitud:** holgura libre 0.50 m (no admite el cruce de dos personas)
- **causa:** dos elementos de la familia PLANTER implantados sin comprobar el hueco entre ellos
- **severidad:** RED
- **estrategias posibles (no aplicadas):** separar las dos instancias · suprimir una · reconocerlo como paso de servicio
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-010 · RECORRIDOS — Paso estrangulado a 0.50 m entre PLANTER+VEGETATION

- **posición:** x=-56.9  y=-16.6  z=0.00
- **magnitud:** holgura libre 0.50 m (no admite el cruce de dos personas)
- **causa:** dos elementos de la familia PLANTER+VEGETATION implantados sin comprobar el hueco entre ellos
- **severidad:** RED
- **estrategias posibles (no aplicadas):** separar las dos instancias · suprimir una · reconocerlo como paso de servicio
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-011 · RECORRIDOS — Paso estrangulado a 0.50 m entre PLANTER

- **posición:** x=-49.6  y=-15.9  z=0.00
- **magnitud:** holgura libre 0.50 m (no admite el cruce de dos personas)
- **causa:** dos elementos de la familia PLANTER implantados sin comprobar el hueco entre ellos
- **severidad:** RED
- **estrategias posibles (no aplicadas):** separar las dos instancias · suprimir una · reconocerlo como paso de servicio
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-012 · RECORRIDOS — Paso estrangulado a 0.50 m entre PLANTER

- **posición:** x=-63.6  y=-15.6  z=0.00
- **magnitud:** holgura libre 0.50 m (no admite el cruce de dos personas)
- **causa:** dos elementos de la familia PLANTER implantados sin comprobar el hueco entre ellos
- **severidad:** RED
- **estrategias posibles (no aplicadas):** separar las dos instancias · suprimir una · reconocerlo como paso de servicio
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-013 · RECORRIDOS — Paso estrangulado a 0.50 m entre PLANTER

- **posición:** x=-42.6  y=-13.6  z=0.00
- **magnitud:** holgura libre 0.50 m (no admite el cruce de dos personas)
- **causa:** dos elementos de la familia PLANTER implantados sin comprobar el hueco entre ellos
- **severidad:** RED
- **estrategias posibles (no aplicadas):** separar las dos instancias · suprimir una · reconocerlo como paso de servicio
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-014 · RECORRIDOS — Paso estrangulado a 0.50 m entre PLANTER

- **posición:** x=-69.9  y=-12.9  z=0.00
- **magnitud:** holgura libre 0.50 m (no admite el cruce de dos personas)
- **causa:** dos elementos de la familia PLANTER implantados sin comprobar el hueco entre ellos
- **severidad:** RED
- **estrategias posibles (no aplicadas):** separar las dos instancias · suprimir una · reconocerlo como paso de servicio
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-015 · RECORRIDOS — Paso estrangulado a 0.50 m entre PODS

- **posición:** x=72.9  y=-12.6  z=0.00
- **magnitud:** holgura libre 0.50 m (no admite el cruce de dos personas)
- **causa:** dos elementos de la familia PODS implantados sin comprobar el hueco entre ellos
- **severidad:** RED
- **estrategias posibles (no aplicadas):** separar las dos instancias · suprimir una · reconocerlo como paso de servicio
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-016 · RECORRIDOS — Paso estrangulado a 0.50 m entre PODS

- **posición:** x=70.1  y=-12.4  z=0.00
- **magnitud:** holgura libre 0.50 m (no admite el cruce de dos personas)
- **causa:** dos elementos de la familia PODS implantados sin comprobar el hueco entre ellos
- **severidad:** RED
- **estrategias posibles (no aplicadas):** separar las dos instancias · suprimir una · reconocerlo como paso de servicio
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-017 · RECORRIDOS — Paso estrangulado a 0.50 m entre PODS

- **posición:** x=75.6  y=-12.1  z=0.00
- **magnitud:** holgura libre 0.50 m (no admite el cruce de dos personas)
- **causa:** dos elementos de la familia PODS implantados sin comprobar el hueco entre ellos
- **severidad:** RED
- **estrategias posibles (no aplicadas):** separar las dos instancias · suprimir una · reconocerlo como paso de servicio
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-018 · RECORRIDOS — Paso estrangulado a 0.50 m entre PLANTER+PODS

- **posición:** x=-77.4  y=-9.9  z=0.00
- **magnitud:** holgura libre 0.50 m (no admite el cruce de dos personas)
- **causa:** dos elementos de la familia PLANTER+PODS implantados sin comprobar el hueco entre ellos
- **severidad:** RED
- **estrategias posibles (no aplicadas):** separar las dos instancias · suprimir una · reconocerlo como paso de servicio
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-019 · RECORRIDOS — Eje de preciados-carretas ocupado por geometria en 1 estaciones

- **posición:** x=-15.6  y=-1.1  z=0.00
- **magnitud:** 1 de 188 estaciones (0 m de traza)
- **causa:** el eje declarado atraviesa WATER
- **severidad:** RED
- **estrategias posibles (no aplicadas):** redefinir la traza del corredor o retirar el elemento invasor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-020 · RECORRIDOS — Eje de montera-espozymina ocupado por geometria en 3 estaciones

- **posición:** x=41.6  y=-5.0  z=0.00
- **magnitud:** 3 de 179 estaciones (2 m de traza)
- **causa:** el eje declarado atraviesa RIBBON
- **severidad:** RED
- **estrategias posibles (no aplicadas):** redefinir la traza del corredor o retirar el elemento invasor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-024 · GALIBOS — Galibo 2.31 m bajo elemento firme: STEP

- **posición:** x=43.4  y=-5.9  z=2.31
- **magnitud:** 2.31 m (0.69 m por debajo del H_CLEAR_MIN 3.00) · 3.00 m2 en 12 manchas · peor punto en (43, -6)
- **causa:** cara inferior de STEP por debajo del estrato libre peatonal (bajo escalera de la cinta)
- **severidad:** RED
- **estrategias posibles (no aplicadas):** cerrar o ajardinar el hueco bajo la zanca · subir el arranque · senalizar el bajo escalera
- **evidencia:** capítulo A2 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-035 · CINTA — Escaleras de la cinta con contrahuella 0.385 m y pendiente 91 %

- **posición:** x=-84.0  y=-5.0  z=3.00
- **magnitud:** CH=0.385 m · H=0.424 m · 2CH+H=1.19 m · 91% (42°) · 16 peldanos para 5.78 m
- **causa:** el generador reparte el desnivel en 16 peldanos sobre una zanca de 6.36 m; no hay meseta ni barandilla
- **severidad:** RED
- **estrategias posibles (no aplicadas):** alargar la zanca a ~11 m con 32 peldanos (CH 0.18 / H 0.30) y meseta intermedia · anadir barandilla · o sustituir por rampa/ascensor
- **evidencia:** capítulo A4 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-036 · ACCESIBILIDAD — La cota +6.00 (cinta) carece de itinerario accesible

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** 6 escaleras, 0 rampas, 0 ascensores, 0 plataformas; desnivel 5.78 m
- **causa:** no se ha proyectado ningun medio de elevacion accesible al nivel elevado
- **severidad:** RED
- **estrategias posibles (no aplicadas):** ascensor en un extremo · rampa al 6 %% (96 m de desarrollo + mesetas) · o declarar la cinta como recorrido complementario no accesible
- **evidencia:** capítulo A4/A5 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-037 · CINTA — Las 6 escaleras no tienen barandilla modelada

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** 0 de 6 escaleras con pasamanos; caida libre lateral hasta 5.78 m
- **causa:** la familia STAIR solo genera 2 zancas + 16 peldanos
- **severidad:** RED
- **estrategias posibles (no aplicadas):** anadir pasamanos a doble altura (0.70/0.95) en ambos lados
- **evidencia:** capítulo A4 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-042 · ACCESIBILIDAD — Itinerario montera-espozymina no puede funcionar como accesible

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** ancho minimo 0.00 m · 94 % de la traza >= 1.80 m · 0 cambios de nivel
- **causa:** estrechamientos y/o desnivel sin medio accesible
- **severidad:** RED
- **estrategias posibles (no aplicadas):** liberar los puntos criticos o declarar un itinerario accesible alternativo
- **evidencia:** capítulo A5 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-043 · ACCESIBILIDAD — Itinerario CINTA +6.00 no puede funcionar como accesible

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** ancho minimo 2.31 m · 100 % de la traza >= 1.80 m · 1 cambios de nivel
- **causa:** estrechamientos y/o desnivel sin medio accesible
- **severidad:** RED
- **estrategias posibles (no aplicadas):** liberar los puntos criticos o declarar un itinerario accesible alternativo
- **evidencia:** capítulo A5 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-046 · METRO — Acceso Cercanías: 5 elementos a nivel de boca dentro de la banda 5,5 m

- **posición:** x=57.0  y=-5.4  z=0.00
- **magnitud:** obstaculo fisico mas proximo a 1.57 m (RIB_SUP) · ancho libre frontal minimo 5.75 m · familias RIBBON,VEGETATION,WATER
- **causa:** la banda de exclusion de D03B-02 se aplico a discos y mastiles, pero la vegetacion E02 y las piezas menores se implantaron despues con reglas propias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** auditar la banda contra el criterio real de Metro de Madrid · retirar los invasores a nivel de boca · mantener libre el frente de evacuacion
- **evidencia:** capítulo A6 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-058 · MANTENIMIENTO — CANOPY / BAJANTE: 37 de 67 componentes sin acceso de mantenimiento

- **posición:** x=-51.0  y=5.0  z=5.30
- **magnitud:** holgura pisable adyacente mediana 1.12 m (se requieren 2.50 m)
- **causa:** el elemento queda rodeado de jardinera/vegetacion/agua o sin superficie de apoyo para plataforma elevadora
- **severidad:** RED
- **estrategias posibles (no aplicadas):** reservar un area tecnica de 2.5x2.5 m junto a cada unidad · pasarela tecnica · acceso desde la cinta
- **evidencia:** capítulo A9 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-060 · MANTENIMIENTO — DEPOSITO DE SUELO: 6 de 6 componentes sin acceso de mantenimiento

- **posición:** x=-44.0  y=17.0  z=2.25
- **magnitud:** holgura pisable adyacente mediana 0.71 m (se requieren 0.90 m)
- **causa:** el elemento queda rodeado de jardinera/vegetacion/agua o sin superficie de apoyo para plataforma elevadora
- **severidad:** RED
- **estrategias posibles (no aplicadas):** reservar un area tecnica de 2.5x2.5 m junto a cada unidad · pasarela tecnica · acceso desde la cinta
- **evidencia:** capítulo A9 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-062 · MANTENIMIENTO — VIVERO: 3 de 3 componentes sin acceso de mantenimiento

- **posición:** x=64.0  y=18.0  z=3.00
- **magnitud:** holgura pisable adyacente mediana 0.71 m (se requieren 0.90 m)
- **causa:** el elemento queda rodeado de jardinera/vegetacion/agua o sin superficie de apoyo para plataforma elevadora
- **severidad:** RED
- **estrategias posibles (no aplicadas):** reservar un area tecnica de 2.5x2.5 m junto a cada unidad · pasarela tecnica · acceso desde la cinta
- **evidencia:** capítulo A9 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-063 · COLISIONES — Interpenetracion CANOPY×RIBBON: LEAF_OV × RIBBON_DECK

- **posición:** x=67.3  y=-0.7  z=5.89
- **magnitud:** 38 voxeles de 0.20 m (0.304 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-064 · COLISIONES — Interpenetracion FURNITURE×PLANTER: BENCH_0 × MAST_3

- **posición:** x=7.6  y=6.5  z=0.23
- **magnitud:** 37 voxeles de 0.20 m (0.296 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-065 · COLISIONES — Interpenetracion FURNITURE×PLANTER: BENCH_2 × MAST_2

- **posición:** x=-0.3  y=4.5  z=0.23
- **magnitud:** 28 voxeles de 0.20 m (0.224 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-066 · COLISIONES — Interpenetracion PODS×VEGETATION: POD_S × MAST_2

- **posición:** x=70.0  y=16.2  z=0.95
- **magnitud:** 27 voxeles de 0.20 m (0.216 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-067 · COLISIONES — Interpenetracion CANOPY×VEGETATION: LEAF_M2 × VEG2_ARBOL_A

- **posición:** x=22.7  y=29.7  z=4.27
- **magnitud:** 27 voxeles de 0.20 m (0.216 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-068 · COLISIONES — Interpenetracion CANOPY×RIBBON: LEAF_L1 × RIBBON_DECK

- **posición:** x=70.3  y=2.0  z=5.96
- **magnitud:** 27 voxeles de 0.20 m (0.216 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-069 · COLISIONES — Interpenetracion CANOPY×RIBBON: LEAF_LT × RIBBON_DECK

- **posición:** x=-5.8  y=15.4  z=5.89
- **magnitud:** 25 voxeles de 0.20 m (0.200 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-070 · COLISIONES — Interpenetracion CANOPY×RIBBON: LEAF_OV × RIBBON_DECK

- **posición:** x=67.3  y=-0.7  z=6.08
- **magnitud:** 22 voxeles de 0.20 m (0.176 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-071 · COLISIONES — Interpenetracion PODS×VEGETATION: POD_TRAIN × MAST_3

- **posición:** x=56.6  y=1.9  z=0.95
- **magnitud:** 21 voxeles de 0.20 m (0.168 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-072 · COLISIONES — Interpenetracion FURNITURE×PLANTER: BENCH_3 × MAST_3

- **posición:** x=-59.5  y=9.3  z=0.23
- **magnitud:** 21 voxeles de 0.20 m (0.168 m3 de solape)
- **causa:** implantacion por reglas independientes sin comprobacion cruzada entre familias
- **severidad:** RED
- **estrategias posibles (no aplicadas):** desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador
- **evidencia:** capítulo A10 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

## 🟡 YELLOW (22)

### V-005 · RECORRIDOS — Estrechamiento en eje-mayor-alcala (s=52 m)

- **posición:** x=-43.5  y=-11.3  z=0.00
- **magnitud:** holgura libre 1.80 m sobre el eje (ancho transversal disponible 20.2 m)
- **causa:** obstaculos laterales: VEGETATION / PLANTER
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-006 · RECORRIDOS — Estrechamiento en eje-mayor-alcala (s=26 m)

- **posición:** x=-69.3  y=-13.7  z=0.00
- **magnitud:** holgura libre 2.00 m sobre el eje (ancho transversal disponible 30.8 m)
- **causa:** obstaculos laterales: PLANTER / ABIERTO
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-007 · RECORRIDOS — Estrechamiento en eje-mayor-alcala (s=32 m)

- **posición:** x=-63.9  y=-12.9  z=0.00
- **magnitud:** holgura libre 2.06 m sobre el eje (ancho transversal disponible 30.8 m)
- **causa:** obstaculos laterales: ABIERTO / PLANTER
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-008 · RECORRIDOS — Estrechamiento en eje-mayor-alcala (s=60 m)

- **posición:** x=-36.5  y=-11.0  z=0.00
- **magnitud:** holgura libre 2.50 m sobre el eje (ancho transversal disponible 31.0 m)
- **causa:** obstaculos laterales: PLANTER / ABIERTO
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-023 · RECORRIDOS — Bolsa de suelo sin conexion pisable (44 m2)

- **posición:** x=6.9  y=-4.1  z=0.00
- **magnitud:** area aislada 44 m2 · cinturon: PLANTER,VEGETATION,WATER (0 % contexto)
- **causa:** cinturon continuo de jardineras/vegetacion/agua sin hueco de paso
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** abrir un vano de acceso o declararla explicitamente como area no accesible
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-025 · GALIBOS — Copas de arbolado E02 por debajo de 2,50 m sobre suelo pisable (29 puntos)

- **posición:** x=-83.9  y=2.9  z=2.21
- **magnitud:** 33.4 m2 de suelo pisable bajo copa a menos de 2,50 m · minimo 2.21 m · bloques implicados: VEG2_ARBOL_A, VEG2_TROPICAL · envolvente de cabeza de la persona de referencia 1,85 m
- **causa:** los bloques VEG2_ARBOL_A/B/EX generan la copa como esfera lobulada sin faldon libre de tronco: la copa arranca a 0.62·h y el lobulo inferior baja hasta 2,21 m
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** poda de formacion a 2,20–2,50 m (practica normal de arbolado urbano) · o elevar el centro de copa en el bloque VEG2_ARBOL. NO es incumplimiento de la regla 7 del HEIGHT_SYSTEM: una copa no es «elemento firme». Se registra para que la decision sea explicita.
- **evidencia:** capítulo A2 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-028 · ALTURAS — H_GROUND_TANK fuera de rango declarado

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** declarado 1.35 (rango [1.2, 1.5]) · construido 2.25
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-029 · ALTURAS — H_NURSERY_TOWER fuera de rango declarado

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** declarado 3.0 (rango [3.0, 3.0]) · construido 3.32
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-030 · ALTURAS — H_CLEAR_MIN fuera de rango declarado

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** declarado 3.0 (rango [2.8, 3.2]) · construido 2.31
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-032 · ALTURAS — H_TREE_EXIST fuera de rango declarado

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** declarado 7.0 (rango [5.0, 8.0]) · construido 8.51
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-034 · ALTURAS — FAMILIA_DOSEL fuera de rango declarado

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** declarado 5.0/6.75/8.5 (rango ['±0.30', '']) · construido 32 de 67 discos fuera
- **causa:** divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-038 · CINTA — Radio de curvatura minimo de la cinta 2.3 m

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** radio minimo 2.3 m (p01 4.7 m) para un tablero de 2.50 m de ancho
- **causa:** la traza se genero como polilinea de 371 puntos sin control de curvatura
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** suavizar la generatriz en 30_CURVES manteniendo los puntos de acometida de escalera
- **evidencia:** capítulo A4 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-040 · ACCESIBILIDAD — Itinerario preciados-carretas accesible salvo puntos criticos

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** ancho minimo 0.00 m (p05 4.00 m)
- **causa:** estrechamientos puntuales
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** liberar los estrechamientos listados en A1
- **evidencia:** capítulo A5 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-041 · ACCESIBILIDAD — Itinerario carmen-correos accesible salvo puntos criticos

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** ancho minimo 0.50 m (p05 3.69 m)
- **causa:** estrechamientos puntuales
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** liberar los estrechamientos listados en A1
- **evidencia:** capítulo A5 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-044 · ACCESIBILIDAD — Barandilla de cinta sin travesano intermedio ni rodapie

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** montantes c/~1.0 m + pasamanos 1.05; hueco libre 0–1.05 m
- **causa:** la familia RIBBON_RAIL solo genera pasamanos y montantes
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** anadir travesano intermedio y rodapie 0.10 m
- **evidencia:** capítulo A5 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-048 · METRO — Acceso Carmen: 6 elementos a nivel de boca dentro de la banda 5,5 m

- **posición:** x=18.5  y=25.1  z=0.00
- **magnitud:** obstaculo fisico mas proximo a 2.95 m (RIB_SUP) · ancho libre frontal minimo 3.25 m · familias PLANTER,RIBBON,VEGETATION,WATER
- **causa:** la banda de exclusion de D03B-02 se aplico a discos y mastiles, pero la vegetacion E02 y las piezas menores se implantaron despues con reglas propias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** auditar la banda contra el criterio real de Metro de Madrid · retirar los invasores a nivel de boca · mantener libre el frente de evacuacion
- **evidencia:** capítulo A6 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-050 · METRO — Acceso Alcalá: 4 elementos a nivel de boca dentro de la banda 5,5 m

- **posición:** x=46.9  y=18.9  z=0.00
- **magnitud:** obstaculo fisico mas proximo a 4.21 m (NEB_POST) · ancho libre frontal minimo 6.75 m · familias PODS,RIBBON,WATER
- **causa:** la banda de exclusion de D03B-02 se aplico a discos y mastiles, pero la vegetacion E02 y las piezas menores se implantaron despues con reglas propias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** auditar la banda contra el criterio real de Metro de Madrid · retirar los invasores a nivel de boca · mantener libre el frente de evacuacion
- **evidencia:** capítulo A6 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-051 · METRO — Acceso Alcalá: 2 elementos a nivel de boca dentro de la banda 5,5 m

- **posición:** x=40.2  y=12.0  z=0.00
- **magnitud:** obstaculo fisico mas proximo a 3.02 m (NEB_POST) · ancho libre frontal minimo 6.50 m · familias RIBBON,WATER
- **causa:** la banda de exclusion de D03B-02 se aplico a discos y mastiles, pero la vegetacion E02 y las piezas menores se implantaron despues con reglas propias
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** auditar la banda contra el criterio real de Metro de Madrid · retirar los invasores a nivel de boca · mantener libre el frente de evacuacion
- **evidencia:** capítulo A6 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-052 · VISUALES — RELOJ visible solo desde el 39 % de la plaza

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** 38.6 % de 2474 puntos de observacion a 1.65 m
- **causa:** dosel continuo 5.0–8.5 + copas E02 sobre la banda sur y el eje Mayor–Alcala
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** abrir un cono visual desde el eje Mayor–Alcala retirando 3–6 discos · elevar la capa baja en la banda de Correos
- **evidencia:** capítulo A7 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-057 · MANTENIMIENTO — BAJANTE/RISER: 1 de 6 componentes sin acceso de mantenimiento

- **posición:** x=-72.0  y=17.0  z=10.50
- **magnitud:** holgura pisable adyacente mediana 0.50 m (se requieren 0.90 m)
- **causa:** el elemento queda rodeado de jardinera/vegetacion/agua o sin superficie de apoyo para plataforma elevadora
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reservar un area tecnica de 2.5x2.5 m junto a cada unidad · pasarela tecnica · acceso desde la cinta
- **evidencia:** capítulo A9 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-059 · MANTENIMIENTO — DEPOSITO +10.5: 1 de 6 componentes sin acceso de mantenimiento

- **posición:** x=-72.0  y=17.0  z=10.50
- **magnitud:** holgura pisable adyacente mediana 0.50 m (se requieren 2.50 m)
- **causa:** el elemento queda rodeado de jardinera/vegetacion/agua o sin superficie de apoyo para plataforma elevadora
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reservar un area tecnica de 2.5x2.5 m junto a cada unidad · pasarela tecnica · acceso desde la cinta
- **evidencia:** capítulo A9 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-061 · MANTENIMIENTO — NEBULIZADOR +4.0: 8 de 42 componentes sin acceso de mantenimiento

- **posición:** x=-61.5  y=18.7  z=4.00
- **magnitud:** holgura pisable adyacente mediana 1.06 m (se requieren 2.50 m)
- **causa:** el elemento queda rodeado de jardinera/vegetacion/agua o sin superficie de apoyo para plataforma elevadora
- **severidad:** YELLOW
- **estrategias posibles (no aplicadas):** reservar un area tecnica de 2.5x2.5 m junto a cada unidad · pasarela tecnica · acceso desde la cinta
- **evidencia:** capítulo A9 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

## 🟢 GREEN (15)

### V-021 · RECORRIDOS — La red peatonal principal se mantiene continua a 3,00 m de holgura

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** con exigencia de 3,00 m continuos sigue conectado el 73 % del suelo libre en 2 componentes (el mayor de 7130 m2); a 1,80 m, el 84 %
- **causa:** —
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capítulo A1 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-022 · ACCESIBILIDAD — El plano de plaza es horizontal en todo el ambito

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** cota 0.00 en toda la superficie construida: 0 %% de pendiente longitudinal y transversal a nivel de suelo
- **causa:** el modelo 03B resuelve la plaza como plano unico
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** verificar en fases posteriores la pendiente real de evacuacion de agua superficial (0 %% no drena)
- **evidencia:** capítulo A5 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-026 · GALIBOS — Ningun cable tensado invade el estrato peatonal

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** 159 cables comprobados · cota minima absoluta 3.00 m (anclaje de mastil en H_BRANCH_START 3.00)
- **causa:** —
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capítulo A2 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-027 · ALTURAS — H_BENCH_BACK declarado pero no construido

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** NO construido: respaldo
- **causa:** decision de proyecto (D9 / simplificacion 03B)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** retirar del HEIGHT_SYSTEM o marcarlo como reserva
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-031 · ALTURAS — H_TANK_TOWER declarado pero no construido

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** NO construido: torre de depositos apilados
- **causa:** decision de proyecto (D9 / simplificacion 03B)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** retirar del HEIGHT_SYSTEM o marcarlo como reserva
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-033 · ALTURAS — H_LOGISTIC_RAIL declarado pero no construido

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** NO construido: carril logistico (G4 apagada, D9)
- **causa:** decision de proyecto (D9 / simplificacion 03B)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** retirar del HEIGHT_SYSTEM o marcarlo como reserva
- **evidencia:** capítulo A3 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-039 · CINTA — La rasante de la cinta es plana y continua

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** 519 m a cota +6.00 constante: pendiente longitudinal 0.0 % y transversal 0.0 %; galibo bajo tablero 5.78 m
- **causa:** —
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** revisar no obstante la pendiente transversal: 0.0 %% implica que el tablero no evacua agua
- **evidencia:** capítulo A4 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-045 · METRO — Acceso Centro Comercial queda fuera del ambito de intervencion

- **posición:** x=-79.3  y=66.7  z=0.00
- **magnitud:** elemento de proyecto mas proximo a nivel de boca: 40.30 m
- **causa:** situado fuera de la envolvente del proyecto
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capítulo A6 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-047 · METRO — Acceso Carretas queda fuera del ambito de intervencion

- **posición:** x=-3.3  y=-27.7  z=0.00
- **magnitud:** elemento de proyecto mas proximo a nivel de boca: 16.71 m
- **causa:** situado fuera de la envolvente del proyecto
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capítulo A6 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-049 · METRO — Acceso Mayor queda fuera del ambito de intervencion

- **posición:** x=-84.2  y=-20.6  z=0.00
- **magnitud:** elemento de proyecto mas proximo a nivel de boca: 12.80 m
- **causa:** situado fuera de la envolvente del proyecto
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion
- **evidencia:** capítulo A6 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-053 · DENSIDAD — Sector (18,5): E02 anadio +4.9 pp de ocupacion

- **posición:** x=18.1  y=5.1  z=0.00
- **magnitud:** MASTER 11.4 % → E02 16.3 % · holgura mediana 1.8 m · cubierto 74 %
- **causa:** densificacion vegetal E02 (huerto de C1 / tropicales de C2 / arbolado)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** aclarar 1 de cada 3 filas de huerto, como ya anoto el propio REGISTRO_E02
- **evidencia:** capítulo A8 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-054 · DENSIDAD — Sector (-62,5): E02 anadio +4.6 pp de ocupacion

- **posición:** x=-61.9  y=5.1  z=0.00
- **magnitud:** MASTER 6.9 % → E02 11.5 % · holgura mediana 3.4 m · cubierto 75 %
- **causa:** densificacion vegetal E02 (huerto de C1 / tropicales de C2 / arbolado)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** aclarar 1 de cada 3 filas de huerto, como ya anoto el propio REGISTRO_E02
- **evidencia:** capítulo A8 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-055 · DENSIDAD — Sector (-42,5): E02 anadio +4.0 pp de ocupacion

- **posición:** x=-41.9  y=5.1  z=0.00
- **magnitud:** MASTER 11.7 % → E02 15.7 % · holgura mediana 2.5 m · cubierto 49 %
- **causa:** densificacion vegetal E02 (huerto de C1 / tropicales de C2 / arbolado)
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** aclarar 1 de cada 3 filas de huerto, como ya anoto el propio REGISTRO_E02
- **evidencia:** capítulo A8 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-056 · DENSIDAD — La densificacion E02 no compromete la ocupacion global de suelo

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** ocupacion del ambito 10.1 % (MASTER 9.0 %): +1.1 pp · superficie libre 9901 m2 de 11014 m2
- **causa:** la vegetacion E02 se implanto sobre jardineras y bajo dosel, no sobre el suelo de paso
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** sin accion; el problema de densidad, donde existe, es local y de cobertura aerea, no de ocupacion global
- **evidencia:** capítulo A8 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

### V-073 · PERSONA — Ningun punto pisable produce impacto de cabeza con el volumen humano de 1,70 m

- **posición:** sin posición puntual (afecta a un conjunto)
- **magnitud:** galibo minimo absoluto sobre suelo pisable 2.21 m > 1,85 m de envolvente de cabeza; los 50 incumplimientos de galibo lo son respecto al criterio propio de 3,00 m, no por choque fisico
- **causa:** —
- **severidad:** GREEN
- **estrategias posibles (no aplicadas):** decidir si 3,00 m sigue siendo el criterio o si bajo dosel se admite un valor menor documentado
- **evidencia:** capítulo A11 · sección automática y captura en `VIABILITY_AUDIT_MASTER.pdf`

---

## Cómo se reproduce

```bash
python audit_run.py      # mide y escribe _data/
python audit_report.py   # arma los PDF, el CSV y este registro
```

El motor reconstruye la escena en memoria interceptando `add_mesh` / `place` / `add_curve` de `build_all_03b.py`: audita exactamente la geometría que produce el modelo aprobado, sin abrir ni escribir ningún `.3dm`.