from pathlib import Path
import shutil,json,pickle,csv
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parents[1];E=P/'ENTREGA';E.mkdir(exist_ok=True)
for folder in ['modelos','habitaciones','vistas','verificacion','fuentes','datos']:(E/folder).mkdir(exist_ok=True)
for src,target in [(P/'modelos_finales',E/'modelos'),(P/'detalles_habitacion',E/'habitaciones')]:
 for p in src.glob('*.3dm'):
  if not p.name.startswith('._'):shutil.copyfile(p,target/p.name)
shutil.copyfile(P/'CATALOGO_40_UNIDADES_COTA0.3dm',E/'CATALOGO_40_UNIDADES_COTA0.3dm')
for p in (P/'vistas').glob('*.png'):
 if not p.name.startswith('._') and not p.name.endswith('_HABITACION.png'):shutil.copyfile(p,E/'vistas'/p.name)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',21)
for mode in ['AXON','PLANTA']:
 for half in range(2):
  sheet=Image.new('RGB',(2100,1330),'#f8f6f0');dr=ImageDraw.Draw(sheet)
  for j in range(20):
   i=half*20+j;code=f'N{i//2+1:02}{"AB"[i%2]}';im=Image.open(E/'vistas'/f'{code}_{mode}.png');im.thumbnail((408,282));x=(j%5)*420;y=(j//5)*330;sheet.paste(im,(x+(420-im.width)//2,y+32));dr.text((x+14,y+5),code,font=font,fill='#253d35')
  sheet.save(E/'vistas'/f'CONTACTO_{mode}_{half+1}.jpg',quality=95)
D=pickle.load(open(P/'datos/GEOMETRIA_3D.pkl','rb'))
with open(E/'datos/SUPERFICIES.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['codigo','planta_previa_m2','suelo_modelo_m2','privado_m2','suelo_terminado_z_m'])
 for d in D:w.writerow([d['code'],round(d['floor'].area,2),round(d['floor3d'].area,2),round(sum(r['poly'].area for r in d['rooms']),2),0])
checks=['AUDITORIA_FINAL_ESPACIO.json','NATIVO_SOLIDOS.json','NATIVO_ENTREGA.json','NATIVO_VERIFICACION_ULTIMA.json','APOYO_MUROS_Y_FORJADO.json','APOYOS_DETALLE.json','CARROS_ACCESO.json','LAVABOS.json','CATALOGO.json','ESPACIO.json']
for name in checks:
 if (P/'verificacion'/name).exists():shutil.copyfile(P/'verificacion'/name,E/'verificacion'/name)
for p in (P/'fuentes').glob('*.py'):
 if not p.name.startswith('._') and p.name not in ['auditar_recorridos.py','prueba_nativa.py']:shutil.copyfile(p,E/'fuentes'/p.name)
shutil.copyfile(P/'datos/GEOMETRIA_3D.pkl',E/'datos/GEOMETRIA_3D.pkl')
print('ENTREGA_COPIADA')
