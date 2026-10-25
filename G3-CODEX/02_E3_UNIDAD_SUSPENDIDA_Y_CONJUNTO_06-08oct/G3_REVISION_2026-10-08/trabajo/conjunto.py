from proponer import *
from shapely.affinity import scale,translate
site=Polygon(json.loads(pathlib.Path('/Volumes/T7/G3 Proyectos/G3 CLAUDE/01_E2_IMAGINARIOS_PERSONAS_Y_MECANISMOS_05-06oct/G3_MECANISMOS_EN_PARCELA_2026-10-05/geometria/parcela_local.geojson').read_text())['geometry']['coordinates'][0])
m=Model();records=[];areas=collections.defaultdict(float);floors=[4.5,7.5,10.5,13.5]
mod=json.loads((B/'trabajo/modulos_datos.json').read_text())
def put(p,z,h,layer,color,name):
 m.solid(p,z,z+h,layer,color,name)
def wall(p,z,h,layer,color='privado',openings=[]):
 w=p.difference(p.buffer(-.15))
 for hole in openings:w=w.difference(hole)
 m.solid(w,z,z+h,layer,color)
def trans(p,x):return translate(scale(p,xfact=1,yfact=-1,origin=(0,0)),xoff=x)
# Flat street datum is explicit. Surveyed street gradient is not silently erased.
m.solid(site,-.16,0,'00 Solar - cota de estudio 622.60','suelo')
for k,z in enumerate(floors):
 kind='D' if k==3 else 'S';d=mod[kind]['depth'];height=5.44 if kind=='D' else 2.76
 for i in range(8):
  x=14+i*4.95;p=trans(Polygon(mod[kind]['footprint']),x);tag=f'{kind}{k+1}{i+1:02}'
  group=(f'Casa {k+1}' if k<3 else ('Casa 4' if i<4 else 'Casa 5'))
  m.solid(p,z-.24,z,f'01 Unidades - nivel {k+1}','madera',tag+' suelo')
  wall(p,z,height,f'01 Unidades - nivel {k+1}','privado',[box(x-.2,-1.15,x+4.9,.2),box(x+4.49,-2.22,x+4.9,-.1)])
  # Glass corner reads continuously, front screen separate from opaque back.
  front=p.intersection(box(x-.1,-1.15,x+4.8,.1)).difference(p.buffer(-.11))
  lower=front.difference(box(x+2.13,-.3,x+3.32,.3))
  m.solid(lower,z,z+2.64 if kind=='D' else z+height,f'02 Vidrio - nivel {k+1}','vidrio')
  if kind=='D':m.solid(front.difference(box(x+2.35,-.2,x+4.8,.2)),z+2.64,z+height,f'02 Vidrio - nivel {k+1}','vidrio')
  m.rect(x+2.16,-.035,1.13,.035,z,z+2.22,f'02 Accesos - nivel {k+1}','ventana',tag+' puerta')
  if kind=='D':
   loft=trans(Polygon(mod[kind]['loft']),x);m.solid(loft,z+2.44,z+2.64,'03 Alas - nivel 4','madera');roof=p.union(loft)
   bay=loft.intersection(box(x,0,x+4.7,1.18));wall(bay,z+2.64,2.80,'03 Alas - nivel 4','vidrio',[box(x,-.3,x+4.7,.12)])
   m.solid(roof,z+5.44,z+5.68,'03 Cubiertas duplex','acero');extra=loft.area
  else:
   
   if k==2:m.solid(p.difference(trans(Polygon(mod['D']['footprint']),x)),z+2.76,z+3.0,f'01 Cubierta posterior - nivel {k+1}','acero')
   extra=0
  areas['privado_bruto']+=p.area+extra
  records.append({'id':tag,'tipo':kind,'residentes':2 if kind=='D' else 1,'grupo':group,'x':x,'z':z,'area_bruta':p.area+extra,'fuera_parcela_m2':p.difference(site).area,'puerta':[x+2.7,0,z]})
 # continuous clear route 1.8, with wide landings facing the broad part of the site.
 gal=box(13.65,0,54,1.8);pocket=box(21.7,1.8,29.4,4.5);connection=box(32.3,1.8,35.1,2.4)
 deck=unary_union([gal,pocket]);m.solid(deck,z-.20,z,f'04 Calle comun - {k+1}','comun');areas['galerias_abiertas']+=deck.area
 # All dwellings have same level entry; rail on outer edge, interrupted only at core.
 edge=LineString([(13.65,1.8),(21.7,1.8),(21.7,4.5),(29.4,4.5),(29.4,1.8),(32.3,1.8)])
 for line in [edge,LineString([(35.1,1.8),(54,1.8)])]:
  m.solid(line.buffer(.025,cap_style=2),z+1.05,z+1.1,f'05 Barandillas - {k+1}','acero')
  for a in np.arange(0,line.length,.105):
   p=line.interpolate(a);m.rect(p.x-.008,p.y-.008,.016,.016,z,z+1.1,f'05 Barandillas - {k+1}','acero')
 # common room at the end: residents do not need to cross it to get home.
 living=box(54,-5.4,60.8,1.8);areas['comun_cerrado_bruto']+=living.area
 m.solid(living,z-.24,z,f'06 Cocina salon - {k+1}','madera');wall(living,z,2.7,f'06 Cocina salon - {k+1}','comun',[box(53.8,.1,54.3,1.45),box(55,1.5,59.6,2.0)])
 m.rect(55,1.68,4.6,.08,z+.4,z+2.65,f'06 Cocina salon - {k+1}','ventana')
 m.rect(54.4,-5.15,5.5,.65,z,z+.92,f'06 Equipamiento - {k+1}','tecnico')
 for yy in [-3.2,-.8]:m.solid(rounded(55.2,yy,3.7,.85,.1),z+.73,z+.78,f'06 Equipamiento - {k+1}','madera')
 
 if k==3:m.solid(living,z+2.76,z+3.0,f'06 Cubierta salon - {k+1}','acero')
