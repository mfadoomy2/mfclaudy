import sys, json, math, numpy as np
sys.path.insert(0,'.')
from base import *; from alzado import sample
from PIL import Image
RES=0.03; CAMH=2.5
F=json.load(open("datos/frentes_ribera.json"))
cams=[(e["id"],cam(e),e["heading_pano"]) for e in META["estaciones"]]
CX=np.array([c[1][0] for c in cams]); CY=np.array([c[1][1] for c in cams])
# rebuild facade segments per building
import frentes_segs
def run(f,idx):
    segs=frentes_segs.get(f["rc"],f["side"])
    pts=[]
    for sg in segs: pts+= [(sg["x1"],sg["y1"]),(sg["x2"],sg["y2"])]
    pts=np.array(pts); s=np.array([CL.project(Point(p)) for p in pts])
    a=pts[s.argmin()]; b=pts[s.argmax()]
    if f["side"]=='W': a,b=b,a       # seen from street: W facade left=south
    L=math.hypot(*(b-a))
    if L<3: return None
    H=(f["plantas_max"] or 6)*3.2+4.0
    nx=int(L/RES); nz=int((H+0.6)/RES)
    t=(np.arange(nx)+0.5)/nx; z=H-(np.arange(nz)+0.5)*RES
    FX=a[0]+(b[0]-a[0])*t; FY=a[1]+(b[1]-a[1])*t
    # facade segments may be offset; use nearest facade point distance: project columns onto actual segments
    dist=np.hypot(FX[:,None]-CX[None,:],FY[:,None]-CY[None,:]); st=dist.argmin(1)
    out=np.zeros((nz,nx,3),np.uint8)
    for k in np.unique(st):
        cid,(cx,cy),hd=cams[k]; m=np.where(st==k)[0]
        dE=(FX[m]-cx)[None,:].repeat(nz,0); dN=(FY[m]-cy)[None,:].repeat(nz,0); dU=(z[:,None]-CAMH).repeat(len(m),1)
        n=np.sqrt(dE**2+dN**2+dU**2)
        out[:,m]=sample(cid,hd,90,0,dE/n,dN/n,dU/n)
    fn=f"vistas/fachadas/{f['side']}{idx:02d}_{f['rc']}.jpg"
    Image.fromarray(out).save(fn,quality=88)
    return dict(file=fn,L=round(L,1),H=round(H,1),estaciones=sorted({cams[k][0] for k in np.unique(st)}),a=a.tolist(),b=b.tolist())
if __name__=="__main__":
    import os; os.makedirs("vistas/fachadas",exist_ok=True)
    res=[]
    for side in "EW":
        L=[f for f in F if f["side"]==side]; L.sort(key=lambda f:f["s0"])
        for i,f in enumerate(L,1):
            r=run(f,i); 
            if r: res.append({**f,**r,"codigo":f"{side}{i:02d}"})
    json.dump(res,open("datos/fachadas_index.json","w"),indent=0)
    print(len(res))
