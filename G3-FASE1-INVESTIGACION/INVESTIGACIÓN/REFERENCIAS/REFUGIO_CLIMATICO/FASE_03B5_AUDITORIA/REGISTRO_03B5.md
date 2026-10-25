# REGISTRO — FASE 03B.5 · AUDITORÍA GEOMÉTRICA Y DE VIABILIDAD
2026-08-10 · registro dual de investigación: **criterio / interpretación · acción · resultado · conclusión**

**ESTADO: AUDITORÍA COMPLETADA. NADA HA SIDO CORREGIDO. EL MASTER NO SE HA MODIFICADO.**
Ni `MASTER_ARCHITECTURE_v002.3dm` ni `SOL_FULL_SCENE_v001.3dm` ni `geometria_maestra_v002.json` han
sido abiertos en escritura. La auditoría reconstruye la escena **en memoria** y sólo lee.

---

## 0 · MÉTODO

**Criterio.** Auditar el modelo aprobado exige medir *exactamente* la geometría aprobada, no una
aproximación. Abrir los `.3dm` con `rhino3dm` daría las instancias de bloque sin hornear y obligaría a
replicar las transformaciones; leer `_viewer/scene_full.js` daría las mallas ya en coordenadas de mundo
pero **sin nombre** para los objetos no instanciados (la estructura, la cinta, el agua), que es
precisamente lo que hay que poder nombrar en un informe de conflictos.

**Acción.** Se importa `build_all_03b.py` y se interceptan sus tres puntos de salida —`add_mesh`,
`place`, `add_curve`— sustituyéndolos por captadores que hornean la transformación y conservan
`(nombre, capa, bloque, vértices, caras)`. Después se llama a `build_site(..., full=True)` con una
`Scene` nula. La guardia `if __name__ == '__main__'` del script original impide que se escriba ningún
archivo.

**Resultado.** 6.857 objetos: **6.672 mallas · 394.610 triángulos** · 185 curvas (159 cables, 20
generatrices, 6 bajantes). La cifra coincide exactamente con la registrada en `REGISTRO_E02.md`
("6.672 mallas / 395k tris"), lo que confirma que lo auditado es el modelo aprobado y no otra cosa.
Reconstrucción completa en 0,5 s; auditoría entera en 35 s.

**Conclusión.** El método es reproducible y no invasivo: `python audit_run.py` vuelve a medir desde
cero. Si la geometría maestra cambia, la auditoría se repite sin tocar nada.

### Instrumentos de medida
| Instrumento | Resolución | Para qué |
|---|---|---|
| Rejilla de suelo | 0,25 m (848×492 celdas) | ocupación, anchuras, gálibos, densidad |
| Banda de cuerpo | z ∈ [0,05 · 2,10] m | qué obstruye realmente el paso |
| Vóxel de colisión | 0,20 m | interpenetración entre familias |
| Vóxel de visibilidad | 0,50 m × 0,50 m alt. | trazado de rayos ojo→objetivo |
| Persona de referencia | 1,70 m · hombros 0,55 · silla 0,80×1,20 | validación espacial |

### Umbrales usados — y de dónde salen
No se ha aplicado **ninguna** normativa. Los umbrales son criterios de trabajo, y su origen se declara
para que puedan discutirse por separado del hallazgo que producen:

| Umbral | Valor | Origen |
|---|---|---|
| Gálibo mínimo bajo elemento firme | 3,00 m | `HEIGHT_SYSTEM`, regla 7 (**del propio proyecto**) |
| Anchura de cruce de dos personas | 1,80 m | criterio de trabajo de esta auditoría |
| Anchura de holgura | 3,00 m | criterio de trabajo de esta auditoría |
| Banda de exclusión de Metro | 5,5 m | decisión **D03B-02** (**del propio proyecto**) |
| Envolvente de cabeza | 1,85 m | persona 1,70 + 0,15 |

La identificación de la normativa aplicable (Orden VIV/561/2010, CTE DB-SUA, ordenanza municipal,
criterio real de Metro de Madrid) es el paso siguiente y **deliberadamente no se hace aquí**.

