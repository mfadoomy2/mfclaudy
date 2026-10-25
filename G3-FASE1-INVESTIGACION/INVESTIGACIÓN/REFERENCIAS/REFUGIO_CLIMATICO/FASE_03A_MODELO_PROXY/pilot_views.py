# -*- coding: utf-8 -*-
"""Renderiza las 8 vistas del fragmento piloto."""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
VIEWER = os.path.join(HERE, '_viewer', 'viewer_pilot.html').replace('\\', '/')
OUT = os.path.join(HERE, 'vistas_piloto')
os.makedirs(OUT, exist_ok=True)
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
EYE = 1.65

VIEWS = [
    ('VISTA01_recorrido', (2, -4, EYE), (14, 20, 4.0), 64, None),
    ('VISTA02_bajo_hojas', (10, 10, EYE), (4, 18, 6.5), 70, None),
    ('VISTA03_estancia', (4, 0, EYE), (10, 10, 1.1), 62, None),
    ('VISTA04_capsulas', (10, 20, EYE), (17, 28, 2.2), 62, None),
    ('VISTA05_veg_estructura', (24, 4, EYE), (8, 14, 5.0), 66, None),
    ('VISTA06_hacia_correos', (12, 16, EYE), (-25.2, -34, 14.0), 58, None),
    ('VISTA07_elevada', (-2, 28, 7.4), (14, 8, 1.5), 62, None),
    ('VISTA08_axonometria', (52, -48, 44), (12, 14, 2), 0, 21),
]

for (name, cam, tgt, fov, ortho) in VIEWS:
    url = 'file:///%s?cx=%s&cy=%s&cz=%s&tx=%s&ty=%s&tz=%s&fov=%s&w=1600&h=1000' % (
        VIEWER, cam[0], cam[1], cam[2], tgt[0], tgt[1], tgt[2], fov)
    if ortho:
        url += '&ortho=%s' % ortho
    png = os.path.join(OUT, name + '.png')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--screenshot=' + png,
                    '--window-size=1600,1000', '--virtual-time-budget=9000',
                    '--default-background-color=FFFFFFFF', url], capture_output=True, timeout=120)
    ok = os.path.exists(png) and os.path.getsize(png) > 20000
    print(('OK  ' if ok else 'FALLO ') + name)
