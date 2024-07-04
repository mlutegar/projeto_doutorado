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

    def set_id(self, id) -> None:
        """
        Define o id do grupo.
        """
        self.id = id

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

    def set_pecas(self, pecas) -> None:
        """
        Adiciona uma peça ao grupo.
        """
        self.pecas = pecas

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


def get_grupo_by_peca(peca):
    """
    Retorna o grupo que contém a peça.
    """
    for grupo in grupos:
        if peca in grupo.pecas:
            return grupo
    return None


# Função para encontrar o grupo pelo qual a peça fazia parte anteriormente
def encontrar_grupo_antigo(peca):
    for grupo in grupos:
        if grupo.verificar_peca(peca):
            return grupo
    return None
