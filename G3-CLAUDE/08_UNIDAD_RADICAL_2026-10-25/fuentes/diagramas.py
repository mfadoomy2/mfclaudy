"""Diagramas analíticos: lo previo a la arquitectura. Fondo blanco, colores vivos, títulos discretos,
sin figuras humanas (los cuerpos son cápsulas de medida). Salida PNG + SVG en ../diagramas."""
import csv
import json
import math
import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, Wedge, FancyBboxPatch, Polygon as MplPoly, Circle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import FAMILIA  # registra la fuente
from geom3d import COL
from cuerpos import CATALOGO

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
D = os.path.join(RAIZ, 'diagramas')
os.makedirs(D, exist_ok=True)
plt.rcParams['font.family'] = FAMILIA
plt.rcParams['svg.fonttype'] = 'none'

ESC = list(csv.DictReader(open(os.path.join(RAIZ, 'escenas.csv'), encoding='utf-8')))
A3 = (42.0 / 2.54, 29.7 / 2.54)
A4 = (29.7 / 2.54, 21.0 / 2.54)
GRIS = '#555555'
C_LUGAR = {'cama': '#D81B8A', 'suelo': '#F4A6C6', 'mesa': '#F26A1B', 'cocina': '#FFD23F', 'bano': '#36C5D1', 'umbral': '#7B2CBF', 'comun': '#2DC653', 'fuera': '#1F7A8C'}
C_EXPO = {'ocultarse': '#1F7A8C', 'controlar': '#36C5D1', 'mostrarse': '#F26A1B', 'indiferente': '#BBBBBB'}


def hora(f):
    h, m = f['hora'].split(':')
    return int(h) + int(m) / 60


def hoja(tam=A3, titulo='', sub=''):
    fig = plt.figure(figsize=tam, dpi=150)
    if titulo:
        fig.text(0.03, 0.965, titulo, fontsize=13, ha='left', va='top', color='#222222')
    if sub:
        fig.text(0.03, 0.935, sub, fontsize=8, ha='left', va='top', color=GRIS)
    return fig


def guardar(fig, nombre):
    fig.savefig(os.path.join(D, nombre + '.png'), facecolor='white')
    fig.savefig(os.path.join(D, nombre + '.svg'), facecolor='white')
    plt.close(fig)
    print('·', nombre)


# ---------------------------------------------------------------------------

def D01_reloj():
    fig = hoja(A3, 'D01 · El reloj de las 150 escenas', 'cada punto es una escena a su hora; el anillo dice dónde pasa (la cama en el centro, la calle fuera); el color, lo que esa persona necesita respecto a ser vista u oída')
    ax = fig.add_axes([0.05, 0.05, 0.6, 0.85], projection='polar')
    ax.set_theta_zero_location('N'); ax.set_theta_direction(-1)
    anillos = ['cama', 'suelo', 'mesa', 'cocina', 'bano', 'umbral', 'comun', 'fuera']
    rng = np.random.default_rng(3)
    for f in ESC:
        th = hora(f) / 24 * 2 * math.pi
        r = anillos.index(f['lugar']) + 1 + rng.uniform(-0.3, 0.3)
        ax.scatter(th, r, s=95, color=C_EXPO[f['exposicion']], edgecolor='white', linewidth=0.6, zorder=3)
    ax.set_xticks([i / 24 * 2 * math.pi for i in range(0, 24, 3)])
    ax.set_xticklabels([f'{i:02d}:00' for i in range(0, 24, 3)], fontsize=8, color=GRIS)
    ax.set_yticks(range(1, 9)); ax.set_yticklabels(anillos, fontsize=7, color=GRIS)
    ax.set_ylim(0, 8.6); ax.grid(color='#DDDDDD', lw=0.5)
    ax.spines['polar'].set_visible(False)
    # noche sombreada
    th = np.linspace(22 / 24 * 2 * math.pi, (24 + 7) / 24 * 2 * math.pi, 100)
    ax.fill_between(th, 0, 8.6, color='#F2F2F2', zorder=0)
    # leyenda y cifras
    ax2 = fig.add_axes([0.68, 0.12, 0.3, 0.75]); ax2.axis('off')
    y = 1.0
    for k, c in C_EXPO.items():
        n = sum(1 for f in ESC if f['exposicion'] == k)
        ax2.scatter([0.03], [y], s=120, color=c); ax2.text(0.08, y, f'{k} · {n}', va='center', fontsize=9)
        y -= 0.06
    y -= 0.04
    franjas = {'07–12': 0, '12–17': 0, '17–22': 0, '22–07': 0}
    for f in ESC:
        h = hora(f)
        franjas['07–12' if 7 <= h < 12 else '12–17' if 12 <= h < 17 else '17–22' if 17 <= h < 22 else '22–07'] += 1
    for k, n in franjas.items():
        ax2.barh(y, n / 60, height=0.035, color='#333333' if k == '22–07' else '#BBBBBB', left=0.03)
        ax2.text(0.03 + n / 60 + 0.01, y, f'{k} · {n}', va='center', fontsize=9)
        y -= 0.055
    y -= 0.04
    n_cama = sum(1 for f in ESC if f['lugar'] == 'cama')
    ax2.text(0.03, y, f'{n_cama} de 150 escenas pasan en la cama', fontsize=10, color='#D81B8A'); y -= 0.05
    ax2.text(0.03, y, f'{sum(1 for f in ESC if hora(f) >= 22 or hora(f) < 7)} entre las 22:00 y las 7:00', fontsize=10); y -= 0.05
    ax2.text(0.03, y, f"{sum(1 for f in ESC if f['exposicion'] in ('ocultarse', 'controlar'))} necesitan no ser vistas u oídas, o controlarlo", fontsize=10); y -= 0.05
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1.05)
    guardar(fig, 'D01_reloj_de_escenas')


