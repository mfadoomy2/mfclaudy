# -*- coding: utf-8 -*-
"""MULTIVIEW INPUT PACKS para Tripo: FRONT/LEFT/BACK/RIGHT del MISMO objeto, fondo neutro."""
import json
import os
import subprocess

from build_all_03b import BLOCKS, LCOL, LOP

HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
PACKS = {
    'TRIPO_PINK_POD_01': ('POD_M', 5.5, 2.2),
    'TRIPO_PINK_POD_TRAIN_01': ('POD_TRAIN', 7.5, 1.6),
    'TRIPO_DROP_TANK_01': ('DROP_TANK', 3.6, 1.2),
    'TRIPO_SPECIAL_PLANTER_01': ('MAST_2', 8.0, 2.8),
    'TRIPO_MIST_HEAD_01': ('NEB_POST', 5.6, 2.2),
}

os.makedirs(os.path.join(HERE, 'tripo'), exist_ok=True)
for pack, (blk, dist, zc) in PACKS.items():
    d = os.path.join(HERE, 'tripo', pack)
    os.makedirs(d, exist_ok=True)
    meshes = []
    for (layer, (V, F)) in BLOCKS[blk]:
        if F:
            meshes.append(dict(layer=layer, color=list(LCOL[layer][:3]), opacity=LOP[layer],
                               V=[[round(a, 3) for a in v] for v in V], F=F))
    js = os.path.join(HERE, '_viewer', 'scene_pack.js')
    with open(js, 'w', encoding='utf-8') as fp:
        fp.write('const SCENE_MESHES = ')
        json.dump(meshes, fp, separators=(',', ':'))
        fp.write(';\nconst SCENE_LINES = [];\n')
    vh = open(os.path.join(HERE, '_viewer', 'viewer_full.html'), encoding='utf-8').read().replace('scene_full.js', 'scene_pack.js')
    vp = os.path.join(HERE, '_viewer', 'viewer_pack.html')
    open(vp, 'w', encoding='utf-8').write(vh)
    for (view, cx, cy) in [('FRONT', 0, -dist), ('LEFT', -dist, 0), ('BACK', 0, dist), ('RIGHT', dist, 0)]:
        url = 'file:///%s?cx=%s&cy=%s&cz=%s&tx=0&ty=0&tz=%s&fov=34&w=1024&h=1024&mat=1' % (
            vp.replace('\\', '/'), cx, cy, zc, zc)
        png = os.path.join(d, view + '.png')
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--screenshot=' + png,
                        '--window-size=1024,1024', '--virtual-time-budget=8000',
                        '--default-background-color=FFFFFFFF', url], capture_output=True, timeout=90)
        ok = os.path.exists(png) and os.path.getsize(png) > 8000
        print(pack, view, 'OK' if ok else 'FALLO')
