# G3 - Plantas corregidas y prueba de parcela

Revisión 19.10.2026. Carpeta nueva; las entregas anteriores se conservan.

## Leer

`output/pdf/G3_PLANTAS_CORREGIDAS_Y_PRUEBA_PARCELA.pdf`: 52 páginas A3 horizontales. Plantas y diagramas vigentes, comparación de uso, ocho ensayos de parcela y 18 antecedentes originales. Los antecedentes no son plantas vigentes ni una generación matemática exacta de las plantas.

## Editar

`modelos_2d/`: ocho plantas y ocho posiciones sobre la parcela en formato 3DM. Son curvas 2D editables, en metros y Z=0. No son modelos constructivos 3D y no se ha realizado una revisión nativa visual en Rhino. Los aparatos de baño son esquemáticos. No se sustituye ni se modifica el archivo de personas o el modelo previo.

`laminas/`: PNG y SVG de cada dibujo. `fuentes/`: scripts y geometría de partida.

## Cambios

- Servicios integrados en borde, sin islas sanitarias centrales, sin pantalla suelta y con paso corto y puertas laterales. Cada baño tiene 3,40 m² de polígono geométrico; las paredes reducen la dimensión interior. El paso nominal de 1,20 m deja unos 1,08 m libres entre muros.
- Mantiene habitación individual de 18,35 m² geométricos, vestidor transitable, bow curva pequeña, cama de 1,25 x 2,00 m y tablero de 1,80 x 0,90 m.
- V01 y V02 compactan el servicio. V03 desplaza dos dormitorios y reconstruye sus llegadas; la unión necesita más separación y reposicionar su mesa para ocho.
- Mantiene diferencias: continuidad / dos ámbitos / cruce central; umbral entre grupos / casa fusionada / encuentro ampliado.

## Control y límites

`verificacion/CONTROL_GEOMETRICO.json`: 52 aproximaciones privadas y 26 a baños conectadas con disco de 90 cm en ocho ensayos alternativos. Sin solapes entre dormitorios, muebles comunes o muros. Prueba privada con disco de 80 cm. No certifica accesibilidad normativa, evacuación, maniobras dentro del baño, estructura, acústica ni iluminación.

`verificacion/ENCAJE_PARCELA.json`: polígono de 650,91 m², escala 1:1. Seis contornos dentro en las posiciones obtenidas. Solo V01_U, V02_U y V01_D conservan llegada exterior de 90 cm desde el frente en estos ensayos. La búsqueda es heurística; un resultado negativo no prueba imposibilidad de cualquier otra posición.

Las bandas de 3 m delante de bow no son una simulación de luz. El contexto es catastral en planta, con alturas sin actualizar. Una bow orientada a una propiedad vecina no queda resuelta por encajar el contorno. No se apilan las posiciones ni se certifican como plantas edificables.

La cifra de 1.500 m² para 40 residentes es un objetivo provisional de estudio. Las cuentas excluyen aún núcleos, estructura e instalaciones generales.

## Continuidad del plan original

Investigación -> acciones y conflictos -> unidades -> agregación -> parcela y sección -> soporte, conexiones y fachada textil. V01_S sirve como referencia de compartir con menos suelo; V02 de graduación entre actividades. La siguiente decisión exige frentes abiertos, sección del entorno y entrada desde calle; no procede apilar automáticamente las siluetas.
