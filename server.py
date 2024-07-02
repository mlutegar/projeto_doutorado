from flask import Flask, request, jsonify, send_file
import csv
from flask_cors import CORS
import util
from util import process_data

app = Flask(__name__)
CORS(app)


@app.route('/save_move', methods=['POST'])
def save_move():
    if request.is_json:
        data = request.get_json()
        data = data['data']

        try:
            process_data(data)
            return jsonify({"status": "success", "message": "Move received"}), 200
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid content type"}), 415


@app.route('/export_csv', methods=['GET'])
def export_csv():
    if not util.jogadas:
        return jsonify({"status": "error", "message": "No data to export"}), 400

    # Define o nome do arquivo CSV
    csv_file = 'moves_data.csv'

    # Cria e escreve os dados no arquivo CSV
    with open(csv_file, 'w', newline='') as file:
        fieldnames = ["id", "peca_uid", "jogador", "tempo", "peca_cor", "peca_posicao_antiga", "peca_posicao_atual",
                      "peca_grupo", "peca_last_player", "peca_vizinho", "situacao_id", "situacao_descricao"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for jogada, situacao in util.jogadas:
            jogada_dict = jogada.to_dict()
            situacao_dict = situacao.to_dict()
            combined_dict = {**jogada_dict, **situacao_dict}
            writer.writerow(combined_dict)

    # Envia o arquivo CSV para download
    return send_file(csv_file, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
