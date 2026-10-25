# -*- coding: utf-8 -*-
"""03B.7 · Ronda 2 de controles: reencuadres + verificacion de la correccion (estatua, trepadora, baja)."""
import math
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
PORT = 8124
VIEWER = 'http://127.0.0.1:%d/viewer_control.html' % PORT
OUT = os.path.join(HERE, '_control')

EX, EY = -28.0, -14.0
# (nombre, cx, cy, cz, tx, ty, tz, fov)
SHOTS = [
    ('CTRL_escalera_2m_b',  -34.6, 22.9, 1.9, -36.3, 20.3, 1.05, 55),
    ('CTRL_escalera_50cm_b', -36.0, 21.0, 1.15, -36.3, 20.55, 0.95, 50),
    ('CTRL_carlos3_10m_b',  EX + 8.2, EY - 5.8, 4.2, EX, EY, 3.6, 55),
    ('CTRL_carlos3_2m_b',   EX + 3.9, EY - 2.6, 3.4, EX + 1.2, EY, 3.5, 55),
    ('CTRL_carlos3_50cm_b', EX + 4.9, EY - 3.4, 0.9, EX + 4.45, EY - 3.05, 0.52, 50),
    ('CTRL_trepadora_2m_b', 2.0, 3.6, 1.9, 0.3, 5.1, 1.8, 55),
    ('CTRL_mastil_50cm_b',  0.9, 4.4, 2.25, 0.35, 4.95, 2.2, 50),
    ('CTRL_baja_1m_b',      -19.2, -15.2, 1.1, -20.0, -16.0, 0.35, 55),
]


def shoot(name, cx, cy, cz, tx, ty, tz, fov, w=1600, h=1000):
    url = '%s?cx=%.2f&cy=%.2f&cz=%.2f&tx=%.2f&ty=%.2f&tz=%.2f&fov=%d&w=%d&h=%d&mat=1' % (
        VIEWER, cx, cy, cz, tx, ty, tz, fov, w, h)
    png = os.path.join(OUT, name + '.png')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu',
                    '--screenshot=' + png, '--window-size=%d,%d' % (w, h),
                    '--virtual-time-budget=22000', '--default-background-color=FFFFFFFF', url],
                   capture_output=True, timeout=300)
    ok = os.path.exists(png) and os.path.getsize(png) > 30000
    print(('OK  ' if ok else 'FALLO ') + name + ((' %d KB' % (os.path.getsize(png) // 1024)) if ok else ''))
    return ok


srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)],
                       cwd=os.path.join(HERE, '_viewer'),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
fallos = 0
try:
    for s in SHOTS:
        if not shoot(*s):
            fallos += 1
finally:
    srv.terminate()
print('fallos: %d' % fallos)
sys.exit(1 if fallos else 0)
