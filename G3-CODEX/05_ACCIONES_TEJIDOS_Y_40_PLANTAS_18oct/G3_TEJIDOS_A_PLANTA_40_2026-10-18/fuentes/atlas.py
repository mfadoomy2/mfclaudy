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
c=canvas.Canvas(str(P/'output/pdf/G3_40_PLANTAS_DESDE_TEJIDOS_A3.pdf'),pagesize=(W,H));c.setTitle('G3 | 20 familias / 40 plantas exploratorias');c.setAuthor('Estudio de proyecto G3 con Adam')
def txt(t,x,y,size=11,color=INK,bold=False):
 c.setFillColor(HexColor(color));c.setFont('ArialB' if bold else 'Arial',size);c.drawString(x,y,t)
def para(t,x,y,width=300,size=11,color=INK):
 style=ParagraphStyle('p',fontName='Arial',fontSize=size,leading=size*1.42,textColor=HexColor(color));p=Paragraph(t,style);a,b=p.wrap(width,H);p.drawOn(c,x,y-b);return y-b-14
def base(k,title,sub):
 global N
 N+=1;c.setFillColor(HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0);txt('G3 / UNIDAD / EXPLORACIÓN',38,H-35,10,CYAN,True);txt(k,38,H-86,32,PINK,True);txt(title,155,H-86,28,INK,True);txt(sub,38,H-112,10);c.setStrokeColor(HexColor(INK));c.setLineWidth(.5);c.line(38,40,W-38,40);txt('18.10.2026  /  Hipótesis geométricas sin implantación ni validación normativa',38,24,9);txt(f'{N:02}',W-60,24,10)
def svg(code,x,y,w,h,suffix='PLANTA'):
 d=svg2rlg(str(P/'plantas'/f'{code}_{suffix}.svg'));f=min(w/d.width,h/d.height);c.saveState();c.translate(x+(w-d.width*f)/2,y+(h-d.height*f)/2);c.scale(f,f);renderPDF.draw(d,c,0,0);c.restoreState()
def img(code,x,y,w,h):c.drawImage(str(P/'plantas'/f'{code}_PLANTA.png'),x,y,w,h,preserveAspectRatio=True,anchor='c',mask='auto')
base('40','Del tejido a la planta','Segunda serie adicional / 20 propuestas × 2 variantes / Conservar la primera serie')
svg('N02A',25,120,790,580,'TRAZA')
y=H-160
for t in ['<b>El punto de partida son los tres tejidos de acciones anteriores.</b> Sus posiciones proporcionan anclajes; no se utiliza una silueta arquitectónica de referencia.', 'Cada dibujo hace visible el coste de la traducción: superficies de uso, repetición de actividades privadas, desplazamientos de los anclajes y conexiones añadidas.', '<b>Esta serie es una prueba de traducción espacial.</b> Los ajustes de huellas deforman mucho el diagrama. No se afirma que sea una copia exacta ni que conserve todas sus relaciones.', '<b>Resultado crítico:</b> las distribuciones son demasiado extensas para el objetivo previo de superficie. Algunas convierten la convivencia en una red de corredores; deben compactarse antes de elegir una vivienda.']:
 y=para(t,840,y,300,12)
