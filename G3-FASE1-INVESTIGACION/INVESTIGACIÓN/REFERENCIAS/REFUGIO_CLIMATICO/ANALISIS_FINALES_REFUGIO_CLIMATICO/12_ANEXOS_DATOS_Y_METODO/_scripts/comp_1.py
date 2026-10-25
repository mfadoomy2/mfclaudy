# -*- coding: utf-8 -*-
"""COMPENDIO parte 1: apertura, metodo, genealogia del proyecto, catalogo de los 279
analisis y AUDITORIA GEOMETRICA COMPLETA A0-A12 con todas sus filas."""
import os
import sys

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from comp_core import (Comp, E, AU, CL, BD, REG, MET, SNAP, MXW, BASE, geo)  # noqa: E402

OUT = os.path.join(BASE, '12_ANEXOS_DATOS_Y_METODO', '_partes')
os.makedirs(OUT, exist_ok=True)
c = Comp(os.path.join(OUT, 'p1.pdf'), 'COMPENDIO ANALÍTICO', 'I · SISTEMA Y AUDITORÍA')

# ============================================================ PORTADA
E.portada(c.doc, 'Compendio\nanalítico completo',
          'Todo lo analizado sobre el Refugio Climático de Puerta del Sol, en un solo '
          'documento: el método, la genealogía de seis versiones, los 279 análisis '
          'catalogados, la auditoría geométrica módulo a módulo, la simulación física '
          'completa, los sistemas de agua, construcción, uso, economía y patrimonio — '
          'con sus tablas de datos íntegras — y, al final, los cruces, las causalidades '
          'y las conclusiones que solo aparecen cuando todo se lee junto.',
          'REFUGIO CLIMÁTICO · PUERTA DEL SOL · DOCUMENTO INTEGRAL',
          [('BASELINE', 'v006 · build 12'), ('ANÁLISIS', '279 catalogados'),
           ('MÉTRICAS', '48 trazadas'), ('HALLAZGOS', '15 con método')],
          img=os.path.join(BASE, '09_RENDERS_Y_REPRESENTACION', '_pipeline', 'refpacks',
                           'H1', 'beauty.png'),
          num='COMPENDIO')

# ============================================================ 0.1 · COMO LEER
c.seccion('0.1 · CÓMO LEER ESTE DOCUMENTO', 'Tres profundidades, un solo hilo', size=17)
c.texto('Este compendio se escribió para ser leído de tres maneras. En VEINTE MINUTOS: '
        'las conclusiones de la Parte XII y el resumen de cada parte. En DOS HORAS: los '
        'capítulos temáticos completos, saltando las tablas de datos. EN PROFUNDIDAD: '
        'todo, incluidas las tablas — que están aquí precisamente porque un dossier que '
        'no publica sus datos no se puede auditar.')
c.y -= 0.05
c.lista([
    ('Estructura.', 'Parte I sistema y auditoría geométrica · Parte II clima y confort · '
     'Parte III movilidad · Parte IV contexto urbano · Parte V agua y ecología · '
     'Parte VI construcción y mantenimiento · Parte VII uso social · Parte VIII economía · '
     'Parte IX patrimonio · Parte X cruces y causalidades · Parte XI conclusiones · '
     'Parte XII anexos de datos.'),
    ('Cada análisis responde una pregunta.', 'La pregunta va en el título; el método, los '
     'datos, las limitaciones y el nivel de certeza van siempre visibles. No hay resultado '
     'sin su procedencia.'),
    ('Tres niveles de conocimiento.', 'A = medido o calculado, reproducible desde la '
     'geometría o el dato. B = inferido mediante un modelo declarado. C = hipótesis o '
     'escenario, plausible pero pendiente de validación. Ningún C se presenta como A.'),
    ('Una sola geometría.', 'Todo procede de la baseline congelada v006 build 12, con '
     'hash SHA-256 por archivo. Los resultados de versiones anteriores aparecen únicamente '
     'como genealogía, nunca mezclados con los actuales.'),
], wrap=100)
c.panel('ADVERTENCIA DE LECTURA HONESTA',
        'Este documento publica también lo que no funciona: los 755 m² donde la propuesta '
        'empeora la sensación térmica, el 40 % de sol de invierno que se pierde, las vistas '
        'del reloj que la estancia sacrifica, el punto de mantenimiento sin acceso, el '
        'término de viento que no está resuelto y las tres incertidumbres que solo un '
        'piloto puede cerrar. Están en el mismo cuerpo tipográfico que los beneficios.',
        alto=1.2)

