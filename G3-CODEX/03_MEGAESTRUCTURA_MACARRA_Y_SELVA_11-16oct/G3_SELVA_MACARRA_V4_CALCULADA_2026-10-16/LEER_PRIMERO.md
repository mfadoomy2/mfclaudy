# SELVA MACARRA V4 — abrir aquí

16 octubre 2026. Propuesta arquitectónica editable y predimensionado de anteproyecto.

## Archivos

- `modelos/SELVA_MACARRA_V4_FINAL.3dm`: conjunto en metros. Diez pabellones, cuarenta residentes, tres grupos de árboles, tres ascensores y dos escaleras de extremo.
- `modelos/UNIDAD_GRAN_BOVEDA_EDITABLE.3dm`: un pabellón independiente, con superficies y sólidos editables, cuatro habitaciones y programa de grupo.
- `modelos/D01_NUDO_RAMIFICADO_1a1.3dm`: brida, tubos huecos, cartelas y pernos.
- `modelos/D02_ENVOLVENTE_Y_BANDEJA_1a1.3dm`: ensamblaje estratificado de cubierta, suelo y desagüe.
- `modelos/D03_ASCENSOR_COMPLETO.3dm`: ascensor separado con cabina, guías, contrapeso, máquina, foso y rellanos.
- `MEMORIA_TECNICA_Y_RAZON_DE_LA_FORMA.md`: hipótesis, cálculo, resultados, fuentes oficiales y límites.
- `GUION_DE_DEFENSA.md`: explicación oral del espacio, las reglas y el funcionamiento colectivo.
- `calculo/*.json`: datos completos y resultados reproducibles.
- `vistas/01…04`: renders de la triangulación del CAD, sin reinterpretación mediante IA. `05…07`: diagramas del cálculo y de las cotas.

## Visualización

La instalación actual de Rhino está mostrando los Breps por sus aristas incluso en modo sombreado. Las superficies son válidas y los renders se generan desde su triangulación. Se incluye `modelos/PREVIA_SOLIDA_MALLAS.3dm` como copia de visualización de esa misma geometría; no sustituye al archivo Brep editable. `08_RHINO_NATIVO.png` registra ese problema gráfico, no es una vista sólida final.

## Cómo editar

Los pabellones se repiten mediante un bloque. Usar BlockEdit para cambiar los diez, o editar el archivo de unidad independiente. Las figuras humanas son bloques de mallas extraídas de PERSONAS.3dm; no son sólidos paramétricos. La arquitectura utiliza principalmente Breps/NURBS. El contexto de vecinos está en `90_CONTEXTO`, oculto para leer el proyecto; encender esa capa para contrastar su relación con el entorno.

Las vistas guardadas incluyen axonometría, frente, árbol, ascensor y planta. Las secciones de tubos proceden del modelo de barras, no de un espesor visual arbitrario. El modelo tiene tolerancia de 1 mm, lo cual no equivale a exactitud de replanteo ni de fabricación.

## Estado real

Hay comprobaciones elásticas lineales de barras, viguetas, arco, pernos de referencia, cable, lluvia y transmitancia de un componente. No se ha certificado seguridad estructural ni cumplimiento integral de CTE. Faltan, entre otros, estabilidad global/segundo orden, cimentación con geotecnia, viento local y membranas, uniones completas, fuego y evacuación, accesibilidad y habitabilidad. Las piezas de cimentación son reservas geométricas.

Las habitaciones actuales rondan 8 m² útiles, por lo que esta versión formal requiere revisión de habitabilidad. La superficie total respecto al objetivo aproximado de 1.500 m² debe contrastarse con los criterios de cómputo del enunciado; no se declaran exentas automáticamente galerías ni terrazas.

No se han modificado los originales MEGAESTRUCTURA_MACARRA.3dm ni PERSONAS.3dm. Las versiones anteriores rechazadas se conservan fuera de esta entrega. La selección de figuras y las fuentes permiten identificar qué se reutiliza y qué se propone.

## Reproducir

`calcular_estructura.py` y `calcular_subsistemas.py` usan Python, NumPy y SciPy. `documentar_calculos.py` usa además Matplotlib. `modelar_v4_rhino.py`, `modelar_detalles.py` y `finalizar_modelos.py` se ejecutan dentro de Rhino 8 con RhinoCommon; escriben archivos nuevos. Los scripts conservan rutas absolutas del proyecto y requieren adaptarlas si se cambia de carpeta. `renderizar_v4.py` usa bpy 4.4 y NumPy 1.26; carga la triangulación exacta guardada en JSON. La parcela y el contexto reutilizados de V2/V3 se incluyen en fuentes, junto con el enunciado y la procedencia de las personas.

## Implantación con contexto

`modelos/SELVA_MACARRA_V4_EN_PARCELA.3dm` conserva escala y posición del conjunto y activa los cuatro objetos del contexto suministrado. Añade el límite magenta y las vistas guardadas 09_IMPLANTACION_CONTEXTO y 10_PARCELA_CENITAL. Las imágenes 09 y 10 muestran la implantación sin retirar vecinos para despejar artificialmente el proyecto. Esta copia posterior se entrega por separado del ZIP inicial.
