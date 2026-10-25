# 150 escenas de cómo vive la juventud hoy, y lo que tienen en común

25 de octubre de 2026. Esto responde a la corrección de Adam de esa misma tarde: la unidad no sale de la encuesta ni de las 20 acciones, sale de **cómo vive la juventud hoy**, contado en muchas escenas; de lo que esas escenas tienen en común sale el foco de la unidad, y solo después se diseña. La radicalidad buscada es de programa (qué contiene la unidad), no solo de forma: la unidad infinita de Superstudio o la unidad-cama de María Palacios.

Archivo de datos: `escenas.csv` (una fila por escena, con etiquetas). Conteo: `fuentes/contar_escenas.py`. Este documento es la lectura.

## De dónde salen las escenas

Cada escena lleva su fuente. Se distingue lo que está en la investigación del proyecto de lo que es hipótesis mía:

| Fuente | Qué es | Escenas |
|---|---|---|
| **Home Alone** | Panel de Fase 1 (`más investigación…/HOME ALONE.pdf`): el joven de hoy abre el portátil en la cama, trabajo y ocio en el mismo metro cuadrado, cuarto como refugio insonorizado a base de cascos, casa como «base de operaciones temporal», azotea para ver el cielo. | 27 |
| **Sol** | Acampada del 26S: testimonios de prensa (Irene, Laura, Andrea, Jairo, Iona, Jorge Collado, Elena Mercero, María Barrier, Pepe), rotación, turnos de 7 h, sacos compartidos, comisiones, cocina externa, punto violeta, comités de barrio (`G3_Acampada_Sol_conversacion.md`, `base.txt`). | 39 |
| **Compendio** | Fase 1, III.2 «Qué significa joven»: cuatro situaciones (primera emancipación, trabajo inestable, residencia prolongada, convivencia de dos) y lo que cada una no quiere compartir. | 9 |
| **Rastro** | Investigación del lugar: el domingo, vender en el suelo, segunda mano, el bar como salón, la calle como extensión de la casa. | 8 |
| **Escena anterior** | Las S01–S16 de Codex que siguen valiendo, reescritas. | 12 |
| **Autor** | Lo que es específico de un estudiante de arquitectura. | 2 |
| **Hipótesis** | Hábitos de la generación Z que aporto yo y que **no están en el repositorio**: redes, series, juegos, apps, delivery, salud mental, citas, mascotas. Son verosímiles, pero no están medidos. | 53 |

Las 53 hipótesis son un tercio. Por eso, en el conteo, cada cifra importante se da también **sin ellas**, para ver si el resultado se sostiene con la investigación sola.

## Cómo se leen

Cada escena tiene hora, día (laborable, noche, fin de semana) y seis etiquetas:

- **cuerpo:** tumbada, sentada, de pie, moviéndose;
- **lugar:** cama, suelo, mesa, cocina, baño, umbral (puerta, pasillo, portal, ventana), común (salón, lavadero), fuera;
- **con quién:** sola; sola pero conectada (el cuerpo solo y la compañía por pantalla); otra persona; grupo; desconocidos;
- **pantalla:** si interviene una pantalla;
- **exposición:** lo que esa persona necesita respecto a ser vista u oída: ocultarse, controlar lo que se ve y se oye, mostrarse, o le da igual;
- **dura:** minutos, una hora, horas, la noche entera.

Las etiquetas las he puesto yo leyendo cada escena. Otra persona etiquetaría algunas de otra manera; las cifras tienen ese margen.

## Las 150 escenas

### Laborable, de 7:00 a 22:00

