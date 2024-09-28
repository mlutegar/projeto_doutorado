import re
from datetime import timedelta

from entities.csv_export import CsvExport
from entities.finalizacao import Finalizacao
from entities.game import Game
from entities.situacao import Situacao


class Process:
    def __init__(self, nome: str, host: str, tabuleiro: str) -> None:
        self.csv_instance = None
        self.game = Game(name=nome, host=host, tabuleiro=int(tabuleiro))

    def process_data(self, move: dict) -> None:
        """
        Processa os dados da jogada, atualizando a lista de movimentos.

        :param move: Dicionário contendo os dados da jogada.
        """
        print("Iniciando process_data com move:", move)

        # Verifica se todas as chaves necessárias estão presentes
        required_keys = {"UID", "PosX", "PosY", "Tempo", "Jogador", "Cor", "Fase"}
        if not required_keys.issubset(move.keys()):
            raise ValueError("Dados incompletos recebidos")
        print("Todas as chaves necessárias estão presentes.")

        # Obtém ou adiciona a peça no jogo
        if move["UID"] not in self.game.pecas:
            peca = self.game.add_peca(uid=int(move["UID"]), cor=move["Cor"])
            print(f"Peça {move['UID']} adicionada ao jogo com cor {move['Cor']}.")
        else:
            peca = self.game.pecas[move["UID"]]
            print(f"Peça {move['UID']} já existe no jogo.")

        # Obtém ou adiciona o jogador no jogo
        if move["Jogador"] not in self.game.jogadores:
            jogador = self.game.add_jogador(nome=move["Jogador"])
            print(f"Jogador {move['Jogador']} adicionado ao jogo.")
        else:
            jogador = self.game.jogadores[move["Jogador"]]
            print(f"Jogador {move['Jogador']} já existe no jogo.")

        if self.game.tabuleiro == 1:
            # Atualiza a posição da peça
            peca.set_posicao_atual_tabuleiro1(pos_x=int(move["PosX"]), pos_y=int(move["PosY"]), jogador=jogador)
            print(f"Peça {peca.uid} movida para posição ({peca.linha}, {peca.coluna}) pelo jogador {jogador.nome}.")
        elif self.game.tabuleiro == 2:
            # Atualiza a posição da peça
            peca.set_posicao_atual_tabuleiro2(pos_x=int(move["PosX"]), pos_y=int(move["PosY"]), jogador=jogador)
            print(f"Peça {peca.uid} movida para posição ({peca.linha}, {peca.coluna}) pelo jogador {jogador.nome}.")

        # Adiciona a jogada no jogo
        jogada = self.game.add_jogada(peca=peca, tempo=timedelta(seconds=float(move["Tempo"])), fase=move["Fase"])

        # Analisa a jogada imediatamente
        situacao = Situacao(game=self.game, jogada=jogada)
        self.game.registrar_situacao(jogada, situacao.casos_id)

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
        self.game.registrar_situacao_finalizacao(finalizacao, situacao.casos_id)

        return finalizacao

    def encerrar_jogo(self) -> None:
        """
        Encerra o jogo e exporta os dados.
        """
        def corrigir_nome_sala(nome: str) -> str:
            """
            Corrige o nome da sala removendo ou substituindo caracteres inválidos.
            """
            # Substitui caracteres inválidos por underscore
            return re.sub(r'[:,]', '', nome).replace(' ', '_').replace(':', '_')

        if not self.game:
            raise ValueError("Jogo não iniciado")
        else:
            nome_da_sala_corrigido = corrigir_nome_sala(self.game.nome_da_sala)
            self.csv_instance = CsvExport(path_root='data', game=self.game, nome=nome_da_sala_corrigido)

        self.csv_instance.analisar_jogadas_game()
        self.csv_instance.write_csv_game()
        self.csv_instance.write_clustered()  # Nova função para gerar o arquivo clusterizado

        print("Jogo encerrado. Dados exportados com sucesso.")
        print("Exportando arquivo CSV...")
        print("Arquivo exportado com sucesso.")
        print("Fim do jogo.")

    def mudar_tabuleiro(self):
        """
        Muda o tabuleiro do jogo.
        """
        self.game.mudar_tabuleiro()
        print("Tabuleiro mudado com sucesso.")
        print("Tabuleiro atual:", self.game.tabuleiro)
        print("Fim da mudança de tabuleiro.")
