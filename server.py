import logging
import random

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path

from process import Process

# Configurando o logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),  # Log em arquivo
                        logging.StreamHandler()  # Log no console
                    ])

app = Flask(__name__)
CORS(app)


class GameState:
    def __init__(self):
        self.processo = None

    def iniciar_processo(self, nome: str, host: str, tabuleiro: str):
        self.processo = Process(nome=nome, host=host, tabuleiro=tabuleiro)
        logging.info(f"Processo iniciado com nome: {nome}, host: {host}, tabuleiro: {tabuleiro}")

    def get_processo(self):
        return self.processo


game_state = GameState()

# Exemplo de lista com itens e seus tipos
itens = [
    {"tipo": "1", "valor": "maçã"},
    {"tipo": "1", "valor": "banana"},
    {"tipo": "1", "valor": "água"},
    {"tipo": "2", "valor": "suco"},
    {"tipo": "2", "valor": "laranja"},
    {"tipo": "2", "valor": "café"}
]

@app.route('/pegar_item_aleatorio', methods=['POST'])
def pegar_item_aleatorio():
    """
    Retorna um item aleatório de uma lista. Se 'tipo' for passado no request,
    retorna um item aleatório apenas desse tipo.
    """
    if not request.is_json:
        return jsonify({"status": "error", "message": "Invalid content type"}), 415

    data = request.get_json()
    tipo = data.get('tipo')

    # Se um tipo foi especificado, filtra a lista para aquele tipo
    if tipo:
        itens_filtrados = [item for item in itens if item['tipo'] == tipo]
        if not itens_filtrados:
            return jsonify({"status": "error", "message": "Nenhum item encontrado para esse tipo"}), 404
        item_escolhido = random.choice(itens_filtrados)
    else:
        # Se não foi especificado um tipo, seleciona de toda a lista
        item_escolhido = random.choice(itens)

    print(f"Item escolhido: {item_escolhido}")
    return jsonify({"status": "success", "item": item_escolhido}), 200

@app.route('/iniciar_jogo', methods=['POST'])
def iniciar_jogo():
    """
    Inicia o jogo.
    """
    if not request.is_json:
        return jsonify({"status": "error", "message": "Invalid content type"}), 415

    data = request.get_json().get('data')
    if not data:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    nome = data.get('nome')
    host = data.get('host')
    tabuleiro = data.get('tabuleiro')

    if not nome or not host or not tabuleiro:
        return jsonify({"status": "error", "message": "Missing 'nome' or 'host'"}), 400

    try:
        logging.info(f"Iniciando jogo com nome: {nome}, host: {host}, tabuleiro: {tabuleiro}")
        game_state.iniciar_processo(nome=nome, host=host, tabuleiro=tabuleiro)
        return jsonify({"status": "success", "message": "Game started"}), 200
    except ValueError as e:
        logging.error(f"Erro ao iniciar o jogo: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/save_move', methods=['POST'])
def save_move():
    if not isinstance(game_state.get_processo(), Process):
        return jsonify({"status": "error", "message": "Invalid process instance"}), 400

    if not request.is_json:
        return jsonify({"status": "error", "message": "Invalid content type"}), 415

    data = request.get_json().get('data')
    if not data:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    try:
        game_state.get_processo().process_data(move=data)
        logging.info(f"Movimento salvo: {data}")
        return jsonify({"status": "success", "message": "Move received"}), 200
    except ValueError as e:
        logging.error(f"Erro ao salvar movimento: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/finalizar_jogo', methods=['POST'])
def finalizar_jogo_route():
    if not isinstance(game_state.get_processo(), Process):
        return jsonify({"status": "error", "message": "Invalid process instance"}), 400

    if not request.is_json:
        return jsonify({"status": "error", "message": "Invalid content type"}), 415

    data = request.get_json().get('data')
    if not data:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    try:
        finalizacao = game_state.get_processo().finalizar_jogo(move=data)
        logging.info(f"Jogo finalizado: {finalizacao.descricao} por {finalizacao.jogador.nome}")
        return jsonify({"status": "success",
                        "message": f"Game {finalizacao.descricao} by {finalizacao.jogador.nome}"}), 200
    except ValueError as e:
        logging.error(f"Erro ao finalizar o jogo: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/export_csv', methods=['GET'])
def export_csv():
    if not isinstance(game_state.get_processo(), Process):
        return jsonify({"status": "error", "message": "Invalid process instance"}), 400

    game_state.get_processo().encerrar_jogo()

    if not game_state.get_processo().game.jogadas:
        return jsonify({"status": "error", "message": "No data to export"}), 400

    csv_file = 'data.csv'
    if not game_state.get_processo().csv_instance or not Path(csv_file).is_file():
        return jsonify({"status": "error", "message": "Failed to create CSV file"}), 500

    logging.info(f"Exportando CSV: {csv_file}")
    return send_file(csv_file, as_attachment=True)

@app.route('/mudar_tabuleiro', methods=['GET'])
def mudar_tabuleiro():
    if not isinstance(game_state.get_processo(), Process):
        return jsonify({"status": "error", "message": "Invalid process instance"}), 400

    game_state.get_processo().mudar_tabuleiro()
    logging.info("Tabuleiro mudado")
    return jsonify({"status": "success", "message": "Tabuleiro mudado"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
