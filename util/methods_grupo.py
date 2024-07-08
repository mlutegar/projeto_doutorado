from entities.game import Game
from entities.grupo import Grupo
from entities.peca import Peca


def get_grupo_by_peca_pai(peca_pai: Peca, game: Game) -> Grupo | None:
    """
    Retorna um grupo pelo identificador da peça pai. Caso não encontre, retorna None.
    :param peca_pai: Identificador da peça pai.
    :param game: Jogo.
    """
    for uid, grupo in game.grupos.items():
        if grupo.peca_pai == peca_pai:
            return grupo
    return None
