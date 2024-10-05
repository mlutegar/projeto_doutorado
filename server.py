import logging
import random
from datetime import datetime

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
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
    {"tipo": "1", "valor": "Você escolheu formar um agrupamento com peças diferentes?"},
    {"tipo": "1", "valor": "Você escolheu formar um agrupamento com peças iguais?"},
    {"tipo": "2", "valor": "Você interagiu com os outros jogadores?"},
    {"tipo": "2", "valor": "Havia algo que impediu você de interagir com os outros jogadores?"},
    {"tipo": "2", "valor": "Algo específico fez você decidir interagir com os outros jogadores?"},
    {"tipo": "1", "valor": "Você corrige suas ações quando percebe que está prestes a cometer um erro ao posicionar as peças?"},
    {"tipo": "1", "valor": "Você analisa as razões quando uma jogada não sai como o esperado?"},
    {"tipo": "1", "valor": "Você acredita que suas escolhas no jogo são mais eficazes do que as dos outros jogadores?"},
    {"tipo": "1", "valor": "A forma como os outros jogadores organizam suas peças influencia suas decisões?"},
    {"tipo": "2", "valor": "Você adapta sua estratégia com base no que observa nos outros jogadores?"},
    {"tipo": "2", "valor": "Você percebe diferenças entre a sua forma de jogar e a dos outros jogadores?"},
    {"tipo": "1", "valor": "Você acha que a estratégia de outro jogador já foi melhor ou pior do que a sua?"},
    {"tipo": "2", "valor": "O sucesso ou falha de outros jogadores influencia a forma como você posiciona suas peças?"},
    {"tipo": "1", "valor": "Você acredita que existe uma maneira específica de agir nesse jogo/instrumento?"},
    {"tipo": "2", "valor": "Você acredita que todos os jogadores seguem padrões similares de pensamento?"},
    {"tipo": "1", "valor": "Você está seguindo regras específicas no jogo?"},
    {"tipo": "1", "valor": "Você acredita que existe uma maneira correta de todos jogarem?"},
    {"tipo": "1", "valor": "Você acredita que a forma como organiza suas peças reflete as regras universais do jogo/instrumento?"},
    {"tipo": "2", "valor": "Você acredita que todos os jogadores interpretam a dinâmica do jogo da mesma maneira?"},
    {"tipo": "2", "valor": "Você ajusta suas jogadas com base na suposição de que outros jogadores podem pensar de forma semelhante a você?"},
    {"tipo": "1", "valor": "Você considera algum aspecto do jogo particularmente desafiador?"},
    {"tipo": "1", "valor": "Você acha que algumas ações no jogo requerem mais planejamento do que outras?"},
    {"tipo": "2", "valor": "Você decidiu desistir do jogo?"},
    {"tipo": "2", "valor": "Você decidiu finalizar o jogo?"},
    {"tipo": "1", "valor": "Você retirou uma peça do lugar que o outro jogador havia colocado?"},
    {"tipo": "1", "valor": "Você retirou uma peça que você mesmo havia colocado?"},
    {"tipo": "1", "valor": "Você utiliza estratégias específicas para posicionar as peças e alcançar seus objetivos?"},
    {"tipo": "1", "valor": "Você decide previamente qual estratégia vai usar para formar um agrupamento?"},
    {"tipo": "1", "valor": "Você planeja suas jogadas antes de executá-las?"},
    {"tipo": "1", "valor": "Você definiu indicadores de desempenho específicos para acompanhar seu progresso no jogo?"},
    {"tipo": "2", "valor": "Há indicadores específicos que fazem você mudar sua estratégia?"},
    {"tipo": "1", "valor": "Você relaciona as ações dos outros jogadores com as suas para melhorar sua estratégia?"},
    {"tipo": "1", "valor": "Você verifica se está utilizando a melhor estratégia durante o jogo?"},
    {"tipo": "1", "valor": "Você definiu indicadores de desempenho específicos para acompanhar seu progresso no jogo?"},
    {"tipo": "2", "valor": "Quando você sente que uma tarefa é fácil ou difícil, isso afeta suas próximas jogadas?"},
    {"tipo": "2", "valor": "Você altera sua estratégia ao sentir frustração ou satisfação durante o jogo?"},
    {"tipo": "1", "valor": "Quando uma jogada não tem o efeito esperado, você muda sua abordagem no jogo?"},
    {"tipo": "1", "valor": "Você definiu um objetivo principal ao jogar este jogo?"},
    {"tipo": "1", "valor": "Seu objetivo principal guia suas decisões durante a partida?"},
    {"tipo": "1", "valor": "Você alterou seus objetivos ao longo do jogo com base na evolução da partida?"},
    {"tipo": "1", "valor": "Você prioriza algum objetivo específico ao interagir com outros jogadores?"},
    {"tipo": "1", "valor": "Você tem critérios claros para determinar se atingiu seu objetivo no jogo?"},
    {"tipo": "1", "valor": "Você planeja suas jogadas antes de começar a posicionar as peças?"},
    {"tipo": "1", "valor": "Você avalia se uma jogada foi bem-sucedida após concluí-la?"},
    {"tipo": "1", "valor": "Você tem critérios específicos para determinar se atingiu seu objetivo no jogo?"}
]

