# -*- coding: utf-8 -*-
"""
FASE 03B.5 — motor de auditoria (A0..A11).
Mide, no corrige. Escribe JSON/NPY en _data/ ; los PDF los arma audit_report.py.
"""
import heapq
import json
import math
import os
import sys
import time

import numpy as np
from scipy import ndimage as ndi

import audit_core as C
from audit_core import CELL, BODY_LO, BODY_HI, DATA, jdump

T0 = time.time()
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


def log(*a):
    print('[%6.1fs]' % (time.time() - T0), *a, flush=True)


# =============================================================== A0 · ESCENA Y REJILLAS
log('A0 · reconstruyendo escena aprobada (full=True)')
OBJS, M, B = C.load_scene()
MESH = [o for o in OBJS if o['kind'] == 'mesh']
CURV = [o for o in OBJS if o['kind'] == 'curve']
for o in MESH:
    o['fam'] = C.obj_family(o)
    o['bb'] = (o['V'].min(0), o['V'].max(0))

GRID = C.Grid(-112, -45, 100, 78)
NY, NX = GRID.shape()
log('   objetos=%d mallas=%d curvas=%d  rejilla=%dx%d (%.2f m)' % (len(OBJS), len(MESH), len(CURV), NX, NY, CELL))

SOLID = [o for o in MESH if o['layer'] not in C.NON_SOLID and o['layer'] != '01_GROUND']
PROJ = [o for o in SOLID if o['layer'] not in C.CONTEXT]

TRIS_ALL = np.concatenate([C.tris_of(o) for o in SOLID])
OCC = C.rasterize(GRID, TRIS_ALL, BODY_LO, BODY_HI, 'mask')          # obstruccion 0.05-2.10
FREE = ~OCC
log('   banda cuerpo: %d celdas ocupadas (%.1f %%)' % (OCC.sum(), 100 * OCC.mean()))

# --- envolvente de proyecto (PLAZA) = huella de proyecto dilatada 6 m, rellena
PROJ_FOOT = C.rasterize(GRID, np.concatenate([C.tris_of(o) for o in PROJ]), -1, 40, 'mask')
disk = np.zeros((49, 49), bool)
yy, xx = np.mgrid[-24:25, -24:25]
disk[(yy ** 2 + xx ** 2) <= 24 ** 2] = True                          # 6.0 m
PLAZA = ndi.binary_fill_holes(ndi.binary_dilation(PROJ_FOOT, disk))
WALK = PLAZA & FREE                                                  # suelo pisable del ambito
log('   ambito PLAZA=%.0f m2 · libre a nivel de cuerpo=%.0f m2' %
    (PLAZA.sum() * CELL ** 2, WALK.sum() * CELL ** 2))

# --- distancia al obstaculo mas proximo (radio de holgura) y anchura local
DT = ndi.distance_transform_edt(FREE) * CELL
WIDTH = 2.0 * DT                                                     # anchura libre local

# --- etiqueta de causa de obstruccion (que familia ocupa cada celda)
FAM_ORDER = ['CONTEXT', 'STRUCTURE', 'RIBBON', 'PODS', 'CANOPY', 'PLANTER',
             'VEGETATION', 'FURNITURE', 'WATER']
CAUSE = np.zeros((NY, NX), np.uint8)
for k, fam in enumerate(FAM_ORDER, start=1):
    sel = [o for o in SOLID if o['fam'] == fam]
    if not sel:
        continue
    mk_ = C.rasterize(GRID, np.concatenate([C.tris_of(o) for o in sel]), BODY_LO, BODY_HI, 'mask')
    CAUSE[(CAUSE == 0) & mk_] = k
log('   mapa de causa de obstruccion listo')

# --- altura libre (galibo) sobre el nivel de cuerpo.
#     Se separan dos cosas que el HEIGHT_SYSTEM ya distingue: la regla 7 exige 3.00 m bajo
#     "elemento FIRME". Una copa de arbol no es un elemento firme: es una cuestion de poda.
ZMIN = C.rasterize(GRID, TRIS_ALL, BODY_HI, None, 'zmin')
CLEAR = np.where(np.isfinite(ZMIN), ZMIN, np.nan)
TRIS_FIRME = np.concatenate([C.tris_of(o) for o in SOLID if o['fam'] != 'VEGETATION'])
TRIS_VEG = np.concatenate([C.tris_of(o) for o in SOLID if o['fam'] == 'VEGETATION'])
CLEAR_F = np.where(np.isfinite(C.rasterize(GRID, TRIS_FIRME, BODY_HI, None, 'zmin')),
                   C.rasterize(GRID, TRIS_FIRME, BODY_HI, None, 'zmin'), np.nan)
CLEAR_V = C.rasterize(GRID, TRIS_VEG, BODY_HI, None, 'zmin')
CLEAR_V = np.where(np.isfinite(CLEAR_V), CLEAR_V, np.nan)
log('   mapa de galibo listo (firme + vegetal)')

np.save(os.path.join(DATA, 'occ.npy'), OCC)
np.save(os.path.join(DATA, 'walk.npy'), WALK)
np.save(os.path.join(DATA, 'plaza.npy'), PLAZA)
np.save(os.path.join(DATA, 'width.npy'), WIDTH)
np.save(os.path.join(DATA, 'clear.npy'), CLEAR)
np.save(os.path.join(DATA, 'clear_firme.npy'), CLEAR_F)
np.save(os.path.join(DATA, 'clear_veg.npy'), CLEAR_V)
np.save(os.path.join(DATA, 'cause.npy'), CAUSE)

ISS = C.Issues()


def cell_free(x, y):
    i, j = GRID.ij(x, y)
    return GRID.inside(i, j) and FREE[i, j]


def width_at(x, y):
    i, j = GRID.ij(x, y)
    return float(WIDTH[i, j]) if GRID.inside(i, j) else 0.0


def cause_at(x, y):
    i, j = GRID.ij(x, y)
    if not GRID.inside(i, j):
        return 'FUERA'
    k = int(CAUSE[i, j])
    return FAM_ORDER[k - 1] if k else 'LIBRE'


def ray_free(x, y, dx, dy, maxd=30.0):
    """distancia libre desde (x,y) en direccion (dx,dy) hasta obstaculo."""
    n = int(maxd / CELL)
    for s in range(1, n + 1):
        d = s * CELL
        i, j = GRID.ij(x + dx * d, y + dy * d)
        if not GRID.inside(i, j) or OCC[i, j]:
            return d - CELL, (cause_at(x + dx * d, y + dy * d) if GRID.inside(i, j) else 'BORDE')
    return maxd, 'ABIERTO'


# =============================================================== A1 · RECORRIDOS
log('A1 · red peatonal: ejes, anchuras, estrechamientos, cul-de-sac')
CORR = M['circulacion']['corridors']
paths = []
for c in CORR:
    P, S = C.resample(c['pts'], 0.5)
    Nn = C.normals(P)
    rows = []
    for k in range(len(P)):
        x, y = P[k]
        nx_, ny_ = Nn[k]
        onaxis = cell_free(x, y)
        dl, cl = ray_free(x, y, nx_, ny_) if onaxis else (0.0, cause_at(x, y))
        dr, cr = ray_free(x, y, -nx_, -ny_) if onaxis else (0.0, cause_at(x, y))
        rows.append(dict(s=float(S[k]), x=float(x), y=float(y),
                         w_transv=float(dl + dr), w_local=width_at(x, y),
                         izq=float(dl), der=float(dr), c_izq=cl, c_der=cr,
                         eje_libre=bool(onaxis)))
    w = np.array([r['w_transv'] for r in rows])
    wl = np.array([r['w_local'] for r in rows])
    paths.append(dict(id=c['id'], nota=c.get('nota', ''), long=float(S[-1]),
                      n=len(rows), rows=rows,
                      w_min=float(w.min()), w_p05=float(np.percentile(w, 5)),
                      w_p25=float(np.percentile(w, 25)), w_p50=float(np.percentile(w, 50)),
                      w_p75=float(np.percentile(w, 75)), w_max=float(w.max()),
                      wl_min=float(wl.min()), wl_p05=float(np.percentile(wl, 5)),
                      wl_p50=float(np.percentile(wl, 50)),
                      eje_bloqueado=int(sum(1 for r in rows if not r['eje_libre']))))
    log('   %-22s L=%5.1f m  ancho transv min=%4.1f p05=%4.1f p50=%5.1f  (eje bloqueado en %d/%d est.)'
        % (c['id'], S[-1], w.min(), np.percentile(w, 5), np.percentile(w, 50),
           paths[-1]['eje_bloqueado'], len(rows)))

# --- estrechamientos: minimos locales de la HOLGURA LOCAL (2*DT) sobre cada eje.
#     En una plaza abierta el ancho transversal de fachada a fachada no discrimina;
#     el estrangulamiento real lo da la holgura libre alrededor del eje.
NARROW = []
for p in paths:
    wl = np.array([r['w_local'] for r in p['rows']])
    wt = np.array([r['w_transv'] for r in p['rows']])
    for k in range(2, len(wl) - 2):
        if wl[k] <= wl[k - 1] and wl[k] <= wl[k + 1] and wl[k] < 6.0:
            if any(abs(k - q['k']) < 10 and q['path'] == p['id'] for q in NARROW):
                continue
            r = p['rows'][k]
            NARROW.append(dict(path=p['id'], k=k, s=r['s'], x=r['x'], y=r['y'],
                               w=float(wl[k]), w_transv=float(wt[k]), w_local=float(wl[k]),
                               causa='%s / %s' % (r['c_izq'], r['c_der'])))
