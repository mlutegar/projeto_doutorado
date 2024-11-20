from src.entities.jogador import Jogador


class Peca:
    def __init__(self, uid: int, cor: str) -> None:
        """
        Inicializa a peça com um identificador único e uma cor.

        :param uid: Identificador único da peça.
        :param cor: Cor da peça.
        """
        self.uid: int = uid
        self.cor: str = cor

        self.posicao: tuple[int, int] = (-1, -1)
        self.linha: int = self.posicao[0]
        self.coluna: int = self.posicao[1]

        self.local: str = "monte"
        self.jogador: Jogador | None = None
        self.eh_ponte: bool = False
        self.ponte_qtd_lideres: int = 0

    def set_posicao_atual_tabuleiro1(self, pos_x: int, pos_y: int, jogador: Jogador) -> None:
        """
        Atualiza a posição atual da peça.

        :param pos_x: Posição x da peça. (as posições podem ser [86, 123, 163, 200, 239, 276, 316, 353, 393, 430, 469, 506, 547, 584, 622, 657, 698, 736, 775, 813,
                   852, 890, 928, 966, 1004, 1042, 1082, 1119, 1158, 1196, 1233, 1270, 1312, 1350])
        :param pos_y: Posição y da peça. (as posições podem ser [74, 143, 211, 284, 351, 424, 490, 561, 633, 702, 770, 841, 912])
        :param jogador: Jogador que moveu a peça.
        """
        if pos_x > 1430:
            self.linha = -1
            self.coluna = -1
            self.local = "monte"
        else:
            self.linha = self.definir_linha_tabuleiro1(pos_y)
            self.coluna = self.definir_coluna_tabuleiro1(pos_x)
            self.local = "tabuleiro"
        self.posicao = (self.linha, self.coluna)
        self.jogador = jogador

    def set_posicao_atual_tabuleiro2(self, pos_x: int, pos_y: int, jogador: Jogador) -> None:
        """
        Atualiza a posição atual da peça.

        :param pos_x: Posição x da peça. (as posições podem ser [110, 184, 260, 337, 414, 490, 568, 643, 719, 796,
        873, 949, 1025, 1103, 1179, 1254, 1333])
        :param pos_y: Posição y da peça. (as posições podem ser [85, 154, 222, 295, 362, 435, 501, 572, 644, 713,
        781, 852, 923])
        :param jogador: Jogador que moveu a peça.
        """
        if pos_x > 1430:
            self.linha = -1
            self.coluna = -1
            self.local = "monte"
        else:
            self.linha = self.definir_linha_tabuleiro2(pos_y)
            self.coluna = self.definir_coluna_tabuleiro2(pos_x)
            self.local = "tabuleiro"
        self.posicao = (self.linha, self.coluna)
        self.jogador = jogador

    @staticmethod
    def definir_linha_tabuleiro1(pos_y: int) -> int:
        """
        Define a linha da peça com base na posição x.
        """
        linhas = [74, 143, 211, 284, 351, 424, 490, 561, 633, 702, 770, 841, 912]
        margem_erro = 20

        for i, linha in enumerate(linhas, start=1):
            if abs(pos_y - linha) <= margem_erro:
                return i

        raise ValueError("Posição x fora do intervalo permitido.")

    @staticmethod
    def definir_coluna_tabuleiro1(pos_x: int) -> int:
        """
        Define a coluna da peça com base na posição y.
        """
        colunas = [86, 123, 163, 200, 239, 276, 316, 353, 393, 430, 469, 506, 547, 584, 622, 657, 698, 736, 775, 813,
                   852, 890, 928, 966, 1004, 1042, 1082, 1119, 1158, 1196, 1233, 1270, 1312, 1350]
        margem_erro = 20

        for i, coluna in enumerate(colunas, start=1):
            if abs(pos_x - coluna) <= margem_erro:
                return i

        raise ValueError("Posição y fora do intervalo permitido.")

    @staticmethod
    def definir_linha_tabuleiro2(pos_y: int) -> int:
        """
        Define a linha da peça com base na posição x.
        """
        linhas = [85, 154, 222, 295, 362, 435, 501, 572, 644, 713, 781, 852, 923]
        margem_erro = 20

        for i, linha in enumerate(linhas, start=1):
            if abs(pos_y - linha) <= margem_erro:
                return i

        raise ValueError("Posição x fora do intervalo permitido.")

    @staticmethod
    def definir_coluna_tabuleiro2(pos_x: int) -> int:
        """
        Define a coluna da peça com base na posição y.
        """
        colunas = [110, 184, 260, 337, 414, 490, 568, 643, 719, 796, 873, 949, 1025, 1103, 1179, 1254, 1333]
        margem_erro = 20

        for i, coluna in enumerate(colunas, start=1):
            if abs(pos_x - coluna) <= margem_erro:
                return i

        raise ValueError("Posição y fora do intervalo permitido.")

    def __eq__(self, other: object) -> bool:
        """
        Verifica se duas peças são iguais.

        :param other: Outro objeto para comparação.
        :return: True se as peças são iguais, False caso contrário.
        """
        if not isinstance(other, Peca):
            return False
        return self.uid == other.uid

    def __hash__(self) -> int:
        """
        Retorna o hash da peça.

        :return: Hash da peça baseado no seu identificador único.
        """
        return hash(self.uid)
