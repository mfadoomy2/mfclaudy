from pathlib import Path
import ast, json, sqlite3, shutil, hashlib
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT=Path('/Volumes/T7/G3 Proyectos/INVESTIGACIÓN')
BASE=Path(__file__).parent
OUT=Path('/Users/adam/Documents/Codex/2026-09-21/crr/outputs')
OUT.mkdir(exist_ok=True)
W,H=595.276,841.89
def literal(file,name):
 for n in ast.parse(file.read_text()).body:
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets):return ast.literal_eval(n.value)
CATS=literal(ROOT/'ETIQUETAS_Y_DXF_QGIS.py','CATEGORIAS')
OLD=literal(ROOT/'TODAS_COORDENADAS_FISICAS_QGIS.py','theme_colors')
conn=sqlite3.connect('file:'+str(ROOT/'QGIS_ETIQUETADO/INVENTARIO_ETIQUETADO.gpkg')+'?mode=ro',uri=True)
COUNTS={t:dict(conn.execute(f'SELECT cat_codigo,count(*) FROM {t} GROUP BY cat_codigo')) for t in ['puntos_fisicos','lineas_fisicas','poligonos_fisicos']}

class Doc:
 def __init__(self,name,title):
  self.path=BASE/name;self.c=canvas.Canvas(str(self.path),pagesize=(W,H));self.c.setTitle(title);self.c.setAuthor('Investigación G3');self.n=0;self.text=[]
 def page(self,title,sub=''):
  if self.n:self.c.showPage()
  self.n+=1;self.c.setFillColor(colors.black);self.c.setFont('Times-Roman',9)
  self.c.drawString(42,809,'RIBERA DE CURTIDORES / INVESTIGACIÓN G3');self.c.drawRightString(553,28,str(self.n))
  self.y=777;self.p(title,20,24,True);self.y-=6
  if sub:self.p(sub,10,13);self.y-=8
  self.c.bookmarkPage('p'+str(self.n));self.c.addOutlineEntry(title,'p'+str(self.n),0)
  self.text+=['\n# '+title+'\n']
 def p(self,s,size=11,leading=14,bold=False,x=42,width=511,gap=7):
  sty=ParagraphStyle('s',fontName='Times-Bold' if bold else 'Times-Roman',fontSize=size,leading=leading,textColor=colors.black)
  p=Paragraph(s,sty);_,h=p.wrap(width,1000)
  if self.y-h<49:raise ValueError((self.path.name,self.n,'overflow',self.y,h,s[:50]))
  p.drawOn(self.c,x,self.y-h);self.y-=h+gap;self.text.append(s+'\n')
 def section(self,title,body):
  self.p(title,12,15,True,gap=5);self.p(body)
 def save(self):
  self.c.save();shutil.copy2(self.path,OUT/self.path.name)
  self.path.with_suffix('.md').write_text('\n'.join(self.text),encoding='utf-8')
  return dict(file=str(self.path),pages=self.n)

d=Doc('EXPLICACION_DIAGRAMAS_Y_80_PREGUNTAS.pdf','Diagramas explicados y 80 preguntas de proyecto')
d.page('Qué significa cada diagrama','Guía de lectura del catálogo «Ribera de Curtidores. Patrones y materia», de 58 páginas. Las referencias de página remiten a ese catálogo, que se conserva sin modificaciones.')
d.section('1. Mapa de apertura / página 1','Sitúa el recorrido de observación cerca de Ribera. Los números identifican posiciones de cámara; una misma posición permite mirar varios frentes. La cruz señala la referencia aproximada de Ribera 31. Los contornos finos son edificios de la base cartográfica; la línea negra sigue el eje seleccionado de la calle. El norte orienta el mapa y la barra permite medir 100 m en su escala de impresión.')
d.p('Sirve para responder «¿dónde están los casos que comparo?». No sitúa cada balcón con precisión de levantamiento. Una cámara en la calle y el elemento que se ve desde ella ocupan posiciones distintas.')
d.section('2. Tejido, frente y pieza / página 2','Las tres filas proponen cambiar de escala. <b>Tejido:</b> relación del edificio con calle, alturas y actividades. <b>Frente:</b> organización de huecos, base y capas exteriores. <b>Pieza:</b> encuentro entre bastidor, junta, superficie y acceso para cuidarla. Las flechas indican un recorrido de análisis, no una conexión física ni una relación causal demostrada.')
d.p('Ejemplo: la presencia de comercio cercano plantea un uso en planta baja; ese uso requiere un acceso; el acceso obliga a resolver puerta, umbral y junta. El interés es que una decisión urbana llegue hasta un detalle concreto.')
d.section('3. Mapas pequeños de cada familia','Aparecen en las páginas 7, 12, 19, 25, 29, 36, 40 y 45. Repiten el mismo territorio para localizar únicamente los casos de esa familia. La lista relaciona número de estación, captura RC/SV y frente B. Los saltos de numeración son normales: las estaciones conservan el mismo número en todo el catálogo.')
d.section('4. Códigos y llamadas sobre las fotografías','<b>B:</b> frente identificado. <b>RC / SV:</b> captura o posición de cámara. <b>F01-F33:</b> fotografías de campo. <b>01-08:</b> familias de patrones. La llamada 1 señala el componente comentado en cada fotografía; no es una cantidad. D1 y D2 son las dos comparaciones dibujadas en cada familia.')
d.p('Las 64 fichas corresponden a observaciones de 18 frentes. Un frente puede aparecer en varias familias: por ejemplo, por su balcón, su base y su comercio. Los mapas tienen escala métrica; los esquemas de fachada no están acotados.')

