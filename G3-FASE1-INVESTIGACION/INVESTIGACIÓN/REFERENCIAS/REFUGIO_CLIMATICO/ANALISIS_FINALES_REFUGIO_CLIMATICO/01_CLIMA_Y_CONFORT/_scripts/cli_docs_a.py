# -*- coding: utf-8 -*-
"""FASE FINAL - PDFs analiticos CLI-01..CLI-05 (sombra, radiacion, MRT, UTCI, aire)."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
import refugio_editorial as E  # noqa: E402

OUT = os.path.join(BASE, '01_CLIMA_Y_CONFORT')
with open(os.path.join(OUT, 'B_DATOS', 'cli_stats.json'), encoding='utf-8') as f:
    R = json.load(f)
geo = E.load_geo()
W = E.np_aud('walk.npy')[::2, ::2].astype(bool)
ny, nx = E.np_cli('u_E2_16_B.npy').shape
W = W[:ny, :nx]
FUENTE = 'FUENTE: _reclima9/_data (v006 build 12, 2026-08-13) · celda 0,5 m · ventana crítica 15 jun–15 sep'


def cabecera_analisis(doc, cid, titulo, pregunta, metodo, datos, nivel, limitaciones):
    """Primera pagina normalizada §27: PREGUNTA / METODO / DATOS / NIVEL."""
    p = doc.page(cid)
    y = E.A4H - 1.0
    y = p.kicker(y, cid + ' · CLIMA Y CONFORT')
    y = p.title(y, titulo, size=19)
    y = p.subtitle(y, pregunta)
    p.chip(E.MX, y - 0.02, nivel)
    y -= 0.34
    colw = (E.A4W - 2 * E.MX - 0.4) / 2
    y1 = p.ficha(E.MX, y, [('MÉTODO', metodo)], wcol=colw, wrap=int(colw * 7.4))
    y2 = p.ficha(E.MX + colw + 0.4, y, [('DATOS', datos), ('LIMITACIONES', limitaciones)],
                 wcol=colw, wrap=int(colw * 7.4))
    return p, min(y1, y2) - 0.08


def mapa_doble(p, y, arrA, arrB, cmap, vmin, vmax, labA, labB, leyenda, cap_lead, cap, alto=3.0):
    w = (E.A4W - 2 * E.MX - 0.35) / 2
    ax = p.axes(E.MX, y - alto, w, alto)
    E.draw_context(ax, geo)
    im = E.show_raster(ax, arrA, cmap, vmin=vmin, vmax=vmax, mask=W)
    p.text(E.MX, y + 0.06, labA, size=6.2, tracked=True, weight='bold', color=E.GRAYTX)
    ax2 = p.axes(E.MX + w + 0.35, y - alto, w, alto)
    E.draw_context(ax2, geo)
    E.show_raster(ax2, arrB, cmap, vmin=vmin, vmax=vmax, mask=W)
    p.text(E.MX + w + 0.35, y + 0.06, labB, size=6.2, tracked=True, weight='bold', color=E.GRAYTX)
    E.cbar(p, im, E.MX, y - alto - 0.32, 1.7, leyenda)
    yy = p.caption(E.MX + 2.1, y - alto - 0.30, cap_lead, cap, fuente=None, wrap=66)
    p.text(E.MX, min(yy, y - alto - 0.62) - 0.02, FUENTE, size=5.4, color=E.GRAYTX)
    return min(yy, y - alto - 0.62) - 0.30


# ================================================================ CLI-01 · SOMBRA
doc = E.Doc(os.path.join(OUT, 'CLI-01_SOMBRA.pdf'), 'CLI-01 · SOMBRA', '01 · CLIMA')
E.portada(doc, 'Sombra', 'Cuánta sombra produce el refugio, dónde cae y qué precio '
          'invernal paga. Situación actual frente a propuesta sobre la ventana crítica '
          'de verano (15 jun–15 sep) y el solsticio de invierno.',
          'CLI-01 · CLIMA Y CONFORT',
          [('BASELINE', 'v006 · build 12'),
           ('SOMBRA CRÍTICA', '3,4 % › 42,3 %'),
           ('SUELO EN SOMBRA ≥50 %', doc.metric('CLI01-M1', '3.669', 'm²', 'A',
            'shade_crit_B>=0.5 sobre pisable', '_reclima9/shade_crit_B.npy')),
           ('COSTE INVERNAL', '−40,3 % sol 21-dic')], num='CLI-01')

p, y = cabecera_analisis(
    doc, 'CLI-01', 'La sombra que no existía',
    '¿Cuánta sombra útil produce el refugio durante la ventana crítica de verano, '
    'dónde cae y sobre qué programa?',
    'Trazado de rayos sobre el vóxel v006 (0,5 m): 431 posiciones solares reales '
    '(algoritmo PSA) en 31 días muestreados de la ventana 15 jun–15 sep; una celda está '
    '«en sombra» cuando su transmitancia directa cae por debajo de 0,5. La vegetación '
    'atenúa con k_veg POR ESPECIE (Beer–Lambert volumétrico).',
    'shade_crit_A/B.npy, sunhours_A/B.npy, zonas.json (build 12). '
    'Clima PVGIS Madrid, ventana crítica de 93 días.',
    'A',
    'La sombra se evalúa a nivel de suelo (0,05 m); los toldos de los kioscos existentes '
    'no están modelados; el arbolado OSM entra con copa cilíndrica equivalente.')
shA, shB = E.np_cli('shade_crit_A.npy'), E.np_cli('shade_crit_B.npy')
y = mapa_doble(p, y - 0.05, shA, shB, E.CMAP_AGUA, 0, 1,
               'A · SOL ACTUAL', 'B · PROPUESTA', 'FRACCIÓN DE SOMBRA · VENTANA CRÍTICA',
               'La plaza pasa de plancha solar a mosaico:',
               'la sombra crítica media sube de 3,4 % a 42,3 % del ámbito analizado (sobre '
               'suelo pisable: 3,2 % a 38,3 %). El anillo '
               'perimetral y la banda de la cinta concentran la sombra nueva; el centro '
               'ceremonial de la plaza queda deliberadamente abierto.')
# bignums
x = E.MX
x0 = x
p.bignum(x, y, '42,3', '%', 'sombra crítica media de la propuesta (antes 3,4 %)'); x += 2.2
p.bignum(x, y, doc.metric('CLI01-M2', '4.186', 'm²', 'A', 'm2_sombra_extra',
                          '_reclima9/metricas.json'), '', 'de sombra nueva en la hora crítica'); x += 2.2
p.bignum(x, y, '6,2 › 3,6', 'h', 'horas de sol 12–18 h sobre el suelo (media A › B)')
doc.add(p)

# pagina 3: invierno + programa
p = doc.page('CLI-01 · INVIERNO Y PROGRAMA')
y = E.A4H - 1.0
y = p.kicker(y, 'CLI-01.2 · EL PRECIO INVERNAL')
y = p.title(y, 'El invierno paga el 40 % — pero no en todas partes', size=16)
y = p.subtitle(y, '¿Cuánto sol de invierno roba la misma sombra que salva el verano? '
                  'Radiación del 21 de diciembre sobre el suelo, estado A frente a B.')
winA, winB = E.np_cli('radwin_A.npy'), E.np_cli('radwin_B.npy')
y = mapa_doble(p, y, winA, winB, E.CMAP_CALOR, 0, max(1.0, float(np.nanmax(winA))),
               'A · 21-DIC ACTUAL', 'B · 21-DIC PROPUESTA', 'RADIACIÓN 21-DIC · KWH/M²·DÍA',
               'El coste existe y se publica:',
               'la media diaria del solsticio cae de 2,30 a 1,29 kWh/m² (−40,3 %). '
               'Aun así, 5.690 m² —el 58 % del suelo pisable— conservan al menos la mitad '
               'de su sol invernal, porque las hojas del dosel se concentran donde el '
               'verano es letal y el corazón de la plaza queda abierto.', alto=2.85)
doc.metric('CLI01-M3', -40.3, '%', 'A', 'radwin_B/radwin_A sobre pisable', '_reclima9/radwin_*.npy',
           'perdida media de radiacion el 21-dic')
doc.metric('CLI01-M4', 5690, 'm²', 'A', 'celdas con radwin_B>=0.5*radwin_A', '_reclima9/radwin_*.npy')
y -= 0.05
y = p.kicker(y, 'CLI-01.3 · SOMBRA POR PROGRAMA')
rows = []
for z in R['zonas_resumen']:
    zz = [w for w in json.load(open(os.path.join(OUT, 'B_DATOS', 'cli_stats.json'), encoding='utf-8'))['zonas_resumen'] if w['zona'] == z['zona']]
    rows.append([z['zona'], '%.0f' % z['m2'], '—', '%.0f %%' % (z.get('refugio_pct') or 0)])
zon = json.loads(open(os.path.join(OUT, 'B_DATOS', 'zonas_programa.csv'), encoding='utf-8-sig').read().splitlines()[0]) if False else None
import csv as _csv
with open(os.path.join(OUT, 'B_DATOS', 'zonas_programa.csv'), encoding='utf-8-sig') as f:
    zrows = list(_csv.DictReader(f))
rows = [[z['zona'], z['m2'], '%s %% › %s %%' % (z['sombra_A'], z['sombra_B']), z['refugio_pct'] + ' %']
        for z in zrows]
y = p.tabla(E.MX, y, E.A4W - 2 * E.MX, ['PROGRAMA', 'M²', 'SOMBRA A › B', 'REFUGIO'],
            rows, col_w=[2.6, 0.9, 2.2, 1.3], size=7.2)
p.text(E.MX, y, FUENTE + ' · zonas.json', size=5.4, color=E.GRAYTX)
doc.add(p)

# pagina 4: conclusion
p = doc.page('CLI-01 · LECTURA')
y = E.A4H - 1.0
y = p.kicker(y, 'CLI-01.4 · LECTURA Y CONCLUSIÓN')
y = p.title(y, 'Qué significa', size=16)
y = p.dashlist(E.MX, y - 0.05, [
    ('La sombra es el mecanismo primario.', 'De los −10,9 K de MRT medio, la práctica '
     'totalidad procede de interceptar radiación directa; el agua y la vegetación refinan.'),
    ('Cae donde se necesita.', 'Bancos (0,7 %›72 %), huerto (0,9 %›83 %) y los recorridos '
     'perimetrales concentran la sombra; el vacío central se preserva como espacio de evento.'),
    ('El coste invernal está localizado.', 'La pérdida del 40 % se concentra bajo las hojas '
     'del dosel; quien busque sol en enero lo encuentra en el 58 % del suelo restante.'),
    ('Decisión de proyecto pendiente de validación:', 'el balance sombra-verano / sol-invierno '
     'es un juicio de valor urbano. Los datos están; la ponderación es política.'),
], wrap=86, gap=0.1)
y -= 0.1
y = p.panel(E.MX, y, E.A4W - 2 * E.MX, 1.05, 'LIMITACIONES')
p.text(E.MX + 0.16, y, 'El umbral tau<0,5 es binario (una celda medio-sombreada cuenta '
       'entera); los kioscos existentes no proyectan sombra en el modelo (subestima la '
       'sombra del estado A en sus entornos inmediatos); no hay nubes: cielo despejado '
       'PVGIS, el caso pésimo. Nivel A en geometría; el clima de entrada es estadístico.',
       size=8.0, wrap=94)
doc.add(p)
doc.close()
print('CLI-01 ok', doc.folio, 'pp')

# ================================================================ CLI-02 · RADIACION
doc = E.Doc(os.path.join(OUT, 'CLI-02_RADIACION.pdf'), 'CLI-02 · RADIACIÓN', '01 · CLIMA')
E.portada(doc, 'Radiación solar',
          'Cuánta energía solar deja de golpear el suelo de Sol: acumulada de la ventana '
          'crítica, retirada por el dosel, y su distribución espacial en verano e invierno.',
          'CLI-02 · CLIMA Y CONFORT',
          [('BASELINE', 'v006 · build 12'),
           ('REDUCCIÓN VERANO', doc.metric('CLI02-M1', '−38,0', '%', 'A',
            'rad_B vs rad_A sobre pisable', '_reclima9/rad_*.npy')),
           ('MEDIA ACTUAL', '653,9 W/m²'), ('MEDIA PROPUESTA', '380,3 W/m²')], num='CLI-02')
p, y = cabecera_analisis(
    doc, 'CLI-02', 'La energía retirada',
    '¿Cuánta radiación solar deja de recibir cada metro de suelo y adónde va la que sigue llegando?',
    'Acumulación de radiación directa+difusa por celda con las mismas 431 posiciones '
    'solares del CLI-01 y bóveda de 61 direcciones para la difusa; media de la ventana '
    'crítica en W/m². Invierno: suma del 21-dic en kWh/m²·día.',
    'rad_A/B.npy, rad_delta.npy, radwin_A/B.npy, metricas.json.', 'A',
    'Sin nubes (caso pésimo) ni reflexiones entre fachadas de segundo orden (albedo '
    'de suelo sí incluido en el balance MRT del CLI-03).')
radA, radB = E.np_cli('rad_A.npy'), E.np_cli('rad_B.npy')
y = mapa_doble(p, y - 0.05, radA, radB, E.CMAP_CALOR, 0, float(np.nanpercentile(radA[W], 98)),
               'A · W/M² MEDIA CRÍTICA', 'B · W/M² MEDIA CRÍTICA', 'RADIACIÓN MEDIA · W/M²',
               'De 654 a 380 W/m² de media:',
               'el dosel retira el 38 % de la energía solar del suelo pisable. El mapa B '
               'enseña la nueva geografía térmica: pasillos protegidos, claros deliberados '
               'y el gradiente hacia los bordes con los edificios.')
x = E.MX
p.bignum(x, y, '654 › 380', 'W/m²', 'radiación media sobre pisable, A › B'); x += 2.6
p.bignum(x, y, '−38 %', '', 'energía retirada en la ventana crítica'); x += 2.2
p.bignum(x, y, '−100 %', '', 'máximo local: bajo las hojas densas del dosel')
doc.metric('CLI02-M2', 653.9, 'W/m²', 'A', 'rad_A media pisable', '_reclima9/rad_A.npy')
doc.metric('CLI02-M3', 380.3, 'W/m²', 'A', 'rad_B media pisable', '_reclima9/rad_B.npy')
doc.add(p)
p = doc.page('CLI-02 · LECTURA')
y = E.A4H - 1.0
y = p.kicker(y, 'CLI-02.2 · LECTURA')
y = p.title(y, 'Energía, no temperatura', size=16)
y = p.dashlist(E.MX, y, [
    ('La radiación es la palanca.', 'A 33 °C de aire, la diferencia entre sol y sombra '
     'son ~25 K de MRT: la energía retirada es el presupuesto del confort del CLI-03/04.'),
    ('El −38 % es promedio, no uniforme.', 'Bajo dosel denso la retirada llega al 100 %; '
     'el claro central mantiene su régimen solar casi intacto (decisión de proyecto).'),
    ('Verano e invierno comparten geometría.', 'La misma hoja retira 38 % en julio y 40 % '
     'en diciembre: el dosel es estacional en el CLIMA (hoja caduca en las especies) pero '
     'la membrana estructural no. Véase la discusión estacional en 04_AGUA/ECO.'),
], wrap=86, gap=0.1)
doc.add(p)
doc.close()
print('CLI-02 ok', doc.folio, 'pp')

# ================================================================ CLI-03 · MRT
doc = E.Doc(os.path.join(OUT, 'CLI-03_MRT.pdf'), 'CLI-03 · MRT', '01 · CLIMA')
E.portada(doc, 'Temperatura radiante',
          'La temperatura que la piel siente de verdad: MRT actual, propuesta, delta, '
          'hotspots supervivientes y la cola donde el proyecto empeora las cosas.',
          'CLI-03 · CLIMA Y CONFORT',
          [('BASELINE', 'v006 · build 12'),
           ('MRT MEDIA', '65,2 › 54,3 °C'),
           ('DELTA MEDIO', doc.metric('CLI03-M1', '−10,9', 'K', 'A',
            'Tmrt_B - Tmrt_A media pisable E2/16h', '_reclima9/f_E2_16_*_Tmrt.npy')),
           ('EN REFUGIO', '−28,2 K')], num='CLI-03')
p, y = cabecera_analisis(
    doc, 'CLI-03', 'Once grados menos de pared radiante',
    '¿Cuánto baja la temperatura media radiante y dónde quedan los puntos calientes?',
    'Balance radiativo completo por celda: onda corta directa/difusa/reflejada + onda '
    'larga de cielo, suelo y superficies (el rayo que atraviesa un dosel transmite sol '
    'pero NO ve el cielo frío). Superficies con temperatura propia (granito/agua/vegetal). '
    'MRT a 1,10 m según VDI 3787.',
    'f_E2_16_A/B_Tmrt.npy, spots.json, metricas.json. Escenario E2 (día caluroso p95) 16:00.',
    'A',
    'Emisividades y albedos son ESTIMADOS declarados en PARAMS; persona estándar (a_k 0,70).')
tA = E.np_cli('f_E2_16_A_Tmrt.npy'); tB = E.np_cli('f_E2_16_B_Tmrt.npy')
y = mapa_doble(p, y - 0.05, tA, tB, E.CMAP_CALOR, 30, 75,
               'A · MRT °C · E2 16H', 'B · MRT °C · E2 16H', 'MRT · °C',
               'De pared radiante a mosaico térmico:',
               'la media pisable cae de 65,2 a 54,3 °C; bajo el dosel la MRT baja hasta '
               '−28 K. Los máximos supervivientes (hotspots CL-HOT) son los claros '
               'deliberados y las bandas junto a fachadas soleadas.')
x = E.MX
p.bignum(x, y, '−10,9', 'K', 'delta MRT medio sobre pisable'); x += 2.0
p.bignum(x, y, '−28,2', 'K', 'delta MRT medio dentro del refugio'); x += 2.0
p.bignum(x, y, '−38,8', 'K', 'delta máximo local bajo dosel denso')
doc.add(p)

p = doc.page('CLI-03 · LA COLA POSITIVA')
y = E.A4H - 1.0
y = p.kicker(y, 'CLI-03.2 · DONDE EMPEORA (§43)')
y = p.title(y, 'La cola positiva crece con el calor', size=16)
y = p.subtitle(y, '¿Hay celdas donde la propuesta EMPEORA la sensación? Sí: y crecen '
                  'con la dureza del día. 55 m² en E1, 755 m² en E2, 1.175 m² en E3.')
dU = E.np_cli('u_E2_16_B.npy') - E.np_cli('u_E2_16_A.npy')
ax = p.axes(E.MX, y - 3.2, 4.6, 3.05)
E.draw_context(ax, geo)
im = E.show_raster(ax, dU, E.CMAP_DELTA, vmin=-6, vmax=6, mask=W)
E.cbar(p, im, E.MX, y - 3.5, 1.7, 'ΔUTCI B−A · K · E2 16H')
cl = R['cola_positiva_E2_16']['clusters']
for c in cl:
    ax.plot(c['x'], c['y'], 'o', mfc='none', mec=E.MAGENTA, ms=9, mew=1.4)
yy = p.ficha(E.MX + 4.95, y - 0.15, [
    ('OBSERVACIÓN', 'Los cinco mayores focos de empeoramiento suman %d m² y NO están bajo '
     'el dosel: toda la cola positiva cae en celdas abiertas.' % sum(c['m2'] for c in cl)),
    ('HIPÓTESIS', 'Pérdida de factor de cielo sin sombra a cambio: las celdas ven MENOS '
     'cielo frío (más onda larga de estructuras calientes) pero el sol les sigue llegando.'),
    ('PRUEBA', 'Medido sobre las 3.021 celdas de la cola: Δsvf −0,53 con Δtau −0,01 '
     '(pierden la mitad del cielo, conservan su sol). Las celdas que mejoran: Δsvf −0,63 '
     'CON Δtau −0,75. La firma del mecanismo, confirmada.'),
    ('CONSECUENCIA', 'Sombra o cielo: media medida a media altura. Donde no se pueda dar '
     'sombra, conviene despejar cielo (candidato de ajuste fino post-piloto).'),
], wcol=2.6, wrap=34)
p.text(E.MX, y - 3.85, FUENTE, size=5.4, color=E.GRAYTX)
doc.metric('CLI03-M2', 755, 'm²', 'A', 'celdas dUTCI>+0.5K en E2/16', 'cli_stats.json')
doc.metric('CLI03-M3', 1175, 'm²', 'A', 'celdas dUTCI>+0.5K en E3/16', 'cli_stats.json')
doc.add(p)
doc.close()
print('CLI-03 ok', doc.folio, 'pp')

# ================================================================ CLI-04 · UTCI
doc = E.Doc(os.path.join(OUT, 'CLI-04_UTCI.pdf'), 'CLI-04 · UTCI', '01 · CLIMA')
E.portada(doc, 'Estrés térmico UTCI',
          'El índice que integra aire, radiación, viento y humedad. Categorías de estrés '
          'por escenario: día típico, día caluroso p95, ola de calor y nebulización activa.',
          'CLI-04 · CLIMA Y CONFORT',
          [('BASELINE', 'v006 · build 12'),
           ('ΔUTCI E2', '−2,5 K'), ('ΔUTCI OLA E3', '−2,0 K'),
           ('CON NIEBLA', doc.metric('CLI04-M1', '−3,4', 'K', 'B',
            'dUTCI E2 con nebulizacion (E4)', '_reclima9/u_E4_16_B.npy'))], num='CLI-04')
p, y = cabecera_analisis(
    doc, 'CLI-04', 'Del «muy fuerte» al «fuerte»',
    '¿Cuánto estrés térmico retira la propuesta en cada escenario meteorológico y a qué '
    'categoría UTCI se muda el suelo de Sol?',
    'UTCI (pythermalcomfort) por celda con la MRT del CLI-03, aire/humedad/viento del '
    'escenario PVGIS. E1=día típico, E2=p95, E3=ola de calor (38 °C), E4=E2+nebulización '
    'isoentálpica. Categorías oficiales de estrés por calor.',
    'u_E{1,2,3}_{14,16,18}_{A,B}.npy + u_E4_16_B.npy, refugio.json.', 'A',
    'Viento de escenario idéntico en A y B (el abrigo del dosel no está resuelto: '
    'véase CLI-08); UTCI evaluado 1 de cada 3 celdas e interpolado (declarado en el método).')
uA = E.np_cli('u_E2_16_A.npy'); uB = E.np_cli('u_E2_16_B.npy')
y = mapa_doble(p, y - 0.05, uA, uB, E.CMAP_CALOR, 30, 44,
               'A · UTCI °C · E2 16H', 'B · UTCI °C · E2 16H', 'UTCI · °C',
               'El mapa que resume el proyecto:',
               'en el día caluroso p95 a las 16 h, 3.451 m² salen de la categoría «MUY '
               'FUERTE» (38–46 °C UTCI). El refugio efectivo (ΔUTCI≤−2 K sostenido) '
               'cubre 3.876 m² — 4.377 m² con la nebulización activa.')
doc.metric('CLI04-M2', 3876, 'm²', 'A', 'refugio efectivo sin niebla', 'refugio.json')
doc.metric('CLI04-M3', 4377, 'm²', 'B', 'refugio efectivo con niebla', 'refugio.json')
# barras de categorias por escenario
ax = p.chart_axes(E.MX, y - 1.85, E.A4W - 2 * E.MX, 1.55)
cats = ['MODERADO', 'FUERTE', 'MUY FUERTE']
colores = ['#e9c46a', '#e76f51', '#9d2235']
xs = np.arange(6)
labels = []
vals = {c: [] for c in cats}
for e in ('E1', 'E2', 'E3'):
    for st in ('A', 'B'):
        k = f'{e}_16_{st}'
        cc = R['escenarios'][k]['UTCI_categorias_m2']
        for c in cats:
            vals[c].append(cc.get(c, 0) / 1000)
        labels.append(f'{e} · {st}')
bot = np.zeros(6)
for c, col in zip(cats, colores):
    ax.bar(xs, vals[c], 0.62, bottom=bot, color=col, label=c)
    bot += np.array(vals[c])
ax.set_xticks(xs); ax.set_xticklabels(labels, size=6)
ax.set_ylabel('miles de m²', size=6)
ax.legend(fontsize=5.6, frameon=False, ncol=3, loc='upper right')
p.caption(E.MX, y - 2.0, 'Categorías UTCI a las 16 h por escenario y estado.',
          'Cuanto más duro el día, más área muda de categoría — y más crece también la '
          'cola que empeora (CLI-03). La propuesta rinde más precisamente cuando más se necesita.',
          fuente=FUENTE, wrap=100)
doc.add(p)
doc.close()
print('CLI-04 ok', doc.folio, 'pp')

# ================================================================ CLI-05 · AIRE
doc = E.Doc(os.path.join(OUT, 'CLI-05_AIRE.pdf'), 'CLI-05 · AIRE', '01 · CLIMA')
E.portada(doc, 'Temperatura del aire',
          'Lo que una sombra puede y no puede hacer: el efecto local y el efecto de '
          'conjunto sobre la temperatura del aire de la plaza, con sus hipótesis a la vista.',
          'CLI-05 · CLIMA Y CONFORT',
          [('BASELINE', 'v006 · build 12'),
           ('ΔTA SENSIBLE', '−0,66 K'), ('ΔTA LATENTE', '−0,43 K'),
           ('ΔTA TOTAL', doc.metric('CLI05-M1', '−1,09', 'K', 'B',
            'balance de volumen de control', '_reclima9/aire.json'))], num='CLI-05')
p, y = cabecera_analisis(
    doc, 'CLI-05', 'El aire apenas se entera — y eso es lo esperable',
    '¿Cuánto baja la temperatura DEL AIRE (no la radiante) y por qué es honesto decir que poco?',
    'Balance de volumen de control: sección de 100 m × 10 m de altura de mezcla barrida '
    'por el viento medio; el término sensible retira el flujo de calor que el suelo '
    'sombreado deja de emitir; el latente suma evaporación de agua y vegetación.',
    'aire.json (dH 771 kW, mdot 1.165 kg/s), agua.json, vegetacion.json.', 'B',
    'ESTIMADO de orden de magnitud, no CFD: la advección real depende de la turbulencia '
    'urbana. El propio json declara la hipótesis textualmente.')
y = p.dashlist(E.MX, y, [
    ('El confort NO viene del aire.', 'De la mejora percibida (−2,5 K UTCI), el ~90 % '
     'procede de la radiación (MRT −10,9 K). El aire aporta ~−1,1 K local.'),
    ('Una sombra no refrigera la ciudad.', 'El volumen de aire de Sol se renueva por '
     'viento en decenas de segundos: cualquier promesa de «bajar la temperatura de '
     'Madrid» sería falsa y no se hace.'),
    ('El efecto local es real y medible a posteriori.', 'El plan municipal (10_SINTESIS) '
     'incluye sensores Ta/HR bajo dosel y fuera para validar el −1,1 K estimado.'),
], wrap=86, gap=0.1)
y -= 0.06
y = p.panel(E.MX, y, E.A4W - 2 * E.MX, 1.5, 'DESCOMPOSICIÓN DEL ΔTA (VOLUMEN DE CONTROL · NIVEL B)')
y = p.tabla(E.MX + 0.16, y, E.A4W - 2 * E.MX - 0.32,
            ['TÉRMINO', 'MECANISMO', 'ΔTA'],
            [['Sensible', 'flujo convectivo que el suelo sombreado deja de ceder al aire', '−0,66 K'],
             ['Latente', 'evaporación de láminas de agua + evapotranspiración vegetal (711 kW)', '−0,43 K'],
             ['Total local', 'suma bajo el dosel, con mezcla de 10 m', '−1,09 K']],
            col_w=[1.3, 4.4, 1.0], size=7.4)
doc.add(p)
doc.close()
print('CLI-05 ok', doc.folio, 'pp')
