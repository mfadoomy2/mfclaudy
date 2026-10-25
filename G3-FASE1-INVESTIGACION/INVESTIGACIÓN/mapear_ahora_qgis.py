# -*- coding: utf-8 -*-
"""
MAPEO INMEDIATO - G3 / Ribera de Curtidores 31

Ejecutar dentro de QGIS:
    exec(open(r"/Volumes/T7/G3 Proyectos/INVESTIGACIÓN/mapear_ahora_qgis.py", encoding="utf-8").read())

El script carga, ordena y simboliza solo la información disponible ahora.
No convierte hipótesis, intensidades previstas ni geometrías aproximadas en datos medidos.
"""

from pathlib import Path

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QColor
from qgis.core import (
    QgsCoordinateReferenceSystem, QgsFeature, QgsField, QgsFillSymbol,
    QgsCoordinateTransform, QgsGeometry, QgsLayerTreeGroup, QgsLineSymbol, QgsMarkerSymbol,
    QgsPalLayerSettings, QgsProject, QgsProperty, QgsRuleBasedRenderer,
    QgsPointXY, QgsRasterLayer, QgsSingleSymbolRenderer, QgsTextBufferSettings, QgsTextFormat,
    QgsVectorFileWriter, QgsVectorLayer, QgsVectorLayerSimpleLabeling,
)


BASE = Path("/Volumes/T7/G3 Proyectos/INVESTIGACIÓN")
PROJECT_FILE = BASE / "MAPEO_ACTUAL_RIBERA_CURTIDORES_31.qgz"
GPKG = BASE / "MAPEO_ACTUAL_RIBERA_CURTIDORES_31.gpkg"
CRS = QgsCoordinateReferenceSystem("EPSG:4326")
SITE_LON, SITE_LAT = -3.707172, 40.407576  # referencia aproximada; verificar en Catastro

RED = QColor("#dc2b1f")
BLUE = QColor("#557f96")
GREEN = QColor("#4d745d")
INK = QColor("#252525")
GREY = QColor("#8a8a8a")

project = QgsProject.instance()
project.clear()
project.setCrs(QgsCoordinateReferenceSystem("EPSG:25830"))  # Madrid / ETRS89 UTM 30N
root = project.layerTreeRoot()


def group(name):
    old = root.findGroup(name)
    if old:
        root.removeChildNode(old)
    return root.addGroup(name)


def add_to_group(layer, parent):
    if not layer or not layer.isValid():
        raise RuntimeError("Capa no válida: " + (layer.name() if layer else "desconocida"))
    project.addMapLayer(layer, False)
    parent.addLayer(layer)
    return layer


def labels(layer, field, size=8, color=INK):
    s = QgsPalLayerSettings()
    s.fieldName = field
    s.enabled = True
    fmt = QgsTextFormat()
    fmt.setSize(size)
    fmt.setColor(color)
    buf = QgsTextBufferSettings()
    buf.setEnabled(True)
    buf.setSize(1.0)
    buf.setColor(QColor("white"))
    fmt.setBuffer(buf)
    s.setFormat(fmt)
    layer.setLabelsEnabled(True)
    layer.setLabeling(QgsVectorLayerSimpleLabeling(s))


def point_symbol(color, size=3.2, outline=QColor("white")):
    return QgsMarkerSymbol.createSimple({
        "name": "circle", "color": color.name(), "size": str(size),
        "outline_color": outline.name(), "outline_width": "0.5"
    })


def save_memory(layer, layer_name):
    """Guarda una capa de memoria en el GeoPackage y la vuelve a cargar."""
    opts = QgsVectorFileWriter.SaveVectorOptions()
    opts.driverName = "GPKG"
    opts.layerName = layer_name
    opts.actionOnExistingFile = (
        QgsVectorFileWriter.CreateOrOverwriteLayer if GPKG.exists()
        else QgsVectorFileWriter.CreateOrOverwriteFile
    )
    result = QgsVectorFileWriter.writeAsVectorFormatV3(
        layer, str(GPKG), project.transformContext(), opts
    )
    if result[0] != QgsVectorFileWriter.NoError:
        raise RuntimeError("No se pudo escribir {}: {}".format(layer_name, result))
    return QgsVectorLayer(f"{GPKG}|layername={layer_name}", layer_name, "ogr")


