# -*- coding: utf-8 -*-
"""Gera o cartaz das mesas com o QR Code do cardapio.

Sai em PNG (para mandar pela grafica ou imprimir em casa) e em PDF A4.

Uso:  python cartaz.py ["URL do cardapio"]
"""
import io, os, sys

from PIL import Image, ImageDraw, ImageFont
import qrcode

BASE = os.path.dirname(os.path.abspath(__file__))
URL = sys.argv[1] if len(sys.argv) > 1 else "https://cuca33.github.io/boteco-do-joao/"

CREME = (246, 238, 223)
ESCURO = (28, 24, 17)
AMARELO = (242, 179, 46)
TIJOLO = (166, 61, 27)
CINZA = (110, 98, 80)

W, H = 2480, 3508          # A4 a 300 dpi
FONTES = r"C:\Windows\Fonts"


def fonte(arquivo, tamanho):
    return ImageFont.truetype(os.path.join(FONTES, arquivo), tamanho)


def centrado(d, y, texto, f, cor, espaco=0):
    if espaco:                      # letter-spacing na mao
        larg = sum(d.textlength(c, font=f) + espaco for c in texto) - espaco
        x = (W - larg) / 2
        for c in texto:
            d.text((x, y), c, font=f, fill=cor)
            x += d.textlength(c, font=f) + espaco
        return
    d.text((W / 2, y), texto, font=f, fill=cor, anchor="ma")


cartaz = Image.new("RGB", (W, H), CREME)
d = ImageDraw.Draw(cartaz)

# moldura
d.rectangle([70, 70, W - 70, H - 70], outline=AMARELO, width=14)
d.rectangle([110, 110, W - 110, H - 110], outline=ESCURO, width=3)

# logo (o mesmo recorte redondo com alfa que a pagina usa)
import base64
logo = Image.open(io.BytesIO(base64.b64decode(
    io.open(os.path.join(BASE, "logo.b64"), encoding="utf-8").read().strip()))).convert("RGBA")
lado = 620
logo = logo.resize((lado, lado), Image.LANCZOS)
cartaz.paste(logo, ((W - lado) // 2, 230), logo)

centrado(d, 950, "BOTECO DO JOÃO", fonte("georgiab.ttf", 150), ESCURO, espaco=10)
centrado(d, 1130, "sua casa fora de casa", fonte("georgia.ttf", 78), TIJOLO)

# faixa
d.rectangle([W / 2 - 560, 1290, W / 2 + 560, 1420], fill=AMARELO)
centrado(d, 1315, "CARDÁPIO DIGITAL", fonte("arialbd.ttf", 74), ESCURO, espaco=8)

# QR
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=24, border=2)
qr.add_data(URL)
qr.make(fit=True)
img_qr = qr.make_image(fill_color="#1C1811", back_color="white").convert("RGB")
lado_qr = 1180
img_qr = img_qr.resize((lado_qr, lado_qr), Image.NEAREST)
qx, qy = (W - lado_qr) // 2, 1560
d.rectangle([qx - 40, qy - 40, qx + lado_qr + 40, qy + lado_qr + 40], fill="white", outline=ESCURO, width=4)
cartaz.paste(img_qr, (qx, qy))

y = qy + lado_qr + 150
centrado(d, y, "Aponte a câmera do celular", fonte("georgiab.ttf", 96), ESCURO)
centrado(d, y + 140, "e o cardápio abre na hora", fonte("georgia.ttf", 84), CINZA)

d.line([W / 2 - 600, y + 300, W / 2 + 600, y + 300], fill=AMARELO, width=6)
centrado(d, y + 340, URL.replace("https://", ""), fonte("arial.ttf", 50), CINZA)

png = os.path.join(BASE, "cartaz-mesa.png")
pdf = os.path.join(BASE, "cartaz-mesa.pdf")
cartaz.save(png, optimize=True)
cartaz.save(pdf, "PDF", resolution=300.0)
print("gerado:", png)
print("gerado:", pdf, "(A4, 300 dpi)")
print("url no QR:", URL)
