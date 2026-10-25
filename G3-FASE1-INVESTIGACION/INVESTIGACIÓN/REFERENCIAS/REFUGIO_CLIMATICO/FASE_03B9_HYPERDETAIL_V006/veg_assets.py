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

# rol -> (ruta, altura_objetivo_m, es_colgante) — rutas con '2:' vienen de _assets_veg2
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
    # 03B.9 — cosecha del agente botanico (provenance2.json)
    'ARBOLURB':  ('2:elm_tree_polybygoogle.glb',                     6.20, False),
    'MONSTERA2': ('2:monstera_large_isalousberg.glb',                1.20, False),
    'ALOCASIA2': ('2:big_leaf_plant_reyshapes.glb',                  1.35, False),
    'NENUFAR':   ('2:water_lilies_polybygoogle.glb',                 0.24, False),
    'JUNCO2':    ('2:japanese_sedge_zsky.glb',                       0.90, False),
    'MAIZ':      ('2:corn_plant_phases_apelab.glb',                  1.55, False),
    'HELECHO2':  ('2:fern_quaternius.glb',                           0.60, False),
    'HIEDRA':    ('2:ivy_polybygoogle.glb',                          1.10, True),
    'ARBUSTO2':  ('2:shrub_01/shrub_01_1k.gltf',                     0.90, False),
    'GRAMALTA':  ('2:tall_grass_quaternius.glb',                     1.30, False),
}
LODS = {'hero': 5000, 'mid': 1200, 'far': 260}
# 03B.9: plantas PLANAS (nenufar) no pueden normalizarse por altura — tope de diametro en planta
DIAM_MAX = {'NENUFAR': 1.35, 'HIEDRA': 1.60}


def layer_de(nombre):
    n = (nombre or '').lower()
    if any(k in n for k in ('pot', 'vase', 'ceramic', 'bucket')):
        return '09_PLANTERS'
    if any(k in n for k in ('soil', 'dirt', 'ground', 'earth', 'mulch')):
        return '19_DETALLE'
    return '15_VEGETATION_FULL'


def cargar(path):
    if path.startswith('2:'):
        full = os.path.join(HERE, '_assets_veg2', path[2:])
    else:
        full = os.path.join(AV, path)
    sc = trimesh.load(full, force='scene', process=False)
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
    dxy0 = max(allz[:, 0].max() - allz[:, 0].min(), allz[:, 1].max() - allz[:, 1].min(), 1e-6)
    if rol in DIAM_MAX and dxy0 * s > DIAM_MAX[rol]:
        s = DIAM_MAX[rol] / dxy0          # la pala manda: escala por DIAMETRO, no por altura
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
        # 03B.9: la decimacion FAR puede comerse la base del tronco (arboles flotando 1 m):
        # re-basar cada LOD a z=0 si quedo en el aire
        if piezas and not colgante:
            zmin_l = min(v[2] for p in piezas for v in p[1])
            if zmin_l > 0.03:
                for p in piezas:
                    for v in p[1]:
                        v[2] = round(v[2] - zmin_l, 3)
        lods[lodn] = piezas
    tris = {k: sum(len(p[2]) for p in v) for k, v in lods.items()}
    OUT[rol] = dict(hero=lods['hero'], mid=lods['mid'], far=lods['far'],
                    alto=htarget, colgante=colgante, fuente=ruta, tris=tris)
    print('%-10s %s  tris hero/mid/far = %s' % (rol, ruta.split('/')[0], tris))

json.dump(OUT, open(os.path.join(HERE, '_veg_blocks.json'), 'w'), separators=(',', ':'))
sz = os.path.getsize(os.path.join(HERE, '_veg_blocks.json')) // 1024
print('OK _veg_blocks.json (%d roles, %d KB)' % (len(OUT), sz))
