class Jogador:
    def __init__(self):
        """
        Inicializa um novo jogador.
        """
        self.nome = None
        self.fez_varias_vezes = False
        self.fez_uma_vez_curto_periodo = False

    def set_nome(self, nome: str) -> None:
        """
        Define o nome do jogador.
        """
        self.nome = nome

    def set_fez_varias_vezes(self, valor: bool) -> None:
        """
        Define se o jogador fez várias vezes uma ação.
        """
        self.fez_varias_vezes = valor

    def set_fez_uma_vez_curto_periodo(self, valor: bool) -> None:
        """
        Define se o jogador fez uma vez em um curto período.
        """
        self.fez_uma_vez_curto_periodo = valor
