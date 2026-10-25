import sys,json,math,numpy as np; sys.path.insert(0,'.')
from estilo import *
from base import *
from figs1 import add_poly, north_scale, north
from shapely.geometry import box, Point
from matplotlib.patches import Rectangle, Circle
R=json.load(open("datos/fachadas_index.json")); F=json.load(open("datos/frentes_ribera.json")); M=json.load(open("datos/metricas_nuevas.json"))
def code(r): return r["codigo"].replace("W","O")
S31=CL.project(PARCELA.centroid)
def f07():
    fig=fig_mm(178,92)
    ax=fig.add_axes([0.06,0.52,0.86,0.42]); bx=fig.add_axes([0.06,0.1,0.86,0.36],sharex=ax)
    for r in R:
        n=r["plantas_frente"]; h=4+(n-1)*3.1
        if r["side"]=="E":
            ax.add_patch(Rectangle((r["s0"],0),r["s1"]-r["s0"],h,facecolor=PIEDRA,edgecolor=TEC,lw=0.3))
            ax.text((r["s0"]+r["s1"])/2,h+0.8,code(r),fontsize=4.2,ha="center",color=TEC,rotation=90)
        else:
            bx.add_patch(Rectangle((r["s0"],0),r["s1"]-r["s0"],h,facecolor=PIEDRA,edgecolor=TEC,lw=0.3))
            bx.text((r["s0"]+r["s1"])/2,h+0.8,code(r),fontsize=4.2,ha="center",color=TEC,rotation=90)
    b=PARCELA.bounds; p0=CL.project(Point(439996,4473236.8)); p1=CL.project(Point(439997.3,4473221.9))
    ax.add_patch(Rectangle((p0,0),p1-p0,1.2,facecolor=ROSA,edgecolor=MAG,lw=0.6)); ax.text((p0+p1)/2,3,"31",ha="center",fontsize=5.5,color=MAG,weight="bold")
    for a in (ax,bx):
        a.set_ylim(0,38); a.set_yticks([0,10,20,30]); a.tick_params(labelsize=5)
    ax.set_xlim(0,660)
    ax.text(2,35,"ACERA ESTE · IMPARES",fontsize=5.5,weight="bold"); bx.text(2,35,"ACERA OESTE · PARES",fontsize=5.5,weight="bold")
    # altitude
    al=M["alt_perfil"]; s=[x[0] for x in al]; z=[x[1]-2.5 for x in al]
    a2=ax.twinx(); a2.plot(s,z,color=AGUA,lw=0.8); a2.set_ylim(600,660); a2.tick_params(labelsize=5,colors=AGUA); a2.spines["right"].set_visible(True); a2.spines["right"].set_color(AGUA); a2.set_ylabel("cota de calzada · m (B)",fontsize=5,color=AGUA)
    bx.set_xlabel("distancia desde Cascorro por el eje de Ribera · m",fontsize=5.5); ax.set_ylabel("m (plantas × hipótesis)",fontsize=5); bx.set_ylabel("m",fontsize=5)
    for e in META["estaciones"]:
        bx.plot([e["s_m"]],[-2.5],marker="|",color=MAG,ms=3,clip_on=False)
    fig.savefig("fig/F07_perfil.png"); plt.close(fig)
def f08():
    fig=fig_mm(178,215)
    front={r["rc"]+r["side"]:r for r in R}
    halves=[(0,340),(320,660)]
    for k,(s0,s1) in enumerate(halves):
        ax=fig.add_axes([k*0.5+0.005,0.0,0.49,1]); ax.set_aspect("equal"); ax.axis("off")
        p0=CL.interpolate(s0); p1=CL.interpolate(s1); cx=(p0.x+p1.x)/2; cy=(p0.y+p1.y)/2
        Hh=(s1-s0)+20; Ww=Hh*(0.49*178)/215
        ax.set_xlim(cx-Ww/2,cx+Ww/2); ax.set_ylim(cy-Hh/2,cy+Hh/2); view=box(cx-Ww,cy-Hh,cx+Ww,cy+Hh)
        for g,p in BLD:
            if not g.intersects(view): continue
            hit=[front.get(p["rc"]+sd) for sd in "EW" if front.get(p["rc"]+sd)]
            add_poly(ax,g,facecolor="#d8d2c6" if hit else PIEDRA,edgecolor="white",lw=0.2)
            for r in hit:
                pt=g.representative_point(); ax.text(pt.x,pt.y,code(r),fontsize=4.4,ha="center",va="center",color=TINTA,clip_on=True)
        add_poly(ax,PARCELA,facecolor=ROSA,edgecolor=MAG,lw=0.8)
        ax.plot(*CL.xy,color=TINTA,lw=0.4)
        for i,e in enumerate(META["estaciones"]):
            x,y=cam(e); ax.add_patch(Circle((x,y),2.6,facecolor="white",edgecolor=MAG,lw=0.7,zorder=5)); ax.text(x-5,y,f"S{i+1:02d}",fontsize=4.8,ha="right",va="center",color=MAG,zorder=6,clip_on=True)
        if k==0: north(ax,cx+Ww/2-8,cy-Hh/2+8,14)
        if k==1: north_scale(ax,cx-Ww/2+6,cy-Hh/2+6,50,"50 m")
        ax.text(cx-Ww/2+4,cy+Hh/2-10,["TRAMO NORTE · CASCORRO → Nº 31","TRAMO SUR · Nº 31 → RONDA"][k],fontsize=5.5,weight="bold",color=TINTA)
    fig.savefig("fig/F08_recorrido.png"); plt.close(fig)
