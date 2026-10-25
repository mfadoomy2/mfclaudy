# FASE 01 — RESUMEN Y PENDIENTES
## REFUGIO CLIMÁTICO · PUERTA DEL SOL · MADRID
07-2026 (auditoría 2026-08-07) · Fase 01 COMPLETADA · **el trabajo se detiene aquí hasta revisión**

---

## 1. Qué se ha encontrado
- El proyecto vive íntegro en `MONTESERIN IA\MONTESERIN IA\MUTACIONES (DIBUJO + IA)\DIBUJO3 (REFUGIO CLIMATICO)\`: dibujo matriz `00_DIBUJO 03.jpg` (07-2026), serie HR01–HR14 (1 cenital arquitectónica + 12 variantes de maqueta + 2 aéreas implantadas) y 46 imágenes de proceso en `IN PROGRESS REFUGIO\` (2 cenitales clave, 1 sección de sistema, láminas técnicas anotadas, ~20 perspectivas con el Sol real verificable, detalles).
- **No existe ningún archivo CAD/vector/3D/texto del Refugio**: toda la Fase 01 se ha reconstruido desde imágenes.
- Carpetas hermanas (DIBUJO1/2/4/5, OTROS, COREA, FUTURE, AMBIENTACIONES): otros proyectos del mismo universo; ~10 archivos útiles como referencia de lenguaje (índice en `00_AUDITORIA\referencias_clasificadas\`).
- `Maqueta\` (raíz): flujo ACTIVO de reconstrucción Rhino de la escultura-reloj — independiente, no tocado (decisión D11).

## 2. Qué se ha reconstruido
| Entregable | Archivo | Estado |
|---|---|---|
| Auditoría y lectura | `00_AUDITORIA\00_AUDITORIA_Y_LECTURA_DEL_PROYECTO.md` + `01_LECTURA_ESPACIAL.md` + índice de 75 referencias clasificadas A–D | ✔ |
| Contexto real | OSM proyectado a métrico local (604 edificios + relations, 365 calles, 11 bocas de metro, 139 árboles, monumentos, Casa de Correos exacta) | ✔ G1 |
| **Planta maestra 2D** | `01_BASE_GEOMETRICA\planta_maestra\geometria_maestra.json` (FUENTE DE VERDAD, 1 u = 1 m) + `planta_maestra.svg` (8 capas-familia) + generador `master_geometry.py` | ✔ |
| Validación | 3 imágenes (`validacion_A/B/C`) + `VALIDACION.md` + métricas (banda Correos 14,8 m · Mariblanca 9,2 m · Carlos III 9,1 m) | ✔ |
| **Modelo 3D esquemático** | `modelo_3d\refugio_fase01.obj/.mtl` (14 grupos-familia, 25 k vértices, Z arriba, LOD 100–200) + `geometria_3d.json` + `axon_preview.png` | ✔ |
| **Manual gráfico** | `02_SISTEMA_GRAFICO\02_MANUAL_GRAFICO_REFUGIO_CLIMATICO.pdf` (10 págs.) + fuente editable HTML + `paleta.json` + `simbolos.svg` + `templates\lamina_A1.svg` | ✔ |
| **P01 Planta General** | `03_DOCUMENTOS_PILOTO\P01_PLANTA_GENERAL\P01_PLANTA_GENERAL_500.svg/.pdf` (A1, 1:500) + generador | ✔ |
| **P02 Axonometría Maestra** | `03_DOCUMENTOS_PILOTO\P02_AXONOMETRIA_MAESTRA\P02_AXONOMETRIA_MAESTRA.svg/.pdf` (A1, militar 32°) + generador | ✔ |
| Previews | `04_PREVIEWS\` (planta, modelo 3D, P01, P02) | ✔ |
| Logs | `05_LOG\decisiones.md` (13 decisiones) + `incertidumbres.md` (17 abiertas) | ✔ |

## 3. El proyecto, entendido
Cadena de **tres clústeres de loops** (C1 gran óvalo O · C2 anillo doble central · C3 este fragmentado) cosidos por una **cinta-recorrido** continua de 5–6 bucles, sobre el cuerpo central de la plaza real: banda libre de 15 m ante la Casa de Correos, monumentos y cruces históricos como claros, arbolado OSM conservado. Tres estratos: **suelo público continuo / dosel de agua-sombra +5–10 m / infraestructura +10–12 m**. El agua desciende por gravedad: depósitos rosas → balsas de microalgas → riego, nebulización y lámina jugable. Trenes de cápsulas neumáticas en los bordes O y SE.

## 4. Nivel de confianza
- **G1** (confirmado): topología de 3 clústeres + cinta, anillo doble C2, trenes de cápsulas O/SE, estratos verticales, implantación con banda libre y claros, contexto OSM.
- **G2**: trazado sintetizado de la cinta, lazos menores, balsas y estanques, racimos, jardineras, mástiles, posición Carlos III / Oso y Madroño.
- **G3**: LAB, cúpula, depósitos, splash, red hidráulica, discos individuales, árboles nuevos.
- **G4/reserva**: instalaciones (bombeo, drenaje, sensores, eléctrico) — categorías reservadas sin geometría.

## 5. Dudas que conviene revisar manualmente (las 5 que más pesan)
1. Orden de clústeres: se adoptó el del dibujo matriz (gran anillo al O); 0F53E6F0 está en espejo — ver `decisiones.md#D3` y validación B. **Confirmar que es la intención.**
2. Trazado de la cinta-recorrido (síntesis G2): revisar sus 6 bucles sobre la planta.
3. Posiciones G3 (LAB, cúpula, depósitos, splash).
4. Posición exacta post-2023 de Carlos III (afecta al claro central).
5. Densidad del dosel (17 % dibujado vs ~30 % aparente en renders): decidir si se densifica ya o se deja al dimensionado climático.

## 6. Qué falta / recomendaciones antes de Fase 02
- **Topografía y subsuelo**: plano municipal de la reforma 2023 (cotas, registros) y geometría de los vestíbulos de Metro/Cercanías bajo la plaza (crítico para cargas y anclajes).
- **Alturas reales del perímetro** (LiDAR/catastro) para sombras arrojadas fiables.
- **Clima horario** (AEMET Retiro/Barajas o EPW Madrid) para radiación, UTCI y balance de agua mensual.
- Decidir densidad objetivo de sombra y consolidar D7 (cinta única vs pasarela+carril).
- Si se desea, importar `refugio_fase01.obj` en Rhino y reconstruir los loops como NURBS sobre las elipses del JSON (los parámetros exactos están en `geometria_maestra.json`).

## 7. Criterio de éxito — cumplido
Sabemos exactamente qué proyecto estamos dibujando; hay una planta maestra fiable y validada sobre el Sol real; la espacialidad tridimensional está modelada y comprobada; y existe un lenguaje gráfico cerrado (manual + paleta + símbolos + retícula) del que ya han salido dos láminas piloto coherentes entre sí.

**FASE 01 TERMINADA. No se inicia la documentación técnica: Fase 02 (Atlas Técnico) espera revisión y nuevo prompt.**
