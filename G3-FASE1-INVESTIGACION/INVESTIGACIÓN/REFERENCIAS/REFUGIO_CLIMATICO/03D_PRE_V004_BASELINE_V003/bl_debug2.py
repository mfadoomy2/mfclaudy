# -*- coding: utf-8 -*-
import os

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, 'SOL_03D.blend'))
sc = bpy.context.scene
# sonda: esfera emisiva de 6 m delante de la camara H5
me = bpy.data.meshes.new('probe')
import bmesh
bm = bmesh.new()
bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=8, radius=6)
bm.to_mesh(me)
ob = bpy.data.objects.new('PROBE', me)
ob.location = (0, 27, 7)
mp = bpy.data.materials.new('PROBE_EM')
mp.use_nodes = True
p = mp.node_tree.nodes['Principled BSDF']
p.inputs['Emission Strength'].default_value = 5.0
p.inputs['Emission Color'].default_value = (1, 0.2, 0.6, 1)
ob.data.materials.append(mp)
sc.collection.objects.link(ob)
# mundo sin volumen + transform estandar
out = sc.world.node_tree.nodes['World Output']
for l in list(sc.world.node_tree.links):
    if l.to_node == out and l.to_socket.name == 'Volume':
        sc.world.node_tree.links.remove(l)
sc.view_settings.view_transform = 'Standard'
sc.cycles.device = 'CPU'
sc.cycles.samples = 12
sc.render.resolution_x, sc.render.resolution_y = 480, 300
sc.camera = bpy.data.objects['CAM_H5']
sc.render.filepath = os.path.join(HERE, '_dbg2.png')
bpy.ops.render.render(write_still=True)
print('probe render ok · film_transparent =', sc.render.film_transparent)