# ============================================================ 0.2 · BASELINE
c.seccion('0.2 · LA BASE DE TODO', 'La geometría congelada v006 build 12')
c.texto('La totalidad de este compendio se calcula sobre una única versión del modelo, '
        'congelada y hasheada antes de empezar. Ningún número procede de una versión '
        'anterior; los de versiones anteriores solo aparecen en la genealogía (§1.2) para '
        'mostrar la evolución.')
aud = SNAP['auditoria_vigente']['counts']
cli = SNAP['clima_vigente']
x = E.MX
c.p.bignum(x, c.y, str(aud['RED']), 'RED', 'incidencias rojas de la auditoría final'); x += 1.9
c.p.bignum(x, c.y, str(aud['YELLOW']), 'YELLOW', 'observaciones amarillas'); x += 2.0
c.p.bignum(x, c.y, str(aud['GREEN']), 'GREEN', 'comprobaciones superadas'); x += 2.0
c.p.bignum(x, c.y, '29', 'SHA-256', 'archivos con hash en el snapshot')
c.y -= 1.25
grupos = {}
for k, v in SNAP['archivos'].items():
    grupos.setdefault(v['grupo'], []).append((k, v))
rows = []
for g in sorted(grupos):
    for k, v in sorted(grupos[g]):
        rows.append([g, k, '%.1f' % (v['bytes'] / 1048576.0), v['mtime'][:16].replace('T', ' '),
                     v['sha256'][:16] + '…'])
c.tabla(['GRUPO', 'ARCHIVO', 'MB', 'MODIFICADO', 'SHA-256 (16)'], rows,
        [0.95, 2.6, 0.5, 1.2, 1.75], size=6.2, titulo='0.2.1 · SNAPSHOT DE LA BASELINE',
        fuente='FUENTE: 00_SISTEMA_Y_FUENTES/BASELINE_SNAPSHOT.json · %s' % SNAP['timestamp'][:19])

# ============================================================ 0.3 · METODO
c.seccion('0.3 · MÉTODO', 'Cómo se mide un proyecto que aún no existe')
c.texto('El proyecto no está construido: no hay sensores que leer. Todo lo medible se '
        'obtiene de tres fuentes — la geometría, la física y el dato externo — y cada una '
        'tiene su propio régimen de verdad.')
c.tabla(['FUENTE', 'QUÉ PERMITE MEDIR', 'CÓMO', 'NIVEL'],
        [['Geometría v006', 'anchos de paso, gálibos, colisiones, distancias, visibilidad, '
          'accesos, superficies, cantidades',
          'reconstrucción de la escena desde el generador e intersección con rásteres de '
          '0,25 m; ningún dato se teclea a mano', 'A'],
         ['Física (balance)', 'sombra, radiación, temperatura radiante, UTCI, evaporación, '
          'transmitancia vegetal',
          'trazado de rayos sobre vóxel de 0,5 m con 431 posiciones solares reales; balance '
          'radiativo completo onda corta y larga; UTCI oficial', 'A/B'],
         ['Dato externo', 'clima de referencia, afluencias, precios unitarios',
          'PVGIS, fuentes institucionales citadas con URL y fecha; cuando no existe dato '
          'público se declara hipótesis y se dan tres escenarios', 'B/C'],
         ['Modelo de comportamiento', 'potencial de estancia, personas-hora protegidas, '
          'efecto comercial',
          'índices con fórmula publicada y sensibilidad a sus pesos; nunca caja negra',
          'C']],
        [1.35, 1.75, 2.85, 0.55], size=6.8, titulo='0.3.1 · LOS TRES REGÍMENES DE VERDAD')
c.panel('LO QUE ESTE MÉTODO NO PUEDE HACER',
        'No predice comportamiento humano real (lo modela y publica la horquilla). No '
        'resuelve la aerodinámica urbana (haría falta CFD; se acota la sensibilidad). No '
        'sustituye un presupuesto de ejecución (da orden de magnitud con rangos). No '
        'garantiza la supervivencia de las especies tropicales (es una apuesta con plan B '
        'declarado). Cada una de estas cuatro limitaciones tiene su vía de validación en '
        'el roadmap municipal.', alto=1.15)

# ============================================================ I.1 · QUE SE PROPONE
c.seccion('I.1 · QUÉ SE PROPONE', 'Una infraestructura de estancia para el peor trimestre')
c.texto('Un dosel estructural de 93 hojas sobre 80 mástiles articulados en tres copas '
        '(C1 oeste, C2 centro, C3 este) que produce 4.186 m² de sombra nueva en la hora '
        'crítica; una cinta-mirador de 733 m a cota +6,00 con 6 escaleras y 3 ascensores; '
        'un sistema de agua con láminas, splash jugable, balsas elevadas y nebulización de '
        'alta presión; 17 especies reales en cuatro estratos; un huerto urbano; y el suelo '
        'de Puerta del Sol intacto, público y reversible: la cimentación es puntual y el '
        'pavimento histórico se conserva bajo las jardineras.')
