import os

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, '_viewer', 'viewer_e01.html')
s = open(p, encoding='utf-8').read()
reps = [
    ("vary(new THREE.Color(0xb7d07e), 12, 0.05), roughness: 0.22",
     "vary(new THREE.Color(0xc6dc90), 10, 0.04), roughness: 0.22"),
    ("opacity: 0.55 + (rnd(6) - 0.5) * 0.14,\n      emissive: 0x9ec25a, emissiveIntensity: 0.20",
     "opacity: 0.50 + (rnd(6) - 0.5) * 0.12,\n      emissive: 0xb8d47e, emissiveIntensity: 0.45"),
    ("vary(new THREE.Color(0xb08055), 4, 0.05)", "vary(new THREE.Color(0xbfa078), 4, 0.05)"),
    ("vary(new THREE.Color(0xb08055), 4, 0.06)", "vary(new THREE.Color(0xbfa078), 4, 0.05)"),
    ("color: 0xe0508e, roughness: 0.35", "color: 0xe06b9c, roughness: 0.42"),
    ("vary(new THREE.Color(0xf0a6c2), 8, 0.04)", "vary(new THREE.Color(0xf2b3cc), 8, 0.03)"),
    ("emissive: 0xd4688f, emissiveIntensity: 0.10", "emissive: 0xe08cae, emissiveIntensity: 0.14"),
    ("vary(new THREE.Color(0x5f8f4c), 16, 0.10)", "vary(new THREE.Color(0x6f9e59), 10, 0.06)"),
    ("color: 0x4a9a72, roughness: 0.08, transparent: true, opacity: 0.92, emissive: 0x2c6647, emissiveIntensity: 0.12",
     "color: 0x4a9a72, roughness: 0.08, transparent: true, opacity: 0.92, emissive: 0x3a7d5a, emissiveIntensity: 0.18"),
    ("color: 0x3e8a63, roughness: 0.08, transparent: true, opacity: 0.92, emissive: 0x2c6647, emissiveIntensity: 0.12",
     "color: 0x4a9a72, roughness: 0.08, transparent: true, opacity: 0.92, emissive: 0x3a7d5a, emissiveIntensity: 0.18"),
]
n = 0
for (a, b) in reps:
    if a in s:
        s = s.replace(a, b)
        n += 1
open(p, 'w', encoding='utf-8').write(s)
print('sustituciones aplicadas:', n)
