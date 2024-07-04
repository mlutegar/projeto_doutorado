import unittest
from entities.grupo import Grupo, grupos
from entities.jogada import Jogada
from entities.peca import Peca
from entities.jogador import Jogador
from entities.situacao import Situacao


class TestSituacao(unittest.TestCase):

    def setUp(self):
        self.jogador = Jogador()
        self.jogador.set_nome("jogador_teste")

        self.peca = Peca()
        self.peca.set_uid(1)
        self.peca.set_cor("vermelha")
        self.peca.set_posicao((1, 1))
        self.peca.set_player(self.jogador)

        self.peca2 = Peca()
        self.peca2.set_uid(2)
        self.peca2.set_cor("vermelha")
        self.peca2.set_posicao((1, 3))
        self.peca2.set_player(self.jogador)

        self.grupo = Grupo()
        self.grupo.add_peca(self.peca)

        self.jogada = Jogada()
        self.jogada.set_peca(self.peca)
        self.jogada.set_grupo(self.grupo)
        self.jogada.set_jogador(self.jogador)
        self.jogada.set_tempo(5)

        grupos.clear()
        grupos.append(self.grupo)

    def test_definir_situacao_caso1(self):
        self.jogada.grupo.criador = None
        situacao = Situacao(self.jogada)
        self.assertIn(1, situacao.casos_id)

    def test_definir_situacao_caso2(self):
        self.jogada.grupo.qtd_pecas = 2
        situacao = Situacao(self.jogada)
        self.assertIn(2, situacao.casos_id)

    def test_definir_situacao_caso3(self):
        self.jogada.grupo.qtd_pecas = 4
        situacao = Situacao(self.jogada)
        self.assertIn(3, situacao.casos_id)

    def test_definir_situacao_caso4(self):
        self.jogada.grupo.qtd_pecas = 7
        situacao = Situacao(self.jogada)
        self.assertIn(4, situacao.casos_id)

    def test_registrar_caso7(self):
        self.jogada.set_tempo(7)
        situacao = Situacao(self.jogada)
        self.assertIn(7, situacao.casos_id)

    def test_registrar_caso9(self):
        self.jogada.set_tempo(2)
        situacao = Situacao(self.jogada)
        self.assertIn(9, situacao.casos_id)

    def test_registrar_caso11(self):
        self.jogada.grupo.qtd_cores = 1
        situacao = Situacao(self.jogada)
        self.assertIn(11, situacao.casos_id)

    def test_registrar_caso13(self):
        self.jogada.grupo.qtd_cores = 2
        situacao = Situacao(self.jogada)
        self.assertIn(13, situacao.casos_id)

    def test_registrar_caso14(self):
        self.jogada.peca.set_posicao((99, 99))
        situacao = Situacao(self.jogada)
        self.assertIn(14, situacao.casos_id)

    def test_to_dict(self):
        situacao = Situacao(self.jogada)
        situacao_dict = situacao.to_dict()
        self.assertEqual(situacao_dict['id'], self.jogada.id)
        self.assertEqual(situacao_dict['casos_id'], situacao.casos_id)
        self.assertEqual(situacao_dict['casos_descricao'], situacao.casos_descricao)


if __name__ == '__main__':
    unittest.main()