- **E001** · 07:10 · Suena la alarma del móvil debajo de la almohada; la apaga y mira notificaciones 12 min sin levantarse. *[Home Alone]*
- **E002** · 07:30 · Desayuna de pie en la cocina mirando el móvil: café de cápsula y una tostada, 6 min. *[Home Alone]*
- **E003** · 07:45 · Se ducha en 5 min porque la compañera espera; se seca el pelo en el cuarto con la puerta cerrada. *[compendio]*
- **E004** · 08:05 · Sale con la mochila siempre hecha: portátil, cargador, táper, cascos; 45 min de cercanías. *[Home Alone]*
- **E005** · 08:30 · Teletrabajo: abre el portátil en la mesa del salón porque el cuarto no tiene mesa; la compañera desayuna al lado. *[Home Alone]*
- **E006** · 09:00 · Entrevista de trabajo por videollamada desde la cama hecha; sube el portátil sobre libros para que la cámara no enseñe la ropa. *[compendio · situación B]*
- **E007** · 09:30 · Clase online con la cámara apagada; sigue en pijama, micrófono en silencio, chat abierto con amigas. *[hipótesis]*
- **E008** · 10:15 · Llega un paquete; el repartidor llama a todos los timbres; baja en chanclas a recogerlo. *[hipótesis]*
- **E009** · 10:40 · Hace la cama solo cuando va a tener videollamada: la cama es el fondo de cámara. *[Home Alone]*
- **E010** · 11:00 · Estudia con un temporizador de 25 min y el móvil boca abajo; en cada descanso, scroll. *[hipótesis]*
- **E011** · 11:30 · Vuelve de un turno de guardia de 7 h en la acampada y duerme a mediodía con la persiana bajada. *[Sol · Laura]*
- **E012** · 12:00 · Duerme de día después de cerrar un bar a las 4; el resto del piso vive en voz baja. *[compendio · situación B]*
- **E013** · 12:30 · Calienta el táper de ayer y come en el cuarto para no cruzarse con nadie. *[escena anterior · S05]*
- **E014** · 13:00 · Reparte a domicilio en bici: el cuarto es donde carga la batería y deja la mochila térmica. *[hipótesis]*
- **E015** · 13:30 · Come en el suelo con el portátil en la silla porque la mesa está llena de cosas de otra. *[Home Alone]*
- **E016** · 14:00 · Videollamada con su madre mientras come; le enseña el cuarto girando el móvil. *[hipótesis]*
- **E017** · 14:30 · Trabajo en grupo por llamada: cuatro pantallas, cada una en su cama en un barrio distinto. *[Home Alone]*
- **E018** · 15:00 · Calor: videollamada con el ventilador al lado; cierra las contraventanas y trabaja a oscuras. *[escena anterior · S12]*
- **E019** · 15:30 · Siesta de 20 min con el móvil en el pecho y una alarma puesta. *[hipótesis]*
- **E020** · 16:00 · Gimnasio en el cuarto: esterilla entre la cama y el armario, vídeo de 30 min, la vecina de abajo lo oye. *[Home Alone]*
- **E021** · 16:30 · Mira pisos en Idealista tumbada; guarda cinco; ninguno baja de 700 €. *[Sol · Elena Mercero]*
- **E022** · 17:00 · Café con wifi: en casa no hay sitio para trabajar sin oír la tele del salón. *[Home Alone]*
- **E023** · 17:30 · Biblioteca pública hasta que cierra; la casa es solo para dormir. *[Home Alone]*
- **E024** · 18:00 · Llega con la compra y la mochila, abre con el codo y lo deja todo en el suelo del cuarto. *[escena anterior · S15]*
- **E025** · 18:20 · Audios de WhatsApp a volumen alto mientras ordena; al otro lado del tabique se oyen enteros. *[hipótesis]*
- **E026** · 18:40 · Se encierra con cascos: el cuarto no aísla, los cascos sí. *[Home Alone]*
- **E027** · 19:00 · Terapia online desde el único sitio donde no la oyen: el baño. *[hipótesis]*
- **E028** · 19:30 · Cocina deprisa en una cocina saturada: tres personas, dos fuegos, un fregadero. *[Home Alone]*
- **E029** · 20:00 · Cena en la cama viendo una serie, el plato sobre la rodilla, la luz apagada. *[Home Alone]*
- **E030** · 20:30 · Cuatro cocinan doce raciones; alguien solo quiere calentar su táper y marcharse. *[escena anterior · S05]*
- **E031** · 21:00 · Ve la serie «juntas» con una amiga en otra ciudad: la misma pantalla sincronizada y el chat al lado. *[hipótesis]*
- **E032** · 21:30 · Pide comida a domicilio a medias con la compañera; comen en el sofá, cada una con su móvil. *[hipótesis]*
- **E072** · 09:50 · Calendario de limpieza en la nevera que nadie mira; la foto de la cocina sucia va al chat. *[escena anterior · S14]*
- **E073** · 20:10 · Habitación de 689 € con alguien que no elegiste; se cruzan en el pasillo sin hablar. *[Sol · base.txt: no eliges con quién]*
- **E074** · 19:45 · La puerta cerrada es la señal; nadie llama. *[compendio]*
- **E076** · 16:20 · Acompaña a alguien que está mal: sentadas en el suelo del pasillo, sin encender la luz. *[escena anterior · S10]*
- **E077** · 10:05 · Bizum del alquiler el día 1: 689 €, el sueldo entero, y el mensaje «ya está». *[Sol · Elena Mercero]*
- **E078** · 11:30 · Visita del casero: esconde al gato, descuelga la pancarta y quita el colchón del suelo. *[hipótesis]*
- **E079** · 08:50 · Maleta sin deshacer tres meses: vive desde la maleta abierta sobre una silla. *[Home Alone · base de operaciones temporal]*
- **E080** · 21:15 · Nada en las paredes: una tira de luces LED y fotos con cinta; todo se quita en 10 min. *[Home Alone]*
- **E087** · 07:20 · Tres horas de transporte al día: el cercanías es la habitación donde lee, duerme y contesta. *[Sol · Jairo]*
- **E088** · 09:20 · Una planta en un jarrón del Rastro: lo único que cuida y lo único que no es de nadie más. *[Home Alone · el jarrón como supervivencia emocional]*
- **E090** · 19:15 · Compra online todo lo pequeño; el portal se llena de cajas de otras. *[hipótesis]*
- **E092** · 17:40 · Regla con dolor: bolsa de agua caliente, cama, serie y aviso en el chat de que hoy no cocina. *[hipótesis]*
- **E093** · 13:00 · Enferma: quiere retirarse sin desaparecer; alguien le deja sopa en la puerta. *[escena anterior · S16]*
- **E095** · 07:55 · Meditación con una app, diez minutos sentada en el suelo entre la cama y la puerta. *[hipótesis]*
- **E096** · 20:00 · Tres días sin salir del cuarto; la comida llega a la puerta; el chat del piso pregunta si está bien. *[hipótesis]*
- **E097** · 18:50 · Estira en el suelo con la espalda rota de trabajar en la cama. *[Home Alone]*
- **E098** · 07:00 · Corre por la Ribera a las 7 con cascos y se ducha en 4 min antes de que se levante nadie. *[Home Alone]*
- **E100** · 17:00 · Cuida de la hija de otra residente dos tardes; la cama hace de parque. *[Sol · chiqui-asamblea]*
- **E102** · 21:40 · Se depila con un espejo de mano en la cama porque la luz del baño es mala. *[hipótesis]*
- **E106** · 09:00 · Teleoperador desde el cuarto: auriculares, guion, 8 h; el micrófono capta la lavadora. *[Sol · Pepe]*
- **E108** · 10:00 · Oposiciones: 8 h en la misma silla; el cuarto es el aula; tapones de cera. *[compendio · situación B]*
- **E110** · 17:30 · Clase particular por videollamada a un niño; el fondo tiene que parecer una oficina. *[hipótesis]*
- **E111** · 11:00 · Vende por Instagram lo que hace: fotos en el suelo con la buena luz de las 11. *[Rastro]*
- **E112** · 16:30 · Turno partido: vuelve a casa 2 h a dormir entre dos turnos, vestida. *[compendio · situación B]*
- **E113** · 21:00 · Rellena un formulario de ayudas en el móvil, en la cama, con el DNI al lado; se cuelga en el paso 4. *[hipótesis]*
- **E114** · 20:30 · Pide un adelanto a un amigo por Bizum para llegar al día 1. *[Sol]*
- **E115** · 08:20 · Lleva el portátil al baño para seguir una reunión mientras hace cola para la ducha. *[Home Alone]*
- **E116** · 21:30 · Asamblea del piso en el salón: 40 min para decidir el wifi; se vota a mano alzada como en Sol. *[Sol]*
- **E117** · 19:30 · Asamblea online del comité de barrio: 30 cuadrados, la mitad sin cámara, desde las camas. *[Sol · comités de barrio]*
- **E118** · 12:30 · Caja de resistencia: cada una pone 10 € para la multa de otra. *[Sol]*
- **E119** · 18:10 · Se prestan el taladro, la plancha y la maleta; hay un inventario en el chat. *[Sol]*
- **E121** · 20:00 · Huelga de alquileres: reunión con la vecina del 2.º en la escalera para no pagar el mismo mes. *[Sol · Sindicato de Inquilinas]*
- **E123** · 14:00 · Reparte la comida de la cocina externa en la plaza: 300 raciones en 40 min. *[Sol]*
- **E124** · 16:00 · Biblioteca de la acampada: libros que llegan en especie y se llevan sin registro. *[Sol]*
- **E125** · 08:00 · El saco de dormir compartido: lo usa una de día y otra de noche. *[Sol · sacos que pasan de mano en mano]*
- **E127** · 18:00 · Redibuja el plano de la plaza a mano en una libreta cada vez que llegan tiendas nuevas. *[Sol · Alejandro T.]*
- **E129** · 21:00 · Directo en Instagram desde la acampada bajo la lluvia: 2.000 personas mirando una tienda. *[Sol]*
- **E133** · 18:30 · Tirada 40 min sin hacer nada; no es descanso, es no poder. *[hipótesis]*
- **E138** · 17:15 · Toca la guitarra con los cascos enchufados a un amplificador de 5 W para no molestar. *[hipótesis]*
- **E140** · 16:45 · Dibuja con la tableta tumbada boca abajo en la cama. *[autor]*
- **E141** · 09:40 · Tres macetas del Rastro en la ventana y una cuerda; riega desde la cama con un vaso. *[Home Alone]*
- **E146** · 07:40 · Contesta mensajes de trabajo desde la cama antes de levantarse; el día empieza acostada. *[Home Alone]*
- **E148** · 19:00 · Graba un pódcast con una amiga con el edredón por encima para que no resuene. *[hipótesis]*
- **E149** · 21:50 · Deja la puerta del cuarto abierta a propósito: hoy quiere que alguien entre a hablar. *[compendio]*

