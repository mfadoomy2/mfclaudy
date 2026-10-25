# -*- coding: utf-8 -*-
"""
INVENTARIO FISICO GEOREFERENCIADO - RIBERA DE CURTIDORES 31

Uso: abrir QGIS > Complementos > Consola de Python y pegar esta linea:

exec(open(r"/Volumes/T7/G3 Proyectos/INVESTIGACIÓN/TODAS_COORDENADAS_FISICAS_QGIS.py", encoding="utf-8").read())

Resultado: consulta todos los elementos fisicos actualmente cartografiados en
OpenStreetMap dentro de 600 m del emplazamiento, conserva sus coordenadas y
geometrias, los clasifica, crea un GeoPackage, exporta inventarios CSV y guarda
un proyecto QGIS. No sustituye un levantamiento topografico ni catastral.
"""

import csv
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QColor
from qgis.core import (
    QgsCoordinateReferenceSystem, QgsFeature, QgsField, QgsFillSymbol,
    QgsGeometry, QgsLineSymbol, QgsMarkerSymbol, QgsPointXY, QgsProject,
    QgsRasterLayer, QgsSingleSymbolRenderer, QgsVectorFileWriter,
    QgsVectorLayer,
)


# ---------------------------------------------------------------------------
# PARAMETROS
# ---------------------------------------------------------------------------
BASE = Path("/Volumes/T7/G3 Proyectos/INVESTIGACIÓN")
LAT, LON = 40.407576, -3.707172          # Ribera de Curtidores 31, aproximado
RADIO_M = 600                            # modificar si se necesita otro ambito
GPKG = BASE / "INVENTARIO_FISICO_600M.gpkg"
QGZ = BASE / "INVENTARIO_FISICO_600M.qgz"
CSV_POINTS = BASE / "COORDENADAS_PUNTOS_600M.csv"
CSV_LINES = BASE / "COORDENADAS_LINEAS_600M.csv"
CSV_POLYGONS = BASE / "COORDENADAS_POLIGONOS_600M.csv"
CRS_WGS84 = QgsCoordinateReferenceSystem("EPSG:4326")


# ---------------------------------------------------------------------------
# CONSULTA: CATEGORIAS FISICAS QUE SE PUEDEN MAPEAR AHORA
# ---------------------------------------------------------------------------
KEYS = [
    "building", "highway", "amenity", "shop", "craft", "office",
    "public_transport", "railway", "leisure", "natural", "landuse",
    "barrier", "entrance", "tourism", "historic", "man_made",
    "emergency", "addr:housenumber", "place", "power",
]

parts = []
for key in KEYS:
    if key == "place":
        parts.append('nwr(around:{},{},{})[place="square"];'.format(RADIO_M, LAT, LON))
    else:
        parts.append('nwr(around:{},{},{})["{}"];'.format(RADIO_M, LAT, LON, key))

QUERY = "[out:json][timeout:90];(" + "".join(parts) + ");out tags center geom;"
ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]


def download_osm():
    encoded = urllib.parse.urlencode({"data": QUERY}).encode("utf-8")
    last_error = None
    for endpoint in ENDPOINTS:
        try:
            request = urllib.request.Request(
                endpoint, data=encoded,
                headers={"User-Agent": "QGIS-G3-Urban-Research/1.0", "Accept": "application/json"},
            )
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            last_error = exc
    raise RuntimeError("No se pudo consultar Overpass: {}".format(last_error))