inv = BD['tec_stats'].get('familias', [])
if inv:
    rows = [[f.get('familia', ''), str(f.get('n_objetos', '')), str(f.get('n_tipos', '')),
             f.get('nota', '')[:70]] for f in inv]
    c.tabla(['FAMILIA', 'OBJETOS', 'TIPOS', 'PAPEL'], rows, [1.6, 0.75, 0.6, 4.05],
            size=6.6, titulo='I.1.1 · DE QUÉ ESTÁ HECHO (INVENTARIO POR FAMILIA)',
            fuente='FUENTE: 05_CONSTRUCCION/B_DATOS/tec_stats.json · escena v006 build 12')

# ============================================================ I.2 · GENEALOGIA
c.seccion('I.2 · GENEALOGÍA', 'Seis versiones, cada una con su auditoría')
c.texto('El proyecto no se dibujó una vez: se generó, se midió, se rompió y se regeneró '
        'seis veces. Cada versión existe porque una auditoría demostró que la anterior '
        'fallaba en algo concreto. Esta tabla es la memoria de ese proceso — y explica por '
        'qué los datos de este compendio proceden solo de la última.')
c.tabla(['VERSIÓN', 'QUÉ INTRODUJO', 'QUÉ DEMOSTRÓ SU AUDITORÍA', 'RESULTADO'],
        [['v001-v002\n03B / 03B.5', 'geometría maestra, familias paramétricas, kit de partes',
          'auditoría A1-A11 sobre 6.857 objetos: 89 pasos <1,20 m, 2 ejes atravesados por '
          'geometría, 1 bolsa sin salida de 44 m², gálibos bajos en 51 manchas',
          'lista de incidencias V-001..V-0xx'],
         ['v003\n03B.6', 'resolución de la auditoría: cinta, ascensores, guardas cruzadas, estatua',
          'reauditoría completa + re-clima: las correcciones no rompieron el clima; '
          'comparación A/B por primera vez',
          'modelo auditado y climatizado'],
         ['v004\n03B.7', 'conflictos urbanos A y B resueltos (El Corte Inglés, abrazo del Metro); '
          'detailing LOD A/B/C',
          'módulo A12 NUEVO (interferencia con volumetrías construidas reales): 0 '
          'penetraciones tras corrección',
          'V004 READY FOR MUNICIPAL ANALYSIS'],
         ['v005\n03B.8', 'purga geométrica forense, microdetalle, vegetación con assets reales',
          'las capturas del autor sirvieron de auditoría de defectos: 48 defectos '
          'catalogados; purga 443 duplicados › 0; z-fighting 33 › 0',
          'V005 PASSES CLOSE-RANGE QA (5 RED residuales)'],
         ['v006\n03B.9', 'botánica real (17 especies), hiperdetalle constructivo, k_veg por especie',
          'auditoría completa en 12 builds: los 5 RED heredados resueltos; 0 RED · 26 '
          'YELLOW · 18 GREEN; purga 191 › 22 errores documentados',
          'V006 HYPERDETAIL PASS — baseline de este compendio'],
         ['FASE FINAL', 'regeneración analítica completa sobre v006 congelada',
          '279 análisis catalogados, 48 métricas trazadas, 15 hallazgos con método '
          'científico, 12 reference packs de control',
          'este documento']],
        [1.15, 1.9, 2.9, 1.55], size=6.4, titulo='I.2.1 · LAS SEIS VERSIONES',
        fuente='FUENTE: registro forense _FORENSIC_PROCESS (240+ eventos) + informes de fase')

# ============================================================ I.3 · CATALOGO 279
c.seccion('I.3 · EL CATÁLOGO', 'Los 279 análisis, uno a uno')
from collections import Counter  # noqa: E402
tm = Counter(r['tema'] for r in REG)
vg = Counter(r['vigencia_v006'] for r in REG)
c.texto('Cada análisis realizado en cualquier fase del proyecto está catalogado con su '
        'pregunta, su método, sus inputs, su script, sus outputs, su unidad, su versión '
        'geométrica, su nivel de certeza y sus limitaciones. La columna de vigencia indica '
        'si el análisis sigue vivo sobre v006, si fue sustituido por un equivalente '
        'posterior, o si solo tiene valor histórico. Las páginas que siguen vuelcan el '
        'catálogo completo por tema.')
