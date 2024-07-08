from typing import List, Dict
from entities.jogador import Jogador
from entities.peca import Peca


class Grupo:
    def __init__(self, peca: Peca) -> None:
        """
        Cria um grupo de peças.
        """
        self.criador: Jogador = peca.jogador
        self.peca_pai: Peca = peca
        self.pecas: Dict[int, Peca] = {peca.uid: peca}
        self.members: Dict[str, Jogador] = {peca.jogador.nome: peca.jogador}

        self.qtd_cores: int = 1
        self.qtd_jogadores: int = 1
        self.qtd_pecas: int = 1

    def add_peca(self, peca: Peca) -> None:
        """
        Adiciona uma peça ao grupo.
        :param peca: Peca a ser adicionada ao grupo.
        """
        self.pecas[peca.uid] = peca
        self.atualizar_status()

    def remover_peca(self, peca: Peca) -> None:
        """
        Remove uma peça do grupo.
        :param peca: Peca a ser removida do grupo.
        """
        if peca.uid in self.pecas:
            self.pecas.pop(peca.uid)
            self.atualizar_status()

            if peca == self.peca_pai and self.pecas:
                self.peca_pai = next(iter(self.pecas.values()))
                self.criador = self.peca_pai.jogador

    def atualizar_status(self) -> None:
        """
        Atualiza as informações do grupo.
        """
        self.set_members()
        self.set_qtd_cores()
        self.set_qtd_jogadores()
        self.set_qtd_pecas()

    def verificar_peca(self, peca: Peca) -> bool:
        """
        Verifica se a peça está no grupo.
        :param peca: Peca a ser verificada.
        :return: True se a peça está no grupo, false caso contrário.
        """
        return peca.uid in self.pecas

    def set_pecas(self, lista_pecas: List[Peca]) -> None:
        """
        Adiciona uma peça ao grupo e atualiza as informações do grupo.
        :param lista_pecas: Lista de peças a serem adicionadas ao grupo.
        """
        for peca in lista_pecas:
            self.pecas[peca.uid] = peca
        self.atualizar_status()

    def set_members(self) -> None:
        """
        Analisa as pecas e adiciona os jogadores ao grupo.
        """
        self.members = {peca.jogador.nome: peca.jogador for peca in self.pecas.values()}

    def set_qtd_cores(self) -> None:
        """
        Define a quantidade de cores do grupo a partir das peças.
        """
        self.qtd_cores = len(set(peca.cor for peca in self.pecas.values()))

    def set_qtd_jogadores(self) -> None:
        """
        Define a quantidade de jogadores do grupo a partir das peças.
        """
        self.qtd_jogadores = len(self.members)

    def set_qtd_pecas(self) -> None:
        """
        Define a quantidade de peças do grupo a partir da lista de peças.
        """
        self.qtd_pecas = len(self.pecas)

    def __eq__(self, other: object) -> bool:
        """
        Verifica se dois grupos são iguais.
        :param other: Outro grupo a ser comparado.
        :return: True se os grupos são iguais, false caso contrário.
        """
        if not isinstance(other, Grupo):
            return False
        return self.criador == other.criador and self.peca_pai == other.peca_pai

    def __hash__(self) -> int:
        """
        Retorna o hash do grupo.
        :return: Hash do grupo.
        """
        return hash((self.criador, self.peca_pai))
