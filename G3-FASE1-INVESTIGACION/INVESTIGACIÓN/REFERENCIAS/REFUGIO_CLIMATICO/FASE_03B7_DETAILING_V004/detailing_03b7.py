# -*- coding: utf-8 -*-
"""03B.7 §6-§20 — DETALLE INFORMACIONAL LOD B/C para las familias v004.
Cada detalle explica como se construye/usa/mantiene la pieza. Consumido por build_all_03b7:
  upgrade_blocks(BLOCKS, mk, rng)  -> enriquece bloques existentes + especies vegetales v2
  (los extras de obra — despiece, atrio, Correos, Estacion — viven como hooks en el generador)
"""
import math


def _rot_pt(x, y, a):
    return (x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a))


def _fan(mk, cx, cy, cz, ax, r, n=5, tilt=0.35):
    """abanico foliar orientado: n triangulos desde un punto (follaje legible, no esfera)."""
    V = [(cx, cy, cz)]
    F = []
    for k in range(n + 1):
        a = ax - 0.55 + 1.1 * k / n
        V.append((cx + r * math.cos(a), cy + r * math.sin(a), cz + tilt * r * (0.4 + 0.2 * (k % 2))))
    for k in range(n):
        F.append((0, k + 1, k + 2))
    return (V, F)