### Laborable, de 22:00 a 7:00

- **E033** · 22:00 · Graba un vídeo para redes con el móvil apoyado en un vaso; necesita fondo limpio y luz; lo repite nueve veces. *[Sol · María Barrier creadora de contenido]*
- **E034** · 22:30 · Hay cena y conversación en el salón; una quiere ducharse y acostarse sin explicar nada. *[escena anterior · S08]*
- **E035** · 23:00 · Juega online con cascos y micro hasta las 3; habla en voz alta; el tabique no lo para. *[hipótesis]*
- **E036** · 23:30 · Pone la lavadora a las 23:30 porque es la única hora en que está libre. *[escena anterior · S11]*
- **E049** · 06:00 · Turno de las 6: sale sin desayunar, con el café en vaso de papel y el móvil al 18 %. *[compendio · situación B]*
- **E050** · 06:30 · En una cocina externa preparan 60 kg de comida caliente para la plaza; empieza a las 8. *[Sol]*
- **E071** · 22:15 · Grupo de WhatsApp del piso: la limpieza se discute por escrito; nadie sale al pasillo. *[hipótesis]*
- **E075** · 23:45 · La pareja viene a dormir tres noches por semana y se convierte en cuarta compañera sin pagar. *[hipótesis]*
- **E085** · 22:40 · Alquiló tres meses y volvió con sus padres; el cuarto de la infancia con el portátil de ahora. *[Sol · Jorge Collado]*
- **E086** · 23:10 · Vive con su abuela: estudia en la mesa de la cocina de noche, cuando ella se acuesta. *[Sol · Iona]*
- **E091** · 22:20 · Ducha larga: el único sitio con pestillo y vapor donde nadie entra; 25 min hasta que se acaba el agua caliente. *[hipótesis]*
- **E094** · 23:20 · Cuidado de la piel en doce pasos delante del móvil con un aro de luz; el baño está ocupado. *[hipótesis]*
- **E101** · 23:00 · Toma la pastilla a la misma hora cada noche: alarma del móvil y vaso de agua en el suelo. *[hipótesis]*
- **E103** · 23:30 · Perro pequeño en un piso que no lo permite; lo saca por la escalera de atrás. *[hipótesis]*
- **E105** · 22:50 · Lava la ropa interior a mano en el lavabo y la seca en el radiador del cuarto. *[Home Alone]*
- **E120** · 23:00 · Pintan carteles en el suelo del pasillo la noche antes de la manifestación. *[Sol]*
- **E126** · 22:00 · Montan una tienda de 2 × 2 en 10 min con cinta y lona contra la lluvia. *[Sol]*
- **E130** · 23:30 · Vuelve a dormir a casa de sus padres y a la plaza a las 7: la tienda queda vacía 8 h. *[Sol · rotación]*
- **E131** · 23:15 · App de citas en la cama: ocho conversaciones, ninguna cita; la foto del perfil, hecha en el cuarto. *[hipótesis]*
- **E137** · 22:00 · Sube a la azotea cerrada con una llave que no debería tener; el cielo de Madrid es la única habitación grande. *[Home Alone · azotea comunitaria]*
- **E150** · 23:55 · Última noche en el piso: duerme en el colchón en el suelo entre cajas; el móvil al 100 % y el despertador a las 6. *[Sol · cambiar de barrio]*

