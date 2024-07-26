import ast
import logging
import zipfile

import pandas as pd
import csv
import io

from datetime import datetime, timedelta
from entities.finalizacao import Finalizacao
from entities.game import Game
from entities.jogada import Jogada
from typing import List, Dict, Union
from pathlib import Path
from util.situacoes import situacoes, acoes_genericas  # Importando as descrições das situações


class CsvExport:
    def __init__(self, path_root: Union[str, Path], game: 'Game', nome: str) -> None:
        """
        Inicializa a classe Csv com o caminho do arquivo e o jogo.

        :param path_root: Caminho raiz dos arquivos.
        :param game: Instância do jogo.
        :param nome: Nome do arquivo.
        """
        if not isinstance(path_root, (str, Path)):
            raise TypeError("path_root deve ser uma string ou uma instância de Path.")
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string.")

        self.nome: str = nome
        self.path_root: Path = Path(path_root) if isinstance(path_root, str) else path_root
        self.path_csv: Path = self.path_root / "csv"
        self.path_excel: Path = self.path_root / "excel"
        self.path_zip: Path = self.path_root / "zip"

        # Cria os diretórios se não existirem
        self._create_directories()

        # Caminhos completos para os arquivos
        self.path_csv_complete: Path = self.path_csv / f"{self.nome}.csv"
        self.path_excel_complete: Path = self.path_excel / f"{self.nome}.xlsx"
        self.path_zip_complete: Path = self.path_zip / f"{self.nome}.zip"

        self.game: Game = game
        self.list_cvs: List = []
        self.caso_descricao: Dict[int, str] = situacoes  # Certifique-se de que 'situacoes' está definido em algum lugar

        logging.info(f"Csv object created with root path {self.path_root} and file name {self.nome}")

    def _create_directories(self) -> None:
        """
        Cria os diretórios necessários se não existirem.
        """
        directories = [self.path_csv, self.path_excel, self.path_zip]
        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                logging.info(f"Diretório {directory} criado com sucesso ou já existia.")
            except Exception as e:
                logging.error(f"Erro ao criar o diretório {directory}: {e}")
                raise

    @staticmethod
    def format_horario(dt: datetime) -> str:
        """
        Formata um objeto datetime para uma string no formato HH:MM:SS.

        :param dt: Objeto datetime a ser formatado.
        :return: String formatada no formato HH:MM:SS.
        :raises TypeError: Se o parâmetro não for uma instância de datetime.
        """
        if not isinstance(dt, datetime):
            raise TypeError("O parâmetro dt deve ser uma instância de datetime.")

        try:
            return dt.strftime("%H:%M:%S")
        except Exception as e:
            raise ValueError(f"Erro ao formatar o datetime: {e}")

    @staticmethod
    def format_timedelta_seconds(td: timedelta) -> str:
        total_seconds = td.total_seconds()
        return f"{total_seconds:.2f}s"

    def analisar_game(self) -> None:
        """
        Analisa todas as jogadas feitas no game e atribui uma situacao para cada uma delas.
        """
        self.list_cvs.extend(self.game.situacoes)

    def write_csv(self) -> None:
        """
        Escreve os dados analisados em um arquivo CSV no caminho especificado.
        """
        try:
            with self.path_csv_complete.open('w', newline='') as file:
                writer = csv.writer(file)
                self._write_csv_header(writer)
                self._write_csv_rows(writer)
        except IOError as e:
            print(f"Erro ao escrever no arquivo {self.path_csv_complete}: {e}")

    @staticmethod
    def _write_csv_header(writer) -> None:
        """
        Escreve o cabeçalho do arquivo CSV.
        """
        writer.writerow([
            'ID',
            'Horario da jogada',
            'Nome do player',
            'Tempo desde o último movimento do jogador',
            'Tempo de reação',  # Nova coluna
            'Tempo de resposta',  # Renomeando 'Duração da jogada' para 'Tempo de resposta'
            'Grupo',
            'Peça UID',
            'Peça Cor',
            'Casos ID',
            'Tipo da jogada'
        ])

    def _write_csv_rows(self, writer) -> None:
        """
        Escreve as linhas de dados no arquivo CSV.
        """
        id_counter = 1
        last_move_time = None  # Variável para armazenar o tempo da última jogada de qualquer jogador
        for item, casos_id in self.list_cvs:
            if isinstance(item, Jogada):
                self._write_jogada_row(writer, id_counter, item, casos_id, last_move_time)
                last_move_time = item.horario_da_jogada  # Atualiza o tempo da última jogada de qualquer jogador
            elif isinstance(item, Finalizacao):
                self._write_finalizacao_row(writer, id_counter, item, casos_id)
            id_counter += 1

    def _write_jogada_row(self, writer, id_counter: int, item: 'Jogada', casos_id: int, last_move_time) -> None:
        """
        Escreve uma linha de dados de uma jogada no arquivo CSV.
        """
        tempo_de_reacao = "N/A" if last_move_time is None else self.format_timedelta_seconds(item.horario_da_jogada - last_move_time)

        writer.writerow([
            id_counter,
            self.format_horario(item.horario_da_jogada),
            item.peca.jogador.nome,
            self.format_timedelta_seconds(item.tempo_desde_ultimo_movimento),
            tempo_de_reacao,  # Tempo de reação
            self.format_timedelta_seconds(item.tempo),  # Tempo de resposta (Duração da jogada)
            f"grupo: {item.grupo.peca_pai.uid} {item.grupo.criador.nome}" if item.grupo else "sem grupo",
            item.peca.uid,
            item.peca.cor,
            casos_id,
            'Jogada'
        ])

    def _write_finalizacao_row(self, writer, id_counter: int, item: 'Finalizacao', casos_id: int) -> None:
        """
        Escreve uma linha de dados de finalização no arquivo CSV.
        """
        writer.writerow([
            id_counter,
            self.format_horario(item.horario_da_finalizacao),
            item.jogador.nome,
            "N/A",  # Tempo desde do último movimento do jogador não aplicável para Finalizacao
            "N/A",  # Tempo de reação não aplicável para Finalizacao
            self.format_timedelta_seconds(item.tempo),  # Tempo de resposta (Duração da jogada)
            "N/A",  # Grupo não aplicável para Finalizacao
            "N/A",  # UID da peça não aplicável para Finalizacao
            "N/A",  # Cor da peça não aplicável para Finalizacao
            casos_id,
            'Finalizacao'
        ])

    def write_clustered(self) -> None:
        """
        Lê o CSV gerado e escreve os dados analisados em um arquivo clusteritzada no caminho especificado.
        """
        csv_path = self.path_csv_complete
        excel_path = self.path_excel_complete
        zip_path = self.path_zip_complete
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
                            "Tempo de reação": row["Tempo de reação"],
                            "Tempo de resposta": row["Tempo de resposta"],
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
                zipf.write(excel_path, arcname=f'{self.nome}.xlsx')

            print(f"Arquivo ZIP salvo em '{zip_path}'.")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    # def gerar_grafo(self):
    #     """
    #     Gera um grafo com as jogadas feitas no game.
    #     """
    #     import pandas as pd
    #     import networkx as nx
    #     import matplotlib.pyplot as plt
    #
    #     # Supondo que você tenha um DataFrame com a sua tabela
    #     data = {
    #         'ID': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4,
    #                4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5],
    #         'Nome do player': ['As'] * 49,
    #         'Descrição do Caso': ['Pegou a peça e largou em algum lugar Aleatório'] * 7 +
    #                              ['Realizou uma ação rápida, menos de 3 segundos'] * 4 +
    #                              ['Fez, sozinho, um agrupamento com 2 peças'] * 2 +
    #                              [
    #                                  'Criou um agrupamento contendo peças iguais e diferentes. Exemplo: Duas amarelas e duas pretas'] * 5 +
    #                              ['Pegou a peça e largou em algum lugar Aleatório'] * 7 +
    #                              ['Realizou uma ação rápida, menos de 3 segundos'] * 2 +
    #                              ['Pegou a peça e largou em algum lugar Aleatório'] * 7 +
    #                              ['Realizou uma ação rápida, menos de 3 segundos'] * 2 +
    #                              ['Finalizou sozinho'] * 5 +
    #                              ['Finalizou sozinho com pouco tempo de jogo'] * 3,
    #         'Ação Genérica': ['Executa Tarefas Simples', 'Não se Envolve / Evita Envolvimento',
    #                           'Ignora Contribuições Alheias', 'Evita Participar', 'Desconsidera o Grupo',
    #                           'Contribui Esporadicamente', 'Desmotiva o Grupo', 'Define Metas Claras',
    #                           'Executa Tarefas Simples', 'Define Metas Claras', 'Executa Tarefas Simples',
    #                           'Não se Envolve', 'Monitora e Avalia Progresso', 'Planeja Estratégicamente',
    #                           'Define Visão de Longo Prazo', 'Desempenha Funções Variadas',
    #                           'Monitora e Avalia Progresso', 'Define Metas Claras', 'Executa Tarefas Simples',
    #                           'Não se Envolve / Evita Envolvimento', 'Ignora Contribuições Alheias', 'Evita Participar',
    #                           'Desconsidera o Grupo', 'Contribui Esporadicamente', 'Desmotiva o Grupo',
    #                           'Define Metas Claras', 'Executa Tarefas Simples', 'Executa Tarefas Simples',
    #                           'Não se Envolve / Evita Envolvimento', 'Ignora Contribuições Alheias', 'Evita Participar',
    #                           'Desconsidera o Grupo', 'Contribui Esporadicamente', 'Desmotiva o Grupo',
    #                           'Define Metas Claras', 'Executa Tarefas Simples', 'Desconsidera o Grupo',
    #                           'Centraliza Decisões', 'Prioriza Interesses Próprios', 'Monitora e Avalia Progresso',
    #                           'Desmotiva o Grupo', 'Monitora e Avalia Progresso', 'Centraliza Decisões',
    #                           'Prioriza Interesses Próprios']
    #     }
    #
    #     df = pd.DataFrame(data)
    #
    #     # Criar o grafo
    #     G = nx.DiGraph()
    #
    #     # Adicionar nós e arestas ao grafo
    #     for i in range(len(df) - 1):
    #         G.add_node(df['Descrição do Caso'][i], action=df['Ação Genérica'][i])
    #         G.add_edge(df['Descrição do Caso'][i], df['Descrição do Caso'][i + 1])
    #
    #     # Desenhar o grafo
    #     plt.figure(figsize=(12, 8))
    #     pos = nx.spring_layout(G, k=0.5)
    #     nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold',
    #             edge_color='gray')
    #     plt.title("Grafo das Ações dos Jogadores")
    #     plt.show()