import sys,json,math,numpy as np; sys.path.insert(0,'.')
from sombras import *
from shapely import contains_xy
from datetime import datetime,timedelta,timezone
lat,lon=SITE_LL[1],SITE_LL[0]
b=PARCELA.bounds; xs=np.arange(b[0],b[2],0.5)+0.25; ys=np.arange(b[1],b[3],0.5)+0.25; X,Y=np.meshgrid(xs,ys)
ins=contains_xy(PARCELA,X,Y)
obs=[(g,altura(p["plantas_sr"])) for g,p in PRT if g.distance(PARCELA)<120 and p["plantas_sr"] and p["rc"]!="0134911VK4703C"]
res={}
for fecha,off in [("2026-12-21",1),("2026-03-21",1),("2026-06-21",2)]:
    d=datetime.fromisoformat(fecha); res[fecha]={}
    suns=[]
    for m in range(0,1440,15):
        tt=datetime(d.year,d.month,d.day,tzinfo=timezone.utc)+timedelta(minutes=m); az,el=solpos(tt,lat,lon)
        if el>1: suns.append((az,el))
    for z in [0,4,7.1,10.2,13.3,16.4,19.5,22.6,25.7]:
        hours=np.zeros(X.shape)
        for az,el in suns:
            sh=[sombra(g,h-z,az,el) for g,h in obs if h>z+0.1]
            sh=unary_union([s for s in sh if s is not None])
            hours+= (~contains_xy(sh,X,Y))*0.25
        v=hours[ins]; res[fecha][z]={"media":round(float(v.mean()),2),"p90":round(float(np.percentile(v,90)),2),"pct_2h":round(float((v>=2).mean()*100),1)}
        print(fecha,z,res[fecha][z],flush=True)
json.dump(res,open("datos/sol_por_altura.json","w"),indent=1)
