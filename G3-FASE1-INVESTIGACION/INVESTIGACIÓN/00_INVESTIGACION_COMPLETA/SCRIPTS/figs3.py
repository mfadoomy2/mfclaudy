import sys,json,math,numpy as np; sys.path.insert(0,'.')
from estilo import *
from base import *
from figs1 import add_poly, north_scale, north
from sombras import altura, solpos
from shapely.geometry import LineString, box
from matplotlib.patches import Rectangle
from datetime import datetime, timezone
def cortar(line, exclude=()):
    segs=[]
    for g,p in PRT:
        if p["rc"] in exclude or not p["plantas_sr"]: continue
        x=line.intersection(g)
        if x.is_empty: continue
        for s in getattr(x,"geoms",[x]):
            if s.length<0.3: continue
            a=line.project(Point(s.coords[0])); b=line.project(Point(s.coords[-1]))
            segs.append((min(a,b),max(a,b),altura(p["plantas_sr"]),p["plantas_sr"],p["rc"]))
    return segs
def f06():
    ymid=4473229.4
    A=LineString([(439935,ymid),(440085,ymid)])
    xm=440021
    B=LineString([(xm,4473160),(xm,4473300)])
    fig=fig_mm(178,120)
    # A-A'
    ax=fig.add_axes([0.06,0.56,0.92,0.4]); 
    segs=cortar(A)
    for a,b,h,n,rc in segs: ax.add_patch(Rectangle((a,0),b-a,h,facecolor=PIEDRA,edgecolor=TEC,lw=0.3))
    pa=A.intersection(PARCELA); a=A.project(Point(pa.coords[0])); b=A.project(Point(pa.coords[-1]))
    ax.add_patch(Rectangle((min(a,b),-0.4),abs(b-a),0.4,facecolor=ROSA,edgecolor=MAG,lw=0.6))
    cl=A.intersection(CL); xc=A.project(cl) if not cl.is_empty else None
    ax.axvline(xc,color=TEC,lw=0.3,ls=(0,(3,3)))
    ax.text(xc,-2.2,"eje Ribera",ha="center",fontsize=5,color=TEC)
    ax.text((a+b)/2,1.2,"PARCELA 31\n651 m² · suelo sin edificar",ha="center",fontsize=5.5,color=MAG)
    # street width
    wx=[s for s in segs if s[1]<xc]; wx=max(s[1] for s in wx); ex=min(a,b)
    ax.annotate("",xy=(wx,30),xytext=(ex,30),arrowprops=dict(arrowstyle="<->",lw=0.5,color=MAG,mutation_scale=5)); ax.text((wx+ex)/2,30.8,f"{ex-wx:.1f} m entre línea de fachada y lindero",ha="center",fontsize=5.5,color=MAG)
    ax.set_xlim(0,150); ax.set_ylim(-3,36); ax.set_aspect("equal"); 
    ax.spines["bottom"].set_visible(False); ax.set_xticks([]); ax.set_yticks([0,10,20,30]); ax.set_ylabel("m",fontsize=5.5)
    ax.text(0,34.5,"A–A′  ·  SECCIÓN OESTE–ESTE POR EL CENTRO DEL FRENTE",fontsize=6,weight="bold",color=TINTA)
    ax.text(150,34.5,"oeste ← → este",ha="right",fontsize=5.5,color=TEC)
    # B-B'
    bx=fig.add_axes([0.06,0.08,0.92,0.4])
    segs=cortar(B)
    for a,b,h,n,rc in segs: bx.add_patch(Rectangle((a,0),b-a,h,facecolor=PIEDRA,edgecolor=TEC,lw=0.3)); 
    pa=B.intersection(PARCELA); a=B.project(Point(pa.coords[0])); b=B.project(Point(pa.coords[-1]))
    pa0,pa1=min(a,b),max(a,b)
    bx.add_patch(Rectangle((pa0,-0.4),pa1-pa0,0.4,facecolor=ROSA,edgecolor=MAG,lw=0.6))
    # south obstacle top: highest seg just south (smaller distance along B since B goes S->N)
    south=[s for s in segs if s[1]<=pa0+0.5]; top=max(south,key=lambda s:s[1]) ; 
    sx=top[1]; sh=top[2]
    lat,lon=SITE_LL[1],SITE_LL[0]
    for fecha,col,lab,utc in [("2026-12-21",AGUA,"21 dic",11.3),("2026-03-21","#e8683a","21 mar",11.4),("2026-06-21","#7a1616","21 jun",11.3)]:
        best=max(((solpos(datetime(2026,int(fecha[5:7]),21,int(m//60),int(m%60),tzinfo=timezone.utc),lat,lon)) for m in range(600,780,2)),key=lambda t:t[1])
        el=best[1]; L=sh/math.tan(math.radians(el))
        bx.plot([sx,sx+L],[sh,0],color=col,lw=0.7); yl={"21 dic":9,"21 mar":14,"21 jun":19}[lab]; xl=sx+(sh-yl)/math.tan(math.radians(el)); bx.text(xl+1.2,yl,f"{lab} · {el:.0f}° · sombra {L:.0f} m",fontsize=5.2,color=col,ha="left",va="center")
    bx.text((pa0+pa1)/2,-2.4,"PARCELA 31",ha="center",fontsize=5.5,color=MAG)
    bx.text(sx-1,sh+0.8,f"vecino sur: {top[3]} plantas (catastro)",ha="right",fontsize=5.2,color=TEC)
    bx.set_xlim(0,140); bx.set_ylim(-3,36); bx.set_aspect("equal"); bx.spines["bottom"].set_visible(False); bx.set_xticks([]); bx.set_yticks([0,10,20,30]); bx.set_ylabel("m",fontsize=5.5)
    bx.text(0,34.5,"B–B′  ·  SECCIÓN SUR–NORTE POR EL FONDO MEDIO DE LA PARCELA · SOL A MEDIODÍA SOLAR",fontsize=6,weight="bold",color=TINTA)
    bx.text(140,34.5,"sur ← → norte",ha="right",fontsize=5.5,color=TEC)
    fig.savefig("fig/F06_secciones.png"); plt.close(fig)
    json.dump({"ancho_calle_31":round(ex-wx,1),"vecino_sur_plantas":top[3],"vecino_sur_altura_B":sh},open("datos/seccion.json","w"))
if __name__=="__main__":
    f06(); print(open("datos/seccion.json").read())
