# -*- coding: utf-8 -*-
"""E03-7: HOJA_CONTACTO_E03.jpg (14 vistas) + COMPARATIVA_E02_E03.jpg (6 pares, luz principal)."""
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'hero_E03')
E02 = os.path.join(HERE, 'direccion_arte')
CREAM, INK, PINK = (247, 244, 238), (26, 26, 26), (214, 87, 127)
IDS = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7']
PAR = {'H1': 'DA_V05_banda_correos', 'H2': 'DA_V06_bajo_C1', 'H3': 'DA_V13_splash',
       'H4': 'DA_V07_reloj', 'H5': 'DA_V19_sobre_cinta', 'H6': 'DA_V10_cupula'}
SUB = {'H1': 'banda Correos — alfombra de sombra', 'H2': 'huerto C1 — capa productiva',
       'H3': 'splash — agua viva total', 'H4': 'reloj — contraluz de tarde',
       'H5': 'CINTA v003 — tablero, escalera y ascensor C2-N', 'H6': 'cupula-pergola',
       'H7': 'aerea — columnas de vapor (equiv. 0F53E6F0)'}


def th(p, w):
    im = Image.open(p).convert('RGB')
    h = int(im.height * w / im.width)
    return im.resize((w, h), Image.LANCZOS)


def label(dr, xy, txt, fill=INK):
    dr.text(xy, txt, fill=fill)


# ---- hoja de contacto: 14 = 7 filas x 2 columnas (mediodia | tarde)
TW = 900
cell_h = int(TW * 1600 / 2560) + 34
sheet = Image.new('RGB', (TW * 2 + 60, cell_h * 7 + 90), CREAM)
dr = ImageDraw.Draw(sheet)
label(dr, (20, 16), 'E03 · TANDA HERO — 7 camaras x 2 luces · escena v003 congelada + capa atmosferica', PINK)
label(dr, (20, 34), 'REFUGIO CLIMATICO PUERTA DEL SOL · 2026-08-11')
y = 64
for hid in IDS:
    for k, luz in enumerate(('mediodia', 'tarde')):
        p = os.path.join(OUT, '%s_%s.png' % (hid, luz))
        if os.path.exists(p):
            t = th(p, TW)
            sheet.paste(t, (20 + k * (TW + 20), y))
    label(dr, (20, y + int(TW * 1600 / 2560) + 4), '%s %s  |  izq: mediodia · der: tarde' % (hid, SUB[hid]))
    y += cell_h
sheet.save(os.path.join(HERE, 'HOJA_CONTACTO_E03.jpg'), quality=88)
print('HOJA_CONTACTO_E03.jpg', sheet.size)

# ---- comparativa E02 -> E03 (luz principal = mediodia), 6 pares
TW2 = 840
c_h = int(TW2 * 1200 / 1920) + 40
comp = Image.new('RGB', (TW2 * 2 + 60, c_h * 6 + 80), CREAM)
dr = ImageDraw.Draw(comp)
label(dr, (20, 14), 'COMPARATIVA E02 (materialidad+vegetacion) -> E03 (atmosfera+agua viva+poblacion) · mismas camaras base', PINK)
y = 46
for hid in IDS[:6]:
    pe = os.path.join(E02, PAR[hid] + '.png')
    pn = os.path.join(OUT, '%s_mediodia.png' % hid)
    if os.path.exists(pe):
        comp.paste(th(pe, TW2), (20, y))
    if os.path.exists(pn):
        t = th(pn, TW2)
        comp.paste(t, (40 + TW2, y))
    label(dr, (20, y + int(TW2 * 1200 / 1920) + 4),
          '%s  E02 (izq, v002) -> E03 (der, v003: cinta real, ascensores, estatua, gente, agua, niebla)' % hid)
    y += c_h
comp.save(os.path.join(HERE, 'COMPARATIVA_E02_E03.jpg'), quality=88)
print('COMPARATIVA_E02_E03.jpg', comp.size)
