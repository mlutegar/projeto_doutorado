import unittest
from pathlib import Path

from process import Process


class TestGameFunctions(unittest.TestCase):

    def setUp(self):
        self.processo = Process("teste_iniciar", "novo_host")

    def teste(self):
        def gerar_grafo():
            """
            Gera um grafo com as jogadas feitas no game.
            """
            import pandas as pd
            import networkx as nx
            import matplotlib.pyplot as plt

            # Supondo que você tenha um arquivo CSV com os dados, vamos lê-lo diretamente
            file_path = 'data.csv'  # Substitua pelo caminho correto do seu arquivo CSV
            df = pd.read_csv(file_path)

            # Criar o grafo
            G = nx.DiGraph()

            # Adicionar nós e arestas ao grafo
            for i in range(len(df) - 1):
                # Vamos garantir que estamos considerando apenas transições entre diferentes ações
                if df['Ação Genérica'][i] != df['Ação Genérica'][i + 1]:
                    G.add_node(df['Descrição do Caso'][i], action=df['Ação Genérica'][i])
                    G.add_edge(df['Descrição do Caso'][i], df['Descrição do Caso'][i + 1])

            # Desenhar o grafo
            plt.figure(figsize=(12, 8))
            pos = nx.spring_layout(G, k=0.5)
            nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold',
                    edge_color='gray')
            plt.title("Grafo das Ações dos Jogadores")
            plt.show()

        gerar_grafo()

    def test_iniciar_jogo(self):
        self.assertEqual(self.processo.game.nome_da_sala, "teste_iniciar")
        self.assertEqual(self.processo.game.host, "novo_host")

    def test_process_data(self):
        move = {
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        }

        self.processo.process_data(move)

        self.assertIn(1, self.processo.game.pecas)
        self.assertIn("jogador1", self.processo.game.jogadores)
        self.assertEqual(self.processo.game.pecas[1].posicao, (1, 1))
        self.assertEqual(self.processo.game.pecas[1].jogador.nome, "jogador1")
        self.assertEqual(len(self.processo.game.jogadas), 1)

    def test_process_data_incomplete(self):
        move = {
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1"
            # "Cor" is missing
        }

        with self.assertRaises(ValueError):
            self.processo.process_data(move)

    def test_finalizar_jogo_desistiu(self):
        # Adiciona jogador para teste
        self.processo.process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        move = {"Jogador": "jogador1", "Acao": "Desistiu"}
        finalizacao = self.processo.finalizar_jogo(move)
        self.assertEqual(finalizacao.descricao, "Desistiu")
        self.assertEqual(finalizacao.jogador.nome, "jogador1")

    def test_finalizar_jogo_finalizou(self):
        # Adiciona jogador para teste
        self.processo.process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        move = {"Jogador": "jogador1", "Acao": "Finalizou"}
        finalizacao = self.processo.finalizar_jogo(move)
        self.assertEqual(finalizacao.descricao, "Finalizou")
        self.assertEqual(finalizacao.jogador.nome, "jogador1")

    def test_finalizar_jogo_invalid_action(self):
        self.processo.process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        move = {"Jogador": "jogador1", "Acao": "Invalid"}
        with self.assertRaises(ValueError):
            self.processo.finalizar_jogo(move)

    def test_finalizar_jogo_invalid_jogador(self):
        move = {"Jogador": "invalid_jogador", "Acao": "Desistiu"}
        with self.assertRaises(ValueError):
            self.processo.finalizar_jogo(move)

    def test_encerrar_jogo(self):
        # Adiciona jogadores e jogadas para teste
        self.processo.process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        self.processo.process_data({
            "UID": 2,
            "PosX": 211,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador2",
            "Cor": "azul"
        })
        self.processo.encerrar_jogo()
        self.assertTrue(Path('data.csv').is_file())

    def test_encerrar_jogo_no_data(self):
        self.processo.game = None  # Certifica que o jogo não foi iniciado
        with self.assertRaises(ValueError):
            self.processo.encerrar_jogo()


if __name__ == '__main__':
    unittest.main()
