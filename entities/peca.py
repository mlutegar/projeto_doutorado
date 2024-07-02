def definir_linha(pos_x: int) -> int:
    """
    Define a linha da peça com base na posição x.
    """
    linhas = [74, 143, 211, 284, 351, 424, 497, 565, 638, 706, 779, 846, 919]
    margem_erro = 20

    for i, linha in enumerate(linhas, start=1):
        if abs(pos_x - linha) <= margem_erro:
            return i
    raise ValueError("Posição x fora do intervalo permitido.")


def definir_coluna(pos_y: int) -> int:
    """
    Define a coluna da peça com base na posição y.
    """
    colunas = [86, 123, 163, 200, 239, 276, 316, 353, 393, 430, 470, 507, 547, 584, 624, 661, 701, 738, 778, 815,
               855, 892, 932, 969, 1009, 1046, 1086, 1123, 1163, 1200, 1240, 1277, 1317, 1354]
    margem_erro = 20

    for i, coluna in enumerate(colunas, start=1):
        if abs(pos_y - coluna) <= margem_erro:
            return i
    raise ValueError("Posição y fora do intervalo permitido.")


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
        self.linha_antiga = definir_linha(pos_x)
        self.coluna_antiga = definir_coluna(pos_y)
        self.posicao_antiga = [self.linha_antiga, self.coluna_antiga]

    def set_posicao_atual(self, pos_x, pos_y) -> None:
        """
        Atualiza a posição atual da peça.
        """
        self.linha_atual = definir_linha(pos_x)
        self.coluna_atual = definir_coluna(pos_y)
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
