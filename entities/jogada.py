from datetime import timedelta, datetime
from entities.grupo import Grupo
from entities.peca import Peca


class Jogada:
    def __init__(self, uid: int, peca: Peca, grupo: Grupo, tempo: timedelta, fase: int) -> None:
        """
        Inicializa uma nova jogada com os atributos especificados.

        :param uid: Identificador único da jogada.
        :param peca: Peça que foi movida.
        :param grupo: Grupo ao qual a peça pertence.
        :param tempo: Tempo que o jogador levou para realizar a jogada.
        :param fase: Fase da jogada.
        """
        self.id: int = uid
        self.peca: Peca = peca
        self.grupo: Grupo = grupo
        self.tempo: timedelta = tempo
        self.fase: int = fase
        self.horario_da_jogada = datetime.now()
        self.tempo_desde_ultimo_movimento: timedelta = timedelta(0)

    def __eq__(self, other: object) -> bool:
        """
        Verifica se esta jogada é igual a outra jogada.

        :param other: Outra instância de Jogada para comparação.
        :return: True se as jogadas são iguais, false caso contrário.
        """
        if other is self:
            return True
        if other is None or not isinstance(other, Jogada):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """
        Retorna o hash da jogada.

        :return: Hash da jogada baseado no seu identificador único.
        """
        return hash(self.id)
