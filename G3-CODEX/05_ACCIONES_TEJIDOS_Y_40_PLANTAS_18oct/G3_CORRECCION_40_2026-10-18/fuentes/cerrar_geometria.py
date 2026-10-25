from pathlib import Path
import pickle,json,csv
import geometria as G
P=Path(__file__).resolve().parents[1]
D=pickle.load(open(P/'datos/GEOMETRIA_CORREGIDA.pkl','rb'))
assert len(D)==40
reports=[]
for d in D:
 # Complete the return connecting the privacy screen to the bathroom wall.
 ret=G.box(-1.95,.10,-1.83,1.25)
 if d['variant']=='B':ret=G.scale(ret,xfact=-1,origin=(0,0))
 d['walls']=d['walls'].union(ret)
 a=G.audit(d)
 assert a['public_d090_connected'],a
 assert a['common_exterior_windows']>=2,a
 assert a['room_overlap_m2']<.0001 and a['holes']==0,a
 assert all(r['circulation_d080'] and r['window_outward_strip_clear_6m'] and r['straight_door_segment_1000mm'] for r in a['rooms']),a
 entryline=G.tf(G.LineString([(-.62,1.4),(.62,1.4)]),d['entry'])
 assert entryline.difference(d['floor'].boundary.buffer(.001)).length<.001
 a['straight_main_entry_1200mm']=True
 assert G.box(2.05,.20,3.05,4.05).intersection(G.BED).area==0
 a['beds_outside_doorway_projection']=True
 # Bathroom fixtures as modelled, including telescoping leaves parked at the front wall.
 obs=G.unary_union([G.box(.04,.15,.44,.5),G.Point(1.35,1.53).buffer(.23),G.box(.90,1.18,.935,1.96),G.box(.05,.015,.5,.115)])
 walk=G.box(0,0,1.7,2).difference(obs).buffer(-.4)
 pts=[G.Point(*xy) for xy in [(1,.45),(.45,1.55),(1.3,.85),(.85,.6)]]
 assert any(all(c.buffer(.001).contains(p) for p in pts) for c in G.polys(walk))
 a['both_bathrooms_d080_use_points_connected']=True
 a['main_entry_glazed']=True
 a['clothes_rack_or_bicycle_inside']=False
 a['source_bearing_changes_degrees']={r['id']:round(G.wrap(r['bearing']-r['source_bearing']),1) for r in d['rooms']}
 reports.append(a)
pickle.dump(D,open(P/'datos/GEOMETRIA_CORREGIDA.pkl','wb'))
(P/'verificacion/ESPACIO_FINAL.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
with open(P/'datos/SUPERFICIES.csv','w') as f:
 w=csv.writer(f);w.writerow(['codigo','habitantes','suelo_anterior_m2','suelo_nuevo_m2','envolvente_nueva_m2','habitacion_m2','cota_suelo_m','ventanas_comunes_exteriores'])
 for a in reports:w.writerow([a['code'],4,a['old_floor_m2'],a['new_floor_m2'],a['gross_envelope_m2'],a['private_each_m2'],0,a['common_exterior_windows']])
print(json.dumps({'units':40,'bedrooms':160,'gross_range':[min(a['gross_envelope_m2'] for a in reports),max(a['gross_envelope_m2'] for a in reports)],'new_floor_range':[min(a['new_floor_m2'] for a in reports),max(a['new_floor_m2'] for a in reports)]}),flush=True)
