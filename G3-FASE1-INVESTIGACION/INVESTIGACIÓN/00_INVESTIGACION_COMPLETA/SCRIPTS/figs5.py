import sys,json,numpy as np; sys.path.insert(0,'.'); sys.path.insert(0,'datos')
from estilo import *
from codificacion_fachadas import C
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors
R=json.load(open("datos/fachadas_index.json"))
def code(c): return c.replace("W","O")
def matriz():
    cols=[("pb_com","PB comercial"),("cierre","cierre enrollable"),("grafiti","grafiti"),("zocalo","basamento"),("ejes","ejes verticales"),("recercado","recercado"),("toldo_alto","textil alto"),("vegetal","plantas"),("alero","alero"),("instal","instalaciones"),("expo","exposición"),("mirador","mirador")]
    order=[r["codigo"] for r in sorted(R,key=lambda r:(r["side"],r["s0"]))]
    fig=fig_mm(178,150); ax=fig.add_axes([0.12,0.02,0.66,0.86]); ax.axis("off")
    n=len(order); m=len(cols)
    ax.set_xlim(0,m+2.2); ax.set_ylim(n+0.5,-2.5)
    for j,(k,l) in enumerate(cols): ax.text(j+0.5,-0.3,l,rotation=55,ha="left",va="bottom",fontsize=5.2,color=TEC,rotation_mode="anchor")
    ax.text(m+0.3,-0.3,"balcón",rotation=55,ha="left",va="bottom",fontsize=5.2,color=TEC,rotation_mode="anchor")
    ax.text(m+1.3,-0.3,"acabado",rotation=55,ha="left",va="bottom",fontsize=5.2,color=TEC,rotation_mode="anchor")
    for i,c in enumerate(order):
        r=next(x for x in R if x["codigo"]==c)
        ax.text(-0.2,i+0.5,f"{code(c)}  {r['anio']}  {r['plantas_frente']} pl",ha="right",va="center",fontsize=5,color=TINTA)
        for j,(k,l) in enumerate(cols):
            v=C[c][k]
            if v==1: ax.add_patch(Rectangle((j+0.1,i+0.12),0.8,0.76,facecolor=TINTA,lw=0))
            elif v==0: ax.add_patch(Rectangle((j+0.1,i+0.12),0.8,0.76,facecolor="white",edgecolor=FILETE,lw=0.4))
            else: ax.add_patch(Rectangle((j+0.1,i+0.12),0.8,0.76,facecolor=PANEL,edgecolor=FILETE,lw=0.4,hatch="/////"))
        b=C[c]["balcon"]; ax.text(m+0.5,i+0.5,{"ind":"ind.","corr":"corrido","mixto":"mixto","ninguno":"—",None:"n/l"}[b],fontsize=4.8,va="center",color=TEC)
        ac=C[c]["acabado"] or "n/l"; ax.text(m+1.5,i+0.5,ac,fontsize=4.8,va="center",color=TEC)
        if c=="E15": ax.plot([0,m+2.2],[i+1,i+1],color=MAG,lw=0.6); ax.text(m+2.3,i+1,"← solar nº 31",fontsize=5,color=MAG,va="center")
    # side separator
    k=sum(1 for c in order if c.startswith("E")); ax.plot([0,m+2.2],[k,k],color=TINTA,lw=0.8)
    ax.text(m+2.3,k,"↑ acera este\n↓ acera oeste",fontsize=5,color=TINTA,weight="bold",va="center")
    # totals
    tx=fig.add_axes([0.76,0.02,0.22,0.86]); tx.axis("off"); tx.set_xlim(0,1); tx.set_ylim(n+0.5,-2.5)
    fig.savefig("fig/F11_matriz.png"); plt.close(fig)
def anios():
    fig=fig_mm(178,40); ax=fig.add_axes([0.06,0.25,0.9,0.7])
    for r in R:
        y=0.6 if r["side"]=="E" else -0.6
        col={True:"#5a3312"}.get(r["anio"]<1900,"#d6a77a" if r["anio"]<1960 else ("#9ec6c0" if r["anio"]<2000 else AGUA))
        ax.add_patch(Rectangle((r["s0"],y-0.45 if y>0 else y-0.05),r["s1"]-r["s0"],0.5,facecolor=col,edgecolor="white",lw=0.3))
        ax.text((r["s0"]+r["s1"])/2,y+0.2 if y>0 else y-0.62,str(r["anio"]),fontsize=4.2,ha="center",rotation=90,va="bottom" if y>0 else "top",color=TEC)
    ax.set_xlim(0,660); ax.set_ylim(-1.8,1.8); ax.set_yticks([0.35,-0.35]); ax.set_yticklabels(["este","oeste"],fontsize=5.5); ax.tick_params(labelsize=5)
    ax.axhline(0,color=TEC,lw=0.3,ls=(0,(3,3)))
    ax.set_xlabel("distancia desde Cascorro · m",fontsize=5.5)
    fig.savefig("fig/F12_anios_frentes.png"); plt.close(fig)
if __name__=="__main__": matriz(); anios(); print("ok")
