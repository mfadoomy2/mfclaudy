# REGISTRO — FASE 03C · E03 (atmósfera, agua viva, población, hero)

## 2026-08-07 — PREPARACIÓN (sin ejecución)
- E02 entregado y en revisión del autor; el autor ordena preparar E03 sin ejecutarla.
- Escrito `E03_EXECUTION_PLAN.md`: orden E03-0…E03-7, 7 cámaras hero (6 validadas + aérea H7 equivalente a 0F53E6F0), estrategia de niebla en dos escalas (micro-boquillas + columnas para la aérea, regla anti-humo), agua viva en 4 sistemas (chorros splash, goteo de embudos, mangueras de riego, rebosaderos de balsas), doble iluminación (mediodía principal / tarde 17:30 de control), población PERSON2 de ~45-50 en 6 poses repartida por programa con validación anti-colisión, 5 refinos selectivos acotados, criterios de aceptación medibles (automáticos + checklist de dirección con regla de iteración única), y 7 outputs.
- Escrito `atmos_config.json` (parámetros completos §2-§5 + cámaras + resolución) y `atmos_prep.py` con **guardia dura** (`--ejecutar-e03`): probado que sin el flag informa y sale sin generar nada.
- Frontera respetada: geometría congelada, ningún .3dm tocado, ninguna vista E03 producida, escena E02 intacta. Todo lo atmosférico irá a `scene_extra.js` (capa de visualización separada).
- Pendientes que E03 hereda de E02 (a decisión del autor al arrancar): densidad del huerto C1 (alta, fiel a referencia) y refino de alocasias (incluido como refino §7.1).

STOP — a la espera del OK para ejecutar E03 tras el reset.

## 2026-08-11 — EJECUCIÓN COMPLETA (orden del autor tras aprobar 03B.6; base = v003 CONGELADA)
- **Base geométrica**: escena v003 (`scene_v003.js`, copia de `FASE_03B6_RESOLUCION/_viewer/scene_full.js`);
  los .3dm no se tocaron. E03 hereda la cinta real (escaleras 35 CH + 3 ascensores + barandilla 3 niveles),
  Carlos III, registros, canaleta y los 27 discos nuevos con rol.
- **E03-0**: recalibración contra 12CA810C / 6BB98FC3 / FBDF10B9 / 24D82F58 / 29A08040 / 2187306B.
  Criterios fijados: niebla blanca legible solo en contraluz; coronas y agua rosa sobre granito espejado;
  vapor como velos ascendentes; mediodía duro con sombra corta; reloj siempre legible.
- **E03-1**: `tex_data2.js` (sprite radial de niebla + corona de chapoteo, data-URL, PIL).
- **E03-2**: `scene_extra.js` determinista (seed 1926): niebla micro en 42 boquillas de suelo v003 + 8 de
  barandilla de cinta + 3 columnas H7; agua viva (10 chorros + espuma §7.2 + 12 goteos de embudo + 3
  mangueras huerto + 1 viveros-istmo + 2 rebosaderos); 40 PERSON2 en 8 programas validadas contra 2.145
  bbox de obstáculos v003 (los peatones proxy v002 se ocultan). Un caminante anclado al tramo H5.
- **E03-3**: `viewer_e03.html` = visor E01/E02 + presets mediodía/tarde (atmos_config §4) + capa extra +
  Carlos III en bronce/granito + reloj emisivo +0.35 en tarde (§7.3).
- **E03-4 (refinos)**: §7.2 espuma ✓ · §7.3 reloj-tarde ✓ · §7.4 colgantes +15 % y §7.5 travesaño YA SON
  GEOMETRÍA v003 ✓ · **§7.1 alocasia 14-seg NO aplicado** (exigiría rehornear la escena congelada) → pasa
  al handoff (`HANDOFF_D5_VRAY.md`).
- **H5 reencuadrada con método**: 4 pruebas registradas; la posición del plan quedaba pegada al pretil y
  regalaba medio encuadre a la medianera. Definitiva: sobre el eje CONSTRUIDO (−12.8, 28.8, 7.55) → (10,
  26, 6.5) fov 63 — tablero en diagonal, escalera conmutada al fondo, discos sombra-cinta a +8.30, dosel
  de C2 a la derecha.
- **E03-5**: 14/14 renders 2560×1600 OK (7 cámaras × mediodía/tarde), `hero_E03\`.
- **Controles §8 (tanda 1, `_checks_e03.json`)**: 14/14 >30 KB · Δluminancia vs E02 máx +2.6 % (límite
  +8) · H1 ROI de sombra 32.2 % (≥30) · H4-tarde contraste torre/cielo 61.2 % (≥15) · chorros H3 24 px
  analíticos a 2560 (≥3 a 1920). **FALLOS: 0.**
- **E03-6 (única ronda global)**: diagnóstico de dirección — la niebla quedaba tímida en toda la tanda y
  las columnas de vapor de H7 (su razón de ser) casi invisibles, con 5+ pts de margen de luminancia.
  Corrección GLOBAL en `atmos_config.json` (micro: sprites 5-8, Ø2.2-5.5, op 0.12-0.26; columnas: 12
  sprites, z 15-19, op 0.26→0.08; barandilla: 5 sprites Ø1.6-3.2) y re-render completo. Sin retoques
  vista a vista.
- **Incidencias técnicas registradas**: `--screenshot` de Edge falla EN SILENCIO con rutas 8.3
  (`IRAXX_~1`) → rutas absolutas simples; servidor 8123 relanzado (el anterior murió con el reset).
- **Tanda 2 (tras la ronda global)**: 14/14 OK, checks automáticos FALLOS: 0. La niebla micro ya se lee
  (H1/H3/H5); H7 mejora (velos presentes) pero **las 3 columnas de vapor siguen sin leerse como columnas**:
  billboard+blending normal+tinte blanco sobre suelo claro es invisible por construcción — la misma regla
  anti-humo que protege las demás vistas. Falla 1 criterio de dirección (<2) → **H7 = OK con reserva
  técnica** y diagnóstico en `ATMOSFERA_NOTES.md` + fila en `HANDOFF_D5_VRAY.md` (volumétrica real).
  Ronda única consumida; no se maquilla.
- **E03-7 · PAQUETE ENTREGADO**: `hero_E03\` (14 vistas 2560×1600) · `HOJA_CONTACTO_E03.jpg` ·
  `COMPARATIVA_E02_E03.jpg` (6 pares E02→E03) · `ATMOSFERA_NOTES.md` (veredicto §8 por cámara: 13 OK /
  1 OK-con-reserva / 0 NO-OK) · `_checks_e03.json` · `HANDOFF_D5_VRAY.md` (equivalencias visor→definitivo,
  incl. §7.1 alocasias y columnas H7) · pipeline reproducible (`atmos_prep.py --ejecutar-e03`,
  `render_e03.py`, `checks_e03.py`, `boards_e03.py`, `viewer_e03.html`, `tex_data2.js`, `scene_extra.js`,
  `scene_v003.js`).
- Frontera respetada de principio a fin: **ningún .3dm tocado; geometría v003 congelada** (la capa E03
  vive en `scene_extra.js` y el visor); nada nocturno, sin lens flares, paleta E02 intacta.

STOP — E03 completa; a la espera de la revisión del autor antes de cualquier "E04 / hero final / nocturno".
