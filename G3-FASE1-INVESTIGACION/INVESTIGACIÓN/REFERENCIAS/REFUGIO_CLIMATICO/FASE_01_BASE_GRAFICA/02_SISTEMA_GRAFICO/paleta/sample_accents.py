# -*- coding: utf-8 -*-
"""Muestreo dirigido de acentos: mediana RGB de regiones concretas de las referencias."""
import os

import numpy as np
from PIL import Image

BASE = r'C:\Users\iraxx_c0wouln\OneDrive\Documentos\iraxxxdios_ARQUITECTURA\xxxmiguelxxx\Monteserin\MONTESERIN IA\MONTESERIN IA\MUTACIONES (DIBUJO + IA)\DIBUJO3 (REFUGIO CLIMATICO)'

REGIONS = [
    ('HR01.png', (364, 707, 525, 848), 'rosa capsulas (tren O)'),
    ('HR01.png', (606, 404, 687, 525), 'turquesa pista/loop'),
    ('HR01.png', (869, 545, 1050, 667), 'verde lima balsa'),
    ('HR01.png', (1420, 440, 1520, 500), 'blanco membrana'),
    ('HR02.png', (608, 607, 770, 688), 'verde agua acrilico maqueta'),
    ('HR11.png', (707, 606, 909, 727), 'rosa hinchable (loop)'),
    (os.path.join('IN PROGRESS REFUGIO', '0F53E6F0-C499-4057-8C95-A0928F3680D9.png'),
     (1080, 500, 1140, 550), 'verde microalgas oscuro (balsa real)'),
    (os.path.join('IN PROGRESS REFUGIO', '0F53E6F0-C499-4057-8C95-A0928F3680D9.png'),
     (940, 380, 1000, 420), 'verde disco claro (dosel real)'),
    (os.path.join('IN PROGRESS REFUGIO', '0F53E6F0-C499-4057-8C95-A0928F3680D9.png'),
     (200, 330, 260, 380), 'granito plaza (pavimento)'),
]

for rel, box, tag in REGIONS:
    im = Image.open(os.path.join(BASE, rel)).convert('RGB')
    a = np.asarray(im.crop(box)).reshape(-1, 3)
    med = np.median(a, 0).astype(int)
    # ademas percentil saturado (para acentos puros): pixel con max saturacion aprox
    mx, mn = a.max(1).astype(int), a.min(1).astype(int)
    sat = mx - mn
    top = a[np.argsort(-sat)[:max(1, len(a) // 50)]]
    acc = np.median(top, 0).astype(int)
    print('%-42s mediana #%02X%02X%02X  acento #%02X%02X%02X' % (tag, *med, *acc))