### Noche (madrugada)

- **E037** · 00:00 · Tiende la ropa en el cuarto, en una cuerda entre la ventana y el armario; mañana olerá a humedad. *[Home Alone]*
- **E038** · 00:30 · Scroll en la cama a oscuras; la pantalla ilumina el techo; 1 h 20 sin querer. *[hipótesis]*
- **E039** · 01:00 · Entrega un trabajo a la 1:00 desde la cama; no hay impresora, lo manda en PDF. *[autor]*
- **E040** · 01:20 · Una corta cartón para una maqueta; otra necesita dormir para entrar a trabajar a las 6. *[escena anterior · S04]*
- **E041** · 02:00 · Llega del bar y calienta algo; la luz de la cocina entra por debajo de la puerta del cuarto de otra. *[hipótesis]*
- **E042** · 02:10 · Una amiga sin sitio donde dormir: comparten la cama de 1,25; la otra tiene entrega a las 9. *[escena anterior · S02]*
- **E043** · 02:30 · Insomnio: mira el techo, luego el móvil, luego el techo. *[hipótesis]*
- **E044** · 03:00 · Sexo con gente al otro lado de un tabique de 7 cm. *[escena anterior · S13]*
- **E045** · 03:30 · Llora sin que la oigan: cascos puestos sin música, cara a la pared. *[hipótesis]*
- **E046** · 04:00 · Llega borracha, no encuentra la llave y llama al móvil de la compañera que duerme. *[hipótesis]*
- **E047** · 04:30 · Desmonta la tienda en Sol para ir a trabajar a las 6 y la deja plegada bajo una lona. *[Sol]*
- **E048** · 05:00 · Desalojo anunciado a las 5:00; vuelven miles; nadie duerme. *[Sol · 17 may 2011]*
- **E089** · 00:50 · Carga el móvil con un cable corto: duerme con el cuerpo torcido hacia el enchufe. *[hipótesis]*
- **E099** · 01:30 · Punto violeta en la acampada: una tienda con luz donde se escucha a quien lo necesita. *[Sol]*
- **E107** · 05:30 · Reparte pedidos de madrugada; carga dos baterías en el cuarto; huele a goma. *[hipótesis]*
- **E109** · 02:45 · Edita vídeos hasta las 3 para subirlos a las 9; el ordenador suena como un avión. *[Sol · creadora de contenido]*
- **E122** · 02:00 · Turno de noche en la acampada: controlar la entrada, repartir mantas, chalecos de colores. *[Sol]*
- **E135** · 00:15 · Lee en el móvil tumbada en el suelo porque la cama da calor. *[hipótesis]*
- **E136** · 01:00 · Fuma sentada en el alféizar con un pie fuera; la calle es el balcón. *[Rastro]*
- **E143** · 00:30 · Karaoke en el salón con el móvil conectado a la tele; el vecino de abajo da golpes en el techo. *[hipótesis]*
- **E144** · 02:20 · Se queda a dormir en el sofá de una amiga en Vallecas para no hacer 1 h 30 de vuelta. *[Sol · periferia]*
- **E145** · 03:10 · Mira el techo: la mancha de humedad es el único cuadro. *[Home Alone]*

