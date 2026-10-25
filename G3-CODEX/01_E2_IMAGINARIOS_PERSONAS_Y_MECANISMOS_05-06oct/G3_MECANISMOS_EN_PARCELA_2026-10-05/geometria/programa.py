from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,ConnectionPatch
ROOT=Path(__file__).resolve().parents[1]
program=[('40 habitaciones × 16 m²',640,'privado'),('Baños y apoyos de aseo',80,'privado'),('Cocina + comer',100,'común'),('Taller seco / textil',75,'común'),('Sonido / cabinas',40,'común'),('Sala transformable / asamblea',80,'común'),('Acogida / cuidados',25,'común'),('Lavandería',30,'común'),('Materiales / herramientas',35,'común'),('Baja estimulación',25,'común'),('Biblioteca / trabajo',30,'común'),('Circulación y núcleos',220,'infraestructura'),('Reserva estructura / cerramientos',120,'infraestructura')]
assert sum(x[1] for x in program)==1500
profiles=[('IRENE · 23','Antropología + técnica de sonido','Cabina aislada / estudio / sueño'),('LAURA · 24','ONG / turnos de siete horas','Llegada discreta / cuidados / cocina'),('ANDREA · 24','Artista / Bellas Artes','Taller / guardar obra / vivir fuera del taller'),('JAIRO · 26','Telecomunicación / presión de venta','Permanencia / mesa / proximidad'),('ARIEL · 25','Inicio de vida laboral / Arganda','Acogida / cuarto propio / relevo'),('IONA · 21','Estudiante / vive con su abuela','Autonomía / estudiar / sostener vínculos')]
fig=plt.figure(figsize=(16,11),facecolor='#e4e2dc'); ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,160),ylim=(0,110));ax.axis('off')
ink='#292f2d';red='#a33e31';muted='#616560'
def txt(x,y,t,s=9,c=ink,**kw):ax.text(x,y,t,fontsize=s,color=c,fontfamily='DejaVu Sans',va='top',**kw)
txt(5,105,'PERSONAS → CONFLICTOS → ESPACIOS',19)
txt(5,100,'Ribera de Curtidores 31 · hipótesis de programa para 40 jóvenes · 1.500 m² construidos',11)
# A qualitative evidence-to-design mapping, no spurious proportional population chart.
for i,(name,situation,need) in enumerate(profiles):
    y=91-i*9
    txt(5,y,name,11,red);txt(5,y-2.5,situation,8.6);txt(47,y,need,9)
    ax.plot([41,45],[y-1,y-1],color=red,lw=.7)
    ax.scatter([45],[y-1],s=6,color=red)
txt(5,35,'LOS TESTIMONIOS NO SON UN CENSO',10,red)
txt(5,31.8,'Situaciones recogidas en el MD aportado. No son residentes asignados,\nni cuotas de admisión, ni porcentajes de la población joven.',9)
# Measured budget, drawn as a space allocation strip and a keyed ledger.
col={'privado':'#3a3f3c','común':'#a24b3b','infraestructura':'#9b988c'}
x=91;w=11;y=92
for index,(label,area,kind) in enumerate(program):
    h=area/1500*70
    ax.add_patch(Rectangle((x,y-h),w,h,facecolor=col[kind],edgecolor='#e4e2dc',lw=.8))
    ly=91-index*4.8
    ax.plot([102,106,109],[y-h/2,ly-1,ly-1],color=col[kind],lw=.5)
    txt(110,ly,label,8.5);txt(154,ly,str(area),9,ha='right')
    y-=h
txt(110,25,'TOTAL',11);txt(154,25,'1.500 m²',11,ha='right')
txt(91,19,'720 privado · 440 común · 340 infraestructura',9)
# Different time scales of change, an explicit rule instead of rotating people through beds.
ax.plot([5,155],[20.8,20.8],color=ink,lw=.65)
for x,title,body in [(5,'CADA DÍA','Cerrar / abrir / descansar\nPaneles y muebles, no camas por turnos.'),(44,'CADA SEMANA','Domingo / reparación / asamblea\nSe abre el taller; la casa mantiene su acceso.'),(84,'CADA ESTANCIA','Entrar / aprender / dejar huella\nDerecho de uso + transmisión de saberes.'),(124,'DURACIÓN LARGA','Reparar / sustituir / sostener\nEstructura colectiva; piezas reversibles.')]:
    txt(x,15,title,9,red);txt(x,11.8,body,8)
txt(5,3.8,'Tanteo de proyecto: áreas y habitabilidad pendientes de desarrollo. El espacio de asamblea/cine/comedor comparte tiempos; no se suma dos veces.',8)
fig.savefig(ROOT/'17_programa_y_habitantes.png',dpi=180,facecolor=fig.get_facecolor());fig.savefig(ROOT/'geometria/17_programa_y_habitantes.svg',facecolor=fig.get_facecolor())
(ROOT/'programa.json').write_text(json.dumps({'plazas_hipotesis':40,'superficie_construida_objetivo':1500,'desglose':[{'uso':a,'m2':b,'categoria':c} for a,b,c in program],'perfiles_md':profiles,'naturaleza':'Programa propuesto; testimonios cualitativos del MD, no censo. No comprobacion normativa.'},ensure_ascii=False,indent=2))
