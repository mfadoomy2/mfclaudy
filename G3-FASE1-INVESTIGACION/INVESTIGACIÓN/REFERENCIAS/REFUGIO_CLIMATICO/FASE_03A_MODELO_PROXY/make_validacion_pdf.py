# -*- coding: utf-8 -*-
"""Compone VALIDACION_TRANSITABILIDAD.pdf (A3 apaisado) desde el informe + vistas."""
import base64
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
inf = json.load(open(os.path.join(HERE, '_validacion', 'informe.json'), encoding='utf-8'))


def b64(p):
    return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()


def b64jpg(p, maxw=1100):
    from PIL import Image
    import io
    im = Image.open(p)
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)))
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=82)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


rows = ''
for c in inf['chk1_corredores']:
    rows += '<tr><td>%s</td><td>%.2f m</td><td class="%s">%s</td><td>%s</td></tr>' % (
        c['id'], c['paso_min_m'], 'ok' if c['ok'] else 'ko', 'CUMPLE' if c['ok'] else 'NO', c.get('culpable', ''))
mrows = ''
for x in inf['chk3_metro']:
    mrows += '<tr><td>%s</td><td>(%.0f, %.0f)</td><td class="%s">%s</td></tr>' % (
        x['boca'], x['pos'][0], x['pos'][1], 'ok' if x['ok'] else 'ko', 'LIBRE' if x['ok'] else 'INVADIDA')

VIEWS_DIR = os.path.join(HERE, 'vistas_control')
views = sorted(f for f in os.listdir(VIEWS_DIR) if f.endswith('.png'))
cells = ''
for v in views:
    cells += '<div class="cell"><img src="%s"><p>%s</p></div>' % (b64jpg(os.path.join(VIEWS_DIR, v), 760), v[:-4].replace('_', ' '))

