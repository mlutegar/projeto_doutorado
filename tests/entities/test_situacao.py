import unittest
from datetime import timedelta

from entities.finalizacao import Finalizacao
from entities.game import Game
from entities.situacao import Situacao


class TestSituacao(unittest.TestCase):

    def setUp(self):
        self.game = Game("teste", "host")
        self.jogador1 = self.game.add_jogador("jogador1")
        self.jogador2 = self.game.add_jogador("jogador2")
        self.jogador3 = self.game.add_jogador("jogador3")
        self.jogador4 = self.game.add_jogador("jogador4")
        self.jogador5 = self.game.add_jogador("jogador5")
        self.peca1 = self.game.add_peca(uid=1, cor="vermelha")
        self.peca2 = self.game.add_peca(uid=2, cor="vermelha")
        self.peca3 = self.game.add_peca(uid=3, cor="verde")
        self.peca4 = self.game.add_peca(uid=4, cor="verde")
        self.peca5 = self.game.add_peca(uid=5, cor="azul")
        self.peca6 = self.game.add_peca(uid=6, cor="azul")
        self.peca7 = self.game.add_peca(uid=7, cor="amarela")

    def test_definir_situacao_caso1(self):
        """
        1: "Pegou a peça e largou em algum lugar Aleatório",
        """
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )

        situacao = Situacao(
            jogada=self.game.add_jogada(
                peca=self.peca1,
                tempo=timedelta(seconds=5)
            ),
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(1, situacao.casos_id)

    def test_definir_situacao_caso2(self):
        """
        2: "Fez, sozinho, um agrupamento com 2 peças",
        """
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )
        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador1
        )

        situacao = Situacao(
            jogada=self.game.add_jogada(
                peca=self.peca2,
                tempo=timedelta(seconds=10)
            ),
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(2, situacao.casos_id)

    def test_definir_situacao_caso3(self):
        """
        3: "Fez, sozinho, um agrupamento com 3 a 6 peças",
        """
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )
        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )
        self.peca3.set_posicao_atual(
            pos_x=239, pos_y=74, jogador=self.jogador1
        )

        situacao = Situacao(
            jogada=self.game.add_jogada(
                peca=self.peca3,
                tempo=timedelta(seconds=15)
            ),
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(3, situacao.casos_id)

    def test_definir_situacao_caso4(self):
        """
        4: "Fez, sozinho, um agrupamento com mais de 6 peças",
        """
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )
        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )
        self.peca3.set_posicao_atual(
            pos_x=239, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=15)
        )
        self.peca4.set_posicao_atual(
            pos_x=316, pos_y=74, jogador=self.jogador1
        )

        self.game.add_jogada(
            peca=self.peca4, tempo=timedelta(seconds=20)
        )

        self.peca5.set_posicao_atual(
            pos_x=393, pos_y=74, jogador=self.jogador1
        )

        self.game.add_jogada(
            peca=self.peca5, tempo=timedelta(seconds=25)
        )

        self.peca6.set_posicao_atual(
            pos_x=123, pos_y=143, jogador=self.jogador1
        )

        self.game.add_jogada(
            peca=self.peca6, tempo=timedelta(seconds=30)
        )

        self.peca7.set_posicao_atual(
            pos_x=200, pos_y=143, jogador=self.jogador1
        )

        situacao = Situacao(
            jogada=self.game.add_jogada(
                peca=self.peca7,
                tempo=timedelta(seconds=35)
            ),
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(4, situacao.casos_id)

    def test_definir_situacao_caso5(self):
        """
        5: "Adicionou uma peça no agrupamento de outro integrante, fez várias vezes",
        """
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )
        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )

        # Primeira infracao
        self.peca3.set_posicao_atual(
            pos_x=239, pos_y=74, jogador=self.jogador2
        )
        self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=15)
        )

        self.peca4.set_posicao_atual(
            pos_x=86, pos_y=284, jogador=self.jogador1
        )

        self.game.add_jogada(
            peca=self.peca4, tempo=timedelta(seconds=20)
        )

        self.peca5.set_posicao_atual(
            pos_x=163, pos_y=284, jogador=self.jogador1
        )

        self.game.add_jogada(
            peca=self.peca5, tempo=timedelta(seconds=25)
        )

        # Segunda infracao
        self.peca6.set_posicao_atual(
            pos_x=239, pos_y=284, jogador=self.jogador2
        )

        self.game.add_jogada(
            peca=self.peca6, tempo=timedelta(seconds=30)
        )

        # Terceira infracao
        self.peca7.set_posicao_atual(
            pos_x=123, pos_y=143, jogador=self.jogador2
        )

        situacao = Situacao(
            jogada=self.game.add_jogada(
                peca=self.peca7,
                tempo=timedelta(seconds=40)
            ),
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(5, situacao.casos_id)

    def test_definir_situacao_caso6(self):
        """
        6: "Adicionou uma peça no agrupamento de outro integrante, faz somente uma vez num período curto",
        """
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )

        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador1
        )

        self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )

        # Adiciona peça no agrupamento de outro integrante (jogador2)
        self.peca3.set_posicao_atual(
            pos_x=239, pos_y=74, jogador=self.jogador2
        )
        jogada1 = self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=10)
        )

        Situacao(
            jogada=jogada1,
            game=self.game
        )

        # jogada qualquer do jogador 2
        self.peca4.set_posicao_atual(
            pos_x=1350, pos_y=912, jogador=self.jogador1
        )

        jogada = self.game.add_jogada(
            peca=self.peca4, tempo=timedelta(seconds=15)
        )

        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(6, situacao.casos_id)

    def test_definir_situacao_caso7(self):
        """
        7: "Segurou uma peça por mais de 6 segundos por exemplo",
        """
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        jogada = self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=7)  # segurando a peça por mais de 6 segundos
        )

        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(7, situacao.casos_id)

    def test_definir_situacao_caso8(self):
        """
        8: "Colocou uma peça no tabuleiro de forma aleatória ou no próprio agrupamento e depois colocou a mesma peça
        no agrupamento do outro",
        """
        # Um outro jogador fez um agrupamento
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )

        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador1
        )

        self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )

        # Jogador 1 coloca em um lugar aleatório
        self.peca3.set_posicao_atual(
            pos_x=1350, pos_y=912, jogador=self.jogador2
        )
        self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=15)
        )

        # depois coloca a mesma peça no agrupamento do outro
        self.peca3.set_posicao_atual(
            pos_x=239, pos_y=74, jogador=self.jogador2
        )

        jogada = self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=20)
        )

        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(8, situacao.casos_id)

    def test_registrar_caso9(self):
        """
        9: "Realizou uma ação rápida, menos de 3 segundos",
        """
        # Colocando a peça no tabuleiro com menos de 3 segundos
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        jogada = self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=2)  # ação rápida
        )

        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(9, situacao.casos_id)

