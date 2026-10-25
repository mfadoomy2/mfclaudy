from pathlib import Path
import json,math,html,sys
from shapely.geometry import Polygon,Point,LineString,box
from shapely.ops import unary_union,polygonize
from shapely import wkt
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from fontTools.ttLib import TTFont as FontToolsFont
from fontTools.varLib.instancer import instantiateVariableFont

P=Path(__file__).resolve().parents[1]
D=json.loads((P/'verificacion/EXTRACCION_GIRO90_RHINO.json').read_text())
META=json.loads((P/'verificacion/REVISION_GEOMETRICA_GIRO90.json').read_text())
FONT=P/'fuentes/IbarraRealNova-Italic-400.ttf'
if not FONT.exists():
    f=FontToolsFont('/Users/adam/Library/Fonts/IbarraRealNova-Italic-VariableFont_wght.ttf')
    f=instantiateVariableFont(f,{'wght':400},inplace=True);f.save(FONT)
pdfmetrics.registerFont(TTFont('Ibarra',str(FONT)))

def clean(g):return g if g.is_valid else g.buffer(0)
def polys(g):return [g] if g.geom_type=='Polygon' else [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']
def region(ob):
    ps=[p for p in ob['profiles'] if len(p)>3 and Point(p[0][:2]).distance(Point(p[-1][:2]))<.002]
    if ps:return clean(Polygon([q[:2] for q in ps[0]],[[q[:2] for q in p] for p in ps[1:]]))
    caps=[]
    for face in ob['caps']:
        outer=next((p['points'] for p in face if p['outer']),None)
        if outer:caps.append(clean(Polygon([q[:2] for q in outer],[[q[:2] for q in p['points']] for p in face if not p['outer']])))
    if caps:return unary_union(caps)
    out=Polygon();lines=[]
    for pp in ob['sections']:
        if len(pp)>3 and Point(pp[0][:2]).distance(Point(pp[-1][:2]))<.002:out=out.symmetric_difference(clean(Polygon([q[:2] for q in pp])))
        elif len(pp)>1:lines.append(LineString([q[:2] for q in pp]))
    if lines:out=out.union(unary_union(list(polygonize(unary_union(lines)))))
    return out

class Sheet:
    def __init__(self,code,size,bounds,title,level,page):
        self.code=code;self.width,self.height=size;self.title=title;self.level=level;self.page=page;self.ops=[]
        x,y,X,Y=bounds;self.bounds=bounds
        self.scale=10.0 # 10 mm of paper for one metre: exactly 1:100.
        center=(150.,153.) if size[0]==420 else (size[0]/2,228. if size[0]==594 else 315.)
        self.offset=(center[0]-10*(x+X)/2,center[1]-10*(y+Y)/2)
        self.meta={'code':code,'sheet_mm':list(size),'scale':100,'cut_elevation_m':level+1.20,'floor_elevation_m':level,'geometry_source':'RhinoCommon: sections, native profiles and cap loops','true_mm_per_model_m':10.0}
    def pt(self,p):return [self.offset[0]+p[0]*10,self.offset[1]+p[1]*10]
    def linepaper(self,pts,lw=.13,dash=None,kind='PROYECCION_VISIBLE'):
        if len(pts)>1:self.ops.append({'type':'line','points':pts,'lw':lw,'dash':dash or [],'kind':kind})
    def line(self,pts,lw=.13,dash=None,kind='PROYECCION_VISIBLE'):self.linepaper([self.pt(p) for p in pts],lw,dash,kind)
    def polygonpaper(self,rings,lw=.13,fill=None,kind='PROYECCION_VISIBLE'):
        self.ops.append({'type':'polygon','rings':rings,'lw':lw,'fill':fill,'kind':kind})
    def geom(self,g,lw=.13,fill=None,dash=None,kind='PROYECCION_VISIBLE'):
        for p in polys(g):
            rings=[[self.pt(q) for q in ring.coords] for ring in [p.exterior]+list(p.interiors)]
            if dash:
                for ring in rings:self.linepaper(ring,lw,dash,kind)
            else:self.polygonpaper(rings,lw,fill,kind)
    def txt(self,p,text,size=2.5,angle=0,align='left',kind='ROTULACION',paper=False):
        self.ops.append({'type':'text','point':list(p) if paper else self.pt(p),'text':text,'height':size,'angle':angle,'align':align,'kind':kind})
    def dim(self,a,b,offset,axis='x'):
        # Native-coordinate overall dimensions; the label is a measured length
        # in metres, while line weights and text sizes are physical millimetres.
        if axis=='x':
            ay=a[1];by=b[1];yy=offset;A=(a[0],yy);B=(b[0],yy)
            self.line([a,(a[0],yy+.20)],.10,kind='COTAS');self.line([b,(b[0],yy+.20)],.10,kind='COTAS');value=abs(b[0]-a[0]);mid=((A[0]+B[0])/2,yy+.20);ang=0
        else:
            xx=offset;A=(xx,a[1]);B=(xx,b[1]);self.line([a,(xx-.20,a[1])],.10,kind='COTAS');self.line([b,(xx-.20,b[1])],.10,kind='COTAS');value=abs(b[1]-a[1]);mid=(xx-.20,(A[1]+B[1])/2);ang=90
        self.line([A,B],.13,kind='COTAS')
        for q in [A,B]:self.line([(q[0]-.10,q[1]-.10),(q[0]+.10,q[1]+.10)],.18,kind='COTAS')
        self.txt(mid,f'{value:.2f}'.replace('.',','),2.3,ang,'center','COTAS')
    def dim_aligned(self,a,b,distance,label=''):
        dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);nx,ny=-dy/length,dx/length
        A=(a[0]+nx*distance,a[1]+ny*distance);B=(b[0]+nx*distance,b[1]+ny*distance)
        for p,q in [(a,A),(b,B)]:self.line([p,(q[0]+nx*.2,q[1]+ny*.2)],.10,kind='COTAS')
        self.line([A,B],.13,kind='COTAS')
        for q in [A,B]:self.line([(q[0]-.1,q[1]-.1),(q[0]+.1,q[1]+.1)],.18,kind='COTAS')
        ang=math.degrees(math.atan2(dy,dx));ang=(ang+90)%180-90
        mid=((A[0]+B[0])/2+nx*.22,(A[1]+B[1])/2+ny*.22)
        self.txt(mid,(label+' '+f'{length:.2f} m').replace('.',','),2.5,ang,'center','COTAS')
    def axis(self,a,b,label,local=False):
        self.line([a,b],.10,[3,.7,.2,.7],'EJES')
        q=self.pt(b);rad=2.1 if not local else 1.6
        rings=[[[q[0]+rad*math.cos(t*math.pi/16),q[1]+rad*math.sin(t*math.pi/16)] for t in range(33)]]
        self.polygonpaper(rings,.13,1,'EJES');self.txt((q[0],q[1]-.7),label,1.8,align='center',kind='EJES',paper=True)
    def door(self,d):
        if d['type']=='sliding':
            a,b,e=d['p0'],d['p1'],d['pocket_end'];self.line([a,b],.18,kind='CARPINTERIAS')
            dx,dy=b[0]-a[0],b[1]-a[1];ll=math.hypot(dx,dy);nn=(-dy/ll*.025,dx/ll*.025)
            self.line([(a[0]+nn[0],a[1]+nn[1]),(b[0]+nn[0],b[1]+nn[1])],.10,kind='CARPINTERIAS');start=b if Point(e).distance(Point(b))<Point(e).distance(Point(a)) else a
            self.line([start,e],.10,[1.2,.6],'PROYECCION_OCULTA')
        else:
            h,c,o=d['hinge'],d['closed'],d['open'];rr=math.hypot(c[0]-h[0],c[1]-h[1]);aa=math.atan2(c[1]-h[1],c[0]-h[0]);bb=math.atan2(o[1]-h[1],o[0]-h[0]);delta=(bb-aa+math.pi)%(2*math.pi)-math.pi
            self.line([h,o],.18,kind='CARPINTERIAS');self.line([(h[0]+rr*math.cos(aa+delta*t/24),h[1]+rr*math.sin(aa+delta*t/24)) for t in range(25)],.10,kind='CARPINTERIAS')
    def legend(self,area,bath_count):
        W,H=self.width,self.height
        self.linepaper([(12,12),(W-12,12),(W-12,H-12),(12,H-12),(12,12)],.13,kind='MARCO')
        self.txt((20,H-27),self.title,5.2,paper=True)
        self.txt((20,H-35),f'PLANTA · E 1:100 · corte +{self.level+1.2:.2f} m · pavimento +{self.level:.2f} m'.replace('.',','),2.7,paper=True)
        self.txt((W-20,20),self.page,4.5,align='right',paper=True)
        if W==420:
            x=300;y=248
            notes=[('PROGRAMA',3.2),(f'4 personas / 4 dormitorios',2.5),(f'Pavimento geométrico: {area:.2f} m²'.replace('.',','),2.5),(f'{bath_count} baños en borde continuo',2.5),('',2.5),('LECTURA DEL DIBUJO',3.2),('Negro sólido: material seccionado',2.5),('0,18 mm: carpinterías y equipamiento',2.5),('0,13 mm: proyección visible',2.5),('Discontinua: elementos sobre el corte',2.5),('Trazo-punto: ejes de referencia',2.5),('S: simetría local de la bow window',2.5),('',2.5),('CRITERIOS APLICADOS',3.2),('Baños integrados en la envolvente',2.5),('Correderas en baños; sin barrido interior',2.5),('Sofás retirados de estas plantas',2.5),('Montantes dentro del borde de servicios',2.5),('Huecos exteriores sin bajantes superpuestas',2.5),('',2.5),('Sin simetría global acreditada',2.5),('X/Y: referencias; no son ejes estructurales',2.5)]
            for t,size in notes:self.txt((x,y),t,size,paper=True);y-=6
        else:
            self.linepaper([(20,61),(W-20,61)],.13,kind='MARCO')
            self.txt((20,53),'Corte negro 0,35 mm / carpintería 0,18 mm / proyección 0,13 mm / superior discontinua 0,10 mm',2.5,paper=True)
            self.txt((20,47),'X/Y: referencia geométrica. Puntos A-D: apoyos medidos del modelo, sin validación estructural.',2.5,paper=True)
            self.txt((20,41),'P: patinillos del borde de servicios. Sofás retirados. Escalera y ascensor conservan su posición.',2.5,paper=True)
        self.txt((20,20),'G3 · revisión arquitectónica medida desde Rhino · anteproyecto',2.4,paper=True)
        # The scale bar is exactly 50 mm = 5 m at 1:100.
        x=W-105;y=29
        for k in range(5):self.polygonpaper([[(x+k*10,y),(x+(k+1)*10,y),(x+(k+1)*10,y+2),(x+k*10,y+2),(x+k*10,y)]],.13,0 if k%2==0 else 1,'ESCALA')
        for k in [0,1,2,5]:self.txt((x+k*10,y+4),str(k)+(' m' if k==5 else ''),2.2,align='center',paper=True)
        self.meta['scale_bar_paper_mm']=50.;self.meta['scale_bar_model_m']=5.
        self.meta['geometric_floor_m2']=area

