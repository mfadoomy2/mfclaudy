from pathlib import Path
import bpy,math,pickle,gzip,json,sys,time
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'vistas';OUT.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
with gzip.open(ROOT/'modelo/geometria_render.pkl.gz','rb') as f:data=pickle.load(f)
materials={}
for layer,color in data['colors'].items():
 m=bpy.data.materials.new(layer);m.diffuse_color=(*[c/255 for c in color],1);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*[c/255 for c in color],1);bs.inputs['Roughness'].default_value=.37;bs.inputs['Metallic'].default_value=.23
 if layer.startswith(('01','06','07','08','15')):bs.inputs['Roughness'].default_value=.69;bs.inputs['Metallic'].default_value=.05
 if layer.startswith(('10','13')):
  bs.inputs['Metallic'].default_value=.03;bs.inputs['Roughness'].default_value=.16
  mix=m.node_tree.nodes.new('ShaderNodeMixShader');trans=m.node_tree.nodes.new('ShaderNodeBsdfTransparent');out=m.node_tree.nodes.get('Material Output');mix.inputs[0].default_value=.26 if layer.startswith('10') else .42;m.node_tree.links.new(bs.outputs['BSDF'],mix.inputs[1]);m.node_tree.links.new(trans.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],out.inputs['Surface'])
 if layer.startswith(('11','18')):
  bs.inputs['Emission Color'].default_value=(*[c/255 for c in color],1);bs.inputs['Emission Strength'].default_value=.13 if layer.startswith('11') else .5
 materials[layer]=m
for k,b in data['batches'].items():
 if not len(b['f']):continue
 me=bpy.data.meshes.new(b['name']);me.from_pydata(b['v'].tolist(),[],b['f'].tolist());me.materials.append(materials[b['layer']]);me.update();ob=bpy.data.objects.new(k,me);bpy.context.collection.objects.link(ob)
 if b['layer'] not in ['01_SUELOS_HABITABLES','03_ESCALERAS_PELDANOS','04_DESCANSILLOS']:
  for p in me.polygons:p.use_smooth=True
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.cycles.max_bounces=6;scene.cycles.transparent_max_bounces=8
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False;scene.world.color=(.0,.0,.0);scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.14,.17,.19,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.25
# A camera-ray black world keeps environmental fill illumination.
nt=scene.world.node_tree;bg=nt.nodes['Background'];out=nt.nodes['World Output'];black=nt.nodes.new('ShaderNodeBackground');black.inputs[0].default_value=(.004,.006,.007,1);black.inputs[1].default_value=1;lp=nt.nodes.new('ShaderNodeLightPath');mix=nt.nodes.new('ShaderNodeMixShader');nt.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);nt.links.new(bg.outputs[0],mix.inputs[1]);nt.links.new(black.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs[0])
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.2
for name,loc,power,size,color in [('KEY',(15,-45,108),32000,65,(1,.95,.84)),('FILL',(-60,-18,60),19000,50,(.71,.90,1)),('RIM',(35,65,90),42000,45,(.84,1,.90))]:
 la=bpy.data.lights.new(name,'AREA');la.energy=power;la.shape='DISK';la.size=size;la.color=color;ob=bpy.data.objects.new(name,la);scene.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector((0,3,25))-ob.location).to_track_quat('-Z','Y').to_euler()
camdata=bpy.data.cameras.new('CAMARA');cam=bpy.data.objects.new('CAMARA',camdata);scene.collection.objects.link(cam);scene.camera=cam;camdata.type='ORTHO';camdata.lens=42;camdata.clip_end=1000
views=[('01_AXONOMETRIA_GENERAL',(116,-142,97),(0,3,24),112),('02_REVERSO',(-112,105,86),(0,3,24),111),('03_PLANTA',(0,3,190),(0,3,20),112),('04_DETALLE_HABITADO',(51,-62,50),(12,-3,22),49),('05_ALZADO',(0,-180,29),(0,3,29),113)]
preview='--preview' in sys.argv
for name,eye,target,scale in (views[:1] if preview else views):
 cam.location=eye;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();camdata.ortho_scale=scale;scene.render.resolution_x=1200 if preview else 2800;scene.render.resolution_y=900 if preview else 2100;scene.render.resolution_percentage=100;scene.cycles.samples=8 if preview else 32
 scene.render.filepath=str(OUT/('PREVIA.png' if preview else name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
 if not preview and name=='01_AXONOMETRIA_GENERAL':bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'modelo/MEGAESTRUCTURA_MACARRA.blend'))
# Let the Python process exit normally without bpy shutdown segfault being treated as asset failure.
print('DONE',flush=True)
