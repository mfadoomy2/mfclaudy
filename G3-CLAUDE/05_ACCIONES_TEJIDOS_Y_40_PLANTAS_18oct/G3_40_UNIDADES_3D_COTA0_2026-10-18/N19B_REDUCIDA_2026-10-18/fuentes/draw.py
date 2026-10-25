import json, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Polygon as MPoly, Circle, FancyArrow
from matplotlib import font_manager as fm
from shapely.geometry import box, Polygon, LineString, Point
from shapely.ops import unary_union
from shapely import wkt
from shapely.affinity import translate
from geo import *

plt.rcParams['font.family'] = 'Inter'
plt.rcParams['pdf.fonttype'] = 42
MM = 1 / 25.4
A3 = (420 * MM, 297 * MM)

INK = '#111111'; GREY = '#8a8a8a'; LGREY = '#d9d9d9'
ROOM = '#5FE3D0'; FIELD = '#FFB067'; BATH = '#7FA8FF'; CORE = '#FF3B5C'; PLAT = '#FF9AD0'
BACK = '#D9F27A'; GLASS = '#1E6BFF'; SUN = '#FF7A00'; TELA = '#E5007E'

def ax_mm(fig, x, y, w, h, x0, y0, scale):
    ax = fig.add_axes([x / 420, y / 297, w / 420, h / 297])
    ax.set_xlim(x0, x0 + w * scale / 1000); ax.set_ylim(y0, y0 + h * scale / 1000)
    ax.set_aspect('equal'); ax.axis('off')
    return ax

from matplotlib.path import Path
from matplotlib.patches import PathPatch
def _ring(coords, ccw):
    import shapely
    pts = list(coords)
    area = sum(pts[i][0]*pts[i+1][1]-pts[i+1][0]*pts[i][1] for i in range(len(pts)-1))
    if (area > 0) != ccw: pts = pts[::-1]
    return pts
def fill(ax, g, fc, ec='none', lw=0, z=1, alpha=1, hatch=None):
    if g.is_empty: return
    for p in ([g] if g.geom_type == 'Polygon' else [q for q in getattr(g, 'geoms', []) if q.geom_type == 'Polygon']):
        verts, codes = [], []
        for ring, ccw in [(p.exterior.coords, True)] + [(h.coords, False) for h in p.interiors]:
            r = _ring(ring, ccw)
            verts += r; codes += [Path.MOVETO] + [Path.LINETO] * (len(r) - 2) + [Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts, codes), fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha, hatch=hatch))

def line(ax, g, c=INK, lw=0.4, z=5, ls='-'):
    for l in ([g] if g.geom_type == 'LineString' else list(getattr(g, 'geoms', []))):
        xs, ys = zip(*l.coords); ax.plot(xs, ys, c=c, lw=lw, zorder=z, ls=ls, solid_capstyle='butt')

def outline(ax, g, c=INK, lw=0.3, z=6, ls='-'):
    for p in ([g] if g.geom_type == 'Polygon' else [q for q in getattr(g, 'geoms', []) if q.geom_type == 'Polygon']):
        xs, ys = zip(*p.exterior.coords); ax.plot(xs, ys, c=c, lw=lw, zorder=z, ls=ls)

def txt(ax, x, y, s, size=5.5, c=INK, ha='center', va='center', w='normal', rot=0, z=10):
    ax.text(x, y, s, fontsize=size, color=c, ha=ha, va=va, fontweight=w, rotation=rot, zorder=z)

def dim(ax, a, b, off, label=None, size=5, horiz=True, c='#444'):
    (x1, y1), (x2, y2) = a, b
    if horiz:
        y = y1 + off; ax.plot([x1, x2], [y, y], c=c, lw=0.25, zorder=8)
        for x in (x1, x2):
            ax.plot([x, x], [y1 + (0.15 if off > 0 else -0.15), y + (0.12 if off > 0 else -0.12)], c=c, lw=0.2, zorder=8)
            ax.plot([x - 0.07, x + 0.07], [y - 0.07, y + 0.07], c=c, lw=0.6, zorder=8)
        lab = f'{abs(x2 - x1):.2f}'.replace('.', ',') if label is None else label
        if lab: txt(ax, (x1 + x2) / 2, y + (0.12 if off > 0 else -0.14), lab, size, c, va='bottom' if off > 0 else 'top')
    else:
        x = x1 + off; ax.plot([x, x], [y1, y2], c=c, lw=0.25, zorder=8)
        for y in (y1, y2):
            ax.plot([x1 + (0.15 if off > 0 else -0.15), x + (0.12 if off > 0 else -0.12)], [y, y], c=c, lw=0.2, zorder=8)
            ax.plot([x - 0.07, x + 0.07], [y - 0.07, y + 0.07], c=c, lw=0.6, zorder=8)
        lab = f'{abs(y2 - y1):.2f}'.replace('.', ',') if label is None else label
        if lab: txt(ax, x + (0.20 if off > 0 else -0.20), (y1 + y2) / 2, lab, size, c, ha='center', rot=90)

