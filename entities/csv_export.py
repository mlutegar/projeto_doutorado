import ast
import zipfile

import pandas as pd
import csv
import io

from datetime import datetime, timedelta
from entities.finalizacao import Finalizacao
from entities.game import Game
from entities.jogada import Jogada
from typing import List, Dict
from pathlib import Path
from util.situacoes import situacoes, acoes_genericas  # Importando as descrições das situações


class CsvExport:
    def __init__(self, path: str, game: Game) -> None:
        """
        Inicializa a classe Csv com o caminho do arquivo e o jogo.
        """
        self.path: Path = Path(path)
        self.game: Game = game
        self.list_cvs: List = []
        self.caso_descricao: Dict[int, str] = situacoes

    @staticmethod
    def format_horario(dt: datetime) -> str:
        return dt.strftime("%H:%M:%S")

    @staticmethod
    def format_timedelta_seconds(td: timedelta) -> str:
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
                    'Tempo de reação',  # Nova coluna
                    'Tempo de resposta',  # Renomeando 'Duração da jogada' para 'Tempo de resposta'
                    'Grupo',
                    'Peça UID',
                    'Peça Cor',
                    'Casos ID',
                    'Tipo da jogada'
                ])

                id_counter = 1
                last_move_time = None  # Variável para armazenar o tempo da última jogada de qualquer jogador
                for item, casos_id in self.list_cvs:
                    if isinstance(item, Jogada):
                        if last_move_time is None:
                            tempo_de_reacao = "N/A"
                        else:
                            tempo_de_reacao = self.format_timedelta_seconds(item.horario_da_jogada - last_move_time)

                        writer.writerow([
                            id_counter,
                            self.format_horario(item.horario_da_jogada),
                            item.peca.jogador.nome,
                            self.format_timedelta_seconds(item.tempo_desde_ultimo_movimento),
                            tempo_de_reacao,  # Tempo de reação
                            self.format_timedelta_seconds(item.tempo),  # Tempo de resposta (Duração da jogada)
                            f"grupo: "
                            f"{item.grupo.peca_pai.uid} "
                            f"{item.grupo.criador.nome}" if item.grupo else "sem grupo",
                            item.peca.uid,
                            item.peca.cor,
                            casos_id,
                            'Jogada'
                        ])
                        last_move_time = item.horario_da_jogada  # Atualiza o tempo da última jogada de qualquer jogador
                    elif isinstance(item, Finalizacao):
                        writer.writerow([
                            id_counter,
                            self.format_horario(item.horario_da_finalizacao),
                            item.jogador.nome,
                            "N/A",  # Tempo desde do último movimento do jogador not applicable for Finalizacao
                            "N/A",  # Tempo de reação not applicable for Finalizacao
                            self.format_timedelta_seconds(item.tempo),  # Tempo de resposta (Duração da jogada)
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
        Lê o CSV gerado e escreve os dados analisados em um arquivo clusteritzada no caminho especificado.
        """
        csv_path = self.path
        excel_path = self.path.with_suffix('.xlsx')
        zip_path = self.path.with_suffix('.zip')
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

                # Para cada caso ID, criar uma nova linha com a descrição do caso e as ações genéricas
                for caso_id in casos_id:
                    descricao_caso = descricoes_casos.get(caso_id, "Descrição não encontrada")
                    for acao_generica in acoes_genericas.get(caso_id, ["Ação genérica não encontrada"]):
                        nova_linha = {
                            "ID": row["ID"],
                            "Nome do player": row["Nome do player"],
                            "Descrição do Caso": descricao_caso,
                            "Ação Genérica": acao_generica
                        }
                        novas_linhas.append(nova_linha)

            # Criar um novo DataFrame com as novas linhas e colunas desejadas
            df_expandido = pd.DataFrame(novas_linhas,
                                        columns=["ID", "Nome do player", "Descrição do Caso", "Ação Genérica"])
            print(f"DataFrame expandido criado com sucesso. Número de linhas: {len(df_expandido)}")

            # Usar buffer de memória para escrever o arquivo Excel
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_expandido.to_excel(writer, index=False)

            # Escrever buffer no arquivo Excel
            with open(excel_path, 'wb') as f:
                f.write(buffer.getvalue())

            print(f"Arquivo Excel salvo em '{excel_path}'.")

            # Criar arquivo ZIP
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                zipf.write(excel_path, arcname=f'{self.path.stem}.xlsx')

            print(f"Arquivo ZIP salvo em '{zip_path}'.")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