def f09():
    d=json.load(open("/mnt/user-data/uploads/G3 Proyectos/INVESTIGACIÓN/ANÁLISIS DEL LUGAR PRECISO/DATOS/clima_AEMET_3195.json"))
    fig=fig_mm(178,62); ax=fig.add_axes([0.06,0.18,0.42,0.74]); bx=fig.add_axes([0.56,0.18,0.42,0.74])
    m=list("EFMAMJJASOND"); x=np.arange(12)
    ax.plot(x,d["TM"],color="#c0392b",lw=1); ax.plot(x,d["T"],color=TINTA,lw=1); ax.plot(x,d["Tm"],color=AGUA,lw=1,ls=(0,(2,1.5)))
    for arr,c in ((d["TM"],"#c0392b"),(d["Tm"],AGUA)):
        for i in (0,6): ax.text(i,arr[i]+0.9,f"{arr[i]:.1f}",fontsize=5,ha="center",color=c)
    ax.set_xticks(x); ax.set_xticklabels(m,fontsize=5.5); ax.set_ylabel("°C",fontsize=5.5); ax.set_ylim(0,36)
    ax.text(0,34,"T máx. media · T media · T mín. media",fontsize=5,color=TEC)
    bx.bar(x,d["R"],color=AGUA,width=0.6)
    for i,v in enumerate(d["R"]): bx.text(i,v+1,str(v),fontsize=5,ha="center",color=TEC)
    bx.set_xticks(x); bx.set_xticklabels(m,fontsize=5.5); bx.set_ylabel("mm",fontsize=5.5); bx.set_ylim(0,70)
    fig.savefig("fig/F09_clima.png"); plt.close(fig)
def f10():
    osm=json.load(open("/mnt/user-data/uploads/G3 Proyectos/INVESTIGACIÓN/CATALOGO_PATRONES_600M/DATOS/ambito_osm_recortado.geojson"))
    from shapely.geometry import shape
    trees=[];benches=[];water=[]
    for f in osm["features"]:
        p=f["properties"]; s=json.dumps(p)
        try: g=shape(f["geometry"])
        except Exception: continue
        if g.is_empty: continue
        pt=g if g.geom_type=="Point" else g.representative_point()
        x,y=T.transform(pt.x,pt.y); q=Point(x,y)
        if q.distance(SITE)>300: continue
        if '"natural": "tree"' in s and g.geom_type=="Point": trees.append(q)
        if '"amenity": "bench"' in s: benches.append(q)
        if '"amenity": "drinking_water"' in s: water.append(q)
    fig=fig_mm(178,150); ax=fig.add_axes([0,0.05,1,0.95]); ax.set_aspect("equal"); ax.axis("off")
    R_=210; ax.set_xlim(SITE.x-R_*1.19,SITE.x+R_*1.19); ax.set_ylim(SITE.y-R_,SITE.y+R_)
    for g,p in BLD: add_poly(ax,g,facecolor=PIEDRA,edgecolor="white",lw=0.15)
    ax.scatter([t.x for t in trees],[t.y for t in trees],s=2.2,color=VERDE,lw=0)
    ax.scatter([t.x for t in benches],[t.y for t in benches],s=5,marker="s",facecolor="none",edgecolor=TINTA,lw=0.35)
    ax.scatter([t.x for t in water],[t.y for t in water],s=10,color=AGUA,lw=0)
    add_poly(ax,PARCELA,facecolor=ROSA,edgecolor=MAG,lw=0.8)
    for r in (100,200): ax.add_patch(Circle((SITE.x,SITE.y),r,fill=False,lw=0.5,ls=(0,(3,2)),color=TEC))
    north_scale(ax,SITE.x-R_*1.15,SITE.y-R_+6,50,"50 m"); north(ax,SITE.x+R_*1.12,SITE.y-R_+6,14)
    n100=sum(1 for t in trees if t.distance(SITE)<=100); n200=sum(1 for t in trees if t.distance(SITE)<=200)
    b100=sum(1 for t in benches if t.distance(SITE)<=100); w200=sum(1 for t in water if t.distance(SITE)<=200)
    json.dump({"arboles_100":n100,"arboles_200":n200,"bancos_100":b100,"bancos_200":sum(1 for t in benches if t.distance(SITE)<=200),"agua_200":w200,"agua_min_m":round(min(t.distance(SITE) for t in water),1)},open("datos/estancia.json","w"))
    fig.savefig("fig/F10_arboles_estancia.png"); plt.close(fig)
if __name__=="__main__":
    f07(); f08(); f09(); f10(); print(open("datos/estancia.json").read())
