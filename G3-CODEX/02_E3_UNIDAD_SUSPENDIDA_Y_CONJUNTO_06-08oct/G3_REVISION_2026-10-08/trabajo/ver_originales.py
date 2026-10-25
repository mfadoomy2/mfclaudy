import rhino3dm as r,numpy as np,pathlib,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
B=pathlib.Path('/Volumes/T7/G3 Proyectos/G3 CLAUDE/02_E3_UNIDAD_SUSPENDIDA_Y_CONJUNTO_06-08oct/G3_REVISION_2026-10-08')
def load(path,root,cut=False):
 f=r.File3dm.Read(path); layers={l.Index:l for l in f.Layers}; tris=[];cols=[]
 for o in f.Objects:
  l=layers[o.Attributes.LayerIndex];g=o.Geometry
  if root not in l.FullPath or not isinstance(g,r.Mesh):continue
  if not l.Visible or 'posición abierta' in l.Name or 'Contexto' in l.Name:continue
  if cut and any(s in l.Name for s in ['Bloque','Mortero','Perfil U','Cubierta','Aislamiento','Agua de lluvia','Vidrio de carpinterías']):continue
  vs=np.array([[p.X,p.Y,p.Z] for p in g.Vertices]); faces=np.array([list(g.Faces[i]) for i in range(len(g.Faces))]);ts=[vs[faces[:,:3]]];q=faces[:,2]!=faces[:,3]
  if q.any():ts.append(vs[faces[q][:,[0,2,3]]])
  ts=np.concatenate(ts);tris.append(ts)
  c=np.array(l.Color[:3])/255
  if o.Attributes.ColorSource==r.ObjectColorSource.ColorFromObject:c=np.array(o.Attributes.ObjectColor[:3])/255
  cols.extend([c]*len(ts))
 return np.concatenate(tris),np.array(cols)
def draw(t,c,path,title,u=None,v=None):
 if u is None:u=np.array([.84,-.54,0]);v=np.array([.32,.50,.80])
 d=np.cross(u,v);norm=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-10);lit=.58+.42*np.abs(norm@np.array([.3,-.5,.812]))
 c=np.clip(c*lit[:,None],0,1);order=np.argsort(t.mean(axis=1)@d);xy=np.stack([t@u,t@v],axis=-1)
 fig,ax=plt.subplots(figsize=(12,10));ax.add_collection(PolyCollection(xy[order],facecolors=c[order],edgecolors='none',rasterized=True));ax.autoscale();ax.set_aspect('equal');ax.axis('off');ax.set_title(title,loc='left',fontsize=16,pad=25);fig.tight_layout();fig.savefig(path,dpi=155);plt.close(fig)
for cut in [False,True]:
 t,c=load('/Users/adam/Downloads/G3_unidad_suspendida_7.3dm','Fuera del cubo 2',cut);t[:,:,0]-=72;draw(t,c,B/'vistas'/('original_F2_'+('interior' if cut else 'exterior')+'.png'),'ORIGINAL APORTADO · F2 · '+('INTERIOR SIN PIEL' if cut else 'EXTERIOR'))
for root in ['B · Peine','G · Muro']:
 t,c=load('/Users/adam/Downloads/G3_conjunto_opciones_1.3dm',root);draw(t,c,B/'vistas'/('original_'+root[0]+'.png'),'ORIGINAL APORTADO · '+root,u=np.array([.86,-.51,0]),v=np.array([.28,.47,.84]))