perguntas = []
respostas = []
jogadores = []
tempos_respostas = []
horarios_perguntas = {}  # Dicionário para armazenar os horários das perguntas


@app.route('/responder_pergunta', methods=['POST'])
def responder_pergunta():
    """
    Responde a uma pergunta.
    """
    if not request.is_json:
        return jsonify({"status": "error", "message": "Invalid content type"}), 415

    data = request.get_json().get('data')

    pergunta = data.get('pergunta')
    resposta = data.get('resposta')
    jogador = data.get('jogador')

    if not pergunta or not resposta or not jogador:
        return jsonify({"status": "error", "message": "Missing 'pergunta', 'resposta' ou 'jogador'"}), 400

    # Calculando o tempo de resposta
    if jogador not in horarios_perguntas:
        return jsonify({"status": "error", "message": "Horário da pergunta não encontrado para o jogador"}), 400

    horario_pergunta = horarios_perguntas.pop(jogador)  # Remove e obtém o horário da pergunta
    horario_resposta = datetime.now()
    tempo_resposta = (horario_resposta - horario_pergunta).total_seconds()

    # Armazenando os dados da resposta
    perguntas.append(pergunta)
    respostas.append(resposta)
    jogadores.append(jogador)
    tempos_respostas.append(tempo_resposta)

    return jsonify({"status": "success", "message": "Pergunta e resposta registradas com sucesso."}), 200


@app.route('/pegar_item_aleatorio', methods=['POST'])
def pegar_item_aleatorio():
    """
    Retorna um item aleatório de uma lista. Se 'tipo' for passado no request,
    retorna um item aleatório apenas desse tipo.
    """
    # Verificando se o conteúdo do request é JSON
    if not request.is_json:
        print("Erro: O conteúdo do request não é JSON.")
        return jsonify({"status": "error", "message": "Invalid content type"}), 415

    data = request.get_json()
    print(f"Dados recebidos: {data}")

    tipo = data.get('tipo')
    jogador = data.get('jogador')

    # Verificando se o jogador foi especificado
    if not jogador:
        print("Erro: 'jogador' não foi especificado.")
        return jsonify({"status": "error", "message": "Missing 'jogador'"}), 400

    # Se um tipo foi especificado, filtra a lista para aquele tipo
    if tipo:
        print(f"Tipo especificado: {tipo}")
        itens_filtrados = [item for item in itens if item['tipo'] == tipo]
        print(f"Itens filtrados: {itens_filtrados}")
        if not itens_filtrados:
            print("Erro: Nenhum item encontrado para o tipo especificado.")
            return jsonify({"status": "error", "message": "Nenhum item encontrado para esse tipo"}), 404
        item_escolhido = random.choice(itens_filtrados)
    else:
        # Se não foi especificado um tipo, seleciona de toda a lista
        print("Nenhum tipo especificado, selecionando de toda a lista.")
        item_escolhido = random.choice(itens)

    # Armazenando o horário da pergunta para o jogador
    horarios_perguntas[jogador] = datetime.now()
    print(f"Horário da pergunta para o jogador '{jogador}': {horarios_perguntas[jogador]}")

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

    game_state.get_processo().encerrar_jogo(perguntas, respostas, jogadores, tempos_respostas)

    excel_file = game_state.get_processo().csv_instance.path_excel_complete
    if not excel_file.is_file():
        return jsonify({"status": "error", "message": "Failed to create Excel file"}), 500

    logging.info(f"Exportando Excel: {excel_file}")
    return send_file(excel_file, as_attachment=True)


@app.route('/mudar_tabuleiro', methods=['GET'])
def mudar_tabuleiro():
    if not isinstance(game_state.get_processo(), Process):
        return jsonify({"status": "error", "message": "Invalid process instance"}), 400

    game_state.get_processo().mudar_tabuleiro()
    logging.info("Tabuleiro mudado")
    return jsonify({"status": "success", "message": "Tabuleiro mudado"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
