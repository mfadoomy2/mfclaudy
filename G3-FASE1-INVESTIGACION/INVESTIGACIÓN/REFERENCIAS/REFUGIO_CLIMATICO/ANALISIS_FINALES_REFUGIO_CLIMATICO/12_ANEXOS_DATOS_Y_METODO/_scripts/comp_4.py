# -*- coding: utf-8 -*-
"""COMPENDIO parte 4: LO QUE SOLO SE VE AL FINAL — indicadores cruzados, matriz de
relaciones, los 15 hallazgos integros, las 9 cadenas de causalidad, la auditoria de
certeza, el interrogatorio municipal, las conclusiones y el roadmap. Mas anexos."""
import io
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from comp_core import (Comp, E, AU, CL, BD, MET, MXW, BASE, SYS, geo, DISC, C)  # noqa: E402

W = E.np_aud('walk.npy')[::2, ::2].astype(bool)
ny, nx = E.np_cli('u_E2_16_B.npy').shape
W = W[:ny, :nx]
OUT = os.path.join(BASE, '12_ANEXOS_DATOS_Y_METODO', '_partes')
c = Comp(os.path.join(OUT, 'p4.pdf'), 'COMPENDIO ANALÍTICO', 'XI · SÍNTESIS')
KP = BD['kpis']
CROSS = BD['global_cross']
CS = BD['cli_stats']

# ============================================================ XI.0 · PORTADILLA
c.seccion('XI · LO QUE SOLO SE VE AL FINAL',
          'Indicadores cruzados, causalidades y conclusiones', size=18,
          sub='Las partes anteriores midieron sistemas por separado. Esta parte los lee '
              'juntos: primero indicadores que ningún análisis individual podía dar, '
              'después la matriz de qué se relaciona con qué, después los quince '
              'hallazgos del barrido de descubrimiento, después las nueve cadenas de '
              'causalidad, y por último las conclusiones y el veredicto.')

# ============================================================ XI.1 · INDICADORES NUEVOS
c.seccion('XI.1 · INDICADORES CRUZADOS', 'Siete métricas que nacen de la división',
          nueva=True)
c.texto('Un indicador cruzado no es una cifra más: es una división entre dos disciplinas. '
        'Cuando se divide el beneficio climático por el suelo ocupado, por el litro '
        'consumido o por la hora de mantenimiento, aparecen preguntas que ni el clima ni '
        'la economía podían formular solos.')
rows = [[k['nombre'][:34], k['formula'][:52], str(k['valor']), k.get('unidad', '')[:12],
         k['nivel'], k['lectura'][:88]] for k in KP['kpis']]
c.tabla(['INDICADOR', 'FÓRMULA', 'VALOR', 'UNIDAD', 'C', 'LECTURA'], rows,
        [1.45, 1.85, 0.55, 0.6, 0.25, 2.3], size=5.8, row_h=0.26,
        titulo='XI.1.1 · LOS SIETE INDICADORES CRUZADOS')
det = KP['cobertura_detalle']
c.espacio(1.9)
ax = c.p.chart_axes(E.MX, c.y - 1.5, MXW, 1.3)
xs = np.arange(len(det))
ax.bar(xs - 0.18, [100 * d['sombra_media_A'] for d in det], 0.34, color='#ddd6cc', label='hoy (A)')
ax.bar(xs + 0.18, [100 * d['sombra_media_B'] for d in det], 0.34, color=E.GREEN, label='propuesta (B)')
ax.set_xticks(xs); ax.set_xticklabels([d['eje'].replace('-', '\n') for d in det], size=5.4)
ax.set_ylabel('% de la traza en sombra', size=6)
ax.legend(fontsize=5.8, frameon=False)
c.y -= 1.7
c.p.caption(E.MX, c.y, 'Cobertura real de tránsito por eje.',
            'El peatón medio pasa del 1,9 % al 23,3 % de su cruce en sombra (×12, '
            'ponderado por flujo y excluyendo la cinta, que es ruta de tablero). El '
            'reparto NO es uniforme: preciados-carretas y carmen-correos multiplican por '
            'setenta y ocho y por sesenta; el eje mayor apenas por cuatro.', wrap=106)
