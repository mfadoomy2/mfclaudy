# ASSET_MANIFEST 03D — lo que la vía B (D5/V-Ray) debe aportar sobre v003

## 1 · Vegetación (roles E02 canónicos → assets hi-poly)
Las POSICIONES son las de v003/E03 (deterministas, ya validadas contra obstáculos). Requisitos
funcionales fijados por el proyecto; las especies concretas las decide el autor — se apuntan
SUGERENCIAS compatibles con Madrid y con las ventanas de invierno (caduco donde toca):
| Rol (bloque) | Requisito | Sugerencia (NO vinculante) |
|---|---|---|
| VEG2_ARBOL_A/B (sombra, base copa ≥2.55) | caduco, porte 5-6.5 m | Celtis australis · Melia azedarach |
| VEG2_ARBOL_EX (existente, 7 m) | perenne/mixto conforme al arbolado real | Platanus x hispanica del entorno |
| VEG2_TROPICAL (alocasia) | palas grandes, 14+ segmentos, SSS foliar | Alocasia macrorrhiza (maceta) |
| VEG2_TREPADORA | hélice en mástil + derrame | Wisteria / Parthenocissus |
| VEG2_BAJA | matas 0.3-0.5 + gramíneas | Stipa tenuissima + salvias |
| VEG2_HUERTO | bancal 2.6 m con tutores | tomatera/judía + aromáticas |
| VEG2_ACUATICA | carrizos + nenúfares | Typha minima + Nymphaea |
| VEG2_COLGANTE | guías 1.3-2.3 m descolgando | Rhipsalis/pothos exterior estival |

## 2 · Personas fotográficas
`PEOPLE_PLACEMENT_03D.csv`: **38 posiciones exactas** (x, y, z_base, pose estimada) validadas contra
2.145 obstáculos v003. Reparto por programa: splash (niños jugando), huerto (cuclillas), bancos
(sentados), corredores/cinta (andando), cúpula/viveros/claros. Verano Madrid, sin multitud.

## 3 · Efectos de agua y niebla
`EFFECTS_03D.csv`: 42 boquillas de suelo + 8 de barandilla + 3 columnas de vapor + splash (10
chorros) + 2 rebosaderos + recirculación. En definitivo: niebla volumétrica real (anisotropía
hacia el sol), caustics en splash, gotas en primer plano si la cámara lo pide (H3).

## 4 · Contexto y monumento
- **Casa de Correos**: fachada con huecos reales, dos tonos ladrillo/piedra, torre+reloj emisivo
  legible (H4). Fuente: fotografía propia + cartografía municipal.
- **Carlos III**: modelo del monumento real (fotogrametría o asset); posición v003 (−28,−14) con
  certeza G2+ **pendiente de verificación municipal** — ajustar solo con plano oficial, nunca borrar.
- **Manzanas del entorno**: volumetría OSM v003 + materiales de revoco/granito por calle; basta
  reconocibilidad, no detalle ventana a ventana (salvo fondos de H1/H4/H7).
- **Granito Puerta del Sol**: escaneo/textura real con despiece 5.4 m (mapas E01 como guía).

## 5 · Cámaras y luces
`gh_scripts_named_views_03d.py` crea las 7 vistas nombradas en Rhino (lente desde fov vertical).
Sol PSA real (`SUN_03D.json`): mediodía 69.48°/165.65° · tarde 45.30°/257.85°. AgX/filmic
equivalente, exposición según brief §2.
