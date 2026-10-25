# -*- coding: utf-8 -*-
"""03B.8 §7-§9 · Conversion de assets vegetales externos (CC0/CC-BY, ver _assets_veg/provenance.json)
a bloques de malla con 3 LOD (HERO/MID/FAR). Salida: _veg_blocks.json
  { "<ROL>": { "hero": [[layer, V, F], ...], "mid": [...], "far": [...], "alto": h, "fuente": ... } }
Z-up, base en z=0, centrado en XY, escalado a altura real de especie."""
import json
import math
import os

import numpy as np
import trimesh
import fast_simplification

HERE = os.path.dirname(os.path.abspath(__file__))
AV = os.path.join(HERE, '_assets_veg')

# rol -> (ruta, altura_objetivo_m, es_colgante)
ASSETS = {
    'HELECHO':   ('fern_02/fern_02_1k.gltf',                         0.55, False),
    'ALOCASIA':  ('anthurium_botany_01/anthurium_botany_01_1k.gltf', 0.60, False),
    'CALATHEA':  ('calathea_orbifolia_01/calathea_orbifolia_01_1k.gltf', 0.50, False),
    'GRAMINEA':  ('grass_medium_02/grass_medium_02_1k.gltf',         0.55, False),
    'ARBUSTO':   ('shrub_04/shrub_04_1k.gltf',                       0.85, False),
    'MACETA':    ('potted_plant_01/potted_plant_01_1k.gltf',         0.80, False),
    'MONSTERA':  ('monstera_plant_isalousberg.glb',                  0.95, False),
    'POTHOS':    ('pothos_hanging_isalousberg.glb',                  0.85, True),
    'JUNCO':     ('cattail_polybygoogle.glb',                        1.35, False),
}
LODS = {'hero': 5000, 'mid': 1200, 'far': 260}


def layer_de(nombre):
    n = (nombre or '').lower()
    if any(k in n for k in ('pot', 'vase', 'ceramic', 'bucket')):
        return '09_PLANTERS'
    if any(k in n for k in ('soil', 'dirt', 'ground', 'earth', 'mulch')):
        return '19_DETALLE'
    return '15_VEGETATION_FULL'


def cargar(path):
    sc = trimesh.load(os.path.join(AV, path), force='scene', process=False)
    if isinstance(sc, trimesh.Trimesh):
        return [('mesh', sc)]
    partes = []
    for node in sc.graph.nodes_geometry:
        tf, gname = sc.graph[node]
        geom = sc.geometry.get(gname)
        if geom is None or not hasattr(geom, 'faces') or not len(geom.faces):
            continue
        g = geom.copy()
        g.apply_transform(tf)
        try:
            g.update_faces(g.nondegenerate_faces(height=1e-7))   # 03B.8 §3: sin slivers del asset
        except Exception:
            pass
        partes.append((gname, g))
    return partes


OUT = {}
for rol, (ruta, htarget, colgante) in ASSETS.items():
    try:
        partes = cargar(ruta)
    except Exception as e:
        print('FALLO carga', rol, ruta, repr(e))
        continue
    # une para medir bbox global en Y-up y calcula transformacion comun
    allv = np.vstack([g.vertices for _n, g in partes])
    # glTF es Y-up -> Z-up: (x, y, z) -> (x, -z, y)
    allz = np.column_stack([allv[:, 0], -allv[:, 2], allv[:, 1]])
    zmin, zmax = allz[:, 2].min(), allz[:, 2].max()
    alto0 = max(zmax - zmin, 1e-6)
    s = htarget / alto0
    cx = (allz[:, 0].min() + allz[:, 0].max()) / 2 * s
    cy = (allz[:, 1].min() + allz[:, 1].max()) / 2 * s

    lods = {}
    for lodn, tmax in LODS.items():
        piezas = []
        ntot = sum(len(g.faces) for _n, g in partes)
        for name, g in partes:
            V = np.column_stack([g.vertices[:, 0], -g.vertices[:, 2], g.vertices[:, 1]]) * s
            V[:, 0] -= cx
            V[:, 1] -= cy
            V[:, 2] -= zmin * s
            F = np.asarray(g.faces, dtype=np.int64)
            cuota = max(60, int(tmax * (len(F) / max(ntot, 1))))
            if len(F) > cuota:
                try:
                    V2, F2 = fast_simplification.simplify(V.astype(np.float32), F.astype(np.int64),
                                                          target_count=cuota)
                except Exception:
                    V2, F2 = V, F[::max(1, len(F) // cuota)]
                V, F = V2, F2
            if colgante:
                V = V.copy()
                V[:, 2] -= htarget      # colgante: origen en el punto de cuelgue (la planta cae hacia abajo)
            piezas.append([layer_de(name),
                           [[round(float(a), 3) for a in v] for v in V],
                           [[int(a) for a in f] for f in F]])
        lods[lodn] = piezas
    tris = {k: sum(len(p[2]) for p in v) for k, v in lods.items()}
    OUT[rol] = dict(hero=lods['hero'], mid=lods['mid'], far=lods['far'],
                    alto=htarget, colgante=colgante, fuente=ruta, tris=tris)
    print('%-10s %s  tris hero/mid/far = %s' % (rol, ruta.split('/')[0], tris))

json.dump(OUT, open(os.path.join(HERE, '_veg_blocks.json'), 'w'), separators=(',', ':'))
sz = os.path.getsize(os.path.join(HERE, '_veg_blocks.json')) // 1024
print('OK _veg_blocks.json (%d roles, %d KB)' % (len(OUT), sz))