def fmt(v, d=1):
    s = f'{v:,.{d}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')

def draw_cluster(ax, cl, detail=True):
    walls, doorcuts = walls_of(cl)
    wcut = unary_union([w.buffer(0.35, cap_style=2) for w in cl['windows']])
    fill(ax, cl['field'], FIELD, z=1)
    for k, r in cl['rooms'].items():
        fill(ax, r['rect'], ROOM, z=1)
    for k, b in cl['baths'].items():
        fill(ax, b['rect'], BATH, z=1)
    solid = walls.difference(wcut)
    fill(ax, solid, INK, z=4)
    # ventanas: dos caras finas + vidrio
    for w in cl['windows']:
        cut = w.buffer(0.35, cap_style=2).intersection(cl['footprint']).difference(cl['interior'])
        if detail:
            outline(ax, cut, INK, 0.25, 5)
            (x1, y1), (x2, y2) = w.coords
            nx, ny = -(y2 - y1), (x2 - x1); L = math.hypot(nx, ny); nx, ny = nx / L * 0.15, ny / L * 0.15
            cx, cy = cl['footprint'].centroid.coords[0]
            if ((x1 + x2) / 2 - cx) * nx + ((y1 + y2) / 2 - cy) * ny < 0: nx, ny = -nx, -ny
            ax.plot([x1 + nx, x2 + nx], [y1 + ny, y2 + ny], c=GLASS, lw=0.9, zorder=6, solid_capstyle='butt')
        else:
            line(ax, w, GLASS, 0.8, 6)
    if not detail:
        return
    # puertas correderas: hoja paralela al muro
    def slide(dl, side_pt):
        (x1, y1), (x2, y2) = dl.coords
        nx, ny = -(y2 - y1), (x2 - x1); L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
        if (side_pt[0] - x1) * nx + (side_pt[1] - y1) * ny < 0: nx, ny = -nx, -ny
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        o = 0.08
        ax.plot([x1 + nx * o - ux * 0.05, x2 + nx * o + ux * 0.05 - ux * 0.0], [y1 + ny * o - uy * 0.05, y2 + ny * o + uy * 0.05],
                c=INK, lw=1.1, zorder=7, solid_capstyle='butt')
    for r in cl['rooms'].values():
        slide(r['door'], r['rect'].centroid.coords[0])
    for b in cl['baths'].values():
        slide(b['door'], b['rect'].centroid.coords[0])
    slide(cl['entry'], cl['field'].centroid.coords[0])
    # mobiliario
    for k, r in cl['rooms'].items():
        fill(ax, r['ward'], '#2BB3A0', INK, 0.25, z=3)
        fill(ax, r['bed'], 'white', INK, 0.3, z=3); fill(ax, r['pillow'], 'white', INK, 0.2, z=3.1)
        fill(ax, r['desk'], 'white', INK, 0.3, z=3); fill(ax, r['chair'], 'white', INK, 0.25, z=3)
        outline(ax, r['free'], '#0B6E62', 0.25, 3.2, ls=(0, (2, 2)))
        c = r['rect'].centroid
        lx, ly = (c.x, c.y)
        # rótulo en la zona libre
        f = r['free'].centroid
        txt(ax, f.x, f.y + 0.12, k, 6.5, INK, w='medium'); txt(ax, f.x, f.y - 0.18, f'{fmt(r["rect"].area,2)} m²', 4.8, '#0B4F46')
    for k, b in cl['baths'].items():
        fill(ax, b['shower'], 'white', INK, 0.25, z=3)
        x0, y0, x1, y1 = b['shower'].bounds; ax.plot([x0, x1], [y0, y1], c=INK, lw=0.15, zorder=3.1); ax.plot([x0, x1], [y1, y0], c=INK, lw=0.15, zorder=3.1)
        fill(ax, b['wc'], 'white', INK, 0.25, z=3)
        fill(ax, b['lav'], 'white', INK, 0.25, z=3)
        c = b['rect'].centroid; txt(ax, c.x, c.y + 0.55, k, 5.5, INK, w='medium'); txt(ax, c.x, c.y + 0.3, f'{fmt(b["rect"].area,2)} m²', 4.5, '#1B3E8F')
    f = cl['furn']
    fill(ax, f['counter'], 'white', INK, 0.3, z=3); fill(ax, f['fridge'], 'white', INK, 0.3, z=3)
    hx0, hy0, hx1, hy1 = f['hob'].bounds
    for dx in (0.15, 0.45):
        for dy in (0.12, 0.32):
            fill(ax, Point(hx0 + dx, hy0 + dy).buffer(0.08), 'white', INK, 0.2, z=3.2)
    fill(ax, f['sink'], 'white', INK, 0.25, z=3.2)
    fill(ax, f['table'], 'white', INK, 0.3, z=3)
    for s in f['stools']: fill(ax, s, 'white', INK, 0.25, z=3)
    fill(ax, f['sofa'], 'white', INK, 0.3, z=3); fill(ax, f['sofa_back'], 'white', INK, 0.25, z=3.1)
    fill(ax, f['low'], 'white', INK, 0.25, z=3)
    fill(ax, f['coats'], 'white', INK, 0.3, z=3)
    fill(ax, f['worktop'], 'white', INK, 0.3, z=3)
    for s in cl['shaft']:
        fill(ax, s, 'white', INK, 0.25, z=3); x0, y0, x1, y1 = s.bounds; ax.plot([x0, x1], [y0, y1], c=INK, lw=0.2, zorder=3.1)

