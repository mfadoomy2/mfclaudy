# -*- coding: utf-8 -*-
"""E01: 6 vistas de direccion de arte + 6 previews de material."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VIEWER = 'http://127.0.0.1:8123/viewer_e01.html'   # servido por http.server (headless bloquea texturas file://)
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
EYE = 1.65

DA = [   # las 6 camaras aprobadas
    ('DA_V07_reloj', (6, 8, EYE), (-25.2, -36.5, 15.0), 58),
    ('DA_V06_bajo_C1', (-56, 2, EYE), (-44, 18, 5.5), 68),
    ('DA_V13_splash', (24, -10, EYE), (14, -1, 1.2), 66),
    ('DA_V10_cupula', (22, -4, EYE), (33, 5, 4.5), 68),
    ('DA_V19_sobre_cinta', (-17.5, 25.8, 7.35), (10, 12, 6.0), 66),
    ('DA_V05_banda_correos', (-2, -18, EYE), (6, 16, 5.0), 62),
]
EXP_OVERRIDE = {'DA_V05_banda_correos': 1.1}
PREV = [  # previews de material (primeros planos en contexto)
    ('MATPREV_pod_tpu', (18.5, 22.5, 1.5), (15.5, 27.2, 2.0), 42),
    ('MATPREV_canopy_membrana', (-46, 8, 1.6), (-50, 12, 5.2), 52),
    ('MATPREV_madera_nudo', (-32, 3, 1.7), (-28, 6, 9.0), 46),
    ('MATPREV_estanque_algas', (8, 17, 1.4), (11, 21, 0.5), 50),
    ('MATPREV_granito_humedo', (20, -6, 1.6), (15, -2, 0.1), 54),
    ('MATPREV_red_rosa', (-32, 4, 1.1), (-28, 1, 0.4), 48),
]


def shoot(outdir, name, cam, tgt, fov, exp=1.2, w=1920, h=1200):
    url = '%s?cx=%s&cy=%s&cz=%s&tx=%s&ty=%s&tz=%s&fov=%s&w=%d&h=%d&exp=%s' % (
        VIEWER, cam[0], cam[1], cam[2], tgt[0], tgt[1], tgt[2], fov, w, h, exp)
    png = os.path.join(outdir, name + '.png')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--allow-file-access-from-files',
                    '--screenshot=' + png, '--window-size=%d,%d' % (w, h), '--virtual-time-budget=16000',
                    '--default-background-color=FFFFFFFF', url], capture_output=True, timeout=180)
    ok = os.path.exists(png) and os.path.getsize(png) > 30000
    print(('OK  ' if ok else 'FALLO ') + name)
    return ok


if __name__ == '__main__':
    sel = sys.argv[1:] or None
    d1 = os.path.join(HERE, 'direccion_arte'); os.makedirs(d1, exist_ok=True)
    d2 = os.path.join(HERE, 'material_previews'); os.makedirs(d2, exist_ok=True)
    for (name, cam, tgt, fov) in DA:
        if sel and not any(s in name for s in sel):
            continue
        shoot(d1, name, cam, tgt, fov, exp=EXP_OVERRIDE.get(name, 1.2))
    for (name, cam, tgt, fov) in PREV:
        if sel and not any(s in name for s in sel):
            continue
        shoot(d2, name, cam, tgt, fov)