# ---------------------------------------------------------------------------
# CLASIFICACION. UN ELEMENTO PUEDE PERTENECER A VARIOS TEMAS.
# ---------------------------------------------------------------------------
def themes(tags):
    result = []
    highway = tags.get("highway", "")
    amenity = tags.get("amenity", "")

    if "building" in tags:
        result.append("EDIFICIOS")
    if highway:
        if highway in {"crossing", "steps", "elevator", "traffic_signals", "street_lamp"}:
            result.append("ACCESIBILIDAD_Y_CALLE")
        else:
            result.append("CALLES_Y_RECORRIDOS")
    if any(k in tags for k in ("public_transport", "railway")) or highway == "bus_stop":
        result.append("TRANSPORTE")
    if any(k in tags for k in ("shop", "craft", "office")):
        result.append("COMERCIO_Y_ACTIVIDAD")
    if amenity:
        if amenity in {"bench", "waste_basket", "drinking_water", "bicycle_parking",
                       "recycling", "waste_disposal", "toilets", "fountain"}:
            result.append("MOBILIARIO_Y_SERVICIOS_CALLE")
        else:
            result.append("EQUIPAMIENTOS_Y_LOCALES")
    if any(k in tags for k in ("leisure", "natural", "landuse")) or tags.get("place") == "square":
        result.append("ESPACIO_PUBLICO_Y_VERDE")
    if any(k in tags for k in ("entrance", "door")) or "wheelchair" in tags:
        result.append("ACCESOS_Y_UMBRALES")
    if "barrier" in tags:
        result.append("BARRERAS")
    if any(k in tags for k in ("historic", "tourism")):
        result.append("PATRIMONIO_Y_CULTURA")
    if any(k in tags for k in ("man_made", "emergency", "power")):
        result.append("INFRAESTRUCTURA")
    if "addr:housenumber" in tags:
        result.append("PORTALES_Y_DIRECCIONES")
    return result or ["OTROS_FISICOS"]


def subtype(tags):
    for key in (
        "building", "highway", "amenity", "shop", "craft", "office",
        "public_transport", "railway", "leisure", "natural", "landuse",
        "barrier", "entrance", "tourism", "historic", "man_made",
        "emergency", "place", "power",
    ):
        if key in tags:
            return "{}={}".format(key, tags[key])
    return "sin subtipo"


def display_name(tags):
    address = " ".join(filter(None, [tags.get("addr:street"), tags.get("addr:housenumber")]))
    return tags.get("name") or tags.get("brand") or address or subtype(tags)


def is_area(tags, coords):
    if len(coords) < 4 or coords[0] != coords[-1]:
        return False
    if tags.get("area") == "yes":
        return True
    return any(k in tags for k in ("building", "landuse", "leisure")) or (
        "natural" in tags and tags.get("natural") not in {"tree", "tree_row"}
    ) or tags.get("place") == "square"


def coord_string(coords):
    # Orden explicito longitud,latitud; la geometria de QGIS conserva todos los vertices.
    return ";".join("{:.7f},{:.7f}".format(float(p["lon"]), float(p["lat"])) for p in coords)


FIELDS = [
    QgsField("osm_id", QVariant.String),
    QgsField("osm_tipo", QVariant.String),
    QgsField("temas", QVariant.String),
    QgsField("subtipo", QVariant.String),
    QgsField("nombre", QVariant.String),
    QgsField("direccion", QVariant.String),
    QgsField("lon_centro", QVariant.Double),
    QgsField("lat_centro", QVariant.Double),
    QgsField("vertices", QVariant.Int),
    QgsField("coordenadas_lon_lat", QVariant.String),
    QgsField("precision", QVariant.String),
    QgsField("url_osm", QVariant.String),
    QgsField("tags_json", QVariant.String),
]


def memory_layer(kind, name):
    layer = QgsVectorLayer("{}?crs=EPSG:4326".format(kind), name, "memory")
    layer.dataProvider().addAttributes(FIELDS)
    layer.updateFields()
    return layer


points = memory_layer("Point", "Todos los puntos fisicos")
lines = memory_layer("LineString", "Todas las lineas fisicas")
polygons = memory_layer("Polygon", "Todos los poligonos fisicos")
providers = {"point": points.dataProvider(), "line": lines.dataProvider(), "polygon": polygons.dataProvider()}