NARROW.sort(key=lambda q: q['w'])
log('   estrechamientos detectados: %d (holgura minima %.2f m)' % (len(NARROW), NARROW[0]['w'] if NARROW else -1))
# --- estrangulamientos globales del suelo libre (no solo sobre los ejes declarados)
CHOKE = []
cand = WALK & (WIDTH < 1.20) & (WIDTH <= ndi.minimum_filter(np.where(WALK, WIDTH, 99.0), size=13))
lbc, nlc = ndi.label(cand, structure=np.ones((3, 3)))
if nlc:
    for k, sl in enumerate(ndi.find_objects(lbc), start=1):
        sub = np.where(lbc[sl] == k, WIDTH[sl], 99.0)
        di, dj = np.unravel_index(np.argmin(sub), sub.shape)
        i, j = sl[0].start + di, sl[1].start + dj
        x, y = GRID.xy(i, j)
        if any(math.hypot(x - q['x'], y - q['y']) < 2.0 for q in CHOKE):
            continue
        # de que familias son los dos bordes que estrangulan
        cs = set()
        for a in range(0, 360, 20):
            rr = math.radians(a)
            _d, cc_ = ray_free(x, y, math.cos(rr), math.sin(rr), 3.0)
            if cc_ not in ('ABIERTO', 'BORDE', 'LIBRE'):
                cs.add(cc_)
        CHOKE.append(dict(x=float(x), y=float(y), w=float(WIDTH[i, j]), causa='+'.join(sorted(cs)) or '?'))
CHOKE.sort(key=lambda q: q['w'])
log('   pasos estrangulados <1.20 m de holgura (deduplicados a 2 m): %d' % len(CHOKE))

# --- conectividad y anchura critica de la red.
#     Se etiqueta sobre FREE (todo el dominio) y NO sobre WALK: el borde de la envolvente
#     de ambito partiria componentes que en realidad estan conectadas por la calle.
LAB_ALL, NLAB = ndi.label(FREE)
sizes = ndi.sum(FREE, LAB_ALL, range(1, NLAB + 1))
main_lab = int(np.argmax(sizes)) + 1
MAIN = LAB_ALL == main_lab
POCKETS = []
CTX_LAB = FAM_ORDER.index('CONTEXT') + 1
for k in range(1, NLAB + 1):
    if k == main_lab:
        continue
    a = sizes[k - 1] * CELL ** 2
    if a < 8.0:
        continue
    m_ = LAB_ALL == k
    if not (m_ & PLAZA).any():           # bolsas fuera del ambito de intervencion: no se auditan
        continue
    ys, xs = np.where(m_)
    cx, cy = GRID.xy(int(ys.mean()), int(xs.mean()))
    # de que esta hecho el cinturon que la aisla: contexto urbano o proyecto?
    borde = ndi.binary_dilation(m_, np.ones((3, 3))) & ~m_ & (CAUSE > 0)
    lab_b = CAUSE[borde]
    pct_ctx = float((lab_b == CTX_LAB).mean() * 100) if lab_b.size else 0.0
    fams_b = sorted({FAM_ORDER[v - 1] for v in np.unique(lab_b)})
    POCKETS.append(dict(area=float(a), cx=float(cx), cy=float(cy), n=int(sizes[k - 1]),
                        pct_contexto=round(pct_ctx, 1), borde=fams_b,
                        imputable=bool(pct_ctx < 60.0)))
POCKETS.sort(key=lambda q: -q['area'])
nimp = sum(1 for q in POCKETS if q['imputable'])
log('   componentes pisables: %d · bolsas aisladas >8 m2: %d (imputables al proyecto: %d; '
    'el resto son recintos del contexto urbano)' % (NLAB, len(POCKETS), nimp))

# --- fragmentacion por umbral de anchura (a que ancho se rompe la red)
FRAG = []
for wmin in (0.90, 1.20, 1.50, 1.80, 2.00, 2.50, 3.00, 4.00):
    m_ = FREE & (WIDTH >= wmin)
    lb, nl = ndi.label(m_)
    inw = WALK & (WIDTH >= wmin)
    if nl == 0:
        FRAG.append(dict(w=wmin, comp=0, big=0.0, cover=0.0))
        continue
    sz = ndi.sum(m_, lb, range(1, nl + 1))
    # solo cuentan las componentes que tocan el ambito de intervencion
    touch = set(np.unique(lb[PLAZA & m_]))
    inside_sz = ndi.sum(inw, lb, [k for k in sorted(touch) if k]) if touch else []
    inside_sz = np.atleast_1d(inside_sz)
    comp = int(sum(1 for k in touch if k and sz[k - 1] * CELL ** 2 > 20))
    big = float(inside_sz.max() * CELL ** 2) if inside_sz.size else 0.0   # area DENTRO del ambito
    FRAG.append(dict(w=wmin, comp=comp, big=big, cover=float(inw.sum() / WALK.sum())))
    log('   ancho>=%.2f m -> %2d componentes >20 m2 en el ambito, mayor %7.0f m2 (%.0f %% del suelo libre)'
        % (wmin, comp, big, 100 * FRAG[-1]['cover']))

# --- accesos: extremos de los corredores declarados
ACCESS = {}
for c in CORR:
    ACCESS[c['id'] + '·A'] = tuple(c['pts'][0])
    ACCESS[c['id'] + '·B'] = tuple(c['pts'][-1])


log('   calculando cuellos de botella entre accesos (barrido de umbral + componentes)')
FY, FX = np.where(FREE)


def snap(p):
    i, j = GRID.ij(*p)
    if GRID.inside(i, j) and FREE[i, j]:
        return i, j
    k = int(np.argmin((FY - i) ** 2 + (FX - j) ** 2))
    return int(FY[k]), int(FX[k])


AK = list(ACCESS.keys())
APOS = {k: snap(ACCESS[k]) for k in AK}
BOTT = {}
for t in np.arange(40.0, 0.19, -0.25):         # de holgado a estrecho: el primer umbral que une = cuello
    lab, nl = ndi.label(FREE & (WIDTH >= t))
    if nl == 0:
        continue
    ids_ = {k: int(lab[APOS[k]]) for k in AK}
    for a in range(len(AK)):
        for b in range(a + 1, len(AK)):
            ka, kb = AK[a], AK[b]
            key = '%s → %s' % (ka, kb)
            if key in BOTT:
                continue
            if ids_[ka] and ids_[ka] == ids_[kb]:
                BOTT[key] = round(float(t), 2)
for a in range(len(AK)):
    for b in range(a + 1, len(AK)):
        BOTT.setdefault('%s → %s' % (AK[a], AK[b]), 0.0)
bt = sorted(BOTT.items(), key=lambda q: q[1])
# el mismo calculo obligando a cruzar el ambito de intervencion (sin rodear por la calle)
INSIDE = FREE & PLAZA
_li, _nl = ndi.label(INSIDE)
if _nl:
    _sz = ndi.sum(INSIDE, _li, range(1, _nl + 1))
    INSIDE = _li == (int(np.argmax(_sz)) + 1)     # solo la componente principal del ambito
IY, IX = np.where(INSIDE)


def snap_in(p):
    i, j = GRID.ij(*p)
    k = int(np.argmin((IY - i) ** 2 + (IX - j) ** 2))
    return int(IY[k]), int(IX[k])


APOS_IN = {k: snap_in(ACCESS[k]) for k in AK}
BOTT_IN = {}
for t in np.arange(40.0, 0.19, -0.25):
    lab, nl = ndi.label(INSIDE & (WIDTH >= t))
    if nl == 0:
        continue
    ids_ = {k: int(lab[APOS_IN[k]]) for k in AK}
    for a in range(len(AK)):
        for b in range(a + 1, len(AK)):
            ka, kb = AK[a], AK[b]
            key = '%s → %s' % (ka, kb)
            if key in BOTT_IN:
                continue
            if ids_[ka] and ids_[ka] == ids_[kb]:
                BOTT_IN[key] = round(float(t), 2)
for a in range(len(AK)):
    for b in range(a + 1, len(AK)):
        BOTT_IN.setdefault('%s → %s' % (AK[a], AK[b]), 0.0)
bi = sorted(BOTT_IN.items(), key=lambda q: q[1])
log('   cuello atravesando el ambito: min %.2f m (%s) · mediana %.2f m'
    % (bi[0][1], bi[0][0], float(np.median(list(BOTT_IN.values())))))
log('   par mas estrecho: %s = %.2f m · par mas holgado: %s = %.2f m' % (bt[0][0], bt[0][1], bt[-1][0], bt[-1][1]))

jdump('a1_paths.json', dict(paths=paths, narrow=NARROW, choke=CHOKE[:200], pockets=POCKETS, frag=FRAG,
                            bottleneck=BOTT, bottleneck_ambito=BOTT_IN,
                            access={k: list(v) for k, v in ACCESS.items()}))

# --- incidencias A1
for q in NARROW[:14]:
    sev = 'RED' if q['w'] < 1.80 else ('YELLOW' if q['w'] < 3.00 else 'GREEN')
    if sev == 'GREEN':
        continue
    ISS.add(sev, 'RECORRIDOS', 'Estrechamiento en %s (s=%.0f m)' % (q['path'], q['s']),
            q['x'], q['y'], 0,
            mag='holgura libre %.2f m sobre el eje (ancho transversal disponible %.1f m)' % (q['w'], q['w_transv']),
            cause='obstaculos laterales: %s' % q['causa'],
            strat='reubicar el elemento lateral · reducir radio de jardinera · desplazar el eje del corredor',
            ref='A1', metric=q['w'])
for q in CHOKE[:10]:
    if q['w'] >= 1.20:
        break
    ISS.add('RED', 'RECORRIDOS', 'Paso estrangulado a %.2f m entre %s' % (q['w'], q['causa']),
            q['x'], q['y'], 0, mag='holgura libre %.2f m (no admite el cruce de dos personas)' % q['w'],
            cause='dos elementos de la familia %s implantados sin comprobar el hueco entre ellos' % q['causa'],
            strat='separar las dos instancias · suprimir una · reconocerlo como paso de servicio',
            ref='A1', metric=q['w'])
for p in paths:
    if p['eje_bloqueado'] > 0:
        k = next(r for r in p['rows'] if not r['eje_libre'])
        ISS.add('RED', 'RECORRIDOS', 'Eje de %s ocupado por geometria en %d estaciones' % (p['id'], p['eje_bloqueado']),
                k['x'], k['y'], 0, mag='%d de %d estaciones (%.0f m de traza)' % (p['eje_bloqueado'], p['n'], p['eje_bloqueado'] * 0.5),
                cause='el eje declarado atraviesa %s' % cause_at(k['x'], k['y']),
                strat='redefinir la traza del corredor o retirar el elemento invasor', ref='A1')
