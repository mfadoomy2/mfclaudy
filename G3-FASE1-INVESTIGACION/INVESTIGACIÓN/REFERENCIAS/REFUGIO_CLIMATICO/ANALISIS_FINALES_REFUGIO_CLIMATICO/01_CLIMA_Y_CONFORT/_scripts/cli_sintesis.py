# -*- coding: utf-8 -*-
"""FASE FINAL - CLIMA_SINTESIS_INTEGRADA.pdf: el documento que cruza CLI-01..10
y responde a la pregunta principal: ¿funciona realmente como refugio climatico?"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
import refugio_editorial as E  # noqa: E402
from cli_common import FUENTE, W, geo  # noqa: E402

OUT = os.path.join(BASE, '01_CLIMA_Y_CONFORT')
with open(os.path.join(OUT, 'B_DATOS', 'cli_stats.json'), encoding='utf-8') as f:
    R = json.load(f)

doc = E.Doc(os.path.join(OUT, 'CLIMA_SINTESIS_INTEGRADA.pdf'),
            'CLIMA · SÍNTESIS INTEGRADA', '01 · CLIMA')

E.portada(doc, '¿Funciona como\nrefugio climático?',
          'Síntesis integrada de los diez análisis climáticos sobre la baseline v006: '
          'qué mecanismo produce el beneficio, dónde funciona mejor y peor, para quién, '
          'cuándo y bajo qué condiciones — con las contradicciones a la vista.',
          '01 · CLIMA Y CONFORT · SÍNTESIS',
          [('VEREDICTO CORTO', 'SÍ, CON CONDICIONES'),
           ('REFUGIO EFECTIVO', '3.876–4.377 m²'),
           ('ΔUTCI P95', '−2,5 K'), ('COSTE CLAVE', 'invierno −40 %')],
          num='S-01')

# ---------------------------------------------------------------- 1 · la respuesta
p = doc.page('LA RESPUESTA')
y = E.A4H - 1.0
y = p.kicker(y, 'S-01.1 · LA RESPUESTA, SIN RODEOS')
y = p.title(y, 'Sí: es un refugio. No: no es un milagro.', size=18)
y = p.subtitle(y, 'La pregunta admite respuesta medida. Un tercio largo del suelo de Sol '
                  'pasa a ser refugio térmico efectivo en el peor mes del año; el aire '
                  'apenas cambia; el invierno paga un precio localizado; y hay 755 m² '
                  'donde la propuesta empeora las cosas — están mapeados y explicados.')
x = E.MX
p.bignum(x, y, '36–41', '%', 'del ámbito analizado es refugio efectivo (sin/con niebla)'); x += 2.35
p.bignum(x, y, '−10,9', 'K', 'de temperatura radiante media (el mecanismo)'); x += 2.35
p.bignum(x, y, '−2,5', 'K', 'de UTCI medio en el día caluroso p95'); x += 2.15
y -= 1.35
y = p.kicker(y, 'S-01.2 · QUÉ MECANISMO PRODUCE EL BENEFICIO')
y = p.tabla(E.MX, y, E.A4W - 2 * E.MX,
            ['MECANISMO', 'APORTE AL CONFORT', 'CONSUME', 'FALLA SI'],
            [['Sombra estructural (dosel)', '~85 % del ΔMRT; el motor del refugio',
              'nada en operación', 'nunca (es geometría)'],
             ['Agua evaporativa (láminas+splash)', '−0,4 K de aire local; superficies frías',
              '1.820 L/h en punta', 'corte de agua'],
             ['Nebulización', '−0,7 K UTCI y +501 m² de refugio en día seco',
              '210 L/h', 'humedad alta / avería'],
             ['Vegetación', '286 kW latentes; ±1 p.p. de sombra; experiencia',
              '~9 m³/día de riego (04_AGUA)', 'sequía prolongada'],
             ['Superficies (albedo/agua)', 'evita re-emisión; Ts granito muy superior a agua/vegetal',
              'mantenimiento', 'suciedad/vaciado']],
            col_w=[2.0, 2.6, 1.4, 1.4], size=7.0)
p.text(E.MX, y - 0.05, FUENTE + ' · síntesis de CLI-01..CLI-07', size=5.4, color=E.GRAYTX)
doc.add(p)

# ---------------------------------------------------------------- 2 · donde/cuando/quien
p = doc.page('DÓNDE · CUÁNDO · QUIÉN')
y = E.A4H - 1.0
y = p.kicker(y, 'S-01.3 · DÓNDE FUNCIONA MEJOR Y PEOR')
y = p.title(y, 'El mapa de la verdad', size=16)
dU = E.np_cli('u_E2_16_B.npy') - E.np_cli('u_E2_16_A.npy')
ax = p.axes(E.MX, y - 3.3, 4.9, 3.15)
E.draw_context(ax, geo)
im = E.show_raster(ax, dU, E.CMAP_DELTA, vmin=-6, vmax=6, mask=W)
E.cbar(p, im, E.MX, y - 3.6, 1.7, 'ΔUTCI B−A · K · E2 16H')
yy = p.ficha(E.MX + 5.25, y - 0.1, [
    ('MEJOR', 'Bancos (−5,2 K), huerto (−5,9 K), vivero y borde de balsas: los programas '
     'de estancia se colocaron deliberadamente bajo el dosel denso.'),
    ('PEOR', 'El claro ceremonial central (sin cambio, por diseño), la cinta a +6 m '
     '(38,0 °C UTCI: mirador, no estancia) y la cola positiva de 755 m².'),
    ('PARA QUIÉN', 'El refugio protege al que espera, cultiva o pasea a nivel de suelo. '
     'No al que camina la cinta al sol de las 16 h.'),
    ('CUÁNDO', 'Rinde más cuanto peor es el día (clases UTCI), pero su cola de '
     'empeoramiento también crece: 55 › 755 › 1.175 m² en E1 › E2 › E3.'),
], wcol=2.35, wrap=32)
p.text(E.MX, y - 3.9, FUENTE, size=5.4, color=E.GRAYTX)
doc.add(p)

# ---------------------------------------------------------------- 3 · sinergias y contradicciones
p = doc.page('SINERGIAS Y CONTRADICCIONES')
y = E.A4H - 1.0
y = p.kicker(y, 'S-01.4 · LO QUE SE REFUERZA Y LO QUE SE CONTRADICE')
y = p.title(y, 'Cinco cruces que cambian la lectura', size=16)
y = p.dashlist(E.MX, y - 0.02, [
    ('Sombra × cielo (contradicción medida).', 'Quitar cielo sin dar sombra EMPEORA: '
     'las 3.021 celdas de la cola positiva perdieron el 53 % de su factor de cielo '
     'conservando su sol (Δtau −0,01). La misma pérdida de cielo CON sombra (Δtau −0,75) '
     'es la que produce los −5 K. El dosel debe ser sombra o ser transparente: '
     'a medias, calienta.'),
    ('Niebla × humedad (dependencia).', 'La nebulización rinde 3,5 K psicrométricos en '
     'día seco y 0,13 K aplicados en día húmedo: es un sistema condicional, no un '
     'mecanismo de base. Activación por sensor de depresión psicrométrica (roadmap).'),
    ('Vegetación × agua (asimetría).', 'La vegetación consume el agua de forma continua '
     '(riego diario) pero su beneficio térmico directo es el término menor; su valor '
     'está en superficies, biodiversidad y experiencia. El agua "cara" es la de la '
     'niebla — y es la más eficiente por litro en su ventana.'),
    ('Verano × invierno (trade-off).', 'La sombra crítica 3,4 › 42,3 % cuesta −40 % de sol '
     'el 21-dic. La geometría del dosel (hojas discontinuas, claro central) deja el 58 % '
     'del suelo con ≥50 % de su sol invernal: el trade-off está gobernado, no eliminado.'),
    ('Confort × movimiento (frontera).', 'El refugio es un fenómeno de ESTANCIA: los '
     'ejes de paso siguen siendo transitables al sol como hoy. Nadie está obligado a '
     'refugiarse — y el que cruza en 40 segundos apenas lo nota. La métrica correcta '
     'para el peatón en tránsito es la de 06_USO_SOCIAL (exposición acumulada).'),
], wrap=88, gap=0.12)
doc.add(p)

# ---------------------------------------------------------------- 4 · vulnerabilidades + condiciones
p = doc.page('VULNERABILIDADES')
y = E.A4H - 1.0
y = p.kicker(y, 'S-01.5 · VULNERABILIDADES Y DEPENDENCIAS FUNCIONALES')
y = p.title(y, 'De qué depende que esto funcione', size=16)
y = p.tabla(E.MX, y, E.A4W - 2 * E.MX,
            ['DEPENDENCIA', 'GRADO', 'EVIDENCIA', 'MITIGACIÓN'],
            [['Agua de red', 'MEDIA', 'sin agua: −0,43 K aire, niebla OFF; sombra intacta',
              'depósitos 24-48 h + prioridad riego'],
             ['Mantenimiento del canopy', 'ALTA (local)', 'cámara seca: +6,9 K MRT en 700 m²',
              'inspección quincenal, registro por disco'],
             ['Estado vegetal', 'BAJA (térmica)', 'LAI −30 %: sombra −1 p.p.',
              'especies xerófilas en borde, hidrozonas'],
             ['Viento no resuelto', 'INCERTIDUMBRE', 'hasta +0,55 K UTCI si abrigo −50 %',
              'CFD o anemometría en piloto (fase B)'],
             ['Meteorología', 'CONDICIONAL', 'niebla inútil en día húmedo; E3 mantiene −2,0 K',
              'control por depresión psicrométrica']],
            col_w=[1.7, 1.15, 2.9, 1.65], size=7.0)
y -= 0.1
y = p.panel(E.MX, y, E.A4W - 2 * E.MX, 1.7, 'LA RESPUESTA LARGA (PARA EL DOSSIER MUNICIPAL)')
p.text(E.MX + 0.16, y,
       'Sí funciona: como sistema de ESTANCIA para el peor trimestre, con un mecanismo '
       'dominante (sombra estructural) que no consume recursos y una corona de sistemas '
       'húmedos que refinan el resultado cuando el clima lo permite. Sus dos costes '
       'estructurales — el sol de invierno y los 755 m² de cielo perdido sin sombra a '
       'cambio — están mapeados, cuantificados y son gobernables con ajuste fino local. '
       'Sus dos incertidumbres — viento y comportamiento real de uso — tienen plan de '
       'validación definido. Ninguna cifra de este dossier requiere fe: todas son '
       'reproducibles desde la baseline congelada v006.', size=8.4, wrap=94)
doc.metric('S01-M1', '36-41', '%', 'A', 'refugio efectivo pisable', 'refugio.json')
doc.add(p)
doc.close()
print('SINTESIS ok', doc.folio, 'pp')
