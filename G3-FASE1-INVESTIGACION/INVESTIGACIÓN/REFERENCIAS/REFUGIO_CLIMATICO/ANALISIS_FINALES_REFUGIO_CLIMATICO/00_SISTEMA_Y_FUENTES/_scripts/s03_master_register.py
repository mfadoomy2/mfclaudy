# -*- coding: utf-8 -*-
"""FASE FINAL - S03: ANALYSIS_MASTER_REGISTER.csv

Catalogo maestro: analisis historicos minados (11 agentes, deduplicados por pregunta)
+ los analisis NUEVOS de la fase final (motores CLI/MOB/AGU/TEC/SOC/PAT). Que sabemos,
como lo sabemos y sobre que version lo sabemos.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..'))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
MONT = os.path.normpath(os.path.join(BASE, '..', '..'))
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402

with open(os.path.join(OUT, '_mining', 'mining_full.json'), encoding='utf-8') as f:
    mining = json.load(f)

# --- dedup por pregunta (las pasadas con 529 produjeron repeticiones)
vistos = {}
for k, v in mining.items():
    if not (isinstance(v, dict) and 'analyses' in v):
        continue
    for a in v['analyses']:
        key = a.get('pregunta', '').strip()[:160]
        if key and key not in vistos:
            vistos[key] = a
hist = list(vistos.values())

CAMPOS = ['id', 'origen', 'tema', 'pregunta', 'metodo', 'inputs', 'script', 'outputs',
          'unidad', 'version_geometrica', 'resolucion_espacial', 'resolucion_temporal',
          'fuente_externa', 'certeza', 'limitaciones', 'metricas_clave',
          'vigencia_v006', 'equivalente_v006']

# ids por tema para los historicos
cnt = {}
rows = []
for a in sorted(hist, key=lambda x: (x.get('tema', 'SYS'), x.get('version_geometrica', ''))):
    t = (a.get('tema') or 'SYS').split('/')[0][:3].upper()
    cnt[t] = cnt.get(t, 0) + 1
    rows.append(dict(id='%s-H%02d' % (t, cnt[t]), origen='HISTORICO',
                     **{k: (a.get(k) or '') for k in CAMPOS if k not in ('id', 'origen')}))

# --- los analisis nuevos de la fase final (registrados a mano: son nuestros)
NUEVOS = [
    ('CLI-01', 'CLI', 'Cuanta sombra util produce el refugio y que precio invernal paga',
     'cli_engine.py + cli_docs_a.py', '01_CLIMA_Y_CONFORT/CLI-01_SOMBRA.pdf', 'A'),
    ('CLI-02', 'CLI', 'Cuanta radiacion deja de recibir el suelo', 'cli_engine.py',
     '01_CLIMA_Y_CONFORT/CLI-02_RADIACION.pdf', 'A'),
    ('CLI-03', 'CLI', 'Cuanto baja la MRT y donde empeora (cola positiva con mecanismo probado)',
     'cli_engine.py', '01_CLIMA_Y_CONFORT/CLI-03_MRT.pdf', 'A'),
    ('CLI-04', 'CLI', 'Cuanto estres UTCI retira por escenario E1/E2/E3/E4',
     'cli_engine.py', '01_CLIMA_Y_CONFORT/CLI-04_UTCI.pdf', 'A'),
    ('CLI-05', 'CLI', 'Que puede y que no puede hacer la sombra sobre la temperatura del aire',
     'aire.json (volumen de control)', '01_CLIMA_Y_CONFORT/CLI-05_AIRE.pdf', 'B'),
    ('CLI-06', 'CLI', 'Que aporta la vegetacion al clima y sensibilidad LAI +-30%',
     'cli_engine.py/sens_kveg', '01_CLIMA_Y_CONFORT/CLI-06_VEGETACION.pdf', 'B'),
    ('CLI-07', 'CLI', 'Cuanto enfria cada termino de agua y a que coste hidrico',
     'agua.json + neb_escenarios.json', '01_CLIMA_Y_CONFORT/CLI-07_AGUA.pdf', 'B'),
    ('CLI-08', 'CLI', 'Sensibilidad del UTCI-B al abrigo de viento no resuelto (-25/-50%)',
     'cli_engine.py/sens_viento', '01_CLIMA_Y_CONFORT/CLI-08_VIENTO.pdf', 'C'),
    ('CLI-09', 'CLI', 'Confort por programa: 9 zonas + cinta + spots',
     'zonas/cinta/spots.json', '01_CLIMA_Y_CONFORT/CLI-09_CONFORT_POR_PROGRAMA.pdf', 'A'),
    ('CLI-10', 'CLI', 'Que beneficio sobrevive a cada modo de fallo',
     'cli_engine.py (composicion)', '01_CLIMA_Y_CONFORT/CLI-10_ESCENARIOS_DE_FALLO.pdf', 'B'),
    ('MOB-01', 'MOB', 'Anchuras, cuellos y fragmentacion de la red con el refugio',
     'a1_paths + mob_engine.py', '02_MOVILIDAD_Y_ACCESIBILIDAD/MOB-01_RED_PEATONAL.pdf', 'A'),
    ('MOB-02', 'MOB', 'Accesibilidad vertical PMR y fallo N-1 de ascensores',
     'mob_engine.py', '02_MOVILIDAD_Y_ACCESIBILIDAD/MOB-02_ACCESIBILIDAD_VERTICAL.pdf', 'A'),
    ('MOB-03', 'MOB', 'Distancia geodesica a salidas y LOS en 3 escenarios de afluencia',
     'mob_engine.py', '02_MOVILIDAD_Y_ACCESIBILIDAD/MOB-03_EVACUACION_Y_AFLUENCIA.pdf', 'A/C'),
    ('URB-01', 'URB', 'Holguras y bandas de respeto de cada acceso de Metro/Cercanias',
     'a6_metro.json', '03_CONTEXTO_URBANO_Y_TRANSPORTE/URB-01_METRO_Y_CERCANIAS.pdf', 'A'),
    ('URB-02', 'URB', 'Bordes, fachadas, servidumbres: dato oficial vs criterio',
     'a12 + contexto', '03_CONTEXTO_URBANO_Y_TRANSPORTE/URB-02_BORDES_Y_FACHADAS.pdf', 'A'),
    ('AGU-01', 'AGU', 'Balance hidrico dia punta/medio y autonomia ante corte',
     'agu_engine.py', '04_AGUA_ECOLOGIA_Y_VEGETACION/AGU-01_BALANCE_HIDRICO.pdf', 'B'),
    ('AGU-02', 'AGU', 'Comunidad vegetal, hidrozonas, estacionalidad y apuesta tropical',
     'BOTANICAL_MASTERPLAN + agu_engine.py', '04_AGUA_ECOLOGIA_Y_VEGETACION/AGU-02_ECOLOGIA_Y_VEGETACION.pdf', 'A/C'),
    ('AGU-03', 'AGU', 'Litros por unidad de beneficio de cada mecanismo climatico',
     'agu_engine.py/eficiencia', '04_AGUA_ECOLOGIA_Y_VEGETACION/AGU-03_AGUA_X_CLIMA.pdf', 'B'),
    ('TEC-01', 'TEC', 'Inventario real de la escena por familia constructiva',
     'tec_engine.py', '05_CONSTRUCCION_ESTRUCTURA_Y_MANTENIMIENTO/TEC-01_INVENTARIO_Y_FAMILIAS.pdf', 'A'),
    ('TEC-02', 'TEC', 'Matriz componente-funcion-acceso-frecuencia-riesgo (160 puntos A9)',
     'tec_engine.py + a9_maint', '05_CONSTRUCCION_ESTRUCTURA_Y_MANTENIMIENTO/TEC-02_MATRIZ_MANTENIMIENTO.pdf', 'B'),
    ('SOC-01', 'SOC', 'Indice de potencial de estancia explicito con sensibilidad de pesos',
     'soc_engine.py', '06_USO_SOCIAL_Y_EXPERIENCIA/SOC-01_POTENCIAL_DE_ESTANCIA.pdf', 'B'),
    ('SOC-02', 'SOC', 'Personas-hora protegidas/dia en LOW/BASE/HIGH',
     'soc_engine.py', '06_USO_SOCIAL_Y_EXPERIENCIA/SOC-02_PERSONAS_HORA_PROTEGIDAS.pdf', 'C'),
    ('PAT-01', 'PAT', 'Visibilidad de hitos por superficie y ponderada por uso + miradores',
     'pat_engine.py', '08_PATRIMONIO_VISUALES_Y_PAISAJE_URBANO/PAT-01_VISIBILIDAD_HITOS.pdf', 'A/B'),
]
for mid, tema, preg, script, out, cert in NUEVOS:
    rows.append(dict(id=mid, origen='FINAL', tema=tema, pregunta=preg, metodo='ver PDF',
                     inputs='v006 build 12', script=script, outputs=out, unidad='',
                     version_geometrica='v006', resolucion_espacial='0,25-0,5 m',
                     resolucion_temporal='ver PDF', fuente_externa='',
                     certeza=cert, limitaciones='declaradas en el PDF',
                     metricas_clave='ver FINAL_METRICS_REGISTRY.csv',
                     vigencia_v006='VIGENTE', equivalente_v006=''))

dst = os.path.join(OUT, 'ANALYSIS_MASTER_REGISTER.csv')
with open(dst, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=CAMPOS)
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, '') for k in CAMPOS})

resumen = dict(historicos=len(hist), nuevos=len(NUEVOS), total=len(rows),
               por_vigencia={})
for r in rows:
    v = r.get('vigencia_v006') or '?'
    resumen['por_vigencia'][v] = resumen['por_vigencia'].get(v, 0) + 1

flog.event(fase='FINAL', tipo_evento='master_register',
           objetivo='ANALYSIS_MASTER_REGISTER.csv: catalogo completo de analisis',
           resultado='%d historicos deduplicados + %d nuevos = %d filas; vigencia: %s'
                     % (len(hist), len(NUEVOS), len(rows),
                        json.dumps(resumen['por_vigencia'], ensure_ascii=False)))
print(json.dumps(resumen, ensure_ascii=False, indent=1))