def D02_lo_que_mide():
    fig = hoja(A3, 'D02 · Con qué se mide el mundo desde la cama', 'sección a escala: un cuerpo reclinado en la superficie y los instrumentos con los que hoy se concibe el exterior; ángulos y distancias medidos, no simbólicos')
    ax = fig.add_axes([0.04, 0.08, 0.92, 0.8]); ax.set_aspect('equal'); ax.axis('off')
    # superficie y canto
    ax.add_patch(Rectangle((0, 0), 4.35, 0.33, color=COL['plinto']))
    ax.add_patch(Rectangle((0, 0.33), 4.35, 0.12, color=COL['blando']))
    ax.add_patch(Rectangle((-0.3, 0), 0.3, 0.45, color=COL['canto'])); ax.add_patch(Rectangle((-0.65, 0), 0.35, 0.72, color=COL['canto']))
    ax.add_patch(Rectangle((4.35, 0), 0.3, 0.45, color=COL['canto'])); ax.add_patch(Rectangle((4.65, 0), 0.35, 0.72, color=COL['canto']))
    # cuerpo reclinado: cápsulas
    ax.add_patch(FancyBboxPatch((1.0, 0.45), 1.0, 0.24, boxstyle='round,pad=0,rounding_size=0.12', color='#D81B8A'))
    ax.add_patch(FancyBboxPatch((1.95, 0.45), 0.9, 0.26, boxstyle='round,pad=0,rounding_size=0.13', color='#D81B8A', transform=matplotlib.transforms.Affine2D().rotate_deg_around(1.95, 0.45, 42) + ax.transData))
    ojo = (2.55, 1.05)
    ax.scatter(*ojo, s=20, color='black', zorder=5)
    # móvil a 0,30 m: 0,15 m de alto a 28°
    d, hm = 0.30, 0.15
    ang = math.degrees(2 * math.atan(hm / 2 / d))
    px, py = ojo[0] - 0.05, ojo[1] - 0.42
    ax.add_patch(Rectangle((px - 0.03, py), 0.012, hm, color='#FFD23F', transform=matplotlib.transforms.Affine2D().rotate_deg_around(px, py, -25) + ax.transData))
    ax.add_patch(Wedge(ojo, 0.9, 180 + 45, 180 + 45 + ang, color='#FFD23F', alpha=0.25))
    ax.text(ojo[0] - 1.0, ojo[1] - 0.95, f'móvil · 6,1" a 0,30 m\n{ang:.0f}° del campo visual', fontsize=8, color='#8A6D00')
    # portátil a 0,55 m: 0,22 de alto a 23°
    d2, hp = 0.55, 0.22
    ang2 = math.degrees(2 * math.atan(hp / 2 / d2))
    ax.add_patch(Rectangle((ojo[0] - 0.75 - 0.33, 0.47), 0.33, 0.015, color=COL['canto']))
    ax.add_patch(Rectangle((ojo[0] - 0.75 - 0.33, 0.47), 0.015, hp, color='#F26A1B'))
    ax.text(ojo[0] - 1.9, 0.75, f'portátil · 13" a 0,55 m · {ang2:.0f}°', fontsize=8, color='#B04A10')
    # cámara del portátil: 70° horizontales: lo que enseña a 1,5 m detrás
    cam = (ojo[0] - 0.75 - 0.33, 0.47 + hp)
    ax.add_patch(Wedge(cam, 2.3, 180 - 35 + 180, 180 + 35 + 180, color='#36C5D1', alpha=0.18))
    ax.plot([cam[0], cam[0] + 2.3 * math.cos(math.radians(35))], [cam[1], cam[1] + 2.3 * math.sin(math.radians(35))], color='#1F7A8C', lw=0.8, ls='--')
    ax.plot([cam[0], cam[0] + 2.3 * math.cos(math.radians(-35))], [cam[1], cam[1] + 2.3 * math.sin(math.radians(-35))], color='#1F7A8C', lw=0.8, ls='--')
    ax.text(cam[0] + 2.0, cam[1] + 1.65, 'la cámara: 70°\nlo que enseña a 2 m es 2,8 m de ancho:\nla membrana cerrada es el fondo', fontsize=8, color='#1F7A8C')
    # cascos: radio de silencio 0 m; voz: 3 m; altavoz pequeño: 6 m
    for r, t, c in [(0.25, 'cascos · el silencio mide 0,25 m', '#7B2CBF'), (3.0, 'voz al móvil · 3 m', '#7B2CBF'), (6.0, 'altavoz pequeño · 6 m, atraviesa un tabique de 7 cm', '#7B2CBF')]:
        ax.add_patch(Circle(ojo, r, fill=False, ec=c, lw=0.9, ls=':' if r > 1 else '-'))
        ax.text(ojo[0] + r * 0.72, ojo[1] + r * 0.72 + 0.05, t, fontsize=7.5, color=c)
    # cielo: hueco 2,0 × 1,4 a 2,6 m a ángulo de cielo
    ax.add_patch(Rectangle((-0.7, 2.6), 1.9, 0.05, color=COL['cielo'], alpha=0.8))
    ax.add_patch(Rectangle((3.15, 2.6), 1.9, 0.05, color=COL['cielo'], alpha=0.8))
    for x in (1.2, 3.15):
        ax.plot([ojo[0], x], [ojo[1], 2.6], color='#8A6D00', lw=0.7, ls='--')
    ang3 = math.degrees(math.atan((3.15 - ojo[0]) / (2.6 - ojo[1])) + math.atan((ojo[0] - 1.2) / (2.6 - ojo[1])))
    ax.text(1.3, 2.75, f'el cielo propio: hueco de 2,0 m a 2,6 m a {ang3:.0f}° desde la cama', fontsize=8, color='#8A6D00')
    # cotas
    ax.annotate('', (0, -0.25), (4.35, -0.25), arrowprops=dict(arrowstyle='<->', lw=0.6)); ax.text(2.17, -0.42, '4,35 m · 15 m² con 3,45 de fondo', ha='center', fontsize=8)
    ax.annotate('', (-1.0, 0), (-1.0, 0.72), arrowprops=dict(arrowstyle='<->', lw=0.6)); ax.text(-1.08, 0.36, '0,72\nmesa', ha='right', va='center', fontsize=7)
    ax.annotate('', (-1.0, 0), (-1.0, 0.45), arrowprops=dict(arrowstyle='<->', lw=0.6, color='#999')); ax.text(-1.08, 0.1, '0,45\nasiento', ha='right', va='center', fontsize=7, color='#777')
    ax.set_xlim(-2.6, 7.4); ax.set_ylim(-0.7, 3.4)
    guardar(fig, 'D02_con_que_se_mide_el_mundo')


