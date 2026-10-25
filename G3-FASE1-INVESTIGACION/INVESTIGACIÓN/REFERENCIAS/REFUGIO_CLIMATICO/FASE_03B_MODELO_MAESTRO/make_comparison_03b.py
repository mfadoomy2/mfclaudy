# -*- coding: utf-8 -*-
"""03B_REFERENCE_COMPARISON.pdf — 10 referencias interiores vs modelo 03B."""
import base64
import io
import os
import subprocess

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.normpath(os.path.join(HERE, '..', '..', 'MONTESERIN IA', 'MONTESERIN IA', 'MUTACIONES (DIBUJO + IA)',
                                    'DIBUJO3 (REFUGIO CLIMATICO)', 'IN PROGRESS REFUGIO'))
VH = os.path.join(HERE, 'vistas_humanas')
MT = os.path.join(HERE, 'material_test')


def b64(p, maxw=940):
    im = Image.open(p)
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)))
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=80)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


PAIRS = [
    ('12CA810C-437B-41C2-B54C-62B449F8FD7B.png', VH, 'V07_salon_C2_reloj',
     'Salón urbano mirando al reloj: la torre de Correos permanece como fondo; cubas con mástil, cinta a +6 y red rosa en suelo coinciden. El modelo aún sin vegetación densa (03C).'),
    ('24D82F58-281B-4FED-8CDF-058C0BCA7257.png', VH, 'V05_banda_correos',
     'Estratificación huerto/tubos/deck: suelo productivo + red 3.5-6 + recorrido a 6. Cotas idénticas al render; la capa hortícola densa llega en 03C.'),
    ('29A08040-DD59-4509-BB21-0735BF86DAEB.png', VH, 'V08_bajo_anillo_C2N',
     'Techo escalonado de discos 5/6.75/8.5 con huecos de cielo: la discontinuidad del dosel se conserva (no cubierta uniforme).'),
    ('999C4F45-0B15-493F-BE41-8A7732CCF2E2.png', VH, 'V06_bajo_C1',
     'Anillos apilados + esferas + suelo libre: el haz triple del loop y las trepadoras en mástiles reproducen la lógica aérea.'),
    ('A2BD2AAA-FA08-48B3-ACD8-BEFFD226B1B1.png', VH, 'V03_acceso_preciados',
     'Módulos lenticulares solapados en 2-3 cotas con cápsulas a cota 0: familia y reparto correctos; nervios radiales legibles.'),
    ('1C334300-C51E-4D66-BF25-0FA619020673.png', VH, 'V15_vivero_C3NE',
     'Racimo de esferas con gajos junto a viveros verticales y estanque: programa agrupado como en el render (LAB reubicado al lado).'),
    ('2AA3157F-D38D-4130-A97B-417EA31A4F54.png', VH, 'V17_hacia_oso',
     'Borde norte más ligero: anillos abiertos, esferas en suelo, vista hacia la esquina de Alcalá (Oso y Madroño).'),
    ('FE41AB82-9CA6-4F29-972E-A311FD500F5F.png', VH, 'V04_acceso_carretas',
     'Acceso con boca de metro conservada y claro de 5.5 m: el dosel se abre sobre el acceso, cápsulas apartadas del claro.'),
    ('6BB98FC3-FC4B-4D4A-8BB0-51670404784F.png', MT, 'MAT_V13_splash',
     'TEST MATERIAL: lámina jugable + niebla + discos translúcidos verdes; primera verificación de la paleta rosa/verde/madera (no render final).'),
    ('79405914-2F38-4010-839D-B75F373FDA46.png', MT, 'MAT_V07_salon_C2_reloj',
     'TEST MATERIAL: eje hacia Correos con estructura madera cálida y membranas verdes; el reloj sigue presente. Materialidad definitiva en 03C.'),
]

rows = ''
for i, (ref, mdir, v, note) in enumerate(PAIRS):
    rows += '''<div class="pair%s"><div class="col"><p class="tag">RENDER ORIGINAL · %s</p><img src="%s"></div>
    <div class="col"><p class="tag">MODELO 03B · %s</p><img src="%s"></div>
    <p class="note">%s</p></div>''' % (
        ' brk' if i % 2 == 0 and i > 0 else '', ref[:8], b64(os.path.join(REF, ref)),
        v, b64(os.path.join(mdir, v + '.png')), note)

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
<div class="hdr"><div class="kicker">FASE 03B · SOL_FULL_SCENE_v001 · REFUGIO CLIMÁTICO PUERTA DEL SOL</div>
<h1>03B REFERENCE COMPARISON</h1>
<p style="font-size:11px;color:#8a877f">Objetivo: que cada render pueda explicarse como una vista distinta de UN MISMO proyecto coherente — no copia literal. Se compara escala · altura · densidad · estructura · transitabilidad · paisaje · profundidad. 8 pares clay + 2 pares test-material.</p></div>
''' + rows + '</body></html>'

src = os.path.join(HERE, '_cmp_src.html')
open(src, 'w', encoding='utf-8').write(html)
out = os.path.join(HERE, '03B_REFERENCE_COMPARISON.pdf')
subprocess.run([r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', '--headless=new', '--disable-gpu',
                '--no-pdf-header-footer', '--print-to-pdf=' + out, 'file:///' + src.replace('\\', '/')],
               capture_output=True, timeout=300)
print('PDF:', os.path.exists(out), os.path.getsize(out) if os.path.exists(out) else 0)
