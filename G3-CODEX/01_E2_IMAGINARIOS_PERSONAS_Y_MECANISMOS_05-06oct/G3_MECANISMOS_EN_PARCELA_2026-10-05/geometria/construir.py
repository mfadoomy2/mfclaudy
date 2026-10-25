from pathlib import Path
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
from shapely.geometry import shape, Polygon, box
from shapely.ops import unary_union
ROOT=Path(__file__).resolve().parents[1]
DATA=Path('/Volumes/T7/G3 Proyectos/INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/DATOS/DERIVADOS/parcela_31.geojson')
j=json.loads(DATA.read_text()); p=shape(j['features'][0]['geometry']); xy=np.array(p.exterior.coords)-[439984,4473229.4]; site=Polygon(xy)
(ROOT/'geometria/parcela_local.geojson').write_text(json.dumps({'type':'Feature','properties':{'origin_utm':[439984,4473229.4],'crs_source':'EPSG:25830','z0':622.6},'geometry':{'type':'Polygon','coordinates':[xy.tolist()]}},indent=2))
source=Path('/Users/adam/Downloads/01.Centro_3D/_MAQUETA_RASTRO/CENTRO_MADRID_8291_edificios_coord-locales.obj')
cache=ROOT/'geometria/contexto.npz'
if not cache.exists():
    verts=[]; faces=[]; obj=''; offset=0; kept=[]; allcount=0
    def flush():
        global allcount
        if not verts:return
        v=np.array(verts); f=np.array(faces,dtype=int)-offset-1
        if obj not in ['40028001','150237'] and v[:,0].max()>-32 and v[:,0].min()<100 and v[:,1].max()>-48 and v[:,1].min()<55:
            if np.ptp(v[:,0])<150 and np.ptp(v[:,1])<150:
                kept.append((obj,v,f))
        allcount+=len(v)
    with source.open() as h:
        for line in h:
            if line.startswith('o '):
                flush(); verts=[];faces=[];offset=allcount;obj=line.strip()[2:]
            elif line.startswith('v '):verts.append(list(map(float,line.split()[1:4])))
            elif line.startswith('f '):
                fi=[int(s.split('/')[0]) for s in line.split()[1:]]
                for i in range(1,len(fi)-1):faces.append([fi[0],fi[i],fi[i+1]])
        flush()
    tri=[]; ids=[]
    for name,v,f in kept:
        v[:,2]-=622.6
        for t in v[f]:tri.append(t);ids.append(name)
    np.savez_compressed(cache,tri=np.array(tri),ids=ids)
    print('buildings',len(kept),'triangles',len(tri))
dat=np.load(cache); tri=dat['tri']; ids=dat['ids']
# Exact plan footprints extracted from the original triangle meshes.
foot=[]
for name in sorted(set(ids)):
    pts=tri[ids==name]
    polys=[Polygon(t[:,:2]) for t in pts if Polygon(t[:,:2]).area>.015]
    if polys:foot.append((name,unary_union(polys)))
BG='#dedbd4'; INK='#292b2b'; RED='#ae352e'
def polygons(g):
    return [g] if g.geom_type=='Polygon' else [p for p in g.geoms if p.geom_type=='Polygon']
def plan():
    fig,ax=plt.subplots(figsize=(15,10),facecolor=BG);ax.set_facecolor(BG)
    for name,g in foot:
        for q in polygons(g):
            a=np.array(q.exterior.coords);ax.fill(a[:,0],a[:,1],facecolor='#999a96',edgecolor='#464b49',lw=.45)
            for ring in q.interiors:
                a=np.array(ring.coords);ax.fill(a[:,0],a[:,1],facecolor=BG,edgecolor=INK,lw=.3)
    ax.fill(xy[:,0],xy[:,1],facecolor='#c17865',edgecolor=RED,lw=2)
    ax.text(34,-.5,'RIBERA 31\nPARCELA REAL',ha='center',va='center',fontsize=12,fontfamily='monospace',weight='bold')
    ax.text(3,10,'RIBERA DE CURTIDORES',rotation=86,fontsize=10,ha='center')
    ax.annotate('N',xy=(76,29),xytext=(76,19),arrowprops=dict(arrowstyle='->',lw=1),ha='center')
    ax.plot([-14,-4],[ -28,-28],c=INK,lw=3);ax.text(-9,-31,'10 m',ha='center',fontsize=10)
    ax.set(xlim=(-24,90),ylim=(-37,45),aspect='equal');ax.axis('off')
    fig.text(.045,.93,'01   EL HUECO QUE EXISTE',fontsize=19,fontfamily='monospace')
    fig.text(.045,.045,'Catastro + malla urbana original · planta en metros · nave 40028001 retirada en la hipótesis de solar libre',fontsize=10)
    fig.savefig(ROOT/'01_parcela_real.png',dpi=180,facecolor=BG);fig.savefig(ROOT/'geometria/01_parcela_real.svg',facecolor=BG);plt.close(fig)
