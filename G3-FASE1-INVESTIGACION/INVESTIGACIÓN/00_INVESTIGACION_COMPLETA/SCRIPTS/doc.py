import sys, json, math, datetime
sys.path.insert(0, "."); sys.path.insert(0, "datos")
from doc_base import *
from codificacion_fachadas import C
from reportlab.lib.utils import ImageReader

M = json.load(open("datos/metricas_nuevas.json"))
SOL = json.load(open("datos/sombras_resumen.json"))["parcela"]
SA = json.load(open("datos/sol_por_altura.json"))
SEC = json.load(open("datos/seccion.json"))
EST = json.load(open("datos/estancia.json"))
PAT = json.load(open("datos/patrones.json"))
R = json.load(open("datos/fachadas_index.json")); RC = {r["codigo"]: r for r in R}
META = json.load(open("/mnt/user-data/uploads/G3 Proyectos/INVESTIGACIÓN/00_INVESTIGACION_COMPLETA/RECORRIDO_STREETVIEW_2026-09-23/G3SV_metadatos.json"))
FR = json.load(open("datos/frentes_ribera.json"))
INV = json.load(open("/mnt/user-data/uploads/G3 Proyectos/INVESTIGACIÓN/CATALOGO_CORREGIDO_RIBERA/inventario_fotos.json"))
HOY = "23·09·2026"
def cod(c): return c.replace("W", "O")
def f1(x): return f"{x:.1f}".replace(".", ",")
def f2(x): return f"{x:.2f}".replace(".", ",")
def miles(x): return f"{x:,}".replace(",", ".")
REG = []  # registro de métricas (R4)
def met(i, v, u, n, metodo, fuente):
    REG.append((i, v, u, n, metodo, fuente)); return v

d = Doc("/home/claude/g3/RIBERA_31_COMPENDIO_INVESTIGACION.pdf")
c = d.c

# ======================= PORTADA (R1)
d.page(furniture=False)
c.setFillColor(TINTA); c.rect(0, 0, PW, PH, stroke=0, fill=1)
c.setFillColor(white); c.setFont("G", 5.8); c.drawString(ML, PH - 12 * mm, spaced("IRAXXXDIOS / G3 · UEM"))
c.drawRightString(PW - MR, PH - 12 * mm, spaced("septiembre 2026"))
ir = ImageReader("fig/strips/continuo_E_320_480.jpg"); iw, ih = ir.getSize()
hh = CW * ih / iw
c.drawImage(ir, ML, PH * 0.47, CW, hh)
c.setFillColor(TINTA); c.setFillAlpha(0.35); c.rect(ML, PH * 0.47, CW, hh, stroke=0, fill=1); c.setFillAlpha(1)
x31 = ML + (358.7 - 320) / 160 * CW; c.setStrokeColor(MAG); c.setLineWidth(0.8); c.line(x31, PH * 0.47 + hh + 1 * mm, x31, PH * 0.47 + hh + 4 * mm); c.setFillColor(MAG); c.setFont("GB", 7); c.drawCentredString(x31, PH * 0.47 + hh + 5.5 * mm, "31")
c.setFillColor(MAG); c.setFont("GB", 6.4); c.drawString(ML, PH * 0.40, spaced("compendio de investigación"))
c.setFillColor(white); c.setFont("GB", 30); c.drawString(ML, PH * 0.40 - 14 * mm, "Ribera de")
c.drawString(ML, PH * 0.40 - 26 * mm, "Curtidores 31")
p = Paragraph("Una sola investigación para una vivienda temporal de jóvenes en El Rastro: el solar medido, la calle censada frente a frente, el sol calculado con las alturas catastrales y los patrones que se repiten ocho veces o más.", sty(9.6, 13.5, color=HexColor("#d9d4cb")))
_, h = p.wrap(120 * mm, 60 * mm); p.drawOn(c, ML, PH * 0.40 - 34 * mm - h)
c.setStrokeColor(HexColor("#555049")); c.setLineWidth(0.4); c.line(ML, 34 * mm, PW - MR, 34 * mm)
cols = [("documento", "RIBERA_31_COMPENDIO"), ("versión", "v1 · " + HOY), ("fuentes", "Catastro · Street View · AEMET · Padrón"), ("formato", "A4 vertical")]
for i, (k, v) in enumerate(cols):
    x = ML + i * CW / 4
    c.setFillColor(GRIS); c.setFont("G", 5); c.drawString(x, 29 * mm, spaced(k))
    c.setFillColor(white); c.setFont("GB", 6.6); c.drawString(x, 24.5 * mm, v)
c.setFillColor(GRIS); c.setFont("G", 5); c.drawString(ML, PH * 0.47 - 4 * mm, spaced("alzado rectificado de la acera este entre 320 y 480 m desde cascorro · la marca señala la parcela 31"))

# ======================= 0.1 CÓMO LEER
d.page("0 · sistema")
d.kicker("0.1 · cómo leer este documento")
d.title("Tres profundidades, un solo hilo")
d.lead("Este compendio sustituye a los cuatro catálogos anteriores, a la guía de diagramas y a las láminas de análisis del lugar. Todo lo que seguía siendo válido se ha conservado; lo que no se sostenía se ha corregido o retirado (tabla 0.3).")
items = [
    ("En treinta segundos.", "La página 0.4 reúne las cifras y los ocho hallazgos. Cada lámina abre con la pregunta en el título y la respuesta en la primera línea."),
    ("En treinta minutos.", "Las partes I a V siguen la misma estructura: pregunta · método · datos · resultado · lectura · consecuencia · límite."),
    ("En profundidad.", "Los anexos publican el registro de métricas, las estaciones del recorrido, los 44 frentes con referencia catastral y las fuentes. Un dossier que no publica sus datos no se puede auditar."),
]
for b, t in items: d.para(f"<font color='#e5007e'>—</font>&nbsp;&nbsp;<b>{b}</b> {t}", gap=2.5)
d.y -= 2 * mm
d.kicker("0.2 · niveles de conocimiento")
d.table([["nivel", "significa", "ejemplos en este documento"],
         ["A · medido", "Dato primario o cálculo reproducible desde la geometría o la fuente citada.", "Superficie catastral 651 m² · plantas y año catastrales · horario municipal del Rastro · Padrón 2026"],
         ["B · inferido", "Resultado de un modelo o de una lectura visual declarada.", "Horas de sol con alturas supuestas · rasgos leídos en alzados rectificados · cota GPS de las panorámicas"],
         ["C · hipótesis", "Escenario plausible pendiente de validación. Nunca se presenta como A.", "Reparto del programa · perfiles de habitante · criterios de proyecto"]],
        [24 * mm, 64 * mm, 90 * mm])
d.panel("Este documento publica también lo que no sabemos: no hay imágenes de domingo con mercado, no hay conteos peatonales, las fotos propias no tienen coordenadas, la altura de cada planta es una hipótesis y la posición GPS de la cámara tiene un error de uno a dos metros. Estas limitaciones aparecen en el mismo cuerpo tipográfico que los resultados.", title="advertencia de lectura honesta")
d.kicker("0.2b · lenguaje gráfico")
d.para("Una sola familia tipográfica serif en cuatro registros; versalitas espaciadas para navegar; el magenta solo señala (títulos de sección, folios, cabeceras de tabla). En los mapas el contexto es gris piedra y el dato va en color: <b>tinta</b> para altura, <b>cobre–agua</b> para año, <b>naranja–rojo</b> para sol, <b>verde</b> para vegetación, <b>agua</b> para agua, <b>rosa</b> para la parcela del proyecto. Todo mapa lleva norte y escala gráfica; todo dato, su nivel A/B/C; toda figura, su fuente al pie. Lenguaje heredado de <i>Refugio Climático</i> (IRAXXXDIOS) y de las láminas de Oviedo; los paneles de patrones siguen la lógica de la lámina científica: casos con letra, misma escala, una sola variable.")

# ======================= 0.3 CORRECCIONES
d.page()
d.kicker("0.3 · qué cambia respecto a las versiones anteriores")
d.title("Lo que se ha corregido y por qué")
d.table([["problema anterior", "corrección en este documento", "nivel"],
    ["Parcela «651 m² según Idealista, a verificar».", "Consultada en la Sede del Catastro (INSPIRE y DNPRC): 651 m², referencia 0134911VK4703C, uso «suelo sin edificar», 0 m² construidos.", "A"],
    ["96 de 115 edificios sin altura (OSM).", "Alturas catastrales de 1.989 partes de edificio: los 44 frentes de Ribera tienen plantas y año.", "A"],
    ["Sol calculado sin obstáculos; «no equivale a sombra».", "Sombras reales con las alturas catastrales: horas de sol en el suelo y en altura sobre la parcela.", "B"],
    ["Recorrido de capturas sin criterio fijo; 25 patrones con dos o tres casos.", "23 estaciones regulares sobre el eje (cada 40 m; cada 20 m cerca del 31), una sola campaña 2021–2022, 42 frentes censados uno a uno.", "A/B"],
    ["Flechas que no coincidían con el objeto; diagramas genéricos D1/D2.", "Alzados rectificados con escala métrica; cada panel es un recorte de fachada identificada con su referencia catastral.", "B"],
    ["Ocho fotos del mismo frente contadas como ocho casos.", "Regla de patrón: al menos ocho frentes distintos; la prevalencia se da como n / frentes legibles.", "B"],
    ["Categorías curiosas (reloj, entramado, fábrica singular).", "Retiradas. Las singularidades relevantes (galerías comerciales, solar 31) se tratan aparte.", "—"],
    ["Cuatro catálogos, una guía y cinco láminas sueltas.", "Un solo compendio. Las versiones anteriores quedan archivadas en _ARCHIVO.", "—"],
    ["Radio de 600 m como regla de selección.", "Foco en Ribera; el radio de 100–200 m solo como contexto métrico.", "—"]],
    [58 * mm, 106 * mm, 14 * mm])
d.panel("Se mantienen sin cambios los datos del Padrón 2026, el ciclo horario del Rastro, las referencias de corralas y Vara de Rey 12, y el clima AEMET 1981–2010. Los textos del documento Word original se han condensado en la parte III.", title="lo que se conserva")

