# -*- coding: utf-8 -*-
"""Publica o cardapio novo: JSON do painel -> template -> index.html -> GitHub.

Faz sozinho o que antes era feito a mao:
  1. acha o arquivo cardapio-boteco.json (Downloads ou pasta do projeto)
  2. aplica no template.html
  3. gera o index.html e o QR
  4. manda para o GitHub (o site atualiza em ~1 minuto)

Uso:  PUBLICAR.bat            (acha o JSON mais recente sozinho)
      PUBLICAR.bat arquivo.json
      arrastar o arquivo .json em cima do PUBLICAR.bat
"""
import glob, io, os, subprocess, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://cuca33.github.io/boteco-do-joao/"
PY = sys.executable


def passo(txt):
    print("\n>> " + txt)


def rodar(*args):
    r = subprocess.run(args, cwd=BASE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    saida = (r.stdout or "") + (r.stderr or "")
    if saida.strip():
        print("   " + saida.strip().replace("\n", "\n   "))
    if r.returncode != 0:
        raise SystemExit("\nPAROU AQUI. Nada foi publicado. Manda esse texto para o Diego.")
    return saida


def achar_json():
    if len(sys.argv) > 1 and sys.argv[1].strip():
        alvo = sys.argv[1].strip().strip('"')
        if not os.path.exists(alvo):
            raise SystemExit("Nao achei o arquivo: " + alvo)
        return alvo

    pastas = [BASE, os.path.join(os.path.expanduser("~"), "Downloads")]
    achados = []
    for p in pastas:
        achados += glob.glob(os.path.join(p, "cardapio*.json"))
    if not achados:
        raise SystemExit(
            "Nao achei nenhum cardapio*.json.\n"
            "No celular: painel do dono -> Publicar -> Baixar arquivo,\n"
            "manda o arquivo para o PC e arrasta ele em cima do PUBLICAR.bat.")
    return max(achados, key=os.path.getmtime)


print("=" * 58)
print("  PUBLICAR O CARDAPIO DO BOTECO DO JOAO")
print("=" * 58)

arquivo = achar_json()
print("\nArquivo do cardapio: " + arquivo)
print("Salvo em            : " + time.strftime("%d/%m/%Y %H:%M", time.localtime(os.path.getmtime(arquivo))))
print("\nConfira a data acima: tem que ser a do cardapio que voce acabou de exportar.")
if input("Publicar esse cardapio? (s = sim) ").strip().lower() not in ("s", "sim", "y"):
    raise SystemExit("\nCancelado. Nada foi publicado.")

passo("1/4  aplicando o cardapio novo no template")
rodar(PY, os.path.join(BASE, "aplicar.py"), arquivo)

passo("2/4  gerando a pagina e o QR Code")
rodar(PY, os.path.join(BASE, "build.py"), SITE)

passo("3/4  gerando o cartaz das mesas")
rodar(PY, os.path.join(BASE, "cartaz.py"), SITE)

passo("4/4  mandando para o site")
mudou = rodar("git", "status", "--porcelain").strip()
if not mudou:
    print("   Nada mudou — o site ja esta com esse cardapio.")
else:
    rodar("git", "add", "-A")
    rodar("git", "-c", "user.name=Diego", "-c", "user.email=diegocuca@hotmail.com",
          "commit", "-m", "Cardapio atualizado em " + time.strftime("%d/%m/%Y %H:%M"))
    rodar("git", "push", "origin", "main")
    print("   Enviado.")

print("\n" + "=" * 58)
print("  PRONTO!")
print("  O cardapio novo entra no ar em ate 1 minuto:")
print("  " + SITE)
print("  O QR Code das mesas continua o mesmo - nao precisa reimprimir.")
print("=" * 58)
