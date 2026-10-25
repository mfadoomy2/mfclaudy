from pathlib import Path
import pickle,json
import geometria as G
P=G.P
D=pickle.load(open(P/'datos/GEOMETRIA_CORREGIDA.pkl','rb'))
for d in D:
 for r in d['rooms']:
  r['poly']=G.tf(G.ROOM,r);r['window']=G.tf(G.box(.75,4.90,2.85,5.32),r);r['ray']=G.tf(G.box(.70,5.14,2.90,11.20),r)
 private=G.unary_union([r['poly'] for r in d['rooms']]);floor=G.unary_union([d['core'],private]+[r['connector'] for r in d['rooms']]).buffer(.12).buffer(-.12).union(d['entry']['pad'])
 if floor.interiors:floor=G.Polygon(floor.exterior)
 d['private']=private;d['floor']=floor
 d['common_windows']=G.common_windows(floor,private,d['program'],d['entry'])
 walls=floor.buffer(.12,join_style=1).difference(floor)
 for r in d['rooms']:walls=walls.union(r['poly'].boundary.buffer(.06,cap_style=2,join_style=1))
 for b in d['program']['baths']:walls=walls.union(b.buffer(.075,join_style=2).difference(b))
 walls=walls.union(d['program']['screen']);ret=G.box(-1.95,.10,-1.83,1.25)
 if d['variant']=='B':ret=G.scale(ret,xfact=-1,origin=(0,0))
 d['walls']=walls.union(ret);d['wincuts']=G.unary_union([r['window'] for r in d['rooms']])
 a=G.audit(d)
 assert a['public_d090_connected'] and a['common_exterior_windows']>=2,a
 assert all(r['circulation_d080'] and r['window_outward_strip_clear_6m'] and r['straight_door_segment_1000mm'] for r in a['rooms']),a
 # The entire 1.0m doorway projects into the clear bedside aisle, not onto the mattress.
 assert G.box(2.05,.20,3.05,4.05).intersection(G.BED).area==0
 print(d['code'],a['new_floor_m2'],a['gross_envelope_m2'],flush=True)
pickle.dump(D,open(P/'datos/GEOMETRIA_CORREGIDA.pkl','wb'))
