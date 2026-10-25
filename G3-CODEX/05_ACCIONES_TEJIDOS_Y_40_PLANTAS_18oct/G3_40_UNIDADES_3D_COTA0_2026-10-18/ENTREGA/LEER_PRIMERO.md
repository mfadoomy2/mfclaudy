# G3 · 40 unidades modeladas en Rhino · Suelo a cota 0

## Abrir

**CATALOGO_40_UNIDADES_COTA0.3dm** contiene las cuarenta alternativas separadas en una retícula de 60 m en XY, todas con el suelo terminado a Z=0. Es un catálogo para comparar modelos; no es una implantación en parcela ni un complejo construido. Las capas principales son N01A–N20B. Las vistas nombradas permiten acercarse a cada alternativa y ver el conjunto.

`modelos/` contiene los 40 archivos individuales. `habitaciones/` contiene dos habitaciones aisladas, con colchón circular y rectangular. `vistas/` contiene capturas reales de Rhino y contactos de las cuarenta unidades.

No se han apilado viviendas ni introducido desniveles. El espesor de forjado queda por debajo del suelo acabado: -0,22 a 0 m. Las alturas de muebles, paredes y cubierta corresponden a su posición de uso.

## Qué está modelado

- Cuatro habitaciones privadas por alternativa: base de 4,20 × 4,40 m, concavidad de armario y bahía exterior de ventana. El tamaño de la base no incluye esas extensiones.
- A: colchón circular Ø2,10 m. B: colchón rectangular 1,25 × 2,00 m. Apoyo de 55 mm con la misma huella del colchón, colchón de 205 mm y almohada apoyada.
- Mesa de dibujo de 1,80 × 0,90 m, inclinada 12°, bisagra por el canto corto, pletinas, puntales y rótulas. No tiene patas permanentes. Taburete apoyado. El mecanismo y sus cargas no están calculados.
- Armario curvo con zócalo, divisiones, coronación, barra y suspensiones. Hay paso interior en la concavidad; no se modelan prendas.
- Ventana con bahía real, cajón de asiento, cojín, vidrio, marco, carril, ménsulas y tejido exterior plegado.
- Dos slabs metálicos de noche y toma propuesta de carga.
- Puertas correderas abiertas, guías y carros, sin barrido de hoja atravesando el paso.
- Cocina con muebles, apoyos regulables, encimera perforada, fregadero, grifería, placa, horno y frigorífico; reconstrucción genérica, no importación del archivo de 3D Warehouse.
- Dos baños equipados: ducha enrasada, mampara, rociador, WC, lavabo compacto de 500 × 400 mm y corredera de dos hojas. No se han creado peldaños en los baños.
- Mesa común, taburetes, sofá con bastidor y patas, mesa de trabajo, almacenaje, bicicleta esquemática y tendedero.
- Forjado continuo extendido bajo los muros, cerramientos, huecos reales y cubierta.

Las conexiones se han redondeado y ensanchado en puntos conflictivos. Se han desplazado seis habitaciones para que las bahías de ventana no invadan la aproximación de otra puerta. La correspondencia con las plantas del atlas se mantiene por código; estas correcciones hacen que el modelo no sea una extrusión idéntica de aquellas plantas.

## Capas de inspección

La cubierta está en `91_CUBIERTA_OCULTA`, a su altura construida de 3 m, y apagada para ver dentro. No está desplazada ni explotada por encima de la vivienda.

`90_ESTADO_MESAS_PLEGADAS_OCULTO` es una reserva visual del tablero plegado. No debe mostrarse simultáneamente con el tablero abierto. No es una simulación cinemática completa del herraje. El estado por defecto muestra tablero abierto y apoyos.

Materiales y colores diferencian cal, madera, corcho, metal, vidrio y textil. Las capturas son vistas de Rhino, no imágenes generadas por IA ni renders que sustituyan la geometría.

## Comprobaciones y límites reales

Se han revisado en Rhino los cuarenta modelos y sus sólidos. La revisión de volúmenes contrasta los perfiles con huecos contra el área de sus polígonos por su altura. Este control permitió detectar y corregir un desplazamiento de los perfiles interiores que no aparecía como geometría inválida.

La auditoría espacial comprueba las conexiones entre las cuatro entradas interiores con un cuerpo circular de 0,90 m, y entre cinco aproximaciones de uso dentro de las habitaciones con un cuerpo de 0,80 m. Incluye cama, escritorio, ropa, taburetes, asiento de ventana y hojas abiertas. Comprueba además una zona de entrada de 1,40 m de diámetro libre de esos muebles. Los datos están en `verificacion/AUDITORIA_FINAL_ESPACIO.json`.

Son pruebas geométricas parciales. **No acreditan accesibilidad reglamentaria, evacuación, funcionamiento de todas las maniobras, cargas de herrajes, estabilidad, acústica, instalaciones ni iluminación suficiente.** El forjado de 220 mm y los muros de 120 mm son hipótesis dimensionales sin cálculo estructural.

**El exceso de superficie no está resuelto.** El modelado y la corrección de pasos amplían el suelo útil conceptual hasta aproximadamente 258–326 m² por unidad. No se presenta como tamaño adecuado para repetir diez veces dentro de 1.500 m². `datos/SUPERFICIES.csv` compara las áreas anteriores con las del modelo. La compactación deberá conservar los pasos y usos comprobados; no consiste en escalar todo indiscriminadamente.

Estos archivos permiten revisar y editar arquitectura en 3D; no constituyen documentación lista para construir. No se han modificado los modelos anteriores de G3 ni el archivo PERSONAS.3dm.

## Fuentes y reproducción

`datos/GEOMETRIA_3D.pkl` conserva las geometrías de estudio. Es un archivo intermedio local de Python; los .3dm se abren y editan sin él. Los scripts se incluyen como registro del proceso. La regeneración completa presupone el atlas previo y la misma estructura de carpetas del proyecto; los modelos entregados son autónomos.

Las capturas generales de las cuarenta unidades corresponden a la revisión nativa del conjunto. En la revisión final se añadieron apoyos y herrajes pequeños, se redujeron los lavabos y se prolongó el forjado bajo los muros, sin cambiar el trazado principal. Las vistas de detalle y del catálogo se capturan después de estas correcciones.
