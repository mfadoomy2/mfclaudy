# -*- coding: utf-8 -*-
"""Driver reanudable de la campana final: un frame por invocacion de Blender,
salta los que ya existen. Relanzable las veces que haga falta."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = r'C:\Program Files\Blender Foundation\Blender 5.0\blender.exe'
OUT = os.path.join(HERE, 'hero_FINAL')
os.makedirs(OUT, exist_ok=True)

TANDAS = [(c, 'tarde', 256) for c in
          ('H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
           'F1_INTERIOR_DOSEL', 'F2_HUERTO', 'F3_ATRIO_ESTACION', 'F4_CARLOS_III',
           'F5_DETALLE_NUDO')] + \
         [('H7', 'mediodia', 256), ('H3', 'mediodia', 256),
          ('H7', 'clay', 192), ('H1', 'clay', 192)]

hechos = saltados = fallos = 0
for cam, luz, samples in TANDAS:
    dst = os.path.join(OUT, '%s_%s.png' % (cam, luz))
    if os.path.exists(dst) and os.path.getsize(dst) > 100_000:
        saltados += 1
        continue
    r = subprocess.run([B, '-b', '-P', os.path.join(HERE, 'bl_scene_v006.py'), '--',
                        'render', cam, luz, '2560', '1600', str(samples)],
                       capture_output=True, text=True, timeout=1800)
    ok = os.path.exists(dst) and os.path.getsize(dst) > 100_000
    print(('OK  ' if ok else 'FALLO ') + cam + ' ' + luz, flush=True)
    hechos += ok
    fallos += (not ok)
    if not ok:
        print((r.stdout or '')[-600:])
print('RESUMEN: %d nuevos, %d ya existian, %d fallos' % (hechos, saltados, fallos))
