import sys,json,math,collections; sys.path.insert(0,'.'); from base import *
def tangent(s):
    a=CL.interpolate(max(0,s-3)); b=CL.interpolate(min(CL.length,s+3)); return (b.x-a.x,b.y-a.y)
segs=[]
for g,p in BLD:
    for poly in polys(g):
        c=list(poly.exterior.coords)
        for (x1,y1),(x2,y2) in zip(c[:-1],c[1:]):
            L=math.hypot(x2-x1,y2-y1)
            if L<0.8: continue
            m=Point((x1+x2)/2,(y1+y2)/2); d=CL.distance(m)
            if d>17: continue
            s=CL.project(m); tx,ty=tangent(s); tn=math.hypot(tx,ty)
            if abs((x2-x1)*tx+(y2-y1)*ty)/(L*tn)<0.8: continue
            q=CL.interpolate(s); cross=tx*(m.y-q.y)-ty*(m.x-q.x)
            side='E' if cross>0 else 'W'   # travel N->S: left(cross>0)=east? check below
            segs.append(dict(rc=p["rc"],side=side,s=s,d=d,L=L,x1=x1,y1=y1,x2=x2,y2=y2))
by=collections.defaultdict(list)
for sg in segs: by[(sg["rc"],sg["side"])].append(sg)
F=[]
props={p["rc"]:p for g,p in BLD}
for (rc,side),L in by.items():
    dmin=min(x["d"] for x in L); keep=[x for x in L if x["d"]<=dmin+2.5]
    # occlusion: building must be first hit from street: check that segment midpoint->centerline ray doesn't cross another building
    F.append(dict(rc=rc,side=side,dmin=round(dmin,1),s0=round(min(min(CL.project(Point(x["x1"],x["y1"])),CL.project(Point(x["x2"],x["y2"]))) for x in keep),1),s1=round(max(max(CL.project(Point(x["x1"],x["y1"])),CL.project(Point(x["x2"],x["y2"]))) for x in keep),1),len=round(sum(x["L"] for x in keep),1),**{k:props[rc].get(k) for k in ("anio","uso","plantas_max","viviendas","unidades")}))
# check side with parcel 31
s31=CL.project(PARCELA.centroid); print("parcela 31 x>cl?",PARCELA.centroid.x>CL.interpolate(s31).x)
F.sort(key=lambda f:(f["side"],f["s0"]))
json.dump(F,open("datos/frentes_ribera.json","w"),indent=0)
for f in F: print(f["side"],f["rc"],f["s0"],f["s1"],f["dmin"],f["anio"],(f["uso"] or "")[:8],f["plantas_max"],f["viviendas"])
print(len(F))