# fixed projection, looking from north-west; near context kept wireframe so the plot remains legible.
U=np.array([.88,.48,0]); V=np.array([-.28,.51,.81]); D=np.cross(U,V)
def project(a):return np.stack([a@U,a@V],axis=-1)
def draw(name,parts=[],frames=False):
    fig,ax=plt.subplots(figsize=(15,10),facecolor=BG);ax.set_facecolor(BG)
    # cropped urban envelope in unmodified original coordinates
    select=tri[(np.mean(tri[:,:,0],axis=1)>-20)&(np.mean(tri[:,:,0],axis=1)<90)&(np.mean(tri[:,:,1],axis=1)>-32)&(np.mean(tri[:,:,1],axis=1)<37)]
    proj=project(select); order=np.argsort(np.sum(select.mean(axis=1)*D,axis=1))
    ax.add_collection(PolyCollection(proj[order],facecolors='#b9bab5',edgecolors='#737b78',linewidths=.12,alpha=.34))
    ground=np.c_[xy,np.zeros(len(xy))];ax.fill(*project(ground).T,color='#ad5347',alpha=.6);ax.plot(*project(ground).T,c=RED,lw=1.5)
    faces=[];colors=[]; paths=[]
    for geom,z0,z1,color in parts:
        for poly in polygons(geom):
            p=np.array(poly.exterior.coords)[:-1]
            bottom=np.c_[p,np.full(len(p),z0)];top=np.c_[p,np.full(len(p),z1)]
            faces.extend([bottom,top]);colors.extend([color,color])
            for k in range(len(p)):
                faces.append(np.array([bottom[k],bottom[(k+1)%len(p)],top[(k+1)%len(p)],top[k]]));colors.append(color)
            paths.extend([bottom,top])
    if faces:
        order=sorted(range(len(faces)),key=lambda i:np.mean(faces[i],axis=0)@D)
        ax.add_collection(PolyCollection([project(faces[i]) for i in order],facecolors=[colors[i] for i in order],edgecolors='#292d2c',linewidths=.5,alpha=.93))
    if frames:
        for x in np.arange(16,59,5.6):
            chord=site.intersection(box(x-.13,-50,x+.13,50))
            if chord.is_empty:continue
            ymin,ymax=chord.bounds[1],chord.bounds[3]
            pts=np.array([[x,ymin,0],[x,ymin,17.3],[x,ymax,17.3],[x,ymax,0]])
            ax.plot(*project(pts).T,c=RED,lw=1.2)
    q=project(np.array([[-20,-32,0],[90,37,30],[-20,37,30],[90,-32,0]]))
    ax.set(xlim=(q[:,0].min()-3,q[:,0].max()+3),ylim=(-25,59),aspect='equal');ax.axis('off')
    fig.text(.04,.935,name.replace('_',' ').upper(),fontsize=17,fontfamily='monospace')
    fig.text(.04,.05,'Huella catastral y vecinos originales · volúmenes propuestos · base de cota simplificada +622,60 m',fontsize=10)
    fig.savefig(ROOT/(name+'.png'),dpi=180,facecolor=BG);fig.savefig(ROOT/'geometria'/(name+'.svg'),facecolor=BG);plt.close(fig)
plan();draw('02_contexto_3d')
# all new horizontal polygons clipped to cadastral property boundary.
def cut(x0,y0,x1,y1):return site.intersection(box(x0,y0,x1,y1))
variants={}
# A: transverse bridges, a thick inhabited spine and slots rising uninterrupted to sky.
a=[]
for z in [0,4.8,9.6,14.4]:
    a.append((cut(13,-7.4,60,-4.8),z,z+.35,'#766e5e'))
    for x in [14,27,40,53]:a.append((cut(x,-7.3,x+5.5,14),z,z+2.9,'#a8a097'))
