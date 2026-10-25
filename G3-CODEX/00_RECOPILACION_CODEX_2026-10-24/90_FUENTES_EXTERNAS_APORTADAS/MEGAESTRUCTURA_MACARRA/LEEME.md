# MEGAESTRUCTURA MACARRA

Una sola arquitectura de conexiones: dos recorridos trenzados ascienden y se cruzan entre 28 estancias. Los enlaces se ensanchan en plazas, descansillos y galerías cubiertas. Se mezclan las tres imágenes de referencia: esqueleto poroso, nervios magenta, bordes amarillos, agua suspendida y velas verdes. Sin personas.

## Abrir y editar

Abrir `modelo/MEGAESTRUCTURA_MACARRA.3dm` en Rhino 8. Unidades: metros. El archivo se ha abierto y revisado en Rhino 8.

23 capas: 21 sistemas visibles y 2 capas de curvas auxiliares inicialmente ocultas. Las mallas están separadas por sistema y estancia; los nombres de objeto identifican su procedencia. No es un único bloque fusionado. La geometría principal es de malla, no NURBS. Para trabajar con una pieza individual dentro de una malla se pueden separar sus componentes desconectados con SplitDisjointMesh.

Vistas guardadas: 01_AXONOMETRIA, 02_REVERSO, 03_PLANTA, 04_ALZADO y 05_INTERIOR. Cambiar entre ellas desde Vistas guardadas. Sombreado o Renderizado permiten leer materiales y membranas; Alámbrico muestra toda la trama.

## Anatomía

- Marfil: troncos ramificados, costillas, células perforadas, tensores y barandillas.
- Amarillo: perímetros estructurales y escaleras con peldaños reales.
- Magenta: haces de conducción y órganos táctiles; líneas inventadas de energía y señal.
- Verde translúcido: velas y galerías de conexión.
- Cian: circuitos hidráulicos, depósitos suspendidos, estanques y ondas.
- Cobre y gris: bridas, válvulas, máquinas, articulaciones y anclajes.

28 estancias, 36 conexiones, 903 peldaños, 12 descansillos habitados y 21 galerías cubiertas. El grafo de recorridos alcanza las 28 estancias. Los extremos de los enlaces entran en las plataformas y sus barandillas dejan pasos.

La precisión corresponde a la geometría y a la continuidad definida de los recorridos. Es una exploración de arquitectura fantástica: los sistemas y usos son inventados; no incorpora cálculo estructural, verificación integral de interferencias ni comprobación normativa de habitabilidad.

## Archivos

- `modelo/MEGAESTRUCTURA_MACARRA.3dm`: modelo principal editable.
- `vistas/`: cinco imágenes de la misma geometría, a 2800 × 2100 px.
- `fuentes/generar_megaestructura.py`: generador reproducible, semilla 11873. Requiere Python, numpy y rhino3dm.
- `fuentes/renderizar_modelo.py`: render de esa geometría con bpy; ejecutar después del generador. Requiere bpy 4.4 y numpy 1.26.
- `verificacion.json`: espacios, conexiones y datos geométricos.
- `auditoria_archivo.json`: comprobación independiente del .3dm reabierto.

La carpeta de trabajo contiene además el .blend y la caché de geometría para reproducir las vistas. El ZIP de entrega reúne Rhino, vistas, fuentes y documentación.

## Índice espacial

00 · UMBRAL DE CONTRABANDO · cota 2.0 m
01 · PLAZA DE LOS NERVIOS · cota 5.2 m
02 · TALLER DEL RESIDUO · cota 8.7 m
03 · FORO DESDOBLADO · cota 12.0 m
04 · ESTANCIA DE AGUA · cota 15.1 m
05 · MIRADOR ROTO · cota 18.7 m
06 · BAÑERA SUSPENDIDA · cota 22.0 m
07 · JARDÍN ELECTROMECÁNICO · cota 25.2 m
08 · BIBLIOTECA DE RUIDOS · cota 28.9 m
09 · BALCÓN DE LA RAÍZ · cota 32.1 m
10 · INVERNADERO IMPOSIBLE · cota 35.7 m
11 · TEATRO DE HILOS · cota 39.1 m
12 · CÁMARA DE LLUVIA · cota 42.6 m
13 · CUEVA COMÚN · cota 9.0 m
14 · COCINA DEL MICELIO · cota 12.4 m
15 · CRUCE HABITADO · cota 15.8 m
16 · FÁBRICA DE VIBRACIÓN · cota 18.6 m
17 · DEPÓSITO MUTANTE · cota 22.1 m
18 · SALA DE REPOSO · cota 25.5 m
19 · HABITACIÓN COLGADA · cota 29.1 m
20 · ARCHIVO DE PIELES · cota 32.4 m
21 · CAPILLA DEL CABLE · cota 36.0 m
22 · SALA DE GLISSANDI · cota 39.4 m
23 · PLAZA FISURADA · cota 42.9 m
24 · TORRE DE CONTACTO · cota 46.2 m
25 · FARO DESOBEDIENTE · cota 49.6 m
26 · NIDO ALTO · cota 49.4 m
27 · OBSERVATORIO POROSO · cota 46.2 m
