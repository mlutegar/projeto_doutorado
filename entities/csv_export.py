from entities.finalizacao import Finalizacao
from entities.game import Game
from entities.jogada import Jogada
from entities.situacao import Situacao
from typing import List
import csv
from pathlib import Path


class CsvExport:
    def __init__(self, path: str, game: Game) -> None:
        """
        Inicializa a classe Csv com o caminho do arquivo e o jogo.
        """
        self.path: Path = Path(path)
        self.game: Game = game
        self.list_cvs: List = []

    def analisar_game(self) -> None:
        """
        Analisa todas as jogadas feitas no game e atribui uma situacao para cada uma delas.
        """
        for jogada in self.game.jogadas.values():
            situacao = Situacao(game=self.game, jogada=jogada)
            self.list_cvs.append((jogada, situacao.casos_id))

        for finalizacao in self.game.finalizacoes.values():
            situacao = Situacao(game=self.game, finalizacao=finalizacao)
            self.list_cvs.append((finalizacao, situacao.casos_id))

    def read(self) -> str:
        """
        Lê o conteúdo do arquivo especificado no caminho.
        :return: Conteúdo do arquivo como string.
        """
        try:
            with self.path.open('r') as file:
                return file.read()
        except FileNotFoundError:
            return f"Arquivo {self.path} não encontrado."
        except IOError as e:
            return f"Erro ao ler o arquivo {self.path}: {e}"

    def write(self) -> None:
        """
        Escreve os dados analisados em um arquivo no caminho especificado.
        """
        try:
            with self.path.open('w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Nome do player', 'Tempo', 'Grupo', 'Peça UID', 'Peça Cor', 'Casos ID', 'Tipo'])

                for item, casos_id in self.list_cvs:
                    if isinstance(item, Jogada):
                        writer.writerow(
                            [item.id,
                             item.peca.jogador.nome,
                             item.tempo,
                             f"grupo: {item.grupo.peca_pai.uid} {item.grupo.criador.nome}" if item.grupo else "sem grupo",
                             item.peca.uid,
                             item.peca.cor,
                             casos_id,
                             'Jogada']
                        )
                    elif isinstance(item, Finalizacao):
                        writer.writerow(
                            ["N/A",  # ID not applicable for Finalizacao
                             item.jogador.nome,
                             item.tempo,
                             "N/A",  # Group not applicable for Finalizacao
                             "N/A",  # Piece UID not applicable for Finalizacao
                             "N/A",  # Piece Color not applicable for Finalizacao
                             casos_id,
                             item.descricao]
                        )
        except IOError as e:
            print(f"Erro ao escrever no arquivo {self.path}: {e}")
