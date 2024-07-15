import unittest
from datetime import timedelta

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
        jogada = self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=10)
        )

        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

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
            pos_x=239, pos_y=74, jogador=self.jogador2
        )
        self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=15)
        )

        # Jogador 2 remove a peça do agrupamento
        self.peca3.set_posicao_atual(
            pos_x=300, pos_y=74, jogador=self.jogador1
        )
        self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=20)
        )

        # Jogador 1 adiciona novamente a peça no agrupamento do Jogador 2
        self.peca3.set_posicao_atual(
            pos_x=239, pos_y=74, jogador=self.jogador2
        )
        jogada = self.game.add_jogada(
            peca=self.peca3, tempo=timedelta(seconds=25)
        )

        situacao = Situacao(
            jogada=jogada,
            game=self.game
        )

        self.assertIn(10, situacao.casos_id)

    def test_registrar_caso11(self):
        """
        11: "Agrupou peças de cor igual",
        """
        pass

    def test_registrar_caso12(self):
        """
        12: "Criou um agrupamento contendo peças iguais e diferentes. Exemplo: Duas amarelas e duas pretas",
        """
        pass

    def test_registrar_caso13(self):
        """
        13: "Agrupou peças de cores diferentes",
        """
        pass

    def test_registrar_caso14(self):
        """
        14: "Retirou peças do Agrupamento do outro integrante e devolveu para o monte",
        """
        pass

    def test_registrar_caso15(self):
        """
        15: "Retirou peças do Agrupamento do outro integrante e colocou no seu próprio agrupamento",
        """
        pass

    def test_registrar_caso16(self):
        """
        16: "Retirou peças do Agrupamento do outro integrante e colocou em um lugar aleatório",
        """
        pass

    def test_registrar_caso17(self):
        """
        17: "Trocou a posição da própria peça",
        """
        pass

    def test_registrar_caso18(self):
        """
        18: "Retirou peças do próprio Agrupamento e devolveu para o monte",
        """
        pass

    def test_registrar_caso19(self):
        """
        19: "Retirou peças do próprio agrupamento e colocou em algum lugar aleatório",
        """
        pass

    def test_registrar_caso20(self):
        """
        20: "Retirou peças dos outros integrantes que adicionaram no agrupamento feito por ele",
        """
        pass

    def test_registrar_caso21(self):
        """
        21: "Criou mais de um agrupamento",
        """
        pass

    def test_registrar_caso22(self):
        """
        22: "Conecta dois ou mais agrupamentos com outros participantes",
        """
        pass

    def test_registrar_caso23(self):
        """
        23: "Conecta dois ou mais agrupamentos consigo mesmo",
        """
        pass

    def test_registrar_caso24(self):
        """
        24: "Forma um agrupamento de 2 peças com outro integrante",
        """
        pass

    def test_registrar_caso25(self):
        """
        25: "Forma um agrupamento de 3 a 6 peças com outro integrante",
        """
        pass

    def test_registrar_caso26(self):
        """
        26: "Forma um agrupamento de mais de 6 peças com outro integrante",
        """
        pass

    def test_registrar_caso27(self):
        """
        27: "Desenvolveu um agrupamento e outro integrante resolveu adicionar peças",
        """
        pass

    def test_registrar_caso28(self):
        """
        28: "Desistiu Sozinho",
        """
        pass

    def test_registrar_caso29(self):
        """
        29: "Desistiu Sozinho com pouco tempo de jogo",
        """
        pass

    def test_registrar_caso30(self):
        """
        30: "Desistiu Sozinho e pouco tempo depois outro integrante desistiu",
        """
        pass

    def test_registrar_caso31(self):
        """
        31: "Desistiu depois de outro integrante Desistir",
        """
        pass

    def test_registrar_caso32(self):
        """
        32: "Finalizou sozinho",
        """
        pass

    def test_registrar_caso33(self):
        """
        33: "Finalizou sozinho com pouco tempo de jogo",
        """
        pass

    def test_registrar_caso34(self):
        """
        34: "Finalizou depois de outro integrante Finalizar",
        """
        pass

    def test_registrar_caso35(self):
        """
        35: "Finalizou Sozinho e pouco tempo depois outro integrante finalizou também",
        """
        pass

    def test_registrar_caso36(self):
        """
        36: "Imitou a forma do mesmo agrupamento do outro (fez depois que outro integrante realizou a ação)",
        """
        pass

    def test_registrar_caso37(self):
        """
        37: "É imitado por alguém",
        """
        pass

    def test_registrar_caso38(self):
        """
        38: "Não realizou ações"
        """
        pass


if __name__ == '__main__':
    unittest.main()
