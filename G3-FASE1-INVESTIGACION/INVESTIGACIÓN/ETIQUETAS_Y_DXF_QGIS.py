# -*- coding: utf-8 -*-
"""Etiquetas y DXF del inventario existente. No descarga datos ni altera originales.
QGIS > Consola Python:
exec(open('/Volumes/T7/G3 Proyectos/INVESTIGACIÓN/ETIQUETAS_Y_DXF_QGIS.py', encoding='utf-8').read())
"""
import json
from pathlib import Path
from collections import Counter
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QColor, QFont
from qgis.core import (
    QgsApplication, QgsProject, QgsVectorLayer, QgsVectorFileWriter,
    QgsField, QgsFeature, QgsGeometry, QgsWkbTypes, QgsCoordinateReferenceSystem,
    QgsCoordinateTransform, QgsRectangle, QgsPointXY, QgsReferencedRectangle,
    QgsPalLayerSettings, QgsTextFormat, QgsTextBufferSettings,
    QgsVectorLayerSimpleLabeling, QgsCategorizedSymbolRenderer,
    QgsRendererCategory, QgsSymbol, QgsMapSettings, QgsMapRendererParallelJob,
)

BASE = Path('/Volumes/T7/G3 Proyectos/INVESTIGACIÓN')
SALIDA = BASE / 'QGIS_ETIQUETADO'
# Cambiar a 'id_mapa' para mostrar solo los IDs. El DXF siempre incluye ID + nombre.
CAMPO_ETIQUETA = 'etiqueta'
EXPORTAR_DXF = True

# Clave original, prefijo, título y color de leyenda. La categoría principal es
# exclusiva para no duplicar objetos. El campo original "temas" se conserva.
CATEGORIAS = [
 ('EMPLAZAMIENTO','EMP','Emplazamiento','#d7191c'),
 ('PATRIMONIO_Y_CULTURA','PAT','Patrimonio y cultura','#a63603'),
 ('TRANSPORTE','TRA','Transporte','#376b91'),
 ('COMERCIO_Y_ACTIVIDAD','COM','Comercio y actividad','#ce3b37'),
 ('MOBILIARIO_Y_SERVICIOS_CALLE','MOB','Mobiliario y servicios de calle','#268c9e'),
 ('ACCESIBILIDAD_Y_CALLE','ACC','Accesibilidad y elementos de calle','#e68241'),
 ('ACCESOS_Y_UMBRALES','UMB','Accesos y umbrales','#9e6a39'),
 ('BARRERAS','BAR','Barreras','#333333'),
 ('INFRAESTRUCTURA','INF','Infraestructura','#777777'),
 ('EQUIPAMIENTOS_Y_LOCALES','EQU','Equipamientos y locales','#8e5aa4'),
 ('EDIFICIOS','EDI','Edificios','#a4a4a4'),
 ('ESPACIO_PUBLICO_Y_VERDE','VER','Espacio público y verde','#4d745d'),
 ('CALLES_Y_RECORRIDOS','VIA','Calles y recorridos','#555555'),
 ('PORTALES_Y_DIRECCIONES','DIR','Portales y direcciones','#756bb1'),
 ('OTROS_FISICOS','OTR','Otros elementos físicos','#999999'),
]
TRADUCCION = {
 'natural=tree':'Árbol', 'natural=tree_row':'Alineación de árboles',
 'amenity=bench':'Banco', 'amenity=waste_basket':'Papelera',
 'amenity=drinking_water':'Fuente de agua potable', 'amenity=fountain':'Fuente',
 'amenity=bicycle_parking':'Aparcabicicletas', 'amenity=recycling':'Reciclaje',
 'amenity=parking':'Aparcamiento', 'amenity=toilets':'Aseos',
 'highway=street_lamp':'Farola', 'highway=crossing':'Paso peatonal',
 'highway=traffic_signals':'Semáforo', 'highway=bus_stop':'Parada de autobús',
 'highway=steps':'Escaleras', 'highway=footway':'Vía peatonal',
 'highway=pedestrian':'Calle peatonal', 'highway=residential':'Calle residencial',
 'building=yes':'Edificio', 'building=apartments':'Edificio de viviendas',
 'entrance=yes':'Acceso', 'entrance=main':'Acceso principal',
 'barrier=bollard':'Bolardo', 'barrier=fence':'Valla', 'barrier=wall':'Muro',
 'barrier=gate':'Puerta de recinto', 'emergency=fire_hydrant':'Hidrante',
}

