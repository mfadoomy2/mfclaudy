"""Láminas axonométricas de las 7 capas de MAPPEADOS (georreferenciadas por GPTS del GeoPDF)."""
import numpy as np, math, json
from PIL import Image, ImageFilter

PXM = 9001.667 / 3118.0          # px/m a 220 ppp
X0, Y0 = 438659.0, 4473847.0     # esquina sup-izq del GeoPDF (EPSG:25830)
OFFX = 2046                       # recorte horizontal aplicado en pdftoppm
C = (440017.838, 4473229.396)     # centroide de la parcela 31

def px(x, y):
    return ((x - X0) * PXM - OFFX, (Y0 - y) * PXM)

ANG = math.radians(-32); SQ = 0.46; RM = 560.0; OUT = 2200

COLS = ["#131313", "#FF8A00", "#2238FF", "#FF4FA3", "#7B2CFF", "#00A86B", "#00B3D6"]

def hex2rgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

def iso_params():
    sc = OUT / (2 * RM)
    W = OUT; H = int(OUT * SQ) + 4
    return sc, W, H

def to_iso(e, n):
    """metros (e,n) desde C -> px en lámina iso (x derecha, y abajo)."""
    sc, W, H = iso_params()
    sx = e * math.cos(ANG) - n * math.sin(ANG)
    sy = e * math.sin(ANG) + n * math.cos(ANG)
    return W / 2 + sx * sc, H / 2 - sy * sc * SQ

def build(k):
    a = np.asarray(Image.open(f"hi/diff_{k}.png")).copy()
    h, w = a.shape[:2]
    cx, cy = px(*C)
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot(xx - cx, yy - cy) / PXM
    alpha = a[..., 3].astype(float)
    if k == 0:  # edificios: gris claro -> usar oscuridad
        lum = a[..., :3].mean(2); alpha = np.clip((255 - lum) * 6, 0, 255) * (a[..., 3] > 0)
    alpha[r > RM] = 0
    rgb = np.array(hex2rgb(COLS[k]), np.uint8)
    out = np.zeros((h, w, 4), np.uint8); out[..., :3] = rgb; out[..., 3] = alpha.astype(np.uint8)
    im = Image.fromarray(out)
    if k in (1, 2, 6):
        # líneas finas: engrosar ligeramente para que lean a escala A1
        al = im.split()[3].filter(ImageFilter.MaxFilter(3)); im.putalpha(al)
    im = im.resize((w // 2, h // 2), Image.LANCZOS); f = 0.5
    sc, W, H = iso_params()
    # afín inversa: salida (X,Y) -> entrada (u,v)
    ca, sa = math.cos(ANG), math.sin(ANG)
    # sx=(X-W/2)/sc ; sy=-(Y-H/2)/(sc*SQ)
    # e = sx*ca + sy*sa ; n = -sx*sa + sy*ca ; u = cx + e*PXM ; v = cy - n*PXM
    ax_, bx_ = 1 / sc, 0; ay_, by_ = 0, -1 / (sc * SQ)
    c_sx = -W / 2 / sc; c_sy = H / 2 / (sc * SQ)
    # e = (ax_*X + c_sx)*ca + (by_*Y + c_sy)*sa
    eX, eY, e0 = ax_ * ca, by_ * sa, c_sx * ca + c_sy * sa
    nX, nY, n0 = -ax_ * sa, by_ * ca, -c_sx * sa + c_sy * ca
    coeffs = tuple(v * f for v in (eX * PXM, eY * PXM, cx + e0 * PXM, -nX * PXM, -nY * PXM, cy - n0 * PXM))
    iso = im.transform((W, H), Image.AFFINE, coeffs, resample=Image.BILINEAR)
    iso.save(f"hi/iso_{k}.png")
    return iso.size

if __name__ == "__main__":
    for k in range(7):
        print(k, build(k))