def upgrade_blocks(BLOCKS, mk, rng):
    n0 = {k: len(v) for k, v in BLOCKS.items()}

    # ---------- §12 MASTILES: placa base + pernos + transicion + casquillo + abrazaderas + valvula
    for nm in ('MAST_1', 'MAST_2', 'MAST_3'):
        P = BLOCKS[nm]
        P[:] = [pt for pt in P if pt[0] != '15_VEGETATION_FULL']   # fuera la BOLA-arbusto del tiesto base
        for j in range(6):                                          # mata foliar en el tiesto (§17)
            aj = 2 * math.pi * j / 6 + 0.3
            P.append(('15_VEGETATION_FULL',
                      _fan(mk, 0.36 * math.cos(aj), 0.36 * math.sin(aj),
                           0.58 + 0.12 * (j % 3), aj, 0.52, 4, 0.45)))
        P.append(('04_MASTS', mk.cylinder((0, 0, 0.0), (0, 0, 0.03), 0.30, 14)))          # placa base
        for a in (0.5, 2.07, 3.64, 5.21):                                                  # 4 pernos
            P.append(('19_DETALLE', mk.cylinder((0.22 * math.cos(a), 0.22 * math.sin(a), 0.03),
                                                (0.22 * math.cos(a), 0.22 * math.sin(a), 0.085), 0.02, 5)))
        P.append(('04_MASTS', mk.cylinder((0, 0, 2.86), (0, 0, 3.14), 0.145, 10)))         # casquillo bifurcacion
        P.append(('19_DETALLE', mk.torus((0, 0, 1.9), 0.125, 0.018, 10, 4)))               # abrazadera
        P.append(('13_PIPES', mk.torus((0.14, 0.09, 1.2), 0.055, 0.014, 8, 4)))            # valvula de riego
        P.append(('19_DETALLE', mk.cylinder((0.14, 0, 4.0), (0.14, 0, 4.1), 0.045, 6)))    # collar del cabezal

    # ---------- §13 PODS: costuras completas + paralelos + valvula + pletinas de pata
    for nm, dia in (('POD_S', 2.25), ('POD_M', 3.25), ('POD_L', 4.5)):
        P = BLOCKS[nm]
        r = dia / 2
        for adeg in (30, 90, 150, 210, 270, 330):                                          # +6 meridianos
            arc = []
            a = math.radians(adeg)
            for t in range(13):
                ph = math.pi * t / 12
                arc.append((r * math.sin(ph) * math.cos(a), r * math.sin(ph) * math.sin(a),
                            r + 0.3 + r * math.cos(ph)))
            P.append(('19_DETALLE', mk.tube(arc, 0.018, 4)))
        for phdeg in (55, 125):                                                            # 2 paralelos
            ph = math.radians(phdeg)
            rr = r * math.sin(ph)
            P.append(('19_DETALLE', mk.torus((0, 0, r + 0.3 + r * math.cos(ph)), rr, 0.018, 14, 4)))
        P.append(('19_DETALLE', mk.cylinder((0.16, 0, dia + 0.30), (0.16, 0, dia + 0.42), 0.035, 5)))  # valvula
        for adeg in (30, 150, 270):                                                        # pletinas de pata
            a = math.radians(adeg)
            P.append(('19_DETALLE', mk.box((r * 0.9 * math.cos(a), r * 0.9 * math.sin(a), 0.005),
                                           0.2, 0.2, 0.02)))

    # POD_TRAIN: mas ventanas + puerta con marco + faldon
    PT = BLOCKS['POD_TRAIN']
    for dx in (-2.4, 2.4):
        ring = []
        for t in range(21):
            a = 2 * math.pi * t / 20
            ring.append((dx, 1.05 * math.cos(a), 1.5 + 1.05 * math.sin(a)))
        PT.append(('19_DETALLE', mk.tube(ring, 0.03, 4)))
    door = []
    for t in range(17):
        a = 2 * math.pi * t / 16
        door.append((2.72, 0.55 * math.cos(a), 1.35 + 0.75 * math.sin(a)))
    PT.append(('19_DETALLE', mk.tube(door, 0.035, 5)))                                     # marco de puerta
    PT.append(('03_SECONDARY_STRUCTURE', mk.box((0, 0, 0.06), 5.3, 2.2, 0.12)))            # faldon base

    # ---------- §15 GOTAS: tapa + valvula + rebosadero + indicador + patas
    D = BLOCKS['DROP_TANK']
    D.append(('19_DETALLE', mk.cylinder((0, 0, 2.25), (0, 0, 2.31), 0.34, 10)))            # tapa
    D.append(('19_DETALLE', mk.cylinder((0.78, 0, 0.75), (0.95, 0, 0.75), 0.03, 5)))       # valvula lateral
    D.append(('19_DETALLE', mk.torus((0.99, 0, 0.75), 0.05, 0.012, 8, 4)))                 # volante
    D.append(('13_PIPES', mk.cylinder((0.55, 0.5, 1.35), (0.72, 0.62, 1.15), 0.025, 5)))   # rebosadero
    D.append(('19_DETALLE', mk.cylinder((-0.68, 0.35, 0.35), (-0.62, 0.32, 1.5), 0.015, 4)))  # indicador nivel
    for a in (0.9, 3.0, 5.1):
        D.append(('19_DETALLE', mk.box((0.55 * math.cos(a), 0.55 * math.sin(a), 0.01), 0.16, 0.16, 0.02)))

    # ---------- NEB_POST: cabezal conico + collar + valvula
    N = BLOCKS['NEB_POST']
    N.append(('19_DETALLE', mk.cylinder((0, 0, 3.82), (0, 0, 3.98), 0.065, 6)))            # collar
    N.append(('13_PIPES', mk.cylinder((0, 0, 1.15), (0.11, 0, 1.15), 0.02, 4)))            # valvula
    cone = [(0.09 * math.cos(2 * math.pi * t / 8), 0.09 * math.sin(2 * math.pi * t / 8), 4.0) for t in range(9)]
    N.append(('19_DETALLE', (([(0, 0, 4.14)] + cone), [(0, 1 + i, 1 + (i + 1) % 8) for i in range(8)])))

    # ---------- TOTEM: pantalla + base
    T = BLOCKS['TOTEM']
    T.append(('19_DETALLE', mk.box((0, 0.075, 0.95), 0.36, 0.012, 0.5)))                   # pantalla
    T.append(('19_DETALLE', mk.box((0, 0, 0.015), 0.6, 0.28, 0.03)))                       # base

    # ---------- §9 ESCALERA: narices + montantes + retornos + pletina + LED + canaleta
    S = BLOCKS['STAIR_SB']
    CH, HU = 6.0 / 35, 0.29
    XA = -2.6
    xa = XA + 18 * HU
    xb = xa - 17 * HU
    for k in range(18):                                                                     # narices tramo A
        S.append(('19_DETALLE', mk.box((XA + HU * (k + 0.5) - HU / 2 + 0.015, 0, CH * (k + 1) + 0.004),
                                       0.03, 1.4, 0.012)))
    for k in range(17):                                                                     # narices tramo B
        S.append(('19_DETALLE', mk.box((xa - HU * (k + 0.5) + HU / 2 - 0.015, -1.55, CH * (19 + k) + 0.004),
                                       0.03, 1.4, 0.012)))
    for y0 in (-0.75, 0.75):                                                                # montantes tramo A
        for k in range(0, 18, 3):
            x0 = XA + HU * (k + 0.5)
            z0 = CH * (k + 1)
            S.append(('03_SECONDARY_STRUCTURE', mk.cylinder((x0, y0, z0), (x0, y0, z0 + 0.68), 0.018, 5)))
    for y0 in (-2.3, -0.8):                                                                 # montantes tramo B
        for k in range(0, 17, 3):
            x0 = xa - HU * (k + 0.5)
            z0 = CH * (19 + k)
            S.append(('03_SECONDARY_STRUCTURE', mk.cylinder((x0, y0, z0), (x0, y0, z0 + 0.68), 0.018, 5)))
    for y0 in (-0.75, 0.75):                                                                # retorno arranque
        S.append(('03_SECONDARY_STRUCTURE', mk.cylinder((XA - 0.3, y0, 0.95), (XA, y0, 0.95), 0.028, 5)))
    S.append(('19_DETALLE', mk.box((XA - 0.1, 0, 0.005), 0.5, 1.6, 0.012)))                 # pletina arranque
    S.append(('19_DETALLE', mk.box((XA + 2.6, 0, 0.002), 5.2, 0.12, 0.006)))                # canaleta pie... (drenaje)
    S.append(('19_DETALLE', mk.cylinder((xa + 0.75, -0.775, 3.02), (xa + 0.75, -0.775, 3.05), 0.09, 8)))  # luminaria meseta

    # ---------- §10 ASCENSOR: puertas + boton + coronacion tecnica + pasamanos interior
    L = BLOCKS['LIFT_TOWER']
    for zdoor in (0.0, 5.97):                                                               # jambas y dintel (lado -y = tablero arriba, +y abajo)
        yd = -1.16 if zdoor > 1 else 1.16
        for xd in (-0.55, 0.55):
            L.append(('03_SECONDARY_STRUCTURE', mk.box((xd, yd, zdoor + 1.05), 0.09, 0.09, 2.1)))
        L.append(('03_SECONDARY_STRUCTURE', mk.box((0, yd, zdoor + 2.13), 1.25, 0.09, 0.09)))
        L.append(('19_DETALLE', mk.box((0.02, yd * 1.02, zdoor + 1.0), 0.02, 0.02, 1.95)))  # junta de hojas
    L.append(('19_DETALLE', mk.box((1.45, 0.6, 0.55), 0.14, 0.14, 1.1)))                    # botonera
    L.append(('03_SECONDARY_STRUCTURE', mk.cylinder((0, 0, 7.4), (0, 0, 7.9), 0.85, 14)))   # caseton tecnico
    for a in (0.4, 1.97, 3.54, 5.11):
        L.append(('19_DETALLE', mk.box((0.85 * math.cos(a), 0.85 * math.sin(a), 7.65), 0.05, 0.3, 0.3)))  # rejillas
    L.append(('19_DETALLE', mk.torus((0, 0, 1.1), 0.82, 0.02, 14, 4)))                      # pasamanos cabina
    L.append(('19_DETALLE', mk.cylinder((0, 0, 0.02), (0, 0, 0.05), 1.0, 14)))              # piso cabina

    # ---------- §17 VEGETACION v2: especies con ramificacion y follaje LEGIBLE
    def arbol_v2(h, rcopa, nramas, seed):
        P = [('15_VEGETATION_FULL', mk.cylinder((0, 0, 0), (0.03, 0.02, h * 0.35), 0.16, 8)),
             ('15_VEGETATION_FULL', mk.cylinder((0.03, 0.02, h * 0.35), (0.05, 0.03, h * 0.58), 0.11, 7))]
        base = 2.55
        for k in range(nramas):
            a = 2 * math.pi * k / nramas + seed * 0.7
            e1 = (0.9 * math.cos(a), 0.9 * math.sin(a), h * 0.62)
            e2 = (1.8 * math.cos(a) * 1.1, 1.8 * math.sin(a) * 1.1, h * 0.72 + 0.25 * (k % 3))
            P.append(('15_VEGETATION_FULL', mk.cylinder((0.05, 0.03, h * 0.55), e1, 0.055, 5)))
            P.append(('15_VEGETATION_FULL', mk.cylinder(e1, e2, 0.032, 4)))
            for j in range(2):
                aa = a + (j - 0.5) * 0.5
                cz = max(e2[2] + 0.32 + 0.22 * ((k + j) % 2), base + 0.55)
                P.append(('15_VEGETATION_FULL',
                          _fan(mk, e2[0] * (1 + 0.18 * j), e2[1] * (1 + 0.18 * j), cz, aa,
                               rcopa * (0.55 + 0.2 * ((k + j) % 3) / 2), 5, 0.4)))
        cz0 = max(h * 0.78, base + rcopa * 0.5)
        for k in range(5):
            a = 2 * math.pi * k / 5 + 0.9 * seed
            P.append(('15_VEGETATION_FULL', _fan(mk, 0.5 * math.cos(a), 0.5 * math.sin(a),
                                                 cz0 + 0.2 * (k % 2), a, rcopa * 0.7, 6, 0.3)))
        return P

    BLOCKS['VEG2_ARBOL_A'] = arbol_v2(5.2, 2.1, 6, 1)
    BLOCKS['VEG2_ARBOL_B'] = arbol_v2(6.2, 1.9, 7, 2)
    BLOCKS['VEG2_ARBOL_EX'] = arbol_v2(7.2, 2.7, 7, 3)

    # alocasia §7.1 (ahora si: la geometria v004 es la rama de detalle)
    P = [('15_VEGETATION_FULL', mk.sphere((0, 0, 0.22), 0.26, 6, 5))]
    for k in range(7):
        a = 2 * math.pi * k / 7 + 0.3
        Lt = 0.9 + 0.5 * ((k * 37) % 10) / 10
        tip = (Lt * math.cos(a), Lt * math.sin(a), 0.7 + 0.45 * (k % 3))
        P.append(('15_VEGETATION_FULL', mk.cylinder((0, 0, 0.15), tip, 0.03, 4)))
        V, F = [], []
        nseg = 14
        for t in range(nseg + 1):
            f = t / nseg
            wid = 0.34 * math.sin(math.pi * min(f * 1.15, 1.0))
            dz = 0.16 * math.sin(math.pi * f) - 0.1 * f
            bx = tip[0] + (0.25 + 0.75 * f) * math.cos(a)
            by = tip[1] + (0.25 + 0.75 * f) * math.sin(a)
            V.append((bx - wid * math.sin(a), by + wid * math.cos(a), tip[2] + dz + 0.1))
            V.append((bx + wid * math.sin(a), by - wid * math.cos(a), tip[2] + dz + 0.1))
        for t in range(nseg):
            i2 = 2 * t
            F += [(i2, i2 + 2, i2 + 3), (i2, i2 + 3, i2 + 1)]
        P.append(('15_VEGETATION_FULL', (V, F)))
    BLOCKS['VEG2_TROPICAL'] = P

    # gramineas + matas foliares (control 50 cm: NADA de esferas — abanicos bajos solapados)
    P = []
    for (dx, dy, r) in ((0, 0, 0.40), (0.5, 0.25, 0.28)):
        for j in range(5):
            aj = 2 * math.pi * j / 5 + dx * 3
            P.append(('15_VEGETATION_FULL',
                      _fan(mk, dx + 0.08 * math.cos(aj), dy + 0.08 * math.sin(aj),
                           0.10 + 0.09 * (j % 3), aj, r * 1.15, 4, 0.5)))
    for k in range(14):
        a = 2 * math.pi * k / 14 + 0.2
        x0, y0 = 0.5 * math.cos(a), 0.5 * math.sin(a)
        hh = 0.5 + 0.4 * ((k * 53) % 10) / 10
        P.append(('15_VEGETATION_FULL', ([(x0, y0, 0), (x0 + 0.04, y0 + 0.01, 0),
                                          (x0 + 0.10 * math.cos(a), y0 + 0.10 * math.sin(a), hh)], [(0, 1, 2)])))
    BLOCKS['VEG2_BAJA'] = P

    # trepadora v2: la helice se queda, las MATAS-ESFERA se vuelven follaje adherido al fuste
    P = []
    hel = []
    for t in range(30):
        f = t / 29
        a = f * 5.2
        hel.append((0.19 * math.cos(a), 0.19 * math.sin(a), f * 3.0))
    P.append(('15_VEGETATION_FULL', mk.tube(hel, 0.045, 5)))
    for t in range(2, 30, 3):
        hx, hy, hz = hel[t]
        aa = math.atan2(hy, hx)
        P.append(('15_VEGETATION_FULL', _fan(mk, hx * 1.7, hy * 1.7, hz, aa, 0.30 + 0.10 * (t % 3), 4, 0.25)))
        P.append(('15_VEGETATION_FULL', _fan(mk, hx * 1.4, hy * 1.4, hz + 0.14, aa + 2.4, 0.22, 3, -0.15)))
    for k in range(5):   # derrame superior: guias colgando con hojas, no esferas
        a = 0.5 + k * 1.15
        g0 = (0.55 * math.cos(a), 0.55 * math.sin(a))
        guia = [(g0[0] * (1 + 0.5 * f), g0[1] * (1 + 0.5 * f), 3.15 - 0.55 * f) for f in [j / 4 for j in range(5)]]
        P.append(('15_VEGETATION_FULL', mk.tube(guia, 0.014, 4)))
        for (gx, gy, gz) in guia[1::2]:
            P.append(('15_VEGETATION_FULL', _fan(mk, gx, gy, gz, math.atan2(gy, gx), 0.24, 3, -0.3)))
    BLOCKS['VEG2_TREPADORA'] = P

    # colgante v2: guias con hojas-quad
    P = []
    for k in range(4):
        a = 2 * math.pi * k / 4 + 0.4
        x0, y0 = 0.25 * math.cos(a), 0.25 * math.sin(a)
        Lc = 1.4 + 0.9 * ((k * 41) % 10) / 10
        guia = [(x0 + 0.1 * math.sin(f * 5 + k), y0 + 0.08 * math.cos(f * 4), -f * Lc)
                for f in [j / 7 for j in range(8)]]
        P.append(('15_VEGETATION_FULL', mk.tube(guia, 0.012, 4)))
        for j in range(1, 8, 2):
            gx, gy, gz = guia[j]
            P.append(('15_VEGETATION_FULL', ([(gx, gy, gz), (gx + 0.16, gy + 0.05, gz - 0.07),
                                              (gx + 0.05, gy + 0.17, gz - 0.1)], [(0, 1, 2)])))
            P.append(('15_VEGETATION_FULL', ([(gx, gy, gz - 0.04), (gx - 0.15, gy - 0.06, gz - 0.12),
                                              (gx - 0.04, gy - 0.16, gz - 0.14)], [(0, 1, 2)])))
    BLOCKS['VEG2_COLGANTE'] = P

    # huerto v2: 3 cultivos + etiqueta
    P = [('09_PLANTERS', mk.box((0, 0, 0), 2.6, 0.7, 0.26))]
    for k in range(5):
        x0 = -1.05 + k * 0.525
        if k % 3 == 0:      # tomatera
            P.append(('15_VEGETATION_FULL', mk.cylinder((x0, 0.1, 0.26), (x0, 0.05, 1.5), 0.02, 4)))
            for j in range(3):
                P.append(('15_VEGETATION_FULL', mk.sphere((x0 + 0.08 * (j - 1), 0.12, 0.6 + 0.35 * j), 0.14, 5, 4)))
            P.append(('13_PIPES', mk.sphere((x0 + 0.1, 0.18, 0.85), 0.045, 4, 3)))
        elif k % 3 == 1:    # lechuga-roseta
            for j in range(6):
                a = 2 * math.pi * j / 6
                P.append(('15_VEGETATION_FULL', ([(x0, 0, 0.30), (x0 + 0.16 * math.cos(a - 0.4), 0.16 * math.sin(a - 0.4), 0.42),
                                                  (x0 + 0.2 * math.cos(a + 0.2), 0.2 * math.sin(a + 0.2), 0.5)], [(0, 1, 2)])))
        else:               # aromatica
            P.append(('15_VEGETATION_FULL', mk.sphere((x0, 0, 0.42), 0.19, 5, 4)))
    for k in range(3):
        x0 = -0.8 + k * 0.8
        P.append(('10_FURNITURE', mk.cylinder((x0, 0.12, 0.26), (x0, 0.05, 1.7), 0.02, 4)))
    P.append(('13_PIPES', mk.tube([(-1.3, -0.2, 0.3), (0, -0.22, 0.3), (1.3, -0.2, 0.3)], 0.03, 5)))
    P.append(('19_DETALLE', mk.box((1.2, -0.3, 0.45), 0.02, 0.14, 0.18)))                    # etiqueta
    BLOCKS['VEG2_HUERTO'] = P

    # acuatica v2: nenufar con muesca + flor
    P = []
    for k in range(6):
        a = 2 * math.pi * k / 6
        x0, y0 = 0.22 * math.cos(a), 0.22 * math.sin(a)
        P.append(('15_VEGETATION_FULL', mk.cylinder((x0, y0, 0), (x0 * 1.6, y0 * 1.6, 0.75 + 0.3 * (k % 2)), 0.02, 4)))
    for (dx, dy) in ((0.55, 0.1), (-0.4, 0.45), (0.15, -0.5)):
        V = [(dx, dy, 0.012)]
        F = []
        for t in range(9):
            a = 0.5 + 5.5 * t / 8
            V.append((dx + 0.24 * math.cos(a), dy + 0.24 * math.sin(a), 0.012))
        for t in range(8):
            F.append((0, t + 1, t + 2))
        P.append(('15_VEGETATION_FULL', (V, F)))
    P.append(('08_PINK_MODULES', mk.sphere((0.1, 0.2, 0.06), 0.05, 5, 4)))                   # flor
    BLOCKS['VEG2_ACUATICA'] = P

    # ---------- §11 DISCOS: kingpost + tensores + rim doble + manguitos + rebosadero + labio
    DIMS = {'LEAF_S1': 1.5, 'LEAF_S2': 1.8, 'LEAF_M1': 2.3, 'LEAF_M2': 2.6, 'LEAF_MT': 2.4,
            'LEAF_OV': 2.9, 'LEAF_L1': 3.2, 'LEAF_LT': 3.4, 'LEAF_XL': 4.2}
    for nm, r in DIMS.items():
        P = BLOCKS[nm]
        P.append(('03_SECONDARY_STRUCTURE', mk.cylinder((0, 0, 0), (0, 0, 0.9 + r * 0.12), 0.05, 6)))  # kingpost
        for adeg in (10, 130, 250):                                                        # tensores rim->kingpost
            a = math.radians(adeg)
            P.append(('05_CABLES', mk.cylinder((r * math.cos(a), r * math.sin(a), 0.0),
                                               (0, 0, 0.9 + r * 0.12), 0.012, 4)))
        P.append(('03_SECONDARY_STRUCTURE', mk.torus((0, 0, -0.06), r * 0.995, 0.028, 20, 4)))  # rim inferior doble
        for adeg in range(0, 360, 60):                                                     # manguitos nervio-aro
            a = math.radians(adeg)
            P.append(('19_DETALLE', mk.cylinder((r * 0.97 * math.cos(a), r * 0.97 * math.sin(a), -0.02),
                                                (r * 1.01 * math.cos(a), r * 1.01 * math.sin(a), -0.02), 0.05, 5)))
        P.append(('13_PIPES', mk.cylinder((r * 0.82, 0, -0.1), (r * 1.12, 0, -0.22), 0.028, 5)))  # rebosadero
        for j in range(3):                                                                 # goteo del rebosadero
            P.append(('12_MIST', mk.sphere((r * 1.14, 0, -0.42 - 0.28 * j), 0.035, 4, 3)))
        P.append(('19_DETALLE', mk.torus((0, 0, -0.31 * 0.35 + 0.055), r * 0.82, 0.02, 18, 4)))   # labio lamina

    return {k: len(BLOCKS[k]) - n0.get(k, 0) for k in BLOCKS if len(BLOCKS[k]) != n0.get(k, 0)}


