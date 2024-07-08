from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import process
from pathlib import Path


app = Flask(__name__)
CORS(app)


@app.route('/iniciar_jogo', method=['POST'])
def iniciar_jogo():
    """
    Inicia o jogo.
    """
    if request.is_json:
        data = request.get_json()
        nome = data['nome']
        host = data['host']

        try:
            process.iniciar_jogo(nome, host)
            return jsonify({"status": "success", "message": "Game started"}), 200
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid content type"}), 415


@app.route('/save_move', methods=['POST'])
def save_move():
    if request.is_json:
        data = request.get_json()
        data = data['data']

        try:
            process.process_data(data)
            return jsonify({"status": "success", "message": "Move received"}), 200
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid content type"}), 415


@app.route('/export_csv', methods=['GET'])
def export_csv():
    process.encerrar_jogo()

    if not process.game.jogadas:
        return jsonify({"status": "error", "message": "No data to export"}), 400

    # Define o nome do arquivo CSV
    csv_file = 'data.csv'

    # Verifica se o arquivo CSV foi criado e escreve os dados
    if not process.csv_instance or not Path(csv_file).is_file():
        return jsonify({"status": "error", "message": "Failed to create CSV file"}), 500

    # Envia o arquivo CSV para download
    return send_file(csv_file, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
