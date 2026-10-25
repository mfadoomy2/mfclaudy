# -*- coding: utf-8 -*-
"""Sondeo forense: que objetos (en banda de cuerpo 0.05-2.10) rodean cada paso estrangulado."""
import audit_core as C

PTS = [(-54, -22), (-57, -17), (-50, -16), (-64, -16), (-31, -14), (-43, -14),
       (-70, -13), (73, -13), (46, -12), (66, -11), (43, 0)]
objs, M, B = C.load_scene()
mesh = [o for o in objs if o['kind'] == 'mesh' and o['layer'] not in C.NON_SOLID]
for (px, py) in PTS:
    print('== (%g,%g) ==' % (px, py))
    for o in mesh:
        lo = o['V'].min(0); hi = o['V'].max(0)
        if lo[0] - 1.6 < px < hi[0] + 1.6 and lo[1] - 1.6 < py < hi[1] + 1.6 and lo[2] < 2.10 and hi[2] > 0.05:
            print('   %-22s %-22s x[%.1f,%.1f] y[%.1f,%.1f] z[%.2f,%.2f]'
                  % (o['name'], o['layer'], lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))
