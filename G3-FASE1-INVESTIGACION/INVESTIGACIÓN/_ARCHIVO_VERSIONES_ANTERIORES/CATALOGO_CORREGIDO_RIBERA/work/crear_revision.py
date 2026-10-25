from pathlib import Path
import json, re, math, shutil, io
from collections import Counter
from xml.sax.saxutils import escape
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib import colors

ROOT=Path('/Volumes/T7/G3 Proyectos/INVESTIGACIÓN')
BASE=ROOT/'CATALOGO_CORREGIDO_RIBERA'
WORK=BASE/'work'
OUT=Path('/Users/adam/Documents/Codex/2026-09-21/crr/outputs')
OUT.mkdir(exist_ok=True)
PDF=BASE/'CATALOGO_CORREGIDO_RIBERA.pdf'
fields=json.loads(Path('/Users/adam/Documents/Codex/2026-09-21/crr/work/correcciones/fotos_inventario.json').read_text())
old={d['id']:d for d in json.loads((ROOT/'CATALOGO_PATRONES_600M/DATOS/observaciones_verificadas.json').read_text())}
sources={}
for d in json.loads((WORK/'capturas/registro.json').read_text()):
    ax=d['ax']; url=re.search(r'URL: "([^"]+)',ax).group(1)
    lat,lon=map(float,re.search(r'@([\d.]+),(-[\d.]+)',url).groups())
    date='julio 2021' if 'Jul 2021' in ax else 'marzo 2022'
    sources[d['id']]={'photo':str(WORK/'capturas'/f"{d['id']}.png"),'url':url,'lat':lat,'lon':lon,'date':date,'author':'Google Street View'}
sources.update(old)

# The physical front, not the photograph, is the counting unit.
fronts={
 'B01':('RC02','Ribera, frente de Chimeneas José Martínez'),
 'B02':('RC02','Ribera, frente sobre acceso Astoria'),
 'B03':('RC03','Ribera, esquina norte de Rodas, frente de ladrillo'),
 'B04':('RC04','Ribera, frente bajo de ladrillo junto a Astoria'),
 'B05':('RC05','Ribera, esquina norte de Fray Ceferino'),
 'B06':('RC05','Ribera, esquina sur de Fray Ceferino / Barrabés'),
 'B07':('RC06','Ribera 10, frente de Amantis'),
 'B08':('RC07','Ribera, frente del supermercado La Plaza'),
 'B09':('RC08','Ribera, frente blanco de Ranger y portales contiguos'),
 'B10':('RC09','Ribera, frente ocre con marcos blancos'),
 'B11':('RC09','Ribera, frente claro a la derecha del ocre'),
 'B12':('RC10','Ribera, frente con despiece y comercios Makalu'),
 'B13':('RC12','Cascorro 12, esquina con Amazonas'),
 'B14':('RC01','Ribera, Galerías Piquer'),
 'B15':('RC04','Ribera, Nuevas Galerías'),
 'B16':('SV016','Mira el Río Alta, comercio Juan Sandoval'),
 'B17':('RC09','Ribera, edificio bajo junto al frente ocre'),
 'B18':('RC07','Ribera, frente blanco y ladrillo junto a La Plaza'),
 'B19':('RC06','Esquina opuesta a Amantis, comercio Paprika'),
}

def case(b, xy, box, note, source=None):
    return dict(front=b,source=source or fronts[b][0],target=xy,crop=box,note=note)

CH=[]
def chapter(code,title,definition,conclusion,question,test,diagram,cases):
    assert len(cases)>=8 and len({v['front'] for v in cases})==len(cases)
    CH.append(dict(code=code,title=title,definition=definition,conclusion=conclusion,question=question,test=test,diagram=diagram,cases=cases))

chapter('01','Hueco vertical y balcón: unidad o banda',
 'Lo que se repite es la asociación entre hueco vertical, antepecho metálico y posición en una retícula de planta. No es «el ladrillo»: el mismo orden aparece con acabados y épocas visualmente distintos. La excepción comparativa es el balcón corrido, que agrupa varios huecos.',
 'Siete casos seleccionados fragmentan el borde en balcones individuales; B08 lo reúne en bandas. La repetición de ejes se observa en el alzado, pero no demuestra dónde están los pilares ni qué muros son portantes.',
 '¿Conviene que las 20 unidades del programa tengan una relación individual con la calle, o que el borde exterior sea un espacio compartido? ¿Dónde debe romperse la repetición para reconocer el acceso colectivo?',
 'Dibujar dos alzados del mismo programa: hueco-balconcillo por unidad y franja compartida. Comparar intimidad, mantenimiento, sombra y posibilidad de estancia; no copiar solo la forma ornamental.',
 'ritmo',[
 case('B01',(.407,.502),(.26,.30,.46,.55),'Balcón individual bajo hueco vertical; contorno de remate ornamentado.'),
 case('B02',(.652,.427),(.49,.05,.74,.48),'Ejes apilados de huecos con barandillas individuales.'),
 case('B03',(.306,.445),(.27,.07,.43,.50),'Serie de huecos en ladrillo, delimitada por bandas claras.'),
 case('B05',(.362,.444),(.275,.19,.46,.49),'Tres huecos con balcones separados: pared entre unidades.'),
 case('B06',(.843,.398),(.68,.05,.95,.46),'Balcones individuales con losa visible y laterales abiertos.'),
 case('B07',(.733,.476),(.54,.04,.83,.50),'Barandillas por hueco sobre la franja comercial.'),
 case('B08',(.538,.329),(.30,.03,.67,.39),'Banda continua: varios huecos comparten un mismo borde.'),
 case('B09',(.394,.480),(.28,.18,.54,.52),'Huecos alineados con balcones estrechos, carpintería oscura.')])

chapter('02','Basamento: la pared cambia al tocar la calle',
 'En ocho frentes distintos, el contacto con la calle se diferencia mediante piezas pétreas o un revestimiento de apariencia pétrea con juntas visibles. Se compara la continuidad, la altura relativa y su interrupción por accesos; no se identifica una cantera por fotografía.',
 'El basamento no es un adorno uniforme. B02 envuelve casi toda la planta baja; B01 y B13 forman una franja más baja; B05 concentra piezas en jambas y machones. El portal obliga a negociar el encuentro entre suelo, pared y carpintería.',
 '¿Qué parte de la planta baja necesita soportar roce, apoyo de objetos, limpieza o reposición? ¿Puede esa banda admitir cambios sin rehacer toda la fachada?',
 'Probar un zócalo con piezas sustituibles y juntas accesibles, comparado con un acabado continuo. Resolver primero umbral, drenaje y encuentro con carpintería; la fotografía no prueba la solución oculta existente.',
 'base',[
 case('B01',(.254,.713),(.19,.57,.30,.77),'Franja gris baja, interrumpida por una puerta de madera.'),
 case('B02',(.561,.601),(.51,.49,.74,.70),'Despiece pétreo en toda la altura del acceso.'),
 case('B03',(.206,.675),(.15,.50,.36,.75),'Piezas grises al pie de los machones, bajo acabado blanco.'),
 case('B04',(.468,.706),(.425,.57,.585,.79),'Juntas horizontales del revestimiento de planta baja.'),
 case('B05',(.308,.694),(.26,.52,.46,.76),'Jamba y machón pétreos entre portal y escaparate.'),
 case('B07',(.638,.713),(.57,.53,.79,.77),'Base pétrea alrededor del portal y tienda Amantis.'),
 case('B09',(.508,.690),(.46,.53,.66,.78),'Grandes piezas con juntas marcadas en la banda de acceso.'),
 case('B13',(.698,.751),(.55,.61,.82,.89),'Zócalo de placas grises, bajo revoco ocre claro.')])