def texto(v):
    return '' if v is None or str(v) in ('NULL','None') else str(v).strip()

def estilo(layer):
    present = set(texto(f['cat_codigo']) for f in layer.getFeatures())
    cats=[]
    for _, code, title, color in CATEGORIAS:
        if code not in present: continue
        sym=QgsSymbol.defaultSymbol(layer.geometryType()); sym.setColor(QColor(color))
        if layer.geometryType()==QgsWkbTypes.PointGeometry: sym.setSize(1.8)
        elif layer.geometryType()==QgsWkbTypes.LineGeometry: sym.setWidth(.3)
        else: sym.setOpacity(.35)
        cats.append(QgsRendererCategory(code,sym,code+' · '+title))
    layer.setRenderer(QgsCategorizedSymbolRenderer('cat_codigo',cats))
    fmt=QgsTextFormat(); fmt.setFont(QFont('Arial')); fmt.setSize(7.5)
    fmt.setColor(QColor('#111111'))
    buf=QgsTextBufferSettings(); buf.setEnabled(True); buf.setSize(.7)
    buf.setColor(QColor('white')); fmt.setBuffer(buf)
    pal=QgsPalLayerSettings(); pal.fieldName=CAMPO_ETIQUETA; pal.setFormat(fmt)
    if layer.geometryType()==QgsWkbTypes.PointGeometry:
        pal.placement=QgsPalLayerSettings.OrderedPositionsAroundPoint; pal.dist=1.5; pal.priority=10
    elif layer.geometryType()==QgsWkbTypes.LineGeometry:
        pal.placement=QgsPalLayerSettings.Line; pal.priority=4
    else: pal.placement=QgsPalLayerSettings.Horizontal; pal.priority=3
    pal.displayAll=False  # Pantalla legible: al acercar aparecen más etiquetas.
    layer.setLabeling(QgsVectorLayerSimpleLabeling(pal)); layer.setLabelsEnabled(True)
    layer.setDisplayExpression('"etiqueta"')
    layer.setMapTipTemplate('[% "etiqueta" %]<br>[% "categoria" %]<br>OSM: [% "osm_tipo" %]/[% "osm_id" %]')

def ancla(g):
    if g.type()==QgsWkbTypes.PointGeometry:
        return g.asMultiPoint()[0] if g.isMultipart() else g.asPoint()
    if g.type()==QgsWkbTypes.LineGeometry:
        parts=g.asGeometryCollection() if g.isMultipart() else [g]
        longest=max(parts,key=lambda x:x.length())
        a=longest.interpolate(longest.length()/2)
    else: a=g.pointOnSurface()
    if a.isEmpty(): a=g.centroid()
    if a.isEmpty(): raise RuntimeError('No se puede ubicar una etiqueta en geometría vacía')
    return a.asPoint()