SHEETS=[]
for idx,meta in enumerate(META):
    is_u=idx<3;code=meta['code'];level=meta['level'];src=D[0] if is_u else D[1]
    objs=[o for o in src['objects'] if o['parents'][0].startswith(code[:3]+'__')] if is_u else src['objects']
    floor=unary_union([region(o) for o in objs if o['name'].startswith('Suelo continuo')])
    if not is_u:
        parcel=unary_union([region(o) for o in objs if o['layer']=='91_PARCELA'])
        bounds=unary_union([parcel,floor]+[region(o) for o in objs if o['layer']=='21_NUCLEO_VERTICAL']).bounds
    else:bounds=floor.bounds
    s=Sheet(code,(420,297) if is_u else (841,594),bounds,code[:3]+' · unidad de cuatro personas' if is_u else 'E02 · ensayo de giro 90° / NO ENCAJA EN LA PARCELA',level,'P0'+str(idx+1))
    cut=level+1.20;wallparts=[];glass=[];projection=[];equipment=[]
    for ob in objs:
        la=ob['layer'];name=ob['name'];z0=ob['bbox'][0][2];z1=ob['bbox'][1][2]
        if la in ['90_CONTEXTO','16_PERSONAS','22_PUERTAS','11_ENERGIA','12_AGUA','19_SOPORTE_PB']:continue
        g=region(ob)
        if g.is_empty:continue
        if la=='91_PARCELA':s.geom(g,.10,dash=[3,1],kind='PARCELA');continue
        if la in ['09_MEMBRANAS','18_LUCERNARIOS']:
            s.geom(g,.10,dash=[1.8,.8],kind='PROYECCION_OCULTA');continue
        if la in ['00_SUELO','07_ACERO','08_COSTILLAS','17_CUBIERTA_TERMICA']:
            if not is_u and la=='07_ACERO' and any(t in name for t in ['Escalera','Meseta','Galeria']):
                s.geom(g,.18 if 'Galeria' in name else .13,kind='CIRCULACION_VERTICAL')
            if la=='08_COSTILLAS' and z0<cut<z1:wallparts.append(g)
            continue
        if la in ['01_MUROS','23_PATINILLOS']:
            if z0<cut-.001 and z1>cut+.001:wallparts.append(g)
            continue
        if la=='06_VIDRIO':
            if z0<cut<z1:glass.append(g)
            continue
        if z1<level-.01 or z0>level+2.74:continue
        if la=='24_MONTANTES_EN_SERVICIOS':equipment.append((g,.13));continue
        if z0>cut+.001:
            projection.append(g)
        else:equipment.append((g,.13 if la in ['02_COLCHON','05_ASIENTO'] else .18))
    for g in projection:s.geom(g,.10,dash=[1.8,.8],kind='PROYECCION_OCULTA')
    for g,lw in equipment:s.geom(g,lw,1,kind='EQUIPAMIENTO')
    wall=unary_union(wallparts);s.geom(wall,.35,0,kind='CORTE_NEGRO')
    windows=unary_union(glass)
    for p in polys(windows):
        s.geom(p,.18,1,kind='CARPINTERIAS');inner=p.buffer(-.025)
        if not inner.is_empty:s.geom(inner,.10,kind='CARPINTERIAS')
    bed_sizes=[];desk_sizes=[]
    for ob in objs:
        name=ob['name'].lower()
        if 'colchon 125x200' in name or 'tablero 180x90 bisagra' in name:
            g=region(ob)
            if g.is_empty:continue
            rr=list(g.minimum_rotated_rectangle.exterior.coords);lengths=[Point(rr[k]).distance(Point(rr[k+1])) for k in range(4)]
            a,b=sorted(lengths)[:1]+sorted(lengths)[-1:]
            if 'colchon' in name:
                bed_sizes.append([a,b]);j=max(range(4),key=lambda k:lengths[k]);ang=math.degrees(math.atan2(rr[j+1][1]-rr[j][1],rr[j+1][0]-rr[j][0]));ang=(ang+90)%180-90
                cc=g.centroid;s.txt((cc.x,cc.y),f'{a:.2f} × {b:.2f}'.replace('.',','),1.7,ang,'center','COTAS_EQUIPAMIENTO')
            else:desk_sizes.append([a,b])
    occupied=unary_union([g for g,lw in equipment])
    for ob in objs:
        if ob['layer']=='17_CUBIERTA_TERMICA' and 'techo privado' in ob['name']:
            room=region(ob);free=room.buffer(-.15).difference(occupied.buffer(.04)).difference(wall)
            if not free.is_empty:
                cc=max(polys(free),key=lambda p:p.area).representative_point();s.txt((cc.x,cc.y),ob['name'].split()[0],2.3,align='center')
    for door in meta['doors']:s.door(door)
    for shaft in meta['shafts']:
        pp=shaft['center'];s.txt((pp[0]+.18,pp[1]+.18),shaft['id'],1.8,kind='INSTALACIONES')
    building=unary_union([floor,wall,windows]);x,y,X,Y=building.bounds
    s.dim((x,y),(X,y),y-1.05,'x');s.dim((x,y),(x,Y),x-1.05,'y')
    cx,cy=floor.centroid.coords[0];s.axis((x-1.7,cy),(X+1.0,cy),'X');s.axis((cx,y-1.7),(cx,Y+1.0),'Y')
    for axis in meta['bow_axes']:s.axis(axis['p0'],axis['p1'],axis['id'],True)
    if not is_u:
        pillars=[o for o in D[2]['objects'] if o['name']=='Tronco bajo vivienda']
        for j,ob in enumerate(pillars):
            pp=region(ob)
            if pp.is_empty:
                a=ob['bbox'][0];b=ob['bbox'][1];pp=Point((a[0]+b[0])/2,(a[1]+b[1])/2).buffer(.16)
            s.geom(pp,.13,dash=[1,.7],kind='APOYOS_INFERIORES');c=pp.centroid
            s.line([(c.x-.45,c.y),(c.x+.45,c.y)],.10,[2,.5,.2,.5],'EJES');s.line([(c.x,c.y-.45),(c.x,c.y+.45)],.10,[2,.5,.2,.5],'EJES');s.txt((c.x+.50,c.y+.35),chr(65+j),2.2,kind='EJES')
        # Below-floor stair and lift outlines already derive from their native
        # profiles; their convention is drawn separately without invented treads.
    s.legend(floor.area,len(meta['baths']))
    if is_u:s.txt((300,85),'Giro +90° / emplazamiento pendiente',2.5,paper=True)
    else:
        s.txt((20,72),'ENSAYO: 25,81 m transversales frente a 20,17 m máximos del solar. Requiere recomponer la agrupación.',3.0,paper=True)
        s.meta['not_fitted_rotation_test']=True
    s.meta['doors']=len(meta['doors']);s.meta['windows_components']=len(polys(windows));s.meta['wall_cut_m2']=wall.area;s.meta['measured_outer_bbox_m']=list(building.bounds);s.meta['native_bed_sizes_m']=bed_sizes;s.meta['native_desk_sizes_m']=desk_sizes
    SHEETS.append(s)