# Core as walls, landings and real stair flights, not a solid inaccessible block.
core=box(29.5,1.8,38.1,6.15)
for j,z in enumerate([0]+floors):
 top=([0]+floors+[16.5])[j+1]
 m.solid(core,z-.20,z,'07 Nucleo - forjados','privado');areas['nucleo_bruto']+=core.area
 wall(core,z,top-z,'07 Nucleo - cerramiento','privado',[box(33.1,1.6,34.3,2.0)])
 m.rect(35.8,4.0,2.0,2.05,z,top,'07 Ascensor - reserva 2 x 2.05','tecnico')
 rise=top-z;N=math.ceil(rise/.175);N+=N%2;nh=N//2;C=rise/N;H=.28;run=(nh-1)*H;xs=31.0
 # first 4.5m interval requires longer runs; reserved next to core as separate lower stair pocket.
 if j==0:xs=31.0
 for q in range(nh):
  m.rect(xs+q*H,3.4,H+.02,1.1,z+q*C,z+(q+1)*C,'07 Escalera comun - tramo A','escalera')
  m.rect(xs+(nh-1-q)*H,4.65,H+.02,1.1,z+rise/2+q*C,z+rise/2+(q+1)*C,'07 Escalera comun - tramo B','escalera')
 m.rect(xs+run,3.4,1.15,2.35,z+rise/2-.16,z+rise/2,'07 Escalera comun - meseta','escalera')
 # schematic handrails on exposed stair edges
 for yy in [3.43,5.72]:m.rod([xs,yy,z+.95],[xs+run,yy,z+rise/2+.95],.025,'07 Pasamanos de nucleo')
# load-bearing regular frame under each party-wall line
for x in [13.9]+[18.85+i*4.95 for i in range(8)]:
 for y in [-6.0,.0]:m.rect(x-.09,y-.09,.18,.18,0,19.25,'08 Porticos continuos - dimensionar','acero')
for z in floors:
 for y in [-6,.0]:m.rect(13.8,y-.1,39.9,.2,z-.38,z-.20,'08 Vigas - dimensionar','acero')
# Ground-floor program, with visible doors and common street left clear.
pb=[('Cantina y cocina',box(14,-6.5,24.2,-.3),'barrio'),('Taller limpio y reparacion',box(26,-6.8,36,-2),'barrio'),('Lavanderia y ropero',box(38,-6.7,44,-2),'tecnico'),('Acogida y cuidados',box(46,-6.4,51,-2),'comun'),('Almacen instalaciones y aseos',box(54,-5.4,60.8,-.2),'tecnico')]
for name,p,col in pb:
 areas['pb_programa_bruto']+=p.area;opening=box(p.bounds[0]+.7,p.bounds[3]-.3,p.bounds[0]+1.8,p.bounds[3]+.3)
 wall(p,0,3.8,'09 Barrio - '+name,col,[opening]);m.solid(p,3.8,4.03,'09 Cubierta - '+name,'acero')
 # a red threshold marks contact with the market, without occupying clear route
for x in [17,21,25]:m.solid(rounded(x,3.2,2,.8,.06),.72,.77,'09 Mesas de intercambio','barrio')
# independent pedestrian approach from the west, ground plane without an invented exit through neighbors.
m.solid(box(12.5,.1,60.8,1.7).intersection(site),0,.015,'09 Pasaje hasta patio interior','comun')
# surface, count and non-overlap checks at schematic level
for u in records:
 u['recorrido_ortogonal_hasta_puerta_nucleo_m']=abs(u['puerta'][0]-33.7)+2.1
 for v in records:
  if u['id']>=v['id'] or u['z']!=v['z']:continue
  p=trans(Polygon(mod[u['tipo']]['footprint']),u['x']);q=trans(Polygon(mod[v['tipo']]['footprint']),v['x'])
  if p.intersection(q).area>1e-6:raise RuntimeError('Units overlap')
report={'resumen':dict(areas),'unidades':records,'habitantes':sum(u['residentes'] for u in records),'count':len(records),'altura_cubierta_duplex':19.18,'max_recorrido_modelo_m':max(u['recorrido_ortogonal_hasta_puerta_nucleo_m'] for u in records),'area_parcela':site.area,'notes':['Superficies geometricas brutas: no equivalen a utiles ni a computo urbanistico.','Recorrido por eje de galeria hasta puerta del nucleo, no certificacion de salida de planta.','Nucleo y estructura requieren proyecto de fuego, ventilacion, puertas y secciones.','Medianeras sin ventilacion prestada. Falta simulacion de luz y ficha urbanistica.']}
(B/'trabajo/conjunto_datos.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));m.save('05_CONJUNTO_propuesto_32_40')
print(json.dumps({**dict(areas),'habitantes':report['habitantes'],'altura':19.18,'max_recorrido':report['max_recorrido_modelo_m'],'fuera_m2':sum(u['fuera_parcela_m2'] for u in records)},indent=2),flush=True)
