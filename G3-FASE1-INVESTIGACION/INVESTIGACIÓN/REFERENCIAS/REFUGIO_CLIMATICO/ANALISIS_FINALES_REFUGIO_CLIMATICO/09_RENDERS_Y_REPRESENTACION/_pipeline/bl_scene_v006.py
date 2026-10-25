# -*- coding: utf-8 -*-
"""FASE FINAL (porta 03D) — produccion final en Blender/Cycles sobre v003 CONGELADA.
Uso:  blender -b --factory-startup -P bl_scene.py -- build
      blender -b -P bl_scene.py -- render <H1..H7|all> <mediodia|tarde|both> [w h samples]
Fuentes (solo lectura): scene_full.js v006 (build 12) + geometria_maestra_v006.json
+ a4_ribbon.json (eje construido) + atmos_config.json (camaras) + SUN_03D.json (PSA real).
La niebla E03 (sprites) se sustituye por VOLUMETRICAS reales; personas proxy v002 fuera, PERSON2 dentro.
"""
import base64
import json
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'FASE_03B9_HYPERDETAIL_V006'))
C3 = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'FASE_03C_VISUALIZACION'))
VIEW = os.path.join(V3, '_viewer')
VIEW_TEX = os.path.join(C3, '_viewer')
BLEND = os.path.join(HERE, 'SOL_FINAL_V006.blend')
ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['build']

CFG = json.load(open(os.path.join(C3, 'atmos_config.json'), encoding='utf-8'))
_camx = os.path.join(HERE, 'cam_final.json')
if os.path.exists(_camx):
    CFG['camaras_hero'] += json.load(open(_camx, encoding='utf-8'))
SUN = json.load(open(os.path.join(HERE, 'SUN_03D.json'), encoding='utf-8'))
M = json.load(open(os.path.join(V3, 'geometria_maestra_v006.json'), encoding='utf-8'))


def set_in(node, names, value):
    for n in names:
        if n in node.inputs:
            node.inputs[n].default_value = value
            return True
    return False


def hexc(h, a=1.0):
    h = h.lstrip('#')

    def lin(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (lin(int(h[0:2], 16)), lin(int(h[2:4], 16)), lin(int(h[4:6], 16)), a)


def principled(name, base, rough=0.6, metal=0.0, transmission=0.0, alpha=1.0,
               emiss=None, emiss_str=0.0, sss=0.0, sss_col=None, ior=1.45):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes['Principled BSDF']
    set_in(p, ['Base Color'], base)
    set_in(p, ['Roughness'], rough)
    set_in(p, ['Metallic'], metal)
    set_in(p, ['Transmission Weight', 'Transmission'], transmission)
    set_in(p, ['Alpha'], alpha)
    set_in(p, ['IOR'], ior)
    if emiss:
        set_in(p, ['Emission Color', 'Emission'], emiss)
        set_in(p, ['Emission Strength'], emiss_str)
    if sss > 0:
        set_in(p, ['Subsurface Weight', 'Subsurface'], sss)
        if sss_col:
            set_in(p, ['Subsurface Radius'], sss_col)
    if transmission > 0.3 or alpha < 1.0:
        try:
            m.surface_render_method = 'BLENDED'
        except AttributeError:
            pass
    return m


def add_tint_variation(mat, amount=0.25):
    """mezcla Base Color con el atributo 'tint' horneado por instancia."""
    nt = mat.node_tree
    p = nt.nodes['Principled BSDF']
    base = p.inputs['Base Color'].default_value[:]
    attr = nt.nodes.new('ShaderNodeVertexColor')
    attr.layer_name = 'tint'
    mixn = nt.nodes.new('ShaderNodeMix')
    mixn.data_type = 'RGBA'
    mixn.inputs['Factor'].default_value = amount
    mixn.inputs[6].default_value = base
    nt.links.new(attr.outputs['Color'], mixn.inputs[7])
    nt.links.new(mixn.outputs[2], p.inputs['Base Color'])


def add_bump_noise(mat, scale=8.0, strength=0.18, detail=4.0):
    nt = mat.node_tree
    p = nt.nodes['Principled BSDF']
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = scale
    nz.inputs['Detail'].default_value = detail
    bp = nt.nodes.new('ShaderNodeBump')
    bp.inputs['Strength'].default_value = strength
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], p.inputs['Normal'])


