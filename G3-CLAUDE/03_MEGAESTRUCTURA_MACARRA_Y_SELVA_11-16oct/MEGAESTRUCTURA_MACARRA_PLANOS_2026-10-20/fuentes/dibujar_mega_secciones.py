# -*- coding: utf-8 -*-
# Megaestructura macarra · secciones 1:200: corte exacto (MeshPlane) + líneas ocultas de Rhino de lo que queda detrás.
import json, os
exec(open('/home/claude/mega/dibujar_mega.py').read().split('SHEETS = []')[0])
TUBES = {'02_BORDES_AMARILLOS', '05_BARANDILLAS', '06_MEGATRONCOS', '07_COSTILLAS', '09_TENSORES', '11_NERVIOS_MAGENTA', '12_CONDUCTOS_CIAN',
         '15_NODULOS_TACTILES', '17_UNIONES_COBRE', '20_ANCLAJES', '21_PARTITURAS'}
POCHE_S = {'01_SUELOS_HABITABLES', '02_BORDES_AMARILLOS', '03_ESCALERAS_PELDANOS', '04_DESCANSILLOS', '05_BARANDILLAS', '06_MEGATRONCOS',
           '07_COSTILLAS', '08_CELULAS_PERFORADAS', '20_ANCLAJES', '17_UNIONES_COBRE'}