---

## 1 · RECORRIDOS

**Criterio.** Medir la red peatonal por dos vías independientes: el **ancho transversal** sobre los 5
corredores declarados en `circulacion.corridors`, y la **holgura libre local** (2 × distancia al
obstáculo más próximo) sobre toda la superficie.

**Acción.** Remuestreo de cada eje a 0,5 m; rayos perpendiculares a ambos lados hasta el primer
obstáculo; transformada de distancia sobre el suelo libre; barrido de umbral con etiquetado de
componentes para los cuellos de botella entre los 10 accesos (45 pares).

**Resultado.**
- Ámbito 11.014 m², suelo libre a nivel de cuerpo **9.901 m² (90 %)**, ocupación **10,1 %**.
- Holgura mediana **6,96 m**; el percentil 5 (0,71 m) corresponde a las celdas pegadas a bordes.
- Cuello de botella del peor par de accesos: **10,75 m**, tanto pudiendo rodear como obligando a
  cruzar el ámbito. Los 45 pares están entre 10,75 y 40 m.
- Exigiendo 3,00 m continuos sigue conectado el **73 %** del suelo libre en 2 componentes.
- **89 pasos** por debajo de 1,20 m de holgura, casi todos entre jardineras (`PLANTER`) o entre
  jardinera y vegetación.
- **1 bolsa real** de 44 m² sin conexión pisable en (6,9 · −4,1), cercada por jardinera + vegetación + agua.
- Dos ejes declarados atraviesan geometría: `preciados-carretas` en 1 estación (sobre un estanque) y
  `montera-espozymina` en 3 (sobre un soporte de la cinta).

**Conclusión.** 🟢 a escala de red, 🔴 en puntos concretos. La plaza no tiene un problema de capacidad
—está holgadamente conectada— sino una acumulación de estrangulamientos locales producidos por
implantar familias con reglas independientes. **El hallazgo estructural del capítulo no es un ancho:
es que dos de los cinco ejes declarados ya no describen un recorrido posible.**

**Rectificación durante el trabajo.** El primer pase midió los estrechamientos sobre el ancho
transversal de fachada a fachada; en una plaza abierta esa medida da p50 = 40 m y no discrimina nada
(detectaba 4 estrechamientos). Se rehízo sobre la holgura local, que es la que estrangula de verdad.

---

## 2 · GÁLIBOS

**Criterio.** Altura libre desde el pavimento hasta la cara inferior del primer elemento, sólo sobre
celdas pisables. Interpolación exacta del plano de cada triángulo, no bounding box.

**Acción.** Rasterizado en modo `zmin` de los 394.610 triángulos por encima de 2,10 m.

**Resultado — y la corrección que lo cambió todo.** El primer pase dio un mínimo de **2,21 m** y 20
manchas por debajo de 3,00 m, y se registró como incumplimiento de la regla 7. Al generar las
secciones automáticas del capítulo 11 se vio que **los cuatro mínimos eran copas de árbol**
(`VEG2_ARBOL_A`), no estructura. La regla 7 dice literalmente *"gálibo mínimo bajo cualquier elemento
**firme** sobre paso: 3,00"*. Una copa no es un elemento firme. Se rehízo el análisis separando ambos
campos:

| | mínimo | superficie afectada | causa |
|---|---|---|---|
| Elemento **firme** | 2,31 m | **3,2 m²** (0,08 % del suelo cubierto) | zancas de las escaleras de la cinta |
| **Vegetación** | 2,21 m | 33,4 m² por debajo de 2,50 m | copas de `VEG2_ARBOL_A/B/EX` |

- Suelo pisable bajo algún elemento: 3.825 m² (39 %). Mediana del gálibo: 6,00 m. p05 bajo firme: 4,42 m.
- **0 cables** por debajo de 3,00 m: los tirantes arrancan exactamente en `H_BRANCH_START` = 3,00.

