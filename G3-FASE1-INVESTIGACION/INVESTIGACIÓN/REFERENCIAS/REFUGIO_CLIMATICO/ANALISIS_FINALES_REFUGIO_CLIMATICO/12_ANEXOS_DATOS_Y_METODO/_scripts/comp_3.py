# -*- coding: utf-8 -*-
"""COMPENDIO parte 3: movilidad, contexto urbano, agua/ecologia, construccion y
mantenimiento, uso social, economia y patrimonio — con sus tablas completas."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from comp_core import (Comp, E, AU, CL, BD, MXW, BASE, geo, MANT, AGUAEL, FUENTES,
                       BOT)  # noqa: E402

W = E.np_aud('walk.npy')[::2, ::2].astype(bool)
ny, nx = E.np_cli('u_E2_16_B.npy').shape
W = W[:ny, :nx]
OUT = os.path.join(BASE, '12_ANEXOS_DATOS_Y_METODO', '_partes')
c = Comp(os.path.join(OUT, 'p3.pdf'), 'COMPENDIO ANALÍTICO', 'IV · SISTEMAS')
MOB, AGU, TEC, SOC, ECO, PAT = (BD['mob_stats'], BD['agu_stats'], BD['tec_stats'],
                                BD['soc_stats'], BD['eco_stats'], BD['pat_stats'])

# ============================================================ IV · MOVILIDAD
c.seccion('IV · MOVILIDAD Y ACCESIBILIDAD', 'La plaza sigue siendo plaza', size=17)
c.texto('La primera obligación de una intervención en Puerta del Sol es no estropear lo '
        'que ya funciona: el paso. Sol es antes que nada un nudo de circulación peatonal. '
        'La auditoría mide anchos reales, cuellos entre accesos, continuidad de la red y '
        'distancia de evacuación; los motores de esta fase añaden el escenario de fallo de '
        'ascensor y el nivel de servicio bajo tres demandas.')
red = MOB['red']
c.tabla(['MAGNITUD', 'VALOR', 'CRITERIO', 'VEREDICTO'],
        [['Incidencias rojas de paso', '0', 'ninguna', 'la red no se degrada'],
         ['Peor cuello entre accesos', '%.2f m' % red['bottleneck_peor'],
          'sin umbral normativo', 'no hay cuello a escala de multitud'],
         ['Estrechamientos locales sobre eje', str(red['narrow_n']), 'informativo',
          'todos en interiores de estancia, no en la traza'],
         ['Pasos estrangulados del ámbito', str(red['choke_n']), '<1,20 m',
          'huecos entre jardineras, no rutas'],
         ['Bolsas sin salida', str(len(red['pockets'])), '0 imputables',
          'ninguna atribuible al proyecto'],
         ['Continuidad a 1,80 m exigidos', '84 %', 'informativo', 'una sola componente'],
         ['Continuidad a 3,00 m exigidos', '73 %', 'informativo', 'dos componentes']],
        [2.0, 1.0, 1.35, 2.65], size=6.8, titulo='IV.1 · LA RED PEATONAL EN CIFRAS')
da = MOB['dist_acceso']
c.mapa(None, lambda ax: (E.draw_context(ax, geo),
                        E.show_raster(ax, np.load(os.path.join(BASE, '02_MOVILIDAD_Y_ACCESIBILIDAD',
                                                               'B_DATOS', 'dist_accesos.npy')),
                                      E.CMAP_CALOR, vmin=0, vmax=120))[1],
       leyenda='DISTANCIA GEODÉSICA A LA SALIDA MÁS PRÓXIMA · M',
       cap_lead='Nadie queda lejos de una salida.',
       cap='Distancia real bordeando obstáculos (frente de onda sobre el ráster pisable), '
           'no distancia en línea recta. Media %.0f m, percentil 95 %.0f m, máximo %.0f m; '
           'el %.1f %% del suelo está a menos de 60 m de un acceso.'
           % (da['media'], da['p95'], da['max'], da['pct_a_menos_60m']))
pm = MOB['pmr']
c.tabla(['ESCENARIO DEL NIVEL +6,00', 'RODEO MÁXIMO SOBRE LA CINTA', 'LECTURA'],
        [['Los %d ascensores operativos' % pm['n_ascensores'], '%.0f m' % pm['rodeo_max_con_todos_m'],
          'servicio pleno; ~2-3 min a paso PMR'],
         ['Peor fallo N−1', '%.0f m' % pm['rodeo_max_N1_m'],
          '~4-5 min: tolerable como avería puntual, no como fuera de servicio crónico'],
         ['A nivel de suelo', '0 m', 'accesibilidad universal sin mediación mecánica']],
        [2.2, 2.1, 2.7], size=6.8, titulo='IV.2 · ACCESIBILIDAD VERTICAL: LA ASIMETRÍA DEL PROYECTO')
c.texto('El nivel +6,00 tiene seis escaleras y tres ascensores. Para una persona con '
        'movilidad reducida, los ascensores no son una comodidad: son la única vía. Esa es '
        'la asimetría reconocida del proyecto, y su mitigación es contractual (SLA de '
        'reparación inferior a 48 h) más el estudio de un cuarto aparato en el arco sur, '
        'que bajaría el peor rodeo a unos 180 m.')
los = MOB['los']['escenarios']
peor = {}
for r in los:
    k = r['escenario']
    if k not in peor or r['q_p_min_m'] > peor[k]['q_p_min_m']:
        peor[k] = r
c.tabla(['ESCENARIO DE DEMANDA', 'EJE PÉSIMO', 'FLUJO', 'ANCHO MÍN.', 'p/min/m', 'LOS'],
        [[k, v['eje'][:22], '%.0f p/h' % v['flujo_p_h'], '%.2f m' % v['ancho_min_m'],
          '%.1f' % v['q_p_min_m'], v['LOS']] for k, v in peor.items()],
        [1.4, 1.5, 1.0, 1.0, 0.8, 1.3], size=6.8,
        titulo='IV.3 · NIVEL DE SERVICIO PEATONAL (HIPÓTESIS DE DEMANDA, NIVEL C)',
        fuente=MOB['los']['hipotesis'][:190])

# ============================================================ V · CONTEXTO URBANO
c.seccion('V · CONTEXTO URBANO Y TRANSPORTE', 'Dónde el proyecto toca la ciudad')
c.texto('Puerta del Sol no es un solar: es el intercambiador de transporte más denso de '
        'España, un conjunto patrimonial y una superficie con servidumbres bajo el '
        'pavimento. El proyecto se mide contra las tres cosas.')
a6 = AU['a6_metro']
rows = [[r['name'][:24], 'sí' if r.get('en_ambito') else 'no',
         '%.1f, %.1f' % (r['x'], r['y']), '%.1f m' % r.get('d_suelo', 0),
         str(r.get('elem_suelo', ''))[:18], '%.1f m' % r.get('libre_min', 0),
         str(r.get('n_banda_suelo', 0))] for r in a6['rows']]
c.tabla(['BOCA', 'EN ÁMBITO', 'POSICIÓN', 'DIST. AL ELEMENTO MÁS PRÓXIMO', 'QUÉ ES',
         'LIBRE MÍN.', 'OBSTÁC.'], rows, [1.35, 0.75, 1.15, 1.35, 1.05, 0.75, 0.6],
        size=6.4, titulo='V.1 · LAS BOCAS DE METRO Y CERCANÍAS · BANDA DE RESPETO %.1f m'
        % a6['band'],
        fuente='FUENTE: _reaudit9/_data/a6_metro.json · 0 obstáculos en banda por debajo de '
               '%.1f m en ninguna boca' % a6['zobst'])
cross = BD['global_cross']
c.tabla(['BOCA', 'DISTANCIA AL PRIMER REFUGIO EFECTIVO', 'SOMBRA DEL ENTORNO DE SALIDA (30 m)'],
        [[b['boca'][:22], '%.0f m' % b['d_refugio_m'], '%.2f' % b['sombra_salida_30m']]
         for b in cross['metro_clima']['bocas']], [1.9, 2.6, 2.5], size=6.8,
        titulo='V.2 · LA PUERTA CLIMÁTICA: QUÉ ENCUENTRA QUIEN SALE DEL METRO',
        fuente='Cálculo propio de esta fase: frente de onda geodésico desde cada boca hasta '
               'la primera celda de refugio efectivo. Dato de flujo: 73 M viajeros/año.')
c.tabla(['COMPROBACIÓN URBANA', 'RESULTADO', 'NIVEL'],
        [['Penetraciones en volumetrías construidas reales', '0 en %d edificios'
          % AU['a12_edificios']['n_edificios'], 'A'],
         ['Distancia del eje de la cinta al edificio más próximo',
          '%.2f m (edificio %s)' % (AU['a12_edificios']['eje_cinta']['dist'],
                                    AU['a12_edificios']['eje_cinta']['edificio']), 'A'],
         ['Aire libre a la fachada más sensible (El Corte Inglés)', '≈2,0 m exigidos y verificados', 'A'],
         ['Servidumbres bajo pavimento', 'no verificadas: exigen cartografía municipal', 'PENDIENTE'],
         ['Informe vinculante de Metro de Madrid', 'no solicitado: fase A del roadmap', 'PENDIENTE']],
        [2.9, 3.0, 1.1], size=6.8, titulo='V.3 · ENCAJE FÍSICO Y TRAMITACIÓN')

# ============================================================ VI · AGUA
c.seccion('VI · AGUA, ECOLOGÍA Y VEGETACIÓN', 'Treinta metros cúbicos el peor día')
bal = AGU['balance_dia_punta_m3']
c.tabla(['TÉRMINO', 'DÍA PUNTA', 'QUÉ COMPRA', 'NIVEL'],
        [['Evaporación de láminas y splash', '%.1f m³' % bal['evaporacion_laminas'],
          'superficies frías y el juego de agua', 'A/B'],
         ['Riego de las 17 especies', '%.1f m³' % bal['riego_vegetal'],
          '286 kW latentes, ecología y paisaje', 'B'],
         ['Nebulización (solo día seco)', '%.2f m³' % bal['nebulizacion'],
          '+501 m² de refugio: el agua más rentable', 'C'],
         ['TOTAL', '%.1f m³' % bal['total'],
          'equivalente aproximado a 12 viviendas', '—']],
        [2.1, 1.1, 2.7, 1.1], size=6.8, titulo='VI.1 · BALANCE HÍDRICO DEL DÍA PUNTA')
c.tabla(['PARÁMETRO DE AUTONOMÍA', 'VALOR'],
        [[k.replace('_', ' '), ('%.2f' % v) if isinstance(v, float) else str(v)]
         for k, v in AGU.items() if isinstance(v, (int, float))][:10],
        [3.6, 3.4], size=6.8, titulo='VI.2 · CAPACIDAD Y AUTONOMÍA')
if AGUAEL:
    ks = list(AGUAEL[0].keys())[:7]
    c.tabla([k.upper()[:14] for k in ks],
            [[str(r.get(k, ''))[:22] for k in ks] for r in AGUAEL],
            [7.0 / len(ks)] * len(ks), size=6.2,
            titulo='VI.3 · INVENTARIO DE ELEMENTOS DE AGUA')
if BOT:
    ks = [k for k in BOT[0].keys()][:8]
    c.tabla([k.upper().replace('_', ' ')[:13] for k in ks],
            [[str(r.get(k, ''))[:26] for k in ks] for r in BOT],
            [7.0 / len(ks)] * len(ks), size=5.6, row_h=0.20,
            titulo='VI.4 · MASTERPLAN BOTÁNICO: LAS 17 ESPECIES',
            fuente='FUENTE: BOTANICAL_MASTERPLAN_v001.csv · especies reales con hábito, '
                   'altura, LAI, necesidad hídrica, tolerancia solar y estrategia estacional')
c.panel('LA JERARQUÍA DE CORTE EN SEQUÍA',
        'Si Madrid decreta restricciones, el sistema se apaga por orden inverso a su valor '
        'irreemplazable: primero la nebulización (recuperable en minutos), después las '
        'láminas ornamentales, después las herbáceas de temporada, después los arbustos — y '
        'NUNCA el arbolado, cuya reposición cuesta quince años. El núcleo del confort, la '
        'sombra estructural, sigue funcionando con los depósitos vacíos.', alto=1.05)

# ============================================================ VII · CONSTRUCCION
c.seccion('VII · CONSTRUCCIÓN Y MANTENIMIENTO', 'Quién cuida qué, cada cuánto')
c.texto('Un proyecto de 15.197 piezas solo es viable si su conservación cabe en un '
        'contrato municipal ordinario. La matriz siguiente asigna a cada componente su '
        'función, su vía de acceso, su frecuencia y el riesgo de no atenderlo.')
if MANT:
    ks = list(MANT[0].keys())
    idx = [k for k in ks][:6]
    c.tabla([k.upper().replace('_', ' ')[:16] for k in idx],
            [[str(r.get(k, ''))[:44] for k in idx] for r in MANT],
            [7.0 / len(idx)] * len(idx), size=5.8, row_h=0.24,
            titulo='VII.1 · MATRIZ COMPONENTE › FUNCIÓN › ACCESO › FRECUENCIA › RIESGO',
            fuente='FUENTE: 05_CONSTRUCCION/B_DATOS/matriz_mantenimiento.csv')
c.tabla(['INDICADOR DE MANTENIBILIDAD', 'VALOR'],
        [[k.replace('_', ' '), ('%.2f' % v) if isinstance(v, float) else str(v)]
         for k, v in TEC.items() if isinstance(v, (int, float, str))][:12],
        [3.9, 3.1], size=6.8, titulo='VII.2 · INDICADORES')

# ============================================================ VIII · USO SOCIAL
c.seccion('VIII · USO SOCIAL', 'Dónde querrá quedarse la gente')
c.texto('Aquí se abandona la certeza y se entra en el modelo. Nadie puede medir el '
        'comportamiento de una plaza que no existe; lo que sí puede hacerse es construir un '
        'índice explícito, publicar su fórmula, comprobar que es estable frente a cambios '
        'de sus pesos y dar la horquilla completa de resultados en vez de un número.')
c.panel('LA FÓRMULA, PUBLICADA',
        'Potencial de estancia = 0,30 · sombra + 0,30 · confort UTCI + 0,15 · asiento '
        'disponible + 0,10 · proximidad al agua + 0,15 · condición de borde. Los pesos se '
        'sometieron a variación de ±50 %: el mapa de zonas de estancia alta conserva un '
        'índice de coincidencia (Jaccard) de 0,74 o superior. El índice es sensible, pero '
        'no arbitrario.', alto=0.95)
ipe = np.load(os.path.join(BASE, '06_USO_SOCIAL_Y_EXPERIENCIA', 'B_DATOS', 'ipe.npy'))
c.mapa(None, lambda ax: (E.draw_context(ax, geo),
                        E.show_raster(ax, ipe, E.CMAP_VERDE, vmin=0, vmax=0.8))[1],
       leyenda='POTENCIAL DE ESTANCIA · ÍNDICE 0–0,8',
       cap_lead='El mapa del quedarse.',
       cap='El 90,7 % de la superficie con potencial alto cae dentro del refugio térmico '
           'efectivo: la inversión climática y la social son, literalmente, la misma.')
ph = SOC['personas_hora']['escenarios']
c.tabla(['ESCENARIO', 'SUPUESTO', 'PERSONAS-HORA/DÍA', 'POR TEMPORADA'],
        [[k.upper(), str(v.get('supuesto', ''))[:56], '%.0f' % v.get('p_h_dia', 0),
          '%.0f' % (v.get('p_h_dia', 0) * 93)] for k, v in ph.items()],
        [1.0, 3.0, 1.5, 1.5], size=6.8,
        titulo='VIII.1 · PERSONAS-HORA PROTEGIDAS: LA HORQUILLA COMPLETA (NIVEL C)')

# ============================================================ IX · ECONOMIA
c.seccion('IX · ECONOMÍA Y OPERACIÓN', 'Qué cuesta y qué compra ese dinero')
cap = ECO.get('capex_MEUR', {})
c.tabla(['PARTIDA', 'LOW', 'BASE', 'HIGH'],
        [[p.get('partida', '')[:40], str(p.get('low', '')), str(p.get('base', '')),
          str(p.get('high', ''))] for p in cap.get('partidas', [])] +
        [['TOTAL CAPEX (M€)', str(cap.get('total', {}).get('low', '')),
          str(cap.get('total', {}).get('base', '')), str(cap.get('total', {}).get('high', ''))]],
        [3.4, 1.2, 1.2, 1.2], size=6.6,
        titulo='IX.1 · CAPEX POR PARTIDA (ORDEN DE MAGNITUD, NIVEL C)')
opx = ECO['opex_kEUR_ano']
c.tabla(['PARTIDA ANUAL', 'LOW', 'BASE', 'HIGH'],
        [[p['partida'][:44], str(p['low']), str(p['base']), str(p['high'])]
         for p in opx['partidas']] +
        [['TOTAL OPEX (k€/año)', str(opx['total']['low']), str(opx['total']['base']),
          str(opx['total']['high'])],
         ['Fondo de reposición (M€/año)', '—', '%.2f' % opx['fondo_reposicion_MEUR_ano'], '—']],
        [3.4, 1.2, 1.2, 1.2], size=6.6, titulo='IX.2 · OPEX POR PARTIDA')
cv = ECO.get('coste_por_ph', {})
c.tabla(['ESCENARIO DE USO', '€ POR PERSONA-HORA PROTEGIDA (25 AÑOS)', 'LECTURA'],
        [[k.upper(), '%.1f €' % v if isinstance(v, (int, float)) else str(v),
          {'low': 'solo defendible como piloto',
           'base': 'cumple con margen un umbral municipal razonable de 8 €',
           'high': 'coste marginal equivalente a un helado por hora protegida'}.get(k, '')]
         for k, v in cv.items()], [1.5, 3.0, 2.5], size=6.8,
        titulo='IX.3 · EL INDICADOR QUE PERMITE COMPARAR')
if FUENTES:
    ks = list(FUENTES[0].keys())[:5]
    c.tabla([k.upper()[:16] for k in ks],
            [[str(r.get(k, ''))[:40] for k in ks] for r in FUENTES],
            [7.0 / len(ks)] * len(ks), size=6.0,
            titulo='IX.4 · FUENTES EXTERNAS UTILIZADAS, CON SU PROCEDENCIA')

# ============================================================ X · PATRIMONIO
c.seccion('X · PATRIMONIO Y VISUALES', 'Tres maneras de medir la misma vista')
c.texto('La pregunta patrimonial habitual —«¿cuánta plaza ve el reloj?»— tiene truco: '
        'mide superficie, no personas. Este dossier la responde tres veces, y las tres '
        'respuestas juntas dicen algo que ninguna dice por separado.')
vf = BD['global_cross']['visuales_flujo']
c.tabla(['MÉTRICA', 'RESULTADO', 'QUÉ SIGNIFICA'],
        [['Por superficie del ámbito', '41,5 %', 'la métrica clásica de los informes patrimoniales'],
         ['Por flujo peatonal (tránsito)', '%.1f %%' % vf['pct_flujo_con_vista_reloj'],
          'quien PASA conserva la vista: los ejes se dejaron despejados'],
         ['Por estancia de alto potencial', '25,5 %',
          'quien SE QUEDA la pierde: la estancia se metió bajo el dosel']],
        [2.1, 1.3, 3.6], size=6.8, titulo='X.1 · VISIBILIDAD DEL RELOJ DE GOBERNACIÓN')
c.tabla(['EJE', '% DE SU TRAZA CON VISTA DEL RELOJ', 'PESO EN EL FLUJO'],
        [[d['eje'], '%.1f %%' % d['pct_traza_con_reloj'], '%.3f' % d['peso_flujo']]
         for d in vf['detalle']], [2.4, 2.5, 2.1], size=6.8,
        titulo='X.2 · DESGLOSE POR EJE')
a7 = AU['a7_views']
pts7 = np.array(a7['pts']); vis7 = np.array(a7['vis']['RELOJ'], bool)


def _dib_vis(ax):
    E.draw_context(ax, geo)
    ax.scatter(pts7[~vis7][:, 0], pts7[~vis7][:, 1], s=1.1, c='#ddd6cc', zorder=4)
    ax.scatter(pts7[vis7][:, 0], pts7[vis7][:, 1], s=1.6, c=E.AGUA, zorder=5)
    ax.plot(-25.2, -34.35, '*', ms=12, c=E.INK, zorder=6)
    return None


c.mapa(None, _dib_vis, cap_lead='Desde dónde se ve el reloj de Gobernación (estrella).',
       cap='Azul: puntos con línea de visión libre al reloj sobre los 2.455 muestreados. '
           'Gris: puntos sin ella. El corredor central se preserva; la pérdida se '
           'concentra bajo las copas, que es exactamente donde el proyecto pone la '
           'estancia — el conflicto que describe el panel siguiente.')
c.panel('EL CONFLICTO CONFORT–CONTEMPLACIÓN, Y SU RECURSO ESCASO',
        'El proyecto separó papeles sin declararlo: el eje es caliente pero tiene vistas; '
        'la estancia es fresca pero las pierde. Existen 896 m² donde ambas cosas coinciden '
        '—confort alto Y vista del reloj—: son los «miradores», un recurso escaso que este '
        'dossier cartografía precisamente para que el proyecto de ejecución los blinde en '
        'lugar de ocuparlos con mobiliario o vegetación alta.', alto=1.05)

n = c.cerrar()
print('COMPENDIO parte 3 ok:', n, 'pp')