c.y -= 0.42

# ============================================================ XI.2 · MATRIZ
c.seccion('XI.2 · MATRIZ DE RELACIONES', 'Qué influye sobre qué')
try:
    CM = C(SYS, 'CROSS_ANALYSIS_MATRIX.csv')
    cols = list(CM[0].keys())
    dom = cols[0]
    rows = [[r[dom][:20]] + [str(r[k])[:3] for k in cols[1:]] for r in CM]
    c.tabla([dom.upper()[:18]] + [k[:9].upper() for k in cols[1:]], rows,
            [1.5] + [(MXW - 1.5) / max(1, len(cols) - 1)] * (len(cols) - 1), size=5.4,
            titulo='XI.2.1 · MATRIZ COMPLETA (R relación · P posible · — no relacionado)',
            fuente='FUENTE: 00_SISTEMA_Y_FUENTES/CROSS_ANALYSIS_MATRIX.csv')
except Exception as ex:
    c.texto('[matriz: %s]' % ex)

# ============================================================ XI.3 · HALLAZGOS
c.seccion('XI.3 · LOS QUINCE HALLAZGOS', 'Barrido de descubrimiento con método científico')
c.texto('Antes de escribir una sola conclusión se hizo un barrido sobre todos los datos '
        'juntos buscando correlaciones, contradicciones, umbrales y zonas donde varias '
        'virtudes o varios problemas coinciden. Cada hallazgo siguió el mismo método: '
        'observación, hipótesis, prueba, resultado, confianza y consecuencia de proyecto. '
        'Los que podían falsarse, se intentaron falsar — y uno de ellos, el papel climático '
        'de la vegetación, quedó REFUTADO respecto a la intuición inicial.')
blocks = re.split(r'\n## ', DISC)
for b in blocks[1:]:
    lines = [l for l in b.strip().split('\n') if l.strip()]
    if not lines:
        continue
    tit = lines[0].strip()
    c.espacio(1.5)
    c.p.hline(E.MX, E.A4W - E.MX, c.y + 0.06, color=E.MAGENTA, lw=1.0)
    c.p.text(E.MX, c.y - 0.04, tit[:96], size=8.6, weight='bold')
    c.y -= 0.26
    for l in lines[1:]:
        s = l.strip().lstrip('- ').replace('**', '')
        if not s:
            continue
        c.espacio(0.4)
        c.y = c.p.body(E.MX + 0.14, c.y, s, wrap=112, size=6.9) + 0.01
    c.y -= 0.10