**Conclusión.** 🟢 para la estructura: el dosel, los loops, la cinta, las cápsulas y los depósitos
cumplen la regla que el propio proyecto se dio. 🟡 para el arbolado: poda de formación a 2,20–2,50 m,
práctica normal, o elevar el centro de copa en el bloque. 🔴 sólo bajo las escaleras. **Sin las
secciones del capítulo 11 este capítulo habría concluido lo contrario: se registra el error para que
conste que la validación por número no bastó.**

---

## 3 · ALTURAS

**Criterio.** Contrastar los 22 parámetros del `HEIGHT_SYSTEM` contra la geometría realmente generada,
midiendo cada bloque y cada objeto con nombre.

**Resultado.** 14 OK · 5 fuera de rango · 3 declarados y no construidos.

- **Fuera de rango:** `H_GROUND_TANK` 1,35 → **2,25** (la cota declarada describe el cuerpo del
  depósito, no el cono superior), `H_NURSERY_TOWER` 3,00 → 3,32, `H_TREE_EXIST` 7,00 → 8,51,
  `H_CLEAR_MIN` 3,00 → 2,31 (ver capítulo 2), y la **familia de dosel**.
- **No construidos:** `H_BENCH_BACK` (no hay respaldos), `H_TANK_TOWER` (no hay torre de depósitos
  apilados), `H_LOGISTIC_RAIL` (reserva G4 apagada — **coherente con la decisión D9**, no es un error).
- **Familia de dosel:** el sistema declara tres capas escalonadas 5,00 / 6,75 / 8,50 y D10 fija 8,50
  como máximo. La geometría lee la cota de cada disco del JSON y la recorta a [4,20 · 8,50]:
  **32 de los 67 discos** caen a más de ±0,30 m de cualquiera de las tres capas.

**Conclusión.** 🟡 documental, no constructivo. Ninguna desviación compromete el uso. Pero el
`HEIGHT_SYSTEM` ha dejado de describir el modelo: describe la intención de 03A. **Antes de E03 hay que
decidir cuál de los dos manda**, porque E03 va a citar cotas.

---

## 4 · CINTA / PASARELA ELEVADA

**Criterio.** Medir la pasarela como se mediría una obra: rasante, pendientes, ancho útil, curvatura,
puntos de acceso y la escalera peldaño a peldaño.

**Resultado.**

| Parámetro | Medido |
|---|---|
| Desarrollo | 519 m a **+6,00 m constante** |
| Pendiente longitudinal / transversal | **0,0 % / 0,0 %** |
| Ancho total / útil entre barandillas | 2,50 m / **2,31 m** |
| Barandilla | 1,05 m, sin travesaño intermedio ni rodapié |
| Gálibo bajo el tablero | 5,78 m |
| Soportes | 40 montantes con capitel, fuera de corredores |
| Radio de curvatura mínimo | **2,3 m** |
| Cambios de nivel | 1 (0,00 → +6,00) |
| Accesos | **6 escaleras · 0 rampas · 0 ascensores** |
| Contrahuella / huella | **0,385 m / 0,424 m** |
| 2CH + H | **1,194 m** (regla de comodidad: 0,62–0,65) |
| Pendiente de escalera | **90,9 % · 42,3°** |
| Barandilla de escalera | no existe |

Las 6 coronaciones caen entre 0,7 y 2,9 m del eje de la cinta: acometen, aunque la de (26 · 15) a 2,9 m
merece revisión.

**Conclusión.** 🔴 **El hallazgo más grave de toda la auditoría.** No es que la escalera sea incómoda:
con 16 peldaños para salvar 5,78 m no es una escalera, es una escala. El generador reparte el desnivel
sobre una zanca de 6,36 m sin meseta ni pasamanos. El proyecto tiene 519 m de paseo por el dosel y
ninguna forma utilizable de subir. Estrategias posibles (**no aplicadas**): alargar la zanca a ~11 m
con 32 peldaños de 0,18/0,30 y meseta intermedia; o resolver el acceso con ascensor/rampa, que además
es la única vía para hacerlo accesible. La pendiente transversal 0,0 % implica además que el tablero
no evacua agua.

---

## 5 · ACCESIBILIDAD GEOMÉTRICA

