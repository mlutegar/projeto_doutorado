from projeto_doutorado.entities.jogador import Jogador
from projeto_doutorado.entities.peca import Peca


class Jogada:
    def __init__(self):
        """
        Inicializa uma nova jogada com os atributos especificados.
        """
        self.id = None
        self.peca = None
        self.jogador = None
        self.tempo = None

    def set_peca(self, peca: Peca) -> None:
        """
        Define a peça associada à jogada.
        """
        self.peca = peca

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