# Two operational states share the same measured public envelope.
PB=json.loads((P/'verificacion/PROGRAMA_PUBLICO_PB.json').read_text())
for sunday in [False,True]:
    src=D[2];objs=src['objects'];parcel=unary_union([region(o) for o in objs if o['layer']=='91_PARCELA'])
    state='DOMINGO' if sunday else 'DIARIA'
    s=Sheet('E02_PB_'+state,(594,420),parcel.bounds,'Parcela · planta baja pública / '+('exposición vecinal del domingo' if sunday else 'biblioteca, estudio y trabajo compartido'),0,'P06' if sunday else 'P05');walls=[];glasses=[]
    for ob in objs:
        la=ob['layer'];name=ob['name'];z0=ob['bbox'][0][2];z1=ob['bbox'][1][2];g=region(ob)
        if g.is_empty or la in ['90_CONTEXTO','16_PERSONAS','11_ENERGIA','12_AGUA','24_MONTANTES_EN_SERVICIOS']:continue
        if la==('26_ESTUDIO_DIARIO' if sunday else '27_EXPOSICION_DOMINGO'):continue
        if la=='91_PARCELA':s.geom(g,.25,kind='PARCELA');continue
        if la=='00_SUELO':
            if name.startswith('Suelo continuo') and z0>3.7:s.geom(g,.10,dash=[2,.8],kind='PROYECCION_OCULTA')
            continue
        if la=='17_CUBIERTA_TERMICA':
            if name.startswith('Cubierta publica'):s.geom(g,.10,dash=[2,.8],kind='PROYECCION_OCULTA')
            continue
        if la in ['09_MEMBRANAS','18_LUCERNARIOS','08_COSTILLAS','10_CABLES','22_PUERTAS','23_PATINILLOS']:continue
        if z0>3.7 or z1<-.10:continue
        if la=='19_SOPORTE_PB':
            if name=='Tronco bajo vivienda':walls.append(g)
            continue
        if la in ['01_MUROS','15_BANOS'] and z0<1.2<z1:walls.append(g)
        elif la=='06_VIDRIO' and z0<1.2<z1:glasses.append(g)
        elif z0>1.2:s.geom(g,.10,dash=[1.8,.8],kind='PROYECCION_OCULTA')
        else:s.geom(g,.13,1,kind='EQUIPAMIENTO')
    s.geom(unary_union(walls),.35,0,kind='CORTE_NEGRO')
    for g in glasses:
        s.geom(g,.18,1,kind='CARPINTERIAS')
        if not g.buffer(-.025).is_empty:s.geom(g.buffer(-.025),.10,kind='CARPINTERIAS')
    for door in PB['public_doors']:s.door(door)
    labels=[((17.2,6.7),'01 · Coworking / 4 puestos'),((25.8,8.7),'02 · Biblioteca / 53,05 m²'),((56.8,.95),'03 · '+('Exposición vecinal' if sunday else 'Estudio / 8 puestos')),((56.8,-5.65),'67,09 m² / sala transformable'),((22.4,-6.05),'04 · Reparar / coser'),((31.8,.0),'05 · Comer juntas'),((35.5,-4.3),'06 · Cocina compartida'),((36.5,5.25),'07 · Punto vecinal'),((28.5,-6.0),'08 · Servicios'),((46.1,-4.1),'Escalera'),((51.1,-3.35),'Ascensor'),((18,-5.65),'09 · Fuente / encuentro'),((20.8,2.3),'10 · '+('Muestra de proyectos / intercambio' if sunday else 'Plaza abierta / actividades'))]
    for pt,label in labels:s.txt(pt,label,2.3,align='center')
    x,y,X,Y=parcel.bounds;s.dim((x,y),(X,y),y-1.05,'x')
    # Street frontage is the actual inclined edge, not the parcel's bounding box.
    front_a=(13.28,-7.5);front_b=(12.07,7.43)
    s.dim_aligned(front_a,front_b,1.45,'FRENTE A CALLE')
    s.meta['frontage_m']=math.dist(front_a,front_b)
    s.meta['overall_extent_x_m']=X-x;s.meta['overall_extent_y_m']=Y-y
    for j,ob in enumerate(o for o in objs if o['name']=='Tronco bajo vivienda'):
        a,b=ob['bbox'];c=((a[0]+b[0])/2,(a[1]+b[1])/2);s.axis((c[0]-.55,c[1]),(c[0]+.55,c[1]),chr(65+j),True)
    s.legend(parcel.area,2)
    # Replace residential-only footer notes in public-level sheets.
    for op in s.ops:
        if op.get('type')=='text' and op['text'].startswith('P: patinillos'):op['text']='Biblioteca y estudio con luz cenital. Mesas plegables / paneles móviles. Planta baja sin vivienda privada.'
    s.meta['programme_state']=state;s.meta['library_area_m2']=PB['library_area_m2'];s.meta['study_area_m2']=PB['study_exhibition_area_m2'];SHEETS.append(s)

