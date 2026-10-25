# -*- coding: utf-8 -*-
"""03B.9 · Productos: BOTANICAL_CONTACT_SHEET.pdf (§28) + V005_V006_CLOSE_RANGE.pdf (§34)."""
import csv
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
PORT = 8129
OUT = os.path.join(HERE, '_species')
os.makedirs(OUT, exist_ok=True)

# tomas dedicadas por especie: (rol, camara -> instancia conocida)
SPECIES_CAMS = [
    ('HELECHO', 'Nephrolepis exaltata', 0.95, 4.55, 0.95, 0.35, 4.95, 0.62, 50),
    ('CALATHEA', 'Calathea orbifolia', -10.9, 31.6, 0.95, -11.5, 32.2, 0.60, 50),
    ('GRAMINEA', 'Deschampsia cespitosa', 1.0, 4.2, 0.9, 0.35, 4.95, 0.58, 50),
    ('GRAMALTA', 'Miscanthus (tall grass)', -19.3, -15.4, 1.0, -20.0, -16.0, 0.55, 52),
    ('HELECHO2', 'helecho estilizado', -19.0, -14.6, 0.85, -19.8, -15.4, 0.45, 52),
    ('MONSTERA2', 'Monstera deliciosa L', 7.2, 12.4, 1.3, 6.4, 13.2, 0.75, 55),
    ('ALOCASIA2', 'Alocasia (big leaf)', 9.4, 10.9, 1.2, 8.6, 11.8, 0.8, 55),
    ('ALOCASIA', 'Anthurium', -50.2, 22.0, 0.95, -51.0, 22.7, 0.55, 52),
    ('NENUFAR', 'Nymphaea (water lilies)', 11.2, 20.0, 0.75, 12.2, 19.2, 0.4, 55),
    ('JUNCO', 'Typha (cattail)', 12.6, 17.6, 0.9, 13.3, 16.9, 0.7, 52),
    ('JUNCO2', 'Carex (sedge)', 11.4, 21.6, 0.8, 12.2, 20.9, 0.5, 52),
    ('ARBOLURB', 'Celtis/olmo urbano', 24.0, 30.0, 2.2, 28.0, 33.0, 3.0, 55),
    ('POTHOS', 'Epipremnum (colgante)', 4.2, 29.2, 7.4, 5.0, 30.0, 7.6, 55),
    ('MAIZ', 'cultivo por fases', -55.7, 5.4, 1.0, -56.5, 6.2, 0.7, 52),
    ('HUERTO', 'lineas de cultivo', -55.4, 5.1, 1.2, -56.7, 6.4, 0.5, 55),
    ('TREPADORA', 'Hedera (helice)', 0.95, 4.15, 1.75, 0.35, 4.85, 1.7, 52),
    ('ACUATICA', 'nenufar procedural', 12.4, 18.6, 0.6, 13.0, 18.0, 0.35, 52),
    ('ARBUSTO', 'Pittosporum (shrub_04)', -7.2, 25.2, 0.95, -8.0, 26.0, 0.55, 52),
    ('TANQUE_V', 'valvula de tanque (bonus)', -34.4, -17.4, 1.2, -35.0, -18.0, 1.1, 52),
]


def shoot(carpeta, png, cx, cy, cz, tx, ty, tz, fov, w=1200, h=800):
    url = ('http://127.0.0.1:%d/%s/viewer_control.html?cx=%.2f&cy=%.2f&cz=%.2f&tx=%.2f&ty=%.2f'
           '&tz=%.2f&fov=%d&w=%d&h=%d&mat=1' % (PORT, carpeta, cx, cy, cz, tx, ty, tz, fov, w, h))
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--screenshot=' + png,
                    '--window-size=%d,%d' % (w, h), '--virtual-time-budget=26000',
                    '--default-background-color=FFFFFFFF', url], capture_output=True, timeout=300)


CSVD = {}
try:
    with open(os.path.join(HERE, 'BOTANICAL_MASTERPLAN_v001.csv'), encoding='utf-8') as fo:
        for row in csv.DictReader(fo):
            CSVD[row['nombre_comun']] = row
except Exception:
    pass

srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=HERE,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    # ---- contact sheet
    pngs = []
    for (rol, nom, cx, cy, cz, tx, ty, tz, fov) in SPECIES_CAMS:
        png = os.path.join(OUT, rol + '.png')
        shoot('_viewer', png, cx, cy, cz, tx, ty, tz, fov)
        pngs.append((rol, nom, png))
    with PdfPages(os.path.join(HERE, 'BOTANICAL_CONTACT_SHEET.pdf')) as pdf:
        for pg in range(0, len(pngs), 6):
            fig, axs = plt.subplots(2, 3, figsize=(16.5, 10.5))
            for k, (rol, nom, png) in enumerate(pngs[pg:pg + 6]):
                ax = axs[k // 3][k % 3]
                try:
                    ax.imshow(mpimg.imread(png))
                except Exception:
                    pass
                ax.set_title('%s — %s' % (rol, nom), fontsize=9)
                ax.axis('off')
            for k in range(len(pngs[pg:pg + 6]), 6):
                axs[k // 3][k % 3].axis('off')
            fig.suptitle('BOTANICAL CONTACT SHEET v006 — especies en obra (fuentes/licencias: ASSET_PROVENANCE.csv)',
                         fontsize=12, fontweight='bold')
            plt.tight_layout(rect=(0, 0, 1, 0.95))
            pdf.savefig(fig); plt.close(fig)
    print('contact sheet OK')

    # ---- close range v005 vs v006 (mismas camaras)
    CAMS = [('planta_hero', 1.3, 3.9, 1.15, 0.35, 4.95, 0.55, 52),
            ('balsa', 10.2, 20.6, 0.9, 12.0, 19.0, 0.34, 55),
            ('arbolado', 22.0, 28.5, 2.0, 28.0, 33.0, 3.5, 55),
            ('canopy_borde', 4.4, 11.6, 6.9, 2.6, 10.2, 6.4, 55),
            ('tanque', -30.5, -15.5, 9.8, -35.0, -18.0, 9.5, 55),
            ('huerto', -55.6, 10.6, 1.4, -58.0, 12.0, 0.5, 55),
            ('ascensor', -66.8, 8.6, 1.6, -70.2, 6.2, 1.2, 58),
            ('atrio_metro', 53.0, -9.5, 2.4, 57.0, -4.0, 1.3, 58)]
    with PdfPages(os.path.join(HERE, 'V005_V006_CLOSE_RANGE.pdf')) as pdf:
        for (nm, cx, cy, cz, tx, ty, tz, fov) in CAMS:
            p5 = os.path.join(OUT, nm + '_v005.png')
            p6 = os.path.join(OUT, nm + '_v006.png')
            shoot('_viewer_v005', p5, cx, cy, cz, tx, ty, tz, fov)
            shoot('_viewer', p6, cx, cy, cz, tx, ty, tz, fov)
            fig, axs = plt.subplots(1, 2, figsize=(16.5, 6.2))
            for ax, pth, lab in ((axs[0], p5, 'v005'), (axs[1], p6, 'v006')):
                try:
                    ax.imshow(mpimg.imread(pth))
                except Exception:
                    pass
                ax.set_title('%s · %s' % (nm, lab), fontsize=10)
                ax.axis('off')
            fig.suptitle('03B.9 · CLOSE RANGE misma camara — %s' % nm, fontsize=12, fontweight='bold')
            plt.tight_layout(rect=(0, 0, 1, 0.93))
            pdf.savefig(fig); plt.close(fig)
    print('close range OK')
finally:
    srv.terminate()
