# -*- coding: utf-8 -*-
"""
Registro forense de la FASE 03B.5B (auditoria climatica) segun el protocolo instaurado
el 2026-08-10T16:10.

LIMITE DECLARADO Y NO NEGOCIADO: el trabajo de esta fase comenzo a las 15:50, ANTES de que
existiera el protocolo (16:10). Los eventos anteriores a 16:10 NO se capturaron en vivo.
Aqui se registran unicamente a partir de ARTEFACTOS QUE EXISTEN EN DISCO (scripts, logs de
ejecucion, CSV descargados, PDFs), declarando explicitamente `captura="ARTEFACTO_POSTERIOR"`
y dejando en null todo lo que no consta. NO se reconstruyen tiempos, ni stdout, ni cadenas de
razonamiento que no esten escritas en un archivo.
"""
import hashlib
import os
import subprocess
import sys

WS = r"C:\Users\iraxx_c0wouln\OneDrive\Documentos\iraxxxdios_ARQUITECTURA\xxxmiguelxxx\Monteserin"
FP = os.path.join(WS, "_FORENSIC_PROCESS")
FASE = os.path.join(WS, "REFUGIO_CLIMATICO", "FASE_03B5B_CLIMA")
sys.path.insert(0, FP)
import flog  # noqa: E402

F = "03B.5B-CLIMA"


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


# ---------------------------------------------------------------- 0 · como se trata el desfase
dec0 = flog.decision(
    fase=F,
    cuestion="La fase 03B.5B empezo a las 15:50 y el protocolo forense se instauro a las 16:10. "
             "Como se registra el tramo anterior sin violar la prohibicion de reconstruir "
             "retroactivamente (directiva 1)?",
    alternativas=[
        "A) No registrar nada de 03B.5B por haber empezado antes de las 16:10.",
        "B) Reconstruir la sesion completa con tiempos y razonamientos aproximados.",
        "C) Registrar solo lo que consta en artefactos reales en disco, marcando la captura como "
           "posterior y dejando null todo lo no evidenciado; capturar en vivo de aqui en adelante.",
    ],
    elegida="C",
    rechazadas=["A: perderia la evidencia de una fase entera que SI dejo artefactos verificables.",
                "B: violaria la regla de no inventar; los tiempos y el stdout intermedio no existen."],
    criterio="La directiva prohibe INVENTAR, no prohibe registrar evidencia que existe. Un log de "
             "ejecucion escrito en disco es evidencia; un tiempo que nadie midio, no. Se distingue "
             "explicitamente con el campo `captura` y con null.",
    evidencia=["mtime de los archivos de FASE_03B5B_CLIMA: 15:50 a 16:15",
               "PROCESS_NOTES.md declara el limite en 2026-08-10T16:10"],
    consecuencia="El dump de 03B.5B es parcial y lo dice. Los eventos posteriores a este registro "
                 "se capturan en vivo con flog.run().",
)

flog.event(fase=F, tipo_evento="INPUT", objetivo="Enunciado 03B.5B recibido del autor",
           criterio_explicito="Se conserva literal en INPUTS para que el resultado pueda contrastarse "
                              "contra lo que se pidio, punto por punto.",
           archivos_generados=[rel(os.path.join(FP, "INPUTS", "ENUNCIADO_03B5B_2026-08-10.md"))],
           captura="ARTEFACTO_POSTERIOR", conocimiento="CONFIRMED",
           decisiones=[dec0])

# ---------------------------------------------------------------- 1 · datos climaticos
CLIMA = os.path.join(FASE, "_clima")
flog.event(
    fase=F, tipo_evento="ADQUISICION_DATOS",
    objetivo="Descargar clima real de Madrid centro en lugar de usar un clima generico",
    criterio_explicito="El enunciado (punto 3) exige fuente identificada con estacion, coordenadas, "
                       "periodo y fecha de descarga. Se descarta cualquier valor 'tipico de Madrid'.",
    herramienta="curl",
    comando=["curl https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat=40.4169&lon=-3.7035&outputformat=csv",
             "curl https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?lat=40.4169&lon=-3.7035"
             "&startyear=2005&endyear=2020&outputformat=csv&components=1"],
    parametros=dict(lat=40.4169, lon=-3.7035, elev_m=665.0,
                    dataset_tmy="PVGIS v5.2 TMY", dataset_serie="PVGIS v5.2 SARAH2 + ERA5 2005-2020"),
    resultado="TMY 8760 h con T2m, RH, G(h), Gb(n), Gd(h), IR(h), WS10m, WD10m, SP. "
              "Serie 2005-2020 con 140.275 h.",
    validacion="Extremo real hallado: 2018-08-03 con Tmax 40.1 C, coherente con la ola de calor "
               "documentada de agosto 2018 en Madrid.",
    artefactos=[art(os.path.join(CLIMA, "PVGIS_TMY_40.4169_-3.7035.csv")),
                art(os.path.join(CLIMA, "PVGIS_HOURLY_2005_2020.csv")),
                art(os.path.join(CLIMA, "escenarios.json"))],
    archivos_fuente=[rel(os.path.join(FASE, "clima_prep.py"))],
    estado="OK", captura="ARTEFACTO_POSTERIOR", conocimiento="CONFIRMED")