chapter('03','Cerrajería: barras y bastidores delante del hueco',
 'Se repite un plano de barras enmarcadas delante del hueco, distinto de la carpintería situada detrás. Hay puertas, rejas y barandillas: son variantes de una relación visual, no ocho ejemplares de una misma pieza industrial. La franja inferior opaca aparece en algunos cierres, no en todos.',
 'El grado de apertura se gradúa sin cambiar siempre el tamaño del hueco. Astoria combina reja alta y faldón; Ranger, reja en el portal; el frente B11 conserva una puerta enrejada. Los balcones trasladan la misma lógica de barras al límite exterior.',
 '¿Qué debe poder verse del edificio comunitario cuando está cerrado? ¿Se puede distinguir acceso doméstico, taller y espacio común por densidad del cierre, y no por añadir tres lenguajes de fachada?',
 'Ensayar alzados de cierre con igual hueco y tres densidades. Comprobar aparte seguridad, accesibilidad y mantenimiento. No deducir mecanismos de giro, espesores ni anclajes de imágenes frontales.',
 'metal',[
 case('B02',(.68,.58),(.63,.49,.75,.68),'Astoria: barras verticales y faldón inferior opaco.'),
 case('B04',(.512,.522),(.49,.45,.59,.58),'Barandilla delante de los paños de carpintería.'),
 case('B05',(.359,.457),(.325,.35,.405,.50),'Barrotes y franja ornamental inferior del balcón.'),
 case('B06',(.824,.407),(.776,.29,.86,.45),'Barandilla metálica separada del plano de ventana.'),
 case('B09',(.49,.672),(.462,.58,.504,.77),'Portal de barras: transparencia en el acceso.'),
 case('B10',(.452,.485),(.427,.407,.495,.548),'Retícula metálica ante un hueco de vivienda.'),
 case('B11',(.61,.727),(.587,.625,.642,.837),'Reja vertical del portal, con zócalo gráfico inferior.'),
 case('B12',(.251,.497),(.243,.435,.286,.55),'Cierre de barras en un hueco inmediatamente sobre el comercio.')])

chapter('04','Capas textiles delante del hueco',
 'Ocho frentes incorporan una capa textil exterior: capota de ventana, toldo comercial, lona sobre balcón o tela colgada. El patrón es la adición de una capa regulable; las funciones de sombra, intimidad y señal comercial no son intercambiables ni están todas verificadas.',
 'La escala cambia: B02 y B13 cubren un hueco; B15 y B16 cubren un frente comercial; B08 repite el textil por tramos de balcón. La tela de B07 está documentada, pero su propósito concreto no se deduce de la imagen.',
 '¿Puede el edificio admitir apropiaciones textiles sin convertirlas en añadidos improvisados? ¿Qué partes las coloca cada habitante y qué partes se gestionan colectivamente?',
 'Dibujar una regla de posición, recogida y sustitución del textil. Ensayar una franja común de sujeción, sin atribuir a la solución fotografiada un anclaje que no se ve. Comprobar sombras con orientación y fecha reales antes de afirmar rendimiento.',
 'textil',[
 case('B02',(.520,.330),(.495,.30,.568,.473),'Capota desplegada sobre un balcón individual.'),
 case('B15',(.808,.55),(.746,.49,.92,.614),'Toldo rojo sobre el acceso comercial de Nuevas Galerías.'),
 case('B05',(.361,.508),(.28,.47,.464,.532),'Franja textil a rayas recogida sobre la tienda.'),
 case('B07',(.719,.27),(.626,.199,.816,.335),'Telas colgadas ante balcones: capa añadida por uso.'),
 case('B08',(.533,.215),(.407,.17,.679,.266),'Toldo verde y blanco: cobertura extendida en banda.'),
 case('B10',(.547,.560),(.412,.537,.577,.602),'Toldo verde de comercio bajo los balcones.'),
 case('B13',(.607,.200),(.563,.181,.65,.291),'Capota verde contenida en el ancho del recercado.'),
 case('B16',(.36,.38),(.165,.29,.70,.455),'Toldo de comercio en la calle lateral; caso de contraste próximo.')])

chapter('05','Comercio: el hueco funciona como vitrina',
 'Se comparan ocho locales distintos, no ocho fotografías de un mismo negocio. El objeto, rótulo y cierre ocupan una banda frontal; la diferencia está en mostrar tras vidrio, abrir el hueco o prolongar el uso al umbral. No se atribuye permiso de ocupación a lo que aparece fuera.',
 'Barrabés y Ranger acumulan objetos detrás del vidrio; la tienda de B05 deja un pequeño objeto en el umbral; Paprika lleva plantas al borde; Amantis presenta una entrada abierta. La planta baja hace legible su actividad mediante profundidad y contenido, no solo mediante color.',
 '¿Puede la planta baja del proyecto aportar reparación, intercambio, exposición o almacenaje al Rastro sin bloquear el acceso de las viviendas? ¿Cómo se reconoce el umbral cuando el taller está cerrado?',
 'Dibujar una franja de espesor útil: cierre, escaparate, lugar de apoyo y circulación libre. Contrastar la actividad diaria con la del mercadillo sin suponer que todas las tiendas sacan mercancía a la calle.',
 'comercio',[
 case('B01',(.411,.673),(.255,.565,.455,.746),'Chimeneas José Martínez: rótulo y escaparates por huecos.'),
 case('B05',(.362,.72),(.314,.542,.442,.758),'Tienda de la esquina: escaparate, puerta y pequeña mesa exterior.'),
 case('B06',(.673,.727),(.609,.594,.727,.798),'Barrabés: material expuesto detrás del vidrio.'),
 case('B07',(.73,.661),(.642,.531,.785,.748),'Amantis: acceso abierto y frente dividido por machones.'),
 case('B08',(.454,.693),(.292,.591,.638,.80),'La Plaza: frente ancho subdividido en huecos de acceso y vidrio.'),
 case('B09',(.756,.647),(.684,.50,.808,.746),'Ranger: vitrina estrecha y densa, reconocible también en F30.'),
 case('B14',(.368,.611),(.338,.51,.413,.68),'Galerías Piquer: escaparate individual junto a varios cierres.'),
 case('B19',(.234,.717),(.13,.568,.284,.784),'Paprika: plantas y objetos delimitan el borde del local.')])

