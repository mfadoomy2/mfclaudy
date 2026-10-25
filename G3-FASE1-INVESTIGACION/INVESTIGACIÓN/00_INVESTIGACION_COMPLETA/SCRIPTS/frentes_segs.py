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
def get(rc,side):
    L=by[(rc,side)]; dmin=min(x["d"] for x in L); return [x for x in L if x["d"]<=dmin+2.5]