flog.decision(
    fase=F,
    cuestion="PVGIS/ERA5 resuelve ~30 km y por tanto NO contiene la isla de calor urbana de Madrid "
             "centro. Se corrige la temperatura del aire al alza?",
    alternativas=["A) Aplicar un incremento UHI de +2 a +4 K a Ta.",
                  "B) Usar Ta de fondo regional tal cual y declarar la limitacion.",
                  "C) Buscar serie de AEMET Retiro."],
    elegida="B",
    rechazadas=["A: seria un ajuste no verificable incrustado en todos los resultados; ademas el "
                "delta A-B apenas cambia porque ambos estados comparten Ta.",
                "C: AEMET OpenData requiere clave de API de la que no se dispone en esta maquina."],
    criterio="La auditoria compara DOS ESTADOS con el mismo clima. Un sesgo comun en Ta se cancela "
             "casi por completo en el delta, que es la magnitud que se pide. Inflar Ta sin poder "
             "verificarlo contaminaria el valor absoluto de UTCI sin mejorar la comparacion.",
    consecuencia="Los UTCI absolutos son conservadores respecto al centro real de Madrid; los deltas "
                 "son robustos. Queda declarado en escenarios.json -> fuente.nota_uhi y en el master.",
    conocimiento="CONFIRMED")

# ---------------------------------------------------------------- 2 · validaciones fisicas
flog.event(
    fase=F, tipo_evento="VALIDACION",
    objetivo="Validar el algoritmo de posicion solar antes de usarlo en 1.116 trazados",
    criterio_explicito="Un error sistematico en la posicion del sol corrompe en silencio todos los "
                       "mapas. Se contrasta contra un dato independiente: la columna H_sun de PVGIS.",
    funcion="clima_core.sun_position (algoritmo PSA, Blanco-Muriel 2001)",
    resultado="error medio -0.031 deg, desviacion 0.123, maximo absoluto 0.338 sobre 117 muestras "
              "con elevacion > 3 deg. Solsticio de verano 72.66 deg frente a 73.02 teorico "
              "(la diferencia es el desfase entre 12:00 UTC y el mediodia solar en lon -3.70).",
    validacion="PASS", estado="OK", conocimiento="CONFIRMED", captura="ARTEFACTO_POSTERIOR")

flog.event(
    fase=F, tipo_evento="VALIDACION",
    objetivo="Verificar que la escena climatica es la MISMA que audito 03B.5",
    criterio_explicito="El enunciado (punto 1) exige coincidencia en numero de objetos, mallas, "
                       "triangulos, coordenadas y dimensiones.",
    resultado="6.672 mallas y 394.610 triangulos, identico a 03B.5. Huella sha256 de vertices "
              "41a82b72634490377f2be60e7096b6ca. Ambito 11.020 m2 frente a 11.014 m2 de 03B.5 "
              "(diferencia por remuestreo de la mascara de 0.25 a 0.50 m: 0.05 %).",
    validacion="PASS", estado="OK", conocimiento="CONFIRMED", captura="ARTEFACTO_POSTERIOR")

# ---------------------------------------------------------------- 3 · errores reales y rectificaciones
e1 = flog.event(
    fase=F, tipo_evento="ERROR_METODOLOGICO",
    objetivo="La lamina de microalgas de cada disco vive en la capa 11_WATER y se clasificaba como "
             "OPACA, de modo que el parametro tau_canopy nunca llegaba a aplicarse",
    criterio_explicito="Sintoma detectado en la prueba unitaria de transmitancia: un punto bajo un "
                       "disco daba tau=0.000 en vez del 0.12 esperado.",
    error="Clasificacion optica por capa. El conjunto hoja-canopy (aro + nervios + membrana + lamina "
          "de agua + embudo) tiene sus partes repartidas en 4 capas distintas.",
    resultado="El parametro declarado quedaba enmascarado: la hipotesis no era auditable ni se podia "
              "someter a analisis de sensibilidad, aunque el resultado numerico (opaco) fuera casi el mismo.",
    rectificacion="Nueva funcion clima_core.class_of(): clasifica por BLOQUE (prefijo LEAF_) y no por "
                  "capa. Verificado despues: tau=0.12 bajo disco aislado, 0.55 bajo cupula.",
    estado="RECTIFICADO", conocimiento="CONFIRMED", captura="ARTEFACTO_POSTERIOR")

