# -*- coding: utf-8 -*-
"""FASE FINAL - S04: CROSS_ANALYSIS_MATRIX.csv (§20) — 12 sistemas x 12 sistemas."""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..'))
MONT = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(MONT, '_FORENSIC_PROCESS'))
import flog  # noqa: E402

SIS = ['clima', 'movilidad', 'accesibilidad', 'agua', 'vegetacion', 'mantenimiento',
       'coste', 'uso', 'patrimonio', 'comercio', 'transporte', 'operacion']

# (a, b, tipo, mecanismo, datos, certeza)  — tipo: RELACION / POSIBLE / NO
REL = [
    ('clima', 'movilidad', 'RELACION',
     'los ejes despejados (regla A1) concentran el 85% del calor residual: paso libre '
     'vs sombra colisionan; solucion posible: sombra alta con galibo >=3 m',
     'D-015 · spots.json x corridors', 'A'),
    ('clima', 'uso', 'RELACION',
     'la estancia sigue al confort: 90,7% del IPE alto dentro del refugio; el proyecto '
     'sombrea las RAZONES de quedarse', 'D-004 · ipe.npy x refugio.npy', 'B'),
    ('clima', 'agua', 'RELACION',
     'el margen fino del confort (-1,1 K aire, +501 m2 refugio) es hidrico; el nucleo '
     '(-10,9 K MRT) es seco', 'CLI-05/07 · AGU-03', 'B'),
    ('clima', 'vegetacion', 'RELACION',
     'la vegetacion NO da la sombra (+-1 p.p. con LAI +-30%): da latente, superficie y '
     'experiencia', 'D-002 · sens_kveg', 'B'),
    ('clima', 'patrimonio', 'RELACION',
     'el dosel que enfria tapa el reloj: visibilidad ponderada por uso 33,6% (41,5% por '
     'superficie); 896 m2 de miradores', 'D-003 · pat_stats', 'A'),
    ('clima', 'mantenimiento', 'RELACION',
     'los 2 componentes de frecuencia mas corta (camara microalgas, niebla) son los de '
     'efecto climatico inmediato: mantener ES politica climatica', 'TEC-02 x CLI-10', 'B'),
    ('clima', 'coste', 'RELACION',
     'coste por persona-hora protegida 1,1-29 EUR segun uso: el retorno depende del uso',
     'D-014 · S-07', 'C'),
    ('clima', 'transporte', 'RELACION',
     'el atrio de la mayor estacion del centro es la primera sombra: puerta climatica '
     'de Madrid centro', 'URB-01 x CLI-09', 'B'),
    ('movilidad', 'accesibilidad', 'RELACION',
     'a suelo, permeabilidad intacta (0 RED); en vertical, equidad = 3 ascensores '
     '(N-1: 286 m)', 'MOB-01/02 · D-011', 'A'),
    ('movilidad', 'uso', 'RELACION',
     'estancia y paso no compiten: IPE alto fuera de ejes (filtro 2,05 del generador '
     'verificado 0 RED)', 'SOC-01 x a1', 'A'),
    ('agua', 'vegetacion', 'RELACION',
     'riego 4,4 m3/dia = 15% de la demanda pero el unico termino IRREVERSIBLE '
     '(arbolado); jerarquia de sequia arboles>laminas>niebla', 'AGU-01/03', 'B'),
    ('agua', 'operacion', 'RELACION',
     'autonomia 3,3 dias punta ante corte; la perdida real es solo evaporacion '
     '(recirculacion cerrada)', 'AGU-01', 'B'),
    ('agua', 'coste', 'RELACION',
     'el agua es el 3% del OPEX: el coste hidrico es mano de obra de sus sistemas, no '
     'el recurso', 'D-006 · ECO-01', 'B'),
    ('vegetacion', 'mantenimiento', 'RELACION',
     'jardineria = mayor partida OPEX (90 kEUR/ano BASE); infraestructura agnostica a '
     'la especie (plan B templado sin obra)', 'ECO-01 x AGU-02', 'B'),
    ('uso', 'comercio', 'POSIBLE',
     'confort->permanencia->exposicion existe en literatura; magnitud local incognita '
     'medible con aforos oficiales antes/despues', 'ECO-02 (C)', 'C'),
    ('uso', 'patrimonio', 'RELACION',
     'quien se queda ve MENOS reloj que quien pasa: la contemplacion comoda es un '
     'recurso escaso cartografiado', 'D-003', 'A'),
    ('mantenimiento', 'accesibilidad', 'RELACION',
     'SLA de ascensores = politica de equidad del nivel +6', 'D-011 · TEC-02', 'A'),
    ('mantenimiento', 'coste', 'RELACION',
     'OPEX dominado por conservacion (jardineria+limpieza+membrana = 72% del total '
     'BASE)', 'ECO-01', 'B'),
    ('transporte', 'comercio', 'POSIBLE',
     '73 M viajeros/ano vierten en la plaza; captura comercial incremental sin dato '
     'local: escenarios LOW/BASE/HIGH', 'F-01 · ECO-02', 'C'),
    ('operacion', 'clima', 'RELACION',
     'niebla por sensor de depresion psicrometrica (no calendario): la operacion '
     'inteligente vale +501 m2 de refugio los dias secos', 'D-013', 'B'),
    ('patrimonio', 'transporte', 'NO', 'sin interaccion medida mas alla del atrio', '—', '-'),
    ('comercio', 'agua', 'NO', 'sin relacion identificada', '—', '-'),
    ('accesibilidad', 'vegetacion', 'NO', 'sin relacion identificada', '—', '-'),
    ('patrimonio', 'agua', 'POSIBLE',
     'laminas de agua como espejo de Correos (valor escenico no cuantificado)', '—', 'C'),
]

# matriz simetrica resumida
idx = {s: i for i, s in enumerate(SIS)}
grid = [['' for _ in SIS] for _ in SIS]
for a, b, t, mec, dat, cert in REL:
    grid[idx[a]][idx[b]] = t
    grid[idx[b]][idx[a]] = t
for i in range(len(SIS)):
    grid[i][i] = '—'

with open(os.path.join(OUT, 'CROSS_ANALYSIS_MATRIX.csv'), 'w', encoding='utf-8-sig',
          newline='') as f:
    w = csv.writer(f)
    w.writerow(['MATRIZ'] + SIS)
    for s, row in zip(SIS, grid):
        w.writerow([s] + row)
    w.writerow([])
    w.writerow(['sistema_a', 'sistema_b', 'tipo', 'mecanismo', 'datos', 'certeza'])
    for r in REL:
        w.writerow(r)

n_rel = sum(1 for r in REL if r[2] == 'RELACION')
n_pos = sum(1 for r in REL if r[2] == 'POSIBLE')
flog.event(fase='FINAL', tipo_evento='cross_matrix',
           objetivo='CROSS_ANALYSIS_MATRIX.csv: 12x12 sistemas',
           resultado='%d relaciones confirmadas, %d posibles, %d no-relaciones declaradas'
                     % (n_rel, n_pos, sum(1 for r in REL if r[2] == 'NO')))
print('relaciones:', n_rel, '| posibles:', n_pos)
