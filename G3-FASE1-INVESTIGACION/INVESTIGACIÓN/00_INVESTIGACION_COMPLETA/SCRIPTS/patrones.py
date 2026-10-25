import json
from PIL import Image
R={r["codigo"]:r for r in json.load(open("datos/fachadas_index.json"))}
RES=0.03
def zrow(r,z):
    H=(r["plantas_max"] or 6)*3.2+4.0
    return int((H-z)/RES)
def crop(code,z0,z1,w,fx=0.5,out=None):
    r=R[code]; im=Image.open(r["file"]); W=im.width
    cx=int(W*fx); hw=int(w/2/RES)
    x0=max(0,cx-hw); x1=min(W,cx+hw)
    y0=max(0,zrow(r,z1)); y1=min(im.height,zrow(r,z0))
    c=im.crop((x0,y0,x1,y1))
    if out: c.save(out,quality=90)
    return c
def ztop(code): r=R[code]; return 4+(r["plantas_frente"]-1)*3.1
P=[
 dict(id="P01",nombre="Hueco vertical con balcón propio",pregunta="¿Cada hueco tiene su propio balcón?",campo=("balcon","ind"),banda="alta",casos=["W02","W03","W09","W11","E07","E14","W13","W18"]),
 dict(id="P02",nombre="Planta baja comercial que se cierra",pregunta="¿Qué fachada queda cuando el comercio cierra?",campo=("cierre",1),banda="pb",casos=["E10","E09","E14","E06","W04","W06","E12","W16"]),
 dict(id="P03",nombre="Basamento que cambia al tocar la calle",pregunta="¿Qué material recibe el contacto de la acera?",campo=("zocalo",1),banda="pb",casos=["W02","W03","W11","W13","W18","W19","W22","E14"]),
 dict(id="P04",nombre="Recercado: un segundo borde del hueco",pregunta="¿Cómo se marca el borde de cada ventana?",campo=("recercado",1),banda="alta",casos=["E14","W09","W18","W04","E06","W11","W14","E16"]),
 dict(id="P05",nombre="Textil en las plantas altas",pregunta="¿Quién controla la sombra de cada vivienda?",campo=("toldo_alto",1),banda="alta",casos=["E10","E16","E07","W13","W14","E08","W17","W09"]),
 dict(id="P06",nombre="Plantas en el balcón",pregunta="¿Dónde se cultiva cuando no hay suelo?",campo=("vegetal",1),banda="alta",casos=["W13","W14","E10","W18","W15","E06","E07","E12"]),
 dict(id="P07",nombre="Alero y cornisa que vuelan",pregunta="¿Cómo termina la fachada contra el cielo?",campo=("alero",1),banda="top",casos=["W02","W13","W14","E06","E07","W09","E10","W16"]),
 dict(id="P08",nombre="Instalaciones como segunda trama",pregunta="¿Por dónde pasan los cables y las máquinas?",campo=("instal",1),banda="media",casos=["E11","W06","E02","W04","W12","E16","E06","E12"]),
 dict(id="P09",nombre="Exposición que ocupa la acera",pregunta="¿Hasta dónde llega la tienda?",campo=("expo",1),banda="pb",casos=["W18","W19","W21","W14","W02","W03","E16","W16"]),
]
def bands(p,code):
    r=R[code]; zt=ztop(code)
    if p["banda"]=="pb": return (-0.2,5.6,9.0)
    if p["banda"]=="alta": return (max(4.5,zt-10.5),min(zt,max(4.5,zt-10.5)+10),8.8)
    if p["banda"]=="top": return (zt-5.5,zt+1.8,8.8)
    if p["banda"]=="media": return (1.0,11.0,8.8)
if __name__=="__main__":
    import os; os.makedirs("fig/panel",exist_ok=True)
    import sys; sys.path.insert(0,"datos"); from codificacion_fachadas import C
    for p in P:
        k,v=p["campo"]
        for c in p["casos"]:
            assert C[c][k]==v,(p["id"],c,C[c][k])
            z0,z1,w=bands(p,c); crop(c,z0,z1,w,out=f"fig/panel/{p['id']}_{c}.jpg")
        n=sum(1 for x in C.values() if x[k]==v); N=sum(1 for x in C.values() if x[k] is not None)
        p["n"]=n; p["N"]=N
        print(p["id"],n,N)
    json.dump(P,open("datos/patrones.json","w"),indent=0,ensure_ascii=False)