variants['03_A_costillas_y_vacios']=a
# B: two opposed stair-stepped inhabitable ranges, a diagonal common braid remains unbuilt.
b=[]
for k,z in enumerate([0,3.6,7.2,10.8,14.4]):
    b.append((cut(14+3*k,-7.3,37+3*k,-1.8),z,z+3.2,'#aba394'))
    b.append((cut(18+3*k,2,44+3*k,14),z,z+3.2,'#8c8b80'))
    b.append((cut(25+3*k,-1.8,28+3*k,2),z,z+.35,'#aa3a31'))
b.append((cut(14,-7.3,30,13),0,.35,'#7b554a'))
variants['04_B_seccion_trenzada']=b
# C: two robust fixed service towers with inhabited deep-span bridges above common ground.
c=[(cut(14,-7.3,21,13),0,15.5,'#847965'),(cut(47,-7.3,55,4),0,15.5,'#847965')]
for z in [5,8.6,12.2]:
    c.extend([(cut(21,-7.3,47,-1.8),z,z+3.1,'#b9b2a6'),(cut(23,2,40,12),z,z+3.1,'#a89f8a')])
variants['05_C_dos_apoyos']=c
# D: permanent frame + irregular occupiable rooms around tall light chimneys; panel changes not entire homes.
d=[]
for k,z in enumerate([0,3.6,7.2,10.8,14.4]):
    for x,yy,w in [(14,-7.3,7),(24,0,8),(34,-7.3,9),(47,-7.3,10)]:
        d.append((cut(x,yy,x+w,yy+5.4),z,z+2.9,['#988367','#8d9190','#b1a392','#8a6556'][k%4]))
    d.append((cut(14,-2,60,0),z,z+.25,'#a94335'))
d.append((cut(14,-7.3,34,13),0,.25,'#8b5644'))
variants['06_D_soporte_y_relevo']=d
stats={}
for name,parts in variants.items():
    draw(name,parts,frames=name.startswith('06'))
    levels=sorted(set(z0 for g,z0,z1,c in parts))
    if name.startswith('05'):levels=[0,5,8.6,12.2]
    area=sum(unary_union([g for g,z0,z1,c in parts if abs(z0-level)<.01 or (z1-z0>10 and z0<=level<z1)]).area for level in levels)
    stats[name]={'area_horizontal_bruta_m2':round(area,1),'altura_max_m':max(z1 for g,z0,z1,c in parts),'area_fuera_parcela_m2':sum(g.difference(site).area for g,z0,z1,c in parts)}
# Editable OBJ with actual context triangles, site wire and separate named proposal objects
with (ROOT/'geometria/variantes_y_contexto.obj').open('w') as f:
    f.write('# meters; local x/y origin UTM25830 439984 4473229.4; local z=absolute-622.6\n');count=0
    f.write('o CONTEXTO_ORIGINAL\n')
    for t in tri:
        for v in t:f.write('v '+' '.join(map(str,v))+'\n')
        f.write(f'f {count+1} {count+2} {count+3}\n');count+=3
    for name,parts in variants.items():
        for index,(g,z0,z1,col) in enumerate(parts):
            f.write(f'o {name}_{index}\n')
            for q in polygons(g):
                pp=list(q.exterior.coords)[:-1];n=len(pp)
                for z in [z0,z1]:
                    for x,y in pp:f.write(f'v {x} {y} {z}\n')
                f.write('f '+' '.join(str(count+i+1) for i in range(n))+'\n');f.write('f '+' '.join(str(count+n+i+1) for i in range(n))+'\n')
                for i in range(n):f.write('f '+' '.join(str(count+j+1) for j in [i,(i+1)%n,(i+1)%n+n,i+n])+'\n')
                count+=2*n
(ROOT/'geometria/verificacion.json').write_text(json.dumps({'area_poligono_m2':site.area,'area_catastral_documentada_m2':651,'nota':'Tanteos volumetricos, no programa resuelto ni comprobacion urbanistica. A/B/C/D alternativos, superpuestos en OBJ: activar solo uno.','variantes':stats},indent=2))
print(stats)