c.tabla(['TEMA', 'N', 'VIGENTES', 'SUPERSEDED', 'HISTÓRICO'],
        [[t, str(n),
          str(sum(1 for r in REG if r['tema'] == t and r['vigencia_v006'] == 'VIGENTE')),
          str(sum(1 for r in REG if r['tema'] == t and r['vigencia_v006'] == 'SUPERSEDED')),
          str(sum(1 for r in REG if r['tema'] == t and r['vigencia_v006'] in ('HISTORICO', 'REGENERAR')))]
         for t, n in sorted(tm.items(), key=lambda kv: -kv[1])],
        [1.4, 0.8, 1.2, 1.4, 1.4], size=7.0, titulo='I.3.1 · REPARTO POR TEMA')

TEMAS = {'CLI': 'CLIMA Y CONFORT', 'MOB': 'MOVILIDAD Y ACCESIBILIDAD',
         'URB': 'CONTEXTO URBANO Y TRANSPORTE', 'AGU': 'AGUA, ECOLOGÍA Y VEGETACIÓN',
         'TEC': 'CONSTRUCCIÓN, ESTRUCTURA Y MANTENIMIENTO', 'SOC': 'USO SOCIAL',
         'PAT': 'PATRIMONIO Y VISUALES', 'REN': 'REPRESENTACIÓN Y RENDER',
         'SYS': 'SISTEMA, MÉTODO Y TRAZABILIDAD'}
for t in ('CLI', 'MOB', 'URB', 'AGU', 'TEC', 'SOC', 'PAT', 'REN', 'SYS'):
    sub = [r for r in REG if r['tema'] == t]
    if not sub:
        continue
    rows = [[r['id'], (r['pregunta'] or '')[:150], (r['metricas_clave'] or '—')[:120],
             r['certeza'], r['vigencia_v006'][:4]] for r in sub]
    c.tabla(['ID', 'PREGUNTA', 'MÉTRICAS CLAVE', 'C', 'VIG'], rows,
            [0.62, 2.7, 3.0, 0.32, 0.42], size=5.5, row_h=0.30,
            titulo='I.3 · %s (%d análisis)' % (TEMAS[t], len(sub)))

# ============================================================ II · AUDITORIA
c.seccion('II · AUDITORÍA GEOMÉTRICA', 'Doce módulos que interrogan al modelo',
          'A0 reconstruye la escena; A1 a A12 la someten a doce preguntas independientes. '
          'Ninguno confía en el generador: todos remiden sobre rásteres propios.')
meta = CL['escena_meta']
c.tabla(['MÓDULO', 'PREGUNTA', 'MÉTODO', 'RESULTADO v006'],
        [['A0', '¿La escena auditada es exactamente el modelo aprobado?',
          'importación del generador con interceptación de sus tres salidas; rasterizado '
          'a 0,25 m en banda de cuerpo 0,05–2,10 m',
          '%d mallas · %s triángulos' % (meta['mallas'], '{:,}'.format(meta['triangulos']).replace(',', '.'))],
         ['A1', '¿Se puede caminar? Anchos, cuellos, continuidad, bolsas',
          'remuestreo de ejes a 0,5 m con rayos perpendiculares; barrido de umbrales de '
          'anchura; componentes conexas',
          '0 RED · peor cuello 10,75 m'],
         ['A2', '¿Hay gálibo suficiente bajo elemento firme?',
          'rasterizado zmin con interpolación exacta del plano de cada triángulo, '
          'separando familias firmes de vegetación',
          '%d manchas bajas (18 vegetales)' % len(AU['a2_clear']['low'])],
         ['A3', '¿Las alturas del sistema son coherentes?',
          'lectura de cotas por bloque y disco contra el HEIGHT_SYSTEM',
          '%d familias · %d discos' % (len(AU['a3_heights']['rows']), len(AU['a3_heights']['cotas_discos']))],
         ['A4', '¿La cinta es transitable y accesible?',
          'perfil completo cada metro: cota, gálibo bajo, suelo libre; escaleras y '
          'ascensores medidos en la escena',
          '733 m · 43 soportes · 6+3 accesos'],
         ['A5', '¿Los itinerarios cumplen criterios de accesibilidad?',
          'pendientes, anchos mínimos, radios de giro y cambios de nivel por eje',
          '%d ejes evaluados' % len(AU['a5_access']['rows'])],
         ['A6', '¿Se respetan las bandas de las bocas de Metro y Cercanías?',
          'banda de respeto de 5,5 m y obstáculos por debajo de 2,5 m alrededor de cada boca',
          '%d bocas · 0 obstáculos' % len(AU['a6_metro']['rows'])],
         ['A7', '¿Qué se ve de los hitos patrimoniales?',
          'visibilidad punto a punto sobre %d puntos de muestreo hacia reloj, torre y Correos'
          % AU['a7_views']['n'],
          'reloj 41,5 % de la superficie'],
         ['A8', '¿Está la plaza sobrecargada de objetos?',
          'ocupación por sector de la envolvente del proyecto',
          '%d sectores · ocupación 8,7 %%' % len(AU['a8_density']['sectors'])],
         ['A9', '¿Se puede mantener lo que se construye?',
          'catálogo de puntos técnicos con holgura, distancia a acceso rodado, necesidad '
          'de plataforma y gálibo vertical',
          '%d puntos · 159 con acceso' % len(AU['a9_maint'])],
         ['A10', '¿Hay colisiones entre familias?',
          'intersección volumétrica por pares de familias y puntos calientes',
          '%d pares · %d focos' % (len(AU['a10_collisions']['pairs']), len(AU['a10_collisions']['hot']))],
         ['A12', '¿El proyecto penetra alguna volumetría construida real?',
          'módulo independiente del generador: pip y distancias propias contra 35 '
          'huellas OSM con altura de tope por tipo',
          '0 penetraciones en %d edificios' % AU['a12_edificios']['n_edificios']]],
        [0.5, 2.0, 3.1, 1.4], size=6.2, titulo='II.0 · LOS DOCE MÓDULOS',
        fuente='FUENTE: _reaudit9/audit_run.py sobre baseline v006 build 12')