chapter('06','Instalaciones: una segunda trama sobre el alzado',
 'Ocho frentes presentan cableado superficial que sigue una línea de planta, atraviesa un paño o cambia de dirección en un borde. Se señalan cables visibles, no conducciones supuestas. La lectura se separa de la estructura portante.',
 'La traza se concentra a menudo sobre los comercios o bajo el primer balcón; el portal, la esquina y la caja obligan a desviarla. El problema de proyecto es la convivencia entre una retícula prevista y añadidos futuros, no la mera presencia de un aparato.',
 '¿Dónde podrán pasar y registrarse futuras instalaciones sin perforar indiscriminadamente la envolvente? ¿Qué recorridos deben quedar disponibles para cambios de uso en planta baja?',
 'Reservar y dibujar un recorrido accesible, sus puntos de registro y la separación entre ámbitos domésticos y comerciales. Contrastar una franja común con tendidos independientes. El catálogo no identifica servicio ni titularidad de cada cable.',
 'cables',[
 case('B01',(.26,.546),(.198,.51,.44,.59),'Tendido horizontal inmediatamente por encima del rótulo comercial.'),
 case('B03',(.310,.489),(.215,.476,.376,.535),'Línea bajo el balcón y sobre el remate claro de la planta baja.'),
 case('B05',(.458,.502),(.334,.462,.493,.552),'Tendido en el cambio entre ladrillo y frente comercial.'),
 case('B07',(.614,.516),(.548,.49,.79,.567),'Paquete de cables que acompaña la base de los balcones.'),
 case('B09',(.516,.529),(.342,.50,.555,.584),'Cableado y cajas sobre los accesos del frente blanco.'),
 case('B10',(.709,.570),(.615,.523,.743,.631),'El tendido sigue el encuentro inferior de la fachada ocre.'),
 case('B11',(.75,.597),(.729,.539,.89,.641),'Cables en el encuentro con el edificio contiguo y bajo balcones.'),
 case('B13',(.672,.524),(.633,.445,.828,.566),'Cable horizontal con derivación curva hacia un hueco.')])

chapter('07','Banda accesible: inscripción, roce y sustitución',
 'Ocho frentes diferentes muestran grafiti o inscripciones en cierres y paños de planta baja. La recurrencia documentada es su presencia en soportes accesibles desde la calle. Las fotos cercanas permiten añadir desgaste y cambios de superficie, sin diagnosticar causas materiales no comprobadas.',
 'El soporte importa: el grafiti ocupa láminas de persiana, madera, piedra y revoco. El cierre concentra gran parte de la superficie visible cuando el comercio está cerrado. Repetición no significa que todos los edificios del barrio estén afectados ni que el turismo sea la causa.',
 '¿Cómo afecta esta condición a la materialidad del edificio? ¿Se puede alojar una superficie de expresión, montaje o intercambio sin convertir cada inscripción en una reparación de toda la fachada?',
 'Comparar panel reemplazable, superficie limpiable y paño de uso gráfico acordado. Probar muestras reales de limpieza antes de especificar tratamientos. Una intervención participativa exige acuerdos; no se deduce su aceptación de las fotos.',
 'huella',[
 case('B14',(.29,.611),(.264,.503,.327,.679),'Galerías Piquer: grafiti sobre las lamas de un cierre.'),
 case('B02',(.605,.627),(.571,.515,.626,.701),'Astoria: inscripción en persiana contigua al acceso enrejado.'),
 case('B03',(.125,.638),(.093,.531,.149,.701),'Rodas: trazos superpuestos en un cierre de planta baja.'),
 case('B05',(.152,.627),(.128,.539,.184,.714),'Esquina de Fray Ceferino: inscripción sobre cierre laminado.'),
 case('B07',(.463,.699),(.444,.626,.479,.775),'Amantis: cierre lateral con una figura gráfica de gran escala.'),
 case('B10',(.536,.724),(.509,.652,.566,.816),'Frente ocre: la persiana se lee como soporte gráfico completo.'),
 case('B18',(.823,.761),(.781,.692,.864,.865),'Junto a La Plaza: grafiti de gran tamaño en cierre comercial.'),
 case('B13',(.694,.748),(.65,.64,.743,.885),'Cascorro 12: trazos finos directamente sobre placas del zócalo.')])

chapter('08','Acabado por componentes: fondo, borde y base',
 'La recurrencia no es un color exacto, sino la diferenciación visual de componentes. En ocho frentes, el campo de pared, el contorno de los huecos o la banda de planta y el basamento se distinguen por tono, textura o junta. Las fotografías no están calibradas para obtener colores de obra.',
 'B03 y B15 hacen muy visibles marcos y bandas claras sobre ladrillo; B10 contrapone recercado blanco y revoco ocre; B09 usa un campo claro casi continuo y una base pétrea; B12 añade un despiece inciso. El acabado participa en el orden del edificio sin demostrar su construcción interior.',
 '¿Debe el proyecto expresar la unidad doméstica, una estructura común o un zócalo colectivo? ¿Qué componente puede cambiar de material sin destruir la lectura general?',
 'Ensayar el mismo alzado con tres distribuciones del acabado: por vivienda, por capa horizontal y por pieza sustituible. Trabajar con muestras reales de las texturas F01, F11, F18 y F32; no convertir una señal de calle en prueba de cerámica generalizada.',
 'acabado',[
 case('B01',(.398,.391),(.268,.32,.46,.55),'Marco claro ornamentado contra un fondo cálido.'),
 case('B03',(.255,.375),(.17,.31,.371,.50),'Bandas y recercados claros sobre el campo de ladrillo.'),
 case('B05',(.398,.354),(.275,.26,.452,.491),'El aparejo y la banda de ladrillo diferencian el campo respecto al hueco.'),
 case('B09',(.388,.536),(.273,.36,.55,.66),'Campo claro y basamento gris; el cable marca otra línea añadida.'),
 case('B10',(.523,.403),(.425,.366,.568,.541),'Recercado blanco con remate curvo sobre revoco ocre.'),
 case('B12',(.295,.300),(.263,.276,.416,.442),'Despiece del acabado claro alrededor de huecos oscuros.'),
 case('B13',(.573,.353),(.557,.255,.655,.481),'Borde blanco del hueco frente al paño de acabado ocre.'),
 case('B15',(.701,.321),(.626,.14,.734,.468),'Bandas y montantes claros dividen el paño rojo.')])

