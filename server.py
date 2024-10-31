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
CORS(app, resources={r"/*": {"origins": "https://preview.construct.net"}})

class GameState:
    def __init__(self):
        self.processo = None

    def iniciar_processo(self, nome: str, host: str, tabuleiro: str):
        self.processo = Process(nome=nome, host=host, tabuleiro=tabuleiro)
        logging.info(f"Processo iniciado com nome: {nome}, host: {host}, tabuleiro: {tabuleiro}")

    def get_processo(self):
        return self.processo


game_state = GameState()
dicionario_perguntas = [
    {
        "jogador": "exemple_player",
        "perguntas_nao_respondidas": [],
        "pergunta/resposta/tempo": [
            {
                "pergunta": "exemple_question",
                "resposta": "exemple_answer",
                "tempo": "exemple_time"
            }
        ]
    }
]
perguntas, respostas, jogadores, tempos_respostas = [], [], [], []
horarios_perguntas = {}  # Dicionário para armazenar os horários das perguntas

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "hello world"}), 200

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

    data = request.get_json().get('data')
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
        itens_filtrados = [item for item in itens if item['tipo'] == str(tipo)]
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

def log_debug(mensagem):
    """
    Função de log para mensagens de debug.
    """
    print(mensagem)

def validar_tipo_conteudo(request):
    """
    Verifica se o tipo de conteúdo da solicitação é JSON.
    """
    if not request.is_json:
        log_debug("Erro: Tipo de conteúdo inválido, esperado JSON.")
        return False
    return True

def resposta_erro(mensagem, status_code):
    """
    Retorna uma resposta de erro em formato JSON.
    """
    log_debug(f"Erro: {mensagem}")
    return jsonify({"status": "error", "message": mensagem}), status_code

def resposta_sucesso(mensagem):
    """
    Retorna uma resposta de sucesso em formato JSON.
    """
    log_debug(mensagem)
    return jsonify({"status": "success", "message": mensagem}), 200

def extrair_dados(request):
    """
    Extrai e retorna os dados do corpo da solicitação.
    """
    data = request.get_json().get('data')
    log_debug(f"Dados recebidos: {data}")
    return data


def validar_parametros_iniciar_jogo(data):
    """
    Verifica se os parâmetros necessários estão presentes nos dados.
    """
    nome = data.get('nome')
    host = data.get('host')
    tabuleiro = data.get('tabuleiro')
    log_debug(f"Parâmetros extraídos - Nome: {nome}, Host: {host}, Tabuleiro: {tabuleiro}")

    if not nome or not host or not tabuleiro:
        log_debug("Erro: Faltando 'nome', 'host' ou 'tabuleiro' nos dados fornecidos.")
        return False
    return True

def iniciar_processo_jogo(data):
    """
    Inicia o processo do jogo com os dados fornecidos.
    """
    nome = data.get('nome')
    host = data.get('host')
    tabuleiro = data.get('tabuleiro')
    log_debug("Tentando iniciar o processo do jogo...")
    logging.info(f"Iniciando jogo com nome: {nome}, host: {host}, tabuleiro: {tabuleiro}")
    game_state.iniciar_processo(nome=nome, host=host, tabuleiro=tabuleiro)
    log_debug("Jogo iniciado com sucesso.")

@app.route('/iniciar_jogo', methods=['POST'])
def iniciar_jogo():
    """
    Inicia o jogo.
    """
    log_debug("Recebendo solicitação para iniciar o jogo.")

    # Validação do tipo de conteúdo
    if not validar_tipo_conteudo(request):
        return resposta_erro("Invalid content type", 415)

    # Extração dos dados
    data = extrair_dados(request)
    if not data:
        return resposta_erro("Missing data", 400)

    # Validação dos parâmetros principais
    if not validar_parametros_iniciar_jogo(data):
        return resposta_erro("Missing 'nome' or 'host'", 400)

    # Tentativa de iniciar o jogo
    try:
        iniciar_processo_jogo(data)
        return resposta_sucesso("Game started")
    except ValueError as e:
        return resposta_erro(str(e), 400)

@app.route('/save_move', methods=['POST'])
def save_move():
    """
    Salva o movimento do jogo.
    """
    # Validações iniciais
    if not validar_instancia_processo(game_state.get_processo()):
        return resposta_erro("Invalid process instance", 400)

    if not validar_tipo_conteudo(request):
        return resposta_erro("Invalid content type", 415)

    # Extração dos dados
    data = extrair_dados(request)
    if not data:
        return resposta_erro("Missing data", 400)

    # Processamento do movimento
    try:
        verificar_jogador(data)
        processar_movimento(data)
        logging.info(f"Movimento salvo: {data}")
        return resposta_sucesso("Move received")
    except ValueError as e:
        logging.error(f"Erro ao salvar movimento: {e}")
        return resposta_erro(str(e), 400)


def verificar_jogador(data):
    """
    Verifica se a lista de jogadores contém o jogador especificados. Caso não esteja, adiciona.
    """
    jogador_nome = data.get('jogador')
    if not jogador_nome:
        raise ValueError("Data deve conter o campo 'jogador'.")

    for jogador in dicionario_perguntas:
        if jogador['jogador'] == jogador_nome:
            log_debug(f"Jogador '{jogador_nome}' encontrado na lista de jogadores.")
            return

    log_debug(f"Jogador '{jogador_nome}' não encontrado na lista de jogadores, adicionando...")
    novo_jogador = {
        "jogador": jogador_nome,
        "perguntas_nao_respondidas": [],
        "pergunta/resposta/tempo": []
    }
    log_debug(f"Lista de jogadores atualizada: {dicionario_perguntas}")

    dicionario_perguntas.append(novo_jogador)


def validar_instancia_processo(processo):
    """
    Verifica se a instância do processo é válida.
    """
    if not isinstance(processo, Process):
        log_debug("Erro: Instância do processo inválida.")
        return False
    return True


def processar_movimento(data):
    """
    Processa o movimento recebido com base na fase atual.
    """
    if data.get('fase') == 3:
        casos_id_perguntas = set()
        casos_id_perguntas = game_state.get_processo().process_data(move=data)
    else:
        game_state.get_processo().process_data(move=data)


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
