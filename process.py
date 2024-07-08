from entities.csv_export import CsvExport
from entities.game import Game
from entities.jogada import Jogada
from entities.jogador import Jogador
from entities.peca import Peca
from entities.situacao import Situacao

game: Game | None = None
csv_instance = None


def iniciar_jogo(nome, host) -> None:
    """
    Função que inicia o objeto do jogo.
    :param nome: Nome do jogo.
    :param host: Host do jogo.
    """
    global game
    game = Game(name=nome, host=host)


def process_data(move: dict) -> None:
    """
    Processa os dados da jogada, atualizando a lista de movimentos.
    """
    required_keys = {"UID", "PosX", "PosY", "Tempo", "Jogador", "Cor"}
    if not required_keys.issubset(move.keys()):
        raise ValueError("Dados incompletos recebidos")

    jogador = None
    peca = None

    for jogador in jogadores:
        if jogador.nome == move["Jogador"]:
            # atualizar jogador
            jogador = jogador
    if not jogador:
        # definir jogador
        jogador = Jogador(move["Jogador"])

    for peca in pecas:
        if peca.uid == int(move["UID"]):
            # lógica para atualizar peça
            peca = peca
    if not peca:
        # lógica para verificar vizinhança
        peca = Peca(int(move["UID"]))
        peca.set_cor(move["Cor"])

    peca.set_posicao_atual(int(move["PosX"]), int(move["PosY"]))
    peca.set_player(jogador)
    peca.set_vizinho()

    # definir jogada
    jogada = Jogada()
    jogada.set_peca(peca)
    jogada.set_tempo(int(move["Tempo"]))

    # definir situação
    situacao = Situacao(jogada)

    # atualizar listas
    if jogadores[jogador.nome]:
        jogadores[jogador.nome] = jogador
    else:
        jogadores.add(jogador)

    if pecas[peca.uid]:
        pecas[peca.uid] = peca
        print(
            f"Peca atualizada: "
            f"UID={peca.uid}, "
            f"Cor={peca.cor}, "
            f"Posição Antiga={peca.posicao_antiga}, "
            f"Posição Atual={peca.posicao}, "
            f"Player={peca.jogador}, "
            f"LastPlayer={peca.jogador_antigo}"
        )
    else:
        print(
            f"Peca criada: "
            f"UID={peca.uid}, "
            f"Cor={peca.cor}, "
            f"Posição Antiga={peca.posicao_antiga}, "
            f"Posição Atual={peca.posicao}, "
            f"Player={peca.jogador}, "
            f"LastPlayer={peca.jogador_antigo}"
        )

    print(f"Grupo: {jogada.grupo.id} - {jogada.grupo.qtd_pecas} peças")
    print(f"Jogador: {jogador.nome}")
    print(f"Tempo: {jogada.tempo} segundos")
    print(f"Situacao: {situacao.casos_id}")
    print("")
    exportar.append((jogada, situacao.casos_id))


def encerrar_jogo() -> None:
    """
    Encerra o jogo e exporta os dados.
    """
    global csv_instance
    global game

    if not game:
        raise ValueError("Jogo não iniciado")
    else:
        csv_instance = CsvExport(path='data.csv', game=game)

    csv_instance.analisar_game()
    csv_instance.write()

    print("Jogo encerrado. Dados exportados com sucesso.")
    print("Exportando arquivo CSV...")
    print("Arquivo exportado com sucesso.")
    print("Fim do jogo.")