def pdfpage(c,s):
    c.setPageSize((s.width*mm,s.height*mm));c.setFillColorRGB(1,1,1);c.rect(0,0,s.width*mm,s.height*mm,fill=1,stroke=0)
    for ob in s.ops:
        c.setStrokeColorRGB(0,0,0);c.setFillColorRGB(0,0,0)
        if ob['type']=='text':
            c.saveState();c.translate(ob['point'][0]*mm,ob['point'][1]*mm);c.rotate(ob['angle']);c.setFont('Ibarra',ob['height']*mm)
            if ob['align']=='center':c.drawCentredString(0,0,ob['text'])
            elif ob['align']=='right':c.drawRightString(0,0,ob['text'])
            else:c.drawString(0,0,ob['text'])
            c.restoreState();continue
        c.setLineWidth(ob['lw']*mm);c.setDash([x*mm for x in ob.get('dash',[])],0);c.setLineJoin(1);c.setLineCap(0)
        path=c.beginPath()
        rings=ob['rings'] if ob['type']=='polygon' else [ob['points']]
        for pts in rings:
            path.moveTo(pts[0][0]*mm,pts[0][1]*mm)
            for q in pts[1:]:path.lineTo(q[0]*mm,q[1]*mm)
            if ob['type']=='polygon':path.close()
        fill=ob.get('fill');c.setFillColorRGB(1,1,1) if fill==1 else c.setFillColorRGB(0,0,0)
        c.drawPath(path,stroke=1,fill=fill is not None,fillMode=0)
    c.showPage()