def clone_filtered(source, name, expression, color, parent, label_field=None):
    layer = source.clone()
    layer.setName(name)
    layer.setSubsetString(expression)
    layer.setRenderer(QgsSingleSymbolRenderer(point_symbol(color)))
    if label_field:
        labels(layer, label_field)
    return add_to_group(layer, parent)


# 00. BASE Y REFERENCIAS ------------------------------------------------------
g0 = group("00_BASE_Y_REFERENCIAS")

osm = QgsRasterLayer(
    "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmin=0&zmax=19",
    "OpenStreetMap - referencia", "wms"
)
if osm.isValid():
    add_to_group(osm, g0)

site_mem = QgsVectorLayer("Point?crs=EPSG:4326", "Parcela - referencia", "memory")
site_mem.dataProvider().addAttributes([
    QgsField("ID", QVariant.String), QgsField("Direccion", QVariant.String),
    QgsField("Estado", QVariant.String), QgsField("Superficie", QVariant.String),
])
site_mem.updateFields()
f = QgsFeature(site_mem.fields())
f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(SITE_LON, SITE_LAT)))
f.setAttributes(["P001", "Ribera de Curtidores 31", "Coordenada aproximada", "651 m2 - verificar"])
site_mem.dataProvider().addFeature(f)
site = save_memory(site_mem, "parcela_referencia")
site.setRenderer(QgsSingleSymbolRenderer(point_symbol(RED, 5.0, INK)))
labels(site, "Direccion", 9)
add_to_group(site, g0)

# Radios de lectura: proximidad inmediata, barrio caminable y contexto ampliado.
site_utm = QgsCoordinateTransform(CRS, QgsCoordinateReferenceSystem("EPSG:25830"), project).transform(
    QgsPointXY(SITE_LON, SITE_LAT)
)
for metres, name, opacity in [(150, "Radio 150 m - entorno inmediato", 0.18),
                              (300, "Radio 300 m - cinco minutos", 0.12),
                              (500, "Radio 500 m - contexto", 0.07)]:
    mem = QgsVectorLayer("Polygon?crs=EPSG:25830", name, "memory")
    mem.dataProvider().addAttributes([QgsField("radio_m", QVariant.Int)])
    mem.updateFields()
    geom = QgsGeometry.fromPointXY(site_utm).buffer(metres, 48)
    feat = QgsFeature(mem.fields()); feat.setGeometry(geom); feat["radio_m"] = metres
    mem.dataProvider().addFeature(feat)
    lyr = save_memory(mem, "radio_{}m".format(metres))
    sym = QgsFillSymbol.createSimple({"color": RED.name(), "outline_color": RED.name(), "outline_width": "0.35"})
    sym.setOpacity(opacity)
    lyr.setRenderer(QgsSingleSymbolRenderer(sym))
    add_to_group(lyr, g0)


# 01. SISTEMA TEMPORAL DEL RASTRO -------------------------------------------
g1 = group("01_SISTEMA_TEMPORAL_RASTRO")
temporal = QgsVectorLayer(str(BASE / "ocupacion_temporal_rastro.geojson"), "Eje temporal del Rastro", "ogr")
temporal.setRenderer(QgsSingleSymbolRenderer(QgsLineSymbol.createSimple({
    "color": RED.name(), "width": "1.4", "line_style": "solid"
})))
labels(temporal, "Categoria", 8, RED)
add_to_group(temporal, g1)

csv_uri = (
    "file:///{0}?type=csv&delimiter=,&xField=Longitud&yField=Latitud"
    "&crs=EPSG:4326&detectTypes=yes&trimFields=yes"
).format(str(BASE / "flujos_peatonales_y_actividades.csv"))
events = QgsVectorLayer(csv_uri, "Eventos, usuarios y acciones", "delimitedtext")
events.setRenderer(QgsSingleSymbolRenderer(point_symbol(RED, 3.5)))
labels(events, "Categoria", 7)
add_to_group(events, g1)

