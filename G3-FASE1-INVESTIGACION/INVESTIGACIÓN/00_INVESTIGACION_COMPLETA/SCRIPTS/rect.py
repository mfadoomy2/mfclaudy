import numpy as np, json, glob, os
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
P="/mnt/user-data/uploads/G3 Proyectos/INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/RECORRIDO_STREETVIEW_2026-09-23"
META=json.load(open(P+"/G3SV_metadatos.json"))
_cache={}
def pano_img(path):
    if path not in _cache:
        _cache.clear(); _cache[path]=np.asarray(Image.open(path).convert("RGB"))
    return _cache[path]
def persp(path, pano_hd, heading, pitch=0, fov=90, W=1600, H=1000, offset=0.0):
    """heading: true-north azimuth of view centre. equirect centre column = pano_hd + offset"""
    eq=pano_img(path); h,w,_=eq.shape
    f=(W/2)/np.tan(np.radians(fov)/2)
    xs=np.arange(W)-W/2+0.5; ys=np.arange(H)-H/2+0.5
    X,Y=np.meshgrid(xs,ys)
    # camera coords: x right, y down, z forward
    d=np.stack([X,Y,np.full_like(X,f)],-1); d/=np.linalg.norm(d,axis=-1,keepdims=True)
    p=np.radians(pitch)
    # rotate by pitch around x (positive pitch = look up)
    y2=d[...,1]*np.cos(p)-d[...,2]*np.sin(p); z2=d[...,1]*np.sin(p)+d[...,2]*np.cos(p); x2=d[...,0]
    lon=np.degrees(np.arctan2(x2,z2))+heading   # azimuth
    lat=-np.degrees(np.arcsin(np.clip(y2,-1,1)))
    u=((lon-(pano_hd+offset))/360.0+0.5)%1.0*w
    v=(0.5-lat/180.0)*h
    ui=np.clip(u.astype(int),0,w-1); vi=np.clip(v.astype(int),0,h-1)
    return Image.fromarray(eq[vi,ui])
def est(i):
    e=META["estaciones"][i-1]; f=glob.glob(P+f"/PANORAMAS/G3SV_E{i:02d}_*.jpg")[0]; return e,f