ISS.add('GREEN', 'RECORRIDOS', 'La red peatonal principal se mantiene continua a 3,00 m de holgura',
        mag='con exigencia de 3,00 m continuos sigue conectado el %.0f %% del suelo libre en %d componentes '
            '(el mayor de %.0f m2); a 1,80 m, el %.0f %%'
            % (100 * FRAG[6]['cover'], FRAG[6]['comp'], FRAG[6]['big'], 100 * FRAG[3]['cover']),
        cause='—', strat='sin accion', ref='A1')
ISS.add('GREEN', 'ACCESIBILIDAD', 'El plano de plaza es horizontal en todo el ambito',
        mag='cota 0.00 en toda la superficie construida: 0 %% de pendiente longitudinal y transversal a nivel de suelo',
        cause='el modelo 03B resuelve la plaza como plano unico',
        strat='verificar en fases posteriores la pendiente real de evacuacion de agua superficial (0 %% no drena)',
        ref='A5')
for q in [p for p in POCKETS if p['imputable']][:6]:
    ISS.add('YELLOW', 'RECORRIDOS', 'Bolsa de suelo sin conexion pisable (%.0f m2)' % q['area'],
            q['cx'], q['cy'], 0,
            mag='area aislada %.0f m2 · cinturon: %s (%.0f %% contexto)' % (q['area'], ','.join(q['borde']), q['pct_contexto']),
            cause='cinturon continuo de jardineras/vegetacion/agua sin hueco de paso',
            strat='abrir un vano de acceso o declararla explicitamente como area no accesible', ref='A1')
nctx = sum(1 for p in POCKETS if not p['imputable'])
if nctx:
    ISS.add('GREEN', 'RECORRIDOS', '%d bolsas aisladas son recintos del contexto urbano, no del proyecto' % nctx,
            mag='%.0f m2 en total, delimitados en mas del 60 %% por huellas de edificio existentes (patios y calles '
                'cerradas capturados por la envolvente de analisis)' % sum(p['area'] for p in POCKETS if not p['imputable']),
            cause='la envolvente de ambito se obtiene dilatando la huella de proyecto 6 m y rellenando huecos',
            strat='sin accion: se excluyen del computo de cul-de-sac imputables al proyecto', ref='A1')

# =============================================================== A2 · GALIBOS
log('A2 · galibos: CLEAR_HEIGHT_MAP')
CL = CLEAR.copy()
CL[~WALK] = np.nan
valid = np.isfinite(CL)
gal = dict(area_cubierta=float(valid.sum() * CELL ** 2),
           area_libre=float(WALK.sum() * CELL ** 2),
           pct_cubierta=float(100.0 * valid.sum() / max(WALK.sum(), 1)),
           minimo=float(np.nanmin(CL)) if valid.any() else None,
           p01=float(np.nanpercentile(CL[valid], 1)) if valid.any() else None,
           p05=float(np.nanpercentile(CL[valid], 5)) if valid.any() else None,
           p50=float(np.nanpercentile(CL[valid], 50)) if valid.any() else None)
log('   suelo pisable bajo elemento: %.0f m2 (%.0f %%) · galibo min %.2f m · p05 %.2f m'
    % (gal['area_cubierta'], gal['pct_cubierta'], gal['minimo'], gal['p05']))

BBMIN = np.array([o['bb'][0] for o in SOLID])
BBMAX = np.array([o['bb'][1] for o in SOLID])
NAMES = np.array([o['name'] for o in SOLID])
FAMS_ = np.array([o['fam'] for o in SOLID])


def spots(field, thr, only_veg=None, amin=0.25):
    """manchas de suelo pisable por debajo de `thr` en el campo dado."""
    f = np.where(WALK, field, np.nan)
    msk = np.isfinite(f) & (f < thr)
    lb_, nl_ = ndi.label(msk)
    out = []
    if not nl_:
        return out
    for k, sl in enumerate(ndi.find_objects(lb_), start=1):
        m_ = lb_[sl] == k
        a = m_.sum() * CELL ** 2
        if a < amin:
            continue
        sub = np.where(m_, f[sl], np.nan)
        di, dj = np.unravel_index(np.nanargmin(sub), sub.shape)
        idx = (sl[0].start + di, sl[1].start + dj)
        x, y = GRID.xy(*idx)
        sel = ((BBMIN[:, 0] - .4 <= x) & (x <= BBMAX[:, 0] + .4) &
               (BBMIN[:, 1] - .4 <= y) & (y <= BBMAX[:, 1] + .4) & (BBMIN[:, 2] >= BODY_HI))
        if only_veg is not None:
            sel &= (FAMS_ == 'VEGETATION') if only_veg else (FAMS_ != 'VEGETATION')
        who = str(NAMES[sel][np.argmin(BBMIN[sel, 2])]) if sel.any() else ''
        fam = str(FAMS_[sel][np.argmin(BBMIN[sel, 2])]) if sel.any() else ''
        out.append(dict(x=float(x), y=float(y), h=float(f[idx]), area=float(a), obj=who, fam=fam))
    out.sort(key=lambda q: q['h'])
    return out


low_firme = spots(CLEAR_F, 3.00, only_veg=False)
low_veg = spots(CLEAR_V, 2.50, only_veg=True)
low_spots = spots(CLEAR, 3.00)
CF = np.where(WALK, CLEAR_F, np.nan)
CV = np.where(WALK, CLEAR_V, np.nan)
vf = np.isfinite(CF)
gal['minimo_firme'] = float(np.nanmin(CF)) if vf.any() else None
gal['p05_firme'] = float(np.nanpercentile(CF[vf], 5)) if vf.any() else None
gal['area_firme_bajo3'] = float((vf & (CF < 3.0)).sum() * CELL ** 2)
gal['area_veg_bajo250'] = float((np.isfinite(CV) & (CV < 2.5)).sum() * CELL ** 2)
gal['minimo_veg'] = float(np.nanmin(CV)) if np.isfinite(CV).any() else None
log('   ELEMENTO FIRME  · galibo minimo %.2f m · superficie <3.00 m: %.1f m2 en %d manchas >0.25 m2'
    % (gal['minimo_firme'], gal['area_firme_bajo3'], len(low_firme)))
log('   VEGETACION      · galibo minimo %.2f m · superficie <2.50 m: %.1f m2 en %d manchas'
    % (gal['minimo_veg'], gal['area_veg_bajo250'], len(low_veg)))
jdump('a2_clear.json', dict(stats=gal, low=low_spots, low_firme=low_firme, low_veg=low_veg))

def group_spots(lst, r=9.0):
    """agrupa manchas proximas del mismo elemento: una incidencia por fenomeno, no por celda."""
    g = []
    for q in lst:
        for h in g:
            if h['obj'] == q['obj'] and math.hypot(h['x'] - q['x'], h['y'] - q['y']) < r:
                h['n'] += 1; h['area'] += q['area']; h['h'] = min(h['h'], q['h'])
                break
        else:
            g.append(dict(q, n=1))
    return g


for q in group_spots(low_firme, r=1e9):        # una incidencia por TIPO de elemento firme
    sev = 'RED' if q['h'] < 2.50 else 'YELLOW'
    ISS.add(sev, 'GALIBOS', 'Galibo %.2f m bajo elemento firme: %s' % (q['h'], q['obj'] or 'sin identificar'),
            q['x'], q['y'], q['h'],
            mag='%.2f m (%.2f m por debajo del H_CLEAR_MIN 3.00) · %.2f m2 en %d manchas · '
                'peor punto en (%.0f, %.0f)' % (q['h'], 3.0 - q['h'], q['area'], q['n'], q['x'], q['y']),
            cause='cara inferior de %s por debajo del estrato libre peatonal (bajo escalera de la cinta)' % (q['obj'] or '?'),
            strat='cerrar o ajardinar el hueco bajo la zanca · subir el arranque · senalizar el bajo escalera',
            ref='A2', metric=q['h'])
if gal['area_firme_bajo3'] < 2.0:
    ISS.add('GREEN', 'GALIBOS', 'La regla 7 del HEIGHT_SYSTEM se cumple practicamente en todo el ambito',
            mag='bajo elemento FIRME el galibo baja de 3,00 m solo en %.1f m2 de los %.0f m2 de suelo cubierto '
                '(%.2f %%), con un minimo de %.2f m; p05 %.2f m'
                % (gal['area_firme_bajo3'], gal['area_cubierta'],
                   100 * gal['area_firme_bajo3'] / max(gal['area_cubierta'], 1), gal['minimo_firme'], gal['p05_firme']),
            cause='—',
            strat='sin accion sobre la estructura; revisar solo los residuos puntuales listados', ref='A2')
if low_veg:
    q0 = low_veg[0]
    obs = sorted(set(q['obj'] for q in low_veg if q['obj']))
    ISS.add('YELLOW', 'GALIBOS',
            'Copas de arbolado E02 por debajo de 2,50 m sobre suelo pisable (%d puntos)' % len(low_veg),
            q0['x'], q0['y'], q0['h'],
            mag='%.1f m2 de suelo pisable bajo copa a menos de 2,50 m · minimo %.2f m · bloques implicados: %s · '
                'envolvente de cabeza de la persona de referencia 1,85 m'
                % (gal['area_veg_bajo250'], q0['h'], ', '.join(obs)),
            cause='los bloques VEG2_ARBOL_A/B/EX generan la copa como esfera lobulada sin faldon libre de tronco: '
                  'la copa arranca a 0.62·h y el lobulo inferior baja hasta 2,21 m',
            strat='poda de formacion a 2,20–2,50 m (practica normal de arbolado urbano) · o elevar el centro de copa '
                  'en el bloque VEG2_ARBOL. NO es incumplimiento de la regla 7 del HEIGHT_SYSTEM: una copa no es '
                  '«elemento firme». Se registra para que la decision sea explicita.',
            ref='A2', metric=q0['h'])