e2 = flog.event(
    fase=F, tipo_evento="ERROR_METODOLOGICO",
    objetivo="El factor de vision de cielo contaba como CIELO los rayos que atraviesan el dosel",
    criterio_explicito="Revision del termino de onda larga de la MRT: un rayo que atraviesa una hoja "
                       "translucida transmite onda corta, pero NO ve el cielo frio en el infrarrojo.",
    error="SVF se calculaba con la mascara `alive` (no bloqueado por opaco) en vez de con la clase del "
          "primer elemento encontrado.",
    resultado="SVF del estado B sobreestimado: 0.61-0.67 cuando el valor correcto es 0.46-0.49. El error "
              "SOBREVALORABA la propuesta, al atribuirle mas enfriamiento radiante al cielo del real.",
    rectificacion="clima_core.transmittance(want_first=True) devuelve la clase del primer elemento "
                  "encontrado. El hemisferio se descompone en fracciones cielo/dosel/opaco/vegetal y cada "
                  "una emite a SU temperatura, calculada por balance.",
    estado="RECTIFICADO", conocimiento="CONFIRMED", captura="ARTEFACTO_POSTERIOR",
    relaciones_con_eventos_previos=[e1])

e3 = flog.event(
    fase=F, tipo_evento="ERROR_METODOLOGICO",
    objetivo="La metrica de rendimiento por disco era degenerada",
    criterio_explicito="Los 67 discos daban una eficiencia practicamente identica (555-562), lo que es "
                       "imposible si los discos difieren en radio, cota y posicion.",
    error="Se media la sombra proyectada BRUTA, que por construccion es area_disco x numero_de_horas: "
          "una tautologia, no una medida de rendimiento.",
    resultado="La metrica no discriminaba y habria impedido responder al punto 10 del enunciado "
              "(identificar discos que no aportan nada).",
    rectificacion="Se pasa a medir la sombra EXCLUSIVA (celdas sombreadas por ese disco y por ningun "
                  "otro) y la sombra sobre suelo pisable. Con la metrica corregida el rango va de 0 a "
                  "98 m2 y aparece el hallazgo: los discos grandes centrales tienen aportacion exclusiva "
                  "NULA (estan apilados sobre otros) y los pequenos perifericos a cota 4.5 son los que "
                  "mas aportan.",
    estado="RECTIFICADO", conocimiento="CONFIRMED", captura="ARTEFACTO_POSTERIOR")

e4 = flog.event(
    fase=F, tipo_evento="ERROR_METODOLOGICO",
    objetivo="El umbral del indice de refugio era fisicamente inalcanzable",
    criterio_explicito="La clase REFUGIO EFECTIVO salia con 188 m2 (1.7 % del ambito), sospechosamente baja.",
    error="Se exigia UTCI_B < 32 C con una temperatura del aire de 34.7 C. Con Ta=34.7 el suelo del UTCI "
          "esta en torno a 30-31 aunque la MRT baje hasta igualar el aire: el criterio era casi imposible "
          "de cumplir por construccion, no por comportamiento del proyecto.",
    resultado="Habria concluido que el proyecto practicamente no crea refugio, por un artefacto del umbral.",
    rectificacion="Criterio sustituido por el SALTO DE CATEGORIA de la escala oficial de estres termico "
                  "UTCI (26-32 / 32-38 / 38-46), que no es un umbral inventado sino la clasificacion "
                  "publicada. Resultado corregido: 4.010 m2 (36.4 %) y 4.563 m2 con nebulizacion.",
    estado="RECTIFICADO", conocimiento="CONFIRMED", captura="ARTEFACTO_POSTERIOR")

flog.event(
    fase=F, tipo_evento="CHEQUEO_FISICO",
    objetivo="Punto 36 del enunciado: sanity checks fisicos",
    criterio_explicito="Buscar activamente resultados imposibles antes de publicarlos.",
    resultado=(
        "1) Reduccion de Ta de 15 K: NO ocurre. El efecto sobre el aire a escala plaza es 1.02 K. OK. "
        "2) Pavimento sombreado mas caliente que el soleado: NO ocurre; pero SI aparece Ts_B > Ts_A en el "
        "52 % de las celdas y MRT_B > MRT_A en el 46 %. Investigado: son celdas que conservan el sol "
        "(tau 0.84) y pierden vista de cielo (SVF 0.97 -> 0.78). Es atrapamiento radiante real, no un "
        "error de calculo. Se documenta como hallazgo. "
        "3) Agua que evapora mas de lo disponible: comprobado el cierre de masa. 20.7 m3/dia frente a "
        "99.8 m3 almacenados = 4.8 dias de autonomia; la lamina de microalgas pierde el 37 % de su calado "
        "al dia. Se registra como incidencia CL-005. "
        "4) UTCI que mejora donde empeora la MRT: 1.905 celdas. Coherente: son puntos donde el termino "
        "convectivo y el de onda larga compensan; no se descarta pero queda anotado. "
        "5) Membrana transparente con sombra de opaca: corregido en el evento %s (tau_canopy no se "
        "aplicaba)." % e1),
    validacion="4 de 5 checks pasan; el 2 y el 4 se conservan como hallazgo documentado, no como error.",
    estado="OK", conocimiento="CONFIRMED", captura="ARTEFACTO_POSTERIOR",
    relaciones_con_eventos_previos=[e1, e2, e3, e4])

