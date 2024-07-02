class Jogador:
    def __init__(self):
        """
        Inicializa um novo jogador.
        """
        self.nome = None
        self.infracoes = 0
        self.fez_varias_vezes = False
        self.fez_uma_vez_curto_periodo = False

    def set_nome(self, nome: str) -> None:
        """
        Define o nome do jogador.
        """
        self.nome = nome

    def set_fez_varias_vezes(self) -> None:
        """
        Define se o jogador fez várias vezes uma ação.
        """
        if self.infracoes > 3:
            self.fez_varias_vezes = True

    def set_fez_uma_vez_curto_periodo(self) -> None:
        """
        Define se o jogador fez uma vez em um curto período.
        """
        if self.infracoes == 1:
            self.fez_uma_vez_curto_periodo = True