d.page('A1 y A2, explicados paso a paso')
d.section('A1. La repetición doméstica dentro del tejido / página 4','<b>Qué muestra.</b> Dos gráficos: un mapa de edificios y un recuento de las plantas registradas. La franja analizada se extiende 100 m a cada lado del eje seleccionado. Contiene 115 polígonos de edificio: 19 tienen el atributo de plantas y 96 no lo tienen.')
d.p('<b>Cómo leer las barras.</b> El número de la izquierda es el número de plantas; el de la derecha, cuántos polígonos declaran ese valor: 4 plantas, 7 casos; 5 plantas, 6; 6 plantas, 4; 7 plantas, 1; 9 plantas, 1. Las barras no representan metros de altura. Los 17 casos de cuatro a seis plantas pertenecen a los 19 con información, no a los 115 del conjunto.')
d.p('<b>Qué significa el blanco grisáceo.</b> En los edificios de la franja, significa que falta ese atributo en la base OSM utilizada. No significa que el edificio sea bajo, uniforme o imposible de contar. No se hizo un recuento visual de esas 96 piezas. Los edificios exteriores a la franja sirven de contexto y tampoco deben leerse como una muestra de alturas.')
d.p('<b>Para qué sirve.</b> Localiza la información disponible y plantea comparar alturas vecinas. Con esta cobertura no permite afirmar cuál es la altura dominante de todo el entorno. El perfil de cornisas de la ficha «Cornisas escalonadas y alturas diferentes» del catálogo de 600 m muestra otra cosa: la relación visual entre remates altos y bajos. Ese perfil se entiende como comparación de siluetas, no como una medición en metros. Aquí no se completa el recuento de alturas.')
d.section('A2. La identidad aparece en la combinación / página 8','<b>En una frase:</b> sirve para ver qué rasgos se han estudiado juntos en una misma fachada, en vez de estudiar cada rasgo por separado.')
d.p('<b>Cómo leerlo.</b> Cada fila B es un frente. Las columnas 01-08 son hueco, base, reja, textil, local, cable, huella y acabado. Un punto significa «este frente se incluyó como ejemplo de esta familia». Una casilla vacía significa «no se codificó esa relación en las fichas», no «ese elemento no existe».')
d.p('<b>Ejemplo real.</b> B05 tiene punto en las ocho columnas: ese frente aparece en las ocho familias. B08 tiene puntos en 01, 04 y 05: se usó para hablar de huecos/balcones, textiles y comercio. No se puede concluir que B08 carezca de rejas, cableado o acabados.')
d.p('<b>La idea útil.</b> Si la misma fachada combina exposición comercial, toldo y acceso, la propuesta puede resolver esas tres cosas mediante un mismo borde. Seis frentes están incluidos a la vez en hueco y base; tres en comercio y huella. Son coincidencias de la selección, no frecuencias medidas de todo el barrio. El título expresa una interpretación: el gráfico, por sí solo, no demuestra una identidad urbana ni relaciones de causa.')

d.page('A3, A4 y A5: intención y alcance')
d.section('A3. Una fachada, varias capas de uso / página 26','<b>Qué intentaba explicar.</b> Separar cuatro cosas visibles en B07/RC06: la pared con su hueco, la carpintería, la barandilla y la tela. La pared define una abertura; la carpintería la cierra; la barandilla forma un límite protector; la tela puede variar con el uso.')
d.p('<b>Por qué cuesta entenderlo.</b> Las piezas se desplazan sin una posición ensamblada de referencia ni líneas de correspondencia suficientes. El dibujo no permite reconstruir dónde encaja cada elemento. Por tanto, no sirve como axonometría explotada rigurosa ni como explicación de un montaje. La afirmación del pie de que conserva la relación entre las piezas no queda suficientemente justificada por el dibujo.')
d.p('<b>Qué sí puede retenerse.</b> La pregunta sobre qué permanece fijo, qué regula cada residente y qué necesita gestión colectiva. La fotografía respalda la presencia visible de las capas; no documenta sus anclajes, espesores o secuencia constructiva. El catálogo queda intacto. Un detalle ajeno encontrado en internet podría servir como referencia identificada, pero no demostraría cómo se construyó esta fachada.')
d.section('A4. Objetos, oficios y planta baja / página 30','<b>Mapa:</b> reúne 112 registros cartográficos de comercio u oficio dentro de la franja. Los 28 puntos negros son 14 antigüedades, 7 muebles, 4 enmarcaciones y 3 oficios. Los círculos blancos son otros registros comerciales. La selección del código también admite segunda mano y coleccionismo, pero aquí no aportan registros a ese recuento.')
d.p('<b>Cadena de flechas:</b> recibir, reparar, mostrar y guardar propone funciones para ensayar en el edificio. No representa una ruta real entre tiendas ni demuestra que los negocios trabajen juntos. Tampoco prueba que cada negocio siga abierto hoy. La relación de proyecto es concreta: si entran objetos, habrá que decidir por dónde llegan, dónde se trabaja con ellos y dónde se almacenan.')
d.section('A5. La repetición también organiza el mantenimiento / página 41','<b>Tabla:</b> para cada componente propone una acción, una forma de acceder y un encuentro a resolver. Ejemplo: si el zócalo se organiza por piezas, interesa poder retirar una sin desmontar toda la base. Es un criterio de diseño, no una técnica de fijación verificada en los edificios fotografiados.')
d.p('<b>Dibujo inferior:</b> la retícula representa una serie de piezas; el hueco discontinuo señala la posición de una de ellas; la pieza desplazada y la flecha explican su sustitución individual. No hay una escala ni un mecanismo constructivo especificado. Para convertirlo en detalle haría falta dibujar soporte, junta, fijación, acceso y tolerancias reales.')

