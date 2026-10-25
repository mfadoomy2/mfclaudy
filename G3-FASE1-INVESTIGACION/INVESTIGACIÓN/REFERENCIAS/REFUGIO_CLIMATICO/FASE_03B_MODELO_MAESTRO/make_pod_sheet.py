# -*- coding: utf-8 -*-
"""TRIPO_POD_EVALUATION.pdf — hoja de evaluacion del POD (generacion bloqueada por suscripcion)."""
import base64
import io
import os
import subprocess

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, 'tripo', 'TRIPO_PINK_POD_01')


def b64(p, maxw=760):
    im = Image.open(p)
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)))
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=82)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


mv = ''.join('<div class="c4"><p class="tag">%s</p><img src="%s"></div>' % (v, b64(os.path.join(D, v + '.png')))
             for v in ('FRONT', 'LEFT', 'BACK', 'RIGHT'))

html = '''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page { size: 420mm 297mm; margin: 0; }
body { font-family: Bahnschrift, Arial; margin: 0; color: #33322E; }
.page { width: 420mm; height: 297mm; padding: 12mm 16mm; box-sizing: border-box; }
.kicker { color: #D6577F; letter-spacing: 3px; font-size: 11px; }
h1 { font-size: 23px; margin: 2px 0 6px; } h2 { font-size: 13px; color: #2E6E6B; letter-spacing: 2px; margin: 8px 0 3px; }
.row { display: flex; gap: 5mm; }
.c4 { width: 24%; } .c4 img, .c3 img { width: 100%; border: 0.3px solid #ccc; }
.c3 { width: 32%; }
.tag { font-size: 9px; font-family: Consolas; color: #2E6E6B; margin: 0 0 1mm; }
.blocked { border: 0.5px dashed #C62828; color: #C62828; font-size: 11px; padding: 10mm 6mm; text-align: center; height: 46mm; box-sizing: border-box; }
p.note { font-size: 11px; color: #55524b; margin: 2mm 0; }
table { border-collapse: collapse; font-size: 11px; margin-top: 2mm; }
td, th { border: 0.4px solid #bbb; padding: 2.5px 7px; text-align: left; }
</style></head><body><div class="page">
<div class="kicker">FASE 03B · PIEZA HÉROE 01 · TRIPO_PINK_POD_01 · workflow api_tripo3_1_multiview_to_model</div>
<h1>EVALUACIÓN POD — TRIPO vs PINK_POD_BASE PARAMÉTRICO</h1>

<h2>1 · MULTIVIEW INPUT PACK (mismo objeto garantizado: bloque paramétrico orbitado, fondo neutro, 1024²)</h2>
<div class="row">''' + mv + '''</div>

<div class="row" style="margin-top:5mm">
<div class="c3"><h2>2 · OUTPUT BRUTO TRIPO</h2><div class="blocked">GENERACIÓN BLOQUEADA<br><br>El workspace de Comfy Cloud no tiene suscripción de pago activa ("Partner-node workflows require a paid subscription").<br><br>Imágenes subidas · workflow verificado (nodos 44/45/46 → TripoMultiviewToModelNode) · 0 créditos consumidos.</div></div>
<div class="c3"><h2>3 · OUTPUT LIMPIO</h2><div class="blocked">PENDIENTE<br><br>Pipeline de limpieza preparado:<br>escala → orientación (Y-up→Z-up) → flotantes → normales → reducción → base → Block → ASSET_LIBRARY.</div></div>
<div class="c3"><h2>4 · VERSIÓN PARAMÉTRICA (PINK_POD_BASE / POD_M Ø3.25)</h2><p class="tag">envolvente + 6 gajos + válvula + 3 pies + amarres + aro de puerta</p><img src="''' + b64(os.path.join(D, 'FRONT.png')) + '''"></div>
</div>

<div class="row" style="margin-top:5mm">
<div class="c3"><h2>5 · APLICACIÓN EN EL MODELO — racimo C2-N</h2><img src="''' + b64(os.path.join(D, 'EN_MODELO_racimo_C2N.png')) + '''"></div>
<div class="c3"><h2>5b · DETALLE</h2><img src="''' + b64(os.path.join(D, 'EN_MODELO_detalle.png')) + '''"></div>
<div class="c3"><h2>6 · QUÉ APORTARÍA TRIPO / REGISTRO</h2>
<p class="note"><b>Lo que la paramétrica YA resuelve (~75-80%):</b> silueta, gajos, válvula, apoyos, amarres, puerta, escala exacta, instanciable como bloque, editable.</p>
<p class="note"><b>Lo que sólo aportaría Tripo:</b> arrugas y tensión de membrana inflada (los renders muestran TPU con pliegues), asimetrías orgánicas, detalle de costura/válvula para PRIMEROS PLANOS de 03C. Irrelevante a >10 m de distancia.</p>
<table>
<tr><th>créditos consumidos</th><td>0 (bloqueo previo al gasto)</td></tr>
<tr><th>tiempo de preparación</th><td>~25 min (packs 4×5 piezas + template + subidas)</td></tr>
<tr><th>tiempo de limpieza</th><td>— (no ejecutado)</td></tr>
<tr><th>decisión propuesta</th><td>①  suscribir workspace y generar SOLO el POD, o ② descartar Tripo para esta familia y confiar en PINK_POD_BASE (criterio del autor: no insistir por inercia)</td></tr>
</table></div>
</div>
</div></body></html>'''

src = os.path.join(D, '_sheet_src.html')
open(src, 'w', encoding='utf-8').write(html)
out = os.path.join(HERE, 'TRIPO_POD_EVALUATION.pdf')
subprocess.run([r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', '--headless=new', '--disable-gpu',
                '--no-pdf-header-footer', '--print-to-pdf=' + out, 'file:///' + src.replace('\\', '/')],
               capture_output=True, timeout=240)
print('PDF:', os.path.exists(out), os.path.getsize(out) if os.path.exists(out) else 0)
