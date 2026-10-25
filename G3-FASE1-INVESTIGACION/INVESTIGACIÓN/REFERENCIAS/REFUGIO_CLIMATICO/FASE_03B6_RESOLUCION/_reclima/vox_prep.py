# -*- coding: utf-8 -*-
"""03B.6: voxelizacion A (contexto) / B (contexto+proyecto v003) — bootstrap que 03B.5B no conservo.
Mismo metodo: clima_core.build_voxels sobre la escena interceptada."""
import os

import numpy as np

import clima_core as C

mesh, M = C.load_scene()
g = C.grid05()
for estado in ('A', 'B'):
    vox = C.build_voxels(mesh, g, estado)
    np.save(os.path.join(C.DATA, 'vox%s.npy' % estado), vox)
    print(estado, vox.shape, 'ocupadas:', int((vox > 0).sum()))
print('ok')