def svg(s):
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.width}mm" height="{s.height}mm" viewBox="0 0 {s.width} {s.height}"><defs><style>@font-face{{font-family:Ibarra;src:url(../fuentes/IbarraRealNova-Italic-400.ttf)}}text{{font-family:Ibarra; font-style:italic}}</style></defs>']
    for ob in s.ops:
        if ob['type']=='text':
            x,y=ob['point'];anchor={'left':'start','center':'middle','right':'end'}[ob['align']]
            out.append(f'<text x="{x}" y="{s.height-y}" font-size="{ob["height"]}" text-anchor="{anchor}" transform="rotate({-ob["angle"]} {x} {s.height-y})">{html.escape(ob["text"])}</text>');continue
        rings=ob['rings'] if ob['type']=='polygon' else [ob['points']]
        path=' '.join('M '+' L '.join(f'{x:.5f},{s.height-y:.5f}' for x,y in pts)+(' Z' if ob['type']=='polygon' else '') for pts in rings)
        fill='none' if ob.get('fill') is None else ('white' if ob['fill']==1 else 'black');dash=' '.join(map(str,ob.get('dash',[])))
        out.append(f'<path d="{path}" fill="{fill}" fill-rule="evenodd" stroke="black" stroke-width="{ob["lw"]}" stroke-dasharray="{dash}"/>')
    out.append('</svg>');return '\n'.join(out)

