# -*- coding: utf-8 -*-
"""03B.8 §3 · PURGA GEOMETRICA FORENSE — escaner automatico sobre la escena interceptada.
Detecta: duplicados exactos, triangulos degenerados, micro-fragmentos, curvas casi-cero,
flotantes sin apoyo, enterrados, coplanaridad/z-fighting, curvas de construccion visibles.
Clasifica: CORRECTO / INTENCIONADO / SOSPECHOSO / ERROR. Salida: _purge_scan.json + resumen.
El criterio del enunciado: "NO EXISTE EL ERROR EN EL MODELO" (no basta con que no se vea)."""
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', 'FASE_03A_MODELO_PROXY')))
import build_all_03b8 as B  # noqa: E402

OBJS = []      # (layer, name, block, V, F)
CURVES = []    # (layer, name, pts)


def _am(f, lidx, layer, name, VF):
    V, F = VF
    if F:
        OBJS.append((layer, name, '', V, F))


_PL_SEEN = set()


def _pl(f, ids, name, x, y, z, rot=0.0, lidx=None):
    key = (name, round(x, 2), round(y, 2), round(z, 2), round(rot, 3))
    if key in _PL_SEEN:
        return          # mismo dedupe que place() real
    _PL_SEEN.add(key)
    ca, sa = math.cos(rot), math.sin(rot)
    for (layer, (V, F)) in B.BLOCKS[name]:
        if F:
            Vt = [(vx * ca - vy * sa + x, vx * sa + vy * ca + y, vz + z) for (vx, vy, vz) in V]
            OBJS.append((layer, name, name, Vt, F))


def _ac(f, lidx, layer, name, pts):
    CURVES.append((layer, name, [tuple(p) for p in pts]))


class NS:
    def inst(self, *a, **k): pass
    def mesh(self, *a, **k): pass
    def line(self, *a, **k): pass


B.add_mesh, B.place, B.add_curve = _am, _pl, _ac
f, lidx = B.new_file()
B.build_site(f, lidx, {n: None for n in B.ALL_BLOCKS}, NS(), full=True)
print('escena interceptada: %d mallas, %d curvas' % (len(OBJS), len(CURVES)))

R = {'duplicados': [], 'degenerados': [], 'micro': [], 'curvas_cero': [],
     'flotantes': [], 'enterrados': [], 'zfight': [], 'curvas_visibles': []}

# ---------- bbox por objeto ----------
META = []
for i, (layer, name, blk, V, F) in enumerate(OBJS):
    xs = [v[0] for v in V]; ys = [v[1] for v in V]; zs = [v[2] for v in V]
    META.append(dict(i=i, layer=layer, name=name, blk=blk,
                     bb=(min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)),
                     nv=len(V), nf=len(F)))

# ---------- 1 · duplicados exactos (mismo layer + malla identica redondeada a 1 cm) ----------
seen = {}
for mt in META:
    layer, name, _b, V, F = OBJS[mt['i']]
    h = hashlib.md5()
    h.update(layer.encode())
    for v in V:
        h.update(b'%d,%d,%d;' % (round(v[0] * 100), round(v[1] * 100), round(v[2] * 100)))
    k = h.hexdigest()
    if k in seen:
        R['duplicados'].append(dict(i=mt['i'], name=name, layer=layer, igual_a=seen[k],
                                    bb=[round(q, 2) for q in mt['bb']], clase='ERROR'))
    else:
        seen[k] = dict(i=mt['i'], name=name)

# ---------- 2 · triangulos degenerados / micro-objetos ----------
for mt in META:
    layer, name, _b, V, F = OBJS[mt['i']]
    ndeg = 0
    for tri in F[:4000]:
        try:
            a, b, c = V[tri[0]], V[tri[1]], V[tri[2]]
        except Exception:
            ndeg += 1
            continue
        ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
        vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
        cxp = (uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx)
        if math.sqrt(cxp[0] ** 2 + cxp[1] ** 2 + cxp[2] ** 2) < 1e-9:
            ndeg += 1
    if ndeg:
        es_asset = str(name).startswith('VEGA_')
        if es_asset:
            clase, nota = 'INTENCIONADO', 'sliver de fotoescaneo (asset externo)'
        elif ndeg <= max(6, int(0.25 * max(len(F), 1))):
            clase, nota = 'INTENCIONADO', 'costura polar de primitiva (esfera/cono del kit de mallas)'
        else:
            clase, nota = 'ERROR', ''
        R['degenerados'].append(dict(i=mt['i'], name=name, layer=layer, tris_degenerados=ndeg,
                                     clase=clase, nota=nota))
    bb = mt['bb']
    diag = math.sqrt((bb[3] - bb[0]) ** 2 + (bb[4] - bb[1]) ** 2 + (bb[5] - bb[2]) ** 2)
    if diag < 0.015:
        R['micro'].append(dict(i=mt['i'], name=name, layer=layer, diag=round(diag, 4), clase='ERROR'))

# ---------- 3 · curvas casi-cero y curvas de construccion visibles ----------
for (layer, name, pts) in CURVES:
    L = sum(math.sqrt((pts[k + 1][0] - pts[k][0]) ** 2 + (pts[k + 1][1] - pts[k][1]) ** 2
                      + ((pts[k + 1][2] if len(pts[k + 1]) > 2 else 0) - (pts[k][2] if len(pts[k]) > 2 else 0)) ** 2)
            for k in range(len(pts) - 1))
    if L < 0.02:
        R['curvas_cero'].append(dict(name=name, layer=layer, L=round(L, 4), clase='ERROR'))
    if name.startswith('EST_RESPETO') or 'GUIDE' in name.upper() or 'AUX' in name.upper():
        R['curvas_visibles'].append(dict(name=name, layer=layer, clase='ERROR',
                                         nota='curva de analisis/construccion en capa visible'))

