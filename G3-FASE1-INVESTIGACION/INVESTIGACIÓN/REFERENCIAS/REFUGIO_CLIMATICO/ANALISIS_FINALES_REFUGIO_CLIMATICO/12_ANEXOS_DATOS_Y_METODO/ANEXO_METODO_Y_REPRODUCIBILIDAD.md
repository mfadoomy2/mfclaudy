# ANEXO · MÉTODO Y REPRODUCIBILIDAD

Fase final de análisis · baseline **v006 build 12** (2026-08-13) · congelada en
`00_SISTEMA_Y_FUENTES/BASELINE_SNAPSHOT.json` (29 archivos, SHA-256).

## 1 · Cadena de reproducción

```text
geometria_maestra_v006.json  (congelado, hash en snapshot)
        │
        ▼
build_all_03b9.py + detailing_03b9.py     → escena determinista (15.197 mallas)
        │
        ├── _reaudit9/audit_run.py        → rásters 0,25 m + módulos A0-A12 (0 RED)
        ├── _reclima9/vox_prep + clima_*  → vóxel 0,5 m + k_veg por especie + UTCI
        │
        ▼
ANALISIS_FINALES_REFUGIO_CLIMATICO/*/_scripts/*_engine.py
        │        (cada motor cachea sus stats en B_DATOS/*.json + CSV)
        ▼
*_docs.py / *_sintesis.py                 → PDFs vía refugio_editorial.py
        │        (Doc.metric() registra cada cifra publicada)
        ▼
00_SISTEMA_Y_FUENTES/FINAL_METRICS_REGISTRY.csv   (48 métricas, 0 conflictos)
```

Cualquier cifra del paquete se regenera ejecutando el script de su columna `script`
en `ANALYSIS_MASTER_REGISTER.csv` sobre la baseline congelada. Los renders se
regeneran con `09_RENDERS_Y_REPRESENTACION/_pipeline/render_driver.py` (reanudable).

## 2 · Diccionario de datos (B_DATOS por tema)

| Archivo | Contenido | Productor |
|---|---|---|
| `01_CLIMA/B_DATOS/cli_stats.json` | estadísticas por escenario/hora/estado, deltas, cola positiva con atribución, sombra/invierno, sensibilidades (viento, k_veg, canopy seco, sin agua) | `cli_engine.py` |
| `01_CLIMA/B_DATOS/zonas_programa.csv` | confort por programa (9 zonas: sombra/MRT/UTCI/refugio) | passthrough `zonas.json` |
| `01_CLIMA/B_DATOS/cinta_estaciones.csv` | 186 estaciones de la cinta (sombra, UTCI, viento por cota) | passthrough `cinta.json` |
| `02_MOVILIDAD/B_DATOS/mob_stats.json` | distancia geodésica a accesos, PMR N−1, LOS por escenarios, red | `mob_engine.py` |
| `02_MOVILIDAD/B_DATOS/dist_accesos.npy` | ráster 0,25 m de distancia a la salida más próxima | `mob_engine.py` |
| `04_AGUA/B_DATOS/agu_stats.json` | balance día punta/medio, hidrozonas, biodiversidad, eficiencia agua×clima | `agu_engine.py` |
| `05_CONSTRUCCION/B_DATOS/tec_stats.json` | inventario por familia + acceso A9 + matriz de mantenimiento | `tec_engine.py` |
| `05_CONSTRUCCION/B_DATOS/matriz_mantenimiento.csv` | componente→función→acceso→frecuencia→riesgo | `tec_engine.py` |
| `06_USO_SOCIAL/B_DATOS/soc_stats.json` | IPE (fórmula+pesos+sensibilidad), personas-hora LOW/BASE/HIGH | `soc_engine.py` |
| `06_USO_SOCIAL/B_DATOS/ipe.npy` | ráster 0,5 m del índice de potencial de estancia | `soc_engine.py` |
| `07_ECONOMIA/B_DATOS/eco_stats.json` | CAPEX/OPEX/comercio LOW-BASE-HIGH + fondo de reposición | `eco_engine.py` |
| `07_ECONOMIA/B_DATOS/fuentes_externas.csv` | F-01..F-06 con URL/institución/fecha/licencia/resolución | `eco_engine.py` |
| `08_PATRIMONIO/B_DATOS/pat_stats.json` | visibilidad por superficie y ponderada por uso (vis×IPE) | `pat_engine.py` |
| `10_SINTESIS/B_DATOS/kpis.json` | 7 indicadores cruzados + detalle de cobertura real por eje | `s05_kpis.py` |

## 3 · Niveles de conocimiento (§5)

- **A · MEDIDO/CALCULADO** — reproducible desde geometría o dato congelado.
- **B · INFERIDO** — modelo declarado sobre datos A (p. ej. Penman, IPE, volumen de control).
- **C · HIPÓTESIS/ESCENARIO** — plausible, pendiente de dato externo o piloto (afluencias, CAPEX, comercio, viento).

Cada PDF lleva el chip de su nivel; el registro de métricas lleva la columna `estado`.
**Regla dura: ningún C se cita como hecho en ningún documento del paquete.**

## 4 · Decisiones de método que conviene conocer

1. **La auditoría manda sobre el generador**: la escena se reconstruye interceptando el
   generador (no se leen los .3dm), y los conflictos se atribuyen por ráster de causa.
2. **El clima separa visual de físico**: el vóxel no muestrea hojas; cada especie entra
   con k_veg=0,5·LAI/3 (Beer–Lambert volumétrico), arbolado OSM por ancla (Platanus).
3. **Los ejes/corredores son abstracciones declaradas** del máster v002: dos rozan
   huellas OSM (documentado en URB-02 y en la genealogía).
4. **Viento idéntico en A y B** (limitación declarada, acotada en CLI-08 con ±25/50 %).
5. **El error se publica**: DISCOVERIES_REGISTER.md contiene los intentos de refutación;
   `_FORENSIC_PROCESS` conserva los 240+ eventos, incluidos los 15 errores instructivos.

## 5 · Software y versiones

Python 3.12 · numpy/scipy/matplotlib (PDFs vectoriales, Georgia embebida) · PyMuPDF 1.28
(QC/contactos) · pythermalcomfort (UTCI) · rhino3dm 8.32 (maestros) · trimesh 5.0 (assets
CC0/CC-BY) · Blender 5.0.1 Cycles/OptiX (campaña visual, RTX 5070 Ti) · flog.py (forense).
