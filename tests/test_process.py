import unittest

from process import *
from entities.game import Game


class TestProcessData(unittest.TestCase):

    def setUp(self):
        self.game = Game("teste", "host")

    def test_process_data(self):
        move = {
            "UID": 1,
            "PosX": 86,
            "PosY": 74,
            "Tempo": 5,
            "Jogador": "jogador1",
            "Cor": "vermelha"
        }

        process_data(self.game, move)

        self.assertIn(1, self.game.pecas)
        self.assertIn("jogador1", self.game.jogadores)
        self.assertEqual(self.game.pecas[1].posicao, (1, 1))
        self.assertEqual(self.game.pecas[1].jogador.nome, "jogador1")


if __name__ == '__main__':
    unittest.main()
