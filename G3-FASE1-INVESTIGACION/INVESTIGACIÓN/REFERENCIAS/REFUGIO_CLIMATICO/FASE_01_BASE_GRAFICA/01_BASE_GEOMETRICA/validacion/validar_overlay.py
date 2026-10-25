# -*- coding: utf-8 -*-
"""Validacion de la planta maestra contra la cenital 0F53E6F0 (Sol real, foto sur-arriba).

CPs (pixel <-> metros): esquinas de fachada de la Real Casa de Correos + pico de la media luna.
La foto es oblicua: el ajuste afin absorbe cizalla, la no-linealidad residual se asume ±3-4 m
en campo lejano (documentado).

Variante A: planta tal cual (norte-arriba -> proyectada a la foto sur-arriba).
Variante B: planta ESPEJADA E-O: reproduce el orden de clusteres de la propia foto
            (la IA conservo el orden izquierda-derecha del dibujo sobre una foto sur-arriba).
"""
import json
import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, '..', 'planta_maestra', 'geometria_maestra.json')
PHOTO = r'C:\Users\iraxx_c0wouln\OneDrive\Documentos\iraxxxdios_ARQUITECTURA\xxxmiguelxxx\Monteserin\MONTESERIN IA\MONTESERIN IA\MUTACIONES (DIBUJO + IA)\DIBUJO3 (REFUGIO CLIMATICO)\IN PROGRESS REFUGIO\0F53E6F0-C499-4057-8C95-A0928F3680D9.png'

model = json.load(open(GEO, encoding='utf-8'))

# afin plan(m) -> foto(px), resuelto con CP1 (15,-33)->(818,238), CP2 (-60,-33)->(1335,238), CP3 (8,63)->(1085,800)
A1, A2, A3 = -6.893, 2.278, 996.6
B1, B2, B3 = 0.0, 5.854, 431.2


def T(p, mirror=False):
    x, y = p
    if mirror:
        x = -x - 6.0   # espejo E-O en torno al eje de la plaza (x=-3)
    return (A1 * x + A2 * y + A3, B1 * x + B2 * y + B3)


def ell(cx, cy, rx, ry, rot_deg, n=60):
    r = math.radians(rot_deg)
    return [(cx + rx * math.cos(2 * math.pi * i / n) * math.cos(r) - ry * math.sin(2 * math.pi * i / n) * math.sin(r),
             cy + rx * math.cos(2 * math.pi * i / n) * math.sin(r) + ry * math.sin(2 * math.pi * i / n) * math.cos(r))
            for i in range(n + 1)]


def render(mirror, out_name, title):
    im = Image.open(PHOTO).convert('RGB')
    # atenuar la foto para leer el overlay
    white = Image.new('RGB', im.size, 'white')
    im = Image.blend(im, white, 0.32)
    d = ImageDraw.Draw(im)

    ep = model['estructura_principal']
    for lp in ep['loops']:
        pts = [T(p, mirror) for p in ell(lp['cx'], lp['cy'], lp['rx'], lp['ry'], lp['rot'])]
        d.line(pts, fill=(0, 130, 125), width=4 if lp['g'] == 'G1' else 2)
    dm = ep['dome']
    d.line([T(p, mirror) for p in ell(dm['cx'], dm['cy'], dm['r'], dm['r'], 0)], fill=(0, 130, 125), width=2)

    d.line([T(p, mirror) for p in model['circulacion']['ribbon']], fill=(10, 90, 86), width=3)

    for c in model['programa']['capsules']:
        r = max(c['w'], c['h']) / 2
        d.line([T(p, mirror) for p in ell(c['cx'], c['cy'], r, r, 0, 16)], fill=(214, 40, 130), width=2)

    for p in model['agua_clima']['pools']:
        d.line([T(q, mirror) for q in ell(p['cx'], p['cy'], p['rx'], p['ry'], p['rot'])], fill=(40, 140, 80), width=2)

    for ds in model['paisaje']['discs'][::2]:
        d.line([T(q, mirror) for q in ell(ds['cx'], ds['cy'], ds['r'], ds['r'], 0, 20)], fill=(120, 170, 60), width=1)

    # marco de contraste: Casa de Correos y banda libre
    cc = model['contexto']['casa_correos']['pts']
    d.line([T(p, False) for p in cc] + [T(cc[0], False)], fill=(60, 60, 60), width=3)
    hit = model['contexto']['hitos']
    for k, col in [('carlos_iii', (0, 0, 0)), ('mariblanca', (0, 0, 0)), ('reloj', (200, 0, 0))]:
        x, y = T(hit[k], False)
        d.ellipse([x - 6, y - 6, x + 6, y + 6], outline=col, width=3)

    d.text((20, 16), title, fill=(0, 0, 0))
    im.save(os.path.join(HERE, out_name))
    print('->', out_name)


render(False, 'validacion_A_orientacion_maestra.png',
       'VALIDACION A - planta maestra (norte-arriba, orden del dibujo matriz) sobre 0F53E6F0 (foto sur-arriba)')
render(True, 'validacion_B_espejo_como_foto.png',
       'VALIDACION B - planta espejada E-O = orden de clusteres tal como lo compuso la IA en esta foto')