# ============================================================ XI.4 · CADENAS
CADENAS = [
    ('CLIMA × MOVILIDAD', 'DEMOSTRADA (A)',
     'DATOS: el 85 % del calor residual está a menos de 8 m de un eje peatonal; la '
     'cobertura de sombra del cruce medio es del 23,3 %; la regla A1 de la auditoría exige '
     'corredores despejados.',
     'HIPÓTESIS: la regla que garantiza el paso expulsó el dosel de los ejes, y con él su '
     'sombra — es decir, el propio criterio de calidad peatonal creó el problema térmico.',
     'COMPROBACIÓN: los claros que no son eje suman solo el 15 % del calor residual; y la '
     'poca sombra que hoy tienen los ejes procede de hojas ALTAS laterales que no violan '
     'ningún gálibo.',
     'CONCLUSIÓN: beneficio térmico y demanda peatonal solo coinciden parcialmente. La '
     'sombra alta sobre ejes, con gálibo mayor de 3 m, es la mejora de mayor palanca del '
     'proyecto y es compatible con TODAS las reglas vigentes. Se documenta; no se '
     'implementa en esta fase.'),
    ('CLIMA × ESTANCIA', 'ROBUSTA (B)',
     'DATOS: mapa de potencial de estancia con fórmula publicada; clases de refugio '
     'térmico; zonas de programa medidas.',
     'HIPÓTESIS: el confort se convertirá en permanencia allí donde ya existan razones '
     'para quedarse.',
     'COMPROBACIÓN: el 90,7 % de la superficie de estancia alta cae dentro del refugio '
     'efectivo; bancos y huerto mejoran entre 5 y 6 K de sensación.',
     'CONCLUSIÓN: la conversión de confort en permanencia es una co-localización DISEÑADA, '
     'no una esperanza. Su magnitud humana exacta sigue siendo incógnita hasta el piloto.'),
    ('AGUA × BENEFICIO', 'ROBUSTA (B)',
     'DATOS: 30,1 m³ en el día punta desglosados por término; beneficio climático de cada '
     'mecanismo por separado.',
     'HIPÓTESIS: no todos los litros compran el mismo confort.',
     'COMPROBACIÓN: la sombra cuesta 0 litros; la nebulización unos 2,5 L por m² de '
     'refugio y día; las láminas unos 6,3 L por m² y día; el riego tiene retorno '
     'principalmente ecológico y paisajístico.',
     'CONCLUSIÓN: existe una jerarquía operativa clara para la sequía, y es contraintuitiva: '
     'se corta primero lo más eficiente por litro (la niebla), porque su beneficio es '
     'margen y no núcleo; y se protege siempre el arbolado, cuyo capital tarda quince años '
     'en reponerse.'),
    ('VEGETACIÓN × CLIMA × MANTENIMIENTO', 'DEMOSTRADA / REFUTADA (A-B)',
     'DATOS: sensibilidad al LAI de ±30 % con efecto de ±1 punto porcentual en sombra; '
     '286 kW de calor latente; 90 k€/año de jardinería, la mayor partida del OPEX.',
     'HIPÓTESIS (la intuición de partida): la vegetación es el mecanismo climático del '
     'refugio.',
     'COMPROBACIÓN: su aporte térmico directo está entre el 2 y el 8 % del total, mientras '
     'consume un tercio del presupuesto anual de conservación.',
     'CONCLUSIÓN: hipótesis REFUTADA como mecanismo principal. La vegetación se defiende '
     'por ecología, experiencia y superficie fría — y así debe presentarse al Ayuntamiento, '
     'sin venderla como parasol. La consecuencia positiva: una sequía no colapsa el '
     'refugio, degrada su piel.'),
    ('METRO × FLUJO × CLIMA', 'DEMOSTRADA (A)',
     'DATOS: 73 millones de viajeros anuales en la estación; distancia geodésica de cada '
     'boca al primer refugio efectivo; sombra del entorno de salida.',
     'HIPÓTESIS: el refugio sirve precisamente donde emerge población procedente del '
     'transporte público.',
     'COMPROBACIÓN: cuatro de las cinco bocas del ámbito salen a entre 0 y 3 metros del '
     'refugio efectivo, con sombra media del entorno de 0,46 a 0,53 frente al 0,42 del '
     'ámbito; la excepción, Mayor, queda a 14 m y documentada.',
     'CONCLUSIÓN: quien emerge del intercambiador encuentra sombra ANTES que sol. El atrio '
     'se convierte, sin haberlo buscado explícitamente, en la primera política de calor '
     'del transporte público madrileño.'),
    ('VISUALES × FLUJO', 'DEMOSTRADA (A)',
     'DATOS: visibilidad del reloj medida de tres maneras — 41,5 % por superficie, 48,9 % '
     'por flujo peatonal y 25,5 % desde la estancia de alto potencial.',
     'HIPÓTESIS: la pérdida patrimonial afecta sobre todo a quien se queda, no a quien pasa.',
     'COMPROBACIÓN: la vista se conserva mejor en movimiento que en reposo, y por la misma '
     'razón geométrica que produce el calor residual de la cadena 1: los ejes se dejaron '
     'despejados.',
     'CONCLUSIÓN: el proyecto separó papeles sin declararlo — eje caliente con vistas, '
     'estancia fresca sin ellas. Consecuencia de diseño: la sombra alta de ejes deberá ser '
     'ALTA Y ESTRECHA para no trasladar a los ejes el conflicto confort-contemplación.'),
    ('CONFORT × COMERCIO × PERMANENCIA', 'HIPÓTESIS (C)',
     'DATOS: entre 6 y 15 minutos de estancia adicional potencial; 13.800 peatones diarios '
     'en Preciados según fuente citada; modelo de cinco factores.',
     'HIPÓTESIS: más confort produce más permanencia, más permanencia produce más '
     'exposición comercial y más exposición produce más gasto.',
     'COMPROBACIÓN: imposible con los datos disponibles. El modelo produce entre 612 y '
     '6.900 € diarios incrementales según los supuestos que se elijan — un rango de más de '
     'diez veces que invalida cualquier afirmación.',
     'CONCLUSIÓN: la hipótesis permanece hipótesis. El proyecto NO se justifica por su '
     'efecto comercial y este dossier lo dice explícitamente. La validación se diseña: '
     'aforos antes y después del piloto.'),
    ('BENEFICIO × COMPLEJIDAD OPERATIVA', 'ROBUSTA (A-B)',
     'DATOS: aporte de cada mecanismo al ΔUTCI; número de dependencias externas de cada '
     'uno; frecuencia de mantenimiento de la matriz técnica.',
     'HIPÓTESIS (el riesgo temido): que el beneficio se concentre en los sistemas más '
     'frágiles, que es el patrón habitual de fracaso de estos proyectos.',
     'COMPROBACIÓN: ocurre exactamente lo contrario. El 85 % del beneficio procede de la '
     'sombra estructural, que tiene CERO dependencias; los sistemas frágiles —niebla, que '
     'necesita agua, bomba de alta presión y meteorología favorable— aportan el margen.',
     'CONCLUSIÓN: la arquitectura es antifrágil por construcción. Los fallos eliminan '
     'refinamientos, nunca el núcleo. Es el argumento central de resiliencia del dossier y '
     'la razón por la que el veredicto puede ser favorable pese a las incertidumbres.'),
    ('VERANO × INVIERNO', 'DEMOSTRADA (A)',
     'DATOS: sombra estival ganada y fracción de sol invernal perdida, celda a celda, sobre '
     'más de 39.000 celdas pisables.',
     'HIPÓTESIS: la misma hoja que salva julio roba diciembre — el trade-off sería '
     'inevitable y proporcional.',
     'COMPROBACIÓN: la correlación es r = 0,71, fuerte y casi lineal, lo que confirma el '
     'trade-off. PERO existen 271 m² de excepción: celdas con mucha sombra estival y poca '
     'pérdida invernal, situadas bajo hojas ALTAS que el sol rasante de diciembre esquiva '
     'por debajo.',
     'CONCLUSIÓN: el trade-off no es destino, es geometría. Las hojas altas pagan menos '
     'invierno por unidad de verano — tercer argumento independiente a favor de la misma '
     'familia de sombra alta que proponen las cadenas 1 y 6.'),
]
c.seccion('XI.4 · CADENAS DE CAUSALIDAD', 'Nueve razonamientos que ningún capítulo contiene')
c.texto('Una cadena no es un resumen: es un razonamiento que empieza en datos de dos o más '
        'disciplinas, formula una hipótesis explícita, la somete a comprobación y termina '
        'en una consecuencia de proyecto. Tres de las nueve convergen, por caminos '
        'independientes, en la misma recomendación.')
