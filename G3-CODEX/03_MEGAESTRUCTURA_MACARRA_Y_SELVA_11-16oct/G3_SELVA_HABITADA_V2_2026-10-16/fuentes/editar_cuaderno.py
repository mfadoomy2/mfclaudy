from pathlib import Path
import json, shutil, textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader

R=Path(__file__).resolve().parents[1]
V=R/'vistas'
F=Path('/Users/adam/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype')
pdfmetrics.registerFont(TTFont('Body',str(F/'Carlito-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Bold',str(F/'Carlito-Bold.ttf')))
W,H=1190.55,841.89
ink='#25342f'; muted='#65736b'; bg='#f5f2e9'; yellow='#e3c83f'; green='#c4d3bc'; pink='#b82778'
c=canvas.Canvas(str(R/'PROPUESTA_SELVA_HABITADA.pdf'),pagesize=(W,H))
c.setTitle('Selva habitada | U4, conjunto y guion de exposición')
c.setAuthor('Adam | estudio de diseño con Codex')
page=0
def para(s,x,y,w=340,size=15,color=ink,bold=False):
 p=Paragraph(s,ParagraphStyle('p',fontName='Bold' if bold else 'Body',fontSize=size,leading=size*1.28,textColor=HexColor(color),spaceAfter=0))
 ww,hh=p.wrap(w,900)
 if y>41 and y-hh<45:raise ValueError('Texto fuera de página: '+s[:70])
 p.drawOn(c,x,y-hh);return y-hh-12
def start(title,sub):
 global page
 page+=1;c.setFillColor(HexColor(bg));c.rect(0,0,W,H,fill=1,stroke=0)
 para(title,40,H-34,W-80,29,bold=True)
 para(sub,42,H-78,W-84,12,muted)
 c.setStrokeColor(HexColor(ink));c.line(40,41,W-40,41)
 para('G3 / SELVA HABITADA / 16.10.2026 / PROPUESTA CONCEPTUAL V2',42,30,1000,9,muted)
 para(f'{page:02}',W-65,30,30,10,ink,True)
def end():c.showPage()
def pic(name,x,y,w,h):
 im=ImageReader(str(V/name));iw,ih=im.getSize();s=min(w/iw,h/ih)
 c.drawImage(im,x+(w-iw*s)/2,y+(h-ih*s)/2,iw*s,ih*s,mask='auto')
def blocks(items,x,y,w,size=15):
 for title,body in items:
  y=para(title,x,y,w,size+1,ink,True)
  y=para(body,x,y,w,size)-12
 return y

start('SELVA HABITADA','Una vivienda colectiva que conserva el refugio privado y multiplica los lugares comunes.')
pic('08_SELVA_EXPLORACION_FORMAL.png',40,87,800,630)
blocks([
 ('40 personas / 10 grupos U4','Hipótesis de ocupación. Cuatro habitaciones privadas por grupo, cocina y estar propios y dos baños compartidos.'),
 ('Radicalidad con reglas','Ramificar los apoyos, desplazar las bandejas, ensanchar los recorridos y repartir los usos. Los vacíos y los umbrales también organizan el conjunto.'),
 ('Dos documentos distintos','Esta imagen generada explora el carácter formal. El Rhino adjunto controla un primer encaje y tiene cinco niveles más regulares. Aún falta coordinar ambas versiones geométricamente.')],870,695,275,16)
end()
start('01 / Por qué elijo una casa para cuatro','Decisión de proyecto, no proporción observada en la acampada ni conclusión sociológica sobre toda la juventud.')
blocks([
 ('Habitar implica poder retirarse','La habitación debe permitir dormir, estudiar, guardar cosas y cerrar la puerta. Lo compartido empieza fuera de ese límite; la intimidad no se sacrifica para conseguir una imagen colectiva.'),
 ('Cuatro permite una escala doméstica','Una mesa, una cocina y dos baños pueden pertenecer a un grupo reconocible. Elegir cuatro reduce el número de personas que deben acordar las tareas diarias; sigue siendo una hipótesis que habría que contrastar con residentes.'),
 ('El conjunto añade posibilidades','La cantina, el taller, la lavandería y el aula amplían la vida doméstica. La cocina de grupo permite decidir cuándo participar. Compartir debe ofrecer recursos, no imponer disponibilidad social permanente.')],45,695,340,17)
pic('07_U4_EXPLORACION_FORMAL.png',415,150,735,550)
para('EXPLORACIÓN GENERADA / interpreta curvatura, material y vida cotidiana; no sustituye la planta acotada.',430,115,700,12,muted)
end()
start('02 / La unidad: cuatro refugios y un centro doméstico','Planta obtenida del modelo. Las superficies útiles y brutas se distinguen; medidas aún de anteproyecto.')
pic('01_UNIDAD_PLANTA.png',40,75,785,640)
blocks([
 ('11,30 × 9,20 m','Envolvente rectangular máxima. La bandeja curva ocupa 102,86 m² brutos. Cada habitación tiene unos 12,15 m² útiles geométricos, antes de descontar el mobiliario.'),
 ('Cocina al fondo','La encimera ya no invade el acceso lateral. Mesa y sillas quedan fuera de la franja transversal nominal de 1,60 m. El común central reserva 25,74 m² brutos.'),
 ('Dos baños / cuatro personas','Dos piezas de 5,07 m² brutos cada una. Su accesibilidad y maniobras no están verificadas. La unidad incorpora almacenamiento privado y una reserva de servicios.'),
 ('Umbral que se puede cerrar','El enlace lateral es una posibilidad entre grupos, no una calle pública que atraviese la vivienda. Falta desarrollar el cierre y el control de este límite en el modelo.')],850,700,295,15)
end()
start('03 / La vida cotidiana decide el espacio','Imagen de ambiente generada: cocina de grupo, puertas privadas y relación visual con la galería.')
pic('09_INTERIOR_EXPLORACION_FORMAL.png',40,195,1110,520)
blocks([('Privado','Habitación, descanso, estudio y pertenencias. Puerta, opacidad y aislamiento acústico por desarrollar.')],45,162,330,15)
blocks([('Compartido por cuatro','Cocina, mesa, estar, baños y limpieza cotidiana. La casa puede funcionar sin usar la cantina.')],425,162,330,15)
blocks([('Compartido por cuarenta','Lavandería, taller, aula, cantina y espacios de reunión. Acceso desde la red exterior a las unidades.')],805,162,330,15)
end()
start('04 / Del grupo a la comunidad','Una unidad se conecta a la infraestructura común; la circulación del conjunto rodea su intimidad.')
pic('02_PARCELA_IMPLANTACION.png',40,300,1110,410)
blocks([('Regla de conexión','Cada U4 tiene un acceso desde una galería. Agrupar significa conectar umbrales y servicios, conservando la autonomía doméstica. Las uniones no convierten los dormitorios en paso.')],45,263,330,16)
blocks([('Regla de variación','En el ensayo hay dos U4 por nivel, desplazadas dentro del lindero. La siguiente versión formal debe variar también los claros y los ramales: el apilamiento actual todavía es demasiado regular para expresar toda la selva.')],425,263,330,16)
blocks([('Regla de continuidad','Dos núcleos con reservas de escalera y ascensor conectan las cotas. El itinerario accesible y la evacuación completa quedan pendientes. La única llegada a la calle dibujada está en el frente oeste.')],805,263,330,16)
end()
start('05 / Escalar exige recomponer','Se mantiene el tamaño del cuerpo humano. Se cambia la cantidad, la luz entre apoyos y la distribución de los espacios.')
pic('03_CAMBIO_ESCALA.png',40,330,1110,380)
blocks([('Conservar','Bandejas curvas, bifurcaciones, diagonales, cubiertas parciales y diferencia entre refugio y claro. La identidad macarra debe aparecer también en la sección y el recorrido.')],45,295,330,16)
blocks([('Quitar o reducir','Escaleras que no llevan a usos, raíces flotantes, puentes redundantes sin destino y una cubierta gigantesca sin necesidad climática clara. No se reduce una cama o una puerta para que quepa la forma.')],425,295,330,16)
blocks([('Añadir y reorganizar','Dos núcleos de conexión, espacios técnicos, cocina y baños cercanos, almacenamiento, envolvente doméstica y recorridos continuos. El solar estrecho obliga a estirar y redistribuir la organización.')],805,295,330,16)
end()
start('06 / Cinco órdenes que se coordinan','La forma se explica mediante jerarquías de privacidad, carga, movimiento, servicios y clima.')
pic('04_UNIDAD_AXONOMETRIA.png',40,225,620,490)
blocks([
 ('1. Estructura primaria','Troncos y ramas propuestos recogen las bandejas y deben transmitir las cargas a cimentación. Material y secciones no están calculados. Las dimensiones dibujadas solo representan el sistema.'),
 ('2. Estructura secundaria','Vigas de bandeja y costillas de cubierta. Las costillas se han sacado del volumen interior. Una eventual suspensión local necesitaría un marco superior y anclajes que hoy no están resueltos.'),
 ('3. Circulación y umbrales','Calle → acceso → núcleo → galería → casa U4 → habitación. La galería pertenece al conjunto; el estar pertenece al grupo.'),
 ('4. Infraestructura','Cocina y baños alimentan ramales registrables hacia montantes comunes. Drenaje por gravedad, pendientes, protección contra incendios y accesos de mantenimiento pendientes.'),
 ('5. Envolvente y clima','Recinto doméstico estanco y aislado, más protecciones exteriores parciales. Las velas no sustituyen impermeabilización, aislamiento ni acústica. Sombra, lluvia y desagüe deben decidir su geometría.')],700,705,445,15)
para('Lectura de cargas propuesta: uso → suelo → vigas de bandeja → ramas → troncos → cimentación. Las velas transmiten sus propias acciones de viento a los anclajes; no sostienen las viviendas.',45,185,610,17,ink,True)
end()
start('07 / Programa y encaje: números que no se esconden','Parcela del archivo: 650,91 m². Ensayo de 40 residentes; objetivo previo de 1.500 m² aún provisional.')
rows=[('10 unidades U4','1.028,59 m²','Cuatro habitaciones por unidad'),('Reserva de dos núcleos','334,08 m²','Huella bruta en seis cotas; incluye huecos'),('Programa comunitario','187,40 m²','Acogida 22,8; lavado 20; técnica 22,5; tres salas de 40,7'),('Total de estudio','1.550,07 m²','50,07 m² por encima del objetivo (+3,34 %)'),('Galerías y claros abiertos','455,62 m²','Se informan aparte; no se presupone exención urbanística')]
y=699
for idx,(a,b,d) in enumerate(rows):
 c.setFillColor(HexColor(green if idx==3 else '#e9e8dc'));c.rect(45,y-66,1100,66,fill=1,stroke=0)
 para(a,58,y-12,280,17,ink,True);para(b,355,y-12,180,19,ink,True);para(d,560,y-12,560,15)
 y-=75
blocks([('Dónde se sitúa lo común','En planta baja: acogida y cuidados, lavado y técnica. A +4,20 m: cantina; a +8,40 m: claro de reunión; a +12,60 m: taller; a +21,00 m: aula y trabajo. Esta distribución reparte destinos, pero el aula alta debe revisarse si prima su acceso público.')],45,280,520,16)
blocks([('Qué se ha comprobado','Diez huellas U4 dentro de la parcela y sin solaparse entre sí en cada nivel. Cinco cotas: +4,20 / +8,40 / +12,60 / +16,80 / +21,00 m. Velas hasta +25,60 m. Altura, edificabilidad, luz, accesibilidad, fuego y estructura NO están validados.')],625,280,520,16)
end()
start('08 / Lo que ya existe y lo que queda por resolver','Este cuaderno es una propuesta conceptual inspeccionable, con un modelo de encaje; no es un proyecto constructivo.')
pic('05_CONJUNTO_GEOMETRIA.png',40,230,690,480)
blocks([
 ('Rhino editable','Dos archivos separados: unidad U4 y conjunto con contexto. Geometría en mallas por capas, en metros; no son sólidos constructivos ni un modelo BIM.'),
 ('Conflictos por estudiar','Ventanas frente a vecinos, interferencias completas con soportes, giros y pendientes accesibles, compartimentación, evacuación hasta calle y efecto del viento sobre las velas.'),
 ('Próxima decisión formal','Trasladar al Rhino los ramales, vacíos y plataformas más diversos de la imagen, sin perder habitaciones, anchos y acceso. La imagen y el modelo aún no describen una única solución coordinada.')],770,700,375,16)
para('La radicalidad se mantiene como criterio de proyecto. La forma de comprobarla será exigir que cada bifurcación produzca un uso, una relación espacial o una condición climática concreta.',45,173,1085,20,ink,True)
end()

guion=[
('1. La idea de partida','Quiero trasladar a la vivienda la capacidad de una acampada para construir vida común mediante refugios, recorridos y lugares de encuentro. No copio literalmente la tienda ni convierto la precariedad en una estética doméstica. Tomo la relación entre un lugar propio y una infraestructura compartida. La propuesta es una selva habitable: muchas piezas y conexiones, con reglas que permiten entender cómo se vive en ella.'),
('2. Por qué una unidad para cuatro','He elegido cuatro personas como primer grupo de convivencia. Si toda la vida doméstica dependiera de cuarenta residentes, cocinar o descansar exigiría demasiada negociación. Si cada habitación fuera una vivienda completamente autónoma, repetiríamos muchos servicios y reduciríamos los motivos cotidianos para encontrarnos. Por eso cada persona tiene una habitación privada y cada grupo tiene una casa común que puede funcionar por sí misma.'),
('3. Cómo funciona la distribución','La unidad mide aproximadamente once metros treinta por nueve metros veinte y ocupa unos ciento tres metros cuadrados brutos. Cuatro habitaciones rodean el centro doméstico. Cada una permite colocar cama, mesa y armario, con unos doce metros cuadrados útiles geométricos. En el centro están la cocina, la mesa y el estar; junto a ellos hay dos baños. He llevado la cocina al fondo para liberar el paso transversal y separar entrar en casa de cocinar.'),
('4. Qué es privado y qué se comparte','Distingo cuatro escalas. La habitación es individual. Cocina, estar y baños pertenecen a cuatro personas. Lavandería, taller, cantina y aula pertenecen al conjunto. Algunos usos pueden relacionarse con el barrio mediante horarios y accesos acordados. Compartir una cocina no convierte la habitación en espacio público. Tampoco obliga a asistir a una actividad colectiva: la posibilidad de retirarse forma parte del proyecto.'),
('5. Qué sucede al juntar unidades','Cada unidad se conecta a una galería mediante un umbral. La galería lleva a los núcleos y a los equipamientos sin atravesar una vivienda. Las unidades pueden acercarse, desplazarse o dejar un claro entre ellas. Lo que se repite es el acuerdo entre acceso, privacidad, servicios y soporte, no necesariamente una posición idéntica. En este primer Rhino hay diez unidades, dos por nivel, para cuarenta personas; esa disposición todavía necesita una variación espacial mayor.'),
('6. Qué ordena la selva','Uso tres reglas espaciales. Primero, toda pieza tiene un destino habitable: no dibujo puentes solo por su imagen. Segundo, las zonas de estancia se ensanchan fuera del paso necesario. Tercero, cada bifurcación debe poder leerse desde el recorrido: se entiende si conduce a una casa, a un equipamiento o a un claro. El zigzag permite mirar en distintas direcciones y encontrarse a diferentes distancias, pero no puede convertir la orientación en un laberinto.'),
('7. Cómo se sostiene','La hipótesis estructural tiene una jerarquía. El suelo de cada unidad descarga en las vigas de su bandeja; estas transmiten las cargas a ramas y troncos, y finalmente a la cimentación. Una estructura secundaria sostiene las cubiertas y cerramientos. En este modelo las bandejas están principalmente apoyadas en ramas. La suspensión más intensa de las imágenes requiere desarrollar marcos superiores, tirantes y anclajes; todavía no puedo presentarla como resuelta. También falta definir la estabilidad frente al viento y las cargas asimétricas.'),
('8. Cómo se organizan servicios y clima','La forma curva no significa que todas las instalaciones deban retorcerse. Los baños y la cocina se conectan mediante recorridos cortos y registrables a montantes comunes. Los desagües necesitan pendientes reales y las redes deben poder mantenerse sin invadir habitaciones. Además separo el recinto doméstico de las protecciones exteriores: la vivienda necesita aislamiento, estanqueidad y acústica; las velas aportan sombra y protección parcial. Sus puntos bajos deben recoger agua y sus anclajes resistir el viento.'),
('9. Cómo funciona el programa colectivo','En la planta baja sitúo acogida y cuidados, lavandería y espacio técnico. En altura aparecen cantina, taller, aula y lugares abiertos de reunión. Así los recorridos conectan actividades y no solo puertas. La cantina complementa la cocina de grupo: no la sustituye. El taller comparte herramientas y permite reparar; la lavandería evita repetir máquinas; el aula puede acoger trabajo y aprendizaje. El acceso del barrio debe ser controlable sin atravesar el espacio privado de las casas.'),
('10. Qué cambia al entrar en la parcela','No aplico un único factor de escala a la megaestructura. La cama, la puerta y el cuerpo mantienen sus medidas. Lo que cambia es cuántas piezas hay, cómo se distribuyen, cuánto separan los apoyos y qué partes dejan de tener función. Quito conexiones sin destino y grandes gestos que no responden al lugar. Añado núcleos, instalaciones y límites domésticos. Mantengo curvas, bifurcaciones y cubiertas parciales, adaptándolas a una parcela alargada y a sus vecinos.'),
('11. Cómo se gestiona lo común','Propongo que las reglas de uso sean parte del diseño: quién accede, dónde se guarda, cómo se limpian los baños, cómo se reservan las salas y quién mantiene las instalaciones. Son acuerdos que deben construir los residentes, no comportamientos que la forma impone por sí sola. La gestión colectiva y el derecho a la intimidad deben apoyarse mutuamente. Los espacios deben admitir cambios de grupo y diferentes grados de participación sin expulsar a quien necesita más tranquilidad.'),
('12. Qué puedo defender hoy','Puedo defender la jerarquía entre habitación, grupo, comunidad y barrio; el programa propuesto; y un primer encaje de diez unidades dentro del lindero, sin solapamientos entre sus huellas en un mismo nivel. El cómputo de estudio ronda mil quinientos cincuenta metros cuadrados, más galerías abiertas: todavía supera el objetivo inicial. No están comprobados la estructura, la normativa, la evacuación, la accesibilidad completa ni la iluminación entre vecinos. La imagen radical marca una dirección; falta coordinar esa forma con el modelo medido.')]
for k in range(3):
 start(f'GUION / {k+1} de 3','Texto para exposición oral / aproximadamente 9-11 minutos en total / hablar señalando plantas, sección e imágenes.')
 for j,(title,body) in enumerate(guion[k*4:k*4+4]):
  x=45+(j%2)*575;y=700-(j//2)*310
  para(title,x,y,525,22,ink,True)
  para(body,x,y-42,525,17)
 end()
start('FUENTES / De la investigación a una decisión de proyecto','Fuentes primarias recuperadas en la investigación previa del 11.10.2026. Las ofertas y comunicados se leen con su fecha.')
sources=[
 ('Urbanismo / circulación, perímetro y vacantes','https://madrid.acampada26s.net/c/blog/comunicado-de-comision-de-urbanismo-slaw2peq?lang=es','Lectura de proyecto: recorridos continuos y límites de privacidad. No prescribe el grupo de cuatro.'),
 ('Lluvia / mantenimiento y respuesta colectiva','https://madrid.acampada26s.net/c/blog/lluvia-plan-de-accion-urgente-7cbdxyly?lang=es','Lectura de proyecto: el agua exige recogida, reparación y organización, además de una cubierta.'),
 ('Comisiones / tareas e infraestructura social','https://madrid.acampada26s.net/c/blog/informacion-comisiones-8x0z0hat?lang=es','Lectura de proyecto: cuidados, limpieza y logística deben tener espacio y gestión.'),
 ('@acampada26s / red de apoyos del barrio','https://www.instagram.com/acampada26s/p/DeMxO6BiL8w/','Publicación de 7 de octubre consultada en el archivo de investigación: apoyos distribuidos para necesidades cotidianas.'),
 ('@inquilinato_madrid / organización territorial','https://www.instagram.com/inquilinato_madrid/p/DeFTuGBjuNN/','Referencia de organización colectiva. No se equiparan automáticamente sus nodos con unidades residenciales.')]
y=700
for title,url,body in sources:
 y=para(title,45,y,1100,18,ink,True)
 y=para(body,45,y,1100,14)
 y=para(f'<link href="{url}" color="#b82778">{url}</link>',45,y,1100,11)-15
para('Archivos de partida: MEGAESTRUCTURA_MACARRA.3dm; parcela_local.geojson y contexto.npz del estudio G3 de 05.10.2026. El material del profesor se usa como referencia, no como instrucción de repetir su solución. Los renders son imágenes generadas; los seis primeros dibujos proceden del modelo de ensayo. No se afirma una nueva revisión completa de Instagram o TikTok en esta entrega.',45,175,1100,14)
end();c.save()

md='# Guion de exposición | Selva habitada\n\nVersión conceptual 2 · 16 de octubre de 2026\n\nDuración orientativa: 9-11 minutos. Las dimensiones son de ensayo; no equivalen a un proyecto constructivo.\n\n'
md+='\n\n'.join('## '+a+'\n\n'+b for a,b in guion)
md+='\n\n## Qué mostrar mientras hablas\n\n1. Imagen del conjunto: apartados 1-2.\n2. Planta U4 e interior: apartados 3-4.\n3. Implantación y modelo del conjunto: apartados 5-6.\n4. Axonometría de la unidad: apartados 7-8.\n5. Cuadro de programa y cambio de escala: apartados 9-10.\n6. Comparar imagen generada y Rhino: apartados 11-12.\n'
(R/'GUION_EXPOSICION.md').write_text(md)
(R/'LEEME.md').write_text('''# Selva habitada | V2 | 16.10.2026

Propuesta conceptual de unidad U4 y primer encaje para 40 residentes. La forma radical de la imagen generada y el modelo de encaje no están todavía coordinados pieza por pieza.

## Contenido

- PROPUESTA_SELVA_HABITADA.pdf: 13 láminas A3 horizontales; propuesta, dibujos, programa, guion oral y fuentes.
- GUION_EXPOSICION.md: texto editable para explicar distribución, estructura, reglas, programa y gestión.
- modelos/01_UNIDAD_U4.3dm: unidad en metros, mallas por capas.
- modelos/02_SELVA_EN_PARCELA.3dm: diez unidades, núcleos, programa, galerías y contexto en metros.
- vistas/01-06: proyecciones y diagramas del ensayo geométrico, PNG y SVG.
- vistas/07-09: exploraciones generadas; no son documentación métrica.
- fuentes/: generador geométrico, editor del cuaderno y prompts de las nuevas imágenes.
- verificacion/: comprobaciones geométricas limitadas y revisión del paquete.

## Límites del estudio

Los 1.550,07 m² suman unidades, reserva bruta de núcleos y programa comunitario; los núcleos incluyen sus huecos. Se añaden 455,62 m² de galerías y claros abiertos. No se presume cómo computan urbanísticamente. El objetivo previo de 1.500 m² y las 40 personas se mantienen como hipótesis.

Se comprueba el lindero de las huellas U4 y la ausencia de solapes entre unidades de un mismo nivel. No se ha validado la normativa, la estabilidad, las cimentaciones, la suspensión, la accesibilidad, el fuego, el confort, la iluminación ni todas las interferencias tridimensionales. Las secciones estructurales son gráficas, no calculadas. La única salida a calle representada es la del frente oeste; el fondo no se considera otra calle.

Esta V2 libera el acceso de la cocina, desplaza las costillas fuera de las habitaciones y añade huecos a las escaleras. No modifica los originales ni sustituye la megaestructura macarra de partida.

## Procedencia

Modelo original: /Users/adam/Downloads/MEGAESTRUCTURA_MACARRA/modelo/MEGAESTRUCTURA_MACARRA.3dm

Parcela y contexto: /Volumes/T7/G3 Proyectos/G3 CLAUDE/01_E2_IMAGINARIOS_PERSONAS_Y_MECANISMOS_05-06oct/G3_MECANISMOS_EN_PARCELA_2026-10-05/geometria/

Investigación previa: /Users/adam/Downloads/G3_SOL_MEGAESTRUCTURA_2026-10-11/

Reproducir dibujos y modelos: uv run --with rhino3dm --with numpy --with shapely --with matplotlib python fuentes/disenar_selva.py

Reproducir PDF: uv run --with reportlab python fuentes/editar_cuaderno.py
''')
print('PDF',page,'páginas; guion',len(md.split()),'palabras')
