# Verificación de entrega

- Seis archivos .3dm releídos por rhino3dm; cero geometrías inválidas en la comprobación IsValid.
- Conjunto final: 11.176 objetos incluyendo definiciones, 33 capas, 16 definiciones de bloque, 10 pabellones y 40 instancias de personas.
- Unidad y detalles independientes contienen Breps sin bloques dependientes externos.
- Conjunto abierto y guardado nativamente en Rhino 8. Se han comprobado en el archivo final las once puertas laterales operables de escaleras, los tres enlaces del extremo este, el colector DN250 y los rellanos revisados.
- La vista nativa muestra aristas en lugar de superficies sólidas incluso tras ClearAllMeshes y reconstrucción de cachés. Captura 08_RHINO_NATIVO.png registra el fallo. No se considera resuelto. Se entrega PREVIA_SOLIDA_MALLAS.3dm, geometría triangulada exacta y validada, para visualizar, además del original Brep editable.
- Los cuatro renders de Blender proceden de la triangulación del CAD final y se han inspeccionado visualmente. No se han generado con IA.
- Modelo de barras: pruebas axial y voladizo, equilibrio de fuerzas y comparación de discretización. No equivale a comprobación estructural integral del edificio.
- No se ha realizado auditoría exhaustiva de interferencias ni certificado de habitabilidad, accesibilidad, incendios o cómputo urbanístico.
- Históricos de fallos resueltos y versiones rechazadas se excluyen del ZIP final.
