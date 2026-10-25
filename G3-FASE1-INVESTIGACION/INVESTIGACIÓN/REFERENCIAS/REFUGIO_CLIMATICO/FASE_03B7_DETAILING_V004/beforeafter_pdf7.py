# -*- coding: utf-8 -*-
"""03B7_V003_V004_BEFORE_AFTER.pdf — A: edificio (ECI) · B: metro/Estacion · C: zooms de detalle."""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

HERE = os.path.dirname(os.path.abspath(__file__))
BA = os.path.join(HERE, '_beforeafter')
CT = os.path.join(HERE, '_control')
OUT = os.path.join(HERE, '03B7_V003_V004_BEFORE_AFTER.pdf')

F_T = dict(fontsize=15, fontweight='bold', color='#2b2b2b')
F_C = dict(fontsize=8.2, color='#333')


def cell(ax, path, label):
    ax.imshow(mpimg.imread(path))
    ax.set_title(label, fontsize=9, pad=3)
    ax.axis('off')


with PdfPages(OUT) as pdf:
    # ---------------- PAGINA A ----------------
    fig, axs = plt.subplots(2, 2, figsize=(16.5, 11.7))
    fig.suptitle('A · EL EDIFICIO (El Corte Ingles) — v003 penetraba, v004 reconoce el borde', **F_T)
    cell(axs[0][0], os.path.join(BA, 'A_eci_aerea_v003.png'), 'v003 · aerea — pod y dosel DENTRO de la edificacion (hasta 10.1 m)')
    cell(axs[0][1], os.path.join(BA, 'A_eci_aerea_v004.png'), 'v004 · aerea — portico-galeria contra fachada, depositos exentos, 0 penetraciones')
    cell(axs[1][0], os.path.join(BA, 'A_eci_calle_v003.png'), 'v003 · a pie de calle')
    cell(axs[1][1], os.path.join(BA, 'A_eci_calle_v004.png'), 'v004 · a pie de calle — el arco aplanado ES el portico (tren T-O regenerado)')
    fig.text(0.5, 0.035, 'Medido: v003 = 439 mallas dentro de ECI (dep. max 10.1 m) · v004 = 0 penetraciones en 79 edificios '
             '(invest_urbano + modulo A12 independiente de la auditoria). Eje de cinta a +3.05 m, radio minimo 4.75 m.',
             ha='center', **F_C)
    plt.tight_layout(rect=(0, 0.05, 1, 0.95))
    pdf.savefig(fig); plt.close(fig)

    # ---------------- PAGINA B ----------------
    fig, axs = plt.subplots(2, 2, figsize=(16.5, 11.7))
    fig.suptitle('B · METRO / CERCANIAS — de punto ignorado a ATRIO (abrazo, no exclusion)', **F_T)
    cell(axs[0][0], os.path.join(BA, 'B_est_aerea_v003.png'), 'v003 · aerea — la Estacion como punto: loops y dosel encima (173 elementos)')
    cell(axs[0][1], os.path.join(BA, 'B_est_aerea_v004.png'), 'v004 · aerea — atrio radial en la boca, dosel ABIERTO, belvedere en la cabeza')
    cell(axs[1][0], os.path.join(BA, 'B_est_boca_v003.png'), 'v003 · desde la boca de Cercanias')
    cell(axs[1][1], os.path.join(BA, 'B_est_boca_v004.png'), 'v004 · desde la boca — anillos de pavimento, senaletica, dintel-portal (galibo 4.7)')
    fig.text(0.5, 0.035, 'Figura espacial B: anillos 7/9/11 m + belvedere de anchura variable + media luna de Carmen + aprons en '
             'estancos + ejes declarados re-proyectados fuera del poligono real (densificados, esquinas validadas).',
             ha='center', **F_C)
    plt.tight_layout(rect=(0, 0.05, 1, 0.95))
    pdf.savefig(fig); plt.close(fig)

    # ---------------- PAGINA C ----------------
    fig, axs = plt.subplots(2, 3, figsize=(16.5, 11.7))
    fig.suptitle('C · DETALLE INFORMACIONAL — LOD B/C: si a 50 cm parece falso, no esta terminado', **F_T)
    cell(axs[0][0], os.path.join(CT, 'CTRL_escalera_2m_b.png'), 'Escalera + pods a 2 m: zancas, montantes, costuras, pletinas de pata')
    cell(axs[0][1], os.path.join(CT, 'CTRL_belvedere_2m.png'), 'Belvedere a 2 m: balaustres, fascia, costillas de canopy')
    cell(axs[0][2], os.path.join(CT, 'CTRL_carlos3_10m_b.png'), 'Carlos III v2 a 10 m: grupo ecuestre + molduras + verja')
    cell(axs[1][0], os.path.join(CT, 'CTRL_mastil_pod_2m.png'), 'Mastil a 2 m: abrazadera, bancos con canto y patas, alocasias')
    cell(axs[1][1], os.path.join(CT, 'CTRL_trepadora_2m_b.png'), 'Trepadora v2: helice + follaje adherido (cero esferas)')
    cell(axs[1][2], os.path.join(CT, 'CTRL_escalera_50cm_b.png'), 'A 50 cm: gota con tapa/valvula/pletinas, juntas de pavimento')
    fig.text(0.5, 0.035, 'Medido: +8 500 objetos (7 997 -> 16 500), 19_DETALLE = 3 470 piezas / 149k tris; 1 468 pletinas, 116 juntas, '
             '42 luminarias, 23 sumideros, 21 mechinales, 12 pendolas. Todo por regla (detailing_03b7.py), cero modelado manual.',
             ha='center', **F_C)
    plt.tight_layout(rect=(0, 0.05, 1, 0.95))
    pdf.savefig(fig); plt.close(fig)

print('OK', OUT)
