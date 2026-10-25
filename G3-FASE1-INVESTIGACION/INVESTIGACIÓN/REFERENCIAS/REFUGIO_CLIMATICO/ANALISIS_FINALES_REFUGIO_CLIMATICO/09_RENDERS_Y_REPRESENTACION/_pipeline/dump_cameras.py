# -*- coding: utf-8 -*-
"""Vuelca CAMERA_METADATA.json por vista: todo lo necesario para reproducir la camara
exactamente (posicion, target, matriz mundo, FOV vertical, focal equivalente, sensor,
clipping, resolucion). Uso: blender -b SOL_FINAL_V006.blend -P dump_cameras.py"""
import json
import math
import os

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
RP = os.path.join(HERE, 'refpacks')
RES = (1920, 1200)

for o in bpy.data.objects:
    if o.type != 'CAMERA' or not o.name.startswith('CAM_'):
        continue
    cam = o.data
    cid = o.name[4:]
    tgt = None
    for c in o.constraints:
        if c.type == 'TRACK_TO' and c.target:
            tgt = list(c.target.location)
    mw = [list(r) for r in o.matrix_world]
    fov_y = math.degrees(cam.angle_y)
    # focal equivalente 35mm (sensor vertical fit)
    f35 = 24.0 / (2 * math.tan(cam.angle_y / 2))       # sensor alto 24 mm
    meta = dict(
        camera_id=cid,
        escena='SOL_FINAL_V006.blend (v006 build 12)',
        location=[round(v, 4) for v in o.location],
        target=[round(v, 4) for v in tgt] if tgt else None,
        matrix_world=mw,
        fov_vertical_deg=round(fov_y, 3),
        focal_equiv_35mm_sensor24=round(f35, 2),
        sensor_fit=cam.sensor_fit,
        clip_start=cam.clip_start, clip_end=cam.clip_end,
        resolucion=list(RES),
        aspect=RES[0] / RES[1],
        dof=dict(activo=cam.dof.use_dof, fstop=cam.dof.aperture_fstop),
        luz='tarde PSA (SUN_03D.json) en beauty/clay/ao; passes de datos sin luz',
        nota='matrix_world transforma camara->mundo (Blender, Z-up, -Z mirada). '
             'depth.png codifica 0-250 m lineal invertido (cerca=1).')
    outdir = os.path.join(RP, cid)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, 'CAMERA_METADATA.json'), 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print('META OK', cid)
print('done')
