import sys,json,math,numpy as np; sys.path.insert(0,'.')
from estilo import *
from base import *
from figs1 import add_poly, north_scale, north
from shapely.geometry import box
import matplotlib.colors as mcolors
def f04():
    Z=np.load("datos/sombras.npz"); X=Z["X"]; Y=Z["Y"]
    fig=fig_mm(178,78)
    cm=mcolors.LinearSegmentedColormap.from_list("cal",CALOR)
    dates=[("2026-12-21","21 DIC"),("2026-03-21","21 MAR"),("2026-06-21","21 JUN")]
    view=box(X.min(),Y.min(),X.max(),Y.max())
    for i,(k,lab) in enumerate(dates):
        ax=fig.add_axes([i/3+0.004,0.14,1/3-0.008,0.84]); ax.set_aspect("equal"); ax.axis("off")
        h=Z[f"h_{k}"]; 
        ax.imshow(h,origin="lower",extent=[X.min()-0.5,X.max()+0.5,Y.min()-0.5,Y.max()+0.5],cmap=cm,vmin=0,vmax=14,interpolation="nearest")
        for g,p in BLD:
            if g.intersects(view): add_poly(ax,g,facecolor=PIEDRA,edgecolor="white",lw=0.2)
        add_poly(ax,PARCELA,facecolor="none",edgecolor=MAG,lw=0.8)
        c=SITE; ax.set_xlim(c.x-70,c.x+70); ax.set_ylim(c.y-70,c.y+70)
        ax.text(c.x-68,c.y+64,lab,fontsize=6.5,color=TINTA,weight="bold")
        if i==0: north_scale(ax,c.x-66,c.y-66,20,"20 m")
    cax=fig.add_axes([0.02,0.06,0.3,0.025]); cb=matplotlib.colorbar.ColorbarBase(cax,cmap=cm,norm=mcolors.Normalize(0,14),orientation="horizontal",ticks=[0,2,4,6,8,10,12,14])
    cb.outline.set_visible(False); cax.tick_params(labelsize=5.5,length=0)
    fig.text(0.34,0.065,spaced("horas de sol directo sobre el suelo · paso 15 min · celda 1 m"),fontsize=5,color=TEC)
    fig.savefig("fig/F04_sol_suelo.png"); plt.close(fig)
def f05():
    d=json.load(open("datos/sol_por_altura.json"))
    fig=fig_mm(178,70); ax=fig.add_axes([0.08,0.17,0.62,0.78])
    cols={"2026-12-21":AGUA,"2026-03-21":"#e8683a","2026-06-21":"#7a1616"}; labs={"2026-12-21":"21 dic","2026-03-21":"21 mar","2026-06-21":"21 jun"}
    for k,v in d.items():
        z=[float(a) for a in v]; m=[v[a]["media"] for a in v]; p=[v[a]["p90"] for a in v]
        ax.plot(m,z,color=cols[k],lw=1.2,marker="o",ms=2.2,label=labs[k]+" · media"); ax.plot(p,z,color=cols[k],lw=0.6,ls=(0,(2,2)))
    for n in range(0,10):
        zz=0 if n==0 else 4.0+(n-1)*3.1
    ax.set_xlabel("horas de sol directo sobre el plano horizontal a cota z (media de la parcela; discontinua = percentil 90)",fontsize=5.5)
    ax.set_ylabel("cota z sobre la acera · m",fontsize=5.5); ax.set_xlim(0,15.5); ax.set_ylim(-0.5,27)
    ax.axhspan(19.5,22.6,color=PANEL,zorder=0)
    ax.legend(frameon=False,fontsize=5.5,loc="lower right")
    ax2=fig.add_axes([0.74,0.17,0.24,0.78]); ax2.axis("off")
    ax2.set_xlim(0,1); ax2.set_ylim(-0.5,27)
    for n in range(1,9):
        z0=0 if n==1 else 4.0+(n-2)*3.1; z1=4.0+(n-1)*3.1
        ax2.add_patch(Rectangle((0.05,z0),0.35,z1-z0,fill=False,lw=0.4,edgecolor=TEC)); ax2.text(0.45,(z0+z1)/2,f"planta {n-1 if n>1 else 'baja'}",fontsize=5,va="center",color=TEC)
    ax2.text(0.05,-1.6,"HIPÓTESIS DE ALTURAS (B): PB 4,0 m · plantas 3,1 m",fontsize=5,color=TEC,va="top")
    fig.savefig("fig/F05_sol_altura.png"); plt.close(fig)
from matplotlib.patches import Rectangle
if __name__=="__main__":
    f04()
    import os
    if os.path.exists("datos/sol_por_altura.json"): f05()
    print("ok")
