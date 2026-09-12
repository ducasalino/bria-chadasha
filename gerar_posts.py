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

    # Card HTML da vitrine (com data-title para busca rápida)
    cards_html += f"""
        <div class="card" data-title="{nome.lower()}">
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

# 3. Template com barra de pesquisa interativa
html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Briá Chadashá | Ofertas & Achados</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        body {{
            background-color: #f4efe6;
            background-image: radial-gradient(circle at 50% 0%, #ffffff 0%, #f4efe6 80%);
            background-attachment: fixed;
            color: #1a202c;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 30px 20px;
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }}

        /* Marca d'água sutil ao fundo */
        body::before {{
            content: "";
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: min(85vw, 650px);
            height: min(85vw, 650px);
            background-image: url('fotos/fotos/logo.png');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            opacity: 0.04;
            pointer-events: none;
            z-index: 0;
        }}

        header {{
            text-align: center;
            margin-bottom: 25px;
            position: relative;
            z-index: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .logo-frame {{
            width: 140px;
            height: 140px;
            border-radius: 20px;
            background: #ffffff;
            padding: 8px;
            box-shadow: 0 10px 25px rgba(11, 37, 69, 0.08);
            border: 1px solid rgba(11, 37, 69, 0.08);
            margin-bottom: 12px;
            transition: transform 0.3s ease;
        }}
        .logo-frame:hover {{
            transform: scale(1.03);
        }}
        .logo-frame img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            border-radius: 14px;
        }}

        h1 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            letter-spacing: 6px;
            color: #0b2545;
            text-transform: uppercase;
            margin-top: 4px;
        }}
        p.subtitle {{
            font-family: 'Montserrat', sans-serif;
            font-size: 0.85rem;
            color: #d65a44;
            font-weight: 600;
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-top: 6px;
        }}

        /* Barra de pesquisa */
        /* Barra de pesquisa mais esticada e fina */
        .search-container {
            width: 100%;
            max-width: 680px;
            margin-bottom: 28px;
            position: relative;
            z-index: 2;
        }
        .search-input {
            width: 100%;
            padding: 9px 18px 9px 40px;
            border-radius: 20px;
            border: 1px solid rgba(11, 37, 69, 0.12);
            background: #ffffff;
            font-size: 0.88rem;
            font-weight: 400;
            color: #1a202c;
            box-shadow: 0 2px 8px rgba(11, 37, 69, 0.04);
            outline: none;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        .search-input:focus {
            border-color: #0b2545;
            box-shadow: 0 4px 14px rgba(11, 37, 69, 0.08);
        }
        .search-icon {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.85rem;
            color: #8da9c4;
            pointer-events: none;
        }

        /* Mensagem quando nenhum produto é encontrado */
        .empty-search {{
            display: none;
            text-align: center;
            color: #5c6b73;
            font-size: 1rem;
            margin-top: 20px;
            width: 100%;
            grid-column: 1 / -1;
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
            border-radius: 16px;
            padding: 16px;
            display: flex;
            align-items: center;
            gap: 16px;
            border: 1px solid rgba(11, 37, 69, 0.07);
            box-shadow: 0 4px 16px rgba(11, 37, 69, 0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }}
        .card:hover {{
            transform: translateY(-3px);
            border-color: rgba(11, 37, 69, 0.18);
            box-shadow: 0 10px 24px rgba(11, 37, 69, 0.08);
        }}
        .card-img {{
            width: 80px;
            height: 80px;
            object-fit: cover;
            border-radius: 10px;
            background-color: #f7f6f2;
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
            color: #1a202c;
            line-height: 1.35;
            margin-bottom: 6px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .card-price {{
            font-size: 1.15rem;
            font-weight: 800;
            color: #d65a44;
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
            background-color: #14365d;
            transform: scale(1.02);
        }}
        footer {{
            margin-top: 55px;
            text-align: center;
            font-size: 0.85rem;
            color: #7b8e9b;
            position: relative;
            z-index: 1;
        }}
    </style>
</head>
<body>
    <header>
        <div class="logo-frame">
            <img src="fotos/fotos/logo.png" alt="Briá Chadashá">
        </div>
        <h1>Briá Chadashá</h1>
        <p class="subtitle">Ofertas & Achados</p>
    </header>

    <!-- Caixa de Busca -->
    <div class="search-container">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" class="search-input" placeholder="Buscar achadinho por nome...">
    </div>

    <main class="container" id="productsGrid">
        {cards_html}
        <div id="emptyMessage" class="empty-search">Nenhum produto encontrado para sua busca.</div>
    </main>

    <footer>
        ✨ "Eis que tudo se fez novo."
    </footer>

    <!-- Script de Busca Instantânea -->
    <script>
        const searchInput = document.getElementById('searchInput');
        const cards = document.querySelectorAll('.card');
        const emptyMessage = document.getElementById('emptyMessage');

        searchInput.addEventListener('input', (e) => {{
            const termo = e.target.value.toLowerCase().trim();
            let visiveis = 0;

            cards.forEach(card => {{
                const titulo = card.getAttribute('data-title');
                if (titulo.includes(termo)) {{
                    card.style.display = 'flex';
                    visiveis++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            emptyMessage.style.display = (visiveis === 0) ? 'block' : 'none';
        }});
    </script>
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
print(" Vitrine index.html atualizada com barra de busca instantânea!")
print(" Arquivo 'legendas_instagram.txt' atualizado!")