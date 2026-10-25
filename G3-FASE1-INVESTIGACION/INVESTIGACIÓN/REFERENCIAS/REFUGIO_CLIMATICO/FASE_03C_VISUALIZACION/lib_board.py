# -*- coding: utf-8 -*-
"""Tablero de la biblioteca vegetal E02: 9 roles renderizados + tabla categoria/rol/ubicacion/comportamiento."""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
B03 = os.path.normpath(os.path.join(HERE, '..', 'FASE_03B_MODELO_MAESTRO'))
sys.path.insert(0, B03)
sys.path.insert(0, os.path.normpath(os.path.join(B03, '..', 'FASE_03A_MODELO_PROXY')))
from build_all_03b import BLOCKS, LCOL, LOP  # noqa: E402

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
OUT = os.path.join(HERE, 'biblioteca_vegetal')
os.makedirs(OUT, exist_ok=True)

LIB = [
    ('VEG2_ARBOL_A', 'ÁRBOL DE SOMBRA A', 'sombra + escala', 'orlas y eje sur', 'da sombra, acompaña recorrido', 5.5, 2.6),
    ('VEG2_ARBOL_B', 'ÁRBOL DE SOMBRA B', 'sombra + escala', 'bordes y claros', 'da sombra', 6.5, 3.0),
    ('VEG2_ARBOL_EX', 'ARBOLADO EXISTENTE', 'preexistencia', 'perímetro real OSM', 'da sombra, marca borde urbano', 7.5, 3.4),
    ('VEG2_TREPADORA', 'TREPADORA DE MÁSTIL', 'verde vertical', '1 de cada 2 mástiles', 'trepa y derrama en el brazo', 3.6, 1.6),
    ('VEG2_BAJA', 'VEGETACIÓN BAJA DE ESTANCIA', 'confort/borde blando', 'junto a bancos y jardineras', 'acompaña la estancia', 1.4, 0.8),
    ('VEG2_TROPICAL', 'TROPICAL HÚMEDA (alocasia)', 'atmósfera húmeda', 'núcleo C2, cúpula, jardineras', 'da sombra baja, acompaña agua', 2.2, 1.2),
    ('VEG2_HUERTO', 'FILA DE HUERTO', 'productivo/social', 'interior C1 bajo balsas', 'acompaña recorrido, se cultiva', 2.2, 0.9),
    ('VEG2_ACUATICA', 'ACUÁTICA + NENÚFAR', 'agua viva', 'estanques de microalgas', 'flota y emerge', 1.6, 0.6),
    ('VEG2_COLGANTE', 'COLGANTE DE ESTRUCTURA', 'lluvia verde', 'aros de loops y borde de cinta', 'cuelga de la estructura', 3.0, 0.0),
]

# render aislado por bloque (escena mono-bloque; el visor 03B en modo material no usa texturas -> file:// ok)
V3B = os.path.join(B03, '_viewer')
for (blk, *_rest, dist, zc) in [(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in LIB]:
    pass
for row in LIB:
    blk, dist, zc = row[0], row[5], row[6]
    meshes = []
    for (layer, (V, F)) in BLOCKS[blk]:
        if F:
            meshes.append(dict(layer=layer, color=list(LCOL[layer][:3]), opacity=LOP[layer],
                               V=[[round(a, 3) for a in v] for v in V], F=F))
    with open(os.path.join(V3B, 'scene_pack.js'), 'w', encoding='utf-8') as fp:
        fp.write('const SCENE_MESHES = ')
        json.dump(meshes, fp, separators=(',', ':'))
        fp.write(';\nconst SCENE_LINES = [];\n')
    vh = open(os.path.join(V3B, 'viewer_full.html'), encoding='utf-8').read().replace('scene_full.js', 'scene_pack.js')
    vp = os.path.join(V3B, 'viewer_pack.html')
    open(vp, 'w', encoding='utf-8').write(vh)
    zoff = zc if zc > 0 else 1.0
    url = 'file:///%s?cx=%s&cy=%s&cz=%s&tx=0&ty=0&tz=%s&fov=38&w=800&h=800&mat=1' % (
        vp.replace('\\', '/'), dist * 0.8, -dist, zoff + (0.4 if blk != 'VEG2_COLGANTE' else -1.2), zoff if blk != 'VEG2_COLGANTE' else -1.0)
    png = os.path.join(OUT, blk + '.png')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--screenshot=' + png,
                    '--window-size=800,800', '--virtual-time-budget=7000',
                    '--default-background-color=FFFFFFFF', url], capture_output=True, timeout=90)
    print(blk, 'ok' if os.path.exists(png) else 'FALLO')

# tablero PIL
try:
    F1 = ImageFont.truetype('bahnschrift.ttf', 26)
    F2 = ImageFont.truetype('arial.ttf', 17)
    F3 = ImageFont.truetype('consola.ttf', 15)
except Exception:
    F1 = F2 = F3 = ImageFont.load_default()

cw, chh = 420, 560
cols = 3
rows = 3
W = cols * cw + 60
Hh = rows * chh + 120
board = Image.new('RGB', (W, Hh), (255, 255, 255))
d = ImageDraw.Draw(board)
d.text((30, 22), 'BIBLIOTECA VEGETAL E02 — REFUGIO CLIMÁTICO PUERTA DEL SOL', font=F1, fill=(51, 50, 46))
d.text((30, 56), 'roles espaciales · bloques Rhino instanciables · capa 15_VEGETATION_FULL apagable · geometría 03B congelada', font=F3, fill=(150, 87, 127))
for i, (blk, nombre, rol, ubic, comp, _d, _z) in enumerate(LIB):
    x = 30 + (i % cols) * cw
    y = 90 + (i // cols) * chh
    p = os.path.join(OUT, blk + '.png')
    if os.path.exists(p):
        im = Image.open(p).resize((cw - 40, cw - 40))
        board.paste(im, (x, y))
    d.rectangle([x, y, x + cw - 40, y + cw - 40], outline=(200, 196, 188))
    d.text((x, y + cw - 30), nombre, font=F2, fill=(51, 50, 46))
    d.text((x, y + cw - 6), 'rol: ' + rol, font=F3, fill=(90, 87, 80))
    d.text((x, y + cw + 16), 'dónde: ' + ubic, font=F3, fill=(90, 87, 80))
    d.text((x, y + cw + 38), 'comportamiento: ' + comp, font=F3, fill=(46, 110, 107))
    d.text((x, y + cw + 62), blk, font=F3, fill=(214, 87, 127))
board.save(os.path.join(HERE, 'BIBLIOTECA_VEGETAL_E02.jpg'), quality=90)
print('tablero listo')
