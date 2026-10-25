import sys,json,glob,numpy as np; sys.path.insert(0,'.')
from base import *; import alzado
from PIL import Image, ImageDraw
H=META["historico_31"]; a=(439997.0,4473252.0); b=(439995.8,4473206.0)
ref=np.asarray(Image.open("vistas/hist/2021-7.jpg").convert("L").resize((230,75))).astype(float)
def load(h):
    f=glob.glob(f"/mnt/user-data/uploads/G3 Proyectos/INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/RECORRIDO_STREETVIEW_2026-09-23/HISTORICO_31/*{h['pano']}.jpg")
    eq=np.asarray(Image.open(f[0]).convert("RGB")); alzado._c.clear(); alzado._c["H"]=eq
out={}
for h in H:
    if h["date"] in ("2021-7","2019-8","2018-8"): out[h["date"]]=0; continue
    load(h); c=T.transform(h["lon"],h["lat"]); best=None
    for off in range(-180,180,3):
        im=alzado.alzado("H",c,h["hd"]+off,90,0,a,b,-1,14,res=0.2)
        g=np.asarray(im.convert("L").resize((230,75))).astype(float)
        cc=np.corrcoef(g.ravel(),ref.ravel())[0,1]
        if best is None or cc>best[0]: best=(cc,off)
    # refine
    for off in np.arange(best[1]-3,best[1]+3.1,0.5):
        im=alzado.alzado("H",c,h["hd"]+off,90,0,a,b,-1,14,res=0.2)
        g=np.asarray(im.convert("L").resize((230,75))).astype(float); cc=np.corrcoef(g.ravel(),ref.ravel())[0,1]
        if cc>best[0]: best=(cc,float(off))
    out[h["date"]]=best[1]; print(h["date"],best,flush=True)
    im=alzado.alzado("H",c,h["hd"]+best[1],90,0,a,b,-1,14,res=0.04); im.save(f"vistas/hist/{h['date']}.jpg",quality=88)
json.dump(out,open("datos/hist_offsets.json","w"))
