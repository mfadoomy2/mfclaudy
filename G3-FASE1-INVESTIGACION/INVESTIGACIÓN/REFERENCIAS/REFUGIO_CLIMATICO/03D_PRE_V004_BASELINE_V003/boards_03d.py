# -*- coding: utf-8 -*-
"""03D: HOJA_CONTACTO_03D.jpg (14) + COMPARATIVA_E03_03D.jpg (7 pares mediodia: previs vs final)."""
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'hero_03D')
E03 = os.path.normpath(os.path.join(HERE, '..', 'FASE_03C_VISUALIZACION', 'hero_E03'))
CREAM, INK, PINK = (247, 244, 238), (26, 26, 26), (214, 87, 127)
IDS = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7']
SUB = {'H1': 'banda Correos', 'H2': 'huerto C1', 'H3': 'splash', 'H4': 'reloj (tarde)',
       'H5': 'CINTA v003', 'H6': 'cupula', 'H7': 'aerea'}


def th(p, w):
    im = Image.open(p).convert('RGB')
    h = int(im.height * w / im.width)
    return im.resize((w, h), Image.LANCZOS)


TW = 900
cell = int(TW * 1600 / 2560) + 34
sheet = Image.new('RGB', (TW * 2 + 60, cell * 7 + 90), CREAM)
dr = ImageDraw.Draw(sheet)
dr.text((20, 16), 'FASE 03D · VISUALIZACION FINAL (Cycles/OptiX, fisica real) — 7 camaras x 2 luces · v003 congelada', fill=PINK)
dr.text((20, 34), 'REFUGIO CLIMATICO PUERTA DEL SOL · 2026-08-11 · sol PSA real · AgX', fill=INK)
y = 64
for hid in IDS:
    for k, luz in enumerate(('mediodia', 'tarde')):
        p = os.path.join(OUT, '%s_%s.png' % (hid, luz))
        if os.path.exists(p):
            sheet.paste(th(p, TW), (20 + k * (TW + 20), y))
    dr.text((20, y + int(TW * 1600 / 2560) + 4), '%s %s | izq mediodia 14:00 (69.5) · der tarde 17:30 (45.3)' % (hid, SUB[hid]), fill=INK)
    y += cell
sheet.save(os.path.join(HERE, 'HOJA_CONTACTO_03D.jpg'), quality=90)
print('HOJA_CONTACTO_03D.jpg', sheet.size)

TW2 = 840
c2 = int(TW2 * 1600 / 2560) + 40
comp = Image.new('RGB', (TW2 * 2 + 60, c2 * 7 + 80), CREAM)
dr = ImageDraw.Draw(comp)
dr.text((20, 14), 'E03 PREVIS (izq) -> 03D FINAL Cycles (der) · mismas camaras, misma escena v003', fill=PINK)
y = 46
for hid in IDS:
    pe = os.path.join(E03, '%s_mediodia.png' % hid)
    pn = os.path.join(OUT, '%s_mediodia.png' % hid)
    if os.path.exists(pe):
        comp.paste(th(pe, TW2), (20, y))
    if os.path.exists(pn):
        comp.paste(th(pn, TW2), (40 + TW2, y))
    dr.text((20, y + int(TW2 * 1600 / 2560) + 4), hid + ' ' + SUB[hid], fill=INK)
    y += c2
comp.save(os.path.join(HERE, 'COMPARATIVA_E03_03D.jpg'), quality=90)
print('COMPARATIVA_E03_03D.jpg', comp.size)
