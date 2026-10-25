import sys, json, math, numpy as np
sys.path.insert(0,'.')
from base import *; from alzado import sample, pano
from shapely.geometry import LineString, Point
from shapely.strtree import STRtree
from PIL import Image
RES=0.05; ZMAX=36.0; ZMIN=-0.5; CAMH=2.5
geoms=[g for g,p in BLD]; tree=STRtree(geoms)
def tangent(s):
    a=CL.interpolate(max(0,s-4)); b=CL.interpolate(min(CL.length,s+4)); dx,dy=b.x-a.x,b.y-a.y; n=math.hypot(dx,dy); return dx/n,dy/n
def facade_dist(s, side):
    p=CL.interpolate(s); tx,ty=tangent(s)
    nx,ny=(-ty,tx) if side=='E' else (ty,-tx)   # E = right of travel direction (travel N->S, right = west?) fixed below
    ray=LineString([(p.x+nx*3,p.y+ny*3),(p.x+nx*30,p.y+ny*30)])
    best=None
    for i in tree.query(ray):
        g=geoms[i]; x=ray.intersection(g.boundary)
        if x.is_empty: continue
        pts=[x] if x.geom_type=='Point' else list(getattr(x,'geoms',[x]))
        for q in pts:
            q=Point(q.coords[0]); d=Point(p).distance(q)
            if best is None or d<best: best=d
    return best,(nx,ny)
if __name__=="__main__":
    side=sys.argv[1]; s_from=float(sys.argv[2]); s_to=float(sys.argv[3])
    # side convention check: parcel 31 must be on 'E'
    s31=CL.project(Point(PARCELA.centroid))
    d,_=facade_dist(s31,'E'); print("E dist at 31",d)
    ss=np.arange(s_from,s_to,1.0); D=[]
    for s in ss:
        d,_=facade_dist(s,side); D.append(d if d is not None and d<22 else np.nan)
    D=np.array(D); gap=np.isnan(D)
    # fill gaps by interpolation / default
    med=np.nanmedian(D); Df=D.copy(); 
    idx=np.arange(len(D)); good=~gap
    Df[gap]=np.interp(idx[gap],idx[good],D[good]) if good.any() else med
    ncol=int((s_to-s_from)/RES); cols_s=s_from+(np.arange(ncol)+0.5)*RES
    dcol=np.interp(cols_s,ss,Df)
    # facade points
    FX=np.empty(ncol); FY=np.empty(ncol)
    for i,s in enumerate(cols_s):
        p=CL.interpolate(s); tx,ty=tangent(s); nx,ny=(-ty,tx) if side=='E' else (ty,-tx)
        FX[i]=p.x+nx*dcol[i]; FY[i]=p.y+ny*dcol[i]
    cams=[(e["id"],cam(e),e["heading_pano"]) for e in META["estaciones"]]
    # assign station: nearest camera
    CX=np.array([c[1][0] for c in cams]); CY=np.array([c[1][1] for c in cams])
    dist=np.hypot(FX[:,None]-CX[None,:],FY[:,None]-CY[None,:]); st=dist.argmin(1)
    nz=int((ZMAX-ZMIN)/RES); z=ZMAX-(np.arange(nz)+0.5)*RES
    out=np.zeros((nz,ncol,3),np.uint8)
    for k in np.unique(st):
        cid,(cx,cy),hd=cams[k]; m=np.where(st==k)[0]
        dE=(FX[m]-cx)[None,:].repeat(nz,0); dN=(FY[m]-cy)[None,:].repeat(nz,0); dU=(z[:,None]-CAMH).repeat(len(m),1)
        n=np.sqrt(dE**2+dN**2+dU**2)
        out[:,m]=sample(cid,hd,90,0,dE/n,dN/n,dU/n)
    Image.fromarray(out).save(f"vistas/continuo_{side}_{int(s_from)}_{int(s_to)}.jpg",quality=90)
    json.dump({"side":side,"s_from":s_from,"s_to":s_to,"res":RES,"zmax":ZMAX,"zmin":ZMIN,"station_per_col":[cams[i][0] for i in st[::20]],"gap_1m":gap.tolist(),"dist_1m":[None if np.isnan(x) else round(float(x),2) for x in D]},open(f"vistas/continuo_{side}_{int(s_from)}_{int(s_to)}.json","w"))
    print("ok",out.shape)
