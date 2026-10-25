import numpy as np, math, glob
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
P="/mnt/user-data/uploads/G3 Proyectos/INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/RECORRIDO_STREETVIEW_2026-09-23/PANORAMAS/"
_c={}
def pano(eid):
    if eid not in _c:
        _c.clear(); f=glob.glob(P+f"G3SV_{eid}_*.jpg")[0]; _c[eid]=np.asarray(Image.open(f).convert("RGB"))
    return _c[eid]
def sample(eid, hd, tilt, roll, dE, dN, dU, sgn=1):
    """dE,dN,dU arrays of world direction; returns rgb"""
    eq=pano(eid); H,W,_=eq.shape
    h=math.radians(hd)
    # rotate world -> pano yaw frame (fwd = heading)
    fwd = dE*math.sin(h)+dN*math.cos(h)
    rgt = dE*math.cos(h)-dN*math.sin(h)
    up = dU
    # pitch correction (tilt 90 = level). positive tp tilts forward axis down
    tp=math.radians((tilt-90)*sgn)
    f2= fwd*math.cos(tp)-up*math.sin(tp); u2= fwd*math.sin(tp)+up*math.cos(tp)
    rr=math.radians(roll if roll<180 else roll-360)*sgn
    r2= rgt*math.cos(rr)+u2*math.sin(rr); u3=-rgt*math.sin(rr)+u2*math.cos(rr)
    az=np.degrees(np.arctan2(r2,f2)); el=np.degrees(np.arctan2(u3,np.hypot(r2,f2)))
    u=((az/360.0+0.5)%1.0)*W; v=(0.5-el/180.0)*H
    return eq[np.clip(v.astype(int),0,H-1),np.clip(u.astype(int),0,W-1)]
def alzado(eid, cam, hd, tilt, roll, a, b, zmin, zmax, res=0.02, camh=2.5, sgn=1):
    """a,b: (x,y) facade endpoints in EPSG:25830 (left->right as seen from street). z relative to street under camera"""
    L=math.hypot(b[0]-a[0],b[1]-a[1]); nx=int(L/res); nz=int((zmax-zmin)/res)
    t=(np.arange(nx)+0.5)/nx; z=zmax-(np.arange(nz)+0.5)*res
    X=a[0]+(b[0]-a[0])*t; Y=a[1]+(b[1]-a[1])*t
    XX,ZZ=np.meshgrid(X,z); YY,_=np.meshgrid(Y,z)
    dE=XX-cam[0]; dN=YY-cam[1]; dU=ZZ-camh
    n=np.sqrt(dE**2+dN**2+dU**2)
    return Image.fromarray(sample(eid,hd,tilt,roll,dE/n,dN/n,dU/n,sgn))
