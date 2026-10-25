import sys,json,math,numpy as np; sys.path.insert(0,'.')
from estilo import *
from base import *
from shapely.geometry import box, Point
from matplotlib.patches import Polygon as MPoly, Rectangle, Circle
from matplotlib.collections import PatchCollection
import matplotlib.colors as mcolors
M=json.load(open("datos/metricas_nuevas.json"))
def add_poly(ax,g,**kw):
    for p in polys(g):
        ax.add_patch(MPoly(np.array(p.exterior.coords),closed=True,**kw))
def north_scale(ax,x,y,L=50,label="50 m"):
    ax.plot([x,x+L],[y,y],color=TINTA,lw=0.8,solid_capstyle="butt"); ax.plot([x,x],[y-1.2,y+1.2],color=TINTA,lw=0.6); ax.plot([x+L,x+L],[y-1.2,y+1.2],color=TINTA,lw=0.6)
    ax.text(x+L/2,y+2.5,label,ha="center",va="bottom",fontsize=5.5,color=TEC)
def north(ax,x,y,s=8):
    ax.annotate("",xy=(x,y+s),xytext=(x,y),arrowprops=dict(arrowstyle="-|>",lw=0.6,color=TINTA,mutation_scale=6)); ax.text(x,y+s+1.5,"N",ha="center",fontsize=6)
# ---------- F01 parcela y colindantes
def f01():
    fig=fig_mm(178,120); ax=fig.add_axes([0,0,1,1]); ax.set_aspect("equal"); ax.axis("off")
    c=PARCELA.centroid; W=100; H=W*120/178
    ax.set_xlim(c.x-W/2-8,c.x+W/2-8); ax.set_ylim(c.y-H/2,c.y+H/2)
    view=box(c.x-W,c.y-W,c.x+W,c.y+W)
    for g,p in PRT:
        if not g.intersects(view): continue
        n=p["plantas_sr"] or 0
        add_poly(ax,g,facecolor=PIEDRA,edgecolor="white",lw=0.5)
        if g.intersects(box(c.x-60,c.y-40,c.x+40,c.y+40)) and g.area>25 and n>0:
            pt=g.representative_point(); ax.text(pt.x,pt.y,str(n),ha="center",va="center",fontsize=5,color=TEC)
    for g,p in BLD:
        if g.intersects(view): add_poly(ax,g,facecolor="none",edgecolor=CONTX,lw=0.5)
    add_poly(ax,PARCELA,facecolor=ROSA,edgecolor=TINTA,lw=0.9,alpha=0.9)
    ax.plot(*CL.xy,color=TINTA,lw=0.4,ls=(0,(4,3)))
    # dimensions
    ax.annotate("",xy=(439993.5,4473221.9),xytext=(439993.5,4473236.83),arrowprops=dict(arrowstyle="<->",lw=0.5,color=MAG,mutation_scale=5))
    ax.text(439992.3,4473229.4,"14,9 m",rotation=90,ha="right",va="center",fontsize=6,color=MAG)
    ax.annotate("",xy=(439996.07,4473219.2),xytext=(440045.55,4473219.2),arrowprops=dict(arrowstyle="<->",lw=0.5,color=MAG,mutation_scale=5))
    ax.text(440020.8,4473217.8,"49,5 m",ha="center",va="top",fontsize=6,color=MAG)
    ax.text(440021,4473230,"0134911VK4703C\n651 m²",ha="center",va="center",fontsize=6.5,color=TINTA)
    ax.text(439983.5,4473262,"RIBERA DE CURTIDORES",rotation=-89,ha="center",va="center",fontsize=5.5,color=TEC)
    north_scale(ax,c.x-W/2-4,c.y-H/2+4,20,"20 m"); north(ax,c.x+W/2-14,c.y-H/2+4)
    fig.savefig("fig/F01_parcela.png"); plt.close(fig)
# ---------- F02/F03 mapas alturas / años (radio 200)
def mapa(campo,fn,cmap,norm,label,ticks):
    fig=fig_mm(178,150); ax=fig.add_axes([0,0.1,1,0.9]); ax.set_aspect("equal"); ax.axis("off")
    R=210; ax.set_xlim(SITE.x-R*1.19/1.0,SITE.x+R*1.19/1.0); ax.set_ylim(SITE.y-R,SITE.y+R)
    C=SITE.buffer(200,resolution=128)
    osm=json.load(open("/mnt/user-data/uploads/G3 Proyectos/INVESTIGACIÓN/CATALOGO_PATRONES_600M/DATOS/ambito_osm_recortado.geojson"))
    from shapely.geometry import shape
    for f in osm["features"]:
        pr=f["properties"]
        if pr.get("building") or "building" in json.dumps(pr)[:0]:
            pass
    # context: catastro buildings outside circle in stone grey
    src=PRT if campo=="plantas_sr" else BLD
    for g,p in src:
        if not g.intersects(C.buffer(60)): continue
        v=p.get(campo)
        if g.centroid.within(C) and v:
            add_poly(ax,g,facecolor=cmap(norm(v)),edgecolor="white",lw=0.15)
        else:
            add_poly(ax,g,facecolor=PIEDRA,edgecolor="white",lw=0.15)
    ax.add_patch(Circle((SITE.x,SITE.y),200,fill=False,lw=0.5,ls=(0,(3,2)),color=TEC)); ax.add_patch(Circle((SITE.x,SITE.y),100,fill=False,lw=0.5,ls=(0,(3,2)),color=TEC))
    ax.text(SITE.x+200*0.71,SITE.y+200*0.71,"200 m",fontsize=5.5,color=TEC); ax.text(SITE.x+100*0.71,SITE.y+100*0.71,"100 m",fontsize=5.5,color=TEC)
    add_poly(ax,PARCELA,facecolor=ROSA,edgecolor=MAG,lw=0.8)
    ax.plot(*CL.xy,color=TINTA,lw=0.35,ls=(0,(4,3)))
    north_scale(ax,SITE.x-R*1.15,SITE.y-R+6,50,"50 m"); north(ax,SITE.x+R*1.12,SITE.y-R+6,14)
    cax=fig.add_axes([0.03,0.045,0.35,0.018]); cb=matplotlib.colorbar.ColorbarBase(cax,cmap=cmap,norm=norm,orientation="horizontal",ticks=ticks)
    cb.outline.set_visible(False); cax.tick_params(labelsize=5.5,length=0); fig.text(0.03,0.075,spaced(label),fontsize=5,color=TEC)
    fig.savefig(fn); plt.close(fig)
if __name__=="__main__":
    f01()
    cm=mcolors.LinearSegmentedColormap.from_list("alt",["#e7e2d9","#b9b2a6","#7d766b","#3f3b35","#141414"])
    mapa("plantas_sr","fig/F02_alturas.png",cm,mcolors.BoundaryNorm([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,11.5],cm.N),"plantas sobre rasante · catastro",[1,2,3,4,5,6,7,8,9,10])
    cy=mcolors.LinearSegmentedColormap.from_list("anio",["#5a3312","#a0633a","#d6a77a","#efe0cc","#9ec6c0","#2e7f9e"])
    mapa("anio","fig/F03_anios.png",cy,mcolors.BoundaryNorm([1800,1880,1900,1930,1960,1980,2000,2026],cy.N),"año de construcción · catastro",[1800,1880,1900,1930,1960,1980,2000,2026])
    print("ok")
