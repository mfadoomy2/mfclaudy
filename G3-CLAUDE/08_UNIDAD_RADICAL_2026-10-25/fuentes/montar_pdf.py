"""Monta el PDF A3 apaisado con todo: unidades, escenas, cuerpos, uniones y diagramas."""
import glob
import json
import os

from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
W, H = landscape(A3)
MM = 72 / 25.4
try:
    pdfmetrics.registerFont(TTFont('Ibarra', os.path.join(RAIZ, 'fuentes', 'IbarraRealNova-Italic-400.ttf')))
    F = 'Ibarra'
except Exception:
    F = 'Times-Italic'

c = canvas.Canvas(os.path.join(RAIZ, 'G3_UNIDAD_RADICAL_MODELOS_Y_DIAGRAMAS_A3.pdf'), pagesize=(W, H))
pagina = [0]


def pie(titulo):
    pagina[0] += 1
    c.setFont(F, 7)
    c.setFillColorRGB(0.35, 0.35, 0.35)
    c.drawString(12 * MM, 8 * MM, 'G3 · Ribera de Curtidores 31 · unidad radical · 25-10-2026 · modelos de estudio, no ejecutivos')
    c.drawRightString(W - 12 * MM, 8 * MM, f'{titulo} · {pagina[0]}')


def cabecera(t, s=''):
    c.setFillColorRGB(0.13, 0.13, 0.13)
    c.setFont(F, 13)
    c.drawString(12 * MM, H - 14 * MM, t)
    if s:
        c.setFont(F, 8)
        c.setFillColorRGB(0.35, 0.35, 0.35)
        c.drawString(12 * MM, H - 19 * MM, s)


def imagen(ruta, x, y, w, h):
    if not os.path.exists(ruta):
        return
    img = ImageReader(ruta)
    iw, ih = img.getSize()
    s = min(w / iw, h / ih)
    c.drawImage(img, x + (w - s * iw) / 2, y + (h - s * ih) / 2, s * iw, s * ih)


def pagina_imagenes(titulo, sub, rutas, cols, filas, pie_t):
    cabecera(titulo, sub)
    x0, y0 = 12 * MM, 14 * MM
    aw, ah = W - 24 * MM, H - 36 * MM
    cw, ch = aw / cols, ah / filas
    for i, r in enumerate(rutas[:cols * filas]):
        col, fila = i % cols, i // cols
        imagen(r, x0 + col * cw + 2, y0 + ah - (fila + 1) * ch + 2, cw - 4, ch - 4)
    pie(pie_t)
    c.showPage()


def pagina_texto(titulo, lineas):
    cabecera(titulo)
    c.setFont(F, 10)
    c.setFillColorRGB(0.13, 0.13, 0.13)
    y = H - 30 * MM
    for l in lineas:
        if l.startswith('## '):
            c.setFont(F, 12); c.drawString(12 * MM, y, l[3:]); c.setFont(F, 10); y -= 7 * MM
        else:
            c.drawString(12 * MM, y, l); y -= 5.2 * MM
        if y < 15 * MM:
            pie(titulo); c.showPage(); cabecera(titulo); c.setFont(F, 10); y = H - 30 * MM
    pie(titulo)
    c.showPage()


V = os.path.join(RAIZ, 'vistas')
P = os.path.join(RAIZ, 'planos')
D = os.path.join(RAIZ, 'diagramas')
uni = json.load(open(os.path.join(RAIZ, 'verificacion', 'UNIDADES.json')))
unio = json.load(open(os.path.join(RAIZ, 'verificacion', 'UNIONES.json')))

# 0 · portada
pagina_texto('Unidad radical · modelos, escenas, cuerpos, uniones y diagramas', [
    'Todo lo que hay aquí sale de las 150 escenas de cómo vive la juventud hoy (01_150_ESCENAS.md) y de lo que tienen en común:',
    'un cuerpo tumbado en 1,25 × 2 m con una pantalla, a una hora distinta de las demás, regulando con membranas ligeras cuánto se le ve y se le oye.',
    '',
    '## Seis unidades de 15 m² (mínimo normativo de la unidad privativa), cada una con sus estados',
    'H1 · La cama con canto · H2 · El casco · H3 · La superficie silenciosa · H4 · El turno · H5 · La mochila y el dock · H6 · La topografía',
    'Para cada una: axonometría abierta y cerrada, cortada a +1,60, planta y dos secciones a 1:25, y tres escenas de capacidad (dos cuerpos, seis sentadas, tres días sin salir).',
    'En H3, además, diez escenas habitadas (E006, E029, E035, E042, E058, E096, E117, E134, E140, E149).',
    '',
    '## Dieciséis cuerpos',
    'Alta y delgada, baja y gorda, gorda y alta, flaca y friolera, twink, peluda y calurosa, trans en transición, con dolor crónico, silla de ruedas, muy musculada,',
    'pareja estable, con insomnio y ansiedad, embarazada, muy baja, sorda, con perro. Cada uno exige medidas; la matriz dice qué unidad las cumple (D08, D10).',
    '',
    '## Cinco uniones de 40 en la parcela real',
    'U1 · El campo · U2 · Las terrazas · U3 · Los racimos de comisión · U4 · La torre de turnos · U5 · La plaza-acampada. Con los vecinos del Catastro y las alturas del sol.',
    'Dato que sale del empaquetado: en una bandeja de la parcela caben 14 superficies H3 (o 19 docks H5), no 40. Para 40 hacen falta tres niveles.',
    '',
    '## Diez diagramas de lo previo a la arquitectura',
    'D01 reloj de escenas · D02 con qué se mide el mundo desde la cama · D03 membranas · D04 tamaños · D05 sol por alturas · D06 turnos · D07 dónde está lo común ·',
    'D08 cuerpos × unidades · D09 cuántas caben y cuántas ven el cielo · D10 lo que cada cuerpo exige.',
    '',
    'Archivos: modelos/UNIDADES_H1_H6.3dm y modelos/UNIONES_U1_U5.3dm (Rhino 8, metros, mallas de estudio, capas por unidad, estado y escena); vistas/, planos/, diagramas/ (PNG + SVG);',
    'verificacion/ (JSON y tablas). Todo se regenera con fuentes/generar_unidades.py, fuentes/uniones.py, fuentes/diagramas.py y fuentes/montar_pdf.py.',
    '',
    'Lo que no está demostrado: aislamiento acústico (DB-HR), estructura, instalaciones, evacuación, normativa de coliving (contrastar los 15 m² con el texto oficial).',
])

