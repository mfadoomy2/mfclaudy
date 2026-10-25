# -*- coding: utf-8 -*-
"""Comparacion climatica v002 (FASE_03B5B_CLIMA/_data) vs v003 (_reclima/_data).
Mismos campos, mismos agregados; sombra EXCLUSIVA recalculada en ambos (leccion EVT-000027)."""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.normpath(os.path.join(HERE, '..', 'FASE_03B5B_CLIMA', '_data'))
NEW = os.path.join(HERE, '_reclima', '_data')


def agg(d):
    r = {}
    for k in ('metricas', 'cinta', 'spots', 'refugio', 'agua', 'mist'):
        p = os.path.join(d, k + '.json')
        if os.path.exists(p):
            r[k] = json.load(open(p, encoding='utf-8'))
    def L(n):
        return np.load(os.path.join(d, n))
    shA, shB = L('shade_crit_A.npy'), L('shade_crit_B.npy')
    excl = shB - shA                     # sombra EXCLUSIVA del proyecto
    r['sombra'] = dict(
        A_pct=round(float(np.nanmean(shA)) * 100, 1),
        B_pct=round(float(np.nanmean(shB)) * 100, 1),
        exclusiva_pct=round(float(np.nanmean(excl)) * 100, 1))
    for esc in ('E1', 'E2', 'E3'):
        tA = L('f_%s_16_A_Tmrt.npy' % esc); tB = L('f_%s_16_B_Tmrt.npy' % esc)
        uA = L('u_%s_16_A.npy' % esc); uB = L('u_%s_16_B.npy' % esc)
        r[esc] = dict(
            Tmrt_A=round(float(np.nanmean(tA)), 1), Tmrt_B=round(float(np.nanmean(tB)), 1),
            dTmrt=round(float(np.nanmean(tB - tA)), 2),
            UTCI_A=round(float(np.nanmean(uA)), 1), UTCI_B=round(float(np.nanmean(uB)), 1),
            dUTCI=round(float(np.nanmean(uB - uA)), 2),
            m2_UTCI_B_ge40=round(float(np.nansum(uB >= 40.0)) * 0.25, 0),
            m2_UTCI_A_ge40=round(float(np.nansum(uA >= 40.0)) * 0.25, 0))
    rw_A, rw_B = L('radwin_A.npy'), L('radwin_B.npy')
    r['invierno'] = dict(
        A=round(float(np.nanmean(rw_A)), 2), B=round(float(np.nanmean(rw_B)), 2),
        perdida_pct=round(100 * (1 - float(np.nanmean(rw_B)) / max(float(np.nanmean(rw_A)), 1e-9)), 1))
    mc = L('mist_cov.npy')
    r['niebla_cobertura_m2'] = round(float(np.nansum(mc > 0)) * 0.25, 0)
    return r


old, new = agg(OLD), agg(NEW)
out = {'v002': old, 'v003': new}
json.dump(out, open(os.path.join(HERE, '_clima_beforeafter.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('== SOMBRA critica (media ambito) ==')
print(' v002', old['sombra'], '\n v003', new['sombra'])
for esc in ('E1', 'E2', 'E3'):
    print('== %s 16:00 ==' % esc)
    print(' v002', old[esc], '\n v003', new[esc])
print('== INVIERNO (radwin) ==\n v002', old['invierno'], '\n v003', new['invierno'])
print('== NIEBLA m2 ==', old['niebla_cobertura_m2'], '->', new['niebla_cobertura_m2'])
for k in ('metricas', 'cinta', 'refugio'):
    if k in old and k in new:
        print('== %s ==' % k)
        print(' v002:', json.dumps(old[k], ensure_ascii=False)[:600])
        print(' v003:', json.dumps(new[k], ensure_ascii=False)[:600])
print('== SPOTS ==')
for tag, dd in (('v002', old), ('v003', new)):
    sp = dd.get('spots', {})
    hot = sp.get('hotspots', sp if isinstance(sp, list) else [])
    cool = sp.get('coolspots', [])
    print(' %s hotspots:%s coolspots:%s' % (tag, len(hot), len(cool)))