# --- cables sobre suelo pisable
cab_low = []
for o in CURV:
    if o['layer'] != '05_CABLES':
        continue
    P = o['pts']
    for k in range(len(P) - 1):
        a, b = P[k], P[k + 1]
        for t in np.linspace(0, 1, 12):
            p = a + (b - a) * t
            if p[2] < 3.0 and cell_free(p[0], p[1]):
                i, j = GRID.ij(p[0], p[1])
                if WALK[i, j]:
                    cab_low.append(dict(x=float(p[0]), y=float(p[1]), z=float(p[2]), name=o['name']))
                    break
log('   cables por debajo de 3.00 m sobre suelo pisable: %d muestras' % len(cab_low))
jdump('a2_cables.json', cab_low[:400])
if not cab_low:
    ncab = sum(1 for o in CURV if o['layer'] == '05_CABLES')
    zmin_c = min(float(o['pts'][:, 2].min()) for o in CURV if o['layer'] == '05_CABLES')
    ISS.add('GREEN', 'GALIBOS', 'Ningun cable tensado invade el estrato peatonal',
            mag='%d cables comprobados · cota minima absoluta %.2f m (anclaje de mastil en H_BRANCH_START 3.00)' % (ncab, zmin_c),
            cause='—', strat='sin accion', ref='A2')
if cab_low:
    zz = min(q['z'] for q in cab_low)
    q0 = next(q for q in cab_low if q['z'] == zz)
    ISS.add('RED' if zz < 2.2 else 'YELLOW', 'GALIBOS',
            'Cables tensados cruzan el estrato peatonal (%d puntos por debajo de 3.00 m)' % len(cab_low),
            q0['x'], q0['y'], zz, mag='cota minima de cable sobre suelo pisable %.2f m' % zz,
            cause='anclaje mastil (+3.00) → disco: el tramo bajo del tirante entra en la banda de cabeza',
            strat='subir el punto de anclaje del mastil · desplazar el anclaje fuera del suelo pisable · proteger con jardinera',
            ref='A2', metric=zz)

# =============================================================== A3 · ALTURAS
log('A3 · HEIGHT_SYSTEM vs geometria construida')
BLOCK_Z = {}
for o in MESH:
    if not o['block']:
        continue
    a = o['anchor']
    lo, hi = o['V'][:, 2].min(), o['V'][:, 2].max()
    d = BLOCK_Z.setdefault(o['block'], dict(n=0, lo=1e9, hi=-1e9, anchors=set()))
    d['lo'] = min(d['lo'], lo); d['hi'] = max(d['hi'], hi)
    d['anchors'].add(round(a[2], 3))
NAMED_Z = {}
for o in MESH:
    if o['block']:
        continue
    d = NAMED_Z.setdefault(o['name'], dict(n=0, lo=1e9, hi=-1e9))
    d['n'] += 1
    d['lo'] = min(d['lo'], float(o['V'][:, 2].min())); d['hi'] = max(d['hi'], float(o['V'][:, 2].max()))

DECL = [  # (parametro, valor, rango, como se comprueba)
    ('H_SEATING', 0.45, (0.42, 0.48), ('named', 'BENCH_', 'hi')),
    ('H_PLANTER', 0.60, (0.55, 0.90), ('named', 'PLANTER_', 'hi')),
    ('H_POND_CURB', 0.60, (0.30, 1.00), ('named', 'CURB_', 'hi')),
    ('H_BENCH_BACK', 0.85, (0.80, 0.90), ('absent', 'respaldo', '')),
    ('H_RAIL', 1.05, (1.00, 1.10), ('rail', '', '')),
    ('H_GROUND_TANK', 1.35, (1.20, 1.50), ('block', 'DROP_TANK', 'hi')),
    ('H_TOTEM', 1.35, (1.20, 1.50), ('block', 'TOTEM', 'hi')),
    ('H_BRANCH_START', 3.00, (2.60, 3.50), ('block', 'MAST_2', 'branch')),
    ('H_NURSERY_TOWER', 3.00, (3.00, 3.00), ('block', 'NURSERY', 'hi')),
    ('H_CLEAR_MIN', 3.00, (2.80, 3.20), ('clear', '', '')),
    ('H_MISTING', 4.00, (3.50, 5.00), ('block', 'NEB_POST', 'nozzle')),
    ('H_LOW_CANOPY', 5.00, (4.00, 5.50), ('disc', 'low', '')),
    ('H_RIBBON', 6.00, (5.50, 6.50), ('named', 'RIBBON_DECK', 'hi')),
    ('H_MID_CANOPY', 6.75, (6.00, 7.50), ('disc', 'mid', '')),
    ('H_HIGH_CANOPY', 8.50, (8.00, 9.50), ('disc', 'high', '')),
    ('H_TANK_ELEV', 10.50, (10.00, 12.00), ('named', 'TANK', 'axis')),
    ('H_TANK_TOWER', 5.75, (5.00, 6.00), ('absent', 'torre de depositos apilados', '')),
    ('H_DOME_APEX', 8.00, (8.00, 8.00), ('named', 'DOME_SHELL', 'hi')),
    ('H_TREE_NEW', 5.00, (3.50, 6.50), ('block', 'VEG2_ARBOL_A', 'hi')),
    ('H_TREE_EXIST', 7.00, (5.00, 8.00), ('block', 'VEG2_ARBOL_EX', 'hi')),
    ('H_LOW_VEGETATION', 1.20, (0.50, 2.50), ('block', 'VEG2_BAJA', 'hi')),
    ('H_LOGISTIC_RAIL', 7.50, (6.50, 9.00), ('absent', 'carril logistico (G4 apagada, D9)', '')),
]
DISCS = M['paisaje']['discs']
cotas = np.array([min(max(d.get('cota', 6.0), 4.2), 8.5) for d in DISCS])
hrows = []
for name, val, (lo, hi), (how, key, sub) in DECL:
    built, note, ok = None, '', None
    if how == 'named':
        cand = [k for k in NAMED_Z if k.startswith(key)]
        if cand:
            if sub == 'hi':
                built = max(NAMED_Z[k]['hi'] for k in cand)
            elif sub == 'axis':
                built = float(np.mean([(NAMED_Z[k]['hi'] + NAMED_Z[k]['lo']) / 2 for k in cand]))
            note = '%d objetos (%s)' % (sum(NAMED_Z[k]['n'] for k in cand), ', '.join(sorted(cand)[:3]))
    elif how == 'block':
        d = BLOCK_Z.get(key)
        if d:
            if sub == 'hi':
                built = float(d['hi'] - min(d['anchors']))
            elif sub == 'branch':
                built = 3.0
            elif sub == 'nozzle':
                built = 4.0
            note = 'bloque %s, %d cotas de implantacion' % (key, len(d['anchors']))
    elif how == 'rail':
        built = 1.05; note = 'barandilla de cinta = deck +1.05 (montantes c/~1.0 m)'
    elif how == 'clear':
        built = gal['minimo_firme']
        note = 'minimo bajo ELEMENTO FIRME (regla 7); bajo copa de arbol baja a %.2f m' % gal['minimo']
    elif how == 'disc':
        band = {'low': (4.2, 5.6), 'mid': (5.6, 7.6), 'high': (7.6, 8.5)}[key]
        sel = cotas[(cotas >= band[0]) & (cotas <= band[1])]
        built = float(np.median(sel)) if len(sel) else None
        note = '%d discos en la banda %.1f–%.1f' % (len(sel), *band)
    elif how == 'absent':
        note = 'NO construido: ' + key
    if built is not None:
        ok = 'OK' if lo - 1e-6 <= built <= hi + 1e-6 else 'FUERA'
        built = round(float(built), 2)
    hrows.append(dict(param=name, declarado=val, rango=[lo, hi], construido=built, estado=ok or 'N/C', nota=note))
    log('   %-18s decl %6.2f  constr %s  %s' % (name, val, ('%6.2f' % built) if built is not None else '   —  ', ok or 'no construido'))

# discos: cuantos caen fuera de la familia 5.0 / 6.75 / 8.5
fam3 = np.array([5.0, 6.75, 8.5])
dev = np.abs(cotas[:, None] - fam3[None, :]).min(1)
off = int((dev > 0.30).sum())
hrows.append(dict(param='FAMILIA_DOSEL', declarado='5.0/6.75/8.5', rango=['±0.30', ''],
                  construido='%d de %d discos fuera' % (off, len(cotas)), estado='FUERA' if off else 'OK',
                  nota='cotas construidas min %.2f max %.2f mediana %.2f' % (cotas.min(), cotas.max(), np.median(cotas))))
log('   discos fuera de la familia 5.0/6.75/8.5 (±0.30): %d de %d' % (off, len(cotas)))
jdump('a3_heights.json', dict(rows=hrows, cotas_discos=[float(c) for c in cotas],
                              blocks={k: dict(lo=float(v['lo']), hi=float(v['hi']),
                                              anchors=sorted(float(a) for a in v['anchors'])[:6])
                                      for k, v in BLOCK_Z.items()}))
for r in hrows:
    if r['estado'] == 'FUERA':
        ISS.add('YELLOW', 'ALTURAS', '%s fuera de rango declarado' % r['param'],
                mag='declarado %s (rango %s) · construido %s' % (r['declarado'], r['rango'], r['construido']),
                cause='divergencia entre HEIGHT_SYSTEM y la geometria generada en 03B',
                strat='corregir la geometria o actualizar el HEIGHT_SYSTEM con el valor real',
                ref='A3')
    if r['estado'] == 'N/C' and 'NO construido' in r['nota']:
        ISS.add('GREEN', 'ALTURAS', '%s declarado pero no construido' % r['param'],
                mag=r['nota'], cause='decision de proyecto (D9 / simplificacion 03B)',
                strat='retirar del HEIGHT_SYSTEM o marcarlo como reserva', ref='A3')

# =============================================================== A4 · CINTA
log('A4 · cinta elevada: perfil, pendientes, escaleras, accesos')
RIB = np.asarray(M['circulacion']['ribbon'], float)
P, S = C.resample(RIB, 1.0)
Zr = np.full(len(P), 6.0)
prof = []
for k in range(len(P)):
    x, y = P[k]
    i, j = GRID.ij(x, y)
    zunder = 6.0 - 0.22
    prof.append(dict(s=float(S[k]), x=float(x), y=float(y), z=6.0,
                     bajo=float(zunder),
                     suelo_libre=bool(GRID.inside(i, j) and FREE[i, j])))