# ======================= 0.4 RESUMEN
d.page()
d.kicker("0.4 · resumen en treinta segundos")
d.title("Ocho cosas que ya sabemos del 31")
y0 = d.y - 6 * mm
bn = [("651", "m²", "parcela catastral 0134911VK4703C; frente 14,9 m, fondo 49,5 m (A)"),
      ("0", "m²", "superficie construida catastral: el solar figura como suelo sin edificar (A)"),
      ("8 · 10", "pl.", "vecino sur (1928) y torre del vecino norte (1952) según Catastro (A)"),
      (f2(SOL['2026-12-21']['media_parcela_h']), "h", "sol directo medio sobre el suelo del solar el 21 de diciembre (B)"),
      ("25,8", "m", "de la fachada de enfrente al lindero del 31 (A)"),
      ("6,8", "%", "pendiente de Ribera junto al 31: ≈1 m de desnivel a lo largo del frente (B)"),
      ("42", "frentes", "censados en alzado rectificado, 23 estaciones, campaña 2021–2022 (B)"),
      ("30/39", "", "frentes legibles con balcón propio por hueco (B)")]
for i, (v, u, l) in enumerate(bn):
    x = ML + (i % 4) * CW / 4; y = y0 - (i // 4) * 27 * mm
    d.bignum(x, y, v, u, l, w=CW / 4 - 5 * mm, col=TINTA if i != 3 else AGUA)
d.y = y0 - 2 * 27 * mm - 2 * mm
d.rule()
H = [("H-01", "El solar no está vacío.", "Catastro lo registra sin construir, pero entre 2008 y 2022 una nave comercial de una planta ocupa el fondo tras un atrio de acceso; cambia de inquilino al menos dos veces. El programa temporal ya existe."),
     ("H-02", "El sol de invierno solo llega arriba.", f"El 21-dic el suelo recibe {f2(SOL['2026-12-21']['media_parcela_h'])} h de media; más de la mitad de la superficie supera 2 h solo entre 19,5 y 22,6 m de cota (plantas 6–7 con la hipótesis de alturas)."),
     ("H-03", "El 31 negocia entre 3 y 10 plantas.", "Base de tres plantas y torre de diez al norte; ocho al sur. En la calle, 9 de 28 medianeras contiguas saltan dos plantas o más: la discontinuidad es la norma."),
     ("H-04", "La unidad de fachada es el hueco con balcón propio.", "30 de 39 frentes legibles. El balcón corrido es excepcional (1 caso puro, 2 mixtos)."),
     ("H-05", "La planta baja es comercial y se cierra.", "37 de 39 frentes con comercio; 19 de 33 con cierre enrollable; grafiti en 23 de 37. La fachada de la hora de cierre existe y es gráfica."),
     ("H-06", "La tienda sale a la acera incluso un laborable.", "8 de 37 frentes exponen objetos fuera (imágenes de lunes a sábado). El domingo no está documentado."),
     ("H-07", "La calle desciende.", "6,2 % de media entre Cascorro y Ronda; 6,8 % junto al 31. El acceso y la planta baja deben resolver ≈1 m de desnivel."),
     ("H-08", "Densidad alta, espacio de estancia escaso.", f"Al menos {miles(M['viv_200'])} viviendas catastrales a menos de 200 m; {EST['bancos_100']} bancos a menos de 100 m; la fuente de agua potable más cercana a {f1(EST['agua_min_m'])} m.")]
for i, (k, t, x) in enumerate(H):
    col = i % 2; row = i // 2
    xx = ML + col * (CW / 2 + 2 * mm); yy = d.y - row * 30 * mm
    d.label(xx, yy, k, 6, MAG, "GB")
    d.para(f"<b>{t}</b> {x}", x=xx + 10 * mm, y=yy + 2.4 * mm, w=CW / 2 - 14 * mm, st=sty(7.2, 9.8))
d.y -= 4 * 30 * mm
d.caption("Lectura.", "Los hallazgos se desarrollan con su prueba en la parte VI. Cada uno cita el análisis que lo sostiene y su nivel de certeza.")

# ======================= ÍNDICE (placeholder; se rellena al final)
d.page(); IDX_PAGE = d.n
d.kicker("0.5 · contenido"); d.title("Índice", toc=False)
IDX_Y = d.y
import os
if os.path.exists("datos/toc.json"):
    T_ = json.load(open("datos/toc.json"))["toc"]; lastp = None; yy = d.y - 2 * mm
    for part, t, pg in T_:
        if part != lastp:
            yy -= 2.5 * mm; d.label(ML, yy, spaced(part), 5.8, MAG, "GB"); yy -= 4.6 * mm; lastp = part
        tt = t.replace("<b>", "").replace("</b>", "")
        d.label(ML + 4 * mm, yy, tt[:95], 7, TINTA); d.label(PW - MR, yy, str(pg), 7, MAG, "G", "r")
        c.setStrokeColor(FILETE); c.setLineWidth(0.25); c.setDash(0.5, 1.5); c.line(ML + 4 * mm + pdfmetrics.stringWidth(tt[:95], "G", 7) + 2 * mm, yy + 0.6 * mm, PW - MR - 7 * mm, yy + 0.6 * mm); c.setDash()
        yy -= 4.3 * mm

# ======================= PARTE I · EL SOLAR
d.page("I · el solar")
d.kicker("I.1 · parcela catastral"); d.nivel("A", y=d.y + 7.2 * mm)
d.title("¿Qué es exactamente el número 31?")
d.lead("Una parcela de 651 m², estrecha y profunda, encajada entre dos edificios altos. El Catastro la registra como suelo sin edificar.")
d.image("fig/F01_parcela.png")
d.caption("Parcela y partes de edificio colindantes.", "Rosa: parcela 0134911VK4703C. Cifras: plantas sobre rasante de cada parte catastral. Línea discontinua: eje de Ribera de Curtidores (OSM). Cotas en magenta medidas sobre la geometría catastral.",
          "Sede Electrónica del Catastro, servicios INSPIRE CP/BU y OVC Consulta_DNPRC, consulta " + HOY + " · EPSG:25830 · precisión nominal 0,1 m")
d.table([["dato", "valor", "fuente", "nivel"],
         ["Referencia catastral", "0134911VK4703C", "Catastro OVC", "A"],
         ["Superficie de parcela", "651 m² (650,9 m² recalculados)", "INSPIRE CadastralParcel", "A"],
         ["Uso / superficie construida", "Obras de urbanización y jardinería, suelos sin edificar · 0 m²", "OVC DNPRC", "A"],
         ["Frente a Ribera · fondo", "14,9 m · 49,5 m (máx.)", "geometría catastral", "A"],
         ["Vecino norte 0134901", "1952 · hasta 10 plantas · 23 viviendas · uso comercial", "INSPIRE BU", "A"],
         ["Vecino sur 0134910", "1928 · 8 plantas · 46 viviendas · residencial", "INSPIRE BU", "A"]],
        [44 * mm, 80 * mm, 40 * mm, 14 * mm])
for k, v in [("par_sup", 651), ("par_frente", 14.9), ("par_fondo", 49.5)]: pass
met("I.1-1", "651", "m²", "A", "área catastral", "INSPIRE CP 0134911VK4703C")
met("I.1-2", "0", "m² construidos", "A", "DNPRC", "OVC Consulta_DNPRC")
met("I.1-3", "14,9 / 49,5", "m", "A", "geometría", "INSPIRE CP")

d.page()
d.kicker("I.2 · encargo y capacidad"); d.nivel("C", y=d.y + 7.2 * mm)
d.title("¿Qué pide el enunciado y qué cabe en 651 m²?")
d.lead("El enunciado G3 v3.0 pide unos 1.500 m² para 20 unidades o 40 habitantes con espacios de comunidad. Sobre 651 m² eso supone 2,30 m² construidos por m² de suelo.")
y0 = d.y - 6 * mm
for i, (v, u, l) in enumerate([("1.500", "m²", "superficie aproximada del enunciado (dato del encargo)"), ("2,30", "m²/m²", "edificabilidad bruta necesaria sobre 651 m²"), ("37,5", "m²", "superficie bruta por habitante (1.500 / 40)"), ("20 / 40", "", "unidades / habitantes (dato del encargo)")]):
    d.bignum(ML + i * CW / 4, y0, v, u, l, w=CW / 4 - 5 * mm)
d.y = y0 - 22 * mm
rows = [["ocupación de parcela", "planta tipo", "plantas necesarias (1.500 m²)", "altura aprox. (PB 4,0 + 3,1 m)", "comparación"]]
for occ in (1.0, 0.8, 0.65, 0.5):
    pt = 651 * occ; n = math.ceil(1500 / pt); hgt = 4.0 + (n - 1) * 3.1
    cmpv = "por debajo del vecino sur (8 pl.)" if n < 8 else ("igual al vecino sur" if n == 8 else "por encima del vecino sur")
    rows.append([f"{int(occ*100)} %", f"{round(pt)} m²", f"{n} ({1500/pt:.1f})".replace(".", ","), f"{f1(hgt)} m", cmpv])
d.table(rows, [30 * mm, 26 * mm, 40 * mm, 40 * mm, 42 * mm])
d.para("<b>Lectura.</b> Con ocupación total bastan 3 plantas; con un patio que libere la mitad del suelo harían falta 5. Todas las opciones quedan por debajo de los vecinos, lo que deja margen para concentrar volumen donde llega el sol (II.6) sin superar la cornisa del entorno inmediato. La tabla es aritmética sobre datos del encargo: <b>no</b> comprueba edificabilidad, alineaciones ni protección del Plan General.")
d.panel("Consultar en el visor urbanístico del Ayuntamiento la norma zonal, la altura máxima, el fondo edificable y la catalogación de la parcela. Sin ese dato, cualquier volumen es un escenario C.", title="lo que falta para pasar de C a A")
d.kicker("programa de trabajo (escenario del análisis 03)")
d.table([["pieza", "m²", "criterio"], ["Vivienda privada", "930", "unidades compactas con almacenamiento real; algunas para dos"], ["Espacios compartidos", "240", "lavandería, trabajo silencioso, taller de reparación, habitación de invitados"], ["Circulación y núcleos", "240", "incluye galería o rellanos de estancia"], ["Instalaciones y reserva", "90", "almacenaje común junto al acceso"]], [48 * mm, 18 * mm, 112 * mm])
d.caption("Escenario C.", "Reparto heredado de la Entrega 1 para contrastar, no una distribución definitiva.")

# ======================= I.3 HISTÓRICO
d.page()
d.kicker("I.3 · el solar en el tiempo"); d.nivel("B", y=d.y + 7.2 * mm)
d.title("¿Cómo ha cambiado el 31 entre 2008 y 2022?")
d.lead("Doce fotografías de la misma posición en catorce años. El solar sin edificar del Catastro es, en la calle, una nave comercial baja retranqueada detrás de un atrio pavimentado.")
import glob
fr = sorted(glob.glob("vistas/hist/*.jpg"), key=lambda f: [int(x) for x in f.split("/")[-1][:-4].split("-")])
wcol = (CW - 4 * mm) / 3
for i, f in enumerate(fr):
    x = ML + (i % 3) * (wcol + 2 * mm); y = d.y - (i // 3) * (wcol * 375 / 1150 + 7 * mm)
    h = d.image(f, x=x, y=y, w=wcol)
    d.label(x, y - h - 3 * mm, f.split("/")[-1][:-4].replace("-", " · "), 5.6, TINTA, "GB")
d.y -= 4 * (wcol * 375 / 1150 + 7 * mm) + 1 * mm
d.table([["fechas", "lo que se ve en el frente del 31", "nivel"],
         ["2008-08 · 2011-04", "Nave con comercio de chimeneas y hogar; toldos y género en el atrio.", "B"],
         ["2012-05", "Andamio y lona en el edificio norte (Galerías Piquer); la nave sigue abierta.", "B"],
         ["2013-10 · 2014-03", "Rótulo «liquidación por cierre».", "B"],
         ["2015-06 · 2016-06", "Nave con otro comercio y menos rótulos; al sur, solar vallado.", "B"],
         ["2017-09", "Nave sin actividad visible; obra en el solar sur (edificio de 2018 según Catastro).", "A/B"],
         ["2018-08 · 2022-03", "Nuevo inquilino «Fang Decoración»; persianas con grafiti.", "B"]],
        [30 * mm, 136 * mm, 12 * mm], fs=6.4)
d.caption("Método.", "Once panorámicas históricas del mismo punto (Street View, 2008–2021) y la de 2022-03 rectificadas sobre el mismo plano de fachada (lindero catastral, 46 m de ancho, 14 m de alto). Las de 2008–2017 tienen menor resolución. Las fechas son de captura, no de apertura o cierre de los comercios.", "Google Street View, panoramas listados en G3SV_metadatos.json → historico_31")

# ======================= I.4 FRENTE HOY
d.page()
d.kicker("I.4 · el frente hoy"); d.nivel("B", y=d.y + 7.2 * mm)
d.title("¿Qué tiene delante y a los lados el 31?")
d.lead("Una base comercial continua de una a tres plantas con dos cuerpos altos: la torre de diez plantas al norte y el bloque de ocho al sur. El 31 abre un vacío en esa cornisa.")
fj = json.load(open("datos/frente31.json"))
ytop = d.y; h = d.image("fig/F13_frente31.jpg")
# límites de parcela y escala
L = fj["L"]; ybot = ytop - h
for yv in fj["parcela_y"]:
    t = (fj["a"][1] - yv) / (fj["a"][1] - fj["b"][1]); x = ML + t * CW
    c.setStrokeColor(MAG); c.setLineWidth(0.7); c.setDash(2, 1.5); c.line(x, ybot, x, ytop); c.setDash()
for z in range(0, 34, 5):
    yy = ybot + (z - fj["zmin"]) / (fj["zmax"] - fj["zmin"]) * h
    c.setStrokeColor(white); c.setLineWidth(0.6); c.line(ML, yy, ML + 3 * mm, yy)
    c.setFillColor(white); c.setFont("G", 5); c.drawString(ML + 4 * mm, yy - 1.5, f"{z} m")
t0 = (fj["a"][1] - fj["parcela_y"][0]) / (fj["a"][1] - fj["b"][1]); t1 = (fj["a"][1] - fj["parcela_y"][1]) / (fj["a"][1] - fj["b"][1])
d.label(ML + (t0 + t1) / 2 * CW, ytop + 1.5 * mm, "LINDEROS DE LA PARCELA 31", 5.2, MAG, "GB", "c")
d.caption("Alzado rectificado del frente este entre y = 4473200 y 4473262 (62 m).", "Proyección de la panorámica S13 (2022-03) sobre el plano de la alineación catastral; escala vertical en metros sobre la acera. Líneas magenta: linderos catastrales del 31. El error de registro horizontal es de ±1–2 m (posición GPS de la cámara) y los cuerpos retranqueados aparecen desplazados.", "Street View S13 0KdzVbjLRLIV_EUL-Kc2aw · Catastro INSPIRE · método en Anexo A3")
d.para("<b>Lectura.</b> La nave ocupa el fondo con una cubierta a dos aguas y un frente de escaparate retranqueado; delante, un atrio de losas con bolardos prolonga la acera. Al norte, la base de Galerías Piquer mantiene la cornisa a unas tres plantas y abre un pasaje comercial al interior de la manzana; la torre retranqueada sube a diez. Al sur, el edificio de 1928 sube en fachada hasta ocho plantas con remate escalonado.")
d.para("<b>Consecuencia.</b> El proyecto puede decidir entre completar la base (tres plantas a la calle) y elevar un cuerpo retranqueado, como hace su vecino norte, o alinearse con el vecino sur. La sección de sol (II.5–II.6) favorece que el volumen alto no se apoye contra la medianera sur.")

# ======================= PARTE II
d.page("II · contexto medido")
d.kicker("II.1 · alturas"); d.nivel("A", y=d.y + 7.2 * mm)
d.title("¿Qué altura tiene el entorno?")
d.lead(f"Mediana de {int(M['plantas_med_200'])} plantas en 200 m. Los frentes de Ribera van de {M['frente_plantas_min']} a {M['frente_plantas_max']} plantas; el 31 queda entre dos de los cuerpos más altos del tramo.")
d.image("fig/F02_alturas.png", w=CW)
d.caption("Plantas sobre rasante de cada parte de edificio.", f"Dentro del círculo de 200 m, color por número de plantas; fuera, contexto. {M['edif_200']} edificios con centroide en 200 m; {M['edif_100']} en 100 m.", "Catastro INSPIRE BuildingPart (numberOfFloorsAboveGround), consulta " + HOY)
met("II.1-1", str(int(M['plantas_med_200'])), "plantas (mediana, 200 m)", "A", "mediana de plantas máx. por edificio", "INSPIRE BU")

d.page()
d.kicker("II.2 · tiempo construido"); d.nivel("A", y=d.y + 7.2 * mm)
d.title("¿De cuándo es lo que se ve?")
d.lead(f"En Ribera conviven edificios de {M['frente_anio_min']} y de {M['frente_anio_max']}. De los 44 frentes, {M['frente_antes1900']} son anteriores a 1900, {M['frente_1900_1959']} de 1900–1959, {M['frente_1960_1999']} de 1960–1999 y {M['frente_2000']} posteriores a 2000.")
h_ = d.image("fig/F03_anios.png", w=CW * 0.8, x=ML + CW * 0.1); d.y -= h_ + 2 * mm
d.image("fig/F12_anios_frentes.png")
d.caption("Año catastral de construcción.", "Arriba: edificios en 200 m. Abajo: los 44 frentes de Ribera ordenados por distancia desde Cascorro. El año catastral puede reflejar una rehabilitación integral y no la fecha original (p. ej. E09, fachada historicista registrada en 1980).", "Catastro INSPIRE Building (dateOfConstruction)")
d.para("<b>Lectura.</b> La sustitución es parcela a parcela: edificios de 2006, 2007 y 2018 se intercalan entre casas de 1850–1880 sin romper la alineación. El proyecto se inserta en esa lógica de reemplazo individual.")

d.page()
d.kicker("II.3 · la sección de Ribera"); d.nivel("A/B", y=d.y + 7.2 * mm)
d.title("¿Qué relación hay entre calle, solar y vecinos?")
d.lead(f"Frente al 31 la calle mide {f1(SEC['ancho_calle_31'])} m de fachada a lindero. El vecino sur, de {SEC['vecino_sur_plantas']} plantas, proyecta a mediodía del 21 de diciembre una sombra de unos 52 m: más larga que todo el solar.")
d.image("fig/F06_secciones.png")
d.caption("Secciones A–A′ y B–B′.", "Alturas = plantas catastrales × hipótesis (PB 4,0 m; plantas 3,1 m): nivel B. Anchuras y posiciones sobre la geometría catastral: nivel A. Rayos: elevación solar máxima de cada fecha (NOAA). La calzada se dibuja horizontal; la pendiente longitudinal (II.4) no aparece en estas secciones.", "Catastro INSPIRE BU · NOAA Solar Calculator")
d.para("<b>Consecuencia.</b> El vacío del 31 es hoy el patio de luz de sus vecinos. Cualquier volumen que se apoye contra el lindero sur quedará en sombra en invierno; el que se apoye contra el lindero norte recibe sol sobre su fachada sur. Esta asimetría es el primer dato de proyecto.")
met("II.3-1", f1(SEC['ancho_calle_31']), "m", "A", "distancia fachada opuesta–lindero", "INSPIRE BU/CP")

d.page()
d.kicker("II.4 · perfil de la calle"); d.nivel("A/B", y=d.y + 7.2 * mm)
d.title("¿Cómo cambian altura y cota a lo largo de Ribera?")
d.lead(f"La calle desciende {f1(M['alt_perfil'][0][1]-M['alt_perfil'][-1][1])} m entre Cascorro y la Ronda de Toledo (6,2 % de media). En 9 de las 28 medianeras contiguas la altura salta dos plantas o más.")
d.image("fig/F07_perfil.png")
d.caption("Alzado lógico de las dos aceras.", "Barras: frentes catastrales con su altura de fachada (plantas de las partes que tocan la alineación × hipótesis B). Línea azul: cota de la cámara de cada estación menos 2,5 m (GPS, nivel B). Marcas magenta: estaciones del recorrido.", "Catastro INSPIRE BU · metadatos Street View (altitud)")
d.table([["medida", "valor", "nivel"], ["Desnivel total del recorrido (S01–S23)", f"{f1(M['alt_perfil'][0][1]-M['alt_perfil'][-1][1])} m en 620 m", "B"], ["Pendiente junto al 31 (S12–S14)", "6,8 % → ≈1,0 m a lo largo del frente de 14,9 m", "B"], ["Medianeras contiguas con salto ≥ 2 plantas", f"{M['saltos_ge2']} de {M['saltos_total']}", "A"], ["Medianeras contiguas sin salto", f"{M['saltos_0']} de {M['saltos_total']}", "A"], ["Plantas de fachada en los frentes", f"de {M['frente_plantas_min']} a {M['frente_plantas_max']}; mediana {int(M['frente_plantas_med'])}", "A"]], [78 * mm, 86 * mm, 14 * mm])
d.para("<b>Consecuencia.</b> El acceso del 31 debe resolver cerca de un metro de desnivel a lo largo de su frente: una planta baja con dos cotas o un umbral en rampa. Frente a 10 plantas al norte y 8 al sur, cualquier altura entre 3 y 8 continúa una calle donde la discontinuidad es lo habitual.")

d.page()
d.kicker("II.5 · sol sobre el suelo"); d.nivel("B", y=d.y + 7.2 * mm)
d.title("¿Cuánto sol llega al suelo del solar?")
s = SOL
d.lead(f"Casi nada en invierno. Media sobre la parcela: {f2(s['2026-12-21']['media_parcela_h'])} h el 21-dic, {f2(s['2026-03-21']['media_parcela_h'])} h el 21-mar y {f2(s['2026-06-21']['media_parcela_h'])} h el 21-jun.")
d.image("fig/F04_sol_suelo.png")
d.caption("Horas de sol directo sobre el suelo.", "Sombras 2,5D de 796 partes catastrales con altura = PB 4,0 m + 3,1 m por planta; posición solar NOAA cada 15 min; celda de 1 m; hora oficial de Madrid. Sin arbolado, relieve ni reflejos: los árboles de Ribera reducirían aún más el sol en verano.", "Catastro INSPIRE BU · NOAA · script sombras.py")
d.table([["fecha", "media en la parcela", "máximo", "superficie con ≥ 2 h", "superficie con ≥ 4 h"]] + [[k[8:10] + "-" + {"12": "dic", "03": "mar", "06": "jun"}[k[5:7]], f"{f2(v['media_parcela_h'])} h", f"{f2(v['max'])} h", f"{f1(v['pct_parcela_>=2h'])} %", f"{f1(v['pct_parcela_>=4h'])} %"] for k, v in s.items()], [30 * mm, 40 * mm, 30 * mm, 40 * mm, 38 * mm])
d.para("<b>Lectura.</b> En marzo solo una quinta parte del suelo supera dos horas de sol. Un patio en planta baja sería un espacio de sombra durante la mayor parte del curso académico. En junio el solar se comporta al revés: casi todo recibe más de cuatro horas.")
for k, v in s.items(): met(f"II.5-{k}", f2(v['media_parcela_h']), "h sol en suelo (media parcela)", "B", "sombras 2,5D", "sombras_resumen.json")

d.page()
d.kicker("II.6 · sol en altura"); d.nivel("B", y=d.y + 7.2 * mm)
d.title("¿A qué altura llega el sol de invierno?")
dz = SA["2026-12-21"]
d.lead(f"A partir de unos 20 m. El 21 de diciembre la media sobre la parcela pasa de {f2(dz['0']['media'])} h en el suelo a {f2(dz['19.5']['media'])} h a 19,5 m, {f2(dz['22.6']['media'])} h a 22,6 m y {f2(dz['25.7']['media'])} h a 25,7 m, la cota de la cornisa del vecino sur.")
d.image("fig/F05_sol_altura.png")
d.caption("Horas de sol sobre planos horizontales a distintas cotas.", "Mismo modelo que II.5, recalculado para cada cota z sobre la parcela (celda 0,5 m). Franja clara: cotas donde en diciembre más de un tercio de la superficie supera 2 h. Columna derecha: correspondencia con plantas según la hipótesis de alturas.", "sol_por_altura.json")
rows = [["cota z", "planta (hipótesis)", "21-dic media", "21-dic ≥ 2 h", "21-mar media", "21-jun media"]]
labs = {"0": "suelo", "4": "1", "7.1": "2", "10.2": "3", "13.3": "4", "16.4": "5", "19.5": "6", "22.6": "7", "25.7": "8"}
for z in ["0", "4", "7.1", "10.2", "13.3", "16.4", "19.5", "22.6", "25.7"]:
    rows.append([f"{z.replace('.', ',')} m", labs[z], f"{f2(SA['2026-12-21'][z]['media'])} h", f"{f1(SA['2026-12-21'][z]['pct_2h'])} %", f"{f2(SA['2026-03-21'][z]['media'])} h", f"{f2(SA['2026-06-21'][z]['media'])} h"])
d.table(rows, [22 * mm, 30 * mm, 30 * mm, 30 * mm, 33 * mm, 33 * mm], fs=6.3)
d.para("<b>Consecuencia.</b> Los espacios comunes que dependan del sol (tendedero, estancia de invierno, huerto) tienen sentido en cubierta o en las plantas altas, no en planta baja. La planta baja puede alojar lo que no necesita sol: acceso, almacenaje, taller, comercio.")
d.panel("La cota z es un plano horizontal sobre todo el solar, no el suelo de una planta concreta con sus muros. Sirve para decidir a qué altura situar un espacio exterior; no sustituye el cálculo de soleamiento de cada vivienda, que dependerá del volumen proyectado.", title="límite")

d.page()
d.kicker("II.7 · clima de referencia"); d.nivel("A", y=d.y + 7.2 * mm)
d.title("¿Qué clima tiene que resolver el edificio?")
d.lead("Veranos de 32 °C de máxima media en julio y 12 mm de lluvia; inviernos de 2,7 °C de mínima media en enero. La lluvia se concentra en otoño.")
d.image("fig/F09_clima.png")
d.caption("Valores climatológicos normales, Madrid-Retiro (3195), 1981–2010.", "Estación a unos 2 km del solar; referencia histórica, no medida en Ribera ni episodio extremo actual.", "AEMET, valores climatológicos normales · https://www.aemet.es/es/serviciosclimaticos/datosclimatologicos/valoresclimatologicos?l=3195")
d.para("<b>Cruce con II.5–II.6.</b> En julio el solar recibe entre 8 y 14 h de sol según la cota: la protección solar de verano es necesaria en fachadas y cubierta. En invierno el problema es el contrario: el sol solo alcanza lo alto. El edificio necesita capas regulables, no una orientación única.")
d.y -= 2 * mm
d.kicker("II.8 · vegetación, estancia y agua"); d.nivel("B", y=d.y + 7.2 * mm)
d.title("¿Dónde sentarse a la sombra cerca del 31?", size=13)
yy = d.y; h_ = d.image("fig/F10_arboles_estancia.png", w=CW * 0.62); d.y -= h_ + 2 * mm
xx = ML + CW * 0.65
for i, (v, u, l) in enumerate([(str(EST['arboles_100']), "", "árboles registrados en 100 m (OSM natural=tree)"), (str(EST['bancos_100']), "", "bancos en 100 m; " + str(EST['bancos_200']) + " en 200 m"), (f1(EST['agua_min_m']), "m", "a la fuente de agua potable más próxima"), (miles(M['viv_100']), "", "viviendas catastrales en 100 m")]):
    d.bignum(xx, yy - 6 * mm - i * 22 * mm, v, u, l, w=CW * 0.34)
d.caption("Árboles (verde), bancos (cuadro) y agua potable (azul).", "Inventario OSM local recortado; no acredita funcionamiento, sombra real ni acceso. Radios de 100 y 200 m.", "OpenStreetMap © colaboradores, ODbL · ambito_osm_recortado.geojson")

# ======================= PARTE III · SOCIEDAD Y TIEMPO
d.page("III · sociedad y tiempo")
d.kicker("III.1 · quién vive en embajadores"); d.nivel("A", y=d.y + 7.2 * mm)
d.title("¿Para quién es la vivienda pequeña aquí?")
d.lead("Casi la mitad de los hogares de Embajadores son de una persona. La vivienda pequeña no es una excepción del barrio: es su forma más común.")
y0 = d.y - 6 * mm
for i, (v, u, l) in enumerate([("48.085", "", "habitantes en Embajadores, 1-1-2026"), ("49,7", "%", "hogares de una persona (11.843 de 23.818)"), ("2,02", "", "personas por hogar"), ("4.233", "", "personas de 20 a 39 años que viven solas"), ("78,4", "%", "población de 16 a 64 años"), ("34,5", "%", "nacionalidad extranjera"), (miles(M['viv_200']), "", "viviendas catastrales a menos de 200 m del 31 (mínimo: la consulta no cubre 19 m del borde oeste)"), ("27,3", "%", "hogares de dos personas")]):
    d.bignum(ML + (i % 4) * CW / 4, y0 - (i // 4) * 25 * mm, v, u, l, w=CW / 4 - 5 * mm)
d.y = y0 - 50 * mm
d.caption("Padrón Municipal de Habitantes.", "Explotación estadística a 1 de enero de 2026: población por edad, hogares por tamaño y personas que viven solas (archivos C141230126, C14150126, C14150926). Las viviendas catastrales son las declaradas por edificio (numberOfDwellings).", "Ayuntamiento de Madrid · Catastro INSPIRE BU")
d.kicker("III.2 · qué significa joven en este proyecto"); d.nivel("C", y=d.y + 7.2 * mm)
d.para("La promoción municipal de Vara de Rey 12 (2010) se destinó a menores de 35 años. La edad no basta: el programa distingue cuatro situaciones que necesitan cosas distintas.")
d.table([["situación", "estancia", "necesita", "no quiere compartir"],
         ["A · primera emancipación", "6–12 meses", "dormir, estudiar, almacenar", "dormitorio, baño"],
         ["B · trabajo inestable", "variable", "descanso, teletrabajo, búsqueda", "horarios, silencio"],
         ["C · residencia prolongada", "12–24 meses", "apropiarse, recibir, cuidar", "cocina propia"],
         ["D · convivencia de dos", "cambiante", "privacidad doble, tareas compartidas", "salón"]], [44 * mm, 24 * mm, 60 * mm, 50 * mm])
d.caption("Escenario C.", "Perfiles de trabajo heredados del análisis 03; deben contrastarse con entrevistas antes de fijar el programa.")

d.page()
d.kicker("III.3 · la semana del rastro"); d.nivel("A", y=d.y + 7.2 * mm)
d.title("¿Cómo cambia la calle el domingo?")
d.lead("La misma calle alterna entre una condición cotidiana y otra de máxima intensidad. 1.200 puestos autorizados montan a las 8, venden de 9 a 15, desmontan hasta las 16 y la limpieza termina a las 18.")
# timeline
y = d.y - 8 * mm; x0 = ML; w = CW
c.setStrokeColor(TEC); c.setLineWidth(0.4); c.line(x0, y, x0 + w, y)
seg = [(0, 8, "reserva de calle · prohibido estacionar desde las 0 h", PANEL), (8, 9, "montaje", HexColor("#f8a870")), (9, 15, "mercado · 1.200 puestos", HexColor("#e8683a")), (15, 16, "desmontaje", HexColor("#f8a870")), (16, 18, "limpieza", HexColor("#fdd9b5")), (18, 24, "uso cotidiano", PANEL)]
for a, b, lab, col in seg:
    c.setFillColor(col); c.rect(x0 + a / 24 * w, y + 1 * mm, (b - a) / 24 * w, 6 * mm, stroke=0, fill=1)
for hh in (0, 8, 9, 15, 16, 18, 24):
    c.line(x0 + hh / 24 * w, y - 1 * mm, x0 + hh / 24 * w, y + 1 * mm); d.label(x0 + hh / 24 * w, y - 4 * mm, f"{hh:02d}:00", 5.2, TEC, "G", "c")
for a, b, lab, col in seg:
    if b - a >= 2: d.label(x0 + (a + b) / 2 / 24 * w, y + 3 * mm, lab, 5.4, TINTA, "G", "c")
d.label(x0 + 8.5 / 24 * w, y + 8.5 * mm, "montaje 8–9", 5, TEC, "G", "c"); d.label(x0 + 15.5 / 24 * w, y + 8.5 * mm, "desmontaje 15–16", 5, TEC, "G", "c")
d.y = y - 10 * mm
d.table([["estado", "horas", "lo que cambia en el frente del 31", "exigencia al proyecto"],
         ["Preparación", "0–9", "calle sin coches, llegan mercancías y estructuras ligeras", "acceso de residentes libre; almacenaje de puestos no en portales"],
         ["Máxima ocupación", "9–15", "puestos, toldos y peatones reducen el paso; el portal puede quedar oculto", "portal legible y retranqueado; doble filtro acústico"],
         ["Retirada y limpieza", "15–18", "carros, residuos y vehículos autorizados", "recogida de residuos fuera del vestíbulo"],
         ["Cotidiano", "resto", "comercio fijo, tránsito local, persianas bajadas en festivos", "fachada de cierre (P02) y planta baja activa"]],
        [30 * mm, 14 * mm, 70 * mm, 64 * mm])
d.caption("Fuente A; exigencias C.", "Horario, número de puestos y cortes de tráfico del Ayuntamiento. Ninguna imagen del recorrido es de domingo con mercado: la ocupación real delante del 31 queda pendiente de observación (VII).", "madrid.es · Mercadillo El Rastro · Calles afectadas por cortes de tráfico")
d.kicker("III.4 · corralas, umbrales y habitar"); d.nivel("A/B", y=d.y + 7.2 * mm)
d.title("¿Qué enseña la casa de corredor al 31?", size=13)
d.para("La corrala organiza parcelas profundas con patio y galería: lleva luz, aire y acceso al interior de la manzana. También fue infravivienda: exposición, ruido y apropiaciones del corredor. El 31 es una parcela profunda (49,5 m) con 14,9 m de frente: el mismo problema de fondo.")
d.table([["referencia", "dato", "lección"],
         ["Sombrerete 13", "casa de corredor histórica", "patio + galería como gradiente público–privado"],
         ["Carlos Arniches 3-5", "corrala rehabilitada como centro cultural", "el patio admite uso colectivo, pero no es intimidad doméstica"],
         ["Embajadores 46", "cuerpo de 6 plantas a calle y 4 interior", "la fachada no revela la organización de la parcela"],
         ["Vara de Rey 12 (2010)", "22 viviendas jóvenes, 6 plantas, patio de 300 m²; 18 a plaza, 4 a patio en plantas altas", "separar circulación, estancia y control solar"]],
        [36 * mm, 66 * mm, 76 * mm], fs=6.4)
d.caption("Gradiente necesario:", "calle (público) → vestíbulo (control) → patio o galería (común) → rellano (proximidad) → vivienda (privado). La comunidad debe ser posible, no obligatoria.", "Paredes Giraldo, UPM 2012 · Ayuntamiento de Madrid (Vara de Rey 12, Embajadores 46, La Corrala)")

# ======================= PARTE IV · RECORRIDO Y CENSO
d.page("IV · recorrido y censo")
d.kicker("IV.1 · el recorrido"); d.nivel("A", y=d.y + 7.2 * mm)
d.title("¿Cómo se ha mirado la calle?")
d.lead("Veintitrés estaciones sobre el eje de Ribera, de Cascorro a la Ronda de Toledo: cada 40 m y cada 20 m en los 130 m a cada lado del 31. Una sola campaña (2021-07 a 2022-03) para comparar con la misma luz y el mismo estado.")
yy = d.y; h_ = d.image("fig/F08_recorrido.png", w=CW * 0.74, x=ML); d.y -= h_ + 2 * mm
xx = ML + CW * 0.77
d.para("<b>Estaciones.</b> Magenta: S01–S23. Gris oscuro con código: los 44 edificios cuyo frente toca la alineación de Ribera (E = acera este, impares; O = acera oeste, pares).", x=xx, y=yy, w=CW * 0.23, st=sty(6.6, 8.9, color=TEC))
d.para("<b>Por qué así.</b> El recorrido anterior elegía capturas por interés visual; aquí el muestreo es regular y la unidad de análisis es el edificio catastral, no la foto. Así se puede contar cuántos frentes tienen un rasgo y cuántos no.", x=xx, y=yy - 38 * mm, w=CW * 0.23, st=sty(6.6, 8.9, color=TEC))
d.para("<b>Panorámicas.</b> Completas (8192 × 4096 px, 360°), no capturas de pantalla: cualquier vista puede recalcularse con su orientación exacta.", x=xx, y=yy - 82 * mm, w=CW * 0.23, st=sty(6.6, 8.9, color=TEC))
d.caption("Recorrido Street View rehecho el " + HOY + ".", "Selección automática de la panorámica más próxima a cada punto del eje (radio 12 m) y de la campaña más cercana a 2022-03. Tabla completa en el Anexo A3.", "Google Street View (metadatos GeoPhotoService) · eje OSM de Ribera · EPSG:25830")

for side, lab, flip in (("E", "acera este · impares", False), ("W", "acera oeste · pares", True)):
    d.page()
    d.kicker(f"IV.2 · alzado continuo · {lab}"); d.nivel("B", y=d.y + 7.2 * mm)
    d.title(f"La {lab.split(' ·')[0]} completa, de Cascorro a la Ronda")
    for k, (a, b) in enumerate([(0, 160), (160, 320), (320, 480), (480, 640)]):
        f = f"fig/strips/continuo_{side}_{a}_{b}.jpg"
        yt = d.y - 5 * mm
        h = d.image(f, y=yt)
        # códigos de frente
        for r in R:
            if r["side"] != side: continue
            m = (r["s0"] + r["s1"]) / 2
            if not (a <= m < b): continue
            t = (m - a) / 160 if not flip else (b - m) / 160
            d.label(ML + t * CW, yt + 1.2 * mm, cod(r["codigo"]), 5, TINTA, "GB", "c")
        for i, e in enumerate(META["estaciones"]):
            if a <= e["s_m"] < b:
                t = (e["s_m"] - a) / 160 if not flip else (b - e["s_m"]) / 160
                c.setStrokeColor(MAG); c.setLineWidth(0.6); c.line(ML + t * CW, yt - h - 0.2 * mm, ML + t * CW, yt - h - 1.8 * mm)
                d.label(ML + t * CW, yt - h - 4.2 * mm, f"S{i+1:02d}", 4.6, MAG, "G", "c")
        if side == "E" and a <= 358 < b:
            t = (358.7 - a) / 160; d.label(ML + t * CW, yt - h + 2 * mm, "31", 7, MAG, "GB", "c")
        d.label(ML if not flip else PW - MR, yt - h - 7.2 * mm, f"{a}–{b} m desde Cascorro" + ("  (norte → sur)" if not flip else "  (sur ← norte)"), 5, GRIS, "G", "l" if not flip else "r")
        d.y = yt - h - 9 * mm
    d.caption("Alzado rectificado continuo.", ("Cada columna proyecta la panorámica de la estación más próxima sobre la línea de fachada, hallada por rayos perpendiculares al eje contra las huellas catastrales; en los huecos (calles, plazas, solar 31) la línea se interpola. Costuras verticales = cambio de estación. Resolución 0,05 m/px; 36 m de alto." + (" La acera oeste se muestra como se ve desde la calle: el sur a la izquierda." if flip else "")), "Street View S01–S23 · Catastro INSPIRE BU · continuo.py")

d.page()
d.kicker("IV.3 · censo de frentes"); d.nivel("B", y=d.y + 7.2 * mm)
d.title("Cuarenta y dos fachadas, una ficha cada una")
d.para("Cada tarjeta es el alzado rectificado de un frente catastral, a su propia escala. Código, año catastral y plantas de fachada debajo; el punto indica el tipo de balcón dominante.")
cards = sorted(R, key=lambda r: (r["side"], r["s0"]))
ncol = 7; cw_ = (CW - (ncol - 1) * 2 * mm) / ncol; chh = cw_ * 1.25
for i, r in enumerate(cards):
    x = ML + (i % ncol) * (cw_ + 2 * mm); y = d.y - (i // ncol) * (chh + 9 * mm)
    ir = ImageReader(r["file"]); iw, ih = ir.getSize()
    # recorte centrado a proporción de tarjeta
    from PIL import Image as PI
    im = PI.open(r["file"]); ar = cw_ / chh
    if iw / ih > ar:
        nw = int(ih * ar); x0_ = (iw - nw) // 2; im = im.crop((x0_, 0, x0_ + nw, ih))
    else:
        nh = int(iw / ar); im = im.crop((0, ih - nh, iw, ih))
    im.thumbnail((500, 700)); fn = f"fig/panel/card_{r['codigo']}.jpg"; im.save(fn, quality=85)
    c.drawImage(fn, x, y - chh, cw_, chh)
    bal = C[r["codigo"]]["balcon"]
    col = {"ind": TINTA, "mixto": AGUA, "corr": AGUA, "ninguno": None, None: None}[bal]
    if col: c.setFillColor(col); c.circle(x + cw_ - 2 * mm, y - chh - 2.6 * mm, 1.1 * mm, stroke=0, fill=1)
    else: c.setStrokeColor(TEC); c.setLineWidth(0.4); c.circle(x + cw_ - 2 * mm, y - chh - 2.6 * mm, 1.1 * mm, stroke=1, fill=0)
    d.label(x, y - chh - 3.2 * mm, cod(r["codigo"]), 5.8, TINTA, "GB")
    d.label(x + 7.5 * mm, y - chh - 3.2 * mm, f"{r['anio']} · {r['plantas_frente']} pl", 5, TEC)
    d.label(x, y - chh - 6.2 * mm, r["rc"], 4.2, GRIS)
d.y -= math.ceil(len(cards) / ncol) * (chh + 9 * mm)
d.caption("Punto:", "negro = balcón individual por hueco; azul = corrido o mixto; hueco = sin balcón o no legible. Los alzados comparten método pero no escala entre tarjetas.", "Anexo A4 · fachadas_index.json")

d.page()
d.kicker("IV.4 · matriz de rasgos"); d.nivel("B", y=d.y + 7.2 * mm)
d.title("¿Qué rasgos aparecen juntos en cada frente?")
d.image("fig/F11_matriz.png", w=CW)
d.caption("Censo de 42 frentes × 12 rasgos.", "Negro = presente; blanco = ausente; rayado = no legible (arbolado, recorte, obra). Lectura visual de un único observador sobre alzados rectificados de 2021–2022: nivel B. Un frente puede tener varios rasgos a la vez.", "codificacion_fachadas.py")

# ======================= PARTE V · PATRONES
d.page("V · patrones")
d.kicker("V.0 · regla de patrón")
d.title("Qué se admite como patrón")
d.lead("Un rasgo es patrón si aparece en al menos ocho frentes catastrales distintos del censo. Se publica siempre como n / frentes legibles, con su variación y su excepción.")
rows = [["patrón", "frentes con el rasgo", "legibles", "prevalencia", "estado"]]
for p in PAT:
    rows.append([f"{p['id']} · {p['nombre']}", str(p["n"]), str(p["N"]), f"{round(p['n']/p['N']*100)} %", "admitido" if p["n"] >= 8 else "no alcanza"])
rows += [["P10 · Salto de altura entre vecinos", str(M["saltos_ge2"]), str(M["saltos_total"]) + " medianeras", f"{round(M['saltos_ge2']/M['saltos_total']*100)} %", "admitido (A)"],
         ["P11 · Sustitución parcela a parcela", "19 frentes ≥ 1960", "44", "43 %", "admitido (A)"],
         ["— Balcón corrido o banda", "1 (+2 mixtos)", "39", "3 %", "variante, no patrón"],
         ["— Mirador acristalado", "3", "39", "8 %", "no alcanza"],
         ["— Pasaje o galería comercial al interior", "2 (E15, O16)", "44", "5 %", "singularidad relevante"]]
d.table(rows, [70 * mm, 30 * mm, 26 * mm, 24 * mm, 28 * mm])
d.para("<b>Cómo leer cada lámina.</b> Ocho casos con letra (A–H), todos recortes de alzado rectificado a la misma escala y con la misma banda de altura (planta baja, plantas altas o remate). Bajo cada letra, el código del frente, su año y sus plantas. Debajo, la tira de la calle sitúa todos los frentes con el rasgo. Texto: lectura, variación, consecuencia y límite.")
d.panel("Los casos se eligieron entre los frentes con el rasgo por legibilidad (menos arbolado). Las cifras cuentan todos los frentes codificados, no solo los ocho mostrados. Las imágenes son de días laborables: los rasgos dominicales (puestos, toldos del mercado) no están en este censo.", title="límite común a todas las láminas")

import patrones as PM
def lamina(p, texto):
    d.page()
    d.kicker(f"{p['id']} · patrón"); d.nivel("B", y=d.y + 7.2 * mm)
    d.title(p["pregunta"])
    d.lead(f"<b>{p['nombre']}.</b> {p['n']} de {p['N']} frentes legibles ({round(p['n']/p['N']*100)} %).")
    z0, z1, w = PM.bands(p, p["casos"][0])
    ncol = 3 if p["banda"] == "pb" else 4; gw = (CW - (ncol - 1) * 3 * mm) / ncol
    gh = gw * (z1 - z0) / w
    gh = min(gh, 52 * mm); nrow = math.ceil(len(p["casos"]) / ncol)
    for i, cc in enumerate(p["casos"]):
        x = ML + (i % ncol) * (gw + 3 * mm); y = d.y - 2 * mm - (i // ncol) * (gh + 9 * mm)
        fn = f"fig/panel/{p['id']}_{cc}.jpg"; ir = ImageReader(fn); iw, ih = ir.getSize()
        # encaje sin deformar: recorte a proporción
        from PIL import Image as PI
        im = PI.open(fn); ar = gw / gh
        if iw / ih > ar: nw = int(ih * ar); im = im.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
        else: nh = int(iw / ar); im = im.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))
        fn2 = fn.replace(".jpg", "_fit.jpg"); im.save(fn2, quality=88)
        c.drawImage(fn2, x, y - gh, gw, gh)
        c.setFillColor(white); c.rect(x, y - 6 * mm, 6 * mm, 6 * mm, stroke=0, fill=1)
        d.label(x + 3 * mm, y - 4.6 * mm, "ABCDEFGH"[i], 9, TINTA, "GB", "c")
        r = RC[cc]; d.label(x, y - gh - 3.2 * mm, cod(cc), 5.8, TINTA, "GB"); d.label(x + 7 * mm, y - gh - 3.2 * mm, f"{r['anio']} · {r['plantas_frente']} pl · {r['rc']}", 4.8, TEC)
    if ncol == 3:
        x = ML + 2 * (gw + 3 * mm); y = d.y - 2 * mm - 2 * (gh + 9 * mm)
        d.para(f"<b>Banda mostrada.</b> Planta baja: de −0,2 a 5,6 m sobre la acera, 9 m de ancho de fachada por recorte. Misma escala en los ocho casos.", x=x, y=y - 2 * mm, w=gw, st=sty(6.4, 8.6, color=TEC))
    d.y -= 2 * mm + nrow * (gh + 9 * mm)
    # tira de la calle
    y = d.y - 4 * mm; k, v = p["campo"]
    c.setStrokeColor(TEC); c.setLineWidth(0.3)
    for sd, yy in (("E", y), ("W", y - 6 * mm)):
        c.line(ML, yy, ML + CW, yy); d.label(ML - 1 * mm, yy - 1, "E" if sd == "E" else "O", 5, TEC, "G", "r")
        for r in R:
            if r["side"] != sd: continue
            x0 = ML + r["s0"] / 660 * CW; x1 = ML + r["s1"] / 660 * CW
            val = C[r["codigo"]][k]
            if val == v: c.setFillColor(TINTA); c.rect(x0, yy - 1.2 * mm, max(x1 - x0, 0.6), 2.4 * mm, stroke=0, fill=1)
            elif val is None: c.setFillColor(PANEL); c.rect(x0, yy - 1.2 * mm, max(x1 - x0, 0.6), 2.4 * mm, stroke=0, fill=1)
            else: c.setStrokeColor(FILETE); c.rect(x0, yy - 1.2 * mm, max(x1 - x0, 0.6), 2.4 * mm, stroke=1, fill=0)
            if r["codigo"] in p["casos"]: d.label((x0 + x1) / 2, yy + 1.8 * mm if sd == "E" else yy - 4.2 * mm, "ABCDEFGH"[p["casos"].index(r["codigo"])], 5.2, MAG, "GB", "c")
    x31 = ML + 358.7 / 660 * CW; d.label(x31, y + 4.6 * mm, "31", 5.5, MAG, "GB", "c")
    d.label(ML, y - 10.5 * mm, "Tira de Ribera, de Cascorro (izquierda) a la Ronda (derecha). Negro: frente con el rasgo · blanco: sin él · gris: no legible · letra: caso mostrado.", 4.9, GRIS)
    d.y = y - 14 * mm
    for b, t in texto:
        d.para(f"<b>{b}</b> {t}", gap=1.6)

TX = {
"P01": [("Lectura.", "El hueco vertical de suelo a techo con su balcón de cerrajería es la unidad que se repite. El orden por ejes verticales aparece en 36 de 38 frentes legibles."),
        ("Variación.", "Vuelo de losa (O02, O03) o balcón enrasado con barandilla (E14, O13); barandilla de barrote simple o de forja con remates; carpintería de madera con contraventanas (O13) o de aluminio."),
        ("Consecuencia.", "Una fachada del 31 que use el hueco con balcón propio continúa la calle sin copiarla. Pregunta: ¿qué comparte cada vivienda con la calle, solo la vista o también un exterior mínimo de 0,4–0,6 m?"),
        ("Límite.", "El balcón corrido solo aparece en E08 (1973) y como mixto en E09 y O19: no es patrón de esta calle.")],
"P02": [("Lectura.", "El comercio en planta baja es casi universal (37 de 39). Cuando cierra, 19 de 33 frentes legibles bajan un cierre enrollable metálico y 23 de 37 muestran grafiti sobre cierres o zócalo."),
        ("Variación.", "Cierre ciego de lamas, cierre de malla, puerta de madera; rótulo en banda continua (E10) o por local; portal residencial entre locales."),
        ("Consecuencia.", "La planta baja del 31 tiene dos fachadas: abierta y cerrada. Diseñar la de cierre como superficie prevista (gráfica, perforada o reversible) evita que el grafiti sea el único acabado de la noche y del domingo por la tarde."),
        ("Límite.", "El grafiti se registra como presencia visible en 2021–2022; no se juzga ni se atribuye a un grupo.")],
"P03": [("Lectura.", "En 27 de 34 frentes legibles la pared cambia de material al tocar la calle: piedra, placado o revoco de otro color hasta la altura de la planta baja o del zócalo."),
        ("Variación.", "Sillares de granito en toda la planta baja (O11, O22), zócalo bajo interrumpido por las puertas (O02, O03), mármol pulido (O19)."),
        ("Consecuencia.", "El basamento del 31 recibe roce, limpieza, carteles y agua de la acera en pendiente (6,8 %). Elegir material por comportamiento y resolver el encuentro con una acera que baja ≈1 m a lo largo del frente."),
        ("Límite.", "No se identifica el tipo de piedra ni su espesor: solo la diferencia visible.")],
"P04": [("Lectura.", "26 de 38 frentes marcan el borde del hueco con un recercado: moldura, franja pintada o cambio de material."),
        ("Variación.", "Recercado blanco sobre ladrillo (E14), orejetas en revoco rosa (O09), jambas pétreas (O11), franja pintada (E06)."),
        ("Consecuencia.", "El recercado da escala doméstica a fachadas altas. En el 31 puede resolverse como pieza real de carpintería o de protección, no como ornamento aplicado."),
        ("Límite.", "El recercado se lee en superficie; no se deduce su construcción.")],
"P05": [("Lectura.", "18 de 37 frentes legibles tienen toldos o textiles en plantas altas, casi siempre por vivienda y a distinta altura de despliegue."),
        ("Variación.", "Toldo de brazo verde o a rayas (E10, E16), lona recogida, persiana de librillo; en E08 las bandas textiles siguen la terraza corrida."),
        ("Consecuencia.", "La sombra la decide cada vivienda. El 31 recibe entre 8 y 14 h de sol en junio (II.6): prever la posición y la recogida del textil desde el alzado."),
        ("Límite.", "Imágenes de invierno y primavera: en verano la presencia sería mayor.")],
"P06": [("Lectura.", "24 de 36 frentes legibles tienen macetas o plantas en balcones: el cultivo ocurre en el borde de la vivienda, no en el suelo."),
        ("Variación.", "Jardineras colgadas de la barandilla, macetas en el vuelo, trepadoras."),
        ("Consecuencia.", "Si el proyecto quiere vegetación, el balcón y la cubierta son los soportes naturales; el suelo del solar apenas recibe sol en invierno (II.5)."),
        ("Límite.", "No se distingue planta viva de artificial en todos los casos (O12).")],
"P07": [("Lectura.", "23 de 37 frentes terminan con alero o cornisa volada que proyecta sombra sobre la última planta."),
        ("Variación.", "Alero de madera con canecillos (O02), cornisa moldurada (O14), teja vista (E11), remate plano sin vuelo en los edificios de 1990–2018."),
        ("Consecuencia.", "La calle se lee por sus remates a distinta altura (P10). El 31 decide qué cornisa continúa: la de la base norte o la del vecino sur."),
        ("Límite.", "El vuelo real no se mide: el alzado proyecta sobre el plano de fachada.")],
"P08": [("Lectura.", "14 de 36 frentes muestran cables, bajantes o máquinas de climatización sobre la fachada: una trama añadida al orden de huecos."),
        ("Variación.", "Cableado horizontal que salta de edificio a edificio (O06), bajantes vistas (E03), climatizadores en cada ventana (E11)."),
        ("Consecuencia.", "Prever recorridos registrables y lugares para máquinas desde el inicio evita que la segunda trama aparezca después."),
        ("Límite.", "No se identifica el servicio de cada cable.")],
"P09": [("Lectura.", "En 8 de 37 frentes el comercio saca objetos a la acera un día laborable: jaulas, muebles, expositores, pizarras."),
        ("Variación.", "Mercancía colgada del dintel (O18), apoyada en el zócalo (O19, O21), veladores y pizarras de hostelería (O02, O03)."),
        ("Consecuencia.", "El umbral del 31 debe admitir exposición sin bloquear el acceso a las viviendas: un retranqueo o un zócalo con apoyos."),
        ("Límite.", "Justo en el umbral de ocho casos y sin imágenes de domingo: es el patrón con menos evidencia del censo.")],
}
for p in PAT: lamina(p, TX[p["id"]])

# P10 / P11 y singularidades
d.page()
d.kicker("P10–P11 · patrones medidos"); d.nivel("A", y=d.y + 7.2 * mm)
d.title("¿Por qué las alturas y los estilos cambian de un edificio a otro?")
d.lead(f"Porque la calle se ha construido y sustituido parcela a parcela. En {M['saltos_ge2']} de {M['saltos_total']} medianeras contiguas la altura salta dos plantas o más; los frentes se reparten entre 1850 y 2018.")
d.image("fig/F12_anios_frentes.png")
d.caption("P11 · año catastral de cada frente.", "Marrón: antes de 1900 · ocre: 1900–1959 · verde agua: 1960–1999 · azul: desde 2000.", "Catastro INSPIRE BU")
hist = {}
for j in M["saltos"]: hist[j] = hist.get(j, 0) + 1
d.table([["salto entre vecinos (plantas)"] + [str(k) for k in sorted(hist)], ["medianeras"] + [str(hist[k]) for k in sorted(hist)]], [50 * mm] + [16 * mm] * len(hist))
d.para("<b>Consecuencia.</b> No hay una altura de cornisa que continuar: hay una secuencia de alturas distintas. El 31 puede fijar la suya por sol, programa y relación con cada vecino (II.3, II.6) sin «romper» una uniformidad que no existe.")
d.kicker("singularidades relevantes (menos de ocho casos)")
d.table([["rasgo", "frentes", "por qué importa al 31"],
         ["Pasaje o galería comercial al interior de manzana", "E15 Galerías Piquer · O16 galería en dos niveles", "El vecino norte ya perfora la manzana: posibilidad de relación trasera con su patio comercial (a verificar)"],
         ["Solar con nave baja y atrio", "31", "Único hueco de cornisa del tramo; hoy funciona como patio de luz de los vecinos"],
         ["Balcón corrido / terraza en banda", "E08 (puro) · E09, O19 (mixtos)", "Variante de P01; útil si se quiere un borde común, pero no es lo habitual"],
         ["Mirador acristalado", "O08, O21, E17", "Solución para ganar luz y vista en plantas altas"]],
        [58 * mm, 52 * mm, 68 * mm], fs=6.4)

# ======================= TEXTURAS
d.page("V · texturas")
d.kicker("V.T · texturas fotografiadas en campo"); d.nivel("B", y=d.y + 7.2 * mm)
d.title("¿Qué se toca, se gasta y se repara?")
d.para("Treinta y tres fotografías propias del entorno. Sin coordenadas GPS: su localización exacta no se verifica y no cuentan para el censo de patrones. Complementan los alzados con la escala de la mano.")
ncol = 7; tw = (CW - (ncol - 1) * 2 * mm) / ncol; th = tw * 1.2
for i, x_ in enumerate(INV):
    x = ML + (i % ncol) * (tw + 2 * mm); y = d.y - (i // ncol) * (th + 6.5 * mm)
    from PIL import Image as PI
    im = PI.open(f"fig/fotos/{x_['id']}.jpg"); iw, ih = im.size; ar = tw / th
    if iw / ih > ar: nw = int(ih * ar); im = im.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
    else: nh = int(iw / ar); im = im.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))
    fn = f"fig/fotos/{x_['id']}_fit.jpg"; im.save(fn, quality=84)
    c.drawImage(fn, x, y - th, tw, th)
    d.label(x, y - th - 3 * mm, x_["id"], 5.6, TINTA, "GB")
    d.label(x + 5.5 * mm, y - th - 3 * mm, x_["analisis"][0][:26], 4.4, TEC)
d.y -= math.ceil(len(INV) / ncol) * (th + 6.5 * mm)
d.page()
d.kicker("V.T · lectura de cada textura")
d.title("Superficie, contacto y reparación", size=13)
rows = [["foto", "rasgo", "lectura", "nota de control"]]
for x_ in INV:
    a = x_["analisis"]; rows.append([x_["id"], a[0], a[1], a[3] if len(a) > 3 else ""])
d.table(rows, [10 * mm, 34 * mm, 88 * mm, 46 * mm], fs=5.6)

# ======================= PARTE VI · CRUCES Y HALLAZGOS
d.page("VI · cruces y hallazgos")
d.kicker("VI.1 · matriz de cruces")
d.title("¿Qué análisis se explican entre sí?")
d.table([["", "sol (II.5–6)", "alturas (II.1, P10)", "pendiente (II.4)", "comercio (P02, P09)", "domingo (III.3)"],
         ["sol", "—", "los vecinos de 8–10 pl. fijan la cota útil ≈20 m", "", "planta baja sin sol: uso comercial y de servicio", "toldos del mercado: sin datos"],
         ["alturas", "", "—", "", "base comercial continua de 1–3 pl. bajo cuerpos altos", ""],
         ["pendiente", "", "", "—", "umbral con dos cotas; exposición en acera inclinada", "carga y descarga en pendiente"],
         ["comercio", "", "", "", "—", "cierre el domingo por la tarde = fachada gráfica"],
         ["hogares pequeños (III.1)", "comunes en altura con sol", "", "", "taller y almacén en planta baja", "almacén para objetos del mercado"]],
        [30 * mm, 28 * mm, 32 * mm, 26 * mm, 32 * mm, 30 * mm], fs=5.8)
d.kicker("VI.2 · hallazgos")
HH = [("H-01 · El solar no está vacío", "Catastro: suelo sin edificar, 0 m² (A).", "¿Hay uso?", "Serie de 12 panorámicas 2008–2022 rectificadas (I.3).", "Nave comercial con al menos tres etapas: comercio, liquidación (2013–2014), nuevo inquilino (2018–2022).", "A/B", "La planta baja hereda 14 años de comercio temporal; el derribo de la nave es una decisión de proyecto."),
      ("H-02 · El sol de invierno solo llega arriba", "Suelo: 0,17 h el 21-dic (B).", "¿A partir de qué cota hay sol?", "Sombras a 9 cotas (II.6).", "≥ 2 h en más de la mitad del solar solo desde ≈22 m.", "B", "Comunes con sol en cubierta o plantas 6–7; planta baja para lo que no necesita sol."),
      ("H-03 · Entre 3 y 10 plantas", "Vecinos 10 (norte) y 8 (sur) (A).", "¿Hay una cornisa que continuar?", "Saltos en 28 medianeras (P10).", "9 saltan ≥ 2 plantas; 5 son iguales.", "A", "La altura se decide por sol y programa, no por mimetismo."),
      ("H-04 · Hueco con balcón propio", "Censo de 42 frentes (B).", "¿Unidad o banda?", "Codificación balcón.", "30/39 individual; 1 corrido; 2 mixtos.", "B", "El balcón individual es la regla común de la calle."),
      ("H-05 · Planta baja que se cierra", "37/39 comercial (B).", "¿Cómo es la fachada cerrada?", "Codificación cierre y grafiti.", "19/33 cierre enrollable; 23/37 grafiti.", "B", "Diseñar el estado cerrado."),
      ("H-06 · Tienda en la acera", "8/37 laborable (B).", "¿Ocurre también en domingo?", "No hay imágenes dominicales.", "Pendiente.", "C", "Observación de campo en domingo 10–13 h."),
      ("H-07 · La calle desciende", "Cotas GPS de 23 panorámicas (B).", "¿Cuánto en el frente?", "Diferencia S12–S14.", "6,8 % → ≈1,0 m en 14,9 m.", "B", "Umbral en dos cotas o rampa; comprobar con levantamiento."),
      ("H-08 · Denso y sin estancia", f"≥ {miles(M['viv_200'])} viviendas en 200 m (A).", "¿Dónde se está al aire libre?", "Bancos y agua OSM (II.8).", f"{EST['bancos_100']} bancos en 100 m; agua a {f1(EST['agua_min_m'])} m.", "B", "Un espacio exterior propio (cubierta) tiene valor alto para 40 residentes.")]
d.table([["hallazgo", "observación", "pregunta", "prueba", "resultado", "nivel", "consecuencia"]] + [list(h) for h in HH],
        [28 * mm, 26 * mm, 20 * mm, 24 * mm, 28 * mm, 10 * mm, 42 * mm], fs=5.5)

d.page()
d.kicker("VI.3 · criterios de proyecto"); d.nivel("C", y=d.y + 7.2 * mm)
d.title("Siete decisiones que la investigación permite ensayar")
crit = [("1 · Volumen por sol.", "Concentrar la altura donde llega el sol de invierno y separar el volumen alto del lindero sur (H-02, II.3). Probar dos alternativas: cuerpo a calle de 3 plantas + cuerpo retranqueado alto, o bloque de 6–7 plantas despegado del vecino sur."),
        ("2 · Planta baja de dos estados.", "Comercio o taller hacia Ribera, con acceso residencial independiente y retranqueado; diseñar la fachada abierta y la cerrada (P02, H-05)."),
        ("3 · Umbral en pendiente.", "Resolver ≈1 m de desnivel del frente en el propio umbral: dos cotas de planta baja o rampa exterior bajo el primer vuelo (H-07, P03)."),
        ("4 · Comunes arriba.", "Lavandería-tendedero, estancia exterior y huerto en cubierta o planta 6–7; en planta baja, almacén, bicicletas, paquetería y taller (H-02, H-08, III.1)."),
        ("5 · Hueco con balcón propio.", "Unidad de fachada = hueco vertical con exterior mínimo propio; textil regulable por vivienda con posición prevista (P01, P05, P06)."),
        ("6 · Profundidad como corrala.", "Parcela de 49,5 m de fondo: patio o galería como infraestructura de luz y aire, dimensionada en sección antes que como plaza (III.4)."),
        ("7 · Segunda trama prevista.", "Recorridos registrables de instalaciones y lugar para máquinas desde el anteproyecto (P08).")]
for b, t in crit: d.para(f"<b>{b}</b> {t}", gap=2.4)
d.kicker("VI.4 · doce preguntas motor")
Q = ["¿Qué debe continuar el edificio: la alineación, una cornisa, el ritmo de huecos o la intensidad de la planta baja?", "¿Cómo cambia la entrada si se llega desde arriba o desde abajo de la pendiente?", "¿Qué altura o retranqueo recibe sol sin empeorar a los vecinos?", "¿Qué aporta un patio si su suelo no recibe sol en invierno?", "¿A qué jóvenes se dirige la propuesta y qué necesidades impiden tratarlos como un grupo?", "¿Qué parte de cocinar, lavar o trabajar se compartiría por elección y no por falta de espacio?", "¿Qué acceso permanece operativo cuando se cierra la parte abierta al barrio?", "¿Por dónde entra un mueble voluminoso sin cruzar el acceso doméstico?", "¿Qué se gana y qué se pierde al pasar del balcón individual a una banda continua?", "¿Qué puede regular cada habitante y qué necesita una regla común?", "¿Qué material responde al roce del zócalo en una acera en pendiente?", "¿Qué evidencia haría abandonar la hipótesis inicial aunque su imagen resulte atractiva?"]
for i, q in enumerate(Q):
    col = i % 2; row = i // 2; xx = ML + col * (CW / 2 + 2 * mm); yy = d.y - row * 11 * mm
    d.label(xx, yy - 2.5 * mm, f"{i+1:02d}", 6, MAG, "GB")
    d.para(q, x=xx + 7 * mm, y=yy, w=CW / 2 - 10 * mm, st=sty(7, 9.4))
d.y -= 6 * 11 * mm

d.page()
d.kicker("VI.5 · lo que no sabemos")
d.title("Límites y trabajo de campo pendiente")
d.table([["hueco", "por qué importa", "cómo cerrarlo", "prioridad"],
         ["Norma urbanística de la parcela", "altura máxima, fondo, protección", "visor urbanístico del Ayuntamiento; ficha de condiciones", "1"],
         ["Levantamiento del solar y cotas", "desnivel de ≈1 m (B), medianeras reales", "levantamiento con cinta y nivel o topográfico", "1"],
         ["Altura real de cada planta vecina", "sombras calculadas con hipótesis 4,0 + 3,1 m", "medir cornisas en alzado rectificado o in situ", "2"],
         ["Domingo con mercado delante del 31", "P09 y III.3 sin imágenes dominicales", "tres visitas: domingo 10–13, domingo 15–17, laborable 10–13", "1"],
         ["Conteos peatonales y ruido", "acceso, fachada acústica", "5 min por punto en los mismos puntos; sonómetro de móvil (orientativo)", "2"],
         ["Entrevistas a jóvenes y vecinos", "programa (C)", "10–15 entrevistas breves sobre tareas, almacenaje, ruido", "2"],
         ["Relación trasera con Galerías Piquer", "posible acceso o patio compartido", "visita y plano catastral de la manzana 01349", "3"],
         ["Fotos propias sin GPS", "no entran en el censo", "repetir con localización activada", "3"]],
        [44 * mm, 44 * mm, 76 * mm, 14 * mm], fs=6.2)
d.panel("Protocolo de campo (heredado y ajustado): en cada estación S11–S15 y en el umbral del 31, anotar fecha, hora, clima, personas en 5 min, acciones dominantes, dirección, obstáculos, sombra, residuos, apertura de comercios y estado del portal; fotografiar desde la misma posición que la panorámica para comparar. Entrevistas breves y voluntarias; patios privados solo con permiso.", title="protocolo")

# ======================= ANEXOS
d.page("anexos")
d.kicker("A1 · registro de métricas")
d.title("Toda cifra publicada, con su origen", size=14)
d.table([["id", "valor", "unidad", "nivel", "método", "fuente"]] + [list(r) for r in REG] + [
    ["IV-1", "42", "frentes codificados", "B", "lectura visual", "codificacion_fachadas.py"],
    ["IV-2", "23", "estaciones", "A", "SingleImageSearch", "G3SV_metadatos.json"],
    ["II.8-1", str(EST['arboles_100']), "árboles 100 m", "B", "OSM natural=tree", "ambito_osm_recortado"],
    ["III.1-1", "49,7", "% hogares unipersonales", "A", "Padrón", "C14150126"]],
    [16 * mm, 20 * mm, 38 * mm, 10 * mm, 42 * mm, 52 * mm], fs=5.6)
d.page()
d.kicker("A2 · estaciones del recorrido")
d.title("Veintitrés panorámicas", size=14)
rows = [["est.", "s (m)", "fecha", "panorama", "lat", "lon", "dirección de referencia"]]
for i, e in enumerate(META["estaciones"]):
    rows.append([f"S{i+1:02d}", f"{e['s_m']:.0f}", e["fecha"], e["pano"], f"{e['lat']:.6f}", f"{e['lon']:.6f}", e["addr"]])
d.table(rows, [10 * mm, 12 * mm, 14 * mm, 44 * mm, 20 * mm, 20 * mm, 58 * mm], fs=5.6)
d.para("S16 está en el cruce con la calle Mira el Sol (panorama de esa calle). Las demás, sobre Ribera. Panorámicas completas en RECORRIDO_STREETVIEW_2026-09-23/PANORAMAS.", st=CAP)
d.page()
d.kicker("A3 · frentes de Ribera")
d.title("Cuarenta y cuatro edificios con frente a la calle", size=14)
rows = [["código", "ref. catastral", "año", "pl. frente", "viv.", "uso catastral", "s (m)"]]
for f_ in sorted(FR, key=lambda f: (f["side"], f["s0"])):
    r = next((x for x in R if x["rc"] == f_["rc"] and x["side"] == f_["side"]), None)
    rows.append([cod(r["codigo"]) if r else "—", f_["rc"], str(f_["anio"]), str(r["plantas_frente"]) if r else "—", str(f_["viviendas"]), (f_["uso"] or "").split("_", 1)[-1], f"{f_['s0']:.0f}–{f_['s1']:.0f}"])
d.table(rows, [16 * mm, 32 * mm, 14 * mm, 16 * mm, 12 * mm, 34 * mm, 24 * mm], fs=5.6)
d.para("Dos frentes (O01 0038906 y O10 0037808) tienen menos de 3 m de alineación y no se codifican. Método del alzado rectificado: cada punto (x, y, z) del plano de fachada catastral se proyecta hacia la cámara (altura supuesta 2,5 m) y se muestrea la panorámica equirrectangular; nivel B por el error de posición de cámara y los elementos fuera de plano.", st=CAP)
d.page()
d.kicker("A4 · fuentes")
d.title("Fuentes y archivos", size=14)
src = ["Dirección General del Catastro. Servicios INSPIRE (CadastralParcel, Building, BuildingPart) y OVC (Consulta_RCCOOR, Consulta_DNPRC). Consulta " + HOY + ". https://ovc.catastro.meh.es",
       "Google Street View. 23 panoramas de recorrido y 11 históricos del nº 31; identificadores en G3SV_metadatos.json. Imágenes © Google, usadas como evidencia de análisis académico.",
       "Ayuntamiento de Madrid. Mercadillo El Rastro; Calles afectadas por cortes de tráfico; Padrón Municipal 1-1-2026 (C141230126, C14150126, C14150926); Estudio PIBA 2019; Vara de Rey 12 (2010, 2011); Embajadores 46 (2007); La Corrala; Lavapiés rehabilitado.",
       "AEMET. Valores climatológicos normales Madrid-Retiro 3195, 1981–2010.",
       "NOAA Global Monitoring Laboratory. General Solar Position Calculations.",
       "OpenStreetMap © colaboradores, ODbL. Eje de Ribera, árboles, bancos y agua.",
       "Paredes Giraldo, M. C. (2012). Estudio tipológico, constructivo y estructural de las casas de corredor en Madrid. UPM. https://oa.upm.es/14326/",
       "Referencias de lenguaje: Refugio Climático · Compendio analítico y Sistema gráfico final (IRAXXXDIOS, 2026); láminas Oviedo «Los datos no contienen un futuro»; lámina científica y archivo de diapositivas (REFERENCIAS/IMG_1946–1947).",
       "Investigación previa (archivada): Investigacion_urbana_Ribera_de_Curtidores_31.docx; ENTREGA_1_ANALISIS_EL_RASTRO_5_A3.pdf; catálogos PATRONES_STREET_VIEW, CATALOGO_PATRONES_600M, CATALOGO_CORREGIDO_RIBERA, CATALOGO_EDITORIAL_RIBERA; GUIA_DIAGRAMAS_Y_QGIS; ANÁLISIS DEL LUGAR PRECISO."]
for i, s_ in enumerate(src): d.para(f"<font color='#e5007e'>{i+1:02d}</font>&nbsp;&nbsp;{s_}", st=sty(7, 9.6), gap=1.8)
d.panel("Carpeta 00_INVESTIGACION_COMPLETA: DATOS (Catastro GML, GeoJSON derivados, registros JSON), RECORRIDO_STREETVIEW_2026-09-23 (panorámicas y metadatos), FIGURAS, SCRIPTS (todo reproducible). Vault de Obsidian: G3 Proyectos/00_CEREBRO.", title="dónde está cada cosa")

# ======================= ÍNDICE (volver a la página 5 no es posible en canvas: se dibuja al final en una página nueva y se reordena)
d.save()
json.dump({"toc": d.toc, "idx_page": IDX_PAGE}, open("datos/toc.json", "w"), ensure_ascii=False)
print("páginas", d.n)