def make_feature(layer, osm_id, osm_type, tags, geom, coords, precision="Geometria OSM"):
    feature = QgsFeature(layer.fields())
    feature.setGeometry(geom)
    centroid = geom.centroid().asPoint()
    address = " ".join(filter(None, [tags.get("addr:street"), tags.get("addr:housenumber")]))
    feature.setAttributes([
        str(osm_id), osm_type, " | ".join(themes(tags)), subtype(tags), display_name(tags),
        address, round(centroid.x(), 7), round(centroid.y(), 7), len(coords),
        coord_string(coords), precision,
        "https://www.openstreetmap.org/{}/{}".format(osm_type, str(osm_id).split("/")[-1]),
        json.dumps(tags, ensure_ascii=False, sort_keys=True),
    ])
    return feature


data = download_osm()
seen = set()
counts = {"point": 0, "line": 0, "polygon": 0}

for element in data.get("elements", []):
    key = (element.get("type"), element.get("id"))
    if key in seen:
        continue
    seen.add(key)
    tags = element.get("tags", {})
    osm_type = element.get("type", "")
    osm_id = element.get("id", "")

    if osm_type == "node" and "lon" in element and "lat" in element:
        coords = [{"lon": element["lon"], "lat": element["lat"]}]
        geom = QgsGeometry.fromPointXY(QgsPointXY(element["lon"], element["lat"]))
        providers["point"].addFeature(make_feature(points, osm_id, osm_type, tags, geom, coords))
        counts["point"] += 1
        continue

    coords = element.get("geometry", [])
    if osm_type == "way" and len(coords) >= 2:
        qpoints = [QgsPointXY(p["lon"], p["lat"]) for p in coords]
        if is_area(tags, coords):
            geom = QgsGeometry.fromPolygonXY([qpoints])
            providers["polygon"].addFeature(make_feature(polygons, osm_id, osm_type, tags, geom, coords))
            counts["polygon"] += 1
        else:
            geom = QgsGeometry.fromPolylineXY(qpoints)
            providers["line"].addFeature(make_feature(lines, osm_id, osm_type, tags, geom, coords))
            counts["line"] += 1
        continue

    # Las relaciones multipoligonales se reconstruyen con sus anillos exteriores.
    if osm_type == "relation":
        outer_rings = []
        all_relation_coords = []
        for member in element.get("members", []):
            ring_coords = member.get("geometry", [])
            if member.get("role") == "outer" and len(ring_coords) >= 4 and ring_coords[0] == ring_coords[-1]:
                outer_rings.append([QgsPointXY(p["lon"], p["lat"]) for p in ring_coords])
                all_relation_coords.extend(ring_coords)
        if outer_rings:
            geom = QgsGeometry.fromMultiPolygonXY([[ring] for ring in outer_rings])
            providers["polygon"].addFeature(make_feature(
                polygons, osm_id, osm_type, tags, geom, all_relation_coords, "Contorno exterior OSM"
            ))
            counts["polygon"] += 1
        elif element.get("center"):
            center = element["center"]
            coords = [{"lon": center["lon"], "lat": center["lat"]}]
            geom = QgsGeometry.fromPointXY(QgsPointXY(center["lon"], center["lat"]))
            providers["point"].addFeature(make_feature(
                points, osm_id, osm_type, tags, geom, coords, "Centro representativo de relacion OSM"
            ))
            counts["point"] += 1