# ---------- 4 · flotantes (sin nada debajo) y enterrados — por INSTANCIA de bloque, no por pieza
AER = {'05_CABLES', '06_MEMBRANES', '07_CANOPIES', '12_MIST', '17_METRO_CLEARANCES'}
COLG = ('VEG2_COLGANTE', 'VEGA_POTHOS', 'NET', 'COLG', 'LEAF', 'TANK', 'CBL', 'DROP')
GRUPOS = {}
for mt in META:
    layer, name, blk, V, F = OBJS[mt['i']]
    if blk:
        k = (blk, round(mt['bb'][0], 1), round(mt['bb'][1], 1) if False else None)
        # agrupar por instancia: ancla aproximada = min de bbox del conjunto no disponible;
        # usamos el nombre de bloque + celda de 2 m del centro
        cx = (mt['bb'][0] + mt['bb'][3]) / 2
        cy = (mt['bb'][1] + mt['bb'][4]) / 2
        k = (blk, int(cx / 2.0), int(cy / 2.0))
    else:
        k = ('#%d' % mt['i'], 0, 0)
    G = GRUPOS.setdefault(k, dict(layer=layer, name=name, blk=blk, bb=list(mt['bb'])))
    for j2 in range(3):
        G['bb'][j2] = min(G['bb'][j2], mt['bb'][j2])
        G['bb'][j2 + 3] = max(G['bb'][j2 + 3], mt['bb'][j2 + 3])

for k, G in GRUPOS.items():
    layer, name, blk, bb = G['layer'], G['name'], G['blk'], G['bb']
    if layer in ('00_CONTEXT', '01_GROUND') or layer in AER:
        continue
    if bb[5] < -0.05:
        R['enterrados'].append(dict(name=name, layer=layer, ztop=round(bb[5], 2), clase='ERROR'))
        continue
    if bb[2] > 0.12 and not any((name or '').startswith(c) or (blk or '').startswith(c) for c in COLG):
        cx, cy = (bb[0] + bb[3]) / 2, (bb[1] + bb[4]) / 2
        apoyo = False
        for k2, G2 in GRUPOS.items():
            if k2 == k:
                continue
            b2 = G2['bb']
            if (b2[0] - 0.35 < cx < b2[3] + 0.35 and b2[1] - 0.35 < cy < b2[4] + 0.35
                    and b2[2] < bb[2] + 0.06 and b2[5] > bb[2] - 0.9):
                apoyo = True
                break
        if not apoyo:
            R['flotantes'].append(dict(name=name, layer=layer, blk=blk,
                                       zmin=round(bb[2], 2), xy=[round(cx, 1), round(cy, 1)],
                                       clase='SOSPECHOSO' if bb[2] > 2.0 else 'ERROR'))

# ---------- 5 · z-fighting: chapas horizontales coplanares que se solapan ----------
def _area_2d(mt):
    """area real proyectada (aprox) — para descartar falsos positivos de mallas ANULARES."""
    layer, name, blk, V, F = OBJS[mt['i']]
    s = 0.0
    for tri in F[:2500]:
        a, b, c = V[tri[0]], V[tri[1]], V[tri[2]]
        s += abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) / 2
    return s


finas = []
for mt in META:
    if ((mt['bb'][5] - mt['bb'][2]) < 0.035
            and (mt['bb'][3] - mt['bb'][0]) > 0.4 and (mt['bb'][4] - mt['bb'][1]) > 0.4):
        bbarea = (mt['bb'][3] - mt['bb'][0]) * (mt['bb'][4] - mt['bb'][1])
        if _area_2d(mt) > 0.30 * bbarea:      # anillos/tubos en planta: fuera del detector
            finas.append(mt)
for a in range(len(finas)):
    for b2 in range(a + 1, len(finas)):
        A, Bm = finas[a], finas[b2]
        if abs(A['bb'][2] - Bm['bb'][2]) > 0.006 and abs(A['bb'][5] - Bm['bb'][5]) > 0.006:
            continue
        ox = min(A['bb'][3], Bm['bb'][3]) - max(A['bb'][0], Bm['bb'][0])
        oy = min(A['bb'][4], Bm['bb'][4]) - max(A['bb'][1], Bm['bb'][1])
        if ox > 0.3 and oy > 0.3:
            R['zfight'].append(dict(a=OBJS[A['i']][1] or A['layer'], b=OBJS[Bm['i']][1] or Bm['layer'],
                                    la=A['layer'], lb=Bm['layer'],
                                    z=round(A['bb'][2], 3), solape_m2=round(ox * oy, 2),
                                    xy=[round((A['bb'][0] + A['bb'][3]) / 2, 1),
                                        round((A['bb'][1] + A['bb'][4]) / 2, 1)],
                                    clase='ERROR'))

json.dump(R, open(os.path.join(HERE, '_purge_scan.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('=== PURGE SCAN ===')
for k, v in R.items():
    ne = sum(1 for q in v if q.get('clase') == 'ERROR')
    print('%-16s %4d (%d ERROR)' % (k, len(v), ne))
tot_err = sum(1 for v in R.values() for q in v if q.get('clase') == 'ERROR')
print('TOTAL ERROR:', tot_err)
