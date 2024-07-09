from datetime import timedelta

from entities.csv_export import CsvExport
from entities.game import Game
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
    # variaves

    required_keys = {"UID", "PosX", "PosY", "Tempo", "Jogador", "Cor"}
    if not required_keys.issubset(move.keys()):
        raise ValueError("Dados incompletos recebidos")

    if not move["UID"] in game.pecas:
        peca = game.add_peca(uid=int(move["UID"]), cor=move["Cor"])
    else:
        peca = game.pecas[move["UID"]]

    if not move["Jogador"] in game.jogadores:
        jogador = game.add_jogador(nome=move["Jogador"])
    else:
        jogador = game.jogadores[move["Jogador"]]

    peca.set_posicao_atual(pos_x=int(move["PosX"]), pos_y=int(move["PosY"]), jogador=jogador)
    game.add_jogada(peca=peca, tempo=timedelta(seconds=move["Tempo"]))


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
