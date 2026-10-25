# -*- coding: utf-8 -*-
"""Renderiza las vistas de control humanas del proxy con Edge headless."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VIEWER = os.path.join(HERE, '_viewer', 'viewer.html').replace('\\', '/')
OUT = os.path.join(HERE, 'vistas_control')
os.makedirs(OUT, exist_ok=True)
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

EYE = 1.65

# nombre, cam(x,y,z), target(x,y,z), fov
VIEWS = [
    ('V01_acceso_arenal', (-94, -2, EYE), (-60, 6, 4.5), 66),
    ('V02_acceso_alcala', (84, 10, EYE), (56, 12, 4.5), 66),
    ('V03_acceso_preciados', (-12, 30, EYE), (2, 6, 3.5), 66),
    ('V04_acceso_carretas', (12, -27, EYE), (8, 10, 4.0), 66),
    ('V05_banda_correos', (-2, -18, EYE), (6, 16, 5.0), 62),
    ('V06_bajo_C1', (-56, 2, EYE), (-44, 18, 5.5), 68),
    ('V07_salon_C2_reloj', (6, 8, EYE), (-25.2, -36.5, 15.0), 58),
    ('V08_bajo_anillo_C2N', (-2, 36, EYE), (12, 8, 4.0), 66),
    ('V09_istmo_oeste', (-30, 12, EYE), (-8, 14, 5.0), 64),
    ('V10_cupula', (42, 18, EYE), (30.5, 2, 4.0), 64),
    ('V11_C3_balsas', (50, -2, EYE), (56, 14, 5.5), 66),
    ('V12_tren_SE', (74, -14, EYE), (66, 2, 2.0), 64),
    ('V13_splash', (24, -10, EYE), (14, -1, 1.2), 66),
    ('V14_escalera_cinta', (6, 34, EYE), (-4, 24, 5.0), 64),
    ('V15_vivero_C3NE', (58, 22, EYE), (48, 8, 3.0), 66),
    ('V16_mariblanca', (-90, -8, EYE), (-60, 4, 3.0), 64),
    ('V17_hacia_oso', (54, 18, EYE), (82, 24, 3.0), 60),
    ('V18_eje_mayor_alcala', (-72, -10, EYE), (30, -4, 3.0), 58),
    ('V19_sobre_cinta', (-20, 27, 5.7 + 1.65), (10, 12, 6.0), 66),
    ('V20_aerea_suave', (0, -80, 42), (2, 12, 0), 55),
]


def shoot(name, cam, tgt, fov, ortho=None, w=1600, h=1000):
    url = 'file:///%s?cx=%s&cy=%s&cz=%s&tx=%s&ty=%s&tz=%s&fov=%s&w=%d&h=%d' % (
        VIEWER, cam[0], cam[1], cam[2], tgt[0], tgt[1], tgt[2], fov, w, h)
    if ortho:
        url += '&ortho=%s' % ortho
    png = os.path.join(OUT, name + '.png')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--force-device-scale-factor=1',
                    '--screenshot=' + png, '--window-size=%d,%d' % (w, h),
                    '--virtual-time-budget=9000', '--default-background-color=FFFFFFFF', url],
                   capture_output=True, timeout=120)
    ok = os.path.exists(png) and os.path.getsize(png) > 20000
    print(('OK  ' if ok else 'FALLO ') + name)
    return ok


if __name__ == '__main__':
    sel = sys.argv[1:] or None
    n_ok = 0
    for (name, cam, tgt, fov) in VIEWS:
        if sel and not any(s in name for s in sel):
            continue
        n_ok += 1 if shoot(name, cam, tgt, fov) else 0
    # axonometria ortografica
    if not sel or 'axon' in ' '.join(sel):
        n_ok += 1 if shoot('V21_axonometria', (140, -140, 120), (0, 8, 0), 0, ortho=80, w=1600, h=1100) else 0
    print('vistas correctas:', n_ok)