# =================================================================== LÁMINA 1 · racimo 1:50
def lamina1(pdf, metr):
    fig = plt.figure(figsize=A3); fig.patch.set_facecolor('white')
    cl = cluster_local()
    ax = ax_mm(fig, 22, 20, 262, 262, -1.25, -1.15, 50)
    draw_cluster(ax, cl, True)
    # rótulos de usos comunes
    txt(ax, 2.0, 4.4, 'estar', 6.5, INK); txt(ax, 5.3, 1.75, 'cocina · comer', 6.5, INK)
    txt(ax, 8.5, 5.25, 'mesa de trabajo', 5, INK); txt(ax, 9.9, 6.1, 'entrada', 6, INK, ha='left')
    txt(ax, 10.5, 2.95, 'armario\ncomún', 4.5, INK)
    txt(ax, 5.25, 5.25, 'suelo común  ' + fmt(cl['field'].area, 1) + ' m²', 5.2, '#7A3A00')
    # cotas
    xs = [0, 0.30, 3.733, 3.833, 7.267, 7.367, 10.80, 11.10]
    for a, b in zip(xs[:-1], xs[1:]):
        dim(ax, (a, 10.8), (b, 10.8), 0.45, f'{b - a:.2f}'.replace('.', ',') if b - a > 0.2 else '', 4.6)
    dim(ax, (0, 10.8), (11.10, 10.8), 0.95, '11,10', 5.5)
    ys = [0, 0.30, 3.80, 3.90, 6.90, 7.00, 10.50, 10.80]
    for a, b in zip(ys[:-1], ys[1:]):
        dim(ax, (0, a), (0, b), -0.45, f'{b - a:.2f}'.replace('.', ',') if b - a > 0.2 else '', 4.6, horiz=False)
    dim(ax, (0, 0), (0, 10.80), -0.95, '10,80', 5.5, horiz=False)
    dim(ax, (7.00, 0), (8.85, 0), -0.45, '1,85', 4.6); dim(ax, (8.95, 0), (10.80, 0), -0.45, '1,85', 4.6)
    dim(ax, (3.833, 0), (6.90, 0), -0.45, '3,07', 4.6)
    # orientación
    txt(ax, -1.12, 1.6, 'calle', 5.5, GREY, rot=90)
    txt(ax, 5.55, -1.0, 'medianera sur', 5.5, GREY)
    txt(ax, 11.95, 6.05, 'plataforma', 5.5, GREY, rot=90)
    txt(ax, 11.95, 2.6, 'núcleo', 5.5, GREY, rot=90)
    # norte
    ax.annotate('', xy=(11.85, 10.9), xytext=(11.85, 10.1), arrowprops=dict(arrowstyle='-|>', lw=0.5, color=INK, mutation_scale=6))
    txt(ax, 11.85, 11.15, 'N', 6, INK, w='medium')

    # ---- columna derecha
    X = 298
    fig.text(X / 420, 282 / 297, 'Racimo de cuatro', fontsize=15, fontweight='light', color=INK, va='top')
    fig.text(X / 420, 271 / 297, 'derivado de N19B · planta 1:50 · nivel tipo', fontsize=7, color=GREY, va='top')
    rows = [('4 habitaciones', '4 × 12,02', fmt(48.06, 1)), ('2 baños', '2 × 3,89', fmt(7.77, 1)),
            ('suelo común', 'cocina, comer, estar, paso', fmt(cl['field'].area, 1)),
            ('útil', '', fmt(103.83, 1)), ('construida', '11,10 × 10,80', fmt(119.88, 1)),
            ('por persona', 'útil / construida', '26,0 / 30,0')]
    y = 258
    for i, (a, b, c) in enumerate(rows):
        wgt = 'medium' if a in ('útil', 'construida') else 'normal'
        fig.text(X / 420, y / 297, a, fontsize=7, color=INK, fontweight=wgt, va='baseline')
        fig.text((X + 34) / 420, y / 297, b, fontsize=6, color=GREY, va='baseline')
        fig.text(405 / 420, y / 297, c + (' m²' if i < 5 else ''), fontsize=7, color=INK, fontweight=wgt, ha='right', va='baseline')
        if a == '2 baños' or a == 'construida':
            fig.add_artist(plt.Line2D([X / 420, 405 / 420], [(y - 2.4) / 297] * 2, lw=0.25, color=LGREY))
        y -= 5.2

    # ---- comparación a la misma escala (1:250)
    n = json.load(open('/mnt/user-data/uploads/G3_40_UNIDADES_3D_COTA0_2026-10-18/N19B_REDUCIDA_2026-10-18/datos/N19B_original_contorno.json'))
    of = wkt.loads(n['floor']); orooms = [wkt.loads(r) for r in n['rooms']]; obaths = [wkt.loads(b) for b in n['baths']]
    ox0, oy0, ox1, oy1 = of.bounds
    sh = lambda g: translate(g, -ox0, -oy0)
    of, orooms, obaths = sh(of), [sh(r) for r in orooms], [sh(b) for b in obaths]
    w_mm = (ox1 - ox0) / 250 * 1000; h_mm = (oy1 - oy0) / 250 * 1000
    axc = ax_mm(fig, X, 128, 107, 92, -0.5, -0.5, 250)
    fill(axc, of, '#EFEFEF', '#9a9a9a', 0.3, z=1)
    for r in orooms: fill(axc, r, '#DADADA', '#9a9a9a', 0.25, z=2)
    for b in obaths: fill(axc, b, '#C9C9C9', '#9a9a9a', 0.25, z=2)
    # nuevo racimo superpuesto, alineado con los baños de N19B (núcleo húmedo)
    bx = (obaths[0].bounds[0] + obaths[1].bounds[2]) / 2; by = obaths[0].bounds[1]
    ncl = place(cluster_local(), bx - 8.875, by - 0.30)
    fill(axc, ncl['field'], FIELD, z=3); [fill(axc, r['rect'], ROOM, z=3) for r in ncl['rooms'].values()]
    [fill(axc, b['rect'], BATH, z=3) for b in ncl['baths'].values()]
    fill(axc, walls_of(ncl)[0], INK, z=4)
    axc.set_xlim(-0.5, -0.5 + 107 * 0.25); axc.set_ylim(-0.5, -0.5 + 92 * 0.25)
    fig.text(X / 420, 124 / 297, 'N19B (gris) y racimo (color) a la misma escala, 1:250', fontsize=6, color=GREY, va='top')
    fig.text(X / 420, 119.5 / 297, f'suelo 273,6 → 103,8 m² útiles · caja 24,8 × 21,4 → 11,1 × 10,8 m', fontsize=6, color=INK, va='top')

    # ---- recorridos
    y = 106
    fig.text(X / 420, y / 297, 'recorridos medios, m', fontsize=7, color=INK, fontweight='medium', va='baseline')
    fig.text(372 / 420, y / 297, 'N19B', fontsize=6, color=GREY, ha='right', va='baseline')
    fig.text(405 / 420, y / 297, 'racimo', fontsize=6, color=GREY, ha='right', va='baseline')
    y -= 5
    for a, o, nv in [('habitación ↔ habitación', '8,6', metr['hab_hab']), ('habitación → baño', '5,9', metr['hab_bano']),
                     ('habitación → cocina', '10,5', metr['hab_cocina']), ('entrada → habitación', '12,5', metr['entrada_hab'])]:
        fig.text(X / 420, y / 297, a, fontsize=6.5, color=INK, va='baseline')
        fig.text(372 / 420, y / 297, o, fontsize=6.5, color=GREY, ha='right', va='baseline')
        fig.text(405 / 420, y / 297, fmt(nv, 1), fontsize=6.5, color=INK, ha='right', va='baseline', fontweight='medium')
        y -= 4.6
    fig.text(X / 420, (y - 0.5) / 297, 'por el suelo libre, esquivando muebles; N19B medido en su modelo 3D', fontsize=5.2, color=GREY, va='baseline')

    # ---- leyenda y notas
    y = 70
    for c, s in [(ROOM, 'habitación · cama 1,25 × 2,00, tablero plegable, armario curvo, Ø 1,50 libre'),
                 (FIELD, 'suelo común continuo de la calle a la plataforma'),
                 (BATH, 'baños contra la medianera, patinillo al núcleo'),
                 (GLASS, 'ventana')]:
        fig.add_artist(plt.Rectangle((X / 420, (y - 1.6) / 297), 4 / 420, 2.6 / 297, fc=c, ec='none'))
        fig.text((X + 6) / 420, y / 297, s, fontsize=5.6, color=INK, va='center')
        y -= 5
    notes = ['Salen al zócalo de PB: cortar/coser (T), reparar (R), bici (G) y secar (D).',
             'Se queda: dormir, trabajar, cocinar, comer, estar y lavarse.',
             'Habitación 3,43 × 3,50 m: el círculo libre de 1,50 m cabe sin tocar muebles.',
             'Suelo común con círculo inscrito de ' + fmt(metr['circulo_comun'], 2) + ' m; ' + fmt(metr['comun_estancia_3m'], 0) + ' m² admiten un círculo de 3 m.',
             'Muro exterior 0,30 · tabique 0,10 · altura libre 2,80 · forjado 0,30.']
    y -= 2
    for s in notes:
        fig.text(X / 420, y / 297, s, fontsize=5.6, color=INK, va='baseline'); y -= 4.2
    pdf.savefig(fig); fig.savefig('lamina1.png', dpi=110); plt.close(fig)

