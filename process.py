from datetime import timedelta

from entities.csv_export import CsvExport
from entities.finalizacao import Finalizacao
from entities.game import Game


class Process:
    def __init__(self, nome: str, host: str) -> None:
        self.csv_instance = None
        self.game = Game(name=nome, host=host)

    def process_data(self, move: dict) -> None:
        """
        Processa os dados da jogada, atualizando a lista de movimentos.

        :param move: Dicionário contendo os dados da jogada.
        """
        # Verifica se todas as chaves necessárias estão presentes
        required_keys = {"UID", "PosX", "PosY", "Tempo", "Jogador", "Cor"}
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

        # Atualiza a posição da peça
        peca.set_posicao_atual(pos_x=int(move["PosX"]), pos_y=int(move["PosY"]), jogador=jogador)

        # Adiciona a jogada no jogo
        self.game.add_jogada(peca=peca, tempo=timedelta(seconds=int(move["Tempo"])))

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

        return finalizacao

    def encerrar_jogo(self) -> None:
        """
        Encerra o jogo e exporta os dados.
        """
        if not self.game:
            raise ValueError("Jogo não iniciado")
        else:
            self.csv_instance = CsvExport(path='data.csv', game=self.game)

        self.csv_instance.analisar_game()
        self.csv_instance.write()

        print("Jogo encerrado. Dados exportados com sucesso.")
        print("Exportando arquivo CSV...")
        print("Arquivo exportado com sucesso.")
        print("Fim do jogo.")
