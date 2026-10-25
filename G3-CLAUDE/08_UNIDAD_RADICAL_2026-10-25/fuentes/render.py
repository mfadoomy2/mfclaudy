"""Render axonométrico y planos en blanco y negro con matplotlib (sin OpenGL).

Fondo blanco, colores vivos, títulos discretos. Las vistas son de estudio: no sustituyen a Rhino.
"""
import math

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
from matplotlib import font_manager
import trimesh
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

import os
FUENTE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'IbarraRealNova-Italic-400.ttf')
try:
    font_manager.fontManager.addfont(FUENTE)
    FAMILIA = font_manager.FontProperties(fname=FUENTE).get_name()
except Exception:
    FAMILIA = 'DejaVu Serif'
plt.rcParams['font.family'] = FAMILIA
plt.rcParams['svg.fonttype'] = 'none'


def base_vista(az=225, el=30):
    """Ejes de proyección ortográfica: cámara en azimut az (grados desde +x hacia +y) y elevación el."""
    a, e = math.radians(az), math.radians(el)
    f = -np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])  # mirada
    r = np.array([-math.sin(a), math.cos(a), 0.0])
    u = np.cross(r, f)
    if u[2] < 0:
        u = -u
    return r, u, f


def _hex(c):
    c = c.lstrip('#')
    return np.array([int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def axon(piezas, salida, az=225, el=30, ancho_cm=24, alto_cm=18, titulo=None, subtitulo=None,
         luz=(-0.4, -0.6, 1.0), dpi=160, lineas=True, recorte=None, escala_fija=None, subdividir=0.6):
    r, u, f = base_vista(az, el)
    luz = np.array(luz) / np.linalg.norm(luz)
    tris, cols, deps, edges = [], [], [], []
    for p in piezas:
        m = p.malla
        if m is None or len(m.faces) == 0:
            continue
        if subdividir and len(m.faces) < 20000:
            try:
                m = m.subdivide_to_size(max_edge=subdividir, max_iter=4)
            except Exception:
                pass
        v = m.vertices
        P = np.column_stack([v @ r, v @ u])
        D = v @ f
        F = m.faces
        n = m.face_normals
        shade = 0.55 + 0.45 * np.clip(n @ luz, 0, 1)
        base = _hex(p.color)
        c = np.clip(base[None, :] * shade[:, None], 0, 1)
        a = np.full((len(F), 1), p.alpha)
        tris.append(P[F])
        cols.append(np.hstack([c, a]))
        deps.append(D[F].mean(axis=1))
        if lineas and p.alpha >= 0.9:
            # aristas de contorno sobre la malla original: ángulo fuerte entre caras
            try:
                mo = p.malla
                vo = mo.vertices
                Po = np.column_stack([vo @ r, vo @ u])
                ang = mo.face_adjacency_angles
                ed = mo.face_adjacency_edges[ang > math.radians(35)]
                edges.append((Po[ed], None))
            except Exception:
                pass
    if not tris:
        return
    T = np.concatenate(tris)
    C = np.concatenate(cols)
    Dm = np.concatenate(deps)
    orden = np.argsort(-Dm)  # lejos primero
    fig = plt.figure(figsize=(ancho_cm / 2.54, alto_cm / 2.54), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    pc = PolyCollection(T[orden], facecolors=C[orden], edgecolors='none', linewidths=0)
    ax.add_collection(pc)
    if edges:
        E = np.concatenate([e for e, _ in edges])
        ax.add_collection(LineCollection(E, colors='#222222', linewidths=0.35, alpha=0.9))
    allp = T.reshape(-1, 2)
    if recorte is not None:
        x0, x1, y0, y1 = recorte
    else:
        x0, x1 = allp[:, 0].min(), allp[:, 0].max()
        y0, y1 = allp[:, 1].min(), allp[:, 1].max()
    mx, my = (x1 - x0) * 0.06, (y1 - y0) * 0.06
    ax.set_xlim(x0 - mx, x1 + mx)
    ax.set_ylim(y0 - my, y1 + my)
    ax.set_aspect('equal')
    ax.axis('off')
    if titulo:
        fig.text(0.02, 0.965, titulo, fontsize=11, color='#222222', ha='left', va='top')
    if subtitulo:
        fig.text(0.02, 0.925, subtitulo, fontsize=7.5, color='#555555', ha='left', va='top')
    fig.savefig(salida, facecolor='white')
    plt.close(fig)


def cortar(piezas, z, arriba=False):
    """Quita lo que está por encima (o por debajo) de z para vistas seccionadas."""
    out = []
    for p in piezas:
        try:
            m = trimesh.intersections.slice_mesh_plane(p.malla, plane_normal=[0, 0, -1 if not arriba else 1],
                                                       plane_origin=[0, 0, z], cap=True)
            if m is not None and len(m.faces):
                q = p.copia()
                q.malla = m
                out.append(q)
        except Exception:
            out.append(p)
    return out


def cortar_plano(piezas, origen, normal):
    out = []
    for p in piezas:
        try:
            m = trimesh.intersections.slice_mesh_plane(p.malla, plane_normal=normal, plane_origin=origen, cap=True)
            if m is not None and len(m.faces):
                q = p.copia()
                q.malla = m
                out.append(q)
        except Exception:
            pass
    return out


# ---------------------------------------------------------------------------
# Planos en blanco y negro (corte negro 0,35 · carpintería 0,18 · proyección 0,13 · discontinua 0,10)

MM = {'corte': 0.35, 'carp': 0.18, 'proy': 0.13, 'disc': 0.10}


def _lw(mm, escala_mm_por_m, dpi_pts=72):
    # ancho de línea en puntos: mm → pt (1 mm = 2.835 pt)
    return mm * 2.835


def seccion_z(malla, z):
    s = malla.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if s is None:
        return None
    try:
        p2, _ = s.to_planar()
        polys = [Polygon(np.asarray(pl)) for pl in p2.polygons_full] if hasattr(p2, 'polygons_full') else []
        # to_planar devuelve coordenadas transformadas; usamos la 3D directamente
    except Exception:
        polys = []
    # Preferible: los caminos 3D proyectados a xy
    res = []
    for ent in s.discrete:
        pts = np.asarray(ent)[:, :2]
        if len(pts) >= 3:
            try:
                pg = Polygon(pts)
                if pg.is_valid and pg.area > 1e-6:
                    res.append(pg)
            except Exception:
                pass
    if not res:
        return None
    res.sort(key=lambda g: -g.area)
    out = res[0]
    for g in res[1:]:
        out = out.symmetric_difference(g)
    return out


def proyeccion_xy(malla):
    try:
        return trimesh.path.polygons.projected(malla, normal=[0, 0, 1], ignore_sign=True)
    except Exception:
        return None


def planta_bn(piezas, z_corte, salida, escala=50, titulo=None, nota=None, hoja_cm=(29.7, 21.0),
              proyectar_bajo=True, dpi=200, cotas=None, origen=None, discontinuos=None):
    """Planta cortada a z_corte. Corte en negro; lo que queda por debajo, en línea fina; lo que
    está por encima del corte (discontinuos), a trazos."""
    fig = plt.figure(figsize=(hoja_cm[0] / 2.54, hoja_cm[1] / 2.54), dpi=dpi)
    ax = fig.add_axes([0.04, 0.06, 0.92, 0.86])
    xs, ys = [], []
    # proyección (por debajo del corte)
    for p in piezas:
        m = p.malla
        bb = m.bounds
        if p.capa.endswith('cuerpos') or 'cuerpos' in p.capa:
            pg = proyeccion_xy(m)
            if pg is not None:
                for g in (pg.geoms if hasattr(pg, 'geoms') else [pg]):
                    x, y = g.exterior.xy
                    ax.plot(x, y, color='black', lw=_lw(MM['carp'], escala))
                    xs += list(x); ys += list(y)
            continue
        if bb[0][2] >= z_corte:
            if discontinuos is not None and p.nombre in discontinuos:
                pg = proyeccion_xy(m)
                if pg is not None:
                    for g in (pg.geoms if hasattr(pg, 'geoms') else [pg]):
                        x, y = g.exterior.xy
                        ax.plot(x, y, color='black', lw=_lw(MM['disc'], escala), ls=(0, (3, 2)))
            continue
        cut = seccion_z(m, z_corte) if bb[1][2] > z_corte else None
        if cut is not None:
            for g in (cut.geoms if hasattr(cut, 'geoms') else [cut]):
                x, y = g.exterior.xy
                ax.fill(x, y, color='black', lw=0)
                for inter in g.interiors:
                    xi, yi = inter.xy
                    ax.fill(xi, yi, color='white', lw=0)
                ax.plot(x, y, color='black', lw=_lw(MM['corte'], escala))
                xs += list(x); ys += list(y)
        if proyectar_bajo:
            m2 = m
            if bb[1][2] > z_corte:
                try:
                    m2 = trimesh.intersections.slice_mesh_plane(m, plane_normal=[0, 0, -1], plane_origin=[0, 0, z_corte], cap=True)
                except Exception:
                    m2 = m
            pg = proyeccion_xy(m2) if m2 is not None and len(m2.faces) else None
            if pg is not None:
                lw = _lw(MM['carp'] if p.capa.endswith('cuerpos') or 'mueble' in p.capa else MM['proy'], escala)
                for g in (pg.geoms if hasattr(pg, 'geoms') else [pg]):
                    x, y = g.exterior.xy
                    ax.plot(x, y, color='black', lw=lw)
                    xs += list(x); ys += list(y)
                    for inter in g.interiors:
                        xi, yi = inter.xy
                        ax.plot(xi, yi, color='black', lw=lw)
    if not xs:
        plt.close(fig)
        return
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    # tamaño de dibujo en metros según escala y hoja
    ancho_m = (hoja_cm[0] * 0.92) / 100 * escala
    alto_m = (hoja_cm[1] * 0.86) / 100 * escala
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ax.set_xlim(cx - ancho_m / 2, cx + ancho_m / 2)
    ax.set_ylim(cy - alto_m / 2, cy + alto_m / 2)
    ax.set_aspect('equal')
    ax.axis('off')
    # barra de escala: 1 m, 2 m, 5 m
    bx, by = cx - ancho_m / 2 + 0.5, cy - alto_m / 2 + 0.4
    for i, L in enumerate([0, 1, 2, 3, 4]):
        ax.add_patch(plt.Rectangle((bx + L, by), 1, 0.08, color='black' if i % 2 == 0 else 'white', ec='black', lw=0.5))
    for L in [0, 1, 2, 5]:
        ax.text(bx + L, by + 0.15, f'{L}', fontsize=6, ha='center')
    ax.text(bx + 5.3, by + 0.02, 'm', fontsize=6)
    if titulo:
        fig.text(0.04, 0.955, titulo, fontsize=10, ha='left', va='top')
    if nota:
        fig.text(0.04, 0.925, nota, fontsize=6.5, ha='left', va='top', color='#333333')
    fig.text(0.96, 0.03, f'E 1:{escala} · corte a +{z_corte:.2f} m', fontsize=6.5, ha='right')
    fig.savefig(salida, facecolor='white')
    plt.close(fig)


def seccion_bn(piezas, salida, origen, normal, escala=50, titulo=None, nota=None, hoja_cm=(29.7, 21.0), dpi=200,
               ver_hacia=None):
    """Sección vertical por un plano. Corte negro; lo que queda detrás, proyectado en fino."""
    normal = np.array(normal, float); normal /= np.linalg.norm(normal)
    origen = np.array(origen, float)
    # ejes 2D del plano: horizontal h = normal × z, vertical z
    h = np.cross([0, 0, 1], normal); h /= np.linalg.norm(h)
    fig = plt.figure(figsize=(hoja_cm[0] / 2.54, hoja_cm[1] / 2.54), dpi=dpi)
    ax = fig.add_axes([0.04, 0.06, 0.92, 0.86])
    xs, ys = [], []
    for p in piezas:
        m = p.malla
        if 'cuerpos' in p.capa:
            from shapely.geometry import MultiPoint
            v = m.vertices
            P = np.column_stack([(v - origen) @ h, v[:, 2]])
            hull = MultiPoint(P).convex_hull
            if hull.geom_type == 'Polygon':
                x, y = hull.exterior.xy
                ax.plot(x, y, color='black', lw=_lw(MM['carp'], escala))
                xs += list(x); ys += list(y)
            continue
        # corte
        s = m.section(plane_origin=origen, plane_normal=normal)
        if s is not None:
            for ent in s.discrete:
                pts = np.asarray(ent)
                X = (pts - origen) @ h; Y = pts[:, 2]
                if len(pts) >= 3:
                    ax.fill(X, Y, color='black', lw=0)
                    ax.plot(X, Y, color='black', lw=_lw(MM['corte'], escala))
                    xs += list(X); ys += list(Y)
        # lo que queda detrás del plano (lado -normal)
        try:
            m2 = trimesh.intersections.slice_mesh_plane(m, plane_normal=-normal, plane_origin=origen, cap=True)
        except Exception:
            m2 = None
        if m2 is not None and len(m2.faces):
            v = m2.vertices
            P = np.column_stack([(v - origen) @ h, v[:, 2]])
            try:
                ang = m2.face_adjacency_angles
                ed = m2.face_adjacency_edges[ang > math.radians(30)]
                segs = P[ed]
                ax.add_collection(LineCollection(segs, colors='black', linewidths=_lw(MM['proy'], escala)))
                # contorno exterior
                xs += list(P[:, 0]); ys += list(P[:, 1])
            except Exception:
                pass
    if not xs:
        plt.close(fig)
        return
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    ancho_m = (hoja_cm[0] * 0.92) / 100 * escala
    alto_m = (hoja_cm[1] * 0.86) / 100 * escala
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ax.set_xlim(cx - ancho_m / 2, cx + ancho_m / 2)
    ax.set_ylim(cy - alto_m / 2, cy + alto_m / 2)
    ax.set_aspect('equal'); ax.axis('off')
    # línea de suelo
    ax.plot([cx - ancho_m / 2, cx + ancho_m / 2], [0, 0], color='black', lw=_lw(MM['corte'], escala))
    bx, by = cx - ancho_m / 2 + 0.5, cy - alto_m / 2 + 0.4
    for i in range(5):
        ax.add_patch(plt.Rectangle((bx + i, by), 1, 0.08, color='black' if i % 2 == 0 else 'white', ec='black', lw=0.5))
    for L in [0, 1, 2, 5]:
        ax.text(bx + L, by + 0.15, f'{L}', fontsize=6, ha='center')
    if titulo:
        fig.text(0.04, 0.955, titulo, fontsize=10, ha='left', va='top')
    if nota:
        fig.text(0.04, 0.925, nota, fontsize=6.5, ha='left', va='top', color='#333333')
    fig.text(0.96, 0.03, f'E 1:{escala}', fontsize=6.5, ha='right')
    fig.savefig(salida, facecolor='white')
    plt.close(fig)
