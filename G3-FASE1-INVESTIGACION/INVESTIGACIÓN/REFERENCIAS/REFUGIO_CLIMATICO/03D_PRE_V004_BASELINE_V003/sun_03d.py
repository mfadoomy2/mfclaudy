# -*- coding: utf-8 -*-
"""03D: posiciones solares reales (PSA, validado vs PVGIS en 03B.5B) para las 2 luces de render."""
import datetime as dt
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', 'FASE_03B6_RESOLUCION', '_reclima')))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', 'FASE_03B6_RESOLUCION', '_reaudit')))
import clima_core as CC

out = {}
for nombre, hloc in (('mediodia', 14.0), ('tarde', 17.5)):
    t = dt.datetime(2026, 7, 21, int(hloc - 2), int((hloc % 1) * 60))   # CEST = UTC+2
    el, az = CC.sun_position(t)
    # vector three/blender: +X este, +Y norte, +Z arriba; az desde N hacia E
    d = 200.0
    x = d * math.cos(math.radians(el)) * math.sin(math.radians(az))
    y = d * math.cos(math.radians(el)) * math.cos(math.radians(az))
    z = d * math.sin(math.radians(el))
    out[nombre] = dict(hora_local='%.1f CEST 21-jul' % hloc, elevacion=round(el, 2), azimut_N_E=round(az, 2),
                       dir_xyz=[round(x, 1), round(y, 1), round(z, 1)])
json.dump(out, open(os.path.join(HERE, 'SUN_03D.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
