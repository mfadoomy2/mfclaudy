# -*- coding: utf-8 -*-
"""
FASE 03B.5B — nucleo fisico.
Escena (identica a 03B.5) · vóxel de transmitancia · posicion solar · marcha de rayos ·
psicrometria · balances de energia.

Todo parametro fisico se declara en PARAMS con su procedencia y su etiqueta de certeza:
MEDIDO (geometria del modelo) · CALCULADO · SIMULADO · ESTIMADO · HIPOTESIS
"""
import json
import math
import os
import sys
import datetime as dt

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
AUD = os.path.join(ROOT, 'FASE_03B5_AUDITORIA')
DATA = os.path.join(HERE, '_data')
CL = os.path.join(HERE, '_clima')
sys.path.insert(0, AUD)
import audit_core as AC  # noqa: E402

LAT, LON, ELEV = 40.4169, -3.7035, 665.0
TZ = 2                      # CEST = UTC+2 en la ventana critica

# ============================================================ PARAMETROS FISICOS
PARAMS = {
    # --- optica
    'tau_canopy': (0.12, 'HIPOTESIS', 'Transmitancia solar de la hoja-canopy: membrana tensada opaca + lamina de '
                                      'microalgas 2-5 cm (D15). Una lamina de agua con algas transmite poco; se toma '
                                      '0.12 con rango 0.05-0.25 en el analisis de sensibilidad.'),
    'tau_net': (0.75, 'ESTIMADO', 'Redes tensadas (cables + velo) de C1/C2/C3: sombra parcial ligera.'),
    'tau_dome': (0.55, 'HIPOTESIS', 'Cupula-pergola: ETFE con reticula de membrana visible (E02 op.0.30). ETFE claro '
                                    'transmite 0.90; con fritado/reticula y suciedad se toma 0.55 (rango 0.35-0.80).'),
    'k_veg': (0.40, 'ESTIMADO', 'Coeficiente de extincion volumetrico del follaje [1/m]. Beer-Lambert: una copa de '
                                '4 m de espesor da tau=exp(-0.40*4)=0.20, coherente con LAI 2.5-3.5 y k_ext 0.5-0.6 '
                                'de arbolado urbano caducifolio.'),
    'alb_granito': (0.30, 'ESTIMADO', 'Albedo del granito de Sol (gris claro, seco). Rango 0.25-0.35.'),
    'alb_granito_hum': (0.18, 'ESTIMADO', 'Albedo del mismo granito humedo (la pelicula de agua oscurece; E01 midio '
                                          '-34 % de color en humedo).'),
    'alb_agua': (0.07, 'CALCULADO', 'Albedo de lamina de agua para angulos solares altos (Fresnel).'),
    'alb_veg': (0.20, 'ESTIMADO', 'Albedo de masa foliar.'),
    'alb_canopy': (0.25, 'ESTIMADO', 'Albedo de la cara inferior de la hoja-canopy (membrana clara).'),
    'eps_sup': (0.95, 'ESTIMADO', 'Emisividad infrarroja de granito, vegetacion y membrana (0.92-0.97).'),
    'eps_agua': (0.96, 'ESTIMADO', 'Emisividad del agua.'),
    # --- persona
    'a_k': (0.70, 'ESTIMADO', 'Coeficiente de absorcion de onda corta del cuerpo vestido (VDI 3787 / Hoppe).'),
    'eps_p': (0.97, 'ESTIMADO', 'Emisividad del cuerpo humano.'),
    'h_mrt': (1.10, 'HIPOTESIS', 'Altura de calculo de MRT [m] (centro de masas del peaton; el enunciado pide 1,10-1,50).'),
    # --- suelo / conveccion
    'G_frac': (0.25, 'ESTIMADO', 'Fraccion del balance neto que se conduce al terreno en pavimento macizo diurno '
                                 '(0.2-0.3 en literatura de pavimentos urbanos).'),
    'z0_plaza': (0.30, 'HIPOTESIS', 'Longitud de rugosidad de la plaza abierta [m] para llevar el viento de 10 m a '
                                    'nivel peatonal. Rango urbano abierto 0.1-0.5.'),
    'z_ped': (1.10, 'CALCULADO', 'Altura de referencia peatonal [m].'),
    # --- nebulizacion (HIPOTESIS declaradas: el modelo 03B no especifica caudales)
    'neb_caudal_L_h': (5.0, 'HIPOTESIS', 'Caudal por boquilla [L/h]. Boquilla de alta presion (70-100 bar) de niebla '
                                         'seca: 3-8 L/h. El modelo 03B define la POSICION de 42 puntos pero no el '
                                         'caudal; se toma 5.0 nominal y se analiza 3.0 / 5.0 / 8.0.'),
    'neb_eficiencia': (0.35, 'HIPOTESIS', 'Eficiencia de saturacion alcanzada en aire libre, es decir fraccion de la '
                                          'depresion de bulbo humedo realmente conseguida. En interiores un panel '
                                          'evaporativo llega a 0.85; a la intemperie con viento la literatura de '
                                          'nebulizacion urbana da 0.15-0.50. Se analiza 0.20 / 0.35 / 0.50.'),
    'neb_radio': (3.0, 'HIPOTESIS', 'Radio nominal de la nube de una boquilla a 4.0 m [m], antes de deriva.'),
    'neb_altura': (4.0, 'MEDIDO', 'Altura de emision: H_MISTING del HEIGHT_SYSTEM, verificada en el modelo.'),
}


