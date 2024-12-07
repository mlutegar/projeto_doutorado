import re
from datetime import timedelta

from src.entities.csv_export import CsvExport
from src.entities.finalizacao import Finalizacao
from src.entities.game import Game
from src.entities.situacao import Situacao


class Process:

    def __init__(self, nome: str, host: str, tabuleiro: str) -> None:
        self.csv_instance = None
        self.game = Game(name=nome, host=host, tabuleiro=int(tabuleiro))

    def process_data(self, move: dict) -> set[int]:
        """
        Processa os dados da jogada, atualizando a lista de movimentos.

        :param move: Dicionário contendo os dados da jogada.
        """
        # Verifica se todas as chaves necessárias estão presentes
        required_keys = {
            "UID", "PosX", "PosY", "Tempo", "Jogador", "Cor", "Fase"
        }
        if not required_keys.issubset(move.keys()):
            raise ValueError("Dados incompletos recebidos")

        # Obtém ou adiciona a peça no jogo
        if move["UID"] not in self.game.pecas:
            peca = self.game.add_peca(uid=int(move["UID"]), cor=move["Cor"])
        else:
            peca = self.game.pecas[move["UID"]]

        # Obtém ou adiciona o jogador no jogo
        if move["Jogador"] not in self.game.jogadores:
            jogador = self.game.add_jogador(nome=move["Jogador"])
        else:
            jogador = self.game.jogadores[move["Jogador"]]

        if self.game.tabuleiro == 1:
            # Atualiza a posição da peça
            peca.set_posicao_atual_tabuleiro1(pos_x=int(move["PosX"]),
                                              pos_y=int(move["PosY"]),
                                              jogador=jogador)
        elif self.game.tabuleiro == 2:
            # Atualiza a posição da peça
            peca.set_posicao_atual_tabuleiro2(pos_x=int(move["PosX"]),
                                              pos_y=int(move["PosY"]),
                                              jogador=jogador)

        # Adiciona a jogada no jogo
        jogada = self.game.add_jogada(
            peca=peca,
            tempo=timedelta(seconds=float(move["Tempo"])),
            fase=move["Fase"])

        # Analisa a jogada imediatamente
        situacao = Situacao(game=self.game, jogada=jogada)
        self.game.registrar_situacao(jogada, situacao.casos_id)
        return situacao.casos_id

    def finalizar_jogo(self, move: dict) -> Finalizacao:
        """
        Jogador encerra a partida para ele.
        Move: {"Jogador": "nome_do_jogador", "Acao": "Desistiu"/"Finalizou"}
        """
        required_keys = {"Jogador", "Acao"}
        if not required_keys.issubset(move.keys()):
            raise ValueError("Dados incompletos recebidos")

        jogador_nome = move["Jogador"]
        acao = move["Acao"]

        if jogador_nome not in self.game.jogadores:
            raise ValueError(f"Jogador {jogador_nome} não encontrado no jogo")

        jogador = self.game.jogadores[jogador_nome]

        if acao == "Desistiu":
            finalizacao = self.game.desistir(player=jogador)
        elif acao == "Finalizou":
            finalizacao = self.game.finalizar(player=jogador)
        else:
            raise ValueError("Ação inválida. Use 'Desistiu' ou 'Finalizou'.")

        # Analisa a finalização imediatamente
        situacao = Situacao(game=self.game, finalizacao=finalizacao)
        self.game.registrar_situacao_finalizacao(finalizacao,
                                                 situacao.casos_id)

        return finalizacao

    def encerrar_jogo(self, perguntas, respostas, jogadores,
                      tempos_respostas) -> None:
        """
        Encerra o jogo e exporta os dados.
        """

        def corrigir_nome_sala(nome: str) -> str:
            """
            Corrige o nome da sala removendo ou substituindo caracteres inválidos.
            """
            # Substitui caracteres inválidos por underscore
            return re.sub(r'[:,]', '', nome).replace(' ',
                                                     '_').replace(':', '_')

        if not self.game:
            raise ValueError("Jogo não iniciado")
        else:
            nome_da_sala_corrigido = corrigir_nome_sala(self.game.nome_da_sala)
            self.csv_instance = CsvExport(path_root='data',
                                          game=self.game,
                                          nome=nome_da_sala_corrigido)

        # Exporta os dados para o arquivo Excel unificado
        self.csv_instance.analisar_jogadas_game()
        self.csv_instance.export_to_excel(perguntas, respostas, jogadores,
                                          tempos_respostas)

    def mudar_tabuleiro(self):
        """
        Muda o tabuleiro do jogo.
        """
        self.game.mudar_tabuleiro()
