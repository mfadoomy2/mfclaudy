# -*- coding: utf-8 -*-
"""03B.9 §27 · 30 MICROSCENES x 4 distancias (10m/2m/50cm/15cm) -> _micro/<punto>_<d>.png"""
import math
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
PORT = 8128
OUT = os.path.join(HERE, '_micro')
os.makedirs(OUT, exist_ok=True)
IT = sys.argv[1] if len(sys.argv) > 1 else 'i1'
SOLO = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else None   # subconjunto de puntos

# (nombre, tx, ty, tz, azimut_grados)
PTS = [
    ('01_canopy_centro', 0.0, 8.0, 6.6, -55), ('02_canopy_borde', 2.6, 10.2, 6.4, -70),
    ('03_tensor', -0.9, 6.0, 4.6, 40), ('04_nudo_mastil', -0.3, 4.5, 3.0, 25),
    ('05_base_mastil', -0.3, 4.5, 0.78, 60), ('06_escalera_inicio', -38.5, 18.4, 0.6, 130),
    ('07_escalera_meseta', -36.9, 18.2, 3.2, 100), ('08_escalera_desembarco', -36.3, 20.3, 6.1, -40),
    ('09_ascensor_inf', -70.2, 6.2, 1.2, -125), ('10_ascensor_sup', -70.2, 6.2, 6.2, -125),
    ('11_pasarela_recta', 2.0, -16.0, 6.05, 100), ('12_pasarela_curva', -34.0, 10.0, 6.05, 30),
    ('13_barandilla_final', -35.0, 21.6, 6.6, -60), ('14_junta_pasarela', 6.0, -15.8, 6.02, 95),
    ('15_sumidero', 10.5, -15.5, 6.0, 95), ('16_jardinera_hero', -8.0, 26.0, 0.5, -110),
    ('17_planta_hero', 0.35, 4.95, 0.62, -120), ('18_trepadora', 0.85, 4.1, 1.7, -35),
    ('19_colgante', 5.0, 30.0, 7.6, -90), ('20_huerto', -56.5, 6.2, 0.5, 45),
    ('21_balsa', 12.0, 19.0, 0.34, -125), ('22_borde_agua', 12.9, 18.2, 0.45, -125),
    ('23_deposito', -35.0, -18.0, 9.5, 70), ('24_valvula_tanque', -35.0, -18.0, 1.15, 70),
    ('25_pod', -61.0, 9.0, 1.4, 40), ('26_pod_suspension', -61.0, 9.0, 2.6, 40),
    ('27_metro', 56.5, -0.8, 1.2, 75), ('28_estanco', 75.9, -3.6, 1.8, -140),
    ('29_carlos_iii', -28.0, -14.0, 3.6, 55), ('30_fachada_proyecto', -55.5, 19.0, 4.0, 40),
]
DIST = [('10m', 10.0, 2.4, 55), ('2m', 2.0, 0.35, 55), ('50cm', 0.5, 0.06, 50), ('15cm', 0.15, 0.02, 46)]


def shoot(name, cx, cy, cz, tx, ty, tz, fov, w=1400, h=900):
    url = ('http://127.0.0.1:%d/viewer_control.html?cx=%.2f&cy=%.2f&cz=%.2f&tx=%.2f&ty=%.2f&tz=%.2f'
           '&fov=%d&w=%d&h=%d&mat=1' % (PORT, cx, cy, cz, tx, ty, tz, fov, w, h))
    png = os.path.join(OUT, '%s_%s.png' % (name, IT))
    # Edge headless se comporta como singleton por perfil: perfil FRESCO por toma
    # (si no, la toma reutiliza/roba el frame de otra instancia o no escribe el PNG)
    import tempfile, shutil
    udd = tempfile.mkdtemp(prefix='ms9_')
    try:
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--user-data-dir=' + udd,
                        '--screenshot=' + png, '--window-size=%d,%d' % (w, h),
                        '--virtual-time-budget=45000',
                        '--default-background-color=FFFFFFFF', url], capture_output=True, timeout=300)
    finally:
        shutil.rmtree(udd, ignore_errors=True)
    return os.path.exists(png) and os.path.getsize(png) > 25000


srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)],
                       cwd=os.path.join(HERE, '_viewer'),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
fallos = []
try:
    for (nm, tx, ty, tz, az) in PTS:
        if SOLO and nm not in SOLO:
            continue
        for (lab, d, dz, fov) in DIST:
            a = math.radians(az)
            ok = shoot('%s_%s' % (nm, lab), tx + d * math.cos(a), ty + d * math.sin(a), tz + dz,
                       tx, ty, tz, fov)
            if not ok:
                fallos.append('%s_%s' % (nm, lab))
finally:
    srv.terminate()
print('microscenes:', len(PTS) * len(DIST), 'tomas · fallos:', len(fallos), fallos[:8])