def P(k):
    return PARAMS[k][0]


# ============================================================ ESCENA + VOXEL
LAYER_CLASS = {
    # 1 opaco · 2 canopy(membrana+lamina de microalgas) · 3 cupula ETFE · 4 vegetacion · 5 red tensada
    '00_CONTEXT': 1, '02_PRIMARY_STRUCTURE': 1, '03_SECONDARY_STRUCTURE': 1, '04_MASTS': 1,
    '08_PINK_MODULES': 1, '09_PLANTERS': 1, '10_FURNITURE': 1, '11_WATER': 1, '13_PIPES': 1,
    '07_CANOPIES': 2, '06_MEMBRANES': 3, '15_VEGETATION_FULL': 4, '14_VEGETATION_PROXY': 4,
}


def class_of(o):
    """Clase optica del objeto. La hoja-canopy es un CONJUNTO (aro + nervios + membrana +
    lamina de microalgas + embudo): sus partes viven en capas distintas pero opticamente
    forman una sola pieza, y se clasifican juntas para que tau_canopy sea un parametro
    real y auditable en vez de quedar enmascarado por la lamina de agua."""
    if o['block'].startswith('LEAF_'):
        return 2
    if o['name'].startswith('NET_'):
        return 5
    if o['name'] in ('DOME_SHELL',):
        return 3
    return LAYER_CLASS.get(o['layer'])
SKIP = {'01_GROUND', '12_MIST', '16_PEOPLE_PROXY', '17_METRO_CLEARANCES', '30_CURVES', '05_CABLES'}

VS = 0.5          # lado del voxel [m]
ZTOP = 36.0
NZ = int(ZTOP / VS)


def load_scene():
    objs, M, B = AC.load_scene()
    mesh = [o for o in objs if o['kind'] == 'mesh']
    for o in mesh:
        o['fam'] = AC.obj_family(o)
        o['bb'] = (o['V'].min(0), o['V'].max(0))
    return mesh, M


def grid05():
    return AC.Grid(-112, -45, 100, 78, VS)


def build_voxels(mesh, g, estado):
    """estado 'A' = contexto existente (edificios + arbolado OSM) · 'B' = A + proyecto.
    Devuelve uint8 [NZ, ny, nx] con la clase de material."""
    vox = np.zeros((NZ, g.ny, g.nx), np.uint8)
    for o in mesh:
        if o['layer'] in SKIP:
            continue
        cls = class_of(o)
        if cls is None:
            continue
        es_contexto = (o['layer'] == '00_CONTEXT') or (o['name'] == 'VEG2_ARBOL_EX')
        if estado == 'A' and not es_contexto:
            continue
        T = AC.tris_of(o)
        if len(T) == 0:
            continue
        z0 = max(T[:, :, 2].min(), 0.0)
        z1 = min(T[:, :, 2].max(), ZTOP)
        k0, k1 = int(z0 / VS), min(int(z1 / VS) + 1, NZ)
        for k in range(k0, k1):
            m = AC.rasterize(g, T, k * VS, (k + 1) * VS, 'mask')
            if m.any():
                sl = vox[k]
                np.copyto(sl, cls, where=m & (sl == 0))
                if cls == 1:
                    sl[m] = 1              # el opaco tiene prioridad
    return vox


