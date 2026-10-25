# -*- coding: utf-8 -*-
"""E03-5: tanda hero — 7 camaras (atmos_config) x 2 luces a 2560x1600."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, 'atmos_config.json'), encoding='utf-8'))
VIEWER = 'http://127.0.0.1:8123/viewer_e03.html'
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
W, H = CFG.get('resolucion_hero', [2560, 1600])
OUT = os.path.join(HERE, 'hero_E03')


def shoot(name, cam, tgt, fov, luz, exp=None, w=W, h=H):
    url = '%s?cx=%s&cy=%s&cz=%s&tx=%s&ty=%s&tz=%s&fov=%s&w=%d&h=%d&luz=%s' % (
        VIEWER, cam[0], cam[1], cam[2], tgt[0], tgt[1], tgt[2], fov, w, h, luz)
    if exp is not None:
        url += '&exp=%s' % exp
    png = os.path.join(OUT, name + '.png')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu',
                    '--screenshot=' + png, '--window-size=%d,%d' % (w, h),
                    '--virtual-time-budget=22000', '--default-background-color=FFFFFFFF', url],
                   capture_output=True, timeout=300)
    ok = os.path.exists(png) and os.path.getsize(png) > 30000
    print(('OK  ' if ok else 'FALLO ') + name + ((' %d KB' % (os.path.getsize(png) // 1024)) if ok else ''))
    return ok


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    sel = sys.argv[1:] or None
    nok = 0
    for c in CFG['camaras_hero']:
        for luz in ('mediodia', 'tarde'):
            name = '%s_%s' % (c['id'], luz)
            if sel and not any(s in name for s in sel):
                continue
            exp = c.get('exp_override')
            if c['id'] == 'H1' and luz == 'mediodia':
                exp = 1.1
            nok += 0 if shoot(name, c['cam'], c['tgt'], c['fov'], luz, exp) else 1
    print('fallos:', nok)
