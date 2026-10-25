# -*- coding: utf-8 -*-
"""03B.7 §controles · Renders de control 50m/10m/2m/50cm sobre la escena v004 detallada.
Regla del enunciado: 'Si algo funciona a 50 m pero a 50 cm parece falso: NO ESTA TERMINADO'."""
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
os.makedirs(OUT, exist_ok=True)

# (nombre, tx, ty, z_detalle, azimut_camara_deg)  — azimut = desde donde MIRA la camara (lado plaza)
TARGETS = [
    ('escalera',  -36.3, 20.3, 1.05, -35.0),    # STAIR@-38,19 anclada: narices/montantes/pletina
    ('carlos3',   -28.0, -14.0, 1.60, 55.0),    # estatua v2: molduras/patas/verja
    ('belvedere',  58.5, -0.5, 5.95, 185.0),    # cabeza de Estacion: fascia/goteron/balaustres
    ('mastil_pod', 0.0,  5.0,  2.20, -120.0),   # centro plaza: mastiles/pods/discos
]
# (etiqueta, distancia_m, delta_z_camara, fov)
DIST = [('50m', 50.0, 24.0, 58), ('10m', 10.0, 2.2, 55), ('2m', 2.0, 0.35, 55), ('50cm', 0.5, 0.05, 50)]


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
    for (nm, tx, ty, zdet, az) in TARGETS:
        for (lab, d, dz, fov) in DIST:
            a = math.radians(az)
            cx, cy = tx + d * math.cos(a), ty + d * math.sin(a)
            tz = (zdet + 2.5) if lab == '50m' else zdet
            cz = tz + dz
            if not shoot('CTRL_%s_%s' % (nm, lab), cx, cy, cz, tx, ty, tz, fov):
                fallos += 1
finally:
    srv.terminate()
print('fallos: %d' % fallos)
sys.exit(1 if fallos else 0)
