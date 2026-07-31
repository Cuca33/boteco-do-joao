# -*- coding: utf-8 -*-
"""Gera o index.html final do cardapio: injeta as imagens (base64) e o QR Code.

Uso:  python build.py [URL_DA_PAGINA]
"""
import datetime, io, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = r"C:\Users\User\AppData\Local\Temp\claude\C--Users-User\21027e41-dec9-4bc1-ab46-5eb69e86f706\scratchpad"


def ler_b64(nome):
    """As imagens vivem na pasta do projeto; o scratchpad antigo e so reserva."""
    for pasta in (BASE, SCRATCH):
        caminho = os.path.join(pasta, nome)
        if os.path.exists(caminho):
            return io.open(caminho, encoding="utf-8").read().strip()
    raise SystemExit("nao achei " + nome)


url = sys.argv[1] if len(sys.argv) > 1 else ""

tpl = io.open(os.path.join(BASE, "template.html"), encoding="utf-8").read()
hero = ler_b64("hero.b64")
logo = ler_b64("logo.b64")

# carimbo da publicacao: muda a cada build e faz o celular do dono
# descartar o rascunho local quando uma versao nova entra no ar
versao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def qr_svg(dados, escala=1):
    """QR Code como SVG (path unico), sem dependencia externa no HTML."""
    import qrcode
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=1, border=2)
    qr.add_data(dados)
    qr.make(fit=True)
    m = qr.get_matrix()
    n = len(m)
    partes = []
    for y, linha in enumerate(m):
        x = 0
        while x < n:
            if linha[x]:
                x0 = x
                while x < n and linha[x]:
                    x += 1
                partes.append("M%d %dh%dv1h-%dz" % (x0, y, x - x0, x - x0))
            else:
                x += 1
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'shape-rendering="crispEdges" role="img" '
            'aria-label="QR Code do cardapio do Boteco do Joao">'
            '<rect width="%d" height="%d" fill="#fff"/>'
            '<path fill="#16130F" d="%s"/></svg>') % (n, n, n, n, "".join(partes))


if url:
    svg = qr_svg(url)
    rotulo = url
else:
    svg = ('<div style="width:200px;height:200px;display:grid;place-items:center;'
           'color:#888;font:600 13px system-ui;text-align:center">QR Code entra '
           'quando a p&aacute;gina for publicada</div>')
    rotulo = "publicando..."

saida = (tpl.replace("__HERO_B64__", hero)
            .replace("__LOGO_B64__", logo)
            .replace("__QR_SVG__", svg)
            .replace("__QR_URL__", rotulo)
            .replace("__VERSAO__", versao))

destino = os.path.join(BASE, "index.html")
io.open(destino, "w", encoding="utf-8").write(saida)
print("gerado:", destino, len(saida), "bytes | url:", url or "(sem url ainda)",
      "| versao:", versao)

# copia solta do QR para imprimir/usar em cartaz
if url:
    io.open(os.path.join(BASE, "qrcode.svg"), "w", encoding="utf-8").write(svg)
    try:
        import qrcode
        img = qrcode.make(url, box_size=20, border=2)
        img.save(os.path.join(BASE, "qrcode.png"))
        print("qrcode.svg + qrcode.png gerados")
    except Exception as e:
        print("png falhou:", e)
