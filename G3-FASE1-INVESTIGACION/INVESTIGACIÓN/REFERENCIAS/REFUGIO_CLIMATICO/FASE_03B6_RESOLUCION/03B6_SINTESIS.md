# FASE 03B.6 — SÍNTESIS FINAL (2026-08-11)

## CAMBIOS ESTRUCTURALES
1. **La cinta es un recorrido de verdad**: eje suavizado a r≥4.75 (tangente a las balsas), 6
   escaleras reales de 35 CH (0.171/0.29, meseta, doble pasamanos, zanca cerrada), **3
   ascensores-cápsula** en C1-O/C2-N/C3-E, barandilla de 3 niveles con huecos de embarque y 8
   nebulizadores propios. La escalera que bloqueaba Montera (V-020) reancló sola 2 m al este.
2. **conflict_guard**: ninguna familia se coloca ya sin chequear metro (base<+2.50), corredores,
   estatua, discos, cúpula, cinta, tuberías y mástiles **en su posición final**. 44 ajustes
   registrados uno a uno.
3. **Sombra con arbitraje**: **27 discos NUEVOS** (23 sombra-cinta +8.30 y 4 sombra-corredor +5.0)
   colocados por regla y filtrados por 9 conos visuales intencionados al reloj y 2 ventanas de
   invierno. Además, los **7 discos** que atravesaban el tablero suben a +8.30 (de colisión a
   función). Total con rol v003: **34** (27 nuevos + 7 re-cotados).
4. **Mantenimiento como sistema**: protocolo (A0/A1/A2) + plataformas y pates en depósitos,
   3 registros técnicos, recirculación por cluster, gotas a 3.05 m, viveros re-implantados en el
   istmo, puertas de servicio.
5. **Carlos III: presencia consolidada en v003** (DEC-0006): grada+pedestal+volumen ecuestre en
   (−28,−14) con respeto r=8; el eje mayor lo rodea por el sur. **Posición y dimensiones con
   certeza G2+ — pendientes de verificación contra plano municipal** (fuente actual: aérea
   canónica 0F53E6F0). No se borra nunca; solo se ajustará con la fuente oficial.
6. **Trenes con puertas por retirada** de cápsulas (nunca >3 seguidas), conservando las
   posiciones aprobadas — la regeneración uniforme violaba los recortes de metro de 03A y se
   descartó con evidencia.

## PROBLEMAS RESUELTOS
- Las **36 incidencias ROJAS** de 03B.5 → **0** (9 iteraciones REGENERAR→REAUDITAR, EVT-000064..101).
- Itinerarios: de 2/6 APTOS (Montera NO APTO, cinta NO APTO) a **6/6 APTOS + cinta APTO CON ASCENSOR**.
- Cercanías: de 5 invasores en banda a boca físicamente limpia (queda 1 elemento en Alcalá, YELLOW).
- Mantenimiento: de 56/133 componentes sin acceso a **1/160**.
- Colisiones no intencionadas: 120 → 25 (las 25 son roces leves YELLOW; contactos de diseño
  documentados como intencionados).
- V-019 (tubería en Preciados): canaleta enrasada. V-023 (bolsillo aislado): abierto. V-025/030/067
  (copas bajas): poda min 2.55. V-027 (respaldos): construidos. V-052 (reloj): red de conos
  intencionada protegida y documentada.

## MÉTRICAS BEFORE → AFTER (E2 tarde calurosa 16:00, mismos scripts, misma física)
| | v002 | v003 |
|---|---|---|
| Sombra crítica / exclusiva | 45.3 % / 40.0 % | **48.0 % / 42.5 %** |
| MRT media (dMRT vs sin proyecto) | 53.7 °C (−10.8) | **52.9 °C (−11.6)** |
| UTCI media / m² UTCI≥40 | 37.3 °C / 4460 m² | **37.1 °C / 4170 m²** |
| Refugio efectivo / beneficiada | 4010 m² / 47.4 % | **4318 m² / 50.5 %** |
| Cinta: sombra / MRT / UTCI | 21 % / 57.7 / 38.2 | **30 % / 54.2 / 37.4** |
| Hotspots | 24 uds / 4884 m² | **23 uds / 4629 m²** |
| Invierno (pérdida solar) | 48.2 % | **50.1 %** (−) |
| Agua total | 1722 L/h | 2034 L/h (−, con recirculación) |

## PROBLEMAS ABIERTOS (documentados, no ocultos)
- 26 YELLOW: roces leves de interpenetración, rangos del HEIGHT_SYSTEM v1 (superado por v2),
  visuales globales 35/38 % (arbitradas por conos), radio de cinta 4.8 < 8 aconsejable, 10 huecos
  de 0.5 m interiores a parterres (textura intencional), 1 elemento en banda de Alcalá.
- Invierno empeora 1.9 pts (precio de los 27 discos nuevos, acotado por las ventanas); mover a
  proyecto técnico si se quiere recuperar (lamas orientables o vaciado invernal ampliado).
- Banda de metro 5.5 m sigue **PROVISIONAL**; estatua pendiente de plano municipal preciso.
- Drenaje del tablero documentado (8 puntos bajos), no modelado.

## ESTADO PARA E03
Los cuatro maestros v003 están en disco y verificados; `E03_EXECUTION_PLAN.md` y
`atmos_config.json` actualizados a v003 (H5 reanclada al eje construido, elementos nuevos en la
lista de materialización); E03 **no ejecutada** conforme al mandato.

**READY FOR E03**
