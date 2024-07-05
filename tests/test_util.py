import unittest
from util import (
    process_data
)
from entities.jogador import jogadores
from entities.peca import Peca, pecas, tem_lateral_vizinho, tem_lateral_diagonal
from entities.grupo import Grupo, grupos, get_grupo_by_peca_pai
from entities.jogada import jogadas


class TestUtil(unittest.TestCase):
    def setUp(self):
        # Limpa os estados globais antes de cada teste
        grupos.clear()
        pecas.clear()
        jogadores.clear()
        jogadas.clear()

    def test_get_grupo_by_peca_pai(self):
        peca1 = Peca(1)
        peca2 = Peca(2)
        grupo1 = Grupo(peca1)

        self.assertEqual(get_grupo_by_peca_pai(peca1), grupo1)
        self.assertIsNone(get_grupo_by_peca_pai(peca2))

    def test_tem_lateral_vizinho(self):
        pos1 = (1, 1)
        pos2 = (1, 3)
        self.assertTrue(tem_lateral_vizinho(pos1, pos2))

        pos3 = (1, 4)
        self.assertFalse(tem_lateral_vizinho(pos1, pos3))

    def test_tem_lateral_diagonal(self):
        pos1 = (1, 1)
        pos2 = (2, 2)
        self.assertTrue(tem_lateral_diagonal(pos1, pos2))

        pos3 = (2, 3)
        self.assertFalse(tem_lateral_diagonal(pos1, pos3))

    def test_process_data(self):
        move = {
            "UID": 1,
            "PosX": 200,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "Jogador1",
            "Cor": "vermelho",
        }
        process_data(move)

        self.assertEqual(len(pecas), 1)
        self.assertEqual(len(jogadas), 1)
        self.assertEqual(pecas[1].uid, 1)
        self.assertEqual(pecas[1].posicao_atual, [1, 4])
