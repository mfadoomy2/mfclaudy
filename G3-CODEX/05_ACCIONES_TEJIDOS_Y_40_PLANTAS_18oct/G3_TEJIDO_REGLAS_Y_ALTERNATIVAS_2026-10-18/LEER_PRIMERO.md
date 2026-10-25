# Tejido reconstruido desde relaciones · 18.10.2026

Seis láminas PNG+SVG: matriz, dos registros de razones y tres colocaciones distintas. Acciones, reglas y resultados en JSON/CSV; código reproducible. No modifica Rhino ni recupera el perímetro anterior.

## Qué se ha eliminado
No hay cuatro retiros en esquinas, acceso fijo a izquierda ni cocina predeterminada arriba. Se estudian20acciones, no20salas ni20personas. Dormir aparece como acción de referencia sin fijar aún cuántas personas lo hacen simultáneamente ni sus habitaciones. Llegar cargada, recibir y salir son acciones distintas; podrían utilizar una misma puerta que aún no se ubica.

Dibujar, guardar maqueta, cortar, coser y reparar bicicleta son acciones separadas. Compartir herramientas no implica compartir ruido, suciedad o espacio.

## Qué hace más comprobable el dibujo
28 relaciones tienen una razón escrita y remiten a situaciones ficticiasS01..S16. Las acciones y escenas son hipótesis de proyecto, no entrevistas ni resultados de una encuesta. La matriz gris significa relación no definida. No significa que sean compatibles. Las etiquetas PROTEGER no equivalen automáticamente a alejar: una separación material adecuada puede resolverlas y todavía no está representada.

## Prueba computacional: limitada y explícita
Los20nodos se colocan en una retícula13x9 de posiciones únicas. No hay metros, orientación, iluminación, muros ni perímetro de vivienda. Se hicieron18 búsquedas con4200iteraciones cada una mediante recocido simulado, sin garantizar un óptimo global.

Para probar el método se adoptan dos umbrales GRÁFICOS: proximidad≤3pasos y protección≥5pasos, con distanciaManhattan. Son decisiones exploratorias de quien modela, no distancias normativas, medidas ni evidencias acústicas. Usar varios pesos sirve para producir candidatos, no para afirmar prioridades sociales científicas. METODO.json los declara. Relaciones por turnos/condicionales se dibujan pero no fuerzan proximidad en esta prueba.

Se selecciona un candidato compacto y otros dos con patrones distintos de distancias entre acciones, todos sin incumplimientos de esos umbrales gráficos. La diferencia entre tejidos no se limita a trasladar una misma figura. El total de proximidades es19,22y21pasos respectivamente. No es tiempo de viaje ni recorrido real.

## Qué NO demuestra el resultado
Cero incumplimientos gráficos no demuestra que quepan cama, mesa, cuerpos, paredes o baños. Tampoco acredita aislamiento, privacidad, acceso, luz,40residentes o cumplimiento. Algunas relaciones aún pueden generar grandes recorridos o interferencias al darles tamaño. La prueba demuestra que las reglas actuales admiten más de una organización: no determina una planta única.

## Cómo leer y discutir
1. Revisar ACCIONES_PARA_DISCUTIR.md: aclarar o eliminar acciones antes de agruparlas.
2. Revisar RELACIONES.csv: cambiar la razón o tipo que no tenga sentido. Cada cambio es una decisión de proyecto explícita.
3. Ver matriz y razones antes de las posiciones.
4. Consultar AUDITORIA_RELACIONES.csv para saber cómo se comporta cada vínculo en cada alternativa.
5. Introducir envolventes de uso medidas, compatibilidades por horario y paso libre. Sólo entonces introducir borde, huecos y condiciones de luz; estas pruebas NO asignan viviendas sobre la parcela.
6. Si al dimensionarlo falla, revisar la colocación o las reglas; no comprimir cuerpos para preservar la figura.

La simetría tampoco se ha impuesto. La petición anterior de dos ejes queda pendiente de discutir después de ver qué relaciones merece conservar. No se ha revocado ni convertido en condición escondida. La idea solar del complejo continúa guardada como fase futura y no se desarrolla aquí.
