# -*- coding: utf-8 -*-
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '_FORENSIC_PROCESS')))
import flog

flog.event(fase='03B9', tipo_evento='cierre',
           objetivo='FASE 03B.9 COMPLETA — VEREDICTO: V006 HYPERDETAIL PASS',
           resultado=('v005 -> v006 en 12 builds. BOTANICA: BOTANICAL_MASTERPLAN_v001.csv (17 especies '
                      'reales con LAI/hidrica/estacional), 19 roles de asset (10 nuevos CC0/CC-BY en '
                      '_assets_veg2, ASSET_PROVENANCE.csv actualizado), variantes anti-clon por posicion '
                      '(espejo/joven/maduro), balsa-microecosistema (nenufares por edades, 2 juncos, '
                      'emergentes, rizomas), huerto con goteo/mulch/plantula/maiz por fases, arbol real '
                      '(olmo->Celtis). CONSTRUCTIVO: terminales de cable (casquillo+tensor+horquilla+ '
                      'pasador), canopy 1:5 (costuras, rulo, camara de microalgas con racores y registro), '
                      'cinta con juntas de dilatacion cada 18 m + tapas mantenimiento, ascensor (guias/'
                      'puertas/sensor/foso/ventilacion/cuadro), pods (cinchas/ojales/corona/inflado), '
                      'depositos (brida/purga/placa), atrio Metro (marquesina VOLADA a la aproximacion '
                      '+4.5, bolardos luminosos, canal recortado contra el poligono OSM), fachadas Correos '
                      '(zocalo/puerta/15 marcos) y ECI (cornisa+zocalo POR ARISTA con guarda de corredor). '
                      'AUDITORIA: 0 RED / 26 YELLOW / 18 GREEN (V-001/002 1.12m resueltos por regla local; '
                      'marquesina 2.43m->fuera; zocalo ECI que cortaba Arenal en el raster -> emision por '
                      'arista; canal atrio 0.63m -> recorte pip; huerto x tren -> guarda 4.5). PURGA: '
                      'TOTAL ERROR 191->22 (residual documentado: 4 dups pliegue, 9 costuras abanico, '
                      '6 tropicales, 3 tuberias enterradas a proposito). CLIMA RE-EJECUTADO (_reclima9): '
                      'k_veg POR ESPECIE en el voxel (Beer-Lambert acumulado), arbolado OSM por ancla '
                      '(Platanus 0.750 vs Celtis 0.633), evapotranspiracion por copa/LAI del masterplan '
                      '(20 arboles + 295 masas: 425 L/h, 286 kW). Resultados: sombra critica 3.4->42.3%, '
                      'dMRT -10.9 K medio (-28.2 refugio), dUTCI -2.6 (-3.4 con niebla), 3876 m2 refugio. '
                      'MICROSCENES: 30 puntos x4 distancias en i1/i2 + delta i3 sobre build 12 (huerto/'
                      'pods completos; harness Edge inestable documentado y endurecido). Autocritica '
                      'adversarial con 12 corregidos + 9 abiertos honestos en SELF_CRITIQUE_V006.md. '
                      'Entregables: 4 masters .3dm, AUDIT_V006_MASTER.pdf, CLIMATE_V006_MASTER.pdf, '
                      'BOTANICAL_CONTACT_SHEET.pdf, V005_V006_CLOSE_RANGE.pdf, HYPERDETAIL_REPORT.md, '
                      'SELF_CRITIQUE_V006.md, BOTANICAL_MASTERPLAN_v001.csv, _veg_clima.json. '
                      'v005 intacta. Lecciones: verificar retargets con grep (4 audits auditaron v005 '
                      'por un raw-string roto); una banda mitered cerrada sobre footprint OSM concavo '
                      'puentea entrantes; el proxy ESTP del generador no es el poligono del auditor.'),
           parametros={'builds': 12, 'red': 0, 'yellow': 26, 'green': 18,
                       'purge_error': 22, 'especies': 17, 'roles_asset': 19,
                       'dMRT_K': -10.9, 'dUTCI_K': -2.62, 'm2_refugio': 3876})
print('cierre 03B9 registrado')
