from proponer import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection,LineCollection
from matplotlib import colors as mc
from shapely.geometry import shape

def triangles(parts,exclude=[]):
 tri=[];color=[];names=[]
 for part in parts:
  if any(s in part['layer'] for s in exclude):continue
  if 'triangles' in part:ts=np.array(part['triangles'])
  else:
   p=Polygon(part['polygon'],part.get('holes',[]));z0,z1=part['z'];ts=[]
   for g in constrained_delaunay_triangles(p).geoms:
    xy=np.array(g.exterior.coords)[:3];ts.extend([np.c_[xy,np.full(3,z0)][::-1],np.c_[xy,np.full(3,z1)]])
   for ring in [p.exterior]+list(p.interiors):
    a=np.array(ring.coords)
    for x,y in zip(a[:-1],a[1:]):ts.extend([np.array([[*x,z0],[*y,z0],[*y,z1]]),np.array([[*x,z0],[*y,z1],[*x,z1]])])
   ts=np.array(ts)
  tri.extend(ts);color.extend([mc.to_rgb(part['color'])]*len(ts));names.extend([part['layer']]*len(ts))
 return np.array(tri,dtype=np.float32),np.array(color,dtype=np.float32),names

def raster(t,c,u,v,W=1600,H=1100):
 d=np.cross(u,v);ns=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);ns/=np.maximum(np.linalg.norm(ns,axis=1)[:,None],1e-10);light=.66+.34*np.abs(ns@np.array([.25,-.5,.83]));c=np.clip(c*light[:,None]*255,0,255).astype(np.uint8)
 xy=np.stack([t@u,t@v],axis=-1);dep=t@d;lo=xy.min(axis=(0,1));hi=xy.max(axis=(0,1));sc=min((W-60)/(hi[0]-lo[0]),(H-60)/(hi[1]-lo[1]));xy=(xy-(lo+hi)/2)*sc;xy[:,:,0]+=W/2;xy[:,:,1]=H/2-xy[:,:,1]
 im=np.full((H,W,3),255,np.uint8);buf=np.full((H,W),-np.inf,np.float32)
 for pts,zz,col in zip(xy,dep,c):
  x0,y0=np.maximum(np.floor(pts.min(axis=0)).astype(int),[0,0]);x1,y1=np.minimum(np.ceil(pts.max(axis=0)).astype(int),[W-1,H-1]);
  if x1<x0 or y1<y0:continue
  A,Bb,C=pts;den=(Bb[1]-C[1])*(A[0]-C[0])+(C[0]-Bb[0])*(A[1]-C[1])
  if abs(den)<1e-8:continue
  xx=np.arange(x0,x1+1,dtype=np.float32)[None,:]+.5;yy=np.arange(y0,y1+1,dtype=np.float32)[:,None]+.5
  w0=((Bb[1]-C[1])*(xx-C[0])+(C[0]-Bb[0])*(yy-C[1]))/den;w1=((C[1]-A[1])*(xx-C[0])+(A[0]-C[0])*(yy-C[1]))/den;w2=1-w0-w1;depth=w0*zz[0]+w1*zz[1]+w2*zz[2];dst=buf[y0:y1+1,x0:x1+1];mask=(w0>=-1e-5)&(w1>=-1e-5)&(w2>=-1e-5)&(depth>dst);dst[mask]=depth[mask];im[y0:y1+1,x0:x1+1][mask]=col
 return im

def draw(parts,out,title,subtitle='',exclude=[],u=None,v=None):
 t,c,names=triangles(parts,exclude)
 if u is None:u=np.array([.86,-.51,0]);v=np.array([.29,.49,.822])
 im=raster(t,c,u,v)
 fig,ax=plt.subplots(figsize=(13,10));ax.imshow(im);ax.axis('off');fig.subplots_adjust(top=.87,bottom=.1);fig.text(.06,.95,title,fontsize=21,weight='bold');fig.text(.06,.905,subtitle,fontsize=11);fig.text(.06,.035,'G3 / RIBERA 31     •     PROPUESTA DE ESTUDIO / 08.10.2026',fontsize=9,color='#555555');fig.savefig(B/'vistas'/out,dpi=160);plt.close(fig)

if __name__=='__main__':
 for name in ['03_MODULO_D_duplex_propuesto','04_MODULO_S_una_planta','05_CONJUNTO_propuesto_32_40']:
  parts=json.loads((B/'trabajo'/(name+'.json')).read_text());t,c,n=triangles(parts);np.savez_compressed(B/'trabajo'/(name+'.npz'),tri=t,colors=c)
  if name.startswith('03'):
   draw(parts,'propuesta_D_exterior.png','D / EL CARACOL Y EL ALA','4,70 × 4,70 m · el ala superior se gira hacia el frente para poder repetir el módulo')
   draw(parts,'propuesta_D_interior.png','D / DOS ÁMBITOS PARA DORMIR','Desembarco separado de las camas · mesa junto a la ventana · espalda técnica',exclude=['05 ','06 ','07 ','08 '])
  elif name.startswith('04'):draw(parts,'propuesta_S_interior.png','S / UNA PLANTA, OTRA FORMA DE HABITAR','4,70 × 6,20 m · autonomía cotidiana · tipo sin escalera interior',exclude=['05 ','06 ','07 ','08 '])
  else:draw(parts,'propuesta_conjunto.png','LA CASA SE COMPARTE POR ESCALAS','24 unidades S + 8 unidades D / 40 residentes · galerías habitables · zócalo para el barrio',u=np.array([-.89,.46,0]),v=np.array([-.22,-.43,.875]))