for tit, nivel, dato, hipo, comp, conc in CADENAS:
    c.espacio(2.2)
    c.p.hline(E.MX, E.A4W - E.MX, c.y + 0.06, color=E.MAGENTA, lw=1.1)
    c.p.text(E.MX, c.y - 0.04, tit, size=9.8, weight='bold')
    c.p.text(E.A4W - E.MX, c.y - 0.04, nivel, size=6.2, color=E.GRAYTX, tracked=True,
             ha='right', weight='bold')
    c.y -= 0.26
    for cuerpo in (dato, hipo, comp, conc):
        c.espacio(0.5)
        c.y = c.p.body(E.MX, c.y, cuerpo, wrap=110, size=7.2) + 0.03
    c.y -= 0.13

# ============================================================ XII · CONCLUSIONES
c.seccion('XII · CONCLUSIONES', 'Las nueve respuestas', size=18,
          sub='Un dossier de decisión debe responder nueve preguntas sin escurrirse. Estas '
              'son las respuestas, con el nivel de certeza que cada una admite.')
NUEVE = [
    ('QUÉ MEJORA', 'La habitabilidad estival del centro simbólico de Madrid: una plancha '
     'de granito con un 3,4 % de sombra crítica se convierte en un refugio de estancia con '
     'agua, huerto, jardín y mirador, manteniendo intacto el suelo público.'),
    ('CUÁNTO', 'Un descenso de 2,5 K de sensación térmica media en el día caluroso p95 y '
     'de 5 a 6 K en los programas de estancia; 3.876 m² de refugio efectivo, 4.377 con '
     'nebulización; 3.451 m² que abandonan la peor categoría de estrés térmico a las 16 h; '
     'y un cruce peatonal medio que pasa del 1,9 % al 23,3 % en sombra.'),
    ('MEDIANTE QUÉ MECANISMOS', 'Aproximadamente el 85 % procede de la sombra estructural, '
     'que no consume nada en operación; el 10 % del agua evaporativa; el 5 % de la '
     'nebulización condicional. La vegetación aporta ecología, superficie fría y '
     'experiencia — no el parasol.'),
    ('QUIÉNES SE BENEFICIAN MÁS', 'Quien espera, cultiva, juega o pasea a nivel de suelo, '
     'y muy especialmente quien emerge del intercambiador: cuatro de cinco bocas salen '
     'directamente al refugio. Se benefician menos quien camina la cinta al sol de las 16 h '
     'y quien busca sol de invierno bajo las hojas.'),
    ('QUÉ TRADE-OFFS INTRODUCE', 'Un 40,3 % menos de sol el 21 de diciembre, con '
     'correlación medida de 0,71 y 271 m² de excepción cartografiada; la visibilidad del '
     'reloj desde la estancia baja del 41,5 % al 25,5 %, con 896 m² de miradores '
     'protegibles; y 755 m² que empeoran, con mecanismo probado y corrección conocida.'),
    ('QUÉ DEPENDENCIAS OPERATIVAS TIENE', 'Un contrato de conservación de en torno a medio '
     'millón de euros anuales con dos frecuencias innegociables —la cámara de microalgas '
     'cada quince días y las boquillas cada trimestre— y un acuerdo de nivel de servicio '
     'para los tres ascensores. El agua es margen, nunca núcleo.'),
    ('QUÉ SIGUE SIENDO INCIERTO', 'Cuatro cosas: el abrigo aerodinámico del dosel (acotado '
     'en hasta +0,55 K), el uso real (horquilla de 350 a 9.580 personas-hora al día), la '
     'supervivencia de las especies tropicales y el coste de construcción (±40 %).'),
    ('QUÉ VALIDAR EN FASE MUNICIPAL', 'Exactamente esas cuatro incertidumbres, en ese '
     'orden, mediante el roadmap A-E: informe vinculante de Metro y CFD; prototipo de un '
     'mástil instrumentado; piloto de un cuadrante durante una temporada crítica con regla '
     'de decisión explícita; monitorización de siete variables; y solo entonces, despliegue.'),
    ('POR QUÉ RESULTA VIABLE', 'Porque su núcleo es geometría que no falla, sus costes '
     'están contados a veinticinco años, sus fallos degradan sin colapsar, su encaje físico '
     'es limpio —cero incidencias rojas, cero penetraciones en edificios, cero obstáculos '
     'en las bandas del Metro— y sus incógnitas tienen un precio de validación (un '
     'prototipo y una temporada de piloto) muy inferior al coste de equivocarse '
     'construyendo, o al de no hacer nada mientras Madrid acumula olas de calor.'),
]
for k, v in NUEVE:
    c.espacio(0.85)
    c.p.text(E.MX, c.y, k, size=7.0, color=E.MAGENTA, tracked=True, weight='bold')
    c.y -= 0.19
    c.y = c.p.body(E.MX, c.y, v, wrap=108, size=8.0) - 0.06

