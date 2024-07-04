from entities.peca import pecas, tem_lateral_vizinho, tem_lateral_diagonal, Peca, get_peca_by_uid


class Grupo:
    def __init__(self):
        self.id = None
        self.criador = None
        self.peca_pai = None
        self.pecas = []
        self.members = []
        self.qtd_cores = 0
        self.qtd_jogadores = 0
        self.qtd_pecas = 0

    def add_peca(self, peca) -> None:
        self.pecas.append(peca)
        if len(self.pecas) == 1:
            self.peca_pai = peca
            self.criador = peca.jogador

        self.set_members()
        self.set_qtd_cores()
        self.set_qtd_jogadores()
        self.set_qtd_pecas()

    def verificar_peca(self, peca) -> bool:
        return peca in self.pecas

    def set_id(self, id_grupo) -> None:
        """
        Define o id do grupo.
        """
        self.id = id_grupo

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
        self.pecas = lista_pecas
        self.set_qtd_cores()
        self.set_qtd_jogadores()
        self.set_qtd_pecas()

    def set_members(self) -> None:
        """
        Analisa as pecas e adicionas os jogadores ao grupo.
        """
        for peca in self.pecas:
            if peca.jogador not in self.members:
                self.members.append(peca.jogador)

    def set_qtd_cores(self) -> None:
        """
        Define a quantidade de cores do grupo.
        """
        cores = []
        for peca in self.pecas:
            if peca.cor not in cores:
                cores.append(peca.cor)
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


grupos = []


def criar_grupo(peca) -> Grupo:
    # definir grupo
    grupo = Grupo()
    if peca.vizinho == 1:
        grupo.set_id(len(grupos) + 1)
        grupo.add_peca(peca)
        grupo.set_pecas(get_pecas_from_grupo(peca))
        grupos.append(grupo)
    elif peca.vizinho > 1:
        # verificar quem sao as pecas desse grupo que acabou de entrar
        pecas_grupo_novo = get_pecas_from_grupo(peca)
        # verificar quem é a peça pai desse grupo
        peca_pai = pecas_grupo_novo[0]
        # atualizar o grupo
        grupo = get_grupo_by_peca_pai(peca_pai)
        grupo.set_pecas(pecas_grupo_novo)
        substituir_grupo(grupo)
    return grupo


def get_pecas_from_grupo(peca):
    pecas_grupo = [peca]
    pecas_uid_analisadas = []
    while pecas_grupo:
        peca_analisada = pecas_grupo.pop()
        pecas_uid_analisadas.append(peca_analisada.uid)
        for outra_peca in pecas:
            if outra_peca.uid in pecas_uid_analisadas or outra_peca in pecas_grupo:
                continue
            if tem_lateral_vizinho(
                    peca_analisada.posicao_atual, outra_peca.posicao_atual
            ) or tem_lateral_diagonal(
                peca_analisada.posicao_atual, outra_peca.posicao_atual
            ):
                pecas_grupo.append(outra_peca)

    pecas_analisadas = []
    for peca_uid_analisada in pecas_uid_analisadas:
        peca_nova = get_peca_by_uid(peca_uid_analisada)
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
    for grupo in grupos:
        if grupo.peca_pai == peca_pai:
            return grupo
    return


def substituir_grupo(grupo_novo):
    """
    Substitui um grupo existente.
    """
    for i, grupo in enumerate(grupos):
        if grupo_novo.peca_pai.uid == grupo.peca_pai.uid:
            grupos[i] = grupo_novo
            return