# Complete analytical inventory of the user's 33 photographs; no guessed GPS.
FNOTES=[
('Fuente: contacto y grano','Pulsador junto a dos superficies de grano y color diferentes; la arista moldurada registra desgaste.','Relacionar la pieza tocada con un soporte reparable y un encuentro que no acumule suciedad. No diagnosticar erosión ni humedad por color.','Mismo objeto que F17 y F29; no tres casos.'),
('Ladrillo, pintura y grafiti','El paño de ladrillo sirve de soporte a franjas pintadas y grafiti; encima se mantiene una banda perforada.','Separar soporte, inscripción y filtro superior. La repetición de piezas dentro del paño no prueba extensión por el barrio.','Mercado de la Cebada; mismo frente que F05, contexto exterior al eje inmediato.'),
('Edificio bajo y borde de piedra','Un frente amarillo de poca altura reúne vanos pequeños, reja y basamento oscuro; el elemento horario es singular.','Conservar la relación entre hueco, esquina y base; retirar el reloj como supuesto patrón territorial.','Mismo conjunto que F15 y F21; comparación visual con RC09.'),
('Rótulo, ménsula y balcón','Una pieza colgada perpendicularmente a la fachada hace visible el local; arriba aparecen barandilla y vegetación.','Preguntar si la señalización puede compartir una regla de soporte con el comercio sin invadir los huecos domésticos.','Ubicación exacta no verificada; no suma al recuento territorial.'),
('Celosía y paño gráfico','La banda superior mantiene perforaciones repetidas; el plano inferior cambia de dibujo y color.','Distinguir permanencia geométrica y variación superficial. No identificar material cerámico solo por semejanza.','Mismo frente que F02; una unidad de observación.'),
('Reja sobre borde pétreo','Barras verticales fijan una separación visual sobre un borde de piedra; se leen sombras y piezas superpuestas.','Estudiar por separado el espesor visible del borde y la transparencia del cierre. El anclaje interno no está documentado.','Localización exacta pendiente.'),
('Suelo: módulo y señal','Piezas pequeñas forman una retícula; una banda transversal y la cifra 210 interrumpen la continuidad.','Un trazado puede ordenar posiciones sin levantar paredes. La función administrativa de la cifra no está confirmada.','Posible relación de tramo con F33; no contar dos tramos sin verificar.'),
('Comercio y objetos en el umbral','Frente rosa con toldo de rayas; objetos y macetas ocupan el borde de un comercio abierto.','Dibujar la profundidad efectiva del uso: interior, hueco y exterior. No confundir apoyo temporal con espacio libre disponible.','No se ha demostrado que sea el mismo local que F31.'),
('Peldaños y cambio de cota','Contrahuellas de ladrillo y piezas de remate claras organizan una sucesión de niveles.','La junta entre suelo y fachada debe absorber desniveles. Dibujar solo los escalones visibles, no una rampa accesible que no aparece.','Ubicación exacta pendiente; no se han medido huellas ni alturas.'),
('Amantis: dividir el frente','Dos huecos comerciales se separan por un machón pétreo; el portal vecino mantiene otra carpintería.','La coexistencia de usos puede resolverse en el mismo plano sin hacerlos indistinguibles.','Ribera 10; mismo frente B07 / RC06. No suma un edificio nuevo.'),
('Pavimento: banda y placa','Losas grandes y piezas pequeñas se encuentran alrededor de un marcador circular; las juntas cambian de dirección.','Dibujar el encuentro de las dos retículas y la posición del marcador, no asignarle una función sin documento.','Mismo detalle que F18.'),
('Farmacia: retícula y carpintería','Paños claros de piezas pequeñas se delimitan por montantes oscuros y huecos de escaparate.','Lo interesante es el reparto entre módulo pequeño y marco grande. Este caso no basta para proclamar un patrón cerámico local.','Farmacia Fuentecilla, Toledo 105; mismo conjunto que F16, caso contextual.'),
('Cierre: barra y panel','Bastidor oscuro con barras en la zona superior y una zona inferior ciega; marco pétreo alrededor.','El cierre filtra de manera desigual según altura. Una elevación explica esa diferencia mejor que un giro de puerta inventado.','Portal no geolocalizado con suficiente certeza.'),
('Fundición: relieve y roce','Relieve vegetal sobre metal pintado; pérdidas de acabado y una inscripción blanca se superponen a la forma.','La textura tiene una escala de contacto distinta a la del zócalo liso. Comparar mantenimiento de huecos y salientes.','Objeto sin localización exacta confirmada.'),
('Frente bajo: líneas superpuestas','Huecos en fachada amarilla, recercados rojizos y cableado que recorre el paño y dobla sobre un arco.','Separar dibujo previsto del acabado y línea añadida de la instalación.','Mismo edificio que F03 y F21; no tres fachadas.'),
('Farmacia: conjunto vertical','La planta baja de retícula clara se relaciona con ventanas, balcón y carpinterías de las plantas superiores.','La foto general permite saber dónde se sitúa el detalle F12 y evita convertir un recorte en fachada completa.','Mismo edificio que F12.'),
('Fuente: cuenco y huella','La pila contiene residuos; aparecen cambios oscuros de superficie en encuentros y relieve de la pieza central.','Preguntar cómo se limpia y vacía un elemento común; no atribuir las manchas a una patología concreta.','Misma fuente que F01 y F29.'),
('Piedra: grano y junta','Primer plano del grano pétreo, las juntas y un marcador circular con el número 432.','Aquí sí puede hablarse de textura visible. No se conoce por la foto cantera, tratamiento antideslizante ni función oficial del número.','Mismo punto que F11.'),
('Cerrajería ornamental','La reja combina barras, círculos, rombos y remates superiores sobre una base pétrea.','Descomponer el dibujo en módulo repetido y remate. No confundir una única verja con ocho emplazamientos.','Ubicación exacta pendiente.'),
('Óculo: piezas radiales y espiral','Una abertura circular tiene un borde de piezas radiales y una reja espiral; la base inferior es pétrea.','La dirección de las juntas cambia alrededor del hueco. No se demuestra por ello la función resistente del anillo.','Caso particular; no se eleva a patrón territorial.'),
('Recercado pintado y cierre','Líneas rojizas siguen el borde de un hueco; el cierre negro y el arco vecino tienen tratamientos distintos.','Señalar el borde pintado, no toda la fachada como cerámica. La figura puede variar sin alterar el hueco.','Mismo frente que F03/F15; imagen de detalle.'),
('Fuente y escalera en la calle','La fuente se inserta junto a una escalera y un frente institucional; el pavimento recoge el desnivel.','El objeto urbano necesita una sección de uso y mantenimiento, no solo una imagen frontal. No se dispone de levantamiento dimensional.','Entorno de Ribera 2, comparado con RC10; conjunto relacionado con F29/F32.'),
('Medianera: soporte de gran escala','Un paño casi sin huecos contiene un dibujo geométrico; árboles y base introducen otra escala delante.','Comparar superficie disponible y uso gráfico. RC11 muestra otro tratamiento en ese mismo soporte; las fechas no permiten ordenar ambos estados con certeza.','Frente norte del recorrido; no prueba frecuencia de medianeras pintadas.'),
('Cierre: madera, metal y deterioro','Tableros y una hoja metálica reciben grafiti; en el pie se observan pérdidas y cambios de superficie.','El contacto con el suelo es el punto a resolver para que una pieza sea sustituible. No diagnosticar causa del deterioro sin inspección.','Localización exacta pendiente.'),
('Esquina: continuidad del balcón','Un edificio rosa gira en la esquina manteniendo barandillas oscuras, base clara y bandas ornamentales.','La continuidad del orden puede doblar una esquina sin producir una fachada secundaria completamente ajena.','Localización exacta pendiente; referencia visual, no nuevo caso contado.'),
('Madera y grafismo de comercio','Carpintería marrón y rótulos ordenan el frente de farmacia; delante aparece una instalación provisional de obra.','Distinguir estado permanente del local y elementos temporales. No atribuir el andamio al funcionamiento habitual.','Farmacia distinta de la de F12/F16; dirección sin confirmar.'),
('Diagonal exterior contemporánea','Elementos blancos diagonales se leen por delante del vidrio; una valla azul modifica el contacto con la calle.','La imagen muestra geometría, no camino de cargas ni sistema resistente verificado. Se conserva como contraste, no como patrón del entorno inmediato.','Localización y documentación constructiva no confirmadas.'),
('Portal: bastidor y franja inferior','Puerta de dos hojas, barrotes verticales y elementos de tono dorado; encima aparece la inscripción 8 EXT.','Comparar tamaño de hoja, transparencia y zócalo visual. No representar apertura o herrajes ocultos.','Número parcial visible; no se asigna una calle solo por él.'),
('Fuente: contexto material','Vista general de pila, pieza vertical y base, junto a ladrillo y escalones; completa los recortes F01/F17.','Relacionar relieve, contacto, drenaje visible y acceso de mantenimiento.','Mismo objeto que F01/F17; conjunto próximo a Ribera 2.'),
('Ranger: exposición detrás del vidrio','Productos y soportes llenan el escaparate; por encima se cruzan carpintería, balcón y cableado.','El contenido puede densificar el frente sin ocupar físicamente la acera. Separar capa de exposición y acceso.','Ribera 6, comparación con RC08; mismo frente B09.'),
('Persiana: imagen al cerrar','Grafiti sobre cierre rosa bajo toldo de rayas; el rótulo permite reconocer Siete vidas de gata.','Diseñar también el alzado de la hora de cierre. No afirmar que F08 sea su estado abierto: la coincidencia cromática no basta.','Localización exacta pendiente.'),
('Ladrillo, piedra y desgaste','En el frente de Mensajeros de la Paz, paño de ladrillo, piezas pétreas y arranque gastado se encuentran en el acceso.','El interés está en la junta entre materiales y en qué pieza llega al suelo. La foto no permite identificar el muro portante.','Ribera 2, dirección de la entidad; conjunto relacionado con F22/F29.'),
('Suelo: repetición y reparación','Pequeñas piezas grises forman una retícula continua; variaciones de tono y junta impiden leerla como una textura perfectamente homogénea.','Pensar un pavimento reparable por unidades y estudiar su encuentro con bandas, tapas y umbrales.','Posible mismo tramo que F07: no se cuenta por duplicado.')
]
assert len(FNOTES)==len(fields)==33

