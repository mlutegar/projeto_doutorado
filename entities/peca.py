from entities.jogador import Jogador


class Peca:
    def __init__(self):
        self.uid = None
        self.cor = None

        self.linha_antiga = 0
        self.coluna_antiga = 0
        self.posicao_antiga = (0, 0)

        self.linha_atual = 99
        self.coluna_atual = 99
        self.posicao_atual = (99, 99)

        self.jogador_antigo = None

        tabuleiro = Jogador()
        tabuleiro.set_nome("tabuleiro")
        self.jogador = tabuleiro
        self.vizinho = 0

        pecas.append(self)

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

    def set_posicao_atual(self, pos_x, pos_y) -> None:
        """
        Atualiza a posição atual da peça.
        """
        self.posicao_antiga = self.posicao_atual

        if pos_x > 1430:
            self.linha_atual = 99
            self.coluna_atual = 99
            tabuleiro = Jogador()
            tabuleiro.set_nome("tabuleiro")
            self.set_player(tabuleiro)
        else:
            self.linha_atual = definir_linha(pos_y)
            self.coluna_atual = definir_coluna(pos_x)
        self.posicao_atual = [self.linha_atual, self.coluna_atual]
        atualizar_vizinhos()

    def set_posicao(self, posicao):
        self.posicao_antiga = self.posicao_atual
        self.posicao_atual = posicao
        self.linha_antiga = self.linha_atual
        self.coluna_antiga = self.coluna_atual
        self.linha_atual = posicao[0]
        self.coluna_atual = posicao[1]

        if self.linha_atual == 99:
            tabuleiro = Jogador()
            tabuleiro.set_nome("tabuleiro")
            self.jogador_antigo = self.jogador
            self.jogador = tabuleiro

        self.set_vizinho()
        atualizar_vizinhos()

    def set_player(self, player) -> None:
        """
        Define o jogador que moveu a peça.
        """
        self.jogador_antigo = self.jogador
        if self.linha_atual == 99:
            tabuleiro = Jogador()
            tabuleiro.set_nome("tabuleiro")
            self.jogador = tabuleiro
        self.jogador = player

    def set_vizinho(self) -> None:
        """
        Define a quantidade de vizinhos da peça.
        """
        self.vizinho = contar_vizinhos_peca(self)


pecas = []


def atualizar_vizinhos():
    """
    Atualiza a quantidade de vizinhos de todas as peças.
    """
    for peca in pecas:
        peca.set_vizinho()


def remover_peca(peca: Peca):
    """
    Remove uma peça da lista de peças.
    """
    pecas.remove(peca)


def contar_vizinhos_peca(peca: Peca):
    """
    Conta a quantidade de peças vizinhas a uma determinada peça analisando as peças já adicionadas.
    """
    vizinhos = 0
    for outra_peca in pecas:
        if outra_peca.uid == peca.uid:
            continue
        if tem_lateral_vizinho(
                peca.posicao_atual, outra_peca.posicao_atual
        ) or tem_lateral_diagonal(
            peca.posicao_atual, outra_peca.posicao_atual
        ):
            vizinhos += 1
    return vizinhos


def definir_linha(pos_y: int) -> int:
    """
    Define a linha da peça com base na posição x.
    """
    linhas = [74, 143, 211, 284, 351, 424, 490, 561, 633, 702, 770, 841, 912]
    margem_erro = 20

    for i, linha in enumerate(linhas, start=1):
        if abs(pos_y - linha) <= margem_erro:
            return i

    raise ValueError("Posição x fora do intervalo permitido.")


def definir_coluna(pos_x: int) -> int:
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


def tem_lateral_vizinho(pos1: tuple, pos2: tuple) -> bool:
    """
    Verifica se duas peças estão na mesma linha e são de colunas duas unidades distantes.
    """
    linha1, coluna1 = pos1
    linha2, coluna2 = pos2
    return linha1 == linha2 and abs(coluna1 - coluna2) == 2


def tem_lateral_diagonal(pos1: tuple, pos2: tuple) -> bool:
    """
    Verifica se duas posições em colunas subsequentes estão em linhas subsequentes.
    """
    linha1, coluna1 = pos1
    linha2, coluna2 = pos2
    return abs(linha1 - linha2) == 1 and abs(coluna1 - coluna2) == 1


def get_peca_by_uid(uid: int):
    """
    Retorna uma peça pelo seu identificador.
    """
    for peca in pecas:
        if peca.uid == uid:
            return peca
    return None
