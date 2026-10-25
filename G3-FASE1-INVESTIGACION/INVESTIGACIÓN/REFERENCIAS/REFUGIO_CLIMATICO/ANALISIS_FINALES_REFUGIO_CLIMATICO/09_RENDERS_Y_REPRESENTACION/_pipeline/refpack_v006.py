# -*- coding: utf-8 -*-
"""REFERENCE PACKS v006 — el 3D como base de control geometrico para imagenes IA.

Passes por OVERRIDE DE SHADER (independiente de la API del compositor):
  beauty.png       materiales base, luz tarde PSA                      96 smp
  clay.png         override neutro (lectura volumetrica)               64 smp
  clay_sinveg.png  clay sin vegetacion/personas (estructura pura)      64 smp
  depth.png        profundidad de camara 0-250 m (cerca=claro)          1 smp
  normal.png       normales en espacio de camara 0-1                    1 smp
  ao.png           oclusion ambiental pura                             32 smp
  id_mat.png       familias de material como grises (mascaras)          1 smp
Uso: blender -b -P refpack_v006.py -- pack <CAM> [w h]
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
BLEND = os.path.join(HERE, 'SOL_FINAL_V006.blend')
ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
sys.path.insert(0, HERE)

FAM_IDX = [('GRANITO', 1), ('VEG_', 2), ('ROSA', 3), ('POD', 3), ('TPU', 3),
           ('AGUA', 4), ('CTX', 5), ('CORREOS', 5), ('MADERA', 6), ('COLUMNA', 6),
           ('CANOPY', 7), ('ETFE', 7), ('PERSON', 8), ('BRONCE', 10), ('RELOJ', 10),
           ('PEDESTAL', 10), ('MOBILIARIO', 11), ('JARDINERA', 12), ('NIEBLA', 14),
           ('ATMOSFERA', 14)]


def _emission_mat(name):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    outp = nt.nodes.new('ShaderNodeOutputMaterial')
    em = nt.nodes.new('ShaderNodeEmission')
    nt.links.new(em.outputs['Emission'], outp.inputs['Surface'])
    return m, nt, em


def mat_depth():
    m, nt, em = _emission_mat('PASS_DEPTH')
    cam = nt.nodes.new('ShaderNodeCameraData')
    mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value = 0.0
    mr.inputs['From Max'].default_value = 250.0
    mr.inputs['To Min'].default_value = 1.0
    mr.inputs['To Max'].default_value = 0.0
    mr.clamp = True
    nt.links.new(cam.outputs['View Z Depth'], mr.inputs['Value'])
    nt.links.new(mr.outputs['Result'], em.inputs['Color'])
    return m


def mat_normal():
    m, nt, em = _emission_mat('PASS_NORMAL')
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    tr = nt.nodes.new('ShaderNodeVectorTransform')
    tr.vector_type = 'NORMAL'
    tr.convert_from = 'WORLD'
    tr.convert_to = 'CAMERA'
    mul = nt.nodes.new('ShaderNodeVectorMath'); mul.operation = 'MULTIPLY_ADD'
    mul.inputs[1].default_value = (0.5, 0.5, 0.5)
    mul.inputs[2].default_value = (0.5, 0.5, 0.5)
    nt.links.new(geo.outputs['Normal'], tr.inputs['Vector'])
    nt.links.new(tr.outputs['Vector'], mul.inputs[0])
    nt.links.new(mul.outputs['Vector'], em.inputs['Color'])
    return m


def mat_ao():
    m, nt, em = _emission_mat('PASS_AO')
    ao = nt.nodes.new('ShaderNodeAmbientOcclusion')
    ao.inputs['Distance'].default_value = 3.0
    nt.links.new(ao.outputs['Color'], em.inputs['Color'])
    return m


def mat_clay():
    m = bpy.data.materials.get('CLAY') or bpy.data.materials.new('CLAY')
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    if p is None:
        m.node_tree.nodes.clear()
        outp = m.node_tree.nodes.new('ShaderNodeOutputMaterial')
        p = m.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        m.node_tree.links.new(p.outputs[0], outp.inputs['Surface'])
    p.inputs['Base Color'].default_value = (0.82, 0.80, 0.76, 1)
    p.inputs['Roughness'].default_value = 0.9
    return m


def hide_veg(on=True):
    """Oculta la VEGETACION (material VEG_*) y personas; las jardineras se quedan."""
    n = 0
    for o in bpy.data.objects:
        if o.type != 'MESH':
            continue
        mat = o.active_material.name.upper() if o.active_material else ''
        if mat.startswith('VEG_') or 'PERSON' in mat or 'PERSON' in o.name.upper():
            o.hide_render = on
            n += 1
    return n


def hide_vols(on=True):
    """Oculta volumetricas (niebla/atmosfera/columnas de luz) en los passes de datos."""
    n = 0
    for o in bpy.data.objects:
        if o.type != 'MESH':
            continue
        mat = o.active_material.name.upper() if o.active_material else ''
        if mat.endswith('_VOL'):
            o.hide_render = on
            n += 1
    return n


def world_black():
    w = bpy.context.scene.world
    if w and w.use_nodes:
        bg = w.node_tree.nodes.get('Background')
        if bg:
            bg.inputs[0].default_value = (0, 0, 0, 1)
            bg.inputs[1].default_value = 0.0


def render_to(sc, path, samples, data_pass=False):
    sc.cycles.samples = samples
    sc.cycles.use_denoising = not data_pass
    sc.view_settings.view_transform = 'Standard' if data_pass else 'AgX'
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print('  saved', os.path.basename(path), flush=True)


def pack(cam, w=1920, h=1200):
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    import bl_scene_v006 as B
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = int(w), int(h)
    sc.camera = bpy.data.objects['CAM_' + cam]
    B.apply_luz(sc, 'tarde')
    outdir = os.path.join(HERE, 'refpacks', cam)
    os.makedirs(outdir, exist_ok=True)
    vl = sc.view_layers[0]

    # 1 · beauty neutro
    render_to(sc, os.path.join(outdir, 'beauty.png'), 96)
    # 2 · clay
    vl.material_override = mat_clay()
    render_to(sc, os.path.join(outdir, 'clay.png'), 64)
    # 3 · clay sin vegetacion/personas
    n = hide_veg(True)
    render_to(sc, os.path.join(outdir, 'clay_sinveg.png'), 64)
    hide_veg(False)
    # 4-7 · passes de datos: sin volumetricas y con mundo negro
    hide_vols(True)
    world_black()
    vl.material_override = mat_ao()
    render_to(sc, os.path.join(outdir, 'ao.png'), 32)
    # 5 · depth
    vl.material_override = mat_depth()
    render_to(sc, os.path.join(outdir, 'depth.png'), 1, data_pass=True)
    # 6 · normal
    vl.material_override = mat_normal()
    render_to(sc, os.path.join(outdir, 'normal.png'), 1, data_pass=True)
    # 7 · id_mat: REESCRIBE los materiales como emision plana (ultimo pase; no se guarda)
    vl.material_override = None
    for m in bpy.data.materials:
        if m.name.startswith('PASS_') or m.name == 'CLAY':
            continue
        idx = next((i for k, i in FAM_IDX if k in m.name.upper()), 15)
        m.use_nodes = True
        nt = m.node_tree
        nt.nodes.clear()
        outp = nt.nodes.new('ShaderNodeOutputMaterial')
        em = nt.nodes.new('ShaderNodeEmission')
        g = idx / 15.0
        em.inputs['Color'].default_value = (g, g, g, 1)
        nt.links.new(em.outputs['Emission'], outp.inputs['Surface'])
    render_to(sc, os.path.join(outdir, 'id_mat.png'), 1, data_pass=True)
    hide_vols(False)
    print('PACK OK %s (%d objetos vegetales en variante sinveg)' % (cam, n), flush=True)


if ARGS and ARGS[0] == 'pack':
    extra = [int(a) for a in ARGS[2:4]]
    pack(ARGS[1], *extra)
