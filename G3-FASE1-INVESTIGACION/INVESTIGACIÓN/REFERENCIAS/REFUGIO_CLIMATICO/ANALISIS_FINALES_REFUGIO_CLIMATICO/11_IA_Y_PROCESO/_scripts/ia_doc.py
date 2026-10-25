# -*- coding: utf-8 -*-
"""FASE FINAL - IA_EN_EL_REFUGIO_CLIMATICO.pdf (§33-§38). Solo Refugio; nunca la Maqueta."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_scripts'))
import refugio_editorial as E  # noqa: E402

OUT = os.path.join(BASE, '11_IA_Y_PROCESO')
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(BASE, '00_SISTEMA_Y_FUENTES', '_mining', 'mining_full.json'),
          encoding='utf-8') as f:
    MIN = json.load(f)
FOR_ = next(v for v in MIN.values() if isinstance(v, dict) and 'n_eventos' in v
            and v['n_eventos'] >= 240)
GEN = next(v for v in MIN.values() if isinstance(v, dict) and 'narrativa_existente' in v)

doc = E.Doc(os.path.join(OUT, 'IA_EN_EL_REFUGIO_CLIMATICO.pdf'),
            'IA EN EL REFUGIO CLIMÁTICO', '11 · IA Y PROCESO')

E.portada(doc, 'No hubo un botón de\n«generar proyecto»',
          'Cómo se usó de verdad la inteligencia artificial en el Refugio Climático: '
          'no como generadora de imágenes, sino como infraestructura de investigación '
          'y diseño — con sus errores, sus diagnósticos y su registro forense completo. '
          'Documento real, no marketing.',
          '11 · IA Y PROCESO',
          [('EVENTOS FORENSES', '240+'), ('ERRORES REGISTRADOS', '15 instructivos'),
           ('VERSIONES', 'v001 › v006'), ('AUDITORÍAS', 'A0–A12 × 6 rondas')],
          num='IA')

# ---------------------------------------------------------------- la tesis + el ciclo
p = doc.page('LA TESIS')
y = E.A4H - 1.0
y = p.kicker(y, 'IA-01 · LA TESIS (§35)')
y = p.title(y, 'El ciclo real, once verbos', size=17)
y = p.subtitle(y, 'El proceso no fue PROMPT  ›  PROYECTO. Fue un ciclo que se recorrió '
                  'cientos de veces, con el error como motor y la auditoría como juez. '
                  'Cada vuelta está registrada con identificador EVT en el forense.')
# diagrama del ciclo
pasos = ['INPUT', 'LECTURA', 'HIPÓTESIS', 'GENERACIÓN', 'MEDICIÓN', 'ERROR',
         'DIAGNÓSTICO', 'RECTIFICACIÓN', 'REGENERACIÓN', 'AUDITORÍA', 'CONOCIMIENTO']
import matplotlib.pyplot as plt  # noqa: E402
ax = p.axes(E.MX, y - 2.5, E.A4W - 2 * E.MX, 2.3)
ax.set_xlim(0, 11); ax.set_ylim(0, 2)
for i, s in enumerate(pasos):
    col = E.MAGENTA if s in ('ERROR', 'CONOCIMIENTO') else (E.GREEN if s == 'AUDITORÍA' else E.INK)
    xx = 0.5 + (i % 6) * 1.8
    yy = 1.45 if i < 6 else 0.45
    ax.add_patch(plt.Rectangle((xx - 0.62, yy - 0.24), 1.24, 0.48, fc='white', ec=col, lw=1.1))
    ax.text(xx, yy, s, ha='center', va='center', size=6.2, color=col, family=E.SERIF,
            weight='bold')
    if i < 5:
        ax.annotate('', xy=(xx + 1.18, yy), xytext=(xx + 0.62, yy),
                    arrowprops=dict(arrowstyle='-|>', color=E.HAIR, lw=1))
    elif i == 5:
        ax.annotate('', xy=(0.5 + 5 * 1.8, 0.69), xytext=(0.5 + 5 * 1.8, 1.21),
                    arrowprops=dict(arrowstyle='-|>', color=E.HAIR, lw=1))
    elif i < 10:
        x2 = 0.5 + (i - 6) * 1.8
        ax.annotate('', xy=(x2 + 1.18, 0.45), xytext=(x2 + 0.62, 0.45),
                    arrowprops=dict(arrowstyle='-|>', color=E.HAIR, lw=1))
ax.axis('off')
y -= 2.75
y = p.dashlist(E.MX, y, [
    ('El error no es la excepción del ciclo: es su combustible.', '15 errores '
     'instructivos registrados con diagnóstico y rectificación; 4 de ellos '
     'METODOLÓGICOS — el instrumento midiéndose mal a sí mismo y corrigiéndose.'),
    ('La auditoría es un poder independiente:', 'los módulos A0–A12 reconstruyen la '
     'escena desde el generador e ignoran lo que el generador CREE haber hecho. '
     'Cuando ambos discrepan, gana el auditor.'),
    ('El conocimiento se acumula fuera de la conversación:', 'geometría en JSON '
     'versionado, decisiones en DEC-xxxx, errores en EVT-xxxx, memoria de proyecto '
     'persistente. Nada vive solo en el contexto de un chat.'),
], wrap=88, gap=0.1)
doc.add(p)

# ---------------------------------------------------------------- casos de error
p = doc.page('EL ERROR COMO MOTOR')
y = E.A4H - 1.0
y = p.kicker(y, 'IA-02 · CINCO ERRORES QUE CONSTRUYERON CRITERIO (§36)')
y = p.title(y, 'Evidencia, no anécdota', size=16)
casos = [
    ('EVT-000025 · La lámina de microalgas era «opaca»',
     'La cámara de microalgas vivía en la capa 11_WATER y el clasificador la trató '
     'como agua opaca: el dosel no transmitía NADA. Diagnóstico: el error no estaba '
     'en la física sino en la taxonomía de capas. Rectificación: clase propia con '
     'tau_canopy=0,12 declarado e intervalo 0,05-0,25. Lección: los errores de '
     'CLASIFICACIÓN son más peligrosos que los de cálculo — no hacen ruido.'),
    ('EVT-000026 · El cielo que no era cielo',
     'El factor de visión de cielo contaba como CIELO los rayos que atravesaban el '
     'dosel: MRT óptimista bajo las hojas. Rectificación: el rayo que atraviesa '
     'transmite sol pero VE membrana (want_first en el trazador). Sin este arreglo, '
     'el descubrimiento D-001 (cola positiva por pérdida de cielo) habría sido '
     'invisible: el instrumento corregido fue el que luego encontró el hallazgo.'),
    ('EVT-000028 · El umbral imposible',
     'El índice de refugio exigía UTCI_B<32 °C con aire a 34,7 °C: físicamente '
     'inalcanzable — TODA la plaza suspendía. Rectificación: umbral relativo '
     '(ΔUTCI≤−2 K sostenido). Lección: una métrica mal planteada convierte un '
     'proyecto que funciona en un fracaso estadístico, y viceversa.'),
    ('Las cuatro auditorías idénticas (03B.9)',
     'Cuatro rondas de auditoría v006 devolvieron resultados byte-idénticos: el '
     'retarget había fallado en silencio (raw string con backslash final) y se '
     'auditaba la versión ANTERIOR. Diagnóstico tras 3 rondas de arreglos fútiles. '
     'Desde entonces todo retarget se verifica con grep y la fase final aborta si '
     'detecta residuos (el port del pipeline de render de este mismo paquete saltó '
     'una vez por esa guarda — funcionó).'),
    ('El zócalo que cortaba la calle Arenal',
     'Un zócalo decorativo del ECI, emitido como banda cerrada sobre el polígono OSM '
     'cóncavo, puenteaba una bocacalle EN EL RÁSTER peatonal: 3 falsos RED. El rastreo '
     'llegó hasta el triángulo culpable (probes 10-12) antes de tocar nada. Lección: '
     'no se re-clasifica un rojo para que desaparezca; se encuentra su triángulo.'),
]
for titulo, cuerpo in casos:
    p.text(E.MX, y, titulo, size=9, weight='bold')
    y -= 0.19
    y = p.body(E.MX, y, cuerpo, wrap=104, size=7.6)
    y -= 0.04
doc.add(p)

# ---------------------------------------------------------------- infraestructura
p = doc.page('IA COMO INFRAESTRUCTURA')
y = E.A4H - 1.0
y = p.kicker(y, 'IA-03 · MÁS ALLÁ DE LA GEOMETRÍA (§37)')
y = p.title(y, 'Lo que la IA midió, cruzó y descubrió', size=16)
y = p.tabla(E.MX, y, E.A4W - 2 * E.MX,
            ['CAPACIDAD', 'INSTANCIA REAL EN EL REFUGIO', 'EVIDENCIA'],
            [['Medir', 'auditoría A0-A12: 848×492 celdas, 45 pares de accesos, 160 puntos de mantenimiento',
              '_reaudit9/_data'],
             ['Simular', 'clima físico: 431 posiciones solares, UTCI por celda, 4 escenarios meteorológicos',
              '_reclima9/_data'],
             ['Detectar contradicciones', 'paso libre vs sombra: el 85 % del calor residual vive sobre los ejes (D-015)',
              'DISCOVERIES_REGISTER'],
             ['Encontrar fallos del instrumento', '4 errores metodológicos del propio simulador, corregidos y registrados',
              'EVT-000025..28'],
             ['Automatizar auditorías', '6 rondas completas v002 › v006; de decenas de RED a 0',
              'ISSUES_REGISTER × 6'],
             ['Explorar escenarios', 'E1/E2/E3/E4, fallos (CLI-10), LOW/BASE/HIGH económicos y sociales',
              'motores fase final'],
             ['Cruzar datos', '18 relaciones confirmadas entre 12 sistemas; 7 KPI nuevos',
              'CROSS_ANALYSIS_MATRIX'],
             ['Construir trazabilidad', '240+ eventos EVT, decisiones DEC, snapshots con hash SHA-256',
              '_FORENSIC_PROCESS + BASELINE_SNAPSHOT']],
            col_w=[1.5, 3.6, 1.6], size=6.8)
y -= 0.08
y = p.panel(E.MX, y, E.A4W - 2 * E.MX, 1.2, 'DÓNDE DECIDIÓ EL HUMANO')
p.text(E.MX + 0.16, y, 'Los mandatos de fase (qué perseguir y con qué criterio de '
       'cierre), los veredictos de aceptación, la elección de la lámina frente al '
       'libro, el «no me des un PASS por cortesía» y el juicio último sobre los '
       'trade-offs (verano/invierno, confort/patrimonio) son humanos. La IA fabricó '
       'evidencia y criterio técnico; la dirección del proyecto nunca dejó de ser '
       'una decisión de autor.', size=8.2, wrap=94)
doc.add(p)

# ---------------------------------------------------------------- proceso en numeros
p = doc.page('EL PROCESO EN NÚMEROS')
y = E.A4H - 1.0
y = p.kicker(y, 'IA-04 · REGISTRO Y REPRODUCIBILIDAD (§36/§51)')
y = p.title(y, 'Todo esto se puede volver a ejecutar', size=16)
x = E.MX
p.bignum(x, y, '240+', '', 'eventos forenses EVT con timestamp'); x += 1.9
p.bignum(x, y, '6', '', 'versiones geométricas v001-v006'); x += 1.7
p.bignum(x, y, '279', '', 'análisis catalogados en el registro maestro'); x += 1.9
p.bignum(x, y, '29', '', 'archivos de baseline con hash SHA-256')
y -= 1.2
y = p.dashlist(E.MX, y, [
    ('Distinción mantenida (§36):', 'EVIDENCIA (npy/json/pdf con ruta y fecha), '
     'REGISTRO (eventos EVT/DEC contemporáneos al hecho) y RECONSTRUCCIÓN EDITORIAL '
     '(este documento). Cuando este PDF narra, cita el registro; no lo sustituye.'),
    ('Reproducibilidad práctica:', 'geometría = build_all_03b9.py (determinista) sobre '
     'geometria_maestra_v006.json congelada; análisis = motores de ANALISIS_FINALES '
     'sobre esa baseline; cada cifra publicada apunta a su script en '
     'FINAL_METRICS_REGISTRY.csv.'),
    ('Lo que este documento NO es:', 'una promesa de que «la IA diseña sola». De los '
     '240 eventos, 11 son ERROR y 4 ERROR_METODOLOGICO: la tasa de fallo es parte '
     'del método, y publicarla es lo que hace creíble el resto.'),
], wrap=88, gap=0.12)
doc.metric('IA-M1', 240, 'eventos', 'A', 'conteo flog', '_FORENSIC_PROCESS')
doc.add(p)
doc.close()
print('IA doc ok', doc.folio, 'pp')
