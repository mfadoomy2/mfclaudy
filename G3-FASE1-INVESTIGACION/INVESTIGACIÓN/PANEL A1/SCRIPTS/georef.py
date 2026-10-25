import numpy as np, re, json
from pyproj import Transformer
T=Transformer.from_crs(4326,25830,always_xy=True)
res={}
import glob,subprocess
for f in sorted(glob.glob('/mnt/user-data/uploads/G3 Proyectos/MAPPEADOS/*.pdf')):
    s=open(f,'rb').read()
    m=re.search(rb'/GPTS \[([^\]]+)\]',s); g=list(map(float,m.group(1).split()))
    m2=re.search(rb'/Viewport[^>]*|/BBox \[([^\]]+)\] /Measure',s)
    bb=re.search(rb'/BBox \[([^\]]+)\] /Measure',s).group(1).split()
    L=[(0,1),(0,0),(1,0),(1,1)]
    P=[T.transform(g[2*i+1],g[2*i]) for i in range(4)]
    A=np.array([[x,y,1] for x,y in P]); U=np.array(L)
    M,resid,_,_=np.linalg.lstsq(A,U,rcond=None)
    err=np.abs(A@M-U).max()
    res[f.split('/')[-1]]=dict(M=M.tolist(),bbox=list(map(float,bb)),err=float(err),P=P)
    print(f.split('/')[-1],bb,round(err,6),[ (round(x),round(y)) for x,y in P])
json.dump(res,open('georef.json','w'))