c.seccion('XII.2 · AUDITORÍA DE CERTEZA', 'Qué afirmamos y con cuánta fuerza')
c.texto('La última comprobación de este compendio no es sobre el proyecto: es sobre el '
        'propio documento. Cada conclusión importante se clasificó por su grado de '
        'demostración y después se verificó que el lenguaje empleado en el texto no fuera '
        'más fuerte que su evidencia. Donde el documento dice «es», hay dato reproducible; '
        'donde dice «podría», hay hipótesis declarada.')
c.tabla(['CONCLUSIÓN', 'CLASIFICACIÓN', 'LENGUAJE EMPLEADO'],
        [['El refugio térmico existe y su magnitud', 'DEMOSTRADA', 'indicativo: «es», «cubre»'],
         ['Cero conflictos físicos con la ciudad', 'DEMOSTRADA', 'indicativo'],
         ['Mecanismo de la cola térmica positiva', 'DEMOSTRADA', 'indicativo con prueba citada'],
         ['85 % del calor residual sobre ejes y la sombra alta como salida',
          'DEMOSTRADA / ROBUSTA', 'indicativo en el dato, condicional en la mejora'],
         ['Degradación benigna ante fallos', 'ROBUSTA', '«conserva del orden de dos tercios»'],
         ['La estancia seguirá al confort', 'ROBUSTA', '«potencial», «diseñada» — nunca «ocurrirá»'],
         ['Personas-hora protegidas', 'INDICATIVA', 'horquilla completa, siempre'],
         ['CAPEX y OPEX', 'INDICATIVA', '«orden de magnitud», rangos, «no es presupuesto»'],
         ['Efecto comercial', 'HIPÓTESIS', '«plausible», «no justifica el proyecto»'],
         ['Abrigo de viento', 'PENDIENTE DE VALIDACIÓN', '«limitación declarada» + cota dura'],
         ['Supervivencia tropical', 'PENDIENTE DE VALIDACIÓN', '«apuesta condicionada» + plan B']],
        [3.1, 1.75, 2.15], size=6.6, titulo='XII.2.1 · LA ESCALA APLICADA AL PROPIO DOCUMENTO')

