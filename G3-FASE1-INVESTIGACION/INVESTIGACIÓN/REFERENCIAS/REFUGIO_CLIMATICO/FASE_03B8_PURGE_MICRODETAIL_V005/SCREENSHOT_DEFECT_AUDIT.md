# SCREENSHOT_DEFECT_AUDIT — FASE 03B.8 · las capturas del autor como PRIMERA AUDITORÍA

Capturas en `_defect_screens/` (S01–S12, nombradas por hora). **Set válido de modelo: S04–S11.**
S01–S03 (visor de grafo documental) y S12 (página de un NAS) no son del modelo y quedan fuera.
Cada defecto lleva ID `D-xx`, clasificación y CAUSA RAÍZ en el generador. Los defectos que el
autor no señaló explícitamente pero yo detecto están marcados `[+]`.

---

## S06 · Escalera + rampa de acceso + cinta (vista alta)

| ID | Defecto | Clase | Causa raíz |
|----|---------|-------|-----------|
| D-01 | El desembarco rampa→escalera no conecta: la placa de la rampa y la meseta de la escalera se cruzan en diagonal sin junta ni continuidad | ERROR | dos familias (acceso Carmen / STAIR_SB) generadas por reglas independientes que "casualmente se tocan" |
| D-02 | Barandilla de la rampa muere en el aire a media bajada (sin montante final, sin retorno) | ERROR | barandilla por offset de curva sin lógica de terminación |
| D-03 | Línea-pelo diagonal cruzando de la rampa al poste (curva CBL desnuda, sin sección ni anclajes) | ERROR | cables como curvas `add_curve` sin geometría de tensor ni placas |
| D-04 | [+] Tiesto del mástil = "hélice" de 4-6 dardos triangulares; la rampa PASA A TRAVÉS del follaje | ERROR | mata foliar `_fan` de la 03B.7 (insuficiente) + sin guarda rampa-vegetación |
| D-05 | [+] Objetos cian "diamante" con palo rosa flotando sin identidad legible (¿boquilla? ¿luminaria?) | SOSPECHOSO | bloque NEB/colgante ambiguo — objeto genérico sin lógica física |
| D-06 | [+] Brazos en V de los soportes tocan el tubo de cinta tangencialmente sin nudo/placa | ERROR | soporte = 2 cilindros hasta la superficie, sin pieza de transferencia |
| D-07 | [+] Aro del registro de pavimento visible como anillo plano sin tapa modelada con relieve | SOSPECHOSO | PAV_REGISTRO 16 mm de relieve — casi invisible: falta marco/tapa real |
| D-08 | [+] Zanca inferior de la escalera: los peldaños vuelan sin zanca visible en el lado cercano | ERROR | STAIR_SB: zanca única + placas; falta zanca por cara exterior |

## S07 · TANK torus + fachada (el "donut rosa")

| ID | Defecto | Clase | Causa raíz |
|----|---------|-------|-----------|
| D-09 | El toro rosa no responde a ¿cómo se sujeta / dónde descarga?: cables negros lo ATRAVIESAN sin tocarlo, no hay poste visible, ni silla, ni racores | ERROR | TANK = torus sobre TKPOLE fino; los cables cercanos son de otro sistema y lo cruzan |
| D-10 | Tensores negros con quiebros que terminan en el aire junto a la fachada | ERROR | curvas de red/cable recortadas por el clip de fachada SIN reanclar |
| D-11 | Proximidad extrema del sistema a la fachada: tubo de loop casi tocando la esquina del edificio | ERROR (mandato §2) | margen loop 3.25 → "justo no colisiona" |
| D-12 | Tren de pods = acordeón de cápsulas interpenetradas | ERROR | paso del tren `w+0.25 = 3.65` < LONGITUD real del bloque POD_TRAIN (5.3 m) |
| D-13 | [+] Píldora blanca flotando en el aire junto al borde de fachada (resto huérfano) | ERROR | pieza residual de iteración (probable jamba/casetón desplazado) — purga |
| D-14 | [+] La membrana de la pérgola termina cortada contra la fachada sin borde construido | ERROR | clip de membrana sin cable de borde ni remate |
| D-15 | [+] Kingpost de discos atraviesa la membrana sin pieza de paso | SOSPECHOSO | kingpost añadido en 03B.7 sin nudo membrana-poste |