# ============================================================ POSICION SOLAR
def sun_position(when_utc, lat=LAT, lon=LON):
    """Algoritmo PSA (Blanco-Muriel et al. 2001). Devuelve (elevacion, azimut) en grados.
    Azimut medido desde el Norte hacia el Este."""
    d = when_utc
    jd = (367 * d.year - int(7 * (d.year + int((d.month + 9) / 12)) / 4)
          + int(275 * d.month / 9) + d.day - 730531.5
          + (d.hour + d.minute / 60.0 + d.second / 3600.0) / 24.0)
    n = jd
    omega = 2.1429 - 0.0010394594 * n
    L = 4.8950630 + 0.017202791698 * n
    g = 6.2400600 + 0.0172019699 * n
    l = (L + 0.03341607 * math.sin(g) + 0.00034894 * math.sin(2 * g)
         - 0.0001134 - 0.0000203 * math.sin(omega))
    ep = 0.4090928 - 6.2140e-9 * n + 0.0000396 * math.cos(omega)
    ra = math.atan2(math.cos(ep) * math.sin(l), math.cos(l))
    if ra < 0:
        ra += 2 * math.pi
    dec = math.asin(math.sin(ep) * math.sin(l))
    gmst = 6.6974243242 + 0.0657098283 * n + (d.hour + d.minute / 60.0 + d.second / 3600.0)
    lmst = (gmst * 15 + lon) * math.pi / 180
    hra = lmst - ra
    latr = math.radians(lat)
    ez = math.acos(math.cos(latr) * math.cos(hra) * math.cos(dec) + math.sin(dec) * math.sin(latr))
    az = math.atan2(-math.sin(hra), math.tan(dec) * math.cos(latr) - math.sin(latr) * math.cos(hra))
    # correccion de paralaje
    EMR = 6371.01
    AU = 149597890.0
    ez = ez + (EMR / AU) * math.sin(ez)
    elev = 90.0 - math.degrees(ez)
    azd = math.degrees(az) % 360.0
    return elev, azd


def sun_vector(elev, azim):
    """vector unitario hacia el sol en el sistema del modelo (+X este, +Y norte, +Z arriba)."""
    e = math.radians(elev)
    a = math.radians(azim)
    return np.array([math.cos(e) * math.sin(a), math.cos(e) * math.cos(a), math.sin(e)])


# ============================================================ MARCHA DE RAYOS
def transmittance(vox, g, X, Y, Z, dvec, max_dist=320.0, ds=0.5, want_first=False):
    """Transmitancia solar de cada punto (X,Y,Z) en la direccion dvec.
    Devuelve (tau, directo_libre) — tau incluye canopy/cupula/vegetacion; opaco -> 0.
    Con want_first=True devuelve ademas la CLASE DEL PRIMER ELEMENTO ENCONTRADO: es la
    superficie cuya emision infrarroja ve realmente el punto (0 = cielo). Necesario para
    el termino de onda larga: un rayo que ATRAVIESA un dosel transmite sol pero NO ve el
    cielo frio, y contarlo como cielo falsea la MRT."""
    n = len(X)
    tau = np.ones(n)
    alive = np.ones(n, bool)
    hit_can = np.zeros(n, bool)
    hit_dom = np.zeros(n, bool)
    hit_net = np.zeros(n, bool)
    nveg = np.zeros(n, np.int32)
    first = np.zeros(n, np.uint8)          # clase del PRIMER elemento encontrado (0 = cielo)
    idx = np.arange(n)
    dx, dy, dz = float(dvec[0]), float(dvec[1]), float(dvec[2])
    if dz <= 0.02:
        z3 = np.zeros(n)
        return (z3, np.zeros(n, bool), np.ones(n, np.uint8)) if want_first else (z3, np.zeros(n, bool))
    nsteps = int(max_dist / ds)
    cx, cy, cz = X.copy(), Y.copy(), np.full(n, Z, float) if np.isscalar(Z) else Z.copy()
    for s in range(nsteps):
        cx += dx * ds; cy += dy * ds; cz += dz * ds
        ok = (cz < ZTOP) & (cx > g.x0) & (cx < g.x1) & (cy > g.y0) & (cy < g.y1)
        if not ok.any():
            break
        if not ok.all():                       # los que salen del dominio ya no se tocan
            keep = ok
            idx = idx[keep]; cx = cx[keep]; cy = cy[keep]; cz = cz[keep]
            if len(idx) == 0:
                break
        j = ((cx - g.x0) / VS).astype(np.int32)
        i = ((cy - g.y0) / VS).astype(np.int32)
        k = (cz / VS).astype(np.int32)
        c = vox[k, i, j]
        if c.any():
            nf = (first[idx] == 0) & (c > 0)
            if nf.any():
                first[idx[nf]] = c[nf]
            op = c == 1
            if op.any():
                alive[idx[op]] = False
            hit_can[idx[c == 2]] = True
            hit_dom[idx[c == 3]] = True
            hit_net[idx[c == 5]] = True
            v = c == 4
            if v.any():
                np.add.at(nveg, idx[v], 1)
            live = ~op
            if not live.all():
                idx = idx[live]; cx = cx[live]; cy = cy[live]; cz = cz[live]
                if len(idx) == 0:
                    break
    tau = np.where(alive, 1.0, 0.0)
    tau = tau * np.where(hit_can, P('tau_canopy'), 1.0)
    tau = tau * np.where(hit_dom, P('tau_dome'), 1.0)
    tau = tau * np.where(hit_net, P('tau_net'), 1.0)
    tau = tau * np.exp(-P('k_veg') * nveg * VS)
    if want_first:
        return tau, alive, first
    return tau, alive


