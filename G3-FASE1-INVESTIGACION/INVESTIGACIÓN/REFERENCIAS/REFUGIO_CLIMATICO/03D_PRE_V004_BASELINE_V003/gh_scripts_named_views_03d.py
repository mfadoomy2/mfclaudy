# -*- coding: utf-8 -*-
"""RhinoPython (ejecutar DENTRO de Rhino 8 con SOL_PRESENTATION_MASTER_v001.3dm abierto):
crea las 7 vistas nombradas H1..H7 de 03D con lente equivalente al fov vertical del brief.
_RunPythonScript o editor de RhinoScript. NO modifica geometria."""
import math

import rhinoscriptsyntax as rs

CAMS = [
    ('H1', (-2, -18, 1.65), (6, 16, 5.0), 62),
    ('H2', (-56, 2, 1.65), (-44, 18, 5.5), 68),
    ('H3', (24, -10, 1.65), (14, -1, 1.2), 66),
    ('H4', (6, 8, 1.65), (-25.2, -36.5, 15.0), 58),
    ('H5', (-12.8, 28.8, 7.55), (10, 26, 6.5), 63),
    ('H6', (22, -4, 1.65), (33, 5, 4.5), 68),
    ('H7', (0, -80, 42), (2, 12, 0), 55),
]
SENSOR_V = 24.0   # mm (fov del brief es VERTICAL)
for (nombre, cam, tgt, fov) in CAMS:
    lens = SENSOR_V / (2 * math.tan(math.radians(fov / 2)))
    rs.ViewCameraTarget(camera=cam, target=tgt)
    rs.ViewCameraLens(lens_length=lens)
    rs.Command('_-NamedView _Save 03D_%s _Enter' % nombre, echo=False)
    print('vista', nombre, 'lente %.1f mm' % lens)
print('7 vistas nombradas 03D_H1..H7 creadas')