c.seccion('XII.3 · EL INTERROGATORIO', 'Once preguntas de un técnico municipal escéptico')
FAQ = [
    ('¿De dónde sale cada cifra?', 'Del registro de métricas: 48 entradas con script de '
     'origen, dato de entrada, nivel de certeza y página donde aparece. Cero cifras '
     'huérfanas y cero conflictos en el test de consistencia entre documentos.'),
    ('¿Qué depende de una hipótesis?', 'Todo lo marcado con nivel C: afluencias, coste de '
     'construcción, efecto comercial, abrigo de viento y supervivencia tropical. Está '
     'listado en la Parte XII y nunca se cita como hecho.'),
    ('¿Qué ocurre si falla el agua?', 'Se pierden 0,43 K del efecto sobre el aire y los '
     '501 m² adicionales de la nebulización. La sombra estructural, que aporta los '
     '−10,9 K de radiante, no se entera. Autonomía de 3,3 días en punta con los depósitos.'),
    ('¿Y si falla un ascensor?', 'El peor caso deja un rodeo máximo de 286 m sobre la '
     'cinta, medido escenario por escenario. A nivel de suelo no hay ninguna dependencia '
     'mecánica. La condición es contractual: reparación en menos de 48 h.'),
    ('¿Qué mantenimiento exige?', 'Doce componentes con frecuencia y vida útil asignadas, '
     '160 puntos técnicos con acceso auditado —159 correctos y uno con corrección '
     'trivial— y en torno a medio millón de euros anuales con el fondo de reposición '
     'incluido.'),
    ('¿Es accesible?', 'A nivel de suelo, universalmente: cero incidencias rojas de paso '
     'y percentil 95 de evacuación en 63 m. En el nivel +6, solo por ascensor: es la '
     'asimetría reconocida del proyecto.'),
    ('¿Entorpece el Metro?', 'No: cero obstáculos en las bandas de respeto de todas las '
     'bocas, y cuatro de cinco salen directamente al refugio. Falta el informe vinculante '
     'de Metro de Madrid, que es la primera tarea de la fase A.'),
    ('¿Qué pasa en invierno?', 'Se pierde el 40,3 % del sol del solsticio; el 58 % del '
     'suelo conserva al menos la mitad; el trade-off es lineal con r = 0,71 y su excepción '
     'geométrica está identificada. La ponderación final es política, con los números '
     'sobre la mesa.'),
    ('¿Qué beneficio cuantificable produce?', 'Entre 3.876 y 4.377 m² de refugio efectivo; '
     '3.451 m² fuera de la peor categoría de estrés a las 16 h; y entre 33.000 y 890.000 '
     'personas-hora protegidas por temporada, a 4,9 € cada una en el escenario base.'),
    ('¿Qué riesgos siguen sin resolver?', 'Viento, uso real, tropicales y tramitación. '
     'Ninguno de ellos es geométrico: el modelo cierra en cero incidencias rojas.'),
    ('¿Qué debería verificar el Ayuntamiento antes de construir?', 'Fase A: informe de '
     'Metro, servidumbres bajo pavimento y CFD de dos direcciones dominantes. Fase B: '
     'prototipo de un mástil con anemometría y transmitancia real. Fase C: piloto de un '
     'cuadrante una temporada, con la regla de decisión de alcanzar al menos el 60 % del '
     'uso base. Solo entonces, despliegue.'),
]
for q, a in FAQ:
    c.espacio(0.8)
    yq = c.p.rich(E.MX, c.y, q, '', wrap=110, size=7.9)
    c.y = c.p.body(E.MX + 0.18, yq + 0.06, a, wrap=104, size=7.3) + 0.02

