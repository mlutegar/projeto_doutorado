import ast
import logging
import pandas as pd

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
                casos_id = ast.literal_eval(row["Casos ID"])
            except Exception as e:
                print(f"Erro ao analisar os casos ID na linha {row['ID']}: {e}")
                continue

            for caso_id in casos_id:
                descricao_caso = self.caso_descricao.get(caso_id, "Descrição não encontrada")
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

        df_expandido = pd.DataFrame(novas_linhas, columns=[
            "ID", "Nome do player", "Tempo de reação", "Tempo de resposta", "Descrição do Caso", "Ação Genérica"
        ])

        # Salvando todos os DataFrames em um único arquivo Excel com várias planilhas
        with pd.ExcelWriter(self.path_excel_complete, engine='openpyxl') as writer:
            game_df.to_excel(writer, sheet_name='Jogadas do Game', index=False)
            perguntas_df.to_excel(writer, sheet_name='Perguntas e Respostas', index=False)
            df_expandido.to_excel(writer, sheet_name='Dados Clusterizados', index=False)

        print(f"Arquivo Excel salvo em '{self.path_excel_complete}'.")
