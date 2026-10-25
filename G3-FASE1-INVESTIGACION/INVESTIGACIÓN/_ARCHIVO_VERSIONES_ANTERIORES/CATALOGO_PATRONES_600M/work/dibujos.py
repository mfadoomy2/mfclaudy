"""Diagramas vectoriales originales: relaciones observables, nunca levantamientos."""
import math
from xml.sax.saxutils import escape

class Drawing:
 def __init__(self,title):self.title=title;self.ops=[];self.w=515;self.h=205
 def line(self,x,y,X,Y,width=1,dash=False):self.ops.append(('line',(x,y,X,Y,width,dash)))
 def rect(self,x,y,w,h,width=1,fill=None):self.ops.append(('rect',(x,y,w,h,width,fill)))
 def circle(self,x,y,r,width=1,fill=None):self.ops.append(('circle',(x,y,r,width,fill)))
 def poly(self,pts,width=1,fill=None,closed=False):self.ops.append(('poly',(pts,width,fill,closed)))
 def text(self,x,y,s,size=9):self.ops.append(('text',(x,y,s,size)))
 def arrow(self,x,y,X,Y,s=None):
  self.line(x,y,X,Y,.8);a=math.atan2(Y-y,X-x)
  for v in [-.45,.45]:self.line(X,Y,X-5*math.cos(a+v),Y-5*math.sin(a+v),.8)
  if s:self.text(x,y-5,s)
 def hatch(self,x,y,w,h,gap=8):
  for t in range(0,int(w+h),gap):
   a=max(0,t-h);b=min(w,t)
   self.line(x+a,y+h-(t-a),x+b,y+h-(t-b),.35)
 def svg(self):
  a=[f'<svg xmlns="http://www.w3.org/2000/svg" width="515" height="205" viewBox="0 0 515 205"><title>{escape(self.title)}</title><rect width="515" height="205" fill="white"/>']
  for kind,v in self.ops:
   if kind=='line':
    x,y,X,Y,sw,dash=v;a.append(f'<line x1="{x}" y1="{y}" x2="{X}" y2="{Y}" stroke="black" stroke-width="{sw}"'+(' stroke-dasharray="3 3"' if dash else '')+'/>')
   elif kind=='rect':
    x,y,w,h,sw,fill=v;a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" stroke="black" stroke-width="{sw}" fill="{fill or "none"}"/>')
   elif kind=='circle':
    x,y,r,sw,fill=v;a.append(f'<circle cx="{x}" cy="{y}" r="{r}" stroke="black" stroke-width="{sw}" fill="{fill or "none"}"/>')
   elif kind=='poly':
    pts,sw,fill,closed=v;tag='polygon' if closed else 'polyline';a.append(f'<{tag} points="'+ ' '.join(f'{x},{y}' for x,y in pts)+f'" stroke="black" stroke-width="{sw}" fill="{fill or "none"}"/>')
   else:
    x,y,s,size=v;a.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="black">{escape(s)}</text>')
  return '\n'.join(a+['</svg>'])
 def draw(self,c,x,top,scale=1):
  c.saveState();c.translate(x,top);c.scale(scale,-scale)
  for kind,v in self.ops:
   c.setStrokeColorRGB(0,0,0);c.setFillColorRGB(0,0,0)
   if kind=='line':
    a,b,A,B,sw,dash=v;c.setLineWidth(sw);c.setDash(3,3) if dash else c.setDash();c.line(a,b,A,B);c.setDash()
   elif kind in ('rect','circle'):
    a,b,w,h,sw,fill=v if kind=='rect' else (*v[:3],None,*v[3:])
    c.setLineWidth(sw)
    if fill=='white':c.setFillColorRGB(1,1,1)
    if kind=='rect':c.rect(a,b,w,h,stroke=1,fill=bool(fill))
    else:c.circle(a,b,w,stroke=1,fill=bool(fill))
   elif kind=='poly':
    pts,sw,fill,closed=v;c.setLineWidth(sw);p=c.beginPath();p.moveTo(*pts[0])
    for pt in pts[1:]:p.lineTo(*pt)
    if closed:p.close()
    if fill=='white':c.setFillColorRGB(1,1,1)
    c.drawPath(p,stroke=1,fill=bool(fill))
   else:
    a,b,s,size=v;c.saveState();c.translate(a,b);c.scale(1,-1);c.setFont('Helvetica',size);c.drawString(0,0,s);c.restoreState()
  c.restoreState()

