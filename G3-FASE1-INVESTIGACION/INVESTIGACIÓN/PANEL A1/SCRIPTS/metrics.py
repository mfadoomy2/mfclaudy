import pickle, math, json, collections
from shapely import wkt
from shapely.geometry import Point
D=pickle.load(open('osm.pkl','rb')); cx,cy=D['C']; C=Point(cx,cy)
F=[]
for f in D['feats']:
    g=wkt.loads(f['wkt']); f['g']=g; p=g.centroid if g.geom_type!='Point' else g
    f['x'],f['y']=p.x,p.y; f['d']=g.distance(C); f['dc']=math.hypot(p.x-cx,p.y-cy)
    f['az']=(math.degrees(math.atan2(p.x-cx,p.y-cy))+360)%360; F.append(f)
def has(f,t): return t in f['temas']
GR={
 'comercio':lambda f:has(f,'COMERCIO_Y_ACTIVIDAD') and f['t']!='lineas_fisicas',
 'equipamientos':lambda f:has(f,'EQUIPAMIENTOS_Y_LOCALES') and f['t']!='lineas_fisicas',
 'arboles':lambda f:f['sub']=='natural=tree',
 'transporte':lambda f:f['sub'] in ('highway=bus_stop','railway=subway_entrance','public_transport=station'),
 'bancos':lambda f:f['sub']=='amenity=bench',
 'portales':lambda f:has(f,'ACCESOS_Y_UMBRALES') and f['t']=='puntos_fisicos',
 'patrimonio':lambda f:has(f,'PATRIMONIO_Y_CULTURA'),
 'farolas':lambda f:f['sub']=='highway=street_lamp',
 'barreras':lambda f:has(f,'BARRERAS'),
 'edificios':lambda f:has(f,'EDIFICIOS') and f['t']=='poligonos_fisicos',
}
R=[100,200,300,400,500]
out={'centro_utm':[cx,cy],'rings':{},'sectores':{},'nearest':{},'subtipos':{}}
for k,fn in GR.items():
    sel=[f for f in F if fn(f)]
    out['rings'][k]=[sum(1 for f in sel if (R[i-1] if i else 0)<f['dc']<=R[i]) for i in range(len(R))]
    out['sectores'][k]=[[sum(1 for f in sel if int(((f['az']+11.25)%360)//22.5)==s and (R[i-1] if i else 0)<f['dc']<=R[i]) for i in range(len(R))] for s in range(16)]
    out['subtipos'][k]=collections.Counter(f['sub'] for f in sel if f['dc']<=500).most_common(8)
# nearest
def near(fn,lab):
    s=sorted([f for f in F if fn(f)],key=lambda f:f['d'])
    if s: out['nearest'][lab]=dict(d=round(s[0]['d'],1),nom=s[0]['nom'],sub=s[0]['sub'],xy=[s[0]['x'],s[0]['y']])
near(lambda f:f['sub']=='railway=subway_entrance','metro (boca)')
near(lambda f:f['sub']=='public_transport=station','estación')
near(lambda f:f['sub']=='highway=bus_stop','bus')
near(lambda f:f['sub'] in('leisure=park','leisure=garden'),'parque/jardín')
near(lambda f:f['sub']=='place=square','plaza')
near(lambda f:f['sub']=='amenity=pharmacy','farmacia')
near(lambda f:f['sub'] in('shop=supermarket',),'supermercado')
near(lambda f:f['sub']=='shop=convenience','alimentación')
near(lambda f:f['sub'] in('amenity=school','building=school'),'colegio')
near(lambda f:f['sub']=='amenity=library','biblioteca')
near(lambda f:f['sub'] in('amenity=drinking_water',),'fuente de beber')
near(lambda f:f['sub']=='amenity=bench','banco')
near(lambda f:f['sub']=='natural=tree','árbol')
near(lambda f:f['sub']=='amenity=bicycle_rental','bici pública')
near(lambda f:f['sub'] in('leisure=playground',),'juegos infantiles')
near(lambda f:f['sub'] in('leisure=pitch','leisure=sports_centre','building=sports_centre'),'deporte')
near(lambda f:f['sub'] in('amenity=cafe','amenity=bar','amenity=pub'),'bar/café')
near(lambda f:f['sub'] in('amenity=university','building=university','amenity=college','building=college'),'universidad')
near(lambda f:f['sub'] in('amenity=marketplace',),'mercado')
near(lambda f:f['sub'] in('amenity=doctors','amenity=clinic','amenity=hospital'),'salud')
# stations named
out['estaciones']=sorted({(f['nom'],round(f['dc'])) for f in F if f['sub'] in('public_transport=station','railway=subway_entrance') and f['dc']<=600},key=lambda x:x[1])
# street lengths by class within 500 (clip)
from shapely.geometry import Point as P
circ=C.buffer(500)
L=collections.Counter()
for f in F:
    if f['t']=='lineas_fisicas' and f['sub'] and f['sub'].startswith('highway='):
        L[f['sub']]+=f['g'].intersection(circ).length
out['longitudes_500']={k:round(v) for k,v in L.most_common()}
# green area within 500
ga=sum(f['g'].intersection(circ).area for f in F if f['t']=='poligonos_fisicos' and f['sub'] in('leisure=park','leisure=garden','place=square','leisure=playground'))
out['verde_m2_500']=round(ga)
out['bld_area_500']=round(sum(f['g'].intersection(circ).area for f in F if GR['edificios'](f)))
out['total']=len(F)
json.dump(out,open('metrics.json','w'),ensure_ascii=False,indent=0)
for k,v in out['rings'].items(): print(k,v,sum(v))
for k,v in out['nearest'].items(): print(k,v['d'],v['nom'],v['sub'])
print(out['estaciones']); print(out['longitudes_500']); print(out['verde_m2_500'],out['bld_area_500'])
for k,v in out['subtipos'].items(): print(k,v[:6])
