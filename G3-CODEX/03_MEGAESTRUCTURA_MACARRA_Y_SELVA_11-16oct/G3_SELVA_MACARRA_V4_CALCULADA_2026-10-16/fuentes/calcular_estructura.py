from pathlib import Path
import numpy as np, json, math
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from shapely.geometry import box,shape,Polygon
R=Path(__file__).resolve().parents[1]
site=shape(json.loads((Path(__file__).resolve().parent/'parcela_local.geojson').read_text())['geometry'])
E=210e6;G=81e6;FY=345000.;rho=77.0
bay=[{'x':23.4,'front':-1.8,'levels':[3.8,9.4,15.,20.6]}, {'x':36.,'front':-3.3,'levels':[6.6,12.2,17.8]}, {'x':48.6,'front':-4.4,'levels':[9.4,15.,20.6]}]
plates=[]
for b,bb in enumerate(bay):
 for k,z in enumerate(bb['levels']):
  # Alternating displacements create the zigzag without changing the room size.
  cx=bb['x']+[-.32,.35,-.18,.22][k];f=bb['front']+[.12,-.12,.08,-.08][k]
  body=box(cx-4.8,f,cx+4.8,f+6.8)
  assert body.difference(site).area<1e-7,(b,k)
  plate=box(cx-6.2+1.4,f-2.1+1.4,cx+6.2-1.4,f+6.95-1.4).buffer(1.4,quad_segs=16).intersection(site)
  plates.append({'id':'P%02d'%(len(plates)+1),'bay':b,'z':z,'cx':cx,'front':f,'outline':list(plate.exterior.coords),'area':plate.area,'body_area':body.area})

def section(D,t):
 d=D-2*t;A=math.pi*(D*D-d*d)/4;I=math.pi*(D**4-d**4)/64;return A,I,2*I,I/(D/2)
def klocal(L,A,I,J):
 k=np.zeros((12,12));a=E*A/L;k[0,0]=k[6,6]=a;k[0,6]=k[6,0]=-a
 a=G*J/L;k[3,3]=k[9,9]=a;k[3,9]=k[9,3]=-a
 for ids,sign in [([1,5,7,11],1),([2,4,8,10],-1)]:
  a=12*E*I/L**3;b=sign*6*E*I/L**2;c=4*E*I/L;d=2*E*I/L
  m=np.array([[a,b,-a,b],[b,c,-b,d],[-a,-b,a,-b],[b,d,-b,c]])
  k[np.ix_(ids,ids)]+=m
 return k
# Independent analytical engine checks.
A,I,J,W=section(.4,.016);L=5.;k=klocal(L,A,I,J);u=np.linalg.solve(k[6:,6:],np.array([0,0,-100,0,0,0.]));expected=100*L**3/(3*E*I)
assert abs(abs(u[2])/expected-1)<1e-8
ax=np.linalg.solve(k[6:,6:],np.array([100.,0,0,0,0,0]))[0];assert abs(ax/(100*L/(E*A))-1)<1e-8

