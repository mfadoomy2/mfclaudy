from pathlib import Path
import json,math,runpy,numpy as np
R=Path(__file__).resolve().parents[1]
# Uses the same independently tested Euler-Bernoulli element as the main frame.
f=runpy.run_path(str(R/'fuentes/calcular_estructura.py'));klocal=f['klocal'];section=f['section'];E=f['E'];G=f['G']
def roof(D,t):
 pts=[[ -4.8,0,0],[-4.8,0,2.2]]+[[ -4.8*math.cos(j*math.pi/32),0,2.2+2.1*math.sin(j*math.pi/32)] for j in range(1,33)]+[[4.8,0,0]]
 pts=np.array(pts);n=len(pts);K=np.zeros((n*6,n*6));load=np.zeros(n*6);mats=[];A,I,J,W=section(D,t);spacing=6.8/14
 for i in range(n-1):
  a,b=pts[i:i+2];v=b-a;L=np.linalg.norm(v);ex=v/L;ref=np.array([0,1.,0]);ey=np.cross(ref,ex);ey/=np.linalg.norm(ey);ez=np.cross(ex,ey);rr=np.vstack([ex,ey,ez]);tt=np.zeros((12,12))
  for j in [0,3,6,9]:tt[j:j+3,j:j+3]=rr
  kl=klocal(L,A,I,J);kg=tt.T@kl@tt;ids=np.r_[np.arange(6*i,6*i+6),np.arange(6*(i+1),6*(i+1)+6)];K[np.ix_(ids,ids)]+=kg;mats.append((kl,tt,ids,L))
  # Gravity tests 0.7 kPa permanent and 1.0 kPa variable on the horizontal projection.
  q=(1.35*1.0+1.5*1.0)*spacing*abs(b[0]-a[0]);load[6*i+2]-=q/2;load[6*(i+1)+2]-=q/2
 fixed=list(range(6))+list(range((n-1)*6,n*6));free=np.setdiff1d(np.arange(n*6),fixed);u=np.zeros(n*6);u[free]=np.linalg.solve(K[np.ix_(free,free)],load[free]);stress=0
 for kl,tt,ids,L in mats:
  fl=kl@(tt@u[ids]);stress=max(stress,max(abs(fl[0]),abs(fl[6]))/A+max(np.linalg.norm(fl[4:6]),np.linalg.norm(fl[10:12]))/W)
 return {'D_mm':D*1000,'t_mm':t*1000,'stress_ULS_MPa':stress/1000,'peak_displacement_ULS_mm':max(np.linalg.norm(u.reshape(-1,6)[:,:3],axis=1))*1000,'peak_displacement_SLS_mm':max(np.linalg.norm(u.reshape(-1,6)[:,:3],axis=1))*1000*2./2.85,'rib_spacing_m':spacing,'assumptions':'Fixed feet, 1.0 kPa G and 1.0 kPa Q; in-plane beam test. Lateral stability, buckling, shell action and wind uplift are not certified by this submodel.'}
roofs=[roof(D,t) for D,t in [(.0889,.004),(.1143,.0063),(.1397,.0063)]]
chosen=next((x for x in roofs if x['stress_ULS_MPa']<220 and x['peak_displacement_SLS_mm']<25),roofs[-1])
# Six secondary RHS joists per deck; end joists already coincide with main CHS beams.
b,h,tw,L=.160,.360,.010,7.15;I=(b*h**3-(b-2*tw)*(h-2*tw)**3)/12;A=b*h-(b-2*tw)*(h-2*tw);qS=8.6*1.15+77*A;qU=(1.35*3.6+1.5*5)*1.15+1.35*77*A
joist={'profile':'RHS360x160x10','span_m':L,'spacing_m':1.15,'I_m4':I,'bending_ULS_MPa':(qU*L*L/8)/(I/(h/2))/1000,'deflection_SLS_mm':5*qS*L**4/(384*210e6*I)*1000,'limit_L300_mm':L/300*1000,'self_weight_kN_each':L*A*77}
# Membrane cable strip: elementary parabolic cable, not a prestressed nonlinear membrane analysis.
lineq=1.0*2.;span=5.25;sag=.60;H=lineq*span*span/(8*sag);vertical=lineq*span/2;T=math.hypot(H,vertical)*1.5
cable={'wind_test_kPa':1.,'tributary_width_m':2.,'span_m':span,'sag_m':sag,'horizontal_kN':H,'tension_ULS_kN':T,'cable_diameter_mm':16,'gross_stress_MPa':T/(math.pi*.016**2/4)/1000,'note':'No prestress, slackening, aerodynamic response or clamp capacity verification.'}
# Rainwater; one canopy is approximately 10.5 x 7.8 m in projection.
catch=10.5*7.8;Q=catch*.1/3600*1000
capacities={}
for D in [.100,.200,.250]:
 ar=.5*math.pi*(D/2)**2;rh=D/4;cap=ar*rh**(2/3)*math.sqrt(.01)/.011*1000;capacities[str(int(D*1000))]=cap
rain={'test_rainfall_mm_h':100,'one_canopy_m2':catch,'one_canopy_L_s':Q,'four_canopies_L_s':4*Q,'all_canopies_L_s':10*Q,'half_full_manning_capacity_L_s_at_1percent':capacities,'n':.011,'note':'Ideal clean circular horizontal collector at half fill. Does not replace HS5 site design, fittings, local rainfall or vertical-stack checks.'}
U=1/(.13+.018/.13+.160/.04+.018/.13+.002/.2+.04)
thermal={'opaque_component_U_W_m2K':U,'layers':'18mm timber +160mm cork lambda0.040 +18mm timber +2mm membrane; Rsi0.13 Rse0.04','note':'One-dimensional assumed-material calculation only; excludes thermal bridges, glazing, airtightness and whole-building energy compliance.'}
a=json.loads((R/'calculo/ESTRUCTURA_RESULTADOS.json').read_text());br=[e for e in a['elements'] if e['kind']=='RAMA'];crit=max(br,key=lambda e:e['M_kNm']);N=crit['N_kN'];M=crit['M_kNm'];nb=16;r=.57;Ftd=.9*800e3*(561e-6)/1.25;demand=N/nb+2*M/(nb*r)
joint={'bolt_group':'16 x M30 class8.8','circle_radius_m':r,'branch_reference_N_kN':N,'branch_reference_M_kNm':M,'bolt_tension_estimate_kN':demand,'bolt_tension_resistance_kN':Ftd,'ratio':demand/Ftd,'note':'Elastic bolt-group screening for the gravity reference forces. Plate prying, welds, shell stresses, concrete anchorage and complete joint stiffness require further design.'}
res={'roof_rib_trials':roofs,'roof_rib_selected':chosen,'secondary_joists':joist,'membrane_cable':cable,'rain':rain,'thermal':thermal,'branch_connection':joint}
(R/'calculo/SUBSISTEMAS_RESULTADOS.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
