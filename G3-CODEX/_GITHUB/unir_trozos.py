#!/usr/bin/env python3
"""Reconstruye los archivos que se partieron en trozos de 24 MiB para poder subirlos a GitHub.
Uso (desde la raíz del repo):  python3 _GITHUB/unir_trozos.py
Lee _GITHUB/TROZOS.tsv, une cada archivo en su ruta original y comprueba su SHA-256.
Los trozos (.parteNNNdeMMM) se pueden borrar después; el .gitignore ya ignora los archivos reconstruidos."""
import csv, hashlib, os, sys
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = mal = 0
with open(os.path.join(raiz, '_GITHUB', 'TROZOS.tsv'), encoding='utf-8') as f:
    for fila in csv.DictReader(f, delimiter='\t'):
        destino = os.path.join(raiz, fila['ruta'])
        n = int(fila['trozos'])
        h = hashlib.sha256()
        with open(destino + '.tmp', 'wb') as out:
            for k in range(1, n + 1):
                with open(f"{destino}.parte{k:03d}de{n:03d}", 'rb') as t:
                    b = t.read(); h.update(b); out.write(b)
        if fila['sha256'] and h.hexdigest() != fila['sha256']:
            mal += 1; print('NO COINCIDE', fila['ruta']); os.remove(destino + '.tmp'); continue
        os.replace(destino + '.tmp', destino); ok += 1
print(f'{ok} archivos reconstruidos, {mal} con error')