def windows(d,x,y,cols=3,rows=3,stepx=38,stepy=35,b=14,h=24,balcony=False):
 for r in range(rows):
  for q in range(cols):
   X=x+q*stepx;Y=y+r*stepy;d.rect(X,Y,b,h,.7)
   if balcony:
    d.line(X-4,Y+h+3,X+b+4,Y+h+3,1.2);d.line(X-4,Y+h-5,X+b+4,Y+h-5,.7)
    for z in range(-4,int(b)+5,4):d.line(X+z,Y+h-5,X+z,Y+h+3,.5)

def wall(d,x,y,w,h):d.rect(x,y,w,h,1.2)
def slats(d,x,y,w,h,gap=7):
 d.rect(x,y,w,h)
 for t in range(gap,int(h),gap):d.line(x,y+t,x+w,y+t,.5)
def label(d,x,y,s,tx,ty):d.arrow(x,y,tx,ty,s)
def make(kind):
 d=Drawing(kind)
 if kind=='streetwall':
  d.text(15,15,'PLANTA · borde de calle y piezas contiguas',10)
  for i,(w,h) in enumerate([(56,68),(82,100),(47,76),(74,91),(62,62)]):
   x=18+sum([56,82,47,74,62][:i]);d.rect(x,43,w,h);d.line(x,145,x+w,145,2)
   d.line(x+w/2,137,x+w/2,153,3)
  d.text(20,177,'CALLE');d.arrow(414,73,271,145,'alineación común');d.arrow(418,111,156,65,'fondos diferentes')
 elif kind=='setback':
  d.text(15,15,'SECCIONES COMPARADAS · relación con la acera',10)
  d.rect(32,43,56,107);d.line(10,150,227,150);d.line(88,150,88,169);d.text(28,188,'A. fachada sobre el borde')
  d.rect(325,43,67,107);d.line(263,150,500,150);d.line(440,110,440,150,2)
  for x in range(403,437,7):d.line(x,139,x+4,127,.6)
  d.arrow(464,59,440,123,'reja');d.text(278,188,'B. edificio / jardín / cerramiento / acera')
 elif kind=='skyline':
  d.text(15,15,'ALZADO · una cornisa distinta por pieza',10)
  heights=[70,124,91,143,112]
  for i,h in enumerate(heights):
   x=30+i*88;d.rect(x,165-h,88,h);d.line(x-2,165-h,x+90,165-h,2)
   windows(d,x+15,173-h,2,max(1,int((h-15)/29)),36,29,13,19)
  d.text(30,190,'La continuidad de la calle no exige una cota única de remate.')
 elif kind=='levels':
  d.text(15,15,'OSM · número de plantas declarado / 381 con dato',10)
  counts=[14,5,25,81,110,60,29,32,21,4]
  for i,n in enumerate(counts):
   x=24+i*47;h=n*.92;d.rect(x,149-h,25,h,.7,'black');d.text(x,166,str(i+1));d.text(x,141-h,str(n),8)
  d.text(20,188,'951 / 1.332 sin dato. No extrapolar esta distribución al conjunto.')
 elif kind=='rhythm':
  d.text(15,15,'ALZADO · seguir el eje, no el material del paño',10)
  d.rect(54,34,205,141);windows(d,77,44,4,3,47,40,16,27,True)
  for x in [85,132,179,226]:d.line(x,25,x,187,.6,True)
  d.arrow(379,63,180,75,'hueco alto');d.arrow(379,101,185,113,'balcón saliente');d.arrow(379,145,132,159,'eje repetido')
 elif kind=='rhythm_variants':
  d.text(15,15,'VARIANTES · no confundir eje de hueco y longitud de balcón',10)
  for off,continuous in [(30,False),(285,True)]:
   windows(d,off+10,53,3,2,54,59,21,38,not continuous)
   if continuous:
    for y in [89,148]:
     d.line(off,y,off+164,y);d.line(off,y+9,off+164,y+9,1.5)
     for x in range(off,off+165,8):d.line(x,y,x,y+9,.5)
  d.text(30,188,'Un hueco / una plataforma');d.text(285,188,'Varios huecos / borde continuo')
 elif kind=='dual_rhythm':
  d.text(15,15,'ALZADO · módulo doméstico y módulo comercial',10)
  d.rect(35,28,310,152);windows(d,55,40,6,2,49,40,17,26,True);d.line(35,124,345,124,1.8)
  for x,w in [(44,24),(82,96),(193,140)]:d.rect(x,135,w,45)
  d.arrow(381,65,263,74,'ejes superiores');d.arrow(380,141,190,127,'cambio de ritmo');d.text(48,196,'portal');d.text(105,196,'local');d.text(224,196,'local agrupado')
 elif kind=='threshold_section':
  d.text(15,15,'SECCIÓN ESQUEMÁTICA · capas independientes',10)
  d.rect(182,25,20,145);d.rect(160,28,86,8);d.line(220,34,220,91);d.line(140,99,242,99,2)
  d.line(182,119,105,143);d.line(15,171,486,171,1.5)
  d.arrow(340,53,220,68,'carpintería doméstica');d.arrow(340,109,168,146,'hueco del local');d.text(26,193,'calle');d.text(259,193,'interior');d.text(77,119,'toldo')
 elif kind=='plinth':
  d.text(15,15,'ALZADO · borde superior, juntas y encuentro con jambas',10)
  d.rect(25,30,295,140);d.line(25,111,320,111,1.8)
  for x in [65,120,240,292]:d.line(x,111,x,170,.8)
  d.line(25,142,320,142,.7);d.rect(145,58,68,112,1.5,'white')
  d.arrow(371,63,264,110,'remate de base');d.arrow(370,119,242,140,'junta de pieza');d.arrow(370,167,214,145,'interrupción en portal')
 elif kind=='slope':
  d.text(15,15,'ALZADO · la acera sube, los huecos no se deforman',10)
  d.line(27,179,472,117,2);d.line(27,108,472,108,1.3)
  for x in [60,154,248,342]:d.rect(x,62,58,66);d.line(x+7,69,x+7,119);d.line(x+22,69,x+22,119)
  d.arrow(374,41,355,109,'remate horizontal');d.text(30,198,'La altura visible del zócalo cambia con el suelo. Sin pendientes métricas.')
 elif kind=='render':
  d.text(15,15,'TRES SUPERFICIES · mismo contorno, distinta lectura',10)
  for x in [20,188,356]:d.rect(x,39,136,122)
  for j in range(80):d.circle(196+(j*37)%118,47+(j*23)%106,.5,.2,'black')
  for y in [69,99,129]:d.line(356,y,492,y,.5)
  for x,y in [(401,39),(447,69),(401,99),(447,129)]:d.line(x,y,x,y+30,.5)
  d.text(20,187,'liso aparente');d.text(188,187,'grano superficial');d.text(356,187,'surcos / juntas dibujadas')
 elif kind=='render_layers':
  d.text(15,15,'DESPIECE CONCEPTUAL · no confundir dibujo y construcción',10)
  for x,w,label_ in [(52,75,'soporte no visible'),(208,17,'revestimiento'),(368,5,'capa superficial')]:
   d.rect(x,44,w,105);d.text(x-7,176,label_)
  d.hatch(52,44,75,105);d.arrow(155,95,195,95);d.arrow(264,95,345,95)
  d.text(19,200,'Espesores y materiales no determinados por Street View.')
 elif kind=='brick':
  d.text(15,15,'PAÑO · la unidad es la pieza y su junta',10)
  x,y,w,h=25,43,270,119;d.rect(x,y,w,h)
  for row in range(7):
   Y=y+row*17;d.line(x,Y,x+w,Y,.6)
   for X in range(x+(0 if row%2==0 else 24),x+w,48):d.line(X,Y,X,min(Y+17,y+h),.6)
  d.arrow(365,58,180,76,'hilada');d.arrow(365,112,145,94,'junta vertical desplazada');d.text(25,189,'Trama ilustrativa: no certifica el aparejo completo ni la función portante.')
 elif kind=='brick_opening':
  d.text(15,15,'HUECO · paño, borde y carpintería son tres sistemas',10)
  d.rect(70,32,239,143)
  for y in range(45,170,14):d.line(70,y,309,y,.45)
  d.rect(133,65,110,110,1,'white');d.rect(143,75,90,100);d.line(188,75,188,175)
  for x in range(125,254,12):d.rect(x,48,10,17,.5,'white')
  d.arrow(365,69,221,54,'franja sobre hueco');d.arrow(365,119,235,120,'cerco');d.text(24,199,'El dibujo aísla el encuentro; el detalle resistente oculto queda sin asignar.')
 elif kind=='moulding':
  d.text(15,15,'ALZADO · repetición del borde dentro del paño',10)
  for x in [50,214,378]:
   d.rect(x,39,71,127);d.rect(x+8,48,55,118);d.line(x-8,37,x+79,37,2)
  d.text(35,193,'cerco continuo');d.text(194,193,'cambio de tono');d.text(353,193,'remate superior')
 elif kind=='moulding_section':
  d.text(15,15,'SECCIÓN DE BORDE · alternativas, no espesores medidos',10)
  for x,kind_ in [(64,0),(228,1),(395,2)]:
   d.rect(x,35,30,130);d.hatch(x,35,30,130)
   d.poly([(x+30,60),(x+45+kind_*6,60),(x+45+kind_*6,79),(x+30,79)],1,None)
   d.line(x+30,115,x+57,115)
  d.text(38,193,'cerco plano');d.text(195,193,'banda saliente');d.text(357,193,'perfil escalonado')
 elif kind=='balcony':
  d.text(15,15,'AXONOMETRÍA ESQUEMÁTICA · acceso, plataforma, protección',10)
  d.poly([(74,128),(240,128),(300,158),(134,158),(74,128)],1.4)
  d.poly([(74,84),(134,114),(300,114),(300,158)],1.1)
  for x in range(134,301,14):d.line(x,114,x,158,.7)
  d.rect(142,24,61,104);d.line(171,24,171,128)
  d.arrow(366,50,187,79,'puerta-ventana');d.arrow(368,103,231,129,'barandilla');d.arrow(365,168,237,158,'plataforma')
 elif kind=='balcony_plan':
  d.text(15,15,'PLANTA · un vuelo corto no es una galería común',10)
  d.line(20,75,229,75,2)
  for x in [42,124]:d.rect(x,75,60,31);d.line(x+8,74,x+48,74,3)
  d.poly([(288,60),(390,60),(390,141),(488,141)],2)
  d.poly([(288,90),(361,90),(361,171),(488,171)],1)
  d.text(27,191,'A. plataformas separadas');d.text(287,191,'B. continuidad al girar la esquina')
 elif kind=='grille':
  d.text(15,15,'ALZADO · el mismo marco admite tramas distintas',10)
  for x in [35,279]:
   d.rect(x,38,175,129,1.5)
   for X in range(x+12,x+175,19):d.line(X,38,X,167,.8)
   d.line(x,72,x+175,72);d.line(x,131,x+175,131)
  for x in [314,354,394,434]:d.circle(x,104,11,.7)
  d.text(35,194,'barrotes y travesaños');d.text(279,194,'trama + motivo curvo')
 elif kind=='grille_section':
  d.text(15,15,'SECCIÓN · tres planos que no deben confundirse',10)
  d.rect(73,40,36,121);d.rect(73,58,36,74,1,'white')
  d.line(95,61,95,131);d.line(126,54,126,140,2);d.line(104,63,126,63);d.line(104,132,126,132)
  d.arrow(257,54,96,94,'vidrio / carpintería');d.arrow(258,102,126,102,'reja delante del hueco');d.arrow(257,154,109,152,'espesor de muro no medido')
 elif kind=='door':
  d.text(15,15,'ALZADOS · hoja opaca y hoja con paños transparentes',10)
  for x in [54,302]:
   d.rect(x,28,115,150,1.5);d.rect(x+8,36,99,134);d.line(x+58,37,x+58,170)
  for x in [64,116]:
   d.poly([(x,64),(x+20,40),(x+43,64),(x+20,111),(x,64)],.7)
  for y in [63,87,112,139]:d.line(311,y,409,y)
  d.circle(156,113,3);d.circle(397,113,3)
  d.text(46,198,'Cabestreros: dibujo de rellenos');d.text(279,198,'Mediodía: vidrio y travesaños')
 elif kind=='door_plan':
  d.text(15,15,'PLANTA · marco, hoja y plano de acceso',10)
  d.rect(25,83,147,20);d.rect(312,83,175,20);d.line(172,93,172,175,2);d.line(312,93,260,153,2)
  d.line(172,93,250,93,.6,True);d.line(312,93,260,93,.6,True)
  d.arrow(75,37,170,98,'jamba');d.arrow(365,163,287,128,'hoja');d.text(110,200,'Giros ilustrativos: la apertura real no está verificada en la foto.')
 elif kind=='shutters':
  d.text(15,15,'SECUENCIA DEL MECANISMO · no secuencia temporal observada',10)
  for x,hh in [(30,119),(196,60),(362,17)]:
   d.rect(x,39,120,128);slats(d,x,39,120,hh,8)
  d.text(30,193,'cerrada');d.text(196,193,'parcialmente recogida');d.text(362,193,'hueco abierto')
 elif kind=='shutter_section':
  d.text(15,15,'SECCIÓN · cajón, guía y lamas',10)
  d.rect(84,40,75,40);d.circle(123,60,14);d.line(135,73,135,174,2);d.line(156,77,156,174,.5)
  d.arrow(255,56,126,61,'recogida superior');d.arrow(255,109,135,112,'paño de lamas');d.arrow(255,157,157,149,'guía lateral')
 elif kind=='awning':
  d.text(15,15,'SECCIÓN · no confundir faldón y plano inclinado',10)
  d.rect(115,29,19,147);d.line(134,67,320,122,2);d.line(134,116,302,122);d.line(320,122,320,145,1.4)
  d.line(25,176,484,176);d.arrow(363,53,230,96,'lona');d.arrow(365,153,320,133,'faldón');d.text(215,195,'proyección hacia la calle')
 elif kind=='awning_states':
  d.text(15,15,'ALZADO · rótulo, toldo y cierre permanecen separados',10)
  d.rect(78,33,305,138);d.rect(91,42,279,26);d.text(180,60,'RÓTULO',11)
  d.poly([(91,76),(370,76),(392,101),(69,101),(91,76)],1)
  d.rect(69,101,323,12);slats(d,97,115,267,56,8)
  d.text(78,195,'El cierre puede estar bajado aunque el toldo esté desplegado.')
 elif kind=='color_fields':
  d.text(15,15,'MAPA DE POSICIONES · sin extraer colores absolutos',10)
  d.rect(47,30,300,141);d.line(47,136,347,136,1.5)
  for x in [74,160,247]:d.rect(x,48,55,68);d.rect(x+7,55,41,61)
  d.rect(159,142,135,29);d.text(63,127,'PAÑO');d.text(60,157,'BASE');d.text(188,161,'LOCAL')
  d.arrow(387,51,165,72,'cerco');d.arrow(387,98,285,99,'metal');d.text(44,197,'El color se describe por su función visual y su posición.')
 elif kind=='color_order':
  d.text(15,15,'COMPARACIÓN · mismo orden, combinaciones diferentes',10)
  names=['paño','cerco','metal','base','local']
  for j,(a,b) in enumerate([('rojizo','ocre'),('claro','claro'),('oscuro','oscuro'),('oscura','gris'),('naranja','azul')]):
   y=48+j*28;d.text(21,y,names[j]);d.line(105,y-4,495,y-4,.3);d.text(161,y-8,a);d.text(362,y-8,b)
  d.text(155,200,'Amparo');d.text(357,200,'Rodas')
 elif kind=='services':
  d.text(15,15,'ALZADO · una red añadida atraviesa el orden de huecos',10)
  d.rect(26,30,300,140);windows(d,48,46,4,1,65,40,31,55)
  for yy in [114,118,122]:d.line(27,yy,309,yy,.6)
  d.line(205,118,205,169,2);d.rect(96,121,28,19);d.rect(273,71,42,31)
  d.arrow(373,54,294,81,'aparato');d.arrow(373,116,239,118,'haz horizontal');d.arrow(373,167,205,151,'tubo vertical')
 elif kind=='services_layers':
  d.text(15,15,'DESPIECE · acabado / fijación / instalación',10)
  d.rect(65,33,37,128);d.hatch(65,33,37,128);d.line(138,37,138,163,3)
  for y in [63,128]:d.line(102,y,138,y,1);d.circle(138,y,5,.7)
  d.arrow(251,57,104,82,'superficie soporte');d.arrow(250,113,126,128,'sujeción visible');d.arrow(250,161,140,152,'elemento añadido')
 elif kind=='paving':
  d.text(15,15,'PLANTA · piezas grandes en el borde, pequeñas en el centro',10)
  for x,w,gap in [(20,92,25),(112,284,13),(396,93,25)]:
   d.rect(x,35,w,139)
   for y in range(35,175,gap):d.line(x,y,x+w,y,.35)
   for X in range(x,x+w,gap*2):d.line(X,35,X,174,.35)
  for y in [57,98,145]:d.circle(105,y,3,1,'black');d.circle(403,y,3,1,'black')
  d.rect(364,114,25,35)
  for y in range(118,147,5):d.line(367,y,386,y)
  d.text(22,197,'borde');d.text(210,197,'calzada');d.text(398,197,'borde')
 elif kind=='street_sections':
  d.text(15,15,'SECCIONES · cambios de cota y de anchura',10)
  d.poly([(27,48),(27,87),(108,87),(108,98),(369,98),(369,87),(484,87),(484,48)],1.5)
  d.poly([(27,141),(27,178),(141,178),(369,178),(484,178),(484,141)],1.5)
  for x in [104,374]:d.line(x,150,x,177,2)
  d.text(193,73,'bordillo + calzada');d.text(177,161,'banda marcada por bolardos')
 elif kind=='green':
  d.text(15,15,'TRES SOPORTES · no confundirlos al contar',10)
  for x in [79,253,427]:d.line(x,91,x,149,2);d.circle(x,68,32)
  d.line(26,150,135,150);d.rect(222,123,62,28);d.poly([(404,134),(450,134),(442,162),(412,162),(404,134)],1)
  d.text(41,190,'árbol en alcorque');d.text(222,190,'jardinera');d.text(411,190,'maceta')
 elif kind=='green_section':
  d.text(15,15,'SECCIÓN DE CALLE · copa, estancia y paso comparten espacio',10)
  d.line(20,173,492,173);d.line(205,85,205,172,2);d.circle(205,58,44)
  d.rect(268,137,67,7);d.line(277,144,277,172);d.line(326,144,326,172)
  d.arrow(373,53,245,71,'copa visible');d.arrow(375,110,317,139,'mobiliario');d.text(22,191,'La sombra dibujada no es un estudio solar anual.')
 elif kind=='threshold_plan':
  d.text(15,15,'PLANTA · el objeto ocupa una posición respecto del acceso',10)
  d.line(18,85,164,85,2);d.line(239,85,494,85,2);d.line(164,85,164,32,1.5)
  d.rect(263,104,43,36);d.rect(333,92,74,15);d.line(17,176,495,176,.6,True)
  d.arrow(191,159,191,65,'acceso');d.arrow(435,134,306,124,'objeto');d.text(30,59,'interior');d.text(45,155,'acera');d.text(334,198,'paso por verificar')
 elif kind=='objects':
  d.text(15,15,'EXPOSICIÓN · tres formas de relacionarse con el borde',10)
  for x in [77,255,425]:d.line(x,36,x,158,1.5);d.line(x-57,159,x+55,159)
  d.rect(79,57,31,71);d.line(246,102,279,102);d.line(246,102,246,151);d.line(279,102,279,151);d.line(246,102,246,77)
  d.rect(429,46,37,84);d.line(416,35,416,159,.5)
  d.text(27,191,'pieza apoyada');d.text(210,191,'mueble exento');d.text(376,191,'detrás del vidrio')
 elif kind=='repair':
  d.text(15,15,'ALZADO · el parche corta la regularidad del paño',10)
  d.rect(28,33,296,135)
  for y in [76,119]:d.line(28,y,324,y,.4)
  pts=[(57,126),(82,108),(100,115),(124,95),(141,110),(172,106),(182,131),(215,136),(197,158),(145,152),(120,162),(81,153),(57,126)]
  d.poly(pts,1);d.hatch(91,121,63,27,7)
  d.arrow(372,54,134,100,'borde irregular');d.arrow(372,115,216,137,'cambio de superficie');d.text(26,195,'Se describe la huella visible; no se diagnostica su causa.')
 elif kind=='repair_layers':
  d.text(15,15,'COMPARACIÓN · tres fenómenos, tres soportes',10)
  for x in [27,196,364]:d.rect(x,42,124,119)
  d.poly([(45,115),(70,88),(87,107),(122,101),(130,133)],1)
  d.rect(215,82,79,61,.7);d.hatch(215,82,79,61,11)
  slats(d,364,42,124,119,10);d.poly([(381,124),(400,61),(418,121),(453,69),(473,132)],2)
  d.text(27,189,'pérdida de acabado');d.text(196,189,'repinte / parche');d.text(364,189,'escritura sobre cierre')
 elif kind=='patio':
  d.text(15,15,'PLANTAS TIPOLÓGICAS · corredor alrededor del vacío',10)
  for x in [26,281]:
   d.rect(x,39,185,127);d.rect(x+33,66,119,73);d.rect(x+24,57,137,91,.6)
   d.text(x+71,106,'PATIO',10)
  d.rect(338,141,76,27,0,'white');d.line(338,141,338,166);d.line(414,141,414,166)
  d.text(30,192,'O · perímetro cerrado');d.text(283,192,'U · lado abierto / interrumpido')
 elif kind=='gallery_section':
  d.text(15,15,'SECCIÓN · habitación / galería / vacío',10)
  for y in [67,132,180]:d.line(31,y,291,y,1.5)
  d.line(178,28,178,180,2);d.line(288,27,288,180,1.5)
  for y in [39,103,151]:d.line(288,y,288,y+27,3);d.line(185,y+20,283,y+20,.5)
  d.text(34,198,'interior');d.text(196,198,'galería');d.text(358,198,'vacío del patio');d.arrow(398,76,245,129,'recorrido común')
 elif kind=='timber':
  d.text(15,15,'ENCUENTRO · piezas visibles del borde del patio',10)
  d.rect(59,36,270,16,1.3);d.rect(113,52,18,112,1.3);d.rect(260,52,18,112,1.3)
  d.poly([(88,52),(113,78),(113,91),(76,52)],1,None,True);d.poly([(131,78),(155,52),(168,52),(131,91)],1,None,True)
  d.rect(107,164,30,16);d.rect(254,164,30,16)
  d.arrow(373,39,233,44,'carrera');d.arrow(373,90,140,77,'tornapunta');d.arrow(373,129,124,130,'pie derecho');d.arrow(373,174,124,174,'basamento')
 elif kind=='timber_infill':
  d.text(15,15,'MODELO DOCUMENTAL · entramado y relleno colaboran',10)
  for x,filled in [(35,True),(293,False)]:
   d.rect(x,44,175,120);d.line(x,104,x+175,104,5);d.line(x+85,44,x+85,164,5)
   if filled:
    d.hatch(x+5,50,75,48,9);d.hatch(x+92,110,77,48,9)
   for X in [x+20,x+85,x+148]:d.arrow(X,22,X,41)
  d.text(25,192,'muro compuesto con cuarteles');d.text(281,192,'pórtico sin relleno: no equivalente')
 elif kind=='filter':
  d.text(15,15,'SECCIÓN · vidrio y filtro no están en el mismo plano',10)
  d.rect(51,33,23,134);d.line(158,33,158,167,1);d.line(274,33,274,167,2)
  for y in range(38,163,13):d.line(264,y,284,y+6,1)
  d.line(74,168,291,168,1.5);d.arrow(377,58,160,69,'vidrio');d.arrow(377,111,275,110,'filtro');d.text(90,194,'profundidad intermedia, sin dimensión medida')
 elif kind=='filter_states':
  d.text(15,15,'ESTADOS DE UNA SEGUNDA PIEL · lectura del mecanismo',10)
  for x,state in [(32,0),(202,1),(372,2)]:
   d.rect(x,43,106,119);d.line(x+53,43,x+53,162)
   if state==0:slats(d,x,43,106,119,9)
   elif state==1:
    slats(d,x,43,53,119,9);d.poly([(x+53,43),(x+97,61),(x+97,177),(x+53,162)],1)
   else:
    d.poly([(x,43),(x-17,54),(x-17,173),(x,162)],1);d.poly([(x+106,43),(x+123,54),(x+123,173),(x+106,162)],1)
  d.text(31,195,'cerrado');d.text(201,195,'posición intermedia');d.text(371,195,'abierto')
 elif kind=='market':
  d.text(15,15,'PUESTO · esquema basado en la descripción municipal [D4]',10)
  d.poly([(76,62),(222,62),(286,94),(140,94),(76,62)],1.3)
  for x,y in [(76,62),(222,62),(286,94),(140,94)]:d.line(x,y,x,y+85,1.5)
  d.poly([(76,110),(222,110),(286,142),(140,142),(76,110)],.8)
  d.text(46,186,'largo: 1-3 m');d.text(219,186,'fondo: 1 o 2 m');d.arrow(380,56,222,85,'tubo desmontable');d.text(337,121,'altura total ≤ 2,5 m')
 elif kind=='market_time':
  d.text(15,15,'TIEMPO DOCUMENTADO [D5] · no observado como secuencia',10)
  for x,w,s in [(25,76,'8-9 h'),(113,270,'9-15 h'),(397,87,'15-16 h')]:d.rect(x,65,w,46);d.text(x+12,92,s,11)
  d.text(29,136,'montaje');d.text(208,136,'venta');d.text(402,136,'retirada')
  d.line(24,164,485,164);d.text(27,193,'Domingos y festivos. La calle laborable no demuestra por sí sola este ciclo.')
 elif kind=='oldnew':
  d.text(15,15,'ALZADO ABSTRACTO · discontinuidad conservada',10)
  pts=[(24,166),(24,75),(52,75),(59,57),(74,62),(88,37),(130,41),(146,50),(177,44),(189,81),(221,85),(221,166)]
  d.poly(pts,1.5,None,True)
  for y in range(88,164,13):d.line(30,y,212,y,.35)
  d.rect(242,87,242,79);windows(d,265,103,4,1,51,30,26,36)
  d.arrow(301,36,221,117,'junta visual / separación');d.text(31,193,'fábrica conservada');d.text(279,193,'volumen de intervención')
 elif kind=='oldnew_section':
  d.text(15,15,'SECCIÓN CONCEPTUAL · materia antigua y nuevo uso',10)
  d.rect(80,29,30,139);d.hatch(80,29,30,139,7);d.rect(384,44,26,124);d.hatch(384,44,26,124,7)
  d.line(120,77,374,77,3);d.line(120,83,374,83,.5)
  d.line(52,170,445,170,1.5);d.rect(166,131,112,6);d.line(177,137,177,169);d.line(264,137,264,169)
  d.arrow(202,32,115,68,'relación entre borde y cubierta');d.text(130,196,'No es el detalle construido de Escuelas Pías.')
 elif kind=='perforation':
  d.text(15,15,'DOS MATRICES · celda hexagonal y taladro circular',10)
  for row in range(4):
   for col in range(6):
    cx=35+col*29+(14.5 if row%2 else 0);cy=53+row*24
    pts=[(cx+15*math.cos(a*math.pi/3),cy+15*math.sin(a*math.pi/3)) for a in range(6)];d.poly(pts,.7,None,True)
  for row in range(6):
   for col in range(4):d.circle(313+col*28,42+row*23,5,.7)
  d.text(20,187,'banda alta · Cebada');d.text(288,187,'franja vertical · Martín de Vargas')
 elif kind=='perforation_section':
  d.text(15,15,'DETALLE ANALÍTICO · hueco / nervio / repetición',10)
  d.rect(59,40,154,114)
  for x in [80,119,158,197]:
   for y in [59,98,137]:d.circle(x,y,11)
  d.arrow(308,58,92,59,'nervio entre huecos');d.arrow(308,108,158,98,'hueco');d.arrow(308,161,120,137,'paso de repetición')
 else:raise KeyError(kind)
 return d

