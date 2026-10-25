# -*- coding: utf-8 -*-
"""FASE FINAL - MOTOR CONSTRUCTIVO (TEC-01..03) sobre v006.

Inventario completo de la escena por familia (cantidades reales del modelo), acceso de
mantenimiento (A9) y la matriz COMPONENTE -> FUNCION -> ACCESO -> FRECUENCIA -> RIESGO.
"""
import json
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
RC = os.path.normpath(os.path.join(BASE, '..'))
MONT = os.path.normpath(os.path.join(RC, '..'))
F9 = os.path.join(RC, 'FASE_03B9_HYPERDETAIL_V006')
OUT = os.path.join(BASE, '05_CONSTRUCCION_ESTRUCTURA_Y_MANTENIMIENTO', 'B_DATOS')
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
sys.path.insert(0, os.path.join(F9, '_reaudit9'))
import flog  # noqa: E402
import audit_core as AC  # noqa: E402

objs, m, B = AC.load_scene()
mesh = [o for o in objs if o['kind'] == 'mesh']

# ---------------------------------------------------------------- inventario por familia
def famclave(o):
    n = o['name']
    if n.startswith('VEGA_'):
        return 'VEGETACION (asset ' + n.split('_')[1] + ')'
    for pref in ('MAST', 'LEAF', 'CANOPY', 'RIB', 'STAIR', 'LIFT', 'POD', 'TANK', 'BAL',
                 'BENCH', 'POND', 'CURB', 'BASIN', 'DECK', 'CABLE', 'EST_', 'ATRIO',
                 'KIOSCO', 'CORREOS', 'ECI_', 'VEG2', 'RECIRC', 'MAIN', 'NEB', 'SUP'):
        if n.startswith(pref):
            return pref.rstrip('_')
    return o['layer']


inv = Counter()
inst = defaultdict(set)
for o in mesh:
    k = famclave(o)
    inv[k] += 1
    if o.get('anchor'):
        inst[k].add((round(o['anchor'][0], 1), round(o['anchor'][1], 1)))

inventario = {k: dict(mallas=v, instancias=len(inst[k]) or None)
              for k, v in sorted(inv.items(), key=lambda kv: -kv[1])}

a9 = json.load(open(os.path.join(F9, '_reaudit9', '_data', 'a9_maint.json'), encoding='utf-8'))
cats = defaultdict(list)
for r in a9:
    cats[r['cat']].append(r)
acceso = {c: dict(n=len(rs),
                  con_acceso=sum(1 for r in rs if r.get('acceso')),
                  plataforma=sum(1 for r in rs if r.get('requiere_plataforma')))
          for c, rs in cats.items()}

# ---------------------------------------------------------------- matriz de mantenimiento
# COMPONENTE -> FUNCION -> ACCESO -> FRECUENCIA -> RIESGO (frecuencias/vidas INFERIDO B
# por analogia con equipamiento urbano; cantidades MEDIDAS en la escena v006)
def n_de(*prefijos):
    tot = 0
    for k, v in inv.items():
        if any(k.startswith(p) for p in prefijos):
            tot += (len(inst[k]) or v)
    return tot