# Puntos propios de la investigacion que deben permanecer visibles aunque OSM no los etiquete.
LOCAL_POINTS = [
    ("LOCAL_PARCELA", -3.707172, 40.407576, "Ribera de Curtidores 31", "EMPLAZAMIENTO", "Coordenada aproximada; verificar Catastro"),
    ("LOCAL_C001", -3.702550, 40.408090, "Corrala de Sombrerete", "PATRIMONIO_Y_CULTURA", "Centroide aproximado"),
    ("LOCAL_C002", -3.708099, 40.408835, "Centro Cultural La Corrala", "PATRIMONIO_Y_CULTURA", "Centroide aproximado"),
    ("LOCAL_C003", -3.704923, 40.408480, "Corrala Embajadores 46", "PATRIMONIO_Y_CULTURA", "Acceso aproximado"),
    ("LOCAL_C004", -3.708177, 40.409578, "Viviendas jovenes Vara de Rey 12", "EDIFICIOS", "Referencia aproximada"),
]
for local_id, lon, lat, name, theme, precision in LOCAL_POINTS:
    tags = {"name": name, "source": "investigacion G3", "local_theme": theme}
    coords = [{"lon": lon, "lat": lat}]
    geom = QgsGeometry.fromPointXY(QgsPointXY(lon, lat))
    feature = make_feature(points, local_id, "local", tags, geom, coords, precision)
    feature["temas"] = theme
    feature["subtipo"] = "referencia local"
    feature["url_osm"] = ""
    providers["point"].addFeature(feature)
    counts["point"] += 1

points.updateExtents(); lines.updateExtents(); polygons.updateExtents()


# ---------------------------------------------------------------------------
# GUARDADO EN GEOPACKAGE
# ---------------------------------------------------------------------------
def write_gpkg(layer, layer_name, first=False):
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = layer_name
    options.fileEncoding = "UTF-8"
    options.actionOnExistingFile = (
        QgsVectorFileWriter.CreateOrOverwriteFile if first
        else QgsVectorFileWriter.CreateOrOverwriteLayer
    )
    result = QgsVectorFileWriter.writeAsVectorFormatV3(
        layer, str(GPKG), QgsProject.instance().transformContext(), options
    )
    if result[0] != QgsVectorFileWriter.NoError:
        raise RuntimeError("Error al guardar {}: {}".format(layer_name, result))


write_gpkg(points, "puntos_fisicos", True)
write_gpkg(lines, "lineas_fisicas")
write_gpkg(polygons, "poligonos_fisicos")


# CSV: cada fila conserva centro, vertices y lista completa lon,lat.
def write_csv(layer, path):
    names = [f.name() for f in layer.fields()]
    with open(path, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(names + ["geometria_wkt"])
        for feat in layer.getFeatures():
            writer.writerow([feat[name] for name in names] + [feat.geometry().asWkt()])


write_csv(points, CSV_POINTS)
write_csv(lines, CSV_LINES)
write_csv(polygons, CSV_POLYGONS)


# ---------------------------------------------------------------------------
# PROYECTO QGIS Y CAPAS TEMATICAS
# ---------------------------------------------------------------------------
project = QgsProject.instance()
project.clear()
project.setCrs(QgsCoordinateReferenceSystem("EPSG:25830"))
root = project.layerTreeRoot()

osm = QgsRasterLayer(
    "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmin=0&zmax=19",
    "OpenStreetMap - base", "wms"
)
if osm.isValid():
    project.addMapLayer(osm, False)
    root.addLayer(osm)

base_group = root.addGroup("00_INVENTARIO_COMPLETO")
loaded = {}
for layer_name, title, geometry_kind in [
    ("puntos_fisicos", "Todos los puntos fisicos", "point"),
    ("lineas_fisicas", "Todas las lineas fisicas", "line"),
    ("poligonos_fisicos", "Todos los poligonos fisicos", "polygon"),
]:
    layer = QgsVectorLayer("{}|layername={}".format(GPKG, layer_name), title, "ogr")
    if geometry_kind == "point":
        layer.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple({
            "name": "circle", "color": "#dc2b1f", "size": "1.7", "outline_style": "no"
        })))
    elif geometry_kind == "line":
        layer.setRenderer(QgsSingleSymbolRenderer(QgsLineSymbol.createSimple({
            "color": "#555555", "width": "0.35"
        })))
    else:
        symbol = QgsFillSymbol.createSimple({
            "color": "#d8d8d8", "outline_color": "#777777", "outline_width": "0.15"
        })
        symbol.setOpacity(0.55)
        layer.setRenderer(QgsSingleSymbolRenderer(symbol))
    project.addMapLayer(layer, False)
    base_group.addLayer(layer)
    loaded[geometry_kind] = layer

