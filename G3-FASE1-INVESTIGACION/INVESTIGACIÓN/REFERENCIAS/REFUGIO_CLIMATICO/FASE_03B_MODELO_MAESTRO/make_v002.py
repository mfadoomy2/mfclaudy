# -*- coding: utf-8 -*-
"""
GEOMETRIA MAESTRA v002 — Fase 03B.
Parte de geometria_maestra.json (Fase 01, INTACTA) + geometria_overrides_f03a.json (aprobados)
+ decisiones D03B-01..04 + dudas resueltas autonomamente.
Salida: geometria_maestra_v002.json (fuente canonica de 03B en adelante).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
F01 = os.path.normpath(os.path.join(HERE, '..', 'FASE_01_BASE_GRAFICA', '01_BASE_GEOMETRICA', 'planta_maestra'))
F03A = os.path.normpath(os.path.join(HERE, '..', 'FASE_03A_MODELO_PROXY'))

m = json.load(open(os.path.join(F01, 'geometria_maestra.json'), encoding='utf-8'))
OV = json.load(open(os.path.join(F03A, 'geometria_overrides_f03a.json'), encoding='utf-8'))

# ---- overrides f03a aprobados ----
for c in m['circulacion']['corridors']:
    ov = OV['corridors'].get(c['id'])
    if ov:
        c['pts'] = [tuple(p) for p in ov]
METRO_XY = [(e['x'], e['y']) for e in m['contexto']['metro'] if -110 < e['x'] < 100 and -45 < e['y'] < 75]
R = OV['metro_exclusion_radius']


def near_metro(x, y, extra=0.0):
    return any(math.hypot(x - mx, y - my) < R + extra for (mx, my) in METRO_XY)


m['programa']['capsules'] = [c for c in m['programa']['capsules'] if not near_metro(c['cx'], c['cy'], max(c['w'], 1.8) / 2)]
for p in m['paisaje']['planters']:
    p['pts'] = [q for q in p['pts'] if not near_metro(q[0], q[1], 0.9)]
for b in m['programa']['benches']:
    b['pts'] = [q for q in b['pts'] if not near_metro(q[0], q[1], 0.5)]
m['estructura_ligera']['drops'] = [d for d in m['estructura_ligera']['drops'] if not near_metro(d[0], d[1], 1.0)]
m['estructura_ligera']['masts'] = [p for p in m['estructura_ligera']['masts'] if not near_metro(p[0], p[1], 0.3)]
m['paisaje']['new_trees'] = [t for t in m['paisaje']['new_trees'] if not near_metro(t[0], t[1], 0.4)]
for idx_s, (f0, f1) in OV.get('planter_trim', {}).items():
    pl = m['paisaje']['planters'][int(idx_s)]
    n = len(pl['pts'])
    pl['pts'] = pl['pts'][int(f0 * n):int(f1 * n)]
for pid, (nx_, ny_) in OV.get('pond_moves', {}).items():
    for p in m['agua_clima']['ground_ponds']:
        if p['id'] == pid and p['kind'] == 'circle':
            p['cx'], p['cy'] = nx_, ny_
cy_min = OV['capsule_rules']['T-O_cy_min']
cx_max = OV['capsule_rules']['T-SE_cx_max']
m['programa']['capsules'] = [c for c in m['programa']['capsules']
                             if not (c.get('id') == 'T-O' and c['cy'] < cy_min)
                             and not (c.get('id') == 'T-SE' and c['cx'] > cx_max)]
lsh = OV['lab_shift']
m['programa']['lab']['pts'] = [(round(p[0] + lsh[0], 2), round(p[1] + lsh[1], 2)) for p in m['programa']['lab']['pts']]
for (old, new) in OV.get('tree_moves', []):
    m['paisaje']['new_trees'] = [tuple(new) if (abs(t[0] - old[0]) < 0.6 and abs(t[1] - old[1]) < 0.6) else t
                                 for t in m['paisaje']['new_trees']]

# ---- D03B-01: trenes apoyados en suelo (cota semantica) ----
for c in m['programa']['capsules']:
    if c.get('id') in ('T-O', 'T-SE'):
        c['cota'] = 'suelo'
        c['apoyo'] = 0.3
        c['dia'] = 2.4

# ---- D03B-04: cupula — APERTURA + MODIFICACION DE APOYO (cambio minimo) ----
# Se mantiene posicion y Ø13 (fidelidad a F295448F). El casquete arranca a +3.2 sobre
# 6 apoyos perimetrales: el corredor puede atravesarla; oculus cenital abierto Ø3.
m['estructura_principal']['dome'].update(dict(
    base_z=3.2, apex_z=8.0, oculus_r=1.5, n_supports=6, g='G2',
    nota='D03B-04: cupula-pergola elevada; casquete +3.2..+8.0, oculus Ø3, 6 apoyos; posicion y diametro originales'))

# ---- dudas resueltas autonomamente (registradas) ----
m['resoluciones_03b'] = {
    'D9-rail': 'UNA sola infraestructura lineal: pasarela a +6.0. Carril logistico = reserva G4 apagada (evidencia insuficiente de dos sistemas).',
    'D10-4a-capa': 'No existe 4a capa de dosel: max 8.5 (los 9-12 de algunos renders = exageracion, SPECULATIVE descartado).',
    'D11-loop-z': 'Cotas de eje por loop segun familia HEIGHT_SYSTEM (INFERRED, editable via curvas generatrices).',
    'D13-colgadas': '2 esferas colgadas en racimo C2-N a +4.5 (999C4F45); resto en suelo.',
    'D14-materialidad': 'Estructura: madera laminada clara/bambu tecnologico con nudos de acero; aros de disco acero claro; red hidraulica rosa TPU; INFERRED (mayoria de renders con Sol confirmado).',
    'D15-agua-discos': 'TODOS los discos llevan lamina de microalgas 2-5 cm (piscinas suspendidas de las laminas tecnicas).',
    'D16-fuentes': 'Sol actual post-2023 sin fuentes: confirmado.',
    'D17-carlos-iii': 'Se mantiene (-28,-14) G2 hasta plano municipal.',
    'D8-borde-norte': 'Contexto v002 usa huellas OSM (la manzana Preciados-Carmen baja a y~27); el poligono grafico de plaza de P01 se corrige en v2.2.',
    'pendientes_autor': ['reubicacion definitiva de las 5 capsulas recortadas de trenes (eliminadas en v002)',
                         'posicion definitiva de Carlos III (G2)'],
}
m['version'] = 'v002 (2026-08-07, Fase 03B)'

out = os.path.join(HERE, 'geometria_maestra_v002.json')
json.dump(m, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
print('v002 escrita:', out)
print('capsulas:', len(m['programa']['capsules']), '· mastiles:', len(m['estructura_ligera']['masts']),
      '· arboles nuevos:', len(m['paisaje']['new_trees']))