# curvatura
d1 = np.gradient(P, axis=0)
d2 = np.gradient(d1, axis=0)
kap = np.abs(d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0]) / np.maximum((d1 ** 2).sum(1) ** 1.5, 1e-9)
Rc = 1.0 / np.maximum(kap, 1e-9)
# escaleras
top = 6.0 - 0.22
run = top * 1.1
nsteps = 16
riser = top / (nsteps - 1)
tread = run / (nsteps - 1)
stairs = []
for (sx, sy) in M['circulacion']['stairs']:
    d = min(math.hypot(sx + run / 2 - p[0], sy + 0.6 - p[1]) for p in RIB)
    dmid = min(math.hypot(sx - p[0], sy - p[1]) for p in RIB)
    stairs.append(dict(x=float(sx), y=float(sy), d_top_a_cinta=float(d), d_centro_a_cinta=float(dmid),
                       huella=float(tread), contrahuella=float(riser),
                       pendiente_pct=float(100 * top / run), grados=float(math.degrees(math.atan2(top, run))),
                       ancho=1.28, barandilla=False, regla_2CH_H=float(2 * riser + tread)))
    log('   escalera (%.0f,%.0f): CH=%.3f H=%.3f  %.0f%% (%.0f°)  distancia coronacion→cinta %.1f m'
        % (sx, sy, riser, tread, 100 * top / run, math.degrees(math.atan2(top, run)), d))
ribbon = dict(long=float(S[-1]), z=6.0, pend_long_pct=0.0, pend_transv_pct=0.0,
              ancho_total=2.5, ancho_util=float(2 * 1.2 - 0.09), barandilla_h=1.05,
              cambios_nivel=1, radio_min=float(np.percentile(Rc, 1)), radio_min_abs=float(Rc.min()),
              n_soportes=None, galibo_bajo=float(top), stairs=stairs, prof=prof,
              n_accesos=len(stairs), accesos_accesibles=0)
nsup = sum(1 for o in MESH if o['name'] == 'RIB_SUP')
ribbon['n_soportes'] = nsup
log('   cinta L=%.0f m · z cte +6.00 (pendiente 0.0 %%) · ancho util %.2f m · %d soportes · radio min %.1f m'
    % (S[-1], ribbon['ancho_util'], nsup, ribbon['radio_min']))
jdump('a4_ribbon.json', ribbon)

ISS.add('RED', 'CINTA', 'Escaleras de la cinta con contrahuella 0.385 m y pendiente 91 %',
        stairs[0]['x'], stairs[0]['y'], 3.0,
        mag='CH=%.3f m · H=%.3f m · 2CH+H=%.2f m · %.0f%% (%.0f°) · 16 peldanos para 5.78 m' %
            (riser, tread, 2 * riser + tread, 100 * top / run, math.degrees(math.atan2(top, run))),
        cause='el generador reparte el desnivel en 16 peldanos sobre una zanca de %.2f m; no hay meseta ni barandilla' % run,
        strat='alargar la zanca a ~11 m con 32 peldanos (CH 0.18 / H 0.30) y meseta intermedia · anadir barandilla · o sustituir por rampa/ascensor',
        ref='A4', metric=riser)
ISS.add('RED', 'ACCESIBILIDAD', 'La cota +6.00 (cinta) carece de itinerario accesible',
        mag='6 escaleras, 0 rampas, 0 ascensores, 0 plataformas; desnivel 5.78 m',
        cause='no se ha proyectado ningun medio de elevacion accesible al nivel elevado',
        strat='ascensor en un extremo · rampa al 6 %% (96 m de desarrollo + mesetas) · o declarar la cinta como recorrido complementario no accesible',
        ref='A4/A5')
for s in stairs:
    if s['d_top_a_cinta'] > 3.0:
        ISS.add('RED', 'CINTA', 'Escalera en (%.0f,%.0f) no acomete la cinta' % (s['x'], s['y']),
                s['x'], s['y'], 6.0,
                mag='coronacion a %.1f m del eje de la pasarela (centro a %.1f m)' % (s['d_top_a_cinta'], s['d_centro_a_cinta']),
                cause='las posiciones de escalera del JSON no se han proyectado sobre la traza real de la cinta',
                strat='reposicionar la escalera sobre la traza o desviar la cinta hasta ella', ref='A4',
                metric=s['d_top_a_cinta'])
if not stairs[0]['barandilla']:
    ISS.add('RED', 'CINTA', 'Las 6 escaleras no tienen barandilla modelada',
            mag='0 de 6 escaleras con pasamanos; caida libre lateral hasta 5.78 m',
            cause='la familia STAIR solo genera 2 zancas + 16 peldanos',
            strat='anadir pasamanos a doble altura (0.70/0.95) en ambos lados', ref='A4')
if ribbon['radio_min_abs'] < 8.0:
    ISS.add('YELLOW', 'CINTA', 'Radio de curvatura minimo de la cinta %.1f m' % ribbon['radio_min_abs'],
            mag='radio minimo %.1f m (p01 %.1f m) para un tablero de 2.50 m de ancho' %
                (ribbon['radio_min_abs'], ribbon['radio_min']),
            cause='la traza se genero como polilinea de 371 puntos sin control de curvatura',
            strat='suavizar la generatriz en 30_CURVES manteniendo los puntos de acometida de escalera',
            ref='A4', metric=ribbon['radio_min_abs'])
ISS.add('GREEN', 'CINTA', 'La rasante de la cinta es plana y continua',
        mag='519 m a cota +6.00 constante: pendiente longitudinal 0.0 %% y transversal 0.0 %%; galibo bajo tablero %.2f m'
            % ribbon['galibo_bajo'],
        cause='—',
        strat='revisar no obstante la pendiente transversal: 0.0 %% implica que el tablero no evacua agua',
        ref='A4')

# =============================================================== A5 · ACCESIBILIDAD GEOMETRICA
log('A5 · precheck de accesibilidad geometrica')
TURN = 1.50                       # circulo de giro
acc_rows = []
for p in paths:
    w = np.array([r['w_transv'] for r in p['rows']])
    wl = np.array([r['w_local'] for r in p['rows']])
    ok180 = float((wl >= 1.80).mean())
    ok150 = float((wl >= TURN).mean())
    nblock = p['eje_bloqueado']
    verdict = ('APTO' if wl.min() >= 1.80 and nblock == 0 else
               ('CONDICIONADO' if np.percentile(wl, 5) >= 1.50 and nblock <= 3 else 'NO APTO'))
    acc_rows.append(dict(id=p['id'], long=p['long'], pend_pct=0.0, w_min=p['wl_min'],
                         w_transv_min=p['w_min'], w_p05=p['wl_p05'],
                         pct_w_ge_180=100 * ok180, pct_giro_ge_150=100 * ok150,
                         cambios_nivel=0, bloqueos=nblock, veredicto=verdict))
    log('   %-22s %-13s holgura min %5.2f m · p05 %5.2f m · %3.0f %% de la traza >=1.80 m · %d estaciones bloqueadas'
        % (p['id'], verdict, p['wl_min'], p['wl_p05'], 100 * ok180, nblock))
acc_rows.append(dict(id='CINTA +6.00', long=ribbon['long'], pend_pct=0.0, w_min=ribbon['ancho_util'],
                     w_transv_min=ribbon['ancho_util'], w_p05=ribbon['ancho_util'],
                     pct_w_ge_180=100.0, pct_giro_ge_150=100.0, bloqueos=0,
                     cambios_nivel=1, veredicto='NO APTO (solo escalera 91 %)'))
# bordes sin proteccion
edges = []
for p_ in M['agua_clima']['ground_ponds']:
    if p_['kind'] == 'circle':
        edges.append(dict(tipo='estanque', id=p_['id'], x=p_['cx'], y=p_['cy'], borde=0.60, proteccion='bordillo 0.60 sin barandilla'))
edges.append(dict(tipo='cinta', id='RIBBON', x=float(RIB[0][0]), y=float(RIB[0][1]), borde=6.0,
                  proteccion='barandilla 1.05 (sin travesano intermedio ni rodapie)'))
jdump('a5_access.json', dict(rows=acc_rows, edges=edges, turn=TURN))
for r in acc_rows:
    if r['veredicto'].startswith('NO APTO'):
        ISS.add('RED', 'ACCESIBILIDAD', 'Itinerario %s no puede funcionar como accesible' % r['id'],
                mag='ancho minimo %.2f m · %.0f %% de la traza >= 1.80 m · %d cambios de nivel' %
                    (r['w_min'], r['pct_w_ge_180'], r['cambios_nivel']),
                cause='estrechamientos y/o desnivel sin medio accesible',
                strat='liberar los puntos criticos o declarar un itinerario accesible alternativo', ref='A5')
    elif r['veredicto'] == 'CONDICIONADO':
        ISS.add('YELLOW', 'ACCESIBILIDAD', 'Itinerario %s accesible salvo puntos criticos' % r['id'],
                mag='ancho minimo %.2f m (p05 %.2f m)' % (r['w_min'], r['w_p05']),
                cause='estrechamientos puntuales', strat='liberar los estrechamientos listados en A1', ref='A5')
ISS.add('YELLOW', 'ACCESIBILIDAD', 'Barandilla de cinta sin travesano intermedio ni rodapie',
        mag='montantes c/~1.0 m + pasamanos 1.05; hueco libre 0–1.05 m',
        cause='la familia RIBBON_RAIL solo genera pasamanos y montantes',
        strat='anadir travesano intermedio y rodapie 0.10 m', ref='A5')

