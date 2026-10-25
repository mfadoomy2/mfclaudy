# AUDIT_RESOLUTION_PLAN — FASE 03B.6
## 73 incidencias geométricas + 6 climáticas → 9 causas raíz · 2026-08-11
Regla: CORREGIR LA REGLA, NO LAS INSTANCIAS. Identidad del proyecto intocable. v002 y archivos
auditados se conservan; todo cambio va a `geometria_maestra_v003.json` (datos) + `build_all_03b6.py`
(reglas), copia del generador aprobado. Validado contra el libro de proceso (P08: verificar efectos
en disco, no fiarse de prints; P13: la regla raíz es la falta de guarda cruzada).

---

## CR-1 · AUSENCIA DE GUARDA CRUZADA ENTRE FAMILIAS  *(la causa madre)*
- **Incidencias**: V-063..V-072 (10 colisiones RED, 220 accidentales en 12 pares), V-019/V-020
  (ejes atravesados), V-023 (bolsa aislada 44 m²), V-025 (copas <2,5), parte de V-046/048/050/051
  (piezas E02 y menores dentro de banda de metro), casos de mantenimiento por invasión mutua. ≈ 30 incidencias.
- **Origen**: cada familia se implanta con su propia regla; `near_corr` protege corredores y
  `near_metro_pt` los claros, pero nada protege a las familias entre sí; varios chequeos se hacían
  en un punto distinto del de colocación final (tropicales: chequeo en el disco, colocación a +0,8,−0,5;
  VEG2_BAJA: offset fijo (+0,9,+0,4) que aterriza dentro del banco; vivero sobre el racimo de pods).
- **Corrección (regla)**: módulo `conflict_guard` central con registro incremental de obstáculos:
  toda colocación de suelo se chequea EN SU POSICIÓN FINAL con su radio real contra corredores,
  bocas de metro (base <+2,50, r=5,5), cinta+escaleras+ascensores, estatua (r=8), conos visuales,
  mástiles/cubas, bancos, jardineras, estanques, pods, huerto y tuberías; reubicación por búsqueda
  espiral determinista o supresión con log. Excepciones intencionadas (mástil–disco, jardinera–vegetación)
  en lista blanca explícita.
- **Riesgo arquitectónico**: nulo — reubicaciones ≤2 m de piezas menores.

## CR-2 · BARRERAS LINEALES SIN PUERTAS (trenes y orlas)
- **Incidencias**: V-009..V-018 (pasos 0,50 m: clúster SO de jardineras (−77..−42, −22..−5) y clúster
  de pods E (70..76,−12)), V-005..V-008 (estrechamientos del eje 1,8-2,5 m), V-023. 89 pasos <1,20 m. ≈ 16.
- **Origen**: los trenes T-O/T-SE se ensartan con huecos ~0,5 m (verja infranqueable) y las orlas de
  jardinera forman frentes continuos; el generador nunca comprobó el HUECO entre piezas adyacentes.
- **Corrección (regla)**: `gate_rule` — toda barrera lineal (tren, orla, frente huerto) se agrupa en
  paquetes de 3-4 piezas con PUERTAS ≥1,80 m cada ≤12 m; los huecos residuales se cierran a <0,30 m
  (leen como una masa) o se abren a ≥1,20 m. El eje Mayor–Alcalá se libera al ensanchar las puertas del
  frente sur de C1 y del tren SE.
- **Riesgo**: bajo — el rosario se conserva (grupos + pausas ya existen en 0F53E6F0).

## CR-3 · CINTA +6,00: ACCESO, SEGURIDAD, GEOMETRÍA Y CLIMA  *(la pieza más débil, doble RED)*
- **Incidencias**: V-035/036/037/042/043/044, V-038 (radio 2,29), V-024 (gálibo 2,31 bajo zancas),
  V-020 (escalera sobre eje Montera), CL-004 (21 % sombra, MRT 57,7). ≈ 11.
- **Origen**: escalera parametrizada por nº fijo de peldaños (16) sobre zanca corta; sin familia de
  elevación; traza polilínea sin control de curvatura; cota +6,00 entre capas de dosel.
