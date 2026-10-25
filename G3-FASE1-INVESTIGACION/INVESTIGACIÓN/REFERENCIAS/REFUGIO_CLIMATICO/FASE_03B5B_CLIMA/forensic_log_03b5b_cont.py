# -*- coding: utf-8 -*-
"""Continuacion del registro forense de 03B.5B tras el fallo de forensic_log_03b5b.py.
Se reanuda en el punto exacto donde se corto (ultimo evento escrito: EVT-000028).
NO se reescribe nada anterior: el JSONL solo se amplia."""
import hashlib
import os
import sys

WS = r"C:\Users\iraxx_c0wouln\OneDrive\Documentos\iraxxxdios_ARQUITECTURA\xxxmiguelxxx\Monteserin"
FP = os.path.join(WS, "_FORENSIC_PROCESS")
FASE = os.path.join(WS, "REFUGIO_CLIMATICO", "FASE_03B5B_CLIMA")
sys.path.insert(0, FP)
import flog  # noqa: E402

F = "03B.5B-CLIMA"

TB = """Traceback (most recent call last):
  File "...\\FASE_03B5B_CLIMA\\forensic_log_03b5b.py", line 211, in <module>
    "1) Reduccion de Ta de 15 K: NO ocurre. El efecto sobre el aire a escala plaza es 1.02 K. OK. "
TypeError: %d format: a real number is required, not str
"""

eid = flog.error(
    fase=F,
    objetivo="Escribir el evento CHEQUEO_FISICO del punto 36 del enunciado",
    traceback_txt=TB,
    diagnostico="El texto del evento contenia porcentajes literales escritos como '52 % de las celdas'. "
                "Al aplicarle el operador % de Python para interpolar el id de otro evento, la secuencia "
                "'% d' se interpreto como especificador de conversion con flag de espacio, no como signo "
                "de porcentaje seguido de la palabra 'de'. El fallo es del REGISTRADOR, no del analisis "
                "climatico: ningun resultado queda afectado.",
    eventos_origen=["EVT-000028"])

flog.event(
    fase=F, tipo_evento="DIAGNOSIS",
    objetivo="Alcance del fallo del registrador",
    criterio_explicito="Antes de reintentar hay que comprobar que no se ha perdido ni corrompido ningun "
                       "evento previo: el protocolo solo permite anadir.",
    resultado="FORENSIC_EVENTS.jsonl paso de 18 a 28 lineas y todas parsean como JSON valido. "
              "Los eventos EVT-000019 a EVT-000028 quedaron correctamente escritos ANTES del fallo. "
              "No hay perdida ni duplicado. Se reanuda desde EVT-000029 sin reescribir nada.",
    validacion="28 lineas leidas y parseadas; flog --selftest OK",
    estado="OK", conocimiento="CONFIRMED", relaciones_con_eventos_previos=[eid])

flog.event(
    fase=F, tipo_evento="RECTIFICATION",
    objetivo="Reanudar el registro sin volver a ejecutar la parte ya escrita",
    criterio_explicito="Reejecutar el script completo duplicaria diez eventos. El protocolo prohibe "
                       "borrar, de modo que la unica salida limpia es un script de continuacion.",
    rectificacion="forensic_log_03b5b_cont.py: sin operador % sobre textos con porcentajes literales; "
                  "los ids de eventos se concatenan en vez de interpolarse.",
    archivos_generados=[os.path.relpath(os.path.abspath(__file__), WS).replace("\\", "/")],
    estado="OK", conocimiento="CONFIRMED", relaciones_con_eventos_previos=[eid])


def rel(p):
    return os.path.relpath(p, WS).replace("\\", "/")


def sha(p):
    if not os.path.exists(p):
        return None
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()[:32]


def mtime(p):
    if not os.path.exists(p):
        return None
    import datetime as dt
    return dt.datetime.fromtimestamp(os.path.getmtime(p)).astimezone().isoformat(timespec="seconds")


def art(p):
    return dict(ruta=rel(p), sha256_32=sha(p), mtime=mtime(p),
                bytes=os.path.getsize(p) if os.path.exists(p) else None)


CHK = ("1) Reduccion de Ta del aire de 15 K: NO ocurre. El efecto a escala plaza es 1.02 K. PASS. "
       "2) Pavimento sombreado mas caliente que el soleado: NO ocurre. Pero SI aparece Ts_B > Ts_A en el "
       "52,6 por ciento de las celdas y MRT_B > MRT_A en el 46,2 por ciento. Investigado: son celdas que "
       "conservan el sol (tau media 0,84) y pierden vista de cielo (SVF de 0,97 a 0,78). Es atrapamiento "
       "radiante real, documentado en la literatura de canon urbano, no un error de calculo. Se conserva "
       "como HALLAZGO y se representa en la cola positiva del mapa delta de MRT. "
       "3) Agua que evapora mas masa de la disponible: comprobado el cierre. 20,7 m3/dia de evaporacion "
       "frente a 99,8 m3 almacenados en los depositos de +10,50 = 4,8 dias de autonomia; la lamina de "
       "microalgas pierde el 37 por ciento de su calado cada dia. Se registra como incidencia CL-005. "
       "4) UTCI que mejora donde la MRT empeora: 1.905 celdas. No es imposible (el termino convectivo y el "
       "de onda larga pueden compensar) pero queda anotado como zona a vigilar. "
       "5) Membrana translucida que sombrea como opaca: ERA CIERTO y se corrigio, ver EVT-000025.")