def D03_membranas():
    fig = hoja(A3, 'D03 · Las membranas que ya usa la juventud', 'lo que separa en las 150 escenas no es un tabique; cada membrana bloquea una cosa distinta y cuesta lo que cuesta. Las dos últimas filas son las del proyecto')
    items = [
        ('cascos', [1, 0, 0, 1], 'E026 · E035 · E045 · E138', 30),
        ('cámara apagada', [0, 1, 0, 0], 'E007 · E117', 0),
        ('fondo de cámara (cama hecha)', [0, 1, 0, 0], 'E006 · E009 · E110', 0),
        ('edredón por encima', [1, 1, 0, 0], 'E148', 0),
        ('pestillo del baño', [1, 1, 1, 0], 'E027 · E091', 0),
        ('puerta cerrada como señal', [0, 1, 1, 0], 'E074 · E149', 0),
        ('modo avión', [0, 0, 1, 1], 'E051', 0),
        ('persiana bajada de día', [0, 1, 0, 1], 'E011 · E012 · E018', 40),
        ('cortina / sábana colgada', [0, 1, 0, 0], 'E037', 10),
        ('cola de la ducha, turno de lavadora', [0, 0, 0, 1], 'E003 · E036 · E115', 0),
        ('chat del piso (hablar sin pasillo)', [1, 1, 1, 0], 'E071 · E072', 0),
        ('tabique de 7 cm', [0, 1, 0, 0], 'E044 · E025 · E035', 900),
        ('membrana H3 (tela acústica en aro)', [1, 1, 1, 0], 'proyecto · por caracterizar', 400),
        ('casco H2 (doble piel 0,25)', [1, 1, 1, 1], 'proyecto · DB-HR', 6000),
    ]
    cols = ['sonido', 'vista', 'presencia', 'tiempo']
    ax = fig.add_axes([0.28, 0.08, 0.42, 0.8]); ax.axis('off')
    n = len(items)
    for j, c in enumerate(cols):
        ax.text(j, n + 0.3, c, ha='center', fontsize=9, color=GRIS)
    for i, (nom, v, esc, coste) in enumerate(items):
        y = n - 1 - i
        ax.text(-0.6, y, nom, ha='right', va='center', fontsize=9, color='#222' if i < 12 else '#D81B8A')
        for j, b in enumerate(v):
            ax.add_patch(Circle((j, y), 0.3, color=['#EEEEEE', '#1F7A8C', '#36C5D1', '#7B2CBF', '#F26A1B'][j + 1] if b else '#EEEEEE'))
        ax.text(3.7, y, esc, va='center', fontsize=7.5, color=GRIS)
        ax.barh(y, min(coste, 6000) / 6000 * 2.2, height=0.35, left=7.2, color='#F26A1B' if coste else '#EEEEEE')
        ax.text(7.2 + min(coste, 6000) / 6000 * 2.2 + 0.1, y, f'{coste} €' if coste else '0 €', va='center', fontsize=7.5, color=GRIS)
    ax.text(8.3, n + 0.3, 'coste aproximado (hipótesis)', ha='center', fontsize=9, color=GRIS)
    ax.set_xlim(-6, 10.5); ax.set_ylim(-1, n + 1)
    guardar(fig, 'D03_membranas')


