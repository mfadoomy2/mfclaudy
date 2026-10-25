# -*- coding: utf-8 -*-
"""GEOMETRIA MAESTRA v004 — FASE 03B.7.
Rama sobre v003 (INTACTA). Cambios de DATOS:
  · urbano_v004: poligonos-guard de edificios reales (la causa raiz de A: ninguna regla los conocia),
    kioscos/estancos, Estacion de Cercanias (edif 106, 20x7 m — v003 la trataba como un punto)
  · retirada del tren T-O de los datos (se regenera en build sobre el arco aplanado contra ECI)
  · arboles del paseo norte re-situados en banda realmente libre
  · figura espacial B: atrio de la Estacion + media luna de Carmen + aprons de estancos + senaletica
  · perfil de anchura del tablero (belvedere sobre la cabeza de la Estacion)
Diff en _v004_diff.json. Las reglas geometricas (recorte de loops, proyeccion de cinta,
EDGE_GUARD) viven en build_all_03b7.py y leen urbano_v004.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, '..', 'FASE_03B6_RESOLUCION'))
m = json.load(open(os.path.join(V3, 'geometria_maestra_v003.json'), encoding='utf-8'))
DIFF = {'base': 'geometria_maestra_v003.json', 'fecha': '2026-08-11', 'cambios': []}


def log(cr, que, detalle=None):
    DIFF['cambios'].append({'causa': cr, 'que': que, 'detalle': detalle})


B = m['contexto']['buildings']

# ---------- URBANO v004: el conocimiento del borde entra en los DATOS ----------
GRANDES = []
KIOS = []                       # 03B.7-C: derivados por REGLA del mismo barrido (74 faltaba en la lista manual)
for i, b in enumerate(B):
    pts = b['pts']
    if len(pts) < 4:
        continue
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    if max(xs) < -115 or min(xs) > 105 or max(ys) < -50 or min(ys) > 80:
        continue
    area = 0.5 * abs(sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1]
                         for k in range(len(pts))))
    if i == 106:
        continue
    if area < 80:
        KIOS.append(i)
        continue
    GRANDES.append(i)

m['urbano_v004'] = {
    'guard_edificios': GRANDES,                      # poligonos duros: NADA del proyecto dentro
    'margen_edificio': {'suelo': 0.8, 'aereo': 0.5, 'loop': 3.25, 'cinta': 2.65},
    'kioscos': KIOS,                                 # estancos/kioscos por regla (area<80 en ambito)
    'margen_kiosco': 1.0,
    'estacion': 106,                                 # Estacion de Cercanias: perimetro REAL
    'margen_estacion': {'suelo': 1.6, 'cinta': 2.65},
    'altura_kiosco': 3.6,                            # sobre esa cota, el aereo puede volar kioscos
    'nota': ('Causa raiz del conflicto A: ni guard ni auditoria conocian los poligonos de edificio. '
             'v004 los incorpora como regla: recorte tangente de loops, proyeccion de cinta al offset '
             'de fachada y EDGE_GUARD para toda familia. ECI (133) genera el portico-galeria; la '
             'Estacion (106) genera el abrazo-balcon.')
}
log('A/B', 'urbano_v004: %d edificios-guard + 3 kioscos + estacion 106' % len(GRANDES))

# ---------- A1b · EJES DECLARADOS vs Estacion REAL (03B7-D V-002) ----------
# El eje montera-espozymina se declaro cuando la Estacion era un PUNTO; el poligono real de la
# cabeza (20x7 m) lo corta. Regla: todo punto de eje dentro de ESTACION+2.0 se proyecta al
# offset de fachada 2.0 del lado de la plaza (el mismo principio del empuje de cinta).
def _dseg(px, py, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    L2 = vx * vx + vy * vy or 1e-9
    t = max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / L2))
    return math.hypot(px - (ax + vx * t), py - (ay + vy * t))


def _reroute_pts():
    est = B[m['urbano_v004']['estacion']]['pts']
    MRG = 2.75                             # 03B7-D it.2: 2.0 dejaba holgura 1.12 contra el zocalo raster
    AX, AY = 47.0, 8.0                     # ancla de plaza al norte de la Estacion
    xs_ = [p[0] for p in est]; ys_ = [p[1] for p in est]
    BB = (min(xs_) - 15, min(ys_) - 15, max(xs_) + 15, max(ys_) + 15)
    nmov = 0
    for c in m['circulacion']['corridors']:
        # it.3: DENSIFICAR a <=2 m cerca de la Estacion — si solo se mueven los vertices, la
        # CUERDA entre dos vertices desviados sigue cortando la esquina del poligono
        pts0 = c['pts']
        dens = [pts0[0]]
        for k in range(1, len(pts0)):
            a, b = dens[-1], pts0[k]
            cerca = (BB[0] < a[0] < BB[2] and BB[1] < a[1] < BB[3]) or (BB[0] < b[0] < BB[2] and BB[1] < b[1] < BB[3])
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            nsub = max(1, int(L / 2.0)) if cerca else 1
            for t in range(1, nsub + 1):
                dens.append([round(a[0] + (b[0] - a[0]) * t / nsub, 2),
                             round(a[1] + (b[1] - a[1]) * t / nsub, 2)])
        c['pts'] = dens
        for p in c['pts']:
            x, y = p[0], p[1]
            dentro = pip(x, y, est)
            dmin, qbest = 1e9, None
            for i in range(len(est)):
                ax, ay = est[i][0], est[i][1]
                bx, by = est[(i + 1) % len(est)][0], est[(i + 1) % len(est)][1]
                vx, vy = bx - ax, by - ay
                L2 = vx * vx + vy * vy or 1e-9
                t = max(0.0, min(1.0, ((x - ax) * vx + (y - ay) * vy) / L2))
                fx, fy = ax + vx * t, ay + vy * t
                d = math.hypot(x - fx, y - fy)
                dmin = min(dmin, d)
                nx, ny = -vy / math.sqrt(L2), vx / math.sqrt(L2)
                for s in (1, -1):
                    qx, qy = fx + nx * s * MRG, fy + ny * s * MRG
                    if pip(qx, qy, est):
                        continue
                    # it.4: en una ESQUINA, estar a MRG de la arista propia no basta — validar TODAS
                    dall = min(_dseg(qx, qy, est[i2][0], est[i2][1],
                                     est[(i2 + 1) % len(est)][0], est[(i2 + 1) % len(est)][1])
                               for i2 in range(len(est)))
                    if dall < MRG - 0.15:
                        continue
                    if qbest is None or (math.hypot(qx - AX, qy - AY) < math.hypot(qbest[0] - AX, qbest[1] - AY)):
                        qbest = (qx, qy)
            if (dentro or dmin < MRG) and qbest is not None:
                p[0], p[1] = round(qbest[0], 2), round(qbest[1], 2)
                nmov += 1
    return nmov


# ---------- A2 · arboles del paseo norte: a banda realmente libre ----------
def pip(x, y, poly):
    n = len(poly)
    d = False
    j = n - 1
    for i in range(n):
        xi, yi = poly[i][0], poly[i][1]
        xj, yj = poly[j][0], poly[j][1]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi):
            d = not d
        j = i
    return d


_nrr = _reroute_pts()
log('A1b', 'ejes declarados: %d puntos re-proyectados fuera de la Estacion+2.0' % _nrr)


def en_edificio(x, y):
    for i in GRANDES + [106, 109, 110, 111]:
        if pip(x, y, B[i]['pts']):
            return i
    return None


def libre_arbol(x, y):
    """fuera de todo edificio/kiosco y con 1.2 m a cualquier fachada (copa aparte, la pone el guard)."""
    if en_edificio(x, y) is not None:
        return False
    for dx, dy in ((1.2, 0), (-1.2, 0), (0, 1.2), (0, -1.2)):
        if en_edificio(x + dx, y + dy) is not None:
            return False
    return True


nt = []
mov = []
for (tx, ty) in m['paisaje']['new_trees']:
    if libre_arbol(tx, ty):
        nt.append((tx, ty))
        continue
    e = en_edificio(tx, ty)
    ok = False
    for dy in [k * 1.5 for k in range(1, 14)]:
        for dx in (0, -2, 2, -4, 4, -6, 6):
            if libre_arbol(tx + dx, ty - dy):
                nt.append((round(tx + dx, 1), round(ty - dy, 1)))
                mov.append({'de': [tx, ty], 'a': list(nt[-1]), 'edificio': e})
                ok = True
                break
        if ok:
            break
    if not ok:
        mov.append({'de': [tx, ty], 'a': None, 'edificio': e})
m['paisaje']['new_trees'] = nt
log('A2', 'arboles nuevos fuera de edificios (busqueda en abanico S/SO)', mov)

# ---------- A1 · tren T-O fuera de los datos: se regenera sobre el arco-portico ----------
caps = m['programa']['capsules']
n_to = sum(1 for c in caps if c.get('id') == 'T-O')
m['programa']['capsules'] = [c for c in caps if c.get('id') != 'T-O']
m['programa']['tren_portico'] = {'id': 'T-O', 'n': max(n_to, 6), 'w': 3.4, 'h': 2.1,
                                 'regla': 'a lo largo del arco de C1-L1 aplanado contra ECI, puertas <=3 seguidas'}
log('A1', 'T-O retirado de datos (%d caps): renace como tren-portico sobre el arco aplanado' % n_to)

# ---------- B · figura espacial: atrio Estacion + Carmen + estancos ----------
est = B[106]['pts']
m['atrio_v004'] = {
    'estacion': {
        'boca': [57.0, -5.4],
        'anillo_pavimento': {'c': [57.0, -5.4], 'r': [7.0, 9.0, 11.0], 'nota': 'bandas radiales de despiece'},
        'belvedere': {'c': [58.5, -0.5], 'ancho_extra': 0.9, 'radio_influencia': 10.0,
                      'nota': 'ensanche del tablero sobre la cabeza este de la Estacion'},
        'senaletica': [[63.5, -3.0], [50.0, 3.0]],
        'zona_espera_libre': [[57.0, -5.4], 9.0]
    },
    'carmen': {
        'boca': [18.5, 25.1],
        'media_luna_bancos': {'c': [18.5, 25.1], 'r': 8.2, 'a0': 200, 'a1': 340},
        'senaletica': [[13.0, 20.0]]
    },
    'aprons_kiosco': [{'edif': 109, 'margen': 3.0}, {'edif': 110, 'margen': 3.0}, {'edif': 111, 'margen': 2.0}],
    'nota': ('B no es un circulo de exclusion: la cinta pasa en concavo por el norte de la Estacion y '
             'envuelve su cabeza este como balcon de llegada; el dosel se abre en oculo sobre la boca; '
             'el tren T-SE y las jardineras forman el borde sur; pavimento radial = atrio.')
}
log('B', 'atrio_v004: estacion (anillo+belvedere+senaletica) + Carmen (media luna) + aprons')

# ---------- meta ----------
m['version'] = 'v004 (2026-08-11, FASE 03B.7 — rama de refinamiento geometrico + detailing)'
m['resoluciones_03b7'] = {'urbano': 'A1 portico ECI · A2 arboles · A3 franjas E/N · B abrazo Estacion',
                          'generador': 'build_all_03b7.py (EDGE_GUARD, loops recortados, cinta proyectada, '
                                       'perfil de anchura, detailing LOD A/B/C)'}
out = os.path.join(HERE, 'geometria_maestra_v004.json')
json.dump(m, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
json.dump(DIFF, open(os.path.join(HERE, '_v004_diff.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('v004:', out)
print('guard edificios:', len(GRANDES), '· arboles reubicados:', sum(1 for x in mov if x['a']), '· retirados:',
      sum(1 for x in mov if not x['a']), '· T-O caps:', n_to)
