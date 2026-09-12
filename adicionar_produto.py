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
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}

def limpar_slug(texto):
    texto = texto.lower()
    texto = re.sub(r"[^\w\s-]", "", texto)
    texto = re.sub(r"[\s_-]+", "_", texto).strip("_")
    return texto[:25] if texto else "produto"

def extrair_dados_ml(url):
    print("\n🔍 Acessando anúncio...")
    session = requests.Session()
    res = session.get(url, headers=HEADERS, allow_redirects=True, timeout=15)
    
    if res.status_code != 200:
        print(f"❌ Erro HTTP {res.status_code}")
        return None

    soup = BeautifulSoup(res.text, "html.parser")

    # 1. Título com múltiplos métodos de captura
    titulo = ""
    tag_h1 = soup.find("h1", class_="ui-pdp-title")
    if tag_h1 and tag_h1.text.strip():
        titulo = tag_h1.text.strip()
    
    if not titulo:
        meta_og = soup.find("meta", property="og:title")
        if meta_og and meta_og.get("content"):
            titulo = meta_og["content"].strip()
            
    if not titulo:
        tag_title = soup.find("title")
        if tag_title and tag_title.text:
            titulo = tag_title.text.split("|")[0].split("-")[0].strip()

    # 2. Imagem
    url_imagem = None
    meta_img = soup.find("meta", property="og:image")
    if meta_img and meta_img.get("content"):
        url_imagem = meta_img["content"]
    else:
        img_pdp = soup.find("img", class_="ui-pdp-image")
        if img_pdp and img_pdp.get("src"):
            url_imagem = img_pdp["src"]

    # 3. Preço
    preco = ""
    meta_price = soup.find("meta", itemprop="price")
    if meta_price and meta_price.get("content"):
        val = meta_price["content"].replace(".", ",")
        preco = f"R$ {val}"
    else:
        frac = soup.find("span", class_="andes-money-amount__fraction")
        preco = f"R$ {frac.text.strip()}" if frac else "Consulte"

    return {
        "titulo": titulo,
        "preco": preco,
        "url_imagem": url_imagem,
        "link": url
    }

def main():
    link_afiliado = input("\nCole o link de afiliado: ").strip()
    if not link_afiliado:
        print("Link não informado.")
        return

    dados = extrair_dados_ml(link_afiliado)
    if not dados:
        return

    # Se o título veio vazio ou genérico, solicita digitação
    titulo_sugerido = dados["titulo"]
    print(f"\n📦 Título capturado: '{titulo_sugerido}'")
    titulo_final = input("Aperte ENTER para manter ou digite o nome do produto: ").strip()
    if not titulo_final:
        titulo_final = titulo_sugerido if titulo_sugerido else "Produto Sem Nome"

    print(f"💲 Preço: {dados['preco']}")

    caminho_json = "produtos.json"
    produtos = []
    if os.path.exists(caminho_json):
        with open(caminho_json, "r", encoding="utf-8") as f:
            produtos = json.load(f)

    proximo_id = len(produtos) + 1

    # Salva com ID único no nome do arquivo para nunca sobrescrever
    slug = limpar_slug(titulo_final)
    nome_foto = f"item_{proximo_id}_{slug}.png"
    caminho_pasta_fotos = os.path.join("fotos", "fotos")
    os.makedirs(caminho_pasta_fotos, exist_ok=True)
    
    caminho_salvar_foto = os.path.join(caminho_pasta_fotos, nome_foto)
    caminho_relativo = f"fotos/fotos/{nome_foto}".replace("\\", "/")

    if dados["url_imagem"]:
        print(f"⬇️  Baixando imagem...")
        try:
            r_img = requests.get(dados["url_imagem"], headers=HEADERS, timeout=10)
            if r_img.status_code == 200:
                with open(caminho_salvar_foto, "wb") as f_img:
                    f_img.write(r_img.content)
                print(f"🖼️ Foto salva: {nome_foto}")
        except Exception as e:
            print(f"Erro ao baixar imagem: {e}")

    novo_item = {
        "id": proximo_id,
        "produto": titulo_final,
        "preco": dados["preco"],
        "comissao": "Oferta",
        "link": link_afiliado,
        "imagem": caminho_relativo
    }

    produtos.append(novo_item)

    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Produto #{proximo_id} inserido com sucesso!")
    subprocess.run(["python", "gerar_posts.py"])

if __name__ == "__main__":
    main()