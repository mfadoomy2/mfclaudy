# -*- coding: utf-8 -*-
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, 'SOL_03D.blend'))
sc = bpy.context.scene
dg = bpy.context.evaluated_depsgraph_get()
cam = bpy.data.objects['CAM_H5'].evaluated_get(dg)
print('CAM_H5 loc', tuple(round(v, 2) for v in cam.matrix_world.translation))
fwd = cam.matrix_world.to_quaternion() @ Vector((0, 0, -1))
print('CAM_H5 fwd', tuple(round(v, 2) for v in fwd))
lo = bpy.data.objects['SOL']
print('SOL rot', tuple(round(math.degrees(a), 1) for a in lo.rotation_euler), 'energy', lo.data.energy)
w = sc.world
print('world nodes:', [n.bl_idname for n in w.node_tree.nodes])
out = w.node_tree.nodes.get('World Output')
print('world surface linked:', bool(out and out.inputs['Surface'].is_linked),
      'volume linked:', bool(out and out.inputs['Volume'].is_linked))
print('view_transform', sc.view_settings.view_transform, 'look', sc.view_settings.look)
print('device', sc.cycles.device, 'samples', sc.cycles.samples)
print('n objetos', len(sc.collection.all_objects), 'materiales', len(bpy.data.materials))
g = bpy.data.objects.get('GROUND')
print('GROUND verts', len(g.data.vertices) if g else None)
# render CPU minimo
sc.cycles.device = 'CPU'
sc.cycles.samples = 12
sc.render.resolution_x, sc.render.resolution_y = 480, 300
sc.camera = bpy.data.objects['CAM_H5']
sc.render.filepath = os.path.join(HERE, '_dbg_cpu.png')
bpy.ops.render.render(write_still=True)
print('render cpu ok')
