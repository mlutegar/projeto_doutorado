from entities.grupo import criar_grupo
from entities.peca import Peca


class Jogada:
    def __init__(self):
        """
        Inicializa uma nova jogada com os atributos especificados.
        """
        self.id = len(jogadas) + 1
        self.peca = None
        self.grupo = None
        self.jogador_jogada = None
        self.tempo = None

    def set_peca(self, peca: Peca) -> None:
        """
        Define a peça associada à jogada.
        """
        self.peca = peca
        self.set_grupo()
        self.set_jogador()

    def set_grupo(self) -> None:
        """
        Define o grupo associado à jogada.
        """
        self.grupo = criar_grupo(self.peca)

    def set_jogador(self) -> None:
        """
        Define o jogador associado à jogada.
        """
        self.jogador_jogada = self.peca.jogador_peca

    def set_tempo(self, tempo: int) -> None:
        """
        Define o tempo da jogada.
        """
        self.tempo = tempo

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "peca_uid": self.peca.uid if self.peca else None,
            "jogador": self.jogador_jogada,
            "tempo": self.tempo,
            "peca_cor": self.peca.cor if self.peca else None,
            "peca_posicao_antiga": self.peca.posicao_antiga if self.peca else None,
            "peca_posicao_atual": self.peca.posicao_atual if self.peca else None,
            "peca_grupo": self.peca.grupo if self.peca else None,
            "peca_last_player": self.peca.jogador_antigo if self.peca else None,
            "peca_vizinho": self.peca.vizinho if self.peca else None,
        }

    def __eq__(self, other):
        if other is self:
            return True
        if other is None or not isinstance(other, Jogada):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


jogadas = {}
