from pathlib import Path
import json,math,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
R=Path(__file__).resolve().parents[1];A=json.loads((R/'calculo/ESTRUCTURA_RESULTADOS.json').read_text());B=json.loads((R/'calculo/SUBSISTEMAS_RESULTADOS.json').read_text())
els=A['elements'];nodes=np.array(A['nodes']);sway=max(v['max_sway_mm'] for k,v in A['cases'].items() if k.startswith('ELS'));vert=A['cases']['ELS_GQ']['max_vertical_mm'];ratio=max(e['utilization'] for e in els);base=max(v['max_sway_mm'] for k,v in A['unbraced_baseline'].items() if k.startswith('ELS'))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11});bg='#f4f1e8';ink='#25382e'
fig=plt.figure(figsize=(15,9),facecolor=bg);ax=fig.add_subplot(111,projection='3d',facecolor=bg)
segs=[nodes[[e['i'],e['j']]] for e in els];lc=Line3DCollection(segs,cmap='magma',linewidths=[max(.6,e['D']*4) for e in els]);lc.set_array(np.array([e['utilization'] for e in els]));lc.set_clim(0,1);ax.add_collection3d(lc)
ax.set_xlim(12,60);ax.set_ylim(-9,11);ax.set_zlim(0,24);ax.set_box_aspect((48,20,24));ax.view_init(18,-72);ax.set_xlabel('x / m');ax.set_ylabel('y / m');ax.set_zlabel('z / m');fig.colorbar(lc,ax=ax,shrink=.5,label='Interacción preliminar N/Nb + M/Mrd')
fig.suptitle('La estructura detrás de la forma / ejes del modelo analítico',fontsize=23,color=ink,x=.05,ha='left');fig.text(.05,.04,f'{len(nodes)} nodos · {len(els)} elementos · 6 grados de libertad/nodo · máximo preliminar {ratio:.2f} · no sustituye la comprobación integral',color=ink)
fig.savefig(R/'vistas/05_ESTRUCTURA_ANALITICA.png',dpi=160,bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(13,7),facecolor=bg);ax.set_facecolor(bg)
vals=[base]+[r['sway_mm'] for r in A['iteration_history']];labels=['Árboles sin conexión posterior']+['Con arriostramiento / escala sección '+str(r['scale']) for r in A['iteration_history']]
ax.barh(labels[::-1],vals[::-1],color=['#bc3578']+['#e0ba31']*(len(vals)-2)+['#506b51']);ax.axvline(40,color=ink,linestyle='--',label='Objetivo de estudio 40 mm')
for i,v in enumerate(vals[::-1]):ax.text(v+2,i,f'{v:.1f} mm',va='center')
ax.set_xlabel('Desplazamiento lateral máximo en las combinaciones de ensayo ELS');ax.set_title('La estabilidad cambia la forma y las secciones',loc='left',fontsize=21,pad=20);ax.legend();ax.spines[['right','top']].set_visible(False)
fig.tight_layout();fig.savefig(R/'vistas/06_ITERACIONES_ESTRUCTURALES.png',dpi=160);plt.close(fig)
# Measured levels and programme drawing, using the actual analytic plate outline.
fig,ax=plt.subplots(figsize=(15,8),facecolor=bg);ax.set_facecolor(bg)
for p in A['plates']:
 xs=[x for x,y in p['outline']];ax.plot([min(xs),max(xs)],[p['z'],p['z']],color='#d1ad25',lw=5);ax.text(p['cx'],p['z']+.35,p['id']+' / +'+str(p['z']),ha='center',fontsize=10)
for b in A['bays']:
 for z in b['levels']:ax.plot([b['x']-4.8,b['x']-4.8,b['x']+4.8,b['x']+4.8],[z,z+2.2,z+2.2,z],color='#8aa797',lw=1)