d.page('Las comparaciones D1 y D2 / familias 01-04','Cada pareja aísla una diferencia visible. Los esquemas simplifican contornos; no sustituyen un levantamiento ni prueban sistemas constructivos ocultos.')
d.section('01. Hueco vertical y balcón / página 7','<b>D1, B05:</b> varios huecos se ordenan en ejes verticales y cada uno tiene un balcón individual. Los rectángulos altos representan puertas-ventana; los pequeños planos de barras, barandillas. <b>D2, B08:</b> la barandilla se prolonga delante de varios huecos y forma una banda continua. La diferencia es «una pieza por abertura» frente a «un borde que agrupa aberturas».')
d.p('<b>Decisión que abre:</b> ¿se quiere un exterior individual, un espacio compartido o solo una imagen continua? Una barandilla visualmente corrida no demuestra que los vecinos puedan circular por toda ella ni que la propiedad sea colectiva.')
d.section('02. Basamento / página 12','<b>D1, B13:</b> una franja baja recorre la pared y se interrumpe al llegar a la puerta. <b>D2, B02:</b> el revestimiento por piezas sube a gran parte de la planta baja. Las líneas interiores representan juntas o subdivisiones visibles, no capas internas del muro.')
d.p('<b>Decisión que abre:</b> elegir qué parte de la pared recibe contacto, roces y limpieza: solo el arranque o toda la altura de acceso. El interés está en el encuentro entre piezas, puerta y suelo, no únicamente en escoger una textura.')
d.section('03. Cerrajería / página 19','<b>D1, B02:</b> combina una zona de barras con un faldón inferior ciego. <b>D2, B09:</b> organiza el cierre del portal mediante un bastidor y subdivisiones enrejadas. Las barras dejan ver parcialmente; el paño ciego tapa la parte baja. Ninguno de los dibujos acredita que el cierre cumpla una prestación de seguridad concreta.')
d.p('<b>Decisión que abre:</b> graduar visibilidad e intimidad. Se puede comparar qué deja ver cada cierre desde la acera y qué ocurre de noche, sin confundir transparencia con libre acceso.')
d.section('04. Textiles / página 25','<b>D1, B13:</b> la protección se ajusta a un único hueco. <b>D2, B08:</b> una franja textil organiza varios huecos a la vez. Los trazos oblicuos describen la presencia y el contorno del textil; no son un cálculo solar ni el mecanismo de un toldo.')
d.p('<b>Decisión que abre:</b> qué regula cada vivienda y qué regla común fija posiciones, dimensiones o recogida. Para afirmar cuánta sombra produce una opción hacen falta orientación, geometría, fecha y hora de cálculo.')

d.page('Las comparaciones D1 y D2 / familias 05-08')
d.section('05. Comercio y vitrina / página 29','<b>D1, B09:</b> pequeños rectángulos representan la ocupación visual del escaparate por objetos. <b>D2, B05:</b> la abertura de acceso se relaciona con un pequeño apoyo exterior. Se contrasta mostrar tras un límite con extender parte de la actividad hasta el umbral. Los rectángulos no son un inventario exacto de productos ni un plano de estanterías.')
d.p('<b>Decisión que abre:</b> dónde termina la exposición y por dónde se entra. Un proyecto puede separar el paso de residentes, la manipulación de objetos y la zona visible desde la calle.')
d.section('06. Instalaciones / página 36','<b>D1, B09:</b> recorrido horizontal, caja y bajada. <b>D2, B13:</b> recorrido que cambia de dirección y se relaciona con un hueco. Las ventanas son referencias para situar el tendido; las líneas representan recorridos visibles sobre la pared. No identifican por sí solas electricidad, telefonía u otro servicio.')
d.p('<b>Decisión que abre:</b> reservar caminos registrables para instalaciones, especialmente donde cambian de dirección o se conectan a locales. No es necesario reproducir el trazado observado para aprender de sus puntos de acceso y acumulación.')
d.section('07. Huella sobre la superficie / página 40','<b>D1, B14:</b> un trazo atraviesa las líneas horizontales de un cierre laminado. <b>D2, B13:</b> atraviesa una superficie dividida en placas. El trazo es un símbolo de inscripción, no una copia exacta del grafiti. La pareja compara el dibujo que queda encima y el soporte que sigue debajo.')
d.p('<b>Decisión que abre:</b> si interesa limpiar, asumir la transformación, habilitar una superficie acordada o sustituir una pieza. Una imagen no demuestra qué producto limpiador funciona ni cuál será el desgaste futuro.')
d.section('08. Fondo, borde y base / página 45','<b>D1, B03:</b> las bandas y bordes claros destacan sobre el campo de ladrillo. <b>D2, B10:</b> el recercado destaca alrededor del hueco sobre un fondo más continuo. Se compara el orden que agrupa plantas o piezas con el que enmarca cada abertura.')
d.p('<b>Decisión que abre:</b> decidir qué se quiere hacer legible: la unidad doméstica, una franja común o una pieza sustituible. Las líneas no prueban dónde están pilares o forjados, y el contraste fotográfico no es una medición calibrada de color.')

