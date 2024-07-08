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

    def test_definir_situacao_caso1(self):
        """
        1: "Pegou a peça e largou em algum lugar Aleatório",
        """
        self.peca1.set_posicao_atual(
            pos_x=86, pos_y=74, jogador=self.jogador1
        )

        situacao = Situacao(
            self.game.add_jogada(
                peca=self.peca1, tempo=timedelta(seconds=5)
            ),
            self.game
        )

        self.assertIn(1, situacao.casos_id)

    def test_definir_situacao_caso2(self):
        self.jogada1.grupo.criador = self.jogada1.peca.jogador
        self.jogada1.grupo.qtd_pecas = 2
        situacao = Situacao(self.jogada1)
        self.assertIn(2, situacao.casos_id)

    def test_definir_situacao_caso3(self):
        self.jogada1.grupo.qtd_pecas = 4
        situacao = Situacao(self.jogada1)
        self.assertIn(3, situacao.casos_id)

    def test_definir_situacao_caso4(self):
        self.jogada1.grupo.qtd_pecas = 7
        situacao = Situacao(self.jogada1)
        self.assertIn(4, situacao.casos_id)

    def test_registrar_caso7(self):
        self.jogada1.set_tempo(7)
        situacao = Situacao(self.jogada1)
        self.assertIn(7, situacao.casos_id)

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
