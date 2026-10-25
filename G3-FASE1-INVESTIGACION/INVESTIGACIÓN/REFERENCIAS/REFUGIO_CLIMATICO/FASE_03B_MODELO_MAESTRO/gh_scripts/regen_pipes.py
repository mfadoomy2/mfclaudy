# -*- coding: utf-8 -*-
"""RhinoPython — ejecutar DENTRO de Rhino (RunPythonScript) con MASTER_ARCHITECTURE_v002.3dm abierto.
Convierte las curvas generatrices (30_CURVES, 05_CABLES, 13_PIPES) en Pipes NURBS reales."""
import rhinoscriptsyntax as rs

SPEC = [
    ('30_CURVES', 'AXIS_', 0.30, '02_PRIMARY_STRUCTURE'),     # ejes de loops -> tubo principal
    ('30_CURVES', 'RIBBON_AXIS', 0.20, '02_PRIMARY_STRUCTURE'),
    ('30_CURVES', 'PIPE_AXIS', 0.16, '13_PIPES'),
    ('30_CURVES', 'BASIN_AXIS', 0.12, '03_SECONDARY_STRUCTURE'),
    ('13_PIPES', 'RISER', 0.08, '13_PIPES'),
    ('05_CABLES', '', 0.008, '05_CABLES'),                     # cables Ø16 mm
]

rs.EnableRedraw(False)
total = 0
for (layer, prefix, radius, out_layer) in SPEC:
    ids = rs.ObjectsByLayer(layer) or []
    for oid in ids:
        if rs.IsCurve(oid):
            name = rs.ObjectName(oid) or ''
            if prefix and not name.startswith(prefix):
                continue
            pipe = rs.AddPipe(oid, 0, radius, cap=1)
            if pipe:
                for p in (pipe if isinstance(pipe, list) else [pipe]):
                    rs.ObjectLayer(p, out_layer)
                    rs.ObjectName(p, 'NURBS_' + name)
                total += 1
rs.EnableRedraw(True)
print('Pipes NURBS generados sobre %d curvas. Las mallas proxy pueden apagarse u ocultarse.' % total)
