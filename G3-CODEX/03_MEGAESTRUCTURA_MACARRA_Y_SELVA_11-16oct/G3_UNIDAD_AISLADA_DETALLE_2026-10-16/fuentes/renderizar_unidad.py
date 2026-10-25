from pathlib import Path
import bpy,json,math,sys
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
a=json.loads((R/'fuentes/geometria_unidad.json').read_text())
for key,b in a.items():
 m=bpy.data.materials.new(b['layer']+key);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*b['color'],1);bs.inputs['Roughness'].default_value=.48;bs.inputs['Metallic'].default_value=.12
 if 'ESTRUCTURA' in b['layer']:bs.inputs['Roughness'].default_value=.32
 if b['alpha']>.01 or 'VIDRIO' in b['layer']:
  mix=m.node_tree.nodes.new('ShaderNodeMixShader');tr=m.node_tree.nodes.new('ShaderNodeBsdfTransparent');out=m.node_tree.nodes.get('Material Output');mix.inputs[0].default_value=.94 if 'VIDRIO' in b['layer'] else b['alpha'];m.node_tree.links.new(bs.outputs['BSDF'],mix.inputs[1]);m.node_tree.links.new(tr.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],out.inputs['Surface'])
 if 'ILUMINACION' in b['layer']:bs.inputs['Emission Color'].default_value=(1,.75,.4,1);bs.inputs['Emission Strength'].default_value=.8
 me=bpy.data.meshes.new(key);me.from_pydata(b['vertices'],[],b['faces']);me.materials.append(m);me.update();ob=bpy.data.objects.new(b['layer']+key,me);bpy.context.collection.objects.link(ob)
 if any(t in b['layer'] for t in ['RAMAS','COSTILLAS','PERSONAS','VEGETACION','ACCESORIOS']):
  for p in me.polygons:p.use_smooth=True
 ob['Rhino_source']='UNIDAD_P02_DETALLADA.3dm'
 if b['layer']=='90_CONTEXTO':ob.hide_render=True
 del b['vertices'];del b['faces']
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.cycles.max_bounces=6;scene.cycles.transparent_max_bounces=12
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.94,.93,.89,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.35
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False;scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=0
for name,loc,power,size in [('KEY',(15,-30,50),13000,35),('FILL',(65,-20,40),7000,30),('RIM',(35,35,60),18000,35)]:
 l=bpy.data.lights.new(name,'AREA');l.energy=power;l.shape='DISK';l.size=size;o=bpy.data.objects.new(name,l);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((35,0,10))-o.location).to_track_quat('-Z','Y').to_euler()
ca=bpy.data.cameras.new('CAMARA');cam=bpy.data.objects.new('CAMARA',ca);scene.collection.objects.link(cam);scene.camera=cam;ca.type='ORTHO';ca.clip_end=500
views=[('01_UNIDAD_COMPLETA',(18,-22,14),(0,2.4,1.8),17),('02_INTERIOR_ABIERTO',(10,-15,16),(0,3.1,1),14),('03_PLANTA_AMUEBLADA',(0,3.0,30),(0,3,0),13.8),('04_DETALLE_TERRAZA',(10,-9,4),(2.4,.4,.4),7.0)]
preview='--preview' in sys.argv
for name,loc,tgt,sc in (views[:1] if preview else views):
 for ob in bpy.data.objects:
  if ob.type=='MESH' and any(q in ob.name for q in ['06_VELAS','12_CUBIERTAS','14_VIDRIOS','13_COSTILLAS','05_CABLES']):ob.hide_render=(name in ['02_INTERIOR_ABIERTO','03_PLANTA_AMUEBLADA'])
 cam.location=loc;cam.rotation_euler=(Vector(tgt)-cam.location).to_track_quat('-Z','Y').to_euler();ca.ortho_scale=sc
 scene.render.resolution_x=1400 if preview else 2600;scene.render.resolution_y=1000 if preview else 1850;scene.render.resolution_percentage=100;scene.cycles.samples=8 if preview else 24
 scene.render.filepath=str(R/'vistas'/('PREVIA_V4.png' if preview else name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'modelos/SELVA_MACARRA_V4_RENDER.blend'))
print('DONE',flush=True)
