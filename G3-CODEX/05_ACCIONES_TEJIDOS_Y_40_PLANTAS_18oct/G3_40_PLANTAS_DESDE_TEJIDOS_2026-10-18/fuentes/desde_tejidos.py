from base_geometrica import *
import pickle,heapq
P=Path(__file__).resolve().parents[1]
SOURCE=json.loads((P/'datos/FUENTE_RESULTADOS.json').read_text());RELS=json.loads((P/'datos/FUENTE_RELACIONES.json').read_text())
IDS=[f'A{i:02}' for i in range(1,21)]
NAMES=['Llegada y cuidado','Trabajo persistente','Encuentro voluntario','Retorno mojado','Conversación y retiro','Carga y descarga','Coser y guardar','Comer a deshora','Acuerdo de privacidad','Trabajo y visita','Herramientas próximas','Humedad separada','Mesa desplegada','Visita discreta','Estar sin cocinar','Dibujar sin recoger','Limpieza accesible','Cambio de turno','Dos ritmos domésticos','Umbral y retirada']

def make(fi,v):
 src=SOURCE[fi%3];ids=IDS;pp=np.array([src['positions'][i] for i in ids],float);pp-=pp.mean(axis=0)
 # Continuous non-uniform deformation of the source grid. No imported architectural silhouette.
 stretch=[(.85,1),(1,.85),(1.1,.8),(.8,1.1),(1,1),(1.05,.9),(1.1,1)][fi//3]
 pp*=np.array(stretch)*.72
 group=[[2,3,4],[10,11,12,13],[7,8],[15,16,17],[5,9]][fi%5]
 center=pp[group].mean(axis=0)
 for j in group:pp[j]=center+(pp[j]-center)*(1.2 if not v else .8)
 if v:
  # B tests a different spatial strain, without rotating the entire drawing.
  pp[:,0]+=pp[:,1]*.16;pp[:,1]*=.94
 apos={id:Point(*p) for id,p in zip(ids,pp)}
 root=pp[0];out=root-pp.mean(axis=0);out/=np.linalg.norm(out)
 baseangle=math.atan2(out[1],out[0]);spread=78+fi%4*6
 for rad in np.arange(2.1,9.01,.35):
  rooms=[]
  for j,a in enumerate(np.linspace(-spread,spread,4)):
   th=baseangle+math.radians(a);vec=np.array([math.cos(th),math.sin(th)]);door=root+vec*rad;ang=math.degrees(th)-90
   rooms.append(private('H'+str(j+1),tuple(door),ang,'A' if not v else 'B',fi))
  if all(rooms[i]['poly'].buffer(.15).intersection(rooms[j]['poly'].buffer(.15)).area<.005 for i in range(4) for j in range(i)):break
 else:raise ValueError('private overlap')
 # PROTECT links become conflicts to resolve, never corridors. All other links are kept as source annotations.
 segs=[]
 for rel in RELS:
  if rel['tipo']=='PROXIMIDAD':segs.append(LineString([apos[rel['a']],apos[rel['b']]]))
 # Access continuity added by minimum-spanning links among action points; source and additions distinguishable.
 used={15};remaining=set(range(20))-used;add=[]
 while remaining:
  _,i,j=min((np.linalg.norm(pp[i]-pp[j]),i,j) for i in used for j in remaining)
  add.append(LineString([pp[i],pp[j]]));remaining.remove(j);used.add(j)
 private_union=unary_union([r['poly'] for r in rooms]);doorpaths=[]
 for room in rooms:
  door=Point(room['door']);doorpaths.append(LineString([door,apos['A01']]))
 network=unary_union(segs+add+doorpaths)
 # Square-ended buffers translate branches to inhabitable strips, avoiding circular blob envelopes.
 items=None
 for width in [1.25,1.5,1.75,2,2.25,2.5,2.8,3.1,3.5,4]:
  core=network.buffer(width,cap_style=2,join_style=2)
  core=core.union(unary_union([p.buffer(width,cap_style=3) for p in apos.values()]))
  shared=core.difference(private_union)
  reserved=reserve_routes(shared,rooms)
  if reserved is None:continue
  targets={'B1':tuple(pp[2]),'B2':tuple(pp[2]+[1.6,0]),'K':tuple(pp[6]),'F':tuple(pp[6]+[.5,0]),'M':tuple(pp[7]),'S':tuple(pp[8]),'G':tuple(pp[19])}
  items=choose_pack(shared,targets,fi*2+v+100,reserved)
  if items:break
 if not items:raise ValueError(('pack fail',fi,v))
 floor=shared.union(private_union);free=shared.difference(unary_union([i['poly'] for i in items]));walk=free.buffer(-.45)
 entries=[]
 for rr in rooms:
  a=math.radians(rr['angle']);d=rr['door'];entries.append(Point(d[0]+math.sin(a)*.8,d[1]-math.cos(a)*.8))
 joined=max([sum(c.distance(q)<.35 for q in entries) for c in polygons(walk)]+[0])
 # Source arrival retained as target; snap to actual exterior shared boundary, never inside a bedroom.
 peri=floor.boundary.intersection(shared.boundary.buffer(.02));ob=unary_union([i['poly'] for i in items]);qs=[]
 for t in np.linspace(0,peri.length-.001,400):
  q=peri.interpolate(float(t))
  if q.distance(private_union)>.7 and q.distance(ob)>1:qs.append(q)
 if not qs:raise ValueError('no external entry')
 arrival=min(qs,key=lambda q:q.distance(apos['A16']))
 conflicts=[]
 for rr in rooms:
  for a,b in [('bed','desk'),('bed','ward'),('desk','ward'),('chair','bed')]:
   if rr[a].intersection(rr[b]).area>.002:conflicts.append(rr['id']+' '+a+'/'+b)
 err={it['name']:round(it['poly'].centroid.distance(Point(targets[it['name']])),2) for it in items}
 return dict(code=f'T{fi+1:02}{"AB"[v]}',family=NAMES[fi],logic='Traslación del tejido '+str(src['alternative'])+'; ' +NAMES[fi].lower()+'.',risk='La traducción desplaza equipamiento y amplía el nodo dormir: consultar las distancias al objetivo.',variant='AB'[v],rooms=rooms,shared=shared,floor=floor,items=items,arrival=arrival,entries=entries,holes=[],walk=walk,connections=joined,reserved=reserved,geometry_conflicts=conflicts,entry_on_boundary=True,radius=width,source=src['alternative'],action_positions=apos,source_positions=src['positions'],near_links=segs,added_links=add,network=network,targets=targets,target_error=err,room_expansion=rad,stretch=stretch)

def draw_source(d,path):
 fig,axes=plt.subplots(1,2,figsize=(15,9));fig.patch.set_facecolor(BG)
 for ax in axes:ax.set_aspect('equal');ax.axis('off');ax.set_facecolor(BG)
 for k,ax in enumerate(axes):
  pos={id:Point(*d['source_positions'][id]) for id in IDS} if k==0 else d['action_positions']
  if k:
   drawpoly(ax,d['shared'],'#eee7d2',INK,.6);drawpoly(ax,d['floor'].difference(d['shared']),ROOM,INK,.8)
   for lineg in d['added_links']:line(ax,list(lineg.coords),'#8e9992',.6,ls='--')
  for rel in RELS:
   a,b=pos[rel['a']],pos[rel['b']];t=rel['tipo']
   line(ax,[(a.x,a.y),(b.x,b.y)],CYAN if t=='PROXIMIDAD' else PINK if t=='PROTEGER' else GOLD,.9 if t=='PROXIMIDAD' else .5,ls='-' if t in ['PROXIMIDAD','PROTEGER'] else '--')
  for id,p in pos.items():
   ax.scatter(p.x,p.y,s=120 if not k else 65,facecolor=BG,edgecolor=INK,lw=.6,zorder=10);label(ax,id[1:],p.x,p.y,7 if not k else 6)
  ax.set_title('TEJIDO '+str(d['source'])+' / sin metros' if not k else 'TRADUCCIÓN / suelo y nodos de actividad',loc='left',fontsize=12,color=INK)
 fig.tight_layout();fig.savefig(path,dpi=150,bbox_inches='tight',facecolor=BG);fig.savefig(path.with_suffix('.svg'),bbox_inches='tight',facecolor=BG);plt.close(fig)

allplans=[];reports=[]
for fi in range(20):
 for v in range(2):
  d=make(fi,v);allplans.append(d);plotplan(d,P/'plantas'/f'{d["code"]}_PLANTA.png');draw_source(d,P/'plantas'/f'{d["code"]}_TRAZA.png')
  r={k:d[k] for k in ['code','family','variant','logic','risk','source','target_error','connections','geometry_conflicts','stretch','room_expansion']};r.update(floor_m2=round(d['floor'].area,2),bedrooms_m2=round(sum(rr['poly'].area for rr in d['rooms']),2),shared_gross_m2=round(d['shared'].area,2),entry_on_boundary=True)
  reports.append(r);(P/'datos'/f'{d["code"]}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(d['code'],r['floor_m2'],d['connections'],d['source'],flush=True)
 with open(P/'datos/geometrias.pkl','wb') as f:pickle.dump(allplans,f)
 (P/'datos/RESUMEN_40.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
print('40_NUEVAS_DERIVADAS',flush=True)