c.seccion('XII.4 · ROADMAP MUNICIPAL', 'Del papel a la plaza, en cinco fases')
c.tabla(['FASE', 'QUÉ', 'DURACIÓN', 'SALE CON'],
        [['A · VALIDACIONES', 'informe vinculante de Metro, servidumbres bajo pavimento, '
          'CFD de dos direcciones dominantes, consulta patrimonial', '4-6 meses',
          'lista de condicionantes cerrada'],
         ['B · PROTOTIPO', 'un mástil con dos hojas, cámara de microalgas y nebulización a '
          'escala real en parcela municipal', '3-4 meses',
          'anemometría, transmitancia real y costes reales'],
         ['C · PILOTO', 'el cuadrante C1 completo en Sol, instrumentado, durante una '
          'temporada crítica', '1 temporada',
          'el uso REAL: la variable que decide todo lo demás'],
         ['D · MONITORIZACIÓN', 'sensores fijos, conteos y panel público de datos',
          'continua desde C', 'el conjunto de datos que gobierna el despliegue'],
         ['E · DESPLIEGUE', 'resto del dosel, cinta y ascensores, incorporando las '
          'correcciones de los hallazgos D-001 y D-015', '12-18 meses', 'la plaza completa']],
        [1.35, 3.3, 1.15, 1.9], size=6.6, titulo='XII.4.1 · LAS CINCO FASES')
c.tabla(['VARIABLE', 'INSTRUMENTO', 'FRECUENCIA', 'QUÉ VALIDA'],
        [['Temperatura y humedad del aire', '6 parejas de sondas dentro y fuera del dosel',
          '10 min', 'el efecto local de −1,1 K estimado'],
         ['UTCI', '2 estaciones biometeorológicas móviles', 'continua', 'el ΔUTCI real'],
         ['Viento peatonal', '4 anemómetros', 'continua', 'la mayor incertidumbre del modelo'],
         ['Agua por circuito', 'contadores en riego, láminas y niebla', 'diaria',
          'el balance hídrico y el protocolo de sequía'],
         ['Usuarios y permanencia', 'conteo anónimo y aforos comparables', 'horaria',
          'las personas-hora reales frente a la horquilla'],
         ['Mantenimiento e incidencias', 'sistema de gestión con los 160 puntos', 'por evento',
          'la matriz técnica y los niveles de servicio'],
         ['Estado vegetal', 'inspección e índice de vegetación estacional', 'mensual',
          'la apuesta botánica y el plan B templado']],
        [1.85, 2.3, 0.95, 1.9], size=6.6,
        titulo='XII.4.2 · QUÉ SE MIDE DESPUÉS DE CONSTRUIR')