theme_colors = {
    "EDIFICIOS": "#bdbdbd",
    "CALLES_Y_RECORRIDOS": "#343434",
    "TRANSPORTE": "#4d7190",
    "COMERCIO_Y_ACTIVIDAD": "#dc2b1f",
    "EQUIPAMIENTOS_Y_LOCALES": "#8856a7",
    "ESPACIO_PUBLICO_Y_VERDE": "#4d745d",
    "ACCESIBILIDAD_Y_CALLE": "#ef8a62",
    "ACCESOS_Y_UMBRALES": "#d95f0e",
    "MOBILIARIO_Y_SERVICIOS_CALLE": "#2b8cbe",
    "BARRERAS": "#111111",
    "PATRIMONIO_Y_CULTURA": "#a63603",
    "INFRAESTRUCTURA": "#737373",
    "PORTALES_Y_DIRECCIONES": "#756bb1",
    "EMPLAZAMIENTO": "#ff0000",
}

for theme, color in theme_colors.items():
    themed_group = root.addGroup(theme)
    for kind, source in loaded.items():
        layer = source.clone()
        layer.setName("{} - {}".format(theme, kind))
        layer.setSubsetString('"temas" LIKE \'%{}%\''.format(theme))
        if kind == "point":
            layer.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple({
                "name": "circle", "color": color, "size": "2.4", "outline_color": "white", "outline_width": "0.3"
            })))
        elif kind == "line":
            layer.setRenderer(QgsSingleSymbolRenderer(QgsLineSymbol.createSimple({"color": color, "width": "0.8"})))
        else:
            symbol = QgsFillSymbol.createSimple({"color": color, "outline_color": color, "outline_width": "0.25"})
            symbol.setOpacity(0.45)
            layer.setRenderer(QgsSingleSymbolRenderer(symbol))
        project.addMapLayer(layer, False)
        themed_group.addLayer(layer)
    themed_group.setItemVisibilityChecked(False)

project.setCustomVariables({
    "ambito": "600 m desde Ribera de Curtidores 31",
    "fecha_consulta_osm": data.get("osm3s", {}).get("timestamp_osm_base", "sin fecha"),
    "orden_coordenadas": "longitud, latitud - EPSG:4326",
    "limite": "Inventario OSM; comprobar en visita, Catastro y cartografia municipal",
})
project.write(str(QGZ))

iface.mapCanvas().setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:25830"))
iface.mapCanvas().setExtent(loaded["polygon"].extent())
iface.mapCanvas().refresh()

print("INVENTARIO TERMINADO")
print("Elementos unicos OSM consultados:", len(seen))
print("Puntos: {point} | Lineas: {line} | Poligonos: {polygon}".format(**counts))
print("Proyecto:", QGZ)
print("GeoPackage:", GPKG)
print("CSV de coordenadas:", CSV_POINTS, CSV_LINES, CSV_POLYGONS)
print("Orden de coordenadas: longitud, latitud; CRS EPSG:4326")

# IDs cortos + nombres visibles + leyenda + DXF con textos editables.
# Para solo actualizar etiquetas, ejecutar ETIQUETAS_Y_DXF_QGIS.py directamente:
# reutiliza el GeoPackage local y evita otra consulta a Overpass.
_script_etiquetas = BASE / "ETIQUETAS_Y_DXF_QGIS.py"
if not _script_etiquetas.exists():
    raise FileNotFoundError("Falta el módulo de etiquetas: " + str(_script_etiquetas))
exec(compile(_script_etiquetas.read_text(encoding="utf-8"), str(_script_etiquetas), "exec"),
     {"__name__": "__main__", "__file__": str(_script_etiquetas)})
