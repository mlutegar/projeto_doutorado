from datetime import datetime, timedelta
from typing import Optional, List


class Jogador:
    def __init__(self, nome: str) -> None:
        """
        Inicializa um novo jogador.

        :param nome: Nome do jogador.
        """
        self.nome: str = nome  # Chave primária
        self.situacao: str = "Jogando"
        self.tempo_em_jogo: timedelta = timedelta(seconds=0)
        self.tempo_inicio: datetime = datetime.now()
        self.tempo_fim: Optional[datetime] = None

        self.qtd_infracoes: int = 0
        self.tabulacao: List[int] = []

    def adicionar_infracao(self) -> None:
        """
        Adiciona uma infração ao jogador.
        """
        self.qtd_infracoes += 1

    def adicionar_tabulacao(self, tabulacao: int) -> None:
        """
        Adiciona uma tabulação ao jogador.

        :param tabulacao: Valor da tabulação.
        """
        self.tabulacao.append(tabulacao)

    def desistir(self) -> None:
        """
        Permite que o jogador desista, alterando a situação para "Desistiu" e registrando o tempo final.

        :raises ValueError: Se o jogador já finalizou ou desistiu.
        """
        if self.situacao != "Jogando":
            raise ValueError("Jogador já finalizou ou desistiu.")
        self.situacao = "Desistiu"
        self.set_tempo_final()

    def finalizar(self) -> None:
        """
        Permite que o jogador finalize, alterando a situação para "Finalizou" e registrando o tempo final.

        :raises ValueError: Se o jogador já finalizou ou desistiu.
        """
        if self.situacao != "Jogando":
            raise ValueError("Jogador já finalizou ou desistiu.")
        self.situacao = "Finalizou"
        self.set_tempo_final()

    def set_tempo_final(self) -> None:
        """
        Define o tempo total que o jogador ficou em jogo.
        """
        self.tempo_fim = datetime.now()
        self.tempo_em_jogo = self.tempo_fim - self.tempo_inicio

    def __repr__(self) -> str:
        """
        Retorna uma representação textual do objeto.

        :return: Uma string representando o objeto Jogador.
        """
        return (f"Jogador(nome={self.nome}, situacao={self.situacao}, "
                f"tempo_em_jogo={self.tempo_em_jogo})")

    def __eq__(self, other: object) -> bool:
        """
        Verifica se dois jogadores são iguais.

        :param other: Outro objeto para comparação.
        :return: True se os jogadores são iguais, False caso contrário.
        """
        if not isinstance(other, Jogador):
            return False
        return self.nome == other.nome

    def __hash__(self) -> int:
        """
        Retorna o hash do objeto.

        :return: O hash baseado no nome do jogador.
        """
        return hash(self.nome)
