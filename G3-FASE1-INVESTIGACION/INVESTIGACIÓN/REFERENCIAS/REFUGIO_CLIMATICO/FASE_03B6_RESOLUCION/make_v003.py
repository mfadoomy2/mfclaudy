# -*- coding: utf-8 -*-
"""
GEOMETRIA MAESTRA v003 — FASE 03B.6.
Transformaciones de DATOS derivadas del AUDIT_RESOLUTION_PLAN (CR-2/3/4/7/8/9).
v002 NO se toca. Cada cambio queda en el diff v002->v003 (_v003_diff.json).
Las reglas de generador (guard, escaleras, ascensores...) viven en build_all_03b6.py.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.normpath(os.path.join(HERE, '..', 'FASE_03B_MODELO_MAESTRO', 'geometria_maestra_v002.json'))
m = json.load(open(V2, encoding='utf-8'))
DIFF = {'base': 'geometria_maestra_v002.json', 'fecha': '2026-08-11', 'cambios': []}


def log(cr, que, detalle):
    DIFF['cambios'].append({'causa': cr, 'que': que, 'detalle': detalle})


def d2seg(px, py, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    L2 = vx * vx + vy * vy or 1e-9
    t = max(0, min(1, ((px - ax) * vx + (py - ay) * vy) / L2))
    return math.hypot(px - (ax + vx * t), py - (ay + vy * t)), t


def d2poly(px, py, pts):
    best = (1e9, 0, 0)
    for i in range(len(pts) - 1):
        d, t = d2seg(px, py, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1])
        if d < best[0]:
            best = (d, i, t)
    return best


RIB = m['circulacion']['ribbon']
LOOPS = {lp['id']: lp for lp in m['estructura_principal']['loops']}
LOOP_Z = {'C1-L1': 10.0, 'C1-L2': 8.0, 'C1-L3': 8.0, 'C2-L1': 11.0, 'C2-L2': 9.0,
          'C2-L3': 7.5, 'C3-L1': 10.0, 'C3-L2': 8.5}

# ================= CR-8 · CONOS VISUALES + VENTANAS DE INVIERNO (datos de arbitraje) =================
RELOJ = (-25.2, -34.35)
CONOS = []
for (vx, vy, nombre) in [(-33, 50, 'preciados'), (6, 58, 'carmen'), (44, 55, 'montera'),
                         (86, -2, 'alcala'), (-92, 4, 'arenal'), (-28, -14, 'estatua'),
                         (17, -8, 'splash'), (-84, -5, 'cinta-C1'), (3, 29, 'cinta-C2')]:
    CONOS.append({'desde': [vx, vy], 'hasta': list(RELOJ), 'semiancho_m': 6.0, 'nombre': nombre})
m['visuales_v003'] = {'objetivo': 'reloj +26.5 / torre +22.0', 'conos': CONOS,
                      'regla': 'ningun elemento NUEVO con cota >2.5 dentro de un cono; existentes documentados (38.6% = precio del dosel)'}
VENTANAS_INVIERNO = [
    {'nombre': 'W1-eje-este+Correos', 'poly': [[-10, -22], [55, -22], [55, -4], [-10, -4]]},
    {'nombre': 'W2-splash', 'poly': [[6, -16], [28, -16], [28, 2], [6, 2]]},
]
m['invierno_v003'] = {'ventanas': VENTANAS_INVIERNO,
                      'regla': 'sin sombra NUEVA dentro; arboles nuevos = caduco; lamina microalgas = vaciado invernal (operacion)',
                      'origen': 'CL-001'}
log('CR-8', 'conos visuales + ventanas de invierno', '9 conos al reloj (semiancho 6 m) y 2 ventanas sin sombra nueva')


def en_cono(px, py):
    for c in CONOS:
        ax, ay = c['desde']; bx, by = c['hasta']
        d, t = d2seg(px, py, ax, ay, bx, by)
        if d < c['semiancho_m'] and 0.02 < t < 0.98:
            return c['nombre']
    return None


def en_ventana(px, py):
    for w in VENTANAS_INVIERNO:
        xs = [p[0] for p in w['poly']]; ys = [p[1] for p in w['poly']]
        if min(xs) <= px <= max(xs) and min(ys) <= py <= max(ys):
            return w['nombre']
    return None


# ================= CR-3c · DISCOS QUE ATRAVIESAN EL TABLERO -> SOMBRA DE CINTA =================
snapped = []
for i, d in enumerate(m['paisaje']['discs']):
    dist, _, _ = d2poly(d['cx'], d['cy'], RIB)
    if dist < d['r'] + 1.7 and 5.2 < d.get('cota', 6.0) < 8.3:
        old = d['cota']
        d['cota'] = 8.3
        d['rol_v003'] = 'sombra-cinta (antes atravesaba el tablero)'
        snapped.append({'i': i, 'xy': [d['cx'], d['cy']], 'cota': [old, 8.3]})
log('CR-3c', 'discos elevados a +8.30 sobre la cinta', snapped)

# ================= CR-3c · NUEVOS DISCOS DE SOMBRA DE CINTA (tramos sin cobertura) =================
DISCS = m['paisaje']['discs']
nuevos_cinta = []
acc = 0.0
lado = 1
for i in range(1, len(RIB)):
    acc += math.hypot(RIB[i][0] - RIB[i - 1][0], RIB[i][1] - RIB[i - 1][1])
    if acc < 9.0:
        continue
    acc = 0.0
    px, py = RIB[i]
    cubierto = any(math.hypot(d['cx'] - px, d['cy'] - py) < 4.0 and d.get('cota', 6) >= 7.6 for d in DISCS)
    if cubierto:
        continue
    dx = RIB[i][0] - RIB[i - 1][0]; dy = RIB[i][1] - RIB[i - 1][1]
    L = math.hypot(dx, dy) or 1e-9
    nx, ny = -dy / L * 2.3 * lado, dx / L * 2.3 * lado
    cx, cy = round(px + nx, 2), round(py + ny, 2)
    if en_cono(cx, cy) or en_ventana(cx, cy):
        continue
    lado *= -1
    nd = dict(cx=cx, cy=cy, r=2.4, cota=8.3, loop='cinta-sombra', g='G3', rol_v003='sombra-cinta E03B6')
    DISCS.append(nd)
    nuevos_cinta.append([cx, cy])
log('CR-3c', 'discos nuevos de sombra de cinta a +8.3 alternados', {'n': len(nuevos_cinta), 'xy': nuevos_cinta})

# ================= CR-4 · SOMBRA SOBRE EL MOVIMIENTO (derogacion aerea de near_corr) =================
CORR = {c['id']: c['pts'] for c in m['circulacion']['corridors']}
CAND_CORREDOR = [
    (-12, 2, 'CL-HOT-010 istmo'), (-18, 17, 'CL-HOT-014 istmo O'), (3, 26, 'CL-HOT-021 C2N'),
    (-25, 31, 'CL-HOT-022'), (-42, 17, 'CL-HOT-012 C1E'), (-36, 35, 'CL-HOT-024'),
    (-4, 37, 'CL-HOT-023'), (-18, -12, 'eje oeste 1'), (-42, -12, 'eje oeste 2'), (-52, -13, 'eje oeste 3'),
]
nuevos_corr = []
for (cx, cy, motivo) in CAND_CORREDOR:
    if en_cono(cx, cy) or en_ventana(cx, cy):
        log('CR-4', 'candidato descartado por cono/ventana', {'xy': [cx, cy], 'motivo': motivo})
        continue
    if math.hypot(cx - (-28), cy - (-14)) < 10.0:
        log('CR-4', 'candidato descartado por respeto a la estatua', {'xy': [cx, cy]})
        continue
    nd = dict(cx=cx, cy=cy, r=2.6, cota=5.0, loop='corredor-sombra', g='G3',
              rol_v003='sombra-corredor E03B6 (%s)' % motivo, mastil_offset=2.4)
    DISCS.append(nd)
    nuevos_corr.append([cx, cy])
log('CR-4', 'discos de sombra de corredor a +5.0 (mastil fuera de eje)', {'n': len(nuevos_corr), 'xy': nuevos_corr})

# arboles de sombra en el paseo norte (CL-HOT-020, zona de contexto)
ARB_N = [(33, 40.5), (39, 42.5), (45, 43.5), (51, 41.5), (57, 39.5)]
arb_ok = []
for (tx, ty) in ARB_N:
    dmin = min(d2poly(tx, ty, pts)[0] for pts in CORR.values())
    if dmin < 2.5:
        continue
    m['paisaje']['new_trees'].append((tx, ty))
    arb_ok.append([tx, ty])
log('CR-4', 'arboles de sombra en paseo norte (caducos)', arb_ok)

# ================= CR-2 · PUERTAS EN LOS TRENES (v2) =================
# Las posiciones aprobadas se CONSERVAN (respetan los recortes de metro de 03A, que la
# regeneracion por arco violaba: POD_TRAIN a 0.22 m de la boca de Cercanias).
# La puerta se abre RETIRANDO capsulas: nunca mas de 3 seguidas; se retira con preferencia
# la capsula que colisiona con un mastil (V-06x). Puerta resultante >= ancho de capsula (3.2 m).
MASTS_XY = [tuple(p) for p in m['estructura_ligera']['masts']]
old_caps = m['programa']['capsules']
finales = [c for c in old_caps if c.get('id') not in ('T-O', 'T-SE')]
puertas = {}
for tid, lp in (('T-O', LOOPS['C1-L1']), ('T-SE', LOOPS['C3-L2'])):
    caps = [c for c in old_caps if c.get('id') == tid]
    r = math.radians(lp['rot'])

    def ang(c, r=r, lp=lp):
        dx, dy = c['cx'] - lp['cx'], c['cy'] - lp['cy']
        xr = dx * math.cos(-r) - dy * math.sin(-r)
        yr = dx * math.sin(-r) + dy * math.cos(-r)
        return math.degrees(math.atan2(yr, xr)) % 360

    caps.sort(key=ang)
    drop = set()
    for i, c in enumerate(caps):
        if any(math.hypot(c['cx'] - mx, c['cy'] - my) < 2.9 for (mx, my) in MASTS_XY):
            drop.add(i)
    seguidas = 0
    for i in range(len(caps)):
        if i in drop:
            seguidas = 0
            continue
        seguidas += 1
        if seguidas > 3:
            drop.add(i)
            seguidas = 0
    finales += [c for i, c in enumerate(caps) if i not in drop]
    puertas[tid] = {'capsulas': len(caps), 'retiradas': [[round(caps[i]['cx'], 1), round(caps[i]['cy'], 1)]
                                                         for i in sorted(drop)]}
m['programa']['capsules'] = finales
log('CR-2', 'puertas por retirada de capsulas (posiciones aprobadas intactas)', puertas)

# ================= CR-9a · RE-TRAZADOS DE CORREDOR (antes del empuje de NEB) =================
# eje: rodea la estatua por el sur (la grada llega a y=-15.9; el eje pasa a -18.6)
# montera: el vertice (43.5,-2) se lleva a (44.8,-2) para librar la cuba del mastil en (41.8,-0.2)
for c in m['circulacion']['corridors']:
    if c['id'] == 'eje-mayor-alcala':
        c['pts'] = [(-95, -10), (-78, -15), (-58, -12), (-40, -11), (-35, -14), (-31, -18.6),
                    (-25, -18.6), (-20, -15), (-16, -12.5), (20, -14), (50, -16), (66, -18),
                    (78, -15), (86, -4)]
    if c['id'] == 'montera-espozymina':
        c['pts'] = [(44, 55), (40, 40), (40, 14), (44.2, -2), (36, -14), (26, -28)]
CORR = {c['id']: c['pts'] for c in m['circulacion']['corridors']}
log('CR-9', 'eje por el sur de la estatua + vertice de montera librando la cuba', None)

# ================= CR-7b · NEBULIZADORES fuera de las bandas de boca (en DATOS) =================
MXY_ = [(e['x'], e['y']) for e in m['contexto']['metro'] if -110 < e['x'] < 100 and -45 < e['y'] < 75]
neb2, nmov = [], []
for (nx, ny) in m['agua_clima']['nebul']:
    for (a, b) in MXY_:
        d = math.hypot(nx - a, ny - b)
        if d < 5.95:
            nx, ny = a + (nx - a) / (d or 1e-9) * 5.95, b + (ny - b) / (d or 1e-9) * 5.95
            nmov.append([round(nx, 2), round(ny, 2)])
    # el poste tampoco pisa el eje de un corredor: a >=2.8 del eje la nube (r 3.0) sigue cubriendolo
    dmin, qi, qt = d2poly(nx, ny, next(iter(CORR.values())))[0], None, None
    for pts in CORR.values():
        dd, i_, t_ = d2poly(nx, ny, pts)
        if dd < 2.8:
            ax_, ay_ = pts[i_]; bx_, by_ = pts[i_ + 1]
            qx_ = ax_ + (bx_ - ax_) * t_; qy_ = ay_ + (by_ - ay_) * t_
            L_ = dd or 1e-9
            nx, ny = qx_ + (nx - qx_) / L_ * 2.8, qy_ + (ny - qy_) / L_ * 2.8
            nmov.append([round(nx, 2), round(ny, 2)])
    neb2.append((round(nx, 2), round(ny, 2)))
m['agua_clima']['nebul'] = neb2
log('CR-7', 'nebulizadores fuera de banda de boca (5.95) y fuera de eje de corredor (2.8)', nmov)

# ================= CR-7 · METRO: E-3 fuera del claro de Carmen =================
for p in m['agua_clima']['ground_ponds']:
    if p['id'] == 'E-3':
        old = [p['cx'], p['cy']]
        p['cx'], p['cy'] = 10.4, 20.4
        log('CR-7', 'estanque E-3 desplazado (bordillo a 4.92 m de boca Carmen)', {'de': old, 'a': [10.4, 20.4]})

# ================= CR-6 · MANTENIMIENTO: gotas re-espaciadas + viveros + registros + recirculacion =================
drops = [tuple(p) for p in m['estructura_ligera']['drops']]
grupos = []
for p in drops:
    for g in grupos:
        if any(math.hypot(p[0] - q[0], p[1] - q[1]) < 4.0 for q in g):
            g.append(p)
            break
    else:
        grupos.append([p])
nd = []
for g in grupos:
    if len(g) < 2:
        nd += g
        continue
    cx = sum(p[0] for p in g) / len(g); cy = sum(p[1] for p in g) / len(g)
    ux, uy = g[-1][0] - g[0][0], g[-1][1] - g[0][1]
    L = math.hypot(ux, uy) or 1.0
    ux, uy = ux / L, uy / L
    for i, _ in enumerate(g):
        s = (i - (len(g) - 1) / 2.0) * 3.05
        nd.append((round(cx + ux * s, 2), round(cy + uy * s, 2)))
m['estructura_ligera']['drops'] = nd
log('CR-6', 'depositos-gota re-espaciados a 3.05 m entre centros (paso libre ~1.45 > 0.90)', nd)

m['mantenimiento_v003'] = {
    'viveros': [[24.0, 16.0], [27.0, 20.0], [21.0, 11.0]],
    'registros_tecnicos': [[-69.5, 15.5], [12.5, 31.5], [78.0, 12.0]],
    'plataforma_deposito': 'plataforma 1.2x1.2 + pates en los 6 postes de deposito +10.5',
    'recirculacion': [
        [[-69.5, 15.5], [-62, 16], [-52, 17], [-44, 16.6]],
        [[12.5, 31.5], [8, 26], [10.4, 20.4], [14, 12]],
        [[78.0, 12.0], [70, 9], [62, 8], [54, 8]],
    ],
    'puerta_jardinera_DC1': 'hueco 1.2 m en la jardinera junto a (-72,17)',
    'protocolo': 'MAINTENANCE_PROTOCOL.md',
}
log('CR-6', 'reserva tecnica: 3 registros + recirculacion por cluster + viveros reubicados', m['mantenimiento_v003']['registros_tecnicos'])

# ================= CR-9 · ESTATUA CARLOS III (DEC-0006) =================
m['contexto']['hitos']['carlos_iii'] = (-28.0, -14.0)
m['estatua_v003'] = {'xy': [-28.0, -14.0], 'g': 'G2+', 'fuente': '0F53E6F0 (DEC-0006); pendiente plano municipal',
                     'pedestal': [4.4, 2.6, 2.4], 'volumen_ecuestre_h': 4.2, 'respeto_r': 8.0}
# (re-trazado del eje: ver CR-9a, antes del empuje de NEB)
log('CR-9', 'estatua consolidada (pedestal 4.4x2.6x2.4 + volumen ecuestre, respeto r=8)',
    m['estatua_v003'])

# ================= CR-3e · BALSA B-C3b (colision con barandilla de cinta) =================
for p in m['agua_clima']['pools']:
    if p['id'] == 'B-C3b':
        old = p['cota']
        p['cota'] = 7.6
        log('CR-3e', 'balsa B-C3b elevada (tocaba la barandilla +7.05)', {'cota': [old, 7.6]})

m['version'] = 'v003 (2026-08-11, FASE 03B.6 - resolucion integrada de auditorias)'
m['resoluciones_03b6'] = {'plan': 'AUDIT_RESOLUTION_PLAN.md', 'causas': 'CR-1..CR-9',
                          'reglas_generador': 'build_all_03b6.py (conflict_guard, escaleras 17+17, 3 ascensores-capsula, barandilla completa, poda, respaldos, canaletas, plataformas)'}

out = os.path.join(HERE, 'geometria_maestra_v003.json')
json.dump(m, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
json.dump(DIFF, open(os.path.join(HERE, '_v003_diff.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('v003:', out)
print('discos:', len(DISCS), '(+%d cinta, +%d corredor, %d re-cotados)' % (len(nuevos_cinta), len(nuevos_corr), len(snapped)))
print('capsulas:', len(m['programa']['capsules']), '· arboles:', len(m['paisaje']['new_trees']), '· cambios diff:', len(DIFF['cambios']))