# ---------------------------------------------------------------- A1 detalle
c.seccion('II.1 · A1 · RECORRIDOS', 'Los cinco ejes, estación a estación')
c.texto('Cada eje declarado se remuestrea cada 0,5 m. En cada estación se lanzan rayos '
        'perpendiculares hasta el primer obstáculo (ancho transversal disponible) y se lee '
        'la holgura local como el doble de la distancia al obstáculo más próximo. Un eje '
        'está «ocupado» cuando su traza cae dentro de geometría.')
rows = []
for pth in AU['a1_paths']['paths']:
    rr = pth['rows']
    wt = [r['w_transv'] for r in rr]
    wl = [r['w_local'] for r in rr]
    nb = sum(1 for r in rr if not r['eje_libre'])
    rows.append([pth['id'], '%.0f m' % pth['long'], str(len(rr)),
                 '%.1f / %.1f' % (min(wt), np.median(wt)),
                 '%.1f / %.1f' % (min(wl), np.median(wl)), str(nb),
                 pth.get('nota', '')[:28]])
c.tabla(['EJE', 'LONG.', 'ESTAC.', 'ANCHO TRANSV. MIN/MED', 'HOLGURA MIN/MED',
         'BLOQ.', 'NOTA'], rows, [1.45, 0.6, 0.6, 1.5, 1.35, 0.45, 1.05], size=6.4,
        titulo='II.1.1 · RESUMEN POR EJE')
narrow = AU['a1_paths']['narrow']
if narrow:
    rows = [[n.get('id', ''), '%.1f' % n.get('s', 0), '%.1f, %.1f' % (n.get('x', 0), n.get('y', 0)),
             '%.2f m' % n.get('w', 0), str(n.get('c_izq', ''))[:14], str(n.get('c_der', ''))[:14]]
            for n in narrow]
    c.tabla(['EJE', 'S (m)', 'POSICIÓN X,Y', 'HOLGURA', 'CAUSA IZQ.', 'CAUSA DER.'],
            rows, [1.5, 0.6, 1.35, 0.85, 1.4, 1.3], size=6.2,
            titulo='II.1.2 · LOS %d ESTRECHAMIENTOS LOCALES SOBRE EJE' % len(narrow))
choke = AU['a1_paths']['choke']
if choke:
    rows = [[str(i + 1), '%.1f, %.1f' % (q.get('x', 0), q.get('y', 0)), '%.2f m' % q.get('w', 0),
             str(q.get('fam', q.get('causa', '')))[:40], '%.1f m²' % q.get('m2', 0) if q.get('m2') else '—']
            for i, q in enumerate(choke)]
    c.tabla(['#', 'POSICIÓN X,Y', 'PASO', 'FAMILIA CAUSANTE', 'ÁREA'], rows,
            [0.4, 1.5, 0.9, 3.2, 1.0], size=6.2,
            titulo='II.1.3 · LOS %d PASOS ESTRANGULADOS DEL ÁMBITO' % len(choke))
frag = AU['a1_paths']['frag']
c.tabla(['ANCHO EXIGIDO', 'COMPONENTES', 'MAYOR (m²)', 'COBERTURA'],
        [['%.2f m' % f['w'], str(f['comp']), '%.0f' % f['big'], '%.1f %%' % (100 * f['cover'])]
         for f in frag], [1.4, 1.3, 1.5, 1.5], size=6.8,
        titulo='II.1.4 · FRAGMENTACIÓN DE LA RED SEGÚN ANCHO EXIGIDO')