d.page('Del análisis a una pregunta de proyecto')
d.section('Tiempo y uso / página 51','Las dos fotografías comparan un comercio abierto y un cierre gráfico de otro local. La primera muestra acceso y exposición; la segunda, la superficie que queda hacia la calle al cerrar. No son un antes y un después del mismo establecimiento. La cuestión de proyecto es cómo cambia el borde cuando una actividad se detiene y qué acceso debe seguir funcionando.')
d.section('Texturas y síntesis / páginas 9-50 y 52','Las fotografías de texturas son observaciones de superficie, junta, contacto o desgaste. Su número F identifica el archivo, no una ubicación medida. La página 52 reúne cinco líneas de decisión; es una síntesis argumental, no un gráfico estadístico. Las páginas 53-58 permiten rastrear capturas, frentes y fuentes.')
d.section('Qué convierte una pregunta en motor','Una pregunta útil enfrenta dos necesidades concretas y permite dibujar alternativas. «¿Cómo integrar el edificio?» es demasiado amplia. «¿Cómo dar al barrio una planta baja compartida sin atravesar el acceso privado?» ya permite comparar plantas, horarios y filtros.')
d.p('<b>Modo de trabajo:</b> elegir una pregunta central; vincularla a dos observaciones; producir dos alternativas con el mismo programa; compararlas mediante una planta y una sección; fijar un criterio para decidir. Las 80 preguntas siguientes son posibilidades de proyecto, no actividades ya demostradas ni obligaciones añadidas al enunciado.')
d.section('Tres motores especialmente ligados a este material','<b>Objeto y domesticidad:</b> ¿cómo alojar temporalmente a personas que llegan y se van, con sus objetos, junto a una cultura local de exposición, reparación e intercambio?<br/><br/><b>Regla y apropiación:</b> ¿qué parte de una fachada común debe permanecer estable y qué puede cambiar cada habitante sin perjudicar al vecino?<br/><br/><b>Calle y privacidad:</b> ¿cómo ofrecer una planta baja útil al entorno y mantener un acceso doméstico tranquilo e independiente?')
d.section('Marco del enunciado y fuentes','El enunciado G3 v3.0 propone vivienda temporal para jóvenes, unos 1.500 m² y un número libre de unidades próximo a 20 unidades o 40 habitantes, con espacios para la vida en comunidad. Estas cifras son aproximaciones del programa, no un reparto dimensional ya resuelto.')
d.p('Lectura apoyada en el catálogo actual y su registro de casos; las fichas urbanas del catálogo de 600 m; el catálogo de frentes próximos; y las observaciones de texturas. El enunciado se ha consultado como fuente del programa. Las preguntas no atribuyen necesidades concretas a residentes que aún no han sido entrevistados.',10,13)

