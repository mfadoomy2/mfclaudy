# -*- coding: utf-8 -*-
"""REGISTRO DE PROCESO — vuelca el forense (240+ eventos) a formato legible: CSV
navegable + PDF con la cronologia, los errores y las decisiones."""
import csv
import io
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
MONT = os.path.normpath(os.path.join(BASE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
sys.path.insert(0, os.path.join(BASE, '12_ANEXOS_DATOS_Y_METODO', '_scripts'))
import refugio_editorial as E  # noqa: E402
from comp_core import Comp, MXW  # noqa: E402

OUT = os.path.join(BASE, '13_CARTOGRAFIA_Y_PROCESO')
DST = os.path.join(OUT, 'D_REGISTROS_FORENSES')
os.makedirs(DST, exist_ok=True)

EV = []
p = os.path.join(MONT, '_FORENSIC_PROCESS', 'FORENSIC_EVENTS.jsonl')
for ln in io.open(p, encoding='utf-8'):
    ln = ln.strip()
    if not ln:
        continue
    try:
        EV.append(json.loads(ln))
    except Exception:
        pass


def g(e, *ks):
    for k in ks:
        v = e.get(k)
        if v:
            return v
    return ''


# ---------------------------------------------------------------- CSV navegable
campos = ['id', 'fecha', 'fase', 'tipo', 'objetivo', 'resultado']
rows = []
for e in EV:
    rows.append({
        'id': g(e, 'run_id', 'event_id', 'id'),
        'fecha': str(g(e, 'inicio', 'timestamp', 'ts', 'fecha'))[:19],
        'fase': g(e, 'fase'),
        'tipo': g(e, 'tipo_evento', 'tipo'),
        'objetivo': str(g(e, 'objetivo'))[:300],
        'resultado': str(g(e, 'resultado', 'diagnostico'))[:900],
    })
with io.open(os.path.join(DST, 'REGISTRO_FORENSE_COMPLETO.csv'), 'w', encoding='utf-8-sig',
             newline='') as f:
    w = csv.DictWriter(f, fieldnames=campos)
    w.writeheader(); w.writerows(rows)

# ---------------------------------------------------------------- PDF de proceso
c = Comp(os.path.join(OUT, 'REGISTRO_DE_PROCESO.pdf'), 'REGISTRO DE PROCESO',
         'TRAZABILIDAD FORENSE')
tipos = Counter(r['tipo'] for r in rows if r['tipo'])
fases = Counter(r['fase'] for r in rows if r['fase'])
E.portada(c.doc, 'Registro\nde proceso',
          'El proyecto se hizo con un protocolo forense: cada ejecución, cada error, cada '
          'decisión y cada corrección quedaron registrados con fecha, objetivo, resultado y '
          'archivos producidos. Este documento vuelca ese registro — %d eventos — a formato '
          'legible, porque un proceso que no se puede auditar no es un método, es una '
          'anécdota.' % len(EV),
          'TRAZABILIDAD COMPLETA · %d EVENTOS FECHADOS' % len(EV),
          [('EVENTOS', str(len(EV))), ('TIPOS', str(len(tipos))),
           ('FASES', str(len(fases))), ('FORMATO', 'JSONL append-only')],
          num='PROCESO')

c.seccion('P.1 · QUÉ SE REGISTRA', 'El protocolo, en seis reglas', size=16)
c.lista([
    ('Append-only.', 'El registro no se edita ni se reescribe: solo crece. Un evento '
     'equivocado se corrige con otro evento que lo declara, nunca borrándolo.'),
    ('Evidencia, no narrativa.', 'Cada entrada guarda el comando ejecutado, la ruta de los '
     'archivos producidos, su tamaño y su estado; no una descripción de lo que se pretendía.'),
    ('Campo inexistente = nulo.', 'Si un dato no se midió, el campo queda vacío. Nunca se '
     'rellena con una estimación disfrazada.'),
    ('Los errores son eventos de primera clase.', 'Un fallo se registra con su traza, su '
     'diagnóstico y el evento que lo originó — con el mismo estatus que un éxito.'),
    ('Las decisiones llevan alternativas.', 'Cada decisión de proyecto registra qué se '
     'eligió, qué se descartó y con qué criterio.'),
    ('Todo output tiene padre.', 'Ningún archivo entregado existe sin un evento que lo '
     'produjo y sin la ejecución que puede reproducirlo.'),
], wrap=100)

c.tabla(['TIPO DE EVENTO', 'CUÁNTOS'],
        [[k, str(v)] for k, v in tipos.most_common(24)], [4.6, 2.4], size=6.8,
        titulo='P.2 · REPARTO POR TIPO DE EVENTO')
if fases:
    c.tabla(['FASE', 'EVENTOS'], [[k, str(v)] for k, v in fases.most_common(20)],
            [4.6, 2.4], size=6.8, titulo='P.3 · REPARTO POR FASE')

# errores destacados
err = [r for r in rows if r['tipo'] in ('error', 'ERROR') or 'error' in (r['tipo'] or '')]
if err:
    c.tabla(['ID', 'FECHA', 'QUÉ FALLÓ Y CÓMO SE DIAGNOSTICÓ'],
            [[r['id'][:12], r['fecha'][:16], (r['objetivo'] + ' — ' + r['resultado'])[:230]]
             for r in err[:40]], [0.85, 1.05, 5.1], size=5.8, row_h=0.28,
            titulo='P.4 · ERRORES REGISTRADOS (primeros 40)')

# cronologia de cierres y decisiones
hitos = [r for r in rows if r['tipo'] in ('cierre', 'decision', 'snapshot_baseline',
                                          'state_change', 'veredicto')]
if hitos:
    c.tabla(['FECHA', 'TIPO', 'HITO'],
            [[r['fecha'][:16], r['tipo'][:14], (r['objetivo'] or r['resultado'])[:210]]
             for r in hitos[:60]], [1.05, 1.0, 4.95], size=5.8, row_h=0.26,
            titulo='P.5 · CRONOLOGÍA DE HITOS, DECISIONES Y CIERRES')

c.panel('POR QUÉ ESTO ACOMPAÑA AL DOSSIER',
        'Porque la diferencia entre un proyecto asistido por máquina que se puede defender '
        'y uno que no, es exactamente esta: la capacidad de responder «¿cómo llegaste a '
        'eso?» con un archivo, no con un recuerdo. Cualquier cifra de este paquete se puede '
        'seguir hacia atrás hasta la ejecución que la produjo, y desde ahí hasta la '
        'geometría exacta que la generó.', alto=1.0)

n = c.cerrar()
print('REGISTRO_DE_PROCESO ok: %d pp · %d eventos volcados a CSV' % (n, len(rows)))
