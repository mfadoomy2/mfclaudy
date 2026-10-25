# -*- coding: utf-8 -*-
"""Vistas 03B: 20 humanas clay + clay overview + test material (8)."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VIEWER = os.path.join(HERE, '_viewer', 'viewer_full.html').replace('\\', '/')
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
EYE = 1.65

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
    ('V10_cupula_interior', (24, 2, EYE), (36, 2, 4.5), 68),
    ('V11_C3_balsas', (50, -2, EYE), (56, 14, 5.5), 66),
    ('V12_tren_SE', (74, -14, EYE), (66, 2, 2.0), 64),
    ('V13_splash', (24, -10, EYE), (14, -1, 1.2), 66),
    ('V14_escalera_cinta', (6, 34, EYE), (-4, 24, 5.0), 64),
    ('V15_vivero_C3NE', (58, 22, EYE), (64, 15, 2.0), 66),
    ('V16_mariblanca', (-90, -8, EYE), (-60, 4, 3.0), 64),
    ('V17_hacia_oso', (54, 18, EYE), (82, 24, 3.0), 60),
    ('V18_eje_mayor_alcala', (-72, -11, EYE), (30, -8, 3.0), 58),
    ('V19_sobre_cinta', (-20, 27, 7.35), (10, 12, 6.0), 66),
    ('V20_reloj_desde_este', (48, -6, EYE), (-25.2, -34.5, 16.0), 52),
]
MAT_SEL = ['V05_banda_correos', 'V06_bajo_C1', 'V07_salon_C2_reloj', 'V10_cupula_interior',
           'V11_C3_balsas', 'V13_splash', 'V15_vivero_C3NE', 'V19_sobre_cinta']


def shoot(outdir, name, cam, tgt, fov, ortho=None, mat=False, w=1600, h=1000):
    url = 'file:///%s?cx=%s&cy=%s&cz=%s&tx=%s&ty=%s&tz=%s&fov=%s&w=%d&h=%d%s' % (
        VIEWER, cam[0], cam[1], cam[2], tgt[0], tgt[1], tgt[2], fov, w, h, '&mat=1' if mat else '')
    if ortho:
        url += '&ortho=%s' % ortho
    png = os.path.join(outdir, name + '.png')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--screenshot=' + png,
                    '--window-size=%d,%d' % (w, h), '--virtual-time-budget=12000',
                    '--default-background-color=FFFFFFFF', url], capture_output=True, timeout=150)
    ok = os.path.exists(png) and os.path.getsize(png) > 20000
    print(('OK  ' if ok else 'FALLO ') + name + (' [MAT]' if mat else ''))
    return ok


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    d1 = os.path.join(HERE, 'vistas_humanas'); os.makedirs(d1, exist_ok=True)
    d2 = os.path.join(HERE, 'clay'); os.makedirs(d2, exist_ok=True)
    d3 = os.path.join(HERE, 'material_test'); os.makedirs(d3, exist_ok=True)
    if which in ('all', 'clay'):
        for (name, cam, tgt, fov) in VIEWS:
            shoot(d1, name, cam, tgt, fov)
        shoot(d2, 'CLAY_OVERVIEW_aerea', (0, -85, 46), (2, 12, 0), 55)
        shoot(d2, 'CLAY_OVERVIEW_axon', (140, -140, 120), (0, 8, 0), 0, ortho=80, w=1600, h=1100)
    if which in ('all', 'mat'):
        for (name, cam, tgt, fov) in VIEWS:
            if name in MAT_SEL:
                shoot(d3, 'MAT_' + name, cam, tgt, fov, mat=True)
        shoot(d3, 'MAT_aerea', (0, -85, 46), (2, 12, 0), 55, mat=True)
