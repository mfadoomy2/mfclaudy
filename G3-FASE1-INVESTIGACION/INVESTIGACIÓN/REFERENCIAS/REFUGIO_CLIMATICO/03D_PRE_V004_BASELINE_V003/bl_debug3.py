# -*- coding: utf-8 -*-
import os

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, 'SOL_03D.blend'))
sc = bpy.context.scene
sc.camera = bpy.data.objects['CAM_H5']
sc.render.resolution_x, sc.render.resolution_y = 480, 300
sc.view_settings.view_transform = 'Standard'

# 1) WORKBENCH: la camara ve geometria?
sc.render.engine = 'BLENDER_WORKBENCH'
sc.render.filepath = os.path.join(HERE, '_dbg_wb.png')
bpy.ops.render.render(write_still=True)
print('wb ok')

# 2) CYCLES CPU sin volumenes (mundo sin Volume, esferas de niebla fuera)
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = 12
out = sc.world.node_tree.nodes['World Output']
for l in list(sc.world.node_tree.links):
    if l.to_node == out and l.to_socket.name == 'Volume':
        sc.world.node_tree.links.remove(l)
for ob in list(sc.collection.all_objects):
    if ob.name.startswith(('NEB_', 'RIBNEB_', 'COLUMNA_')):
        ob.hide_render = True
sc.render.filepath = os.path.join(HERE, '_dbg_novol.png')
bpy.ops.render.render(write_still=True)
print('novol ok')

# 3) sky: parametros reales
for n in sc.world.node_tree.nodes:
    if n.bl_idname == 'ShaderNodeTexSky':
        print('sky type', n.sky_type, 'elev', getattr(n, 'sun_elevation', None),
              'rot', getattr(n, 'sun_rotation', None), 'int', getattr(n, 'sun_intensity', None))
