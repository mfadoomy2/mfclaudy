# -*- coding: utf-8 -*-
"""FASE FINAL - S07: INDICE_GENERAL_ANALISIS_FINALES.pdf (§47) +
MANIFIESTO_ENTREGA_FINAL.csv (§46) con hash SHA-256 por entregable."""
import csv
import datetime
import glob
import hashlib
import json
import os
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..'))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
MONT = os.path.normpath(os.path.join(BASE, '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402
import refugio_editorial as E  # noqa: E402

# pregunta de cada documento (para el lector que llega sin contexto)
PREGUNTA = {
    'FINAL_GRAPHIC_SYSTEM': 'Como se lee esta familia de documentos (manual del sistema grafico).',
    'CLI-01_SOMBRA': 'Cuanta sombra produce el refugio, donde cae y que precio invernal paga.',
    'CLI-02_RADIACION': 'Cuanta energia solar deja de golpear el suelo.',
    'CLI-03_MRT': 'Cuanto baja la temperatura radiante y donde empeora (con el mecanismo probado).',
    'CLI-04_UTCI': 'Cuanto estres termico retira en cada escenario meteorologico.',
    'CLI-05_AIRE': 'Que puede y que no puede hacer una sombra sobre la temperatura del aire.',
    'CLI-06_VEGETACION': 'Que hace de verdad la capa vegetal en el clima (y su sensibilidad).',
    'CLI-07_AGUA': 'Cuanto enfria cada termino de agua y a que coste.',
    'CLI-08_VIENTO': 'Que pasaria si el dosel frena el viento (el termino no resuelto).',
    'CLI-09_CONFORT_POR_PROGRAMA': 'Que siente quien usa cada programa, de los bancos al atrio.',
    'CLI-10_ESCENARIOS_DE_FALLO': 'Que beneficio sobrevive cuando algo falla.',
    'CLIMA_SINTESIS_INTEGRADA': 'FUNCIONA COMO REFUGIO? La sintesis que cruza los diez.',
    'MOB-01_RED_PEATONAL': 'El refugio estrangula el movimiento? Anchuras, cuellos, continuidad.',
    'MOB-02_ACCESIBILIDAD_VERTICAL': 'Que pasa con el itinerario PMR cuando falla un ascensor.',
    'MOB-03_EVACUACION_Y_AFLUENCIA': 'A que distancia esta cada punto de una salida; aguanta multitudes?',
    'MOVILIDAD_SINTESIS_INTEGRADA': 'Se puede seguir cruzando Sol? Sintesis con el asterisco PMR.',
    'URB-01_METRO_Y_CERCANIAS': 'Convive el proyecto con el intercambiador? Bandas y holguras.',
    'URB-02_BORDES_Y_FACHADAS': 'Donde toca la ciudad: bordes, servidumbres, dato oficial vs criterio.',
    'CONTEXTO_SINTESIS_INTEGRADA': 'Cabe en Sol? Implantacion fisica resuelta, tramitacion pendiente.',
    'AGU-01_BALANCE_HIDRICO': 'Cuanta agua consume el peor dia y cuantos dias aguanta un corte.',
    'AGU-02_ECOLOGIA_Y_VEGETACION': 'Que comunidad vegetal lo sostiene y que riesgo asume.',
    'AGU-03_AGUA_X_CLIMA': 'Litros por kelvin: que mecanismo rinde mas por litro.',
    'AGUA_SINTESIS_INTEGRADA': 'Es sostenible el agua? Sintesis con protocolo de sequia.',
    'TEC-01_INVENTARIO_Y_FAMILIAS': 'De que esta hecho: 15.197 piezas con nombre.',
    'TEC-02_MATRIZ_MANTENIMIENTO': 'Quien cuida que, cada cuanto, con que riesgo.',
    'CONSTRUCCION_SINTESIS_INTEGRADA': 'Se puede construir y mantener? Sintesis tecnica.',
    'SOC-01_POTENCIAL_DE_ESTANCIA': 'Donde querra quedarse la gente (indice explicito).',
    'SOC-02_PERSONAS_HORA_PROTEGIDAS': 'A cuanta gente protege, en tres escenarios honestos.',
    'USO_SOCIAL_SINTESIS_INTEGRADA': 'Para quien es este refugio? Sintesis social.',
    'ECO-01_CAPEX_OPEX_CICLO_DE_VIDA': 'Que cuesta construirlo y operarlo 25 anos.',
    'ECO-02_ESCENARIOS_DE_COMERCIO': 'Que gasto comercial plausible genera (sin cuentos).',
    'ECONOMIA_SINTESIS_INTEGRADA': 'Cuanto vale una hora de sombra? El euro por persona-hora.',
    'PAT-01_VISIBILIDAD_HITOS': 'Cuanto reloj se ve — por superficie y por uso real.',
    'PATRIMONIO_SINTESIS_INTEGRADA': 'Respeta el lugar? Sintesis patrimonial.',
    'INDICADORES_CRUZADOS': 'Siete metricas nuevas que ningun analisis individual podia dar.',
    'REFUGIO_CLIMATICO_ANALISIS_GLOBAL': 'EL DOCUMENTO: viabilidad, veredicto y roadmap municipal.',
    'IA_EN_EL_REFUGIO_CLIMATICO': 'Como se uso la IA de verdad: ciclo, errores y trazabilidad.',
    'REFUGIO_CLIMATICO_COMPENDIO_ANALITICO': 'TODO lo analizado en un solo volumen: metodo, genealogia, auditoria completa, clima, sistemas, cruces y conclusiones.',
    'REFERENCE_PACKS': 'Los 12 packs de control geometrico (8 passes/vista) para la fase de imagenes IA.',
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------- manifiesto
entregables = []
for pat in ('*.pdf', '*/*.pdf', '*/*.csv', '*/*.md', '*/B_DATOS/*.json', '*/B_DATOS/*.csv',
            '09_RENDERS_Y_REPRESENTACION/_pipeline/refpacks/*/*.png'):
    entregables += glob.glob(os.path.join(BASE, pat))
entregables = sorted(set(os.path.normpath(p) for p in entregables))
rows = []
for p in entregables:
    rel = os.path.relpath(p, BASE).replace('\\', '/')
    st = os.stat(p)
    tipo = os.path.splitext(p)[1].lstrip('.').upper()
    rows.append([rel, tipo, st.st_size,
                 datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M'),
                 sha256(p)])
with open(os.path.join(OUT, 'MANIFIESTO_ENTREGA_FINAL.csv'), 'w', encoding='utf-8-sig',
          newline='') as f:
    w = csv.writer(f)
    w.writerow(['ruta', 'tipo', 'bytes', 'modificado', 'sha256'])
    w.writerows(rows)

# ---------------------------------------------------------------- indice PDF
doc = E.Doc(os.path.join(BASE, 'INDICE_GENERAL_ANALISIS_FINALES.pdf'),
            'ÍNDICE GENERAL', 'ANÁLISIS FINALES')
E.portada(doc, 'Análisis finales del\nRefugio Climático',
          'Índice general del paquete: cada documento con la pregunta que responde. '
          'Pensado para entrar sin conocer el proyecto: empiece por el ANÁLISIS GLOBAL '
          'y baje a la síntesis temática que le interese; los analíticos individuales '
          'sostienen cada cifra.',
          'ÍNDICE GENERAL',
          [('DOCUMENTOS PDF', str(len(glob.glob(os.path.join(BASE, '*/*.pdf'))) + 1)),
           ('MÉTRICAS TRAZADAS', '48'), ('HALLAZGOS', '15'),
           ('BASELINE', 'v006 · build 12')], num='ÍNDICE')

carpetas = {}
for pdf in sorted(glob.glob(os.path.join(BASE, '*/*.pdf'))):
    rel = os.path.relpath(pdf, BASE).replace('\\', '/')
    carp = rel.split('/')[0]
    base = os.path.splitext(os.path.basename(pdf))[0]
    d = fitz.open(pdf); n = d.page_count; d.close()
    carpetas.setdefault(carp, []).append((base, n, PREGUNTA.get(base, '—')))

p = doc.page('CÓMO LEER EL PAQUETE')
y = E.A4H - 1.0
y = p.kicker(y, 'RUTA DE LECTURA')
y = p.title(y, 'Tres puertas de entrada', size=16)
y = p.dashlist(E.MX, y, [
    ('30 segundos:', 'portadas del ANÁLISIS GLOBAL y de cada síntesis — las bandas de '
     'datos llevan las cifras llave.'),
    ('30 minutos:', 'REFUGIO_CLIMATICO_ANALISIS_GLOBAL.pdf completo + '
     'DISCOVERIES_REGISTER.md (15 hallazgos).'),
    ('30 horas:', 'las 8 síntesis temáticas, los 23 analíticos, los CSV de sistema y '
     'los motores en _scripts — todo reproducible desde BASELINE_SNAPSHOT.json.'),
], wrap=88, gap=0.1)
y -= 0.1
for carp in sorted(carpetas):
    if y < 1.6:
        doc.add(p)
        p = doc.page('ÍNDICE')
        y = E.A4H - 1.0
    y = p.kicker(y, carp.replace('_', ' '))
    y = p.tabla(E.MX, y, E.A4W - 2 * E.MX, ['DOCUMENTO', 'PP', 'PREGUNTA QUE RESPONDE'],
                [[b, str(n), q] for b, n, q in carpetas[carp]],
                col_w=[2.5, 0.4, 4.1], size=6.6)
    y -= 0.08
doc.add(p)
doc.close()

flog.event(fase='FINAL', tipo_evento='indice_manifiesto',
           objetivo='INDICE_GENERAL + MANIFIESTO_ENTREGA_FINAL con SHA-256',
           resultado='%d entregables hasheados; indice de %d carpetas' % (len(rows), len(carpetas)))
print('entregables:', len(rows), '| indice pp:', doc.folio)
