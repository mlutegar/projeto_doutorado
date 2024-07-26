from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path

from process import Process

app = Flask(__name__)
CORS(app)


class GameState:
    def __init__(self):
        self.processo = None

    def iniciar_processo(self, nome, host):
        self.processo = Process(nome=nome, host=host)

    def get_processo(self):
        return self.processo


game_state = GameState()


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
    if not nome or not host:
        return jsonify({"status": "error", "message": "Missing 'nome' or 'host'"}), 400

    try:
        print(f"Iniciando jogo com nome: {nome}, host: {host}")
        game_state.iniciar_processo(nome=nome, host=host)
        return jsonify({"status": "success", "message": "Game started"}), 200
    except ValueError as e:
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
        return jsonify({"status": "success", "message": "Move received"}), 200
    except ValueError as e:
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
        return jsonify({"status": "success",
                        "message": f"Game {finalizacao.descricao} by {finalizacao.jogador.nome}"}), 200
    except ValueError as e:
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

    return send_file(csv_file, as_attachment=True)


@app.route('/mudar_tabuleiro', methods=['GET'])
def mudar_tabuleiro():
    if not isinstance(game_state.get_processo(), Process):
        return jsonify({"status": "error", "message": "Invalid process instance"}), 400

    game_state.get_processo().mudar_tabuleiro()
    return jsonify({"status": "success", "message": "Tabuleiro mudado"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