c.panel('VEREDICTO GLOBAL DEL PROYECTO',
        'VIABLE CON CONDICIONES. El Refugio Climático de Puerta del Sol convierte un tercio '
        'largo de la plaza en refugio térmico medible durante el peor trimestre del año, sin '
        'cerrar suelo público, sin tocar un solo edificio protegido y con su mecanismo '
        'dominante funcionando a coste operativo cero. Sus costes están cuantificados y '
        'publicados con el mismo peso que sus beneficios; sus fallos degradan el margen pero '
        'nunca el núcleo; y sus cuatro incertidumbres tienen un plan de validación cuyo '
        'coste es una fracción mínima del proyecto. Se recomienda avanzar a las fases A y B '
        'del roadmap, con la sombra alta sobre ejes incorporada al estudio y los miradores '
        'patrimoniales protegidos en el proyecto de ejecución.', alto=1.75, wrap=100)

# ============================================================ ANEXO · METRICAS
c.seccion('ANEXO A · REGISTRO DE MÉTRICAS', 'Las 48 cifras publicadas y su trazabilidad')
c.texto('Ninguna cifra de este compendio es huérfana. Cada una tiene identificador, valor, '
        'unidad, nivel de certeza, método, dato de origen y el documento y página donde '
        'aparece. Esta tabla permite reproducir cualquier resultado o refutarlo.')
rows = [[m.get('id', '')[:12], str(m.get('valor', ''))[:14], m.get('unidad', '')[:10],
         m.get('estado', '')[:1], (m.get('metodo', '') or '')[:56],
         (m.get('fuente', '') or '')[:44]] for m in MET]
c.tabla(['ID', 'VALOR', 'UNIDAD', 'C', 'MÉTODO', 'DATO DE ORIGEN'], rows,
        [0.95, 0.9, 0.65, 0.25, 2.35, 1.9], size=5.6, row_h=0.155,
        titulo='ANEXO A.1 · FINAL_METRICS_REGISTRY',
        fuente='FUENTE: 00_SISTEMA_Y_FUENTES/FINAL_METRICS_REGISTRY.csv · 48 métricas · '
               '0 conflictos de consistencia entre documentos')

c.seccion('ANEXO B · CIERRE', 'Qué contiene el paquete completo')
c.tabla(['BLOQUE', 'CONTENIDO'],
        [['Sistema y fuentes', 'inventario del corpus (2.486 archivos), catálogo de 279 '
          'análisis, matriz de cruces, registro de métricas, registro de hallazgos, sistema '
          'gráfico y snapshot de baseline con hashes'],
         ['Analíticos temáticos', '23 documentos individuales y 8 síntesis integradas, una '
          'por disciplina'],
         ['Documento global', 'informe de viabilidad y dossier de decisión municipal'],
         ['Este compendio', 'todo lo anterior en un solo volumen, con las tablas de datos '
          'íntegras y las conclusiones cruzadas'],
         ['Proceso', 'documento sobre el uso real de la inteligencia artificial en el '
          'proyecto: ciclo, errores, rectificaciones y trazabilidad'],
         ['Representación', '12 packs de control geométrico con ocho capas cada uno, '
          'metadatos de cámara y la regla de fidelidad jerárquica para la fase de imagen'],
         ['Anexos', 'manifiesto de entrega con hash SHA-256 por archivo e índice general']],
        [1.6, 5.4], size=6.8, titulo='ANEXO B.1 · ESTRUCTURA DE LA ENTREGA')

n = c.cerrar()
print('COMPENDIO parte 4 ok:', n, 'pp')
