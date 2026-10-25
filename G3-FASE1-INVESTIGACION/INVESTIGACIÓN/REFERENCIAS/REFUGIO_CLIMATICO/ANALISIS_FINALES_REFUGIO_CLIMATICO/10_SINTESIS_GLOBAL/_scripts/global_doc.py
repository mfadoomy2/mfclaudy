# -*- coding: utf-8 -*-
"""FASE FINAL - REFUGIO_CLIMATICO_ANALISIS_GLOBAL.pdf — informe de viabilidad +
dossier de decision municipal (§29-§32). El documento analitico mas importante."""
import json
import os
import sys

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


def J(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


kpis = J(os.path.join(OUT, 'B_DATOS', 'kpis.json'))
doc = E.Doc(os.path.join(OUT, 'REFUGIO_CLIMATICO_ANALISIS_GLOBAL.pdf'),
            'ANÁLISIS GLOBAL', '10 · SÍNTESIS GLOBAL')

E.portada(doc, 'Refugio Climático\nPuerta del Sol',
          'Análisis global del proyecto sobre la baseline v006: qué se propone, qué se '
          'ha medido, qué funciona, qué no, qué cuesta, qué arriesga y qué aporta. '
          'Informe de viabilidad y dossier de decisión municipal en un solo documento.',
          'ANÁLISIS GLOBAL · DOSSIER DE DECISIÓN',
          [('VEREDICTO', 'VIABLE CON CONDICIONES'),
           ('REFUGIO', '3.876–4.377 m²'), ('ΔUTCI P95', '−2,5 K'),
           ('CAPEX', '8–17 M€ (C)')], num='GLOBAL')

MXW = E.A4W - 2 * E.MX

# ============================================================ 01-02 · QUE + MEDIDO
p = doc.page('01 · QUÉ SE PROPONE')
y = E.A4H - 1.0
y = p.kicker(y, '01 · QUÉ SE PROPONE')
y = p.title(y, 'Una infraestructura de estancia para el peor trimestre', size=16)
y = p.subtitle(y, 'Un dosel estructural de 93 hojas sobre 80 mástiles que produce 4.186 m² '
                  'de sombra nueva; agua evaporativa y nebulización; 17 especies en cuatro '
                  'estratos; una cinta-mirador de 733 m a +6 m con 3 ascensores; y el suelo '
                  'de Sol intacto, público y reversible.')
y = p.kicker(y, '02 · QUÉ SE HA MEDIDO')
y = p.body(E.MX, y, 'El sistema analítico: 279 análisis catalogados (ANALYSIS_MASTER_'
           'REGISTER.csv), 12 módulos de auditoría geométrica, simulación climática física '
           'con 431 posiciones solares y 4 escenarios, motores nuevos de movilidad, agua, '
           'construcción, uso, patrimonio y economía, 18 relaciones cruzadas confirmadas y '
           '15 hallazgos con método científico (DISCOVERIES_REGISTER.md). Tres niveles de '
           'conocimiento en todo el paquete: A medido · B inferido · C escenario.',
           wrap=104, size=8.4)
x = E.MX
p.chip(x, y - 0.05, 'A'); p.chip(x + 1.9, y - 0.05, 'B'); p.chip(x + 3.3, y - 0.05, 'C')
y -= 0.4
# mapa sintesis
dU = E.np_cli('u_E2_16_B.npy') - E.np_cli('u_E2_16_A.npy')
ax = p.axes(E.MX, y - 3.0, 4.5, 2.85)
E.draw_context(ax, geo)
im = E.show_raster(ax, dU, E.CMAP_DELTA, vmin=-6, vmax=6, mask=W)
E.cbar(p, im, E.MX, y - 3.3, 1.7, 'ΔUTCI B−A · K · DÍA P95 16H')
yy = p.ficha(E.MX + 4.85, y - 0.05, [
    ('EL MAPA QUE RESUME TODO', 'Verde: donde la propuesta enfría (hasta −6 K de '
     'sensación). Blanco: sin cambio (el claro central, por diseño). Rojo: los 755 m² '
     'donde empeora — mapeados, explicados (D-001) y con corrección conocida.'),
], wcol=2.6, wrap=36)
doc.add(p)

# ============================================================ 03-04 · FUNCIONA / NO
p = doc.page('03-04 · QUÉ FUNCIONA / QUÉ NO')
y = E.A4H - 1.0
y = p.kicker(y, '03 · QUÉ FUNCIONA (EVIDENCIA)')
y = p.tabla(E.MX, y, MXW, ['AFIRMACIÓN', 'CIFRA', 'NIVEL'],
            [['Refugio térmico efectivo en el peor mes', '3.876 m² (4.377 con niebla) · 36-41 % del pisable', 'A'],
             ['La sensación térmica baja donde importa', 'ΔUTCI −2,5 K medio p95 · −5,9 K en el huerto', 'A'],
             ['3.451 m² salen de la clase «MUY FUERTE» a las 16 h', 'clases UTCI E2, A›B', 'A'],
             ['La red peatonal no se degrada', '0 RED · peor cuello 10,75 m · p95 a salida 63 m', 'A'],
             ['Cero conflicto físico con la ciudad', '0 penetraciones en 35 edificios · 0 obstáculos en bandas de Metro', 'A'],
             ['El sistema se deja mantener', '159/160 puntos técnicos con acceso auditado', 'A'],
             ['Degrada bien: ningún fallo lo devuelve al estado actual', '~66 % del beneficio sobrevive al peor fallo combinado', 'B'],
             ['El tránsito también gana', 'el cruce medio pasa de 2 % a 21 % en sombra', 'B']],
            col_w=[4.2, 2.3, 0.5], size=6.9)
y -= 0.12
y = p.kicker(y, '04 · QUÉ NO FUNCIONA / LIMITACIONES (SIN ESCONDER)')
y = p.tabla(E.MX, y, MXW, ['HECHO INCÓMODO', 'CIFRA', 'ESTADO'],
            [['El invierno pierde sol', '−40,3 % el 21-dic (58 % del suelo conserva ≥½)', 'trade-off gobernado'],
             ['Hay celdas que EMPEORAN, y crecen con el calor', '55›755›1.175 m² en E1›E2›E3', 'mecanismo probado (D-001)'],
             ['El 85 % del calor residual vive sobre los ejes', '4.356 m² a <8 m de un eje', 'mejora identificada (D-015)'],
             ['Quien mejor está, peor ve el reloj', 'visibilidad 41,5›25,5 % en estancia alta', 'miradores cartografiados'],
             ['La cinta no protege a sus usuarios', '22,6 % sombra · UTCI 38,0 °C', 'es mirador, no estancia'],
             ['El viento no está resuelto', 'hasta +0,55 K si abrigo −50 %', 'pendiente CFD/piloto'],
             ['El uso real es incógnita', 'p·h/día 350–9.580 según escenario', 'se valida en piloto'],
             ['Un punto técnico sin acceso', 'BOMBA-1 (159/160)', 'corrección trivial']],
            col_w=[3.6, 2.4, 1.0], size=6.9)
doc.add(p)

# ============================================================ 05-13 · SINTESIS TEMATICAS
p = doc.page('05-13 · SÍNTESIS POR SISTEMA')
y = E.A4H - 1.0
y = p.kicker(y, '05-13 · NUEVE SISTEMAS EN UNA PÁGINA')
y = p.title(y, 'El estado de cada frente', size=16)
y = p.tabla(E.MX, y, MXW, ['SISTEMA', 'VEREDICTO CORTO', 'CIFRA LLAVE', 'DOSSIER'],
            [['05 · Clima', 'SÍ es refugio; no es milagro', '−10,9 K MRT · 36-41 % refugio', '01_CLIMA (11 PDF)'],
             ['06 · Movilidad', 'la plaza sigue fluyendo', '0 RED · LOS A-B incluso a 120k/día', '02_MOVILIDAD (4)'],
             ['07 · Accesibilidad', 'universal a suelo; +6 pende de 3 máquinas', 'N−1: 286 m de rodeo', '02_MOVILIDAD'],
             ['08 · Agua y ecología', 'sostenible con protocolo de sequía', '30,1 m³/día punta · 3,3 días autonomía', '04_AGUA (4)'],
             ['09 · Viabilidad técnica', 'kit repetitivo, mantenible', '15.197 piezas · 12 familias', '05_CONSTRUCCIÓN (3)'],
             ['10 · Operación', 'OPEX = mano de obra, no recurso', '276 k€/año + 0,21 M€ fondo', '07_ECONOMÍA (3)'],
             ['11 · Uso social', 'estancia donde protege', 'IPE alto 90,7 % dentro del refugio', '06_USO_SOCIAL (3)'],
             ['12 · Economía', 'retorno función del uso', '4,9 €/p·h BASE (1,1–29)', '07_ECONOMÍA'],
             ['13 · Patrimonio', 'respeta; coste visual medido', 'reloj 41,5 % · 896 m² miradores', '08_PATRIMONIO (2)']],
            col_w=[1.5, 2.6, 2.0, 0.9], size=6.7)
p.text(E.MX, y - 0.04, 'Cada fila remite a su síntesis temática integrada; cada cifra, a '
       'FINAL_METRICS_REGISTRY.csv.', size=6.2, color=E.GRAYTX)
doc.add(p)

# ============================================================ 14 · INTERACCIONES
p = doc.page('14 · INTERACCIONES')
y = E.A4H - 1.0
y = p.kicker(y, '14 · INTERACCIONES ENTRE SISTEMAS — LA PARTE MÁS IMPORTANTE')
y = p.title(y, 'Lo que solo se ve cruzando', size=16)
y = p.dashlist(E.MX, y - 0.02, [
    ('Las reglas del propio proyecto colisionan — y ahora se sabe dónde.', 'La regla '
     '«corredores despejados» (auditoría A1) mantuvo los ejes libres… y calientes: el '
     '85 % del calor residual vive sobre ellos (D-015). La salida no exige elegir: '
     'sombra ALTA con gálibo ≥3 m satisface ambas reglas. Es la mejora de mayor '
     'palanca del proyecto y está documentada, no implementada.'),
    ('Sombra sin cielo es peor que nada.', 'Las 3.021 celdas que empeoran perdieron '
     'el 53 % de su cielo conservando su sol (D-001). Regla de diseño derivada: cada '
     'elemento alto debe dar sombra o dejar cielo — nunca la media medida.'),
    ('El confort compite con la contemplación.', 'El dosel que produce los −5 K tapa '
     'el reloj (D-003): 896 m² de «miradores» son el recurso escaso a proteger en '
     'ejecución.'),
    ('La inversión social y la climática son la misma.', 'El 90,7 % de la mejor '
     'estancia cae dentro del refugio (D-004): no hay que repartir presupuesto entre '
     '«clima» y «uso» — el mismo euro compra ambos.'),
    ('El mantenimiento ES política climática y de equidad.', 'Los dos componentes de '
     'ciclo corto (cámara de microalgas, niebla) son los de efecto inmediato; los 3 '
     'ascensores son la única puerta PMR del nivel +6. El contrato de conservación '
     'decide más confort que cualquier ajuste de diseño restante.'),
], wrap=88, gap=0.12)
doc.add(p)

# ============================================================ 15-17 · RIESGOS/OPORT/ESCENARIOS
p = doc.page('15-17 · RIESGOS · OPORTUNIDADES · ESCENARIOS')
y = E.A4H - 1.0
y = p.kicker(y, '15 · RIESGOS')
y = p.tabla(E.MX, y, MXW, ['RIESGO', 'PROBABILIDAD', 'IMPACTO', 'MITIGACIÓN'],
            [['Abrigo de viento reduce el beneficio', 'media', 'hasta +0,55 K UTCI', 'CFD / anemometría del piloto'],
             ['Tropicales no sobreviven', 'media', 'estético-ecológico', 'plan B templado sin obra'],
             ['Ascensor crónicamente parado', 'baja-media', 'equidad del +6', 'SLA <48 h; 4º aparato en estudio'],
             ['Sequía decretada', 'media', 'pierde margen fino, no el núcleo', 'protocolo jerárquico (AGU)'],
             ['Uso real < LOW', 'baja', '€/p·h insostenible', 'regla de decisión del piloto'],
             ['Vandalismo (pods, niebla)', 'media', 'OPEX creciente', 'materiales reparables, piezas cortas']],
            col_w=[2.3, 1.1, 1.7, 1.9], size=6.8)
y -= 0.1
y = p.kicker(y, '16 · OPORTUNIDADES')
y = p.dashlist(E.MX, y, [
    ('Sombra alta sobre ejes:', 'ataca el 85 % del calor residual sin tocar una sola regla (D-015).'),
    ('Primer estándar municipal de €/persona-hora:', 'Madrid puede fijar el indicador que otras ciudades copien.'),
    ('Puerta climática del intercambiador:', '73 M de viajeros/año desembocan en la primera sombra del centro.'),
    ('Laboratorio urbano instrumentado:', 'el plan de monitorización convierte Sol en el dataset de confort más rico de España.'),
], wrap=88, gap=0.08)
y -= 0.06
y = p.kicker(y, '17 · ESCENARIOS')
y = p.tabla(E.MX, y, MXW, ['ESCENARIO', 'P·H/TEMPORADA', '€/P·H (25 AÑOS)', 'LECTURA'],
            [['LOW', '33.000', '29 €', 'solo defendible como piloto'],
             ['BASE', '200.000', '4,9 €', 'umbral municipal 8 € cumplido con margen'],
             ['HIGH', '890.000', '1,1 €', 'coste marginal de un helado por hora protegida']],
            col_w=[1.2, 1.8, 1.8, 2.2], size=7.2)
doc.add(p)

# ============================================================ 18 · CONCLUSION GLOBAL
p = doc.page('18 · CONCLUSIÓN GLOBAL')
y = E.A4H - 1.0
y = p.kicker(y, '18 · CONCLUSIÓN GLOBAL')
y = p.title(y, 'Veredicto razonado', size=17)
y = p.dashlist(E.MX, y - 0.02, [
    ('¿Es viable?', 'Técnicamente sí (0 conflictos físicos, kit mantenible, agua '
     'dimensionada); espacialmente sí (la plaza sigue siendo plaza: 0 RED de paso, '
     'suelo 100 % público y reversible); climáticamente sí (el mecanismo dominante es '
     'geometría que no falla); operativamente sí CONDICIONADO a un contrato de '
     'conservación serio (~0,5 M€/año todo incluido); socialmente PROBABLE — es la '
     'única dimensión que exige piloto antes de afirmarse.'),
    ('¿Mejora el confort? ¿Cuánto, dónde, cuándo, para quién?', '−2,5 K de UTCI medio '
     'y −5 a −6 K en los programas de estancia; en el 36-41 % del ámbito; sobre todo de '
     '14 a 19 h de junio a septiembre; para quien espera, cultiva, juega o pasea a '
     'nivel de suelo — no para quien camina la cinta al sol ni, apenas, para quien '
     'cruza en 40 segundos (aunque su cruce pasa de 2 % a 21 % en sombra).'),
    ('¿Qué precio operativo tiene?', '276 k€/año de operación + 0,21 M€/año de fondo '
     'de reposición + 30 m³ de agua el día punta. El coste real es mano de obra: el '
     'refugio es un jardín con máquinas, no una máquina con plantas.'),
    ('¿Qué impactos secundarios podría generar?', 'Pérdida invernal de sol (−40 %, '
     'localizada), reducción de visibilidad del reloj (medida y con miradores '
     'protegibles), posible presión de uso sobre el huerto y concentración de estancia '
     'nocturna — a gestionar, no a temer.'),
    ('¿Qué riesgos quedan y qué necesita validación posterior?', 'Viento (CFD o '
     'anemometría), supervivencia tropical (una temporada), uso real (conteos), '
     'servidumbres administrativas e informe vinculante de Metro. Ninguno es '
     'geométrico: la geometría está cerrada en v006 con 0 RED.'),
    ('¿Qué valor aporta a Puerta del Sol?', 'Convierte el centro simbólico de España '
     '— hoy una plancha de granito con 3,4 % de sombra — en el primer espacio público '
     'del país diseñado, medido y monitorizable como REFUGIO CLIMÁTICO, sin cerrar un '
     'metro de suelo y con cada afirmación de este dossier trazable a un script y una '
     'versión congelada.'),
], wrap=88, gap=0.12)
y -= 0.05
y = p.panel(E.MX, y, MXW, 0.85, 'VEREDICTO GLOBAL DEL PROYECTO')
p.text(E.MX + 0.16, y, 'VIABLE CON CONDICIONES: contrato de conservación desde el día '
       'uno, validación de viento y uso en piloto instrumentado, y las tres correcciones '
       'locales documentadas (BOMBA-1, bancos-mirador, sombra alta de ejes) incorporadas '
       'al proyecto de ejecución. Ninguna condición es una enmienda al proyecto: son su '
       'siguiente iteración natural.', size=8.4, wrap=94)
doc.add(p)

# ============================================================ ROADMAP MUNICIPAL (§32)
p = doc.page('ROADMAP MUNICIPAL')
y = E.A4H - 1.0
y = p.kicker(y, 'ROADMAP MUNICIPAL (§32)')
y = p.title(y, 'Cinco fases del papel a la plaza', size=16)
y = p.tabla(E.MX, y, MXW, ['FASE', 'QUÉ', 'DURACIÓN', 'SALE CON'],
            [['A · VALIDACIONES', 'informe Metro, servidumbres, CFD/túnel de 2 direcciones, licencias', '4-6 meses',
              'lista de condicionantes cerrada'],
             ['B · PROTOTIPO', '1 mástil + 2 hojas + cámara de microalgas + nebulización a escala real en parcela municipal',
              '3-4 meses', 'anemometría, tau real, costes reales de fabricación'],
             ['C · PILOTO', 'cuadrante C1 completo en Sol (mástil, agua, huerto, 1/3 del dosel) instrumentado',
              '1 temporada crítica', 'uso real medido: la variable que decide'],
             ['D · MONITORIZACIÓN', 'sensores fijos + conteos + panel público de datos', 'continua desde C',
              'el dataset que gobierna el despliegue'],
             ['E · DESPLIEGUE', 'resto del dosel + cinta + ascensores, con los ajustes D-001/D-015 incorporados',
              '12-18 meses', 'la plaza completa']],
            col_w=[1.35, 3.3, 1.15, 1.9], size=6.8)
y -= 0.1
y = p.kicker(y, 'QUÉ SE MONITORIZA DESPUÉS DE CONSTRUIR')
y = p.tabla(E.MX, y, MXW, ['VARIABLE', 'INSTRUMENTO', 'FRECUENCIA', 'VALIDA'],
            [['Ta / HR bajo dosel y fuera', '6 parejas de sondas', '10 min', 'CLI-05: el −1,1 K local'],
             ['UTCI (estación biometeorológica)', '2 unidades móviles', 'continua', 'CLI-04 y el ΔUTCI real'],
             ['Viento peatonal', '4 anemómetros', 'continua', 'CLI-08: la incógnita mayor'],
             ['Agua (contadores por circuito)', 'riego/láminas/niebla', 'diaria', 'AGU-01 y el protocolo de sequía'],
             ['Usuarios y permanencia', 'conteo anónimo por visión + aforos F-04', 'horaria', 'SOC-02: personas-hora REALES'],
             ['Mantenimiento e incidencias', 'GMAO municipal con los 160 puntos A9', 'por evento', 'TEC-02 y los SLA'],
             ['Estado vegetal', 'inspección + NDVI estacional', 'mensual', 'AGU-02 y la apuesta tropical']],
            col_w=[1.9, 2.1, 1.0, 2.7], size=6.6)
p.text(E.MX, y - 0.05, 'El proyecto nace instrumentable: convertir Sol en sistema medible '
       'post-ocupación es un entregable, no un accesorio.', size=7.4, color='#4a4a4a')
doc.add(p)
doc.close()
print('GLOBAL ok', doc.folio, 'pp')