### Fin de semana

- **E051** · 10:00 · Duerme 12 h seguidas con el móvil en modo avión; nadie puede saber si está. *[hipótesis]*
- **E052** · 11:30 · Resaca: agua, pantalla, cortina; sale del cuarto solo para ir al baño. *[hipótesis]*
- **E053** · 12:00 · Se cortan el pelo una a otra en la cocina, como la peluquería gratis de la acampada. *[Sol]*
- **E054** · 13:00 · Llama al casero por una gotera; le dice que pasará el martes; habrá que esconder al gato. *[hipótesis]*
- **E055** · 14:00 · Comen juntas una vez por semana: la mesa se despeja de portátiles. *[compendio · situación C]*
- **E056** · 16:00 · Cocina para cinco días y etiqueta los táperes con su nombre. *[hipótesis]*
- **E057** · 17:00 · Vende ropa en Vinted: fotos sobre la cama hecha, paquetes en el suelo, cola en Correos. *[hipótesis]*
- **E058** · 18:00 · Previa en el cuarto: seis personas en una cama de 1,25, un altavoz pequeño; el resto del piso lo oye. *[hipótesis]*
- **E059** · 19:00 · Se maquilla delante del móvil apoyado en la ventana porque el baño está ocupado. *[hipótesis]*
- **E060** · 20:00 · Botellón en la plaza: el bar es caro y el salón es de todas. *[Rastro]*
- **E061** · 23:00 · Cumpleaños sorpresa en el salón; la tarta se esconde en el cuarto de la que menos recibe. *[hipótesis]*
- **E062** · 08:00 · Baja al Rastro antes de que se llene: busca una lámpara y una silla por menos de 10 €. *[Rastro]*
- **E063** · 10:00 · Vende en el suelo lo que no cabe en la mudanza: libros, un espejo, una tabla. *[Rastro]*
- **E064** · 11:00 · Se prueba ropa del Rastro delante del espejo del cuarto; lo que no vale va a una bolsa para vender. *[Rastro]*
- **E065** · 12:00 · Pintan una pancarta en el suelo del salón y la cuelgan del balcón con bridas. *[Sol]*
- **E066** · 13:00 · Caña en el bar de abajo con los compañeros; el bar hace de salón. *[Rastro]*
- **E067** · 15:00 · Siesta de domingo con el ruido del mercadillo recogiéndose. *[Rastro]*
- **E068** · 17:00 · Vuelve a casa de sus padres a cenar y a poner lavadoras; se trae táperes para la semana. *[Sol · Andrea / Irene]*
- **E069** · 19:00 · Vuelve de la manifestación con la garganta rota y se tumba con los zapatos puestos. *[Sol · 26S]*
- **E070** · 21:00 · Domingo noche: ansiedad por el lunes; mira el techo con la lámpara nueva encendida. *[hipótesis]*
- **E081** · 12:00 · Mudanza en un coche de alquiler por horas: tres cajas y la planta; el colchón se queda. *[Sol · María Barrier: cambiar de barrio cada dos años]*
- **E082** · 18:30 · Guarda lo que no cabe en casa de sus padres: la bici, los libros, la ropa de invierno. *[Home Alone]*
- **E083** · 13:30 · Deja a quien viene la cafetera, el perchero y la lista de teléfonos: queda memoria para quien llega. *[Sol · cuaderno: temporalidad → continuidad]*
- **E084** · 09:00 · Subarrienda el cuarto en agosto a una desconocida y guarda su ropa en una bolsa bajo la cama. *[hipótesis]*
- **E104** · 19:30 · Se tatúa en casa de una amiga que está aprendiendo: sofá, flexo, guantes. *[hipótesis]*
- **E128** · 19:00 · Taller de autodefensa feminista en el salón con los muebles contra la pared. *[Sol · comisión feminismos]*
- **E132** · 20:30 · Primera cita en casa porque el bar es caro: ordena el cuarto, esconde la ropa, enciende las luces LED. *[hipótesis]*
- **E134** · 21:00 · Ven un partido tres personas en una pantalla de 13 pulgadas sobre la cama. *[hipótesis]*
- **E139** · 11:20 · Pone música en un altavoz pequeño mientras limpia; la baja cuando oye la puerta de otra. *[hipótesis]*
- **E142** · 12:30 · Compra una silla de oficina de segunda mano porque la espalda ya no aguanta la cama. *[Home Alone]*
- **E147** · 10:30 · Recoge el cuarto en 10 min grabando un vídeo acelerado para redes. *[hipótesis]*