**Criterio.** *No emitir certificado.* Sólo identificar qué itinerarios **pueden** funcionar como
accesibles y cuáles claramente no.

**Resultado.** El plano de plaza es horizontal en todo el ámbito (cota 0,00): a nivel de suelo no hay
pendientes que evaluar y la accesibilidad depende sólo de anchura, obstáculos y giros.

| Itinerario | Holgura mín. | % traza ≥1,80 | Pre-chequeo |
|---|---|---|---|
| eje-mayor-alcala | 1,80 m | 100 % | 🟢 APTO |
| arenal-alcala | 5,10 m | 100 % | 🟢 APTO |
| preciados-carretas | 0,00 m | 98 % | 🟡 CONDICIONADO |
| carmen-correos | 0,50 m | 98 % | 🟡 CONDICIONADO |
| montera-espozymina | 0,00 m | 94 % | 🔴 NO APTO (3 estaciones sobre geometría) |
| **CINTA +6,00** | 2,31 m | 100 % | 🔴 **NO APTO** (único acceso: escalera al 91 %) |

Bordes sin protección: 4 estanques con bordillo de 0,60 m sin barandilla ni cambio de textura.

**Conclusión.** Dos itinerarios accesibles completos de este a oeste y norte a sur — el esqueleto
funciona. Dos condicionados a liberar puntos concretos. Uno inviable por trazado. Y **la cota +6,00
sin ningún medio accesible**: hay que decidir explícitamente si la cinta se dota de ascensor o se
declara recorrido complementario no accesible. Es una decisión de proyecto, no un defecto de dibujo.

---

## 6 · METRO / CERCANÍAS

**Criterio.** Auditar la banda de 5,5 m de D03B-02 **sin interpretarla como obligación normativa**.

**Acción, y la corrección que la hizo válida.** El primer pase midió distancia en planta y devolvió
"0,09 m" en el acceso de Alcalá — alarmante y **falso**: era un loop cruzando por encima a +9,7 m. Se
rehízo separando (a) obstáculo a nivel de boca (base por debajo de +2,50 m, con el que se tropieza o
que estrecha el frente de evacuación) de (b) estructura aérea, que cubre pero no invade.

| Acceso | Ámbito | Obstáculo a nivel de boca | n<5,5 m | Frontal libre | Gálibo |
|---|---|---|---|---|---|
| Cercanías | sí | **1,57 m** (`RIB_SUP`) | 5 | 5,75 m | 6,00 m |
| Carmen | sí | **2,95 m** (`RIB_SUP`) | 6 | 3,25 m | 6,00 m |
| Alcalá (40 · 12) | sí | 3,02 m (`NEB_POST`) | 2 | 6,50 m | 6,00 m |
| Alcalá (47 · 19) | sí | 4,21 m (`NEB_POST`) | 4 | 6,75 m | 6,00 m |
| Mayor / Carretas / C. Comercial | no | 12,8 / 16,7 / 40,3 m | 0 | — | cielo |

**Conclusión.** 🔴 uno (Cercanías, soporte de cinta a 1,57 m), 🟡 tres. Ningún acceso queda tapado: el
gálibo sobre las cuatro bocas del ámbito es de 6,00 m. La banda de 5,5 m se aplicó en 03B a discos y
mástiles, pero la vegetación E02 y las piezas menores se implantaron después con reglas propias.
**Acción pendiente antes de mover nada: contrastar con el criterio real de Metro de Madrid.** La banda
de 5,5 m sigue siendo provisional.

---

## 7 · VISUALES

**Criterio.** Desde una rejilla de observadores a 1,65 m sobre suelo pisable, ¿qué porcentaje de la
plaza conserva visión directa de la Real Casa de Correos, la torre y el reloj?

**Acción.** Vóxel de 0,50 m sobre toda la escena; 2.474 puntos de observación; rayo ojo→objetivo con
paso de 0,45 m. La membrana ETFE de la cúpula se trata como **translúcida** (opacidad 0,30 en E02);
dosel, copas, cápsulas, estructura y contexto como opacos.

