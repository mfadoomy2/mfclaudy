# REGISTRO — FASE 03C · E02 (biblioteca vegetal real)
2026-08-07 · geometría 03B congelada: la vegetación se INSTANCIA sobre el modelo aprobado, nada estructural se mueve.

## 1 · Correcciones de continuidad E01 aplicadas (los 6 ajustes aprobados)
1. MEMBRANA_VERDE → lima-alga cálido: base #D3DD7E, emisivo #C9D468 ×0.5 (menos teal/digital).
2. MADERA_LAMINADA → #B5A084 con variación de matiz ±7° y valor ±9% por instancia (menos miel plástica uniforme).
3. POD_TPU_ROSA → más lechoso: #F3C4D5, opacidad 0.74, roughness 0.36, emisivo blanco-rosado #F0D4DE ×0.22; arrugas y costuras se mantienen (D03B-05).
4. CÚPULA/ETFE → opacidad 0.30 + **retícula de membrana visible** (wireframe estructural superpuesto): deja de ser masa blanca.
5. CONTEXTO → Real Casa de Correos con lectura material mínima: cuerpo ladrillo #C4907A, torre #D9C4A4, esfera del reloj crema emisiva (legible a distancia). Resto del contexto sigue neutro.
6. GRANITO_SOL v2 → juntas con sombra+brillo, cortes transversales cada 5.4 m, contraste seco/húmedo ampliado (color −34 %, roughness 0.85→0.16), reflejo controlado (nunca espejo continuo).

## 2 · Biblioteca vegetal por roles (9 bloques VEG2, capa 15_VEGETATION_FULL apagable)
Ver `BIBLIOTECA_VEGETAL_E02.jpg`. Instancias con rotación/semilla determinista; el modelo sigue por bloques (37 definiciones, escena 6.672 mallas / 395k tris — manejable).
Plantación POR LÓGICA DE PROYECTO, no scatter:
- **Huerto** (filas con bancal, tutores y línea de goteo rosa): retícula en el interior de C1 bajo las balsas elevadas (cf. render 24D82F58), respetando corredores (chequeo near_corr) y claros de metro (r 6).
- **Tropicales húmedas**: núcleo denso de C2 (bajo discos de cota ≥6.2), interior de la cúpula-pérgola (nota E01 resuelta) y jardineras.
- **Baja de estancia**: cosida a los arcos de bancos (cada 3er punto).
- **Trepadoras**: 1 de cada 2 mástiles, con derrame en el brazo.
- **Colgantes**: bajo los aros de C1-L1/C2-L1/C3-L1 cada 40° y borde de la cinta cada ~14 m (lluvia verde del render 281A44BD).
- **Acuáticas + nenúfares**: 3 por estanque de microalgas.
- **Árboles**: multilobulados (A/B nuevos, EX existentes OSM) sustituyendo los lollipops.

## 3 · Qué aporta la vegetación a cada cámara (E01 → E02)
- **V07 reloj**: el eje gana ritmo verde vertical (trepadoras) y el fondo ya tiene la Casa de Correos en ladrillo con reloj legible; la vista deja de ser "estructura + suelo".
- **V06 bajo C1**: LA transformación — el huerto en filas convierte el interior de C1 en la capa productiva del render de referencia; colgantes desde la cinta; el dosel lima cálido filtra como vegetal, no como vidrio.
- **V13 splash**: matas bajas y acuáticas acercan el agua a escala de cuerpo; los árboles multilobulados dan horizonte vegetal al fondo.
- **V10 cúpula**: el interior ya tiene programa vegetal (tropicales bajo el óculo) y la retícula de membrana hace legible la pérgola como estructura ligera.
- **V19 sobre cinta**: se camina ENTRE copas y colgantes — la cinta por fin lee como paseo por el dosel; recuadre +2 m aplicado (el depósito ya no tapa).
- **V05 banda Correos**: la alfombra de sombra ahora es sombra de dosel + copas mezcladas; exposición 1.1 recupera el cielo.

## 4 · Proceso / incidencias
- Servidor del visor relanzado tras cierre de sesión (http 8123).
- Bloque nuevo VEG2 con guardia __main__ reutilizado para el tablero (renders aislados en modo material sin texturas → file:// válido).
- Fallo corregido: helper near_metro_pt inexistente en el pase de huerto → definido inline (r 6.0).
- Pendiente estético anotado para tu revisión: la densidad del huerto de C1 es alta (fiel a referencia, pero valida si quieres aclarar 1 de cada 3 filas); las palas de alocasia son low-poly evidentes en primer plano (suficiente E02; refinable en E03 si una cámara hero las acerca).

## 5 · Entrega
`BIBLIOTECA_VEGETAL_E02.jpg` · 6 vistas en `direccion_arte\` (E01 archivado en `direccion_arte_E01\`) ·
`COMPARATIVA_E01_E02.jpg` · modelo actualizado (`SOL_FULL_SCENE_v001.3dm` con capa VEG2; MASTER y ASSET_LIBRARY regenerados con los 9 bloques nuevos) · este registro.
**STOP: no se inicia E03 (atmósfera/agua viva/hero) sin tu OK.**