QUESTIONS=[
('Lugar, sección urbana y relación con Ribera',[
'¿Qué debe continuar el edificio: la alineación de calle, una cornisa, el ritmo de huecos o la intensidad de la planta baja?',
'¿Dónde conviene producir una pausa en el frente sin convertirla en un rincón residual?',
'¿Cómo cambia la entrada si se llega desde arriba o desde abajo de la pendiente de Ribera?',
'¿Qué diferencia de cota debe resolver el umbral para que el acceso no dependa de un escalón?',
'¿Qué altura o retranqueo permitiría recibir luz sin empeorar las condiciones de los vecinos?',
'¿Qué espacio de transición hace falta entre una calle activa y una vivienda temporal?',
'¿Puede una esquina o un ensanchamiento alojar una estancia sin bloquear el paso?',
'¿Qué vista desde la calle debería revelar un uso común y cuál debería proteger lo doméstico?',
'¿Qué aporta un patio al conjunto y cómo se comprueba que no sea solo un vacío sobrante?',
'¿Qué observación del solar podría hacer descartar la primera idea volumétrica?']),
('Habitantes, intimidad y vida cotidiana',[
'¿A qué jóvenes se dirige la propuesta y qué necesidades distintas impiden tratarlos como un grupo homogéneo?',
'¿Qué debe poder hacer una persona sola, sin pedir permiso ni coordinarse con otras?',
'¿Qué significa tener un lugar propio si la estancia dura semanas, meses o años?',
'¿Qué parte de cocinar, comer, lavar o trabajar se compartiría por elección y no por falta de espacio?',
'¿Cómo puede convivir quien trabaja de noche con quien estudia de día?',
'¿Dónde puede una persona recibir visitas sin atravesar el dormitorio de otra?',
'¿Qué necesita quien llega con pocas pertenencias y qué quien trae muchas?',
'¿Qué situaciones de discapacidad o movilidad reducida deben estar presentes al definir las unidades?',
'¿Dónde se guarda lo íntimo cuando se comparten cocina, lavado o espacios de trabajo?',
'¿Qué conversaciones con futuros habitantes cambiarían la distribución antes de dibujar una planta definitiva?']),
('Temporalidad, llegada y transformación',[
'¿Qué recorrido hace alguien desde que llega con una maleta hasta que reconoce un lugar como suyo?',
'¿Qué elementos permiten personalizar una unidad sin obras ni residuos en cada cambio de residente?',
'¿Qué partes deben mantenerse al cambiar una unidad de una a dos personas?',
'¿Puede una habitación cambiar de uso sin mover todas las instalaciones?',
'¿Dónde se guardan muebles y pertenencias entre dos ocupaciones?',
'¿Qué ocurre con los espacios comunes cuando varias viviendas están vacías?',
'¿Cómo se limpia o repara una unidad entre estancias sin perturbar las contiguas?',
'¿Qué cambios cotidianos son distintos de los cambios de temporada o de residente?',
'¿Qué información necesita una persona recién llegada para regular sombra, ventilación y consumos?',
'¿Cómo se evita que temporal signifique desechable en materiales, mobiliario y relaciones de cuidado?']),
('Comunidad, circulación y gradientes de acceso',[
'¿Qué actividad compartida tiene capacidad real para reunir a habitantes con horarios diferentes?',
'¿Dónde empieza lo común y quién puede entrar en cada tramo desde la calle hasta la habitación?',
'¿Puede la circulación permitir encuentros sin obligar a pasar delante de toda la intimidad doméstica?',
'¿Qué espacios admiten estar acompañado sin tener que conversar?',
'¿Qué agrupación de unidades facilitaría cuidar un espacio común de tamaño manejable?',
'¿Conviene un único espacio colectivo o varios pequeños próximos a las viviendas?',
'¿Cómo se puede salir de una actividad comunitaria y encontrar silencio inmediatamente?',
'¿Qué acceso permanece operativo cuando se cierra la parte abierta al barrio?',
'¿Cómo se gestiona la presencia de invitados sin transformar el acceso en un control hostil?',
'¿Qué partes comunes pueden transformarse si los residentes no usan el programa inicialmente previsto?']),
('Planta baja, objetos y actividades del Rastro',[
'¿Qué necesidad local debe confirmarse antes de proponer un taller, una tienda o una sala de intercambio?',
'¿Puede el edificio aportar reparación o préstamo en lugar de repetir oferta comercial existente?',
'¿Por dónde entraría un mueble voluminoso sin cruzarse con el acceso doméstico?',
'¿Qué espacio necesita recibir, clasificar, reparar, mostrar y guardar un objeto?',
'¿Qué parte del trabajo puede verse desde la calle sin exponer a sus usuarios de forma permanente?',
'¿Cómo cambia la planta baja entre actividad comercial, cierre y uso por residentes?',
'¿Qué almacenamiento evita que la exposición termine ocupando recorridos y salidas?',
'¿Qué relaciones de ruido, polvo u olor impedirían colocar un taller junto a una vivienda?',
'¿Quién gestionaría una actividad abierta al barrio y qué ocurriría si esa gestión desapareciera?',
'¿Qué puede ofrecer el umbral sin apropiarse de la acera ni obstaculizar el paso?']),
('Fachada, balcón, sombra y clima',[
'¿Qué función concreta debe tener el balcón: estar, secar, proteger, cultivar o conectar?',
'¿Qué se gana y qué se pierde al pasar del balcón individual a una banda continua?',
'¿Cómo se impide que un borde común elimine la intimidad de las habitaciones?',
'¿Qué posiciones de apertura y recogida de una protección solar deben quedar previstas desde el alzado?',
'¿Qué puede regular cada habitante y qué necesita una decisión colectiva para funcionar?',
'¿Dónde conviene transparencia y dónde opacidad cuando la planta baja está cerrada?',
'¿Qué profundidad y orientación hacen que una sombra sea útil en el momento requerido?',
'¿Cómo se puede ventilar sin depender de dejar abierta una ventana expuesta a ruido o miradas?',
'¿Puede la fachada admitir ropa, plantas y objetos sin que cada incorporación sea una improvisación?',
'¿Qué ensayo de luz, sombra y vistas permite elegir entre dos soluciones de hueco?']),
('Estructura, material, textura y construcción',[
'¿Qué retícula permite agrupar las unidades previstas y mantener una planta baja adaptable?',
'¿Qué relación real debería existir entre módulo estructural, partición doméstica y ritmo de fachada?',
'¿Qué parte del proyecto exige verificar luces, cargas y apoyos antes de adoptar una imagen formal?',
'¿Cómo expresar una regla común sin imitar literalmente el ladrillo o el ornamento del entorno?',
'¿Qué material responde al contacto y al roce del zócalo y cuál a las zonas protegidas?',
'¿Qué tamaño de pieza hace compatibles colocación, sustitución y aprovechamiento de material?',
'¿Qué encuentro entre suelo, revestimiento y puerta debe dibujarse primero para entender el conjunto?',
'¿Dónde puede incorporarse material recuperado y qué comprobaciones necesita para ese uso?',
'¿Cómo distinguir visualmente una pieza resistente de un revestimiento sin fingir su construcción?',
'¿Qué muestra a escala real permitiría decidir textura, junta, contraste y comportamiento al tacto?']),
('Instalaciones, cuidado, recursos y comprobación',[
'¿Por dónde pueden ampliarse instalaciones sin romper acabados ni entrar en otra vivienda?',
'¿Dónde se concentran registros para que el mantenimiento no invada la vida cotidiana?',
'¿Qué componente puede sustituir el usuario y cuál requiere personal especializado?',
'¿Cómo se accede con seguridad a un toldo, una luminaria o una pieza exterior?',
'¿Qué superficies conviene que envejezcan mostrando uso y cuáles deben mantener otra condición?',
'¿Qué consume menos recursos durante el uso y la reposición, no solo durante la construcción inicial?',
'¿Qué debe pasar con el agua al pie de fachada y cómo se verifica el encuentro con el suelo?',
'¿Qué coste y tiempo de limpieza supone cada alternativa de espacio común?',
'¿Qué indicador concreto permitirá comparar dos propuestas: intimidad, superficie útil, luz, coste o facilidad de cambio?',
'¿Qué evidencia haría abandonar la hipótesis inicial aunque su imagen resulte atractiva?'])]
assert sum(len(q) for _,q in QUESTIONS)==80
num=0
for start in range(0,8,2):
 d.page(f'Preguntas de proyecto / {start*10+1:02d}-{(start+2)*10:02d}','Elegir y relacionar; no es necesario responderlas todas para iniciar el proyecto.')
 for title,qs in QUESTIONS[start:start+2]:
  d.p(title,13,16,True,gap=9)
  for q in qs:
   num+=1;d.p(f'<b>{num:02d}.</b> {escape(q)}',10.4,12.7,gap=5)
  d.y-=8
