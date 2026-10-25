# -*- coding: utf-8 -*-
"""03B8_SCREENSHOT_BEFORE_AFTER.pdf — MISMAS camaras (aprox. de S06-S11 + QA), v004 vs v005."""
import os
import subprocess
import sys
import time

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
PORT = 8127
OUT = os.path.join(HERE, '_beforeafter8')
os.makedirs(OUT, exist_ok=True)

CAMS = [
    ('S06_escalera_rampa', -31.5, 24.5, 8.4, -36.3, 20.3, 5.6, 55),
    ('S08_fachada_eci',    -40.5, 6.5, 1.8, -57.0, 20.0, 4.5, 62),
    ('S09_escalera_mastiles', -33.2, 17.4, 1.7, -36.0, 19.6, 2.6, 58),
    ('S10_tiesto_50cm',    1.3, 3.9, 1.15, 0.35, 4.95, 0.55, 52),
    ('S11_desembarco',     -31.5, 24.5, 8.4, -36.3, 20.3, 6.1, 50),
    ('S04_aerea_c1',       -18.0, -22.0, 52.0, -55.0, 18.0, 4.0, 50),
    ('S05_aerea_c3',       30.0, -32.0, 46.0, 57.0, -5.0, 3.0, 50),
    ('QA_estacion',        47.5, -13.5, 1.75, 58.0, -2.5, 4.5, 62),
]


def shoot(carpeta, tag, cx, cy, cz, tx, ty, tz, fov):
    url = ('http://127.0.0.1:%d/%s/viewer_control.html?cx=%.2f&cy=%.2f&cz=%.2f&tx=%.2f&ty=%.2f'
           '&tz=%.2f&fov=%d&w=1500&h=950&mat=1' % (PORT, carpeta, cx, cy, cz, tx, ty, tz, fov))
    png = os.path.join(OUT, '%s_%s.png' % (tag[0], tag[1]))
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--screenshot=' + png,
                    '--window-size=1500,950', '--virtual-time-budget=30000',
                    '--default-background-color=FFFFFFFF', url], capture_output=True, timeout=300)
    return png


srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=HERE,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    with PdfPages(os.path.join(HERE, '03B8_SCREENSHOT_BEFORE_AFTER.pdf')) as pdf:
        for (nm, cx, cy, cz, tx, ty, tz, fov) in CAMS:
            p4 = shoot('_viewer_v004', (nm, 'v004'), cx, cy, cz, tx, ty, tz, fov)
            p5 = shoot('_viewer', (nm, 'v005'), cx, cy, cz, tx, ty, tz, fov)
            fig, axs = plt.subplots(1, 2, figsize=(16.5, 6.2))
            for ax, pth, lab in ((axs[0], p4, 'v004 (ANTES)'), (axs[1], p5, 'v005 (DESPUES)')):
                try:
                    ax.imshow(mpimg.imread(pth))
                except Exception:
                    pass
                ax.set_title('%s · %s' % (nm, lab), fontsize=10)
                ax.axis('off')
            fig.suptitle('03B.8 · MISMA CAMARA antes/despues — %s' % nm, fontsize=13, fontweight='bold')
            plt.tight_layout(rect=(0, 0, 1, 0.94))
            pdf.savefig(fig); plt.close(fig)
            print('pagina', nm)
finally:
    srv.terminate()
print('OK 03B8_SCREENSHOT_BEFORE_AFTER.pdf')
