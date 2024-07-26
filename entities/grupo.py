from datetime import datetime
from typing import List, Dict
from entities.jogador import Jogador
from entities.peca import Peca


class Grupo:
    def __init__(self, peca: Peca) -> None:
        """
        Cria um grupo de peças.

        :param peca: Peça fundadora do grupo. A peça que quando foi colocada no tabuleiro, formou o grupo.
        """
        # definir informações principais do grupo
        self.criador: Jogador = peca.jogador
        self.peca_pai: Peca = peca
        self.pecas: Dict[int, Peca] = {peca.uid: peca}
        self.members: Dict[str, Jogador] = {peca.jogador.nome: peca.jogador}

        # definir informações de quantidade do grupo
        self.qtd_cores: int = 1
        self.qtd_jogadores: int = 1
        self.qtd_pecas: int = 1

        # definir informações de tempo
        self.horario_criado: datetime = datetime.now()

        # definir informações de identificação
        self.id = hash((self.criador, self.peca_pai))

        # definir informações de estrutura para então comparar com outros grupos e dizer se são iguais
        # em relação à estrutura
        self.estrutura: str = "-"

    def add_peca(self, peca: Peca) -> None:
        """
        Adiciona uma peça ao grupo.
        :param peca: Peca a ser adicionada ao grupo.
        """
        self.pecas[peca.uid] = peca
        self.atualizar_status()
        self.atualizar_estrutura()

    def remover_peca(self, peca: Peca) -> None | tuple[str, int]:
        """
        Remove uma peça do grupo.
        :param peca: Peca a ser removida do grupo.
        :return: Retorna True se o grupo foi removido, False caso contrário.
        """
        if peca.uid in self.pecas:
            # Remove a peça do dicionário de peças do grupo
            self.pecas.pop(peca.uid)

            # Atualiza o status do grupo após a remoção
            self.atualizar_status()
            self.atualizar_estrutura()

            # Verifica se a peça removida era a peça principal (peca_pai)
            if peca == self.peca_pai and self.pecas:
                # Define uma nova peça principal se ainda houver peças no grupo
                self.peca_pai = next(iter(self.pecas.values()))
                self.criador = self.peca_pai.jogador

            # Verifica se o tamanho do grupo é igual a 1 após a remoção
            if len(self.pecas) == 1:
                chave = (self.criador.nome, self.peca_pai.uid)
                return chave  # Retorna a chave do grupo removido

        return None  # Indica que o grupo não foi removido

    def atualizar_status(self) -> None:
        """
        Atualiza as informações do grupo.
        """
        self.set_members()
        self.set_qtd_cores()
        self.set_qtd_jogadores()
        self.set_qtd_pecas()

    def atualizar_estrutura(self) -> None:
        """
        Atualiza a estrutura do grupo.
        """
        self.estrutura = self.definir_estrutura()

    def definir_estrutura(self) -> str:
        """
        Define a estrutura do grupo. Ele olha o formato do grupo e retorna uma string que representa a estrutura.
        Para isso ele pega a posição (linha e coluna) de cada peça e verifica se elas estão em uma linha, coluna
        ou diagonal.
        """
        pass

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
