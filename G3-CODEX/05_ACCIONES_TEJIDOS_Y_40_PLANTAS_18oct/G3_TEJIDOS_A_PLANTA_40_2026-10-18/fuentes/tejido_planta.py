from base_geometrica import *
import pickle,heapq
P=Path(__file__).resolve().parents[1]
SRC=json.loads((P/'datos/FUENTE_RESULTADOS.json').read_text());REL=json.loads((P/'datos/FUENTE_RELACIONES.json').read_text())
IDS=[f'A{i:02}' for i in range(1,21)]
TITLES=['Descanso y trabajo','Cocina y comedor','Tareas y herramientas','Llegada con carga','Voces y privacidad','Ropa y humedad','Visita y recogida','Trabajo que permanece','Reparación en el umbral','Comer sin reunirse','Cuidados próximos','Dos ritmos de trabajo','Secar sin invadir','Coser y cortar','Retirarse sin cruzar','Entrada y conversación','Limpieza y almacenaje','Noche y actividad','Cuatro retiros dispersos','Cruces habitables']

def solve(target,wh,seed):
 rng=np.random.default_rng(seed);p=target.copy()+rng.normal(0,.14,target.shape)
 # Preserve diagram anchors elastically; only displace footprints to remove collisions.
 for it in range(1800):
  if it<1200:p+=(target-p)*.003
  pairs=[(i,j) for i in range(len(p)) for j in range(i)];rng.shuffle(pairs)
  for i,j in pairs:
   delta=p[i]-p[j];need=(wh[i]+wh[j])/2+2.0;over=need-np.abs(delta)
   if min(over)>0:
    ax=int(np.argmin(over));sign=1 if delta[ax]>0 else -1
    if abs(delta[ax])<1e-6:sign=rng.choice([-1,1])
    shift=sign*(over[ax]+.002)*.501;p[i,ax]+=shift;p[j,ax]-=shift
 # Final exact separation audit
 for i in range(len(p)):
  for j in range(i):
   assert min((wh[i]+wh[j])/2-np.abs(p[i]-p[j]))<.002,(i,j)
 return p

def astar(a,b,obstacles,bounds):
 from shapely import contains_xy
 step=.27;x0,y0,x1,y1=bounds;xs=np.arange(x0,x1+step,step);ys=np.arange(y0,y1+step,step);xx,yy=np.meshgrid(xs,ys)
 mask=~contains_xy(obstacles,xx,yy)
 def ij(q):return (round((q[1]-y0)/step),round((q[0]-x0)/step))
 start,end=ij(a),ij(b)
 # keep endpoints safe; exact approaches checked against solid footprints elsewhere
 for i,j in [start,end]:mask[i,j]=True
 queue=[(0,start)];dist={start:0};prev={start:None}
 while queue:
  _,u=heapq.heappop(queue)
  if u==end:break
  i,j=u
  for di,dj in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
   ni,nj=i+di,j+dj
   if ni<0 or nj<0 or ni>=len(ys) or nj>=len(xs) or not mask[ni,nj]:continue
   if di and dj and (not mask[i,nj] or not mask[ni,j]):continue
   v=(ni,nj);nd=dist[u]+math.hypot(di,dj)
   if nd<dist.get(v,1e12):dist[v]=nd;prev[v]=u;heapq.heappush(queue,(nd+math.hypot(ni-end[0],nj-end[1]),v))
 if end not in prev:raise ValueError('route blocked')
 pts=[b];u=end
 while u is not None:pts.append((float(xs[u[1]]),float(ys[u[0]])));u=prev[u]
 pts.append(a);return LineString(pts[::-1]).simplify(.05)

