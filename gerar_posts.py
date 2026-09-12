import json

# 1. Carrega os produtos do arquivo JSON
with open("produtos.json", "r", encoding="utf-8") as f:
    produtos = json.load(f)

# 2. Gera os cards HTML e as legendas para o Instagram
cards_html = ""
legendas_insta = []

for item in produtos:
    item_id = item["id"]
    nome = item["produto"]
    preco = item["preco"]
    comissao = item["comissao"]
    link = item["link"]
    imagem = item["imagem"]

    # Card HTML da vitrine
    cards_html += f"""
        <div class="card">
            <img src="{imagem}" alt="{nome}" class="card-img">
            <div class="card-info">
                <h3 class="card-title">{nome}</h3>
                <span class="card-price">{preco}</span>
            </div>
            <a href="{link}" target="_blank" rel="noopener noreferrer" class="btn-oferta">Ver Oferta</a>
        </div>
    """

    # Legenda para Instagram
    legenda = f"""----------------------------------------
PRODUTO #{item_id}: {nome}
----------------------------------------
Achadinho imperdível no Mercado Livre! 🔥

✨ {nome}
💰 Por apenas: {preco} ({comissao})

👉 Para garantir o seu, clique no link da bio e busque pelo produto #{item_id} ou acesse direto:
{link}

#achadinhos #mercadolivre #promocao #ofertas #compras
\n"""
    legendas_insta.append(legenda)

# 3. Monta o template da página com Grid responsivo (Lado a Lado no PC)
html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Briá Chadashá | Vitrine de Ofertas</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }}
        body {{
            background-color: #f7f5f0;
            color: #1a202c;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
            min-height: 100vh;
        }}
        header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        h1 {{
            font-size: 1.8rem;
            font-weight: 700;
            letter-spacing: 2px;
            color: #0b2545;
            text-transform: uppercase;
        }}
        p.subtitle {{
            font-size: 0.95rem;
            color: #718096;
            margin-top: 5px;
        }}
        /* Grid responsivo: organiza lado a lado */
        .container {{
            width: 100%;
            max-width: 1100px;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
        }}
        .card {{
            background: #ffffff;
            border-radius: 12px;
            padding: 16px;
            display: flex;
            align-items: center;
            gap: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
        }}
        .card-img {{
            width: 75px;
            height: 75px;
            object-fit: cover;
            border-radius: 8px;
            background-color: #edf2f7;
            flex-shrink: 0;
        }}
        .card-info {{
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        .card-title {{
            font-size: 0.95rem;
            font-weight: 600;
            color: #2d3748;
            line-height: 1.3;
            margin-bottom: 6px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .card-price {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #dd6b20;
        }}
        .btn-oferta {{
            background-color: #0b2545;
            color: #ffffff;
            text-decoration: none;
            padding: 10px 16px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            white-space: nowrap;
            transition: background 0.2s ease;
            flex-shrink: 0;
        }}
        .btn-oferta:hover {{
            background-color: #134074;
        }}
        footer {{
            margin-top: 40px;
            text-align: center;
            font-size: 0.85rem;
            color: #a0aec0;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Briá Chadashá</h1>
        <p class="subtitle">Achadinhos & Ofertas Selecionadas</p>
    </header>

    <main class="container">
        {cards_html}
    </main>

    <footer>
        ✨ "Eis que tudo se fez novo."
    </footer>
</body>
</html>
"""

# 4. Salva a vitrine index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

# 5. Salva as legendas
with open("legendas_instagram.txt", "w", encoding="utf-8") as f:
    f.writelines(legendas_insta)

print(" Tudo pronto!")
print(" Vitrine index.html atualizada em formato Grid (lado a lado)!")
print(" Arquivo 'legendas_instagram.txt' gerado com sucesso!")