# --- direcciones de cielo (Tregenza reducido) para SVF y difusa
def sky_dirs(n_alt=8):
    """devuelve (dirs, pesos) con pesos = cos(theta)*dOmega / pi  (suma 1 en cielo despejado)."""
    dirs, w = [], []
    for ia in range(n_alt):
        alt0 = 90.0 * ia / n_alt
        alt1 = 90.0 * (ia + 1) / n_alt
        alt = 0.5 * (alt0 + alt1)
        naz = max(1, int(round(12 * math.cos(math.radians(alt)))))
        # peso de la banda: integral de cos*sin dtheta dphi
        t0, t1 = math.radians(90 - alt1), math.radians(90 - alt0)
        band = math.pi * (math.sin(t1) ** 2 - math.sin(t0) ** 2)   # * (1/pi) ya normalizado abajo
        for iz in range(naz):
            az = 360.0 * (iz + 0.5) / naz
            dirs.append(sun_vector(alt, az))
            w.append(band / naz / math.pi)
    w = np.array(w)
    return np.array(dirs), w / w.sum()


# ============================================================ PSICROMETRIA
def psat(T):
    T = np.asarray(T, float)
    return 611.21 * np.exp((18.678 - T / 234.5) * (T / (257.14 + T)))


def pvap(T, RH):
    return np.asarray(RH, float) / 100.0 * psat(T)


def dewpoint(T, RH):
    e = np.maximum(pvap(T, RH), 1e-3)
    g = np.log(e / 611.21)
    return 243.12 * g / (17.62 - g)


def wetbulb(T, RH, Pa=94000.0):
    T = np.asarray(T, float); e = pvap(T, RH)
    lo = np.full_like(T, -20.0); hi = T.copy()
    for _ in range(50):
        w = 0.5 * (lo + hi)
        est = psat(w) - 6.53e-4 * Pa * (T - w)
        hi = np.where(est > e, w, hi)
        lo = np.where(est > e, lo, w)
    return 0.5 * (lo + hi)


def lambda_v(T):
    """calor latente de vaporizacion [J/kg]"""
    return (2500.8 - 2.36 * np.asarray(T, float)) * 1000.0


def wind_at(u10, z=None):
    """perfil logaritmico de 10 m a la altura z."""
    z = z or P('z_ped')
    z0 = P('z0_plaza')
    return u10 * math.log(z / z0) / math.log(10.0 / z0)


def h_conv(u):
    """coeficiente de conveccion superficie-aire [W/m2K] — McAdams para placa rugosa."""
    return 5.7 + 3.8 * np.asarray(u, float)


# ============================================================ BALANCE DE SUPERFICIE
SIGMA = 5.670374419e-8


