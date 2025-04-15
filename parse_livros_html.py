import requests
from bs4 import BeautifulSoup
import os

# URL do backend para cadastrar livros
URL = "http://localhost:5000/cadastrar-livro"

# Função pra parsear um único arquivo HTML e extrair os livros
def parse_livros_html(arquivo_html):
    with open(arquivo_html, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    livros = []

    # Extrair o livro principal
    livro_principal = {}
    livro_principal['titulo'] = soup.find('h1', class_='text-2xl sm:text-3xl font-bold mb-2').text.strip()
    livro_principal['autor'] = soup.find('p', class_='text-lg text-muted-foreground mb-4').text.strip()
    preco_text = soup.find('span', class_='text-3xl font-bold').text.strip()
    preco = float(preco_text.replace('R$', '').replace(',', '.'))
    livro_principal['preco'] = preco
    img_tag = soup.find('img', alt=livro_principal['titulo'])
    livro_principal['imagem'] = img_tag['src'] if img_tag else ""
    desconto_tag = soup.find('div', class_='absolute top-2 right-2 z-10 bg-primary text-white text-xs font-bold px-2 py-1 rounded')
    livro_principal['desconto'] = desconto_tag.text.strip() if desconto_tag else ""
    descricao_div = soup.find('div', class_='prose prose-invert max-w-none')
    livro_principal['descricao'] = " ".join(p.text.strip() for p in descricao_div.find_all('p')) if descricao_div else f"Descrição genérica para {livro_principal['titulo']}."

    livros.append(livro_principal)

    # Extrair os livros da seção "Você também pode gostar"
    carousel = soup.find('div', class_='darkside-container').find('div', recursive=False).find_next_sibling()
    if carousel:
        carousel_items = carousel.find_all('div', class_='book-card p-2 group')
        for item in carousel_items:
            livro = {}
            livro['titulo'] = item.find('h1', class_='text-2xl sm:text-3xl font-bold mb-2') or item.find('h3', class_='font-bold text-sm leading-tight mb-1').text.strip()
            livro['autor'] = item.find('p', class_='text-lg text-muted-foreground mb-4') or item.find('p', class_='text-xs text-muted-foreground mb-2').text.strip()
            preco_tag = item.find('p', class_='font-bold')
            preco_text = preco_tag.text.strip() if preco_tag else item.find('div', class_='flex items-baseline gap-1').find('p').text.strip()
            preco = float(preco_text.replace('R$', '').replace(',', '.'))
            livro['preco'] = preco
            img_tag = item.find('img', class_='book-card-image object-cover rounded')
            livro['imagem'] = img_tag['src'] if img_tag else ""
            desconto_tag = item.find('div', class_='absolute top-2 right-2 z-10')
            livro['desconto'] = desconto_tag.text.strip() if desconto_tag else ""
            livro['descricao'] = f"Descrição genérica para {livro['titulo']}."

            livros.append(livro)

    return livros

# Função pra cadastrar os livros
def cadastrar_livros(livros):
    for livro in livros:
        livro_data = {
            "titulo": livro['titulo'],
            "descricao": livro['descricao'],
            "preco": livro['preco'],
            "imagem": livro['imagem'],
            "desconto": livro['desconto']
        }
        try:
            response = requests.post(URL, json=livro_data)
            if response.status_code == 201:
                print(f"Livro '{livro['titulo']}' cadastrado com sucesso!")
            else:
                print(f"Erro ao cadastrar '{livro['titulo']}': {response.text}")
        except Exception as e:
            print(f"Erro ao cadastrar '{livro['titulo']}': {str(e)}")

if __name__ == "__main__":
    # Pasta onde os arquivos HTML estão
    pasta_html = "html_files"

    # Criar a pasta se não existir
    if not os.path.exists(pasta_html):
        os.makedirs(pasta_html)

    # Listar todos os arquivos HTML na pasta
    arquivos_html = [f for f in os.listdir(pasta_html) if f.endswith('.html')]

    if not arquivos_html:
        print(f"Nenhum arquivo HTML encontrado na pasta '{pasta_html}'.")
        exit()

    todos_livros = []
    for arquivo in arquivos_html:
        caminho_arquivo = os.path.join(pasta_html, arquivo)
        print(f"\nParseando o arquivo: {caminho_arquivo}")
        livros = parse_livros_html(caminho_arquivo)
        todos_livros.extend(livros)

    # Exibir os livros extraídos
    print("\nLivros extraídos:")
    for livro in todos_livros:
        print(f"- Título: {livro['titulo']}")
        print(f"  Autor: {livro['autor']}")
        print(f"  Preço: R$ {livro['preco']}")
        print(f"  Imagem: {livro['imagem']}")
        print(f"  Desconto: {livro['desconto']}")
        print(f"  Descrição: {livro['descricao']}\n")

    # Cadastrar os livros
    print("Iniciando cadastro de livros...")
    cadastrar_livros(todos_livros)
    print("Cadastro concluído!")