def D04_tamanos():
    fig = hoja(A3, 'D04 · Tamaños, a la misma escala', 'lo que ocupa hoy una persona joven, lo que le damos y lo que mide la parcela. 40 superficies de 15 m² son 600 m²; la parcela tiene 650,9, pero en una bandeja solo caben 14–18 porque tiene 15 m de ancho')
    ax = fig.add_axes([0.03, 0.05, 0.94, 0.85]); ax.set_aspect('equal'); ax.axis('off')
    items = [('colchón 1,25 × 2,00', 1.25, 2.0, '#D81B8A'), ('tienda de Sol 2 × 2', 2.0, 2.0, '#36C5D1'), ('habitación N19B 12,0 m²', 3.43, 3.5, '#BBBBBB'),
             ('superficie 15 m² (3,45 × 4,35)', 3.45, 4.35, '#F4A6C6'), ('habitación V01 18,35 m²', 3.9, 4.7, '#BBBBBB'), ('piso de mercado · 40 m² por persona', 5.5, 7.3, '#DDDDDD')]
    x = 0
    for nom, w, h, c in items:
        ax.add_patch(Rectangle((x, 0), w, h, color=c, alpha=0.9))
        ax.text(x + w / 2, -0.5, f'{nom}', ha='right', va='top', fontsize=7.5, rotation=45)
        ax.text(x + w / 2, h + 0.2, f'{w * h:.1f} m²', ha='center', fontsize=8, color=GRIS)
        x += w + 1.2
    # parcela
    from uniones import PARCELA
    px, py = PARCELA.exterior.xy
    ox, oy = 0, 11.0
    ax.add_patch(MplPoly(np.column_stack([np.array(px) - 12 + ox, np.array(py) + 8 + oy]), closed=True, color=COL['parcela'], ec='#333', lw=0.8))
    ax.text(ox + 1, oy + 17.5, 'parcela 650,9 m² · 14,98 m de frente · 49,5 m de fondo', fontsize=8)
    # 40 × 15 m² como rejilla al lado
    gx, gy = 0, 32
    for i in range(40):
        r, c = divmod(i, 10)
        ax.add_patch(Rectangle((gx + c * 3.9, gy + r * 4.8), 3.45, 4.35, color='#F4A6C6', ec='white'))
    ax.text(gx, gy + 4 * 4.8 + 0.4, '40 × 15 m² = 600 m² de superficie privada, sin canto ni paso', fontsize=8)
    # una bandeja: 14-18
    ax.text(ox + 1, oy - 1.2, 'en una bandeja caben 14 superficies H3 con canto y paso (o 18–19 docks H5): hacen falta 3 bandejas para 40', fontsize=8, color='#D81B8A')
    ax.set_xlim(-1, 42); ax.set_ylim(-3, 56)
    guardar(fig, 'D04_tamanos')