# ==================== DETALLES DE OBRA (site_details: se llama desde build_site) ====================
def site_details(add, sc, mk, m, rib, WH, rib_side_w, in_bld_any, EST, ESTP, B):
    """add(layer, nombre, VF) — despiece, canaletas, LED, Carlos III v2, Correos, Estacion, kioscos."""
    # ---- §8 CINTA: fascia + goteron + canaletas + juntas de tablas + sumideros + LED + luminarias
    for side in (rib_side_w(0.02), [(2 * rib[i][0] - q[0], 2 * rib[i][1] - q[1])
                                    for i, q in enumerate(rib_side_w(0.02))]):
        add('02_PRIMARY_STRUCTURE', 'DECK_FASCIA', mk.strip(side, 0.055, 5.72, 6.03))
        add('19_DETALLE', 'DECK_GOTERON', mk.strip(side, 0.03, 5.70, 5.73))
    for side in (rib_side_w(-0.20), [(2 * rib[i][0] - q[0], 2 * rib[i][1] - q[1])
                                     for i, q in enumerate(rib_side_w(-0.20))]):
        add('19_DETALLE', 'DECK_CANALETA', mk.strip(side, 0.10, 5.99, 6.005))
    acc = 0.0
    JV, JF = [], []
    LUM = 0.0
    for i in range(1, len(rib)):
        seg = math.hypot(rib[i][0] - rib[i - 1][0], rib[i][1] - rib[i - 1][1])
        acc += seg
        LUM += seg
        if acc >= 0.62:                                    # junta de tablas
            acc = 0.0
            tx = rib[i][0] - rib[i - 1][0]; ty = rib[i][1] - rib[i - 1][1]
            L = math.hypot(tx, ty) or 1e-9
            nx0, ny0 = -ty / L, tx / L
            w = WH[i] - 0.12
            o = len(JV)
            for (du, dz) in ((-0.011, 6.0005), (0.011, 6.0005)):
                JV += [(rib[i][0] + nx0 * w + tx / L * du, rib[i][1] + ny0 * w + ty / L * du, dz),
                       (rib[i][0] - nx0 * w + tx / L * du, rib[i][1] - ny0 * w + ty / L * du, dz)]
            JF += [(o, o + 2, o + 3), (o, o + 3, o + 1)]
        if LUM >= 12.0:                                    # luminaria de soffit + manguito de pasamanos
            LUM = 0.0
            add('19_DETALLE', 'DECK_LUMINARIA', mk.cylinder((rib[i][0], rib[i][1], 5.74),
                                                            (rib[i][0], rib[i][1], 5.78), 0.09, 8))
            q = rib_side_w(-0.05)[i]
            add('19_DETALLE', 'RAIL_MANGUITO', mk.cylinder((q[0], q[1], 7.01), (q[0], q[1], 7.09), 0.055, 6))
    add('19_DETALLE', 'DECK_JUNTAS', (JV, JF))
    add('19_DETALLE', 'RAIL_LED', mk.strip(rib_side_w(-0.10), 0.02, 6.96, 6.98))
    acc = 0.0
    for i in range(1, len(rib)):                           # sumideros cada ~24 m
        acc += math.hypot(rib[i][0] - rib[i - 1][0], rib[i][1] - rib[i - 1][1])
        if acc >= 24.0:
            acc = 0.0
            q = rib_side_w(-0.30)[i]
            add('19_DETALLE', 'DECK_SUMIDERO', mk.box((q[0], q[1], 5.995), 0.34, 0.22, 0.012))

    # ---- §18 PAVIMENTO: despiece 5.4 + registros de suelo + alcorques
    def linea(p0, p1, nombre):
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        nseg = max(2, int(L / 1.35))
        run = []
        for k in range(nseg + 1):
            t = k / nseg
            x, y = p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t
            if in_bld_any(x, y, 0.15, 0.0):
                if len(run) > 1:
                    add('19_DETALLE', nombre, mk.strip(run, 0.045, 0.004, 0.014))
                run = []
            else:
                run.append((x, y))
        if len(run) > 1:
            add('19_DETALLE', nombre, mk.strip(run, 0.045, 0.004, 0.014))
    x = -97.2
    while x <= 97.2:
        linea((x, -32.4), (x, 70.2), 'PAV_JUNTA_V')
        x += 5.4
    y = -32.4
    while y <= 70.2:
        linea((-97.2, y), (97.2, y), 'PAV_JUNTA_H')
        y += 5.4
    for (rx0, ry0) in [(-60, 0), (-30, -6), (0, 10), (28, 6), (52, 12), (70, -4), (-14, 24), (40, 26)]:
        if not in_bld_any(rx0, ry0, 0.5, 0.0):
            add('19_DETALLE', 'PAV_REGISTRO', mk.box((rx0, ry0, 0.008), 0.6, 0.6, 0.016))
            add('19_DETALLE', 'PAV_REGISTRO_MARCO', mk.box((rx0, ry0, 0.004), 0.72, 0.72, 0.006))
    for (tx0, ty0) in m['paisaje']['new_trees']:
        add('19_DETALLE', 'ALCORQUE', mk.torus((tx0, ty0, 0.015), 0.62, 0.028, 14, 4))

    # ---- §19 CARLOS III v2: molduras + patas del caballo + cola + bicornio + verja perimetral
    ex, ey = EST['xy']
    add('00_CONTEXT', 'EST_MOLDURA_1', mk.box((ex, ey, 0.44), 5.0, 3.2, 0.18))
    add('00_CONTEXT', 'EST_MOLDURA_2', mk.box((ex, ey, 2.76), 4.7, 2.9, 0.14))
    for (dx, dy) in ((1.05, 0.3), (-0.95, 0.3), (-0.95, -0.3)):        # 3 patas apoyadas en peana (top 2.9)
        add('00_CONTEXT', 'EST_PATA', mk.cylinder((ex + dx, ey + dy, 2.9), (ex + dx * 1.02, ey + dy, 3.72), 0.10, 6))
    add('00_CONTEXT', 'EST_PATA',                                       # mano delantera ALZADA (caracoleo)
        mk.cylinder((ex + 1.5, ey - 0.3, 3.35), (ex + 1.05, ey - 0.3, 3.78), 0.10, 6))
    add('00_CONTEXT', 'EST_COLA', mk.cylinder((ex - 1.5, ey, 4.3), (ex - 1.88, ey, 3.35), 0.09, 5))
    add('00_CONTEXT', 'EST_BICORNIO', mk.cylinder((ex - 0.15, ey - 0.16, 6.14), (ex - 0.15, ey + 0.16, 6.14), 0.19, 6))
    # 03B.7-D (V-003/6): verja CENIDA a la grada (como el monumento real) — 5.2x4.0 estrangulaba
    # el eje-mayor-alcala a 1.12-1.58 m; 3.5x2.6 deja el paseo integro
    for k in range(10):
        a = 2 * math.pi * k / 10
        px, py = ex + 3.5 * math.cos(a), ey + 2.6 * math.sin(a)
        add('19_DETALLE', 'EST_VERJA_POSTE', mk.cylinder((px, py, 0), (px, py, 0.55), 0.025, 5))
    ring = [(ex + 3.5 * math.cos(2 * math.pi * k / 40), ey + 2.6 * math.sin(2 * math.pi * k / 40), 0.5)
            for k in range(41)]
    add('19_DETALLE', 'EST_VERJA_RIEL', mk.tube(ring, 0.018, 4))

    # ---- §20 CORREOS: ritmo de huecos + portada + balcon del reloj
    for fila, z0, hv in ((0, 3.4, 2.4), (1, 7.6, 2.2), (2, 11.4, 1.9)):
        for k in range(15):
            wx = -52 + k * 4.35
            add('00_CONTEXT', 'CORREOS_HUECO', mk.box((wx, -28.35, z0 + hv / 2), 1.5, 0.18, hv))
    add('00_CONTEXT', 'CORREOS_PORTADA', mk.box((-25.2, -28.3, 2.6), 3.6, 0.35, 5.2))
    add('00_CONTEXT', 'CORREOS_BALCON', mk.box((-25.2, -27.9, 5.4), 5.2, 0.7, 0.22))
    add('00_CONTEXT', 'CORREOS_CORNISA', mk.box((-22, -28.3, 14.2), 60, 0.4, 0.35))

    # ---- §20 ESTACION: costillas de la ballena + portal este
    xs = [p[0] for p in ESTP]; ys = [p[1] for p in ESTP]
    ex0, ex1 = min(xs) + 1.2, max(xs) - 1.2
    cyE = (min(ys) + max(ys)) / 2
    wE = (max(ys) - min(ys)) / 2
    xk = ex0
    while xk <= ex1:
        arco = []
        for t in range(13):
            a = math.pi * t / 12
            arco.append((xk, cyE - wE * math.cos(a), 5.6 * math.sin(a) * 0.92 + 0.2))
        add('00_CONTEXT', 'ESTACION_COSTILLA', mk.tube(arco, 0.09, 6))
        xk += 2.6
    esp = [(xk2, cyE - wE, 0.2) for xk2 in [ex0 + 2.6 * j for j in range(int((ex1 - ex0) / 2.6) + 1)]]
    add('00_CONTEXT', 'ESTACION_ESPINA', mk.tube([(p[0], cyE, 5.35) for p in esp], 0.09, 6))
    add('00_CONTEXT', 'ESTACION_PORTAL', mk.box((max(xs) - 0.3, cyE, 4.7), 0.5, 4.4, 2.2))   # dintel: galibo 4.7 (V-015)

    # ---- §20 KIOSCOS: cornisa + banda de rotulo
    for ki in m['urbano_v004']['kioscos']:
        poly = B[ki]['pts']
        cxk = sum(p[0] for p in poly) / len(poly)
        cyk = sum(p[1] for p in poly) / len(poly)
        ring = []
        for p in poly[::max(1, len(poly) // 20)]:
            d = math.hypot(p[0] - cxk, p[1] - cyk) or 1e-9
            s = (d + 0.22) / d
            ring.append((cxk + (p[0] - cxk) * s, cyk + (p[1] - cyk) * s, 3.35))
        add('00_CONTEXT', 'KIOSCO_CORNISA', mk.tube(ring + [ring[0]], 0.07, 5))
        add('00_CONTEXT', 'KIOSCO_ROTULO', mk.tube([(p[0], p[1], 3.07) for p in ring + [ring[0]]], 0.05, 4))   # galibo cara inferior >= 3.0