## Lo que tienen en común (conteo)

Salida de `fuentes/contar_escenas.py` sobre `escenas.csv`.

**Dónde pasa**

| valor | escenas | % |
|---|---|---|
| cama | 71 | 47 % |
| fuera | 24 | 16 % |
| umbral | 16 | 11 % |
| comun | 11 | 7 % |
| suelo | 9 | 6 % |
| cocina | 7 | 5 % |
| mesa | 7 | 5 % |
| bano | 5 | 3 % |

**Postura del cuerpo**

| valor | escenas | % |
|---|---|---|
| tumbada | 45 | 30 % |
| sentada | 43 | 29 % |
| de_pie | 37 | 25 % |
| moviendose | 25 | 17 % |

**Con quién**

| valor | escenas | % |
|---|---|---|
| sola_conectada | 39 | 26 % |
| sola | 39 | 26 % |
| otra | 32 | 21 % |
| grupo | 26 | 17 % |
| desconocidos | 14 | 9 % |

**Hay pantalla**

| valor | escenas | % |
|---|---|---|
| si | 84 | 56 % |
| no | 66 | 44 % |

**Qué necesita respecto a ser vista u oída**

| valor | escenas | % |
|---|---|---|
| ocultarse | 52 | 35 % |
| indiferente | 47 | 31 % |
| mostrarse | 29 | 19 % |
| controlar | 22 | 15 % |

**Cuánto dura**

| valor | escenas | % |
|---|---|---|
| min | 60 | 40 % |
| hora | 43 | 29 % |
| horas | 38 | 25 % |
| noche | 9 | 6 % |

**Fuente**

| valor | escenas | % |
|---|---|---|
| GZ | 53 | 35 % |
| SOL | 39 | 26 % |
| HA | 27 | 18 % |
| ESC | 12 | 8 % |
| COMP | 9 | 6 % |
| RAS | 8 | 5 % |
| AUT | 2 | 1 % |

**Hora**

Entre las 22:00 y las 7:00 pasan 44 escenas (29 %).

| franja | escenas |
|---|---|
| 07–12 | 34 |
| 12–17 | 27 |
| 17–22 | 45 |
| 22–07 | 44 |

**Cruces**

| condición | escenas | % |
|---|---|---|
| en la cama | 71 | 47 % |
| en la cama o en el suelo | 80 | 53 % |
| tumbada | 45 | 30 % |
| tumbada o sentada (sin mesa) | 81 | 54 % |
| con pantalla | 84 | 56 % |
| en la cama y con pantalla | 46 | 31 % |
| en la cama y NO durmiendo (hay pantalla, otra persona o trabajo) | 55 | 37 % |
| sola o sola pero conectada | 78 | 52 % |
| sola pero conectada (cuerpo solo, compañía por pantalla) | 39 | 26 % |
| quiere ocultarse o controlar lo que se ve y se oye | 74 | 49 % |
| quiere mostrarse | 29 | 19 % |
| en la mesa | 7 | 5 % |
| en la cocina | 7 | 5 % |
| en un espacio común de la casa (comun, cocina, mesa) | 25 | 17 % |
| fuera de la casa | 24 | 16 % |
| con sonido que cruza un tabique (cascos, audios, micro, altavoz, voz, máquina) | 21 | 14 % |
| el móvil o el portátil aparece nombrado | 51 | 34 % |
| dormir, siesta o insomnio | 21 | 14 % |
| la casa es provisional (maleta, mudanza, casero, subarriendo, padres, cajas, alquiler) | 17 | 11 % |

**Dónde pasa, según la fuente**

| fuente | n | cama | suelo | mesa | cocina | bano | umbral | comun | fuera |
|---|---|---|---|---|---|---|---|---|---|
| GZ | 53 | 34 | 2 | 1 | 2 | 2 | 5 | 7 | 0 |
| SOL | 39 | 12 | 2 | 3 | 1 | 0 | 5 | 3 | 13 |
| HA | 27 | 12 | 3 | 1 | 2 | 2 | 0 | 0 | 7 |
| ESC | 12 | 5 | 1 | 0 | 2 | 0 | 3 | 1 | 0 |
| COMP | 9 | 4 | 0 | 2 | 0 | 1 | 2 | 0 | 0 |
| RAS | 8 | 2 | 1 | 0 | 0 | 0 | 1 | 0 | 4 |
| AUT | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### ¿Se sostiene sin mis hipótesis?

Quitando las 53 escenas marcadas como hipótesis quedan 97, todas de la investigación del proyecto:

| condición | con las 150 | solo investigación (97) |
|---|---|---|
| en la cama | 47 % | **38 %** (37 de 97) |
| sola o sola conectada | 52 % | 43 % |
| con pantalla | 56 % | 46 % |
| quiere ocultarse o controlar | 49 % | 42 % |

En Home Alone, el panel de Adam, 12 de las 27 escenas pasan en la cama. En Sol, 12 de 39 pasan en la cama y 13 fuera: la acampada reparte la vida entre la tienda y la plaza, y casi nada en medio. El resultado baja sin mis hipótesis, pero no cambia de signo: **la cama sigue siendo, de largo, el lugar donde más pasa**; la mesa y la cocina juntas no llegan al 10 % en ninguna de las dos cuentas.

## Lo que tienen en común (lectura)

Lo que sigue es lectura mía de las cifras, no dato.

**1. El lugar es la cama.** 71 de 150 escenas pasan en la cama; 80 en la cama o en el suelo. La mesa, 7; la cocina, 7. En la cama se duerme, pero sobre todo se trabaja, se come, se estudia, se hace la entrevista, se llora, se recibe a la pareja, a la amiga sin casa o a seis personas en una previa, se vende ropa, se hace la asamblea del barrio, se cuida a una niña. De las 71 escenas en la cama, 55 no son dormir. Home Alone ya lo decía: «abre el portátil en su cama si los compañeros ocupan el espacio».

**2. El cuerpo está tumbado o sentado sin mesa.** 81 de 150. La silla con mesa aparece en 7. El cuerpo joven en casa es horizontal o semihorizontal; la postura de oficina es la excepción, y cuando existe (oposiciones, teleoperador) es un castigo con tapones de cera.

**3. Sola, pero conectada.** 78 escenas son de una persona sola; en 39 de ellas el cuerpo está solo y la compañía llega por la pantalla: la serie «juntas», el trabajo en grupo a cuatro camas, la asamblea en 30 cuadrados, la terapia desde el baño. El grupo físico dentro de la casa (salón, cocina, mesa) suma 25 escenas, el 17 %. **Lo común de la juventud no está en el salón:** está en el chat, en la plaza, en el bar, en Sol. El salón compartido es, en las escenas, el sitio que se evita (E034, E013, E073, E074).

**4. Casi la mitad necesita no ser vista ni oída, y la pared no lo resuelve.** 74 escenas piden ocultarse o controlar la exposición; 29 piden mostrarse, y casi siempre a una cámara (el fondo de cámara, el vídeo repetido nueve veces, el directo) o fuera de casa. Lo que separa en las escenas no es un tabique: son los cascos, el edredón, el pestillo del baño, la puerta cerrada como señal, la cámara apagada, la cortina. El sonido cruza en 21 escenas. La **membrana** que la juventud usa hoy es ligera, graduable y personal; el tabique de 7 cm no sirve para nada de eso.

**5. Pasa de noche y en fragmentos.** 44 escenas entre las 22:00 y las 7:00; 89 a partir de las 17:00. Sesenta duran minutos. La casa joven vive a horas distintas que la casa de familia y a horas distintas entre sus habitantes: la que cierra el bar, la que entra a las 6, la que edita hasta las 3. Esto ya lo decían las 16 escenas anteriores, y la encuesta por otro lado (ruido como primera queja); aquí vuelve a salir sin buscarlo.

**6. La casa es de paso y la cama no.** Maleta sin deshacer, nada en las paredes, colchón en el suelo, casero, subarriendo, padres, cambiar de barrio cada dos años: 17 escenas. Lo que la persona joven posee y lleva consigo es el móvil, la mochila, los cascos y, como mucho, la planta. La cama suele ser del piso. En Sol es al revés: la tienda es tuya y se monta en diez minutos.

### Por qué hemos pensado en estas cosas

Porque todas las escenas son la misma escena: **un cuerpo tumbado en una superficie de 1,25 × 2 m, con una pantalla, a una hora distinta de las demás, regulando con membranas ligeras cuánto se le ve y se le oye, en una casa que no es suya.** Lo que cambia es qué hace ahí (dormir, trabajar, comer, llorar, follar, vender, reunirse) y con quién está al otro lado de la pantalla o de la tela.

La vivienda que se ha dibujado hasta ahora en el proyecto, incluida la de Codex y la mía, parte de la casa de familia: habitación con cama y mesa, salón, cocina, comedor, baños. Las escenas dicen que la juventud ya no vive en esa casa, aunque viva en ella: vive en la cama con la pantalla, y usa el resto como se usa un pasillo. La habitación de 18 m² con tablero abatible y la cocina-comedor de 50 m² para cuatro resuelven un programa que las escenas no contienen.

## Qué significa para la unidad (hipótesis de proyecto)

La conclusión radical no es formal: es que **la unidad es la cama**, y todo lo demás sale de ella y va al edificio. Eso es exactamente la acampada: una tienda, todo lo demás común (`base.txt`). El proyecto lo tenía escrito desde la primera semana y nunca lo hizo: V01–V03 dan a cada persona 18 m² de habitación **y además** 50 m² de salón-cocina para cuatro, es decir, un piso.