c.showPage()
base('01','Cómo se traduce el diagrama','Las acciones no equivalen a habitaciones. Las líneas tienen significados distintos.')
blocks=[('ANCLAJES Y HUELLAS','Se toman literalmente las coordenadas de RESULTADOS.json, tejidos 1, 2 y 3. La retícula original no tenía metros: se ensaya una conversión de 0,94 m por paso, con deformaciones distintas en X e Y. Esta escala es una decisión de ensayo, no un dato medido. A y B alteran ligeramente la deformación y las huellas de uso.'),('CUATRO RETIROS, NO UN ÚNICO DORMIR','Se repiten cama, ropa, mesa de dibujo y privacidad en H1–H4. Sus anclajes iniciales se toman de dormir, entrevista, hablar en privado y dibujar: nodos A01, A06, A10 y A11. Es una interpretación nueva del programa, no cuatro dormitorios ya demostrados por el grafo. Cada actividad privada aparece en varios lugares.'),('SUPERFICIES QUE PUEDEN COMPARTIRSE','A13 cortar y A14 coser comparten una mesa de trabajo por turnos. A16 llegar, A17 recibir y A18 salir comparten un umbral. R contiene reparación y herramientas. Los baños se duplican; secar tiene reserva propia. Son elecciones explícitas que deben discutirse.'),('RUTAS Y PROTECCIÓN','Cocinar–comer y ducharse–secar generan enlaces funcionales. Se añaden enlaces para conectar las huellas y se buscan trayectos alrededor de los obstáculos. Las relaciones PROTEGER nunca se construyen como pasillos por sí mismas. Su resolución acústica o visual no se acredita con distancia.'),('QUÉ CAMBIA RESPECTO AL DIBUJO','La separación automática evita solapes entre las huellas y reserva 2 m entre sus cajas para permitir rutas. Esto es conservador y produce mucho exceso de suelo. Los puntos rosas y sus líneas muestran cuánto se desplaza cada anclaje. Las rutas se calculan en una malla de 0,27 m; no son un trazado arquitectónico definitivo.'),('LÍMITES Y COMPARACIÓN','Suelo geométrico, sin espesores de paredes ni estructura. Recorridos de 1,20 m nominal en el generador; una comprobación parcial relaciona las aproximaciones a los dormitorios, sin acreditar accesibilidad o evacuación. No hay análisis solar, acústico, ni parcela. La lectura de las acciones sigue siendo una hipótesis del proyecto.')]
for i,(head,body) in enumerate(blocks):
 x=42+(i%3)*385;y=H-165-(i//3)*255;txt(head,x,y,12,CYAN,True);para(body,x,y-20,340,12)
c.showPage()
for sheet in range(4):
 base(f'I{sheet+1}','Índice de la segunda serie',f'Propuestas {sheet*5+1:02}–{sheet*5+5:02} / A circular / B rectangular / Comparar las cotas, no el tamaño de la miniatura')
 for j in range(5):
  a,b=R[sheet*10+j*2:sheet*10+j*2+2];x=38+j*226;txt(a['code'][1:3],x,H-151,20,PINK,True);para(a['family'],x,H-163,210,12)
  for v,r in enumerate([a,b]):
   yy=H-425-v*288;img(r['code'],x,yy,215,220);txt(r['code']+' / '+f"{r['floor_m2']:.1f} m²",x,yy-16,11,INK,True)
 c.showPage()
for r in R:
 code=r['code'];base(code,'Tejido '+str(r['source'])+' → '+r['family'],'Trazabilidad / Izquierda: diagrama original de acciones / Derecha: huellas ajustadas y rutas')
 svg(code,25,130,1130,570,'TRAZA')
 para('Rosa discontinua a la derecha: desplazamiento desde el anclaje geométrico. Turquesa: conexiones físicas añadidas. El programa se consolida y las actividades privadas se repiten. La distribución resultante no conserva todas las distancias del grafo: el gráfico permite ver y discutir esa deformación.',45,120,1080,11)
 c.showPage()
 base(code,r['family'],'Planta / '+('A: colchón circular Ø2,10 m' if r['variant']=='A' else 'B: colchón rectangular 1,25 × 2,00 m')+' / Misma base de acciones, ajuste dimensional distinto')
 svg(code,20,60,805,650)
 x=852;y=H-158;w=300
 txt('4 HABITACIONES PRIVADAS',x,y,12,CYAN,True);y-=36;txt(f"{r['floor_m2']:.1f} m²",x,y,30,INK,True);y-=24
 y=para(f"Privado: {r['bedrooms_m2']:.1f} m²<br/>Común bruto, incluidos baños y recorridos: {r['shared_gross_m2']:.1f} m²",x,y,w,11)
 txt('DERIVACIÓN',x,y,11,CYAN,True);y=para(r['logic'],x,y-18,w,11)
 txt('AJUSTE RESPECTO AL GRAFO',x,y,11,PINK,True)
 ordered=sorted(r['displacements'].items(),key=lambda q:-q[1]);y=para('Mayores desplazamientos desde el anclaje escalado:<br/>'+' · '.join(k+': '+f'{v:.1f} m' for k,v in ordered[:4])+'.<br/>Un desplazamiento grande exige revisar la relación original.',x,y-18,w,10)
 txt('PRUEBA DE CONEXIÓN',x,y,11,CYAN,True);y=para(f"{r['connections']}/4 aproximaciones a dormitorios asociadas a una componente libre. Es una prueba parcial, sin validar puertas, maniobras, accesibilidad o evacuación. La continuidad de todo el suelo se comprueba aparte.",x,y-18,w,10)
 txt('CRÍTICA DE LA PROPUESTA',x,y,11,PINK,True);y=para(f"Diez unidades iguales ocuparían {r['floor_m2']*10:.0f} m² de suelo, antes de espacios generales. Supera el objetivo previo de 1.500 m². La red debe compactarse y transformarse en estancia; conservar cada ramal como corredor no resuelve la vivienda.",x,y-18,w,10)
 para('VERDE / privado · CREMA / suelo común<br/>LILA / baños y ropa · TURQUESA / equipos<br/>ROSA / textil, bisagra y estancia<br/>K cocinar · M comer · S conversar · T cortar/coser<br/>R reparar/guardar · D secar · E entrar/salir<br/>Cotas en metros; dibujo a escala variable.<br/>Ventanas propuestas; luz sin calcular.',x,y,w,9)
 c.showPage()
for half in range(2):
 base('C'+str(half+1),'Comparación de la segunda serie','Áreas conceptuales / El objetivo de este ensayo es reconocer las consecuencias de traducir el tejido')
 for t,x in [('CÓDIGO',40),('TEJIDO',125),('PROPUESTA',220),('SUELO m²',650),('RED PARCIAL',800),('MAYOR AJUSTE m',965)]:txt(t,x,H-157,10,CYAN,True)
 for j,r in enumerate(R[half*20:half*20+20]):
  y=H-185-j*26
  for t,x in [(r['code'],40),(str(r['source']),125),(r['family'],220),(f"{r['floor_m2']:.1f}",650),(str(r['connections'])+'/4',800),(f"{max(r['displacements'].values()):.1f}",965)]:txt(t,x,y,11)
 para('No hay selección de una vivienda ganadora. La serie muestra que copiar posiciones abstractas exige consolidar acciones, ajustar la escala y evitar que todas las conexiones se conviertan en superficie de paso.',42,100,1080,11)
 c.showPage()
c.save();print('PDF',N,'páginas')
with open(P/'datos/COMPARACION.csv','w',newline='') as f:
 writer=csv.writer(f);writer.writerow(['codigo','tejido','nombre','suelo_m2','privado_m2','comun_m2','conexion_parcial_4','max_desplazamiento_m'])
 for r in R:writer.writerow([r['code'],r['source'],r['family'],r['floor_m2'],r['bedrooms_m2'],r['shared_gross_m2'],r['connections'],max(r['displacements'].values())])