# Vistas temáticas del mismo CSV: permiten activar una sola lectura cada vez.
categories = [
    ("Mercado", RED), ("Montaje", QColor("#ef7b67")),
    ("Desmontaje", QColor("#b44b3f")), ("Limpieza", BLUE),
    ("Uso cotidiano", GREEN), ("Logística", INK),
]
for category, color in categories:
    clone_filtered(events, "Actividad - " + category, '"Categoria" = \'{}\''.format(category), color, g1, "Accion")


# 02. TIPOLOGÍAS, CORRALAS Y FORMAS DE HABITAR -------------------------------
g2 = group("02_CORRALAS_Y_TIPOLOGIAS")
corralas = QgsVectorLayer(str(BASE / "corralas_y_tipologias_historicas.geojson"),
                         "Corralas y referencias residenciales", "ogr")
corralas.setRenderer(QgsSingleSymbolRenderer(point_symbol(BLUE, 4.0)))
labels(corralas, "Nombre", 8)
add_to_group(corralas, g2)
clone_filtered(corralas, "Casas de corredor históricas", '"Categoria" = \'Corrala\'', BLUE, g2, "Nombre")
clone_filtered(corralas, "Reinterpretación contemporánea", '"Categoria" = \'Vivienda colectiva\'', GREEN, g2, "Nombre")


# 03. OBSERVACIÓN DE CAMPO --------------------------------------------------
g3 = group("03_OBSERVACION_DE_CAMPO")
obs_uri = (
    "file:///{0}?type=csv&delimiter=,&xField=Longitud&yField=Latitud"
    "&crs=EPSG:4326&detectTypes=yes&trimFields=yes"
).format(str(BASE / "plantilla_observacion_campo.csv"))
observations = QgsVectorLayer(obs_uri, "Observaciones de campo - editable en CSV", "delimitedtext")
observations.setRenderer(QgsSingleSymbolRenderer(point_symbol(GREEN, 3.5)))
labels(observations, "ID", 7)
add_to_group(observations, g3)

# Estas copias se llenarán automáticamente al completar el CSV.
field_views = [
    ("Conteos peatonales", '"Conteo_Personas" IS NOT NULL'),
    ("Texturas y materiales", '"Textura" IS NOT NULL AND "Textura" <> \'\''),
    ("Paisaje sonoro", '"Sonido" IS NOT NULL AND "Sonido" <> \'\''),
    ("Sombra y confort", '"Sombra" IS NOT NULL AND "Sombra" <> \'\''),
    ("Obstáculos y accesibilidad", '"Obstaculo" IS NOT NULL AND "Obstaculo" <> \'\''),
]
for name, expr in field_views:
    clone_filtered(observations, name, expr, GREEN, g3, "ID")


# 04. CALIDAD Y LÍMITES DEL DATO --------------------------------------------
g4 = group("04_CALIDAD_Y_DATOS_PENDIENTES")
clone_filtered(events, "Eventos con intensidad pendiente", '"Estado_Dato" ILIKE \'%pendiente%\'', GREY, g4, "Categoria")
clone_filtered(corralas, "Geometría aproximada o centroide", 
               '"Precision_Geometria" ILIKE \'%aproximad%\' OR "Precision_Geometria" ILIKE \'%centroide%\'',
               GREY, g4, "Nombre")


# Orden, visibilidad inicial y guardado --------------------------------------
g4.setItemVisibilityChecked(False)
for child in g1.children()[2:]:
    child.setItemVisibilityChecked(False)
for child in g2.children()[1:]:
    child.setItemVisibilityChecked(False)
for child in g3.children()[1:]:
    child.setItemVisibilityChecked(False)

project.setCustomVariables({
    "proyecto": "G3 - La materia de lo doméstico",
    "emplazamiento": "Ribera de Curtidores 31",
    "advertencia": "No usar hipótesis o geometrías aproximadas como mediciones confirmadas",
})
project.write(str(PROJECT_FILE))

iface.mapCanvas().setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:25830"))
iface.mapCanvas().setExtent(site.extent())
iface.mapCanvas().zoomScale(6000)
iface.mapCanvas().refresh()

print("MAPEO CREADO")
print("Proyecto:", PROJECT_FILE)
print("GeoPackage:", GPKG)
print("Capas disponibles: parcela y radios; ciclo del mercado; actividades y usuarios; corralas y tipologías; observación, conteos, texturas, sonido, sombra, obstáculos y calidad del dato.")
