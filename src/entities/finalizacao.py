from src.entities.jogador import Jogador
from datetime import timedelta, datetime


class Finalizacao:
    def __init__(self, jogador: Jogador, descricao: str, tempo: timedelta) -> None:
        """
        Inicializa uma nova finalização com os atributos especificados.
        Pode ser desistencia ou finalizacao.
        :param jogador: Jogador que realizou a finalização.
        :param descricao: Descrição da finalização. Pode ser "Desistiu" ou "Finalizou".
        :param tempo: Tempo que o jogador levou para realizar a finalização.
        """
        self.jogador: Jogador = jogador
        self.descricao: str = descricao
        self.tempo: timedelta = tempo
        self.horario_da_finalizacao: datetime = datetime.now()

        # limitar a descrição para apenas "Desistiu" ou "Finalizou"
        if descricao not in ["Desistiu", "Finalizou"]:
            raise ValueError("Descrição inválida. A descrição deve ser 'Desistiu' ou 'Finalizou'.")