bt = AU['a1_paths']['bottleneck']
peores = sorted(bt.items(), key=lambda kv: kv[1])[:14]
c.tabla(['PAR DE ACCESOS', 'CUELLO'],
        [[k[:78], '%.2f m' % v] for k, v in peores], [5.3, 1.7], size=6.4,
        titulo='II.1.5 · LOS 14 PEORES CUELLOS ENTRE PARES DE ACCESOS (de 45)',
        fuente='FUENTE: _reaudit9/_data/a1_paths.json · celda 0,25 m · banda 0,05–2,10 m')

c.seccion('II.1-BIS · LA RED, EN MAPA', 'Dónde está el ancho y dónde falta')
plaza = E.np_aud('plaza.npy'); width = E.np_aud('width.npy')
c.mapa(None, lambda ax: (E.draw_context(ax, geo),
                         E.show_raster(ax, np.clip(width, 0, 12), E.CMAP_VERDE,
                                       mask=plaza & (width > 0)))[1],
       leyenda='ANCHURA LIBRE LOCAL · M',
       cap_lead='La anchura útil, celda a celda.',
       cap='Verde intenso: más de 12 m de holgura. Los pasillos claros entre jardineras son '
           'los que la auditoría vigila; ninguno baja del umbral que convertiría la plaza '
           'en un laberinto. La mediana del suelo pisable supera los 5,5 m.')
ax = c.p.chart_axes(E.MX, c.y - 1.5, MXW, 1.3)
wv = width[plaza & (width > 0)]
ax.hist(np.clip(wv, 0, 20), bins=40, color=E.GREEN)
ax.axvline(1.8, color=E.MAGENTA, lw=1.0, ls='--')
ax.axvline(3.0, color=E.AGUA, lw=1.0, ls='--')
ax.set_xlabel('anchura libre local · m (líneas: 1,80 y 3,00 m exigidos)', size=6)
ax.set_ylabel('celdas', size=6)
c.y -= 1.72
c.y = c.p.caption(E.MX, c.y, 'Distribución de anchuras.',
                  'La masa de la distribución está muy por encima de los umbrales de '
                  'proyecto: el refugio no estrangula la plaza, la amuebla.', wrap=108)

# ---------------------------------------------------------------- A2 galibos
c.seccion('II.2 · A2 · GÁLIBOS', 'Qué altura libre hay sobre la cabeza')
st = AU['a2_clear']['stats']
c.texto('La regla 7 del sistema de alturas exige 3,00 m libres bajo elemento FIRME sobre '
        'suelo pisable. La vegetación se evalúa aparte: una copa baja es una cuestión de '
        'poda, no un defecto de proyecto.')
c.tabla(['MAGNITUD', 'VALOR'],
        [[k.replace('_', ' '), ('%.2f' % v) if isinstance(v, float) else str(v)]
         for k, v in st.items()], [3.4, 3.6], size=6.8,
        titulo='II.2.1 · ESTADÍSTICA DE GÁLIBO')
low = AU['a2_clear']['low']
if low:
    rows = [[str(i + 1), '%.1f, %.1f' % (q.get('x', 0), q.get('y', 0)),
             '%.2f m' % q.get('z', q.get('clear', 0)), str(q.get('obj', q.get('fam', '')))[:34],
             '%.1f m²' % q.get('m2', 0) if q.get('m2') else '—'] for i, q in enumerate(low[:40])]
    c.tabla(['#', 'POSICIÓN', 'GÁLIBO', 'ELEMENTO', 'ÁREA'], rows,
            [0.4, 1.4, 0.85, 3.0, 1.35], size=6.0,
            titulo='II.2.2 · MANCHAS DE GÁLIBO BAJO (%d en total; primeras 40)' % len(low))

c.mapa(None, lambda ax: (E.draw_context(ax, geo),
                         E.show_raster(ax, E.np_aud('clear_firme.npy'), E.CMAP_AGUA,
                                       vmin=2, vmax=12, mask=E.np_aud('walk.npy')))[1],
       leyenda='GÁLIBO LIBRE BAJO ELEMENTO FIRME · M',
       cap_lead='La altura libre sobre la cabeza.',
       cap='Solo se computan familias firmes: una copa baja es poda, no defecto. Las zonas '
           'oscuras son los puntos donde la cinta y las hojas vuelan más bajo — todas por '
           'encima del mínimo exigido de 3,00 m salvo las manchas catalogadas.')

