# DISCOVERIES_REGISTER — hallazgos del DISCOVERY PASS (§21-§22)

Fase final · baseline v006 build 12 · 2026-08-13.
Cada hallazgo sigue el método: OBSERVACIÓN → HIPÓTESIS → PRUEBA → RESULTADO → CONFIANZA → CONSECUENCIA.
Los que pudieron falsarse, se intentaron falsar.

---

## D-001 · La cola positiva crece con el calor — y su mecanismo es "cielo perdido sin sombra a cambio"
- **Observación:** las celdas donde la propuesta EMPEORA el UTCI (>+0,5 K) crecen 55 → 755 → 1.175 m² en E1→E2→E3.
- **Datos:** u_E*_16_A/B.npy, f_E2_16_*_svf/tau.npy (3.021 celdas de cola en E2).
- **Hipótesis:** pierden factor de cielo (más onda larga de estructuras calientes) sin ganar sombra.
- **Prueba:** Δsvf y Δtau medios por grupo. Cola: Δsvf −0,53, Δtau −0,01. Celdas que mejoran: Δsvf −0,63 CON Δtau −0,75. Resto: −0,13 / −0,01.
- **Resultado:** firma del mecanismo confirmada; la correlación puntual dU~dsvf a Δtau≈0 es débil (+0,24) por confusores — la evidencia fuerte es la de grupos.
- **Confianza:** ALTA (A sobre datos; mecanismo B).
- **Consecuencia:** regla de diseño «sombra o cielo, nunca media medida»: donde no se pueda sombrear, despejar. Ajuste fino local post-piloto.

## D-002 · La sombra del refugio es estructural, no vegetal
- **Observación:** intuición previa: "la vegetación da la sombra". Sensibilidad LAI ±30 % → fracción de sombra 42,4/43,2/43,4 %.
- **Prueba:** re-trazado de transmitancia con k_veg ×0,7/×1,3 (3 posiciones solares 15-jul).
- **Resultado:** ±1 punto porcentual. La vegetación aporta latente (286 kW), superficies y experiencia — no el parasol.
- **Confianza:** ALTA (B).
- **Consecuencia:** una sequía degrada el confort fino, no el refugio. La narrativa municipal no debe vender la vegetación como sombra.

## D-003 · Confort y contemplación compiten: el precio patrimonial se paga en las zonas de estancia
- **Observación:** visibilidad del reloj 41,5 % por superficie, pero 33,6 % ponderada por uso y 25,5 % desde estancia alta.
- **Prueba:** vis × IPE sobre 2.455 puntos (a7_views × soc IPE). Intento de refutación: ¿es artefacto de los pesos del IPE? Jaccard ≥0,74 con pesos ±50 % — no lo es.
- **Resultado:** el dosel que fabrica el confort tapa el reloj; quedan 896 m² de "miradores" (confort + vista).
- **Confianza:** ALTA (A/B).
- **Consecuencia:** cartografiar y PROTEGER los miradores en ejecución; orientar 2-3 bancos a corredores visuales (mejora documentada, no implementada).

## D-004 · La estancia sigue al confort — medido, no deseado
- **Observación/Prueba:** el 90,7 % de las celdas IPE≥0,6 cae dentro de la clase REFUGIO EFECTIVO.
- **Confianza:** ALTA (B — el IPE es modelo).
- **Consecuencia:** la inversión social y la climática son LA MISMA inversión: no hay que elegir.

## D-005 · El invierno paga −40 %, pero el coste está gobernado
- **Observación:** radiación 21-dic 2,30 → 1,29 kWh/m²·día (−40,3 %).
- **Prueba:** radwin_A/B por celda; 5.690 m² (58 % del pisable) conservan ≥50 % de su sol invernal.
- **Confianza:** ALTA (A).
- **Consecuencia:** el trade-off verano/invierno es un juicio político con números encima de la mesa; la geometría ya lo mitiga (claro central + hojas donde el verano mata).

## D-006 · El OPEX del refugio es mano de obra, no recurso
- **Observación:** agua 9 k€/año frente a jardinería 90 + limpieza/membrana 110 k€/año.
- **Confianza:** MEDIA (B/C — partidas por analogía).
- **Consecuencia:** la sostenibilidad económica se juega en el contrato de conservación, no en la factura del Canal.

## D-007 · La cinta no protege a sus usuarios: protege a los de abajo
- **Observación:** 22,6 % de sombra propia, UTCI medio 38,0 °C a cota +6; su sombra proyectada sí computa abajo.
- **Confianza:** ALTA (A).
- **Consecuencia:** comunicar la cinta como mirador en movimiento; sombra ligera en tramos sur = mejora documentada (§54).

