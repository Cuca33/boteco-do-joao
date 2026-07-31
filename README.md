# Boteco do João — cardápio digital

Cardápio online do **Boteco do João** ("sua casa fora de casa"), feito para abrir no
celular pelo QR Code das mesas.

**No ar:** https://cuca33.github.io/boteco-do-joao/

- 22 seções, ~180 produtos, busca por nome **ou pelo código do sistema**
- comanda que soma e manda o pedido pronto pelo WhatsApp — (71) 99123-2952
- tema claro/escuro automático; imprimir a página imprime só o QR Code
- **painel do dono** para editar preços e produtos direto no celular

## Painel do dono

Entra com **5 toques no logo** da capa ou abrindo o link com `#dono` no fim.

Dá para editar nome/preço/código/descrição de qualquer item, adicionar e apagar
produtos e seções, reordenar e aplicar reajuste em % (no cardápio inteiro ou numa
seção só).

As alterações ficam guardadas **no aparelho de quem editou** (`localStorage`) — a
página é estática, não tem servidor. Para os clientes verem, use o botão
**Publicar**, guarde o JSON e publique de novo (abaixo).

## Publicar uma versão nova

```bash
python aplicar.py cardapio-boteco.json          # aplica o JSON exportado no template
python build.py "https://cuca33.github.io/boteco-do-joao/"
git commit -am "cardapio novo" && git push      # o GitHub Pages atualiza sozinho
```

O endereço nunca muda, então **o QR Code impresso continua valendo**.

## Arquivos

| arquivo | para que serve |
| --- | --- |
| `template.html` | fonte — dados no array `CARDAPIO_PADRAO`, ajustes em `CONFIG` |
| `build.py` | gera o `index.html` (embute as imagens, desenha o QR, carimba a versão) |
| `aplicar.py` | pega o JSON exportado pelo painel e reescreve o `CARDAPIO_PADRAO` |
| `index.html` | página publicada (gerada — não editar à mão) |
| `qrcode.png` / `qrcode.svg` | QR solto, para cartaz ou gráfica |
| `hero.b64` / `logo.b64` | imagens da capa em base64 |