W,H=595.276,841.89
C=canvas.Canvas(str(PDF),pagesize=(W,H),pageCompression=1)
C.setTitle('Ribera de Curtidores | Catálogo corregido de patrones')
C.setAuthor('Investigación G3 · revisión a partir de las correcciones y fotografías aportadas')
PAGE=0
manifest=[]
def p(text,x,y,w,size=11,leading=None,bold=False):
    st=ParagraphStyle('t',fontName='Times-Bold' if bold else 'Times-Roman',fontSize=size,leading=leading or size*1.24,textColor=colors.black)
    para=Paragraph(text,st); aw,ah=para.wrap(w,1000)
    if y-ah<43: raise ValueError(f'Text overflow page {PAGE}: {text[:100]} at {y-ah}')
    para.drawOn(C,x,y-ah)
    return y-ah
def page(kicker,title):
    global PAGE
    if PAGE: C.showPage()
    PAGE+=1
    C.setFont('Times-Roman',9); C.drawString(42,H-34,'RIBERA DE CURTIDORES / INVESTIGACIÓN G3')
    C.drawRightString(W-42,28,str(PAGE))
    p(kicker.upper(),42,H-66,W-84,9)
    return p(title,42,H-86,W-84,23,25,True)-18
def img(path,x,y,w,h,crop=None):
    im=ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    if crop:
        iw,ih=im.size; im=im.crop(tuple(round(a*b) for a,b in zip(crop,(iw,ih,iw,ih))))
    iw,ih=im.size; scale=min(w/iw,h/ih); dw,dh=iw*scale,ih*scale
    xx=x+(w-dw)/2; yy=y+(h-dh)/2
    im.thumbnail((1800,1800)); bio=io.BytesIO(); im.save(bio,'JPEG',quality=91)
    C.drawImage(ImageReader(bio),xx,yy,dw,dh)
    return xx,yy,dw,dh
def arrow(tx,ty,sx,sy):
    # White under-stroke preserves legibility; a single exact endpoint per case.
    C.setStrokeColor(colors.white); C.setLineWidth(3.5); C.line(sx,sy,tx,ty)
    C.setStrokeColor(colors.black); C.setLineWidth(.9); C.line(sx,sy,tx,ty)
    angle=math.atan2(ty-sy,tx-sx)
    for d in (-.48,.48): C.line(tx,ty,tx-7*math.cos(angle+d),ty-7*math.sin(angle+d))
    C.setFillColor(colors.white); C.circle(sx,sy,7,fill=1,stroke=0)
    C.setFillColor(colors.black); C.setFont('Times-Bold',8); C.drawCentredString(sx,sy-2.7,'1')
def casecard(ch,v,index,x,top):
    src=sources[v['source']]; crop=v['crop']; tw=244
    iw,ih=Image.open(src['photo']).size
    if (crop[2]-crop[0])*iw/((crop[3]-crop[1])*ih)>2.5:
        mid=(crop[1]+crop[3])/2; hh=(crop[2]-crop[0])*iw/(2.2*ih)
        crop=(crop[0],max(0,mid-hh/2),crop[2],min(1,mid+hh/2))
        v['crop']=crop
    label=f"{ch['code']}.{index:02d} / {v['front']} / {v['source']}"
    p(label,x,top,tw,10,bold=True)
    xx,yy,dw,dh=img(src['photo'],x,top-191,tw,168,crop)
    u=(v['target'][0]-crop[0])/(crop[2]-crop[0]); z=(v['target'][1]-crop[1])/(crop[3]-crop[1])
    assert 0<=u<=1 and 0<=z<=1,(label,u,z)
    tx=xx+u*dw; ty=yy+(1-z)*dh
    sx=max(xx+9,min(xx+dw-9,tx+(-42 if u>.45 else 42)))
    sy=max(yy+9,min(yy+dh-9,ty+34))
    arrow(tx,ty,sx,sy)
    y=top-198
    y=p(escape(fronts[v['front']][1]),x,y,tw,9.2,10.5)
    y=p('1. '+escape(v['note']),x,y-5,tw,10,11.5)
    p(f"Detalle · © {escape(src['author'])} · {src['date']}",x,y-5,tw,7.5,9)
    manifest.append(dict(category=ch['code'],case=label,**v))
def label(t,x,y,w=210): return p(t,x,y,w,10,12)
def rect(x,y,w,h): C.rect(x,y,w,h,stroke=1,fill=0)
def bars(x,y,w,h,n=9):
    rect(x,y,w,h)
    for i in range(1,n): C.line(x+w*i/n,y,x+w*i/n,y+h)