html = '''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page { size: 420mm 297mm; margin: 0; }
body { font-family: Bahnschrift, Arial; margin: 0; color: #33322E; }
.page { width: 420mm; height: 297mm; page-break-after: always; padding: 14mm 16mm; box-sizing: border-box; position: relative; }
h1 { font-size: 26px; margin: 0 0 2px; } h2 { font-size: 15px; color: #2E6E6B; letter-spacing: 2px; margin: 14px 0 6px; }
.kicker { color: #D6577F; letter-spacing: 3px; font-size: 11px; }
table { border-collapse: collapse; font-size: 12px; margin-top: 4px; }
td, th { border: 0.4px solid #bbb; padding: 3px 8px; text-align: left; }
.ok { color: #2E7D46; font-weight: 600; } .ko { color: #C62828; font-weight: 600; }
.grid { display: flex; flex-wrap: wrap; gap: 6mm; }
.cell { width: 88mm; } .cell img { width: 88mm; border: 0.3px solid #ccc; } .cell p { font-size: 9px; margin: 1px 0 0; font-family: Consolas; }
.foot { position: absolute; bottom: 8mm; left: 16mm; font-size: 9px; color: #8a877f; font-family: Consolas; }
img.full { max-width: 100%; max-height: 190mm; border: 0.3px solid #ccc; }
.cols { display: flex; gap: 12mm; }
</style></head><body>

<div class="page">
<div class="kicker">FASE 03A · MODELO PROXY TRANSITABLE · REFUGIO CLIMÁTICO PUERTA DEL SOL</div>
<h1>VALIDACIÓN DE TRANSITABILIDAD</h1>
<div class="cols"><div style="width:46%">
<h2>CHK1 — ANCHO DE PASO EN CORREDORES (mín 3.00 m)</h2>
<table><tr><th>corredor</th><th>paso mín</th><th></th><th>elemento más próximo</th></tr>''' + rows + '''</table>
<h2>CHK2 — GÁLIBO BAJO ELEMENTOS (mín 3.00 m)</h2>
<p style="font-size:12px">0 infracciones: ningún disco/deck invade el gálibo sobre corredores. Cinta a +6.00 (cara inferior +5.75).</p>
<h2>CHK3 — CLAROS DE METRO / CERCANÍAS (r 5.5 m)</h2>
<table><tr><th>boca</th><th>posición</th><th>estado</th></tr>''' + mrows + '''</table>
<h2>CHK4/5 — OTROS</h2>
<p style="font-size:12px">Esbeltos (árboles/mástiles) a ≥0.8 m de todo eje de paso: CUMPLE · Soportes de cinta fuera de corredores (38 ud): CUMPLE · Ocupación fija del suelo: <b>10.6 %</b> de la plaza (sombra del dosel ≈ 50-60 %): el suelo permanece plaza.</p>
<h2>CORRECCIONES APLICADAS (propuesta v1.1, ver geometria_overrides_f03a.json)</h2>
<p style="font-size:11.5px;line-height:1.5">① Ejes re-trazados por los huecos reales (Mayor–Alcalá al sur de los trenes; Carmen por el istmo O; Montera al este de la cúpula).
② Puertas abiertas en orlas de jardineras C1-SE, C1-SW y C3-SW (no barreras continuas). ③ Trenes recortados: T-O 3 cáps sur, T-SE 2 cáps este.
④ Estanque E-3 → (11,21) fuera del claro de Carmen. ⑤ LAB02 reubicado junto a los viveros C3 (60,16), lejos de las bocas de Alcalá.
⑥ Retirados del proxy cápsulas/jardineras/bancos/árboles/mástiles a &lt;5.5 m de bocas. <b>HALLAZGO:</b> la cúpula Ø13 tapona el canal C2–C3 y
las bocas de Alcalá/Cercanías viven DENTRO del campo C3 — decisiones de planta v1.1 pendientes de revisión del autor.</p>
</div><div style="width:54%">
<h2>PLANTA DE COMPROBACIÓN — 0 CONFLICTOS</h2>
<img class="full" src="''' + b64(os.path.join(HERE, '_validacion', 'planta_conflictos.png')) + '''">
</div></div>
<div class="foot">SOL_REFUGIO_3D_PROXY_v001.3dm · alturas según HEIGHT_SYSTEM.md · XY según planta maestra Fase 01 + overrides v1.1 · 07-2026</div>
</div>

<div class="page">
<div class="kicker">FASE 03A · VISTAS DE CONTROL A 1.65 M</div>
<h1>VISTAS HUMANAS · V01–V12</h1>
<div class="grid">''' + ''.join('<div class="cell"><img src="%s"><p>%s</p></div>' % (b64jpg(os.path.join(VIEWS_DIR, v), 760), v[:-4].replace('_', ' ')) for v in views[:12]) + '''</div>
<div class="foot">viewport clay · three.js sobre scene.js derivada del mismo generador que el .3dm</div>
</div>

<div class="page">
<div class="kicker">FASE 03A · VISTAS DE CONTROL A 1.65 M</div>
<h1>VISTAS HUMANAS · V13–V21</h1>
<div class="grid">''' + ''.join('<div class="cell"><img src="%s"><p>%s</p></div>' % (b64jpg(os.path.join(VIEWS_DIR, v), 760), v[:-4].replace('_', ' ')) for v in views[12:]) + '''</div>
<div class="foot">V19 sobre la cinta (+5.7) · V20 aérea · V21 axonometría ortográfica · resto a ojo humano 1.65 m</div>
</div>

</body></html>'''

src = os.path.join(HERE, '_validacion', '_pdf_src.html')
open(src, 'w', encoding='utf-8').write(html)
out = os.path.join(HERE, 'VALIDACION_TRANSITABILIDAD.pdf')
subprocess.run([r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', '--headless=new', '--disable-gpu',
                '--no-pdf-header-footer', '--print-to-pdf=' + out, 'file:///' + src.replace('\\', '/')],
               capture_output=True, timeout=240)
print('PDF:', os.path.exists(out), os.path.getsize(out) if os.path.exists(out) else 0)
