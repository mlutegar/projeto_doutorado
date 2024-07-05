import unittest
from entities.jogada import Jogada
from entities.peca import Peca
from entities.jogador import Jogador
from entities.situacao import Situacao


class TestSituacao(unittest.TestCase):

    def setUp(self):
        # O jogador 1 vai mexer na peça 1 e colocar em uma posição aleatória
        self.jogador1 = Jogador("jogador1")

        self.peca = Peca(1)
        self.peca.set_cor("vermelha")
        self.peca.set_posicao((1, 1))
        self.peca.set_player(self.jogador1)

        self.jogada1 = Jogada()
        self.jogada1.set_peca(self.peca)
        self.jogada1.set_tempo(5)

        # O jogador 1 vai mexer na peça 2 e colocar ao lado da peça 1 criando um grupo
        self.peca2 = Peca(2)
        self.peca2.set_cor("vermelha")
        self.peca2.set_posicao((1, 3))
        self.peca2.set_player(self.jogador1)

        self.jogada2 = Jogada()
        self.jogada2.set_peca(self.peca2)
        self.jogada2.set_tempo(5)

        # O jogador 2 vai mexer nas peças 3 e colocar em uma posição aleatória
        self.jogador2 = Jogador("jogador2")

        self.peca3 = Peca(3)
        self.peca3.set_cor("vermelha")
        self.peca3.set_posicao((5, 1))
        self.peca3.set_player(self.jogador2)

        self.jogada3 = Jogada()
        self.jogada3.set_peca(self.peca3)
        self.jogada3.set_tempo(5)

        # O jogador 2 vai mexer na peça 4 e colocar ao lado da peça 3 criando um grupo

        self.peca4 = Peca(4)
        self.peca4.set_cor("vermelha")
        self.peca4.set_posicao((5, 3))
        self.peca4.set_player(self.jogador2)

        self.jogada4 = Jogada()
        self.jogada4.set_peca(self.peca4)
        self.jogada4.set_tempo(5)

    def test_definir_situacao_caso1(self):
        self.jogada1.grupo.criador = None
        situacao = Situacao(self.jogada1)
        self.assertIn(1, situacao.casos_id)

    def test_definir_situacao_caso2(self):
        self.jogada1.grupo.criador = self.jogada1.jogador_jogada
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

        jogada_nova = Jogada()
        jogada_nova.set_peca(self.peca4)
        jogada_nova.set_tempo(5)

        situacao = Situacao(jogada_nova)
        self.assertIn(14, situacao.casos_id)

    def test_registrar_caso15(self):
        # jogador 1 mexeu na peça do jogador 2 que estava em um grupo e colocou em um grupo dele
        self.peca4.set_player(self.jogador1)
        self.peca4.set_posicao((1, 5))

        jogada_nova = Jogada()
        jogada_nova.set_peca(self.peca4)
        jogada_nova.set_tempo(5)

        situacao = Situacao(jogada_nova)
        self.assertIn(15, situacao.casos_id)

    def test_registrar_caso16(self):
        # jogador 1 mexeu na peça do jogador 2 que estava em um grupo e colocou em um lugar aleatório
        self.peca4.set_player(self.jogador1)
        self.peca4.set_posicao((11, 9))

        jogada_nova = Jogada()
        jogada_nova.set_peca(self.peca4)
        jogada_nova.set_tempo(5)

        situacao = Situacao(jogada_nova)
        self.assertIn(16, situacao.casos_id)

    def test_registrar_caso18(self):
        # jogador 1 mexeu na peça do jogador 1 que estava em um grupo e devolveu para o monte
        self.peca.set_posicao((99, 99))

        jogada_nova = Jogada()
        jogada_nova.set_peca(self.peca)
        jogada_nova.set_tempo(5)

        situacao = Situacao(jogada_nova)
        self.assertIn(18, situacao.casos_id)

    def test_registrar_caso19(self):
        # jogador 1 mexeu na peça do jogador 1 que estava em um grupo e colocou em um lugar aleatório
        self.peca.set_posicao((7, 9))

        jogada_nova = Jogada()
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
