from pathlib import Path
import bpy,json,math
from mathutils import Vector
R=Path(__file__).resolve().parents[1];cache=json.loads((R/'fuentes/geometria_render.json').read_text());A=json.loads((R/'calculo/ESTRUCTURA_RESULTADOS.json').read_text());p=A['plates'][3];cx,fy,zz=p['cx'],p['front'],p['z']
def make(sceneid):
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 for k,b in cache.items():
  la=b['layer']
  if la in ['90_CONTEXTO','28_CIMENTACION','00_PARCELA'] or 'ESTADO_VERANO' in la:continue
  if sceneid=='unit' and la in ['02_ESTRUCTURA_RAMAS','26_ARRIOSTRAMIENTO','09_ESCALERAS','07_GALERIAS','18_ASCENSOR','19_ASCENSOR_VIDRIO']:continue
  vs=b['vertices'];sel=[]
  for f in b['faces']:
   pts=[vs[i] for i in f];xx=sum(q[0] for q in pts)/len(pts);yy=sum(q[1] for q in pts)/len(pts);z=sum(q[2] for q in pts)/len(pts)
   if sceneid=='unit':ok=(cx-6.3<=xx<=cx+6.3 and fy-2.2<=yy<=fy+7.2 and zz-.65<=z<=zz+5.35)
   else:ok=(-.25<=z<=3.10 and 12<=xx<=61 and -8<=yy<=12)
   if ok:sel.append(f)
  if not sel:continue
  used=sorted(set(i for f in sel for i in f));mapping={j:i for i,j in enumerate(used)};pts=[vs[i] if sceneid=='pb' else [vs[i][0]-cx,vs[i][1]-fy,vs[i][2]-zz] for i in used];faces=[[mapping[j] for j in f] for f in sel]
  me=bpy.data.meshes.new(k);me.from_pydata(pts,[],faces);me.update();m=bpy.data.materials.new(k);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*b['color'],1);bs.inputs['Roughness'].default_value=.5
  if b['alpha']>.01 or 'VIDRIO' in la:
   mix=m.node_tree.nodes.new('ShaderNodeMixShader');tr=m.node_tree.nodes.new('ShaderNodeBsdfTransparent');o=m.node_tree.nodes.get('Material Output');mix.inputs[0].default_value=.92 if 'VIDRIO' in la else b['alpha'];m.node_tree.links.new(bs.outputs[0],mix.inputs[1]);m.node_tree.links.new(tr.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],o.inputs['Surface'])
  me.materials.append(m);ob=bpy.data.objects.new(la+k,me);bpy.context.collection.objects.link(ob)
  if any(t in la for t in ['PERSONAS','COSTILLAS','RAMAS']):
   for poly in me.polygons:poly.use_smooth=True
 sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=16;sc.cycles.use_denoising=True;sc.cycles.transparent_max_bounces=32;sc.render.resolution_x=2400;sc.render.resolution_y=1650;sc.render.resolution_percentage=100;sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.96,.95,.92,1);sc.world.node_tree.nodes['Background'].inputs[1].default_value=.65;sc.view_settings.view_transform='AgX'
 for loc,pow,size in [((0,-10,30),4500,25),((20,20,25),3500,20)]:
  if sceneid=='pb':loc=(loc[0]+35,loc[1],loc[2]+10);pow*=5;size*=2
  ll=bpy.data.lights.new('L','AREA');ll.energy=pow;ll.shape='DISK';ll.size=size;oo=bpy.data.objects.new('L',ll);bpy.context.collection.objects.link(oo);oo.location=loc;oo.rotation_euler=(Vector((35,0,0) if sceneid=='pb' else (0,3,1))-oo.location).to_track_quat('-Z','Y').to_euler()
 ca=bpy.data.cameras.new('C');cam=bpy.data.objects.new('C',ca);bpy.context.collection.objects.link(cam);sc.camera=cam;ca.type='ORTHO'
 return sc,cam
sc,cam=make('unit');cam.location=(16,23,17);cam.rotation_euler=(Vector((0,2.8,1.6))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=17;sc.render.filepath=str(R/'diagramas/08_UNIDAD_V5_NORTE.png');bpy.ops.render.render(write_still=True)
for o in bpy.data.objects:
 if o.type=='MESH' and any(t in o.name for t in ['12_CUBIERTAS','13_COSTILLAS','14_VIDRIOS','06_VELAS','05_CABLES']):o.hide_render=True
cam.location=(0,3,35);cam.rotation_euler=(Vector((0,3,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=14;sc.render.filepath=str(R/'diagramas/09_UNIDAD_V5_PLANTA.png');bpy.ops.render.render(write_still=True)
sc,cam=make('pb');cam.location=(80,-65,50);cam.rotation_euler=(Vector((36,-.5,1))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=54;sc.render.filepath=str(R/'diagramas/10_PLANTA_BAJA_V5.png');bpy.ops.render.render(write_still=True)
print('RENDERS_V5_LISTOS',flush=True)