## D-008 · El refugio rinde más cuanto peor es el día — y su cola también crece
- **Observación:** ΔUTCI −2,8/−2,5/−2,0 K en E1/E2/E3 con refugio útil creciente por clases; cola positiva 55→1.175 m².
- **Confianza:** ALTA (A).
- **Consecuencia:** doble filo del calor extremo: el proyecto es más necesario Y más imperfecto en ola de calor. El plan de monitorización debe medir AMBOS lados.

## D-009 · El sistema degrada bien: ningún fallo devuelve la plaza al estado A
- **Prueba:** composición de fallos (CLI-10): sin agua, sin niebla, canopy seco, LAI −30 %, E3.
- **Resultado:** el peor caso combinado conserva ~2/3 del beneficio UTCI; la sombra estructural nunca se apaga.
- **Confianza:** MEDIA-ALTA (B).
- **Consecuencia:** argumento de resiliencia central para el dossier municipal.

## D-010 · El punto ciego del mantenimiento: BOMBA-1
- **Observación:** 159/160 puntos A9 con acceso; BOMBA-1 (−70,0 · 22,0) con holgura 0,0 m.
- **Confianza:** ALTA (A).
- **Consecuencia:** corrección trivial en ejecución (desplazar 1,5 m o registro en murete). Prioridad ALTA por servir la recirculación oeste.

## D-011 · La equidad del nivel +6 pende de tres máquinas
- **Prueba:** rodeo PMR máximo 174 m con 3 ascensores; 286 m en el peor N−1 (proyección de anclas sobre la cinta).
- **Confianza:** ALTA (A).
- **Consecuencia:** SLA <48 h en contrato; estudio de 4º aparato en ejecución.

## D-012 · El viento es la incertidumbre metodológica dominante — y está acotada
- **Observación:** el modelo usa el mismo viento en A y B (limitación declarada, no error).
- **Prueba:** UTCI-B con viento −25/−50 % → +0,36/+0,55 K.
- **Resultado:** incluso la cota dura deja el neto en −1,95 K. CFD o anemometría del piloto lo cierra.
- **Confianza:** la sensibilidad es C; la conclusión "no invalida el neto" es B.

## D-013 · La niebla es el agua más rentable — pero solo cuando el aire tiene sed
- **Prueba:** 9 escenarios caudal×clima: 3,5 K psicrométricos en seco, 0,13 K aplicados en húmedo; 2,5 L/día por m² de refugio añadido (mejor ratio del sistema).
- **Confianza:** MEDIA (B).
- **Consecuencia:** activación por depresión psicrométrica, nunca por calendario.

## D-014 · El retorno se mide en €/persona-hora — y depende del uso, no del clima
- **Prueba:** (CAPEX + 25 años OPEX) / (p·h 25 años) = 1,1 – 4,9 – 29 €/p·h en HIGH/BASE/LOW.
- **Confianza:** C (escenario) — y así se publica.
- **Consecuencia:** regla de decisión propuesta: piloto ≥60 % del uso BASE → despliegue opera <8 €/p·h.

## D-015 · El 85 % del calor residual vive sobre los ejes de tránsito — por diseño
- **Observación:** 4.356 de 5.150 m² de hotspots supervivientes están a <8 m de un eje declarado; el mayor (2.548 m²) A 1 METRO del eje mayor.
- **Hipótesis:** la regla de auditoría A1 (corredores despejados, filtro 2,05 m del generador) expulsó el dosel de los ejes — y con él, su sombra.
- **Prueba:** distancia de cada CL-HOT a la polilínea de eje más próxima (15/15 medidos). Intento de refutación: ¿los hotspots son simplemente "todo lo abierto"? No: hay claros no-eje (CL-HOT-001, a 26 m) pero suman solo el 15 % del área caliente.
- **Resultado:** confirmado. Dos reglas del propio proyecto (paso libre vs sombra) COLISIONAN y la colisión estaba invisible hasta cruzar los datos.
- **Confianza:** ALTA (A).
- **Consecuencia:** la mejora de mayor palanca del proyecto: **sombra ALTA sobre los ejes** (hojas a >3 m de gálibo no violan A1 ni el filtro de corredor). Ataca el 85 % del calor residual con cero conflicto normativo interno. DOCUMENTADA — no implementada (§54: sin modificaciones geométricas tras el cierre).

---

*Todas las cifras de este registro proceden de los motores de la fase final y son reproducibles
desde la baseline congelada (BASELINE_SNAPSHOT.json). Los D con nivel C no se citan como hechos
en ningún documento de la familia.*