def make(fi,v):
 source=SRC[fi%3];orig=np.array([source['positions'][i] for i in IDS],float);orig-=orig.mean(axis=0)
 # Original shape retained as the anchor field; six controlled strains generate 20 tests.
 gx=[.95,1.05,.9,1.15,1,1.1,.85][fi//3];gy=[1.05,.9,1.1,.85,1,.95,1.15][fi//3]
 anchors=orig*np.array([gx,gy])*.94
 if v:anchors[:,0]+=anchors[:,1]*.10
 # A single action can have several loci. Four private spaces begin at four low-voice/work nodes.
 h_idx=[0,5,9,10];specs=[];templates=[]
 for j,k in enumerate(h_idx):
  outward=anchors[k]-anchors.mean(axis=0);theta=math.degrees(math.atan2(outward[1],outward[0]))-90
  angle=round(theta/90)*90 if fi%4!=3 else round(theta/45)*45
  rr=private('H'+str(j+1),(0,0),angle,'A' if not v else 'B',fi);bb=rr['poly'].bounds;wh=(bb[2]-bb[0],bb[3]-bb[1]);templates.append((angle,(bb[0]+bb[2])/2,(bb[1]+bb[3])/2));specs.append(('H'+str(j+1),anchors[k],wh))
 for code,indices,size in [('K',[6],(4.1,2.2)),('M',[7],(3.1,2.8)),('S',[8],(3.6,3.1)),('B1',[2],(2.1,2.4)),('B2',[2],(2.1,2.4)),('D',[3],(2.4,1.5)),('T',[12,13],(3.,2.6)),('R',[14,19],(2.6,2.4)),('E',[15,16,17],(2.2,2.2))]:
  q=anchors[indices].mean(axis=0)
  if code=='B2':q=q+np.array([2.1,0])
  if v and code in ['S','M','T']:size=size[::-1]
  specs.append((code,q,size))
 targets=np.array([q[1] for q in specs]);wh=np.array([q[2] for q in specs]);pos=solve(targets,wh,180+fi*2+v)
 zones={code:box(*(list(p-whh/2)+list(p+whh/2))) for (code,_,_),p,whh in zip(specs,pos,wh)}
 rooms=[]
 for j,(angle,cx,cy) in enumerate(templates):rooms.append(private('H'+str(j+1),(pos[j,0]-cx,pos[j,1]-cy),angle,'A' if not v else 'B',fi))
 # Fixed equipment uses its own activity cell; no global packing moves a kitchen to an unrelated node.
 items=[]
 def item(name,g,rot=0):
  a,b,c,d=g.bounds;items.append(dict(name=name,poly=g,approach=g,angle=rot,x=a,y=b,w=c-a,h=d-b))
 for code in ['B1','B2']:item(code,zones[code])
 x,y,X,Y=zones['K'].bounds;item('K',box(x+.15,Y-.85,x+3.75,Y-.15));item('F',box(X-.85,y+.1,X-.15,y+.8))
 x,y,X,Y=zones['M'].bounds;item('M',box((x+X)/2-.9,(y+Y)/2-.45,(x+X)/2+.9,(y+Y)/2+.45))
 x,y,X,Y=zones['S'].bounds;item('S',box(x+.35,Y-1.1,x+2.75,Y-.25))
 x,y,X,Y=zones['R'].bounds;item('G',box(x+.1,Y-.6,x+1.5,Y-.1))
 # Common task furniture is explicit; these are not additional enclosed rooms.
 x,y,X,Y=zones['T'].bounds;task=box(x+.4,Y-1.1,x+2.6,Y-.3)
 x,y,X,Y=zones['D'].bounds;dry=box(x+.25,Y-.7,X-.25,Y-.25)
 private_union=unary_union([r['poly'] for r in rooms]);baths=unary_union([zones['B1'],zones['B2']]);solids=unary_union([private_union,baths]+[it['poly'] for it in items if not it['name'].startswith('B')]+[task,dry])
 access={}
 for r in rooms:
  a=math.radians(r['angle']);access[r['id']]=(r['door'][0]+math.sin(a)*.9,r['door'][1]-math.cos(a)*.9)
 for code in ['B1','B2']:
  x,y,X,Y=zones[code].bounds;access[code]=(x+1.05,y-.9)
 for code in ['K','M','S','D','T','R','E']:
  x,y,X,Y=zones[code].bounds;access[code]=((x+X)/2,y-.9)
 # Explicit functional edges then minimum extra connections; PROTEGER edges are not routes.
 edges=[('K','M'),('B1','D'),('B2','D'),('T','R'),('E','R'),('E','S')]
 codes=list(access);used={codes[0]};remaining=set(codes[1:]);extra=[]
 while remaining:
  _,a,b=min((math.dist(access[a],access[b]),a,b) for a in used for b in remaining);extra.append((a,b));used.add(b);remaining.remove(b)
 edges=list(dict.fromkeys(tuple(sorted(e)) for e in edges+extra))
 total=unary_union(list(zones.values()));x,y,X,Y=total.bounds;bounds=(x-3,y-3,X+3,Y+3);obstacles=solids.buffer(.72,join_style=2);routes=[]
 for a,b in edges:
  routes.append(astar(access[a],access[b],obstacles,bounds))
 net=unary_union([g.buffer(.60,cap_style=1,join_style=2) for g in routes])
 # Door vestibules actually reach private and wet thresholds.
 vestibules=[]
 for rr in rooms:
  a=math.radians(rr['angle']);end=(rr['door'][0]-math.sin(a)*.15,rr['door'][1]+math.cos(a)*.15);vestibules.append(LineString([access[rr['id']],end]).buffer(.6,cap_style=2))
 for code in ['B1','B2']:
  x,y,X,Y=zones[code].bounds;vestibules.append(LineString([access[code],(x+1.05,y)]).buffer(.6,cap_style=2))
 for code in ['K','M','S','D','T','R','E']:
  x,y,X,Y=zones[code].bounds;vestibules.append(LineString([access[code],((x+X)/2,y)]).buffer(.6,cap_style=1))
 floor=unary_union(list(zones.values())+[r['poly'] for r in rooms]+[net]+vestibules)
 # Remove unused bounding-box corners around private outlines.
 common=unary_union([g for k,g in zones.items() if not k.startswith('H')]+[net]+vestibules).difference(private_union)
 floor=unary_union([g for k,g in zones.items() if not k.startswith('H')]+[private_union,net]+vestibules);free=common.difference(unary_union([it['poly'] for it in items]+[task,dry]));walk=free.buffer(-.44)
 entries=[Point(access['H'+str(i)]) for i in range(1,5)];joined=max([sum(c.distance(q)<.35 for q in entries) for c in polygons(walk)]+[0])
 ec=zones['E'].centroid;perimeter=floor.boundary.intersection(common.boundary.buffer(.01));candidates=[]
 for t in np.linspace(0,perimeter.length-.001,500):
  q=perimeter.interpolate(float(t))
  if q.distance(private_union)>.7 and q.distance(solids)>1:candidates.append(q)
 arrival=min(candidates,key=lambda p:p.distance(ec)) if candidates else nearest_points(ec,floor.boundary)[1]
 conflicts=[]
 for rr in rooms:
  for key in ['bed','desk','chair','ward']:
   if rr[key].difference(rr['poly']).area>.02:conflicts.append(rr['id']+' '+key+' fuera')
  for aa,bb in [('bed','desk'),('bed','ward'),('desk','ward'),('chair','bed')]:
   if rr[aa].intersection(rr[bb]).area>.002:conflicts.append(rr['id']+' '+aa+'/'+bb)

 # map each action to actual loci; one-to-many for private activities is explicitly retained
 amap={'A01':[r['poly'].centroid for r in rooms],'A02':[r['ward'].centroid for r in rooms],'A03':[zones['B1'].centroid,zones['B2'].centroid],'A04':[dry.centroid],'A05':[r['ward'].centroid for r in rooms],'A06':[r['desk'].centroid for r in rooms],'A07':[items[2]['poly'].centroid],'A08':[zones['M'].centroid],'A09':[zones['S'].centroid],'A10':[r['poly'].centroid for r in rooms],'A11':[r['desk'].centroid for r in rooms],'A12':[zones['T'].centroid],'A13':[task.centroid],'A14':[task.centroid],'A15':[zones['R'].centroid],'A16':[zones['E'].centroid],'A17':[zones['E'].centroid],'A18':[zones['E'].centroid],'A19':[zones['K'].centroid],'A20':[zones['R'].centroid]}
 return dict(code=f'N{fi+1:02}{"AB"[v]}',family=TITLES[fi],logic='Tejido '+str(source['alternative'])+' traducido mediante huellas de uso y rutas; desplazamientos locales para evitar solapes.',risk='Revisar distancia de conexiones, privacidad y luz en la parcela.',variant='AB'[v],rooms=rooms,shared=common,floor=floor,items=items,arrival=arrival,entries=entries,holes=[],walk=walk,connections=joined,reserved=net.intersection(common),geometry_conflicts=conflicts,entry_on_boundary=arrival.distance(floor.boundary)<.05,radius=0,source=source['alternative'],original_positions=source['positions'],anchors=anchors,zones=zones,task=task,dry=dry,routes=routes,edges=edges,action_map=amap,displacements={q[0]:round(float(np.linalg.norm(p-t)),2) for q,p,t in zip(specs,pos,targets)},positions=pos,targets=targets)

def draw(d):
 path=P/'plantas'/f'{d["code"]}_PLANTA.png';plotplan(d,path)
 # Add missing task / drying objects, activity labels and equipment on an alternative explicit program overlay.
 fig,ax=plt.subplots(figsize=(12,10));fig.patch.set_facecolor(BG);ax.set_aspect('equal');ax.axis('off')
 drawpoly(ax,d['floor'],'#eee7d2',INK,1)
 for rr in d['rooms']:drawpoly(ax,rr['poly'],ROOM,INK,1)
 for code,g in d['zones'].items():
  if code.startswith('H'):continue
  drawpoly(ax,g,'none',CYAN,.6);c=g.centroid;label(ax,code,c.x,c.y,10)
 for route in d['routes']:line(ax,list(route.coords),CYAN,.6,ls='--')
 for it in d['items']:drawpoly(ax,it['poly'],WET if it['name'].startswith('B') else '#a4c4b5',INK,.5)
 drawpoly(ax,d['task'],WOOD,INK,.5);drawpoly(ax,d['dry'],'none',PINK,.8)
 for code,points in d['action_map'].items():
  p=points[0];label(ax,code,p.x,p.y,7,PINK)
 x,y,X,Y=d['floor'].bounds;ax.set_xlim(x-1,X+1);ax.set_ylim(y-1,Y+1);fig.savefig(P/'plantas'/f'{d["code"]}_PROGRAMA.png',dpi=145,bbox_inches='tight',facecolor=BG);plt.close(fig)

def sourceplot(d):
 fig,axes=plt.subplots(1,2,figsize=(15,9));fig.patch.set_facecolor(BG)
 for k,ax in enumerate(axes):
  ax.axis('off');ax.set_aspect('equal');ax.set_facecolor(BG)
  if not k:
   pp={id:Point(*d['original_positions'][id]) for id in IDS}
   for r in REL:
    a,b=pp[r['a']],pp[r['b']];t=r['tipo'];line(ax,[(a.x,a.y),(b.x,b.y)],CYAN if t=='PROXIMIDAD' else PINK if t=='PROTEGER' else GOLD,.8,ls='-' if t in ['PROXIMIDAD','PROTEGER'] else '--')
   for id,p in pp.items():ax.scatter(p.x,p.y,s=90,fc=BG,ec=INK,zorder=5);label(ax,id[1:],p.x,p.y,7)
  else:
   drawpoly(ax,d['floor'],'#eee7d2',INK,.5)
   for rr in d['rooms']:drawpoly(ax,rr['poly'],ROOM,INK,.5)
   for route in d['routes']:line(ax,list(route.coords),CYAN,.8)
   for i,(target,pos) in enumerate(zip(d['targets'],d['positions'])):
    line(ax,[tuple(target),tuple(pos)],PINK,.7,ls='--');ax.scatter(*target,s=12,c=PINK);label(ax,list(d['zones'])[i],*pos,8)
  ax.set_title('TEJIDO '+str(d['source'])+' / acciones, sin metros' if not k else 'TRADUCCIÓN / puntos rosa: anclajes previos al ajuste',loc='left',color=INK,fontsize=11)
 fig.tight_layout();fig.savefig(P/'plantas'/f'{d["code"]}_TRAZA.png',dpi=145,bbox_inches='tight',facecolor=BG);fig.savefig(P/'plantas'/f'{d["code"]}_TRAZA.svg',bbox_inches='tight',facecolor=BG);plt.close(fig)

plans=[];reports=[]
for fi in range(20):
 for v in range(2):
  d=make(fi,v);plans.append(d);draw(d);sourceplot(d)
  r={k:d[k] for k in ['code','family','logic','risk','variant','source','connections','geometry_conflicts','entry_on_boundary','displacements','edges']};r.update(floor_m2=round(d['floor'].area,2),bedrooms_m2=round(sum(r['poly'].area for r in d['rooms']),2),shared_gross_m2=round(d['shared'].area,2));reports.append(r)
  (P/'datos'/f'{d["code"]}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(d['code'],r['floor_m2'],d['connections'],'/4',flush=True)
 with open(P/'datos/geometrias.pkl','wb') as f:pickle.dump(plans,f)
 (P/'datos/RESUMEN_40.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
print('40_NUEVAS_COMPLETAS',flush=True)
