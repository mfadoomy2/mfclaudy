import geometria as G
import json
from shapely.geometry import shape,mapping
from scipy.optimize import differential_evolution
P=G.P;R=G.R
src=P/'fuentes/PARCELA_REAL.geojson'
raw=json.loads(src.read_text());parcel=shape(raw['geometry']);origin=raw['properties']['origin_utm']
results=[];placements=[]
for f in G.F:
 hull=f['floor'].buffer(.12);c=hull.centroid;local=G.translate(hull,-c.x,-c.y).simplify(.025,preserve_topology=True)
 count=[0]
 def obj(v):
  count[0]+=1;x,y,ang=v;g=G.translate(G.rotate(local,ang,origin=(0,0)),x,y)
  return g.difference(parcel).area*10000 + x*.001
 cache=json.loads((P/'verificacion/ENCAJE_PARCELA.json').read_text()) if (P/'verificacion/ENCAJE_PARCELA.json').exists() else None
 if cache:
  prev=next(a for a in cache['resultados'] if a['codigo']==f['audit']['codigo']);v0=prev['centro_local_m']+[prev['rotacion_grados']]
 else:
  op0=differential_evolution(obj,[(19,53),(-3,6),(0,360)],seed=32,popsize=10,maxiter=130,tol=1e-7,polish=False);v0=op0.x
 local=G.translate(hull,-c.x,-c.y)
 def refine(v):
  count[0]+=1;x,y,ang=v;g=G.translate(G.rotate(local,ang,origin=(0,0)),x,y)
  return g.difference(parcel.buffer(-.05)).area
 opt=differential_evolution(refine,[(v0[0]-1.5,v0[0]+1.5),(v0[1]-1,v0[1]+1),(v0[2]-4,v0[2]+4)],seed=22,popsize=8,maxiter=100,tol=1e-8,polish=True)
 x,y,ang=opt.x
 T=lambda g,c=c,x=x,y=y,ang=ang:G.translate(G.rotate(G.translate(g,-c.x,-c.y),ang,origin=(0,0)),x,y)
 actual=T(hull);outside=actual.difference(parcel).area
 row={'codigo':f['audit']['codigo'],'habitantes':len(f['rooms']),'area_envolvente_m2':round(hull.area,2),'fuera_parcela_m2':round(outside,4),'ajuste_completo':outside<.001,'rotacion_grados':round(ang,3),'centro_local_m':[round(x,3),round(y,3)],'evaluaciones':count[0],'modelo':'Escala 1:1, giros y traslaciones; envolvente de estudio +0.12 m. Busqueda heuristica, no prueba de imposibilidad.'}
 front=G.LineString([(12.07,7.43),(13.28,-7.50)])
 free=parcel.buffer(-.45).difference(actual.buffer(.45));ent=T(G.Point(f['entry']['outside']))
 root=next((p for p in G.polys(free) if p.buffer(.005).covers(ent)),None)
 row['paso_exterior_90cm_desde_frente']=bool(root is not None and root.distance(front)<.451)
 row['bows_con_banda_3m_dentro_parcela']=sum(parcel.covers(T(st)) for st in f['strips'])
 row['margen_envolvente_al_limite_m']=round(actual.distance(parcel.boundary),3) if outside<.001 else 0
 results.append(row);placements.append((f,T,actual,row));print('FIT',row,flush=True)
(P/'verificacion/ENCAJE_PARCELA.json').write_text(json.dumps({'parcela_m2':parcel.area,'origen_utm':origin,'crs':'EPSG:25830','resultados':results,'limite':'Encaje geometrico aislado. No valida normativa, acceso desde calle, contexto, luz o posibilidad de apilar.'},ensure_ascii=False,indent=2))
(P/'fuentes/PARCELA_REAL.geojson').write_text(src.read_text())
if __name__=='__main__':pass
