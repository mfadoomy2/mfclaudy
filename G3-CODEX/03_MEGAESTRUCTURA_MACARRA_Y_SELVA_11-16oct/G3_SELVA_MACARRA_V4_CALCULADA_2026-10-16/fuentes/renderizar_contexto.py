from pathlib import Path
import bpy,json,math
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'modelos/SELVA_MACARRA_V4_RENDER.blend'))
for ob in bpy.data.objects:
 if ob.name.startswith('90_CONTEXTO'):
  ob.hide_render=False
  for mat in ob.data.materials:
   bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.64,.65,.63,1);bs.inputs['Roughness'].default_value=.9
p=json.loads((R/'fuentes/parcela_local.geojson').read_text())['geometry']['coordinates'][0]
mat=bpy.data.materials.new('Limite de parcela');mat.diffuse_color=(.8,.025,.17,1);mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.8,.025,.17,1)
cu=bpy.data.curves.new('LIMITE PARCELA','CURVE');cu.dimensions='3D';cu.bevel_depth=.07;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(len(p)-1)
for pt,q in zip(sp.points,p):pt.co=(q[0],q[1],.1,1)
ob=bpy.data.objects.new('LIMITE PARCELA',cu);bpy.context.collection.objects.link(ob);ob.data.materials.append(mat)
scene=bpy.context.scene;scene.cycles.samples=16;scene.render.resolution_x=2400;scene.render.resolution_y=1800
cam=scene.camera
for name,loc,tgt,scale in [('09_IMPLANTACION_CONTEXTO',(110,-100,110),(41,4,12),105),('10_PARCELA_CENITAL',(37,3,150),(37,3,0),85)]:
 cam.location=loc;cam.rotation_euler=(Vector(tgt)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
 scene.render.filepath=str(R/'vistas'/ (name+'.png'));bpy.ops.render.render(write_still=True);print('RENDER',name,flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'modelos/SELVA_MACARRA_V4_CONTEXTO.blend'))