def sketch(kind,x,y,variant):
    C.saveState(); C.translate(x,y); C.setLineWidth(.8); C.setStrokeColor(colors.black)
    # Every sketch is a comparative elevation of visible parts, not a construction section.
    if kind=='ritmo':
        for r in range(3):
            for j in range(3): rect(18+j*57,18+r*47,20,33)
        if variant==0:
            for r in range(3):
                for j in range(3): bars(12+j*57,16+r*47,32,12,7)
        else:
            for r in range(3): bars(8,16+r*47,163,12,28)
    elif kind=='base':
        rect(8,5,175,128)
        C.line(8,62 if variant==0 else 113,183,62 if variant==0 else 113)
        for yy in ([24,43] if variant==0 else [24,43,62,81,100]):
            C.line(8,yy,183,yy)
            for xx in (35,80,125,170): C.line(xx,yy-19,xx,yy)
        C.setFillColor(colors.white); C.rect(58,5,44,95,fill=1,stroke=1); C.setFillColor(colors.black)
        if variant: C.line(106,5,106,112)
    elif kind=='metal':
        rect(28,5,126,130)
        bars(32,40 if variant==0 else 8,118,91 if variant==0 else 123,14)
        if variant==0: C.line(91,5,91,135); C.line(28,38,154,38)
        else:
            for yy in (32,64,96): C.line(32,yy,150,yy)
    elif kind=='textil':
        n=1 if variant==0 else 3
        for j in range(n): rect(23+j*53,18,31,91)
        width=45 if variant==0 else 160
        rect(17,106,width,9)
        a=C.beginPath(); a.moveTo(17,106); a.lineTo(8,84); a.lineTo(8+width,84); a.lineTo(17+width,106); C.drawPath(a)
        for j in range(6 if variant==0 else 16):
            xx=17+j*width/(6 if variant==0 else 16); C.line(xx,106,xx-9,84)
        C.line(8,84,8,76); C.line(8+width,84,8+width,76)
    elif kind=='comercio':
        rect(12,15,155,118); rect(16,103,147,24)
        if variant==0:
            rect(21,20,130,77)
            for r in range(3):
                C.line(23,30+22*r,149,30+22*r)
                for j in range(5): rect(27+23*j,31+22*r,13,13)
        else:
            rect(22,20,54,77); rect(95,20,54,77)
            C.line(12,15,181,15); rect(82,0,26,10)
            C.line(85,0,85,-8); C.line(104,0,104,-8)
    elif kind=='cables':
        for j in range(3): rect(16+57*j,61,23,51); rect(15+57*j,4,33,35)
        C.line(5,51,179,51)
        C.setLineWidth(2)
        C.line(5,47,179,47)
        if variant==0:
            rect(57,43,9,9); C.line(61,43,61,12)
        else:
            C.bezier(94,47,104,40,99,30,109,21); C.line(151,47,151,11)
        C.setLineWidth(.5)
    elif kind=='huella':
        rect(20,7,138,126)
        if variant==0:
            for yy in range(13,132,7): C.line(21,yy,157,yy)
        else:
            for yy in (30,59,88): C.line(20,yy,158,yy)
            C.line(70,7,70,133); C.line(120,7,120,133)
        C.setLineWidth(1.5)
        path=C.beginPath(); path.moveTo(32,32); path.curveTo(77,105,43,112,118,78); path.curveTo(155,45,85,6,68,36); C.drawPath(path)
    elif kind=='acabado':
        rect(8,8,168,125)
        if variant==0:
            for yy in range(13,132,8): C.line(8,yy,176,yy)
            C.setFillColor(colors.white)
            for yy in (49,95): C.rect(8,yy,168,6,fill=1,stroke=1)
            for xx in (23,81,136): C.rect(xx,54,27,42,fill=1,stroke=1)
            C.setFillColor(colors.black)
        else:
            for xx in (20,79,134):
                rect(xx,51,30,58); rect(xx+5,56,20,48)
            C.line(8,37,176,37)
            for xx in (35,83,139): C.line(xx,8,xx,37)
    C.restoreState()

DIAG={
'ritmo':('B05 / RC05: unidades separadas','B08 / RC07: borde continuo','D1 aísla tres ejes y tres niveles visibles: cada balcón corresponde a un hueco. D2 agrupa la barandilla de varios huecos. Las distancias están abstraídas, no medidas.'),
'base':('B13 / RC12: franja baja','B02 / RC02: planta baja revestida','D1 muestra la interrupción de una banda baja por el acceso. D2 extiende las piezas hasta la cabeza del hueco. El dibujo representa juntas visibles; no espesor ni sistema de fijación.'),
'metal':('B02 / RC02: barras y faldón','B09 / RC08: cierre enrejado','D1 separa la zona de barras de la franja inferior ciega. D2 representa la subdivisión del portal. No son planos de fabricación: el módulo de barras es un esquema de lectura.'),
'textil':('B13 / RC12: cubrir un hueco','B08 / RC07: cubrir una banda','D1 relaciona ancho textil y ancho del vano. D2 reúne varios huecos bajo una franja. Son proyecciones esquemáticas del contorno visible; no describen brazos, bisagras ni cálculo de sombra.'),
'comercio':('B09 / RC08: vitrina densa','B05 / RC05: hueco y apoyo','D1 ordena visualmente los productos tras el vidrio. D2 sitúa una pieza pequeña junto al acceso abierto. Los objetos se simplifican; no se dibuja una planta interior que no está documentada.'),
'cables':('B09 / RC08: línea y registro','B13 / RC12: línea y derivación','D1 distingue el recorrido horizontal de una caja y su bajada. D2 destaca un cambio de dirección sobre un hueco. Las ventanas sirven de referencia; el trazado no identifica servicios.'),
'huella':('B14 / RC01: soporte laminado','B13 / RC12: soporte de placas','D1 y D2 comparan cómo la inscripción cruza dos despieces. El trazo es un símbolo analítico, no una transcripción del grafiti. Lo persistente es el soporte y su posibilidad de sustitución.'),
'acabado':('B03 / RC03: bandas y ladrillo','B10 / RC09: recercado y fondo','D1 destaca bandas y bordes claros sobre un campo de piezas. D2 conserva el borde del hueco sobre un fondo continuo. Son mapas de componentes, no paletas cromáticas calibradas.')}

y=page('Revisión del catálogo / 22 septiembre 2026','Patrones próximos a Ribera de Curtidores')
y=p('Ocho familias comparadas, ocho casos físicos por familia y análisis de las 33 fotografías aportadas.',42,y,W-84,16,20)-18
img(sources['RC05']['photo'],42,350,W-84,245)
y=p('Del parecido visual a una decisión de arquitectura',42,323,W-84,16,bold=True)-10
y=p('La revisión sustituye categorías demasiado amplias por relaciones comprobables: qué elemento se repite, dónde está, en qué cambia y qué pregunta permite plantear al proyecto de vivienda colectiva y espacios comunes del Rastro.',42,y,W-84,12)-12
y=p('No es un censo completo de los 600 m. Es un catálogo comparativo centrado en el eje inmediato, con un contraste lateral próximo. Ocho casos documentan recurrencia en la muestra; no permiten afirmar un porcentaje sobre todo el barrio.',42,y,W-84,11)-12
p('Fotografías de campo: archivo aportado por el usuario, sin fecha ni GPS verificables. Street View: imágenes históricas de 2021 y 2022; las fechas figuran en cada caso. Se conservan las fuentes originales.',42,y,W-84,10)

y=page('Cómo leer y comprobar el catálogo','Un caso no es una fotografía')
for head,txt in [
 ('Unidad de recuento','B01-B19 identifican frentes físicos. Una segunda foto del mismo frente no aumenta la frecuencia. Un edificio puede aparecer en varias familias porque se comparan relaciones distintas; no son 64 edificios diferentes.'),
 ('Evidencia visible','Cada ficha reúne ocho casos, todos fotografiados, con una única flecha numerada y una descripción de su destino. Los recortes muestran el elemento; los identificadores RC/SV remiten al registro de capturas, fechas, coordenadas de cámara y enlaces.'),
 ('Recorrido','Se parte del entorno de Galerías Piquer y Rodas, se sube por Fray Ceferino, los frentes de La Plaza y Ranger y el tramo de Ribera 2, y se llega a Cascorro/Amazonas. Mira el Río Alta solo aporta el octavo contraste de capa textil. El orden de las categorías va de la organización del frente a las capas añadidas y las huellas de uso.'),
 ('Qué no se ha demostrado','No se deducen estructura, tipo de muro, anclajes, prestaciones térmicas, especie de piedra o patología a partir del aspecto. No se afirma un cambio reciente cuando faltan fechas comparables. Tampoco se atribuye el grafiti al turismo.'),
 ('Diagrama y pregunta','Los 16 dibujos comparan componentes visibles de casos identificados. Son alzados y abstracciones, no secciones constructivas inventadas. Cada familia termina en una pregunta y una prueba de proyecto, sin el apartado «lectura de proyecto».'),
 ('Fotografías aportadas','F01-F33 se conservan completas en el atlas. Se indican duplicados de fuente, farmacia, frente bajo y detalle del pavimento. Las ubicaciones no confirmadas no se usan para alcanzar ocho casos territoriales.')]:
    y=p(head,42,y,W-84,13,bold=True)-5; y=p(txt,42,y,W-84,11)-16

