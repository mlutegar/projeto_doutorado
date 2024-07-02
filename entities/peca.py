class Peca:
    def __init__(self):
        self.uid = None
        self.cor = None

        self.linha_antiga = None
        self.coluna_antiga = None
        self.posicao_antiga = None

        self.linha_atual = None
        self.coluna_atual = None
        self.posicao_atual = None

        self.grupo = None
        self.last_player = None
        self.player = None
        self.vizinho = 0

    def set_uid(self, uid: int) -> None:
        """
        Define o identificador da peça.
        """
        self.uid = uid

    def set_cor(self, cor: str) -> None:
        """
        Define a cor da peça.
        """
        self.cor = cor

    def set_posicao_antiga(self, pos_x, pos_y) -> None:
        """
        Atualiza a posição antiga da peça.
        """
        self.linha_antiga = pos_x
        self.coluna_antiga = pos_y
        self.posicao_antiga = [self.linha_antiga, self.coluna_antiga]

    def set_posicao_atual(self, pos_x, pos_y) -> None:
        """
        Atualiza a posição atual da peça.
        """
        self.linha_atual = pos_x
        self.coluna_atual = pos_y
        self.posicao_atual = [self.linha_atual, self.coluna_atual]

    def set_grupo(self, grupo: int) -> None:
        """
        Define o grupo da peça.
        """
        self.grupo = grupo

    def set_last_player(self, last_player: str) -> None:
        """
        Define o último jogador que moveu a peça.
        """
        self.last_player = last_player

    def set_player(self, player: str) -> None:
        """
        Define o jogador que moveu a peça.
        """
        self.player = player

    def set_vizinho(self, vizinho: int) -> None:
        """
        Define a quantidade de vizinhos da peça.
        """
        self.vizinho = vizinho
