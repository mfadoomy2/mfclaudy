"""Cuenta las 150 escenas de escenas.csv y escribe las tablas de lo que tienen en común.

No decide nada: solo cuenta. La lectura va en 01_150_ESCENAS.md.
"""
import collections
import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(AQUI, '..', 'escenas.csv')

filas = list(csv.DictReader(open(CSV, encoding='utf-8')))
n = len(filas)


def tabla(titulo, clave, orden=None):
    c = collections.Counter(f[clave] for f in filas)
    claves = orden or [k for k, _ in c.most_common()]
    print(f'\n**{titulo}**\n')
    print('| valor | escenas | % |')
    print('|---|---|---|')
    for k in claves:
        print(f'| {k} | {c[k]} | {100 * c[k] / n:.0f} % |')


def hora(f):
    h, m = f['hora'].split(':')
    return int(h) + int(m) / 60


print(f'Escenas: {n}')
tabla('Dónde pasa', 'lugar')
tabla('Postura del cuerpo', 'cuerpo')
tabla('Con quién', 'con_quien')
tabla('Hay pantalla', 'pantalla')
tabla('Qué necesita respecto a ser vista u oída', 'exposicion')
tabla('Cuánto dura', 'dura', ['min', 'hora', 'horas', 'noche'])
tabla('Fuente', 'fuente')

# Horas
noche = sum(1 for f in filas if hora(f) >= 22 or hora(f) < 7)
print(f'\n**Hora**\n\nEntre las 22:00 y las 7:00 pasan {noche} escenas ({100 * noche / n:.0f} %).')
franjas = collections.Counter()
for f in filas:
    h = hora(f)
    franjas['07–12' if 7 <= h < 12 else '12–17' if 12 <= h < 17 else '17–22' if 17 <= h < 22 else '22–07'] += 1
print('\n| franja | escenas |\n|---|---|')
for k in ['07–12', '12–17', '17–22', '22–07']:
    print(f'| {k} | {franjas[k]} |')

# Cruces
def pct(cond):
    k = sum(1 for f in filas if cond(f))
    return k, f'{100 * k / n:.0f} %'

print('\n**Cruces**\n')
print('| condición | escenas | % |\n|---|---|---|')
cruces = [
    ('en la cama', lambda f: f['lugar'] == 'cama'),
    ('en la cama o en el suelo', lambda f: f['lugar'] in ('cama', 'suelo')),
    ('tumbada', lambda f: f['cuerpo'] == 'tumbada'),
    ('tumbada o sentada (sin mesa)', lambda f: f['cuerpo'] in ('tumbada', 'sentada') and f['lugar'] != 'mesa'),
    ('con pantalla', lambda f: f['pantalla'] == 'si'),
    ('en la cama y con pantalla', lambda f: f['lugar'] == 'cama' and f['pantalla'] == 'si'),
    ('en la cama y NO durmiendo (hay pantalla, otra persona o trabajo)', lambda f: f['lugar'] == 'cama' and (f['pantalla'] == 'si' or f['con_quien'] != 'sola')),
    ('sola o sola pero conectada', lambda f: f['con_quien'] in ('sola', 'sola_conectada')),
    ('sola pero conectada (cuerpo solo, compañía por pantalla)', lambda f: f['con_quien'] == 'sola_conectada'),
    ('quiere ocultarse o controlar lo que se ve y se oye', lambda f: f['exposicion'] in ('ocultarse', 'controlar')),
    ('quiere mostrarse', lambda f: f['exposicion'] == 'mostrarse'),
    ('en la mesa', lambda f: f['lugar'] == 'mesa'),
    ('en la cocina', lambda f: f['lugar'] == 'cocina'),
    ('en un espacio común de la casa (comun, cocina, mesa)', lambda f: f['lugar'] in ('comun', 'cocina', 'mesa')),
    ('fuera de la casa', lambda f: f['lugar'] == 'fuera'),
    ('con sonido que cruza un tabique (cascos, audios, micro, altavoz, voz, máquina)', lambda f: any(w in f['escena'].lower() for w in ('casco', 'audio', 'micro', 'altavoz', 'tabique', 'oye', 'oigan', 'voz alta', 'resuen', 'ruido', 'suena', 'golpes', 'lavadora', 'tapones'))),
    ('el móvil o el portátil aparece nombrado', lambda f: any(w in f['escena'].lower() for w in ('móvil', 'portátil', 'pantalla', 'chat', 'videollamada', 'online', 'app', 'vídeo', 'tableta', 'ordenador'))),
    ('dormir, siesta o insomnio', lambda f: any(w in f['escena'].lower() for w in ('duerme', 'dormir', 'siesta', 'insomnio', 'alarma', 'despertador'))),
    ('la casa es provisional (maleta, mudanza, casero, subarriendo, padres, cajas, alquiler)', lambda f: any(w in f['escena'].lower() for w in ('maleta', 'mudanza', 'casero', 'subarrienda', 'padres', 'cajas', 'alquil', 'idealista', 'colchón', 'abuela'))),
]
for nombre, cond in cruces:
    k, p = pct(cond)
    print(f'| {nombre} | {k} | {p} |')

# Por fuente, dónde pasa
print('\n**Dónde pasa, según la fuente**\n')
fuentes = [k for k, _ in collections.Counter(f['fuente'] for f in filas).most_common()]
lugares = ['cama', 'suelo', 'mesa', 'cocina', 'bano', 'umbral', 'comun', 'fuera']
print('| fuente | n | ' + ' | '.join(lugares) + ' |')
print('|---|---|' + '---|' * len(lugares))
for fu in fuentes:
    sub = [f for f in filas if f['fuente'] == fu]
    c = collections.Counter(f['lugar'] for f in sub)
    print(f'| {fu} | {len(sub)} | ' + ' | '.join(str(c[l]) for l in lugares) + ' |')
