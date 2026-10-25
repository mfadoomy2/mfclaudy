# -*- coding: utf-8 -*-
# Megaestructura macarra · plantas a cada nivel: corte horizontal completo a +1,20 m sobre los tableros de cada nivel.
import json
exec(open('/home/claude/mega/dibujar_mega.py').read().split('SHEETS = []')[0])
NV = json.load(open('/mnt/user-data/uploads/T7/G3_RHINO/out/mega/NIVELES_MEGA.json'))
LCUT = collections.defaultdict(list)
for c in NV['cuts']: LCUT[c['level']].append(c)
POCHE_N = {'05_BARANDILLAS', '06_MEGATRONCOS', '07_COSTILLAS', '08_CELULAS_PERFORADAS', '20_ANCLAJES', '02_BORDES_AMARILLOS', '17_UNIONES_COBRE', '01_SUELOS_HABITABLES', '04_DESCANSILLOS', '03_ESCALERAS_PELDANOS'}
LIGHT_N = {'09_TENSORES', '10_MEMBRANAS', '21_PARTITURAS', '12_CONDUCTOS_CIAN', '11_NERVIOS_MAGENTA', '15_NODULOS_TACTILES', '18_LUZ'}
SHEETS = []
for L in NV['levels']:
    ids = L['estancias']; zc = L['cut']; lid = L['id']
    s = Sheet(f'MG{int(lid[1:]) + 1:02d}', f'Megaestructura macarra · nivel {lid[1:]} · {" / ".join(cota(DECKZ[i][1]) for i in ids)}',
              f'PLANTA · E 1:200 · corte horizontal a {cota(zc)} m · todo lo cortado en negro · lo que queda debajo en proyección')
    s.grid()
    # 1. debajo: tableros más bajos, de abajo arriba (el más alto tapa)
    below = sorted([j for j in DECK if DECKZ[j][1] < L['base'] - .5], key=lambda j: DECKZ[j][1])
    for j in below:
        dz = L['base'] - DECKZ[j][1]
        s.geom(DECK[j], .10 if dz < 8 else .06, 1, kind='TABLERO_INFERIOR')
        c = SP[j]['c']; s.tx(s.pt((c[0], c[1])), f'E{j:02d} {cota(DECKZ[j][1])}', 1.6, align='center', kind='TABLERO_INFERIOR', mask=True)
    s.trunks(lw=.10, labels=False)
    # 2. escaleras que llegan o salen de este nivel, o que el corte atraviesa
    eids = []
    for Lk in LK:
        pts = ROUTE[Lk['id']]; z0 = min(p[2] for p in pts); z1 = max(p[2] for p in pts)
        if Lk['from'] in ids or Lk['to'] in ids or z0 < zc < z1:
            s.stair(Lk, zcut=zc); eids.append(int(Lk['id'][1:3]))
    descansillos(s, eids)
    # 3. tableros del nivel y su equipamiento visto
    for i in ids:
        g = DECK[i]; s.geom(g, .25, 1, kind='TABLERO'); s.geom(g.buffer(-.28), .10, None, kind='CORDON')
        for lay, lw in [('14_AGUA', .10), ('13_DEPOSITOS_CRISTAL', .13), ('19_MOBILIARIO', .18), ('16_MAQUINARIA', .10), ('18_LUZ', .10)]:
            for p in PIECES[lay]:
                if est_of(p['name']) != i: continue
                z0, z1 = p['z']
                for o in p['outline']:
                    if len(o) < 3: continue
                    pg = clean(Polygon(o))
                    if z1 < DECKZ[i][0] - .02: s.geom(pg, .10, None, [1.0, .6], 'BAJO_TABLERO')
                    elif z0 > zc: s.geom(pg, .10, None, [1.8, .8], 'SOBRE_CORTE')
                    elif not (z0 < zc < z1): s.geom(pg, lw, 1 if lay == '19_MOBILIARIO' else None, kind='VISTO')
        for o in OUTL['10_MEMBRANAS']:
            if est_of(o['name']) == i:
                for r in o['polys']:
                    if len(r) > 2: s.line(r + [r[0]], .08, [1.8, .8], 'VELA_SOBRE_CORTE')
    # tableros justo encima (hasta 6 m): discontinua
    for j in DECK:
        if L['base'] + 1.5 < DECKZ[j][1] < L['base'] + 6.5: s.geom(DECK[j], .08, None, [2.4, .9], 'TABLERO_SUPERIOR')
    # 4. corte horizontal completo
    poche = []; thin = []
    for c in LCUT[lid]:
        for r in c['polys']:
            if len(r) < 2: continue
            closed = len(r) > 3 and math.dist(r[0], r[-1]) < .01
            if not closed: s.line(r, .18, kind='CORTE'); continue
            pg = clean(Polygon(r))
            if pg.is_empty: continue
            if c['layer'] in POCHE_N: poche.append(pg)
            elif c['layer'] in LIGHT_N: s.geom(pg, .08, None, kind='CORTE_LIGERO')
            else: thin.append(pg)
    for pg in thin: s.geom(pg, .18, 1, kind='CORTE_EQUIPAMIENTO')
    if poche: s.geom(unary_union(poche), .18, 0, kind='CORTE_NEGRO')
    for i in ids: s.ovalaxes(i); label_est(s, i)
    crossing = []
    for Lk in LK:
        if int(Lk['id'][1:3]) not in eids: continue
        pts = ROUTE[Lk['id']]; mid = pts[len(pts) // 2]; a, b = Lk['from'], Lk['to']
        lo, hi = (a, b) if SP[a]['c'][2] < SP[b]['c'][2] else (b, a)
        s.tx(s.pt((mid[0], mid[1] + .35)), f'{Lk["id"][:3]} · E{lo:02d} a E{hi:02d}', 1.8, align='center', kind='CONEXION', mask=True)
        s.tx(s.pt((mid[0], mid[1] - .55)), f'{Lk["risers"]} p · {num(Lk["rise_max"] * 100, 1)} cm · {num(Lk["width"])} m', 1.6, align='center', kind='CONEXION', mask=True)
        crossing.append((Lk, lo, hi))
    # columna
    col = [('NIVEL', 3.2), (f'{lid} · corte a {cota(zc)} m', 2.6)]
    for i in ids: col.append((f'      {num(zc - DECKZ[i][1])} m sobre el tablero de E{i:02d} ({cota(DECKZ[i][1])})', 2.0))
    col += [('gap', 'gap'), ('PROGRAMA', 3.2)]
    for i in ids:
        seats = sum(1 for p in PIECES['19_MOBILIARIO'] if est_of(p['name']) == i) // 2
        water = any(est_of(p['name']) == i for p in PIECES['14_AGUA'])
        mach = sum(1 for p in PIECES['16_MAQUINARIA'] if est_of(p['name']) == i)
        lights = sum(1 for p in PIECES['18_LUZ'] if est_of(p['name']) == i)
        sails = sum(1 for o in OUTL['10_MEMBRANAS'] if est_of(o['name']) == i)
        col.append((f'E{i:02d} · {title(SP[i]["name"])}', 2.6))
        col.append((f'      {cota(DECKZ[i][1])} · {num(DECK[i].area, 1)} m² · tablero {num((DECKZ[i][1] - DECKZ[i][0]) * 100, 0)} cm', 2.0))
        bits = [f'{seats} bancos con respaldo' if seats else 'sin bancos', f'{sails} velas', f'{mach} cilindros bajo el tablero' if mach else '', f'{lights} luces' if lights else '', 'cuenco de agua y vasijas colgadas' if water else '']
        col.append(('      ' + ' · '.join(b for b in bits if b), 2.0))
        trs = [t for t, d in TR.items() if i in d['serves']]
        col.append(('      sostenida por ' + ' · '.join(trs) if trs else '      sin rama de tronco propia', 2.0))
    col += [('gap', 'gap'), ('CONEXIONES EN ESTA PLANTA', 3.2)]
    for Lk, lo, hi in crossing:
        how = 'sale' if lo in ids else ('llega' if hi in ids else 'pasa cortada')
        col.append((f'{Lk["id"][:3]} · {how} · E{lo:02d} {cota(DECKZ[lo][1])} a E{hi:02d} {cota(DECKZ[hi][1])}', 2.0))
    col += [('gap', 'gap'), ('LECTURA DEL DIBUJO', 3.2), ('Negro: todo lo cortado a la cota del corte', 2.2), ('0,25 mm: tableros del nivel', 2.2),
            ('0,10 / 0,06 mm: tableros inferiores, según profundidad', 2.2), ('Discontinua larga: tableros superiores, velas y luces', 2.2),
            ('Discontinua corta: máquinas bajo el tablero', 2.2), ('Trazo-punto: troncos, ramas, malla y ejes S', 2.2)]
    s.frame(col, [f'Corte horizontal único a {cota(zc)} m sobre toda la megaestructura: cada malla de Rhino intersecada con el plano.',
                  'Debajo, los tableros inferiores en proyección: el más alto tapa al más bajo. Encima, hasta 6 m, en discontinua.',
                  'Escaleras: línea de huella, arranque (círculo) y llegada (triángulo); peldaños por encima del corte en discontinua.'])
    SHEETS.append(s)

c = canvas.Canvas(str(OUT / 'G3_MEGAESTRUCTURA_PLANTAS_POR_NIVEL_1_200.pdf'), pageCompression=1); c.setTitle('Megaestructura macarra · plantas por nivel 1:200'); c.setAuthor('G3')
for s in SHEETS:
    pdfpage(c, s); (OUT / f'{s.page}_NIVEL.svg').write_text(svg(s))
c.save()
print('ok', len(SHEETS))
