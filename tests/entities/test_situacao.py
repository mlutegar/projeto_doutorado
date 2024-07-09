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
        pass

    def test_definir_situacao_caso7(self):
        """
        7: "Segurou uma peça por mais de 6 segundos por exemplo",
        """
        pass

    def test_registrar_caso9(self):
        self.jogada1.set_tempo(2)
        situacao = Situacao(self.jogada1)
        self.assertIn(9, situacao.casos_id)

    def test_registrar_caso11(self):
        self.jogada1.grupo.qtd_cores = 1
        situacao = Situacao(self.jogada1)
        self.assertIn(11, situacao.casos_id)

    def test_registrar_caso13(self):
        self.jogada1.grupo.qtd_cores = 2
        situacao = Situacao(self.jogada1)
        self.assertIn(13, situacao.casos_id)

    def test_registrar_caso14(self):
        # jogador 1 mexeu na peça do jogador 2 que estava em um grupo e devolveu para o monte
        self.peca4.set_player(self.jogador1)
        self.peca4.set_posicao((99, 99))

        self.game.add_jogada()
        jogada_nova = self.game.jogadas[5]
        jogada_nova.set_peca(self.peca4)
        jogada_nova.set_tempo(5)

        situacao = Situacao(jogada_nova)
        self.assertIn(14, situacao.casos_id)

    def test_registrar_caso15(self):
        # jogador 1 mexeu na peça do jogador 2 que estava em um grupo e colocou em um grupo dele
        self.peca4.set_player(self.jogador1)
        self.peca4.set_posicao((1, 5))

        self.game.add_jogada()
        jogada_nova = self.game.jogadas[5]
        jogada_nova.set_peca(self.peca4)
        jogada_nova.set_tempo(5)

        situacao = Situacao(jogada_nova)
        self.assertIn(15, situacao.casos_id)

    def test_registrar_caso16(self):
        # jogador 1 mexeu na peça do jogador 2 que estava em um grupo e colocou em um lugar aleatório
        self.peca4.set_player(self.jogador1)
        self.peca4.set_posicao((11, 9))

        self.game.add_jogada()
        jogada_nova = self.game.jogadas[5]
        jogada_nova.set_peca(self.peca4)
        jogada_nova.set_tempo(5)

        situacao = Situacao(jogada_nova)
        self.assertIn(16, situacao.casos_id)

    def test_registrar_caso18(self):
        # jogador 1 mexeu na peça do jogador 1 que estava em um grupo e devolveu para o monte
        self.peca.set_posicao((99, 99))

        self.game.add_jogada()
        jogada_nova = self.game.jogadas[5]
        jogada_nova.set_peca(self.peca)
        jogada_nova.set_tempo(5)

        situacao = Situacao(jogada_nova)
        self.assertIn(18, situacao.casos_id)

    def test_registrar_caso19(self):
        # jogador 1 mexeu na peça do jogador 1 que estava em um grupo e colocou em um lugar aleatório
        self.peca.set_posicao((7, 9))

        self.game.add_jogada()
        jogada_nova = self.game.jogadas[5]
        jogada_nova.set_peca(self.peca)
        jogada_nova.set_tempo(5)

        situacao = Situacao(jogada_nova)
        self.assertIn(19, situacao.casos_id)

    def test_to_dict(self):
        situacao = Situacao(self.jogada1)
        situacao_dict = situacao.to_dict()
        self.assertEqual(situacao_dict['id'], self.jogada1.id)
        self.assertEqual(situacao_dict['casos_id'], situacao.casos_id)
        self.assertEqual(situacao_dict['casos_descricao'], situacao.casos_descricao)


if __name__ == '__main__':
    unittest.main()
