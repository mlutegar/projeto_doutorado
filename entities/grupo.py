from entities.jogador import Jogador
from entities.peca import pecas, tem_lateral_vizinho, tem_lateral_diagonal, Peca


class Grupo:
    def __init__(self, peca):
        self.criador: Jogador = peca.jogador_peca
        self.peca_pai: Peca = peca
        self.pecas: dict[int, Peca] = dict()
        self.members: dict[str, Jogador] = dict()
        self.qtd_cores = 0
        self.qtd_jogadores = 0
        self.qtd_pecas = 0

        grupos[(self.criador.nome, self.peca_pai.uid)] = self

    def add_peca(self) -> None:
        self.pecas[self.peca_pai.uid] = self.peca_pai
        self.set_members()
        self.set_qtd_cores()
        self.set_qtd_jogadores()
        self.set_qtd_pecas()

    def verificar_peca(self, peca) -> bool:
        for uid, peca_analisada in self.pecas.items():
            if peca == peca_analisada:
                return True

    def set_criador(self, criador) -> None:
        """
        Define o criador do grupo.
        """
        self.criador = criador

    def set_peca_pai(self, peca_pai) -> None:
        """
        Define a peça pai do grupo.
        """
        self.peca_pai = peca_pai

    def set_pecas(self, lista_pecas) -> None:
        """
        Adiciona uma peça ao grupo.
        """
        for i in lista_pecas:
            self.pecas[i.uid] = i
        self.set_qtd_cores()
        self.set_qtd_jogadores()
        self.set_qtd_pecas()

    def set_members(self) -> None:
        """
        Analisa as pecas e adicionas os jogadores ao grupo.
        """
        for uid, peca in self.pecas.items():
            self.members[peca.jogador_peca.nome] = peca.jogador_peca

    def set_qtd_cores(self) -> None:
        """
        Define a quantidade de cores do grupo.
        """
        cores = set()
        for uid, peca in self.pecas.items():
            if peca.cor not in cores:
                cores.add(peca.cor)
        self.qtd_cores = len(cores)

    def set_qtd_jogadores(self) -> None:
        """
        Define a quantidade de jogadores do grupo.
        """
        self.qtd_jogadores = len(self.members)

    def set_qtd_pecas(self) -> None:
        """
        Define a quantidade de peças do grupo.
        """
        self.qtd_pecas = len(self.pecas)

    def __eq__(self, other):
        if other is self:
            return True
        if other is None or not isinstance(other, Grupo):
            return False
        return (self.criador == other.criador and
                self.peca_pai == other.peca_pai)

    def __hash__(self):
        return hash((self.criador, self.peca_pai))


grupos = dict()


def criar_grupo(peca) -> Grupo:
    def encontrar_peca_vizinha(item):
        for _, peca_analisada in pecas.items():
            if tem_lateral_vizinho(item.posicao_atual, peca_analisada.posicao_atual):
                return peca_analisada
        return None

    peca_vizinho = encontrar_peca_vizinha(peca)

    if peca_vizinho:
        # Verificar se o vizinho já tem um grupo
        for _, grupo in grupos.items():
            if peca_vizinho in grupo.pecas:
                grupo.add_peca(peca)
                grupo.set_pecas(get_pecas_from_grupo(peca))
                return grupo

    # Se não encontrar um grupo ou vizinho, criar um novo grupo
    grupo = Grupo(peca)
    grupo.set_pecas(get_pecas_from_grupo(peca))
    return grupo


def get_pecas_from_grupo(peca):
    pecas_grupo = set()
    pecas_grupo.add(peca)
    pecas_uid_analisadas = []
    while pecas_grupo:
        peca_analisada = pecas_grupo.pop()
        pecas_uid_analisadas.append(peca_analisada.uid)
        for _, outra_peca in pecas.items():
            if outra_peca.uid in pecas_uid_analisadas or outra_peca in pecas_grupo:
                continue
            if tem_lateral_vizinho(
                    peca_analisada.posicao_atual, outra_peca.posicao_atual
            ) or tem_lateral_diagonal(
                peca_analisada.posicao_atual, outra_peca.posicao_atual
            ):
                pecas_grupo.add(outra_peca)

    pecas_analisadas = []
    for peca_uid_analisada in pecas_uid_analisadas:
        peca_nova = pecas[peca_uid_analisada]
        pecas_analisadas.append(peca_nova)

    return pecas_analisadas


def get_grupo_by_peca(peca):
    """
    Retorna o grupo que contém a peça.
    """
    for grupo in grupos:
        if peca in grupo.pecas:
            return grupo
    return None


# Função para encontrar o grupo pelo qual a peça fazia parte anteriormente
def encontrar_grupo_antigo(peca) -> Grupo | None:
    for grupo in grupos:
        if grupo.verificar_peca(peca):
            return grupo
    return None


def get_grupo_by_peca_pai(peca_pai: Peca) -> Grupo | None:
    """
    Retorna um grupo pelo identificador da peça pai.
    """
    for uid, grupo in grupos.items():
        if grupo.peca_pai == peca_pai:
            return grupo
    return
