# -*- coding: utf-8 -*-
import io, os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.html")
with io.open(p, encoding="utf-8") as f:
    linhas = f.readlines()

nova = 'const semAcento = s => s.normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").toLowerCase();\n'
alvo = 'const semAcento'
achou = 0
for i, l in enumerate(linhas):
    if l.lstrip().startswith(alvo):
        linhas[i] = nova
        achou += 1

# garante <meta charset> logo no topo
if not any("charset" in l for l in linhas[:3]):
    linhas.insert(0, '<meta charset="utf-8">\n')

with io.open(p, "w", encoding="utf-8", newline="") as f:
    f.writelines(linhas)

with io.open(p, encoding="utf-8") as f:
    txt = f.read()
print("linhas trocadas:", achou, "| tem u0300:", "u0300" in txt, "| tem charset:", "charset" in txt[:60])
