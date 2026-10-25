# -*- coding: utf-8 -*-
"""Driver reanudable de REFERENCE PACKS + post-proceso de edges.
Un pack por invocacion de Blender; salta packs completos; al final, edge pass por
Sobel(depth)+Sobel(normal) para cada vista y hoja de contacto del pack."""
import os
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
B = r'C:\Program Files\Blender Foundation\Blender 5.0\blender.exe'
RP = os.path.join(HERE, 'refpacks')
CAMS = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
        'F1_INTERIOR_DOSEL', 'F2_HUERTO', 'F3_ATRIO_ESTACION', 'F4_CARLOS_III',
        'F5_DETALLE_NUDO']
PASSES = ['beauty', 'clay', 'clay_sinveg', 'depth', 'normal', 'ao', 'id_mat']


def completo(cam):
    d = os.path.join(RP, cam)
    return all(os.path.exists(os.path.join(d, p + '.png')) and
               os.path.getsize(os.path.join(d, p + '.png')) > 50_000 for p in PASSES[:3]) and \
           all(os.path.exists(os.path.join(d, p + '.png')) for p in PASSES[3:])


def sobel(a):
    gx = np.abs(np.diff(a.astype(float), axis=1, prepend=a[:, :1]))
    gy = np.abs(np.diff(a.astype(float), axis=0, prepend=a[:1, :]))
    return np.hypot(gx, gy)


def edges(cam):
    d = os.path.join(RP, cam)
    dep = np.asarray(Image.open(os.path.join(d, 'depth.png')).convert('L'))
    nor = np.asarray(Image.open(os.path.join(d, 'normal.png')).convert('L'))
    e = sobel(dep) * 2.2 + sobel(nor) * 1.0
    e = np.clip(e / max(np.percentile(e, 99.5), 1e-6), 0, 1)
    img = (255 - e * 255).astype(np.uint8)          # lineas negras sobre blanco
    Image.fromarray(img).save(os.path.join(d, 'edges.png'))


def contacto(cam):
    d = os.path.join(RP, cam)
    tiles = PASSES + ['edges']
    ims = []
    for p in tiles:
        f = os.path.join(d, p + '.png')
        if os.path.exists(f):
            im = Image.open(f).convert('RGB')
            im.thumbnail((640, 400))
            ims.append((p, im))
    if not ims:
        return
    w, h = ims[0][1].size
    cols = 4
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * (h + 18)), 'white')
    from PIL import ImageDraw
    dr = ImageDraw.Draw(sheet)
    for k, (p, im) in enumerate(ims):
        x = (k % cols) * w
        y = (k // cols) * (h + 18)
        sheet.paste(im, (x, y + 18))
        dr.text((x + 4, y + 2), p.upper(), fill='black')
    sheet.save(os.path.join(d, '_contacto_pack.png'))


hechos = saltados = fallos = 0
for cam in CAMS:
    if completo(cam):
        saltados += 1
    else:
        r = subprocess.run([B, '-b', '-P', os.path.join(HERE, 'refpack_v006.py'), '--',
                            'pack', cam, '1920', '1200'],
                           capture_output=True, text=True, timeout=2400)
        if completo(cam):
            hechos += 1
            print('OK  %s' % cam, flush=True)
        else:
            fallos += 1
            print('FALLO %s' % cam, flush=True)
            print((r.stdout or '')[-400:], flush=True)
            continue
    try:
        edges(cam)
        contacto(cam)
        print('OK  %s edges+contacto' % cam, flush=True)
    except Exception as ex:
        print('FALLO %s post: %s' % (cam, ex), flush=True)

print('RESUMEN: %d nuevos, %d ya completos, %d fallos' % (hechos, saltados, fallos),
      flush=True)
