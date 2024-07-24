import pandas as pd
import csv

from datetime import datetime, timedelta
from entities.finalizacao import Finalizacao
from entities.game import Game
from entities.jogada import Jogada
from typing import List, Dict
from pathlib import Path
from util.situacoes import situacoes  # Importando as descrições das situações


class CsvExport:
    def __init__(self, path: str, game: Game) -> None:
        """
        Inicializa a classe Csv com o caminho do arquivo e o jogo.
        """
        self.path: Path = Path(path)
        self.game: Game = game
        self.list_cvs: List = []
        self.caso_descricao: Dict[int, str] = situacoes

    def format_horario(self, dt: datetime) -> str:
        return dt.strftime("%H:%M:%S")

    def format_timedelta_seconds(self, td: timedelta) -> str:
        total_seconds = td.total_seconds()
        return f"{total_seconds:.2f}s"

    def analisar_game(self) -> None:
        """
        Analisa todas as jogadas feitas no game e atribui uma situacao para cada uma delas.
        """
        self.list_cvs.extend(self.game.situacoes)

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
                writer.writerow([
                    'ID',
                    'Horario da jogada',
                    'Nome do player',
                    'Tempo desde do último movimento do jogador',
                    'Duração da jogada',
                    'Grupo',
                    'Peça UID',
                    'Peça Cor',
                    'Casos ID',
                    'Tipo da jogada'
                ])

                id_counter = 1
                for item, casos_id in self.list_cvs:
                    if isinstance(item, Jogada):
                        writer.writerow([
                            id_counter,
                            self.format_horario(item.horario_da_jogada),
                            item.peca.jogador.nome,
                            self.format_timedelta_seconds(item.tempo_desde_ultimo_movimento),
                            self.format_timedelta_seconds(item.tempo),
                            f"grupo: {item.grupo.peca_pai.uid} {item.grupo.criador.nome}" if item.grupo else "sem grupo",
                            item.peca.uid,
                            item.peca.cor,
                            casos_id,
                            'Jogada'
                        ])
                    elif isinstance(item, Finalizacao):
                        writer.writerow([
                            id_counter,
                            self.format_horario(item.horario_da_finalizacao),
                            item.jogador.nome,
                            "N/A",  # Tempo desde do último movimento do jogador not applicable for Finalizacao
                            self.format_timedelta_seconds(item.tempo),
                            "N/A",  # Group not applicable for Finalizacao
                            "N/A",  # Piece UID not applicable for Finalizacao
                            "N/A",  # Piece Color not applicable for Finalizacao
                            casos_id,
                            'Finalizacao'
                        ])
                    id_counter += 1
        except IOError as e:
            print(f"Erro ao escrever no arquivo {self.path}: {e}")

    def write_clustered(self) -> None:
        """
        Escreve os dados analisados em um arquivo clusterizado no caminho especificado.
        """
        try:
            data = {
                'ID': [],
                'Nome do player': [],
                'Casos ID': [],
                'Descrição caso': []
            }

            id_counter = 1
            for item, casos_id in self.list_cvs:
                if isinstance(item, Jogada) or isinstance(item, Finalizacao):
                    for caso_id in casos_id:
                        data['ID'].append(id_counter)
                        data['Nome do player'].append(
                            item.peca.jogador.nome if isinstance(item, Jogada) else item.jogador.nome)
                        data['Casos ID'].append(f'Caso {caso_id}')
                        data['Descrição caso'].append(self.caso_descricao.get(caso_id, 'Descrição não encontrada'))
                    id_counter += 1

            # Debug print to check the data dictionary
            print("Data dictionary:", data)

            df = pd.DataFrame(data)

            # Debug print to check the DataFrame
            print("DataFrame head:", df.head())

            # Debug print to check the DataFrame info
            print("DataFrame info:", df.info())

            df.to_excel(self.path.with_suffix('.xlsx'), index=False, engine='openpyxl')
            print(f"Arquivo {self.path.with_suffix('.xlsx')} escrito com sucesso.")
        except Exception as e:
            print(f"Erro ao escrever no arquivo {self.path.with_suffix('.xlsx')}: {e}")
