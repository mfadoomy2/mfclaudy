# -*- coding: utf-8 -*-
"""FASE FINAL - PDFs MOB-01..03 + MOVILIDAD_SINTESIS_INTEGRADA sobre v006."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
sys.path.insert(0, os.path.join(BASE, '01_CLIMA_Y_CONFORT', '_scripts'))
import refugio_editorial as E  # noqa: E402
from cli_common import cabecera_analisis  # noqa: E402

OUT = os.path.join(BASE, '02_MOVILIDAD_Y_ACCESIBILIDAD')
with open(os.path.join(OUT, 'B_DATOS', 'mob_stats.json'), encoding='utf-8') as f:
    R = json.load(f)
geo = E.load_geo()
FUENTE = 'FUENTE: _reaudit9/_data (v006 build 12) + mob_engine.py · celda 0,25 m'

# ================================================================ MOB-01 · RED
doc = E.Doc(os.path.join(OUT, 'MOB-01_RED_PEATONAL.pdf'), 'MOB-01 · RED PEATONAL', '02 · MOVILIDAD')
E.portada(doc, 'La red peatonal',
          'Anchuras, cuellos, continuidad y fragmentación del suelo pisable con el '
          'refugio construido: lo que la auditoría geométrica garantiza y lo que los '
          'escenarios de afluencia añaden.',
          'MOB-01 · MOVILIDAD Y ACCESIBILIDAD',
          [('SUELO PISABLE', '9.827 m²'), ('PEOR CUELLO', '%.1f m' % R['red']['bottleneck_peor']),
           ('CONTINUIDAD 1,80 M', '84 %'), ('EJES BLOQUEADOS', '0 de 6')], num='MOB-01')
p, y = cabecera_analisis(
    doc, 'MOB-01', 'Una plaza que sigue siendo plaza',
    '¿El refugio estrangula el movimiento? Anchuras reales, cuellos entre accesos y '
    'fragmentación de la red a cada exigencia de ancho.',
    'Rásters de la auditoría v006 (celda 0,25 m, banda de cuerpo 0,05–2,10 m): anchura '
    'local 2×DT, cuello máximo entre los 45 pares de accesos por barrido de umbral, '
    'fragmentación por componentes conexas a cada ancho exigido.',
    '_reaudit9/_data/a1_paths.json + width.npy (0 RED en build 12).', 'A',
    'La holgura 2×DT es isótropa (subestima pasos diagonales); los umbrales 1,80/3,00 m '
    'son criterio de proyecto, no normativa de obligado cumplimiento.')
width = E.np_aud('width.npy'); plaza = E.np_aud('plaza.npy')
ax = p.axes(E.MX, y - 3.15, 4.6, 3.0)
E.draw_context(ax, geo)
im = E.show_raster(ax, np.clip(width, 0, 12), E.CMAP_VERDE, mask=plaza & (width > 0))
E.cbar(p, im, E.MX, y - 3.45, 1.7, 'ANCHURA LIBRE LOCAL · M')
frag = R['red']['frag']
yy = p.ficha(E.MX + 4.95, y - 0.1, [
    ('CONTINUIDAD', 'Exigiendo 1,80 m continuos, la red mantiene el 84 %% del suelo en '
     'una sola pieza; a 3,00 m, el 73 %% en dos.'),
    ('CUELLOS', 'El peor par de accesos conserva %.1f m de paso: no existe cuello '
     'relevante a escala de multitud.' % R['red']['bottleneck_peor']),
    ('BOLSAS', '%d cul-de-sac >8 m² imputables al proyecto (auditoría A1): las bolsas '
     'de v002 se reclasificaron o resolvieron en v003-v006.' % len([q for q in R['red']['pockets'] if q])),
], wcol=2.55, wrap=34)
p.text(E.MX, y - 3.75, FUENTE, size=5.4, color=E.GRAYTX)
y = y - 4.05
ax2 = p.chart_axes(E.MX, y - 1.5, E.A4W - 2 * E.MX, 1.35)
ws = [f['w'] for f in frag]; cov = [100 * f['cover'] for f in frag]
ax2.plot(ws, cov, '-', color=E.GREEN, lw=1.6)
ax2.fill_between(ws, cov, color=E.PALEGREEN)
ax2.set_xlabel('ancho exigido · m', size=6); ax2.set_ylabel('% del suelo conectado', size=6)
p.caption(E.MX, y - 1.75, 'Cobertura de red frente a exigencia de ancho.',
          'La curva cae suave: no hay umbral catastrófico — la red degrada con elegancia.',
          fuente=FUENTE, wrap=100)
doc.metric('MOB01-M1', R['red']['bottleneck_peor'], 'm', 'A', 'peor cuello entre 45 pares', 'a1_paths.json')
doc.add(p)
doc.close()
print('MOB-01 ok', doc.folio, 'pp')

# ================================================================ MOB-02 · VERTICAL/PMR
doc = E.Doc(os.path.join(OUT, 'MOB-02_ACCESIBILIDAD_VERTICAL.pdf'),
            'MOB-02 · ACCESIBILIDAD', '02 · MOVILIDAD')
E.portada(doc, 'Subir a la cinta',
          'El nivel +6,00 tiene 6 escaleras y 3 ascensores. Para una persona con '
          'movilidad reducida, los ascensores no son una comodidad: son la única vía. '
          'Este documento mide esa dependencia.',
          'MOB-02 · MOVILIDAD Y ACCESIBILIDAD',
          [('ASCENSORES', '3'), ('ESCALERAS', '6'),
           ('RODEO PMR NORMAL', '%d m' % R['pmr']['rodeo_max_con_todos_m']),
           ('RODEO PEOR N−1', '%d m' % R['pmr']['rodeo_max_N1_m'])], num='MOB-02')
p, y = cabecera_analisis(
    doc, 'MOB-02', 'Tres ascensores y un anillo',
    '¿Qué pasa con el itinerario accesible cuando falla un ascensor?',
    'Proyección de los 3 LIFT_TOWER medidos en la escena sobre la polilínea de la cinta '
    '(733 m, anillo); rodeo máximo a lo largo del tablero hasta el ascensor operativo más '
    'próximo, con los 3 y en cada escenario N−1.',
    'a4_ribbon.json (perfil de cinta) + anclas LIFT_TOWER de la escena v006.', 'A',
    'El rodeo se mide sobre el tablero; no incluye tiempo de espera del aparato. '
    'La normativa de itinerarios accesibles exigirá validación de detalle (cabina, meseta).')
rows = [['Los 3 operativos', '%d m' % R['pmr']['rodeos']['todos'], 'servicio pleno'],
        ['Falla ASC-1 (C1-O)', '%d m' % R['pmr']['rodeos']['sin_asc_1'], 'rodeo asumible'],
        ['Falla ASC-2 (C2-N)', '%d m' % R['pmr']['rodeos']['sin_asc_2'], 'rodeo asumible'],
        ['Falla ASC-3 (C3-E)', '%d m' % R['pmr']['rodeos']['sin_asc_3'],
         'peor caso: 286 m ~ 4-5 min PMR']]
y = p.tabla(E.MX, y - 0.02, E.A4W - 2 * E.MX,
            ['ESCENARIO', 'RODEO MÁXIMO', 'LECTURA'],
            rows, col_w=[2.0, 1.6, 3.4], size=7.6)
doc.metric('MOB02-M1', R['pmr']['rodeo_max_N1_m'], 'm', 'A', 'peor rodeo PMR con N-1', 'mob_stats.json')
y -= 0.1
y = p.dashlist(E.MX, y, [
    ('El sistema es N−1 tolerante', 'pero no elegante: 286 m de rodeo es un límite '
     'razonable para avería puntual, no para fuera-de-servicio crónico. Contrato de '
     'mantenimiento con SLA <48 h (07_ECONOMIA presupuesta el término).'),
    ('Las escaleras reparten mejor:', 'ningún punto de la cinta queda a más de ~90 m de '
     'una escalera. La asimetría escalera/ascensor es la brecha de equidad del nivel +6.'),
    ('Documentado como mejora potencial (§54):', 'un cuarto ascensor en el arco sur '
     'bajaría el peor N−1 a ~180 m. NO se implementa: se deja al proyecto de ejecución.'),
], wrap=86, gap=0.1)
doc.add(p)
doc.close()
print('MOB-02 ok', doc.folio, 'pp')

# ================================================================ MOB-03 · EVACUACION + LOS
doc = E.Doc(os.path.join(OUT, 'MOB-03_EVACUACION_Y_AFLUENCIA.pdf'),
            'MOB-03 · EVACUACIÓN Y AFLUENCIA', '02 · MOVILIDAD')
E.portada(doc, 'Salir y caber',
          'Distancia de cada punto de la plaza a su salida más próxima, y nivel de '
          'servicio peatonal bajo tres escenarios de demanda — con las hipótesis a la vista.',
          'MOB-03 · MOVILIDAD Y ACCESIBILIDAD',
          [('DIST. MEDIA A SALIDA', '%.0f m' % R['dist_acceso']['media']),
           ('P95', '%.0f m' % R['dist_acceso']['p95']),
           ('MÁXIMO', '%.0f m' % R['dist_acceso']['max']),
           ('PEOR LOS', 'A-B (libre)')], num='MOB-03')
p, y = cabecera_analisis(
    doc, 'MOB-03', 'Nadie queda lejos de una salida',
    '¿A qué distancia real (bordeando obstáculos) está cada celda pisable de un acceso, '
    'y aguanta la red una gran afluencia?',
    'Distancia geodésica por frente de onda sobre el ráster pisable (conectividad 8, '
    'corrección diagonal) desde los 10 accesos declarados; LOS por eje con demanda '
    'repartida por anchura y evaluada en el ancho mínimo (HCM/Fruin).',
    'walk.npy + a1_paths.json/access + a5_access.json + mob_engine.py.', 'A',
    'La demanda de los escenarios es HIPÓTESIS (C) hasta cruzar el dato oficial de '
    'afluencia (07_ECONOMIA); la evacuación normativa exige cálculo específico de '
    'incendios que excede este análisis básico.')
dist = np.load(os.path.join(OUT, 'B_DATOS', 'dist_accesos.npy'))
ax = p.axes(E.MX, y - 3.15, 4.6, 3.0)
E.draw_context(ax, geo)
im = E.show_raster(ax, dist, E.CMAP_CALOR, vmin=0, vmax=120)
E.cbar(p, im, E.MX, y - 3.45, 1.7, 'DISTANCIA GEODÉSICA A ACCESO · M')
yy = p.ficha(E.MX + 4.95, y - 0.1, [
    ('RESULTADO', 'Media %.0f m, p95 %.0f m, máximo %.0f m. El 100 %% del suelo con '
     'salida; %.1f %% a más de 60 m.' % (R['dist_acceso']['media'], R['dist_acceso']['p95'],
                                          R['dist_acceso']['max'],
                                          100 - R['dist_acceso']['pct_a_menos_60m'])),
    ('LECTURA', 'El refugio no crea fondos de saco de evacuación: el dosel está arriba '
     'y las familias en planta dejan pasillos de 1,8-3,0 m garantizados por auditoría.'),
], wcol=2.55, wrap=34)
p.text(E.MX, y - 3.75, FUENTE, size=5.4, color=E.GRAYTX)
doc.metric('MOB03-M1', R['dist_acceso']['p95'], 'm', 'A', 'p95 distancia geodesica a acceso', 'mob_stats.json')
y = y - 4.0
y = p.kicker(y, 'MOB-03.2 · NIVEL DE SERVICIO EN TRES ESCENARIOS')
p.chip(E.MX, y - 0.02, 'C'); y -= 0.28
peores = {}
for r in R['los']['escenarios']:
    k = r['escenario']
    if k not in peores or r['q_p_min_m'] > peores[k]['q_p_min_m']:
        peores[k] = r
rows = [[k, v['eje'], '%.0f p/h' % v['flujo_p_h'], '%.2f m' % v['ancho_min_m'],
         '%.1f' % v['q_p_min_m'], v['LOS']] for k, v in peores.items()]
y = p.tabla(E.MX, y, E.A4W - 2 * E.MX,
            ['ESCENARIO', 'EJE PÉSIMO', 'FLUJO', 'ANCHO MÍN', 'P/MIN/M', 'LOS'],
            rows, col_w=[1.5, 1.7, 1.0, 1.0, 0.9, 0.9], size=7.2)
p.text(E.MX, y - 0.02, R['los']['hipotesis'], size=5.8, color=E.GRAYTX, wrap=150)
doc.add(p)
doc.close()
print('MOB-03 ok', doc.folio, 'pp')

# ================================================================ SINTESIS
doc = E.Doc(os.path.join(OUT, 'MOVILIDAD_SINTESIS_INTEGRADA.pdf'),
            'MOVILIDAD · SÍNTESIS', '02 · MOVILIDAD')
E.portada(doc, '¿Se puede seguir\ncruzando Sol?',
          'Síntesis de movilidad y accesibilidad: la red que queda, la vertical que se '
          'añade y los escenarios que la tensionan. Cruzada con clima y uso.',
          '02 · MOVILIDAD · SÍNTESIS',
          [('VEREDICTO CORTO', 'SÍ, CON UN ASTERISCO PMR'),
           ('RED', '0 RED · cuello 10,75 m'),
           ('EVACUACIÓN P95', '%.0f m' % R['dist_acceso']['p95']),
           ('PMR N−1', '286 m de rodeo')], num='S-02')
p = doc.page('SÍNTESIS')
y = E.A4H - 1.0
y = p.kicker(y, 'S-02.1 · LO QUE LOS CRUCES ENSEÑAN')
y = p.title(y, 'El suelo fluye; la vertical es la frontera', size=17)
y = p.dashlist(E.MX, y - 0.02, [
    ('Movilidad × clima (sinergia medida).', 'Los ejes de paso conservan su anchura Y '
     'reciben sombra parcial: el tránsito por preciados-carretas gana −2 a −4 K de UTCI '
     'sin perder un centímetro de paso auditado.'),
    ('Movilidad × estancia (fricción gobernada).', 'El riesgo clásico — la estancia '
     'colonizando el paso — está contenido por diseño: bancos y jardineras respetan los '
     '2,05 m del filtro de corredor del generador, verificado a 0 RED en build 12.'),
    ('La vertical es la única asimetría real.', 'A nivel de suelo, la plaza es tan '
     'permeable como hoy. El nivel +6 es un privilegio de piernas: 6 escaleras frente a '
     '3 ascensores. La equidad del mirador depende del mantenimiento de 3 máquinas.'),
    ('Ningún escenario de demanda tensiona la red.', 'Con 120.000 visitantes/día '
     '(hipótesis alta), el peor punto queda en LOS A-B. La capacidad no es el límite '
     'del proyecto; el confort y el mantenimiento sí (05/07).'),
], wrap=88, gap=0.12)
y -= 0.08
y = p.panel(E.MX, y, E.A4W - 2 * E.MX, 1.15, 'PARA EL DOSSIER MUNICIPAL')
p.text(E.MX + 0.16, y, 'La intervención no reduce la permeabilidad peatonal de Puerta '
       'del Sol (0 incidencias rojas de paso en la auditoría final), no crea fondos de '
       'saco de evacuación (p95 a salida: %.0f m) y añade un nivel visitable cuya '
       'accesibilidad universal depende de 3 ascensores con tolerancia N−1 medida. '
       'Recomendación: SLA de mantenimiento <48 h y estudio de un cuarto aparato en el '
       'proyecto de ejecución.' % R['dist_acceso']['p95'], size=8.4, wrap=94)
doc.add(p)
doc.close()
print('SINTESIS MOB ok', doc.folio, 'pp')