# ---------------------------------------------------------------- A4 cinta
c.seccion('II.3 · A4 · LA CINTA', 'Setecientos treinta y tres metros a seis metros')
rb = AU['a4_ribbon']
c.tabla(['PARÁMETRO', 'VALOR', 'CRITERIO', 'LECTURA'],
        [['Longitud', '%.0f m' % rb['long'], '—', 'recorrido continuo en anillo'],
         ['Cota', '+%.2f m' % rb['z'], 'constante', 'pendiente longitudinal 0,0 %'],
         ['Ancho total / útil', '%.2f / %.2f m' % (rb['ancho_total'], rb['ancho_util']),
          '≥1,80 m', 'cumple con holgura'],
         ['Barandilla', '%.2f m' % rb['barandilla_h'], '≥1,00 m', 'cumple'],
         ['Radio mínimo', '%.2f m' % rb['radio_min'], 'giro de silla 1,50 m', 'revisar en ejecución'],
         ['Soportes', str(rb['n_soportes']), '—', 'RIB_SUP en planta'],
         ['Gálibo bajo la cinta', '%.2f m' % rb['galibo_bajo'], '≥3,00 m', 'cumple ampliamente'],
         ['Accesos', '%d escaleras + 3 ascensores' % rb['n_accesos'], 'itinerario accesible',
          'solo los ascensores son accesibles: la asimetría del proyecto']],
        [1.5, 1.5, 1.3, 2.7], size=6.8, titulo='II.3.1 · PARÁMETROS DE LA CINTA')
prof = rb['prof']
if prof:
    zs = [q['bajo'] for q in prof if 'bajo' in q]
    libres = sum(1 for q in prof if q.get('suelo_libre'))
    c.texto('El perfil se mide cada metro: %d estaciones. Gálibo bajo la cinta entre '
            '%.2f y %.2f m (media %.2f); %d de %d estaciones tienen suelo libre debajo '
            '(%.0f %%) — el resto vuela sobre jardineras, agua o mobiliario, que es la '
            'intención de proyecto.'
            % (len(prof), min(zs), max(zs), float(np.mean(zs)), libres, len(prof),
               100.0 * libres / len(prof)))
    ax = c.p.chart_axes(E.MX, c.y - 1.5, MXW, 1.3)
    ax.plot([q['s'] for q in prof], zs, '-', color=E.GREEN, lw=0.8)
    ax.axhline(3.0, color=E.MAGENTA, lw=0.8, ls='--')
    ax.set_xlabel('recorrido s · m', size=6); ax.set_ylabel('gálibo bajo cinta · m', size=6)
    c.y -= 1.7
    c.p.caption(E.MX, c.y, 'Perfil de gálibo bajo la cinta.',
                'La línea magenta marca los 3,00 m exigidos; el perfil no baja de %.2f m '
                'en ningún punto de los 733 m.' % min(zs), wrap=104)
    c.y -= 0.3
stairs = rb['stairs']
if stairs:
    c.tabla(['#', 'POSICIÓN X,Y', 'DIST. ARRANQUE A CINTA', 'DIST. CENTRO A CINTA'],
            [[str(i + 1), '%.1f, %.1f' % (s['x'], s['y']), '%.2f m' % s['d_top_a_cinta'],
              '%.2f m' % s['d_centro_a_cinta']] for i, s in enumerate(stairs)],
            [0.5, 1.8, 2.2, 2.2], size=6.6, titulo='II.3.2 · LAS SEIS ESCALERAS')

# ---------------------------------------------------------------- A9 mantenimiento
c.seccion('II.4 · A9 · MANTENIMIENTO', 'Los 160 puntos técnicos, uno a uno')
c.texto('Un sistema que no se puede mantener no es viable aunque funcione el primer día. '
        'Este módulo cataloga cada punto técnico del proyecto con su holgura alrededor, su '
        'distancia al acceso rodado más próximo, si exige plataforma elevadora y el gálibo '
        'vertical disponible para maniobrarla. La tabla completa se vuelca a continuación.')
mn = AU['a9_maint']
por_cat = {}
for m in mn:
    por_cat.setdefault(m['cat'], []).append(m)
c.tabla(['CATEGORÍA', 'PUNTOS', 'HOLGURA MED.', 'DIST. ACCESO MED.', 'CON PLATAFORMA'],
        [[k, str(len(v)), '%.2f m' % float(np.mean([q['holgura'] for q in v])),
          '%.0f m' % float(np.mean([q['dist'] for q in v])),
          '%d de %d' % (sum(1 for q in v if q['requiere_plataforma']), len(v))]
         for k, v in sorted(por_cat.items())],
        [2.0, 0.8, 1.2, 1.5, 1.5], size=6.8, titulo='II.4.1 · RESUMEN POR CATEGORÍA')
