from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import sqlite3
import os
from jinja2 import Environment, FileSystemLoader, ChoiceLoader

app = Flask(__name__)
CORS(app)

# Configurar o carregador de templates para múltiplas pastas
template_loader = ChoiceLoader([
    FileSystemLoader('templates'),  # Pasta padrão para templates
    FileSystemLoader('public')      # Pasta adicional para index.html
])
app.jinja_env = Environment(loader=template_loader)

def get_db_connection():
    conn = sqlite3.connect('livros.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT,
        preco REAL,
        imagem TEXT,
        desconto TEXT,
        autor TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    sort_by = request.args.get('sort', 'id')
    sort_query = {
        'mais-vendidos': 'id DESC',
        'preco-menor': 'preco ASC',
        'preco-maior': 'preco DESC'
    }.get(sort_by, 'id')
    
    conn = get_db_connection()
    livros = conn.execute(f'SELECT * FROM livros ORDER BY {sort_query}').fetchall()
    conn.close()
    
    # Formatar os preços e preços com desconto
    livros_formatados = []
    for livro in livros:
        livro_dict = dict(livro)
        livro_dict['preco'] = f"{livro['preco']:.2f}"
        if livro['desconto']:
            livro_dict['preco_com_desconto'] = f"{livro['preco'] * 0.9:.2f}"
        else:
            livro_dict['preco_com_desconto'] = None
        livros_formatados.append(livro_dict)
    
    return render_template('index.html', livros=livros_formatados, sort_by=sort_by)

@app.route('/livro/<int:id>')
def detalhes_livro(id):
    conn = get_db_connection()
    livro = conn.execute('SELECT * FROM livros WHERE id = ?', (id,)).fetchone()
    conn.close()
    if livro is None:
        return render_template('livro_nao_encontrado.html'), 404
    
    livro_dict = dict(livro)
    livro_dict['preco'] = f"{livro['preco']:.2f}"
    if livro['desconto']:
        livro_dict['preco_com_desconto'] = f"{livro['preco'] * 0.9:.2f}"
    else:
        livro_dict['preco_com_desconto'] = None
    
    return render_template('detalhes_livro.html', livro=livro_dict)

@app.route('/admin.html')
def serve_admin():
    return render_template('admin.html')

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    print(f"Tentando servir: assets/{filename}")
    return send_from_directory('assets', filename)

@app.route('/cadastrar-livro', methods=['POST'])
def cadastrar_livro():
    data = request.get_json()
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    preco = data.get('preco')
    imagem = data.get('imagem')
    desconto = data.get('desconto')
    autor = data.get('autor')

    conn = get_db_connection()
    conn.execute('INSERT INTO livros (titulo, descricao, preco, imagem, desconto, autor) VALUES (?, ?, ?, ?, ?, ?)',
                 (titulo, descricao, preco, imagem, desconto, autor))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Livro cadastrado com sucesso!'}), 201

@app.route('/livros', methods=['GET'])
def listar_livros():
    sort_by = request.args.get('sort', 'id')
    sort_query = {
        'mais-vendidos': 'id DESC',
        'preco-menor': 'preco ASC',
        'preco-maior': 'preco DESC'
    }.get(sort_by, 'id')
    
    conn = get_db_connection()
    livros = conn.execute(f'SELECT * FROM livros ORDER BY {sort_query}').fetchall()
    conn.close()
    
    livros_formatados = []
    for livro in livros:
        livro_dict = dict(livro)
        livro_dict['preco'] = f"{livro['preco']:.2f}"
        if livro['desconto']:
            livro_dict['preco_com_desconto'] = f"{livro['preco'] * 0.9:.2f}"
        else:
            livro_dict['preco_com_desconto'] = None
        livros_formatados.append(livro_dict)
    
    return jsonify(livros_formatados)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)