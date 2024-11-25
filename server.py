import logging
import os
import pandas as pd

from datetime import datetime
from flask import Flask, send_file, jsonify, request, render_template, send_from_directory, redirect, url_for
from flask_cors import CORS

from app.routes.home import home_bp
from process import Process
from src.entities.grafo_dash import layouts, gerar_grafo, fases_disponiveis
from src.util.situacoes import perguntas_unica, perguntas, situacoes
from dash import Dash, dcc, html, Input, Output

from src.util.nome_file import process_files

# Configurando o logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),  # Log em arquivo
                        logging.StreamHandler()  # Log no console
                    ])

app = Flask(__name__)
CORS(app, resources={
    r"/*": {"origins": ["https://preview.construct.net", "https://white-coast-08b1df80f.5.azurestaticapps.net"]}
})
numero_jogada = 0

app.register_blueprint(home_bp)

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
        "perguntas_nao_respondidas": list(perguntas_unica.values()),
        "pergunta/resposta/tempo": [
            {
                "pergunta": "exemple_question",
                "resposta": "exemple_answer",
                "horario": "exemple_time"
            }
        ],
        "perguntas_pendentes": []
    }
]

ZIP_DIR = 'data'

# Inicializa a aplicação Dash com o Flask
dash_app = Dash(
    server=app,
    url_base_pathname='/dash/'
)

df_clusterizado = pd.read_excel("sd.xlsx", sheet_name='Dados Clusterizados')
jogadores = df_clusterizado["Nome do player"].unique()

# Layout inicial do Dash
dash_app.layout = html.Div(
        [
            html.H1("Visualizador de Grafos"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Selecione o Jogador:"),
                            dcc.Dropdown(
                                id="jogador-dropdown",
                                options=[{"label": jogador, "value": jogador} for jogador in jogadores],
                                value=jogadores[0],
                            ),
                        ], style={'width': '100%'}
                    ),
                    html.Div(
                        [
                            html.Label("Selecione o Layout:"),
                            dcc.Dropdown(
                                id="layout-dropdown",
                                options=[{"label": layout, "value": layout} for layout in layouts.keys()],
                                value="Spectral",
                            ),
                        ], style={'width': '100%'}
                    ),
                    html.Div(
                        [
                            html.Label("Selecione as Fases da Jogada:"),
                            dcc.Dropdown(
                                id="fases-dropdown",
                                options=[{"label": fase, "value": fase} for fase in fases_disponiveis],
                                value=[],
                                multi=True,  # Permite seleção múltipla
                            ),
                        ], style={'width': '100%'}
                    ),
                ], style={'display': 'flex', 'gap': '10px'}
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Jogada inicial:"),
                            dcc.Input(
                                id="jogada-inicial",
                                type="number",
                                placeholder="Ex: 10",
                                value=1,
                            ),
                        ],
                    ),
                    html.Div(
                        [
                            html.Label("Jogada final:"),
                            dcc.Input(
                                id="jogada-final",
                                type="number",
                                placeholder="Ex: 20",
                                value=10,
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Ver Estados:"),
                            dcc.Checklist(
                                id="ver-estados-checkbox",
                                options=[{"label": "Habilitar", "value": "ver_estados"}],
                                value=[],
                                inline=True,
                            ),
                        ]
                    ),
                ],
                className="flex-container",
            ),
            dcc.Graph(id="grafo-output", className="graph-container"),
        ]
    )

