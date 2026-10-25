from pathlib import Path
import bpy,json,math,sys
from mathutils import Vector
P=Path(__file__).resolve().parents[1]
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
codes=args or ['E01_ENCUENTRO','E02_COMUNA','E03_DOS_CLAROS']
TOP=['09_MEMBRANAS','17_CUBIERTA_TERMICA','18_LUCERNARIOS','08_COSTILLAS','10_CABLES']
for code in codes:
 data=json.loads((P/'fuentes'/(code+'_render.json')).read_text())
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 colors=data['colors'];groups={}
 for o in data['objects']:
  if not o['faces']:continue
  key=o['layer'];b=groups.setdefault(key,{'v':[],'f':[]});n=len(b['v']);b['v']+=o['vertices'];b['f'] += [[i+n for i in face] for face in o['faces']]
 for key,g in groups.items():
  mat=bpy.data.materials.new(key);mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');c=colors[key];bs.inputs['Base Color'].default_value=tuple((a/255)**2.2 for a in c)+(1,);bs.inputs['Roughness'].default_value=.55;bs.inputs['Metallic'].default_value=.48 if key in ['07_ACERO','10_CABLES','13_METAL'] else .0
  if key in ['06_VIDRIO','90_CONTEXTO','18_LUCERNARIOS']:
   mix=mat.node_tree.nodes.new('ShaderNodeMixShader');tr=mat.node_tree.nodes.new('ShaderNodeBsdfTransparent');out=mat.node_tree.nodes.get('Material Output');mix.inputs[0].default_value=.91 if key=='06_VIDRIO' else .80 if key=='90_CONTEXTO' else .4;mat.node_tree.links.new(bs.outputs['BSDF'],mix.inputs[1]);mat.node_tree.links.new(tr.outputs[0],mix.inputs[2]);mat.node_tree.links.new(mix.outputs[0],out.inputs['Surface'])
  if key=='09_MEMBRANAS':bs.inputs['Roughness'].default_value=.8;bs.inputs['Subsurface Weight'].default_value=.1
  me=bpy.data.meshes.new(key);me.from_pydata(g['v'],[],g['f']);me.materials.append(mat);me.update();ob=bpy.data.objects.new(key,me);bpy.context.collection.objects.link(ob)
  if key in ['08_COSTILLAS','10_CABLES','11_ENERGIA','12_AGUA','16_PERSONAS']:
   for p in me.polygons:p.use_smooth=True
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.cycles.max_bounces=5;scene.cycles.transparent_max_bounces=12
 scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.88,.88,.84,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.7
 scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX';scene.render.film_transparent=False
 x,y,X,Y=data['bounds'];cx=(x+X)/2;cy=(y+Y)/2;span=max(X-x,Y-y)
 # Ground plane supports the model in the visual; floor remains Z=0 in CAD.
 bpy.ops.mesh.primitive_plane_add(size=span*12,location=(cx,cy,-.20 if data['site'] else -.70));ground=bpy.context.object;mat=bpy.data.materials.new('Fondo');mat.diffuse_color=(.78,.77,.72,1);ground.data.materials.append(mat)
 for name,loc,power,size in [('Key',(cx-span*.3,cy-span*.7,span*1.3),span*span*25,span*1.2),('Fill',(cx+span,cy+span,span),span*span*18,span)]:
  l=bpy.data.lights.new(name,'AREA');l.energy=power;l.size=size;o=bpy.data.objects.new(name,l);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((cx,cy,0))-o.location).to_track_quat('-Z','Y').to_euler()
 ca=bpy.data.cameras.new('Camara');cam=bpy.data.objects.new('Camara',ca);scene.collection.objects.link(cam);scene.camera=cam;ca.type='ORTHO';ca.ortho_scale=span*1.18
 # Long dimension is read across the image; preserve actual plan proportions.
 loc=(cx+span*.40,cy-span*.85,span*.85);tgt=(cx,cy,3.8 if data['site'] else 1.1);cam.location=loc;cam.rotation_euler=(Vector(tgt)-cam.location).to_track_quat('-Z','Y').to_euler()
 for mode in (['INTERIOR','CUBIERTA'] if data['site'] else ['INTERIOR']):
  target=P/'vistas'/(code+'_'+mode+'.png')
  if target.exists() and target.stat().st_mtime>(P/'fuentes'/(code+'_render.json')).stat().st_mtime:continue
  for ob in scene.objects:
   if ob.name in TOP:ob.hide_render=mode=='INTERIOR'
   if ob.name=='90_CONTEXTO':ob.hide_render=True
  scene.cycles.samples=20 if data['site'] else 8;scene.render.resolution_x=1900 if data['site'] else 1300;scene.render.resolution_y=1350 if data['site'] else 950;scene.render.resolution_percentage=100;scene.render.filepath=str(P/'vistas'/(code+'_'+mode+'.png'));bpy.ops.render.render(write_still=True);print('RENDER',code,mode,flush=True)
 if data['site']:
  for ob in scene.objects:
   if ob.name in TOP:ob.hide_render=False
  ca.ortho_scale=span*1.18;cam.location=(cx-span*.65,cy-span*1.30,9.0);cam.rotation_euler=(Vector((cx,cy,3.3))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.resolution_x=1900;scene.render.resolution_y=1200;scene.render.filepath=str(P/'vistas'/(code+'_PLANTA_BAJA_3D.png'));bpy.ops.render.render(write_still=True);print('RENDER',code,'PLANTA_BAJA_3D',flush=True)
  for ob in scene.objects:
   if ob.name=='90_CONTEXTO':ob.hide_render=False
  ca.ortho_scale=68;cam.location=(70,-60,55);cam.rotation_euler=(Vector((35,0,1))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.resolution_x=1700;scene.render.resolution_y=1150;scene.render.filepath=str(P/'vistas'/(code+'_CONTEXTO.png'));bpy.ops.render.render(write_still=True);print('RENDER',code,'CONTEXTO',flush=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(P/'modelos'/(code+'_VISTAS.blend')))
