# -*- coding: utf-8 -*-
"""03B.7 · Pares v003/v004 con LA MISMA camara para 03B7_V003_V004_BEFORE_AFTER.pdf.
Un solo http.server sirve la carpeta de fase: /_viewer_v003/ y /_viewer/ (v004)."""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
PORT = 8125
OUT = os.path.join(HERE, '_beforeafter')
os.makedirs(OUT, exist_ok=True)

# (nombre, cx, cy, cz, tx, ty, tz, fov) — mismas camaras para ambas versiones
SHOTS = [
    # Pagina A — El Corte Ingles: aerea del arco aplanado + portico, y calle junto a fachada
    ('A_eci_aerea',  -18.0, -22.0, 52.0, -55.0, 18.0, 4.0, 50),
    ('A_eci_calle',  -40.5, 6.5, 1.8, -57.0, 20.0, 4.5, 62),
    # Pagina B — Estacion de Cercanias: aerea del atrio/abrazo, y peatonal en la boca
    ('B_est_aerea',  30.0, -32.0, 46.0, 57.0, -5.0, 3.0, 50),
    ('B_est_boca',   47.5, -13.5, 1.75, 58.0, -2.5, 4.5, 62),
]


def shoot(prefix, viewer_dir, cx, cy, cz, tx, ty, tz, fov, w=1600, h=1000):
    url = ('http://127.0.0.1:%d/%s/viewer_control.html?cx=%.2f&cy=%.2f&cz=%.2f&tx=%.2f&ty=%.2f&tz=%.2f'
           '&fov=%d&w=%d&h=%d&mat=1' % (PORT, viewer_dir, cx, cy, cz, tx, ty, tz, fov, w, h))
    png = os.path.join(OUT, prefix + '.png')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu',
                    '--screenshot=' + png, '--window-size=%d,%d' % (w, h),
                    '--virtual-time-budget=22000', '--default-background-color=FFFFFFFF', url],
                   capture_output=True, timeout=300)
    ok = os.path.exists(png) and os.path.getsize(png) > 30000
    print(('OK  ' if ok else 'FALLO ') + prefix)
    return ok


srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=HERE,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
fallos = 0
try:
    for (nm, cx, cy, cz, tx, ty, tz, fov) in SHOTS:
        if not shoot(nm + '_v003', '_viewer_v003', cx, cy, cz, tx, ty, tz, fov):
            fallos += 1
        if not shoot(nm + '_v004', '_viewer', cx, cy, cz, tx, ty, tz, fov):
            fallos += 1
finally:
    srv.terminate()
print('fallos: %d' % fallos)
sys.exit(1 if fallos else 0)
