from pathlib import Path
import json,csv,math,hashlib,zipfile
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
P=Path(__file__).resolve().parents[1];R=json.loads((P/'datos/RESUMEN_40.json').read_text())
pdfmetrics.registerFont(TTFont('Arial','/System/Library/Fonts/Supplemental/Arial.ttf'));pdfmetrics.registerFont(TTFont('ArialB','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
W,H=1190.55,841.89;INK='#253d35';PINK='#c94088';BG='#faf8f0';CYAN='#179fa8';N=0
c=canvas.Canvas(str(P/'output/pdf/G3_40_PLANTAS_ATLAS_A3.pdf'),pagesize=(W,H));c.setTitle('G3 | 20 familias / 40 plantas exploratorias');c.setAuthor('Estudio de proyecto G3 con Adam')
def txt(t,x,y,size=11,color=INK,bold=False):
 c.setFillColor(HexColor(color));c.setFont('ArialB' if bold else 'Arial',size);c.drawString(x,y,t)
def para(t,x,y,width=300,size=11,color=INK):
 style=ParagraphStyle('p',fontName='Arial',fontSize=size,leading=size*1.42,textColor=HexColor(color));p=Paragraph(t,style);a,b=p.wrap(width,H);p.drawOn(c,x,y-b);return y-b-14
def base(k,title,sub):
 global N
 N+=1;c.setFillColor(HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0);txt('G3 / UNIDAD / EXPLORACIÓN',38,H-35,10,CYAN,True);txt(k,38,H-86,32,PINK,True);txt(title,155,H-86,28,INK,True);txt(sub,38,H-112,10);c.setStrokeColor(HexColor(INK));c.setLineWidth(.5);c.line(38,40,W-38,40);txt('18.10.2026  /  Hipótesis geométricas sin implantación ni validación normativa',38,24,9);txt(f'{N:02}',W-60,24,10)
def svg(code,x,y,w,h):
 d=svg2rlg(str(P/'plantas'/f'{code}_PLANTA.svg'));f=min(w/d.width,h/d.height);c.saveState();c.translate(x+(w-d.width*f)/2,y+(h-d.height*f)/2);c.scale(f,f);renderPDF.draw(d,c,0,0);c.restoreState()
def img(code,x,y,w,h):c.drawImage(str(P/'plantas'/f'{code}_PLANTA.png'),x,y,w,h,preserveAspectRatio=True,anchor='c',mask='auto')
base('40','Plantas para discutir la unidad','20 familias espaciales × 2 variantes / Cuatro personas y cuatro habitaciones privadas en cada ensayo')
svg('12A',30,170,745,535)
y=H-160
y=para('Una colección para abrir el proyecto. Alas, peines, giros, patios y cadenas prueban distintas maneras de relacionar intimidad, trabajo, cuidado y convivencia.',810,y,330,16)
y=para('<b>Lo que permanece:</b> cuatro retiros privados, mesa de dibujo, cocina, mesa compartida, estancia y dos baños. Se mantienen para comparar la distribución con una base común.',810,y,330)
y=para('<b>Lo que cambia:</b> posiciones, orientaciones, longitud, vacíos, acceso propuesto y situación del equipamiento común. B también cambia el colchón circular por uno rectangular.',810,y,330)
y=para('<b>Lectura crítica:</b> las habitaciones conservan una familia geométrica común; este atlas explora sobre todo su agregación. No son cuarenta soluciones de detalle constructivo.',810,y,330)
para('Todos los ensayos superan 150 m² de superficie geométrica de suelo. Aún no resuelven el objetivo previo de 1.500 m² para 40 personas con accesos, estructura y servicios generales.',810,y,330,11,PINK)
txt('ENSAYO / COMPARACIÓN / DESCARTE / NUEVA SÍNTESIS',60,114,17,INK,True);c.showPage()
base('01','Reglas y límites de la exploración','La forma es una hipótesis de convivencia. Las medidas ayudan a ponerla a prueba.')
columns=[(42,340),(430,340),(818,330)]
texts=[[
('PROGRAMA QUE SE COMPARA','4 habitaciones individuales de unos 18 m², con base útil de 3,80 × 4,40 m y nicho lateral; dos baños de 2,10 × 2,40 m; frente de cocina de 3,60 × 0,70 m; frigorífico; mesa común de 1,80 × 0,90 m; sofá de 2,40 × 0,85 m y almacenamiento.'),
('DOS VARIANTES POR FAMILIA','A: colchón circular Ø2,10 m sin pedestal de mayor diámetro. B: colchón rectangular 1,25 × 2,00 m, nicho lateral más profundo y ajustes de ángulo, posición y equipamiento. No se trata de una rotación del mismo dibujo.'),
('TRABAJO DENTRO DE CADA CUARTO','Tablero de dibujo de 1,80 × 0,90 m abierto, articulado por el canto corto de 0,90 m. Línea rosa: eje de giro en pared. Requiere herraje, bloqueo y soporte calculados; aquí no se resuelve su construcción. Taburete y zona de uso representados.')],
[('CÓMO SE COLOCAN LAS PIEZAS','Cada familia propone anclajes y orientaciones explícitos. Se separan las habitaciones hasta evitar intersecciones y se conectan sus umbrales. Después se sitúa el programa compartido, manteniendo una red de paso libre. Los puntos son decisiones proyectuales revisables, no datos observados ni una optimización objetiva.'),
('RECORRIDOS COMPROBADOS','Se reserva una red antes de colocar mobiliario. Se comprueba conexión entre las cuatro aproximaciones a las puertas mediante un espacio erosionado 0,45 m alrededor de los obstáculos dibujados. La tolerancia de asociación a esa red es 0,35 m. El resultado 4/4 es una prueba geométrica parcial, no accesibilidad ni evacuación verificadas.'),
('SUPERFICIES COMPARABLES','Suelo = unión de habitaciones y ámbito compartido, descontando patios. Son áreas de contornos conceptuales: no superficie construida reglamentaria. Los baños están incluidos en el compartido bruto. No se añade espesor de cerramientos ni estructura.')],
[('LUZ Y TEXTILES','Turquesa: huecos propuestos en el borde exterior de cada habitación. Rosa discontinua: segunda capa textil. No representan horas de sol, iluminancia o protección térmica calculadas. Es necesario probar cada alternativa en la parcela real y frente a sus vecinos.'),
('RETIRO Y VIDA EN COMÚN','Dormir, dibujar y guardar se mantienen en privado. Preparar comida, comer y estar se comparten. El sofá y la mesa son focos iniciales; las formas alargadas todavía tienen espacios residuales. No se afirma que estos hábitos describan a toda una generación.'),
('LO QUE AÚN HAY QUE DISEÑAR','Acceso al complejo y a cada unidad, puertas exteriores, filtros visuales ante baños, ventilación, ventana habitable con volumen real, instalaciones, acústica, sección, estructura y envolvente. Los baños son reservas equipadas: su integración en una pared continua queda pendiente. Ningún ensayo es proyecto ejecutivo.')]]
for (x,w),blocks in zip(columns,texts):
 y=H-160
 for title,t in blocks:
  txt(title,x,y,12,CYAN,True);y=para(t,x,y-18,w,11)-20
c.showPage()
for sheet in range(4):
 base(f'{sheet+2:02}','Índice de alternativas',f'Familias {sheet*5+1:02}–{sheet*5+5:02} / A circular / B rectangular / Imágenes a distinta escala: comparar con las cotas')
 for j in range(5):
  a,b=R[sheet*10+j*2:sheet*10+j*2+2];x=38+j*226
  txt(a['code'][:2],x,H-151,20,PINK,True);para(a['family'],x,H-163,210,12)
  for v,r in enumerate([a,b]):
   yy=H-425-v*288;img(r['code'],x,yy,215,220);txt(r['code']+'  /  '+f"{r['floor_m2']:.1f} m²",x,yy-16,11,INK,True)
 c.showPage()
for r in R:
 code=r['code'];base(code,r['family'],('A / Colchón circular y anclajes iniciales' if r['variant']=='A' else 'B / Colchón rectangular, giros y relaciones modificados'))
 svg(code,24,66,798,650)
 x=847;y=H-158;w=305
 txt('4 PERSONAS / 4 RETIROS',x,y,13,CYAN,True);y-=31
 txt(f"{r['floor_m2']:.1f} m²",x,y,30,INK,True);y-=24
 y=para(f"Suelo geométrico: {r['floor_m2']:.2f} m²<br/>Privado: {r['bedrooms_m2']:.2f} m²<br/>Compartido bruto, incluidos baños: {r['shared_gross_m2']:.2f} m²",x,y,w,11)
 txt('REGLA ESPACIAL',x,y,11,CYAN,True);y=para(r['logic'],x,y-17,w,11)
 txt('PUNTO DÉBIL',x,y,11,PINK,True);y=para(r['risk'],x,y-17,w,11)
 txt('COMPROBACIÓN PARCIAL',x,y,11,CYAN,True)
 y=para(f"Red común: {r['connections_090_graphic']}/4 umbrales asociados.<br/>Colisiones cama/mesa/armario: {len(r['geometry_conflicts'])}.<br/>Punto E/S sobre borde común: {'sí' if r['entry_on_boundary'] else 'pendiente'}.<br/>No se verifica recorrido completo desde E/S, accesibilidad ni evacuación.",x,y-17,w,10)
 txt('COSTE DE SUPERFICIE',x,y,11,PINK,True)
 y=para(f"Diez unidades iguales: {r['floor_m2']*10:,.0f} m² de suelo, antes de elementos generales. Supera el objetivo previo de 1.500 m². Necesita compactación o revisión del programa.",x,y-17,w,10)
 y=para('VERDE / privado · CREMA / compartido<br/>LILA / baños y nichos · TURQUESA / trabajo y cocina<br/>ROSA / estancia, bisagra y textil · G / guardar<br/>VERDE AZUL CLARO / reserva de paso, sin paredes<br/>E/S / acceso propuesto, sin puerta exterior resuelta',x,y,w,9)
 para('Cotas en metros. Dibujo vectorial a escala variable.<br/>Espesores y mecanismos sin dimensionar.',x,y,w,9)
 c.showPage()
for half in range(2):
 base(f'{47+half:02}','Comparación de superficie',f'Familias {half*10+1:02}–{half*10+10:02} / El menor consumo de suelo no implica la mejor vivienda')
 headers=[('CÓDIGO',42),('FAMILIA',125),('SUELO m²',435),('PRIVADO m²',565),('COMÚN m²',705),('RED*',850),('10 UNIDADES m²',935)]
 for t,x in headers:txt(t,x,H-158,10,CYAN,True)
 for j,r in enumerate(R[half*20:half*20+20]):
  y=H-185-j*26;txt(r['code'],42,y,10,INK,True);txt(r['family'],125,y,10);txt(f"{r['floor_m2']:.1f}",435,y,10);txt(f"{r['bedrooms_m2']:.1f}",565,y,10);txt(f"{r['shared_gross_m2']:.1f}",705,y,10);txt(str(r['connections_090_graphic'])+'/4',850,y,10);txt(f"{r['floor_m2']*10:.0f}",935,y,10,PINK)
 para('* Asociación de cuatro aproximaciones a una misma componente geométrica libre. Prueba parcial definida en la página 2. Toda la colección es exploratoria: no hay una alternativa declarada apta para construir o implantar.',42,105,1080,10)
 c.showPage()
c.save()
with open(P/'datos/COMPARACION.csv','w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=[k for k in R[0] if k not in ['geometry_conflicts','footprint_bounds','room_angles']]);writer.writeheader();writer.writerows([{k:v for k,v in r.items() if k in writer.fieldnames} for r in R])
print('PDF_GENERADO',N)