TITLES={
 'streetwall':'La alineación y la parcela son órdenes diferentes','setback':'Tres límites posibles: fachada, jardín y reja','skyline':'Lectura de remates sin inventar alturas','levels':'Distribución declarada y datos ausentes',
 'rhythm':'Qué significa aquí «modulación»','rhythm_variants':'La variante que agrupa varios huecos','dual_rhythm':'Desfase entre huecos superiores y planta baja','threshold_section':'Las capas no comparten profundidad',
 'plinth':'El zócalo se identifica por sus encuentros','slope':'La pendiente cambia su altura expuesta','render':'Distinguir textura y dibujo de juntas','render_layers':'El revestimiento no revela el soporte',
 'brick':'Aislar la escala de la pieza','brick_opening':'Leer el encuentro alrededor del hueco','moulding':'El cerco repite el borde','moulding_section':'El relieve se entiende en sección',
 'balcony':'Descomposición de un balcón','balcony_plan':'Individual y corrido no son equivalentes','grille':'Descomposición de la trama','grille_section':'Reja delante de la carpintería',
 'door':'Comparar las hojas, no solo el color','door_plan':'El portal en planta','shutters':'Un cierre con varios estados','shutter_section':'Cómo se recoge el paño',
 'awning':'El toldo tiene espesor y proyección','awning_states':'Relación con rótulo y persiana','color_fields':'Distribución del color en la fachada','color_order':'Comparación de posiciones cromáticas',
 'services':'Cruce de dos tramas','services_layers':'La instalación se añade al soporte','paving':'Las bandas se leen en planta','street_sections':'La sección permite distinguirlas',
 'green':'Comparación de soportes vegetales','green_section':'Relación entre copa, paso y estancia','threshold_plan':'Localizar la ocupación del umbral','objects':'Tres posiciones de exposición',
 'repair':'La huella irregular sobre el paño regular','repair_layers':'Procesos distintos, no una causa común','patio':'El vacío organiza el recorrido','gallery_section':'La galería como espesor compartido',
 'timber':'Nombrar cada pieza visible','timber_infill':'No borrar el papel del relleno [D2]','filter':'Dos planos y una distancia','filter_states':'El movimiento cambia la permeabilidad',
 'market':'Estructura y módulo documentados','market_time':'Secuencia oficial, no simulación observada','oldnew':'Lo conservado y lo añadido','oldnew_section':'Relación espacial, no reconstrucción técnica',
 'perforation':'La repetición dentro de una celosía','perforation_section':'Las tres variables geométricas'
}