def D05_sol():
    fig = hoja(A3, 'D05 · El sol por alturas y dónde se ponen las superficies', '21 de diciembre: porcentaje de la parcela con ≥ 2 h de sol a cada altura (SOL_POR_ALTURA_ESTUDIO_PREVIO.json, modelo 2,5D con alturas catastrales) · vecinos: 7–8 plantas al sur en la medianera, 7–10 al norte y al este a 7–12 m')
    datos = {0: 3.1, 4: 6.7, 7.1: 8.6, 10.2: 10.5, 13.3: 12.7, 16.4: 16.5, 19.5: 33.4, 22.6: 65.2, 25.7: 100.0}
    ax = fig.add_axes([0.08, 0.1, 0.4, 0.78])
    hs = list(datos.keys()); ps = list(datos.values())
    ax.barh(hs, ps, height=2.4, color=[COL['cielo'] if p >= 50 else '#DDDDDD' for p in ps])
    for h, p in datos.items():
        ax.text(p + 1.5, h, f'{p:.0f} %', va='center', fontsize=8)
    ax.axvline(50, color='#D81B8A', lw=0.8, ls='--'); ax.text(51, 27.5, 'la mitad de la parcela, hacia +21 m', fontsize=8, color='#D81B8A')
    ax.set_xlabel('% de la parcela con ≥ 2 h de sol el 21-dic', fontsize=8); ax.set_ylabel('altura sobre la calle (m)', fontsize=8)
    ax.set_xlim(0, 115); ax.set_ylim(-2, 32)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=8)
    # alturas de las uniones
    ax2 = fig.add_axes([0.55, 0.1, 0.42, 0.78])
    try:
        uni = json.load(open(os.path.join(RAIZ, 'verificacion', 'UNIONES.json')))
    except Exception:
        uni = []
    for k, u in enumerate(uni):
        for z in u['alturas']:
            ax2.plot([k - 0.3, k + 0.3], [z, z], color='#1F7A8C', lw=3)
        ax2.text(k, 31, f"{u['id']}\n{u['unidades']} u.\n{u['con_cielo']} con cielo", ha='center', fontsize=8)
    ax2.axhspan(21, 32, color=COL['cielo'], alpha=0.15); ax2.text(-0.45, 21.3, 'desde +21 m, más de la mitad de la parcela tiene sol', fontsize=7.5, color='#8A6D00')
    ax2.set_ylim(-2, 36); ax2.set_xlim(-0.6, len(uni) - 0.4 if uni else 4); ax2.set_xticks([]); ax2.set_ylabel('m', fontsize=8); ax2.tick_params(labelsize=8)
    for s in ('top', 'right', 'bottom'):
        ax2.spines[s].set_visible(False)
    ax2.set_title('alturas de las bandejas en U1–U5', fontsize=9, loc='left', color=GRIS)
    guardar(fig, 'D05_sol_por_alturas')