results=[d.save()]

g=Doc('LEYENDA_Y_ETIQUETAS_QGIS.pdf','Leyenda y etiquetas del inventario físico QGIS')
g.page('Leyenda de colores / qué proyecto estás viendo','Los dos proyectos guardados tienen simbologías distintas. La columna I corresponde al inventario inicial por temas; la columna E, al proyecto etiquetado por categoría principal.')
g.p('<b>I:</b> INVENTARIO_FISICO_600M.qgz. <b>E:</b> QGIS_ETIQUETADO/INVENTARIO_ETIQUETADO.qgz. La leyenda coloreada es funcional; el resto del documento utiliza texto negro sobre blanco.',10,13)
g.y-=4
y=g.y;g.p('Código y categoría',11,14,True)
g.c.setFont('Times-Bold',10);g.c.drawString(365,y-11,'I: inicial');g.c.drawString(459,y-11,'E: etiquetado')
for key,code,title,col in CATS:
 y=g.y;g.p(f'{code}  {title}',10.5,13,width=310,gap=10)
 for x,c in [(365,OLD.get(key)),(459,col)]:
  if c:
   g.c.setFillColor(colors.HexColor(c));g.c.rect(x,y-11,15,9,fill=1,stroke=0);g.c.setFillColor(colors.black);g.c.setFont('Times-Roman',8);g.c.drawString(x+20,y-10,c)
  else:g.c.setFillColor(colors.black);g.c.setFont('Times-Roman',8);g.c.drawString(x,y-10,'Sin grupo')
g.y-=8
g.section('Si todos los puntos aparecen rojos','En el grupo 00_INVENTARIO_COMPLETO, el rojo #dc2b1f significa «todos los puntos», no «todos son comercios». Las líneas son #555555 y las áreas, #d8d8d8 con borde #777777. Los grupos temáticos iniciales están desactivados al crearlos; un mismo objeto puede figurar en varios si se activan.')
g.section('En el proyecto etiquetado','El color representa cat_codigo y no el nombre individual. Cada objeto tiene una categoría principal según la prioridad del script. El resto de sus temas se conserva en el campo temas. Los polígonos usan opacidad del 35 %, por lo que se ven más claros sobre blanco. Los códigos permiten distinguir categorías con colores parecidos.')

