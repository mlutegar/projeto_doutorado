import unittest

from datetime import timedelta
from src.entities.game import Game
from src.entities.situacao import Situacao


class TestSituacao(unittest.TestCase):

    def setUp(self):
        self.game = Game(name="teste", host="host")

    def test_definir_situacao_caso1(self):
        """
        1: "Pegou a peça e largou em algum lugar Aleatório",
        """
        move = {
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        }

        process_data(move)

        jogada = self.game.jogadas[1]  # Assumindo que esta é a primeira jogada

        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(1, situacao.casos_id)

    def test_definir_situacao_caso2(self):
        """
        2: "Fez, sozinho, um agrupamento com 2 peças",
        """
        move1 = {
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        }

        move2 = {
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        }

        process_data(move1)
        process_data(move2)

        jogada = self.game.jogadas[2]  # Assumindo que esta é a segunda jogada

        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(2, situacao.casos_id)

    def test_definir_situacao_caso3(self):
        """
        3: "Fez, sozinho, um agrupamento com 3 a 6 peças",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 3,
            "PosX": 239,
            "PosY": 74,
            "Tempo": 15,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        jogada = self.game.jogadas[3]  # Assumindo que esta é a terceira jogada

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(3, situacao.casos_id)

    def test_definir_situacao_caso4(self):
        """
        4: "Fez, sozinho, um agrupamento com mais de 6 peças",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 3,
            "PosX": 239,
            "PosY": 74,
            "Tempo": 15,
            "Jogador": "jogador1",
            "Cor": "verde"
        })
        process_data({
            "UID": 4,
            "PosX": 316,
            "PosY": 74,
            "Tempo": 20,
            "Jogador": "jogador1",
            "Cor": "verde"
        })
        process_data({
            "UID": 5,
            "PosX": 393,
            "PosY": 74,
            "Tempo": 25,
            "Jogador": "jogador1",
            "Cor": "azul"
        })
        process_data({
            "UID": 6,
            "PosX": 123,
            "PosY": 143,
            "Tempo": 30,
            "Jogador": "jogador1",
            "Cor": "azul"
        })
        process_data({
            "UID": 7,
            "PosX": 200,
            "PosY": 143,
            "Tempo": 35,
            "Jogador": "jogador1",
            "Cor": "amarela"
        })

        jogada = self.game.jogadas[7]  # Assumindo que esta é a sétima jogada

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(4, situacao.casos_id)

    def test_definir_situacao_caso5(self):
        """
        5: "Adicionou uma peça no agrupamento de outro integrante, fez várias vezes",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        # Primeira infracao
        process_data({
            "UID": 3,
            "PosX": 239,
            "PosY": 74,
            "Tempo": 15,
            "Jogador": "jogador2",
            "Cor": "verde"
        })

        process_data({
            "UID": 4,
            "PosX": 86,
            "PosY": 284,
            "Tempo": 20,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        process_data({
            "UID": 5,
            "PosX": 163,
            "PosY": 284,
            "Tempo": 25,
            "Jogador": "jogador1",
            "Cor": "azul"
        })

        # Segunda infracao
        process_data({
            "UID": 6,
            "PosX": 239,
            "PosY": 284,
            "Tempo": 30,
            "Jogador": "jogador2",
            "Cor": "azul"
        })

        # Terceira infracao
        process_data({
            "UID": 7,
            "PosX": 123,
            "PosY": 143,
            "Tempo": 40,
            "Jogador": "jogador2",
            "Cor": "amarela"
        })

        jogada = self.game.jogadas[7]  # Assumindo que esta é a sétima jogada

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(5, situacao.casos_id)

    def test_definir_situacao_caso6(self):
        """
        6: "Adicionou uma peça no agrupamento de outro integrante, faz somente uma vez num período curto",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 3,
            "PosX": 239,
            "PosY": 74,
            "Tempo": 15,
            "Jogador": "jogador2",
            "Cor": "verde"
        })

        jogada1 = self.game.jogadas[3]  # Adiciona peça no agrupamento de outro integrante (jogador2)

        situacao1 = Situacao(jogada=jogada1, game=self.game)

        # Jogada qualquer do jogador 1
        process_data({
            "UID": 4,
            "PosX": 1350,
            "PosY": 912,
            "Tempo": 20,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        jogada2 = self.game.jogadas[4]

        situacao2 = Situacao(jogada=jogada2, game=self.game)

        print(situacao2.casos_id)
        self.assertIn(6, situacao2.casos_id)

    def test_definir_situacao_caso7(self):
        """
        7: "Segurou uma peça por mais de 6 segundos por exemplo",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 7,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        jogada = self.game.jogadas[1]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(7, situacao.casos_id)

    def test_definir_situacao_caso8(self):
        """
        8: "Colocou uma peça no tabuleiro de forma aleatória ou no próprio agrupamento e depois colocou a mesma peça
        no agrupamento do outro",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        # Jogador 1 coloca em um lugar aleatório
        process_data({
            "UID": 3,
            "PosX": 1350,
            "PosY": 912,
            "Tempo": 15,
            "Jogador": "jogador2",
            "Cor": "verde"
        })

        # depois coloca a mesma peça no agrupamento do outro
        process_data({
            "UID": 3,
            "PosX": 239,
            "PosY": 74,
            "Tempo": 20,
            "Jogador": "jogador2",
            "Cor": "verde"
        })

        jogada = self.game.jogadas[4]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(8, situacao.casos_id)

    def test_registrar_caso9(self):
        """
        9: "Realizou uma ação rápida, menos de 3 segundos",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 2,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        jogada = self.game.jogadas[1]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(9, situacao.casos_id)

    def test_registrar_caso10(self):
        """
        10: "Adicionou uma peça no agrupamento do outro, que a remove, mas continua a repetir a ação",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })

        # Jogador 1 adiciona peça no agrupamento do Jogador 2
        process_data({
            "UID": 3,
            "PosX": 239,
            "PosY": 74,
            "Tempo": 15,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        # Jogador 2 remove a peça do agrupamento
        process_data({
            "UID": 3,
            "PosX": 506,
            "PosY": 284,
            "Tempo": 20,
            "Jogador": "jogador2",
            "Cor": "verde"
        })

        # Jogador 1 adiciona novamente a peça no agrupamento do Jogador 2
        process_data({
            "UID": 3,
            "PosX": 239,
            "PosY": 74,
            "Tempo": 25,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        jogada = self.game.jogadas[5]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(10, situacao.casos_id)

    def test_registrar_caso11(self):
        """
        11: "Agrupou peças de cor igual",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        jogada = self.game.jogadas[2]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(11, situacao.casos_id)

    def test_registrar_caso12(self):
        """
        12: "Criou um agrupamento contendo peças iguais e diferentes. Exemplo: Duas amarelas e duas pretas",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 3,
            "PosX": 239,
            "PosY": 74,
            "Tempo": 15,
            "Jogador": "jogador1",
            "Cor": "verde"
        })
        process_data({
            "UID": 4,
            "PosX": 316,
            "PosY": 74,
            "Tempo": 20,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        jogada = self.game.jogadas[4]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(12, situacao.casos_id)

    def test_registrar_caso13(self):
        """
        13: "Agrupou peças de cores diferentes",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 3,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "verde"
        })
        process_data({
            "UID": 5,
            "PosX": 239,
            "PosY": 74,
            "Tempo": 15,
            "Jogador": "jogador1",
            "Cor": "azul"
        })

        jogada = self.game.jogadas[3]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(13, situacao.casos_id)

    def test_registrar_caso14(self):
        """
        14: "Retirou peças do Agrupamento do outro integrante e devolveu para o monte",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })

        # Jogador 1 retira a peça do agrupamento do Jogador 2 e a devolve para o monte
        process_data({
            "UID": 1,
            "PosX": 1500,
            "PosY": 150,
            "Tempo": 15,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        jogada = self.game.jogadas[3]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(14, situacao.casos_id)

    def test_registrar_caso15(self):
        """
        15: "Retirou peças do Agrupamento do outro integrante e colocou no seu próprio agrupamento",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })

        # Jogador 1 agrupa duas peças
        process_data({
            "UID": 3,
            "PosX": 200,
            "PosY": 284,
            "Tempo": 15,
            "Jogador": "jogador1",
            "Cor": "verde"
        })
        process_data({
            "UID": 4,
            "PosX": 239,
            "PosY": 284,
            "Tempo": 20,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        # Jogador 1 retira a peça do agrupamento do Jogador 2 e a coloca no seu próprio agrupamento
        process_data({
            "UID": 1,
            "PosX": 276,
            "PosY": 284,
            "Tempo": 25,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        jogada = self.game.jogadas[5]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(15, situacao.casos_id)

    def test_registrar_caso16(self):
        """
        16: "Retirou peças do Agrupamento do outro integrante e colocou em um lugar aleatório",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })

        # Jogador 1 agrupa duas peças
        process_data({
            "UID": 3,
            "PosX": 200,
            "PosY": 150,
            "Tempo": 15,
            "Jogador": "jogador1",
            "Cor": "verde"
        })
        process_data({
            "UID": 4,
            "PosX": 239,
            "PosY": 150,
            "Tempo": 20,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        # Jogador 1 retira a peça do agrupamento do Jogador 2 e a coloca em um lugar aleatório
        process_data({
            "UID": 1,
            "PosX": 1270,
            "PosY": 424,
            "Tempo": 25,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        jogada = self.game.jogadas[5]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(16, situacao.casos_id)

    def test_registrar_caso17(self):
        """
        17: "Trocou a posição da própria peça",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        # Jogador 1 troca a posição da mesma peça
        process_data({
            "UID": 1,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        jogada = self.game.jogadas[2]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(17, situacao.casos_id)

    def test_registrar_caso18(self):
        """
        18: "Retirou peças do próprio Agrupamento e devolveu para o monte",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        # Jogador 1 retira uma peça do próprio agrupamento e a devolve para o monte
        process_data({
            "UID": 1,
            "PosX": 1500,
            "PosY": 150,
            "Tempo": 15,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        jogada = self.game.jogadas[3]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(18, situacao.casos_id)

    def test_registrar_caso19(self):
        """
        19: "Retirou peças do próprio agrupamento e colocou em algum lugar aleatório",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        # Jogador 1 retira uma peça do próprio agrupamento e a coloca em um lugar aleatório
        process_data({
            "UID": 1,
            "PosX": 400,
            "PosY": 300,
            "Tempo": 15,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        jogada = self.game.jogadas[3]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(19, situacao.casos_id)

    def test_registrar_caso20(self):
        """
        20: "Retirou peças dos outros integrantes que adicionaram no agrupamento feito por ele",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        # Jogador 2 adiciona uma peça no agrupamento do Jogador 1
        process_data({
            "UID": 3,
            "PosX": 239,
            "PosY": 74,
            "Tempo": 15,
            "Jogador": "jogador2",
            "Cor": "verde"
        })

        # Jogador 1 retira a peça adicionada pelo Jogador 2
        process_data({
            "UID": 3,
            "PosX": 1350,
            "PosY": 912,
            "Tempo": 20,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        jogada = self.game.jogadas[4]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(20, situacao.casos_id)

    def test_registrar_caso21(self):
        """
        21: "Criou mais de um agrupamento",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        # Jogador 1 cria o segundo agrupamento
        process_data({
            "UID": 3,
            "PosX": 239,
            "PosY": 150,
            "Tempo": 15,
            "Jogador": "jogador1",
            "Cor": "verde"
        })
        process_data({
            "UID": 4,
            "PosX": 316,
            "PosY": 150,
            "Tempo": 20,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        jogada = self.game.jogadas[4]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(21, situacao.casos_id)

    def test_registrar_caso22(self):
        """
        22: "Conecta dois ou mais agrupamentos com outros participantes",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        # Jogador 2 cria o segundo agrupamento
        process_data({
            "UID": 3,
            "PosX": 86,
            "PosY": 211,
            "Tempo": 15,
            "Jogador": "jogador2",
            "Cor": "verde"
        })
        process_data({
            "UID": 4,
            "PosX": 163,
            "PosY": 211,
            "Tempo": 20,
            "Jogador": "jogador2",
            "Cor": "verde"
        })

        # Jogador 1 conecta os agrupamentos
        process_data({
            "UID": 5,
            "PosX": 123,
            "PosY": 143,
            "Tempo": 25,
            "Jogador": "jogador1",
            "Cor": "azul"
        })

        jogada = self.game.jogadas[5]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(22, situacao.casos_id)

    def test_registrar_caso23(self):
        """
        23: "Conecta dois ou mais agrupamentos consigo mesmo",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        # Jogador 1 cria o segundo agrupamento
        process_data({
            "UID": 3,
            "PosX": 86,
            "PosY": 211,
            "Tempo": 15,
            "Jogador": "jogador1",
            "Cor": "verde"
        })
        process_data({
            "UID": 4,
            "PosX": 163,
            "PosY": 211,
            "Tempo": 20,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        # Jogador 1 conecta os agrupamentos
        process_data({
            "UID": 5,
            "PosX": 123 ,
            "PosY": 143,
            "Tempo": 25,
            "Jogador": "jogador1",
            "Cor": "azul"
        })

        jogada = self.game.jogadas[5]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(23, situacao.casos_id)

    def test_registrar_caso24(self):
        """
        24: "Forma um agrupamento de 2 peças com outro integrante",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador2",
            "Cor": "verde"
        })

        jogada = self.game.jogadas[2]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(24, situacao.casos_id)

    def test_registrar_caso25(self):
        """
        25: "Forma um agrupamento de 3 a 6 peças com outro integrante",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 3,
            "PosX": 239,
            "PosY": 74,
            "Tempo": 15,
            "Jogador": "jogador2",
            "Cor": "verde"
        })

        jogada = self.game.jogadas[3]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(25, situacao.casos_id)

    def test_registrar_caso26(self):
        """
        26: "Forma um agrupamento de mais de 6 peças com outro integrante",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 3,
            "PosX": 239,
            "PosY": 74,
            "Tempo": 15,
            "Jogador": "jogador2",
            "Cor": "verde"
        })
        process_data({
            "UID": 4,
            "PosX": 316,
            "PosY": 74,
            "Tempo": 20,
            "Jogador": "jogador2",
            "Cor": "verde"
        })
        process_data({
            "UID": 5,
            "PosX": 393,
            "PosY": 74,
            "Tempo": 25,
            "Jogador": "jogador1",
            "Cor": "azul"
        })
        process_data({
            "UID": 6,
            "PosX": 470,
            "PosY": 74,
            "Tempo": 30,
            "Jogador": "jogador2",
            "Cor": "azul"
        })
        process_data({
            "UID": 7,
            "PosX": 547,
            "PosY": 74,
            "Tempo": 35,
            "Jogador": "jogador1",
            "Cor": "amarela"
        })

        jogada = self.game.jogadas[7]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(26, situacao.casos_id)

    def test_registrar_caso27(self):
        """
        27: "Desenvolveu um agrupamento e outro integrante resolveu adicionar peças",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        # Jogador 2 adiciona uma peça no agrupamento do Jogador 1
        process_data({
            "UID": 3,
            "PosX": 239,
            "PosY": 74,
            "Tempo": 15,
            "Jogador": "jogador2",
            "Cor": "verde"
        })

        jogada1 = self.game.jogadas[3]

        Situacao(jogada=jogada1, game=self.game)

        # Jogada qualquer do Jogador 1
        process_data({
            "UID": 4,
            "PosX": 316,
            "PosY": 74,
            "Tempo": 20,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        jogada2 = self.game.jogadas[4]

        situacao = Situacao(jogada=jogada2, game=self.game)

        print(situacao.casos_id)
        self.assertIn(27, situacao.casos_id)

    def test_registrar_caso28(self):
        """
        28: "Desistiu Sozinho",
        """
        # Jogador 1 faz uma jogada qualquer
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        move = {"Jogador": "jogador1", "Acao": "Desistiu"}
        finalizacao = finalizar_jogo(move)
        situacao = Situacao(game=self.game, finalizacao=finalizacao)
        self.assertIn(28, situacao.casos_id)

    def test_registrar_caso29(self):
        """
        29: "Desistiu Sozinho com pouco tempo de jogo",
        """
        # Jogador 1 faz uma jogada qualquer
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        move = {"Jogador": "jogador1", "Acao": "Desistiu"}
        finalizacao = finalizar_jogo(move)
        situacao = Situacao(game=self.game, finalizacao=finalizacao)
        self.assertIn(29, situacao.casos_id)

    def test_registrar_caso30(self):
        """
        30: "Desistiu Sozinho e pouco tempo depois outro integrante desistiu",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })

        self.game.jogadores["jogador1"].tempo_em_jogo = timedelta(seconds=200)
        move1 = {"Jogador": "jogador1", "Acao": "Desistiu"}
        move2 = {"Jogador": "jogador2", "Acao": "Desistiu"}

        finalizar_jogo(move1)
        finalizar_jogo(move2)

        encerrar_jogo(self.game)

        situacao = Situacao(game=self.game)
        self.assertIn(30, situacao.casos_id)

    def test_registrar_caso31(self):
        """
        31: "Desistiu depois de outro integrante Desistir",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })

        move1 = {"Jogador": "jogador2", "Acao": "Desistiu"}
        move2 = {"Jogador": "jogador1", "Acao": "Desistiu"}

        finalizar_jogo(move1)
        finalizacao = finalizar_jogo(move2)

        situacao = Situacao(game=self.game, finalizacao=finalizacao)
        self.assertIn(31, situacao.casos_id)

    def test_registrar_caso32(self):
        """
        32: "Finalizou sozinho",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        move = {"Jogador": "jogador1", "Acao": "Finalizou"}
        finalizacao = finalizar_jogo(move)
        situacao = Situacao(game=self.game, finalizacao=finalizacao)
        self.assertIn(32, situacao.casos_id)

    def test_registrar_caso33(self):
        """
        33: "Finalizou sozinho com pouco tempo de jogo",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        self.game.jogadores["jogador1"].tempo_em_jogo = timedelta(seconds=250)
        move = {"Jogador": "jogador1", "Acao": "Finalizou"}
        finalizacao = finalizar_jogo(move)
        situacao = Situacao(game=self.game, finalizacao=finalizacao)
        self.assertIn(33, situacao.casos_id)

    def test_registrar_caso34(self):
        """
        34: "Finalizou depois de outro integrante Finalizar",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })

        move1 = {"Jogador": "jogador2", "Acao": "Finalizou"}
        move2 = {"Jogador": "jogador1", "Acao": "Finalizou"}

        finalizar_jogo(move1)
        finalizacao = finalizar_jogo(move2)

        situacao = Situacao(game=self.game,finalizacao=finalizacao)
        self.assertIn(34, situacao.casos_id)

    def test_registrar_caso35(self):
        """
        35: "Finalizou Sozinho e pouco tempo depois outro integrante finalizou também",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })

        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })

        self.game.jogadores["jogador1"].tempo_em_jogo = timedelta(seconds=200)

        move1 = {"Jogador": "jogador1", "Acao": "Finalizou"}
        move2 = {"Jogador": "jogador2", "Acao": "Finalizou"}

        finalizar_jogo(move1)
        finalizar_jogo(move2)

        encerrar_jogo(self.game)

        situacao = Situacao(game=self.game)
        self.assertIn(35, situacao.casos_id)

    def test_registrar_caso36(self):
        """
        36: "Imitou a forma do mesmo agrupamento do outro (fez depois que outro integrante realizou a ação)",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        # Jogador 2 imita a forma do agrupamento do Jogador 1
        process_data({
            "UID": 3,
            "PosX": 86,
            "PosY": 150,
            "Tempo": 15,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 4,
            "PosX": 163,
            "PosY": 150,
            "Tempo": 20,
            "Jogador": "jogador2",
            "Cor": "verde"
        })

        jogada = self.game.jogadas[4]

        situacao = Situacao(jogada=jogada, game=self.game)

        print(situacao.casos_id)
        self.assertIn(36, situacao.casos_id)

    def test_registrar_caso37(self):
        """
        37: "É imitado por alguém",
        """
        process_data({
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 2,
            "PosX": 163,
            "PosY": 74,
            "Tempo": 10,
            "Jogador": "jogador1",
            "Cor": "verde"
        })

        # Jogador 2 imita a forma do agrupamento do Jogador 1 com duas peças verdes
        process_data({
            "UID": 3,
            "PosX": 86,
            "PosY": 150,
            "Tempo": 15,
            "Jogador": "jogador2",
            "Cor": "vermelha"
        })
        process_data({
            "UID": 4,
            "PosX": 163,
            "PosY": 150,
            "Tempo": 20,
            "Jogador": "jogador2",
            "Cor": "verde"
        })

        for jogada in self.game.jogadas.values():
            situacao = Situacao(jogada=jogada, game=self.game)
            if 37 in situacao.casos_id:
                break

        self.assertIn(37, situacao.casos_id)

    def test_registrar_caso38(self):
        """
        38: "Não realizou ações"
        """
        situacao = Situacao(game=self.game)
        self.assertIn(38, situacao.casos_id)


if __name__ == '__main__':
    unittest.main()