def exportar_dxf(layers, path, project):
    """DXF 2004 CP1252: geometrías + un TEXT por objeto, sin filtro de colisiones.
    Unidades metros, EPSG:25830. Capas G_* = geometría, T_* = textos.
    No depende de fuentes SHX, plugins ni del motor de etiquetas del visor.
    """
    records=[]; extent=QgsRectangle()
    for layer in layers:
        tr=QgsCoordinateTransform(layer.crs(),QgsCoordinateReferenceSystem('EPSG:25830'),project)
        for f in layer.getFeatures():
            g=QgsGeometry(f.geometry())
            if g.isEmpty(): raise RuntimeError('Geometría vacía: '+f['id_mapa'])
            g.transform(tr); extent.combineExtentWith(g.boundingBox())
            records.append((f,g,ancla(g)))
    def ascii_dxf(s):
        s=str(s).replace('\n',' ').replace('\r',' ').replace('\\','/')
        return s
    # CP1252 conserva todos los nombres del inventario y evita mojibake en
    # versiones antiguas de GDAL/CAD. Fallar explícitamente si aparecen otros alfabetos.
    for f,g,a in records: f['etiqueta'].encode('cp1252')
    with open(path,'w',encoding='cp1252',newline='\n') as h:
        def pair(code,value): h.write(str(code)+'\n'+ascii_dxf(value)+'\n')
        # Strings with Unicode escape sequences must retain their backslashes.
        def rawtext(code,value): h.write(str(code)+'\n'+value+'\n')
        pair(0,'SECTION');pair(2,'HEADER')
        for var,code,val in [('$ACADVER',1,'AC1018'),('$DWGCODEPAGE',3,'ANSI_1252'),('$INSUNITS',70,6),('$MEASUREMENT',70,1)]: pair(9,var);pair(code,val)
        pair(0,'ENDSEC');pair(0,'SECTION');pair(2,'TABLES')
        pair(0,'TABLE');pair(2,'LTYPE');pair(70,1)
        pair(0,'LTYPE');pair(2,'CONTINUOUS');pair(70,0);pair(3,'Solid line');pair(72,65);pair(73,0);pair(40,0);pair(0,'ENDTAB')
        layercolors={'0':'#ffffff','LEYENDA':'#111111'}
        for f,g,a in records:
            color=next(c[3] for c in CATEGORIAS if c[1]==f['cat_codigo'])
            key=f['id_mapa'][0]+'_'+f['cat_codigo']
            layercolors['G_'+key]=color;layercolors['T_'+key]=color
        pair(0,'TABLE');pair(2,'LAYER');pair(70,len(layercolors))
        for name,color in sorted(layercolors.items()):
            pair(0,'LAYER');pair(2,name);pair(70,0);pair(62,7);pair(420,int(color[1:],16));pair(6,'CONTINUOUS')
        pair(0,'ENDTAB');pair(0,'ENDSEC');pair(0,'SECTION');pair(2,'ENTITIES')
        def point(p,layer):
            pair(0,'POINT');pair(100,'AcDbEntity');pair(8,layer);pair(100,'AcDbPoint')
            pair(10,p.x());pair(20,p.y());pair(30,0)
        def polyline(pts,layer,closed=False):
            if closed and len(pts)>1 and pts[0]==pts[-1]: pts=pts[:-1]
            pair(0,'LWPOLYLINE');pair(100,'AcDbEntity');pair(8,layer);pair(100,'AcDbPolyline')
            pair(90,len(pts));pair(70,1 if closed else 0)
            for p in pts: pair(10,p.x());pair(20,p.y())
        def label(value,x,y,layer,height=1.5):
            pair(0,'TEXT');pair(100,'AcDbEntity');pair(8,layer);pair(100,'AcDbText')
            pair(10,x);pair(20,y);pair(30,0);pair(40,height)
            rawtext(1,ascii_dxf(value));pair(50,0);pair(100,'AcDbText')
        for f,g,a in records:
            key=f['id_mapa'][0]+'_'+f['cat_codigo']; gl='G_'+key
            if g.type()==QgsWkbTypes.PointGeometry:
                for p in (g.asMultiPoint() if g.isMultipart() else [g.asPoint()]): point(p,gl)
            elif g.type()==QgsWkbTypes.LineGeometry:
                for pts in (g.asMultiPolyline() if g.isMultipart() else [g.asPolyline()]): polyline(pts,gl)
            else:
                for polygon in (g.asMultiPolygon() if g.isMultipart() else [g.asPolygon()]):
                    for ring in polygon: polyline(ring,gl,True)
            label(f['etiqueta'],a.x()+2,a.y()+2,'T_'+key)
        x=extent.xMaximum()+30;y=extent.yMaximum()
        legend=['LEYENDA | EPSG:25830 | metros','P = punto; L = linea; A = area/poligono',
                'G_* geometria; T_* ID + nombre (TEXT editable)',
                'IDs estables: ver registro_ids.json. No son IDs OSM.',
                'Texto completo: puede solaparse; mover en CAD.']
        counts=Counter(f['cat_codigo'] for f,g,a in records)
        legend += [code+' - '+title+' ('+str(counts[code])+')' for _,code,title,_ in CATEGORIAS if counts[code]]
        for i,t in enumerate(legend): label(t,x,y-i*5,'LEYENDA',2)
        pair(0,'ENDSEC');pair(0,'EOF')
    return len(records)

