# SELF_CRITIQUE_V006 — pasada adversarial (§29): atacar el trabajo, no defenderlo

## Encontrado y CORREGIDO en esta fase
1. **Nenúfares gigantes** (una pala cubría la balsa entera): el asset plano no puede
   normalizarse por altura → tope de diámetro en el conversor. Corregido y verificado.
2. **Línea de recirculación tendida en superficie muriendo en nada** (arrastrada desde S09):
   enterrada con tapas en los quiebros. Corregido.
3. **Olmos FLOTANDO ~1 m** (la decimación FAR se comió la base del tronco): re-base por LOD.
4. **Postes de barandilla apilados** en el pliegue cóncavo de la Estación (30 uds): dedupe;
   el offset plegado en curvas cóncavas queda VIGILADO (ver abierto #3).
5. **Goteros-esfera degenerados** en huerto → cilindros.
6. **Foso/umbral de ascensor coplanares** → separados.
7. **Plantas de tiesto invadiendo ejes** (los 2 RED reales de v005) → orientación al lado
   contrario + especie compacta junto a corredor.
8. **Cuatro rondas de auditoría "idénticas" que NO lo eran** (builds 5-8): el retarget de
   `_reaudit9` había fallado en silencio (raw string con backslash final = SyntaxError) y
   audité v005 cuatro veces creyendo auditar v006. Lección grabada: verificar retargets
   con grep y desconfiar de resultados byte-idénticos. Tras el arreglo, TODOS los focos
   se rastrearon hasta su triángulo culpable (probes 10-12) antes de tocar nada.
9. **Mi propio zócalo del ECI cortaba la calle Arenal en el raster peatonal** (banda
   mitered cerrada sobre footprint cóncavo + tapa a z 0.90 rasterizable). No lo tapé
   reclasificando: emisión por arista + guarda de corredor, y el porqué documentado.
10. **La marquesina del atrio penetraba la Estación 2.43 m** (la boca vive sobre la
   huella del edificio; "delante de la boca" era DENTRO). Volada a la aproximación.
11. **El canal del atrio moría dentro del polígono de la Estación** (0.63 m): el proxy
   ESTP del generador no es el polígono OSM del auditor; el canal se recorta ahora contra
   el criterio del AUDITOR.
12. **El huerto tenía un cajón en la ruta del tren** (V-037): guarda 4.5 m + 7 omisiones
   registradas; las cámaras de producto se reapuntaron al cajón superviviente (−56.5, 6.2).

## Lo que TODAVÍA me da vergüenza (abierto, honesto)
1. **El harness de captura (Edge headless) es INESTABLE en esta máquina**: con decenas de
   procesos msedge zombis, las tomas contaminan frames entre instancias o salen en blanco
   de forma no determinista (la MISMA cámara renderiza en una tirada y sale blanca en la
   siguiente). La iteración i3 (delta de builds 8-12) validó con contenido real:
   20_huerto ×4 distancias, 25/26_pod ×4, 27_metro (50cm) y 30_fachada (50cm/15cm);
   las series completas ×4 de los 30 puntos existen en i1/i2. Es un defecto del harness
   de captura, no del modelo (las auditorías geométricas son la verdad de referencia).
   `shoot()` quedó endurecido con perfil de Edge fresco por toma para futuras campañas.
2. **5 tropicales procedurales** clasificadas flotantes sobre jardineras elevadas (apoyo sin
   verificar visualmente); siguen SOSPECHOSO.
3. **El offset de barandilla puede plegarse** en cóncavas muy cerradas: los postes ya no se
   apilan, pero el tubo del rail dobla apretado ahí. Candidato: poda de puntos plegados.
4. **9 objetos** con costuras de abanico >umbral en huerto procedural (invisibles a 15 cm
   pero existen).
5. **La tomatera es maíz**: no existe tomatera CC0/CC-BY descargable digna; el maíz por fases
   cubre el rol visual. Documentado en provenance como proxy.
6. **HIEDRA descargada pero no colocada**: el manto de hiedra necesita orientación por
   superficie (muro/pérgola) que el sistema de instancias por punto no resuelve aún con
   dignidad. Antes de colocarla mal, queda en biblioteca. (La trepadora de mástil sigue
   siendo la hélice procedural, que sí funciona.)
7. **MACETA fotoescaneada (16k tris)** sin colocar por peso: reservada para accents de la
   campaña de render.
8. ~~**Clima**: re-ejecución pendiente~~ → CERRADO: `_reclima9/` re-ejecutó la simulación
   completa sobre v006 con k_veg POR ESPECIE en el vóxel (CLIMATE_V006_MASTER.pdf).
   Matices honestos que quedan: el LAI de cada especie es bibliográfico (ESTIMADO, no
   medido), la tomatera sigue representada por maíz también en el clima (misma k), y las
   copas usan cilindros del masterplan, no la silueta real del asset.
9. **4 duplicados de pletina y 9 costuras de abanico** siguen en el purge (pliegue cóncavo
   de la Estación y abanicos PRIMARY/SAT): visualmente invisibles, técnicamente ERROR,
   honestamente listados.
