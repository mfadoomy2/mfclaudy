# E03_EXECUTION_PLAN — ATMÓSFERA, AGUA VIVA, POBLACIÓN Y CÁMARAS HERO
## Preparado 2026-08-07 · ACTUALIZADO A v003 el 2026-08-11 (FASE 03B.6) · NADA ejecutado aún
Geometría base: **v003** (`FASE_03B6_RESOLUCION/`): `SOL_FULL_SCENE_v002.3dm` + visor
`FASE_03B6_RESOLUCION/_viewer/scene_full.js`. Todo lo atmosférico vive en una capa separada
(`scene_extra.js`): los .3dm NO se tocan. Parámetros: `atmos_config.json` (actualizado).

### 0-bis · CAMBIOS v002→v003 QUE AFECTAN A E03
- **Posiciones deterministas** (E03-2): leer `geometria_maestra_v003.json`, NO v002 (eje re-trazado
  por el sur de la estatua, montera 44.2, E-3 en (10.4,20.4), NEB re-situados, viveros en el istmo).
- **Elementos nuevos que salen en cámara**: escaleras reales STAIR_SB (madera+acero, zanca cerrada),
  3 ascensores-cápsula LIFT_TOWER (fuste translúcido + cabina rosa — protagonista de H5), estatua de
  Carlos III (bronce/granito, entra en H4 y H7), barandilla de cinta a 3 niveles, 8 nebulizadores de
  barandilla (añadir su micro-niebla a §2 a cota +7.3), registros técnicos y recirculación (rosa
  técnico), canaleta enrasada en cruces.
- **H5 reanclada** al eje construido v003 (el suavizado movió la traza ~1.1 m): ahora recorre el
  tablero hacia el ascensor C2-norte (ver `atmos_config.json`).
- **Refino §7.4 (colgantes +15 %) YA CONSTRUIDO en v003** — eliminar del backlog de refinos.
- **Refino §7.5 (montante intermedio) YA CONSTRUIDO en v003** (travesaño 0.55 + rodapié 0.10).
- **Goteo de embudos** (§3): los 3 discos que atravesaban el tablero están ahora a +8.30 (rol
  sombra-cinta); los 4 discos sombra-corredor a +5.0 son los mejores candidatos a goteo visible.
- **Población** (§5): validar contra obstáculos v003 (corredores nuevos, respeto de estatua r=8,
  huellas de escaleras/ascensores/registros).

---

## 0 · ORDEN EXACTO DE TRABAJO
| Paso | Qué | Ejecuta | Valida |
|---|---|---|---|
| E03-0 | Recalibración visual: releer 12CA810C (niebla), 6BB98FC3 (mangueras), FBDF10B9 (splash), 24D82F58 (riego), 29A08040 (vapor), 2187306B (luz) | Read directo | criterios §8 fijados contra ellas |
| E03-1 | Texturas de efecto (`tex_mist.py`): sprite radial de niebla, corona de chapoteo, gota — a data-URL `tex_data2.js` | script | sprite legible sobre negro y sobre blanco |
| E03-2 | `scene_extra_builder.py` → `scene_extra.js`: niebla + agua viva + población (posiciones DETERMINISTAS desde geometria_maestra_v002 + atmos_config) | script | recuento y bbox por capa impresos |
| E03-3 | `viewer_e03.html` (= e01 + capa extra + presets de luz + THREE.Sprite billboards + param `luz=`) | copia+parche | test 1 vista (V13) mediodía |
| E03-4 | Refinos selectivos §7 | parches acotados | diff visual antes/después |
| E03-5 | Tanda hero: 7 cámaras × 2 luces (mediodía / tarde-control) 2560×1600 | render_e03.py | criterios §8 por vista |
| E03-6 | Iteración única de corrección (máx 1 ronda global, no por vista) | — | re-chequeo §8 |
| E03-7 | Hoja de contacto + comparativa E02→E03 + notas por cámara + REGISTRO_E03 + STOP | — | entrega §9 |

