# -*- coding: utf-8 -*-
"""03B.7 §27 · METRICAS DE DETALLE v003 -> v004, medidas (no estimadas):
  - escena horneada: objetos, triangulos, por capa y por familia
  - biblioteca: familias de bloque y PIEZAS por bloque (antes/despues del upgrade)
  - conexiones legibles: pletinas, abrazaderas, pernos, manguitos, valvulas, sumideros...
Salida: METRICAS_DETALLE_v004.json + resumen por stdout."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V3V = os.path.normpath(os.path.join(HERE, '..', 'FASE_03B6_RESOLUCION', '_viewer', 'scene_full.js'))
V4V = os.path.join(HERE, '_viewer', 'scene_full.js')


def load(p):
    txt = open(p, encoding='utf-8').read()
    a = txt.index('const SCENE_MESHES = ') + len('const SCENE_MESHES = ')
    MS = json.loads(txt[a:txt.index(';\nconst SCENE_LINES')])
    b = txt.index('const SCENE_LINES = ') + len('const SCENE_LINES = ')
    tail = txt[b:]
    LN = json.loads(tail[:tail.index(';\n')])
    return MS, LN


def stats(MS, LN):
    per_layer = {}
    per_fam = {}
    tris = 0
    for o in MS:
        nt = len(o['F'])
        tris += nt
        L = per_layer.setdefault(o['layer'], [0, 0])
        L[0] += 1; L[1] += nt
        fam = o.get('fam') or o.get('name') or '?'
        fam = re.sub(r'_\d+.*$', '', str(fam))
        per_fam[fam] = per_fam.get(fam, 0) + 1
    return dict(objetos=len(MS), tris=tris, lineas=len(LN),
                por_capa={k: dict(n=v[0], tris=v[1]) for k, v in sorted(per_layer.items())},
                familias=len(per_fam),
                por_familia=dict(sorted(per_fam.items(), key=lambda kv: -kv[1])))


M3, L3 = load(V3V)
M4, L4 = load(V4V)
S3, S4 = stats(M3, L3), stats(M4, L4)

# ---- biblioteca de bloques v004 (piezas por familia tras el upgrade) ----
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', 'FASE_03A_MODELO_PROXY')))
cwd = os.getcwd()
os.chdir(HERE)
import build_all_03b7 as B  # noqa: E402
os.chdir(cwd)
piezas = {k: len(v) for k, v in sorted(B.BLOCKS.items())}

# ---- conexiones/elementos LOD B-C: por NOMBRE real, interceptando el generador ----
NOBJ = []


def _am(f, lidx, layer, name, VF):
    NOBJ.append(name)


def _pl(f, ids, name, x, y, z, rot=0.0, lidx=None):
    NOBJ.append('BLK:' + name)


def _ac(f, lidx, layer, name, pts):
    pass


class _NS:
    def inst(self, *a, **k): pass
    def mesh(self, *a, **k): pass
    def line(self, *a, **k): pass


B.add_mesh, B.place, B.add_curve = _am, _pl, _ac
f2, l2 = B.new_file()
B.build_site(f2, l2, {n: None for n in B.ALL_BLOCKS}, _NS(), full=True)

CONX = {}
CLAVES = ('PLETINA', 'PERNO', 'ABRAZ', 'MANGUITO', 'VALVULA', 'SUMIDERO', 'GOTERON', 'CANALETA',
          'JUNTA', 'LUMINARIA', 'REGISTRO', 'ALCORQUE', 'NARIZ', 'MONTANTE', 'REJILLA', 'BOTONERA',
          'GARGOLA', 'PENDOLA', 'MECHINAL', 'VERJA', 'TENSOR', 'KINGPOST', 'FASCIA', 'LED', 'APRON')
for nm in NOBJ:
    u = str(nm).upper()
    for c in CLAVES:
        if c in u:
            CONX[c] = CONX.get(c, 0) + 1
            break

R = dict(v003=dict(objetos=S3['objetos'], tris=S3['tris'], lineas=S3['lineas'], familias=S3['familias'],
                   por_capa=S3['por_capa']),
         v004=dict(objetos=S4['objetos'], tris=S4['tris'], lineas=S4['lineas'], familias=S4['familias'],
                   por_capa=S4['por_capa'], por_familia_top40=dict(list(S4['por_familia'].items())[:40])),
         delta=dict(objetos=S4['objetos'] - S3['objetos'], tris=S4['tris'] - S3['tris'],
                    familias=S4['familias'] - S3['familias']),
         piezas_por_bloque=piezas,
         conexiones_lod_bc=dict(sorted(CONX.items(), key=lambda kv: -kv[1])))
json.dump(R, open(os.path.join(HERE, 'METRICAS_DETALLE_v004.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

print('v003: %d obj · %d tris · %d familias' % (S3['objetos'], S3['tris'], S3['familias']))
print('v004: %d obj · %d tris · %d familias' % (S4['objetos'], S4['tris'], S4['familias']))
print('delta: +%d obj · +%d tris · +%d familias' % (R['delta']['objetos'], R['delta']['tris'], R['delta']['familias']))
print('capa 19_DETALLE:', S4['por_capa'].get('19_DETALLE'))
print('conexiones LOD B/C:', R['conexiones_lod_bc'])
print('bloques con mas piezas:', dict(sorted(piezas.items(), key=lambda kv: -kv[1])[:12]))
