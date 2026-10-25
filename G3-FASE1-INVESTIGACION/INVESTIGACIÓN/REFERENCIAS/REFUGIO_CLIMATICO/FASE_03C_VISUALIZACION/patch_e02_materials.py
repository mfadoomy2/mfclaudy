# -*- coding: utf-8 -*-
"""Correcciones de continuidad E01->E02 aprobadas (ajustes 1-5) sobre viewer_e01.html."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, '_viewer', 'viewer_e01.html')
s = open(p, encoding='utf-8').read()

reps = [
    # 1 MEMBRANA_VERDE: teal -> lima-alga calido humedo
    ("vary(new THREE.Color(0xc6dc90), 10, 0.04)", "vary(new THREE.Color(0xd3dd7e), 8, 0.04)"),
    ("emissive: 0xb8d47e, emissiveIntensity: 0.45", "emissive: 0xc9d468, emissiveIntensity: 0.5"),
    # 2 MADERA: menos miel uniforme, mas natural
    ("vary(new THREE.Color(0xbfa078), 4, 0.05)", "vary(new THREE.Color(0xb5a084), 7, 0.09)"),
    # 3 POD: mas lechoso, menos caramelo
    ("color: vary(new THREE.Color(0xf2b3cc), 8, 0.03), roughness: 0.30 + (rnd(4) - 0.5) * 0.24",
     "color: vary(new THREE.Color(0xf3c4d5), 6, 0.03), roughness: 0.36 + (rnd(4) - 0.5) * 0.2"),
    ("transparent: true, opacity: 0.66 + (rnd(5) - 0.5) * 0.1,\n      emissive: 0xe08cae, emissiveIntensity: 0.14",
     "transparent: true, opacity: 0.74 + (rnd(5) - 0.5) * 0.08,\n      emissive: 0xf0d4de, emissiveIntensity: 0.22"),
    # 4 CUPULA/ETFE: membrana ligera con reticula (wireframe overlay se anade abajo)
    ("color: 0xedf3ea, roughness: 0.28, transparent: true, opacity: 0.42",
     "color: 0xf2f5ec, roughness: 0.22, transparent: true, opacity: 0.30"),
]
n = 0
for (a, b) in reps:
    if a in s:
        s = s.replace(a, b)
        n += 1

# 4b reticula de la cupula + 5 Casa de Correos dos tonos: inyectar tras crear mesh
marker = """  const mesh = new THREE.Mesh(g, matFor(o, gi));"""
inject = """  const mesh = new THREE.Mesh(g, matFor(o, gi));
  // E02-4b: reticula de membrana en la cupula (bbox grande en capa 06 cerca de 30.5,2)
  if (o.layer === '06_MEMBRANES') {
    let cx=0, cy=0, n0=o.V.length;
    for (const v of o.V) { cx+=v[0]; cy+=v[1]; }
    cx/=n0; cy/=n0;
    if (Math.abs(cx-30.5)<3 && Math.abs(cy-2)<3 && n0>120) {
      const wf = new THREE.LineSegments(new THREE.WireframeGeometry(g),
        new THREE.LineBasicMaterial({color: 0xb9b3a4, transparent: true, opacity: 0.6}));
      scene.add(wf);
    }
  }
  // E02-5: Casa de Correos con lectura material minima (dos tonos + reloj legible)
  if (o.layer === '00_CONTEXT') {
    let bx0=1e9,bx1=-1e9,by0=1e9,by1=-1e9,bz1=-1e9;
    for (const v of o.V){ if(v[0]<bx0)bx0=v[0]; if(v[0]>bx1)bx1=v[0]; if(v[1]<by0)by0=v[1]; if(v[1]>by1)by1=v[1]; if(v[2]>bz1)bz1=v[2]; }
    const enCorreos = bx0>-64 && bx1<20 && by0>-96 && by1<-28;
    if (enCorreos) {
      if (bz1 > 25.5 && (bx1-bx0) < 5) {            // esfera reloj / cupulin pequeno
        mesh.material = new THREE.MeshStandardMaterial({color: 0xf5efdf, roughness: 0.4, emissive: 0xf0e6c8, emissiveIntensity: 0.25});
      } else if (bz1 > 16.5) {                       // torre + cupulin
        mesh.material = new THREE.MeshStandardMaterial({color: 0xd9c4a4, roughness: 0.7});
      } else {                                       // cuerpo: ladrillo + granito
        mesh.material = new THREE.MeshStandardMaterial({color: 0xc4907a, roughness: 0.8});
      }
    }
  }"""
if marker in s and 'E02-4b' not in s:
    s = s.replace(marker, inject, 1)
    n += 1

open(p, 'w', encoding='utf-8').write(s)
print('parches E02 aplicados:', n)
