from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from shapely.affinity import scale,translate
from shapely.geometry import box,LineString,Point
from shapely.ops import unary_union
import rhino3dm as rh
import estudio as E
P=Path(__file__).resolve().parents[1];f=E.B
# Mirror the complete second dwelling; keep scale and human dimensions.
shift=2*5.35+3.0
T=lambda g:translate(scale(g,xfact=-1,yfact=1,origin=(0,0)),shift,0)
x1=5.35;x2=shift-5.35;mid=(x1+x2)/2
# A shared threshold, outside the two independent dwelling outlines.
link=box(x1,-.45,x2,.85).union(Point(mid,.2).buffer(1.3,quad_segs=40)).union(box(mid-.65,-1.8,mid+.65,.2))
link=link.difference(f['floor'].union(T(f['floor'])))
ray=box(.8,5.65,2.9,8.65)
privateclear=[]
for r in f['rooms']:
 privateclear.append(E.tf(ray,r).intersection(T(f['floor'])).area<1e-6)
 privateclear.append(T(E.tf(ray,r)).intersection(f['floor']).area<1e-6)
assert all(privateclear)
assert f['floor'].intersection(T(f['floor'])).area<1e-6
fig,ax=plt.subplots(figsize=(20,12),facecolor='#faf8f2')
E.draw(ax,link,'#d7ccad',E.C['wall'])
for trans in [lambda x:x,T]:
 E.draw(ax,trans(f['floor']),E.C['floor'])
 for r in f['rooms']:
  E.draw(ax,trans(E.tf(E.ROOM,r)),E.C['private'])
  for k,g in E.FURN.items():E.draw(ax,trans(E.tf(g,r)),E.C['ward'] if k=='ropa' else E.C['seat'] if k=='rincon_ventana' else E.C['desk'])
  E.draw(ax,trans(E.tf(E.WIN,r)),E.C['glass'])
  E.line(ax,trans(E.tf(LineString([(.65,5.73),(3.15,5.73)]),r)),E.C['seat'],1.4,'--')
 E.draw(ax,trans(f['solid']),E.C['wall'])
 for b in f['baths']:E.draw(ax,trans(b),E.C['bath'],E.C['wall'])
 for w in f['wincommon']:E.draw(ax,trans(w),E.C['glass'])
 for k in ['kitchen','table','sofa']:E.draw(ax,trans(f[k]),E.C['seat'] if k=='sofa' else E.C['desk'],E.C['wall'])
 for chair in f['chairs']:E.draw(ax,trans(chair),E.C['desk'],E.C['wall'])
for x,tx in [(4.7,'A'),(shift-4.7,'B')]:
 ax.annotate('',xy=(x,.2),xytext=(mid,.2),arrowprops=dict(arrowstyle='->',color=E.C['route'],lw=1.6))
ax.annotate('',xy=(mid,-1.2),xytext=(mid,-3.2),arrowprops=dict(arrowstyle='->',color=E.C['route'],lw=1.6))
E.txt(ax,mid,-3.7,'ACCESO COMÚN\ncota 0 de este ensayo',9)
E.txt(ax,mid,1.85,f'UMBRAL COMPARTIDO\n{link.area:.2f} m² adicionales',9)
E.txt(ax,-.5,9.8,'UNIDAD A / 4 PERSONAS',12);E.txt(ax,shift+.5,9.8,'UNIDAD B / 4 PERSONAS',12)
x,y,X,Y=unary_union([f['floor'],T(f['floor']),link]).bounds
ax.set_xlim(x-.9,X+.9);ax.set_ylim(y-1.3,Y+1.8);ax.set_aspect('equal');ax.axis('off')
E.line(ax,LineString([(x,y-.55),(x+5,y-.55)]),'#263d35',2);E.txt(ax,x+2.5,y-.9,'5 m',9)
fig.suptitle('PRIMER ENCUENTRO / DOS VIVIENDAS, UN UMBRAL',x=.04,y=.97,ha='left',fontsize=23,color='#263d35')
fig.text(.04,.90,'La segunda vivienda se refleja sin escalar. Cada grupo conserva cocina, baños, estancia y cuatro dormitorios.\nEl encuentro ocurre antes de entrar: no obliga a atravesar la vivienda vecina. Las telas siguen siendo controlables por habitación.',fontsize=12,color='#263d35')
fig.text(.04,.035,'8 ventanas privadas con franjas de 3 m sin intersección con la otra vivienda, en este ensayo horizontal. No demuestra iluminación suficiente.\nLas ventanas comunes enfrentadas requieren estudio de privacidad y luz. Faltan parcela, alturas vecinas, núcleo vertical y soporte estructural.\nLa unión es una hipótesis espacial; no se ha convertido todavía en una megaestructura.',fontsize=10,color='#263d35')
fig.subplots_adjust(left=.04,right=.98,top=.82,bottom=.12)
fig.savefig(P/'04_DOS_UNIDADES_UMBRAL.png',dpi=140);fig.savefig(P/'04_DOS_UNIDADES_UMBRAL.svg');plt.close(fig)
m=rh.File3dm();m.Settings.ModelUnitSystem=rh.UnitSystem.Meters;m.Settings.ModelAbsoluteTolerance=.001
for prefix,trans in [('A',lambda x:x),('B',T),('COMUN',lambda x:x)]:
 gs=[('SUELO',link)] if prefix=='COMUN' else [('SUELO',trans(f['floor'])),('MUROS',trans(f['solid'])),('HUECOS',trans(f['wins']))]+[(f'H{i+1}_{k}',trans(E.tf(g,r))) for i,r in enumerate(f['rooms']) for k,g in E.FURN.items()]+[(f'COMUN_{i}',trans(g)) for i,g in enumerate(f['baths']+f['furn'])]
 for name,g in gs:
  l=rh.Layer();l.Name=prefix+'_'+name;idx=m.Layers.Add(l)
  for p in E.G.polys(g) if hasattr(E,'G') else ([g] if g.geom_type=='Polygon' else [v for v in getattr(g,'geoms',[]) if v.geom_type=='Polygon']):
   for ring in [p.exterior]+list(p.interiors):
    pts=[]
    for xx,yy in ring.coords:
     pt=rh.Point3d(xx,yy,0)
     if not pts or pt.DistanceTo(pts[-1])>1e-5:pts.append(pt)
    if len(pts)<4:continue
    pts[-1]=pts[0];cv=rh.PolylineCurve(pts);assert cv.IsValid
    a=rh.ObjectAttributes();a.LayerIndex=idx;a.Name=name;m.Objects.AddCurve(cv,a)
m.Strings['Alcance']='Pareja de estudio 2D; sin parcela ni calculo solar/estructural.'
m.Write(str(P/'DOS_UNIDADES_PLANTA_EDITABLE.3dm'),8)
(P/'VERIFICACION_PAREJA.json').write_text(json.dumps({'unidad':'V02','habitantes':8,'superficie_suelo_viviendas_m2':round(f['floor'].area*2,2),'suelo_umbral_adicional_m2':round(link.area,2),'ventanas_privadas_con_franja3m_sin_otro_vecino':sum(privateclear),'solape_viviendas_m2':0,'alcance':'Ensayo horizontal 2D. No se verifica luz ni estructura ni parcela.'},ensure_ascii=False,indent=2))
