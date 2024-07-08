from datetime import timedelta
from entities.grupo import Grupo
from entities.peca import Peca


class Jogada:
    def __init__(self, uid: int, peca: Peca, grupo: Grupo, tempo: timedelta) -> None:
        """
        Inicializa uma nova jogada com os atributos especificados.

        :param uid: Identificador único da jogada.
        :param peca: Peça que foi movida.
        :param grupo: Grupo ao qual a peça pertence.
        :param tempo: Tempo que o jogador levou para realizar a jogada.
        """
        self.id: int = uid
        self.peca: Peca = peca
        self.grupo: Grupo = grupo
        self.tempo: timedelta = tempo

    def to_dict(self) -> dict:
        """
        Retorna um dicionário com as informações da jogada.

        :return: Dicionário contendo os dados da jogada.
        """
        return {
            "id": self.id,
            "peca_uid": self.peca.uid,
            "tempo": self.tempo,
            "peca_cor": self.peca.cor,
            "peca_posicao_antiga": self.peca.posicao_antiga,
            "peca_posicao_atual": self.peca.posicao,
            "peca_last_player": self.peca.jogador_antigo,
            "peca_vizinho": self.peca.qtd_vizinho,
        }

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
