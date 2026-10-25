import sys, json, math, numpy as np
sys.path.insert(0,'.')
from base import *
from shapely.geometry import Polygon, MultiPolygon, box, Point
from shapely.ops import unary_union
from shapely import prepared
from datetime import datetime, timedelta, timezone
H_PB=4.0; H_PL=3.1   # hipótesis nivel B: PB 4,0 m + 3,1 m por planta
def altura(n): return 0 if not n else H_PB+(n-1)*H_PL
def solpos(dt_utc, lat, lon):
    # NOAA simplified
    doy=dt_utc.timetuple().tm_yday; hr=dt_utc.hour+dt_utc.minute/60
    g=2*math.pi/365*(doy-1+(hr-12)/24)
    eqt=229.18*(0.000075+0.001868*math.cos(g)-0.032077*math.sin(g)-0.014615*math.cos(2*g)-0.040849*math.sin(2*g))
    decl=0.006918-0.399912*math.cos(g)+0.070257*math.sin(g)-0.006758*math.cos(2*g)+0.000907*math.sin(2*g)-0.002697*math.cos(3*g)+0.00148*math.sin(3*g)
    tst=hr*60+eqt+4*lon; ha=math.radians(tst/4-180)
    la=math.radians(lat)
    cosz=math.sin(la)*math.sin(decl)+math.cos(la)*math.cos(decl)*math.cos(ha); z=math.acos(max(-1,min(1,cosz)))
    el=90-math.degrees(z)
    az=math.degrees(math.atan2(math.sin(ha), math.cos(ha)*math.sin(la)-math.tan(decl)*math.cos(la)))+180
    return az%360, el
def sombra(poly,h,az,el):
    if el<=0.5: return None
    L=h/math.tan(math.radians(el)); dx=-L*math.sin(math.radians(az)); dy=-L*math.cos(math.radians(az))
    parts=[poly]
    for p in polys(poly):
        c=list(p.exterior.coords)
        for a,b in zip(c[:-1],c[1:]):
            q=Polygon([a,b,(b[0]+dx,b[1]+dy),(a[0]+dx,a[1]+dy)])
            if q.is_valid and q.area>0: parts.append(q)
    return unary_union(parts)
if __name__=="__main__":
    lat,lon=SITE_LL[1],SITE_LL[0]
    cx,cy=SITE.x,SITE.y; R=90
    zone=box(cx-R,cy-R,cx+R,cy+R)
    obs=[(g,altura(p["plantas_sr"])) for g,p in PRT if g.distance(zone)<60 and p["plantas_sr"]]
    print("partes",len(obs))
    # grid 1 m
    xs=np.arange(cx-R,cx+R,1.0)+0.5; ys=np.arange(cy-R,cy+R,1.0)+0.5
    X,Y=np.meshgrid(xs,ys)
    from shapely import contains_xy
    built=unary_union([g for g,h in obs])
    out={}
    for fecha in ["2026-03-21","2026-06-21","2026-12-21"]:
        d=datetime.fromisoformat(fecha)
        off=2 if d.month in (3,6) and not (d.month==3 and d.day<29) else 1
        if d.month==6: off=2
        if d.month==3: off=1   # 21-mar: horario de invierno (UTC+1)
        if d.month==12: off=1
        hours=np.zeros(X.shape); steps=0; frames={}
        t=datetime(d.year,d.month,d.day,0,0,tzinfo=timezone.utc)
        for m in range(0,24*60,15):
            tt=t+timedelta(minutes=m); az,el=solpos(tt,lat,lon)
            if el<=1: continue
            sh=unary_union([s for s in (sombra(g,h,az,el) for g,h in obs) if s is not None])
            lit=~contains_xy(sh,X,Y)
            hours+=lit*0.25
            loc=(tt+timedelta(hours=off))
            if loc.minute==0 and loc.hour in (9,12,15,18): frames[loc.hour]=(~lit).astype(np.uint8)
        out[fecha]=(hours,frames,off)
        print(fecha,"max horas",hours.max())
    np.savez_compressed("datos/sombras.npz",X=X,Y=Y,**{f"h_{k}":v[0] for k,v in out.items()},**{f"f_{k}_{h}":fr for k,v in out.items() for h,fr in v[1].items()})
    # horas medias sobre la parcela
    inside=contains_xy(PARCELA,X,Y)
    res={k:{"media_parcela_h":round(float(v[0][inside].mean()),2),"min":round(float(v[0][inside].min()),2),"max":round(float(v[0][inside].max()),2),"pct_parcela_>=4h":round(float((v[0][inside]>=4).mean()*100),1),"pct_parcela_>=2h":round(float((v[0][inside]>=2).mean()*100),1)} for k,v in out.items()}
    json.dump({"hipotesis_altura":f"PB {H_PB} m + {H_PL} m/planta (B)","resolucion_m":1,"paso_min":15,"parcela":res},open("datos/sombras_resumen.json","w"),indent=1)
    print(json.dumps(res,indent=1))