# PAREI AQUI
    def test_registrar_caso10(self):
        """
        10: "Adicionou uma peça no agrupamento do outro, que a remove, mas continua a repetir a ação",
        """
        # Jogador 2 monta um agrupamento inicial
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador2
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )

        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador2
        )
        self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )

        # Jogador 1 adiciona peça no agrupamento do Jogador 2
        self.peca3.set_posicao_atual(
            pos_x=239, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=15)
        )

        # Jogador 2 remove a peça do agrupamento
        self.peca3.set_posicao_atual(
            pos_x=506, pos_y=284, jogador=self.jogador2
        )
        self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=20)
        )

        # Jogador 1 adiciona novamente a peça no agrupamento do Jogador 2
        self.peca3.set_posicao_atual(
            pos_x=239, pos_y=74, jogador=self.jogador1
        )
        jogada = self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=25)
        )

        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(10, situacao.casos_id)

    def test_registrar_caso11(self):
        """
        11: "Agrupou peças de cor igual",
        """
        # Jogador 1 agrupa duas peças vermelhas
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )

        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador1
        )
        jogada = self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )

        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(11, situacao.casos_id)

    def test_registrar_caso12(self):
        """
        12: "Criou um agrupamento contendo peças iguais e diferentes. Exemplo: Duas amarelas e duas pretas",
        """
        # Jogador 1 agrupa duas peças verdes e duas peças vermelhas
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )

        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )

        self.peca3.set_posicao_atual(
            pos_x=239, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=15)
        )

        self.peca4.set_posicao_atual(
            pos_x=316, pos_y=74, jogador=self.jogador1
        )
        jogada = self.game.add_jogada(
            peca=self.peca4, tempo=timedelta(seconds=20)
        )

        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(12, situacao.casos_id)

    def test_registrar_caso13(self):
        """
        13: "Agrupou peças de cores diferentes",
        """
        # Jogador 1 agrupa uma peça vermelha, uma verde e uma azul
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )

        self.peca3.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=10)
        )

        self.peca5.set_posicao_atual(
            pos_x=239, pos_y=74, jogador=self.jogador1
        )
        jogada = self.game.add_jogada(
            peca=self.peca5, tempo=timedelta(seconds=15)
        )

        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(13, situacao.casos_id)

    def test_registrar_caso14(self):
        """
        14: "Retirou peças do Agrupamento do outro integrante e devolveu para o monte",
        """
        # Jogador 2 agrupa duas peças
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador2
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )

        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador2
        )
        self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )

        # Jogador 1 retira a peça do agrupamento do Jogador 2 e a devolve para o monte
        self.peca1.set_posicao_atual(
            pos_x=1500, pos_y=150, jogador=self.jogador1  # Colocando a peça no monte
        )
        jogada = self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=15)
        )

        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(14, situacao.casos_id)

    def test_registrar_caso15(self):
        """
        15: "Retirou peças do Agrupamento do outro integrante e colocou no seu próprio agrupamento",
        """
        # Jogador 2 agrupa duas peças
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador2
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )

        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador2
        )
        self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )

        # Jogador 1 agrupa duas peças
        self.peca3.set_posicao_atual(
            pos_x=200, pos_y=284, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=15)
        )

        self.peca4.set_posicao_atual(
            pos_x=239, pos_y=284, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca4, tempo=timedelta(seconds=20)
        )

        # Jogador 1 retira a peça do agrupamento do Jogador 2 e a coloca no seu próprio agrupamento
        self.peca1.set_posicao_atual(
            pos_x=276, pos_y=284, jogador=self.jogador1
        )
        jogada = self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=25)
        )

        # Verifica se a situação 15 foi registrada corretamente
        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(15, situacao.casos_id)

    def test_registrar_caso16(self):
        """
        16: "Retirou peças do Agrupamento do outro integrante e colocou em um lugar aleatório",
        """
        # Jogador 2 agrupa duas peças
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador2
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )

        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador2
        )
        self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )

        # Jogador 1 agrupa duas peças
        self.peca3.set_posicao_atual(
            pos_x=200, pos_y=150, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=15)
        )

        self.peca4.set_posicao_atual(
            pos_x=239, pos_y=150, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca4, tempo=timedelta(seconds=20)
        )

        # Jogador 1 retira a peça do agrupamento do Jogador 2 e a coloca em um lugar aleatório
        self.peca1.set_posicao_atual(
            pos_x=1270, pos_y=424, jogador=self.jogador1  # Colocando a peça em um lugar aleatório
        )
        jogada = self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=25)
        )

        # Verifica se a situação 16 foi registrada corretamente
        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(16, situacao.casos_id)

    def test_registrar_caso17(self):
        """
        17: "Trocou a posição da própria peça",
        """
        # Jogador 1 coloca a peça em uma posição inicial
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )

        # Jogador 1 troca a posição da mesma peça
        self.peca1.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador1
        )
        jogada = self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=10)
        )

        # Verifica se a situação 17 foi registrada corretamente
        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(17, situacao.casos_id)

    def test_registrar_caso18(self):
        """
        18: "Retirou peças do próprio Agrupamento e devolveu para o monte",
        """
        # Jogador 1 agrupa duas peças
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )

        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )

        # Jogador 1 retira uma peça do próprio agrupamento e a devolve para o monte
        self.peca1.set_posicao_atual(
            pos_x=1500, pos_y=150, jogador=self.jogador1  # Colocando a peça no monte
        )
        jogada = self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=15)
        )

        # Verifica se a situação 18 foi registrada corretamente
        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(18, situacao.casos_id)

    def test_registrar_caso19(self):
        """
        19: "Retirou peças do próprio agrupamento e colocou em algum lugar aleatório",
        """
        # Jogador 1 agrupa duas peças
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )

        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )

        # Jogador 1 retira uma peça do próprio agrupamento e a coloca em um lugar aleatório
        self.peca1.set_posicao_atual(
            pos_x=400, pos_y=300, jogador=self.jogador1  # Colocando a peça em um lugar aleatório
        )
        jogada = self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=15)
        )

        # Verifica se a situação 19 foi registrada corretamente
        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        print(situacao.casos_id)
        self.assertIn(19, situacao.casos_id)

    def test_registrar_caso20(self):
        """
        20: "Retirou peças dos outros integrantes que adicionaram no agrupamento feito por ele",
        """
        # Jogador 1 cria um agrupamento com duas peças
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca1, tempo=timedelta(seconds=5)
        )

        self.peca2.set_posicao_atual(
            pos_x=163, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca2, tempo=timedelta(seconds=10)
        )

        # Jogador 2 adiciona uma peça no agrupamento do Jogador 1
        self.peca3.set_posicao_atual(
            pos_x=239, pos_y=74, jogador=self.jogador2
        )
        self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=15)
        )

        # Jogador 1 retira a peça adicionada pelo Jogador 2
        self.peca3.set_posicao_atual(
            pos_x=1350, pos_y=912, jogador=self.jogador1  # Colocando a peça no monte
        )
        jogada = self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=20)
        )

        # Verifica se a situação 20 foi registrada corretamente
        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        self.assertIn(20, situacao.casos_id)

    def test_registrar_caso21(self):
        """
        21: "Criou mais de um agrupamento",
        """
        # Jogador 1 cria o primeiro agrupamento
        self.peca1.set_posicao_atual(pos_x=86, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca1, tempo=timedelta(seconds=5))
        self.peca2.set_posicao_atual(pos_x=163, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca2, tempo=timedelta(seconds=10))

        # Jogador 1 cria o segundo agrupamento
        self.peca3.set_posicao_atual(pos_x=239, pos_y=150, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca3, tempo=timedelta(seconds=15))
        self.peca4.set_posicao_atual(pos_x=316, pos_y=150, jogador=self.jogador1)
        jogada = self.game.add_jogada(peca=self.peca4, tempo=timedelta(seconds=20))

        # Verifica se a situação 21 foi registrada corretamente
        situacao = Situacao(jogada=jogada, game=self.game)
        self.assertIn(21, situacao.casos_id)

    def test_registrar_caso22(self):
        """
        22: "Conecta dois ou mais agrupamentos com outros participantes",
        """
        # Jogador 1 cria o primeiro agrupamento
        self.peca1.set_posicao_atual(pos_x=86, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca1, tempo=timedelta(seconds=5))
        self.peca2.set_posicao_atual(pos_x=163, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca2, tempo=timedelta(seconds=10))

        # Jogador 2 cria o segundo agrupamento
        self.peca3.set_posicao_atual(pos_x=86, pos_y=211, jogador=self.jogador2)
        self.game.add_jogada(peca=self.peca3, tempo=timedelta(seconds=15))
        self.peca4.set_posicao_atual(pos_x=163, pos_y=211, jogador=self.jogador2)
        self.game.add_jogada(peca=self.peca4, tempo=timedelta(seconds=20))

        # Jogador 1 conecta os agrupamentos
        self.peca5.set_posicao_atual(pos_x=123, pos_y=143, jogador=self.jogador1)
        jogada = self.game.add_jogada(peca=self.peca5, tempo=timedelta(seconds=25))

        # Verifica se a situação 22 foi registrada corretamente
        situacao = Situacao(jogada=jogada, game=self.game)
        self.assertIn(22, situacao.casos_id)

    def test_registrar_caso23(self):
        """
        23: "Conecta dois ou mais agrupamentos consigo mesmo",
        """
        # Jogador 1 cria o primeiro agrupamento
        self.peca1.set_posicao_atual(pos_x=86, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca1, tempo=timedelta(seconds=5))
        self.peca2.set_posicao_atual(pos_x=163, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca2, tempo=timedelta(seconds=10))

        # Jogador 1 cria o segundo agrupamento
        self.peca3.set_posicao_atual(pos_x=86, pos_y=211, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca3, tempo=timedelta(seconds=15))
        self.peca4.set_posicao_atual(pos_x=163, pos_y=211, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca4, tempo=timedelta(seconds=20))

        # Jogador 1 conecta os agrupamentos
        self.peca5.set_posicao_atual(pos_x=123, pos_y=143, jogador=self.jogador1)
        jogada = self.game.add_jogada(peca=self.peca5, tempo=timedelta(seconds=25))

        # Verifica se a situação 23 foi registrada corretamente
        situacao = Situacao(jogada=jogada, game=self.game)
        self.assertIn(23, situacao.casos_id)

    def test_registrar_caso24(self):
        """
        24: "Forma um agrupamento de 2 peças com outro integrante",
        """
        # Jogador 1 e Jogador 2 formam um agrupamento juntos
        self.peca1.set_posicao_atual(pos_x=86, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca1, tempo=timedelta(seconds=5))
        self.peca2.set_posicao_atual(pos_x=163, pos_y=74, jogador=self.jogador2)
        jogada = self.game.add_jogada(peca=self.peca2, tempo=timedelta(seconds=10))

        # Verifica se a situação 24 foi registrada corretamente
        situacao = Situacao(jogada=jogada, game=self.game)
        self.assertIn(24, situacao.casos_id)

    def test_registrar_caso25(self):
        """
        25: "Forma um agrupamento de 3 a 6 peças com outro integrante",
        """
        # Jogador 1 e Jogador 2 formam um agrupamento juntos de 3 peças
        self.peca1.set_posicao_atual(pos_x=86, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca1, tempo=timedelta(seconds=5))
        self.peca2.set_posicao_atual(pos_x=163, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca2, tempo=timedelta(seconds=10))
        self.peca3.set_posicao_atual(pos_x=239, pos_y=74, jogador=self.jogador2)
        jogada = self.game.add_jogada(peca=self.peca3, tempo=timedelta(seconds=15))

        # Verifica se a situação 25 foi registrada corretamente
        situacao = Situacao(jogada=jogada, game=self.game)
        self.assertIn(25, situacao.casos_id)

    def test_registrar_caso26(self):
        """
        26: "Forma um agrupamento de mais de 6 peças com outro integrante",
        """
        # Jogador 1 e Jogador 2 formam um agrupamento juntos de mais de 6 peças
        self.peca1.set_posicao_atual(pos_x=86, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca1, tempo=timedelta(seconds=5))
        self.peca2.set_posicao_atual(pos_x=163, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca2, tempo=timedelta(seconds=10))
        self.peca3.set_posicao_atual(pos_x=239, pos_y=74, jogador=self.jogador2)
        self.game.add_jogada(peca=self.peca3, tempo=timedelta(seconds=15))
        self.peca4.set_posicao_atual(pos_x=316, pos_y=74, jogador=self.jogador2)
        self.game.add_jogada(peca=self.peca4, tempo=timedelta(seconds=20))
        self.peca5.set_posicao_atual(pos_x=393, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca5, tempo=timedelta(seconds=25))
        self.peca6.set_posicao_atual(pos_x=470, pos_y=74, jogador=self.jogador2)
        self.game.add_jogada(peca=self.peca6, tempo=timedelta(seconds=30))
        self.peca7.set_posicao_atual(pos_x=547, pos_y=74, jogador=self.jogador1)
        jogada = self.game.add_jogada(peca=self.peca7, tempo=timedelta(seconds=30))

        # Verifica se a situação 26 foi registrada corretamente
        situacao = Situacao(jogada=jogada, game=self.game)
        self.assertIn(26, situacao.casos_id)

    def test_registrar_caso27(self):
        """
        27: "Desenvolveu um agrupamento e outro integrante resolveu adicionar peças",
        """
        # Jogador 1 cria um agrupamento
        self.peca1.set_posicao_atual(pos_x=86, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca1, tempo=timedelta(seconds=5))
        self.peca2.set_posicao_atual(pos_x=163, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca2, tempo=timedelta(seconds=10))

        # Jogador 2 adiciona uma peça no agrupamento do Jogador 1
        self.peca3.set_posicao_atual(pos_x=239, pos_y=74, jogador=self.jogador2)

        Situacao(
            jogada=self.game.add_jogada(peca=self.peca3, tempo=timedelta(seconds=15)),
            game=self.game
        )

        # Jogada qualquer do Jogador 1
        self.peca4.set_posicao_atual(pos_x=316, pos_y=74, jogador=self.jogador1)
        jogada = self.game.add_jogada(peca=self.peca4, tempo=timedelta(seconds=20))

        # Verifica se a situação 27 foi registrada corretamente
        situacao = Situacao(jogada=jogada, game=self.game)
        self.assertIn(27, situacao.casos_id)

    def test_registrar_caso28(self):
        """
        28: "Desistiu Sozinho",
        """
        finalizacao = self.game.desistir(player=self.jogador1)
        situacao = Situacao(game=self.game, finalizacao=finalizacao)
        self.assertIn(28, situacao.casos_id)

    def test_registrar_caso29(self):
        """
        29: "Desistiu Sozinho com pouco tempo de jogo",
        """
        self.jogador1.tempo_em_jogo = timedelta(seconds=250)
        finalizacao = self.game.desistir(player=self.jogador1)
        situacao = Situacao(game=self.game, finalizacao=finalizacao)
        self.assertIn(29, situacao.casos_id)

    def test_registrar_caso30(self):
        """
        30: "Desistiu Sozinho e pouco tempo depois outro integrante desistiu",
        """
        self.jogador1.tempo_em_jogo = timedelta(seconds=200)

        Situacao(
            game=self.game,
            finalizacao=self.game.desistir(player=self.jogador1)
        )

        self.jogador2.tempo_em_jogo = timedelta(seconds=250)
        finalizacao = self.game.desistir(player=self.jogador2)

        Situacao(game=self.game, finalizacao=finalizacao)

        self.game.acabar_jogo()

        situacao = Situacao(game=self.game)
        self.assertIn(30, situacao.casos_id)

    def test_registrar_caso31(self):
        """
        31: "Desistiu depois de outro integrante Desistir",
        """
        self.game.desistir(player=self.jogador2)
        self.jogador1.tempo_em_jogo = timedelta(seconds=250)
        finalizacao = self.game.desistir(player=self.jogador1)
        situacao = Situacao(game=self.game, finalizacao=finalizacao)
        self.assertIn(31, situacao.casos_id)

    def test_registrar_caso32(self):
        """
        32: "Finalizou sozinho",
        """
        finalizacao = self.game.finalizar(player=self.jogador1)
        situacao = Situacao(game=self.game, finalizacao=finalizacao)
        self.assertIn(32, situacao.casos_id)

    def test_registrar_caso33(self):
        """
        33: "Finalizou sozinho com pouco tempo de jogo",
        """
        self.jogador1.tempo_em_jogo = timedelta(seconds=250)
        finalizacao = self.game.finalizar(player=self.jogador1)
        situacao = Situacao(game=self.game, finalizacao=finalizacao)
        self.assertIn(33, situacao.casos_id)

    def test_registrar_caso34(self):
        """
        34: "Finalizou depois de outro integrante Finalizar",
        """
        self.game.finalizar(player=self.jogador2)
        self.jogador1.tempo_em_jogo = timedelta(seconds=250)
        finalizacao = self.game.finalizar(player=self.jogador1)
        situacao = Situacao(game=self.game, finalizacao=finalizacao)
        self.assertIn(34, situacao.casos_id)

    def test_registrar_caso35(self):
        """
        35: "Finalizou Sozinho e pouco tempo depois outro integrante finalizou também",
        """
        self.jogador1.tempo_em_jogo = timedelta(seconds=200)
        Situacao(game=self.game, finalizacao=self.game.finalizar(player=self.jogador1))

        self.jogador2.tempo_em_jogo = timedelta(seconds=250)
        Situacao(game=self.game, finalizacao=self.game.finalizar(player=self.jogador2))

        self.game.acabar_jogo()

        situacao = Situacao(game=self.game)
        self.assertIn(35, situacao.casos_id)

    def test_registrar_caso36(self):
        """
        36: "Imitou a forma do mesmo agrupamento do outro (fez depois que outro integrante realizou a ação)",
        """
        # Jogador 1 cria um agrupamento
        self.peca1.set_posicao_atual(pos_x=86, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca1, tempo=timedelta(seconds=5))
        self.peca4.set_posicao_atual(pos_x=163, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca4, tempo=timedelta(seconds=10))

        # Jogador 2 imita a forma do agrupamento do Jogador 1
        self.peca3.set_posicao_atual(pos_x=86, pos_y=150, jogador=self.jogador2)
        self.game.add_jogada(peca=self.peca3, tempo=timedelta(seconds=15))
        self.peca2.set_posicao_atual(pos_x=163, pos_y=150, jogador=self.jogador2)
        jogada = self.game.add_jogada(peca=self.peca2, tempo=timedelta(seconds=20))

        # Verifica se a situação 36 foi registrada corretamente
        situacao = Situacao(jogada=jogada, game=self.game)
        self.assertIn(36, situacao.casos_id)

    def test_registrar_caso37(self):
        """
        37: "É imitado por alguém",
        """
        # Jogador 1 cria um agrupamento com duas peças vermelhas
        self.peca1.set_posicao_atual(pos_x=86, pos_y=74, jogador=self.jogador1)
        self.game.add_jogada(peca=self.peca1, tempo=timedelta(seconds=5))
        self.peca2.set_posicao_atual(pos_x=163, pos_y=74, jogador=self.jogador1)
        jogada1 = self.game.add_jogada(peca=self.peca2, tempo=timedelta(seconds=10))

        # Jogador 2 imita a forma do agrupamento do Jogador 1 com duas peças verdes
        self.peca3.set_posicao_atual(pos_x=86, pos_y=150, jogador=self.jogador2)
        self.game.add_jogada(peca=self.peca3, tempo=timedelta(seconds=15))
        self.peca4.set_posicao_atual(pos_x=163, pos_y=150, jogador=self.jogador2)
        self.game.add_jogada(peca=self.peca4, tempo=timedelta(seconds=20))

        # Verifica se a situação 37 foi registrada corretamente para o Jogador 1
        situacao1 = Situacao(jogada=jogada1, game=self.game)
        print("Casos identificados para Jogador 1:", situacao1.casos_id)
        self.assertIn(37, situacao1.casos_id)

    def test_registrar_caso38(self):
        """
        38: "Não realizou ações"
        """
        situacao = Situacao(game=self.game)
        self.assertIn(38, situacao.casos_id)


if __name__ == '__main__':
    unittest.main()
