import numpy as np
from PIL import Image
H='hi/'
names=['MAPA_1_EDIFICIOS','MAPA_2','MAPA_3_CON_TRANSPORTE','MAPA_4_CON_COMERCIO','MAPA_5_CON_EQUIPAMIENTOS','MAPA_6_CON_VERDE','MAPA_COMPLETO']
A=[np.asarray(Image.open(H+n+'.png').convert('RGB')).astype(np.int16) for n in names]
PXM=9001.667/3118.0
def px(x,y): return ((x-438659)*PXM-2046,(4473847-y)*PXM)
np.save('pxm.npy',np.array([PXM]))
for k in range(len(A)):
    base=A[k-1] if k else np.full_like(A[0],255)
    d=np.abs(A[k]-base).sum(2)
    m=d>45
    print(names[k], m.mean().round(4))
    rgba=np.zeros(A[k].shape[:2]+(4,),np.uint8); rgba[...,:3]=A[k]; rgba[...,3]=np.where(m,255,0)
    Image.fromarray(rgba).save(f'hi/diff_{k}.png')
    t=Image.fromarray(rgba); t.thumbnail((700,700)); bg=Image.new('RGB',t.size,'white'); bg.paste(t,mask=t.split()[3]); bg.save(f'/tmp/claude-0/diff_{k}.jpg')