**Resultado.** Casa de Correos **44,6 %** · torre **41,6 %** · reloj **38,6 %**.

**Conclusión.** 🟡. No es un error: es el precio del dosel, que es el argumento entero del proyecto. Se
mide para que la renuncia sea consciente y cuantificada, no para corregirla automáticamente. Si se
quiere subir la cifra, la estrategia con menos daño es abrir un cono visual desde el eje
Mayor–Alcalá retirando 3–6 discos, no aclarar el dosel en general. **Las vistas V07 y V20 de 03B
verifican que el reloj es visible desde puntos concretos; este mapa responde una pregunta distinta.**

---

## 8 · DENSIDAD ESPACIAL

**Criterio.** Detectar áreas excesivamente densas *después de E02*, lo que exige comparar contra el
estado anterior, no medir sólo el actual.

**Acción.** Se reconstruye también la escena `full=False` (MASTER, sin vegetación E02) y se compara
sector a sector en retícula de 20×20 m.

**Resultado.** Ocupación global del ámbito: **9,0 % (MASTER) → 10,1 % (E02)**, es decir **+1,1 puntos**.
Sector más ocupado: (18 · 25) con 20,8 %. Ningún sector supera el 25 %. Superficie cubierta por
dosel/cinta: 28,4 % del ámbito (hasta 74 % en el sector (58 · 5)).

