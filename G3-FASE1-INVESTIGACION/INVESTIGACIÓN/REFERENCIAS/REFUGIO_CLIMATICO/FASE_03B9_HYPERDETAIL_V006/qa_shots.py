# -*- coding: utf-8 -*-
"""03B.8 · QA visual de iteracion: tomas en los nudos de defecto de las capturas del autor."""
import math
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
PORT = 8126
OUT = os.path.join(HERE, '_qa')
os.makedirs(OUT, exist_ok=True)

IT = sys.argv[1] if len(sys.argv) > 1 else 'i1'
SHOTS = [
    ('aerea_c1',   -18.0, -22.0, 52.0, -55.0, 18.0, 4.0, 50),
    ('nudo_escalera', -31.5, 24.5, 8.4, -36.3, 20.3, 5.6, 55),
    ('portico_eci', -40.5, 6.5, 1.8, -57.0, 20.0, 4.5, 62),
    ('tiesto_mastil', 1.3, 3.9, 1.15, 0.35, 4.95, 0.55, 52),
    ('estacion',   47.5, -13.5, 1.75, 58.0, -2.5, 4.5, 62),
    ('aerea_c3',   30.0, -32.0, 46.0, 57.0, -5.0, 3.0, 50),
    ('escalera_pie', -33.2, 17.4, 1.7, -36.0, 19.6, 2.6, 58),
]


def shoot(name, cx, cy, cz, tx, ty, tz, fov, w=1600, h=1000):
    url = ('http://127.0.0.1:%d/viewer_control.html?cx=%.2f&cy=%.2f&cz=%.2f&tx=%.2f&ty=%.2f&tz=%.2f'
           '&fov=%d&w=%d&h=%d&mat=1' % (PORT, cx, cy, cz, tx, ty, tz, fov, w, h))
    png = os.path.join(OUT, '%s_%s.png' % (name, IT))
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--screenshot=' + png,
                    '--window-size=%d,%d' % (w, h), '--virtual-time-budget=30000',
                    '--default-background-color=FFFFFFFF', url], capture_output=True, timeout=300)
    ok = os.path.exists(png) and os.path.getsize(png) > 30000
    print(('OK  ' if ok else 'FALLO ') + png.split(os.sep)[-1])


srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)],
                       cwd=os.path.join(HERE, '_viewer'),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    for s in SHOTS:
        shoot(*s)
finally:
    srv.terminate()
print('ok')
