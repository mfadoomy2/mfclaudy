# -*- coding: utf-8 -*-
"""FASE FINAL - REFUGIO_CLIMATICO_ANALISIS_GLOBAL.pdf v2 (mandato de revision §3-§9).

El documento de decision completo: funciona sin abrir los otros 36 PDFs. Una pagina por
sistema con su grafico; NUEVE cadenas interdisciplinares con DATO->HIPOTESIS->
COMPROBACION->CONCLUSION; auditoria de certeza de cada conclusion; FAQ del tecnico
municipal esceptico; renders integrados con funcion declarada cuando existen.
"""
import json
import os
import sys

import matplotlib.image as mpimg
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
RC = os.path.normpath(os.path.join(BASE, '..'))
F9 = os.path.join(RC, 'FASE_03B9_HYPERDETAIL_V006')
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
sys.path.insert(0, os.path.join(BASE, '01_CLIMA_Y_CONFORT', '_scripts'))
import refugio_editorial as E  # noqa: E402
from cli_common import W, geo  # noqa: E402

OUT = os.path.join(BASE, '10_SINTESIS_GLOBAL')
IMG = os.path.join(BASE, '09_RENDERS_Y_REPRESENTACION', '_pipeline', 'refpacks')


def J(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


CROSS = J(os.path.join(OUT, 'B_DATOS', 'global_cross.json'))
KPIS = J(os.path.join(OUT, 'B_DATOS', 'kpis.json'))
CLIS = J(os.path.join(BASE, '01_CLIMA_Y_CONFORT', 'B_DATOS', 'cli_stats.json'))
MOB = J(os.path.join(BASE, '02_MOVILIDAD_Y_ACCESIBILIDAD', 'B_DATOS', 'mob_stats.json'))
AGU = J(os.path.join(BASE, '04_AGUA_ECOLOGIA_Y_VEGETACION', 'B_DATOS', 'agu_stats.json'))
TEC = J(os.path.join(BASE, '05_CONSTRUCCION_ESTRUCTURA_Y_MANTENIMIENTO', 'B_DATOS', 'tec_stats.json'))
SOC = J(os.path.join(BASE, '06_USO_SOCIAL_Y_EXPERIENCIA', 'B_DATOS', 'soc_stats.json'))
ECO = J(os.path.join(BASE, '07_ECONOMIA_OPERACION_Y_ESCENARIOS', 'B_DATOS', 'eco_stats.json'))
PAT = J(os.path.join(BASE, '08_PATRIMONIO_VISUALES_Y_PAISAJE_URBANO', 'B_DATOS', 'pat_stats.json'))
MXW = E.A4W - 2 * E.MX

doc = E.Doc(os.path.join(OUT, 'REFUGIO_CLIMATICO_ANALISIS_GLOBAL.pdf'),
            'ANÁLISIS GLOBAL', '10 · SÍNTESIS GLOBAL')


def render_img(p, y, fn, alto, funcion, cap, wrap=100):
    """Integra un render con su FUNCION declarada; si no existe, no rompe la pagina.
    fn = '<CAM>/<pass>.png' dentro de refpacks/."""
    ruta = os.path.join(IMG, fn)
    if not os.path.exists(ruta):
        return y, False
    ax = p.axes(E.MX, y - alto, MXW, alto)
    ax.imshow(E.load_img_small(ruta), aspect='auto')
    ax.set_xticks([]); ax.set_yticks([])
    p.text(E.MX + 0.06, y - 0.22, funcion, size=6.0, color='white', tracked=True,
           weight='bold')
    yy = p.caption(E.MX, y - alto - 0.08, '', cap + ' · Cycles/OptiX sobre v006 build 12, cámara identificada.',
                   wrap=wrap)
    return yy - 0.05, True


# ================================================================ PORTADA
E.portada(doc, 'Refugio Climático\nPuerta del Sol',
          'El documento de decisión: qué se propone, qué se ha medido sobre la '
          'geometría congelada v006, qué funciona y qué no, qué cuestan sus 25 años, '
          'qué interacciones entre sistemas cambian la lectura y qué debe validar el '
          'Ayuntamiento antes de construir. Autónomo: no exige abrir los otros 36 '
          'documentos del paquete — pero cada cifra remite a ellos.',
          'ANÁLISIS GLOBAL · INFORME DE VIABILIDAD Y DOSSIER DE DECISIÓN',
          [('VEREDICTO', 'VIABLE CON CONDICIONES'),
           ('REFUGIO', '3.876–4.377 m²'), ('ΔUTCI DÍA P95', '−2,5 K'),
           ('CAPEX / OPEX', '8–17 M€ · ~0,5 M€/año')],
          img=os.path.join(IMG, 'H1', 'beauty.png'), num='GLOBAL')

# ================================================================ 00 · RESUMEN EJECUTIVO
p = doc.page('00 · RESUMEN EJECUTIVO')
y = E.A4H - 1.0
y = p.kicker(y, '00 · RESUMEN EJECUTIVO — PARA LEER EN DOS MINUTOS')
y = p.title(y, 'Doce cifras y una decisión', size=17)
x = E.MX
p.bignum(x, y, '3,4›42,3', '%', 'sombra crítica del ámbito, hoy › con refugio'); x += 2.5
p.bignum(x, y, '−10,9', 'K', 'temperatura radiante media (−28 en refugio)'); x += 2.3
p.bignum(x, y, '−2,5', 'K', 'UTCI medio el día caluroso p95')
y -= 1.15
x = E.MX
p.bignum(x, y, '3.876', 'm²', 'refugio efectivo sin niebla (4.377 con)'); x += 2.5
p.bignum(x, y, '0', 'RED', 'incidencias geométricas en la auditoría final'); x += 2.3
p.bignum(x, y, '×12', '', 'sombra del cruce peatonal medio (1,9›23,3 %)')
y -= 1.15
x = E.MX
p.bignum(x, y, '30,1', 'm³/día', 'agua el día punta · autonomía 3,3 días'); x += 2.5
p.bignum(x, y, '11,9', 'M€', 'CAPEX BASE (8,4–16,5) · nivel C'); x += 2.3
p.bignum(x, y, '4,9', '€/p·h', 'coste por persona-hora protegida (BASE, 25 años)')
y -= 1.15
x = E.MX
p.bignum(x, y, '−40,3', '%', 'sol del 21-dic (58 % del suelo conserva ≥½)'); x += 2.5
p.bignum(x, y, '159/160', '', 'puntos de mantenimiento con acceso auditado'); x += 2.3
p.bignum(x, y, '15', '', 'hallazgos con método científico (D-001..D-015)')
y -= 1.2
y = p.panel(E.MX, y, MXW, 1.55, 'LA DECISIÓN EN CUATRO LÍNEAS')
p.text(E.MX + 0.16, y,
       'El proyecto convierte un tercio largo de Puerta del Sol en refugio térmico '
       'medible durante el peor trimestre, sin cerrar suelo público, sin tocar un '
       'edificio y con su mecanismo dominante (sombra estructural) funcionando a coste '
       'operativo cero. Sus costes — sol de invierno, vistas del reloj desde la '
       'estancia, ~0,5 M€/año de conservación — están cuantificados, no escondidos. '
       'Sus incertidumbres — viento, uso real, supervivencia tropical — tienen plan de '
       'validación con regla de decisión explícita (piloto ≥60 % del uso BASE  ›  '
       'despliegue <8 €/p·h). Se recomienda avanzar a FASE A-B del roadmap.',
       size=8.4, wrap=94)
doc.add(p)

# ================================================================ 01 · QUE SE PROPONE
p = doc.page('01 · QUÉ SE PROPONE')
y = E.A4H - 1.0
y = p.kicker(y, '01 · QUÉ SE PROPONE')
y = p.title(y, 'Una infraestructura de estancia para el peor trimestre', size=16)
y = p.subtitle(y, 'Un dosel estructural de 93 hojas sobre 80 mástiles (4.186 m² de '
                  'sombra nueva); agua evaporativa, splash jugable y nebulización; 17 '
                  'especies reales en cuatro estratos; una cinta-mirador de 733 m a '
                  '+6 m con 6 escaleras y 3 ascensores; el suelo de Sol intacto, '
                  'público, reversible.')
y, ok = render_img(p, y, 'H7/beauty.png', 3.6, 'ATMÓSFERA',
                   'La propuesta completa desde el aire: las tres copas, la cinta y el '
                   'claro ceremonial conservado (cámara H7, tarde).')
if not ok:
    ax = p.axes(E.MX, y - 3.4, MXW, 3.3)
    E.draw_context(ax, geo)
    sh = E.np_cli('shade_crit_B.npy')
    im = E.show_raster(ax, sh, E.CMAP_AGUA, vmin=0, vmax=1, mask=W)
    E.cbar(p, im, E.MX, y - 3.7, 1.7, 'SOMBRA CRÍTICA · PROPUESTA')
    y -= 3.9
doc.add(p)

# ================================================================ 02 · QUE SE HA MEDIDO
p = doc.page('02 · QUÉ SE HA MEDIDO')
y = E.A4H - 1.0
y = p.kicker(y, '02 · QUÉ SE HA MEDIDO — EL SISTEMA ANALÍTICO')
y = p.title(y, 'Nada de este dossier es una opinión suelta', size=16)
y = p.dashlist(E.MX, y - 0.02, [
    ('Geometría congelada:', 'baseline v006 build 12, 15.197 mallas, 29 archivos con '
     'hash SHA-256 (BASELINE_SNAPSHOT.json). Ningún resultado mezcla versiones.'),
    ('Auditoría independiente:', '12 módulos (A0-A12) que reconstruyen la escena desde '
     'el generador: anchos, gálibos, colisiones, Metro, vistas, mantenimiento. '
     'Resultado final: 0 RED · 26 YELLOW · 18 GREEN.'),
    ('Clima físico:', '431 posiciones solares reales, balance radiativo completo, UTCI '
     'por celda de 0,5 m, 4 escenarios meteorológicos, k_veg por especie.'),
    ('Motores de la fase final:', 'movilidad (distancias geodésicas, N−1, LOS), agua '
     '(balance diario), construcción (matriz de 160 puntos), uso (índice explícito), '
     'patrimonio (visibilidad ponderada), economía (LOW/BASE/HIGH con fuentes).'),
    ('Trazabilidad:', '279 análisis catalogados; 48 métricas publicadas con script y '
     'página en FINAL_METRICS_REGISTRY.csv; 240+ eventos forenses.'),
], wrap=88, gap=0.1)
y -= 0.06
x = E.MX
p.chip(x, y, 'A'); p.chip(x + 1.95, y, 'B'); p.chip(x + 3.35, y, 'C')
y -= 0.26
p.text(E.MX, y, 'Tres niveles en todo el paquete: A medido/calculado · B inferido por '
       'modelo declarado · C hipótesis/escenario. Regla dura: ningún C se presenta '
       'como hecho — y la conclusión de este documento se audita contra esa escala en '
       'la §18.', size=8.2, wrap=96)
doc.add(p)

# ================================================================ 03-04 (mantengo v1 mejorado)
p = doc.page('03-04 · QUÉ FUNCIONA / QUÉ NO')
y = E.A4H - 1.0
y = p.kicker(y, '03 · QUÉ FUNCIONA (EVIDENCIA)')
y = p.tabla(E.MX, y, MXW, ['AFIRMACIÓN', 'CIFRA', 'NIVEL'],
            [['Refugio térmico efectivo en el peor mes', '3.876 m² (4.377 con niebla) · 36-41 % del ámbito', 'A'],
             ['La sensación térmica baja donde importa', 'ΔUTCI −2,5 K medio p95 · −5,9 K en el huerto', 'A'],
             ['3.451 m² salen de la clase «MUY FUERTE» a las 16 h', 'clases UTCI E2, A›B', 'A'],
             ['La red peatonal no se degrada', '0 RED · peor cuello 10,75 m · p95 a salida 63 m', 'A'],
             ['Cero conflicto físico con la ciudad', '0 penetraciones en 35 edificios · 0 obstáculos en bandas de Metro', 'A'],
             ['El transporte desemboca en el refugio', '4 de 5 bocas salen a 0-3 m del refugio efectivo', 'A'],
             ['El sistema se deja mantener', '159/160 puntos técnicos con acceso auditado', 'A'],
             ['Degrada bien ante fallos', '~66 % del beneficio sobrevive al peor fallo combinado', 'B'],
             ['El tránsito también gana', 'el cruce medio pasa del 1,9 % al 23,3 % en sombra (×12)', 'B']],
            col_w=[4.2, 2.3, 0.5], size=6.8)
y -= 0.12
y = p.kicker(y, '04 · QUÉ NO FUNCIONA / LIMITACIONES (SIN ESCONDER)')
y = p.tabla(E.MX, y, MXW, ['HECHO INCÓMODO', 'CIFRA', 'ESTADO'],
            [['El invierno pierde sol', '−40,3 % el 21-dic (58 % del suelo conserva ≥½)', 'trade-off medido (r=0,71)'],
             ['Hay celdas que EMPEORAN, y crecen con el calor', '55›755›1.175 m² en E1›E2›E3', 'mecanismo probado (D-001)'],
             ['El 85 % del calor residual vive sobre los ejes', '4.356 m² a <8 m de un eje', 'mejora identificada (D-015)'],
             ['Quien mejor está, peor ve el reloj', '41,5 % superficie › 25,5 % estancia alta', 'miradores cartografiados'],
             ['La cinta no protege a sus usuarios', '22,6 % sombra · UTCI 38,0 °C', 'es mirador, no estancia'],
             ['El viento no está resuelto', 'hasta +0,55 K si abrigo −50 %', 'pendiente CFD/piloto'],
             ['El uso real es incógnita', 'p·h/día 350–9.580 según escenario', 'se valida en piloto'],
             ['Un punto técnico sin acceso', 'BOMBA-1 (159/160)', 'corrección trivial']],
            col_w=[3.6, 2.4, 1.0], size=6.8)
doc.add(p)

# ================================================================ 05 · CLIMA (2 pp)
p = doc.page('05 · CLIMA')
y = E.A4H - 1.0
y = p.kicker(y, '05 · CLIMA Y CONFORT')
y = p.title(y, 'El mapa que resume el proyecto', size=16)
dU = E.np_cli('u_E2_16_B.npy') - E.np_cli('u_E2_16_A.npy')
ax = p.axes(E.MX, y - 3.15, 4.7, 3.0)
E.draw_context(ax, geo)
im = E.show_raster(ax, dU, E.CMAP_DELTA, vmin=-6, vmax=6, mask=W)
E.cbar(p, im, E.MX, y - 3.45, 1.7, 'ΔUTCI B−A · K · DÍA P95 16H')
yy = p.ficha(E.MX + 5.0, y - 0.05, [
    ('VERDE', 'donde la propuesta enfría — hasta −6 K de sensación en bancos, huerto y balsas.'),
    ('BLANCO', 'sin cambio: el claro central, por decisión de proyecto (eventos).'),
    ('ROJO', 'los 755 m² que empeoran: pierden el 53 % de su cielo sin ganar sombra (D-001).'),
    ('POR ESCENARIO', 'ΔUTCI −2,8 / −2,5 / −2,0 K en día típico / p95 / ola de calor: rinde más cuanto peor es el día.'),
], wcol=2.5, wrap=34)
p.text(E.MX, y - 3.75, 'FUENTE: _reclima9 v006 build 12 · celda 0,5 m', size=5.4, color=E.GRAYTX)
y = y - 4.05
# clases UTCI barras
ax2 = p.chart_axes(E.MX, y - 1.6, MXW, 1.35)
cats = ['MODERADO', 'FUERTE', 'MUY FUERTE']
colores = ['#e9c46a', '#e76f51', '#9d2235']
xs = np.arange(6)
labels = []
vals = {c: [] for c in cats}
for e_ in ('E1', 'E2', 'E3'):
    for st in ('A', 'B'):
        cc = CLIS['escenarios'][f'{e_}_16_{st}']['UTCI_categorias_m2']
        for c in cats:
            vals[c].append(cc.get(c, 0) / 1000)
        labels.append(f'{e_} · {st}')
bot = np.zeros(6)
for c, col in zip(cats, colores):
    ax2.bar(xs, vals[c], 0.62, bottom=bot, color=col, label=c)
    bot += np.array(vals[c])
ax2.set_xticks(xs); ax2.set_xticklabels(labels, size=6)
ax2.set_ylabel('miles de m²', size=6)
ax2.legend(fontsize=5.6, frameon=False, ncol=3)
p.caption(E.MX, y - 1.8, 'Categorías de estrés UTCI a las 16 h.',
          'En el día p95, 3.451 m² abandonan la clase «MUY FUERTE». La propuesta no '
          'elimina el calor de Madrid: recorta su peor categoría donde la gente se queda.',
          wrap=104)
doc.add(p)

p = doc.page('05 · CLIMA (II) — EVIDENCIA VISUAL')
y = E.A4H - 1.0
y = p.kicker(y, '05 · CLIMA (II) — LA SOMBRA, SIN MAQUILLAJE')
y, ok = render_img(p, y - 0.05, 'H7/clay.png', 3.5, 'EVIDENCIA',
                   'Render CLAY con el sol real de la tarde crítica: cada mancha de '
                   'sombra de esta imagen existe en el ráster shade_crit_B, y viceversa '
                   '(cámara H7, material neutro).')
y, ok2 = render_img(p, y - 0.1, 'F1_INTERIOR_DOSEL/beauty.png', 3.3, 'EXPLICACIÓN',
                    'Debajo de las hojas: la luz filtrada que produce los −28 K de MRT '
                    'del refugio (cámara F1, interior del dosel C1).')
if not (ok or ok2):
    p.text(E.MX, y, '[Los renders de evidencia se integran al completar la campaña '
           'visual: H7_clay y F1_INTERIOR_DOSEL]', size=8, color=E.GRAYTX)
doc.add(p)

# ================================================================ 06-07 · MOVILIDAD + ACCESIBILIDAD
p = doc.page('06 · MOVILIDAD')
y = E.A4H - 1.0
y = p.kicker(y, '06 · MOVILIDAD')
y = p.title(y, 'La plaza sigue fluyendo', size=16)
width = E.np_aud('width.npy'); plaza = E.np_aud('plaza.npy')
ax = p.axes(E.MX, y - 3.0, 4.5, 2.85)
E.draw_context(ax, geo)
im = E.show_raster(ax, np.clip(width, 0, 12), E.CMAP_VERDE, mask=plaza & (width > 0))
E.cbar(p, im, E.MX, y - 3.3, 1.7, 'ANCHURA LIBRE LOCAL · M')
yy = p.ficha(E.MX + 4.8, y - 0.05, [
    ('RED', '0 incidencias rojas de paso; el peor cuello entre los 45 pares de accesos '
     'conserva 10,75 m; a 1,80 m exigidos, el 84 % del suelo sigue en una pieza.'),
    ('EVACUACIÓN', 'distancia geodésica p95 a una salida: 63 m; máximo 101 m; sin '
     'fondos de saco imputables al proyecto.'),
    ('DEMANDA', 'con 120.000 visitantes/día (hipótesis alta), el punto pésimo queda en '
     'LOS A-B: la capacidad no es el límite del proyecto.'),
], wcol=2.7, wrap=36)
y = min(y - 3.55, yy) - 0.1
y = p.kicker(y, '07 · ACCESIBILIDAD')
y = p.tabla(E.MX, y, MXW, ['ESCENARIO PMR (NIVEL +6)', 'RODEO MÁXIMO', 'LECTURA'],
            [['3 ascensores operativos', '174 m', 'servicio pleno'],
             ['Peor fallo N−1 (ASC-3 Este)', '286 m', '~4-5 min PMR: tolerable como avería, no como crónico'],
             ['A nivel de suelo', '0 m', 'accesibilidad universal sin mediación mecánica']],
            col_w=[2.5, 1.4, 3.1], size=7.2)
p.text(E.MX, y - 0.02, 'Condición recomendada: SLA <48 h en el contrato de aparatos y '
       'estudio de 4º ascensor en proyecto de ejecución (MOB-02).', size=7.4,
       color='#4a4a4a', wrap=110)
doc.add(p)

# ================================================================ 08 · AGUA
p = doc.page('08 · AGUA Y ECOLOGÍA')
y = E.A4H - 1.0
y = p.kicker(y, '08 · AGUA Y ECOLOGÍA')
y = p.title(y, 'Treinta metros cúbicos el peor día — y un termostato', size=16)
bal = AGU['balance_dia_punta_m3']
y = p.tabla(E.MX, y, MXW, ['TÉRMINO', 'DÍA PUNTA', 'NIVEL', 'QUÉ COMPRA'],
            [['Evaporación de láminas y splash', '%.1f m³' % bal['evaporacion_laminas'], 'A/B',
              'superficies frías + juego de agua'],
             ['Riego (17 especies, hidrozonas)', '%.1f m³' % bal['riego_vegetal'], 'B',
              '286 kW latentes + ecología + paisaje'],
             ['Nebulización (solo día seco)', '%.2f m³' % bal['nebulizacion'], 'C',
              '+501 m² de refugio; el agua más rentable'],
             ['TOTAL (~12 viviendas)', '%.1f m³' % bal['total'], '—',
              'autonomía 3,3 días con depósitos llenos']],
            col_w=[2.6, 1.0, 0.6, 2.8], size=7.2)
y -= 0.1
y = p.dashlist(E.MX, y, [
    ('El núcleo del confort no bebe:', 'la sombra estructural (−10,9 K) funciona con '
     'los depósitos vacíos. El agua compra el margen fino y se corta por jerarquía: '
     'niebla › láminas › herbáceas › arbustos › NUNCA el arbolado.'),
    ('La apuesta ecológica se declara:', 'las tropicales de sotobosque viven del '
     'microclima del dosel (C); el plan B templado no exige obra. La infraestructura '
     'es agnóstica a la especie.'),
    ('El coste del agua es ruido económico:', '~9 k€/año de consumo frente a 200 k€ de '
     'mano de obra de conservación: el agua es termostato, no talón de Aquiles.'),
], wrap=88, gap=0.1)
doc.add(p)

# ================================================================ 09-10 · TECNICA + OPERACION
p = doc.page('09-10 · TÉCNICA Y OPERACIÓN')
y = E.A4H - 1.0
y = p.kicker(y, '09 · VIABILIDAD TÉCNICA')
y = p.dashlist(E.MX, y - 0.02, [
    ('Kit repetitivo:', '15.197 piezas con nombre en 12 familias; 93 hojas iguales en '
     '3 tamaños, 42 nebulizadores idénticos: almacén corto, cuadrilla formable.'),
    ('Mantenible por diseño:', '160 puntos técnicos georreferenciados con acceso '
     'auditado (159 con acceso; BOMBA-1 con corrección trivial pendiente); red '
     'enterrada con registro cada 9 m: la hidráulica se repara sin levantar la plaza.'),
    ('Reversible:', 'cimentación puntual de mástiles, pavimento conservado bajo las '
     'jardineras, suelo 100 % público las 24 h.'),
], wrap=88, gap=0.1)
y -= 0.08
y = p.kicker(y, '10 · OPERACIÓN Y MANTENIMIENTO')
opx = ECO['opex_kEUR_ano']
y = p.tabla(E.MX, y, MXW, ['PARTIDA', 'LOW', 'BASE', 'HIGH', 'CLAVE'],
            [[o['partida'], str(o['low']), str(o['base']), str(o['high']),
              'sí' if 'ascensor' in o['partida'].lower() or 'microalgas' in o['partida'].lower()
              or 'camara' in o['partida'].lower() or 'membrana' in o['partida'].lower() else '']
             for o in opx['partidas']] +
            [['TOTAL OPEX (k€/año) + fondo reposición %.2f M€' % opx['fondo_reposicion_MEUR_ano'],
              str(opx['total']['low']), str(opx['total']['base']), str(opx['total']['high']), '']],
            col_w=[3.6, 0.65, 0.7, 0.7, 1.35], size=6.8)
p.text(E.MX, y - 0.02, 'Las partidas «clave» concentran el efecto climático inmediato '
       '(cámara de microalgas, membrana) o la equidad (ascensores): son el corazón del '
       'contrato de conservación, no partidas recortables.', size=7.4, color='#4a4a4a',
       wrap=110)
doc.add(p)

# ================================================================ 11-12 · USO + ECONOMIA
p = doc.page('11-12 · USO Y ECONOMÍA')
y = E.A4H - 1.0
y = p.kicker(y, '11 · USO SOCIAL')
ipe = np.load(os.path.join(BASE, '06_USO_SOCIAL_Y_EXPERIENCIA', 'B_DATOS', 'ipe.npy'))
ax = p.axes(E.MX, y - 2.8, 4.3, 2.65)
E.draw_context(ax, geo)
im = E.show_raster(ax, ipe, E.CMAP_VERDE, vmin=0, vmax=0.8)
E.cbar(p, im, E.MX, y - 3.1, 1.7, 'POTENCIAL DE ESTANCIA (IPE) · 0-0,8')
ph = SOC['personas_hora']['escenarios']
yy = p.ficha(E.MX + 4.6, y - 0.05, [
    ('EL ÍNDICE', 'IPE = 0,30 sombra + 0,30 confort + 0,15 asiento + 0,10 agua + 0,15 '
     'borde — fórmula publicada, estable a ±50 % de pesos (Jaccard ≥0,74).'),
    ('EL CRUCE', 'el 90,7 % de la estancia alta cae dentro del refugio: la inversión '
     'social y la climática son la misma.'),
    ('PERSONAS-HORA', 'LOW 350 · BASE 2.160 · HIGH 9.580 al día (C): ~33.000 a '
     '~890.000 por temporada. El piloto convierte esta horquilla en dato.'),
], wcol=2.9, wrap=38)
y = min(y - 3.4, yy) - 0.1
y = p.kicker(y, '12 · ECONOMÍA')
y = p.tabla(E.MX, y, MXW, ['ESCENARIO', 'P·H/TEMPORADA', '€/P·H (25 AÑOS)', 'LECTURA'],
            [['LOW', '33.000', '29 €', 'solo defendible como piloto'],
             ['BASE', '200.000', '4,9 €', 'umbral municipal propuesto (8 €) cumplido con margen'],
             ['HIGH', '890.000', '1,1 €', 'coste marginal de un helado por hora protegida']],
            col_w=[1.1, 1.7, 1.7, 2.6], size=7.2)
p.text(E.MX, y - 0.02, 'El comercio se modela en 3 escenarios (612–6.900 €/día '
       'incrementales, nivel C) y NO se usa para justificar el proyecto: ni el HIGH '
       '«paga» el CAPEX. La justificación es climático-social y así se presenta.',
       size=7.4, color='#4a4a4a', wrap=110)
doc.add(p)

# ================================================================ 13 · PATRIMONIO
p = doc.page('13 · PATRIMONIO')
y = E.A4H - 1.0
y = p.kicker(y, '13 · PATRIMONIO Y VISUALES')
y = p.title(y, 'Tres maneras de medir la misma vista', size=16)
vf = CROSS['visuales_flujo']
ax = p.chart_axes(E.MX, y - 1.7, 4.4, 1.5)
mets3 = [('POR SUPERFICIE', 41.5, '#b9b3aa'), ('POR FLUJO (tránsito)', vf['pct_flujo_con_vista_reloj'], E.AGUA),
         ('POR ESTANCIA ALTA', 25.5, E.GREEN)]
ax.barh(range(3), [m[1] for m in mets3], 0.55, color=[m[2] for m in mets3])
ax.set_yticks(range(3)); ax.set_yticklabels([m[0] for m in mets3], size=6)
ax.set_xlabel('% con vista del reloj', size=6)
for i, m in enumerate(mets3):
    ax.text(m[1] + 0.8, i, '%.1f %%' % m[1], va='center', size=6.5, family=E.SERIF)
yy = p.ficha(E.MX + 4.75, y - 0.05, [
    ('LA LECTURA', 'Quien PASA conserva la vista (48,9 % del flujo); quien SE QUEDA la '
     'pierde (25,5 %). Las dos caras de la misma decisión: los ejes se dejaron '
     'despejados (y con vistas); la estancia se metió bajo el dosel (y sin ellas).'),
    ('LO PROTEGIBLE', '896 m² de «miradores» combinan confort y reloj: recurso escaso '
     'cartografiado para blindarlo en ejecución.'),
    ('LO FÍSICO', '0 penetraciones en 35 edificios; ~2 m de aire a la fachada más '
     'sensible; atrio del Metro tratado como umbral.'),
], wcol=2.75, wrap=36)
y = min(y - 2.1, yy) - 0.15
y, _ = render_img(p, y, 'H4/beauty.png', 3.1, 'COMPARACIÓN',
                  'El corredor visual protegido hacia Casa de Correos: el dosel enmarca '
                  'la torre sin invadirla (cámara H4).')
doc.add(p)

# ================================================================ 14 · INTERACCIONES (nucleo)
CADENAS = [
    ('CLIMA × MOVILIDAD', 'D-015 + cobertura real',
     'DATOS: 85 % del calor residual a <8 m de un eje (spots × trazas) + cobertura del '
     'cruce medio 1,9 › 23,3 % + regla A1 de corredores despejados.',
     'HIPÓTESIS: la regla de paso libre expulsó el dosel de los ejes y con él su sombra.',
     'COMPROBACIÓN: los claros no-eje suman solo el 15 % del calor residual; la sombra '
     'de eje existente procede de hojas ALTAS laterales que no violan gálibos.',
     'CONCLUSIÓN: el beneficio térmico y la demanda peatonal solo coinciden hoy '
     'parcialmente (23 %). La sombra alta (gálibo ≥3 m) sobre ejes es la mejora de '
     'mayor palanca del proyecto — compatible con TODAS las reglas vigentes.', 'DEMOSTRADA (A)'),
    ('CLIMA × ESTANCIA', 'IPE × refugio',
     'DATOS: mapa IPE (fórmula pública) + clases de refugio + zonas de programa.',
     'HIPÓTESIS: el confort se transformará en permanencia donde ya hay razones de estar.',
     'COMPROBACIÓN: el 90,7 % de la estancia alta (IPE≥0,6) cae dentro del REFUGIO '
     'EFECTIVO; bancos/huerto mejoran −5 a −6 K.',
     'CONCLUSIÓN: la conversión confort › permanencia es una co-localización DISEÑADA, '
     'no una esperanza; su magnitud humana exacta queda para el piloto.', 'ROBUSTA (B)'),
    ('AGUA × BENEFICIO', 'litros por kelvin',
     'DATOS: 30,1 m³/día punta por término + beneficios por mecanismo (CLI-05/07).',
     'HIPÓTESIS: no todos los litros enfrían igual.',
     'COMPROBACIÓN: sombra 0 L · niebla 2,5 L/m²·refugio·día · láminas 6,3 L/m²·día · '
     'riego con retorno principalmente ecológico.',
     'CONCLUSIÓN: jerarquía operativa clara; en sequía se corta primero lo más '
     'eficiente por litro (niebla) porque su beneficio es margen, no núcleo — y el '
     'arbolado, irreemplazable a 15 años vista, se protege siempre.', 'ROBUSTA (B)'),
    ('VEGETACIÓN × CLIMA × MANTENIMIENTO', 'la honestidad vegetal',
     'DATOS: sensibilidad LAI ±30 % (±1 p.p. de sombra) + 286 kW latentes + 90 k€/año '
     'de jardinería (mayor partida OPEX).',
     'HIPÓTESIS: la vegetación se justifica por clima.',
     'COMPROBACIÓN: su aporte térmico directo es ~2-8 % del total; su coste, el 33 % '
     'del OPEX.',
     'CONCLUSIÓN: REFUTADA como mecanismo climático principal. La vegetación se '
     'defiende por ecología, experiencia y superficie fría — y así se presenta al '
     'Ayuntamiento. La sequía no colapsa el refugio: degrada su piel.', 'DEMOSTRADA (A/B)'),
    ('METRO × FLUJO × CLIMA', 'la puerta climática',
     'DATOS: 73 M viajeros/año (F-01) + distancia geodésica boca › refugio + sombra del '
     'entorno de salida (cálculo nuevo de este documento).',
     'HIPÓTESIS: el refugio sirve precisamente donde emerge población de transporte.',
     'COMPROBACIÓN: 4 de 5 bocas del ámbito salen a 0-3 m del refugio efectivo; sombra '
     'media del entorno de salida 0,46-0,53 (frente a 0,42 del ámbito); la excepción '
     '(Mayor, 14 m) queda documentada.',
     'CONCLUSIÓN: quien emerge del intercambiador encuentra sombra ANTES que sol. El '
     'atrio es la primera política de calor del transporte público madrileño.', 'DEMOSTRADA (A)'),
    ('VISUALES × FLUJO', 'la tercera métrica',
     'DATOS: visibilidad del reloj por superficie (41,5 %), por estancia (25,5 %) y '
     'por FLUJO (48,9 %, cálculo nuevo sobre las trazas).',
     'HIPÓTESIS: la pérdida patrimonial afecta sobre todo a quien se queda.',
     'COMPROBACIÓN: la vista se conserva mejor en movimiento que en reposo — los '
     'mismos ejes despejados de D-015 preservan los corredores visuales.',
     'CONCLUSIÓN: el proyecto separó papeles sin declararlo: eje = caliente pero con '
     'vistas; estancia = fresca pero sin ellas. La sombra alta de ejes (D-015) deberá '
     'diseñarse ALTA Y ESTRECHA para no repetir en los ejes el conflicto '
     'confort/contemplación.', 'DEMOSTRADA (A)'),
    ('CONFORT × COMERCIO × PERMANENCIA', 'el mecanismo plausible',
     'DATOS: +6-15 min de estancia potencial (SOC) + 13.800 peatones/día en Preciados '
     '(F-03) + modelo de 5 factores (ECO-02).',
     'HIPÓTESIS: confort  ›  permanencia  ›  exposición  ›  gasto.',
     'COMPROBACIÓN: imposible con datos actuales — el modelo produce 612-6.900 €/día '
     'según supuestos. Se diseña la validación (aforos F-04 antes/después del piloto).',
     'CONCLUSIÓN: HIPÓTESIS que permanece hipótesis. El proyecto no se justifica por '
     'comercio y este dossier lo dice explícitamente.', 'HIPÓTESIS (C)'),
    ('BENEFICIO × COMPLEJIDAD OPERATIVA', 'el cuadrante de dependencias',
     'DATOS: aporte al ΔUTCI por mecanismo + dependencias + frecuencia de la matriz '
     'TEC-02.',
     'HIPÓTESIS: el beneficio podría concentrarse en los sistemas más frágiles.',
     'COMPROBACIÓN: es lo contrario — el 85 % del beneficio (sombra) tiene CERO '
     'dependencias; los sistemas frágiles (niebla: agua+bomba+meteo) aportan el margen.',
     'CONCLUSIÓN: arquitectura antifrágil por construcción: los fallos eliminan '
     'refinamientos, nunca el núcleo. Es el argumento de resiliencia central del '
     'dossier.', 'ROBUSTA (A/B)'),
    ('VERANO × INVIERNO', 'el trade-off medido',
     'DATOS: sombra estival ganada y sol invernal perdido, celda a celda (39.000+ '
     'celdas pisables).',
     'HIPÓTESIS: la misma hoja que salva julio roba diciembre.',
     'COMPROBACIÓN: correlación r = 0,71 — el trade-off es fuerte y casi lineal. PERO '
     'existen 271 m² de excepción (mucha sombra estival, poca pérdida invernal): '
     'celdas bajo hojas ALTAS que el sol rasante de invierno esquiva por debajo.',
     'CONCLUSIÓN: el trade-off no es destino: es geometría. Las hojas altas pagan '
     'menos invierno por unidad de verano — otro argumento para la familia de sombra '
     'alta de D-015.', 'DEMOSTRADA (A)'),
]
i = 0
while i < len(CADENAS):
    p = doc.page('14 · INTERACCIONES')
    y = E.A4H - 1.0
    if i == 0:
        y = p.kicker(y, '14 · INTERACCIONES ENTRE SISTEMAS — LA PARTE MÁS IMPORTANTE')
        y = p.title(y, 'Nueve cadenas que ningún análisis individual contiene', size=15)
        y -= 0.05
    for _ in range(4):
        if i >= len(CADENAS):
            break
        tit, sub, dato, hipo, comp, conc, nivel = CADENAS[i]
        p.hline(E.MX, E.A4W - E.MX, y + 0.06, color=E.MAGENTA, lw=1.0)
        p.text(E.MX, y - 0.04, tit, size=9.5, weight='bold')
        p.text(E.A4W - E.MX, y - 0.04, nivel, size=6.2, color=E.GRAYTX, tracked=True,
               ha='right', weight='bold')
        y -= 0.24
        for etiqueta, cuerpo in (('', dato), ('', hipo), ('', comp), ('', conc)):
            y = p.body(E.MX, y, cuerpo, wrap=108, size=7.3)
            y += 0.045
        y -= 0.14
        i += 1
    doc.add(p)
    # pagina llena cada 3 cadenas

# ================================================================ HALLAZGOS EN IMAGEN
p = doc.page('14-BIS · LOS HALLAZGOS EN IMAGEN')
y = E.A4H - 1.0
y = p.kicker(y, '14-BIS · LOS HALLAZGOS CLAVE, CARTOGRAFIADOS')
y = p.title(y, 'D-015 y D-003: los dos mapas que cambian la ejecución', size=15)
# D-015: hotspots sobre ejes
spots = J(os.path.join(F9, '_reclima9', '_data', 'spots.json'))
Mgeo = J(os.path.join(F9, 'geometria_maestra_v006.json'))
ax = p.axes(E.MX, y - 3.05, 3.55, 2.9)
E.draw_context(ax, geo)
sh_ = E.np_cli('shade_crit_B.npy')
E.show_raster(ax, np.where(np.nan_to_num(sh_) > 0.5, 0.35, np.nan), E.CMAP_VERDE,
              vmin=0, vmax=1, mask=W, alpha=0.5)
for c_ in Mgeo['circulacion']['corridors']:
    pts_ = c_.get('pts') or [c_.get('desde'), c_.get('hasta')]
    if pts_ and pts_[0]:
        ax.plot([q[0] for q in pts_], [q[1] for q in pts_], '-', color=E.AGUA, lw=1.4)
for s_ in spots.get('hot', []):
    ax.scatter(s_['x'], s_['y'], s=max(8, s_['m2'] / 28), c='#c22a52', zorder=5,
               edgecolors='white', linewidths=0.4)
p.text(E.MX, y + 0.06, 'D-015 · CALOR RESIDUAL × EJES', size=6.2, tracked=True,
       weight='bold', color=E.GRAYTX)
# D-003: miradores
a7_ = J(os.path.join(F9, '_reaudit9', '_data', 'a7_views.json'))
pts7 = np.array(a7_['pts']); vis7 = np.array(a7_['vis']['RELOJ'], bool)
ipe_ = np.load(os.path.join(BASE, '06_USO_SOCIAL_Y_EXPERIENCIA', 'B_DATOS', 'ipe.npy'))
w7 = np.array([ipe_[int((py - (-45)) / 0.5), int((px - (-112)) / 0.5)]
               if 0 <= int((py - (-45)) / 0.5) < ipe_.shape[0]
               and 0 <= int((px - (-112)) / 0.5) < ipe_.shape[1] else np.nan
               for px, py in pts7])
w7 = np.nan_to_num(w7)
ax2 = p.axes(E.MX + 3.85, y - 3.05, 3.55, 2.9)
E.draw_context(ax2, geo)
ax2.scatter(pts7[~vis7][:, 0], pts7[~vis7][:, 1], s=0.9, c='#ddd6cc')
ax2.scatter(pts7[vis7 & (w7 < 0.5)][:, 0], pts7[vis7 & (w7 < 0.5)][:, 1], s=1.2, c=E.PALEAGUA)
mir7 = vis7 & (w7 >= 0.5)
ax2.scatter(pts7[mir7][:, 0], pts7[mir7][:, 1], s=2.6, c=E.MAGENTA)
ax2.plot(-25.2, -34.35, '*', ms=11, c=E.INK)
p.text(E.MX + 3.85, y + 0.06, 'D-003 · MIRADORES (CONFORT + RELOJ ★)', size=6.2,
       tracked=True, weight='bold', color=E.GRAYTX)
y -= 3.35
p.caption(E.MX, y, 'Izquierda:', 'los 15 focos de calor residual (rojo, tamaño = m²) '
          'pegados a los ejes peatonales (azul); el verde translúcido es la sombra '
          '≥50 %. El 85 % del área caliente vive a <8 m de un eje: la sombra alta con '
          'gálibo ≥3 m es la corrección. Derecha: los 896 m² de mirador (magenta) '
          'donde confort y contemplación del reloj coinciden — recurso escaso a '
          'proteger en ejecución.', wrap=108)
y -= 0.5
# barras: sombra por eje A->B ponderada
ax3 = p.chart_axes(E.MX, y - 1.55, MXW, 1.3)
det = KPIS['cobertura_detalle']
xs3 = np.arange(len(det))
ax3.bar(xs3 - 0.18, [100 * d['sombra_media_A'] for d in det], 0.34, color='#ddd6cc',
        label='hoy (A)')
ax3.bar(xs3 + 0.18, [100 * d['sombra_media_B'] for d in det], 0.34, color=E.GREEN,
        label='propuesta (B)')
ax3.set_xticks(xs3)
ax3.set_xticklabels([d['eje'].replace('-', '\n') for d in det], size=5.4)
ax3.set_ylabel('% de la traza en sombra', size=6)
ax3.legend(fontsize=5.8, frameon=False)
p.caption(E.MX, y - 1.75, 'Cobertura real por eje (sombra media de la traza).',
          'De aquí sale el ×12 del cruce medio (1,9 %  ›  23,3 %, ponderado por flujo, '
          'cinta excluida): preciados-carretas y carmen-correos multiplican ×80 y ×60; '
          'el eje mayor apenas ×4 — el reparto NO es uniforme y el mapa D-015 explica '
          'por qué.', wrap=108)
doc.add(p)

# ================================================================ 15-17
p = doc.page('15-17 · RIESGOS · OPORTUNIDADES · ESCENARIOS')
y = E.A4H - 1.0
y = p.kicker(y, '15 · RIESGOS')
y = p.tabla(E.MX, y, MXW, ['RIESGO', 'PROBABILIDAD', 'IMPACTO', 'MITIGACIÓN'],
            [['Abrigo de viento reduce el beneficio', 'media', 'hasta +0,55 K UTCI', 'CFD / anemometría del piloto'],
             ['Tropicales no sobreviven', 'media', 'estético-ecológico', 'plan B templado sin obra'],
             ['Ascensor crónicamente parado', 'baja-media', 'equidad del +6', 'SLA <48 h; 4º aparato en estudio'],
             ['Sequía decretada', 'media', 'pierde margen fino, no el núcleo', 'protocolo jerárquico (AGU)'],
             ['Uso real < LOW', 'baja', '€/p·h insostenible', 'regla de decisión del piloto'],
             ['Vandalismo (pods, niebla)', 'media', 'OPEX creciente', 'materiales reparables, piezas cortas'],
             ['Cámara de microalgas desatendida', 'media si no hay contrato', '+6,9 K MRT local', 'frecuencia quincenal contractual']],
            col_w=[2.3, 1.15, 1.65, 1.9], size=6.8)
y -= 0.1
y = p.kicker(y, '16 · OPORTUNIDADES')
y = p.dashlist(E.MX, y, [
    ('Sombra alta sobre ejes:', 'ataca el 85 % del calor residual sin tocar una regla; '
     'diseñada alta y estrecha, preserva además los corredores visuales (cadenas 1 y 6).'),
    ('Primer estándar municipal €/persona-hora:', 'Madrid puede fijar el indicador y '
     'su método de medición post-ocupación.'),
    ('Puerta climática del intercambiador:', '4 de 5 bocas ya desembocan en refugio: '
     'la señalética «ruta fresca» es gratis.'),
    ('Laboratorio urbano instrumentado:', 'el plan de monitorización convierte Sol en '
     'el dataset de confort urbano más rico de España.'),
], wrap=88, gap=0.08)
y -= 0.06
y = p.kicker(y, '17 · ESCENARIOS')
y = p.tabla(E.MX, y, MXW, ['ESCENARIO', 'P·H/TEMPORADA', '€/P·H (25 AÑOS)', 'LECTURA'],
            [['LOW', '33.000', '29 €', 'solo defendible como piloto'],
             ['BASE', '200.000', '4,9 €', 'umbral municipal 8 € cumplido con margen'],
             ['HIGH', '890.000', '1,1 €', 'coste marginal de un helado por hora protegida']],
            col_w=[1.2, 1.8, 1.8, 2.2], size=7.2)
doc.add(p)

# ================================================================ FAQ MUNICIPAL ESCEPTICO
p = doc.page('FAQ · TÉCNICO MUNICIPAL ESCÉPTICO')
y = E.A4H - 1.0
y = p.kicker(y, 'FAQ · LAS PREGUNTAS DE UN TÉCNICO ESCÉPTICO')
y = p.title(y, 'Once ataques y sus respuestas trazables', size=15)
FAQ = [
    ('¿De dónde sale cada cifra?', 'De FINAL_METRICS_REGISTRY.csv: 48 métricas con '
     'script, dato de origen, nivel A/B/C y página. Cero cifras huérfanas; 0 conflictos '
     'en el test de consistencia.'),
    ('¿Qué depende de una hipótesis?', 'Todo lo marcado C: afluencias, CAPEX, comercio, '
     'abrigo de viento, supervivencia tropical. Está listado en §04 y §18 y NUNCA '
     'se cita como hecho.'),
    ('¿Qué ocurre si falla el agua?', 'Se pierden −0,43 K de aire y la niebla '
     '(−501 m² de refugio); la sombra (−10,9 K MRT) no se entera. Autonomía 3,3 días '
     'punta con depósitos. CLI-10 + AGU-01.'),
    ('¿Y si falla un ascensor?', 'Peor caso N−1: 286 m de rodeo PMR sobre la cinta '
     '(los 3 medidos uno a uno). Condición: SLA <48 h. A nivel de suelo no hay '
     'dependencia mecánica alguna. MOB-02.'),
    ('¿Qué mantenimiento exige?', 'Matriz de 12 componentes con frecuencia y vida '
     'útil; 160 puntos de acceso auditados (159 OK, 1 con corrección trivial); '
     '~0,5 M€/año todo incluido con fondo de reposición. TEC-02 + ECO-01.'),
    ('¿Es accesible?', 'Suelo: universal, 0 RED de paso, evacuación p95 63 m. '
     'Nivel +6: solo por ascensor (3 uds) — la única asimetría reconocida del '
     'proyecto. MOB-01/02.'),
    ('¿Entorpece el Metro?', 'No: 0 obstáculos en las bandas de respeto de todas las '
     'bocas; 4 de 5 salen directamente al refugio. Falta el informe VINCULANTE de '
     'Metro de Madrid: fase A del roadmap. URB-01.'),
    ('¿Qué pasa en invierno?', 'Se pierde el 40,3 % del sol del 21-dic; el 58 % del '
     'suelo conserva ≥ la mitad; el trade-off es lineal (r=0,71) y su excepción '
     '(hojas altas) está identificada. La ponderación final es política, con los '
     'números encima de la mesa. CLI-01.'),
    ('¿Qué beneficio cuantificable produce?', '3.876-4.377 m² de refugio; 3.451 m² '
     'fuera de la clase UTCI «MUY FUERTE» a las 16 h; 33.000-890.000 personas-hora '
     'protegidas por temporada (horquilla honesta); a 4,9 €/p·h en BASE.'),
    ('¿Qué riesgos siguen sin resolver?', 'Viento (acotado ±0,55 K, pendiente CFD), '
     'uso real (piloto), tropicales (una temporada), tramitación (Metro, servidumbres, '
     'patrimonio). Ninguno es geométrico. §15.'),
    ('¿Qué tendría que verificar el Ayuntamiento antes de construir?', 'Fase A: '
     'informe Metro + servidumbres + CFD. Fase B: prototipo 1 mástil (anemometría, '
     'tau real, costes). Fase C: piloto de un cuadrante UNA temporada con la regla de '
     'decisión ≥60 % del uso BASE. Solo entonces, despliegue. Roadmap completo en la '
     'página siguiente.'),
]
for q, a in FAQ:
    yq = p.rich(E.MX, y, q, '', wrap=108, size=7.8)
    y = p.body(E.MX + 0.18, yq + 0.06, a, wrap=100, size=7.2)
    y += 0.02
    if y < 1.3 and (q, a) != FAQ[-1]:
        doc.add(p)
        p = doc.page('FAQ · TÉCNICO MUNICIPAL ESCÉPTICO')
        y = E.A4H - 1.0
doc.add(p)

# ================================================================ 18 · CONCLUSION + CERTEZA
p = doc.page('18 · CONCLUSIÓN GLOBAL')
y = E.A4H - 1.0
y = p.kicker(y, '18 · CONCLUSIÓN GLOBAL — LAS NUEVE RESPUESTAS')
y = p.dashlist(E.MX, y - 0.02, [
    ('QUÉ MEJORA:', 'la habitabilidad estival del centro simbólico de Madrid: de '
     'plancha de granito (3,4 % de sombra) a refugio de estancia con agua, huerto y '
     'mirador.'),
    ('CUÁNTO:', '−2,5 K de UTCI medio y −5/−6 K en estancia el día p95; 36-41 % del '
     'ámbito en refugio efectivo; el cruce medio ×12 en sombra; 3.451 m² fuera de la '
     'peor clase de estrés.'),
    ('MEDIANTE QUÉ MECANISMOS:', '~85 % sombra estructural (gratis en operación), '
     '~10 % agua evaporativa, ~5 % niebla condicional; la vegetación aporta ecología y '
     'superficie, no el parasol.'),
    ('QUIÉNES SE BENEFICIAN MÁS:', 'quien espera, cultiva, juega o pasea a nivel de '
     'suelo — y quien emerge del Metro: 4 de 5 bocas salen al refugio. Menos: quien '
     'camina la cinta al sol y quien busca sol de invierno bajo las hojas.'),
    ('QUÉ TRADE-OFFS INTRODUCE:', 'invierno −40,3 % (r=0,71, excepción cartografiada); '
     'reloj 41,5›25,5 % desde la estancia (miradores protegibles); 755 m² que empeoran '
     'con mecanismo probado y corrección conocida.'),
    ('QUÉ DEPENDENCIAS OPERATIVAS:', 'contrato de conservación (~0,5 M€/año) con dos '
     'frecuencias sagradas (cámara quincenal, boquillas trimestral) y SLA de '
     'ascensores; agua como margen, nunca como núcleo.'),
    ('QUÉ SIGUE SIENDO INCIERTO:', 'viento (±0,55 K), uso real (350-9.580 p·h/día), '
     'tropicales, CAPEX (±40 %), tramitación administrativa.'),
    ('QUÉ VALIDAR EN FASE MUNICIPAL:', 'las cuatro incertidumbres anteriores, en ese '
     'orden, con el roadmap A-E y la monitorización de 7 variables ya especificada.'),
    ('POR QUÉ RESULTA VIABLE:', 'porque su núcleo es geometría que no falla, sus '
     'costes están contados a 25 años, sus fallos degradan sin colapsar, su encaje '
     'físico es limpio (0 RED, 0 penetraciones) y sus incógnitas tienen precio de '
     'validación (~un prototipo y una temporada de piloto) muy inferior al coste de '
     'equivocarse construyendo — o de no construir nada mientras Madrid suma olas de '
     'calor.'),
], wrap=88, gap=0.11)
doc.add(p)

p = doc.page('18 · AUDITORÍA DE CERTEZA')
y = E.A4H - 1.0
y = p.kicker(y, '18-BIS · AUDITORÍA DE CERTEZA DE LAS CONCLUSIONES (§7)')
y = p.title(y, 'Qué afirmamos y con cuánta fuerza', size=15)
y = p.tabla(E.MX, y, MXW, ['CONCLUSIÓN', 'CLASIFICACIÓN', 'LENGUAJE USADO'],
            [['El refugio térmico existe y su magnitud', 'DEMOSTRADA', 'indicativo («es», «cubre»)'],
             ['0 conflictos físicos con la ciudad', 'DEMOSTRADA', 'indicativo'],
             ['Mecanismo de la cola positiva (cielo sin sombra)', 'DEMOSTRADA', 'indicativo con prueba citada'],
             ['85 % del calor residual sobre ejes + salida sombra alta', 'DEMOSTRADA / ROBUSTA', 'indicativo + condicional en la mejora'],
             ['Degradación benigna ante fallos', 'ROBUSTA', '«conserva ~2/3» con nivel B visible'],
             ['Estancia seguirá al confort (90,7 % co-localización)', 'ROBUSTA', '«potencial», «diseñada» — nunca «ocurrirá»'],
             ['Personas-hora protegidas', 'INDICATIVA', 'horquilla completa 350-9.580, siempre'],
             ['CAPEX/OPEX', 'INDICATIVA', '«orden de magnitud», rangos, «no es presupuesto»'],
             ['Efecto comercial', 'HIPÓTESIS', '«plausible», «no justifica el proyecto»'],
             ['Abrigo de viento', 'PENDIENTE DE VALIDACIÓN', '«limitación declarada», cota dura publicada'],
             ['Supervivencia tropical', 'PENDIENTE DE VALIDACIÓN', '«apuesta condicionada», plan B explícito']],
            col_w=[3.3, 1.75, 1.95], size=6.8)
p.text(E.MX, y - 0.04, 'Regla verificada en todo el documento: el verbo nunca es más '
       'fuerte que el nivel. Donde diga «es», hay dato A; donde diga «podría», hay C.',
       size=7.4, color='#4a4a4a', wrap=110)
doc.add(p)

# ================================================================ ROADMAP + MONITORIZACION
p = doc.page('ROADMAP MUNICIPAL')
y = E.A4H - 1.0
y = p.kicker(y, 'ROADMAP MUNICIPAL (§32)')
y = p.title(y, 'Cinco fases del papel a la plaza', size=16)
y = p.tabla(E.MX, y, MXW, ['FASE', 'QUÉ', 'DURACIÓN', 'SALE CON'],
            [['A · VALIDACIONES', 'informe vinculante Metro, servidumbres, CFD 2 direcciones, patrimonio', '4-6 meses',
              'lista de condicionantes cerrada'],
             ['B · PROTOTIPO', '1 mástil + 2 hojas + cámara + niebla a escala real en parcela municipal',
              '3-4 meses', 'anemometría, tau real, costes reales'],
             ['C · PILOTO', 'cuadrante C1 completo en Sol, instrumentado, una temporada crítica',
              '1 temporada', 'USO REAL: la variable que decide (regla ≥60 % BASE)'],
             ['D · MONITORIZACIÓN', 'sensores fijos + conteos + panel público de datos', 'continua desde C',
              'el dataset que gobierna el despliegue'],
             ['E · DESPLIEGUE', 'resto del dosel + cinta + ascensores, con D-001/D-015 incorporados',
              '12-18 meses', 'la plaza completa']],
            col_w=[1.35, 3.3, 1.15, 1.9], size=6.8)
y -= 0.1
y = p.kicker(y, 'QUÉ SE MONITORIZA DESPUÉS DE CONSTRUIR')
y = p.tabla(E.MX, y, MXW, ['VARIABLE', 'INSTRUMENTO', 'FRECUENCIA', 'VALIDA'],
            [['Ta / HR bajo dosel y fuera', '6 parejas de sondas', '10 min', 'CLI-05: el −1,1 K local'],
             ['UTCI (estación biometeorológica)', '2 unidades móviles', 'continua', 'CLI-04 y el ΔUTCI real'],
             ['Viento peatonal', '4 anemómetros', 'continua', 'CLI-08: la incógnita mayor'],
             ['Agua (contadores por circuito)', 'riego/láminas/niebla', 'diaria', 'AGU-01 y el protocolo de sequía'],
             ['Usuarios y permanencia', 'conteo anónimo + aforos F-04', 'horaria', 'SOC-02: personas-hora REALES'],
             ['Mantenimiento e incidencias', 'GMAO con los 160 puntos A9', 'por evento', 'TEC-02 y los SLA'],
             ['Estado vegetal', 'inspección + NDVI estacional', 'mensual', 'AGU-02 y la apuesta tropical']],
            col_w=[1.9, 2.1, 1.0, 2.7], size=6.6)
p.text(E.MX, y - 0.05, 'El proyecto nace instrumentable: convertir Sol en sistema '
       'medible post-ocupación es un entregable, no un accesorio.', size=7.4,
       color='#4a4a4a')
doc.add(p)
doc.close()
print('GLOBAL v2 ok', doc.folio, 'pp')