# Carrega o arquivo Excel baseado no parâmetro da URL
@app.route('/dashboard')
def dashboard():
    file_name = request.args.get('file')
    if not file_name:
        return redirect(url_for('home'))

    file_path = os.path.join("data", file_name)
    if not os.path.exists(file_path):
        return f"Arquivo {file_name} não encontrado.", 404

    # Carrega o arquivo e atualiza os valores do dropdown
    global df_clusterizado
    global jogadores

    df_clusterizado = pd.read_excel(file_path, sheet_name='Dados Clusterizados')
    jogadores = df_clusterizado["Nome do player"].unique()

    # Layout inicial do Dash
    # Layout inicial do Dash
    dash_app.layout = html.Div(
        [
            html.H1("Visualizador de Grafos"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Selecione o Jogador:"),
                            dcc.Dropdown(
                                id="jogador-dropdown",
                                options=[{"label": jogador, "value": jogador} for jogador in jogadores],
                                value=jogadores[0],
                            ),
                        ], style={'width': '100%'}
                    ),
                    html.Div(
                        [
                            html.Label("Selecione o Layout:"),
                            dcc.Dropdown(
                                id="layout-dropdown",
                                options=[{"label": layout, "value": layout} for layout in layouts.keys()],
                                value="Spectral",
                            ),
                        ], style={'width': '100%'}
                    ),
                    html.Div(
                        [
                            html.Label("Selecione as Fases da Jogada:"),
                            dcc.Dropdown(
                                id="fases-dropdown",
                                options=[{"label": fase, "value": fase} for fase in fases_disponiveis],
                                value=[],
                                multi=True,  # Permite seleção múltipla
                            ),
                        ], style={'width': '100%'}
                    ),
                ], style={'display': 'flex', 'gap': '10px'}
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Jogada inicial:"),
                            dcc.Input(
                                id="jogada-inicial",
                                type="number",
                                placeholder="Ex: 10",
                                value=1,
                            ),
                        ],
                    ),
                    html.Div(
                        [
                            html.Label("Jogada final:"),
                            dcc.Input(
                                id="jogada-final",
                                type="number",
                                placeholder="Ex: 20",
                                value=10,
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label("Ver Estados:"),
                            dcc.Checklist(
                                id="ver-estados-checkbox",
                                options=[{"label": "Habilitar", "value": "ver_estados"}],
                                value=[],
                                inline=True,
                            ),
                        ]
                    ),
                ],
                className="flex-container",
            ),
            dcc.Graph(id="grafo-output", className="graph-container"),
        ]
    )

    return redirect('/dash/')


# Callback para atualizar o grafo
@dash_app.callback(
    Output("grafo-output", "figure"),
    [
        Input("jogador-dropdown", "value"),
        Input("layout-dropdown", "value"),
        Input("jogada-inicial", "value"),
        Input("jogada-final", "value"),
        Input("fases-dropdown", "value"),
        Input("ver-estados-checkbox", "value"),
    ]
)
def update_grafo(jogador, layout_name, jogada_inicial, jogada_final, fases_selecionadas, ver_estados):
    # Converte a lista de valores para booleano (se "ver_estados" está na lista)
    mostrar_estados = "ver_estados" in ver_estados
    return gerar_grafo(df_clusterizado, jogador, layout_name, jogada_inicial, jogada_final, mostrar_estados,
                       fases_selecionadas)


@app.route('/versao', methods=['GET'])
def versao():
    return jsonify({"versao": "back: v.1.0 18/11/2024"})


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(ZIP_DIR, filename, as_attachment=True)


@app.route('/responder_pergunta', methods=['POST'])
def responder_pergunta():
    """
    Responde a uma pergunta.
    """
    print("Iniciando o processamento de /responder_pergunta...")

    if not request.is_json:
        print("Erro: Tipo de conteúdo inválido.")
        return jsonify({"status": "error", "message": "Invalid content type"}), 415

    data = request.get_json()
    print("Dados recebidos:", data)

    pergunta = data.get('pergunta')
    resposta = data.get('resposta')
    jogador = data.get('jogador')
    print(f"Pergunta: {pergunta}, Resposta: {resposta}, Jogador: {jogador}")

    if not pergunta or not resposta or not jogador:
        print("Erro: Faltando 'pergunta', 'resposta' ou 'Jogador' nos dados.")
        return jsonify({"status": "error", "message": "Missing 'pergunta', 'resposta' ou 'Jogador'"}), 400

    # Localiza o dicionário do jogador
    jogador_data = next((item for item in dicionario_perguntas if item["jogador"] == jogador), None)
    if not jogador_data:
        print("Erro: Jogador não encontrado no dicionário.")
        return jsonify({"status": "error", "message": "Jogador não encontrado"}), 400
    else:
        print("Jogador encontrado:", jogador_data)

    # Calcula o horário atual para a resposta
    horario_resposta = datetime.now()
    print("Horário da resposta:", horario_resposta)

    # Armazena a pergunta, resposta e o horário da resposta
    jogador_data["pergunta/resposta/tempo"].append({
        "pergunta": pergunta,
        "resposta": resposta,
        "horario": horario_resposta.strftime("%Y-%m-%d %H:%M:%S")  # Converte datetime para string
    })
    print("Dados atualizados do jogador após registro de resposta:", jogador_data)

    # Remove a pergunta de perguntas_nao_respondidas, se presente
    if pergunta in jogador_data["perguntas_nao_respondidas"]:
        jogador_data["perguntas_nao_respondidas"].remove(pergunta)
        print(f"Pergunta '{pergunta}' removida de perguntas_nao_respondidas.")
    else:
        print(f"Pergunta '{pergunta}' não encontrada em perguntas_nao_respondidas.")

    # Remove a pergunta de perguntas_pendentes, se presente
    if pergunta in jogador_data["perguntas_pendentes"]:
        jogador_data["perguntas_pendentes"].remove(pergunta)
        print(f"Pergunta '{pergunta}' removida de perguntas_pendentes.")
    else:
        print(f"Pergunta '{pergunta}' não encontrada em perguntas_pendentes.")

    print("Resposta registrada com sucesso.")
    return jsonify({"status": "success", "message": "Pergunta e resposta registradas com sucesso."}), 200