Referencias que pone Adam, tal como las entiendo (comprobar con el profesor):

- **Superstudio, *Supersuperficie* (1972, primera de las *Cinco actas fundamentales: Vida*) y el *Monumento Continuo* (1969).** La unidad es infinita porque es una superficie continua, cuadriculada, que da energía e información en cualquier punto: no hay muebles ni habitaciones; el cuerpo se tumba donde quiere y hace lo que quiere. Lo radical es que **el suelo lo es todo**.
- **María Palacios (misma parcela):** la unidad es una cama redonda, y los muebles y telas que inventó hacen que en esa cama se pueda dormir, trabajar con el ordenador, comer y ver una serie. Lo radical es que **el objeto lo es todo**.

Las escenas apoyan las dos, pero apuntan a algo entre medias que no es ninguna de ellas. Cinco hipótesis, de menos a más radical:

| | Hipótesis | Qué contiene la unidad | De qué escenas sale | Riesgo |
|---|---|---|---|---|
| H1 | **La cama con canto.** Una plataforma-cama de unos 2,0 × 2,4 m con un borde duro a la altura del colchón (mesa, repisa, enchufes) y un dosel textil que se cierra. | Dormir, trabajar, comer, recibir a una persona, llamar, esconderse, mostrarse a la cámara. | 1, 2, 4 | Se parece a Palacios. Hay que decir en qué se distingue. |
| H2 | **El casco.** La unidad es lo único insonorizado del edificio: una cápsula acústica y visual de 15 m² alrededor de la cama; fuera de ella el edificio es abierto, ruidoso y común. | Lo de H1 más silencio real (DB-HR comprobado) y oscuridad a cualquier hora. | 4, 5 | Cápsula = cajón. Hay que resolver luz y cielo. |
| H3 | **La superficie.** 15 m² de suelo blando continuo, sin muebles: el colchón es el suelo entero; un canto duro perimetral y enchufes; una membrana graduable alrededor; abierta al cielo. Todo lo demás (cocina, mesa, baño, lavadero) está fuera, en la estructura, como en Sol. | Cualquier escena de cuerpo tumbado o sentado: en los 15 m² caben una persona, una pareja, seis en una previa, una amiga sin casa. | 1, 2, 3, 4, 6 | Es Superstudio a 15 m². Hay que demostrar que no es un gimnasio vacío: lo que la hace habitable son el canto, la membrana y el cielo. |
| H4 | **El turno.** La unidad no es un espacio: es un tiempo. Camas asignadas por turnos (la que entra a las 6 y la que cierra a las 4 usan la misma superficie), como el saco compartido de Sol. 40 personas, menos de 40 camas. | H3 más un armario-maleta propio y una norma de uso. | 5, 6 | Radical de verdad, y políticamente legible. Choca con el mínimo normativo de 15 m² por unidad privativa y con la intimidad (E044, E013). Para discutir, no para dar por hecho. |
| H5 | **La mochila y el dock.** La unidad es lo que llevas (mochila, cascos, móvil, maleta) y el edificio da docks: enchufe, taquilla, superficie, membrana. | Nada fijo. | 6 | Es un albergue. Pierde lo que las escenas más piden: esconderse. |

**Lo que recomiendo probar primero: H3 con el silencio de H2.** Una superficie blanda de 15 m² (el mínimo normativo, usado entero como cama), con un canto duro que es mesa y repisa, una membrana acústica y visual graduable que es la vela de la megaestructura a escala del cuerpo, y un hueco propio al cielo. Es radical de programa (no hay habitación, no hay muebles, no hay piso), responde a las cinco cosas comunes, cabe en la norma, se monta y se desmonta como una tienda, y convierte lo que ya dibujamos como «velas» en la pieza que de verdad hace falta. El edificio, entonces, es Sol: superficies arriba, con el sol; abajo y entre medias, las comisiones (cocina, lavadero, baños, taller, asamblea, plaza).

Lo que no se decide aquí: cuántas superficies forman un grupo, ni si hay cocinas por grupo. Las escenas dicen que lo común está fuera de la casa; el tamaño del grupo sale de las comisiones, no de la cocina.

## Lo que haría a continuación, si Adam dice que sí

1. Dibujar la **superficie H3 a 1:20**, en planta y sección, con el cuerpo dentro en diez de las escenas (E006 entrevista, E029 cena con serie, E035 juego con micro, E042 dos en la cama, E058 previa de seis, E096 tres días sin salir, E117 asamblea desde la cama, E134 partido entre tres, E140 dibujar boca abajo, E149 puerta abierta). Comprobar que cada escena cabe, y qué pide del canto, de la membrana y de la luz.
2. Dibujar a la vez H1 y H2 a la misma escala, para que la comparación sea de programa y no de forma.
3. Solo después, llevarlas a la megaestructura: la superficie como bandeja, la membrana como vela, el turno como regla de uso.

Lo que no haría: generar veinte variantes ni volver a la casa de cuatro.