MATRIZ = [
    dict(componente='Mástiles estructurales', n=len(inst.get('MAST', [])) or inv.get('MAST', 0),
         funcion='soporte primario del dosel', acceso='desde suelo + línea de vida',
         frecuencia='inspección anual', vida='50 años', riesgo='BAJO',
         dependencia='ninguna (fundación propia)'),
    dict(componente='Hojas de dosel (canopy)', n=n_de('LEAF', 'CANOPY'),
         funcion='sombra + cámara de microalgas', acceso='plataforma elevadora desde claros',
         frecuencia='limpieza semestral · cámara quincenal', vida='15-20 años (membrana)',
         riesgo='MEDIO — cámara seca = +6,9 K local (CLI-10)', dependencia='bombeo microalgas'),
    dict(componente='Cinta (pasarela +6)', n=1,
         funcion='recorrido elevado 733 m', acceso='propio tablero; juntas cada 18 m, tapas cada 36 m',
         frecuencia='inspección trimestral de juntas', vida='30 años (tablero)',
         riesgo='MEDIO — elemento con público', dependencia='43 soportes'),
    dict(componente='Ascensores', n=3,
         funcion='itinerario accesible al +6', acceso='cuartos técnicos propios',
         frecuencia='mensual (normativa aparatos)', vida='20 años',
         riesgo='ALTO para equidad — N−1 = 286 m de rodeo (MOB-02)', dependencia='energía'),
    dict(componente='Escaleras', n=6,
         funcion='acceso general al +6', acceso='directo',
         frecuencia='inspección anual', vida='40 años', riesgo='BAJO', dependencia='—'),
    dict(componente='Pods rosa', n=n_de('POD'),
         funcion='estancia/servicio inflable', acceso='desde suelo; válvula e inflado propios',
         frecuencia='presión semanal · recambio membrana 8-10 años', vida='10 años',
         riesgo='MEDIO — vandalismo', dependencia='soplante'),
    dict(componente='Depósitos-gota', n=acceso.get('DEPOSITO +10.5', {}).get('n', 12),
         funcion='almacenamiento 99,8 m³', acceso='%d de %d con acceso auditado; plataforma' %
                (acceso.get('DEPOSITO +10.5', {}).get('con_acceso', 0),
                 acceso.get('DEPOSITO +10.5', {}).get('n', 0)),
         frecuencia='purga mensual · limpieza anual', vida='25 años',
         riesgo='MEDIO — carga en altura', dependencia='estructura mástil'),
    dict(componente='Red hidráulica enterrada', n=4,
         funcion='mains + recirculación', acceso='tapas de registro cada 9 m',
         frecuencia='inspección anual · purga estacional', vida='30 años',
         riesgo='BAJO (enterrada, registrable)', dependencia='bombas'),
    dict(componente='Nebulizadores', n=42,
         funcion='enfriamiento evaporativo', acceso='desde suelo (cabezal a 3,5 m)',
         frecuencia='boquillas trimestral (cal)', vida='7 años',
         riesgo='MEDIO — agua dura de Madrid', dependencia='bomba alta presión + agua'),
    dict(componente='Balsas y estanques', n=acceso.get('BALSA', {}).get('n', 0) or n_de('POND', 'BASIN'),
         funcion='lámina fría + microecosistema', acceso='borde practicable',
         frecuencia='limpieza mensual · vaciado anual', vida='30 años (vaso)',
         riesgo='MEDIO — calidad de agua estival', dependencia='recirculación'),
    dict(componente='Barandillas y remates', n=n_de('BAL'),
         funcion='protección de borde', acceso='directo',
         frecuencia='repaso anual', vida='25 años', riesgo='BAJO', dependencia='—'),
    dict(componente='Mobiliario (bancos)', n=n_de('BENCH'),
         funcion='estancia', acceso='directo', frecuencia='repaso anual', vida='15 años',
         riesgo='BAJO', dependencia='—'),
]

R = dict(baseline='v006 build 12',
         escena=dict(mallas=len(mesh), objetos=len(objs)),
         inventario=inventario, acceso_a9=acceso, matriz=MATRIZ)

with open(os.path.join(OUT, 'tec_stats.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)

import csv
with open(os.path.join(OUT, 'matriz_mantenimiento.csv'), 'w', encoding='utf-8-sig',
          newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(MATRIZ[0].keys()))
    w.writeheader(); w.writerows(MATRIZ)

flog.event(fase='FINAL', tipo_evento='motor_tecnico',
           objetivo='TEC: inventario de escena por familia + matriz de mantenimiento',
           resultado='%d mallas; %d categorias A9 (todas con acceso: %s); matriz de %d componentes'
                     % (len(mesh), len(acceso),
                        all(v['con_acceso'] == v['n'] for v in acceso.values()), len(MATRIZ)))
print('mallas:', len(mesh))
print('top familias:', dict(list(inventario.items())[:8]))
print('acceso A9:', json.dumps(acceso, ensure_ascii=False)[:400])
