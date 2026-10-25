# -*- coding: utf-8 -*-
"""FASE FINAL - REFERENCE_PACKS.pdf: el 3D como base de control geometrico para la
fase de imagenes IA. Un pack por vista hero: beauty + 6 passes de control."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
import refugio_editorial as E  # noqa: E402

OUT = os.path.join(BASE, '09_RENDERS_Y_REPRESENTACION')
RP = os.path.join(OUT, '_pipeline', 'refpacks')

VISTAS = [
    ('H1', 'Hero general a nivel de ojo', 'plaza completa: cinta, mástiles, dosel, gotas'),
    ('H2', 'Frente oeste', 'copas C1 con escalera-viga y jardineras de borde'),
    ('H3', 'La lámina jugable', 'splash y estanques con la estructura detrás'),
    ('H4', 'Corredor visual a Correos', 'el dosel enmarcando torre y reloj'),
    ('H5', 'Sobre la cinta', 'el mirador en movimiento a cota +6'),
    ('H6', 'Entre mástiles', 'el bosque estructural con los pods rosa'),
    ('H7', 'Aérea general', 'las tres copas, la cinta y el claro ceremonial'),
    ('F1_INTERIOR_DOSEL', 'Interior del dosel', 'mirando arriba: hojas y microalgas'),
    ('F2_HUERTO', 'El huerto C1', 'maíz por fases, goteo, mulch'),
    ('F3_ATRIO_ESTACION', 'Atrio del Metro', 'marquesina volada y bolardos'),
    ('F4_CARLOS_III', 'Carlos III', 'la estatua con el refugio detrás'),
    ('F5_DETALLE_NUDO', 'Nudo mástil-hoja', 'cables, casquillos y tensores 1:5'),
]
PASSES = ['beauty', 'clay', 'clay_sinveg', 'ao', 'depth', 'normal', 'edges', 'id_mat']

doc = E.Doc(os.path.join(OUT, 'REFERENCE_PACKS.pdf'), 'REFERENCE PACKS', '09 · RENDERS')
E.portada(doc, 'El 3D como\nbase de control',
          'Doce vistas hero con su paquete completo de control geométrico: beauty '
          'neutro, clay con y sin vegetación, oclusión, profundidad, normales, líneas '
          'y máscaras de familia. La base fiel sobre la que la fase de imágenes IA '
          'podrá ser atmosférica, vegetal y viva SIN rediseñar el proyecto.',
          '09 · RENDERS Y REPRESENTACIÓN · CONTROL GEOMÉTRICO',
          [('VISTAS', str(len(VISTAS))), ('PASSES POR VISTA', '8'),
           ('RESOLUCIÓN', '1920×1200'), ('ESCENA', 'v006 build 12')],
          img=os.path.join(RP, 'H1', 'beauty.png'), num='RP')

# pagina de uso
p = doc.page('CÓMO USAR LOS PACKS')
y = E.A4H - 1.0
y = p.kicker(y, 'RP-00 · PROPÓSITO Y REGLAS DE USO')
y = p.title(y, 'La IA potencia; el 3D manda', size=16)
y = p.dashlist(E.MX, y - 0.02, [
    ('beauty.png', 'imagen base con materiales y luz PSA de tarde: referencia de color, '
     'escala y relación urbana. Punto de partida img2img de denoise moderado.'),
    ('depth.png + normal.png', 'control duro de geometría (tipo ControlNet '
     'depth/normalbae): la IA no puede mover un mástil ni engordar la cinta.'),
    ('edges.png', 'control de línea (Sobel de depth+normal): conserva barandillas, '
     'costillas y perfiles finos que el depth solo no protege.'),
    ('id_mat.png', 'máscaras por familia (granito/vegetación/rosa/agua/contexto/madera/'
     'canopy/monumento): inpainting selectivo — enriquecer la vegetación SIN tocar la '
     'estructura, revivir el agua SIN alterar fachadas.'),
    ('clay.png / clay_sinveg.png', 'lectura volumétrica pura y variante sin verde: '
     'para regenerar la vegetación completa con IA manteniendo la estructura exacta.'),
    ('ao.png', 'oclusión pura: refuerzo de contacto y sombra propia en el compositing.'),
    ('CAMERA_METADATA.json', 'cámara exacta reproducible: posición, target, matriz '
     'mundo, FOV vertical, focal equivalente, clipping y resolución.'),
], wrap=88, gap=0.09)
y -= 0.06
y = p.kicker(y, 'RP-01 · REGLA DE FIDELIDAD JERÁRQUICA')
y = p.tabla(E.MX, y, E.A4W - 2 * E.MX,
            ['NIVEL', 'ELEMENTOS', 'QUÉ PUEDE HACER LA IA'],
            [['HARD LOCK', 'arquitectura, cámara, estructura, pasarela, escaleras, '
              'ascensores, canopies, mástiles, pods, agua construida, edificios, '
              'Metro, Carlos III, geometría urbana principal',
              'NADA: coincidencia con edges/depth; cualquier mutación descarta la imagen'],
             ['SOFT LOCK', 'jardineras, mobiliario, distribución y masa general de la '
              'vegetación', 'variar densidad y textura DENTRO de su huella id_mat; no '
              'crear ni borrar piezas'],
             ['CONTROLLED FREEDOM', 'hojas individuales, pequeñas ramas, personas, '
              'vapor, salpicaduras, reflejos, textura superficial, imperfecciones, '
              'atmósfera', 'libertad total: aquí vive lo fotográfico y lo vivo']],
            col_w=[1.05, 3.75, 2.2], size=6.6)
p.text(E.MX, y - 0.04, 'edges.png impide el rediseño estructural; NO exige coincidencia '
       'píxel a píxel de fenómenos orgánicos. El piloto (una sola vista, H1) congela el '
       'método antes de aplicarlo al resto: pack › generación › comprobación geométrica '
       '› corrección › versión final.', size=7.2, color='#4a4a4a', wrap=112)
doc.add(p)

# una pagina por vista
import matplotlib.image as mpimg  # noqa: E402
import io as _io


def io_open(p):
    return _io.open(p, encoding='utf-8')
for cam, tit, desc in VISTAS:
    d = os.path.join(RP, cam)
    if not os.path.exists(os.path.join(d, 'beauty.png')):
        continue
    p = doc.page('RP · ' + cam)
    y = E.A4H - 0.95
    y = p.kicker(y, 'PACK · ' + cam)
    y = p.title(y, tit, size=14)
    p.text(E.MX, y + 0.02, desc, size=8, color='#4a4a4a')
    y -= 0.18
    ax = p.axes(E.MX, y - 4.35, E.A4W - 2 * E.MX, 4.3)
    ax.imshow(E.load_img_small(os.path.join(d, 'beauty.png')), aspect='auto')
    ax.set_xticks([]); ax.set_yticks([])
    y -= 4.58
    # tira de passes 4 x 2
    tile_w = (E.A4W - 2 * E.MX - 3 * 0.10) / 4
    tile_h = tile_w * 0.625
    x = E.MX
    fila = 0
    for k, ps in enumerate([q for q in PASSES if q != 'beauty']):
        f = os.path.join(d, ps + '.png')
        if not os.path.exists(f):
            continue
        ax = p.axes(x, y - tile_h, tile_w, tile_h)
        ax.imshow(E.load_img_small(f, 480), aspect='auto')
        ax.set_xticks([]); ax.set_yticks([])
        p.text(x, y + 0.03, ps.upper(), size=5.2, tracked=True, color=E.GRAYTX)
        x += tile_w + 0.10
        if (k + 1) % 4 == 0:
            x = E.MX
            y -= tile_h + 0.22
    # ficha de camara: la vista es reproducible desde estos numeros
    import json as _json
    fmeta = os.path.join(d, 'CAMERA_METADATA.json')
    if os.path.exists(fmeta):
        m = _json.load(io_open(fmeta))
        y -= tile_h + 0.30
        y = p.tabla(E.MX, y, E.A4W - 2 * E.MX,
                    ['CÁMARA', 'POSICIÓN (X Y Z)', 'OBJETIVO', 'FOV V', 'FOCAL EQ.', 'CLIP'],
                    [[m['camera_id'],
                      ' '.join('%.1f' % v for v in m['location']),
                      (' '.join('%.1f' % v for v in m['target']) if m.get('target') else '—'),
                      '%.1f°' % m['fov_vertical_deg'],
                      '%.0f mm' % m['focal_equiv_35mm_sensor24'],
                      '%.2f–%.0f m' % (m['clip_start'], m['clip_end'])]],
                    col_w=[1.55, 1.55, 1.35, 0.6, 0.85, 1.1], size=6.6)
    doc.add(p)
doc.close()
print('REFERENCE_PACKS ok', doc.folio, 'pp')
