from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_cors import CORS
from flask import Flask
import json
import os

# Configurações do arquivo de dados e servidor
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.json')

app = Flask(__name__, static_folder='../static', template_folder='../templates')
CORS(app)

def read_data():
    """Lê os dados do arquivo JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def write_data(data):
    """Escreve os dados no arquivo JSON."""
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Erro ao escrever no arquivo: {e}")

@app.route('/')
def home():
    """Renderiza a página inicial."""
    return render_template('index.html')

@app.route('/style.css')
def serve_css():
    """Serve o arquivo CSS."""
    return send_from_directory('../static', 'style.css')

@app.route('/script.js')
def serve_js():
    """Serve o arquivo JavaScript."""
    return send_from_directory('../static', 'script.js')

@app.route('/api/items', methods=['GET'])
def get_items():
    """Retorna todos os itens válidos."""
    data = read_data()
    valid_data = [item for item in data if item.get('codigo') and item['codigo'] != "undefined"]
    return jsonify(valid_data), 200

@app.route('/api/items', methods=['POST'])
def add_item():
    """Adiciona um novo item."""
    data = read_data()
    new_item = request.json

    if not new_item.get('codigo') or new_item.get('codigo') == "undefined":
        return jsonify({"error": "Código é obrigatório"}), 400

    data.append(new_item)
    write_data(data)
    return jsonify(new_item), 201

@app.route('/api/items/<codigo>', methods=['PUT'])
def update_item(codigo):
    """Atualiza um item existente."""
    data = read_data()
    updated_item = request.json

    for i, item in enumerate(data):
        if item.get('codigo') == codigo:
            data[i].update(updated_item)  # Atualiza campos específicos
            write_data(data)
            return jsonify({"message": "Item atualizado"}), 200

    return jsonify({"error": "Item não encontrado"}), 404

@app.route('/api/items/<codigo>', methods=['DELETE'])
def delete_item(codigo):
    """Remove um item pelo código."""
    data = read_data()

    new_data = [item for item in data if item.get('codigo') != codigo]

    if len(data) == len(new_data):
        return jsonify({"error": "Item não encontrado"}), 404

    write_data(new_data)
    return jsonify({"message": "Item removido"}), 200

@app.route('/dashboard')
def dashboard():
    """Renderiza o dashboard com os dados do estoque."""
    data = read_data()

    # Separa os nomes e quantidades dos produtos
    produtos = [item['nome'] for item in data if 'nome' in item and 'quantidade' in item]
    quantidades = [item['quantidade'] for item in data if 'nome' in item and 'quantidade' in item]

    return render_template('dashboard.html', produtos=produtos, quantidades=quantidades)


if __name__ == '__main__':
    app.run(debug=True)