class Frame:
 def __init__(self,scale=1.,braced=True,div=4):self.nodes=[];self.index={};self.el=[];self.fixed=[];self.P=[];self.scale=scale;self.div=div;self.build(braced)
 def node(self,p):
  key=tuple(round(float(x),7) for x in p)
  if key not in self.index:self.index[key]=len(self.nodes);self.nodes.append(list(key))
  return self.index[key]
 def member(self,a,b,D,t,kind):
  ia=self.node(a);ib=self.node(b)
  if ia!=ib:
   taper=1-.30*(a[2]+b[2])/48. if kind=='TRONCO' else 1.
   self.el.append({'i':ia,'j':ib,'D':D*self.scale*taper,'t':t*self.scale*taper,'kind':kind})
 def curve(self,a,c,b,D,t,kind):
  ps=[]
  for j in range(self.div+1):
   s=j/self.div;ps.append((1-s)**2*np.array(a)+2*s*(1-s)*np.array(c)+s*s*np.array(b))
  Lb=sum(np.linalg.norm(q-p) for p,q in zip(ps,ps[1:]))
  for p,q in zip(ps,ps[1:]):
   self.member(p,q,D,t,kind);self.el[-1]['Lb']=float(Lb)
 def build(self,braced):
  self.trunks={}
  for b,bb in enumerate(bay):
   zlev=[0]+[z-2.8 for z in bb['levels']]+[max(bb['levels'])+.4]
   for rear in [False,True]:
    y=bb['front']+(7.5 if rear else -1.8)
    pts=[]
    for z in zlev:
     x=bb['x']+.35*math.sin(z*.19)+(0 if rear else -.7)
     pts.append([x,y+.15*math.sin(z*.25),z]);self.trunks[(b,rear,round(z,5))]=pts[-1]
    self.fixed.append(self.node(pts[0]))
    for a,c in zip(pts,pts[1:]):
     # Curved primary trunk represented by matching short straight elements.
     mid=(np.array(a)+c)/2;mid[0]+=.12
     self.curve(a,mid,c,.7112,.025,'TRONCO')
  for p in plates:
   cx,f,z=p['cx'],p['front'],p['z'];top=z-.50
   grid=[]
   for rear in [False,True]:
    yy=f+(6.9 if rear else -.25)
    row=[]
    for dx in [-4.6,0,4.6]:row.append(self.node([cx+dx,yy,top]))
    grid.append(row)
    start=self.trunks[(p['bay'],rear,round(z-2.8,5))]
    for n in row:
     end=self.nodes[n];mid=(np.array(start)+end)/2;mid[2]-=.15
     self.curve(start,mid,end,.3556,.016,'RAMA')
   for row in grid:
    for i,j in zip(row,row[1:]):self.member(self.nodes[i],self.nodes[j],.3239,.016,'BORDE_EQUIVALENTE')
   for j in range(3):self.member(self.nodes[grid[0][j]],self.nodes[grid[1][j]],.4064,.020,'VIGA_BANDEJA')
   self.member(self.nodes[grid[0][0]],self.nodes[grid[1][2]],.2191,.010,'DIAGONAL_BANDEJA');self.member(self.nodes[grid[0][2]],self.nodes[grid[1][0]],.2191,.010,'DIAGONAL_BANDEJA')
   self.P.append((p,[i for row in grid for i in row]))
  if braced:
   # Back-side diagrid joins the trees outside the inhabited cells.
   for b in [0,1]:
    b1,b2=bay[b],bay[b+1]
    for k in range(3):
     zlo=0 if k==0 else 6.4*k;zhi=6.4*(k+1)
     def rear_at(b,z):
      keys=sorted([(zz,pt) for (bb,r,zz),pt in self.trunks.items() if bb==b and r])
      for (za,a),(zb,c) in zip(keys,keys[1:]):
       if za-1e-6<=z<=zb+1e-6:return (1-(z-za)/(zb-za))*np.array(a)+(z-za)/(zb-za)*np.array(c)
      return np.array(keys[-1][1])
     a=rear_at(b,zlo);c=rear_at(b,zhi);d=rear_at(b+1,zlo);e=rear_at(b+1,zhi)
     # Tie the new brace nodes into their parent trunks by splitting crossing members below.
     self.member(a,e,.2191,.010,'ARRIOSTRAMIENTO_TRASERO');self.member(c,d,.2191,.010,'ARRIOSTRAMIENTO_TRASERO')
   # Merge brace nodes into curved trunk elements within a 0.25 m distance.
   for n,p in enumerate(self.nodes):
    if n in {e['i'] for e in self.el if e['kind']=='ARRIOSTRAMIENTO_TRASERO'}|{e['j'] for e in self.el if e['kind']=='ARRIOSTRAMIENTO_TRASERO'}:
     cand=[j for j,q in enumerate(self.nodes) if j!=n and abs(q[0]-p[0])<1 and abs(q[1]-p[1])<.6 and abs(q[2]-p[2])<2]
     if cand:
      j=min(cand,key=lambda j:np.linalg.norm(np.array(self.nodes[j])-p));self.member(p,self.nodes[j],.3239,.016,'ENLACE_ARRIOSTRAMIENTO')
 def solve(self):
  N=len(self.nodes);nd=6*N;rows=[];cols=[];vals=[];Fg=np.zeros(nd);Fq=np.zeros(nd);Wx=np.zeros(nd);Wy=np.zeros(nd);mats=[]
  for el in self.el:
   a=np.array(self.nodes[el['i']]);b=np.array(self.nodes[el['j']]);v=b-a;L=np.linalg.norm(v);ex=v/L;ref=np.array([0.,0,1]) if abs(ex[2])<.9 else np.array([0.,1,0]);ey=np.cross(ref,ex);ey/=np.linalg.norm(ey);ez=np.cross(ex,ey);rr=np.vstack([ex,ey,ez]);tt=np.zeros((12,12))
   for j in [0,3,6,9]:tt[j:j+3,j:j+3]=rr
   A,I,J,W=section(el['D'],el['t']);kl=klocal(L,A,I,J);kg=tt.T@kl@tt;dofs=np.r_[np.arange(el['i']*6,el['i']*6+6),np.arange(el['j']*6,el['j']*6+6)]
   for i in range(12):
    for j in range(12):
     if abs(kg[i,j])>1e-12:rows.append(dofs[i]);cols.append(dofs[j]);vals.append(kg[i,j])
   weight=L*A*rho
   for n in [el['i'],el['j']]:Fg[n*6+2]-=weight/2
   mats.append((el,kl,tt,dofs,L,A,I,J,W))
  for p,ns in self.P:
   if p['id'] in ['P02','P05','P08']:Fg[ns[1]*6+2]-=2.5
   for n in ns:Fg[n*6+2]-=(6*.0100*7.15*77)/6
   # Entire outdoor+indoor plate conservatively takes q=5, rather than only the 2 kPa sleeping cells.
   for n in ns:
    Fg[6*n+2]-=3.6*p['area']/6;Fq[6*n+2]-=5.0*p['area']/6;Wx[6*n]+=1.0*6.8*4.3/6;Wy[6*n+1]+=1.0*9.6*4.3/6;Wx[6*n+4]+=1.0*6.8*4.3/6*2.15;Wy[6*n+3]-=1.0*9.6*4.3/6*2.15
  K=coo_matrix((vals,(rows,cols)),shape=(nd,nd)).tocsc();fixed=np.array([6*n+i for n in self.fixed for i in range(6)]);free=np.setdiff1d(np.arange(nd),fixed);kf=K[free,:][:,free]
  cases={'ELS_GQ':Fg+Fq,'ELS_GQ_WX':Fg+Fq+Wx,'ELS_GQ_WY':Fg+Fq+Wy,'ELU_GRAVEDAD':1.35*Fg+1.5*Fq,'ELU_WX':1.35*Fg+1.5*Wx+1.05*Fq,'ELU_WY':1.35*Fg+1.5*Wy+1.05*Fq,'ELS_GQ_WX_NEG':Fg+Fq-Wx,'ELS_GQ_WY_NEG':Fg+Fq-Wy,'ELU_WX_NEG':1.35*Fg-1.5*Wx+1.05*Fq,'ELU_WY_NEG':1.35*Fg-1.5*Wy+1.05*Fq,'ELU_Q_WX':1.35*Fg+1.5*Fq+.9*Wx,'ELU_Q_WX_NEG':1.35*Fg+1.5*Fq-.9*Wx,'ELU_Q_WY':1.35*Fg+1.5*Fq+.9*Wy,'ELU_Q_WY_NEG':1.35*Fg+1.5*Fq-.9*Wy}
  results={};env=np.zeros(len(self.el));worstforces=[];support=[]
  for name,load in cases.items():
   u=np.zeros(nd);u[free]=spsolve(kf,load[free]);react=K@u-load
   assert np.isfinite(u).all()
   force_error=max(abs(np.array([react[i::6].sum()+load[i::6].sum() for i in range(3)])))
   assert force_error<1e-4
   maxratio=0;forces=[]
   for ii,(el,kl,tt,dofs,L,A,I,J,W) in enumerate(mats):
    fl=kl@(tt@u[dofs]);Ncomp=max(0,fl[0],-fl[6]);Nc=max(abs(fl[0]),abs(fl[6]));M=max(np.linalg.norm(fl[4:6]),np.linalg.norm(fl[10:12]));stress=Nc/A+M/W
    Ncr=math.pi**2*E*I/el.get('Lb',L)**2;lam=math.sqrt(A*FY/Ncr);phi=.5*(1+.49*(lam-.2)+lam*lam);chi=min(1,1/(phi+math.sqrt(max(0,phi*phi-lam*lam))));Nb=chi*A*FY/1.05
    ratio=Ncomp/Nb+M/(W*FY/1.05)
    if name.startswith('ELU'):env[ii]=max(env[ii],ratio);maxratio=max(maxratio,ratio)
    forces.append({'N_kN':Nc,'M_kNm':M,'stress_MPa':stress/1000,'ratio_member_Euler_bending':ratio})
   disp=u.reshape(-1,6)[:,:3];sway=max(np.linalg.norm(disp[:,:2],axis=1));uz=max(abs(disp[:,2]))
   results[name]={'max_sway_mm':sway*1000,'max_vertical_mm':uz*1000,'max_member_ratio':maxratio,'force_balance_error_kN':force_error}
   if name=='ELU_GRAVEDAD':worstforces=forces;support=[{'node':int(n),'position':self.nodes[n],'Fx_Fy_Fz_kN':react[6*n:6*n+3].tolist(),'Mx_My_Mz_kNm':react[6*n+3:6*n+6].tolist()} for n in self.fixed]
  return {'cases':results,'nodes':self.nodes,'elements':[dict(el,utilization=float(env[i]),**worstforces[i]) for i,el in enumerate(self.el)],'reactions':support,'checks':{'cantilever_relative_error':abs(abs(expected)-abs(np.linalg.solve(k[6:,6:],np.array([0,0,-100,0,0,0.]))[2]))/expected,'axial_test':True},'loads':{'G_floor_kPa':3.6,'Q_all_plate_kPa':5.,'wind_test_kPa':1.,'self_weight_included':True},'material':{'E_kN_m2':E,'G_kN_m2':G,'fy_design_base_MPa':FY/1000,'density_kN_m3':rho},'section_scale':self.scale}