ax.set_xlim(12,61);ax.set_ylim(0,27);ax.set_aspect('equal');ax.set_title('Orden espacial / tres árboles y cotas alternadas',loc='left',fontsize=21);ax.set_xlabel('Longitud / m');ax.set_ylabel('Cota / m');ax.grid(alpha=.15);fig.tight_layout();fig.savefig(R/'vistas/07_ORDEN_Y_COTAS.png',dpi=160);plt.close(fig)
rib=B['roof_rib_selected'];j=B['secondary_joists'];joint=B['branch_connection'];rain=B['rain'];thermal=B['thermal'];cab=B['membrane_cable'];conv=A['convergence'];area=sum(p['area'] for p in A['plates'])
md=f'''# Selva macarra V4 | Memoria técnica y razón de la forma

16 de octubre de 2026. Anteproyecto y predimensionado reproducible. El nombre del archivo «calculada» identifica la existencia de un modelo analítico preliminar; no significa edificio certificado ni proyecto de ejecución.

## Decisiones que ordenan la radicalidad

Diez grandes pabellones, repartidos en tres grupos de árboles, sustituyen el apilamiento uniforme rechazado. Cada pabellón contiene cuatro refugios privados, cocina y mesa de grupo, y dos baños. Las plataformas se alternan en altura para producir diagonales, perspectivas y vacíos de más de una planta. La bóveda reúne cada grupo en un volumen grande. Las ramas recogen los bordes del forjado y los troncos adelgazan hacia arriba. Una retícula posterior conecta los árboles para controlar la deriva; el frente conserva la apertura y los voladizos.

Cotas por grupo: {A['bays'][0]['levels']}; {A['bays'][1]['levels']}; {A['bays'][2]['levels']}. La altura máxima de cubiertas exteriores ronda 25,9 m. La parcela procede del archivo geométrico del proyecto, no de una nueva comprobación urbanística.

## Qué se ha calculado

Pórtico espacial de {len(nodes)} nodos y {len(els)} elementos de viga de seis grados de libertad por nodo. Modelo elástico lineal de barras con ejes curvos discretizados; pies empotrados y uniones idealizadas rígidas. Perfiles circulares huecos de acero. E=210 GPa, G=81 GPa, fy adoptado=345 MPa por el intervalo de espesores de la propuesta S355. Autopeso del acero incluido. Las secciones y sus ejes se transfieren al Rhino; las curvas NURBS interpolan la discretización analítica.

Hipótesis de carga: 3,6 kN/m² permanentes de suelo, acabados, particiones, cubierta e instalaciones; 5,0 kN/m² variables sobre TODA la bandeja, como ensayo conservador de zonas comunes respecto a dormitorios; además, autopeso de seis viguetas por bandeja y 2,5 kN en cada uno de tres depósitos. Ensayo de viento de ±1,0 kN/m² en las dos direcciones, con momento por aplicación a 2,15 m sobre la planta. Esta presión es una hipótesis de ensayo, no la determinación completa del viento de Madrid.

Se han explorado combinaciones ELS G+Q con viento positivo y negativo y ELU 1,35G+1,5Q; 1,35G+1,5W+1,05Q; 1,35G+1,5Q+0,9W, con los signos aplicables. Las cargas asimétricas de ocupación, torsiones accidentales y fases de montaje aún requieren casos adicionales.

## Resultados que han modificado el diseño

- Árboles sin conexión posterior ni aumento de secciones: deriva máxima de ensayo **{base:.1f} mm**.
- Versión con conexión posterior y secciones afinadas seleccionadas: **{sway:.1f} mm** de deriva máxima ELS y **{vert:.1f} mm** de desplazamiento vertical máximo para G+Q.
- Interacción preliminar máxima de barras N/Nb + M/Mrd: **{ratio:.3f}**. Se usa cribado de Euler con longitud de cada tramo curvo completo y curva de imperfección conservadora; esto no verifica el pandeo global ni sustituye la normativa de estabilidad.
- Refinamiento de cuatro a ocho segmentos por curva: {conv['sway_mm_4']:.2f} → {conv['sway_mm_8']:.2f} mm de deriva máxima.
- Pruebas del motor: tracción axial y voladizo contrastados con soluciones analíticas; equilibrio global de fuerzas comprobado para cada caso.

La elección la condiciona la rigidez, además de la resistencia. Por ello aparecen la conexión posterior, la profundidad de las ramas y las vigas de bandeja. La disminución de diámetro del tronco responde a la reducción de cargas hacia su extremo superior. Todas las barras se identifican por tipo, diámetro y espesor en `ESTRUCTURA_RESULTADOS.json`.

## Suelo y envolvente

Viguetas secundarias **{j['profile']}**, cada 1,15 m, luz de ensayo 7,15 m: tensión de flexión ELU {j['bending_ULS_MPa']:.1f} MPa y flecha ELS {j['deflection_SLS_mm']:.1f} mm frente a L/300={j['limit_L300_mm']:.1f} mm. Se modelan como perfiles huecos; los extremos, soldaduras y colaboración del tablero deben desarrollarse.

Costillas de bóveda seleccionadas **Ø{rib['D_mm']:.1f} × {rib['t_mm']:.1f} mm** cada {rib['rib_spacing_m']:.3f} m. Ensayo plano con pies fijos, G=1,0 y Q=1,0 kN/m²: tensión ELU {rib['stress_ULS_MPa']:.1f} MPa y desplazamiento ELS aproximado {rib['peak_displacement_SLS_mm']:.1f} mm. Faltan el pandeo, la acción de la envolvente, succión y el arriostramiento fuera del plano.

Detalle estratificado: contrachapado 18 mm + corcho 160 mm + tablero 18 mm + impermeabilización 2 mm, cámara y piel exterior. Transmitancia unidimensional de ensayo **U={thermal['opaque_component_U_W_m2K']:.3f} W/m²K**, con conductividades asumidas. Los puentes térmicos, las carpinterías, la estanqueidad y el comportamiento energético global no están verificados.

## Nudo ramificado

Se desarrolla una brida anular de dos placas de 35 mm, dieciséis M30 8.8 en círculo de radio 0,57 m, cartelas y tubos huecos. Para las fuerzas de referencia del ramal crítico de gravedad: N={joint['branch_reference_N_kN']:.1f} kN; M={joint['branch_reference_M_kNm']:.1f} kNm. Reparto elástico simplificado: tracción estimada por perno={joint['bolt_tension_estimate_kN']:.1f} kN, frente a resistencia nominal estimada={joint['bolt_tension_resistance_kN']:.1f} kN. No se han comprobado el efecto palanca de las chapas, las soldaduras, las tensiones locales del casquillo ni la rigidez real de la unión.

Los apoyos transmiten esfuerzos importantes al suelo. Las placas y encepados del Rhino son reservas geométricas; no se ha dimensionado una cimentación con capacidad geotécnica. Las reacciones se entregan para que ese siguiente cálculo parta de datos, en lugar de atribuir capacidad a raíces decorativas.

## Velas, lluvia y mantenimiento

La cubierta textil es una protección exterior adicional. Sus anclajes transmiten viento y pretensado a las bandejas. Ensayo elemental de cable parabólico de 5,25 m, flecha 0,60 m, franja tributaria de 2 m y presión 1,0 kN/m²: tensión ELU aproximada **{cab['tension_ULS_kN']:.1f} kN**. La propuesta dibuja tensores y manguitos; queda pendiente el análisis no lineal de membrana, el pretensado y la respuesta aerodinámica. Los tirantes principales se representan de Ø18 mm, superiores al Ø16 mm del ensayo; deben comprobarse sus terminales y pretensado.

Una vela recoge aproximadamente {rain['one_canopy_m2']:.1f} m². Lluvia de ensayo 100 mm/h: **{rain['one_canopy_L_s']:.3f} L/s** por vela y **{rain['all_canopies_L_s']:.2f} L/s** para el conjunto. A media sección y pendiente 1 %, con n=0,011, Manning da {rain['half_full_manning_capacity_L_s_at_1percent']['100']:.2f} L/s para DN100, {rain['half_full_manning_capacity_L_s_at_1percent']['200']:.2f} para DN200 y {rain['half_full_manning_capacity_L_s_at_1percent']['250']:.2f} para DN250. Son comprobaciones hidráulicas ideales, no sustituyen HS5, accesorios, mantenimiento, lluvia local ni el cálculo de bajantes.

En el modelo hay ramales DN100, rebosaderos DN50 y montantes de lluvia DN200; saneamiento DN110 y bandeja eléctrica se mantienen diferenciados. Tres depósitos suspendidos de unos 250 L apoyan el riego, con su carga añadida al modelo analítico. No se presupone la conexión real con una red municipal sin su comprobación.

## Programa, ascensores y límites de privacidad

40 residentes en diez grupos. Las habitaciones son privadas; cocina, estar y baños se comparten por grupo; las terrazas, talleres, cantina, aula y lavandería forman la infraestructura del conjunto. Los accesos a los pabellones se sitúan en el paso transversal lateral; el frente acristalado no exige cruzar una cocina para entrar.

Los tres ascensores resuelven las cotas alternadas de cada grupo de árboles, con cabinas propuestas de 1,40 × 1,60 m, puertas nominales de 0,90 m, guías, contrapesos, máquina, botoneras, foso y rellanos. Las escaleras diagonales permiten recorrer el conjunto; las escaleras de extremo se separan de las habitaciones. El fondo no se considera otra calle: la descarga debe volver al frente oeste por el recorrido de suelo.

La reconstrucción formal de la gran bóveda modifica la unidad V2. Las células dibujadas ahora son compactas, aproximadamente 8 m² útiles geométricos, y no conservan los 12 m² de aquella versión. La distribución accesible de baño y habitaciones, acústica y habitabilidad deben revisarse antes de dar por cerrada la tipología.

Las diez bandejas suman **{area:.2f} m²** en proyección horizontal, incluyendo viviendas y terrazas. No se deben sumar de nuevo los suelos de los pabellones que ya están dentro de esas bandejas. Se entrega un inventario geométrico aparte para programa de planta baja, escaleras, galerías y núcleos. Su comparación completa con los 1.500 m² aproximados del enunciado sigue abierta; no se atribuye automáticamente una exención a las superficies exteriores.

## Qué significa y qué no acredita este estudio

Permite relacionar forma, cargas, secciones y desplazamientos y reproducir las decisiones de predimensionado. No certifica la seguridad del edificio. Permanecen pendientes segundo orden, pandeo global, imperfecciones, estabilidad de montaje, vibración y confort dinámico, fatiga, todas las uniones, fuego, cimentación, viento de sitio y membranas, compartimentación, evacuación hasta calle y accesibilidad completa. El modelo de arquitectura tampoco cuenta como comprobación integral de interferencias.

## Fuentes de referencia y archivos de cálculo

- CTE DB-SE-AE, acciones: https://www.codigotecnico.org/pdf/Documentos/SE/DBSE-AE.pdf
- CTE DB-SE-A, acero: https://www.codigotecnico.org/pdf/Documentos/SE/DBSE-A.pdf
- CTE DB-SUA: https://www.codigotecnico.org/pdf/Documentos/SUA/DBSUA.pdf
- CTE DB-SI: https://www.codigotecnico.org/pdf/Documentos/SI/DBSI.pdf
- Enunciado del taller: copia de `lectura/enunciado.txt`, viviendas temporales para jóvenes en El Rastro, aproximadamente 1.500 m², número libre cercano a veinte unidades o cuarenta habitantes y desarrollo de anteproyecto.
- Modelo analítico completo: `calculo/ESTRUCTURA_RESULTADOS.json`.
- Cálculos locales: `calculo/SUBSISTEMAS_RESULTADOS.json`.
- Fuentes reproducibles: `fuentes/calcular_estructura.py`, `fuentes/calcular_subsistemas.py`, `fuentes/modelar_v4_rhino.py` y `fuentes/modelar_detalles.py`.
'''
(R/'MEMORIA_TECNICA_Y_RAZON_DE_LA_FORMA.md').write_text(md)
print('MEMORIA',len(md.split()),'palabras','Sway',sway,'ratio',ratio)
