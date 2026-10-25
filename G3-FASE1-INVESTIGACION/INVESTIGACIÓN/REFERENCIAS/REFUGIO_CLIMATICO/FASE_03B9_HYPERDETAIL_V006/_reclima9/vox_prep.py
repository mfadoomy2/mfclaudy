# -*- coding: utf-8 -*-
"""03B.9: voxelizacion A (contexto) / B (contexto+proyecto v006) + campo k_veg por especie.
Mismo metodo que 03B.6/7: clima_core.build_voxels sobre la escena interceptada."""
import os

import numpy as np

import clima_core as C

os.makedirs(C.DATA, exist_ok=True)
mesh, M = C.load_scene()
g = C.grid05()
for estado in ('A', 'B'):
    vox, kv = C.build_voxels(mesh, g, estado)
    np.save(os.path.join(C.DATA, 'vox%s.npy' % estado), vox)
    np.save(os.path.join(C.DATA, 'kv%s.npy' % estado), kv)
    print(estado, vox.shape, 'ocupadas:', int((vox > 0).sum()),
          'veg:', int((vox == 4).sum()), 'k_veg medio:', round(float(kv[vox == 4].mean()), 3) if (vox == 4).any() else 0)
print('ok')