SHEETS = []
LEVELS = json.load(open('/mnt/user-data/outputs/rhino/mega_niveles.json'))
for sid in 'ABCD':
    fn = f'/mnt/user-data/uploads/T7/G3_RHINO/out/mega/SECCIONES_MEGA_{sid}.json'
    if not os.path.exists(fn): continue
    S = json.load(open(fn)); d = S['def']; IL = S['idlayer']; O = d['origin']; xd = d['xdir']
    def U(p): return (p[0] - O[0]) * xd[0] + (p[1] - O[1]) * xd[1]
    umin, zmin, umax, zmax = S['beyond_bbox_uv']
    s = Sheet(f'MG{17 + "ABCD".index(sid)}', f'Megaestructura macarra · sección {sid}', f'SECCIÓN · E 1:200 · {d["label"]} · corte exacto y líneas ocultas de Rhino')
    s.ox = 330 - (umin + umax) / 2 * K; s.oy = 330 - (zmin + zmax) / 2 * K
    def pt(u, z): return [s.ox + u * K, s.oy + z * K]
    # 1. proyección
    for pts, src, sil in S['hld']:
        la = IL.get(src, ['?'])[0]
        if sil == 'Crease' and la in TUBES: continue
        lw = .09 if sil == 'Tangent' else .05
        if la in ('09_TENSORES', '21_PARTITURAS', '08_CELULAS_PERFORADAS', '10_MEMBRANAS'): lw = .05
        s.lp([pt(*p) for p in pts], lw, kind='PROYECCION')
    # 2. corte
    groups = collections.defaultdict(list); decks = []
    for c in S['cut']:
        q = [(U(p), p[2]) for p in c['pts']]
        if len(q) > 3 and math.dist(q[0], q[-1]) < .01:
            pg = clean(Polygon(q))
            if not pg.is_empty:
                groups[c['layer']].append(pg)
                if c['layer'] == '01_SUELOS_HABITABLES': decks.append((c['name'], pg))
        elif len(q) > 1: s.lp([pt(*p) for p in q], .18, kind='CORTE')
    allc = unary_union([g for la, gs in groups.items() for g in gs])
    for p in polys(allc): s.pp([[pt(*xy) for xy in r.coords] for r in [p.exterior] + list(p.interiors)], .01, 1, 'FONDO')
    for la, gs in groups.items():
        if la in POCHE_S: continue
        for g in gs:
            for p in polys(g): s.pp([[pt(*xy) for xy in r.coords] for r in [p.exterior] + list(p.interiors)], .13 if la not in ('10_MEMBRANAS', '09_TENSORES') else .08, 1, 'CORTE_' + la)
    po = unary_union([g for la, gs in groups.items() if la in POCHE_S for g in gs])
    for p in polys(po): s.pp([[pt(*xy) for xy in r.coords] for r in [p.exterior] + list(p.interiors)], .15, 0, 'CORTE_NEGRO')
    # 3. cota 0 del modelo
    s.lp([pt(umin - 2, 0), pt(umax + 2, 0)], .13, [4, 1], 'COTA_CERO'); s.tx(pt(umax + 2.4, -.3), '±0,00 · cota cero del modelo', 2.0)
    # 4. ejes de la malla que cruzan la sección
    along_x = abs(xd[0]) > .5
    G = GX if along_x else GY
    for lab, v, t in G:
        u = U((v, O[1])) if along_x else U((O[0], v))
        if umin - 1 < u < umax + 1:
            s.lp([pt(u, zmin - 2), pt(u, zmax + 2)], .10, [3, .7, .2, .7], 'EJES_MALLA'); s.bubble(pt(u, zmax + 3.4), lab)
            s.tx(pt(u + .5, zmin - 2.6), f'{t}', 1.8, kind='EJES')
    # troncos cortados: su eje vertical
    # 5. niveles: todos los niveles de la estructura, en la cadena de la izquierda
    xl = pt(umin, 0)[0] - 14
    prev = -1e9
    for L in LEVELS:
        y = s.oy + L['base'] * K
        s.pp([[(xl, y), (xl - 1.2, y + 1.4), (xl + 1.2, y + 1.4), (xl, y)]], .13, 1, 'NIVEL')
        s.lp([(xl - 3, y), (xl + 6, y)], .08, kind='NIVEL')
        ty = max(y + .3, prev + 2.3); prev = ty
        s.tx((xl - 3.5, ty), f'{L["id"]} ' + ' / '.join(cota(DECKZ[i][1]) for i in L['estancias']), 1.8, align='right', kind='NIVEL')
    # 6. rótulos de estancias cortadas
    for name, pg in decks:
        i = est_of(name); b = pg.bounds
        q = pt((b[0] + b[2]) / 2, b[3] + .55)
        s.tx(q, f'E{i:02d} · {title(SP[i]["name"])} · {cota(DECKZ[i][1])}', 1.9, align='center', kind='ESTANCIA', mask=True)
    # cotas
    s.dim((umin, zmin), (umax, zmin), zmin - 4.0, 'x') if False else None
    A = pt(umin, zmin - 4.5); B = pt(umax, zmin - 4.5)
    s.lp([A, B], .13, kind='COTAS')
    for q in (A, B): s.lp([(q[0] - .8, q[1] - .8), (q[0] + .8, q[1] + .8)], .18, kind='COTAS')
    s.tx(((A[0] + B[0]) / 2, A[1] + 1), num(umax - umin), 2.0, align='center', kind='COTAS')
    xr = pt(umax, 0)[0] + 10
    A = (xr, s.oy + zmin * K); B = (xr, s.oy + zmax * K); C0 = (xr, s.oy)
    s.lp([A, B], .13, kind='COTAS')
    for q in (A, C0, B): s.lp([(q[0] - .8, q[1] - .8), (q[0] + .8, q[1] + .8)], .18, kind='COTAS')
    s.tx((xr - 1, (A[1] + C0[1]) / 2), num(-zmin), 2.0, 90, 'center', 'COTAS'); s.tx((xr - 1, (C0[1] + B[1]) / 2), num(zmax), 2.0, 90, 'center', 'COTAS')
    cut_est = sorted(set(est_of(n) for n, g in decks))
    col = [('SECCIÓN ' + sid, 3.2), (d['label'], 2.2), ('gap', 'gap'), ('ESTANCIAS CORTADAS', 3.2)]
    for i in cut_est: col.append((f'E{i:02d} · {title(SP[i]["name"])} · {cota(DECKZ[i][1])}', 2.2))
    stairs = sorted(set(c['name'][:3] for c in S['cut'] if c['layer'] == '03_ESCALERAS_PELDANOS'))
    col += [('gap', 'gap'), ('ESCALERAS CORTADAS', 3.2), (' · '.join(stairs) if stairs else 'ninguna', 2.2)]
    trs = sorted(set(c['name'][:3] for c in S['cut'] if c['layer'] == '06_MEGATRONCOS'))
    col += [('gap', 'gap'), ('TRONCOS CORTADOS', 3.2), (' · '.join(trs) if trs else 'ninguno', 2.2),
            ('gap', 'gap'), ('LECTURA DEL DIBUJO', 3.2), ('Negro: tableros, bordes, peldaños, troncos, costillas y células cortadas', 2.2),
            ('0,13 mm blanco: mobiliario, máquinas, depósitos y conductos cortados', 2.2), ('0,09 mm: contornos aparentes de lo que queda detrás', 2.2),
            ('0,05 mm: aristas, tensores, velas y células detrás', 2.2), ('Izquierda: los quince niveles N01-N15', 2.2), ('Trazo-punto: ejes de la malla de troncos', 2.2)]
    s.frame(col, [f'Plano vertical por {d["label"].split(",")[0]}: cada malla de Rhino intersecada con el plano (negro) y líneas ocultas de Rhino de lo que queda detrás.',
                  'De los tubos (bordes, barandillas, troncos, costillas, tensores, nervios) solo se dibuja su contorno aparente, no las aristas de faceta.',
                  'El modelo no tiene terreno: la línea ±0,00 es la cota cero del archivo. Las raíces de los troncos bajan hasta −8,24 m.'])
    s.meta.update({'section': sid, 'extent_u': [umin, umax], 'extent_z': [zmin, zmax], 'cut_objects': len(S['cut']), 'projection_segments': len(S['hld'])})
    SHEETS.append(s)

c = canvas.Canvas(str(OUT / 'G3_MEGAESTRUCTURA_SECCIONES_1_200.pdf'), pageCompression=1); c.setTitle('Megaestructura macarra · secciones 1:200'); c.setAuthor('G3')
for s in SHEETS:
    pdfpage(c, s); (OUT / f'{s.page}_MEGAESTRUCTURA.svg').write_text(svg(s))
c.save()
print('ok', [s.page for s in SHEETS])
