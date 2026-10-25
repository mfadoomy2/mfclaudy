# -*- coding: utf-8 -*-
"""6 secciones arquitectonicas desde scene_full.js -> SVG (1:200 en A1) + PDF."""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
raw = open(os.path.join(HERE, '_viewer', 'scene_full.js'), encoding='utf-8').read()
MESHES = json.loads(raw.split('const SCENE_MESHES = ')[1].split(';')[0])

OUT = os.path.join(HERE, 'secciones')
os.makedirs(OUT, exist_ok=True)

COL = {
    '00_CONTEXT': '#B5B1A9', '01_GROUND': '#8E8A82', '02_PRIMARY_STRUCTURE': '#8A5A2B',
    '03_SECONDARY_STRUCTURE': '#A87840', '04_MASTS': '#96683A', '06_MEMBRANES': '#9DB8A0',
    '07_CANOPIES': '#6E8B3D', '08_PINK_MODULES': '#D6577F', '09_PLANTERS': '#4E7040',
    '10_FURNITURE': '#8A5A2B', '11_WATER': '#2F7D57', '12_MIST': '#8FC7AE',
    '13_PIPES': '#D6577F', '14_VEGETATION_PROXY': '#5E9C55', '15_VEGETATION_FULL': '#4E8446',
    '16_PEOPLE_PROXY': '#33322E', '17_METRO_CLEARANCES': '#5B5B8F',
}
LEVELS = [(0, '±0.00'), (3.0, '+3.00 gálibo'), (5.0, '+5.00 dosel bajo'), (6.0, '+6.00 cinta'),
          (6.75, '+6.75 dosel medio'), (8.5, '+8.50 dosel alto'), (10.5, '+10.50 depósitos')]

SECS = [
    ('S01_LONG_y8', 'y', 8.0, +1, 'SECCIÓN LONGITUDINAL S01 · y=+8 · mirando al norte', (-100, 95), 18),
    ('S02_LONG_y-12', 'y', -12.0, -1, 'SECCIÓN LONGITUDINAL S02 · y=−12 · eje Mayor–Alcalá mirando al sur (Casa de Correos al fondo)', (-100, 95), 30),
    ('S03_TRANS_x-52', 'x', -52.0, -1, 'SECCIÓN TRANSVERSAL S03 · x=−52 · clúster C1', (-45, 70), 16),
    ('S04_TRANS_x8', 'x', 8.0, +1, 'SECCIÓN TRANSVERSAL S04 · x=+8 · nudo C2, anillo doble', (-45, 70), 16),
    ('S05_TRANS_x30', 'x', 30.5, +1, 'SECCIÓN TRANSVERSAL S05 · x=+30.5 · cúpula-pérgola y lámina jugable', (-45, 70), 16),
    ('S06_TRANS_x56', 'x', 56.0, +1, 'SECCIÓN TRANSVERSAL S06 · x=+56 · clúster C3, balsas y viveros', (-45, 70), 16),
]

SC = 3.0   # mm por metro (1:200 aprox en A1 seria 4.2; usamos 3.0 para que quepan 195 m)


