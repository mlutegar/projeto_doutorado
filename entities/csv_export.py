import ast

import pandas as pd
import csv
import io

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
        Lê o CSV gerado e escreve os dados analisados em um arquivo clusterizado no caminho especificado.
        """
        csv_path = "data/Sat_20_Jul_2024_01_39_45_GMT.csv"
        excel_path = "data/Sat_20_Jul_2024_01_39_45_GMT_clusterizado.xlsx"
        descricoes_casos = situacoes

        try:
            # Verificar se o CSV existe e lê-lo
            try:
                df = pd.read_csv(csv_path)
                print(f"CSV lido com sucesso. Número de linhas: {len(df)}")
            except FileNotFoundError:
                print(f"Erro: O arquivo CSV '{csv_path}' não foi encontrado.")
                return
            except Exception as e:
                print(f"Erro ao ler o arquivo CSV: {e}")
                return
        
            # Lista para armazenar as novas linhas
            novas_linhas = []
        
            # Iterar sobre cada linha do DataFrame
            for index, row in df.iterrows():
                try:
                    casos_id = ast.literal_eval(row["Casos ID"])
                except Exception as e:
                    print(f"Erro ao analisar os casos ID na linha {index}: {e}")
                    continue
        
                # Para cada caso ID, criar uma nova linha com a descrição do caso
                for caso_id in casos_id:
                    nova_linha = row.copy()
                    nova_linha["Casos ID"] = caso_id
                    nova_linha["Descrição do Caso"] = descricoes_casos.get(caso_id, "Descrição não encontrada")
                    novas_linhas.append(nova_linha)
        
            # Criar um novo DataFrame com as novas linhas
            df_expandido = pd.DataFrame(novas_linhas)
            print(f"DataFrame expandido criado com sucesso. Número de linhas: {len(df_expandido)}")
        
            # Usar buffer de memória para escrever o arquivo Excel
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_expandido.to_excel(writer, index=False)
        
            # Escrever buffer no arquivo Excel
            with open(excel_path, 'wb') as f:
                f.write(buffer.getvalue())
        
            print(f"Arquivo Excel salvo em '{excel_path}'.")
        
        except Exception as e:
            print(f"Ocorreu um erro: {e}")