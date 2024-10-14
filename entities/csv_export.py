import zipfile
import logging
import pandas as pd
import shutil
import networkx as nx

import matplotlib
matplotlib.use('Agg')  # Adicione esta linha

from datetime import datetime, timedelta
from entities.finalizacao import Finalizacao
from entities.game import Game
from entities.jogada import Jogada
from typing import List, Dict, Union
from pathlib import Path
from util.situacoes import situacoes, operacoes  # Importando as descrições das situações

import plotly.graph_objects as go

class CsvExport:
    def __init__(self, path_root: Union[str, Path], game, nome: str) -> None:
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
        self.path_excel: Path = self.path_root / "excel"

        # Cria os diretórios se não existirem
        self._create_directories()

        # Caminho completo para o arquivo
        self.path_excel_complete: Path = self.path_excel / f"{self.nome}.xlsx"

        self.game: Game = game
        self.list_cvs: List = []
        self.caso_descricao: Dict[int, str] = situacoes  # Certifique-se de que 'situacoes' está definido em algum lugar

        logging.info(f"Csv object created with root path {self.path_root} and file name {self.nome}")

    def _create_directories(self) -> None:
        """
        Cria os diretórios necessários se não existirem.
        """
        directories = [self.path_excel]
        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                logging.info(f"Diretório {directory} criado com sucesso ou já existia.")
            except Exception as e:
                logging.error(f"Erro ao criar o diretório {directory}: {e}")
                raise

    def format_horario(self, dt: datetime) -> str:
        """
        Formata um objeto datetime para uma string no formato HH:MM:SS.

        :param dt: Objeto datetime a ser formatado.
        :return: String formatada no formato HH:MM:SS.
        """
        if not isinstance(dt, datetime):
            raise TypeError("O parâmetro dt deve ser uma instância de datetime.")

        try:
            return dt.strftime("%H:%M:%S")
        except Exception as e:
            raise ValueError(f"Erro ao formatar o datetime: {e}")

    def analisar_jogadas_game(self) -> None:
        """
        Analisa todas as jogadas feitas no game e atribui uma situacao para cada uma delas.
        """
        self.list_cvs.extend(self.game.situacoes)

    @staticmethod
    def format_timedelta_seconds(td: timedelta) -> str:
        if not isinstance(td, timedelta):
            raise TypeError("O parâmetro td deve ser uma instância de timedelta.")
        total_seconds = td.total_seconds()
        return f"{total_seconds:.2f}s"

    def export_to_excel(self, perguntas: List[str], respostas: List[str], jogadores: List[str],
                        tempo_resposta: List[str]) -> None:
        """
        Exporta os dados para um arquivo Excel, com cada tabela em uma planilha diferente.
        """
        # Criação dos DataFrames necessários
        # DataFrame 1: Jogadas do game
        game_data = []
        last_move_time = None
        for id_counter, (item, casos_id) in enumerate(self.list_cvs, start=1):
            if isinstance(item, Jogada):
                tempo_de_reacao = "N/A" if last_move_time is None else self.format_timedelta_seconds(
                    item.horario_da_jogada - last_move_time)
                game_data.append([
                    id_counter,
                    self.format_horario(item.horario_da_jogada),
                    item.peca.jogador.nome,
                    self.format_timedelta_seconds(item.tempo_desde_ultimo_movimento),
                    tempo_de_reacao,
                    self.format_timedelta_seconds(item.tempo),
                    f"grupo: {item.grupo.peca_pai.uid} {item.grupo.criador.nome}" if item.grupo else "sem grupo",
                    item.peca.uid,
                    item.peca.cor,
                    casos_id,
                    'Jogada',
                    item.fase
                ])
                last_move_time = item.horario_da_jogada
            elif isinstance(item, Finalizacao):
                game_data.append([
                    id_counter,
                    self.format_horario(item.horario_da_finalizacao),
                    item.jogador.nome,
                    "N/A",
                    "N/A",
                    self.format_timedelta_seconds(item.tempo),
                    "N/A",
                    "N/A",
                    "N/A",
                    casos_id,
                    'Finalizacao',
                    "N/A"
                ])

        game_df = pd.DataFrame(game_data, columns=[
            'ID', 'Horario da jogada', 'Nome do player', 'Tempo desde o último movimento do jogador',
            'Tempo de reação', 'Tempo de resposta', 'Grupo', 'Peça UID', 'Peça Cor', 'Casos ID',
            'Tipo da jogada', 'Fase da jogada'
        ])

        # DataFrame 2: Perguntas e Respostas
        perguntas_data = list(zip(perguntas, respostas, jogadores, tempo_resposta))
        perguntas_df = pd.DataFrame(perguntas_data, columns=['Pergunta', 'Resposta', 'Jogador', 'Tempo resposta'])

        # DataFrame 3: Clustered data (expandido)
        novas_linhas = []

        for _, row in game_df.iterrows():
            casos_id = row["Casos ID"]

            for caso_id in casos_id:
                descricao_caso = self.caso_descricao.get(caso_id, "Descrição não encontrada")
                operacoes_descricao = operacoes.get(caso_id, ["Operacao não encontrada"])

                # Cria uma linha para cada jogada com até 243 ações genéricas
                nova_linha = {
                    "ID": row["ID"],
                    "Nome do player": row["Nome do player"],
                    "Tempo de reação": row["Tempo de reação"],
                    "Tempo de resposta": row["Tempo de resposta"],
                    "Descrição do Caso": descricao_caso
                }

                # Preenche as colunas de 'Ação Genérica' (de 1 a 243)
                for i in range(243):
                    coluna = f"Operação {i + 1}"
                    nova_linha[coluna] = operacoes_descricao[i] if i < len(operacoes_descricao) else None

                novas_linhas.append(nova_linha)

        # Cria o DataFrame com as novas colunas
        df_expandido = pd.DataFrame(novas_linhas)

        # Salvando todos os DataFrames em um único arquivo Excel com várias planilhas
        with pd.ExcelWriter(self.path_excel_complete, engine='openpyxl') as writer:
            game_df.to_excel(writer, sheet_name='Jogadas do Game', index=False)
            perguntas_df.to_excel(writer, sheet_name='Perguntas e Respostas', index=False)
            df_expandido.to_excel(writer, sheet_name='Dados Clusterizados', index=False)

        print(f"Arquivo Excel salvo em '{self.path_excel_complete}'.")

    def gerar_grafo(self) -> None:
        """Gera um grafo interativo para cada jogador, representando as jogadas e as ações associadas."""
        # Lê o DataFrame modificado
        df_clusterizado = pd.read_excel(self.path_excel_complete, sheet_name='Dados Clusterizados')

        # Cria o diretório para salvar os grafos, caso necessário
        grafo_path_root = self.path_root / "grafo"
        grafo_path_root.mkdir(parents=True, exist_ok=True)

        jogadores = df_clusterizado["Nome do player"].unique()

        for jogador in jogadores:
            df_jogador = df_clusterizado[df_clusterizado["Nome do player"] == jogador]

            G = nx.DiGraph()  # Grafo direcionado

            jogadas = df_jogador["ID"].unique()
            previous_jogada = None

            for jogada_id in jogadas:
                jogada = f"Jogada {jogada_id}"
                G.add_node(jogada, label=jogada, color='blue')  # Cor azul para jogadas

                if previous_jogada:
                    G.add_edge(previous_jogada, jogada)

                df_jogada = df_jogador[df_jogador["ID"] == jogada_id]

                for _, row in df_jogada.iterrows():
                    caso_descricao = f"Caso {row['Descrição do Caso']}"
                    if caso_descricao not in G:
                        G.add_node(caso_descricao, label=caso_descricao, color='green')  # Verde para casos

                    G.add_edge(jogada, caso_descricao)

                    # Itera sobre as colunas de operações
                    for i in range(1, 244):
                        acao_coluna = f"Operação {i}"
                        operacao_descricao = row.get(acao_coluna)

                        if operacao_descricao and operacao_descricao not in G:
                            G.add_node(operacao_descricao, label=operacao_descricao,
                                       color='yellow')  # Amarelo para operações

                        if operacao_descricao:
                            G.add_edge(caso_descricao, operacao_descricao)

                    previous_jogada = jogada

            # Gerar as posições dos nós usando spring_layout
            pos = nx.spring_layout(G, seed=42)

            # Construir as coordenadas das arestas para o Plotly
            edge_x = []
            edge_y = []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=0.5, color='#888'),
                hoverinfo='none',
                mode='lines'
            )

            # Construir as coordenadas dos nós
            node_x = []
            node_y = []
            node_color = []
            node_text = []

            for node in G.nodes(data=True):
                x, y = pos[node[0]]
                node_x.append(x)
                node_y.append(y)
                node_color.append(node[1]['color'])  # A cor do nó
                node_text.append(node[1]['label'])  # O rótulo do nó

            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                marker=dict(
                    size=10,
                    color=node_color,
                    line=dict(width=2, color='black')
                ),
                text=node_text,
                hoverinfo='text'
            )

            # Criar a figura e adicionar os traços
            fig = go.Figure(data=[edge_trace, node_trace],
                            layout=go.Layout(
                                title=f"Grafo das Ações do Jogador: {jogador}",
                                titlefont_size=16,
                                showlegend=False,
                                hovermode='closest',
                                margin=dict(b=20, l=5, r=5, t=40),
                                xaxis=dict(showgrid=False, zeroline=False, visible=False),
                                yaxis=dict(showgrid=False, zeroline=False, visible=False)
                            ))

            # Opcional: salvar o grafo como um HTML
            grafo_path = grafo_path_root / f"{self.nome}_{jogador}.html"
            fig.write_html(str(grafo_path))
            print(f"Grafo salvo para o jogador '{jogador}' em '{grafo_path}'.")

        logging.info("Todos os grafos foram gerados e salvos com sucesso.")

    def zipar_partida(self) -> None:
        """
        Cria um arquivo ZIP contendo o Excel da partida e todos os grafos gerados para essa partida.
        """
        # Define o caminho para salvar o ZIP
        zip_path = self.path_root / f"{self.nome}.zip"
        zip_path.parent.mkdir(parents=True, exist_ok=True)  # Cria o diretório /partida se não existir

        # Caminho do Excel e dos grafos
        excel_path = self.path_excel_complete
        grafo_path_root = self.path_root / "grafo"
        grafo_files = list(grafo_path_root.glob(f"{self.nome}_*.png"))

        # Cria o arquivo ZIP e adiciona os arquivos
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(excel_path, excel_path.name)  # Adiciona o arquivo Excel
            for grafo_file in grafo_files:
                zipf.write(grafo_file, grafo_file.name)  # Adiciona cada grafo

        print(f"Arquivo ZIP salvo em '{zip_path}'.")

        # Remover as pastas 'grafo' e 'excel'
        self.remover_pastas()

    def remover_pastas(self) -> None:
        """
        Remove as pastas 'grafo' e 'excel' após o arquivo ZIP ser criado.
        """
        # Define os caminhos das pastas
        grafo_path = self.path_root / "grafo"
        excel_path = self.path_excel

        # Remove a pasta 'grafo' se ela existir
        if grafo_path.exists() and grafo_path.is_dir():
            shutil.rmtree(grafo_path)
            logging.info(f"Pasta '{grafo_path}' removida com sucesso.")

        # Remove a pasta 'excel' se ela existir
        if excel_path.exists() and excel_path.is_dir():
            shutil.rmtree(excel_path)
            logging.info(f"Pasta '{excel_path}' removida com sucesso.")