**Conclusión.** 🟢, y en contra de lo que se temía en `REGISTRO_E02.md` §4 ("la densidad del huerto de
C1 es alta"). En términos de **ocupación de suelo** E02 no ha densificado la plaza: la vegetación se
implantó sobre jardineras y bajo dosel, no sobre el suelo de paso. Si hay una sensación de densidad
es de **cobertura aérea**, que es otra magnitud y en el sector (58 · 5) llega al 74 %. La decisión de
aclarar 1 de cada 3 filas de huerto sigue siendo legítima, pero por criterio visual, no por saturación
medible del suelo.

---

## 9 · MANTENIMIENTO

**Criterio.** Primera auditoría *geométrica*: ¿queda sitio para llegar a cada componente con la
geometría E02 puesta? Un rojo no significa "imposible de mantener", significa "no hay superficie de
apoyo suficiente sin retirar vegetación o mobiliario".

**Resultado.** 133 componentes auditados, **56 sin acceso suficiente**.

| Componente | uds | sin acceso | Holgura mediana |
|---|---|---|---|
| Canopy / bajante | 67 | **37** | 2,00 m |
| Nebulizador +4,0 | 42 | 8 | 5,78 m |
| Depósito de suelo | 6 | **6** | 0,71 m |
| Vivero | 3 | **3** | 0,71 m |
| Depósito +10,5 / bajante | 12 | 2 | 3,92 m |
| Bombeo | 3 | 0 | 2,50 m |

**Conclusión.** 🔴 en depósitos de suelo y viveros (0,71 m de holgura: no cabe un operario con
herramienta), 🟡 en el dosel. La causa es única y anterior a E02: **el modelo 03B no contiene ninguna
reserva de área técnica.** Los depósitos se implantaron en racimos de 2,4 m de paso y los viveros
juntos por lógica de composición. Acción pendiente: definir primero el protocolo de mantenimiento
(¿desde la cinta? ¿plataforma sobre pavimento? ¿módulos desmontables?) y sólo después decidir qué
se mueve.

---

## 10 · COLISIONES

**Criterio.** Comprobación sistemática entre familias distinguiendo **contacto intencionado** de
interpenetración accidental. Se declara explícitamente la lista de pares intencionados
(mástil↔disco, estructura↔cinta, jardinera↔vegetación, estructura↔agua, estructura↔cápsula…) para que
el criterio sea discutible.

**Acción.** Vóxel de 0,20 m por familia, intersección de conjuntos, y desglose objeto a objeto de los
pares no intencionados mediante índice clave→objeto.

**Resultado.** 24 pares de familias en contacto: **12 intencionados, 12 a revisar**. 220 colisiones
objeto-objeto no intencionadas. Las mayores:

| Par | Objetos | Solape |
|---|---|---|
| CANOPY × RIBBON | `LEAF_OV` × `RIBBON_DECK` | 0,304 m³ |
| FURNITURE × PLANTER | `BENCH_0` × jardinera de `MAST_3` | 0,296 m³ |
| FURNITURE × PLANTER | `BENCH_2` × jardinera de `MAST_2` | 0,224 m³ |
| PODS × VEGETATION | `POD_S` × mata de `MAST_2` | 0,216 m³ |
| CANOPY × VEGETATION | `LEAF_M2` × `VEG2_ARBOL_A` | 0,216 m³ |

**Conclusión.** 🔴 los discos de dosel que atraviesan el tablero de la cinta (no es contacto: la hoja
pasa por dentro del paso) y los arcos de banco que entran en la jardinera base de un mástil.
🟡 el resto. Causa común: cada familia se implanta con su propia regla sin comprobación cruzada. El
`near_corr` del generador protege los corredores, pero **nada protege a las familias entre sí**.

---

## 11 · PERSONA DE REFERENCIA

**Criterio.** No fiarse de los números: validar cada conflicto rojo con un volumen humano y una
sección real del modelo.

**Acción, y la corrección que la hizo honesta.** El primer pase evaluaba la celda pisable *más
próxima* al punto de la incidencia; como esa celda siempre está pegada al obstáculo, el test daba
"no pasa" por construcción. Se rehízo distinguiendo: las incidencias **de paso** (recorridos, gálibos,
accesibilidad) se miden en el propio punto, que es el estrangulamiento; las **de objeto** (colisión,
mantenimiento, metro) se miden en su entorno de 2,5 m, porque lo que importa es si cabe una persona
junto a la pieza.

**Resultado.** 31 puntos rojos con coordenada: 16 de paso, 15 de objeto. No admiten el cuerpo (0,55 m):
15. No admiten silla (0,80 m): 15. No admiten el cruce de dos personas (1,80 m): 16. **No admiten la
cabeza (1,85 m): 0.**

**Conclusión.** Matiz importante y tranquilizador: **nadie se golpea la cabeza en ningún punto pisable
del proyecto.** Los incumplimientos de gálibo lo son respecto al criterio propio de 3,00 m, no por
choque físico. Los problemas reales de la persona son de **anchura**, no de altura.

---

## 12 · NO CORREGIR

Se ha respetado íntegramente. Ninguna de las 73 incidencias ha sido reparada. Cada una lleva posición,
magnitud medida, causa, severidad y estrategias posibles, y espera revisión. Verificación: los
`.3dm`, el JSON maestro y `build_all_03b.py` conservan su fecha de modificación anterior a esta fase.

---

## SÍNTESIS

**73 incidencias: 🔴 36 · 🟡 22 · 🟢 15.**

| Capítulo | 🔴 | 🟡 | 🟢 |
|---|---|---|---|
| Recorridos | 16 | 5 | 2 |
| Colisiones | 10 | 0 | 0 |
| Accesibilidad | 3 | 3 | 1 |
| Mantenimiento | 3 | 3 | 0 |
| Cinta | 2 | 1 | 1 |
| Gálibos | 1 | 1 | 1 |
| Metro | 1 | 3 | 3 |
| Alturas | 0 | 5 | 3 |
| Visuales | 0 | 1 | 0 |
| Densidad | 0 | 0 | 4 |
| Persona | 0 | 0 | 1 |

**Lo que aguanta.** La estructura respeta el gálibo que el proyecto se dio. La red peatonal está
holgadamente conectada (73 % del suelo libre sigue unido exigiendo 3,00 m continuos; peor cuello entre
accesos 10,75 m). E02 no ha densificado el suelo. Ningún acceso de Metro queda tapado. Nadie se golpea
la cabeza.

**Lo que no.** La cota +6,00 no tiene acceso utilizable ni accesible. Dos ejes declarados atraviesan
geometría. Hay 89 pasos por debajo de 1,20 m entre jardineras. 56 de 133 componentes técnicos no
tienen sitio para mantenerse. Discos de dosel atraviesan el tablero de la cinta.

**El patrón detrás de casi todo.** Los conflictos no vienen de errores de dibujo sino de una misma
causa: **cada familia se implanta con su propia regla y ninguna comprueba a las demás.** El generador
protege los corredores declarados (`near_corr`) y los claros de metro (`near_metro_pt`), pero no
protege el paso entre jardineras, ni el tablero de la cinta frente a los discos, ni reserva área
técnica. Corregir caso a caso resolvería los 36 rojos; corregir la regla evitaría los siguientes.

**Lo que hay que decidir antes de E03** (son decisiones de proyecto, no de dibujo):
1. La cinta: ¿ascensor/rampa, o se declara recorrido complementario no accesible?
2. `HEIGHT_SYSTEM` frente al modelo: ¿cuál manda?
3. Mantenimiento: ¿cuál es el protocolo, antes de mover ninguna pieza?
4. Metro: contrastar la banda de 5,5 m con el criterio real antes de retirar nada.
5. Reloj visible desde el 38,6 % de la plaza: ¿se acepta o se abre un cono visual?

---

## ERRORES Y RECTIFICACIONES DE ESTA FASE

Se registran porque tres de ellos habrían producido conclusiones falsas:

1. **Metro medido en planta.** Daba "0,09 m" en Alcalá; era un loop cruzando a +9,7 m. Rectificado
   separando obstáculo a nivel de boca de estructura aérea. *Habría reportado una invasión inexistente.*
2. **Gálibo sin distinguir firme de vegetal.** Daba 20 incumplimientos de la regla 7; en realidad la
   estructura cumple y el mínimo son copas de árbol. Detectado al mirar las secciones automáticas.
   *Habría acusado a la estructura de un problema de poda.*
3. **Bolsas aisladas.** El primer pase daba 3 cul-de-sac, dos de ellos de 306 y 227 m²; eran recintos
   del contexto urbano cortados por el borde de mi propia envolvente de análisis. Rectificado
   etiquetando la conectividad sobre todo el suelo libre y atribuyendo el cinturón de cada bolsa.
   *Habría inventado dos cul-de-sac que el proyecto no tiene.* Queda **1** real, de 44 m².
4. **Test de persona sesgado.** Evaluaba la celda libre más próxima, que siempre está pegada al
   obstáculo: "no pasa" salía por construcción. Rectificado distinguiendo incidencias de paso y de objeto.
5. **Estrechamientos sobre ancho transversal.** En plaza abierta no discrimina (p50 = 40 m).
   Rehecho sobre holgura local.
6. Cuello de botella: el barrido empezaba en 8,0 m y saturaba; subido a 40 m.
7. Rendimiento: el detalle de colisiones era O(n²) sobre 3.193 × 125 objetos. Reescrito con índice
   clave→objeto. El maximin-Dijkstra por accesos se sustituyó por barrido de umbral con etiquetado.
   La auditoría completa pasó de no terminar en 10 min a 35 s.
8. Consola Windows en cp1252: el carácter «→» abortaba el log. `sys.stdout.reconfigure(utf-8)`.

---

## ENTREGA

`VIABILITY_AUDIT_MASTER.pdf` (10 láminas A3) · `PATH_WIDTH_MAP.pdf` (2) · `CLEAR_HEIGHT_MAP.pdf` (2) ·
`ACCESSIBILITY_PRECHECK.pdf` · `METRO_CLEARANCE_AUDIT.pdf` · `VIEW_CORREOS_CLOCK.pdf` ·
`COLLISION_REPORT.pdf` · `MAINTENANCE_ACCESS.pdf` · `VIABILITY_METRICS.csv` (433 filas) ·
`ISSUES_REGISTER.md` (V-001…V-073) · este registro.

Motor reproducible: `audit_core.py` · `audit_run.py` · `audit_report.py`. Datos intermedios en `_data/`.

**STOP. No se ejecuta E03 ni se corrige nada sin tu revisión.**