history=[];baseline=Frame(1,False).solve();answer=None
for sc in [1.,1.15,1.30,1.5,1.75,2.0]:
 ans=Frame(sc,True).solve();ratio=max(v['max_member_ratio'] for k,v in ans['cases'].items() if k.startswith('ELU'));sway=max(v['max_sway_mm'] for k,v in ans['cases'].items() if k.startswith('ELS'));vert=ans['cases']['ELS_GQ']['max_vertical_mm']
 history.append({'scale':sc,'max_ratio':ratio,'sway_mm':sway,'vertical_mm':vert});print(history[-1],flush=True)
 if ratio<.9 and sway<40 and vert<25:answer=ans;break
if answer is None:answer=ans
refined=Frame(answer['section_scale'],True,div=8).solve()
answer['convergence']={'segments_per_curve': [4,8], 'sway_mm_4':max(v['max_sway_mm'] for k,v in answer['cases'].items() if k.startswith('ELS')), 'sway_mm_8':max(v['max_sway_mm'] for k,v in refined['cases'].items() if k.startswith('ELS'))}
answer['iteration_history']=history;answer['unbraced_baseline']=baseline['cases'];answer['scope']='Linear elastic 3D beam frame; small straight segments represent curved CHS. Preliminary member Euler + linear bending screen only. Not a full stability, second-order, dynamic, connection, foundation, fire, or membrane verification.'
answer['plates']=plates;answer['bays']=bay
(R/'calculo/ESTRUCTURA_RESULTADOS.json').write_text(json.dumps(answer,indent=2))
print('BASELINE',baseline['cases']);print('FINAL',answer['cases'])