- **Corrección**:
  a) **Escaleras reales** (6): dos tramos 17+17, CH 0,170 / H 0,290 (2CH+H=0,63), meseta 1,50 m,
     doble pasamanos, zanca cerrada donde gálibo <2,20; posición validada por guard (la de (43.4,−5.9)
     se reubica: bloquea Montera y está a 1,57 m tras el soporte de la boca de Cercanías).
  b) **3 ASCENSORES-CÁPSULA** integrados en el lenguaje (torre ligera transparente Ø2,4 + cabina rosa
     tipo POD + plataforma de embarque 2,0×2,5): nodos C1-oeste, C2-norte y C3-este → itinerario
     accesible real a la cota +6,00 en los tres clústeres.
  c) **Confort climático sin segundo techo**: los 3 discos que HOY atraviesan el tablero (V-063/068/069/070)
     se elevan a +8,30 y pasan a dar sombra a la cinta (de colisión a función); se añaden ~14 LEAF_M a
     +8,2-8,4 alternados ±2,3 m del eje SOLO en tramos sin cobertura (perfil `_data/cinta.json`);
     colgantes +15 %; 8 nebulizadores de barandilla alimentados de los troncales.
  d) **Barandilla completa**: travesaño intermedio a 0,55 + rodapié 0,10 (V-044).
  e) **Radio**: suavizado local de la traza (Chaikin selectivo) hasta radio ≥4,7 m (V-038).
  f) Evacuación de agua del tablero: documentada como detalle constructivo (limahoya + gárgola en
     soportes), sin cambio geométrico en esta fase.
- **Riesgo**: medio — es el mayor cambio; se preserva "pasear entre las copas" (sombra alterna, no túnel).

## CR-4 · near_corr SOBRE-AMPLIO: EL PROYECTO SOMBREA LA ESTANCIA Y DEJA AL SOL EL MOVIMIENTO
- **Incidencias**: CL-005 (corredores −1,07 K vs −5,99 K), CL-002 parcial (hotspots EN corredores/istmo:
  CL-HOT-010/012/014/021/022/024, y CL-HOT-002 centro-sur). ≈ 8 zonas.
- **Origen**: `near_corr` excluye de los corredores TODO, incluido el dosel alto que no obstruye.
- **Corrección (regla)**: separar exclusión de SUELO (se mantiene) de exclusión AÉREA (se deroga para
  cota ≥4,6): **discos de corredor** LEAF_M/L a 4,8-5,2 sobre los tramos-hotspot del istmo y de los
  corredores N (mástiles fuera del eje, ≥2,2 m), y 5 árboles de sombra en el paseo norte (CL-HOT-020).
  El eje Mayor–Alcalá solo se sombrea en su tramo oeste: el tramo este queda como **ventana de sol de
  invierno** (CR-8) y banda visual de Correos.
- **Riesgo**: bajo — más proyecto donde ya hay proyecto; los claros deliberados se respetan.

## CR-5 · HEIGHT_SYSTEM DESCRIBE LA INTENCIÓN DE 03A, NO EL MODELO
- **Incidencias**: V-028/029/030/032/034 (5 fuera de rango) + V-027/031/033 (declarado no construido). ≈ 8.
- **Origen**: el documento se congeló en 03A; la geometría evolucionó legítimamente (decisión del autor: manda el modelo).
- **Corrección**: `HEIGHT_SYSTEM_v2.md` describiendo lo CONSTRUIDO (bandas reales del dosel 4,2-5,6 /
  6,1-7,4 / 8,2-8,5 + variaciones intencionales + los no-construidos como decisiones D9/D18);
  anomalías REALES sí se corrigen: copas de árbol con base <2,50 → poda de formación en el bloque
  (base de copa ≥2,55, resuelve V-025 y V-030 y la colisión LEAF×ÁRBOL V-067); V-027 (respaldo
  declarado y no construido) se construye (existía en el piloto).
- **Riesgo**: nulo.

## CR-6 · SIN PROTOCOLO NI RESERVA TÉCNICA DE MANTENIMIENTO
- **Incidencias**: V-057..V-062 (56/133 componentes). ≈ 6 (cientos de piezas).
- **Origen**: ninguna regla reservó espacio de operación; los depósitos-gota se implantan en racimo a
  2,4 m; el vivero cae sobre el racimo de pods; nada garantiza el paso de una plataforma elevadora.
- **Corrección**: `MAINTENANCE_PROTOCOL.md` clasifica TODOS los componentes por método (suelo manual
  0,90 m / plataforma 2,50 m / desde cinta ≤6 m / pates+plataforma en depósito +10,5 / desmontable);
  geometría mínima: re-espaciado de gotas (1,0 m), vivero desplazado 1,5 m del racimo, puerta de 1,2 m
  en la jardinera que encierra D-C1-1, plataforma 1,2×1,2 + pates en los 6 postes de depósito,
  **3 registros técnicos** de suelo (1,2×0,8×1,1, uno por clúster junto al bombeo G4) y **línea de
  recirculación** por clúster (cierra CL-006/CL-003 como sistema: depósito→balsas→estanques→registro→depósito).
- **Riesgo**: bajo — piezas técnicas en lenguaje del proyecto.