rows = [[m['id'][:22], m['cat'][:16], '%.1f, %.1f, %.1f' % (m['x'], m['y'], m['z']),
         '%.2f' % m['holgura'], '%.0f' % m['dist'],
         'sí' if m['requiere_plataforma'] else 'no',
         'sí' if m['acceso'] else 'NO',
         ('%.1f' % m['galibo_vertical']) if m.get('galibo_vertical') is not None else '—']
        for m in mn]
c.tabla(['ID', 'CATEGORÍA', 'X, Y, Z', 'HOLG.', 'DIST.', 'PLAT.', 'ACCESO', 'GÁLIBO'],
        rows, [1.35, 1.0, 1.35, 0.5, 0.5, 0.4, 1.0, 0.55], size=5.4, row_h=0.135,
        titulo='II.4.2 · CATÁLOGO COMPLETO DE PUNTOS TÉCNICOS',
        fuente='FUENTE: _reaudit9/_data/a9_maint.json · 160 puntos · v006 build 12')

c.seccion('II.4-BIS · EL MAPA DEL MANTENIMIENTO', 'Los 160 puntos, en planta')
mnx = [q['x'] for q in mn]; mny = [q['y'] for q in mn]
mnp = [1 if q['requiere_plataforma'] else 0 for q in mn]


def _dib_mant(ax):
    E.draw_context(ax, geo)
    ax.scatter([x for x, p in zip(mnx, mnp) if not p],
               [y for y, p in zip(mny, mnp) if not p],
               s=9, c=E.GREEN, edgecolors='white', linewidths=0.3, zorder=5,
               label='acceso a pie')
    ax.scatter([x for x, p in zip(mnx, mnp) if p],
               [y for y, p in zip(mny, mnp) if p],
               s=13, c=E.MAGENTA, marker='^', edgecolors='white', linewidths=0.3,
               zorder=6, label='requiere plataforma')
    ax.legend(fontsize=5.4, frameon=False, loc='lower left')
    return None


c.mapa(None, _dib_mant, cap_lead='Dónde hay que subirse a una plataforma.',
       cap='Cada punto es un elemento que alguien tendrá que revisar, limpiar o sustituir '
           'durante veinticinco años. Los triángulos magenta exigen plataforma elevadora: '
           'su distribución determina el coste real del contrato de conservación y la '
           'frecuencia con que la plaza se ocupa parcialmente para mantenerla.')

# ---------------------------------------------------------------- A10 colisiones
c.seccion('II.5 · A10 · COLISIONES', 'Dónde se tocan las familias')
c.texto('Las intersecciones entre familias no siempre son errores: una jardinera que toca '
        'el pavimento o una planta que roza su tiesto son uniones declaradas. El módulo '
        'las mide todas y la lista blanca del proyecto separa lo intencionado de lo '
        'accidental. En v006 no queda ninguna colisión no declarada.')
pairs = AU['a10_collisions']['pairs']
rows = [[p.get('a', '')[:26], p.get('b', '')[:26], str(p.get('n', '')),
         '%.3f m³' % p.get('vol', 0) if p.get('vol') else '—',
         'declarada' if p.get('wl') else 'medida'] for p in pairs]
c.tabla(['FAMILIA A', 'FAMILIA B', 'FOCOS', 'VOLUMEN', 'ESTADO'], rows,
        [1.85, 1.85, 0.7, 1.1, 1.5], size=6.2,
        titulo='II.5.1 · LOS %d PARES CON CONTACTO' % len(pairs))

# ---------------------------------------------------------------- incidencias
c.seccion('II.6 · REGISTRO DE INCIDENCIAS', 'Las 44 comprobaciones y su veredicto')
iss = AU['issues']
sev = {'RED': 0, 'YELLOW': 0, 'GREEN': 0}
for i in iss:
    sev[i['sev']] = sev.get(i['sev'], 0) + 1
c.texto('La auditoría no produce una nota: produce un registro. Cada entrada tiene '
        'severidad, categoría, posición, magnitud medida, causa atribuida y estrategia de '
        'corrección. En la baseline final: %d rojas, %d amarillas, %d verdes.'
        % (sev.get('RED', 0), sev.get('YELLOW', 0), sev.get('GREEN', 0)))
rows = [[i['id'], i['sev'][:1], i['cat'][:12], i['title'][:64], (i.get('magnitud') or '')[:52]]
        for i in iss]
c.tabla(['ID', 'S', 'CATEGORÍA', 'COMPROBACIÓN', 'MAGNITUD MEDIDA'], rows,
        [0.55, 0.25, 0.95, 2.6, 2.65], size=5.6, row_h=0.20,
        titulo='II.6.1 · REGISTRO COMPLETO',
        fuente='FUENTE: _reaudit9/_data/issues.json · v006 build 12 · 0 RED')

n = c.cerrar()
print('COMPENDIO parte 1 ok:', n, 'pp')