y=page('Índice de relaciones','De la fachada común a su transformación')
for ch in CH:
    y=p(f"{ch['code']}   {ch['title']}",42,y,W-84,14,bold=True)-6
    y=p('Ocho casos / comparación dibujada / pregunta y prueba concreta.',65,y,W-107,10)-18
p('Después de las ocho familias: atlas F01-F33, vegetación y pavimento, temporalidad del Rastro, síntesis de decisiones, registro de fuentes y control de las correcciones.',42,y-5,W-84,11)

for ch in CH:
    for half in range(2):
        top=page(f"Familia {ch['code']} / evidencia {half+1} de 2",ch['title'])
        p('8 frentes independientes en esta familia. La flecha 1 identifica el componente descrito.',42,top,W-84,10)
        for j,v in enumerate(ch['cases'][half*4:half*4+4]):
            casecard(ch,v,half*4+j+1,42+(j%2)*267,top-30-(j//2)*303)
    y=page(f"Familia {ch['code']} / comparación y decisión",ch['title'])
    y=p(ch['definition'],42,y,W-84,11)-16
    a,b,explain=DIAG[ch['diagram']]
    label('D1. '+a,48,y,230); label('D2. '+b,314,y,230)
    sketch(ch['diagram'],62,y-176,0); sketch(ch['diagram'],327,y-176,1)
    y=p(explain,42,y-205,W-84,10)-15
    y=p('Qué se puede concluir',42,y,W-84,13,bold=True)-5
    y=p(ch['conclusion'],42,y,W-84,11)-15
    y=p('Pregunta que abre el proyecto',42,y,W-84,13,bold=True)-5
    y=p(ch['question'],42,y,W-84,11)-15
    y=p('Prueba concreta',42,y,W-84,13,bold=True)-5
    p(ch['test'],42,y,W-84,11)

for start in range(0,33,2):
    top=page('Atlas de fotografías aportadas','Texturas, encuentros y usos observados')
    for j,idx in enumerate(range(start,min(start+2,33))):
        d=fields[idx]; title,obs,meaning,status=FNOTES[idx]
        yy=top-j*324
        p(f"{d['id']} / {title}",42,yy,W-84,13,bold=True)
        img(d['path'],42,yy-288,202,263)
        ty=p('Se ve',260,yy-28,292,11,bold=True)-5
        ty=p(obs,260,ty,292,11)-12
        ty=p('Qué obliga a pensar',260,ty,292,11,bold=True)-5
        ty=p(meaning,260,ty,292,11)-12
        p(status,260,ty,292,9.5)
    if start==32:
        p('El atlas conserva incluso las imágenes singulares porque aportan observaciones materiales. No se usan esas singularidades para inflar la frecuencia de un patrón. El nombre original de cada archivo y su correspondencia F01-F33 se guardan en el registro JSON de esta revisión.',42,top-365,W-84,12)

y=page('Lecturas complementarias / no ocho casos certificados','Vegetación y suelo: posición, no decoración')
img(sources['RC08']['photo'],42,y-207,250,187,(.27,.22,.55,.54))
img(fields[8]['path'],315,y-207,237,187)
y=p('Vegetación en B09 / RC08 y desnivel fotografiado en F09.',42,y-218,W-84,9)-17
y=p('La maceta está asociada a una barandilla y a un hueco; el árbol ocupa el suelo de la calle. Son dos escalas y dos gestiones distintas. F08 y RC06 añaden macetas junto al comercio. El catálogo anterior confundía la presencia de verde con una relación espacial: aquí la pregunta es quién lo mantiene, dónde drena y qué paso deja libre.',42,y,W-84,11)-15
y=p('En F07/F33, la retícula pequeña del pavimento contrasta con las losas y bandas de F11/F18. F09 y F22 documentan desnivel y escaleras. Sin direcciones y mediciones suficientes, no se presentan ocho tramos independientes ni una solución universal de accesibilidad.',42,y,W-84,11)-15
y=p('Ensayo: dibujar una planta de borde con tres franjas identificadas -uso doméstico/comercial, paso y elementos fijos-, midiendo los pasos reales. Situar macetas y piezas sustituibles sin ocupar la circulación. Levantar el encuentro entre zócalo y suelo antes de decidir una textura continua.',42,y,W-84,11)-15
p('Pendiente de verificación: dimensiones libres, pendientes, especie y porte de los árboles, desagües y función de los marcadores 210 y 432. Estas carencias se mantienen explícitas en vez de inventar patrones para completar categorías.',42,y,W-84,10)

y=page('Temporalidad del Rastro','El mismo soporte, distintos estados de uso')
y=p('La información municipal distingue el mercadillo de la actividad de las tiendas del entorno. Las capturas de este catálogo documentan un estado puntual: comercios abiertos, cierres bajados y calle sin puestos montados. No hay una serie fotográfica emparejada que permita medir ocupación dominical frente a día laborable.',42,y,W-84,12)-17
img(sources['RC01']['photo'],42,y-230,W-84,220)
y-=243
y=p('RC01. Galerías Piquer: alternancia de accesos, vitrinas y cierres; árboles y bolardos son soportes físicos persistentes. No se dibujan puestos supuestos sobre esta imagen.',42,y,W-84,10)-17
for head,txt in [
 ('Lo estable','Huecos, pavimento, arbolado, bolardos, altura de los accesos y separación entre local y vivienda.'),
 ('Lo variable observado','Apertura del cierre, cantidad de objetos visibles, capa textil y presencia puntual de objetos en el umbral. F08 y F31 no son una pareja antes/después verificada.'),
 ('Lo que el proyecto debe ensayar','Un espacio común de recepción, exposición y reparación con acceso propio, almacenaje y cierre legible fuera del horario de actividad. Es una hipótesis para complementar el Rastro, no un programa demandado estadísticamente.'),
 ('Cómo comprobarlo','Repetir una posición de cámara en día laborable y día de mercadillo; registrar franjas horarias, ancho ocupado y libre, carga/descarga, cierres y permanencias. Entrevistar a residentes y comerciantes antes de atribuirles necesidades.')]:
    y=p(head,42,y,W-84,12,bold=True)-4; y=p(txt,42,y,W-84,10.5)-12

y=page('Síntesis','Cinco decisiones que sí se desprenden del estudio')
for head,txt in [
 ('1. Separar permanencia y cambio','El orden de huecos y el basamento permanecen mientras toldos, rótulos, objetos y grafiti cambian. Proponer una base material mantenible y una capa de apropiación sustituible es una respuesta a esa coexistencia, no una copia de una fachada histórica.'),
 ('2. Dar espesor útil a la planta baja','Vitrina, acceso y apoyo de objetos son situaciones diferentes. Una planta baja comunitaria puede recibir actividad vinculada al Rastro si separa circulación, exposición, trabajo y acceso doméstico. Hay que contrastar demanda y gestión antes de fijar usos.'),
 ('3. Elegir conscientemente el borde doméstico','Balcón individual y banda continua producen lecturas distintas de la vivienda colectiva. El catálogo aporta ambas variantes; no demuestra cuál funciona mejor para 40 residentes. Esa elección necesita plantas, sección de uso, privacidad y mantenimiento.'),
 ('4. Proyectar el estado cerrado y el mantenimiento','La persiana es una gran superficie pública cuando baja. La junta, la limpieza y la sustitución de una pieza deben formar parte del diseño. Una superficie expresiva o participativa es una posibilidad a acordar, no una respuesta automática al grafiti.'),
 ('5. No confundir apariencia y estructura','El ritmo del ladrillo visible no revela el sistema resistente. Antes de elegir una estructura para el proyecto hacen falta luces, cargas, programa, levantamiento y documentación técnica. Por eso se han retirado las secciones constructivas ficticias del catálogo anterior.')]:
    y=p(head,42,y,W-84,14,bold=True)-6; y=p(txt,42,y,W-84,11)-20

y=page('Control de tus correcciones','Qué se ha cambiado y qué no se finge resuelto')
for head,txt in [
 ('P01-P08 / organización, zócalo, ladrillo y marco','Rehechos como familias 01, 02 y 08. Se indica qué línea, pieza o borde interesa. El ladrillo visible no se interpreta como estructura; el grano solo se analiza en fotografías próximas.'),
 ('P09-P13 / balcones, cierres, carpintería y toldos','Familias 01, 03 y 04, ocho frentes por familia. Se eliminan mecanismos de apertura no observados y la persiana como categoría autónoma. Los portales adicionales F13/F28 quedan documentados sin inventar dirección.'),
 ('P14-P19 / color, instalaciones, suelo, plantas, comercio y huellas','Familias 05-08 y atlas completo. El color se relaciona con componentes; los cables con recorridos; el grafiti con soportes. Suelo y plantas se explican por posición y encuentros, sin elevar los pocos emplazamientos localizados a un censo.'),
 ('P20-P25 / patios, entramados, filtros y singularidades','Se retiran las generalizaciones basadas en un único patio, entramado o rehabilitación. La celosía de la Cebada y la diagonal contemporánea quedan en el atlas como casos particulares, no patrones dominantes de Ribera.'),
 ('Flechas y dibujos','Cada caso tiene un destino físico y un texto propio. Los 16 dibujos se vinculan a dos casos identificados por familia y explican una diferencia; no añaden espesores ni soluciones internas que la foto no permite conocer.'),
 ('Límite de exhaustividad','Esta revisión no afirma haber inspeccionado todos los edificios de 600 m ni medido frecuencias poblacionales. Para eso haría falta un inventario de frentes completo y trabajo de campo homogéneo. Se entrega una muestra trazable y más próxima, no una estadística inventada.')]:
    y=p(head,42,y,W-84,12.5,bold=True)-5; y=p(txt,42,y,W-84,10.7)-16

used=sorted({v['source'] for ch in CH for v in ch['cases']}|{'RC10','RC11','RC13'})
for start in range(0,len(used),4):
    top=page('Registro visual / originales sin flechas','Posiciones y fuentes del recorrido')
    for j,sid in enumerate(used[start:start+4]):
        x=42+(j%2)*267; yy=top-(j//2)*303; src=sources[sid]
        p(f"{sid} / {src['date']}",x,yy,243,12,bold=True)
        img(src['photo'],x,yy-162,243,144)
        ty=p(f"Cámara: {src['lat']:.7f}, {src['lon']:.7f}",x,yy-175,243,9)
        ty=p('La coordenada identifica la cámara, no el portal ni el límite de parcela.',x,ty-5,243,9)
        p(f'<link href="{escape(src["url"],{chr(34):"&quot;"})}">Abrir captura original en Google Maps</link>',x,ty-8,243,10)

y=page('Registro de los frentes','Identificadores físicos utilizados en el recuento')
for b,(sid,desc) in fronts.items():
    y=p(f'<b>{b} / {sid}</b>  {escape(desc)}',42,y,W-84,10.5)-10
p('Los nombres comerciales ayudan a reconocer una imagen histórica; no garantizan que el negocio continúe abierto. La dirección mostrada por Google corresponde a la posición de cámara y puede estar en la acera opuesta al objeto descrito.',42,y-5,W-84,10)

y=page('Fuentes y reproducibilidad','Consultar, corregir y volver al lugar')
refs=[
 ('Archivo de trabajo','Cinco fotografías de correcciones IMG_1984-IMG_1988; 33 fotografías de la carpeta «fotos de patrones por la zona, esteticos». Se conserva el vínculo a cada nombre original en inventario_fotos.json.'),
 ('Enunciado G3','G3 ESP - LA MATERIA DE LO DOMÉSTICO v3.0.pdf. Programa de referencia: vivienda colectiva temporal, 20 unidades y 40 habitantes, con espacios comunes. No se convierte el programa en prueba de necesidades observadas en la calle.'),
 ('Street View','Capturas RC01-RC13 realizadas para esta revisión, con imagen histórica de julio 2021 o marzo 2022; SV016 procede del archivo anterior. Registro íntegro de enlaces y coordenadas de cámara en fuentes_capturas.json. © Google y proveedor indicado en cada imagen.'),
]
for head,txt in refs:
    y=p(head,42,y,W-84,13,bold=True)-5; y=p(txt,42,y,W-84,11)-17
links=[
 ('Ayuntamiento de Madrid: mercadillo El Rastro','https://www.madrid.es/portales/munimadrid/es/Inicio/El-Ayuntamiento/Publicaciones/Mercadillo-en-la-via-publica-El-Rastro/?vgnextchannel=e968e3d5d3e07010VgnVCM100000dc0ca8c0RCRD&vgnextfmt=default&vgnextoid=781192355c51c010VgnVCM2000000c205a0aRCRD'),
 ('Amantis: tienda de Ribera de Curtidores','https://www.amantis.net/tiendas/amantis-curtidores/'),
 ('Mensajeros de la Paz: sede y contacto','https://mensajerosdelapaz.org/quienes/nosotros/'),
 ('Farmacia Fuentecilla: referencia cartográfica OSM','https://mapcarta.com/es/N1007383075')]
for title,url in links:
    y=p(f'<link href="{escape(url,{chr(34):"&quot;"})}">{escape(title)}</link>',42,y,W-84,11)-13
y=p('Fecha de revisión: 22/09/2026. Los enlaces no alteran la antigüedad de las imágenes. No se han descargado detalles constructivos ajenos para atribuirlos a edificios locales.',42,y-10,W-84,10)-16
p('El archivo editable de datos y el generador se guardan junto al PDF en CATALOGO_CORREGIDO_RIBERA/work. Cada familia tiene una carpeta con su índice de casos; los originales permanecen sin sobrescribir.',42,y,W-84,10)

C.save()
for ch in CH:
    folder=BASE/(ch['code']+'_'+re.sub(r'[^A-Z0-9]+','_',ch['title'].upper()).strip('_'))
    folder.mkdir(exist_ok=True)
    (folder/'casos.json').write_text(json.dumps(ch,ensure_ascii=False,indent=2))
    for sid in sorted({v['source'] for v in ch['cases']}):
        shutil.copy2(sources[sid]['photo'],folder/(sid+'.png'))
(BASE/'casos_y_flechas.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(BASE/'inventario_fotos.json').write_text(json.dumps([dict(**d,analisis=FNOTES[i]) for i,d in enumerate(fields)],ensure_ascii=False,indent=2))
(BASE/'fuentes_capturas.json').write_text(json.dumps({sid:sources[sid] for sid in used},ensure_ascii=False,indent=2))
shutil.copy2(PDF,OUT/PDF.name)
print(json.dumps({'pdf':str(PDF),'pages':PAGE,'families':len(CH),'cases_per_family':[len(ch['cases']) for ch in CH],'physical_fronts':len({v['front'] for ch in CH for v in ch['cases']}),'field_photos':len(fields)},ensure_ascii=False))
