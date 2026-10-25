from geo import *
import numpy as np, heapq, json
from shapely import contains_xy, maximum_inscribed_circle
from shapely.ops import unary_union
def metrics(cl):
    fl=cl['field'].buffer(0.02); res=0.1; minx,miny,maxx,maxy=fl.bounds
    xs=np.arange(minx,maxx,res)+res/2; ys=np.arange(miny,maxy,res)+res/2
    X,Y=np.meshgrid(xs,ys); ok=contains_xy(fl,X,Y)
    f=cl['furn']; obs=unary_union([f['counter'],f['fridge'],f['table'],f['sofa'],f['low'],f['coats'],f['worktop']]+f['stools'])
    ok&=~contains_xy(obs.buffer(0.2),X,Y); H,Wd=ok.shape
    def cell(p):
        i=int((p[1]-miny)/res); j=int((p[0]-minx)/res); idx=np.argwhere(ok); k=np.argmin((idx[:,0]-i)**2+(idx[:,1]-j)**2); return tuple(idx[k])
    nb=[(a,b,(a*a+b*b)**.5) for a in (-1,0,1) for b in (-1,0,1) if a or b]
    def dij(p):
        d=np.full(ok.shape,np.inf); s=cell(p); d[s]=0; q=[(0,s)]
        while q:
            dd,(i,j)=heapq.heappop(q)
            if dd>d[i,j]: continue
            for a,b,c in nb:
                u,v=i+a,j+b
                if 0<=u<H and 0<=v<Wd and ok[u,v] and dd+c*res<d[u,v]: d[u,v]=dd+c*res; heapq.heappush(q,(d[u,v],(u,v)))
        return d
    doors={k:r['door'].interpolate(.5,normalized=True).coords[0] for k,r in cl['rooms'].items()}
    bd=[b['door'].interpolate(.5,normalized=True).coords[0] for b in cl['baths'].values()]
    ent=cl['entry'].interpolate(.5,normalized=True).coords[0]
    kx,ky=f['hob'].centroid.coords[0]; kit=(kx,ky+0.75)
    D={k:dij(p) for k,p in doors.items()}; de=dij(ent); dk=dij(kit); dbs=[dij(p) for p in bd]
    rr=[D[a][cell(doors[b])] for a in D for b in D if a<b]
    out=dict(hab_hab=round(float(np.mean(rr)),1), hab_hab_max=round(float(max(rr)),1),
      hab_bano=round(float(np.mean([min(db[cell(p)] for db in dbs) for p in doors.values()])),1),
      hab_cocina=round(float(np.mean([dk[cell(p)] for p in doors.values()])),1),
      entrada_hab=round(float(np.mean([de[cell(p)] for p in doors.values()])),1),
      entrada_hab_max=round(float(max(de[cell(p)] for p in doors.values())),1),
      circulo_comun=round(2*maximum_inscribed_circle(cl['field']).length,2),
      comun_estancia_3m=round(cl['field'].buffer(-1.5).buffer(1.5).area,1))
    return out
if __name__=='__main__':
    m=metrics(cluster_local()); print(m); json.dump(m,open('metr_racimo.json','w'))
