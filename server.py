from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from process import *
from pathlib import Path

from entities.game import Game

game: Game | None = None
app = Flask(__name__)
CORS(app)


@app.route('/iniciar_jogo', methods=['POST'])
def iniciar_jogo():
    """
    Inicia o jogo.
    """
    global game

    if request.is_json:
        data = request.get_json()
        data = data['data']
        nome = data.get('nome')
        host = data.get('host')

        if not nome or not host:
            return jsonify({"status": "error", "message": "Missing 'nome' or 'host'"}), 400

        try:
            # Simulação de processamento
            print(f"Iniciando jogo com nome: {nome}, host: {host}")
            iniciar_jogo(nome=nome, host=host, game=game)
            return jsonify({"status": "success", "message": "Game started"}), 200
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid content type"}), 415


@app.route('/save_move', methods=['POST'])
def save_move():
    global game

    if request.is_json:
        data = request.get_json()
        data = data['data']

        try:
            process_data(game=game, move=data)
            return jsonify({"status": "success", "message": "Move received"}), 200
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid content type"}), 415

@app.route('/finalizar_jogo', methods=['POST'])
def finalizar_jogo_route():
    global game

    if request.is_json:
        data = request.get_json()
        data = data['data']

        try:
            finalizacao = finalizar_jogo(game=game, move=data)
            return jsonify({"status": "success", "message": f"Game {finalizacao.descricao} by {finalizacao.jogador.nome}"}), 200
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid content type"}), 415


@app.route('/export_csv', methods=['GET'])
def export_csv():
    global game

    encerrar_jogo(game=game)

    if not game.jogadas:
        return jsonify({"status": "error", "message": "No data to export"}), 400

    # Define o nome do arquivo CSV
    csv_file = 'data.csv'

    # Verifica se o arquivo CSV foi criado e escreve os dados
    if not csv_instance or not Path(csv_file).is_file():
        return jsonify({"status": "error", "message": "Failed to create CSV file"}), 500

    # Envia o arquivo CSV para download
    return send_file(csv_file, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
