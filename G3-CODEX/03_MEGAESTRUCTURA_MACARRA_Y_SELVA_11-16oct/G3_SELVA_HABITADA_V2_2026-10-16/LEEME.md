# Selva habitada | V2 | 16.10.2026

Propuesta conceptual de unidad U4 y primer encaje para 40 residentes. La forma radical de la imagen generada y el modelo de encaje no están todavía coordinados pieza por pieza.

## Contenido

- PROPUESTA_SELVA_HABITADA.pdf: 13 láminas A3 horizontales; propuesta, dibujos, programa, guion oral y fuentes.
- GUION_EXPOSICION.md: texto editable para explicar distribución, estructura, reglas, programa y gestión.
- modelos/01_UNIDAD_U4.3dm: unidad en metros, mallas por capas.
- modelos/02_SELVA_EN_PARCELA.3dm: diez unidades, núcleos, programa, galerías y contexto en metros.
- vistas/01-06: proyecciones y diagramas del ensayo geométrico, PNG y SVG.
- vistas/07-09: exploraciones generadas; no son documentación métrica.
- fuentes/: generador geométrico, editor del cuaderno y prompts de las nuevas imágenes.
- verificacion/: comprobaciones geométricas limitadas y revisión del paquete.

## Límites del estudio

Los 1.550,07 m² suman unidades, reserva bruta de núcleos y programa comunitario; los núcleos incluyen sus huecos. Se añaden 455,62 m² de galerías y claros abiertos. No se presume cómo computan urbanísticamente. El objetivo previo de 1.500 m² y las 40 personas se mantienen como hipótesis.

Se comprueba el lindero de las huellas U4 y la ausencia de solapes entre unidades de un mismo nivel. No se ha validado la normativa, la estabilidad, las cimentaciones, la suspensión, la accesibilidad, el fuego, el confort, la iluminación ni todas las interferencias tridimensionales. Las secciones estructurales son gráficas, no calculadas. La única salida a calle representada es la del frente oeste; el fondo no se considera otra calle.

Esta V2 libera el acceso de la cocina, desplaza las costillas fuera de las habitaciones y añade huecos a las escaleras. No modifica los originales ni sustituye la megaestructura macarra de partida.

## Procedencia

Modelo original: /Users/adam/Downloads/MEGAESTRUCTURA_MACARRA/modelo/MEGAESTRUCTURA_MACARRA.3dm

Parcela y contexto: /Volumes/T7/G3 Proyectos/G3 CLAUDE/01_E2_IMAGINARIOS_PERSONAS_Y_MECANISMOS_05-06oct/G3_MECANISMOS_EN_PARCELA_2026-10-05/geometria/

Investigación previa: /Users/adam/Downloads/G3_SOL_MEGAESTRUCTURA_2026-10-11/

Reproducir dibujos y modelos: uv run --with rhino3dm --with numpy --with shapely --with matplotlib python fuentes/disenar_selva.py

Reproducir PDF: uv run --with reportlab python fuentes/editar_cuaderno.py
