# URBAN_INTEGRATION_REPORT — FASE 03B.7 · v003 → v004

## Conflicto A · El proyecto penetraba edificación existente

**Medición inicial (v003 horneada, `URBAN_CONFLICTS_v003.json`):** 439 mallas hasta **10.1 m**
dentro de El Corte Inglés (edif. 133); 173 elementos sobre la Estación de Cercanías (edif. 106,
un edificio real de 20×7 m que v003 trataba como un punto); árboles dentro de edificación;
franjas E/N invadidas en las manzanas 110/117/124/131.

**Causa raíz:** ninguna regla del generador conocía los polígonos de edificio. No era un error
de un elemento: era una CATEGORÍA ausente del sistema de reglas.

**Solución v004 — el borde construido entra en la regla generadora (no parches):**
- `EDGE_GUARD`: 33 manzanas + kioscos (derivados por regla: área<80 m² en ámbito) + Estación,
  con márgenes por familia y CONCIENCIA DE ALTURA (la Estación ~6 m y los kioscos ~3.6 m solo
  bloquean lo que vuela por debajo de su cota real).
- Los **loops se recortan contra fachada** (clip↔suavizado iterado, margen 3.25). El arco de
  C1-L1 aplanado contra ECI no es un corte: es el **pórtico-galería**, y el tren T-O se regenera
  sobre él (la regla produce arquitectura, no ausencia).
- La **cinta se proyecta con empuje hacia la plaza** (candidatos en todas las aristas; el empuje
  por arista-más-cercana falla en vértices cóncavos). Eje final a **+3.05 m** de ECI con radio
  mínimo **4.75 m** (el clip dejaba un quiebro de 0.1 m; se pule sin perder holgura).
- **Anclajes de escaleras/ascensores validados con la huella real transformada** del bloque
  (las rejillas de sondas fallaban con el espejo s=−1) y deslizamiento acotado sin wrap.
- Guardas por familia (discos = r+0.85 con z de cota−1.5, mástiles 3.2 = alcance de brazo,
  árboles = **alcance real del bloque v2** medido de sus vértices, depósitos r+1.0, etc.).

**Verificación final (independiente, módulo A12 de la auditoría + `invest_urbano.py v004`):**
**CERO penetraciones en los 79 edificios del ámbito**, con la escena completamente detallada.

## Conflicto B · Metro / Cercanías / estancos: abrazo, no exclusión

- **Atrio de la Estación**: anillos de pavimento radial (7/9/11 m) en la boca, **belvedere** de
  anchura variable de la cinta sobre la cabeza este (la cinta pasa en cóncavo por el norte y se
  ensancha como balcón de llegada), señalética (tótems), zona de espera.
- **Dosel abierto sobre la Estación**: colgantes y redes se recortan sobre su volumen real.
- **Media luna de Carmen**: banco en arco (r 8.2, 200–340°) que abraza la boca de Carmen.
- **Aprons** en los tres estancos (109/110/111): banda de pavimento perimetral enrasada.
- Los kioscos existentes reciben **cornisa y banda de rótulo** (gálibo ≥3.0) como contexto.
- Ejes declarados **re-proyectados fuera del polígono real** de la Estación (densificados a ≤2 m
  y validando todas las aristas — la cuerda entre vértices desviados cortaba la esquina).

## Regla CR-2 generalizada (descubierta en la reauditoría)

Los márgenes de seguridad de 0.5–0.8 m contra fachada **fabricaban ranuras-trampa de ~0.5 m**
(intransitables pero aparentemente pasables). Doctrina aplicada por regla (`snap_facade`):
un elemento lineal contra fachada queda **CERRADO** (borde a ~2 cm) **o ABIERTO** (≥1.5 m),
nunca en el rango trampa. Aplica a jardineras, bancos y balsas; la jardinera cierra también
contra el tiesto del mástil. Fragmentos residuales (<2.4 m jardinera / <1.8 m banco) se eliminan.

## Estado

Conflictos A y B **resueltos por regla generadora** y verificados por auditoría independiente.
Reauditoría completa v004: **0 RED / 28 YELLOW / 20 GREEN** (las YELLOW son la misma clase
documentada con la que se cerró v003: divergencias de doctrina declarada, contactos vegetales
blandos, visuales del reloj). Detalle en `AUDIT_V004_MASTER.pdf` e `ISSUES_REGISTER`.
