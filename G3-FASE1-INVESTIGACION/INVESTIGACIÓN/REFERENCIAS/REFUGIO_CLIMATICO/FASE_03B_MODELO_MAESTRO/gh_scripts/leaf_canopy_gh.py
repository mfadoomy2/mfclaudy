# -*- coding: utf-8 -*-
"""RhinoPython — LEAF_CANOPY_MASTER en NURBS nativo. Ejecutar dentro de Rhino.
Parametros identicos a la familia de build_all_03b.leaf_canopy()."""
import math

import rhinoscriptsyntax as rs

# ------------------- PARAMETROS (editar aqui o convertir a GHPython inputs) -------------------
L = 5.2            # eje mayor (m)
W = 5.2            # eje menor (m)
Z = 6.75           # cota del aro
ROTATION = 0.0     # grados
CENTRAL_DROP = 0.47   # embudo (0.18*R por defecto)
MEMBRANE_SAG = 0.21   # flecha adicional
RIM_SECTION = 0.12    # diametro del tubo del aro
RIB_COUNT = 10
INCLINATION = 0.0     # grados
CX, CY = 0.0, 0.0

rx, ry = L / 2.0, W / 2.0
tilt = math.radians(INCLINATION)
rot = math.radians(ROTATION)


def pt(a_deg, f):
    a = math.radians(a_deg)
    x, y = rx * f * math.cos(a), ry * f * math.sin(a)
    xr = x * math.cos(rot) - y * math.sin(rot)
    yr = x * math.sin(rot) + y * math.cos(rot)
    z = Z - CENTRAL_DROP * (1 - f) ** 1.6 - MEMBRANE_SAG * math.sin(math.pi * f) * 0.5 + math.sin(tilt) * xr
    return (CX + xr, CY + yr, z)


rs.EnableRedraw(False)
# aro
rim_pts = [pt(a, 1.0) for a in range(0, 361, 6)]
rim = rs.AddInterpCurve(rim_pts, degree=3)
rs.AddPipe(rim, 0, RIM_SECTION / 2.0, cap=1)
# membrana: loft de anillos concentricos
rings = []
for j in range(6):
    f = max(j / 5.0, 0.02)
    rings.append(rs.AddInterpCurve([pt(a, f) for a in range(0, 361, 10)], degree=3))
srf = rs.AddLoftSrf(rings)
# nervios
for k in range(RIB_COUNT):
    a = 360.0 * k / RIB_COUNT
    rib = rs.AddInterpCurve([pt(a, f) for f in (0.02, 0.3, 0.6, 1.0)], degree=3)
    rs.AddPipe(rib, 0, 0.035, cap=1)
# bajante
c0 = pt(0, 0.02)
rs.AddPipe(rs.AddLine(c0, (c0[0], c0[1], c0[2] - 0.55)), 0, 0.08, cap=1)
rs.EnableRedraw(True)
print('LEAF_CANOPY NURBS: L=%.2f W=%.2f Z=%.2f ribs=%d' % (L, W, Z, RIB_COUNT))