g.page('Qué identifica cada símbolo y cada código')
g.p('<b>P</b> = punto; <b>L</b> = línea; <b>A</b> = área o polígono. El prefijo de id_mapa indica geometría, no categoría. Por ejemplo, P02511 es «La Latina», categoría TRA. El ID cartográfico no es el ID de OpenStreetMap.')
g.p('<b>etiqueta:</b> ID + nombre. <b>nombre_mapa:</b> nombre o descripción disponible. <b>cat_codigo:</b> código de categoría. <b>subtipo:</b> etiqueta OSM de referencia. <b>osm_tipo + osm_id:</b> identidad en la fuente. Los números siguientes son registros del archivo local, no un censo de personas o actividades.')
y=g.y;g.p('Categoría',11,14,True)
g.c.setFont('Times-Bold',10)
for x,t in zip([365,444,530],['Puntos','Líneas','Áreas']):g.c.drawRightString(x,y-11,t)
for key,code,title,col in CATS:
 y=g.y;g.p(f'{code}  {title}',10,12,width=300,gap=7)
 for x,t in zip([365,444,530],COUNTS):
  g.c.setFont('Times-Roman',10);g.c.drawRightString(x,y-11,str(COUNTS[t].get(code,0)))
g.y-=4
totals=[sum(v.values()) for v in COUNTS.values()]
g.p(f'<b>Total:</b> {totals[0]:,} puntos, {totals[1]:,} líneas y {totals[2]:,} polígonos; {sum(totals):,} registros.'.replace(',','.'),11,14)
g.section('Precauciones al leer los nombres de categoría','<b>UMB</b> incluye objetos con entrada, puerta o información wheelchair: no todos son portales. <b>ACC</b> agrupa pasos, escaleras, ascensores, semáforos y farolas: no expresa un nivel de accesibilidad. <b>PAT</b> procede de historic o tourism: no equivale a protección patrimonial. <b>VER</b> incluye leisure, natural y landuse: no garantiza vegetación ni acceso público.')
g.p('COM agrupa shop, craft y office; MOB incluye bancos, papeleras, fuentes, aparcabicis, reciclaje y aseos; EQU recoge otros amenity; INF incluye man_made, emergency y power. EDI se asigna por building. Para saber qué es un objeto concreto, consultar etiqueta, temas y tags_json. El subtipo único puede no recoger todas sus funciones.',10,13)

g.page('Mostrar el nombre de cada punto en QGIS')
g.section('1. Abrir el proyecto que ya contiene las etiquetas','Guarda primero cualquier cambio de tu proyecto abierto. Después usa <b>Proyecto &gt; Abrir</b> y selecciona <b>INVENTARIO_ETIQUETADO.qgz</b> dentro de INVESTIGACIÓN / QGIS_ETIQUETADO. No necesitas descargar ni volver a ejecutar el inventario completo.')
g.p('El script principal genera el proyecto etiquetado como archivo independiente, pero no lo abre en la ventana activa. Seguir en INVENTARIO_FISICO_600M.qgz explica que aparezcan los colores iniciales y falten los campos añadidos.')
g.section('2. Activar o comprobar las etiquetas','En la capa <b>P · Puntos físicos</b>: botón derecho &gt; <b>Propiedades &gt; Etiquetas &gt; Etiquetas sencillas</b>. En el valor o campo de etiqueta elige <b>etiqueta</b> y pulsa Aplicar. Ese campo muestra el ID y el nombre. Para ver solo el número corto, usa <b>id_mapa</b>; para ver solo el nombre, <b>nombre_mapa</b>.')
g.p('Las tres capas guardadas ya tienen activado el campo etiqueta. Repite la comprobación en L · Líneas físicas y A · Polígonos físicos solo si deseas mostrar sus nombres también. Si el selector no contiene estos campos, estás en una capa del inventario original, no en la etiquetada.')
g.section('3. Leer todos los objetos sin amontonar texto','Acércate hasta una manzana o un tramo de calle. QGIS oculta etiquetas que chocan entre sí: que falte un texto en pantalla no significa que falte el punto. Para centrarte en puntos, desactiva temporalmente las etiquetas de líneas y polígonos, no sus datos.')
g.p('Si necesitas una categoría, usa el filtro de la capa con <b>"cat_codigo" = \'COM\'</b> para comercio, por ejemplo. Al terminar, elimina el filtro para recuperar todo. Para saber qué es un punto oculto por otros, usa <b>Identificar objetos espaciales</b> o la tabla de atributos y consulta etiqueta. Una leyenda explica los colores; las etiquetas identifican cada objeto.')
g.section('4. Recuperar el estilo si has cargado el GPKG directamente','En Propiedades de la capa, abre <b>Estilo &gt; Cargar estilo</b> y elige el QML correspondiente dentro de QGIS_ETIQUETADO: puntos_fisicos.qml, lineas_fisicas.qml o poligonos_fisicos.qml. Carga cada estilo en su propia capa. Así recuperas colores y configuración de etiquetas.')
g.p('Referencia de interfaz: <link href="https://docs.qgis.org/3.40/en/docs/user_manual/working_with_vector/vector_properties.html">Manual QGIS: propiedades de capas vectoriales y etiquetado</link>. Los nombres exactos de algunos controles pueden variar con la versión y el idioma.',9.5,12)