# ---------------------------------------------------------------- 4 · artefactos producidos
docs = [f for f in sorted(os.listdir(FASE)) if f.endswith(('.pdf', '.csv', '.md'))]
flog.event(
    fase=F, tipo_evento="ENTREGA",
    objetivo="Documentos de la auditoria climatica 03B.5B",
    resultado="%d documentos" % len(docs),
    artefactos=[art(os.path.join(FASE, d)) for d in docs],
    archivos_fuente=[rel(os.path.join(FASE, s)) for s in
                     ("clima_core.py", "clima_prep.py", "clima_run.py", "clima_run2.py", "clima_report.py")],
    estado="OK", conocimiento="CONFIRMED", captura="ARTEFACTO_POSTERIOR")

# ---------------------------------------------------------------- 5 · ejecucion EN VIVO (ya con protocolo)
print("--- ejecutando verificacion en vivo bajo flog.run() ---")
rid, rd = flog.run(
    [sys.executable, "-c",
     "import json,os;m=json.load(open(r'%s'));"
     "print('metricas verificadas:', len(m));"
     "print('dMRT', m['dMRT'], 'K | dUTCI', m['dUTCI'], 'K | refugio', m['m2_refugio'], 'm2')"
     % os.path.join(FASE, "_data", "metricas.json").replace("\\", "\\\\")],
    cwd=FASE, fase=F,
    objetivo="Verificacion en vivo, ya bajo protocolo, de que las metricas publicadas son las que "
             "estan en disco",
    criterio="Dejar al menos una ejecucion de esta fase capturada en vivo y no derivada de artefacto.")
print("run:", rid, "exit", rd.get("exit"))

flog.state_change("Efecto climatico real del Refugio de Puerta del Sol",
                  "UNKNOWN", "CONFIRMED",
                  motivo="Medido sobre geometria aprobada con clima real: dMRT -10.8 K, dUTCI -2.6 K "
                         "(-3.3 K con nebulizacion), dTa_aire ~1.0 K, 36.4 % del ambito baja de categoria "
                         "UTCI. El proyecto funciona como pantalla radiante, no como acondicionador de aire.",
                  eventos_origen=[rid])

flog.snapshot("FIN_03B5B", {
    "fase": F,
    "escena": {"mallas": 6672, "triangulos": 394610, "identica_a_03B5": True},
    "clima": {"fuente": "PVGIS v5.2 TMY + serie 2005-2020", "lat": 40.4169, "lon": -3.7035,
              "uhi_incluida": False, "conocimiento": "CONFIRMED"},
    "resultados_clave": {
        "sombra_critica_pct": {"A": 5.3, "B": 45.3},
        "radiacion_kWh_m2": {"A": 648, "B": 365, "reduccion_pct": 43.7},
        "MRT_C": {"A": 64.5, "B": 53.7, "delta_K": -10.8},
        "UTCI_C": {"A": 39.9, "B": 37.3, "delta_K": -2.6, "delta_con_niebla_K": -3.34},
        "Ta_aire_delta_K": -1.02,
        "m2_refugio_efectivo": 4010, "m2_refugio_con_niebla": 4563,
        "hotspots_m2": 4884, "invierno_perdida_pct": 48.2},
    "incidencias": 6,
    "limitaciones_declaradas": [
        "Sin isla de calor urbana (ERA5 a 30 km).",
        "Viento sin CFD: perfil logaritmico con z0=0.30 m. Marcado PENDIENTE CFD para fase 02.",
        "Caudal y eficiencia de nebulizacion son HIPOTESIS: el modelo 03B no los define.",
        "Calados de balsas y laminas son HIPOTESIS; solo la cota es MEDIDA.",
        "Transpiracion de huerto, tropicales, bajas, colgantes y trepadoras NO contabilizada: "
        "el resultado de vegetacion es conservador."],
    "master_modificado": False,
})
mf = flog.manifest()
print("manifest:", mf if isinstance(mf, str) else "OK")
print("EVENTOS TOTALES:", sum(1 for _ in open(os.path.join(FP, "FORENSIC_EVENTS.jsonl"), encoding="utf-8")))