combined=canvas.Canvas(str(P/'planos/G3_PLANOS_TECNICOS_1_100.pdf'),pageCompression=1);combined.setTitle('G3 · Plantas técnicas · 1:100');combined.setAuthor('G3')
pbpdf=canvas.Canvas(str(P/'planos/P05_P06_PLANTA_BAJA_DIARIA_Y_DOMINGO_1_100.pdf'),pageCompression=1)
for i,s in enumerate(SHEETS):
    if i<4:
        dest=P/'planos'/(s.page+'_'+s.code+'_1_100.pdf');cc=canvas.Canvas(str(dest),pageCompression=1);pdfpage(cc,s);cc.save()
    else:pdfpage(pbpdf,s)
    pdfpage(combined,s)
    (P/'planos'/(s.page+'_'+s.code+'_1_100.svg')).write_text(svg(s))
pbpdf.save()
combined.save()
(P/'fuentes/DIBUJO_VECTORIAL.json').write_text(json.dumps([{'code':s.code,'page':s.page,'width':s.width,'height':s.height,'meta':s.meta,'ops':s.ops} for s in SHEETS],ensure_ascii=False,separators=(',',':')))
(P/'verificacion/ESCALAS_Y_MEDIDAS.json').write_text(json.dumps([s.meta for s in SHEETS],ensure_ascii=False,indent=2))
print('6 plantas vectoriales / 6 PDF / 6 SVG / escala exacta 10 mm por metro')
