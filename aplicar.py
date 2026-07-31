# -*- coding: utf-8 -*-
"""Aplica no template.html o cardapio exportado pelo painel do dono.

O Joao Vitor edita no celular -> toca em "Publicar" -> "Copiar dados" ou
"Baixar arquivo" -> manda o JSON. Aqui esse JSON vira o CARDAPIO_PADRAO
do template, e depois basta rodar o build.py e republicar o index.html.

Uso:  python aplicar.py cardapio-boteco.json
      python build.py "https://claude.ai/code/artifact/9b590b67-a016-4f5d-8b24-ba354eace2d4"
"""
import io, json, os, re, shutil, sys

BASE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(BASE, "template.html")

if len(sys.argv) < 2:
    raise SystemExit("uso: python aplicar.py <arquivo.json>")

dados = json.loads(io.open(sys.argv[1], encoding="utf-8-sig").read())

# ---- validacao: melhor recusar do que publicar cardapio quebrado ----
if not isinstance(dados, list) or not dados:
    raise SystemExit("JSON invalido: esperava uma lista de secoes")
total = 0
for sec in dados:
    if not isinstance(sec, dict) or not sec.get("nome") or not isinstance(sec.get("itens"), list):
        raise SystemExit("secao invalida: %r" % (sec,))
    for it in sec["itens"]:
        if not isinstance(it, dict) or not it.get("nome"):
            raise SystemExit("item invalido na secao %s: %r" % (sec["nome"], it))
        p = it.get("preco", None)
        if p is not None and not isinstance(p, (int, float)):
            raise SystemExit("preco invalido em %s: %r" % (it["nome"], p))
        total += 1


def txt(s):
    """String JS segura (json.dumps ja escapa aspas, barras e quebras)."""
    return json.dumps(s, ensure_ascii=False)


def preco(p):
    return "null" if p is None else "%.2f" % float(p)


linhas = ["const CARDAPIO_PADRAO = ["]
for si, sec in enumerate(dados):
    cab = " {id:%s, nome:%s" % (txt(sec.get("id") or "s%d" % si), txt(sec["nome"]))
    if sec.get("destaque"):
        cab += ", destaque:true"
    if sec.get("faixa"):
        cab += ", faixa:true"
    if sec.get("nota"):
        cab += ", nota:%s" % txt(sec["nota"])
    linhas.append(cab + ", itens:[")
    corpo = []
    for it in sec["itens"]:
        partes = ["cod:%s" % txt(it.get("cod") or ""),
                  "nome:%s" % txt(it["nome"]),
                  "preco:%s" % preco(it.get("preco", None))]
        if it.get("desc"):
            partes.append("desc:%s" % txt(it["desc"]))
        corpo.append("   {%s}" % ", ".join(partes))
    linhas.append(",\n".join(corpo))
    linhas.append(" ]}," if si < len(dados) - 1 else " ]}")
linhas.append("];")
novo = "\n".join(linhas)

tpl = io.open(TPL, encoding="utf-8").read()
padrao = re.compile(r"const CARDAPIO_PADRAO = \[.*?\n\];", re.S)
if not padrao.search(tpl):
    raise SystemExit("nao achei o bloco CARDAPIO_PADRAO no template.html")

shutil.copy(TPL, TPL + ".bak")
io.open(TPL, "w", encoding="utf-8").write(padrao.sub(lambda m: novo, tpl, count=1))
print("template.html atualizado: %d secoes, %d itens (backup em template.html.bak)"
      % (len(dados), total))
print("agora rode:  python build.py \"<URL do cardapio>\"")