def D06_turnos():
    fig = hoja(A3, 'D06 · ¿Funciona el turno? Ocupación de la cama hora a hora', 'proporción de escenas que pasan en la cama en cada franja horaria (de las 150); si todo el mundo está en la cama a las 3:00, dos personas no pueden compartir una superficie salvo que trabajen de noche')
    ax = fig.add_axes([0.07, 0.12, 0.6, 0.75])
    bins = np.arange(0, 25, 2)
    tot = np.zeros(12); cama = np.zeros(12)
    for f in ESC:
        b = min(int(hora(f) // 2), 11)
        tot[b] += 1
        if f['lugar'] == 'cama':
            cama[b] += 1
    prop = np.where(tot > 0, cama / np.maximum(tot, 1), 0)
    ax.bar(bins[:-1] + 1, prop * 100, width=1.8, color=['#D81B8A' if p > 0.5 else '#F4A6C6' for p in prop])
    for b, p, t in zip(bins[:-1] + 1, prop, tot):
        ax.text(b, p * 100 + 2, f'{p * 100:.0f} %\n({int(t)})', ha='center', fontsize=7, color=GRIS)
    ax.axhline(50, color='#333', lw=0.7, ls='--'); ax.text(0.2, 52, 'por encima del 50 %, dos personas no caben por turnos en una superficie', fontsize=8)
    ax.set_xticks(range(0, 25, 2)); ax.set_xticklabels([f'{h:02d}' for h in range(0, 25, 2)], fontsize=8)
    ax.set_ylabel('% de las escenas de esa franja que pasan en la cama', fontsize=8); ax.set_ylim(0, 110); ax.tick_params(labelsize=8)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax2 = fig.add_axes([0.72, 0.15, 0.26, 0.7]); ax2.axis('off')
    txt = ['Lo que dice:', '', 'De 22:00 a 8:00 casi todas las escenas', 'pasan en la cama. El turno (H4, U4) solo', 'funciona entre quien trabaja de noche', '(bar, reparto, edición) y quien trabaja', 'de día; en Sol funcionaba porque la', 'tienda se desmontaba y la gente rotaba', 'por días, no por horas.', '',
           'Por tanto: el turno no reduce camas a', 'la mitad; como mucho a 2/3, y exige', 'una norma de uso y dos armarios.']
    for i, t in enumerate(txt):
        ax2.text(0, 1 - i * 0.055, t, fontsize=9, color='#222' if i else '#D81B8A')
    guardar(fig, 'D06_turnos')


def D07_lo_comun():
    fig = hoja(A3, 'D07 · Dónde está lo común de la juventud', 'de las 150 escenas: dónde pasa y con quién; el salón compartido de la casa es el sitio que menos aparece, y cuando aparece se evita')
    ax = fig.add_axes([0.06, 0.15, 0.55, 0.7]); ax.axis('off')
    grupos = [('en la cama', lambda f: f['lugar'] == 'cama'), ('en el suelo', lambda f: f['lugar'] == 'suelo'), ('en el umbral: puerta, pasillo, portal, ventana', lambda f: f['lugar'] == 'umbral'),
              ('en el baño', lambda f: f['lugar'] == 'bano'), ('en lo común de la casa: salón, cocina, mesa', lambda f: f['lugar'] in ('comun', 'cocina', 'mesa')), ('fuera: calle, plaza, bar, Sol, transporte', lambda f: f['lugar'] == 'fuera')]
    y = 1.0
    for nom, cond in grupos:
        n = sum(1 for f in ESC if cond(f))
        sub = [f for f in ESC if cond(f)]
        x = 0
        for cq, c in [('sola', '#BBBBBB'), ('sola_conectada', '#36C5D1'), ('otra', '#7B2CBF'), ('grupo', '#2DC653'), ('desconocidos', '#F26A1B')]:
            k = sum(1 for f in sub if f['con_quien'] == cq)
            ax.barh(y, k, left=x, height=0.09, color=c); x += k
        ax.text(x + 1, y, f'{n}', va='center', fontsize=9); ax.text(0, y + 0.065, nom, fontsize=9)
        y -= 0.16
    ax.set_xlim(0, 80); ax.set_ylim(0.0, 1.15)
    ax2 = fig.add_axes([0.66, 0.15, 0.32, 0.7]); ax2.axis('off')
    yy = 1.0
    for cq, c, t in [('sola', '#BBBBBB', 'sola'), ('sola_conectada', '#36C5D1', 'sola pero conectada: el cuerpo solo, la compañía por pantalla'), ('otra', '#7B2CBF', 'con otra persona'), ('grupo', '#2DC653', 'en grupo'), ('desconocidos', '#F26A1B', 'con desconocidos')]:
        n = sum(1 for f in ESC if f['con_quien'] == cq)
        ax2.add_patch(Rectangle((0, yy - 0.03), 0.05, 0.06, color=c)); ax2.text(0.08, yy, f'{t} · {n}', va='center', fontsize=9)
        yy -= 0.09
    yy -= 0.05
    for t in ['Lo común no está en el salón: está en el chat,', 'en la plaza, en el bar y en Sol. La casa de cuatro', 'con cocina-comedor común (V01–V03) resuelve un', 'programa que las escenas no contienen.', '', 'Para el edificio: las comisiones de Sol como', 'común (cocina, lavandería, baños, taller, asamblea,', 'cuidados), y arriba, superficies.']:
        ax2.text(0, yy, t, fontsize=9, color='#222'); yy -= 0.05
    guardar(fig, 'D07_donde_esta_lo_comun')


def D08_cuerpos_unidades():
    fig = hoja(A3, 'D08 · Cuerpos × unidades', 'cada celda: criterios cumplidos de 10 (tumbarse, dos cuerpos, seis sentadas, canto para sentarse, cierre, sonido, temperatura, movilidad, vestirse dentro, perro); reglas en fuentes/matriz_cuerpos.py · las medidas de los cuerpos son hipótesis')
    filas = json.load(open(os.path.join(RAIZ, 'verificacion', 'CUERPOS_X_UNIDADES.json')))
    ids = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6']
    ax = fig.add_axes([0.3, 0.08, 0.45, 0.8]); ax.axis('off')
    n = len(filas)
    for j, u in enumerate(ids):
        ax.text(j, n + 0.4, u, ha='center', fontsize=10)
    tot = [0] * 6
    for i, fila in enumerate(filas):
        y = n - 1 - i
        ax.text(-0.6, y, f"{fila['cuerpo']} · {fila['nombre']} · {fila['estatura']:.2f} m", ha='right', va='center', fontsize=8.5)
        for j, u in enumerate(ids):
            k = fila['unidades'][u]['ok']; tot[j] += k
            col = plt.cm.RdPu(0.15 + 0.8 * k / 10)
            ax.add_patch(Rectangle((j - 0.45, y - 0.42), 0.9, 0.84, color=col))
            ax.text(j, y, str(k), ha='center', va='center', fontsize=9, color='white' if k >= 7 else '#222')
            falla = [kk for kk, v in fila['unidades'][u]['detalle'].items() if not v]
            if falla:
                ax.text(j, y - 0.3, ', '.join(falla)[:28], ha='center', va='center', fontsize=4.5, color='white' if k >= 7 else '#444')
    for j, u in enumerate(ids):
        ax.text(j, -1.0, f'{tot[j]} / {10 * n}', ha='center', fontsize=9, color='#D81B8A')
    ax.set_xlim(-7, 6.5); ax.set_ylim(-1.6, n + 1)
    ax2 = fig.add_axes([0.78, 0.2, 0.2, 0.6]); ax2.axis('off')
    for i, t in enumerate(['Lectura:', '', 'H3 y H4 (superficie con canto', 'y membrana) y H2 (casco) sirven', 'a casi todos los cuerpos.', '', 'H1 falla con dos cuerpos y seis', 'sentadas: la cama es pequeña.', '', 'H5 falla en canto y cierre:', 'un colchón en el suelo no vale', 'para quien tiene dolor ni para', 'quien se viste dentro.', '', 'H6 pierde por vestirse dentro:', 'la cúpula no cierra del todo.']):
        ax2.text(0, 1 - i * 0.055, t, fontsize=9, color='#D81B8A' if i == 0 else '#222')
    guardar(fig, 'D08_cuerpos_x_unidades')


def D09_parcela_capacidad():
    fig = hoja(A3, 'D09 · Cuántas caben y cuántas ven el cielo', 'las cinco uniones de 40 en la parcela real: unidades colocadas, unidades con cielo en vertical, número de niveles; el dato sale del empaquetado en el polígono catastral')
    try:
        uni = json.load(open(os.path.join(RAIZ, 'verificacion', 'UNIONES.json')))
    except Exception:
        uni = []
    ax = fig.add_axes([0.08, 0.15, 0.55, 0.7])
    xs = np.arange(len(uni))
    ax.bar(xs - 0.2, [u['unidades'] for u in uni], width=0.38, color='#F4A6C6', label='unidades (o superficies)')
    ax.bar(xs + 0.2, [u['con_cielo'] for u in uni], width=0.38, color=COL['cielo'], label='con cielo en vertical')
    for k, u in enumerate(uni):
        ax.text(k - 0.2, u['unidades'] + 0.6, str(u['unidades']), ha='center', fontsize=9)
        ax.text(k + 0.2, u['con_cielo'] + 0.6, str(u['con_cielo']), ha='center', fontsize=9)
        ax.text(k, -4.5, f"{u['id']} · {u['nombre']}\n{len(u['alturas'])} niveles · +{min(u['alturas']):.1f} a +{max(u['alturas']):.1f}", ha='center', fontsize=8)
    ax.axhline(40, color='#D81B8A', lw=0.8, ls='--'); ax.text(-0.4, 41, '40 personas', fontsize=8, color='#D81B8A')
    ax.set_xticks([]); ax.set_ylim(0, 46); ax.legend(fontsize=8, frameon=False, loc='upper right'); ax.tick_params(labelsize=8)
    for s in ('top', 'right', 'bottom'):
        ax.spines[s].set_visible(False)
    ax2 = fig.add_axes([0.68, 0.15, 0.3, 0.7]); ax2.axis('off')
    yy = 1.0
    for u in uni:
        ax2.text(0, yy, f"{u['id']} · {u['nombre']}", fontsize=9, color='#D81B8A'); yy -= 0.04
        import textwrap
        for line in textwrap.wrap(u['nota'], 52):
            ax2.text(0, yy, line, fontsize=8); yy -= 0.035
        yy -= 0.03
    guardar(fig, 'D09_parcela_capacidad')


def D10_cuerpos_medidas():
    fig = hoja(A3, 'D10 · Lo que cada cuerpo exige de la superficie', 'largo y ancho para tumbarse (estatura + 0,25; anchura + 0,30) y para dos cuerpos; el colchón de 1,25 × 2,00 del proyecto y la superficie de 3,45 × 4,35; altura de canto para sentarse y levantarse')
    ax = fig.add_axes([0.06, 0.1, 0.5, 0.8]); ax.set_aspect('equal')
    ax.add_patch(Rectangle((0, 0), 2.0, 1.25, fill=False, ec='#D81B8A', lw=1.5)); ax.text(0.05, 1.3, 'colchón 2,00 × 1,25', fontsize=8, color='#D81B8A')
    ax.add_patch(Rectangle((0, 0), 4.35, 3.45, fill=False, ec='#F4A6C6', lw=1.5)); ax.text(0.05, 3.5, 'superficie 4,35 × 3,45', fontsize=8, color='#D81B8A')
    for c in CATALOGO:
        ax.scatter(c.largo_tumbada, c.ancho_tumbada, s=60, color='#1F7A8C', zorder=3)
        ax.scatter(c.largo_tumbada, c.ancho_dos, s=60, color='#F26A1B', zorder=3, marker='s')
        ax.text(c.largo_tumbada + 0.03, c.ancho_tumbada + 0.03, c.id, fontsize=6, color='#1F7A8C')
    ax.scatter([], [], s=60, color='#1F7A8C', label='una tumbada: largo × ancho'); ax.scatter([], [], s=60, color='#F26A1B', marker='s', label='dos cuerpos: largo × ancho')
    ax.legend(fontsize=8, frameon=False, loc='lower right'); ax.set_xlim(0, 4.6); ax.set_ylim(0, 3.8); ax.set_xlabel('m', fontsize=8); ax.set_ylabel('m', fontsize=8); ax.tick_params(labelsize=8)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax2 = fig.add_axes([0.62, 0.1, 0.35, 0.8])
    for i, c in enumerate(CATALOGO):
        lo, hi = c.canto_sentarse
        ax2.plot([lo, hi], [i, i], color='#7B2CBF', lw=4, solid_capstyle='butt')
        ax2.text(hi + 0.01, i, f'{c.id} {c.nombre}', va='center', fontsize=7.5)
    ax2.axvline(0.45, color='#2B2B2B', lw=1); ax2.text(0.452, len(CATALOGO) - 0.5, 'canto bajo 0,45', fontsize=8)
    ax2.axvline(0.72, color='#2B2B2B', lw=1, ls='--'); ax2.text(0.722, len(CATALOGO) - 0.5, 'canto alto 0,72', fontsize=8)
    ax2.axvline(0.12, color='#BBBBBB', lw=1); ax2.text(0.122, len(CATALOGO) - 0.5, 'colchón en el suelo 0,12 (H5)', fontsize=8, color='#777')
    ax2.set_xlim(0.0, 0.95); ax2.set_ylim(-1, len(CATALOGO) + 0.5); ax2.set_yticks([]); ax2.set_xlabel('altura de asiento cómoda (m) · 0,26 × estatura; con dolor o silla, ≥ 0,48', fontsize=8); ax2.tick_params(labelsize=8)
    for s in ('top', 'right', 'left'):
        ax2.spines[s].set_visible(False)
    guardar(fig, 'D10_cuerpos_medidas')


if __name__ == '__main__':
    for f in [D01_reloj, D02_lo_que_mide, D03_membranas, D04_tamanos, D05_sol, D06_turnos, D07_lo_comun, D08_cuerpos_unidades, D09_parcela_capacidad, D10_cuerpos_medidas]:
        try:
            f()
        except Exception as e:
            import traceback; traceback.print_exc()