def log_debug(mensagem):
    """
    Função de log para mensagens de debug.
    """
    print(mensagem)


def validar_tipo_conteudo(conteudo):
    """
    Verifica se o tipo de conteúdo da solicitação é JSON.
    """
    if not conteudo.is_json:
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


def extrair_dados(conteudo):
    """
    Extrai e retorna os dados do corpo da solicitação.
    """
    data = conteudo.get_json().get('data')
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

    # Zerar o dicionário de perguntas
    global dicionario_perguntas
    dicionario_perguntas = []

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
    global numero_jogada  # numero_jogada: variável global para contar o número de jogadas
    print(f"Numero da jogada: {numero_jogada}")

    # Validações iniciais
    if not validar_instancia_processo(game_state.get_processo()):
        print("Erro: Instância do processo inválida.")
        return resposta_erro("Invalid process instance", 400)
    print("Instância do processo válida.")

    if not validar_tipo_conteudo(request):
        print("Erro: Tipo de conteúdo inválido.")
        return resposta_erro("Invalid content type", 415)
    print("Tipo de conteúdo válido.")

    # Extração dos dados
    data = extrair_dados(request)
    print(f"Dados extraídos: {data}")
    if not data:
        print("Erro: Dados ausentes.")
        return resposta_erro("Missing data", 400)

    # Processamento do movimento
    try:
        verificar_jogador(data)
        resultado = processar_movimento(data)
        resultado = resultado[:5] if resultado else None
        print(f"Resultado: {resultado}")
        print(f"Fase: {data.get('Fase')}")

        # Verifica se o movimento é da fase 3, se houve resultado e se é uma jogada múltipla de 5
        if data.get('Fase') == 3 and resultado and numero_jogada % 5 == 0:
            numero_jogada += 1
            return jsonify({"perguntas": resultado}), 200

        logging.info(f"Movimento salvo: {data}")
        numero_jogada += 1
        print(f"Numero da jogada: {numero_jogada}")
        return resposta_sucesso("Move received")
    except ValueError as e:
        logging.error(f"Erro ao salvar movimento: {e}")
        return resposta_erro(str(e), 400)