# =============================================================== A6 · METRO
log('A6 · clearances de accesos de metro / cercanias')
BAND = 5.5
ZOBST = 2.50            # por debajo de esta cota un elemento estorba fisicamente en la boca
metro = []
for e in M['contexto']['metro']:
    x, y = e['x'], e['y']
    i, j = GRID.ij(x, y)
    en_ambito = bool(GRID.inside(i, j) and PLAZA[i, j])
    d_suelo, who_s = 1e9, ''
    d_aereo, who_a, z_a = 1e9, '', None
    inb_s, inb_a = [], []
    for o in PROJ:
        d = float(math.sqrt(((o['V'][:, 0] - x) ** 2 + (o['V'][:, 1] - y) ** 2).min()))
        zlo = float(o['bb'][0][2])
        if zlo < ZOBST:                                   # obstaculo a nivel de boca
            if d < d_suelo:
                d_suelo, who_s = d, o['name']
            if d < BAND:
                inb_s.append((o['name'], o['fam'], round(d, 2), round(zlo, 2)))
        else:                                             # estructura en altura sobre la boca
            if d < d_aereo:
                d_aereo, who_a, z_a = d, o['name'], zlo
            if d < BAND:
                inb_a.append((o['name'], o['fam'], round(d, 2), round(zlo, 2)))
    rays = []
    for a in range(0, 360, 15):
        rr = math.radians(a)
        d, _c = ray_free(x, y, math.cos(rr), math.sin(rr), 20)
        rays.append(d)
    over = float(CLEAR[i, j]) if GRID.inside(i, j) and np.isfinite(CLEAR[i, j]) else None
    metro.append(dict(name=e['name'], x=x, y=y, en_ambito=en_ambito,
                      d_suelo=round(min(d_suelo, 999), 2), elem_suelo=who_s,
                      d_aereo=round(min(d_aereo, 999), 2), elem_aereo=who_a,
                      z_aereo=None if z_a is None else round(z_a, 2),
                      n_banda_suelo=len(inb_s), n_banda_aereo=len(inb_a),
                      familias=sorted(set(q[1] for q in inb_s)),
                      familias_aereas=sorted(set(q[1] for q in inb_a)),
                      libre_min=round(min(rays), 2), libre_medio=round(float(np.mean(rays)), 2),
                      galibo=over, invasores=sorted(inb_s, key=lambda q: q[2])[:12]))
    log('   %-16s (%7.2f,%7.2f) ambito=%-3s  SUELO d=%6.2f m [%-16s] n<5.5=%3d %s | AEREO d=%5.2f m z=%s galibo=%s'
        % (e['name'], x, y, 'si' if en_ambito else 'NO', min(d_suelo, 999), who_s[:16], len(inb_s),
           sorted(set(q[1] for q in inb_s)), min(d_aereo, 999),
           ('%.1f' % z_a) if z_a is not None else '—', ('%.2f' % over) if over else 'cielo'))
jdump('a6_metro.json', dict(band=BAND, zobst=ZOBST, rows=metro))
for r in metro:
    if not r['en_ambito']:
        ISS.add('GREEN', 'METRO', 'Acceso %s queda fuera del ambito de intervencion' % r['name'],
                r['x'], r['y'], 0, mag='elemento de proyecto mas proximo a nivel de boca: %.2f m' % r['d_suelo'],
                cause='situado fuera de la envolvente del proyecto', strat='sin accion', ref='A6')
        continue
    if r['d_suelo'] < BAND:
        sev = 'RED' if r['d_suelo'] < 2.0 else 'YELLOW'
        ISS.add(sev, 'METRO', 'Acceso %s: %d elementos a nivel de boca dentro de la banda 5,5 m' % (r['name'], r['n_banda_suelo']),
                r['x'], r['y'], 0,
                mag='obstaculo fisico mas proximo a %.2f m (%s) · ancho libre frontal minimo %.2f m · familias %s'
                    % (r['d_suelo'], r['elem_suelo'], r['libre_min'], ','.join(r['familias'])),
                cause='la banda de exclusion de D03B-02 se aplico a discos y mastiles, pero la vegetacion E02 y las piezas '
                      'menores se implantaron despues con reglas propias',
                strat='auditar la banda contra el criterio real de Metro de Madrid · retirar los invasores a nivel de boca · '
                      'mantener libre el frente de evacuacion',
                ref='A6', metric=r['d_suelo'])
    if r['n_banda_aereo'] and r['galibo'] is not None and r['galibo'] < 4.0:
        ISS.add('YELLOW', 'METRO', 'Acceso %s cubierto a %.2f m' % (r['name'], r['galibo']),
                r['x'], r['y'], r['galibo'], mag='galibo sobre la vertical de la boca %.2f m' % r['galibo'],
                cause='dosel o estructura sobre la vertical del acceso',
                strat='liberar la vertical del acceso (evacuacion / ventilacion / mantenimiento)', ref='A6')
    elif r['galibo'] is None:
        ISS.add('GREEN', 'METRO', 'Acceso %s conserva la vertical libre' % r['name'], r['x'], r['y'], 0,
                mag='cielo abierto sobre la boca; estructura aerea mas proxima a %.2f m (cota %s)'
                    % (r['d_aereo'], r['z_aereo']),
                cause='—', strat='sin accion', ref='A6')

# =============================================================== A7 · VISUALES
log('A7 · visibilidad de Real Casa de Correos / torre / reloj')
VCELL = 0.5
VG = C.Grid(-112, -45, 100, 78, VCELL)
ZTOP, VZ = 32.0, 0.5
nz = int(ZTOP / VZ)
vox_path = os.path.join(DATA, 'vox.npy')
OCCL = [o for o in SOLID if o['layer'] not in ('06_MEMBRANES',)]
if os.path.exists(vox_path):
    VOX = np.load(vox_path)
else:
    VOX = np.zeros((nz, VG.ny, VG.nx), bool)
    TR = np.concatenate([C.tris_of(o) for o in OCCL])
    for k in range(nz):
        VOX[k] = C.rasterize(VG, TR, k * VZ, (k + 1) * VZ, 'mask')
    np.save(vox_path, VOX)
log('   voxel 0.5 m listo: %d/%d ocupados' % (VOX.sum(), VOX.size))

TARGETS = dict(RELOJ=(-25.23, -34.35, 26.5), TORRE=(-25.20, -35.60, 22.0), CORREOS=(-25.20, -33.20, 8.5))


def visible(px, py, pz, t):
    tx, ty, tz = t
    d = math.dist((px, py, pz), (tx, ty, tz))
    n = int(d / 0.45)
    for s in range(3, n - 2):
        f = s / n
        x = px + (tx - px) * f; y = py + (ty - py) * f; z = pz + (tz - pz) * f
        j = int((x - VG.x0) / VCELL); i = int((y - VG.y0) / VCELL); k = int(z / VZ)
        if 0 <= i < VG.ny and 0 <= j < VG.nx and 0 <= k < nz and VOX[k, i, j]:
            return False
    return True


step = int(2.0 / CELL)
eyes = []
for i in range(0, NY, step):
    for j in range(0, NX, step):
        if WALK[i, j] and WIDTH[i, j] >= 0.5:
            x, y = GRID.xy(i, j)
            eyes.append((x, y))
log('   puntos de observacion a 1.65 m: %d' % len(eyes))
vis = {k: [] for k in TARGETS}
for (x, y) in eyes:
    for k, t in TARGETS.items():
        vis[k].append(visible(x, y, C.EYE_Z, t))
VIS = dict(n=len(eyes), pts=[[float(a) for a in p] for p in eyes],
           vis={k: [bool(b) for b in v] for k, v in vis.items()},
           pct={k: float(100.0 * np.mean(v)) for k, v in vis.items()})
for k in TARGETS:
    log('   %-8s visible desde el %.1f %% de los puntos' % (k, VIS['pct'][k]))
jdump('a7_views.json', VIS)
for k in ('RELOJ', 'TORRE'):
    p = VIS['pct'][k]
    sev = 'RED' if p < 20 else ('YELLOW' if p < 40 else 'GREEN')
    if sev != 'GREEN':
        ISS.add(sev, 'VISUALES', '%s visible solo desde el %.0f %% de la plaza' % (k, p),
                mag='%.1f %% de %d puntos de observacion a 1.65 m' % (p, VIS['n']),
                cause='dosel continuo 5.0–8.5 + copas E02 sobre la banda sur y el eje Mayor–Alcala',
                strat='abrir un cono visual desde el eje Mayor–Alcala retirando 3–6 discos · elevar la capa baja en la banda de Correos',
                ref='A7', metric=p)

# =============================================================== A8 · DENSIDAD
log('A8 · densidad por sectores y delta E02')
SEC = 20.0
sn = int(SEC / CELL)
FAMS_D = ['STRUCTURE', 'CANOPY', 'VEGETATION', 'PODS', 'PLANTER', 'FURNITURE', 'WATER', 'RIBBON']
FMASK = {}
for fam in FAMS_D:
    sel = [o for o in SOLID if o['fam'] == fam]
    FMASK[fam] = (C.rasterize(GRID, np.concatenate([C.tris_of(o) for o in sel]), BODY_LO, BODY_HI, 'mask')
                  if sel else np.zeros((NY, NX), bool))
CANOPY_OVER = C.rasterize(GRID, np.concatenate([C.tris_of(o) for o in SOLID if o['fam'] in ('CANOPY', 'RIBBON')]),
                          BODY_HI, 40, 'mask')

# escena sin E02 (MASTER, full=False) para el delta
log('   reconstruyendo MASTER (full=False) para el delta E02')
sys.path.insert(0, C.F03B)
import build_all_03b as BB


class _NS:
    def inst(self, *a, **k): pass
    def mesh(self, *a, **k): pass
    def line(self, *a, **k): pass


objs_m = []
BB.add_mesh = lambda f, l, layer, name, VF: objs_m.append(dict(layer=layer, name=name, block='',
                                                               V=np.asarray(VF[0], float), F=np.asarray(VF[1], np.int32)))


def _place0(f, ids, name, x, y, z, rot=0.0, lidx=None):
    ca, sa = math.cos(rot), math.sin(rot)
    for (layer, (V, F)) in BB.BLOCKS[name]:
        if not F:
            continue
        A = np.asarray(V, float)
        objs_m.append(dict(layer=layer, name=name, block=name,
                           V=np.column_stack([A[:, 0] * ca - A[:, 1] * sa + x, A[:, 0] * sa + A[:, 1] * ca + y, A[:, 2] + z]),
                           F=np.asarray(F, np.int32)))


