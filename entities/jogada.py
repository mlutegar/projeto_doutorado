from entities.grupo import criar_grupo
from entities.jogador import Jogador
from entities.peca import Peca


class Jogada:
    def __init__(self):
        """
        Inicializa uma nova jogada com os atributos especificados.
        """
        self.id = None
        self.peca = None
        self.grupo = None
        self.jogador = None
        self.tempo = None

    def set_peca(self, peca: Peca) -> None:
        """
        Define a peça associada à jogada.
        """
        self.peca = peca

    def set_grupo(self) -> None:
        """
        Define o grupo associado à jogada.
        """
        self.grupo = criar_grupo(self.peca)

    def set_jogador(self, jogador: Jogador) -> None:
        """
        Define o jogador associado à jogada.
        """
        self.jogador = jogador

    def set_tempo(self, tempo: int) -> None:
        """
        Define o tempo da jogada.
        """
        self.tempo = tempo

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "peca_uid": self.peca.uid if self.peca else None,
            "jogador": self.jogador,
            "tempo": self.tempo,
            "peca_cor": self.peca.cor if self.peca else None,
            "peca_posicao_antiga": self.peca.posicao_antiga if self.peca else None,
            "peca_posicao_atual": self.peca.posicao_atual if self.peca else None,
            "peca_grupo": self.peca.grupo if self.peca else None,
            "peca_last_player": self.peca.jogador_antigo if self.peca else None,
            "peca_vizinho": self.peca.vizinho if self.peca else None,
        }


jogadas = []
