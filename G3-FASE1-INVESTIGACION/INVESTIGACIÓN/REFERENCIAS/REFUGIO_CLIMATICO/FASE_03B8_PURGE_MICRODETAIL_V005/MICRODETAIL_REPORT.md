# MICRODETAIL_REPORT — FASE 03B.8

Métrica de esta fase (§18): **¿aguanta un primer plano?** — no el número de objetos.

## §2 Fachada: AIRE, no tangencia
Márgenes de dato v005: cinta 2.65→**3.80** (borde de tablero a ≈2.5 m libres), loop 3.25→**4.30**,
aéreo 0.5→1.2, suelo 0.8→1.0. Eje re-muestreado a paso 0.65 con filete puntual de esquinas
cóncavas (ECI y Estación). Verificado: **0 penetraciones** (sonda con nombres + barrido de 79
edificios sobre escena horneada).

## §5 Escalera↔pasarela: UNA pieza
`stair_switchback` v3: zancas-VIGA cajón continuas ambos tramos + vigas de borde de meseta,
dado de arranque, 2 pies de meseta con placa, poste de cabeza, pasarela con vigas de borde,
ménsulas al poste y junta cubrejuntas contra el tablero; **barandilla CONTINUA**
arranque→meseta→tramo B (polilínea única por lado con jog del pozo), montantes desde huella,
remate de arranque en gancho. El despiece del tablero (juntas) se INTERRUMPE en los desembarcos.

## §6 Barandilla v2
Tramos cerrados se cierran de verdad (sin costura); tramos abiertos: montante final + gancho
pasamanos→travesaño + pletina; fragmentos <1.6 m eliminados; 215 postes duplicados de v004 → 0.

## §11-§12 Canopy/tubos
Kingpost+tensores+manguitos+aro doble (03B.7) + rebosadero con boquilla terminal; discos a la
misma cota ya no solapan láminas (separación con orden fachada→disco↔disco→fachada);
cables = tubo con catenaria y anclaje en ambos extremos, nunca por el volumen peatonal.

## §13-§14 Pods / depósitos
Tren con paso = LONGITUD real de cápsula (v004 las interpenetraba: paso 3.65 vs cuerpo 5.3).
Tanque-toro: **trípode con horquillas** bajo el anillo + placas base, bajante central con
válvula y volante, toma, rebosadero, indicador de nivel, registro superior, plataforma+pates.
El donut ya responde: se sujeta (3 horquillas), descarga (bajante), y está para riego del cluster.

## §15 Ascensor
Umbral superior e inferior con rampa, vigas de apoyo de pasarela, jambas/dintel/botonera/casetón
(03B.7). Cabina esférica rosa se mantiene (identidad) — panelización fina → campaña de render.

## §16 Pavimento
Mains ENTERRADAS con línea de tapas cada 9 m; camas de plantación bajo toda planta exenta;
tapa/marco de registro sin coplanaridad; splash bajo placas; alcorques; juntas fuera de
desembarcos.

## Test de distancia (§19) e iteraciones (§21)
7 builds medidos con `purge_scan` + tomas `_qa/` en los nudos de las capturas del autor
(aérea/50m → 2m → 50cm). Ronda i1 detectó y corrigió: poste NEB en balsa, cantos de banco sin
testero, plantas sin cama, manguera vista. Comparativa de cámaras idénticas:
`03B8_SCREENSHOT_BEFORE_AFTER.pdf`.

## ABIERTO (honesto)
- 5 tropicales procedurales sobre jardineras elevadas clasificadas SOSPECHOSO (apoyo a validar).
- ~49 objetos con costuras de abanico >umbral en huerto procedural (invisibles; candidatos a
  limpieza de primitiva en la siguiente pasada).
- Árbol urbano: sigue procedural (no existe fotoescaneo CC0 digno); mejora candidata.
- Panelización fina de pods y clima re-calibrado (k_veg/LAI por especie nueva) → §23: tras
  esta fase de modelado, en la pasada climática siguiente.