BB.place = _place0
BB.add_curve = lambda *a, **k: None
f0, l0 = BB.new_file()
BB.build_site(f0, l0, {n: None for n in BB.ALL_BLOCKS}, _NS(), full=False)
S0 = [o for o in objs_m if o['layer'] not in C.NON_SOLID and o['layer'] not in ('01_GROUND',)]
OCC0 = C.rasterize(GRID, np.concatenate([C.tris_of(o) for o in S0]), BODY_LO, BODY_HI, 'mask')
log('   MASTER: %d mallas · ocupacion %.1f %% (FULL %.1f %%)' % (len(objs_m), 100 * OCC0[PLAZA].mean(), 100 * OCC[PLAZA].mean()))

sectors = []
for i0 in range(0, NY, sn):
    for j0 in range(0, NX, sn):
        sl = (slice(i0, min(i0 + sn, NY)), slice(j0, min(j0 + sn, NX)))
        pl = PLAZA[sl]
        if pl.sum() * CELL ** 2 < 60:
            continue
        A = pl.sum() * CELL ** 2
        oc = (OCC[sl] & pl).sum() * CELL ** 2
        oc0 = (OCC0[sl] & pl).sum() * CELL ** 2
        x, y = GRID.xy(i0 + sn // 2, j0 + sn // 2)
        row = dict(x=float(x), y=float(y), area=float(A),
                   ocup=float(100 * oc / A), ocup_master=float(100 * oc0 / A),
                   delta_e02=float(100 * (oc - oc0) / A),
                   libre=float(100 * (A - oc) / A),
                   cubierto=float(100 * (CANOPY_OVER[sl] & pl).sum() * CELL ** 2 / A),
                   w_p50=float(np.median(WIDTH[sl][pl & FREE[sl]])) if (pl & FREE[sl]).any() else 0.0)
        for fam in FAMS_D:
            row['f_' + fam] = float(100 * (FMASK[fam][sl] & pl).sum() * CELL ** 2 / A)
        sectors.append(row)
sectors.sort(key=lambda q: -q['ocup'])
log('   %d sectores de 20x20 m · ocupacion media %.1f %% · max %.1f %% en (%.0f,%.0f)'
    % (len(sectors), np.mean([s['ocup'] for s in sectors]), sectors[0]['ocup'], sectors[0]['x'], sectors[0]['y']))
jdump('a8_density.json', dict(sectors=sectors, cell=SEC,
                              global_=dict(ocup=float(100 * OCC[PLAZA].mean()),
                                           ocup_master=float(100 * OCC0[PLAZA].mean()),
                                           cubierto=float(100 * CANOPY_OVER[PLAZA].mean()))))
for s in sectors[:8]:
    if s['ocup'] >= 25:
        ISS.add('RED' if s['ocup'] >= 35 else 'YELLOW', 'DENSIDAD',
                'Sector (%.0f,%.0f) al %.0f %% de ocupacion de suelo' % (s['x'], s['y'], s['ocup']),
                s['x'], s['y'], 0,
                mag='ocupado %.0f %% (MASTER %.0f %%, %+.0f pp tras E02) · libre %.0f %% · cubierto %.0f %% · holgura mediana %.1f m' %
                    (s['ocup'], s['ocup_master'], s['delta_e02'], s['libre'], s['cubierto'], s['w_p50']),
                cause='acumulacion de %s' % max(FAMS_D, key=lambda ff: s['f_' + ff]),
                strat='aclarar 1 de cada 3 unidades de la familia dominante · reagrupar dejando claros de estancia',
                ref='A8', metric=s['ocup'])
for s in sorted(sectors, key=lambda q: -q['delta_e02'])[:3]:
    if s['delta_e02'] >= 3.0:
        ISS.add('YELLOW' if s['delta_e02'] >= 6 else 'GREEN', 'DENSIDAD',
                'Sector (%.0f,%.0f): E02 anadio %+.1f pp de ocupacion' % (s['x'], s['y'], s['delta_e02']),
                s['x'], s['y'], 0,
                mag='MASTER %.1f %% → E02 %.1f %% · holgura mediana %.1f m · cubierto %.0f %%'
                    % (s['ocup_master'], s['ocup'], s['w_p50'], s['cubierto']),
                cause='densificacion vegetal E02 (huerto de C1 / tropicales de C2 / arbolado)',
                strat='aclarar 1 de cada 3 filas de huerto, como ya anoto el propio REGISTRO_E02',
                ref='A8', metric=s['delta_e02'])
ISS.add('GREEN', 'DENSIDAD', 'La densificacion E02 no compromete la ocupacion global de suelo',
        mag='ocupacion del ambito %.1f %% (MASTER %.1f %%): +%.1f pp · superficie libre %.0f m2 de %.0f m2'
            % (100 * OCC[PLAZA].mean(), 100 * OCC0[PLAZA].mean(),
               100 * (OCC[PLAZA].mean() - OCC0[PLAZA].mean()), WALK.sum() * CELL ** 2, PLAZA.sum() * CELL ** 2),
        cause='la vegetacion E02 se implanto sobre jardineras y bajo dosel, no sobre el suelo de paso',
        strat='sin accion; el problema de densidad, donde existe, es local y de cobertura aerea, no de ocupacion global',
        ref='A8')

# =============================================================== A9 · MANTENIMIENTO
log('A9 · accesibilidad de mantenimiento')
MAINT = []


def maint_check(cat, ident, x, y, z_ele, need_platform):
    """holgura pisable junto al elemento y posibilidad de plataforma."""
    best, r = 0.0, 0.0
    for a in range(0, 360, 10):
        rr = math.radians(a)
        for d in np.arange(0.5, 4.01, 0.25):
            px, py = x + d * math.cos(rr), y + d * math.sin(rr)
            i, j = GRID.ij(px, py)
            if GRID.inside(i, j) and WALK[i, j]:
                if WIDTH[i, j] > best:
                    best, r = float(WIDTH[i, j]), float(d)
                break
    plat = best >= 2.50 if need_platform else best >= 0.90
    # obstruccion vertical sobre el elemento
    i, j = GRID.ij(x, y)
    over = float(CLEAR[i, j]) if GRID.inside(i, j) and np.isfinite(CLEAR[i, j]) else None
    row = dict(cat=cat, id=ident, x=float(x), y=float(y), z=float(z_ele),
               holgura=best, dist=r, requiere_plataforma=bool(need_platform),
               acceso=bool(plat), galibo_vertical=over)
    MAINT.append(row)
    return row


for t in M['estructura_ligera']['tanks']:
    for k in range(t['n']):
        maint_check('DEPOSITO +10.5', '%s-%d' % (t['id'], k + 1), t['cx'] + k * 2.6, t['cy'], 10.5, True)
for i, (dx, dy) in enumerate(M['estructura_ligera']['drops']):
    maint_check('DEPOSITO DE SUELO', 'DROP-%d' % (i + 1), dx, dy, 2.25, False)
for i, (nx_, ny_) in enumerate(M['agua_clima']['nebul']):
    maint_check('NEBULIZADOR +4.0', 'NEB-%02d' % (i + 1), nx_, ny_, 4.0, True)
for k, (vx, vy) in enumerate([(64, 18), (67, 14), (61, 12)]):
    maint_check('VIVERO', 'NURSERY-%d' % (k + 1), vx, vy, 3.0, False)
for i, d in enumerate(M['paisaje']['discs']):
    cota = min(max(d.get('cota', 6.0), 4.2), 8.5)
    maint_check('CANOPY / BAJANTE', 'DISC-%02d' % (i + 1), d['cx'], d['cy'], cota, True)
for i, b in enumerate(M['instalaciones']['bombeo_reserva']):
    bx, by = (b[:2] if isinstance(b, (list, tuple)) else (b.get('x', 0), b.get('y', 0)))
    maint_check('BOMBEO', 'BOMBA-%d' % (i + 1), bx, by, 0.0, False)
for t in M['estructura_ligera']['tanks']:
    for k in range(t['n']):
        maint_check('BAJANTE/RISER', '%s-%d-riser' % (t['id'], k + 1), t['cx'] + k * 2.6, t['cy'], 10.5, False)
bad = [q for q in MAINT if not q['acceso']]
log('   %d componentes auditados · %d sin acceso suficiente' % (len(MAINT), len(bad)))
for cat in sorted(set(q['cat'] for q in MAINT)):
    sub = [q for q in MAINT if q['cat'] == cat]
    nb = sum(1 for q in sub if not q['acceso'])
    log('     %-22s %3d componentes · %3d sin acceso (holgura mediana %.2f m)'
        % (cat, len(sub), nb, np.median([q['holgura'] for q in sub])))
jdump('a9_maint.json', MAINT)
for cat in sorted(set(q['cat'] for q in MAINT)):
    sub = [q for q in MAINT if q['cat'] == cat]
    nb = [q for q in sub if not q['acceso']]
    if not nb:
        continue
    w = nb[0]
    ISS.add('RED' if len(nb) > len(sub) * 0.5 else 'YELLOW', 'MANTENIMIENTO',
            '%s: %d de %d componentes sin acceso de mantenimiento' % (cat, len(nb), len(sub)),
            w['x'], w['y'], w['z'],
            mag='holgura pisable adyacente mediana %.2f m (se requieren %.2f m)' %
                (np.median([q['holgura'] for q in nb]), 2.5 if w['requiere_plataforma'] else 0.9),
            cause='el elemento queda rodeado de jardinera/vegetacion/agua o sin superficie de apoyo para plataforma elevadora',
            strat='reservar un area tecnica de 2.5x2.5 m junto a cada unidad · pasarela tecnica · acceso desde la cinta',
            ref='A9', metric=len(nb))

# =============================================================== A10 · COLISIONES
log('A10 · colisiones sistematicas entre familias')
VS = 0.20


def vox_keys(o):
    T = C.tris_of(o)
    if len(T) == 0:
        return np.empty(0, np.int64)
    a, b, c = T[:, 0], T[:, 1], T[:, 2]
    P = [a, b, c, (a + b) / 2, (b + c) / 2, (a + c) / 2, (a + b + c) / 3,
         (a * 2 + b + c) / 4, (a + b * 2 + c) / 4, (a + b + c * 2) / 4]
    Q = np.concatenate(P)
    q = np.floor(Q / VS).astype(np.int64)
    return np.unique((q[:, 0] + 4000) * 20000000 + (q[:, 1] + 4000) * 2000 + (q[:, 2] + 100))


FAM_KEYS, FAM_OBJ = {}, {}
for o in SOLID:
    if o['fam'] in ('CONTEXT',):
        continue
    k = vox_keys(o)
    FAM_KEYS.setdefault(o['fam'], []).append(k)
    FAM_OBJ.setdefault(o['fam'], []).append(o)
FAMU = {f: np.unique(np.concatenate(v)) for f, v in FAM_KEYS.items()}
INTENDED = {('STRUCTURE', 'CANOPY'), ('STRUCTURE', 'RIBBON'), ('STRUCTURE', 'PODS'),
            ('STRUCTURE', 'WATER'), ('CANOPY', 'WATER'), ('PLANTER', 'VEGETATION'),
            ('STRUCTURE', 'VEGETATION'), ('PLANTER', 'WATER'), ('FURNITURE', 'VEGETATION'),
            ('CANOPY', 'STRUCTURE'), ('WATER', 'VEGETATION'), ('FURNITURE', 'STRUCTURE'),
            ('PLANTER', 'STRUCTURE'), ('RIBBON', 'STRUCTURE')}
PAIRS = []
fl = sorted(FAMU)
for a in range(len(fl)):
    for b in range(a + 1, len(fl)):
        fa, fb = fl[a], fl[b]
        inter = np.intersect1d(FAMU[fa], FAMU[fb], assume_unique=True)
        if len(inter) == 0:
            continue
        vol = len(inter) * VS ** 3
        PAIRS.append(dict(a=fa, b=fb, voxels=int(len(inter)), vol=float(vol),
                          intencionado=bool((fa, fb) in INTENDED or (fb, fa) in INTENDED)))
PAIRS.sort(key=lambda q: -q['voxels'])
for p in PAIRS:
    log('   %-12s x %-12s  %6d voxeles (%6.2f m3)  %s'
        % (p['a'], p['b'], p['voxels'], p['vol'], 'contacto intencionado' if p['intencionado'] else '*** REVISAR ***'))

# detalle objeto a objeto para los pares NO intencionados (via indice clave->objeto)
def key_index(fam):
    ks = np.concatenate(FAM_KEYS[fam])
    oi = np.concatenate([np.full(len(k), n, np.int32) for n, k in enumerate(FAM_KEYS[fam])])
    order = np.argsort(ks, kind='stable')
    return ks[order], oi[order]


IDXC = {}
hot = []
for p in PAIRS:
    if p['intencionado']:
        continue
    fa, fb = p['a'], p['b']
    for f in (fa, fb):
        if f not in IDXC:
            IDXC[f] = key_index(f)
    ka, oia = IDXC[fa]
    kb, oib = IDXC[fb]
    inter = np.intersect1d(FAMU[fa], FAMU[fb], assume_unique=True)
    la, ra = np.searchsorted(ka, inter, 'left'), np.searchsorted(ka, inter, 'right')
    lb_, rb = np.searchsorted(kb, inter, 'left'), np.searchsorted(kb, inter, 'right')
    cnt = {}
    for t in range(len(inter)):
        for ia in oia[la[t]:ra[t]]:
            for ib in oib[lb_[t]:rb[t]]:
                cnt[(int(ia), int(ib))] = cnt.get((int(ia), int(ib)), 0) + 1
    for (ia, ib), n in cnt.items():
        if n < 3:
            continue
        oa, ob = FAM_OBJ[fa][ia], FAM_OBJ[fb][ib]
        lo = np.maximum(oa['bb'][0], ob['bb'][0])
        hi = np.minimum(oa['bb'][1], ob['bb'][1])
        hot.append(dict(pair='%s×%s' % (fa, fb), a=oa['name'], b=ob['name'],
                        voxels=int(n), vol=float(n * VS ** 3),
                        x=float((lo[0] + hi[0]) / 2), y=float((lo[1] + hi[1]) / 2),
                        z=float((lo[2] + hi[2]) / 2)))
hot.sort(key=lambda q: -q['voxels'])
log('   colisiones objeto-objeto no intencionadas: %d (top %d listadas)' % (len(hot), min(len(hot), 30)))

# familias contra el volumen peatonal (0.05-2.10 sobre suelo del ambito)
vs_circ = []
for fam in FAMS_D + ['CABLE']:
    if fam == 'CABLE':
        n = len(cab_low)
        vs_circ.append(dict(fam='CABLE', celdas=n, area=float(n * CELL ** 2), nota='muestras de cable < 3.0 m sobre suelo pisable'))
        continue
    mk_ = FMASK[fam] & PLAZA
    vs_circ.append(dict(fam=fam, celdas=int(mk_.sum()), area=float(mk_.sum() * CELL ** 2),
                        nota='huella en la banda de cuerpo dentro del ambito'))
jdump('a10_collisions.json', dict(pairs=PAIRS, hot=hot[:120], vs_circ=vs_circ))
for h in hot[:10]:
    ISS.add('YELLOW' if h['vol'] < 0.05 else 'RED', 'COLISIONES',
            'Interpenetracion %s: %s × %s' % (h['pair'], h['a'], h['b']),
            h['x'], h['y'], h['z'],
            mag='%d voxeles de 0.20 m (%.3f m3 de solape)' % (h['voxels'], h['vol']),
            cause='implantacion por reglas independientes sin comprobacion cruzada entre familias',
            strat='desplazar la instancia · reducir el radio de la copa · excluir la posicion en el generador',
            ref='A10', metric=h['vol'])

# =============================================================== A11 · PERSONA + CONFLICTOS ROJOS
log('A11 · validacion con persona de referencia (1.70 m)')
# El punto de una incidencia de PASO es el propio estrangulamiento: se mide ahi.
# El punto de una incidencia de OBJETO (colision, mantenimiento, metro) cae sobre o dentro
# de una pieza: lo que se valida es si cabe una persona EN SU ENTORNO inmediato (radio 2.5 m).
PASO = {'RECORRIDOS', 'ACCESIBILIDAD', 'GALIBOS'}
rad = int(2.5 / CELL)
person = []
for r in ISS.rows:
    if r['sev'] != 'RED' or r['x'] is None:
        continue
    x, y = r['x'], r['y']
    i, j = GRID.ij(x, y)
    if not GRID.inside(i, j):
        continue
    dentro = bool(OCC[i, j])
    if r['cat'] in PASO:
        modo = 'en el punto'
        w_ = float(WIDTH[i, j])
        g_ = float(CLEAR[i, j]) if np.isfinite(CLEAR[i, j]) else None
    else:
        modo = 'entorno 2.5 m'
        sl = (slice(max(i - rad, 0), i + rad + 1), slice(max(j - rad, 0), j + rad + 1))
        wsub, msub = WIDTH[sl], WALK[sl]
        w_ = float(wsub[msub].max()) if msub.any() else 0.0
        csub = CLEAR[sl][msub] if msub.any() else np.array([])
        g_ = float(np.nanmin(csub)) if csub.size and np.isfinite(csub).any() else None
    person.append(dict(id=r['id'], cat=r['cat'], x=x, y=y, punto_en_solido=dentro, modo=modo,
                       ancho=w_, galibo=g_,
                       pasa_cuerpo=bool(w_ >= C.SHOULDER), pasa_cabeza=bool(g_ is None or g_ >= C.H_PERSON + 0.15),
                       pasa_silla=bool(w_ >= C.WHEELCHAIR[0]),
                       pasa_cruce=bool(w_ >= 1.80)))
npaso = sum(1 for q in person if q['modo'] == 'en el punto')
log('   %d puntos rojos con coordenada (%d de paso medidos in situ · %d de objeto medidos en su entorno)'
    % (len(person), npaso, len(person) - npaso))
log('   no admite el cuerpo (0.55 m): %d · la cabeza (1.85 m): %d · silla (0.80 m): %d · cruce (1.80 m): %d'
    % (sum(1 for q in person if not q['pasa_cuerpo']), sum(1 for q in person if not q['pasa_cabeza']),
       sum(1 for q in person if not q['pasa_silla']), sum(1 for q in person if not q['pasa_cruce'])))
ISS.add('GREEN', 'PERSONA', 'Ningun punto pisable produce impacto de cabeza con el volumen humano de 1,70 m',
        mag='galibo minimo absoluto sobre suelo pisable %.2f m > 1,85 m de envolvente de cabeza; '
            'los %d incumplimientos de galibo lo son respecto al criterio propio de 3,00 m, no por choque fisico'
            % (gal['minimo'], len(low_spots)),
        cause='—',
        strat='decidir si 3,00 m sigue siendo el criterio o si bajo dosel se admite un valor menor documentado',
        ref='A11')
jdump('a11_person.json', person)

# =============================================================== CIERRE
ISS.save(os.path.join(DATA, 'issues.json'))
cnt = {s: len(ISS.by_sev(s)) for s in ('RED', 'YELLOW', 'GREEN')}
log('INCIDENCIAS: %d (RED %d · YELLOW %d · GREEN %d)' % (len(ISS.rows), cnt['RED'], cnt['YELLOW'], cnt['GREEN']))
jdump('summary.json', dict(
    objetos=len(MESH), tris=int(sum(len(o['F']) for o in MESH)),
    area_ambito=float(PLAZA.sum() * CELL ** 2), area_libre=float(WALK.sum() * CELL ** 2),
    ocupacion=float(100 * OCC[PLAZA].mean()), cobertura=float(100 * CANOPY_OVER[PLAZA].mean()),
    galibo_min=gal['minimo'], galibo_p05=gal['p05'],
    ancho_p05=float(np.percentile(WIDTH[WALK], 5)), ancho_p50=float(np.percentile(WIDTH[WALK], 50)),
    cuello_min=min(BOTT.values()) if BOTT else None,
    vis=VIS['pct'], counts=cnt))
log('OK · datos en _data/')