def ejecutar():
    SALIDA.mkdir(exist_ok=True)
    source=BASE/'INVENTARIO_FISICO_600M.gpkg'
    if not source.exists(): raise FileNotFoundError('Primero debe existir '+str(source))
    gpkg=SALIDA/'INVENTARIO_ETIQUETADO.gpkg'
    # Proyecto independiente: no limpiar ni guardar encima del proyecto del usuario.
    project=QgsProject();project.setCrs(QgsCoordinateReferenceSystem('EPSG:25830'))
    registry_path=SALIDA/'registro_ids.json'
    registry=json.loads(registry_path.read_text()) if registry_path.exists() else {}
    layers=[]; summary=Counter(); ids=set()
    for table,prefix,title in [('puntos_fisicos','P','P · Puntos físicos'),('lineas_fisicas','L','L · Líneas físicas'),('poligonos_fisicos','A','A · Polígonos físicos')]:
        src=QgsVectorLayer(str(source)+'|layername='+table,title,'ogr')
        if not src.isValid(): raise RuntimeError('Capa no válida: '+table)
        memory=src.materialize(__import__('qgis.core',fromlist=['QgsFeatureRequest']).QgsFeatureRequest())
        newfields=['id_mapa','nombre_mapa','cat_codigo','categoria','etiqueta','capa_dxf']
        memory.dataProvider().addAttributes([QgsField(n,QVariant.String) for n in newfields]);memory.updateFields()
        next_id=max([int(v[1:]) for v in registry.values() if v.startswith(prefix)]+[0])+1
        changes={}
        features=sorted(memory.getFeatures(),key=lambda f:(texto(f['osm_tipo']),texto(f['osm_id'])))
        for f in features:
            key=prefix+'|'+texto(f['osm_tipo'])+'|'+texto(f['osm_id'])
            if key not in registry: registry[key]=prefix+str(next_id).zfill(5);next_id+=1
            ident=registry[key]
            if ident in ids: raise RuntimeError('ID duplicado: '+ident)
            ids.add(ident)
            themes=set(texto(f['temas']).split(' | '))
            cat=next((c for c in CATEGORIAS if c[0] in themes),CATEGORIAS[-1])
            name=texto(f['nombre']); subtype=texto(f['subtipo'])
            if not name or name==subtype:
                name=TRADUCCION.get(subtype,subtype or 'Elemento sin nombre registrado')
            # Comillas rectas para interoperabilidad CAD; el nombre original no cambia.
            name=name.translate(str.maketrans({'“':'"','”':'"','‘':"'",'’':"'"}))
            values=[ident,name,cat[1],cat[2],ident+' · '+name,prefix+'_'+cat[1]]
            changes[f.id()]={memory.fields().indexFromName(n):v for n,v in zip(newfields,values)}
            summary[(prefix,cat[1])]+=1
        if not memory.dataProvider().changeAttributeValues(changes): raise RuntimeError('No se pudieron guardar los nombres')
        opts=QgsVectorFileWriter.SaveVectorOptions();opts.driverName='GPKG';opts.layerName=table
        opts.actionOnExistingFile=QgsVectorFileWriter.CreateOrOverwriteLayer if gpkg.exists() else QgsVectorFileWriter.CreateOrOverwriteFile
        result=QgsVectorFileWriter.writeAsVectorFormatV3(memory,str(gpkg),project.transformContext(),opts)
        if result[0]!=QgsVectorFileWriter.NoError: raise RuntimeError(str(result))
        layer=QgsVectorLayer(str(gpkg)+'|layername='+table,title,'ogr');estilo(layer)
        layer.saveNamedStyle(str(SALIDA/(table+'.qml')))
        project.addMapLayer(layer);layers.append(layer)
    registry_path.write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')
    project.layerTreeRoot().setHasCustomLayerOrder(True)
    project.layerTreeRoot().setCustomLayerOrder(layers)  # puntos sobre líneas y polígonos
    tr=QgsCoordinateTransform(QgsCoordinateReferenceSystem('EPSG:4326'),project.crs(),project)
    center=tr.transform(QgsPointXY(-3.707172,40.407576))
    extent=QgsRectangle(center.x()-650,center.y()-650,center.x()+650,center.y()+650)
    project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(extent,project.crs()))
    project.setTitle('Inventario físico · IDs, nombres y leyenda')
    target=SALIDA/'INVENTARIO_ETIQUETADO.qgz'
    if not project.write(str(target)): raise RuntimeError('No se pudo guardar el proyecto')
    md=['# Leyenda del inventario físico','',
        'P = punto; L = línea; A = área/polígono. El ID corto no sustituye el ID OSM.',
        'Los nombres provienen del inventario. Si no hay nombre propio se muestra una descripción del tipo; no se inventan nombres.',
        'Se conserva exactamente la geometría del inventario previo, sin nuevo recorte ni nueva comprobación de campo.',
        'La clasificación principal sirve para dibujar sin duplicados. Todas las categorías originales siguen en `temas`.','',
        '| Código | Categoría | Puntos | Líneas | Polígonos |','|---|---|---:|---:|---:|']
    for _,code,title,color in CATEGORIAS:
        md.append('| {} | {} | {} | {} | {} |'.format(code,title,summary['P',code],summary['L',code],summary['A',code]))
    md += ['', '## Etiquetas y DXF','',
        'El mapa muestra `etiqueta` = ID + nombre. QGIS oculta colisiones para mantener la lectura: acercar el zoom, filtrar una categoría o usar `id_mapa` como campo de etiqueta.',
        'El DXF automático conserva TODOS los textos (uno por objeto), aunque se solapen. Son entidades TEXT editables, no atributos ocultos ni contornos de letras. No se truncan nombres.',
        'DXF: metros, EPSG:25830, plano Z=0. G_P_* / G_L_* / G_A_* = geometrías; T_P_* / T_L_* / T_A_* = textos. LEYENDA queda a la derecha del dibujo.',
        'No usar el DXF como levantamiento topográfico: conserva la precisión y limitaciones del inventario OSM/local.',
        'Para otra exportación manual desde QGIS: Proyecto > Importar/Exportar > Exportar proyecto a DXF, seleccionar las tres capas etiquetadas, CRS EPSG:25830 y escala adecuada (p. ej. 1:1000). Las etiquetas se exportan como TEXT/MTEXT. Guardar una capa como DXF no equivale a exportar las etiquetas del proyecto.',
        'La exportación manual puede omitir etiquetas por colisión; el DXF generado por este script no las omite.',
        'Documentación: https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/qgis/vectorgeneral.html#export-layers-to-dxf',
        '', '## Repetir sin descargar','',
        'Ejecutar ETIQUETAS_Y_DXF_QGIS.py. Se regeneran SOLO los archivos de QGIS_ETIQUETADO; no se modifican el inventario original ni el catálogo.',
        'Conservar registro_ids.json: mantiene los IDs de cada objeto al repetir y añade nuevos sin reutilizar identificadores.',
        'El proyecto nuevo se guarda aparte. No se cierra ni sobrescribe el proyecto abierto. Abrir INVENTARIO_ETIQUETADO.qgz para verlo.']
    (SALIDA/'LEYENDA_Y_USO.md').write_text('\n'.join(md),encoding='utf-8')
    if EXPORTAR_DXF:
        n=exportar_dxf(layers,SALIDA/'INVENTARIO_CON_NOMBRES.dxf',project)
        print('DXF: {} objetos con {} textos ID + nombre'.format(n,n))
    print('Proyecto:',target)
    print('Leyenda:',SALIDA/'LEYENDA_Y_USO.md')
    return project,layers

if QgsApplication.instance() is None:
    _qgis_app=QgsApplication([],False);_qgis_app.initQgis()
_proyecto_etiquetado,_capas_etiquetadas=ejecutar()
