# -*- coding: utf-8 -*-
"""ATLAS CARTOGRAFICO v006 — una lamina por campo medido, a pagina completa y con el
sistema grafico del Refugio. Regenera sobre la baseline actual los mapas que en fases
anteriores vivian dispersos en cada carpeta de fase."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
sys.path.insert(0, os.path.join(BASE, '12_ANEXOS_DATOS_Y_METODO', '_scripts'))
import refugio_editorial as E  # noqa: E402
from comp_core import Comp, MXW, AU, CL, geo  # noqa: E402

OUT = os.path.join(BASE, '13_CARTOGRAFIA_Y_PROCESO')
W25 = E.np_aud('walk.npy').astype(bool)
PL25 = E.np_aud('plaza.npy').astype(bool)
ny, nx = E.np_cli('u_E2_16_B.npy').shape
W = W25[::2, ::2][:ny, :nx]

c = Comp(os.path.join(OUT, 'ATLAS_CARTOGRAFICO_v006.pdf'), 'ATLAS CARTOGRÁFICO',
         'CARTOGRAFÍA TÉCNICA v006')

E.portada(c.doc, 'Atlas\ncartográfico',
          'Una lámina por campo medido sobre la baseline v006 build 12. Todo lo que el '
          'proyecto sabe de sí mismo, expresado como mapa: la red peatonal, los gálibos, '
          'las causas de obstrucción, la sombra, la radiación de verano y de invierno, la '
          'temperatura radiante, el estrés térmico, el refugio efectivo, la nebulización, '
          'las horas de sol, el potencial de estancia y la accesibilidad.',
          'CARTOGRAFÍA TÉCNICA · TODOS LOS CAMPOS, TODOS SOBRE LA MISMA GEOMETRÍA',
          [('LÁMINAS', '24'), ('CELDA', '0,25 / 0,50 m'),
           ('ÁMBITO', '10.756 m²'), ('BASELINE', 'v006 · build 12')], num='ATLAS')

FAM_ORDER = ['CONTEXTO', 'ESTRUCTURA', 'CINTA', 'MÓDULOS', 'DOSEL', 'JARDINERAS',
             'VEGETACIÓN', 'MOBILIARIO', 'AGUA']


def lamina(titulo, subtitulo, arr, cmap, leyenda, lectura, vmin=None, vmax=None,
           mask=None, celda='0,50 m', fuente='', puntos=None, discreto=None):
    """Lamina a pagina completa: titulo, mapa grande, leyenda, lectura y fuente."""
    c.nueva()
    c.y = c.p.kicker(c.y, 'ATLAS · ' + titulo.upper())
    c.y = c.p.title(c.y, subtitulo, size=16)
    alto = MXW / c.ASPECTO
    ax = c.p.axes(E.MX, c.y - alto - 0.1, MXW, alto)
    E.draw_context(ax, geo)
    im = None
    if arr is not None:
        im = E.show_raster(ax, arr, cmap, vmin=vmin, vmax=vmax, mask=mask)
    if puntos is not None:
        puntos(ax)
    c.y -= alto + 0.42
    if im is not None:
        E.cbar(c.p, im, E.MX, c.y, 1.9, leyenda)
        c.y -= 0.30
    c.y = c.p.body(E.MX, c.y - 0.12, lectura, wrap=106, size=8.0)
    c.p.text(E.MX, c.y - 0.04, (fuente or 'FUENTE: baseline v006 build 12') +
             ' · celda %s · ámbito −112..100 × −45..78 m' % celda, size=5.4, color=E.GRAYTX)


# ============================================================ RED Y GEOMETRIA
width = E.np_aud('width.npy')
lamina('A1 · ANCHURA LIBRE', 'Cuánto sitio hay para pasar',
       np.clip(width, 0, 14), E.CMAP_VERDE, 'ANCHURA LIBRE LOCAL · M',
       'La anchura libre local es el doble de la distancia al obstáculo más próximo: mide '
       'el sitio real que tiene un cuerpo, no la distancia entre fachadas. El verde intenso '
       'marca las grandes bolsas de holgura; los pasillos claros entre jardineras son los '
       'que la auditoría vigila. La mediana del suelo pisable supera los 5,5 m y el peor '
       'cuello entre accesos conserva 10,75 m: la plaza sigue siendo plaza.',
       mask=PL25 & (width > 0), celda='0,25 m',
       fuente='FUENTE: _reaudit9/_data/width.npy (módulo A1)')

lamina('A1 · SUELO PISABLE', 'Dónde se puede estar de pie',
       np.where(W25, 1.0, np.nan), E.CMAP_VERDE, 'SUELO PISABLE · BANDA DE CUERPO 0,05–2,10 M',
       'Máscara binaria del suelo transitable en la banda de cuerpo: todo lo que no está '
       'ocupado por estructura, mobiliario, agua construida, jardineras o vegetación en el '
       'rango de 5 cm a 2,10 m de altura. Son 9.827 m² de los 10.756 m² del ámbito. Es la '
       'base sobre la que se calculan todas las estadísticas de este dossier: cuando el '
       'documento dice «media sobre pisable», se refiere exactamente a este mapa.',
       vmin=0, vmax=1.4, mask=W25, celda='0,25 m',
       fuente='FUENTE: _reaudit9/_data/walk.npy (módulo A0)')

cause = E.np_aud('cause.npy')
lamina('A0 · CAUSA DE OBSTRUCCIÓN', 'Qué familia ocupa cada metro',
       np.where(cause > 0, cause, np.nan), E.CMAP_ROSA, 'FAMILIA CAUSANTE · 1 A 9',
       'Cada celda ocupada se atribuye a la familia que la ocupa, en orden de prioridad: '
       'contexto urbano, estructura, cinta, módulos, dosel, jardineras, vegetación, '
       'mobiliario y agua. Este mapa es el que permite responder «¿quién estrecha este '
       'paso?» sin abrir el modelo, y el que sostiene la atribución de causa de cada '
       'incidencia del registro de auditoría.',
       vmin=1, vmax=9, celda='0,25 m',
       fuente='FUENTE: _reaudit9/_data/cause.npy (módulo A0) · orden: ' + ' · '.join(FAM_ORDER))

clf = E.np_aud('clear_firme.npy')
lamina('A2 · GÁLIBO FIRME', 'Qué altura libre hay sobre la cabeza',
       clf, E.CMAP_AGUA, 'ALTURA LIBRE BAJO ELEMENTO FIRME · M',
       'Solo se computan familias firmes: una copa baja es una cuestión de poda, no un '
       'defecto de proyecto, y por eso la vegetación se evalúa en un mapa aparte. Las zonas '
       'oscuras son los puntos donde la cinta y las hojas vuelan más bajo. El criterio de '
       'proyecto son 3,00 m libres sobre suelo pisable; las manchas que no lo cumplen están '
       'catalogadas una a una en el registro de incidencias.',
       vmin=2, vmax=12, mask=W25, celda='0,25 m',
       fuente='FUENTE: _reaudit9/_data/clear_firme.npy (módulo A2)')

clv = E.np_aud('clear_veg.npy')
lamina('A2 · GÁLIBO VEGETAL', 'La altura de la vegetación, medida aparte',
       clv, E.CMAP_VERDE, 'ALTURA LIBRE BAJO VEGETACIÓN · M',
       'El mismo cálculo, restringido a las familias vegetales. Se publica separado porque '
       'su gestión es distinta: donde el gálibo firme obliga a rediseñar, el gálibo vegetal '
       'se corrige con una poda de temporada. Comparando ambos mapas se ve qué parte de la '
       'sensación de cobijo procede de la arquitectura y qué parte del jardín.',
       vmin=1.5, vmax=10, mask=W25, celda='0,25 m',
       fuente='FUENTE: _reaudit9/_data/clear_veg.npy (módulo A2)')

# ============================================================ CLIMA
lamina('CLI · SOMBRA ACTUAL', 'La plaza que hoy no tiene sombra',
       E.np_cli('shade_crit_A.npy'), E.CMAP_AGUA, 'FRACCIÓN DE SOMBRA · VENTANA CRÍTICA',
       'Fracción de las horas críticas del trimestre 15 jun – 15 sep que cada celda pasa en '
       'sombra, en el estado actual. La media del suelo pisable es del 3,2 %: prácticamente '
       'todo el mapa está en blanco. Las únicas manchas azules proceden de las sombras '
       'arrojadas por las fachadas a primera y última hora, y del arbolado existente.',
       vmin=0, vmax=1, mask=W, fuente='FUENTE: _reclima9/_data/shade_crit_A.npy')

lamina('CLI · SOMBRA PROPUESTA', 'La sombra que el proyecto fabrica',
       E.np_cli('shade_crit_B.npy'), E.CMAP_AGUA, 'FRACCIÓN DE SOMBRA · VENTANA CRÍTICA',
       'El mismo cálculo con el refugio construido: la media sube al 38,3 % del suelo '
       'pisable y 3.669 m² superan el 50 % de sombra durante la ventana crítica. La '
       'estructura del mapa importa tanto como la cifra: el anillo perimetral y las bandas '
       'de la cinta concentran la protección mientras el vacío central se conserva '
       'deliberadamente despejado para los usos ceremoniales de la plaza.',
       vmin=0, vmax=1, mask=W, fuente='FUENTE: _reclima9/_data/shade_crit_B.npy')

lamina('CLI · HORAS DE SOL', 'Cuántas horas de sol recibe cada metro',
       E.np_cli('sunhours_B.npy'), E.CMAP_CALOR, 'HORAS DE SOL ACUMULADAS · VENTANA CRÍTICA',
       'Horas acumuladas con transmitancia solar superior al 50 % durante todo el trimestre '
       'crítico. Es la traducción temporal del mapa de sombra: donde la sombra es alta, las '
       'horas de sol caen. El promedio pasa de 1.215 a 670 horas — el suelo de Sol recibe '
       'literalmente la mitad de sol del verano.',
       mask=W, fuente='FUENTE: _reclima9/_data/sunhours_B.npy')

lamina('CLI · RADIACIÓN ACTUAL', 'La energía que hoy golpea el suelo',
       E.np_cli('rad_A.npy'), E.CMAP_CALOR, 'RADIACIÓN MEDIA · W/M² · VENTANA CRÍTICA',
       'Media de radiación global (directa más difusa) sobre el suelo durante la ventana '
       'crítica: 653,9 W/m². Esta es la energía que después se convierte en temperatura de '
       'superficie, en emisión de onda larga hacia el cuerpo humano y, en última instancia, '
       'en la sensación de que la plaza es inhabitable a las cuatro de la tarde.',
       mask=W, fuente='FUENTE: _reclima9/_data/rad_A.npy')

lamina('CLI · RADIACIÓN PROPUESTA', 'La energía que el dosel retira',
       E.np_cli('rad_B.npy'), E.CMAP_CALOR, 'RADIACIÓN MEDIA · W/M² · VENTANA CRÍTICA',
       'La misma magnitud con el refugio: 380,3 W/m² de media, un 38 % menos. Bajo las '
       'hojas densas la retirada alcanza el 100 %. Compárese con la lámina anterior en la '
       'misma escala de color: la diferencia entre ambas es el presupuesto energético con '
       'el que se compra todo el confort de este proyecto.',
       vmin=0, vmax=float(np.nanpercentile(E.np_cli('rad_A.npy')[W], 98)), mask=W,
       fuente='FUENTE: _reclima9/_data/rad_B.npy')

rd = E.np_cli('rad_delta.npy')
lamina('CLI · DELTA DE RADIACIÓN', 'Dónde exactamente se retira la energía',
       rd, E.CMAP_DELTA, 'Δ RADIACIÓN B−A · W/M²',
       'Diferencia celda a celda. El verde intenso marca los focos donde el dosel retira '
       'más energía; el blanco, las zonas que el proyecto decidió no tocar. Este mapa es la '
       'huella energética real de la intervención — y la razón por la que la sombra, y no '
       'el agua ni la vegetación, es el mecanismo dominante del refugio.',
       mask=W, fuente='FUENTE: _reclima9/_data/rad_delta.npy')

lamina('CLI · INVIERNO ACTUAL', 'El sol de diciembre que hoy llega',
       E.np_cli('radwin_A.npy'), E.CMAP_CALOR, 'RADIACIÓN 21-DIC · KWH/M²·DÍA',
       'Radiación acumulada del solsticio de invierno en el estado actual: 2,30 kWh/m² de '
       'media diaria. En invierno el sol está bajo y las propias fachadas de la plaza '
       'proyectan sombras largas: obsérvese que la mitad norte ya está en penumbra sin '
       'necesidad de ningún dosel.',
       mask=W, fuente='FUENTE: _reclima9/_data/radwin_A.npy')

lamina('CLI · INVIERNO PROPUESTA', 'El precio invernal, mapeado',
       E.np_cli('radwin_B.npy'), E.CMAP_CALOR, 'RADIACIÓN 21-DIC · KWH/M²·DÍA',
       'Con el refugio: 1,29 kWh/m²·día, un 40,3 % menos. Este es el coste que el proyecto '
       'paga por su beneficio de verano, y se publica con el mismo peso. La geometría lo '
       'gobierna parcialmente: 5.690 m² —el 58 % del suelo pisable— conservan al menos la '
       'mitad de su sol invernal, porque las hojas se concentran donde el verano es letal y '
       'el corazón de la plaza queda abierto.',
       vmin=0, vmax=float(np.nanmax(E.np_cli('radwin_A.npy'))), mask=W,
       fuente='FUENTE: _reclima9/_data/radwin_B.npy')

for esc, nom in (('E2', 'DÍA CALUROSO p95'),):
    lamina('CLI · MRT ACTUAL', 'La pared radiante de la plaza de hoy',
           E.np_cli('f_%s_16_A_Tmrt.npy' % esc), E.CMAP_CALOR, 'MRT · °C · %s · 16 H' % nom,
           'Temperatura radiante media a 1,10 m: la temperatura que la piel siente de '
           'verdad, integrando el sol directo, el difuso, el reflejado y la emisión '
           'infrarroja de todas las superficies visibles. La media de 65,2 °C explica por '
           'qué a las cuatro de la tarde nadie se detiene en Sol: no es el aire a 33 °C, es '
           'el granito emitiendo.',
           vmin=30, vmax=75, mask=W, fuente='FUENTE: _reclima9/_data/f_E2_16_A_Tmrt.npy')
    lamina('CLI · MRT PROPUESTA', 'El mosaico térmico del refugio',
           E.np_cli('f_%s_16_B_Tmrt.npy' % esc), E.CMAP_CALOR, 'MRT · °C · %s · 16 H' % nom,
           'La misma magnitud con el proyecto: 54,3 °C de media, con caídas locales de '
           'hasta 38,8 K bajo el dosel denso. La plaza deja de ser una superficie térmica '
           'homogénea y se convierte en un mosaico donde el usuario puede elegir. Los '
           'máximos supervivientes son los claros deliberados y las bandas junto a las '
           'fachadas soleadas.',
           vmin=30, vmax=75, mask=W, fuente='FUENTE: _reclima9/_data/f_E2_16_B_Tmrt.npy')

dM = E.np_cli('f_E2_16_B_Tmrt.npy') - E.np_cli('f_E2_16_A_Tmrt.npy')
lamina('CLI · DELTA MRT', 'Los once grados, repartidos',
       dM, E.CMAP_DELTA, 'Δ MRT B−A · K · DÍA p95 · 16 H',
       'Diferencia de temperatura radiante celda a celda. La media del suelo pisable es de '
       '−10,9 K y dentro del refugio efectivo alcanza los −28,2 K. Las escasas zonas rojas '
       'son las celdas que pierden factor de cielo sin ganar sombra: el mecanismo está '
       'demostrado en el hallazgo D-001 y su corrección conocida.',
       vmin=-30, vmax=10, mask=W, fuente='FUENTE: diferencia de f_E2_16_*_Tmrt.npy')

lamina('CLI · UTCI ACTUAL', 'El estrés térmico que hoy soporta la plaza',
       E.np_cli('u_E2_16_A.npy'), E.CMAP_CALOR, 'UTCI · °C · DÍA p95 · 16 H',
       'El índice universal de clima térmico integra aire, radiación, viento y humedad en '
       'una sola temperatura equivalente. Casi todo el suelo de la plaza actual está en la '
       'categoría oficial de estrés por calor MUY FUERTE (38 a 46 °C): 9.035 m² de los '
       '9.827 m² pisables.',
       vmin=30, vmax=44, mask=W, fuente='FUENTE: _reclima9/_data/u_E2_16_A.npy')

lamina('CLI · UTCI PROPUESTA', 'El mapa que resume el proyecto',
       E.np_cli('u_E2_16_B.npy'), E.CMAP_CALOR, 'UTCI · °C · DÍA p95 · 16 H',
       'Con el refugio, 3.451 m² abandonan la categoría MUY FUERTE y pasan a FUERTE. No es '
       'un cambio cosmético: es la diferencia entre una superficie que expulsa a la gente y '
       'otra donde esperar, cultivar o jugar resulta posible. La media baja 2,5 K y en los '
       'programas de estancia llega a 5,9 K.',
       vmin=30, vmax=44, mask=W, fuente='FUENTE: _reclima9/_data/u_E2_16_B.npy')

dU = E.np_cli('u_E2_16_B.npy') - E.np_cli('u_E2_16_A.npy')
lamina('CLI · DELTA UTCI', 'Dónde mejora y dónde empeora',
       dU, E.CMAP_DELTA, 'Δ UTCI B−A · K · DÍA p95 · 16 H',
       'El mapa más honesto del dossier. Verde: la propuesta enfría, hasta 6 K en los '
       'programas de estancia. Rojo: la propuesta calienta — 755 m² en este escenario, '
       'que crecen a 1.175 m² en ola de calor. Esas celdas pierden el 53 % de su factor de '
       'cielo conservando su sol; el mecanismo está probado y la regla de diseño que se '
       'deriva es «sombra o cielo, nunca media medida».',
       vmin=-6, vmax=6, mask=W, fuente='FUENTE: diferencia de u_E2_16_*.npy')

ref = E.np_cli('refugio.npy')
lamina('CLI · CLASES DE REFUGIO', 'La clasificación final del suelo',
       np.where(np.nan_to_num(ref) > 0, ref, np.nan), E.CMAP_VERDE,
       'CLASE · 0 SIN MEJORA · 1 LEVE · 2 MODERADA · 3 REFUGIO EFECTIVO',
       'Cuatro clases según la mejora sostenida de sensación térmica. La clase superior '
       '—refugio efectivo— suma 3.876 m², y 4.377 m² con la nebulización activa. Es la '
       'cifra que este dossier defiende ante el Ayuntamiento, y este el mapa que la '
       'sostiene: no un porcentaje abstracto, sino un contorno concreto sobre la plaza.',
       vmin=0, vmax=3, mask=W, fuente='FUENTE: _reclima9/_data/refugio.npy')

lamina('CLI · NEBULIZACIÓN', 'La nube que deriva con el viento',
       np.where(E.np_cli('mist_dT.npy') > 0.02, E.np_cli('mist_dT.npy'), np.nan),
       E.CMAP_AGUA, 'Δ TEMPERATURA DEL AIRE POR NEBULIZACIÓN · K',
       'Cobertura y efecto de los 42 nebulizadores, modelados con deriva por viento '
       'dominante y perfil gaussiano de dispersión, no como círculos rígidos. El '
       'enfriamiento local llega a 2-3 K en la zona cubierta y añade 501 m² de refugio '
       'efectivo. Es el sistema más eficiente por litro — y el más condicional: con humedad '
       'alta la depresión psicrométrica se hunde y la niebla deja de servir.',
       fuente='FUENTE: _reclima9/_data/mist_dT.npy')

# ============================================================ USO Y ACCESIBILIDAD
ipe = np.load(os.path.join(BASE, '06_USO_SOCIAL_Y_EXPERIENCIA', 'B_DATOS', 'ipe.npy'))
lamina('SOC · POTENCIAL DE ESTANCIA', 'Dónde querrá quedarse la gente',
       ipe, E.CMAP_VERDE, 'ÍNDICE DE POTENCIAL DE ESTANCIA · 0 A 0,8',
       'Índice con fórmula publicada: 30 % sombra, 30 % confort térmico, 15 % asiento '
       'disponible, 10 % proximidad al agua y 15 % condición de borde. Sometido a variación '
       'de sus pesos en ±50 %, el mapa de estancia alta conserva un índice de coincidencia '
       'de 0,74: es sensible pero no arbitrario. El 90,7 % de la estancia alta cae dentro '
       'del refugio térmico — la inversión social y la climática son la misma.',
       vmin=0, vmax=0.8, fuente='FUENTE: 06_USO_SOCIAL/B_DATOS/ipe.npy')

dst = np.load(os.path.join(BASE, '02_MOVILIDAD_Y_ACCESIBILIDAD', 'B_DATOS', 'dist_accesos.npy'))
lamina('MOB · DISTANCIA A SALIDA', 'A qué distancia real está la salida más próxima',
       dst, E.CMAP_CALOR, 'DISTANCIA GEODÉSICA AL ACCESO MÁS PRÓXIMO · M',
       'Distancia calculada bordeando obstáculos mediante frente de onda sobre el suelo '
       'pisable, no en línea recta: es la distancia que una persona recorre de verdad. '
       'Media de 41 m, percentil 95 de 63 m y máximo de 101 m, con el 100 % del suelo '
       'conectado a alguna salida. El refugio no crea fondos de saco de evacuación.',
       vmin=0, vmax=120, celda='0,25 m',
       fuente='FUENTE: 02_MOVILIDAD/B_DATOS/dist_accesos.npy')

a7 = AU['a7_views']
pts7 = np.array(a7['pts']); vis7 = np.array(a7['vis']['RELOJ'], bool)


def _vis(ax):
    ax.scatter(pts7[~vis7][:, 0], pts7[~vis7][:, 1], s=1.2, c='#ddd6cc', zorder=4)
    ax.scatter(pts7[vis7][:, 0], pts7[vis7][:, 1], s=1.8, c=E.AGUA, zorder=5)
    ax.plot(-25.2, -34.35, '*', ms=13, c=E.INK, zorder=6)


lamina('PAT · VISIBILIDAD DEL RELOJ', 'Desde dónde se ve el reloj de Gobernación',
       None, None, '',
       'Azul: los 2.455 puntos de muestreo con línea de visión libre al reloj (estrella). '
       'Gris: los que la han perdido. El 41,5 % de la superficie conserva la vista, pero '
       'solo el 25,5 % de las zonas de estancia alta — y en cambio el 48,9 % del flujo '
       'peatonal. El proyecto separó papeles sin declararlo: quien pasa ve, quien se queda '
       'no. Los 896 m² donde coinciden confort y vista son un recurso escaso a proteger.',
       puntos=_vis, celda='muestreo 2.455 pts',
       fuente='FUENTE: _reaudit9/_data/a7_views.json (módulo A7)')

mn = AU['a9_maint']


def _mant(ax):
    xs = [q['x'] for q in mn]; ys = [q['y'] for q in mn]
    pl = [q['requiere_plataforma'] for q in mn]
    ax.scatter([x for x, p in zip(xs, pl) if not p], [y for y, p in zip(ys, pl) if not p],
               s=11, c=E.GREEN, edgecolors='white', linewidths=0.35, zorder=5,
               label='acceso a pie')
    ax.scatter([x for x, p in zip(xs, pl) if p], [y for y, p in zip(ys, pl) if p],
               s=15, c=E.MAGENTA, marker='^', edgecolors='white', linewidths=0.35,
               zorder=6, label='requiere plataforma elevadora')
    ax.legend(fontsize=5.6, frameon=False, loc='lower left')


lamina('TEC · PUNTOS DE MANTENIMIENTO', 'Los 160 elementos que alguien tendrá que cuidar',
       None, None, '',
       'Cada punto es un elemento que durante veinticinco años habrá que revisar, limpiar o '
       'sustituir: depósitos, bajantes, boquillas de niebla, cámaras de microalgas, bombas, '
       'luminarias, juntas. Los triángulos exigen plataforma elevadora, y su distribución '
       'determina tanto el coste del contrato de conservación como la frecuencia con que la '
       'plaza se ocupará parcialmente para mantenerla. 159 de los 160 tienen acceso '
       'auditado; el restante necesita una corrección trivial en proyecto de ejecución.',
       puntos=_mant, celda='puntos discretos',
       fuente='FUENTE: _reaudit9/_data/a9_maint.json (módulo A9)')

spots = CL['spots']


def _spots(ax):
    for s in spots.get('hot', []):
        ax.scatter(s['x'], s['y'], s=max(10, s['m2'] / 26), c='#c22a52', zorder=5,
                   edgecolors='white', linewidths=0.4)
    for c_ in CL['discos'] if isinstance(CL['discos'], list) else []:
        pass
    Mg = geo
    for cc in Mg['circulacion']['corridors']:
        p_ = cc.get('pts')
        if p_:
            ax.plot([q[0] for q in p_], [q[1] for q in p_], '-', color=E.AGUA, lw=1.3)


lamina('D-015 · CALOR RESIDUAL SOBRE EJES', 'El hallazgo que cambia la ejecución',
       np.where(np.nan_to_num(E.np_cli('shade_crit_B.npy')) > 0.5, 0.3, np.nan),
       E.CMAP_VERDE, 'SOMBRA ≥50 % (VERDE) · FOCOS DE CALOR (ROJO) · EJES (AZUL)',
       'Los focos de calor residual (rojo, tamaño proporcional a su superficie) aparecen '
       'sistemáticamente pegados a los ejes peatonales (azul). El 85 % del área caliente '
       'está a menos de 8 metros de un eje, y la causa es la propia regla de calidad que '
       'exige corredores despejados: al proteger el paso, se expulsó el dosel de los ejes y '
       'con él su sombra. La salida —sombra alta con gálibo superior a 3 m— es compatible '
       'con todas las reglas vigentes y es la mejora de mayor palanca del proyecto.',
       vmin=0, vmax=1, mask=W, puntos=_spots,
       fuente='FUENTE: cruce de spots.json × trazas de circulación (hallazgo D-015)')

n = c.cerrar()
print('ATLAS_CARTOGRAFICO ok:', n, 'pp')