def datauri_png(uri, name):
    raw = base64.b64decode(uri.split(',', 1)[1])
    p = os.path.join(HERE, name)
    open(p, 'wb').write(raw)
    img = bpy.data.images.load(p)
    img.pack()
    return img


# ============================================================ BUILD
def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'

    # ---------- fuentes ----------
    txt = open(os.path.join(VIEW, 'scene_full.js'), encoding='utf-8').read()
    a = txt.index('const SCENE_MESHES = ') + len('const SCENE_MESHES = ')
    b = txt.index(';\nconst SCENE_LINES')
    MESHES = json.loads(txt[a:b])
    c0 = txt.index('const SCENE_LINES = ') + len('const SCENE_LINES = ')
    LINES = json.loads(txt[c0:txt.index(';', c0)])
    XM, XL = [], []      # v006: scene_full.js ya lo contiene todo (sin capa extra E03)
    tex = open(os.path.join(VIEW_TEX, 'tex_data.js'), encoding='utf-8').read()

    def uri_of(var):
        i = tex.index(var) + len(var)
        i = tex.index('"', i) + 1
        return tex[i:tex.index('"', i)]

    img_col = datauri_png(uri_of('GRAN_COL_URI'), '_gran_col.png')
    img_rgh = datauri_png(uri_of('GRAN_RGH_URI'), '_gran_rgh.png')

    # ---------- materiales ----------
    MAT = {}
    mg = bpy.data.materials.new('GRANITO_SOL')
    mg.use_nodes = True
    ntg = mg.node_tree
    pg = ntg.nodes['Principled BSDF']
    tc = ntg.nodes.new('ShaderNodeTexCoord')
    mp = ntg.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1 / 320, 1 / 220, 1)
    mp.inputs['Location'].default_value = (0.5, 0.5227, 0)
    t1 = ntg.nodes.new('ShaderNodeTexImage'); t1.image = img_col
    t2 = ntg.nodes.new('ShaderNodeTexImage'); t2.image = img_rgh
    t2.image.colorspace_settings.name = 'Non-Color'
    ntg.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    ntg.links.new(mp.outputs['Vector'], t1.inputs['Vector'])
    ntg.links.new(mp.outputs['Vector'], t2.inputs['Vector'])
    ntg.links.new(t1.outputs['Color'], pg.inputs['Base Color'])
    ntg.links.new(t2.outputs['Color'], pg.inputs['Roughness'])
    MAT['GROUND'] = mg

    MAT['CTX'] = principled('CTX_REVOCO', hexc('#D8D0C2'), rough=0.9)
    MAT['CTX_LADRILLO'] = principled('CORREOS_LADRILLO', hexc('#C4907A'), rough=0.75)
    add_bump_noise(MAT['CTX_LADRILLO'], scale=22, strength=0.1)
    MAT['CTX_PIEDRA'] = principled('CORREOS_PIEDRA', hexc('#D9C4A4'), rough=0.65)
    MAT['RELOJ'] = principled('RELOJ', hexc('#F5EFDF'), rough=0.35, emiss=hexc('#F0E6C8'), emiss_str=0.6)
    MAT['BRONCE'] = principled('CARLOS_III_BRONCE', hexc('#3E3A30'), rough=0.38, metal=0.92)
    MAT['PEDESTAL'] = principled('PEDESTAL_GRANITO', hexc('#B8B0A2'), rough=0.7)
    add_bump_noise(MAT['PEDESTAL'], scale=30, strength=0.06)
    MAT['MADERA_P'] = principled('MADERA_PRIMARIA', hexc('#A98F72'), rough=0.48)
    add_bump_noise(MAT['MADERA_P'], scale=3.2, strength=0.08, detail=6)
    MAT['MADERA_S'] = principled('MADERA_SECUNDARIA', hexc('#C0A886'), rough=0.55)
    MAT['DECK'] = principled('DECK_TABLERO', hexc('#8F7355'), rough=0.42)
    add_bump_noise(MAT['DECK'], scale=1.6, strength=0.12, detail=5)
    MAT['CANOPY'] = principled('CANOPY_MEMBRANA', hexc('#D3DD7E'), rough=0.28, transmission=0.55, ior=1.35)
    add_tint_variation(MAT['CANOPY'], 0.22)
    MAT['ALGAS'] = principled('LAMINA_MICROALGAS', hexc('#4A9A72'), rough=0.05, transmission=0.85, ior=1.33)
    MAT['POD'] = principled('POD_TPU', hexc('#F3C4D5'), rough=0.3, transmission=0.6, ior=1.42,
                            sss=0.12, sss_col=(0.9, 0.35, 0.5))
    add_bump_noise(MAT['POD'], scale=6.5, strength=0.22, detail=5)
    add_tint_variation(MAT['POD'], 0.12)
    MAT['ETFE'] = principled('ETFE_CUPULA', hexc('#F2F5EC'), rough=0.12, transmission=0.88, ior=1.4)
    MAT['PLANTER'] = principled('JARDINERA', hexc('#9C8662'), rough=0.8)
    MAT['MOBILIARIO'] = principled('MOBILIARIO', hexc('#B5A084'), rough=0.55)
    MAT['PIPE'] = principled('TUBERIA_ROSA', hexc('#E06B9C'), rough=0.35, metal=0.1)
    MAT['HOJA'] = principled('VEG_HOJA', hexc('#5F9448'), rough=0.55, sss=0.18, sss_col=(0.2, 0.6, 0.2))
    add_tint_variation(MAT['HOJA'], 0.35)
    MAT['TRONCO'] = principled('VEG_TRONCO', hexc('#6E5A44'), rough=0.75)
    add_bump_noise(MAT['TRONCO'], scale=9, strength=0.2)
    MAT['AGUA'] = principled('AGUA', hexc('#DFF2EE'), rough=0.03, transmission=0.95, ior=1.33)
    MAT['AGUA_ALTA'] = principled('AGUA_BALSA', hexc('#4A9A72'), rough=0.06, transmission=0.85, ior=1.33)
    MAT['CHORRO'] = principled('CHORRO', hexc('#EFFFFC'), rough=0.08, transmission=0.9, ior=1.33)
    MAT['ESPUMA'] = principled('ESPUMA', hexc('#FFFFFF'), rough=0.5, alpha=0.55)
    MAT['PERSONA'] = principled('PERSONA', hexc('#8A8078'), rough=0.85)
    add_tint_variation(MAT['PERSONA'], 0.55)
    MAT['CABLE'] = principled('CABLE', hexc('#6E6E6A'), rough=0.4, metal=0.6)

    # ---------- clasificacion y fusion por cubos de material ----------
    def correos_zone(bb):
        return bb[0] > -64 and bb[2] < 20 and bb[1] > -96 and bb[3] < -28

    def estatua_zone(bb):
        return bb[0] > -32 and bb[2] < -24 and bb[1] > -17 and bb[3] < -11

    def key_for(o, bb, zmax, dx, dy, dz):
        lay, nm = o['layer'], o.get('name', o.get('fam', ''))
        if lay == '01_GROUND':
            return 'GROUND'
        if lay == '00_CONTEXT':
            if estatua_zone(bb):
                return 'BRONCE' if zmax > 2.9 else 'PEDESTAL'
            if correos_zone(bb):
                if zmax > 25.5 and dx < 5:
                    return 'RELOJ'
                return 'CTX_PIEDRA' if zmax > 16.5 else 'CTX_LADRILLO'
            return 'CTX'
        if lay == '02_PRIMARY_STRUCTURE':
            return 'DECK' if nm == 'RIBBON_DECK' else 'MADERA_P'
        if lay in ('03_SECONDARY_STRUCTURE', '04_MASTS'):
            return 'MADERA_S'
        if lay == '10_FURNITURE':
            return 'MOBILIARIO'
        if lay == '09_PLANTERS':
            return 'PLANTER'
        if lay == '13_PIPES':
            return 'PIPE'
        if lay == '07_CANOPIES':
            return 'CANOPY'
        if lay == '08_PINK_MODULES':
            return 'POD'
        if lay == '06_MEMBRANES':
            return 'ETFE'
        if lay == '11_WATER':
            return 'AGUA' if zmax < 0.1 else 'AGUA_ALTA'
        if lay in ('14_VEGETATION_PROXY', '15_VEGETATION_FULL'):
            return 'TRONCO' if (dz > 1.6 * max(dx, dy) and max(dx, dy) < 0.9) else 'HOJA'
        return None   # 12_MIST proxy, 16 proxy, 17 metro fuera

    import random
    rnd = random.Random(1926)
    BUF = {}

    def push(key, V, F, tint=None):
        d = BUF.setdefault(key, {'v': [], 'f': [], 'c': []})
        off = len(d['v'])
        d['v'].extend(V)
        d['f'].extend([(a + off, b2 + off, c2 + off) for (a, b2, c2) in F])
        t = tint or (1, 1, 1, 1)
        d['c'].extend([t] * len(V))

    for o in MESHES:
        V = o['V']
        xs = [v[0] for v in V]; ys = [v[1] for v in V]; zs = [v[2] for v in V]
        bb = (min(xs), min(ys), max(xs), max(ys))
        k = key_for(o, bb, max(zs), max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
        if not k:
            continue
        tint = None
        if k in ('HOJA', 'CANOPY', 'POD'):
            h = rnd.uniform(-1, 1)
            if k == 'HOJA':
                tint = (0.05 + 0.09 * rnd.random(), 0.16 + 0.14 * rnd.random(), 0.035 + 0.05 * rnd.random(), 1)
            elif k == 'CANOPY':
                tint = (0.5 + 0.16 * h, 0.68, 0.14 + 0.08 * rnd.random(), 1)
            else:
                tint = (0.88, 0.44 + 0.12 * h, 0.62, 1)
        push(k, V, o['F'], tint)

    for o in XM:
        col = hexc(o['color'])
        if o.get('layer') == '18_PEOPLE2':
            push('PERSONA', o['V'], o['F'], col)
        elif o['op'] < 0.7 and o['rough'] < 0.2:
            push('CHORRO', o['V'], o['F'])
        elif o['color'] == '#FFFFFF':
            push('ESPUMA', o['V'], o['F'])
        elif o['color'] == '#E06B9C':
            push('PIPE', o['V'], o['F'])
        else:
            push('CHORRO', o['V'], o['F'])

    col_main = bpy.data.collections.new('SOL_03D')
    sc.collection.children.link(col_main)
    for k, d in BUF.items():
        me = bpy.data.meshes.new(k)
        me.from_pydata(d['v'], [], d['f'])
        me.update()
        ca = me.color_attributes.new(name='tint', type='FLOAT_COLOR', domain='POINT')
        for i, cval in enumerate(d['c']):
            ca.data[i].color = cval
        ob = bpy.data.objects.new(k, me)
        ob.data.materials.append(MAT[k])
        col_main.objects.link(ob)
        if k in ('POD', 'PERSONA', 'HOJA'):
            for p2 in me.polygons:
                p2.use_smooth = True

    # cables + goteo como curvas finas
    def curveset(name, segs, radius, mat):
        cu = bpy.data.curves.new(name, 'CURVE')
        cu.dimensions = '3D'
        cu.bevel_depth = radius
        cu.bevel_resolution = 2
        for (p0, p1) in segs:
            sp = cu.splines.new('POLY')
            sp.points.add(1)
            sp.points[0].co = (*p0, 1)
            sp.points[1].co = (*p1, 1)
        ob = bpy.data.objects.new(name, cu)
        ob.data.materials.append(mat)
        col_main.objects.link(ob)

    curveset('CABLES', [(l['pts'][i], l['pts'][i + 1]) for l in LINES for i in range(len(l['pts']) - 1)],
             0.008, MAT['CABLE'])
    curveset('GOTEO', [(l['a'], l['b']) for l in XL], 0.006, MAT['CHORRO'])

    # ---------- niebla y columnas como VOLUMENES reales ----------
    mvol = bpy.data.materials.new('NIEBLA_VOL')
    mvol.use_nodes = True
    nt = mvol.node_tree
    nt.nodes.remove(nt.nodes['Principled BSDF'])
    pv = nt.nodes.new('ShaderNodeVolumePrincipled')
    pv.inputs['Color'].default_value = hexc('#EAF6F2')
    pv.inputs['Density'].default_value = 0.05
    set_in(pv, ['Anisotropy'], 0.55)
    nt.links.new(pv.outputs['Volume'], nt.nodes['Material Output'].inputs['Volume'])
    mcol = mvol.copy(); mcol.name = 'COLUMNA_VOL'
    mcol.node_tree.nodes['Principled Volume'].inputs['Density'].default_value = 0.028

    def vol_sphere(name, x, y, z, r, rz, mat):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=1, location=(x, y, z))
        ob = bpy.context.active_object
        ob.name = name
        ob.scale = (r, r, rz)
        ob.data.materials.append(mat)
        ob.visible_shadow = False

    a4 = json.load(open(os.path.join(V3, '_reaudit9', '_data', 'a4_ribbon.json'), encoding='utf-8'))
    PROF = [(r['x'], r['y']) for r in a4['prof']]
    for i, (nx, ny) in enumerate(M['agua_clima']['nebul']):
        vol_sphere('NEB_%02d' % i, nx + 0.4, ny, 2.2, 2.0, 2.2, mvol)
    n8 = max(len(PROF) // 8, 1)
    for j, i in enumerate(range(len(PROF) // 16, len(PROF) - 1, n8)):
        if j >= 8:
            break
        vol_sphere('RIBNEB_%d' % j, PROF[i][0], PROF[i][1], 7.0, 1.5, 1.1, mvol)
    for j, (ccx, ccy) in enumerate(CFG['niebla']['columnas_h7']['centros']):
        vol_sphere('COLUMNA_%d' % j, ccx, ccy, 12.0, 3.4, 7.5, mcol)

    # ---------- mundo: cielo Nishita + perspectiva aerea ----------
    w = bpy.data.worlds.new('CIELO')
    sc.world = w
    w.use_nodes = True
    wn = w.node_tree
    sky = wn.nodes.new('ShaderNodeTexSky')
    for st in ('MULTIPLE_SCATTERING', 'NISHITA', 'HOSEK_WILKIE'):
        try:
            sky.sky_type = st
            break
        except TypeError:
            continue
    for attr, val in (('sun_intensity', 0.15), ('altitude', 650)):
        try:
            setattr(sky, attr, val)
        except (AttributeError, TypeError):
            pass
    bgn = wn.nodes['Background']
    bgn.inputs['Strength'].default_value = 0.38
    wn.links.new(sky.outputs['Color'], bgn.inputs['Color'])
    # perspectiva aerea como volumen ACOTADO (el volumen de mundo infinito rinde negro en 5.0)
    matm = bpy.data.materials.new('ATMOSFERA_VOL')
    matm.use_nodes = True
    ntA = matm.node_tree
    ntA.nodes.remove(ntA.nodes['Principled BSDF'])
    pva = ntA.nodes.new('ShaderNodeVolumePrincipled')
    pva.inputs['Color'].default_value = hexc('#F2EFE7')
    pva.inputs['Density'].default_value = 0.00045
    set_in(pva, ['Anisotropy'], 0.35)
    ntA.links.new(pva.outputs['Volume'], ntA.nodes['Material Output'].inputs['Volume'])
    bpy.ops.mesh.primitive_cube_add(location=(0, 5, 29))
    atm = bpy.context.active_object
    atm.name = 'ATMOSFERA'
    atm.scale = (230, 175, 30)
    atm.data.materials.append(matm)
    atm.visible_shadow = False

    lamp = bpy.data.lights.new('SOL', 'SUN')
    lamp.energy = 4.0
    lamp.angle = math.radians(0.53)
    lo = bpy.data.objects.new('SOL', lamp)
    sc.collection.objects.link(lo)

    # ---------- camaras ----------
    for c in CFG['camaras_hero']:
        cam = bpy.data.cameras.new(c['id'])
        cam.sensor_fit = 'VERTICAL'
        cam.angle_y = math.radians(c['fov'])          # three.js PerspectiveCamera.fov es VERTICAL
        cam.clip_end = 1200
        cam.dof.use_dof = True
        cam.dof.aperture_fstop = 8.0
        co = bpy.data.objects.new('CAM_' + c['id'], cam)
        co.location = c['cam']
        tgt = bpy.data.objects.new('TGT_' + c['id'], None)
        tgt.location = c['tgt']
        sc.collection.objects.link(co)
        sc.collection.objects.link(tgt)
        tr = co.constraints.new('TRACK_TO')
        tr.target = tgt
        tr.track_axis = 'TRACK_NEGATIVE_Z'
        tr.up_axis = 'UP_Y'
        cam.dof.focus_object = tgt

    # ---------- render base ----------
    cy = sc.cycles
    cy.samples = 160
    cy.use_adaptive_sampling = True
    cy.use_denoising = True
    cy.max_bounces = 8
    cy.transmission_bounces = 8
    cy.volume_bounces = 1
    cy.sample_clamp_indirect = 8.0
    sc.render.resolution_x, sc.render.resolution_y = CFG.get('resolucion_hero', [2560, 1600])
    sc.view_settings.view_transform = 'AgX'
    for lk in ('AgX - Punchy', 'Punchy', 'AgX - Base Contrast'):
        try:
            sc.view_settings.look = lk
            break
        except TypeError:
            continue
    prefs = bpy.context.preferences.addons['cycles'].preferences
    for dtype in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI'):
        try:
            prefs.compute_device_type = dtype
            prefs.get_devices()
            if any(d.type != 'CPU' for d in prefs.devices):
                for d in prefs.devices:
                    d.use = True
                cy.device = 'GPU'
                print('GPU:', dtype, [d.name for d in prefs.devices if d.type != 'CPU'])
                break
        except Exception:
            continue
    bpy.ops.wm.save_as_mainfile(filepath=BLEND, compress=True)
    print('BUILD OK ->', BLEND, '· objetos:', len(list(sc.collection.all_objects)))


# ============================================================ RENDER
def apply_clay(sc):
    m = bpy.data.materials.get('CLAY') or bpy.data.materials.new('CLAY')
    m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (0.82, 0.80, 0.76, 1)
    p.inputs['Roughness'].default_value = 0.9
    sc.view_layers[0].material_override = m


def apply_luz(sc, luz):
    s = SUN[luz]
    el, az = math.radians(s['elevacion']), math.radians(s['azimut_N_E'])
    lo = bpy.data.objects['SOL']
    d = Vector((math.cos(el) * math.sin(az), math.cos(el) * math.cos(az), math.sin(el)))
    lo.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    lo.data.energy = 3.2 if luz == 'mediodia' else 2.2
    lo.data.color = (1.0, 0.95, 0.86) if luz == 'mediodia' else (1.0, 0.80, 0.58)
    for n in sc.world.node_tree.nodes:
        if n.bl_idname == 'ShaderNodeTexSky':
            n.sun_elevation = el
            n.sun_rotation = math.pi - az
    sc.view_settings.exposure = -0.35 if luz == 'mediodia' else -0.45


def render(sel, luces, w=None, h=None, samples=None):
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sc = bpy.context.scene
    if w:
        sc.render.resolution_x, sc.render.resolution_y = int(w), int(h)
    if samples:
        sc.cycles.samples = int(samples)
    out = os.path.join(HERE, 'hero_FINAL')
    os.makedirs(out, exist_ok=True)
    ids = [c['id'] for c in CFG['camaras_hero']] if sel == 'all' else [sel]
    for cid in ids:
        for luz in (('mediodia', 'tarde') if luces == 'both' else [luces]):  # o 'clay'
            sc.camera = bpy.data.objects['CAM_' + cid]
            if luz == 'clay':
                apply_luz(sc, 'tarde')
                apply_clay(sc)
            else:
                apply_luz(sc, luz)
            sc.render.filepath = os.path.join(out, '%s_%s.png' % (cid, luz))
            bpy.ops.render.render(write_still=True)
            print('RENDER OK', cid, luz)


if ARGS[0] == 'build':
    build()
elif ARGS[0] == 'render':
    render(ARGS[1], ARGS[2], *(ARGS[3:6] or []))