## CR-7 · BANDA DE METRO APLICADA SOLO A LAS FAMILIAS DE 03B
- **Incidencias**: V-046 (RED Cercanías: RIB_SUP a 1,57 m), V-048/050/051 (11 piezas menores). ≈ 4.
- **Origen**: la exclusión r=5,5 se aplicó a discos/mástiles/cápsulas en 03B, pero la vegetación E02,
  los NEB_POST, un soporte de cinta y el bordillo de E-3 se implantaron después con reglas propias.
- **Corrección**: la banda entra en `conflict_guard` para TODA familia con base <+2,50 (criterio
  anti-falso-positivo del libro: la estructura aérea a +9,7-10,5 NO invade); reubicación del soporte
  de Cercanías (±3 m por la traza), 4-5 NEB_POST, 2 piezas vegetales, E-3 a (10,4, 20,4). El resto de
  casos queda documentado para contraste normativo posterior (banda sigue siendo PROVISIONAL).
- **Riesgo**: nulo.

## CR-8 · CONFLICTOS DE OBJETIVOS NO ARBITRADOS (visuales / invierno / atrapamiento)
- **Incidencias**: V-052 (reloj 38,6 %), CL-001 (invierno −48 %), atrapamiento radiante (MRT sube en
  46 % de celdas, bordes de racimo y bajo redes). ≈ 3 sistémicas.
- **Origen**: sombra, visuales y sol de invierno compiten por el mismo cielo y nadie arbitró.
- **Corrección (arbitraje explícito, no persecución de cifras)**:
  · **Red de conos visuales intencionados** al reloj/torre desde los 5 accesos + estatua + splash +
    2 nodos de cinta → entra en el guard: NINGÚN elemento nuevo dentro de un cono; los existentes se
    documentan (el 38,6 % es el precio declarado del dosel).
  · **2 ventanas de invierno** donde no se añade sombra nueva: splash+banda Correos y eje este;
    atributo `caduco` en árboles nuevos y `vaciado_invernal` en la lámina de microalgas (operación).
  · **Atrapamiento**: los discos nuevos de CR-3/CR-4 convierten sombra parcial mala en sombra real en
    los bordes; no se añaden redes nuevas (tau_net 0,75 es la peor óptica del sistema); las piezas
    climáticamente redundantes (16 discos con exclusiva 0) SE CONSERVAN salvo doble redundancia — los
    3 que además colisionaban con la cinta cambian de cota y GANAN función.
- **Riesgo**: bajo — arbitraje documentado, sin desmontar el dosel.

## CR-9 · PIEZAS DECLARADAS SIN CONSTRUIR + DETALLES DE FUENTE
- **Incidencias**: V-027 (respaldos), tubería troncal cruzando ejes a +0,32 (V-019: canaleta rebajada
  z=0,08 en cruces con corredor), bug JSON clave duplicada 'carmen-correos' en overrides (libro),
  a2_cables.json vacío (instrumento, no modelo). ≈ 4.
- **Corrección**: respaldos construidos; `pipe_dip_rule` en cruces; overrides v003 sin claves duplicadas;
  estatua de **Carlos III consolidada** (DEC-0006: (−28,−14) G2+, pedestal 4,4×2,6×2,4 + volumen ecuestre
  ~4,2, respeto r=8, eje curvado localmente a y=−17 entre x=−36..−20, cono visual propio hacia el reloj).

---

## Orden de ejecución
1. `make_v003.py` → geometria_maestra_v003.json (datos: cotas de disco, puertas de tren, corredor-estatua,
   E-3, gotas, discos nuevos con rol, árboles N, balsa B-C3b, conos, ventanas de invierno).
2. `build_all_03b6.py` (copia del generador + conflict_guard + escaleras/ascensores/barandilla/poda/
   respaldos/registros/canaletas/plataformas) → MASTER_ARCHITECTURE_v003.3dm · SOL_FULL_SCENE_v002.3dm ·
   ASSET_LIBRARY_v002.3dm · SOL_PRESENTATION_MASTER_v001.3dm + escena en memoria.
3. Reauditoría 03B.5 completa sobre v003 (mismo interceptor; sin abrir .3dm) + clima E2-16h A/B para
   los campos afectados (sombra/MRT/UTCI/cinta) con los 4 avisos metodológicos del libro aplicados.
4. `03B6_BEFORE_AFTER.pdf` + diff v002→v003 + actualización E03 (H5 y config) + veredicto.

Continúo automáticamente (§15): ninguna corrección altera la identidad (implantación, dosel, cinta
como paseo entre copas, trenes-rosario, paleta, lenguaje de piezas se conservan).
