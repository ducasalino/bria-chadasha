import json

# 1. Carrega os dados do JSON
with open("produtos.json", "r", encoding="utf-8") as f:
    produtos = json.load(f)

# Tratamento para evitar erro caso venha uma lista aninhada
if isinstance(produtos, list) and len(produtos) > 0 and isinstance(produtos[0], list):
    produtos = produtos[0]

cards_html = ""
legendas_insta = []

# 2. Itera sobre os produtos para gerar os cards HTML e as legendas
for item in produtos:
    if not isinstance(item, dict):
        continue

    item_id = item.get("id", 1)
    nome = item.get("produto", "Produto Selecionado")
    preco = item.get("preco", "Consulte no link")
    link = item.get("link", "https://ducasalino.github.io/bria-chadasha/")
    imagem = item.get("imagem", "")

    # Monta o card para a vitrine HTML
    cards_html += f"""
      <a href="{link}" target="_blank" rel="noopener noreferrer" class="product-card">
        <img src="{imagem}" alt="{nome}" class="product-thumb" />
        <div class="product-info">
          <div class="product-name">{nome}</div>
          <div class="product-price">{preco}</div>
        </div>
        <span class="btn-buy">Ver Oferta</span>
      </a>
    """

    # Monta a legenda persuasiva para o post no Instagram
    legenda = f"""==================================================
PRODUTO #{item_id}: {nome}
==================================================
✨ ACHADINHO DO DIA | BRIÁ CHADASHÁ ✨

Procurando qualidade com o melhor preço do Mercado Livre? Olha esse achado incrível que garimpamos hoje!

🏷️ Produto: {nome}
💥 Valor Especial: {preco}
🚚 Compra 100% segura e entrega rápida!

👉 COMO COMPRAR:
1. Acesse o link no nosso perfil (@briachadasha / Bio)
2. Toque no produto #{item_id} para ir direto à oferta oficial no Mercado Livre!

📲 Comente "EU QUERO" que te enviamos o link no direct!
.
.
#achadinhos #mercadolivre #ofertadodia #comprasonline #descontos #briachadasha #achadinhosmercadolivre
\n"""
    legendas_insta.append(legenda)

# 3. Monta o template completo do index.html
html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Briá Chadashá | Vitrine de Ofertas</title>
  <style>
    :root {{
      --bg: #F4F1EA;
      --card-bg: #FFFFFF;
      --primary: #0A2540;
      --accent: #E05A47;
      --text-muted: #556B82;
      --border: #E2DDD5;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    body {{
      background-color: var(--bg);
      color: var(--primary);
      display: flex;
      justify-content: center;
      padding: 32px 16px;
    }}
    .container {{
      width: 100%;
      max-width: 440px;
      text-align: center;
    }}
    .brand-title {{
      font-size: 1.3rem;
      letter-spacing: 2px;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--primary);
    }}
    .brand-subtitle {{
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-top: 4px;
      margin-bottom: 24px;
    }}
    .product-list {{
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    .product-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px 14px;
      text-decoration: none;
      color: inherit;
      display: flex;
      align-items: center;
      gap: 12px;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
      box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }}
    .product-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(10, 37, 64, 0.08);
    }}
    .product-thumb {{
      width: 58px;
      height: 58px;
      border-radius: 8px;
      object-fit: contain;
      background-color: #FAFAFA;
      border: 1px solid var(--border);
      flex-shrink: 0;
    }}
    .product-info {{
      text-align: left;
      flex-grow: 1;
    }}
    .product-name {{
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--primary);
      line-height: 1.25;
    }}
    .product-price {{
      font-size: 1rem;
      font-weight: 700;
      color: var(--accent);
      margin-top: 4px;
    }}
    .btn-buy {{
      background-color: var(--primary);
      color: #FFF;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 0.75rem;
      font-weight: 600;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    footer {{
      margin-top: 32px;
      font-size: 0.75rem;
      color: var(--text-muted);
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="logo-container">
      <h1 class="brand-title">Briá Chadashá</h1>
      <p class="brand-subtitle">Achadinhos & Ofertas Selecionadas</p>
    </div>

    <div class="product-list">
{cards_html}
    </div>

    <footer>
      <p>✨ "Eis que tudo se fez novo."</p>
    </footer>
  </div>
</body>
</html>
"""

# 4. Salva o HTML da vitrine
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

# 5. Salva as legendas em um arquivo de texto
with open("legendas_instagram.txt", "w", encoding="utf-8") as f:
    f.writelines(legendas_insta)

print("✅ Tudo pronto!")
print("📄 Vitrine index.html atualizada com sucesso.")
print("📝 Arquivo 'legendas_instagram.txt' gerado com as legendas para o feed!")