# =================================================================== LÁMINA 2 · planta tipo 1:200 y sección
def lamina2(pdf):
    fig = plt.figure(figsize=A3); fig.patch.set_facecolor('white')
    pt = planta_tipo()
    # ---- planta
    ax = ax_mm(fig, 14, 168, 262, 116, 9.8, -9.6, 200)
    fill(ax, PARCELA, 'white', 'none', 0, z=0)
    fill(ax, pt['back'], BACK, z=0.5)
    fill(ax, pt['plat'], PLAT, z=0.5)
    outline(ax, PARCELA, INK, 0.45, 6)
    # retranqueo de 2 m de vistas rectas al lindero norte
    setback = LINDERO_N.buffer(2.0, cap_style=2, single_sided=False).boundary.intersection(PARCELA.buffer(-0.01))
    line(ax, setback, GREY, 0.3, 2, ls=(0, (1.5, 1.5)))
    for k in ('c1', 'c2'):
        draw_cluster(ax, pt[k], False)
    fill(ax, pt['core'], CORE, z=2)
    fill(ax, pt['core'].difference(pt['core_in']), INK, z=4)
    for t in pt['treads']: line(ax, t, 'white', 0.3, 5)
    outline(ax, pt['lift'], 'white', 0.4, 5)
    ax.plot([pt['cabin'].bounds[0], pt['cabin'].bounds[2]], [pt['cabin'].bounds[1], pt['cabin'].bounds[3]], c='white', lw=0.3, zorder=5)
    ax.plot([pt['cabin'].bounds[0], pt['cabin'].bounds[2]], [pt['cabin'].bounds[3], pt['cabin'].bounds[1]], c='white', lw=0.3, zorder=5)
    # rótulos
    for k, lab in (('c1', 'racimo C1'), ('c2', 'racimo C2 · espejo')):
        c = pt[k]['field'].centroid; txt(ax, c.x, c.y + 0.1, lab, 6, INK, w='medium')
    for k in ('c1', 'c2'):
        for rk, r in pt[k]['rooms'].items():
            c = r['rect'].centroid; txt(ax, c.x, c.y, rk, 5, INK)
    txt(ax, XCORE + CORE_W / 2, YS + CORE_D + 4.0, 'plataforma\ncomún\nabierta', 5.5, '#7A0044')
    c = pt['back'].centroid; txt(ax, c.x + 2, c.y, 'terrazas comunes / patio-huerto en PB', 5.5, '#4A5A00')
    txt(ax, 11.2, 0, 'Ribera de Curtidores', 6, GREY, rot=94.6)
    txt(ax, 53.5, -7.3, 'medianera sur', 5.5, GREY, rot=4.6)
    txt(ax, 34.5, 6.7, 'retranqueo de vistas 2 m', 5, GREY, rot=-21)
    # línea de sección
    ys_ = -3.0
    ax.plot([10.6, 12.6], [ys_, ys_], c=INK, lw=0.6, zorder=7); ax.plot([42.2, 45.5], [ys_, ys_], c=INK, lw=0.6, zorder=7)
    for xx in (10.6, 45.5):
        ax.annotate('', xy=(xx, ys_ - 1.0), xytext=(xx, ys_), arrowprops=dict(arrowstyle='-|>', lw=0.5, color=INK, mutation_scale=5))
    txt(ax, 10.6, ys_ + 0.6, 'S', 5.5, INK, w='medium')
    ax.annotate('', xy=(60.0, 12.6), xytext=(60.0, 10.6), arrowprops=dict(arrowstyle='-|>', lw=0.5, color=INK, mutation_scale=6))
    txt(ax, 60.0, 13.2, 'N', 6, INK, w='medium')
    # cotas generales
    dim(ax, (XC1, YS), (XCORE, YS), -0.9, '11,10', 5); dim(ax, (XCORE, YS), (XC2, YS), -0.9, '5,20', 5)
    dim(ax, (XC2, YS), (XC2 + W, YS), -0.9, '11,10', 5)
    fig.text(14 / 420, 165 / 297, 'planta tipo, niveles +8,00 a +20,40 · 1:200', fontsize=6.5, color=GREY, va='top')

    # ---- sección S, mirando al sur
    axs = ax_mm(fig, 14, 12, 262, 146, 9.8, -1.6, 200)
    zb = [0.0] + NIVELES
    # medianera sur al fondo
    axs.add_patch(plt.Rectangle((13.3, 0), 48.2, 22.0, fc='#F2F2F2', ec='none', zorder=0))
    txt(axs, 60.9, 20.9, 'medianera sur al fondo\nmedia +22,0 · máx. +28,2', 5, GREY, ha='right', va='top')
    # sol de invierno (diagnóstico de luz del 12-10)
    for zz, s in ((16.0, '+16 · por debajo, casi sin sol el 21-dic'), (22.0, '+22 · 2 h de sol el 21-dic en el 66 % de la parcela')):
        axs.plot([10.2, 61.2], [zz, zz], c=SUN, lw=0.45, ls=(0, (4, 2)), zorder=1)
        txt(axs, 61.2, zz + 0.35, s, 5, SUN, ha='right', va='bottom')
    # terreno
    axs.plot([9.8, 62], [0, 0], c=INK, lw=0.7, zorder=6)
    fill(axs, box(9.8, -1.2, 62, 0), '#E9E9E9', z=0.4)
    # zócalo
    for x0 in (XC1, XC2):
        fill(axs, box(x0, 0, x0 + W, ZOCALO_H - 0.30), '#FFE7A8', z=1)
        for xw in (x0, x0 + W - 0.30):
            fill(axs, box(xw, 0, xw + 0.30, ZOCALO_H - 0.30), INK, z=4)
        txt(axs, x0 + W / 2, 2.0, 'zócalo social (indicativo)', 5.2, '#6B5200')
    fill(axs, box(XC1, ZOCALO_H - 0.30, XC2 + W, ZOCALO_H), INK, z=4)
    txt(axs, XCORE + CORE_W + 3, ZOCALO_H + 1.6, 'plaza alta abierta', 5.2, GREY)
    # soportes (vistos)
    for x0 in (XC1, XC2):
        for xx in (x0 + 0.2, x0 + W / 2, x0 + W - 0.2):
            fill(axs, box(xx - 0.15, ZOCALO_H, xx + 0.15, NIVELES[0] - 0.30), '#B9B9B9', z=1)
    # racimos
    for i, z in enumerate(NIVELES):
        for x0 in (XC1, XC2):
            fill(axs, box(x0, z, x0 + W, z + 2.80), FIELD, z=1)
            fill(axs, box(x0, z - 0.30, x0 + W, z), INK, z=4)
            # fachadas cortadas: ventana del estar en el lado de la calle (C1) o al fondo (C2), muro ciego al núcleo
            win_side = x0 if x0 == XC1 else x0 + W - 0.30
            blind = x0 + W - 0.30 if x0 == XC1 else x0
            fill(axs, box(blind, z, blind + 0.30, z + 2.80), INK, z=4)
            fill(axs, box(win_side, z, win_side + 0.30, z + 0.60), INK, z=4)
            fill(axs, box(win_side, z + 2.40, win_side + 0.30, z + 2.80), INK, z=4)
            axs.plot([win_side + 0.15] * 2, [z + 0.60, z + 2.40], c=GLASS, lw=0.8, zorder=5)
            # al fondo (vistos): baños y cocina contra la medianera
            bx0 = x0 + (7.00 if x0 == XC1 else W - 10.80)
            fill(axs, box(bx0, z, bx0 + 3.80, z + 2.80), BATH, z=1.5, alpha=0.9)
            hx0 = x0 + (0.30 if x0 == XC1 else W - 3.833)
            fill(axs, box(hx0, z, hx0 + 3.533, z + 2.80), 'white', INK, 0.25, z=1.5)
            dx0 = x0 + (2.633 if x0 == XC1 else W - 3.433)
            fill(axs, box(dx0, z, dx0 + 0.80, z + 2.10), ROOM, INK, 0.25, z=1.6)
            kx0 = x0 + (3.833 if x0 == XC1 else W - 6.90)
            fill(axs, box(kx0, z, kx0 + 3.07, z + 0.90), 'white', INK, 0.25, z=1.6)
        txt(axs, XC1 - 0.6, z + 0.45, f'+{fmt(z, 2)}', 5.2, INK, ha='right')
    fill(axs, box(XC1, CUBIERTA - 0.30, XC1 + W, CUBIERTA), INK, z=4)
    fill(axs, box(XC2, CUBIERTA - 0.30, XC2 + W, CUBIERTA), INK, z=4)
    for x0 in (XC1, XC2):
        for xx in (x0, x0 + W - 0.10):
            fill(axs, box(xx, CUBIERTA, xx + 0.10, CUBIERTA + 1.10), INK, z=4)
    txt(axs, XC1 - 0.6, CUBIERTA + 0.4, f'+{fmt(CUBIERTA, 2)}', 5.2, INK, ha='right')
    txt(axs, XC1 - 0.6, ZOCALO_H - 0.1, '+4,50', 5.2, INK, ha='right')
    txt(axs, XC1 - 0.6, 0.3, '±0,00 = 622,90', 5.2, INK, ha='right')
    # núcleo-mástil
    TOP = CUBIERTA + 2.60
    fill(axs, box(XCORE, 0, XCORE + CORE_W, TOP), CORE, z=1)
    fill(axs, box(XCORE, 0, XCORE + 0.30, TOP), INK, z=4); fill(axs, box(XCORE + CORE_W - 0.30, 0, XCORE + CORE_W, TOP), INK, z=4)
    fill(axs, box(XCORE + 2.80, 0, XCORE + 2.95, TOP), INK, z=4)
    fill(axs, box(XCORE, TOP - 0.30, XCORE + CORE_W, TOP), INK, z=4)
    lv = [0.0] + NIVELES + [CUBIERTA]
    for a, b in zip(lv[:-1], lv[1:]):
        mid = (a + b) / 2
        axs.plot([XCORE + 0.35, XCORE + 2.75], [a, mid], c='white', lw=0.6, zorder=3)
        axs.plot([XCORE + 2.75, XCORE + 0.35], [mid, b], c='white', lw=0.6, zorder=3)
        fill(axs, box(XCORE + 0.30, b - 0.20, XCORE + 2.80, b), 'white', z=3)
    txt(axs, XCORE + 4.05, TOP / 2, 'ascensor', 5, 'white', rot=90)
    txt(axs, XCORE + CORE_W / 2, TOP + 0.6, 'núcleo-mástil', 5.5, '#B0002A', w='medium')
    # tela sobre la cubierta común
    import numpy as np
    for xa, xb in ((XCORE, XC1), (XCORE + CORE_W, XC2 + W)):
        t = np.linspace(0, 1, 40); xs_ = xa + (xb - xa) * t
        zs_ = TOP - 0.05 + (CUBIERTA + 1.10 - TOP + 0.05) * t - 1.4 * np.sin(np.pi * t)
        axs.plot(xs_, zs_, c=TELA, lw=0.7, zorder=5)
    txt(axs, (XC1 + XCORE) / 2, CUBIERTA + 2.4, 'tela de la cubierta común', 5, TELA)
    fig.text(14 / 420, 9 / 297, 'sección S por el suelo común de los racimos, mirando al sur · 1:200', fontsize=6.5, color=GREY, va='top')

    # ---- columna derecha
    X = 290
    fig.text(X / 420, 282 / 297, 'Diez racimos en la parcela', fontsize=15, fontweight='light', color=INK, va='top')
    fig.text(X / 420, 271 / 297, 'dos por planta, uno a cada lado del núcleo', fontsize=7, color=GREY, va='top')
    y = 258
    fig.text(X / 420, y / 297, 'niveles', fontsize=7, fontweight='medium', color=INK, va='baseline'); y -= 5
    for a, b in [('±0,00', 'zócalo social y pasaje al patio (indicativo)'), ('+4,50', 'plaza alta abierta, sólo estructura'),
                 ('+8,00 a +20,40', '5 plantas × 2 racimos = 40 personas'), ('+23,50', 'cubierta común bajo la tela'),
                 ('cada 3,10 m', 'forjado 0,30 · altura libre 2,80')]:
        fig.text(X / 420, y / 297, a, fontsize=6.3, color=INK, va='baseline')
        fig.text((X + 27) / 420, y / 297, b, fontsize=6.3, color=INK, va='baseline'); y -= 4.4
    y -= 3
    fig.text(X / 420, y / 297, 'superficie construida, m²', fontsize=7, fontweight='medium', color=INK, va='baseline'); y -= 5
    sup = [('10 racimos', '10 × 119,9', 1198.8), ('núcleo', '8 niveles × 27,0', 216.3), ('zócalo PB (indicativo)', '2 × 119,9', 239.8)]
    for a, b, c in sup:
        fig.text(X / 420, y / 297, a, fontsize=6.3, color=INK, va='baseline'); fig.text((X + 42) / 420, y / 297, b, fontsize=6, color=GREY, va='baseline')
        fig.text(405 / 420, y / 297, fmt(c, 1), fontsize=6.3, color=INK, ha='right', va='baseline'); y -= 4.4
    fig.add_artist(plt.Line2D([X / 420, 405 / 420], [(y + 2.4) / 297] * 2, lw=0.25, color=LGREY))
    fig.text(X / 420, y / 297, 'total', fontsize=6.5, color=INK, fontweight='medium', va='baseline')
    fig.text((X + 42) / 420, y / 297, 'enunciado ≈ 1.500 (+10 %)', fontsize=6, color=GREY, va='baseline')
    fig.text(405 / 420, y / 297, fmt(1654.9, 1), fontsize=6.5, color=INK, fontweight='medium', ha='right', va='baseline'); y -= 4.4
    fig.text(X / 420, y / 297, 'plataformas abiertas (6 × 63,7) no computadas', fontsize=5.6, color=GREY, va='baseline'); y -= 8

    fig.text(X / 420, y / 297, 'comprobado sobre el modelo', fontsize=7, fontweight='medium', color=INK, va='baseline'); y -= 5
    checks = ['Todo dentro del contorno de Catastro (651 m²).',
              'Cada ventana tiene 2 m libres delante dentro de la parcela o da a la calle',
              '   (art. 582 del Código Civil, vistas rectas).',
              'Puerta del racimo → escalera: 1,9 m (C1) y 4,2 m (C2); máx. 25 m (DB SI 3).',
              'Altura de evacuación +20,40: escalera protegida (DB SI 3, entre 14 y 28 m).',
              'Escalera: tramos 1,05 m, huella 0,28, contrahuella 0,172, mesetas 1,15',
              '   (DB SUA 1: ≥ 1,00 · ≥ 0,28 · ≤ 0,185 · ≥ 1,00).',
              'Barandilla de 1,10 m en plataformas (DB SUA 1, desnivel > 6 m).',
              'Ascensor con cabina 1,10 × 1,40 junto a la escalera.']
    for s in checks:
        fig.text(X / 420, y / 297, s, fontsize=5.7, color=INK, va='baseline'); y -= 4.1
    y -= 3
    fig.text(X / 420, y / 297, 'por decidir', fontsize=7, fontweight='medium', color=INK, va='baseline'); y -= 5
    for s in ['Altura máxima del Centro Histórico (cubierta +23,50, medianera +22 / +28,2).',
              'Sol: las plantas +8 y +11 quedan bajo +16; la luz les llega de norte, calle y fondo.',
              'Estructura: apoyar en el zócalo o colgar los racimos del núcleo-mástil.',
              'Figura legal: vivienda compartida de 4 (2 baños) o residencia compartida',
              '   (dormitorio con baño en cada unidad).']:
        fig.text(X / 420, y / 297, s, fontsize=5.7, color=INK, va='baseline'); y -= 4.1
    y -= 3
    for c, s in [(ROOM, 'habitación'), (FIELD, 'suelo común'), (BATH, 'baños'), (CORE, 'núcleo-mástil'), (PLAT, 'plataforma'), (BACK, 'fondo común'), (SUN, 'umbral de sol')]:
        fig.add_artist(plt.Rectangle((X / 420, (y - 1.4) / 297), 3.5 / 420, 2.4 / 297, fc=c, ec='none'))
        fig.text((X + 5.5) / 420, y / 297, s, fontsize=5.5, color=INK, va='center'); y -= 3.8
    pdf.savefig(fig); fig.savefig('lamina2.png', dpi=110); plt.close(fig)

if __name__ == '__main__':
    metr = json.load(open('metr_racimo.json'))
    with PdfPages('G3_N19B_REDUCIDA_A3.pdf') as pdf:
        lamina1(pdf, metr); lamina2(pdf)
    print('ok')
