# VÍA TRIPO — ARCHIVADA (D03B-05, 2026-08-07)

Cerrada por decisión del autor (Opción ②): PINK_POD_BASE paramétrico = master definitivo de la
familia POD. NO activar suscripción ni relanzar generaciones.

Conservado para reutilización futura:
- 5 multiview packs completos (FRONT/LEFT/BACK/RIGHT × 1024², fondo neutro, mismo objeto):
  TRIPO_PINK_POD_01 · TRIPO_PINK_POD_TRAIN_01 · TRIPO_DROP_TANK_01 · TRIPO_SPECIAL_PLANTER_01 · TRIPO_MIST_HEAD_01
- Workflow verificado: `api_tripo3_1_multiview_to_model` (Comfy Cloud) — LoadImage 44=FRONT,
  45=LEFT, 46=BACK → TripoMultiviewToModelNode(47) → SaveGLB. Coste observado: ~63 créditos/pieza.
  Requiere suscripción de pago del workspace.
- Generador de packs: `../tripo_packs.py` (reproducible desde los bloques de build_all_03b.py).
- Evaluación: `../TRIPO_POD_EVALUATION.pdf` · Registro: `../REGISTRO_03B.md` (adenda + D03B-05).