def section(name, axis, val, sign, title, ext, depth):
    ai = 0 if axis == 'x' else 1   # eje de corte
    hi = 1 if axis == 'x' else 0   # eje horizontal del dibujo
    cuts = {}
    beyond = []
    for o in MESHES:
        V = o['V']
        F = o['F']
        lay = o['layer']
        for (a, b, c) in F:
            va, vb, vc = V[a], V[b], V[c]
            ds = [va[ai] - val, vb[ai] - val, vc[ai] - val]
            neg = sum(1 for d in ds if d < 0)
            if 0 < neg < 3:
                seg = []
                tri = [va, vb, vc]
                for i in range(3):
                    j = (i + 1) % 3
                    d0, d1 = ds[i], ds[j]
                    if (d0 < 0) != (d1 < 0):
                        t = d0 / (d0 - d1)
                        p = [tri[i][k] + (tri[j][k] - tri[i][k]) * t for k in range(3)]
                        seg.append((p[hi], p[2]))
                if len(seg) == 2:
                    cuts.setdefault(lay, []).append(seg)
            elif all(0 < d * sign <= depth for d in ds):
                if (a + b) % 3 == 0:   # submuestreo del alzado
                    beyond.append(((va[hi], va[2]), (vb[hi], vb[2])))

    x0, x1 = ext
    W = (x1 - x0) * SC + 70
    Hmm = 34 * SC + 46
    S = ['<svg xmlns="http://www.w3.org/2000/svg" width="%.0fmm" height="%.0fmm" viewBox="0 0 %.0f %.0f" font-family="Arial">' % (W, Hmm, W, Hmm)]
    S.append('<rect width="%.0f" height="%.0f" fill="#FFFFFF"/>' % (W, Hmm))

    def T(h, z):
        return (35 + (h - x0) * SC, Hmm - 28 - z * SC)

    # niveles
    for (z, lbl) in LEVELS:
        p0, p1 = T(x0, z), T(x1, z)
        S.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#D6577F" stroke-width="0.09" stroke-dasharray="2.4 1.6" opacity="0.7"/>' % (p0[0], p0[1], p1[0], p1[1]))
        S.append('<text x="%.1f" y="%.1f" font-size="2.2" fill="#D6577F" font-family="Consolas">%s</text>' % (p1[0] + 1.5, p1[1] + 0.7, lbl))
    # alzado en profundidad
    S.append('<g stroke="#C9C4BB" stroke-width="0.05" opacity="0.55">')
    for ((h0, z0), (h1, z1)) in beyond:
        if x0 - 2 < h0 < x1 + 2 and x0 - 2 < h1 < x1 + 2 and z0 < 33 and z1 < 33:
            p0, p1 = T(h0, z0), T(h1, z1)
            S.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (p0[0], p0[1], p1[0], p1[1]))
    S.append('</g>')
    # cortes por familia
    for lay, segs in cuts.items():
        col = COL.get(lay, '#333')
        w = 0.55 if lay in ('02_PRIMARY_STRUCTURE', '00_CONTEXT', '01_GROUND') else 0.35
        S.append('<g stroke="%s" stroke-width="%.2f" stroke-linecap="round">' % (col, w))
        for ((h0, z0), (h1, z1)) in segs:
            if x0 - 2 < h0 < x1 + 2 and z0 < 33 and z1 < 33:
                p0, p1 = T(h0, z0), T(h1, z1)
                S.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (p0[0], p0[1], p1[0], p1[1]))
        S.append('</g>')
    # suelo
    p0, p1 = T(x0, 0), T(x1, 0)
    S.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#33322E" stroke-width="0.7"/>' % (p0[0], p0[1], p1[0], p1[1]))
    # titulo + escala
    S.append('<text x="35" y="12" font-size="5.2" fill="#33322E" font-family="Bahnschrift" letter-spacing="1">%s</text>' % title)
    S.append('<text x="35" y="17.5" font-size="2.6" fill="#8a877f" font-family="Consolas">corte por familias · alzado %d m en gris · niveles HEIGHT_SYSTEM · 1:333 en este pliego · fuente SOL_FULL_SCENE_v001</text>' % depth)
    bx = T(x0, 0)[0]
    by = Hmm - 10
    S.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#33322E" stroke-width="0.35"/>' % (bx, by, bx + 20 * SC, by))
    for k in (0, 5, 10, 20):
        S.append('<text x="%.1f" y="%.1f" font-size="2.2" fill="#33322E">%d</text>' % (bx + k * SC - 1, by + 3.4, k))
    S.append('</svg>')
    open(os.path.join(OUT, name + '.svg'), 'w', encoding='utf-8').write('\n'.join(S))
    ncuts = sum(len(v) for v in cuts.values())
    print(name, 'cortes:', ncuts, 'alzado:', len(beyond))
    return W, Hmm


dims = []
for sec in SECS:
    dims.append(section(*sec))

# PDF: 3 paginas A1 apaisadas, 2 secciones por pagina
pages = ''
for i in range(0, 6, 2):
    imgs = ''
    for j in (i, i + 1):
        svg = open(os.path.join(OUT, SECS[j][0] + '.svg'), encoding='utf-8').read()
        imgs += '<div class="sec">%s</div>' % svg
    pages += '<div class="page">%s</div>' % imgs
html = '''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page { size: 841mm 594mm; margin: 0; }
body { margin: 0; }
.page { width: 841mm; height: 594mm; page-break-after: always; padding: 12mm; box-sizing: border-box; }
.sec { margin-bottom: 8mm; }
svg { display: block; }
</style></head><body>''' + pages + '</body></html>'
src = os.path.join(OUT, '_secciones_src.html')
open(src, 'w', encoding='utf-8').write(html)
out = os.path.join(HERE, 'SECCIONES_03B.pdf')
subprocess.run([r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', '--headless=new', '--disable-gpu',
                '--no-pdf-header-footer', '--print-to-pdf=' + out, 'file:///' + src.replace('\\', '/')],
               capture_output=True, timeout=300)
print('PDF:', os.path.exists(out), os.path.getsize(out) if os.path.exists(out) else 0)