## S08 · Cinta pegada a la fachada de ECI (tramo largo)

| ID | Defecto | Clase | Causa raíz |
|----|---------|-------|-----------|
| D-16 | TODO el tramo va rozando la fachada: entre pasamanos y muro no cabe ni la vista. La fachada no respira | ERROR (mandato §2) | eje a 3.05 del muro con tablero de 2.5+: borde a ~1.6. Se exige ≈2.0 LIBRE continuo |
| D-17 | Filas de montantes duplicadas donde convergen los raíles del arco aplanado | ERROR | 4 offsets de barandilla (sideP/N/M/C) independientes que colapsan en curvas cerradas |
| D-18 | Rim de un disco terminando contra el edificio (aro cortado sin remate) | ERROR | disco empujado por guarda; aro del bloque no se recorta — queda tangente sin nudo |
| D-19 | [+] Cables de catenaria con quiebros angulosos sobre el tablero | SOSPECHOSO | polilíneas de 2 puntos sin flecha; leer como cable exige curva y anclas |
| D-20 | [+] Montantes sin pasamanos superior en un tramo del lado lejano | ERROR | tramos donde el offset del pasamanos se descartó pero los postes no |

## S09 · Escalera + ascensor + mástiles (vista cercana)

| ID | Defecto | Clase | Causa raíz |
|----|---------|-------|-----------|
| D-21 | El tiro superior ATRAVIESA un plano inclinado (placa del tiro inferior/lateral) — dos chapas cruzándose a media escalera | ERROR | STAIR_SB: faldón lateral = paralelogramo que no acompaña la quiebra de tiros |
| D-22 | Tercera placa inclinada FLOTANDO a la derecha con dos varillas clavadas en diagonal | ERROR | resto de generador (¿pasamanos de meseta desplazado?) — purga |
| D-23 | Pasamanos superior muere en el aire sobre el hueco; varilla horizontal suelta al lado | ERROR | terminación de barandilla inexistente |
| D-24 | Tubería rosa (MAIN) se HINCA en un tiesto de mástil y muere | ERROR | main recortada por guarda sin dispositivo terminal |
| D-25 | Poliedro magenta colgado de la main sin identidad | SOSPECHOSO | VEG2_COLGANTE colocado sobre la tubería — ni planta ni válvula |
| D-26 | 6+ tiestos-turbina idénticos clonados con la misma rotación | ERROR | mata `_fan` + colocación sin variación |
| D-27 | [+] Cabina del ascensor = esfera rosa mayor que la caja; sin puerta legible en este ángulo | SOSPECHOSO | LIFT_TOWER: cabina esférica genérica |
| D-28 | [+] Planta bajo el arranque de la escalera sin holgura (follaje contra zanca) | ERROR | sin guarda escalera-vegetación |
| D-29 | [+] Polilínea gris en L sobre el pavimento que termina en nada (línea de recirculación a ras) | ERROR | recirculación como tubo superficial sin registro/dispositivo en extremos |

## S10 · Tiesto del mástil a 50 cm (LA prueba vegetal)

| ID | Defecto | Clase | Causa raíz |
|----|---------|-------|-----------|
| D-30 | "Maceta con cuatro triángulos verdes": cilindro facetado sin borde, sin espesor, sin tierra; dardos planos como follaje | ERROR (mandato §7/§10) | `mast()` tiesto primitivo + `_fan` |
| D-31 | Anillo rosa (válvula de riego) FLOTANDO detrás del fuste sin tubo que la alimente | ERROR | válvula del §12 col colocada sin acometida |
| D-32 | Cable pasa por el encuadre sin origen ni destino visibles | ERROR | mismo D-03 |
| D-33 | [+] El fuste ATRAVIESA el tiesto sin collarín/rejilla ni separación tallo-borde | ERROR | mandato §10: resolver relación mástil-jardinera |

## S11 · Desembarco superior escalera↔cinta (belvedere)

