from typing import Optional

from entities.game import Game
from entities.grupo import Grupo
from entities.jogada import Jogada
from entities.jogador import Jogador
from entities.peca import Peca


def pegar_jogada_da_peca(peca: Peca, game: Game, indice: int) -> Optional[Jogada]:
    """
    Cria uma lista com todas as jogadas relacionadas à peça indicada e retorna o índice específico de ordem
    decrescente. Ou seja, se indice for 0, ele retorna o último elemento. Se indice for 1, ele retorna o penúltimo.

    :param peca: Peça cuja jogada deseja-se obter.
    :param game: Jogo atual, onde estão as jogadas.
    :param indice: Índice da jogada que deseja-se obter.
    :return: A jogada no índice especificado ou None se o índice estiver fora dos limites.
    """
    # Filtra as jogadas relacionadas à peça
    jogadas = [jogada for jogada in game.jogadas.values() if jogada.peca == peca]
    # Ordena as jogadas em ordem decrescente (presumindo que a ordem é baseada no ID)
    jogadas.sort(key=lambda x: x.id, reverse=True)

    # Verifica se o índice está dentro dos limites da lista
    if 0 <= indice < len(jogadas):
        return jogadas[indice]

    # Retorna None se o índice estiver fora dos limites
    return None


def pegar_jogada_do_grupo(game: Game, grupo: Grupo, indice: int) -> Jogada | None:
    """
    Cria uma lista com todas as jogadas relacionadas ao grupo indicado e retorna o índice específico de ordem
    decrescente. Ou seja, se indice for 0, ele retorna o último elemento. Se indice for 1, ele retorna o penúltimo.

    :param game: Jogo atual, onde estão as jogadas.
    :param grupo: Grupo cuja jogada deseja-se obter.
    :param indice: Índice da jogada que deseja-se obter.

    :return: A jogada no índice especificado ou None se o índice estiver fora dos limites.
    """
    # Filtra as jogadas relacionadas ao grupo
    jogadas = [jogada for jogada in game.jogadas.values() if jogada.grupo == grupo]
    # Ordena as jogadas em ordem decrescente (presumindo que a ordem é baseada no ID)
    jogadas.sort(key=lambda x: x.id, reverse=True)

    # Verifica se o índice está dentro dos limites da lista
    if 0 <= indice < len(jogadas):
        return jogadas[indice]

    # Retorna None se o índice estiver fora dos limites
    return None


def pegar_jogada_do_jogador(game: Game, jogador: Jogador, indice: int) -> Jogada | None:
    """
    Cria uma lista com todas as jogadas relacionadas ao jogador indicado e retorna o índice específico de ordem
    decrescente. Ou seja, se indice for 0, ele retorna o último elemento. Se indice for 1, ele retorna o penúltimo.

    :param game: Jogo atual, onde estão as jogadas.
    :param jogador: Jogador cuja jogada deseja-se obter.
    :param indice: Índice da jogada que deseja-se obter.

    :return: A jogada no índice especificado ou None se o índice estiver fora dos limites.
    """
    # Filtra as jogadas relacionadas ao jogador
    jogadas = [jogada for jogada in game.jogadas.values() if jogada.peca.jogador == jogador]
    # Ordena as jogadas em ordem decrescente (presumindo que a ordem é baseada no ID)
    jogadas.sort(key=lambda x: x.id, reverse=True)

    # Verifica se o índice está dentro dos limites da lista
    if 0 <= indice < len(jogadas):
        return jogadas[indice]

    # Retorna None se o índice estiver fora dos limites
    return None
