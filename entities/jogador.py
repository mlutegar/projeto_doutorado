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

    def incrementar_infracao(self) -> None:
        """
        Incrementa a contagem de infrações do jogador e atualiza os estados correspondentes.
        """
        self.infracoes += 1
        self.atualizar_estados()

    def atualizar_estados(self) -> None:
        """
        Atualiza os estados 'fez_varias_vezes' e 'fez_uma_vez_curto_periodo' com base no número de infrações.
        """
        self.fez_varias_vezes = self.infracoes > 3
        self.fez_uma_vez_curto_periodo = self.infracoes == 1

    def __repr__(self) -> str:
        return (f"Jogador(nome={self.nome}, infracoes={self.infracoes}, "
                f"fez_varias_vezes={self.fez_varias_vezes}, fez_uma_vez_curto_periodo={self.fez_uma_vez_curto_periodo})")


jogadores = []