# 1 · unidades
pagina_imagenes('Las seis unidades a la misma escala', 'membranas abiertas · 15 m² de superficie privada cada una', [f'{V}/unidades/00_las_seis_unidades.png'], 1, 1, 'unidades')
for u in uni:
    uid = u['id']
    sub = f"{u['nombre']} · superficie blanda {u['area_blanda']} m² · huella {u['area_huella']} m² · cierre: {u['cierre']} · cielo: {u['cielo']} · sonido: {u['sonido']}"
    rutas = [f'{V}/unidades/{uid}_abierta.png', f'{V}/unidades/{uid}_cerrada.png', f'{V}/unidades/{uid}_cortada_160.png',
             f'{P}/{uid}_planta_1_25.png', f'{P}/{uid}_seccion_1_25.png', f'{P}/{uid}_seccion_long_1_25.png']
    pagina_imagenes(f'{uid} · {u["nombre"]}', sub, rutas, 3, 2, uid)
    extra = [r for r in [f'{V}/unidades/{uid}_media.png', f'{V}/unidades/{uid}_verano.png', f'{V}/unidades/{uid}_dividida.png', f'{V}/unidades/{uid}_cortada_160_cerrada.png'] if os.path.exists(r)]
    rutas2 = [f'{V}/unidades/{uid}_E042.png', f'{V}/unidades/{uid}_E058.png', f'{V}/unidades/{uid}_E096.png'] + extra
    pagina_imagenes(f'{uid} · {u["nombre"]} · capacidad y estados', 'E042 dos cuerpos · E058 previa de seis · E096 tres días sin salir · y los demás estados de la membrana', rutas2, 3, 2, uid)

# 2 · escenas H3
esc = sorted(glob.glob(f'{V}/unidades/H3_escena_*.png'))
pagina_imagenes('H3 habitada · diez de las 150 escenas', 'cuerpos del catálogo colocados en la superficie silenciosa; la membrana en el estado que pide cada escena', esc[:6], 3, 2, 'escenas')
pagina_imagenes('H3 habitada · diez de las 150 escenas (continuación)', '', esc[6:], 3, 2, 'escenas')

# 3 · cuerpos
pagina_imagenes('Cuerpos × unidades', '', [f'{D}/D08_cuerpos_x_unidades.png'], 1, 1, 'cuerpos')
pagina_imagenes('Lo que cada cuerpo exige de la superficie', '', [f'{D}/D10_cuerpos_medidas.png'], 1, 1, 'cuerpos')

# 4 · uniones
for u in unio:
    uid = u['id']
    sub = f"{u['unidades']} unidades · {u['con_cielo']} con cielo en vertical · niveles a " + ', '.join(f'+{z:.1f}' for z in u['alturas']) + f" · {u['nota']}"
    rutas = [f'{V}/uniones/{uid}_contexto.png', f'{V}/uniones/{uid}_solo.png', f'{V}/uniones/{uid}_desde_la_calle.png', f'{P}/{uid}_planta_1_250.png', f'{P}/{uid}_seccion_1_250.png']
    pagina_imagenes(f'{uid} · {u["nombre"]}', sub[:230], rutas, 3, 2, uid)

# 5 · diagramas
for d in ['D01_reloj_de_escenas', 'D02_con_que_se_mide_el_mundo', 'D03_membranas', 'D04_tamanos', 'D05_sol_por_alturas', 'D06_turnos', 'D07_donde_esta_lo_comun', 'D09_parcela_capacidad']:
    pagina_imagenes(d.replace('_', ' '), '', [f'{D}/{d}.png'], 1, 1, 'diagramas')

c.save()
print('pdf ok', pagina[0], 'páginas')
