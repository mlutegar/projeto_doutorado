from entities.game import Game
from entities.jogada import Jogada
from entities.situacao import Situacao
from typing import List, Tuple
import csv
from pathlib import Path


class CsvExport:
    def __init__(self, path: str, game: Game) -> None:
        """
        Inicializa a classe Csv com o caminho do arquivo e o jogo.
        """
        self.path: Path = Path(path)
        self.game: Game = game
        self.list_cvs: List[Tuple[Jogada, List[int]]] = []

    def analisar_game(self) -> None:
        """
        Analisa todas as jogadas feitas no game e atribui uma situacao para cada uma delas.
        """
        for jogada in self.game.jogadas.values():
            situacao = Situacao(game=self.game, jogada=jogada)
            self.list_cvs.append((jogada, situacao.casos_id))

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
                writer.writerow(['ID', 'Nome do player', 'Tempo', 'Grupo', 'Peça UID',  'Peça Cor', 'Casos ID'])
                for jogada, casos_id in self.list_cvs:
                    writer.writerow(
                        [jogada.id,
                         jogada.peca.jogador.nome,
                         jogada.tempo,
                         "grupo: " + str(jogada.grupo.peca_pai.uid) + jogada.grupo.criador.nome if jogada.grupo else "sem grupo",
                         jogada.peca.uid,
                         jogada.peca.cor,
                         casos_id]
                    )
        except IOError as e:
            print(f"Erro ao escrever no arquivo {self.path}: {e}")
