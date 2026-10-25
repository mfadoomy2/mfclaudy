# -*- coding: utf-8 -*-
"""COMPENDIO parte 2: CLIMA Y CONFORT completo — parametros fisicos, 4 escenarios x 3
horas x 2 estados, sombra, radiacion, MRT, UTCI, aire, vegetacion, agua, viento,
programa, fallos. Con todas sus tablas."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from comp_core import (Comp, E, CL, BD, MXW, BASE, RC, geo, J, VEGCLI)  # noqa: E402

W = E.np_aud('walk.npy')[::2, ::2].astype(bool)
ny, nx = E.np_cli('u_E2_16_B.npy').shape
W = W[:ny, :nx]
CS = BD['cli_stats']
OUT = os.path.join(BASE, '12_ANEXOS_DATOS_Y_METODO', '_partes')
c = Comp(os.path.join(OUT, 'p2.pdf'), 'COMPENDIO ANALÍTICO', 'II · CLIMA Y CONFORT')

ESC = J(RC, 'FASE_03B5B_CLIMA', '_clima', 'escenarios.json')

# ============================================================ II.0 · METODO FISICO
c.seccion('III.0 · EL MODELO FÍSICO', 'Qué se simula exactamente', size=17)
c.texto('El confort térmico al aire libre no depende de la temperatura del aire: depende '
        'sobre todo de la RADIACIÓN. A 33 °C de aire, la diferencia entre estar al sol y '
        'estar a la sombra son unos 25 K de temperatura radiante media — el equivalente '
        'sensorial de mudarse de ciudad. Por eso el modelo invierte su esfuerzo en resolver '
        'el balance radiativo completo, celda a celda, y no en estimar el aire.')
c.tabla(['ETAPA', 'QUÉ HACE', 'RESOLUCIÓN'],
        [['1 · Voxelización', 'la escena v006 se convierte en un vóxel de clases de material '
          '(opaco, dosel, cúpula, vegetación, red) con un campo k_veg por especie',
          '0,5 m · 36 m de altura'],
         ['2 · Posición solar', 'algoritmo PSA (Blanco-Muriel 2001) para cada hora de los '
          'días muestreados de la ventana crítica',
          '431 posiciones · 31 días de 93'],
         ['3 · Transmitancia', 'marcha de rayos: opaco corta, dosel multiplica por su '
          'transmitancia, vegetación atenúa por Beer-Lambert con el k de SU especie',
          'paso 0,5 m · 61 direcciones de cielo'],
         ['4 · Balance de superficie', 'onda corta directa+difusa+reflejada y onda larga de '
          'cielo, suelo y superficies con temperatura propia por material',
          'por celda y hora'],
         ['5 · MRT', 'temperatura radiante media sobre un cuerpo a 1,10 m según VDI 3787, '
          'con el matiz de que un rayo que atraviesa dosel transmite sol pero NO ve cielo frío',
          'por celda'],
         ['6 · UTCI', 'índice universal de clima térmico (norma ISO) integrando aire, MRT, '
          'viento y humedad; se evalúa 1 de cada 3 celdas y se interpola',
          'por celda · 4 escenarios'],
         ['7 · Agua y niebla', 'Penman de lámina libre por elemento; nebulización '
          'isoentálpica con deriva por viento y perfil gaussiano de cobertura',
          'por elemento · 9 escenarios']],
        [1.3, 3.75, 1.95], size=6.6, titulo='III.0.1 · LA CADENA DE CÁLCULO')

# parametros fisicos completos
sys.path.insert(0, os.path.join(RC, 'FASE_03B9_HYPERDETAIL_V006', '_reclima9'))
try:
    import clima_core as CC
    P = CC.PARAMS
    rows = [[k, ('%.3f' % v[0]) if isinstance(v[0], float) else str(v[0]), v[1],
             v[2][:150]] for k, v in sorted(P.items())]
    c.tabla(['PARÁMETRO', 'VALOR', 'PROCEDENCIA', 'JUSTIFICACIÓN'], rows,
            [1.15, 0.62, 0.85, 4.38], size=5.5, row_h=0.26,
            titulo='III.0.2 · TODOS LOS PARÁMETROS FÍSICOS, CON SU ETIQUETA DE CERTEZA',
            fuente='FUENTE: _reclima9/clima_core.py PARAMS · MEDIDO / CALCULADO / '
                   'SIMULADO / ESTIMADO / HIPOTESIS declarado uno a uno')
except Exception as ex:
    c.texto('[parámetros no cargados: %s]' % ex)

# ============================================================ escenarios
c.seccion('III.1 · LOS ESCENARIOS', 'Cuatro climas, tres horas, dos estados')
vc = ESC['ventana_critica']
c.texto('La ventana crítica es el trimestre 15 de junio – 15 de septiembre: %d horas de '
        'datos PVGIS para Madrid. De esa distribución salen los escenarios: E1 es el día '
        'típico de la ventana, E2 el día caluroso (percentil 95), E3 la ola de calor, y E4 '
        'es E2 con la nebulización activada. Cada uno se evalúa a las 14, 16 y 18 h, en '
        'estado A (la plaza actual) y estado B (con el refugio).'
        % vc.get('horas', 2232))
rows = []
for en in ('E1', 'E2', 'E3'):
    e = ESC['escenarios'][en]
    for h in ('14:00', '16:00', '18:00'):
        v = e['horas'][h]
        rows.append([en, h, '%.1f °C' % v['Ta'], '%.0f %%' % v['RH'],
                     '%.0f W/m²' % v['Bn'], '%.0f W/m²' % v['Dh'],
                     '%.1f m/s' % v['WS'], '%.0f W/m²' % v.get('IR', 0)])
c.tabla(['ESC.', 'HORA', 'AIRE', 'HUMEDAD', 'DIRECTA', 'DIFUSA', 'VIENTO', 'IR CIELO'],
        rows, [0.55, 0.6, 0.8, 0.85, 0.95, 0.9, 0.85, 1.0], size=6.6,
        titulo='III.1.1 · CONDICIONES DE CONTORNO DE CADA ESCENARIO',
        fuente='FUENTE: PVGIS Madrid · ventana 15-jun a 15-sep · Ta media %.1f °C, '
               'máxima %.1f °C, p95 %.1f °C' % (vc['Ta_media'], vc['Ta_max'], vc['Ta_p95']))

# resultados por escenario/hora/estado
rows = []
for en in ('E1', 'E2', 'E3'):
    for h in ('14', '16', '18'):
        a = CS['escenarios']['%s_%s_A' % (en, h)]
        b = CS['escenarios']['%s_%s_B' % (en, h)]
        rows.append([en, h + ':00',
                     '%.1f' % a['MRT']['media'], '%.1f' % b['MRT']['media'],
                     '%+.1f' % (b['MRT']['media'] - a['MRT']['media']),
                     '%.1f' % a['UTCI']['media'], '%.1f' % b['UTCI']['media'],
                     '%+.2f' % (b['UTCI']['media'] - a['UTCI']['media'])])
c.tabla(['ESC.', 'HORA', 'MRT A', 'MRT B', 'ΔMRT', 'UTCI A', 'UTCI B', 'ΔUTCI'],
        rows, [0.6, 0.7, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85], size=6.8,
        titulo='III.1.2 · RESULTADO DE LAS 18 COMBINACIONES (°C y K, medias sobre pisable)')
c.texto('Lectura: el beneficio radiante es máximo a las 14–16 h (hasta −13 K de MRT) y se '
        'reduce al atardecer, cuando el sol rasante entra por debajo del dosel. El ΔUTCI '
        'sigue el mismo patrón amortiguado por el aire y el viento, que no cambian entre A '
        'y B. Obsérvese que el beneficio DISMINUYE al subir la temperatura (E1 −2,84 K, '
        'E2 −2,50 K, E3 −1,99 K): cuanto más extremo el día, más difícil es compensar '
        'radiativamente — un matiz que la síntesis optimista suele ocultar.')

# categorias UTCI
rows = []
for en in ('E1', 'E2', 'E3'):
    for st in ('A', 'B'):
        cc = CS['escenarios']['%s_16_%s' % (en, st)]['UTCI_categorias_m2']
        rows.append([en, st, '%.0f' % cc.get('SIN ESTRÉS / LEVE', 0),
                     '%.0f' % cc.get('MODERADO', 0), '%.0f' % cc.get('FUERTE', 0),
                     '%.0f' % cc.get('MUY FUERTE', 0), '%.0f' % cc.get('EXTREMO', 0)])
c.tabla(['ESC.', 'EST.', 'SIN/LEVE', 'MODERADO', 'FUERTE', 'MUY FUERTE', 'EXTREMO'],
        rows, [0.6, 0.6, 1.0, 1.05, 1.05, 1.15, 1.0], size=6.8,
        titulo='III.1.3 · SUPERFICIE (m²) POR CATEGORÍA OFICIAL DE ESTRÉS TÉRMICO · 16 H',
        fuente='Clases UTCI: moderado 26–32 °C · fuerte 32–38 · muy fuerte 38–46 · extremo >46')

# ============================================================ sombra
c.seccion('III.2 · SOMBRA', 'La sombra que no existía')
sh = CS['sombra']
c.mapa_doble(lambda ax: (E.draw_context(ax, geo),
                         E.show_raster(ax, E.np_cli('shade_crit_A.npy'), E.CMAP_AGUA,
                                       vmin=0, vmax=1, mask=W))[1],
             lambda ax: (E.draw_context(ax, geo),
                         E.show_raster(ax, E.np_cli('shade_crit_B.npy'), E.CMAP_AGUA,
                                       vmin=0, vmax=1, mask=W))[1],
             'A · LA PLAZA ACTUAL', 'B · CON EL REFUGIO',
             'FRACCIÓN DE SOMBRA · VENTANA CRÍTICA',
             'La geografía de la sombra nueva.',
             'Cada celda indica qué fracción de las horas críticas pasa en sombra. A la '
             'izquierda, la plaza de hoy: prácticamente blanca. A la derecha, la propuesta: '
             'el anillo perimetral y las bandas de la cinta concentran la protección y el '
             'vacío central se conserva deliberadamente despejado para los usos '
             'ceremoniales de la plaza.')
c.espacio(2.0)
ax = c.p.chart_axes(E.MX, c.y - 1.55, MXW, 1.35)
shA_ = E.np_cli('shade_crit_A.npy')[W]; shB_ = E.np_cli('shade_crit_B.npy')[W]
bins = np.linspace(0, 1, 21)
ax.hist(shA_, bins=bins, color='#ddd6cc', label='hoy (A)')
ax.hist(shB_, bins=bins, color=E.GREEN, alpha=0.75, label='propuesta (B)')
ax.set_xlabel('fracción de la ventana crítica en sombra', size=6)
ax.set_ylabel('celdas de suelo pisable', size=6)
ax.legend(fontsize=5.8, frameon=False)
c.y -= 1.75
c.y = c.p.caption(E.MX, c.y, 'Distribución completa, no solo la media.',
                  'La plaza actual concentra todo su suelo en la columna del cero: no hay '
                  'sombra que repartir. La propuesta genera una distribución ancha — hay '
                  'suelo a plena sombra, suelo en penumbra y suelo deliberadamente '
                  'soleado. Esa variedad es el proyecto.', wrap=108)
c.tabla(['MAGNITUD', 'ESTADO A', 'ESTADO B', 'DIFERENCIA'],
        [['Sombra crítica media', '%.1f %%' % (100 * sh['critica_A']['media']),
          '%.1f %%' % (100 * sh['critica_B']['media']),
          '+%.1f p.p.' % (100 * (sh['critica_B']['media'] - sh['critica_A']['media']))],
         ['Suelo con ≥50 % de sombra', '%.0f m²' % sh['m2_sombra50_A'],
          '%.0f m²' % sh['m2_sombra50_B'],
          '+%.0f m²' % (sh['m2_sombra50_B'] - sh['m2_sombra50_A'])],
         ['Horas de sol (12–18 h)', '%.1f h' % sh['sunhours']['A']['media'],
          '%.1f h' % sh['sunhours']['B']['media'],
          '%.1f h' % (sh['sunhours']['B']['media'] - sh['sunhours']['A']['media'])],
         ['Percentil 95 de sombra', '%.2f' % sh['critica_A']['p95'],
          '%.2f' % sh['critica_B']['p95'], '—']],
        [2.1, 1.5, 1.5, 1.9], size=6.8, titulo='III.2.1 · SOMBRA EN CIFRAS')

# ============================================================ radiacion e invierno
c.seccion('III.3 · RADIACIÓN Y EL PRECIO DEL INVIERNO',
          'Lo que se gana en julio y lo que se paga en diciembre')
rd = CS['radiacion']
c.tabla(['MAGNITUD', 'A', 'B', 'VARIACIÓN', 'LECTURA'],
        [['Radiación media de verano', '%.1f W/m²' % rd['verano_kWh_m2']['A']['media'],
          '%.1f W/m²' % rd['verano_kWh_m2']['B']['media'],
          '−%.1f %%' % rd['verano_kWh_m2']['reduccion_pct'],
          'el dosel retira más de un tercio de la energía solar del suelo'],
         ['Radiación 21-dic', '%.2f kWh/m²·día' % rd['invierno_kWh_m2_dia']['A']['media'],
          '%.2f kWh/m²·día' % rd['invierno_kWh_m2_dia']['B']['media'],
          '−%.1f %%' % rd['invierno_kWh_m2_dia']['perdida_pct'],
          'el coste invernal, publicado con el mismo peso que el beneficio'],
         ['Suelo que conserva ≥½ de su sol invernal', '—',
          '%.0f m²' % rd['invierno_m2_conservan50'], '58 % del pisable',
          'el trade-off está gobernado por la geometría, no eliminado']],
        [1.9, 1.15, 1.15, 1.0, 1.8], size=6.6, titulo='III.3.1 · VERANO CONTRA INVIERNO')
c.mapa(None, lambda ax: (E.draw_context(ax, geo),
                        E.show_raster(ax, E.np_cli('radwin_B.npy'), E.CMAP_CALOR,
                                      vmin=0, vmax=float(np.nanmax(E.np_cli('radwin_A.npy'))),
                                      mask=W))[1],
       leyenda='RADIACIÓN 21-DIC · KWH/M²·DÍA (PROPUESTA)',
       cap_lead='El invierno bajo el dosel.',
       cap='Las zonas oscuras son las que pierden sol en diciembre — coinciden con las '
           'hojas densas. El corazón de la plaza y las bandas exteriores conservan su '
           'régimen invernal casi intacto. La ponderación final entre estos dos mapas es '
           'una decisión política con los números encima de la mesa.')

# ============================================================ MRT y UTCI mapas
c.seccion('III.4 · TEMPERATURA RADIANTE Y ESTRÉS TÉRMICO', 'Los mapas que resumen el proyecto')
c.mapa_doble(lambda ax: (E.draw_context(ax, geo),
                         E.show_raster(ax, E.np_cli('f_E2_16_A_Tmrt.npy'), E.CMAP_CALOR,
                                       vmin=30, vmax=75, mask=W))[1],
             lambda ax: (E.draw_context(ax, geo),
                         E.show_raster(ax, E.np_cli('f_E2_16_B_Tmrt.npy'), E.CMAP_CALOR,
                                       vmin=30, vmax=75, mask=W))[1],
             'A · MRT ACTUAL · 16 H', 'B · MRT PROPUESTA · 16 H', 'MRT · °C · DÍA P95',
             'De pared radiante a mosaico térmico.',
             'De 65,2 °C de media en la plaza actual a 54,3 °C con el refugio; bajo el '
             'dosel denso la caída alcanza los 38,8 K. Los máximos supervivientes son los '
             'claros deliberados y las bandas junto a fachadas soleadas — exactamente donde '
             'el proyecto decidió no intervenir.')
c.mapa_doble(lambda ax: (E.draw_context(ax, geo),
                         E.show_raster(ax, E.np_cli('u_E2_16_A.npy'), E.CMAP_CALOR,
                                       vmin=30, vmax=44, mask=W))[1],
             lambda ax: (E.draw_context(ax, geo),
                         E.show_raster(ax, E.np_cli('u_E2_16_B.npy'), E.CMAP_CALOR,
                                       vmin=30, vmax=44, mask=W))[1],
             'A · UTCI ACTUAL', 'B · UTCI PROPUESTA', 'UTCI · °C · DÍA P95 · 16 H',
             'El índice que integra todo.',
             'UTCI combina aire, radiación, viento y humedad en la temperatura que un '
             'cuerpo humano percibe realmente. La mancha oscura de la izquierda es la '
             'categoría «muy fuerte» de estrés por calor cubriendo casi toda la plaza; a la '
             'derecha, 3.451 m² han salido de ella.')
dU = E.np_cli('u_E2_16_B.npy') - E.np_cli('u_E2_16_A.npy')
c.mapa(None, lambda ax: (E.draw_context(ax, geo),
                        E.show_raster(ax, dU, E.CMAP_DELTA, vmin=-6, vmax=6, mask=W))[1],
       leyenda='ΔUTCI B−A · K · DÍA P95 · 16 H',
       cap_lead='Dónde mejora y dónde empeora.',
       cap='Verde: la propuesta enfría. Rojo: la propuesta calienta. Los 755 m² rojos no '
           'son un descuido: son celdas que pierden factor de cielo sin ganar sombra a '
           'cambio, y su mecanismo está probado en la Parte X.')

# cola positiva
cp = CS['cola_positiva_E2_16']
c.tabla(['ESCENARIO', 'ÁREA QUE EMPEORA >0,5 K', 'ÁREA QUE MEJORA >1 K', 'ÁREA QUE MEJORA >3 K'],
        [[e, '%.0f m²' % CS['deltas_16h'][e]['m2_empeora_05K'],
          '%.0f m²' % CS['deltas_16h'][e]['m2_mejora_1K'],
          '%.0f m²' % CS['deltas_16h'][e]['m2_mejora_3K']] for e in ('E1', 'E2', 'E3')],
        [1.6, 1.9, 1.7, 1.8], size=6.8, titulo='III.4.1 · EL BALANCE COMPLETO POR ESCENARIO')
if cp.get('clusters'):
    c.tabla(['#', 'POSICIÓN X,Y', 'ÁREA', 'ΔUTCI MEDIO', 'ΔMRT MEDIO'],
            [[str(i + 1), '%.1f, %.1f' % (q['x'], q['y']), '%.0f m²' % q['m2'],
              '%+.2f K' % q['dUTCI_medio'], '%+.2f K' % q['dMRT_medio']]
             for i, q in enumerate(cp['clusters'])],
            [0.5, 1.7, 1.2, 1.5, 1.5], size=6.8,
            titulo='III.4.2 · LOS FOCOS DE EMPEORAMIENTO, LOCALIZADOS')

ref = E.np_cli('refugio.npy')
c.mapa(None, lambda ax: (E.draw_context(ax, geo),
                         E.show_raster(ax, np.where(np.nan_to_num(ref) > 0, ref, np.nan),
                                       E.CMAP_VERDE, vmin=0, vmax=3, mask=W))[1],
       leyenda='CLASE DE REFUGIO · 0 SIN MEJORA a 3 REFUGIO EFECTIVO',
       cap_lead='La clasificación final del suelo.',
       cap='Cuatro clases según la mejora sostenida de sensación térmica: sin mejora, leve, '
           'moderada y refugio efectivo. Los 3.876 m² de la clase superior (4.377 con '
           'nebulización) son la cifra que este dossier defiende ante el Ayuntamiento.')

# ============================================================ aire
c.seccion('III.5 · TEMPERATURA DEL AIRE', 'Lo que una sombra no puede hacer')
ai = CL['aire']
c.texto('Una promesa habitual de estos proyectos es «bajar la temperatura de la ciudad». '
        'Este dossier no la hace. El aire de una plaza abierta se renueva por viento en '
        'decenas de segundos: el efecto sobre la temperatura del aire es local y modesto. '
        'Se cuantifica con un balance de volumen de control declarado como estimación de '
        'orden de magnitud, no como CFD.')
c.tabla(['TÉRMINO', 'MECANISMO', 'ΔTa'],
        [['Sensible', 'flujo convectivo que el suelo sombreado deja de ceder al aire',
          '−%.2f K' % ai['dTa_sensible']],
         ['Latente', 'evaporación de láminas de agua y evapotranspiración vegetal',
          '−%.2f K' % ai['dTa_latente']],
         ['TOTAL local', 'suma bajo el dosel con altura de mezcla de 10 m',
          '−%.2f K' % ai['dTa_total']]],
        [1.2, 4.3, 1.5], size=7.0, titulo='III.5.1 · DESCOMPOSICIÓN DEL EFECTO SOBRE EL AIRE',
        fuente='HIPÓTESIS declarada: %s' % ai['hipotesis'][:150])
c.panel('LA PROPORCIÓN QUE IMPORTA',
        'De los −2,5 K de sensación térmica que gana un usuario en el día p95, en torno al '
        '90 % procede de la radiación (−10,9 K de MRT) y en torno al 10 % del aire (−1,1 K). '
        'Quien busque un proyecto que refrigere Madrid no encontrará aquí el argumento; '
        'quien busque uno que haga habitable el estar en Sol, sí.', alto=0.95)

# ============================================================ vegetacion
c.seccion('III.6 · VEGETACIÓN', 'Diecisiete especies con su física')
c.texto('Cada especie entra al modelo climático con su índice de área foliar (LAI) '
        'bibliográfico, del que se deriva su coeficiente de extinción volumétrico '
        'k = 0,5·LAI/3 y su transmitancia. El modelo VISUAL (miles de hojas) y el modelo '
        'FÍSICO (extinción volumétrica sobre un cilindro equivalente) están deliberadamente '
        'separados y ligados solo por metadatos: así una mejora estética no falsea el clima.')
rows = [[k, v.get('nombre', '')[:26], '%.1f' % v['LAI'], '%.3f' % v['k_veg'],
         '%.3f' % v['transmitancia'], '%.2f m' % v['altura'], '%.2f m' % v['diametro'],
         v.get('uso', '')[:34]] for k, v in sorted(VEGCLI.items())]
c.tabla(['ESPECIE', 'NOMBRE COMÚN', 'LAI', 'k_veg', 'TAU', 'ALTURA', 'DIÁM.', 'PAPEL'],
        rows, [1.45, 1.15, 0.42, 0.5, 0.5, 0.55, 0.5, 1.94], size=5.8,
        titulo='III.6.1 · LAS 17 ESPECIES Y SU FÍSICA',
        fuente='FUENTE: _veg_clima.json + BOTANICAL_MASTERPLAN_v001.csv · LAI bibliográfico (ESTIMADO)')
vg = CL['vegetacion']
c.tabla(['DOSEL ARBOLADO', 'EJEMPLARES', 'LAI', 'TAU COPA', 'PROYECCIÓN', 'L/H', 'kW'],
        [[r['bloque'][:30], str(r['n']), '%.1f' % r['LAI'], '%.3f' % r['tau'],
          '%.0f m²' % r['proy_m2'], '%.0f' % r['L_h'], '%.1f' % r['kW']]
         for r in vg['rows']], [1.9, 0.85, 0.5, 0.75, 0.95, 0.6, 0.55], size=6.8,
        titulo='III.6.2 · EVAPOTRANSPIRACIÓN DEL ARBOLADO')
sk = CS['sens_kveg']['resultado']
c.tabla(['HORA (15-JUL)', 'LAI −30 %', 'LAI BASE', 'LAI +30 %', 'CONCLUSIÓN'],
        [[h, '%.1f %%' % sk[h]['LOW']['pct_sombra'], '%.1f %%' % sk[h]['BASE']['pct_sombra'],
          '%.1f %%' % sk[h]['HIGH']['pct_sombra'],
          'la sombra se mueve ±1 punto: es ESTRUCTURAL, no vegetal'] for h in sorted(sk)],
        [1.2, 1.05, 1.05, 1.05, 2.65], size=6.8,
        titulo='III.6.3 · SENSIBILIDAD AL DATO BIBLIOGRÁFICO (fracción de suelo en sombra)')

# ============================================================ agua
c.seccion('III.7 · EL AGUA QUE ENFRÍA', 'Kilovatios líquidos')
ag = CL['agua']
rows = [[r['kind'][:12], r['id'][:10], '%.1f m²' % r['area'], '%.2f m' % r['depth'],
         '%.1f' % r['E_kg_m2_h'], '%.0f' % r['L_h'], '%.1f' % r['kW'],
         '%.1f' % r.get('mm_dia', 0)] for r in ag['rows']]
c.tabla(['TIPO', 'ID', 'SUPERFICIE', 'CALADO', 'kg/m²·h', 'L/H', 'kW', 'mm/día'],
        rows, [1.0, 0.85, 0.95, 0.8, 0.8, 0.7, 0.6, 0.7], size=6.4,
        titulo='III.7.1 · CADA ELEMENTO DE AGUA Y SU EVAPORACIÓN')
nb = CL['neb_escenarios']
c.tabla(['ESCENARIO', 'CLIMA', 'CAUDAL', 'Ta', 'HR', 'T. HÚMEDO', 'ΔT PSICROM.', 'ΔT APLICADO'],
        [[n['escenario'], n['clima'], '%.1f L/h' % n['q_L_h'], '%.1f °C' % n['Ta'],
          '%.0f %%' % n['RH'], '%.1f °C' % n['Twb'], '%.2f K' % n['dT_psicrometrico'],
          '%.2f K' % n['dT_aplicado']] for n in nb],
        [0.85, 0.55, 0.8, 0.7, 0.6, 0.85, 1.05, 1.1], size=6.4,
        titulo='III.7.2 · LOS NUEVE ESCENARIOS DE NEBULIZACIÓN',
        fuente='La depresión psicrométrica (Ta − T. húmedo) es el techo físico del '
               'enfriamiento evaporativo: con humedad alta, la niebla no sirve.')

# ============================================================ programa
c.seccion('III.8 · CONFORT POR PROGRAMA', 'Qué siente cada uso')
zn = CL['zonas']
c.tabla(['PROGRAMA', 'ÁREA', 'SOMBRA A › B', 'MRT A › B', 'ΔMRT', 'UTCI A › B', 'ΔUTCI', 'REFUGIO'],
        [[z['zona'][:22], '%.0f m²' % z['m2'], '%.0f › %.0f %%' % (z['sombra_A'], z['sombra_B']),
          '%.0f › %.0f' % (z['MRT_A'], z['MRT_B']), '%.1f' % z['dMRT'],
          '%.1f › %.1f' % (z['UTCI_A'], z['UTCI_B']), '%.2f' % z['dUTCI'],
          '%.0f %%' % z.get('refugio_pct', 0)] for z in zn],
        [1.35, 0.7, 1.0, 0.85, 0.55, 0.95, 0.6, 0.7], size=6.4,
        titulo='III.8.1 · LAS NUEVE ZONAS DE PROGRAMA')
cin = CL['cinta']
c.texto('La cinta merece párrafo aparte porque es la paradoja del proyecto: solo el '
        '%.1f %% de sus %d estaciones va en sombra y su UTCI medio (%.1f °C) apenas mejora '
        'la plaza actual. A cambio, a cota de tablero el viento sube de %.2f a %.2f m/s, '
        'que compensa parcialmente. Conclusión honesta: la cinta NO es un programa de '
        'estancia térmica, es un mirador en movimiento — y su papel climático real es dar '
        'sombra A LOS DE ABAJO.'
        % (cin['pct_sombra'], cin['n'], cin['UTCI'], cin['u_suelo'], cin['u_deck']))

# ============================================================ fallos
c.seccion('III.9 · ESCENARIOS DE FALLO', 'Qué sobrevive cuando algo se rompe')
cs = CS['canopy_seco']
sa = CS['sin_agua']
sv = CS['sens_viento']['UTCI_B_E2_16']
c.tabla(['MODO DE FALLO', 'CAUSA TIPO', 'EFECTO MEDIDO', 'NIVEL'],
        [['Sin nebulización', 'válvulas cerradas o avería',
          '−%.0f m² de refugio efectivo (quedan %.0f)' % (sa['perdida_neb_m2'], sa['refugio_m2_sin_neb']), 'A'],
         ['Sin agua en absoluto', 'corte de red con depósitos vacíos',
          '−%.2f K del término latente del aire; niebla OFF; la sombra estructural intacta' % sa['dTa_latente_perdida_K'], 'B'],
         ['Cámara de microalgas seca', 'mantenimiento no ejecutado',
          '+%.1f K de MRT bajo %.0f m² de dosel (≈+%.1f K de UTCI local)'
          % (cs['dMRT_medio_K'], cs['m2_bajo_dosel'], cs['dUTCI_aprox_K']), 'C'],
         ['Ola de calor (E3)', 'Ta 38 °C, HR 10 %',
          'ΔUTCI −1,99 K: sigue rindiendo, pero la cola que empeora crece a 1.175 m²', 'A'],
         ['Vegetación degradada', 'sequía, plaga o poda dura',
          'sombra −1 p.p.; se pierde un tercio del calor latente vegetal', 'B'],
         ['Abrigo de viento (no resuelto)', 'el dosel frena el viento peatonal',
          'UTCI-B pasaría de %.2f a %.2f °C con viento −50 %%' % (sv['BASE'], sv['VIENTO -50%']), 'C']],
        [1.5, 1.55, 3.35, 0.5], size=6.4, titulo='III.9.1 · LOS SEIS MODOS DE FALLO ESTUDIADOS')
c.panel('EL MÍNIMO GARANTIZADO',
        'El refugio se diseñó para degradarse bien: el mecanismo dominante — la sombra '
        'estructural, responsable de unos −10,9 K de temperatura radiante — no consume '
        'agua, no depende de bombas y no se seca. Todos los modos de fallo estudiados '
        'erosionan el margen; ninguno devuelve la plaza al estado actual. El peor caso '
        'combinado (sequía + ola de calor + cámara seca) conserva del orden de dos tercios '
        'del beneficio de sensación térmica.', alto=1.05)

n = c.cerrar()
print('COMPENDIO parte 2 ok:', n, 'pp')