def surface_temp(Sabs, Ldown, Ta, u, eps=None, LE=0.0, Gfrac=None):
    """Resuelve el balance de energia de una superficie:
       Sabs + eps*Ldown - eps*sigma*Ts^4 - hc*(Ts-Ta) - G - LE = 0
       Sabs [W/m2] onda corta absorbida · Ldown [W/m2] infrarrojo descendente
       Devuelve Ts [C]. CALCULADO."""
    eps = eps if eps is not None else P('eps_sup')
    Gf = Gfrac if Gfrac is not None else P('G_frac')
    hc = h_conv(u)
    Ta = np.asarray(Ta, float)
    Ts = Ta + 5.0
    for _ in range(60):
        Tk = Ts + 273.15
        Rn = Sabs + eps * Ldown - eps * SIGMA * Tk ** 4
        f = Rn - hc * (Ts - Ta) - Gf * np.maximum(Rn, 0) - LE
        df = -4 * eps * SIGMA * Tk ** 3 * (1 + Gf * np.where(Rn > 0, 1, 0)) - hc
        step = np.clip(f / np.where(np.abs(df) < 1e-9, -1e-9, df), -20, 20)
        Ts = Ts - step
        if np.nanmax(np.abs(step)) < 1e-4:
            break
    return Ts


def thin_element_temp(Sabs, Ldown_top, Ldown_bot, Ta, u, eps=None, LE=0.0):
    """Temperatura de un elemento delgado suspendido en aire (hoja-canopy):
    conveccion por las DOS caras, radiacion por las dos caras, sin conduccion al terreno.
    Sabs + eps*(Ld_top + Ld_bot) - 2*eps*sigma*Ts^4 - 2*hc*(Ts-Ta) - LE = 0.  CALCULADO."""
    eps = eps if eps is not None else P('eps_sup')
    hc = h_conv(u)
    Ta = np.asarray(Ta, float)
    Ts = Ta + 3.0
    for _ in range(80):
        Tk = Ts + 273.15
        f = (Sabs + eps * (Ldown_top + Ldown_bot) - 2 * eps * SIGMA * Tk ** 4
             - 2 * hc * (Ts - Ta) - LE)
        df = -8 * eps * SIGMA * Tk ** 3 - 2 * hc
        step = np.clip(f / df, -20, 20)
        Ts = Ts - step
        if np.nanmax(np.abs(step)) < 1e-4:
            break
    return Ts


def penman_open_water(Rn, Ta, RH, u, Pa=94000.0):
    """Evaporacion de lamina libre [kg/m2/s] — Penman (1948). CALCULADO.
    Rn [W/m2] radiacion neta sobre el agua."""
    Ta = np.asarray(Ta, float)
    es = psat(Ta); ea = pvap(Ta, RH)
    D = 4098.0 * es / (Ta + 237.3) ** 2          # pendiente de la curva de saturacion [Pa/K]
    lam = lambda_v(Ta)
    gam = 1005.0 * Pa / (0.622 * lam)            # constante psicrometrica [Pa/K]
    # funcion de viento de Penman en unidades SI de flujo de masa
    fu = 2.6e-8 * (1.0 + 0.54 * np.asarray(u, float))   # kg/(m2 s Pa)
    Ea = fu * (es - ea)
    E = (D * Rn / lam + gam * Ea) / (D + gam)
    return np.maximum(E, 0.0)


# ============================================================ MRT
def proj_area_factor(elev_deg):
    """factor de area proyectada de una persona de pie frente al haz directo (Fanger)."""
    h = np.asarray(elev_deg, float)
    return 0.308 * np.cos(np.radians(h * (0.998 - h ** 2 / 50000.0)))


def mrt(I_dir, tau_dir, elev, D_sky, R_grd, L_sky, L_grd, ak=None, epsp=None):
    """Temperatura radiante media [C]. Modelo de dos hemisferios (F_sky = F_grd = 0.5),
    coherente con VDI 3787 / Hoppe. CALCULADO."""
    ak = ak if ak is not None else P('a_k')
    epsp = epsp if epsp is not None else P('eps_p')
    fp = proj_area_factor(elev)
    Sabs = ak * (fp * I_dir * tau_dir + 0.5 * D_sky + 0.5 * R_grd)
    Labs = epsp * (0.5 * L_sky + 0.5 * L_grd)
    return ((Sabs + Labs) / (epsp * SIGMA)) ** 0.25 - 273.15


def jdump(name, obj):
    p = os.path.join(DATA, name)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1,
                  default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
    return p


def jload(name):
    return json.load(open(os.path.join(DATA, name), encoding='utf-8'))
