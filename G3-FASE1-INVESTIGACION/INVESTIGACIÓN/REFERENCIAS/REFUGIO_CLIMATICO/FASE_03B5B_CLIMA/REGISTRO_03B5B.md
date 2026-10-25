# REGISTRO — FASE 03B.5B · AUDITORÍA CLIMÁTICA DEL REFUGIO
2026-08-10 · registro dual: **criterio / hipótesis · acción · resultado · interpretación · rectificación**

**ESTADO: AUDITORÍA COMPLETADA. NADA HA SIDO CORREGIDO. EL MASTER NO SE HA MODIFICADO.**
Registro forense en `_FORENSIC_PROCESS\` (EVT-000019 → EVT-000036, DEC-0003/0004, snapshot `FIN_03B5B`).
El tramo anterior a las 16:10 se registra desde artefactos reales, marcado como tal; **nada se reconstruye
inventado** (DEC-0003).

---

## LA RESPUESTA, ANTES DEL DETALLE

**¿Es esto realmente un refugio climático?**
**Sí, pero como pantalla radiante, no como acondicionador de aire.**

El proyecto retira del suelo de la plaza **283 kWh/m²** durante el verano (−43,7 %), baja la temperatura
radiante media **10,8 K** y la del pavimento **7,5 K**. Eso es mucho y es real. Pero el índice de confort
UTCI sólo mejora **2,6 K** (3,3 K con nebulización), porque el UTCI está dominado por la temperatura del
**aire**, que una estrategia de sombra apenas cambia (≈1,0 K a escala plaza).

**36,4 % del ámbito** (4.010 m², 4.563 m² con nebulización) baja de categoría en la escala oficial de
estrés térmico. **4.884 m² de suelo pisable siguen en estrés térmico muy fuerte.**

Y el hallazgo más incómodo: **el beneficio disminuye cuanto más se necesita** — ΔUTCI −3,0 K en verano
normal, −2,6 K en tarde calurosa, **−2,05 K en ola de calor**.

---

## 0 · MÉTODO Y BASE

**Criterio.** Ningún resultado puede proceder de un coeficiente global ni de una analogía. Todo sale de la
geometría real, del clima real y de física cerrada, con la certeza de cada cifra declarada.

**Acción.** Se reconstruye en memoria la misma escena de 03B.5 y se vóxeliza a 0,50 m en dos estados:
**A** = contexto existente (edificios OSM + arbolado existente) y **B** = A + proyecto.

**Resultado.** 6.672 mallas · 394.610 triángulos · huella sha256 de vértices `41a82b7263449037…`,
idéntica a 03B.5. Ámbito 11.020 m² frente a 11.014 m² (0,05 % por el remuestreo de 0,25 a 0,50 m).

**Interpretación.** La comparación es limpia: misma geometría urbana, misma orientación, mismo clima,
misma rejilla y misma escala de color. **La intervención es la única variable.**

**Decisión registrada.** El arbolado existente (OSM) se incluye en **ambos** estados. Atribuir al proyecto
la sombra de árboles que ya existen habría inflado el resultado.

---

## 1 · CLIMA — no un «Madrid genérico»

**Criterio.** Fuente identificable, con coordenadas, periodo y fecha de descarga.

**Acción.** Descarga real de dos series de PVGIS v5.2 en **40,4169 N · 3,7035 O · 665 m** (Puerta del Sol):
TMY horario (8.760 h con T2m, HR, G(h), Gb(n), Gd(h), **IR(h)**, WS10m, WD10m, SP) y serie horaria
2005–2020 (140.275 h, base de radiación SARAH2, temperatura ERA5).

**Resultado.**

| Ventana crítica 15 jun – 15 sep (2.232 h) | |
|---|---|
| Ta media / máxima | 23,5 °C / 37,6 °C |
| Ta media de tarde (12–18 UTC) | 28,8 °C · p95 34,3 °C |
| HR media / mínima | 38 % / 6 % |
| Punto de rocío mediano de tarde | **4,3 °C** |
| Viento medio / dominante | 2,26 m/s · **SO** (44 % de las tardes) |
| Día más cálido real del registro | **2018-08-03 · 40,1 °C** |

**Interpretación.** El dato que gobierna toda la auditoría es el punto de rocío: **4,3 °C**. El aire de
Madrid en verano es extremadamente seco, y eso deja una **depresión de bulbo húmedo de 13,8 K en tarde
calurosa y 22,2 K en ola de calor**. Es un margen enorme para enfriamiento evaporativo — y explica por qué
la nebulización, y no la sombra, es la única palanca capaz de tocar la temperatura del aire.

**Escenarios** (todos con radiación de cielo despejado del TMY y humedad por conservación del punto de rocío):
E1 verano normal (29,2 °C) · E2 tarde calurosa (34,7 °C, p95 real) · E3 ola de calor (**40,1 °C, día real**)
· E4 = E2 con nebulización activa.

**Limitación declarada, no disimulada.** ERA5 resuelve ~30 km: **estos datos no contienen la isla de calor
urbana de Madrid centro.** No se ha aplicado ningún ajuste oculto. Los valores absolutos de UTCI son
conservadores; los **deltas A→B son robustos**, porque un sesgo común en Ta se cancela casi por completo en
la diferencia. Registrado en DEC-0004.

---

## 2 · VALIDACIÓN DEL INSTRUMENTO (antes de creerse ningún mapa)

**Criterio.** Un error sistemático en la posición del sol corrompe en silencio todos los resultados.

**Acción.** Se contrasta el algoritmo PSA implementado contra un dato independiente: la columna `H_sun` de
la serie PVGIS.

**Resultado.** Error medio **−0,031°**, desviación 0,123°, máximo absoluto 0,338° sobre 117 muestras.
Solsticio de invierno 26,07° (teórico 26,14°); equinoccio 49,57° (teórico 49,58°).

**Conclusión.** El instrumento mide. A partir de aquí los mapas son discutibles en sus hipótesis, no en su
aritmética.

---

## 3 · SOL Y SOMBRA

**Acción.** 431 posiciones solares por estado (31 días muestreados cada 3 días × horas de luz), trazado de
rayos sobre el vóxel con transmitancia por clase óptica.

**Resultado.**

| | ACTUAL | PROPUESTA |
|---|---|---|
| Sombra en 12–18 h (ámbito) | **5,3 %** | **45,3 %** |
| Sombra en 12–18 h (suelo pisable) | 5,8 % | 40,5 % |
| Horas de sol acumuladas | 1.206 h | 635 h |
| m² de sombra añadidos | — | **4.407 m²** |

**Interpretación.** Puerta del Sol hoy es una plaza esencialmente sin sombra, y la poca que tiene la dan los
edificios del borde. El proyecto multiplica por 8,5 la sombra en las horas de mayor estrés. **Éste es el
logro más sólido de la propuesta y no admite discusión.**

**Pero el reparto es muy desigual:** bajo dosel 84,9 %, viveros 85,3 %, huerto 81,9 % — **corredores
peatonales 21,5 %**. El proyecto sombrea la estancia y deja al sol el movimiento. Es consecuencia directa
de la regla `near_corr` del generador, la misma que en 03B.5 garantizaba la transitabilidad.

---

## 4 · RADIACIÓN

**Resultado.** 648 → **365 kWh/m²** acumulados en la ventana: **−43,7 %**, con puntos que llegan al −100 %.
Sobre los 11.020 m² del ámbito son del orden de **3.100 MWh** de energía solar retirados del balance de la
plaza en 93 días.

---

## 5 · DOSEL, DISCO A DISCO

**Rectificación registrada (EVT-000027).** El primer pase midió la sombra proyectada **bruta**, que por
construcción es `área_disco × horas`: los 67 discos daban una eficiencia idéntica (555–562). Era una
tautología, no una medida. Se rehízo midiendo la **sombra exclusiva** (celdas que sombrea ese disco y
ningún otro) y la sombra sobre suelo pisable.

**Resultado con la métrica corregida** — rango de 0 a 98 m²:

- **Los discos grandes centrales no aportan NADA exclusivo.** Disco 15 (Ø8,4 m, cota 8,5), disco 1
  (Ø8,0 m, cota 5,3), disco 16, disco 2 y disco 32: **0 m² de sombra exclusiva**. Están apilados sobre
  otros discos: su sombra ya la daba alguien.
- **Los que trabajan son los pequeños periféricos a cota baja:** discos 53, 56 y 54 (Ø3,6 m, cota 4,5)
  aportan 65 m² exclusivos cada uno, y el disco 14 llega a 98 m².

**Interpretación.** La eficiencia climática de un disco no depende de su tamaño sino de **estar solo**.
El racimo denso de C2 es, climáticamente, redundante. No se mueve nada: sólo se identifica, como pedía el encargo.

---

## 6 · TEMPERATURA DE SUPERFICIE Y EL HALLAZGO DEL DOSEL

**Criterio.** Nada de convertir temperatura del aire en temperatura de superficie. Balance de energía por celda.

**Resultado.** Granito al sol **54,7 °C** con un aire de 34,7 °C (+20 K). Bajo la propuesta, **47,2 °C**.

**El dato más importante de la auditoría no está en el suelo sino en el dosel.** La cara inferior de la
hoja-canopy, resuelta como elemento delgado con convección por las dos caras:

| | temperatura |
|---|---|
| Con la lámina de microalgas evaporando (D15) | **33,8 °C** — por debajo del aire |
| La misma hoja, **seca** | **45,5 °C** |

**Interpretación.** Esos **11,7 K** los recibe directamente el cuerpo de quien está debajo. La lámina de
agua de la decisión D15 no es un recurso paisajístico: es lo que convierte la sombra en **sombra fresca** en
lugar de una plancha radiante suspendida a cinco metros. Si esa lámina se seca —y el capítulo de agua muestra
que pierde el 37 % de su calado al día— **el dosel deja de funcionar como refugio y empieza a funcionar como
radiador**.

---

## 7 · MRT — y una cola positiva que no se puede ocultar

**Resultado.** MRT media 64,5 → **53,7 °C** (**−10,8 K**); −27,6 K en las zonas de refugio; máximo −38,7 K.

**Hallazgo incómodo, verificado antes de publicarlo.** En el **46 % de las celdas la MRT SUBE** en el estado
B, hasta +8,5 K. Se investigó porque el punto 36 del encargo obliga a hacerlo. **No es un error de cálculo:**
son celdas que conservan el sol (τ media 0,84) pero han **perdido vista de cielo frío** (SVF de 0,97 a 0,78).
Pierden capacidad de radiar hacia arriba y a cambio ven la cara inferior de estructuras. Es el mecanismo
clásico de atrapamiento radiante urbano.

**Consecuencia de proyecto:** una estructura que reduce el factor de visión de cielo **sin llegar a dar
sombra** empeora las cosas. Ocurre en los bordes de los racimos y bajo la trama de cables y redes.

---

## 8 · AGUA — separando lo que enfría de lo que decora

**Criterio del encargo (punto 14): no sobrevalorar.** Se separan cinco efectos y se dice cuál es cuál.

**Resultado.** 1.900 m² de lámina, **1.722 L/h evaporados, 1.157 kW latentes, 20,7 m³/día.**

Pero el reparto lo cambia todo:

| | potencia latente | efecto real |
|---|---|---|
| **En altura** (láminas de microalgas + balsas) | **943 kW (82 %)** | enfría **la hoja**, no el aire. Efecto **RADIANTE** sobre el peatón: los 11,7 K del capítulo 6. Real e importante. |
| **A nivel de suelo** (splash + estanques) | **214 kW (18 %)** | efecto de **contacto y borde**. |
| **Sobre la temperatura del AIRE de la plaza** | — | **≈1,0 K** contando también el menor calor sensible del pavimento. |

**Interpretación honesta.** Los estanques son, climáticamente, **sobre todo paisaje**: enfrían su propio
borde y poco más (el splash pad sólo mejora 1,8 K de UTCI pese al agua, porque está mayoritariamente al sol).
Decir que «el agua del proyecto mueve 1.157 kW» sería cierto y engañoso a la vez: el 82 % de esa potencia
está trabajando cinco metros por encima de la cabeza de la gente. Trabaja **bien** —es lo que mantiene fría
la hoja— pero no es enfriamiento del aire.

**Cierre de masa (chequeo exigido).** 20,7 m³/día frente a **99,8 m³** almacenados en los depósitos de
+10,50 → **4,8 días de autonomía** sin reposición. La lámina de microalgas pierde **11,1 mm/día = 37 % de su
calado diario**. Registrado como CL-005: es un requisito de instalación, no un defecto geométrico, pero
**condiciona el funcionamiento climático del dosel**.

---

## 9 · NEBULIZACIÓN — la única palanca sobre el aire

**Criterio.** Prohibido asumir «−5 °C». Cálculo en tres pasos, cada uno auditable.

1. **Límite físico:** depresión de bulbo húmedo, CALCULADA con psicrometría real → 17,8 K (E2), **22,2 K (E3)**.
2. **Eficiencia de saturación al aire libre:** HIPÓTESIS declarada η = 0,20 / **0,35** / 0,50.
3. **Cierre por balance de masa** del aire tratado; se toma **el menor** de los dos.

**Resultado nominal (42 boquillas × 5 L/h):** 210 L/h · **141 kW** · **hasta −6,2 K de aire local**, sobre
2.054 m² de cobertura efectiva. **ΔUTCI adicional −0,74 K de media** y **−3,1 K bajo la nube**.

**La nube no es un círculo.** Con 1,0 m/s a nivel peatonal y una velocidad de sedimentación de 0,30 m/s, la
gota recorre **13,4 m** antes de evaporarse: la mancha se alarga a favor del SO dominante. El mapa lo
representa así, no con círculos perfectos.

**Interpretación.** Es el único sistema del proyecto que baja la temperatura del **aire**, y funciona
precisamente porque Madrid es seco. Su margen de mejora es el mayor de todo el proyecto: pasar de η 0,35 a
0,50, o de 5 a 8 L/h por boquilla, es una decisión de instalación, no de geometría.

---

## 10 · VEGETACIÓN

67 árboles, 1.114 m² de proyección de copa, τ de copa **0,20** (Beer-Lambert, k = 0,40 m⁻¹). Transpiración
**284 L/h · 190 kW**. Sombrea menos que el dosel artificial (τ 0,12) pero lo hace **enfriándose a sí mismo**
en vez de calentarse. **Resultado conservador**: no se contabiliza la transpiración del huerto, las
tropicales, la vegetación baja, las colgantes ni las trepadoras por falta de superficie foliar fiable.

---

## 11 · UTCI Y CONFORT

| Escenario 16:00 | Ta | UTCI A | UTCI B | Δ |
|---|---|---|---|---|
| E1 verano normal | 29,2 °C | 34,6 | 31,6 | **−3,00 K** |
| E2 tarde calurosa | 34,7 °C | 39,9 | 37,3 | **−2,60 K** |
| E3 ola de calor | 40,1 °C | 44,6 | 42,5 | **−2,05 K** |
| E4 = E2 + nebulización | 34,7 °C | 39,9 | 36,6 | **−3,34 K** |

**Separación exigida por el punto 24, cumplida:** el UTCI base está calculado con el **polinomio oficial de
Bröde et al. (2012)** vía `pythermalcomfort` 4.4.0 — no con una aproximación propia. El efecto de la
nebulización **no se descuenta sobre el índice**: se introduce modificando Ta y HR locales por saturación
adiabática (física cerrada) y se vuelve a evaluar el polinomio.

**Interpretación, sin maquillar.** La MRT baja 10,8 K y el UTCI sólo 2,6 K. No es contradicción: el UTCI
integra aire, radiación, viento y humedad, y **el aire pesa más**. Y el efecto **decrece** al subir la
temperatura. Una tarde de 34,7 °C no se convierte en una de 30 °C sombreándola.

---

## 12 · CINTA +6,00 — medida, no supuesta

**Criterio del encargo (punto 28): no asumir que por estar entre vegetación es confortable.**

**Resultado.** Sólo el **21 % del desarrollo está en sombra**. MRT **57,7 °C** frente a 53,7 °C de la plaza
que sobrevuela. UTCI **38,2** frente a 37,3. El viento ayuda (2,45 m/s frente a 1,00 m/s) pero no compensa.

**Interpretación.** **La cinta es más cálida que la plaza que atraviesa.** Va a +6,00, es decir **por encima**
de la capa baja del dosel (discos a 4,2–5,6) y sólo por debajo de la alta: en la mayor parte de su recorrido
está al descubierto. Se suma a lo que ya dijo 03B.5 sobre sus escaleras: el recorrido elevado es, hoy, el
elemento más débil del proyecto.

---

## 13 · INVIERNO

**Resultado.** 21 de diciembre: 2,34 → **1,21 kWh/m²·día**. El dosel retiene el **48 %** de la radiación de
invierno.

**Interpretación.** No es menor. El dosel **no es estacional**: la membrana tensada y la lámina de microalgas
son fijas, a diferencia de un arbolado caduco. La misma pieza que protege en agosto sombrea en diciembre, en
una plaza que en invierno es un lugar de estancia al sol. Registrado como CL-001; **no se corrige**.

---

## 14 · CHEQUEOS FÍSICOS (punto 36)

| Check | Resultado |
|---|---|
| ¿Reducción de Ta del aire de 15 K? | **NO.** 1,02 K. Pasa. |
| ¿Pavimento sombreado más caliente que el soleado? | No. Pero Ts_B > Ts_A en el 52,6 % de celdas → **investigado: atrapamiento radiante real**, se conserva como hallazgo. |
| ¿El agua evapora más de lo disponible? | Comprobado el cierre: 4,8 días de autonomía. **Se registra CL-005.** |
| ¿UTCI mejora donde la MRT empeora? | 1.905 celdas. Coherente (compensación convectiva) pero **anotado**. |
| ¿Membrana translúcida con sombra de opaca? | **ERA CIERTO.** Corregido, ver abajo. |

---

## 15 · ERRORES Y RECTIFICACIONES

Cuatro errores metodológicos reales, los cuatro conservados en el registro forense porque **tres de ellos
habrían cambiado las conclusiones**:

1. **EVT-000025 — la lámina de microalgas anulaba el parámetro `tau_canopy`.** Las partes de la hoja-canopy
   viven en 4 capas distintas; clasificando por capa, el agua interior la hacía opaca y la hipótesis
   declarada **nunca llegaba a aplicarse**. Rectificado clasificando por **bloque** (`LEAF_*`).
2. **EVT-000026 — el SVF contaba como cielo los rayos que atraviesan el dosel.** Un rayo que cruza una hoja
   translúcida transmite sol pero **no ve el cielo frío** en el infrarrojo. El SVF del estado B estaba
   sobreestimado (0,61–0,67 en vez de 0,46–0,49): **el error favorecía a la propuesta**. Rectificado
   descomponiendo el hemisferio en fracciones cielo/dosel/opaco/vegetal, cada una emitiendo a **su**
   temperatura calculada por balance.
3. **EVT-000027 — la métrica de disco era una tautología** (ver capítulo 5).
4. **EVT-000028 — el umbral del índice de refugio era inalcanzable.** Se exigía UTCI_B < 32 °C con un aire de
   34,7 °C: imposible por construcción, no por comportamiento del proyecto. Daba 188 m² de refugio (1,7 %).
   Sustituido por el **salto de categoría de la escala oficial UTCI**, que no es un umbral inventado.
   Resultado corregido: **4.010 m² (36,4 %)**.
5. **EVT-000029 — falló el propio registrador forense** (un `%` literal interpretado como especificador de
   formato). Se conserva la cadena completa ERROR → DIAGNOSIS → RECTIFICATION → NEW_RUN, y se comprobó que
   no se perdió ningún evento.

---

## 16 · LO QUE NO SE HA HECHO

- **Viento: PENDIENTE CFD.** Perfil logarítmico con z₀ = 0,30 m para llevar el viento de 10 m a nivel
  peatonal. Suficiente para deriva de niebla y convección; **insuficiente** para canalizaciones y remolinos.
- **Sin isla de calor urbana** (limitación de la fuente, declarada).
- **Caudal y eficiencia de nebulización, y calados de balsas y láminas: HIPÓTESIS.** El modelo 03B fija
  posiciones y cotas, no caudales ni profundidades.
- **No se ha corregido nada.** 6 incidencias climáticas registradas con posición, magnitud, causa, severidad
  y estrategias posibles.

---

## RESPUESTA FINAL

**¿Es esto un refugio climático?** Sí, en 4.010 m² de los 11.020 del ámbito, y de forma espectacular en los
viveros de C3 (−7,0 K de UTCI), el huerto de C1 (−5,6 K) y el interior de los racimos de dosel (−6,0 K):
ahí el punto **cambia de categoría de estrés térmico**, que es la definición no arbitraria de refugio.

**No lo es** en los corredores por los que camina la gente (−1,1 K), ni sobre la cinta elevada, que resulta
**más cálida** que la plaza. Y **4.884 m² siguen en estrés térmico muy fuerte**.

**Lo que de verdad enfría** no es el agua de los estanques —que es sobre todo paisaje— sino dos cosas: la
**sombra del dosel** y, dentro de ella, la **lámina de microalgas que mantiene la hoja a 33,8 °C en vez de a
45,5 °C**. La nebulización es la única pieza que toca la temperatura del aire, y es la que más margen de
mejora conserva.

**STOP. No se ejecuta E03 ni se corrige nada sin tu revisión.**
