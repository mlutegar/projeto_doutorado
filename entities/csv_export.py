import re
import logging
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from entities.finalizacao import Finalizacao
from entities.game import Game
from entities.jogada import Jogada
from typing import List, Dict, Union
from pathlib import Path
from util.situacoes import situacoes, acoes_genericas  # Importando as descrições das situações


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
            try:
                # Certifique-se de que casos_id é um conjunto de inteiros
                casos_id = row["Casos ID"]
                if not isinstance(casos_id, set):
                    raise TypeError(f"Esperado um conjunto, mas obteve {type(casos_id)}")
            except Exception as e:
                print(f"Erro ao analisar os casos ID na linha {row['ID']}: {e}")
                continue

            for caso_id in casos_id:
                descricao_caso = self.caso_descricao.get(caso_id, "Descrição não encontrada")
                acoes = acoes_genericas.get(caso_id, ["Ação genérica não encontrada"])
                if not acoes:  # Verifica se ações genéricas estão vazias
                    continue

                for acao_generica in acoes:
                    nova_linha = {
                        "ID": row["ID"],
                        "Nome do player": row["Nome do player"],
                        "Tempo de reação": row["Tempo de reação"],
                        "Tempo de resposta": row["Tempo de resposta"],
                        "Descrição do Caso": descricao_caso,
                        "Ação Genérica": acao_generica
                    }
                    novas_linhas.append(nova_linha)

        df_expandido = pd.DataFrame(novas_linhas, columns=[
            "ID", "Nome do player", "Tempo de reação", "Tempo de resposta", "Descrição do Caso", "Ação Genérica"
        ])


        # Salvando todos os DataFrames em um único arquivo Excel com várias planilhas
        with pd.ExcelWriter(self.path_excel_complete, engine='openpyxl') as writer:
            game_df.to_excel(writer, sheet_name='Jogadas do Game', index=False)
            perguntas_df.to_excel(writer, sheet_name='Perguntas e Respostas', index=False)
            df_expandido.to_excel(writer, sheet_name='Dados Clusterizados', index=False)

        print(f"Arquivo Excel salvo em '{self.path_excel_complete}'.")

    def gerar_grafo(self) -> None:
        """
        Gera um grafo para cada jogador, representando as jogadas e os casos e ações associados.
        """
        # Lendo o DataFrame expandido gerado anteriormente
        df_expandido = pd.read_excel(self.path_excel_complete, sheet_name='Dados Clusterizados')

        # Criando o diretório para salvar os grafos, caso não exista
        grafo_path_root = self.path_root / "grafo"
        grafo_path_root.mkdir(parents=True, exist_ok=True)

        # Agrupando os dados por jogador
        jogadores = df_expandido["Nome do player"].unique()
        data_atual = datetime.now().strftime("%a_%d_%b_%Y_%H%M%S_GMT")  # Formato da data para o nome do arquivo

        for jogador in jogadores:
            df_jogador = df_expandido[df_expandido["Nome do player"] == jogador]

            # Criando o grafo direcionado
            G = nx.DiGraph()

            # Adicionando nós e arestas ao grafo para o jogador atual
            jogadas = df_jogador["ID"].unique()
            previous_jogada = None

            # Dicionário para armazenar cores dos nós
            color_map = []

            for jogada_id in jogadas:
                jogada = f"Jogada {jogada_id}"
                G.add_node(jogada, label=jogada)
                color_map.append('blue')  # Cor azul para jogadas

                # Conecta a jogada atual com a jogada anterior
                if previous_jogada:
                    G.add_edge(previous_jogada, jogada)

                # Filtrando os dados para a jogada atual
                df_jogada = df_jogador[df_jogador["ID"] == jogada_id]

                for _, row in df_jogada.iterrows():
                    # Adiciona o nó do caso ID e a conexão com a jogada
                    caso_descricao = f"Caso {row['Descrição do Caso']}"
                    if caso_descricao not in G:
                        G.add_node(caso_descricao, label=caso_descricao)
                        color_map.append('green')  # Cor verde para casos ID
                    G.add_edge(jogada, caso_descricao)

                    # Adiciona o nó da ação genérica e a conexão com o caso ID
                    acao_generica = row["Ação Genérica"]
                    if acao_generica not in G:
                        G.add_node(acao_generica, label=acao_generica)
                        color_map.append('yellow')  # Cor amarela para ações genéricas
                    G.add_edge(caso_descricao, acao_generica)

                # Atualiza a jogada anterior
                previous_jogada = jogada

            # Plotando e salvando o grafo
            plt.figure(figsize=(14, 10))  # Ajuste o tamanho para melhorar a visualização
            pos = nx.spring_layout(G, seed=42, k=0.5)  # Ajuste do layout com parâmetro `k` para controlar a distância entre os nós
            nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_size=1000,
                    node_color=color_map, font_size=8, font_weight='bold', edge_color='gray', arrows=True, width=0.8)
            plt.title(f"Grafo das Ações do Jogador: {jogador}")

            # Salvando a imagem no diretório especificado
            grafo_path = grafo_path_root / f"{data_atual}_{jogador}.png"
            plt.savefig(grafo_path, dpi=300)  # Salvando com maior resolução
            plt.close()

            print(f"Grafo salvo para o jogador '{jogador}' em '{grafo_path}'.")

        logging.info("Todos os grafos foram gerados e salvos com sucesso.")