| ID | Defecto | Clase | Causa raíz |
|----|---------|-------|-----------|
| D-34 | BOSQUE de montantes: tres+ filas paralelas de postes cruzándose en diagonal sobre el tablero | ERROR | mismos 4 offsets de barandilla + barandilla de hueco de escalera, sin resolver el nudo |
| D-35 | Z-fighting a franjas en las chapas del tablero (superficies coplanares) | ERROR | tablero var_strip + fascia/canaleta/juntas coplanares en el desembarco |
| D-36 | Varilla diagonal ATRAVIESA el tablero desde abajo y asoma por arriba | ERROR | brazo del trípode de soporte sin recorte contra el plano del tablero |
| D-37 | Cables cruzan la superficie de paso EN DIAGONAL a la altura de la rodilla | ERROR | tensores disco-cinta trazados sin respetar el volumen peatonal |
| D-38 | Cubo y píldora CIAN flotando junto a la barandilla | ERROR | escombros huérfanos (residuo de bloque) — purga |
| D-39 | Rebosadero del disco = muñón rosa cortado en el aire | ERROR | rebosadero §11 sin cadena de goteo ni destino |
| D-40 | Tiro inferior flotante: el extremo bajo del tramo no apoya en nada visible | ERROR | anclaje deslizado sin pie/dado de apoyo |
| D-41 | [+] Meseta con doble chapa a distinta z (borde doble visible) | ERROR | meseta del bloque + plataforma del desembarco duplicadas |

## S04–S05 · Aéreas (C1 y C3/Estación)

| ID | Defecto | Clase | Causa raíz |
|----|---------|-------|-----------|
| D-42 | Círculo negro de construcción dibujado en el suelo (r8 de respeto de la estatua) | ERROR | curva de análisis en capa visible 30_CURVES |
| D-43 | DOS toros-depósito ENTRELAZADOS como eslabones de cadena | ERROR | fila de tanques `cx + k·2.6` con radio de toro ~2 → paso < diámetro |
| D-44 | Toros flotando sin lectura de poste/apoyo desde el aire | ERROR | TKPOLE r0.18 invisible a esa distancia; sin silla/cuelgue creíble |
| D-45 | Cápsulas rosas "salchicha" sueltas por el suelo con un pincho | SOSPECHOSO | pods del tren dispersos tras las guardas — leen como residuos |
| D-46 | Membrana de la pérgola con bordes vivos sin cable de borde donde cruza loops | ERROR | mismo D-14 |
| D-47 | Mains magenta serpenteando A RAS de suelo por zonas de paso | SOSPECHOSO | mains a z 0.25-0.85 sin zanja/tapa: decidir enterrado+registros o bandeja |
| D-48 | [+] Escalera de contexto (¿boca Metro?) junto al loop con peldaños al aire | SOSPECHOSO | verificación de la pieza de contexto |

---

## SÍNTESIS — clases sistémicas (lo que de verdad hay que arreglar)

1. **TERMINACIONES** (D-02/03/10/19/23/24/29/31/32/39): ningún elemento lineal tiene lógica de
   final. → Regla global §4: tapa/placa/nudo/anclaje/dispositivo en TODO extremo.
2. **BARANDILLA** (D-17/20/34): el sistema por 4 offsets independientes es el origen de las
   marañas. → Familia única `rail_run()` con montantes, pasamanos, rodapié, remates y huecos.
3. **NUDO ESCALERA-CINTA** (D-01/21/22/34/35/36/40/41): reconstrucción completa como una pieza.
4. **VEGETACIÓN + MACETAS** (D-04/26/30/33): sustitución total (assets + procedural v3 + LOD).
5. **FACHADA** (D-11/16/18): retracción ~2 m libres continuos.
6. **TANQUES/PODS** (D-09/12/43/44/45): paso ≥ dimensión real + apoyo/suspensión legible.
7. **PURGA** (D-13/22/38/42 + escaneo automático): escombros y curvas de construcción, fuera.
8. **CABLES** (D-03/10/19/37): geometría real con flecha, y SIEMPRE de anclaje a anclaje, fuera
   del volumen peatonal.
9. **Z-FIGHTING/COPLANARIDAD** (D-35/41): separaciones mínimas y prioridad de chapa.
10. **HIDRÁULICA VISTA** (D-24/29/47): todo tramo visto acaba en dispositivo; el resto, enterrado
    con registro.

48 defectos catalogados (35 del autor + 13 adicionales `[+]`). Cámaras de S04–S11 reproducidas
en `beforeafter8.py` para el antes/después obligatorio (§25).