g.page('Poner la leyenda en un plano y conservar nombres')
g.section('Leyenda automática dentro de QGIS','En un diseño de impresión, añade primero un mapa y después <b>Añadir leyenda</b>. Selecciona la leyenda y vincúlala a ese mapa. En «Elementos de leyenda», desactiva la actualización automática si quieres retirar entradas innecesarias. Mantén las capas P, L y A que realmente estés representando; sus categorías aparecerán con código, nombre y símbolo.')
g.p('Si filtras la leyenda por el contenido del mapa, mostrará solo las categorías presentes en esa vista. Para una clave general de todo el inventario, deja ese filtro desactivado. La leyenda automática responde a la simbología real de las capas; conviene usarla si vas a cambiar colores.')
g.section('Leyenda preparada para insertar','Junto a esta guía se entregan <b>LEYENDA_ETIQUETADO.svg</b> y <b>LEYENDA_INVENTARIO_INICIAL.svg</b>. En el diseño: <b>Añadir imagen</b>, dibuja un rectángulo, selecciona imagen SVG y busca el archivo adecuado. Mantén las proporciones; una anchura de unos 110-140 mm permite leer sus categorías.')
g.p('Estos SVG son claves vectoriales fijas: no cargan datos ni etiquetan puntos y no se actualizan al cambiar la simbología. El SVG inicial incluye además la clave de «todos los puntos/líneas/áreas». Usa la versión que corresponda al proyecto abierto.')
g.section('Nombres en DXF','El archivo existente <b>QGIS_ETIQUETADO/INVENTARIO_CON_NOMBRES.dxf</b> fue generado por el script con un texto por objeto. Las capas <b>G_P_*, G_L_*, G_A_*</b> contienen geometría; <b>T_P_*, T_L_*, T_A_*</b> contienen ID y nombre como TEXT. LEYENDA aparece a la derecha del dibujo. El sistema es EPSG:25830 y las unidades son metros.')
g.p('En CAD, activa las capas T_* para ver los nombres. Que muchos textos se solapen no significa que se hayan perdido: necesitan organización por escala o categoría. Cambiar una etiqueta en QGIS no actualiza automáticamente ese DXF ya guardado. La leyenda SVG insertada en un diseño de impresión tampoco se incorpora por sí sola al DXF.')
g.section('Archivos y comprobación','Esta guía se obtiene de los dos scripts guardados, los estilos QML, el proyecto etiquetado y las tablas del GPKG existente. No se han modificado el catálogo, el inventario ni el proyecto QGIS. Los nombres y las categorías conservan la información del archivo local, sin nueva comprobación de campo.')
g.p('<link href="https://docs.qgis.org/3.40/en/docs/user_manual/print_layout/layout_items/layout_legend.html">Manual QGIS: leyenda del diseño</link><br/><link href="https://docs.qgis.org/3.40/en/docs/user_manual/print_layout/layout_items/layout_image.html">Manual QGIS: imágenes y SVG en el diseño</link>',9.5,12)
results.append(g.save())

def svg(initial):
 title='INVENTARIO INICIAL' if initial else 'INVENTARIO ETIQUETADO'
 a=['<svg xmlns="http://www.w3.org/2000/svg" width="140mm" height="193mm" viewBox="0 0 560 772">', '<rect width="560" height="772" fill="white"/>', '<g font-family="Arial,sans-serif" fill="#111">',f'<text x="16" y="29" font-size="18">{title}</text>', '<text x="16" y="52" font-size="12">Color = categoría; forma = geometría. P / L / A.</text>']
 y=84
 for key,code,title,col in CATS:
  if initial and key not in OLD:continue
  col=OLD[key] if initial else col
  a += [f'<circle cx="24" cy="{y}" r="4" fill="{col}"/>',f'<path d="M40 {y}h22" stroke="{col}" stroke-width="2"/>',f'<rect x="74" y="{y-6}" width="16" height="12" fill="{col}" fill-opacity="{.45 if initial else .35}" stroke="{col}"/>',f'<text x="105" y="{y+4}" font-size="13">{escape(code+" · "+title)}</text>']
  y+=35
 if initial:
  a += [f'<text x="16" y="{y+12}" font-size="13">00_INVENTARIO_COMPLETO (sin separar categorías)</text>']
  for text,col in [('Todos los puntos','#dc2b1f'),('Todas las líneas','#555555'),('Todas las áreas','#d8d8d8')]:
   y+=28;a += [f'<rect x="18" y="{y+6}" width="18" height="9" fill="{col}"/>',f'<text x="45" y="{y+15}" font-size="12">{text}</text>']
 else:
  a += [f'<text x="16" y="{y+13}" font-size="12">P = punto; L = línea; A = área o polígono.</text>',f'<text x="16" y="{y+35}" font-size="12">La etiqueta identifica el objeto: ID + nombre.</text>',f'<text x="16" y="{y+57}" font-size="12">Áreas al 35 % de opacidad; claves de color en la guía.</text>',f'<text x="16" y="{y+79}" font-size="12">UMB puede incluir información wheelchair, no solo accesos.</text>']
 a+=['</g></svg>'];name='LEYENDA_INVENTARIO_INICIAL.svg' if initial else 'LEYENDA_ETIQUETADO.svg';p=BASE/name;p.write_text('\n'.join(a));shutil.copy2(p,OUT/name)
svg(True);svg(False)
(BASE/'verificacion_contenido.json').write_text(json.dumps({'documents':results,'questions':num,'counts':COUNTS,'totals':totals},ensure_ascii=False,indent=2))
print(json.dumps({'documents':results,'questions':num,'records':sum(totals)},ensure_ascii=False))
