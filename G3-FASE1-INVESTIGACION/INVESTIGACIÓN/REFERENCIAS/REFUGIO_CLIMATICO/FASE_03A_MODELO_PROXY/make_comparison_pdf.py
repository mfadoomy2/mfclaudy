# -*- coding: utf-8 -*-
"""PILOT_REFERENCE_COMPARISON.pdf — referencia vs modelo, 8 pares, A3 apaisado."""
import base64
import io
import os
import subprocess

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.normpath(os.path.join(HERE, '..', '..', 'MONTESERIN IA', 'MONTESERIN IA', 'MUTACIONES (DIBUJO + IA)',
                                    'DIBUJO3 (REFUGIO CLIMATICO)', 'IN PROGRESS REFUGIO'))
VP = os.path.join(HERE, 'vistas_piloto')


def b64(p, maxw=980):
    im = Image.open(p)
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)))
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=80)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


PAIRS = [
    ('VISTA01_recorrido', '79405914-2F38-4010-839D-B75F373FDA46.png',
     'Escala y altura del dosel coinciden (capa baja ~5 m sobre el eje). Densidad del modelo algo menor (proxy sin follaje). Materialidad pendiente: en render, membranas celulares; en proxy, discos rígidos. Tipo de espacio: eje sombreado flanqueado por masas — CORRECTO.'),
    ('VISTA02_bajo_hojas', '29A08040-DD59-4509-BB21-0735BF86DAEB.png',
     'El techo escalonado de discos (5/6.75/8.5) reproduce la lógica de capas del render. Relación humano-estructura correcta: mástiles c/4-6 m, ramificación a 3 m. Falta la vibración del rosa serpenteante entre estructura (Fase 03B).'),
    ('VISTA03_estancia', '12CA810C-437B-41C2-B54C-62B449F8FD7B.png',
     'Bancos-isla curvos con respaldo a 0.45/0.85 y cubas con mástil integrado = misma familia del render. El salón queda más abierto en proxy (sin vegetación densa). Paso entre islas 3-5 m: COINCIDE.'),
    ('VISTA04_capsulas', '1C334300-C51E-4D66-BF25-0FA619020673.png',
     'Racimo de esferas Ø2.5-4 con gajos y válvula, mezcla suelo/colgadas: coincide en escala (2 alturas de persona) y en posición del racimo N de C2. En render las esferas se apilan más denso y llevan vegetación interior (Tripo héroe en 03B).'),
    ('VISTA05_veg_estructura', '999C4F45-0B15-493F-BE41-8A7732CCF2E2.png',
     'Haz de anillos elevados + discos + cables reproducen el sistema aéreo; el suelo queda libre igual que en el render. Altura del anillo (9-11) coherente con los anillos apilados del render. Falta trepadora vertical (asset 03B).'),
    ('VISTA06_hacia_correos', '24D82F58-281B-4FED-8CDF-058C0BCA7257.png',
     'NOTA: el fragmento aislado no incluye contexto, la Casa de Correos no aparece (validada en V07 del proxy completo). La estratificacion huerto/tubos/pasarela del render coincide en cotas: suelo productivo, red a 3.5-6, deck a 6.'),
    ('VISTA07_elevada', '2187306B-96B2-4FC4-91A2-4E0DE1C110B1.png',
     'Desde +7.4 la cinta serpentea entre discos como la cinta blanca del render (transitable, ~2.5 m de ancho, barandilla 1.05). Densidad de dosel comparable; el proxy revela el orden radial de nervios que el render insinúa.'),
    ('VISTA08_axonometria', 'F295448F-64C4-4AE3-A230-C56C8776C3F6.png',
     'El nudo C2 en axonometría: anillo doble + corona de discos + racimo rosa + cinta = misma anatomía que el nudo central de la aérea de referencia. Proporción disco/anillo y cadencia de mástiles coherentes.'),
]

rows = ''
for i, (v, ref, note) in enumerate(PAIRS):
    rows += '''<div class="pair%s"><div class="col"><p class="tag">REFERENCE · %s</p><img src="%s"></div>
    <div class="col"><p class="tag">3D MODEL · %s</p><img src="%s"></div>
    <p class="note">%s</p></div>''' % (
        ' brk' if i % 2 == 0 and i > 0 else '', ref[:8], b64(os.path.join(REF, ref)),
        v, b64(os.path.join(VP, v + '.png')), note)

html = '''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page { size: 420mm 297mm; margin: 0; }
body { font-family: Bahnschrift, Arial; margin: 0; color: #33322E; }
.hdr { padding: 12mm 16mm 4mm; }
.kicker { color: #D6577F; letter-spacing: 3px; font-size: 11px; }
h1 { font-size: 24px; margin: 2px 0; }
.pair { display: flex; flex-wrap: wrap; gap: 6mm; padding: 4mm 16mm; }
.pair.brk { page-break-before: always; padding-top: 12mm; }
.col { width: 46%; } .col img { width: 100%; border: 0.3px solid #ccc; }
.tag { font-size: 10px; font-family: Consolas; color: #2E6E6B; margin: 0 0 1mm; }
.note { font-size: 11px; margin: 1mm 0 0; width: 94%; color: #55524b; }
</style></head><body>
<div class="hdr"><div class="kicker">FASE 03A · FRAGMENTO PILOTO C2 (32×33 m) · REFUGIO CLIMÁTICO PUERTA DEL SOL</div>
<h1>PILOT REFERENCE COMPARISON</h1>
<p style="font-size:11px;color:#8a877f">No se busca identidad de imagen sino coincidencia de: escala · densidad · altura · materialidad · tipo de espacio · relación humano-estructura. Clay = geometría; el material llega en 03B.</p></div>
''' + rows + '</body></html>'

src = os.path.join(HERE, '_validacion', '_cmp_src.html')
open(src, 'w', encoding='utf-8').write(html)
out = os.path.join(HERE, 'PILOT_REFERENCE_COMPARISON.pdf')
subprocess.run([r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', '--headless=new', '--disable-gpu',
                '--no-pdf-header-footer', '--print-to-pdf=' + out, 'file:///' + src.replace('\\', '/')],
               capture_output=True, timeout=240)
print('PDF:', os.path.exists(out), os.path.getsize(out) if os.path.exists(out) else 0)
