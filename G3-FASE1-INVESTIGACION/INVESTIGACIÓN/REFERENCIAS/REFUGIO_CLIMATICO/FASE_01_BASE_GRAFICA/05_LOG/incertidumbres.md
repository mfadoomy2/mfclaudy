# INCERTIDUMBRES ABIERTAS — FASE 01
Lo que NO sabemos con certeza, clasificado. Nada de esto se ha convertido silenciosamente en geometría "real".

## Geometría de la propuesta
1. **Trazado exacto de la cinta-recorrido** — cada cenital lo resuelve con variaciones; el trazado modelado es una síntesis G2. Los bucles (5–6) y su continuidad O-E sí son constantes.
2. **Nº y diámetro de los loops secundarios de C2** — el nudo central varía entre 2 y 4 anillos según referencia; modelado: anillo doble + lazo SW (G1/G2).
3. **Posición en el Sol real de:** LAB 02, cúpula geodésica, depósitos elevados, splash pad, racimos menores (todo G3).
4. **Dualidad pasarela/carril logístico** — ver decisiones D7.
5. **Cotas exactas del dosel** — rango 5–10 m consistente, pero el escalonamiento disco a disco es inferido (aleatorio determinista en el modelo).
6. **Densidad de sombra necesaria** — 17 % actual vs 30-35 % aparente en renders; dimensionar con radiación/UTCI en Fase 02.

## Contexto
7. **Posición exacta de Carlos III post-2023** — estimada (−28, −14) G2; verificar con plano municipal de la reforma.
8. **Oso y el Madroño** — (+80, +22) G2 (no aparece como nodo etiquetado en el volcado OSM usado).
9. **Alturas de la edificación perimetral** — OSM `building:levels` incompleto; el 3D usa 18 m por defecto (20 m Casa de Correos). Suficiente LOD100, insuficiente para sombras arrojadas de Fase 02: conseguir LiDAR/catastro.
10. **Marquesinas de Cercanías y elementos de la reforma 2023** — presentes en OSM como polígonos sin etiqueta clara; dibujados como contexto genérico.
11. **Subsuelo (vestíbulos de Metro/Cercanías bajo la plaza)** — sin datos en Fase 01; CRÍTICO para cargas sobre losa y anclajes de mástiles en Fase 02.

## Referencias
12. **0F53E6F0 estira la plaza** ~20–30 % hacia el este y está en espejo E-O (ver VALIDACION.md): útil para lógica de implantación, no para métrica.
13. **Discrepancia material** bambú/acero/cobre/cromo entre generaciones de render (D4).
14. **Rotulo "SOLARIS"** (1C334300): posible nombre del proyecto en alguna iteración; sin confirmar.

## Técnicas
15. **El OBJ de contexto** usa triangulación en abanico: en huellas cóncavas las tapas de cubierta presentan artefactos (las paredes son correctas). Al importar en Rhino, considerar regenerar tapas o ignorarlas.
16. **CMYK de paleta.json** es conversión directa: ajustar con perfil ICC en preimpresión.
17. **Tipografías**: Bahnschrift/Consolas son de Windows; para intercambio usar las equivalencias libres (Archivo/Inter/IBM Plex Mono) declaradas en el manual.