## 1 · CÁMARAS HERO (validadas + 2 nuevas)
| ID | Base | Encuadre | Luz protagonista | Por qué es hero |
|---|---|---|---|---|
| H1 | V05 banda Correos | igual (exp 1.1) | mediodía | alfombra de sombra + tren de cápsulas: EL argumento climático |
| H2 | V06 huerto C1 | igual | mediodía | capa productiva completa (huerto+colgantes+dosel) |
| H3 | V13 splash | igual | mediodía | agua viva total: chorros, corona, niños, niebla |
| H4 | V07 reloj | igual | **tarde 17:30** (contraluz cálido) | el proyecto contra el monumento; reloj legible |
| H5 | V19 sobre cinta | recuadre E02 | mediodía | pasear entre copas y colgantes |
| H6 | V10 cúpula | igual | mediodía (haz por óculo) | pérgola D03B-04 con programa vegetal |
| H7 | NUEVA aérea (0,−80,42)→(2,12,0) fov 55 | — | mediodía | equivalente 0F53E6F0: columnas de vapor sobre C1/C2/C3 |
Prohibido en E03 (sigue): nocturnos, lens flares, postpro fuerte.

## 2 · ESTRATEGIA DE NEBULIZACIÓN
- **Micro (peatonal)**: 4–7 sprites billboard por boquilla (42 puntos reales), Ø1.5–4 m, opacidad 0.08–0.18, textura radial suave, deriva determinista +X 0.3–0.8 m (brisa O), doble capa (fina arriba, densa 0–2.5 m).
- **Columnas (aérea H7)**: 3 columnas de 8 sprites apilados sobre C1(−52,10), C2(6,20), C3(58,10) hasta z 14–18, escala creciente, opacidad decreciente 0.16→0.04.
- **Regla anti-humo**: la niebla se lee EN CONTRALUZ y sobre fondos oscuros; sobre cielo claro debe casi desaparecer (blending normal, nunca aditivo puro; tinte #EAF6F2).
- Fog global se mantiene (lectura de profundidad); niebla local NUNCA gris plomo.

## 3 · ESTRATEGIA DE AGUA VIVA
- **Splash pad**: 10 chorros verticales (tubos alpha #DFF2EE 0.5–1.6 m con cabeza esférica) + corona-sprite en pie + 6 figuras jugando alrededor (§5); lámina ya reflectante.
- **Goteo de embudos**: en 12 discos seleccionados (los más bajos sobre estancias), línea dash vertical embudo→suelo + mini-corona; en el resto, solo bajante existente (no saturar).
- **Mangueras de riego**: 3 arcos paramétricos en el huerto C1 y 1 en viveros C3 (tubo fino rosa + arco de agua alpha), cf. 24D82F58/6BB98FC3.
- **Rebosadero de balsas**: 2 hilos de agua en B-C2a y B-C3a (línea alpha + brillo) — el ciclo del agua visible de arriba a abajo.
- Todo en `scene_extra.js` capa AGUA_VIVA; nada en los .3dm.

## 4 · ILUMINACIÓN
- **Principal — mediodía de verano Madrid** (periodo proyecto 15 jun–15 sep): sol alt ~68°, az S → dir three (20,−45,150); color #FFF3DC int 2.7; hemisferio 0.8; exposure 1.2 (H1 1.1). Sombra corta y densa = argumento del refugio.
- **Variante de control — tarde 17:30**: alt ~30°, az O-SO → (−120,−60,75); color #FFD9A8 int 2.2; hemisferio 0.6 cálido #F2E7D5; exposure 1.05; fog 60/300 #F4E9D8. Objetivo: probar que el refugio funciona sin sol cenital (sombras largas de mástiles, dosel encendido en contraluz).
- Preset por URL `&luz=mediodia|tarde` en viewer_e03; parámetros en atmos_config.json.

## 5 · POBLACIÓN / USO SOCIAL (bloques PERSON2_*, capa 16)
6 poses paramétricas low-poly (cilindro+esfera articulado, NADA hiperreal): de_pie, andando (zancada), sentado (0.45), en_cuclillas (huerto), niño_saltando (splash), pareja. Tinte de ropa por instancia ±val, gris cálido.
Distribución POR PROGRAMA (determinista, validada contra obstáculos con la rutina de E02):
splash 6–8 (niño_saltando/de_pie) · huerto 5 en_cuclillas/riego · bancos C1-C2 8 sentados ·
corredores 10–12 andando · cinta 5 andando · cúpula 3 · viveros 3 · claros 4. Total ≈ 45–50.
Criterio: densidad de plaza viva en agosto SIN multitud (1 persona ≥ 25 m² en claros).

## 6 · (reservado — sin cambios de geometría)

## 7 · REFINAMIENTOS SELECTIVOS (solo visor/bloques, acotados)
1. Alocasia: palas 8→14 segmentos + leve curvatura (block upgrade, mismo footprint).
2. Espuma de borde en splash: toro fino blanco alpha 0.3 en el perímetro.
3. H4/tarde: intensificar emisivo de la esfera del reloj ×0.35 para contraluz.
4. Colgantes: +15 % de longitud en los de la cinta (lectura desde H5).
5. Barandilla cinta: montante intermedio horizontal (línea, no malla) si H5 lo pide.
NO se toca: huerto (densidad queda como E02 salvo orden contraria), POD, estructura, granito.

## 8 · CRITERIOS CONCRETOS DE ACEPTACIÓN POR VISTA
Técnicos (automáticos): render OK >30 KB · sin z-fighting visible · niebla no eleva la luminancia media global >8 % vs E02 · en H3 los chorros ≥3 px de ancho a 1920 · en H1-mediodía, ROI de suelo bajo C2 con ≥30 % de píxeles bajo p35 de luminancia (sombra dappled real) · en H4-tarde, contraste torre/cielo ≥15 %.
De dirección (checklist manual por vista): ① ¿se reconoce el mismo refugio de los renders originales (comparación 1:1 con su referencia)? ② ¿la niebla parece agua pulverizada y no humo? ③ ¿el agua se lee viva a 25 m? ④ ¿la gente usa el espacio de forma creíble (nadie flotando/intersectando)? ⑤ ¿paleta E02 intacta (6 hex clave ±8 ΔHSL)? ⑥ ¿cielo visible y profundidad legible?
**Regla**: si una vista falla ≥2 criterios de dirección → se corrige en la iteración única E03-6; si tras ella sigue fallando, se entrega marcada NO-OK con diagnóstico (no se maquilla).

## 9 · OUTPUTS PREVISTOS
1. `tex_data2.js` + `scene_extra.js` + `viewer_e03.html` + `render_e03.py` (pipeline reproducible).
2. **14 vistas hero** (7 cámaras × mediodía/tarde) 2560×1600 en `hero_E03\`.
3. `HOJA_CONTACTO_E03.jpg` + `COMPARATIVA_E02_E03.jpg` (7 pares, luz principal).
4. `ATMOSFERA_NOTES.md`: por cámara — qué funciona / qué no / veredicto según §8.
5. `REGISTRO_E03.md` completo (incidencias y pruebas fallidas incluidas).
6. Handoff a máquina del autor: lista de equivalencias visor→D5/V-Ray (niebla volumétrica real, cáusticas, SSS de PODs) para el render definitivo post-E03.
7. STOP antes de cualquier "E04/hero final/nocturno".

## Preparado hoy (sin ejecutar)
`atmos_config.json` (todos los parámetros de §2-§5) · `atmos_prep.py` (generadores de sprite/extra/render con guardia: imprime aviso y sale si no se pasa --ejecutar-e03) · este plan · entrada en REGISTRO_E03.md.