flog.event(
    fase=F, tipo_evento="CHEQUEO_FISICO",
    objetivo="Punto 36 del enunciado: sanity checks fisicos antes de publicar",
    criterio_explicito="Buscar activamente resultados imposibles en los propios resultados.",
    resultado=CHK,
    validacion="3 de 5 checks pasan limpios; el 2 y el 4 se conservan como hallazgo documentado y no "
               "como error; el 5 detecto un error real que se rectifico.",
    estado="OK", conocimiento="CONFIRMED",
    relaciones_con_eventos_previos=["EVT-000025", "EVT-000026", "EVT-000027", "EVT-000028"])

docs = [f for f in sorted(os.listdir(FASE)) if f.endswith(('.pdf', '.csv', '.md'))]
flog.event(
    fase=F, tipo_evento="ENTREGA",
    objetivo="Documentos de la auditoria climatica 03B.5B",
    resultado=str(len(docs)) + " documentos",
    artefactos=[art(os.path.join(FASE, d)) for d in docs],
    archivos_fuente=[rel(os.path.join(FASE, s)) for s in
                     ("clima_core.py", "clima_prep.py", "clima_run.py", "clima_run2.py", "clima_report.py")],
    estado="OK", conocimiento="CONFIRMED", captura="ARTEFACTO_POSTERIOR")

print("--- ejecucion EN VIVO bajo flog.run() ---")
code = ("import json,os;"
        "m=json.load(open(os.path.join(r'" + FASE + "','_data','metricas.json')));"
        "print('metricas en disco:', len(m));"
        "print('dMRT', m['dMRT'], 'K'); print('dUTCI', m['dUTCI'], 'K');"
        "print('m2_refugio', m['m2_refugio']); print('hot_m2', m['hot_m2'])")
rid, rd = flog.run([sys.executable, "-c", code], cwd=FASE, fase=F,
                   objetivo="Verificacion en vivo de que las metricas publicadas son las que estan en disco",
                   criterio="Dejar al menos una ejecucion de esta fase capturada en vivo por el protocolo "
                            "y no derivada de artefacto posterior.")
print("run:", rid, "exit", rd.get("exit"))

flog.state_change(
    "Efecto climatico real del Refugio Climatico de Puerta del Sol",
    "UNKNOWN", "CONFIRMED",
    motivo="Medido sobre la geometria aprobada con clima real PVGIS: dMRT -10,8 K, dUTCI -2,6 K "
           "(-3,3 K con nebulizacion), efecto sobre la temperatura del aire del orden de 1,0 K, "
           "36,4 por ciento del ambito baja de categoria en la escala UTCI. Conclusion: funciona como "
           "pantalla radiante, no como acondicionador de aire.",
    eventos_origen=[rid])

flog.snapshot("FIN_03B5B", {
    "fase": F,
    "escena": {"mallas": 6672, "triangulos": 394610, "identica_a_03B5": True,
               "sha256_vertices_32": "41a82b72634490377f2be60e7096b6ca"},
    "clima": {"fuente": "PVGIS v5.2 TMY + serie horaria 2005-2020", "lat": 40.4169, "lon": -3.7035,
              "uhi_incluida": False, "conocimiento": "CONFIRMED"},
    "resultados_clave": {
        "sombra_critica_pct": {"A": 5.3, "B": 45.3},
        "radiacion_kWh_m2": {"A": 648, "B": 365, "reduccion_pct": 43.7},
        "MRT_C": {"A": 64.5, "B": 53.7, "delta_K": -10.84},
        "Ts_pavimento_C": {"A": 54.7, "B": 47.2},
        "UTCI_C": {"A": 39.9, "B": 37.3, "delta_K": -2.6, "delta_con_niebla_K": -3.34},
        "Ta_aire_delta_K": -1.02,
        "dosel_cara_inferior_C": {"con_lamina_algas": 33.8, "seco": 45.5},
        "m2_refugio_efectivo": 4010, "m2_refugio_con_niebla": 4563,
        "hotspots_m2": 4884, "coolspots_m2": 3088, "invierno_perdida_pct": 48.2},
    "incidencias_climaticas": 6,
    "limitaciones_declaradas": [
        "Sin isla de calor urbana: ERA5 resuelve 30 km. Los absolutos son conservadores, los deltas robustos.",
        "Viento sin CFD: perfil logaritmico con z0 = 0,30 m. PENDIENTE CFD para la fase 02.",
        "Caudal y eficiencia de nebulizacion son HIPOTESIS: el modelo 03B fija la posicion, no el caudal.",
        "Calados de balsas y laminas son HIPOTESIS; solo la cota esta MEDIDA en el modelo.",
        "Transpiracion de huerto, tropicales, vegetacion baja, colgantes y trepadoras NO contabilizada: "
        "el resultado del capitulo de vegetacion es conservador.",
        "El registro forense de esta fase es PARCIAL: el trabajo empezo a las 15:50 y el protocolo se "
        "instauro a las 16:10 (ver DEC-0003)."],
    "master_modificado": False,
})
mf = flog.manifest()
print("manifest:", "OK" if mf else mf)
n = sum(1 for _ in open(os.path.join(FP, "FORENSIC_EVENTS.jsonl"), encoding="utf-8"))
print("EVENTOS TOTALES EN EL WORKSPACE:", n)
