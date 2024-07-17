from datetime import timedelta

from entities.csv_export import CsvExport
from entities.finalizacao import Finalizacao
from entities.game import Game
csv_instance = None


def iniciar_jogo(nome: str, host: str, game: Game) -> None:
    """
    Função que inicia o objeto do jogo.
    :param nome: Nome do jogo.
    :param host: Host do jogo.
    :param game: Instância do jogo.
    """
    game = Game(name=nome, host=host)


def process_data(game: Game, move: dict) -> None:
    """
    Processa os dados da jogada, atualizando a lista de movimentos.

    :param game: Instância do jogo.
    :param move: Dicionário contendo os dados da jogada.
    """
    # Verifica se todas as chaves necessárias estão presentes
    required_keys = {"UID", "PosX", "PosY", "Tempo", "Jogador", "Cor"}
    if not required_keys.issubset(move.keys()):
        raise ValueError("Dados incompletos recebidos")

    # Obtém ou adiciona a peça no jogo
    if move["UID"] not in game.pecas:
        peca = game.add_peca(uid=int(move["UID"]), cor=move["Cor"])
    else:
        peca = game.pecas[move["UID"]]

    # Obtém ou adiciona o jogador no jogo
    if move["Jogador"] not in game.jogadores:
        jogador = game.add_jogador(nome=move["Jogador"])
    else:
        jogador = game.jogadores[move["Jogador"]]

    # Atualiza a posição da peça
    peca.set_posicao_atual(pos_x=int(move["PosX"]), pos_y=int(move["PosY"]), jogador=jogador)

    # Adiciona a jogada no jogo
    game.add_jogada(peca=peca, tempo=timedelta(seconds=int(move["Tempo"])))


def finalizar_jogo(game: Game, move: dict) -> Finalizacao:
    """
    Jogador encerra a partida para ele.
    Move: {"Jogador": "nome_do_jogador", "Acao": "Desistiu"/"Finalizou"}
    """
    required_keys = {"Jogador", "Acao"}
    if not required_keys.issubset(move.keys()):
        raise ValueError("Dados incompletos recebidos")

    jogador_nome = move["Jogador"]
    acao = move["Acao"]

    if jogador_nome not in game.jogadores:
        raise ValueError(f"Jogador {jogador_nome} não encontrado no jogo")

    jogador = game.jogadores[jogador_nome]

    if acao == "Desistiu":
        finalizacao = game.desistir(player=jogador)
    elif acao == "Finalizou":
        finalizacao = game.finalizar(player=jogador)
    else:
        raise ValueError("Ação inválida. Use 'Desistiu' ou 'Finalizou'.")

    return finalizacao


def encerrar_jogo(game: Game) -> None:
    """
    Encerra o jogo e exporta os dados.
    """
    global csv_instance

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
