# -*- coding: utf-8 -*-
"""Sondeo con NOMBRES: que objetos exactos penetran ECI(133)/Estanco(110) en v004."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', 'FASE_03A_MODELO_PROXY')))
import build_all_03b7 as B

OBJS = []


def _am(f, lidx, layer, name, VF):
    V, F = VF
    if F:
        OBJS.append((layer, name, V))


def _pl(f, ids, name, x, y, z, rot=0.0, lidx=None):
    ca, sa = math.cos(rot), math.sin(rot)
    for (layer, (V, F)) in B.BLOCKS[name]:
        if F:
            OBJS.append((layer, 'BLK:' + name, [(vx * ca - vy * sa + x, vx * sa + vy * ca + y, vz + z)
                                                for (vx, vy, vz) in V]))


CURVES = {}


def _ac(f, lidx, layer, name, pts):
    CURVES.setdefault(name, []).append([tuple(p) for p in pts])


B.add_mesh, B.place, B.add_curve = _am, _pl, _ac


class NS:
    def inst(self, *a, **k): pass
    def mesh(self, *a, **k): pass
    def line(self, *a, **k): pass


f, lidx = B.new_file()
ids = {n: None for n in B.ALL_BLOCKS}
B.build_site(f, lidx, ids, NS(), full=True)

POLY = {133: B.m['contexto']['buildings'][133]['pts'], 110: B.m['contexto']['buildings'][110]['pts'],
        106: B.m['contexto']['buildings'][106]['pts']}
HTOPE = {133: 99.0, 110: 4.1, 106: 6.5}
for bid, poly in POLY.items():
    print('=== edif', bid, '===')
    vistos = {}
    for (layer, name, V) in OBJS:
        if layer in ('00_CONTEXT', '01_GROUND', '17_METRO_CLEARANCES', '12_MIST', '16_PEOPLE_PROXY'):
            continue
        for v in V[::max(1, len(V) // 60)]:
            if v[2] > HTOPE[bid]:
                continue
            if B._pip(v[0], v[1], poly):
                d = B._edge_near(v[0], v[1], poly)[0]
                k = (layer, name)
                if k not in vistos or d > vistos[k][0]:
                    vistos[k] = (d, tuple(round(a, 1) for a in v))
                break
    for (layer, name), (d, ex) in sorted(vistos.items(), key=lambda kv: -kv[1][0]):
        print('  %-24s %-18s dep %.2f  ej %s' % (layer, name, d, ex))

print('\n=== anclajes STAIR/LIFT en GUARD_LOG ===')
for e in B.GUARD_LOG:
    if 'STAIR' in str(e.get('tag', '')) or 'LIFT' in str(e.get('tag', '')) or 'ANCLAJE' in str(e.get('regla', '')).upper():
        print('  ', e)

rax = CURVES.get('RIBBON_AXIS', [[]])[0]
eci = POLY[133]
print('\n=== eje de cinta vs ECI ===')
peor = None
for i, p in enumerate(rax):
    ins = B._pip(p[0], p[1], eci)
    d = B._edge_near(p[0], p[1], eci)[0]
    s = -d if ins else d
    if peor is None or s < peor[0]:
        peor = (s, i, (round(p[0], 1), round(p[1], 1)))
print('distancia firmada minima del EJE a ECI: %.2f m en idx %d %s (negativo = dentro)' % peor)
i0 = peor[1]
for j in range(max(0, i0 - 3), min(len(rax), i0 + 4)):
    print('   idx %3d (%7.2f, %6.2f)' % (j, rax[j][0], rax[j][1]))
