import os
import re
import json
import requests
from bs4 import BeautifulSoup
import subprocess

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}

def limpar_nome_arquivo(texto):
    """Gera um nome limpo para salvar a imagem localmente."""
    texto = texto.lower()
    texto = re.sub(r"[^\w\s-]", "", texto)
    texto = re.sub(r"[\s_-]+", "_", texto).strip("_")
    return texto[:30]

def capturar_dados_ml(url_afiliado):
    print("\n🔍 Acessando o anúncio no Mercado Livre...")
    session = requests.Session()
    response = session.get(url_afiliado, headers=HEADERS, allow_redirects=True, timeout=15)

    if response.status_code != 200:
        print(f"❌ Erro ao acessar o link: Código {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # 1. Título do Produto
    titulo_elem = (
        soup.find("h1", class_="ui-pdp-title")
        or soup.find("meta", property="og:title")
    )
    if titulo_elem:
        titulo = titulo_elem.text.strip() if hasattr(titulo_elem, "text") else titulo_elem.get("content", "")
    else:
        titulo = "Produto Selecionado"

    # 2. Imagem Principal
    img_elem = (
        soup.find("meta", property="og:image")
        or soup.find("img", class_="ui-pdp-image")
    )
    url_imagem = img_elem.get("content") or img_elem.get("src") if img_elem else None

    # 3. Preço Atual
    preco_elem = soup.find("meta", itemprop="price")
    if preco_elem and preco_elem.get("content"):
        preco_val = preco_elem["content"].replace(".", ",")
        preco = f"R$ {preco_val}"
    else:
        fracao = soup.find("span", class_="andes-money-amount__fraction")
        preco = f"R$ {fracao.text.strip()}" if fracao else "Consulte"

    return {
        "titulo": titulo,
        "preco": preco,
        "url_imagem": url_imagem,
        "link": url_afiliado
    }

def main():
    link_afiliado = input("\nCole o link de afiliado (meli.la ou mercadolivre): ").strip()
    if not link_afiliado:
        print("Link não informado.")
        return

    dados = capturar_dados_ml(link_afiliado)
    if not dados:
        return

    print(f"📦 Título: {dados['titulo']}")
    print(f"💲 Preço: {dados['preco']}")

    # 1. Ler catálogo existente
    caminho_json = "produtos.json"
    produtos = []
    if os.path.exists(caminho_json):
        with open(caminho_json, "r", encoding="utf-8") as f:
            produtos = json.load(f)

    proximo_id = len(produtos) + 1

    # 2. Salvar imagem automaticamente
    caminho_pasta_fotos = os.path.join("fotos", "fotos")
    os.makedirs(caminho_pasta_fotos, exist_ok=True)

    nome_base = limpar_nome_arquivo(dados["titulo"])
    nome_foto = f"{nome_base}.png"
    caminho_salvar_foto = os.path.join(caminho_pasta_fotos, nome_foto)
    caminho_relativo_foto = f"fotos/fotos/{nome_foto}".replace("\\", "/")

    if dados["url_imagem"]:
        print("⬇️  Baixando imagem principal...")
        try:
            img_resp = requests.get(dados["url_imagem"], headers=HEADERS, timeout=10)
            if img_resp.status_code == 200:
                with open(caminho_salvar_foto, "wb") as f_img:
                    f_img.write(img_resp.content)
                print(f"🖼️ Imagem salva com sucesso: {caminho_salvar_foto}")
        except Exception as e:
            print(f"Aviso ao baixar imagem: {e}")

    # 3. Adicionar item ao JSON
    novo_produto = {
        "id": proximo_id,
        "produto": dados["titulo"],
        "preco": dados["preco"],
        "comissao": "Oferta",
        "link": dados["link"],
        "imagem": caminho_relativo_foto
    }

    produtos.append(novo_produto)

    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=2)

    print(f"✅ Produto #{proximo_id} inserido em produtos.json!")

    # 4. Atualizar a vitrine HTML e as legendas
    print("⚙️  Regerando vitrine HTML...")
    subprocess.run(["python", "gerar_posts.py"])

    print("\n🎉 Concluído com sucesso! Agora é só enviar ao GitHub:")
    print('   git add . ; git commit -m "Adiciona novo achadinho" ; git push origin main\n')

if __name__ == "__main__":
    main()