def verificar_jogador(data):
    """
    Verifica se a lista de jogadores contém o jogador especificados. Caso não esteja, adiciona.
    """
    jogador_nome = data.get('Jogador')
    if not jogador_nome:
        raise ValueError("Data deve conter o campo 'jogador'.")

    for jogador in dicionario_perguntas:
        if jogador['jogador'] == jogador_nome:
            log_debug(f"Jogador '{jogador_nome}' encontrado na lista de jogadores.")
            return

    log_debug(f"Jogador '{jogador_nome}' não encontrado na lista de jogadores, adicionando...")
    novo_jogador = {
        "jogador": jogador_nome,
        "perguntas_nao_respondidas": list(perguntas_unica.values()),
        "pergunta/resposta/tempo": [],
        "perguntas_pendentes": []  # Adicione esta linha
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
    print("\n--------------------------------------------------")
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"processar_movimento: {data}")

    if data.get('Fase') == 3 and numero_jogada % 5 == 0:
        print(f"fase == {data.get('Fase')} e numero_jogada % 5 == {numero_jogada % 5}")

        casos_id_perguntas = game_state.get_processo().process_data(move=data)
        print(f"casos_id_perguntas após processamento: {casos_id_perguntas}")

        # Lista para acumular perguntas correspondentes aos casos
        perguntas_extracao = []
        print("Iniciando a extração de perguntas correspondentes aos casos.")

        # Percorre os IDs e extrai perguntas correspondentes
        for caso_id in casos_id_perguntas:
            print(f"Todos os casos: {situacoes}")
            print(f"O caso que será verificado é o caso de id: {caso_id}")
            if caso_id in perguntas:
                print(
                    f"Caso encontrado no dicionário 'casos' para ID {caso_id}. Perguntas: {perguntas[caso_id]}")
                perguntas_extracao.extend(perguntas[caso_id])
            else:
                print(f"Caso não encontrado no dicionário 'casos' para ID {caso_id}.")

        # Localiza o dicionário do jogador
        jogador_data = next((item for item in dicionario_perguntas if item["jogador"] == data["Jogador"]), None)

        if jogador_data:
            # Filtra apenas as perguntas que ainda não foram respondidas
            perguntas_validas = [pergunta for pergunta in perguntas_extracao if
                                 pergunta in jogador_data["perguntas_nao_respondidas"] and
                                 pergunta not in jogador_data.get("perguntas_respondidas", [])]

            jogador_data["perguntas_pendentes"].extend(perguntas_validas)
            jogador_data["perguntas_pendentes"] = list(
                set(jogador_data["perguntas_pendentes"]))  # Remove duplicatas, se necessário

            print("\nJogador encontrado no dicionário.")
            print(f"Dados do jogador encontrado: {jogador_data}")
            print(f"Perguntas pendentes atualizadas: {jogador_data['perguntas_pendentes']}")

        else:
            print("\nJogador não encontrado no dicionário.")
            return

        # Retorna todas as perguntas pendentes para a fase 3
        return jogador_data["perguntas_pendentes"]

    else:
        print("Fase diferente de 3 detectada. Processando dado sem perguntas.")
        game_state.get_processo().process_data(move=data)
        return None


@app.route('/finalizar_jogo', methods=['POST'])
def finalizar_jogo_route():
    """
    Finaliza a fase para o player. Quando o player clica em finalizar ou desistir jogo, ativa essa tela. E espera
    o host iniciar outra fase ou finalizar o jogo.
    """
    # VALIDAÇÕES
    if not isinstance(game_state.get_processo(), Process):
        return jsonify({"status": "error", "message": "Invalid process instance"}), 400
    if not request.is_json:
        return jsonify({"status": "error", "message": "Invalid content type"}), 415

    data = request.get_json().get('data')
    log_debug(f"Dados recebidos: {data}")
    if not data:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    # Verifica se o jogador finalizou a fase 3, caso sim, envia todas as pergunta pendentes para o player.
    if data.get('fase') == 3:
        print("Fase 3 detectada. Enviando perguntas pendentes para o jogador...")
        jogador_data = next((item for item in dicionario_perguntas if item["jogador"] == data["Jogador"]), None)
        if jogador_data:
            print("Jogador encontrado no dicionário.")
            print(f"Perguntas pendentes: {jogador_data['perguntas_nao_respondidas']}")
            return jsonify({"perguntas": jogador_data["perguntas_nao_respondidas"]}), 200
        else:
            print("Jogador não encontrado no dicionário.")
            return jsonify({"status": "error", "message": "Player not found"}), 400

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

    # Extrai perguntas, respostas, jogadores e tempos_respostas do dicionario_perguntas
    perguntas_export = []
    respostas_export = []
    jogadores_export = []
    tempos_respostas_export = []

    for entry in dicionario_perguntas:
        jogador = entry["jogador"]
        for prt in entry["pergunta/resposta/tempo"]:
            perguntas_export.append(prt["pergunta"])
            respostas_export.append(prt["resposta"])
            jogadores_export.append(jogador)
            tempos_respostas_export.append(prt["horario"])  # Assumindo que já está no formato string

    # Encerrar o jogo passando os dados extraídos
    game_state.get_processo().encerrar_jogo(
        perguntas_export, respostas_export, jogadores_export, tempos_respostas_export
    )

    # Verifica se o arquivo Excel foi criado corretamente
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

# Retirado da aqui, e colocado no main.py
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
