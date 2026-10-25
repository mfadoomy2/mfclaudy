from pathlib import Path
import rhino3dm as rh
import geometria as G
from primitivas import Model
from modelar import room
P=Path(__file__).resolve().parents[1]
m=Model('HABITACION');floor=G.ROOM;walls=floor.buffer(.12).difference(floor).union(floor.boundary.buffer(.06));door=G.box(2.05,-.22,3.05,.22);win=G.box(.75,4.90,2.85,5.32)
m.ex(floor.buffer(.13),-.20,.20,'forjado acabado Z=0','01_SUELO','corcho',support='reserva estructural')
for z,h,cut in [(0,.47,door),(.47,1.73,door.union(win)),(2.20,.35,win),(2.55,.45,G.Polygon())]:m.ex(walls.difference(cut),z,h,'pared habitación','02_PAREDES_CONTINUAS','cal',support='suelo, jambas y dinteles')
room(m,{'q':(0,0),'dc':0,'phi':0,'mirror':False})
m.ex(floor,3.0,.15,'cubierta oculta','91_CUBIERTA_OCULTA','blanco',visible=False,support='muros, sin cálculo estructural')
m.f.Strings['Dimensiones']='Cama1250x2000; mesa1800x900, bisagra canto900; armario máximo550 de profundidad; asiento2100x550; puerta1000. Metros y acabado z=0.'
assert m.f.Write(str(P/'HABITACION_CORREGIDA.3dm'),8)
print('HABITACION',len(m.f.Objects),flush=True)
