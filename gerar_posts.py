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

# 3. Monta o template da página com o novo fundo elegante e marca d'água
html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Briá Chadashá | Vitrine de Ofertas</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }}
        body {{
            /* Fundo gradiente com iluminação sutil no centro superior */
            background: radial-gradient(circle at 50% 0%, #eef5fc 0%, #f7f6f2 75%);
            background-attachment: fixed;
            color: #1a202c;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }}

        /* Marca d'água elegante da Briá Chadashá no fundo */
        body::before {{
            content: "BRIÁ CHADASHÁ";
            position: fixed;
            top: 45%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-12deg);
            font-size: clamp(3rem, 9vw, 8rem);
            font-weight: 900;
            letter-spacing: 12px;
            color: rgba(11, 37, 69, 0.035);
            white-space: nowrap;
            pointer-events: none;
            z-index: 0;
            user-select: none;
        }}

        header {{
            text-align: center;
            margin-bottom: 35px;
            position: relative;
            z-index: 1;
        }}
        h1 {{
            font-size: 2rem;
            font-weight: 900;
            letter-spacing: 3px;
            color: #0b2545;
            text-transform: uppercase;
        }}
        p.subtitle {{
            font-size: 0.95rem;
            color: #5c6b73;
            margin-top: 6px;
            letter-spacing: 0.5px;
        }}

        /* Grid dos produtos */
        .container {{
            width: 100%;
            max-width: 1150px;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
            position: relative;
            z-index: 1;
        }}
        .card {{
            background: #ffffff;
            border-radius: 14px;
            padding: 16px;
            display: flex;
            align-items: center;
            gap: 16px;
            border: 1px solid rgba(11, 37, 69, 0.06);
            box-shadow: 0 4px 14px rgba(11, 37, 69, 0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }}
        .card:hover {{
            transform: translateY(-3px);
            border-color: rgba(11, 37, 69, 0.15);
            box-shadow: 0 8px 20px rgba(11, 37, 69, 0.08);
        }}
        .card-img {{
            width: 78px;
            height: 78px;
            object-fit: cover;
            border-radius: 10px;
            background-color: #f1f5f9;
            flex-shrink: 0;
        }}
        .card-info {{
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            overflow: hidden;
        }}
        .card-title {{
            font-size: 0.92rem;
            font-weight: 600;
            color: #1e293b;
            line-height: 1.35;
            margin-bottom: 6px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .card-price {{
            font-size: 1.1rem;
            font-weight: 800;
            color: #d9531e;
        }}
        .btn-oferta {{
            background-color: #0b2545;
            color: #ffffff;
            text-decoration: none;
            padding: 10px 18px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            white-space: nowrap;
            transition: background 0.2s ease, transform 0.1s ease;
            flex-shrink: 0;
        }}
        .btn-oferta:hover {{
            background-color: #134074;
            transform: scale(1.02);
        }}
        footer {{
            margin-top: 50px;
            text-align: center;
            font-size: 0.85rem;
            color: #8da9c4;
            position: relative;
            z-index: 1;
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
print(" Vitrine index.html atualizada com o novo fundo e marca d'água!")
print(" Arquivo 'legendas_instagram.txt' atualizado!")